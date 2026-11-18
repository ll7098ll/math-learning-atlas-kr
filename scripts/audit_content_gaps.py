"""Read existing content and rerun non-regenerating checks for a gap report.

Writes only the requested new audit JSON. Existing authoring data, generated
pages, deployment records and earlier audit results are left untouched.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'tmp/pathways-release'


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    standards = read('data/standards.json')['standards']
    files = sorted((ROOT / 'data').glob('goal_hierarchy_*.json'))
    corpora = [json.loads(p.read_text(encoding='utf-8')) for p in files]
    entries = [e for d in corpora for e in d['entries']]
    goals = [g for e in entries for g in e['goals']]
    cases = [c for d in corpora for c in d['cases']]
    active_cases = [c for c in cases if not c.get('superseded_by_case_ids')]
    codes = {s['code'] for s in standards}
    source_files = [ROOT / 'data/standards.json', *files,
                    *sorted((ROOT / 'data').glob('revisions_*.json')),
                    ROOT / 'data/revised_relations.json',
                    ROOT / 'data/concept_taxonomy.json']
    root_site_diff = []
    for p in source_files:
        q = SITE / 'research' / p.relative_to(ROOT)
        if not q.exists() or sha(p) != sha(q):
            root_site_diff.append(p.relative_to(ROOT).as_posix())
    catalog = read('tmp/pathways-release/dist/content/catalog.json')
    checks = []
    py_names = ['test_hierarchy_review.py', 'test_goal_hierarchy.py',
                'test_content_objects.py', 'test_portal_retention.py',
                *sorted(p.name for p in (ROOT / 'scripts').glob('check_*.py'))]
    for name in py_names:
        checks.append(([sys.executable, '-X', 'utf8', str(ROOT / 'scripts' / name)], ROOT))
    for name in ['test_goal_network.mjs', 'test_task_pathways.mjs',
                 'test_all_concept_pathways.mjs', 'test_school_revision.mjs',
                 'test_catalog_groups.mjs']:
        checks.append(([shutil.which('node') or 'node', str(SITE / 'tests' / name)], SITE))
    checks.append(([sys.executable, '-X', 'utf8', str(ROOT / 'scripts/plan_portal_retention.py'), '--verify-only'], ROOT))

    def run(item):
        command, cwd = item
        try:
            p = subprocess.run(command, cwd=cwd, capture_output=True,
                               encoding='utf-8', errors='replace', timeout=120)
            return dict(command=command, exit_code=p.returncode,
                        status='pass' if p.returncode == 0 else 'fail',
                        stdout=p.stdout.strip(), stderr=p.stderr.strip())
        except Exception as e:
            return dict(command=command, status='error', error=str(e))

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, checks))

    # In-memory mutation only: demonstrate whether the loader can accept a
    # future documented review without changing any author's stored status.
    from goal_hierarchy import load_goal_hierarchies
    load_goal_hierarchies(standards)
    selected = files[0]
    original_reader = Path.read_text
    promotion_checks = []
    for field, value in [('state', 'independently_reviewed'),
                         ('independent_review', True), ('student_validated', True)]:
        changed = json.loads(original_reader(selected, encoding='utf-8'))
        changed['entries'][0]['review'][field] = value
        changed['entries'][0]['review']['evidence'] = 'In-memory audit fixture only'
        payload = json.dumps(changed, ensure_ascii=False)

        def patched_reader(path, *a, **kw):
            return payload if path == selected else original_reader(path, *a, **kw)

        try:
            with patch.object(Path, 'read_text', patched_reader):
                load_goal_hierarchies(standards)
            outcome = 'accepted'
        except AssertionError:
            outcome = 'rejected_by_assertion'
        promotion_checks.append(dict(field=field, value=value, outcome=outcome))

    registry = read('data/analysis_registry.json')
    graph_audit = read('data/goal_network_audit.json')
    relation_records = read('data/revised_relations.json')['relations']
    standard_relations = [r for r in relation_records
                          if r['from'].startswith('standard:') and r['to'].startswith('standard:')]
    review_registry = read('data/hierarchy_review_registry.json')['relations']
    relation_status = Counter(review_registry.get(r['id'], {}).get('state', 'unrecorded') for r in standard_relations)
    source_status = Counter(s['sourceReview'] for s in catalog['standards'])
    audit_hash_mismatches = []
    for rel, digest in graph_audit['source_hashes'].items():
        if sha(ROOT / rel) != digest:
            audit_hash_mismatches.append(rel)
    result = dict(
        generated_at=datetime.now(timezone(timedelta(hours=9))).isoformat(),
        scope='Local supplied curriculum corpus; current national revisions and live deployment not reverified.',
        counts=dict(standards=len(standards), school_levels=dict(Counter(s['school_level'] for s in standards)),
                    high_school_subjects=len({s['subject'] for s in standards if s['school_level']=='고등학교'}),
                    goal_files=len(files), goal_entries=len(entries), goals=len(goals),
                    goal_count_distribution=dict(Counter(len(e['goals']) for e in entries)),
                    goal_cases=len(cases), active_goal_cases=len(active_cases),
                    routes=sum(len(c['routes']) for c in active_cases),
                    concept_groups=len(read('data/concept_taxonomy.json')['groups']),
                    standard_relations=len(standard_relations)),
        coverage=dict(missing_goal_entries=sorted(codes-{e['code'] for e in entries}),
                      missing_analysis_files=sorted(c for c in codes if not (ROOT/'analyses'/f'{c}.md').is_file()),
                      duplicate_goal_entries=[c for c,n in Counter(e['code'] for e in entries).items() if n>1]),
        statuses=dict(analysis=dict(Counter(e['status'] for e in registry)),
                      student_validated_analyses=sum(bool(e['student_response_validation']) for e in registry),
                      source_review=dict(source_status), relation_review=dict(relation_status)),
        root_site_compared_files=len(source_files), root_site_mismatches=root_site_diff,
        prior_goal_audit_hash_mismatches=audit_hash_mismatches,
        goal_network_coverage=graph_audit['coverage'],
        review_promotion_simulation=promotion_checks,
        simulation_interpretation='Loader rejects state changes before considering evidence; no real review was performed or recorded.',
        source_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in source_files},
        check_summary=dict(total=len(results), counts=dict(Counter(r['status'] for r in results))),
        checks=results,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['counts','coverage','statuses','root_site_mismatches','prior_goal_audit_hash_mismatches','review_promotion_simulation','check_summary']}, ensure_ascii=False, indent=2))
    return int(any(r['status'] != 'pass' for r in results))


if __name__ == '__main__':
    raise SystemExit(main())

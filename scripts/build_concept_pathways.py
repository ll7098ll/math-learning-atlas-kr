"""Extend recorded expansion paths to every concept; never infer prerequisites."""
import argparse
import hashlib
import json
from pathlib import Path
from hierarchy_review import load_registry, reviewed_record
from content_objects import write_content_object

ROOT = Path(__file__).resolve().parents[1]


def build(site):
    content = site / 'dist' / 'content'
    read = lambda name: json.loads((content / f'{name}.json').read_text(encoding='utf-8'))
    catalog, flows, relations, pilot = [read(n) for n in ('catalog', 'flows', 'connections', 'hierarchy')]
    assert len({d['version'] for d in (catalog, flows, relations, pilot)}) == 1
    standards = {s['code']: s for s in catalog['standards']}
    records = [r for r in relations['relations'] if r['from'].startswith('standard:') and r['to'].startswith('standard:')]
    source_ids = {s['id'] for s in relations['sources']}
    registry = load_registry(ROOT, standards, [r['id'] for r in records])
    groups, datasets = [], {}
    for concept in flows['strands']:
        members = list(dict.fromkeys(c for stage in concept['stages'] for c in stage['codes']))
        member_set = set(members)
        selected = [r for r in records if r['from'][9:] in member_set or r['to'][9:] in member_set]
        ids = member_set | {r[k][9:] for r in selected for k in ('from', 'to')}
        nodes = [{'id': c, 'member': c in member_set,
                  'hierarchy_review': registry.get('standards', {}).get(c, {}).get('state', 'unreviewed'),
                  'goal_analysis_review': registry.get('standards', {}).get(c, {}).get('goal_analysis', {}).get('review_state', 'unreviewed'),
                  'goal_analysis_scope': registry.get('standards', {}).get(c, {}).get('goal_analysis', {}).get('scope', ''),
                  'order_decision': registry.get('standards', {}).get(c, {}).get('order_decision')} for c in standards if c in ids]
        edges = []
        for r in selected:
            assert r['from'][9:] in standards and r['to'][9:] in standards
            assert all(i in source_ids for i in r.get('source_ids', []))
            edges.append({**reviewed_record(r, registry),
                          'order_role': 'meaning_expansion' if r['type'] in ('generalizes','requires_for_task') and r.get('review_state') != 'candidate' else 'unordered_connection'})
        expansions = sum(r['order_role'] == 'meaning_expansion' for r in edges)
        pilots = [m['id'] for m in pilot['hierarchy']['maps'] if any(c in member_set for n in m['nodes'] for c in n['standards'])]
        summary = {'id': concept['id'], 'title': concept['title'], 'domain': concept['domain'],
                   'question': concept['question'], 'member_codes': members,
                   'members': len(members), 'related_nodes': len(nodes) - len(members),
                   'relations': len(edges), 'expansions': expansions, 'reviewed': sum(r['independent_review'] for r in edges),
                   'hierarchy_status': 'expansion_draft' if expansions else 'order_unreviewed', 'pilot_maps': pilots}
        summary['by_scope'] = {}
        for scope, level in [('e','초등학교'),('m','중학교'),('h','고등학교')]:
            local = [r for r in edges if standards[r['from'][9:]]['level'] == level and standards[r['to'][9:]]['level'] == level]
            n = sum(standards[c]['level'] == level for c in members)
            count = sum(r['order_role'] == 'meaning_expansion' for r in local)
            summary['by_scope'][scope] = {'members': n, 'relations': len(local), 'expansions': count, 'hierarchy_status': 'expansion_draft' if count else 'order_unreviewed'}
        groups.append(summary)
        used_sources = {i for e in edges for i in e.get('source_ids', [])}
        datasets[concept['id']] = {'version': catalog['version'], 'concept': summary, 'nodes': nodes,
                                  'relations': edges, 'sources': [s for s in relations['sources'] if s['id'] in used_sources]}
    decision_ids = {rid for e in registry.get('standards', {}).values() for rid in e.get('order_decision', {}).get('relation_ids', [])}
    graph = {'version': catalog['version'], 'nodes': list(standards),
             'context_relations': [reviewed_record(r, registry) for r in records if r['id'] in decision_ids],
             'standard_decisions': {c: e['order_decision'] for c, e in registry.get('standards', {}).items() if e.get('order_decision')},
             'relations': [reviewed_record(r, registry) for r in records if r['type'] in ('generalizes', 'requires_for_task') and r.get('review_state') != 'candidate'],
             'sources': relations['sources']}
    encoded = json.dumps({'datasets': datasets, 'graph': graph}, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    dataset_version = hashlib.sha256(encoded.encode('utf-8')).hexdigest()[:16]
    def write(path, obj):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    files={key:write_content_object(content,'concept-pathways',data) for key,data in datasets.items()}
    files['graph']=write_content_object(content,'concept-pathways',graph)
    index = {'version': catalog['version'], 'datasetVersion': dataset_version, 'files': files, 'groups': groups,
             'coverage': {'concepts': len(groups), 'standards': len(standards),
                          'relations': len(records), 'independently_reviewed_hierarchies': sum(all(registry.get('standards', {}).get(c, {}).get('independent_review', False) for c in g['member_codes']) for g in groups)},
             'interpretation': '이 지도는 기준 간 의미 확장과 과제별 조건의 기존 기록을 제공하며 관계별 실제 검토 상태를 보존한다. 하위 목표별 출발 조건·대안·후속 활용은 목표별 위계 원장에서 확인한다. 학년순·유사도순으로 선수 조건을 생성하지 않는다.'}
    write(content / 'concept-pathways-index.json', index)
    return {**index['coverage'], 'datasetVersion': dataset_version,
            'with_expansion': sum(g['expansions'] > 0 for g in groups),
            'without_expansion': sum(g['expansions'] == 0 for g in groups),
            'largest_bytes': max((content / 'concept-pathways' / 'items' / (files[g['id']]+'.json')).stat().st_size for g in groups)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--site-dir', type=Path, default=ROOT if (ROOT / 'dist').is_dir() else ROOT / 'portal' / 'math-atlas')
    print(json.dumps(build(parser.parse_args().site_dir), ensure_ascii=False))

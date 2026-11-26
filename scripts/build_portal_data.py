"""Export the existing research corpus to the dependency-free portal.

Run again after editing the source JSON or analysis Markdown. The portal does
not infer prerequisite relations from grade order or from similar words.
"""
import json
import re
import shutil
import hashlib
from pathlib import Path
from full_concepts import compile_flows

ROOT = Path(__file__).resolve().parents[1]
import os
OUT = Path(os.environ.get('MATH_ATLAS_DIST', ROOT.parent / 'dist' if ROOT.name == 'research' else ROOT / 'tmp' / 'pathways-release' / 'dist'))


def load(name):
    return json.loads((ROOT / 'data' / f'{name}.json').read_text(encoding='utf-8'))


def tables(text, heading):
    section = re.search(r'^## ' + heading + r'[^\n]*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not section:
        return []
    rows = []
    for line in section[1].splitlines():
        if line.startswith('|'):
            cells = [s.strip() for s in re.split(r'(?<!\\)\|', line.strip('|'))]
            if not all(re.fullmatch(r'[-: ]+', c) for c in cells):
                rows.append(cells)
    return rows[1:]


def sections(text):
    return [{'title': m[1].strip(), 'body': m[2].strip()} for m in
            re.finditer(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)', text, re.M | re.S)]


def normalized_steps(values):
    result = []
    for row in values:
        cells = row.split('|') if isinstance(row, str) else row
        result.append({'label': cells[0], 'meaning': cells[1] if len(cells) > 1 else '',
                       'observable': cells[2] if len(cells) > 2 else '',
                       'conditions': cells[3] if len(cells) > 3 else ''})
    return result


def main():
    inventory = load('standards')
    source_scope = {r['code']: r['state'] for r in load('content_review_queue').get('full_scope_source_review', [])}
    details = load('analysis_details')
    entries = {x['code']: x for x in details['analyses']}
    secondary = load('secondary_analysis_details')
    secondary_entries = {x['code']: x for x in secondary['analyses']}
    analyses = {}
    initial_cases = load('initial_case_studies') if (ROOT/'data/initial_case_studies.json').exists() else {}
    for item in load('analysis_registry'):
        code = item['code']
        text = initial_cases.get(code) or (ROOT / item['file']).read_text(encoding='utf-8')
        entry = entries.get(code) or secondary_entries.get(code)
        family = (details['families'][entry['family']] if code in entries else secondary['profiles'][entry['family']]) if entry else None
        def rows(values):
            return [x.split('|') if isinstance(x, str) else x for x in values]
        title = re.sub(r'\s*상세 분석 초안$', '', text.splitlines()[0].lstrip('# '))
        analyses[code] = {
            'title': title, 'markdown': text, 'status': item['status'],
            'validated': item['student_response_validation'],
            'task': entry['task'] if entry else next((p for p in text.split('\n\n') if p.startswith('대표 과제')), ''),
            'idea': entry['idea'] if entry else text.split('\n\n')[1],
            'steps': rows(entry['steps']) if entry else (tables(text, '목표의 하위요소') or tables(text, '공통 하위요소')),
            'processes': rows(family.get('processes', [])) if family else [],
            'probes': rows(entry['probes']) if entry else (tables(text, '진단 과제') or tables(text, '오류와 진단')),
            'commonProbe': entry.get('common_probe', []) if entry else [],
            'paths': entry.get('paths', family['paths']) if entry else [],
            'bridge': entry.get('bridge', '') if entry else '',
            'limit': entry['limit'] if entry else '대표 과제와 선택한 경로의 조건을 확인한다. 모든 학생에게 같은 학습 순서를 가정하지 않는다.',
            'precursors': entry.get('precursors', entry.get('prior', [])) if entry else [],
            'subgoals': entry.get('branches', []) if entry else [],
            'family': entry['family'] if entry else {'6수01-10': 'divide', '6수02-03': 'ratio', '6수03-14': 'area'}[code],
        }
        a = analyses[code]
        a['sections'] = sections(text)
        if not entry:
            path_sections = [s for s in a['sections'] if any(w in s['title'] for w in ['경로', '수행 과정'])]
            a['paths'] = [s['body'] for s in path_sections]
            if not a['task']:
                a['task'] = '\n\n'.join(p for s in path_sections for p in s['body'].split('\n\n') if '대표 수치' in p)
        a['stepObjects'] = normalized_steps(a['steps'])
        a['probeObjects'] = [dict(zip(['question', 'expected', 'interpretation', 'followup'], row + [''] * (4 - len(row)))) for row in a['probes']]
        a['profile'] = family or {}
    standards = []
    for s in inventory['standards']:
        review_state = source_scope.get(s['code'], 'unreviewed')
        review_label = s.get('source_review_status', '미대조')
        if review_state == 'self_checked_source_image':
            review_label += ' · 문장·해설·고려 사항 자체 대조'
        elif review_state == 'statement_image_only_requires_full_scope_review':
            review_label += ' · 문장·수식 범위, 해설·고려 사항 확인 전'
        elif review_state == 'needs_re_review':
            review_label += ' · 변경 후 재대조 필요'
        standards.append({
            'code': s['code'], 'level': s['school_level'], 'band': s['grade_band'],
            'domain': s['domain'], 'subject': s['subject'], 'category': s['subject_category'],
            'statement': s.get('statement_display', s['statement_extracted']),
            'title': analyses[s['code']]['title'] if s['code'] in analyses else s.get('statement_display', s['statement_extracted']),
            'pdfPages': s['source_pdf_pages'], 'printedPages': s['source_printed_pages'],
            'sourceReview': review_label, 'sourceReviewState': review_state,
            'extracted': s['statement_extracted'],
            'sourceId': s['source_id'], 'domainCode': s['domain_code'],
        })
    relations = load('relations')['relations']
    from detailed_revision import apply as apply_revisions
    relations = apply_revisions(analyses, inventory, relations)
    standard_edges = [x for x in relations if x['from'].startswith('standard:') and x['to'].startswith('standard:')]
    data = {
        'meta': {'curriculum': inventory['curriculum_version'], 'source': inventory['source_file'],
                 'sourceSha256': inventory['source_sha256'], 'elementary': sum(s['level'] == '초등학교' for s in standards),
                 'standards': len(standards), 'elements': len(load('elements')['elements']),
                 'individualRevisionDrafts': sum(a.get('schemaVersion') == 2 for a in analyses.values()), 'standardConnections': len(standard_edges), 'reviewed': sum(a['status'] == '검토 완료' for a in analyses.values()), 'studentValidated': sum(a['validated'] is True for a in analyses.values())},
        'standards': standards, 'analyses': analyses, 'families': details['families'],
        'elements': load('elements')['elements'], 'relations': relations, 'sources': load('sources'),
        'hierarchy': load('hierarchy_pilot'),
        'conceptFlows': compile_flows(load('concept_taxonomy'), standards, relations),
        'essay': (ROOT / 'analyses' / '나눗셈분수비율연결.md').read_text(encoding='utf-8'),
    }
    assert len(analyses) == len(standards)
    assert all(s['code'] in analyses for s in standards)
    assert all(analyses[c]['steps'] and analyses[c]['probes'] for c in analyses)
    for m in data['hierarchy']['maps']:
        m['route_relationship'] = 'different_goals' if m['id'] == 'ratio' else 'alternative_explanations'
        groups = {}
        for c in m['claims']:
            c['review'] = {'mathematical': 'self_checked', 'independent': c['independent_review'], 'student': c['student_validated'], 'history': []}
            if c.get('condition_group'):
                assert c['kind'] == 'task_condition', f"Mixed condition group: {c['id']}"
                g = groups.setdefault(c['condition_group'], {'id': c['condition_group'], 'operator': 'AND', 'target': c['target'], 'claim_ids': [], 'members': []})
                assert g['target'] == c['target']
                g['claim_ids'].append(c['id'])
                g['members'].append(c['source'])
        m['condition_groups'] = list(groups.values())
    OUT.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    # Small initial index; long analyses and relation evidence load on demand.
    version = hashlib.sha256(encoded.encode('utf-8')).hexdigest()[:16]
    def write_json(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    words = {}
    for e in data['elements']:
        for code in e.get('standards', []):
            words.setdefault(code, []).extend([e['label'], e.get('observable', '')])
    index_standards = [{**s, 'searchTerms': ' '.join(words.get(s['code'], []))} for s in standards]
    resource_root = f'content/versions/{version}/'
    write_json(OUT / 'content' / 'catalog.json', {'version': version, 'resourceRoot': resource_root, 'meta': data['meta'], 'standards': index_standards})
    write_json(OUT / 'content' / 'sources.json', {'version': version, 'sources': data['sources']})
    write_json(OUT / 'content' / 'connections.json', {'version': version, 'relations': relations, 'sources': data['sources'], 'hierarchy': data['hierarchy']})
    pilot_ids = {rid for m in data['hierarchy']['maps'] for c in m['claims'] for rid in c['original_relation_ids']}
    pilot_relations = [r for r in relations if r['id'] in pilot_ids]
    # The small pilot bundle needs only the sources it actually cites. Keep
    # each selected source and relation intact, including all review evidence.
    # Full-source and per-standard bundles still carry the complete registry.
    pilot_source_ids = ({s['sourceId'] for s in standards}
                        | {sid for m in data['hierarchy']['maps'] for c in m['claims'] for sid in c['research_context']}
                        | {sid for r in pilot_relations for sid in r.get('source_ids', [])})
    assert pilot_source_ids <= {s['id'] for s in data['sources']}
    pilot_bundle = {'version': version, 'hierarchy': data['hierarchy'], 'sources': [s for s in data['sources'] if s['id'] in pilot_source_ids], 'relations': pilot_relations}
    write_json(OUT / 'content' / 'hierarchy.json', pilot_bundle)
    write_json(OUT / resource_root / 'hierarchy.json', pilot_bundle)
    for s in standards:
        code = s['code']
        # The catalog's resourceRoot selects these immutable records. Do not
        # emit a second, unindexed copy under content/relations/.
        write_json(OUT / resource_root / 'relations' / f'{code}.json', {'version': version, 'sources': data['sources'], 'relations': [r for r in relations if 'standard:' + code in (r['from'], r['to'])]})
    write_json(OUT / 'content' / 'flows.json', {'version': version, **data['conceptFlows']})
    corrections = load('source_corrections')
    notes = load('secondary_source_review')['notes']
    for s in standards:
        code = s['code']
        detail = {**analyses[code], 'elements': [e for e in data['elements'] if code in e.get('standards', [])],
                  'sourceNotes': [n for n in notes if n['code'] == code],
                  'correction': {'changed': code in corrections['corrections'], 'method': corrections['review_method']} if code in corrections['corrections'] else None}
        write_json(OUT / 'content' / 'standards' / f'{code}.json', {'version': version, 'analysis': detail})
    source_pdf = ROOT / inventory['source_file']
    if source_pdf.exists() and source_pdf.resolve() != (OUT/'curriculum.pdf').resolve():
        shutil.copyfile(source_pdf, OUT / 'curriculum.pdf')
    assert (OUT/'curriculum.pdf').exists()
    from build_concept_pathways import build as build_concept_pathways
    build_concept_pathways(OUT.parent)
    from build_task_pathways import build as build_task_pathways
    build_task_pathways(OUT.parent)
    from build_distribution_lab import build as build_distribution_lab
    build_distribution_lab(OUT)
    from build_inquiry_workbook import build as build_inquiry_workbook
    build_inquiry_workbook(OUT)
    print(json.dumps({'standards': len(standards), 'analyses': len(analyses),
                      'connections': len(standard_edges), 'index_bytes': (OUT / 'content' / 'catalog.json').stat().st_size,
                      'detail_files': len(analyses), 'version': version}, ensure_ascii=False))


if __name__ == '__main__':
    main()

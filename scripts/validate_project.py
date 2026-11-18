"""Check source provenance, coverage, references and project consistency."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    data = read('data/standards.json')
    standards = data['standards']
    by_code = {r['code']: r for r in standards}
    assert len(by_code) == len(standards) == 435
    assert Counter(r['school_level'] for r in standards) == Counter({'초등학교': 121, '중학교': 60, '고등학교': 254})
    assert len({r['subject'] for r in standards if r['school_level'] == '고등학교'}) == 15
    assert hashlib.sha256((ROOT / data['source_file']).read_bytes()).hexdigest() == data['source_sha256']
    assert all(r['statement_extracted'] and r['statement_display'] and r['source_pdf_pages'] for r in standards)
    assert all(r['statement_display'].endswith('.') for r in standards)
    assert all(not any(0xE000 <= ord(c) <= 0xF8FF for c in r['statement_display']) for r in standards)
    corrections = read('data/source_corrections.json')['corrections']
    assert set(corrections) <= set(by_code)
    assert len(corrections) == 29
    assert not read('data/inventory_quality.json')['records_requiring_source_review']
    registry = read('data/analysis_registry.json')
    revision_path=ROOT/'data/revision_coverage.json'
    migrated={r['code'] for r in read('data/revision_coverage.json')['entries'] if r['status']!='개별 재작성 대기'} if revision_path.exists() else set()
    assert len({r['code'] for r in registry}) == len(registry)
    for entry in registry:
        assert entry['code'] in by_code
        assert (ROOT / entry['file']).is_file(), entry['file']
        assert by_code[entry['code']]['analysis_status'] == entry['status']
        if entry['student_response_validation']:
            assert entry['status'] == '학생 반응 검증'
            assert entry.get('validation_evidence_file')
            assert (ROOT / entry['validation_evidence_file']).is_file()
    sources = read('data/sources.json')
    source_ids = {s['id'] for s in sources}
    assert len(source_ids) == len(sources)
    for source in sources:
        if source.get('local_path'):
            assert (ROOT / source['local_path']).is_file()
    elements = read('data/elements.json')['elements']
    element_ids = {e['id'] for e in elements}
    assert len(element_ids) == len(elements)
    for element in elements:
        assert element['observable']
        assert set(element['standards']) <= set(by_code)
    valid_nodes = {f'standard:{code}' for code in by_code} | {f'element:{e}' for e in element_ids}
    relation_types = {'has_subskill', 'requires_for_task', 'meaning_connection', 'representation_translation', 'generalizes', 'contrasts', 'instructional_sequence', 'supports_learning'}
    relations = read('data/relations.json')['relations']
    assert len({r['id'] for r in relations}) == len(relations)
    for relation in relations:
        assert relation['from'] in valid_nodes, relation['id']
        assert relation['to'] in valid_nodes, relation['id']
        assert relation['from'] != relation['to']
        assert relation['type'] in relation_types
        assert relation['rationale'] and relation['scope'] and relation['conditions'] and relation['limit']
        assert set(relation['source_ids']) <= source_ids
        assert set(relation.get('intermediate_standards', [])) <= set(by_code)
        if 'prerequisite_group' in relation:
            group = relation['prerequisite_group']
            assert group['operator'] in {'AND', 'OR'}
            assert set(group['members']) <= valid_nodes
        if relation['type'] == 'generalizes':
            assert relation.get('additional_learning')
    detail_path = ROOT / 'data/analysis_details.json'
    if detail_path.exists():
        details = read('data/analysis_details.json')['analyses']
        elementary = {r['code'] for r in standards if r['school_level'] == '초등학교'}
        if not (ROOT / 'data/secondary_analysis_details.json').exists():
            assert {r['code'] for r in registry} == elementary
        else:
            assert {r['code'] for r in registry} == set(by_code)
        assert len(details) == 118
        for entry in details:
            assert len(entry['steps']) >= 4 and len(entry['probes']) >= 3
            levels = {by_code[c[0]]['school_level'] for c in entry['connections']}
            assert {'중학교', '고등학교'} <= levels, entry['code']
            content = (ROOT / f'analyses/{entry["code"]}.md').read_text(encoding='utf-8')
            assert len(content) > (0 if entry['code'] in migrated else 2000), entry['code']
            for section in (['수학적 의미', '세부 사고', '관찰할 수행', '표현 사이', '오류와 진단', '학습 활동', '같은 학교급', '근거와 검토'] if entry['code'] in migrated else ['수학적 의미', '세부 사고', '선수 조건', '표현 사이', '오류와 진단', '학습 활동', '중고등 수학', '근거와 후속']):
                assert section in content, (entry['code'], section)
    secondary_path = ROOT / 'data/secondary_analysis_details.json'
    if secondary_path.exists():
        secondary = read('data/secondary_analysis_details.json')
        goals = secondary['analyses']
        expected = {c for c, s in by_code.items() if s['school_level'] != '초등학교'}
        assert len(goals) == 314 and {g['code'] for g in goals} == expected
        assert len({g['code'] for g in goals}) == len(goals)
        for goal in goals:
            assert len(goal['steps']) >= 4 and all(len(r) == 2 for r in goal['steps']), goal['code']
            assert len(goal['probes']) >= 2 and all(len(r) == 4 for r in goal['probes']), goal['code']
            profile = secondary['profiles'][goal['family']]
            assert len(profile['probe']) == 4 and len(profile['paths']) == 2
            assert all(by_code[c]['school_level'] == '초등학교' for c, _ in profile['anchors'])
            assert all(c in by_code for c, _ in goal['prior'] + goal['onward'])
            content = (ROOT / f'analyses/{goal["code"]}.md').read_text(encoding='utf-8')
            assert len(content) > (0 if goal['code'] in migrated else 2600), goal['code']
            for section in (['수학적 의미', '세부 사고', '관찰할 수행', '표현 사이', '오류와 진단', '학습 활동', '같은 학교급', '근거와 검토'] if goal['code'] in migrated else ['수학적 의미', '개별 과제의 세부 사고', '선수 조건', '표현 사이', '오류와 진단', '학습 활동', '초등에서 오는 의미', '후속 및 분기', '근거와 후속']):
                assert section in content, (goal['code'], section)
        coverage = read('data/secondary_coverage.json')
        for code, digest in coverage['elementary_files_preserved_sha256'].items():
            if code not in migrated:assert hashlib.sha256((ROOT / f'analyses/{code}.md').read_bytes()).hexdigest() == digest, code
    code_pattern = re.compile(r'(?<![0-9가-힣])(?:[2469]수\d{2}-\d{2}|10(?:공수|기수)[12]-\d{2}-\d{2}|12(?:대수|확통|기하|경수|인수|직수|수문|실통|수과)\d{2}-\d{2}|12미적[ⅠⅡ]-\d{2}-\d{2})')
    docs = [ROOT / 'README.md'] + list((ROOT / 'docs').glob('*.md')) + list((ROOT / 'analyses').glob('*.md')) + list((ROOT / 'indexes').glob('*.md'))
    for path in docs:
        text = path.read_text(encoding='utf-8')
        assert '\ufffd' not in text, path
        assert set(code_pattern.findall(text)) <= set(by_code), path
        for link in re.findall(r'\]\(([^\s)]+)\)', text):
            if link.startswith(('https:', 'http:', '#')):
                continue
            local = unquote(link.split('#', 1)[0])
            assert (path.parent / local).resolve().is_file(), (path, link)
    result = {
        'status': 'pass',
        'standards': len(standards), 'elementary': 121, 'middle': 60, 'high': 254,
        'high_school_subjects': 15, 'visually_corrected_records': len(corrections),
        'detailed_analysis_drafts': sum(r['status'] == '초안' for r in registry),
        'reviewed_analyses': sum(r['status'] in {'검토 완료', '학생 반응 검증'} for r in registry),
        'student_validated_analyses': sum(r['student_response_validation'] for r in registry),
        'elements': len(elements), 'relations': len(relations), 'sources': len(sources),
        'checked_markdown_files': len(docs),
    }
    (ROOT / 'data/project_validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()

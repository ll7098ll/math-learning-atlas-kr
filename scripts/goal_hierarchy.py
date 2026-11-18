"""Read authored constituent goals and task-specific condition provenance."""
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_review(review):
    state=review['state']
    assert state in ('self_checked','independently_reviewed','student_validated')
    if state=='independently_reviewed':assert review.get('independent_review')
    if state=='student_validated':assert review.get('student_validated')
    for flag in ('independent_review','student_validated'):
        if review.get(flag):
            evidence=review.get(flag+'_evidence',{})
            assert all(evidence.get(k) for k in ('reviewer','date','scope','file')), 'Missing '+flag+' evidence'
            path=(ROOT/evidence['file']).resolve()
            assert path.is_relative_to(ROOT) and path.is_file(), 'Missing review evidence file'


def validate_condition_source(source, case, goals):
    targets=source.get('applies_to_goal_ids',case['goal_ids'])
    assert targets and set(targets)<=set(case['goal_ids'])
    assert len(targets)==len(set(targets)), 'Duplicate condition target'
    assert source['kind'] in ('goal','entry_capability','within_task','task_assumption')
    assert source['rationale']
    if source['kind']=='goal':
        assert source['goal_id'] in goals, source
        assert source['goal_id'] not in targets, 'Do not require a target goal as its own entry skill'
    else:assert 'goal_id' not in source
    return targets


def load_goal_hierarchies(standards):
    standards = {s['code']:s for s in standards}
    entries, cases, goals = {}, [], {}
    norm = lambda s: ''.join(s.split())
    for filename in sorted((ROOT/'data').glob('goal_hierarchy_*.json')):
        data = json.loads(filename.read_text(encoding='utf-8'))
        assert data['schema_version']==1, filename
        assert data['source_pdf_sha256']==hashlib.sha256((ROOT/'[별책8] 수학과 교육과정.pdf').read_bytes()).hexdigest(), 'Curriculum source changed; reconcile reviewed scope'
        for entry in data['entries']:
            code = entry['code']
            assert code in standards and code not in entries, code
            official = standards[code].get('statement', standards[code].get('statement_display'))
            assert norm(entry['official_goal'])==norm(official), code+' official goal changed'
            assert entry['scope'] and entry['goals'] and entry['source_review']['pdf_pages']
            validate_review(entry['review'])
            entries[code] = {**entry, 'authored_from':'data/'+filename.name}
            for goal in entry['goals']:
                assert goal['id'].startswith(code+':') and goal['id'] not in goals
                assert goal['title'] and goal['success'] and goal['case_ids']
                assert norm(goal['official_span']) in norm(official), goal['id']
                goals[goal['id']] = {**goal,'code':code}
        cases.extend(data['cases'])
    by_case = {c['id']:c for c in cases}
    assert len(by_case)==len(cases)
    for goal in goals.values():
        for case_id in goal['case_ids']:
            assert case_id in by_case and goal['id'] in by_case[case_id]['goal_ids'], goal['id']
    for case in cases:
        assert case['goal_ids'] and case['alternative_review']
        for goal_id in case['goal_ids']:
            assert goal_id in goals and goals[goal_id]['code']==case['standard'], case['id']
        for route in case['routes']:
            sources=route['condition_sources']
            assert {s['condition_index'] for s in sources}==set(range(len(route['conditions'])))
            assert len(sources)==len(route['conditions']), route['id']
            for source in sources:
                validate_condition_source(source,case,goals)
    return entries, cases, goals


def write_goal_report(entries, cases, goals):
    """Human-readable review surface from the exact same authored records."""
    labels={'goal':'앞선 목표의 부분 수행','within_task':'과제 안에서 구성·확인','entry_capability':'기초 출발 능력','task_assumption':'주어진 수학적 가정'}
    anchor=lambda goal:'goal-'+goal.replace(':','-')
    lines=['# 성취기준의 하위 목표와 과제별 위계 설계','',
           '공식 문구와 해설·적용 시 고려 사항을 대조한 자체 설계다. 카드와 절의 순서는 학생의 학습 순서가 아니다. 각 조건은 명시한 과제 경로에만 적용하며 출발 성취기준 전체의 보편적 선행 숙달을 뜻하지 않는다.','',
           f'{len(entries)}개 기준·{len(goals)}개 하위 목표·{len(cases)}개 대표 과제다. 독립 검토·학생 반응 검증 전이며, 전체 435개 기준의 완성 현황은 [별도 원장](../data/task_pathway_coverage.json)에서 관리한다.','',
           '각 항목에 공식 문구의 출처 쪽수와 작성 원본을 기록한다. 텍스트 대조와 원문 이미지 대조 상태는 구별한다.','']
    for code,entry in entries.items():
        pages=', '.join(map(str,entry['source_review']['pdf_pages']))
        lines += ['## '+code,'','> '+entry['official_goal'],'',entry['scope'],'',
                  '작성 원본: [목표·과제·조건](../'+entry['authored_from']+'). 교육과정 PDF '+pages+'쪽. '+entry['source_review']['scope'],'']
        for goal in entry['goals']:
            lines += ['<a id="'+anchor(goal['id'])+'"></a>','', '### '+goal['title'],'',
                      '공식 문구: '+goal['official_span'],'','확인할 수행: '+goal['success'],'',
                      '대표 과제: '+', '.join(next(c['title'] for c in cases if c['id']==i) for i in goal['case_ids']), '']
        for case in (c for c in cases if c['standard']==code):
            lines += ['### 과제: '+case['title'],'',case['task'],'','목표: '+case['goal'],'','공통 조건:','']
            lines += ['- '+text for text in case['shared_conditions']]+['']
            for resource in case.get('resources',[]):
                name=resource['path'].split('/')[-1]
                tools={'stats-inference.py':'statistical_tools.py','economy-ai-models.py':'economy_ai_models.py'}
                target='../scripts/'+tools[name] if name in tools else '../data/teaching_examples/'+name
                lines += ['연습 자료: ['+resource['label']+']('+target+')','']
            for reference in case.get('references',[]):
                lines += ['참고: ['+reference['title']+']('+reference['url']+'). 확인일 '+reference['accessed']+'.','']
            if len(case['routes'])>1:
                lines += ['아래는 이 대표 과제에서 같은 목표에 이르는 대안 경로다. 한 경로의 조건을 다른 경로까지 합쳐 요구하지 않는다.','']
            for route in case['routes']:
                lines += ['#### '+route['title'],'','이 경로에서 함께 확인할 AND 조건:','']
                for i,text in enumerate(route['conditions']):
                    source=next(s for s in route['condition_sources'] if s['condition_index']==i)
                    origin=labels[source['kind']]
                    if source['kind']=='goal':
                        g=goals[source['goal_id']]
                        origin+=' — ['+g['title']+' · '+g['code']+'](#'+anchor(g['id'])+')'
                    if 'applies_to_goal_ids' in source:
                        origin+='; 적용 목표: '+', '.join(goals[g]['title'] for g in source['applies_to_goal_ids'])
                    lines += ['- '+text+' ('+origin+')']
                lines += ['','설명과 수행:','']+[str(i+1)+'. '+text for i,text in enumerate(route['steps'])]
                lines += ['',route['result'],'','확인 질문: '+route['diagnostic']['question'],'','기대하는 설명: '+route['diagnostic']['expected'],'']
            lines += ['대안과 범위 검토: '+case['alternative_review'],'']
    (ROOT/'docs/하위목표과제별위계.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

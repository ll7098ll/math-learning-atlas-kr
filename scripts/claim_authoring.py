"""Export explicitly authored route claims and preserve their review provenance."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def write_claims(claims, filename):
    codes={s['code'] for s in json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']}
    records=[]
    for c in claims:
        assert c['source'] in codes and c['target'] in codes, c['id']
        assert c['source']!=c['target'],c['id']
        records.append({
            'id':c['id'],'from':'standard:'+c['source'],'to':'standard:'+c['target'],
            'type':c['kind'],'scope':c['scope'],'rationale':c['rationale'],
            'conditions':c['conditions'],'diagnostic':c['diagnostic'],
            'expected_response':c['expected'],'alternative_route':c['alternative'],
            'additional_learning':c.get('additional_learning',[]),
            'limit':c['alternative']+' 이 기록은 명시한 과제 경로의 자체 분석이며 성취기준 전체의 보편적 선행 숙달을 주장하지 않는다.',
            'evidence_kind':c.get('evidence_kind','수학적 자체 분석'),'source_ids':['CURRICULUM_2022_33'],
            'status':'초안','review_state':'self_checked','independent_review':False,
            'student_validated':False,'hierarchy_review':'self_checked',
            'review_history':[{'date':'2026-10-30','reviewer':'Codex','kind':'self_check','scope':c['scope'],'method':'정의·예시 풀이·경계 조건·대안 경로 대조'}],
            'authored_from':'data/'+filename,
        })
    assert len({r['id'] for r in records})==len(records)
    (ROOT/'data'/filename).write_text(json.dumps({'relations':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    registry_file=ROOT/'data/hierarchy_review_registry.json'
    registry=json.loads(registry_file.read_text(encoding='utf-8'))
    for r in records:
        review=registry['relations'].setdefault(r['id'],{'state':'self_checked','rationale':r['rationale'],'history':r['review_history'],'independent_review':False,'student_validated':False})
        if review.get('rationale')!=r['rationale']:
            assert not review.get('independent_review') and not review.get('student_validated'), 'Reconcile independent review before revising a checked claim'
            review['history'].append({**r['review_history'][0],'reason':'자체 논증을 보강하고 이전 검토 이력을 보존','previous_rationale':review.get('rationale')})
            review['rationale']=r['rationale']
        entry=registry['standards'][r['to'][9:]]
        if entry['state']=='unreviewed':entry['state']='in_progress'
    registry_file.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Authored {len(records)} task-route claims: {filename}')

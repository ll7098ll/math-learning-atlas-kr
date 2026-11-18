"""Render cross-school/course review surfaces from authored conditions, without assigning review states."""
from pathlib import Path
from collections import Counter
import json,hashlib
from goal_hierarchy import load_goal_hierarchies
ROOT=Path(__file__).resolve().parents[1]
def content_hash(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def build():
    standards=json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']
    entries,cases,goals=load_goal_hierarchies(standards)
    by_code={s['code']:s for s in standards}
    all_records=[]
    for case in cases:
        for route in case['routes']:
            for source in route['condition_sources']:
                if source['kind']!='goal':continue
                origin=goals[source['goal_id']];a=by_code[origin['code']];b=by_code[case['standard']]
                school=a['school_level']!=b['school_level']
                course=a['school_level']==b['school_level']=='고등학교' and a['subject']!=b['subject']
                all_records.append(dict(case_id=case['id'],route_id=route['id'],condition_index=source['condition_index'],
                    transition='학교급 전환' if school else '고교 과목 전환' if course else '같은 학교급·과목',source_standard=origin['code'],source_goal=source['goal_id'],
                    source_title=origin['title'],source_performance=origin['success'],source_scope=entries[origin['code']]['scope'],
                    source_school=a['school_level'],source_subject=a.get('subject'),target_standard=case['standard'],
                    target_school=b['school_level'],target_subject=b.get('subject'),target_goals=source.get('applies_to_goal_ids',case['goal_ids']),
                    condition=route['conditions'][source['condition_index']],rationale=source['rationale'],
                    target_task=case['task'],shared_conditions=case['shared_conditions'],route_conditions=route['conditions']))
    records=[r for r in all_records if r['transition']!='같은 학교급·과목']
    snapshots={}
    for r in all_records:
        key=r['case_id']+'|'+r['route_id']+'|'+str(r['condition_index'])
        snapshots[key]=content_hash(r)
    ledger_path=ROOT/'data/hierarchy_integration_review.json'
    ledger=json.loads(ledger_path.read_text(encoding='utf-8')) if ledger_path.exists() else {}
    # Review assertions belong to the exact content inspected by the reviewer.
    # A source edit requires reconciliation, never an automatic fresh stamp.
    source_changes=[name for name,digest in ledger.get('source_hashes',{}).items()
                    if not (ROOT/name).is_file() or content_hash(json.loads((ROOT/name).read_text(encoding='utf-8')))!=digest]
    reviewed=ledger.get('condition_snapshots',{})
    changed=[key for key,digest in snapshots.items() if reviewed.get(key)!=digest]
    stale=[key for key in reviewed if key not in snapshots]
    summary=dict(all_goal_condition_records=len(all_records),condition_records=len(records),by_transition=dict(Counter(r['transition'] for r in records)),
        scoped_goal_applications=sum(len(r['target_goals']) for r in records),
        matching_review_snapshots=len(snapshots)-len(changed),needs_review=changed,removed_review_snapshots=stale,
        source_changes_since_review=source_changes)
    (ROOT/'data/goal_condition_review_table.json').write_text(json.dumps(dict(summary=summary,records=all_records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result=dict(kind='authored_transition_review_surface',interpretation='조건별 부분 수행과 전체 과제 조건을 함께 대조한다. 표 생성은 검토 상태를 올리지 않는다.',summary=summary,records=records)
    (ROOT/'data/hierarchy_transition_table.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# 학교급 전환표와 고교 과목 분기표','',
        '조건별 출발 목표의 실제 수행·범위와 도착 과제의 전체 조건을 같은 원장에서 대조한다. 과목 전체의 필수 이수 순서가 아니며 초등에서 고교로 연결된 경우도 명시한 부분 수행만 사용한다. 표의 생성은 자체 점검이나 독립 검토를 자동 승인하지 않는다.','',
        '세부 자료: [조건별 전환표](../data/hierarchy_transition_table.json). 검토 시점의 내용 해시는 [통합 검토 기록](../data/hierarchy_integration_review.json)에 보존한다. 내용이 바뀌면 일치하지 않는 항목을 다시 검토한다.','',
        f"전환 {len(records)}개 조건 기록, {summary['scoped_goal_applications']}개 적용 목표다. 같은 학교급·과목을 포함한 전체 {len(all_records)}개 목표 참조 중 검토 스냅샷 일치 {summary['matching_review_snapshots']}개, 재검토 필요 {len(changed)}개, 제거된 기록 {len(stale)}개.",'']
    for section in ['학교급 전환','고교 과목 전환']:
        lines += ['## '+section,'']
        for r in records:
            if r['transition']!=section:continue
            lines += ['### '+r['case_id']+' / '+r['route_id']+' / '+str(r['condition_index']),'',
                '**출발:** '+r['source_goal']+' '+r['source_title'],'',
                '출발 수행: '+r['source_performance'],'','출발 범위: '+r['source_scope'],'',
                '**도착:** '+', '.join(r['target_goals']),'','과제: '+r['target_task'],'',
                '이 조건: '+r['condition'],'','연결 이유: '+r['rationale'],'','과제 공통 조건:','']
            lines += ['- '+s for s in r['shared_conditions']]+['','이 경로 전체의 AND 조건:','']
            lines += ['- '+s for s in r['route_conditions']]+['']
    (ROOT/'docs/학교급과과목전환표.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('needs_review','removed_review_snapshots')}|dict(needs_review_count=len(changed),removed_review_count=len(stale)),ensure_ascii=False))
    return snapshots,result

if __name__=='__main__':
    _,result=build()
    assert not any(result['summary'][k] for k in ('needs_review','removed_review_snapshots','source_changes_since_review')),'Reconcile transition content with the integration review ledger'

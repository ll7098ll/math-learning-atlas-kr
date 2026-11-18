"""Prioritize scope review without treating a generated queue as a completed review."""
from pathlib import Path
from collections import Counter
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
 relations=[r for r in read('data/revised_relations.json')['relations'] if r['from'].startswith('standard:') and r['to'].startswith('standard:')]
 registry=read('data/hierarchy_review_registry.json').get('relations',{});rows=[]
 from relation_analysis_review import load_reviews
 scope_reviews=load_reviews()['records']
 assert len({r['id'] for r in relations})==len(relations)
 assert all(r.get('review_state') and isinstance(r.get('independent_review'),bool) and isinstance(r.get('student_validated'),bool) for r in relations)
 for r in relations:
  if r['review_state'] not in ['legacy_draft','candidate']:continue
  if r['type'] in ['requires_for_task','generalizes']:
   priority=1;reason='방향을 가진 과제 조건/의미 확장의 실제 범위·정당화·예외를 우선 확인'
  elif r['review_state']=='candidate' or r['type']=='contrasts':
   priority=2;reason='후보 판단이나 대비 관계의 성립 범위·반례를 확인'
  else:
   priority=3;reason='의미 연결의 대상·표현·조건과 기존 진단의 적합성을 개별 확인'
  rows.append(dict(relation_id=r['id'],from_code=r['from'][9:],to_code=r['to'][9:],type=r['type'],analysis_state=r['review_state'],separate_hierarchy_state=registry.get(r['id'],{}).get('state','unreviewed'),queue_state='needs_scope_review',priority=priority,priority_reason=reason,source_snapshot=digest(r),current_rationale=r['rationale'],diagnostic=r.get('diagnostic',''),expected_response=r.get('expected_response',''),task_ids=r.get('diagnostic_task_ids',[]),goal_ids=r.get('diagnostic_goal_ids',[]),required_review=['양쪽 목표·실제 과제·적용 조건과 수 범위 대조','관계 유형과 방향의 수학적 이유·반례 또는 한계 확인','진단 질문·기대 설명·대안 경로의 목표 적합성 확인','필수 선수성·교수 순서·독립 검토·학생 검증과 구별한 실제 판단 및 근거 기록']))
 rows.sort(key=lambda r:(r['priority'],r['from_code'],r['to_code'],r['relation_id']))
 out=dict(schema_version=1,interpretation='현재 상태에서의 검토 대기 목록이다. 자동 생성은 검토 완료·오류 확정·필수 선수성의 승인이 아니다. 우선순위는 방향 주장과 후보/대비를 먼저 보는 작업 순서이며 수학적 타당성의 판정이 아니다. 개별 검토 범위가 아직 기록되지 않은 legacy_draft와 별도 위계 검토 상태를 구별한다.',source_file='data/revised_relations.json',source_snapshot=digest(relations),summary=dict(standard_relations=len(relations),analysis_states=dict(Counter(r['review_state'] for r in relations)),queued=len(rows),by_priority=dict(Counter(str(r['priority']) for r in rows)),by_type=dict(Counter(r['type'] for r in rows)),separate_hierarchy_records=len(registry),newly_completed_reviews=0),records=rows)
 out['summary']['durable_scoped_math_reviews']=len(scope_reviews)
 assert not set(scope_reviews)&{r['relation_id'] for r in rows}
 (ROOT/'data/relation_analysis_scope_queue.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(out['summary'],ensure_ascii=False))
if __name__=='__main__':main()

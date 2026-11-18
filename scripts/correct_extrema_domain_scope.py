"""Reconcile the closed-interval task with the open-domain fence example."""
import copy,json
from relation_analysis_review import ROOT,digest,load_reviews
from literature_review import load_registry
CODE='10공수1-02-06'
OLD='주어진 닫힌 구간만 비교한다. 꼭짓점이 범위 밖이면 최솟값 후보에 넣지 않는다.'
NEW='각 과제의 정의역과 끝점 포함 여부를 먼저 확인한다. 닫힌 구간에서는 포함된 꼭짓점과 끝점 값을 비교한다. 열린 구간의 보충 예에서는 경계에 가까워지는 값과 실제로 달성하는 최댓값·최솟값을 구별한다.'
MEANING='꼭짓점과 경계를 정의역에 맞게 비교한다. 닫힌 구간의 주과제는 허용된 꼭짓점·끝점을 평가하고, 열린 구간의 울타리 보충 예는 달성되는 최댓값과 달성되지 않는 하한을 구별한다.'
REASON='닫힌 구간만 비교한다는 상세 원고의 조건이 같은 원고의 0<x<10인 울타리 보충 예와 모순되었다. 주과제의 닫힌 구간과 보충 예의 열린 정의역을 각각 명시했다. A=x(10−x)=25−(x−5)²는 최대25를 x=5에서 달성하지만0은 경계 접근값일 뿐 최소값이 아니다. 기존 풀이·목표·과제·자료는 그대로 보존했다. 최소값 부재는 유한한 표본 관찰이 아니다. 0<x≤5이면 y=x/2에서 A(x)−A(y)=x(20−3x)/4>0이고, 5<x<10이면 10−x의 대칭을 사용해 항상 더 작은 양의 넓이를 얻는다.'

def main():
 reviews=load_reviews();literature=load_registry();p=ROOT/'data/revisions_high.json';data=json.loads(p.read_text(encoding='utf-8'));r=data[CODE]
 evidence=ROOT/'data/extrema_domain_scope_correction.json'
 if r['conditions']==[NEW]:
  assert r['mathematicalMeaning']==MEANING and evidence.exists()
  print('Extrema domain correction remains current');return
 assert r['conditions']==[OLD]
 assert not any('standard:'+CODE in [v['from'],v['to']] for v in reviews['records'].values())
 assert not any('revision:'+CODE in c['target_snapshots'] for c in literature['claims'])
 before=copy.deepcopy(r);r['conditions']=[NEW];r['mathematicalMeaning']=MEANING
 permitted=copy.deepcopy(before);permitted.update(conditions=[NEW],mathematicalMeaning=MEANING);assert permitted==r
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 evidence.write_text(json.dumps(dict(date='2026-11-05',standard_code=CODE,reason=REASON,previous_fields={k:before[k] for k in ['conditions','mathematicalMeaning']},current_fields={k:r[k] for k in ['conditions','mathematicalMeaning']},previous_revision_snapshot=digest(before),current_revision_snapshot=digest(r),independent_review=False,student_validated=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 load_reviews();load_registry();print('Corrected closed/open domain scope; earlier reviews remain current')
if __name__=='__main__':main()

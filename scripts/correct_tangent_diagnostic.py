"""Explicitly replace a non-witness for multiple tangent intersections."""
import json
from literature_review import ROOT,digest,target_value,load_registry
CODE='12미적Ⅰ-02-05';TARGET='revision:'+CODE
OLD='x³의 원점 접선을 본다.'
NEW='f(x)=x³−x의x=1 접선y=2x−2가x=−2에서도 만남을 확인한다.'
REASON='한 점에서만 만나는지 묻는 질문에x³의 원점 접선은 교차하지만 만나는 점은 하나여서 반례가 아니었다. f=x³−x의x=1 접선은y=2x−2이고 f(x)−(2x−2)=(x−1)²(x+2)이므로x=−2에서도 만난다. x³의 원점 예는 곡선 횡단의 예로만 유지한다. 기존 주과제·풀이·조건·목표·과제 원장은 그대로이며 후속 예와 피드백만 고쳤다.'

def main():
 registry=load_registry();path=ROOT/'data/revisions_high.json';revisions=json.loads(path.read_text(encoding='utf-8'));entry=revisions[CODE]
 diagnostic=next(v for v in entry['diagnostics'] if v['question']=='접선은 곡선과 한 점에서만 만나는 선인가')
 if diagnostic['followup']==NEW:
  assert NEW in entry['feedback'];print('Corrected witness and reviewed target remain current');return
 assert diagnostic['followup']==OLD and OLD in entry['feedback']
 before=target_value(TARGET);before_hash=digest(before)
 # Independent polynomial identity: x³−3x+2=(x−1)²(x+2).
 assert [2,-3,0,1]==[1*2,1-4,2-2,1]
 assert 3*1**2-1==2 and 1**3-1==2*1-2
 assert (-2)**3-(-2)==2*(-2)-2
 diagnostic['followup']=NEW;entry['feedback']=[NEW if v==OLD else v for v in entry['feedback']]
 # Verify that no unrelated authored part changes.
 permitted=json.loads(json.dumps(before));permitted['revision']['diagnostics']=entry['diagnostics'];permitted['revision']['feedback']=entry['feedback']
 assert permitted==dict(file='revisions_high.json',revision=entry)
 generator=ROOT/'scripts/secondary_calculus.py';text=generator.read_text(encoding='utf-8');assert text.count(OLD)==1
 path.write_text(json.dumps(revisions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');generator.write_text(text.replace(OLD,NEW),encoding='utf-8')
 affected=[]
 for claim in registry['claims']:
  if TARGET not in claim['target_snapshots']:continue
  assert claim['target_snapshots'][TARGET]==before_hash
  claim.setdefault('target_review_history',[]).append(dict(date='2026-11-05',target=TARGET,previous_snapshot=before_hash,reason=REASON))
  claim['target_snapshots'][TARGET]=digest(target_value(TARGET));affected.append(claim['id'])
 assert affected==['OD02']
 (ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (ROOT/'data/tangent_diagnostic_correction.json').write_text(json.dumps(dict(date='2026-11-05',standard_code=CODE,old_followup=OLD,new_followup=NEW,reason=REASON,affected_claims=affected,previous_target_snapshot=before_hash,current_target_snapshot=digest(target_value(TARGET)),independent_review=False,student_validated=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 load_registry();print('Corrected tangent witness; explicitly re-reviewed OD02 only')
if __name__=='__main__':main()

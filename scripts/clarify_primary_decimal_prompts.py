"""Put existing decimal inputs in the question and reconcile the exact delta."""
from pathlib import Path
import copy,json
from mapping_review_author import digest,changed_targets
from write_hierarchy_transition_tables import content_hash,build as build_transitions
R=Path(__file__).resolve().parents[1]
CHANGES={
'early-4수01-14-compare':('세 쌍의 소수를 비교하고 숫자 개수가 아닌 자릿값으로 이유를 말한다.','0.9와0.12, 1.03과1.003, 0.4와0.40을 비교하고 숫자 개수가 아닌 자릿값으로 이유를 말한다.'),
'early-4수01-16-add':('두 소수의 합을 구하고1.2를1.20으로 쓸 수 있는 이유를 설명한다.','1.27+0.86과1.2+0.35를 계산하고, 1.2를1.20으로 쓸 수 있는 이유를 설명한다.'),
'early-4수01-16-subtract':('두 소수의 차를 구하고 전체·십분의 일·백분의 일 사이의 교환을 설명한다.','2.04−0.87과1.2−0.35를 계산하고, 전체·십분의 일·백분의 일 사이의 교환을 설명한다.')}
REASON='기존 목표 문장에 있던 소수 입력을 문제 본문에도 명시. 입력·정의역·모든 풀이와 결과·목표·선수 조건은 그대로이며 자릿값 비교·같은 단위 합차의 의미 대응이 유지됨을 재대조.'

def reconcile_conditions():
 snapshots,result=build_transitions();lp=R/'data/hierarchy_integration_review.json';ledger=json.loads(lp.read_text(encoding='utf-8'))
 rows=json.loads((R/'data/goal_condition_review_table.json').read_text(encoding='utf-8'))['records']
 targets={r['case_id']+'|'+r['route_id']+'|'+str(r['condition_index']):r for r in rows if r['case_id'] in CHANGES}
 changed=result['summary']['needs_review']
 assert set(changed)<=set(targets) and not result['summary']['removed_review_snapshots'] and not result['summary']['source_changes_since_review']
 if not changed:return
 previous={}
 for key in changed:
  row=copy.deepcopy(targets[key]);old,new=CHANGES[row['case_id']];assert row['target_task']==new
  row['target_task']=old;assert ledger['condition_snapshots'][key]==content_hash(row),'Unreviewed change beyond the target prompt'
  previous[key]=ledger['condition_snapshots'][key];ledger['condition_snapshots'][key]=snapshots[key]
 ledger['history'].append(dict(date='2026-11-04',reviewer='Codex',kind='condition_prompt_re_review',condition_keys=changed,previous_snapshots=previous,scope=REASON+' 조건 기록의 유일한 변화가 target_task임을 이전 해시로 검증.'))
 lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');build_transitions()

def main():
 rel='data/goal_hierarchy_primary_3_4_number_patterns.json';p=R/rel;before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before)
 selected=[c for c in after['cases'] if c['id'] in CHANGES];assert len(selected)==len(CHANGES)
 if all(c['task']==CHANGES[c['id']][1] for c in selected):reconcile_conditions();print('Decimal prompts already clarified');return
 for c in selected:
  old,new=CHANGES[c['id']];assert c['task']==old;c['task']=new
  if 'alternative_decision' in c:
   assert c['alternative_decision']['performance']==old;c['alternative_decision']['performance']=new
  c.setdefault('history',[]).append(dict(date='2026-11-04',reviewer='Codex',kind='prompt_clarification',previous_task=old,scope=REASON))
 assert before['entries']==after['entries']
 for a,b in zip(before['cases'],after['cases']):
  assert {k:v for k,v in a.items() if k not in ('task','alternative_decision','history')}=={k:v for k,v in b.items() if k not in ('task','alternative_decision','history')}
  assert {k:v for k,v in a.get('alternative_decision',{}).items() if k!='performance'}=={k:v for k,v in b.get('alternative_decision',{}).items() if k!='performance'}
 lp=R/'data/hierarchy_integration_review.json';ledger=json.loads(lp.read_text(encoding='utf-8'));assert ledger['source_hashes'][rel]==content_hash(before)
 prior=ledger['source_hashes'][rel];ledger['source_hashes'][rel]=content_hash(after)
 ledger['history'].append(dict(date='2026-11-04',reviewer='Codex',kind='prompt_scope_reconciliation',case_ids=list(CHANGES),previous_source_hash=prior,scope=REASON))
 # Re-review the existing item selections against the verified metadata delta.
 entries={};cases={}
 for path in (R/'data').glob('goal_hierarchy_*.json'):
  d=json.loads(path.read_text(encoding='utf-8'));entries.update({e['code']:e for e in d['entries']});cases.update({c['id']:c for c in d['cases']})
 cases.update({c['id']:c for c in after['cases']});old_cases={c['id']:c for c in before['cases']}
 mp=R/'data/curriculum_mapping_reviews.json';registry=json.loads(mp.read_text(encoding='utf-8'));affected=0
 for review in registry['reviews'].values():
  ids=[cid for cid in review['case_snapshots'] if cid in CHANGES]
  if not ids:continue
  assert set(changed_targets(review,entries,cases))=={'case:'+cid for cid in ids}
  previous={cid:review['case_snapshots'][cid] for cid in ids}
  assert all(previous[cid]==digest(old_cases[cid]) for cid in ids)
  for cid in ids:review['case_snapshots'][cid]=digest(cases[cid])
  review.setdefault('history',[]).append(dict(date='2026-11-04',reason=REASON,case_ids=ids,previous_case_snapshots=previous));affected+=1
 p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');mp.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 reconcile_conditions();print('Clarified 3 prompts; explicitly re-reviewed item mappings:',affected)
if __name__=='__main__':main()

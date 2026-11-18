"""Clarify the fixed objects in a counting prompt without changing its model."""
import copy,json
from pathlib import Path
from write_hierarchy_transition_tables import content_hash,build as build_transitions
R=Path(__file__).resolve().parents[1]
OLD='색상3종과포장2종을 하나씩 고르는 가상 상품에서 검정·종이 포장만 금지한다. 허용 상품 수와 서로 다른3개 진열 순서를 센다.'
NEW='색상3종과포장2종을 하나씩 고르는 가상 상품에서 검정·종이 포장만 금지한다. 허용 상품 수를 구하고, 미리 고른 서로 다른3개 상품을 모두 한 번씩 한 줄로 진열하는 순서를 센다.'
def reconcile_condition():
 snapshots,result=build_transitions();key='early-12직수04-01-bundles|bundles|0'
 lp=R/'data/hierarchy_integration_review.json';ledger=json.loads(lp.read_text(encoding='utf-8'))
 if ledger['condition_snapshots'][key]==snapshots[key]:return
 assert result['summary']['needs_review']==[key] and not result['summary']['removed_review_snapshots'] and not result['summary']['source_changes_since_review']
 row=next(r for r in result['records'] if r['case_id']=='early-12직수04-01-bundles')
 assert row['source_goal']=='9수04-05:count' and row['target_task']==NEW
 previous=copy.deepcopy(row);previous['target_task']=OLD
 assert content_hash(previous)==ledger['condition_snapshots'][key],'Condition changed beyond the explicitly reviewed prompt clarification'
 old_hash=ledger['condition_snapshots'][key];ledger['condition_snapshots'][key]=snapshots[key]
 ledger['history'].append(dict(date='2026-11-04',reviewer='Codex',kind='condition_prompt_re_review',condition_keys=[key],previous_snapshot=old_hash,new_snapshot=snapshots[key],
  scope='출발 목표9수04-05:count의 열거·조건에 맞는 경우 세기는 고정3개 진열의6가지 계산에 그대로 적용. 전체 조건 기록의 유일한 차이가 target_task의 선택 대상 명료화임을 이전 해시로 대조.'))
 lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 build_transitions()
def main():
 rel='data/goal_hierarchy_work_culture_inquiry.json';p=R/rel;before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before)
 case=next(c for c in after['cases'] if c['id']=='early-12직수04-01-bundles')
 if case['task']==NEW:reconcile_condition();print('Counting prompt already clarified; condition review reconciled');return
 assert case['task']==OLD and case['alternative_decision']['performance']==OLD
 case['task']=NEW;case['alternative_decision']['performance']=NEW
 case['history'].append(dict(date='2026-11-04',reviewer='Codex',kind='prompt_clarification',previous_task=OLD,
  scope='3개 상품이 미리 선택되어 있음을 명시. 허용 5종 중 3종을 새로 고르는 60가지 문제와 구별. 기존 답6·풀이·목표·선수 조건 유지.'))
 assert before['entries']==after['entries']
 for a,b in zip(before['cases'],after['cases']):
  assert {k:v for k,v in a.items() if k not in ('task','alternative_decision','history')}=={k:v for k,v in b.items() if k not in ('task','alternative_decision','history')}
  assert {k:v for k,v in a.get('alternative_decision',{}).items() if k!='performance'}=={k:v for k,v in b.get('alternative_decision',{}).items() if k!='performance'}
 lp=R/'data/hierarchy_integration_review.json';ledger=json.loads(lp.read_text(encoding='utf-8'))
 assert ledger['source_hashes'][rel]==content_hash(before)
 prior=ledger['source_hashes'][rel];ledger['source_hashes'][rel]=content_hash(after)
 ledger['history'].append(dict(date='2026-11-04',reviewer='Codex',kind='prompt_scope_reconciliation',case_ids=[case['id']],previous_source_hash=prior,
  scope='고정된3개 물품의 순서임을 발문에 명시. 전체 원고 비교로 목표·공유조건·모든 경로의 조건·계산·진단이 그대로임을 확인.'))
 p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Clarified 1 counting prompt; all goals, conditions and solutions preserved')
 reconcile_condition()
if __name__=='__main__':main()

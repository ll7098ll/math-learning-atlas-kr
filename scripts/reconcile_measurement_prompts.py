"""Reconcile only two explicitly clarified prompts, without waiving conditions."""
import json
from pathlib import Path
from write_hierarchy_transition_tables import build,content_hash
R=Path(__file__).resolve().parents[1]
ALLOWED={'early-4수03-19-capacity-operations':'두 들이의 합과 차를 각각 구하고 단위 교환을 설명한다.',
         'early-4수03-23-weight-operations':'두 무게의 합과 차를 각각 구하고 단위 교환을 설명한다.'}
def main():
 old=json.loads((R/'data/goal_condition_review_table.json').read_text(encoding='utf-8'))
 ledger_path=R/'data/hierarchy_integration_review.json';ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
 build()
 new=json.loads((R/'data/goal_condition_review_table.json').read_text(encoding='utf-8'))
 key=lambda r:r['case_id']+'|'+r['route_id']+'|'+str(r['condition_index'])
 previous={key(r):r for r in old['records']};current={key(r):r for r in new['records']}
 assert previous.keys()==current.keys()
 cases=json.loads((R/'data/goal_hierarchy_primary_3_4_geometry_measure_data.json').read_text(encoding='utf-8'))['cases']
 cases={c['id']:c for c in cases}
 changed=[]
 for k,b in current.items():
  a=previous[k]
  if a==b:continue
  assert b['case_id'] in ALLOWED,k
  assert a['target_task']==ALLOWED[b['case_id']]
  assert b['target_task']==cases[b['case_id']]['goal']+' 각각의 상황에서 단위 교환 과정을 설명한다.'
  assert {field for field in a if a[field]!=b[field]}=={'target_task'}
  assert ledger['condition_snapshots'][k]==content_hash(a)
  changed.append(k)
 for k in changed:ledger['condition_snapshots'][k]=content_hash(current[k])
 prior_sources=dict(ledger['source_hashes']);source_changes=[]
 for rel,digest in prior_sources.items():
  value=content_hash(json.loads((R/rel).read_text(encoding='utf-8')))
  if value!=digest:
   assert rel=='data/goal_hierarchy_primary_3_4_geometry_measure_data.json',rel
   ledger['source_hashes'][rel]=value;source_changes.append(rel)
 if changed or source_changes:
  ledger['history'].append(dict(date='2026-11-04',reviewer='Codex',kind='prompt_scope_reconciliation',
   scope='목표에 있던 들이·무게 수치를 문제 본문에도 명시. 조건·출발 목표·적용 목표·풀이의 차이가 없음을 전수 비교.',
   condition_keys=changed,previous_source_hashes=prior_sources,
   previous_condition_snapshots={k:content_hash(previous[k]) for k in changed}))
  ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 build()
 print('Reconciled prompt-only differences:',len(changed))
if __name__=='__main__':main()

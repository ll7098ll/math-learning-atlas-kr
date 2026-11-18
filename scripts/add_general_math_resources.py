"""Add five explicit engineering-tool resources and reconcile metadata only."""
import copy,json
from pathlib import Path
from write_hierarchy_transition_tables import content_hash
R=Path(__file__).resolve().parents[1]
IDS=['early-12대수01-07-graphs','early-12대수02-02-unit-circle','early-12미적Ⅰ-01-01-hole','early-12미적Ⅰ-02-01-derivative','early-12미적Ⅰ-03-03-signed-area']
RESOURCE=dict(label='함수·극한·미분·부호 있는 넓이의 계산 모형 CSV',path='examples/model-general-functions.csv')
def main():
 rel='data/goal_hierarchy_algebra_calculus_one.json';p=R/rel;before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before)
 changed=[]
 for c in after['cases']:
  if c['id'] in IDS and RESOURCE not in c.get('resources',[]):
   old=list(c.get('resources',[]));c.setdefault('resources',[]).append(RESOURCE)
   c.setdefault('history',[]).append(dict(date='2026-11-04',reviewer='Codex',kind='tool_resource',scope='기존 문제·풀이·조건을 바꾸지 않고 계산 모형 CSV를 연결',previous_resources=old))
   changed.append(c['id'])
 if not changed:print('Resources already attached');return
 ledger_path=R/'data/hierarchy_integration_review.json';ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
 assert ledger['source_hashes'][rel]==content_hash(before)
 assert before['entries']==after['entries']
 for a,b in zip(before['cases'],after['cases']):
  assert {k:v for k,v in a.items() if k not in ('resources','history')}=={k:v for k,v in b.items() if k not in ('resources','history')}
 prior=ledger['source_hashes'][rel];ledger['source_hashes'][rel]=content_hash(after)
 ledger['history'].append(dict(date='2026-11-04',reviewer='Codex',kind='tool_resource_reconciliation',scope='5개 과제의 CSV 연결 외에 문제·풀이·조건·목표가 같음을 전수 비교',case_ids=changed,previous_source_hash=prior))
 p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Attached resources:',len(changed))
if __name__=='__main__':main()

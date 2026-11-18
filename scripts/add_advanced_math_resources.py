"""Attach tool data while proving original tasks and conditions unchanged."""
import copy,json
from pathlib import Path
from write_hierarchy_transition_tables import content_hash
from mapping_review_author import resource_file
R=Path(__file__).resolve().parents[1]
CALCULUS=dict(label='수열·부분합·리만합의 유한 계산 모형 CSV',path='examples/model-advanced-calculus.csv')
GEOMETRY=dict(label='이차곡선·구의 단면·정사영의 계산 모형 CSV',path='examples/model-geometry-tools.csv')
RESOURCES={**dict.fromkeys(['early-12미적Ⅱ-01-01-sequences','early-12미적Ⅱ-01-04-series','early-12미적Ⅱ-03-04-rectangles'],CALCULUS),
 **dict.fromkeys(['early-12기하01-01-parabola','early-12기하01-02-ellipse','early-12기하01-03-hyperbola','early-12기하02-03-projection','early-12기하02-05-sphere'],GEOMETRY)}
def main():
 rel='data/goal_hierarchy_calculus_two_geometry.json';p=R/rel;before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before)
 changed=[]
 assert set(RESOURCES)<={c['id'] for c in after['cases']}
 for c in after['cases']:
  resource=RESOURCES.get(c['id'])
  if resource and resource not in c.get('resources',[]):
   assert resource_file(resource['path']).is_file()
   old=list(c.get('resources',[]));c.setdefault('resources',[]).append(dict(resource))
   c.setdefault('history',[]).append(dict(date='2026-11-04',reviewer='Codex',kind='tool_resource',scope='문제·풀이·조건을 유지하며 계산 모형 CSV 연결',previous_resources=old));changed.append(c['id'])
 if not changed:print('Resources already attached');return
 ledger_path=R/'data/hierarchy_integration_review.json';ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
 assert ledger['source_hashes'][rel]==content_hash(before)
 assert before['entries']==after['entries']
 for a,b in zip(before['cases'],after['cases']):assert {k:v for k,v in a.items() if k not in ('resources','history')}=={k:v for k,v in b.items() if k not in ('resources','history')}
 prior=ledger['source_hashes'][rel];ledger['source_hashes'][rel]=content_hash(after)
 ledger['history'].append(dict(date='2026-11-04',reviewer='Codex',kind='tool_resource_reconciliation',scope='8개 과제의 CSV 연결 외 문제·풀이·조건·목표가 같음을 전수 비교',case_ids=changed,previous_source_hash=prior))
 p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Attached resources:',len(changed))
if __name__=='__main__':main()

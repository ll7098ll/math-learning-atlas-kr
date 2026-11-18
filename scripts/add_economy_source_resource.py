"""Attach source data with a metadata-only integration reconciliation."""
import copy,json
from pathlib import Path
from write_hierarchy_transition_tables import content_hash
R=Path(__file__).resolve().parents[1]
CASE_ID='early-12경수01-01-index'
RESOURCE=dict(label='World Bank 한국 GDP 연간 성장률 2020–2024 동결본(실제 공개 통계)',path='examples/source-korea-gdp-growth.csv')

def main():
 rel='data/goal_hierarchy_economy_ai.json';p=R/rel;before=json.loads(p.read_text(encoding='utf-8'));after=copy.deepcopy(before)
 case=next(c for c in after['cases'] if c['id']==CASE_ID)
 if RESOURCE in case.get('resources',[]):print('Source resource already attached');return
 assert (R/'data/teaching_examples/source-korea-gdp-growth.csv').is_file()
 case.setdefault('resources',[]).append(RESOURCE.copy())
 case['history'].append(dict(date='2026-11-04',reviewer='Codex',kind='source_resource',scope='기존 가상 지수 문제·풀이·조건 유지. 실제 GDP 성장률 비교 활동은 내용 체계의 별도 보완 발문으로 제공.'))
 lp=R/'data/hierarchy_integration_review.json';ledger=json.loads(lp.read_text(encoding='utf-8'))
 assert ledger['source_hashes'][rel]==content_hash(before)
 assert before['entries']==after['entries']
 for a,b in zip(before['cases'],after['cases']):assert {k:v for k,v in a.items() if k not in ('resources','history')}=={k:v for k,v in b.items() if k not in ('resources','history')}
 prior=ledger['source_hashes'][rel];ledger['source_hashes'][rel]=content_hash(after)
 ledger['history'].append(dict(date='2026-11-04',reviewer='Codex',kind='source_resource_reconciliation',scope='기존40개 과제의 문제·풀이·조건·목표 동일성 비교. 경제 지표 한 과제에 출처 보존 CSV만 추가.',case_ids=[CASE_ID],previous_source_hash=prior))
 p.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Attached official statistics to 1 case; all task content unchanged')
if __name__=='__main__':main()

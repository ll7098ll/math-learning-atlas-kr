"""Persist explicit item decisions and immutable target-content snapshots."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def entry_digest(entry):return digest({k:v for k,v in entry.items() if k!='authored_from'})
def changed_targets(review,entries,cases):
 return (['entry:'+code for code,value in review.get('entry_snapshots',{}).items() if code not in entries or entry_digest(entries[code])!=value]
  +['case:'+cid for cid,value in review.get('case_snapshots',{}).items() if cid not in cases or digest(cases[cid])!=value]
  +['resource:'+rel for rel,value in review.get('resource_snapshots',{}).items() if not (R/rel).is_file() or hashlib.sha256((R/rel).read_bytes()).hexdigest()!=value])
def resource_file(public_path):
 name=Path(public_path).name
 assert public_path=='examples/'+name
 if name.endswith('.csv'):return R/'data/teaching_examples'/name
 aliases={'stats-inference.py':'statistical_tools.py','economy-ai-models.py':'economy_ai_models.py'}
 assert name in aliases,public_path
 return R/'scripts'/aliases[name]
def write_decisions(page,decisions,extensions,reviewed_changes=None):
 structure=json.loads((R/'data/curriculum_structure.json').read_text(encoding='utf-8'))
 path=R/'data/curriculum_mapping_reviews.json'
 registry=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'schema_version':1,'reviews':{}}
 entries={};cases={}
 for p in (R/'data').glob('goal_hierarchy_*.json'):
  d=json.loads(p.read_text(encoding='utf-8'));entries.update({e['code']:e for e in d['entries']});cases.update({c['id']:c for c in d['cases']})
 items=[i for i in structure['items'] if i['pdf_page']==page]
 assert set(decisions)=={int(i['id'].rsplit('-',1)[1]) for i in items}
 for item in items:
  n=int(item['id'].rsplit('-',1)[1]);codes,reason=decisions[n]
  assert set(codes)<=set(item['scope_codes'])
  ids=list(dict.fromkeys(cid for code in codes for g in entries[code]['goals'] for cid in g['case_ids']))
  resources={resource_file(resource['path']) for cid in ids for resource in cases[cid].get('resources',[])}
  record=dict(source_text=item['text'],state='self_checked_scope_mapping',reviewer='Codex',date='2026-11-04',
   review_scope='공식 내용 항목과 성취기준·목표의 의미 대응. 태도와 타 교과 확장은 새 관찰 설계로 구별함.',standard_codes=codes,
   goal_ids=[g['id'] for code in codes for g in entries[code]['goals']],case_ids=ids,rationale=reason,
   entry_snapshots={code:entry_digest(entries[code]) for code in codes},case_snapshots={cid:digest(cases[cid]) for cid in ids},
   resource_snapshots={path.relative_to(R).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(resources)},
   independent_review=False,student_validated=False)
  if n in extensions:record['observation_extension']=dict(question=extensions[n][0],expected=extensions[n][1],status='authored_activity_not_observed')
  prior=registry['reviews'].get(item['source_fingerprint'])
  if prior:
   changes=changed_targets(prior,entries,cases)
   assert not changes or (reviewed_changes or {}).get(n), 'Changed target needs explicit re-review rationale: '+item['id']+' '+str(changes)
   record['history']=prior.get('history',[])
   if {k:v for k,v in prior.items() if k!='history'}!={k:v for k,v in record.items() if k!='history'}:
    record['history']=record['history']+[dict(date='2026-11-04',reason=(reviewed_changes or {}).get(n,'대응 원장 보강 및 대상 원본 해시 보존'),previous_record={k:v for k,v in prior.items() if k!='history'})]
  registry['reviews'][item['source_fingerprint']]=record
 path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f'Recorded {len(items)} explicit decisions for PDF page {page}')

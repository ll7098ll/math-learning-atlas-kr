"""Apply explicitly authored scope reviews; never refresh changed evidence automatically."""
import copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILE='data/relation_analysis_reviews.json'
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def read(root,path):return json.loads((root/path).read_text(encoding='utf-8'))

def materials(root=ROOT):
 standards={s['code']:s for s in read(root,'data/standards.json')['standards']}
 raw={r['id']:r for r in read(root,'data/relations.json')['relations']};revisions={};entries={};cases={}
 for p in sorted((root/'data').glob('revisions_*.json')):
  data=json.loads(p.read_text(encoding='utf-8'));assert not revisions.keys()&data.keys(),'Duplicate revision source'
  revisions.update({c:dict(file=p.name,value=v) for c,v in data.items()})
 # REV identities are generated from authored revision links, never from the
 # previously generated output. Bind the exact link, its index and its file.
 for code,revision in revisions.items():
  value=revision['value']
  for i,link in enumerate(value.get('internalRelations',[])+value.get('externalRelations',[])):
   source=link.get('from',code);target=link['target']
   if source==target:continue
   rid='REV-'+code+'-'+str(i+1);assert rid not in raw,'Duplicate authored relation: '+rid
   candidate=link.get('reviewState')=='candidate' or '후보' in str(link.get('status',''))
   raw[rid]=dict(id=rid,to='standard:'+target,type='meaning_connection' if candidate else link.get('kind','meaning_connection'),authored_from='data/'+revision['file'],authored_link_index=i,authored_link=link)
   raw[rid]['from']='standard:'+source
 for p in sorted((root/'data').glob('goal_hierarchy_*.json')):
  data=json.loads(p.read_text(encoding='utf-8'))
  entries.update({e['code']:e for e in data['entries']});cases.update({c['id']:c for c in data['cases']})
 archive=root/'data/initial_case_studies.json'
 initial=json.loads(archive.read_text(encoding='utf-8')) if archive.exists() else {}
 return dict(standards=standards,raw=raw,revisions=revisions,entries=entries,cases=cases,initial=initial)

def source_value(rid,root=ROOT,data=None):
 data=data or materials(root);r=data['raw'][rid];endpoints={}
 for code in [r['from'][9:],r['to'][9:]]:
  s=data['standards'][code];e=data['entries'][code]
  ids=list(dict.fromkeys(cid for g in e['goals'] for cid in g['case_ids']));cases=[data['cases'][cid] for cid in ids]
  resources={}
  for case in cases:
   for resource in case.get('resources',[]):
    public=resource['path'];name=Path(public).name;assert public=='examples/'+name
    aliases={'stats-inference.py':'statistical_tools.py','economy-ai-models.py':'economy_ai_models.py'}
    if name.endswith('.csv'):path=Path('data/teaching_examples')/name
    else:assert name in aliases;path=Path('scripts')/aliases[name]
    resources[path.as_posix()]=hashlib.sha256((root/path).read_bytes()).hexdigest()
  endpoints[code]=dict(official={k:s[k] for k in ['code','statement_display','school_level','subject','domain']},revision=data['revisions'][code],goal_entry={k:v for k,v in e.items() if k!='authored_from'},cases=cases,resources=resources)
  if code in data['initial']:endpoints[code]['initial_case_study']=data['initial'][code]
 return dict(original_relation=r,endpoints=endpoints)

def load_reviews(root=ROOT,data=None):
 if not (root/FILE).exists():return dict(schema_version=1,records={})
 registry=read(root,FILE);data=data or materials(root)
 for rid,review in registry['records'].items():
  assert rid in data['raw'] and review['relation_id']==rid
  assert review['state']=='self_checked_scope_math' and review['reviewer'] and review['date']
  assert review['independent_review'] is False and review['student_validated'] is False
  for key in ['scope','rationale','conditions','diagnostic','expected_response','limit','additional_learning','mathematical_check','type_decision_reason']:
   assert review[key],rid+': '+key
  assert isinstance(review['conditions'],list) and all(isinstance(v,str) and v for v in review['conditions'])
  assert isinstance(review['additional_learning'],list) and all(isinstance(v,str) and v for v in review['additional_learning'])
  assert review['type'] in ['generalizes','meaning_connection','requires_for_task','contrasts']
  raw=data['raw'][rid]
  assert review['from']==raw['from'] and review['to']==raw['to']
  assert digest(source_value(rid,root,data))==review['source_snapshot'],'Changed relation or endpoint needs explicit re-review: '+rid
 return registry

def apply_review(record,review):
 result=copy.deepcopy(record)
 assert result['id']==review['relation_id'] and result['from']==review['from'] and result['to']==review['to']
 previous={k:copy.deepcopy(result.get(k)) for k in ['type','rationale','conditions','diagnostic','expected_response','limit','review_state']}
 for key in ['type','rationale','conditions','diagnostic','expected_response','limit','additional_learning']:
  result[key]=copy.deepcopy(review[key])
 result['review_state']='self_checked'
 result['scope']=review['scope'];result['analysis_review_note']=review['scope']+' '+review['limit']
 result['condition_scope_note']='아래 조건은 이 관계에서 새로 대조한 수행 범위에 한정한다. 도착 기준 전체의 모든 연산 조건을 대신하지 않는다.'
 result['analysis_review_evidence']=dict(file=FILE,relation_id=review['relation_id'],source_snapshot=review['source_snapshot'],reviewer=review['reviewer'],date=review['date'],scope=review['scope'],type_decision_reason=review['type_decision_reason'],mathematical_check=review['mathematical_check'],independent_review=False,student_validated=False)
 result['analysis_review_history']=copy.deepcopy(review.get('history',[]))+[dict(date=review['date'],reviewer=review['reviewer'],reason=review['type_decision_reason'],previous_derived_fields=previous)]
 # Existing external evidence belongs to its original review, not this self-check.
 return result

def apply_reviews(records,root=ROOT):
 registry=load_reviews(root);seen=set();out=[]
 for r in records:
  if r['id'] in registry['records']:
   r=apply_review(r,registry['records'][r['id']]);seen.add(r['id'])
  out.append(r)
 assert seen==set(registry['records']),'Reviewed relation disappeared during generation'
 return out

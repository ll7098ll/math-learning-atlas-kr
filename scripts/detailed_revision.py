"""Render individually authored revisions; preserve the three original case studies."""
import json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TITLES=['공식 성취기준과 범위','핵심 의미와 목표 수행','대표 과제와 성공한 수행','수학적 의미와 성립 조건','세부 사고와 관찰할 수행','수행 과정과 대안 경로','표현 사이의 대응','오류와 진단 및 후속 질문','학습 활동과 피드백','같은 학교급 안의 관계와 위계','다른 학교급으로 이어지는 관계','근거와 검토 상태']
IDS=['curriculum','meaning','task','mathematics','thinking','paths','representations','diagnosis','activities','internal','connections','references']
PILOTS=['6수01-10','6수02-03','6수03-14']
def load_revisions():
 result={}
 for p in sorted((ROOT/'data').glob('revisions_*.json')):
  entries=json.loads(p.read_text(encoding='utf-8-sig'))
  assert isinstance(entries,dict),p
  assert not (result.keys() & entries.keys()), ('duplicate authored code',p)
  for value in entries.values():value['_source_file']=p.name
  result.update(entries)
 return result
def prose(x):
 if isinstance(x,str):return x
 if isinstance(x,list):return '\n\n'.join(prose(v) for v in x)
 if isinstance(x,dict):return ' · '.join(f'{k}: {prose(v)}' for k,v in x.items())
 return str(x or '')
def table(headers,rows):
 def cell(v):return prose(v).replace('|','\\|').replace('\n',' ')
 return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join('---' for h in headers)+'|']+['| '+' | '.join(cell(v) for v in row)+' |' for row in rows])
def as_list(value):return value if isinstance(value,list) else [value] if value else []
def bullets(values):return '\n'.join('- '+prose(x) for x in values)
def render_branches(branches):
 result=[]
 for x in branches:
  p=x.get('diagnosis',{})
  if isinstance(p,dict):p=table(['진단 질문','기대하는 설명','가능한 해석','후속 확인'],[[p.get(k,'') for k in ['question','expected','interpretation','followup']]])
  result.append('### 하위 목표 '+x.get('goal','')+'\n\n**과제** '+x.get('task','')+'\n\n**풀이와 설명** '+x.get('solution','')+'\n\n'+str(p))
 return '\n\n'.join(result)

def apply(analyses,inventory,relations):
 from literature_review import load_registry,notes_for
 from hierarchy_review import analysis_review_record
 literature=load_registry()
 from goal_hierarchy import load_goal_hierarchies
 goal_entries,goal_cases,all_goals=load_goal_hierarchies(inventory['standards'])
 by_case={c['id']:c for c in goal_cases}
 from mapping_review_author import changed_targets
 mapping_file=ROOT/'data/curriculum_mapping_reviews.json'
 mapping_records=json.loads(mapping_file.read_text(encoding='utf-8')).get('reviews',{}) if mapping_file.exists() else {}
 activity_extensions={}
 for mapping in mapping_records.values():
  if mapping.get('observation_extension') and not changed_targets(mapping,goal_entries,by_case):
   for code in mapping['standard_codes']:activity_extensions.setdefault(code,[]).append(mapping)
 revisions={c:r for c,r in load_revisions().items() if r.get('taskSolution') and r.get('review',{}).get('contentRevision')!='pending'};by={s['code']:s for s in inventory['standards']}
 archive=ROOT/'data/initial_case_studies.json'
 if not archive.exists():archive.write_text(json.dumps({c:(ROOT/f'analyses/{c}.md').read_text(encoding='utf-8') for c in PILOTS},ensure_ascii=False,indent=2),encoding='utf-8')
 originals=json.loads(archive.read_text(encoding='utf-8'))
 enriched=[dict(r) for r in relations if not r['id'].startswith('REV-')]
 for code,rev in revisions.items():
  assert code in by,code
  for i,link in enumerate(rev.get('internalRelations',[])+rev.get('externalRelations',[])):
   target=link['target'];source=link.get('from',code)
   if source==target:continue
   assert source in by and target in by,(source,target)
   if link in rev.get('internalRelations',[]):assert by[source]['school_level']==by[target]['school_level'],(source,target)
   kind=link.get('kind','meaning_connection')
   candidate=link.get('reviewState')=='candidate' or '후보' in prose(link.get('status',''))
   if candidate:kind='meaning_connection'
   assert kind in ['generalizes','requires_for_task','meaning_connection','contrasts'],kind
   rid='REV-'+code+'-'+str(i+1)
   enriched.append({'id':rid,'from':'standard:'+source,'to':'standard:'+target,'type':kind,
    'scope':link.get('scope','개별 상세 분석의 학교급 내부 관계'),'rationale':link['rationale'],
    'conditions':as_list(link.get('conditions',[])),'additional_learning':as_list(link.get('additionalLearning',[])),
    'diagnostic':link.get('diagnostic',''),'limit':link.get('limit','명시한 수행과 설명의 관계이며 유일한 학습 순서나 선행 숙달을 뜻하지 않는다.'),
    'evidence_kind':'자체 수학적 분석','source_ids':['CURRICULUM_2022_33'],'status':'초안',
    'independent_review':False,'student_validated':False,'review_state':'candidate' if candidate else 'self_checked',
    'authored_from':'data/'+rev['_source_file']})
 from authored_hierarchy import load_claims
 authored_claims=load_claims(ROOT, by, [r['id'] for r in enriched])
 authored_ids={r['id'] for r in authored_claims}
 enriched.extend(authored_claims)
 # Original records remain addressable. Replace family-wide conditions in
 # the derived corpus with the explicit authored task scope, retaining history.
 checked={}
 for r in enriched:
  if r['id'].startswith('REV-') and r.get('review_state')=='self_checked':checked.setdefault((r['from'][9:],r['to'][9:]),r)
 for r in enriched:
  if r['id'].startswith('REV-') or r['id'] in authored_ids or not r['from'].startswith('standard:') or not r['to'].startswith('standard:'):continue
  a,b=r['from'][9:],r['to'][9:]
  match=checked.get((a,b))
  target=revisions.get(b,{})
  corrected=match.get('conditions') if match else target.get('conditions')
  if corrected:
   r['original_conditions']=r.get('conditions',[])
   r['conditions']=as_list(corrected)
   r['condition_scope_note']='아래 조건'+('은 새로 자체 분석한 연결의 선택 경로에 적용한다.' if match else '은 도착 기준의 대표 과제에 적용한다. 두 기준 전체의 필수 선수 관계를 입증하는 조건은 아니다.')
   r['revision_history']=[{'reason':'공통 프로필의 조건을 개별 과제와 관계의 조건으로 교정','original_conditions':r['original_conditions'],'authored_from':match.get('authored_from') if match else 'data/'+target.get('_source_file','')}]
 for r in enriched:
  if not (r['from'].startswith('standard:') and r['to'].startswith('standard:')):continue
  r.update(analysis_review_record(r))
  r.setdefault('expected_response','연결 이유를 양쪽 수행의 대상·표현·조건으로 설명한다: '+r['rationale']+' 연결은 기록한 범위에 한정한다.')
  r['diagnostic_task_ids']=[c['id'] for c in goal_cases if c['standard'] in (r['from'][9:],r['to'][9:])]
  r['diagnostic_goal_ids']=[g['id'] for code in (r['from'][9:],r['to'][9:]) for g in goal_entries[code]['goals']]
 from relation_analysis_review import apply_reviews
 enriched=apply_reviews(enriched)
 from relation_literature_review import apply_literature_context
 apply_literature_context(enriched,literature)
 report=[]
 for code,a in analyses.items():
  s=by[code];rev=revisions.get(code);sections=[]
  internal=[r for r in enriched if r['from'].startswith('standard:') and r['to'].startswith('standard:') and 'standard:'+code in [r['from'],r['to']] and by[r['from'][9:]]['school_level']==by[r['to'][9:]]['school_level']]
  external=[r for r in enriched if r['from'].startswith('standard:') and r['to'].startswith('standard:') and 'standard:'+code in [r['from'],r['to']] and by[r['from'][9:]]['school_level']!=by[r['to'][9:]]['school_level']]
  def relation_table(records):
   rows=[]
   literature_rows=[]
   for r in records:
    other=r['to'][9:] if r['from']=='standard:'+code else r['from'][9:]
    diagnosis=r.get('diagnostic','')
    if r.get('analysis_review_evidence'):diagnosis+=' 기대 설명: '+r['expected_response']+' 해석 한계: '+r['limit']
    rows.append([f'[{other}]({other}.md)',{'generalizes':'의미 확장','requires_for_task':'과제별 필요 조건','meaning_connection':'의미 연결','contrasts':'대조'}.get(r['type'],r['type']),r['rationale'],([r['condition_scope_note']]+as_list(r.get('conditions',[])) if r.get('condition_scope_note') else r.get('conditions',[])),r.get('additional_learning',[]),diagnosis,{'self_checked':'수학적 자체 점검 초안','candidate':'검토 후보'}.get(r.get('review_state'),'기존 분석 초안')])
    for note in r.get('literature_context',[]):
     literature_rows.append(f"- {r['id']} · [{note['claim_id']}]({note['url']}) · {note['role']}. {note['finding']} {note['limit']}")
   if not rows:return '현재 분석 범위에 기록된 관계가 없습니다. 선수 개념이 없다는 뜻은 아닙니다.'
   body=table(['상대 기준','관계 종류','연결 이유','성립 조건','추가 사고','확인 질문','검토 상태'],rows)
   if literature_rows:body+='\n\n### 관계별 문헌 대조\n\n'+'\n'.join(literature_rows)
   return body
  if code in PILOTS:
   source=originals[code]
   original_sections=[(m[1],m[2].strip()) for m in re.finditer(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',source,re.M|re.S)]
   grouped={i:[] for i in range(12)}
   for title,body in original_sections:
    index=0 if title=='교육과정과 목표' else 3 if title.startswith('수학적 의미') else 4 if '하위요소' in title else 6 if title=='표현 연결' else 7 if '진단' in title else 8 if title.startswith('학습 활동') else 10 if '연결' in title else 11 if title=='다음 조사' else 5
    grouped[index].append('### '+title+'\n\n'+body)
   grouped[1]=[source.split('\n\n')[1]]
   grouped[2]=[a['task'] or '대표 과제와 성공한 수행은 아래 원래 과제 설명 및 경로별 수치 사례에서 확인한다.']
   grouped[9]=[relation_table(internal)]
   grouped[10]=['### 초기 연결 설명 보존\n\n아래 초기 설명은 작성 당시의 분석 기록이다. 현재 관계별 조건·질문·자체 점검 상태는 이어지는 표에서 확인한다.']+grouped[10]+['### 현재 관계별 분석\n\n'+relation_table(external)]
   sections=[{'id':id,'title':title,'body':'\n\n'.join(grouped[i]) or '해당 내용은 연결된 원래 과제의 상세 설명에서 함께 확인한다.'} for i,(id,title) in enumerate(zip(IDS,TITLES))]
  elif rev:
   required=['mathematicalMeaning','taskSolution','conditions','paths','thinking','representations','diagnostics','feedback','internalRelations']
   assert all(k in rev for k in required),(code,[k for k in required if k not in rev])
   thinking=rev['thinking'];probes=rev['diagnostics']
   a.update({'stepObjects':thinking,'probeObjects':probes,'paths':rev['paths'],'profile':{},'revision':rev,'commonProbe':[]})
   body=[f"- 성취기준: **{code}**\n- 원문: {s.get('statement_display',s['statement_extracted'])}\n- 범위: {s['school_level']} {s['grade_band']} {s['subject']} {s['domain']}\n- 원문 위치: PDF {', '.join(map(str,s['source_pdf_pages']))}쪽, 인쇄 {', '.join(map(str,s['source_printed_pages']))}쪽.",
    a['idea'],a['task']+('\n\n'+table(['하위 목표','별도로 구성할 사고','확인 과제'],a['subgoals']) if a.get('subgoals') else '')+'\n\n**성공한 수행**\n\n'+a['idea']+' '+thinking[-1]['observable'],
    prose(rev['mathematicalMeaning'])+'\n\n**적용 조건**\n\n'+bullets(rev['conditions'])+'\n\n**교육과정 범위**\n\n'+a['limit'],
    table(['사고 요소','구성할 의미','이 사고가 필요한 이유','관찰할 수행'],[[x['label'],x['meaning'],x.get('reason',''),x['observable']] for x in thinking]),
    '### 대표 과제의 해설\n\n'+prose(rev['taskSolution'])+('\n\n'+render_branches(rev['branchAnalyses']) if rev.get('branchAnalyses') else '')+'\n\n'+'\n\n'.join(f'### 설명 경로 {i+1}\n\n'+prose(path) for i,path in enumerate(rev['paths']) if prose(path).strip()!=prose(rev['taskSolution']).strip())+'\n\n경로별 조건을 구별하며, 사고 요소의 나열을 고정된 발달 순서로 해석하지 않는다.',
    bullets(rev['representations']),
    table(['질문','기대하는 설명','반응의 가능한 해석','후속 확인'],[[p['question'],p['expected'],p['interpretation'],p['followup']] for p in probes]),
    bullets(rev['feedback']),relation_table(internal),relation_table(external),
    f'공식 목표와 범위의 근거는 교육부 고시 제2022-33호 {code}이다. 과제 해설·사고 분석·관계는 자체 수학적 분석과 교수 설계 초안이다.\n\n'+'\n\n'.join(str(rev.get('review',{}).get(k,'')) for k in ['status','mathematical','scope','notes','coverage'] if rev.get('review',{}).get(k))+'\n\n독립 검토와 학생 반응 검증은 수행 전이다. 원문 대조 상태와 내용 검토 상태는 별도로 관리한다.']
   if rev.get('references'):
    body[11]+='\n\n### 개별 참고 자료'+'\n\n'+'\n\n'.join('['+ref['title']+']('+ref['url']+')\n\n확인 위치: '+prose(ref.get('location',''))+'\n\n지원하는 내용: '+prose(ref.get('support','')) for ref in rev['references'])
   sections=[{'id':id,'title':title,'body':body[i]} for i,(id,title) in enumerate(zip(IDS,TITLES))]
  else:
   report.append({'code':code,'status':'개별 재작성 대기'});continue
  entry=goal_entries[code]
  complete=['### 전체 하위 목표와 과제별 진단','',
   '아래는 공식 문구와 적용 범위를 포함한 전체 목표다. 앞의 대표 과제와 함께 읽는다. '
   '[전체 목표 원장](../docs/하위목표과제별위계.md#'+code+') · '
   '[공식 내용 체계 대응](../docs/공식내용체계대응표.md)','',entry['scope']]
  for g in entry['goals']:
   complete+=['','#### '+g['title'],'','확인할 수행: '+g['success']]
   for cid in g['case_ids']:
    c=by_case[cid]
    complete+=['','**과제** '+c['task'],'','적용 조건: '+' / '.join(c['shared_conditions'])]
    for route in c['routes']:
     complete+=['','**'+route['title']+'**','',prose(route['steps']),'','결과: '+route['result'],
      '','진단: '+route['diagnostic']['question'],'','기대 설명: '+route['diagnostic']['expected']]
  sections[2]['body']+='\n\n'+'\n'.join(complete)
  for mapping in activity_extensions.get(code,[]):
   ex=mapping['observation_extension']
   sections[8]['body']+='\n\n### 공식 내용 체계에 따른 보완 관찰\n\n내용 요소: '+mapping['source_text']+'\n\n보완 이유: '+mapping['rationale']+'\n\n발문: '+ex['question']+'\n\n기대 설명과 관찰: '+ex['expected']+'\n\n관찰 설계 초안이다. 실제 학생의 반응·선택·수정 기록으로 판단하며 계산 정답만으로 태도나 흥미를 판정하지 않는다.'
  literature_notes=notes_for(code,literature)
  if literature_notes:sections[11]['body']+='\n\n'+literature_notes
  for source in literature['sources'].values():
   for probe in source.get('observations',[]):
    if code in probe['standard_codes']:
     sections[8]['body']+='\n\n### 문헌을 참고한 추가 관찰 '+probe['id']+'\n\n발문: '+probe['question']+'\n\n기대 설명: '+probe['expected']+'\n\n해석 범위: '+probe['interpretation']
  a['sections']=sections;a['schemaVersion']=2;a['internalRelationCount']=len(internal)
  a['markdown']='# '+a['title']+' 상세 분석 초안\n\n'+a['idea']+'\n\n'+'\n\n'.join('## '+sec['title']+'\n\n'+sec['body'] for sec in sections)+'\n'
  (ROOT/f'analyses/{code}.md').write_text(a['markdown'],encoding='utf-8')
  report.append({'code':code,'status':'초기 상세 보존' if code in PILOTS else '개별 보강 초안','internalRelations':len(internal),'independentReview':False,'studentValidated':False})
 result={'schemaVersion':2,'standards':len(by),'individually_revised':len([c for c in revisions if c not in PILOTS]),'initial_preserved':3,'entries':report}
 (ROOT/'data/revision_coverage.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'data/revised_relations.json').write_text(json.dumps({'relations':enriched},ensure_ascii=False,indent=2),encoding='utf-8')
 return enriched

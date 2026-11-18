"""Preserve official table blocks and link their scope to authored tasks.

Scope references are explicit, not claims that every task realizes every value.
"""
import hashlib,json,re
from pathlib import Path
import pdfplumber
ROOT=Path(__file__).resolve().parents[1]
TABLES=[(13,'수학','수와 연산'),(14,'수학','변화와 관계'),(15,'수학','도형과 측정'),(16,'수학','자료와 가능성'),
 (65,'공통수학1',None),(70,'공통수학2',None),(84,'기본수학1',None),(89,'기본수학2',None),
 (105,'대수',None),(119,'미적분Ⅰ',None),(133,'확률과 통계',None),(149,'미적분Ⅱ',None),
 (163,'기하',None),(177,'경제 수학',None),(191,'인공지능 수학',None),(206,'직무 수학',None),
 (223,'수학과 문화',None),(238,'실용 통계',None),(252,'수학과제 탐구',None)]

def split_bullets(raw):
 # Only a marker at the start of a visual text line starts an item. The same
 # glyph inside a phrase (e.g. 토의⋅토론) is part of its original wording.
 return [' '.join(part.split()) for part in re.split(r'(?:^|\n)\s*[⋅•]',raw)[1:] if part.strip()]

def build():
 standards=json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']
 from goal_hierarchy import load_goal_hierarchies
 entries,cases,goals=load_goal_hierarchies(standards)
 correction_path=ROOT/'data/curriculum_text_corrections.json'
 corrections=json.loads(correction_path.read_text(encoding='utf-8'))['corrections'] if correction_path.exists() else []
 pdf=pdfplumber.open(ROOT/'[별책8] 수학과 교육과정.pdf')
 blocks=[];items=[];pages={};lines=['# 공식 내용 체계와 성취기준 대응표','','공식 표 19개의 네 범주를 원문 블록으로 보존한다. 연결 목록은 과목·영역의 적용 범위이며 각 과제의 내용 충족 판정과 구별한다. 과정·기능과 가치·태도는 아래 관찰 설계로 과제에 적용하며 실제 학생 관찰은 별도 기록한다.','']
 for n,subject,domain in TABLES:
  page=pdf.pages[n-1];table=page.find_tables()[0];rows=table.rows
  # Dotted/merged cells do not yield reliable extract_tables contents. Read
  # the entire horizontal band, including all columns missed by cell detection.
  selected=[rows[0],rows[4] if n<=16 else rows[2],rows[-2],rows[-1]]
  scope=[s['code'] for s in standards if s['subject']==subject and (not domain or s['domain']==domain)]
  assert scope,(subject,domain)
  lines+=['## '+subject+(' '+domain if domain else ''),'',f'교육과정 PDF {n}쪽.','']
  for cat,row in zip(['핵심 아이디어','지식·이해','과정·기능','가치·태도'],selected):
   box=(table.bbox[0],row.bbox[1],table.bbox[2],row.bbox[3])
   text=page.crop(box).extract_text(x_tolerance=1.5,y_tolerance=3)
   assert text and '⋅' in text,(n,cat,text)
   bid=f'CT-{n:03d}-{len(blocks)%4+1}'
   links=[dict(code=code,goal_ids=[g['id'] for g in entries[code]['goals']],case_ids=[c['id'] for c in cases if c['standard']==code]) for code in scope]
   observation={'핵심 아이디어':'각 과제 풀이에서 다른 사례에도 유지되는 관계와 추가로 필요한 조건을 말하고, 범위를 바꾼 예 또는 반례를 제시한다.',
    '지식·이해':'연결된 하위 목표의 수행과 과제별 기대 설명을 확인하고 정의·대상·수 범위를 바꾸었을 때의 차이를 설명한다.',
    '과정·기능':'과제의 단계별 설명과 표현 전환을 기록하고, 방법 선택 이유와 결과 확인 방법을 설명한다.',
    '가치·태도':'과제를 해결한 뒤 방법의 쓸모와 한계를 설명하고, 다른 풀이의 근거를 검토해 자신의 설명을 수정한 이유를 기록한다. 계산 성공만으로 태도를 판정하지 않는다.'}[cat]
   blocks.append(dict(id=bid,subject=subject,domain=domain,category=cat,pdf_page=n,bbox=list(box),source_text=text,
    mapping_kind='official_subject_domain_scope',links=links,observation_design=observation,
    semantic_item_mapping_status='requires_item_level_review',student_observations=[]))
   content_left=rows[3].cells[1][0] if n<=16 else rows[2].cells[1][2]
   regions=[((content_left,box[1],box[2],box[3]),scope)]
   if n<=16 and cat=='지식·이해':
    regions=[]
    for col,band in zip(rows[3].cells[1:],['1~2학년','3~4학년','5~6학년','1~3학년']):
     scoped=[code for code in scope if band in next(s['grade_band'] for s in standards if s['code']==code)]
     if band=='1~3학년':
      # Dashed vertical rules divide the middle-school knowledge cell into
      # three columns. They are not separate official grade assignments.
      width=(col[2]-col[0])/3
      regions.extend(((col[0]+j*width,box[1],col[0]+(j+1)*width,box[3]),scoped) for j in range(3))
     else:regions.append(((col[0],box[1],col[2],box[3]),scoped))
   elif n<=16 and cat in ('과정·기능','가치·태도'):
    boundary=rows[3].cells[-1][0]
    regions=[((rows[3].cells[1][0],box[1],boundary,box[3]),[code for code in scope if next(s['school_level'] for s in standards if s['code']==code)=='초등학교']),
             ((boundary,box[1],box[2],box[3]),[code for code in scope if next(s['school_level'] for s in standards if s['code']==code)=='중학교'])]
   for region,codes in regions:
    raw=page.crop(region).extract_text(x_tolerance=1.5,y_tolerance=3)
    for bullet in split_bullets(raw):
     raw_bullet=bullet;correction=next((v for v in corrections if v['pdf_page']==n and v['raw_text']==bullet),None)
     if correction:
      assert (ROOT/correction['evidence_file']).is_file()
      bullet=correction['display_text']
     tokens=set(re.findall('[가-힣]{2,}',bullet))
     ranked=sorted(codes,key=lambda code:sum(term in (entries[code]['official_goal']+' '+entries[code]['scope']) for term in tokens),reverse=True)
     refs=ranked[:3]
     items.append(dict(id=f'{bid}-{len(items)+1}',block_id=bid,text=bullet,pdf_page=n,bbox=list(region),scope_codes=codes,
      proposed_standards=refs,proposed_goal_ids=[g['id'] for code in refs for g in entries[code]['goals']],
      mapping_status='proposal_requires_semantic_review',
      mapping_method='공식 과목·영역·학년 범위를 먼저 제한하고 문구 공통어로 검토 후보를 찾음. 선수 관계나 반영 완료를 판정하지 않음.',
      observation_prompt='다음 내용 요소를 연결된 과제에서 어떻게 사용했는지 설명하고, 설명이나 방법을 수정한 근거를 기록한다: '+bullet))
     items[-1]['source_fingerprint']=hashlib.sha256(json.dumps([bid,bullet,codes],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
     if correction:items[-1].update(source_text_raw=raw_bullet,display_correction=correction)
   lines+=['### '+bid+' '+cat,'']
   for item in (v for v in items if v['block_id']==bid):
    lines+=['- '+item['id']+' '+item['text']]
   lines+=['','관찰 설계: '+observation,'','연결 범위: '+', '.join('['+code+'](../analyses/'+code+'.md)' for code in scope),'']
 # Every goal has a source page record; comments remain identifiable as raw
 # source text rather than being marked as semantically reconciled by extraction.
 for e in entries.values():
  for n in e['source_review']['pdf_pages']:
   if str(n) not in pages:pages[str(n)]=dict(pdf_page=n,text=pdf.pages[n-1].extract_text(),goal_entries=[])
   pages[str(n)]['goal_entries'].append(e['code'])
 registry_path=ROOT/'data/curriculum_mapping_reviews.json'
 registry=json.loads(registry_path.read_text(encoding='utf-8')) if registry_path.exists() else {'reviews':{}}
 from mapping_review_author import changed_targets
 for item in items:
  review=registry['reviews'].get(item['source_fingerprint'])
  if review:
   assert review['source_text']==item['text']
   assert review['rationale'] and review['reviewer'] and review['date']
   assert set(review['standard_codes'])<=set(item['scope_codes'])
   assert all(g in goals and goals[g]['code'] in review['standard_codes'] for g in review['goal_ids'])
   item['mapping_review']=review
   changed=changed_targets(review,entries,{c['id']:c for c in cases})
   item['mapping_status']='needs_re_review' if changed else review['state']
   item['changed_cases_since_review']=changed
 data=dict(source_sha256=hashlib.sha256((ROOT/'[별책8] 수학과 교육과정.pdf').read_bytes()).hexdigest(),
  tables=len(TABLES),blocks=blocks,items=items,source_pages=list(pages.values()),
  interpretation='공식 네 범주의 원문과 적용 범위·과제 ID를 제공한다. 원문 bullet별 의미 대응 검토와 실제 태도 관찰은 추출로 완료 처리하지 않는다.')
 (ROOT/'data/curriculum_structure.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 checked=[i for i in items if i['mapping_status']=='self_checked_scope_mapping']
 lines[3:3]=['원문 블록과 세부 항목·연결 후보: [내용 체계 원장](../data/curriculum_structure.json). 세부 항목 '+str(len(items))+'개 중 의미 대응 자체 점검 '+str(len(checked))+'개. [검토 원장](../data/curriculum_mapping_reviews.json)에 이유와 과제별 내용 해시를 보존한다.','']
 lines+=['## 항목별 의미 대응 검토','']
 for item in checked:
  review=item['mapping_review']
  lines+=['### '+item['id'],'',item['text'],'','연결 기준: '+', '.join(review['standard_codes']),'','선정 이유: '+review['rationale'],'','연결 과제: '+', '.join(review['case_ids']),'']
  if review.get('observation_extension'):
   ex=review['observation_extension'];lines+=['보완 발문: '+ex['question'],'','기대 설명과 관찰: '+ex['expected'],'','새 관찰 설계이며 실제 학생 응답 검증 전이다.','']
 (ROOT/'docs/공식내용체계대응표.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(json.dumps(dict(tables=len(TABLES),blocks=len(blocks),items=len(items),self_checked_items=len(checked),pending_items=len(items)-len(checked),scope_standards=len({l['code'] for b in blocks for l in b['links']}),source_pages=len(pages))))
if __name__=='__main__':build()

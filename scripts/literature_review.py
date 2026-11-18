"""Read scoped literature evidence without turning it into student validation."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def digest(value):
 return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def read(root,path):return json.loads((root/path).read_text(encoding='utf-8'))

def target_value(target,root=ROOT):
 kind,key=target.split(':',1)
 if kind=='relation':return next(v for v in read(root,'data/relations.json')['relations'] if v['id']==key)
 if kind=='family':return read(root,'data/analysis_details.json')['families'][key]
 if kind=='initial':
  return dict(file='initial_case_studies.json',body=read(root,'data/initial_case_studies.json')[key])
 if kind=='revision':
  found=[(p.name,json.loads(p.read_text(encoding='utf-8'))[key]) for p in sorted((root/'data').glob('revisions_*.json')) if key in json.loads(p.read_text(encoding='utf-8'))]
  assert len(found)==1,'Revision target must have one authored source: '+key
  return dict(file=found[0][0],revision=found[0][1])
 if kind=='pilot':
  for group in read(root,'data/hierarchy_pilot.json')['maps']:
   for claim in group['claims']:
    if claim['id']==key:
     return dict(task=group['task'],claim=claim,nodes=[n for n in group['nodes'] if n['id'] in [claim['source'],claim['target']]],routes=[r for r in group['routes'] if r['id'] in claim['routes']])
 raise KeyError(target)

def load_registry(root=ROOT):
 path=root/'data/literature_claim_reviews.json'
 if not path.exists():return dict(schema_version=1,sources={},claims=[])
 data=read(root,'data/literature_claim_reviews.json');sources={s['id']:s for s in read(root,'data/sources.json')}
 assert len({c['id'] for c in data['claims']})==len(data['claims'])
 for sid,review in data['sources'].items():
  assert sid in sources and review['source_id']==sid
  assert digest(sources[sid])==review['bibliography_snapshot'],'Changed bibliography needs explicit literature re-review: '+sid
  assert review['reviewer'] and review['date'] and review['read_scope'] and review['limits']
  assert review['independent_review'] is False and review['student_validated'] is False
  file=root/review['snapshot_file'];assert file.is_file(),str(file)
  assert file.resolve().is_relative_to((root/'data/literature_evidence').resolve())
  assert hashlib.sha256(file.read_bytes()).hexdigest()==review['snapshot_sha256'],'Changed literature snapshot: '+sid
  for historical in review.get('snapshot_history',[]):
   prior=root/historical['snapshot_file']
   assert prior.resolve().is_relative_to((root/'data/literature_evidence').resolve())
   assert prior.is_file() and hashlib.sha256(prior.read_bytes()).hexdigest()==historical['snapshot_sha256'],'Changed historical literature snapshot: '+sid
   assert historical['date'] and historical['read_scope']
  kind=review.get('snapshot_kind','source_pdf')
  assert kind in ['source_pdf','authored_review_notes']
  if 'reading_extension' in review:
   assert kind=='source_pdf','A PDF reading extension retains its licensed primary source'
   extension=review['reading_extension'];path=root/extension['file']
   assert path.resolve().is_relative_to((root/'data/literature_evidence').resolve()) and path.suffix=='.json'
   assert hashlib.sha256(path.read_bytes()).hexdigest()==extension['sha256'],'Changed literature reading extension: '+sid
   notes=json.loads(path.read_text(encoding='utf-8'))
   assert notes['source_id']==sid and notes['source_pdf_sha256']==review['snapshot_sha256']
   assert notes['cumulative_read_scope']==review['read_scope'],'Changed cumulative reading scope: '+sid
   assert notes['cumulative_text_pdf_pages']==review['text_pdf_pages'] and notes['cumulative_visual_pdf_pages']==review['visual_pdf_pages']
   assert notes['contains_source_full_text'] is False and notes['reading_log']
  if kind=='authored_review_notes':
   assert file.suffix=='.json' and review['redistribution_license']=='workspace_authored_notes'
   notes=json.loads(file.read_text(encoding='utf-8'))
   assert notes['source_id']==sid and notes['source_url']==review['display']['url']
   asset_kind=review.get('source_asset_kind','pdf')
   assert asset_kind in ['pdf','publisher_html','web_pdf_text','author_web_text','repository_xml','repository_docx']
   if asset_kind=='pdf':
    assert notes['source_pdf_sha256']==review['source_pdf_sha256']
    assert len(notes['source_pdf_sha256'])==64
   elif asset_kind=='repository_docx':
    from docx_source_review import validate_docx_review
    validate_docx_review(review,notes)
   elif asset_kind=='repository_xml':
    assert notes['source_asset_kind']==asset_kind and notes['read_scope']==review['read_scope']
    assert notes['source_asset_sha256']==review['source_asset_sha256']
    assert re.fullmatch('[0-9a-f]{64}',notes['source_asset_sha256']),'Invalid repository XML hash'
    assert all('source_pdf_sha256' not in row for row in (notes,review)),'An XML reading is not a PDF reading'
    assert notes['original_page_layout_review'] is False and notes['pdf_read'] is False
    assert notes['source_asset_redistributed'] is False
    scope=notes['repository_xml_review']
    assert scope==review['repository_xml_review'],'Changed repository XML scope requires review'
    assert scope['url'].startswith('https://') and scope['repository'] and scope['article_identifier'] and scope['publication_doi']
    assert scope['binary_obtained'] is True and scope['content_type'] in ['application/xml','text/xml']
    elements=scope['selected_elements']
    assert elements and len({e['id'] for e in elements})==len(elements),'Duplicate or missing XML elements'
    assert all(e['id'] and re.fullmatch('[0-9a-f]{64}',e['sha256']) for e in elements),'Invalid XML element provenance'
   elif asset_kind=='web_pdf_text':
    assert notes['source_asset_kind']==asset_kind and notes['read_scope']==review['read_scope']
    scope=notes['pdf_text_review']
    assert scope==review['pdf_text_review'],'Changed web PDF text scope requires review'
    assert 'source_pdf_sha256' not in notes and 'source_pdf_sha256' not in review
    assert scope['binary_obtained'] is False and notes['original_page_layout_review'] is False
    assert scope['visual_pdf_pages']==[],'Extracted text is not a visual page review'
    count=scope['reported_pdf_pages']
    pages=scope['text_pdf_pages']
    assert type(count) is int and count>0 and pages
    assert all(type(p) is int and 1<=p<=count for p in pages) and pages==sorted(set(pages))
    ranges=scope['page_text_line_ranges']
    assert len(ranges)==len(pages)
    next_line=0
    for first,last in ranges:
     assert first==next_line and type(last) is int and last>=first
     next_line=last+1
    assert next_line==scope['text_line_count']
   elif asset_kind=='author_web_text':
    assert notes['source_asset_kind']==asset_kind and notes['read_scope']==review['read_scope']
    scope=notes['author_text_review']
    assert scope==review['author_text_review'],'Changed author text scope requires review'
    assert scope['url'].startswith('https://') and scope['uploaded_by']
    assert scope['article_pdf_obtained'] is False and notes['original_page_layout_review'] is False
    assert all(key not in record for record in (notes,review) for key in ('source_asset_sha256','source_pdf_sha256'))
    first,last=scope['article_printed_pages']
    sections=scope['selected_sections']
    assert type(first) is int and type(last) is int and 0<first<=last and sections
    assert len({item['section'] for item in sections})==len(sections)
    for item in sections:
     start,end=item['printed_pages']
     assert item['section'] and type(start) is int and type(end) is int and first<=start<=end<=last
   else:
    assert notes['source_asset_kind']==asset_kind
    asset_base=notes.get('asset_base_url',notes['source_url'])
    if 'asset_base_url' in notes or 'asset_base_url' in review:
     assert notes['asset_base_url']==review['asset_base_url'],'Changed HTML asset base requires review'
     assert asset_base.startswith('https://') and asset_base.endswith('/') and notes['source_url'].startswith(asset_base),'HTML asset base must contain the canonical source URL'
    assert notes['source_asset_sha256']==review['source_asset_sha256'] and len(notes['source_asset_sha256'])==64
    assert 'source_pdf_sha256' not in notes and 'source_pdf_sha256' not in review,'An HTML reading cannot be labelled as a PDF reading'
    assert notes['original_page_layout_review'] is False,'Primary HTML is not a PDF page-layout review'
    supplements=review.get('supplementary_pdf_read_manifest',[])
    assert supplements==notes.get('supplementary_pdf_read_manifest',[]),'Changed supplementary PDF reading manifest requires review'
    if supplements:
     assert notes['pdf_read'] is True and notes['primary_asset_is_pdf'] is False,'PDF reading must identify supplementary assets separately from primary HTML'
     assert len({a['url'] for a in supplements})==len(supplements),'Duplicate supplementary PDF URLs'
     html_urls={a['url'] for a in review['html_read_manifest']}
     for asset in supplements:
      assert asset['url'].startswith(asset_base) and asset['status']==200 and asset['content_type'].split(';')[0]=='application/pdf'
      assert re.fullmatch('[0-9a-f]{64}',asset['sha256']),'Invalid supplementary PDF hash'
      refs=asset['linked_page_urls']
      assert refs and len(refs)==len(set(refs)) and set(refs)<=html_urls,'Supplementary PDF must identify reviewed linking pages'
      assert asset['read_kind']=='linked_pdf_content_and_visual_review' and asset['redistributed'] is False,'Supplementary PDF reading does not authorize redistribution'
      count=asset['pdf_pages'];content=asset['content_pdf_pages'];visual=asset['visual_pdf_pages'];renders=asset['rendered_pages']
      assert type(count) is int and count>0 and content and visual
      assert all(type(p) is int and 1<=p<=count for p in content) and len(content)==len(set(content)),'Invalid supplementary PDF content pages'
      assert all(type(p) is int for p in visual) and len(visual)==len(set(visual)) and set(visual)<=set(content),'Invalid supplementary PDF visual pages'
      assert [a['pdf_page'] for a in renders]==visual and all(re.fullmatch('[0-9a-f]{64}',a['sha256']) for a in renders),'Supplementary PDF renders must bind reviewed visual pages'
    else:
     assert notes['pdf_read'] is False,'HTML text and embedded figures are not a PDF page-layout review'
    assert notes['source_asset_redistributed'] is False
    if 'html_read_manifest' in review:
     manifest=review['html_read_manifest']
     assert manifest==notes['html_read_manifest'],'Changed HTML reading manifest requires review'
     assert notes['read_scope']==review['read_scope'],'Changed HTML reading scope requires review'
     assert len({a['url'] for a in manifest})==len(manifest),'Duplicate HTML reading URLs'
     assert len({a['key'] for a in manifest})==len(manifest),'Duplicate HTML reading keys'
     assert all(a['url'].startswith(asset_base) and a['status']==200 and len(a['sha256'])==64 for a in manifest)
    if 'image_read_manifest' in review:
     images=review['image_read_manifest']
     assert images==notes['image_read_manifest'],'Changed image reading manifest requires review'
     assert len({a['url'] for a in images})==len(images),'Duplicate image reading URLs'
     html_urls={a['url'] for a in review['html_read_manifest']}
     for asset in images:
      assert asset['page_url'] in html_urls,'Image review must identify a reviewed HTML page'
      assert asset['url'].startswith(asset_base) and asset['status']==200 and len(asset['sha256'])==64
      assert asset['content_type'].startswith('image/') and asset['read_kind']=='inline_image_visual_review'
      assert asset['redistributed'] is False,'Image review does not authorize redistribution'
      assert len(asset['dimensions'])==2 and all(type(v) is int and v>0 for v in asset['dimensions'])
   assert notes['reading_log'] and isinstance(notes['source_corrections'],list)
   assert notes['contains_source_full_text'] is False and notes['source_pdf_redistributed'] is False
   if 'source_integrity' in review:
    assert notes['source_integrity']==review['source_integrity'],'Changed source integrity requires review'
    if review['source_integrity']['status']=='incomplete_repeated_segments':
     assert review['source_integrity']['whole_book_obtained'] is False,'Incomplete asset cannot be a whole book'
     assert notes['read_scope']==review['read_scope'] and notes['text_pdf_pages']==review['text_pdf_pages'] and notes['visual_pdf_pages']==review['visual_pdf_pages'],'Changed selected reading scope requires review'
     audit=root/notes['asset_audit_file']
     assert audit.resolve().is_relative_to((root/'data/literature_evidence').resolve())
     assert hashlib.sha256(audit.read_bytes()).hexdigest()==notes['asset_audit_sha256'],'Changed source asset audit requires review'
   if 'empirical_scope' in review:assert notes['empirical_scope']==review['empirical_scope'],'Changed empirical reading scope requires review'
 for claim in data['claims']:
  assert claim['source_id'] in data['sources']
  assert claim['role'] in ['related_theoretical_context','mathematical_explanation','empirical_result_with_scope','instructional_recommendation_with_evidence_scope']
  assert claim['locations'] and claim['support'] and claim['does_not_establish'] and claim['standard_codes']
  assert claim['independent_review'] is False and claim['student_validated'] is False
  if claim['role']=='instructional_recommendation_with_evidence_scope':
   source=data['sources'][claim['source_id']]
   assert claim['recommendations'] and claim['local_effect_tested'] is False
   for recommendation in claim['recommendations']:
    assert recommendation['evidence_rating']==source['evidence_ratings'][str(recommendation['number'])],'Changed recommendation rating requires review'
    assert recommendation['application_limit']
  if claim['role']=='empirical_result_with_scope':
   scope=claim['empirical_scope']
   source=data['sources'][claim['source_id']]
   if 'empirical_scope' in source:assert scope==source['empirical_scope'],'Changed empirical claim scope requires review'
   assert scope['design'] and scope['sample_description'] and scope['inference_limit']
   assert scope['local_effect_tested'] is False
   if scope['design']=='cross_sectional_with_selected_interviews':
    assert scope['causal_effect_established'] is False,'Cross-sectional comparisons do not establish a causal effect'
    assert scope['longitudinal_cohort'] is False,'Different grade groups are not a longitudinal cohort'
   if scope['design']=='comparative_textbook_content_analysis':
    assert scope['student_outcome_study'] is False,'Textbook content analysis is not a student outcome study'
    assert scope['causal_effect_established'] is False,'Textbook content analysis does not establish a causal effect'
  for target,old in claim['target_snapshots'].items():
   assert digest(target_value(target,root))==old,'Changed literature target needs re-review: '+target
 return data

def rating_note(claim):
 ratings=claim.get('recommendations',[])
 return (' 연결 권고의 근거 등급: '+', '.join(str(r['number'])+' '+r['evidence_rating'] for r in ratings)+'.') if ratings else ''

def empirical_note(claim):
 scope=claim.get('empirical_scope')
 return (' 연구 비교의 범위: '+scope['sample_description']+' '+scope['inference_limit']) if scope else ''

def notes_for(code,registry):
 out=[]
 for sid,source in registry['sources'].items():
  claims=[c for c in registry['claims'] if c['source_id']==sid and code in c['standard_codes']]
  if not claims:continue
  b=source['display']
  out+=['### 문헌의 실제 지원 범위','',f"[{b['title']}]({b['url']})",'',source['scope_note'],'']
  for claim in claims:
   out += [f"- {claim['id']} · 위치: {'; '.join(claim['locations'])}. {claim['support']}{rating_note(claim)}{empirical_note(claim)} 범위: {claim['does_not_establish']}"]
  out+=['','이 문헌 대응은 자체 검토다. 현재 과제의 독립 검토·학생 검증 상태를 바꾸지 않는다.','']
 return '\n'.join(out)

def build_report():
 data=load_registry();lines=['# 문헌의 읽기 범위와 주장별 근거','','교육과정 외 문헌의 실제 읽은 범위와 현재 원고에서 지원하는 주장을 연결한다. 연구의 과제·표본·분석과 자체 제작 과제의 타당성을 구별한다.','']
 for sid,source in data['sources'].items():
  b=source['display'];lines += ['## '+b['title'],'',f"[{b['authors_year']}]({b['url']}) · {source['read_scope']}",'',source['scope_note'],'',source['method_note'],'',source['limits'],'','| 대응 기록 | 원문 위치 | 지원하는 내용 | 적용 한계 |','|---|---|---|---|']
  for claim in [c for c in data['claims'] if c['source_id']==sid]:
   lines += ['| '+claim['id']+' · '+', '.join(claim['target_snapshots'])+' | '+'; '.join(claim['locations'])+' | '+claim['support']+rating_note(claim)+empirical_note(claim)+' | '+claim['does_not_establish']+' |']
  lines += ['','현재 원고에 대한 판단과 추가 관찰: '+source['editorial_action'],'']
 lines+=['[구조화 원장](../data/literature_claim_reviews.json)에 근거 파일·서지·대상 주장의 해시를 보존한다. 재배포 조건을 확인한 원문은 원문을, 그 외 출처는 직접 작성한 읽기 기록과 확인한 원문의 형식·해시·주소를 보존한다. 출판사 웹본문·저장소 XML의 지정 절 읽기와 PDF 판면 대조를 구별한다. 후자의 검사는 읽기 기록과 대응 주장의 일치 범위이며 원격 원문의 이후 변경을 실시간 확인하지 않는다. 다른 원문 버전을 사용하거나 대상 주장이 바뀌면 재검토한다.','']
 (ROOT/'docs/문헌주장별근거.md').write_text('\n'.join(lines),encoding='utf-8')
 print(json.dumps(dict(read_sources=len(data['sources']),claim_mappings=len(data['claims'])),ensure_ascii=False))
if __name__=='__main__':build_report()

"""Add named-engine layout reading while preserving the original DOCX evidence."""
import copy
from literature_review import ROOT,load_registry,build_report,digest
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,apply_literature_context
from check_anderson_displayed_counts import check,SERIES

SOURCE='ANDERSON_SHATTUCK_2012_MANUSCRIPT';DATE='2026-11-18'
CACHE=ROOT/'tmp/literature/anderson-rendered-layout-utf8-20261118'
FIRST=ROOT/'tmp/literature/anderson-rendered-layout-20261118'
DOCX=ROOT/'tmp/literature/dbr-review-originals-20261117/anderson-shattuck-repository-manuscript.docx'
PRIOR='data/literature_evidence/ANDERSON_SHATTUCK_2012_MANUSCRIPT_review_notes.json'
PRIOR_SHA='d69e30697be56700d2da25c02f135dca02f0089fe890624e92d472e2b545e5af'
PRIOR_BIB='2f1c9757538e15907d143c8b2a37b3c90da600a01ad9693d03ea318b6d0cc502'
NOTES='data/literature_evidence/ANDERSON_SHATTUCK_2012_rendered_layout_review_notes.json'
TITLE='Design-Based Research: A Decade of Progress in Education Research? — institutional submitted DOCX, complete23-page LibreOffice rendering and original chart-cache comparison'
SCOPE='기존 기관 저장소 제출 DOCX의 174본문블록·4XML부분·차트10개 XML/캐시와 삽입PNG1개의 읽기 기록을 보존한다. 원본 바이트를 바꾸지 않고 LibreOffice26.8.3.1로 변환한 23쪽의 판면을 전부 읽었다. Fig1은 검색 화면 비트맵이고, 네이티브 차트10개는 Fig2–10의9개와 Table1의막대차트1개다. 캡션과 도형이 서로 다른 쪽에 있는 경우를 대조표로 남겼다. 별도 추출문은 변환쪽6–18의13쪽을 재독했다. 출력 로그의 cp949/UTF8 해독 경고를 UTF8모드의 별도 재렌더로 해소했고,23PNG가 처음 실제로 읽은 이미지와 바이트까지 같음을 확인했다. 추가23쪽 독해나 새 PDF 출처로 중복 집계하지 않는다. 이는 해당 엔진의 로컬 판면이며 Microsoft Word의 동일 배치나 학술지16–25쪽의 출판 PDF를 확인한 것이 아니다.'
LIMITS='연도별 상위 인용 47논문의 서지·초록 중심 검토를 담은 제출 원고와 로컬 렌더링의 대조다. 새 실증 연구·학생 표본·47편 원논문/원자료를 확보하지 않았다. 원본 DOCX와 구조 읽기 기록은 그대로이며 새로 얻은 PDF는 그 파일의 파생 변환물이다. 출판 PDF·공식 부속xlsx·Word원래배치와의 동일성은 미확인이다. 해당 엔진에서 일부 원형 차트의 라벨 겹침을 관찰했지만 이를 출판본의 결함으로 단정하지 않는다. 반올림 백분율의 합계102%와 범주 중복은 서로 다른 문제다. 논문47·실증31·학과45분류·학교급55분류·결과36언급·반복34기록·검색화면118·전체검색1940은 같은 분모가 아니다. 역사적 검색 화면/검색서비스 서술을 현재 상황이나 국내 효과로 일반화하지 않고 실제 독립·학생·브라우저 시각 검증은 미완료로 둔다.'

def main():
 registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:build_report();return
 assert s['snapshot_file']==PRIOR and s['snapshot_sha256']==PRIOR_SHA and s['bibliography_snapshot']==PRIOR_BIB and sha(ROOT/PRIOR)==PRIOR_SHA
 a=load(CACHE/'acquisition.json');first=load(FIRST/'acquisition.json')
 assert a['rendering_completed'] and a['reading_completed'] and a['images_viewed'] and a['viewed_image_pages']==list(range(1,24)) and a['read_text_pages']==list(range(6,19))
 assert a['pixel_identity_to_actually_viewed_first_render'] and a['utf8_rerender_completed'] and not a['renderer_stdout_decode_warning'] and not a['source_docx_modified'] and not a['publisher_pdf_obtained']
 assert sha(DOCX)==s['source_asset_sha256']==a['source_docx_sha256'] and sha(CACHE/a['derived_pdf_file'])==a['derived_pdf_sha256']
 assert a['derived_pdf_pages']==23 and sha(FIRST/'acquisition.json')==a['first_render_acquisition_sha256']
 assert 'UnicodeDecodeError' not in (CACHE/'render.log').read_text(encoding='utf-8')
 for n,row in enumerate(a['rendered_images'],1):
  assert row['page']==n and sha(CACHE/row['file'])==row['sha256']==first['rendered_images'][n-1]['sha256']
  assert sha(FIRST/first['rendered_images'][n-1]['file'])==row['sha256']
 assert check()['status']=='pass'
 old_source=copy.deepcopy(s);old_notes=load(ROOT/PRIOR);old_claims=[copy.deepcopy(c) for c in registry['claims'] if c['source_id']==SOURCE];old_obs=copy.deepcopy(s['observations']);assert len(old_claims)==2 and len(old_obs)==5
 reviewed=load(ROOT/FILE);ids={c['id'] for c in old_claims};old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in ids];assert len(old_rows)==3
 bib=load(ROOT/'data/sources.json');entry=next(x for x in bib if x['id']==SOURCE);old_entry=copy.deepcopy(entry)
 entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review='후속 출판 PDF16–25·공식 부속xlsx·47편 원논문/원자료·Word배치 동일성과 실제 독립/학생 검증을 별도 확인한다.')
 empirical=copy.deepcopy(s['empirical_scope']);empirical['inference_limit']=LIMITS
 layout=dict(read_kind='local_named_engine_rendering_of_unchanged_repository_docx',source_docx_sha256=a['source_docx_sha256'],source_docx_modified=False,renderer_version=a['libreoffice_version'],renderer_script_sha256=a['renderer_script_sha256'],renderer_binary_sha256=a['libreoffice_executable_sha256'],renderer_package_sha256=a['runtime_package_sha256'],headless=True,ui_automation=False,derived_pdf_sha256=a['derived_pdf_sha256'],derived_pdf_pages=23,derived_pdf_is_original_journal=False,visual_rendered_pages=list(range(1,24)),selected_extracted_rendered_pages=list(range(6,19)),rendered_image_sha256={str(x['page']):x['sha256'] for x in a['rendered_images']},rendered_image_dimensions={str(x['page']):x['dimensions'] for x in a['rendered_images']},caption_chart_page_map=a['caption_chart_page_map'],all_ten_native_charts_viewed=True,embedded_screenshot_viewed=True,renderer_label_overlap_observed_pages=[10,16],published_pdf_obtained=False,publisher_binary_fidelity_verified=False,word_native_layout_fidelity_verified=False,official_supplement_workbook_obtained=False,initial_stdout_decode_warning=True,utf8_rerender_warning_resolved=True,second_render_images_identical_to_inspected_first_render=True,additional_source_pages_counted_on_rerender=0,first_render_derived_pdf_sha256=first['derived_pdf_sha256'],original_structural_docx_manifest_preserved=True,exact_displayed_counts=check(),independent_review=0,student_validation=0)
 notes=copy.deepcopy(old_notes);notes.update(date=DATE,read_scope=SCOPE,empirical_scope=empirical,previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=old_obs,previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,repository_docx_review_is_initial_structural_evidence=True,rendered_docx_followup=layout)
 notes['reading_log']+=['2026-11-18:원본DOCX불변을확인하고로컬변환23쪽을모두직접읽었다. Fig1검색화면·Fig2–10및Table1의차트10개를XML/캐시와대조했다. UTF8재렌더의23PNG는실제읽은첫23PNG와동일해추가쪽으로세지않는다. 출판PDF와Word동일배치·공식xlsx확보가아니다.']
 notes['source_corrections'] += [dict(location='Local rendered23pages,not journal16–25',issue='A formerly missing local renderer is now available. Actual23-page manuscript layout read;all10native charts andbitmap identified with caption/visual page mapping. Initial structural manifest andfailed-renderhistory retained;do not promote to publisher PDF or native Word fidelity.'),dict(location='Rendered6–8,Fig1/2',issue='Fig1shows a2011-only search with118papers,Fig2covers2000–2010with cached annual total1872,and prose reports1940search hits/47selected articles. Forced1872+118=1990does not reconcile to1940;do not silently repair historical totals or infer identical query/snapshot scopes.'),dict(location='Rendered11–17,Fig5/6/9/10',issue='Discipline45/sector55may include empirical project examples in expository papers. Iteration34count pie rounds to102%,outcome36andsector55pies to99%. Rounding totals alone do not prove/exclude duplicate original items;the source explicitly reports overlapping outcomes among31abstracts.'),dict(location='Rendered10/16',issue='Observed chart-label overlap in this named LibreOffice renderer;not evidence of a defect in the unacquired journal PDF or exact native Word layout. Kept as a rendering limitation rather than editing source figures.')]
 write(ROOT/NOTES,notes)
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])],bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,empirical_scope=empirical,method_note='기존 DOCX 구조/차트캐시 대조를 보존하고 해당 LibreOffice엔진의23판면·네이티브차트10개·비트맵1개를 읽었다. 파생 PDF/엔진 판면과 미확보 출판 PDF·Word배치 동일성을 구별한다.',editorial_action='기존2주장의범위·3과제설명과3관계근거스냅샷을재검토했다. 새출처·주장·과제·관계해석이나독립실증표본은추가하지않았다.',display={**s['display'],'title':TITLE})
 for task in s['observations']:
  if task['id']=='DBRR17-P01':
   task['question']+=' 그림1의2011년검색118건도같은분모인가?'
   task['expected']+=' 그림1은2011년만을설정한118건의화면이며,전체검색1940건·선정47편·그림2의2000–2010년연간추이를구별한다. 캐시연간합1872와118을억지로더한1990을1940의정정값으로쓰지않는다. 검색조건·시점이같다는근거없이집계를맞추지않는다.'
  elif task['id']=='DBRR17-P03':
   task['question']+=' 반복단계그림의표시백분율합계102%이면반드시중복인가?'
   task['expected']+=' 학과분류45와학교급분류55에는실증31편외해설논문속프로젝트예의정보도포함될수있다. 반복단계건수6·8·6·3·2·3·3·2·1의합은34이고,각백분율을정수로반올림하면18·24·18·9·6·9·9·6·3으로합102가된다. 반올림과범주중복은따로따지며,결과36언급/실증초록31개에서명시된중복은그대로보존한다.'
  elif task['id']=='DBRR17-P04':
   task.update(question='기관저장소의제출DOCX를LibreOffice로23쪽렌더해차트10개와삽입이미지를읽었다. 학술지16–25쪽출판PDF와Word의같은배치도확인됐는가?',expected='아니다. 원본DOCX의174본문블록·차트XML/캐시와,같은파일의해당엔진23쪽판면을구별해기록한다. 네이티브차트10개는Fig2–10과Table1이고Fig1은별도비트맵이다. 캡션과도형쪽이다른경우연결표를확인한다. Table1의n=31과본문47초록서술차이는미해결로남긴다. 원본바이트가같아도렌더러·글꼴·배치가다를수있으며출판PDF/공식xlsx/Word동일배치는미확인이다.',interpretation='원본불변과로컬판면독해완료는확인했지만파생PDF를새출판본으로세지않는다. 라벨겹침등엔진의관찰한계를남기고이전렌더실패기록도보존한다. 실제독립검토·학생검증·브라우저검증을뜻하지않는다.')
 by_id={c['id']:c for c in registry['claims']}
 for c in registry['claims']:
  if c['source_id']!=SOURCE:continue
  c['empirical_scope']=copy.deepcopy(empirical)
  c['does_not_establish']+=' 원본불변의로컬23쪽렌더를읽었지만출판PDF·공식xlsx·Word동일배치는미확인이다.'
  if c['id']=='ASR17-01':c['does_not_establish']+=' 2011년검색화면118건과2000–2010연간추이·전체검색1940건·선정47편의범위를섞어총수를임의정정하지않는다.'
  else:c['does_not_establish']+=' 45학과/55학교급분류와34단계/36결과언급을구별하고,반올림표시합102%만으로중복을추론하지않는다. 36언급/31초록의명시된범주중복을반올림으로설명해지우지않는다.'
  pages=[6,7,8] if c['id']=='ASR17-01' else [9,10,11,12,13,14,15,16,17,18]
  c['locations'] += [f'{s["repository_docx_review"]["url"]} · 로컬LibreOffice26.8.3.1렌더{p}쪽(출판쪽수아님)' for p in pages]
 for row in reviewed['records']:
  if row['claim_id'] in ids:row['claim_snapshot']=claim_snapshot(by_id[row['claim_id']],s)
 relations=load(ROOT/'data/revised_relations.json')['relations'];apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');next(x for x in queue['literature_review'] if x['source']['id']==SOURCE)['source']=entry
 write(ROOT/'data/sources.json',bib);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report()
 print('Same Anderson manuscript:23actual rendered pages/10native charts+bitmap read;2claim scopes/3task explanations/3snapshots rereviewed;no new sources,claims,tasks,contexts or independent samples')

if __name__=='__main__':main()

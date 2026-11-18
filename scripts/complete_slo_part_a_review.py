"""Complete the same SLO2013 PartA PDF reading without inflating claim/task counts."""
import copy
from literature_review import ROOT,load_registry,build_report,digest
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,apply_literature_context
SOURCE='SLO_EDR_2013_INQUIRY_SELECTED';DATE='2026-11-17';CACHE=ROOT/'tmp/literature/slo-part-a-completion-20261117'
PRIOR='data/literature_evidence/SLO_EDR_2013_method_choice_review_notes.json'
PRIOR_SHA='67c159d9b819d43a57a07f5cc66753c64122ca51dd2401cc5ad5e7f547da80e5'
PRIOR_BIB='46bcdef50f2aa6fdc8953a7f2c1c712eb409abc790700eb5af220bfc832e93f8'
NOTES='data/literature_evidence/SLO_EDR_2013_complete_part_a_review_notes.json'
SHA='952ca654a1d44ed91cd9304e7d8386b3b7bbd0d7364a61c2c60dd41600f18110'
TITLE='Educational Design Research Part A: complete206-page revised2013PDF, all seven chapters and front/back matter'
SCOPE='같은 2013년 개정 Part A 206쪽 PDF의 새 추출문 69쪽·판면 75쪽을 더해 누적 추출문 191쪽·전체 206판면을 대조했다. '+'1장 남은 본문/도식·표4·참고문헌,7장 전체의 선정 서지/전재 초록/학위논문 목록과 표지·서문·저자 소개·뒤표지를 읽고 기존2–6장 전체의 이력을 보존했다.191쪽에는 표지/서지/저자소개도 포함되며191쪽 본문을 뜻하지 않는다. 사진/색면/쪽번호 전용15쪽도 실제 판면으로 확인했다. 출판사 서지3건의 연도·학술지·권수를 대조했다.7장 선정 목록·전재 초록·URL 확인일과 원논문/링크 본문의 독해는 다르며 전수 서지 검증·원연구 전체 독해는 아니다.'
LIMITS='완료한 것은 같은SHA의 Part A206판면/191추출문 읽기다. Part B51사례·2009이전판·인용 원논문 전체/원자료·모든 서지/정오표·역사적 URL의 현재 유효성·현장 사용/학습 효과·실제 독립/학생/시각 검증은 미완료다. 개발/검증 연구와 단순 설계·이론적/통계적 일반화·여러 성과·예상/실제를 구별한다. 사례의 사이클 수·표본·품질 기준 배치를 모든 학생에게 강제하거나 서로 다른 연구의 수를 합산하지 않는다. 도식의화살표와proof of existence를 수학적 선수 사슬·보편 인과·수학적 존재 정리로 바꾸지 않는다.7장의선정편향·전재초록·당시웹확인일·저자직함을 보존하고 원논문독해나현재정보로 승격하지 않는다.'
METADATA=[
 dict(title='Design-Based Research: A Decade of Progress in Education Research?',authors='Terry Anderson; Julie Shattuck',url='https://journals.sagepub.com/doi/abs/10.3102/0013189X11428813',doi='10.3102/0013189X11428813',year=2012,journal='Educational Researcher',volume=41,issue=1,pages='16–25',source_locations=['PDF48','PDF181','PDF183'],source_value='2010',corrected_field='publication_year',scope='Publisher metadata page read; original article full text and supplemental workbook not read',direct_page_access='success',checked_date=DATE),
 dict(title='Ontological Innovation and the Role of Theory in Design Experiments',authors='Andrea A. diSessa; Paul Cobb',url='https://www.tandfonline.com/doi/abs/10.1207/s15327809jls1301_4',doi='10.1207/s15327809jls1301_4',year=2004,online_date='2009-11-17',journal='Journal of the Learning Sciences',volume=13,issue=1,pages='77–103',source_locations=['PDF48','PDF174'],source_value='PDF48:Educational Researcher32(1);PDF174:JLS13(1)',corrected_field='journal_and_volume',scope='Publisher-indexed metadata and issue contents corroborate the internal discrepancy; direct article request403; original full text not read',direct_page_access='403',checked_date=DATE),
 dict(title='Developmental research as a way to an empirically based didactical structure of science',authors='P. L. Lijnse',url='https://onlinelibrary.wiley.com/doi/abs/10.1002/sce.3730790205',doi='10.1002/sce.3730790205',year=1995,journal='Science Education',volume=79,issue=2,pages='189–199',source_locations=['PDF49','PDF190'],source_value='Science Education29(2)',corrected_field='volume',scope='Publisher-indexed metadata read; direct article request403; original full text not read',direct_page_access='403',checked_date=DATE)]

def main():
 registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:
  assert sha(ROOT/NOTES)==s['snapshot_sha256'];build_report();return
 assert(s['snapshot_file'],s['snapshot_sha256'],s['bibliography_snapshot'])==(PRIOR,PRIOR_SHA,PRIOR_BIB)
 assert sha(ROOT/PRIOR)==PRIOR_SHA and sha(CACHE/'slo-design-part-a-2013.pdf')==SHA
 a=load(CACHE/'acquisition.json');old_notes=load(ROOT/PRIOR);new_text=a['candidate_new_text_pages'];new_visual=a['new_visual_pages']
 assert a['read_text_pages']==new_text and a['viewed_image_pages']==new_visual and len(new_text)==69 and len(new_visual)==75
 assert not set(new_text)&set(old_notes['selected_text_pages']) and not set(new_visual)&set(old_notes['visual_pdf_pages'])
 full_text=sorted(old_notes['selected_text_pages']+new_text);full_visual=sorted(old_notes['visual_pdf_pages']+new_visual)
 assert full_visual==list(range(1,207)) and len(full_text)==191
 excluded=sorted(set(full_visual)-set(full_text));assert excluded==[5,10,11,52,53,72,73,114,115,134,135,152,153,171,201]
 a.update(reading_completed=True,images_viewed=True,text_scope_requires_visual_confirmation=False,new_text_pages=new_text,cumulative_text_pages=191,cumulative_visual_pages=206,all_part_a_read=True,excluded_extracted_text_pages=excluded)
 write(CACHE/'acquisition.json',a)
 old_source=copy.deepcopy(s);old_claims=[copy.deepcopy(c) for c in registry['claims'] if c['source_id']==SOURCE];old_tasks=copy.deepcopy(s['observations'])
 assert len(old_claims)==39 and len(old_tasks)==57 and len(registry['claims'])==1015
 reviewed=load(ROOT/FILE);old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in {c['id'] for c in old_claims}];assert len(old_rows)==55 and len(reviewed['records'])==765
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry);entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review=LIMITS)
 notes=copy.deepcopy(old_notes)
 notes.update(date=DATE,read_scope=SCOPE,selected_text_pages=full_text,visual_pdf_pages=full_visual,rendered_page_sha256={**old_notes['rendered_page_sha256'],**{str(p):sha(CACHE/f'rendered/slo-design-part-a-2013-{p}.png') for p in new_visual}},previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=old_tasks,previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,reading_log=old_notes['reading_log']+['2026-11-17: 남은 추출문 69쪽·판면 75쪽을 읽어 같은 Part A 전체 191추출문쪽/206판면을 대조했다. 전재 초록과 원연구 본문·서지 검증을 구별하고 기존 주장/과제 수를 늘리지 않았다.'])
 notes['complete_part_a_followup']=dict(new_text_pages=new_text,new_visual_pages=new_visual,cumulative_text_pages=191,cumulative_visual_pages=206,complete_chapters=[1,2,3,4,5,6,7],prior_complete_chapters=[2,3,4,5,6],all_part_a_read=True,front_back_matter_read=True,part_b_read=False,cited_originals_read=False,all_bibliographic_records_verified=False,all_historical_urls_rechecked=False,source_errata_verified=False,earlier_2009_edition_read=False,raw_data_reanalyzed=False,local_student_validation=False,actual_implementation_verified=False,new_claims=0,new_tasks=0,new_relation_entries=0,existing_relation_snapshots_rereviewed=55)
 notes['non_text_page_classification']=dict(photograph_or_illustration_dividers=[5,11,53,73,115,135,153],solid_colour_dividers=[171,201],header_or_page_number_only=[10,52,72,114,134,152],image_only_sign_lettering=[5],note='Not all low/empty extraction pages are blank. Covers, bibliographic matter and biographies are counted among the191textpages, not as191bodypages.')
 notes['publisher_bibliographic_rechecks']=METADATA
 notes['colophon_vs_internal_dates']=dict(colophon_revision='November2013',internal_url_checked='December19,2013 at PDF179',note='Both literal dates retained; no new release or file-modification date inferred',isbn_from_back_cover='9789032923341')
 notes['source_corrections']=old_notes['source_corrections']+[
  dict(location='PDF5/10/11/52/171/201',issue='5은 글자가있는표지판사진·11은설계도사진·171은자홍색면·201은회갈색면이고10/52는머리말/쪽번호전용이다. 빈추출문을빈판면으로취급하지않는다.'),
  dict(location='PDF17–18/22/28/32–35/43–45',issue='체계적설계와연구의두산출·맥락/입력/과정/여러성과·역할/작성자편향·일반화의한계를구별한다. 이장의사례기반일반화를모든실험의모집단추론이불가능하다는보편주장으로확장하지않는다. proof of existence는수학적존재정리가아니다.'),
  dict(location='PDF39–42 Table4/Figures6–7',issue='표4의단계별표본을고유인원으로합산하지않고원연구원자료와구별한다. 그림7은회전배치/폰트기호깨짐을실제판면으로대조했다.8사이클은하나의사례이고Prototype3은To be developed이며모두실행된수업으로세지않는다.1기준/사이클을보편고정규칙으로쓰지않는다.'),
  dict(location='PDF48/174',issue='diSessa/Cobb2004는PDF48의Educational Researcher32(1)과달리PDF174와출판사색인의Journal of the Learning Sciences13(1),77–103이다. 인쇄권호2004와출판사온라인일2009-11-17을구별한다. 직접본문403·원논문전체미독을보존한다.'),
  dict(location='PDF48/181/183',issue='Anderson/Shattuck의원목록2010과출판사2012,ER41(1),16–25를구별한다. 출판사서지/초록을읽은것이며원논문전체나부속xlsx는미독이다.'),
  dict(location='PDF49/190',issue='Lijnse1995의원목록Science Education29(2)를출판사색인79(2),189–199와구별한다. 직접본문403·원논문전체미독이며출판사정오표를확보했다는주장은아니다.'),
  dict(location='PDF22/32/34/51 and PDF172–206',issue='Wademan그림4/참고목록2005와본문1995차이는대응원전미확인으로보존한다.7장선정편향·전재초록·역사적웹확인일·서지불일치를전수원논문검증으로세지않는다. 저자소개/기관설명은당시정보이며현재직함/연락처로검증하지않았다.')]
 write(ROOT/NOTES,notes)
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])],bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,method_note='같은 Part A의 전체 206판면/191추출문과 출판사 서지 3건을 대조했다. 원논문/원자료·다른 판본/Part B·실제 학생 효과는 별도다.',editorial_action='기존39주장·57과제·55관계해석의이전원장을보존하고출처범위/서지대조를갱신했다. 새주장·과제·관계기록을추가하지않았다.',display={**s['display'],'title':TITLE})
 by_claim={c['id']:c for c in registry['claims']}
 for row in reviewed['records']:
  if row['claim_id'] in {c['id'] for c in old_claims}:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 relations=load(ROOT/'data/revised_relations.json')['relations'];apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');row=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);row.update(source=entry,claim_ids=[c['id'] for c in old_claims])
 write(ROOT/'data/sources.json',bibliography);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report()
 print('Completed same PartA206-page reading;all1015claims/1153tasks/765interpretations retained;55source snapshots rereviewed')
if __name__=='__main__':main()

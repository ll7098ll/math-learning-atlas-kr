"""Continue the same scan through printed149; keep prior30/54-spread records."""
import copy
from literature_review import ROOT,load_registry,build_report,digest
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,apply_literature_context
from record_polya_classroom_method_review import SOURCE,CACHE,SHA,URL,LI,PL,RU,OU,RE
from check_polya_definition_induction_models import check
DATE='2026-11-18'
PRIOR='data/literature_evidence/POLYA_SECOND_EDITION_heuristic_followup_review_notes.json'
PRIOR_SHA='4ff1bd9791600e4e4315eeff3ffdaadc302d65889abdb27fa303a8a7bec588b1'
PRIOR_BIB='001bb98f8d4b8fbb92fb76049800031b8e2b6de0ad22fde4749f361875e031ce'
NOTES='data/literature_evidence/POLYA_SECOND_EDITION_definition_induction_review_notes.json'
TITLE='How to Solve It, second-edition course scan — complete Parts I–II and selected dictionary pp37–149; 86 PDF spreads, actual printing unverified'
SCOPE='이전30/54PDF판면의 읽기 기록과 해시를 보존하고 PDF55–86(인쇄86–149)32판면을 추가로 직접 읽어 누적86판면을 확인했다. 대부분 책 두 면 스캔이며 추출문/OCR은0쪽이다. Part III의Definition·조건/진단·추측 점검·그림·일반화·귀납/수학적 귀납법·Modern Heuristic·Notation·Pappus·Pedantry and Mastery를 이어 읽었다. Practical Problems는149첫 면만 읽었으며 PDF87–138·사전 전체·Part IV·138판면 전권의 완료가 아니다. Princeton 공식 발췌는 별도 출처다.'
LIMITS='교수 조언·수학 예제·이상화 대화의 방법론적 서술이며 새 실증 표본이나 국내 학생 효과가 아니다. 2판 저작권1957·표시 인쇄1971/1973·서문1944/1954/1956·스캔2006과 미확정 실제 인쇄연도를 구별한다. 출판사 직접 파일/동일성·다른 판본·PDF87–138·인용 원연구/정오표·실제 독립/학생 검증은 미확인이다. 방정식 수·느린 풀이/실수의 원인·정형 문제의 모든 자료 사용을 무조건 일반화하지 않는다. 유추·유한 사례와 수학적 귀납법의 기초/임의 단계 증명을 구별한다. Pappus항목은Pólya의자유로운재서술이며Heath번역/고대원문을읽은것이아니다.'
CLAIM_UPDATES={
 'POLY18-01':dict(does_not_establish='책의4부·Part II의대화 소제목과4단계는 서로 다른 구분이다. 목록을 한 번씩 채우는 절차나 언제나 해결되는 알고리즘으로 쓰지 않는다. 모든 자료 사용이라는 질문은 필수 자료와 중복 조건을 구별해 적용하며, 미사용 자료 하나만으로 풀이 오류를 단정하지 않는다.'),
 'POLY18-02':dict(does_not_establish='원문의예시/이상화대화를 실제 학생자료로 세지 않는다. 도움을 적게 준다는 조언이 지원을 숨기거나 독립 수행을 꾸며 쓰는 허가가 아니며 정답을 암시한 질문의 성공을 보편 효과로 바꾸지 않는다. 인쇄94쪽의 느림/실수를 의욕·이해 부족으로 돌리는 서술은 관찰만으로 모든 학생의 원인을 확정하는 근거가 아니다.'),
 'POLY18-03':dict(does_not_establish='인쇄16쪽의rectangular parallelogram표기는7쪽문제·Fig1·세직각변이 가리키는직육면체와대조한다. 자체좌표/미분검산은 실제 측정이나 학생자료가 아니며 교과에 없는 미분을 모든 탐구에 요구하지 않는다. 그림의 모양·정의의 이름만으로 결론을 얻지 않고 점과 직선의 거리는 수선의 길이로 명시한다.'),
 'POLY18-04':dict(support='되돌아보기에서 결과·논증·다른 풀이·변형 문제를 구분한다. 대칭·단위·특수 경우나 유한한 사례의 관찰은 추측 점검이며 일반 증명과 다르다. 수학적 귀납법은 시작값의 참과 임의의 자연수n에서n+1로 넘어가는 함의를 모두 보인다.',does_not_establish='검사 몇 개를 통과한 사실만으로 모든 경우의 증명이 되지 않는다. 증가량이 맞아도 시작값이 틀릴 수 있다. 인쇄101의엄격부등식과102의a=b제외를함께읽어 일반 비교는≥와등호조건a=b로제시하며 직사각형 특수 증명을 모든 사각형의 증명으로 바꾸지 않는다. 자체 틀린 식은Pólya의식·실제학생오답이아니다.'),
 'POLYH18-01':dict(does_not_establish='서로 풀 수 있는 두 문제가 같은 미지수나 일대일 대응을 가져야 하는 것은 아니다. 원문 사차식의 x=±2,±3과 인쇄144–145의 지수식에서 y=2^x>0,z=y+1/y≥2 및 네 원래 해를 복원하는 규칙을 구별한다. Pappus재서술의역변환가능성문구는저자가추가했다고147쪽에서밝힌다. 임시 가정·보조정리는 최종 증명 의무를 없애지 않는다. 자체 근호/직육면체 예는 실제 학생 오답이 아니다.')}

def p(n,codes,q,e,i):return dict(id=f'POLYDI18-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS=[
 p(1,[LI,RU],'초점F=(0,1),준선d:y=−1이다. R=(2,0),Q=(0,−1)에서RF=RQ이므로R이포물선위라는설명이맞는가?','아니다. Q는준선위이지만수선의발이아니다. 수선의발H=(2,−1)에대해RH=1이고RF=√5다. RF=RQ=√5는임의의준선위점과의거리일뿐이므로정의의점–직선거리조건을만족하지않는다.','인쇄85–92의정의로돌아가기·Fig17을바탕으로만든자체좌표반례다. 초점은준선밖의같은평면에두고 수선의발/직각을명시한다. 원문그림의실측·실제학생자료·이차곡선판별식접선과제가아니다.'),
 p(2,[PL,RU],'서로수직인모서리3,4,12를모두받았다. 밑면넓이풀이에서12를사용하지않으면틀린가? 공간대각선은어떤가?','밑면을3과4의변으로정했다면넓이는12이며높이12는불필요한추가자료다. 공간대각선은세길이와직각조건을써서13이다.5만구하면밑면대각선이므로원래질문에답하지못한다. 무엇을구하는지와필수/중복자료를먼저나눈다.','인쇄95–98은모든자료사용의적용한계를명시한다. 미사용기호의유무만으로오류를판정하지않으며 가상풀이의실수/느림을학생의의욕부족으로확정하지않는다.'),
 p(3,[OU,RE],'양의변a,b인직사각형과같은둘레의정사각형은항상넓이가엄격히더큰가? 이비교로모든사각형의최대넓이를증명한것인가?','정사각형넓이((a+b)/2)²와ab의차이는(a−b)²/4≥0이다. a=b일때같고a≠b일때만엄격히크다. 둘레12에서3×3은같은9,2×4는8<9다. 이논증의범위는직사각형이며모든사각형의최대넓이를증명한것은아니다.','원문101의>와102의a=b제외·일반문제미해결설명을함께대조한자체과제다. 문맥의등호조건을명시하는일을공식정오표·모든판본의오류확인으로바꾸지않는다.'),
 p(4,[RU,OU,RE],'귀납법을배운경우:처음여섯세제곱합이F(n)=[n(n+1)/2]²와맞으면모든자연수에대한증명인가?','아니다. 기초F(1)=1과임의의자연수n에대한F(n+1)−F(n)=(n+1)³을보여합의정의를통해수학적귀납법을적용한다. 자체후보G(n)=F(n)+∏(n−k),k=1,…,6은처음여섯값만맞고n=7에서1504로실제합784와다르다. F(n)+1은같은증가량을가져도시작값이틀리므로단계만으로증명되지않는다.','인쇄114–121의관찰에의한귀납과수학적귀납법을구별한다. 정확다항식계수항등식과시작값은일반논증을검산하고유한대입몇개를증명으로세지않는다. 가짜후보식은작성자의것이며모든학생에게귀납법을요구하지않는다.'),
 p(5,[LI,RU,OU],'인쇄144–145의8(4^x+4^(−x))−54(2^x+2^(−x))+101=0을y=2^x,z=y+1/y로바꾸었다. z만구하면끝인가?','실수x에서y>0,z≥2다.8z²−54z+85=0은z=5/2,17/4를주며,각각y=2,1/2와4,1/4를복원해x=1,−1,2,−2를얻는다. 원래식·양의y·두치환의되돌림을확인한다.','원문수학예제를다시계산한자체과제다. Pappus항목은Pólya의재서술이며역변환가능성문구는저자의삽입이다. Heath1908번역·고대원문을읽었거나임시가정만으로증명한것으로기록하지않는다.')]
UPDATED_OBSERVATIONS={
 'POLY18-P02':dict(interpretation='문구만으로언제나좋은/나쁜질문을판정하지않는다. 실수·느린풀이만으로의욕이나이해부족을확정하지않고실제풀이·질문·지원뒤변화를확인한다. 가상비교이며실제학생응답·독립검토가아니다.'),
 'POLY18-P08':dict(expected='최초30판면과후속24판면으로누적54를읽은기록은각각보존한다. 이후PDF55–86의32판면을더해현재누적86판면이며사전의Pappus·Pedantry and Mastery까지와Practical Problems149첫면을읽었다.2판저작권1957·표시인쇄1971/1973·스캔2006·미확정실제인쇄연도를구별하고Princeton공식발췌와동일판본으로단정하지않는다.',interpretation='추출문/OCR은0쪽이다. 누적86판면은전권138판면·전체사전/Part IV·인용원연구·출판사직접파일동일성의완료가아니다. 이전30/54판면기록을덮어쓰지않는다. Pappus재서술을역사원문독해로세지않는다.')}
ENTRY_RANGES={'Definition':'85–92','Descartes':'92–93','Determination,Hope,Success':'93–94','Diagnosis':'94–95','Did You Use All the Data?':'95–98','Do You Know a Related Problem?':'98–99','Examine Your Guess':'99–103','Figures':'103–108','Generalization':'108–110','Have You Seen It Before?':'110','Here Is a Problem Related to Yours and Solved Before':'110–112','Heuristic':'112–113','Heuristic Reasoning':'113–114','If You Cannot Solve the Proposed Problem':'114','Induction and Mathematical Induction':'114–121',"Inventor’s Paradox":'121–122','Is It Possible to Satisfy the Condition?':'122–123','Leibniz':'123','Lemma':'123','Look at the Unknown':'123–129','Modern Heuristic':'129–134','Notation':'134–141','Pappus':'141–148','Pedantry and Mastery':'148–149'}

def main():
 registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:build_report();return
 assert s['snapshot_file']==PRIOR and s['snapshot_sha256']==PRIOR_SHA and s['bibliography_snapshot']==PRIOR_BIB and sha(ROOT/PRIOR)==PRIOR_SHA and check()['status']=='pass'
 a=load(CACHE/'definition-induction-acquisition-20261118.json');assert a['source_pdf_sha256']==SHA and a['reading_completed'] and a['images_viewed'] and a['viewed_image_pages']==list(range(55,87)) and a['new_text_pages']==[] and not a['ocr_used'] and sha(CACHE/'polya-second-edition-university-course-copy.pdf')==SHA
 old_notes=load(ROOT/PRIOR);images={str(n):sha(CACHE/f'rendered/polya-{n}.png') for n in range(1,87)};assert {k:images[k] for k in old_notes['rendered_page_sha256']}==old_notes['rendered_page_sha256']
 old_source=copy.deepcopy(s);old_claims=[copy.deepcopy(x) for x in registry['claims'] if x['source_id']==SOURCE];old_obs=copy.deepcopy(s['observations']);assert len(old_claims)==6 and len(old_obs)==12
 assert not {x['id'] for x in OBSERVATIONS}&{x['id'] for v in registry['sources'].values() for x in v.get('observations',[])}
 reviewed=load(ROOT/FILE);ids={c['id'] for c in old_claims};old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in ids];assert len(old_rows)==28
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry);entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review=LIMITS)
 empirical=copy.deepcopy(s['empirical_scope']);empirical['inference_limit']=LIMITS
 detail=copy.deepcopy(old_notes['classroom_method_scan_review']);detail.update(selected_pdf_pages=list(range(1,87)),part_iii_selected_printed_pages='37–149',definition_first_page_only=None,practical_problems_first_page_only=149,remaining_pdf_pages_without_visual_review=list(range(87,139)),source_figures_viewed=list(range(1,19)))
 notes=copy.deepcopy(old_notes);notes.update(date=DATE,read_scope=SCOPE,visual_pdf_pages=list(range(1,87)),rendered_page_sha256=images,empirical_scope=empirical,previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=old_obs,previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,classroom_method_scan_review=detail,
  reading_log=old_notes['reading_log']+['2026-11-18:PDF55–86의32판면을직접읽었다. 인쇄86–149,누적86PDF판면,추출문/OCR0쪽.'],
  definition_induction_followup=dict(new_visual_pages=list(range(55,87)),new_text_pages=[],ocr_used=False,cumulative_visual_pages=86,printed_pages='86–149',complete_entry_printed_ranges=ENTRY_RANGES,practical_problems_first_page_only=149,part_iii_complete=False,part_iv_read=False,whole_book_read=False,new_claims=0,new_tasks=5,new_relation_entries=0,rereviewed_prior_claims=6,rereviewed_prior_tasks=2,rereviewed_prior_relation_snapshots=28,historical_originals_read=False,actual_independent_review=0,actual_student_validation=0))
 notes['source_corrections'] += [dict(location='printed85–92,Definition/Fig17',issue='Use the perpendicular point-to-line distance, not distance to an arbitrary point of the directrix. Own coordinates are a counterexample, not measured source/learner data.'),dict(location='printed94–98,Determination/Diagnosis/Data',issue='Do not infer lack of will/understanding from slowness or errors alone. All-data advice is limited by essential versus redundant conditions, explicitly discussed on97–98.'),dict(location='printed101–102,Examine Your Guess',issue='Read strict > together with the following a=b exception. General rectangle comparison is >= with equality iff a=b; the text explicitly has not yet solved the all-quadrilateral problem. Not an official erratum/all-edition claim.'),dict(location='printed108–109,Generalization',issue='A line and a center determine a unique plane only when the center is not on the line. If the center is on it, many planes through that line bisect the centrally symmetric solid; existence does not establish uniqueness.'),dict(location='printed114–121,Induction',issue='A finite table suggests a conjecture; induction needs a valid base and an arbitrary-n implication. Exact coefficient identity checks the step; own offset/product counterexamples are not source errors or student records.'),dict(location='printed141–148,Pappus',issue='Author explicitly labels this a free paraphrase, with modern symbols and a convertible-derivation proviso interpolated by him. Heath translation/Greek originals remain unread. Temporary assumptions/lemmas require final justification.'),dict(location='printed92,99,145–146,historical narratives',issue='Dated cultural/personality generalizations and imagined characters are not adopted as current empirical anthropology, learner diagnosis or a participant sample.')]
 write(ROOT/NOTES,notes)
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])],bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,empirical_scope=empirical,method_note='동일PDF의추가32판면을직접읽었다. 누적86판면·추출문/OCR0쪽이며전권완료가아니다.',editorial_action='기존6주장의범위/한계·2과제설명·28관계근거스냅샷을다시대조하고원기록을보존했다. 자체과제5개를더하며새주장/관계해석은추가하지않았다.',display={**s['display'],'title':TITLE})
 for obs in s['observations']:
  if obs['id'] in UPDATED_OBSERVATIONS:obs.update(UPDATED_OBSERVATIONS[obs['id']])
 s['observations']+=copy.deepcopy(OBSERVATIONS)
 by_claim={c['id']:c for c in registry['claims']}
 for cid in ids:
  claim=by_claim[cid];claim['empirical_scope']=copy.deepcopy(empirical)
  if cid in CLAIM_UPDATES:claim.update(CLAIM_UPDATES[cid])
  additions={'POLY18-01':[59,60,73,86],'POLY18-02':[59],'POLY18-03':[55,56,65],'POLY18-04':[62,63,69,70,71,72],'POLYH18-01':[83,84,85],'POLYH18-02':[60,73]}[cid]
  claim['locations']=list(dict.fromkeys(claim['locations']+[f'{URL}#page={n}' for n in additions]))
 for row in reviewed['records']:
  if row['claim_id'] in ids:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 relations=load(ROOT/'data/revised_relations.json')['relations'];apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');row=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);row.update(source=entry,claim_ids=[x['id'] for x in registry['claims'] if x['source_id']==SOURCE])
 write(ROOT/'data/sources.json',bibliography);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report()
 print('Same scan:32new visual spreads/86cumulative;6claims/2task explanations/28snapshots rereviewed,5own tasks added; no new claims or relation entries')

if __name__=='__main__':main()

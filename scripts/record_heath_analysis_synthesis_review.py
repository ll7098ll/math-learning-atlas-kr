"""Record a bounded visual reading of Heath's cited commentary, not Greek Pappus."""
from record_scoped_pdf_research import record
from literature_review import ROOT
from extend_lt2_length_assets_review import load
from check_heath_analysis_models import check

SOURCE='HEATH_1908_ANALYSIS_SYNTHESIS';DATE='2026-11-18'
CACHE=ROOT/'tmp/literature/heath-pappus-original-20261118'
SHA='511495a96bbedc77fd376b0454a72128e5c5e4d8a592a95cac4250141fc56d85'
URL='https://www.wilbourhall.org/pdfs/heath_euclid_i.pdf'
PAGES=list(range(5,17))+list(range(154,165))
LI='12수과02-01';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
SCOPE='Heath 번역·해설 원론 제1권의 Google 도서관 스캔449PDF판면 중23판면을 직접 보았다. 앞부분PDF5–16의12판면에는 빈 면5개와 그리스어 필사본 도판1개가 포함된다. 영어 본문은PDF154–164/인쇄133–143의11쪽이며 분석·종합 절 전체137–142,그 안의 Pappus 영어 인용138–139와 Heath 해설139–142를 읽었다. 인쇄133–136의 앞 문맥과143의정의절첫쪽은 경계 읽기다. 표제면PDF6의1908·번역/해설T.L.Heath·Cambridge출판을 확인했으나 실제 사본의 인쇄/재인쇄 시점은 확정하지 않는다. 추출문·OCR 읽기는0쪽이며 그리스어 도판의 글을 번역해 읽지는 않았다.'
LIMIT='역사적 번역·수학 해설과 자체 반례의 대조다. 새 실증 표본·국내 학생 효과·실제 독립/학생 검증을 확보하지 않았다.449판면 전권/Books I–II 전체·그리스어 Pappus Collection VII634–636·각주가 인용한 Hankel/Zeuthen/Proclus/Aristotle/Tannery/Geminus/Euclid Data의 원문 전체를 읽은 것은 아니다. 제3자 호스트의 도서관 스캔이며 출판사 직접 바이너리/실제 인쇄·다른 판본 동일성·외부/후대 정오표 전체는 미확인이다. 부착 정오표PDF16의항목을읽었지만모든판본오류확인으로일반화하지않는다.'
SPECS={SOURCE:dict(stem='heath-euclid-volume1-1908-google-scan',render_stem='heath',sha256=SHA,total=449,pages=PAGES,text_pages=[],visuals=PAGES,pdf_url=URL,url=URL,year=1908,title="The Thirteen Books of Euclid's Elements, Volume I — selected introduction pp.133–143, complete Analysis and Synthesis pp.137–142; title-page year1908, actual printing unverified",authors=['T. L. Heath'],scope=SCOPE,limit=LIMIT,design='역사적 번역·수학 해설의 선정 범위를 원래 스캔 판면으로 대조',sample='Pappus의 영어 인용과 Heath 해설이며 실증 참여자 수·효과크기를 보고하는 학생 연구가 아니다.',student_outcome_study=False,supports=['분석에서 종합으로 돌아가는 논리 조건','참인 결과와 가정의 참의 구분','원 위의 각의 역명제·같은 호·밑변 끝점 조건'],next_review='그리스어 Pappus 원문과 나머지 각주 원전·판본/정오표를 별도 대조하고 자체 과제의 실제 응답과 독립 검토는 따로 확보한다.')}
CLAIMS=[
 (SOURCE,'HEATH18-01',[LI,PL,RU],[159,160,161,162,163],'목표 명제A를 가정해 알려진 결과K를 얻는 분석에서,A⇒K와K의참만으로A를증명할수없다. 되돌리는각단계의조건을확인하거나별도의종합에서원래조건을만족함을증명한다. 반면A⇒K인데K가거짓이면대우로A를반박할수있다.','Pappus 영어 인용과 Heath의해설을구별한다. 무조건 역으로 되돌릴 수 있어야 한다는 조건은Heath 인쇄139쪽에도명시돼있어이를Pólya의새발명으로단정하지않는다. 이역사해설을실제학생의성공/실패자료나현대의모든문제에적용되는알고리즘으로쓰지않는다.'),
 (SOURCE,'HEATH18-02',[LI,RU,OU,RE],[160],'Heath 인쇄139쪽의원위각역명제설명에서는원이밑변의두끝점을지나고꼭짓점이같은호/밑변의같은쪽에있다는조건을함께확인한다. 같은원이라는조건만남기거나0일수있는식으로양변을곱한뒤역으로약분하면원래명제와의동치를잃을수있다.','동일한원·같은쪽조건을따로빠뜨린자체좌표반례를원문도형의실측이나학생오답으로표시하지않는다. 해설의역사적given/구성가능성을모든현대의수치자료와동일시하지않고그리스어Pappus/Euclid Data전체독해로승격하지않는다.')]

def task(n,codes,q,e,i):return dict(id=f'HEATH18-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS={SOURCE:[
 task(1,[LI,PL,RU],'원래방정식x=2의양변에x−1을곱하면(x−1)(x−2)=0이다. x=1도원래문제의답인가? 참인결과를얻으면처음가정도참인가?','변형식의후보는1,2이지만원래식에는2만맞는다. x=1에서는0=0이되어정보를잃는다. x−1로약분하려면x≠1을확인해야한다. A⇒K와K참은A참을보장하지않고,A⇒K와K거짓은A거짓을보장한다. 후보를원래식에대입하고역방향추론조건을설명한다.','자체논리·대수예다. 정수표본검사와4행진리표를구별하고방정식의후보도인수분해로설명한다. 실제학생오답·학습효과나모든역사예제의독립증명이아니다.'),
 task(2,[LI,RU,OU],'A=(−1,0),B=(1,0),P=(0,3),Q=(0,−1/3)은중심(0,4/3),반지름5/3인같은원위에있다. ∠APB와∠AQB는같은가?','네점은중심까지거리제곱25/9로같은원위에있지만P,Q는AB의반대쪽이다. 각의코사인은각각4/5,−4/5로서로다르고두각은보각이다. 같은호/밑변의같은쪽이라는조건이필요하다.','원의밑변끝점조건은만족시킨채호조건만뺀자체반례다. 그림모양이나동일원이라는말만으로각의같음을확정하지않는다.'),
 task(3,[LI,RU,OU,RE],'A=(−1,0),B=(1,0),P=(0,2),R=(6/5,8/5)라하자. P,R은원x²+y²=4위이며모두AB위쪽이다. 두꼭짓점의각은같은가?','A,B는이원위에없다. 두각의코사인은양수지만제곱이각각9/25,225/481로다르다. 같은원·같은쪽만으로충분하지않으며그원이밑변의두끝점도지나야한다.','같은쪽조건을유지하고밑변끝점의원위조건만뺀자체좌표반례다. 코사인제곱비교에서는부호도확인하며실제학생응답이나원문도형의실측으로세지않는다.'),
 task(4,[LI,RE],'이선정본문을읽으면Pappus그리스어원문·Heath449판면전권·Pólya의모든인용원전을읽은것인가? 역변환조건은누구의어떤글에서확인했는가?','아니다. Pappus그리스어원문,Heath의영어인용138–139,Heath의해설139–142,Pólya의자유로운재서술을구별한다. Heath139쪽에도역으로되돌릴수있어야한다는조건이있다. 이번23시각판면은영어본문11쪽과앞부분12판면이며빈면5개·그리스어도판1개를포함하고추출문/OCR은0쪽이다.','분석·종합137–142전체를읽었지만449판면전권·그리스어원문·모든각주원전·실제인쇄/출판사바이너리·후대정오표는미확인이다. 부분독해완료를전체목표완료나외부독립/학생검증으로바꾸지않는다.')
]}
DETAILS={SOURCE:dict(read_kind='visual_only_library_scan',selected_pdf_pages=PAGES,english_body_pdf_pages=list(range(154,165)),english_body_printed_pages='133–143',front_matter_pdf_pages=list(range(5,17)),blank_front_pdf_pages=[5,7,9,11,13],frontispiece_pdf_pages=[12],greek_frontispiece_text_translated=False,machine_extracted_text_pages=[],ocr_used=False,complete_analysis_synthesis_section_read=True,analysis_synthesis_printed_pages='137–142',analysis_synthesis_pdf_pages=list(range(158,164)),pappus_english_quotation_printed_pages='138–139',heath_commentary_printed_pages='139–142',definition_section_first_page_only=143,whole_section_6_read=False,whole_definition_section_read=False,whole_book_read=False,whole_available_copy_read=False,title_page_year=1908,title_page_pdf=6,actual_printing_date_verified=False,publisher_direct_pdf_obtained=False,publisher_binary_fidelity_verified=False,bound_errata_pdf_page=16,bound_errata_read=True,all_later_errata_verified=False,pappus_greek_original_read=False,cited_originals_all_read=False,polya_cross_reference_source='POLYA_SECOND_EDITION_COURSE_SCAN',convertibility_condition_already_in_heath_commentary=True,quote_commentary_paraphrase_kept_distinct=True,independent_review=0,student_validation=0,exact_own_model_check=check())}
CORRECTIONS={SOURCE:['Pappus의영어인용·Heath의해설·Pólya의자유로운재서술을구별한다. 역변환가능조건은Heath139쪽에도있으며새발명의우선권을추론하지않는다.','참인결과도달과목표명제증명을구별하고,거짓결과에의한반박과참인결과에서의역추론을나눈다.','원위의각의역명제에는밑변양끝점이그원위에있음과같은호/같은쪽조건을명시한다.0인인수와후보해의원래조건도대조한다.','23시각판면중영어본문은11쪽이며앞부분의빈면·그리스어이미지는본문/OCR쪽으로세지않는다.1908은확인한표제연도이며실제인쇄·출판사직접파일동일성은미확인이다.','부착정오표는읽었지만전권·다른판본·모든후대정오표·그리스어Pappus/각주원전전체독해를확인한것은아니다.']}
INTERPRETATIONS={}
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1','SEC_12수과03-01_C04','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'HEATH18-01']=('inference_limit','목표에서알려진결과로가는계획과실행에서각단계의역방향조건을확인하고종합으로원래조건을만족함을설명한다.','A⇒K와참인K만으로A를증명하지않는다. K가거짓일때의반박과구별하며역사해설·자체반례를학생자료나성공보장으로세지않는다.')
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1','SEC_12수과03-02_C04','HP-inquiry-presentation','SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'HEATH18-02']=('inference_limit','원위각의역명제를발표·성찰할때밑변두끝점의원위조건과같은호/같은쪽조건을각각밝히고,0인인수로잃은정보를원래조건으로대조한다.','같은원이라는조건만으로각의같음을일반화하거나영인수변형을동치로쓰지않는다. 자체좌표반례는원문도형의실측·실제학생오답·그리스어원전전체검증이아니다.')

def main():
 if SOURCE not in load(ROOT/'data/literature_claim_reviews.json')['sources']:
  a=load(CACHE/'acquisition.json')
  assert a['sha256']==SHA and a['reading_completed'] and a['images_viewed']
  assert a['read_text_pages']==[] and a['viewed_image_pages']==PAGES and not a['whole_book_read']
  assert check()['status']=='pass'
 record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='역사수학해설의분석·종합·역명제조건대조',detail_key='analysis_synthesis_commentary_review',roles={c[1]:'mathematical_explanation' for c in CLAIMS})

if __name__=='__main__':main()

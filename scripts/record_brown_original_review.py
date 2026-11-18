"""Review the complete Brown1992 scan, with outcome and fidelity limits."""
from record_scoped_pdf_research import record
from literature_review import ROOT
from extend_lt2_length_assets_review import load
from check_brown_recording_models import check

SOURCE='BROWN_1992_DESIGN_EXPERIMENTS';DATE='2026-11-18'
CACHE=ROOT/'tmp/literature/brown-original-20261118'
SHA='470fc4ef753490680e151f1ed5525e3851fe908f2c946706365dfbf0dea6334c'
URL='https://www.cs.uml.edu/ecg/projects/cricketscience/pdf/brown-1992-design-experiments.pdf'
DOI='https://www.tandfonline.com/doi/abs/10.1207/s15327809jls0202_2'
LI='12수과02-01';DE='12수과02-04';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
SCOPE='미국대학의 공개 스캔39PDF판면을 모두 직접 읽었다. PDF1–38은 인쇄141–178의 논문38쪽,PDF39는EBSCO2002저작권표시1쪽이며추출문·OCR독해는0쪽이다. Fig1–5·Table1·감사·참고문헌을 확인했다. 실험실/교실의 상호 참고,도움을 받은 수행과 유지·독립 전이,동적 평가,기록·전사 자료의 선정,지원 조건과 확산을 대조했다. 인쇄1992와말미배포표시2002를구별한다.'
LIMIT='방법론 논의와 저자 연구 프로그램의 결과·선정 사례를 포함한 사본이다. 약100명/년·3년연구,초기연구37명·미니사례6명·전사2명,연구교실약60명을서로다른기술범위로남긴다. 발언유형의비율·언급수·학생수·단원별점수는같은단위가아니다. 원자료·영상·Fig4재인용원장·Palincsar/Brown1984·Bruner/Dewey/Hawthorne원전을모두읽은것이아니고출판사직접바이너리·모든정오표도미확인이다. FCL계열의후대검토와독립표본으로중복집계하지않고국내수학효과·현재학생검증으로바꾸지않는다.'
SPECS={SOURCE:dict(stem='brown-1992-university-copy',render_stem='brown',sha256=SHA,total=39,pages=list(range(1,40)),text_pages=[],visuals=list(range(1,40)),pdf_url=URL,url=DOI,year=1992,title='Design Experiments: Theoretical and Methodological Challenges in Creating Complex Interventions in Classroom Settings — complete article, public university scan',authors=['Ann L. Brown'],scope=SCOPE,limit=LIMIT,design='방법론·자전적 연구사와 교실 프로그램의 결과/사례를 함께 서술',sample='초기인용연구37명·사례6명·전사2명과Fig4연구교실약60명은같은통합표본이아니다. 비교조건의정확한전체N·모든원자료·무작위배정/종속성은이사본만으로재구성하지않는다.',student_outcome_study=True,supports=['도움·동적평가·독립전이의구별','발언/학생/점수·그래프축의구별','자료포착과전사선정·해석한계','지원조건·실제확산의확인'])}
CLAIMS=[
 (SOURCE,'B92-01',[LI,PL,RU],[5,8,9,17,19,20,27,28,29,30,31],'문헌과 계획에서 질문·명료화·요약·예상을 이해 점검의 수단으로 참고하고,실행 기록에 준 도움·후속 질문·도움 없는 재확인을 나누어 남긴다. 학생의 현재 설명과 새 조건에서의 적용을 함께 살핀다.','질문 이름을 채우거나 도움 뒤 정답을 얻은 사실은 독립 전이·장기 유지의 증명이 아니다. 원문의 안내된 발견은 지원 금지나 교사의 특정 정답 해석을 강제하는 허가가 아니며 현재 이해를 고정된 학습 불가능 판정으로 쓰지 않는다.'),
 (SOURCE,'B92-02',[OU,RE],[14,15,16,17,18,21],'발표·성찰에서 그래프의 세로축·시작값·분모와 측정 단위를 밝혀 비교한다. 발언 유형·언급 횟수·학생 인원·개별 설명을 나누고,전체 참여자와 일부 심층 사례를 중복 합산하지 않는다.','원문의Fig2/3은발언사례의비율이며Fig3모든유형이단조롭게증가하지않는다. Fig4의단원별축시작값과집단처치가다르고Fig5는언급수다. 그림의막대길이로정확한원빈도·효과크기·개인별발달을재구성하지않는다.'),
 (SOURCE,'B92-03',[LI,RE],[22,23,33,34,35,36,37,38],'문헌의 사례와 성찰 기록을 읽을 때 무엇을 처음 포착했고 그중 무엇을 전사·선정했는지 구별한다. 성공 장면뿐 아니라 선정 이유·빠진 자료·반대 해석·분석하지 못한 부분을 남긴다.','기록이나 영상을 보존한 사실이 대표성·독립 재분석 완료를 보장하지 않는다. 한 편의 원논문 독해를 그 참고문헌·원영상·원자료 전체의 독해로 바꾸지 않으며 당시inpress를현재상태로추정하지않는다.'),
 (SOURCE,'B92-04',[DE,PL,RE],[1,2,3,27,29,31,32,33],'개발 계획과 성찰에서 작성자 환경의 작동,도움을 준 선정 현장의 사용,지원이 줄어든 다른 현장의 사용을 구별한다. 핵심 기능과 필요한 지원·훈련·조건을 밝혀 재확인할 범위를 적는다.','원문의alpha/beta/gamma는확산문제의비유이지공인제품인증이나이사이트의현장검증등급이아니다. 작동예·발표성공·호의적반응은광범위사용·지속효과의완료가아니며 전문연구의 초점을 사용자 전체 요구 축소에 쓰지 않는다.')
]
def task(n,codes,q,e,i):return dict(id=f'B92-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS={SOURCE:[
 task(1,[LI,RE],'논문이 소개한 초기 연구는 참여자37명·미니사례6명·전사2명을 서술한다. 이를45명으로 더해도 되는가?','전체37명과그중일부의심층기록을중복합산하지않는다. 6사례와2전사의겹침을모르면그둘의고유대상은6–8명범위이며두수가각각새표본이라는근거는없다. 다른단원연구의약60명과도합치지않는다.','사본의집계범위를읽는자체과제다. 원자료의실제개인명단이나국내학생37명을확보한것이아니다.'),
 task(2,[OU,RE],'자체 기록 A는100발언 중20건,B는50발언 중15건이 같은 유형이다. 비율 상승이 발언 건수 증가나 더 많은 학생의 이해를 뜻하는가?','A는20%,B는30%로비율은올랐지만해당발언은20건에서15건으로줄었다. 누가여러번말했는지모르면고유학생수나개인의변화를산출할수없다. 원논문그래프의정확한빈도를역산한예가아니다.','발언과학생·비율과빈도를구별하는자체합성자료다. 실측응답이나Brown의복원원자료가아니다.'),
 task(3,[LI,PL],'버스3대에20명씩 타는 경우와20대에3명씩 타는 경우는 총인원도 필요한 버스 수도 같은가?','총인원은3×20=20×3=60명으로같다. 버스수는3대와20대로다르며버스당인원이라는역할도바뀐다. 교환법칙의수학적같음과상황의단위·자원조건을구별한다.','Brown이재인용한Bruner의집/사람예에서착안해새로만든과제다. Bruner원전독해나실제운송계획이아니다.'),
 task(4,[RU,RE],'힌트를 준 직후3문항을 맞혔다. 다음 주 도움 없이 새로운 문제를 푸는 능력까지 확인됐는가?','도움의종류·직후조건·문항을기록하고,지연시점·새과제·도움없는수행은별도로확인한다. 직후3/3은그지원조건의결과이며지연유지·독립전이의실제자료는아직없다.','가상수행상황이다. 실제학생3명·응답3건검증으로세지않는다.'),
 task(5,[OU,RE],'자체 그래프에 점수36과72를 표시하고 세로축은12에서 시작했다. 막대 길이의 비가 점수 비와 같은가?','점수비는72/36=2이고,축12위막대길이의비는(72−12)/(36−12)=60/24=5/2이다. 표시값·축시작값과단위를읽고그림길이의비를점수비로바꾸지않는다.','비영점축의영향을계산한자체예다. 원논문의라벨없는3차원막대를숫자로판독·복원한자료가아니다.'),
 task(6,[DE,PL,RE],'작성자 환경에서만 도구가 작동하고 다른 교사의 사용 자료는 없다. 여러 현장에 널리 정착했다고 보고할 수 있는가?','작동을확인한버전·환경·지원만보고하고,다른교사의사용·필요훈련·지원축소뒤사용과지속여부는미확인으로남긴다. 원문의확산비유를검증등급이나현장인증으로쓰지않는다.','이사이트배포·자동검사통과를실제교실사용으로승격하지않는자체검토과제다.')
]}
DETAILS={SOURCE:dict(full_article_read=True,read_kind='visual_only_university_scan',pdf_pages=39,article_pdf_pages=list(range(1,39)),article_printed_pages='141–178',trailing_rights_pdf_pages=[39],trailing_rights_year=2002,source_publication_year=1992,machine_extracted_text_pages=[],ocr_used=False,numbered_figures=5,numbered_tables=1,figure_pdf_pages={'1':2,'2':14,'3':15,'4':18,'5':21},table_pdf_pages={'1':10},fig1_landscape_in_scan=True,fig2_3_unit='proportion of discourse examples/instances,not distinct students',fig3_all_categories_monotonically_increasing=False,fig4_y_axis_minima=[10,30,10],fig4_research_classrooms_approximate_n=60,fig4_all_groups_total_n_verified=False,fig4_adapted_from='Brown/Campione,in press;original chapter not read here',fig5_unit='number of mentions;not total students',source_bar_counts_digitized=False,source_raw_data_reconstructed=False,publisher_direct_pdf_obtained=False,publisher_binary_fidelity_verified=False,raw_classroom_records_read=False,cited_originals_all_read=False,all_errata_verified=False,local_independent_review=0,local_student_validation=0,exact_own_model_check=check())}
CORRECTIONS={SOURCE:['39판면중논문38쪽과말미EBSCO2002표시1쪽을나누고2002를논문출판연도로쓰지않는다.','Fig2/3발언비율·Fig4점수·Fig5언급수를구별한다. Fig3의모든범주가단조롭게증가한다고요약하지않고단원별점수축의다른시작값도보존한다.','전체37명과6미니사례·2전사를더하지않고연간약100명·연구교실약60명·3년기간도고유총표본으로더하지않는다.','Table1의대비는연속선의끝점이라는원문설명을보존하며질적/양적·전통/탐구를배타적이분법으로고정하지않는다.','직후지원수행과유지·독립전이,안내된발견과지원없는발견,성공예와다른현장의확산을구별한다.','Fig4재인용원장·Palincsar/Brown1984·Bruner/Dewey/Hawthorne원전과교실영상·원자료전체미독을보존한다.']}
INTERPRETATIONS={}
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1','SEC_12수과03-01_C04','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'B92-01']=('activity_context','계획의이해점검질문과실행의도움·후속설명·독립재확인을연결한다.','지원뒤정답·질문이름의수행은독립전이·장기유지의증거가아니다.')
for rid in ['SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'B92-02']=('activity_context','발표뒤성찰에서축·분모·단위와전체대상/일부사례를구별해결과를설명한다.','발언비율·언급수·그림의막대길이를개인학생수·개인변화·정확한원자료로바꾸지않는다.')

def main():
 if SOURCE not in load(ROOT/'data/literature_claim_reviews.json')['sources']:
  a=load(CACHE/'acquisition.json');assert a['sha256']==SHA and a['reading_completed'] and a['images_viewed']
  assert a['read_text_pages']==[] and a['viewed_image_pages']==list(range(1,40)) and not a['ocr_used']
  assert check()['status']=='pass'
 record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='교실 탐구의 도움·집계 단위·원기록·확산 원논문 대조',detail_key='complete_brown_original_review',roles={c[1]:'related_theoretical_context' for c in CLAIMS})

if __name__=='__main__':main()

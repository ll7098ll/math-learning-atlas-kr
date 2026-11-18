"""Read the full cited diSessa/Cobb paper; keep the academic-copy provenance."""
from record_scoped_pdf_research import record
from literature_review import ROOT
from extend_lt2_length_assets_review import load

SOURCE='DISESSA_COBB_2004_ORIGINAL';DATE='2026-11-17'
CACHE=ROOT/'tmp/literature/disessa-cobb-original-20261117'
SHA='853bea3473e933bfaced1423405f56c4a9382aa422514a68e0b9ee15013b0d77'
URL='https://pat-thompson.net/RUME2S19Public/files/30070.pdf'
DOI='https://www.tandfonline.com/doi/abs/10.1207/s15327809jls1301_4'
LI='12수과02-01';DE='12수과02-04';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
SCOPE='연구자의 공개 강의 자료에 실린 JSTOR 형식 사본28쪽의 추출문·판면 전체를 읽었다. PDF1은 별도 표지이고 PDF2–28은 인쇄77–103의 논문27면(본문·감사·참고문헌)이다. 두 역사적 사례에서 표현을 만들고 평가·수정하는 능력(MRC), 사회적 규범·사회수학적 규범·교실 수학 실천, 설명 이론과 설계 선택의 간격, 회고 분석·재설계·맥락 변화의 한계를 대조했다. 표지·본문·쪽수는 출판사 서지JLS13(1),2004,77–103과 부합하며 온라인일2009-11-17·사본의2013다운로드 표기·이번 확인일은 다른 날짜다. 출판사에서 직접 확보한 파일이나 무주석 동일본이라고 주장하지 않는다.'
LIMIT='이 논문은 이론 논의와 두 역사적 연구 프로그램의 사례 서술이다. 해당 논문 전체 읽기와 그 안의 인용 원연구·교실 영상/원자료·원실험의 재분석을 구별한다. 국내 학생·독립 검토·실제 도구 사용/학습 효과를 검증한 것이 아니다. MRC의 운동/공간 자료 간 차이·교사 지원·맥락을 보존하며 동일한 흥미나 보편 전이를 보장하지 않는다. 사회수학적 규범을 한 학생의 발언이나 동의 수로 확정하지 않고, 합의·유창함·표현 변경을 수학적 타당성·새 풀이·학습 향상과 구별한다. 전문 연구의 새 이론 개발을 모든 학생에게 요구하거나 원문의 연구 초점 조정을 사용자의 전체 보완 목표 축소로 바꾸지 않는다.'
SPECS={SOURCE:dict(stem='disessa-cobb-2004-course-copy',render_stem='disessa-cobb',sha256=SHA,total=28,pages=list(range(1,29)),visuals=list(range(1,29)),pdf_url=URL,url=DOI,year=2004,title='Ontological Innovation and the Role of Theory in Design Experiments — complete article, public academic course copy',authors=['Andrea A. diSessa','Paul Cobb'],scope=SCOPE,limit=LIMIT,design='이론 논의와 두 역사적 설계연구 프로그램 사례의 종합',sample='1989–1990 Boxer 표현 설계 사례와1986년부터 시작한 초등 교실 연구 프로그램을 서술한다. 통합 고유 참여자 수·통제 비교 효과크기를 제공하는 논문으로 취급하지 않는다.',student_outcome_study=False,supports=['표현 대안·목적·판단 기준','수학적 설명과 토론의 근거','회고 자료와 새 가설·맥락 변화'])}
CLAIMS=[
 (SOURCE,'DC04-01',[DE,PL],[2,5,6,7,8,9,10,24,25,26],'개발 탐구를 계획할 때 어떤 설명·가정이 어떤 설계 대안을 고르는 데 쓰였는지 밝히고, 시간·도구·역할 같은 실제 제약과 구별한다. 좋은 이론의 이름을 붙이는 일과 구체 설계 선택·실행 근거를 제시하는 일을 나눈다.','원문은 거대 이론·지향 틀·행동 틀·영역별 교수 이론을 무가치하다고 하지 않는다. 이론에서 한 가지 교수법이 자동 도출되거나 모든 학생이 새로운 이론 범주를 만들어야 한다는 근거가 아니다.'),
 (SOURCE,'DC04-02',[DE,OU,RE],[11,12,13,14,15,16,17,24,25],'표현을 만드는 것뿐 아니라 무엇을 드러내고 놓치는지 목적과 기준에 따라 비판·수정하는 활동을 구성한다. 다른 표·그림·식이 보존하는 정보와 사용 조건을 설명하고, 선택 이유를 산출물과 성찰에 남긴다.','원문의 표현 설계 능력과 운동 개념 이해는 같은 측정이 아니다. 운동에서 공간 자료로 옮길 때 흥미·어려움도 달랐다. 보기 좋은 표현·새 표기·활발한 참여를 학습 효과나 보편 전이로 바꾸지 않는다. 자체 직사각형 예는 원논문 학생 자료가 아니다.'),
 (SOURCE,'DC04-03',[OU,RE],[17,18,19,20,21,22,23],'발표와 성찰에서 무엇을 수학적으로 다른 풀이·명확한 설명·받아들일 만한 근거로 판단했는지 구체 발언·계산·수정으로 설명한다. 일반적인 대화 참여 규칙과 수학적 판단의 기준을 나누어 관찰한다.','사회수학적 규범은 교사와 학생의 반복된 상호작용에서 추론하는 설명 범주다. 한 번의 발언·손들기·동의 수로 교실 전체의 규범이나 개인의 독립적 이해를 확정하지 않는다. 합의는 조건·논증의 타당성 확인을 대신하지 않는다.'),
 (SOURCE,'DC04-04',[LI,RU,RE],[3,11,12,13,15,20,23,25,26,27,28],'문헌에서 얻은 예상과 실제 탐구 중 새로 나타난 관찰을 구별하고, 회고 분석에서 고른 자료·선정 이유·다른 설명·가설 변경을 기록한다. 이전 기록으로 새 질문을 제안하는 일과 새 조건에서 다시 확인한 일을 나눈다.','회고 분석과 우연한 발견은 새 가설의 검증 완료가 아니다. 이 논문 한 편의 독해가 참고문헌 전체·원영상·원자료의 독해가 아니며 당시 투고중/출판예정 표기를 현재 출판 상태로 추정하지 않는다. 연구 초점의 유한성을 전체 사용자 목표를 줄이는 허가로 쓰지 않는다.')]

def task(n,codes,question,expected,interpretation):return dict(id=f'DC04-P{n:02d}',standard_codes=codes,question=question,expected=expected,interpretation=interpretation,student_validated=False)
OBSERVATIONS={SOURCE:[
 task(1,[DE,OU],'둘레20의정수 입력판에서 가로x를 다시 알아내려 한다. 넓이A만 남긴 기록과(x,A)표는 같은 정보를 주는가?','A=9이면x=1과9가 모두 가능하므로 A만으로 표지가 붙은 가로x를 유일하게 복원할 수 없다. (x,A)를 함께 남긴 표는 그x를 보존한다. 두 경우의 변은(1,9),(9,1)로 순서를 바꾼 합동인 직사각형이며 서로 다른 모양을 발견한 것은 아니다. 목적이 최댓값 비교인지 가로 복원인지에 따라 표현의 적합성을 판단한다.','정수1–9의 자체 수학 모형이다. 정보 손실은 명시한 복원 목적에 관한 말이며 넓이만 적는 모든 표현이 나쁘다는 뜻이 아니다. 원논문 학생 응답을 재구성한 것이 아니다.'),
 task(2,[OU,RE],'x(10−x),10x−x²,25−(x−5)²를 썼으니 서로 다른 풀이3개를 발견했다고 할 수 있는가?','세 식은 같은 다항식이다. 전개·완전제곱 변형과 최댓값을 보이는 논증의 역할을 설명하고 어떤 의미의 다른 풀이를 세는지 기준을 먼저 밝힌다. 0<x<10에서 마지막 식으로 A≤25와같음x=5를 논증할 수 있지만 식을 다르게 적었다는 사실만으로 독립적인 해결 전략3개가 생기는 것은 아니다.','다른 표현·다른 전략·수학적 타당성의 기준을 설명하는 자체 과제다. 교실에서 합의한 분류를 보편적인 유일 분류로 고정하지 않는다.'),
 task(3,[OU,RE],'모둠이x=1,5,9의넓이9,25,9에동의했다. 모든 양의 실수 변에서 최대25라는 증명과 교실 전체의 토론 규범도 확인됐는가?','세 계산과 모둠의 동의는 그 범위만 확인한다. 전체 실수 범위에는 A=25−(x−5)²≤25와같음 조건 같은 일반 논증이 필요하다. 교실 규범을 알아보려면 여러 상호작용에서 어떤 설명을 왜 받아들이거나 수정했는지 살핀다.','동의 수·자료점 수·수학적 증명·규범 추론을 구별한다. 이 가상 상황을 실제 동료 검토·학생 응답으로 집계하지 않는다.'),
 task(4,[DE,RE],'운동을 표현하는 활동에서 참여가 활발했다면 지형 자료 표현 활동에서도 같은 흥미와 성과가 나올까?','목적·자료 구조·도구·교사 지원·참여와 이해의 근거를 다시 확인한다. 원논문은 공간 자료 표현에서도 능력이 드러났지만 같은 정도의 지속적 흥미를 보이지 않고 표현상의 어려움도 달랐다고 서술한다. 새 과제에서는 무엇을 보존하고 다시 확인할지 계획한다.','문헌 사례와 국내 실제 전이 효과는 다르다. 활동의 맥락 변화를 반복 측정의 동일 조건으로 합산하지 않는다.'),
 task(5,[RU,RE],'예상하지 못한 풀이가 한 영상에서 보였다. 나중에 그 장면을 골라 새 가설을 세웠다면 어떤 기록이 필요한가?','원래 질문·자료 수집 당시 목적·영상 선택 이유·새 관찰/가설·빠진 장면과 다른 설명을 구별한다. 회고 기록이 알려 주는 범위와 다음 과제/조건에서 실제로 재확인할 계획을 나눈다. 원문 사례에서도 영상 확보·선택과 후속 연구를 구별했다.','장면 하나를 교실 전체의 규범이나 새 가설의 확정 증거로 바꾸지 않는다. 실제 영상·학생 자료를 확보했다는 뜻이 아니며 목표 전체의 검토 의무를 삭제하지 않는다.'),
 task(6,[LI],'이 자료의2004·2009-11-17·2013다운로드·2026확인일은 모두 출판연도인가? 참고문헌까지 모두 읽은 것인가?','인쇄 권호2004,출판사온라인일2009-11-17,사본의과거다운로드표기2013,이번확인일2026을분리한다. 공개강의사본의논문27면과JSTOR표지1면을읽은것이며연결원영상·원자료·인용논문전체를읽은것은아니다.','날짜 필드·배포 경로·원논문과 인용 원연구를 구별하는 자체 문헌 과제다. 출판사 직접 파일·모든 정오표·이후 출판 현황을 검증한 것으로 쓰지 않는다.')
]}
DETAILS={SOURCE:dict(full_article_read=True,pdf_pages=28,article_pdf_pages=list(range(2,29)),wrapper_pdf_pages=[1],article_printed_pages='77–103',publisher_direct_pdf_obtained=False,publisher_issue_year=2004,publisher_online_date='2009-11-17',course_copy_download_stamp_year=2013,provenance='Public academic course copy, not a direct publisher-provided binary; copy contains red reference-margin arrows on PDF26–28',no_numbered_article_figures_or_tables=True,raw_classroom_records_read=False,cited_originals_all_read=False,actual_independent_review=0,actual_student_validation=0,prior_slo_bibliographic_recheck='The earlier SLO review recorded publisher metadata only for this article; this new source records the subsequently read complete course copy without rewriting that historical snapshot.',own_tasks_are_not_student_responses=True)}
CORRECTIONS={SOURCE:['공개 강의 사본의27논문면과JSTOR별도표지1면을구별한다. PDF26–28의빨간여백화살표는이사본의주석이며원논문도식으로세지않는다.','SLO PDF48의Educational Researcher32(1)와달리논문판면·출판사서지는JLS13(1),2004,77–103이다. 온라인일2009를인쇄연도로대체하지않는다.','표현설계능력·운동개념이해·흥미를같은결과변수로묶지않고,운동과공간자료사이의차이를보존한다.','사회적규범·사회수학적규범·교실수학실천을구별하며집단의반복된상호작용을개인총점으로바꾸지않는다. 이론적범주가교수법을세부적으로자동결정한다는주장을피한다.','당시submitted/in press·인용연구·영상·원자료는원문전체미독/현재상태미확인이다. 두서술사례의수와참여자수를더하지않는다.']}
INTERPRETATIONS={}
for rid in ['SEC_12수과02-04_C04','SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'DC04-02']=('activity_context','표현의목적·보존/손실정보·판단기준을개발산출물과발표뒤수정에연결한다.','표현의 모양·참여의 활발함·표기 변경이 실제 개념 이해·학습 효과를 보장하지 않는다. 맥락/지원이 다른 표현 활동을 같은 결과로 합치지 않는다.')
for rid in ['SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'DC04-03']=('activity_context','실제발표/토론에서무엇이다른풀이·명확한설명·수용할근거인지판단한이유와수정내용을성찰한다.','한 번의 동의·발언이나 다수결로 수학적 타당성·교실 규범·독립 이해를 확정하지 않는다. 자체 가상 대화는 실제 피드백이 아니다.')
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1']:
 INTERPRETATIONS[rid,'DC04-04']=('inference_limit','문헌의예상·실행중새관찰·회고자료의선택·새가설과재확인범위를구별해기록한다.','논문 한 편·장면 하나의 독해가 인용 원연구/원자료 전체나 새 가설 검증의 완료가 아니다. 연구 초점 조정을 사용자 전체 목표 축소로 바꾸지 않는다.')

def main():
 if SOURCE not in load(ROOT/'data/literature_claim_reviews.json')['sources']:
  a=load(CACHE/'acquisition.json');assert a['sha256']==SHA and a['reading_completed'] and a['images_viewed']
  assert a['read_text_pages']==a['viewed_image_pages']==list(range(1,29))
  from check_representation_information import check
  assert check()['status']=='pass'
 record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='표현 설계·수학적 토론·개발 탐구의 원논문 대조',detail_key='complete_original_article_review',roles={c[1]:'related_theoretical_context' for c in CLAIMS})

if __name__=='__main__':main()

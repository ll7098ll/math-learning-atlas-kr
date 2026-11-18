"""Read two cited foundational papers without treating methods as local effects."""
import logging
from record_scoped_pdf_research import record
from literature_review import ROOT
from extend_lt2_length_assets_review import load

DATE='2026-11-18';CACHE=ROOT/'tmp/literature/dbr-foundations-20261118'
COBB='COBB_ET_AL_2003_DESIGN_EXPERIMENTS';COLLINS='COLLINS_JOSEPH_BIELACZYC_2004'
LI='12수과02-01';DE='12수과02-04';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
SPECS={
 COBB:dict(stem='cobb-2003-course-copy',sha256='abd897b68879ef72f7da85c2e9e2fe142230e5cd17b76c4f1110c90bda070c2d',total=6,pages=list(range(1,7)),visuals=list(range(1,7)),pdf_url='https://pat-thompson.net/RUME2S19Public/files/29093.pdf',url='https://journals.sagepub.com/doi/10.3102/0013189X032001009',year=2003,title='Design Experiments in Educational Research — complete article, public academic course copy',authors=['Paul Cobb','Jere Confrey','Andrea diSessa','Richard Lehrer','Leona Schauble'],scope='공개 강의 사본6PDF쪽의 추출문과 판면 전체를 읽었다. PDF1은 JSTOR별도표지,PDF2–6은 인쇄9–13의 논문5쪽이다. 학습과 지원 수단의 상호작용,준비·실행·회고 분석,구성개념과 측정의 구별을 대조했다. 별도 번호 표·그림이나 독립 참고문헌 목록은 없고 본문 인용·주·저자란을 읽었다. 2013년 과거 다운로드 표기와 인쇄2003을 구별한다.',limit='연구자들의 방법론 논의이며 통합 참여자 수·통제 비교 효과크기를 제시한 새 실증 연구로 세지 않는다. 공개 강의 사본 전체 읽기는 출판사 직접 바이너리·인용 원연구 전체·현재 학생의 학습 효과 검증이 아니다. 연구 초점과 배경을 구별하라는 설명을 사용자 전체 보완 목표의 축소 허가로 쓰지 않는다.',design='설계 실험의 공통 특징·실행·회고 분석에 관한 방법론 논의',sample='다양한 연구 맥락을 예시한다. 이 논문을 하나의 새 학생 표본으로 합산하지 않는다.',student_outcome_study=False,supports=['검증 가능한 예상과 지원 수단','측정의 구성개념 타당성','회고 분석의 반대 근거·선정 이유']),
 COLLINS:dict(stem='collins-2004-public-copy',sha256='0ba91fc6fa880b1e43d8172936136048a6ffee310ed8fd69ae46ad69fceeed2d',total=29,pages=list(range(1,30)),visuals=list(range(1,30)),pdf_url='https://static1.squarespace.com/static/57309137ab48de6f423b3eec/t/59a7138d7131a56e32c47b18/1504121741402/Collins%2Bet%2Bal.%2B2004.pdf',url='https://www.tandfonline.com/doi/abs/10.1207/s15327809jls1301_2',year=2004,title='Design Research: Theoretical and Methodological Issues — complete article, public copy',authors=['Allan Collins','Diana Joseph','Katerine Bielaczyc'],scope='공개 사본29PDF쪽의 추출문·판면 전체를 읽었다. PDF1은 Taylor&Francis배포표지,PDF2–29는 인쇄15–42의 논문28쪽이며 표1(27쪽)·표2(33쪽),감사·참고문헌을 포함한다. FCL·VideoCrew두 사례의 수정 과정,참여·학습·시스템 결과,맥락·비용,형성적 수정과 고정 절차의 총괄 평가를 대조했다. 인쇄2004·온라인2009-11-17·사본 다운로드2017-08-30·이번2026확인은 다른 날짜다. 사본 업로더와 출판사 직접 바이너리 동일성은 확인하지 않았다.',limit='방법론 논의와 두 연구 프로그램 사례 서술이다. 같은 프로그램의 여러 단계·후대 검토 논문을 독립 실증 표본으로 중복 집계하지 않는다. FCL·VideoCrew의 인용 원자료·학위논문·교실 영상 전체를 읽은 것이 아니다. 독립 평가의 필요성에 관한 제안은 이 사이트가 독립 검토나 학생 검증을 받았다는 증거가 아니다. 교과 수학의 타당성·개인의 이해·집단 참여·지속 가능성을 단일 총점으로 바꾸지 않는다.',design='설계 연구의 방법론 논의와 FCL·VideoCrew두 사례의 발전 과정',sample='VideoCrew1단계33명,2단계10명,3단계다른집단을 서술한다. 중복·탈락·3단계인원 불명으로 고유 총수를 계산하지 않는다. FCL전체 참여자 수·통합 효과크기도 이 논문에서 산출하지 않는다.',student_outcome_study=False,supports=['의도한 설계와 실제 실행·단계별 수정','참여·학습·시스템 결과의 분리','형성 평가와 고정 절차·독립 총괄 평가'])
}
CLAIMS=[
 (COBB,'C03-01',[DE,PL],[2,3,4],'탐구 계획에서 현재의 수학적 이해와 목표,예상하는 변화,이를 지원할 과제·표현·상호작용을 연결한다. 무엇을 관찰하면 예상을 지지하거나 수정할지 먼저 적는다.','이론 이름이나 활동 목록만으로 구체 설계 선택·효과가 입증되지 않는다. 전문 연구의 이론 개발을 모든 학생에게 요구하거나 탐구의 모든 조건을 통제했다고 주장하지 않는다.'),
 (COBB,'C03-02',[RU,OU,RE],[4,5],'결과를 설명할 때 측정값이 어떤 이해·추론을 나타내는 지표인지 밝히고,계산·설명·표현·상황 자료를 목적에 맞게 대조한다. 점수가 정밀하거나 반복돼도 측정하려는 이해를 충분히 보여 주는지 별도로 확인한다.','정확한 기록·신뢰로운 채점·집단의 정답은 구성개념 타당성이나 개인의 독립 이해와 동일하지 않다. 식물 수관의 부피 예시는 문제 맥락이며 실제 성장의 비례 법칙을 입증한 자료가 아니다.'),
 (COBB,'C03-03',[LI,RE],[5,6],'성찰에서 처음의 예상,실행 중 변경과 이유,회고 분석에 고른 자료와 빠진 자료를 구별하고 다른 해석·반대 근거를 검토한다. 후속 확인이 필요한 조건을 명시한다.','나중에 고른 성공 장면이나 실행 중 직관적 수정만으로 일반화·원인·재현성이 확정되지 않는다. 논문 전체 독해가 본문 인용 원연구의 전체 독해나 실제 외부 검토를 대신하지 않는다.'),
 (COLLINS,'CJB04-01',[DE,PL,RU],[4,6,20,21],'의도한 계획과 실제 실행을 나누고 바뀐 과제·지원·참여 조건,변경 이유와 시점을 기록한다. 단계마다 같은 점과 달라진 점을 밝혀 결과를 해석한다.','계속 수정한 활동의 전후 차이를 한 요소만의 효과로 단정하지 않는다. 단계 변경은 실패 기록을 지우거나 사용자의 전체 요구를 줄일 이유가 아니다.'),
 (COLLINS,'CJB04-02',[OU,RE],[14,17,18,19,20,22,23,24,25],'발표와 성찰에서 참여·협력,수학적 이해·추론,필요 자원·비용·지속 가능성의 근거를 구별한다. 같은 결과값이라도 대상·지원·기간이 다르면 함께 명시한다.','흥미·활발한 토론·완성된 공동 산출물이 개인의 학습이나 이후의 독립 사용을 보장하지 않는다. 사례의33명·10명·다른집단을 단순 합산하거나 고유 표본·국내 효과로 쓰지 않는다.'),
 (COLLINS,'CJB04-03',[LI,RE],[15,21,26,27,28,29],'문헌과 성찰에서 개발 중 수정한 결과와 절차를 고정해 비교한 평가를 구별하고,누가 무엇을 어떤 자료로 판단했는지 남긴다. 성공·실패·조건과 미분석 자료를 함께 설명한다.','형성적 수정의 유연성을 총괄 비교의 절차 변경 허가로 바꾸지 않는다. 자기 점검·자동 검사·이 논문의 독해는 실제 독립 평가나 학생 검증이 아니다. 인용 원연구·당시submitted/inrevision의 현재 출판 상태도 별도 확인 사항이다.')
]
def task(prefix,n,codes,q,e,i):return dict(id=f'{prefix}-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS={COBB:[
 task('C03',1,[RU,OU],'수관을 닮은 구로 단순화해 첫 부피를1로 놓았다. 모든 길이가2배가 되면 부피도2배인가? 이 모형이 실제 식물의 시간별 성장을 증명하는가?','닮은 입체의 부피비는2³=8이다. 길이에 대한 비례와 부피에 대한 비례를 나누고,실제 수관은 닮은 구라는 가정·측정 자료·시간과 길이의 관계를 따로 확인한다.','원문의 수관 탐구 예에서 착안한 자체 수학 모형이다. 원논문 학생의 계산이나 실제 식물 측정값이 아니다.'),
 task('C03',2,[OU,RE],'4명이 낸 공동 답안이4문항 모두 정답이었다. 네 사람 모두 각 문항을 혼자 풀 수 있다고 결론 내릴 수 있는가?','공동 산출물은4/4이나 개인별 풀이 증거는 없다. 한 사람이 모두 해결했을 가능성과 각자가 설명한 경우를 구별하고,개별 설명·새 문항 등 목표에 맞는 근거를 추가로 확인한다.','집단 정답률과 개인 이해를 구별하는 가상 상황이다. 학생4명 검증이나 실제 응답4건으로 집계하지 않는다.'),
 task('C03',3,[LI,RE],'전체 기록20장 중 예상과 맞는3장만 골라 설명했다. 나머지17장이 반대 사례인지 모른다면 무엇을 보고해야 하는가?','3/20=15%는 선정 비율이며 성공률이 아니다. 선정 기준·빠진17장·다른 해석과 미분석 상태를 밝히고 전체 기록을 체계적으로 대조한다.','자체 가상 기록 수다. 17장이 모두 반례라고 단정하지 않고 미확인 상태를 보존한다.'),
 task('C03',4,[DE,PL],'“표현 활동이 좋다”는 설명으로 계획이 충분한가? 목표가 넓이 최댓값 설명일 때 예상과 확인 근거를 구체화하라.','0<x<10에서A=x(10−x)=25−(x−5)²≤25와 같음x=5를 목표 근거로 삼고,표·그림·식에서 무엇을 설명할지 계획한다. 실제 학생이 이 설명을 구성하는지는 별도 관찰한다.','수학적 증명과 수업 설계의 기대 효과를 구별하는 자체 과제다. 식의 검산을 학생 학습 검증으로 바꾸지 않는다.')
],COLLINS:[
 task('CJB04',1,[PL,RU],'1단계 뒤 설명 자료·도구·모둠 구성도 바꾸고 점수가 올랐다. 설명 자료 하나의 효과인가?','단계별 조건·변경 시점·이유·평가 도구·대상을 기록한다. 여러 요소가 동시에 바뀌었으므로 관찰된 상승만으로 어느 한 요소의 원인 효과를 분리할 수 없다.','형성적 수정 기록을 위한 가상 상황이며 실제 점수 상승 자료가 아니다.'),
 task('CJB04',2,[OU,RE],'참여가 활발하고 포스터가 완성됐다. 개인의 비례 이해와 다음 학기의 지속 사용도 확인됐는가?','참여·공동 산출물,개별 수학 설명·새 문제,후속 사용·지원 기록은 다른 근거다. 확인한 결과와 아직 확인하지 않은 결과를 각각 적는다.','참여·학습·시스템 결과를 단일 성공 점수로 합치지 않는 자체 분류 과제다.'),
 task('CJB04',3,[LI,RE],'논문의 VideoCrew1단계33명과2단계10명을 더해 고유 참여자43명이라고 써도 되는가?','겹침을 모르므로 그 두 단계의 고유 인원은33–43명 범위다. 원문은3단계가 다른 집단이라고 하지만 인원은 이 독해 범위에서 확정하지 않는다. 세 단계 전체의 정확한 고유 총수는 산출하지 않는다.','33–43은 두 유한 집합의 합집합 경계이며 실제 두 단계의 겹침을 추정한 값이 아니다. FCL 참여자와도 합치지 않는다.'),
 task('CJB04',4,[OU,RE],'장비100단위만 지출했다며 비용을 보고했다. 지원30·교체20도 필요하면 총비용과 장비의 비중은?','명시한 세 항목 합계는150단위,장비 비중은100/150=2/3이다. 인건비·기간·다른 자원이 빠졌다면150도 그 세 항목의 부분 합계로 표시한다.','원문이 강조한 지원·교체 비용 누락에서 착안한 자체 산술 예다. 실제 학교 견적·현재 가격이 아니다.'),
 task('CJB04',5,[LI,RE],'비교 평가 도중 A집단에만 추가 힌트를 줬다. 처음 고정한 절차와 같은 비교인가?','계획된 조건과 실제 지원의 차이를 기록한다. 힌트를 포함한 실행 조건의 결과를 보고하되 원래 계획대로 동일 절차를 지킨 비교라고 쓰지 않는다. 개발 과정의 수정과 고정 절차의 총괄 비교를 구별한다.','구체 연구의 윤리·효과 판정을 대신하지 않는 가상 방법론 과제다. 실제 학생에게 힌트를 준 기록이 아니다.'),
 task('CJB04',6,[LI],'인쇄2004·온라인2009·사본 다운로드2017·이번확인2026은 모두 출판연도인가? 표1의 재인용 원문도 읽었는가?','인쇄권호2004,온라인공개2009-11-17,사본다운로드2017-08-30,이번확인2026을 분리한다. 이 사본의 본문·표·참고문헌은 읽었지만 표1의Brown/Campione1996원장·영상·학위논문 전체를 읽었다고 하지 않는다.','공개 사본의 판본·배포 경로와 재인용 한계를 확인하는 자체 과제다. 사본의 오래된 조회·인용 수를 현재 지표로 쓰지 않는다.')
]}
DETAILS={COBB:dict(full_article_read=True,pdf_pages=6,article_pdf_pages=list(range(2,7)),wrapper_pdf_pages=[1],article_printed_pages='9–13',publisher_direct_pdf_obtained=False,provenance='Public academic course copy in Pat Thompson RUME2S19Public;JSTOR wrapper/access stamp2013 retained.',numbered_figures=0,numbered_tables=0,separate_reference_list_in_copy=False,raw_classroom_records_read=False,cited_originals_all_read=False,actual_independent_review=0,actual_student_validation=0),COLLINS:dict(full_article_read=True,pdf_pages=29,article_pdf_pages=list(range(2,30)),wrapper_pdf_pages=[1],article_printed_pages='15–42',publisher_direct_pdf_obtained=False,provenance='Public Squarespace-hosted article copy;SUNYdownloadstamp2017retained,uploader not independently identified.',publisher_issue_year=2004,publisher_online_date='2009-11-17',copy_download_date='2017-08-30',numbered_figures=0,numbered_tables=2,table_visual_pdf_pages=[14,20],table_printed_pages=[27,33],table1_reproduced_from='Brown/Campione1996;that original chapter not read here',table2_reporting_lines=6,body_reporting_sections=5,reporting_difference='Table2includesmultimediadocumentation;body38–39tentativelyproposesfive reporting sections. Do not force this into a rigid six-section mandate.',video_crew_phase1_participants=33,video_crew_phase2_participants=10,unique_total_participants_unknown=True,raw_classroom_records_read=False,cited_originals_all_read=False,actual_independent_review=0,actual_student_validation=0)}
CORRECTIONS={COBB:['Anderson제출원고의5–8과달리실제논문판면과출판사서지는9–13이다.이전검토기록을덮어쓰지않는다.','학습의 구성개념·측정값·정확한 채점·개인/집단의 추론을 구별한다.','연구 설계의 초점/배경 구별은 사용자 전체 목표를 줄이는 근거가 아니다.'],COLLINS:['실제 논문 머리말·배포표지와 저자 기관 서지는JLS13(1),15–42,2004이며Anderson제출원고의EducationalResearcher표기와 다르다.','표1은Brown/Campione1996재인용이며 이 논문 읽기를 그 원장 읽기로 바꾸지 않는다.','표2의보고항목6줄과본문의잠정5절을구별하고,원문의형성수정/총괄고정절차와독립평가의구별을보존한다.','FCL·VideoCrew같은프로그램의단계와검토논문을독립학생표본으로중복집계하지않는다.']}
INTERPRETATIONS={}
def add(ids,cid,role,finding,limit):
 for rid in ids:INTERPRETATIONS[rid,cid]=(role,finding,limit)
add(['SEC_12수과03-02_C04','HP-inquiry-presentation','SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection'],'C03-02','activity_context','실행자료·산출물에서무엇이수학적이해의지표인지설명하고성찰한다.','정밀한점수·공동정답·반복기록은개인의이해나구성개념타당성과동일하지않다.')
add(['SEC_12수과03-01_C04','HP-inquiry-execution'],'CJB04-01','activity_context','계획과실제개발실행·단계별변경이유·조건차이를함께기록한다.','여러요소를함께바꾼전후차이는한요소의원인효과를분리하지못한다.')
add(['SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection'],'CJB04-02','activity_context','발표뒤성찰에서참여·수학적학습·지원과지속가능성의근거를나누어보고한다.','공동산출물·흥미와개인의이해·후속사용은다른결과이며같은프로그램의단계를독립표본으로더하지않는다.')

def main():
 logging.getLogger('pypdf').setLevel(logging.ERROR)
 if not set(SPECS)<=load(ROOT/'data/literature_claim_reviews.json')['sources'].keys():
  rows={x['stem']:x for x in load(CACHE/'acquisition.json')}
  for s in SPECS.values():
   a=rows[s['stem']];assert a['sha256']==s['sha256'] and a['reading_completed'] and a['images_viewed']
   assert a['read_text_pages']==a['viewed_image_pages']==s['pages']
  from check_dbr_measurement_models import check
  assert check()['status']=='pass'
 record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='개발 탐구의 측정·단계 기록·평가 원논문 대조',detail_key='complete_foundational_article_review',roles={c[1]:'related_theoretical_context' for c in CLAIMS})

if __name__=='__main__':main()

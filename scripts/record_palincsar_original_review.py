"""Read the cited1984original, retaining measurement and design limitations."""
from record_scoped_pdf_research import record
from literature_review import ROOT
from extend_lt2_length_assets_review import load
from check_palincsar_measurement_models import check

SOURCE='PALINCSAR_BROWN_1984_RECIPROCAL';DATE='2026-11-18'
CACHE=ROOT/'tmp/literature/palincsar-original-20261118'
SHA='f08475a3164aad9fe32a3dc3f6f1f3f3780da9db0db69fb716403b6341d685fe'
URL='https://images.scholastic.co.uk/assets/a/d6/6f/palincsar-reciprocal-teaching-1619152.pdf'
DOI='https://www.tandfonline.com/doi/abs/10.1207/s1532690xci0102_1'
VISUALS=[1,10,11,12,13,20,21,22,23,24,25,26,27,29,30,31,33,35,36,37,38,41,42,43,45,46,47,48,49,50]
LI='12수과02-01';DE='12수과02-04';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
SCOPE='Scholastic 공개 배포 사본에서 논문 117–175쪽 전체 59쪽의 추출문과 선정 30판면을 읽었다. 표 1–12의 이어지는 부분·그림 1–4·감사·참고문헌을 확인했다. 네 활동의 조건부 사용·지원 조정·독립 평가·유지·교실 일반화·전이 과제와 표본·척도·미수집·비유의 결과를 대조했다. 전체 59판면을 모두 시각 대조한 것은 아니다.'
LIMIT='읽기 이해 연구다. 연구 1의 37명은 각 6명인 네 집단의 24명과 규준 비교 13명이다. RT/통제 집단과 6개월 뒤 진행된 LI/검사만 집단을 동시에 진행한 네 집단 무작위 실험으로 보지 않는다. 연구 2는 기존 네 집단 7/5/5/4명, 합계 21명이며 교사 연수 3회와 주간 지원이 있었다. 표 8과 본문의 수치 차이·전이 검사 미수집 집단·중요도 평정의 미개선·전체 상호작용의 비유의를 보존한다. 원자료·원테이프·1982년 박사논문/예비 연구·모든 인용 원전·출판사 직접 파일/정오표는 미확인이다. Brown(1992)의 재서술과 독립 표본으로 중복 집계하지 않고 국내 수학 효과·현재 학생 검증으로 옮기지 않는다.'
SPECS={SOURCE:dict(stem='palincsar-brown-1984-distributor-copy',render_stem='palincsar',sha256=SHA,total=59,pages=list(range(1,60)),text_pages=list(range(1,60)),visuals=VISUALS,pdf_url=URL,url=DOI,year=1984,title='Reciprocal Teaching of Comprehension-Fostering and Comprehension-Monitoring Activities — complete59page article, public distributor copy',authors=['Annemarie Sullivan Palincsar','Ann L. Brown'],scope=SCOPE,limit=LIMIT,design='연구1:시점이다른비교집단과가변기초선;연구2:기존교사집단의가변기초선·전후검사',sample='연구1각6명RT/LI/검사만/통제집단24명과규준13명. 연구2기존4집단21명;모두7학년은아님. 검사의대상집단과시점·척도는같지않다.',student_outcome_study=True,supports=['실제이해문제에따른질문·요약·명료화·예상과지원조정','훈련·독립수행·지연유지·다른과제의대응','척도·미수집·비유의결과·표본조건의보고'],next_review='현재수학활동의익명실제응답과독립검토를확보하고정식출판사판/표8정오표·1982원학위논문을추가대조한다.')}
CLAIMS=[
 (SOURCE,'PB84-01',[LI,PL,RU],[3,4,5,6,7,8,14,15,22,23,24,25,26,27,45,46,47,53],'문헌 읽기와 탐구 실행에서 요약·질문·명료화·예상을 실제 이해 문제에 맞게 사용한다. 무엇이 불명확했는지, 바꾼 순서, 교사의 모델/힌트와 학생 자기 설명을 남기고 새 내용을 도움 없이 읽는 수행을 따로 확인한다.','원논문에서도 명료화·예상은 필요할 때 사용했고 매 문단의 의무 순서나 각 활동의 빈도를 모두 채점하지 않았다. 교사 말의 반복·네 이름 채우기·학습 중 발언 개선만으로 독립 이해·수학 전이를 보장하지 않는다.'),
 (SOURCE,'PB84-02',[DE,PL,RE],[9,10,11,14,16,17,18,19,32,34,36,37,41,42,48,51,52,53,54],'평가 계획에서 훈련 중 대화·별도 자료의 독립 수행·지연 검사·교실 일반화·형식이 다른 전이 과제를 나누고 대상 집단과 도움 조건을 기록한다. 시행하지 않은 검사는 미수집으로 남기고 지원 변경과 검사 상황 변경을 함께 보고한다.','연구 1의 일반화/전이는 RT와 통제 집단에서만 수집됐고 LI/검사만 집단의 결과는 0점이 아니다. 연구 2의 교사들은 연수와 주간 지원을 받았다. 저자가 인정한 복수 요인의 혼입을 지워 한 활동의 단독 인과 효과나 지원 없는 현장 정착으로 쓰지 않는다.'),
 (SOURCE,'PB84-03',[OU,RE],[10,11,12,13,27,29,30,31,32,33,34,35,36,37,38,41,43,44,48,49,50,52],'결과 발표와 성찰에서 정답률·이상 탐지·백분위·학년과 개월 표기·집단 평균을 구별한다. 표본/집단의 시점·선정과 미수집·변화가 불확실한 결과·원문 표와 본문의 수치 차이도 같이 남긴다.','연구 1 질문 예상 검사의 전체 상호작용은 비유의이고 낮은 시작점의 4명에서만 개선이 보고됐다. 중요도 평정은 두 연구 모두 개선 입증이 없었다. 이를 모든 전이의 성공이나 모든 능력의 효과 0으로 바꾸지 않고 표 8/본문의 불일치를 임의로 교정·통합하지 않는다.')
]

def task(n,codes,q,e,i):return dict(id=f'PB84-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS={SOURCE:[
 task(1,[LI,PL,RU],'문헌의 주장처럼 쓴 “모든 실수 x에 대해 (x+1)²=x²+1”을 읽었다. 요약을 끝냈다는 표시보다 먼저 무엇을 확인하고 어떻게 고칠까?','x=1에서 왼쪽 4·오른쪽 2이므로 반례가 된다. 전개하면 (x+1)²=x²+2x+1이다. 어떤 부분이 틀렸는지와 수정 근거를 말하고, 필요한 질문·명료화·요약을 선택한다. 한 값의 일치나 네 활동명 기입은 항등식의 증명이 아니다.','새로 만든 수학 문헌 읽기 과제다. 영어 읽기 처치의 수학 효과를 검증한 것이 아니다.'),
 task(2,[OU,RE],'표가 4,2를 4학년+2개월, 5,0을 5학년+0개월로 정의한다. 차이를 십진소수 5.0−4.2로 계산해도 되는가?','정의된 표기는 학년과 개월의 쌍이다. 12개월 단위로 바꾸면 60−50=10개월이며 십진 차 0.8년=9.6개월과 다르다. 학년 환산 점수 차를 실제 수업 10개월·진급·일반 능력의 성장으로 단정하지 않는다.','원논문 표 1/10의 범례에서 착안한 자체 값의 예다. 원표본의 새 결과나 학년 환산 척도의 현행 타당성 검증이 아니다.'),
 task(3,[DE,OU,RE],'가상 자료 36건 중 이상 3건·정상 33건이다. A는 전부 정상이라 했고, B는 이상 3건 모두와 정상 3건을 이상이라 했다. 둘의 전체 정답률과 이상 탐지율은 같은가?','A는 정답 33/36, 이상 탐지 0/3이다. B도 정답 (3+30)/36=33/36이지만 이상 탐지는 3/3이고 정상 중 오탐은 3/33이다. 같은 전체 정답률로 이상 탐지 능력을 동일하게 판정할 수 없다. 분모·오탐·미탐을 함께 보고한다.','원논문의 36줄·이상 3줄 측정 구조에서 착안한 합성 분류 예다. 저자의 추측 교정 점수 공식을 복원하거나 실제 응답을 재분석한 것이 아니다.'),
 task(4,[DE,PL,RE],'연구 1이 각 6명인 네 집단과 규준 13명을 보고했다. 전이 검사는 RT와 통제 집단에만 있다. 이를 37명 모두 처치·네 집단 모두 전이 검증으로 보고해도 되는가?','전체 37명 안에 처치/비처치 대상 24명과 규준 13명이 있으며 RT 처치는 6명이다. LI와 검사만 집단은 6개월 뒤 진행됐고 전이 자료가 없으므로 0점으로 채우지 않는다. 연구 2의 21명과도 동일한 설계·독립 무작위 표본으로 합산하지 않는다.','원문 설계 범위를 읽는 자체 과제다. 개인 명단·테이프·원응답을 새로 확보하거나 현재 학생을 검증한 것이 아니다.')
]}
DETAILS={SOURCE:dict(full_article_text_read=True,all_pdf_images_viewed=False,pdf_pages=59,article_pages=59,article_printed_pages='117–175',wrapper_pages=0,selected_text_pages=list(range(1,60)),selected_visual_pages=VISUALS,numbered_figures=4,numbered_tables=12,figure_pdf_pages={'1':29,'2':30,'3':31,'4':49},table_pdf_pages={'1':[12,13],'2':[20],'3':[21],'4':[22,23],'5':[24,25],'6':[26,27],'7':[33],'8':[35],'9':[38],'10':[43],'11':[45],'12':[46,47]},study1_total=37,study1_eligible_groups=[6,6,6,6],study1_normative_volunteers=13,study1_all_groups_simultaneous_randomized_trial_verified=False,study1_transfer_groups=['RT','untreated control'],study1_transfer_not_collected=['LI','test only'],study2_group_sizes=[7,5,5,4],study2_total=21,study2_all_seventh_graders=False,study2_teacher_training_sessions=3,study2_weekly_researcher_support=True,study2_concurrent_untreated_arm_verified=False,importance_rating_improvement_demonstrated=False,study1_predicting_questions_overall_interaction_significant=False,study1_initially_lower_scoring_subgroup_n=4,study1_standardized_readministration_mode_changed=True,source_table_body_discrepancies=[dict(measure='Study2summarizingpost',table8='48.75',body164='48.71'),dict(measure='Study2questions',table8=['53.74','61.20'],body166=['53.62','61.24']),dict(measure='Study2totalcorrect',table8=['30.48','33.68'],body166=['30.47','33.47']),dict(measure='Study2anomaliespost',table8='1.89',body166='1.84')],source_discrepancies_resolved=False,table8_footnote_printed='N/3',body_anomalous_lines=3,extraction_correction=dict(pdf_page=36,printed_page=152,extracted='6.17',actual_scan='61.7',source_binary_modified=False),all_errata_verified=False,publisher_direct_binary_obtained=False,raw_tapes_or_student_data_read=False,cited_originals_all_read=False,parent_retelling='BROWN_1992_DESIGN_EXPERIMENTS',parent_is_independent_replication=False,exact_own_model_check=check())}
CORRECTIONS={SOURCE:['연구 1의 37명은 각 6명인 네 집단의 24명과 규준 비교 13명이다. 네 집단 모두를 동시에 진행한 무작위 비교로 보지 않는다.','네 활동은 필요에 맞춰 사용한다. 명료화와 예상을 매 문단 의무 수행·전부 채점으로 바꾸지 않는다.','전체 질문 예상 상호작용의 비유의·선정 4명 개선·중요도 평정 미개선·일부 검사 미수집을 구별한다.','표 8과 본문의 수치 불일치는 확보 사본의 미해결 차이로 남기고 정오표 없이 진짜 값을 선택하지 않는다. PDF 36의 6.17 추출 오류만 실제 판면 61.7로 대조한다.','정답률·탐지율·백분위·학년/개월·집단 평균과 개인을 구별한다. 축 절단과 8주 시간 간격을 무시해 원자료를 재구성하지 않는다.','연구 2의 기존 혼합 학년 21명·교사 연수 3회/주간 지원을 보존하고 현재 수학 효과·독립 현장 검증·Brown(1992)과 새로운 독립 반복으로 세지 않는다.']}
INTERPRETATIONS={}
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1','SEC_12수과03-01_C04','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'PB84-01']=('activity_context','문헌의 이해 점검과 실행의 자기 설명·지원 조정을 연결한다.','네 활동명의 수행이나 교사 모델의 반복을 독립 읽기·수학 전이의 검증으로 세지 않는다.')
for rid in ['SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'PB84-03']=('activity_context','결과 발표의 척도·표본·미수집·불확실한 결과를 성찰 기록과 대조한다.','전체 정답률·집단 평균·선정 하위 집단의 개선을 개인 능력·모든 전이·단독 인과 효과로 확대하지 않는다.')

def main():
 if SOURCE not in load(ROOT/'data/literature_claim_reviews.json')['sources']:
  a=load(CACHE/'acquisition.json');assert a['sha256']==SHA and a['reading_completed']
  assert a['read_text_pages']==list(range(1,60)) and a['viewed_image_pages']==VISUALS and not a['all_pdf_images_viewed']
  assert check()['status']=='pass'
 record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='인용 원연구의 이해점검·전이검사·측정과 표본 대조',detail_key='palincsar_original_review',roles={c[1]:'related_theoretical_context' for c in CLAIMS})

if __name__=='__main__':main()

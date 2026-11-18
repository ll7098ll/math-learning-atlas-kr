"""Read the ERIC article and keep intervention, analysis and mathematical scopes."""
from record_scoped_pdf_research import record
from literature_review import ROOT
from extend_lt2_length_assets_review import load
from check_xin_problem_and_sample_models import check

SOURCE='XIN_JITENDRA_DEATLINE_BUCHMAN_2005';DATE='2026-11-18'
CACHE=ROOT/'tmp/literature/xin-original-20261118'
SHA='1b2115e23d17ada1b3b4aa5eb87a497be8bdf78b76bd9ce5b05a711355766b52'
URL='https://files.eric.ed.gov/fulltext/EJ722297.pdf'
PAGES=list(range(1,13))
RATIO=['6수02-02','6수02-03','6수02-04','9수02-01']
STUDY=['12수과02-04','12수과03-03','12수과03-04']
SCOPE='ERIC 공개 사본의 논문181–192쪽 전체12쪽 추출문과 전체12판면을 읽었다. 표1–3·그림1–2·방법·결과·제한·감사·참고문헌을 대조했다. 시작22명과 네 시점 완료19명·LD완료16명, 시점별 표본·계산기/읽기 지원·지연 검사 전 전략 복습·점수와 효과크기 정의를 구별했다. 인쇄186쪽의 비례식은 실제 판면을 대조하고 올바른 수량 대응을 자체 계산했다.'
LIMIT='미국 한 중학교의 학습문제가 있는6–8학년22명에 대한12회 약1시간 별도 수업의 비교다. 두 조건 모두 명시적 지도·연습·피드백·계산기를 제공했고 GSI도 그림을 사용했다. 지연 검사는 전략 복습 뒤 시행했으며 추적 간격은3주–약3개월로 일정하지 않다. 원자료·개인별 결측 사유·출판사 직접 파일/정오표·학위논문·모든 인용 원연구·WWC 재분석 원자료는 미확인이다. 국내 학생·독립 현장 효과나 도식 하나의 단독 효과로 일반화하지 않는다.'
SPECS={SOURCE:dict(stem='xin-jitendra-deatline-buchman-2005-eric',render_stem='xin',sha256=SHA,total=12,pages=PAGES,text_pages=PAGES,visuals=PAGES,pdf_url=URL,url=URL,year=2005,title='Effects of Mathematical Word Problem–Solving Instruction on Middle School Students with Learning Problems — complete12page ERIC copy',authors=['Yan Ping Xin','Asha K. Jitendra','Andria Deatline-Buchman'],scope=SCOPE,limit=LIMIT,design='두코호트8/14명내학생무작위배정,SBI/GSI각11명,교사조건교환을포함한사전사후·유지·전이비교',sample='6–8학년22명=학교분류LD18+정서장애1+수학학습위험3. 네시점완료19명,LD완료16명;시점별분모는같지않다.',student_outcome_study=True,supports=['기준량·비교량·동일한양의짝을보존하는도식과식','시점별표본·결측·처치묶음·지연지원조건','부분점수·전이·효과크기의정의와한계'],next_review='원자료/결측 사유·정식 출판판/정오표·WWC 분석 산출물을 대조하고 자체 수학 과제의 실제 응답을 별도로 확보한다.')}
CLAIMS=[
 (SOURCE,'XIN05-01',RATIO,[3,4,5,6,7],
  '곱셈적 비교에서는 기준량·비교량·배율을 먼저 정하고 도식의 각 수량을 식의 같은 자리에 대응시킨다. 비례 상황은 두 양의 단위와 방향을 유지해 같은 비율인지 확인한다. 확보 사본186쪽의3/12=12/80은 성립하지 않는다. 같은 짝의 비는3/20=12/80이고, 두 짝 사이의 배를 비교하면3/12=20/80이다.',
  '이는 확보 사본의 수식과 수량 대응을 대조한 자체 수학 검토다. 공식 정오표·잘못 인쇄된 원인의 확인은 아니다. 영어 문장에서의 위치 규칙을 한국어 전 문항의 키워드 규칙으로 옮기거나 교차곱만으로 비례 여부를 판단하지 않는다. 두 조건 모두 그림을 사용했으므로 그림 유무의 단독 실험으로 보지 않는다.'),
 (SOURCE,'XIN05-02',STUDY,[2,3,7,8,9,10],
  '연구 설계와 결과를 보고할 때 참가22명·네 시점 완료19명·LD완료16명과 검사별 실제 분모를 구별한다. 표3의 직후 검사는11/11명, 유지9/11명, 추적9/10명, 일반화 사후11/10명이다. 두 가이드의19명/22명은 원논문에 명시된 서로 다른 분석 범위로 설명할 수 있으며 하나를 오자로 교체하지 않는다.',
  '개인별 결측 사유와 두 가이드의 전체 재분석 파일은 확보하지 않았다. 완료 표본의 서술을 모든 검사에 강제하지 않고 미수집을0점으로 채우지 않는다. LD시작18명/완료16명과 전체22명/완료19명을 혼동하지 않는다. 수업 묶음의 비교이며 무지도 통제나 한국 학생 검증이 아니다.'),
 (SOURCE,'XIN05-03',STUDY,[6,7,8,9,10],
  '평가에서는 정답1점·맞는 식만 세운 경우0.5점을 포함한 백분율과 완전 정답 문항률을 구별한다. 16문항 목표 검사와10문항 일반화 검사를 구별하고, 전략 복습을 받은 지연 수행과 도움 없는 독립 유지를 구별한다. 원논문 표3직후 효과1.69와 대수 가이드1.87은 계산 정의를 확인해 보고한다.',
  '공개 반올림 평균/표준편차로 사전 차이를 보정하고 소표본 보정하면 약1.87이 재현되지만 WWC의 정확한 원자료 재분석 확인은 아니다. 직후–추적의SBI집단내p=.051을5%기준 유의 개선으로 쓰지 않는다. 전이 검사의 시점×집단 상호작용과 집단 주효과p=.819를 구별하며 모든 실생활 문제·무지원 장기 유지의 효과로 확대하지 않는다.')
]
def task(n,codes,q,e,i):return dict(id=f'XIN05-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS={SOURCE:[
 task(1,RATIO,'가상 조리표에서 달걀3개로20개를 만들고 달걀12개로80개를 만든다. 3/12=12/80으로 같은 비를 확인할 수 있는가?',
  '3/12=1/4이지만12/80=3/20이므로 같지 않다. 같은 양의 짝을 유지한3/20=12/80, 또는 두 짝 사이의 배를 비교한3/12=20/80은 성립한다. 분자·분모의 양과 단위를 먼저 적는다.',
  '원논문186쪽의 수식 불일치에서 착안한 자체 설명 과제다. 출판사 정오표나 실제 학생 반응을 확보한 것은 아니다.'),
 task(2,['6수02-02','6수02-03','9수02-01'],'가상 상황에서 민수가 모은12개는 지수가 모은 수의1/3이다. “1/3”을 보고12를3으로 나누면 되는가?',
  '지수의 수를x라 하면12=x/3이므로x=36이다. 민수12가 비교량, 지수36이 기준량이며12/36=1/3이다. 기준량과 비교량을 바꾸면 비율도 바뀌므로 단어 하나로 연산을 정하지 않는다.',
  '원논문의 곱셈적 비교 구조를 바꾼 자체 과제다. GSI의 모든 그림 전략이나 다른 교수법의 효과를 판정하는 과제가 아니다.'),
 task(3,STUDY,'연구의 시작은11/11명이고 유지 검사는9/11명, 추적은9/10명이다. 모든 시점의 표본을19명이라 쓰거나 결측3명을0점으로 넣어도 되는가?',
  '시작/직후22명, 유지20명, 추적19명이다. 네 시점 모두 완료한19명의 반복측정 분석과 시점별 관측 표본은 구별한다. LD시작18명·모든 검사완료16명도 다른 수다. 결측은 미수집으로 남기고 사유·조건별 비율과 분석 방식을 확인한다.',
  '공개 논문의 집계 단위를 읽는 자체 과제다. 개인별 결측 사유나 원자료를 복원한 것이 아니다.'),
 task(4,STUDY,'16문항에서 식만 맞춘1문항에0.5점을 주고 나머지는0점이라면 백분율은 얼마인가? 전략 복습 뒤 추적 점수가 높아졌고p=.051이면 무지원 유지가 유의하게 개선됐다고 해도 되는가?',
  '부분점수 포함 점수는0.5/16×100=3.125%이고 완전 정답 문항률은0%다. 10문항 검사라면 같은0.5점도5%다. 전략 복습이 있었다는 조건을 남기고p=.051은5%기준 유의 개선으로 쓰지 않는다. 비유의만으로 효과가0이라고 단정하지도 않는다.',
  '부분점수 예는 합성 자료이며 논문 참가자의 실제 점수가 아니다. 복습 조건·척도·유의성의 구분을 확인하는 자체 과제다.')
]}
DETAILS={SOURCE:dict(full_article_text_read=True,all_pdf_images_viewed=True,pdf_pages=12,article_pages=12,article_printed_pages='181–192',wrapper_pages=0,numbered_tables=3,numbered_figures=2,initial_groups=[11,11],cohorts=[8,14],initial_ld=18,initial_emotional_disorder=1,initial_at_risk=3,complete_case_groups=[9,10],ld_complete_case=16,maintenance_groups=[9,11],generalization_post_groups=[11,10],iq_achievement_records_n=9,instruction_sessions=12,session_minutes_approximately=60,calculators_both_conditions_and_tests=True,both_conditions_use_pictures=True,delayed_tests_strategy_review=True,followup_lapse='3weeks–about3months',target_items=16,generalization_items=10,correct_points=1,equation_only_points=0.5,source_equation_discrepancy=dict(pdf_page=6,printed_page=186,displayed='3/12=12/80',correct_same_pair='3/20=12/80',valid_across_pairs='3/12=20/80',observed_in_actual_image=True,official_erratum_verified=False),caption_alignment_limit='Figure1captionmentionsgeneralstepsbutimageisSBIcomparative/proportiondiagrams;Figure2captionisschematicrepresentationswhilebodyusesitforGSIpictures. Identifybyactualpage/content,notcaptionalone;publishercauseunverified.',table1_label_limit='RowprintsSENwhilefootnotedefinesSED;bodyreportsoneparticipantwithsevereemotionaldisorders. Preserveactualcopyspelling,donotcreatenewcategory.',source_table3_post_d=1.69,algebra_guide_post_effect=1.87,within_sbi_post_to_followup_p=0.051,transfer_group_main_p=0.819,transfer_group_time_interaction_significant=True,guide_crosschecks=dict(fractions_source='IES_FRACTIONS_2010',fractions_pdf_page=70,fractions_reported_n=19,fractions_ld_n=16,algebra_source='IES_ALGEBRA_2015',algebra_reported_n=22,sample_scope_difference_supported_by_original=True,guide_error_established=False,exact_individual_sample_identity_verified=False),raw_student_data_read=False,publisher_direct_binary_obtained=False,publisher_binary_fidelity_verified=False,all_errata_verified=False,cited_originals_all_read=False,dissertation_read=False,exact_own_model_check=check())}
CORRECTIONS={SOURCE:[
 '22명은 시작/직후 표본,19명은 네 시점 완료 표본이다. LD18명/완료16명도 구별하며 가이드 수치 하나를 오류로 교체하지 않는다.',
 '186쪽 실제 판면의3/12=12/80은 거짓이다. 수량 짝을 유지한3/20=12/80과 배를 비교한3/12=20/80을 자체 계산으로 제시한다. 원 PDF 바이트는 변경하지 않는다.',
 'SBI와GSI모두 명시적 지도·연습·피드백·그림·계산기를 포함한다. 도식 유무 한 요인의 실험이나 무지도 비교가 아니다.',
 '유지/추적 전 전략 복습과 가변 추적 간격,부분점수,각 검사 분모,p=.051·전이 집단 주효과 비유의를 보존한다.',
 '원논문1.69와 가이드1.87은 요약 통계의 사전 차이/소표본 보정으로 설명 가능하다. 정확한WWC산출물과 원자료는 미확인이다.'
]}
INTERPRETATIONS={}
for rid in ['REV-6수02-04-1','REV-6수02-03-1','REV-6수02-03-2']:
 INTERPRETATIONS[rid,'XIN05-01']=('activity_context','두 양의 기준·단위·방향을 고정하고 같은 짝의 비와 두 짝 사이의 배를 연결한다.','확보 사본186쪽의 잘못된 식을 그대로 복사하지 않고 수량 대응을 확인한다. 수업 묶음의 결과를 도식 하나의 효과로 확대하지 않는다.')
for cid in ['XIN05-02','XIN05-03']:
 for rid in ['SEC_12수과02-04_C04','SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
  INTERPRETATIONS[rid,cid]=('activity_context','평가 계획과 결과 성찰에서 시점별 분모·결측·지원 조건·점수 정의와 분석 범위를 대응시킨다.','원자료가 없는 표본의 사유를 추정하거나 미수집을0점으로 넣지 않는다. 복습 뒤 지연 검사·부분점수·서로 다른 효과 정의를 독립 수행으로 합치지 않는다.')

def main():
 if SOURCE not in load(ROOT/'data/literature_claim_reviews.json')['sources']:
  a=load(CACHE/'acquisition.json');assert a['reading_completed'] and a['sha256']==SHA
  assert a['read_text_pages']==a['viewed_image_pages']==PAGES and a['all_pdf_images_viewed']
 record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='비례 문장제 원연구의 수량 대응·분석 표본·지원 조건 대조',detail_key='xin_original_review')

if __name__=='__main__':main()

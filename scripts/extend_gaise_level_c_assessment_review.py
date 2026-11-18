"""Complete the GAISE main-text reading, retaining bounded prior review history."""
import copy
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from statistics import mean, median, stdev
from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews
from record_gaise_level_a_review import SOURCE, URL, SHA

PRIOR_NOTES='data/literature_evidence/GAISE_2020_level_b_review_notes.json'
PRIOR_SHA='c9eba33437731a2cf62e5f2b73d9eee8040f7a37b8cfd39687a4b703b677e088'
NOTES='data/literature_evidence/GAISE_2020_level_c_assessment_review_notes.json'
NEW_TEXT=[1,2]+list(range(79,127))
NEW_VISUAL=[1,2,79,85,86,87,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,113,114,115,116,117,118,119,120,121,123,124,125,126]

MAPPINGS=[
 ('G2C01',['12실통02-04'],['인쇄77–79 / PDF85–87'],
  '산포의 기준·단위·분모와 기술 요약·모수 추정을 구별하는 자체 계산에 참고한다.',
  'n−1 보정이 표준편차 자체를 불편추정량으로 만든다고 설명하지 않는다. 평균±MAD/SD를 정해진 포함률의 구간으로 쓰지 않고,정규 모형의 경험 규칙을 모든 분포에 적용하지 않는다. MAD는 교사용 확장이다.'),
 ('G2C02',['12실통03-04'],['인쇄72–76·80–84·87–88 / PDF80–84·88–92·95–96','인쇄113 / PDF121'],
  '귀무 모형·통계량·꼬리 방향·반복 단위를 명시하고 모의실험의0회와 정확한0확률을 구별하는 자체 활동에 참고한다.',
  '유한 모의실험에서 극단값0회는 이론 p값0의 증명이 아니다. p값을 귀무가설의 사후확률이나 인과 증거로 바꾸지 않는다. 자료를 본 뒤 검정 방향을 바꾸거나 표집과 배정의 모형을 혼용하지 않는다.'),
 ('G2C03',['12실통03-02','12실통03-03'],['인쇄74·82–83 / PDF82·90–91','인쇄111 / PDF119'],
  '구간의 반복 표집 해석·표준오차·표본 크기의 효과를 확인하는 자체 비교에 참고한다.',
  '원문의2배 표준오차는 근사다. 무작위성·독립성·유한 모집단·성공/실패 빈도를 확인하며,새 표본의 중심·관측 비율이 그대로라고 보장하지 않는다. 신뢰구간은 개인값의95% 범위나 모수의 사후확률이 아니다.'),
 ('G2C04',['12실통02-02'],['인쇄84–88 / PDF92–96','인쇄92–94 / PDF100–102','인쇄109–110 / PDF117–118'],
  '관찰·실험·측정 단위·실험 단위와 결측을 확인하고 결론 범위를 제한하는 자체 설계에 참고한다.',
  '원문 씨앗 실험의 봉투별 공유 조건과 처리별 반복 수를 추가 확인한다. 미발아 수가 같아도 결측 편향이 없다는 증명은 아니다. 건강 사례는 관찰 연구의 교육용 설명이며 현재 의료 권고나 한국어 과제 효과가 아니다.'),
 ('G2C05',['12인수04-02'],['인쇄89–91 / PDF97–99','인쇄112–113 / PDF120–121'],
  '최소제곱 예측·잔차·측정 단위·관측 범위와 평균 반응/개별 관측의 구별을 자체 예에 연결한다.',
  '원문의 간이 예측구간과 다른 결론 구간은 계산 방법이 일치하지 않아 그대로 전용하지 않는다. 정식 회귀 추론의 가정·레버리지·오차를 별도 확인하고,관측 범위 안이라는 사실만으로 적합·인과·새 대상 예측 정확도를 보장하지 않는다.'),
 ('G2C06',['12인수04-01','12인수04-03'],['인쇄97–103 / PDF105–111'],
  '혼동행렬의 행·열·분모와 규칙 선택 자료/새 평가 자료를 구별하는 자체 분류 비교에 참고한다.',
  '분류 규칙을 고른 같은 자료의 오류율을 새 자료의 검증 성능으로 쓰지 않는다.27/160은16.875%이며 원문 약18%를 복사하지 않는다. CART 전체 알고리즘·새 원자료·학습 효과를 검증한 주장이 아니다.'),
 ('G2C07',['6수04-03','12실통01-02'],['인쇄95–97 / PDF103–105','인쇄105–113 / PDF113–121'],
  '질문·측정·표현·해석과 결정 기준이 맞는지 여러 발문에서 확인하는 자체 평가 활동에 참고한다.',
  '계산 정답 하나를 통계적 탐구 전체나 고정 발달 단계의 판정으로 쓰지 않는다. 지도 면적·지역 수를 인구 가중으로 읽지 않고 이동평균의 창·시점·자료 처리 규칙을 적는다. LOCUS/STEW의 신뢰도·원문 학생 자료를 자체 활동에 부여하지 않는다. 초등에 순위 합산·중앙값·추론 공식을 새 필수로 넣지 않는다.')
]

OBSERVATIONS=[
 dict(id='GC-P1',standard_codes=['12실통02-04'],
  question='교사용 가상 모형에서 모집단 값0과2를 같은 가능성으로 두 번 독립 복원 추출한다. 가능한 네 순서쌍을 모두 써서,분모n과n−1인 분산의 평균 및 n−1 표준편차의 평균을 비교하라.',
  expected='(0,0),(0,2),(2,0),(2,2)는 같은 가능성이다. 모집단 평균1·분산1·표준편차1이다. n=2 분모의 분산은0,1,1,0으로 평균1/2이고,n−1 분모의 분산은0,2,2,0으로 평균1이다. 후자의 표준편차 평균은√2/2로1과 다르다. 분산의 불편성과 제곱근의 불편성은 별개다.',
  interpretation='제곱 단위·원래 단위와 기술 분산·추정 분산을 구별한다. 작은 유한 모형의 전수 계산이며 모든 현실 자료가 독립·동일분포라는 증거는 아니다. 교사용 확장이고 실제 학생 반응이나 도구 실행 자료가 아니다.',student_validated=False),
 dict(id='GC-P2',standard_codes=['12실통03-04'],
  question='가상 서로 다른 카드6장 중 성공3장·실패3장을 섞어 앞 집단3장과 뒤 집단3장으로 나눈다. 앞 집단에 성공3장이 모두 온 결과를 사전에 정한 한쪽 극단으로 삼는다. 이 극단이20회 모의실험에서0회였다면 정확한 확률도0인가?',
  expected='앞 집단의 가능한 카드 집합은6개 중3개를 고른20가지이며 해당 극단은1가지라 정확한 한쪽 확률은1/20이다. 독립적으로20번 다시 섞었을 때 한 번도 극단이 없을 확률은(19/20)^20으로 양수다. 극단0/20은 이 모의실험의 관측 비율이며 정확한0확률이 아니다. 양쪽의 완전 분리를 극단으로 정하면2/20으로 다른 질문이다.',
  interpretation='카드ID·전체 성공 수·집단 크기를 고정하는 모형,꼬리 방향·동률 포함·반복 수를 먼저 적는다. 실제 난수 실험을 수행한 기록이 아닌 정확한 조합 계산이다. p값을 가설의 사후확률이나 효과 크기로 읽지 않는다.',student_validated=False),
 dict(id='GC-P3',standard_codes=['12실통03-02','12실통03-03'],
  question='가상 독립 무작위 표본에서 찬성 비율0.6을 고정해 비교한다. n=100과400일 때1.96√[0.6×0.4/n]인95% 정규근사 오차한계를 구하라. 표본을 네 배 늘리면 중심과 새 응답도 보장되는가?',
  expected='오차한계는 각각약0.09602·0.04801로 반이 된다. 고정한0.6 중심의 비교 구간은약[0.5040,0.6960]·[0.5520,0.6480]이다. 실제 새 표본에서는 관측 비율과 중심도 달라질 수 있다.95%는 같은 절차를 반복할 때 고정 모비율을 포함하는 장기 비율이며 개인 응답의95% 범위나 이미 정한 구간의 사후확률이 아니다.',
  interpretation='같은 신뢰수준·방법·비율을 고정한 비교와 실제 새 표본을 구별한다. 성공/실패 수·독립성·표집 비율·유한 모집단 조건을 확인한다. 가상 근사 계산이고 실제 표집·학생 검증 자료가 아니다.',student_validated=False),
 dict(id='GC-P4',standard_codes=['12실통02-02'],
  question='가상 재배 계획에서 밝음 봉투1개·어두움 봉투1개에 씨앗20개씩 넣고 처리한다.20개씩의 독립 실험 반복이라고 해도 되는가? 다른 기록에서 두 집단의 길이 자료가[2,4,누락,누락]·[6,8,누락,누락]이면 누락 수가 같으므로 전체 평균 차가 편향 없다고 할 수 있는가?',
  expected='같은 봉투의 씨앗은 물·온도 등 조건을 공유할 수 있고 처리와 봉투가 겹쳐 있다. 처리별 독립 봉투를 반복하고 봉투 배정·위치·측정 규칙을 설계해야 한다. 관측 길이 평균은3과7이지만,첫 집단 누락이10·10이고 둘째가0·0이었다면 전체 평균은6.5와3.5로 순서도 바뀐다. 이 완성값은 가능성을 보이는 가상 반례이며 실제 누락값의 추정이 아니다.',
  interpretation='측정 개수와 독립 실험 단위·관측자 범위·결측 원인을 구별한다. 미발아를 길이0으로 정의할지 미측정으로 둘지는 질문·판정 기준을 먼저 정한다. 자체 반례이며 실제 식물 실험·인과 효과·학생 반응 자료가 아니다.',student_validated=False),
 dict(id='GC-P5',standard_codes=['12인수04-02'],
  question='가상 짝 자료(x,y)=(1,2),(2,3),(3,7)에서 두 변수의 단위가cm일 때 최소제곱 직선과x=2의 잔차를 구하라. x만mm로 바꾸거나 x=4를 예측할 때 무엇이 달라지는가?',
  expected='평균은x=2,y=4이고 기울기는5/2,절편은−1이라 ŷ=−1+(5/2)x다. x=2의 예측4와 관측3의 잔차는−1이다. x′=10x이면 ŷ=−1+(1/4)x′로 같은 대상을 예측하고,x=4의 예측9는 관측 범위[1,3] 밖 외삽이다. 맞춘 직선은 실제 관측값·인과 법칙·개별 예측의 보장이 아니다.',
  interpretation='짝·변수 역할·잔차 부호·단위를 기록하고 평균 반응 신뢰구간과 새 개별 관측 예측구간을 구별한다. 주어진 세 점의 자체 계산이며 원문의 신체 측정 자료나 실제 도구 화면 실행·학생 반응이 아니다.',student_validated=False),
 dict(id='GC-P6',standard_codes=['12인수04-01','12인수04-03'],
  question='가상 분류 규칙을 고른 학습 자료의 표가 행예측A·B,열실제A·B에서[[8,1],[2,9]]다. 규칙을 고정한 뒤 처음 보는 평가 자료의 표는[[3,2],[2,3]]이다. 각 전체 오류율과A예측 중 맞은 비율을 구하고 어느 값이 새 자료 평가인가 설명하라.',
  expected='학습 자료 오류율은(1+2)/20=15%,A예측 중 맞은 비율은8/9다. 새 평가 자료 오류율은(2+2)/10=40%,A예측 중 맞은 비율은3/5다. 두 표를 합친7/30만 제시해 학습·평가의 차이를 지우지 않는다. 규칙을 평가 자료에 맞춰 다시 고르면 이 자료는 더 이상 독립된 최종 평가가 아니다.',
  interpretation='행·열·정답 열람 시점·자료 분리·분모를 먼저 적는다. 실제A 중A예측 비율과A예측 중 실제A 비율도 구별한다. 유한 가상 예로서 새 환경의 오류율·개별 대상의 확률·모형 우월성을 보장하지 않는다. 실제 시스템·학생 검증 자료가 아니다.',student_validated=False),
 dict(id='GC-P7',standard_codes=['6수04-03','12실통01-02'],
  question='가상5명의 선호 순서가3명은A>B>C,2명은B>C>A다. 한 가지 최선호 도수로 고른 결과와1·2·3위에1·2·3점을 주어 합이 작은 것을 고른 결과를 비교하고,조사 질문·선정 기준·자료 표현을 설명하라.',
  expected='최선호 도수는A3·B2·C0이라A를 고른다. 순위 합은A9·B8·C13이라 정한 합산 규칙에서는B를 고른다. 두 결과는 서로 다른 결정 기준이다. 순위 점수의 간격을 실제 선호 강도의 같은 차이라고 볼 근거는 없다. 초등에서는 한 가지 최선호의 도수·그래프·질문 범위를 확인하고 순위 합산은 교사용 비교로 둔다.',
  interpretation='자료를 본 뒤 유리한 결정 규칙만 고르지 않고 문항·대상·단위·표현·추천 근거를 적는다. 계산 답·설명·재질문·도움 후 반응을 구별하며 한 발문으로 탐구 전체의 숙달을 판정하지 않는다. 가상 자료이고 실제 조사·학생 반응이나 진단 타당성 검증이 아니다.',student_validated=False)
]

# Only numerical facts transcribed for arithmetic checking; no source pages are redistributed.
FOREARM=[(45,180),(44.5,173.2),(39.5,155),(43.9,168),(47,170),(49.1,185.2),(48,181.1),(47.9,181.9),(40.6,156.8),(45.5,171),(46.5,175.5),(43,158.5),(41,163),(39.5,155),(43.5,166),(41,158),(42,165),(45.5,167),(46,162),(42,161),(46,181),(45.6,156),(43.9,172),(44.1,167)]
LIGHT=[2,3,5,5,5,5,5,7,7,7,8,8,8,9,10,10,10,10,10,10,10,10,14,15,15,20,21,21]
MIXED=[3,4,5,9,10,10,10,10,10,11,13,15,15,15,17,20,20,20,20,20,21,21,22,22,23,25,25,27]
DARK=[5,8,8,10,10,14,15,15,15,20,20,20,20,20,22,25,25,25,25,26,30,30,35,35,35,35,36,37,38,5,8,8,10,10,10,11,14,15,15,15,16,20,20,20,20,20,24,25,29,30,30,30,30,31,33,35,35,40]

def calculate():
 xbar=mean(x for x,y in FOREARM);ybar=mean(y for x,y in FOREARM)
 sxx=sum((x-xbar)**2 for x,y in FOREARM);syy=sum((y-ybar)**2 for x,y in FOREARM);sxy=sum((x-xbar)*(y-ybar) for x,y in FOREARM)
 slope=sxy/sxx;intercept=ybar-slope*xbar
 fit=dict(n=len(FOREARM),slope=slope,intercept=intercept,r=sxy/math.sqrt(sxx*syy),residual_se=math.sqrt(sum((y-intercept-slope*x)**2 for x,y in FOREARM)/22))
 tails={str(p):str(sum((F(math.comb(60,k))*p**k*(1-p)**(60-k) for k in range(35,61)),F(0))) for p in [F(1,2),F(2,5)]}
 shuffle=sum((F(math.comb(35,k)*math.comb(25,37-k),math.comb(60,37)) for k in range(30,36)),F(0))
 return dict(forearm_table_recalculation=fit,seed_table_summary=[dict(n=len(v),sum=sum(v),mean=mean(v),sample_sd=stdev(v)) for v in [LIGHT,MIXED,DARK]],binomial_tail_n60_x_at_least35=tails,fixed_margin_shuffle_one_sided_tail=str(shuffle),cvd_counts=[[93,12,22,28],[1921,655,389,342]],cart_leaf_counts=[[42,4],[6,1],[9,1],[11,21],[4,3],[7,51]])

def verify():
 assert len(NEW_TEXT)==50 and len(NEW_VISUAL)==41 and set(NEW_VISUAL)<=set(NEW_TEXT)
 samples=list(itertools.product([0,2],repeat=2));sse=[sum((x-F(sum(v),2))**2 for x in v) for v in samples]
 assert sse==[0,2,2,0] and sum(sse)/4==1 and sum(sse)/8==.5
 assert math.sqrt(2)/2!=1
 allocations=list(itertools.combinations(range(6),3));extreme=sum(set(a)=={0,1,2} for a in allocations)
 assert len(allocations)==20 and extreme==1 and F(19,20)**20>0
 assert math.isclose(1.96*math.sqrt(.6*.4/100),2*1.96*math.sqrt(.6*.4/400))
 assert mean([2,4,10,10])==6.5 and mean([6,8,0,0])==3.5
 pairs=[(F(1),F(2)),(F(2),F(3)),(F(3),F(7))]
 assert sum((x-2)*(y-4) for x,y in pairs)/sum((x-2)**2 for x,y in pairs)==F(5,2)
 assert sum(y-(-1+F(5,2)*x) for x,y in pairs)==0 and 3-(-1+F(5,2)*2)==-1
 assert F(3,20)==F(15,100) and F(4,10)==F(40,100) and F(8,9)!=F(3,5)
 assert [3*1+2*3,3*2+2*1,3*3+2*2]==[9,8,13]
 calc=calculate();fit=calc['forearm_table_recalculation']
 assert fit['n']==24 and round(fit['slope'],2)==2.76 and round(fit['intercept'],1)==45.8 and round(fit['r'],1)==.8 and round(fit['residual_se'],1)==5.8
 assert [(s['n'],s['sum']) for s in calc['seed_table_summary']]==[(28,270),(28,443),(58,1268)]
 assert [(round(s['mean'],2),round(s['sample_sd'],2)) for s in calc['seed_table_summary']]==[(9.64,5.03),(15.82,6.76),(21.86,9.75)]
 assert F(2,30)!=F(2,60)
 assert round(100*1921/2014,1)==95.4 and round(100*155/3462,1)==4.5 and round(100*3307/3462,1)==95.5
 assert 100*(F(93,2014)-F(12,667))<3
 assert sum(sum(v) for v in calc['cart_leaf_counts'])==160 and sum(min(v) for v in calc['cart_leaf_counts'])==27 and F(27,160)*100==F(135,8)
 assert mean([0,1,1,2,2,2,3,5,6,8])==3 and mean([0,0,0,1,1,3,4,5,7,8])==2.9
 return calc

def guards():
 return [
  dict(kind='variance_and_coverage_guard',location='인쇄78–79 / PDF86–87',action='n−1 보정은 독립 동일분포·유한 분산 표본에서 분산의 불편 추정과 관련된다. 표준편차 자체가 불편하다는 뜻은 아니다. 평균±MAD/SD에는 일반적인 고정 포함률이 없고,MAD도 평균을 기준으로 하므로 이상값 영향이 전혀 없는 요약으로 설명하지 않는다.'),
  dict(kind='finite_simulation_zero_guard',location='인쇄80–84·87–88 / PDF88–92·95–96',action='0/100·0/200은 유한 모의실험에서 관측한0회다. 정확한 확률0이나 불가능의 증명이 아니다. 원문17/100·1/100도 난수 결과의 근사로 두며 정확한 이항 꼬리 확률로 바꾸어 표시하지 않는다.35/60은 반올림58%이고 학교 비복원 표집과 독립 동전의 근사 모형을 구별한다.'),
  dict(kind='interval_method_guard',location='인쇄82·91·111 / PDF90·99·119',action='2×표준오차와1.96×표준오차,개별 예측구간과 평균 반응 신뢰구간을 구별한다. 같은 조건에서n을늘릴때 폭이줄어드는 경향과 새 표본의 중심·비율까지 유지된다는 보장은 별개다. 원문 간이식161.7±11.6은150.1–173.3이고 같은 쪽 결론149.5–174.2와 다르다. 후자의 생성 방법은 명시되지 않아 임의로 하나를 정답으로 고치지 않는다.'),
  dict(kind='experimental_unit_and_missingness_guard',location='인쇄85–88 / PDF93–96',action='처리별 봉투 수는1·1·2이고 씨앗 수는30·30·60이다. 미발아2·2·2는 같은 비율이 아니며 동일 누락 수만으로 결측의 무편향을 증명하지 못한다. 봉투별 공유 조건·독립 반복·실제 배정 단위를 확인하기 전 씨앗114개를 모두 독립 실험 반복으로 삼은 인과·순열 해석을 전용하지 않는다. 자체 설계에서는 처리별 봉투의 반복·배정과 발아율/발아한 길이라는 대상량을 명시한다.'),
  dict(kind='regression_layout_and_generalization_guard',location='인쇄89–91 / PDF97–99',action='표7은 한 인쇄 행에 두 쌍이 나뉘어 총24쌍이다. 표의 상관·기울기·절편·잔차 표준오차는 전사 수치로 재계산해 반올림이 맞음을 확인했다.39–50cm는 실제 최소39.5·최대49.1을 둥글린 범위이며 밖의 값을 자동으로 내삽이라 하지 않는다. 학급 자료의 적합을 모든 고교생의 유효 예측구간으로 확대하지 않는다.'),
  dict(kind='conditional_percentage_arithmetic_guard',location='인쇄92–94 / PDF100–102',action='표8의도수로계산하면무낮잠열의비사건1921/2014는약95.4%로표9의94.4%와다르다. 전체사건155/3462는약4.5%,비사건3307/3462는약95.5%다.3–5회열의비사건389/411은약94.6%다.93/2014와12/667의차는약2.819퍼센트포인트로최소3이라는본문과맞지않는다. 표10의기대도수는원도수의주변합으로계산하며잘못된주변비율95.2%를쓰지않는다. 이산술대조는의료권고·인용원논문·원자료재검증이아니다.'),
  dict(kind='secondary_map_and_smoothing_guard',location='인쇄95–97 / PDF103–105',action='지역 수·지도 면적과 사람 수의 가중을 구별한다. 감소 지역이 지도에서 넓어도 전체 인구가 감소한다고 단정하지 않는다.12개월 평균에는 사용할 창·결측 처리·끝 처리·짝수 창의 표시 시점을 적는다. 미래 달을 쓰는 중심 평균은 그 당시 실시간 예측값이 아니다. 월별 감소의 원인을 생년 계산으로 확정하지 않는다.'),
  dict(kind='classification_table_tree_and_evaluation_guard',location='인쇄98–102 / PDF106–110',action='6.25g 규칙에서 실제자연81개중81개의분류성공과자연예측134개중정확81개는다르다. 그림19는본문과상하배치가다르고축mm와설명cm가맞지않는다. 그림20의재분기질량4.35와본문4.25도구별한다. 잎별오류4+1+1+11+3+7=27이고전체160으로나누면16.875%이지18%가아니다. 학습자료에서고른규칙의오류율을새자료성능으로전용하지않으며CART의세부최적화구현전체를확인한것이아니다.'),
  dict(kind='assessment_dotplot_and_design_guard',location='인쇄105–113 / PDF113–121',action='그림4의팀A점은[0,1,1,2,2,2,3,5,6,8]로평균3·MAD2다. 팀B점은[0,0,0,1,1,3,4,5,7,8]로평균2.9여서두팀평균3이라는표현을정확값으로전용하지않는다. 반올림의도는미확인이다. 히스토그램에서정확한개별평균을복원하거나자발적으로선택한두경주의차이를같은사람의효과로바꾸지않는다. 계산·해석·표집/배정·추천기준을따로판정한다.'),
  dict(kind='historical_assessment_and_reference_scope',location='인쇄105–106·115–116 / PDF113–114·123–124',action='시험구성·PISA예정연도·웹서비스소개는2020년의서술이며현행정보로옮기지않는다. 참고문헌의서지·주소를읽은것은각원연구·LOCUS원도구·STEW원활동·원자료·정오표를확인한것과다르다. A/B/C를한국고정학년이나자체진단규준으로승격하지않는다.')
 ]

def main():
 calc=verify();registry=load_registry();review=registry['sources'][SOURCE];ids={m[0] for m in MAPPINGS};existing={c['id'] for c in registry['claims']}
 if ids<=existing:
  assert {p['id'] for p in OBSERVATIONS}<={p['id'] for p in review['observations']}
  build_report();print('GAISE C and assessment reading remains current; no automatic refresh');return
 assert not ids&existing
 assert review['snapshot_file']==PRIOR_NOTES and review['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 assert hashlib.sha256((ROOT/'tmp/literature/GAISE_2020.pdf').read_bytes()).hexdigest()==SHA
 prior=copy.deepcopy(review);old_claims=copy.deepcopy([c for c in registry['claims'] if c['source_id']==SOURCE]);old_relations=copy.deepcopy(load_reviews()['records'])
 old_notes=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'));pages=json.loads((ROOT/'tmp/literature/GAISE_2020_pages.json').read_text(encoding='utf-8'))
 assert len(pages)==126 and 'Assessment' in pages[112]['text'] and 'References' in pages[122]['text']
 images=[]
 for p in NEW_VISUAL:
  path=ROOT/f'tmp/literature/GAISE_2020-p{p}.png';images.append(dict(pdf_page=p,local_temporary_file=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 notes=dict(source_id=SOURCE,source_url=URL,source_pdf_sha256=SHA,date='2026-11-06',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,
  previous_review=prior,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,pdf_pages_total=126,read_pdf_pages=list(range(1,127)),new_read_pdf_pages=NEW_TEXT,
  visually_reviewed_pages=old_notes['visually_reviewed_pages']+images,new_visually_reviewed_pages=images,source_corrections=old_notes['source_corrections']+guards(),source_numeric_checks=calc,
  official_asset_comparison=old_notes['official_asset_comparison'],
  reading_log=['기존 A/B·서문·도입의PDF3–78 텍스트 지정76쪽·선정33쪽 이미지 기록을 보존했다.',
   '이번에PDF79–111의Level C 목차·본문8예·요약,PDF113–121의평가소개·A4예/B5예/C4예,PDF123–124의참고문헌을 모두 읽었다. 빈112·122·125쪽의 추출 텍스트,표지1·126과 빈2쪽도 확인했다. 신규 확인 쪽은50쪽이다.',
   '선정41쪽의 전체 페이지 이미지를 직접 대조했다. 누적74쪽 이미지이며 표지1·126과빈2·125도 포함한다. 다른빈쪽은빈추출확인과이미지대조를구별한다.126쪽전체이미지를대조했다는집계가아니다.',
   '이제원문본문·평가예·참고문헌의텍스트전범위를읽었다. 수식·표·그림의선정이미지에서분모·잔차·조건·단위·오류율을확인했다. 원문수치의일부산술전사검산과자체7활동을별도계산했다. 인용연구의원자료분석·모든웹링크·도구화면실행을완료한것은아니다.'],
  unread_followups=['보고서 본문·평가예·참고문헌 자체의 미독 장은 없다. More4U·LOCUS/STEW 원도구·인용 원연구·원자료·정오표·수치 불일치의 작성 의도는 미확인이다.','원문 그림·표의 일부 산술 재계산은 원자료 생성·전체 연구 분석의 독립 재검증이 아니다. 현재 한국어 과제의 실제 반응·독립 검토·학생 검증은 추가하지 않았다.'],
  interpretation_limits=old_notes['interpretation_limits']+['본문 전범위 독해와 모든 원연구·부록 웹자산·원자료·개별 과제 효과의 확인을 구별한다. 원전의 일부 산술·표기·추론 적용 한계는 별도 기록하고 그대로 옮기지 않는다.'])
 (ROOT/NOTES).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 path=ROOT/'data/sources.json';sources=json.loads(path.read_text(encoding='utf-8'));b=next(s for s in sources if s['id']==SOURCE)
 b.update(review_scope='126쪽 PDF의 본문·평가 예·참고문헌 텍스트 전 범위를 읽고 표지·빈 쪽을 확인했다. 선정74쪽의 전체 페이지 이미지를 대조했다. 원연구·원자료·More4U·LOCUS/STEW 원도구·공식 정오표는 미확인.',next_review='기록한 수치·표기·추론 조건의 불일치를 원자료·인용 원연구·공식 정오표와 추가 대조하고,한국어 과제의 실제 반응·독립 검토를 확인한다. 원전 본문의 미독 장 대기는 해소했다.')
 review.update(snapshot_file=NOTES,snapshot_sha256=hashlib.sha256((ROOT/NOTES).read_bytes()).hexdigest(),bibliography_snapshot=digest(b),
  snapshot_history=prior.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=prior['date'],read_scope=prior['read_scope'])],
  read_scope='126쪽 PDF의 본문·평가 예·참고문헌 텍스트 전 범위,표지·빈 쪽 확인과 선정74쪽 이미지;인용 원연구·원자료·웹부록은 별도',
  method_note='A/B의 기존12주장·12관찰과 읽기 기록을 보존하고 C·평가의7주장·7가상 활동을 추가했다. 추정 분산·유한 모의실험·구간·실험 단위·결측·회귀·분류·탐구 평가의 적용 조건을 대조하고 자체 수치와 일부 원문 표를 재계산했다.',
  limits='원전 본문·평가 예·참고문헌은 모두 읽었지만126쪽 전부의 이미지 대조·모든 인용 원연구·원자료·More4U·원도구·공식 정오표 확인은 아니다. 원문의 산술·조건·그림 표기 불일치는 별도 기록하고 전용을 보류했다. PDF·페이지 이미지는 재배포하지 않는다.',
  editorial_action='누적19주장·19가상 관찰을 대응했다. 분산의 분모·모의실험0회·구간의 대상·실험 단위·결측·예측과 잔차·분류 평가 분모·결정 기준을 보완했다. 관계 승인·독립 검토·실제 학생 검증 수는 늘리지 않았다.',observations=prior['observations']+OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 path=ROOT/'data/content_review_queue.json';queue=json.loads(path.read_text(encoding='utf-8'));row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE)
 row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE]);path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 current=load_registry();assert old_claims==[c for c in current['claims'] if c['id'] in {v['id'] for v in old_claims}]
 assert load_reviews()['records']==old_relations
 build_report();print('Completed GAISE main-text scope: 7 new claims / 7 own observations; prior records preserved')

if __name__=='__main__':main()

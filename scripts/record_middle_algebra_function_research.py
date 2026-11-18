"""Scope expressions, natural exponents, inequalities and function references."""
from fractions import Fraction
from record_conic_representation_research import probe
from record_middle_number_system_research import amsi
from record_scoped_pdf_research import ROOT, record

DATE='2026-11-13'
CACHE=ROOT/'tmp/literature/middle-algebra-functions'
AE='AMSI_2011_ALGEBRAIC_EXPRESSIONS'
IL='AMSI_2011_NEGATIVE_INDEX_LAWS'
GR='NCETM_2021_GRAPHICAL_REPRESENTATIONS'
IQ='NCETM_2025_LINEAR_INEQUALITIES'
FN='NCETM_2025_EXPLORING_FUNCTIONS'
E,P,A,M,B,U,F,L,Q=[f'9수02-{i:02d}' for i in [1,8,9,10,11,12,14,17,21]]

def ncetm(year,title,stem,url,total,pages,visuals,scope,limit,supports):
 return dict(year=year,authors=['National Centre for Excellence in the Teaching of Mathematics'],
  title=title,url=url,pdf_url=url,stem=stem,total=total,pages=pages,visuals=visuals,
  scope=scope,limit=limit,supports=supports,student_outcome_study=False,
  design='교사 전문성 개발을 위한 개념·예시·토의 발문. 직접 복제하는 교과서 수업안과 구별.',
  sample='학생 표본 없음. 예상 난점과 가상 응답은 실제 학생의 반응 빈도가 아니다.')

SPECS={
 AE:amsi('Algebraic expressions',23,'7','amsi-algebraic-expressions-2011','Algebraic_expressions',
  '32e3f39bdaeb549eee128faa5cabe5b9eee1f59069ed900618c57d0c21c3faa4',22,
  [1,2,3,5,6,7,8,9,10,11,12,16,17,18],[6,8,9,11,16,18],
  '표지·서지와 문자의 역할, 말에서 식으로의 변환과 대입, 동류항·괄호·분수선 및 분배법칙의 지정 본문·그림을 대조했다.',
  '주로 음이 아닌 수를 대입하는 교사 가이드다. 문자의 맥락·허용값과 형식적 식을 구별한다. 6쪽의 대입값 30은 실제 계산 50과 달라 옮기지 않는다. 0 지수는 국내 중학교 추가 요구로 삼지 않는다.',
  ['문자의 수량·단위·허용값','괄호와 분수선의 범위 및 식의 값']),
 IL:amsi('Negatives and the index laws in algebra',24,'7–8','amsi-negative-index-laws-2011','Negative_and_the_Index_Laws',
  'a9e933b374f1220013390b586ff592bf7c285f7c20943d34b4b7d54a88330e5e',22,
  [1,2,3,4,8,9,11,12,13,14,15,16,17],[9,11,14,15,17],
  '부호를 포함한 항·동류항, 분배법칙, 자연수 지수의 인수 개수와 곱·거듭제곱 및 지정 몫 규칙을 대조했다.',
  '교사용 설명이다. 15쪽 odd/negative 문구와 17쪽 m<n인 몫 공식의 지수 방향을 구별한다. 자체 학생 과제는 자연수 지수와 다항식이 되는 몫에 한정하며 0·음·분수 지수를 도입하지 않는다.',
  ['부호를 보존한 동류항과 분배','인수 개수와 자연수 지수법칙','나눗셈의 0 아닌 제수 조건']),
 GR:ncetm(2021,'4.2 Graphical representations: Mastery Professional Development, KS3, ©2019, 2021',
  'ncetm-graphical-representations','https://www.ncetm.org.uk/media/s05nyur0/ncetm_ks3_cc_4_2.pdf',33,
  [1,2,3,6,7,8,9,10,13,18,19,24],[6,7,8,18,19,24],
  '교사용 목적·판권 연도와 좌표-식-그래프의 대응, 직선·수직선, 기울기와 절편, 이차함수 용어의 지정 부분을 읽고 수식·도식을 대조했다.',
  '원장의 2021은 마지막 인쇄 판권 연도이며 정확한 발행일을 확정하지 않는다. 수직선 x=a를 y의 x에 대한 함수로 쓰지 않는다. 원문의 바뀐 기울기 설명·그래프 표기와 빠진 이차항 계수 조건을 기록했다.',
  ['직선 위의 모든 해와 비정수 좌표','방정식 형태와 기울기·절편의 역할','이차함수의 형태와 계수 조건']),
 IQ:ncetm(2025,'9.1 Exploring linear equations and inequalities: Mastery Professional Development, KS4, ©2025',
  'ncetm-linear-inequalities','https://www.ncetm.org.uk/media/rp4bcrfw/ncetm_ks4_cc_9_1.pdf',32,
  [1,2,3,4,9],[1,3,9],
  '2025 표지·목적과 연결 개요, 일차방정식·부등식의 해와 수직선, 양변 변형과 음수 곱셈의 부등호 방향을 지정 부분에서 대조했다.',
  '교사 개발 자료이며 국내 자체 과제는 한 미지수의 일차부등식으로 한정한다. 두 변수의 영역·운동학·직교 기울기는 추가 요구로 삼지 않는다. 0개 또는 1개라는 연립방정식 개요를 모든 경우의 정리로 옮기지 않는다.',
  ['부등식 해의 범위와 경계','음수로 곱하거나 나눌 때의 방향과 적용 맥락']),
 FN:ncetm(2025,'9.4 Exploring functions: Mastery Professional Development, KS4, ©2025, selected definitions and examples',
  'ncetm-exploring-functions','https://www.ncetm.org.uk/media/tgnhs4se/ncetm_ks4_cc_9_4.pdf',37,
  [1,3,6,7,17,18,19,20,21,22],[6,18,20,21,22],
  '2025 표지와 함수 정의·입력 범위, 여러 입력과 같은 출력, 표현의 한계 및 x²·제곱근·수직선 검사 예시의 지정 부분을 대조했다.',
  '교사용 활동이다. 함수의 엄밀한 집합 용어·합성·역·지수함수·일반 변환은 이번 중학교의 추가 필수로 요구하지 않는다. x²의 0 경계와 정의역 밖 수직선, 실제 상황의 다른 조건을 명시한다.',
  ['허용 입력마다 하나인 출력','상수·다대일과 함수의 조건','x²의 0 경계와 수직선 검사의 범위']),
}
SPECS[AE]['title']='Algebraic expressions: TIMES Module 23, A guide for teachers, Year 7, June 2011'
SPECS[GR]['text_pages']=[1,2,3,7,8,9,10,13]
for sid,sha in [(GR,'bf9793b423ab24feb40e7be14558ae2574bb3d6ac724ff40a2dfbbcbe7d172fe'),
 (IQ,'446334bcf00319636722e9d832409597656ab51d15bd38304dfa302198784270'),
 (FN,'e179490b1e3f0bebc39c8f1e7f71b0d9b3d4d637d32b8ea89ccfec6ad8a1907e')]: SPECS[sid]['sha256']=sha

CLAIMS=[
 (AE,'AE11-01',[E],[5,6,7,9,11],
  '문자를 주어진 수·미지수·일반적인 수·연결된 수량 등 여러 역할로 사용하고, 말로 주어진 수량을 식으로 표현한 뒤 값을 대입하는 과제를 구별한다.',
  '같은 문자는 같은 맥락에서 같은 값을 나타낸다. 물건 개수의 음이 아닌 정수 조건과 형식적 식에 대입 가능한 수를 나누며 6쪽의 5(2²+3×2)=30은 정확한 값 50과 달라 정답으로 옮기지 않는다.'),
 (AE,'AE11-02',[E],[8,12,16,17,18],
  '괄호와 분수선이 계산 범위를 정하는 역할을 설명하고, 먼저 더한 뒤 나누는 식과 먼저 나눈 뒤 더하는 식을 구별해 대입한다.',
  '분수와 지수의 위아래 배치는 추출문만으로 판독하지 않았다. x²와 x/2, (x+5)/3과 x+5/3을 구별하며 조건이 없는 0 지수 표기를 이번 학생 과제에 도입하지 않는다.'),
 (IL,'IL11-01',[A],[8,9,11,12],
  '항의 부호를 함께 보존하고 문자 부분과 각 지수가 같은 동류항의 계수를 모으며, 괄호 앞 음수를 모든 항에 분배한 뒤 정리하도록 설명한다.',
  '합의 동류항 정리와 곱의 지수법칙은 다르다. 숫자 한 번 대입한 일치는 항등성의 증명이 아니며 교사 예시를 실제 학생 빈도로 해석하지 않는다.'),
 (IL,'IL11-02',[M],[11,12,17],
  '단항식을 괄호 안 모든 항에 부호까지 포함해 곱하고, 자연수 지수의 곱을 분배법칙과 함께 처리한 뒤 동류항을 모으는 예시를 제시한다.',
  '같은 제수로 항별 나누는 자체 과제는 분배법칙과 약분의 역방향 적용이다. 몫이 다항식인 경우에 한정하고 약분 뒤에도 원식의 제수가 0이 아니라는 조건을 보존한다.'),
 (IL,'IL11-03',[P,M],[12,13,14,15,16,17],
  '자연수 지수에서 같은 밑의 곱은 인수 개수를 합하고 거듭제곱의 거듭제곱은 곱하며, 곱의 거듭제곱은 계수와 각 인수에 함께 적용한다고 설명한다.',
  '나눗셈은 0 아닌 밑에서 약분해 설명하며 같은 지수의 몫은 1로 쓴다. 17쪽 m<n의 잘못된 지수 방향을 옮기지 않고 0·음·분수 지수를 추가로 요구하지 않는다. 15쪽의 odd는 음수의 홀수 거듭제곱이 음수라는 뜻과 구별한다.'),
 (GR,'GR21-01',[L],[2,3,7,8,9,10,13,18,19,24],
  '직선을 몇 개 정수 좌표만이 아니라 식을 만족하는 모든 좌표의 집합으로 보고, y에 대해 정리한 식과 다른 형태의 일차방정식을 오가며 기울기·절편의 역할을 확인하도록 한다.',
  'y의 계수가 0인 수직선과 수평선·상수함수를 구별한다. 기울기는 Δy/Δx이며 원문 8쪽의 역방향 설명과 18쪽 그림의 +2 표기를 그대로 옮기지 않는다. 문자 이름만으로 계수 역할을 판정하지 않는다.'),
 (GR,'GR21-02',[Q],[6,9],
  '자료는 ax²+bx+c 형태와 포물선 그래프를 이차함수의 표현으로 연결하고 직선 관계와 다른 그래프 형태를 비교하도록 제안한다.',
  '원문 용어표에는 a≠0이 빠져 있다. 자체 설명에서는 반드시 정리 후 이차항 계수가 0이 아닌지 확인한다. 두세 점을 잇는 것만으로 일반식이나 함수 유형을 확정하지 않는다.'),
 (IQ,'IQ25-01',[U],[3,9],
  '방정식의 하나인 해와 부등식의 해 범위를 수직선으로 대조하고, 양변에 같은 수를 더하거나 빼는 변형이 관계를 보존하는지 설명하도록 한다.',
  '실수 범위의 해와 개수 맥락의 정수 해를 구별한다. 원문의 두 변수 영역 활동을 국내 한 미지수 일차부등식의 필수 범위로 추가하지 않는다.'),
 (IQ,'IQ25-02',[B,U],[3,9],
  '일차부등식의 양변을 음수로 곱하거나 나눌 때 부등호 방향이 반대가 됨을 방정식의 변형과 구별하고 수직선·대입으로 확인하도록 설명한다.',
  '0으로 나누지 않으며 경계의 포함 여부를 보존한다. 특정 경계 한 값만 맞는 것과 전체 해의 범위가 맞는 것은 다르다. 설명 순서를 실제 학생의 유일한 학습 순서로 해석하지 않는다.'),
 (FN,'FN25-01',[F],[3,6,7,17,18,19],
  '함수는 허용한 각 입력에 출력이 하나로 정해지는 대응으로 설명하며, 다른 입력들이 같은 출력을 갖는 예와 입력-출력 기계 등 표현의 장단점을 비교한다.',
  '출력이 항상 변해야 하거나 함수가 꼭 일대일이어야 하는 것은 아니다. 실제 상황에서는 다른 조건을 고정한 모형인지 확인한다. 국내 자체 과제에서는 집합 용어·역·합성의 형식화를 필수로 요구하지 않는다.'),
 (FN,'FN25-02',[F,Q],[6,20],
  'x²의 좌표·표·그래프·식과 여러 성질 문장을 비교해, 표현이 보여 주는 정보와 함수 전체에 적용하는 성질을 나누어 보도록 제안한다.',
  '20쪽 나열 문장을 모두 참으로 복사하지 않는다. 실수 전체의 x²에서 출력 0의 입력은 0 하나이며 출력은 음이 아닌 수이므로 모두 양수라는 문구에는 0 예외가 있다. 유한한 표는 전체 그래프와 같지 않다.'),
 (FN,'FN25-03',[F,L],[21,22],
  '제곱근 그래프와 여러 비예를 비교하며, 같은 x에서 y가 두 값 나오는 관계와 한 값인 함수를 수직선 검사로 구별하도록 제안한다.',
  '각 허용 입력에서는 정확히 한 출력이고 정의역 밖에서는 교점이 없어도 된다. 모든 실수 x에서 꼭 한 번 만나야 한다고 확대하지 않는다. 수직선 x=c를 y의 x에 대한 함수로 처리하지 않는다.'),
]

OBSERVATIONS={
 AE:[
  probe('AE-P1',E,'한 묶음에 연필 n자루가 있고 각 묶음에 3자루씩 더 넣는다. 네 묶음의 총수를 식으로 나타내고 n=7일 때 구하라. n의 허용값도 설명하라.',
   '4(n+3)=4n+12이고 n=7이면 40자루다. n은 처음 연필 개수이므로 음이 아닌 정수다. 4n+3은 전체에 3자루만 더한 다른 상황이다.',
   '문자의 수량·단위, 각 묶음과 전체에 더하는 차이, 허용값을 확인한다.'),
  probe('AE-P2',E,'t=2일 때 5(t²+3t)의 값을 구하라. 30이라고 쓰인 답을 제곱과 괄호 안 계산으로 검산하라.',
   't²=4, 3t=6이므로 5(4+6)=50이다. 30은 이 식의 대입값이 아니다. 먼저 안쪽 합 10을 만든 뒤 바깥 5를 곱한다.',
   'AMSI 6쪽의 대입값 불일치를 정답으로 옮기지 않는 자체 검산 과제다.'),
  probe('AE-P3',E,'x=10일 때 (x+6)/4와 x+6/4를 각각 구하고 분수선·괄호가 정한 범위를 말하라.',
   '각각 4와 23/2=11.5다. 첫 식은 x와 6의 합 전체를 4로 나누며 둘째 식은 6만 4로 나눈 뒤 x를 더한다.',
   '분수선이 분자 전체를 묶는 역할과 계산 순서를 구별한다.'),
 ],
 IL:[
  probe('IL-P1',A,'(3x²−2x+5)−(x²+4x−1)을 정리하고, x=0에서만 맞는 답이면 충분한지 설명하라.',
   '3x²−2x+5−x²−4x+1=2x²−6x+6이다. x=0에서만 6이 같아도 2x²+6과 같은 오식을 배제할 수 없다. 괄호 전체의 부호와 동류항 계수로 설명해야 한다.',
   '뺄셈 부호의 분배, 동류항, 한 번 대입한 검산의 한계를 확인한다.'),
  probe('IL-P2',M,'−2x(3x−4)를 전개하고 (−6x²+8x)÷(−2x)를 간단히 하라. 두 식에 x=0을 넣는 것은 같은가?',
   '곱은 −6x²+8x이고 몫은 3x−4(x≠0)다. 곱은 x=0에서도 정의되지만 원래 나눗셈식은 제수 0으로 정의되지 않는다.',
   '모든 항의 부호와 약분 전 제수 조건을 보존한다. 다항식인 몫의 범위에 한정한 자체 역방향 과제다.'),
  probe('IL-P3',P,'(−2a²)³와 −2(a²)³를 각각 간단히 하라. 바깥 계수에도 같은 지수를 적용했는지 설명하라.',
   '각각 −8a⁶과 −2a⁶이다. 첫 식은 −2까지 세 번 곱하지만 둘째 식의 −2는 거듭제곱 밖에 남는다.',
   '거듭제곱의 밑 범위·계수와 지수의 역할을 구별한다.'),
  probe('IL-P4',P,'a⁵/a²와 a³/a³를 인수 약분으로 설명하고 a=0일 때도 같은지 판단하라. 지수법칙을 a³+a²에도 적용할 수 있는가?',
   'a≠0일 때 각각 a³과 1이다. a=0이면 원식의 분모가 0이므로 정의하지 않는다. a³+a²는 곱이 아니며 a=2이면 12로 a⁵=32와 다르다.',
   '같은 지수의 몫은 1로 설명하고 0 지수나 음의 지수를 새로 요구하지 않는다.'),
 ],
 GR:[
  probe('GR-P1',L,'3x+2y=7을 y에 대해 나타내고 x=1/3인 해를 구하라. 정수 좌표 몇 개만 찍으면 모든 해를 나타낸 것인가?',
   'y=−3x/2+7/2이고 해는 (1/3,3)이다. 모든 실수 x에 대응하는 해가 직선 전체를 이루며 정수 좌표만이 전부는 아니다.',
   '비정수 좌표의 검산과 방정식의 해 전체·직선 전체의 대응을 확인한다.'),
  probe('GR-P2',L,'2y=6x−4에서 기울기와 y절편을 구하라. y=cx+m으로 쓰면 어느 문자가 어떤 역할인가? x=2, y=2는 각각 y를 x의 일차함수로 나타내는가?',
   'y=3x−2이므로 기울기 3, y절편 −2다. y=cx+m에서는 c가 기울기이고 m이 y절편이다. x=2는 한 x에 여러 y라 함수가 아니며 y=2는 상수함수로 국내 일차함수의 기울기≠0 조건과 구별한다.',
   'y의 계수를 먼저 정리하고 문자 이름보다 수식의 역할을 확인한다.'),
  probe('GR-P3',Q,'y=3x², y=(x+1)²−x², y=0x²+2x+1이 각각 이차함수인지 설명하라. 정사각형 넓이 x²의 입력 범위와 형식적 함수 x²의 범위도 비교하라.',
   '첫 식만 이차함수다. 나머지는 2x+1로 정리돼 이차항이 없다. 실제 변 길이는 양수이고 형식적 함수 x²는 모든 실수 입력을 허용한다.',
   '정리 후 이차항 계수≠0과 상황의 허용값을 확인한다. 항 개수나 x²의 겉모양만으로 판단하지 않는다.'),
 ],
 IQ:[
  probe('IQ-P1',U,'5−3x<11을 풀고 경계 −2 및 그 양쪽 수 −3, −1로 확인하라.',
   '−3x<6에서 x>−2다. −2에서는 11<11이 거짓이고 −3에서는 14<11이 거짓, −1에서는 8<11이 참이다. 경계는 포함하지 않는다.',
   '음수로 나눌 때 방향을 바꾸고 경계와 양쪽의 참·거짓을 구별한다.'),
  probe('IQ-P2',U,'입장료 1200원과 체험 한 번당 700원이 든다. 5000원 이하로 낼 때 체험을 최대 몇 번 할 수 있는가? 입장만 해도 입장료는 낸다.',
   '음이 아닌 정수 n에 대해 1200+700n≤5000이므로 n≤38/7이다. 최대 5번이며 4700원이다. 6번이면 5400원으로 넘는다.',
   '실수 해의 경계와 횟수의 정수 조건·최대값 검산을 나눈다. 반올림으로 최대 횟수를 정하지 않는다.'),
  probe('IQ-P3',B,'x+4=10, x+4<10, x+4≤10의 해를 비교하라. 양변을 −2로 곱하면 각각 어떻게 쓰며 0으로 나눌 수 있는가?',
   '각각 x=6, x<6, x≤6이다. −2x−8=−20, −2x−8>−20, −2x−8≥−20으로 바뀐다. 등식은 등호를 유지하고 부등식은 방향을 바꾸며 0으로 나누지 않는다.',
   '하나인 해와 범위, 경계의 포함, 음수 곱셈의 변형을 구별한다.'),
 ],
 FN:[
  probe('FN-P1',F,'모든 실수 x에 f(x)=5를 대응시킨다. 입력이 달라도 출력이 같으면 함수가 아닌가? f(−2), f(0), f(2)를 구하라.',
   '각 값은 모두 5이며 함수다. 각 허용 입력의 출력이 하나면 되고 서로 다른 입력의 출력이 꼭 달라야 하는 것은 아니다.',
   '상수함수·다대일 대응과 일대일 조건을 구별한다. 함수라는 이유로 출력의 변화나 일차함수의 기울기≠0을 강제하지 않는다.'),
  probe('FN-P2',F,'실수 범위의 y=√x와 y²=x를 비교하라. x=4에서는 각각 어떤 출력이 가능하며 x=−1에서 교점이 없는 사실로 y=√x가 함수가 아니라고 할 수 있는가?',
   'y=√x는 x≥0에서 출력 하나이며 x=4에서는 2다. y²=x는 x=4에서 ±2로 y를 x의 함수로 나타내지 못한다. −1은 √x의 허용 입력이 아니므로 교점이 없어도 함수 조건에 어긋나지 않는다.',
   '허용 입력마다 정확히 한 출력인 것과 정의역 밖 교점 0개를 구별한다.'),
  probe('FN-P3',Q,'실수 전체의 f(x)=x²에서 출력은 모두 양수이고 모든 출력의 입력이 두 개라는 주장은 맞는가? 출력 0과 4를 각각 확인하라.',
   '출력 0의 입력은 0 하나이고 출력 4의 입력은 ±2다. 출력은 모두 0 이상이지만 모두 양수는 아니다. 양의 출력에 대한 설명을 0까지 확대하면 틀린다.',
   '원문 성질 목록을 그대로 참으로 옮기지 않고 0 경계를 확인하는 자체 과제다.'),
 ],
}

DETAILS={
 AE:dict(module=23,publication='June 2011',source_page_6_substitution_printed=30,correct_value=50,
  fractions_and_superscripts_visually_distinguished=True,zero_index_not_required=True),
 IL:dict(module=24,publication='June 2011',indices_in_student_probes='positive_integers_only',
  page_15_odd_should_be_negative=True,page_17_m_less_n_denominator_index_printed='m-n',
  correct_denominator_index='n-m',division_domain_preserved=True,zero_negative_fractional_indices_not_required=True),
 GR:dict(printed_copyright_years=[2019,2021],registry_year_is_last_printed_copyright=True,exact_publication_date_not_established=True,
  page_7_vertical_line_not_y_function=True,page_8_gradient_sentence_reversed=True,
  page_18_graph_label='y=3x+2',correct_table_and_graph_equation='y=3x-2',
  quadratic_nonzero_leading_coefficient_explicit_in_own_tasks=True),
 IQ:dict(printed_copyright_year=2025,student_probes_single_variable_only=True,negative_multiplier_reverses_order=True,
  page_3_zero_or_one_solutions_not_exhaustive=True,page_9_equation_region_label_not_imported=True,
  integer_context_distinguished_from_real_solution=True),
 FN:dict(printed_copyright_year=2025,domain_and_unique_output_distinguished=True,
  constant_functions_allowed=True,page_20_zero_output_counterexample=True,
  page_20_positive_range_requires_nonnegative=True,page_22_vertical_test_domain_limit=True,
  highest_degree_nonzero_coefficient_added_to_own_definition=True,
  real_contexts_require_fixed_other_conditions=True,advanced_function_topics_not_required=True),
}
CORRECTIONS={
 AE:'PDF 6쪽은 x=2에서 5(x²+3x)를 30으로 적지만 정확한 값은 50이다. 실제 판면에서 확인하고 자체 대입 과제에는 50과 계산 순서를 썼다. 8·9·16·18쪽에서 추출문에 평평하게 붙은 분수·지수를 판면으로 구별했다. 8쪽의 조건 없는 x⁰=1을 현재 중학교의 추가 요구로 복사하지 않는다.',
 IL:'인쇄 쪽은 PDF 쪽보다 3 작다. PDF 15쪽은 음수의 홀수 거듭제곱을 odd라고 쓰며 실제 값의 부호는 negative다. PDF 17쪽 m<n 분수의 분모 지수 m−n은 n−m이어야 한다. 원문을 조용히 고친 인용으로 만들지 않고 불일치를 기록했다. 자체 과제는 자연수 지수·다항식인 몫·0 아닌 제수에 한정한다.',
 GR:'인쇄 판권 2019·2021을 함께 보존했다. PDF 7쪽 x=a는 y의 x에 대한 함수가 아니다. 8쪽의 rate at which x changes with respect to y는 같은 문서 6쪽의 Δy/Δx 및 앞의 y 증가 질문과 반대다. 18쪽 표와 그림의 직선은 y=3x−2인데 그림 표기는 +2다. 용어표 이차함수에 빠진 a≠0도 자체 과제에 명시했다. 의도적 가상 오답과 이러한 문서 불일치를 구별한다.',
 IQ:'표지의 2025 판권을 확인했다. 3쪽 9.1.3.1의 연립일차방정식 해가 0 또는 1개라는 문구를 모든 경우의 정리로 옮기지 않는다. 같은 직선이면 무수히 많은 해가 있을 수 있다. 9쪽 9.1.2.3은 equation을 region으로 쓰지만 자체 과제에는 한 미지수 부등식의 해와 경계만 사용한다. 예상 난점은 실제 학생 통계가 아니다.',
 FN:'2025 판권과 지정 문항의 판면을 대조했다. 20쪽 x² 성질 목록의 각 출력에 여러 입력·모두 양수는 출력 0에서 맞지 않는다. 나열 문장을 모두 참인 정답으로 옮기지 않았다. 22쪽 수직선 검사는 정의역의 각 입력에서 하나이며 범위 밖에서는 교점이 없을 수 있다. 6쪽 선형·이차 함수 용어는 국내 일차·이차함수의 최고차항 계수≠0 조건을 따로 적용하고 고급 주제의 생략된 조건은 근거로 쓰지 않는다. 실제 생활의 단일 변수 모형은 다른 조건을 고정해야 한다.',
}
INTERPRETATIONS={
 ('REV-9수02-08-1','IL11-03'):('activity_context',
  '단항식의 자연수 지수를 반복된 인수의 개수로 설명하고 분배법칙을 이용한 다항식 곱의 각 항에 적용한다.',
  '이 풀이에 필요한 곱·자연수 지수에 한정한다. 다항식인 몫과 0 아닌 제수 조건을 유지하고 0·음·분수 지수를 추가 필수로 올리지 않는다.'),
 ('SEC_9수02-11_C03','IQ25-02'):('activity_context',
  '한 미지수 부등식의 양변을 음수로 곱하거나 나눌 때 부등호 방향이 반대가 되는 이유를 해의 범위와 연결한다.',
  '실수 해의 경계와 그 양쪽을 확인하고 개수 맥락에서는 정수 허용값을 다시 살핀다. 0으로 나누기는 허용하지 않는다.'),
 ('SEC_9수02-12_C02','IQ25-02'):('activity_context',
  '일차부등식 풀이에서 등식과 다른 방향 변화 및 경계의 포함 여부를 수직선·대입으로 대조한다.',
  '원자료의 두 변수 영역 활동이나 고급 함수 내용을 국내 한 미지수 과제의 필수 선수로 추가하지 않는다. 예상 난점과 실제 학생 응답은 다르다.'),
 ('REV-9수02-11-1','IQ25-02'):('inference_limit',
  '양변에 음수를 곱할 때에는 부등호 방향을 바꿔 원래와 같은 해의 범위를 유지해야 하지만 경계 한 값의 검산만으로 전체 풀이가 입증되지는 않는다.',
  '교사 자료는 이 변형의 수학적 이유를 제안한다. 수직선·직접 대입 등 다른 해결 경로를 배제하거나 모든 학생의 유일한 선행 숙달 순서를 실험으로 확정한 근거로 쓰지 않는다.'),
}

if __name__=='__main__':
 assert 4*(7+3)==40 and 5*(2**2+3*2)==50
 assert Fraction(10+6,4)==4 and 10+Fraction(6,4)==Fraction(23,2)
 for x in range(-4,5):
  assert (3*x*x-2*x+5)-(x*x+4*x-1)==2*x*x-6*x+6
  assert -2*x*(3*x-4)==-6*x*x+8*x
  assert (-2*x*x)**3==-8*x**6
  assert ((5-3*x<11)==(x>-2))
  if x: assert Fraction(x**5,x**2)==x**3 and Fraction(x**3,x**3)==1
 assert 3*Fraction(1,3)+2*3==7
 assert [n for n in range(10) if 1200+700*n<=5000]==list(range(6))
 record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,
  interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='중학교 문자·식·함수의 교사용 수학·표현 참고',
  detail_key='middle_algebra_function_review',roles={cid:'mathematical_explanation' for _,cid,*_ in CLAIMS})

"""Record selected official HTML readings from one College Algebra book."""
import hashlib
import json

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot

DATE='2026-11-13'
SOURCE='OPENSTAX_2021_COLLEGE_ALGEBRA_SELECTED'
URL='https://openstax.org/books/college-algebra-2e'
CACHE=ROOT/'tmp/literature/college-algebra-remaining'
C=lambda suffix:'10공수1-'+suffix
B=lambda suffix:'10기수1-'+suffix
CC,CL,CS=C('02-01'),C('02-05'),C('02-08')
BL=B('02-06');CI,BI=C('02-09'),B('02-07');CA,BA=C('02-10'),B('02-08')
CP,BP=C('03-01'),B('03-01');CR,BR=C('03-02'),B('03-02');CO,BO=C('03-03'),B('03-03')
CM,BM=C('04-01'),B('04-01');CX,BX=C('04-02'),B('04-02')
CG,BG='10공수2-01-05','10기수2-01-05'
SELECTION={'preface':[1,6,10],'complex':[5,7,8,9,10],'inequalities':[4,5,6,7,8],
           'systems':[1,4,5,6],'matrices':[1,3,4,5,6,7,8],'counting':[4,5,6,7]}
HTML_HASHES={
 'preface':'e202767265beaf314993fb52c6add1838edac022588db6b61d91ee8155f8e844',
 'complex':'3f8d1aea91fb4b08d23d36034d24b515c7a55c8ebe94632c9baf03898507c965',
 'inequalities':'87d841fa984c1d7805b4a4360ec9e9d5ef96c35d4011f35f8c89fb92bf13812a',
 'systems':'e4df6c54714b4fd72aa145fd6b49a242edcc863d4fd981ba5c5c43ad57f98160',
 'matrices':'50da8f6dd802effbd4b8cb2d7d7675f845a7f06cb3a3dc55497fc1804d397c1a',
 'counting':'7ce352ce29b5fb3e2895adbf24ad9af6acdc6c2145e58cde6d7d6fa6360815a0'}
SCOPE=('College Algebra 2e 한 권의 공식 웹본문 중 서문의 자원·개발·저자 블록, '
 '2.4절의 음수 제곱근·복소수 사칙연산·i의 거듭제곱, 2.7절의 구간·부등식 성질·일차 및 복합·절댓값 부등식, '
 '7.3절의 목표·도입·대입·소거, 7.5절의 목표·장비 표·행렬 합차·실수배·곱, '
 '9.5절의 합·곱의 법칙·서로 다른 대상의 순열·조합 블록을 읽었다. '
 '기록한 삽입 그림 14개를 시각 대조했다. 선택 블록 밖의 절 전체·연습 전체·책 전권·PDF 판면은 읽은 것으로 세지 않는다.')
LIMIT=('수학 교재의 설명과 예시이며 학생 표본·교수 효과·국내 학생 반응을 조사한 연구가 아니다. '
 '공통·기본수학은 선택·대체 분기다. 기본수학의 실수 계산·단순 부등식·한 절댓값과 두 사건의 간단한 경우의 수를 유지한다. '
 '행렬의 각 차원은 2 이하로 제한하며 역행렬·행렬식·일반 구조 법칙을 새 필수 평가로 추가하지 않는다. '
 '복소평면 블록, 비선형부등식·부분집합·중복 대상의 순열·후속 연습은 이번 읽기 범위가 아니다. '
 '자체 과제의 독립 검토와 실제 학생 응답 검증은 별도다.')

# IDs, domestic standards, selected source blocks, own support and inference limits.
CLAIMS=[
 ('CA11-01',[CC],['complex:5'],
  'i²=−1로 두고 복소수를 a+bi로 나타낸다. 실수부분은 a, 허수부분은 실수 계수 b이며 순허수와 0을 구별한다.',
  '원문 그림은 5+2i에서 2i를 imaginary part로 가리키지만 이 자료에서는 국내 정의에 맞춰 허수부분을 2로 쓴다. 기본수학에 복소수 연산·복소평면을 추가하지 않는다.'),
 ('CA11-02',[CC],['complex:7','complex:8'],
  '복소수 합·차는 실수 계수끼리 모으고 곱은 분배한 뒤 i²=−1로 정리한다. a+bi 형태의 두 계수가 같은지를 비교해 검산한다.',
  '실수의 분배법칙을 활용한 수학 설명이며 해당 방법의 학생 효과를 입증하지 않는다. 음수 제곱근에서 √a√b=√(ab)를 모든 실수 a,b로 확대하지 않는다.'),
 ('CA11-03',[CC],['complex:9','complex:10'],
  '0이 아닌 a+bi의 켤레를 분자·분모에 곱하면 분모가 a²+b²가 되어 나눗셈을 a+bi 꼴로 정리할 수 있다. i의 정수 거듭제곱은 주기 4로 확인한다.',
  '분모의 두 계수는 동시에 0이 아니면 된다. 각각 모두 0이 아니어야 한다는 원문의 제한이나 허수로 나눌 수 없다는 표현을 그대로 쓰지 않는다. i로도 나눌 수 있으며 0으로는 나눌 수 없다.'),
 ('CA11-04',[CL],['systems:5'],
  'y=f(x)인 이차함수와 비수직 직선 y=mx+n의 교점은 f(x)=mx+n의 실근과 대응한다. 차이인 이차식의 판별식으로 두 점·접점 한 점·교점 없음을 나눈다.',
  '각 함수의 판별식을 따로 적용하지 않는다. 수직 직선 x=c는 (c,f(c)) 한 점에서 만나므로 한 교점이면 언제나 접선이라는 일반화는 하지 않는다. 미분을 새 선수 요건으로 추가하지 않는다.'),
 ('CA11-05',[CS],['systems:5','systems:6'],
  '두 방정식을 동시에 만족하는 순서쌍을 구한다. 한 식이 일차인 간단한 연립에서는 대입하고, 인수분해 가능한 이차식에서는 경우를 나눈 뒤 원래 두 식에 모두 확인한다.',
  '인수분해 경우 나누기는 자체 변형 과제다. 원문의 원·타원 연립처럼 일반적인 두 이차곡선 문제를 공통수학1의 필수 범위로 옮기지 않는다. 한 식에만 맞는 순서쌍이나 나눗셈으로 잃은 가지를 해로 확정하지 않는다.'),
 ('CA11-06',[CG,BG],['systems:5'],
  '원과 직선의 교점은 두 식의 공통해이며 실수 교점 수는 0·1·2개다. 직선을 대입하거나 중심과 직선 사이의 거리를 반지름과 비교해 위치를 판단한다.',
  '거리 비교와 수직선 예는 자체 설명이며 원문 대입 예와 구별한다. 반지름은 양수이고 직선 방정식의 두 계수는 동시에 0이 아니어야 한다. 기본수학의 위치 판단과 공통수학의 활용 요구를 구별하며 원의 방정식 기준 전체까지 이 근거로 대응시키지 않는다.'),
 ('CA11-07',[BL],['inequalities:5','inequalities:6'],
  '일차부등식의 양변에 같은 수를 더하거나 양수를 곱하면 부등호 방향을 보존하고 음수를 곱하거나 나누면 방향을 바꾼다. 해는 조건을 만족하는 모든 실수 입력이다.',
  '0으로 나누거나 부호를 모르는 미지수로 곧바로 나누지 않는다. 같은 수를 더하는 것과 음수배를 혼동하지 않도록 한 단계씩 확인하며 한 답의 성공을 개념 전체의 검증으로 세지 않는다.'),
 ('CA11-08',[CI,BI],['inequalities:4','inequalities:7'],
  '연립일차부등식에서 두 조건을 모두 만족하는 해는 각 해집합의 교집합이다. 수직선·구간 표기로 끝점 포함과 공집합을 확인한다.',
  '또는으로 연결한 합집합과 모두 만족하는 교집합을 구별한다. 원문의 그림 3은 열린 두 끝점으로 실제 확인했으므로 엄격부등호와 맞으며 대체설명만으로 닫힌 점의 오류라고 기록하지 않는다.'),
 ('CA11-09',[CA,BA],['inequalities:8'],
  '절댓값은 0 이상인 거리다. k>0일 때 |u|≤k는 −k≤u≤k이고 |u|>k는 u<−k 또는 u>k다. k=0이나 음수인 경계는 먼저 절댓값의 범위로 판단한다.',
  '절댓값 방정식은 언제나 두 해라는 원문 설명을 일반화하지 않는다. 기본수학에서는 절댓값 기호가 하나인 간단한 일차부등식으로 제한하고 중첩·여러 절댓값을 요구하지 않는다.'),
 ('CA11-10',[CP,BP],['counting:4','counting:5'],
  '겹치지 않는 두 경우 중 하나를 고르는 수는 더하고, 두 단계에서 각각 하나씩 고르는 수는 가능한 쌍을 세어 곱한다. 선택 조건을 문장·표·나무그림에 일치시킨다.',
  '겹친 경우를 중복 합산하거나 선택하지 않는 경우를 빠뜨리지 않는다. 원문의 옷 예에서 스웨터를 입지 않아도 된다는 문장과 2가지로 곱한 계산의 차이를 명시한다. 기본수학 과제는 두 사건의 간단한 합·곱부터 다룬다.'),
 ('CA11-11',[CR,BR],['counting:6'],
  '서로 다른 n개에서 중복 없이 r개를 뽑아 순서를 정하면 각 단계의 남은 선택 수를 곱한다. 역할이나 자리가 다르면 같은 구성원이라도 다른 경우로 센다.',
  '0≤r≤n인 정수이고 대상이 서로 다르며 재선택하지 않는 조건이다. 중복·원순열·같은 대상의 순열은 이번 범위가 아니고 기본수학은 작은 수의 직접 열거와 계산을 비교한다.'),
 ('CA11-12',[CO,BO],['counting:7'],
  '순서 없이 서로 다른 r개를 고르면 같은 묶음의 r!가지 순서가 한 경우이므로 순열 수를 r!로 나눈다. 구성원 집합과 역할을 가진 순서쌍을 구별한다.',
  '재선택 없는 서로 다른 대상·정수 0≤r≤n의 조건을 유지한다. 같은 사람을 두 역할에 둘 수 있는 상황이나 중복조합을 같은 식으로 계산하지 않는다. 작은 열거 과제의 성공을 일반 발달 순서의 근거로 세지 않는다.'),
 ('CA11-13',[CM,BM],['matrices:3','matrices:4','matrices:6'],
  '행렬은 정해 둔 행·열의 의미에 따라 자료를 배열한다. m×n은 행 수×열 수이고 aᵢⱼ는 i행 j열이며 성분의 단위와 범주를 함께 읽는다.',
  '표를 옮길 때 행·열의 순서를 먼저 고정한다. 원문 MathML을 단순 평탄화한 토큰 순서로 행·열 오류를 단정하지 않는다. 자체 학생 과제는 각 차원이 2 이하이며 실제 기관의 관측 자료라고 표시하지 않는다.'),
 ('CA11-14',[CX,BX],['matrices:6','matrices:7'],
  '크기가 같은 두 행렬의 같은 위치 성분끼리 더하고 빼며, 실수배는 모든 성분에 같은 실수를 곱한다. 생활 자료라면 같은 범주·단위의 성분인지 함께 확인한다.',
  '크기가 다르면 같은 위치의 합·차로 정의할 수 없다. 2 이하 차원의 간단한 연산을 유지하고 원문의 3×3 예·일반 행렬 구조 법칙을 새 필수 평가로 확대하지 않는다.'),
 ('CA11-15',[CX,BX,CM,BM],['matrices:8'],
  '행렬곱은 앞 행렬의 열 수와 뒤 행렬의 행 수가 같을 때 행과 열의 대응 성분을 곱해 더한다. 결과의 크기와 자료 단위를 확인하고 곱의 순서를 유지한다.',
  '각 차원이 2 이하인 자체 과제다. AB와 BA는 다를 수 있지만 항상 다르다고 말하지 않는다. 역행렬·행렬식·전치의 일반 이론을 추가하지 않으며 자료의 비용 계산을 실제 조사나 교육 효과로 세지 않는다.'),
]

def task(id,codes,question,expected,interpretation):
 return dict(id=id,standard_codes=codes,question=question,expected=expected,interpretation=interpretation,student_validated=False)

OBSERVATIONS=[
 task('CA-P1',[CC],'z=5+2i의 실수부분·허수부분을 말하라. 2i가 허수부분이라는 그림 설명도 검토하라. 3과 −i는 a+bi로 어떻게 쓰는가?',
  '실수부분은 5, 허수부분은 2다. 2i는 허수항이며 계수 2와 구별한다. 3=3+0i, −i=0−1i다.',
  '국내 복소수 정의에 맞춘 계수 읽기다. 원문 그림과 정의 문장을 구별하며 복소평면·극형식을 요구하지 않는다.'),
 task('CA-P2',[CC],'(1+2i)+(3−i), (1+2i)−(3−i), (1+2i)(3−i)를 구하고 i²의 처리를 설명하라.',
  '각각 4+i, −2+3i, 5+5i다. 곱은 3−i+6i−2i²로 전개한 뒤 i²=−1을 사용한다.',
  '전체 뺄셈 부호와 분배·i² 대입을 따로 기록한다. 실제 학생에게 관찰한 오답 빈도는 없다.'),
 task('CA-P3',[CC],'(1+i)/(1−i)와 1/i를 a+bi 꼴로 구하라. 분모의 실수부분이 0이면 나눌 수 없다는 말이 맞는가?',
  '첫 값은 (1+i)²/2=i이고 1/i=−i다. 분모 자체가 0이 아니면 나눌 수 있으므로 i도 허용한다. a+bi의 허용 조건은 a²+b²>0이다.',
  '표준형으로 정리하는 방법과 나눗셈 가능 조건을 구별한다. 두 계수가 모두 0이 아니어야 한다는 과도한 제한을 사용하지 않는다.'),
 task('CA-P4',[CC],'i¹⁸을 구하고 1/(0+0i)의 정의 여부를 설명하라. √(−1)√(−1)=√1이라는 계산도 점검하라.',
  'i¹⁸=i²=−1이다. 0인 복소수로는 나눌 수 없다. 왼쪽 제곱근의 곱은 i²=−1이어서 1과 다르며 실수의 제곱근 곱 성질을 음수까지 그대로 확대할 수 없다.',
  '주기·0인 분모·제곱근 성질의 범위를 구별한다. 일반 복소 제곱근의 가지 이론은 추가하지 않는다.'),
 task('CA-P5',[CL],'y=x²와 y=2x+k의 교점 수를 실수 k로 분류하고 k=0의 좌표를 구하라. 수직선 x=2도 한 교점이므로 접선인가?',
  'x²−2x−k=0의 D=4(1+k)다. k>−1이면 두 점, k=−1이면 (1,1) 한 점, k<−1이면 없다. k=0이면 (0,0),(2,4)다. x=2는 (2,4) 한 점에서 만나지만 포물선의 접선은 아니다.',
  '차이 식의 실근·교점 순서쌍·비수직 조건을 확인한다. 수직선 반례는 교사용 일반화 점검이며 미분 계산을 요구하지 않는다.'),
 task('CA-P6',[CS],'x−y=−1, y=x²+1을 연립하여 풀고 두 원식에 확인하라. y=2일 때 x=−1도 둘째 식을 만족하므로 연립의 해인가?',
  '대입하면 x²−x=0이므로 (x,y)=(0,1),(1,2)다. (−1,2)는 x−y=−3이어서 첫째 식을 만족하지 않으므로 공통해가 아니다.',
  '대입 결과의 x와 복원한 y를 함께 원래 두 식에 확인한다. 한 식에서 가능한 값 전체를 연립의 해로 확정하지 않는다.'),
 task('CA-P7',[CS],'실수에서 x²−y²=0, xy=4를 풀어라. 첫 식에서 x=y만 남겨도 모든 해를 얻는지 설명하라.',
  '(x−y)(x+y)=0이므로 x=y 또는 x=−y다. x=y이면 x²=4로 (2,2),(−2,−2)이고 x=−y이면 −y²=4라 실수 해가 없다. 두 가지를 검토한 뒤 같은 부호의 두 해를 얻는다.',
  '한 식이 쉽게 인수분해되는 자체 확장이다. 일반적인 두 이차곡선·타원 연립을 필수 범위로 요구하지 않는다.'),
 task('CA-P8',[CG],'x²+y²=5, y=3x−5의 교점을 구하고 원·직선 위치를 판정하라. 중근과 두 서로 다른 교점은 어떻게 구별하는가?',
  '대입하면 10x²−30x+20=0이어서 x=1,2, 교점은 (1,−2),(2,1)이다. 서로 다른 두 점에서 만난다. 중근은 같은 x와 y의 한 점이며 서로 다른 두 점이 아니다.',
  '공통수학의 대입·위치 활용 과제다. 좌표를 원과 직선 두 식에 확인하고 반지름·실수 좌표 조건을 유지한다.'),
 task('CA-P9',[BG],'원 x²+y²=9와 직선 x=c의 교점 수를 c=0,3,4에서 판단하고 |c|와 3의 비교로 설명하라.',
  '차례로 두 점 (0,3),(0,−3), 한 점 (3,0), 교점 없음이다. |c|<3이면 두 점, |c|=3이면 접점 한 점, |c|>3이면 없다.',
  '기본수학의 간단한 위치 판단이다. 수직 직선도 포함하며 원의 한 교점 접촉 성질을 포물선의 모든 직선으로 일반화하지 않는다.'),
 task('CA-P10',[BL],'−2x+3<7을 풀어 x=−2와 0을 확인하라. −2로 나눌 때 부등호를 그대로 두어도 되는가?',
  '−2x<4에서 x>−2다. −2는 등호가 되므로 제외하고 0은 만족한다. 음수로 나누면 순서가 바뀌므로 부등호를 뒤집는다.',
  '양변의 같은 수 빼기와 음수 나누기를 따로 본다. 0으로 나누거나 부호를 모르는 미지수로 곧바로 나누는 풀이를 허용하지 않는다.'),
 task('CA-P11',[CI],'2x−1≥0과 3x+2<8을 동시에 만족하는 해를 구하라. 각 부등식의 해를 또는으로 합쳐도 되는가?',
  '각각 x≥1/2, x<2이므로 해는 1/2≤x<2다. 모두 만족해야 하므로 교집합이며 합집합으로 바꾸면 안 된다.',
  '공통수학에서 연립의 논리와 끝점 포함을 확인한다. 원문 그림의 열린 점과 엄격부등호를 일치시킨다.'),
 task('CA-P12',[BI],'x≥1과 x<3의 연립, x≥3과 x<1의 연립을 각각 수직선으로 설명하라.',
  '첫 해는 1≤x<3으로 1을 포함하고 3을 제외한다. 둘째는 두 조건을 동시에 만족하는 실수가 없어 공집합이다.',
  '기본수학의 간단한 연립일차부등식이다. 해가 없음을 0 하나가 해라는 뜻으로 바꾸지 않으며 교집합과 합집합을 구별한다.'),
 task('CA-P13',[CA],'|2x−1|≤3과 |2x−1|>3을 각각 풀어라. |2x−1|<0, |2x−1|≤0의 해도 비교하라.',
  '첫 해는 −1≤x≤2, 둘째는 x<−1 또는 x>2다. <0은 해가 없고 ≤0은 x=1/2 한 개다.',
  '사이의 두 조건은 모두, 바깥의 두 조건은 또는이다. 오른쪽 0의 경계를 먼저 판단하고 언제나 두 해라는 설명을 쓰지 않는다.'),
 task('CA-P14',[BA],'|x−1|≤2와 |x−1|>2를 풀고 |x−1|≤−1은 가능한지 설명하라.',
  '각각 −1≤x≤3, x<−1 또는 x>3이다. 절댓값은 0 이상이어서 ≤−1의 해는 없다.',
  '절댓값 기호가 하나인 기본수학의 간단한 일차부등식이다. 끝점 포함과 공집합을 확인하며 여러 절댓값의 복잡한 경우 나누기를 추가하지 않는다.'),
 task('CA-P15',[BP],'서로 다른 빨간 카드 2장과 파란 카드 3장 중 한 장을 고르는 경우와, 빨간 카드 한 장·파란 카드 한 장을 함께 고르는 경우를 세어라.',
  '한 장은 겹치지 않는 두 색의 경우여서 2+3=5다. 두 색에서 각각 한 장이면 가능한 쌍이 2×3=6이다.',
  '기본수학의 두 사건에서 합과 곱을 구별한다. 서로 다른 카드·각각 하나·동시 선택의 조건을 먼저 고정한다.'),
 task('CA-P16',[CP],'상의 4개와 스웨터 2개가 있다. 상의 한 개와 스웨터 한 개를 반드시 입는 경우와 스웨터를 안 입어도 되는 경우의 수를 비교하라.',
  '반드시 입으면 4×2=8이다. 안 입기도 하나의 선택이면 스웨터 단계가 3가지여서 4×3=12다. 조건 문장이 바뀌면 선택 수가 바뀐다.',
  '원문 선택 문장과 계산의 불일치를 변형한 자체 과제다. 없는 선택을 빠뜨리지 않고 합의 법칙에서는 서로 겹치는 경우를 중복 계산하지 않는다.'),
 task('CA-P17',[CR],'서로 다른 5명 중 회장 한 명·부회장 한 명을 겸임 없이 정하는 수를 구하라. 두 사람의 역할을 바꾸면 같은 경우인가?',
  '회장 5가지와 남은 부회장 4가지여서 20이다. A회장·B부회장과 B회장·A부회장은 역할이 달라 다른 경우다.',
  '역할의 순서와 중복 없는 선택을 확인한다. 같은 구성원 둘이라는 이유만으로 조합으로 세지 않는다.'),
 task('CA-P18',[BR],'A,B,C,D 네 사람 중 서로 다른 두 사람을 1번·2번 자리에 배치하는 수를 구하고 A가 1번인 경우를 모두 써라.',
  '4×3=12가지다. A가 1번이면 (A,B),(A,C),(A,D)의 3가지다. 같은 사람을 두 자리에 둘 수 없다.',
  '기본수학에서 작은 수의 열거와 곱을 비교한다. 순서쌍·재선택 불가 조건을 명시하고 공식 암기만으로 판정하지 않는다.'),
 task('CA-P19',[CO],'서로 다른 5명 중 역할 구분 없는 대표 2명을 고르는 수를 구하고 회장·부회장을 뽑는 수 20과 왜 다른지 설명하라.',
  '각 묶음이 두 순서로 중복되므로 20/2!=10이다. {A,B}와 {B,A}는 같은 대표 묶음이지만 회장·부회장의 두 배치는 다르다.',
  '순서를 세었다가 한 묶음의 순서 수로 나누는 이유를 확인한다. 같은 사람을 재선택하거나 역할이 다른 경우를 같은 조합으로 다루지 않는다.'),
 task('CA-P20',[BO],'A,B,C,D 중 순서 없이 두 명을 고르는 묶음을 모두 써라. 4×3=12로 답한 풀이를 점검하라.',
  '{A,B},{A,C},{A,D},{B,C},{B,D},{C,D}의 6개다. 12는 같은 묶음을 두 번씩 세므로 2로 나눈다.',
  '기본수학의 작은 조합에서 열거와 중복 제거를 비교한다. 중복조합·부분집합 전체의 수를 새 필수 과제로 추가하지 않는다.'),
 task('CA-P21',[CM],'가상 두 매장의 품목 A,B 재고를 Q=[[2,3],[4,1]]로 쓴다. 행은 매장, 열은 품목이다. 크기와 q₂₁의 의미를 말하고 행·열을 바꾸면 무엇이 달라지는가?',
  '크기는 2×2, q₂₁=4는 둘째 매장의 A 재고 4개다. 행·열의 역할을 바꾸면 같은 위치 성분의 의미가 달라지므로 표제를 함께 바꿔야 한다.',
  '행·열의 순서와 단위를 읽는 공통수학 과제다. 가상 자료이며 실제 매장의 조사·학생 응답 검증 결과가 아니다.'),
 task('CA-P22',[BM],'행은 월·화, 열은 사과·배인 판매수량 [[3,1],[2,4]]에서 1행 2열과 2행 1열을 읽고 행렬의 크기를 말하라.',
  '1행 2열은 월요일 배 1개, 2행 1열은 화요일 사과 2개이며 크기는 2×2다.',
  '기본수학에서 생활 표와 행렬의 의미를 연결한다. 숫자만 읽는 응답과 행·열 범주·단위를 함께 읽는 응답을 구별한다.'),
 task('CA-P23',[CX],'A=[[1,2],[3,4]], B=[[2,0],[1,−1]]일 때 A+B, A−B, 2A를 구하라. 2×1과 1×2 행렬은 성분 수가 같으므로 더할 수 있는가?',
  'A+B=[[3,2],[4,3]], A−B=[[−1,2],[2,5]], 2A=[[2,4],[6,8]]이다. 합·차는 행 수와 열 수가 각각 같아야 하므로 2×1과 1×2는 더할 수 없다.',
  '모든 성분에 실수배를 적용하고 전체 성분 개수와 행렬 크기를 구별한다. 2 이하 차원의 계산 범위다.'),
 task('CA-P24',[BX],'같은 품목·단위로 정리한 A=[[3,1],[2,4]], B=[[1,2],[0,1]]의 A+B, A−B, 2B를 구하라.',
  'A+B=[[4,3],[2,5]], A−B=[[2,−1],[2,3]], 2B=[[2,4],[0,2]]다. 차의 −1은 둘째 자료가 해당 위치에서 1개 더 많다는 뜻이다.',
  '기본수학의 간단한 성분 연산이다. 뺄셈 결과와 원래 수량 자료의 단위를 구별하고 일반 행렬 구조의 법칙 증명을 요구하지 않는다.'),
 task('CA-P25',[CM,CX],'Q=[[2,3],[4,1]]은 매장별 A,B 수량, P=[[100],[200]]는 품목별 원/개 가격이다. QP의 크기와 값을 구하라. P Q도 계산 가능한가?',
  '2×2와 2×1의 곱이므로 QP는 2×1이고 [[800],[600]]원이다. PQ는 안쪽 차원 1과 2가 달라 정의되지 않는다.',
  '행과 열의 대응·합산·결과 단위·곱 가능 조건을 함께 확인한다. 양쪽 행렬의 각 차원은 2 이하이며 원문 3개 품목의 장비 예를 그대로 요구하지 않는다.'),
 task('CA-P26',[BM,BX],'A=[[1,1],[0,1]], B=[[1,0],[1,1]]의 AB와 BA를 구하라. 단위행렬 I=[[1,0],[0,1]]도 사용해 곱의 순서를 바꾸면 항상 값이 다르다는 말을 검토하라.',
  'AB=[[2,1],[1,1]], BA=[[1,1],[1,2]]로 이 경우는 다르다. AI=IA=A이므로 순서를 바꿔도 같은 경우도 있다.',
  '2×2의 직접 계산으로 다를 수 있음과 항상 다름을 구별한다. 단위행렬은 계산 반례에만 사용하며 역행렬·일반 구조 법칙을 필수 평가로 확대하지 않는다.'),
]

def candidate_pairs(relations):
 return {(r['id'],cid):r for r in relations for cid,codes,*_ in CLAIMS
         if all(r[k].startswith('standard:') for k in ('from','to'))
         and {r[k][9:] for k in ('from','to')}<=set(codes)}

# Filled after reading the existing relation's own rationale and conditions.
INTERPRETATIONS={
 ('SEC_10공수1-04-02_C03','CA11-15'):('activity_context','수량 표의 행·열 의미와 가격의 품목 순서를 맞춰 대응 곱의 합을 매출로 해석한다.','곱의 안쪽 크기·상품 순서·원/개 단위를 함께 확인한다. 각 차원 2 이하이며 실제 매장 조사나 일반 구조 법칙의 검증이 아니다.'),
 ('SEC_10기수1-02-07_C03','CA11-08'):('activity_context','두 일차부등식의 공통해를 교집합으로 구하고 원래 두 조건으로 끝점 포함을 확인하는 공통 원리를 비교한다.','그리고와 또는를 구별한다. 기본·공통의 선택 분기를 순차 이수로 해석하지 않는다.'),
 ('SEC_10기수1-02-08_C03','CA11-09'):('activity_context','한 절댓값의 거리 조건에서 사이 구간의 동시 만족과 바깥 구간의 택일을 비교한다.','오른쪽이 0·음수이면 비음수 범위를 먼저 쓴다. 기본수학에 여러 절댓값이나 중첩 절댓값을 추가하지 않는다.'),
 ('SEC_10기수1-03-01_C04','CA11-10'):('activity_context','서로 겹치지 않는 택일에는 합을, 각 단계의 선택 수가 일정한 쌍에는 곱을 쓰는 원리를 비교한다.','뒤 선택 수가 달라지면 가지별로 세어 더한다. 확률적 독립과 경우의 수 곱의 법칙을 동일시하지 않고 기본수학은 두 사건의 간단한 상황을 유지한다.'),
 ('SEC_10기수1-03-02_C03','CA11-11'):('activity_context','회장·부회장의 다른 역할에 중복 없이 배치하면 4명은 12가지, 5명은 20가지임을 작은 열거와 비교한다.','겸임 허용이면 다른 모형이다. 순서 있는 선택이라는 공통 원리를 학생의 유일한 발달 순서로 해석하지 않는다.'),
 ('SEC_10기수1-03-03_C03','CA11-12'):('activity_context','역할 없는 두 대표의 같은 묶음이 정확히 두 순서로 세어짐을 확인해 4명 중 6개·5명 중 10개를 얻는다.','역할을 부여하면 서로 다른 순서가 되어 2로 나누지 않는다. 중복 없는 서로 다른 대상이라는 조건을 유지한다.'),
 ('SEC_10기수1-04-01_C04','CA11-13'):('activity_context','날짜×품목과 매장×품목의 표에서 같은 a₂₁=4도 행의 대상에 따라 뜻이 달라짐을 비교한다.','행·열 제목과 순서·단위를 함께 보존하며 가상 자료를 실제 조사로 표시하지 않는다. 큰 차원 행렬을 필수로 추가하지 않는다.'),
 ('SEC_10기수1-04-01_C04','CA11-15'):('inference_limit','곱에서 대응할 품목의 순서를 지키려면 먼저 행·열 자료의 의미가 명시되어야 함을 이 자료 경로에서 확인한다.','교재의 곱 설명이 모든 행렬 정의 활동에 곱셈이 필수라는 뜻은 아니다. 두 기준의 생활 표 비교를 역행렬·전치 이론의 선행으로 확대하지 않는다.'),
 ('SEC_10기수1-04-02_C03','CA11-14'):('activity_context','같은 크기·같은 자료 역할의 성분별 합차와 모든 성분의 실수배를 두 과목의 작은 행렬에서 비교한다.','덧셈·실수배와 행렬곱을 구별한다. 기본수학의 간단한 연산에서 일반 행렬 구조 법칙 증명을 요구하지 않는다.'),
 ('SEC_10기수1-04-02_C03','CA11-15'):('activity_context','Q=[[2,3],[4,1]]과 가격 [[100],[200]]의 곱 [[800],[600]]에서 품목 순서·원 단위를 확인한다.','가격의 행 순서만 뒤집으면 다른 대응이다. 각 차원 2 이하의 곱이며 수량과 비용·성분별 곱을 혼동하지 않는다.'),
 ('SEC_10기수2-01-05_C04','CA11-06'):('activity_context','원 중심과 같은 직선 사이 거리가 같아도 비교할 반지름이 다르면 접함과 두 교점이 달라짐을 확인한다.','거리와 반지름은 비음수이며 반지름은 양수다. 기본수학의 위치 판단과 공통수학의 활용 요구를 구별한다.'),
 ('REV-10공수1-04-02-1','CA11-15'):('activity_context','자료의 성분 의미를 유지해 수량의 열과 가격의 행을 대응시키는 곱의 합을 설명한다.','크기가 맞아도 품목 순서가 다르면 매출 해석이 맞지 않는다. 수량 표의 해석이 모든 수치 행렬 계산의 필수 경험이라는 뜻은 아니다.'),
 ('REV-10기수1-02-07-1','CA11-08'):('inference_limit','연립일차부등식의 교집합 원리는 두 과목에서 비교할 수 있으나 교재 설명은 선택 분기의 이수 순서를 정하지 않는다.','기본·공통 과목의 범위와 난도를 유지한다. 교수 효과·독립 검토·실제 학생 검증으로 세지 않는다.'),
 ('REV-10기수1-02-08-1','CA11-09'):('inference_limit','거리의 안쪽·바깥쪽과 0·음수 경계는 비교 가능한 공통 원리다.','기본수학은 한 절댓값의 간단한 일차부등식이다. 공통수학의 모든 형태를 필수로 옮기거나 두 과목을 순차 이수로 배열하지 않는다.'),
 ('REV-10기수1-03-01-1','CA11-10'):('inference_limit','택일·단계별 쌍의 구분은 비교할 수 있으나 문장의 선택 조건을 먼저 확인해야 한다.','기본수학의 두 사건 범위를 유지한다. 교재의 다단계 의복 예나 서술 순서를 모든 학생의 필수 선행 숙달로 옮기지 않는다.'),
 ('REV-10기수1-03-02-1','CA11-11'):('inference_limit','중복 없이 다른 역할에 배치한다는 공통 구조를 기본·공통 과목의 작은 과제로 비교한다.','같은 대상의 순열·중복·원순열을 이번 근거로 추가하지 않는다. 평행한 대체 분기를 필수 이수 순서로 바꾸지 않는다.'),
 ('REV-10기수1-03-03-1','CA11-12'):('inference_limit','한 묶음의 순서 중복을 제거하는 조합의 원리를 서로 다른 과제 크기에서 비교한다.','서로 다른 대상·재선택 없음·역할 없음을 먼저 명시한다. 기본수학을 공통수학의 필수 선수로 만들지 않는다.'),
 ('REV-10기수1-04-01-1','CA11-13'):('inference_limit','행·열의 범주와 순서·단위를 지정해 성분을 읽는 공통 원리를 비교한다.','날짜와 매장처럼 자료 대상의 차이를 보존한다. 수학 교재가 두 선택 분기의 동일 난도나 선후 이수를 검증한 것은 아니다.'),
 ('REV-10기수1-04-01-1','CA11-15'):('inference_limit','곱을 해석하는 자체 자료 경로에서 행·열의 대응을 확인하되 정의 기준의 전체 범위와 구별한다.','행렬 자료를 읽는 모든 활동에 곱셈을 추가하지 않는다. 각 차원 2 이하의 자체 과제이며 전치·역행렬 이론을 요구하지 않는다.'),
 ('REV-10기수1-04-02-1','CA11-14'):('inference_limit','같은 위치 합차와 실수배라는 공통 계산을 기본·공통의 간단한 행렬에서 비교한다.','교재의 3×3 계산이나 일반 대수 구조 법칙을 기본수학의 새 필수로 올리지 않는다. 선택 분기의 선후 이수 근거가 아니다.'),
 ('REV-10기수1-04-02-1','CA11-15'):('inference_limit','행과 열의 곱합·안쪽 차원이라는 공통 원리는 비교할 수 있지만 두 과목의 이수 관계를 뜻하지 않는다.','2 이하 차원의 계산을 유지하고 AB와 BA는 다를 수 있음과 항상 다름을 구별한다. 실제 학생 수행·교수 효과는 조사하지 않았다.'),
 ('REV-10기수2-01-05-1','CA11-06'):('inference_limit','원의 실수 교점 수와 중심 거리·반지름의 비교는 두 과목에서 공유할 수 있는 수학적 설명이다.','기본수학의 위치 판단과 공통수학의 문제 활용을 구별한다. 원의 방정식 전체 기준·학습 순서·효과의 검증으로 세지 않는다.'),
 ('HC-common-matrix','CA11-15'):('inference_limit','행·열 의미를 유지하는 표 경로에서 대응 곱의 합과 안쪽 차원은 계산을 정당화한다.','수치 행렬 계산에서 출발하는 대안도 있다. 표 해석을 모든 학생의 보편적 선행 경험으로 정하거나 교재를 필수 선수성의 실증으로 쓰지 않는다.'),
 ('HC-basic-matrix','CA11-15'):('inference_limit','기본수학의 간단한 표 경로에서 같은 품목끼리 대응해 곱을 합하고 단위를 해석한다.','각 차원 2 이하로 제한한다. 표 자료를 먼저 다루는 교수 순서나 모든 학생의 선행 숙달·실제 효과를 검증한 것은 아니다.'),
}

def main():
 registry=load_registry()
 if SOURCE in registry['sources']:
  assert {c[0] for c in CLAIMS}<={c['id'] for c in registry['claims']}
  build_report();print('Selected College Algebra mapping already recorded');return
 bibliography=load(ROOT/'data/sources.json');queue=load(ROOT/'data/content_review_queue.json')
 assert SOURCE not in {b['id'] for b in bibliography}
 manifest=load(CACHE/'html-manifest-20261113.json')
 assert len(manifest)==6 and {a['key'] for a in manifest}==SELECTION.keys()
 for asset in manifest:
  key=asset['key'];assert sha(CACHE/f'{key}.html')==asset['sha256']==HTML_HASHES[key]
  blocks=load(CACHE/f'{key}.blocks.json')
  selected=[b for b in blocks if b['index'] in SELECTION[key]]
  assert len(selected)==len(SELECTION[key]) and all(b['text'].strip() for b in selected)
  asset['selected_blocks']=[dict(index=b['index'],element_id=b.get('id'),normalized_text_sha256=hashlib.sha256(b['text'].encode()).hexdigest()) for b in selected]
 images=load(CACHE/'selected-images-20261113.json');assert len(images)==14
 for asset in images:
  assert sha(CACHE/asset['file'])==asset['sha256']
  assert asset['page_url'] in {a['url'] for a in manifest}
  assert asset['status']==200 and asset['redistributed'] is False
 source_fields=dict(source_asset_kind='publisher_html',source_asset_sha256=digest(manifest),html_read_manifest=manifest)
 empirical=dict(design='수학 교재의 정의·성질·풀이·예시 대조',sample_description='해당 없음: 학생 표본 연구가 아님',
  inference_limit=LIMIT,student_outcome_study=False,causal_effect_established=False,local_effect_tested=False)
 entry=dict(id=SOURCE,year=2021,publication_date='2021-12-21',url=URL,title='College Algebra 2e — selected sections 2.4, 2.7, 7.3, 7.5, 9.5',
  authors=['Jay Abramson','OpenStax contributing authors'],kind='공통·기본수학의 복소수·부등식·경우의 수·행렬 수학 참고',
  review_scope=SCOPE,does_not_establish=LIMIT,supports=['복소수 사칙연산과 조건','단순 연립·위치와 부등식','합·곱·순열·조합의 선택 조건','2 이하 차원의 행렬 자료·연산'],
  next_review='선택 블록 밖 본문·연습·변경 정오표, 독립 검토와 실제 학생 응답은 후속 범위다.')
 note=f'data/literature_evidence/{SOURCE}_review_notes.json'
 write(ROOT/note,dict(source_id=SOURCE,source_url=URL,**source_fields,date=DATE,reviewer='Codex',read_scope=SCOPE,empirical_scope=empirical,
  hash_scope='source_asset_sha256는 선택 블록 메타데이터를 포함한 순서 있는 HTML manifest의 digest이며 PDF나 단일 HTML 파일의 해시가 아니다. 각 원문 HTML 해시는 manifest에 별도 보존한다.',
  observed_image_assets=images,source_asset_redistributed=False,contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,
  pdf_download=dict(url='https://assets.openstax.org/oscms-prodcms/media/documents/College-Algebra-2e-WEB.pdf',http_status=403,binary_obtained=False),
  reading_log=[SCOPE,'본문 블록과 MathML 행·열을 대조하고 삽입 그림 14개를 직접 읽었다. 평탄화로 반복·재배열된 수식 토큰을 원문의 수학 오류로 세지 않았다.',
   '발행일은 공식 HTML의 citation_date 및 publish_date에서 2021-12-21로 확인했다. 현재 서문에 표시된 웹 라이선스는 CC BY-NC-SA 4.0이다. 원문·삽입 자산은 재배포하지 않고 자체 기록만 보존한다.',
   '7.3절의 원·타원 소거는 교사 참고로 읽되 국내 간단한 연립 범위로 옮기지 않았다. 비선형부등식·부분집합·같은 대상의 순열 블록과 외부 매체·연습 전체는 읽지 않았다.'],
  source_corrections=[
   dict(location='2.4절 복소수 도식',observation='5+2i의 2i를 imaginary part로 지시한다.',action='국내 정의의 허수부분은 실수 계수 2로 명확히 썼다.'),
   dict(location='2.4절 나눗셈',observation='허수로 나눌 수 없다는 설명과 분모 두 계수가 각각 0이 아니어야 한다는 조건이 지나치게 제한적이다.',action='0이 아닌 복소수면 허용하고 켤레 곱은 표준형 정리 방법으로 구별했다.'),
   dict(location='2.7절 절댓값',observation='절댓값 방정식은 언제나 두 해라는 서술은 오른쪽이 0·음수인 경우에는 성립하지 않는다.',action='자체 과제에서 0·음수 경계를 구별했다.'),
   dict(location='2.7절 그림 3',observation='실제 그림은 −4와 5/6의 열린 점으로 본문의 엄격부등호와 일치한다.',action='대체설명을 닫힌 점이라고 과해석해 오류를 만들지 않았다.'),
   dict(location='7.3절 포물선과 직선',observation='한 교점이면 접선이라는 설명에는 비수직 직선 조건이 필요하다.',action='x=c 수직선의 한 교점을 자체 반례로 구별했다.'),
   dict(location='9.5절 옷 선택 예',observation='스웨터를 입을지 선택한다는 문장과 2벌만 곱한 계산은 안 입는 선택의 포함 여부가 다르다.',action='반드시 한 벌·안 입어도 됨을 분리해 두 선택 수를 계산했다.'),
   dict(location='9.5절 그림 1 및 7.5절 행렬 MathML',observation='기기 그림은 3+5=8이고 본문과 맞는다. MathML의 중첩 열 배열을 평탄화하면 행·열 순서를 오독할 수 있다.',action='그림 대체설명의 기기 수와 실제 그림을 구별하고, 장비 행렬 방향을 평탄화 토큰만으로 오류라고 단정하지 않았다.')],
  domestic_scope=dict(basic_complex_arithmetic_added=False,basic_absolute_value_signs=1,basic_counting_two_events=True,matrix_max_dimension=2,
   common_basic_parallel_alternatives=True,nonlinear_inequalities_added=False,circle_equation_standard_mapped=False)))
 registry['sources'][SOURCE]=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date=DATE,snapshot_kind='authored_review_notes',
  **source_fields,snapshot_file=note,snapshot_sha256=sha(ROOT/note),redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(entry),
  display=dict(title=entry['title'],url=URL,authors_year='Jay Abramson 외, OpenStax, 2021'),read_scope=SCOPE,limits=LIMIT,empirical_scope=empirical,
  scope_note='한 책의 지정 블록 읽기와 삽입 그림 확인이다. 다섯 절을 독립된 다섯 출처로 세지 않는다.',
  method_note='공식 HTML의 지정 본문·수식·표 및 삽입 그림을 실제 대조했다. PDF 다운로드 403으로 PDF 판면을 읽지 않았다.',
  editorial_action='남은 공통·기본수학1 및 원·직선 위치 기준에 근거와 자체 과제를 보완했다. 독립·학생 검증 완료로 표시하지 않는다.',
  independent_review=False,student_validated=False,observations=OBSERVATIONS)
 new={}
 for cid,codes,locations,support,limit in CLAIMS:
  loc=[]
  for ref in locations:
   key,index=ref.split(':');asset=next(a for a in manifest if a['key']==key)
   block=next(b for b in asset['selected_blocks'] if b['index']==int(index))
   loc.append(asset['url']+(('#'+block['element_id']) if block['element_id'] else f' [selected block {index}]'))
  new[cid]=dict(id=cid,source_id=SOURCE,role='mathematical_explanation',empirical_scope=empirical,standard_codes=codes,locations=loc,support=support,
   does_not_establish=limit,independent_review=False,student_validated=False,target_snapshots={f'revision:{c}':digest(target_value(f'revision:{c}')) for c in codes})
 relations=load(ROOT/'data/revised_relations.json')['relations'];pairs=candidate_pairs(relations)
 assert pairs.keys()==INTERPRETATIONS.keys(),sorted(pairs)
 reviewed=load(ROOT/FILE)
 for (rid,cid),(role,finding,limit) in INTERPRETATIONS.items():
  reviewed['records'].append(dict(relation_id=rid,claim_id=cid,role=role,finding=finding,limit=limit,relation_snapshot=relation_snapshot(pairs[rid,cid]),
   claim_snapshot=claim_snapshot(new[cid],registry['sources'][SOURCE])))
 registry['claims'].extend(new.values());bibliography.append(entry)
 queue['literature_review'].append(dict(source=entry,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_evidence_fields=entry['supports'],claim_ids=list(new)))
 apply_literature_context(relations,registry,registry=reviewed)
 for filename,value in [('data/sources.json',bibliography),('data/content_review_queue.json',queue),('data/literature_claim_reviews.json',registry),(FILE,reviewed)]:write(ROOT/filename,value)
 build_report();print(json.dumps(dict(newSources=1,newClaims=len(new),newTasks=len(OBSERVATIONS),newRelationEntries=len(pairs)),ensure_ascii=False))

if __name__=='__main__':main()

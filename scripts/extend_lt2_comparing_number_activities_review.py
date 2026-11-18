"""Record the reviewed LT2 English activity pages on comparing and ordering number."""
import copy
from fractions import Fraction
from urllib.parse import urljoin, urlparse

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_composing_number_assets_review_notes.json'
PRIOR_SHA = 'c4a407cc99668e7c22682028bd64c8a4a827a48ffc554a3fc65369e45c33b9f9'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_comparing_number_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-comparing-number-activities'
SCOPE = (
    '수량 비교·순서 수준에 연결된 영어 활동 안내 63개를 대조했다. '
    '누적 공개 HTML은 690개이며, 활동·교사자료 목록 824개 중 본문 440개를 확인했고 384개가 남았다.'
)
LIMITS = (
    '새 연결 PDF 8개와 삽입 이미지 88개 URL은 후속 검토 범위다. '
    '앞서 확인한 LT2 PDF 81개 URL과 이미지 526개 URL, 외부 스캔의 해당 10쪽은 이전 확인 범위를 유지한다. '
    '영상·인용 연구·번역 동등성, 독립 검토·학생 응답과 효과 검증은 별도다.'
)

READING = '''
build-stairs--whats-the-missing-step|1~5층 계단에서 탑 하나를 뺀다. 빠진 탑에 필요한 블록 수와 탑을 놓을 위치를 구별한다.
build-stairs-serial-orderer-to-6comparing-number|수준 이름과 달리 절차는 1~10개 블록의 탑을 준비한다. 정렬 전후에 몇 번째 탑인지와 블록이 몇 개인지를 따로 묻는다.
chip-flip-century|주황 판의 31~90부터 보라 판의 171~230까지 범위를 구별한다. 같은 거리의 빈칸이 여럿이면 선택 기준을 정하며, 행과 열의 변화는 판을 확인한 뒤 적용한다.
clothesline-number|카드를 뽑아 크기 순서대로 끼우고 양말 카드가 나오면 다시 시작한다. 놀이의 초기화와 이미 정한 수의 순서를 구별한다.
clothesline-to-10-mental-number-line-to-10|걸린 수의 순서를 맞추는 것과 두 수 사이의 같은 단위 간격을 표현하는 것을 따로 확인한다.
compare-snapshots-similar-items|접시의 3개와 잠깐 보여 준 4개는 같은 개수가 아니다. 잠깐 본 판단과 다시 세어 확인한 답을 구별한다.
comparing-blocks|블록 네 개씩 쌓은 두 탑을 비교한다. 같다는 말의 기준이 블록 개수인지, 높이·색·모양인지 정한다.
comparing-by-matching-matching-comparer|곰마다 그릇을 하나씩 놓고 남는 그릇이 있는지 살핀다. 준비한 전체와 실제 나눠 준 수를 따로 센다.
comparing-quantities|장난감·걸음의 개수와 길이·들이·시간의 크기를 구별한다. 비교할 속성과 기준을 먼저 정한다.
comparing-snapshots-counting-comparer-same-size|3개와 5개를 짧게 보고 비교한 뒤 다시 보여 주고 센다. 처음의 비교 판단과 정확한 수의 확인을 나눠 기록한다.
crack-the-code|숫자판의 가린 칸을 주변에 보이는 수로 찾는다. 인접 칸의 변화는 판에서 확인하며 그림의 물리적 방향만으로 정하지 않는다.
crowded-room|0~5 카드를 보여 주지만 직접 만드는 다섯 장은 손님 1~5명이다. 0은 들어오기 전 상태로 따로 다룬다.
dot-comparer--counting-comparer-5|점과 물건을 각각 세어 5점과 물건 3개를 비교한다. 물건 크기와 수, 같은 수를 다시 세는 도움을 구별한다.
estimate-how-many-benchmark|먼저 작은 묶음을 세고 그 수를 어림의 기준으로 쓴다. 표본 묶음이 전체에 고르게 적용되는지 설명하게 한다.
estimate-how-many-composition|규칙 배열의 부분을 세고 전체로 합성한다. 불규칙 배열에서는 남는 물건과 크기가 다른 부분을 따로 반영한다.
estimate-how-many-scanning-estimator|새 떼를 빠르게 어림하는 6과 7 예의 곱은 42지만, 약 40이라는 어림과 정확한 개수는 구별한다. 직사각형으로 빈틈없이 놓였는지 확인한다.
estimate-how-many-spatial-extent|물건이 퍼진 정도를 단서로 활용한다. 차지하는 영역이 같아도 밀도와 개수는 다를 수 있다.
estimating-game-composition-estimator|82를 약 80으로 보는 예와 검산 장면의 5개씩 16묶음과 3개의 합 83을 구별한다. 덮기 전 예상과 펼쳐 센 수를 따로 기록한다.
find-my-home-stemie-early-comparison-corresponder|한 자리에 한 개씩 놓아 가득 채울 때 자릿수와 놓은 수가 같다. 두 개가 한 자리에 들어가면 남은 자리를 다시 확인한다.
first-second-ordinality-stemie-first-second-ordinal-counter|시간의 순서와 줄에서의 순위를 말한다. 앞을 어느 쪽으로 잡았는지, 다음에 할 일을 무엇으로 정했는지 밝힌다.
flip-to-compare-counting-comparer-5|1~5의 점을 비교한다. 점 크기나 배치가 다른 자료와 숫자 글자를 읽는 지원을 구별하고, 마지막에 동률이면 적용할 규칙을 정한다.
flip-to-compare-same-size|두 카드의 수가 같으면 다음 카드를 뒤집는 절차다. 더 뒤집을 카드가 없을 때의 규칙을 따로 정한다.
get-just-enough-counting-comparer-5|멀리 있는 물건을 사람 수만큼 가져오고 실제로 나눠 주어 검산한다. 눈앞에서 직접 짝짓기와 수를 기억해 가져오는 수행을 구별한다.
groupitize|같은 색과 여러 색, 가까이 모은 배열과 흩어진 배열을 바꿔 어림하고 센다. 색 개수와 전체 물건 수를 구별하며 조건이 통제되지 않은 결과로 효과를 일반화하지 않는다.
help-mr-mix-up-put-numbers-in-order|목표의 물건 수는 5까지지만 절차에 6과 10을 센 예가 있다. 마지막 수를 전체로 말하지 않기, 순서를 건너뛰기, 중복 세기를 구별한다.
i-have-more-flip-to-compare|큰 수 카드의 주인이 두 장을 가져가는 예다. 같은 수일 때의 처리와 가져온 카드를 다시 뒤집을지 명시한다.
im-thinking-of-a-number-mental-number-line-to-100|선의 왼쪽 표지는 0이지만 숨긴 수의 범위는 1~100이다. 55보다 크고 60보다 작은 후보는 56~59다.
im-thinking-of-a-number-mental-number-line-to-1000|445보다 크고 460보다 작은 후보는 446~459다. 450은 그중 하나이며 더 구체적인 단서가 있어야 하나로 정해진다.
is-it-fair-dissimilar-early-comparer-of-dissimilar-items|사과 세 개와 바나나 세 개의 개수는 같다. 크기나 무게 등 다른 속성까지 같다고 판단하지 않는다.
is-it-fair-similar-early-comparer-of-similar-items|같은 종류의 물건을 두 인형에게 나눠 준 뒤 개수를 비교한다. 공평하다는 말의 기준을 이 활동에서는 개수로 한정한다.
longest-train|열차 길이와 블록 수의 차이를 함께 보려면 같은 크기 블록을 이어 붙이고 시작점을 맞춘다. 더 긴 부분을 가리키고 블록 수를 센다.
match-them-up|종이와 아이, 모자와 인형, 자동차와 트럭의 짝을 맞춘다. 닮은 물건끼리 고르기와 두 모임의 수를 같게 만들기를 구별한다.
math-with-motion-serial-orderer-to-6comparing-number|먼저 1씩 잇고 다음 변형은 2씩 잇는다. 모두 있을 때 두 줄이 되며 일부 카드를 가리면 같은 차이를 유지한 연결이 끊길 수 있다.
mr-mixup-counting-comparer-10|큰 물건 4개와 작은 물건 6개를 비교한다. 크기나 차지하는 공간이 아니라 짝짓기와 세기로 개수를 확인한다.
name-frame|이름의 글자를 한 칸에 하나씩 쓰고 10글자보다 길면 틀을 더 쓴다. 글자 개수와 실제 글자 폭이나 소리 길이를 구별한다.
number-line-estimator-stemie|추정 최대가 450 정도일 때 0~500을 잡으면 중점은 250이다. 실제 개수를 공개한 뒤 추정 순서와 위치를 따로 검산한다.
one-to-one-puzzles-early-comparison-corresponder|조각에 맞는 자리를 선택한 것과 조각을 끝까지 끼우는 손동작을 구별한다. 남거나 비어 있는 곳을 따로 확인한다.
order-cards-serial-orderer-to-5-comparing-number|1~5 점 카드를 보는 방향에서 증가하도록 정렬한다. 다음 수 예상과 섞은 뒤 다시 정렬하는 수행을 구별한다.
order-cards-serial-orderer-to-6-comparing-number|수준 이름과 달리 절차는 1~10 또는 그 이상을 사용한다. 놀이를 빨리 끝내는 것과 정렬의 근거를 구별한다.
order-cube-towers-6|안쪽 탑을 빼고 틈을 닫는다. 보이는 탑의 차이를 보고 어느 위치에 몇 개짜리 탑이 들어갈지 설명한다.
put-them-together-early-comparison-corresponder|뚜껑·양말·달걀의 대응을 만들고 남는 물건을 확인한다. 몸짓이나 선택의 지원 전후를 따로 기록한다.
race-to-space-mental-number-line-to-10|1번 칸에서 2번 이동하면 3번이다. 1에서 10까지의 9번 이동 가운데 5까지는 4번이므로 5번 칸이 이동의 정확한 절반은 아니다.
race-to-space-to-100|6에서 2가 나오면 7과 8에 차례로 닿는다. 본문에 주사위와 돌림 표현이 섞이며 출발·도착 표시와 초과 시 규칙은 자료로 확인한다.
rocket-blast-100|1과 100을 끝점으로 정한다. 간격 99개와 1부터 100까지의 숫자 100개를 구별한다.
rocket-blast-1000|끝점과 숨긴 수는 1~1000으로 지정하지만 뒤에서는 1~100이라고 적는다. 앞의 설정을 쓰면 단위 간격은 999개다.
schedule-mess|익숙한 일정 6~10개를 시간 순서대로 다시 놓는다. 순번과 걸린 시간의 길이를 구별한다.
setting-the-table-stemie-early-comparison-corresponder|접시·냅킨·도구 각각을 사람마다 하나씩 놓는다. 도우미가 자기 자리도 준비하는지와 남는 물건을 정한다.
super-secret-number-mental-number-line-to-10|1~10 카드 하나를 가리고 틈을 닫는다. 2와 4가 이웃하게 되면 원래 사이에 3이 있었다는 규칙을 설명한다.
the-estimating-jar|큰 물건 5~15개 또는 5~10개를 담아 어림한 뒤 꺼내 센다. 어림의 기준으로 본 10과 실제로 확인한 수를 구별한다.
the-estimating-jar-scanning-with-intuitive-quantification|같은 물건을 병에 둔 상태와 펼친 상태에서 각각 어림한다. 5개씩 네 묶음과 낱개 4개는 정확히 24다.
the-estimating-jar-smallbig|먼저 큰 물건 5~10개로 시작한다. 눈으로 어림한 값과 꺼내 센 값을 구별하고 물건 크기로 개수를 단정하지 않는다.
the-mysterious-cookie-jar|그대로·하나 더함·하나 뺌을 구별한다. 숨기기 전 수와 다시 센 수를 비교하며 0개에서 하나 빼는 경우는 시행하지 않는다.
what-is-the-largestsmallest-number-i-can-make|7과 3을 바꿔 놓으면 73과 37이다. 0이 앞서는 07의 수 값과 두 자리 수만 허용하는 규칙을 구별한다.
whats-the-missing-step-5|1에서 5까지 커졌다가 작아지는 판에 3개짜리 탑이 두 곳 있다. 빠진 탑의 크기와 오름·내림 쪽의 위치를 구별한다.
whats-the-missing-step-mental-number-line-to-10|1에서 10까지 오른 뒤 내려오는 19개 탑에서 9는 9번째와 11번째에 있다. 9개짜리와 9번째를 두 자리 모두에 같은 뜻으로 쓰지 않는다.
where-does-this-card-go|0~10 카드를 한 방향에서 정렬한다. 8이 2보다 뒤라는 것과 바로 뒤라는 것을 구별하고 사이 간격도 확인한다.
which-has-more-perceptual-comparer|3개와 5개를 짧게 비교한 뒤 센다. 큰 두 모임에 차이를 크게 주는 지원을 일반적인 비교 한계로 삼지 않는다.
which-has-more-stemie--very-small-number-recognizer|1~3개 모임을 비교한다. 교사가 많은 쪽을 가리킨 뒤의 반응과 먼저 한 비교 판단을 나눠 본다.
which-number-is-greater|십의 자리를 가리면 일의 자리만으로 두 자리 수의 대소를 정할 수 없는 경우가 있다. 이미 본 값을 기억한 답과 보이는 정보로 정한 답을 구별한다.
who-has-more|2 대 4, 5 대 10, 10 대 20을 비교한다. 늘어놓은 줄 길이를 근거로 쓰려면 짝마다 간격과 시작점을 맞춘다.
who-is-older-mental-number-line-to-10|5살과 6살을 비교하고 5~10 범위에서 반복한다. 나이의 기준과 단위를 동일하게 둔다.
who-is-older-mental-number-line-to-5|2살과 3살을 비교하고 0~5 범위에서 반복한다. 수의 앞뒤와 실제로 몇 년 더 나이가 많은지를 따로 답한다.
whos-up-first-stemie|줄이나 차례에서 첫째와 둘째를 정한다. 첫째의 위치를 어디부터 셌는지 확인한다.
'''

CLAIMS = [
    ('LT74', ['2수01-01', '2수01-03', '2수03-06'], [5, 6, 7, 8, 9, 12, 18, 20, 22, 28, 29, 30, 31, 33, 36, 40, 46, 56, 57, 59],
     '짝짓기와 세기로 모임의 개수를 비교한다. 물건의 종류, 크기, 줄의 길이가 달라져도 개수의 대소는 각각 센 값으로 확인한다. 길이 비교에는 출발점과 단위를 맞춘다.',
     '잠깐 본 추정과 다시 세어 확인한 결과를 구별한다. 같은 개수로 나눴다는 사실만으로 무게·들이·실제 공평함까지 같다고 보지 않는다.'),
    ('LT75', ['2수01-01', '2수01-03'], [0, 1, 3, 11, 19, 24, 32, 37, 38, 39, 45, 47, 53, 54, 55, 62],
     '수의 증가·감소 규칙과 관찰할 시작 방향을 먼저 정한다. 오르내리는 계단에는 같은 높이의 탑이 두 곳에 있을 수 있으므로 블록 개수와 탑의 순번을 별도로 설명한다.',
     '순번이 탑의 블록 수와 우연히 같은 경우를 다른 배치에 확대하지 않는다. 원래 수열의 규칙이 없으면 비어 있는 항을 하나로 정할 수 없는 경우가 있다.'),
    ('LT76', ['2수01-03', '2수01-06', '2수03-13'], [2, 4, 10, 26, 27, 35, 41, 42, 43, 44, 55],
     '수직선에서 끝점, 단위 간격, 도착 수를 구별한다. 1~10의 이동은 9번이고 1~1000의 간격은 999개다. 위치의 순서가 맞아도 축척이 맞는지는 별도로 확인한다.',
     '1000 활동에 섞인 1~100 문구와 1에서 출발해 5에 이르면 절반이라는 문구는 설정에 맞게 고친다. 놀이 칸의 수나 숫자 표지를 실제 길이와 동일하게 읽지 않는다.'),
    ('LT77', ['2수01-01', '2수01-04', '2수01-10', '2수01-11'], [13, 14, 15, 16, 17, 23, 35, 48, 49, 50, 51],
     '작은 기준 묶음, 묶음 개수, 남는 물건을 이용해 어림한다. 정확히 같은 묶음이 반복되면 곱으로 검산할 수 있고, 빈칸이 있거나 실제로 세지 않은 부분이 있으면 조건과 오차를 표시한다.',
     '배열의 색이나 넓이만으로 정확한 개수를 정하거나, 한 활동의 어림 결과를 학생 집단의 일반적인 효과로 해석하지 않는다.'),
    ('LT78', ['2수01-02', '2수01-03'], [21, 25, 26, 27, 52, 58, 60, 61],
     '두 자리 수의 대소는 십의 자리부터 확인한다. 십의 자리가 같은 경우 일의 자리를 본다. 수를 만드는 카드에서 앞의 0이나 가려진 자리의 가능 범위를 먼저 정한다.',
     '같은 일의 자리 정보와 양립하는 두 가지 배치가 서로 반대 대소를 만들 수 있다. 정해지지 않은 자리나 선행 0을 근거로 하나의 두 자리 수를 확정하지 않는다.'),
]

OBSERVATIONS = [
    dict(id='LT-P65', standard_codes=['2수01-01', '2수01-03', '2수03-06'],
         question='가에는 작은 단추 6개를 좁게 놓고, 나에는 큰 단추 4개를 가보다 더 긴 줄이 되게 띄어 놓았다. 어느 쪽에 단추가 더 많은가? 어느 줄이 더 긴가? 한 개씩 짝지으면 어떤 일이 생기는가?',
         expected='단추는 가가 6개로 더 많고, 줄은 조건에 따라 나가 더 길다. 가와 나에서 한 개씩 짝을 만들면 네 짝이 되고 가에 두 개가 남는다.',
         interpretation='개수와 길이 중 어느 양에 대한 답인지 말한다. 처음 보인 인상과 짝짓기로 확인한 근거를 따로 기록한다.', student_validated=False),
    dict(id='LT-P66', standard_codes=['2수01-01', '2수01-03'],
         question='탑을 이루는 블록 수가 왼쪽부터 1·2·3·4·5·4·3·2·1이다. 3개짜리 탑 둘 중 오른쪽 탑을 뺐다. 그 탑은 처음에 왼쪽에서 몇 번째였는가? 원래 어떤 두 탑 사이에 있었는가?',
         expected='3개짜리는 처음에 세 번째와 일곱 번째였다. 오른쪽 탑은 일곱 번째이며 내리막의 4개짜리와 2개짜리 사이에 있었다.',
         interpretation='탑에 든 수 3과 처음 위치 7, 어느 쪽으로 세는지를 따로 답하게 한다. 오름 쪽의 3개짜리를 빼면 위치와 양옆이 바뀐다.', student_validated=False),
    dict(id='LT-P67', standard_codes=['2수01-03', '2수01-06', '2수03-13'],
         question='같은 간격으로 1번부터 10번까지 놓인 길에서 1번에 출발한다. 5번까지 몇 번, 10번까지 모두 몇 번 움직이는가? 절반은 어느 두 칸 사이인가? 0번에서 출발한다면 5번은 어떤 위치인가?',
         expected='5번까지 4번, 10번까지 9번 움직인다. 5번에서는 앞으로 5번이 남아 중간은 5번과 6번 사이다. 0번에서 10번까지라면 5번이 정확한 중간이다.',
         interpretation='출발 칸을 새 이동으로 세는지 확인한다. 1~10에서 5를 절반이라고 할 때 숫자 10의 절반과 이동 전체의 절반을 따로 말하게 한다.', student_validated=False),
    dict(id='LT-P68', standard_codes=['2수01-04', '2수01-10', '2수01-11'],
         question='작은 말이 6행 7열의 자리 중 일부에 놓여 있다. 처음에는 가득 찼다고 보고 어림했다. 확인하니 빈 자리가 3곳이다. 어림한 수와 실제 개수를 말하고 두 값이 달라진 까닭을 설명하라.',
         expected='가득 찼다는 가정에서는 7개씩 6행이어서 42개다. 빈 자리 3곳을 빼면 39개다. 처음 값은 자리 전체의 수이고 확인한 값은 놓인 말의 수다.',
         interpretation='묶음으로 계산하는 전략과 각 묶음이 다 찼는지 확인하는 전략을 구별한다. 빈 곳의 합을 세거나 행마다 놓인 수를 합해 검산할 수 있다.', student_validated=False),
    dict(id='LT-P69', standard_codes=['2수01-02', '2수01-03'],
         question='두 자리 수 두 개를 비교한다. 십의 자리를 가리니 왼쪽에는 4, 오른쪽에는 8만 보인다. 왼쪽이 큰 예와 오른쪽이 큰 예를 각각 하나씩 만들고, 왼쪽의 십이 6이고 오른쪽의 십이 5라는 단서를 받으면 어느 수가 큰지 설명하라.',
         expected='64와 58에서는 왼쪽이 크다. 54와 68에서는 오른쪽이 크다. 새 단서에서는 64와 58이므로 십의 자리가 더 큰 64가 크다.',
         interpretation='보이는 일의 자리와 아직 모르는 십의 자리를 구별한다. 새 단서 전후에 판단이 달라지는 까닭을 설명한다.', student_validated=False),
]


def verify_examples(bodies):
    assert '1 and 1000' in bodies[44]['body'] and '1-100 number line' in bodies[44]['body']
    assert '1st space' in bodies[41]['body'] and 'halfway to 10' in bodies[41]['body']
    assert 'up to five' in bodies[24]['body'] and 'counts 10' in bodies[24]['body']
    assert 5 - 1 == 4 and 10 - 5 == 5 and Fraction(1 + 10, 2) == Fraction(11, 2)
    assert Fraction(0 + 10, 2) == 5 and 1000 - 1 == 999
    path = [*range(1, 6), *range(4, 0, -1)]
    assert [i for i, height in enumerate(path, 1) if height == 3] == [3, 7] and path[5:8] == [4, 3, 2]
    assert 6 * 7 - 3 == 39 and 16 * 5 + 3 == 83
    assert 64 > 58 and 54 < 68 and 64 % 10 == 54 % 10 and 58 % 10 == 68 % 10


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        assert source['snapshot_sha256'] == sha(ROOT / NOTES)
        assert {row[0] for row in CLAIMS} <= {row['id'] for row in registry['claims']}
        assert source['observations'][-len(OBSERVATIONS):] == OBSERVATIONS
        build_report()
        return
    assert source['snapshot_file'] == PRIOR and sha(ROOT / PRIOR) == PRIOR_SHA
    prior = load(ROOT / PRIOR)
    pages, bodies, selected = [load(CACHE / name) for name in ('activity-manifest.json', 'english-bodies.json', 'selection.json')]
    followup = copy.deepcopy(prior['activity_followup_catalog'])
    assert selected == [row for row in followup['records'] if not row['body_read']
                        and any('/math/comparing-and-ordering-number/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|', 1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 63
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/', 1)[-1] for row in pages] == [row[0] for row in reading]
    verify_examples(bodies)

    old_images = {row['url'] for row in prior['image_read_manifest']}
    old_pdfs = {row['url'] for row in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for page, body, (_, note) in zip(pages, bodies, reading):
        url = page['url']
        assert page['status'] == 200 and page['final_url'] == url and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256'] and '\nActivity\n' in body['body']
        assert 'Type:\nTeacher Resources' not in body['body']
        groups['activities'].append(page['key'])
        logs.append(dict(url=url, page_kind='activity_procedure', note=note))
        linked_images = {urljoin(url, image['src']) for image in page['images'] if '/upload/' in image.get('src', '')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert len({url for links in images.values() for url in links}) == 88
    assert len({url for links in pdfs.values() for url in links}) == 8
    assert {k: len(v) for k, v in groups.items()} == dict(general=6, domain_overviews=20, levels=224, activities=424, teacher_resources=16)
    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key', 'url', 'title', 'sha256', 'status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 690
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'], followup['listed_body_pending']) == (440, 384)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
                 observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
                 catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies': 440, 'pending_activity_bodies': 384},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=63, teacher_resources=0, inline_images=0, supplementary_pdf_urls=0),
                 comparing_number_reading_log=logs, completed_comparing_number_records=selected,
                 comparing_number_pdf_urls_not_reviewed=pdfs, comparing_number_image_urls_not_reviewed=images,
                 comparing_number_procedure_scope=dict(activity_procedures=63, teacher_resources=0),
                 comparing_number_line_checks=[dict(url=pages[41]['url'], endpoints=[1, 10], intervals=9, jumps_to_five=4, midpoint='11/2'),
                                               dict(url=pages[44]['url'], endpoints=[1, 1000], intervals=999, competing_text_endpoints=[1, 100])],
                 reading_log=prior['reading_log'] + ['수량 비교·순서 수준에 연결된 영어 활동 63개의 목표·절차·준비물과 교사 지원을 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='comparison_attributes_and_number_line_endpoints', locations=[pages[i]['url'] for i in (1, 24, 33, 41, 42, 44, 52, 54, 58)],
                     action='같은 개수의 기준, 목표와 예시의 수 범위, 수직선 끝점과 칸 이동, 두 자리 수에서 가려진 정보, 같은 탑 높이의 다른 순번을 각각 명시했다.')],
                 unread_followups=[LIMITS, '수량 비교·순서 활동의 첨부와 다음 수량·연산 활동 본문을 검토한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
                  method_note='영어 목표와 절차의 수 범위, 비교 속성, 시작 위치와 축척, 교사 지원을 대조했다.',
                  editorial_action='문헌 대응 5건과 자체 관찰 과제 5개를 추가했다.', observations=source['observations'] + OBSERVATIONS)
    for cid, codes, indices, support, limit in CLAIMS:
        registry['claims'].append(dict(id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
                                       locations=[pages[i]['url'] for i in indices], support=support, does_not_establish=limit,
                                       independent_review=False, student_validated=False,
                                       target_snapshots={'revision:' + code: digest(target_value('revision:' + code)) for code in codes}))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE])
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Reviewed 63 English activities; added 5 mappings and 5 observations. Public activity bodies pending: 384.')


if __name__ == '__main__':
    main()

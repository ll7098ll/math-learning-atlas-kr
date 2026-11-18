"""Register the reviewed English goals and procedures of LT2 addition activities."""
import copy
import hashlib
import re
from urllib.parse import urljoin, urlparse

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_counting_assets_review_notes.json'
PRIOR_SHA = '10b42027b8461126684112bee680ccc565037fc8df367dcf87dd95df4b400816'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_addition_subtraction_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-addition-subtraction-activities'
MINT = 'https://www.usmint.gov/learn/coins-and-medals/circulating-coins'
SCOPE = (
    '덧셈·뺄셈 수준에 연결된 미검토 공개 페이지 71개의 영어 목표와 활동 절차를 확인했다. '
    '활동 안내 60개, 그림책 읽기 제안 1개, 교사자료 10개다. 교사자료 10개 주소의 문제 유형 본문은 같다. '
    '누적 공개 HTML 565개이며 활동·교사자료 목록 824개 중 본문 315개를 확인했고 509개가 남았다.'
)
LIMITS = (
    '새로 연결된 PDF 24개 URL과 삽입 이미지 92개 URL은 별도 검토 대상이다. '
    '이전 PDF 39개 URL과 삽입 이미지 349개 URL의 확인 범위는 유지한다. '
    '영상, 원전 교재·그림책, 개별 연구, 번역 동등성, 독립 검토와 학생 응답은 후속 범위다.'
)
TEACHER_NOTE = (
    '열두 예를 제시한 공통 교사자료다. 합류·제거에서는 시작량·변화량·결과량, 정적인 부분·전체와 비교에서는 각 수의 역할을 따로 기록한다. '
    '비교 예는 비교량 두 경우와 차이 한 경우로 기준량을 구하는 예가 없다. 마지막 예는 물건 명칭이 섞인다.'
)

READING = '''
21|21 이하 중 가장 큰 합을 찾는 놀이로 읽는다. 10 카드의 값과 에이스 1/11의 선택 시점, 동률과 탈락 처리 조건을 별도로 정한다.
add-it-up|60+7과 50+2에서 십 묶음과 낱개를 유지한다. 뺄셈은 변형으로만 언급되므로 세부 절차를 임의로 보충하지 않는다.
adding-animals-stemie|동물 한 마리를 더하거나 빼는 장면과 교사의 수 표현을 확인했다. 시선, 손 뻗기, 수 설명을 각각 관찰한다.
adding-lots-of-things|더 많다·더 적다가 적용되는 속성을 정한다. 물건 수의 한 개 변화와 길이·시간의 크기 표현은 다른 양이다.
adding-one-more--again-and-again-preverbal-|본문 절차는 같은 종류를 하나씩 놓아 4개까지 간다. 목표에 언급된 제거 절차가 별도로 제시되지는 않는다.
addingsubtracting-problem-types|공통 교사자료.
addingsubtracting-problem-types-counting-strategies-|공통 교사자료.
addingsubtracting-problem-types-deriver--addingsubtracting|공통 교사자료.
addingsubtracting-problem-types-find-change-|공통 교사자료.
addingsubtracting-problem-types-make-it-n|공통 교사자료.
addingsubtracting-problem-types-multidigit--addingsubtracting|공통 교사자료.
addingsubtracting-problem-types-numbers-in-numbers-|공통 교사자료.
addingsubtracting-problem-types-part-whole-|공통 교사자료.
addingsubtracting-problem-types-problem-solver--addingsubtracting|공통 교사자료.
addingsubtracting-problem-types-small-number-|공통 교사자료.
addition-bingo|두 카드의 합을 찾아 표시한다. 합을 구하는 수행과 판에서 네 칸 줄을 만드는 규칙을 구별한다.
addition-easel|채운 6칸에 4칸을 더하면 전체 10칸이다. 주어진 양, 빈 자리 수, 완성된 전체를 각각 말하게 한다.
age-differences|기준 나이를 먼저 지정한다. 10살보다 2살 적으면 8살이다. 식에서 어느 사람을 어느 문자로 나타냈는지 정한다.
bear-stories-joining|곰이 집이나 탈것에 들어오는 장면에서 세는 장소와 시작 수를 정한다. 이야기 만들기와 이미 준 이야기를 푸는 수행을 구별한다.
bear-stories-separating|놀이터 전체에 있는 곰과 모래밭에 남은 곰은 다르다. 자리를 옮긴 뒤 무엇을 세는지 지정한다.
big-fish-story--find-result-|강은 변화량을 검사하는 중간 장소이고 바다는 결과를 세는 장소다. 현재 수보다 큰 양을 빼는 카드는 이 과제에서 제외한다.
big-fish-story-small-number|3에 1을 더해 4를 만든다. 목표를 5 이하로 해석하면 다음 시행의 결과도 확인해야 한다. 결과가 5를 넘은 뒤에 비우는 것은 같은 제한이 아니다.
break-apart-to-make-ten-to-100|100 도구의 빈 자리로 다음 십을 완성하고 나머지를 잇는다. 100의 상한과 뺄 수 있는 양을 지정한다.
break-apart-to-make-ten-to-20|20 도구에서 10을 채울 부분과 나머지를 나눈다. 구슬을 옮긴 동작과 계산을 설명한 시점을 구별한다.
cherry-and-mr-smore|27은 10 묶음 두 개와 7개다. 4를 더해 31을 만든다. 떨어진 양이 현재 더하는 대상인지 이야기 속 위치를 정한다.
chip-stack|7에서 3만큼 이어 세면 8·9·10이다. 탑 높이나 균형과 개수를 구별하고 시작 수를 새 변화로 세지 않는다.
chocolate-chip-count|두 그림의 점 수와 합을 따로 말한다. 결과를 적는 도움과 합을 스스로 구한 응답을 구별한다.
coin-dice|미국 조폐국 액면 25·10·5센트를 더하면 40센트다. 본문의 80센트 예는 틀렸다. 주사위 한 개에 같은 액면이 적힌 면이 두 개 있다는 설명은 합과 별도다.
crossing-decades|제목의 표현과 달리 절차에서 더하거나 빼는 수는 10의 배수다. 낱개가 넘어 다음 십을 만드는 문제와 다르다.
decade-spin|3+4, 33+4, 63+4는 일의 자리가 10을 넘지 않는다. 같은 일의 자리의 패턴을 십을 넘는 모든 경우로 확대하지 않는다.
dot-to-dot|두 모임의 점과 말을 대응한다. 전부 다시 세기와 시작량을 유지하고 이어 세기를 서로 다른 전략으로 기록한다.
double-war-find-result-|합이 같은 경우 다음 라운드로 이어간다. 마지막 카드까지 동률이 남았을 때의 처리와 받은 카드 수를 별도로 정한다.
feed-the-animals|목표 수에 맞게 한 개를 더하거나 빼고 나서 먹인다. 처음 맞춘 수와 교사 모형을 보고 고친 수를 구별한다.
finding-pennies|각기 다른 시작값에 3을 더하는 관계다. 2+3은 두 배 4에 1을 더해 설명할 수 있다. 한 값 계산과 여러 값에 공통인 규칙 설명을 구별한다.
five-six-in-a-row|제목과 별도로 영어 절차는 가로·세로·대각선 중 네 칸을 먼저 잇도록 한다. 판에서 허용하는 두 수와 중복 선택 여부를 먼저 확인한다.
flip-the-cards|목표 6은 6 한 장 또는 2+4나 1+5로도 만들 수 있다. 카드를 한 번에 한 모임에만 쓰고 뒤집지 않은 카드의 값 합을 비교한다.
grid-race-deriver--addingsubtracting|0에서 99로 간다. 16에서 9칸 이동하면 25다. 정확히 99일 필요가 없다는 조건을 다른 판으로 옮기지 않는다.
guess-my-rule-numbers-in-numbers|같은 수를 더하거나 빼는 규칙으로 범위를 정하면 4→8과 10→14에서 +4다. 몇 개의 짝만으로 가능한 모든 규칙이 하나가 되지는 않는다.
hat-height|적어 둔 두 길이를 합한다. 모자가 머리에 씌워져 겹치는 부분이 있으면 실제 키 증가량은 모자 전체 길이와 다를 수 있다. 식의 결과는 모자를 쓴 전체 높이다.
hiding-bears|처음 모임의 전체와 보이는 부분으로 가린 부분을 예상한다. 가림을 해제한 뒤 확인한 수를 처음 예상과 구별한다.
how-far-from-the-start|두 사람이 같은 방향으로 연달아 움직일 때 출발점부터의 칸 수를 더한다. 시작 칸을 한 걸음으로 세지 않으며 실제 거리의 단위도 구별한다.
how-many-answers-can-you-find|가능한 답과 다른 풀이 방법을 구별한다. 빈칸의 자리 수, 0 허용, 날짜별 거리, 상자를 묶는 끈의 경로를 정해야 답의 범위를 판단할 수 있다.
how-many-more-game|10자리에 남은 수를 구한다. 마지막에 필요한 수가 정확히 나와야 한다는 규칙을 명시한 경우다. 초과 이동을 허용한 다른 놀이와 구별한다.
jumping-to-100-multidigit--addingsubtracting|낱개 주사위 값과 십 단위 주사위 값을 현재 위치에 더한다. 100에 닿거나 넘으면 끝나는 규칙이다.
knock-knock|에이스는 1로 고정한다. 가장 큰 합을 찾는지 가장 작은 합을 찾는지 먼저 결정하고, 마지막 추가 차례와 동률을 구별한다.
lets-go-shopping|두 손에 각각 나타낸 양을 합한다. 손가락의 수가 제약일 수 있어 물건이나 점 표시로도 응답할 수 있다.
magic-hat-find-change-|6개에 2개를 더해 8개라는 관계다. 모자에 준비한 총수, 모자에서 꺼낸 수, 두 부분을 합친 수를 구별한다.
make-me-100-multidigit--addingsubtracting|47의 보수는 53이다. 34의 보수 66처럼 같은 숫자가 두 자리에서 필요할 수 있다. 카드가 숫자마다 한 장뿐이면 중복 표기 수단을 준비한다.
make-or-break-part-whole-|연결한 큐브를 둘로 나눠도 전체는 같다. 보이는 6개와 가린 4개의 합 10을 확인하고 열어 보기 전 답을 기록한다.
mealtimes-stemie-arithmetic-senser-foundations|내놓은 수, 먹은 수, 남은 수를 구별한다. 더 달라는 표현을 정확한 수 보고로 해석하지 않는다.
more-toppings|5에서 8로 바꿀 때 더한 수는 3이다. 9에서 4로 바꿀 때 뺀 수는 5다. 시작 수를 변화 횟수에 포함하지 않는다.
number-cube-equations|뺄셈에서 큰 수를 먼저 놓아 음수 결과를 피한다. 같은 수가 나오면 0이다. 카드 배열로 만든 식과 등호가 포함된 완성식을 구별한다.
number-scenes-find-result-|오렌지 3개와 배 3개를 합할 때 세는 대상은 모든 과일이다. 배경 그림, 실제 올린 토큰, 아이가 말한 이야기의 범위를 지정한다.
number-stories-everywhere|합류·제거·필요한 수의 예를 제공한다. 이야기에 시작량이 없으면 들어온 사람 수만으로 지금 모임의 전체를 정하지 않는다.
phil-the-baker-find-change-|이미 있는 수는 7~10, 주문 카드는 10~19로 제시된다. 10이 준비돼 있고 주문도 10인 경우 추가는 0개다.
plan-a-picnic|가린 바구니의 변화를 본 뒤 자기 바구니를 맞춘다. 비교할 때 덮개를 열고 고친 수를 최초 예상과 구별한다.
quince--problem-solver-|15를 넘지 않는 합을 비교한다. 합이 같을 때의 처리와 실제 사용하는 카드의 값은 절차에서 별도로 명시해야 한다.
race-to-100|십 묶음과 낱개를 합하고 100까지 얼마가 남았는지 구한다. 눈금이나 게임 순서보다 현재 수와 필요한 양에 초점을 둔다.
reading-with-infants|그림을 짚어 수를 말해 보는 짧은 읽기 제안이다. 소개된 그림책의 전체 본문과 실제 수행은 포함하지 않는다.
roll-call|명부에 든 학생 수와 출석 수를 같은 날 같은 범위로 세고 차이를 구한다. 표시 누락, 중복, 뒤늦은 출석의 처리 시점을 정한다.
sammy-the-squirrel|나무의 5개 중 3개를 옮기면 나무에는 2개가 남는다. 두 장소에 보이는 전체와 나무에 남은 수를 구별한다.
searching-for-goldilocks|3에 2가 합류해 5가 된다. 곰 2개를 보여 주기 전 예상과 모두 놓은 뒤 세기 검산을 구별한다.
sneaky-swiper-counting-strategies-|첫 시행에서 5개를 뺀다는 절차와 2~4개만 빼라는 설명이 다르다. 처음 수와 남은 수로 실제 제거량을 확인한다.
span-decades|13+7은 다음 십에 정확히 닿고 23+9는 그 십을 넘어간다. 10을 채울 양과 남는 양을 각각 설명한다.
talk-it-out|빈 수직선에 사고를 나타낸다. 호의 이동값, 숫자의 변화, 십의 경계를 넘는 경우를 설명한다. 소리 내 말하기 외에 다른 표현도 가능하다.
ten-spot|30+10의 한 묶음은 10개를 뜻한다. 5칸 틀과 10칸 틀을 바꿔 쓸 때 같은 수를 나타내는지 점을 확인한다.
the-confused-customer-make-it-n-|4를 6으로 고치는 수행과 2개 더했다고 보고하는 수행을 구별한다. 결과를 보고 합류·제거한 양을 설명하게 하는 단계는 별도다.
tic-tac-20|1~10에서 숫자는 한 번씩만 쓴다는 기본 규칙과 중복을 허용한 변형이 다르다. 세 칸의 합이 20인지 확인한다.
tic-tac-total|표시된 목록에는 0이 두 번 나온다. 숫자 0과 각 카드의 사용 기회를 구별하고 목표 합 9와 행 조건을 명시한다.
toy-word-problems|서로 다른 종류의 공룡 3개와 2개를 합하면 공룡 전체 5개다. 어떤 공룡을 포함하는지 말이나 동작으로 확인한다.
wake-up-sleeping-giants-addingsubtracting|세 값 2·5·6으로 6+5−2=9 또는 2+5=7과 별도 6을 만들 수 있다. 같은 값을 두 번 쓰는지와 뒤집힌 카드의 처리 조건을 확인한다.
'''

CLAIMS = [
    ('LT54', ['2수01-04', '2수01-05', '2수01-07', '2수01-09'], [5, 18, 19, 39, 46, 48, 50, 60, 66],
     '합류·제거에서는 시작량과 변화량, 결과량을 정한다. 부분과 전체, 두 수량의 비교에서는 변화가 없어도 미지수가 생긴다. 같은 □ 값이라도 뜻을 따로 설명한다.',
     '비교의 기준량과 차이를 시간 순서의 시작량과 변화량으로 바꾸지 않는다. 같은 유형 예시를 싣는 주소 10개를 독립 근거 10건으로 세지 않는다.'),
    ('LT55', ['2수01-05', '2수01-06', '2수01-09'], [20, 21, 35, 36, 41, 42, 43, 51, 54, 62],
     '허용하는 수, 0의 포함 여부, 시작 상태와 종료 규칙, 변경할 수 있는 양을 먼저 정한다. 예시와 범위가 충돌할 때에는 둘을 구별하고 같은 조건에서 확인한다.',
     '놀이에서 정확히 도착하기, 넘어서기, 다시 시작하기는 서로 다른 규칙이다. 조건을 정하지 않은 열린 문제의 답을 모두 찾았다고 판단하지 않는다.'),
    ('LT56', ['2수01-02', '2수01-06', '2수01-09'], [1, 22, 23, 24, 28, 29, 30, 47, 57, 63, 64, 65],
     '십을 채우는 데 필요한 양과 남는 양을 구별한다. 보수의 값과 그 값을 만들 수 있는 카드의 수량·표기 조건을 함께 확인한다.',
     '십의 묶음과 한 자리 숫자 카드는 서로 다른 도구다. 카드가 한 장씩이면 같은 숫자를 두 자리에서 쓰는 수를 직접 만들 수 없다.'),
    ('LT57', ['2수01-06', '2수01-08'], [0, 15, 26, 27, 31, 34, 44, 56, 67, 68, 70],
     '여러 항을 합할 때 각 값과 합을 먼저 검산한다. 미국 동전 놀이의 25·10·5센트 합은 40센트다. 도착 순서, 카드 수, 점수 합은 놀이 규칙에 따라 따로 기록한다.',
     '동전 이름이나 놀이의 성공만으로 세 수의 덧셈을 판정하지 않는다. 해외 화폐 단위를 국내 필수 내용으로 요구하지 않는다.'),
    ('LT58', ['2수02-01', '2수03-13'], [17, 33, 37, 38, 40],
     '같은 양을 더하는 규칙을 찾을 때 입력과 결과, 공통 변화량을 구별한다. 길이 두 개를 합할 때 실제로 더해지는 구간과 단위를 확인한다.',
     '유한 예시에서 무제한의 규칙을 하나로 결정하거나 겹쳐 놓인 두 물체의 길이를 항상 그대로 더하지 않는다. 문자식이나 외국 길이 단위를 저학년의 새 필수로 삼지 않는다.'),
]

OBSERVATIONS = [
    dict(id='LT-P49', standard_codes=['2수01-05', '2수01-09'],
         question='가에서는 단추 5개가 있던 상자에 몇 개를 더 넣어 8개가 됐다. 나에서는 단추 8개 중 빨간 단추가 5개이고 나머지는 파란 단추다. 다에서는 준호가 8개를 가지고 있고 민서보다 3개 많다. 가에서 더 넣은 수, 나에서 파란 단추 수, 다에서 민서의 수를 각각 □가 있는 식으로 나타내고 설명하라.',
         expected='가는 5+□=8에서 3을 넣었다. 나는 5+□=8에서 파란 단추 3개를 뜻한다. 다는 □+3=8에서 비교의 기준이 되는 민서의 수가 5다. 앞의 두 식은 모양이 같아도 □이 뜻하는 것은 다르다.',
         interpretation='실제 변화량, 움직이지 않은 모임의 일부, 비교의 기준량을 각각 말하게 한다. □의 자리나 ‘더 많다’라는 말만 보고 연산을 고르는지 확인한다.', student_validated=False),
    dict(id='LT-P50', standard_codes=['2수01-02', '2수01-06'],
         question='24에 더해 90을 만드는 수를 구한다. 상대편에게는 0부터 9까지 숫자 카드가 한 장씩만 있다. 그 수를 카드로 만들 수 있는가? 카드 수가 부족하다면 수가 틀린 것인지, 어떻게 표현할 수 있는지 설명하라.',
         expected='24에서 30까지 6, 30에서 90까지 60을 더하므로 필요한 수는 66이다. 24+66=90으로 확인한다. 숫자 6 카드가 한 장뿐이면 두 자리를 동시에 만들 수 없다. 6을 한 장 더 받거나, 십 묶음 6개와 낱개 6개로 나타낼 수 있다.',
         interpretation='계산 결과와 도구로 구현할 수 있는 조건을 구별한다. 66의 두 숫자가 각각 다른 자릿값을 가리키는지 살핀다.', student_validated=False),
    dict(id='LT-P51', standard_codes=['2수01-06', '2수01-09'],
         question='23이나 33 중 하나에서 0, 2, 4, 6 중 하나를 뺐더니 답의 십의 자리가 2였다. 가능한 뺄셈식을 모두 찾아라. 0을 빼는 것을 금지하면 어떤 식이 빠지는가?',
         expected='23−0=23, 23−2=21, 33−4=29, 33−6=27이 된다. 23에서 4나 6을 빼면 20보다 작고, 33에서 0이나 2를 빼면 29보다 크다. 0을 금지하면 23−0=23만 빠진다.',
         interpretation='두 시작 수와 네 뺄 수의 조합을 표나 묶음으로 확인한다. 답을 몇 개 찾는 것과 주어진 조건에서 빠짐없이 확인하는 것을 구별한다.', student_validated=False),
]


def procedure_fingerprint(body):
    _, _, procedure = body.partition('\nActivity\n')
    procedure = re.split(r'\n(?:Adaptation Suggestions|Materials|Teaching Tips|Differentiating Instructions|References|Remember to use formative assessment)', procedure, maxsplit=1)[0]
    return hashlib.sha256(re.sub(r'\s+', '', procedure).encode()).hexdigest()


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        assert {row[0] for row in CLAIMS} <= {c['id'] for c in registry['claims']}
        assert source['observations'][-3:] == OBSERVATIONS
        build_report()
        return
    assert source['snapshot_file'] == PRIOR and sha(ROOT / PRIOR) == PRIOR_SHA
    prior = load(ROOT / PRIOR)
    pages = load(CACHE / 'activity-manifest.json')
    bodies = load(CACHE / 'english-bodies.json')
    selected = [r for r in prior['activity_followup_catalog']['records']
                if not r['body_read'] and any('/math/adding-subtracting/' in u for u in r['linked_level_urls'])]
    assert selected == load(CACHE / 'selection.json')
    reading = [line.split('|', 1) for line in READING.strip().splitlines()]
    assert len(selected) == len(pages) == len(bodies) == len(reading) == 71
    assert [a['url'] for a in pages] == [r['url'] for r in selected] == [b['url'] for b in bodies]
    assert [a['url'].rsplit('/', 1)[-1] for a in pages] == [row[0] for row in reading]
    teacher_hashes = {procedure_fingerprint(a['body']) for a in bodies[5:15]}
    assert teacher_hashes == {'923bb71cf099629a02366d87aa37d688a8fb60bfa78e04b2a8fea2c1b2c52d2f'}
    assert sum((25, 10, 5)) == 40 and sum((25, 10, 5)) != 80
    assert 24 + 66 == 90
    valid = {(a, b) for a in (23, 33) for b in (0, 2, 4, 6) if 20 <= a - b <= 29}
    assert valid == {(23, 0), (23, 2), (33, 4), (33, 6)}

    old_images = {a['url'] for a in prior['image_read_manifest']}
    old_pdfs = {a['url'] for a in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for index, (page, body, (_, note)) in enumerate(zip(pages, bodies, reading)):
        url = page['url']
        assert page['status'] == 200 and url == page['final_url'] and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256'] and '\nActivity\n' in body['body']
        teacher = 'Type:\nTeacher Resources' in body['body']
        assert teacher == (5 <= index <= 14)
        kind = 'teacher_resource' if teacher else 'reading_suggestion' if index == 58 else 'activity_procedure'
        groups['teacher_resources' if teacher else 'activities'].append(page['key'])
        logs.append(dict(url=url, page_kind=kind, note=TEACHER_NOTE if teacher else note))
        linked_images = {urljoin(url, a['src']) for a in page['images'] if '/upload/' in a.get('src', '')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert len({url for links in images.values() for url in links}) == 92
    assert len({url for links in pdfs.values() for url in links}) == 24
    assert {k: len(v) for k, v in groups.items()} == dict(general=6, domain_overviews=20, levels=224, activities=302, teacher_resources=13)
    manifest = prior['html_read_manifest'] + [{k: a[k] for k in ('key', 'url', 'title', 'sha256', 'status')} for a in pages]
    read_urls = {a['url'] for a in manifest}
    assert len(manifest) == len(read_urls) == 565
    followup = copy.deepcopy(prior['activity_followup_catalog'])
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(a['body_read'] for a in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'], followup['listed_body_pending']) == (315, 509)

    source_path = ROOT / 'data/sources.json'
    bibliography = load(source_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(
        date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
        html_read_manifest=manifest, observed_html_assets=manifest, read_groups=groups,
        new_read_groups=dict(domain_overviews=0, levels=0, activities=61, teacher_resources=10, inline_images=0, supplementary_pdf_urls=0),
        activity_followup_catalog=followup,
        catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies': 315, 'pending_activity_bodies': 509},
        addition_subtraction_reading_log=logs, completed_addition_subtraction_records=selected,
        addition_subtraction_pdf_urls_not_reviewed=pdfs, addition_subtraction_image_urls_not_reviewed=images,
        addition_subtraction_procedure_scope=dict(activity_procedures=60, reading_suggestions=1, teacher_resources=10),
        repeated_problem_type_procedure=dict(urls=[a['url'] for a in pages[5:15]], normalized_sha256=next(iter(teacher_hashes)),
                                            normalization='공백을 제외한 영어 Activity 절차', example_count=12),
        coin_value_fact_check=dict(url=MINT, activity_url=pages[27]['url'], cents=[25, 10, 5], stated_cents=80, calculated_cents=40),
        reading_log=prior['reading_log'] + ['덧셈·뺄셈과 연결된 71개 영어 페이지의 목표·활동 절차·교사 설명을 대조했다.'],
        source_corrections=prior['source_corrections'] + [dict(
            kind='addition_conditions_and_example_corrections', locations=[pages[i]['url'] for i in (5, 21, 27, 34, 37, 38, 41, 47, 62)],
            action='문제 유형별 수의 역할, 동전 합 40센트, 5 이하의 결과와 다시 시작하는 시점, 네 칸 줄, 규칙의 범위, 모자 겹침, 열린 문제의 조건, 같은 숫자 카드, 제거량 5와 2~4의 차이를 각각 기록했다.',
        )],
        unread_followups=[LIMITS],
    )
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                                date=source['date'], read_scope=source['read_scope'])]
    source.update(
        date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
        bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
        method_note='영어 목표와 실제 절차를 대조했다. 교사자료에서 같은 설명을 반복한 주소, 활동의 실제 시행 조건, 계산 예의 오류를 구별했다.',
        editorial_action='덧셈·뺄셈에 관한 문헌 대응 5건과 자체 관찰 과제 3개를 추가했다.',
        observations=source['observations'] + OBSERVATIONS,
    )
    for cid, codes, indices, support, limit in CLAIMS:
        locations = [pages[i]['url'] for i in indices]
        if cid == 'LT57':
            locations.append(MINT)
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
            locations=locations, support=support, does_not_establish=limit,
            target_snapshots={'revision:' + code: digest(target_value('revision:' + code)) for code in codes},
            independent_review=False, student_validated=False,
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(r for r in queue['literature_review'] if r['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[c['id'] for c in registry['claims'] if c['source_id'] == SOURCE])
    write(source_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Reviewed 71 pages, five mappings and three observations. Public bodies pending: 509.')


if __name__ == '__main__':
    main()

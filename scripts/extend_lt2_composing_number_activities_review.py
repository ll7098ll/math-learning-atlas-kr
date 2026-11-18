"""Register the reviewed English goals and procedures of LT2 composing number activities."""
import copy
from itertools import combinations, combinations_with_replacement, product
from urllib.parse import urljoin, urlparse

from extend_lt2_addition_subtraction_activities_review import procedure_fingerprint
from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_addition_subtraction_assets_review_notes.json'
PRIOR_SHA = '1508f7e1f56ce395e93209ff66141d4eb6e0f24f5c880e9fb821183c03b29d04'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_composing_number_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-composing-number-activities'
TEACHER_SHA = '923bb71cf099629a02366d87aa37d688a8fb60bfa78e04b2a8fea2c1b2c52d2f'
SCOPE = (
    '수의 합성·분해 수준에 연결된 공개 영어 페이지 62개를 대조했다. '
    '활동 안내 59개와 이전 교사자료와 같은 문제 유형 절차를 싣는 주소 3개다. '
    '누적 공개 HTML은 627개이며, 목록 824개 중 활동·교사자료 본문 377개를 확인했고 447개가 남았다.'
)
LIMITS = (
    '새 연결 PDF 19개 URL과 삽입 이미지 85개 URL은 확인할 첨부 범위다. '
    '앞서 확인한 PDF 63개 URL과 이미지 441개 URL의 범위는 유지한다. '
    '영상·소개 교재·인용 연구, 번역 동등성, 실제 게임 진행과 효과, 독립 검토·학생 응답은 후속 범위다.'
)

READING = '''
21-composing-numbers|에이스의 1과 11을 언제 바꿀지 지정한다. 10 카드의 값과 동률 처리는 본문의 나열에서 분명하지 않다.
add-it-up-composing-numbers|60+7과 50+2에서 10 묶음과 낱개를 말한다. 덧셈 예와 세부 절차가 없는 뺄셈 변형을 구별한다.
addingsubtracting-problem-types-deriver--composing-numbers|이전 교사자료와 같은 12개 예다. 비교에서 묻는 양과 시간에 따른 변화량을 구별한다.
addingsubtracting-problem-types-multidigit--composing-numbers|같은 교사자료 절차다. 웹 본문에는 기준량 미지수 예가 없고 이전에 확인한 연결 PDF에는 별도 예가 있다.
addingsubtracting-problem-types-problem-solver--composing-numbers|같은 교사자료 절차다. 마지막 비교 예에서 물건 명칭을 한 종류로 맞춘다.
all-together-stemie|조각을 맞춰 물체 하나를 만드는 것과 조각의 수를 더하는 것을 구별한다. 시범 전과 시범 뒤에 연결한 부분을 구분해 기록한다.
birthday-candles|케이크 네 개의 초가 각각 5개에서 6개로 바뀐다. 전체가 20에서 24로 늘어난 까닭을 묶음마다 1개씩 더하는 것으로 설명한다.
bunches-of-balloonscreative-problem-solving|풍선 묶음을 쓰려면 그 묶음의 모든 풍선을 채운다. 낱개 1이 없는 예의 불가능 판단을 다른 인쇄판에 일반화하지 않는다.
bunny-ears-composer-to-10|한 손 5개 이내라는 도구 조건을 확인한다. 두 손의 다른 배치와 그 배치가 나타내는 수 조합을 구별한다.
bunny-ears-composer-to-4-then-5|한 손 또는 두 손을 쓰는 예에서 한쪽 0을 표현할 수 있다. 손동작 외에 물건·가리키기 등으로도 양을 답할 수 있다.
chilly-cherry|20은 가득 찬 10칸 틀 두 개, 32는 10 세 묶음과 2개다. 주문 수를 읽는 것과 실제 수량을 검산하는 것을 구별한다.
compounding-cakes|생일 초 활동과 같은 중심 계산을 제시하고 케이크 그림을 준비물에 추가한다. 두 주소를 서로 다른 계산 근거로 세지 않는다.
cookie-game-composer-to-10|목표 10은 과자 한 개마다 적용한다. 5와 2가 있는 두 과자에는 각각 5와 8이 필요하다. 남는 칩을 다른 과자로 옮기는 범위를 지정한다.
cookie-game-composer-to-4-then-5|목표 4에서 1개가 있는 과자에는 3개, 2개가 있는 과자에는 2개가 필요하다. 주사위로 가져온 수와 실제 놓은 수를 구별한다.
cookie-game-composer-to-7|목표 7에서 5개와 3개에 각각 2개와 4개가 필요하다. 판 전체의 양과 과자 한 개의 양을 구별한다.
crossing-decades-composing-numbers|더하거나 빼는 수를 10의 배수로 지정한다. 낱개를 더해 다음 십을 만드는 과제와 조건을 구별한다.
decade-spin-composing-numbers|3·33·63에 각각 4를 더하는 예는 일의 합이 7이다. 받아올림이 있는 예까지 같은 방식으로 설명했는지 별도로 확인한다.
double-war-composer-to-20|제목과 달리 절차는 보이는 카드와 딜러가 말한 합으로 가린 카드를 찾는다. 준비 지시의 카드와 자료란의 수 카드 역할을 먼저 정한다.
figure-it-with-fingers-composer-to-4-then-5|곰 4마리 중 3마리가 떠나면 1마리가 남는다. 이 예는 시간에 따라 양이 변하며 정적인 두 부분 이야기와 구별한다.
find-a-partner|목표 7의 조합을 0·7부터 순서대로 놓는다. 카드가 어느 묶음에서 왔는지와 좌우 순서까지 서로 다르게 볼지 명시한다.
finger-games-composer-to-10|서로 다른 양을 양손에 놓으라는 지시와 4·4 예가 섞인다. 한 사람의 엄지를 제외하면 최대 8이며, 짝과 합치는 경우와 구별한다.
finger-games-composer-to-4-then-5|엄지를 제외하면 한 손에 4개까지 쓸 수 있다. 같은 5를 만들더라도 한 손 사용 가능 여부는 도구 조건에 달려 있다.
finger-games-composer-to-7|6은 3·3으로 나눌 수 있고 7은 두 손에 정수 개씩 같게 나눌 수 없다. 다른 손가락을 펴는 것과 양이 다른 조합을 구별한다.
go-10|카드를 모두 나눠 주고 필요한 짝을 상대에게 묻는다. 자료의 1~9 카드에서는 0+10이 나오지 않는다.
go-fish-for-tens|0~10 카드 세 묶음에서 0+10과 5+5를 허용한다. 처음 받은 카드와 가운데에서 새로 뽑은 카드를 구별한다.
go-round|11~19를 10 묶음 하나와 낱개로 나타낸다. 다른 재료로 같은 수를 만들 때 각 묶음이 실제로 10개인지 확인한다.
grid-race-deriver--composing-numbers|16에서 9칸 이동하면 25다. 99를 정확히 밟지 않아도 된다는 조건과 역방향 변형의 끝 규칙을 따로 적는다.
hiding-cubes|10개짜리 탑 세 개와 낱개 5개는 35개다. 가리기 전에 보인 양, 가린 뒤 첫 응답, 다시 열어 확인한 값을 기록한다.
how-many-sea-creatures-composer-to-10|한 종류를 하나 늘리고 다른 종류를 하나 줄이면 전체 10은 같다. 두 종류가 모두 있어야 하는지에 따라 0·10의 포함 여부가 달라진다.
jumping-to-100-multidigit--composing-numbers|목표의 십 주사위는 10·20·30이 두 번씩 나오고, 준비물은 10~60의 십 배수를 나열한다. 두 설정에서 가능한 이동과 종료가 다르다.
lucky-seven-composer-to-7|1~6에서 합 7인 무순서 짝은 세 가지다. 지원용 1~5에서는 1+6을 뺀다. 카드가 우연히 나오는 횟수와 전체 경우의 수를 구별한다.
make-a-match-composer-to-10|0~10의 두 세트를 쓰고 목표보다 큰 카드를 뺀다. 보수를 예상하는 것과 뒤집은 카드가 실제 그 수인지 확인하는 것을 구별한다.
make-a-number|목표 설명은 목표 이상을 빼고 새 카드를 펼친 카드와 맞추도록 한다. 본 절차는 목표보다 큰 카드만 빼고 두 장을 뒤집는다. 목표와 같은 카드, 0의 포함, 낱장 사용 규칙을 먼저 정한다.
make-me-100-multidigit--composing-numbers|47을 100으로 만드는 양은 53이다. 카드가 숫자마다 한 장이면 66 같은 보수를 만들 때 별도 표기 수단이 필요하다.
math-with-motion-composing-numbers-composer-to-20|앞줄의 0~10 카드가 한 장씩이라 5+5는 두 사람 짝으로 만들 수 없다. 세 수를 쓰는 변형과 뒤쪽 확인자가 실제로 참여할 조건을 구별한다.
musical-fingers|코끼리가 하나씩 더해져 다섯이 되는 이야기를 수로 말한다. 노래 동작을 따라 하는 것과 전체 수를 설명하는 것을 구별한다.
number-soup-composer-to-4-then-5|한 색에서 하나씩만 넣으면 두 개다. 목표 4의 예로는 4+0·3+1·2+2 등 실제 네 개가 되도록 보충한다.
numbers-in-nature--stemie|잎과 줄기, 가지와 잎 등 어느 물체가 전체인지 지정한다. 식물의 이름을 말하는 수행과 부분을 찾는 수행을 구별한다.
piggy-bank-composer-to-10|7센트와 3센트를 모아 10센트를 만든다. 카드 장수, 그림에 보이는 동전 수, 액면 합을 따로 세고 승리 점수 단위를 정한다.
piggy-bank-composer-to-4-then-5|2센트와 3센트를 모아 5센트를 만들 수 있다. 한 동전이 그 목표 액면을 나타내는 경우도 카드 한 장으로 처리한다.
pour-and-sing-to-7|흔드는 횟수 7과 칩의 총수 7을 구별한다. 보이는 두 색의 합은 같은 칩이 빠지거나 더해지지 않는 경우 7이다.
race-to-100-composing-numbers|100에 가까운 전체를 세고 100에 필요한 수를 따로 구한다. 제목과 달리 본문에는 경쟁 종료 규칙이 따로 없다.
roll-the-die--composer-to-4-then-5|5를 4·1 또는 5·0으로 나타낸다. 목표 범위를 5까지로 잡을 때 주사위에서 6이 나오는 경우를 정한다.
salute-composer-to-20|세 사람 중 한 사람이 합을 말하고 나머지가 각자 가린 값을 찾는다. 더블 워 제목의 활동과 같은 핵심 절차를 공유한다.
slap-a-ten-composer-to-10|목표·절차의 1~10 카드와 준비물의 0~10 카드가 다르다. 10 카드를 짝으로 쓰려면 0이 필요하며, 낱장으로 쓰는 규칙은 별도로 정한다.
snap-composer-to-7|보이는 4개와 숨긴 3개가 전체 7이다. 오류를 고치는 시범의 ‘4’ 반복을 빼고 한 물건당 한 수를 말한다.
span-decades-composing-numbers|13+7은 다음 십에 닿고 23+9는 넘어간다. 십까지 채운 수와 나머지를 각각 확인한다.
spill-the-beans-making-ten-composer-to-10|10개 칩에서 윗면 색을 구별한다. 놀이에서 관찰한 조합과 양끝 0·10을 포함한 가능한 조합 전체를 따로 확인한다.
split-them-up|물건 8개를 두 부분에 겹치거나 빠짐없이 나눈다. 두 부분을 모두 써야 하는지 먼저 정하고 다시 모아 전체를 확인한다.
subitize|2초 동안 보인 점의 수를 떠올리는 답과 나중에 네 보기 중 그림을 고르는 답을 구별한다.
talk-it-out-composing-numbers|35+57은 92다. 빈 수직선에 표시한 시작값과 이동한 양, 도착값을 각각 설명한다. 그림 자체의 배치는 첨부 확인 범위다.
ten-spot-composing-numbers|십을 더하거나 뺀다는 말은 10개짜리 묶음을 단위로 센다는 뜻이다. 5칸 틀 한 장을 바로 10으로 세지 않는다.
tens-memory-game|1~9의 두 배열에서 하나씩 골라 합 10을 찾는다. 각 배열에 5가 한 장씩 있어 5+5가 가능하다.
the-sneaky-snake--composer-to-4-then-5|구슬 5개 중 4개가 보이면 1개가 가려졌다. 숨긴 수의 예상과 천을 걷어 확인한 응답을 구별한다.
the-sneaky-snake-composer-to-10|보이는 6개와 가린 4개는 전체 10개다. 보이는 수가 달라져도 줄의 구슬이 빠지지 않으면 전체는 같다.
tic-tac-total-cn|두 0은 별개의 사용 기회다. 한 줄에 상대의 수를 합산할지와 홀수 목표가 가능한 줄 구성을 따로 정한다.
toy-bag-parts-in-a-whole|가방 속 수의 첫 짐작, 두 종류의 수를 알려 준 뒤의 합, 펼쳐서 한 개씩 세는 검산을 구별한다.
turn-over-ten|가운데 더미에서 공개한 카드와 이미 펼쳐 둔 카드도 짝의 후보가 된다. 새로 뒤집지 않고 공개된 두 장을 고를 수 있는 차례를 따로 센다.
up-and-down-composer-to-10|두 손의 10개 중 8개가 펴져 있으면 2개가 접혀 있다. 왼쪽부터 세는 활동이 수 방향에 관한 보편성을 입증하지는 않는다.
up-and-down-composer-to-4-then-5|3개를 펴고 2개가 접혔다는 답은 한 손의 5개를 전체로 잡을 때다. 다른 손의 손가락까지 세는 규칙과 구별한다.
wake-up-sleeping-giants-composer-to-10|2·3·4를 더한 9를 4와 5의 카드로 바꿀 수 있다. 주사위 하나의 중복 사용과 이미 뒤집힌 카드의 상태를 따로 관리한다.
wheres-its-buddy|두 물건이라는 수와 함께 쓰는 한 쌍이라는 조건을 구별한다. 장갑과 장화는 둘이지만 같은 종류의 짝이 아니다.
'''

CLAIMS = [
    ('LT64', ['2수01-04', '2수01-05'], [7, 19, 20, 22, 28, 34, 36, 40, 47, 48],
     '고정된 전체를 두 부분으로 나누는 경우를 정리할 때 순서, 0, 사용 가능한 물건 수를 먼저 정한다. 손가락이나 카드의 제약이 바뀌면 나타낼 수 있는 조합도 바뀐다.',
     '색을 바꾸어 두 순서로 기록하는 활동과 크기만 같아 같은 조합으로 보는 활동은 서로 다르다. 한 사람의 두 손에서 엄지를 빼는 조건을 여러 사람이나 별도 물건으로 바꾸지 않는다.'),
    ('LT65', ['2수01-04', '2수01-05', '2수01-09'], [23, 24, 30, 31, 32, 44, 52, 57],
     '목표 합을 아는 것과 실제 카드에서 그 짝을 만들 수 있는 것을 구별한다. 목표와 같은 값의 카드, 0, 같은 값의 카드 두 장이 각각 있는지 확인한다.',
     '목표 이상을 제외한다는 안내와 목표보다 큰 수만 제외한다는 절차를 합치지 않는다. 1~10 카드와 0~10 카드의 차이도 결과에 반영한다.'),
    ('LT66', ['2수01-02', '2수01-06', '2수01-08'], [1, 10, 15, 16, 25, 26, 27, 29, 33, 41, 46, 50, 51],
     '십 묶음, 낱개, 현재 위치의 합을 각각 나타낸다. 100까지 이동하는 놀이에서 십 주사위의 눈 목록에 따라 도달 가능한 위치를 따로 계산한다.',
     '목표와 준비물에 적힌 서로 다른 눈 목록을 같은 것으로 읽지 않는다. 100에 닿거나 넘어서면 끝나는 규칙과 100에 정확히 닿는 경우를 구별한다.'),
    ('LT67', ['2수01-10', '2수01-11'], [6, 11, 61],
     '케이크 네 개에 초가 5개씩 있을 때 각 케이크에 초를 하나 더하면 전체는 4개 늘어난다. 묶음 수를 유지하고 한 묶음의 크기를 바꾸는 관계다.',
     '한 묶음에만 1개를 더하는 상황과 구별한다. 두 주소에서 같은 중심 절차를 제공하므로 별개 효과 근거로 세지 않는다.'),
    ('LT68', ['2수01-04', '2수01-07', '2수01-08', '2수01-09'], [17, 18, 43, 45, 49, 53, 54, 55, 56, 60],
     '알려 준 전체와 보이는 부분으로 가린 값을 구해 다시 합하여 확인한다. 세 수를 쓰는 놀이에서는 숫자 값, 실제 사용 횟수, 상대가 놓은 칸을 합에 넣는 조건을 정한다.',
     '가린 값을 처음 예상한 응답과 가림을 푼 뒤 센 응답을 구별한다. 합이 홀수라는 사실만으로 그 줄의 수를 모두 같은 사람이 놓았다고 볼 수 없다.'),
]

OBSERVATIONS = [
    dict(id='LT-P56', standard_codes=['2수01-04'],
         question='한 사람의 두 손에서 엄지를 빼면 손마다 네 손가락을 쓸 수 있다. 8을 만들면서 두 손에 서로 다른 개수를 펼 수 있는가? 엄지를 다시 써도 되면 어떤 방법이 생기는가?',
         expected='엄지를 빼면 한 손 최대 4개여서 8은 4+4뿐이다. 엄지를 쓰면 5+3과 3+5로 서로 다르게 펼 수 있다. 4+4도 여전히 가능하다.',
         interpretation='좌우 위치를 바꾼 표시와 서로 다른 수의 짝을 구별한다. 손동작 대신 같은 제한을 둔 4칸·5칸 판으로 설명할 수 있다.', student_validated=False),
    dict(id='LT-P57', standard_codes=['2수01-04', '2수01-09'],
         question='0부터 7까지 카드가 한 장씩 있다. 서로 다른 두 카드를 골라 7을 만든다. 규칙 가에서는 7 이상, 나에서는 7보다 큰 카드를 먼저 빼기로 한다. 두 규칙에서 만들 수 있는 짝을 순서를 무시하고 모두 적어라.',
         expected='가에서는 1+6, 2+5, 3+4가 가능하다. 나에서는 세 짝에 0+7이 추가된다. 가에서 0에 필요한 짝은 7인데 그 카드가 빠져 있다.',
         interpretation='계산으로 가능한 보수와 카드가 실제로 있는 경우를 구별한다. 첫 카드가 작아지는 짝을 차례로 찾아 누락과 중복을 확인할 수 있다.', student_validated=False),
    dict(id='LT-P58', standard_codes=['2수01-02', '2수01-06', '2수01-08'],
         question='말이 57에 있다. 낱개 주사위는 1~6이다. 십 주사위 가는 10·20·30이 두 번씩, 나는 10·20·30·40·50·60이 한 번씩 있다. 각 주사위에서 나온 수를 현재 위치에 한 번씩 더할 때, 어느 설정에서 이번 차례에 정확히 100에 닿을 수 있는가?',
         expected='57에서 100까지 43이 필요하다. 가에서 가장 큰 이동은 30+6=36이라 93까지만 간다. 나는 40과 3으로 57+40+3=100을 만들 수 있다.',
         interpretation='남은 거리, 십과 낱개의 합, 선택할 수 있는 눈을 각각 확인한다. 넘으면 끝나는 규칙으로 바꿨을 때 40과 4도 가능한 종료 사례로 설명할 수 있다.', student_validated=False),
    dict(id='LT-P59', standard_codes=['2수01-10', '2수01-11'],
         question='케이크 네 개에 초가 5개씩 있다. 가에서는 네 케이크 모두에 한 개씩 더 넣고, 나에서는 케이크 하나에만 한 개를 더 넣는다. 두 경우 전체는 각각 몇 개인가? 언제 6개씩 네 묶음으로 셀 수 있는가?',
         expected='처음에는 5개씩 네 묶음으로 20개다. 가는 4개 늘어 24개이고 6개씩 네 묶음이다. 나는 1개 늘어 21개이며 6개짜리 하나와 5개짜리 세 묶음이다.',
         interpretation='케이크의 수와 케이크당 초의 수를 따로 설명한다. 같은 수만큼 든 묶음이 유지되는 경우에만 그 크기의 반복으로 나타낸다.', student_validated=False),
    dict(id='LT-P60', standard_codes=['2수01-08', '2수01-09'],
         question='세 칸 줄에 2와 4가 있고 한 칸이 비었다. 세 칸에 있는 수의 합을 9로 만들려면 어떤 수가 필요한가? 짝수만 놓는 차례라면 그 수를 놓을 수 있는가? 홀수만 놓는 사람이 그 칸에 놓고 세 칸 모두의 수를 합산하는 규칙이면 어떠한가?',
         expected='2+4=6이고 3이 더 필요하다. 3은 짝수 차례에는 놓을 수 없다. 홀수 차례에 3을 놓으면 2+4+3=9가 되므로 세 칸 모두를 쓰는 규칙에서는 목표를 만족한다.',
         interpretation='빈칸에 필요한 값을 먼저 구한다. 실제 차례가 허용하는 값, 어느 사람이 둔 수인지, 줄의 합산 규칙을 구별한다.', student_validated=False),
]


def verify_examples():
    assert [(a, b) for a, b in combinations_with_replacement(range(5), 2) if a + b == 8] == [(4, 4)]
    assert [(a, b) for a, b in combinations_with_replacement(range(6), 2) if a + b == 8] == [(3, 5), (4, 4)]
    pairs = [{(a, b) for a, b in combinations(range(stop), 2) if a + b == 7} for stop in (7, 8)]
    assert pairs == [{(1, 6), (2, 5), (3, 4)}, {(0, 7), (1, 6), (2, 5), (3, 4)}]
    advances = [{a + b for a, b in product(range(1, 7), tens)} for tens in (range(10, 31, 10), range(10, 61, 10))]
    assert max(advances[0]) == 36 and 43 not in advances[0] and 43 in advances[1]
    assert 4 * 5 + 4 == 4 * 6 == 24 and 6 + 3 * 5 == 21
    assert [n for n in range(10) if 2 + 4 + n == 9] == [3]
    return [sorted(values) for values in advances]


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
                        and any('/math/composing-numbers/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|', 1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 62
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/', 1)[-1] for row in pages] == [row[0] for row in reading]
    assert {procedure_fingerprint(row['body']) for row in bodies[2:5]} == {TEACHER_SHA}
    assert '10, 20, 30, 10, 20, 30' in bodies[29]['body'] and '10, 20, 30, 40, 50, 60' in bodies[29]['body']
    assert '7 or more' in bodies[32]['body'] and 'higher than that number' in bodies[32]['body']
    assert '1–10 cards' in bodies[44]['body'] and '0- 10' in bodies[44]['body']
    advances = verify_examples()

    old_images = {row['url'] for row in prior['image_read_manifest']}
    old_pdfs = {row['url'] for row in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for i, (page, body, (_, note)) in enumerate(zip(pages, bodies, reading)):
        url = page['url']
        assert page['status'] == 200 and page['final_url'] == url and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256'] and '\nActivity\n' in body['body']
        teacher = 'Type:\nTeacher Resources' in body['body']
        assert teacher == (2 <= i <= 4)
        groups['teacher_resources' if teacher else 'activities'].append(page['key'])
        logs.append(dict(url=url, page_kind='teacher_resource' if teacher else 'activity_procedure', note=note))
        linked_images = {urljoin(url, image['src']) for image in page['images'] if '/upload/' in image.get('src', '')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert len({url for links in images.values() for url in links}) == 85
    assert len({url for links in pdfs.values() for url in links}) == 19
    assert {k: len(v) for k, v in groups.items()} == dict(general=6, domain_overviews=20, levels=224, activities=361, teacher_resources=16)
    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key', 'url', 'title', 'sha256', 'status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 627
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'], followup['listed_body_pending']) == (377, 447)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
                 observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
                 catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies': 377, 'pending_activity_bodies': 447},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=59, teacher_resources=3, inline_images=0, supplementary_pdf_urls=0),
                 composing_number_reading_log=logs, completed_composing_number_records=selected,
                 composing_number_pdf_urls_not_reviewed=pdfs, composing_number_image_urls_not_reviewed=images,
                 composing_number_procedure_scope=dict(activity_procedures=59, teacher_resources=3),
                 composing_number_repeated_problem_types=dict(urls=[row['url'] for row in pages[2:5]], normalized_sha256=TEACHER_SHA, example_count=12),
                 composing_number_cube_check=dict(url=pages[29]['url'], unit_faces=[1, 2, 3, 4, 5, 6],
                                                  objective_tens_faces=[10, 20, 30, 10, 20, 30], materials_tens_faces=[10, 20, 30, 40, 50, 60],
                                                  reachable_advances_from_objective=advances[0], reachable_advances_from_materials=advances[1]),
                 reading_log=prior['reading_log'] + ['수의 합성·분해와 연결된 영어 페이지 62개의 목표·활동 절차·준비물을 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='composition_capacity_and_material_rules', locations=[pages[i]['url'] for i in (20, 29, 32, 34, 36, 44, 45, 55)],
                     action='손·카드로 나타낼 수 있는 수, 목표 수 카드의 제외 여부, 준비물의 주사위 눈, 목표 4와 두 물건의 수, 하나씩 세는 시범을 각각 구별했다.')],
                 unread_followups=[LIMITS, '수의 합성·분해 첨부와 수량 비교 활동의 본문을 우선 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
                  method_note='영어 목표·절차·준비물과 사용 조건을 대조했다. 반복된 교사자료와 다른 도구 규칙을 구별했다.',
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
    print('Reviewed 62 English pages; added 5 mappings and 5 observations. Public activity bodies pending: 447.')


if __name__ == '__main__':
    main()

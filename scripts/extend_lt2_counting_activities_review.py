"""Record the English goals and procedures of the remaining LT2 counting pages."""
import copy
import hashlib
import json
from urllib.parse import urljoin, urlparse

from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_length_assets_review_notes.json'
PRIOR_SHA = '23a50001b3bf5fc78d74f374e153c4f466181ace4b6bf421cc611aaa3804dc6b'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_counting_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-counting-activities'
SCOPE = (
    '공개 영어 HTML 494개를 대조했다. 일반 6·영역 개요 20·수준 224·활동 241·교사자료 3개다. '
    '세기 수준에 연결된 미검토 89개 페이지의 영어 목표와 활동 절차를 확인했다. '
    '활동 절차 87개, 책 읽기 제안 1개, 교사자료 1개다. 기록된 활동과 교사자료 824개 중 공개 본문 244개를 확인했고 580개가 남았다.'
)

READING = '''
a-bounty-of-counting|일상의 2~5개 모임을 스스로 알아본 경우와 지시 뒤 찾은 경우를 구별한다. 출처가 인용한 연구는 별도다.
a-scoop-for-every-cone|콘마다 하나씩 놓은 대응과 사용한 토큰 총수를 따로 확인한다.
acting-out-songs-and-poems--reciter|노래 순서, 시범을 따라 하나씩 놓기, 모임의 전체 개수를 말하기를 구별한다.
animal-spots|주사위 점 읽기, 그 수만큼 모으기, 함께 고치기를 나눈다. 도입과 참고문의 연도 표기가 달라 판본을 확인해야 한다.
beanbag-counting|던진 사건과 잡은 사건을 구별한다. 절차에서는 잡는 순간에 세므로 놓친 시행과 운동 도움을 기록한다.
big-fish-story-counter-from-n|빈 그릇의 0, 하나 추가·제거, 모두 치워 0으로 되돌리는 장면을 구별한다. 기존 수에서 이어 세는 것과 전부 다시 세는 것은 다른 전략이다.
blast-off|10부터 0까지의 수말 11개와 10번의 한 칸 이동을 구별한다. 0은 출발 신호이기도 하며 뛰는 동작은 대체할 수 있다.
blooming-flowers|목표에는 0까지라고 쓰였으나 절차는 10에서 1까지다. 끝 수를 지정하고 시범과 독립 응답을 구별한다.
busy-beaver-10s-skip-counter-by-10s-to-100|막대 10개, 10짜리 묶음 1개와 같은 양이다. 두 묶음은 20개다. 영어 수말 관습을 한국어의 자릿값 판정에 옮기지 않는다.
busy-beaver-counter-beyond-100|110에 10을 더하면 120이다. 한 묶음을 풀어 120 뒤에서 121부터 130까지 열 번을 확인한다. 10묶음과 100묶음의 규격을 섞지 않는다.
buying-candy-bars-counter-of-quantitative-unitsplace-value|지폐 수와 액면 합을 구별한다. 1달러당 물건 하나라는 가정에서만 두 수가 같다. 액면 5·10·1에 맞춰 더한다.
chocolate-chips-to-10-counter-10|주문 수 5와 점 5개가 대응한다. 중간에 점 1개짜리를 고르라는 지시는 그 뒤 세는 수 5와 충돌한다.
chocolate-chips-to-5-counter-small-number|주문 1에는 점 1개, 주문 4에는 점 4개를 맞춘다. 즉시 알아보기와 하나씩 세기를 따로 관찰한다.
concentration-game-dots-to-10|점 카드와 수 카드의 값이 같아야 짝이다. 뒤집은 카드 위치 기억과 수의 대응은 다른 수행이다.
cookie-game-producer-small-number|주사위 값만큼 검사 접시에 놓고 확인한 뒤 판으로 옮긴다. 남은 칸보다 더 큰 수가 나온 경우의 처리 규칙은 본문에서 확정되지 않는다.
count-and-move-with-patterns-reciter-10|손뼉과 발 구르기의 반복 단위와 전체 동작 수를 구별한다. 교사와 함께 맞춘 속도나 몸짓만으로 독립 세기를 판정하지 않는다.
count-the-days-of-school-counter-beyond-100|기준은 등교일이다. 33일은 3개의 10과 3개의 1로 나타낼 수 있다. 100·200에 표시하는 것과 100 묶음을 이해하는 것은 따로 확인한다.
count-the-days-of-school-to-100-counter-to-100|29 다음은 30이다. 33을 셀 때 10·20·30 뒤에는 31·32·33을 잇는다. 배열 색만 보고 답했는지 따로 확인한다.
countdown-game|10~0은 수말이 11개다. 원형 자리에서는 참가자가 적으면 같은 사람을 다시 가리킬 수 있어 고유 인원 수를 세는 활동과 구별한다.
counting-books-number-word-sayer-foundations|그림의 수량 표현과 실제로 세어 붙인 수를 구별한다. 언급된 책 본문과 일대일 세기 수행은 이 페이지에서 확인하지 않는다.
counting-counting-counting-counter-10|어느 사람이나 물건을 세는지 모임 경계를 먼저 정한다. 합창에 참여한 사실을 독립 세기와 구별한다.
counting-jar-counter-10|날마다 같은 통이라도 내용 개수는 바뀔 수 있다. 물건을 세는 것, 전체를 말하는 것, 기록하는 것을 나눈다.
counting-wand-what-comes-next|차례를 넘길 때 앞사람의 마지막 수를 다시 세지 않고 그 다음 수부터 잇는다. 정방향과 역방향을 지정한다.
cross-the-stream-or-very-big-hop-scotch|출발 칸을 0번 이동으로 본다. 먼저 도착 칸을 예상한 경우와 칸을 실제로 짚어 확인한 경우를 구별한다.
cubes-in-boxes-producer-small-numbers|주문 수만큼 만들어 넣기, 상자 표지 쓰기, 다른 사람이 표지를 골라 실제 수량을 확인하기를 구별한다.
decade-dimmers-to-100-counter-to-100|17과 71처럼 자리 교환을 구별한다. 0을 앞에 붙인 표기는 두 자리 자연수로 세지 않으며, 시작이 이미 10의 배수일 때 다음 목표를 지정한다.
diez-amigos-finger-play|수말과 하나씩 펴는 손가락의 순서를 구별한다. 스페인어 노래 따라 하기는 한국어 수말이나 전체 개수의 독립 설명과 다르다.
ding-clink-bam-corresponder|한 소리에 토큰 하나를 대응한다. 소리가 겹치거나 기다리는 시간이 짧으면 사건을 분리한다. 일대일 대응과 마지막 수가 뜻하는 전체를 구별한다.
exploring-counting-materials|재료 탐색과 교사가 말해 준 수량 표현을 구별한다. 두 눈과 입을 합칠 때 세는 전체의 범위를 먼저 정한다.
feed-the-puppet|교사의 하나씩 먹이는 동작을 따라 한 것과 수말을 사용해 스스로 목표 수만큼 만드는 것을 구별한다.
fill-the-egg-cartons|자리를 보고 바로 채우는 일과 필요한 수를 듣고 별도 쟁반에 먼저 만드는 일을 나눈다. 마지막에 자리에 배치해 확인한다.
five-little-fingers-finger-play-counter-small-numbers|편 손가락 수, 손가락 이름, 전체 수말을 구별한다. 손 사용이 어렵다면 그림이나 표시물로 바꿀 수 있다.
follow-me|3에서 2만큼 커지는 두 번의 이동은 4와 5다. 출발 수, 이동 횟수, 도착 수를 각각 기록한다.
get-just-enough-counter-and-producer-10|사람 수를 먼저 정하고 떨어진 곳에서 필요한 물건을 한꺼번에 가져와 나눈다. 빈자리마다 하나씩 왕복하는 절차와 다르다.
get-just-enough-small-number|5 이하의 모임에서 필요한 수를 기억해 만들어 오는 활동이다. 교사나 또래가 먼저 말한 답과 학생이 독립적으로 정한 수를 구별한다.
get-on-the-bus|제공된 장난감 10개, 좌석 대응, 함께 말한 수를 따로 본다. 버스 인쇄물은 별도다.
gone-swimming|가린 5개에 보이는 4개를 붙이면 6부터 9까지 이어 센다. 매 시행 모두 비웠는지 확인하고 가리기 전후 설명을 기록한다.
growth-spurt|0에서 시작해 다시 0까지 돌아온다. 7이나 9부터의 거꾸로 세기도 같은 구조인지 별도로 확인한다.
hop-to-the-finish-counter-on-keeping-track|두 주사위 4와 3의 합 7을 먼저 정한다. 출발 칸은 이동으로 세지 않고 7칸 움직인다. 정확히 끝나야 하는지는 판 규칙을 확인한다.
how-many-am-i-hiding-counter-10|가리기 전 본 수량, 가린 뒤 기억, 다시 확인한 개수를 구별한다.
how-many-am-i-hiding-counter-small-numbers|목표는 교사가 숨은 것을 센다고 요약하지만 절차에서는 아이가 보이는 것을 먼저 센다. 다시 보인 뒤 답을 최초 응답으로 소급하지 않는다.
how-many-in-the-box-now-counter-from-n-n1-n-1|가린 상자에 하나씩 더하는 절차다. 수준 이름에 뺄셈이 있더라도 이 본문에 없는 제거 절차를 읽은 것으로 세지 않는다.
how-many-in-the-box-now-counter-on-using-patterns|4에 2를 더하면 6이다. 소리 두 번, 손가락 두 개, 두 번 이어 세기, 모두 다시 세기를 비교한다. 다시 설명할 때 물건을 초기 상태로 돌렸는지 확인한다.
how-many-now-counter-from-n-n-1-n--1|현재 5개에 1개를 더하고 새 전체를 설명한다. 시작값을 바꾸는 새 시행과 같은 모임에 계속 더하는 시행을 구별한다.
how-many-now-counter-on-using-patterns|가린 3개에 2개를 넣으면 5개다. 같은 모임에 2개를 실제로 다시 넣으면 7개가 되므로 5를 재현할 때 초기 상태를 복구한다.
how-many-now-hidden-version-counter-from-n-n-1-n--1|가린 5개에 하나씩 더하고 필요할 때만 꺼내 확인한다. 모둠 답을 듣기 전후와 기억에 도움을 받은 경우를 구별한다.
how-to-sprinkle-math-into-read-alouds-with-young-children-number-word-sayerfoundations|교사자료다. 그림을 짚어 센 뒤 전체 이름을 붙이는 제안을 확인했다. 인용된 성취 관련 연구나 인과 효과를 별도로 검증하지 않았다.
jumping-on-a-number-line--counter-forward-and-back-10s-and-1s|빈 수직선은 표기한 이동값과 도착 수가 중요하다. 호의 실제 길이는 축척이 아니며 표준 수직선의 같은 간격과 구별한다.
knock-it-down-|쌓은 블록을 흩뜨려도 추가·분실이 없으면 개수는 같다. 10칸 판으로 확인하기와 확인 전 설명을 구별한다.
lets-count-to-five-reciter|일상 놀이의 5 이하 모임이다. 교사와 함께 수를 말하기, 물건을 각각 짚기, 전체를 보고하는 것을 구별한다.
little-birds|한 마리 추가와 손가락 하나를 맞춘다. 5에서 6으로 갈 때 손이 바뀌어도 전체 모임은 이어진다.
magicians-trick-counter-and-producer-10|처음 절차는 1부터 위치를 세고 해설은 기준 카드에서 이어 세기를 언급한다. 앞에 0 카드를 두면 1의 위치가 바뀌는 조건을 기록한다.
magicians-trick-counter-from-n-n-1-n-1|뒤집어 보이는 기준 카드 앞·뒤에서 이어 센다. 맨 끝 카드에서는 그 방향의 다음 칸이 없을 수 있다.
make-a-number-counter-and-producer-10|같은 목표 수를 여러 재료로 배열한다. 모양이 다른 결과라도 각각 같은 수인지 확인하고 수정 전후를 기록한다.
mealtimes-number-word-sayer-foundations|놓아 준 양, 먹은 양, 남은 양을 구별한다. 한 개 더 달라는 표현을 정확한 전체 수 보고로 간주하지 않는다.
memory-match-counter-10|두 카드가 다른 배열이어도 점 개수가 같으면 짝이 된다. 카드 색과 위치 기억은 수량 판정과 다르다.
mr-mix-up-catch-the-mistake|인형이 일부러 수말을 생략하거나 반복한다. 수말 순서 오류와 물건을 두 번 짚는 오류를 구별한다.
mr-mixup-counter-10|센 마지막 수 다음 수를 전체라고 말하는 오류를 비교한다. 다시 세는 행동만으로 전체 수의 뜻을 모른다고 확정하지 않는다.
mr-mixup-counter-small-numbers|목표는 5 이하지만 본문 예에 6과 10이 있다. 실제 제시 범위를 지정하고 인형의 의도적 오답을 올바른 규칙으로 옮기지 않는다.
my-very-own-10|크기와 종류가 다른 물건도 각각 10개일 수 있다. 가정 물건의 종류나 공개 여부를 수학 수행 판정에 쓰지 않는다.
mystery-boxes|상자에 넣은 수를 기억하는 것, 표지를 읽는 것, 열어 다시 세는 것을 구별한다. 교사가 표지를 썼는지도 기록한다.
number-flip-counter-from-n|1~20의 순서에서 바로 앞이나 뒤를 예상해 뒤집는다. 경계에서 바깥 카드가 있는지와 한 칸 간격을 확인한다.
number-flip-to-100-counter-to-100|39·40·41 전후를 양방향으로 비교한다. 교사의 말 늘이기와 보이는 카드의 도움을 독립 응답에서 분리한다.
number-moves|수 카드 읽기와 그 수만큼 움직여 멈추기를 따로 관찰한다. 움직임 종류나 발화 방식은 바꿀 수 있다.
number-path-race|은행 역할이 요청받은 개수를 만들고, 다른 역할이 칸에 놓고 말을 옮긴다. 거리 비교에는 공통 종점과 남은 칸을 사용한다.
number-scenes|장면에 놓인 사물 중 어떤 것을 세는지 먼저 정한다. 말의 풍부함과 개수의 일대일 대응은 다른 관찰 항목이다.
rhythmic-counting-corresponder|박자에 동작 하나씩을 맞춘다. 느리게 말하거나 다른 동작을 선택해도 대응 관계는 같다.
shopkeeper-fill-orders-to-5|요청량, 실제로 꺼낸 물건, 지불액을 구별한다. 예에서 물건 한 개에 1달러라는 조건을 명시해야 두 수가 일치한다.
shopkeeper-sort-and-label-to-5|먼저 분류 기준을 정하고 용기별 개수를 표지한다. 용기에 기록된 수와 전체 물건 수를 구별한다.
simon-says-corresponder|지시 신호를 알아듣는 것과 요청된 횟수만큼 동작하는 것을 분리한다. 소개한 실행 기능 효과의 근거는 별도다.
skip-counting|같은 크기의 묶음에서만 일정한 간격으로 센다. 예의 사람 수나 손가락 수를 일반적인 신체 가정으로 강제하지 않는다.
skip-counting-ourselves-skip-counter|10씩 10묶음이면 100이다. 동작 수와 묶음 수를 정한다. 다른 수준 주소의 같은 활동 설명과 별개의 연구로 합산하지 않는다.
skip-counting-ourselves-skip-counter-by-10s-to-100|10을 더하는 단위 묶음을 드러낸다. 6묶음은 60이며 인접 주소의 같은 절차가 독립 활동 근거를 늘리지 않는다.
skip-counting-with-cubes|막대를 모두 놓기 전후에도 묶음 크기가 같아야 한다. 묶음 수와 한 묶음 크기를 구별하고 10짜리와 5짜리를 섞으면 따로 더한다.
skip-with-me|5개씩 두 묶음을 합쳐 10을 만든다. 묶음 안의 개수, 묶음 수, 전체를 분리해 설명한다.
sneaky-swiper-counter-from-n-n-1-n--1|5에서 하나를 빼 4, 같은 하나를 되돌려 5다. 빼지 않은 통과 바뀐 통을 함께 비교한다.
take-away-songs|한 번에 하나가 줄어드는 이야기와 0을 실제로 말하거나 표시하는 절차를 구별한다. 두 노래가 0을 같은 방식으로 표현하지 않는다.
the-count-how-many-board-counter-small-numbers|다른 물건에서 같은 개수를 찾고 한 개 추가·제거 전후를 비교한다. 책이나 첨부의 전체 내용을 읽은 것으로 세지 않는다.
the-how-many-box|한 칸을 열고 그 모임의 물건을 센다. 각 칸의 수와 여러 칸을 합한 전체를 구별한다.
the-hungry-caterpillar|그림책에서 수량을 말해 보는 짧은 제안이다. 책 전체, 마지막에 먹는 양의 실제 비교, 상세 교수 절차를 확인하지 않았다.
the-ten-museum-counter-and-producer-10|먼저 10개를 만들어 멈추고, 모둠 앞에서 세어 확인한다. 최초 만든 수량과 확인 뒤 수정한 결과를 구별한다.
this-old-man-songs-and-finger-plays|노래의 구절과 몸짓이 여러 번 반복된다. 구절 수말, 실제 손뼉 수, 별도로 셀 물건 수를 한 양으로 취급하지 않는다.
tricky-fox-number-conserver|4개 줄을 7개 줄보다 길게 펼쳐도 4가 더 크지 않다. 위치만 바뀌었는지와 재계수 전 설명을 확인한다.
two-little-butterflies-finger-play-number-word-sayer-foundations|보이는 손과 표현한 나비 수를 구별한다. 숨긴 경우와 없어진 경우를 같은 사건으로 다루지 않는다.
vegetable-market|품목별 주문량과 가져온 수를 비교한다. 정액 결제와 개당 단가 계산은 별도 확장이다.
whats-hiding-counter-10|서로 다른 개수의 통을 옮긴 뒤 위치를 고르는 것과 통 안의 수를 세는 것을 구별한다.
whats-hiding-reciter-10|숨긴 모임을 예상하고 실제로 확인한다. 외운 위치나 한 번 맞힌 답으로 수말 순서와 전체 수 설명을 모두 판정하지 않는다.
whats-missing-counter-from-n-n1-n-1|연속 카드에서 하나를 없앤 경우다. 빈자리를 남겼는지, 양쪽 수가 보이는지, 양 끝 카드인지에 따라 단서가 달라진다.
when-i-was-one|손가락으로 표현한 나이와 실제 개인의 발달 시기를 구별한다. 이야기의 예를 현재 아이의 발달 규준으로 사용하지 않는다.
'''

CLAIMS = [
    ('LT45', ['2수01-01', '2수01-03'], [6, 7, 15, 18, 22, 37, 56, 61, 62],
     '수말의 순서, 시작 수와 끝 수, 한 번 이동하거나 제거할 때 바뀌는 수를 각각 명시한다. 0에서 멈추는 절차와 1에서 멈추는 절차를 구별한다.',
     '함께 수를 말하거나 동작을 따라 한 사실만으로 0의 뜻, 전체 개수 또는 독립적인 순서 이해를 판정하지 않는다.'),
    ('LT46', ['2수01-01', '2수01-04'], [1, 11, 12, 24, 27, 28, 30, 33, 34, 46, 53, 58, 80, 82],
     '수 카드가 지정한 수량, 물건을 한 번씩 짚기, 전체를 말하기, 그 수만큼 따로 모으고 검산하기를 구별한다. 서로 다른 부분을 합친 모임에서도 부분 수와 전체 수를 확인한다. 주문 5와 점 1개를 연결한 지시는 점 5개를 세는 예와 충돌한다.',
     '정답 뒤 도움을 받거나 일대일로 채워 얻은 결과를 처음부터 주어진 수만큼 만들어 멈춘 수행으로 기록하지 않는다.'),
    ('LT47', ['2수01-02', '2수01-03'], [8, 9, 10, 16, 17, 25, 51, 52, 62],
     '낱개와 묶음, 액면과 지폐 장수, 카드 값과 배열에서의 위치를 구별한다. 자리 교환과 십의 경계를 확인할 때 두 자리 수의 조건과 기준 칸을 명시한다.',
     '숫자 0을 앞에 붙여도 두 자리 자연수가 되지는 않는다. 100 이후의 해외 활동이나 영어 수말 관습을 국내 해당 기준의 일괄 요구로 옮기지 않는다.'),
    ('LT48', ['2수01-05', '2수01-06'], [5, 23, 32, 36, 38, 41, 42, 44, 45, 47, 64, 75],
     '이어 세기는 이미 확정한 시작 수를 반복해 더하지 않는다. 가린 물건을 다시 놓는 시행은 초기 수를 확인한다. 빈 수직선의 호 표시는 이동값을 설명하며 종이에서 보이는 길이와 구별한다.',
     '출발 위치를 이동 1회로 세거나, 같은 모임에 물건을 다시 넣고 이전 결과를 유지하거나, 호 길이만 보고 덧셈량을 정하지 않는다.'),
    ('LT49', ['2수01-02', '2수01-10', '2수01-11'], [8, 9, 10, 70, 71, 72, 73, 74],
     '뛰어 세기에서 같은 묶음의 크기와 묶음 수를 함께 말한다. 크기가 다른 묶음이 섞이면 각각의 개수를 합한다.',
     '묶음 수만 같거나 낱개가 하나 빠진 경우에 같은 크기의 묶음이라는 가정을 유지할 수 없다. 설명이 같은 두 활동 주소를 독립 연구로 세지 않는다.'),
]

OBSERVATIONS = [
    dict(id='LT-P43', standard_codes=['2수01-01', '2수01-03'],
         question='접시에 단추 4개를 놓고, 한 번에 하나씩 빼서 빈 접시까지 남은 수를 적는다. 한 학생은 4, 3, 2, 1만 적고 다 기록했다고 한다. 빼기 전부터 빈 접시까지 기록한 수를 쓰고, 수를 적는 횟수와 단추를 빼는 횟수가 같은지 설명하라.',
         expected='빼기 전 4를 적고, 뺄 때마다 3, 2, 1, 0을 적는다. 기록은 5번이고 빼는 동작은 4번이다. 1에서 멈추면 단추가 한 개 남아 있는 상태이고, 빈 접시의 개수는 0이다.',
         interpretation='기록된 상태와 상태 사이의 변화, 말한 0과 응답하지 않은 경우를 구별한다. 단추를 움직이기 전 예상과 움직여 확인한 뒤 수정도 따로 기록한다.', student_validated=False),
    dict(id='LT-P44', standard_codes=['2수01-02', '2수01-03'],
         question='숫자 카드 2와 9를 한 번씩 사용해 만들 수 있는 두 자리 수를 모두 적는다. 각 수보다 큰 10의 배수 중 가장 작은 수까지 한 칸씩 가면 몇 칸인가? 0과 7로 같은 일을 하면 07과 70을 모두 두 자리 수로 써도 되는가?',
         expected='29 다음에는 30이므로 한 칸이다. 92에서 100까지는 여덟 칸이다. 07은 수 7을 나타내므로 두 자리 자연수가 아니고 70만 해당한다. 70보다 큰 가장 작은 10의 배수는 80이어서 열 칸이다.',
         interpretation='십의 자리와 일의 자리, 출발 수를 포함해 읽은 수의 개수와 이동 칸 수를 구별한다. 시작값도 10의 배수일 때 문제에서 요구한 조건을 다시 읽게 한다.', student_validated=False),
    dict(id='LT-P45', standard_codes=['2수01-06'],
         question='눈금이 없는 선에 47을 표시했다. 한 풀이에서는 20을 더한 뒤 5를 더하고, 다른 풀이에서는 5를 더한 뒤 20을 더한다. 중간 수와 도착 수를 각각 써라. 그림에서 5를 뜻하는 호가 20을 뜻하는 호보다 길게 그려졌다면 계산도 틀렸는가?',
         expected='47에서 20을 더하면 67, 여기에 5를 더하면 72다. 47에서 5를 더하면 52, 여기에 20을 더해도 72다. 빈 수직선에서 호의 표기와 도착 수를 확인한다. 눈금 간격을 정해 그리는 수직선이라면 같은 수만큼의 간격도 같아야 한다.',
         interpretation='두 자리 수 덧셈의 수량과 그림 축척을 구별한다. 20과 5의 순서를 바꾸었을 때 중간 수는 달라지고 도착 수는 같다는 설명을 확인한다.', student_validated=False),
    dict(id='LT-P46', standard_codes=['2수01-10', '2수01-11'],
         question='봉지 네 개에 단추를 다섯 개씩 넣었다. 마지막 봉지에서 단추 한 개만 빼서 다른 상자에 옮겼다. 한 학생은 봉지가 여전히 네 개라서 5씩 네 번 세면 된다고 말한다. 봉지 안에 남은 단추는 몇 개인가? 따로 옮긴 단추까지 모두 포함하면 몇 개인가?',
         expected='봉지에는 5개씩 든 세 봉지와 4개 든 한 봉지가 있다. 봉지 안에는 5+5+5+4로 19개이고, 따로 옮긴 1개까지 포함하면 20개다. 처음에는 묶음 크기가 모두 5였으나 옮긴 뒤에는 같지 않다.',
         interpretation='봉지 수, 한 봉지의 수, 어느 곳까지 포함한 전체를 구별한다. 같은 묶음에만 곱셈을 적용하거나 처음 20에서 1을 빼는 설명을 각각 인정한다.', student_validated=False),
]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        assert {row[0] for row in CLAIMS} <= {c['id'] for c in registry['claims']}
        assert [o['id'] for o in source['observations'][-4:]] == [o['id'] for o in OBSERVATIONS]
        build_report()
        return
    assert source['snapshot_file'] == PRIOR and sha(ROOT / PRIOR) == PRIOR_SHA
    prior = read(ROOT / PRIOR)
    pages = read(CACHE / 'activity-manifest.json')
    bodies = read(CACHE / 'english-bodies.json')
    expected = [r for r in prior['activity_followup_catalog']['records']
                if not r['body_read'] and any('/math/counting/' in u for u in r['linked_level_urls'])]
    assert expected == read(CACHE / 'selection.json')
    reading = [line.split('|', 1) for line in READING.strip().splitlines()]
    assert len(expected) == len(pages) == len(bodies) == len(reading) == 89
    assert [p['url'] for p in pages] == [r['url'] for r in expected] == [b['url'] for b in bodies]
    assert [p['url'].rsplit('/', 1)[-1] for p in pages] == [row[0] for row in reading]

    old_images = {a['url'] for a in prior['image_read_manifest']}
    old_pdfs = {a['url'] for a in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for index, (page, body, (_, note)) in enumerate(zip(pages, bodies, reading)):
        url = page['url']
        assert page['status'] == 200 and url == page['final_url'] and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256'] and '\nActivity\n' in body['body']
        kind = 'activity_procedure'
        group = 'activities'
        if index == 46:
            assert 'Type:\nTeacher Resources' in body['body']
            kind, group = 'teacher_resource', 'teacher_resources'
        elif index == 79:
            kind = 'reading_suggestion'
        groups[group].append(page['key'])
        logs.append(dict(url=url, page_kind=kind, note=note))
        linked_images = {urljoin(url, a['src']) for a in page['images'] if '/upload/' in a.get('src', '')}
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link}
        if linked_images - old_images:
            images[url] = sorted(linked_images - old_images)
        if linked_pdfs - old_pdfs:
            pdfs[url] = sorted(linked_pdfs - old_pdfs)

    image_count = len({u for links in images.values() for u in links})
    pdf_count = len({u for links in pdfs.values() for u in links})
    assert image_count == 146
    assert {key: len(value) for key, value in groups.items()} == dict(general=6, domain_overviews=20, levels=224, activities=241, teacher_resources=3)
    fields = ('key', 'url', 'title', 'sha256', 'status')
    manifest = prior['html_read_manifest'] + [{key: a[key] for key in fields} for a in pages]
    read_urls = {a['url'] for a in manifest}
    assert len(manifest) == len(read_urls) == 494
    followup = copy.deepcopy(prior['activity_followup_catalog'])
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(a['body_read'] for a in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'], followup['listed_body_pending']) == (244, 580)

    limits = (
        f'새 세기 페이지에서 연결된 삽입 이미지 {image_count}개 URL과 PDF {pdf_count}개 URL은 별도로 확인해야 한다. '
        '이전에 확인한 삽입 이미지 203개 URL과 PDF 24개 URL·29쪽의 범위는 유지한다. '
        '남은 공개 영어 본문, 영상·교재·개별 원연구·번역·독립 검토·학생 반응은 후속 범위다.'
    )
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = read(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=limits)
    notes = dict(prior)
    notes.update(
        date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
        html_read_manifest=manifest, observed_html_assets=manifest, read_groups=groups,
        new_read_groups=dict(domain_overviews=0, levels=0, activities=88, teacher_resources=1, inline_images=0, supplementary_pdf_urls=0),
        activity_followup_catalog=followup,
        catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies': 244, 'pending_activity_bodies': 580},
        counting_page_reading_log=logs, completed_counting_activity_records=expected,
        counting_linked_pdf_urls_not_reviewed=pdfs, counting_inline_image_urls_not_reviewed=images,
        counting_procedure_scope=dict(activity_procedures=87, reading_suggestions=1, teacher_resources=1),
        reading_log=prior['reading_log'] + ['세기와 연결된 영어 목표·절차·관련 교사 안내 89개를 본문별로 대조했다.'],
        source_corrections=prior['source_corrections'] + [
            dict(kind='counting_examples_and_boundaries', locations=[pages[i]['url'] for i in (7, 11, 25, 40, 44, 47, 51, 58, 73)],
                 action='0과 1의 끝점, 숫자 카드와 점 개수, 두 자리 수의 시작 조건, 가리기 전후, 다시 넣을 때의 초기 상태, 빈 수직선의 축척, 위치와 수, 같은 묶음의 크기를 각각 확인했다.'),
        ],
        unread_followups=[limits, '북부준주 안내서의 공개 추출 본문은 별도 출처 NT_PRESCHOOL_MATHS_GAMES에 연결했다.'],
    )
    notes_path = ROOT / NOTES
    write(notes_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                                date=source['date'], read_scope=source['read_scope'])]
    source.update(
        date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(notes_path), snapshot_history=history,
        bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE,
        method_note='영어 목표와 실제 활동 절차를 비교하고 교사자료와 그림책 제안을 구별했다. 링크만 확인한 첨부와 삽입 이미지는 대기 목록에 보존했다.',
        limits=limits, editorial_action='세기 자료의 문헌 대응 5건과 자체 관찰 과제 4개를 추가했다.',
        observations=source['observations'] + OBSERVATIONS,
    )
    for cid, codes, indices, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
            locations=[pages[i]['url'] for i in indices], support=support, does_not_establish=limit,
            target_snapshots={'revision:' + code: digest(target_value('revision:' + code)) for code in codes},
            independent_review=False, student_validated=False,
        ))
    assert 100 - 92 == 8 and 30 - 29 == 1 and 80 - 70 == 10
    assert 47 + 20 + 5 == 47 + 5 + 20 == 72 and 3 * 5 + 4 == 19
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = read(queue_path)
    row = next(r for r in queue['literature_review'] if r['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[c['id'] for c in registry['claims'] if c['source_id'] == SOURCE])
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print(f'Reviewed 89 pages. New unread attachments: {pdf_count} PDF URLs and {image_count} image URLs.')


if __name__ == '__main__':
    main()

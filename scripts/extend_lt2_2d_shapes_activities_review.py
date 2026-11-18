"""Record the reviewed English LT2 plane-geometry activity pages."""
import copy
from urllib.parse import urljoin, urlparse

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_patterns_assets_review_notes.json'
PRIOR_SHA = '1ca4cb48dfe37bd81a67bccb78f6d5ba5767fcae37a311a44fef90b68c9e83b0'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_2d_shapes_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-2d-shapes-activities'
SCOPE = '평면도형에 연결된 공개 영어 페이지 65개를 대조했다. 활동 절차 64개와 일상 공간 말 자료 1개다. 활동·교사자료 목록 824개 중 627개를 확인했고 197개가 남았다.'
LIMITS = '새 연결 PDF 30개, 삽입 이미지 92개 URL, 영상·책과 인용 원연구는 별도다. 가정 말 자료에 연결된 별도 안내서와 학생 반응은 이 범위에 포함되지 않는다.'

READING = """
angle-hunt|책상과 별의 꼭짓점, 문의 벌어진 각을 직각과 비교한다. 도형 이름만으로 그 도형의 모든 각의 종류를 정하지 않는다.
as-the-world-turns-angle-representer|문·가위·경사로·이동에서 기준과 회전량을 정한다. 두 선분의 끝점 거리나 경사도의 비를 각도와 혼동하지 않는다.
attribute-match-most-attributes-comparer|세 물체 중 둘을 짝지어 색·크기·모양·촉감 중 어떤 속성이 같은지 설명한다.
build-shapes-constructor-of-shapes-from-partslooks-like|빨대 끝점을 이은 닫힌 도형을 만든다. 정사각형의 네 같은 변과 네 직각을 모두 확인한다. 벌어진 빨대 끝과 벌어진 각을 구별한다.
circle-time-shape-recognizertypical|고리의 가장자리를 따라 닫힌 곡선을 찾는다. 실물 고리·시계의 윤곽과 수학적 원을 구별한다.
circles-and-cans|깡통의 밑면을 종이에 본떠 포갠다. 입체 물체, 평평한 원 모양 밑면, 그 둘레의 원을 구별한다.
dont-burn-your-feet--shape-class-identifier|길쭉한 육각형도 여섯 변이면 육각형이다. 사각형과 마름모가 아닌 도형 등 서로 다른 규칙을 바꾸어 적용한다.
dont-burn-your-feet-constructor-of-shapes-from-partslooks-like|수준명은 구성 단계이지만 본문 절차는 바닥 도형 중 정해 준 종류를 골라 밟는다. 도형을 직접 만든 것으로 세지 않는다.
dont-burn-your-feet-shape-property-identifier|직각이 하나 이상이거나 평행한 변이 두 쌍이라는 조건을 지정한다. 도형 이름을 맞히는 일과 속성을 확인하는 일을 구별한다.
dont-burn-your-feet-shape-recognizer--more-shapes|사다리꼴·육각형·마름모를 여러 방향과 비율로 배치해 범주를 확인한다. 한 모양으로만 이름을 연상하지 않는다.
explore-shapes-and-angles|변을 따라 세고 꼭짓점은 점으로 짚는다. 꼭짓점은 두 변이 만나는 점이고 각은 그 점에서 두 방향이 벌어진 것이다.
exploring-circles-four-ways|동심원은 중심이 같다. 중심이 다른 두 원도 서로 포함될 수 있다. 지름은 중심을 지나고, 외접 정사각형의 대각선 교점이 중심이다.
exploring-shapes-sides|변의 시작과 진행 방향을 정해 한 번씩 센다. 여섯 직선 변의 닫힌 다각형을 육각형이라 한다.
feely-bag-side-recognizer|보이는 짝과 숨긴 짝을 변 수로 추측하고 꺼내 검증한다. 보기 중 고르는 것과 변 수 하나로 모든 도형을 판별하는 것을 구별한다.
feely-box--shape-recognizer-circles-squares-and-triangles|촉각으로 원·정사각형·삼각형을 말하고 꺼내 확인한다. 보기와 짝짓기 지원과 이름 말하기를 분리한다.
feely-box-congruence-superposer|동일한 크기와 모양의 짝을 촉각으로 예측한 뒤 꼭짓점·변·각의 대응을 포개어 검증한다.
feely-box-corner-angle-recognizer|숨긴 도형의 꼭짓점 수를 손으로 센다. 각의 개수와 각 크기, 꼭짓점의 개수를 별도로 말한다.
feely-box-most-attributes-comparer|변은 선분을 따라, 꼭짓점은 점을 찍어 센다. 짝이 듣고 도형을 추측한 뒤 꺼내 확인한다.
feely-box-parts-of-shapes-identifier|여러 변 수의 보기에서 숨긴 도형을 설명한다. 같은 변 수의 보기가 둘 이상이면 추가 속성을 묻는다.
feely-box-shape-identifier|변 수·변 길이·각을 촉각으로 설명하고 공개한 뒤 확인한다. 보기와 색을 바꾸어도 속성은 유지된다.
feely-box-shape-matcher--identical-orientation-sizes|상자 밖 보기와 상자 안 도형을 손으로 짝짓는다. 이름을 말하지 않아도 일치 여부를 확인할 수 있다.
feely-box-shape-property-identifier|이름을 말하기 전에 변 수·직각·변 길이를 알려 준다. 맞힌 이름보다 사용한 판별 근거를 함께 기록한다.
fill-spill-same-thing-comparer-foundations|물체를 담고 쏟으며 모양을 알아차린다. 들어간다는 사실만으로 두 도형의 합동을 판단하지 않는다.
find-my-pair-stemie-congruence-representer|단위 블록으로 대응변을 재고 도형을 포갠다. 같은 수의 변과 같은 대응변 길이만으로 일반 사각형의 합동이 결정되지 않는다.
find-the-twin-circles-triangles-squares|색을 달리한 같은 모양과 같은 크기의 짝을 포개며 이름과 완전 일치를 구별한다.
find-the-twin-shape-matcheridentical-orientations-sizes|같은 방향으로 놓은 두 색 도형을 포갠다. 종류가 같기만 한 보기와 크기도 같은 보기를 나눈다.
find-the-twin-shape-recognizer-more-shapes|마름모·사다리꼴·오각형·육각형의 정확한 짝을 찾는다. 도형을 회전해 대응 부분을 확인한다.
find-the-twin-shape-recognizer-typical|대표 도형의 두 색 짝을 확인한다. 교사가 포개기를 보여 준 경우와 학습자가 먼저 확인한 경우를 구별한다.
guess-my-rule-shape-class-identifier|예시 더미를 보고 범주 규칙을 예상한 뒤 새 도형에 적용한다. 초기 보기가 같은 두 규칙은 구별할 새 보기가 필요하다.
guess-my-rule-shape-property-identifier|직사각형 예에 정사각형을 포함한다. 모든 변 길이가 같다와 직각이 하나 이상이다는 서로 다른 조건이다.
i-spy-shape-property-identifier|칠판 등 물체의 면에서 마주 보는 평행한 변 두 쌍을 짚는다. 해당 속성을 가진 후보는 둘 이상일 수 있다.
i-spy-shape-recognizer-all-rectangles|세로·가로로 놓이지 않은 직사각형을 포함한다. 네 직각이 방향에 따라 바뀌지 않는다.
is-it-or-not-circles|타원 등 닫힌 곡선을 원과 비교한다. 닫혀 있다는 조건만으로 원이 되지 않는다.
is-it-or-not-shape-recognizer-more-shapes|도입의 직사각형과 실제 마름모 판별을 구별한다. 네 변이 모두 같지 않은 평행사변형을 마름모의 반례로 둔다.
is-it-or-not-side-recognizer|직선 변 네 개로 닫힌 도형을 고른다. 굽은 부분과 직선 변, 맞닿지 않은 끝을 구별한다.
is-it-or-not-squares|크기·방향·색을 바꾼 정사각형과 길쭉한 직사각형·비직각 마름모를 네 변과 각으로 가른다.
is-it-or-not-triangles|목표 문구는 정사각형을 말하지만 절차는 삼각형을 판별한다. 직선 변 세 개가 닫히는 조건을 적용한다.
is-it-or-not-typical|수평 밑변의 정삼각형은 대표 예다. 방향·변 길이가 다른 삼각형도 같은 범주에 들어간다.
make-me-double|공통 꼭짓점과 한 반직선을 맞추고 내부가 겹치지 않게 이으면 30°와 30°의 합은 60°다. 다른 두 각 20°와 40°도 같다.
match-and-name-shapes|두 색 도형의 정확한 짝을 먼저 찾고 이름은 별도로 말한다. 포개기와 촉각 설명을 함께 활용한다.
mr-mix-up--angles-and-shapes-angle-recognizer--more-contexts|정사각형은 네 직각이 있는 마름모다. 네 직각이 없는 마름모와 비교하는 사례를 서로 배타적인 두 범주로 만들지 않는다.
mr-mixup-2d-shapes-property-class-identifier|직사각형은 두 쌍의 평행한 변이 있는 평행사변형이다. 직각 네 개는 더 좁은 범주인 직사각형의 조건이다.
mr-mixup-shape-identifier|사다리꼴을 평행한 변이 정확히 한 쌍인 경우로 쓰는 예다. 다른 정의에서의 포함관계를 이 활동의 정의에 그대로 옮기지 않는다.
name-that-shape|마름모의 네 같은 변, 육각형의 여섯 변, 팔각형의 여덟 변을 짚는다. 정팔각형 표지와 일반 팔각형을 구별한다.
name-the-faces|입체의 평평한 면과 그 면의 변·꼭짓점을 나눠 센다. 직각 삼각기둥의 옆면은 직사각형이지만 일반 비스듬한 각기둥의 옆면에는 같은 설명을 적용하지 않는다.
pentomino-symmetry-games|축 반대쪽에 조각의 반사상을 배치한다. 같은 조각이라도 축까지의 거리와 방향이 맞아야 전체가 선대칭이다.
quadrilateral-family-geometry--hierarchical-geometry|네 직각 여부와 평행·변 길이 조건으로 분류한다. 정사각형은 직사각형이면서 마름모이며 사각형 범주에 포함된다.
quick-shapes-and-straws|잠깐 본 모형을 빨대로 재현한 뒤 다시 확인한다. 닮아 보이는 근사와 길이·각이 일치하는 경우를 구별한다.
rectangles-boxes|직육면체 상자의 여섯 면을 따로 본떠 어느 상자인지 맞춘다. 서로 떨어진 여섯 면의 그림을 전개도로 보지 않는다.
shape-books-same-thing-comparer-foundations|기울인 정사각형은 여전히 정사각형이다. 악기의 이름과 닫힌 직선 세 변의 수학적 조건을 구별한다.
shape-hunt-rectangles|찾는 것은 물체의 직사각형 면이다. 원문의 삼각형 안내는 목표와 다르다. 두 긴 변·두 짧은 변은 직사각형의 정의가 아니다.
shape-hunt-triangles--shape-recognizer-circles-squares-and-triangles|물체 전체와 삼각형 면을 구별한다. 모든 삼각형의 변 길이가 같을 필요는 없다.
shape-pegs|구멍에 끼운 것과 다른 도형 위에 포개 정확히 일치한 것을 구별하고 이름을 붙인다.
shape-show-shape-recognizer--all-rectangles|둘레를 따라 네 변과 네 직각을 확인한다. 정사각형도 포함하고 발문의 세 차례 회전과 실제 네 꼭짓점을 구별한다.
shape-show-squares|네 같은 변과 네 직각을 함께 확인한다. 한 막대로 변 길이를 확인하고 직각 모형은 별도로 댄다.
shape-show-triangles|직선 변 세 개가 끝점에서 이어져 닫힌 모양을 만든다. 세 변의 길이나 각의 크기가 같을 필요는 없다.
shape-sort|설명에 맞는 모든 후보를 골라 이유를 말한다. 남은 비예가 조건을 충족하지 않는 이유도 확인한다.
shape-stacker-congruence-superposer|같은 크기·모양의 평면도형을 포개어 확인한다. 색이 다르거나 놓인 자리가 다른 것은 합동의 조건이 아니다.
shapes-all-around-stemie-same-thing-comparer-foundations|책등·담요·과자의 면과 회전 놀이의 이동 경로를 예로 들어 물체와 평면 모양을 구별한다.
spatial-talk-same-thing-comparer-foundations|일상에서 안·밖, 위·아래, 좌·우·가운데를 쓰는 어휘 목록이다. 별도 가정 자료의 전체 내용은 여기서 확인하지 않는다.
straw-angles|빨대 길이가 달라도 벌어진 회전량이 같으면 같은 각이다. 두 각을 나란히 잇고 직각과 비교한다.
tracing-challenge|물체의 한 면을 본떠 맞춘다. 한 면의 모양이 같아도 두 입체 전체가 같다고 결론 내리지 않는다.
triangle-family-geometry-hierarchical-geometry|변 길이와 각으로 하는 분류를 교차해 본다. 작은 각 하나로 예각삼각형이 되지 않는다. 세 각이 모두 90° 미만이어야 한다.
what-shape-do-you-see-shape-recognizertypical|상자와 공의 굴리기·쌓기, 거품 만들기를 비교한다. 도구 윤곽과 떨어진 거품의 입체 모양을 구별한다.
which-shape-could-it-be|가려진 도형의 일부에서 가능한 후보를 고른다. 한 직각만으로 직사각형을 확정할 수 없어 더 보인 변과 꼭짓점을 확인한다.
"""

CLAIMS = [
    ('LT120', ['2수03-03','2수03-04','2수03-05','4수03-11'], [6,12,13,28,34,36,37,55,56,64],
     '삼각형은 직선 변 세 개로 닫힌 다각형이다. 변을 한 번씩 세고 방향·크기·색이 다른 예와 열린 모양을 비교한다.',
     '변 개수로 다각형의 큰 범주는 가를 수 있으나 변 길이와 각에 따른 세부 종류나 합동까지 결정하지 못한다.'),
    ('LT121', ['2수03-01','2수03-03','6수03-03','6수03-05','6수03-07'], [5,44,48,51,61,63],
     '물체 전체, 본뜬 평면의 모양, 면을 둘러싼 선을 구별한다. 원기둥의 원 모양 밑면과 직육면체의 직사각형 면을 본뜰 수 있다.',
     '같은 한 면은 같은 입체의 충분조건이 아니다. 옆면이 직사각형이라는 설명은 직각인 각기둥 모형에서 확인한다.'),
    ('LT122', ['4수03-01','4수03-02','4수03-24'], [0,1,3,10,16,38,60],
     '꼭짓점은 두 반직선의 공통 시작점이다. 각의 크기는 빨대 길이가 아니라 두 방향의 벌어짐으로 비교한다.',
     '두 각의 합은 공통 꼭짓점과 반직선을 맞추고 각의 내부가 겹치지 않게 나란히 이을 때 바깥 두 변 사이에서 읽는다.'),
    ('LT123', ['2수03-04','4수03-06','4수03-07'], [4,11,32],
     '원 위 점은 중심에서 거리가 같다. 동심원은 중심을 공유하며 외접 정사각형의 대각선 교점은 원의 중심이다.',
     '한 원이 다른 원 안에 있는 것만으로 동심원을 판단할 수 없다. 바깥 정사각형이 네 변에서 원에 접하는지 확인한다.'),
    ('LT124', ['4수03-03','4수03-10'], [8,29,30,31,33,35,40,41,42,46,50,53,54],
     '정사각형은 네 직각과 네 같은 변을 갖춰 직사각형이면서 마름모다. 직사각형과 마름모는 모두 평행사변형의 조건을 만족한다.',
     '대표 모형의 서로 다른 특징과 범주의 포함을 구별한다. 사다리꼴의 평행한 변을 정확히 한 쌍으로 세는 활동에서는 그 정의를 밝힌다.'),
    ('LT125', ['4수03-08','4수03-09','4수03-25'], [0,51,55,62],
     '변 길이 기준과 각 기준은 동시에 적용할 수 있다. 예각삼각형은 세 각이 모두 90°보다 작고, 직각이등변삼각형은 두 변이 같으며 한 각이 90°다.',
     '작은 각 하나는 예각삼각형을 가르는 조건이 아니다. 삼각형에서 두 각이 직각이면 남은 각이 0°이므로 닫힌 삼각형이 되지 않는다.'),
    ('LT126', ['4수03-04','6수03-01'], [15,20,23,24,25,26,27,39,52,57],
     '밀기·돌리기·뒤집기로 꼭짓점과 변, 각이 맞게 포개지는지 확인한다. 대응변이 같은 정사각형과 비직각 마름모는 각이 달라 합동이 아니다.',
     '같은 종류, 같은 방향, 대응변 길이의 일치만으로 일반 다각형의 합동이 결정되지는 않는다.'),
    ('LT127', ['4수03-04','4수03-12','6수03-02'], [45],
     '펜토미노를 축의 반대쪽에 거울처럼 놓는다. 대응점은 축에서 같은 수직 거리에 있고 방향도 반사에 맞아야 한다.',
     '같은 모양을 반대편으로 평행이동하는 것만으로 선대칭이 되는지는 조각 모양과 위치에 따라 달라진다.'),
]

OBSERVATION_DATA = [
    ('LT-P111', '기울어진 삼각형과 직선 세 개로 거의 닫힌 열린 모양을 비교한다. 어느 것이 삼각형인가? 변을 따라 근거를 말하라.',
     '기울어진 도형에서 세 선분이 끝점끼리 이어져 닫혔다. 열린 모양은 끝점 사이에 틈이 있다.', '방향과 닫힘을 독립적으로 확인한다.'),
    ('LT-P112', '가로·세로가 3과 2인 밑면을 가진 높이 4 상자와 높이 7 상자가 있다. 같은 종이 밑면 그림에 둘 다 맞는가? 상자 전체가 같은가?',
     '둘 다 밑면이 3×2라 같은 그림에 맞는다. 높이가 달라 입체 전체는 다르다.', '한 면의 일치를 입체의 일치로 확대하는지 확인한다.'),
    ('LT-P113', '같은 30°로 벌어진 두 각에서 한 쪽 빨대만 더 길다. 어느 각이 더 큰가? 두 30° 각을 한 변에서 맞대되 내부가 겹치지 않게 이으면 몇 도인가?',
     '두 각의 크기는 같다. 공통 반직선을 경계로 나란히 이으면 60°다.', '끝점 거리와 회전량, 맞댄 각과 겹친 각을 구별한다.'),
    ('LT-P114', '반지름 5인 원 안에 반지름 1인 원이 있고 중심 사이 거리는 2다. 두 원은 동심원인가? 작은 원을 어떻게 옮기면 동심원이 되는가?',
     '2+1이 5보다 작아 작은 원은 안에 있지만 중심이 다르다. 두 중심이 일치하도록 옮기면 동심원이다.', '포함 관계와 중심의 일치를 구별한다.'),
    ('LT-P115', '네 변이 같은 두 사각형이 있다. 하나는 네 각이 90°이고, 다른 하나는 60°와 120°가 번갈아 나온다. 각각 어느 사각형 범주에 속하는가?',
     '둘 다 마름모이고 평행사변형이다. 네 직각이 있는 것은 정사각형이면서 직사각형이다.', '같은 변 길이와 직각 조건을 각각 적용한다.'),
    ('LT-P116', '세 각이 45°·45°·90°인 삼각형과 30°·30°·120°인 삼각형을 변 길이와 각으로 분류하라. 작은 각이 하나라도 있으면 예각삼각형인가?',
     '둘 다 같은 크기의 각에 마주 보는 변이 같아 이등변삼각형이다. 첫째는 직각, 둘째는 둔각이다. 예각삼각형의 세 각은 모두 90° 미만이다.', '두 분류 기준과 예각 하나·전체 조건을 구별한다.'),
    ('LT-P117', '한 변이 3인 정사각형과 네 변이 모두 3인 비직각 마름모를 비교한다. 합동인가? 포개었을 때 맞지 않는 부분을 말하라.',
     '네 변 길이는 같지만 대응각이 맞지 않는다. 한 변을 맞추어도 나머지 변과 꼭짓점이 모두 포개지지 않는다.', '필요조건 하나와 실제 겹침을 구별한다.'),
    ('LT-P118', '세로 축 왼쪽에 놓인 방향이 있는 펜토미노의 대응 조각을 오른쪽에 두려 한다. 왼쪽의 모든 칸을 오른쪽으로 같은 거리만큼 밀면 언제나 맞는가?',
     '각 칸을 축에 수직인 방향으로 반사해 축까지 같은 거리에 둔다. 조각에 따라 방향도 바뀌므로 평행이동만으로 항상 맞지는 않는다.', '같은 조각, 대칭축까지 거리, 반사 방향을 구별한다.'),
]

OBSERVATIONS = [dict(id=oid, standard_codes=claim[1], question=question, expected=expected,
                     interpretation=interpretation, student_validated=False)
                for claim, (oid, question, expected, interpretation) in zip(CLAIMS, OBSERVATION_DATA, strict=True)]


def verify_examples(bodies):
    text = [r['body'] for r in bodies]
    assert 'circles completely contained within one another' in text[11]
    assert 'square outside the circle' in text[11]
    assert 'corresponding sides much be the same length' in text[23]
    assert 'is or is not a square' in text[36].split('\nActivity\n')[0] and 'Is it a triangle?' in text[36]
    assert 'parallelograms whose sides are not all equal' in text[33]
    assert 'all squares are actually a special kind of rhombus' in text[40]
    assert 'trapezoid only has 1 pair' in text[42] and 'one small angle' in text[62]
    assert 'mirror image' in text[45] and 30 + 30 == 20 + 40 == 60
    assert 45 + 45 + 90 == 30 + 30 + 120 == 180 and 2 + 1 < 5
    return dict(nested_circle_witness=dict(outer_radius=5, inner_radius=1, center_distance=2),
                congruence_counterexample=dict(all_sides=3, square_angles=[90] * 4, other_angles=[60,120] * 2),
                obtuse_isosceles_angles=[30,30,120], right_isosceles_angles=[45,45,90],
                adjacent_angles=[30,30,60])


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
                        and any('/math/2d-shapes/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|', 1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 65
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/', 1)[-1] for row in pages] == [row[0] for row in reading]
    examples = verify_examples(bodies)

    old_images = {row['url'] for row in prior['image_read_manifest']}
    old_pdfs = {row['url'] for row in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for page, body, (_, note) in zip(pages, bodies, reading):
        url = page['url']
        assert page['status'] == 200 and page['final_url'] == url and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256']
        landing = url.rsplit('/', 1)[-1] in {'spatial-talk-same-thing-comparer-foundations'}
        assert '\nActivity\n' in body['body']
        assert 'Type:\nTeacher Resources' not in body['body']
        groups['activities'].append(page['key'])
        logs.append(dict(url=url, page_kind='spatial_language_prompt' if landing else 'activity_procedure', note=note))
        linked_images = {urljoin(url, image['src']) for image in page['images'] if '/upload/' in image.get('src', '')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert sum(row['page_kind'] == 'spatial_language_prompt' for row in logs) == 1
    assert len({url for links in images.values() for url in links}) == 92
    assert len({url for links in pdfs.values() for url in links}) == 30
    assert {k: len(v) for k, v in groups.items()} == dict(general=6, domain_overviews=20, levels=224, activities=611, teacher_resources=16)
    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key', 'url', 'title', 'sha256', 'status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 877
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'], followup['listed_body_pending']) == (627, 197)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
                 observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
                 catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies': 627, 'pending_activity_bodies': 197},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=65, teacher_resources=0, inline_images=0, supplementary_pdf_urls=0),
                 geometry_2d_reading_log=logs, completed_geometry_2d_records=selected,
                 geometry_2d_pdf_urls_not_reviewed=pdfs, geometry_2d_image_urls_not_reviewed=images,
                 geometry_2d_procedure_scope=dict(activity_procedures=64, spatial_language_prompts=1),
                 geometry_2d_checked_examples=examples,
                 geometry_2d_cited_works_pending=[
                     dict(linking_pages=[pages[11]['url']], url='https://doi.org/10.1080/10986065.2022.2119497',
                          read_scope='출판사 웹 본문과 Durham 저장소의 출판본 경로를 확인했다. 판본별 본문 대조는 별도다.'),
                     dict(linking_pages=[pages[i]['url'] for i in (46,62)], citation='Zaranis, 2018',
                          read_scope='활동 페이지에는 저자·연도만 있어 어느 자료를 개작했는지 확인이 필요하다.'),
                 ],
                 reading_log=prior['reading_log'] + ['평면도형의 영어 활동 절차 64개와 일상 공간 말 자료 1개를 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='geometry_defining_properties_and_task_scope', locations=[pages[i]['url'] for i in (7,10,11,23,33,36,40,42,44,50,62)],
                     action='목표와 절차, 도형의 정의와 반례, 원의 중심, 합동 조건을 구별했다.')],
                 unread_followups=[LIMITS, '평면도형의 첨부와 연결 원연구를 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
                  method_note='평면도형의 정의, 분류 조건, 합동과 선대칭을 영어 본문과 대조했다.',
                  editorial_action='문헌 대응 8건과 자체 관찰 과제 8개를 추가했다.', observations=source['observations'] + OBSERVATIONS)
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
    print('Reviewed 65 English pages; added 8 mappings and 8 observations. Public activity bodies pending: 197.')


if __name__ == '__main__':
    main()

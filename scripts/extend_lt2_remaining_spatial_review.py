"""Register LT2 spatial visualization and disembedding activities, templates, and checked examples."""
import copy
from itertools import product
from urllib.parse import urljoin, urlparse

from extend_lt2_composing_2d_assets_review import pdf_name, verified_assets
from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_classification_data_review_notes.json'
PRIOR_SHA = '428babbb654d01dea037b4d70a8d8f8a08a7d4ec2bd090e999805299b49f89e4'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_remaining_spatial_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-remaining-spatial-activities'
ASSETS = ROOT / 'tmp/literature/lt2-remaining-spatial-assets'
SCOPE = ('공개 영어 HTML 1074개와 기록된 활동·교사자료 목록 824개 전부를 대조했다. '
         '공간 시각화와 도형 찾아내기의 남은 영어 페이지 29개, LT2 PDF 21개 URL·97쪽과 이미지 29개 URL을 확인했다.')
LIMITS = ('별도 가정 자료와 조작 카드, 펜토미노 V~VIII의 일치하는 원본, 영상, 인용 연구 및 학생 수행은 후속 범위다. '
          '활동 소개와 절차가 없는 페이지를 완전한 활동 절차로 세지 않는다.')

READING = """
can-you-build-from-memory-mental-mover|연결 큐브 4~6개를 10초간 보고 가린 뒤 재현한다. 같은 개수, 서로 닿는 위치, 본 방향을 따로 확인한다.
color-and-disembed-complete-disembedder|원래 그려진 다섯 유형의 도형 수와, 여러 경계에서 새로 찾는 아홉 윤곽을 구별한다.
color-and-disembed-secondary-structure-disembedder|삼각형·원·사각형을 색칠한 뒤 숨은 윤곽 열두 개를 추적한다. 답지 색은 단서로 기록한다.
discover-the-shape|복합 그림에서 경계를 따라 찾는다. 목표에 열린 선과 닫힌 도형이 모두 나온다.
exploring-your-spatial-world-foundations|몸과 물체를 움직일 기회를 제시한다. 특정 발달 단계의 인과적 증거는 아니다.
fill-spill-intuitive-mover|구멍에 넣기 전에 방향을 바꾼 수행과 교사의 물리적 도움을 구별한다.
find-the-shape|복합 그림에서 목표 윤곽을 선분 단위로 확인한다. 물건 찾기 그림은 도형 과제의 도입이다.
find-the-shapes-all-around-intuitive-disembedder-stemie|상자 한 면과 여러 상자의 배열, 사다리에서 만들어진 사각형을 짚는다.
find-the-shapes-all-around-simple-disembedder|창 전체와 유리 칸을 따로 찾고, 책 한 권의 보이는 면과 입체 물체를 구별한다.
finding-embedded-pictures|그림책에서 부분을 먼저 가리킨다. 그림책의 물체 이름과 평면도형 이름을 구별한다.
finding-funny-figures|여러 도형의 일부 경계에서 열린 윤곽도 찾는다. 열린 윤곽을 오각형으로 이름 붙이지 않는다.
fixing-elevators|삼각형 두 개로 만든 정사각형을 밀어 나눈 뒤 복원한다. 변 방향이 바뀐 상황은 별도로 제시한다.
pattern-block-play-simple-slider-and-turner|패턴 블록 퍼즐 번호와 내부선 제공 여부를 실제 파일에서 확인한다. 10번에는 내부선이 있다.
pentomino-puzzle-perfection|본문은 펜토미노 V~VIII를 안내하지만 첨부는 탱그램 5~8이다. 해당 펜토미노 도안은 확인 전이다.
piecing-pentominoes-together|펜토미노 I 위 도안의 첨부 힌트는 P·L 또는 Z·T다. 본문의 P·U는 이 윤곽을 채우지 못한다.
put-the-halves-back-together-diagonal-mover|대각선 이동을 예상하도록 안내하지만 공유 도안 자체의 초기 배치도 확인한다.
put-the-halves-back-together-mental-mover|조각을 대기 전에 어떤 도형이 될지 말하고, 실제 맞추기로 확인한다.
put-the-halves-back-together-slider-flipper-turner|이동·회전·뒤집기를 설명한다. 연결 파일을 공유하는 활동에서는 지시와 시작 자세를 구별한다.
putting-the-pieces-together-simple-turner|직소에서 가장자리·색·방향 단서를 활용한다. 원연구의 가정 관찰과 수업 효과를 구별한다.
recreate-my-design|원본과 조각을 본떠 재현한다. 위치만 같은지, 조각의 방향과 접점도 같은지 확인한다.
researcher-note-tangram-puzzles-slider-flipper-turner|정사각형의 기준 자세와 45° 돌아간 자세를 비교하는 교사 설명이다. 인용 연구 본문의 확인은 별도다.
spatial-learning-at-home-concrete-slider-flipper-turner|가정 안내 소개와 미리보기를 확인했다. 별도 배포본은 확인 전이다.
spatial-learning-at-home-intuitive-mover-foundations|가정 자료 미리보기와 절차가 비어 있는 페이지를 확인했다. 활동 절차를 읽은 건으로 세지 않는다.
spatial-talk-concrete-slider-flipper-turner|일과 속 위치말을 짝지어 사용한다. 기준 물체와 보는 방향을 명시한다.
spatial-talk-intuitive-mover-foundations|일과에서 위·아래·안·밖을 말하고, 말이나 가리키기로 응답할 기회를 준다.
tangram-and-pattern-block-play-diagonal-mover|대각선 이동을 안내한다. 패턴 블록 14~18과 탱그램 9~12가 링크되며 도안마다 내부선이 다르다.
tangram-and-pattern-block-play-mental-mover|대기 전에 조각의 위치와 방향을 예상한다. 같은 도안의 조작 후 수정과 초기 예상은 따로 기록한다.
tangram-puzzle-play-slider-flipper-turner|첨부 탱그램 5~8의 내부선과 본문의 안내가 다르다. 블록과 탱그램 재료도 구별한다.
whats-the-smallest-shape-in-the-image-stemie|포함된 도형의 경계를 찾아 작은 부분을 설명한다. 부분 포함과 임의의 너비·넓이 비교를 구별한다.
"""

PDF_NOTES = {
    '1584053640755': [([1], '숨은 물건을 색으로 표시한 도입 예시다. 목표 도형을 찾는 평가 도안과 다르다.')],
    '1584564024223': [([1], '위 도안 10칸과 아래 도안 15칸. 위 힌트는 P·L 또는 Z·T, 아래는 U·W·F다.'),
                      ([2,3,4], 'II~IV 윤곽과 조각 힌트다. IV의 내부 사각형은 바깥 윤곽과 따로 확인한다.')],
    '1584564364786': [([1,2,3], '조각 네 개씩 총 12종의 펜토미노다. 각 조각은 변으로 연결한 정사각형 다섯 개로 구성된다.')],
    '1587584002728': [([1,2,3,4], '두 조각과 네 완성 후보를 제시하는 공유 도안이다. 활동 제목이 달라도 연결 파일은 같다.')],
    '1587585517254': [(list(range(1,9)), '다양한 시작 자세의 두 조각을 네 완성 후보와 비교한다. 실제 맞추기 전 예상 답을 따로 기록한다.')],
    '1587610801265': [([1,2], '겹친 직사각형·격자·삼각형·마름모 등에서 목표 윤곽을 찾는 5문항이다.')],
    '1587611148482': [([1,2], '열린 꺾은 선, 원, 십자 모양과 닫힌 윤곽 등이 섞인 6문항이다.')],
    '1587611421102': [([1,2], '열린 꺾은 선과 닫힌 윤곽을 복합 그림에서 찾는다. 목표가 표시한 선과 꼭짓점을 따른다.')],
    '1588095036171': [(list(range(1,6)), '다섯 완성 배열이다. 마지막 배열은 같은 색이라 위치와 경계의 단서가 중요하다.')],
    '1588095062699': [(list(range(1,6)), '완성 배열 다섯 개에 대응하는 분리 조각이다. 같은 조각 집합으로 배치를 비교한다.')],
    '1592585576150': [(list(range(1,6)), '패턴 블록 14~18이다. 16번의 아래 도안은 내부선이 있다.')],
    '1592585602024': [([1,2,3,4], '탱그램 9~12의 윤곽이다. 같은 번호의 다른 파일을 이 도안으로 간주하지 않는다.')],
    '1592586762854': [([1,2,3,4], '탱그램 5~8이며 내부선이 있다. 펜토미노 활동에 잘못 연결된 파일과 바이트가 같다.')],
    '1608314413157': [([1], '삼각형·원·직사각형의 개수를 기록하는 지시와 표다.'), ([2,3], '겹친 도형과 별도로 찾아야 하는 윤곽 12개가 제시된다.')],
    '1608314436234': [([1,2], '답안 표는 삼각형 6·원 8·직사각형 8이다. 색칠한 그림은 숨은 윤곽을 번호로 표시한다.')],
    '1608564855069': [([1], '원·삼각형·직사각형·오각형·육각형을 세는 지시와 표다.'), ([2,3], '겹친 도형의 도안과 별도로 찾을 아홉 윤곽이다.')],
    '1608564871437': [([1,2], '답안 표는 원 6·삼각형 5·직사각형 6·오각형 4·육각형 4다. 붉은 선은 숨은 윤곽을 표시한다.')],
    '1615943737952': [([1,2], '겹치거나 포함된 보기 7개와 선택형 시각 단서다. 도형 유형을 제시하는 단서는 크기 측정의 정의를 대신하지 않는다.')],
    '1642006860884': [([1,2,3,4], '펜토미노 V~VIII라는 링크가 열지만 실제 페이지 제목과 도형은 탱그램 5~8이다.')],
    '1712762945261': [([1], '패턴 블록과 탱그램의 변 길이, 각과 뒤집기를 비교한다. 사용 중인 실물의 치수와 별도로 확인한다.')],
    '1713196617742': [([1], '조각 배열 단계 표지다.'), (list(range(2,11)), '퍼즐 1~9의 조각선과 일부 사이 간격을 확인했다.'),
                      ([11], '그림 만들기와 밀기·돌리기 단계의 표지다.'),
                      (list(range(12,18)), '퍼즐 10~15다. 10번을 포함한 일부 보기에 내부선이 있다.'),
                      ([18], '도형 구성과 밀기·돌리기 단계의 표지다.'),
                      (list(range(19,28)), '퍼즐 16~24의 내부선, 맞닿는 부분, 외곽선을 대조했다.'),
                      ([28], '대체 구성과 대각 이동 단계 표지다.'), ([29,30,31], '퍼즐 25~27은 외곽선 또는 여러 조각선을 보여 준다.')],
}

IMAGE_NOTES = [
    ([0,1,7,17,20], '겹친 도형이나 목표 윤곽의 일부 미리보기다. 완전한 활동지와 답지는 별도로 기록한다.'),
    ([3,4,8,9,10,11,22,23,27], '펜토미노, 조각과 완성 후보, 탱그램과 블록의 보이는 자세를 대조했다. 사진에서 치수를 추정하지 않는다.'),
    ([15,25,26,28], '가정 안내나 위치말 미리보기다. 별도 배포본을 읽은 것으로 세지 않는다.'),
    ([18,19,21], '생활 그림의 평면 윤곽과 포함 관계의 예시다. 원근 사진에서 각도나 변 길이를 판정하지 않는다.'),
    ([2,5,6,12,13,14,16,24], '교사 안내와 활동 장면이다. 사진으로 수행의 독립 여부나 효과를 판단하지 않는다.'),
]

CLAIMS = [
    ('LT175','LT-P166',['2수03-03','2수03-04','2수03-05'],(1,2,3,6,7,8,9,10),('1587611148482','1587611421102','1608314436234','1608564871437'),
     '복합 그림에서 이미 그려진 도형을 세는 일과 여러 경계의 선분으로 다른 윤곽을 찾는 일을 구별한다. 닫혔는지와 꼭짓점을 직접 확인한다.',
     '찾아야 하는 윤곽은 열린 선일 수 있다. 열린 선은 삼각형이나 오각형의 경계를 완성하지 않는다.',
     '정사각형 안에 위쪽 변의 가운데 점에서 아래쪽 두 꼭짓점으로 선을 그었다. 안쪽 삼각형의 세 변을 따라가고, 비스듬한 두 선만 남기면 무엇이 달라지는지 설명한다.',
     '비스듬한 두 선과 정사각형의 아래쪽 변으로 삼각형이 닫힌다. 비스듬한 두 선만 있으면 열린 꺾은 선이다.',
     '도형의 이름과 함께 실제 세 변을 모두 짚는지, 열린 선을 닫힌 도형과 구별하는지 기록한다.'),
    ('LT176','LT-P167',['4수03-04','6수03-01','6수03-13'],(13,14),('1584564024223','1584564364786','1642006860884'),
     '같은 크기의 정사각형 다섯 칸으로 된 조각 두 개는 10칸을 덮을 수 있지만, 합이 같아도 외곽선에 맞으려면 겹침과 빈칸이 없어야 한다.',
     '초급 I의 위 도안에서는 첨부 힌트 P·L 또는 Z·T가 맞고 본문의 P·U는 회전·뒤집기·격자 이동을 허용해도 맞지 않는다. V~VIII의 링크는 다른 종류의 도안이다.',
     '10칸 도안을 5칸짜리 조각 두 개로 채우려 한다. 두 조각의 칸 수 합이 10이라는 정보만으로 맞는다고 할 수 있는가? 배치를 어떻게 확인할까?',
     '칸 수 합은 필요한 조건이다. 각 조각이 윤곽 안에 놓이고 겹치는 칸과 비는 칸이 없는지 실제 배치에서 확인해야 한다.',
     '필요한 넓이 조건과 실제 배치의 증거를 따로 확인한다.'),
    ('LT177','LT-P168',['4수03-04','6수03-01'],(5,11,15,16,17,19,20,25,26),('1587584002728','1587585517254','1588095036171','1588095062699'),
     '조각을 평행이동하면 방향이 유지된다. 방향이나 좌우 순서가 달라진 목표는 회전과 뒤집기를 각각 허용하는지 확인한다.',
     '대각선으로 이동하는 방향과 조각의 회전은 다른 변화다. 먼저 설명한 변환과 실제 조작에서 추가한 변환을 따로 기록한다.',
     '가로로 놓인 2 cm×1 cm 직사각형을 대각선 위쪽으로 밀면 긴 변이 세로가 되는가? 가로에서 세로로 바꾸려면 어떻게 할까?',
     '밀기만 하면 긴 변은 여전히 가로다. 90° 돌리면 긴 변이 세로가 되고, 그다음 필요한 위치까지 밀 수 있다.',
     '조각의 위치 변화와 변의 방향 변화를 따로 말하고, 대기 전 예상과 조작 후 수정의 순서를 기록한다.'),
    ('LT178','LT-P169',['2수03-02','6수03-09','6수03-10'],(0,19),(),
     '가린 모형을 재현할 때 조각 수, 닿는 면, 바닥에 놓인 부분과 관찰 방향을 따로 확인한다. 한 방향의 그림이 같아도 전체 모형은 다를 수 있다.',
     '10초 뒤 재현하는 활동은 기억과 조작의 영향을 함께 받는다. 정해진 시간의 수행을 공간 능력 점수로 사용하지 않는다.',
     '세 칸을 가로로 한 줄 놓고 왼쪽 끝 칸 위에 한 개를 더 얹은 모형을 봤다. 네 개를 바닥에 한 줄로 놓으면 무엇이 같고 무엇이 다른가?',
     '큐브 개수는 4개로 같다. 원래 모형은 바닥의 칸이 세 개이고 왼쪽 높이가 두 개다. 새 모형은 바닥의 칸이 네 개이고 높이는 모두 한 개다.',
     '모형을 고정한 채 앞과 위에서 본 차이를 말하고, 모형을 다시 본 뒤 바꾼 위치를 기록한다.'),
    ('LT179','LT-P170',['2수03-03','4수03-04','6수03-01'],(12,20,25,26,27),('1592585576150','1592586762854','1713196617742'),
     '같은 외곽이라도 내부 조각선이 있으면 조각의 선택과 위치 단서가 늘어난다. 같은 교구로 내부선이 있는 경우와 없는 경우를 비교한다.',
     '패턴 블록 10번과 탱그램 5~8에는 내부선이 있다. 해당 번호 자체나 내부선 유무 하나로 모든 도안의 난이도를 단정하지 않는다.',
     '정사각형 외곽과 빗변이 이 정사각형의 대각선과 같은 길이인 직각이등변삼각형 두 조각이 있다. 대각선을 표시하면 무엇을 알 수 있는가? 표시가 없을 때에도 완성할 수 있는가?',
     '대각선은 두 조각이 맞닿는 변과 각 조각의 위치를 알려 준다. 선이 없어도 두 빗변을 같은 대각선에서 맞대어 정사각형을 만들 수 있다.',
     '외곽선만 있을 때 생각한 분할 위치와 조각을 놓은 뒤 확인한 위치를 따로 기록한다.'),
    ('LT180','LT-P171',['2수03-06','6수03-13','6수03-14'],(7,8,28),('1615943737952',),
     '한 도형이 다른 도형의 내부에 완전히 포함되면 넓이 비교에 포함 관계를 이용할 수 있다. 포함되지 않는 보기에서는 무엇을 비교하는지 먼저 정한다.',
     '가장 작은 도형이라는 표현만으로 폭, 높이, 넓이를 동시에 판정할 수 없다. 도형을 찾는 일과 넓이를 재는 일을 구별한다.',
     '완전히 겹쳐 들어가는 두 직사각형과, 따로 놓인 1×6 직사각형과 2×2 정사각형을 본다. 어느 보기에서 포함 관계를 쓸 수 있는가? 따로 놓인 두 도형의 넓이는 각각 얼마인가?',
     '완전히 포함된 보기에서는 안쪽 도형의 넓이가 바깥 도형보다 크지 않다. 따로 놓인 보기에서는 단위가 같을 때 각각 6과 4제곱단위다.',
     '학생이 폭이나 높이 한 가지와 넓이를 혼동하는지, 포함 근거와 단위 넓이 계산을 구별하는지 확인한다.'),
]

OBSERVATIONS = [
    dict(id=oid,standard_codes=codes,question=question,expected=expected,interpretation=interpretation,student_validated=False)
    for _,oid,codes,_,_,_,_,question,expected,interpretation in CLAIMS
]


BOARD = {(x, y) for y, row in enumerate(('X....', 'XXXX.', '..XX.', '..XXX'))
         for x, cell in enumerate(row) if cell == 'X'}
PIECES = {
    'P': {(0,0),(1,0),(0,1),(1,1),(0,2)},
    'L': {(0,0),(0,1),(0,2),(0,3),(1,3)},
    'U': {(0,0),(2,0),(0,1),(1,1),(2,1)},
    'Z': {(0,0),(1,0),(1,1),(1,2),(2,2)},
    'T': {(0,0),(1,0),(2,0),(1,1),(1,2)},
}


def placements(piece):
    for swapped, sign_x, sign_y in product((False,True),(-1,1),(-1,1)):
        oriented = {(sign_x * (y if swapped else x), sign_y * (x if swapped else y)) for x,y in piece}
        left, top = min(x for x,_ in oriented), min(y for _,y in oriented)
        for dx,dy in product(range(5),range(4)):
            placed = frozenset((x-left+dx,y-top+dy) for x,y in oriented)
            if placed <= BOARD:
                yield placed


def covers(first, second):
    second_placements = set(placements(PIECES[second]))
    return sorted({tuple(sorted(first_placement)) for first_placement in placements(PIECES[first])
                   if frozenset(BOARD - first_placement) in second_placements})


def verify_examples():
    assert len(BOARD) == 10 and all(len(piece) == 5 for piece in PIECES.values())
    solutions = {pair:covers(*pair) for pair in ('PL','ZT','PU')}
    assert [len(solutions[pair]) for pair in ('PL','ZT','PU')] == [1,1,0]
    return dict(first_pentomino_outline_cells=sorted(BOARD), solutions=solutions,
                no_overlap_and_complete_cover=True, other_outline_area_checks=[1*6,2*2],
                original_cube_column_heights=[2,1,1], changed_cube_column_heights=[1,1,1,1])


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
    pages, bodies, selected = [load(CACHE / name) for name in ('activity-manifest.json','english-bodies.json','selection.json')]
    followup = copy.deepcopy(prior['activity_followup_catalog'])
    assert selected == [row for row in followup['records'] if not row['body_read']
                        and any(f'/math/{domain}/' in url for url in row['linked_level_urls']
                                for domain in ('spatial-visualization-and-imagery','disembedding-shapes'))]
    reading = [line.split('|',1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 29
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/',1)[-1] for row in pages] == [row[0] for row in reading]

    old_images = {row['url'] for row in prior['image_read_manifest']}
    old_pdfs = {row['url'] for row in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    other_page_kinds = {20:'teacher_resource',21:'activity_introduction',22:'activity_without_procedure'}
    for index,(page,body,(_,note)) in enumerate(zip(pages,bodies,reading,strict=True)):
        url = page['url']
        assert page['status'] == 200 and page['final_url'] == url and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256']
        teacher = 'Type:\nTeacher Resources' in body['body']
        intro = '\nActivity\n' not in body['body']
        assert teacher == (index == 20) and intro == (index in (20,21))
        kind = other_page_kinds.get(index,'activity_procedure')
        groups['teacher_resources' if teacher else 'activities'].append(page['key'])
        logs.append(dict(url=url, page_kind=kind, note=note))
        linked_images = {urljoin(url, img['src']) for img in page['images'] if '/upload/' in img.get('src','')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert {k:len(v) for k,v in groups.items()} == dict(general=6,domain_overviews=20,levels=224,activities=792,teacher_resources=32)

    raw_pdfs, raw_images = [load(ASSETS / f'{kind}-manifest.json') for kind in ('pdf','image')]
    new_pdfs, new_images, pdf_notes, image_notes = verified_assets(raw_pdfs,raw_images,PDF_NOTES,IMAGE_NOTES)
    assert (len(new_pdfs),sum(a['pdf_pages'] for a in new_pdfs),len(new_images)) == (21,97,29)
    assert asset_pairs(new_pdfs) == linked_pairs(pdfs) and asset_pairs(new_images) == linked_pairs(images)
    all_pdfs = prior['supplementary_pdf_read_manifest'] + new_pdfs
    all_images = prior['image_read_manifest'] + new_images
    unique_pdfs = {a['sha256']:a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs),sum(a['pdf_pages'] for a in all_pdfs),len(unique_pdfs),sum(unique_pdfs.values())) == (203,720,186,649)
    assert (len(all_images),len({a['sha256'] for a in all_images})) == (1083,1049)
    asset_urls = {pdf_name(asset['url']):asset['url'] for asset in new_pdfs}

    manifest = prior['html_read_manifest'] + [{k:row[k] for k in ('key','url','title','sha256','status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 1074
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'],followup['listed_body_pending']) == (824,0)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE,next_review=LIMITS)
    notes = dict(prior)
    notes.update(
        date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
        observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
        catalog_coverage={**prior['catalog_coverage'],'read_activity_bodies':824,'pending_activity_bodies':0},
        new_read_groups=dict(domain_overviews=0,levels=0,activities=28,teacher_resources=1,inline_images=29,supplementary_pdf_urls=21),
        remaining_spatial_reading_log=logs, completed_remaining_spatial_records=selected,
        remaining_spatial_checked_examples=verify_examples(), remaining_spatial_pdf_reading_log=pdf_notes,
        remaining_spatial_image_reading_log=image_notes,
        supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
        supplementary_pdf_coverage=dict(urls=203,page_occurrences=720,distinct_sha256_files=186,
            pages_after_file_deduplication=649,all_selected_pages_visual_reviewed=True,whole_site_attachment_review=False),
        pdf_exact_reuse_groups=reuse_groups(all_pdfs),
        pdf_reading_log={**prior['pdf_reading_log'],**{
            url:[f"{', '.join(map(str,row['pdf_pages']))}쪽. {row['note']}" for row in rows] for url,rows in pdf_notes.items()
        }},
        reading_log=prior['reading_log'] + ['공간 시각화와 도형 찾아내기의 활동 절차 26개, 소개 1개, 절차가 없는 페이지 1개, 교사자료 1개와 LT2 PDF 97쪽·이미지 29개 URL을 대조했다.'],
        source_corrections=prior['source_corrections'] + [dict(
            kind='disembedding_contours_transformation_and_mismatched_puzzle_attachments',
            locations=[pages[i]['url'] for i in (1,2,10,12,13,14,27,28)] + list(asset_urls.values()),
            action='열린 윤곽과 닫힌 도형, 내부선이 있는 도안, 이동과 회전, 펜토미노 조각 이름과 잘못 연결된 탱그램 파일을 구별했다.',
        )],
        remaining_spatial_material_followups=[
            dict(page=pages[13]['url'], material='펜토미노 V~VIII', status='linked_pdf_is_tangrams_5_to_8'),
            dict(page=pages[18]['url'], url='https://pmc.ncbi.nlm.nih.gov/articles/PMC3289766/',
                 material='Levine 외 퍼즐 놀이 종단 관찰 연구', status='author_lab_pdf_acquired_separate_review_pending'),
            dict(page=pages[20]['url'], url='https://eric.ed.gov/?id=EJ1394812',
                 material='Bofferding·Zhu 탱그램 관련 논문', status='bibliography_and_abstract_identified_full_text_pending'),
            dict(page=pages[21]['url'], material='가정용 도형·공간 관계 자료', status='preview_read_separate_handout_not_reviewed'),
            dict(page=pages[22]['url'], material='가정용 도형·공간 관계 자료', status='no_procedure_on_page'),
        ],
        unread_followups=prior['unread_followups'] + [LIMITS],
    )
    note_path = ROOT / NOTES
    write(note_path,notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=source['date'],read_scope=source['read_scope'])]
    source.update(
        date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
        bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
        method_note='공간 시각화와 도형 찾아내기의 본문 및 첨부에서 조각 배치와 경계 추적을 대조했다.',
        editorial_action='문헌 대응 6건과 자체 관찰 과제 6개를 추가했다.', observations=source['observations'] + OBSERVATIONS,
        image_read_manifest=all_images, supplementary_pdf_read_manifest=all_pdfs,
    )
    for cid,_,codes,indices,files,support,limit,*_ in CLAIMS:
        registry['claims'].append(dict(
            id=cid,source_id=SOURCE,role='related_theoretical_context',standard_codes=codes,
            locations=[pages[i]['url'] for i in indices] + [asset_urls[file] for file in files],
            support=support,does_not_establish=limit,independent_review=False,student_validated=False,
            target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry,claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE])
    write(bibliography_path,bibliography)
    write(ROOT / 'data/literature_claim_reviews.json',registry)
    write(queue_path,queue)
    build_report()
    print('Reviewed the final 29 listed LT2 pages, 21 PDFs and 29 images; added 6 claims and 6 observations.')


if __name__ == '__main__':
    main()


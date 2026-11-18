"""Record reviewed English LT2 plane-shape composition activities and teacher notes."""
import copy
from functools import lru_cache
from urllib.parse import urljoin, urlparse

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL

DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_2d_shapes_assets_review_notes.json'
PRIOR_SHA = '8727688db4d4bdfea39ab60fd3bd372c1e44693355d00963acfea02e541b0afb'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_composing_2d_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-composing-2d-shapes-activities'
SCOPE = '평면도형 구성에 연결된 공개 영어 페이지 36개를 대조했다. 활동 절차 33개와 탱그램 교사자료 3개다. 활동·교사자료 목록 824개 중 663개를 확인했고 161개가 남았다.'
LIMITS = '새 연결 PDF 24개, 삽입 이미지 41개 URL, 별도 영상·책 본문과 인용 연구는 후속 범위다. 조각의 계산·배치 검산을 학생 반응으로 집계하지 않는다.'

READING = """
building-with-the-minds-eye-shape-composer|말로 준 조각의 위치와 방향을 실제 배열에 옮긴다. 노란 조각을 마름모라고 부르는 예는 사용한 세트의 조각표를 먼저 확인한다. 마름모의 네 변은 길이가 같다.
can-you-draw-this|10초 동안 본 정사각형 분할을 가린 뒤 재현한다. 정확한 분할과 분할선을 기억했는지 구별한다.
duplicate-the-design|볼 수 있는 본보기와 실제로 배열한 조각을 비교한다. 크기·위치·방향 중 무엇을 일치시킬지 정한다.
five-busy-shapes|같은 크기 정사각형 두 개를 변끼리 이으면 직사각형이다. 대각선으로 자른 정사각형은 합동인 직각이등변삼각형 두 개가 된다. 이야기 제목과 처음 등장하는 네 정사각형·세 원의 수를 구별한다.
ghost-shapes-shape-composer|투명 조각을 놓고 겹쳐 본보기의 선을 만든다. 조각이 겹칠 수 있어 바깥 윤곽의 넓이가 조각 넓이의 합과 항상 같지는 않다.
how-did-i-make-this|정육각형을 중심에서 여섯 합동인 정삼각형으로 나눈다. 두 사다리꼴 또는 세 마름모로 나누는 예와 조각의 단위를 구별한다.
lets-make-something-new|왼쪽 도형의 조각을 오른쪽에 다시 배치한다. 같은 조각을 모두 쓰고 겹치지 않으면 두 그림의 넓이는 같다.
magic-keys-shape-composer|정사각형 다섯 개가 변을 맞대 연결돼야 한다. 여섯 개는 이야기 속 과제의 목표이고 가능한 전체 모양의 수는 아니다.
magic-keys-shape-composerunits-of-units|앞 단계와 같은 세 가지 규칙으로 열쇠 여섯 개를 만든다. 회전·반사로 맞는 배열을 한 모양으로 셀지 먼저 정한다.
make-a-pair|스스로 만든 구성을 다른 조각으로 한 번 더 만들고 대응하는 위치와 방향을 비교한다.
make-a-square|정사각형의 대각선 분할 조각을 포갠 뒤 변끼리 이어 다른 모양을 만든다. 똑같은 두 조각도 붙이는 변과 방향에 따라 바깥 모양이 달라진다.
paper-quilts|한 칸의 구성과 색을 여러 칸에 복제한다. 전체 목표 아홉 칸과 시간에 맞춘 최소 세 번을 구별한다.
pattern-block-play|자유롭게 만든 그림과 사용한 조각 수를 함께 기록한다. 도형 이름 말하기가 활동 참여의 전제는 아니다.
pattern-block-puzzles|윤곽에 조각을 대고 맞지 않으면 밀기·뒤집기·돌리기를 비교한다. 배치 전에 예상한 움직임과 실제로 한 움직임을 구별한다.
pattern-block-puzzles-and-tangram-puzzles-new-ways|먼저 필요한 조각 수를 예상한 뒤 윤곽을 실제로 덮어 센다. 같은 넓이는 맞는 배치의 필요조건이다.
pattern-block-puzzles-and-tangram-puzzles-picture-maker|패턴 블록과 일곱 조각 탱그램을 각각 맞는 윤곽에 사용한다. 같은 이름의 삼각형이라도 변 길이와 각이 다를 수 있다.
pattern-block-puzzles-and-tangram-puzzles-piece-assembler|내부 윤곽이 있는 퍼즐에서 어떤 조각이 어느 자리에 맞는지 확인한다. 퍼즐 번호 자체는 학습자의 수준 판정이 아니다.
pattern-block-puzzles-and-tangram-puzzles-shape-composer|주어진 윤곽을 조각의 밀기·돌리기·뒤집기로 채운다. 다른 교구의 같은 이름 조각을 서로 바꿔 쓰지 않는다.
pattern-block-puzzles-separate-shapes-actor-foundations|조각을 그림 위에 올려 보는 탐색과 윤곽에 정확히 맞추는 것을 별도로 관찰한다.
pentominoes-create-and-solve|다섯 칸씩 이어진 조각으로 퍼즐을 만들고 짝이 다시 푼다. 전체와 조각 수, 사용 조건을 함께 전한다.
picture-pie|원의 1/4 조각을 돌려 직선 변을 맞댄다. 중심을 지나는 두 수직선으로 자른 네 조각은 넓이가 같다.
put-the-halves-back-together-picture-maker|두 조각을 밀어 윤곽을 완성한다. 두 조각이라는 사실과 각각 전체의 절반인지는 따로 본다.
put-the-halves-back-together-shape-composer|돌리거나 뒤집어야 맞는 조각을 실제로 배치해 확인한다. 짝의 동의 표시와 맞는 이유를 말하는 것을 구별한다.
researcher-note-tangram-puzzles-picture-maker|방향을 45° 바꾼 토끼 퍼즐 예를 제시하는 교사자료다. 절차나 독립 검증으로 집계하지 않는다.
researcher-note-tangram-puzzles-piece-assembler|같은 정사각형을 다른 방향에 놓는 지원을 소개한다. 내부선이 있는 문제와 없는 문제를 구분한다.
researcher-note-tangram-puzzles-shape-composer|내부선을 줄이고 돌리기·뒤집기가 필요한 퍼즐로 진행하는 제안이다. 본문의 2022와 인용 권호의 2023을 구별한다.
see-it-build-it-check-it|본보기를 보면서 재현하는 절차와 5초 뒤 가린 상태에서 재현하는 절차를 나눠 기록한다.
super-shape-decomposer-with-help|중점끼리, 꼭짓점끼리, 꼭짓점과 중점을 잇는 자르기만 허용한다. 사용한 원본 종이 수와 남은 조각을 구별한다.
super-shape-ii-stemie|정육각형은 꽃, 정사각형은 로켓의 윤곽을 만든다. 먼저 분할선을 그린 뒤 잘라 맞추고 남은 조각을 확인한다.
super-shape-shape-decomposer-with-units-of-units|정해진 자르기 방법을 사용한다. ‘적은 종이’라는 목표는 남은 조각과 실제로 덮이는지를 별도로 확인한다.
tetrominoes|8×12를 네 칸 조각으로 덮으려면 24개다. T 네 조각의 4×4 배열은 이미 확인했고, S·Z 모양은 반사까지 허용해도 8×12를 덮지 못하는 경우를 별도로 검산한다.
the-shape-transformer|먼저 여러 분할을 예측하고 기계의 한 출력과 비교한다. 출력과 다른 분할도 같은 전체를 정확히 덮는지 본다.
the-shape-transformer-simple-decomposer|원에 다각형의 같은 변·각 조건을 적용하지 않는다. 정사각형을 반으로 나눌 때 직사각형 두 개 또는 삼각형 두 개가 되는 예를 구분한다.
tiling-patterns|6×4를 두 색으로 덮고 행·열의 반복 단위를 찾는다. 하나의 모양으로 덮는 예와 여러 모양도 허용하는 일반 타일링을 구별한다.
tiling-tetrominoes-shape-composer--units-of-units|한 종류를 여러 번 복제해 덮는다. 96÷4라는 개수 조건과 기하 배치가 가능한지를 따로 검사한다.
what-can-you-make|주사위를 굴려 받은 조각으로 만들고 다시 복제한다. 굴린 횟수와 완성 그림의 반복 단위를 혼동하지 않는다.
"""

CLAIMS = [
    ('LT133',['2수03-03','4수03-04','4수03-12'],[0,1,2,9,13,18,21,22,23,24,25,26,35],
     '윤곽에 맞는 조각을 먼저 예상하고 밀기·돌리기·뒤집기로 확인한다. 내부선과 본보기를 볼 수 있는 정도를 조절한다.',
     '교사자료가 제시한 지원과 아동이 실제로 독립해 해결한 기록은 별개다. 같은 모양이어도 방향과 위치가 다를 수 있다.'),
    ('LT134',['4수01-09','4수03-11','4수03-12','6수03-14'],[3,5,6,10,20,27,28,29,31,32],
     '정육각형을 중심에서 여섯 합동 정삼각형으로 나눌 수 있고, 정사각형의 대각선은 같은 넓이의 두 삼각형을 만든다. 분할된 조각을 모두 다시 쓸 때 넓이를 비교한다.',
     '기계의 출력은 한 가지 예다. 원에 다각형의 변·각 조건을 적용하지 않고, 둘로 자른 조각의 넓이가 같은지는 따로 확인한다.'),
    ('LT135',['4수03-12','6수03-12','6수03-13'],[4,6,14,15,16,17,18,33],
     '투명 조각을 겹쳐 그림을 만드는 과제와 빈틈도 겹침도 없이 덮는 과제는 조건이 다르다. 덮기에서는 예상한 개수와 실제 배치를 모두 확인한다.',
     '넓이가 같다는 계산만으로 덮을 수 있다고 판단하지 않는다. 일반 타일링에는 여러 종류의 조각을 쓸 수도 있다.'),
    ('LT136',['4수03-04','4수03-12','6수03-01'],[7,8,19],
     '다섯 정사각형이 변을 맞대 연결된 배치를 비교한다. 밀기·돌리기·뒤집기로 맞는 것을 한 모양으로 세면 열두 모양이다.',
     '과제에서 만드는 여섯 열쇠와 가능한 모양의 총수를 구별한다. 뒤집기를 금지하면 세는 수가 바뀐다.'),
    ('LT137',['2수02-01','2수02-02','4수03-12','6수03-13'],[9,11,33,35],
     '한 칸의 도안과 전체 격자, 행과 열의 반복 단위를 구별한다. 6×4 격자는 24칸이고 그 안의 반복 단위는 배열에 따라 다르다.',
     '두 색이 각각 12칸이라는 정보만으로 행과 열의 순서가 정해지지 않는다.'),
    ('LT138',['4수01-05','4수03-12','6수03-13'],[14,30,34],
     '8×12판은 96칸이라 네 칸 조각 24개가 필요하다. T형 네 개로 만든 4×4 배열을 반복할 수 있지만, S형과 그 반사형만 허용한 배치는 이 판을 덮을 수 없다.',
     '같은 넓이의 조각을 세는 계산과 조각 전체의 배치 가능성을 구별한다. 결론의 판 크기, 허용한 회전과 반사를 명시한다.'),
]

OBSERVATION_DATA = [
    ('LT-P124','꼭짓점 하나가 위로 향한 정사각형 자리에 수평인 정사각형 조각을 놓는다. 변 길이는 같다. 무엇을 하면 맞는가?',
     '조각을 45° 돌리고 중심을 맞추어 놓는다. 변 길이와 모양은 변하지 않는다.','크기를 바꾸는 것과 방향을 바꾸는 것을 구별한다.'),
    ('LT-P125','정사각형을 대각선으로 잘라 두 조각을 만들었다. 조각을 겹치지 않게 이어 다른 윤곽을 만들면 전체 넓이는 어떻게 되는가?',
     '두 조각은 합동인 삼각형이다. 둘을 모두 쓰고 겹치지 않으면 전체 넓이는 같다.','윤곽의 변화와 조각의 넓이 보존을 구별한다.'),
    ('LT-P126','넓이가 각각 4인 두 투명 조각이 넓이 1만큼 겹친다. 두 조각의 넓이를 더한 값과 바깥에서 보이는 영역의 넓이는 각각 얼마인가?',
     '넓이를 더하면 8이다. 겹친 넓이 1을 한 번 빼면 합친 영역은 7이다.','겹친 부분을 두 번 센 경우와 실제로 가린 범위를 구별한다.'),
    ('LT-P127','변을 맞대 만든 다섯 칸 열쇠를 90° 돌려 두었다. 회전과 반사로 포개면 같은 것으로 센다는 규칙에서 새 열쇠인가?',
     '포개어지는 같은 열쇠다. 점에서만 닿는 조각은 변을 맞대 연결한다는 조건을 만족하지 않는다.','배치 방향, 합동, 연결 조건을 구별한다.'),
    ('LT-P128','가로 6칸과 세로 4칸을 두 색이 번갈아 나오도록 채운다. 각 색은 몇 칸이고 가로·세로에서 몇 칸마다 같은 색이 나타나는가?',
     '각 색은 12칸이다. 가로와 세로에서 두 칸마다 같은 색이 나타난다.','전체의 개수와 방향별 반복 단위 길이를 구별한다.'),
    ('LT-P129','8×12판을 네 칸 조각으로 덮을 때 24개라는 계산이 나왔다. 모양이 다른 조각도 각각 24개만 있으면 다 덮을 수 있는가?',
     '24개는 넓이에서 나온 조건이다. T형은 4×4 배열을 반복해 덮을 수 있다. S형과 그 반사형만 쓰면 이 판을 덮는 배치가 없다.','개수 계산의 범위와 실제 배치 가능성의 범위를 분리한다.'),
]

OBSERVATIONS = [dict(id=oid, standard_codes=claim[1], question=question, expected=expected,
                     interpretation=interpretation, student_validated=False)
                for claim, (oid, question, expected, interpretation) in zip(CLAIMS, OBSERVATION_DATA, strict=True)]


def normalize(cells):
    cells = list(cells)
    x0 = min(x for x, _ in cells)
    y0 = min(y for _, y in cells)
    return tuple(sorted((x-x0, y-y0) for x, y in cells))


def forms(cells, reflected):
    result = set()
    for sign in ((1, -1) if reflected else (1,)):
        current = [(x, sign*y) for x, y in cells]
        for _ in range(4):
            result.add(normalize(current))
            current = [(-y, x) for x, y in current]
    return result


def pentomino_counts():
    fixed = {((0,0),)}
    for _ in range(4):
        fixed = {normalize((*shape, (x+dx,y+dy))) for shape in fixed for x,y in shape
                 for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)) if (x+dx,y+dy) not in shape}
    return len(fixed), len({min(forms(s, False)) for s in fixed}), len({min(forms(s, True)) for s in fixed})


def skew_cover_possible(width, height):
    placements = [[] for _ in range(width*height)]
    skew = ((1,0),(2,0),(0,1),(1,1))
    for shape in forms(skew, True):
        for y in range(height-max(b for _, b in shape)):
            for x in range(width-max(a for a, _ in shape)):
                indices = [(y+b)*width+x+a for a,b in shape]
                mask = sum(1 << index for index in indices)
                for index in indices:
                    placements[index].append(mask)
    all_cells = (1 << (width*height))-1

    @lru_cache(maxsize=None)
    def cover(used):
        if used == all_cells:
            return True
        empty = [i for i in range(width*height) if not used & (1 << i)]
        candidates = [[mask for mask in placements[i] if not mask & used] for i in empty]
        # Every complete tiling must cover the selected empty cell using one of these placements.
        return any(cover(used | mask) for mask in min(candidates, key=len))

    possible = cover(0)
    return possible, cover.cache_info().currsize, sum(map(len, placements)) // 4


def verify_examples(bodies):
    text = [row['body'] for row in bodies]
    assert 'arranging and overlaying' in text[4]
    assert '6 different triangles' in text[5] and 'six different magic keys' in text[7]
    assert '45-degree orientation' in text[23] and '45-degree orientation' in text[25]
    assert 'all angles and side lengths are equal' in text[32]
    assert 'a single shape' in text[33]
    assert all('8-by-12 grid' in text[i] for i in (30,34))
    square = ['AAAB','CABB','CCDB','CDDD']
    t = ((0,0),(1,0),(2,0),(1,1))
    assert all(normalize((x,y) for y,row in enumerate(square) for x,letter in enumerate(row) if letter==key)
               in forms(t, False) for key in 'ABCD')
    assert pentomino_counts() == (63,18,12)
    possible, states, placements = skew_cover_possible(8,12)
    assert not possible and placements == 272
    return dict(pentomino_counts=dict(fixed=63, rotation_only=18, rotation_and_reflection=12),
                t_tile_4_by_4=square, board=[8,12], copies=8*12//4,
                skew_rotations_and_reflections=dict(placements=placements, explored_states=states, possible=possible))


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
                        and any('/math/composing-2d-shapes/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|', 1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 36
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
        is_teacher_note = url.rsplit('/', 1)[-1].startswith('researcher-note-tangram-puzzles-')
        assert ('\nActivity\n' in body['body']) != is_teacher_note
        assert ('Type:\nTeacher Resources' in body['body']) == is_teacher_note
        groups['teacher_resources' if is_teacher_note else 'activities'].append(page['key'])
        logs.append(dict(url=url, page_kind='teacher_research_note' if is_teacher_note else 'activity_procedure', note=note))
        linked_images = {urljoin(url, image['src']) for image in page['images'] if '/upload/' in image.get('src', '')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert sum(row['page_kind'] == 'teacher_research_note' for row in logs) == 3
    assert len({url for links in images.values() for url in links}) == 41
    assert len({url for links in pdfs.values() for url in links}) == 24
    assert {k: len(v) for k, v in groups.items()} == dict(general=6, domain_overviews=20, levels=224, activities=644, teacher_resources=19)
    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key', 'url', 'title', 'sha256', 'status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 913
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'], followup['listed_body_pending']) == (663, 161)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
                 observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
                 catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies': 663, 'pending_activity_bodies': 161},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=33, teacher_resources=3, inline_images=0, supplementary_pdf_urls=0),
                 composing_2d_reading_log=logs, completed_composing_2d_records=selected,
                 composing_2d_pdf_urls_not_reviewed=pdfs, composing_2d_image_urls_not_reviewed=images,
                 composing_2d_procedure_scope=dict(activity_procedures=33, teacher_research_notes=3),
                 composing_2d_checked_examples=examples,
                 composing_2d_cited_works_pending=[
                     dict(linking_pages=[pages[i]['url'] for i in (21,22)], url='https://doi.org/10.1037/0012-1649.42.6.1259',
                          read_scope='시카고대 연구실에서 제공하는 본문을 확보했다. 자료와 원연구의 대조는 별도다.'),
                     dict(linking_pages=[pages[i]['url'] for i in (23,24,25)], url='https://doi.org/10.5951/MTLT.2022.0200',
                          read_scope='권호의 발행연도는 2023년이다. 본문 대조는 별도다.'),
                     dict(linking_pages=[pages[i]['url'] for i in (7,8)], citation='Moss & Bruce, 2016, Taking Shape',
                          read_scope='LT2 활동과 서지 확인. 단행본의 해당 부분은 별도다.'),
                 ],
                 reading_log=prior['reading_log'] + ['평면도형 구성의 활동 절차 33개와 탱그램 교사자료 3개를 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='composition_overlay_area_and_exact_tiling', locations=[pages[i]['url'] for i in (3,4,5,7,14,23,30,31,32,33,34)],
                     action='겹침과 덮기, 조각의 합동과 방향, 격자의 개수 조건과 실제 배치를 구별했다.')],
                 unread_followups=[LIMITS, '평면도형 구성의 첨부와 연결 원연구를 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
                  method_note='조각의 겹침, 분할, 구성과 타일링을 영어 활동 본문과 대조했다.',
                  editorial_action='문헌 대응 6건과 자체 관찰 과제 6개를 추가했다.', observations=source['observations'] + OBSERVATIONS)
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
    print('Reviewed 36 English pages; added 6 mappings and 6 observations. Public activity bodies pending: 161.')


if __name__ == '__main__':
    main()

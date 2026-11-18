"""Register LT2 spatial orientation activities, diagrams, and checked examples."""
import copy
from collections import deque
from fractions import Fraction
from urllib.parse import urljoin, urlparse

from extend_lt2_composing_2d_assets_review import pdf_name, verified_assets
from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_angle_turn_review_notes.json'
PRIOR_SHA = '4cded48fc799c4279642132abaad1267a6f4ce62d8d0e5372554a8d71e0ca88a'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_spatial_orientation_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-spatial-orientation-activities'
ASSETS = ROOT / 'tmp/literature/lt2-spatial-orientation-assets'
ROSIE_URL = 'https://www.st-catharines.gloucs.sch.uk/wp-content/uploads/2020/04/Rosies-Walk.pdf'
STUDY_URL = 'https://research.unipd.it/handle/11577/3318127'
YARD_URL = 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors'
SCOPE = ('공개 영어 HTML 1010개를 대조했다. 활동·교사자료 목록 824개 중 760개를 확인했고 64개가 남았다. '
         '공간 방향의 영어 페이지 32개, LT2 PDF 1개 URL·1쪽과 이미지 33개 URL을 확인했다.')
LIMITS = ('삽입 지도와 좌표 그림은 본문 및 실제 활동지와 구별했다. 외부 그림책, 기관의 좌표 삼목 활동지, '
          '위치 표지 연구의 결과표와 비교 조건, 영상과 실제 수업 결과는 별도다.')

READING = """
another-bear-hunt|새로운 장소말로 경로를 만들고 역순으로 돌아온다. 돌아올 때 진행 방향과 회전도 다시 정한다.
baby-basketball|공과 포개는 컵으로 안과 밖, 위와 아래를 나타낸다. 어느 물체를 기준으로 말하는지 표시한다.
block-play-spatial-orientation-foundations|쌓기·가라지·정리 중의 위치를 말과 몸짓으로 나타낸다. 물체와 기준 물체를 따로 짚는다.
dance-the-hokey-pokey|원의 안팎과 몸을 기준으로 한 왼쪽·오른쪽을 움직임으로 확인한다. 영상은 별도다.
exploring-your-spatial-world-spatial-orientation-foundations|이동과 손 뻗기 기회를 안내한다. 지원한 이동과 스스로 선택한 방향을 구별한다.
find-the-lost-pet|교실의 지도와 실제 표지를 맞춰 물체를 찾는다. 지도의 방향을 먼저 확인한다.
follow-the-gem-path|같은 방향을 보는 두 사람이 5×5 지도에서 이동 지시를 주고받는다. 화살표의 회전과 한 칸 이동을 구별한다.
going-on-a-bear-hunt|교실에 표지를 정해 이야기 경로를 가고 되돌아온다. 장소의 순서와 몸을 기준으로 한 방향을 구별한다.
helicopter-ride|항공 사진에서 방위·거리·표지와 대안 경로를 비교한다. 프로젝트 과제에는 가상 학교 지도를 사용한다.
landmark-locater|위에서 본 설명과 걸으면서 본 설명에 표지 다섯 개씩을 쓴다. 두 보기의 표지 종류가 다르다.
letter-delivery-stemie|학교에서 편지 받을 사람의 위치와 경로를 설명한다. 말·그림과 이동 보조를 구별한다.
local-framework-user-general-activity|교실 모형과 경로 지도를 만들며 가깝다·지나간다를 비교한다. 표지와 지도 위 위치를 대응한다.
local-self-framework-user-general-activity|서 있는 지점을 바꾸며 표지를 가리키고, 축소 모형의 위치와 실제 위치를 연결한다.
mail-carriers|좌표와 격자 이동 거리로 배달 경로를 비교한다. 통로가 있는 실제 경로와 제한 없는 격자 거리를 구별한다.
map-user-general-activity|방향·거리·위치·무엇인지의 네 질문으로 지도를 읽는다. 지도 방향과 걸어가는 방향을 따로 본다.
movement-is-learning|안전한 공간의 자유 이동을 교사자료로 안내한다. 본문 소개를 별도 효과 시험으로 세지 않는다.
number-cylinders|장난감 조작 중 안·위·아래를 설명한다. 교구의 명칭만으로 수 세기 활동으로 분류하지 않는다.
obstacle-course-map-user|이야기 경로를 장애물 코스와 범례가 있는 지도에 나타낸다. 그림책은 별도다.
on-the-move--path-integrator|이동하며 위치말을 듣거나 방향을 선택한다. 움직임과 의사 표시를 각각 관찰한다.
playground-geocache|출발점과 방위, 길이 단위와 축척을 기록한다. 야드자와 미터자 표기를 같은 길이로 읽지 않는다.
playing-in-padded-area|완충된 공간에서 경사판 위·아래와 높고 낮음을 말한다. 실제 경사각 측정 과제와 구별한다.
playing-with-stuffed-animals-spatial-orientation|인형이 물체의 앞·뒤·옆·안에 놓이는 예를 비교한다.
researcher-note--spatial-language|영어 위치말과 기준의 변화를 설명한다. 언어와 연령이 다른 집단의 판정 기준으로 바로 옮기지 않는다.
researcher-note-language-of-space-path-integrator|이동·표지·거리 단서가 경로 재현을 도울 수 있다는 연구자 설명이다. 원연구 표본과 비교는 별도다.
researcher-note-language-of-space-place-learner|가까운 표지와 방의 벽을 기준으로 위치를 찾는 예를 설명한다.
researchers-note-language-of-space-local-self-framework-user|익숙한 표지와 경로를 걸으며 사이·옆을 말하는 기회를 계획한다.
ring-stacker|고리를 잡고 움직이는 활동에 위치말을 연결한다. 배열의 수나 측정 목표는 별개다.
route-map-follower-general-activity|직접 만든 경로 지도를 교환한다. 출발 위치와 방향이 전달되었는지 확인한다.
small-local-framework-user-general-activity|경로의 길고 짧음, 앞·뒤와 좌우를 말로 설명한다. 지도 방향과 말하는 사람의 방향을 확인한다.
spatial-talk-path-integrator|일과에서 위치말을 쓰는 안내다. 같은 위치라도 기준 물체가 달라지면 표현이 달라질 수 있다.
tic-tac-toe-with-coordinates|삼목 표식을 칸이 아니라 격자선 교점에 둔다. 두 축의 교점은 원점이고 삽입 예시는 본문의 눈금 범위와 다르다.
up-down-all-around-stemie|보기·가리키기·이동으로 공간 관계를 나타낸다. 이동이나 언어 지원을 따로 기록한다.
"""

PDF_NOTES = {
    '1616770828900': [([1], '다리·축구 골대·미끄럼틀·연못·그네·나무·시소·구름사다리 카드 8장이다. 두 이야기에서 공통으로 쓰는 표지는 미끄럼틀과 축구 골대다.')],
}
IMAGE_NOTES = [
    ([0], '일상 위치말과 도형 이름을 제시하는 그림이다.'),
    ([6,7], '곰 사냥 그림책 표지다. 본문과 낭독은 별도다.'),
    ([12,13,14,16], '연구자 소개용 사진이다. 영상과 논문의 내용은 별도다.'),
    ([21,22,23,28,29], '좌표·장소 지도·방위·보석 길과 표지 배치의 삽입 그림이다. 21의 0~8 눈금은 본문의 0~6과 다르다. 28은 5×5 칸이다. 29는 두 이야기의 정답판이 아니다.'),
    ([1,2,3,4,5,8,9,10,11,15,17,18,19,20,24,25,26,27,30,31,32], '활동 장면, 항공 사진과 재료 이미지다. 실제 주소, 이동 거리와 학생 수행을 그림에서 추정하지 않는다.'),
]

CLAIMS = [
    ('LT162','LT-P153',['4수03-03','9수02-05'],(13,30),('1588981233921',),
     '점 (x,y)는 x값의 세로 격자선과 y값의 가로 격자선이 만나는 곳이다. 좌표축끼리 만나는 점은 원점이다.',
     '0~6 눈금의 6×6 칸은 7×7 교점이다. 삽입 그림은 0~8까지 보여 활동지의 눈금 범위를 대신하지 않는다.',
     '가로와 세로 눈금을 0에서 6까지 붙인 격자에서 (2,5)를 찍는다. 좌표축의 교점은 어디이며, 격자 교점은 모두 몇 개인가?',
     'x=2인 세로선과 y=5인 가로선의 교점이 (2,5)다. 두 축의 교점은 (0,0)이다. 한 방향에 눈금이 7개라 교점은 49개다.',
     '두 축과 두 격자선을 가리키고 칸과 교점을 따로 센다.'),
    ('LT163','LT-P154',['2수03-02','4수03-04'],(0,3,6,7,10,13,27),(),
     '이동자의 오른쪽은 바라보는 방향에 따라 달라진다. 같은 길을 되짚을 때는 이동 순서를 뒤집고 각 구간을 반대 방향으로 간다.',
     '고정된 지도에서의 오른쪽과 사람의 오른쪽을 구별한다. 되돌아가는 첫 방향은 마지막 도착 방향의 반대다.',
     '북쪽으로 2칸 간 뒤 오른쪽으로 돌아 1칸 간다. 온 길을 그대로 돌아오려면 처음 어느 쪽을 보고 몇 칸 간 뒤 어느 쪽으로 돌아야 하는가?',
     '먼저 서쪽을 보고 1칸 간다. 그다음 이동자 기준 왼쪽으로 돌아 남쪽으로 2칸 가면 출발점이다.',
     '지도 위 북쪽과 이동자가 바라보는 방향을 별도로 표시한다.'),
    ('LT164','LT-P155',['2수03-13','9수02-05','9수03-15'],(6,11,13,28),('1616653490211',),
     '가로·세로로만 인접 칸을 이동할 때 두 방향의 좌표 차이 합은 이동 수의 하한이다. 이만큼만 이동하는 길이 열려 있으면 그 길이 최단이다.',
     '장애물이 있어 두 방향으로만 전진하는 길이 없으면 우회가 필요할 수 있다. 대각선 직선거리는 이동 칸 수와 다르다.',
     '5×5 칸에서 오른쪽 위 칸부터 왼쪽 아래 칸까지 간다. 가로·세로로만 이동하고 위쪽과 왼쪽 가장자리는 비어 있다. 최소 몇 칸을 이동하는가?',
     '왼쪽 4칸과 아래 4칸이 반드시 필요하다. 위쪽 가장자리에서 왼쪽으로 4칸, 왼쪽 가장자리에서 아래로 4칸 가면 8칸이므로 최단이다.',
     '가능한 길 하나와 그보다 짧을 수 없는 이유를 모두 말하게 한다.'),
    ('LT165','LT-P156',['2수03-10','4수03-15','6수02-04'],(8,14,19),(),
     '지도에서 방향과 거리, 시작 위치, 축척을 적는다. 같은 숫자라도 미터와 야드는 실제 길이가 다르므로 단위를 확인한 뒤 같은 척도로 바꾼다.',
     '원문은 야드자와 미터자를 섞어 언급한다. 예시 지도는 길이 단위를 먼저 정하고, 주행 거리와 직선 거리를 따로 표시한다.',
     '실제 3 m를 지도에서 1 cm로 나타낸다. 동쪽으로 12 m 이동을 그리려면 어디로 몇 cm를 그리는가? 12 yd도 같은 길이로 표시해도 되는가?',
     '동쪽으로 4 cm를 그린다. 1 yd는 0.9144 m이므로 12 yd는 12 m와 다르다. 같은 축척에서는 미터로 환산한 뒤 표시한다.',
     '방향과 길이 단위, 지도와 실제 길이의 비를 확인한다.'),
    ('LT166','LT-P157',['2수03-02','6수03-10'],(5,9,17),('1616770828900','1616778958562'),
     '위에서 본 지도는 표지의 고정된 위치를, 이동 경로 설명은 진행 방향과 표지 순서를 나타낼 수 있다. LT2의 두 예시는 같은 카드 여덟 장을 쓰지만 이야기에서 실제 나오는 표지가 다르다.',
     '어느 관점에서 더 잘 찾는지 비교할 때 표지 종류·개수, 언어와 단서, 설명 횟수와 도움을 함께 확인한다. 삽입 배치는 두 이야기의 답안이 아니다.',
     '같은 공원에서 위에서 본 설명과 걸어가는 설명을 비교한다. 위에서 본 이야기에는 나무가 있고 걸어가는 이야기에는 나무 대신 연못이 있다. 어떤 조건을 맞추어 다시 비교하는가?',
     '두 이야기에서 동일한 표지와 위치를 쓰고 설명 횟수와 도움을 맞춘다. 위에서 보는지 걸어가며 설명하는지만 구분해 본다.',
     '관점과 표지 기억의 조건을 따로 말하도록 한다.'),
    ('LT167','LT-P158',['2수03-02'],(1,2,4,18,21,22,24,25,26,29,31),(),
     '안·뒤·사이 같은 위치말은 기준 물체와 함께 기록한다. 한 물체가 동시에 상자 안에 있고 의자 뒤에 놓일 수 있다.',
     '말하기, 손짓, 모형으로 보인 위치 관계를 구별하고, 도움 여부와 표현 기준을 함께 적는다.',
     '앞뒤가 분명한 의자의 뒤쪽에 상자 전체가 놓여 있고 블록은 그 상자 안에 있다. 블록은 무엇의 안이며 무엇의 뒤인지 말하거나 가리킨다.',
     '블록은 상자 안이고, 의자의 앞뒤가 정해져 있다면 의자 뒤다. 두 설명은 기준 물체가 다르므로 동시에 성립한다.',
     '설명에서 대상과 기준 물체를 각각 짚는다.'),
]
OBSERVATIONS = [
    dict(id=oid,standard_codes=codes,question=question,expected=expected,interpretation=interpretation,student_validated=False)
    for _,oid,codes,_,_,_,_,question,expected,interpretation in CLAIMS
]


def verify_examples():
    start, goal = (4,4), (0,0)
    blocked = {(3,3),(1,1)}
    frontier = deque([(start,0)])
    visited = {start}
    while frontier:
        (x,y), distance = frontier.popleft()
        if (x,y) == goal:
            break
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            point = x+dx,y+dy
            if all(0 <= coordinate < 5 for coordinate in point) and point not in blocked and point not in visited:
                visited.add(point)
                frontier.append((point,distance+1))
    assert (x,y) == goal and distance == 8
    survey = {'swings','soccer goal','tree','seesaw','slide'}
    route = {'slide','monkey bars','pond','soccer goal','bridge'}
    assert survey & route == {'slide','soccer goal'} and len(survey | route) == 8
    assert 7*7 == 49 and Fraction(12,3) == 4 and Fraction('0.9144')*12 == Fraction('10.9728')
    return dict(grid_body_cell_count=36, grid_body_intersection_count=49, grid_body_axis_range=[0,6],
                grid_insert_axis_range=[0,8], gem_start=start, gem_goal=goal,
                gem_blocked=sorted(blocked), gem_shortest_path_steps=distance,
                survey_landmarks=sorted(survey), route_landmarks=sorted(route),
                common_landmarks=sorted(survey & route), international_yard_in_metres='0.9144')


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
                        and any('/math/spatial-orientation/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|',1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 32
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/',1)[-1] for row in pages] == [row[0] for row in reading]

    old_images = {row['url'] for row in prior['image_read_manifest']}
    old_pdfs = {row['url'] for row in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for page, body, (_, note) in zip(pages,bodies,reading,strict=True):
        url = page['url']
        assert page['status'] == 200 and page['final_url'] == url and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256']
        teacher = 'Type:\nTeacher Resources' in body['body']
        assert '\nActivity\n' in body['body']
        kind = 'teacher_resource' if teacher else 'activity_procedure'
        groups['teacher_resources' if teacher else 'activities'].append(page['key'])
        logs.append(dict(url=url, page_kind=kind, note=note))
        linked_images = {urljoin(url, image['src']) for image in page['images'] if '/upload/' in image.get('src','')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert [row['page_kind'] for row in logs].count('teacher_resource') == 5
    assert pdfs[pages[17]['url']] == [ROSIE_URL]
    lt2_pdfs = {page: [url for url in urls if url != ROSIE_URL] for page, urls in pdfs.items()}

    raw_pdfs, raw_images = [load(ASSETS / f'{kind}-manifest.json') for kind in ('pdf','image')]
    new_pdfs, new_images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images, PDF_NOTES, IMAGE_NOTES)
    assert len(new_pdfs) == 1 and len(new_images) == 33
    assert asset_pairs(new_pdfs) == linked_pairs(lt2_pdfs) and asset_pairs(new_images) == linked_pairs(images)
    all_pdfs = prior['supplementary_pdf_read_manifest'] + new_pdfs
    all_images = prior['image_read_manifest'] + new_images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (178,616)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (164,560)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (1012,982)
    asset_urls = {pdf_name(asset['url']): asset['url'] for asset in new_pdfs + new_images}

    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key','url','title','sha256','status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 1010
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'],followup['listed_body_pending']) == (760,64)

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
        catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies':760, 'pending_activity_bodies':64},
        new_read_groups=dict(domain_overviews=0,levels=0,activities=27,teacher_resources=5,inline_images=33,supplementary_pdf_urls=1),
        spatial_orientation_reading_log=logs, completed_spatial_orientation_records=selected, spatial_orientation_checked_examples=verify_examples(),
        spatial_orientation_pdf_reading_log=pdf_notes, spatial_orientation_image_reading_log=image_notes,
        supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
        supplementary_pdf_coverage=dict(urls=178,page_occurrences=616,distinct_sha256_files=164,
            pages_after_file_deduplication=560,all_selected_pages_visual_reviewed=True,whole_site_attachment_review=False),
        pdf_exact_reuse_groups=reuse_groups(all_pdfs),
        pdf_reading_log={**prior['pdf_reading_log'], **{
            url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows] for url,rows in pdf_notes.items()
        }},
        reading_log=prior['reading_log'] + ['공간 방향의 영어 페이지 32개와 LT2 PDF 1쪽·이미지 33개 URL을 대조했다.'],
        source_corrections=prior['source_corrections'] + [dict(
            kind='coordinate_grids_route_distance_and_reference_frames',
            locations=[pages[i]['url'] for i in (6,9,13,19,30)] + [asset_urls[id] for id in ('1616770828900','1588981233921','1616653490211')],
            action='좌표축과 격자선의 교점, 그림과 본문의 축 범위, 좌우 기준, 길이 단위, 표지 구성을 구별했다.',
        )],
        spatial_orientation_separate_material_pending=[
            dict(page=pages[6]['url'], material='경로와 좌우 손 인쇄물', status='partial_preview_read_separate_print_not_read'),
            dict(page=pages[17]['url'], url=ROSIE_URL, material='Rosie’s Walk', status='linked_external_book_not_read'),
            dict(page=pages[30]['url'], material='좌표 삼목 기관 활동지', status='institutional_resource_not_read'),
        ],
        spatial_orientation_cited_study=dict(
            url=STUDY_URL, doi='10.1016/j.cogdev.2019.100841', linking_page=pages[9]['url'],
            read_scope='대학 저장소의 초록과 서지', reported_sample='5~6세 63명',
            status='publisher_full_text_not_read', limit='원문 비교 조건과 결과표의 검토는 남았다.',
        ),
        unread_followups=prior['unread_followups'] + [LIMITS],
    )
    note_path = ROOT / NOTES
    write(note_path,notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=source['date'],read_scope=source['read_scope'])]
    source.update(
        date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(note_path),snapshot_history=history,
        bibliography_snapshot=digest(entry),html_read_manifest=manifest,read_scope=SCOPE,limits=LIMITS,
        method_note='공간 방향, 좌표 교점, 지도 표지와 경로 길이를 본문·첨부에서 대조했다.',
        editorial_action='문헌 대응 6건과 자체 관찰 과제 6개를 추가했다.',observations=source['observations'] + OBSERVATIONS,
        image_read_manifest=all_images,supplementary_pdf_read_manifest=all_pdfs,
    )
    for cid,_,codes,indices,files,support,limit,*_ in CLAIMS:
        registry['claims'].append(dict(
            id=cid,source_id=SOURCE,role='related_theoretical_context',standard_codes=codes,
            locations=[pages[i]['url'] for i in indices]+[asset_urls[file] for file in files]+([YARD_URL] if cid=='LT165' else []),
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
    print('Reviewed 32 spatial orientation pages, 1 LT2 PDF and 33 images; added 6 claims and 6 observations.')


if __name__ == '__main__':
    main()

"""Record checked LT2 plane-geometry cards, handouts, and inline figures."""
import copy
from math import sqrt

from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_2d_shapes_activities_review_notes.json'
PRIOR_SHA = 'a28b4ed57b65ae4053bc3b8ee16d7b67781fe5695d83e7cccfb1875340b93b3e'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_2d_shapes_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-2d-shapes-assets'
SCOPE = ('공개 영어 HTML 877개와 활동·교사자료 페이지 627개를 확인했다. 목록에 197개가 남았다. '
         '평면도형의 연결 PDF 30개 URL·185쪽과 삽입 이미지 92개 URL을 대조했다. '
         '연결 PDF는 이번 범위에서 동일 파일을 한 번씩 세면 28개·153쪽이다.')
LIMITS = ('분류 카드의 문자와 그림을 대조했고, 사진의 실제 중심·각도 및 인쇄물 크기는 측정하지 않았다. '
          '별도 가정 자료, 영상, 책 본문 및 연결 원연구의 본문 대조가 남아 있다.')

PDF_NOTES = {
    '1593028192976': [([1,2,3], '사각형 가족 이야기다. 마주 보는 각이 각각 같은 것만으로 마름모를 정할 수 없다. 연꼴의 두 쌍은 서로 이웃한 같은 길이의 변이지 평행한 변이 아니다.'),
                       ([4,5], '예각·둔각·직각인 이등변삼각형과 정삼각형을 이야기로 나타낸다. 부모와 자녀라는 관계를 도형 범주의 포함으로 해석하지 않는다.')],
    '1593028242251': [([1], '여섯 사각형 조각이다. 평행한 변의 쌍과 직각, 같은 변을 확인한다.'),
                       ([2,3], '삼각형과 사각형 조각의 방향·크기·색이 다양하다. 기울기와 범주를 구별한다.')],
    '1593028334885': [([1], '이등변의 예각·둔각·직각 사례를 구분한다. 맨 위 그림은 부등변삼각형의 예로 설명되지만 이등변삼각형이 부등변삼각형에 속하지는 않는다.')],
    '1593029263564': [([1], '분류표 화살표와 각 칸의 문구를 분리해 읽는다. 직사각형과 정사각형 칸에 직각 조건이 빠졌다. 이웃한 같은 변 두 쌍의 연꼴 정의에서는 마름모도 조건을 충족한다.'),
                       ([2], '별도 도형이나 답안이 없는 빈 쪽이다.')],
    '1599505855845': [([1], '개별 생각, 짝과 비교, 전체 공유를 나타내는 영어 그림 세 장이다.')],
    '1599507330697': [([1], '짝과 말하는 같은 장면을 2×2로 반복한 인쇄 자료다.')],
    '1599507486669': [([1], '영어로 생각·짝·공유 절차와 동작 신호를 안내한다. 도형의 답안과는 별도다.')],
    '1637183672407': [([1], '규칙을 보여 주기, 고르기, 답 확인, 역할 바꾸기의 네 절차 카드다.')],
    '1642175172312': [([1,2,3], 'T·Z·L·N, U·W·Y·I, P·X·F·V를 네 개씩 배치했다. 각 펜토미노는 변을 맞대 연결한 다섯 칸이며, 대칭 활동에서는 축에 대해 조각을 뒤집어 본다.')],
    '1676058109278': [([1], '바닥에 분필로 그린 여러 닫힌 윤곽의 사진이다. 사진에서 중심 일치를 측정할 수 없다.')],
    '1676058133384': [([1], '종이에 그린 여러 겹의 한 줄을 살펴보는 사진이다. 감긴 한 줄과 여러 개의 닫힌 원을 구별한다.')],
    '1676058163096': [([1], '둥근 재료 주위에 끈을 놓아 교차시키는 사진이다. 바깥 네 변이 접하는 조건을 별도로 확인한다.')],
    '1677859176095': [([1,2], '원·삼각형·정사각형·직사각형의 예와 비예다. 회전한 정사각형도 직사각형 예에 들어간다.'),
                       ([3], '오각형과 육각형의 정다각형 설명에 각이 모두 같다는 조건이 빠졌다.'),
                       ([4], '마름모 설명과 사다리꼴 설명이 이어진다. 사다리꼴의 한 쌍 조건 아래에 두 쌍·정사각형 설명이 잘못 반복된다. 한 옆변이 밑변에 수직이면 양 밑변에서 직각이 하나씩 생긴다.'),
                       ([5], '평행사변형과 사각형 예다. 굽거나 열린 윤곽과 닫힌 직선 변을 구분한다.')],
    '1680268550002': [([1], '영어 규칙 목록에서 도형 범주, 닫힘, 변·각 개수, 직각과 대칭을 차례로 비교한다.')],
    '1686591296049': [(list(range(1,12)), '첫 카드 묶음은 원·정사각형·직사각형·육각형·삼각형의 변형이다.'),
                       (list(range(12,22)), '둘째 묶음은 오각형·팔각형·사다리꼴·마름모·타원 예다.'),
                       (list(range(22,28)), '마지막 묶음은 교차하거나 열린 모양과 굽은 경계, 오목한 닫힌 육각형을 포함한다. 어떤 조건의 비예인지 확인한다.')],
    '1691086719769': [([1], '생각·짝·공유의 스페인어 그림 세 장이다.')],
    '1691162805076': [([1], '스페인어 생각·짝·공유 절차와 참여 동작을 제시한다.')],
    '1691163310038': [([1], '스페인어 분류 규칙 목록이다. 분류판에 실제 놓이는 도형은 별도로 확인한다.')],
    '1691174546626': [([1,2], '스페인어 목차·절차와 빈 분류판이다.'),
                       (list(range(3,28)), '두 칸에 놓인 도형을 모두 확인했다. 인쇄 10번은 왼쪽 삼각형과 오른쪽 비예가 보여 목차의 육각형 대 사다리꼴과 다르다.')],
    '1693418532317': [(list(range(1,6)), '1677859176095의 도형 용어집과 PDF 해시가 같다.')],
    '1694816631737': [(list(range(1,17)), '짝수 쪽은 규칙 카드 뒷면이다. 홀수 쪽 앞면은 변 또는 각의 개수와 최솟값을 예와 비예로 제시한다.'),
                       ([17,18], '5보다 많은 변을 다룬다. 8변 도형이 비예에 들어가 있고 위쪽 육각형에는 변 화살표가 5개만 보인다.'),
                       (list(range(19,27)), '각이나 변의 개수 경계를 비교한다. 4보다 적은 직선 변의 예는 0개도 포함할 수 있으므로 곡선의 유무와 다각형 여부를 따로 말한다.'),
                       ([27,28], '3변·3각 카드의 예에 굽은 경계가 있다. 직선 세 변이 닫히는 삼각형 기준에서는 빼야 한다.'),
                       (list(range(29,35)), '변과 각이 각각 4·5·6개인 도형을 나눈다. 곡선과 열린 모양의 유사성을 분류 근거와 구분한다.')],
    '1699027289688': [([1], '영어 분류 규칙 목록이다. 같은 범주의 방향과 크기 차이, 각과 대칭의 속성을 나눈다.')],
    '1701453581228': [([1], '초록과 빨강 엄지로 예·비예에 답하는 카드다. 근거를 말하는 발문이 별도로 필요하다.')],
    '1701984867317': [([1], '직선 변 수를 3과 4 중심으로 비교한다. 비예에 적힌 수와 실제 직선 경계를 따로 대조한다.')],
    '1705099303904': [([1], '직사각형에 정사각형을 포함하고 사다리꼴은 평행한 변이 정확히 한 쌍인 규칙을 쓴다.')],
    '1706566075567': [([1,2], '열림·닫힘과 삼각형·정사각형·직사각형·마름모 등의 여집합을 제시한다. 범주 포함을 반영해 정사각형을 직사각형 또는 마름모의 비예로 두지 않는다.')],
    '1734465803874': [([1], '영어 원 예·비예다. 고리나 채운 원 모양 그림의 바깥 원과 그림 전체 영역을 구별한다.')],
    '1744238127311': [([1,2], '영어 목차와 빈 분류판이다.'),
                       (list(range(3,28)), '각 분류판의 두 칸을 대조했다. 인쇄 10번에 삼각형이 모여 있어 육각형 대 사다리꼴이라는 목차와 다르다.')],
    '1744239775613': [(list(range(1,28)), '1744238127311과 동일한 영어 분류판 PDF다.')],
    '1758837605205': [([1], '스페인어 원 예·비예다. 타원·각진 모양과 원의 경계를 비교한다.')],
}

IMAGE_NOTES = [
    ([*range(29),30,31,32,35,36,37,40,41,42,43,44,46,48,49,50,51,52,53,54,55,65,72,73,75,78,82,87,89],
     '교실·놀이·도형 도구 사진이다. 포개기·분류·그리기 장면은 보이는 범위만 확인했다. 48은 종이에 감긴 선, 53은 상자와 본뜬 면이다.'),
    ([29,38,71,76,77,79,80,81], '각·회전의 상황과 빨대·각도기 도구 그림이다. 빨대 길이, 서로 다른 눈금과 각 크기를 구별한다.'),
    ([33,34,47,59,61,68,70,83,84,85,86], '분류 이야기, 도형 보기와 비예, 응답 카드다. 방향과 색은 바뀔 수 있으며 실제 답은 경계와 속성을 확인한다.'),
    ([39,45,56,57,58,60,62,63,64,66,69,74,88,90,91], '책 표지·가정 자료·상자·블록·깡통 등 도구와 맥락 그림이다. 교재나 가정 안내의 전체 본문은 별도다.'),
    ([67], '깡통 밑면을 본뜬 그림 아래의 글이 원과 지름을 같은 대상으로 적는다. 원은 경계이고 지름은 중심을 지나는 선분 또는 그 길이다.'),
]

CLAIMS = [
    ('LT128',['4수03-02','4수03-03','4수03-10'],['1593028192976','1593029263564','1677859176095','1705099303904'],[],
     '분류표의 직사각형에는 네 직각, 정사각형에는 네 직각과 네 같은 변이 필요하다. 사다리꼴에서 한 옆변이 서로 평행한 두 밑변에 수직이면 직각 두 개가 생긴다.',
     '용어집의 마름모 문장이 사다리꼴에도 반복된다. 평행한 변이 정확히 한 쌍이라는 정의와 구별하며, 연꼴에서 같은 길이의 두 변은 각각 이웃한다.'),
    ('LT129',['4수03-11'],['1677859176095','1744238127311'],[],
     '정다각형은 모든 변의 길이가 같고 모든 내각의 크기도 같다. 단위 길이 여섯 개로 만든 육각형도 각이 서로 다를 수 있다.',
     '같은 길이의 변만으로 정오각형이나 정육각형이라고 판단하지 않는다. 눈으로 보이는 대칭과 정확한 각의 일치를 구별한다.'),
    ('LT130',['2수03-04','2수03-05','4수03-11'],['1686591296049','1694816631737','1701984867317'],[],
     '5보다 많은 변이라는 규칙에는 6변 도형과 8변 도형이 모두 들어간다. 삼각형을 판별할 때는 직선 세 변이 닫혀 있는지 확인한다.',
     '카드 17쪽의 팔각형은 비예에 잘못 놓였다. 27쪽의 굽은 경계는 직선 변을 전제로 한 삼각형의 예에서 제외한다.'),
    ('LT131',['4수03-08','4수03-09','4수03-25'],['1593028192976','1593028242251','1593028334885'],[33],
     '도형 가족 그림에서는 변 길이와 각 기준을 따로 적용한다. 이등변삼각형의 위 범주는 삼각형이며 부등변삼각형은 나란한 범주다.',
     '이야기의 가족 관계는 포함관계의 근거가 아니다. 적어도 두 변의 길이가 같다는 정의를 쓰면 정삼각형도 이등변삼각형이다.'),
    ('LT132',['2수03-03','4수03-06','6수03-07'],['1676058109278','1676058133384','1676058163096','1734465803874'],[48,67],
     '깡통을 본뜬 닫힌 경계는 원으로 보고 지름은 중심을 지나 양 끝이 그 원 위에 놓인 선분으로 표시한다. 감긴 한 줄과 여러 개의 원을 구별한다.',
     '자료 그림과 실제 원의 중심·길이를 구별한다. 고리의 바깥 경계가 원이어도 고리 전체 영역을 지름이라고 부르지 않는다.'),
]

OBSERVATION_DATA = [
    ('LT-P119','평행한 두 밑변의 왼쪽 끝을 수직인 옆변으로 이은 사다리꼴을 그려 직각을 모두 표시하라. 오른쪽 옆변은 기울어져 있다.',
     '왼쪽 옆변이 두 밑변에 모두 수직이므로 왼쪽 위와 왼쪽 아래가 직각이다.', '평행한 두 밑변과 직각의 개수를 따로 확인한다.'),
    ('LT-P120','변 여섯 개의 길이가 모두 같은 육각형에 크기가 다른 두 내각이 표시돼 있다. 정육각형인가? 필요한 조건을 말하라.',
     '정육각형이 되려면 변의 길이와 내각의 크기가 각각 모두 같아야 한다. 이 그림은 내각의 조건을 만족하지 않는다.', '같은 변 길이 하나와 정다각형의 두 조건을 구별한다.'),
    ('LT-P121','5보다 많은 변이 있는 다각형을 고른다. 닫힌 오각형·육각형·팔각형 중 어느 것을 골라야 하는가?',
     '육각형과 팔각형을 고른다. 5는 경계값이므로 오각형은 고르지 않는다.', '5 초과와 6이라는 한 개의 값을 구별한다.'),
    ('LT-P122','세 변의 길이가 모두 같은 삼각형과 두 변만 같은 삼각형을 분류한다. 이등변의 정의를 적어도 두 변이 같다고 하면 어느 쪽이 들어가는가?',
     '둘 다 이등변삼각형에 들어간다. 세 변이 같은 것은 정삼각형에도 들어간다.', '도형의 예와 상위 범주를 구별한다.'),
    ('LT-P123','깡통의 밑면을 본떠 그린 경계에서 원과 지름을 각각 가리켜라. 중심을 지나지 않는 두 원 위 점을 잇는 선분도 지름인가?',
     '닫힌 둥근 경계가 원이다. 원 위 두 점을 이은 선분 중 중심을 지나는 것이 지름이다.', '원 모양 전체와 지름 선분을 구별한다.'),
]

OBSERVATIONS = [dict(id=oid, standard_codes=claim[1], question=question, expected=expected,
                     interpretation=interpretation, student_validated=False)
                for claim, (oid, question, expected, interpretation) in zip(CLAIMS, OBSERVATION_DATA, strict=True)]


def verify_figures(names, raw_images):
    glossary = (CACHE / '1677859176095.txt').read_text(encoding='utf-8')
    assert 'exactly one pair of parallel sides' in glossary and glossary.count('Exactly 2 pairs of parallel lines') == 3
    assert 'regular pentagon' in glossary and 'regular hexagon' in glossary
    rules = (CACHE / '1694816631737.txt').read_text(encoding='utf-8')
    assert 'More than 5 sides' in rules and '3 sides and 3 angles' in rules
    assert raw_images[67]['url'].endswith('/1744671687326.png')
    assert {'1677859176095','1693418532317','1744238127311','1744239775613'} <= set(names)
    # Unit edges in order at 0, 60, 90, 180, 240, and 270 degrees form a nonregular hexagon.
    vectors = [(1,0),(.5,sqrt(3)/2),(0,1),(-1,0),(-.5,-sqrt(3)/2),(0,-1)]
    assert all(abs(x*x + y*y - 1) < 1e-12 for x,y in vectors)
    assert all(abs(sum(component)) < 1e-12 for component in zip(*vectors))
    turns = [60,30,90,60,30,90]
    assert sum(turns) == 360 and len(set(turns)) == 3
    return dict(more_than_five_sides=[6,8], equal_side_hexagon_turns=turns,
                right_trapezoid_vertices=[[0,0],[4,0],[2,2],[0,2]], right_angle_vertices=[1,4])


def verified_assets(raw_pdfs, raw_images):
    pdfs, images, pdf_notes = [], [], {}
    for row in raw_pdfs:
        pages = list(range(1, row['pdf_pages'] + 1))
        entries = PDF_NOTES[row['url'].rsplit('/', 1)[-1].removesuffix('.pdf')]
        assert [p for group, _ in entries for p in group] == pages
        assert row['status'] == 200 and sha(ROOT / row['file']) == row['sha256']
        assert [a['pdf_page'] for a in row['renders']] == pages
        assert all(sha(ROOT / a['file']) == a['sha256'] for a in row['renders'])
        asset = {k: row[k] for k in ('url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'pdf_pages')}
        pdfs.append(dict(asset, read_kind='linked_pdf_content_and_visual_review', redistributed=False,
                         content_read_method='visual_pages_and_available_text', content_pdf_pages=pages, visual_pdf_pages=pages,
                         rendered_pages=[{k: a[k] for k in ('pdf_page', 'sha256')} for a in row['renders']]))
        pdf_notes[row['url']] = [dict(pdf_pages=group, note=note) for group, note in entries]
    for index, row in enumerate(raw_images):
        assert row['index'] == index and row['status'] == 200 and sha(ROOT / row['file']) == row['sha256']
        asset = {k: row[k] for k in ('url', 'page_url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'dimensions')}
        images.append(dict(asset, read_kind='inline_image_visual_review', redistributed=False))
    listed = [i for group, _ in IMAGE_NOTES for i in group]
    assert sorted(listed) == list(range(len(images)))
    return pdfs, images, pdf_notes, [dict(image_urls=[images[i]['url'] for i in group], note=note) for group, note in IMAGE_NOTES]


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
    raw_pdfs, raw_images = [load(CACHE / f'{kind}-manifest.json') for kind in ('pdf', 'image')]
    assert len(raw_pdfs) == len(PDF_NOTES) == 30 and len(raw_images) == 92
    pdfs, images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images)
    assert asset_pairs(pdfs) == linked_pairs(prior['geometry_2d_pdf_urls_not_reviewed'])
    assert asset_pairs(images) == linked_pairs(prior['geometry_2d_image_urls_not_reviewed'])
    all_pdfs = prior['supplementary_pdf_read_manifest'] + pdfs
    all_images = prior['image_read_manifest'] + images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (145, 528)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (131, 472)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (865, 840)
    assert len({a['sha256'] for a in images}) == 91
    names = {a['url'].rsplit('/', 1)[-1].removesuffix('.pdf'): a['url'] for a in pdfs}
    checks = verify_figures(names, raw_images)
    pdf_hashes = {a['url']: a['sha256'] for a in pdfs}
    assert pdf_hashes[names['1677859176095']] == pdf_hashes[names['1693418532317']]
    assert pdf_hashes[names['1744238127311']] == pdf_hashes[names['1744239775613']]
    assert len(set(pdf_hashes.values())) == 28

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
                 supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
                 supplementary_pdf_coverage=dict(urls=145, page_occurrences=528, distinct_sha256_files=131,
                                                 pages_after_file_deduplication=472, all_selected_pages_visual_reviewed=True,
                                                 whole_site_attachment_review=False),
                 pdf_exact_reuse_groups=reuse_groups(all_pdfs), geometry_2d_image_exact_reuse_groups=reuse_groups(images),
                 geometry_2d_pdf_urls_not_reviewed={}, geometry_2d_image_urls_not_reviewed={},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=92, supplementary_pdf_urls=30),
                 geometry_2d_pdf_reading_log=pdf_notes, geometry_2d_image_reading_log=image_notes, geometry_2d_checked_figures=checks,
                 pdf_reading_log={**prior['pdf_reading_log'], **{
                     url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows]
                     for url, rows in pdf_notes.items()}},
                 reading_log=prior['reading_log'] + ['평면도형의 연결 PDF 30개 URL·185쪽과 삽입 이미지 92개 URL을 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='geometry_card_definitions_and_sorting_examples',
                     locations=[names[n] for n in ('1593028192976','1593028334885','1593029263564','1677859176095','1694816631737','1744238127311')] + [images[67]['url']],
                     action='도형 정의의 누락 조건, 분류표와 예시의 불일치, 원과 지름 표기를 대조했다.')],
                 unread_followups=[LIMITS, '평면도형의 인용 원연구와 다음 도형 활동 본문을 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
                  method_note='도형 카드와 용어집의 정의, 쪽별 그림, 분류의 반례를 대조했다.',
                  editorial_action='LT2 문헌 대응 5건과 관찰 과제 5개를 추가했다.', image_read_manifest=all_images,
                  supplementary_pdf_read_manifest=all_pdfs, observations=source['observations'] + OBSERVATIONS)
    for cid, codes, filenames, indices, support, limit in CLAIMS:
        registry['claims'].append(dict(id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
                                       locations=[names[name] for name in filenames] + [images[i]['url'] for i in indices],
                                       support=support, does_not_establish=limit, independent_review=False, student_validated=False,
                                       target_snapshots={'revision:' + code: digest(target_value('revision:' + code)) for code in codes}))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE])
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Reviewed 30 LT2 PDF URLs, 185 pages and 92 images; added 5 mappings and 5 observations.')


if __name__ == '__main__':
    main()

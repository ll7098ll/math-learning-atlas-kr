"""Record a bounded review of composing-number printables, figures and a linked source scan."""
import copy
from itertools import combinations

from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_composing_number_activities_review_notes.json'
PRIOR_SHA = '2c0d5003e689c604fa32fd589caa431191ca89dc347714d800c1719a377acfd0'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_composing_number_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-composing-number-assets'
SCOPE = (
    '공개 영어 HTML 627개와 활동·교사자료 본문 377개를 확인했다. 본문 447개가 남았다. '
    '합성·분해의 LT2 연결 PDF 18개·45쪽과 삽입 이미지 85개 URL을 대조했다. '
    '외부 대학 서버의 풍선 묶음 원본은 해당 10쪽을 확인했으며 LT2 사본 10쪽과 같은 렌더를 얻었다. '
    'LT2 누적 PDF 81개 URL·218쪽과 이미지 526개 URL이며, 파일 해시가 같은 것을 한 번으로 세면 PDF 73개·203쪽과 이미지 515개다.'
)
LIMITS = (
    '외부 풍선 묶음 스캔의 확인 범위는 물리 47~56쪽이다. 원본과 LT2 사본을 별개의 수학 근거로 세지 않는다. '
    '과자판 인쇄 치수, 실제 놀이의 진행과 효과, 영상·인용 연구·번역 동등성, '
    '나머지 자료의 본문과 첨부, 독립 검토·학생 응답은 후속 범위다.'
)

PDF_NOTES = {
    '1586299768091': [([1], '점 카드 0~5가 2열×5행의 틀에 들어 있다. 왼쪽 열 아래부터 채운다. 앞서 읽은 1586295352926과 같은 파일이다.')],
    '1586299815830': [([1], '점 카드 6~10은 첫 열을 다 채우고 둘째 열에 나머지를 놓는다. 앞서 읽은 1586295390727과 같은 파일이다.')],
    '1591643613581': [([1], '네 그림 모두 점 4개다. 대각선, 위·중간·아래가 섞인 배열, 네 꼭짓점 배열, 세로줄이 서로 다르다.'), ([2], '네 그림 모두 점 5개다. 개수로는 네 보기를 가를 수 없어 보았던 배치도 기억해야 한다.')],
    '1598466053309': [([1], '케이크 네 개에 초가 각각 5개다. 그림 전체는 20개다.'), ([2], '케이크 네 개에 초가 각각 6개다. 앞 쪽과 같은 네 묶음에 각각 하나씩 늘어 전체 24개다.')],
    '1618590296112': [([1], '망치 노래의 세 동작을 하는 대목 첫 줄에 망치 둘이 쓰였다. 같은 절의 반복과 손 두 개·발 한 개 동작은 셋이다. 벌 노래는 한 손의 다섯 손가락을 차례로 펼친다.'), ([2], '코끼리가 한 마리부터 다섯 마리까지 모이는 절과 마지막에 다섯 마리가 돌아오는 장면을 구별한다.')],
    '1635978176032': [([1], '스페인어 진행 안내는 짧은 행동 하나를 보이고 다음 행동을 이어 붙이는 방법을 제안한다. 순서·차례·짝의 지원을 따로 본다.'), ([2], '모두 끝내기와 승리 순서의 예를 구별한다. 교사에게 전략을 살피도록 안내하며 놀이의 수학 효과를 보고한 결과표는 아니다.')],
    '1643927250016': [([1], '과자 네 개짜리 그림 판 두 개다. 과자마다 칩을 놓을 점은 미리 그려져 있지 않다.')],
    '1647029341407': [([1, 2], '큰 과자 한 개의 흰 자리는 각각 20개와 50개다. 다른 쪽의 과자별 목표 7을 자리 수로 읽지 않는다.'), ([3, 4], '과자 네 개를 한 판 또는 두 판으로 나타냈다. 과자 위에 칩 자리는 표시하지 않았다.')],
    '1675191631369': [([1], '풍선 묶음 그림, 목표를 적는 곳, 사용한 묶음을 표시하는 곳을 색 테두리로 나눠 보여 준다.')],
    '1675191760337': [([1, 2], '인쇄 19쪽 활동지와 설명이다. 2·3·4·8 묶음이 하나씩 있다. 풍선 하나에 말은 최대 하나이고, 선택한 묶음은 모두 채운다.'), ([3, 4], '인쇄 20A에서 1·2·3·4 묶음이 하나씩 있다. 가능한 수 자체를 점수로 쓰는 방법과 가능한 목표마다 1점을 주는 방법이 있다.'), ([5, 6], '인쇄 20B에서 2와 3 묶음은 각각 두 개다. 1~10 중 1과 9는 만들 수 없다.'), ([7, 8], '인쇄 21A는 3과 5 묶음이 각각 세 개다. 24가 전체이며 1~24의 모든 수가 가능한 것은 아니다.'), ([9, 10], '인쇄 21B는 3과 4 묶음이 각각 세 개다. 21이 전체다. 앞 활동지와 묶음의 종류와 가능한 합이 다르다.')],
    '1675191846306': [([1], '인쇄 19쪽 예에서 목표 1을 만들 수 없다고 표시하는 부분을 보여 준다. 다른 묶음 판에는 그대로 적용하지 않는다.')],
    '1675191876864': [([1], '목표 2·3·4를 각 크기의 한 묶음으로 만들고 해당 칸을 표시한다.')],
    '1675191912463': [([1], '5는 2와 3, 6은 2와 4, 7은 3과 4의 묶음을 표시한다. 부분 묶음은 쓰지 않는다.')],
    '1676653418517': [([1, 2], '수 카드 0~5와 6~10이다. 10 짝 놀이 본문의 1~9 카드 범위보다 넓다. 앞서 읽은 1676655464842와 같은 파일이다.')],
    '1690825669835': [([1, 2, 3, 4], '1센트 동전 1~4개를 그린 카드가 이어진다. 한 장에 그린 동전 수와 카드 장수를 구별한다.'), ([5, 6, 7], '여러 1센트 동전 그림과 단일 5센트 동전 그림이 섞여 있다. 5센트 동전은 세 쪽에 두 장씩이다.'), ([8, 9], '8·9센트에 해당하는 여러 동전 그림과 단일 10센트 동전 카드가 있다. 9쪽 저금통 그림은 점수 카드가 아니다.')],
    '1690827009213': [([1], '해양 생물 두 종류의 수를 적는 칸과 빈 2×5 틀 하나다. 본문의 빈 틀 11개를 준비하려면 이 파일 한 장을 그대로 쓰는 것으로는 부족하다.')],
    '1694619108388': [([1], '영어 단계 그림의 목표 카드는 2이고 주사위 예는 3이다. 접시에 가져오는 수와 과자 한 개의 목표가 다르다.'), ([2], '짝이 확인한 뒤 말 3개를 과자 두 곳에 2개와 1개로 나눠 놓는다. 한 과자에 2개를 넘기지 않는다.')],
    '1696882039265': [([1], '스페인어 단계 그림에서도 목표 2와 가져오는 3이 구별된다. 교사용 설명과 그림 자료의 역할을 나눠 기록한다.'), ([2], '짝 확인, 2와 1로 나누어 놓기, 역할 바꾸기의 그림을 확인했다. 이 비교는 두 언어 자료의 전체 번역 검증과 구별한다.')],
}

IMAGE_NOTES = [
    ([0, 1, 2, 8, 30, 31, 39, 59, 63], '손가락·손 모양·토끼 귀 예시다. 편 손가락과 손가락이 속한 손, 보조 도구를 구별한다. 동작 사진은 수 설명을 한 기록으로 처리하지 않는다.'),
    ([16, 33, 34, 83], '묶음·낱개, 십의 자리 계산 예, 수 표 일부의 자료다. 83의 예시 그림에 보이는 탑은 각 6칸이고 따로 그린 낱개는 3개다. 실제 활동 지시의 열 개짜리 탑을 준비할 때는 따로 센다.'),
    ([22, 41, 42, 44, 45, 51, 70], '숫자 카드와 보수의 그림이다. 22는 11 카드까지 보이며 활동의 기본 1~10 범위와 다르다. 51은 7+3, 70은 6+4의 목표 10 예다.'),
    ([26, 32, 36, 37, 38, 67, 68, 69], '케이크와 과자 및 준비물 그림이다. 36·37은 같은 사진이며 네 과자에 점이 두 개씩 놓였다. 목표 7 카드는 놓인 점의 수와 다르다.'),
    ([29, 40, 47, 48, 49, 50, 52, 53, 54, 60, 61, 80], '점 배열·풍선 묶음·구슬·저금통·색 칩의 예다. 보이는 부분, 표시한 전체, 준비 재료의 수를 구별한다. 48은 전체 10 중 4가 가려졌음을 명시한다.'),
    ([43, 46, 55, 56, 58, 62, 71, 72, 74, 75, 76, 81, 82, 84], '교사 지원, 장난감·자연물과 준비 도구의 그림이다. 삽입 유형표는 이미 대조한 설명과 같은 범위이며 독립된 사례로 더하지 않는다.'),
]

CLAIMS = [
    ('LT69', ['2수01-04', '2수01-08', '2수01-09'], ['1675191760337', '1675191631369'], [40],
     '풍선 묶음은 하나를 고르면 묶음 전부를 쓰고 풍선마다 말을 최대 하나 놓는다. 인쇄 19쪽의 2·3·4·8 묶음은 1과 16을 만들 수 없다. 다른 판에서 같은 크기의 묶음이 여러 개면 가능한 합이 달라진다.',
     '외부 스캔 47~56쪽과 LT2 사본의 해당 렌더는 같다. 두 파일을 독립 근거로 세지 않으며, 범위 밖이나 다른 묶음의 가능성을 이 판으로 판단하지 않는다.'),
    ('LT70', ['2수01-04', '2수01-05', '2수01-08'], ['1690825669835', '1676653418517'], [41, 45, 53, 54],
     '저금통 카드에서 카드 장수와 그림 속 동전 수, 액면 합을 따로 셀 수 있다. 같은 10센트도 동전 한 개, 두 개, 여러 개를 그린 카드 조합으로 나타낼 수 있다. 0~10 인쇄 카드와 1~9 사용 조건도 구별한다.',
     '인쇄된 모든 카드를 목표 5 놀이에 그대로 쓰거나 저금통 그림까지 점수로 세지 않는다. 외국 화폐의 액면은 자료를 읽는 조건이며 국내 필수 내용으로 확대하지 않는다.'),
    ('LT71', ['2수01-04', '2수01-05', '2수01-06', '2수01-10'], ['1643927250016', '1647029341407', '1694619108388', '1696882039265', '1690827009213'], [36, 38, 52],
     '과자 한 개의 목표와 놀이판에 인쇄된 자리 수를 구별한다. 단계 예는 가져온 말 3개를 목표 2인 과자 두 곳에 2개와 1개로 나눈다. 과자 네 개의 전체 필요량은 과자마다 정한 목표를 합한다.',
     '큰 과자의 인쇄 자리 20·50은 별도 그림의 수다. 그림의 용량만으로 게임 중 놓아야 할 양이나 목표를 넘겼을 때의 실제 처리 규칙을 정하지 않는다.'),
    ('LT72', ['2수01-01', '2수01-02', '2수01-04'], ['1586299768091', '1586299815830', '1591643613581'], [29, 48, 83],
     '점의 개수와 배열이 같은지 따로 확인한다. 같은 개수의 점을 다른 모양으로 놓을 수 있고, 틀에서 5개를 한 열로 보아 나머지를 셀 수 있다. 탑의 크기를 셈의 단위로 쓸 때는 실제 묶음 크기를 확인한다.',
     '같은 개수의 보기 중 원래 배치를 골랐다는 응답을 개수 세기와 동일하게 기록하지 않는다. 삽입된 일반 그림의 탑이 활동 지시의 십 묶음을 뜻한다고 가정하지 않는다.'),
    ('LT73', ['2수01-01', '2수01-10', '2수01-11'], ['1598466053309', '1618590296112'], [26, 32],
     '케이크 그림은 네 묶음의 크기가 5에서 6으로 바뀌는 예를 보여 준다. 노래에서 수 말과 세는 동작이 어긋나면 무엇을 몇 번 세는지 확인한다.',
     '인쇄된 가사에 수 표기가 섞인 대목과 반복으로 주어진 규칙을 구별한다. 노래의 동작을 따라 했다는 사실로 합이나 곱을 이해했다고 판단하지 않는다.'),
]

OBSERVATIONS = [
    dict(id='LT-P61', standard_codes=['2수01-04', '2수01-08', '2수01-09'],
         question='2개, 3개, 4개, 8개짜리 풍선 묶음이 한 개씩 있다. 한 묶음을 쓰려면 그 묶음의 풍선을 전부 채운다. 15개, 16개, 17개를 각각 채울 수 있는지 찾아라. 16개가 어렵다면 묶음의 한 부분만 채웠을 때와 어떤 차이가 있는가?',
         expected='15는 3+4+8이고 17은 네 묶음을 전부 쓰면 된다. 전체 17에서 16을 만들려면 1개를 빼야 하는데 1개 묶음은 없다. 일부만 채워도 된다면 모든 묶음 중 풍선 하나만 비워 16이 된다.',
         interpretation='여러 합을 시도한 뒤 불가능한 경우의 근거를 설명하게 한다. 전체에서 제외한 양과 묶음을 쪼갤 수 있는지의 조건을 따로 확인한다.', student_validated=False),
    dict(id='LT-P62', standard_codes=['2수01-04', '2수01-05', '2수01-08'],
         question='가에는 10점 동전 그림 한 개가 그려진 카드 한 장, 나에는 5점 동전 그림 한 개가 그려진 카드 두 장이 있다. 다에는 1점 동전 그림을 7개 그린 카드 한 장과 3개 그린 카드 한 장이 있다. 각 경우 카드 장수, 동전 그림 수, 총점을 각각 말하라.',
         expected='가는 카드 1장·동전 그림 1개·10점이다. 나는 2장·2개·10점이고, 다는 2장·10개·10점이다. 카드 두 장이라고 동전 그림이 두 개라는 뜻은 아니다.',
         interpretation='카드, 그림 속 물건, 총점을 각각 단위와 함께 말하게 한다. 별도 화폐 지식 없이 그림마다 정해 준 점수로 답할 수 있다.', student_validated=False),
    dict(id='LT-P63', standard_codes=['2수01-06', '2수01-10'],
         question='과자 네 개에 칩을 7개씩 놓으려 한다. 준비판의 표시된 자리에 한 칸당 칩 한 개를 놓는다. 준비판 가는 20자리, 나는 50자리다. 어느 판에 필요한 칩을 모두 놓을 수 있는가? 각 판에서는 몇 자리가 모자라거나 남는가?',
         expected='7개씩 네 묶음이므로 28개가 필요하다. 가는 8자리가 모자라며, 나는 모두 놓고 22자리가 남는다.',
         interpretation='이 과제에서는 준비판에 먼저 놓는 조건을 명시한다. 과자 한 개의 목표 7, 필요한 전체 28, 준비판의 전체와 빈 자리를 따로 답하는지 살핀다.', student_validated=False),
    dict(id='LT-P64', standard_codes=['2수01-01', '2수01-04'],
         question='한 카드에는 점 네 개가 네모의 꼭짓점에 있고, 다른 카드에는 점 네 개가 세로 한 줄에 있다. 처음 잠깐 본 카드가 네모 배열이었다면 두 카드의 점 개수와 처음 본 카드의 모양을 각각 말하라. 점 개수만 기억했다면 처음 본 카드를 고를 수 있는가?',
         expected='두 카드의 점은 모두 네 개다. 처음 본 카드는 네모 배열이다. 점 개수만으로는 두 후보 중 하나를 정할 수 없다.',
         interpretation='개수를 보고한 답과 점이 어디에 있었는지 설명한 답을 별도로 기록한다. 두 배열을 같은 네 개로 설명하는 전략을 확인할 수 있다.', student_validated=False),
]


def verify_external(pdfs):
    external = load(CACHE / 'external-balloons-preliminary-review.json')
    access = external['access']
    assert sha(ROOT / access['file']) == access['sha256'] and access['pdf_pages'] == 655
    pages = external['fully_read_target_physical_pages']
    assert pages == list(range(47, 57))
    copy_asset = next(asset for asset in pdfs if asset['url'].endswith('/1675191760337.pdf'))
    matches = []
    for page, render in zip(pages, copy_asset['rendered_pages']):
        assert sha(CACHE / f'cda-balloons-{page:03}.png') == external['render_sha256'][str(page)]
        assert render['pdf_page'] == page - 46
        assert sha(CACHE / f'cda-match-{page:03}.png') == render['sha256']
        matches.append(dict(original_pdf_page=page, copy_pdf_page=render['pdf_page'], identical_render_sha256=render['sha256']))
    for board in external['checks']:
        values = board['group_sizes']
        possible = {sum(chosen) for size in range(len(values) + 1) for chosen in combinations(values, size)}
        assert sorted(set(range(1, sum(values) + 1)) - possible) == board['unreachable_positive_targets']
    return dict(url=access['url'], final_url=access['final_url'], status=200, sha256=access['sha256'],
                content_type=access['content_type'], linked_page_urls=access['linked_page_urls'], pdf_pages=access['pdf_pages'],
                content_pdf_pages=pages, visual_pdf_pages=pages, linked_copy_url=copy_asset['url'],
                rendered_page_matches=matches, scan_render_sha256=external['render_sha256'],
                rendered_long_edge_pixels=1600, board_checks=external['checks'], redistributed=False,
                read_scope='인쇄 19·20A·20B·21A·21B의 학생용 판과 다음 교사 안내만 확인했다. 20A는 같은 목표를 반복할 수 있는지를 명시하지 않으므로 점수 최댓값을 단일 값으로 등록하지 않는다.')


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
    for i, row in enumerate(raw_images):
        assert row['index'] == i and row['status'] == 200 and sha(ROOT / row['file']) == row['sha256']
        asset = {k: row[k] for k in ('url', 'page_url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'dimensions')}
        images.append(dict(asset, read_kind='inline_image_visual_review', redistributed=False))
    listed = [i for group, _ in IMAGE_NOTES for i in group]
    assert len(listed) == len(set(listed)) and set(listed) <= set(range(len(images)))
    others = sorted(set(range(len(images))) - set(listed))
    groups = IMAGE_NOTES + [(others, '놀이·수업·물건·자리의 사진과 예시다. 장면만으로 아이의 답, 교사의 도움이나 놀이 결과를 판단하지 않는다.')]
    return pdfs, images, pdf_notes, [dict(image_urls=[images[i]['url'] for i in group], note=note) for group, note in groups]


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
    assert len(raw_pdfs) == len(PDF_NOTES) == 18 and len(raw_images) == 85
    pdfs, images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images)
    external = verify_external(pdfs)
    assert asset_pairs(pdfs + [external]) == linked_pairs(prior['composing_number_pdf_urls_not_reviewed'])
    assert asset_pairs(images) == linked_pairs(prior['composing_number_image_urls_not_reviewed'])
    all_pdfs = prior['supplementary_pdf_read_manifest'] + pdfs
    all_images = prior['image_read_manifest'] + images
    unique_pdfs = {asset['sha256']: asset['pdf_pages'] for asset in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (81, 218)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (73, 203)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (526, 515)
    assert 4 * 7 == 28 and 28 - 20 == 8 and 50 - 28 == 22
    names = {a['url'].rsplit('/', 1)[-1].removesuffix('.pdf'): a['url'] for a in pdfs}
    coin_inventory = [7, 6, 6, 7, 6, 2, 2, 2, 2]
    assert sum(coin_inventory) + 6 + 2 == 48 and sum(coin_inventory[:4]) + 2 + 2 == 30

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
                 supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
                 supplementary_pdf_coverage=dict(urls=81, page_occurrences=218, distinct_sha256_files=73,
                                                 pages_after_file_deduplication=203, all_selected_pages_visual_reviewed=True,
                                                 whole_site_attachment_review=False),
                 pdf_exact_reuse_groups=reuse_groups(all_pdfs), composing_number_image_exact_reuse_groups=reuse_groups(images),
                 composing_number_pdf_urls_not_reviewed={}, composing_number_image_urls_not_reviewed={},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=85, supplementary_pdf_urls=18),
                 composing_number_pdf_reading_log=pdf_notes, composing_number_image_reading_log=image_notes,
                 composing_number_external_pdf_review=external,
                 composing_number_piggy_bank_card_check=dict(url=names['1690825669835'], penny_card_counts_by_number=coin_inventory,
                                                            nickel_cards=6, dime_cards=2, value_cards=48, level_five_card_count_in_body=30),
                 pdf_reading_log={**prior['pdf_reading_log'], **{
                     url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows]
                     for url, rows in pdf_notes.items()}},
                 reading_log=prior['reading_log'] + ['수의 합성·분해 연결 LT2 PDF 18개·45쪽과 삽입 이미지 85개 URL을 대조했다. 외부 원본의 물리 47~56쪽은 LT2 사본과 렌더가 일치했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='composition_printable_scope_and_rules', locations=[names[n] for n in ('1675191760337', '1690825669835', '1647029341407', '1591643613581', '1618590296112')],
                     action='풍선판별 가능한 합, 카드 장수와 액면, 칩 자리와 목표, 점 개수와 배치, 노래의 수 표기와 동작을 구별했다.')],
                 unread_followups=[LIMITS, '수량 비교·순서 활동의 본문을 우선 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
                  method_note='LT2 PDF 45쪽과 삽입 이미지 85개를 시각 대조했다. 외부 풍선 자료 10쪽을 읽고 LT2 사본의 렌더와 해시를 비교했다.',
                  editorial_action='문헌 대응 5건과 관찰 과제 4개를 추가했다.', image_read_manifest=all_images,
                  supplementary_pdf_read_manifest=all_pdfs, observations=source['observations'] + OBSERVATIONS)
    for cid, codes, filenames, indices, support, limit in CLAIMS:
        locations = [names[name] for name in filenames] + [images[i]['url'] for i in indices]
        if cid == 'LT69':
            locations.append(external['final_url'] + '#page=47')
        registry['claims'].append(dict(id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
                                       locations=locations, support=support, does_not_establish=limit, independent_review=False,
                                       student_validated=False, target_snapshots={'revision:' + code: digest(target_value('revision:' + code)) for code in codes}))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE])
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Reviewed 18 LT2 PDFs, 45 pages, 85 images and the matched 10-page external excerpt; added 5 mappings and 4 observation tasks.')


if __name__ == '__main__':
    main()

"""Record a bounded review of LT2 length PDFs and inline figures."""
import copy
import hashlib
import json
from collections import defaultdict
from math import isclose

from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR_NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_length_activities_review_notes.json'
PRIOR_SHA = '485e64372538d9e8471f84c6bc734dab0840e0b3c905ba8ee2e994f5bbfaff9c'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_length_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-length-assets'

SCOPE = (
    '공식 공개 영어 HTML 405개를 대조했다. 일반 6·영역 개요 20·수준 224·활동 153·교사자료 2개다. '
    '기록된 활동/교사자료 824개 중 공개 본문 155개를 읽었고 669개가 남았다. '
    '길이 페이지에서 추가로 삽입 이미지 93개 URL과 첨부 PDF 8개 URL의 10쪽을 대조했다. '
    '누적 삽입 이미지는 203개 URL·200개 고유 파일 해시, 누적 첨부 PDF는 24개 URL·29쪽이다. '
    '같은 PDF 파일을 한 번씩 세면 21개 파일·26쪽이다.'
)
LIMITS = (
    '페이지에 삽입된 철도 지도·조각·띠, 굽은 길, 타일, 가정 안내와 어휘 자료는 보이는 범위에서 확인했다. '
    '별도 배포본·실물 인쇄 배율과 조각 맞춤, 야드 안내, 영상·책 본문·인용 원연구, 669개 미검토 본문과 '
    '외부 매뉴얼 전체, 독립 검토·학생 응답 검증은 후속 범위다.'
)

PDF_NOTES = {
    '1574711908549.pdf': [
        'Clifford 지도는 10×7.5인치 PDF다. 표시된 도로 선분 중심의 끝을 기준으로 Ben 쪽 약 7인치, Jerry 쪽 약 6인치다. 건물 그림의 테두리와 실제 도로 거리는 별개다.',
    ],
    '1574713542905.pdf': [
        '두 도로 지도는 7.5×10인치 PDF다. 학교 쪽에 모이는 Alex 선분은 약 5인치, Maria 선분은 약 6인치다. 두 선에 동일한 비율을 적용하면 길이 순서는 유지되며 절대 인쇄 길이는 별도로 확인한다.',
    ],
    '1574715227424.pdf': [
        '택시 지도의 두 경로는 표시된 공통 시작점과 끝점을 잇는다. 회색 선분 2개 합은 약 12.00000인치, 검은 선분 10개 합은 약 11.98919인치다. 선분 중심의 길이를 따로 합산한 결과로 약 0.27mm 차이다. 도면의 미세한 어긋남·틈과 이상적인 연속 직각 경로의 등길이를 구별한다.',
    ],
    '1580229855250.pdf': [
        '파란 A 도면 외곽 격자는 가로 10칸·세로 7칸이다. 본문의 파란 9단위 예가 외곽 전체의 칸 수는 아니다. 본문 예에 해당하는 지정 끝점 표시는 찾지 못했다.',
        '초록 B 도면 외곽 격자는 가로 20칸·세로 14칸이다. A와 용지 크기는 같고 격자 외곽 치수는 비슷하다. 본문의 초록 18단위와 외곽 전체 20칸을 구별한다. 한 방향 간격 수와 전체 격자 칸 넓이는 서로 다른 양이다.',
    ],
    '1611676643614.pdf': [
        '크기가 차례로 달라지는 파란 정사각형 응답 카드 세 개다. 실제 장난감 길이의 측정값이나 선택 결과를 제공하지 않는다. 사진 속 크기와 실물 크기를 비교할 때 촬영 조건과 공통 기준을 확인한다.',
    ],
    '1632507899806.pdf': [
        '첫 쪽은 여섯 칸의 사회적 이야기 틀이다. 참여 장면과 관점, 행동과 응답을 제시할 공간을 둔다.',
        '둘째 쪽은 놀이와 쌓기, 돌봄, 감정, 공간, 정리를 다루는 여섯 장면의 예다. 참여 지원에 활용할 수 있으며 길이 측정의 수행이나 효과를 보여 주는 자료는 아니다.',
    ],
    '1664923800264.pdf': [
        '도움 요정 영어판에는 바닥과 벽 설명이 섞여 있다. 5~8인치 틈, 1인치 도구, 늘어나지 않는 테이프, 끈/두꺼운 종이 대안, 다시 맞춰 보는 절차를 확인했다. 이 자료에는 틈 길이가 인치의 정수배라는 조건이 없다. 정확히 맞지 않을 때 남는 길이를 처리해야 한다.',
    ],
    '1664923831603.pdf': [
        '스페인어 표기 자료도 바닥과 벽 설명이 섞여 있다. 길이를 묻는 대목에 시간 표현인 «cuánto tiempo»가 있고, 도구를 나누어 주는 주요 절차 문단은 영어로 남아 있다. 완전한 번역이나 등가 과제로 등록하지 않는다.',
    ],
}

IMAGE_NOTES = [
    ([2, 3, 11, 26], '지도/도면 미리보기. 11번은 다른 도로 쪽 표기가 일부 잘려 있으며, 원본 도면과 별도로 인쇄 치수를 확인한다.'),
    ([4, 37], '측정 어휘 그림과 가정 활동 포스터의 보이는 범위다. 크기·온도·무게·속도 등 다른 속성이 포함되며 배포 자료 전체를 확인한 것으로 세지 않는다.'),
    ([29, 70], '같은 블록의 계단 배열 그림이다. 1~5 배열과 1~10~1 배열이 보인다. 되돌아오는 배열의 높이와 위치를 구별한다.'),
    ([33], '해적 줄 그림 표에는 보라 8·빨강 16·갈색 4가 보인다. 단위 관계 식 오른쪽 일부는 잘려 있으며 색 자체가 길이를 보장하지 않는다.'),
    ([39], '도서관 그림의 초록 칸은 위부터 1·3·2·1개로 총 7개다. 본문의 타일 6개 지시와 다른 예다. 같은 정사각형으로 보면 공유변 7개, 바깥 둘레 14단위, 넓이 7제곱단위다.'),
    ([57, 58, 59, 60, 61], '철도 지도에는 11×14인치 및 8.5×11인치 표기가 보인다. 58번은 길이가 다른 직선 선로 6개 그림, 60번은 막대와 자 사진, 61번은 자를 수 있는 띠 그림이다. 화면 파일에서 인쇄 실측값이나 지도와 조각의 맞음을 확정하지 않는다.'),
    ([75, 86, 87], '자전거길 지도, 시작/끝을 표시한 굽은 길, 정사각형 타일 인쇄물의 그림이다. 지도 전체 인쇄와 실제 치수, 곡선 길이의 측정 방법은 별도로 확인한다.'),
    ([90, 91, 92], '팔과 물건을 비교하는 그림의 약 13인치·15인치 이상 표기는 활동 예시다. 지정 끝과 실제 길이를 확인하며 신체 규준이나 13.4인치와 25cm 병기의 근거로 사용하지 않는다.'),
    ([38, 44, 50, 64, 81, 89], '그림책 표지 또는 표지 모음이다. 본문, 실물 크기 인쇄와 실제 동물 크기는 별도다.'),
    ([8, 19, 42, 51, 52, 53, 54, 55, 56, 63, 65, 66, 67, 68, 69, 76, 77, 79, 80, 82, 83, 84, 88], '재료·도구·배치 예시 그림이다. 숫자가 붙은 준비 수량과 그림 속 수를 구별하고 사진에 나타난 길이를 실제 치수로 읽지 않는다.'),
    ([0, 1, 5, 6, 7, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 27, 28, 30, 31, 32, 34, 35, 36, 40, 41, 43, 45, 46, 47, 48, 49, 62, 71, 72, 73, 74, 78, 85], '수업·놀이·일상 장면 또는 소개 사진이다. 도움 여부, 대상의 길이, 학생의 설명과 독립 수행을 사진만으로 판정하지 않는다.'),
]

OBSERVATIONS = [
    dict(
        id='LT-P41', standard_codes=['2수03-10', '2수03-12'],
        question='A 띠는 길이 16cm를 같은 간격 4개로, B 띠는 길이 16cm를 같은 간격 8개로 나눴다. B를 가로 길이가 절반이 되도록 복사했다. 복사본의 칸 수와 실물 길이는 각각 얼마인가? 처음 B에서 한 칸과 같은 길이로 잘라 둔 2cm 조각을 복사본에 빈틈 없이 놓으면 몇 개가 필요한가?',
        expected='A와 처음 B는 길이가 같고, 한 칸은 각각 4cm와 2cm다. 복사본은 여전히 8칸이지만 한 칸이 1cm여서 전체 길이는 8cm다. 길이를 바꾸지 않은 2cm 조각은 4개가 필요하다. 복사본의 눈금 사이를 재거나 2cm 조각을 놓아 확인한다.',
        interpretation='복사 전후의 칸 수, 칸 한 개의 실제 길이, 복사와 무관하게 고정한 도구를 각각 관찰한다. 비율 계산을 저학년의 필수로 삼지 않고 절반 크기로 준비한 띠를 제공할 수 있다. 실제 교실에서는 먼저 출력물을 재어 준비 조건을 확인한다.',
        student_validated=False,
    ),
    dict(
        id='LT-P42', standard_codes=['2수03-10', '2수03-13'],
        question='움직일 수 없는 두 표시 사이의 길이를 2cm 조각으로 잰다. 왼쪽 끝에서 빈틈 없이 다섯 번 놓으니 오른쪽 끝까지 1cm가 남았다. 2cm 조각을 여섯 번 놓으면 정확히 맞는가? 같은 길이의 띠를 다른 자리에서 만들어 가져오려면 남는 부분을 어떻게 처리하고 확인할까?',
        expected='다섯 조각은 10cm이고 남은 1cm를 합하면 11cm다. 여섯 조각은 12cm라서 1cm 넘친다. 2cm 다섯 개와 길이가 확인된 1cm 한 개를 잇거나, 늘어나지 않는 띠에 두 끝을 표시해 옮긴다. 가져온 띠를 같은 두 끝에 다시 맞춰 본다.',
        interpretation='주어진 2cm 조각의 반복과 1cm 보조 단위를 섞어 쓸 때 각 길이를 명시한다. 단위로 다 채울 수 없는 조건을 끝 맞춤 오류와 구별하고, 최초 예상·나머지 설명·도움 후 수정·실물 확인을 따로 기록한다.',
        student_validated=False,
    ),
]


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def linked_pairs(by_page):
    return {(url, page) for page, urls in by_page.items() for url in urls}


def asset_pairs(assets):
    return {(asset['url'], page) for asset in assets for page in asset['linked_page_urls']}


def reuse_groups(assets):
    groups = defaultdict(list)
    for asset in assets:
        groups[asset['sha256']].append(asset['url'])
    return [dict(sha256=key, urls=urls) for key, urls in groups.items() if len(urls) > 1]


def review_pdfs(raw):
    assets = []
    logs = {}
    layouts = {}
    for item in raw:
        url = item['url']
        pages = list(range(1, item['pdf_pages'] + 1))
        name = url.rsplit('/', 1)[-1]
        assert item['status'] == 200 and sha(ROOT / item['file']) == item['sha256']
        assert len(PDF_NOTES[name]) == len(pages)
        assert [r['pdf_page'] for r in item['renders']] == pages
        for render in item['renders']:
            assert sha(ROOT / render['file']) == render['sha256']
        asset = {k: item[k] for k in ('url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'pdf_pages')}
        asset.update(
            read_kind='linked_pdf_content_and_visual_review', redistributed=False,
            content_read_method='page_visual_review_with_available_text',
            content_pdf_pages=pages, visual_pdf_pages=pages,
            rendered_pages=[dict(pdf_page=r['pdf_page'], sha256=r['sha256']) for r in item['renders']],
        )
        assets.append(asset)
        logs[url] = [f'{page}쪽. {note}' for page, note in zip(pages, PDF_NOTES[name])]
        layouts[url] = item['page_geometry']
    return assets, logs, layouts


def review_images(raw):
    assets = []
    for index, item in enumerate(raw):
        assert item['index'] == index and item['status'] == 200
        assert item['page_url'] in item['linked_page_urls']
        assert sha(ROOT / item['file']) == item['sha256']
        asset = {k: item[k] for k in ('url', 'page_url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'dimensions')}
        assets.append(dict(asset, read_kind='inline_image_visual_review', redistributed=False))
    indices = sorted(index for group, _ in IMAGE_NOTES for index in group)
    assert indices == list(range(len(raw)))
    logs = [dict(image_urls=[assets[i]['url'] for i in group], note=note) for group, note in IMAGE_NOTES]
    return assets, logs


def check_geometry():
    raw = load(CACHE / 'map-geometry.json')
    routes = [[s['inches'] for s in raw[key]] for key in ('1574711908549', '1574713542905', '1574715227424')]
    clifford, road, taxi = routes
    assert [round(x) for x in clifford] == [7, 6] and [round(x) for x in road] == [5, 6]
    assert len(taxi) == 12
    gray, black = sum(taxi[:2]), sum(taxi[2:])
    difference = abs(gray - black) * 25.4
    assert isclose(gray, 12, abs_tol=0.00001) and round(black, 5) == 11.98919
    assert round(difference, 2) == 0.27
    cells = {(0, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (0, 3)}
    shared = sum((x + 1, y) in cells for x, y in cells) + sum((x, y + 1) in cells for x, y in cells)
    assert len(cells) == shared == 7 and 4 * len(cells) - 2 * shared == 14
    assert 16 // 4 == 4 and 16 // 8 == 2 and (16 // 2) // 8 == 1 and (16 // 2) // 2 == 4
    assert divmod(11, 2) == (5, 1) and 6 * 2 == 12
    return dict(
        method='PDF 벡터의 좌표 변환을 적용해 도로 선분 중심의 양 끝 간 거리를 합산했다.',
        clifford_road_inches=clifford, shorter_road_inches=road,
        taxi_gray_segment_inches=taxi[:2], taxi_black_segment_inches=taxi[2:],
        taxi_gray_sum_inches=gray, taxi_black_sum_inches=black,
        taxi_difference_mm=difference, physical_print_measured=False,
    )


def new_claims(pdfs, images):
    pdf_urls = {a['url'].rsplit('/', 1)[-1]: a['url'] for a in pdfs}
    specs = [
        (
            'LT42', ['2수03-10', '2수03-12', '2수03-13'],
            [pdf_urls[name] for name in ('1574711908549.pdf', '1574713542905.pdf', '1574715227424.pdf', '1580229855250.pdf')],
            '길이 도면에서 선분 끝점, 격자 간격 수, 고정된 측정 단위와 인쇄 배율을 구별한다. 같은 끝점을 잇고 되돌아감이 없는 이상적 직각 경로의 길이는 같다. 택시 도면의 실제 두 선분 합은 약 0.27mm 차이다.',
            '그림의 외곽 칸 수를 지정 선분의 단위 수로 사용하려면 끝을 확인해야 한다. 도면으로 실물 인쇄 치수, 실제 거리, 요금 또는 학생 수행을 확정하지 않는다.',
        ),
        (
            'LT43', ['2수03-10', '2수03-13'],
            [pdf_urls[name] for name in ('1664923800264.pdf', '1664923831603.pdf')],
            '고정한 두 끝 사이를 동일한 단위로 재고 남은 길이를 따로 표시한다. 늘어나지 않는 도구로 옮긴 뒤 원래 두 끝에 맞춰 확인한다. 두 언어 자료에는 위치 설명의 불일치가 있으며 스페인어 자료에 시간 표현과 영어 절차가 남아 있다.',
            '첨부에는 정수배 길이 조건이 없으므로 정수 단위 개수만으로 항상 정확히 맞는다고 하지 않는다. 두 자료의 번역 동등성이나 수업 효과는 확인하지 않았다.',
        ),
        (
            'LT44', ['2수03-06', '6수03-11', '6수03-13'],
            [pdf_urls[name] for name in ('1611676643614.pdf', '1632507899806.pdf')]
            + [images[39]['page_url'], images[39]['url']],
            '선택 카드와 사회적 이야기의 역할을 실제 측정과 구별한다. 도서관의 본문 지시는 정사각형 6개이고 그림은 7개다. 같은 단위 타일로 본 그림의 넓이는 7제곱단위, 바깥 둘레는 14단위다.',
            '카드, 사진, 참여 지원 예시를 학생의 측정 결과로 사용하지 않는다. 7개 그림의 둘레를 6개 활동의 답으로 옮기지 않는다.',
        ),
    ]
    return [dict(
        id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
        locations=locations, support=support, does_not_establish=limit,
        target_snapshots={'revision:' + code: digest(target_value('revision:' + code)) for code in codes},
        independent_review=False, student_validated=False,
    ) for cid, codes, locations, support, limit in specs]


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        assert {'LT42', 'LT43', 'LT44'} <= {c['id'] for c in registry['claims']}
        assert [o['id'] for o in source['observations'][-2:]] == ['LT-P41', 'LT-P42']
        build_report()
        return
    assert source['snapshot_file'] == PRIOR_NOTES and sha(ROOT / PRIOR_NOTES) == PRIOR_SHA
    previous = load(ROOT / PRIOR_NOTES)
    raw_pdfs = load(CACHE / 'pdf-manifest.json')
    raw_images = load(CACHE / 'image-manifest.json')
    assert len(raw_pdfs) == 8 and len(raw_images) == 93
    assert asset_pairs(raw_pdfs) == linked_pairs(previous['linked_length_attachments_not_read'])
    assert asset_pairs(raw_images) == linked_pairs(previous['linked_length_inline_images_not_reviewed'])
    pdfs, pdf_logs, layouts = review_pdfs(raw_pdfs)
    images, image_logs = review_images(raw_images)
    geometry = check_geometry()

    all_pdfs = previous['supplementary_pdf_read_manifest'] + pdfs
    all_images = previous['image_read_manifest'] + images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert len(all_pdfs) == 24 and sum(a['pdf_pages'] for a in all_pdfs) == 29
    assert len(unique_pdfs) == 21 and sum(unique_pdfs.values()) == 26
    assert len(all_images) == 203 and len({a['sha256'] for a in all_images}) == 200
    claims = new_claims(pdfs, images)
    all_claims = [c for c in registry['claims'] if c['source_id'] == SOURCE] + claims
    assert len(all_claims) == 44 and len({code for c in all_claims for code in c['standard_codes']}) == 48
    assert len(source['observations']) == 40

    sources_path = ROOT / 'data/sources.json'
    bibliography = load(sources_path)
    entry = next(v for v in bibliography if v['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(previous)
    notes.update(
        date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source),
        previous_bibliography=previous_entry, previous_notes_file=PRIOR_NOTES, previous_notes_sha256=PRIOR_SHA,
        new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=93, supplementary_pdf_urls=8),
        image_read_manifest=all_images, supplementary_pdf_read_manifest=all_pdfs,
        pdf_reading_log={**previous['pdf_reading_log'], **pdf_logs},
        supplementary_pdf_coverage=dict(
            urls=24, page_occurrences=29, distinct_sha256_files=21, pages_after_file_deduplication=26,
            all_selected_pages_visual_reviewed=True, whole_site_attachment_review=False,
        ),
        pdf_exact_reuse_groups=reuse_groups(all_pdfs),
        linked_length_attachments_not_read={}, linked_length_inline_images_not_reviewed={},
        length_attachment_page_layouts=layouts, length_image_reading_log=image_logs,
        length_image_exact_reuse_groups=reuse_groups(images), length_map_geometry=geometry,
        reading_log=previous['reading_log'] + [
            '길이 페이지의 연결 PDF 8개 URL에 있는 10쪽과 삽입 이미지 93개 URL을 확인했다. 도면과 참여 지원 자료를 구분하고 실제 인쇄 측정은 별도로 남겼다.',
        ],
        source_corrections=previous['source_corrections'] + [dict(
            kind='length_asset_and_body_discrepancies', locations=[a['url'] for a in pdfs] + [images[39]['url']],
            action='택시 도면의 실제 선분 합과 이상적인 등길이 경로, 우주선 예시 수와 전체 격자, 도서관 본문 6개와 그림 7개, 도움 요정의 남는 길이와 언어별 표현을 구별했다.',
        )],
        unread_followups=[LIMITS, previous['external_manual_access_followup']['web_cached_text_seen_scope']],
    )
    notes_path = ROOT / NOTES
    write(notes_path, notes)
    source.update(
        date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(notes_path),
        snapshot_history=source['snapshot_history'] + [dict(
            snapshot_file=PRIOR_NOTES, snapshot_sha256=PRIOR_SHA, date=source['date'], read_scope=source['read_scope'],
        )],
        bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
        method_note='연결 PDF의 모든 쪽을 렌더해 확인하고 텍스트 및 지도 벡터 길이를 대조했다. 삽입 그림은 해당 페이지와 연결하고 같은 파일을 해시로 구별했다.',
        editorial_action='길이 첨부·삽입 그림을 바탕으로 6개 기준에 주장 3건과 자체 관찰 과제 2개를 대응했다. LT2 누적 주장 44건·관찰 42건·기준 48개다.',
        image_read_manifest=all_images, supplementary_pdf_read_manifest=all_pdfs,
        observations=source['observations'] + OBSERVATIONS,
    )
    registry['claims'].extend(claims)
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(v for v in queue['literature_review'] if v['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[c['id'] for c in all_claims])
    write(sources_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Reviewed 8 PDFs (10 pages) and 93 image URLs. Added 3 claims and 2 observation activities.')


if __name__ == '__main__':
    main()

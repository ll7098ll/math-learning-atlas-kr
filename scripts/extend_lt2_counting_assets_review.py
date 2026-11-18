"""Record the counting worksheets and figures reviewed against LT2 activity text."""
import copy

from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_counting_activities_review_notes.json'
PRIOR_SHA = '46e75f3935d698c73b3e8f4d6a04211c3cdf2fe51b973f275c04c61931a3981a'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_counting_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-counting-assets'

SCOPE = (
    '공개 영어 HTML 494개와 활동·교사자료 본문 244개를 확인했다. 목록의 본문 580개가 남았다. '
    '세기 활동의 연결 PDF 15개 URL·78쪽과 삽입 이미지 146개 URL을 추가로 대조했다. '
    '누적 PDF 39개 URL·107쪽, 삽입 이미지 349개 URL이다. 같은 파일을 한 번씩 세면 PDF 36개·104쪽과 이미지 343개다.'
)
LIMITS = (
    '링크로 확인한 PDF와 삽입 그림의 범위다. 별도 게임판의 실제 인쇄·진행, 삽입 그림 밖의 자료, '
    '책 목록에 소개한 책 원문, 인용 원연구, 번역 동등성, 독립 검토와 학생 응답은 후속 범위다.'
)

PDF_NOTES = {
    '1580172018146.pdf': [
        ([1], '0~5 카드마다 2열×5행의 틀이 하나 있다. 0은 틀에 점이 없는 경우이며 칸 자체는 10개다.'),
        ([2], '6~10 카드는 왼쪽 열에 5개를 채운 뒤 오른쪽 열 아래부터 점을 채운다. 숫자와 점 개수가 일치한다.'),
    ],
    '1580172084628.pdf': [
        ([1], '0~5 카드마다 열 칸짜리 틀 두 개가 있다. 0에서 두 틀 모두 비어 있다.'),
        ([2], '6~11 카드에서 10은 첫 틀이 가득 찬 상태, 11은 둘째 틀에 한 점을 더한 상태다.'),
        ([3], '12~17은 첫 틀에 10개, 둘째 틀에 나머지 점이 있다.'),
        ([4], '18~20에서 19는 빈 칸이 하나이며 20은 두 틀이 모두 찼다.'),
    ],
    '1582239622565.pdf': [
        ([1, 2], '표지·목차다. 3~6쪽의 읽기 안내와 7~27쪽의 추천 자료 목록을 구별한다.'),
        ([3, 4], '수학이 줄거리에 필요한 책, 특정 개념을 설명할 기회를 주는 책, 삽화를 탐색하는 책을 구별한다. 상호 대화와 질문을 제안하며 개별 효과 연구는 별도다.'),
        ([5, 6], '5쪽 표는 수 글자 찾기·읽는 방향·내용 질문의 예다. 왼쪽에서 오른쪽으로 읽을수록 수가 커진다는 말은 그 배열의 조건을 확인한다. 어휘와 읽기 이후 재구성 활동도 제안한다.'),
        (list(range(7, 16)), '추천도서와 수 분야 목록이다. 순서를 거꾸로 읽기, 소리·물건 세기, 개수와 자리를 구별하는 예를 확인했다. 일부 항목 번호와 서지 표기가 불연속이므로 번호를 그대로 합산하지 않는다.'),
        ([16, 17, 18, 19], '모임 단위, 순서, 하나 더하기, 수의 합성, 큰 수의 사례다. 한 묶음과 묶음 안의 낱개, 이야기의 수치와 실제 관측을 구별한다.'),
        ([20, 21, 22, 23, 24], '분수와 전체, 공간의 기준, 도형과 도형 합성의 추천 목록이다. 입체 물체·사진에 드러난 평면 흔적과 도형의 성질을 구별한다.'),
        ([25, 26, 27], '길이, 넓이, 부피, 무게, 시간, 규칙, 분류·그래프 주제를 소개한다. 소개한 책의 전권이나 그림에 나온 양의 실제 측정은 포함하지 않는다.'),
    ],
    '1589493436638.pdf': [
        ([1], '교사가 단계를 시범 보이고 아이가 단계별로 설명하는 표다. 게임 규칙 설명을 이해하는 것과 게임에서 수를 독립적으로 세는 것은 따로 관찰한다.'),
        ([2], '경쟁보다 참여와 전략 관찰을 강조한다. 특정 놀이판의 끝이나 초과 수 처리 규칙을 제공하지 않는다.'),
    ],
    '1600363477918.pdf': [([1], '생각하기·짝과 마주하기·생각 나누기를 보여 주는 세 칸이다. 수학 답안이나 실제 학생 기록은 없다.')],
    '1630081475115.pdf': [([1], '1~20의 번호 칸과 별도 출발·도착 그림이 있다. 20에서 도착 그림까지를 한 칸으로 더 세는지는 본문과 함께 정해야 한다.')],
    '1638558477915.pdf': [
        (list(range(1, 9)), '한 쪽에 버스 그림 4대, 한 버스에 2×5 자리다. 1~8쪽의 렌더가 같은 해시다.'),
        ([9, 10], '각 쪽에 가로 방향 버스 한 대와 자리 10개가 있다. 자리 수, 버스 수, 별도로 올려놓은 말 수를 구별한다.'),
    ],
    '1659473212043.pdf': [(list(range(1, 11)), '영어 표제의 장면 그림 10개다. 공항·해변·공룡·농장·자연·파티·놀이터·축구·우주·거리의 배경 그림과 위에 놓을 물건 중 무엇을 세는지 정한다.')],
    '1659475950567.pdf': [(list(range(1, 11)), '같은 주제 순서의 스페인어 표제 10쪽이다. 일부에 검은 띠나 블록이 보인다. 두 자료의 그림 배치와 가려진 부분까지 같다고 보지 않는다.')],
    '1690820089888.pdf': [([1], '주머니 사진 두 장에 서로 다른 모임을 제시한다. 그림에 보이는 물건과 닫힌 주머니 안의 수를 구별한다.')],
    '1691086878007.pdf': [([1], '개인 생각, 짝, 차례로 공유하는 안내다. 특정한 몸짓이나 시선보다 실제로 설명한 수학 내용과 도움 전후를 기록한다.')],
    '1693604961063.pdf': [([1], '0~10의 동일한 간격을 표시한 수직선이다. 눈금 11개와 그 사이 간격 10개를 구별한다.')],
    '1698429547825.pdf': [
        ([1, 2, 3], '한 과자 그림의 점 자리는 각각 10·20·50개다. 렌더에서 닫힌 흰 원을 검산했다.'),
        ([4, 5], '과자 윤곽은 각각 4개와 8개다. 어느 쪽에도 점 자리는 미리 표시되어 있지 않다.'),
    ],
    '1698457501922.pdf': [
        ([1], '주사위를 던지고 그 수만큼 확인 접시에 놓고, 짝이 확인한 뒤 과자로 옮기는 순서다.'),
        ([2], '역할을 바꾸고 두 판을 채울 때까지 진행한다. 남은 자리보다 큰 수가 나오면 어떻게 하는지 정하지 않는다.'),
    ],
    '1743450846128.pdf': [([1], '1~100의 10행×10열 표다. 0과 100을 넘는 수는 그 표에 없다. 100 이후 활동에는 이어지는 자료가 필요하다.')],
}

IMAGE_NOTES = [
    ([36, 45, 48, 53, 72, 75, 84, 87, 105, 106, 117, 129, 130], '점·초·창·과자·카드의 그림에서 세는 대상을 정한다. 이미지 105의 5 접시는 점 5개와 함께 제시되어 영어 절차의 점 1개 지시와 다르다. 117에서 보이는 37·38·39 뒤의 카드는 연속 배열 조건이 있어야 값을 예상할 수 있다.'),
    ([41, 42, 57, 58, 67, 74, 76, 78, 80, 110, 136, 139], '수 카드와 놀이판의 미리보기다. 42는 40에서 70까지의 이동값 30을 표시한 빈 수직선이다. 78의 이름에는 1~5가 있으나 보이는 그림은 0 카드도 포함한다. 포스터·수 카드 전체와 실제 페이지의 축척은 별도로 확인한다.'),
    ([8, 55, 59, 63, 65, 68, 70, 77, 79, 82, 83, 116, 123, 131, 132, 133, 140], '가린 모임, 용기와 실제 내용, 자리와 물건, 묶음, 액면과 장수의 차이를 확인한다. 70에는 1 표시 다섯 장과 5 표시 한 장이 있어 여섯 장의 액면 합은 10이다.'),
    ([62], 'RGB 값이 모든 픽셀에서 같은 회색 파일이다. 수 모형·학생 응답·절차 그림으로 판정하지 않는다.'),
    ([89, 108, 109, 111, 143, 144, 145], '제목 또는 도구 미리보기다. 145의 그림만으로 1~6이 표시된 실물 돌림판의 구획이나 각 결과의 가능성을 확정하지 않는다. 끝 판과 역할표의 실제 배포본은 구별한다.'),
]

CLAIMS = [
    ('LT50', ['2수01-01', '2수01-02', '2수01-04'], ['1580172018146.pdf', '1580172084628.pdf', '1638558477915.pdf'], [78, 105],
     '틀의 전체 칸 수, 놓은 점의 수, 빈 칸 수를 구별한다. 열 칸을 채운 뒤 나머지를 놓는 배열은 10과 낱개의 합을 보여 준다. 과자 그림의 5 접시는 점 5개와 대응한다.',
     '틀이 10칸이라고 현재 놓인 점도 10개인 것은 아니다. 같은 수는 다른 배치로도 나타낼 수 있으며, 익숙한 모양에서 맞힌 답만으로 독립 세기를 판단하지 않는다.'),
    ('LT51', ['2수01-05', '2수01-06'], ['1630081475115.pdf', '1698429547825.pdf', '1698457501922.pdf', '1589493436638.pdf'], [143, 145],
     '정해진 수만큼 먼저 모아 확인한 뒤 판으로 옮기는 절차와, 판의 남은 자리 및 차례를 끝내는 규칙을 구별한다. 과자 판의 표시된 자리 수는 10·20·50이다.',
     '단계 그림과 번호 판에서 초과 수를 처리하는 규칙은 확정되지 않는다. 말이 출발 그림에서 어디까지 움직이는지, 남은 양을 어디에 두는지 활동 전에 정한다.'),
    ('LT52', ['2수01-01', '2수04-01'], ['1659473212043.pdf', '1659475950567.pdf', '1690820089888.pdf', '1600363477918.pdf', '1691086878007.pdf'], [62, 63],
     '배경에 그려진 것, 활동 중에 놓은 물건, 가려져 볼 수 없는 물건을 구분해 세는 대상을 지정한다. 생각하고 짝과 확인한 뒤 공유하는 단계는 수학 응답을 관찰할 시점을 제공한다.',
     '장면 사진, 역할 지원 그림, 단색 파일을 독립 학생 응답이나 수학 효과의 자료로 집계하지 않는다. 같은 표제라도 언어판의 가린 영역과 배치까지 일치한다고 보지 않는다.'),
    ('LT53', ['2수01-03'], ['1582239622565.pdf', '1693604961063.pdf', '1743450846128.pdf'], [42, 117, 139],
     '읽기 안내의 방향과 수의 크기에 관한 예를 쓰려면 오름차순 배열을 확인한다. 같은 간격의 수직선, 행과 열로 놓인 1~100 표, 이동값만 적은 빈 수직선을 구별한다.',
     '왼쪽에서 오른쪽으로 보는 것만으로 수가 커진다고 할 수 없다. 1~100 표를 0이나 101 이후의 근거로 쓰지 않으며 추천 목록에 든 책 전체나 인용 연구를 읽은 것으로 세지 않는다.'),
]

OBSERVATIONS = [
    dict(id='LT-P47', standard_codes=['2수01-02', '2수01-04'],
         question='열 칸짜리 틀 두 개가 있다. 가에서는 첫 틀에 10개, 둘째에 1개를 놓고, 나에서는 첫 틀에 5개, 둘째에 6개를 놓았다. 두 경우의 놓인 수와 비어 있는 칸 수를 각각 구하라. 어느 배치에서 10과 낱개가 바로 보이는가?',
         expected='가의 10+1과 나의 5+6은 모두 11이다. 틀 전체의 20칸 중 11칸을 썼으므로 두 경우 모두 9칸이 비었다. 가에서는 한 틀이 가득 차 10과 낱개 1이 바로 보인다.',
         interpretation='채워진 수·빈 칸 수·수용할 수 있는 전체를 구별한다. 나에서 둘째 틀의 5개를 첫 틀로 옮겨도 전체 수는 변하지 않음을 도구로 설명하게 한다.', student_validated=False),
    dict(id='LT-P48', standard_codes=['2수01-05', '2수01-06'],
         question='20칸 놀이판에 말이 18개 놓여 있다. 이번 차례에 4가 나와 접시에 말 4개를 가져왔다. 규칙 A에서는 가져온 말이 모두 들어갈 때만 놓는다. 규칙 B에서는 빈 칸만큼 놓고 남는 말은 접시에 둔다. 규칙마다 판과 접시에 몇 개가 남는가?',
         expected='빈 칸은 20−18로 2칸이다. A에서는 한 개도 옮기지 않아 판 18개와 접시 4개다. B에서는 2개를 옮겨 판 20개와 접시 2개다. 판과 접시를 합하면 두 경우 모두 22개다.',
         interpretation='두 규칙은 과제에서 정한 가정이다. 주사위 값, 옮긴 말 수, 판에 놓인 수, 두 모임의 전체를 각각 설명하는지 확인한다.', student_validated=False),
]


def reviewed_pdfs(raw):
    assets, notes = [], {}
    for item in raw:
        name = item['url'].rsplit('/', 1)[-1]
        pages = list(range(1, item['pdf_pages'] + 1))
        entries = PDF_NOTES[name]
        assert [p for group, _ in entries for p in group] == pages
        assert item['status'] == 200 and sha(ROOT / item['file']) == item['sha256']
        assert [r['pdf_page'] for r in item['renders']] == pages
        for render in item['renders']:
            assert sha(ROOT / render['file']) == render['sha256']
        asset = {k: item[k] for k in ('url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'pdf_pages')}
        asset.update(read_kind='linked_pdf_content_and_visual_review', redistributed=False,
                     content_read_method='visual_pages_and_available_text', content_pdf_pages=pages,
                     visual_pdf_pages=pages, rendered_pages=[{k: r[k] for k in ('pdf_page', 'sha256')} for r in item['renders']])
        assets.append(asset)
        notes[item['url']] = [dict(pdf_pages=group, note=note) for group, note in entries]
    return assets, notes


def reviewed_images(raw):
    assets = []
    for index, item in enumerate(raw):
        assert item['index'] == index and item['status'] == 200 and sha(ROOT / item['file']) == item['sha256']
        asset = {k: item[k] for k in ('url', 'page_url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'dimensions')}
        assets.append(dict(asset, read_kind='inline_image_visual_review', redistributed=False))
    listed = [i for indices, _ in IMAGE_NOTES for i in indices]
    assert len(listed) == len(set(listed)) and set(listed) <= set(range(len(raw)))
    remainder = sorted(set(range(len(raw))) - set(listed))
    groups = IMAGE_NOTES + [(remainder, '나머지 수업·일상 사진, 책 표지, 재료와 동작 예시 그림을 확인했다. 사진만으로 한 번씩 셌는지, 학생이 무엇을 설명했는지, 배포 자료 전체가 들어 있는지는 판단하지 않는다.')]
    return assets, [dict(image_urls=[assets[i]['url'] for i in indices], note=note) for indices, note in groups]


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        assert {row[0] for row in CLAIMS} <= {c['id'] for c in registry['claims']}
        assert source['observations'][-2:] == OBSERVATIONS
        build_report()
        return
    assert source['snapshot_file'] == PRIOR and sha(ROOT / PRIOR) == PRIOR_SHA
    prior = load(ROOT / PRIOR)
    raw_pdfs = load(CACHE / 'pdf-manifest.json')
    raw_images = load(CACHE / 'image-manifest.json')
    assert len(raw_pdfs) == 15 and len(raw_images) == 146
    assert asset_pairs(raw_pdfs) == linked_pairs(prior['counting_linked_pdf_urls_not_reviewed'])
    assert asset_pairs(raw_images) == linked_pairs(prior['counting_inline_image_urls_not_reviewed'])
    pdfs, pdf_notes = reviewed_pdfs(raw_pdfs)
    images, image_notes = reviewed_images(raw_images)
    cookie = load(CACHE / 'cookie-mark-counts.json')
    assert [r['white_mark_count'] for r in cookie] == [10, 20, 50, 0, 0]
    assert 10 + 1 == 5 + 6 == 11 and 20 - 11 == 9
    assert 20 - 18 == 2 and 18 + 4 == 20 + 2 == 22

    all_pdfs = prior['supplementary_pdf_read_manifest'] + pdfs
    all_images = prior['image_read_manifest'] + images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert len(all_pdfs) == 39 and sum(a['pdf_pages'] for a in all_pdfs) == 107
    assert len(unique_pdfs) == 36 and sum(unique_pdfs.values()) == 104
    assert len(all_images) == 349 and len({a['sha256'] for a in all_images}) == 343
    assert len({r['sha256'] for a in pdfs for r in a['rendered_pages']}) == 71
    names = {a['url'].rsplit('/', 1)[-1]: a['url'] for a in pdfs}
    source_path = ROOT / 'data/sources.json'
    bibliography = load(source_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(
        date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
        supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
        supplementary_pdf_coverage=dict(urls=39, page_occurrences=107, distinct_sha256_files=36, pages_after_file_deduplication=104,
                                       all_selected_pages_visual_reviewed=True, whole_site_attachment_review=False),
        pdf_exact_reuse_groups=reuse_groups(all_pdfs), counting_image_exact_reuse_groups=reuse_groups(images),
        new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=146, supplementary_pdf_urls=15),
        counting_linked_pdf_urls_not_reviewed={}, counting_inline_image_urls_not_reviewed={},
        pdf_reading_log={**prior['pdf_reading_log'], **{
            url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows]
            for url, rows in pdf_notes.items()
        }},
        counting_pdf_reading_log=pdf_notes, counting_image_reading_log=image_notes,
        counting_pdf_render_coverage=dict(page_occurrences=78, distinct_render_hashes=71),
        cookie_mark_counts=dict(url=names['1698429547825.pdf'], counts=cookie,
                                method='렌더에서 과자 색 영역의 경계 상자 안에 있는 흰 연결 성분을 세고 그림과 대조했다.'),
        reading_log=prior['reading_log'] + ['세기 연결 PDF 15개·78쪽과 삽입 이미지 146개 URL을 원래 활동 페이지와 대조했다.'],
        source_corrections=prior['source_corrections'] + [dict(
            kind='counting_printables_and_rules', locations=[names[k] for k in ('1580172084628.pdf', '1630081475115.pdf', '1698429547825.pdf', '1698457501922.pdf', '1743450846128.pdf')] + [images[105]['url']],
            action='틀 칸과 실제 점, 도착 그림과 번호 칸, 초과 수의 처리, 1~100의 자료 경계와 주문 5의 점 그림을 각각 구별했다.',
        )],
        unread_followups=[LIMITS, '다음 공개 본문은 남은 수량·연산 활동의 목표와 절차부터 대조한다.'],
    )
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                                date=source['date'], read_scope=source['read_scope'])]
    source.update(
        date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
        bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
        method_note='PDF 78쪽의 렌더와 가용 문자를 대조하고 삽입 이미지의 조건과 범위를 확인했다. 같은 파일과 같은 쪽 렌더를 해시로 구별했다.',
        editorial_action='수 카드와 인쇄 놀이판을 기준으로 문헌 대응 4건과 자체 관찰 과제 2개를 추가했다.',
        image_read_manifest=all_images, supplementary_pdf_read_manifest=all_pdfs,
        observations=source['observations'] + OBSERVATIONS,
    )
    for cid, codes, filenames, indices, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
            locations=[names[name] for name in filenames] + [images[i]['url'] for i in indices],
            support=support, does_not_establish=limit, independent_review=False, student_validated=False,
            target_snapshots={'revision:' + code: digest(target_value('revision:' + code)) for code in codes},
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(r for r in queue['literature_review'] if r['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[c['id'] for c in registry['claims'] if c['source_id'] == SOURCE])
    write(source_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Reviewed counting assets: 15 PDFs, 78 pages, 146 inline images; 4 mappings, 2 observations')


if __name__ == '__main__':
    main()

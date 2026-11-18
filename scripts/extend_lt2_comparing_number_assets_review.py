"""Register reviewed LT2 number-comparison printables and inline figures."""
import copy
import re

from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE
from record_mix_moore_holcomb_review import NOTES as STUDY_NOTES, PDF_URL as STUDY_PDF, SOURCE as STUDY_SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_comparing_number_activities_review_notes.json'
PRIOR_SHA = '9a99765f93bf7a05c0ffe456f4678e0c32e403f4a1e393d7fac52203dcb3ca29'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_comparing_number_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-comparing-number-assets'
SCOPE = (
    '공개 영어 HTML 690개와 활동·교사자료 본문 440개를 확인했다. 본문 384개가 남았다. '
    '수량 비교·순서의 LT2 연결 PDF 7개·14쪽과 삽입 이미지 88개 URL을 대조했다. '
    'LT2 누적 PDF 88개 URL·232쪽, 이미지 614개 URL이며 파일 해시로 중복을 빼면 PDF 79개·216쪽과 이미지 598개다. '
    '연결된 일대일 짝짓기 원연구는 별도 출처로 검토했다.'
)
LIMITS = (
    '실제 인쇄 치수와 가정·교실 진행, 영상·별도 배포본·다른 인용 원연구는 후속 범위다. '
    '원연구에서 보고한 두 조건의 비교와 자체 관찰 과제의 국내 학생 응답·독립 검토를 구별한다.'
)

PDF_NOTES = {
    '1580344555562': [([1], '0~5 수 글자와 2열×5행 점 틀을 한 장에 제시한다. 0은 빈 틀이며 카드가 빠진 상태와 구별한다.')],
    '1650999298856': [([1], '가로 10칸씩 10행에 1~100을 표시했다. 본문에 언급된 출발과 도착 글자는 인쇄판에 없다. 10에서 11로 넘어가는 줄 바꿈을 따로 보여 준다.'),
                       ([2], '렌더의 모든 채널이 흰색이고 수나 놀이 지시가 없다.')],
    '1681918582095': [([1], '71~130의 6행×10열 판이다. 115 바로 오른쪽은 빈칸이다.'),
                       ([2], '171~230의 6행×10열 판이다. 위아래로 10, 같은 행에서 오른쪽으로 1이 커진다.'),
                       ([3], '91~150의 판이다. 1쪽과 91~130을 공유하지만 116을 이 쪽에는 인쇄했다.'),
                       ([4], '51~110의 판이다. 99와 100은 같은 행이며 101은 다음 행의 첫 칸이다.'),
                       ([5], '31~90의 판이다. 본문의 색상 안내는 물리 쪽 순서와 다르다.')],
    '1686588095250': [([1], '다시 시작을 알리는 양말 그림 한 장이다. 실제 준비하는 양말 카드의 수는 본문 지시로 확인한다.')],
    '1730241658680': [([1], '수 글자 없이 빈 틀부터 다섯 점까지 여섯 장을 제시한다. 다른 주소 1586295352926의 파일과 같은 해시다.')],
    '1775680358124': [([1], '스페인어 진행 안내는 행동을 한 단계씩 보이고 짝과 차례를 정하는 설명을 싣는다.'),
                       ([2], '규칙을 바꿀 때 구성원과 합의하는 조건과 경쟁·교사의 관찰을 다룬다.')],
    '1775680358130': [([1], '영어 진행 안내에는 시범과 아이 설명의 표, 차례와 놀이 선택 방법이 있다.'),
                       ([2], '규칙 변경, 경쟁, 교사의 역할을 설명한다. 개별 수 카드의 준비 범위나 학생 수행을 보고하는 표가 아니다.')],
}

IMAGE_NOTES = [
    ([9, 27, 39, 54, 55, 56, 58, 60, 61, 62, 64, 65, 67, 68, 69, 70, 71, 72, 73, 76, 77, 78, 79, 80],
     '개수 비교, 짝짓기, 탑과 용기 재료의 그림이다. 73은 블록 30개를 표시한 준비 그림이다. 80은 틀 안의 물건과 바깥 물건이 보여 자리 수와 전체 물건 수의 범위를 나눠야 한다.'),
    ([29, 32, 33, 34, 45, 48, 51, 52, 57, 59, 66],
     '수 글자·점·격자 미리보기다. 33은 920이 두 위치에 나오며, 선택 수를 각각 다르게 해야 하는 과제에서는 이 조건을 확인한다. 52의 숫자는 0~10이다. 빈 틀을 빈자리나 분실된 카드와 구별한다.'),
    ([22, 23, 26, 46, 84, 85],
     '수직선과 놀이판·도구의 장면이다. 46은 1~100 판의 미리보기이며 하단에 화면 도구가 겹친다. 85의 미리보기에는 1~10이 모두 보이며 본문이 지목한 1·5·10의 표기와 구별한다.'),
    ([10, 35, 36, 37, 40, 41, 43, 44, 53, 63, 74, 75],
     '글자·일정·추정 대상과 준비 도구의 그림이다. 41의 첫째부터 셋째까지는 활동 순서이며 실제 활동 시간이나 개수가 아니다. 추정 사진의 화면 밖 물건은 세지 않는다.'),
]

CLAIMS = [
    ('LT79', ['2수01-02', '2수01-03'], ['1681918582095'], [48],
     '같은 행은 1씩, 같은 열은 10씩 달라지는 수판에서 빈칸의 값을 찾는다. 71~130 판과 91~150 판은 일부를 공유하지만 116의 인쇄 여부가 다르다.',
     '빈칸은 빠진 수의 위치를 나타낸다. PDF의 물리 쪽 순서에 본문의 색 이름 순서를 그대로 적용하거나 공통 범위의 모든 인쇄 상태가 같다고 가정하지 않는다.'),
    ('LT80', ['2수01-01', '2수01-03', '2수01-06'], ['1650999298856'], [46, 85],
     '100칸 판은 각 행에서 왼쪽부터 커지고 다음 행 첫 칸으로 이어진다. 출발·도착 글자가 없는 판에서는 어디에서 시작하고, 끝에 닿거나 넘는 값을 어떻게 처리할지 명시한다.',
     '숫자 표지 100개, 1에서 100까지의 이동 99번, 주사위 값과 실제 이동을 서로 구별한다. 1~10 미리보기는 별도의 판이다.'),
    ('LT81', ['2수01-01', '2수01-03', '2수01-04'], ['1580344555562', '1730241658680', '1686588095250', '1775680358124', '1775680358130'], [45, 51, 52, 57, 59, 66],
     '0의 빈 점 카드와 실제 카드가 없는 상태를 구별한다. 카드가 0~5인지 1~5인지 먼저 정하고, 다시 시작하는 표식과 수량을 나타내는 카드의 기능도 나눈다.',
     '숫자 글자의 유무, 놀이 규칙을 기억하는 수행과 수를 정렬하는 수행을 구별한다. 일반 진행 안내로 특정 활동의 카드 범위나 효과를 판단하지 않는다.'),
    ('LT82', ['2수01-03', '2수01-06', '2수03-06'], [], [27, 58, 60, 65, 73],
     '블록 열차 두 개를 동시에 만들 때 각 열차에 필요한 수를 합해 준비량과 비교한다. 열차의 길이 차이를 블록 수로 설명하려면 같은 크기의 블록을 쓰고 시작점을 맞춘다.',
     '블록 그림의 수량과 수 카드에 허용한 최대값은 서로 다를 수 있다. 한 사람의 준비량인지 두 사람의 공유량인지 먼저 정한다.'),
]

OBSERVATIONS = [
    dict(id='LT-P70', standard_codes=['2수01-02', '2수01-03'],
         question='한 행에 열 칸이 있는 수판이다. 가로로 오른쪽 한 칸은 1이 더 크고, 세로로 아래 한 칸은 10이 더 크다. 빈칸의 왼쪽이 115, 바로 위가 106이다. 두 단서를 각각 써서 빈칸을 구하라. 다른 수판의 같은 자리에 이 수가 적혀 있다면 두 판에서 뜻하는 수는 다른가?',
         expected='왼쪽의 115에 1을 더해 116이다. 위의 106에 10을 더해도 116이다. 같은 수 범위와 행 규칙이라면, 인쇄되어 있는지와 관계없이 그 칸의 수는 116이다.',
         interpretation='가로와 세로의 단위 변화가 다름을 설명하게 한다. 어느 한 칸을 빈 상태로 두는 것과 규칙에서 값이 빠지는 것을 구별한다.', student_validated=False),
    dict(id='LT-P71', standard_codes=['2수01-03', '2수01-06'],
         question='수판에서는 10 다음에 아래 행의 첫 칸 11로 간다. 9번에서 3번 움직이면 어느 칸인가? 98번에서 4가 나오면 100번에 닿는 데 몇 번이 필요한가? 100에 닿으면 멈추는 규칙과 정확히 닿을 때만 이동하는 규칙을 각각 적용해 보라.',
         expected='9 다음의 10·11·12에 닿으므로 12번이다. 98에서는 99와 100까지 두 번이면 된다. 닿으면 멈추는 규칙에서는 100에 도착하며 두 번의 이동이 남는다. 정확히 닿을 때만 움직이는 규칙에서는 이번에 98에 남는다.',
         interpretation='행이 바뀌어도 수의 차이는 1임을 설명한다. 주사위 값, 실제 이동 횟수와 멈추는 조건을 따로 기록한다.', student_validated=False),
    dict(id='LT-P72', standard_codes=['2수01-01', '2수01-03', '2수01-04'],
         question='가의 카드 묶음에는 점이 없는 틀과 점 1~5개짜리 카드가 한 장씩 있다. 나의 묶음에는 점 1~5개짜리 카드만 있다. 점이 적은 것부터 놓으면 각각 첫 카드가 나타내는 수와 전체 카드 장수는 얼마인가?',
         expected='가는 0부터 시작하고 카드가 6장이다. 나는 1부터 시작하고 카드가 5장이다. 가의 빈 틀은 점이 0개인 카드 한 장이다.',
         interpretation='카드 장수와 카드 위의 점 수를 구별한다. 1부터 시작하는 규칙에서 0을 준비하지 않은 것을 누락이라고 판정하지 않는다.', student_validated=False),
    dict(id='LT-P73', standard_codes=['2수01-06', '2수03-06'],
         question='같은 크기의 블록으로 12개짜리 열차와 15개짜리 열차를 동시에 만들려 한다. 두 사람이 공유하는 그릇에 블록은 20개뿐이다. 두 열차가 다 필요로 하는 블록 수와 모자란 수를 구하라. 시작점을 맞춰 두 열차를 나란히 놓으면 어느 쪽이 몇 블록 길이만큼 더 긴가?',
         expected='모두 27개가 필요해 7개가 모자란다. 같은 크기의 블록을 빈틈없이 이으면 15개짜리가 3블록 길이만큼 더 길다.',
         interpretation='준비량에서 모자란 7개와 두 열차 길이의 차이 3블록을 구별한다. 블록 크기가 서로 다르면 개수만으로 길이 차이를 정할 수 없다.', student_validated=False),
]


def verify_printed_numbers():
    grid_path = CACHE / '1681918582095.txt'
    text = grid_path.read_text(encoding='utf-8')
    pages = re.split(r'=== PDF PAGE \d+ ===', text)[1:]
    starts = [71, 171, 91, 51, 31]
    results, printed = [], []
    for page, (start, raw) in enumerate(zip(starts, pages), 1):
        rows = [[int(v) for v in line.split()] for line in raw.splitlines() if line.strip()]
        assert len(rows) == 6
        assert all(set(row) <= set(range(start + 10 * i, start + 10 * i + 10)) for i, row in enumerate(rows))
        present = set(sum(rows, []))
        assert len(present) == sum(map(len, rows))
        printed.append(present)
        results.append(dict(pdf_page=page, first_value=start, last_value=start + 59, row_count=6, column_count=10,
                            printed_value_count=len(present), empty_cell_count=60-len(present)))
    shared = set(range(91, 131))
    assert (printed[0] ^ printed[2]) & shared == {116} and 116 not in printed[0] and 116 in printed[2]
    assert 115 in printed[0] and 106 in printed[0] and 115 + 1 == 106 + 10 == 116
    race = (CACHE / '1650999298856.txt').read_text(encoding='utf-8')
    first, second = re.split(r'=== PDF PAGE \d+ ===', race)[1:]
    assert not second.strip() and not re.search(r'\b(?:Start|Finish)\b', first)
    assert [int(v) for v in re.findall(r'\b\d+\b', first)] == list(range(1, 101))
    assert 12 + 15 - 20 == 7 and 15 - 12 == 3 and 100 - 98 == 2 and 9 + 3 == 12
    return dict(number_grids=results, shared_rows=dict(pages=[1, 3], values=[91, 130], differing_printed_value=116),
                race_board=dict(printed_range=[1, 100], blank_pages=[2], start_and_finish_labels=False))


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
    assert len(listed) == len(set(listed)) and set(listed) <= set(range(len(images)))
    others = sorted(set(range(len(images))) - set(listed))
    groups = IMAGE_NOTES + [(others, '놀이·수업 장면에서 재료와 위치를 확인했다. 장면만으로 아이의 답, 교사가 준 도움이나 놀이 결과를 판단하지 않는다.')]
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
    assert len(raw_pdfs) == len(PDF_NOTES) == 7 and len(raw_images) == 88
    pdfs, images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images)
    study = registry['sources'][STUDY_SOURCE]
    assert study['snapshot_file'] == STUDY_NOTES and study['snapshot_sha256'] == sha(ROOT / STUDY_NOTES)
    linked_pdf_pairs = linked_pairs(prior['comparing_number_pdf_urls_not_reviewed'])
    study_link = (STUDY_PDF, 'https://www.learningtrajectories.org/math-activities/put-them-together-early-comparison-corresponder')
    assert asset_pairs(pdfs) | {study_link} == linked_pdf_pairs and study_link not in asset_pairs(pdfs)
    assert asset_pairs(images) == linked_pairs(prior['comparing_number_image_urls_not_reviewed'])
    all_pdfs = prior['supplementary_pdf_read_manifest'] + pdfs
    all_images = prior['image_read_manifest'] + images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (88, 232)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (79, 216)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (614, 598)
    assert len({a['sha256'] for a in images}) == 85
    names = {a['url'].rsplit('/', 1)[-1].removesuffix('.pdf'): a['url'] for a in pdfs}
    numbers = verify_printed_numbers()

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
                 supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
                 supplementary_pdf_coverage=dict(urls=88, page_occurrences=232, distinct_sha256_files=79,
                                                 pages_after_file_deduplication=216, all_selected_pages_visual_reviewed=True,
                                                 whole_site_attachment_review=False),
                 pdf_exact_reuse_groups=reuse_groups(all_pdfs), comparing_number_image_exact_reuse_groups=reuse_groups(images),
                 comparing_number_pdf_urls_not_reviewed={}, comparing_number_image_urls_not_reviewed={},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=88, supplementary_pdf_urls=7),
                 comparing_number_pdf_reading_log=pdf_notes, comparing_number_image_reading_log=image_notes,
                 comparing_number_printed_number_checks=numbers,
                 comparing_number_external_study=dict(source_id=STUDY_SOURCE, url=study_link[0], linking_activity=study_link[1],
                                                      snapshot_file=STUDY_NOTES, snapshot_sha256=study['snapshot_sha256']),
                 pdf_reading_log={**prior['pdf_reading_log'], **{
                     url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows]
                     for url, rows in pdf_notes.items()}},
                 reading_log=prior['reading_log'] + ['수량 비교·순서의 LT2 연결 PDF 7개·14쪽과 삽입 이미지 88개 URL을 대조했다. 연결 원연구는 별도 등록했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='number_grid_material_and_card_scope', locations=[names[n] for n in ('1681918582095', '1650999298856', '1730241658680')],
                     action='공통 수 격자의 인쇄 상태, 놀이판의 표기와 줄 바꿈, 0 카드와 놀이 범위, 실제 블록 준비량을 구별했다.')],
                 unread_followups=[LIMITS, '수량을 세지 않고 알아보는 활동의 공개 본문을 우선 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
                  method_note='판과 카드의 범위, 삽입 미리보기와 본문에 적힌 조건을 대조했다.',
                  editorial_action='LT2 문헌 대응 4건과 관찰 과제 4개를 추가했다.', image_read_manifest=all_images,
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
    print('Reviewed 7 LT2 PDFs, 14 pages and 88 images; added 4 mappings and 4 observation tasks.')


if __name__ == '__main__':
    main()

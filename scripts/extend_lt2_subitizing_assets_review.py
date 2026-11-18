"""Register reviewed printables and images linked from LT2 subitizing activities."""
import copy

from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE
from record_bjorklund_palmer_landgren_review import NOTES as STUDY_NOTES, URL as STUDY_URL, SOURCE as STUDY_SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_subitizing_activities_review_notes.json'
PRIOR_SHA = '0ae514e3728dc490d23cf619280fbb6df792abfd9824d44c1dab999a4558c618'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_subitizing_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-subitizing-assets'
SCOPE = (
    '공개 영어 HTML 721개와 활동·교사자료 본문 471개를 확인했다. 본문 353개가 남았다. '
    '수량을 세지 않고 알아보는 활동의 LT2 PDF 6개·47쪽과 삽입 이미지 41개 URL을 대조했다. '
    'LT2 누적 PDF 94개 URL·279쪽, 이미지 655개 URL이며 같은 파일을 한 번만 세면 PDF 84개·262쪽과 이미지 635개다. '
    '연결된 유아 놀이 관찰 연구는 별도 출처로 검토했다.'
)
LIMITS = (
    '배열과 영아 수량 탐색의 인용 원연구, 실제 인쇄 크기와 노출 시간, 번역 동등성 및 카드 덱 전체는 후속 범위다. '
    '교실의 학생 응답·진단 검증과 외부 연구의 관찰을 구별한다.'
)

PDF_NOTES = {
    '1610648702529': [([1], '빈 십 틀부터 5점까지 여섯 카드다. Concentration의 기본 지시는 최대 3점이다. 선택할 범위는 활동의 지시에 맞춘다.')],
    '1639767336750': [([1], '표지의 수준명은 10까지다. 다음 20쪽은 빨강과 노랑의 점을 각각 다른 십 틀에 놓는다.'),
                       ([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], '서로 다른 카드에 같은 점 수가 있는 경우를 포함한다. 2쪽은 7과 6이다. 3·5·9·14쪽은 좌우 점 수가 같다.'),
                       ([15, 16, 17, 18, 19, 20, 21], '15쪽은 1과 2다. 21쪽은 7과 9다. 전체 20쌍의 각 틀에 나온 수는 1~9이고 10점이 든 틀은 없다.')],
    '1695326045545': [([1], '4점 배열을 줄과 정방형 모양 등 여러 방식으로 제시한다.'),
                       ([2], '5점 배열의 난이도를 나누어 제시한다. 배열이 바뀌어도 각 모임의 점 수는 5다.')],
    '1741025258884': [([1, 2, 3], '1~3개의 점을 중앙·가장자리, 줄과 꺾인 모양 등으로 보여 준다. 접시의 테두리는 점을 놓을 위치의 참고선이다.'),
                       ([4, 5], '4와 5를 각각 다른 쪽에 다양한 배치로 제시한다. 난이도 표기는 편집 안내에 해당한다.')],
    '1753996858184': [([1, 2], '영어와 스페인어 안내는 7 초과의 도전 카드가 포함되어 있다고 설명한다.'),
                       ([3, 4], '점 카드의 두 부분은 각각 1과 2, 3과 4다. 합은 3과 7이다.'),
                       ([5, 6, 7], '합이 각각 11·15·19다. 6쪽의 도전 문구와 별도로 실제로 7을 넘는 쪽은 5~7쪽이다.')],
    '1759865438623': [([1, 2], '같은 활동 제목의 다른 PDF다. 영어·스페인어 인쇄 안내가 있다.'),
                       ([3, 4, 5, 6, 7, 8], '전체 점 수는 순서대로 5·5·7·7·5·7이다. 6쪽에 도전 카드라고 적혀 있으나 합은 7이다.'),
                       ([9, 10], '각각 6점이다. 9쪽은 구분선 없이 위아래 3개씩이고 10쪽은 좌우에 3개씩이다.'),
                       ([11], '활동 제목과 접시의 7점 예시가 있는 쪽이다. 앞의 카드 쪽과 별도로 기록한다.')],
}

IMAGE_NOTES = [
    ([5, 10, 11], '같은 파일의 세 그릇 사진이다. 들어 올린 순간을 보여 주며 그릇의 이전 위치와 아이가 고른 수를 판단할 수 없다.'),
    ([18, 19, 23, 26], '18은 빨강 3과 노랑 4, 19는 빨강 7과 노랑 9다. 23은 빈 십 틀이다. 26은 별도 틀에 각각 9개와 2개를 넣은 예시다.'),
    ([22, 32, 34, 35, 38, 40], '22는 1~5 배열 준비, 32는 2·3·3·5점 접시다. 34는 여우, 35는 점 카드 PDF의 표지, 38은 1~5 수 글자와 점 쿠키, 40은 카드 덱 표지다.'),
    ([20, 21, 24, 25, 29, 30, 31], '천·물건·접시와 동작 선택판 등 준비물 그림이다. 그림이 한 차례에 사용한 수량이나 학생의 수행을 입증하지 않는다.'),
]

CLAIMS = [
    ('LT88', ['2수01-01', '2수01-03'], ['1610648702529', '1741025258884'], [22, 32, 38],
     '카드 전체의 범위와 한 활동에서 실제로 고른 범위를 구별한다. 빈 십 틀은 점이 0개인 카드이고, 같은 수의 점도 위치나 배치를 달리할 수 있다.',
     '카드에 0이나 5가 있다는 사실만으로 기본 짝짓기에 그 수를 반드시 쓴다고 해석하지 않는다.'),
    ('LT89', ['2수01-03', '2수01-05', '2수01-06'], ['1639767336750'], [18, 19, 23],
     '빨강과 노랑의 두 십 틀에 서로 다른 수 또는 같은 수가 놓인다. 각자 맡은 색의 수, 두 수의 대소, 두 수의 합을 따로 질문한다.',
     '한 틀의 실제 예는 1~9다. 두 틀을 한 사람의 문항으로 합치려면 별도의 규칙을 명시한다.'),
    ('LT90', ['2수01-04', '2수01-05', '2수01-06'], ['1695326045545', '1753996858184', '1759865438623'], [35],
     '같은 활동 제목의 두 PDF에서 7을 넘는 카드가 있는 쪽과 카드가 모두 7 이하인 쪽을 구별한다. 각 카드의 두 부분과 전체를 말하고 인쇄 범위에 맞게 고른다.',
     '제목이나 도전 문구만으로 점의 합을 확정하지 않는다. 배열 안내의 난이도와 개인별 반응은 따로 기록한다.'),
    ('LT91', ['2수01-02', '2수01-04', '2수01-06'], [], [23, 26],
     '9점과 2점이 따로 들어 있는 두 틀의 점을 합해 11이라고 설명하고, 2점 중 1점을 옮겨 가득 찬 십 틀과 낱개 1로 다시 나타낼 수 있다.',
     '틀의 총 자리 수는 20이며 채운 점은 11이다. 옮기는 설명은 활동 이미지로부터 구성한 자체 발문이다.'),
]

OBSERVATIONS = [
    dict(id='LT-P79', standard_codes=['2수01-01', '2수01-03'],
         question='점이 0개인 틀부터 5개인 틀까지 카드가 한 장씩 있다. 1~3점 카드만 골라 쓰면 몇 장이고, 전체 묶음은 몇 장인가? 빈 틀과 카드가 없는 자리를 가리켜 설명하라.',
         expected='1·2·3점 카드는 3장이다. 전체 묶음에는 0~5점 카드 6장이 있다. 빈 틀은 점이 0개인 카드 한 장이고 카드가 없는 자리는 장수에 포함하지 않는다.',
         interpretation='카드 장수, 각 카드의 점 수, 놀이에서 고른 수 범위를 구별한다.', student_validated=False),
    dict(id='LT-P80', standard_codes=['2수01-03', '2수01-05', '2수01-06'],
         question='왼쪽 십 틀에는 빨간 점 7개, 오른쪽에는 노란 점 6개가 있다. 각자 자기 색만 말하면 각각 몇 개인가? 두 색을 합치라는 새 규칙에서는 몇 개인가? 두 틀에 각각 5개씩 있다면 어느 쪽이 더 많은가?',
         expected='각자 답은 7과 6이다. 두 색을 합치면 13이다. 5개씩이라면 두 쪽의 개수가 같다.',
         interpretation='서로 다른 카드가 같은 수를 나타낼 수 있음을 설명하게 한다. 한 틀에 대한 답과 전체에 대한 답을 구별한다.', student_validated=False),
    dict(id='LT-P81', standard_codes=['2수01-04', '2수01-05', '2수01-06'],
         question='두 부분이 3점과 4점인 카드, 5점과 6점인 카드, 1점과 6점인 카드가 있다. 합이 7 이하인 것만 고르면 어떤 카드가 남는가? 7을 넘는 카드의 합은 얼마인가?',
         expected='3과 4, 1과 6인 카드가 남는다. 모두 합이 7이다. 5와 6인 카드의 합은 11이다.',
         interpretation='가장 큰 부분만 보고 카드 전체를 판단하는지 확인한다. 두 부분이 서로 달라도 전체가 같은 경우를 말하게 한다.', student_validated=False),
    dict(id='LT-P82', standard_codes=['2수01-02', '2수01-04', '2수01-06'],
         question='한 십 틀에 점 9개, 다른 십 틀에 점 2개가 있다. 한 점을 옮겨 십 틀 하나를 가득 채워라. 옮기기 전후에 전체 점은 몇 개인가? 두 틀에서 빈자리는 모두 몇 개인가?',
         expected='2점 중 하나를 9점이 있던 틀로 옮기면 10점과 1점이다. 옮기기 전후 모두 11점이며 두 틀의 전체 20자리 중 9자리가 비어 있다.',
         interpretation='십 틀의 자리 수와 실제 놓인 점 수를 구별한다. 점을 옮겨도 전체가 보존되는 근거를 묻는다.', student_validated=False),
]


def verify_dot_counts():
    counts = load(CACHE / 'preliminary-dot-counts.json')
    paired = counts['1639767336750']
    assert [p['pdf_page'] for p in paired] == list(range(2, 22))
    assert {p[side] for p in paired for side in ('left', 'right')} == set(range(1, 10))
    assert [p['pdf_page'] for p in paired if p['left'] == p['right']] == [3, 5, 9, 14]
    assert [(p['left'], p['right']) for p in (paired[0], paired[13], paired[-1])] == [(7, 6), (1, 2), (7, 9)]
    over_seven = counts['1753996858184']
    assert [p['total'] for p in over_seven] == [3, 7, 11, 15, 19]
    assert [p['pdf_page'] for p in over_seven if p['total'] > 7] == [5, 6, 7]
    to_seven = counts['1759865438623']
    assert [p['total'] for p in to_seven[:-1]] == [5, 5, 7, 7, 5, 7, 6, 6]
    assert to_seven[-1]['pdf_page'] == 11 and to_seven[-1]['illustrative_dots'] == 7
    assert all(p['left'] + p['right'] == p['total'] for p in paired + over_seven + to_seven[:6] + to_seven[7:8])
    assert to_seven[6]['top'] + to_seven[6]['bottom'] == to_seven[6]['total'] == 6
    return counts


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
    assert len(raw_pdfs) == len(PDF_NOTES) == 6 and len(raw_images) == 41
    pdfs, images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images)
    study = registry['sources'][STUDY_SOURCE]
    assert study['snapshot_file'] == STUDY_NOTES and study['snapshot_sha256'] == sha(ROOT / STUDY_NOTES)
    study_page = 'https://www.learningtrajectories.org/math-activities/what-changed'
    external_pairs = linked_pairs(prior['subitizing_external_proceedings_urls_not_reviewed'])
    assert external_pairs == {(STUDY_URL, study_page), (STUDY_URL.replace('https://', 'http://', 1), study_page)}
    assert asset_pairs(pdfs) == linked_pairs(prior['subitizing_pdf_urls_not_reviewed'])
    assert not asset_pairs(pdfs) & external_pairs
    assert asset_pairs(images) == linked_pairs(prior['subitizing_image_urls_not_reviewed'])
    all_pdfs = prior['supplementary_pdf_read_manifest'] + pdfs
    all_images = prior['image_read_manifest'] + images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (94, 279)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (84, 262)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (655, 635)
    assert len({a['sha256'] for a in images}) == 39
    names = {a['url'].rsplit('/', 1)[-1].removesuffix('.pdf'): a['url'] for a in pdfs}
    numbers = verify_dot_counts()
    dot_card_hashes = {a['sha256'] for a in all_pdfs if a['url'].rsplit('/', 1)[-1] in {
        '1610648702529.pdf', '1586295352926.pdf', '1586299768091.pdf', '1730241658680.pdf'}}
    assert len(dot_card_hashes) == 1
    assert len({images[index]['sha256'] for index in (5, 10, 11)}) == 1

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
                 supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
                 supplementary_pdf_coverage=dict(urls=94, page_occurrences=279, distinct_sha256_files=84,
                                                 pages_after_file_deduplication=262, all_selected_pages_visual_reviewed=True,
                                                 whole_site_attachment_review=False),
                 pdf_exact_reuse_groups=reuse_groups(all_pdfs), subitizing_image_exact_reuse_groups=reuse_groups(images),
                 subitizing_pdf_urls_not_reviewed={}, subitizing_image_urls_not_reviewed={},
                 subitizing_external_proceedings_urls_not_reviewed={},
                 subitizing_cited_research_pending=[row for row in prior['subitizing_cited_research_pending'] if row['linking_page'] != study_page],
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=41, supplementary_pdf_urls=6),
                 subitizing_pdf_reading_log=pdf_notes, subitizing_image_reading_log=image_notes,
                 subitizing_counted_dots=numbers,
                 subitizing_external_study=dict(source_id=STUDY_SOURCE, url=STUDY_URL, linking_activity=study_page,
                                                      snapshot_file=STUDY_NOTES, snapshot_sha256=study['snapshot_sha256'],
                                                      activity_links=sorted(url for url, _ in external_pairs)),
                 pdf_reading_log={**prior['pdf_reading_log'], **{
                     url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows]
                     for url, rows in pdf_notes.items()}},
                 reading_log=prior['reading_log'] + ['수량을 세지 않고 알아보는 활동의 LT2 PDF 6개·47쪽과 삽입 이미지 41개 URL을 대조했다. 연결된 유아 놀이 관찰 연구는 별도 등록했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='subitizing_printed_card_scope', locations=[names[n] for n in ('1610648702529', '1639767336750', '1753996858184', '1759865438623')],
                     action='카드 전체의 범위와 활동에서 고른 수, 색별 개수와 합, 같은 제목을 가진 PDF 두 개의 카드 범위를 구별했다.')],
                 unread_followups=[LIMITS, '다음에는 곱셈·나눗셈 수준에 연결된 영어 활동 본문을 우선 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
                  method_note='점 카드의 범위와 각 부분의 점 수를 세고, 삽입 미리보기와 본문에 적힌 조건을 대조했다.',
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
    print('Reviewed 6 LT2 PDFs, 47 pages and 41 images; added 4 mappings and 4 observation tasks.')


if __name__ == '__main__':
    main()

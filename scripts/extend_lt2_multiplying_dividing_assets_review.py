"""Record the reviewed images for LT2 multiplication and division activities."""
import copy

from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE
from record_davis_pitkethly_review import NOTES as STUDY_NOTES, URL as STUDY_URL, SOURCE as STUDY_SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_multiplying_dividing_activities_review_notes.json'
PRIOR_SHA = '522098a3ccc742b6761487d1a3e1f16d2692e15df5a69f24aafe34bfe54881b0'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_multiplying_dividing_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-multiplying-dividing-assets'
SCOPE = (
    '공개 영어 HTML 742개와 활동·교사자료 본문 492개를 확인했다. 본문 332개가 남았다. '
    '곱셈·나눗셈의 삽입 이미지 23개 URL을 대조했다. 누적 LT2 PDF 94개 URL·279쪽과 이미지 678개 URL이다. '
    '파일을 한 번씩 세면 PDF 84개·262쪽과 이미지 658개다. 연결된 과자 나누기 원연구는 별도 출처로 검토했다.'
)
LIMITS = (
    '읽기 책과 영상, 출판사 서지만 확인한 연구의 본문, 다운로드 링크가 없는 일부 준비물은 후속 범위다. '
    '사진 속 재료·배치와 실제 학생의 수행·수업 효과를 구별한다.'
)

IMAGE_NOTES = [
    ([6], '갈색·주황·녹색·빨강의 T 조각 네 개가 4×4를 덮는다. 색을 A·B·C·D로 바꾸면 각 행은 AAAB, CABB, CCDB, CDDD다. 8×12 전체는 이 블록을 2행 3열로 잇는 자체 확장이다.'),
    ([10, 11, 19, 20], '빈 상자와 달걀이 담긴 상자, 재료 대용품을 나누어 확인했다. 11과 19는 각각 달걀 10개다. 19는 두 활동에서 같은 주소를 사용한다.'),
    ([8, 12, 14], '신발·과일·과자의 예시다. 방향과 크기가 맞는 한 켤레라는 기준, 조각 개수와 나누는 실제 양, 한 차례의 준비량을 각각 구별한다.'),
    ([13, 16, 17, 18], '책 표지 또는 제목 그림이다. 책 속의 모자 개수와 사건의 분배 결과는 표지만으로 판단하지 않는다.'),
    ([9, 21, 22], '동물이 겹치거나 사진에서 일부가 가려질 수 있다. 한 동물당 다리 수의 조건을 먼저 정한다.'),
    ([0, 1, 2, 3, 4, 5, 7, 15], '활동 장면과 재료 예시다. 실제 응답, 분배한 수, 수업 효과를 사진 한 장에서 판단하지 않는다.'),
]

CLAIMS = [
    ('LT97', ['4수01-04', '4수01-05', '6수03-13'], [6],
     'T형 네 조각으로 4×4 블록을 만들 수 있다. 이 블록을 2행 3열로 배열하면 8×12를 덮고 T형 조각이 24개 들어간다.',
     '사진이 보여 주는 범위는 4×4 한 블록이다. 8×12의 배치는 그 블록을 반복한 자체 수학 검산이다.'),
    ('LT98', ['2수01-10', '4수01-05', '4수01-06'], [10, 11, 19, 20],
     '빈 자리, 실제 들어 있는 달걀, 상자 수를 구별한다. 10개들이 상자의 자리 수가 같아도 채운 수가 같다는 보장은 없다.',
     '가득 찬 상자와 일부만 찬 상자의 달걀을 따로 센다. 전체 자리 수와 실제 물건 수를 같은 뜻으로 쓰지 않는다.'),
    ('LT99', ['2수01-03', '4수01-05'], [8, 12, 14],
     '한 짝의 개수와 실제로 짝을 맞추는 조건을 구별한다. 과자·과일을 개수로 나눌 때와 같은 양을 나눌 때의 판단 기준을 정한다.',
     '예시 이미지로 실제 준비량, 과일 조각의 질량 또는 학생이 나눈 결과를 확정하지 않는다.'),
]

OBSERVATIONS = [
    dict(id='LT-P88', standard_codes=['4수01-04', '4수01-05', '6수03-13'],
         question='T형 조각 네 개가 빈틈없이 4×4 정사각형을 만든다. 같은 정사각형 블록으로 8×12 격자를 덮으려면 블록은 몇 개, T형 조각은 몇 개 필요한가?',
         expected='세로에 2개, 가로에 3개씩 블록 6개를 놓는다. 블록마다 T형 조각 4개가 있으므로 모두 24개다.',
         interpretation='단위 칸 96개, 4칸 조각 24개, 16칸 블록 6개를 구별한다.', student_validated=False),
    dict(id='LT-P89', standard_codes=['2수01-10', '4수01-05', '4수01-06'],
         question='달걀 27개를 한 상자에 최대 10개씩 넣는다. 가득 채운 상자는 몇 개인가? 달걀을 하나도 밖에 두지 않으려면 상자는 몇 개인가? 마지막 상자에는 빈자리가 몇 개인가?',
         expected='가득 찬 상자는 2개다. 남은 달걀 7개를 셋째 상자에 넣으므로 상자는 모두 3개이고 마지막 상자의 빈자리는 3개다.',
         interpretation='가득 찬 묶음의 수, 물건을 모두 담기 위한 상자 수와 나머지 물건을 구별한다.', student_validated=False),
    dict(id='LT-P90', standard_codes=['2수01-03', '4수01-05'],
         question='왼발 신발이 두 개, 오른발 신발이 한 개 있고 모두 같은 크기다. 한 켤레에 왼발과 오른발이 하나씩 필요할 때 몇 켤레를 만들며 어느 신발이 남는가? 세 개가 모두 왼발 신발이라면 어떻게 달라지는가?',
         expected='처음에는 한 켤레를 만들고 왼발 신발이 하나 남는다. 모두 왼발 신발이면 전체가 3개여도 한 켤레도 만들 수 없다.',
         interpretation='두 개씩의 개수 묶음과 속성 조건을 만족하는 실제 짝을 구별한다.', student_validated=False),
]


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        assert source['snapshot_sha256'] == sha(ROOT / NOTES)
        assert source['observations'][-len(OBSERVATIONS):] == OBSERVATIONS
        build_report()
        return
    assert source['snapshot_file'] == PRIOR and sha(ROOT / PRIOR) == PRIOR_SHA
    prior = load(ROOT / PRIOR)
    study = registry['sources'][STUDY_SOURCE]
    assert study['snapshot_file'] == STUDY_NOTES and study['snapshot_sha256'] == sha(ROOT / STUDY_NOTES)
    raw_images = load(CACHE / 'image-manifest.json')
    assert len(raw_images) == 23 and not prior['multiplying_dividing_pdf_urls_not_reviewed']
    images = []
    for index, row in enumerate(raw_images):
        assert row['index'] == index and row['status'] == 200 and sha(ROOT / row['file']) == row['sha256']
        data = {k: row[k] for k in ('url', 'page_url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'dimensions')}
        images.append(dict(data, read_kind='inline_image_visual_review', redistributed=False))
    assert asset_pairs(images) == linked_pairs(prior['multiplying_dividing_image_urls_not_reviewed'])
    assert sorted(i for group, _ in IMAGE_NOTES for i in group) == list(range(len(images)))
    image_notes = [dict(image_urls=[images[i]['url'] for i in group], note=note) for group, note in IMAGE_NOTES]
    all_images = prior['image_read_manifest'] + images
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (678, 658)
    assert prior['multiplying_dividing_checked_examples']['four_t_tetrominoes_square'] == ['AAAB', 'CABB', 'CCDB', 'CDDD']
    assert divmod(27, 10) == (2, 7) and 30 - 27 == 3

    html = load(ROOT / 'tmp/literature/lt2-multiplying-dividing-activities/activity-manifest.json')
    reused = {page['url']: [u for u in page['links'] if u.endswith('.pdf') and '/downloads/' not in u] for page in html}
    reused = {page: urls for page, urls in reused.items() if urls}
    assert len(reused) == 3
    linked = {u for urls in reused.values() for u in urls}
    assert len(linked) == 2 and linked <= {a['url'] for a in prior['supplementary_pdf_read_manifest']}
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, image_read_manifest=all_images,
                 multiplying_dividing_image_urls_not_reviewed={}, multiplying_dividing_image_reading_log=image_notes,
                 multiplying_dividing_previously_reviewed_pdf_links=reused,
                 multiplying_dividing_external_study=dict(source_id=STUDY_SOURCE, url=STUDY_URL,
                     linking_activity='https://www.learningtrajectories.org/math-activities/biscuits-baby',
                     snapshot_file=STUDY_NOTES, snapshot_sha256=study['snapshot_sha256']),
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=23, supplementary_pdf_urls=0),
                 reading_log=prior['reading_log'] + ['곱셈·나눗셈 삽입 이미지 23개를 대조하고 과자 나누기 연구를 별도 등록했다.'],
                 unread_followups=[LIMITS, '다음에는 분수 활동 본문을 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
                  method_note='점유한 칸과 물건 수, 전체 준비량과 화면에 보이는 양을 구별해 대조했다.',
                  editorial_action='LT2 문헌 대응 3건과 관찰 과제 3개를 추가했다.', image_read_manifest=all_images,
                  observations=source['observations'] + OBSERVATIONS)
    for cid, codes, indices, support, limit in CLAIMS:
        registry['claims'].append(dict(id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
                                       locations=[images[i]['url'] for i in indices], support=support, does_not_establish=limit,
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
    print('Reviewed 23 LT2 images; added 3 mappings and 3 observations.')


if __name__ == '__main__':
    main()

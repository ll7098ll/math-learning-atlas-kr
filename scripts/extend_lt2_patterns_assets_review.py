"""Record reviewed LT2 pattern printables and inline figures."""
import copy

from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_patterns_activities_review_notes.json'
PRIOR_SHA = '1133fd914e149a2451b581697dcb096150bdd17f919b6e9ac23385dd781e9268'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_patterns_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-patterns-assets'
SCOPE = (
    '공개 영어 HTML 812개와 활동·교사자료 페이지 562개를 확인했다. 목록에 262개가 남았다. '
    '규칙성·대수적 사고 활동의 연결 PDF 7개·24쪽과 삽입 이미지 68개 URL을 대조했다. '
    '누적 LT2 PDF 115개 URL·343쪽, 이미지 773개 URL이며 같은 파일을 한 번씩 세면 PDF 104개·320쪽과 이미지 751개다.'
)
LIMITS = (
    '별도 가정 안내 배포본, 영상·책 본문과 인용 연구의 출판본은 후속 범위다. '
    '인쇄 크기와 실제 학생의 행동은 확인 범위에 포함되지 않는다.'
)

PDF_NOTES = {
    '1583447147522': [([1, 2, 3], '서로 다른 도형 두 개의 AB를 세 번 반복해 여섯 개씩 나타냈다.'),
                       ([4, 5], '육각형·육각형·정사각형과 마름모·마름모·사다리꼴의 AAB를 두 번씩 그렸다.'),
                       ([6], '삼각형·사다리꼴·사다리꼴의 ABB를 두 번 그렸다.'),
                       ([7], '육각형·사다리꼴·삼각형의 ABC를 두 번 그렸다.')],
    '1623267895583': [([1, 2], '한 쪽에 네 칸씩 여덟 개의 빈 일과 카드다. 활동 이름이나 반복 순서는 제공하지 않는다.')],
    '1623267960383': [([1, 2], '두 쪽에 차례 1~8이 있는 일과 카드다. 번호는 제시된 자리이고 행동의 수나 반복 단위는 아니다.')],
    '1623269155737': [([1, 2], '등원·놀이·음악·점심과 독서·낮잠·바깥 놀이·하원 예다. 주어진 한 날의 차례와 여러 날에 걸친 반복을 구별한다.')],
    '1678466250498': [([1], 'AB 끈 표지마다 두 종류의 구슬이 세 개씩, 구멍 표시 뒤에 교대로 놓인다.'),
                       ([2], 'AAB·ABB·ABC는 구슬 아홉 개, AABB는 열두 개다. 왼쪽 고리는 구슬이 아니다. AAB와 ABB는 두 종류의 역할이 다르다.')],
    '1693930480621': [([1], 'AB 세 띠다. 띠마다 단위가 두 자리이고 세 번 반복된다.'),
                       ([2], 'ABC 세 띠로 각 단위가 세 자리다.'),
                       ([3], 'ABB 네 띠로 두 번째와 세 번째 도형이 같다.'),
                       ([4], 'AAB 세 띠로 첫 두 도형이 같다.'),
                       ([5], 'AABB 세 띠는 네 자리 단위를 두 번 그렸다. 한 띠의 같은 도형은 같은 방향으로 나타난다.')],
    '1696967381558': [([1], '목표는 AB 세 단위다. 앉아서 하는 작은 동작과 시각 지원을 함께 제안한다.'),
                       ([2], '본문 시범은 AB 두 단위를 제시하고 속도를 바꾼다. 언어 지원의 박수·박수·발·발 예는 한 AABB 단위다.'),
                       ([3], '교사와 함께 따라 하기, 다음 동작 예상, 멈춘 뒤 독립적으로 잇기를 구별한다. 수를 모두 말하면서 짝수에 강세를 주는 예가 있다.'),
                       ([4], '블록 색, 나뭇잎과 나뭇가지, 스티커에 번갈아 하는 규칙을 옮긴다. 소개한 책과 동작 지원의 효과는 이 PDF로 확인하지 않는다.')],
}

IMAGE_NOTES = [
    ([0,1,2,3,4,7,8,9,10,11,12,13,15,16,17,18,19,20,25,26,34,35,37,57],
     '구슬과 재료, 교실 놀이, 동작·수 세기 장면이다. 한 장의 사진으로 동작 순서나 학생이 독립적으로 설명한 내용을 판정하지 않는다.'),
    ([5,6,38,39,40,45,52,56,58,60,62,63,64,65,67],
     '띠와 뱀, 과일, 구슬, 옷, 점과 줄, 동물 등 반복을 찾는 시각 예다. 58번은 점·줄·줄을 세 번, 62번은 두 색 구슬을 11개씩 교대로, 67번은 돼지·오리를 세 번 그렸다. 색과 크기 등 어느 속성을 읽을지 정한다.'),
    ([23,42,44], '23번의 보이는 1~50 수판에서 2와 3의 배수 색이 겹치는 첫 칸은 6이며 이후 6씩 늘어난다. 42번과 44번은 1부터 시작하는 판이다.'),
    ([24,41], '24번의 네 배열 개수는 1·3·5, 4·7·10, 1·4·9, 1·3·6이다. 41번의 첫 그림은 1×2 직사각형이라 2·4·9다. 첫 그림을 정사각형 한 칸으로 바꾸어 읽지 않는다.'),
    ([28,29,30,31,32,36,43,46,47,48,49,50,51,53,54,55,61],
     '달걀판, 동물, 모자, 가위와 표, 구슬 재료, 음악과 책, 번호가 적힌 놀이판, 도형 등 문제 상황과 준비물이다. 재료 그림만으로 식이나 규칙을 확정하지 않는다.'),
    ([14,27,59], '가정 안내나 활동 배포물의 화면 일부다. 삽입된 그림 범위만 확인했고 별도 배포본 전체를 검토한 것으로 세지 않는다.'),
    ([21,22,33,66], '칠판의 수식과 두 배 덧셈 그림이다. 적힌 예와 학생이 답한 과정, 등식이 일반적으로 성립하는 이유를 구별한다.'),
]

CLAIMS = [
    ('LT116', ['2수02-01','2수02-02'], ['1583447147522','1678466250498','1693930480621'], [],
     '도형 띠와 구슬 표지에서 구분할 속성과 시작점을 정한다. 두 종류로 만든 AAB와 ABB는 단위에서 반복되는 자리의 역할이 다르다.',
     '종류 수와 단위 길이, 단위 수와 전체 개수를 각각 센다. 표지의 왼쪽 구멍을 구슬로 세지 않는다.'),
    ('LT117', ['2수02-01'], ['1623267895583','1623267960383','1623269155737'], [],
     '일과 카드의 빈칸, 차례를 표시한 1~8, 활동 그림은 서로 다른 지원이다. 하루 안의 순서와 며칠에 걸쳐 다시 나타나는 순서를 구별한다.',
     '카드 번호가 활동 횟수나 되풀이되는 단위를 뜻하지 않는다. 날마다 일정이 같은지는 별도로 확인한다.'),
    ('LT118', ['2수01-03','2수02-01','2수02-02'], ['1696967381558'], [],
     '번갈아 하는 동작은 속도를 바꿔도 AB다. 같은 동작을 두 번씩 묶은 박수·박수·발·발은 AABB이며 단위가 네 자리다.',
     '동작을 따라 하기와 스스로 다음을 잇기를 구별한다. 수를 모두 말하며 짝수에 강세를 두는 것과 짝수만 말하는 것도 다르다.'),
    ('LT119', ['2수02-01','4수02-01','6수02-01'], [], [24,41],
     '한 그림에서 L자 타일은 1·3·5, 정사각 격자는 1·4·9다. 다른 그림은 처음이 1×2라 2·4·9다. 실제 칸을 센 뒤 배열과 식을 대응한다.',
     '첫 항, 모양을 만드는 규칙과 증가량을 밝혀야 한다. 처음 세 수만으로 뒷항이 유일해지지 않는다.'),
]

OBSERVATIONS = [
    dict(id='LT-P107',standard_codes=['2수02-01','2수02-02'],
         question='육각형·육각형·정사각형을 두 번 그렸다. 가장 짧은 단위와 전체 도형 수를 말하고, 육각형을 파랑, 정사각형을 빨강으로 바꾸어 같은 규칙을 이어라.',
         expected='육각형·육각형·정사각형이 한 단위로 모두 여섯 개다. 파랑·파랑·빨강을 두 번 놓은 뒤 다음은 파랑이다.',
         interpretation='도형 두 종류, 단위의 세 자리, 전체 여섯 개를 따로 센다.',student_validated=False),
    dict(id='LT-P108',standard_codes=['2수02-01'],
         question='첫날 카드에 놀이·음악·점심을 붙였다. 둘째 날은 놀이·그림·점심이다. 카드에 1·2·3을 매일 적으면 활동이 같은 순서로 반복됐다고 할 수 있는가?',
         expected='번호는 자리다. 둘째 자리가 음악에서 그림으로 바뀌므로 두 날의 활동 배열은 다르다.',
         interpretation='활동 이름과 차례의 번호, 여러 날에 걸친 반복을 구별한다.',student_validated=False),
    dict(id='LT-P109',standard_codes=['2수01-03','2수02-01','2수02-02'],
         question='1부터 6까지 모두 말하며 짝수에서만 박수를 친다. 박수 여부를 적고 가장 짧은 단위를 말하라. 박수를 두 번 하고 두 번 쉬는 동작은 같은 규칙인가?',
         expected='쉼·박수를 세 번 반복한다. 박수·박수·쉼·쉼은 네 자리 단위로 두 자리 단위와 다르다.',
         interpretation='말한 수의 배열, 박수의 위치, 동작 단위의 길이를 따로 본다.',student_validated=False),
    dict(id='LT-P110',standard_codes=['2수02-01','4수02-01','6수02-01'],
         question='세 격자의 크기는 차례로 1×2, 2×2, 3×3이다. 각 칸 수를 구하고 모두 같은 수씩 늘었는지 말하라. 4번째는 4×4 격자로 그린다고 정하면 몇 칸인가?',
         expected='칸 수는 2·4·9이고 차는 2와 5다. 조건대로 네 번째를 그리면 16칸이다.',
         interpretation='첫 격자를 실제로 센 결과와 나머지 정사각형의 모양을 구별한다.',student_validated=False),
]


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
    assert len(raw_pdfs) == len(PDF_NOTES) == 7 and len(raw_images) == 68
    pdfs, images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images)
    assert asset_pairs(pdfs) == linked_pairs(prior['patterns_pdf_urls_not_reviewed'])
    assert asset_pairs(images) == linked_pairs(prior['patterns_image_urls_not_reviewed'])
    all_pdfs = prior['supplementary_pdf_read_manifest'] + pdfs
    all_images = prior['image_read_manifest'] + images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (115, 343)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (104, 320)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (773, 751)
    assert len({a['sha256'] for a in images}) == 68
    names = {a['url'].rsplit('/', 1)[-1].removesuffix('.pdf'): a['url'] for a in pdfs}
    assert [1 * 2, 2 * 2, 3 * 3, 4 * 4] == [2, 4, 9, 16]
    assert [2 * n - 1 for n in range(1, 4)] == [1, 3, 5]
    assert [n for n in range(1, 51) if n % 2 == n % 3 == 0] == list(range(6, 51, 6))

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
                 supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
                 supplementary_pdf_coverage=dict(urls=115, page_occurrences=343, distinct_sha256_files=104,
                                                 pages_after_file_deduplication=320, all_selected_pages_visual_reviewed=True,
                                                 whole_site_attachment_review=False),
                 pdf_exact_reuse_groups=reuse_groups(all_pdfs), patterns_image_exact_reuse_groups=reuse_groups(images),
                 patterns_pdf_urls_not_reviewed={}, patterns_image_urls_not_reviewed={},
                 patterns_study_access_notes=[
                     dict(publisher='https://link.springer.com/article/10.1007/s10649-016-9745-0',
                          publisher_scope='출판사 미리보기와 서지',
                          conference_draft='https://s3.amazonaws.com/conference-handouts/2015-nctm-boston-research/pdfs/Variable_LT_NCTM.pdf',
                          conference_draft_scope='공개 발표 자료 46쪽 확보, 본문 대조 및 출판본 동일성은 별도'),
                     dict(publisher='https://doi.org/10.5951/jresematheduc.46.5.0511',
                          bibliography='https://eric.ed.gov/?id=EJ1082153', publisher_scope='서지·초록, 출판 본문 미확보'),
                 ],
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=68, supplementary_pdf_urls=7),
                 patterns_pdf_reading_log=pdf_notes, patterns_image_reading_log=image_notes,
                 pdf_reading_log={**prior['pdf_reading_log'], **{
                     url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows]
                     for url, rows in pdf_notes.items()}},
                 reading_log=prior['reading_log'] + ['규칙성·대수적 사고의 LT2 PDF 7개·24쪽과 삽입 이미지 68개 URL을 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='pattern_repeat_and_growth_visual_distinctions',
                     locations=[names['1696967381558'], images[24]['url'], images[41]['url']],
                     action='목표와 지원 예에 나온 동작 단위의 차이와 격자 첫 항의 차이를 각각 기록했다.')],
                 unread_followups=[LIMITS, '다음에는 평면도형 활동의 영어 본문과 인용 연구를 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
                  method_note='PDF의 반복 단위와 교실 일과 지원, 동작 규칙과 타일 배열을 대조했다.',
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
    print('Reviewed 7 LT2 PDFs, 24 pages and 68 images; added 4 mappings and 4 observations.')


if __name__ == '__main__':
    main()

"""Register reviewed fraction printables, inline figures, and source study links."""
import copy
from decimal import Decimal
from fractions import Fraction
import re

from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_fraction_intervention_studies import HAMDAN, BOYER, notes_file
from record_lt2_public_review import SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_fractions_activities_review_notes.json'
PRIOR_SHA = 'eab32bdbbc1932e735273e905dedef3f8df93cba60009c26613b46aded5970c8'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_fractions_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-fractions-assets'
SCOPE = (
    '공개 영어 HTML 765개와 활동·교사자료 본문 515개를 확인했다. 본문 309개가 남았다. '
    '분수 활동의 연결 PDF 14개·40쪽과 삽입 이미지 27개 URL을 대조했다. '
    '누적 LT2 PDF 108개 URL·319쪽, 이미지 705개 URL이며 같은 파일을 한 번만 세면 PDF 97개·296쪽과 이미지 684개다. '
    '수직선과 주스 비율의 원연구 두 편은 별도 출처로 등록했다.'
)
LIMITS = (
    '실물 크기와 색·대체 도구, 영상과 읽기 책, 나머지 인용 연구는 후속 범위다. '
    '자료의 수학 검산과 실제 학생 응답 또는 효과 검증을 구별한다.'
)

PDF_NOTES = {
    '1592931128145': [([1], '0과 1이 있는 얇은 띠 여덟 개가 등분되어 있다. 내부 표시와 끝점을 포함한 표시 수를 구별한다.')],
    '1592931154889': [([1], '같은 수직선의 미등분 띠 여덟 개다. 각 0~1을 같은 간격으로 나누는 활동에 쓴다.')],
    '1592931190914': [([1], '0과 1을 먼저 놓고 네 등분한다. 0에서 첫 구간을 칠한 뒤 그 오른쪽 끝에 1/4을 적는다.')],
    '1598473604631': [([1, 2, 3, 4, 5, 6], '내부 선이 있는 정사각형·직사각형·별·팔각형과 대각선 예다. 조각 수와 각 조각의 넓이는 각각 확인한다.')],
    '1598479047541': [([1, 2, 3, 4, 5, 6], '1598473604631과 파일 해시가 일치하는 내선 도형 여섯 쪽이다.')],
    '1598479079221': [([1, 2, 3, 4, 5, 6, 7], '내부 선이 없는 윤곽이다. 선이 없는 상태에서 조각 개수나 등분 여부를 정하지 않는다.')],
    '1612914605331': [([1, 2, 3], '가로 눈금선이 있는 세 조리법이다. 파랑은 물이다. 세 번째는 한 눈금의 절반을 단위로 쓰면 막대 높이를 정수 단위로 나타낼 수 있다.')],
    '1612914628562': [([1, 2, 3], '가로 눈금선은 없지만 세 조리법의 색 막대 길이와 순서는 눈금선이 있는 판과 같다.')],
    '1612914658870': [([1], '세 조리법의 정답은 각각 선택지 1·2·3이다. 막대의 주스 대 전체 비율과 대조했다.')],
    '1621005972366': [([1], '소수 카드의 .13과 .88은 합이 1.01이다. 1/8과 7/8을 소수 둘째 자리까지 각각 반올림한 값으로 해석할 수 있다.')],
    '1621006009477': [([1], '1/8과 7/8 등 합이 1이 되는 두 분수를 짝지었다. 두 장을 합친 수와 각 카드에 적힌 수를 구별한다.')],
    '1621006220990': [([1], '단위분수와 단위분수가 아닌 카드의 정렬 예다.'),
                       ([2], '1/4·1/2·3/4에 눈금이 있고 1/3·2/3은 수를 적은 위치다. 2/3에 대응한 소수는 .66이다.'),
                       ([3], '반을 나타낸 카드 하나를 2/4로 바꾼 예로 기본 분수 카드의 실제 목록과 다르다.'),
                       ([4, 5, 6], '소수·비·백분율 카드 정렬 예다. .67과 67%는 각각 반올림값이다.'),
                       ([7], '2/3에 .67과 66%가 함께 적혀 있다. 정확한 2/3과 근삿값을 구별하고 자리별 반올림 규칙을 통일한다.')],
    '1628876472138': [([1], '13%와 88%를 더하면 101%다. 정확한 보수와 각각을 반올림한 정수 백분율을 구별한다.')],
    '1628876491726': [([1], '두 수의 비교에서 기준량을 확인한다. 예를 들어 카드의 1:8과 7:8은 각각 전체 8에 대한 비교일 때 1/8과 7/8이다.')],
}

IMAGE_NOTES = [
    ([2, 3, 11, 12], '같거나 유사한 개와 색 블록 그림이다. 이미지에 보이는 물건 수가 활동에서 사용한 양이나 크기를 뜻하지 않는다.'),
    ([7, 8, 9, 10, 13, 14, 17, 22], '풍선, 조각과 퀼트, 분수 카드의 예다. 13은 육각형의 여러 분할, 14는 같은 색과 모양의 여러 타일, 17은 분수 카드 예다. 22는 인쇄물 미리보기다.'),
    ([0, 1, 4, 5, 6, 15, 16, 18, 19, 20, 21, 23, 24, 25, 26], '책 표지, 놀이 장면, 간식과 재료 그림이다. 사진 한 장으로 등분의 실제 넓이, 학생의 답이나 영상 전체를 판단하지 않는다.'),
]

CLAIMS = [
    ('LT106', ['6수01-06','6수01-12','6수02-03'], ['1621005972366','1621006009477','1628876472138'], [17],
     '1/8과 7/8의 정확한 소수는 0.125와 0.875로 합이 1이다. 인쇄 카드의 반올림값 0.13과 0.88을 합하면 1.01이다.',
     '각 항목을 반올림한 결과와 전체를 먼저 합한 결과를 구별한다. 13%와 88%도 정확한 보수의 합을 나타내지 않는다.'),
    ('LT107', ['4수01-10','4수01-11','6수01-12','6수02-03'], ['1592931128145','1592931154889','1592931190914','1621006220990'], [],
     '수직선에서 0과 1, 간격, 눈금선과 숫자 표기를 구별한다. 2/3에 적힌 .66, .67, 66%는 자릿수와 표현을 통일해 해석한다.',
     '정확한 2/3은 유한소수 .66이나 .67과 같지 않다. 반올림해 정수 백분율로 나타내면 약 67%다.'),
    ('LT108', ['6수02-02','6수02-03','6수02-04'], ['1612914605331','1612914628562','1612914658870'], [],
     '두 판의 세 조리법에서 색 막대의 상대적 높이가 같다. 세 정답은 주스와 물 양을 각각 같은 배율로 바꾼 선택지 1·2·3이다.',
     '파랑은 물이다. 기준을 물로 두는 비와 주스·물을 합한 전체에 대한 주스 비율을 구별한다.'),
    ('LT109', ['4수01-09','6수03-13'], ['1598473604631','1598479079221'], [9,13,14],
     '같은 윤곽에 내부 선이 있는 도형과 없는 도형을 비교한다. 조각 수만 세지 않고 분수의 기준 전체와 단위 넓이를 확인한다.',
     '내선이 있는 도형에서도 각 칸이 같은 넓이인지는 별도로 확인한다. 다른 도형의 조각 한 장을 같은 단위로 간주하지 않는다.'),
]

OBSERVATIONS = [
    dict(id='LT-P97', standard_codes=['6수01-06','6수01-12','6수02-03'],
         question='전체를 1/8과 7/8로 나눴다. 각각 정확한 소수로 바꿔 더하라. 소수 둘째 자리까지 각각 반올림한 뒤 더하면 얼마인가?',
         expected='정확한 값 0.125와 0.875의 합은 1이다. 각각 반올림한 0.13과 0.88의 합은 1.01이다.',
         interpretation='정확한 합과 각각의 반올림값을 더한 결과의 차이를 설명한다.', student_validated=False),
    dict(id='LT-P98', standard_codes=['4수01-10','4수01-11','6수01-12','6수02-03'],
         question='0과 1 사이의 2/3 위치에 .66과 .67이 적혀 있다. 2/3의 정확한 소수 표기와 소수 둘째 자리까지 반올림한 값, 정수 백분율로 반올림한 값을 각각 말하라.',
         expected='정확한 값은 0.666…이다. 소수 둘째 자리까지 반올림하면 0.67, 정수 백분율로 반올림하면 67%다.',
         interpretation='순환하는 값의 점 위치와 근삿값을 구별한다. 66%가 같은 반올림 규칙에서 나온 값인지 확인한다.', student_validated=False),
    dict(id='LT-P99', standard_codes=['6수02-02','6수02-03','6수02-04'],
         question='기준 조리법은 주스 6과 물 4다. 가는 주스 3과 물 2, 나는 주스 5와 물 1, 다는 주스 5와 물 4다. 어느 것이 같은 비인가? 가의 주스 대 물의 비와 전체에 대한 주스 비율을 각각 말하라.',
         expected='가는 두 재료를 모두 절반으로 줄였으므로 같은 비다. 주스 대 물은 3:2, 전체에서 주스는 3/5다.',
         interpretation='한 재료의 양이 같은 선택지와 두 재료를 같은 배율로 바꾼 선택지를 구별한다.', student_validated=False),
    dict(id='LT-P100', standard_codes=['4수01-09','6수03-13'],
         question='같은 넓이의 정사각형 12개로 만든 직사각형에 내부 선을 그었다. 여섯 칸씩 나누면 각각 전체의 얼마인가? 내부 선을 지운 그림에서 임의로 그은 선이 반으로 나누는지는 어떻게 확인하는가?',
         expected='각 부분은 6칸으로 전체의 절반이다. 눈금을 다시 표시해 같은 크기 단위로 넓이를 비교하거나 잘라 옮겨 빈틈과 겹침 없이 같은 넓이임을 설명한다.',
         interpretation='내부 선이 표시된 상태에서 센 값과 선이 없는 상태에서 직접 만든 넓이 단위를 구별한다.', student_validated=False),
]


def verify_fraction_values():
    preliminary = load(CACHE / 'preliminary-fraction-assets-review.json')
    juice = preliminary['juice']
    shares = [[str(Fraction(j, j+w)) for j,w in recipe] for recipe in juice['values']]
    matches = [[i for i in range(1,4) if row[i] == row[0]] for row in shares]
    assert shares == juice['shares'] and matches == juice['matching_options'] == [[1],[2],[3]]
    answer_text = (CACHE / '1612914658870.txt').read_text(encoding='utf-8')
    assert re.findall(r'Option (\d)', answer_text) == ['1','2','3']
    line = (CACHE / '1621006220990.txt').read_text(encoding='utf-8')
    pages = re.split(r'=== PDF PAGE \d+ ===', line)[1:]
    assert len(pages) == 7 and '.66' in pages[1] and '.67' in pages[6] and '66%' in pages[6]
    assert Fraction(1,8) + Fraction(7,8) == 1
    assert Decimal('.13') + Decimal('.88') == Decimal('1.01')
    return dict(juice=juice, discrepancies=preliminary['discrepancies'])


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
    assert len(raw_pdfs) == len(PDF_NOTES) == 14 and len(raw_images) == 27
    pdfs, images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images)
    studies = {}
    for sid in (HAMDAN, BOYER):
        study = registry['sources'][sid]
        assert study['snapshot_file'] == notes_file(sid) and study['snapshot_sha256'] == sha(ROOT / notes_file(sid))
        url = study['display']['url']
        linking_activity = next(r['linking_page'] for r in prior['fractions_cited_works_pending'] if r['url'] == url)
        studies[sid] = dict(url=url, linking_activity=linking_activity, snapshot_file=study['snapshot_file'],
                            snapshot_sha256=study['snapshot_sha256'])
    assert asset_pairs(pdfs) == linked_pairs(prior['fractions_pdf_urls_not_reviewed'])
    assert asset_pairs(images) == linked_pairs(prior['fractions_image_urls_not_reviewed'])
    all_pdfs = prior['supplementary_pdf_read_manifest'] + pdfs
    all_images = prior['image_read_manifest'] + images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (108, 319)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (97, 296)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (705, 684)
    assert len({a['sha256'] for a in images}) == 26
    names = {a['url'].rsplit('/', 1)[-1].removesuffix('.pdf'): a['url'] for a in pdfs}
    values = verify_fraction_values()
    assert len({a['sha256'] for a in pdfs if a['url'] in {names['1598473604631'], names['1598479047541']}}) == 1

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
                 supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
                 supplementary_pdf_coverage=dict(urls=108, page_occurrences=319, distinct_sha256_files=97,
                                                 pages_after_file_deduplication=296, all_selected_pages_visual_reviewed=True,
                                                 whole_site_attachment_review=False),
                 pdf_exact_reuse_groups=reuse_groups(all_pdfs), fractions_image_exact_reuse_groups=reuse_groups(images),
                 fractions_pdf_urls_not_reviewed={}, fractions_image_urls_not_reviewed={},
                 fractions_cited_works_pending=[], fractions_external_studies=studies,
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=27, supplementary_pdf_urls=14),
                 fractions_pdf_reading_log=pdf_notes, fractions_image_reading_log=image_notes, fractions_checked_values=values,
                 pdf_reading_log={**prior['pdf_reading_log'], **{
                     url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows]
                     for url, rows in pdf_notes.items()}},
                 reading_log=prior['reading_log'] + ['분수 활동의 LT2 PDF 14개·40쪽과 삽입 이미지 27개 URL을 대조했다. 수직선과 비율 원연구는 별도로 등록했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='fraction_printed_rounding_and_scale', locations=[names[n] for n in ('1621005972366', '1621006220990', '1628876472138', '1612914605331')],
                     action='반올림 전에 보수의 합, 같은 수직선 위치의 근삿값 표기, 색 막대의 기준량을 검산했다.')],
                 unread_followups=[LIMITS, '다음에는 규칙성·대수적 사고 활동의 영어 본문을 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
                  method_note='분수 카드와 수직선의 표기, 비율 자료의 정답과 근삿값, 그림을 대조했다.',
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
    print('Reviewed 14 LT2 PDFs, 40 pages and 27 images; added 4 mappings and 4 observations.')


if __name__ == '__main__':
    main()

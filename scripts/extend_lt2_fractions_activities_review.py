"""Record reviewed LT2 English activity procedures linked to fractions."""
import copy
from fractions import Fraction
from urllib.parse import urljoin, urlparse

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_multiplying_dividing_assets_review_notes.json'
PRIOR_SHA = '4a689c5e4f738eccac724e4d7ceb7983f9f3ea75bc3d0d952094db15849a6698'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_fractions_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-fractions-activities'
SCOPE = '분수 수준에 연결된 영어 활동 23개를 대조했다. 누적 공개 HTML은 765개이며 활동·교사자료 목록 824개 중 515개를 확인했고 309개가 남았다.'
LIMITS = '새 연결 PDF 14개와 삽입 이미지 27개 URL, 책·영상·인용 원연구의 후속 대조가 남아 있다. 자체 검산은 독립 검토와 학생의 실제 수행과 구별한다.'

READING = """
balloon-bundle|자르지 않는 풍선은 짝수 개일 때만 두 사람이 같은 수로 모두 받을 수 있다. 홀수의 절반이 수로 존재한다는 사실과 정수 개수 분배를 구별한다.
bernadettes-juice|주스와 물의 양을 같은 배율로 바꾼다. 주스 대 물의 비와 전체에 대한 주스 비율은 기준량이 다르다. 선택지와 정답표는 첨부 대조에 남긴다.
buried-treasure-stemie|모래 상자의 전체를 먼저 정하고 넓이가 같은 두 영역을 나눈다. 장난감 찾기는 기억이나 접근 방식의 영향도 받는다.
creating-3d-figures-using-fractions|직육면체를 두 정육면체로 정확히 채우면 한 조각은 부피의 절반이다. 두 조각의 겹침·빈틈과 변의 길이 절반을 구별한다.
feed-the-dog-fractions|같은 넓이의 원형 빵을 전제로 1/4 두 조각이 1/2 한 조각과 같다. 원판 크기가 다르면 빵의 실제 양을 따로 비교한다.
feed-the-dog-halves|직사각형의 가운데를 지나 변과 평행한 선이나 꼭짓점을 잇는 대각선으로 넓이가 같은 두 부분을 만든다. 두 조각이라는 사실만으로 절반을 판단하지 않는다.
fourths-and-thirds|타일 8개의 1/4은 2개, 9개의 1/3은 3개다. 도전의 두 가지 색과 세 등분을 구별하고 색이 반복돼도 경계를 확인한다.
fraction-as-symmetry|반사한 위치와 방향을 맞추어 선대칭을 만든다. 넓이가 같은 두 부분과 축에 대해 서로 겹치는 조건을 구별한다.
fractions-of-rectangles|같은 정사각형 6개는 3개씩 나눈다. 7개에서 불가능하다는 설명은 타일을 자르지 않는 조건이다.
freshly-baked-fractions|직사각형의 기준 넓이를 같게 해야 1/4 두 조각을 다른 판의 1/2과 직접 비교할 수 있다. 조각의 크기를 확인한다.
half-and-half|자르는 횟수와 부분의 크기를 구별한다. 사과를 한 번 잘라도 두 조각이 같은 양이어야 각각 절반이다.
hanging-fractions-on-a-number-line-fraction-integer-sequencer|0과 1을 공유하는 수직선에 같은 수의 분수·소수·백분율을 같은 위치에 둔다. 1:2를 1/2로 나타낼 때 비교하는 양과 기준량을 밝힌다.
how-many-eggs-half-recognizer|완성된 달걀 하나와 네 조각에서 맞는 두 쌍을 만들면 원래 세 개다. 모형이 맞물리는 것과 두 조각의 부피가 같은 조건을 구별한다.
marshmallow-munch-stemie|목표와 준비물은 두 사람에게 3개, 절차는 짝마다 1개를 준다. 처음 양에 따라 3/2개씩과 1/2개씩을 구별한다.
number-hop-fraction-crawl|0~1을 네 등분해 1/4 간격으로 옮긴다. 간격 수와 양 끝을 포함한 눈금 수를 구별한다. 지원 문구의 ²⁄?는 분모를 확정할 수 없다.
picture-pie-fraction-talk|중심을 지나게 접어 같은 넓이의 반원을 만든 뒤 다시 등분한다. 처음의 크기가 다르면 접기를 반복해도 원의 등분을 보장하지 않는다.
quilt-talk|같은 넓이 타일에서 색 타일 수와 전체 수를 센다. 한 타일의 색칠과 퀼트 전체에서의 색칠 넓이는 기준 전체가 다르다.
shape-fraction-combinations|육각형 하나를 전체로 두고 1/2+3/6과 2/6+2/3이 모두 1인지 확인한다. 합과 실제 배치를 구별한다.
shape-fractions|블록 크기가 다르면 파란 블록 수의 비율과 파란 넓이의 비율이 다를 수 있다. 내부 선이 나눈 조각의 넓이를 확인한다.
shape-puzzle-halves|모양이 달라도 두 조각의 넓이가 같을 수 있다. 겹치기가 가능한 예와 단위 넓이로 확인할 예를 나눈다.
share-the-cake|합동인 반쪽과 넓이는 같지만 모양이 다른 반쪽을 모두 인정한다. 전체를 빈틈과 겹침 없이 덮는지도 확인한다.
symmetric-halves|접기 전 예상과 접은 결과를 구별한다. 특정 선으로 접어 겹치지 않아도 다른 방식으로 같은 넓이 두 부분을 만들 수 있다.
there-arent-enough-cookies|같은 크기의 쿠키 두 개를 여섯 명에게 자를 수 있게 나누면 1인당 한 쿠키의 2/6, 곧 1/3이다. 처음 두 개를 전체로 하면 각자 1/6이다.
"""

CLAIMS = [
    ('LT100', ['4수01-09', '6수03-01', '6수03-02'], [2, 5, 7, 10, 15, 19, 20, 21],
     '같은 넓이의 반쪽, 두 조각의 합동, 특정 선에 대한 대칭을 구별한다. 다른 모양도 같은 넓이일 수 있다.',
     '겹치기 외에 단위 넓이 세기와 분해·재구성으로 반쪽을 확인할 수 있다.'),
    ('LT101', ['4수01-06', '4수01-09', '4수01-10'], [0, 8, 13, 22],
     '자르지 않는 풍선과 나눌 수 있는 같은 크기의 간식은 같은 사람 수에서도 나머지 처리가 다르다.',
     '처음 양을 먼저 확인하고 정수 나머지와 그 나머지를 등분한 양을 구별한다.'),
    ('LT102', ['4수01-09', '4수01-15', '6수01-06', '6수03-19'], [3, 4, 6, 9, 12, 17],
     '기준 전체를 고정하고 단위분수의 합을 확인한다. 입체의 결합 가능성과 부피의 등분을 따로 확인한다.',
     '동치인 분수와 서로 다른 전체에서 떼어 낸 실제 양을 구별한다.'),
    ('LT103', ['4수01-10', '4수01-11', '6수01-06', '6수01-12'], [11, 14],
     '0과 1 사이의 단위분수 간격을 반복한다. 1/2과 2/4는 같은 점이며 같은 단위에서 소수와도 대응한다.',
     '눈금의 수와 움직인 간격 수를 나누고, 분모가 빠진 예는 확정하지 않는다.'),
    ('LT104', ['6수02-02', '6수02-03', '6수02-04'], [1, 11],
     '같은 비를 만들려면 주스와 물을 같은 배율로 바꾼다. 주스가 전체에서 차지하는 비율의 기준량은 혼합물 전체다.',
     '주스 대 물이 1:2라면 전체 중 주스는 1/3이다. 비의 뒤 수를 언제나 전체로 읽지 않는다.'),
    ('LT105', ['4수01-09', '6수02-03', '6수03-13'], [6, 16, 18],
     '타일 장수 비율과 색이 덮은 넓이 비율은 다른 양이다. 같은 넓이의 타일을 한 장씩 셀 때 두 값이 일치한다.',
     '블록 크기가 다르거나 일부만 색칠한 타일은 한 장씩 세어 넓이를 구할 수 없다.'),
]

OBSERVATIONS = [
    dict(id='LT-P91', standard_codes=['4수01-09', '6수03-01', '6수03-02'],
         question='가로 4칸, 세로 3칸인 같은 크기 격자에서 왼쪽 위의 3×2 직사각형을 떼었다. 두 조각은 각각 전체의 얼마이며, 움직여 정확히 겹칠 수 있는가?',
         expected='둘 다 6칸으로 전체의 1/2이다. 하나는 직사각형이고 다른 하나는 꺾인 모양이므로 합동이 아니고 접어서도 겹치지 않는다.',
         interpretation='넓이가 같다는 근거와 합동·대칭의 근거를 따로 묻는다.', student_validated=False),
    dict(id='LT-P92', standard_codes=['4수01-06', '4수01-09', '4수01-10'],
         question='같은 크기 간식 3개를 두 사람이 같은 양으로 나눈다. 자르지 않을 때와 잘라 모두 나눌 때의 한 사람 몫과 나머지를 각각 말하라.',
         expected='자르지 않으면 1개씩 받고 1개가 남는다. 자르면 남은 것을 반씩 받아 1과 1/2개씩 받으며 남는 양은 없다.',
         interpretation='처음 수를 고정하고 나눌 수 있는 단위와 나머지 처리만 바꾸어 비교한다.', student_validated=False),
    dict(id='LT-P93', standard_codes=['4수01-09', '4수01-15', '6수01-06'],
         question='넓이가 12칸인 판의 1/4 조각 두 개를 모았다. 그 판의 얼마인가? 넓이가 8칸인 다른 판의 1/2 조각과 실제 넓이도 같은가?',
         expected='두 조각은 각각 3칸이므로 합이 6칸이고 그 판의 2/4, 즉 1/2이다. 다른 판의 1/2은 4칸이다.',
         interpretation='같은 수인 분수와 전체가 다른 두 조각의 실제 넓이를 구별한다.', student_validated=False),
    dict(id='LT-P94', standard_codes=['4수01-10', '4수01-11', '6수01-06', '6수01-12'],
         question='0부터 1까지를 네 등분했다. 0에서 두 간격을 움직이면 얼마인가? 이 점을 1/2과 0.5로 부를 수 있는 까닭을 설명하라. 양 끝을 포함한 눈금은 몇 개인가?',
         expected='1/4을 두 번 이동해 2/4에 도착한다. 전체의 절반인 같은 점이 1/2이고 0.5다. 눈금은 다섯 개다.',
         interpretation='같은 전체 단위에서 분수의 동치를 설명하고 간격과 눈금을 구별한다.', student_validated=False),
    dict(id='LT-P95', standard_codes=['6수02-02', '6수02-03', '6수02-04'],
         question='주스 2컵과 물 3컵을 섞는다. 주스 4컵으로 같은 맛의 비를 유지하려면 물은 몇 컵인가? 주스 대 물의 비와 전체에서 주스가 차지하는 백분율을 각각 말하라.',
         expected='물도 두 배인 6컵이다. 주스 대 물은 2:3이며, 전체에서 주스는 2/5이므로 40%다.',
         interpretation='물을 기준으로 할 때와 혼합물 전체를 기준으로 할 때의 양을 각각 가리킨다.', student_validated=False),
    dict(id='LT-P96', standard_codes=['4수01-09', '6수02-03', '6수03-13'],
         question='보라색 타일 두 장은 각각 1제곱센티미터이고 흰색 한 장은 4제곱센티미터다. 타일 전체에서 보라색의 장수 비율과, 겹치지 않게 놓았을 때 넓이 비율은 각각 얼마인가?',
         expected='장수는 세 장 중 두 장이므로 2/3이다. 넓이는 6제곱센티미터 중 2제곱센티미터이므로 1/3이다.',
         interpretation='분모의 단위를 구별한다. 같은 넓이의 타일만 쓰면 두 비율이 같아지는 까닭을 설명한다.', student_validated=False),
]


def verify_examples(bodies):
    text = [r['body'] for r in bodies]
    assert 'three marshmallows' in text[13] and 'one marshmallow' in text[13]
    assert '²⁄?' in text[14] and '0 and 1 line up' in text[14]
    assert 'not perfectly equal in size' in text[12]
    assert 'shapes can’t be halves' in text[19] and 'that are not the same shape' in text[20]
    assert 2 * Fraction(1, 4) == Fraction(1, 2) and Fraction(2, 6) + 2 * Fraction(1, 3) == 1
    assert Fraction(2, 3) == Fraction(4, 6) and Fraction(2, 5) * 100 == 40
    assert Fraction(3, 2) == 1 + Fraction(1, 2)
    return dict(marshmallow_possible_starting_counts=[1, 3], marshmallow_quotients=['1/2', '3/2'],
                ratio_reference=dict(juice_to_water=[2, 3], juice_share='2/5', juice_percent=40),
                number_line=dict(unit=[0, 1], intervals=4, ticks=5, unresolved_source_denominator=True),
                unequal_shape_halves=dict(whole_grid=[3, 4], rectangular_part=[2, 3], equal_areas=[6, 6]))


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
    pages, bodies, selected = [load(CACHE / name) for name in ('activity-manifest.json', 'english-bodies.json', 'selection.json')]
    followup = copy.deepcopy(prior['activity_followup_catalog'])
    assert selected == [row for row in followup['records'] if not row['body_read']
                        and any('/math/fractions/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|', 1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 23
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/', 1)[-1] for row in pages] == [row[0] for row in reading]
    examples = verify_examples(bodies)

    old_images = {row['url'] for row in prior['image_read_manifest']}
    old_pdfs = {row['url'] for row in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for page, body, (_, note) in zip(pages, bodies, reading):
        url = page['url']
        assert page['status'] == 200 and page['final_url'] == url and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256'] and '\nActivity\n' in body['body']
        assert 'Type:\nTeacher Resources' not in body['body']
        groups['activities'].append(page['key'])
        logs.append(dict(url=url, page_kind='activity_procedure', note=note))
        linked_images = {urljoin(url, image['src']) for image in page['images'] if '/upload/' in image.get('src', '')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert len({url for links in images.values() for url in links}) == 27
    assert len({url for links in pdfs.values() for url in links}) == 14
    assert {k: len(v) for k, v in groups.items()} == dict(general=6, domain_overviews=20, levels=224, activities=499, teacher_resources=16)
    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key', 'url', 'title', 'sha256', 'status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 765
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'], followup['listed_body_pending']) == (515, 309)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
                 observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
                 catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies': 515, 'pending_activity_bodies': 309},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=23, teacher_resources=0, inline_images=0, supplementary_pdf_urls=0),
                 fractions_reading_log=logs, completed_fractions_records=selected,
                 fractions_pdf_urls_not_reviewed=pdfs, fractions_image_urls_not_reviewed=images,
                 fractions_procedure_scope=dict(activity_procedures=23, teacher_resources=0),
                 fractions_checked_examples=examples,
                 fractions_cited_works_pending=[
                     dict(linking_page=pages[1]['url'], url='https://doi.org/10.1037/a0039010', read_scope='서지와 공개 초록 확인'),
                     dict(linking_page=pages[14]['url'], url='https://doi.org/10.1037/dev0000252', read_scope='저자 공개 PDF 확보, 후속 독립 등록 대기'),
                 ],
                 reading_log=prior['reading_log'] + ['분수 수준에 연결된 영어 활동 23개의 목표·절차·준비물과 교사 지원을 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='fraction_whole_equipartition_and_scale', locations=[pages[i]['url'] for i in (0, 1, 9, 12, 13, 14, 18, 19, 20, 22)],
                     action='처음 전체와 자르는 단위, 넓이와 합동, 분모와 기준량, 수직선 눈금과 간격을 구별했다.')],
                 unread_followups=[LIMITS, '분수 활동의 첨부와 연결된 원연구를 먼저 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
                  method_note='영어 목표와 절차에서 기준 전체, 분할 단위, 동치와 실제 크기, 비와 수직선을 대조했다.',
                  editorial_action='문헌 대응 6건과 자체 관찰 과제 6개를 추가했다.', observations=source['observations'] + OBSERVATIONS)
    for cid, codes, indices, support, limit in CLAIMS:
        registry['claims'].append(dict(id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
                                       locations=[pages[i]['url'] for i in indices], support=support, does_not_establish=limit,
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
    print('Reviewed 23 English activities; added 6 mappings and 6 observations. Public activity bodies pending: 309.')


if __name__ == '__main__':
    main()

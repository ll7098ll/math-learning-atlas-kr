"""Record the LT2 English activities linked to multiplication and division."""
import copy
from urllib.parse import urljoin, urlparse

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_subitizing_assets_review_notes.json'
PRIOR_SHA = '96490edda8dbec42b7383441d9a259e98f776a5604a0c6ea555f2ef65d915ac0'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_multiplying_dividing_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-multiplying-dividing-activities'
SCOPE = (
    '곱셈·나눗셈 수준에 연결된 영어 활동 21개의 본문을 대조했다. '
    '누적 공개 HTML은 742개이며, 활동·교사자료 목록 824개 중 492개를 확인했고 332개가 남았다.'
)
LIMITS = (
    '새 삽입 이미지 23개 URL과 영상·읽기 책·인용 연구 원문은 후속 대조 범위다. '
    '본문에 언급된 격자·준비물이 실제 다운로드 링크로 제공되는지는 별도로 확인한다. '
    '지시의 수정과 자체 발문을 수업 효과나 독립 검토·학생 응답으로 집계하지 않는다.'
)

READING = """
animal-legs--concrete-modeler-|네 발인 동물 그림을 같은 조건으로 1~3마리 그린다. 한 마리당 4개와 다리 전체 4·8·12를 구별한다.
animal-legs-partitive-divisor|수준명은 등분제 나눗셈을 가리키지만 실제 예시는 마릿수로 다리 전체를 구한다. 같은 크기 모임의 수, 한 모임의 크기와 전체 중 무엇을 알고 있는지 먼저 정한다.
biscuits-baby|과자 12개를 두 인형에게 6개씩 주었다가 세 인형에게 4개씩 다시 준다. 먼저 받은 두 인형이 각각 2개를 내면 새 인형에게 4개가 된다.
brownie-arrays|100칸의 10×10 격자를 네 개의 5×5 배열로 나눌 수 있다. 준비물의 10 x0 10 표기는 본문의 10×10과 어긋난다. 각 배열이 같은 수인지와 한 격자에 나머지 없이 들어가는지를 따로 본다.
buying-candy-bars|한 개가 1달러라는 가정에서 지폐 수와 돈의 액수를 구별한다. 본문의 나와 친구 한 명·두 명은 각각 두 사람·세 사람이다. 전체를 고정하고 나누는 단위와 나머지 처리에 따라 몫을 해석한다.
buying-candy-bars-concrete-modeler|1·5·10달러 지폐의 장수와 총액, 개당 1달러일 때 살 수 있는 개수를 따로 답한다. 같은 액면끼리 묶어 센다.
caps-for-sale-how-much|활동에서 정한 모자 한 개당 9달러를 사용한다. 주인 모자를 제외하면 16개 144달러, 포함하면 17개 153달러다. 9달러는 예시의 가정으로 기록한다.
extra-extra|두 개를 한 짝으로 만들고 세 번째가 남는다. 물건 두 개라는 수 조건과 좌·우나 크기가 맞는 실제 장갑 한 켤레라는 조건을 구별한다.
feeding-time-at-the-zoo|나누기 전에 한 마리가 받을 수를 예상하고 실제로 나눈 뒤 센다. 최소 6개씩 준비하라는 조건은 전체를 모두 나머지 없이 나눌 수 있다는 보장이 아니다.
how-many-carton-sets|열 개씩 들어가는 상자에 30개면 세 상자다. 도입 준비량 10~30개와 뒤의 40·50개 도전은 구별하며 실물로 하는 경우 추가 재료를 준비한다.
how-many-eggs-concrete-modeler|10개씩 두 상자·세 상자를 전체 세기, 10씩 세기, 곱셈으로 나타낸다. 지원을 위해 상자마다 5개만 넣으면 자리 수 10과 실제 묶음 크기 5가 다르다.
is-it-fair-stemie|과일 조각 여덟 개를 두 사람이 4개씩 받는다. 여기서 공평은 조각 수에 한정하며 조각 크기나 먹는 양을 같다고 단정하지 않는다.
multiplication-relation|2×5에서 한 인수만 세 배가 되어 6×5가 되면 곱도 세 배다. 두 인수를 모두 세 배로 바꾸는 경우의 곱과 구별한다.
read-aloud-bean-thirteen-concrete-modeler--|책의 사건에 맞춰 콩 13개를 옮긴다. 웹 안내에 모든 장면의 인원수와 몫이 열거되어 있지 않아 책과 영상의 대조는 별도로 남긴다.
read-aloud-quack-and-count-concrete-modeler--|새끼 오리 전체는 일곱이다. 전체를 다시 세는 활동과 한 부분이 3이면 다른 부분이 4임을 설명하는 활동을 나눈다.
shared-story-two-of-everything|네 개를 넣고 두 배로 만들면 여덟이다. 두 배와 두 개 더하기를 구별한다. 본문 괄호의 2017과 참고문헌 및 DOI 등록의 2021이 다르다.
sharing-food-with-friends-beginning-grouper-and-distributive-sharer|모두가 하나 이상 받았는지와 모두가 같은 수를 받았는지는 다른 조건이다. 한 사람씩 주는 지원 전후를 따로 기록한다.
tea-party-sharing|준비한 전체, 참여한 사람, 이미 받은 사람을 구별한다. 모두에게 주는 것부터 관찰하며 기본 절차는 수가 같은 분배를 요구하지 않는다.
tiling-tetrominoes-deriver-x|한 종류의 조각을 여러 개 복사한다. 8×12=96칸을 4칸씩 덮으려면 24개가 필요하다. 개수의 필요조건과 실제로 빈틈없이 맞추는 조건을 따로 확인한다.
time-to-eat-stemie|스스로 나누는 반응과 교사의 발문 뒤의 반응을 구별한다. 같은 수로 나누기와 참여·운동·언어 지원을 별도로 기록한다.
wake-up-sleeping-giants-multiplyingdividing|주사위 2·5·6에서 (6÷2)×5=15는 맞다. 1과 5를 각각 뒤집기와 10의 카드 한 장을 뒤집기, 남은 주사위 값 6을 카드로 쓰기는 서로 다른 규칙이다.
"""

CLAIMS = [
    ('LT92', ['2수01-10', '2수01-11', '4수02-01'], [0, 1, 5, 6, 10, 12, 15],
     '한 동물당 다리 수, 모자 하나의 가격, 상자 한 개에 든 수처럼 묶음의 크기를 고정하고 묶음 수를 바꾼다. 한 인수만 세 배면 곱도 세 배다.',
     '동물이나 물건의 한 묶음 크기가 같다는 조건을 먼저 확인한다. 일정한 수를 더하는 변화와 곱셈적인 변화를 구별한다.'),
    ('LT93', ['4수01-05'], [1, 2, 4, 8, 9, 10, 11, 16, 17, 19],
     '전체와 묶음 수를 알 때 한 몫을 구하는 질문과 전체와 한 묶음의 크기를 알 때 묶음 수를 구하는 질문을 구별한다. 예상·실제 분배·검산을 나눠 기록한다.',
     '한 사람도 빠뜨리지 않은 상태가 같은 몫을 보장하지 않는다. 준비물의 최소량, 나머지 없이 나뉘는 수, 나눌 수 있는 단위를 구별한다.'),
    ('LT94', ['4수01-05', '4수01-06', '6수02-01'], [2, 4, 7, 13],
     '전체 수가 일정할 때 받는 사람 수와 한 사람 몫을 함께 바꿔 비교한다. 자르지 않는 물건의 몫은 서로 다른 사람 수에서도 같을 수 있으며 나머지는 달라질 수 있다.',
     '전체를 고정하지 않거나 자를 수 있는 단위로 바꾸면 비교 조건도 달라진다. 두 묶음 크기를 보고 곧바로 반비례를 일반화하지 않는다.'),
    ('LT95', ['4수01-04', '4수01-05', '6수03-13'], [3, 18],
     '10×10 배열을 네 개의 5×5 배열로 나누거나 8×12 격자에서 4칸 조각의 개수를 구한다. 조각 수를 구한 뒤 겹침과 빈칸이 없는 배치를 확인한다.',
     '넓이를 4로 나눈 몫이 정수인 것은 배치의 필요조건이다. 특정 조각의 방향과 자리까지 점검해야 하며 모든 조각이 맞는다는 결론은 얻지 않는다.'),
    ('LT96', ['4수01-05', '6수01-01'], [12, 20],
     '식을 계산하는 규칙, 쓸 주사위 눈의 범위, 계산 결과를 카드로 바꾸는 규칙을 따로 합의한다. 나눗셈을 포함한 식의 값은 괄호와 연산 순서에 맞춰 확인한다.',
     '15가 한 장인지 1·5 두 장인지와 남은 6을 쓸 수 있는지는 계산 결과에서 결정되지 않는다. 정한 규칙을 두 예시에 똑같이 적용한다.'),
]

OBSERVATIONS = [
    dict(id='LT-P83', standard_codes=['2수01-10', '2수01-11', '4수02-01'],
         question='네 발인 동물 그림이 두 마리에서 여섯 마리로 늘어난다. 다리 전체는 각각 몇 개이고 몇 배가 되는가? 여섯 마리 중 한 마리가 두 발인 새라면 전체는 몇 개인가?',
         expected='모두 네 발이면 8개에서 24개가 되어 세 배다. 새 한 마리가 섞이면 4×5+2=22개다.',
         interpretation='마릿수와 한 마리당 다리 수를 구별하고 같은 크기의 묶음이라는 조건이 바뀔 때 계산도 바꾼다.', student_validated=False),
    dict(id='LT-P84', standard_codes=['4수01-05'],
         question='과자 12개를 두 사람에게 같은 수로 주면 한 사람당 몇 개인가? 12개를 6개씩 봉지에 넣으면 봉지는 몇 개가 필요한가? 두 식에서 2와 6이 무엇을 뜻하는지 말하라.',
         expected='앞의 12÷2=6에서는 2가 사람 수, 6이 한 사람의 몫이다. 뒤의 12÷6=2에서는 6이 한 봉지의 과자 수, 2가 봉지 수다.',
         interpretation='같은 12를 써도 무엇을 세고 무엇을 구하는지 말한다. 과자를 하나씩 나눠 주는 방법과 6개씩 묶는 방법을 비교한다.', student_validated=False),
    dict(id='LT-P85', standard_codes=['4수01-05', '4수01-06', '6수02-01'],
         question='자르지 않는 과자 5개를 세 사람에게 같은 수로 주고 가능한 많이 나눠 준다. 네 사람에게 주면 한 사람 몫은 줄어드는가? 두 경우 각각 몇 개가 남는가?',
         expected='세 사람일 때에도 네 사람일 때에도 한 사람 몫은 1개다. 세 사람에게 줄 때 2개, 네 사람에게 줄 때 1개가 남는다.',
         interpretation='사람 수가 늘어도 정수 몫이 항상 엄격하게 감소하지 않음을 설명한다. 남는 수를 정수 몫과 함께 본다.', student_validated=False),
    dict(id='LT-P86', standard_codes=['4수01-04', '4수01-05', '6수03-13'],
         question='8행 12열 격자의 단위 칸을 한 조각에 4칸씩 덮으려 한다. 빈틈없이 덮을 수 있다면 조각이 몇 개 필요한가? 2×2 정사각형 조각으로 가능함을 배열로 설명하라.',
         expected='전체는 96칸이므로 24개가 필요하다. 두 행과 두 열씩 나누면 정사각형 조각이 4행 6열로 배치되어 정확히 덮인다.',
         interpretation='96÷4=24에서 얻는 개수와 실제 놓는 위치를 따로 설명한다. 다른 4칸 조각의 배치를 같은 계산만으로 판정하지 않는다.', student_validated=False),
    dict(id='LT-P87', standard_codes=['4수01-05', '6수01-01'],
         question='주사위 눈은 2·5·6이고 계산 결과와 같은 수가 적힌 카드만 한 장 뒤집을 수 있다. 카드가 1~10이라면 (6÷2)×5의 결과로 뒤집을 수 있는 카드가 있는가? 눈을 두 개만 써도 된다면 2×5는 어떤 카드를 뒤집는가?',
         expected='첫 식은 15이므로 해당 카드가 없다. 눈 두 개만 쓰는 조건에서 2×5는 10이므로 10 카드 한 장을 뒤집는다. 남은 눈 6은 이 식의 값이 아니다.',
         interpretation='계산의 정당성과 놀이 규칙을 따로 설명한다. 결과의 자릿수를 따로 읽는 변형에서는 카드 선택이 어떻게 바뀌는지 묻는다.', student_validated=False),
]


def verify_examples(bodies):
    text = [r['body'] for r in bodies]
    assert '10 x0 10 array' in text[3] and '10 x 10 array' in text[3]
    assert 'two groups' in text[4] and 'three groups' in text[4]
    assert '10 to 30' in text[9] and '40 eggs, 50 eggs' in text[9]
    assert 'Smith et al., 2017' in text[15] and 'A. Smith. (2021)' in text[15]
    assert 'a single tetromino' in text[18] and 'many copies' in text[18]
    assert 'the numerals 1 and 5' in text[20] and 'the 10 and the 6' in text[20]
    assert (12 // 2, 12 // 3) == (6, 4) and (divmod(5, 3), divmod(5, 4)) == ((1, 2), (1, 1))
    assert (16 * 9, 17 * 9) == (144, 153) and 8 * 12 // 4 == 24
    assert (6 // 2) * 5 == 15 and 15 not in range(1, 11) and 2 * 5 == 10
    square = ('AAAB', 'CABB', 'CCDB', 'CDDD')
    for tag in 'ABCD':
        cells = {(x, y) for y, row in enumerate(square) for x, value in enumerate(row) if value == tag}
        assert len(cells) == 4
        assert sorted(sum(abs(x - u) + abs(y - v) == 1 for u, v in cells) for x, y in cells) == [1, 1, 1, 3]
    assert (8 // 4) * (12 // 4) * 4 == 24
    return dict(four_t_tetrominoes_square=list(square), repeated_blocks=[2, 3],
                equal_share_fixed_total=5, quotients=[1, 1], remainders=[2, 1],
                sleeping_giants=dict(dice=[2, 5, 6], computed_value=15, one_card_available=False))


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
                        and any('/math/multiplying-dividing/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|', 1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 21
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
    assert len({url for links in images.values() for url in links}) == 23
    assert len({url for links in pdfs.values() for url in links}) == 0
    assert {k: len(v) for k, v in groups.items()} == dict(general=6, domain_overviews=20, levels=224, activities=476, teacher_resources=16)
    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key', 'url', 'title', 'sha256', 'status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 742
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'], followup['listed_body_pending']) == (492, 332)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
                 observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
                 catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies': 492, 'pending_activity_bodies': 332},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=21, teacher_resources=0, inline_images=0, supplementary_pdf_urls=0),
                 multiplying_dividing_reading_log=logs, completed_multiplying_dividing_records=selected,
                 multiplying_dividing_pdf_urls_not_reviewed=pdfs, multiplying_dividing_image_urls_not_reviewed=images,
                 multiplying_dividing_procedure_scope=dict(activity_procedures=21, teacher_resources=0),
                 multiplying_dividing_checked_examples=examples,
                 multiplying_dividing_cited_works_pending=[
                     dict(linking_page=pages[9]['url'], url='https://doi.org/10.1007/978-981-10-7153-9_14', read_scope='출판사 공개 초록과 서지, 같은 장의 본문은 후속 대조'),
                     dict(linking_page=pages[15]['url'], url='https://doi.org/10.5951/MTLT.2020.0298', read_scope='Crossref 등록일 2021년 11월, 본문 대조 대기'),
                 ],
                 reading_log=prior['reading_log'] + ['곱셈·나눗셈 수준에 연결된 영어 활동 21개의 목표·절차·준비물과 교사 지원을 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='multiplication_and_division_procedure_conflicts', locations=[pages[i]['url'] for i in (1, 3, 4, 9, 15, 18, 20)],
                     action='묶음 수와 묶음의 크기, 몫과 나머지, 배열의 필요조건과 실제 배치, 계산과 카드 규칙을 구별했다.')],
                 unread_followups=[LIMITS, '삽입 이미지와 연결된 원연구를 대조하고 남은 분수 활동 본문을 검토한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
                  method_note='영어 목표와 절차의 단위, 전체 고정, 묶음 크기와 수, 나머지, 카드 규칙을 대조했다.',
                  editorial_action='문헌 대응 5건과 자체 관찰 과제 5개를 추가했다.', observations=source['observations'] + OBSERVATIONS)
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
    print('Reviewed 21 English activities; added 5 mappings and 5 observations. Public activity bodies pending: 332.')


if __name__ == '__main__':
    main()

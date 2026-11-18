"""Record the LT2 English activities linked to the subitizing trajectory."""
import copy
from urllib.parse import urljoin, urlparse

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_comparing_number_assets_review_notes.json'
PRIOR_SHA = 'bd0cdfa4c855c807a9861ba1001e3c6359bb73ed425048cfd1b031f2d9c34cfa'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_subitizing_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-subitizing-activities'
SCOPE = (
    '수량을 세지 않고 알아보는 수준에 연결된 영어 활동 31개의 본문을 대조했다. '
    '누적 공개 HTML은 721개이며, 활동·교사자료 목록 824개 중 471개를 확인했고 353개가 남았다.'
)
LIMITS = (
    '새 LT2 PDF 6개와 삽입 이미지 41개 URL, 두 주소가 가리키는 외부 학술대회 자료 1건, '
    '배열과 영아 수량 탐색의 인용 연구는 후속 대조 범위다. '
    '반응 시간으로 전략을 확정할 수 없으며 독립 검토와 학생 응답은 별도다.'
)

READING = '''
arrays-a-gateway-to-multiplication|흩어진 점과 배열을 각각 제시한다. 같은 크기 행의 개수와 한 행의 수를 말하게 하고 90도 돌렸을 때 행·열은 바뀌지만 전체는 같음을 설명한다.
board-games--small-numbers|주사위나 돌림판은 1~3점이고 0은 선택이다. 눈의 수와 말이 출발 칸 이후에 이동한 칸 수를 맞춘다.
chocolate-chips-to-5-perceptual-subitizer-to-5|2초 동안 본 뒤 최대 5초 생각하고 말·손가락·접시 가리키기로 답한다. 숨겼다가 다시 보여 확인한 답과 처음 답을 따로 기록한다.
concentration|준비·재료는 한쪽을 펼치고 다른 쪽을 덮는다. 목표에 적힌 양쪽 덮기는 변형과 가깝다. 같은 점 개수와 같은 배치, 기억한 위치를 구별한다.
dice-movement-game-small-collection-namer|일반 주사위와 1~3점 지원용을 구별한다. 보인 점의 수를 말하는 것과 동작을 한 번씩 대응해 하는 수행을 따로 본다.
dice-race|두 십 주사위에서 2십과 3십, 낱개 주사위에서 4를 보았다면 합은 54다. 원문의 끝말 4와 합을 구별하고 노출 시간과 생각 시간을 따로 둔다.
fantastic-five-tricky-two|3·4·5의 그릇 중 5의 위치를 따라간다. 그릇과 내용물을 함께 옮길 조건을 명시하고 고른 위치와 들어 올린 뒤 파악한 수를 구별한다.
foxy-four-perceptual-subitizer-to-4|2·3·4에서 시작하지만 반복 절차에는 3·4·5가 있다. 손으로 표시한 수, 그릇의 위치를 기억한 답, 다시 본 답을 따로 기록한다.
get-the-number-maker-of-small-collections|최대 세 사람에게 한 물건씩 나누어 준다. 한 번에 다 가져오기와 사람별로 가져오기를 구별하고 들고 오는 지원 여부를 기록한다.
hearing-numbers-to-4|한 소리를 1~4번 들려준다. 소리를 다시 들려주기 전의 응답, 다시 들은 뒤 확인과 실제 사용한 세기 전략을 구별한다.
i-see-numbers-small-collection-namer|목표의 1~3과 일상 예시에서 언급한 5까지를 구별한다. 세어 말하기와 수 이름을 듣고 물건을 집는 반응을 따로 본다.
is-it|최대 3개의 모임을 5~7회 제시한다. 처음 정한 수인지의 응답과 모임에 실제로 든 수를 각각 기록한다.
knockout-conceptual-subitizer-to-10|색으로 각자 읽을 십 틀을 정한다. 각 틀에서 채운 수와 전체 자리 수를 구별하고 경쟁 변형의 응답 속도와 설명을 따로 본다.
make-groups-maker-of-small-collections|한 모임의 개수를 보고 같은 개수의 새 모임 하나를 만든다. 지원 문구의 모임 수와 절차에서 비교하는 모임 안의 물건 수를 구별한다.
naming-numbers|일상에서 0~5 수 이름을 쓰며 두 컵과 두 숟가락을 맞춘다. 수 이름이나 물건의 종류가 달라도 개수의 기준은 그대로인지 확인한다.
number-me-small-collection-namer|나이, 손가락으로 표시한 수, 실제 신체 부위 수를 구별한다. 사람에 따라 신체 조건이 다르므로 제시한 대상에서 확인 가능한 양을 묻는다.
number-peekaboo|장난감 하나의 나타남을 반복한 뒤 두 개와 세 개로 바꾼다. 수 이외에 소리·표정·장난감 종류가 함께 달라질 수 있어 시선만으로 개수 인식을 확정하지 않는다.
numbers-on-me-very-small-number-recognizer|두 개까지의 신체 부위와 수를 연결한다. 사람마다 신체 조건이 다르다는 본문 지침과 말·가리키기·수 카드 지원을 구분해 기록한다.
reach-21-conceptual-subitizer-with-place-value|두 장에서 시작한다. 목표는 두세 장이나 본문은 차례마다 추가할 수 있다고 쓴다. 추가 장수와 공동 최고 합, 모두 21 초과 때의 처리는 시작 전에 정한다.
snapshots-conceptual-subitizer-to-20|11~20을 5나 10의 익숙한 부분으로 배열한다. 20에서 두 십과 나머지 0, 그보다 작은 수에서 한 십과 남은 점을 설명한다.
snapshots-conceptual-subitizer-to-5|1~5개를 2초 안팎으로 보인 뒤 손가락으로 답한다. 맞힌 수만으로 한눈에 본 전략과 작은 부분을 더한 전략을 구별할 수 없다.
snapshots-conceptual-subitizer-to-50|십 틀을 3~5초 정도 제시한다. 가득 찬 십 틀과 일부만 채운 틀의 점을 구별하고 같은 합을 다른 묶음으로 설명한다.
snapshots-conceptual-subitizer-to-7|1~7개의 여러 배치를 2초 보여 준다. 첨부 이름의 1~7+와 본문 범위를 구별하고 7의 배열은 일반 주사위 눈과 별도로 확인한다.
snapshots-perceptual-subitizer-to-4|목표·절차는 1~4이고 준비물 목록은 1~5, 선택 카드는 0~5다. 준비물 전체의 범위를 한 회의 제시 범위로 옮기지 않는다.
snapshots-perceptual-subitizer-to-5|같은 개수의 줄·주사위형·흩어진 배치에서 최초 응답과 다시 보고 확인한 응답을 분리한다. 3과 2로 나눈 제시는 다음 유형으로 잇는다.
speedy-spots|빨강과 흰 카드 각각의 점을 묻고, 두 장을 더하는 것은 변형이다. 같은 수를 2와 2, 3과 1 등으로 본 방법을 비교한다.
swipe-7|카드 두 장의 합과 부분을 말한다. 남은 더미가 소진되는 경우나 가져온 카드를 다시 쓰는 조건을 정한다. 1~4만 나오는 주사위 변형에서는 3과 4만 7을 만든다.
tricky-two-small-collection-namer|목표와 다음 문장은 1·2·3을 말하지만 준비 문장에 43이 적혀 있다. 본문 흐름을 따를 때 셋째 그릇은 3으로 두고 위치 선택과 잠깐 본 수를 따로 기록한다.
what-changed|종류가 다른 물건, 색만 다른 물건, 같은 물건을 차례로 사용한다. 없어진 물건의 이름, 없어진 수, 남은 수를 각각 말하게 한다.
wheres-that-number|각 그릇 아래 1~4개를 두고 순서를 바꾼다. 목표 수의 그릇을 찾는 것과 들어 올린 뒤 실제 개수를 확인하는 것을 구별한다.
which-has-more-very-small-number-recognizer|3개와 5개를 차례로 본 뒤 어느 쪽이 더 많은지 설명한다. 첫 비교와 이후 세기, 큰 수의 약 두 배 조건을 구별한다.
'''

CLAIMS = [
    ('LT83', ['2수01-01', '2수01-03'], [1, 2, 3, 4, 9, 11, 17, 23, 24, 30],
     '짧게 본 뒤 개수 이름·카드·몸짓으로 답하게 하고 다시 보고 확인한다. 배열, 노출 시간, 대기 시간과 응답 도구를 구별해 기록한다.',
     '한 번의 빠른 응답만으로 세지 않았는지 또는 발달 수준을 확정할 수 없다. 익숙한 배치나 반응 방식의 차이도 고려한다.'),
    ('LT84', ['2수01-01', '2수01-04'], [6, 7, 13, 16, 25, 27, 28, 29],
     '가린 물건의 위치를 추적하는 수행과 펼친 뒤 알아본 수를 구별한다. 물건의 이름, 없어진 수, 남은 수는 각각 확인할 수 있다.',
     '정답 한 번으로 기억, 물건의 특징, 개수 인식 중 어떤 단서를 썼는지 확정하지 않는다. 영아 활동의 시선 반응은 초등 평가 결과가 아니다.'),
    ('LT85', ['2수01-02', '2수01-04', '2수01-06', '2수01-08'], [5, 12, 18, 19, 21],
     '가득 찬 십 틀과 일부만 채운 틀을 구별하며 십 묶음과 낱개로 전체를 구성한다. 2십과 3십에 낱개 4를 합하면 54다.',
     '절차에서 본 수 범위에 한정하며 큰 수의 자릿값 일반화나 재묶기 숙달까지 판단하지 않는다. 놀이 승패와 수의 구조 설명을 구별한다.'),
    ('LT86', ['2수01-04', '2수01-05', '2수01-07', '2수01-09'], [20, 22, 25, 26, 28],
     '같은 전체를 여러 두 부분으로 합성하고 시작 수·없어진 수·남은 수를 말하게 한다. 7을 만드는 두 카드의 값을 함께 말한다.',
     '카드 합을 맞히는 것과 빠진 부분을 거꾸로 찾는 설명을 따로 확인한다. 모든 카드의 구성과 종료 규칙은 자료 확인을 거친다.'),
    ('LT87', ['2수01-10', '2수01-11'], [0],
     '배열의 한 행에 든 수와 행 수를 말하고 둘을 합성 단위로 쓴다. 회전했을 때 열과 행의 역할이 바뀌어도 점 전체가 유지된다.',
     '흩어진 점의 합을 구하거나 회전 후 다시 세는 답과 같은 크기 묶음으로 설명하는 답을 구별한다. 인용 원연구의 효과 판정은 별도다.'),
]

OBSERVATIONS = [
    dict(id='LT-P74', standard_codes=['2수01-01', '2수01-03'],
         question='가에는 점 4개를 네모 모양으로, 나에는 점 4개를 길게 한 줄로 놓았다. 두 카드를 각각 잠깐 본 뒤 어느 쪽에 점이 더 많은지 말하라. 다시 본 뒤 처음 답과 같은지 확인하라.',
         expected='두 카드의 점은 각각 4개다. 펼쳐서 가의 점 하나와 나의 점 하나를 차례로 연결하면 남는 점 없이 네 짝이 된다.',
         interpretation='첫 판단과 다시 보고 확인한 판단을 나눠 적는다. 줄의 길이와 점의 개수, 짝짓기 지원 전후의 반응을 구별한다.', student_validated=False),
    dict(id='LT-P75', standard_codes=['2수01-01', '2수01-04', '2수01-05'],
         question='같은 단추 5개를 보여 주고 천을 덮었다. 다시 펼쳤더니 단추가 3개다. 빠진 단추는 몇 개인가? 처음 단추가 4개였다면 답은 어떻게 바뀌는가?',
         expected='처음이 5개일 때 빠진 수는 2다. 처음이 4개일 때에는 1개가 빠졌다. 남은 3개만 보고는 빠진 수를 정할 수 없다.',
         interpretation='처음 수를 기억한 것과 전체에서 남은 부분을 빼 빠진 부분을 찾는 것을 구별한다. 처음 수를 다시 알려 주기 전후의 설명을 기록한다.', student_validated=False),
    dict(id='LT-P76', standard_codes=['2수01-02', '2수01-04', '2수01-06'],
         question='가득 찬 십 틀이 한 카드에 2개, 다른 카드에 3개 있다. 별도 카드에는 점이 4개다. 모두 몇 개인가? 점 4개가 아니라 10개라면 어떻게 기록하는가?',
         expected='십 묶음 5개와 낱개 4개를 합하면 54다. 낱개 10개는 십 묶음 하나가 되므로 다음 경우는 60이다.',
         interpretation='십 틀의 개수와 점의 개수, 낱개 10개의 재묶기를 따로 설명하게 한다. 빠르게 답한 것과 자릿값을 설명한 것을 구별한다.', student_validated=False),
    dict(id='LT-P77', standard_codes=['2수01-04', '2수01-07', '2수01-09'],
         question='점 두 카드의 합이 7이다. 한 카드에 4개가 보인다. 가린 카드에는 몇 개가 있는가? 보인 카드가 2개로 바뀌면 가린 수는 어떻게 되는가? 두 상황을 빈칸이 있는 덧셈식으로 나타내라.',
         expected='4+□=7에서는 3, 2+□=7에서는 5다. 각각 7에서 보인 수를 빼 확인한다.',
         interpretation='합을 고정해 부분 하나를 바꿀 때 다른 부분을 어떻게 찾는지 본다. 사용한 카드에 5점 카드가 없으면 두 번째 상황을 별도로 구성한다.', student_validated=False),
    dict(id='LT-P78', standard_codes=['2수01-10', '2수01-11'],
         question='점이 한 줄에 5개씩 4줄 놓였다. 판을 90도 돌렸을 때 한 줄에 몇 개씩 몇 줄인가? 돌리기 전후 점 전체는 몇 개씩이며, 한 점을 빼면 여전히 같은 크기 줄로 이루어진 배열인가?',
         expected='돌리면 한 줄에 4개씩 5줄이다. 각각 전체 20개다. 한 점을 빼면 총 19개이고 원래 행·열 틀의 한 줄이 비어 있는 자리를 포함하므로 모든 줄의 점 수가 같지 않다.',
         interpretation='회전이 개수를 보존하는 까닭과 같은 크기 묶음으로 계산할 수 있는 배열의 조건을 따로 설명하게 한다.', student_validated=False),
]


def verify_examples(bodies):
    text = [row['body'] for row in bodies]
    assert 'that makes 50, and 4. That’s 4!' in text[5] and 2 * 10 + 3 * 10 + 4 == 54
    assert '43 counters or cubes' in text[27] and 'the set of 3 counters' in text[27]
    assert 'collections of 1 to 4 objects' in text[23] and 'arrangements of 1 - 5' in text[23]
    assert 'two or three sets' in text[18] and 'During each turn' in text[18]
    assert 'one through four' in text[26] and [(a, b) for a in range(1, 5) for b in range(1, 5) if a + b == 7] == [(3, 4), (4, 3)]
    assert '257–264' in text[16] and 'tb01061.x' in text[16]


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
                        and any('/math/subitizing/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|', 1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 31
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/', 1)[-1] for row in pages] == [row[0] for row in reading]
    verify_examples(bodies)

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
    assert len({url for links in images.values() for url in links}) == 41
    assert len({url for links in pdfs.values() for url in links}) == 8
    external_pdfs = {page: [url for url in urls if not url.startswith(URL)]
                     for page, urls in pdfs.items() if any(not url.startswith(URL) for url in urls)}
    pdfs = {page: [url for url in urls if url.startswith(URL)]
            for page, urls in pdfs.items() if any(url.startswith(URL) for url in urls)}
    assert len({url for links in pdfs.values() for url in links}) == 6
    assert list(external_pdfs) == [pages[28]['url']]
    assert len(external_pdfs[pages[28]['url']]) == 2
    assert len({urlparse(url).netloc + urlparse(url).path for url in external_pdfs[pages[28]['url']]}) == 1
    assert {k: len(v) for k, v in groups.items()} == dict(general=6, domain_overviews=20, levels=224, activities=455, teacher_resources=16)
    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key', 'url', 'title', 'sha256', 'status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 721
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'], followup['listed_body_pending']) == (471, 353)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
                 observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
                 catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies': 471, 'pending_activity_bodies': 353},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=31, teacher_resources=0, inline_images=0, supplementary_pdf_urls=0),
                 subitizing_reading_log=logs, completed_subitizing_records=selected,
                 subitizing_pdf_urls_not_reviewed=pdfs, subitizing_image_urls_not_reviewed=images,
                 subitizing_external_proceedings_urls_not_reviewed=external_pdfs,
                 subitizing_cited_research_pending=[
                     dict(linking_page=pages[0]['url'], url='https://doi.org/10.1016/j.jmathb.2023.101049', read_scope='출판사 서지 확인'),
                     dict(linking_page=pages[16]['url'], url='https://doi.org/10.1111/j.2044-835X.1987.tb01061.x', read_scope='Crossref 제목·인쇄 범위 대조'),
                     dict(linking_page=pages[28]['url'], url='https://swepub.kb.se/bib/swepub%3Aoai%3ADiVA.org%3Alnu-117858?language=en&tab2=abs', read_scope='국가 서지의 11~22쪽 표기 확인, 학술대회 원문 대조 대기'),
                 ],
                 subitizing_procedure_scope=dict(activity_procedures=31, teacher_resources=0),
                 subitizing_source_checks=dict(dice_reported_total=4, dice_computed_total=54,
                                               tricky_two_printed_third_collection=43, tricky_two_inferred_third_collection=3,
                                               perceptual_snapshot_procedure_range=[1, 4], perceptual_snapshot_material_range=[1, 5]),
                 reading_log=prior['reading_log'] + ['수량을 세지 않고 알아보는 수준에 연결된 영어 활동 31개의 목표·절차·준비물과 교사 지원을 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='subitizing_quantity_and_procedure_conflicts', locations=[pages[i]['url'] for i in (5, 6, 7, 10, 13, 18, 23, 26, 27)],
                     action='십과 일의 합, 목표와 준비물의 수 범위, 그릇을 섞는 방식, 카드 더미와 종료 조건을 구별했다.')],
                 unread_followups=[LIMITS, '이 활동들의 첨부·삽입 이미지와 연결된 원연구를 먼저 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
                  method_note='영어 목표와 절차의 수 범위, 처음 제시와 확인, 낱개·부분·십 묶음·행의 역할을 대조했다.',
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
    print('Reviewed 31 English activities; added 5 mappings and 5 observations. Public activity bodies pending: 353.')


if __name__ == '__main__':
    main()

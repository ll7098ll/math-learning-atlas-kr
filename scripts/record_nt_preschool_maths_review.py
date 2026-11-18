"""Register the public text of the NT Preschool Maths Games guide."""
import hashlib
import json

from literature_review import ROOT, build_report, digest, load_registry, target_value


SOURCE = 'NT_PRESCHOOL_MATHS_GAMES'
DATE = '2026-11-09'
URL = 'https://education.nt.gov.au/media/docs/support-for-teachers/nt-maths-games.pdf'
LANDING = 'https://education.nt.gov.au/support-for-teachers/preschool-stem-games'
ALIAS = 'https://education.nt.gov.au/__data/assets/pdf_file/0003/444567/nt-maths-games.pdf'
NOTES = 'data/literature_evidence/NT_PRESCHOOL_MATHS_GAMES_review_notes.json'
SCOPE = '교육청이 연결한 40쪽 PDF의 웹 추출 텍스트에서 물리 1~39쪽을 대조했다. 표지·소개·목차와 18개 활동의 두 쪽씩을 확인했다.'
LIMITS = (
    '40쪽에 대응하는 텍스트가 추출 결과에 없고, 직접 PDF 파일 요청에는 403이 반환됐다. '
    '원본 쪽 이미지와 파일 해시, 주소별 파일 동일성, 별도 효과 연구의 본문, 국내 학생 응답은 미검증이다.'
)

# Numbered positions in the provider's text view, indexed from zero.
LAST_TEXT_LINES = [
    3, 43, 67, 121, 162, 215, 268, 312, 363, 412, 440, 487, 526, 555, 593,
    626, 663, 697, 737, 771, 797, 845, 883, 918, 949, 983, 1015, 1053, 1080,
    1115, 1139, 1179, 1238, 1280, 1317, 1367, 1423, 1460, 1512,
]

ACTIVITIES = [
    ('수와 세기', '고리 안의 물건 세기', '수 말하기, 하나에 한 번씩 짚기, 마지막 수로 전체 말하기를 구별한다. 빈 고리는 0이며 같은 물건의 자리만 바꾸면 개수는 유지된다.'),
    ('수와 세기', '쌓기에 쓸 블록 세기', '요청한 수, 받은 수, 실제 쓴 수를 구별한다. 블록 크기가 다르면 높이와 블록 수의 순서가 같을 필요는 없다.'),
    ('수와 세기', '자리마다 하나 놓기', '사람이 앉을 자리를 먼저 정하고 접시·컵을 자리마다 하나씩 배치한다. 물건 수와 자리 수가 같아도 중복과 누락을 따로 확인한다.'),
    ('수와 세기', '부른 수만큼 걷기', '한 걸음마다 한 수를 세고 부른 수에서 멈춘다. 몇 시라는 말은 놀이 신호이며 시계 읽기, 경과 시간 측정, 보폭의 동일성과 구별한다.'),
    ('도형과 공간', '입체 물체의 면 본뜨기', '선택한 면을 따라 그린 평면 모양과 물체 전체를 구별한다. 누르기·윤곽 따라 그리기에서 어떤 흔적을 얻는지도 확인한다.'),
    ('도형과 공간', '물체의 위치 말하기', '상자·종이·의자를 기준으로 장난감의 위치를 설명한다. 같은 물체라도 기준물과 보는 방향이 바뀌면 표현이 달라질 수 있다.'),
    ('도형과 공간', '장애물 길의 위치와 이동', '무엇의 위·아래·안·옆을 지나는지 말한다. 다른 경로가 허용되는지, 말의 이해와 운동 수행 및 시범 도움을 구별한다.'),
    ('도형과 공간', '잘라 놓은 원 복원하기', '두 조각을 맞추어 전체를 만드는 활동이다. 두 조각이라는 사실과 두 조각의 넓이가 같다는 조건을 구별한다. 조각을 뒤집거나 돌릴 수 있는지도 지정한다.'),
    ('도형과 공간', '여러 기준으로 모양 분류하기', '색 3가지에 큰 원 2개와 작은 원 2개씩 총 12개다. 색과 크기를 기준으로 한 분류의 결과가 다르며, 색은 삼각형을 정하는 성질이 아니다.'),
    ('도형과 공간', '덮는 면과 둘레 비교', '면을 덮는 것과 가장자리를 따라가는 것을 나눈다. 박수 수나 걸린 시간으로 둘레를 비교하려면 박수 간격과 이동 속도 등을 따로 통제한다.'),
    ('규칙과 구조', '그림 카드 짝 맞추기', '무엇이 같은지를 지정한다. 한 기준으로 짝을 만드는 과제와 새 기준으로 묶는 과제, 짝의 수와 카드의 수를 구별한다.'),
    ('규칙과 구조', '꿰는 물체의 반복', '반복 단위와 시작 방향을 말하게 한다. 빈 자리의 답은 선택한 규칙과 시작점에 따라 검토한다. 꿰기 동작 도움은 규칙 이해와 따로 기록한다.'),
    ('규칙과 구조', '모자이크 반복', '교대 배열과 두 개씩 묶는 배열에서 기본 반복 단위를 설명한다. 다른 재료로 같은 구조를 만들 때 위치별 대응을 확인한다.'),
    ('규칙과 구조', '동작과 소리의 반복', '동작 순서와 소리의 구조를 대응시킨다. 보인 동작을 따라 하는 것, 반복 단위를 설명하는 것, 다음 항목을 예상하는 것은 따로 관찰한다.'),
    ('측정', '물의 양과 용기의 들이', '현재 물의 양과 가득 채웠을 때의 들이를 구별한다. 같은 컵을 같은 선까지 채우고 초기 물·흘림·넘침·남은 양을 확인한다.'),
    ('측정', '곧게 놓아 길이 비교', '비교할 방향을 정하고 공통 시작점을 맞춘다. 서로 다른 길이의 막대와 각각 비교한 말만으로 두 물건의 길이 순서를 정할 수 없다.'),
    ('자료', '자연물 분류와 세기', '겹치는 분류를 허용하는 단계가 있다. 한 물건이 둘에 속할 수 있을 때 분류별 개수의 합과 실제 물건 수를 구별한다. 쌓아 둔 더미 크기로 개수를 확정하지 않는다.'),
    ('자료', '책 투표를 표시하고 비교하기', '한 사람에게 표지물 하나를 주고 대응시킨다. 고른 책과 실제 투표 수, 줄 길이와 투표 수, 단독 최다와 동률을 구별한다.'),
]

CLAIMS = [
    ('NT01', ['2수01-01', '2수01-03'], '4~11쪽',
     '수말의 순서, 물건이나 동작마다 한 번씩 세기, 마지막 수가 뜻하는 전체, 자리마다 하나씩 배정하는 대응을 따로 관찰한다.',
     '마지막 수가 맞거나 동작을 따라 했다는 이유만으로 세기 절차와 수의 크기 비교를 모두 이해했다고 판단하지 않는다.'),
    ('NT02', ['2수03-01', '2수03-02', '2수03-03', '2수03-04'], '12~17쪽',
     '입체 물체의 선택한 면을 본뜬 평면도형과 물체 전체를 구별한다. 모양이나 움직임의 위치 표현에는 기준물과 보는 방향을 명시한다.',
     '평면 흔적 하나만으로 원래 입체를 정할 수 없으며, 장애물을 지나는 운동 능력과 위치 관계 설명은 따로 관찰한다.'),
    ('NT03', ['4수01-09', '4수03-12'], '18~19쪽',
     '원래 도형을 조각으로 나누고 다시 맞추는 활동은 부분과 전체의 관계를 보여 준다. 절반이나 사분의 일을 말할 때에는 정한 전체와 같은 크기로 나눈 조건을 확인한다.',
     '두 조각을 합쳐 원을 복원했다는 사실로 각 조각이 원의 절반이라고 확정하지 않는다.'),
    ('NT04', ['6수03-11', '6수03-13'], '22~23쪽',
     '덮은 면의 넓이와 바깥 경계의 길이를 구별한다. 걸린 시간과 둘레 길이는 이동 속도, 멈춤, 경로 선택을 따로 확인한 뒤 비교한다.',
     '원문에 나온 걷기나 박수 수만으로 둘레를 재거나, 넓이가 더 큰 도형의 둘레도 더 크다고 일반화하지 않는다.'),
    ('NT05', ['2수02-01', '2수02-02'], '24~31쪽',
     '카드 짝의 일치 조건과 순서에서 반복하는 단위를 구별한다. 모양, 색, 소리, 동작 사이에 위치별 대응을 정해 같은 반복 구조를 표현할 수 있다.',
     '재료를 비슷하게 고르거나 첫 동작을 따라 하는 것만으로 반복 단위를 설명하거나 새로운 규칙을 만들 수 있다고 보지 않는다.'),
    ('NT06', ['2수03-06', '2수03-10', '4수03-17'], '32~35쪽',
     '길이는 공통 시작점과 방향을 정해 비교한다. 들이는 빈 용기를 정한 선까지 채울 때의 양으로 비교하며, 현재 담긴 양과 구별한다.',
     '각자 다른 막대나 컵의 사용 횟수만 비교할 수 없다. 안내서의 비표준 도구 예는 국내 표준 단위 측정의 전체 성취를 보여 주지 않는다.'),
    ('NT07', ['2수04-01', '2수04-02', '2수04-03'], '36~39쪽',
     '한 물건이 여러 분류 기준을 만족할 수 있음을 설명한다. 한 사람당 한 표를 주는 모의 투표에서는 표지물과 사람의 대응을 정한 뒤 표시를 세고 동률을 확인한다.',
     '겹치는 두 분류의 합을 곧바로 물건 수로 읽지 않는다. 모의 투표는 현재 참여 집단의 선택을 나타내며 다른 집단의 선호나 효과를 입증하지 않는다.'),
]

OBSERVATIONS = [
    dict(
        id='NT-P1', standard_codes=['2수01-01'],
        question='자리 A·B·C·D·E 다섯 곳마다 카드 한 장씩 놓으려 한다. A에는 두 장, B·C·D에는 한 장씩, E에는 한 장도 없다. 카드가 모두 다섯 장이면 배치가 끝난 것인가? 카드를 더 만들지 않고 고치고, 어떻게 확인했는지 설명하라.',
        expected='전체 카드는 2+1+1+1+0으로 다섯 장이다. A에 한 장이 더 있고 E에는 한 장이 빠졌다. A의 카드 한 장을 E로 옮긴 뒤 모든 자리에 정확히 한 장씩 있는지 확인한다.',
        interpretation='전체 개수 맞히기와 자리마다 하나씩 대응하기를 따로 기록한다. 처음부터 오류를 찾았는지, 빈 자리를 가리켜 준 뒤 수정했는지도 구별한다.',
        student_validated=False,
    ),
    dict(
        id='NT-P2', standard_codes=['2수03-01', '2수03-04'],
        question='한 변 3cm인 주사위 모형과 3cm×3cm×5cm인 상자 모형을 준비했다. 주사위의 한 면과 상자의 3cm×3cm 면을 종이에 대고 둘레를 따라 그렸다. 종이에서 3cm×3cm 모양 하나만 보면 어느 물체의 흔적인지 고를 수 있는가? 상자의 3cm×5cm 면을 대면 어떻게 달라지는가?',
        expected='두 물체 모두 3cm×3cm의 정사각형을 만들 수 있어 흔적 하나로 구별할 수 없다. 상자의 3cm×5cm 면을 대면 그 크기의 직사각형이 나온다. 물체 전체와 종이에 닿는 면을 구별한다.',
        interpretation='치수는 교사가 준비할 조건이다. 학생은 실제 면을 대고 모서리를 따라 그리거나 완성된 흔적을 포개어 확인할 수 있다. 본뜨기 동작에 도움을 받은 경우에도 어떤 면을 고른 이유를 따로 기록한다.',
        student_validated=False,
    ),
    dict(
        id='NT-P3', standard_codes=['6수03-11', '6수03-13'],
        question='직사각형 길 A는 가로 4m·세로 2m, B는 가로 7m·세로 1m다. 두 사람이 각각 다른 길의 바깥 경계를 한 바퀴 도는 데 모두 30초가 걸렸다. 두 둘레는 같은가? 어느 길이 둘러싼 넓이가 더 큰가? 걸린 시간으로 둘레를 비교하려면 무엇을 확인해야 하는가?',
        expected='A의 둘레는 12m이고 넓이는 8m²다. B의 둘레는 16m이고 넓이는 7m²다. 같은 시간이 걸려도 두 사람이 이동한 거리는 다르다. 같은 기준으로 한 바퀴를 돌았는지, 같은 속도로 걷고 멈추지 않았는지 등을 확인한다.',
        interpretation='둘레와 넓이를 모두 단위와 함께 기록한다. 걸린 시간이 같다는 정보만으로 길이를 같다고 판단하는지 살핀다. 속도의 수치 계산을 요구하지 않는다.',
        student_validated=False,
    ),
    dict(
        id='NT-P4', standard_codes=['2수04-01', '2수04-02'],
        question='카드 네 장은 빨간 삼각형, 빨간 원, 파란 삼각형, 파란 원이다. 각각 한 장씩 있다. 빨간 카드 수와 삼각형 카드 수를 표의 두 줄에 적어라. 둘 중 적어도 한 기준에 해당하는 카드는 몇 장인가? 표의 두 수를 더한 결과와 비교하고 차이가 생긴 이유를 설명하라.',
        expected='빨간 카드는 두 장이고 삼각형 카드도 두 장이다. 빨간 삼각형, 빨간 원, 파란 삼각형의 세 장이 둘 중 적어도 한 기준에 해당한다. 두 수의 합은 4이지만 빨간 삼각형이 두 번 들어갔다. 파란 원은 어느 기준에도 속하지 않는다.',
        interpretation='기준을 서로 겹치게 허용한 표다. 카드마다 색·모양을 가리키거나 카드에 표시하며 어느 줄에 들어가는지 확인한다. 분류표의 합을 물건의 고유 개수로 읽는 조건을 관찰하며 집합 기호를 요구하지 않는다.',
        student_validated=False,
    ),
]


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def write(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert {row[0] for row in CLAIMS} <= {c['id'] for c in registry['claims'] if c['source_id'] == SOURCE}
        build_report()
        return

    assert len(ACTIVITIES) == 18 and len(LAST_TEXT_LINES) == 39
    assert 2 * (4 + 2) == 12 and 2 * (7 + 1) == 16 and 4 * 2 == 8 and 7 * 1 == 7
    assert sum([2, 1, 1, 1, 0]) == 5 and len({'A', 'B'} | {'A', 'C'}) == 3
    bounds = [[lo + 1, hi] for lo, hi in zip([-1] + LAST_TEXT_LINES, LAST_TEXT_LINES)]
    assert all(lo <= hi for lo, hi in bounds)
    scope = dict(
        reported_pdf_pages=40, text_pdf_pages=list(range(1, 40)), visual_pdf_pages=[],
        binary_obtained=False, text_line_count=1513, page_text_line_ranges=bounds,
    )
    method = '교육청 안내에서 연결한 PDF의 웹 추출 텍스트를 물리 쪽별로 읽었다. 목차의 18개 활동과 설명·교사 절차를 대조하고, 자료 조건과 적용 한계를 자체 작성했다.'
    entry = dict(
        id=SOURCE, title='Northern Territory Preschool Maths Games',
        authors=['Caroline Cohrssen'], contributor='Elizabeth Cook',
        kind='교육청 수학놀이 안내서의 공개 PDF 추출 텍스트', url=URL,
        review_scope=SCOPE, next_review=LIMITS,
        supports=['소집단 수학 활동과 관찰 발문 설계', '길이·둘레·분류의 조건 구분'],
        does_not_establish='국내 성취기준에 대한 학생 진단의 정확도 또는 안내서 자체의 독립적 효과 검증',
    )
    activity_log = [
        dict(domain=domain, description=title, pdf_pages=[4 + 2 * index, 5 + 2 * index], note=note)
        for index, (domain, title, note) in enumerate(ACTIVITIES)
    ]
    notes = dict(
        source_id=SOURCE, source_url=URL, source_asset_kind='web_pdf_text',
        date=DATE, reviewer='Codex', read_scope=SCOPE, pdf_text_review=scope,
        original_page_layout_review=False, contains_source_full_text=False, source_pdf_redistributed=False,
        reading_log=['물리 1~3쪽의 표지·소개·목차와 4~39쪽의 활동 18개를 확인했다. 40쪽은 웹 추출에 대응하는 텍스트가 없다.'],
        activity_reading_log=activity_log,
        source_corrections=[
            dict(pdf_pages=[22, 23], action='박수 수나 소요 시간을 둘레 길이로 해석하려면 속도와 측정 조건을 통제한다.'),
            dict(pdf_pages=[36, 37, 38, 39], action='중복 분류의 합, 한 물건당 한 번 세기, 한 사람당 한 표, 단독 최다와 동률을 구별한다.'),
        ],
        access=dict(official_landing=LANDING, direct_file_403=[URL, ALIAS], alias_byte_identity_verified=False),
        bibliography_note='표지에서 저자와 도움을 준 사람을 확인했다. 2쪽 참고의 2013년은 선행 자료의 연도이므로 이 안내서의 발행 연도로 사용하지 않았다.',
        related_study=dict(url='https://doi.org/10.1080/09669760.2019.1629882', full_text_read=False, results_mapped=False),
    )
    write(NOTES, notes)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
        snapshot_kind='authored_review_notes', snapshot_file=NOTES,
        snapshot_sha256=hashlib.sha256((ROOT / NOTES).read_bytes()).hexdigest(),
        source_asset_kind='web_pdf_text', pdf_text_review=scope,
        redistribution_license='workspace_authored_notes', bibliography_snapshot=digest(entry),
        display=dict(title=entry['title'], url=URL, authors_year='Caroline Cohrssen · Elizabeth Cook의 도움'),
        read_scope=SCOPE, scope_note='교육청의 활동 안내를 국내 과제의 설계 참고로 사용한다.',
        method_note=method, limits=LIMITS,
        editorial_action='문헌 근거 7건과 자체 관찰 과제 4개를 연결했다. 정답과 과정, 물체와 자국, 넓이와 둘레, 겹치는 분류와 고유 개수를 구별한다.',
        independent_review=False, student_validated=False, observations=OBSERVATIONS,
    )
    for cid, codes, pages, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='related_theoretical_context', locations=[f'웹 PDF 텍스트 {pages}'],
            standard_codes=codes, support=support, does_not_establish=limit,
            target_snapshots={'revision:' + code: digest(target_value('revision:' + code)) for code in codes},
            independent_review=False, student_validated=False,
        ))

    bibliography = read('data/sources.json')
    assert SOURCE not in {item['id'] for item in bibliography}
    bibliography.append(entry)
    queue = read('data/content_review_queue.json')
    queue['literature_review'].append(dict(
        source=entry, status='self_read_claim_mapping',
        claim_evidence_fields=['기준 코드', 'PDF 쪽', '활동 조건', '적용 한계'],
        evidence_file='data/literature_claim_reviews.json', claim_ids=[row[0] for row in CLAIMS],
    ))
    write('data/sources.json', bibliography)
    write('data/literature_claim_reviews.json', registry)
    write('data/content_review_queue.json', queue)
    build_report()


if __name__ == '__main__':
    main()

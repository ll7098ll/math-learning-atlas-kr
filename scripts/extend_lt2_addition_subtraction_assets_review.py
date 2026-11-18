"""Record the reviewed LT2 addition and subtraction printables and figures."""
import copy
import re
from collections import Counter
from itertools import combinations, combinations_with_replacement, product

from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_addition_subtraction_activities_review_notes.json'
PRIOR_SHA = '013f5355713d7a31c60d96a55b5b50731678e6c37ba40ce8cc99d2cb852f9d43'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_addition_subtraction_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-addition-subtraction-assets'
SCOPE = (
    '공개 영어 HTML 565개와 활동·교사자료 본문 315개를 확인했다. 본문 509개가 남았다. '
    '덧셈·뺄셈의 연결 PDF 24개 URL·66쪽과 삽입 이미지 92개 URL을 추가로 대조했다. '
    '누적 PDF는 63개 URL·173쪽이고 삽입 이미지는 441개 URL이다. '
    '파일 해시가 같은 경우를 한 번으로 세면 PDF 58개·162쪽, 이미지 434개다.'
)
LIMITS = (
    '문제 유형표의 웹 본문·삽입 표·연결 PDF를 구별했다. 인쇄 판의 칸과 가능한 합은 자료 조건을 적용해 계산했다. '
    '다른 인쇄본, 실제 놀이의 승률·진행과 수업 효과, 인용 원연구, 영상 전체, '
    '미검토 본문과 별도 첨부, 독립 검토·학생 응답은 후속 범위다.'
)

PDF_NOTES = {
    '1566297700464.pdf': [([1], '합류·분리·부분과 전체·비교를 12가지로 배열한다. 비교는 작은 양·차이·큰 양을 구별한다. 차이 예는 블록 7개와 5개를 쓴다. 마지막 비교에서 물건 명칭이 구슬에서 공으로 바뀌므로 같은 종류를 센다는 조건을 명시한다.'), ([2], '로고·테두리·저작권 표기가 있으며 수학 본문은 없다.')],
    '1580171966479.pdf': [(range(1, 5), '수 카드의 0~5, 6~11, 12~17, 18~20을 순서대로 확인했다. 활동별로 쓰는 범위는 본문에 따른다.')],
    '1580181269307.pdf': [([1], '1~6 숫자와 접착 날개가 있는 주사위 전개도다. 숫자 구성이 실제 각 면의 확률을 보장하지 않는다.')],
    '1585585635113.pdf': [([1], '10×10 격자에서 대각으로 마주 보는 5×5 구역 두 곳이 분홍이다. 분홍 50칸과 나머지 50칸을 구별한다.')],
    '1585586396873.pdf': [([1], '세 개의 2×10 격자 각각에서 왼쪽 2×5만 분홍이다. 격자 하나에 분홍 10칸과 흰색 10칸이다.')],
    '1586295352926.pdf': [([1], '개별 수 글자 없이 점으로 0~5를 나타낸다. 빈 배열을 0과 대응한다.')],
    '1586295390727.pdf': [([1], '점 카드 6~10이다. 채운 첫 열의 5개와 둘째 열의 나머지를 더한다.')],
    '1676655464842.pdf': [([1, 2], '숫자 카드 0~5와 6~10이다. 틱택 20 본문이 지정한 카드 범위 1~10과 인쇄물 범위를 구별한다.')],
    '1681919865046.pdf': [(range(1, 5), '수 0~20을 열 칸 틀 두 개와 함께 나타낸다. 첫 틀 10과 둘째 틀의 낱개 및 전체 빈 칸을 구별한다. 세기에서 읽은 1580172084628과 같은 파일이다.')],
    '1681919886394.pdf': [(range(1, 5), '0~20의 숫자 카드다. 같은 파일이 다른 주소에도 연결되어 있다. 제빵 활동의 주문 카드 범위는 10~19다.')],
    '1681919930732.pdf': [([1], '눈 세 개가 있는 파란 캐릭터 도안이다. 도안 자체에는 놀이에서 센 과자 수나 응답 기록이 없다.')],
    '1686760037635.pdf': [(range(1, 5), '열 칸 틀에 먼저 놓인 컵케이크 수가 10·9·8·7개 순이다. 첫 틀의 빈 자리와 주문을 완성하는 데 더 필요한 수를 구별한다.')],
    '1686760059659.pdf': [([1], '2×5 빈 틀이다. 19개 주문을 7개에서 완성하려면 첫 틀 3자리와 추가 틀 9자리를 사용한다.')],
    '1686762649370.pdf': [(range(1, 10), '2×5 틀의 아이스크림 그림이 9개에서 1개까지 한 쪽에 하나씩 감소한다. 윗줄을 먼저 채운다.')],
    '1686762666024.pdf': [([1], '2×5에 아이스크림 그림 10개가 채워져 있다.')],
    '1686762680783.pdf': [([1], '이야기에서 쓰는 캐릭터 도안이다. 양을 나타내는 별도 카드와 구별한다.')],
    '1686762693697.pdf': [([1], '트럭 아래 빈 판은 4열×2행이다. 열 칸 틀이나 실제 트럭의 적재량으로 읽지 않는다.')],
    '1686937745816.pdf': [(range(1, 5), '빨강 4×4 빙고판 네 장은 각각 2~10을 모두 포함하며 일곱 값이 두 번씩 나온다.')],
    '1686937769567.pdf': [(range(1, 5), '주황 4×4 빙고판 네 장은 각각 2~12를 모두 포함하며 다섯 값이 두 번씩 나온다.')],
    '1686937788439.pdf': [([1, 2, 3], '노랑 4×4 빙고판에 3~18이 한 번씩 나온다. 지정 카드로 가능한 2는 없다.'), ([4], '12가 두 번 나오고 앞 세 판에 있던 11은 없다. 2는 이 판에도 없다.')],
    '1690822105674.pdf': [([1], '상자 위에서 두 방향의 끈이 만나는 사진이다. 가려진 밑면의 경로, 매듭과 여유 길이, 상자의 세 치수를 사진만으로 정할 수 없다.')],
    '1690823468129.pdf': [(range(1, 9), '인쇄 카드 69장, 서로 다른 34개 액면 합을 확인했다. 명시된 동전 주사위 세 개에서 가능한 값의 집합과 같다. 40과 80은 모두 실린 값이다. 25+10+5는 40이고, 80을 만드는 값은 순서를 빼면 50+25+5다.')],
    '1690826166215.pdf': [([1], '더하는 수를 고르는 3×3 작은 판과 5×5 큰 판이다. 큰 판의 모든 수는 다른 두 칸을 골라 만들 수 있다.'), ([2], '큰 판은 5행×6열이다. 큰 판의 모든 수가 가능하며, 여섯 칸 줄은 가로에서만 가능하다.'), ([3], '큰 판은 6×6이다. 작은 판에서 두 수를 골라서는 53·75·79·87·97을 만들 수 없다. 같은 칸을 두 번 허용해도 이 다섯 값은 그대로다. 여섯 칸 줄은 가능한 값만 있는 줄을 따로 확인한다.')],
    '1778111716070.pdf': [([1], '합류와 분리 각 3개 예다. 각 이야기에서 시작량·변화량·결과량 중 무엇이 미지수인지 찾는다.'), ([2], '비교 예 6개다. 아래 왼쪽과 오른쪽은 비교 기준량을 구한다. 위 양쪽은 비교하는 양, 가운데 두 예는 차이를 구한다. 공통 열 제목을 비교량의 의미로 그대로 적용하지 않는다.'), ([3], '전체를 구하는 예 하나와 부분을 구하는 예 둘이다. 시간에 따른 추가 행동이 없는 상황이며 인용 문헌 본문 확인과 구별한다.')],
}

IMAGE_NOTES = [
    ([23, 41, 42, 51, 55, 69, 72, 91], '숫자 카드·점 카드·빈 틀·주사위 도구의 미리보기다. 보이는 범위를 전체 인쇄물이나 실제 추첨 범위와 구별한다.'),
    ([25, 26], '두 주소의 그림은 같은 파일이다. 25+23과 50−2가 모두 48이라는 예에서 계산 방향을 구별한다.'),
    ([36, 45, 50, 62, 90], '7+빈칸=10 그림에는 빈 칸 3개가 보인다. 노랑 빙고 예는 3과 점 4를 더해 7에 표시한다. 8−5=3 그림, 0~10 수직선, 30~99 일부 수 표는 해당 배치와 절차의 범위를 구별한다.'),
    ([67, 78, 79, 81, 82, 83, 84, 85, 86, 87], '삽입 비교 행에서 차이 또는 비교하는 양을 묻는다. 연결 PDF 2쪽에 따로 있는 기준량 미지수 두 예는 이 삽입 표에 없다.'),
    ([44, 48, 49, 52, 53, 54, 59, 60, 70, 73, 74, 75, 76, 80, 88, 89], '재료·도구·사진과 준비 그림이다. 준비물의 수량 표기, 사진에 보이는 물건, 실제 사용하는 양을 구별한다.'),
]

CLAIMS = [
    ('LT59', ['2수01-05', '2수01-09'], ['1566297700464', '1778111716070'], [67],
     '새 교사 PDF의 비교 6개 예에는 기준량을 구하는 두 예가 있다. 비교하는 양, 기준량, 차이를 각각 표시하면 같은 5와 2가 주어져도 비교 방향에 따라 구하는 값이 달라진다.',
     '웹 본문·삽입 표와 새 연결 PDF의 예는 구별한다. 비교 표의 결과·변화·시작이라는 열 이름은 시간에 따라 수가 변한다는 뜻이 아니다.'),
    ('LT60', ['2수01-04', '2수01-06', '2수01-09'], ['1681919886394', '1686760037635', '1686760059659', '1585585635113', '1585586396873'], [36],
     '주문 10~19와 먼저 놓인 컵케이크 7~10을 대응시킨다. 첫 틀의 빈 칸, 추가 틀이 필요한 수, 주문까지 더 놓을 전체 수는 서로 다른 양이다. 분홍 격자는 지정한 열 묶음을 보여 준다.',
     '수 카드 전체 범위 0~20과 이 활동의 주문 범위를 구별한다. 채색된 칸이나 빈 칸 자체를 활동 중 이미 놓은 물건으로 세지 않는다.'),
    ('LT61', ['2수01-05', '2수01-06'], ['1686937745816', '1686937769567', '1686937788439'], [45],
     '카드 두 묶음이 만드는 합과 놀이판에 실제 인쇄한 값을 따로 확인한다. 노랑은 카드 1~15와 1~3으로 2~18을 만들지만 2가 인쇄되어 있지 않고, 넷째 판은 12가 두 번이고 11이 없다.',
     '같은 합을 한 칸에만 표시할지 여러 칸에 표시할지, 한 장짜리 묶음을 어떻게 다시 쓸지는 활용할 때 명시한다. 배열 차이를 학생의 계산 오류로 처리하지 않는다.'),
    ('LT62', ['2수01-06', '2수01-09'], ['1690826166215'], [],
     '두 수만 골라 만드는 합을 큰 판과 대조한다. 2단계의 여섯 칸 줄은 가로만 가능하다. 3단계에 인쇄된 다섯 값은 주어진 두 수를 더해서 만들 수 없다.',
     '영어 웹 절차의 네 칸 종료 조건과 인쇄판 제목의 다섯·여섯 칸을 구별한다. 가능한 합의 배열만으로 실제 놀이의 승률이나 진행 순서를 정하지 않는다.'),
    ('LT63', ['2수01-06', '2수01-08'], ['1690823468129'], [],
     '동전 주사위 세 개에서 만들 수 있는 34가지 액면 합이 인쇄 카드의 34가지 값과 일치한다. 25+10+5는 40이고 80은 50+25+5로 만들 수 있다.',
     '같은 1이 두 면에 있는 전개 조건을 값의 종류와 구별한다. 가능한 조합이나 면 순서의 수는 실제 주사위의 공정성을 보여 주지 않는다.'),
]

OBSERVATIONS = [
    dict(id='LT-P52', standard_codes=['2수01-05', '2수01-09'],
         question='민지는 구슬이 5개다. 가에서는 민지가 준서보다 2개 많다. 나에서는 준서가 민지보다 2개 많다. 준서는 각각 몇 개인가? 같은 5와 2가 나오는데 답이 다른 까닭을 두 줄 그림으로 설명하라.',
         expected='가는 준서가 비교의 기준이어서 준서 3개에 2개를 더하면 민지 5개다. 나는 민지 5개에 2개를 더해 준서 7개다.',
         interpretation='많다는 말과 계산 기호를 바로 연결하는지, 기준으로 삼는 양과 비교하는 양을 찾는지 구별한다. 방향을 바꾼 새 문장에서도 그림의 긴 줄과 짧은 줄을 지정하도록 한다.', student_validated=False),
    dict(id='LT-P53', standard_codes=['2수01-04', '2수01-06', '2수01-09'],
         question='19개 주문에서 열 칸짜리 첫 상자에 7개를 넣었다. 첫 상자를 먼저 채운 뒤 둘째 상자에 넣는다. 더 넣어야 할 수와 상자별로 새로 넣는 수는 각각 얼마인가? 완성하면 빈 자리는 몇 곳인가?',
         expected='12개가 더 필요하다. 첫 상자에 3개, 둘째에 9개를 넣어 10+9로 19개다. 두 상자 20자리 중 1자리가 비어 있다.',
         interpretation='첫 상자의 빈 자리 3개, 추가하는 전체 12개, 완성 후 빈 자리 1개를 구별한다. 10개 주문에 첫 상자가 이미 찬 경우에는 추가량 0도 확인할 수 있다.', student_validated=False),
    dict(id='LT-P54', standard_codes=['2수01-05', '2수01-06'],
         question='노랑 빙고판 네 번째 판에서 12는 두 칸, 11은 한 칸도 없다. 카드 9와 3, 다음에 카드 10과 1을 뽑았다. 각 합과 표시할 수 있는 자리는 무엇인가? 한 번에 한 칸만 표시하는 규칙이면 첫 차례에 몇 칸을 표시하는가?',
         expected='첫 합은 12이고 두 후보 칸 중 한 곳을 표시한다. 다음 합은 11이고 해당 칸이 없어 표시하지 않는다. 11을 정확히 계산해도 판에 그 수가 없을 수 있다.',
         interpretation='덧셈 결과와 판에 표시 가능한 수를 구별한다. 모든 같은 수를 표시하는 규칙을 새로 정하면 첫 차례 결과만 달라지는지 확인한다.', student_validated=False),
    dict(id='LT-P55', standard_codes=['2수01-06', '2수01-09'],
         question='작은 판에 11·19·22·28·33·37·41·45·55가 있다. 서로 다른 두 칸을 골라 더한다. 큰 판의 53과 56을 만들 수 있는지 각각 확인하고, 가능한 합에는 두 수를 적어라.',
         expected='56은 11+45 또는 19+37로 만들 수 있다. 53을 만들려면 53보다 작은 후보 각각의 짝이 42·34·31·25·20·16·12·8 중 하나여야 하는데 작은 판에 없다. 55를 쓰면 이미 53보다 크다.',
         interpretation='두 수를 찾은 경우와 찾지 못한 경우의 근거를 구별한다. 카드에서 하나씩 선택해 필요한 짝을 기록하거나 작은 수부터 모든 후보를 검토하는 방법을 쓸 수 있다.', student_validated=False),
]


def checked_assets(raw_pdfs, raw_images):
    pdfs, pdf_notes, images = [], {}, []
    for item in raw_pdfs:
        pages = list(range(1, item['pdf_pages'] + 1))
        rows = PDF_NOTES[item['url'].rsplit('/', 1)[-1]]
        assert [p for group, _ in rows for p in group] == pages
        assert [r['pdf_page'] for r in item['renders']] == pages
        assert item['status'] == 200 and sha(ROOT / item['file']) == item['sha256']
        assert all(sha(ROOT / r['file']) == r['sha256'] for r in item['renders'])
        asset = {k: item[k] for k in ('url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'pdf_pages')}
        pdfs.append(dict(asset, read_kind='linked_pdf_content_and_visual_review', redistributed=False,
                         content_read_method='visual_pages_and_available_text', content_pdf_pages=pages,
                         visual_pdf_pages=pages, rendered_pages=[{k: r[k] for k in ('pdf_page', 'sha256')} for r in item['renders']]))
        pdf_notes[item['url']] = [dict(pdf_pages=list(group), note=note) for group, note in rows]
    for index, item in enumerate(raw_images):
        assert item['index'] == index and item['status'] == 200 and sha(ROOT / item['file']) == item['sha256']
        asset = {k: item[k] for k in ('url', 'page_url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'dimensions')}
        images.append(dict(asset, read_kind='inline_image_visual_review', redistributed=False))
    listed = [i for indices, _ in IMAGE_NOTES for i in indices]
    assert len(listed) == len(set(listed)) and set(listed) <= set(range(len(images)))
    others = sorted(set(range(len(images))) - set(listed))
    groups = IMAGE_NOTES + [(others, '수업·놀이·물건 그림과 가린 모임의 예다. 사진의 짧은 장면은 독립 수행, 발화 전체, 교사의 도움이나 과제 결과로 집계하지 않는다.')]
    image_notes = [dict(image_urls=[images[i]['url'] for i in indices], note=note) for indices, note in groups]
    return pdfs, pdf_notes, images, image_notes


def numeric_rows(name):
    text = (CACHE / f'{name}.txt').read_text(encoding='utf-8')
    pages = re.split(r'=== PDF PAGE \d+ ===', text)[1:]
    return [[list(map(int, line.split())) for line in page.splitlines()
             if re.fullmatch(r'\d+(?: +\d+)+', line.strip())] for page in pages]


def verify_printed_numbers(names):
    bingo = []
    for name, color, a, b in [('1686937745816', '빨강', 9, 1), ('1686937769567', '주황', 9, 3), ('1686937788439', '노랑', 15, 3)]:
        possible = {i + j for i, j in product(range(1, a + 1), range(1, b + 1))}
        for page, rows in enumerate(numeric_rows(name), 1):
            assert len(rows) == 4 and all(len(row) == 4 for row in rows)
            counts = Counter(sum(rows, []))
            repeated = sorted(value for value, count in counts.items() if count > 1)
            missing = sorted(possible - counts.keys())
            assert not counts.keys() - possible
            assert missing == ([] if a == 9 else [2, 11] if page == 4 else [2])
            assert len(repeated) == (7 if b == 1 else 5 if a == 9 else int(page == 4))
            if a == 15 and page == 4:
                assert repeated == [12] and counts[12] == 2
            bingo.append(dict(url=names[name], color=color, pdf_page=page, board_size=[4, 4],
                              possible_sum_range=[min(possible), max(possible)], repeated=repeated, unprinted_possible_sums=missing))

    lines = []
    name = '1690826166215'
    for page, rows in enumerate(numeric_rows(name), 1):
        small = [row for row in rows if len(row) == 3]
        large = [row for row in rows if len(row) > 3]
        assert len(small) == 3
        height, width = len(large), len(large[0])
        assert (height, width) == [(5, 5), (5, 6), (6, 6)][page - 1]
        assert all(len(row) == width for row in large)
        values = sum(small, [])
        possible = {a + b for a, b in combinations(values, 2)}
        repeated_allowed = {a + b for a, b in combinations_with_replacement(values, 2)}
        unreachable = sorted(set(sum(large, [])) - possible)
        assert unreachable == sorted(set(sum(large, [])) - repeated_allowed)
        assert unreachable == ([53, 75, 79, 87, 97] if page == 3 else [])
        assert page != 3 or {tuple(sorted(pair)) for pair in combinations(values, 2) if sum(pair) == 56} == {(11, 45), (19, 37)}
        n = 5 if page == 1 else 6
        directions = {'horizontal': (0, 1), 'vertical': (1, 0), 'diagonal_down': (1, 1), 'diagonal_up': (-1, 1)}
        counts = {}
        for direction, (di, dj) in directions.items():
            counts[direction] = sum(
                0 <= i + (n - 1) * di < height and 0 <= j + (n - 1) * dj < width
                and all(large[i + k * di][j + k * dj] in possible for k in range(n))
                for i, j in product(range(height), range(width))
            )
        assert tuple(counts.values()) == [(5, 5, 1, 1), (5, 0, 0, 0), (3, 2, 1, 0)][page - 1]
        lines.append(dict(url=names[name], pdf_page=page, addend_grid_size=[3, 3], board_size=[height, width],
                          unreachable_with_two_addends=unreachable, printed_title_line_size=n, attainable_lines_by_direction=counts))

    coin_text = (CACHE / '1690823468129.txt').read_text(encoding='utf-8')
    printed = [int(cents) if cents else 100 * int(dollars) + int(change)
               for cents, dollars, change in re.findall(r'(\d+)₵|\$(\d+)\.(\d{2})', coin_text)]
    faces = [1, 1, 5, 10, 25, 50]
    outcomes = Counter(sum(triple) for triple in product(faces, repeat=3))
    assert len(printed) == 69 and len(set(printed)) == 34 and set(printed) == outcomes.keys()
    combos_80 = {tuple(sorted(triple)) for triple in product(faces, repeat=3) if sum(triple) == 80}
    assert combos_80 == {(5, 25, 50)} and outcomes[40] == outcomes[80] == 6
    coin = dict(card_count=len(printed), unique_printed_values=len(set(printed)), reachable_values=len(outcomes),
                face_values=faces, ways_for_40=outcomes[40], ways_for_80=outcomes[80], combinations_80=sorted(combos_80))
    return dict(bingo=bingo, line_boards=lines, coin=dict(coin, url=names['1690823468129']))


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        assert source['snapshot_sha256'] == sha(ROOT / NOTES)
        assert {row[0] for row in CLAIMS} <= {c['id'] for c in registry['claims']}
        assert source['observations'][-len(OBSERVATIONS):] == OBSERVATIONS
        build_report()
        return
    assert source['snapshot_file'] == PRIOR and sha(ROOT / PRIOR) == PRIOR_SHA
    prior = load(ROOT / PRIOR)
    raw_pdfs, raw_images = [load(CACHE / f'{kind}-manifest.json') for kind in ('pdf', 'image')]
    assert len(raw_pdfs) == len(PDF_NOTES) == 24 and len(raw_images) == 92
    assert asset_pairs(raw_pdfs) == linked_pairs(prior['addition_subtraction_pdf_urls_not_reviewed'])
    assert asset_pairs(raw_images) == linked_pairs(prior['addition_subtraction_image_urls_not_reviewed'])
    pdfs, pdf_notes, images, image_notes = checked_assets(raw_pdfs, raw_images)
    all_pdfs = prior['supplementary_pdf_read_manifest'] + pdfs
    all_images = prior['image_read_manifest'] + images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert len(all_pdfs) == 63 and sum(a['pdf_pages'] for a in all_pdfs) == 173
    assert len(unique_pdfs) == 58 and sum(unique_pdfs.values()) == 162
    assert len(all_images) == 441 and len({a['sha256'] for a in all_images}) == 434
    names = {a['url'].rsplit('/', 1)[-1].removesuffix('.pdf'): a['url'] for a in pdfs}
    number_checks = verify_printed_numbers(names)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
                 supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
                 supplementary_pdf_coverage=dict(urls=63, page_occurrences=173, distinct_sha256_files=58,
                                                 pages_after_file_deduplication=162, all_selected_pages_visual_reviewed=True,
                                                 whole_site_attachment_review=False),
                 pdf_exact_reuse_groups=reuse_groups(all_pdfs), addition_subtraction_image_exact_reuse_groups=reuse_groups(images),
                 addition_subtraction_pdf_urls_not_reviewed={}, addition_subtraction_image_urls_not_reviewed={},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=92, supplementary_pdf_urls=24),
                 addition_subtraction_pdf_reading_log=pdf_notes, addition_subtraction_image_reading_log=image_notes,
                 addition_subtraction_printed_number_checks=number_checks,
                 pdf_reading_log={**prior['pdf_reading_log'], **{
                     url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows]
                     for url, rows in pdf_notes.items()}},
                 reading_log=prior['reading_log'] + ['덧셈·뺄셈 첨부 PDF 24개·66쪽과 삽입 이미지 92개 URL을 활동 본문과 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='addition_subtraction_printables_and_rules',
                     locations=[names[n] for n in ('1778111716070', '1686937788439', '1690826166215', '1690823468129')],
                     action='기준량 미지수의 자료별 범위, 빙고판의 누락·중복, 줄 만들기 판의 줄 방향·만들 수 없는 값, 40과 80의 다른 동전 조합을 명시했다.')],
                 unread_followups=[LIMITS, '남은 수의 합성·분해와 수량 비교 활동의 본문부터 확인한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
                  method_note='PDF 66쪽의 렌더와 가용 문자를 대조하고 삽입 그림 92개를 확인했다. 인쇄 수는 가능한 카드 합과 비교했다.',
                  editorial_action='문헌 대응 5건과 자체 관찰 과제 4개를 추가했다.',
                  image_read_manifest=all_images, supplementary_pdf_read_manifest=all_pdfs,
                  observations=source['observations'] + OBSERVATIONS)
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
    print('Reviewed 24 PDFs, 66 pages and 92 inline images; added 5 mappings and 4 observation tasks.')


if __name__ == '__main__':
    main()

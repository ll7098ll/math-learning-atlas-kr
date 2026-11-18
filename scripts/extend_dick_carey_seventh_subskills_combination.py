"""Apply the remaining selected subskills and entry-skills passages to mathematics tasks."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_subskills_combination_review_notes.json'
PREVIOUS_SHA = '9bd9ffab40d7b7533e420f7cd76b562b7364fc7f05d6c8bb51d8b8c703632d1a'
SCOPE_ADDITION = ' 하위·출발 기능 분석의 국제판 62~70쪽과 74~77쪽 전사문에서 혼합 분석, 사례, 연습과 피드백을 추가로 대조했다.'

MAPPINGS = [
    ('DC35', ['4수03-04'], '국제판 62~66쪽, 계획과 실제 조작을 나눈 혼합 분석',
     '도형을 조작하기 전에 예상 위치를 묻고, 실제로 조작한 위치와 그 뒤의 설명을 나누어 관찰한다.',
     '미리 예상할 수 있는지와 조작할 수 있는지를 같은 결과로 묶지 않는다. 예상의 기록을 뒤집기·돌리기 활동 전체의 필수 시작 조건으로 삼지 않는다.',
     '정사각형 카드의 위쪽 변 한가운데에 점을 찍었다. 카드의 중심을 고정하고 시계 방향으로 90° 돌리기 전에 점의 위치를 예상한 뒤 실제로 돌려 확인하라. 처음 상태에서 가운데 세로선을 기준으로 뒤집을 때도 확인하라.',
     '시계 방향으로 90° 돌리면 점은 오른쪽 변의 가운데로 간다. 처음 상태에서 가운데 세로선을 기준으로 뒤집으면 점은 그 선 위에 있어서 위쪽 변의 가운데에 남는다.',
     '조작 전 예상, 돌리는 방향, 뒤집는 기준선, 실제 점의 위치를 각각 적는다. 특정 점이 움직이지 않았다고 카드의 모든 점이 그대로인 것은 아니다.'),
    ('DC36', ['2수03-10', '4수03-15'], '국제판 62~66쪽과 74~76쪽, 조작·설명과 도구를 이용한 하위 기능',
     '대상을 자에 맞추는 동작, 단위와 두 끝의 눈금을 확인하는 설명, 눈금 사이 간격을 구한 결과를 따로 기록한다.',
     '자의 표시를 읽은 반응만으로 실제로 도구를 올바르게 댔다고 판단하지 않는다. mm를 쓰는 조건은 해당 학년 범위에서 다룬다.',
     '띠를 자에 대고 2cm 눈금과 17cm 눈금에 양 끝을 맞춰 길이를 말하라. mm 눈금자를 쓰는 별도 과제에서는 두 끝이 23mm와 68mm일 때 길이를 설명하라.',
     '끝점 사이의 간격이 길이다. 첫 띠는 17−2=15cm이고, 별도 띠는 68−23=45mm다. 두 경우 모두 오른쪽 끝의 눈금값만 말하면 실제 길이와 다르다.',
     '먼저 자를 놓은 방법과 두 끝을 확인한다. 초등 1~2학년군에는 cm 과제를 적용하고, mm 과제의 설명은 초등 3~4학년군에서 확인한다.'),
    ('DC37', ['6수02-03', '6수02-04'], '국제판 74~77쪽, 지도 읽기 연습·피드백과 그림 4.12의 축척 항목',
     '지도 거리와 대응하는 실제 거리의 방향과 단위를 먼저 정한다. 주어진 거리에 맞춰 단위량, 배, 비례식 중 어떤 풀이를 선택하는지 본다.',
     '원문의 축척 표기를 자체 문항의 수치로 가져오지 않는다. 축척이 일정한 지도 위 거리의 모형이며 실제 이동 경로는 별도다.',
     '어떤 지도에서는 2cm가 실제 거리 3km에 대응한다. 지도 거리 6cm와 3cm는 각각 실제 몇 km인가? 여러 번 더하는 방법과 기준을 1cm로 바꾸는 방법을 비교하라.',
     '6cm는 2cm의 세 배여서 3+3+3=9km다. 3cm는 2cm의 한 배와 절반이므로 3+1.5=4.5km다. 1cm에 1.5km가 대응하므로 6과 3을 각각 곱해도 같다.',
     '지도와 실제 거리의 단위를 따로 표시한다. 6cm의 정수 배 풀이가 3cm에서 그대로 반복되지는 않으므로 절반이나 단위량을 어떻게 설명하는지 기록한다.'),
    ('DC38', ['6수01-06', '6수01-09'], '국제판 66~70·74~75쪽, 실제 적용과 잠정 출발 기능의 구분',
     '분수 곱의 값을 구하는 일과 크기가 같은 분수로 나타내는 설명을 분리한다. 약분을 적용했다면 어느 단계에서 어떤 수의 크기가 보존되는지 확인한다.',
     '계산 중에 먼저 약분하는 절차를 모든 풀이에 요구하지 않는다. 분수 표현과 그림 설명은 기록된 반응에 근거해 판단한다.',
     '직사각형의 가로를 4등분하고 세로를 3등분했다. 가로로 4분의 3, 세로로 3분의 2만큼 겹치는 부분의 넓이는 전체의 얼마인가? 두 분수의 곱과 같은 크기의 분수로 설명하라.',
     '같은 크기의 12칸 중 6칸이다. 3/4×2/3=6/12=1/2다. 겹친 칸이 6칸인 이유와 6/12를 분자·분모 각각 6으로 나누면 1/2가 되는 이유를 따로 설명한다.',
     '그림에서 선택한 두 방향, 곱으로 표현한 식, 같은 크기의 분수로 바꾼 근거를 기록한다. 절반이라는 정답만 주어지면 각 근거는 별도로 확인한다.'),
    ('DC39', ['9수04-05', '9수04-06'], '국제판 67~70·76~77쪽, 명칭 묶음과 분류·규칙 적용',
     '가능한 결과에 붙인 이름의 수와 그 결과를 만드는 등가능한 경우의 수를 구분한다. 확률을 계산할 때 분모로 무엇을 셌는지 설명하게 한다.',
     '이 사례는 같은 가능성으로 선택되는 칸을 조건으로 준다. 이름이 다른 결과를 언제나 같은 가능성으로 취급하지 않는다.',
     '같은 가능성으로 멈추는 네 칸이 있다. 두 칸에는 빨강, 한 칸에는 파랑, 한 칸에는 초록이라고 적혀 있다. 가능한 색과 빨강이 나올 확률을 말하라. 가능한 색이 세 가지라는 사실로 분모를 3으로 잡을 수 있는가?',
     '가능한 색은 세 가지다. 하지만 같은 가능성으로 선택되는 칸은 네 개이고 빨강이 적힌 칸은 두 개여서 빨강의 확률은 2/4=1/2이다. 파랑과 초록의 확률은 각각 1/4이다.',
     '색 이름 목록과 동일하게 선택되는 칸의 목록을 분리한다. 같은 크기만 보고 가능성이 같다고 가정하지 않도록 공정한 선택 조건이 발문에 제시됐는지 확인한다.'),
]

RELATIONS = [
    ('REV-4수03-15-1', 'DC36', '자의 시작과 끝을 확인하고 눈금의 단위를 붙여 차를 설명한다.',
     'cm에서 확인한 조작을 mm 눈금이나 다른 도구에서도 할 수 있는지는 따로 관찰한다.'),
    ('REV-6수02-04-1', 'DC37', '2cm와 3km의 대응을 유지한 채 6cm와 3cm를 각각 계산한다.',
     '정수 배로 풀었다는 사실만으로 단위량이나 비례식을 설명할 수 있다고 판단하지 않는다.'),
    ('REV-6수02-03-2', 'DC37', '대응하는 두 양의 단위와 순서를 고정하고 1cm에 대응하는 값을 설명한다.',
     '지도에서의 두 점 사이 거리와 실제 이동 경로는 계산할 대상부터 구분한다.'),
    ('REV-6수01-09-1', 'DC38', '곱을 6/12로 나타낸 뒤 1/2와 같은 크기임을 12칸 그림과 식에서 확인한다.',
     '약분은 이 표현을 간단히 쓰는 방법이다. 계산 중 약분을 먼저 해야만 곱을 구할 수 있는 것은 아니다.'),
    ('REV-9수04-05-1', 'DC39', '색 이름 세 가지와 같은 가능성으로 선택되는 네 칸을 별도로 센다.',
     '확률의 분모로 경우의 수를 쓰려면 센 경우가 등가능하다는 조건을 확인한다.'),
]


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        build_report()
        return
    previous = copy.deepcopy(source)
    assert previous['snapshot_sha256'] == PREVIOUS_SHA
    assert hashlib.sha256((ROOT / previous['snapshot_file']).read_bytes()).hexdigest() == PREVIOUS_SHA
    asset_hash = hashlib.sha256((ROOT / TRANSCRIPT).read_bytes()).hexdigest()
    prior_notes = read(ROOT, previous['snapshot_file'])
    assert asset_hash == TRANSCRIPT_SHA == prior_notes['transcript']['sha256']
    assert 17 - 2 == 15 and 68 - 23 == 45
    per_cm = Fraction(3, 2)
    assert per_cm * 6 == 9 and per_cm * 3 == Fraction(9, 2)
    assert Fraction(3, 4) * Fraction(2, 3) == Fraction(6, 12) == Fraction(1, 2)
    assert Fraction(2, 4) + Fraction(1, 4) + Fraction(1, 4) == 1

    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    followup = '학습자·맥락 분석 88~97쪽의 사례·연습, 각 장과 부록의 나머지 본문, 공식 판면·도식과 인용 연구를 대조한다. 독립 검토와 학생 응답은 실제 자료로 확인한다.'
    book.update(review_scope=scope, next_review=followup)
    notes = dict(prior_notes, date=DATE, read_scope=scope, previous_review=previous,
                 previous_bibliography=prior_book,
                 subskills_combination_extension=dict(
                     international_printed_page_ranges=[[62, 70], [74, 77]],
                     original_edition_printed_page_ranges=[[74, 82], [86, 89]],
                     transcript_only=True, diagram_connections_from_text=False,
                     independent_review=False, student_validated=False))
    notes['reading_log'] += [
        '국제판 62~66쪽의 혼합 분석에서 조작 전 계획, 실제 조작, 그에 필요한 지식 및 시작점의 차이를 확인했다.',
        '66~70쪽에서 목표 전체의 절차, 한 단계의 하위 분석, 이름이나 정보를 묶는 표를 분리했다. 나란히 놓인 세 활동을 본문이 위계 없이 배치했다고 설명한다.',
        '74~77쪽의 연습과 피드백에서 축척을 계산하는 서로 다른 방법, 가정한 출발 기능, 예시와 다른 분석의 검토를 읽었다.',
    ]
    notes['source_corrections'] += [
        dict(kind='transcript_subskill_count', location='국제판 62~63쪽, 그림 4.6 주변 본문',
             action='전사 본문은 하위 기능을 네 개라고 쓰고 4.1·4.3·4.4·4.5의 조작 기능과 4.2의 별도 기능을 언급한다. 표기 차이는 보존하고 판면에서의 범위와 개수를 확정하지 않는다.'),
        dict(kind='transcript_scale_labels', location='국제판 76쪽, 그림 4.12의 4.4·4.5·4.6 항목',
             action='한 눈금 길이 1인치와 눈금이 뜻하는 5마일을 적은 항목, 2인치와 5마일을 짝지은 항목을 각각 기록했다. 하나의 축척으로 묶지 않고 자체 예에는 독립적으로 정한 수치를 쓴다.'),
    ]
    notes['unread_followups'] = [followup]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    observations = [probe(int(cid[2:]), codes, question, expected, interpretation)
                    for cid, codes, _, _, _, question, expected, interpretation in MAPPINGS]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 계획과 실제 조작, 절차와 자료 묶음, 잠정 출발 기능의 관찰을 구분했다.',
                  editorial_action='성취기준 9개에 근거 5건과 자체 관찰 5건을 대응하고 관계별 대조 5건을 작성했다.',
                  observations=previous['observations'] + observations)
    old_claims = {row['id']: row for row in registry['claims'] if row['source_id'] == SOURCE}
    new_claims = {
        cid: dict(id=cid, source_id=SOURCE, role='related_theoretical_context',
                  locations=[f'비공식 HTML 전사본 · {location}'], support=support, does_not_establish=limit,
                  target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
                  standard_codes=codes, independent_review=False, student_validated=False)
        for cid, codes, location, support, limit, *_ in MAPPINGS
    }
    assert set(new_claims).isdisjoint({row['id'] for row in registry['claims']})
    assert len({code for claim in new_claims.values() for code in claim['standard_codes']}) == 9
    registry['claims'].extend(new_claims.values())

    relations = read(ROOT, 'data/revised_relations.json')['relations']
    by_id = {row['id']: row for row in relations}
    reviews = read(ROOT, FILE)
    pairs = {(row['id'], cid) for row in relations for cid, claim in new_claims.items()
             if all(row[key].startswith('standard:') for key in ('from', 'to'))
             and {row[key][9:] for key in ('from', 'to')} <= set(claim['standard_codes'])}
    assert pairs == {(rid, cid) for rid, cid, *_ in RELATIONS}
    for row in reviews['records']:
        if row['claim_id'] in old_claims:
            claim = old_claims[row['claim_id']]
            assert row['claim_snapshot'] == claim_snapshot(claim, previous)
            row['claim_snapshot'] = claim_snapshot(claim, source)
    for rid, cid, finding, limit in RELATIONS:
        reviews['records'].append(dict(relation_id=rid, claim_id=cid, role='activity_context', finding=finding,
                                       limit=limit, relation_snapshot=relation_snapshot(by_id[rid]),
                                       claim_snapshot=claim_snapshot(new_claims[cid], source)))
    apply_literature_context(relations, registry, registry=reviews)
    queue_path = 'data/content_review_queue.json'
    queue = read(ROOT, queue_path)
    item = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    item.update(source=book, claim_ids=[row['id'] for row in registry['claims'] if row['source_id'] == SOURCE])
    (ROOT / NOTES).write_text(notes_text, encoding='utf-8', newline='\n')
    write('data/sources.json', bibliography)
    write('data/literature_claim_reviews.json', registry)
    write(FILE, reviews)
    write(queue_path, queue)
    build_report()
    print('Seventh international edition subskills combination: 5 claims, 5 observation designs, 5 relation records')


if __name__ == '__main__':
    main()

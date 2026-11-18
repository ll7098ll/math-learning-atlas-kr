"""Apply the newly reviewed goal-analysis passages to specific mathematics tasks."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_goal_analysis_review_notes.json'
PREVIOUS_SHA = 'd4fa9802ab834454751ba1a60fe830db2e5577390d8374909e3af8a58aafec7b'
SCOPE_ADDITION = ' 목표 분석 뒷부분의 국제판 36~45쪽(원서 48~57쪽) 전사문과 그림·표의 본문 설명을 추가로 대조했다.'

MAPPINGS = [
    ('DC31', ['9수02-03', '9수02-04'], '국제판 36~38쪽, 표 3.2와 지도 거리 예의 선택 조건 설명',
     '풀이의 선택 조건을 실제 수행으로 드러낸다. 양변에 같은 묶음이 나타나는지 먼저 확인하고, 선택한 풀이의 첫 변형이 해를 보존하는지 설명하게 한다.',
     '전개 풀이도 두 식에서 유효하다. 선택의 이유와 적용 범위를 관찰하며 이 예에 고정된 풀이 순서를 부여하지 않는다.',
     '4(x+2)=3(x+2)+9와 4(x+2)=3(x−2)+9를 풀어라. 두 식의 괄호를 비교하고, 첫 식에서 쓴 첫 연산을 둘째 식에 쓰면 어떤 결과가 남는지 설명하라.',
     '첫 식에서 양변의 3(x+2)를 빼면 x+2=9여서 x=7이다. 둘째 식에서도 같은 식을 양변에서 빼는 연산 자체는 타당하지만 오른쪽에 3(x−2)−3(x+2)=−12가 남는다. 따라서 x+2=−3에서 x=−5다. 두 식 모두 전개해서 풀 수도 있다.',
     '학생이 알아차린 괄호의 조건, 선택한 첫 변형, 오른쪽에 남는 항, 해를 따로 기록한다. 다른 타당한 첫 변형도 허용한다.'),
    ('DC32', ['6수04-02', '6수04-03'], '국제판 37~38·42쪽, 질문이 이후 선택을 바꾸는 경우와 목표 분석 점검표',
     '탐구 질문에 맞춰 어떤 값을 그래프로 옮길지 결정하게 한다. 하루의 구성과 여러 날의 변화를 확인하는 데 필요한 자료와 그래프 선택의 이유를 기록한다.',
     '그래프를 고르는 기준을 묻되 한 종류만 정답으로 고정하지 않는다. 전체가 다른 날의 횟수 증가와 비율의 변화를 구별한다.',
     '세 날의 전체 응답과 걸어서 온 응답은 각각 10명 중 5명, 20명 중 6명, 25명 중 10명이다. 둘째 날의 전체 구성을 나타내고, 세 날에 걸어서 온 응답의 비율이 어떻게 변했는지도 나타내라. 각 질문에 고른 그래프와 이유를 설명하라.',
     '둘째 날은 걸어서 30%, 그 밖의 방법 70%라 띠그래프나 원그래프로 나타낼 수 있다. 세 날의 비율은 50%, 30%, 40%다. 날짜를 가로축으로 놓고 같은 눈금으로 비율을 표시하면 줄었다가 늘어난 것이 드러난다. 걸어서 온 인원은 5명, 6명, 10명으로 계속 늘었다.',
     '질문별 분모와 표시할 값을 먼저 확인한다. 100% 막대 세 개처럼 타당한 대안도 설명과 함께 인정하고, 실제 관찰이 필요한 조사와 제공 자료의 해석을 구분한다.'),
    ('DC33', ['6수02-05'], '국제판 40~42쪽, 목표 문구 수정과 앞 단계 산출을 사용하는 절차의 예',
     '주어진 양을 비례배분할 때 같은 크기의 부분 수를 합해 전체의 기준을 만든다. 해당 풀이에서 어떤 중간값을 다음 계산에 썼는지 관찰한다.',
     '중간값을 종이에 쓰는 순서는 풀이에 따라 달라진다. 교사가 가르친 순서나 문장 수를 채점 기준으로 쓰지 않는다.',
     '물 98mL를 두 병에 2:5로 나눈다. 2+5로 만든 수가 어떤 역할을 하는지 말하고 두 양을 구해라. 한 부분의 양을 적지 않고 구할 수 있는 방법도 설명하라.',
     '같은 크기의 부분이 모두 7개다. 한 부분은 98÷7=14mL이므로 28mL와 70mL다. 또는 전체의 2/7과 5/7을 곱해 구한다. 합은 98mL이며 28:70을 14로 나누면 2:5다.',
     '7이 전체 부분 수임을 설명하는지와 최종 배분을 따로 기록한다. 한 부분의 양을 명시하는 풀이와 전체의 몫을 직접 쓰는 풀이를 구별한다.'),
    ('DC34', ['4수03-10', '9수03-11'], '국제판 40·42~45쪽, 목록의 조직과 수행 순서, 연습 피드백',
     '사각형 이름을 정리한 표의 배열과 실제 분류에 사용하는 조건을 구분한다. 정사각형을 직사각형과 마름모 양쪽에 넣을 근거를 각각 확인한다.',
     '초등에서 주어진 성질을 확인해 분류하는 과제와 중학교에서 포함을 정당화하는 과제를 구별한다. 이름을 어떤 순서로 물었는지로 선수 관계를 정하지 않는다.',
     '네 각이 직각이고 네 변 길이가 같은 사각형을 비스듬히 그렸다. 직사각형과 마름모 중 어디에 해당하는가? 이번에는 두 이름을 묻는 순서를 바꾸어 각각 이유를 말하라.',
     '네 각이 직각이어서 직사각형이고, 네 변 길이가 같아서 마름모다. 묻는 순서를 바꾸거나 그림을 돌려도 두 조건은 유지된다. 두 이름은 동시에 붙을 수 있다.',
     '두 조건을 따로 확인한다. 초등에서는 제시된 조건에 따른 분류를 관찰하고, 중학교에서는 모든 정사각형이 두 정의를 만족하는 이유로 설명을 확장한다.'),
]

RELATIONS = [
    ('SEC_9수02-03_C04', 'DC31', '두 식에 같은 첫 연산을 적용하고 남는 묶음을 각각 비교한다.',
     '등식 변형이 타당한지와 그 변형이 식을 얼마나 단순하게 만드는지를 따로 본다.'),
    ('SEC_9수02-04_C03', 'DC31', '공통식이 있는 경우와 괄호가 다른 경우에서 해를 구하고 처음 줄의 근거를 설명한다.',
     '해를 맞힌 것만으로 조건에 맞는 변형을 고른 이유를 확인할 수 없다.'),
    ('REV-9수02-03-1', 'DC31', '같은 식을 양변에서 빼기 전후에 어떤 항이 남는지 살핀다.',
     '해를 보존하는 기능이 필요한 범위는 이 풀이의 해당 단계다. 학습 순서 전체로 일반화하지 않는다.'),
    ('REV-6수04-03-2', 'DC32', '둘째 날의 구성 비율과 세 날의 비율 변화를 질문에 맞게 표현한다.',
     '비율 그래프를 그리는 기능이 모든 통계 탐구 질문에서 같은 방식으로 쓰이지 않는다.'),
    ('SEC_9수03-11_C02', 'DC34', '기울여 그린 사각형에서 직각 조건과 같은 변 길이 조건을 각각 확인한다.',
     '겉모양을 보고 이름을 맞힌 반응만으로 포함의 근거를 확인하지 않는다.'),
    ('SEC_9수03-11_C03', 'DC34', '한 사각형이 두 정의에 속할 수 있는지 각 정의를 사용해 설명한다.',
     '초등의 개별 도형 분류와 중학교의 일반 정당화는 관찰 항목을 분리한다.'),
    ('AN_4수03-10_C01', 'DC34', '정사각형이 직사각형과 마름모에 동시에 속하는 이유를 조건별로 확인한다.',
     '포함 관계는 두 이름의 제시 순서나 한 정의가 다른 정의보다 먼저 학습되어야 함을 정하지 않는다.'),
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
    assert 4 * (7 + 2) == 3 * (7 + 2) + 9
    assert 4 * (-5 + 2) == 3 * (-5 - 2) + 9
    assert [Fraction(a, b) * 100 for a, b in ((5, 10), (6, 20), (10, 25))] == [50, 30, 40]
    assert Fraction(2, 7) * 98 == 28 and Fraction(5, 7) * 98 == 70

    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    followup = '다른 장과 부록의 선정 범위 밖 본문, 공식 판면과 도식 및 인용 연구를 대조한다. 독립 검토와 학생 응답은 실제 자료로 확인한다.'
    book.update(review_scope=scope, next_review=followup)
    notes = dict(prior_notes, date=DATE, read_scope=scope, previous_review=previous,
                 previous_bibliography=prior_book,
                 goal_analysis_extension=dict(international_printed_pages=[36, 45], original_edition_printed_pages=[48, 57],
                                              transcript_only=True, diagram_connections_from_text=False,
                                              independent_review=False, student_validated=False))
    notes['reading_log'] += [
        '국제판 36~39쪽에서 교사 설명과 실제 수행, 전문가 사이의 경로 차이 및 지도 거리 예의 선택 조건을 읽었다.',
        '40~42쪽에서 중복이나 과도하게 큰 단계의 수정, 단계 산출물과 다음 입력, 점검표의 행동·산출·분기 문항을 확인했다.',
        '43~45쪽에서 회상 항목을 묶은 제시 순서, 실제 조작의 의존과 반복, 연습 답안의 가능한 차이를 구분했다.',
    ]
    notes['source_corrections'] += [dict(
        kind='goal_analysis_scope', location='전사본 국제판 36~45쪽·원서 48~57쪽, 그림 3.1 및 3.4~3.10 설명',
        action='국제판의 페이지와 원서 쪽을 구분했다. 그림 본문에 설명된 순서·선택과 회상 목록의 제시 순서를 구별했고, 전사 행의 배열에서 연결선을 복원하지 않았다.')]
    notes['unread_followups'] = [followup]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    observations = [probe(int(cid[2:]), codes, question, expected, interpretation)
                    for cid, codes, _, _, _, question, expected, interpretation in MAPPINGS]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 목표 분석의 실제 수행과 자료 제시 순서, 선택 조건을 구분했다.',
                  editorial_action='성취기준 7개에 근거 4건과 자체 관찰 4건을 대응하고 관계별 대조 7건을 작성했다.',
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
    assert len({code for claim in new_claims.values() for code in claim['standard_codes']}) == 7
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
    print('Seventh international edition goal analysis: 4 claims, 4 observation designs, 7 relation records')


if __name__ == '__main__':
    main()

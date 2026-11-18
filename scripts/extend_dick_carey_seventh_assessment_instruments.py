"""Apply the newly reviewed assessment-instrument passages to mathematics tasks."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_assessment_instruments_review_notes.json'
PREVIOUS_SHA = 'a032f11c2df7700d40b8a8ab2301b6e939a63a2560f54cbe4ca8788b5582bb25'
SCOPE_ADDITION = ' 평가 도구 개발 국제판 129~133·137~151쪽의 선정 전사문과 사례·연습의 조건을 추가로 대조했다.'

MAPPINGS = [
    ('DC46', ['6수01-02', '9수02-11'], '국제판 148~150쪽, 과제 14와 피드백의 거리 기준·경계',
     '문항의 이상·이하 방향과 경계 포함을 채점 기준에 똑같이 반영한다. 대입 판정과 부등식 변형의 근거를 따로 확인한다.',
     '전사문의 거리 기준을 자체 문항의 답으로 옮기지 않는다. 초등의 수 범위 표현과 중학교의 부등식 변형을 학년군에 맞게 구분한다.',
     '거리 기준이 3m 이하인 경우 2m, 3m, 4m를 각각 판정하고, 3m 이상으로 바꾼 경우도 비교하라. 중학교에서는 7−2x≤3을 만족하는 실수의 범위를 구하고 경계값을 확인하라.',
     '3m 이하는 2m와 3m, 3m 이상은 3m와 4m를 포함한다. 7−2x≤3에서 −2x≤−4이므로 −2로 나누면 부등호의 방향이 바뀌어 x≥2다. x=2에서 등호가 성립한다.',
     '경계 포함과 방향을 따로 판정한다. 중학교에서는 변형에서 방향을 바꾼 이유도 보며, 초등 과제에 문자식 풀이를 추가하지 않는다.'),
    ('DC47', ['4수03-15', '4수03-16'], '국제판 131~133·137~140쪽, 수행 조건과 관찰 기회',
     '직접 재는 동작과 주어진 길이 기록을 다른 단위로 쓰는 계산을 분리한다. 자를 쓰는 기회가 제공됐는지 먼저 확인한다.',
     '도구가 주어지지 않아 직접 측정하지 않은 경우와 자를 사용했으나 길이를 잘못 잰 경우의 기록을 구분한다.',
     '띠와 mm 눈금자를 받았다면 띠를 직접 재고 두 끝의 눈금을 적어라. 별도의 기록 문제에서 주어진 47mm를 몇 cm 몇 mm로 나타내라.',
     '직접 측정 결과는 실제 띠와 두 끝의 눈금에 따라 정한다. 기록 문제에서 47mm는 4cm 7mm다. 47mm가 직접 잰 띠의 길이인지 여부는 측정 기록을 확인한다.',
     '자·띠의 제공 여부, 실제 사용, 결과, 환산을 따로 표시한다. 도구가 없으면 측정은 미실시로 두고 환산만 판정한다.'),
    ('DC48', ['9수02-03', '9수02-04'], '국제판 141~146쪽, 평가 형식과 병렬 문항의 조건',
     '비슷한 두 방정식에서 풀이를 독립적으로 선택했는지 보려면 첫 연산을 알려 준 시점과 범위를 따로 기록한다.',
     '연산을 알려 준 문항과 알려 주지 않은 문항에서 같은 수의 정답을 얻어도 풀이 선택의 근거는 다르게 해석한다.',
     '3(x+2)=15와 4(y−1)=16을 각각 풀고 각 풀이의 첫 줄을 남겨라. 풀이를 보존한 뒤 둘째 식에서 양변을 4로 나누는 첫 줄이 왜 타당한지 설명하라.',
     '첫 식에서 3으로 나누면 x+2=5에서 x=3, 둘째 식에서 4로 나누면 y−1=4에서 y=5다. 둘 다 전개로도 풀 수 있다. 4는 0이 아니고 양변 전체를 같은 수로 나누므로 둘째 변형은 해를 보존한다.',
     '문항별 최초 풀이와 연산을 알려 준 뒤의 설명을 분리한다. 서로 다른 시점의 문항을 비교할 때 제시한 단서도 대조한다.'),
    ('DC49', ['12미적Ⅰ-03-04', '12미적Ⅰ-03-05'], '국제판 129~133·146~147쪽, 산출값과 수행 근거의 판정',
     '정적분의 수치, 그래프의 부호 변화, 도형 넓이를 계산할 때 구간을 나눈 이유를 독립 항목으로 확인한다.',
     '정적분의 값이 맞았다는 사실만으로 넓이 계산과 분할의 근거를 확인하지 않는다.',
     '0≤x≤3에서 y=x−1의 정적분과 그래프·x축·직선 x=0·x=3이 둘러싸는 부분의 넓이를 각각 구하라. 두 값이 달라지는 이유를 말하라.',
     '0에서 1까지 정적분은 −1/2, 1에서 3까지는 2이므로 전체 정적분은 3/2다. 두 부분의 넓이는 1/2와 2여서 합은 5/2다. x=1에서 부호가 바뀌므로 넓이를 구할 때 음인 부분의 부호를 바꾼다.',
     '적분값, 분할 위치, 두 넓이를 따로 판정한다. 최종값만 적으면 분할의 근거는 별도 질문으로 확인한다.'),
    ('DC50', ['12확통02-02', '12확통02-03'], '국제판 129~133·137~140쪽, 채점 항목과 확인 근거',
     '같은 확률을 서로 다른 방법으로 계산할 때 각 방법의 분모, 중복과 여사건을 구성한 근거를 나누어 확인한다.',
     '여사건을 사용해 정답을 낸 반응에서 덧셈정리의 중복 처리를 했다고 추정하지 않는다.',
     '1부터 12까지의 정수 중 하나를 같은 가능성으로 뽑는다. 짝수 또는 3의 배수가 나올 확률을 중복을 빼는 방법과 여사건을 이용하는 방법으로 각각 구하라.',
     '짝수는 6개, 3의 배수는 4개이고 공통인 6과 12는 2개이므로 합집합은 8개다. 둘 다 아닌 정수는 1,5,7,11로 4개다. 따라서 8/12=1−4/12=2/3이다.',
     '분모 12, 공통 원소 2개, 여사건 4개를 따로 확인한다. 한 풀이만 했다면 사용하지 않은 풀이의 수행은 별도로 남긴다.'),
    ('DC51', ['6수03-13', '6수03-14'], '국제판 130~133·145~147쪽, 과정과 산출물의 평가',
     '넓이 계산의 수치와 도형을 나누거나 다시 배치해 식의 근거를 설명한 내용을 나누어 기록한다.',
     '수치가 맞았다는 사실로 넓이 공식의 유도나 도형을 조작한 과정을 확인하지 않는다.',
     '가로 8cm, 세로 5cm인 직사각형을 한 대각선으로 나눴다. 직사각형의 넓이와 두 삼각형 각각의 넓이를 구하고 왜 두 삼각형의 넓이가 같은지 설명하라.',
     '직사각형은 40cm²이고 두 삼각형은 각각 20cm²다. 같은 두 변 길이와 그 사이의 직각을 가지는 두 직각삼각형은 겹쳐지므로 넓이가 같다. 전체를 두 부분으로 나눈 결과다.',
     '초등에서는 잘라 겹치거나 그림으로 보인 근거를 허용한다. 정답, 두 부분이 같은 넓이라는 근거, 넓이 단위를 따로 본다.'),
]

RELATIONS = [
    ('SEC_9수02-11_C01', 'DC46', '3 이하와 3 이상에 3이 모두 포함되는지 확인한다.', '경계 포함과 부등호의 방향은 다른 판정 항목이다.'),
    ('SEC_9수02-11_C02', 'DC46', 'x=2에서 등호가 성립하는지 대입하고 양옆 값도 비교한다.', '몇 값의 대입만으로 모든 실수의 해 범위를 확정하지 않는다.'),
    ('AN_6수01-02_C01', 'DC46', '수 범위에 경계가 들어가는 이유를 먼저 말하고 문자식의 해 범위에도 적용한다.', '초등 수 범위 과제에 음수로 나누는 부등식 변형을 요구하지 않는다.'),
    ('REV-4수03-16-1', 'DC47', '실제 잰 길이와 주어진 길이를 변환한 결과를 각각 기록한다.', '자가 없었던 조건에서 환산 정답을 직접 측정으로 채점하지 않는다.'),
    ('SEC_9수02-03_C04', 'DC48', '첫 연산을 선택한 기록과 양변을 4로 나눈 근거를 구분한다.', '두 기록은 서로 다른 제시 조건에서 얻었다.'),
    ('SEC_9수02-04_C03', 'DC48', '첫 풀이와 질문 뒤의 설명을 나누어 해와 변형을 확인한다.', '해만 맞힌 반응에서 각 변형의 타당성 설명을 추정하지 않는다.'),
    ('REV-9수02-03-1', 'DC48', '양변 전체를 같은 0 아닌 수로 나누는 단계가 해를 보존하는 이유를 설명한다.', '전개를 선택하는 다른 풀이도 허용한다.'),
    ('SEC_12확통02-02_C04', 'DC50', '합집합의 8개를 셀 때 공통인 6과 12를 한 번씩만 센다.', '여사건 풀이를 했는지는 응답에서 따로 확인한다.'),
    ('REV-12확통02-02-2', 'DC50', '1,5,7,11이 둘 다 아닌 경우임을 확인해 여사건을 구성한다.', '두 계산값이 같아도 사용한 사건과 근거는 별도로 확인한다.'),
    ('REV-6수03-14-2', 'DC51', '대각선으로 나눈 두 삼각형의 넓이가 같은 근거와 전체 넓이를 연결한다.', '같은 넓이를 확인하는 설명 없이 계산값만 비교한 반응과 구별한다.'),
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
    assert [7 - 2 * x <= 3 for x in (1, 2, 3)] == [False, True, True]
    assert divmod(47, 10) == (4, 7)
    assert 3 * (3 + 2) == 15 and 4 * (5 - 1) == 16
    negative_integral = Fraction(1, 2) - 1
    positive_integral = (Fraction(9, 2) - 3) - negative_integral
    assert negative_integral + positive_integral == Fraction(3, 2)
    assert -negative_integral + positive_integral == Fraction(5, 2)
    outcomes = set(range(1, 13))
    even = {x for x in outcomes if x % 2 == 0}
    multiples_of_three = {x for x in outcomes if x % 3 == 0}
    assert even & multiples_of_three == {6, 12}
    assert outcomes - (even | multiples_of_three) == {1, 5, 7, 11}
    assert Fraction(8 * 5, 2) == 20
    assert 7 * 4 + 20 * 0 == 28 > 27

    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    followup = '수업 전략·자료 개발·형성평가의 미검토 대목과 관련 부록, 공식 판면·도식과 인용 연구를 대조한다. 독립 검토와 학생 응답은 실제 자료로 확인한다.'
    book.update(review_scope=scope, next_review=followup)
    notes = dict(prior_notes, date=DATE, read_scope=scope, previous_review=previous,
                 previous_bibliography=prior_book,
                 assessment_instruments_extension=dict(
                     selected_international_page_ranges=[[129, 133], [137, 151]],
                     transcript_only=True, diagram_connections_from_text=False,
                     official_erratum_found=False,
                     putting_example=dict(exercise_distance_rule='distance_at_least_3_feet',
                                          feedback_positive_points_distance_at_most_feet=3,
                                          feedback_outside_points=0, attempts=27,
                                          aggregate_example=[4] * 7 + [0] * 20,
                                          aggregate_threshold_as_described=27)))
    notes['reading_log'] += [
        '129~133쪽에서 짧은 정오 문항과 수행·산출물 평가, 관찰 기회와 판단 기준을 구별했다.',
        '137~147쪽의 사례·점검에서 과제 조건과 관찰 기회, 병렬 문항의 단서, 채점 항목의 방향을 대조했다.',
        '148~151쪽의 연습·피드백에서 거리의 경계, 시도별 채점과 점수 합계의 차이를 확인했다.',
    ]
    notes['source_corrections'] += [
        dict(kind='distance_direction_mismatch', location='국제판 148~150쪽, 연습 14와 피드백·그림 7.4 설명',
             action='전사문 연습은 3피트 이상을 적었지만 피드백은 3피트 이내에 양의 점수를 주고 바깥은 0점으로 둔다. 두 표기를 보존하고 공식 판면과 정오표에서 다시 확인한다.'),
        dict(kind='item_vs_total_criterion', location='국제판 149~150쪽, 27회 평가의 개별 거리와 합계',
             action='거리 기준과 합계 27점 기준은 다르다. 합계를 기준으로 하면 홀인 7회와 0점 20회의 28점도 27점을 넘는다. 전체 시도마다 같은 거리 기준을 충족했다는 뜻으로 해석하지 않는다.'),
        dict(kind='opportunity_and_score', location='국제판 132~133·139~140쪽, 발생 기회와 점검표',
             action='상황이 생기지 않아 수행을 볼 수 없었던 항목과 실제 수행의 오류를 구분하고, 빈도와 함께 관찰 기회 수를 기록한다.'),
    ]
    notes['unread_followups'] = [followup]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    observations = [probe(int(cid[2:]), codes, question, expected, interpretation)
                    for cid, codes, _, _, _, question, expected, interpretation in MAPPINGS]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 평가 문항의 조건, 관찰 기회, 근거와 점수를 분리했다.',
                  editorial_action='성취기준 12개에 근거 6건과 자체 관찰 6건을 대응하고 관계별 대조 10건을 작성했다.',
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
    assert len({code for claim in new_claims.values() for code in claim['standard_codes']}) == 12
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
    print('Seventh international edition assessment instruments: 6 claims, 6 observation designs, 10 relation records')


if __name__ == '__main__':
    main()

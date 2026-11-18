"""Apply the newly reviewed instructional-revision and scoring passages."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_revision_followup_review_notes.json'
PREVIOUS_SHA = 'ad3f8bb233fcb22a140155b2310dce3ccc533dcbf328d52786e01b9263a78e4a'
SCOPE_ADDITION = ' 자료 수정 국제판 287~288·293~299·303~305쪽의 선정 전사문을 추가로 대조했다.'

MAPPINGS = [
    ('DC70', ['6수04-01', '12실통02-02'], '국제판 286~288쪽, 표 11.2·11.3의 표시 행과 집계 대상',
     '개별 행을 공개한 범위와 평균을 낸 전체 범위를 구분한다. 수집 범위가 분명한지 확인한 뒤 평균을 해석한다.',
     '예시로 보이는 다섯 행의 평균을 전체 20명의 평균으로 사용하지 않는다. 발췌 행에 대표성을 가정하지 않는다.',
     '20명이 참여한 가상 활동에서 다섯 명의 해결 문항 수만 2, 3, 4, 5, 6으로 보인다. 다섯 명의 평균을 구하고 전체 평균도 결정할 수 있는지 설명하라. 나머지 15명이 모두 2개인 경우와 모두 6개인 경우를 비교하라.',
     '다섯 명의 평균은 4개다. 두 경우의 전체 평균은 각각 2.5개와 5.5개이므로 실제 전체 평균은 다섯 행만으로 정할 수 없다.',
     '계산에 사용한 행과 평균의 대상, 더 필요한 자료를 따로 기록한다. 두 가정은 실제 자료에 더하지 않는다.'),
    ('DC71', ['6수04-02', '9수04-03'], '국제판 293~296·303~305쪽, 범주와 문항별 분모',
     '정답·오답·무응답의 상대도수와 미실시를 나눈다. 띠나 원에서 어느 집단이 전체인지 명시한다.',
     '미실시를 오답으로 합치거나, 응답자만의 비율을 전체 제공 인원의 비율로 옮기지 않는다.',
     '가상 기록에서 15명 중 12명에게 문항을 제공했다. 정답 8명, 오답 2명, 무응답 2명이다. 제공받은 사람을 전체로 한 원그래프의 각도를 구하고, 응답자만 대상으로 한 정답률과 비교하라.',
     '제공받은 12명의 세 범주는 240°, 60°, 60°다. 정답 비율은 8/12이고 응답자 10명 중 정답률은 8/10이다. 미실시 3명은 이 두 분모에 포함되지 않는다.',
     '제공 여부, 응답 여부, 정오, 그래프와 비율의 분모를 따로 기록한다.'),
    ('DC72', ['10공수2-02-04'], '국제판 303~305쪽, 표 11.7·11.8의 사례 판정',
     '목표에 속한 모든 문항이 맞았다는 명제와 전체 문항의 정답률을 구분한다. 틀린 문항 하나로 전칭 명제를 반박할 수 있다.',
     '정답 수가 같다는 사실로 목표별 통과 여부까지 같다고 판단하지 않는다. 모든 문항 정답은 이 예의 규칙이다.',
     '목표 4개에 문항이 3개씩 있다. A와 B의 목표별 정답 수는 각각 (3,3,2,1), (3,2,2,2)다. 목표 통과 조건은 그 목표의 문항을 모두 맞히는 것이다. 전체 정답률과 목표 통과율을 각각 구하고 B의 두 번째 목표의 판정 근거를 설명하라.',
     '전체 정답률은 둘 다 9/12=75%다. 통과율은 A가 2/4=50%, B가 1/4=25%다. B의 두 번째 목표에는 틀린 문항이 하나 있으므로 모든 문항을 맞혔다는 조건은 거짓이다.',
     '전체 문항 분모, 목표 분모, 목표별 전칭 판정과 반례를 각각 기록한다.'),
    ('DC73', ['9수02-03', '9수02-04'], '국제판 297~302쪽, 수정 문제와 근거 및 새 문항',
     '식의 변형에서 동치가 깨진 줄을 확인한다. 문항의 표현을 바꾸는 수정과 등식의 성질을 다시 다루는 수업 수정의 근거를 나눈다.',
     '오답 하나로 발문과 수업 중 무엇을 고쳐야 하는지 결정하지 않는다. 바꾼 사례에서 처음 준 단서도 기록한다.',
     '3(x−2)=x+8에서 한 가상 답안은 양변에서 x를 뺀 다음 2(x−2)=8이라고 썼다. 그 줄을 점검하고 해를 구하라. 다음에는 2(x+3)=x+11을 풀고 두 식의 해를 각각 대입해 확인하라.',
     '첫 변형은 3(x−2)−x=2x−6이어야 한다. 첫 해 7을 넣으면 양변이 15다. 둘째 해는 5이며 양변이 16이다.',
     '가상 오류의 위치, 학생의 수정 이유와 대입 확인, 새 과제에서 설명이 유지되는지 따로 기록한다.'),
    ('DC74', ['4수03-13', '4수03-14'], '국제판 289~292·300~302쪽, 소요 시간과 수정 자료',
     '시각 읽기, 두 시각 사이의 시간, 발문을 다시 보거나 기다린 시간을 구분한다.',
     '과제에 걸린 시간만으로 시각 읽기나 계산의 이해를 단정하지 않는다. 시작과 끝 기록의 기준을 맞춘다.',
     '실험은 오전 9시 59분 48초에 시작하여 오전 10시 00분 15초에 끝났다. 몇 초 걸렸는가? 별도 과제에서는 오전 11시 58분 52초부터 75초 뒤의 시각을 구하라.',
     '첫 소요 시간은 12초+15초=27초다. 둘째 시각은 정오 12시 00분 07초다. 75초에서 정오까지 68초를 빼면 7초가 남는다.',
     '시각 읽기와 경계 넘기 계산을 따로 판정한다. 발문 재확인이나 장비 대기가 있으면 풀이 시간과 구별한다.'),
    ('DC75', ['9수04-04', '9수04-08'], '국제판 287~289·293~299쪽, 요약 그림과 원자료 대조',
     '두 자료를 같은 축과 정한 규칙으로 비교한다. 도구가 표시한 수염과 자료의 최대값이 다른지 원자료에서 확인한다.',
     '중앙값이나 그래프의 겉모양만으로 모든 관측값이 같다고 판단하지 않는다. 수염 규칙을 섞어 비교하지 않는다.',
     '가상 시간 A=(1,2,3,4,9), B=(1,2,3,4,5)분을 같은 축에서 비교하라. 중앙값 양쪽에서 중앙값을 제외하고 사분위수를 구하며, 수염은 최소·최대까지 그리도록 정한다. 사용한 도구가 다른 규칙을 쓰면 표시 차이도 기록하라.',
     '두 중앙값은 3분이다. A의 제1·제3사분위수는 1.5분과 6.5분, B는 1.5분과 4.5분이다. 최소값은 둘 다 1분이고 최대값은 9분과 5분이다.',
     '원자료, 사분위수와 수염 규칙, 공통 축, 분포 해석을 각각 확인한다.'),
]

RELATIONS = [
    ('SEC_12실통02-02_C01', 'DC70', '표시한 다섯 행의 평균을 계산하고 나머지 행에 따라 전체 평균이 달라짐을 설명한다.', '자료의 확보 범위와 결론의 집단 범위를 맞춘다.'),
    ('AN_6수04-02_C01', 'DC71', '제공받은 인원을 분모로 세 범주의 상대도수를 원의 각도로 나타낸다.', '응답자만을 분모로 한 비율과 비교할 때 무응답 수를 밝힌다.'),
    ('SEC_9수02-03_C04', 'DC73', '양변에서 x를 빼는 동치 변형과 왼쪽 식을 정리하는 계산을 구분한다.', '오답 줄을 고친 근거와 새 식에서 적용한 근거를 따로 확인한다.'),
    ('SEC_9수02-04_C03', 'DC73', '후보 7과 5를 각각 원식에 넣어 좌우 값을 비교한다.', '가상의 오류 답안을 실제 학생 수행으로 처리하지 않는다.'),
    ('REV-9수02-03-1', 'DC73', '등식의 양변에 같은 연산을 한 뒤 식을 정리해 해를 구한다.', '최초 풀이와 수정 후 설명을 분리한다.'),
    ('REV-4수03-14-1', 'DC74', '두 시각을 읽고 분과 시의 경계를 넘는 실제 시간 차를 초로 계산한다.', '시각을 읽은 답과 경과 시간의 근거를 각각 확인한다.'),
    ('REV-9수04-04-1', 'DC75', '공통 축과 동일한 수염 규칙으로 두 자료를 비교한다.', '도구의 기본 설정과 과제에서 정한 규칙을 따로 기록한다.'),
    ('REV-9수04-08-1', 'DC75', '요약 그림의 중앙값과 최댓값을 원자료에서 다시 확인한다.', '그림만으로 원래 관측값 전체를 복원할 수 있다고 보지 않는다.'),
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
    from datetime import datetime, timedelta
    from statistics import median
    visible = [2, 3, 4, 5, 6]
    assert Fraction(sum(visible), len(visible)) == 4
    assert [Fraction(sum(visible) + 15 * v, 20) for v in (2, 6)] == [Fraction(5, 2), Fraction(11, 2)]
    assert [Fraction(n, 12) * 360 for n in (8, 2, 2)] == [240, 60, 60]
    assert Fraction(8, 12) != Fraction(8, 10)
    counts = [(3, 3, 2, 1), (3, 2, 2, 2)]
    assert [sum(values) for values in counts] == [9, 9]
    assert [sum(n == 3 for n in values) for values in counts] == [2, 1]
    assert 3 * (7 - 2) == 7 + 8 == 15 and 2 * (5 + 3) == 5 + 11 == 16
    assert datetime(2026, 1, 1, 10, 0, 15) - datetime(2026, 1, 1, 9, 59, 48) == timedelta(seconds=27)
    assert datetime(2026, 1, 1, 11, 58, 52) + timedelta(seconds=75) == datetime(2026, 1, 1, 12, 0, 7)
    for values, upper in [((1, 2, 3, 4, 9), 6.5), ((1, 2, 3, 4, 5), 4.5)]:
        assert (median(values[:2]), median(values), median(values[3:])) == (1.5, 3, upper)


    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    followup = '총괄평가 317~330쪽의 사례·루브릭과 부록 L 이후의 남은 대목, 공식 판면·도식과 인용 연구를 대조한다. 독립 검토와 학생 응답은 실제 자료로 확인한다.'
    book.update(review_scope=scope, next_review=followup)
    notes = dict(prior_notes, date=DATE, read_scope=scope, previous_review=previous,
                 previous_bibliography=prior_book,
                 revision_followup_extension=dict(
                     selected_pages=[[287, 288], [293, 299], [303, 305]], transcript_only=True,
                     group_examples=dict(displayed_learners=5, aggregated_learners=20,
                                         tables=['11.2', '11.3']),
                     worked_table_check=dict(table='11.8', transcribed_objective_count=1,
                                             transcribed_objective_percent=50, objective_denominator=4,
                                             row_alignment_verified=False),
                     assessment_and_material_changes_separated=True))
    notes['reading_log'] += [
        '287~288쪽 표 11.2·11.3의 개별 행 표시 범위와 전체 집계의 분모를 확인했다.',
        '293~299쪽에서는 전체 사전·사후 점수와 행동별 수행, 수업 중 문항으로 대신한 잠정적 비교, 태도 점수와 개방 응답을 구별했다.',
        '303~305쪽에서는 문항의 정오와 목표별 판정, 문제에 대한 변경안과 근거를 구별했다. 306쪽은 총괄평가의 시작이다.',
    ]
    notes['source_corrections'] += [
        dict(kind='displayed_subset', location='국제판 286~288쪽, 표 11.2·11.3',
             action='주석에 따라 개인 자료를 보이는 5명과 집계 20명을 구별했다. 표시된 행으로 전체 집계값을 재계산하지 않았다.'),
        dict(kind='objective_count_percent', location='국제판 304~305쪽, 표 11.8 전사',
             action='네 번째 위치의 목표 통과 수 1과 50%는 네 목표 기준으로 맞지 않는다. 같은 학생의 값으로 읽으면 1/4는 25%다. 열 정렬과 원전의 값은 공식 판면에서 확인한다. 전체 문항 정답률 9/12=75%와 별도다.'),
        dict(kind='embedded_response_limit', location='국제판 295~297쪽, 그림 11.3 전후 설명',
             action='사후 자료가 없어서 수업 중 수행을 잠정 비교에 사용한 경우를 확인했다. 후속 평가를 실제로 시행한 경우와 구별한다.'),
    ]

    notes['unread_followups'] = [followup]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    observations = [probe(int(cid[2:]), codes, question, expected, interpretation)
                    for cid, codes, _, _, _, question, expected, interpretation in MAPPINGS]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 표시 행과 전체 집계, 목표와 문항의 판정, 변경안과 변경 근거를 구별했다.',
                  editorial_action='성취기준 11개에 근거 6건과 자체 관찰 6건을 대응하고 관계별 대조 8건을 작성했다.',
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
    assert len({code for claim in new_claims.values() for code in claim['standard_codes']}) == 11
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
    print('Seventh international edition revision followup: 6 claims, 6 observation designs, 8 relation records')


if __name__ == '__main__':
    main()

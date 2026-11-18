"""Apply the newly reviewed school-case appendix and glossary passages."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_appendices_followup_review_notes.json'
PREVIOUS_SHA = '620714c229f79a8bb3e25a881872c26cb82ca7d6631af443a8174b68c10bd638'
SCOPE_ADDITION = ' 부록 L·M 국제판 364~369·371~372쪽과 용어집 373~379쪽의 선정 전사문을 대조했고 383~393쪽 색인은 탐색에 사용했다.'

MAPPINGS = [
    ('DC82', ['6수04-02', '6수04-03'], '국제판 365~367·371쪽, 전체와 하위집단의 포함 범위',
     '전체 인원과 그래프에 표시된 집단의 명단을 비교한다. 빠진 사례를 임의로 두 집단 중 하나에 넣지 않는다.',
     '서로 겹치지 않는 두 표시 집단이 전체를 모두 포함한다고 가정하지 않는다. 분모 14와 15를 명시한다.',
     '가상 탐구의 참여자는 15명이다. 그래프에는 1~4번과 6~15번 집단을 따로 보여 준다. 전체 15명을 분모로 두 집단과 그래프에 표시되지 않은 참여자의 원그래프 각도를 구하라. 두 집단만 분모로 한 그래프와 무엇이 다른가?',
     '전체를 분모로 하면 4명은 96°, 10명은 240°, 표시되지 않은 1명은 24°다. 두 집단만 대상으로 하면 분모는 14이고 전체 참여자 그래프와 구별해야 한다.',
     '그래프에 표시된 집단, 미표시 사례, 전체와 표시 집단의 분모, 근거 없이 분류하지 않았는지를 기록한다.'),
    ('DC83', ['9수04-02', '9수04-03'], '국제판 365~366쪽, 시점별 도수와 상대도수',
     '비교하는 두 시점과 분모를 밝힌다. 시점 사이의 퍼센트포인트 차이와 전체 기간의 차이를 따로 확인한다.',
     '시점별 집계만으로 어느 학생이 좋아지거나 나빠졌는지 결정하지 않는다.',
     '각 시점에 15명의 풀이 시간을 0초 이상 30초 미만과 30초 이상 60초 미만으로 분류했다. 첫 구간의 도수는 사전 5, 연습 14, 사후 10이다. 나머지 구간의 도수와 각 시점 첫 구간의 상대도수를 구하고 세 쌍의 차이를 퍼센트포인트로 비교하라.',
     '두 번째 구간의 도수는 각각 10, 1, 5다. 첫 구간은 5/15, 14/15, 10/15다. 사전→연습은 +60%p, 연습→사후는 약 −26.7%p, 사전→사후는 약 +33.3%p다.',
     '각 시점의 구간과 분모, 차이의 방향과 반올림, 개인 대응 자료가 있는지를 각각 확인한다.'),
    ('DC84', ['9수02-04'], '국제판 368~369·371~372쪽, 답 선택과 스스로 식 쓰기',
     '보기에서 고른 식과 학생이 상황을 읽고 세운 식을 별도로 확인한다. 바꾼 발문에서 무엇을 새로 기록할지 명시한다.',
     '식 선택을 맞혔다는 이유로 새 상황에서 미지수와 양의 관계를 스스로 정했다고 판단하지 않는다.',
     '공책 3권과 600원짜리 지우개를 사서 4200원을 냈다. 공책 한 권 값을 구하는 식을 3x+600=4200과 3(x+600)=4200 중 고르고 x의 뜻을 설명하라. 다음에는 보기 없이 공책 4권과 800원짜리 지우개를 사서 6000원을 냈을 때의 식과 답을 쓰라.',
     '첫 식은 3x+600=4200이며 x는 공책 한 권 값 1200원이다. 새 문제에서는 4x+800=6000이므로 x=1300원이다.',
     '보기 선택, 변수의 의미, 보기 없이 식을 세운 반응, 계산과 단위를 각각 기록한다.'),
    ('DC85', ['12실통02-01', '12실통02-02'], '국제판 367~369·372쪽, 태도 문항과 직접 자료',
     '도구가 쉬웠다는 응답과 실제 완료 시간의 자료 종류를 구별하고, 각각 어떤 질문에 필요한지 정한다.',
     '편의성 응답과 수행 시간만으로 도구가 성취도를 높였다고 판단하지 않는다.',
     '가상 활동에서 사용하기 쉬웠는지에 대한 예·아니요 응답과 풀이 완료 시간을 초 단위로 기록했다. 두 자료의 종류를 말하고 두 도구의 사용 경험과 풀이 시간을 비교하려면 각각 어떤 수집 방식이 적절한지 설명하라.',
     '예·아니요는 범주형이고 완료 시간은 수치형이다. 같은 질문으로 사용 경험을 묻고, 비슷한 난도의 과제와 같은 시간 기록 기준으로 완료 시간을 수집한다. 도구 순서가 영향을 줄 수 있으므로 순서를 기록한다.',
     '질문의 뜻, 자료 종류, 시간 기록 기준, 도구 순서와 수행 여부를 구별한다.'),
    ('DC86', ['6수01-10', '6수01-11'], '국제판 365·371쪽 및 376~377쪽 용어집, 출발 기능과 목표 사전 검사',
     '자연수 나눗셈의 몫을 분수로 표현하는 수행과 분수를 단위분수로 나누는 수행을 따로 확인한다.',
     '첫 과제의 성공만으로 분수의 나눗셈을 할 수 있다고 판단하지 않는다. 첫 과제가 모든 학습자에게 고정된 선행 순서라고 가정하지 않는다.',
     '주스 3L를 네 사람이 똑같이 나눌 때 한 사람이 받는 양을 분수로 쓰라. 별도 과제에서 그 양을 1/8L씩 따르면 몇 잔인지 그림이나 식으로 설명하라.',
     '한 사람은 3/4L를 받는다. 3/4L는 6/8L여서 1/8L씩 여섯 잔이다.',
     '자연수 나눗셈을 분수로 표현한 풀이와 분수 단위를 바꿔 잔 수를 구한 근거를 분리한다.'),
    ('DC87', ['6수02-02', '6수02-03'], '국제판 371~372쪽 및 378~379쪽 용어집, 새 적용 장면',
     '비를 같은 기준의 비율로 바꾸고, 장면이 달라져도 부분과 전체를 다시 확인하게 한다.',
     '주어진 식을 따라 계산한 응답만으로 새 장면에 적용했다고 판단하지 않는다. 전체 정보가 없는 경우에는 비율을 확정하지 않는다.',
     '과일 8개 중 사과가 3개일 때 사과 수와 전체의 비를 쓰라. 새 상황에서 책 24권 중 이야기책이 9권인 비율과 비교하라. 이야기책이 9권이라고만 알려 주면 무엇이 더 필요한가?',
     '비는 3:8과 9:24다. 비율은 둘 다 3/8=0.375=37.5%다. 이야기책 수만 주어지면 비율을 구하는 데 전체 책 수가 더 필요하다.',
     '두 상황의 전체, 비와 비율의 표현, 새 맥락에서 도움 없이 전체를 정했는지를 구분한다.'),
]

RELATIONS = [
    ('REV-6수04-03-2', 'DC82', '전체 15명과 표시된 14명을 구별하여 원그래프의 범주를 정한다.', '그림에 표시되지 않은 사례를 특정 집단에 넣지 않는다.'),
    ('REV-9수04-02-1', 'DC83', '같은 시간 구간의 도수와 상대도수를 세 시점에서 비교한다.', '집단 비율 차이와 개인 변화는 별도 자료가 필요하다.'),
    ('REV-6수01-11-2', 'DC86', '3÷4를 3/4로 나타낸 뒤 1/8 단위의 개수를 설명한다.', '몫의 분수 표현을 확인한 답을 분수 나눗셈의 증거로 합산하지 않는다.'),
    ('REV-6수01-10-2', 'DC86', '같은 양을 3/4L와 6/8L로 나타내 두 과제의 단위를 설명한다.', '한 사람의 주스 양과 잔 수의 단위를 구별한다.'),
    ('REV-6수02-03-1', 'DC87', '두 상황의 부분과 전체를 확인해 3:8과 9:24의 비율을 비교한다.', '부분만 주어진 상황에서 비율을 확정하지 않는다.'),
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
    assert [Fraction(n * 360, 15) for n in (4, 10, 1)] == [96, 240, 24]
    counts = (5, 14, 10)
    assert [15 - count for count in counts] == [10, 1, 5]
    assert [Fraction((counts[b] - counts[a]) * 100, 15) for a, b in ((0, 1), (1, 2), (0, 2))] == [60, Fraction(-80, 3), Fraction(100, 3)]
    assert 3 * 1200 + 600 == 4200 and 4 * 1300 + 800 == 6000
    assert Fraction(3, 4) / Fraction(1, 8) == 6
    assert Fraction(3, 8) == Fraction(9, 24) == Fraction('0.375')
    assert round(Fraction(100 * (14 - 5), 15)) == 60
    assert round(Fraction(100 * (10 - 14), 15)) == -27
    assert round(Fraction(100 * (15 - 5), 15)) == 67
    assert round(Fraction(100 * (12 - 15), 15)) == -20


    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    followup = '공식 판면에서 그림·표 정렬과 정오표를 확인하고, 이 책과 관련 문헌이 인용한 원연구의 대상·과제·결과와 한계를 이어서 대조한다. 독립 검토와 학생 응답은 실제 자료로 확인한다.'
    book.update(review_scope=scope, next_review=followup)
    notes = dict(prior_notes, date=DATE, read_scope=scope, previous_review=previous,
                 previous_bibliography=prior_book,
                 appendices_followup_extension=dict(
                     selected_appendices={'L': [364, 369], 'M': [371, 372]},
                     selected_glossary=[373, 379], index_locator_only=[383, 393],
                     transcript_only=True, table_layout_verified=False,
                     subgroup_scope=dict(all_learners=15, table_missing_entry_skills=[1,2,3,4,5],
                                         chart_without_entry_skills=[1,2,3,4], chart_with_entry_skills=list(range(6,16)),
                                         learner_absent_from_both_charts=5),
                     adjacent_counts=[5,14,10], adjacent_changes_rounded_pp=[60,-27],
                     before_after_exact_pp='100/3'))
    notes['reading_log'] += [
        '364~369쪽의 문항별 정오, 목표별 통과, 시점별 집계, 태도 응답을 구별했다.',
        '371~372쪽에서 표의 사례 5번과 그래프 집단의 차이, 보기 선택과 직접 작성, 변경안과 변경 근거를 확인했다.',
        '373~379쪽 용어집의 출발 기능·사전검사·전이 관련 표제어를 대조했다. 383~393쪽 색인은 표제어 탐색에만 이용했다.',
    ]
    notes['source_corrections'] += [
        dict(kind='subgroup_coverage', location='국제판 365~367·371쪽, 부록 L·M',
             action='표 주석의 1~5번, 그래프의 1~4번과 6~15번, 부록 M의 5번 사례 설명을 따로 보존했다. 두 그래프를 전원 15명의 완전 분할로 집계하지 않는다.'),
        dict(kind='time_difference_column', location='국제판 365~366쪽, 부록 L',
             action='차이 열 주석은 사전과 사후를 가리킨다. 인접한 5·14·10과 +60·−27은 인접 두 구간의 퍼센트포인트 차이와 맞으며 사전·사후 차이는 정확히 100/3 퍼센트포인트다. 열 정렬과 66 표기의 반올림 의도는 공식 판면에서 확인한다.'),
        dict(kind='selection_vs_production', location='국제판 371~372쪽, 부록 M',
             action='정형 문항의 사후 성공과 스스로 글을 쓰는 데 남은 어려움, 뉴스레터에 대한 태도와 실제 참여를 각각 확인했다. 변경안은 실제 시행 후의 효과를 뜻하지 않는다.'),
    ]

    notes['unread_followups'] = [followup]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    observations = [probe(int(cid[2:]), codes, question, expected, interpretation)
                    for cid, codes, _, _, _, question, expected, interpretation in MAPPINGS]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 전체와 하위집단, 비교하는 두 시점, 보기 선택과 실제 산출, 출발 기능과 목표를 구별했다.',
                  editorial_action='성취기준 11개에 근거 6건과 자체 관찰 6건을 대응하고 관계별 대조 5건을 작성했다.',
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
    print('Seventh international edition appendices followup: 6 claims, 6 observation designs, 5 relation records')


if __name__ == '__main__':
    main()

"""Apply the newly reviewed formative-evaluation and transfer passages."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_formative_followup_review_notes.json'
PREVIOUS_SHA = '5781375eeb6396f6e82bd1d4f4b0f5327e0009df8f4f0356575a481679d5290d'
SCOPE_ADDITION = ' 형성평가 국제판 259~264·269~281쪽의 선정 전사문을 추가로 대조했다.'

MAPPINGS = [
    ('DC64', ['4수01-09', '4수01-10'], '국제판 262~264·269~270쪽, 일대일 초안 점검',
     '도움 전에 전체의 기준과 한 조각을 설명하게 하고, 그림 읽기의 어려움을 별도로 확인한다.',
     '전체를 표시해 준 뒤의 응답으로 처음부터 그 기준을 스스로 정했다고 판단하지 않는다.',
     '같은 크기의 띠 두 장을 각각 세 등분했다. 한 장의 세 조각과 다른 장의 두 조각을 색칠했다. 띠 한 장을 전체로 하여 색칠한 양을 가분수와 대분수로 써라. 첫 풀이를 보존하고 필요하면 한 장의 경계를 표시한다. 이후 네 등분한 조각 일곱 개를 새 과제로 제시한다.',
     '처음은 5/3=1과 2/3, 새 과제는 7/4=1과 3/4다. 두 과제에서 각각 띠 한 장이 전체의 기준이다.',
     '첫 풀이의 전체, 표시 제공 여부와 수정 이유, 새 과제의 전체와 단위분수를 구분한다.'),
    ('DC65', ['4수04-01', '4수04-02'], '국제판 270~272·277~279쪽, 소집단과 현장 조건',
     '조에 제공한 축과 단위를 확인하고 조가 완성한 그래프와 학생 개인의 해석을 따로 수집한다.',
     '조별 산출물이나 교사가 읽어 준 값을 개인의 독립 수행으로 세지 않는다.',
     '가상 자료에서 월·화·수 수집량은 4병, 7병, 6병이다. 조별로 막대그래프와 꺾은선그래프를 그리고, 개인별로 화요일 수집량과 월요일에서 화요일까지의 증가량을 설명하라. 목요일의 실제 수집량도 알 수 있는가?',
     '요일별 양은 막대 높이와 꺾은선의 관측점으로 읽는다. 화요일 양은 7병이고 증가는 3병이다. 목요일 값은 제시되지 않았다.',
     '사용할 수 있었던 축 자료, 조별 작성, 개인 설명 및 교사의 추가 발문을 따로 남긴다.'),
    ('DC66', ['9수02-05', '9수02-06'], '국제판 272~275쪽, 태도와 직접 수행',
     '그래프를 읽기 편하다는 응답과 좌표 순서 및 단위를 해석한 답을 각각 확인한다.',
     '어려움이나 자신감의 응답을 좌표 해석 점수로 바꾸지 않는다.',
     '가로축은 출발 뒤 시간(분), 세로축은 출발점에서의 거리(m)다. 점 (3,12), (5,12)를 읽고 시간 차와 두 거리 값의 차를 설명하라. 별도로 축 이름이 잘 보였는지 적어라.',
     '3분과 5분에 거리는 각각 12m다. 시간 차는 2분, 두 거리 값의 차는 0m다. 두 점만으로 그 사이에 움직이지 않았다고 확정할 수 없다.',
     '좌표 순서와 단위, 관측 사이에 대한 해석, 읽기 편의 응답을 따로 기록한다.'),
    ('DC67', ['9수04-05', '9수04-06'], '국제판 259~261·275~276쪽, 적용 기회와 후속 응답',
     '새 과제에서 방법을 썼다고 말한 응답과 직접 경우를 세고 확률을 계산한 기록을 구별한다.',
     '과제를 받지 않았거나 방법을 써 볼 기회가 없었던 경우를 오답이나 미적용으로 합산하지 않는다.',
     '서로 독립인 공정한 동전 두 개를 한 번씩 던져 앞면이 정확히 한 개인 확률을 구하라. 이후 새 과제에서 서로 독립인 공정한 1~4 회전판과 동전을 한 번씩 사용해 짝수와 앞면이 함께 나올 확률을 구하라.',
     '첫 과제는 네 등확률 결과 중 두 개여서 1/2이다. 새 과제는 여덟 등확률 결과 중 (2, 앞면), (4, 앞면) 두 개여서 1/4이다.',
     '새 과제 제공 여부, 열거 또는 곱의 근거, 자기보고와 직접 수행, 추가 단서를 구분한다.'),
    ('DC68', ['6수04-03', '9수04-07'], '국제판 259~261·277~279쪽, 자료 수집과 수행 맥락',
     '자료 수집 조건과 실제 적용에서 쓸 수 있었던 도구를 기록한다. 관찰한 자료의 퍼짐을 비교한 근거를 살핀다.',
     '도구 부족과 설명 부족을 같은 이유로 처리하지 않는다. 가상 자료에서 관찰한 차이를 다른 집단까지 확장하지 않는다.',
     '같은 시간대와 단위로 기록한 가상 대기 시간이 A=(2,4,6), B=(3,4,5)분이다. 같은 눈금의 점그래프로 비교하라. 분산을 배운 뒤에는 각 자료의 관측값 개수로 나누어 분산을 구하고 해석하라.',
     '평균은 각각 4분이다. A의 분산은 8/3분², B는 2/3분²이므로 표준편차도 A가 더 크다. 비교는 제시된 관측값에 대한 것이다.',
     '초등의 자료 수집 계획·그래프 해석과 중학교의 분산 계산을 별도로 기록하고 자료 조건과 도구 이용 여부를 남긴다.'),
    ('DC69', ['10공수2-03-03'], '국제판 273~279쪽, 후속 확인 시점과 새 과제',
     '역관계가 함수가 되는 이유를 새 정의역에서 설명하게 하고, 이전 풀이의 단서를 다시 보여 줬는지 기록한다.',
     '이전 예의 재현과 새 조건에서의 판단을 구별한다. 설문 예시의 1년을 고정 간격으로 적용하지 않는다.',
     'f(x)=x²의 정의역이 {-2,0,2}, 공역이 {0,4}일 때 역함수가 있는지 설명하라. 이후 정의역을 {0,2}로 바꾸고 같은 공역을 유지한 새 과제에서 다시 판단하고 역함수의 값을 적어라.',
     '첫 함수에서 4의 원상이 -2와 2이므로 역관계는 함수가 아니다. 새 함수는 일대일 대응이며 역함수는 0↦0과 4↦2다.',
     '정의역과 공역, 출력에 대응하는 입력 수, 두 과제 사이 시간과 추가 도움을 구분한다.'),
]

RELATIONS = [
    ('REV-4수01-10-1', 'DC64', '띠 한 장을 단위로 하여 1/3을 다섯 번 모은 양을 두 분수 형식으로 표현한다.', '전체 경계 표시 시점과 새 단위분수의 독립 설명을 구별한다.'),
    ('REV-4수04-02-1', 'DC65', '막대 높이와 꺾은선의 관측점에서 7병과 3병 증가를 구별한다.', '개인 해석과 조별 작성 기록을 각각 확인한다.'),
    ('REV-9수02-05-1', 'DC66', '좌표의 두 성분을 각 축의 단위로 읽어 시간과 거리 값의 차를 설명한다.', '자료 읽기 편의 응답과 좌표 해석을 따로 확인한다.'),
    ('REV-9수04-05-1', 'DC67', '네 등확률 결과와 여덟 등확률 결과를 각각 세어 두 확률을 구한다.', '새 과제 제공 여부와 학생의 직접 수행을 구별한다.'),
    ('SEC_9수04-07_C02', 'DC68', '같은 눈금으로 퍼짐을 살핀 뒤 분산으로 비교 근거를 명시한다.', '자료 수집 조건, 도구 이용 여부와 계산 근거를 각각 기록한다.'),
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
    assert divmod(5, 3) == (1, 2) and divmod(7, 4) == (1, 3)
    assert 7 - 4 == 3 and (5 - 3, 12 - 12) == (2, 0)
    assert Fraction(sum(a + b == 1 for a in (0, 1) for b in (0, 1)), 4) == Fraction(1, 2)
    assert Fraction(sum(x % 2 == 0 and face == 1 for x in range(1, 5) for face in (0, 1)), 8) == Fraction(1, 4)
    for values, expected in [((2, 4, 6), Fraction(8, 3)), ((3, 4, 5), Fraction(2, 3))]:
        assert Fraction(sum(values), len(values)) == 4
        assert Fraction(sum((value - 4) ** 2 for value in values), len(values)) == expected
    assert [x for x in (-2, 0, 2) if x ** 2 == 4] == [-2, 2]
    assert {x ** 2: x for x in (0, 2)} == {0: 0, 4: 2}


    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    followup = '자료 수정 287~288·293~299·303~306쪽과 총괄평가의 나머지, 부록 L 이후, 공식 판면·도식과 인용 연구를 대조한다. 독립 검토와 학생 응답은 실제 자료로 확인한다.'
    book.update(review_scope=scope, next_review=followup)
    notes = dict(prior_notes, date=DATE, read_scope=scope, previous_review=previous,
                 previous_bibliography=prior_book,
                 formative_followup_extension=dict(
                     selected_pages=[[259, 264], [269, 281]], transcript_only=True,
                     transfer_opportunity_separated_from_performance=True,
                     use_report_separated_from_direct_performance=True,
                     trial_stages=['one_to_one', 'small_group', 'field_trial'],
                     survey_prompt_discrepancy=dict(general_figure='10.2', case_figure='10.4',
                                                   official_layout_verified=False),
                     survey_one_year_is_example_prompt=True))
    notes['reading_log'] += [
        '259~261쪽은 적용 기회와 지원, 사용 여부의 자기보고와 직접 관찰, 목표에 따라 달라지는 확인 시점을 구별한다.',
        '261~264·269~272쪽은 일대일의 직접 질문과 초안, 소집단의 준비 자료와 진행 조건을 구별한다. 제안된 최소 참여 인원은 효능 판정 기준이 아니다.',
        '273~279쪽에서 태도 응답과 후속 설문 및 현장 시험을 구분했다. 279~281쪽은 참고문헌의 인용 목록을 확인했다.',
    ]
    notes['source_corrections'] += [
        dict(kind='transfer_survey_prompt', location='국제판 260~261·275~276쪽, 그림 10.2와 10.4',
             action='일반 양식은 미사용 이유를 묻는다. 사례 양식 B절 제목과 선택 항목도 미사용에 해당하나 마지막 개방형 발문은 사용 중인 이유라고 전사돼 있다. 이 문구 차이는 공식 판면에서 확인한다.'),
        dict(kind='survey_time_example', location='국제판 275~276쪽, 그림 10.4',
             action='워크숍 뒤 1년이 지났다는 문장은 설문 예문의 문구다. 실제 관측 시점이나 모든 후속 평가의 필요 간격으로 등록하지 않았다.'),
        dict(kind='field_trial_scope', location='국제판 277~279쪽, 학교 사례와 피드백',
             action='학교 작문 사례는 두 맥락이 같다고 설명하며 별도의 적용 맥락 평가를 제안하지 않는다. 그 사례의 조건으로 보존하고 실제 대상, 자료와 운영 조건을 기록한다.'),
    ]

    notes['unread_followups'] = [followup]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    observations = [probe(int(cid[2:]), codes, question, expected, interpretation)
                    for cid, codes, _, _, _, question, expected, interpretation in MAPPINGS]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 첫 반응과 도움 뒤 수정, 자기보고와 새 과제의 실제 수행 및 적용 기회를 구별했다.',
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
    print('Seventh international edition formative followup: 6 claims, 6 observation designs, 5 relation records')


if __name__ == '__main__':
    main()

"""Apply the newly reviewed instructional-strategy and school case passages."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_strategy_followup_review_notes.json'
PREVIOUS_SHA = '47133e60cea78cf638dc5ef766d5823f02e3e0773491ac6afed3a9efb41372ba'
SCOPE_ADDITION = ' 수업 전략 국제판 171~180·187~189·192~209쪽과 부록 F·G·H 343~347·349~352쪽의 선정 전사문을 추가로 대조했다.'

MAPPINGS = [
    ('DC52', ['4수01-13', '4수01-14'], '국제판 171~172·343~346쪽, 회상 단서와 새 문항의 수행',
     '소수를 읽고 자릿값을 확인하는 일과, 표시가 없는 새 수에서 크기를 설명하는 일을 나누어 기록한다. 자릿값 표를 언제 제시했는지도 남긴다.',
     '한 번의 비교나 단서를 제공한 뒤의 설명을 근거로 다른 수에서도 독립적으로 비교한다고 판단하지 않는다.',
     '0.407과 0.47의 크기를 먼저 비교하고 이유를 적어라. 자릿값 표로 두 수를 확인한 뒤 표를 치우고 1.205와 1.25를 비교해 설명하라.',
     '0.47은 0.470과 같아서 0.407보다 크다. 1.25는 1.250과 같아서 1.205보다 크다. 두 쌍 모두 소수 첫째 자리는 같고 둘째 자리에서 크기가 달라진다.',
     '자릿값 표를 보기 전 답과 설명, 표를 보며 고친 설명, 표를 치운 뒤의 비교를 구분한다. 뒤 문항 한 개의 결과를 장기 유지로 해석하지 않는다.'),
    ('DC53', ['6수04-03', '9수04-04'], '국제판 175~180·349~352쪽, 공동 탐구와 개인 수행',
     '모둠이 정한 수집 조건과 공동 그래프, 각 학생이 설명하는 결론과 그 근거를 나누어 기록한다. 공학 도구를 누가 사용했는지도 확인한다.',
     '제공된 예시 자료의 그래프를 그리는 일과 실제 조사·개별 도구 사용은 다른 수행이다. 다섯 날의 관측에서 원인이나 다른 기간의 결과를 추정하지 않는다.',
     '급식실 두 줄에서 같은 시각에 다섯 날 동안 기다리는 학생을 센다고 하자. 비교에 필요한 수집 조건을 정하고, 연습 자료 A=(12,18,15,19,16), B=(8,13,14,15,10)를 그래프로 나타내라. 모둠 발표 뒤 각자 어떤 결론이 자료에서 나오는지 설명하라.',
     '두 줄을 같은 날 같은 시각에 관측하고 줄의 범위를 같은 기준으로 정한다. 같은 세로 눈금에서 날별 인원을 비교할 수 있다. 다섯 날 평균은 A가 16명, B가 12명이다. 이 표만으로 차이가 난 원인이나 다른 시기의 인원을 말할 수 없다.',
     '조건·축·결론을 누가 제안했는지와 발표 뒤의 개인 설명을 기록한다. 공학 도구의 직접 조작 여부는 중학교 과제에서 따로 확인한다.'),
    ('DC54', ['12수과02-02', '12수과02-03'], '국제판 175~180·202~207쪽, 주어진 사례와 직접 탐구의 구분',
     '이미 제시된 사례에서 확인한 정보, 실험에서 직접 만든 사례, 그 결과를 정당화하는 설명을 분리한다.',
     '정해진 범위의 실험이 맞았다고 해서 모든 정수에 대한 명제가 성립하는 것은 아니다. 정당화는 실험 기록과 구별한다.',
     '1×2, 2×3, 3×4의 사례에서 공통점을 찾아라. 이어 시작하는 수를 0과 −3으로 바꾸어 직접 계산한 뒤, 연속한 두 정수의 곱이 항상 짝수인지 판단하라.',
     '제시된 곱은 2,6,12로 모두 짝수다. 새로 계산한 0×1은 0이고 (−3)×(−2)는 6이다. 연속한 두 정수 중 하나는 짝수라 모든 경우에 그 곱은 2의 배수다.',
     '주어진 세 사례, 직접 추가한 사례, 일반 설명을 각각 남긴다. 모둠이 만든 설명은 다른 예에서 개인이 설명한 반응과 나누어 기록한다.'),
    ('DC55', ['9수02-02', '9수02-03'], '국제판 345~347쪽, 단서가 있는 분류와 새로운 예의 생성',
     '주어진 식에서 동류항을 정리한 결과와 등식을 참으로 만드는 수를 구분한다. 스스로 새로운 예를 만들었는지 따로 확인한다.',
     '기호가 강조된 예를 알아본 결과만으로 모든 x에서 성립하는지, 특정 해에서만 성립하는지 설명했다고 판단하지 않는다.',
     '4x+(2−x)를 정리한 뒤 4x+(2−x)=3x+2와 4x+(2−x)=14가 각각 언제 참인지 말하라. x=5에서 참이 되는 두 번째 식과 같은 꼴의 방정식을 만들어라.',
     '왼쪽은 3x+2다. 첫 등식은 모든 x에서 참이고, 둘째는 3x+2=14이므로 x=4에서 참이다. x=5에서 왼쪽이 17이므로 오른쪽이 17인 식을 만들 수 있다.',
     '항을 정리한 근거, 두 등식이 참인 범위, 새로운 오른쪽을 고른 이유를 따로 본다. 밑줄이나 색으로 동류항을 미리 알려 준 경우도 기록한다.'),
    ('DC56', ['6수02-04', '6수02-05'], '국제판 187~189·343~344쪽, 목표별 연습과 이후 적용 점검',
     '비례배분에서 전체가 달라진 경우에도 두 부분의 합과 비가 조건에 맞는지 확인한다. 연습 때 제공한 풀이 표와 표 없이 한 설명을 구별한다.',
     '표 없이 한 새 계산은 해당 문항의 반응이다. 비례식 풀이 전체의 성취나 오래 뒤의 적용을 대신하지 않는다.',
     '96개를 3:5로 나눠라. 전체가 104개로 바뀌면 앞서 쓴 풀이 표 없이 두 양을 구하고 합과 비를 각각 확인하라.',
     '전체를 같은 크기의 8부분으로 보면 96개에서는 36개와 60개, 104개에서는 39개와 65개다. 각각 합이 원래 전체와 같고 36:60과 39:65는 모두 3:5로 줄일 수 있다.',
     '첫 과제에서 표를 받았는지, 둘째에서 전체 부분 수를 스스로 정했는지, 합과 비를 각각 검산했는지 남긴다.'),
    ('DC57', ['12직수02-03'], '국제판 192~204·349~352쪽, 자료로 규칙을 읽는 일과 직접 쓰는 일',
     '주어진 표를 읽는 수행과 조건을 설명하고 새 대응값을 만드는 수행을 나누어 관찰한다.',
     '몇 개의 대응만으로 모든 경우의 규칙을 확정하지 않는다. 실제 조건과 표에서 추정한 규칙을 구분한다.',
     '한 작업에서 상자마다 부품 6개를 넣고 예비 부품 2개를 작업 전체에 한 번만 준비한다. 상자 1, 3, 5개에 필요한 부품의 표를 만든 뒤 상자 4개인 행을 추가하고 규칙을 말하라.',
     '1, 3, 5개에 각각 8, 20, 32개가 필요하고 4개에는 26개가 필요하다. 상자 수를 n이라 하면 필요한 수는 6n+2다. 예비 부품 2개를 상자마다 더하지 않는다.',
     '주어진 조건, 표 작성, 새 행, 고정된 2개의 의미를 각각 기록한다. 이미 계산된 표를 제공한 경우 학생이 직접 만든 부분을 구분한다.'),
]

RELATIONS = [
    ('REV-4수01-14-1', 'DC52', '같은 소수에 끝의 0을 붙여 자릿값을 맞춘 뒤 표 없이 새 수를 비교한다.', '단서가 있는 풀이와 단서를 치운 뒤의 설명을 분리한다.'),
    ('SEC_9수04-04_C02', 'DC53', '같은 조건에서 수집한 두 줄의 날별 값을 동일한 축에서 비교한다.', '제공된 수의 해석과 실제 수집을 따로 본다.'),
    ('SEC_9수04-04_C03', 'DC53', '모둠 그래프가 나타내는 범위와 각 학생이 설명한 결론을 구별한다.', '모둠의 결론을 모든 학생의 개별 수행으로 세지 않는다.'),
    ('AN_6수04-03_C01', 'DC53', '탐구 질문과 그래프의 관측 단위가 맞는지 확인한 뒤 도구 사용 기록을 덧붙인다.', '초등의 질문·해석 수행에 중학교의 공학 도구 조작을 일률적으로 요구하지 않는다.'),
    ('REV-6수02-05-1', 'DC56', '전체가 달라도 두 배분량의 합과 비를 각각 확인한다.', '표를 제공한 연습과 표를 치운 뒤 독립적으로 구한 배분을 나누어 기록한다.'),
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
    assert Fraction('0.407') < Fraction('0.47') and Fraction('1.205') < Fraction('1.25')
    assert Fraction(sum((12, 18, 15, 19, 16)), 5) == 16
    assert Fraction(sum((8, 13, 14, 15, 10)), 5) == 12
    assert [x * (x + 1) for x in (1, 2, 3, 0, -3)] == [2, 6, 12, 0, 6]
    assert 4 * 4 + (2 - 4) == 14 and 4 * 5 + (2 - 5) == 17
    assert [(total * Fraction(3, 8), total * Fraction(5, 8)) for total in (96, 104)] == [(36, 60), (39, 65)]
    assert [6 * n + 2 for n in (1, 3, 5, 4)] == [8, 20, 32, 26]

    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    followup = '자료 개발 222~243쪽의 사례·점검과 관련 부록 I·J, 형성평가의 미검토 대목, 공식 판면·도식과 인용 연구를 대조한다. 독립 검토와 학생 응답은 실제 자료로 확인한다.'
    book.update(review_scope=scope, next_review=followup)
    notes = dict(prior_notes, date=DATE, read_scope=scope, previous_review=previous,
                 previous_bibliography=prior_book,
                 strategy_followup_extension=dict(
                     selected_strategy_pages=[[171, 180], [187, 189], [192, 209]],
                     selected_appendix_pages={'F': [343, 344], 'G': [345, 347], 'H': [349, 352]},
                     explicit_blank_boundaries=[342, 348],
                     transcript_only=True, diagram_connections_from_text=False,
                     session_13=dict(general_plan_figure='8.6', session_detail_figure='8.8',
                                     pretest=False, posttest=False, rehearsal=True)))
    notes['reading_log'] += [
        '171~180쪽에서 회상 단서, 새로운 환경에서의 적용, 직접 수행과 모의 사례, 복합 탐구에서의 학습 지원을 구분했다.',
        '187~189·192~209쪽의 계획·사례·점검에서 목표별 연습과 평가, 학습자 편성, 매체 제공과 실제 참여를 대조했다.',
        '부록 F·G·H에서 시작 조건과 분기, 분류 단서와 새로운 예 작성, 개별 작업과 공동 산출물을 나누었다.',
    ]
    notes['source_corrections'] += [
        dict(kind='session_level_assessment_exception', location='국제판 193쪽 그림 8.6과 199쪽 그림 8.8',
             action='각 회기의 사전·사후 평가를 설명한 일반 계획과 13회기에 평가를 시행하지 않는 개별 배정을 함께 남겼다. 13회기의 모둠 연습을 시험 결과나 결측 응답으로 세지 않는다.'),
        dict(kind='planned_time_by_setting', location='국제판 93~94쪽 표 5.6과 201쪽 표 8.6',
             action='센터에서 정한 15시간과 다른 설계에서 가능한 2시간짜리 14회기를 각 계획의 표기로 보존했다. 운영 맥락과 실제 실시 시간을 확인하기 전 단일 분모로 합치지 않는다.'),
        dict(kind='appendix_page_labels', location='국제판 342~352쪽, 부록 F·G·H 경계',
             action='부록의 국제판 쪽과 원서 쪽 번호를 따로 기록했고, 빈 쪽 안내를 본문 읽기 또는 사례 수에 넣지 않았다.'),
    ]
    notes['unread_followups'] = [followup]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    observations = [probe(int(cid[2:]), codes, question, expected, interpretation)
                    for cid, codes, _, _, _, question, expected, interpretation in MAPPINGS]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 수업의 단서, 개인과 모둠의 수행, 회기별 평가 계획을 구분했다.',
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
    print('Seventh international edition strategy followup: 6 claims, 6 observation designs, 5 relation records')


if __name__ == '__main__':
    main()

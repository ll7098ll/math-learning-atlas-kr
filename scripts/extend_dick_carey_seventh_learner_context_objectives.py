"""Apply the newly reviewed learner, context, and objective passages to mathematics tasks."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_learner_context_objectives_review_notes.json'
PREVIOUS_SHA = '9257218357eee9bc521d6b995bf741699114c2dc6d18449c223c186f07071d5a'
SCOPE_ADDITION = ' 학습자·맥락 분석 국제판 88~97쪽과 부록 D 337~338쪽, 수행목표 99~101·108~114쪽의 선정 전사문을 추가로 대조했다.'

MAPPINGS = [
    ('DC40', ['6수01-14', '6수01-15'], '국제판 88~91쪽의 표 5.1·5.4와 부록 D 337쪽, 학습 이력과 초기 수행',
     '소수 몫을 배웠다는 응답과 실제 계산·설명을 구분한다. 자연수 나눗셈의 소수 몫과 나누는 수가 소수인 나눗셈에서 각각 한 일을 확인한다.',
     '이전 단원 이수나 한 문항의 결과로 소수 나눗셈 전체의 능력을 판단하지 않는다.',
     '5÷4와 1.5÷0.4의 몫을 각각 구하고 어떻게 계산했는지 설명하라. 둘째 식을 자연수로 나누는 식으로 바꾸면 무엇이 함께 달라지는가?',
     '5÷4=1.25다. 1.5÷0.4는 나누어지는 수와 나누는 수를 모두 10배 하면 15÷4가 되고 몫은 3.75다. 한쪽만 10배 하면 몫이 달라진다.',
     '배웠다는 응답, 도움 없는 첫 풀이, 두 수를 함께 바꾸는 이유를 따로 기록한다. 힌트를 준 경우 첫 풀이와 나중 설명을 분리한다.'),
    ('DC41', ['12실통02-02', '12실통02-03'], '국제판 88~89·92~97쪽, 수집 범주·자료원·실제 수행 맥락',
     '조사 목적에 맞는 관측 단위와 자료 수집 조건을 정하고, 같은 질문에 답하도록 자료와 그래프를 연결한다.',
     '연습 자료의 그래프 작성은 실제 조사나 표본의 대표성을 확인한 기록과 구분한다.',
     '점심시간에 도서관 이용자가 많은 때를 알고 싶다. 한 번에 안에 있는 인원을 비교하는 질문에 맞춰 수집 방법을 정하라. 연습 기록인 12:10의 8명, 12:20의 14명, 12:30의 10명을 그래프로 나타내고 어떤 결론을 내릴 수 있는지 말하라.',
     '같은 출입 기준과 관측 지점에서 정해진 시각마다 그때 안에 있는 인원을 센다. 시각과 인원을 축에 표시하면 세 시각 가운데 12:20의 14명이 가장 많다. 이 값들을 더하면 같은 이용자를 중복해서 셀 수 있으므로 하루의 고유 이용자 수로 해석할 수 없다.',
     '학생이 고른 관측 단위, 그래프의 축, 자료가 뒷받침하는 결론을 각각 확인한다. 다른 날도 비교하려면 요일과 시각 등 수집 조건을 함께 기록한다.'),
    ('DC42', ['12인수04-02'], '국제판 93~96쪽의 도구·지원 조건과 부록 D 338쪽의 실제 이용 가능성',
     '공학 도구에 입력한 관측값, 사용한 추세선, 새 자료의 예측과 실제 결과를 구분한다. 도구를 학생이 직접 조작했는지 기록한다.',
     '공학 도구가 제공되지 않았거나 작동 여부를 모르는 상황에서 계산 결과를 도구의 독립 사용 증거로 쓰지 않는다.',
     '공학 도구에 (1,11), (2,14), (3,17)을 넣고 일차 추세선을 구해 x=4의 값을 예측하라. 이후 관측한 x=4의 실제 값이 18이라면 실제값에서 예측값을 뺀 값을 설명하라.',
     '세 점은 y=3x+8에 있어 x=4의 예측값은 20이다. 새 관측값 18에서 예측값 20을 빼면 −2다. 세 점에 잘 맞는 추세선이 새 값과 일치한다고 보장할 수는 없다.',
     '추세선을 구하는 데 쓴 점과 나중에 알려 준 점을 구별한다. 학생이 직접 입력했는지, 식이나 화면을 대신 제공했는지 남긴다.'),
    ('DC43', ['10공수2-02-03', '10공수2-02-04'], '국제판 100~101·112~114쪽, 이름을 말하는 반응과 조건을 적용한 수행',
     '집합 이름을 말하는 일과 원소를 분류하고 명제의 참·거짓을 설명하는 일을 구분한다. 판단할 전체 집합과 반례의 범위를 발문에 명시한다.',
     '그림에 표시된 영역의 이름을 맞혔다는 사실로 모든 원소나 어떤 원소가 조건을 만족하는지 설명했다고 판단하지 않는다.',
     '전체집합 {1,2,3,4,5,6}에서 A는 짝수의 집합, B는 3의 배수의 집합이다. 교집합을 구한 뒤 모든 A의 원소가 B에 속한다는 말과 어떤 A의 원소는 B에 속한다는 말을 각각 판단하라.',
     'A={2,4,6}, B={3,6}, A∩B={6}이다. 2가 A에는 속하고 B에는 속하지 않으므로 첫 명제는 거짓이다. 6이 양쪽에 속하므로 둘째 명제는 참이다.',
     '영역 표시, 반례 2의 사용, 존재를 보이는 6의 사용을 각각 확인한다. 반례와 존재의 근거를 교사가 미리 줬는지도 기록한다.'),
    ('DC44', ['12미적Ⅰ-02-07', '12미적Ⅰ-02-08'], '국제판 108~109·114쪽, 목표에 맞는 문항과 관찰 가능한 판정 기준',
     '도함수의 부호, 그래프의 개형, 닫힌 구간에서의 가장 큰 값과 작은 값을 묻는 경우에 필요한 비교를 각각 관찰한다.',
     '증가·감소를 맞힌 결과로 끝점까지 확인했거나 그래프의 개형을 설명했다고 판단하지 않는다.',
     'f(x)=x³−3x²의 도함수 부호를 이용해 −1≤x≤3의 개형을 그려라. 이 구간에서 가장 큰 값과 가장 작은 값이 각각 어디에서 나오는지 모두 표시하라.',
     'f′(x)=3x(x−2)다. −1부터 0까지 증가하고, 0부터 2까지 감소하고, 2부터 3까지 증가한다. f(−1)=f(2)=−4이고 f(0)=f(3)=0이다. 최댓값은 0으로 x=0,3에서 나오고 최솟값은 −4로 x=−1,2에서 나온다.',
     '도함수의 부호, 양 끝점과 내부 후보를 비교한 근거, 같은 값을 얻는 위치를 모두 표시했는지 따로 기록한다.'),
    ('DC45', ['9수03-12', '9수03-13'], '국제판 108~109·112~114쪽, 목표 수행에 맞춘 문항과 조건이 달라질 때의 판정',
     '두 삼각형의 대응을 밝히고, 닮음 조건을 충족하는 데 필요한 비교를 드러내는 문항을 둔다.',
     '주어진 예에서 두 쌍의 변 비가 같다는 사실만으로 닮음을 결론 내리지 않는다. 각 조건을 함께 주는 다른 과제와 구별한다.',
     '변 길이가 3,4,5인 삼각형을 6,8,10인 삼각형 및 6,8,11인 삼각형과 각각 비교한다. 그림 없이 닮음 여부와 닮은 경우의 확대 배율을 설명하라.',
     '6,8,10은 짧은 변부터 대응시키면 세 비가 모두 2여서 닮았다. 6,8,11은 처음 두 비가 2지만 마지막 비가 11/5이므로 닮지 않았다. 두 번째도 6+8>11이므로 삼각형을 이룬다.',
     '대응 변, 비교에 사용한 닮음 조건, 닮음이 성립하는 경우의 배율을 나누어 본다. 학생에게 짝을 알려 주기 전의 풀이도 남긴다.'),
]

RELATIONS = [
    ('REV-6수01-15-1', 'DC40', '두 수를 함께 10배 해 1.5÷0.4를 15÷4로 바꾼 뒤 소수 몫을 설명한다.',
     '자연수끼리 나눈 한 사례의 정답만으로 나누는 수가 소수일 때의 변형을 확인할 수 없다.'),
    ('REV-9수03-12-1', 'DC45', '세 대응 변의 비를 모두 비교하고 닮은 경우의 확대 배율을 기록한다.',
     '6,8,11의 두 비가 같다는 사실만으로 세 변을 비교하는 닮음 조건을 충족하지 않는다.'),
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
    assert Fraction(5, 4) == Fraction('1.25')
    assert Fraction('1.5') / Fraction('0.4') == Fraction(15, 4) == Fraction('3.75')
    assert max(((10, 8), (20, 14), (30, 10)), key=lambda pair: pair[1]) == (20, 14)
    assert [3 * x + 8 for x in (1, 2, 3, 4)] == [11, 14, 17, 20] and 18 - 20 == -2
    assert {2, 4, 6} & {3, 6} == {6} and 2 not in {3, 6}
    assert [x ** 3 - 3 * x ** 2 for x in (-1, 0, 2, 3)] == [-4, 0, -4, 0]
    assert [Fraction(a, b) for a, b in zip((6, 8, 10), (3, 4, 5))] == [2, 2, 2]
    assert 6 + 8 > 11 and Fraction(11, 5) != 2

    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    followup = '평가 도구 129~133·137~151쪽과 각 장·부록의 미검토 대목, 공식 판면·도식과 인용 연구를 대조한다. 독립 검토와 학생 응답은 실제 자료로 확인한다.'
    book.update(review_scope=scope, next_review=followup)
    notes = dict(prior_notes, date=DATE, read_scope=scope, previous_review=previous,
                 previous_bibliography=prior_book,
                 learner_context_objectives_extension=dict(
                     learner_and_context_pages=[88, 97], school_case_appendix_d_pages=[337, 338],
                     selected_objectives_page_ranges=[[99, 101], [108, 114]],
                     transcript_only=True, diagram_connections_from_text=False,
                     independent_review=False, student_validated=False))
    notes['reading_log'] += [
        '88~97쪽 표 5.1~5.6과 사례·점검·연습에서 확인할 범주, 수집 방법, 확인한 내용과 조건이 바뀐 상황을 나누었다.',
        '부록 D 337~338쪽에서 수업 이력과 실제 작문, 장비 지급과 작동, 교실과 집의 접근 조건을 대조했다.',
        '99~101·108~114쪽의 선정 대목에서 목표의 실제 적용 조건과 수업 종료 평가의 조건, 수행을 확인할 문항과 관찰 기준을 구분했다.',
    ]
    notes['source_corrections'] += [
        dict(kind='case_participants_and_plan', location='국제판 91~92쪽 표 5.4·5.5',
             action='이전 연수 16명의 의견, 장소당 20명 운영 계획, 관찰한 3개 회의는 서로 다른 기록이다. 계획 인원으로 실제 관찰 인원을 대신하지 않는다.'),
        dict(kind='case_equipment_ranges', location='국제판 93~94쪽 표 5.6',
             action='시설 설명의 컴퓨터 5~6대와 일정 조정 항목의 5~8대를 각각 남겼다. 같은 장소에서 실제 사용 가능한 대수로 확정하려면 운영 자료가 필요하다.'),
        dict(kind='school_site_and_access', location='국제판 337~338쪽 부록 D',
             action='학교 사례의 학습 장소와 수행 장소를 같은 곳으로 다룬 조건을 보존했다. 집에서의 도구·연결 조건과 장비의 지급·작동 상태를 따로 기록한다.'),
    ]
    notes['unread_followups'] = [followup]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    observations = [probe(int(cid[2:]), codes, question, expected, interpretation)
                    for cid, codes, _, _, _, question, expected, interpretation in MAPPINGS]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 학습 이력과 초기 수행, 도구 제공과 실제 사용, 과제 조건과 판정 근거를 구별했다.',
                  editorial_action='성취기준 11개에 근거 6건과 자체 관찰 6건을 대응하고 관계별 대조 2건을 작성했다.',
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
    print('Seventh international edition learner context and objectives: 6 claims, 6 observation designs, 2 relation records')


if __name__ == '__main__':
    main()

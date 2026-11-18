"""Map the seventh international edition assessment reading to current tasks."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


NOTES = 'data/literature_evidence/DICK_CAREY_2014_assessment_revision_review_notes.json'
PREVIOUS_SHA = 'f6f81fa01018bdc8353a06d582a6c8f84e7a553bfac28d8592ce9582ba2b082f'
SCOPE_ADDITION = (' 수행목표와 평가(국제판 102~107, 119~128, 134~136쪽), 형성평가(245~258, 265~268쪽)와 '
                  '자료 수정(283~286, 289~292, 300~302쪽)의 선정 본문을 더 확인했다.')

MAPPINGS = [
    ('DC14', ['4수01-12', '4수01-13'], '국제판 102~107쪽, 수행의 조건과 판정 기준',
     '눈금의 시작값과 끝값, 같은 크기의 구간 수, 지정 점의 소수 표현을 분리해 과제의 조건과 관찰 기준으로 쓴다.',
     '점 하나를 정확히 쓴 답으로 구간 수나 자릿값 설명까지 확인했다고 집계하지 않는다. 주어진 소수 눈금의 범위에 한정한다.'),
    ('DC15', ['2수01-06'], '국제판 119~123쪽, 평가의 목적별 구별',
     '십과 낱개의 등가 확인, 도움 없는 첫 계산, 단서가 있는 연습, 다른 수에서의 후속 설명을 각각 기록한다.',
     '목적별 수행의 조건을 보존한다. 후속 문항을 만들었다고 난이도의 동등성이나 수업 효과를 입증한 것은 아니다.'),
    ('DC16', ['9수03-15'], '국제판 123~128쪽·134~136쪽, 목표와 문항 및 응답 방식의 대응',
     '직각 조건을 찾고 수치 반례를 설명하는 수행과 임의의 직각삼각형에서 정리를 정당화하는 수행을 각각 요구한다.',
     '선택형 응답 하나로 반례의 이유나 일반 정당화를 확인하지 않는다. 도식이나 말로 설명할 때도 판정할 수학 조건을 유지한다.'),
    ('DC17', ['6수02-03', '6수02-04'], '국제판 123~128쪽, 목표·학습자·맥락·문항 조건',
     '두 비에서 비교량과 기준량을 같은 방향으로 맞추고, 같은 배를 곱할 때 비율이 보존되는 설명을 평가 항목으로 둔다.',
     '빈칸의 정답만으로 비율의 의미를 설명했다고 보지 않는다. 도구나 표기가 달라질 때 묻는 수량 관계도 다시 점검한다.'),
    ('DC18', ['6수04-01'], '국제판 283~286쪽, 문항과 하위 응답별 정리',
     '평균이 같은 두 자료를 사용해 계산값과 자료 수·합·변화 설명을 분리해 기록한다.',
     '일부 반응을 하나의 총점에 합치면 오류 위치가 가려진다. 원전의 예시 표에서 오답에 쓴 빈칸을 현재 관찰의 무응답과 같게 쓰지 않는다.'),
    ('DC19', ['2수03-10', '2수03-12'], '국제판 245~258쪽·265~268쪽, 일대일·소집단·현장 시범',
     '일대일 관찰의 질문과 단서, 수정된 발문의 독립 수행, 다른 자나 실제 책을 쓴 현장 반응을 분리해 기록한다.',
     '형성평가의 세 장면은 점수 하나로 합치지 않는다. 이 과제의 실제 학생 반응과 다른 맥락으로의 전이는 확인 전이다.'),
    ('DC20', ['12실통02-02'], '국제판 289~292쪽·300~302쪽, 오류 근거와 수정·재확인',
     '자료가 어떻게 수집됐는지 확인한 뒤 무응답, 실제 0, 수집 방법 선택을 별개 항목으로 기록한다. 문제의 위치와 수정할 설명을 함께 남긴다.',
     '잘못 해석한 한 행을 조사 전체의 실패로 확대하지 않는다. 특정 응답이 빠졌다고 실제 값이 0이거나 결측이 무작위라고 가정하지 않는다.'),
    ('DC21', ['6수04-05', '6수04-06'], '국제판 283~286쪽·289~292쪽, 문항별 반응과 수정 범위',
     '모형이 말하는 가능성과 반복 시행에서 관찰한 비율을 별개로 묻고, 각각 어느 조건을 해석했는지 기록한다.',
     '한 문항의 정답이나 두 관찰 비율의 차이로 모형 이해, 모형의 공정성 또는 문항 수정 효과를 단정하지 않는다.'),
]

OBSERVATIONS = [
    probe(14, MAPPINGS[0][1],
          '1.2와 1.3 사이를 같은 크기의 열 구간으로 나눈 눈금에서 1.27을 표시한다. 작은 한 구간의 크기와 경계 눈금의 개수를 각각 설명한다.',
          '한 구간은 0.01이다. 1.2에서 일곱 구간 오른쪽이 1.27이다. 양 끝을 포함하면 경계 눈금은 11개다.',
          '구간의 수와 표시점의 수, 한 구간의 크기를 구별한다. 1.2와 1.20을 같은 위치로 보는 이유와 점을 고른 답은 별도 확인한다.'),
    probe(15, MAPPINGS[1][1],
          '십 하나가 일 몇 개인지 먼저 설명한다. 도움 없이 68−29를 계산하고, 연습에서는 교사의 단서를 받아 73−38을 설명한다. 이후 새 계산 82−46을 도움 없이 설명한다.',
          '십 하나는 일 열 개다. 세 계산의 결과는 각각 39, 35, 36이다. 묶음 교환이나 보상으로 답을 구한 경우 그 이유를 설명한다.',
          '출발 기능 질문, 첫 수행, 단서가 있는 연습, 후속 수행을 구별한다. 네 응답을 한 점수로 합치거나 후속 성공을 수업 효과로 처리하지 않는다.'),
    probe(16, MAPPINGS[2][1],
          '6cm, 8cm, 11cm인 삼각형이 직각삼각형인지 판단한다. 이 수치 판단이 임의의 직각삼각형에 대한 정당화인지도 설명한다.',
          '6+8>11이므로 삼각형이 된다. 빗변 후보는 가장 긴 11cm인데 6²+8²=100이고 11²=121이므로 직각삼각형일 수 없다. 한 삼각형의 판정과 정리의 일반 정당화는 구별한다.',
          '정리의 적용 조건과 불일치를 설명하는 근거를 남긴다. 별도로 임의의 직각삼각형에 대해 넓이나 다른 일반 근거를 제시하게 한다.'),
    probe(17, MAPPINGS[3][1],
          '빨강 대 파랑이 3:5, 9:15, 12:19인 세 조합 중 앞 조합과 같은 비율을 고른다. 기준량과 비교량을 말하고 3:5=12:□의 빈칸도 설명한다.',
          '파랑이 기준량이고 빨강이 비교량이다. 9:15는 두 항이 각각 3배라 같고 12:19는 같지 않다. 12는 3의 4배이므로 빈칸은 20이다.',
          '비율을 비교한 이유, 비례식의 값을 구한 이유와 정답을 따로 기록한다. 빨강을 전체와 비교하는 비율로 바꾸면 질문이 달라진다.'),
    probe(18, MAPPINGS[4][1],
          '자료 4, 8, 12와 자료 4, 8, 8, 12의 평균을 각각 구한다. 두 번째 자료에서 수와 합이 바뀌는데도 평균이 같은 이유를 말한다.',
          '첫 자료는 합 24를 3으로, 둘째는 합 32를 4로 나누어 평균이 모두 8이다. 기존 평균과 같은 값 8을 하나 추가했기 때문이다.',
          '합, 자료 수, 계산, 추가한 값의 역할을 별도로 기록한다. 설명하지 않은 부분은 틀린 설명과 구별한다.'),
    probe(19, MAPPINGS[5][1],
          '10cm 기준량으로 길이를 먼저 어림한다. 안내를 받은 연습에서는 자의 2cm와 25cm에 놓인 양 끝을, 다른 자의 독립 과제에서는 5cm와 28cm에 놓인 양 끝을 비교한다.',
          '두 길이는 각각 25−2=23cm, 28−5=23cm다. 어림에 사용한 기준량과 실측에서 읽은 간격을 따로 설명한다.',
          '첫 발문, 자 그림, 자의 끝과 시작 눈금, 실제 단서와 조건을 남긴다. 자가 바뀐 뒤의 반응으로 학습 효과를 단정하지 않는다.'),
    probe(20, MAPPINGS[6][1],
          '통학 조사에서 0분 응답 한 건과 답을 쓰지 않은 한 건이 있다. 두 행을 어떻게 기록할지 정하고 통학 시간 분포를 알아볼 자료 수집 방법을 고른다.',
          '0분은 우선 응답값으로 보존하고 조사 정의에 맞는지 확인한다. 미응답은 결측으로 표시한다. 같은 정의의 시간 자료를 같은 기간에 수집하도록 조사 대상과 질문을 정한다.',
          '수집 방법을 고른 이유와 결측 처리 설명을 따로 확인한다. 누락 이유를 모르면 밝혀지지 않았다고 기록하고 문항의 모호함은 별도 수정한다.'),
    probe(21, MAPPINGS[7][1],
          '공정한 동전이라고 가정한다. 10회에서 앞면이 7번, 다른 20회에서 9번 나왔다. 모형에서 앞면의 가능성과 각 기록 및 합친 기록의 앞면 비율을 구분한다.',
          '모형의 가능성은 1/2이다. 관찰 비율은 각각 7/10과 9/20이다. 같은 조건의 기록을 합치면 16/30이다. 두 비율을 똑같이 가중해 평균 내지 않는다.',
          '두 기록의 시행 조건을 먼저 확인한다. 관찰 비율의 차이로 다음 결과가 정해지거나 동전의 공정성이 증명되지는 않는다.'),
]

RELATIONS = [
    ('REV-4수01-13-1', 'DC14', '1.2에서 1.3까지를 백분의 일씩 나누고 일곱 간격을 지난 점을 1.27로 표시한다.',
     '백분의 일의 크기와 반복 횟수를 설명하는 한 과제다. 이 문항으로 소수 세 자리까지 숙달했다고 판단하지 않는다.'),
    ('REV-6수02-04-1', 'DC17', '비례식의 두 비를 같은 방향의 비교로 읽고, 각각의 기준량과 비교량을 가리킨다.',
     '교차 곱으로 정답만 맞혔다면 비율의 뜻을 설명하는 수행을 추가로 확인한다.'),
    ('REV-6수02-03-2', 'DC17', '3:5에서 두 양을 각각 4배로 늘리면 12:20이 되고 비교량을 기준량으로 나눈 값은 그대로다.',
     '3:5와 12:19는 같은 배가 아니다. 숫자를 같은 만큼 더하는 방법을 비율 보존으로 인정하지 않는다.'),
    ('REV-2수03-12-1', 'DC19', '어림에 쓴 10cm와 자에서 확인한 23cm의 근거를 묻고, 자의 시작 눈금이 달라진 경우에도 간격을 확인한다.',
     '단서 뒤의 측정 성공과 단서 없이 기준량을 사용한 어림은 각각 기록한다.'),
    ('REV-6수04-06-2', 'DC21', '공정 모형의 1/2과 기록의 7/10·9/20·16/30을 서로 다른 질문의 답으로 다룬다.',
     '같은 조건이 아니면 시행을 곧바로 합치지 않는다. 관찰 비율이 1/2과 다르다는 사실만으로 모형을 기각하지 않는다.'),
]


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        build_report()
        return

    assert hashlib.sha256((ROOT / TRANSCRIPT).read_bytes()).hexdigest() == TRANSCRIPT_SHA
    assert source['snapshot_sha256'] == PREVIOUS_SHA
    assert Fraction('1.2') + 7 * Fraction('0.01') == Fraction('1.27')
    assert (68 - 29, 73 - 38, 82 - 46) == (39, 35, 36)
    assert 6 + 8 > 11 and 6**2 + 8**2 == 100 < 11**2
    assert Fraction(3, 5) == Fraction(9, 15) == Fraction(12, 20) != Fraction(12, 19)
    assert Fraction(sum((4, 8, 12)), 3) == Fraction(sum((4, 8, 8, 12)), 4) == 8
    assert 25 - 2 == 28 - 5 == 23
    assert Fraction(16, 30) != (Fraction(7, 10) + Fraction(9, 20)) / 2

    previous = copy.deepcopy(source)
    old_claims = {c['id']: c for c in registry['claims'] if c['source_id'] == SOURCE}
    previous_notes = read(ROOT, previous['snapshot_file'])
    assert previous_notes['transcript']['sha256'] == TRANSCRIPT_SHA
    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    book.update(review_scope=scope,
                next_review='목표 분석 뒷부분, 수업 전략·자료·총괄평가와 부록의 미검토 대목, 공식 판면과 도식을 추가 대조한다. 외부 검토와 학생 응답은 별도 증거가 필요하다.')
    notes = dict(previous_notes, read_scope=scope, previous_review=previous, previous_bibliography=prior_book)
    notes['reading_log'] += [
        '국제판 102~107·119~128·134~136쪽의 선정 본문에서 행동·조건·판정, 출발 기능·사전·연습·사후 평가, 문항 조건과 목표 대응을 구별했다.',
        '245~258·265~268쪽의 선정 본문에서 일대일·소집단·현장 시범과 실제 수행 맥락의 질문을 구별했다.',
        '283~286·289~292·300~302쪽의 선정 본문에서 문항별 반응, 발문·자료 문제, 수정 이유와 근거를 연결하는 방법을 확인했다.',
    ]
    notes['source_corrections'] += [
        dict(kind='blank_and_item_score', location='국제판 285~286쪽, 표 11.1 설명',
             action='원전 예시 표의 빈칸은 오답 표시다. 자체 자료에서는 오답·무응답·미실시를 분리하고 분모를 명시한다.'),
        dict(kind='formative_scope', location='국제판 249~258·265~268쪽',
             action='일대일·소집단·현장 시범의 규모와 절차 예를 한국 교육과정의 검증 기준이나 실제 시행 기록으로 사용하지 않는다.'),
    ]
    notes['unread_followups'] = [book['next_review'], '원전 표의 판면과 도식, 선정 범위 밖 본문 및 인용 원연구를 대조한다.']
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    source.update(snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {k: previous[k] for k in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}
                  ], bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 평가 유형과 문항별 반응, 형성평가 시범의 조건 및 수정 근거를 구분했다.',
                  editorial_action='선정 본문에 따른 새 주장 8건과 자체 관찰 8건을 성취기준 12개에 대응하고 관계 5건에 적용 범위를 남겼다.',
                  observations=previous['observations'] + OBSERVATIONS)
    new_claims = {}
    for cid, codes, location, support, limit in MAPPINGS:
        new_claims[cid] = dict(id=cid, source_id=SOURCE, role='related_theoretical_context',
                               locations=[f'비공식 HTML 전사본 · {location}'], support=support, does_not_establish=limit,
                               target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
                               standard_codes=codes, independent_review=False, student_validated=False)
    assert len({code for claim in new_claims.values() for code in claim['standard_codes']}) == 12
    assert set(new_claims).isdisjoint({r['id'] for r in registry['claims']})
    registry['claims'].extend(new_claims.values())

    relations = read(ROOT, 'data/revised_relations.json')['relations']
    by_id = {row['id']: row for row in relations}
    relation_reviews = read(ROOT, FILE)
    new_pairs = {(rel['id'], claim['id'])
                 for rel in relations for claim in new_claims.values()
                 if all(rel[k].startswith('standard:') for k in ('from', 'to'))
                 and {rel[k][9:] for k in ('from', 'to')} <= set(claim['standard_codes'])}
    assert new_pairs == {(rid, cid) for rid, cid, *_ in RELATIONS}
    rebound = set()
    for row in relation_reviews['records']:
        cid = row['claim_id']
        if cid in old_claims:
            assert row['claim_snapshot'] == claim_snapshot(old_claims[cid], previous)
            row['claim_snapshot'] = claim_snapshot(old_claims[cid], source)
            rebound.add(cid)
    assert rebound == {'DC07', 'DC08', 'DC09', 'DC12'}
    for rid, cid, finding, limit in RELATIONS:
        relation_reviews['records'].append(dict(
            relation_id=rid, claim_id=cid, role='activity_context', finding=finding, limit=limit,
            relation_snapshot=relation_snapshot(by_id[rid]), claim_snapshot=claim_snapshot(new_claims[cid], source),
        ))
    apply_literature_context(relations, registry, registry=relation_reviews)

    queue_path = 'data/content_review_queue.json'
    queue = read(ROOT, queue_path)
    item = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    item.update(source=book, claim_ids=[row['id'] for row in registry['claims'] if row['source_id'] == SOURCE])
    (ROOT / NOTES).write_text(notes_text, encoding='utf-8', newline='\n')
    write('data/sources.json', bibliography)
    write('data/literature_claim_reviews.json', registry)
    write(FILE, relation_reviews)
    write(queue_path, queue)
    build_report()
    print('Assessment and revision: 8 claims, 8 observation designs, 5 relation records')


if __name__ == '__main__':
    main()

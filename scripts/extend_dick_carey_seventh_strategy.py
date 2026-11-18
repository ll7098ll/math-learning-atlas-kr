"""Map selected strategy, materials, evaluation and appendix passages to mathematics tasks."""
import copy
import hashlib
import json
from fractions import Fraction as F

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


NOTES = 'data/literature_evidence/DICK_CAREY_2014_strategy_materials_review_notes.json'
PREVIOUS_SHA = 'd8690a9074fa29c11b5b747929db8666e7e6f27045341452d504a435536d3003'
SCOPE_ADDITION = (' 수업 전략(국제판 154~164·166~170·181~186·190~191쪽), 자료 개발(211~221쪽), '
                  '총괄평가(307~316쪽), 부록 E·L·M(339~341·365~369·371~372쪽)의 선정 본문을 더 확인했다.')

# Each observation uses the same standards as its bounded source claim.
MAPPINGS = [
    ('DC22', ['9수02-15', '9수02-16'], '국제판 154~164·181~186쪽, 전달 방식과 학습 활동',
     '일차함수를 표·식·그래프로 확인할 때 각 매체에 표시한 축과 단위, 학생이 설명할 초기값과 변화율을 구별한다.',
     '그래프가 화면에 나타났다는 사실로 식의 계수나 상황의 조건을 설명했다고 보지 않는다. 수업 순서를 이 사례로 고정하지 않는다.',
     '가상 요금 y=1000x+3000에서 x는 km, y는 원이다. x=0, 1, 3의 표를 만들고 그래프에 표시한다. 화면에 x≥1만 보일 때에도 기본요금과 1km당 추가 요금을 설명한다.',
     '요금은 3000, 4000, 6000원이다. x=0에서 3000원이 기본요금이고, 거리 1km마다 1000원씩 증가한다. 화면에 안 보이는 점을 식과 표에서 확인한다.',
     '공학 도구가 그린 점과 학생이 직접 읽은 축·단위·변화율을 각각 기록한다. 일정 단가인 모형의 범위와 실제 요금 적용 범위를 구별한다.'),
    ('DC23', ['12미적Ⅰ-02-07', '12미적Ⅰ-02-08'], '국제판 166~170쪽, 예·반례와 풀이 과정에 대한 피드백',
     '도함수의 값이 0인 점을 찾는 일과 좌우 부호로 극값을 판정하는 일을 구별하고, 그래프 개형에 반영하는 발문을 둔다.',
     '극값이 있는 예의 결론을 모든 정지점에 옮기지 않는다. 선택한 창의 그림이나 교사의 설명만으로 학생의 부호 판단을 확인하지 않는다.',
     'f(x)=x³−3x의 도함수가 0인 두 점에서 좌우의 부호를 확인하고 그래프 개형을 설명한다. g(x)=x³의 x=0에서도 같은 판정을 할 수 있는가?',
     'f′(x)=3(x²−1)은 x<−1과 x>1에서 양수, −1<x<1에서 음수다. x=−1에서 극댓값 2, x=1에서 극솟값 −2다. g′(x)=3x²은 0 양쪽에서 양수라 x=0은 극값을 갖는 점이 아니다.',
     '좌우 부호를 학생이 정했는지, 교사가 알려 줬는지 기록한다. 극값 판정과 전체 개형의 설명을 각각 확인한다.'),
    ('DC24', ['12미적Ⅰ-03-04', '12미적Ⅰ-03-05'], '국제판 159~164·181~186쪽, 연습·피드백 및 매체 선택',
     '정적분 계산과 도형의 넓이를 구하는 구간 선택을 각각 관찰한다. 그래프 도구를 쓰는 경우에도 부호가 바뀌는 지점을 설명한다.',
     '도구가 제공한 적분값을 넓이와 같다고 판단하지 않는다. 부호가 달라지는 구간을 확인한 근거를 따로 남긴다.',
     'y=x−2, x축, x=0과 x=5로 둘러싸인 두 부분의 넓이 합을 구한다. 도구가 [0,5]의 정적분을 5/2로 주었다면 그 값과 비교한다.',
     'x=2에서 구간을 나눈다. 아래쪽 삼각형의 넓이는 2, 위쪽은 9/2이므로 넓이 합은 13/2다. 정적분은 −2+9/2=5/2다.',
     '부호와 구간을 정한 과정, 도구의 출력, 넓이 합의 근거를 따로 기록한다. 도구 화면에서 가려진 부분이 있으면 축과 창을 확인한다.'),
    ('DC25', ['12인수04-02'], '국제판 181~186·211~221쪽, 매체와 기존 자료의 적합성',
     '추세선 출력, 입력 자료의 단위, 새 관측에서 예측과 실제값의 차이를 나누어 확인한다.',
     '매끄러운 선이나 한 새 관측으로 예측의 전반적인 정확도를 입증하지 않는다. 입력 범위와 측정 조건을 보존한다.',
     '가상 자료 (1,3), (2,5), (3,7)에 추세선 y=2x+1을 사용한다. x=4의 예측과, 나중에 같은 조건으로 관측한 y=8을 구분한다.',
     'x=4에서 예측값은 9이고 관측값은 8이다. 관측값에서 예측값을 빼면 −1이다. x=4는 선을 정할 때 사용한 입력 범위 밖이다.',
     '자료의 단위와 도구 설정, 선을 정할 때 사용한 행과 나중 관측한 행을 구별한다. 모형 적합과 예측의 성과를 따로 기록한다.'),
    ('DC26', ['10공수2-01-03'], '국제판 166~170·211~221쪽, 반례와 자료 선택',
     '직선까지의 거리 예에서 도구의 거리 출력과 수선이라는 조건을 설명하는 수행을 구별한다.',
     '좌표축 방향의 길이가 항상 최단거리라고 일반화하지 않는다. 화면의 격자 배율로 수직 관계를 판정하지 않는다.',
     '원점에서 직선 3x+4y−10=0까지의 거리와 y축을 따라 그 직선에 닿을 때까지의 길이를 비교한다.',
     '거리 공식의 분모는 5이므로 최단거리는 2다. 수선의 발 (6/5,8/5)까지의 거리도 2다. y축으로 가면 (0,5/2)에 닿으므로 길이는 5/2다.',
     '최단거리와 특정 방향의 길이를 구별한 이유를 확인한다. 공식·벡터·도형 중 어떤 경로를 사용했는지 별도로 남긴다.'),
    ('DC27', ['12실통02-02', '12실통02-03'], '국제판 211~221·307~316쪽, 자료의 적합성과 실행 조건',
     '그래프에 표시한 관측 단위·수집 범위를 먼저 확인하고, 자료의 시각적 전달과 조사 질문에 답할 수 있는지 별도로 판단한다.',
     '그림이 읽기 쉽다는 사실로 표집의 적절성이나 결과의 일반화 가능성을 판단하지 않는다.',
     '도서관에서 평일 10~11시 출입구를 통과한 30명의 체류 시간을 조사했다. 체류 시간의 분포를 나타낼 그래프를 정하고, 전체 이용자의 체류 시간으로 해석할 수 있는지 설명한다.',
     '분 단위 체류 시간을 같은 폭의 구간별 빈도로 정리한 히스토그램을 그릴 수 있다. 축에 시간 단위와 빈도를 적는다. 해당 시간대 출입구 표본이므로 다른 시간대나 전체 이용자에게 바로 일반화하지 않는다.',
     '같은 사람이 반복해서 포함될 수 있는지와 관측 단위를 먼저 확인한다. 그래프 표현의 적절성과 표집 설계의 범위를 따로 검토한다.'),
    ('DC28', ['12수과02-03'], '국제판 190~191·307~316쪽, 실행과 결과 판단',
     '실험에서 확인한 수 범위, 실험 결과로 세운 추측, 추측을 수정하게 한 반례를 구분한다.',
     '유한한 확인을 모든 자연수의 증명으로 읽지 않는다. 계산 도구를 사용할 수 있다는 사실과 탐구 설명의 적절성을 별도로 판단한다.',
     'n²+n+41이 n=0부터 4까지 소수라는 결과를 보고, 모든 음이 아닌 정수 n에서 소수라고 결론 내릴 수 있는지 확인한다.',
     '처음 다섯 값은 41, 43, 47, 53, 61이지만 n=40이면 1681=41²이므로 합성수다. 관찰 범위, 추측, 반례를 따로 쓴다.',
     '도구로 시험한 n의 범위와 반례를 발견한 근거를 기록한다. 이 반례를 다른 명제의 정당화로 확대하지 않는다.'),
    ('DC29', ['4수01-14'], '국제판 339~341쪽, 부록 E의 기능·목표·병렬 문항',
     '수의 위치나 표기 길이가 다른 과제에서도 같은 자릿값 비교를 요구하는지 확인하고 이유 설명을 따로 요청한다.',
     '병렬 예를 만든 결과로 두 문항의 난이도가 같거나 진단 점수가 동등하다고 보지 않는다.',
     '0.58과 0.6, 0.8과 0.79를 각각 비교하고 어느 자리에서 크기가 결정되는지 말한다.',
     '0.58<0.60=0.6이고 0.80=0.8>0.79다. 두 쌍 모두 십분의 일 자리에서 대소가 정해진다.',
     '답과 비교 근거를 분리한다. 둘째 문항을 도움 없이 풀었는지와 첫 문항에서 제공한 단서를 별도로 기록한다.'),
    ('DC30', ['6수04-01'], '국제판 365~369·371~372쪽, 부록 L·M의 응답·판단·수정 연결',
     '평균 계산과 균등화 설명을 다른 항목으로 확인하고, 발문을 수정하는 이유와 근거를 연결해 남긴다.',
     '원전 사례의 집단 결과나 수정안을 현재 활동의 효과 또는 보편적인 출발 기능 기준으로 옮기지 않는다.',
     '가상 답안에는 자료 3, 9, 12의 평균을 8로 쓴 기록만 있다. 이 기록에서 확인할 수 있는 것과 균등화를 확인하는 데 필요한 추가 질문을 구별한다.',
     '합 24를 3으로 나눈 평균은 8이다. 9에서 1, 12에서 4를 3 쪽으로 옮기면 8, 8, 8이 된다. 계산값만 있는 답안에는 이 설명의 근거가 없다.',
     '수정한 질문과 추가 설명에서 확인할 수행을 연결한다. 가상 답안은 실제 학생 자료와 구별한다.'),
]

OBSERVATIONS = [probe(number, codes, question, expected, interpretation)
                for number, (_, codes, _, _, _, question, expected, interpretation)
                in enumerate(MAPPINGS, start=22)]
RELATIONS = [
    ('SEC_9수02-15_C04', 'DC22', '식과 표에 x=0을 포함해 화면의 시작점과 실제 요금 모형의 초기값을 구별한다.',
     'x축을 잘라 표시해도 모형에서 x=0을 제외한다는 뜻은 아니다. 요금의 상황 범위를 먼저 확인한다.'),
    ('REV-9수02-15-1', 'DC22', '두 거리 값의 차와 요금 차를 나누어 1000원/km를 확인한다. 한 거리에서 요금을 거리로 나눈 값과 비교한다.',
     '기본요금이 있어 3km에서 6000원을 3으로 나눈 평균과 1km당 추가 요금은 다르다.'),
]


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        build_report()
        return
    assert source['snapshot_sha256'] == PREVIOUS_SHA
    assert hashlib.sha256((ROOT / TRANSCRIPT).read_bytes()).hexdigest() == TRANSCRIPT_SHA
    assert [1000*x + 3000 for x in (0, 1, 3)] == [3000, 4000, 6000]
    assert (-1)**3 - 3*(-1) == 2 and 1**3 - 3 == -2
    assert F(9, 2) - 2 == F(5, 2) and F(9, 2) + 2 == F(13, 2)
    assert 2*4 + 1 == 9 and 8 - 9 == -1
    assert 3*F(6, 5) + 4*F(8, 5) == 10 and F(6, 5)**2 + F(8, 5)**2 == 4
    assert [n*n+n+41 for n in range(5)] == [41, 43, 47, 53, 61]
    assert 40**2 + 40 + 41 == 41**2
    assert F('0.58') < F('0.6') and F('0.8') > F('0.79')
    assert sum((3, 9, 12)) == 3*8 and (3+1+4, 9-1, 12-4) == (8, 8, 8)

    previous = copy.deepcopy(source)
    old_claims = {r['id']: r for r in registry['claims'] if r['source_id'] == SOURCE}
    previous_notes = read(ROOT, previous['snapshot_file'])
    assert previous_notes['transcript']['sha256'] == TRANSCRIPT_SHA
    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    book.update(review_scope=scope, next_review='목표 분석 뒷부분과 장·부록의 선정 범위 밖 본문, 공식 판면·도식과 인용 연구를 대조한다. 외부 검토와 학생 응답은 실제 자료로 확인한다.')
    notes = dict(previous_notes, read_scope=scope, previous_review=previous, previous_bibliography=prior_book)
    notes['reading_log'] += [
        '국제판 154~164·166~170·181~186·190~191쪽의 선정 본문에서 수업 순서, 활동, 피드백, 집단·매체 선택과 사전 점검을 구별했다.',
        '211~221쪽의 선정 본문에서 기존 자료의 일부·전체 선택과 목표·학습자·맥락·학습 지원·기술 요건을 확인했다.',
        '307~316쪽의 선정 본문에서 전문가 판단과 실제 시행, 적합성·내용·설계·실행 가능성과 결과를 구별했다.',
        '부록 E의 339~341쪽과 L의 365~369쪽, M의 371~372쪽에서 기능·목표·평가의 대응, 반응과 의견, 수정안과 그 근거를 대조했다.',
    ]
    notes['source_corrections'] += [
        dict(kind='appendix_pagination_and_scope', location='공식 미리보기 PDF 5쪽과 전사본 부록 E·L·M',
             action='부록 E의 국제판 시작 쪽은 339, 인접한 원서 표기는 349다. 판본별 장·쪽 번호와 표 안에 적힌 수를 구별한다.'),
        dict(kind='response_vs_revision', location='국제판 365~369·371~372쪽, 부록 L·M',
             action='응답표의 빈칸 표기, 사전·사후 수행, 만족도 응답을 따로 읽는다. 특정 집단에서 일부 항목을 출발 기능으로 옮긴 사례를 현재 전체 기준의 필수 순서로 쓰지 않는다.'),
    ]
    notes['unread_followups'] = [book['next_review']]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    source.update(snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}
                  ], bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 수업 자료의 선택과 실제 시행, 부록의 대응표와 수정 근거를 구별했다.',
                  editorial_action='성취기준 13개에 새 근거 9건과 자체 관찰 9건을 대응하고 관계 2건에 적용 범위를 남겼다.',
                  observations=previous['observations'] + OBSERVATIONS)
    new_claims = {
        cid: dict(id=cid, source_id=SOURCE, role='related_theoretical_context',
                  locations=[f'비공식 HTML 전사본 · {location}'], support=support, does_not_establish=limit,
                  target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
                  standard_codes=codes, independent_review=False, student_validated=False)
        for cid, codes, location, support, limit, *_ in MAPPINGS
    }
    assert len({code for claim in new_claims.values() for code in claim['standard_codes']}) == 13
    assert set(new_claims).isdisjoint({row['id'] for row in registry['claims']})
    registry['claims'].extend(new_claims.values())

    relations = read(ROOT, 'data/revised_relations.json')['relations']
    by_id = {r['id']: r for r in relations}
    reviews = read(ROOT, FILE)
    pairs = {(r['id'], cid) for r in relations for cid, claim in new_claims.items()
             if all(r[k].startswith('standard:') for k in ('from', 'to'))
             and {r[k][9:] for k in ('from', 'to')} <= set(claim['standard_codes'])}
    assert pairs == {(rid, cid) for rid, cid, *_ in RELATIONS}
    rebound = 0
    for row in reviews['records']:
        cid = row['claim_id']
        if cid in old_claims:
            assert row['claim_snapshot'] == claim_snapshot(old_claims[cid], previous)
            row['claim_snapshot'] = claim_snapshot(old_claims[cid], source)
            rebound += 1
    assert rebound == 9
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
    print('Strategy, materials and evaluation: 9 claims, 9 observation designs, 2 relation records')


if __name__ == '__main__':
    main()

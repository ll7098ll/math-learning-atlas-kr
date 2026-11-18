"""Apply the newly reviewed summative-evaluation and school appendix passages."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_summative_followup_review_notes.json'
PREVIOUS_SHA = '0bfacfc03d896e22a804b864cfb51bba5a98c38b549a2b19daaa8b60f95de27e'
SCOPE_ADDITION = ' 총괄평가 국제판 317~330쪽과 부록 A~C 331~336쪽의 선정 전사문을 추가로 대조했다.'

MAPPINGS = [
    ('DC76', ['6수03-13', '6수03-14'], '국제판 317~319쪽, 그림 12.2의 자료와 평가 대조',
     '자료가 직사각형과 삼각형의 넓이 유도를 각각 보여 주는지와 문항이 그 유도를 확인하는지를 따로 기록한다.',
     '공식을 싣거나 넓이 수치 하나를 묻는 것만으로 분할과 재구성의 설명을 확인했다고 보지 않는다.',
     '8cm×5cm 직사각형을 한 대각선으로 나눈다. 두 삼각형의 넓이가 같은 이유와 각 넓이를 설명하라. 계산값만 적게 하는 문항은 어떤 부분을 확인할 수 없는가?',
     '직사각형의 넓이는 40cm²다. 한 삼각형을 직사각형의 중심을 기준으로 반 바퀴 돌리면 다른 삼각형과 포개지므로 각 20cm²다. 수치만 받으면 같은 넓이로 나뉘는 이유는 확인할 수 없다.',
     '자료에 실린 설명, 문항이 요구한 설명, 실제 설명이 주어진 경우 그 내용을 별도 칸에 적는다.'),
    ('DC77', ['9수03-04'], '국제판 319~323·326~327쪽, 사용 가능성과 적절한 수행 증거',
     '작도 도구가 있는지와 합동 조건을 설명했는지를 구분한다. 자 없이 풀 수 있는 문항과 실제 작도 과제의 요구를 명시한다.',
     '그림이 포개져 보이거나 각이 같다는 응답을 합동 조건의 증명으로 세지 않는다.',
     '두 삼각형의 세 변이 각각 3cm, 4cm, 5cm라고 정확히 주어진 경우 합동인지 설명하라. 두 번째 경우에는 대응하는 세 각만 같고 변의 길이는 주어지지 않는다. 그 정보로 합동인지 판단하라.',
     '첫 경우는 대응하는 세 변이 같으므로 SSS 합동이다. 두 번째 경우에는 3·4·5와 6·8·10인 두 삼각형처럼 각만 같고 크기가 다를 수 있다.',
     '치수가 주어진 경우와 직접 측정한 경우, 도구가 없었던 경우 및 합동 판단 근거를 나눈다.'),
    ('DC78', ['12실통03-03', '12실통03-04'], '국제판 324~328쪽, 결과 분석과 운영 자료',
     '응답 자료로 모비율을 추정하고 검정을 해석하는 일과 수집 운영 상태를 확인하는 일을 구분한다.',
     '수집 조건이 확인되지 않은 가상 표본에서 모집단 결론을 내리지 않는다. 유의하지 않은 결과를 모비율이 정확히 0.5라는 증거로 쓰지 않는다.',
     '가상의 무작위 표본 100건 중 성공은 58건이다. 도구가 준 95% 정규근사 신뢰구간 [0.483,0.677]과 모비율 0.5에 대한 양측 검정 p≈0.110을 해석하라. 표본 100건의 독립성 확인이 없었다면 무엇을 따로 확인해야 하는가?',
     '표본 비율은 0.58이다. 주어진 구간에 0.5가 포함되며 유의수준 5%에서 귀무가설을 기각하지 않는다. 표집 방법과 독립성 등 실제 분석 조건을 추가로 확인해야 한다.',
     '도구의 입력·계산 조건, 추정 범위와 검정 판단, 수집 과정의 자료 및 미확인 항목을 따로 적는다.'),
    ('DC79', ['6수02-04', '6수02-05'], '국제판 332쪽 부록 A, 목표 집단과 사용할 수 있는 도구',
     '전체량과 부분의 비를 명시하고 비례식을 세울 때 쓸 수 있는 자료를 확인한다. 교실과 다른 장소에서 도구 이용 가능 여부를 기록한다.',
     '도구가 지급됐다는 이유로 매번 이용할 수 있다고 판단하지 않는다. 먼저 준 분할 표시와 학생이 정한 분할을 구별한다.',
     '같은 크기의 구슬 42개를 두 묶음으로 2:5가 되게 나누라. 비례식으로 구해도 되고 일곱 칸의 띠를 그려도 된다. 계산과 함께 두 묶음의 합이 42인지 확인하라.',
     '같은 한 칸이 42÷7=6개이므로 두 묶음은 12개, 30개다. 첫 묶음을 x라 하면 x/42=2/7이고, 12+30=42와 12:30=2:5를 확인할 수 있다.',
     '방법 선택, 처음 제공한 표시와 도구, 같은 한 칸의 의미, 합과 비의 확인을 구분한다.'),
    ('DC80', ['9수03-16', '9수03-17'], '국제판 333~334쪽 부록 B, 목표의 단계와 산출',
     '어떤 변이 기준각의 맞은편인지 확인한 뒤 사용할 비를 선택하게 한다. 올바른 다른 풀이도 목표의 설명을 보였는지 살핀다.',
     '예시 절차의 순서나 특정 계산기를 공통 필수 경로로 정하지 않는다. 길이의 계산과 관계의 설명은 구별한다.',
     '직각삼각형에서 기준각 θ에 대해 tan θ=3/4이고 그 각의 맞은편 변이 9m다. θ에 인접한 직각변의 길이와 빗변의 길이를 구하라. 그림에 두 변의 위치를 표시하라.',
     '맞은편과 인접 직각변의 길이 비가 3:4라서 인접 직각변은 12m이고 빗변은 15m다. 비례 계산과 피타고라스 정리 또는 3·4·5 삼각형의 확대를 이용할 수 있다.',
     '기준각, 변의 위치, 식의 방향과 검산을 기록한다. 계산 순서가 달라도 같은 수학적 근거인지 확인한다.'),
    ('DC81', ['10공수2-01-02', '10공수2-01-03'], '국제판 335~336쪽 부록 C, 출발 기능과 목표 수행',
     '수직 조건을 확인하는 출발 기능과 수선의 발을 이용해 거리를 구하는 목표 수행을 각각 관찰한다.',
     '기울기 조건을 안다는 사실만으로 점과 직선 사이 거리를 구했다고 보지 않는다. 출발 기능은 특정 과제와 학습자 범위에서 확인한다.',
     '점 P=(0,6)에서 직선 y=2x+1에 내린 수선의 발을 구하고 거리를 설명하라. 먼저 기울기가 2인 직선과 수직인 직선의 기울기를 확인하라.',
     '수선의 기울기는 −1/2이고 방정식은 y=−x/2+6이다. 교점은 (2,5)이며 두 점 사이 거리는 √(2²+1²)=√5다.',
     '기울기 판정, 수선의 식과 교점, 거리 계산을 따로 확인한다. 다른 타당한 거리 풀이를 사용한 경우도 근거를 남긴다.'),
]

RELATIONS = [
    ('REV-6수03-14-2', 'DC76', '직사각형을 대각선으로 분할해 삼각형의 넓이와 그 근거를 설명한다.', '자료의 내용과 문항에서 실제로 요구하는 수행을 구별한다.'),
    ('SEC_12실통03-03_C04', 'DC78', '같은 표본의 모비율 신뢰구간과 가설검정의 결과를 주어진 조건에서 해석한다.', '수집 조건과 도구 입력을 확인하고 비기각을 모비율 일치로 확대하지 않는다.'),
    ('REV-6수02-05-1', 'DC79', '전체 42개와 부분의 비 2:5를 연결해 두 부분을 구한다.', '비례식과 띠 중 어느 도구를 썼는지와 단위 해석을 각각 확인한다.'),
    ('REV-9수03-16-1', 'DC80', '기준각에 대한 변의 위치를 확인하고 탄젠트 비로 길이를 구한다.', '기준각이 달라지면 변의 역할이 바뀌며 타당한 다른 경로도 인정한다.'),
    ('SEC_9수03-17_C03', 'DC80', '탄젠트 비로 구한 인접 직각변을 바탕으로 빗변을 구하고 길이를 검산한다.', '처음에 주어진 변과 그 뒤에 계산한 변을 구분해 풀이의 근거를 남긴다.'),
    ('HC-common-point-line', 'DC81', '기울기 2와 −1/2의 수직 조건을 이용해 수선의 발과 거리를 구한다.', '수직 조건을 제시한 응답과 거리까지 설명한 응답을 구별한다.'),
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
    from math import erfc, isclose, sqrt
    assert Fraction(8 * 5, 2) == 20
    assert {(8 - x, 5 - y) for x, y in ((0, 0), (8, 0), (8, 5))} == {(8, 5), (0, 5), (0, 0)}
    assert all(b == 2 * a for a, b in zip((3, 4, 5), (6, 8, 10)))
    observed = 0.58
    margin = 1.96 * sqrt(observed * (1 - observed) / 100)
    assert (round(observed - margin, 3), round(observed + margin, 3)) == (0.483, 0.677)
    z = (observed - 0.5) / sqrt(0.5 * 0.5 / 100)
    assert isclose(z, 1.6) and round(erfc(z / sqrt(2)), 3) == 0.110
    assert Fraction(42 * 2, 7) == 12 and Fraction(42 * 5, 7) == 30
    assert Fraction(9, 12) == Fraction(3, 4) and 9 ** 2 + 12 ** 2 == 15 ** 2
    assert Fraction(-1, 2) * 2 == -1 and 2 * 2 + 1 == Fraction(-1, 2) * 2 + 6 == 5
    assert (2 - 0) ** 2 + (5 - 6) ** 2 == 5


    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    followup = '부록 L·M의 나머지와 용어집·색인, 공식 판면과 도식, 인용 원연구를 대조한다. 독립 검토와 학생 응답은 실제 자료로 확인한다.'
    book.update(review_scope=scope, next_review=followup)
    notes = dict(prior_notes, date=DATE, read_scope=scope, previous_review=previous,
                 previous_bibliography=prior_book,
                 summative_followup_extension=dict(
                     selected_pages=[[317, 330]], selected_appendices={'A': [331, 332], 'B': [333, 334], 'C': [335, 336]},
                     transcript_only=True, diagram_arrows_verified=False,
                     coverage_example=dict(figure='12.2', skill_count=22, example_only=True, candidate_columns_verified=False),
                     assessment_content_and_observed_performance_separated=True,
                     expert_judgment_and_field_trial_separated=True))
    notes['reading_log'] += [
        '317~323쪽에서 필요와 목표의 일치, 자료와 검사에서 기능이 다뤄지는지, 전략의 존재와 대상에 대한 적절성을 구별했다.',
        '324~330쪽에서 사용자 보고와 전문가 판단, 현장 시험의 수행과 운영 기록, 보고서와 참고문헌의 역할을 구별했다.',
        '부록 A~C의 요구 분석과 목표 집단, 수행 맥락, 목표 분석 번호 및 출발 기능선에 관한 전사문을 대조했다. 원서 번호와 국제판 번호가 함께 나타난다.',
    ]
    notes['source_corrections'] += [
        dict(kind='candidate_coverage_example', location='국제판 318~319쪽 그림 12.2',
             action='본문의 가상 예에서 기능 22개를 확인했다. 전사된 수를 후보 자료·사전·사후 검사의 각 열에 재배치하지 않았다. 자료와 문항의 포함 표시는 실제 수행 기록과 구별한다.'),
        dict(kind='not_applicable_mark', location='국제판 326~327쪽 총괄평가 루브릭',
             action='지침에서 해당 없음 표시를 No 열에 적도록 하지만 미충족과 해당 없음의 뜻은 구별한다. 외부 평가·운영·학생 수행의 기록도 각각 분리한다.'),
        dict(kind='comparison_and_entry_scope', location='국제판 325쪽 사례 및 331~336쪽 부록 A~C',
             action='비교 후보가 없다는 설명은 방범 교육 사례의 조건이다. 학교 작문 예의 대상과 출발 기능선은 해당 설계 범위에서 읽고 화살표와 선의 정렬은 공식 판면에서 확인한다.'),
    ]

    notes['unread_followups'] = [followup]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    observations = [probe(int(cid[2:]), codes, question, expected, interpretation)
                    for cid, codes, _, _, _, question, expected, interpretation in MAPPINGS]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 자료의 목표 포함 여부와 평가 문항, 실제 수행과 운영 여건, 출발 기능과 목표를 구별했다.',
                  editorial_action='성취기준 11개에 근거 6건과 자체 관찰 6건을 대응하고 관계별 대조 6건을 작성했다.',
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
    print('Seventh international edition summative followup: 6 claims, 6 observation designs, 6 relation records')


if __name__ == '__main__':
    main()

"""Apply the newly reviewed instructional-materials and school case passages."""
import copy
import hashlib
import json
from fractions import Fraction

from extend_dick_carey_seventh_subskills import SOURCE, TRANSCRIPT, TRANSCRIPT_SHA, probe, write
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_materials_followup_review_notes.json'
PREVIOUS_SHA = '05ed9a17a8c4672738ca9873f08fda3835bd4c4d2620b744aad49a0e36248001'
SCOPE_ADDITION = ' 자료 개발 국제판 222~243쪽과 부록 I·J·K 353~363쪽의 선정 전사문을 추가로 대조했다.'

MAPPINGS = [
    ('DC58', ['4수03-15', '4수03-16'], '국제판 222~224·238~240쪽, 실제 도구와 읽을 수 있는 표시',
     '눈금의 단위와 두 끝점이 자료에 모두 드러나는지 확인한다. 실제 길이를 알아낸 수행과 주어진 길이를 환산하는 수행을 구별한다.',
     '자 그림이나 사진에서 시작점이 빠진 경우, 끝점 눈금만으로 길이를 확정하지 않는다.',
     '띠의 왼쪽 끝은 15mm, 오른쪽 끝은 62mm 눈금에 놓였다. 길이를 mm와 몇 cm 몇 mm로 써라. 두 번째 그림에서 왼쪽 끝이 가려지고 오른쪽 끝만 보인다면 무엇이 더 필요한가?',
     '띠의 길이는 62−15=47mm이며 4cm 7mm다. 왼쪽 끝이 가려졌다면 그 끝의 눈금이나 길이를 정할 수 있는 다른 정보가 필요하다.',
     '처음 읽은 두 눈금, 두 값의 차, 환산, 그림의 빠진 정보를 따로 기록한다. 자료에서 시작점이 가려진 경우를 학생의 눈금 읽기 오류로 세지 않는다.'),
    ('DC59', ['6수03-12', '6수03-13'], '국제판 235~237쪽, 같은 풀이와 연결되는 피드백',
     '길이 단위의 배와 넓이 단위의 배가 달라지는 줄을 짚고, 새 과제에서 학생이 같은 근거를 설명하는지 확인한다.',
     '고쳐 쓴 답만으로 오류를 스스로 찾아냈다고 판단하지 않는다. 넓이의 수치와 제곱 단위를 구분한다.',
     '가로 3m, 세로 2m인 직사각형의 넓이를 m²와 cm²로 써라. 첫 풀이를 남긴 뒤, 가상의 답안 6m²=600cm²에서 잘못된 줄을 찾아라. 이어 가로 2m, 세로 4m인 새 직사각형을 두 단위로 나타내라.',
     '첫 넓이는 6m²=60000cm²다. 1m²는 100cm×100cm여서 10000cm²이고, 길이의 100배를 넓이에 한 번만 적용한 줄이 잘못됐다. 새 직사각형은 8m²=80000cm²다.',
     '최초 답, 잘못된 줄의 위치, 이유와 수정값, 새 직사각형의 답을 구별한다. 가상의 오답을 실제 학생 응답으로 세지 않는다.'),
    ('DC60', ['10공수2-02-04', '10공수2-02-05'], '국제판 359~363쪽 부록 K, 형태의 분류와 기호의 사용',
     '명제의 역·대우를 만드는 일과 각 명제의 참·거짓을 판단하는 일을 분리한다. 화살표나 부정 표시를 먼저 보여 줬는지도 기록한다.',
     '기호를 바르게 배치했다는 사실로 명제의 참·거짓이나 반례의 설명이 확인되었다고 판단하지 않는다.',
     '정수 n에 대하여 “n이 4의 배수이면 n은 짝수다”의 역과 대우를 쓰고, 세 문장이 각각 참인지 판단하라. 거짓인 문장에는 반례를 들어라.',
     '원명제는 4의 배수가 2의 배수이므로 참이다. 역은 짝수이면 4의 배수라는 말로 6이 반례다. 대우는 짝수가 아니면 4의 배수가 아니라는 말이며 참이다.',
     '정수 범위, 조건과 결론의 자리, 부정, 참·거짓의 근거를 따로 확인한다. 문장과 기호 중 한 형식으로 타당한 이유를 제시해도 인정한다.'),
    ('DC61', ['12실통02-03', '12실통02-04'], '국제판 222~224·238~240쪽, 그래프 표현과 판단 근거',
     '자료의 중심과 퍼짐을 비교할 때 그래프의 눈금과 관측값, 요약값의 뜻을 각각 확인한다.',
     '그래프를 매끄럽게 그린 것만으로 자료의 퍼짐을 설명했다고 보지 않는다. 범위만으로 분포 전체가 같거나 다르다고 확정하지 않는다.',
     '가상 자료 A=(2,2,5,8,8), B=(4,4,5,6,6)을 같은 가로 눈금의 점그래프로 나타내라. 평균과 범위를 각각 구하고 그림과 연결해 해석하라.',
     '두 평균은 5다. A의 범위는 8−2=6, B의 범위는 6−4=2다. 이 자료에서는 평균은 같고 가장 작은 값과 큰 값 사이가 A에서 더 넓다.',
     '반복값을 빠뜨리지 않고 표시했는지, 같은 눈금인지, 평균과 범위 계산 및 해석을 각각 기록한다.'),
    ('DC62', ['4수01-12', '4수01-13'], '국제판 353~356·359~363쪽, 학습자용 표시와 새 자료',
     '어느 구간을 몇 등분했는지와 기준점을 학생이 스스로 읽었는지 구분한다. 정답 표기를 제시한 연습 뒤에는 다른 눈금으로 다시 설명하게 한다.',
     '설계자용 표시나 앞 단계에서 알려 준 눈금값을 학생이 독립적으로 알아낸 값으로 기록하지 않는다.',
     '0에서 1까지 같은 길이의 열 구간으로 나눴을 때 0에서 여섯 구간 간 점을 분수와 소수로 쓰라. 다음에는 0.6에서 0.7까지를 열 구간으로 나눴다. 0.6에서 네 구간 간 점을 읽어라.',
     '첫 점은 6/10=0.6이다. 둘째 눈금의 한 구간은 0.01이고 네 구간은 0.04이므로 지정한 점은 0.64다.',
     '구간 크기, 출발 눈금, 간격 수를 따로 기록한다. 눈금을 어느 단계에서 표시해 줬는지와 새 자료의 독립 답을 구별한다.'),
    ('DC63', ['9수02-07'], '국제판 228~237·357~358쪽, 예와 연습 및 오류 위치를 알려 주는 피드백',
     '값이 감소하는 모습과 두 양의 곱이 일정하다는 조건을 구별한다. 잘못된 행의 위치를 찾아 다른 행에서 다시 확인하게 한다.',
     '내려가는 그래프나 한두 개의 일치만으로 반비례라고 판단하지 않는다. 주어진 표에서는 나머지 행도 확인한다.',
     'x=2,3,4에 대해 A표의 y는 6,4,3이고 B표의 y는 6,4,2다. 어느 표가 y=12/x에 맞는가? 잘못된 행을 고친 뒤 x=6의 y를 새로 구하라.',
     'A표는 곱이 모두 12다. B표는 x=4에서 곱이 8이므로 y를 3으로 고쳐야 한다. x=6이면 y=2다.',
     '잘못된 행을 학생이 처음 찾았는지와 피드백을 본 뒤 고친 이유, 새 행에 같은 조건을 적용한 설명을 구분한다.'),
]

RELATIONS = [
    ('REV-4수03-16-1', 'DC58', '두 끝의 눈금 차로 47mm를 구하고 4cm 7mm로 바꾼다.', '시작점 정보가 빠진 그림에서는 환산과 실제 길이 결정을 따로 본다.'),
    ('REV-6수03-13-1', 'DC59', '3m와 2m를 각각 cm로 바꿔 60000cm²를 확인한다.', '길이의 환산 배율을 넓이에 한 번만 적용하지 않는다.'),
    ('REV-6수03-14-1', 'DC59', '직사각형을 덮는 단위 정사각형과 두 변의 길이를 연결해 설명한다.', '넓이 단위가 바뀌어도 덮는 영역은 같아야 한다.'),
    ('HC-common-logic', 'DC60', '역과 대우에서 조건·결론 및 부정을 확인하고 거짓인 역의 반례를 찾는다.', '정수 범위와 명제의 판단 근거를 각각 보존한다.'),
    ('REV-12실통02-03-1', 'DC61', '같은 눈금에서 중심이 같은 두 자료의 양 끝 거리를 비교한다.', '평균 일치가 범위나 분포 전체의 일치를 뜻하지 않는다.'),
    ('REV-4수01-13-1', 'DC62', '0.6에서 시작한 네 구간의 크기를 확인해 0.64를 설명한다.', '표시된 정답을 읽은 반응과 구간의 크기를 스스로 설명한 반응을 구분한다.'),
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
    assert divmod(62 - 15, 10) == (4, 7)
    assert (3 * 100) * (2 * 100) == 60_000 and (2 * 100) * (4 * 100) == 80_000
    assert 6 % 2 == 0 and 6 % 4 != 0
    first, second = (2, 2, 5, 8, 8), (4, 4, 5, 6, 6)
    assert Fraction(sum(first), len(first)) == Fraction(sum(second), len(second)) == 5
    assert max(first) - min(first) == 6 and max(second) - min(second) == 2
    assert Fraction(6, 10) + 4 * Fraction(1, 100) == Fraction('0.64')
    assert [x * y for x, y in zip((2, 3, 4), (6, 4, 3))] == [12, 12, 12]
    assert 4 * 2 != 12 and Fraction(12, 6) == 2

    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    scope = previous['read_scope'] + SCOPE_ADDITION
    followup = '형성평가 259~264·269~281쪽의 미검토 대목, 자료 수정과 총괄평가의 나머지, 공식 판면·도식과 인용 연구를 대조한다. 독립 검토와 학생 응답은 실제 자료로 확인한다.'
    book.update(review_scope=scope, next_review=followup)
    notes = dict(prior_notes, date=DATE, read_scope=scope, previous_review=previous,
                 previous_bibliography=prior_book,
                 materials_followup_extension=dict(
                     selected_materials_pages=[222, 243],
                     selected_appendix_pages={'I': [353, 356], 'J': [357, 358], 'K': [359, 363]},
                     transcript_only=True, diagram_connections_from_text=False,
                     learner_material_and_designer_notes_separated=True,
                     feedback_case=dict(exercise_figure='9.5', feedback_figure='9.6',
                                        matched_episode=True, verbatim_match=False)))
    notes['reading_log'] += [
        '222~224쪽에서 초안, 수업 자료, 평가와 운영 안내의 역할을 구별했다.',
        '225~243쪽에서 계획을 자료로 바꾸는 예, 먼저 답한 반응과 피드백, 읽기와 탐색에 필요한 조건을 대조했다.',
        '부록 I·J·K에서 설계자에게만 보이는 기능 번호, 사전 수행 과제, 분류와 표시의 정확성을 구분했다.',
    ]
    notes['source_corrections'] += [
        dict(kind='feedback_script_wording', location='국제판 235~237쪽, 그림 9.5와 9.6 및 본문',
             action='본문은 피드백에서 연습의 대본을 다시 제시한다고 설명한다. 전사문에서 같은 장면의 일부 표현은 다르게 적혀 있다. 두 자료의 문장별 동일성은 공식 판면에서 확인하고, 자체 자료에서는 발문과 피드백이 동일한 사례를 가리키도록 한다.'),
        dict(kind='classification_vs_mark', location='국제판 361~363쪽, 부록 K 설명과 연습 5.10',
             action='설명의 문장 유형 판정과 연습에서의 끝 기호 정오 판정을 각각 기록했다. 같은 규칙을 설명한다고 가정해 표기를 합치지 않는다. 작문 예는 수학 내용으로 등록하지 않았다.'),
        dict(kind='designer_only_marker', location='국제판 355~356쪽, 부록 I의 점검 과제',
             action='목표와 문항을 연결하는 기능 번호는 설계자에게 보이는 표시다. 학습자가 본 단서인지 여부를 구별한다.'),
    ]
    notes['unread_followups'] = [followup]
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    observations = [probe(int(cid[2:]), codes, question, expected, interpretation)
                    for cid, codes, _, _, _, question, expected, interpretation in MAPPINGS]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=previous['snapshot_history'] + [
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=scope,
                  method_note=previous['method_note'] + ' 학습자 자료와 설계자 표시, 첫 수행과 오류 위치의 피드백을 구분했다.',
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
    print('Seventh international edition materials followup: 6 claims, 6 observation designs, 6 relation records')


if __name__ == '__main__':
    main()

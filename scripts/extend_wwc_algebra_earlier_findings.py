"""Extend the WWC algebra ledger with its earlier equation-solving reviews."""
import copy
from collections import Counter
from fractions import Fraction

from record_wwc_algebra_findings_export import (
    DATE, EMPIRICAL, FINDING_FIELDS, GUIDE, ROOT, SOURCE, URL,
    build_report, digest, load, load_registry, read_export_rows, sha, target_value, write,
)
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


NOTES = f'data/literature_evidence/{SOURCE}_earlier_review_notes.json'
PRIOR_SHA = '05e84983078135f0b32bff26e4534e05dd4dfb39d952782f966ed4897b750a99'
STUDIES = {'79838', '79861', '79862'}
SOURCE_STUDIES = {
    '79838': 'STAR_SEIFERT_2006_ALTERNATIVE_ORDER',
    '79861': 'RITTLE_JOHNSON_STAR_2007_EQUATION_METHODS',
    '79862': 'RITTLE_JOHNSON_STAR_2009_EQUATION_COMPARISONS',
}
NEXT = '원논문 판면과 원자료, WWC 효과 크기·유의 판정의 산출 기록을 확인한다. 국내 과제의 독립 검토와 학생 반응은 별도로 기록한다.'
CLAIMS = [
    ('WAE05', ['9수02-04'], '79838', '결과 8644·10269–10271 및 원논문 291·293쪽',
     '2006년 연구의 WWC 분석 32명에서 사후 네 지표의 최종 표기는 모두 비유의다. 비전형적 변형 횟수의 WWC p≈0.0589이며 원논문은 같은 평균 2.5 대 0.7에 p<.05를 보고했다. 원논문의 여러 순서 평균과 서로 다른 순서를 3문항 이상에 쓴 인원도 별개 지표다.',
     '정답과 변형 순서, 주어진 방식과 다른 풀이의 수를 따로 관찰한다. 서로 다른 판정의 산출 방법과 국내 과제 효과는 확인 전이다.'),
    ('WAE06', ['9수02-04'], '79861', '결과 8511–8514 및 원논문 표 3~5',
     '2007년 연구의 WWC 69명 비교에서 절차 지식과 절차 유연성은 연구 p 열 0.04·0.01, WWC p 열 약 0.171·0.057, 최종 표기는 모두 유의다. 별도 지름길 사용은 비유의다. 논문은 70명을 배정하고 사후 결석 1명의 결과를 대치했다.',
     '내보내기의 평균 열과 원논문의 변화량 및 WWC 효과 크기를 서로 대신 쓰지 않는다. 절차 유연성 점수와 지름길 사용 빈도는 다르며 최종 판정의 계산 근거는 확인 전이다.'),
    ('WAE07', ['9수02-03', '9수02-04'], '79862', '심사 1902431·1902439 및 원논문 529~544쪽',
     '2009년 두 저자 연구에서 WWC의 방법 비교 대 동형 문제 비교는 2주 뒤 실제 전략 사용과 유연성 지식에서 유의다. 문제 유형 비교 대 동형 문제 비교는 2주 네 지표 모두 비유의다. 분석 표본은 지표와 시점에 따라 94~106명이다.',
     '공통 비교군을 사용하는 두 대비의 결과를 합산하지 않는다. 원논문의 세 조건 반복 측정과 WWC의 시점별 대비를 구분하고, 새 과제에서 실제 쓴 전략을 보기 선택과 분리한다.'),
]
OBSERVATIONS = [
    dict(id='WAE-P4', standard_codes=['9수02-04'],
         question='5(x−2)+15=40을 먼저 풀고 첫 두 변형을 남겨라. 같은 식에서 처음 한 연산과 다른 연산으로 시작해 다시 풀어라. 두 풀이의 해와 순서를 비교하라.',
         expected='15를 먼저 빼면 5(x−2)=25다. 양변 전체를 5로 먼저 나누면 x−2+3=8이다. 모두 x=7이며, 전개로 시작하는 풀이도 각 줄이 동치면 타당하다.',
         interpretation='처음 두 변형과 요구 뒤의 변형 순서, 정답을 따로 기록한다. 단일 문항의 두 순서를 여러 문항의 자발적 전략 사용으로 집계하지 않는다.', student_validated=False),
    dict(id='WAE-P5', standard_codes=['9수02-04'],
         question='2(x+5)=x+17에서 먼저 전개하는 시작과 양변을 먼저 2로 나누는 시작이 각각 가능한지 설명하라. 양변을 2로 나눌 때 오른쪽에 남는 식을 쓰고 두 방법을 비교하라.',
         expected='전개하면 2x+10=x+17이다. 먼저 나누면 x+5=(x+17)/2다. 두 시작 모두 타당하고 해는 x=7이다. 이 식에서는 전개하면 정수 계수를 유지하면서 x항을 바로 모을 수 있다.',
         interpretation='정답, 가능한 변형의 인식, 해당 식에서 계산이 더 간단한 이유를 따로 확인한다.', student_validated=False),
    dict(id='WAE-P6', standard_codes=['9수02-03', '9수02-04'],
         question='6(u−1)=4(u−1)+8을 먼저 풀고 첫 변형을 기록하라. 이어 오른쪽을 4(u+1)+8로 바꾼 새 식을 보기 없이 풀고 이전과 같은 이유로 부분식을 모을 수 있는지 설명하라.',
         expected='첫째는 2(u−1)=8이므로 u=5다. 둘째의 괄호는 다르므로 같은 부분식으로 합칠 수 없다. 전개하면 6u−6=4u+12이므로 u=9다. 각 해를 해당 원식에 대입해 확인할 수 있다.',
         interpretation='두 식에 처음 적용한 변형과 이후 설명을 각각 기록한다. 나중에 다시 물을 때는 시점과 제공한 단서를 남긴다.', student_validated=False),
]
RELATIONS = {
    'SEC_9수02-03_C04': ('첫 식에서 공통 부분식을 빼는 이유와 두 번째 식에서 같은 부분이 남지 않는 이유를 설명한다.', '같은 부분식으로 모으려면 괄호 전체가 같아야 한다.'),
    'SEC_9수02-04_C03': ('두 조건의 방정식을 각각 풀고 원식에 대입한다.', '변형 근거와 두 해 5와 9의 대입 확인을 구분한다.'),
    'REV-9수02-03-1': ('표현이 달라지면 어떤 변형이 여전히 타당한지 설명한다.', '보기 선택과 새 식에서 자발적으로 사용한 변형은 다른 기록이다.'),
}


def check_rows(studies, rows):
    assert len(studies) == 10
    assert Counter(row['StudyID'] for row in rows) == {'79838': 4, '79861': 4, '79862': 16}
    assert len({row['FindingID'] for row in rows}) == 24
    for row in rows:
        assert int(row['Outcome_Sample_Size']) == sum(int(row[key]) for key in (
            'Outcome_Measure_Intervention_Sample_Size', 'Outcome_Measure_Comparison_Sample_Size'))
    by_id = {row['FindingID']: row for row in rows}
    assert {row['FindingID'] for row in rows if row['Is_Statistically_Significant'] == 'True'} == {
        '8481', '8511', '8512', '10277', '10278'}
    assert round(float(by_id['10271']['p_Value_WWC']), 4) == .0589
    assert by_id['8511']['p_Value_Study'] == '0.04' and round(float(by_id['8511']['p_Value_WWC']), 3) == .171
    assert by_id['8512']['p_Value_Study'] == '0.01' and round(float(by_id['8512']['p_Value_WWC']), 3) == .057
    assert min(int(row['Outcome_Sample_Size']) for row in rows if row['StudyID'] == '79862') == 94
    assert max(int(row['Outcome_Sample_Size']) for row in rows if row['StudyID'] == '79862') == 106
    assert all(row['Is_Statistically_Significant'] == 'False' for row in rows
               if row['ReviewID'] == '1902439' and row['Period'] == '2 Weeks')


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        build_report()
        return
    previous = copy.deepcopy(source)
    assert previous['snapshot_sha256'] == PRIOR_SHA
    old_notes = load(ROOT / previous['snapshot_file'])
    studies, rows = read_export_rows(STUDIES, FINDING_FIELDS + ('Outcome_Domain',))
    check_rows(studies, rows)
    assert 5 * (7 - 2) + 15 == 40 and (7 - 2) + Fraction(15, 5) == 8
    assert 2 * (7 + 5) == 7 + 17
    assert 6 * (5 - 1) == 4 * (5 - 1) + 8
    assert 6 * (9 - 1) == 4 * (9 + 1) + 8

    bibliography = load(ROOT / 'data/sources.json')
    queue = load(ROOT / 'data/content_review_queue.json')
    source_entry = next(row for row in bibliography if row['id'] == SOURCE)
    guide_entry = next(row for row in bibliography if row['id'] == GUIDE)
    guide = registry['sources'][GUIDE]
    previous_guide = copy.deepcopy(guide)
    scope = previous['read_scope'] + ' 연구 79838·79861·79862의 심사 10건과 결과 24개 행을 더 대조했다.'
    source_entry.update(review_scope=scope, next_review=NEXT)
    empirical = dict(EMPIRICAL, design='outcome_level_wwc_reviews_of_six_equation_solving_studies',
                     sample_description='2006·2007·2008·2009·2012년 방정식 풀이 연구 6편의 결과별 분석 표본이다.')
    notes = dict(old_notes, read_scope=scope, empirical_scope=empirical, unresolved_followup=NEXT,
                 review_rows=old_notes['review_rows'] + studies, outcome_rows=old_notes['outcome_rows'] + rows,
                 prior_snapshot=dict(file=previous['snapshot_file'], sha256=PRIOR_SHA),
                 study_urls={**old_notes['study_urls'],
                             **{sid: f'https://ies.ed.gov/ncee/wwc/study/{sid}' for sid in sorted(STUDIES)}},
                 additional_original_studies={sid: dict(
                     source_id=original, snapshot_file=registry['sources'][original]['snapshot_file'],
                     snapshot_sha256=registry['sources'][original]['snapshot_sha256'])
                     for sid, original in SOURCE_STUDIES.items()})
    notes['reading_log'] += [
        '추가 세 연구를 ReviewID로 연결해 24개 결과 행의 시점, 분모, p값과 최종 유의 판정을 대조했다.',
        'ReviewDictionary.csv에서 연구 보고값, WWC 계산값, WWC 최종 유의 판정이 별도 필드임을 확인했다.',
    ]
    notes['source_corrections'] += [
        dict(location='79838, 10271 및 2006년 원논문', issue='평균 2.5 대 0.7의 원논문 판정과 WWC 비유의를 구별한다.'),
        dict(location='79861, 8511·8512', issue='연구 p 열, WWC p 열 및 최종 유의 여부를 각각 기록한다.'),
        dict(location='79862, 1902431·1902439', issue='방법 비교와 유형 비교를 나누고, 즉시 검사와 2주 검사 및 측정별 분모를 구분한다.'),
    ]
    assert len(notes['review_rows']) == 21 and len(notes['outcome_rows']) == 50
    write(ROOT / NOTES, notes)
    source.update(date=DATE, read_scope=scope, snapshot_file=NOTES, snapshot_sha256=sha(ROOT / NOTES),
                  snapshot_history=[*previous.get('snapshot_history', []),
                                    {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(source_entry), empirical_scope=empirical,
                  observations=previous['observations'] + OBSERVATIONS,
                  editorial_action='근거 3건과 관찰 과제 3개를 추가하고 관계별 대조 3건을 보완했다.')

    previous_claims = {row['id']: copy.deepcopy(row) for row in registry['claims'] if row['source_id'] == SOURCE}
    for claim in registry['claims']:
        if claim['id'] in previous_claims:
            claim['empirical_scope'] = empirical
    for cid, codes, sid, location, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='empirical_result_with_scope', standard_codes=codes,
            locations=[f'{notes["study_urls"][sid]} · {location}'], support=support, does_not_establish=limit,
            empirical_scope=empirical, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    claims = {row['id']: row for row in registry['claims']}
    ids = [row['id'] for row in registry['claims'] if row['source_id'] == SOURCE]
    guide_entry['next_review'] = 'WWC 내보내기로 방정식 풀이 비교 연구 6편의 결과 50개 행을 대조했다. ' + NEXT
    guide['bibliography_snapshot'] = digest(guide_entry)
    guide['findings_export_crosscheck'] = dict(
        source_id=SOURCE, claim_ids=ids, snapshot_file=NOTES, snapshot_sha256=source['snapshot_sha256'],
        study_ids=sorted(notes['study_urls']), review_count=21, finding_count=50,
    )
    next(row for row in queue['literature_review'] if row['source']['id'] == GUIDE)['source'] = guide_entry
    next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE).update(
        source=source_entry, claim_ids=ids,
    )

    relations = load(ROOT / 'data/revised_relations.json')['relations']
    by_id = {row['id']: row for row in relations}
    reviewed = load(ROOT / FILE)
    for row in reviewed['records']:
        claim = claims[row['claim_id']]
        if claim['source_id'] in (SOURCE, GUIDE):
            earlier, current = (previous, source) if claim['source_id'] == SOURCE else (previous_guide, guide)
            assert row['claim_snapshot'] == claim_snapshot(previous_claims.get(claim['id'], claim), earlier)
            row['claim_snapshot'] = claim_snapshot(claim, current)
    eligible = {(row['id'], cid) for row in relations for cid, codes, *_ in CLAIMS
                if all(row[key].startswith('standard:') for key in ('from', 'to'))
                and {row[key][9:] for key in ('from', 'to')} <= set(codes)}
    assert eligible == {(rid, 'WAE07') for rid in RELATIONS}
    for rid, (finding, limit) in RELATIONS.items():
        reviewed['records'].append(dict(relation_id=rid, claim_id='WAE07', role='activity_context',
                                        finding=finding, limit=limit, relation_snapshot=relation_snapshot(by_id[rid]),
                                        claim_snapshot=claim_snapshot(claims['WAE07'], source)))
    apply_literature_context(relations, registry, registry=reviewed)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviewed)
    build_report()
    print('WWC earlier algebra findings: 10 review records, 24 findings, 3 claims, 3 observation tasks, 3 relation records')


if __name__ == '__main__':
    main()

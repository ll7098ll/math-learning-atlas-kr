"""Register the decimal sequencing study and reconcile the WWC cross-reference."""
import copy
import hashlib
from fractions import Fraction
from math import sqrt

from pypdf import PdfReader

from extend_lt2_length_assets_review import load, write
from literature_review import ROOT, build_report, digest, load_registry
from record_direct_learning_trajectory_trials import register
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


SOURCE = 'RITTLE_JOHNSON_KOEDINGER_2009_DECIMAL_SEQUENCE'
GUIDE = 'IES_FRACTIONS_2010'
PDF = 'https://pact.cs.cmu.edu/pubs/Rittle-Johnson%2C%20Koedinger%202009.pdf'
HANDBOOK = 'https://ies.ed.gov/ncee/wwc/Docs/referenceresources/wwc_procedures_v2_standards_handbook.pdf'
PDF_HASH = '940ea9f1650c59d12037ecba32c049221a42da55191730cf518e25fce4d0e4a7'
VISUAL = [1, 6, 7, 8, 9, 10, 11, 12, 13]
RELATION = 'REV-4수01-16-1'
CLAIMS = [
    ('RJK-01', ['4수01-13', '4수01-16'], [6, 7, 8, 9, 10],
     '실험 1은 교사별 두 학급을 서로 다른 조건에 무작위 배정했다. 초기 88명 중 두 검사를 완료한 77명을 분석했다. 원논문의 소수 연산 향상 비교는 F(1,74)=7.07, p=.01이었다. 자릿값 정답률 향상 비교는 p=.98이었다.',
     '무작위화 단위는 학생이 아니라 네 학급이다. 논문의 학생 수준 검정과 가이드의 학급 배정 결과 판정을 구별한다. 자릿값에서 유의하지 않았다는 결과는 동등성의 근거가 아니다.'),
    ('RJK-02', ['4수01-13', '4수01-16'], [9, 11, 12, 13, 15],
     '실험 2는 같은 학급 안에서 학생을 13명씩 무작위 배정했다. 논문의 소수 연산 향상 공변량 보정 비교는 F(1,23)=22.72, p<.001, η²=.50이다. 공개된 평균·표준편차와 WWC 2.0 방식으로 가이드 본문의 2.38을 재현했다.',
     '사전 5명과 사후의 다른 3명의 결측을 추정했다. 재계산한 값은 논문의 보정 검정과 별개다. 가이드 표 D2의 2.83과 공식 정정은 확인되지 않았으며, 결과를 국내 과제 효과나 분수 전체로 확대하지 않는다.'),
    ('RJK-03', ['4수01-13'], [6, 9, 11, 12, 13],
     '실험 2의 자릿값 결과는 문항 유형과 조건의 상호작용을 보였다. 그림 4에서 연습과 같은 형식은 개념 우선 조건의 추정 향상이 높았고, 새 형식은 번갈아 학습한 조건의 추정 향상이 높았다. 자릿값 표현과 같은 양을 다른 단위로 나타내는 설명을 각각 묻는다.',
     '그림은 공변량을 반영한 향상의 추정 주변평균이며 표 3의 단순 정답률 차와 구별한다. 막대만 보고 각 문항 유형의 집단 간 차이를 별도로 유의하다고 단정하지 않는다.'),
    ('RJK-04', ['4수01-16'], [6, 7, 8, 10, 11, 12],
     '실험 1에서 소수점 정렬 오류와 받아내림에서 줄여야 할 자리의 오류를 따로 채점했다. 실험 2에서는 0을 건너 교환하는 연산 예를 수업에 추가했다. 같은 단위끼리 놓는 설명과 교환 전후 양의 보존을 각각 확인하는 관찰에 참고한다.',
     '두 오류를 하나의 오개념으로 분류하지 않는다. 연구에는 국내 초등 기준의 수 범위 밖 문항과 외국 단위가 있다. 원논문의 검사 형식이나 결과를 현재 과제의 채점 타당성으로 바꾸지 않는다.'),
]
OBSERVATIONS = [
    dict(id='RJK-P1', standard_codes=['4수01-13'],
         question='3.46을 3일 4십분의 일 6백분의 일로 나타낸다. 백분의 일 16개를 쓰는 방법과 일 하나를 십분의 일로 바꾸는 방법을 각각 설명한다.',
         expected='3일 3십분의 일 16백분의 일, 2일 14십분의 일 6백분의 일은 모두 3.46이다. 한 단위를 줄인 만큼 같은 양을 다른 단위에 더한다.',
         interpretation='답의 개수와 교환한 단위의 크기·개수·전체 보존 설명을 나누어 기록한다. 원논문의 문항을 재현하거나 타당도가 검증된 검사로 해석하지 않는다.',
         student_validated=False),
    dict(id='RJK-P2', standard_codes=['4수01-16'],
         question='3.40−0.85를 계산한다. 소수점을 맞춘 이유와 백분의 일 자리에 줄 수 있는 양을 설명한 뒤 0.85를 더해 검산한다.',
         expected='3.40의 4십분의 일 중 하나를 백분의 일 10개로 풀고, 십분의 일은 일 하나를 풀어 13개로 만든다. 2일 13십분의 일 10백분의 일에서 0.85를 빼면 2.55이고 2.55+0.85=3.40이다.',
         interpretation='정렬과 교환의 오류를 따로 기록한다. 필요한 경우 처음 반응과 같은 단위나 교환을 알려 준 뒤의 반응을 나눈다.',
         student_validated=False),
]


def recalculate():
    groups = {
        'concepts_first': dict(n=13, pre=.52, post=.84, post_sd=.19),
        'iterative': dict(n=13, pre=.23, post=.94, post_sd=.12),
    }
    pooled_sd = sqrt((.19**2 + .12**2) / 2)
    correction = 1 - 3 / (4 * 26 - 9)
    gain_difference = float((Fraction('.94') - Fraction('.23')) - (Fraction('.84') - Fraction('.52')))
    estimated_g = gain_difference / pooled_sd * correction
    low = .37 / sqrt((.195**2 + .125**2) / 2) * correction
    high = .41 / sqrt((.185**2 + .115**2) / 2) * correction
    assert round(estimated_g, 2) == 2.38 and high < 2.83
    return dict(groups=groups, gain_difference=gain_difference, pooled_post_sd=pooled_sd,
                small_sample_correction=correction, reconstructed_g=estimated_g,
                rounding_sensitivity=[low, high], guide_prose=2.38, guide_table=2.83,
                author_ancova=dict(F=22.72, df=[1, 23], p_less_than=.001, eta_squared=.50),
                official_correction_confirmed=False, table_calculation_identified=False,
                handbook=HANDBOOK)


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        build_report()
        return
    pdf_path = ROOT / 'tmp/literature/rittle-johnson-koedinger-2009-decimal-sequencing.pdf'
    assert hashlib.sha256(pdf_path.read_bytes()).hexdigest() == PDF_HASH
    assert len(PdfReader(pdf_path).pages) == 18
    images = {str(p): hashlib.sha256((ROOT / f'tmp/pdfs/rittle-2009/p{p}.png').read_bytes()).hexdigest()
              for p in VISUAL}
    assert Fraction('3.46') == 3 + Fraction(3, 10) + Fraction(16, 100) == 2 + Fraction(14, 10) + Fraction(6, 100)
    assert Fraction('3.40') == 2 + Fraction(13, 10) + Fraction(10, 100)
    assert Fraction('3.40') - Fraction('.85') == Fraction('2.55')
    reconciliation = recalculate()
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography, queue = load(bibliography_path), load(queue_path)
    register(dict(
        id=SOURCE, year=2009, title='Iterating between lessons on concepts and procedures can improve mathematics knowledge',
        authors=['Rittle-Johnson, B.', 'Koedinger, K.'], authors_year='Rittle-Johnson·Koedinger, 2009',
        doi='https://doi.org/10.1348/000709908X398106', url=PDF, publisher='https://doi.org/10.1348/000709908X398106',
        sha256=PDF_HASH, pdf_pages=18, printed_pages='483–500', text_pages=list(range(1, 19)), visual_pages=VISUAL,
        kind='소수 개념과 연산의 교수 순서 비교',
        design='실험 1은 학급 단위 무작위 배정, 실험 2는 학급 내 학생 단위 무작위 배정.',
        sample='미국 6학년. 실험 1의 분석은 네 학급 77명, 실험 2는 각 조건 13명씩 총 26명이다.',
        scope='원논문 18쪽의 추출문과 표 1~4, 그림 3·4, 주요 방법·결과가 있는 선정 판면 9쪽을 대조했다.',
        limit='소수 자릿값과 연산의 즉시 검사다. 실험별 무작위화·결측 처리·검사 형식이 다르며 장기 유지와 국내 과제 효과는 확인하지 않았다.',
        next_review='가이드 표 D2의 산출 기록, 공식 정정, 원자료와 장기·전이 결과는 별도 확인한다.',
        supports='자릿값과 소수 계산의 수업 순서, 두 실험의 방법과 결과, 효과크기 불일치의 재계산.',
        results=dict(experiment_1=dict(initial=88, pre_or_post_absent=11, analyzed=77,
                                      randomized_classes=4, not_finished_included=9,
                                      arithmetic_F=7.07, arithmetic_df=[1, 74], arithmetic_p=.01,
                                      place_value_p=.98, alignment_percent_iterative_vs_concepts_first=[8, 20]),
                     experiment_2=dict(assigned_per_condition=13, missing_pre=5, missing_post_different_students=3,
                                       missing_method='EM', gain_by_familiarity_interaction_F=10.04,
                                       gain_by_familiarity_interaction_scope='place_value',
                                       gain_by_familiarity_interaction_p=.004),
                     effect_reconciliation=reconciliation),
        corrections=[
            ('PDF 9·13쪽', '표 3은 정답률과 표준편차, 그림 4는 추정 주변평균과 표준오차 막대다. 막대 높이를 단순 정답률 차로 전사하지 않는다.'),
            ('IES 분수 가이드 PDF 66~67쪽', '2.38은 WWC 2.0 방식으로 재현됐다. 같은 방식에서 표의 2.83은 재현되지 않았고 공식 정정은 미확인이다.'),
        ],
        claims=CLAIMS,
    ), images, bibliography, queue, registry)
    article = registry['sources'][SOURCE]
    article.update(observations=OBSERVATIONS, editorial_action='문헌 대응 4건과 자체 관찰 2건을 추가했다.')

    guide = registry['sources'][GUIDE]
    old_guide = copy.deepcopy(guide)
    guide_entry = next(item for item in bibliography if item['id'] == GUIDE)
    guide_entry['next_review'] = '26명 연구는 원논문과 대조했다. 가이드 본문의 2.38은 재현했고 표 D2의 2.83 산출 근거와 공식 정정은 미확인이다. 다른 원연구와 국내 과제의 효과는 별도 검토한다.'
    guide['bibliography_snapshot'] = digest(guide_entry)
    guide['limits'] = guide['limits'].replace(
        '26명 연구의 효과크기는본문2.38과표D2 2.83이 달라 수치 인용을 보류한다.',
        '26명 연구는 원논문의 공개 요약값으로 본문의 2.38을 재현했다. 표 D2의 2.83은 산출 근거와 공식 정정을 확인하지 못했다.')
    discrepancy = guide['source_discrepancies'][0]
    assert discrepancy['status'] == 'unresolved_do_not_select_one'
    discrepancy.update(status='prose_reproduced_table_unresolved',
                       followup='같은 계산에서 2.83이 나오지 않는다. 공식 정정과 해당 행의 산출 근거를 확인한다.',
                       followup_source_id=SOURCE, followup_snapshot=article['snapshot_file'],
                       followup_snapshot_sha256=article['snapshot_sha256'], recalculation=reconciliation)
    next(r for r in queue['literature_review'] if r['source']['id'] == GUIDE)['source'] = guide_entry

    relations = load(ROOT / 'data/revised_relations.json')['relations']
    by_id = {r['id']: r for r in relations}
    by_claim = {c['id']: c for c in registry['claims']}
    reviews = load(ROOT / FILE)
    for row in reviews['records']:
        claim = by_claim[row['claim_id']]
        if claim['source_id'] == GUIDE:
            assert row['claim_snapshot'] == claim_snapshot(claim, old_guide)
            row['claim_snapshot'] = claim_snapshot(claim, guide)
    new_pairs = {(r['id'], cid) for r in relations for cid, codes, *_ in CLAIMS
                 if all(r[k].startswith('standard:') for k in ('from', 'to'))
                 and {r[k][9:] for k in ('from', 'to')} <= set(codes)}
    assert new_pairs == {(RELATION, 'RJK-01'), (RELATION, 'RJK-02')}
    for cid, finding, limit in [
        ('RJK-01', '같은 자릿값을 정렬하는 설명을 계산 결과와 별도로 확인한다. 실험 1은 학급 단위 비교였다.',
         '자릿값 검사에서 유의한 향상 차이가 확인되지 않았다. 연산 결과로 자릿값 전체의 선행 숙달을 입증하지 않는다.'),
        ('RJK-02', '0을 건너 교환하는 예에서 줄어든 자리와 늘어난 자리를 표시하고 전체 양이 유지되는지 설명한다.',
         '두 수업 순서와 전체 검사 결과의 비교다. 이 설명 활동 하나의 효과크기나 필수 선수성을 뜻하지 않는다.'),
    ]:
        reviews['records'].append(dict(relation_id=RELATION, claim_id=cid, role='activity_context',
                                       finding=finding, limit=limit, relation_snapshot=relation_snapshot(by_id[RELATION]),
                                       claim_snapshot=claim_snapshot(by_claim[cid], article)))
    apply_literature_context(relations, registry, registry=reviews)
    write(bibliography_path, bibliography)
    write(queue_path, queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviews)
    build_report()
    print('Decimal sequencing: 4 claims, 2 observation designs, 2 relation records and a guide cross-reference')


if __name__ == '__main__':
    main()

"""Compare three registered analysis plans, the report, and WWC review criteria."""
from copy import deepcopy

from extend_lt2_length_assets_review import load, sha, write
from extend_making_pre_k_count_appendices_review import DATE, WWC, inspect_pdf
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_making_pre_k_count_review import CACHE, GRADE_3
from relation_literature_review import FILE, apply_literature_context, claim_snapshot


SID = GRADE_3['id']
PRIOR = 'c87b00b03416d721bf97457532c650a36344ba8d016718804ddd835317811d1e'
NOTE = f'data/literature_evidence/{SID}_preregistration_review_notes.json'
HANDBOOK = 'https://ies.ed.gov/ncee/wwc/Docs/referenceresources/WWC-Standards-Handbook-v4-1-508.pdf'
SCOPE = ' 3학년 비교별 사전등록 계획 3편과 최종 보고서의 배정, 표본 분모, 기초 공변량 대치, 탐색 분석을 대조했다. WWC 기준 4.1에서 결측 처리 방법과 추적 탈락 수준의 검토 단계를 확인했다.'
PLANS = [
    ('bm6va', 24, [13, 14, 15, 19, 20, 21], [15, 19], '983d2bb3c49f0aae7384aaa192ca6eb00319691ada81afffc1947b2c98ecaafc', [1448, 1371], 34.6, .3),
    ('ujxnr', 14, [7, 8, 9, 10, 11], [9, 11], '68a33cd50cbda079cb1efa8f68338a504f1ed8189d29038c26a5e11dbfa29e7f', [306, 311], 26.1, .1),
    ('68yxg', 14, [7, 8, 9, 10, 11], [9, 11], '6eccb1db43fdaa1c46fe66f0dbfe65d37608011445a5fe5a1eca57ed27586a98', [306, 345], 26.1, .1),
]
PLAN_LINKS = [f'https://osf.io/{row[0]}/' for row in PLANS]


def report_links(*pages):
    return [f'{GRADE_3["url"]}#page={n}' for n in pages]


COLLECTION, TESTING = '12실통02-02', '12실통03-04'
CLAIMS = [
    ('MPC21-07', [COLLECTION], [PLAN_LINKS[0], *report_links(25, 27, 53, 72)],
     'MPC 사전등록 표 2의 전체 시행 연도 분모는 학급 명단 2,819명이다. 최종 보고서는 동의와 연령 기준을 충족한 2,702명, 하나 이상 결과가 있는 2,277명, 수학 점수가 있는 1,844명을 구별한다.',
     '사전등록 표의 검사 자료 탈락 34.6%와 보고서의 수학 분석 탈락 약 32%는 분모와 자료 정의를 확인하고 비교한다.'),
    ('MPC21-08', [COLLECTION], [*PLAN_LINKS, *report_links(24, 58, 60, 61, 67, 68)],
     'High 5s 추가 비교는 MPC를 받은 공립학교에 남은 아동을 학교 내에서 개별 배정했다. 두 해 결합 비교는 공립학교의 첫 배정도 반영한다. 사전등록 표의 617명과 651명, 최종 보고서의 655명과 665명은 비교별로 보존한다.',
     '두 비교는 High 5s를 제공받도록 배정된 집단이 겹친다. 등록 당시 표와 최종 보고서의 차이를 특정 학생의 추가나 탈락으로 단정할 수 없다.'),
    ('MPC21-09', [COLLECTION, TESTING], [*PLAN_LINKS, *report_links(27, 65, 68), HANDBOOK + '#page=41', WWC],
     '사전등록 3편에서 다중 대치는 빠진 기초 평가 또는 공변량을 대상으로 한다. 최종 보고서도 기초 평가 대치를 기술했다. WWC 기준 4.1은 결측 처리 방법의 적합성 검토와 추적 탈락 수준을 판정하는 단계를 구별한다.',
     '기초 공변량 대치를 3학년 수학 점수의 대치로 간주하지 않는다. 공개 심사는 미충족 이유의 범주를 제시하며 어떤 세부 요구에서 실패했는지 확인할 기록은 없다.'),
    ('MPC21-10', [TESTING], [PLAN_LINKS[0], *report_links(32, 53, 71, 72)],
     'MPC 최종 보고서의 표 C.1은 전체 시행 연도 수학 주 분석 1,844명에서 p=.19를, 같은 연도 유치원 검사 하위표본 974명에서 탐색 p=.03을 보고했다. 다른 탐색 표본도 별도 행으로 제시한다.',
     '표본과 분석의 역할을 먼저 확인한다. 하위표본의 p값이 작다고 확인적 결과를 대체하거나 독립 재현으로 집계하지 않는다.'),
]
OBSERVATIONS = [
    dict(id='MPC21-P3', standard_codes=[COLLECTION],
         question='가상 연구의 학급 명단은 200명이고, 동의와 연령 조건을 충족한 사람은 180명이다. 결과가 하나라도 있는 사람은 160명, 수학 점수가 있는 사람은 135명이다. 적격자 기준 수학 점수 미확보 비율을 구하고 전체 명단 기준과 비교하라.',
         expected='적격자 기준은 (180−135)/180=25%다. 명단 전체 기준은 (200−135)/200=32.5%이며 적격자 외 학생도 포함한다. 160명은 수학 점수 확인 인원이 아니다.',
         interpretation='적격, 한 가지 이상 결과, 특정 결과의 분모와 분자를 구별한다.', student_validated=False),
    dict(id='MPC21-P4', standard_codes=[COLLECTION],
         question='가상 연구에서 기관을 먼저 배정하고, 실험 기관에 남은 아동을 추가 활동 제공 여부로 다시 배정했다. 추가 활동 대 기본 프로그램 비교와 결합 프로그램 대 기존 교육 비교의 배정 단위를 구별하라.',
         expected='추가 활동은 같은 기관의 아동별 배정을 사용한다. 결합 비교는 기관별 최초 배정도 반영해야 한다. 추가 활동 집단은 두 비교에 공통으로 들어간다.',
         interpretation='첫 배정과 두 번째 배정, 잔류 조건과 집단 중복을 확인한다.', student_validated=False),
    dict(id='MPC21-P5', standard_codes=[COLLECTION, TESTING],
         question='가상 추적 자료에서 가 학생은 시작 때의 언어 점수만 없고 나 학생은 종료 수학 점수만 없다. 연구팀이 시작 점수 결측만 대치했다. 어떤 값이 아직 없으며 최종 심사를 판단하려면 무엇을 더 확인해야 하는가?',
         expected='나 학생의 종료 수학 점수는 여전히 없다. 대치 대상, 대치 절차와 표준오차 산출, 종료 자료 미확보의 분모와 집단 차이를 각각 확인해야 한다.',
         interpretation='기초 공변량과 결과의 시점 및 역할을 구별한다. 탈락률만으로 대치 방법 적합성을 판정하는지도 관찰한다.', student_validated=False),
    dict(id='MPC21-P6', standard_codes=[TESTING],
         question='가상 연구에서 사전 지정한 주 분석의 p값은 .18, 같은 연구의 하위표본 탐색 분석은 .03이다. 각 분석에서 5% 기준을 적용한 결과와 보고할 때의 순서를 설명하라.',
         expected='주 분석에서는 기각하지 않고 탐색 분석은 해당 비교에서 기각한다. 사전 지정한 주 분석을 먼저 보고하고 같은 연구의 탐색 결과로 따로 표시한다.',
         interpretation='비교별 판정과 확인적·탐색적 역할을 따로 기록하며, 표본이 겹치는 두 분석을 독립 증거로 세는지 확인한다.', student_validated=False),
]


def plans_evidence():
    plans = []
    for osf_id, total, pages, visuals, fingerprint, counts, attrition, differential in PLANS:
        registration = CACHE / f'osf-registrations-{osf_id}.json'
        attrs = load(registration)['data']['attributes']
        upload, = attrs['registration_responses']['uploader']
        assert attrs['public'] and attrs['date_registered'].startswith('2020-06-24T')
        assert upload['file_hashes']['sha256'] == fingerprint
        images = inspect_pdf(f'osf-plan-{osf_id}', fingerprint, total, pages, visuals)
        plans.append(dict(osf_id=osf_id, registered=attrs['date_registered'], title=attrs['title'],
                          registration_url=f'https://api.osf.io/v2/registrations/{osf_id}/',
                          registration_sha256=sha(registration), pdf_sha256=fingerprint, pdf_pages=total,
                          selected_text_pages=pages, rendered_page_sha256=images,
                          table_2_total=sum(counts), table_2_groups=counts, table_2_test_attrition_percent=attrition,
                          table_2_test_differential_percentage_points=differential, referenced_attrition_standard='4.0'))
    return plans


def main():
    registry = load_registry()
    source = registry['sources'][SID]
    if source['snapshot_file'] == NOTE:
        build_report()
        return
    previous = deepcopy(source)
    assert source['snapshot_sha256'] == PRIOR
    notes = load(ROOT / previous['snapshot_file'])
    assert sha(ROOT / previous['snapshot_file']) == PRIOR
    assert sha(CACHE / f'{GRADE_3["file"]}.pdf') == GRADE_3['sha256']
    plans = plans_evidence()
    handbook_sha = 'f3950189a71bc377e1b60af1bc98fffee1479a579626e61072207bf100187571'
    handbook_images = inspect_pdf('wwc-standards-handbook-v4.1', handbook_sha, 116, [41, 42], [41, 42])
    samples = dict(registered_table_2_denominators=[2819, 617, 651], report_reference_samples=[2702, 655, 665],
                   any_result=[2277, 556, 587], math_result=[1844, 456, 481], math_group_counts=[[945, 899], [226, 230], [226, 255]],
                   report_mpc_subsample=dict(math_result=974, p=.03, exploratory=True))
    assert samples['registered_table_2_denominators'] == [row['table_2_total'] for row in plans]
    assert samples['math_result'] == [sum(pair) for pair in GRADE_3['results']['math_outcome']]
    assert samples['any_result'] == [sum(pair) for pair in GRADE_3['results']['any_outcome']]
    assert all(m <= a <= r for m, a, r in zip(samples['math_result'], samples['any_result'], samples['report_reference_samples']))
    assert round(100 * (1 - 1844 / 2702), 2) == 31.75
    report_images = [27, 53, 65, 68, 72]
    scope = source['read_scope'] + SCOPE
    notes.update(date=DATE, read_scope=scope,
                 selected_text_pages=sorted(set(notes['selected_text_pages']) | {53, 54, 58, 60, 61, 71, 72}),
                 visual_pdf_pages=sorted(set(notes['visual_pdf_pages']) | set(report_images)),
                 rendered_page_sha256={**notes['rendered_page_sha256'], **{
                     str(n): sha(CACHE / 'followup-pages' / f'{GRADE_3["file"]}-{n}.png') for n in report_images}},
                 prior_snapshot=dict(file=previous['snapshot_file'], sha256=PRIOR),
                 preregistration_review=dict(plans=plans, samples=samples, report_mpc_attrition_percent=31.75,
                     shared_high5s_math_group_n=226, imputation_scope='baseline_covariates',
                     final_outcome_imputation_verified=False, study_review_worksheet_verified=False,
                     handbook=dict(url=HANDBOOK, sha256=handbook_sha, pdf_pages=116, standard='4.1',
                         rendered_page_sha256=handbook_images, steps=['method_acceptability', 'attrition_level'])))
    notes['reading_log'].append('사전등록의 표 2와 최종 보고서의 결과별 분모, 비교별 배정과 기초 자료 대치 사양을 대조했다.')
    notes['source_corrections'].append(dict(location='사전등록 표 2 및 최종 보고서 표 2.1·C.1',
        issue='등록 시점 표본과 보고서 분석 집단, 확인적 결과와 탐색 하위표본을 분리한다.'))
    bibliography = load(ROOT / 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SID)
    book.update(review_scope=scope, next_review='후속 출판 논문의 판면, 민감도 분석의 구현 및 공개되지 않은 세부 심사 산출 근거를 확인한다. 독립 검토와 실제 학생 반응은 별도다.')
    write(ROOT / NOTE, notes)
    source.update(date=DATE, read_scope=scope, snapshot_file=NOTE, snapshot_sha256=sha(ROOT / NOTE),
                  snapshot_history=[*previous.get('snapshot_history', []),
                      {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), observations=previous['observations'] + OBSERVATIONS,
                  editorial_action='사전등록과 최종 보고서 대조의 근거 4건 및 자체 관찰 과제 4개를 추가했다.')
    for cid, codes, locations, support, limit in CLAIMS:
        registry['claims'].append(dict(id=cid, source_id=SID, role='empirical_result_with_scope',
            empirical_scope=source['empirical_scope'], standard_codes=codes, locations=locations,
            support=support, does_not_establish=limit, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes}))
    source_claims = {row['id']: row for row in registry['claims'] if row['source_id'] == SID}
    queue = load(ROOT / 'data/content_review_queue.json')
    entry = next(row for row in queue['literature_review'] if row['source']['id'] == SID)
    entry.update(source=book, claim_ids=list(source_claims))
    reviews = load(ROOT / FILE)
    for row in reviews['records']:
        claim = source_claims.get(row['claim_id'])
        if claim:
            assert row['claim_snapshot'] == claim_snapshot(claim, previous)
            row['claim_snapshot'] = claim_snapshot(claim, source)
    relations = load(ROOT / 'data/revised_relations.json')['relations']
    assert not {(row['id'], cid) for row in relations for cid, codes, *_ in CLAIMS
                if all(row[k].startswith('standard:') for k in ('from', 'to'))
                and {row[k][9:] for k in ('from', 'to')} <= set(codes)}
    apply_literature_context(relations, registry, registry=reviews)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviews)
    build_report()
    print('MPC preregistrations: 3 plans, 4 claims, 4 observation tasks')


if __name__ == '__main__':
    main()

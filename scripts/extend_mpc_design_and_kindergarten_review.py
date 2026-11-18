"""Compare MPC design evidence with the kindergarten sample sensitivity check."""
from copy import deepcopy

from extend_lt2_length_assets_review import load, sha, write
from extend_making_pre_k_count_appendices_review import DATE, inspect_pdf
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_making_pre_k_count_review import CACHE, FAMILY, KINDER
from relation_literature_review import FILE, apply_literature_context, claim_snapshot


DESIGN, REPORT = 'MATTERA_ET_AL_2017_MPC_DESIGN', KINDER['id']
DOI = 'https://doi.org/10.1016/bs.acdb.2017.04.002'
ERIC = 'https://files.eric.ed.gov/fulltext/ED651010.pdf'
DESIGN_SHA = '1c73db048ed405ef14a7466b3400f4ec6a0c28cadf64ec94b8b97e858c233b05'
PRIOR = '06b98f96d87b12069e060c8bac450fcc7bf498f770ab688ff723821bba25b9fe'
SAGE = 'https://journals.sagepub.com/doi/10.1177/0193841X231159472'
SCOPE = 'ERIC 공개본에서 프로그램 선정, 주간 운영 기준, 통상 수업, 검사 선택과 두 단계 배정을 설명하는 선정 본문 및 표 1·2를 대조했다.'
REPORT_SCOPE = ' 부록 B·H에서 최초 배정, 주 분석의 학교 잔류·추가 배정 조건, 최초 배정 추적 표본의 효과 추정치를 대조했다.'
LIMIT = '동일 연구의 설계 설명이다. 교육과정 선정표나 운영 기준으로 활동의 효과 또는 국내 학생의 학습 순서를 확정하지 않는다.'
COLLECTION, TESTING, ADD, SHAPE = '12실통02-02', '12실통03-04', '2수01-05', '2수03-03'

CLAIMS = [
    (DESIGN, 'MPCD-01', [ADD], [6, 7, 8],
     '설계 장의 선정표는 Building Blocks와 Big Math for Little Kids를 기존 효과 근거, 활동 범위와 연수 등으로 비교한다. Building Blocks의 스페인어 지원은 일부 자료와 소프트웨어로 한정됐다.',
     '교육과정 선정 기준과 실제 활동에서 덧셈 설명을 이해하는지를 별도로 점검한다. 두 프로그램의 효과를 직접 비교한 시험으로 읽지 않는다.'),
    (DESIGN, 'MPCD-02', [COLLECTION], [11, 12, 13, 14, 15],
     '표 2의 대집단 활동 기준은 출석일 중 실시한 날의 비율 66% 이상이고, 소집단 활동 기준은 전체 아동 중 참여한 비율 75% 이상이다. 연구는 통상 수업 집단에서도 수업 시간과 내용 자료를 수집했다.',
     '날짜 단위의 시행률과 아동 단위의 참여율을 구별한다. 통상 수업에도 수학이 포함될 수 있으므로 비교 조건의 실제 내용을 기록한다.'),
    (DESIGN, 'MPCD-03', [ADD, SHAPE], [17, 18, 19],
     'ECLS-B는 수 감각, 연산, 측정, 도형, 공간과 패턴을 다루는 검사이고 WJ 응용문제는 전국 규준을 갖춘 검사다. 설계 장은 시점이 달라질 때 같은 도구를 유지하거나 점수를 연결할 수 있는지 검토했다.',
     '검사 전체 점수로 덧셈 전략이나 도형 설명을 판단하지 않는다. 도구가 바뀐 두 시점의 점수를 바로 빼서 개인의 변화로 해석하지 않는다.'),
    (DESIGN, 'MPCD-04', [COLLECTION], [15, 16, 23, 24, 25],
     '취학 전에는 기관을 배정했고 유치원 High 5s는 MPC를 받은 공립학교에서 아동을 학교 내 배정했다. 진행자 25명, 감독자 5명, 클럽 79개, 공립학교 24개는 운영 규모다.',
     '배정 단위, 운영 단위, 아동 결과의 관찰 단위를 나눈다. 2017년 설계 장에서 언급한 초기 결과는 이후 유치원·3학년 최종 분석과 시점을 구별한다.'),
    (REPORT, 'MPC18-08', [COLLECTION], [75, 135, 136],
     'High 5s 최초 동의 배정은 320명 대 335명이다. 주 분석 303명 대 310명에는 High 5s 참여에 동의하지 않았으나 별도 배정된 18명이 포함됐다. 표 H.1은 최초 동의 배정 중 추적 평가를 받은 307명 대 315명을 사용했다.',
     '같은 학교 잔류 조건과 High 5s 참여 동의 및 실제 추적을 각각 확인한다. 최초 배정 655명과 표 H.1 결과 622명을 구별한다.'),
    (REPORT, 'MPC18-09', [TESTING], [52, 135, 136],
     'High 5s 추가 비교의 주 분석과 표 H.1에서 REMA-K 효과 크기는 .19와 .20이며 인쇄 p는 모두 .01이다. 두 표의 별 표기는 각각 두 개와 세 개다. WJ 효과 크기는 각각 .09이며 p는 .18과 .20이다.',
     '두 표본은 같은 연구에서 분석 조건을 달리한 것이다. 인쇄 p값과 별 표기를 그대로 보존하고 반올림된 값으로 정확한 p나 별 표기의 차이를 재구성하지 않는다.'),
]

OBSERVATIONS = {
    DESIGN: [
        dict(id='MPCD-P1', standard_codes=[COLLECTION],
             question='가상 학급에서 아이들이 출석한 5일 중 4일에 전체 활동을 했고, 전체 아동 20명 중 14명이 소집단 활동에 참여했다. 실시일 기준 66%와 참여 기준 75%를 각각 충족하는가?',
             expected='날짜 단위는 4/5=80%라 기준을 충족한다. 아동 단위는 14/20=70%라 기준에 미달한다.',
             interpretation='일수와 아동 수를 섞지 않고, 활동 제공과 실제 참여를 따로 기록한다.', student_validated=False),
        dict(id='MPCD-P2', standard_codes=[ADD, SHAPE],
             question='그림 속 블록 4개에 2개를 더한다. 합을 설명한 뒤, 별도로 제시된 사각형과 삼각형을 특징을 들어 구분한다. 두 과제의 총점만 같으면 덧셈과 도형을 같은 방식으로 이해했다고 할 수 있는가?',
             expected='합은 6개다. 제시한 두 도형은 곧은 변이 각각 네 개와 세 개다. 같은 총점이어도 두 과제의 수행과 설명은 다를 수 있다.',
             interpretation='개수 합의 설명, 도형을 분류한 근거, 문항별 응답과 총점을 따로 기록한다.', student_validated=False),
    ],
    REPORT: [
        dict(id='MPC18-P3', standard_codes=[COLLECTION],
             question='가상 연구에서 동의 후 배정된 아동은 100명이고 그중 92명이 추적됐다. 주 분석에는 같은 학교에 남아 추적된 84명과 별도로 배정된 미참여 4명이 들어갔다. 두 분석의 분모와 최초 배정에서 추적되지 않은 비율을 구하라.',
             expected='최초 배정 추적 분석은 92명, 주 분석은 88명이다. 최초 배정자 중 추적되지 않은 비율은 8/100=8%다.',
             interpretation='배정, 실제 참여, 결과 확보와 분석 포함 조건을 구별한다.', student_validated=False),
        dict(id='MPC18-P4', standard_codes=[TESTING],
             question='가상 연구가 같은 시험 자료의 두 분석에서 p값을 소수 둘째 자리까지 .01로 인쇄했다. 한 표는 p<.01을, 다른 표는 p<.05를 표시했다. 두 p값이 정확히 같은지 설명하라.',
             expected='반올림 전 p값이 .008과 .012라면 둘 다 .01로 인쇄되지만 .01 미만 여부는 다르다. 두 인쇄값으로 실제 p값이 같다고 판단할 수 없다.',
             interpretation='인쇄 정밀도와 표의 기준을 확인한다. 예시의 수치가 원연구의 미공개 p값인지도 구별한다.', student_validated=False),
    ],
}


def main():
    registry = load_registry()
    if DESIGN in registry['sources']:
        build_report()
        return
    report = registry['sources'][REPORT]
    previous = deepcopy(report)
    assert previous['snapshot_sha256'] == PRIOR
    assert sha(ROOT / previous['snapshot_file']) == PRIOR
    assert sha(CACHE / f'{KINDER["file"]}.pdf') == KINDER['sha256']
    pages, visuals = [6, 7, 8, *range(11, 20), 23, 24, 25], [8, 12, 16, 19, 23]
    images = inspect_pdf('eric-2017-design-chapter', DESIGN_SHA, 28, pages, visuals)
    added_report_pages = [75, 135, 136]
    report_images = {str(n): sha(CACHE / 'followup-pages' / f'{KINDER["file"]}-{n}.png') for n in added_report_pages}
    cohort = dict(initial_consent_assignment=[320, 335], primary_analysis=[303, 310], original_assignment_followup=[307, 315],
                  second_phase_nonconsenting=18, original_followup_missing=33, original_followup_missing_percent=5.04)
    assert [sum(cohort[k]) for k in ('initial_consent_assignment', 'primary_analysis', 'original_assignment_followup')] == [655, 613, 622]
    assert round(100 * cohort['original_followup_missing'] / 655, 2) == cohort['original_followup_missing_percent']
    assert cohort['primary_analysis'] == KINDER['results']['compared_children'][1]
    bibliography = load(ROOT / 'data/sources.json')
    queue = load(ROOT / 'data/content_review_queue.json')
    design_book = dict(id=DESIGN, year=2017, url=DOI,
        title='Designing Studies to Test Causal Questions About Early Math: The Development of Making Pre-K Count',
        authors=['Shira K. Mattera', 'Pamela A. Morris', 'Robin Jacob', 'Michelle Maier', 'Natalia Rojas'],
        kind='MPC 동일 연구의 설계 장', review_scope=SCOPE, does_not_establish=LIMIT,
        next_review='설계 논문의 제한된 본문과 후속 유치원 평가 표를 계속 대조한다.',
        supports=['프로그램 선정', '운영·참여 단위', '검사 선택', '두 단계 배정'])
    assert all(b['id'] != DESIGN for b in bibliography)
    bibliography.append(design_book)
    design_note = f'data/literature_evidence/{DESIGN}_review_notes.json'
    write(ROOT / design_note, dict(source_id=DESIGN, source_url=DOI, source_pdf_url=ERIC,
        source_asset_kind='pdf', source_pdf_sha256=DESIGN_SHA, source_pdf_redistributed=False, contains_source_full_text=False,
        date=DATE, reviewer='Codex', read_scope=SCOPE, pdf_pages=28, selected_text_pages=pages, visual_pdf_pages=visuals,
        rendered_page_sha256=images, study_family=FAMILY, design_only=True,
        reading_log=['선정표의 표식과 각주, 활동 기준별 분모, 검사 목적 및 배정 수준을 확인했다.'],
        source_corrections=[dict(location='표 1·2', issue='프로그램 선정표와 운영 기준을 직접 효과 추정으로 해석하지 않는다.')],
        planned_weekly_benchmarks=dict(whole_group_attendance_days_percent=66, small_group_all_children_percent=75),
        implementation_counts=dict(facilitators=25, supervisors=5, clubs=79, public_schools=24),
        design_followup=dict(url=SAGE, reviewed='abstract_and_references', reported_kindergarten_n=613, full_text_verified=False)))
    registry['sources'][DESIGN] = dict(source_id=DESIGN, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
        snapshot_kind='authored_review_notes', source_asset_kind='pdf', source_pdf_sha256=DESIGN_SHA,
        snapshot_file=design_note, snapshot_sha256=sha(ROOT / design_note), redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(design_book), display=dict(title=design_book['title'], url=DOI, authors_year='Mattera 외, 2017'),
        read_scope=SCOPE, limits=LIMIT, scope_note='중재 설계와 평가 절차를 확인한다.', method_note='ERIC 본문·선정 판면과 유치원 보고서의 분석 분모를 대조했다.',
        editorial_action='근거 4건과 자체 관찰 과제 2개를 추가했다.', independent_review=False, student_validated=False,
        observations=OBSERVATIONS[DESIGN])
    queue['literature_review'].append(dict(source=design_book, status='self_read_claim_mapping',
        evidence_file='data/literature_claim_reviews.json', claim_evidence_fields=design_book['supports'], claim_ids=[]))

    report_book = next(b for b in bibliography if b['id'] == REPORT)
    scope = report['read_scope'] + REPORT_SCOPE
    report_book.update(review_scope=scope, next_review='검사 전체 시행·중단 규칙, 문항별 도달과 응답, 2023년 설계 논문 전체 결과표를 대조한다.')
    notes = load(ROOT / previous['snapshot_file'])
    notes.update(date=DATE, read_scope=scope, selected_text_pages=sorted(set(notes['selected_text_pages']) | set(added_report_pages)),
        visual_pdf_pages=sorted(set(notes['visual_pdf_pages']) | set(added_report_pages)),
        rendered_page_sha256={**notes['rendered_page_sha256'], **report_images},
        prior_snapshot=dict(file=previous['snapshot_file'], sha256=PRIOR),
        sample_sensitivity=dict(cohort=cohort, primary_table='3.2', sensitivity_table='H.1',
            rema_k_effect_sizes=[.19, .20], rema_k_printed_p=['.01', '.01'], rema_k_markers=['**', '***'],
            wj_effect_sizes=[.09, .09], wj_p=[.18, .20], samples_independent=False))
    notes['reading_log'].append('주 분석의 포함 조건과 최초 배정 추적 표의 두 수학 검사 결과를 판면에서 대조했다.')
    notes['source_corrections'].append(dict(location='PDF 52·135~136쪽', issue='최초 배정 분모와 두 분석 표본, 인쇄 p값과 별을 구별한다.'))
    report_note = f'data/literature_evidence/{REPORT}_sample_sensitivity_review_notes.json'
    write(ROOT / report_note, notes)
    report.update(date=DATE, read_scope=scope, snapshot_file=report_note, snapshot_sha256=sha(ROOT / report_note),
        snapshot_history=[*previous.get('snapshot_history', []),
            {k: previous[k] for k in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
        bibliography_snapshot=digest(report_book), observations=previous['observations'] + OBSERVATIONS[REPORT],
        editorial_action='표본 민감도 근거 2건과 자체 관찰 과제 2개를 추가했다.')
    next(e for e in queue['literature_review'] if e['source']['id'] == REPORT)['source'] = report_book

    for sid, cid, codes, refs, support, limit in CLAIMS:
        base = ERIC if sid == DESIGN else KINDER['url']
        row = dict(id=cid, source_id=sid, role='related_theoretical_context', standard_codes=codes,
            locations=[f'{base}#page={n}' for n in refs], support=support, does_not_establish=limit,
            independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes})
        if sid == REPORT:
            row.update(role='empirical_result_with_scope', empirical_scope=report['empirical_scope'])
        registry['claims'].append(row)
    claims = {r['id']: r for r in registry['claims']}
    for item in queue['literature_review']:
        sid = item['source']['id']
        if sid in OBSERVATIONS:
            item['claim_ids'] = [r['id'] for r in claims.values() if r['source_id'] == sid]
    reviews = load(ROOT / FILE)
    for row in reviews['records']:
        claim = claims[row['claim_id']]
        if claim['source_id'] == REPORT:
            assert row['claim_snapshot'] == claim_snapshot(claim, previous)
            row['claim_snapshot'] = claim_snapshot(claim, report)
    relations = load(ROOT / 'data/revised_relations.json')['relations']
    assert not {(r['id'], cid) for r in relations for _, cid, codes, *_ in CLAIMS
                if all(r[k].startswith('standard:') for k in ('from', 'to'))
                and {r[k][9:] for k in ('from', 'to')} <= set(codes)}
    apply_literature_context(relations, registry, registry=reviews)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviews)
    build_report()
    print('MPC design and kindergarten sample: 1 source, 6 claims, 4 observation tasks')


if __name__ == '__main__':
    main()

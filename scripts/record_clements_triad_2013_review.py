"""Register the first-grade TRIAD follow-up with its distinct analysis samples."""
from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value


SOURCE = 'CLEMENTS_ET_AL_2013_TRIAD_FOLLOWTHROUGH'
DOI = 'https://doi.org/10.3102/0002831212469270'
PUBLISHER = 'https://journals.sagepub.com/doi/10.3102/0002831212469270'
AUTHOR = 'https://www.researchgate.net/publication/254325922_Longitudinal_Evaluation_of_a_Scale-Up_Model_for_Teaching_Mathematics_With_Trajectories_and_Technologies'
KINDERGARTEN = 'https://researchconnect.suny.edu/en/publications/longitudinal-evaluation-of-a-scale-up-model-for-teaching-mathemat/'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
SCOPE = ('출판사 초록과 저자가 공개한 선출판판 전사에서 연구 개요, 유치원 결과 회고, 배정·표본·교사 지원, '
         'REMA 도구, 표 1~5와 결과·한계의 관련 문단을 대조했다. 원논문 PDF 파일과 판면은 미확보다.')
LIMIT = ('미국 두 도시 학군의 동일 TRIAD 코호트를 초등 1학년까지 추적했다. '
         'REMA 총점 비교에서 국내 개별 성취기준과 과제의 효과 또는 교사 연수 요소별 효과는 확인할 수 없다.')
NEXT = ('2012년 유치원 원논문의 표·모형과 유의 판정 차이, 2013년 논문의 원본 판면 및 부록, '
        '같은 표본을 사용한 후속 재분석의 표본 선택과 척도를 대조한다.')
COHORT = dict(
    randomized_schools=42, original_pre_k_analyzed=1305, first_grade_tested=1127,
    first_grade_tested_classrooms=347, first_grade_tested_schools=172,
    arm_order=['FT', 'NFT', 'control'], itt_counts=[383, 375, 321], tot_counts=[262, 253, 235],
)
CONTRASTS = dict(
    contrast_order=['FT vs control', 'NFT vs control', 'FT vs NFT'],
    itt_hedges_g=[.38, .21, .18], itt_table_2_p=['<.001', '.014', '.032'],
    tot_hedges_g=[.51, .28, .24], tot_p=['<.001', '.028', '.046'],
    tot_pre_k_pre_and_post_adjusted=dict(contrast='FT vs NFT', g=.25, p=.032),
)
SOURCE_CORRECTIONS = [
    dict(location='저자 공개 페이지 상단 초록과 본문 초록',
         issue='상단의 유치원 결과는 2012년 논문의 기관 서지 초록과 일치한다. 2013년 초등 1학년 본문 결과로 옮기지 않는다.'),
]
OUTCOME_CODES = ['2수01-01', '2수01-04', '2수01-05', '2수03-03']
CLAIMS = [
    ('BB2013-01', OUTCOME_CODES, 'empirical_result_with_scope', 'ITT',
     '같은 취학 전 코호트 1,305명에서 초등 1학년 말 1,127명을 검사했다. 두 검사 부분을 모두 완료한 1,079명의 원래 배정 기준 분석에서 REMA 수학 총점의 효과크기 g는 후속 지원 대 대조 .38, 취학 전 중재만 대 대조 .21, 후속 지원 대 취학 전 중재만 .18이었다.',
     '원래 배정을 유지했지만 결과가 확보된 아동을 분석했다. 2011년 연구와 같은 코호트이며, 총점 차이는 개별 성취기준의 효과를 뜻하지 않는다.'),
    ('BB2013-02', ['2수01-04', '2수01-05', '2수03-03'], 'empirical_result_with_scope', 'TOT',
     '배정 학교에 남고 검사 등 포함 조건을 충족한 750명의 분석에서 세 비교의 g는 각각 .51, .28, .24였다. 같은 하위 표본에서 취학 전 사전·사후 점수를 모두 보정한 후속 지원 대 취학 전 중재만 비교는 g=.25였다.',
     '배정 이후 학교 잔류 및 검사 완료로 골라진 표본이므로 이 값과 원래 배정 기준 분석의 차이로 지원 기간이나 지원량의 효과를 분리할 수 없다.'),
    ('BB2013-03', ['2수01-01', '2수01-04', '2수01-05', '2수03-06'], 'related_theoretical_context', None,
     '초등 1학년 교사들은 학군 교육과정을 사용하면서, 이전 학습을 파악하고 학생의 사고 수준에 맞춰 세기·덧셈·뺄셈·길이 등의 과제를 조정하는 연수를 받았다. 두 중재 조건의 취학 전 프로그램은 같았다.',
     '연수와 자료를 함께 제공한 연구다. 길이 비교나 특정 발문에 대한 단독 효과 및 국내 학년별 지도 순서는 별도로 검토해야 한다.'),
    ('BB2013-04', OUTCOME_CODES, 'related_theoretical_context', None,
     'REMA는 수와 기하의 두 검사 부분에서 개별 면담 응답을 모아 Rasch 척도의 총점을 산출했다. 초등 1학년 검사에는 영역별 시작·중단 기준을 적용했다. 전체 점수와 수 합성·연산·도형 구성의 과제별 관찰을 구분한다.',
     '검사에 해당 주제가 포함됐다는 사실로 특정 과제의 변화나 국내 성취기준 도달을 판단할 수 없다.'),
]


def analysis_scope(sample):
    if sample == 'ITT':
        return dict(
            design='school_cluster_randomized_followup_with_observed_outcomes',
            sample_description='원래 학교 배정을 유지한 초등 1학년 검사 완료자 1,079명이다.',
            inference_limit='원래 배정의 비교이며 결과가 확보되지 않은 학생이 있다.',
            student_outcome_study=True, causal_effect_established=True, local_effect_tested=False,
        )
    return dict(
        design='school_cluster_trial_post_assignment_selected_followup',
        sample_description='배정 학교 잔류와 검사 완료 등 조건을 충족한 750명이다.',
        inference_limit='배정 후 조건으로 선정된 하위 표본에서 관측한 모형 결과다.',
        student_outcome_study=True, causal_effect_established=False, local_effect_tested=False,
    )


def main():
    registry = load_registry()
    ids = [row[0] for row in CLAIMS]
    if SOURCE in registry['sources']:
        assert set(ids) == {c['id'] for c in registry['claims'] if c['source_id'] == SOURCE}
        build_report()
        return
    assert 'CLEMENTS_ET_AL_2011_BUILDING_BLOCKS' in registry['sources']
    assert sum(COHORT['itt_counts']) == 1079 and sum(COHORT['tot_counts']) == 750
    assert COHORT['first_grade_tested'] - sum(COHORT['itt_counts']) == 48
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography, queue = load(bibliography_path), load(queue_path)
    assert all(row['id'] != SOURCE for row in bibliography)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    text_scope = dict(
        url=AUTHOR, uploaded_by='Douglas H. Clements', article_pdf_obtained=False,
        article_printed_pages=[1, 39], journal_issue_pages=[812, 850],
        reviewed_pagination='OnlineFirst Version of Record, 2012-12-27',
        selected_sections=[
            dict(section='논문 초록', printed_pages=[1, 2]),
            dict(section='유치원 결과 회고', printed_pages=[6, 6]),
            dict(section='학교 배정, 표 1 표본과 후속 지원', printed_pages=[8, 10]),
            dict(section='REMA 개별 면담과 문항 범위', printed_pages=[12, 13]),
            dict(section='초등 1학년 REMA 결과와 표 2~5', printed_pages=[15, 21]),
            dict(section='초등 1학년 결과 요약과 구성요소의 한계', printed_pages=[25, 31]),
        ],
    )
    notes = dict(
        source_id=SOURCE, source_url=DOI, date='2026-11-09', reviewer='Codex',
        source_asset_kind='author_web_text', author_text_review=text_scope, read_scope=SCOPE,
        original_page_layout_review=False, contains_source_full_text=False, source_pdf_redistributed=False,
        same_cohort_as='CLEMENTS_ET_AL_2011_BUILDING_BLOCKS', cohort=COHORT, first_grade_effects=CONTRASTS,
        source_corrections=SOURCE_CORRECTIONS,
        reading_log=[
            '원래 배정 기준 표본은 1,079명이며 배정 학교 잔류 등으로 제한한 표본은 750명이다. 학교 배정 42곳과 추후 검사 학교 172곳을 구별한다.',
            '정식 출판사 초록의 .51·.28·.24를 본문 표 4 분석에 연결했다. 표 2 원래 배정 기준 결과와 표 5 사전·사후 점수 보정 결과는 별도다.',
            '저자 공개 페이지 상단에 표시된 유치원 초록의 문구와 수치는 2012년 논문의 기관 서지 초록과 일치한다. 본문에 붙은 2013년 초록과 시점을 구별했다.',
        ],
        crosschecks=dict(
            publisher=PUBLISHER, kindergarten_abstract=KINDERGARTEN,
            kindergarten_significance_discrepancy='2012년 초록은 유치원 말 원래 배정 기준 분석의 두 비교를 유의하다고 적었다. 2013년 선출판판의 유치원 회고는 후속 지원 대 대조만 유의했다고 적었다. 2012년 표와 모형을 확인하기 전에는 두 진술을 합치지 않는다.',
        ),
    )
    entry = dict(
        id=SOURCE, year=2013, url=DOI, kind='학교 단위 무작위 배정 연구의 초등 1학년 후속 보고',
        title='Longitudinal Evaluation of a Scale-Up Model for Teaching Mathematics With Trajectories and Technologies: Persistence of Effects in the Third Year',
        authors=['Douglas H. Clements', 'Julie Sarama', 'Christopher B. Wolfe', 'Mary Elaine Spitler'],
        review_scope=SCOPE, next_review=NEXT, does_not_establish=LIMIT,
        supports=['원래 배정 분석과 배정 학교 잔류 표본 분석', '후속 교사 지원의 구성', 'REMA 총점과 개별 과제의 차이'],
    )
    path = ROOT / NOTES
    write(path, notes)
    bibliography.append(entry)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=notes['date'],
        snapshot_kind='authored_review_notes', source_asset_kind='author_web_text', author_text_review=text_scope,
        snapshot_file=NOTES, snapshot_sha256=sha(path), redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=DOI, authors_year='Clements 외, 2013'),
        read_scope=SCOPE, scope_note='2011년 유아 연구와 같은 표본의 초등 1학년 결과를 분석별로 연결한다.',
        method_note='출판사 초록, 저자 공개 선출판판 전사, 2012년 기관 서지 초록을 대조했다.',
        limits=LIMIT, independent_review=False, student_validated=False,
        editorial_action='문헌 대응 4건을 추가했다.', observations=[],
    )
    for claim_id, codes, role, sample, support, limit in CLAIMS:
        claim = dict(
            id=claim_id, source_id=SOURCE, role=role, standard_codes=codes,
            locations=[AUTHOR, PUBLISHER], support=support, does_not_establish=limit,
            independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        )
        if sample:
            claim['empirical_scope'] = analysis_scope(sample)
        registry['claims'].append(claim)
    queue['literature_review'].append(dict(
        source=entry, status='self_read_claim_mapping', evidence_file='data/literature_claim_reviews.json',
        claim_evidence_fields=['학교 배정과 분석 분모', '초등 1학년 효과와 척도', '국내 과제 적용 한계'],
        claim_ids=ids,
    ))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()


if __name__ == '__main__':
    main()

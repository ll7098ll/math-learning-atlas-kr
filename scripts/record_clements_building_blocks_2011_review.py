"""Register the 2011 Building Blocks trial and distinguish reported estimands."""
from math import sqrt

from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_ies_early_literature_review import PDF_URL as GUIDE


SOURCE = 'CLEMENTS_ET_AL_2011_BUILDING_BLOCKS'
DATE = '2026-11-09'
DOI = 'https://doi.org/10.5951/jresematheduc.42.2.0127'
AUTHOR = 'https://www.researchgate.net/publication/258933028_Mathematics_Learned_by_Young_Children_in_an_Intervention_Based_on_Learning_Trajectories_A_Large-Scale_Cluster_Randomized_Trial'
WWC = 'https://ies.ed.gov/ncee/WWC/Docs/InterventionReports/WWC_Building-Blocks_report.pdf'
WWC_SHA = '3cb8988573e6d2a3e1dbb80183a09038bb3aecf04a1d0440269849b4cf9caaa0'
CACHE = ROOT / 'tmp/literature/clements-2011-building-blocks'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
SCOPE = ('저자가 공개한 웹 본문에서 인쇄 127·130~132·134~138·141·144~151·154~156·160~161쪽의 관련 문단과 표를 대조했다. '
         '원논문 PDF와 판면은 미확보다. 2013 IES 가이드 표 D.2와 2023 WWC 보고서의 PDF 6~7쪽을 별도로 대조했다.')
LIMITS = ('두 미국 도시 학군의 유아 단계에서 교육과정·교사 연수·기술 지원을 함께 제공한 결과다. '
          '요소별 인과 효과, 국내 활동의 효과, 유치원·1학년 후속 지원의 효과는 이 비교에서 확인되지 않았다.')
EMPIRICAL = dict(
    design='school_cluster_randomized_block_trial',
    sample_description='42개 학교·106개 교실에서 유아 1,375명을 모집했고 사전·사후 점수가 있는 중재 927명과 대조 378명을 분석했다.',
    inference_limit=LIMITS, student_outcome_study=True, causal_effect_established=True, local_effect_tested=False,
)
SECTIONS = [
    ('연구 개요와 서지', 127, 127), ('학교 배정과 유아 단계 비교', 130, 132),
    ('정규 수업과 평가 도구', 134, 138), ('사후검사 탈락', 141, 141),
    ('총점·주제별 점수, 다층모형 및 교실 관찰', 144, 151),
    ('문항별 해석과 비교 조건', 154, 156), ('구성요소 해석의 한계', 160, 161),
]
SCORES = [
    ('REMA Rasch 총점', (18.54, 51.36, 17.25), (19.63, 44.01, 17.89), 0.48),
    ('수 원점수 합', (9.47, 29.71, 12.72), (10.26, 25.53, 13.20), 0.39),
    ('기하 원점수 합', (7.25, 14.34, 3.69), (7.65, 12.39, 3.71), 0.64),
]
CLAIMS = [
    ('BB2011-01', ['2수01-01', '2수03-03'], [f'{GUIDE}#page=79', f'{WWC}#page=7'],
     '학교를 세 조건으로 배정했으나 유아 단계에서 같은 교육을 받은 두 중재 조건을 합쳐 정규 수업과 비교했다. 모집 1,375명 중 70명이 탈락했고 사전·사후 자료가 있는 1,305명을 분석했다. 정규 수업에도 수학 활동이 있었다.',
     '개별 아동 배정이나 세 유아 프로그램 간 비교가 아니다. 같은 비교가 여러 가이드 표에 실려도 독립 연구 수는 하나다.'),
    ('BB2011-02', ['2수01-01', '2수01-03', '2수03-03'], [f'{GUIDE}#page=79', f'{WWC}#page=6'],
     '원논문은 사전 점수를 고려한 총점 다층모형의 효과크기를 0.72로 보고했다. 2013 가이드와 2023 WWC의 전체 점수 효과크기는 0.48이다. 원논문 표 3의 수·기하 원점수 합은 총점의 Rasch 척도와 구별한다.',
     '총점 효과크기를 특정 수 세기, 수 비교 또는 도형 찾기 과제의 효과크기로 사용할 수 없다. 공개 표로 한 근사 검산은 원자료 모형이나 WWC 코드 재현과 범위가 다르다.'),
    ('BB2011-03', ['2수01-01', '2수01-03', '2수01-04', '2수01-05'], [f'{GUIDE}#page=80'],
     '원논문의 주제별 기술통계에서 물체 세기와 수 비교·계열 결과를 분리했다. IES의 13개 하위척도 판정에서는 수의 합성과 산술의 효과가 뚜렷하지 않았다. 세기, 전체 개수 판단, 수 합성, 상황식 설명은 따로 관찰한다.',
     '유아의 작은 집합 과제 결과를 국내 네 자리 수 비교나 기호 계산의 성취로 확대할 수 없다. 뚜렷한 효과를 확인하지 못한 결과는 두 조건의 동등성을 입증하지 않는다.'),
    ('BB2011-04', ['2수03-03', '4수03-04', '4수03-10', '4수03-12'], [f'{GUIDE}#page=80'],
     '원논문은 도형 식별·구성과 도형 비교의 기술 결과를 구분했다. IES는 회전과 도형 비교에서 뚜렷한 효과를 확인하지 않았다. 원논문에서 모든 집단은 사후에 정사각형을 직사각형 예로 선택하는 빈도가 줄었다.',
     '도형 합성 결과로 회전 또는 포함 관계의 향상을 판단할 수 없다. 포함 관계는 국내 해당 학년의 필수 평가 항목으로 추가하지 않는다.'),
    ('BB2011-05', ['2수02-01', '2수03-06'], [f'{GUIDE}#page=80', f'{WWC}#page=6'],
     '원논문은 반복 단위 찾기 등을 포함한 패턴과 측정 주제의 원점수 기술통계를 따로 제시했다. 교실 관찰에서도 수학 활동 횟수와 활동에 쓴 시간을 다른 지표로 분석했다.',
     '주제 원점수나 교실 관찰로 특정 길이·들이·무게·넓이 과제 또는 패턴 발문의 인과 효과를 분리할 수 없다.'),
]


def approximate_effect(experimental, control):
    """Check the rounded guide values with the published group summaries."""
    n_exp, n_control = 927, 378
    pre_exp, post_exp, sd_exp = experimental
    pre_control, post_control, sd_control = control
    df = n_exp + n_control - 2
    pooled = sqrt(((n_exp - 1) * sd_exp ** 2 + (n_control - 1) * sd_control ** 2) / df)
    gain_difference = (post_exp - pre_exp) - (post_control - pre_control)
    return gain_difference / pooled * (1 - 3 / (4 * df - 1))


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert {row[0] for row in CLAIMS} == {c['id'] for c in registry['claims'] if c['source_id'] == SOURCE}
        build_report()
        return
    report = CACHE / 'wwc-building-blocks-2023.pdf'
    reader = PdfReader(report)
    assert sha(report) == WWC_SHA and len(reader.pages) == 9
    assert all(token in reader.pages[5].extract_text() for token in ('1,305', '0.48', '52.40', '44.01'))
    assert all(token in reader.pages[6].extract_text() for token in ('1,305', '106 classrooms', 'Without Reservations'))
    assert 1375 - 52 - 18 == 927 + 378 == 1305
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography = load(bibliography_path)
    queue = load(queue_path)
    assert all(row['id'] != SOURCE for row in bibliography)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    effects = []
    for outcome, exp, control, guide_effect in SCORES:
        effect = approximate_effect(exp, control)
        assert round(effect, 2) == guide_effect
        effects.append(dict(outcome=outcome, intervention=exp, comparison=control, guide_2013=guide_effect,
                            approximate_from_table_3=round(effect, 6)))
    text_scope = dict(url=AUTHOR, uploaded_by='Douglas H. Clements', article_pdf_obtained=False,
                      article_printed_pages=[127, 166], selected_sections=[
                          dict(section=label, printed_pages=[first, last]) for label, first, last in SECTIONS])
    notes = dict(
        source_id=SOURCE, source_url=DOI, source_asset_kind='author_web_text', author_text_review=text_scope,
        read_scope=SCOPE, date=DATE, reviewer='Codex', original_page_layout_review=False,
        contains_source_full_text=False, source_pdf_redistributed=False, empirical_scope=EMPIRICAL,
        reading_log=[
            '저자의 웹 본문에서 모집·배정과 탈락, 두 유아 중재 조건의 통합, 정규 수업에 포함된 수학을 확인했다.',
            'REMA 총점 추론 분석, 영역별 원점수 기술통계, 개별 문항에 관한 설명을 구별했다.',
            '2013 가이드 D.2와 2023 WWC의 결과를 비교했다. 2023년 표 4·5는 PDF 텍스트와 이미지를 모두 대조했다.',
        ],
        source_corrections=[
            dict(location='2013 가이드 참고문헌과 원논문 서지', issue='가이드에 126~177쪽으로 적힌 범위를 원논문 서지 127~166쪽과 구별했다.'),
            dict(location='원논문 표 3·4와 WWC 2023 표 4', issue='중재 집단 사후 평균 51.36과 WWC 표의 52.40, 그리고 0.72와 0.48을 각각 보고된 분석과 표에 귀속했다.'),
        ],
        flow=dict(schools=42, classrooms=106, enrolled=1375, attrition_by_arm=[52, 18],
                  analyzed_by_arm=[927, 378], classrooms_by_arm=[72, 34]),
        comparisons=dict(
            paper_multilevel_total_effect=0.72, report_2023_total_effect=0.48,
            report_2023_means=[52.40, 44.01],
            table_3_value_order=['사전 평균', '사후 평균', '사후 표준편차'], table_3_checks=effects,
            approximation='변화량 차이를 사후 합동 표준편차로 나누고 소표본 보정을 적용했다. 보고된 평균·표준편차만으로 한 근사 검산이다.',
            guide_no_discernible_subscales=['회전', '도형 비교', '산술', '수 합성'],
        ),
        supplementary_report=dict(url=WWC, sha256=WWC_SHA, pdf_pages=9, text_and_visual_pages=[6, 7],
                                  image_sha256={str(p): sha(CACHE / f'wwc-page-{p}.png') for p in (6, 7)}),
    )
    entry = dict(
        id=SOURCE, title='Mathematics Learned by Young Children in an Intervention Based on Learning Trajectories: A Large-Scale Cluster Randomized Trial',
        authors=['Douglas H. Clements', 'Julie Sarama', 'Mary Elaine Spitler', 'Alissa A. Lange', 'Christopher B. Wolfe'],
        year=2011, kind='학교 단위 유아 수학 무작위 비교 연구', url=DOI, review_scope=SCOPE, next_review=LIMITS,
        supports=['배정과 분석 표본', '총점과 세부 주제 결과의 차이', '원논문과 WWC의 분석별 수치'],
        does_not_establish=LIMITS,
    )
    path = ROOT / NOTES
    write(path, notes)
    bibliography.append(entry)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
        snapshot_kind='authored_review_notes', source_asset_kind='author_web_text', author_text_review=text_scope,
        snapshot_file=NOTES, snapshot_sha256=sha(path), redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=DOI, authors_year='Clements 외, 2011'),
        read_scope=SCOPE, scope_note='유아 단계의 중재 묶음 비교와 해당 평가에서 얻은 결과를 연결한다.',
        method_note='저자 공개 전사와 공식 WWC 보고서를 대조하고 세 개의 효과크기를 공개 기술통계로 근사 확인했다.',
        limits=LIMITS, empirical_scope=EMPIRICAL, independent_review=False, student_validated=False,
        editorial_action='문헌 대응 5건을 추가했다. 기존 관찰 과제의 범위는 유지했다.', observations=[],
    )
    for claim_id, codes, crosschecks, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=claim_id, source_id=SOURCE, role='empirical_result_with_scope', standard_codes=codes,
            locations=[AUTHOR, *crosschecks], support=support, does_not_establish=limit,
            empirical_scope=EMPIRICAL, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue['literature_review'].append(dict(
        source=entry, status='self_read_claim_mapping', evidence_file='data/literature_claim_reviews.json',
        claim_evidence_fields=['배정·탈락과 분석 단위', '총점과 주제 원점수', '효과크기와 적용 범위'],
        claim_ids=[row[0] for row in CLAIMS],
    ))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()


if __name__ == '__main__':
    main()

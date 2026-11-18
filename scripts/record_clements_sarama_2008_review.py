"""Register the 2008 Building Blocks trial with its three comparison conditions."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_clements_building_blocks_2011_review import CACHE as WWC_CACHE, WWC, WWC_SHA
from record_ies_early_literature_review import PDF_URL as GUIDE


SOURCE = 'CLEMENTS_SARAMA_2008_BUILDING_BLOCKS'
DATE = '2026-11-09'
DOI = 'https://doi.org/10.3102/0002831207312908'
WEB_PDF = 'https://scispace.com/pdf/experimental-evaluation-of-the-effects-of-a-research-based-27126df8zy.pdf'
PREK_2013 = 'https://ies.ed.gov/ncee/WWC/Docs/InterventionReports/wwc_prekmath_121713.pdf#page=9'
PREK_2023 = 'https://ies.ed.gov/ncee/wwc/Study/90773'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
SCOPE = ('53쪽으로 표시된 원논문의 웹 추출에서 인쇄 443·448·450·462~463·467~470·483~484·489쪽의 관련 문단과 표를 대조했다. '
         '원논문 PDF 파일과 판면은 미확보다. 2013 가이드 및 2013·2023년 WWC의 개입별 판정은 따로 대조했다.')
LIMITS = ('미국 뉴욕 유아 교실의 교육과정 묶음 비교다. 지도·교사 지원·자료가 함께 달랐고 개별 요소 효과와 국내 과제 효과는 확인되지 않았다. '
          '강화 수학 조건은 저소득층 교실에만 배정됐다.')
EMPIRICAL = dict(
    design='classroom_cluster_trial_with_two_assignment_strata',
    sample_description='초기 36교실에서 시작해 35교실 276명이 연구에 남았다. 사전·사후 완전 자료는 정규 101명, 강화 수학 51명, Building Blocks 101명이다.',
    inference_limit=LIMITS, student_outcome_study=True, causal_effect_established=True, local_effect_tested=False,
)
# Physical PDF pages and inclusive web extraction line ranges, limited to the reviewed excerpts.
EXCERPTS = [
    (2, 50, 53), (7, 206, 224), (9, 265, 293), (21, 699, 721), (22, 726, 730),
    (26, 892, 910), (27, 925, 956), (28, 968, 988), (29, 1000, 1007),
    (42, 1290, 1305), (43, 1309, 1323), (48, 1511, 1519),
]
CLAIMS = [
    ('BB2008-01', ['2수01-01', '2수01-05', '2수03-03'], [7, 9, 22, 27], [f'{WWC}#page=7', f'{GUIDE}#page=79'],
     '초기 저소득층 교실은 세 조건, 혼합 소득 교실은 Building Blocks와 정규 수업 두 조건에 배정했다. 원논문 세 조건 분석은 253명이고, WWC의 Building Blocks 대 정규 수업 비교는 각각 101명씩 202명이다. 강화 수학 조건에는 소집단 수업, 가정 활동, DLM 소프트웨어가 포함됐다.',
     '202명과 253명은 같은 연구에서 다른 조건을 포함한 수다. 정규 수업 교실의 교육과정은 하나로 통일되어 있지 않았다.'),
    ('BB2008-02', ['2수01-01', '2수01-05'], [27, 28, 29], [f'{WWC}#page=6', PREK_2013, PREK_2023],
     '원논문의 전체 수학 효과크기는 Building Blocks 대 정규 수업 1.07, 강화 수학 대 정규 수업 0.64, Building Blocks 대 강화 수학 0.47이다. 2023 WWC는 Building Blocks 대 정규 수업을 유보 없이 기준 충족으로 분류했다. Pre-K Mathematics의 별도 평가에서는 기준 미충족으로 분류했다.',
     '원논문의 세 비교와 WWC의 개입별 판정을 서로 바꿔 인용할 수 없다. 전체 수학 효과로 덧셈·뺄셈 상황이나 특정 소프트웨어의 효과를 따로 추정할 수 없다.'),
    ('BB2008-03', ['2수03-03', '4수03-04', '4수03-12'], [27, 42, 43], [],
     '도형 합성은 Building Blocks가 정규 수업보다 높았다. 강화 수학 조건과의 차이는 표 5에서 p<.10으로 표시됐고, 별도의 변환 한 문항에는 같은 유의 표시가 없다. 원논문은 일부 학생이 조각을 놓기 전에 방향을 돌려 맞춘 과정을 따로 기술했다.',
     '도형 합성 결과를 밀기·뒤집기·돌리기 전반의 효과로 확대하지 않는다. 훈련 활동과 비슷한 문항의 결과는 새로운 과제로의 전이와 구별한다.'),
    ('BB2008-04', ['2수02-01', '2수03-06'], [26, 27, 43], [],
     '반복 배열의 AB와 ABB 문항에서 기술 결과가 달랐다. 측정 하위척도의 차이는 작았고 원논문 설명에서는 정규 수업 집단의 향상 폭이 가장 컸다. 교실 수학 환경 관찰은 Building Blocks 대 정규 수업에서 차이가 있었고, 강화 수학 대비 사후 비교는 p=.06이었다.',
     '교실 환경 점수는 개별 학생의 측정·규칙 수행과 별개다. 배열별 기술 결과와 총점 비교를 동일한 검정 결과로 처리하지 않는다.'),
]


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert {row[0] for row in CLAIMS} == {row['id'] for row in registry['claims'] if row['source_id'] == SOURCE}
        build_report()
        return
    report = WWC_CACHE / 'wwc-building-blocks-2023.pdf'
    reader = PdfReader(report)
    assert sha(report) == WWC_SHA and len(reader.pages) == 9
    assert all(value in reader.pages[5].extract_text() for value in ('202 children', '61.78', '53.22', '1.07'))
    assert 101 + 51 + 101 == 253 and 101 + 101 == 202
    ranges = []
    start = 0
    for _, first, last in EXCERPTS:
        length = last - first + 1
        ranges.append([start, start + length - 1])
        start += length
    text_scope = dict(reported_pdf_pages=53, text_pdf_pages=[p for p, _, _ in EXCERPTS], visual_pdf_pages=[],
                      binary_obtained=False, text_line_count=start, page_text_line_ranges=ranges)
    notes = dict(
        source_id=SOURCE, source_url=DOI, source_asset_kind='web_pdf_text', source_pdf_url=WEB_PDF,
        date=DATE, reviewer='Codex', read_scope=SCOPE, pdf_text_review=text_scope,
        original_page_layout_review=False, contains_source_full_text=False, source_pdf_redistributed=False,
        empirical_scope=EMPIRICAL, publication='American Educational Research Journal, 45(2), 443–494',
        web_excerpt_ranges=[dict(pdf_page=p, source_lines=[first, last]) for p, first, last in EXCERPTS],
        reading_log=[
            '웹 추출에서 양 소득 집단의 배정 범위, 탈락, 정규 수업과 두 중재의 세부 구성을 확인했다.',
            '표 5의 집단별 인원과 사후 평균, 표 6의 다층모형과 대안 표준화 값, COEMET 관찰을 구별했다.',
            'WWC 2023 Building Blocks 보고서 PDF 6~7쪽의 표 4·5와 Pre-K Mathematics 2013·2023 판정을 각각 대조했다.',
        ],
        source_corrections=[
            dict(location='원논문 표 5와 2023 WWC 표 4', issue='중재 사후 평균은 원논문 59.39, WWC 표 61.78이다. 정규 수업 53.22는 일치한다. 공개 표의 차이를 같은 원평균으로 옮기지 않았다.'),
            dict(location='원논문 450쪽과 WWC 개입별 비교', issue='정규 수업에 여러 자료가 쓰였다. 강화 수학은 PMC 수업과 가정 활동, DLM 소프트웨어를 포함했다. 기준 충족 판정은 해당 비교에 귀속했다.'),
        ],
        assignment=dict(initial_classrooms=36, retained_classrooms=35, retained_children=276,
                        low_income_classrooms=24, mixed_income_classrooms=12, analyzed_children=[101, 51, 101],
                        analyzed_arm_order=['정규 수업', '강화 수학', 'Building Blocks']),
        achievement=dict(original_total_effects=[1.07, 0.64, 0.47], alternative_standardization=[1.09, 0.60, 0.54],
                         comparison_order=['Building Blocks 대 정규', '강화 수학 대 정규', 'Building Blocks 대 강화 수학'],
                         original_posttest_means=[53.22, 53.77, 59.39], wwc_posttest_means=[53.22, 61.78],
                         wwc_students=202),
        wwc_reviews=[
            dict(url=f'{WWC}#page=7', scope='2023 Building Blocks 대 정규 수업', rating='유보 없이 충족'),
            dict(url=PREK_2013, scope='2013 Pre-K Mathematics with DLM', rating='기준 미충족',
                 reason='해당 분석 조건의 배정 또는 배정 후 배치와 동등성 요건'),
            dict(url=PREK_2023, scope='2023 Pre-K Mathematics', rating='기준 미충족',
                 reason='효과를 해당 개입에만 귀속할 수 없다고 평가'),
        ],
        supplementary_report=dict(url=WWC, sha256=WWC_SHA, text_and_visual_pages=[6, 7]),
    )
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography = load(bibliography_path)
    queue = load(queue_path)
    assert all(row['id'] != SOURCE for row in bibliography)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    entry = dict(id=SOURCE, title='Experimental Evaluation of the Effects of a Research-Based Preschool Mathematics Curriculum',
                 authors=['Douglas H. Clements', 'Julie Sarama'], year=2008, kind='유아 수학 교육과정의 세 조건 비교 연구',
                 url=DOI, review_scope=SCOPE, next_review=LIMITS,
                 supports=['정규 수업과 강화 수학 비교의 구별', '분석별 표본과 효과크기', '도형 합성과 변환 평가의 구별'],
                 does_not_establish=LIMITS)
    snapshot = ROOT / NOTES
    write(snapshot, notes)
    bibliography.append(entry)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
        snapshot_kind='authored_review_notes', source_asset_kind='web_pdf_text', pdf_text_review=text_scope,
        snapshot_file=NOTES, snapshot_sha256=sha(snapshot), redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=DOI, authors_year='Clements·Sarama, 2008'),
        read_scope=SCOPE, empirical_scope=EMPIRICAL, limits=LIMITS,
        scope_note='교실 수준의 배정과 아동 자료의 분석 분모, 비교별 평정을 구별한다.',
        method_note='원논문 웹 추출의 문단·표와 WWC 개입 보고를 대조했다.',
        editorial_action='원연구 근거 4건을 추가했다. 기존 관찰 과제의 범위는 유지했다.',
        independent_review=False, student_validated=False, observations=[],
    )
    for claim_id, codes, pages, references, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=claim_id, source_id=SOURCE, role='empirical_result_with_scope', standard_codes=codes,
            locations=[*(f'{WEB_PDF}#page={p}' for p in pages), *references], support=support,
            does_not_establish=limit, empirical_scope=EMPIRICAL, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue['literature_review'].append(dict(
        source=entry, status='self_read_claim_mapping', evidence_file='data/literature_claim_reviews.json',
        claim_evidence_fields=['배정 범위·분모', '비교별 효과크기와 평정', '총점·관찰과 세부 과제'],
        claim_ids=[row[0] for row in CLAIMS],
    ))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()


if __name__ == '__main__':
    main()

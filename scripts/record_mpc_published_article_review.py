"""Record a journal reanalysis without counting it as another experiment."""
from extend_lt2_length_assets_review import load, sha, write
from extend_mpc_preregistration_review import DATE, NOTE as REPORT_NOTE, report_links
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_making_pre_k_count_review import FAMILY, GRADE_3
from relation_literature_review import apply_literature_context


SID = 'MATTERA_ET_AL_2026_MPC_PUBLISHED'
DOI = 'https://doi.org/10.1080/19345747.2025.2509234'
WEB_PDF = 'https://www.tandfonline.com/doi/pdf/10.1080/19345747.2025.2509234'
NOTE = f'data/literature_evidence/{SID}_review_notes.json'
COLLECTION, TESTING, EARLY = '12실통02-02', '12실통03-04', '2수01-05'
SCOPE = '출판사 PDF에서 추출된 439·443~448·455쪽의 선정 본문과 표 2·4·5를 2021년 보고서 및 사전등록과 대조했다.'
LIMIT = '동일한 MPC 연구의 출판 분석이다. 보고서와 독립 표본으로 합산하지 않는다. 부록 파일과 원자료·코드, 자체 과제의 학생 반응은 확인 범위 밖이다.'
EMPIRICAL = dict(design='취학 전 기관을 배정한 Making Pre-K Count 연구의 취학 전 및 초등 3학년 출판 분석.',
                 sample_description='동의 표본 2,715명, 취학 전 평가 1,389명, 3학년 수학 분석 1,844명.',
                 inference_limit=LIMIT, student_outcome_study=True, causal_effect_established=False,
                 local_effect_tested=False, study_family=FAMILY)
# PDF page numbers include the publisher's cover sheet.
EXCERPTS = [(9, 357, 397), (13, 622, 645), (14, 733, 774), (15, 780, 821),
            (16, 823, 923), (17, 1093, 1144), (18, 1149, 1289), (25, 1569, 1595)]
CLAIMS = [
    ('MPCJ-01', [COLLECTION], [9, 14], report_links(25, 53),
     '논문은 동의자 2,715명, 취학 전 직접 평가 1,389명, 3학년 수학 1,844명을 제시했다. 2021년 보고서는 동의자 2,717명 가운데 연령까지 충족한 2,702명과 결과가 하나라도 있는 2,277명을 따로 제시했다.',
     '분모의 정의를 자료별로 보존한다. 동의자 수 차이의 원인을 공개 집계만으로 확정할 수 없다.'),
    ('MPCJ-02', [TESTING], [13, 14, 16, 17], report_links(32, 65, 66),
     '논문은 아동·학급·기관의 3수준을, 2021년 보고서의 주 분석은 아동·기관의 2수준과 배정 블록 지표를 사용했다. 3학년 수학은 두 자료 모두 945명 대 899명과 효과 크기 .10을 제시한다. p값은 논문 .18, 보고서 .19다.',
     '논문 표 4는 모형이 다름을 밝힌다. 같은 비교의 두 사양으로 기록하고, 반올림된 표만으로 p값 차이의 산출 과정을 재현할 수 없다.'),
    ('MPCJ-03', [COLLECTION, TESTING], [14, 25], report_links(65, 68),
     '논문은 관측 정보에 조건부로 결측이 무작위라고 가정해 기초 공변량을 50개 자료에서 대치하고 추정과 불확실성을 결합했다. 결과변수는 대치하지 않았다고 명시했다. 연구의 원자료와 코드는 공개하지 않았다고 밝혔다.',
     '50개 자료를 50번의 별도 관찰이나 실험으로 세지 않는다. 논문의 처리 설명으로 2021년 보고서에 대한 WWC의 세부 판정 사유를 확정하지 않는다.'),
    ('MPCJ-04', [TESTING], [15, 18], [],
     '논문 표 5의 3학년 수학 효과 크기는 낮은 억제 조절 집단 .36, 높은 집단 .14다. 낮은 집단의 효과에는 유의 표기가 있고, 두 집단 효과 차이 .22에는 유의 표기가 없다. 문해 결과의 집단 간 차이에는 별도 표기가 있다.',
     '집단 내 효과와 집단 간 효과 차이는 서로 다른 검정이다. 한 집단의 p값만으로 집단 간 차이를 판정하지 않는다.'),
    ('MPCJ-05', [EARLY], [16], [],
     '취학 전 전체 분석의 ECLS-B 수학과 WJ 응용문제 효과 크기는 각각 .03이다. 두 검사 모두 전체 수학 결과에서 유의한 차이가 보고되지 않았다.',
     '검사 전체 점수의 결과로 덧셈 문항에서 아동이 쓴 전략이나 개별 활동의 효과를 판정하지 않는다.'),
]
OBSERVATIONS = [
    dict(id='MPCJ-P1', standard_codes=[COLLECTION], question='가상 연구에서 동의한 240명 중 취학 전 검사에 130명, 3학년 수학에 170명이 포함됐다. 두 시점에 모두 참여한 인원이 170명인지 설명하라.',
         expected='두 시점의 참여자는 130명과 170명이다. 교집합은 70명 이상 130명 이하이고 정확한 인원은 개인 연결 자료가 필요하다.',
         interpretation='같은 240명 모집 집단이라는 조건에서 합집합과 교집합을 확인한다. 시점별 표본 크기로 같은 학생을 추정하는지 기록한다.', student_validated=False),
    dict(id='MPCJ-P2', standard_codes=[TESTING], question='같은 자료의 가상 모형 A와 B에서 효과 크기가 모두 .10이고 p값은 .18과 .19다. 유의수준 5%에서 각각 판단하고 두 연구가 재현된 것인지 설명하라.',
         expected='두 분석 모두 귀무가설을 기각하지 않는다. 같은 자료를 분석한 두 사양이다. 반올림된 효과 크기가 같아도 표준오차나 모형의 가정이 다를 수 있다.',
         interpretation='효과의 크기, 검정 결과, 데이터 공유 여부를 각각 기록한다.', student_validated=False),
    dict(id='MPCJ-P3', standard_codes=[COLLECTION, TESTING], question='가상 연구가 결측 기초 점수를 대치한 자료 50개에서 결과를 각각 계산하고 결합했다. 50개가 서로 다른 참여자 집단인지, 대치의 불확실성을 어떻게 고려할지 설명하라.',
         expected='같은 참여 자료의 빠진 기초 점수에 대해 여러 가능한 값을 넣은 자료다. 각 자료 안의 추정 오차와 자료 사이의 추정 차이를 함께 고려한다.',
         interpretation='관찰 자료와 대치값, 대치 대상과 결과변수, 추정의 두 불확실성 성분을 구별한다.', student_validated=False),
    dict(id='MPCJ-P4', standard_codes=[TESTING], question='가상 결과에서 A집단 효과 검정 p=.01, B집단 p=.22, A와 B의 효과 차이 검정 p=.16이다. 5% 기준으로 어떤 차이를 확인할 수 있는가?',
         expected='A집단 안의 효과 0 가설만 기각한다. B집단 효과 0 가설과 두 효과가 같다는 가설은 각각 기각하지 않는다.',
         interpretation='집단별 검정과 두 효과의 차이 검정을 구별하는지 기록한다.', student_validated=False),
]


def main():
    registry = load_registry()
    if SID in registry['sources']:
        build_report()
        return
    report = registry['sources'][GRADE_3['id']]
    assert report['snapshot_file'] == REPORT_NOTE and sha(ROOT / REPORT_NOTE) == report['snapshot_sha256']
    prior = load(ROOT / REPORT_NOTE)
    assert prior['preregistration_review']['samples']['math_group_counts'][0] == [945, 899]
    assert prior['appendices_review']['p_by_source'] == {'report': .19, 'journal': .18}
    ranges, next_line = [], 0
    for _, first, last in EXCERPTS:
        end = next_line + last - first
        ranges.append([next_line, end])
        next_line = end + 1
    text_scope = dict(reported_pdf_pages=29, text_pdf_pages=[p for p, _, _ in EXCERPTS], visual_pdf_pages=[],
                      binary_obtained=False, text_line_count=next_line, page_text_line_ranges=ranges)
    notes = dict(source_id=SID, source_url=DOI, source_pdf_url=WEB_PDF, source_asset_kind='web_pdf_text',
                 date=DATE, reviewer='Codex', read_scope=SCOPE, pdf_text_review=text_scope, empirical_scope=EMPIRICAL,
                 original_page_layout_review=False, contains_source_full_text=False, source_pdf_redistributed=False,
                 publication=dict(volume=19, issue=2, printed_pages=[432, 459], online_date='2025-07-15', issue_year=2026),
                 web_excerpt_ranges=[dict(pdf_page=p, source_lines=[first, last]) for p, first, last in EXCERPTS],
                 reading_log=['출판사 PDF 추출의 분모·모형·대치 절차·검정 결과와 2021년 보고서를 대조했다.'],
                 source_corrections=[dict(location='439쪽·표 4·표 5', issue='동의 분모, 효과의 p값, 집단 간 차이 검정을 구별한다.')],
                 companion_report=dict(source_id=GRADE_3['id'], snapshot_file=REPORT_NOTE, sha256=report['snapshot_sha256']),
                 sample=dict(journal_consented=2715, report_consented=2717, report_eligible=2702, report_any_outcome=2277,
                             journal_pre_k=1389, grade_3_math_groups=[945, 899], grade_3_math=1844, retained_high5s=226),
                 model=dict(journal_levels=['child', 'classroom', 'pre_k_site'], report_levels=['child', 'pre_k_site'],
                            journal_baseline_imputations=50, journal_assumption='missing_at_random', journal_outcomes_imputed=False),
                 results=dict(pre_k_math_effects=[.03, .03], grade_3_math_effect=.10, journal_p=.18, report_p=.19,
                              low_high_inhibitory_math=[.36, .14], math_contrast=.22, math_contrast_significance_marker=False),
                 supplemental_workbook_verified=False, participant_data_public=False, analysis_code_public=False)
    bibliography = load(ROOT / 'data/sources.json')
    queue = load(ROOT / 'data/content_review_queue.json')
    entry = dict(id=SID, year=2026, url=DOI, title='The Impact of Making PreK Count on Short and Longer-Term Outcomes',
                 authors=['Shira Mattera', 'Robin Jacob', 'Pamela Morris-Perez', 'Catherine Asher'],
                 kind='MPC 동일 연구의 취학 전·3학년 출판 분석', review_scope=SCOPE, does_not_establish=LIMIT,
                 next_review='출판사 부록 파일을 확보해 두 시점에 공통으로 관찰된 표본과 민감도 분석을 대조한다.',
                 supports=['시점별 분모', '다층 모형과 결측 처리', '하위집단 효과와 집단 간 차이'])
    assert all(row['id'] != SID for row in bibliography)
    assert all(row['source']['id'] != SID for row in queue['literature_review'])
    bibliography.append(entry)
    write(ROOT / NOTE, notes)
    registry['sources'][SID] = dict(source_id=SID, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
        snapshot_kind='authored_review_notes', source_asset_kind='web_pdf_text', pdf_text_review=text_scope,
        snapshot_file=NOTE, snapshot_sha256=sha(ROOT / NOTE), redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=DOI, authors_year='Mattera 외, 2026'),
        read_scope=SCOPE, empirical_scope=EMPIRICAL, limits=LIMIT, scope_note='같은 연구의 분석 사양을 출처별로 비교한다.',
        method_note='출판사 PDF 추출문과 2021년 보고서의 표 및 사전등록 대조 기록을 확인했다.',
        editorial_action='문헌 근거 5건과 자체 관찰 과제 4개를 추가했다.',
        independent_review=False, student_validated=False, observations=OBSERVATIONS)
    for cid, codes, pages, references, support, limit in CLAIMS:
        registry['claims'].append(dict(id=cid, source_id=SID, role='empirical_result_with_scope', empirical_scope=EMPIRICAL,
            standard_codes=codes, locations=[*(f'{WEB_PDF}#page={p}' for p in pages), *references], support=support,
            does_not_establish=limit, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes}))
    queue['literature_review'].append(dict(source=entry, status='self_read_claim_mapping',
        evidence_file='data/literature_claim_reviews.json', claim_evidence_fields=entry['supports'],
        claim_ids=[row[0] for row in CLAIMS]))
    relations = load(ROOT / 'data/revised_relations.json')['relations']
    assert not {(r['id'], cid) for r in relations for cid, codes, *_ in CLAIMS
                if all(r[k].startswith('standard:') for k in ('from', 'to'))
                and {r[k][9:] for k in ('from', 'to')} <= set(codes)}
    apply_literature_context(relations, registry)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    build_report()
    print('MPC journal analysis: 1 source, 5 claims, 4 observation tasks')


if __name__ == '__main__':
    main()

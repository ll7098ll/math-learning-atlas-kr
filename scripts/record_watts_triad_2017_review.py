"""Register the TRIAD reanalysis with separate measurement and model scopes."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value


SOURCE = 'WATTS_ET_AL_2017_TRIAD_STATE_TRAIT'
DOI = 'https://doi.org/10.1080/19345747.2016.1204640'
PMC = 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5791897/'
UCI = 'https://bpb-us-e2.wpmucdn.com/faculty.sites.uci.edu/dist/7/112/files/2011/03/Watts-Does-Early-Mathematics-Intervention-Change-the-Processes-Underlying-Children-s-Learning.pdf'
AUTHOR = 'https://tylerwatts.org/wp-content/uploads/2016/10/watts-et-al-in-press-jree.pdf'
CACHE = ROOT / 'tmp/literature/clements-triad-followthrough'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
PDF_SHA = '748f7ddd16f57119e546bb8af35aa2cea0cf3bdcf9140e7a72cce97218411cc2'
AUTHOR_SHA = 'c240900054fb44fe71b8c0780d778c6db776b47cdf1f0bc4604feda369ea057c'
TEXT_PAGES = [1, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 29, 30, 31, 32, 40, 41, 42, 43]
VISUAL_PAGES = [15, 25, 26, 40, 42, 43]
AUTHOR_TEXT_PAGES = [1, 2, 13, 14, 15, 20, 21, 37, 38, 39, 40]
AUTHOR_VISUAL_PAGES = [14, 39, 40]
SCOPE = ('UC Irvine에 공개된 수락 원고의 표본·평가·모형·한계 관련 문단과 표 1~3·그림 1을 읽었다. '
         '제1저자 사이트의 출판 전 원고 및 PMC HTML에서 표본과 모형 수치를 교차 확인했다. '
         '별도 보충 문서와 출판사 권호 판면은 미확보다.')
LIMIT = ('같은 TRIAD 코호트 중 취학 전 중재만 받은 집단과 대조군을 재분석했다. '
         '모형의 총점 경로로 국내 개별 과제의 전이, 고정된 발달 단계 또는 필수 선수관계를 확인할 수 없다.')
EMPIRICAL = dict(
    design='latent_state_trait_reanalysis_of_school_cluster_trial',
    sample_description='후속 지원군을 제외한 30개 학교 880명 중 수학 결과가 한 번 이상 있는 834명을 분석했다.',
    inference_limit=LIMIT, student_outcome_study=True, causal_effect_established=False, local_effect_tested=False,
)
CLAIMS = [
    ('BBW-01', ['2수01-01', '2수01-05', '2수03-03'], [13, 14, 15, 40, 42], [f'{PMC}#T1'],
     '같은 TRIAD 자료에서 후속 지원군을 제외한 30개 학교의 880명 중 수학 결과가 한 번 이상 있는 834명을 분석했다. 표 1과 표 3의 중재 456명과 대조 378명은 전체 분석 인원과 합계가 맞는다.',
     '본문에는 중재 465명으로도 적혀 있다. 이 분석은 후속 지원군의 효과나 원연구의 독립 재현을 보여 주지 않는다.'),
    ('BBW-02', ['2수01-01', '2수01-05', '2수03-03', '2수03-06'], [16, 17, 21, 31], [],
     '취학 전부터 초등 1학년 봄까지 개별 면담형 REMA를 썼고, 초등 4학년 가을에는 별도의 객관식 TEAM 3–5를 썼다. 4학년 자료의 전체 탈락률은 44%였다.',
     '두 도구의 과제·문항 범위가 다르다. 총점 추적을 같은 세기·측정·도형 과제를 반복해 얻은 변화로 읽을 수 없다.'),
    ('BBW-03', ['2수01-04', '2수01-05', '2수03-03'], [19, 22, 23, 43], [f'{PMC}#F1', f'{AUTHOR}#page=40'],
     '전체 표본 모형에서 취학 전 중재와 첫 시점의 상태 성분 사이 경로는 .53(p<.001)이었다. 여러 시점에서 공통인 잠재 특성 성분으로의 경로는 −.04(p=.59)였으며 뚜렷한 차이가 확인되지 않았다.',
     '상태와 특성은 이 자료에서 추정한 모형 성분이다. −.04의 비유의 결과로 효과가 정확히 0이라고 결론 내리거나 학습자의 능력을 고정할 수 없다.'),
    ('BBW-04', ['2수01-04', '2수01-05', '2수03-06'], [25, 26, 42], [f'{PMC}#T3', f'{AUTHOR}#page=39'],
     '표 3에서 취학 전 사후부터 유치원까지의 상태 경로는 중재 .30, 대조 .08이었다. 연구는 중재 직후 전이 가능성을 해석했다. 표의 모형 1·2는 중재·대조이고 3·4는 사전 점수 중앙값 기준 집단이다.',
     '본문에서 표의 모형 번호를 반대로 소개한다. 집단별 유의 표기나 모형 전체의 적합도 차이로 특정 경로의 집단 간 차이를 검정했다고 볼 수 없다.'),
]


def pdf_review(filename, url, expected_hash, page_count, text_pages, visual_pages, image_prefix):
    path = CACHE / filename
    assert sha(path) == expected_hash
    reader = PdfReader(path)
    assert len(reader.pages) == page_count
    return reader, dict(
        url=url, sha256=expected_hash, pdf_pages=page_count, selected_text_pages=text_pages,
        visual_pdf_pages=visual_pages,
        rendered_page_sha256={str(p): sha(CACHE / f'{image_prefix}-{p}.png') for p in visual_pages},
    )


def main():
    registry = load_registry()
    ids = [claim[0] for claim in CLAIMS]
    if SOURCE in registry['sources']:
        assert set(ids) == {claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE}
        build_report()
        return
    uci, primary = pdf_review('watts-processes-author.pdf', UCI, PDF_SHA, 43, TEXT_PAGES, VISUAL_PAGES, 'watts-processes-page')
    author, in_press = pdf_review('watts-in-press-author.pdf', AUTHOR, AUTHOR_SHA, 40, AUTHOR_TEXT_PAGES,
                                  AUTHOR_VISUAL_PAGES, 'watts-in-press-page')
    for reader, method, table, subgroup in ((uci, 15, 40, 42), (author, 14, 37, 39)):
        assert all(token in reader.pages[method - 1].extract_text() for token in ('834', '465', '378'))
        assert all(token in reader.pages[table - 1].extract_text() for token in ('456', '378'))
        assert all(token in reader.pages[subgroup - 1].extract_text() for token in ('456', '378', '416', '418'))
    assert 456 + 378 == 416 + 418 == 834
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography, queue = load(bibliography_path), load(queue_path)
    assert all(row['id'] != SOURCE for row in bibliography)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    notes = dict(
        source_id=SOURCE, source_url=DOI, date='2026-11-09', reviewer='Codex',
        source_asset_kind='pdf', source_pdf_sha256=PDF_SHA, source_pdf_redistributed=False,
        contains_source_full_text=False, read_scope=SCOPE, empirical_scope=EMPIRICAL,
        source_pdf_review=primary, in_press_pdf_review=in_press, pmc=PMC, journal_issue_pages=[96, 115],
        same_cohort_as='CLEMENTS_ET_AL_2011_BUILDING_BLOCKS', included_conditions=['NFT', 'control'],
        sample=dict(schools=30, recruited_in_included_schools=880, analyzed=834, tables_counts=[456, 378],
                    method_prose_counts=[465, 378], missing_outcomes_percent=[7, 14, 44]),
        model=dict(
            waves=['취학 전 사후', '유치원 봄', '1학년 봄', '4학년 가을'], instruments=['REMA', 'REMA', 'REMA', 'TEAM 3–5'],
            intervention_to_state1=dict(beta=.53, p='<.001'), intervention_to_trait=dict(beta=-.04, p=.59),
            consecutive_state_paths=[.25, .04, .13], consecutive_state_p=['<.001', '.24', '<.01'],
            table_3_models=['중재', '대조', '사전 점수 높은 집단', '사전 점수 낮은 집단'],
            first_state_path_by_condition=[.30, .08], treatment_control_joint_constraint_test=dict(df=21, chi_square=187.21, p='<.001'),
        ),
        reading_log=[
            '수락 원고와 출판 전 원고의 표본 분모·시점·표 번호를 본문·표·그림별로 대조했다.',
            '중재에서 상태와 잠재 특성으로 향하는 표준화 경로, 시점 간 경로, 집단별 모형 비교를 구분했다.',
            '원고에 링크된 별도 보충 문서와 출판사 권호 판면은 확인하지 못했다.',
        ],
        source_corrections=[
            dict(location='수락 원고 PDF 15·40·42쪽과 출판 전 원고 PDF 14·37·39쪽',
                 issue='본문 중재 465명은 대조 378명과 합하면 843명이다. 두 표의 456명과 378명은 전체 834명과 일치한다.'),
            dict(location='표 3 열 머리와 본문 하위 집단 분석',
                 issue='본문에서 모형 1·2와 3·4의 설명을 서로 바꿔 적었다. 계수의 집단 귀속은 표 머리와 본문에 제시된 수치를 함께 대조했다.'),
            dict(location='모형 방법의 측정 시점과 그림 1',
                 issue='모형 방법은 네 시점을 연말 측정으로 소개하지만, 4학년 TEAM 3–5는 방법·그림에 가을로 표시된다.'),
        ],
    )
    entry = dict(
        id=SOURCE, year=2017, url=DOI, kind='무작위 비교 자료의 종단 잠재변수 모형 재분석',
        title='Does Early Mathematics Intervention Change the Processes Underlying Children’s Learning?',
        authors=['Tyler W. Watts', 'Douglas H. Clements', 'Julie Sarama', 'Christopher B. Wolfe', 'Mary Elaine Spitler', 'Drew H. Bailey'],
        review_scope=SCOPE, does_not_establish=LIMIT,
        next_review='별도 보충 문서의 후속 지원군 제외 근거와 모형 제약, 출판사 권호 판면을 확인한다.',
        supports=['재분석 대상과 도구의 변화', '상태와 특성 모형의 구별', '표 3 경로 해석의 범위'],
    )
    snapshot = ROOT / NOTES
    write(snapshot, notes)
    bibliography.append(entry)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=notes['date'],
        snapshot_kind='authored_review_notes', source_asset_kind='pdf', source_pdf_sha256=PDF_SHA,
        snapshot_file=NOTES, snapshot_sha256=sha(snapshot), redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=DOI, authors_year='Watts 외, 2017'),
        read_scope=SCOPE, scope_note='같은 코호트의 두 조건을 대상으로 한 종단 모형 재분석이다.',
        method_note='수락 원고와 제1저자 공개 출판 전 원고의 본문·표·그림, PMC 공개 본문을 대조했다.',
        limits=LIMIT, empirical_scope=EMPIRICAL, independent_review=False, student_validated=False,
        editorial_action='문헌 대응 4건을 추가했다.', observations=[],
    )
    for claim_id, codes, pages, links, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=claim_id, source_id=SOURCE, role='empirical_result_with_scope', standard_codes=codes,
            locations=[*(f'{UCI}#page={p}' for p in pages), *links], support=support, does_not_establish=limit,
            empirical_scope=EMPIRICAL, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue['literature_review'].append(dict(
        source=entry, status='self_read_claim_mapping', evidence_file='data/literature_claim_reviews.json',
        claim_evidence_fields=['재분석 표본과 측정 시점', '모형 계수와 비교 범위', '과제 적용 한계'], claim_ids=ids,
    ))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()


if __name__ == '__main__':
    main()

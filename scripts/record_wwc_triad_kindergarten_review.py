"""Register the WWC kindergarten review and separate its published estimates."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_clements_triad_2013_review import AUTHOR as FIRST_GRADE_TEXT, KINDERGARTEN as STUDY_ABSTRACT


SOURCE = 'WWC_2014_TRIAD_KINDERGARTEN'
URL = 'https://ies.ed.gov/ncee/wwc/Docs/SingleStudyReviews/wwc_sarama_070114.pdf'
ONLINE = 'https://ies.ed.gov/ncee/wwc/study/79014'
STUDY_DOI = 'https://doi.org/10.1080/19345747.2011.627980'
CACHE = ROOT / 'tmp/literature/clements-triad-followthrough'
PDF_SHA = '67f8cfb87bdb750aac97cc2f675871e95186e75379bfabb2bd9309306f401960'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
TEXT_PAGES = list(range(1, 9))
VISUAL_PAGES = [2, 6, 7]
SCOPE = ('2014년 WWC 단일 연구 평가 PDF의 8쪽 텍스트와 2·6·7쪽 판면, '
         'WWC 사이트의 2014년·2018년 심사, Sarama 외 2012년 논문의 기관 서지 초록을 대조했다. '
         '2012년 원논문 본문과 표의 판면은 미확보다.')
LIMIT = ('같은 미국 TRIAD 코호트의 유치원 말 REMA 총점에 관한 심사다. '
         '탈락 관련 유보가 있으며 개별 수학 과제와 국내 성취기준에 대한 효과는 확인할 수 없다.')
EMPIRICAL = dict(
    design='school_cluster_randomized_followup_with_wwc_reservations',
    sample_description='42개 학교의 963명을 포함한 유치원 말 분석이다. 두 조건씩 비교한 표본은 630명, 618명, 678명이다.',
    inference_limit=LIMIT, student_outcome_study=True, causal_effect_established=False, local_effect_tested=False,
)
COMPARISONS = [
    dict(contrast='FT vs control', schools=28, children=630, significant=True,
         pdf_2014_means=[53.47, 51.61], pdf_2014_effect_size=.40, pdf_2014_improvement_index=15,
         online_2014_means=[53.47, 51.61], online_2014_improvement_index=16,
         online_2018_means=[53.22, 51.61], online_2018_improvement_index=13),
    dict(contrast='NFT vs control', schools=30, children=618, significant=True, pdf_2014_p=.03,
         pdf_2014_means=[52.64, 51.61], pdf_2014_effect_size=None, pdf_2014_improvement_index=None,
         online_2014_improvement_index=9, online_2018_improvement_index=9),
    dict(contrast='FT vs NFT', schools=26, children=678, significant=False, pdf_2014_p=.13,
         pdf_2014_means=[53.22, 52.64], pdf_2014_effect_size=None, pdf_2014_improvement_index=None),
]
CLAIMS = [
    ('BBK-01', ['2수01-01', '2수01-04', '2수01-05'], 'related_theoretical_context', [1, 3, 4], [ONLINE],
     '취학 전 두 중재군은 같은 Building Blocks 교육과정을 사용했다. 유치원 후속 지원군은 학군 교육과정에 형성평가 중심 교사 연수와 학습경로 도구를 더했다. 교사 연수는 일곱 회에 걸쳐 32시간을 제공했고 평균 참석률은 63%였다.',
     '유치원에서 Building Blocks 교육과정 전체를 다시 사용한 비교로 해석할 수 없다. 연수, 도구, 과제 중 어느 하나의 독립적인 효과는 구분되지 않는다.'),
    ('BBK-02', ['2수01-01', '2수01-05', '2수03-03'], 'empirical_result_with_scope', [2, 3, 5, 6], [ONLINE],
     'WWC 유치원 말 REMA 총점에서 후속 지원군 대 정규 수업군 630명, 취학 전 중재만 대 정규 수업군 618명은 모두 유의한 차이가 있었다. 후속 지원군 대 취학 전 중재만 678명에서는 차이가 뚜렷하지 않았다(p=.13).',
     '963명의 표본에서 비교군을 공유하므로 세 분모를 합산하지 않는다. 직접 비교의 비유의 결과로 두 조건의 동등성을 입증할 수 없다.'),
    ('BBK-03', ['2수01-05', '2수03-03'], 'empirical_result_with_scope', [6], [ONLINE],
     '2014년 PDF 부록 C는 후속 지원군 대 정규 수업군에 조정 평균 53.47·51.61과 효과크기 .40을 보고했다. 2018년 온라인 심사는 같은 비교에서 53.22·51.61을 표시한다. 2014년 PDF는 다른 두 비교의 계산 행에서 효과크기를 미보고로 표기했다.',
     'PDF의 두 중재군 영역 요약 행에 반복된 .40은 해당 비교 계산 행과 주석의 미보고 설명에 어긋난다. 근거가 확인되는 후속 지원군 대 정규 수업군에만 .40을 귀속한다.'),
    ('BBK-04', ['2수01-01', '2수01-05'], 'empirical_result_with_scope', [2, 6, 7], [ONLINE, STUDY_ABSTRACT, FIRST_GRADE_TEXT],
     '2012년 초록과 WWC는 유치원 말 두 중재군이 각각 정규 수업군보다 높았다고 보고했다. 2013년 후속 논문의 유치원 회고는 후속 지원군만 유의하다고 적었다. WWC의 2014년 PDF는 탈락 정보 미확보를, 2018년 온라인 심사는 높은 탈락률을 유보 사유로 적었다.',
     '심사와 원논문의 표현을 같은 분석으로 가정하지 않는다. 2012년 원논문 표가 확보되기 전까지 회고의 유의 판정 차이가 생긴 원인을 확정하지 않는다.'),
]


def main():
    registry = load_registry()
    ids = [claim[0] for claim in CLAIMS]
    if SOURCE in registry['sources']:
        assert set(ids) == {claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE}
        build_report()
        return
    path = CACHE / 'wwc-kindergarten-2014.pdf'
    assert sha(path) == PDF_SHA
    reader = PdfReader(path)
    assert len(reader.pages) == len(TEXT_PAGES)
    table = ' '.join(reader.pages[5].extract_text().split())
    assert all(token in table for token in ('618 students', '630 students', '678 st', '0.40', 'g = .21', 'g = .14'))
    assert '963 students' in ' '.join(reader.pages[1].extract_text().split())
    assert sum(row['children'] for row in COMPARISONS) == 2 * 963
    assert sum(row['schools'] for row in COMPARISONS) == 2 * 42
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography, queue = load(bibliography_path), load(queue_path)
    assert all(row['id'] != SOURCE for row in bibliography)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    notes = dict(
        source_id=SOURCE, source_url=URL, date='2026-11-09', reviewer='Codex',
        source_asset_kind='pdf', source_pdf_sha256=PDF_SHA, source_pdf_redistributed=False,
        contains_source_full_text=False, read_scope=SCOPE, empirical_scope=EMPIRICAL,
        pdf_text_pages=TEXT_PAGES, visual_pdf_pages=VISUAL_PAGES,
        rendered_page_sha256={str(p): sha(CACHE / f'wwc-kindergarten-page-{p}.png') for p in VISUAL_PAGES},
        original_article=dict(doi=STUDY_DOI, printed_pages=[105, 135], abstract_url=STUDY_ABSTRACT,
                              original_pdf_obtained=False, original_page_layout_review=False,
                              abstract_comparison_order=['FT vs control', 'NFT vs control'],
                              abstract_itt_g=[.33, .22], abstract_tot_g=[.38, .30]),
        study_page=ONLINE, same_cohort_as=['CLEMENTS_ET_AL_2011_BUILDING_BLOCKS', 'CLEMENTS_ET_AL_2013_TRIAD_FOLLOWTHROUGH'],
        comparisons=COMPARISONS,
        reading_log=[
            'WWC PDF 본문·부록·미주·용어를 읽고 2·6·7쪽의 유보, 계산 표와 판정 범위를 이미지로 확인했다.',
            '같은 WWC 사이트의 2014년 단일 연구 평가와 2018년 보조금 심사를 따로 대조했다.',
            '2012년 기관 서지 초록의 효과크기와 2013년 선출판판의 유치원 결과 회고를 비교했다.',
        ],
        source_corrections=[
            dict(location='WWC 2014 PDF 부록 C, 두 중재군 비교', issue='효과크기 계산 행은 nr이고 주석도 미보고라고 설명한다. 영역 요약 행에 반복 인쇄된 .40·+15는 해당 비교의 추정치로 사용하지 않는다.'),
            dict(location='2012년 초록과 WWC 2014 PDF 부록 C 주석', issue='취학 전 중재만 대 대조의 g는 초록에 .22, WWC가 인용한 논문 116쪽에 .21로 적혔다. 두 중재군 비교의 .14도 WWC가 인용한 저자 수치다. WWC는 두 크기를 독립적으로 재구성하지 못했다.'),
            dict(location='WWC 2014 PDF와 2014·2018 온라인 표', issue='후속 지원 대 대조의 개선 지수는 PDF +15, 2014년 온라인 +16, 2018년 온라인 +13이다. 평균과 지수는 각 자료에 귀속한다.'),
            dict(location='2012년 초록, WWC 심사, 2013년 후속 논문 선출판판 6쪽', issue='유치원 말 취학 전 중재만 대 대조의 유의 여부가 다르게 서술됐다. 원논문의 분석표는 미확보다.'),
            dict(location='WWC 2014 PDF 8쪽 용어 풀이', issue='p값은 귀무가설과 검정 가정 아래에서 관측값만큼 또는 그보다 극단적인 검정 통계량을 얻을 확률이다. 차이가 우연 때문일 확률로 읽지 않는다. 표의 .00도 정확한 0으로 읽지 않는다.'),
        ],
    )
    entry = dict(
        id=SOURCE, year=2014, url=URL, kind='동일 무작위 연구의 유치원 결과에 대한 공식 단일 연구 심사',
        title='WWC Review of Longitudinal Evaluation of a Scale-Up Model for Teaching Mathematics with Trajectories and Technologies',
        authors=['Institute of Education Sciences, What Works Clearinghouse'],
        review_scope=SCOPE, does_not_establish=LIMIT,
        next_review='Sarama 외 2012년 논문의 116~117쪽 모형·기술통계와 탈락 분모를 원본에서 확인한다.',
        supports=['유치원 말 세 비교의 분모와 판정', '후속 교사 지원 범위', 'WWC PDF와 온라인 수치의 귀속'],
    )
    snapshot = ROOT / NOTES
    write(snapshot, notes)
    bibliography.append(entry)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=notes['date'],
        snapshot_kind='authored_review_notes', source_asset_kind='pdf', source_pdf_sha256=PDF_SHA,
        snapshot_file=NOTES, snapshot_sha256=sha(snapshot), redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=URL, authors_year='WWC, 2014'),
        read_scope=SCOPE, scope_note='유치원 말 REMA의 심사 결과다. 초등 1학년 결과와 동일 표본의 후속 보고를 구별한다.',
        method_note='2014년 PDF 표의 계산 행과 주석, 2014년·2018년 온라인 표를 비교했다.',
        limits=LIMIT, empirical_scope=EMPIRICAL, independent_review=False, student_validated=False,
        editorial_action='문헌 대응 4건을 추가했다.', observations=[],
    )
    for claim_id, codes, role, pages, links, support, limit in CLAIMS:
        claim = dict(
            id=claim_id, source_id=SOURCE, role=role, standard_codes=codes,
            locations=[*(f'{URL}#page={p}' for p in pages), *links],
            support=support, does_not_establish=limit, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        )
        if role == 'empirical_result_with_scope':
            claim['empirical_scope'] = EMPIRICAL
        registry['claims'].append(claim)
    queue['literature_review'].append(dict(
        source=entry, status='self_read_claim_mapping', evidence_file='data/literature_claim_reviews.json',
        claim_evidence_fields=['유치원 지원의 범위', '비교별 분모와 효과의 출처', '심사 유보와 적용 한계'],
        claim_ids=ids,
    ))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()


if __name__ == '__main__':
    main()

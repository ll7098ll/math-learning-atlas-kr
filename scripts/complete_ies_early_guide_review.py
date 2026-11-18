"""Register the endnotes and bibliography of the IES early mathematics guide."""
import copy

from extend_ies_early_instruction_study_tables import NOTES as PRIOR, SIEGLER
from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_ies_early_literature_review import PDF_URL, RATINGS, SHA, SOURCE


PRIOR_SHA = '378a9640f9d8a718da1ff4edf24d506bafb4a99c8f4d689c0fed3b9c8c24f5a0'
NOTES = 'data/literature_evidence/IES_EARLY_2013_endnotes_references_review_notes.json'
PAGES = [*range(138,142), *range(143,151), *range(152,166)]
SCOPE = ('가이드 PDF 전체 165쪽의 텍스트와 선정 116쪽 이미지를 대조했다. '
         '남은 미주·참고문헌 26쪽을 등록했다. 별도 WWC 2.1 절차의 9쪽 텍스트 검토도 유지한다.')
LIMITS = ('가이드의 서지·비교 조건·집계 기준을 확인한 범위다. 인용 원연구의 미확인 본문, 일부 표와 본문의 집계 의도, '
          '다른 판본·후속 연구와의 대조, 독립 검토와 국내 학생 관찰 검증은 별도 범위다.')
KLEIN = 'https://ies.ed.gov/ncee/wwc/study/77968'
FUCHS = 'https://doi.org/10.1086/499684'
PCER = 'https://ies.ed.gov/sites/default/files/migrated/nces_pubs/ncer/pubs/20082009/pdf/20082009_rev.pdf'

# Units normalize author-year aliases across notes without merging distinct PCER chapters.
MEASUREMENT_RESULTS = [
    'Clements_Sarama_2007b', 'Clements_Sarama_2008', 'Clements_2011', 'Fantuzzo_2011',
    'Klein_2008', 'PCER_2008_ch2', 'PCER_2008_ch3', 'Sarama_2008', 'Weaver_1991',
]
DATA_TARGETED = ['Clements_Sarama_2007b', 'Clements_Sarama_2008', 'Clements_2011', 'Klein_2008', 'Sarama_2008']
DATA_ADDITIONAL = ['PCER_2008_ch2', 'PCER_2008_ch3', 'Fantuzzo_2011']
UNKNOWN_D7 = ['Arnold_2002', 'Clements_Sarama_2008', 'Griffin_1995_1994', 'PCER_2008_ch2', 'PCER_2008_ch3', 'Sarama_2008']
UNKNOWN_D8 = ['Aunio_2005', 'Clements_Sarama_2008', 'Griffin_1995_1994', 'PCER_2008_ch2', 'PCER_2008_ch3', 'Sarama_2008']
BOLD_BY_START_PAGE = {
    158: ['Arnold 2002', 'Aunio et al. 2005', 'Barnett 2008', 'Baroody et al. 2009', 'Casey 2008'],
    159: ['Clements and Sarama 2007b', 'Clements and Sarama 2008', 'Clements et al. 2011', 'Curtis et al. 2009'],
    160: ['Dyson et al. 2013', 'Fantuzzo et al. 2011', 'Fuchs et al. 2001', 'Griffin et al. 1995', 'Griffin et al. 1994'],
    161: ['Jordan et al. 2012', 'Kidd et al. 2008', 'Klein et al. 2008', 'Lai et al. 2008'],
    162: ['Monahan 2007'],
    163: ['PCER 2008 ch. 2', 'PCER 2008 ch. 3', 'Ramani and Siegler 2008', 'Ramani and Siegler 2011',
          'Sarama et al. 2008', 'Siegler 1995', 'Siegler and Ramani 2008', 'Siegler and Ramani 2009', 'Sood 2009'],
    164: ['Sophian 2004', 'Weaver 1991'],
    165: [],
}

CORRECTIONS = [
    dict(status='measurement_counts_reproduced_editorial_intent_open', locations=['PDF 32 and 142 notes 78–79', 'PDF 99', 'PDF 152 notes 284, 287–288', 'PDF 153 note 293'],
         issue='측정 결과 서술의 인용은 9개다. D.5의 표시 비교 11개를 인용·장으로 묶으면 미주 284와 같은 10개다. 두 목록에서 다른 항목은 Sophian(2004)이다.',
         followup='Sophian은 양의 단위를 다뤘으나 가이드는 측정을 명시적 요소로 보기 어렵다고 설명한다. 두 집계는 목록으로 재현되며 본문 집필진의 집계 의도는 미확정이다.'),
    dict(status='data_analysis_five_and_eight_scopes_reconciled', locations=['PDF 32', 'PDF 99', 'PDF 142 notes 80–82', 'PDF 153 notes 294–296'],
         issue='부록의 5개는 Building Blocks 또는 DLM을 포함해 자료 분석을 의도적으로 다룬 연구다. PCER 2·3장과 EPIC을 더하면 본문의 8개다.',
         followup='교육 활동의 구성과 시험이 실제로 측정한 결과를 구별한다.'),
    dict(status='comparison_description_counts_scoped', locations=['PDF 116 note 364', 'PDF 125 note 406', 'PDF 144 note 123', 'PDF 145 note 142', 'PDF 155 note 364', 'PDF 157 note 406'],
         issue='권고 4의 비교군 정보 부족은 본문 미주 6개와 부록 9개, 권고 5는 본문 미주 6개와 부록 11개다.',
         followup='부록 미주의 목록은 재현했다. 표에 ?만 있는 경우와 X가 있으나 비교군의 일부 요소가 불명확한 경우를 구별한다. 본문 6개의 집계 기준은 확정하지 않는다.'),
    dict(status='siegler_endnotes_feedback_order_corrected', locations=['PDF 154 note 355', 'PDF 155 note 363', SIEGLER],
         issue='미주는 자기 추론 설명이 피드백 뒤라고 쓰지만 원논문 방법에서 자기 설명은 피드백 전이다. 실험자의 판단 이유를 설명한 조건에서는 아이가 피드백 뒤에 설명했다.',
         followup='IE17의 원연구 역할을 실험자로 정정한다. 국내 자체 과제의 교사 역할과 구별한다.'),
    dict(status='fuchs_and_klein_years_crosschecked', locations=['PDF 142 note 79', 'PDF 144 note 121', 'PDF 152 notes 284, 287', 'PDF 153 note 290', 'PDF 155 notes 374–375', 'PDF 160–161', FUCHS, KLEIN],
         issue='일부 미주의 2011 표기와 달리 Fuchs 외 PALS 논문은 2001년, Klein 외 278명 비교 논문은 2008년이다.',
         followup='가이드 참고문헌·출판사·WWC 연구 기록에 맞춰 해당 논문을 식별한다. 인쇄된 미주 표기는 차이 기록에 보존한다.'),
    dict(status='sood_nonverbal_maintenance_discrepancy_open', locations=['PDF 92–93', 'PDF 150 note 229'],
         issue='미주는 Sood의 비언어적 계산 효과가 3주 뒤 유지됐다고 설명하나, 표 D.4의 유지 행은 0.12 ns로 뚜렷하지 않음이다.',
         followup='직후 0.37 ns와 유지 0.12 ns를 분리한다. 두 해석의 차이는 원학위논문에서 검토한다.'),
    dict(status='barnett_domain_and_summary_discrepancy_open', locations=['PDF 82', 'PDF 140 note 36', 'PDF 142 note 77', 'PDF 151 note 258'],
         issue='미주 36은 Barnett을 긍정 연구 목록에 포함하고 미주 77은 일반 수리력을 언급한다. D.3 본행과 미주 258은 연산 결과를 뚜렷하지 않음으로 분류한다.',
         followup='D.3에 실린 WJ-R 응용 문제 결과는 0.17 ns다. 다른 영역이나 판정은 원연구의 분석 범위 확인 전까지 보류한다.'),
]

MAPPINGS = [
    ('IE19', ['2수03-06', '2수03-10'], [32, 99, 142, 152, 153],
     '측정 활동을 포함한 인용과 길이·들이·무게를 직접 평가한 결과는 서로 다르다. 미주 288은 해당 측정 개입 묶음 중 Clements 외(2011)가 별도 측정 하위척도를 보고했다고 밝힌다. 자체 과제에서 직접 비교, 단위 선택, 반복을 따로 관찰하는 데 참고한다.',
     '권고 2는 Minimal이다. 측정 관련 인용 9개와 부록 전체 10개를 구별한다. 여러 내용이 포함된 일반 수리력 결과를 특정 측정 과제의 학습 효과로 해석할 수 없다.'),
    ('IE20', ['2수04-01', '2수04-02', '2수04-03'], [32, 99, 142, 153],
     '가이드의 자료 분석 범위는 집중 연구 5개와 추가 비교 3개다. 표에는 프로그램의 일반 수리력·기본 수 개념 등 결과가 실린다. 자체 과제에서는 자료 분류, 표 기록, 그래프 표현과 해석을 따로 확인한다.',
     '권고 2는 Minimal이다. 활동을 가르친 범위와 그 활동을 직접 검사한 결과를 구분한다. 국내 분류·표·그래프 발문의 효과나 학습 순서의 타당성은 별도 검증이 필요하다.'),
]


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['reading_extension']['file'] == NOTES:
        assert {row[0] for row in MAPPINGS} <= {claim['id'] for claim in registry['claims']}
        build_report()
        return
    assert source['reading_extension'] == dict(file=PRIOR, sha256=PRIOR_SHA)
    assert sha(ROOT / PRIOR) == PRIOR_SHA and sha(ROOT / source['snapshot_file']) == SHA
    previous = load(ROOT / PRIOR)
    assert previous['unread_full_pdf_pages'] == PAGES
    assert not set(PAGES) & set(source['visual_pdf_pages'])
    text_pages = sorted(source['text_pdf_pages'] + PAGES)
    visual_pages = sorted(source['visual_pdf_pages'] + PAGES)
    assert text_pages == list(range(1,166)) and len(visual_pages) == 116
    prior_number = load(ROOT / previous['previous_reading_extension']['file'])
    appendix = load(ROOT / prior_number['previous_reading_extension']['file'])
    prior_measure = load(ROOT / appendix['previous_reading_extension']['file'])
    rows = prior_measure['measurement_table_audit']['rows']
    measure_units = sorted({row['citation_unit'] for row in rows})
    assert len(rows) == 11 and len(measure_units) == 10
    assert set(measure_units) - set(MEASUREMENT_RESULTS) == {'Sophian_2004'}
    assert len(set(MEASUREMENT_RESULTS)) == 9
    assert set(DATA_TARGETED).isdisjoint(DATA_ADDITIONAL)
    bold = {name for names in BOLD_BY_START_PAGE.values() for name in names}
    d1 = set(appendix['table_d1']['citation_rows'])
    assert len(bold) == 30 and len(d1) == 29
    assert (bold - {'Griffin et al. 1995', 'Griffin et al. 1994'}) | {'Griffin et al. 1995 and related 1994 publication'} == d1
    log = [
        'PDF 138~157의 미주를 대조했다. 기존 등록 PDF 142·151을 제외한 18쪽을 추가했다. 미주 3은 파일럿 SCD/RDD의 근거 등급 반영 제외를 명시한다. 별도 검토 절차의 연구 설계 적격과 구별한다.',
        '미주 79·284·287의 측정 인용 단위, 미주 80~82·294~296의 자료 분석 범위, 미주 123·142·364·406의 비교 조건을 대조했다.',
        'PDF 158~165의 참고문헌 8쪽에서 굵은 인용 항목 30개를 D.1의 인용·장 29개와 연결했다. Griffin 관련 두 서지를 한 인용행에서 사용한다.',
    ]
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    corrections = source['source_discrepancies'] + CORRECTIONS
    claim = next(row for row in registry['claims'] if row['id']=='IE17')
    original_support = claim['support']
    assert original_support.count('교사가') == 2
    claim['support'] = original_support.replace('교사가','실험자가')
    claim['locations'] += [f'{PDF_URL}#page={p}' for p in [154,155]]
    notes = dict(
        source_id=SOURCE, source_url=source['display']['url'], source_pdf_sha256=SHA,
        contains_source_full_text=False, licensed_source_pdf_preserved=True,
        previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_reading_extension=dict(file=PRIOR, sha256=PRIOR_SHA),
        cumulative_read_scope=SCOPE, cumulative_text_pdf_pages=text_pages, cumulative_visual_pdf_pages=visual_pages,
        new_text_pdf_pages=PAGES, new_visual_pdf_pages=PAGES, unread_full_pdf_pages=[], reading_log=log,
        new_image_sha256={str(p): sha(ROOT / f'tmp/literature/ies-early-endnotes-review/page-{p}.png') for p in PAGES},
        evidence_ratings=RATINGS, source_corrections=corrections,
        measurement=dict(d5_printed_comparison_rows=11, appendix_note_284_citation_units=measure_units,
                         result_summary_notes_79_and_287_citation_units=MEASUREMENT_RESULTS,
                         appendix_only_inclusion='Sophian_2004', common_pcer_control_chapter=2,
                         original_editorial_intent_confirmed=False, measurement_outcome_note_288='Clements_2011'),
        data_analysis=dict(appendix_targeted_note_294=DATA_TARGETED, appendix_additional_notes_295_296=DATA_ADDITIONAL,
                           main_total_notes_81_82=len(DATA_TARGETED)+len(DATA_ADDITIONAL)),
        comparison_information=dict(
            d7_six_table_question_mark_units=UNKNOWN_D7,
            d7_nine_note_364_units=UNKNOWN_D7+['Barnett_2008','Klein_2008','Sophian_2004'],
            d8_six_table_question_mark_only_units=UNKNOWN_D8,
            d8_eleven_note_406_units=UNKNOWN_D8+['Arnold_2002','Barnett_2008','Clements_Sarama_2007b','Klein_2008','Sophian_2004'],
            main_text_counting_rules_confirmed=False),
        bibliography=dict(bold_entries_by_start_pdf_page=BOLD_BY_START_PAGE, bold_reference_entries=30, d1_citation_rows=29,
                          grouped_related_publications=['Griffin et al. 1995','Griffin et al. 1994'],
                          dissertation_identifiers=dict(Monahan='3271792',Sood='3373089'),
                          pcer_original=dict(url=PCER, chapter_2_printed_pages=[41,54],chapter_3_printed_pages=[55,64],
                                             chapter_2_initial_total=309, chapter_2_initial_shared_comparison=105,
                                             guide_comparison_analysis_n=100),
                          cited_study_reading_implied=False),
        revised_claim=dict(id='IE17', previous_support=original_support, current_support=claim['support']),
    )
    write(ROOT / NOTES, notes)
    source.update(date='2026-11-09', bibliography_snapshot=digest(entry),
                  reading_extension=dict(file=NOTES, sha256=sha(ROOT / NOTES)),
                  text_pdf_pages=text_pages, visual_pdf_pages=visual_pages, read_scope=SCOPE, limits=LIMITS,
                  reading_log=source['reading_log'] + log, source_discrepancies=corrections,
                  editorial_action='미주와 참고문헌 대조를 마쳐 근거 2건을 추가하고 기존 1건의 원연구 역할을 바로잡았다.')
    for cid, codes, pages, support, limit in MAPPINGS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='instructional_recommendation_with_evidence_scope',
            locations=[f'{PDF_URL}#page={p}' for p in pages], support=support, does_not_establish=limit,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
            standard_codes=codes, independent_review=False, student_validated=False, local_effect_tested=False,
            recommendations=[dict(number=2, evidence_rating=RATINGS['2'], application_limit=limit)],
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE])
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json',registry)
    write(queue_path,queue)
    build_report()
    print('Registered all guide text pages, the bibliography crosswalk, and two scoped claims.')


if __name__ == '__main__':
    main()

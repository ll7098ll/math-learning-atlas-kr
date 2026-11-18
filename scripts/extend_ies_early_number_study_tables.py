"""Record the IES number intervention comparisons and their review protocol."""
import copy

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_ies_early_literature_review import PDF_URL, RATINGS, SHA, SOURCE


PRIOR = 'data/literature_evidence/IES_EARLY_2013_appendix_review_notes.json'
PRIOR_SHA = 'fdd91d6dbdff771697ab5b9d7a09804445b7e49cfdf79baaa8bbe1a9bd40709f'
NOTES = 'data/literature_evidence/IES_EARLY_2013_number_study_tables_review_notes.json'
PAGES = list(range(82, 96))
SCOPE = ('가이드 PDF 165쪽 중 누적 텍스트 110쪽과 이미지 61쪽을 대조했다. '
         '표 D.3·D.4와 주석을 추가로 확인하고, 별도 WWC 2.1 검토 절차 PDF의 전체 9쪽 텍스트를 확인했다.')
LIMITS = ('가이드 D.6~D.8, 나머지 미주·참고문헌 55쪽과 표에 인용된 원연구의 미확인 범위는 후속이다. '
          '측정 연구 건수 9와 10, Lai 외의 가이드 분석표본 30명과 원연구 초록 전체 60명의 관계는 보류한다.')
CURTIS = 'https://doi.org/10.1016/j.ecresq.2009.04.003'
CURTIS_WWC = 'https://ies.ed.gov/ncee/wwc/study/77951'
AUNIO = 'https://www.researchgate.net/publication/46664799_Mathematical_thinking_intervention_programmes_for_preschool_children_with_normal_and_low_number_sense'
LAI = 'https://doi.org/10.1016/j.cogdev.2007.06.002'
SIEGLER = 'https://siegler.tc.columbia.edu/wp-content/uploads/2019/02/sieg-ram08.pdf'
PROTOCOL = 'https://ies.ed.gov/ncee/wwc/Docs/ReferenceResources/numeracy_protocol_v2.1.pdf'
PROTOCOL_SHA = '5916a5a60431cfc4352e7353deca4b72a1e88446b68145979e3fa3901e364fc5'

# Each outcome count refers to printed rows for the comparison, including maintenance.
D3 = [
    ('Aunio et al. 2005', 'Lets Think and Maths', 82, 45, 22, 23, 8),
    ('Barnett et al. 2008', 'Tools of the Mind', 82, 202, 85, 117, 1),
    ('Fantuzzo et al. 2011', 'EPIC vs DLM', 82, 778, 397, 381, 1),
    ('PCER 2008 ch. 2', 'Creative Curriculum', 83, 193, 93, 100, 3),
    ('PCER 2008 ch. 2', 'Bright Beginnings', 83, 198, 98, 100, 3),
    ('PCER 2008 ch. 3', 'Creative Curriculum', 83, 170, 90, 80, 6),
]
D4 = [
    ('Baroody et al. 2009', 'semi-structured vs haphazard', 87, 40, 20, 20, 2),
    ('Baroody et al. 2009', 'implicit vs haphazard', 87, 40, 20, 20, 2),
    ('Baroody et al. 2009', 'explicit vs haphazard', 87, 40, 20, 20, 2),
    ('Curtis et al. 2009', 'experiment 1 count support', 88, 25, 14, 21, 4),
    ('Curtis et al. 2009', 'experiment 2 count support', 88, 54, 27, 27, 4),
    ('Dyson et al. 2013', 'additional numeracy vs regular instruction', 89, 121, 56, 65, 4),
    ('Jordan et al. 2012', 'numeracy vs regular instruction', 89, 86, 42, 44, 4),
    ('Jordan et al. 2012', 'numeracy vs additional literacy', 89, 84, 42, 42, 4),
    ('Kidd et al. 2008', 'numeracy vs art', 90, 52, 26, 26, 5),
    ('Kidd et al. 2008', 'numeracy vs cognitive instruction', 90, 52, 26, 26, 5),
    ('Lai et al. 2008', 'inversion vs composition and decomposition', 90, 30, 15, 15, 1),
    ('Monahan 2007', 'math vs reading', 91, 80, 41, 39, 1),
    ('Monahan 2007', 'math with story vs reading', 91, 81, 42, 39, 1),
    ('Monahan 2007', 'math with movement vs reading', 91, 78, 39, 39, 1),
    ('Ramani and Siegler 2008', 'numbers vs colors', 91, 124, 68, 56, 6),
    ('Siegler and Ramani 2008', 'experiment 2 numbers vs colors', 92, 36, 18, 18, 2),
    ('Sood 2009', 'number sense vs regular instruction', 92, 101, 61, 40, 16),
    ('Sophian 2004', 'measurement-focused math vs literacy', 93, 94, 46, 48, 1),
]

CORRECTIONS = [
    dict(status='curtis_experiment_1_total_corrected', locations=['PDF 88', CURTIS, CURTIS_WWC],
         issue='Curtis 외 실험 1의 인쇄 합계 25명은 중재 14명과 비교 21명 및 출판사 초록·2022년 WWC 검토와 일치하지 않는다.',
         printed_total=25, corrected_total=35, experiment_2_total=54,
         followup='합계는 35명을 사용한다. 가이드의 2.1 검토와 WWC의 2022년 4.1 검토를 구별한다.'),
    dict(status='aunio_prose_table_classification_distinguished', locations=['PDF 81', 'PDF 82', AUNIO],
         issue='본문은 6개월 후 기하에서 뚜렷한 효과가 없다고 요약한다. 표는 도형 유추 0.24를 뚜렷하지 않음, 공간 관계 0.36을 긍정으로 분류한다. 두 값 모두 ns다.',
         followup='원논문 인쇄 139~140쪽의 전체 표본 추후 검사도 유의한 집단 차이를 보고하지 않는다. 역사적 크기 기준과 통계적 유의성, 원논문의 별도 소표본 분석을 구별한다.'),
    dict(status='siegler_note_pointer_mismatch_direction_verified', locations=['PDF 92', 'PDF 95 notes 25, 27, 28', SIEGLER + '#page=5'],
         issue='수직선 추정 오차의 0.86* 옆에 미주 25가 달려 있으나 이는 Monahan의 움직임 비교를 설명한다. 낮을수록 바람직한 오차의 표시 방향 설명은 미주 27에 있다.',
         printed_note=25, related_note=27, reported_effect=0.86,
         followup='Siegler와 Ramani 원논문 인쇄 659쪽에서 숫자판 집단 오차 28%→20%, 색깔판 27%→28%를 확인했다. 원척도 오차가 낮아진 방향과 가이드의 양의 표기를 구별한다. 인쇄 미주와 효과값은 그대로 기록한다.'),
    dict(status='lai_analytic_sample_scope_open', locations=['PDF 90', 'PDF 95 note 21', LAI],
         issue='가이드 비교는 15명씩 30명을 싣고, 출판사 초록의 전체 훈련 실험은 4~5세 60명을 보고한다.',
         followup='두 수를 별도 범위로 인용하고, 어떤 하위 표본이 가이드에 포함됐는지는 원연구의 상세 분석 대조 전까지 보류한다.'),
]

OBSERVATIONS = [
    dict(id='IE-P10', standard_codes=['2수01-01', '2수03-06'],
         question='무게가 같은 빈 봉투 두 개에 같은 무게의 추를 A에는 4개, B에는 3개 넣었다. 어느 봉투가 더 무거운가? B의 추 하나를 더 무거운 추로 바꾸면 개수만 세어도 비교할 수 있을까? 무엇으로 확인할까?',
         expected='처음에는 같은 추를 1개 더 넣은 A가 무겁다. 바꾼 뒤에는 개수가 그대로라도 바뀐 추의 무게에 따라 결과가 달라진다. 두 봉투를 양팔저울로 직접 비교한다.',
         interpretation='처음 비교에서 일대일 대응이나 셈을 활용하는지, 조건이 달라진 뒤에도 개수가 무게를 결정한다고 보는지 구별한다. 무게 추측과 저울 확인을 따로 기록한다.',
         student_validated=False),
    dict(id='IE-P11', standard_codes=['2수01-05', '2수01-07'],
         question='상자에 구슬이 6개 있다. 3개를 넣었다가 3개를 꺼내면, 다시 전부 세지 않고도 몇 개인지 어떻게 알 수 있을까? 3개를 넣고 2개만 꺼내면 무엇이 달라질까?',
         expected='넣은 개수만큼 꺼내면 처음의 6개로 돌아간다. 2개만 꺼내면 넣은 3개 중 1개만큼 늘어 7개가 된다.',
         interpretation='두 번 계산해 얻은 답과 같은 수를 더했다 빼는 관계 설명을 구별한다. 같은 구슬을 꺼내야만 전체 개수가 돌아온다고 설명하면 다른 구슬을 꺼내도 되는지 물어 수량과 개체를 구분하는지 본다.',
         student_validated=False),
]

MAPPINGS = [
    ('IE12', OBSERVATIONS[0]['standard_codes'], 1, [88, 94], [CURTIS, CURTIS_WWC],
     'Curtis 외의 가이드 표는 성인이 추를 세어 전체 개수를 말해 준 조건을 비교한다. 실험 1의 합계는 35명이고, 무게 차이가 큰 문항과 작은 문항의 가이드 효과 방향이 서로 달랐다. 개수와 무게의 대응 조건을 확인하는 발문에 참고한다.',
     '두 문항 모두 가이드에서 통계적으로 유의하지 않다. WWC의 2022년 별도 검토도 실험 1에서 유의한 긍정 결과를 확인하지 않았다. 자체 봉투 과제의 효과나 무게 비교 전반을 검증한 자료는 아니다.'),
    ('IE13', ['2수03-03'], 2, [81, 82, 84], [AUNIO],
     'Aunio 외의 추후 검사에서 도형 유추와 공간 관계는 서로 다른 척도다. 표 D.3은 공간 관계 0.36을 당시 크기 기준으로 긍정 분류했으나 유의하지 않았다. 도형 구성 활동의 성과를 설명할 때 과제별 근거를 구별하는 데 참고한다.',
     'D.3은 권고 1 근거 표이며 여기서는 권고 2의 도형 활동에 결과 해석의 한계만 연결한다. 이 비교는 국내 도형 구성 활동의 효과나 장기 전이를 확립하지 않는다.'),
    ('IE14', OBSERVATIONS[1]['standard_codes'], 1, [90, 95], [LAI],
     '표 D.4의 Lai 외 비교는 역관계를 다룬 지도와 수의 합성·분해 활동을 비교해 역연산 문항의 변화에 0.54*를 보고했다. 더한 만큼 빼는 경우와 덜 빼는 경우의 설명을 구별하는 발문에 참고한다.',
     '가이드 비교표의 30명과 논문 초록의 전체 60명을 구별한다. 활동을 받은 두 집단의 특정 문항 결과이며 국내 과제의 효과나 전체 연산의 전이를 확인한 자료는 아니다.'),
    ('IE15', ['2수01-01'], 1, [92, 95], [SIEGLER + '#page=5'],
     'Siegler와 Ramani의 실험 2는 수를 붙인 선형판과 색깔판을 비교했다. 수직선 위치 오차가 작아지는 것과 수의 순서를 더 자주 맞히는 것을 따로 측정했다. 수의 크기와 위치에 관한 학생 설명을 따로 확인하는 데 참고한다.',
     '가이드의 양의 효과는 오차가 커졌다는 뜻이 아니다. 36명의 두 조건 비교이며 놀이의 장기 효과, 다른 수 범위나 국내 활동으로의 전이는 확인하지 않았다.'),
]


def comparison_rows(rows):
    return [dict(citation=citation, contrast=contrast, first_pdf_page=page,
                 last_pdf_page=93 if citation == 'Sood 2009' else page,
                 printed_total=total, intervention=n1, comparison=n2,
                 checked_total=n1 + n2, printed_outcome_rows=count)
            for citation, contrast, page, total, n1, n2, count in rows]


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['reading_extension']['file'] == NOTES:
        assert source['observations'][-2:] == OBSERVATIONS
        assert {row[0] for row in MAPPINGS} <= {claim['id'] for claim in registry['claims']}
        build_report()
        return
    assert source['reading_extension'] == dict(file=PRIOR, sha256=PRIOR_SHA)
    assert sha(ROOT / PRIOR) == PRIOR_SHA and sha(ROOT / source['snapshot_file']) == SHA
    protocol_file = ROOT / 'tmp/literature/ies-early-protocol-2_1.pdf'
    assert sha(protocol_file) == PROTOCOL_SHA
    assert not set(PAGES) & set(source['text_pdf_pages'])
    text_pages = sorted(source['text_pdf_pages'] + PAGES)
    visual_pages = sorted(set(source['visual_pdf_pages']) | set(PAGES))
    assert (len(text_pages), len(visual_pages)) == (110, 61)
    d3 = comparison_rows(D3)
    d4 = comparison_rows(D4)
    assert (len(d3), sum(row['printed_outcome_rows'] for row in d3)) == (6, 22)
    assert (len(d4), sum(row['printed_outcome_rows'] for row in d4)) == (18, 65)
    assert [row['contrast'] for row in d3+d4 if row['printed_total'] != row['checked_total']] == ['experiment 1 count support']
    log = [
        'PDF 82~84쪽의 D.3과 주석에서 다섯 인용·장, 비교 6개, 결과 22행을 대조했다. PCER 제2장 두 비교는 비교 집단 크기가 모두 100명이지만 인원 동일성은 이 표만으로 확정하지 않았다.',
        'PDF 85~95쪽의 표적 개입 설명과 D.4 및 주석에서 인용 11개, 비교 18개, 결과 65행을 대조했다. Sood의 PDF 92~93쪽은 한 비교의 결과 16행이다. Baroody의 E-3은 셈으로 답한 경우와 일률 전략 반응 편향을 제외한다.',
        'Curtis의 실험 1과 2는 각각 결과별 사전검사 대신 셈과 양 어림의 사전검사를 썼다고 주석 11·13이 설명한다. 실험 1 총계와 가이드 판정의 범위를 기록했다.',
        '별도 WWC 검토 절차 2.1 텍스트 1~9쪽에서 검색·포함·척도·탈락·동등성·조정 규칙을 대조했다. 이 9쪽은 가이드의 읽기 누계에서 제외했다.',
    ]
    corrections = source['source_discrepancies'] + CORRECTIONS
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(
        source_id=SOURCE, source_url=source['display']['url'], source_pdf_sha256=SHA,
        contains_source_full_text=False, licensed_source_pdf_preserved=True,
        previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_reading_extension=dict(file=PRIOR, sha256=PRIOR_SHA),
        cumulative_read_scope=SCOPE, cumulative_text_pdf_pages=text_pages, cumulative_visual_pdf_pages=visual_pages,
        new_text_pdf_pages=PAGES, new_visual_pdf_pages=PAGES,
        unread_full_pdf_pages=sorted(set(range(1, 166))-set(text_pages)), reading_log=log,
        new_image_sha256={str(p): sha(ROOT / f'tmp/literature/ies-early-appendix-review/page-{p}.png') for p in PAGES},
        evidence_ratings=RATINGS, source_corrections=corrections,
        table_d3=dict(citation_or_chapter_units=5, comparisons=d3, participants_are_not_summed=True),
        table_d4=dict(citation_units=11, comparisons=d4, participants_are_not_summed=True,
                      shared_arms=[
                          dict(citation='Baroody et al. 2009', shared_arm='comparison', n=20, contrasts=3),
                          dict(citation='Jordan et al. 2012', shared_arm='intervention', n=42, contrasts=2),
                          dict(citation='Kidd et al. 2008', shared_arm='intervention', n=26, contrasts=2),
                          dict(citation='Monahan 2007', shared_arm='comparison', n=39, contrasts=3),
                      ]),
        review_protocol=dict(url=PROTOCOL, version='2.1', pdf_sha256=PROTOCOL_SHA, text_pdf_pages=list(range(1,10)),
                             visual_pdf_pages=[], separate_from_guide=True, database_count=7,
                             age_scope='3~6세 중 대다수가 6세 미만인 표본 또는 유치원. 혼합 연령은 분리 결과나 적격 연령 과반이 필요하다.',
                             eligibility='영어 보고서, 원칙적으로 1989~2011년, 위원 제안 예외 허용. 표본 국가와 수업 언어는 제한하지 않는다. RCT, QED, RD, SCD를 검토한다.',
                             outcome_scope='여섯 영역으로 나누고 일반 수리력은 두 영역 이상을 포함한다. 중재에 과도하게 맞춘 평가를 등급 결정에서 제외하고 직후와 유지 검사를 구별한다.',
                             reliability_minima=dict(internal_consistency=0.60, test_retest=0.40, inter_rater=0.50),
                             attrition_boundary='liberal', baseline_adjustment_if_difference_exceeds_sd=0.05,
                             baseline_equivalence_maximum_sd=0.25, default_intraclass_correlation=0.20,
                             technical_scope='사전 동등성은 필요한 경우 분석표본의 해당 결과 사전검사를 기준으로 한다. 대체 척도는 별도 판단한다. 필요하면 군집과 비교·영역 내 다중 검정의 유의성을 조정한다.'),
    )
    write(ROOT / NOTES, notes)
    source.update(date='2026-11-09', bibliography_snapshot=digest(entry),
                  reading_extension=dict(file=NOTES, sha256=sha(ROOT / NOTES)),
                  text_pdf_pages=text_pages, visual_pdf_pages=visual_pages, read_scope=SCOPE, limits=LIMITS,
                  reading_log=source['reading_log'] + log, source_discrepancies=corrections,
                  editorial_action='연구표 D.3·D.4를 대조해 문헌 대응 4건과 자체 관찰 과제 2개를 추가했다.',
                  observations=source['observations'] + OBSERVATIONS)
    for cid, codes, number, pages, extra_sources, support, limit in MAPPINGS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='instructional_recommendation_with_evidence_scope',
            locations=[f'{PDF_URL}#page={page}' for page in pages] + extra_sources,
            support=support, does_not_establish=limit,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
            standard_codes=codes, independent_review=False, student_validated=False, local_effect_tested=False,
            recommendations=[dict(number=number, evidence_rating=RATINGS[str(number)], application_limit=limit)],
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[c['id'] for c in registry['claims'] if c['source_id'] == SOURCE])
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Registered IES D.3 and D.4, four scoped claims, and two observation tasks.')


if __name__ == '__main__':
    main()

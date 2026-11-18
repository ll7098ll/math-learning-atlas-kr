"""Register the remaining intervention comparisons in Appendix D of the IES guide."""
import copy

from extend_ies_early_number_study_tables import AUNIO, NOTES as PRIOR
from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_ies_early_literature_review import PDF_URL, RATINGS, SHA, SOURCE


PRIOR_SHA = '1e3069fa3862407ce866badccff0f89da85cd521ab3a1b60546fe2528b310c82'
NOTES = 'data/literature_evidence/IES_EARLY_2013_instruction_study_tables_review_notes.json'
SIEGLER = 'https://siegler.tc.columbia.edu/wp-content/uploads/2020/10/How-does-change-occure-1995.pdf#page=15'
PAGES = list(range(109, 138))
SCOPE = '가이드 PDF 165쪽 중 누적 텍스트 139쪽과 이미지 90쪽을 대조했다. 부록 D의 남은 표 D.6~D.8과 관련 설명·주석 29쪽을 확인했다. 별도 WWC 2.1 절차의 9쪽 텍스트 검토도 유지한다.'
LIMITS = ('가이드의 남은 미주·참고문헌 26쪽, 인용 원연구의 미확인 범위, 표 사이의 미해결 차이는 후속이다. '
          '권고 3~5의 당시 Minimal 등급을 유지한다. 국내 자체 관찰 과제의 효과나 진단 타당성은 별도 검증이 필요하다.')

# Counts reflect printed outcomes, including results with no effect size reported.
D6 = [
    (110, 2, 3), (111, 4, 9), (112, 4, 10), (113, 3, 12), (114, 1, 1),
]
D7 = [
    (118, 4, 5), (119, 4, 10), (120, 4, 10), (121, 3, 12), (122, 5, 5),
]
D8 = [
    (127, 2, 4), (128, 3, 9), (129, 4, 9), (130, 4, 10), (131, 4, 8),
    (132, 2, 12), (133, 4, 9), (134, 2, 12), (135, 1, 1),
]
CORRECTIONS = [
    dict(status='pcer_chapter_2_common_comparison_documented', locations=['PDF 83', 'PDF 109', 'PDF 113'],
         issue='D.3 표만으로 구별하지 못한 PCER 2장의 비교 집단을 본문에서 확인했다. 두 개입은 동일한 정규 수업 비교군에 대비된다.',
         comparison_arm_reported_n=100, comparisons=2),
    dict(status='dyson_and_jordan_maintenance_windows_distinguished', locations=['PDF 109', 'PDF 111–112'],
         issue='본문은 두 추가 수학 연구의 유지 검사를 6주로 요약한다. D.6은 Dyson 6주, Jordan 8주를 기록한다. Dyson의 연산 합계 유지 결과 0.18 ns도 뚜렷하지 않음으로 분류한다.',
         followup='비교별 시점과 척도를 사용한다. 두 연구 전체의 연산 유지 효과가 긍정적이었다고 인용하지 않는다.'),
    dict(status='siegler_feedback_procedure_corrected', locations=['PDF 117', 'PDF 122', 'PDF 124 notes 27–29', SIEGLER],
         issue='가이드는 한 집단이 평가자의 이유 설명을 들었다고 쓴다. 원논문 인쇄 239쪽에 따르면 평가자는 정답을 알려 주고, 아이에게 평가자가 어떻게 알았는지 설명해 보게 했다.',
         followup='원연구의 질문 주체와 순서를 사용한다. 자신의 추론을 말한 집단은 피드백 전에 설명했다. 세 비교는 15명씩 배정한 한 실험의 세 집단에서 나온다.'),
    dict(status='klein_footnote_year_discrepancy', locations=['PDF 120', 'PDF 124 note 23', 'https://ies.ed.gov/ncee/wwc/study/77968'],
         issue='D.7의 278명 비교 본행은 Klein 외 2008, 연결 미주 23은 2011로 인쇄됐다. WWC 연구 기록은 같은 프로그램 비교와 분석 278명을 2008 연구로 기록한다.',
         followup='이 행의 서지는 2008로 연결하고 인쇄된 미주 연도는 보존한다.'),
    dict(status='aunio_counting_significance_open', locations=['PDF 82', 'PDF 127', AUNIO],
         issue='Aunio의 직후 ENT 셈 척도는 두 표에서 효과크기 0.87이 같으나 D.3은 ns, D.8은 *다. 원논문은 직후 셈 척도의 집단 차이에 유의성을 보고한다.',
         followup='가이드의 개별 군집·다중비교 보정 내역을 확인하기 전 하나의 유의성 표기로 통합하지 않는다.'),
    dict(status='d8_repeated_number_line_effect_note_verified', locations=['PDF 92', 'PDF 133', 'PDF 137 note 31'],
         issue='D.4에 미주 25가 붙은 0.86*가 D.8에서는 31과 연결된다. 미주 31은 낮을수록 좋은 추정 오차를 양의 효과로 표시한 이유를 설명한다.'),
    dict(status='d8_nonsignificant_footnote_pointers_open', locations=['PDF 133–134', 'PDF 136 note 24', 'PDF 137 notes 34–35'],
         issue='Ramani·Siegler(2011) 정답률 ns의 미주 24는 Monahan 비교를, Siegler·Ramani(2009) 일부 ns의 미주 34는 Sarama 하위척도를 설명한다. 미주 35는 미보고 효과크기를 다룬다.',
         followup='표가 비워 둔 효과크기는 미보고 상태로 둔다. 인쇄 번호와 내용상 관련 후보를 구별한다.'),
    dict(status='monahan_arm_counts_open', locations=['PDF 91', 'PDF 130–131', 'PDF 136–137 notes 23–26', 'https://ies.ed.gov/ncee/wwc/Study/78066'],
         issue='같은 Monahan 연구에서 D.4의 이야기 집단은 42명이고 D.8 이야기 대 수학 비교는 중재 41명, 비교 42명으로 인쇄됐다. 움직임도 표별 39명과 37명이다.',
         followup='D.4는 책읽기와 비교하고 D.8은 수학 중재 방식끼리 비교한다. 원논문의 분석 표본을 대조할 때까지 집단 수를 바꾸거나 통합하지 않는다.'),
]

OBS = [
    dict(id='IE-P12', standard_codes=['2수01-01'],
         question='단추가 놓인 판의 개수를 세고, 어떻게 한 번씩 셌는지 말해 보자. 세어 본 단추를 표시하는 방법을 한 가지 본 뒤, 배열이 다른 두 번째 판에서도 개수를 세어 보자. 두 판에서 어떤 방법을 썼는가?',
         expected='단추 하나에 수 이름 하나를 대응하고 마지막 수로 전체 개수를 말한다. 첫 시도와 도움 뒤 시도에서 건너뛰거나 두 번 세는 경우가 줄었는지 설명한다.',
         interpretation='각 판에 단추 8개를 놓고 수는 미리 알려 주지 않는다. 최초 방법, 제공한 도움, 배열이 바뀐 뒤 방법을 따로 기록한다. 도움이 줄어도 일대일 대응이 유지되는지 새 판으로 다시 관찰한다.',
         student_validated=False),
    dict(id='IE-P13', standard_codes=['2수01-01'],
         question='단추 6개씩 두 줄을 놓고 한 줄의 간격만 넓혔다. 어느 줄이 더 많은가? 교사가 “두 줄은 개수가 같아”라고 판단했다. 교사는 무엇을 보고 그렇게 판단했을까? 한 줄에 단추 한 개를 더 놓으면 답이 어떻게 바뀌는가?',
         expected='간격만 바꾸면 추가하거나 뺀 단추가 없어서 두 줄 모두 6개다. 한 줄에 단추를 실제로 더하면 그 줄이 7개가 되어 더 많다.',
         interpretation='정답을 듣기 전 최초 판단, 정답을 들은 뒤 이유를 스스로 설명한 반응, 실제 추가 상황의 설명을 따로 기록한다. 필요하면 두 줄을 일대일로 다시 대응해 확인한다.',
         student_validated=False),
    dict(id='IE-P14', standard_codes=['2수01-01','2수01-03'],
         question='1부터 10까지 적힌 한 줄 판에서 말이 4에 있다. 두 칸 앞으로 움직이며 밟는 수를 말하자. 놀이를 마친 뒤 판을 가리고 6과 8 중 어느 수가 더 큰지, 6 다음 수가 무엇인지 각각 설명하자.',
         expected='5와 6을 밟아 6에 도착한다. 6보다 8이 크고 6 다음 수는 7이다. 같은 방향으로 갈 때 수가 1씩 커짐을 설명할 수 있다.',
         interpretation='출발 칸을 다시 세는지, 놀이판을 보며 이동하는지, 판 없이 순서와 크기를 판단하는지를 따로 관찰한다. 한 자리 수 과제로 네 자리 수 전체를 평가하지 않는다.',
         student_validated=False),
]
MAPPINGS = [
    ('IE16', 3, [109, 110, 111, 112, 115], [],
     'D.6은 진행 관찰로 수업을 조정한 활동과 아이가 이미 아는 것에서 출발하는 활동을 구분한다. EPIC와 DLM은 둘 다 진행을 관찰했다. 같은 개수에서 배열을 바꿔 도움 전후의 셈 방법을 확인하는 기록에 참고한다.',
     '권고 3은 Minimal이다. 추가 수업 시간, 수업 내용, 비교군의 기존 관찰이 함께 달라 자체 발문이나 진행 관찰만의 효과를 분리할 수 없다.'),
    ('IE17', 4, [117, 122, 124], [SIEGLER],
     'Siegler의 원연구에서 한 집단은 교사가 알려 준 답에 대해 교사가 어떻게 판단했는지 직접 설명했다. 두 줄의 간격과 단추 수를 구별할 때 학생의 처음 판단과 정답을 들은 뒤의 이유 설명을 분리하는 데 참고한다.',
     '권고 4는 Minimal이다. 한 유아 수 보존 실험의 세 집단 비교이고 각 설명의 순서도 다르다. 설명을 듣기만 하는 방식이나 국내 과제의 효과를 검증한 결과는 아니다.'),
    ('IE18', 5, [125, 127, 132, 133, 134, 137], [],
     'D.8은 숫자판과 색깔판, 선형·원형 숫자판과 별도 수 활동을 비교한 연구를 나누어 싣는다. 말의 이동, 판 없이 다음 수 찾기, 크기 비교를 별도 과제로 관찰하는 데 참고한다.',
     '권고 5는 Minimal이다. 결과는 비교군과 척도마다 다르며, 놀이를 포함한 전체 지도와 놀이만의 비교가 섞여 있다. 한 자리 수 활동으로 네 자리 수 전체나 매일 놀이의 효과를 판단하지 않는다.'),
]


def table_summary(citations, page_rows, contrasts, outcomes):
    assert sum(row[1] for row in page_rows) == contrasts
    assert sum(row[2] for row in page_rows) == outcomes
    return dict(citation_or_chapter_units=citations, comparison_blocks=contrasts, printed_outcome_rows=outcomes,
                pages=[dict(pdf_page=p, comparisons_started=c, printed_outcome_rows=o) for p,c,o in page_rows],
                participants_are_not_summed=True, repeated_comparisons_across_tables_are_not_independent=True)


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['reading_extension']['file'] == NOTES:
        assert source['observations'][-3:] == OBS
        assert {row[0] for row in MAPPINGS} <= {claim['id'] for claim in registry['claims']}
        build_report()
        return
    assert source['reading_extension'] == dict(file=PRIOR, sha256=PRIOR_SHA)
    assert sha(ROOT / PRIOR) == PRIOR_SHA and sha(ROOT / source['snapshot_file']) == SHA
    assert not set(PAGES) & set(source['text_pdf_pages'])
    text_pages = sorted(source['text_pdf_pages'] + PAGES)
    visual_pages = sorted(set(source['visual_pdf_pages']) | set(PAGES))
    assert (len(text_pages), len(visual_pages)) == (139, 90)
    log = [
        'PDF 109~115의 D.6 설명·표·주석에서 비교 14개와 결과 35행을 대조했다. Arnold와 Rightstart는 표 제목과 달리 진행 관찰 열이 비어 있고 출발 지식 열에만 ?가 있다. ?는 비교군의 수업 정보가 부족함을 나타낸다.',
        'PDF 116~124의 D.7에서 비교 20개와 결과 42행을 대조했다. 수학 대화·어휘·비형식 지식의 표현을 구별했다. Fuchs 외의 같은 정규 교육과정에 추가한 짝 활동은 SESAT 0.28 ns, SAT-P 0.12 ns다. SAT-P 사전검사는 SESAT으로 대체했다.',
        'PDF 125~137의 D.8에서 비교 26개와 결과 74행을 대조했다. PDF 127~128에 걸친 Aunio 결과는 한 비교에 속한다. 정기 수학 14·일과 통합 11·게임 6은 20개 연구에 중복되는 구성이다.',
    ]
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    corrections = source['source_discrepancies'] + CORRECTIONS
    notes = dict(
        source_id=SOURCE, source_url=source['display']['url'], source_pdf_sha256=SHA,
        contains_source_full_text=False, licensed_source_pdf_preserved=True,
        previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_reading_extension=dict(file=PRIOR, sha256=PRIOR_SHA),
        cumulative_read_scope=SCOPE, cumulative_text_pdf_pages=text_pages, cumulative_visual_pdf_pages=visual_pages,
        new_text_pdf_pages=PAGES, new_visual_pdf_pages=PAGES,
        unread_full_pdf_pages=sorted(set(range(1,166))-set(text_pages)), reading_log=log,
        new_image_sha256={str(p): sha(ROOT / f'tmp/literature/ies-early-appendix-review/page-{p}.png') for p in PAGES},
        evidence_ratings=RATINGS, source_corrections=corrections,
        table_d6=table_summary(12,D6,14,35), table_d7=table_summary(16,D7,20,42), table_d8=table_summary(20,D8,26,74),
        selected_d6_conditions=dict(epic_and_dlm_both_monitored=True, dyson_additional_math_hours=12,
                                    dyson_regular_curriculum_monitored=True, jordan_math_connects_monitoring_confirmed=False,
                                    jordan_followup_weeks=8, dyson_followup_weeks=6),
        selected_d7_conditions=dict(siegler_total_randomized=45, group_size=15,
                                    own_reasoning_before_feedback=True, child_explains_examiner_reasoning_after_feedback=True,
                                    own_vs_feedback=-0.60, examiner_vs_feedback=0.30, own_vs_examiner=-0.88),
        selected_d8_conditions=dict(regular_math_studies=14, integration_studies=11, game_studies=6,
                                    components_can_overlap=True, ramani_siegler_2011_total=88,
                                    ramani_siegler_2011_linear_contrast_total=59, ramani_siegler_2011_circular_contrast_total=58),
    )
    write(ROOT / NOTES, notes)
    source.update(date='2026-11-09', bibliography_snapshot=digest(entry),
                  reading_extension=dict(file=NOTES, sha256=sha(ROOT / NOTES)),
                  text_pdf_pages=text_pages, visual_pdf_pages=visual_pages, read_scope=SCOPE, limits=LIMITS,
                  reading_log=source['reading_log'] + log, source_discrepancies=corrections,
                  editorial_action='표 D.6~D.8의 비교 조건을 대조해 문헌 대응 3건과 자체 관찰 과제 3개를 추가했다.',
                  observations=source['observations'] + OBS)
    for observation, (cid, number, pages, extra, support, limit) in zip(OBS, MAPPINGS, strict=True):
        codes = observation['standard_codes']
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='instructional_recommendation_with_evidence_scope',
            locations=[f'{PDF_URL}#page={p}' for p in pages] + extra,
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
    print('Registered D.6 through D.8, three scoped claims, and three observation tasks.')


if __name__ == '__main__':
    main()

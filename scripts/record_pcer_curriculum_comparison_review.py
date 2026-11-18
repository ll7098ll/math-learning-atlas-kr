"""Link the original PCER comparisons to the scopes reported in the IES guide."""
import shutil

from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_ies_early_literature_review import PDF_URL as GUIDE


SOURCE = 'PCER_2008_CHAPTERS_2_3'
URL = 'https://ies.ed.gov/sites/default/files/migrated/nces_pubs/ncer/pubs/20082009/pdf/20082009_rev.pdf'
BRIGHT = 'https://ies.ed.gov/ncee/wwc/Docs/InterventionReports/wwc_brightbeginnings_030513.pdf'
CREATIVE = 'https://ies.ed.gov/ncee/wwc/Docs/InterventionReports/wwc_creativecurriculum_030513.pdf'
SHA = 'f6e68860c47d6377e4d1ec23f72a6806348b3a5fa159242565b8aea4258b2101'
CACHE = ROOT / 'tmp/literature/pcer-2008-revised'
PDF = f'data/literature_evidence/{SOURCE}.pdf'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
PAGES = [1, 3, 58, 88, *range(92,116), 381, 383, 385, 413, 415, 417]
SCOPE = ('PCER 2008 개정 원보고서 442쪽 중 제2·3장 인쇄 41~64쪽 전체와 표지·발행 정보·배정·검출력·부록 자료표를 포함한 선정 34쪽의 텍스트와 이미지를 대조했다. '
         '세 비교의 수학 결과를 2013년 WWC 보고서 및 가이드 표 D.3과 대조했다.')
LIMITS = ('두 연구팀의 프로그램 묶음 비교에 한정한다. 다른 연구팀과 장, 개별 학생의 원자료, 단일 수업 요소, 국내 과제의 효과는 별도 검토 범위다. '
          '유의한 차이를 확인하지 못한 결과는 동일 효과의 입증으로 사용할 수 없다.')
EMPIRICAL_SCOPE = dict(
    design='randomized_program_comparisons_with_classroom_assignment',
    sample_description='Tennessee의 21학급·309명 기초 표본에서 두 개입이 공통 비교군을 사용했다. NC·GA의 18학급·194명은 별도 표본이다.',
    inference_limit='학교·학급 단위와 검사별 아동 응답 수를 구별하며 국내 개별 수업의 효과로 옮기지 않는다.',
    student_outcome_study=True, causal_effect_established=False, local_effect_tested=False,
)

# Test rows are in WJ Applied Problems, CMA-A composite, Shape Composition order.
COMPARISONS = [
    dict(chapter=2, site='Tennessee', program='Bright Beginnings', effect_table='2.4', pdf_page=101,
         original_demographic_arm_counts=[103,105], guide_reported_pre_k_n=198,
         pre_k_spring_n=[[98,100],[98,100],[98,100]], kindergarten_spring_n=[[100,104],[100,103],[100,104]],
         pre_k_spring_effects=[0.16,0.14,-0.03], kindergarten_spring_effects=[0.13,0.07,0.15],
         guide_lists_kindergarten=False, shared_comparison_id='TN-regular'),
    dict(chapter=2, site='Tennessee', program='Creative Curriculum', effect_table='2.5', pdf_page=105,
         original_demographic_arm_counts=[101,105], guide_reported_pre_k_n=193,
         pre_k_spring_n=[[93,100],[93,100],[93,100]], kindergarten_spring_n=[[96,104],[96,103],[96,104]],
         pre_k_spring_effects=[0.17,0.10,-0.12], kindergarten_spring_effects=[0.17,0.05,0.00],
         guide_lists_kindergarten=False, shared_comparison_id='TN-regular'),
    dict(chapter=3, site='North Carolina and Georgia', program='Creative Curriculum', effect_table='3.4', pdf_page=115,
         original_demographic_arm_counts=[97,97], guide_reported_pre_k_n=170,
         pre_k_spring_n=[[89,80],[90,80],[89,80]], kindergarten_spring_n=[[85,76],[85,76],[85,76]],
         pre_k_spring_effects=[0.20,-0.10,0.19], kindergarten_spring_effects=[0.09,0.14,-0.01],
         guide_lists_kindergarten=True, shared_comparison_id='NC-GA-regular'),
]
CORRECTIONS = [
    dict(status='shared_control_and_measure_specific_counts_verified', locations=[f'{URL}#page=58', f'{URL}#page=93', f'{URL}#page=381', f'{URL}#page=383', f'{URL}#page=385', f'{GUIDE}#page=83'],
         issue='2장의 두 비교는 같은 정규 수업 집단을 썼다. 3장의 170명은 CMA-A에 해당하며 취학 전 봄의 WJ 응용과 도형 합성 응답은 각각 169명이다.',
         followup='등록·추적 인원과 검사별 응답, 두 비교의 공통 비교군을 구별한다. 표에 나온 여러 비교의 인원을 합산하지 않는다.'),
    dict(status='bright_beginnings_classroom_observation_timing_discrepancy', locations=[f'{URL}#page=99', f'{URL}#page=100', f'{URL}#page=101'],
         issue='인쇄 49쪽의 Arnett 봄 관찰 문장은 유치원 봄이라고 쓰지만 바로 앞 방법과 표 2.4 주석은 교실 수준 자료가 취학 전 학년에만 수집되었다고 설명한다.',
         followup='학생 유치원 추적과 교실 수준 결과를 구별한다. 후속 교실 측정으로 인용하기 전 원자료나 정오표를 대조한다.'),
    dict(status='creative_standards_ratings_separated_by_review', locations=[CREATIVE, f'{GUIDE}#page=83'],
         issue='2013년 3월 WWC Creative Curriculum 보고서는 PCER 2장에 유보를, 3장에는 유보 없이 기준 충족을 부여한다. 11월 가이드 D.3에서는 두 장에 유보를 적는다.',
         followup='각 판정을 검토 문서와 시점으로 구별한다. 이 차이만으로 어느 기준 적용이 틀렸다고 단정하지 않는다.'),
]
MAPPINGS = [
    ('PCER01', ['2수01-05'], [58,93,98,101,102,105,381,383], [BRIGHT, CREATIVE],
     'Tennessee 두 프로그램의 취학 전 봄 WJ 응용 문제 효과크기는 0.16과 0.17이고 두 결과에서 유의한 차이가 확인되지 않았다. 두 비교는 같은 비교군을 썼다. 분석 표본 198명과 193명에는 그 비교군 100명이 각각 들어 있다.',
     'WJ 응용 문제 전체 결과에 해당한다. 덧셈·뺄셈 상황의 개별 유형이나 국내 성취기준의 수행을 따로 검증한 결과는 아니다.'),
    ('PCER02', ['2수03-03','4수03-04'], [106,111,115,385,417], [CREATIVE],
     'NC·GA의 도형 합성 효과크기는 취학 전 봄 0.19, 유치원 봄 −0.01이며 두 시점 모두 유의한 차이가 확인되지 않았다. 취학 전 도형 합성 응답은 169명으로 같은 표의 CMA-A 응답 170명과 다르다.',
     '여러 구성 요소가 포함된 프로그램 비교다. 조각을 밀기·뒤집기·돌리기 중 어떤 동작이 달라졌는지나 국내 도형 구성 과제의 효과는 확인하지 않았다.'),
    ('PCER03', ['2수03-03'], [88,110,111,113,115], [],
     'NC·GA에서 교실 전반의 질은 긍정적 결과가 있었고 아동 수학 검사 세 가지와 교실 수학 지도 관찰에서는 유의한 차이가 확인되지 않았다. 교실 환경, 관찰한 지도, 아동이 수행한 검사를 서로 다른 기록으로 해석한다.',
     '보고서의 수학 합성 척도 검출력 범위는 개별 검사에 대한 동등성 기준이 아니다. 교실 관찰 점수를 아동의 도형 이해에 대한 직접 평가로 사용할 수 없다.'),
]


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert registry['sources'][SOURCE]['snapshot_sha256'] == SHA
        assert {row[0] for row in MAPPINGS} <= {claim['id'] for claim in registry['claims']}
        build_report()
        return
    raw = CACHE / 'source.pdf'
    reader = PdfReader(raw)
    assert sha(raw) == SHA and len(reader.pages) == 442
    assert len(PAGES) == len(set(PAGES)) == 34
    license_statement = 'This report is in the public domain.'
    assert license_statement in reader.pages[2].extract_text()
    assert [sum(pair) for pair in COMPARISONS[2]['pre_k_spring_n']] == [169,170,169]
    assert all(all(sum(pair) == row['guide_reported_pre_k_n'] for pair in row['pre_k_spring_n']) for row in COMPARISONS[:2])
    assert COMPARISONS[0]['shared_comparison_id'] == COMPARISONS[1]['shared_comparison_id'] != COMPARISONS[2]['shared_comparison_id']
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = dict(id=SOURCE,title='Effects of Preschool Curriculum Programs on School Readiness',
                 authors=['Preschool Curriculum Evaluation Research Consortium'],year=2008,
                 kind='유아 교육과정 무작위 배정 연구 보고서 제2·3장',url=URL,review_scope=SCOPE,next_review=LIMITS,
                 supports=['두 연구팀의 비교 설계와 결과별 분모','아동 수학 평가와 교실 관찰의 구별'],
                 does_not_establish=LIMITS)
    assert all(row['id'] != SOURCE for row in bibliography)
    bibliography.append(entry)
    log = [
        'PDF 1·3·58·88에서 판본과 공공 영역 선언, 무작위 배정 단위, 검출력 가정과 집계 범위를 확인했다.',
        'PDF 92~105의 Tennessee 제2장에서 두 프로그램 설명, 표본 및 공통 비교군, 파일럿 뒤 학급 대체, 관찰 시기와 아동·교실 결과를 확인했다.',
        'PDF 106~115의 NC·GA 제3장에서 별도 배정·응답 표본, 교실 환경과 아동 수학 세 검사의 결과를 확인했다.',
        'PDF 381·383·385의 부록 C에서 비조정 점수와 시점별 검사 응답 수를, PDF 413·415·417의 부록 D에서 조정 평균 차이와 표준오차를 각각 대조했다.',
    ]
    notes = dict(
        source_id=SOURCE, source_url=URL, source_pdf_sha256=SHA, contains_source_full_text=False,
        licensed_source_pdf_preserved=True, cumulative_read_scope=SCOPE, cumulative_text_pdf_pages=PAGES,
        cumulative_visual_pdf_pages=PAGES, reading_log=log, source_corrections=CORRECTIONS,
        image_sha256={str(page):sha(CACHE/f'page-{page:03d}.png') for page in PAGES},
        chapter_2=dict(local_recruited_classrooms=36, local_recruited_children=558, national_classrooms=21,
                       national_baseline_children=309, common_comparison_baseline_children=105,
                       common_comparison_spring_math_children=100, replacement_classrooms_after_pilot=8),
        chapter_3=dict(baseline_classrooms=18, recruited_children=194, baseline_child_assessment_responses=190,
                       kindergarten_child_assessment_responses=162, spring_followup_battery_wwc_children=171,
                       student_math_assessment_significant=False, classroom_ecers_r_effect=1.66,
                       classroom_ecers_r_significant=True, classroom_tbrs_math_effect=0.75,
                       classroom_tbrs_math_significant=False),
        measures=['WJ Applied Problems','CMA-A Mathematics Composite','Building Blocks Shape Composition'],
        mathematics_comparisons=COMPARISONS, any_listed_math_effect_statistically_significant=False,
        minimum_detectable_math_composite_effects=dict(tennessee=[0.49,0.60], nc_ga=[0.48,0.56], alpha=0.05, icc=[0.05,0.15]),
        participant_counts_are_not_summed_across_comparisons=True,
    )
    path = ROOT / PDF
    if path.exists():
        assert sha(path) == SHA
    else:
        shutil.copyfile(raw,path)
    write(ROOT / NOTES,notes)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-09',
        snapshot_kind='source_pdf',snapshot_file=PDF,snapshot_sha256=SHA,source_pdf_url=URL,pdf_pages_total=442,
        redistribution_license='Public domain (explicit report declaration)',license_location='PDF 3',license_statement=license_statement,
        bibliography_snapshot=digest(entry),display=dict(title=entry['title'],url=URL,authors_year='PCER Consortium, 2008'),
        text_pdf_pages=PAGES,visual_pdf_pages=PAGES,read_scope=SCOPE,reading_log=log,limits=LIMITS,empirical_scope=EMPIRICAL_SCOPE,
        reading_extension=dict(file=NOTES,sha256=sha(ROOT / NOTES)),source_discrepancies=CORRECTIONS,
        scope_note='두 연구팀이 수행한 세 프로그램 비교와 실제 측정한 결과를 구별한다.',
        method_note='표준화 효과크기, 비조정 원점수의 응답 수, 조정 평균 차이, 수업 관찰을 별도 원문 표에서 확인했다.',
        editorial_action='공통 비교군·검사별 응답·아동 수행과 교실 관찰을 구별해 문헌 근거 3건을 추가했다.',
        independent_review=False,student_validated=False,observations=[],
    )
    for cid,codes,pages,extra,support,limit in MAPPINGS:
        registry['claims'].append(dict(
            id=cid,source_id=SOURCE,role='empirical_result_with_scope',standard_codes=codes,
            locations=[f'{URL}#page={page}' for page in pages]+extra,support=support,does_not_establish=limit,
            independent_review=False,student_validated=False,empirical_scope=EMPIRICAL_SCOPE,
            target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    queue['literature_review'].append(dict(
        source=entry,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',
        claim_evidence_fields=['공통 비교군','검사별 응답과 효과','교실 관찰과 아동 성취'],claim_ids=[row[0] for row in MAPPINGS],
    ))
    write(bibliography_path,bibliography)
    write(ROOT / 'data/literature_claim_reviews.json',registry)
    write(queue_path,queue)
    build_report()
    print('Registered the PCER original report chapters with three scoped claims.')


if __name__ == '__main__':
    main()

"""Extend the existing PCER report review with the California/New York comparison."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_pcer_curriculum_comparison_review import PDF, SHA, SOURCE, URL


CACHE = ROOT / 'tmp/literature/prekmath-pcer-klein'
NOTES = f'data/literature_evidence/{SOURCE}_chapter_10_review_notes.json'
WWC = 'https://ies.ed.gov/ncee/WWC/Docs/InterventionReports/wwc_prekmath_121713.pdf'
WWC_SHA = '85ca5226cd30ca20d3fd29f973540e79144797ac6667b71e0926f0a856b05abd'
TEXT = [*range(182, 194), 309, 310, 314, 403, 435]
VISUAL = [184, 189, 190, 193, 310, 314, 403, 435]
WWC_VISUAL = [7, 16, 18]
SCOPE = ('개정 PCER 보고서 제2·3장과 제10장 및 관련 부록을 대조했다. '
         '제10장은 인쇄 131~142쪽과 선정 부록 5쪽의 텍스트, 선정 8쪽의 이미지를 확인했다. '
         '2013 WWC의 별도 개입 보고로 코호트와 분석 방식을 대조했다.')
LIMITS = ('연구팀과 비교별 배정·분모·측정·분석 범위를 유지한다. PDF의 다른 장, Klein 원논문 전체, '
          '개별 수업 요소의 효과와 국내 과제 효과는 별도 확인 범위다.')
CH10_SCOPE = dict(
    design='classroom_assignment_with_post_pilot_replacements',
    sample_description='California·New York의 40교실에서 316명을 모집했다. 2003~04년 취학 전 봄 수학 검사 응답은 296~297명이다.',
    inference_limit='2년차 비교에서 교사가 교체됐고 WWC는 유보를 붙였다. 중재는 소집단·가정 활동과 소프트웨어의 묶음이다.',
    student_outcome_study=True, causal_effect_established=False, local_effect_tested=False,
)
CORRECTIONS = [
    dict(location=f'{URL}#page=184', issue='표 10.1의 전체 비교군 평균 연령을 44.4세로 인쇄했다. 본문은 전체 평균 4.3세, 두 지역 비교군은 4.4세와 4.3세로 제시한다.',
         followup='44.4를 연구 표본의 연령으로 사용하지 않는다. 반올림한 하위 평균으로 정확한 전체 비교군 값을 복원하지 않는다.'),
    dict(location=f'{URL}#page=190', issue='유치원 봄 수학 전반의 요약은 뚜렷한 효과가 없었다고 적었지만 도형 합성 개별 검사는 표 10.4에서 .41, p<.001이다.',
         followup='포괄 요약과 개별 검사 결과를 별도로 인용한다.'),
    dict(location=f'{URL}#page=310', issue='부록 본문의 유치원 봄 도형 합성 효과크기 자리에 p<.001만 인쇄됐다.',
         followup='수치 .41은 표 10.4와 A-18의 반복측정 열을 출처로 사용한다.'),
    dict(location=f'{WWC}#page=16', issue='WWC 부록 C.4는 .91에 p>0.01을 인쇄했다. 참조하는 PCER 표 A-18의 ANCOVA .91에는 p<.0001에 해당하는 별 네 개가 있다.',
         followup='WWC 본문의 유의 판정은 기록하되 두 문서의 p 표기를 바꾸거나 같은 값으로 옮기지 않는다.'),
]
CLAIMS = [
    ('PCER04', ['2수01-01', '2수03-03'], [182, 186, 187, 403], [f'{WWC}#page=18'],
     'Klein의 1년차 278명과 PCER 제10장의 2년차 최대 297명은 서로 다른 아동 코호트다. 교사 33명이 양쪽에 참여했고 2년차에 7명이 교체됐다. 제10장의 취학 전 봄 WJ 응답은 296명, CMA-A와 도형 합성은 각각 297명이다.',
     '아동 표본을 같은 아이로 간주할 수 없고 교사까지 독립이라고 가정할 수도 없다. 제10장의 316명은 모집 인원이다.'),
    ('PCER05', ['2수03-03', '4수03-04', '4수03-12'], [189, 190, 193, 310, 314, 403], [],
     '제10장 도형 합성의 반복측정 효과크기는 취학 전 봄 .96, 유치원 봄 .41이며 두 결과 모두 p<.001이다. 유치원 봄 ANCOVA 값은 .30이다. 가을의 .25와 개입 시작 시점으로 역추정한 .08을 구별했다.',
     '유치원 봄 수학 전체 요약과 도형 합성 검사의 결과는 적용 범위가 다르다. 역추정값은 실제 개입 전 관측이 아니며 도형 합성 결과를 회전의 단독 효과로 해석할 수 없다.'),
    ('PCER06', ['2수01-05', '2수03-03'], [189, 193, 314, 403], [f'{WWC}#page=7', f'{WWC}#page=16', f'{WWC}#page=17'],
     'PCER 반복측정에서 취학 전 봄 CMA-A는 .44로 유의했다. 2013 WWC는 같은 코호트의 ANCOVA .35를 사용했고 다중 비교 보정 후 유의하다고 보지 않았다. WJ 응용은 양쪽에서 뚜렷하지 않았으며 WWC는 도형 합성의 유의를 확인했다.',
     '같은 데이터의 모형과 판정 차이를 독립 재현으로 합산하지 않는다. WJ와 CMA-A 총점에서 개별 덧셈·뺄셈 발문의 효과를 분리할 수 없다.'),
    ('PCER07', ['2수01-01', '2수03-03'], [182, 188, 191, 192, 193], [],
     '교사는 소집단 활동에서 기록지를 썼고 가정·컴퓨터 활동도 같은 주제와 연결했다. 취학 전 봄 교실 수학 지도 관찰 TBRS의 효과크기는 .57로 유의한 차이가 확인되지 않았다. 교실 관찰과 학생 도형 과제는 다른 척도다.',
     '교실 관찰 결과로 아동 도형 검사 결과를 대신할 수 없다. 기록지·가정 자료·소프트웨어만의 효과는 별도 실험이 필요하다.'),
]


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    existing = {claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE}
    new_ids = [row[0] for row in CLAIMS]
    if set(new_ids) <= existing:
        assert source['reading_extension']['file'] == NOTES
        build_report()
        return
    assert existing == {'PCER01', 'PCER02', 'PCER03'} and not set(new_ids) & existing
    report = ROOT / PDF
    review = CACHE / 'wwc-prekmath-2013.pdf'
    assert sha(report) == SHA and sha(review) == WWC_SHA
    reader, wwc_reader = PdfReader(report), PdfReader(review)
    assert len(reader.pages) == 442 and len(wwc_reader.pages) == 20
    assert all(value in reader.pages[192].extract_text() for value in ('.44', '.96', '.41'))
    assert all(value in wwc_reader.pages[15].extract_text() for value in ('0.35', '0.91', '297 children'))
    responses = dict(pre_k_spring=[[148, 148], [148, 149], [148, 149]], kindergarten_spring=[[145, 139]] * 3)
    assert [sum(pair) for pair in responses['pre_k_spring']] == [296, 297, 297]
    assert all(sum(pair) == 284 for pair in responses['kindergarten_spring'])

    previous = source['reading_extension']
    old_notes = load(ROOT / previous['file'])
    text_pages = sorted(set(source['text_pdf_pages']) | set(TEXT))
    visual_pages = sorted(set(source['visual_pdf_pages']) | set(VISUAL))
    logs = source['reading_log'] + [
        '제10장 PDF 182~193의 배정·교체·세 수학 검사·교실 관찰과 관련 부록을 확인했다.',
        '2013 WWC는 1년차와 2년차의 아동 코호트를 분리하고, 제10장에 ANCOVA와 다중 비교 보정을 사용했다.',
    ]
    notes = dict(
        source_id=SOURCE, source_url=URL, source_pdf_sha256=SHA, contains_source_full_text=False,
        licensed_source_pdf_preserved=True, previous_reading=previous,
        cumulative_read_scope=SCOPE, cumulative_text_pdf_pages=text_pages, cumulative_visual_pdf_pages=visual_pages,
        reading_log=logs, source_corrections=source['source_discrepancies'] + CORRECTIONS,
        image_sha256=old_notes['image_sha256'] | {str(page): sha(CACHE / f'pcer-page-{page}.png') for page in VISUAL},
        chapter_10=dict(
            recruited_children=316, recruited_by_arm=[159, 157], evaluation_classrooms=40,
            teacher_overlap_with_pilot=33, replaced_teachers=7, pilot_klein_analyzed_children=278,
            measures=['WJ Applied Problems', 'CMA-A Mathematics Composite', 'Building Blocks Shape Composition'],
            responses_by_arm=responses, rm_effects=dict(pre_k_spring=[.22, .44, .96], kindergarten_spring=[.13, .13, .41]),
            ancova_effects=dict(pre_k_spring=[.16, .35, .91], kindergarten_spring=[.05, .10, .30]),
            shape_rm_start_extrapolation=.08, shape_rm_fall_observed=.25, tbrs_math_concepts=.57,
            wwc_pre_k_spring_significant=[False, False, True], wwc_rating='meets_with_reservations',
        ),
        wwc_report=dict(url=WWC, sha256=WWC_SHA, pdf_pages=20, selected_text_pages=[7, 8, 11, 12, 13, 16, 17, 18],
                        visual_pdf_pages=WWC_VISUAL,
                        visual_sha256={str(page): sha(CACHE / f'wwc-page-{page}.png') for page in WWC_VISUAL}),
    )
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography = load(bibliography_path)
    queue = load(queue_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    queue_entry = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    assert queue_entry['source'] == entry
    entry.update(kind='유아 교육과정 무작위 배정 연구 보고서 제2·3·10장', review_scope=SCOPE,
                 next_review=LIMITS, does_not_establish=LIMITS,
                 supports=[*entry['supports'], '코호트 교사 중복과 두 분석의 비교'])
    queue_entry.update(source=entry, claim_ids=queue_entry['claim_ids'] + new_ids,
                       claim_evidence_fields=queue_entry['claim_evidence_fields'] + ['코호트·분석 방법과 보정'])
    source.setdefault('snapshot_history', []).append(dict(snapshot_file=previous['file'], snapshot_sha256=previous['sha256'],
                                                          date=source['date'], read_scope=source['read_scope']))
    # The report now covers different study designs. Scope remains on each claim.
    source.pop('empirical_scope')
    path = ROOT / NOTES
    write(path, notes)
    source.update(bibliography_snapshot=digest(entry), text_pdf_pages=text_pages, visual_pdf_pages=visual_pages,
                  read_scope=SCOPE, limits=LIMITS, reading_log=logs, reading_extension=dict(file=NOTES, sha256=sha(path)),
                  source_discrepancies=notes['source_corrections'],
                  scope_note='연구팀별 비교군과 코호트, 아동·교실 측정과 분석 방법의 차이를 기록한다.',
                  editorial_action='제2·3장의 근거 3건을 보존하고 제10장 근거 4건을 추가했다.')
    for cid, codes, pages, extra, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='empirical_result_with_scope', standard_codes=codes,
            locations=[f'{URL}#page={page}' for page in pages] + extra, support=support, does_not_establish=limit,
            empirical_scope=CH10_SCOPE, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()


if __name__ == '__main__':
    main()

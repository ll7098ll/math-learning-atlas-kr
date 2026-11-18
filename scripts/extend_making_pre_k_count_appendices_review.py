"""Record the MPC appendices, High 5s implementation, and WWC review separately."""
import copy

from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_making_pre_k_count_review import CACHE, GRADE_3, KINDER, FAMILY
from record_wwc_algebra_findings_export import read_export_rows
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


DATE = '2026-11-10'
IMPLEMENTATION = 'JACOB_ERICKSON_MATTERA_2018_HIGH5S_IMPLEMENTATION'
REPORT = 'https://www.mdrc.org/work/publications/launching-kindergarten-math-clubs'
ERIC = 'https://files.eric.ed.gov/fulltext/ED581568.pdf'
WWC = 'https://ies.ed.gov/ncee/wwc/Study/90485'
JOURNAL = 'https://doi.org/10.1080/19345747.2025.2509234'
IMPLEMENTATION_PDF = 'high-5s-implementation-eric-2018'
IMPLEMENTATION_SHA = '6f90c0ff3e84bcbf4c9ec8fb6e1b2e1ddce55a72de73004b07b1408ea0a217af'
WWC_SHA = '759e9acd13900805526d3d9e310783ba6ef610ea1f6941e358698cd62cfe0daf'
KINDER_ID, THIRD_ID = KINDER['id'], GRADE_3['id']
PRIOR = {KINDER_ID: 'fb978e056d3f07262dadb172dd09ee25ce70f4090e5bfdd7933516e4151f0569',
         THIRD_ID: '20c33c6bceb1af270c5d3c7c112aaf331130a3dd511a86f3ee47fefe2d7303ef'}
SCOPES = {
    KINDER_ID: ' 부록 D의 검사 구성과 E의 점수·표본 민감도를 PDF 91~94·97~99쪽에서 추가 확인했다.',
    THIRD_ID: ' 부록 B·F의 분석 모형과 탐색 표를 PDF 65~68·93~95쪽에서 확인했다. WWC 90485의 2026년 심사 3건과 후속 권호 논문에 표시된 3학년 수학 결과를 대조했다.',
    IMPLEMENTATION: 'High 5s 시행 보고서 PDF 26·40~42·46·71쪽에서 활동 예, 출석, 진행자 기록과 관찰, 참여 평정의 범위를 확인했다.',
}
NEXT = {
    KINDER_ID: '검사의 전체 시행·중단 규칙과 항목별 도달 및 응답 자료를 확인한다. 자체 과제의 독립 검토와 학생 검증은 별도다.',
    THIRD_ID: '후속 논문 판면과 원자료, 결측 처리의 심사 산출 기록 및 실제 학생 반응을 확인한다.',
    IMPLEMENTATION: '나머지 활동 예와 운영 순서, 관찰 기록 양식 및 국내 과제의 실제 운영과 학생 반응을 확인한다.',
}

CLAIMS = [
    (KINDER_ID, 'MPC18-06', ['2수01-05', '2수03-03'], [91, 93, 94, 103],
     'REMA-K 48문항과 WJ 응용문제 31문항은 내용 분포가 다르다. 덧셈 예에서 두 묶음의 개수 합과 동전의 값·단위를 해석하는 요구가 다르다. 보고서는 도형 문항에 도달했는지도 도형 하위점수에 영향을 줄 수 있다고 설명한다.',
     '개수의 덧셈, 단위 해석, 도형 문항 제공 여부를 따로 본다. 문항이 제시되지 않은 경우는 그 문항의 오답으로 처리하지 않는다.'),
    (KINDER_ID, 'MPC18-07', ['12실통03-04'], [97, 98, 99],
     '부록 E에서 주 분석 REMA-K T점수는 비유의였고, 로짓·원점수의 효과 크기 .10·.12는 유의였다. High 5s 189명을 제외한 두 민감도 사양의 효과 크기는 모두 약 .09였으며 한 사양만 유의였다. 그림 E.1은 90% 구간이다.',
     '점수 변환과 표본 가중 방식의 비교를 구별한다. 다섯 사양을 독립 연구나 한 효과를 다섯 번 확인한 것으로 세지 않는다.'),
    (THIRD_ID, 'MPC21-05', ['12실통02-02'], [65, 66, 67, 68, 93, 94, 95],
     '부록 B는 아동이 이후 다른 학교로 이동했어도 취학 전 배정 기관과 블록을 모형에 유지한다. 부록 F의 2013·2019년 학교 수준 비교와 표 F.2의 학교 기초 성과 보정은 아동 개인의 추적 반응과 다르다.',
     '학교 평균의 시점별 차이를 같은 학생의 변화로 읽지 않는다. 표 F.2의 제목과 하단 비교 설명의 차이는 표기 그대로 보존한다.'),
    (THIRD_ID, 'MPC21-06', ['12실통03-04'], [27, 32, 42],
     '2021년 보고서 표 3.1의 MPC 단독 3학년 수학 효과 크기 .10의 p는 .19이고, 후속 논문의 .10에는 p=.18이 보고됐다. WWC 90485의 2026년 세 심사는 결측 처리 방식을 이유로 기준 미충족이며 내보내기에 연결된 결과 행은 없다.',
     '보고서 효과 추정과 WWC 설계 판정을 분리한다. 판정 미충족과 결과 행 부재로 효과를 0 또는 비유의로 환산하지 않는다.'),
    (IMPLEMENTATION, 'H5I18-01', ['2수01-05', '2수01-06'], [26, 71],
     'High 5s 활동 예는 카드 두 장의 점을 보고 합을 구하게 하며 모두 세기와 이어 세기를 구별한다. 더 큰 수가 들어 있는 단계에서는 숫자 카드와 점 카드를 사용한다.',
     '활동 예에 전략이 실려 있다는 사실로 아동이 그 전략을 독립적으로 썼다고 판단하지 않는다. 단계 표를 모든 학생의 필수 순서로 적용하지 않는다.'),
    (IMPLEMENTATION, 'H5I18-02', ['2수01-01'], [40, 42, 46],
     '시행 보고서에서 연간 출석률은 87.4%였다. 표 4.2는 예정 회기 7,031회와 게임일을 제외한 운영 지표의 분모 5,971회를 구별한다. 표 4.3은 진행자 기록과 봄 관찰의 참여 평정을 따로 제시한다.',
     '회기 시행, 출석과 참여 평정은 학생의 수 세기 수행 자료와 다르다. 시행 보고서를 같은 프로그램의 별도 효과 연구로 합산하지 않는다.'),
]

OBSERVATIONS = {
    KINDER_ID: [
        dict(id='MPC18-P1', standard_codes=['2수01-05', '2수03-03'],
             question='바구니에 돌이 4개 있고 3개를 더 넣었다. 모두 몇 개인지 설명하라. 다음 도형 문항을 받았을 때만 원, 삼각형, 사각형을 골라 이름을 말하라.',
             expected='돌의 수는 4+3=7개다. 제시된 원, 삼각형, 사각형을 각각 가리켜 이름을 말한다.',
             interpretation='도형을 제시할 때는 이름을 말하지 않는다. 덧셈의 뜻과 도형 문항 제공 여부, 실제 도형 응답을 따로 기록한다. 제시하지 않은 도형 문항은 오답으로 세지 않는다.', student_validated=False),
        dict(id='MPC18-P2', standard_codes=['12실통03-04'],
             question='가상 보고서가 같은 효과에 대해 두 분석의 90% 신뢰구간 [−0.02,0.18]과 [0.01,0.19]를 제시했다. 양측 검정과 짝을 이루는 구간이라면 유의수준 10%에서 효과 0을 기각하는지 설명하라.',
             expected='첫 구간에는 0이 있어 기각하지 않고, 둘째 구간에는 0이 없어 기각한다. 같은 참여 자료로 만든 두 분석이면 두 번의 독립 실험으로 셀 수 없다.',
             interpretation='신뢰수준과 유의수준, 각 구간의 0 포함 여부, 점수·표본을 바꾼 사양인지를 구별한다.', student_validated=False),
    ],
    THIRD_ID: [
        dict(id='MPC21-P1', standard_codes=['12실통02-02'],
             question='가상 학교의 2013년 3학년 평균은 70점, 2019년 3학년 평균은 76점이다. 같은 학생이 6점 올랐는지 답하고, 개인의 변화를 보려면 어떤 자료가 필요한지 설명하라.',
             expected='두 시점의 학교 평균 차이는 6점이다. 같은 학생의 변화인지 확인하려면 같은 학생에게서 비교 가능한 시점별 점수와 검사 조건을 확보해야 한다.',
             interpretation='수집 단위가 학교인지 학생인지, 학생이 시점별로 연결되는지, 검사가 비교 가능한지를 기록한다.', student_validated=False),
        dict(id='MPC21-P2', standard_codes=['12실통03-04'],
             question='가상 분석 A의 p값은 0.19, 분석 B는 0.18이다. 유의수준 5%의 판정을 설명하라. 별도 검토표에 결측 처리 기준 미충족과 결과 미제공이 표시됐을 때 그 칸에 0을 넣어도 되는가?',
             expected='두 p값 모두 0.05보다 크므로 귀무가설을 기각하지 않는다. 결측 처리 판정은 분석 방법에 대한 평가다. 검토표에 결과 수치가 제공되지 않았으므로 효과 0이나 p값 0을 입력할 근거가 없다.',
             interpretation='통계 판정과 자료의 부재, 심사 판정의 차이를 구별한다.', student_validated=False),
    ],
    IMPLEMENTATION: [
        dict(id='H5I-P1', standard_codes=['2수01-05', '2수01-06'],
             question='점 6개와 점 3개가 있는 두 카드를 보고 합을 구하라. 처음 어떻게 셌는지 설명하라. 다음에는 숫자 13 카드와 점 4개 카드에서 합을 구하고, 숫자 13을 다시 점으로 그렸는지 설명하라.',
             expected='첫 합은 9다. 모두 세거나 6을 먼저 잡고 7, 8, 9로 이어 셀 수 있다. 둘째 합은 17이고 13에서 14, 15, 16, 17로 이어 셀 수 있다.',
             interpretation='첫 자발적 전략, 이어 세는 중 추가한 횟수, 교사의 시범과 실제 참여 여부를 따로 적는다.', student_validated=False),
    ],
}


def inspect_pdf(stem, fingerprint, total, text_pages, visual_pages):
    file = CACHE / f'{stem}.pdf'
    assert sha(file) == fingerprint
    reader = PdfReader(file)
    assert len(reader.pages) == total
    assert all(reader.pages[n - 1].extract_text().strip() for n in text_pages)
    return {str(n): sha(CACHE / 'followup-pages' / f'{stem}-{n}.png') for n in visual_pages}


def main():
    registry = load_registry()
    if IMPLEMENTATION in registry['sources']:
        build_report()
        return
    kinder_pages, third_pages, impl_pages = [91, 92, 93, 94, 97, 98, 99], [65, 66, 67, 68, 93, 94, 95], [26, 40, 41, 42, 46, 71]
    images = {
        KINDER_ID: inspect_pdf(KINDER['file'], KINDER['sha256'], 142, kinder_pages, [93, 98, 99]),
        THIRD_ID: inspect_pdf(GRADE_3['file'], GRADE_3['sha256'], 101, third_pages, [66, 95]),
        IMPLEMENTATION: inspect_pdf(IMPLEMENTATION_PDF, IMPLEMENTATION_SHA, 107, impl_pages, [42, 46, 71]),
    }
    assert sha(CACHE / 'wwc-90485-third-grade-20261110.html') == WWC_SHA
    reviews, outcomes = read_export_rows({'90485'})
    assert len(reviews) == 3 and not outcomes
    assert {row['ReviewID'] for row in reviews} == {'1913155', '1912974', '1912973'}
    assert all(row['Study_Rating'] == 'Does not meet WWC standards' for row in reviews)
    assert {row['Standards_Version'] for row in reviews} == {'4.1'}
    counts = [[7, 20, 5, 4, 4, 4, 4, 0], [9, 17, 2, 1, 0, 0, 1, 1]]
    assert list(map(sum, counts)) == [48, 31]

    bibliography = load(ROOT / 'data/sources.json')
    queue = load(ROOT / 'data/content_review_queue.json')
    entry = dict(id=IMPLEMENTATION, year=2018, url=REPORT,
                 title='Launching Kindergarten Math Clubs: The Implementation of High 5s in New York City',
                 authors=['Robin Tepper Jacob', 'Anna Erickson', 'Shira Kolnik Mattera'],
                 kind='High 5s 운영과 참여 관찰 보고서', review_scope=SCOPES[IMPLEMENTATION],
                 does_not_establish='동일 연구의 시행 보고서다. 출석, 참여 평정, 활동 운영을 수학 성취의 효과 추정으로 쓰지 않는다.',
                 next_review=NEXT[IMPLEMENTATION], supports='덧셈 활동 예, 실제 시행과 참여 평정의 관찰 범위.')
    bibliography.append(entry)
    new_notes = dict(source_id=IMPLEMENTATION, source_url=REPORT, date=DATE, reviewer='Codex',
                     source_asset_kind='pdf', source_pdf_sha256=IMPLEMENTATION_SHA, pdf_url=ERIC,
                     source_pdf_redistributed=False, contains_source_full_text=False, pdf_pages=107,
                     selected_text_pages=impl_pages, visual_pdf_pages=[42, 46, 71],
                     rendered_page_sha256=images[IMPLEMENTATION], read_scope=SCOPES[IMPLEMENTATION],
                     study_family=FAMILY, implementation_only=True,
                     reading_log=['활동의 계산 전략과 실제 회기 운영 및 참여 평정을 구분했다.'],
                     source_corrections=[dict(location='표 4.2·4.3', issue='예정 회기·게임일 제외·관찰 회기의 분모와 평정자를 구별한다.')],
                     results=dict(attendance_percent=87.4, attendance_benchmark=80,
                                  scheduled_sessions=7031, scheduled_activity_sessions=5971, observed_sessions=[25, 26]))
    note_path = f'data/literature_evidence/{IMPLEMENTATION}_review_notes.json'
    write(ROOT / note_path, new_notes)
    registry['sources'][IMPLEMENTATION] = dict(
        source_id=IMPLEMENTATION, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
        snapshot_kind='authored_review_notes', snapshot_file=note_path, snapshot_sha256=sha(ROOT / note_path),
        source_asset_kind='pdf', source_pdf_sha256=IMPLEMENTATION_SHA,
        redistribution_license='workspace_authored_notes', bibliography_snapshot=digest(entry),
        display=dict(title=entry['title'], url=REPORT, authors_year='Jacob·Erickson·Mattera, 2018'),
        read_scope=SCOPES[IMPLEMENTATION], scope_note='시행 자료와 효과 자료를 구별한다.',
        method_note='활동 예·진행자 기록·관찰 판면을 대조했다.', limits=entry['does_not_establish'],
        independent_review=False, student_validated=False, observations=OBSERVATIONS[IMPLEMENTATION],
        editorial_action='근거 2건과 자체 관찰 과제 1개를 추가했다.',
    )
    queue['literature_review'].append(dict(source=entry, status='self_read_claim_mapping',
        evidence_file='data/literature_claim_reviews.json', claim_evidence_fields=['활동 예', '운영 분모', '관찰과 평정'], claim_ids=[]))

    evidence = {
        KINDER_ID: dict(table_d1_counts=counts, scores=['T', 'logit', 'raw'], confidence_percent=90,
                        effects_logit_raw=[.10, .12], excluded_high5s=189, replacement_group=132,
                        already_included_upweighted=183, significant_specifications=3, all_specifications=5),
        THIRD_ID: dict(assignment_levels=['child', 'pre_k_site', 'randomization_block'],
                       table_f2_math=dict(effect_size=.37, printed_p=.01, n=[226, 255], caption_note_conflict=True),
                       p_by_source=dict(report=.19, journal=.18), journal_url=JOURNAL,
                       wwc_url=WWC, wwc_html_sha256=WWC_SHA, wwc_reviews=reviews, wwc_outcome_rows=outcomes,
                       wwc_reason='approach_to_missing_data_not_acceptable'),
    }
    previous_sources = {}
    for spec, pages, reading, correction in [
        (KINDER, kinder_pages, '검사별 문항 구성과 점수 및 표본 사양을 대조했다.',
         '주 분석 T점수와 로짓·원점수, 189명 제외 후 가중하는 두 사양을 별개로 유지한다.'),
        (GRADE_3, third_pages, '배정 기관을 유지한 모형과 학교 기초 성과를 조정한 탐색 결과, WWC 결측 판정을 확인했다.',
         '표 F.2 제목은 MPC와 High 5s 결합을, 하단 주석 일부는 MPC 대 정규 취학 전만을 서술한다. 본문의 결합 비교 설명과 표본 226·255명을 대조했고 원전의 상충 문구를 보존한다.'),
    ]:
        sid = spec['id']
        source = registry['sources'][sid]
        previous = previous_sources[sid] = copy.deepcopy(source)
        assert previous['snapshot_sha256'] == PRIOR[sid]
        book = next(row for row in bibliography if row['id'] == sid)
        scope = source['read_scope'] + SCOPES[sid]
        book.update(review_scope=scope, next_review=NEXT[sid])
        old = load(ROOT / previous['snapshot_file'])
        notes = dict(old, date=DATE, read_scope=scope,
                     selected_text_pages=sorted(set(old['selected_text_pages']) | set(pages)),
                     visual_pdf_pages=sorted(set(old['visual_pdf_pages']) | set(map(int, images[sid]))),
                     rendered_page_sha256={**old['rendered_page_sha256'], **images[sid]},
                     appendices_review=evidence[sid], prior_snapshot=dict(file=previous['snapshot_file'], sha256=PRIOR[sid]))
        notes['reading_log'].append(reading)
        notes['source_corrections'].append(dict(location='부록과 후속 대조', issue=correction))
        path = f'data/literature_evidence/{sid}_appendices_review_notes.json'
        write(ROOT / path, notes)
        source.update(date=DATE, read_scope=scope, snapshot_file=path, snapshot_sha256=sha(ROOT / path),
                      snapshot_history=[*previous.get('snapshot_history', []),
                          {key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                      bibliography_snapshot=digest(book),
                      observations=previous['observations'] + OBSERVATIONS[sid],
                      editorial_action='부록의 문헌 근거 2건과 자체 관찰 과제 2개를 추가했다.')
        next(row for row in queue['literature_review'] if row['source']['id'] == sid)['source'] = book

    source_urls = {KINDER_ID: KINDER['url'], THIRD_ID: GRADE_3['url'], IMPLEMENTATION: ERIC}
    for sid, cid, codes, pages, support, limit in CLAIMS:
        locations = [f'{source_urls[sid]}#page={n}' for n in pages]
        if cid == 'MPC21-06':
            locations += [WWC, JOURNAL]
        row = dict(id=cid, source_id=sid, role='related_theoretical_context', standard_codes=codes,
                   locations=locations, support=support, does_not_establish=limit,
                   independent_review=False, student_validated=False,
                   target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes})
        if sid != IMPLEMENTATION:
            row.update(role='empirical_result_with_scope', empirical_scope=registry['sources'][sid]['empirical_scope'])
        registry['claims'].append(row)
    claims = {row['id']: row for row in registry['claims']}
    for item in queue['literature_review']:
        if item['source']['id'] in SCOPES:
            item['claim_ids'] = [row['id'] for row in claims.values() if row['source_id'] == item['source']['id']]

    relations = load(ROOT / 'data/revised_relations.json')['relations']
    reviewed = load(ROOT / FILE)
    for row in reviewed['records']:
        claim = claims[row['claim_id']]
        sid = claim['source_id']
        if sid in previous_sources:
            assert row['claim_snapshot'] == claim_snapshot(claim, previous_sources[sid])
            row['claim_snapshot'] = claim_snapshot(claim, registry['sources'][sid])
    candidates = {(row['id'], cid) for row in relations for _, cid, codes, *_ in CLAIMS
                  if all(row[key].startswith('standard:') for key in ('from', 'to'))
                  and {row[key][9:] for key in ('from', 'to')} <= set(codes)}
    assert candidates == {('REV-2수01-06-2', 'H5I18-01')}
    relation = next(row for row in relations if row['id'] == 'REV-2수01-06-2')
    reviewed['records'].append(dict(
        relation_id=relation['id'], claim_id='H5I18-01', role='activity_context',
        finding='두 카드의 양을 합해 보고 모두 세기와 이어 세기의 계산을 비교한다.',
        limit='활동을 제공한 사실과 학생이 스스로 선택한 방법을 구별한다.',
        relation_snapshot=relation_snapshot(relation),
        claim_snapshot=claim_snapshot(claims['H5I18-01'], registry['sources'][IMPLEMENTATION]),
    ))
    apply_literature_context(relations, registry, registry=reviewed)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviewed)
    build_report()
    print('MPC appendices and High 5s: 6 claims, 5 observation tasks, 1 relation record, 3 WWC reviews')


if __name__ == '__main__':
    main()

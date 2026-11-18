"""Register the direct length and shape-composition comparisons."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value


CACHE = ROOT / 'tmp/literature/direct-learning-trajectory-trials'
DATE = '2026-11-09'
LENGTH = dict(
    id='SARAMA_ET_AL_2021_LENGTH_SEQUENCE', year=2021, file='sarama-2021-length',
    title='Testing a Theoretical Assumption of a Learning-Trajectories Approach in Teaching Length Measurement to Kindergartners',
    authors=['Julie Sarama', 'Douglas H. Clements', 'Arthur J. Baroody', 'Traci S. Kutaka',
             'Pavel Chernyavskiy', 'Jackie Shi', 'Menglong Cong'],
    doi='https://doi.org/10.1177/23328584211026657', url='https://files.eric.ed.gov/fulltext/EJ1323924.pdf',
    publisher='https://journals.sagepub.com/doi/full/10.1177/23328584211026657',
    sha256='578e7f39fb865693335bf46cbaeb306bf30c1d5bbf291589e9c994edce9d352b',
    pdf_pages=15, printed_pages=[1, 15], text_pages=[1, 4, 5, 6, 7, 8, 9, 10, 11],
    visual_pages=[4, 6, 7, 8, 9, 10],
    scope='출판판의 초록, 배정·평가·결과·논의 관련 문단과 표 2~9·그림 1을 확인했다. 표본과 결과의 주요 판면을 이미지로 대조했다.',
    sample='유치원 5개 학교에서 사전검사 187명, 사후검사 185명이다. 표 2는 정규 57명, 정순 69명, 역순 59명이다.',
    design='within_classroom_randomized_length_instruction_comparison',
    limit='유치원 길이의 단기 개별 수업이다. 활동 순서와 반응에 따른 과제 조정·피드백이 함께 달랐다. 다른 측정량, 국내 단위 과제 또는 필수 학습 순서의 효과를 분리할 수 없다.',
    next_review='집단별 사후분포와 원자료를 확보하면 표의 분모와 정순 대 역순 구간을 재확인한다.',
    supports=['사전·사후 분모와 조건별 수업', '정순·역순·정규 수업의 분석 차이', '길이 비교와 단위 반복의 관찰'],
    checks={1: ['189'], 6: ['185', '69', '187'], 9: ['185', '71', '0.57, 0.07'], 10: ['0.58', '0.27', '0.53']},
    results=dict(
        counts=dict(abstract=189, methods_pre=187, methods_post=185, arm_order=['BAU', 'LT', 'REV'],
                    table_2=[57, 69, 59], table_4_row_totals=[59, 69, 57], table_5_headers=[57, 71, 59]),
        contrasts=dict(
            lt_vs_bau=dict(posterior_median=.58, credible_95=[.33, .84]),
            rev_vs_bau=dict(posterior_median=.27, credible_95=[-.01, .53]),
            lt_vs_rev=dict(posterior_median=.32, endpoints_as_printed=[.57, .07]),
        ),
    ),
    corrections=[
        ('초록·방법·표 2·4·5', '초록 189, 사전 187, 사후 185를 위치별로 보존한다. 표 2와 달리 표 4의 BAU·REV 행 합계가 각각 59·57이고, 표 5의 열 머리는 187명인데 행에는 185명으로 적혀 있다. 사후 분모는 방법과 일치하는 표 2에 귀속한다.'),
        ('9쪽 본문·출판사 HTML과 표 9', '정순 대 역순 .32의 구간 끝점은 [.57,.07] 순으로 인쇄됐다. 정규 대비 역순 추정 .27의 95% 신용구간 [−.01,.53]은 0을 포함한다. 저자의 방향 요약과 구간을 구별한다.'),
        ('10~11쪽 논의', '두 지도 조건에서 순서 외에도 오답에 대한 비계와 활동 조정이 달랐다. 정규 수업 비교에는 개별 수업 여부도 함께 달랐다.'),
    ],
    claims=[
        ('LTDL-01', ['2수03-06', '2수03-10'], [4, 5, 6, 9],
         '길이 연구의 방법은 사전검사 187명과 사후검사 185명을 구분한다. 사후 표 2의 정규 수업·정순·역순 인원은 각각 57명·69명·59명이다.',
         '초록 189명과 표 5 머리글의 정순 71명은 사후 표 2의 분모와 다르다. 사후 비교에 표 2의 분모를 사용한다.'),
        ('LTDL-02', ['2수03-06', '2수03-10'], [6, 7, 10, 11],
         '정순은 학생이 보인 수준의 다음 활동에서 시작하고 반응에 맞춰 비계를 조정했다. 역순은 비슷한 길이 활동을 높은 수준부터 제시하고 오답 뒤에 풀이를 보여 줬다. 두 조건 모두 개별 수업을 받았다.',
         '순서와 피드백·활동 조정이 함께 달라 순서만의 효과를 분리할 수 없다. 정규 수업 비교에는 개별 수업 여부도 다르다.'),
        ('LTDL-03', ['2수03-06', '2수03-10'], [8, 9, 10],
         '정규 수업 대비 사후 Rasch 점수 추정은 정순 .58(95% 신용구간 .33~.84), 역순 .27(−.01~.53)이었다. 정순 대 역순은 .32로 보고했고 구간 끝점은 본문에 .57, .07 순으로 실렸다.',
         '역순 대 정규의 구간은 0을 포함한다. 정순 대 역순 구간은 원문의 표기를 보존했으며 모형을 재추정한 값이 아니다.'),
        ('LTDL-04', ['2수03-06', '2수03-10'], [7, 8, 10],
         '연구의 활동은 한쪽 끝을 맞춘 길이 비교, 여러 단위를 빈틈 없이 놓기, 한 단위 반복, 자의 영점과 단위의 관계를 구별했다. 평가는 길이 문항의 정답과 전략을 기록했다.',
         '길이 결과로 들이·무게·넓이의 비교나 국내 cm·m 과제의 성취를 대신할 수 없다. 단계 이름을 필수 선수관계로 추가하지 않는다.'),
    ],
)
SHAPE = dict(
    id='CLEMENTS_ET_AL_2019_SHAPE_SEQUENCE', year=2019, file='clements-2019-shape',
    title='Evaluating the Efficacy of a Learning Trajectory for Early Shape Composition',
    authors=['Douglas H. Clements', 'Julie Sarama', 'Arthur J. Baroody', 'Candace Joswick', 'Christopher B. Wolfe'],
    doi='https://doi.org/10.3102/0002831219842788', url='https://files.eric.ed.gov/fulltext/EJ1234710.pdf',
    publisher='https://journals.sagepub.com/doi/10.3102/0002831219842788',
    sha256='d1b814d20bd1e9b1d6e85ff9f1d5fa0e9e1dbca65be511155445efc6f7d6788d',
    pdf_pages=22, printed_pages=[2509, 2530], text_pages=list(range(9, 18)),
    visual_pages=[9, 10, 13, 14, 15, 16],
    scope='출판판 인쇄 2517~2525쪽의 방법·결과·논의 관련 문단과 그림 2·표 1~2를 읽었다. 표본·루브릭·결과의 주요 판면을 이미지로 대조했다.',
    sample='15개 유아 교실의 동의 아동 152명 중 배정 전 1명, 배정 후 사후자료 6명을 제외했다. 순서 중재 82명과 목표 수준 직접 지도 63명을 분석했다.',
    design='within_classroom_randomized_small_group_shape_composition_comparison',
    limit='유아의 평면 퍼즐 구성에 대한 단기 소집단 비교다. 목표 수준 도달 및 전략을 국내 성취기준 전체, 정신적 변환 전반, 고정된 선수관계로 확대할 수 없다.',
    next_review='문항 1의 개수·백분율의 실제 분모와 같은 설계를 이용한 후속 도형 연구를 대조한다.',
    supports=['단계 순서와 목표 수준 직접 지도의 비교', '퍼즐 정답·회전 전략의 구별', '가까운·중간·먼 전이'],
    checks={9: ['152', '145', '82', '63'], 13: ['.003', '.55'], 14: ['59%', '35%'], 15: ['Medium transfer', 'Far transfer']},
    results=dict(
        counts=dict(consented=152, before_assignment_excluded=1, after_assignment_excluded=[2, 4], analyzed=[82, 63]),
        main_model=dict(g=.55, p=.003),
        item_1_complete_correct_counts=[44, 23], item_1_complete_correct_percent_as_printed=[59, 35],
        item_1_rotation_strategy_post_mean=[1.47, 1.30],
    ),
    corrections=[
        ('인쇄 2522쪽 문항 1 설명', '완전 정답 44명(59%)·23명(35%)은 전체 조건별 82명·63명을 분모로 계산한 비율과 맞지 않는다. 문항별 분모를 추정하지 않고 개수·백분율·전체 분석 인원을 분리한다.'),
        ('인쇄 2518·2521쪽 그림 2와 표 1', '그림 2 문항 1A 판면에 오답·부분 정답·완전 정답이 있다. 표 1 제목과 본문에서 정답·과정을 사용하는 범위가 다르게 표현된다. 코딩, 기술통계와 전체 모형의 수치를 구분한다.'),
    ],
    claims=[
        ('LTDS-01', ['2수03-03', '4수03-12'], [9, 11, 12, 13, 16],
         '교실 안에서 소집단을 배정했다. 다음 수준부터 활동을 조정한 집단 82명과 목표 수준을 바로 지도한 집단 63명을 분석했다. 사전 점수를 고려한 기본 모형의 효과크기는 g=.55(p=.003)였다.',
         '특정 유아 퍼즐 단원의 조건 비교다. 교실 전체 수업이나 일정 기간 뒤 유지 효과, 국내 성취기준별 효과를 직접 검증한 자료는 아니다.'),
        ('LTDS-02', ['2수03-03', '4수03-04', '4수03-12'], [10, 14, 15],
         '문항 1의 채점은 퍼즐을 완전히 채웠는지와 조각을 놓기 전에 알맞은 방향으로 돌렸는지를 구별했다. 놓은 뒤 방향을 바꾸는 행동도 따로 기록했다.',
         '정답과 전략의 관찰 코드는 밀기·뒤집기·돌리기 전반의 별도 효과크기가 아니다. 문항 1 본문의 개수·비율은 전체 분석 분모로 재계산해 인용하지 않는다.'),
        ('LTDS-03', ['2수03-03', '4수03-12'], [9, 14, 15, 16, 17],
         '차이는 주로 조작물로 비슷한 퍼즐을 해결하는 가까운 전이 문항에 나타났다. 추가 조건이 붙는 중간 전이는 사용한 모양에 따라 달랐고 조작물 없이 예상하는 먼 전이에서는 뚜렷한 차이가 없었다.',
         '비슷한 퍼즐의 결과로 머릿속 도형 합성, 새로운 조각 조건 또는 모든 공간 과제의 효과를 추정할 수 없다.'),
        ('LTDS-04', ['2수03-03', '4수03-12'], [11, 12, 16, 17],
         '다음 수준부터 지도한 조건은 필요한 경우 안쪽 선을 그어 난도를 조절했다. 목표 수준 직접 지도 조건은 같은 방식으로 난도를 낮추지 않았다. 두 조건 모두 목표 수준 퍼즐을 다뤘다.',
         '조정과 비계가 포함된 지도 조건의 비교다. 특정 안쪽 선이나 순서가 모든 학생에게 필요하다는 근거로 쓰지 않는다.'),
    ],
)


def verify_pdf(spec, cache=CACHE):
    path = cache / f"{spec['file']}.pdf"
    assert sha(path) == spec['sha256']
    reader = PdfReader(path)
    assert len(reader.pages) == spec['pdf_pages']
    for page, expected in spec['checks'].items():
        body = ' '.join(reader.pages[page - 1].extract_text().split())
        assert all(token in body for token in expected), (spec['id'], page)
    return {str(p): sha(cache / f"{spec['file']}-page-{p}.png") for p in spec['visual_pages']}


def register(spec, images, bibliography, queue, registry):
    review_date = spec.get('date', DATE)
    source_id = spec['id']
    source_url = spec.get('canonical_url') or spec['doi']
    ids = [row[0] for row in spec['claims']]
    assert all(row['id'] != source_id for row in bibliography)
    assert all(row['source']['id'] != source_id for row in queue['literature_review'])
    empirical = dict(
        design=spec['design'], sample_description=spec['sample'], inference_limit=spec['limit'],
        student_outcome_study=True, causal_effect_established=spec.get('causal_effect_established', True),
        local_effect_tested=False,
    )
    if 'study_family' in spec:
        empirical['study_family'] = spec['study_family']
    notes_path = f'data/literature_evidence/{source_id}_review_notes.json'
    notes = dict(
        source_id=source_id, source_url=source_url, date=review_date, reviewer='Codex',
        source_asset_kind='pdf', source_pdf_sha256=spec['sha256'], source_pdf_redistributed=False,
        contains_source_full_text=False, read_scope=spec['scope'], empirical_scope=empirical,
        pdf_url=spec['url'], publisher_url=spec['publisher'], pdf_pages=spec['pdf_pages'],
        printed_pages=spec['printed_pages'], selected_text_pages=spec['text_pages'],
        visual_pdf_pages=spec['visual_pages'], rendered_page_sha256=images, results=spec['results'],
        reading_log=[spec['scope'], '분모와 비교 조건을 확인하고 전체 모형과 과제별 관찰을 구분했다.'],
        source_corrections=[dict(location=location, issue=issue) for location, issue in spec['corrections']],
    )
    if 'pdf_edition' in spec:
        notes['pdf_edition'] = spec['pdf_edition']
        notes['journal_issue_pages'] = spec['journal_issue_pages']
    entry = dict(
        id=source_id, year=spec['year'], url=source_url, title=spec['title'], authors=spec['authors'],
        kind=spec.get('kind', '초기 수학의 지도 조건 무작위 비교'), review_scope=spec['scope'],
        does_not_establish=spec['limit'], next_review=spec['next_review'], supports=spec['supports'],
    )
    write(ROOT / notes_path, notes)
    bibliography.append(entry)
    registry['sources'][source_id] = dict(
        source_id=source_id, state='self_read_claim_mapping', reviewer='Codex', date=review_date,
        snapshot_kind='authored_review_notes', source_asset_kind='pdf', source_pdf_sha256=spec['sha256'],
        snapshot_file=notes_path, snapshot_sha256=sha(ROOT / notes_path), redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry), display=dict(title=spec['title'], url=source_url,
                                                         authors_year=spec.get('authors_year', f"{spec['authors'][0].split()[-1]} 외, {spec['year']}")),
        read_scope=spec['scope'], scope_note='해당 영역에서 실제 제공한 지도 조건과 결과를 연결한다.',
        method_note=spec.get('method_note', '출판판의 방법·표·그림과 대상 성취기준의 수행 범위를 대조했다.'),
        limits=spec['limit'], empirical_scope=empirical, independent_review=False, student_validated=False,
        editorial_action=f'문헌 대응 {len(ids)}건을 추가했다.', observations=[],
    )
    for claim_id, codes, pages, support, limit in spec['claims']:
        assert set(pages) <= set(spec['text_pages'])
        registry['claims'].append(dict(
            id=claim_id, source_id=source_id, role='empirical_result_with_scope', standard_codes=codes,
            locations=[f"{spec['url']}#page={p}" for p in pages], support=support, does_not_establish=limit,
            empirical_scope=empirical, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue['literature_review'].append(dict(
        source=entry, status='self_read_claim_mapping', evidence_file='data/literature_claim_reviews.json',
        claim_evidence_fields=['표본 분모', '수업 조건과 결과', '도구·과제·적용 한계'], claim_ids=ids,
    ))


def main():
    registry = load_registry()
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography, queue = load(bibliography_path), load(queue_path)
    pending = []
    for spec in (LENGTH, SHAPE):
        if spec['id'] in registry['sources']:
            assert {c[0] for c in spec['claims']} == {row['id'] for row in registry['claims'] if row['source_id'] == spec['id']}
        else:
            pending.append((spec, verify_pdf(spec)))
    if pending:
        assert sum(LENGTH['results']['counts']['table_2']) == 185
        assert sum(LENGTH['results']['counts']['table_5_headers']) == 187
        assert 152 - 1 - sum(SHAPE['results']['counts']['after_assignment_excluded']) == 82 + 63
        for spec, images in pending:
            register(spec, images, bibliography, queue, registry)
        write(bibliography_path, bibliography)
        write(ROOT / 'data/literature_claim_reviews.json', registry)
        write(queue_path, queue)
    build_report()


if __name__ == '__main__':
    main()

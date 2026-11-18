"""Register the alternative-ordering trial and reconcile its outcome definitions."""
import copy
from fractions import Fraction

import pdfplumber

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry
from record_direct_learning_trajectory_trials import register
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


SOURCE = 'STAR_SEIFERT_2006_ALTERNATIVE_ORDER'
GUIDE = 'IES_ALGEBRA_2015'
PDF = 'https://sites.lsa.umich.edu/wp-content/uploads/sites/224/2015/01/star.seifert2006.pdf'
DOI = 'https://doi.org/10.1016/j.cedpsych.2005.08.001'
WWC = 'https://ies.ed.gov/ncee/wwc/study/79838'
DATE = '2026-11-10'

RESULTS = dict(
    group_order=['alternative_ordering', 'isomorphic_equations'],
    counts=dict(volunteers=36, assigned=[18, 18], analyzed=[17, 15],
                excluded=dict(withdrawal=1, prior_knowledge_pretest=1, prior_knowledge_first_session=2)),
    design=dict(assignment_unit='group_of_six_as_described_on_printed_page_286',
                practice_days=3, same_pre_post_items=19, delayed_test=False,
                maximum_practice_items=45, rerun_opportunities=18),
    practice=dict(attempted_mean=[31, 42], correct_pct=[85, 81], transformation_error_free_pct=[74, 84]),
    author_posttest=dict(correct_pct=[76, 79], transformation_error_free_pct=[90, 92],
                         continuous_distinct_sequence_mean=[3.2, 2.4], table_3_marker='*',
                         table_3_legend='p<.05', continuous_text_p=.146,
                         distinct_sequence_items=6, threshold=3, threshold_counts=[13, 6],
                         threshold_chi2=4.394, threshold_p='<.05',
                         invention_eligible_items=11, invention_opportunities=[6, 3, 10],
                         invention_mean=[2.5, .7], invention_F=5.152, invention_df=[1, 31],
                         invention_p='<.05'),
    wwc=dict(url=WWC, review_date='2024-02', n=32, period_as_displayed='3 Days',
             means=dict(inventions=[2.5, .7], unique_strategies=[3.2, 2.4],
                        standard_solutions=[2, 2.2], correct_pct=[71.61, 79]),
             significant_outcomes=[]),
    guide=dict(pdf_pages=[63, 64], procedural_knowledge_g=-.35, procedural_flexibility_g=.64,
               flexibility_measure_g=[.58, .70], flexibility_measures_significant=False),
)

SPEC = dict(
    id=SOURCE, year=2006, date=DATE, title='The development of flexibility in equation solving',
    authors=['Jon R. Star', 'Colleen Seifert'], authors_year='Star·Seifert, 2006',
    doi=DOI, url=PDF, publisher=DOI,
    sha256='c95cd1f11a5bbfb0c18a491276fcccb5efe420e30d2a5a9d77b29eb3d99c72ea',
    pdf_edition='출판본, University of Michigan 연구실 공개 사본',
    journal_issue_pages='Contemporary Educational Psychology 31(3), 280–300',
    pdf_pages=21, printed_pages=[280, 300], text_pages=list(range(1, 22)),
    visual_pages=[2, 7, 8, 9, 10, 12, 13, 14],
    kind='같은 방정식의 다른 변형 순서 연습 비교',
    scope='출판본 21쪽의 텍스트와 변형 예·연습·채점·표 3의 주요 판면 8쪽을 대조했다. IES 가이드 D.4와 WWC 연구 79838의 결과를 원논문과 비교했다.',
    sample='미국 중서부 한 공립 학군의 6학년 자원자 36명. 방법에 6명씩 묶은 집단을 배정했다고 서술했다. 사후 분석은 재풀이 17명, 유사 구조의 다른 식 15명이다.',
    design='randomized_alternative_ordering_practice_comparison', causal_effect_established=False,
    limit='한 학군의 소수 자원자를 대상으로 한 3일 연습과 직후 검사다. 연습에서의 재풀이와 사후 여러 식에서 관찰한 전략은 측정이 다르다. 국내 성취기준의 효과, 장기 유지나 필수 순서를 확인하지 않았다.',
    next_review='원자료와 분석 산출물을 확보하면 표 3의 별표 및 WWC의 정답률·유의 판정 차이를 확인한다. 독립 검토와 학생 반응은 별도로 기록한다.',
    supports=['첫 풀이와 요구 후 재풀이의 구분', '식 전체에 적용하는 등식 변형', '변형 오류와 수치 정답의 분리'],
    method_note='첫 수업, 재풀이와 다른 식 연습, 사후 6문항의 서로 다른 변형 순서, 11문항의 비전형적 변형을 분리했다.',
    results=RESULTS,
    corrections=[
        ('인쇄 291쪽 표 3과 293쪽 본문', '표 3의 3.2 대 2.4 행은 별표가 있다. 본문의 연속 점수 비교는 p=.146이다. 마지막 6문항 중 적어도 3문항을 서로 다른 순서로 푼 기준은 13/17 대 6/15로 별도 보고됐다.'),
        ('인쇄 291·293쪽과 WWC 79838', '비전형적 변형 횟수 2.50 대 0.70을 원논문은 p<.05, WWC는 비유의로 표시했다. 사후 수치 정답률도 원논문 76% 대 79%와 WWC 71.61% 대 79.00%로 다르다. 차이의 원인은 이 자료에서 확정하지 못했다.'),
    ],
    claims=[
        ('SS06-01', ['9수02-03', '9수02-04'], [7, 8, 9, 10],
         '공통 수업 뒤 한 조건은 같은 방정식을 다른 변형 순서로 다시 풀었다. 다른 조건은 구조가 같은 별도 방정식을 풀었다. 다시 풀기 전의 첫 풀이와 요구를 받은 뒤의 풀이를 따로 보존하고, 양변 전체에 한 변형이 해를 보존하는지 확인한다.',
         '연습에서는 산술 오류를 고쳐 주거나 변형을 상기시킬 수 있었고 다음 전략은 제안하지 않았다. 요청 뒤에 얻은 두 번째 풀이는 도움 없이 스스로 선택한 전략과 구분한다.'),
        ('SS06-02', ['9수02-04'], [9, 10, 12, 13, 14],
         '사후 마지막 6개 식에 나타난 서로 다른 변형 순서의 평균은 3.2 대 2.4였다. 표 3은 별표를 붙였고 본문은 연속 점수에 p=.146을 보고했다. 3개 이상을 기준으로 나눈 결과는 13/17 대 6/15였다. 비전형적 변형 사용 2.50 대 0.70은 원논문에서 유의, WWC에서 비유의였다.',
         '서로 다른 6개 식에서 사용한 순서의 수와 한 식의 풀이를 두 개 설명하는 능력은 측정이 다르다. 평균, 기준 이상 인원, 비전형적 변형 횟수의 판정을 각각 해석한다.'),
        ('SS06-03', ['9수02-04'], [9, 12, 13],
         '연습 시도 수는 재풀이 31개, 다른 식 42개였다. 사후의 수치 정답률은 76% 대 79%, 변형 오류가 없었던 비율은 90% 대 92%였고 두 사후 지표에 유의한 차이가 보고되지 않았다. WWC 정답률 행은 71.61% 대 79.00%로 비유의였다.',
         '정답과 변형의 적용을 따로 채점했으며 변형 지표에는 산술 오류를 허용했다. 풀이에서 변형과 계산을 별도로 관찰하고, 비유의 결과로 두 조건이 동등하다고 판정하지 않는다.'),
    ],
)

OBSERVATIONS = [
    dict(id='SS06-P1', standard_codes=['9수02-03', '9수02-04'],
         question='6(2x−3)+12=42를 풀고 처음 한 변형을 적어라. 이어서 같은 식을 다른 변형으로 시작해 다시 풀어라. 먼저 6으로 나눌 때 왼쪽의 +12는 어떻게 되는가?',
         expected='먼저 양변에서 12를 빼고 6으로 나누면 2x−3=5다. 먼저 양변을 6으로 나누면 2x−3+2=7이다. 두 풀이에서 x=4를 얻고 원식에 대입하면 양변이 42다. 6은 0이 아니며 왼쪽 전체를 나누므로 12도 2가 된다.',
         interpretation='첫 풀이, 다시 풀라는 요구 뒤의 변형 순서, 각 단계의 양변 적용을 별도로 기록한다. 한 번의 재풀이에서 여러 식에 걸친 전략 선택을 판단하지 않는다. 학생 검증 대기인 자체 과제다.', student_validated=False),
    dict(id='SS06-P2', standard_codes=['9수02-04'],
         question='4(x+1)=2x+10을 풀어라. 다음 풀이에서 x=3을 원식에 넣어 본 뒤 각 화살표가 해를 보존하는지 확인하라. 4(x+1)=2x+10 → 4x+1=2x+10 → 2x=6 → x=3.',
         expected='x=3이면 원식 양변은 16이다. 첫 화살표의 전개는 4x+4여야 한다. 잘못 전개한 식에서 정리하면 2x=9가 되어 둘째 화살표도 성립하지 않는다. 올바르게 전개한 식에서 양변의 2x와 4를 빼면 2x=6이 된다.',
         interpretation='최종 수치, 원식 대입, 분배법칙, 다음 변형에서 해 보존을 별도로 기록한다. 정답을 확인한 반응만으로 식의 변형을 이해했다고 판단하지 않는다. 학생 검증 대기인 자체 과제다.', student_validated=False),
]

RELATIONS = {
    'SEC_9수02-03_C04': ('같은 식을 다시 풀 때 먼저 12를 빼는 길과 양변 전체를 6으로 나누는 길을 설명한다.',
                         '먼저 나누는 길에서는 12도 6으로 나눠야 한다. 서로 다른 시작은 각 단계가 해를 보존할 때 타당하다.'),
    'SEC_9수02-04_C03': ('두 순서로 x=4를 구해 원식에 대입한 뒤 첫 변형을 각각 설명한다.',
                         '답의 대입 확인과 등식의 성질에 따른 각 변형의 설명을 나누어 관찰한다.'),
    'REV-9수02-03-1': ('첫 풀이, 다른 순서를 요구한 뒤의 풀이, 양변의 각 항에 한 연산을 나누어 기록한다.',
                       '유도 후 다른 순서의 성공은 여러 식에서의 자발적 전략 선택이나 필수 학습 순서를 입증하지 않는다.'),
}


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        build_report()
        return
    source = ROOT / 'tmp/literature/star-seifert-2006-flexibility.pdf'
    pages = ROOT / 'tmp/pdfs/star-seifert-2006'
    assert sha(source) == SPEC['sha256']
    with pdfplumber.open(source) as pdf:
        assert len(pdf.pages) == SPEC['pdf_pages']
    images = {str(page): sha(pages / f'p{page:02d}.jpg') for page in SPEC['visual_pages']}
    assert sum(RESULTS['counts']['analyzed']) + sum(RESULTS['counts']['excluded'].values()) == 36
    assert round(32 * (13 * 9 - 4 * 6) ** 2 / (17 * 15 * 19 * 13), 3) == 4.394
    assert 6 * (2 * 4 - 3) + 12 == 42 and 2 * 4 - 3 + Fraction(12, 6) == Fraction(42, 6)
    assert 4 * (3 + 1) == 2 * 3 + 10 and 4 * 3 + 1 != 2 * 3 + 10

    bp = ROOT / 'data/sources.json'
    qp = ROOT / 'data/content_review_queue.json'
    bibliography, queue = load(bp), load(qp)
    register(SPEC, images, bibliography, queue, registry)
    article = registry['sources'][SOURCE]
    article.update(observations=OBSERVATIONS, editorial_action='근거 3건, 관찰 과제 2개, 관계별 대조 3건을 추가했다.')
    source_claims = [claim for claim in registry['claims'] if claim['source_id'] == SOURCE]
    for claim in source_claims[1:]:
        claim['locations'].append(WWC)
    guide = registry['sources'][GUIDE]
    old_guide = copy.deepcopy(guide)
    guide_entry = next(row for row in bibliography if row['id'] == GUIDE)
    guide_entry['next_review'] = '2006년 재풀이 연구의 출판본과 공식 WWC 심사, 2007·2009년 연구, 2012년 공식 WWC 심사·초록을 대조했다. 남은 원연구 본문·판면과 원자료 및 실제 검증을 확인한다.'
    guide['bibliography_snapshot'] = digest(guide_entry)
    guide['primary_source_crosschecks'].append(dict(
        source_id=SOURCE, claim_ids=[claim['id'] for claim in source_claims],
        snapshot_file=article['snapshot_file'], snapshot_sha256=article['snapshot_sha256'],
        author_analyzed_n=[17, 15], wwc_n=32, same_sample_size=True,
        equivalent_outcome_report=False, guide_pdf_pages=[63, 64], wwc_url=WWC))
    next(row for row in queue['literature_review'] if row['source']['id'] == GUIDE)['source'] = guide_entry

    relations = load(ROOT / 'data/revised_relations.json')['relations']
    reviews = load(ROOT / FILE)
    claims = {claim['id']: claim for claim in registry['claims']}
    for row in reviews['records']:
        claim = claims[row['claim_id']]
        if claim['source_id'] == GUIDE:
            assert row['claim_snapshot'] == claim_snapshot(claim, old_guide)
            row['claim_snapshot'] = claim_snapshot(claim, guide)
    cross_scope = {f'standard:{code}' for code in source_claims[0]['standard_codes']}
    matched = {row['id']: row for row in relations if {row['from'], row['to']} == cross_scope}
    assert set(matched) == set(RELATIONS)
    for rid, (finding, limit) in RELATIONS.items():
        reviews['records'].append(dict(relation_id=rid, claim_id='SS06-01', role='activity_context',
                                       finding=finding, limit=limit, relation_snapshot=relation_snapshot(matched[rid]),
                                       claim_snapshot=claim_snapshot(claims['SS06-01'], article)))
    apply_literature_context(relations, registry, registry=reviews)
    write(bp, bibliography)
    write(qp, queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviews)
    build_report()
    print('Star and Seifert 2006: 3 claims, 2 probes and 3 relation entries')


if __name__ == '__main__':
    main()

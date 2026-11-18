"""Reconcile three equation-solving studies with WWC's outcome-level export."""
import copy
import csv
import io
from collections import Counter
from fractions import Fraction
from zipfile import ZipFile

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


SOURCE = 'WWC_ALGEBRA_FINDINGS_EXPORT'
GUIDE = 'IES_ALGEBRA_2015'
DATE = '2026-11-10'
URL = 'https://ies.ed.gov/ncee/wwc/StudyFindings'
PAPER_2009 = 'https://doi.org/10.1037/a0016026'
PAPER_2008 = 'https://doi.org/10.1016/j.learninstruc.2007.09.018'
CACHE = ROOT / 'tmp/literature'
ARCHIVE = CACHE / 'wwc-study-findings-export-20261110.zip'
ARCHIVE_SHA = 'e5192a5a503590328c91ea6771b562e62c18be717cc4f1048faef6bcd78def09'
PAGE_SHA = '7bbb50cad9cd9e9c813eeeb9cf54c071cf4f3656bee931e2f48446a951c26fc4'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
STUDIES = {'79863', '79864', '79868'}
SCOPE = 'WWC 연구 79863·79864·79868의 내보내기에서 심사 11건과 결과 26개 행을 추출했다. 공식 웹 결과표, 개정 가이드 D.4, 2008년 논문 공개 발췌와 2009년 출판본 웹 텍스트의 선정 대목을 대조했다.'
SCOPE_NOTE = '논문 전체 표본과 각 심사의 분석 표본, 결과별 측정 및 최종 판정을 구별한다.'
LIMIT = '원연구의 전체 참여자와 각 WWC 결과의 분석 표본, 측정·시점과 유의 판정을 구별한다. 내보내기는 심사 수준의 데이터다. 조정 방법, 원자료, 국내 과제 효과, 독립 검토와 학생 검증은 별도다.'
NEXT = '2008·2012년 출판본 전체, 2009년 공식 판면, 분석 표본 선정과 효과 크기·유의 판정의 산출 근거 및 실제 학생 반응을 확인한다.'
EMPIRICAL = dict(
    design='outcome_level_wwc_reviews_of_three_randomized_studies',
    sample_description='2008년 63·66명 비교, 2009년 사전 대수 사용 95명과 미사용 55명 비교, 2012년 124·118·115명 결과 행이다.',
    inference_limit=LIMIT, student_outcome_study=True, local_effect_tested=False,
)

CLAIMS = [
    ('WAE01', ['9수02-03', '9수02-04'], '79868, 결과 10274–10276·8760–8762',
     '2008년 연구의 전략 시범 없이 재풀이를 요구한 63명 비교와 재풀이 요구 없이 시범을 보인 66명 비교는 같은 비교 조건을 쓴다. 63명 지름길 행의 p값은 연구 열 0.36, WWC 열 약 0.0395이며 최종 표기는 유의다. 다중 전략 사용 행은 WWC p≈0.0417이면서 최종 비유의다. 정답과 전략을 별도로 읽는다.',
     '공유 비교군을 중복 합산하지 않는다. 가이드 각주 q와 내보내기의 차이는 보존하고, WWC p값만으로 최종 판정을 다시 매기거나 조정 원인을 추정하지 않는다.'),
    ('WAE02', ['9수02-04'], '79863, 결과 8488–8510와 개정 가이드 D.4',
     '2009년 연구의 2023년 WWC 사후 비교는 사전 대수 시도 95명과 미시도 55명이다. 55명의 절차 지식 행은 연구 p=0.04, WWC p≈0.111로 최종 비유의다. 네 지표의 영역 판단은 실질적으로 중요한 부정적 효과로 표시된다.',
     '영역의 판단과 각 행의 통계적 유의 여부는 구분한다. 가이드의 101명·55명과 원논문의 분석 236명은 서로 다른 분석 범위이며 101명과 95명의 차이 원인은 확인 전이다.'),
    ('WAE03', ['9수02-04'], '2009년 출판본 842~846쪽 및 표 3·4',
     '출판본은 유지검사 미참여 46명과 개념 지식 부분 미진입 추가 43명을 보고하고 해당 결과의 결측을 37%로 적었다. 약 2주 뒤 컴퓨터 검사에서는 풀이를 기록할 수 없었고 정오 피드백이 주어졌다. 표 3의 실제 지름길 사용은 유지검사에서 미제공이다.',
     '결측의 대치와 관찰된 실제 응답을 구분한다. 89를 분석 대상 236으로 단순 나눈 값과 출판본의 37%는 각각 남긴다. 유연성 인식과 자발적 전략 사용을 같은 유지 결과로 해석하지 않는다.'),
    ('WAE04', ['9수02-04'], '79864, 결과 10298·10312·10333와 개정 가이드 D.4',
     '2012년 즉시 비교의 실제 전략 사용은 하루 124명과 한 달 118명 행 모두 유의다. 유연성 지식은 두 시점 모두 비유의다. 한 달 개념 지식 행의 효과 크기는 내보내기 연구 열 −0.14와 WWC 열 약 −0.212이며, 가이드 각주는 +0.14다.',
     '하루 124명, 한 달 118명, 지연 비교 115명과 논문 전체 배정 198명을 구별한다. 서로 다른 지표의 결과를 전략 전반의 향상이나 국내 과제의 효과로 합산하지 않는다.'),
]

OBSERVATIONS = [
    dict(id='WAE-P1', standard_codes=['9수02-03', '9수02-04'],
         question='먼저 8(x−1)+4=2(x−1)+22를 혼자 풀고 첫 변형을 남겨라. 그 뒤 전개 풀이와 공통 부분식을 남기는 풀이를 각각 설명하라.',
         expected='공통 부분식을 남기면 6(x−1)=18에서 x=4다. 전개하면 8x−4=2x+20에서 6x=24다. 원식의 두 값은 모두 28이다.',
         interpretation='첫 전략, 요구를 받은 뒤의 재풀이, 양변에 적용한 연산과 정답을 각각 남긴다.', student_validated=False),
    dict(id='WAE-P2', standard_codes=['9수02-04'],
         question='2(3x+1)=20을 풀 때 두 시작 방법이 있다. A는 양변을 2로 나누고 B는 왼쪽을 전개한다. 어느 방법이 계산하기 편한지 이유를 써라. 다음에는 보기 없이 2(3x+1)+4=24를 풀고 각 줄의 근거를 써라.',
         expected='첫 식은 양변을 2로 나누면 3x+1=10이므로 x=3이다. 둘째 식은 양변에서 4를 먼저 빼도 된다. 2로 먼저 나누면 3x+1+2=12다. 어느 쪽도 x=3이다.',
         interpretation='보기에서의 인식, 독립 풀이에서 실제 쓴 전략과 근거를 나눈다. 풀이를 남길 수 없는 형식에서는 전략을 미관찰로 표시한다.', student_validated=False),
    dict(id='WAE-P3', standard_codes=['9수02-04'],
         question='4(t+2)+3(t+2)=35를 풀고 묶은 이유를 설명하라. 다음 식 4(t+2)+3(t+1)=35에서도 같은 방식으로 묶을 수 있는지 판단하고 풀어라.',
         expected='첫째는 공통 식 t+2를 묶어 7(t+2)=35가 되므로 t=3이다. 둘째는 두 괄호가 달라 7(t+2)로 묶을 수 없다. 전개하면 7t+11=35이므로 t=24/7이다.',
         interpretation='익숙한 구조에서의 첫 풀이와 구조가 달라진 경우의 판단을 구별한다. 정답 피드백 뒤 바뀐 전략은 첫 풀이와 따로 남긴다.', student_validated=False),
]

RELATIONS = {
    'SEC_9수02-03_C04': ('두 변형 경로에서 양변에 적용한 연산을 설명한다.', '첫 풀이와 재풀이 요구 뒤의 응답을 구분한다.'),
    'SEC_9수02-04_C03': ('전개하거나 공통 부분식을 남겨 해를 구하고 원식에 대입한다.', '정답률과 특정 전략 사용을 별도로 관찰한다.'),
    'REV-9수02-03-1': ('같은 해에 이르는 다른 변형을 설명하고 순서를 기록한다.', '요구 뒤 전략 사용으로 자발적 선택을 판정하지 않는다.'),
}

STUDY_FIELDS = ('StudyID', 'ReviewID', 'Protocol', 'Protocol_Version', 'Standards_Version',
                'Study_Rating', 'ReviewedDate', 'Posting_Date', 'Product_Name')
FINDING_FIELDS = ('ReviewID', 'FindingID', 'Outcome_Measure', 'Period', 'Sample_Description',
                  'Outcome_Sample_Size', 'Outcome_Measure_Intervention_Sample_Size',
                  'Outcome_Measure_Comparison_Sample_Size', 'Intervention_Mean', 'Comparison_Mean',
                  'Effect_Size_Study', 'Effect_Size_WWC', 'p_Value_Study', 'p_Value_WWC',
                  'Is_Statistically_Significant')


def read_export_rows(study_ids, finding_fields=FINDING_FIELDS):
    assert sha(ARCHIVE) == ARCHIVE_SHA
    assert sha(CACHE / 'wwc-study-findings-20261110.html') == PAGE_SHA
    with ZipFile(ARCHIVE) as archive:
        with archive.open('Studies.csv') as stream:
            studies = [{key: row[key] for key in STUDY_FIELDS}
                       for row in csv.DictReader(io.TextIOWrapper(stream, encoding='utf-8-sig'))
                       if row['StudyID'] in study_ids]
        ids = {row['ReviewID']: row['StudyID'] for row in studies}
        with archive.open('Findings.csv') as stream:
            rows = [dict(StudyID=ids[row['ReviewID']], **{key: row[key] for key in finding_fields})
                    for row in csv.DictReader(io.TextIOWrapper(stream, encoding='utf-8-sig'))
                    if row['ReviewID'] in ids]
    assert len(ids) == len(studies)
    return studies, rows


def extract():
    studies, rows = read_export_rows(STUDIES)
    assert len(studies) == 11
    assert Counter(row['StudyID'] for row in rows) == {'79863': 8, '79864': 10, '79868': 8}
    assert len({row['FindingID'] for row in rows}) == len(rows) == 26
    for row in rows:
        assert int(row['Outcome_Sample_Size']) == (
            int(row['Outcome_Measure_Intervention_Sample_Size']) +
            int(row['Outcome_Measure_Comparison_Sample_Size']))
    lookup = {row['FindingID']: row for row in rows}
    assert {row['FindingID'] for row in rows if row['Is_Statistically_Significant'] == 'True'} == {
        '8762', '10274', '10275', '10298', '10312'}
    assert lookup['8488']['p_Value_Study'] == '0.04' and round(float(lookup['8488']['p_Value_WWC']), 3) == .111
    assert lookup['10275']['p_Value_Study'] == '0.36' and round(float(lookup['10275']['p_Value_WWC']), 4) == .0395
    assert all(float(lookup[key]['p_Value_WWC']) < .05 and
               lookup[key]['Is_Statistically_Significant'] == 'False' for key in ('10276', '8760'))
    assert lookup['10333']['Effect_Size_Study'] == '-0.14'
    return studies, rows


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        build_report()
        return
    studies, rows = extract()
    assert round(100 * Fraction(46 + 43, 236), 1) == Fraction('37.7')
    assert 8 * (4 - 1) + 4 == 2 * (4 - 1) + 22 == 28
    assert 2 * (3 * 3 + 1) == 20 and 2 * (3 * 3 + 1) + 4 == 24
    assert 4 * (3 + 2) + 3 * (3 + 2) == 35
    t = Fraction(24, 7)
    assert 4 * (t + 2) + 3 * (t + 1) == 35

    bibliography = load(ROOT / 'data/sources.json')
    queue = load(ROOT / 'data/content_review_queue.json')
    entry = dict(id=SOURCE, year=2026, url=URL, title='WWC Data from Study Reviews: Equation-Solving Comparisons',
                 authors=['What Works Clearinghouse'], kind='공식 연구 심사 결과와 원논문 대조',
                 review_scope=SCOPE, does_not_establish=LIMIT, next_review=NEXT,
                 supports='분석 표본, 측정 시점, 원연구와 WWC의 p값 및 최종 판정의 구분.')
    notes = dict(
        source_id=SOURCE, source_url=URL, date=DATE, reviewer='Codex',
        source_asset_kind='publisher_html', source_asset_sha256=PAGE_SHA, source_asset_redistributed=False,
        pdf_read=False, original_page_layout_review=False, source_pdf_redistributed=False,
        contains_source_full_text=False, read_scope=SCOPE, empirical_scope=EMPIRICAL,
        reading_log=['공식 내보내기의 Studies.csv와 Findings.csv를 ReviewID로 연결해 원연구 3편의 심사 11건과 결과 26개 행을 확인했다.',
                     '공식 웹에서 유의 판정과 영역 판단을 확인하고 가이드의 효과 크기·각주와 구별했다.',
                     '2009년 출판본의 웹 텍스트에서 표 2~4, 결측 처리, 유지검사의 시행 방식과 제한을 확인했다. 직접 PDF 취득은 HTTP 403이었고 판면은 확인 전이다.'],
        source_corrections=[
            dict(location='79868, 10275·10276·8760', issue='WWC p 열과 최종 판정 열을 모두 보존한다. 가이드 각주와 다른 판정의 계산 이유는 확인 전이다.'),
            dict(location='79863, 8488 및 2009년 출판본 842~846쪽', issue='연구·WWC의 p 열을 구별한다. 보고된 결측 37%와 46명·43명 단순 합산의 37.7%를 별도로 적는다.'),
            dict(location='79864, 10333 및 가이드 표 D.4 각주 j', issue='한 달 개념 지식의 연구·WWC 효과 크기 두 값은 모두 음수다. 가이드의 양수 표기를 보존하고 원자료나 분석 산출물로 원인을 확인한다.'),
        ],
        study_urls={study: f'https://ies.ed.gov/ncee/wwc/study/{study}' for study in sorted(STUDIES)},
        paper_crosschecks={'2008': PAPER_2008, '2009': PAPER_2009, '2012': 'https://doi.org/10.1111/j.2044-8279.2011.02037.x'},
        export=dict(sha256=ARCHIVE_SHA, file_names=['Studies.csv', 'Findings.csv'],
                    row_join='ReviewID', source_zip_redistributed=False, participant_level_data=False),
        author_2009_retention=dict(print_pages=[842, 846], absent=46, did_not_start_conceptual_after_beginning=43,
                                   analyzed_n=236, reported_missing_percent=37, simple_quotient_percent=37.7,
                                   em_imputation=True, written_strategy_observed=False, per_item_feedback=True),
        review_rows=studies, outcome_rows=rows, unresolved_followup=NEXT,
    )
    write(ROOT / NOTES, notes)
    review = dict(
        source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
        snapshot_kind='authored_review_notes', snapshot_file=NOTES, snapshot_sha256=sha(ROOT / NOTES),
        source_asset_kind='publisher_html', source_asset_sha256=PAGE_SHA,
        redistribution_license='workspace_authored_notes', bibliography_snapshot=digest(entry),
        display=dict(title=entry['title'], url=URL, authors_year='WWC · 2008·2009·2012 연구'),
        read_scope=SCOPE, scope_note=SCOPE_NOTE, method_note='원논문과 심사 자료의 분모·지표·시점·판정을 각각 확인했다.',
        limits=LIMIT, empirical_scope=EMPIRICAL, observations=OBSERVATIONS,
        independent_review=False, student_validated=False,
        editorial_action='근거 4건, 관찰 과제 3개, 관계별 대조 3건을 추가했다.',
    )
    bibliography.append(entry)
    registry['sources'][SOURCE] = review
    for cid, codes, location, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='empirical_result_with_scope', standard_codes=codes,
            locations=[f'{URL} · {location}'], support=support, does_not_establish=limit,
            empirical_scope=EMPIRICAL, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    claim_ids = [row[0] for row in CLAIMS]
    queue['literature_review'].append(dict(
        source=entry, status='self_read_claim_mapping', evidence_file='data/literature_claim_reviews.json',
        claim_evidence_fields=['연구·심사 ID', '분모와 시점', '효과 크기·p값·최종 판정'], claim_ids=claim_ids,
    ))

    guide = registry['sources'][GUIDE]
    prior_guide = copy.deepcopy(guide)
    guide_entry = next(row for row in bibliography if row['id'] == GUIDE)
    guide_entry['next_review'] = 'WWC 내보내기로 2008·2009·2012년 연구의 결과 26개 행을 대조했다. 남은 원논문 판면과 원자료, 효과 크기·유의 판정의 산출 근거 및 실제 검증을 확인한다.'
    guide['bibliography_snapshot'] = digest(guide_entry)
    guide['findings_export_crosscheck'] = dict(source_id=SOURCE, claim_ids=claim_ids, snapshot_file=NOTES,
                                               snapshot_sha256=review['snapshot_sha256'], study_ids=sorted(STUDIES),
                                               review_count=11, finding_count=26)
    next(row for row in queue['literature_review'] if row['source']['id'] == GUIDE)['source'] = guide_entry

    relations = load(ROOT / 'data/revised_relations.json')['relations']
    claims = {row['id']: row for row in registry['claims']}
    by_id = {row['id']: row for row in relations}
    reviewed = load(ROOT / FILE)
    for row in reviewed['records']:
        claim = claims[row['claim_id']]
        if claim['source_id'] == GUIDE:
            assert row['claim_snapshot'] == claim_snapshot(claim, prior_guide)
            row['claim_snapshot'] = claim_snapshot(claim, guide)
    eligible = {(row['id'], cid) for row in relations for cid, codes, *_ in CLAIMS
                if all(row[key].startswith('standard:') for key in ('from', 'to'))
                and {row[key][9:] for key in ('from', 'to')} <= set(codes)}
    assert eligible == {(rid, 'WAE01') for rid in RELATIONS}
    for rid, (finding, limit) in RELATIONS.items():
        reviewed['records'].append(dict(relation_id=rid, claim_id='WAE01', role='activity_context',
                                        finding=finding, limit=limit, relation_snapshot=relation_snapshot(by_id[rid]),
                                        claim_snapshot=claim_snapshot(claims['WAE01'], review)))
    apply_literature_context(relations, registry, registry=reviewed)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviewed)
    build_report()
    print('WWC algebra export: 11 review records, 26 findings, 4 claims, 3 observation tasks, 3 relation records')


if __name__ == '__main__':
    main()

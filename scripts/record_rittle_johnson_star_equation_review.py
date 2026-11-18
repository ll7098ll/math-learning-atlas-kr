"""Register the three-condition equation comparison and reconcile the WWC scope."""
import copy
import hashlib
from fractions import Fraction

from pypdf import PdfReader

from extend_lt2_length_assets_review import load, write
from literature_review import ROOT, build_report, digest, load_registry
from record_direct_learning_trajectory_trials import register
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot

SOURCE = 'RITTLE_JOHNSON_STAR_2009_EQUATION_COMPARISONS'
GUIDE = 'IES_ALGEBRA_2015'
URL = 'https://dash.harvard.edu/bitstreams/7312037c-9058-6bd4-e053-0100007fdf3b/download'
DOI = 'https://doi.org/10.1037/a0014224'
PUBLISHED = 'https://citeseerx.ist.psu.edu/document?doi=7f45c9bebd7bf8e05ec29a74e5aa09084800def5&repid=rep1&type=pdf'
WWC = 'https://ies.ed.gov/ncee/wwc/study/79862'
PDF_SHA = '6f5015e2fb1d7b2298fe85c227dc793fc473d74d6b23a8b219f9b7eb88974fd5'
VISUAL = list(range(45,54)) + [55,56,57]

CLAIMS = [
    ('RJS-01', ['9수02-03','9수02-04'], [14,15,22,23,45,46,51,55],
     '세 조건은 같은 식의 서로 다른 풀이, 서로 다른 유형에 적용한 같은 풀이, 같은 유형에 적용한 같은 풀이를 비교했다. 사후와 2주 뒤 유지 검사를 함께 분석한 조건 효과는 개념 지식 p=.004, 절차 지식 p=.402였다. 양변에서 공통인 부분식을 빼는 경로와 전개하는 경로를 같은 해집합으로 설명하는 데 참고한다.',
     '같은 반의 짝 단위 배정이며 예제 짝, 질문, 독립 연습 형식이 함께 달랐다. 절차 지식의 비유의 결과는 동등성이나 현재 과제 효과를 입증하지 않는다. WWC의 시점별 두 집단 비교와 논문의 세 집단 분석을 구별한다.'),
    ('RJS-02', ['9수02-04'], [16,17,19,23,24,25,48,50,51,57],
     '첫 연산에서 복합식을 묶어 처리한 빈도와, 별도로 여러 방법을 만들고 적절한 첫 단계를 알아보고 타당성과 효율을 평가하는 지식을 구별했다. 두 유연성 지표의 세 조건 비교는 각각 p=.008이었다. 새 방정식에서 자발적으로 고른 연산은 예시를 보며 설명한 반응과 따로 기록한다.',
     '전략 사용은 친숙한 문항과 근전이 문항의 첫 연산에서 측정한 지표다. 원전이 두 문항은 사전·사후 정답자가 없어 절차 분석에서 제외됐다. 조건 전체의 p값을 개별 대비나 특정 방법의 효과로 옮기지 않는다.'),
    ('RJS-03', ['9수02-02'], [10,12,16,24,25,46,47],
     '괄호를 통째로 나누기, 동일한 부분식을 한쪽에서 모으기, 양변에서 같은 부분식을 빼기를 구별한다. 동류항을 판단할 때 괄호 모양이나 문자 하나만 보지 말고 괄호 안 전체와 연산을 설명하도록 한다.',
     '개념 검사에는 동치와 동류항 등 여러 문항이 들어 있다. 출판본에서 풀이 방법 집단의 추가 사용 차이를 논의한 전략은 공통 부분식 빼기다. 괄호를 통째로 나눈 경우에는 집단별 사용 차이가 확인되지 않았다.'),
]
OBSERVATIONS = [
    dict(id='RJS-P1', standard_codes=['9수02-03','9수02-04'],
         question='7(2x−1)=4(2x−1)+21을 먼저 전개하는 방법과 같은 부분식을 빼는 방법으로 풀어라. 오른쪽 괄호를 2x+1로 바꾸면 두 부분식을 같은 것으로 보고 묶을 수 있는가?',
         expected='첫 식은 양변에서 4(2x−1)을 빼면 3(2x−1)=21이므로 x=4다. 전개해도 같은 해를 얻는다. 바뀐 식의 두 괄호는 같지 않아 그 방법으로 묶을 수 없다. 전개하면 6x=32이므로 x=16/3이다.',
         interpretation='같은 식을 빼도 해집합이 유지되는 근거와, 두 괄호가 같지 않을 때 달라지는 계산을 분리한다. 자체 과제이며 학생 검증 대기다.',
         student_validated=False),
    dict(id='RJS-P2', standard_codes=['9수02-02','9수02-04'],
         question='4(3x+2)=44와 4(3x+2)+2(3x+2)=48을 비교해 각 식에서 편한 첫 연산을 설명하라. 두 예를 가린 뒤 9(2t+3)=5(2t+3)+28의 첫 연산과 해를 적어라.',
         expected='첫 식은 양변을 4로 나누면 x=3이다. 둘째 식은 두 항을 모아 6(3x+2)=48로 만들면 x=2다. 새 식은 공통 부분식을 빼면 4(2t+3)=28이므로 t=2다. 세 식 모두 올바르게 전개하는 풀이도 가능하다.',
         interpretation='첫 연산의 타당성, 어떤 구조를 보았는지, 예를 가린 뒤의 자발적 사용, 최종 정답을 구별한다. 자체 과제이며 학생 검증 대기다.',
         student_validated=False),
]
RELATIONS = {
    'SEC_9수02-03_C04': ('같은 식의 두 풀이를 나란히 두고 양변에서 4(2x−1)을 빼는 단계가 해를 보존하는 이유를 확인한다.',
                        '다른 괄호끼리 공통인 것처럼 빼면 남은 항을 잃는다. 수업 처치의 효과를 등식의 성질에 대한 별도 검사로 해석하지 않는다.'),
    'SEC_9수02-04_C03': ('공통 부분식을 먼저 빼는 경로와 전개하는 경로가 x=4로 이어지는지 대조한다.',
                        '빠른 풀이와 타당한 풀이를 구별하며, 바뀐 식에서 동일 부분식이라는 조건을 다시 확인한다.'),
    'REV-9수02-03-1': ('첫 연산의 타당성을 먼저 설명하고 새 방정식에서 전략을 스스로 고르는지를 따로 기록한다.',
                       '세 조건의 단기 수업 비교로 현재 과제의 필수 선수성이나 학생 숙달을 입증할 수 없다.'),
}


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        build_report()
        return
    path = ROOT / 'tmp/literature/rittle-johnson-star-2009-compared.pdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == PDF_SHA
    assert len(PdfReader(path).pages) == 57
    images = {str(p): hashlib.sha256((ROOT / f'tmp/pdfs/rittle-johnson-star-2009/p{p}.jpg').read_bytes()).hexdigest()
              for p in VISUAL}
    x = Fraction(16,3)
    assert 7*(2*4-1) == 4*(2*4-1)+21
    assert 7*(2*x-1) == 4*(2*x+1)+21
    assert 4*(3*3+2) == 44 and 6*(3*2+2) == 48 and 9*(2*2+3) == 5*(2*2+3)+28
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography, queue = load(bibliography_path), load(queue_path)
    crosscheck = dict(guide_pdf_pages=[61,63], wwc_types_comparison=WWC,
                      author_conditions={'methods':54,'types':56,'equivalent':52},
                      guide_methods_vs_equivalent={'immediate_analytic_n':[98,105],'flexibility_domain_g':.36,
                                                   'flexibility_knowledge_g':.45,'flexibility_use_g':.25,
                                                   'retention_flexibility_domain_g':.50},
                      guide_types_vs_equivalent={'immediate_analytic_n':[101,106],'flexibility_domain_g':.35},
                      shared_comparison=True, same_analysis=False)
    register(dict(
        id=SOURCE, date='2026-11-10', year=2009, title='Compared with what? The effects of different comparisons on conceptual knowledge and procedural flexibility for equation solving',
        authors=['Rittle-Johnson, B.','Star, J. R.'], authors_year='Rittle-Johnson·Star, 2009',
        doi=DOI, url=URL, publisher=DOI, sha256=PDF_SHA, pdf_pages=57, printed_pages='저자 원고 1–56쪽과 DASH 표지',
        pdf_edition='Harvard DASH revised author manuscript with repository cover', journal_issue_pages='529–544',
        text_pages=list(range(1,58)), visual_pages=VISUAL,
        scope='하버드 DASH 저자 원고 57쪽 추출문, 표 1–8과 그림 1–3의 선정 판면 12쪽, 출판본 검색 텍스트의 전략 명칭·표 4·6을 대조했다.',
        kind='일차방정식의 풀이 비교 조건 연구', design='within_classroom_randomized_dyad_equation_comparison',
        method_note='같은 반 안에서 짝을 세 조건에 배정했다. 세 수업 뒤 즉시·2주 뒤 유지 검사, 결과별 세 조건의 공변량 분석과 WWC의 쌍별 산출을 구별했다.',
        sample='미국 중학교 3곳, 수학 9개 학급의 7~8학년 162명. 풀이 방법 54명, 문제 유형 56명, 같은 유형 52명이다. 1명을 제외했고 17명은 한 검사 결측을 추정했다.',
        limit='기초 방정식 수업을 받은 학생에게 시행한 단기 연구다. 자료와 질문·연습 형식을 함께 비교했으며 원전이와 현재 국내 과제 효과는 확인하지 않았다.',
        next_review='출판본의 나머지 텍스트와 판면, 표 4의 절차 지식 행 중복에 대한 원자료나 공식 정정, 2007년·2012년 별도 비교 연구를 확인한다.',
        supports='부분식을 묶어 처리하는 방법의 조건과 풀이 비교에서 개념 지식·절차 지식·유연성 사용·유연성 지식의 구분.',
        results=dict(crosscheck=crosscheck, retained_analysis_n=161, imputed_single_assessment_n=17,
                     condition_p={'conceptual':.004,'procedural':.402,'flexibility_use':.008,'flexibility_knowledge':.008},
                     post_and_retention_same_measure=True, far_transfer_items_omitted=2,
                     published_pdf_text_url=PUBLISHED, published_binary_obtained=False),
        corrections=[
            ('저자 원고 PDF25 · 출판본 인쇄 539쪽', '원고 요약의 나누기(divide)는 출판본 요약에서 빼기(subtract)로 바뀌었다. 세부 결과에서도 나누기 사용은 집단 차이가 없고 빼기는 전체 조건 p=.006이었다.'),
            ('저자 원고 PDF49 · 출판본 인쇄 537쪽 표 4', '절차 지식의 방법과 동형 문제 행은 사전·사후·유지의 평균과 표준편차 여섯 값이 모두 같다. 원자료 없이 오류로 단정하거나 수치를 바꾸지 않는다.'),
            ('가이드 PDF61,63과 WWC 연구 79862', '공통 비교군을 쓰는 두 쌍의 시점별 결과다. 원논문 사후·유지 반복 측정의 공변량 분석과 분석 인원·유의 표기를 합치지 않는다.'),
        ], claims=CLAIMS,
    ), images, bibliography, queue, registry)
    article = registry['sources'][SOURCE]
    article.update(observations=OBSERVATIONS, editorial_action='문헌 대응 3건, 자체 관찰 과제 2개, 관계별 문헌 대조 3건을 추가했다.')

    guide = registry['sources'][GUIDE]
    old_guide = copy.deepcopy(guide)
    entry = next(row for row in bibliography if row['id'] == GUIDE)
    entry['next_review'] = '2009년 두 저자의 풀이 비교 연구는 저자 원고와 대조했다. 나머지 판면·도구·영상·일반 핸드북, 다른 원논문과 원자료, 독립 검토와 실제 학생 반응은 후속 범위다.'
    guide.update(bibliography_snapshot=digest(entry),
                 primary_source_crosschecks=[dict(source_id=SOURCE, claim_ids=['RJS-01','RJS-02','RJS-03'],
                                                  snapshot_file=article['snapshot_file'], snapshot_sha256=article['snapshot_sha256'],
                                                  **crosscheck)])
    next(row for row in queue['literature_review'] if row['source']['id'] == GUIDE)['source'] = entry
    relations = load(ROOT / 'data/revised_relations.json')['relations']
    by_id = {row['id']:row for row in relations}
    claims = {row['id']:row for row in registry['claims']}
    reviews = load(ROOT / FILE)
    for row in reviews['records']:
        claim = claims[row['claim_id']]
        if claim['source_id'] == GUIDE:
            assert row['claim_snapshot'] == claim_snapshot(claim,old_guide)
            row['claim_snapshot'] = claim_snapshot(claim,guide)
    pairs = {(row['id'],cid) for row in relations for cid,codes,*_ in CLAIMS
             if all(row[key].startswith('standard:') for key in ('from','to'))
             and {row[key][9:] for key in ('from','to')} <= set(codes)}
    assert pairs == {(rid,'RJS-01') for rid in RELATIONS}
    for rid,(finding,limit) in RELATIONS.items():
        reviews['records'].append(dict(relation_id=rid,claim_id='RJS-01',role='activity_context',
                                       finding=finding,limit=limit,relation_snapshot=relation_snapshot(by_id[rid]),
                                       claim_snapshot=claim_snapshot(claims['RJS-01'],article)))
    apply_literature_context(relations,registry,registry=reviews)
    write(bibliography_path,bibliography)
    write(queue_path,queue)
    write(ROOT/'data/literature_claim_reviews.json',registry)
    write(ROOT/FILE,reviews)
    build_report()
    print('Equation comparisons: 3 claims, 2 probes, 3 relation entries and WWC cross-check')


if __name__ == '__main__':
    main()

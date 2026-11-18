"""Record the 2007 equation-solving comparison and its WWC discrepancies."""
import copy
from math import sqrt

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot

SOURCE = 'RITTLE_JOHNSON_STAR_2007_EQUATION_METHODS'
GUIDE = 'IES_ALGEBRA_2015'
DOI = 'https://doi.org/10.1037/0022-0663.99.3.561'
AUTHOR = 'https://www.researchgate.net/publication/228339259_Does_Comparing_Solution_Methods_Facilitate_Conceptual_and_Procedural_Knowledge_An_Experimental_Study_on_Learning_to_Solve_Equations'
WWC = 'https://ies.ed.gov/ncee/wwc/study/79861'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
DATE = '2026-11-10'
SCOPE = '저자가 공개한 출판본의 초록과 선정 방법·결과 텍스트, 표 3–5의 결과 및 WWC의 가이드와 연구 페이지를 대조했다. PDF 파일과 원본 판면은 미확보다.'
LIMIT = '미국 도시의 선발형 사립학교 한 곳에서 7학년 네 학급을 맡은 교사 한 명이 참여했다. 풀이의 제시 방식과 설명 질문이 함께 달랐다. 단기 즉시 검사이며 현재 국내 과제의 효과와 장기 유지, 방법별 별도 효과는 확인하지 않았다.'
NEXT = '출판본 원본 판면과 원자료, WWC의 대조군 요약이 다른 이유 및 산출 기록을 확인한다. 2012년 별도 연구와 실제 학생 검증을 구별한다.'
SCOPE_NOTE = '같은 식에 대한 풀이의 타당성과 다음 계산의 편의성을 구별한다.'
METHOD_NOTE = '저자 공개 텍스트의 짝 배정·이틀 처치·즉시 검사와 WWC의 표본 및 산출을 대조했다.'
TEXT = dict(url=AUTHOR, uploaded_by='Bethany Rittle-Johnson', article_pdf_obtained=False,
            article_printed_pages=[561,574], selected_sections=[
                dict(section='초록과 표본·배정·제시 조건', printed_pages=[561,564]),
                dict(section='평가와 분석의 결과 영역·사후 결측', printed_pages=[564,567]),
                dict(section='즉시 성과·다층 분석·연습 중 전략, 표 3–5', printed_pages=[567,569]),
            ])
COMPARISON = dict(assigned_n=70, assigned_pairs=[18,17], missing_posttest_n=1,
                  author_imputed_by='regression single imputation with Stata 9 IMPUTE',
                  wwc_n=69, same_analysis=False, wwc_study_url=WWC,
                  guide_pdf_pages=[61,64,70], comparison_description_conflict=True,
                  author_sequential_worked_examples=24, author_sequential_examples_per_sheet=1,
                  wwc_summary_sequential_worked_examples=12, wwc_summary_sequential_examples_per_page=2)
CLAIMS = [
    ('RJS07-01',['9수02-03','9수02-04'],'인쇄563–564쪽의 처치와 표 1 설명',
     '같은 일차방정식의 두 타당한 풀이를 나란히 비교한 조건과, 동형 문제를 사용해 한 장에 풀이 하나씩 읽은 조건을 비교했다. 원논문의 네 번째 유형은 전개보다 번거로운 대안을 포함한다. 첫 연산의 타당성과 계산의 편의성을 따로 판단하는 데 참고한다.',
     '원논문에서는 대조군도 24개 풀이 예와 24개 질문에 노출됐다. WWC의 대조군 요약은 12개 예를 두 개씩 같은 쪽에 제시했다고 적었다. 저자와 WWC의 서술 차이를 보존하고 한쪽의 조건을 다른 쪽에 덮어쓰지 않는다.'),
    ('RJS07-02',['9수02-04'],'인쇄567–569쪽 표 3–5와 가이드 PDF61·64·70',
     '원논문에서는 짝에 속한 학생의 향상을 다층 모형으로 분석했다. 조건 계수는 절차 지식 .08, 유연성 지식 .10, 개념 지식 −.04이며 앞의 두 결과에 유의 표시가 있다. 원논문의 지름길 사용 비율 .17과 .10에 대한 유의 표기는 WWC 연구 페이지의 비유의 판정과 다르다.',
     '원논문은 70명 배정 후 사후 결석 1명의 결과를 추정했고 WWC는 69명을 보고했다. 영역별 계산과 검정이 달라 p값, 원논문 변화량 d와 WWC 효과크기를 서로 대신 쓰지 않는다. 개념 지식의 비유의는 동등성 판정이 아니다.'),
    ('RJS07-03',['9수02-02'],'인쇄563–565쪽의 네 식 유형과 검사 설명',
     '같은 부분식을 묶거나 빼는 풀이에서 괄호 전체가 같아야 모아 쓸 수 있음을 설명한다. 원논문의 예에는 묶어서 계산량을 줄이는 세 유형과, 먼저 빼는 풀이가 오히려 번거로운 유형이 포함됐다.',
     '과제에서 실제로 적은 첫 연산과 연구가 미리 정의한 지름길의 사용률을 구별한다. 한 번의 풀이로 특정 오류의 원인이나 모든 식에서의 효율을 단정할 수 없다.'),
]
OBSERVATIONS = [
    dict(id='RJS07-P1', standard_codes=['9수02-03','9수02-04'],
         question='3(x+2)=x+14에서 먼저 전개한 풀이와 먼저 양변에서 x를 뺀 풀이를 각각 써라. 어느 첫 연산이 다음 계산을 더 간단하게 하는지 설명하라.',
         expected='먼저 전개하면 3x+6=x+14이므로 2x=8, x=4다. 먼저 x를 빼면 3(x+2)−x=14이고 전개·정리해도 2x=8이다. 두 첫 연산 모두 해를 보존하지만 이 식에서는 먼저 전개하면 동류항을 바로 찾을 수 있다.',
         interpretation='같은 해를 얻는 근거, 식에 맞는 선택 이유, 원식 대입을 따로 기록한다. 학생 검증 대기인 자체 과제다.', student_validated=False),
    dict(id='RJS07-P2', standard_codes=['9수02-02','9수02-04'],
         question='앞의 예를 가린 뒤 4(2t−1)+3=2(2t−1)+13을 풀어라. 첫 연산을 왜 골랐는지, 괄호 안이 달라지면 같은 이유를 쓸 수 있는지 설명하라.',
         expected='양변에서 2(2t−1)과 3을 빼면 2(2t−1)=10이므로 t=3이다. 전개해도 같은 해다. 양변의 괄호가 달라지면 같은 부분식으로 묶는 간단한 경로를 그대로 적용할 수 없다.',
         interpretation='먼저 스스로 고른 방법과 도움 뒤의 설명을 구분한다. 전개한 풀이도 타당하면 인정한다. 학생 검증 대기인 자체 과제다.', student_validated=False),
]
RELATIONS = {
    'SEC_9수02-03_C04': ('먼저 x를 빼도 양변이 동치인 까닭과 전개해 먼저 정리하는 선택을 각각 설명한다.',
                         '변형의 타당성과 다음 계산의 편의는 다른 판정이다.'),
    'SEC_9수02-04_C03': ('두 경로에서 x=4가 나오는지 확인하고 원식의 양변 값 18을 대조한다.',
                         '같은 해를 얻었다는 사실만으로 계산량이 같다고 판단하지 않는다.'),
    'REV-9수02-03-1': ('처음 제시한 방정식에서 해의 보존을 설명하고 계수·괄호가 다른 새 문제를 독립적으로 푼다.',
                       '연구의 즉시 비교는 이 과제의 필수 선수성이나 학생의 숙달을 확정하지 않는다.'),
}


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        build_report()
        return
    assert 3*(4+2) == 4+14 == 18
    assert 4*(2*3-1)+3 == 2*(2*3-1)+13
    assert sum(COMPARISON['assigned_pairs'])*2 == COMPARISON['assigned_n']
    assert COMPARISON['assigned_n']-COMPARISON['missing_posttest_n'] == COMPARISON['wwc_n']
    # Approximate the original gain-score d from its rounded means and SDs.
    table3 = {'procedural':(34.0,23.6,20.6,19.0), 'flexibility':(36.7,29.7,16.7,19.7),
              'conceptual':(12.9,15.5,18.9,16.8)}
    reconstructed = {key: round((a-b)/sqrt((35*s1*s1+33*s2*s2)/68),3)
                     for key,(a,b,s1,s2) in table3.items()}
    empirical = dict(design='within_classroom_randomized_dyad_equation_comparison',
                     sample_description='미국 사립 중학교 7학년 70명, 35쌍 배정. 사후 결석 1명은 논문에서 추정 처리했다.',
                     inference_limit=LIMIT, student_outcome_study=True, causal_effect_established=True, local_effect_tested=False)
    corrections = [
        dict(location='원논문 인쇄563–564쪽, WWC 79861 비교 조건과 가이드 표 D.4', issue=CLAIMS[0][-1]),
        dict(location='원논문 표 4, WWC 79861 유연성 결과', issue='같은 .17·.10 사용 비율에 대해 원논문은 유의, WWC 연구 페이지는 비유의로 표시했다. 개별 측정과 가이드 PDF64 각주 h의 표기를 따로 보존한다.'),
        dict(location='가이드 PDF70 정정과 PDF61 표 D.4', issue='2018년 1월 31일 변경은 절차 지식 0.33에 유의 표시를 추가했다. 저자 논문의 Cohen d 또는 지름길 사용에 대한 정정으로 취급하지 않는다.'),
    ]
    notes = dict(source_id=SOURCE,source_url=DOI,date=DATE,reviewer='Codex',
                 source_asset_kind='author_web_text',author_text_review=TEXT,read_scope=SCOPE,
                 original_page_layout_review=False,contains_source_full_text=False,source_pdf_redistributed=False,
                 empirical_scope=empirical,source_corrections=corrections,crosscheck=COMPARISON,
                 reading_log=['선발형 사립 중학교, 짝 단위 배정, 이틀 동안 자료 제시·질문과 즉시 검사 범위를 확인했다.',
                              '두 조건의 예제 노출 수와 제시 단위에 관한 원논문과 WWC의 표현을 대조했다.',
                              '표 3의 변화량, 표 4의 시도당 전략 비율, 표 5의 짝 단위 다층 분석, 가이드 D.4와 각주를 구별했다.'],
                 results=dict(author_table3_gain_d={'procedural':.53,'flexibility':.38,'conceptual':-.14},
                              reconstructed_d_from_rounded_summary=reconstructed,
                              author_table5_condition_coefficient={'procedural':.08,'flexibility':.10,'conceptual':-.04},
                              author_table4_shortcut_use={'proportions':[.17,.10],'significant':True},
                              wwc_page_shortcut_use={'proportions':[.17,.10],'significant':False},
                              guide_effects={'procedural':.33,'flexibility':.40,'conceptual':-.19}))
    bibliography_path = ROOT/'data/sources.json'
    queue_path = ROOT/'data/content_review_queue.json'
    bibliography, queue = load(bibliography_path),load(queue_path)
    entry = dict(id=SOURCE,year=2007,url=DOI,title='Does Comparing Solution Methods Facilitate Conceptual and Procedural Knowledge? An Experimental Study on Learning to Solve Equations',
                 authors=['Rittle-Johnson, B.','Star, J. R.'],kind='일차방정식 풀이 비교의 짝 단위 배정 연구',
                 review_scope=SCOPE,does_not_establish=LIMIT,next_review=NEXT,
                 supports='여러 풀이의 타당성과 효율, 연구와 WWC의 대조 조건·분석 차이.')
    write(ROOT/NOTES,notes)
    bibliography.append(entry)
    article = dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date=DATE,
                   snapshot_kind='authored_review_notes',source_asset_kind='author_web_text',
                   author_text_review=TEXT,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),
                   redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(entry),
                   display=dict(title=entry['title'],url=DOI,authors_year='Rittle-Johnson·Star, 2007'),
                   read_scope=SCOPE,scope_note=SCOPE_NOTE,method_note=METHOD_NOTE,
                   limits=LIMIT,empirical_scope=empirical,observations=OBSERVATIONS,
                   independent_review=False,student_validated=False,
                   editorial_action='근거 3건, 관찰 과제 2개, 관계별 대조 3건을 추가했다.')
    registry['sources'][SOURCE] = article
    for cid,codes,location,support,limit in CLAIMS:
        registry['claims'].append(dict(
            id=cid,source_id=SOURCE,role='empirical_result_with_scope',standard_codes=codes,
            locations=[f'{AUTHOR} {location}', WWC],support=support,does_not_establish=limit,
            empirical_scope=empirical,independent_review=False,student_validated=False,
            target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes}))
    ids = [row[0] for row in CLAIMS]
    queue['literature_review'].append(dict(source=entry,status='self_read_claim_mapping',
                                           evidence_file='data/literature_claim_reviews.json',
                                           claim_evidence_fields=['처치·대조 조건','배정과 분석 분모','측정과 효과크기의 차이'],claim_ids=ids))

    guide = registry['sources'][GUIDE]
    old_guide = copy.deepcopy(guide)
    guide_entry = next(row for row in bibliography if row['id']==GUIDE)
    guide_entry['next_review'] = '2007년과 2009년 두 저자의 방정식 풀이 비교를 각각 대조했다. 2007년 대조군 설명과 전략 사용 판정의 차이, 2012년 연구와 기타 원논문·원자료, 남은 판면·자료와 독립·학생 검증은 후속 범위다.'
    guide['bibliography_snapshot'] = digest(guide_entry)
    guide['primary_source_crosschecks'].append(dict(source_id=SOURCE,claim_ids=ids,snapshot_file=NOTES,
                                                     snapshot_sha256=article['snapshot_sha256'],**COMPARISON))
    next(row for row in queue['literature_review'] if row['source']['id']==GUIDE)['source'] = guide_entry
    relations = load(ROOT/'data/revised_relations.json')['relations']
    by_id = {row['id']:row for row in relations}
    claims = {row['id']:row for row in registry['claims']}
    reviews = load(ROOT/FILE)
    for row in reviews['records']:
        claim = claims[row['claim_id']]
        if claim['source_id']==GUIDE:
            assert row['claim_snapshot']==claim_snapshot(claim,old_guide)
            row['claim_snapshot'] = claim_snapshot(claim,guide)
    pairs = {(row['id'],cid) for row in relations for cid,codes,*_ in CLAIMS
             if all(row[key].startswith('standard:') for key in ('from','to'))
             and {row[key][9:] for key in ('from','to')} <= set(codes)}
    assert pairs == {(rid,'RJS07-01') for rid in RELATIONS}
    for rid,(finding,limit) in RELATIONS.items():
        reviews['records'].append(dict(relation_id=rid,claim_id='RJS07-01',role='activity_context',
                                       finding=finding,limit=limit,relation_snapshot=relation_snapshot(by_id[rid]),
                                       claim_snapshot=claim_snapshot(claims['RJS07-01'],article)))
    apply_literature_context(relations,registry,registry=reviews)
    write(bibliography_path,bibliography)
    write(queue_path,queue)
    write(ROOT/'data/literature_claim_reviews.json',registry)
    write(ROOT/FILE,reviews)
    build_report()
    print('2007 equation comparisons: 3 claims, 2 probes, 3 relation entries')


if __name__ == '__main__':
    main()

"""Record the prior-knowledge study without conflating its WWC subgroup contrasts."""
import copy
from fractions import Fraction

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot

SOURCE = 'RITTLE_JOHNSON_STAR_DURKIN_2009_PRIOR_ALGEBRA'
GUIDE = 'IES_ALGEBRA_2015'
DOI = 'https://doi.org/10.1037/a0016026'
AUTHOR = 'https://www.researchgate.net/publication/241843433_The_Importance_of_Prior_Knowledge_When_Comparing_Examples_Influences_on_Conceptual_and_Procedural_Knowledge_of_Equation_Solving'
WWC = 'https://ies.ed.gov/ncee/wwc/study/79863'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
DATE = '2026-11-10'
SCOPE = '저자 공개 출판본의 초록·선정 방법과 표 3·4 및 사후·유지 결과를 IES 가이드 D.4의 하위 분석과 대조했다. 출판본 PDF와 원본 판면은 확보 대기다.'
LIMIT = '미국 한 도시 중학교 11개 학급에서 짝에 수업 조건을 무작위 배정했다. 사전 대수 사용은 관찰된 분류다. 국내 학생을 한 번의 시도로 분류하거나 지도 순서·개별 과제 효과를 확정하는 근거가 아니다.'
NEXT = '출판본 PDF·판면·나머지 표와 원자료, WWC 연구 페이지의 전체 행과 집계 근거를 확인한다. 독립 검토와 학생 반응은 별도로 기록한다.'
TEXT = dict(url=AUTHOR,uploaded_by='Bethany Rittle-Johnson',article_pdf_obtained=False,
            article_printed_pages=[836,852],selected_sections=[
                dict(section='초록과 연구 결과 요약',printed_pages=[836,836]),
                dict(section='표본과 짝 배정·개입·측정 방법',printed_pages=[838,840]),
                dict(section='결측, 사전 분류, 사후 결과와 표 3·4',printed_pages=[842,845]),
                dict(section='유지 검사 조건과 결과의 선정 문단',printed_pages=[846,847]),
            ])
COMPARISON = dict(participated_n=239,excluded={'missed_two_sessions':1,'declined_packets':2},
                  author_analysis_n=236,author_condition_n={'methods':80,'problem_types':78,'sequential':78},
                  observed_pretest_attempt_pct={'at_least_once':59,'never':41},attempt_could_be_incorrect=True,
                  guide_n={'attempted':101,'not_observed':55},guide_contrast=['methods','sequential'],
                  same_analysis=False,guide_pdf_pages=[62,64],wwc_url=WWC)
CLAIMS = [
    ('RJSD09-01',['9수02-03','9수02-04'],'인쇄838–843쪽, 표본·사전 분류',
     '연구는 사전 검사에서 대수적 방법을 한 번이라도 시도했는지를 기록했다. 틀린 변형도 시도에 들어간다. 방정식에서 먼저 쓴 접근, 각 변형이 해를 보존하는지, 최종 해를 구분해 기록하는 데 참고한다.',
     '사전의 대수 사용은 관찰된 분류이며 무작위로 배정한 능력 수준이 아니다. 사용하지 않은 사례가 지식 부재나 현재 기준 미숙달을 뜻하지 않는다.'),
    ('RJSD09-02',['9수02-04'],'인쇄843–845쪽 표 4와 가이드 PDF62·64',
     '원논문의 세 조건 분석에서 사후 절차 지식과 실제 전략 사용에 조건×사전 대수 사용 상호작용이 있었다. 유연성 지식과 개념 지식의 상호작용에는 각각 p=.080과 p=.085가 보고됐다. WWC 가이드는 방법 비교와 순차 제시의 두 조건만 뽑아 사전 대수 사용별 101명·55명으로 제시했다.',
     '짝 배정은 수업 조건에만 적용됐다. 원논문의 세 조건 모형과 가이드의 두 집단별 효과크기는 서로 대신 쓸 수 없다. 두 결과로 모든 학습자에게 일률적인 제시 시점을 정하지 않는다.'),
    ('RJSD09-03',['9수02-04'],'인쇄842–847쪽 표 3과 유지 검사',
     '사후에는 풀이를 적을 수 있었지만 컴퓨터 유지 검사에서는 풀이를 남길 수 없어 실제 전략 사용을 채점하지 않았다. 후속 과제에서 풀이를 보존한 경우에만 사용한 전략을 판정하고, 답만 있으면 풀이 과정은 확인 불가로 기록한다.',
     '유지 검사에서 개념 지식 자료의 37%가 빠져 추정으로 채웠다. 응답 양식과 결측을 고려해 유지 정답률을 전략 유지 또는 학생 전체의 효과로 확대하지 않는다.'),
]
OBSERVATIONS = [
    dict(id='RJSD09-P1',standard_codes=['9수02-03','9수02-04'],
         question='5x+6=2x+18을 원하는 방법으로 풀고 처음 한 일을 적어라. 다음으로 5x+6=2x+18에서 왼쪽만 바꾼 3x+6=2x+18이 같은 해를 갖는지 확인하라.',
         expected='양변에서 2x와 6을 빼면 3x=12이므로 x=4다. 값을 찾아 원식에 대입하는 방법도 x=4가 해임을 확인한다. 왼쪽만 2x를 뺀 식에서는 x=12가 되어 해가 달라진다.',
         interpretation='숫자 대입·대수 시도·무응답과 첫 변형의 타당성·해의 정답을 따로 기록한다. 첫 반응 한 건으로 학생을 능력 집단에 배정하지 않는다. 학생 검증 대기인 자체 과제다.',student_validated=False),
    dict(id='RJSD09-P2',standard_codes=['9수02-04'],
         question='−3(y−2)=y+6을 먼저 풀어라. 답과 첫 변형을 남긴 뒤 −3(y−2)=(y−2)+12에서 괄호를 전개하거나 공통 부분식을 먼저 빼는 풀이를 비교하라.',
         expected='첫 식은 −3y+6=y+6에서 y=0이다. 둘째 식은 양변에서 y−2를 빼면 −4(y−2)=12여서 y=−1이다. 전개해도 같은 해다. 각각 원식에 대입하면 양변이 같다.',
         interpretation='처음 시도와 두 풀이를 본 뒤의 설명을 분리한다. 정답만 적힌 경우 사용 전략은 확인 불가로 둔다. 학생 검증 대기인 자체 과제다.',student_validated=False),
]
RELATIONS = {
    'SEC_9수02-03_C04': ('처음 쓴 접근과 변형이 양변에 함께 적용됐는지 별도로 확인한다.','대수 시도에는 오답도 포함되므로 시도만으로 등식 변형의 이해를 판단하지 않는다.'),
    'SEC_9수02-04_C03': ('원래 식에 x=4를 대입하고, 한쪽만 바꾼 식에서 나온 x=12를 따로 검산한다.','대입으로 해를 확인하는 것과 각 변형이 해집합을 보존하는 것은 다른 설명이다.'),
    'REV-9수02-03-1': ('첫 시도, 양변에 한 연산, 최종 해를 따로 기록한다.','연구의 사전 시도 분류는 관찰 변수이며 현재 과제의 필수 선수성을 입증하지 않는다.'),
}


def main():
    registry=load_registry()
    if SOURCE in registry['sources']:
        build_report()
        return
    assert sum(COMPARISON['author_condition_n'].values())==COMPARISON['author_analysis_n']
    assert COMPARISON['participated_n']-sum(COMPARISON['excluded'].values())==COMPARISON['author_analysis_n']
    assert 5*4+6==2*4+18 and 3*4+6!=2*4+18
    assert 3*12+6==2*12+18 and 5*12+6!=2*12+18
    assert -3*(0-2)==0+6 and -3*(-1-2)==(-1-2)+12
    assert (Fraction('.03')+Fraction('.21'))/2==Fraction('.12')
    assert (Fraction('-.37')+Fraction('-.33'))/2==Fraction('-.35')
    empirical=dict(design='within_classroom_randomized_dyad_comparison_with_observed_pretest_moderator',
                   sample_description='한 학교의 7~8학년 239명 참여·236명 분석. 짝 단위 배정은 세 수업 조건에만 적용했다.',
                   inference_limit=LIMIT,student_outcome_study=True,local_effect_tested=False)
    notes=dict(source_id=SOURCE,source_url=DOI,date=DATE,reviewer='Codex',
               source_asset_kind='author_web_text',author_text_review=TEXT,read_scope=SCOPE,
               original_page_layout_review=False,contains_source_full_text=False,source_pdf_redistributed=False,
               empirical_scope=empirical,crosscheck=COMPARISON,
               reading_log=['같은 반의 짝 배정과 참여·제외·분석 인원을 확인했다.',
                            '틀린 대수 풀이도 사전 사용에 포함되며, 사후 결과 영역별 상호작용과 유지 검사 결측을 구분했다.',
                            '가이드 D.4의 두 조건 하위 분석 및 각주 m–o를 세 조건 원논문과 대조했다.'],
               source_corrections=[
                   dict(location='원논문 인쇄843쪽과 가이드 PDF62',issue='가이드가 사전 지식으로 요약한 분류는 원논문에서 대수적 방법을 사전 검사에 시도했는지다. 옳은 풀이와 틀린 풀이가 모두 포함된다.'),
                   dict(location='원논문 표 3과 가이드 PDF64 각주 m–o',issue='전략 사용의 유지 결과는 채점되지 않았다. WWC 효과크기는 추정값이 포함된 표준편차를 사용했고, 하위 전략 결과의 유의 표기는 별도다.')],
               author_posttest_interaction={'procedural':{'F':8.466,'df':[2,213],'p':'<.001'},
                                            'flexibility_use':{'F':7.292,'df':[2,210],'p':'<.001'},
                                            'flexibility_knowledge':{'F':2.548,'df':[2,224],'p':.080},
                                            'conceptual':{'F':2.497,'df':[2,226],'p':.085}},
               retention={'strategy_use_scored':False,'conceptual_missing_pct':37,'conceptual_imputed':True},
               guide_g={'attempted':{'conceptual':-.13,'procedural':.19,'flexibility':.12,'flexibility_knowledge':.03,'flexibility_use':.21},
                        'not_observed':{'conceptual':-.42,'procedural':-.44,'flexibility':-.35,'flexibility_knowledge':-.37,'flexibility_use':-.33}},
               guide_flexibility_submeasures_significant=False)
    bp=ROOT/'data/sources.json'
    qp=ROOT/'data/content_review_queue.json'
    bibliography,queue=load(bp),load(qp)
    entry=dict(id=SOURCE,year=2009,url=DOI,
               title='The importance of prior knowledge when comparing examples: Influences on conceptual and procedural knowledge of equation solving',
               authors=['Rittle-Johnson, B.','Star, J. R.','Durkin, K.'],kind='사전 대수 사용에 따른 풀이 비교 연구',
               review_scope=SCOPE,does_not_establish=LIMIT,next_review=NEXT,supports='사전 시도·풀이 타당성·사후 전략 사용·유지 검사의 구분.')
    write(ROOT/NOTES,notes)
    bibliography.append(entry)
    article=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date=DATE,
                 snapshot_kind='authored_review_notes',source_asset_kind='author_web_text',author_text_review=TEXT,
                 snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),redistribution_license='workspace_authored_notes',
                 bibliography_snapshot=digest(entry),display=dict(title=entry['title'],url=DOI,authors_year='Rittle-Johnson·Star·Durkin, 2009'),
                 read_scope=SCOPE,scope_note='사전 검사에서의 접근 시도와 풀이의 성취를 따로 기록한다.',
                 method_note='세 조건의 짝 배정, 관찰된 사전 지표, WWC의 두 조건 하위 비교를 대조했다.',
                 limits=LIMIT,empirical_scope=empirical,observations=OBSERVATIONS,independent_review=False,student_validated=False,
                 editorial_action='근거 3건과 관찰 과제 2개, 관계별 대조 3건을 추가했다.')
    registry['sources'][SOURCE]=article
    for cid,codes,location,support,limit in CLAIMS:
        registry['claims'].append(dict(id=cid,source_id=SOURCE,role='empirical_result_with_scope',standard_codes=codes,
            locations=[f'{AUTHOR} {location}',DOI],support=support,does_not_establish=limit,
            empirical_scope=empirical,independent_review=False,student_validated=False,
            target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes}))
    ids=[row[0] for row in CLAIMS]
    queue['literature_review'].append(dict(source=entry,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',
         claim_evidence_fields=['사전 시도의 정의','짝 배정과 분석 분모','사후·유지 검사'],claim_ids=ids))
    guide=registry['sources'][GUIDE]
    old_guide=copy.deepcopy(guide)
    guide_entry=next(row for row in bibliography if row['id']==GUIDE)
    guide_entry['next_review']='2007년과 2009년 두 저자의 연구, 2009년 사전 지식 연구와 2012년 공식 WWC 심사·초록을 각각 대조했다. 남은 본문·판면과 다른 원연구, 원자료 및 실제 검증을 확인한다.'
    guide['bibliography_snapshot']=digest(guide_entry)
    guide['primary_source_crosschecks'].append(dict(source_id=SOURCE,claim_ids=ids,snapshot_file=NOTES,
                                                    snapshot_sha256=article['snapshot_sha256'],**COMPARISON))
    next(row for row in queue['literature_review'] if row['source']['id']==GUIDE)['source']=guide_entry
    relations=load(ROOT/'data/revised_relations.json')['relations']
    by_id={row['id']:row for row in relations}
    claims={row['id']:row for row in registry['claims']}
    reviews=load(ROOT/FILE)
    for row in reviews['records']:
        claim=claims[row['claim_id']]
        if claim['source_id']==GUIDE:
            assert row['claim_snapshot']==claim_snapshot(claim,old_guide)
            row['claim_snapshot']=claim_snapshot(claim,guide)
    pairs={(row['id'],cid) for row in relations for cid,codes,*_ in CLAIMS
           if all(row[key].startswith('standard:') for key in ('from','to'))
           and {row[key][9:] for key in ('from','to')} <= set(codes)}
    assert pairs=={(rid,'RJSD09-01') for rid in RELATIONS}
    for rid,(finding,limit) in RELATIONS.items():
        reviews['records'].append(dict(relation_id=rid,claim_id='RJSD09-01',role='activity_context',
                                       finding=finding,limit=limit,relation_snapshot=relation_snapshot(by_id[rid]),
                                       claim_snapshot=claim_snapshot(claims['RJSD09-01'],article)))
    apply_literature_context(relations,registry,registry=reviews)
    write(bp,bibliography)
    write(qp,queue)
    write(ROOT/'data/literature_claim_reviews.json',registry)
    write(ROOT/FILE,reviews)
    build_report()
    print('2009 prior algebra study: 3 claims, 2 probes and 3 relation entries')


if __name__=='__main__':
    main()

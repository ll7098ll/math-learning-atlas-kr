"""Bind WWC study 79864 and the 2012 article abstract to scoped observations."""
import copy
import html
import re

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot

SOURCE = 'WWC_79864_EQUATION_COMPARISON_2012'
GUIDE = 'IES_ALGEBRA_2015'
URL = 'https://ies.ed.gov/ncee/wwc/study/79864'
DOI = 'https://doi.org/10.1111/j.2044-8279.2011.02037.x'
ABSTRACT = 'https://pubmed.ncbi.nlm.nih.gov/22881048/'
CACHE = ROOT/'tmp/literature/wwc-79864-2012.html'
SHA = '33bf32837ac58070622261020f3089877ad795297f2477b228214699c3703f8b'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
DATE = '2026-11-10'
SCOPE = 'WWC 79864 공식 웹 검토의 두 비교·10개 결과 행과 2019년 개정 가이드 D.4, 2012년 출판사 초록을 대조했다. 2012년 원논문 전체와 판면은 확보 대기다.'
LIMIT = '미국 공립 중학교 두 곳의 8학년을 대상으로 한 약 3시간의 다단계 방정식 수업이다. 두 WWC 비교는 대조군을 공유하며 개입 순서와 예제 짝이 함께 다르다. 국내 과제 효과와 필수 순서는 검증 대기다.'
FOLLOWUP = '출판본 436–455쪽의 전체 방법·표·그림과 원자료, 한 달 개념 지식 방향 차이의 산출 근거, 독립 검토와 실제 학생 반응을 확인한다.'

# Comparison, measure, assessment time, analytic n, two WWC means, significance.
OUTCOMES = [
    ('immediate','conceptual','1 Day',124,26.79,29.10,False),
    ('immediate','conceptual','1 Month',118,25.18,28.81,False),
    ('immediate','flexibility_use','1 Day',124,27.17,15.00,True),
    ('immediate','flexibility_knowledge','1 Day',124,50.87,42.63,False),
    ('immediate','flexibility_use','1 Month',118,23.51,9.79,True),
    ('immediate','flexibility_knowledge','1 Month',118,47.42,40.00,False),
    ('immediate','procedural','1 Day',124,38.09,34.20,False),
    ('immediate','procedural','1 Month',118,35.59,31.07,False),
    ('delayed','flexibility_knowledge','2 Days',115,41.09,42.63,False),
    ('delayed','flexibility_use','2 Days',115,9.91,15.00,False),
]
CLAIMS = [
    ('WWC79864-01','두 풀이를 처음부터 비교한 조건과 늦게 다른 풀이에 노출된 조건의 비교',
     'WWC의 124명 사후와 118명 한 달 비교에서는 실제 전략 사용에 유의 표시가 있었다. 별도의 유연성 지식과 개념·절차 지식에는 같은 비교에서 유의 표시가 없었다. 독립 풀이의 첫 연산을 먼저 보존하고, 이후에 여러 방법을 알아보고 평가하는 반응을 따로 묻는 설계에 참고한다.',
     '198명은 논문 초록의 전체 배정 수이며 두 집단만 포함한 WWC의 분석 인원과 다르다. 지식 검사의 비유의는 동등성을 뜻하지 않는다. 현지 비교의 결과를 현재 국내 과제의 효과로 확대하지 않는다.'),
    ('WWC79864-02','두 풀이를 나중에 비교한 조건과 늦게 다른 풀이에 노출된 조건의 비교',
     '115명 비교에서 첫날은 서로 다른 식에 같은 방법을, 둘째 날은 같은 식에 다른 방법을 나란히 제시했다. 지식과 실제 사용 모두에 유의 표시가 없었다. 활동을 비교할 때 두 풀이를 언제 보았는지와 그때 무엇을 나란히 보았는지 기록한다.',
     '이 비교는 높은 탈락률로 WWC 설계 판정에 유보가 붙었다. 앞선 124명 비교와 대조군을 공유하며 두 효과를 합산하거나 시점 하나의 인과 효과로 분리하지 않는다.'),
]
OBSERVATIONS = [
    dict(id='WWC79864-P1',standard_codes=['9수02-03','9수02-04'],
         question='먼저 혼자 6(2x+1)=2(2x+1)+20을 풀고 첫 연산을 적어라. 그 기록을 남긴 뒤 전개하는 풀이와 양변에서 2(2x+1)을 빼는 풀이의 첫 단계를 각각 설명하라.',
         expected='공통 부분식을 빼면 4(2x+1)=20에서 x=2다. 전개하면 12x+6=4x+22에서 8x=16이므로 같은 해다. 양변에서 같은 식을 빼거나 각 항을 동치인 식으로 전개하면 해를 보존한다.',
         interpretation='보기 전의 첫 연산·정답과, 비교 자료를 본 뒤 두 방법을 설명한 응답을 분리한다. 첫 풀이를 사후에 고쳐 적지 않는다. 자체 설계이며 학생 검증 대기다.',
         student_validated=False),
    dict(id='WWC79864-P2',standard_codes=['9수02-02','9수02-04'],
         question='5(t+4)+2(t+4)=42와 5(t+4)+2(t+3)=42를 차례로 풀어라. 첫 식의 첫 단계를 두 번째 식에 그대로 쓸 수 있는지 설명하라.',
         expected='첫 식은 7(t+4)=42여서 t=2다. 둘째 식은 괄호가 달라 7(t+4)로 묶을 수 없다. 전개하면 7t+26=42여서 t=16/7이다.',
         interpretation='예의 순서와 제시한 비교를 기록하고, 풀이 선택·타당성·정답을 따로 표시한다. 자체 설계이며 학생 검증 대기다.',
         student_validated=False),
]


def verify_official_rows():
    assert sha(CACHE)==SHA
    labels = {'Conceptual knowledge subtest of study generated test':'conceptual',
              'Procedural knowledge subtest of study generated test':'procedural',
              'flexible use of procedures':'flexibility_use','flexibility knowledge':'flexibility_knowledge'}
    rows = []
    for body in re.findall(r'<tr\b[^>]*>(.*?)</tr>', CACHE.read_text(encoding='utf-8'), flags=re.S):
        fields = [' '.join(html.unescape(re.sub(r'<[^>]+>',' ',value)).split())
                  for value in re.findall(r'<td\b[^>]*>(.*?)</td>',body,flags=re.S)]
        if len(fields)<7 or 'Comparison of Procedures vs. Delayed Exposure' not in fields[3]:
            continue
        comparison = 'immediate' if 'Immediate Comparison' in fields[3] else 'delayed'
        n = int(re.search(r'(\d+) students',fields[3])[1])
        assert fields[6] in ('Yes','No')
        rows.append((comparison,labels[fields[0]],fields[2],n,float(fields[4]),float(fields[5]),fields[6]=='Yes'))
    assert rows==OUTCOMES


def main():
    registry=load_registry()
    if SOURCE in registry['sources']:
        build_report()
        return
    verify_official_rows()
    assert 6*(2*2+1)==2*(2*2+1)+20
    assert 5*(2+4)+2*(2+4)==42
    assert 5*(16+4*7)+2*(16+3*7)==42*7
    empirical=dict(design='wwc_review_of_randomized_equation_comparison',
                   sample_description='논문 초록은 미국 공립 중학교 두 곳의 8학년 198명 배정을 보고한다. WWC의 쌍별 분석은 124명·118명과 별도 115명이다.',
                   inference_limit=LIMIT,student_outcome_study=True,local_effect_tested=False)
    crosscheck=dict(article_total_assigned_n=198,immediate_comparison_n={'1 Day':124,'1 Month':118},
                    delayed_comparison_n={'2 Days':115},shared_comparison_group=True,article_full_text_obtained=False,
                    official_html_rows=10,guide_pdf_pages=[62,64],doi=DOI)
    corrections=[
        dict(location='가이드 PDF64 각주 j와 WWC 79864의 한 달 개념 지식 행',
             issue='가이드의 효과크기는 +0.14이고 WWC 연구 페이지의 평균은 즉시 비교 집단 25.18, 대조 집단 28.81이다. 분석·산출 기록을 확인하기 전 부호를 임의 정정하지 않는다.'),
        dict(location='가이드 PDF62·64와 WWC 79864의 두 심사 결과',
             issue='115명 비교의 표 본문은 유보 없는 연구 묶음 안에 보이지만 각주 l 및 연구 페이지는 높은 탈락률 때문에 유보를 명시한다. 그 비교의 판정은 해당 각주와 연구 페이지를 따라 표기한다.'),
    ]
    notes=dict(source_id=SOURCE,source_url=URL,date=DATE,reviewer='Codex',
               source_asset_kind='publisher_html',source_asset_sha256=SHA,source_asset_redistributed=False,
               pdf_read=False,original_page_layout_review=False,source_pdf_redistributed=False,
               contains_source_full_text=False,read_scope=SCOPE,empirical_scope=empirical,
               publisher_abstract={'doi':DOI,'crosscheck_url':ABSTRACT,'article_full_text_obtained':False},
               source_corrections=corrections,crosscheck=crosscheck,
               reading_log=['공식 웹 자료의 두 비교 조건, 심사 판정 및 결과표 10행을 대조했다.',
                            '출판사 초록에서 전체 배정과 세 수업 조건, 사전·사후·한 달 평가 범위를 확인했다.',
                            '가이드 표 D.4와 각주 j–l에서 결과 영역과 별도 측정의 차이, 탈락과 부호의 차이를 확인했다.'],
               outcomes=[dict(comparison=c,measure=m,timing=t,n=n,wwc_means=[a,b],significant=s)
                         for c,m,t,n,a,b,s in OUTCOMES],
               guide_flexibility_g=dict(immediate_domain=.37,retention_domain=.42,delayed_domain=-.15),
               guide_delayed_conceptual_g=.14,wwc_month_conceptual_direction='negative_means_difference',
               unresolved_followup=FOLLOWUP)
    bp=ROOT/'data/sources.json'
    qp=ROOT/'data/content_review_queue.json'
    bibliography,queue=load(bp),load(qp)
    entry=dict(id=SOURCE,year=2019,url=URL,
               title='WWC Study 79864: Developing Procedural Flexibility (2012 study)',
               authors=['What Works Clearinghouse'],kind='공식 연구 심사 결과와 출판사 초록의 대조',
               review_scope=SCOPE,does_not_establish=LIMIT,next_review=FOLLOWUP,
               supports='즉시·지연 풀이 비교의 분모와 조건 및 전략 사용·전략 지식 구분.')
    write(ROOT/NOTES,notes)
    bibliography.append(entry)
    review=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date=DATE,
                snapshot_kind='authored_review_notes',source_asset_kind='publisher_html',
                source_asset_sha256=SHA,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),
                redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(entry),
                display=dict(title=entry['title'],url=URL,authors_year='WWC 2019 검토 · Rittle-Johnson 외 2012 연구'),
                read_scope=SCOPE,scope_note='공식 연구 심사와 저자 초록의 범위를 구별한다.',
                method_note='두 쌍별 비교의 표본·조건·시점과 열 개 결과를 확인했다.',
                limits=LIMIT,empirical_scope=empirical,observations=OBSERVATIONS,
                independent_review=False,student_validated=False,
                editorial_action='일차방정식 기준에 문헌 근거 2건, 자체 관찰 과제 2개를 연결했다.')
    registry['sources'][SOURCE]=review
    for cid,location,support,limit in CLAIMS:
        registry['claims'].append(dict(id=cid,source_id=SOURCE,role='empirical_result_with_scope',
            locations=[f'{URL} {location}',DOI],support=support,does_not_establish=limit,
            standard_codes=['9수02-04'],target_snapshots={'revision:9수02-04':digest(target_value('revision:9수02-04'))},
            empirical_scope=empirical,independent_review=False,student_validated=False))
    ids=[row[0] for row in CLAIMS]
    queue['literature_review'].append(dict(source=entry,status='self_read_claim_mapping',
        evidence_file='data/literature_claim_reviews.json',claim_evidence_fields=['분모와 비교 조건','전략 사용·지식','가이드 표와 공식 웹 차이'],claim_ids=ids))

    guide=registry['sources'][GUIDE]
    old_guide=copy.deepcopy(guide)
    guide_entry=next(row for row in bibliography if row['id']==GUIDE)
    guide_entry['next_review']='2007·2009년 두 저자의 연구와 2012년의 공식 WWC 심사·출판사 초록을 대조했다. 2012년 전체 본문과 다른 원연구, 원자료, 후속 판면·자료 및 실제 검증을 확인한다.'
    guide['bibliography_snapshot']=digest(guide_entry)
    guide.setdefault('official_review_crosschecks',[]).append(dict(source_id=SOURCE,claim_ids=ids,snapshot_file=NOTES,
         snapshot_sha256=review['snapshot_sha256'],**crosscheck))
    next(row for row in queue['literature_review'] if row['source']['id']==GUIDE)['source']=guide_entry
    relations=load(ROOT/'data/revised_relations.json')['relations']
    claims={row['id']:row for row in registry['claims']}
    reviews=load(ROOT/FILE)
    for row in reviews['records']:
        claim=claims[row['claim_id']]
        if claim['source_id']==GUIDE:
            assert row['claim_snapshot']==claim_snapshot(claim,old_guide)
            row['claim_snapshot']=claim_snapshot(claim,guide)
    assert not any(row['from']==row['to']=='standard:9수02-04' for row in relations)
    apply_literature_context(relations,registry,registry=reviews)
    write(bp,bibliography)
    write(qp,queue)
    write(ROOT/'data/literature_claim_reviews.json',registry)
    write(ROOT/FILE,reviews)
    build_report()
    print('WWC 79864: verified 10 outcome rows, 2 claims and 2 observation tasks')


if __name__ == '__main__':
    main()

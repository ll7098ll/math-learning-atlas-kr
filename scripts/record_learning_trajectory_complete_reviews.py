"""Close the selected-body gaps for two trials, retaining original notes and limits."""
import copy,hashlib,json
from literature_review import ROOT,load_registry,digest
from relation_literature_review import claim_snapshot
from check_learning_trajectory_trial_models import check

SPECS=[('length','SARAMA_ET_AL_2021_LENGTH_SEQUENCE',15,9),('shape','CLEMENTS_ET_AL_2019_SHAPE_SEQUENCE',22,16)]
NOTES=[f'data/literature_evidence/{sid}_complete_visual_review_notes.json' for _,sid,_,_ in SPECS]
LENGTH_LIMIT='5개 학교16개 교실의 유치원 길이 과제에 관한 단기 조건 비교다. 정순·역순 모두 계획10회×12분의 개별 수업이지만 순서와 반응별 비계·활동 조정이 함께 달랐고 실제 연습량·간격의 동일성은 입증되지 않았다. 정규 수업 비교에는 길이 내용과 개별 관심도 함께 달랐다. 확률적 사고 수준을 모든 학생의 필수 경로로 확대하지 않으며 국내 단위 과제·다른 측정량·독립 지연 전이는 확인하지 않았다.'
SHAPE_LIMIT='15개 유아 교실에서 소집단을 조건에 배정한5주간 두 활성 지도 조건의 비교다. 순서와 난도를 낮추는 비계가 함께 달라 각 요소의 독립 효과가 아니다. 결과는 정답·과정 행동을 포함한Rasch척도이며 무처치 대비 전체 효과·장기 유지·모든 공간 과제의 전이·국내 과제 효과를 확인하지 않았다. 비유의 조절변수는 모든 집단의 동일 효과를 입증하지 않으며 단계 순서가 모든 경우의 필요조건은 아니다.'

def read(p):return json.loads((ROOT/p).read_bytes())
def write(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def main():
    l=load_registry();old=copy.deepcopy(l);bib=read('data/sources.json');queue=read('data/content_review_queue.json');model=check()
    assert len(l['sources'])==176 and len(l['claims'])==1055 and not any((ROOT/p).exists() for p in NOTES)
    for index,(label,sid,total,new_count) in enumerate(SPECS):
        s=l['sources'][sid];prior=read(s['snapshot_file']);p=read(f'tmp/literature/lt-complete-20261118/{label}/reading-progress.json');a=read(f'tmp/literature/lt-complete-20261118/{label}/acquisition.json')
        assert p['reading_completed'] and p['actually_viewed_pdf_pages_this_turn']==list(range(1,total+1)) and len(p['new_visual_pdf_pages'])==new_count and p['new_full_extracted_text_pages_read']==0
        assert p['source_pdf_sha256']==a['asset']['sha256']==s['source_pdf_sha256']==sha(f'tmp/literature/lt-complete-20261118/{label}/source.pdf')
        for page,h in p['rendered_page_sha256'].items():assert sha(f'tmp/literature/lt-complete-20261118/{label}/rendered/page-{int(page):02d}.png')==h
        limit=LENGTH_LIMIT if label=='length' else SHAPE_LIMIT
        scope=f'ERIC의 출판 형식 PDF{total}쪽 전체 본문·표·그림·참고문헌을 실제 판면으로 읽었다. 이전 선정9쪽의 관련 추출문 대조는 보존하며 이번 새 전문 추출문 독해는0쪽이다. 기존6판면과 새{new_count}판면을 합친 범위다.'
        if label=='length':scope+=' 표1–9·그림1·감사·주·저자 소개를 포함한다.'
        else:scope+=' 그림1의 이어지는 두 판면·그림2·표1–2·연구비/이해관계 주를 포함한다.'
        empirical=copy.deepcopy(s['empirical_scope']);empirical['inference_limit']=limit
        if label=='length':empirical['sample_description']='5개 학교16개 교실의 사전187명·사후185명이다. 사후 표2의 정규57명·정순69명·역순59명을 위치에 귀속한다. 초록189명·다른 표의 인원·학교 유형별 본문 인원은 불일치가 남아 있다.'
        else:empirical['sample_description']='15개 교실에서 소집단을 조건에 무작위 배정했다. 동의152명 중 배정 전1명과 배정 후 사후자료6명을 제외해 순서 지도82명·목표 수준 지도63명,145명을 분석했다.'
        s['snapshot_history']=copy.deepcopy(s.get('snapshot_history',[]))+[dict(snapshot_file=s['snapshot_file'],snapshot_sha256=s['snapshot_sha256'],date=s['date'],read_scope=s['read_scope'])]
        s.update(date='2026-11-18',read_scope=scope,visual_pdf_pages=list(range(1,total+1)),empirical_scope=empirical,limits=limit,
                 scope_note='전체 판면 대조에서 지도 조건 묶음·배정 단위·평가 시행/코드·집계 분모·추정량을 구별했다. 저자도 더 유용한 순서와 모든 경우의 필요조건을 구별한다. 원자료·공식 정오표·국내 학생 검증은 미확인이다.',
                 method_note='PDF 전체 판면과 표/그림의 문맥을 읽고 표시된 집계 및 자체 반례를 정확 유리수로 점검했다. 원 학생 반응이나Rasch/Bayesian모형을 재추정하지 않았다.',
                 editorial_action=f'2026-11-18: 전체{total}판면 대조로 기존 주장4건의 범위·한계를 보완했다. 새 출처·주장·과제·관계는0이다.')
        n=copy.deepcopy(prior);n.update(date=s['date'],read_scope=scope,empirical_scope=empirical,previous_review=old['sources'][sid],previous_snapshot_file=s['snapshot_file'],previous_snapshot_sha256=s['snapshot_sha256'],
            visual_pdf_pages=list(range(1,total+1)),rendered_page_sha256=p['rendered_page_sha256'],previous_rendered_page_sha256=prior['rendered_page_sha256'],new_visual_pdf_pages=p['new_visual_pdf_pages'],new_text_pdf_pages=[],new_full_extracted_text_pages=0,
            whole_article_visual_read=True,reading_log=prior['reading_log']+p['reading_log'],exact_own_checks=model,publisher_direct_binary_obtained=False,publisher_binary_fidelity_verified=False,raw_student_data_read=False,all_cited_originals_read=False,official_erratum_verified=False,independent_review=False,student_validated=False)
        if label=='length':
            n['audit_findings']=[
                dict(pdf_pages=[2,3,4,11,12],finding='LT는 목표·사고 진행·지도 활동의 결합이며 확률적 사고 패턴과 유일한 경로는 다르다. REV는 주제·프로젝트·연간 전통 수업 전체를 직접 시행한 처치가 아니다. 순서가 더 유용하다는 결과를 모든 경우의 필요조건으로 바꾸지 않는다.'),
                dict(pdf_pages=[5,6,7],finding='계획120분과 실제 연습량·주간 간격은 다르다. 두 조건 모두 정오 피드백·시범을 받고 REV는 시범 뒤 재시도했다. LT만 앞 수준으로 난도를 낮추는 조정이 가능했다. BAU 일부에는 다른 수학 게임이 허용됐다. 매 회기 전수 충실도 측정은 아니며 연구진의 점검을 우리 자료의 외부 검토로 세지 않는다.'),
                dict(pdf_pages=[7,8],finding='28문항에서 사전3연속오류 중단과 사후 전 문항 시행을 구별한다. 시작 수준의75%는 해당 수준과 모든 이전 수준의 공동 기준이다. 미시행을 실제 오답으로 처리하거나75%를 보편적 숙달 기준으로 옮기지 않는다.'),
                dict(pdf_pages=[5,6,8,9],finding='사전187·사후185·초록189와 표4/5의 인원 불일치를 유지한다. 표1의 학교 유형별 참여 인원은 공립150/사립37이나 본문은52/135다. 표4의39(20.08%)는185분모의21.08%와 다르며 소수 둘째 자리 반올림만으로 맞지 않는다. 원 분모·교정값을 확정하지 않는다.'),
                dict(pdf_pages=[8,9,10],finding='표8의 작은WAIC가 낮은 표본 밖 예측 성능이라는 주석은 본문의 작은 값 선호와 반대다. 공식loo정의WAIC=-2*elpd_waic를 참고해 방향을 구별하되 논문 모형은 재추정하지 않는다.95%신용구간은빈도주의p값이 아니며 REV대BAU는0을포함한다. 사후중앙값의 차를 별도 대비의 중앙값과 강제로 일치시키지 않는다. 그림1성장 표기·단순 변화·사전 통제 사후 모형을 구별한다.')]
            n['method_reference']=dict(url=model['waic_direction_reference'],scope='공식loo문서의Value절 WAIC=-2*elpd_waic 정의만 대조했다. 논문의 원 모형·로그우도·사후표본·WAIC오차를 복원하지 않았다.',full_document_or_cited_papers_read=False)
            n['source_corrections']+= [dict(location='표4·PDF8',issue=n['audit_findings'][3]['finding'],status='displayed_arithmetic_discrepancy_not_official_erratum'),dict(location='표1·PDF5와본문PDF9',issue='학교 유형별 참여 인원150/37과52/135를 함께 보존한다. 분류·분석 대상을 원자료 없이 확정하지 않는다.',status='unresolved_source_counts'),dict(location='표8주석·PDF10',issue=n['audit_findings'][4]['finding'],status='criterion_direction_crosscheck_not_model_reanalysis')]
        else:
            n['renderer_overrides']=p['renderer_overrides'];n['table2_orientation_image']=p['table2_orientation_image'];n['rendering_note']='기본1900px Poppler에서5쪽 계산이 끝나지 않아 해당 쪽은pypdfium2 5.13.0의1900px대체 판면으로 읽었다. 대체 확인 후 자신이 실행한 해당 작업 프로세스만 종료했고 사용자 프로세스는 중지하지 않았다. 원인과 엔진간 픽셀 동일성은 미확인이다.'
            n['audit_findings']=[
                dict(pdf_pages=[9,12,13],finding='소집단을 교실 안에서 조건에 배정한 군집 비교다. 동의/배정/분석 인원과 교실/소집단/아동 층위를 구별한다. 무처치 조건이 없으며 사전 점수를 통제한 두 활성 조건의g=.55,p=.003을 전체 교육 효과로 읽지 않는다.'),
                dict(pdf_pages=[10,11,13,15],finding='그림2정확성은0/1/2와NR,전략에는9=무응답을 쓴다. 본문의이진 명칭·표1정확성 제목·정답/과정 포함Rasch부분점수 설명을 원자료 없이 한 코딩으로 복원하지 않는다.9는 최고 전략 점수가 아니다. 전략의9처리 방법 전체는 미확인이다.'),
                dict(pdf_pages=[13,14],finding='ICC24%를 대다수 분산이라 부르는 문구는 수치상 과반과 다르다. 문항1의44(59%)/23(35%)와3(4%)/9(13%)를 표시대로 보존한다. 가장 가까운 정수 백분율로 반올림했다는 가정에서skip의9/13%와23/35%는 공통 정수 분모가 없으며23/35%분모65/66도전체분석63보다크다. 저자의 실제 반올림·가중·문항별 분석 분모는 확인하지 못했다.'),
                dict(pdf_pages=[14,15,17,18],finding='문항7·8은사후전용이므로빈사전칸은0이나변화점수가아니다. 문항9와10의인쇄평균변화대비는각각-.07/.02지만원반응·표준오차나인과효과를재추정한값이아니다. 먼전이/조절효과 비유의는 동등성 입증이 아니다. 좌절은현장노트 관찰이고체계적정서코딩은후속계획이다.'),
                dict(pdf_pages=[11,12,17,18],finding='양조건모두격려와적절한퍼즐교체를허용했다. LT만난도를낮추는비계를허용해순서만의독립효과가아니다. 회기수1–10과평균회기수8.07·회당8.59분에는도입/전환이포함된다. 저자는순서가유용해도모든경우필요하지않다고명시한다.')]
            n['source_corrections'] += [dict(location='본문PDF13',issue='ICC24%는수치상과반이아니다. 군집구조·추정치와효과크기g를서로바꾸지않는다.',status='numerical_language_scope'),dict(location='본문PDF14',issue=n['audit_findings'][2]['finding'],status='rounding_assumption_check_without_raw_item_denominators')]
        write(NOTES[index],n);s['snapshot_file']=NOTES[index];s['snapshot_sha256']=sha(NOTES[index]);entry=next(x for x in bib if x['id']==sid);entry['review_scope']=scope;entry['does_not_establish']=limit;entry['next_review']='원 반응·문항별/분석별 분모·코딩·출판사 정오표는 추가 확인한다. 인용 원문·외부 독립 검토·실제 국내 학생 검증은 미완료다.';s['bibliography_snapshot']=digest(entry)
        next(x for x in queue['literature_review'] if x['source']['id']==sid)['source']=copy.deepcopy(entry)
        for c in l['claims']:
            if c['source_id']==sid:c['empirical_scope']=copy.deepcopy(empirical)
    claims={c['id']:c for c in l['claims']}
    claims['LTDL-01']['does_not_establish']='초록189명, 표4의 조건별 합계, 표5머리글187명과 행185명, 학교 유형별 본문 인원은 불일치가 남아 있다. 사후 표2의 인원을 다른 표의 분모·모든 분석 분모로 강제 적용하지 않는다.'
    claims['LTDL-02']['support']='정순은 학생이 보인 수준의 다음 활동에서 시작하고 필요한 경우 앞 수준으로 난도를 낮췄다. 역순은 높은 수준부터 비슷한 길이 활동을 제시하고 오답 후 시범과 아동의 재시도를 제공했다. 두 조건 모두 개별 수업·정오 피드백·시범을 받았다.'
    claims['LTDL-02']['does_not_establish']='순서와 비계·활동 조정이 함께 달랐다. 계획120분은 실제 연습량·주간 간격의 동일성을 보증하지 않는다. 정규 조건은 길이 개별 지도가 없었으나 일부 다른 수학 게임이 허용돼 모든 개별 관심이0이라고 단정하지 않는다.'
    claims['LTDL-03']['does_not_establish']='역순 대 정규의95%신용구간은0을 포함하며 정순 대 역순 구간의 원문 끝점 순서를 보존했다. 사후중앙값의 차로 별도 대비의 중앙값을 교정하지 않는다. 조정 사후Rasch추정·단순 변화·정답률·표본 밖 예측 기준은 다른 양이며 모형 재추정은 하지 않았다.'
    claims['LTDL-04']['does_not_establish']='사전3연속오답 중단과 사후 전 문항 시행을 구별한다. 시작 수준의75%는 해당 수준과 모든 이전 수준을 함께 확인하는 연구 규칙이며 보편적 숙달 기준이 아니다. 다른 측정량·국내cm/m성취를 대신하거나 단계 이름을 필수 선수로 추가하지 않는다.'
    claims['LTDL-04']['locations']+=['https://files.eric.ed.gov/fulltext/EJ1323924.pdf#page=2','https://files.eric.ed.gov/fulltext/EJ1323924.pdf#page=11']
    claims['LTDS-01']['does_not_establish']='소집단을 조건에 배정한 두 활성 퍼즐 지도 조건의 상대 비교다. 무처치 대비 전체 효과·교실 전체 지도·장기 유지·국내 성취기준별 효과를 검증하지 않았다. 비유의 사전 차이나 조절변수로 동등성·모든 집단의 동일 효과를 입증하지 않는다.'
    claims['LTDS-02']['support']='그림2의 문항1A는 오답·부분 정답·완전 정답과 무응답을 구별하고, 과정 코드는 조각을 놓기 전의 회전과 놓은 뒤 맞추려는 회전을 구별했다. 전략의9는 무응답 표시이며 높은 전략 점수가 아니다.'
    claims['LTDS-02']['does_not_establish']='정답 코드와 과정 코드·Rasch척도는 같은 단위가 아니다. 본문의이진 명칭·그림0/1/2·부분점수 모형을 원자료 없이 하나의 코딩으로 복원하지 않는다. 문항별 개수·백분율의 분모와 전략 무응답 처리 전체는 미확인이다.'
    claims['LTDS-03']['does_not_establish']='문항7·8은 사후전용이라 빈 사전칸을0이나 성장값으로 바꾸지 않는다. 가까운 전이의 결과로 모든 공간 과제를 추정하지 않으며 먼 전이의 비유의 차이는 동일 효과나 어느 조건에도 학습이 없었다는 증거가 아니다.'
    claims['LTDS-04']['support']='다음 수준부터 지도한 조건은 필요에 따라 안쪽 선을 그어 난도를 낮췄고 목표 수준 직접 지도 조건은 이를 허용하지 않았다. 양조건 모두 노력에 대한 격려와 적절한 다른 퍼즐 선택이 가능했으며 목표 수준 퍼즐을 다뤘다.'
    claims['LTDS-04']['does_not_establish']='순서와 난도 조정이 결합된 지도 비교다. 특정 안쪽 선·순서가 모든 학생에게 필요한지는 입증하지 않았다. 현장노트의 좌절 관찰을 검증된 정서 척도나 수학 기피의 인과 효과로 바꾸지 않는다.'
    for cid in ['LTDS-01','LTDS-02','LTDS-04']:claims[cid]['locations'].append('https://files.eric.ed.gov/fulltext/EJ1234710.pdf#page=18')
    reviews=read('data/relation_literature_reviews.json');oldclaims={c['id']:c for c in old['claims']};count=0;sids={sid for _,sid,_,_ in SPECS}
    for row in reviews['records']:
        c=claims[row['claim_id']]
        if c['source_id'] in sids:
            assert row['claim_snapshot']==claim_snapshot(oldclaims[c['id']],old['sources'][c['source_id']]);row['claim_snapshot']=claim_snapshot(c,l['sources'][c['source_id']]);count+=1
    assert all(l['sources'][sid]['observations']==old['sources'][sid]['observations'] for sid in l['sources'])
    for p,v in [('data/sources.json',bib),('data/content_review_queue.json',queue),('data/literature_claim_reviews.json',l),('data/relation_literature_reviews.json',reviews)]:write(p,v)
    print(json.dumps(dict(status='recorded',total_visual_pages=37,new_visual_pages=25,new_full_extracted_text_pages=0,changed_claims=8,new_sources=0,new_claims=0,new_tasks=0,refreshed_context_snapshots=count)))

if __name__=='__main__':main()

"""Record a bounded full visual reading while retaining the earlier selected review."""
import copy,hashlib,json
from literature_review import ROOT,digest,load_registry
from relation_literature_review import claim_snapshot
from check_conservation_cue_and_transition_models import check

SOURCE='SIEGLER_1995_NUMBER_CONSERVATION'
NOTES='data/literature_evidence/SIEGLER_1995_complete_visual_review_notes.json'
SCOPE='저자 연구실 PDF49쪽(인쇄225–273)의 본문·표1–2·그림1–7·참고문헌을 실제 판면으로 모두 읽었다. 이전 선정17쪽의 관련 추출문 대조는 보존하되 전문49쪽 추출문 독해로 확대하지 않는다. 이번 처음 읽은 판면은42쪽이며 재대조7쪽은 중복 합산하지 않는다.'
LIMIT='97명 사전검사 중 두 공동 선정 조건을 충족한45명을15명씩 무작위 배정했다. 최대2주의 같은 큰 집합24문항 반복에 관한 조건 묶음 비교다. 설명 대상·피드백 전후 순서·설명할 판단의 정오 여부가 함께 달라 각각의 효과를 분리하지 못한다. 시행 중 설명 다양성과 학습의 관련성은 관찰적이며 인과 효과가 확인되지 않았다. 지연 검사·미경험 문항 전이·국내 과제 효과는 확인되지 않았다.'

def read(p):return json.loads((ROOT/p).read_bytes())
def write(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def main():
    l=load_registry();old=copy.deepcopy(l);s=l['sources'][SOURCE]
    assert not (ROOT/NOTES).exists() and len(l['claims'])==1055
    progress=read('tmp/literature/siegler-complete-20261118/reading-progress.json')
    assert progress['reading_completed'] and progress['actually_viewed_pdf_pages_this_turn']==list(range(1,50))
    assert progress['new_text_pages_read']==0 and progress['source_pdf_sha256']==s['source_pdf_sha256']
    assert sha('tmp/literature/siegler-complete-20261118/siegler-source.pdf')==s['source_pdf_sha256']
    for p,h in progress['rendered_page_sha256'].items():assert sha(f'tmp/literature/siegler-complete-20261118/rendered/page-{int(p):02d}.png')==h
    prior=read(s['snapshot_file']);notes=copy.deepcopy(prior)
    empirical=copy.deepcopy(s['empirical_scope']);empirical.update(inference_limit=LIMIT,causal_effect_scope='randomized condition bundle only;not variability association',observational_variability_causal_effect_established=False)
    s.update(date='2026-11-18',read_scope=SCOPE,limits=LIMIT,empirical_scope=empirical,
             scope_note='전체49판면을 대조했다. 무작위 배정은 훈련 조건 묶음에만 적용되며, 동일 아동·문항의 전환 비율과 사후 사례 분류는 아동 숙달률·새 문항 전이·설명 다양성의 인과 효과와 구별한다.',
             method_note='이전7판면을 포함한49판면을1900px 렌더링으로 읽고 본문·2표·7그림을 대조했다. 자체 단서·분모·조건부 검정·반올림 모형은 원 학생자료 재분석이 아니다.',
             editorial_action='2026-11-18 전체 판면 대조로 기존SNC01–03·IE17의 한계와SNC-P1 관찰 해석을 보완했다. 신규 출처·주장·과제·관계는0이다.')
    s['snapshot_history']=copy.deepcopy(s.get('snapshot_history',[]))+[dict(snapshot_file=s['snapshot_file'],snapshot_sha256=s['snapshot_sha256'],date=old['sources'][SOURCE]['date'],read_scope=old['sources'][SOURCE]['read_scope'])]
    s['text_pdf_pages']=prior['text_pdf_pages'];s['visual_pdf_pages']=list(range(1,50))
    notes.update(date=s['date'],read_scope=SCOPE,empirical_scope=empirical,previous_review=old['sources'][SOURCE],
                 previous_snapshot_file=s['snapshot_file'],previous_snapshot_sha256=s['snapshot_sha256'],
                 visual_pdf_pages=list(range(1,50)),visual_pdf_page_hashes=progress['rendered_page_sha256'],
                 text_read_method=prior['text_read_method']+' 이번 전문 추출문 독해는0쪽이다.',
                 new_visual_pdf_pages=sorted(set(range(1,50))-set(prior['visual_pdf_pages'])),new_text_pdf_pages=[],
                 previous_visual_pdf_page_hashes=prior['visual_pdf_page_hashes'],whole_article_visual_read=True,
                 publisher_binary_fidelity_verified=False,all_cited_originals_read=False,official_erratum_verified=False,
                 raw_student_data_read=False,independent_review=False,student_validated=False,exact_own_checks=check())
    notes['reading_log']=prior['reading_log']+progress['reading_log']
    notes['audit_findings']=[
        dict(pdf_pages=[11,12,14,23],finding='8회 전체는 사전4회·훈련4회다. 큰 집합 고유24문항을 사전1회·훈련2회로 각각3번 제시했다.97명 중45명의 선정은 정답과 변환 설명의 공동 기준이며 낮은 전체 정확률만을 뜻하지 않는다.'),
        dict(pdf_pages=[15,38,39,40],finding='모든 조건은 정답 피드백을 받았다. 설명 대상·피드백 순서·설명할 판단의 정오 여부가 함께 달라 성인 관점 취하기나 옳은 답 설명 각각의 독립 효과는 확인되지 않았다.'),
        dict(pdf_pages=[13],finding='길이 단서와 밀도 단서의 정오 패턴이 정확히 반대라는 문장은6유형 전체에는 맞지 않는다. 표1상Equal에서는 둘 다 맞고Conflict-equal에서는 둘 다 틀린다. 중간4유형에만 반대다. 자체 논리 점검이며 공식 정오표나 원 반응 재분석은 아니다.'),
        dict(pdf_pages=[15,20,24],finding='한 시행의 여러 설명은 주 코딩에서 마지막 이유를 썼다.5주요 이유의 표2 합98%/97%는 비망라 범주이므로 합100으로 재정규화하지 않는다. 다양성 분석의 여러 이유 집계와 주 코딩은 다르다.'),
        dict(pdf_pages=[17,18,23,24,34,35,36],finding='집단 평균·정답 시행·틀린 답 중 특정 유형·앞서 변환 설명을 한 아동×문항 전환의 분모는 다르다.22%정답 반전과24%변환 설명 반전은 아동 숙달 상실률이 아니다. 새 문항·독립 지연 검사로 확대하지 않는다.'),
        dict(pdf_pages=[27,28,29,30,31,32,33,37],finding='실험자 판단 설명15명 중8/4/3의 사례 분류는 결과를 보고 나눈 것이다. n15 단계적 회귀R²와 설명 다양성 관련성은 인과 효과·외부 예측 검증이 아니다. 실험 전체8/8대3/7의p<.03을 사전6/8대3/7에 옮기지 않는다. 그림4 반올림 표기는 본문49→86과 양립 가능해 오류로 확정하지 않는다.'),
        dict(pdf_pages=[41,42,43,44,45,46],finding='그림7은 나이 축의 개념도이며 전략1–5를 표2 이유 이름이나 고정 연령·실측 확률로 읽지 않는다. ASCM은 산술에 구현된 모형으로 이 수 보존 자료 적합 결과가 아니다. Q-SOAR와 다른 영역의 인용은 별도 연구이며 원문 독해로 세지 않는다.'),
        dict(pdf_pages=[46,47,48,49],finding='논의 마지막의 변화·수 세기·산술 지식 연결은 제안된 설명이다. 인쇄270–273 참고문헌과1994-08-03 수락 표기는 읽었으나 인용 원문과 공식 정오표까지 확보했다는 뜻은 아니다.')]
    notes['source_corrections']=prior['source_corrections']+[dict(location='표1·인쇄237쪽',issue=notes['audit_findings'][2]['finding'],status='own_logical_audit_not_official_erratum')]
    write(NOTES,notes);s['snapshot_file']=NOTES;s['snapshot_sha256']=sha(NOTES)
    claims={c['id']:c for c in l['claims']}
    claims['SNC01']['does_not_establish']='설명 대상·설명 시점·설명할 판단의 정오 여부가 함께 달랐다. 성인 관점 취하기나 옳은 판단 설명 각각의 효과를 분리하지 못한다. 정답을 알려 주는 것과 이유를 대신 말해 주는 것은 다른 절차다.'
    claims['SNC01']['locations'].append(prior['source_pdf_url']+'#page=40')
    claims['SNC02']['does_not_establish']='정답률은 반복한 큰 집합 문항의 집단 요약이다. 중간 회차·개별 아동의 경로는 단조롭지 않다.72%를 숙달 아동 비율로, 모든 유형의 개선이나 미경험 문항 전이로 해석할 수 없고 정답만으로 세기와 변환 추론을 구별하지 못한다.'
    claims['SNC03']['support']='길이·세기·실제 추가나 제거에 근거한 설명을 구분했다. 한 시행에 여러 이유가 있으면 주 코딩은 마지막 이유를 썼고, 동일 문항에서도 이후 다른 설명으로 바뀌었다. 이를 참고한 자체 관찰에서는 최초 답·최초 이유·이후 수정한 이유와 도움을 순서대로 따로 기록한다.'
    claims['SNC03']['does_not_establish']='한 번의 정답이나 설명으로 모든 배열의 전략을 판정하지 않는다. 조건부 아동×문항 전환 비율은 아동 숙달 상실률이 아니다. 설명 다양성과 학습의 관련성·결과에 따른8/4/3 사례 분류는 인과 효과나 고정 발달 단계가 아니며 기호식 숙달도 측정하지 않았다.'
    claims['SNC03']['locations'] += [prior['source_pdf_url']+'#page=15',prior['source_pdf_url']+'#page=37']
    for cid in ['SNC01','SNC02','SNC03']:claims[cid]['empirical_scope']=copy.deepcopy(empirical)
    claims['IE17']['does_not_establish']='권고4는Minimal이다. 한 유아 수 보존 실험에서 설명 대상·피드백 순서·설명할 판단의 정오 여부가 함께 달랐다. 이 요소 각각의 효과, 이유를 듣기만 하는 방식이나 국내 과제 효과는 확인되지 않았다.'
    claims['IE17']['recommendations'][0]['application_limit']=claims['IE17']['does_not_establish']
    claims['IE17']['locations'].append(prior['source_pdf_url']+'#page=40')
    s['observations'][0]['interpretation']='세 경우에서 위 줄은 모두 더 길다. 최초 답·최초 이유와 뒤에 스스로 수정한 이유, 교사의 도움·정답 피드백·짝짓기 확인 후 반응을 순서대로 구별해 기록한다. 원논문의 마지막 이유 주 코딩을 최초 이유 기록과 혼동하지 않는다. 둘째만 맞히면 길이 단서로도 가능한 답인지 다른 두 경우와 대조한다. 같은 문항의 재응답과 새 배열 전이를 따로 확인하며 국내 학생 반응·과제 타당성은 미검증이다.'
    bib=read('data/sources.json');entry=next(x for x in bib if x['id']==SOURCE);entry['review_scope']=SCOPE;entry['does_not_establish']=LIMIT;entry['next_review']='출판사 파일 동일성·정오표·인용 원문과 원 학생 반응은 별도 확인한다. 국내 관찰 과제·외부 독립 검토와 실제 학생 검증은 미완료다.';s['bibliography_snapshot']=digest(entry)
    q=read('data/content_review_queue.json');next(x for x in q['literature_review'] if x['source']['id']==SOURCE)['source']=copy.deepcopy(entry)
    reviews=read('data/relation_literature_reviews.json');oldclaims={c['id']:c for c in old['claims']};n=0
    for row in reviews['records']:
        cid=row['claim_id'];sid=claims[cid]['source_id']
        if sid==SOURCE or cid=='IE17':
            assert row['claim_snapshot']==claim_snapshot(oldclaims[cid],old['sources'][sid])
            row['claim_snapshot']=claim_snapshot(claims[cid],l['sources'][sid]);n+=1
    for p,v in [('data/sources.json',bib),('data/content_review_queue.json',q),('data/literature_claim_reviews.json',l),('data/relation_literature_reviews.json',reviews)]:write(p,v)
    print(json.dumps(dict(status='recorded',new_visual_pages=42,total_visual_pages=49,new_text_pages=0,changed_claims=['SNC01','SNC02','SNC03','IE17'],changed_tasks=['SNC-P1'],refreshed_context_snapshots=n,new_sources=0,new_claims=0,new_tasks=0)))


if __name__=='__main__':main()

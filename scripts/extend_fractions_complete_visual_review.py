"""Complete the unchanged public-domain guide and private protocol visual scope."""
import copy,hashlib,json
from literature_review import ROOT,build_report,digest,load_registry,read
from relation_literature_review import FILE,claim_snapshot
from check_fraction_guide_reading_conditions import check

SOURCE='IES_FRACTIONS_2010'
NOTES='data/literature_evidence/IES_FRACTIONS_2010_complete_visual_review_notes.json'
SHA='ed94a5ee4127a32240fd0114d2afc025c15ba8233014da3c07601157b770c252'
PROTOCOL_SHA='6e68bc533fee2fa0f02c5327a7a02f9e2c122907afc93dbf30926aa7c804891e'
PRIOR_VISUAL=[4,17,20,21,22,27,28,29,30,34,35,36,37,38,39,44,45,46,64,66,67,74,75]
NEW_VISUAL=sorted(set(range(1,91))-set(PRIOR_VISUAL))
SCOPE='2010년 분수 지도 가이드90쪽의 기존 전체 추출문과 전체90판면, 별도 심사 프로토콜 v2.0의 기존8쪽 추출문과 전체8판면을 대조했다. 이번에 가이드67판면·프로토콜7판면을 추가 확인했으며 새 추출문 독해는0쪽이다.'
BOUNDARY='용어집의 조밀성은 서로 다른 두 유리수 값 사이에서 읽는다. 같은 값의 다른 표기 사이에 새 값을 요구하지 않는다. 가분수의 분자·분모 크기 비교는 양의 분모·비음수 분수 범위로 한정하고, 단위비는 어느 양을1로 삼는지 먼저 정한다. 이를 한국 초등의 새 음수 분수 필수 내용으로 추가하지 않는다.'
LIMIT='가이드와 해당 프로토콜의 판면 대조 완료는 모든 인용 원연구·원자료·별도 WWC2.0 일반 핸드북·관련 영상/전사·정오표·후속 판본·외부 독립 검토·한국 학생 검증 완료가 아니다. 기존2.38/2.83 불일치와 수업 묶음·표본·분석 단위·권고 등급의 적용 한계를 유지한다.'
LOG=[
 'PDF1–3·5–16·18–19: 표지/표제, 목차, 권고·근거 수준, 도입과 초기 나눔을 판면으로 읽었다. 2010년9월/NCEE2010-4039의 서지 범위이며 현행 미국 학생·교사 상태를 새로 조사한 것이 아니다.',
 'PDF23–26·31–33·40–43·47–54: 나눔/양, 수직선의 단위와 내부 눈금, 개념·절차 왕복, 어림과 정확 계산, 비례 전략과 교사 지식을 대조했다. 부분·전체 표현 하나나 함께 변한다는 관찰로 분수/비례의 모든 의미를 대신하지 않는다.',
 'PDF55–63·65·68–73: 부록A–D와 연구 비교의 나머지 판면을 읽었다. 초기125개 심사/26개 기준 충족과 추가7개는 전체132개/33개, 권고 직접 관련20개와 구별한다. 연구/교사/학급/학생/측정값을 합산하지 않는다.',
 'PDF70·78 미주121: Xin2005의19명 중16명은 학습장애 진단, 나머지도 학습 문제를 보였다. 비진단 학생을 함께 포함한 혼합 표본이므로 전원 진단 학생 제외 조건과의 단순 모순으로 분류하지 않는다. Moore1989의9–11학년 등은 범위 밖 보조 근거로 구별한다.',
 'PDF69–71·80 미주230·237: Fujimura2001의 대조 조건별0.74유의/0.34비유의, Terwel2009의0.41비유의, Jitendra2009의 군집 보정 후 비유의, Saxe2001의 무작위 연수 비교와 별도 교육과정 비교를 구별한다.',
 'PDF76–90: 미주1–250, 참고문헌, 마지막 색인을 판면으로 확인했다. 굵은 서지 표시를 해당 원논문 본문 독해로 더하지 않는다. 기존 효과크기2.38/2.83의 보류와 공개 요약값 재계산 기록을 보존한다.',
 '별도 프로토콜PDF1–3·5–8: WWC2.0, 검색1989년 이후/패널 요청1983–1988예외, 혼합 표본, 여러 집단의 대비별 탈락·효과, 결과 영역, 동등성·보정·결측 처리와 처치 기술을 읽었다. 기존PDF4 탈락 곡선 대조와 합쳐8판면이다. 역사적 프로토콜이며 현행 WWC기준이나 본 사이트 인증으로 바꾸지 않는다.',
]

def write(path,value):(ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    registry=load_registry();source=registry['sources'][SOURCE]
    if source.get('reading_extension',{}).get('file')==NOTES:build_report();return
    assert source['snapshot_sha256']==SHA and source['visual_pdf_pages']==PRIOR_VISUAL and '90쪽 전체' in source['read_scope']
    assert hashlib.sha256((ROOT/source['snapshot_file']).read_bytes()).hexdigest()==SHA and len(NEW_VISUAL)==67
    previous=copy.deepcopy(source)
    bibliography=read(ROOT,'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry)
    entry.update(review_scope=SCOPE,next_review=LIMIT)
    source.update(date='2026-11-18',bibliography_snapshot=digest(entry),read_scope=SCOPE,text_pdf_pages=list(range(1,91)),visual_pdf_pages=list(range(1,91)),limits=previous['limits']+' '+LIMIT)
    source['scope_note']+=' 전체90판면과 별도 프로토콜8판면 대조 완료. '+BOUNDARY
    source['reading_log']=previous['reading_log']+LOG
    source['editorial_action']+=' 2026-11-18: 남은 가이드67판면·프로토콜7판면을 확인하고 용어 적용 조건을 보완했다. 기존6주장·4과제와 관련 원연구 대조 기록은 보존한다.'
    protocol=copy.deepcopy(source['additional_read_artifacts'][0]);assert protocol['sha256']==PROTOCOL_SHA
    protocol.update(version='2.0',text_pdf_pages=list(range(1,9)),visual_pdf_pages=list(range(1,9)),prior_visual_pdf_pages=[4],new_visual_pdf_pages=[1,2,3,5,6,7,8],redistributed=False)
    notes=dict(source_id=SOURCE,source_pdf_sha256=SHA,contains_source_full_text=False,cumulative_read_scope=SCOPE,cumulative_text_pdf_pages=list(range(1,91)),cumulative_visual_pdf_pages=list(range(1,91)),new_text_pdf_pages=[],new_visual_pdf_pages=NEW_VISUAL,previous_review=previous,previous_bibliography=old_entry,previous_whole_text_reading_record=previous['reading_log'][0],reading_log=source['reading_log'],unread_followups=[LIMIT],protocol=protocol,source_discrepancies=previous['source_discrepancies'],table_inventory=['1','2','D.1','D.2','E.1'],numbered_figures=10,numbered_examples=5,mathematical_reading_conditions=[BOUNDARY],exact_condition_checks=check(),all_cited_originals_read=False,independent_review=False,student_validated=False)
    encoded=(json.dumps(notes,ensure_ascii=False,indent=2)+'\n').encode('utf-8');source['reading_extension']=dict(file=NOTES,sha256=hashlib.sha256(encoded).hexdigest())
    claims={x['id']:x for x in registry['claims'] if x['source_id']==SOURCE};assert len(claims)==6 and len(source['observations'])==4
    reviews=read(ROOT,FILE);refreshed=0
    for row in reviews['records']:
        if row['claim_id'] in claims:
            assert row['claim_snapshot']==claim_snapshot(claims[row['claim_id']],previous)
            row['claim_snapshot']=claim_snapshot(claims[row['claim_id']],source);refreshed+=1
    queue=read(ROOT,'data/content_review_queue.json');item=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);item['source']=entry
    (ROOT/NOTES).write_bytes(encoded)
    for p,v in [('data/sources.json',bibliography),('data/literature_claim_reviews.json',registry),(FILE,reviews),('data/content_review_queue.json',queue)]:write(p,v)
    build_report();print(json.dumps(dict(new_guide_visual_pages=67,new_protocol_visual_pages=7,new_text_pages=0,refreshed_relation_snapshots=refreshed,new_claims=0,new_tasks=0)))

if __name__=='__main__':main()

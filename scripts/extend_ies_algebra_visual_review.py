"""Record the completed visual reading of the unchanged licensed algebra guide."""
import copy
import hashlib
import json

from literature_review import ROOT, build_report, digest, load_registry, read
from relation_literature_review import FILE, claim_snapshot

SOURCE = 'IES_ALGEBRA_2015'
NOTES = 'data/literature_evidence/IES_ALGEBRA_2015_complete_visual_review_notes.json'
SHA = '83f6f973eb79caa2170f2818034d533322258708d38a777620862b95a9cbc730'
PRIOR_VISUAL = [9,13,16,17,27,28,29,37,38,48,55,57,58,61,62,63,70]
NEW_VISUAL = sorted(set(range(1,72))-set(PRIOR_VISUAL))
SCOPE = '2019년 1월 개정 가이드 PDF 71쪽의 추출문과 전체 71판면을 대조했다. 이번에 남은 54판면을 읽었고 새 추출문 독해는 0쪽이다. 별도 공식 심사 프로토콜 v3.0은 기존 8쪽 추출문 독해 범위이며 판면 대조는 하지 않았다.'
LIMIT = '관련 도구 모음·영상, 별도 심사 프로토콜의 판면, WWC 3.0 일반 핸드북, 아직 대조하지 않은 개별 원논문·원자료, 외부 독립 검토와 실제 학생 반응은 후속 확인한다.'
CORRECTION = '공식 PDF 표지·표제면(PDF1·3)의 보고서 번호는 NCEE 2015-4010이나 권장 인용문(PDF4)은 NCEE 2014-4333이다. PDF4의 발행·개정일은 2015년 4월·2019년 1월이다. 이 내부 표기 차이를 기록하며 번호의 연도를 발행연도로 대체하거나 공식 정오표·원인을 확인했다고 주장하지 않는다.'
LOG = [
    'PDF1–8: 표지·표제·발행/공공영역 고지·목차·예 목록·개요를 판면으로 대조했다. 예 3.8은 목차와 본문 모두 인쇄33쪽(PDF39)이므로 쪽수 불일치로 기록하지 않는다.',
    'PDF10–12·14–15·18–26: 목표별 풀이, 의도적으로 잘못된 학생 예, 불완전 예, 자기 질문, 식의 표현과 분배 도식·언어를 읽었다. 오답 예를 문헌의 계산 오류나 실제 학생 자료로 바꾸지 않는다. 예2.4 유리식 변형에는 원래 분모의 x≠±1 조건이 필요하다.',
    'PDF30–36·39–47: 장애 상황별 지도, 협력 활동, 전략 비교·선택·정당화, 용어집과 근거 등급 정의를 읽었다. 모든 전략의 일시 숙달이나 무조건적 효율 우위를 요구하는 것으로 확대하지 않는다.',
    'PDF49–54·56·59–60·64–69·71: 저자·지원 인력·이해관계, 부록 D와 표의 주석, 참고문헌·미주·발간물 안내를 읽었다. 표 D.2–D.4의 기존 비교 조건·유의성·영역/하위 결과·공유 대조군 해석을 유지한다.',
    '검색 인용, 30개 집단설계 심사, 4개 단일사례 심사와 기준 충족15개 집단설계는 서로 다른 집계다. 미주50에서 Hutchinson1993이 집단·단일사례 양쪽 집계에 포함됨을 확인했다. 30+4를 고유 연구34개로 단정하지 않는다.',
    '부록의 긍정·부정 효과 분류는 통계적 유의성 또는 실질적 중요성이다. 별표와 분류를 동일시하지 않는다. 개념/절차/유연성의 측정 중첩·즉시/지연 시점과 독립 적용을 구별한다.',
]

def write(path,value):
    (ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    registry=load_registry();source=registry['sources'][SOURCE]
    if source.get('reading_extension',{}).get('file')==NOTES:
        build_report();return
    assert source['snapshot_sha256']==SHA
    assert source['visual_pdf_pages']==PRIOR_VISUAL and source['text_pdf_pages']==list(range(1,72))
    assert len(NEW_VISUAL)==54 and hashlib.sha256((ROOT/source['snapshot_file']).read_bytes()).hexdigest()==SHA
    previous=copy.deepcopy(source);previous_notes=read(ROOT,previous['reading_extension']['file'])
    bibliography=read(ROOT,'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry)
    entry.update(review_scope=SCOPE,next_review=LIMIT)
    source.update(date='2026-11-18',bibliography_snapshot=digest(entry),read_scope=SCOPE,visual_pdf_pages=list(range(1,72)),limits=LIMIT)
    source['scope_note']+=' 전체 71판면 대조 완료. '+CORRECTION
    source['reading_log']=previous['reading_log']+LOG
    source['editorial_action']+=' 2026-11-18: 남은 54판면을 확인하고 보고서 번호의 내부 표기 차이를 안내했다. 기존 11주장·9과제와 관계 해석은 보존한다.'
    notes=dict(source_id=SOURCE,source_pdf_sha256=SHA,contains_source_full_text=False,cumulative_read_scope=SCOPE,
        cumulative_text_pdf_pages=list(range(1,72)),cumulative_visual_pdf_pages=list(range(1,72)),new_text_pdf_pages=[],new_visual_pdf_pages=NEW_VISUAL,
        previous_review=previous,previous_bibliography=old_entry,previous_reading_extension=previous['reading_extension'],
        reading_log=source['reading_log'],unread_followups=[LIMIT],discrepancies=previous_notes['discrepancies']+[CORRECTION],
        comparison_notes=previous_notes['comparison_notes'],protocol=previous_notes['protocol'],
        table_inventory=['1','A.1','D.1','D.2','D.3','D.4'],numbered_example_count=30,
        official_erratum_or_cause_verified=False,all_cited_originals_read=False,independent_review=False,student_validated=False)
    encoded=(json.dumps(notes,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    source['reading_extension']=dict(file=NOTES,sha256=hashlib.sha256(encoded).hexdigest())
    reviews=read(ROOT,FILE);claims={x['id']:x for x in registry['claims'] if x['source_id']==SOURCE};assert len(claims)==11 and len(source['observations'])==9
    refreshed=0
    for row in reviews['records']:
        if row['claim_id'] in claims:
            assert row['claim_snapshot']==claim_snapshot(claims[row['claim_id']],previous)
            row['claim_snapshot']=claim_snapshot(claims[row['claim_id']],source);refreshed+=1
    queue=read(ROOT,'data/content_review_queue.json')
    item=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);item['source']=entry
    (ROOT/NOTES).write_bytes(encoded)
    write('data/sources.json',bibliography);write('data/literature_claim_reviews.json',registry);write(FILE,reviews);write('data/content_review_queue.json',queue)
    build_report();print(json.dumps(dict(new_visual_pages=54,new_text_pages=0,refreshed_relation_snapshots=refreshed,new_claims=0,new_tasks=0)))

if __name__=='__main__':main()

"""Preserve prior reviews while closing four cached documents' visual reading."""
import copy,hashlib,json
from literature_review import ROOT,read,digest,load_registry,build_report
from relation_literature_review import FILE,claim_snapshot
from check_gaise_missing_day import check

SOURCES=['IES_EARLY_2013','IES_ALGEBRA_2015','GAISE_2020']
CACHE='tmp/literature/guide-visual-closure-20261118'
def write(p,v):
    (ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def image_records(key,pages):
    return [dict(pdf_page=p,local_temporary_file=f'{CACHE}/{key}/page-{p:03}.png',sha256=sha(f'{CACHE}/{key}/page-{p:03}.png')) for p in pages]

def main():
    registry=load_registry();m=read(ROOT,CACHE+'/preparation.json')
    assert m['reading_completed'] and sum(map(len,m['new_visual_pages_read'].values()))==109
    old=copy.deepcopy(registry);bibliography=read(ROOT,'data/sources.json');reviews=read(ROOT,FILE);queue=read(ROOT,'data/content_review_queue.json')
    for sid,key in [('IES_EARLY_2013','early'),('IES_ALGEBRA_2015','algebra_protocol'),('GAISE_2020','gaise')]:
        s=registry['sources'][sid];prior=copy.deepcopy(s)
        entry=next(x for x in bibliography if x['id']==sid);previous_bib=copy.deepcopy(entry)
        n=read(ROOT,s.get('reading_extension',{}).get('file',s['snapshot_file']));previous_notes=copy.deepcopy(n)
        if sid=='IES_EARLY_2013':
            scope='가이드 전체165쪽 추출문과 전체165판면, 별도 심사 프로토콜2.1 전체9쪽 추출문·판면을 대조했다. 이번 새 판면은 가이드49쪽·프로토콜9쪽이고 새 추출문 독해는0쪽이다.'
            limit=prior['limits']+' WWC 일반 핸드북 전체·현재 심사 기준의 확인으로 확대하지 않는다.'
            correction=dict(status='main_appendix_search_counts_unresolved',locations=['PDF16 / 인쇄10','PDF71 / 인쇄65'],issue='본문은 검토79·기준충족29, 부록은 검토78·기준충족28로 적는다. D.1의29인용·장 단위 행과 참고문헌의 굵은30항목도 별도 집계다.',followup='문헌·연구·장·비교의 단위와 집계 의도는 확정하지 않았다. 어느 한쪽을 정답으로 선택하거나 공식 정오표를 확인했다고 주장하지 않는다.')
            s['source_discrepancies'].append(correction)
            s['scope_note']+=' 본문은 검토79·기준충족29, 부록은78·28로 적는다. 인용·장·비교의 집계 단위와 편집 의도는 미확인이다.'
            protocol=copy.deepcopy(read(ROOT,'data/literature_evidence/IES_EARLY_2013_number_study_tables_review_notes.json')['review_protocol'])
            protocol.update(version='2.1',pdf_pages=9,text_pdf_pages=list(range(1,10)),visual_pdf_pages=list(range(1,10)),new_text_pdf_pages=[],new_visual_pdf_pages=list(range(1,10)),sha256=m['sources']['early_protocol']['sha256'],redistributed=False,new_image_records=image_records('early_protocol',range(1,10)))
            # Korean authored commentary, with historical protocol rules kept distinct.
            protocol['reading_log']=[
                'PDF1–4: 1989–2011 검색과 위원 예외, 영어 보고·임의 국가/수업 언어, 주로6세 미만인3–6세 또는 kindergarten 조건을 확인했다. 혼합 대상은 분리 가능하거나 적격 학생50% 초과여야 한다. 지도 예와 근거 등급 채택은 구별한다.',
                'PDF5: 여섯 결과 영역은 기초 수 개념·연산·기하·패턴/분류·숫자 인식·일반 수리력이다. 측정을 독립된 일곱째 결과 영역으로 추가하지 않는다. 지도 내용과 결과 영역은 다른 분류다.',
                'PDF6–9: 종료에 가장 가까운 검사를 주요 결과, 후속 검사를 유지로 구별한다. 신뢰도 최소치와 위원장 판단, 낙관적 탈락 경계, 사전차.05초과–.25이하의 조정 및.25초과의 처리를 읽었다. 기본ICC.20은 실제 관측치가 아니다.',
                '다중성 본문과5결과×2대비=10검정 예를 함께 보존한다. 공유 대조군·여러 코호트·후속 검사를 독립 재현 연구로 더하지 않는다. 일반 핸드북 전체나 현재 기준을 읽은 것으로 표시하지 않는다.']
            logs=['남은49판면을 읽어 표지·발행일·목차·본문·부록의 판면 대조를 완료했다. 발행일2013년11월과 보고서번호NCEE2014-4005는 별도 표기다. 표18개·그림7개·예11개를 구별했다.',correction['issue']+' '+correction['followup'],'권고1Moderate·나머지Minimal은 중요도나 효과0을 뜻하지 않는다. 23개 연구가 같은 내용에서 특정 발달 순서만 직접 비교한 근거라는 주장은 하지 않는다. 도형의 일부 필요 성질을 충분한 정의로 바꾸거나 미국 단위 예를 한국 초등 필수 내용으로 옮기지 않는다.']+protocol['reading_log']
            n.update(protocol=protocol,source_corrections=s['source_discrepancies'])
            filename='data/literature_evidence/IES_EARLY_2013_complete_visual_review_notes.json'
            s['visual_pdf_pages']=list(range(1,166));newguide=m['sources']['early']['new_visual']
        elif sid=='IES_ALGEBRA_2015':
            scope='2019년1월 개정 가이드 전체71쪽 추출문·판면과 별도 공식 심사 프로토콜v3.0 전체8쪽 추출문·판면을 대조했다. 이번 새 판면은 프로토콜8쪽이며 새 가이드 판면·추출문은0쪽이다.'
            limit='관련 도구 모음·영상, WWC3.0 일반 핸드북, 아직 대조하지 않은 개별 원논문·원자료, 외부 독립 검토와 실제 학생 반응은 후속 확인한다.'
            p=n['protocol'];p.update(visual_pdf_pages=list(range(1,9)),new_visual_pdf_pages=list(range(1,9)),new_text_pdf_pages=[],new_image_records=image_records(key,range(1,9)))
            logs=[
                '프로토콜PDF1–3: 1993–2013년9월 검색 및 위원 예외, 영어 보고·임의 국가/수업 언어,6–12학년의 재현 가능한 지도법 범위를 읽었다. 포괄 교육과정·정책·학교개혁은 제외하며 브랜드 유무만으로 적격을 결정하지 않는다. 학생 수 없는 혼합 학년의50% 학년 규칙을 학생 수50%로 바꾸지 않는다.',
                'PDF4–5: 보수적 탈락 경계와 분석 표본의 사전 동등성, 인구학적 차이의 별도 판단을 읽었다. 사전검사 공변량ANCOVA가 있어도 동등성 미확인 연구의 등급 기여와 WWC기준 충족은 같은 판정이 아니다.',
                'PDF6–8: 개념·절차·유연성을 구별하며 불명확한 결과는 기본적으로 절차로 분류한다. 종료2주 이내 결과를 직후 범위로, 지연은2주–1개월·1–3·3–6·6개월 초과로 나누고 새 맥락 전이를 별도 기록한다. 교사 부여 성적은 직접 대수 결과가 아니다.',
                '통계 조정·RD/SCD 시범 기준의 상당 부분은 별도 WWC3.0 일반 핸드북을 참조한다. 이8쪽 독해를 그 핸드북 전체 독해·현재 기준 검증으로 확대하지 않는다. Early2.1의 낙관적 탈락 경계와 이 문서의 보수적 경계를 혼용하지 않는다.']
            p['reading_log']=logs;filename='data/literature_evidence/IES_ALGEBRA_2015_protocol_visual_review_notes.json';newguide=[]
            s['scope_note']+=' 별도 심사 프로토콜3.0 전체8판면도 대조했다. 해당 문서의 보수적 탈락 경계와 다른 프로토콜의 경계를 혼용하지 않는다.'
        else:
            scope='확보한126쪽 PDF 전체 추출문과 전체126판면을 대조했다. 기존 본출처74판면과 같은 책의 별도 탐구 출처9판면을 중복 제거한83판면에 새43판면을 더했다. 이번 새 추출문 독해는0쪽이다.'
            limit='확보본 전체 판면을 대조한 범위다. 인용 원연구·원자료·More4U·원도구·공식 정오표와 별도 현행 공식 PDF의 판면 동일성은 미확인이다. 원문의 산술·조건·그림 표기 불일치는 보존한다. PDF·페이지 이미지는 재배포하지 않는다.'
            logs=[
                'PDF3–15·29–33·35: 표제·저작권·목차·서문과 A수준 도입을 읽었다. 2020저작권·승인과2021도서관 서지 기술은 별개다. 수준은 고정 학년표가 아니며 성인도A에서 시작할 수 있다. 제한된 음악 응답 선택지와 반 전수조사를 학년 전체 대표 표본으로 바꾸지 않는다.',
                'PDF5–6·11·51: 목차의 A6+B9+C8=23번호 예와 서문의22예 표기는 다르다. 연속·재방문 예는 맥락을 공유한다. 편집 의도나 공식 정오표 없이23개 독립 연구나 고유 맥락으로 세지 않는다.',
                'PDF39·45·47–48: 사진/카드의 관측 단위, 시계열 누락일, 다섯 변수의 짝·단위를 읽었다. cm는 표준 미터법 단위이며 미국 관습 단위와의 대조를 비표준 측정으로 번역하지 않는다. 산점도의 같은 직선 근처와 정확한 동일값을 혼동하지 않는다.',
                'PDF52–54·56·62·71–75·77–84·88: B/C질문·변수·표집·무작위 배정·시뮬레이션과 사진 사례를 읽었다. 자원 가족의 사진 수는 고유 가족 수·세계 대표 표본 수가 아니다. 보이지 않는 자물쇠를 없음으로 단정하지 않고 소비 추정치·소득·관찰/인과를 구별한다. 낮은 확률은 불가능이나 원인 확정이 아니다.',
                'PDF50·78·112·122의 빈 판면도 확인했다. 기존 분모·QCR·그림/표·분산과 표준편차·신뢰/예측 구간·종자 실험 단위·누락·훈련/검증 오류의 한계는 유지한다.']
            n['source_corrections'].append(dict(kind='maximum_daily_change_not_identified_with_missing_day',location='PDF45 / 인쇄37 Table6',observed='9일째 미측정인데 하루 최대2cm·세 번으로 서술한다.',action='실측된 연속 날짜 쌍의 최대는2cm다. 하지만8일7cm·10일10cm 사이9일 값이7 또는10인 가상 단조 완성에서는 하루3cm가 가능하다. 실제 최대가2cm였다고 단정하지 않는다. 가상 완성은 새 관측값이 아니다. 공식 정오표·작성 의도는 미확인이다.'))
            n['source_corrections'].append(dict(kind='numbered_example_count_unresolved',location='PDF5–6 / 목차, PDF11 / 서문',observed='목차A6+B9+C8=23번호 예, 서문22예',action='관찰한 표기를 함께 보존한다. 계속되는 예·재방문 예의 중복 맥락과 독립 연구 수를 구별하며 집계 의도는 미확인이다.'))
            task=next(x for x in s['observations'] if x['id']=='GA-P5')
            task['interpretation']+=' 미측정일이 있으면 관측된 연속 날짜 쌍의 최대 변화량과 실제 전체 기간의 최대 하루 변화량을 구별한다. 구간 평균만으로 실제 최대를 단정하지 않는다.'
            n['missing_day_exact_counterexamples']=check()
            extra=read(ROOT,registry['sources']['GAISE_2020_INQUIRY_SELECTED']['snapshot_file'])
            assert extra['source_pdf_sha256']==n['source_pdf_sha256']
            extra_images=[dict(pdf_page=p,local_temporary_file='historical separate authored review',sha256=extra['rendered_page_sha256'][str(p)]) for p in extra['visual_pdf_pages']]
            n.update(previous_notes_file=prior['snapshot_file'],previous_notes_sha256=prior['snapshot_sha256'],new_read_pdf_pages=[],new_visually_reviewed_pages=image_records(key,m['sources'][key]['new_visual']),visually_reviewed_pages=sorted(previous_notes['visually_reviewed_pages']+extra_images+image_records(key,m['sources'][key]['new_visual']),key=lambda x:x['pdf_page']),previous_same_book_additional_source='GAISE_2020_INQUIRY_SELECTED',previous_same_book_union_visual=m['sources'][key]['previous_same_book_union_visual'],read_scope=scope)
            assert len(n['visually_reviewed_pages'])==len({x['pdf_page'] for x in n['visually_reviewed_pages']})==126
            n['unread_followups']=[limit];filename='data/literature_evidence/GAISE_2020_complete_visual_review_notes.json';newguide=m['sources'][key]['new_visual']
            s['snapshot_history'].append({k:prior[k] for k in ['snapshot_file','snapshot_sha256','date','read_scope']})
            s['scope_note']+=' 미측정일이 있는 식물 예의 하루 최대2cm는 실측된 연속 날짜 쌍의 최대다. 미측정일의 실제 값을 모르면 전체 기간의 실제 최대 하루 변화량을 확정할 수 없다.'
        entry.update(review_scope=scope,next_review=limit)
        s.update(date='2026-11-18',bibliography_snapshot=digest(entry),read_scope=scope,limits=limit)
        s['editorial_action']+=' 2026-11-18: 남은 판면을 읽고 읽기 범위를 갱신했다. 미해결 집계와 비교 조건은 보존한다.'
        s['reading_log']=prior.get('reading_log',previous_notes.get('reading_log',[]))+logs
        n.update(previous_review=prior,previous_bibliography=previous_bib,reading_log=s['reading_log'],contains_source_full_text=False,new_text_pdf_pages=[],new_visual_pdf_pages=newguide,all_cited_originals_read=False,independent_review=False,student_validated=False,official_erratum_or_cause_verified=False)
        if sid!='GAISE_2020':
            n.update(previous_reading_extension=prior['reading_extension'],cumulative_read_scope=scope,cumulative_text_pdf_pages=s['text_pdf_pages'],cumulative_visual_pdf_pages=s['visual_pdf_pages'],new_image_records=image_records('early',newguide) if sid=='IES_EARLY_2013' else [])
            write(filename,n);s['reading_extension']=dict(file=filename,sha256=sha(filename))
        else:
            write(filename,n);s.update(snapshot_file=filename,snapshot_sha256=sha(filename))
        claims={x['id']:x for x in registry['claims'] if x['source_id']==sid}
        for row in reviews['records']:
            if row['claim_id'] in claims:
                assert row['claim_snapshot']==claim_snapshot(claims[row['claim_id']],prior)
                row['claim_snapshot']=claim_snapshot(claims[row['claim_id']],s)
        next(x for x in queue['literature_review'] if x['source']['id']==sid)['source']=entry
    assert registry['claims']==old['claims']
    changed=[(sid,x['id']) for sid,s in registry['sources'].items() for x,y in zip(s.get('observations',[]),old['sources'][sid].get('observations',[])) if x!=y]
    assert changed==[('GAISE_2020','GA-P5')],changed
    write('data/sources.json',bibliography);write('data/literature_claim_reviews.json',registry);write(FILE,reviews);write('data/content_review_queue.json',queue)
    build_report();print(json.dumps(dict(new_visual_pages=109,new_text_pages=0,new_sources=0,new_claims=0,new_tasks=0,changed_existing_tasks=changed)))

if __name__=='__main__':main()

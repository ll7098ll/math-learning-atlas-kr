"""Guarded review migration. Importing this module does not read private files."""
import copy, hashlib, json
from literature_review import ROOT, load_registry, digest
from check_mpc_design_models import check

SID='MATTERA_ET_AL_2017_MPC_DESIGN'
NOTE=f'data/literature_evidence/{SID}_complete_visual_review_notes.json'
SCOPE='ERIC 공개 PDF28판면 전체를 읽었다. ERIC표지1판면과 인쇄227–253쪽의 출판대기 장27판면이며 표2개·그림0개·참고문헌을 포함한다. 기존5·새23판면이고 새 전문 추출문 독해는0쪽이다. 종전 선정 추출문15쪽 및2023설계논문 초록·참고문헌 대조 이력을 보존한다.'
LIMIT='동일MPC·High5s 연구 계열의2017설계 설명이다. 프로그램 선정·제공·실제 참여·성취·인과매개는 다르다. 세 비교는 완전2×2요인설계가 아니며 초기·예비 결과를 최종 장기 결과나 독립 재현으로 바꾸지 않는다. 원자료·공식 정오표·인용 원전 전체·국내 검증은 미확인이다.'

def read(p):return json.loads((ROOT/p).read_bytes())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def write(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    l=load_registry();old=copy.deepcopy(l);s=l['sources'][SID];prior=read(s['snapshot_file'])
    assert len(l['claims'])==1057 and s['snapshot_sha256']=='0d3fd00e2a642011c088351ece261485a987b44bab0c1878ca2e88f6618ebec6'
    assert not (ROOT/NOTE).exists()
    p=read('tmp/literature/mpc-design-complete-20261119/reading-progress.json')
    assert p['reading_completed'] and p['actually_viewed_pdf_pages_this_turn']==list(range(1,29))
    assert len(p['new_visual_pdf_pages'])==23 and len(p['previous_visual_pdf_pages'])==5
    assert p['source_pdf_sha256']==s['source_pdf_sha256']==sha('tmp/literature/mpc-design-complete-20261119/source.pdf')
    for page,h in p['rendered_page_sha256'].items():assert sha(f'tmp/literature/mpc-design-complete-20261119/rendered/page-{int(page):03d}.png')==h
    findings=[dict(pdf_pages=x['pages'],finding=' '.join(x['findings'])) for x in p['reading_log']]
    n=copy.deepcopy(prior)
    n.update(date='2026-11-19',read_scope=SCOPE,previous_snapshot_file=s['snapshot_file'],previous_snapshot_sha256=s['snapshot_sha256'],
        previous_review=copy.deepcopy(s),visual_pdf_pages=list(range(1,29)),new_visual_pdf_pages=p['new_visual_pdf_pages'],
        previous_visual_pdf_pages=p['previous_visual_pdf_pages'],previous_rendered_page_sha256=prior['rendered_page_sha256'],
        rendered_page_sha256=p['rendered_page_sha256'],new_text_pdf_pages=[],new_full_extracted_text_pages=0,
        whole_report_visual_read=True,whole_report_includes_cover=True,chapter_printed_pages='227–253',
        whole_report_tables=dict(count=2,figures=0),audit_findings=findings,exact_own_checks=check(),
        all_cited_originals_read=False,raw_student_data_read=False,models_refitted=False,official_erratum_verified=False,
        independent_review=False,student_validated=False,source_pdf_redistributed=False,contains_source_full_text=False)
    n['reading_log']=prior['reading_log']+[SCOPE]+[f['finding'] for f in findings]
    n['source_corrections'] += [dict(location='PDF '+','.join(map(str,f['pdf_pages'])),issue=f['finding'],status='own_bounded_audit_not_official_erratum') for f in findings]
    write(NOTE,n)
    s.setdefault('snapshot_history',[]).append({k:s[k] for k in ['snapshot_file','snapshot_sha256','date','read_scope']})
    s.update(date='2026-11-19',snapshot_file=NOTE,snapshot_sha256=sha(NOTE),read_scope=SCOPE,limits=LIMIT,
        scope_note='2011선정 판단·운영 충실도·측정 계획·배정 단위를 구별한다. 선정/참여 기준은 학생 숙달 판정이 아니며 완전요인설계의 상승작용을 검정하지 않았다.',
        method_note='ERIC28판면 전체와 표1·2를 읽고 AND/OR조건·분모·코칭 시간 단위·빠진 요인 셀의 가상 반례를 자체 검산했다. 학생 원자료·원모형 재분석은 수행하지 않았다.',
        editorial_action='2026-11-19: 전체 설계 장 대조로 기존4주장을 보완했다. 새 출처·주장·관찰 과제·관계는0이며 기존 과제와 수정 이력을 보존했다.')
    updates={
      'MPCD-01':('2011선정에서9모형을 검토한 뒤 Building Blocks와 Big Math for Little Kids를 집중 비교했다. 표1의 효과 기준은 취학전의 유의한 근거와 전국규준.2SD 또는 개발자척도.5SD다. BMLK의 해당 효과 근거는 유치원판에 한정됐고 소프트웨어는 개발 중이었다. BB스페인어 지원은 일부 자료·소프트웨어였다.',
        '선정표의 체크·체크플러스·각주는 범주 판단이다. 수치 순위·이번 연구의 두 프로그램 직접 효과 비교·보편적 필수 순서로 쓰지 않는다. 선행BB/PreKMathematics 비교와 이번BB/BMLK선정을 나누며 AND/OR·시점·측정 종류를 유지한다.'),
      'MPCD-02':('표2는 대집단 활동 실시와 수학센터 이용가능일 각각 출석일의66%이상, 소집단·컴퓨터 활동은 전체 아동의75%이상 참여를 요구한다. 가정통신문은 발송 또는 불필요다. 코칭 평균149/180분은 매주,99/120분은 격주이며 회기 실시율96/98%와 다르다. 대조군의 실제 수학 수업도 조사했다.',
        '일수·아동수·회기수·시간과 제공·이용가능·실제 참여를 섞지 않는다. 첫해 소집단 주1활동과 둘째해 두 활동이 제시된 주에는 둘 다 실시하는 요구를 구별한다. 운영 기준은 아동 숙달률이나 모든 이전 학습수준75%통과 규칙이 아니다. 교사2년 훈련은 모든 교사11일 실제 참여·같은 아동2년 수업을 뜻하지 않는다.'),
      'MPCD-03':('ECLS-B의 여러 수학영역을 아우르는 중재근접 척도와 WJ응용문제의 전국규준 척도는 목적·민감도가 다르다. 설계 장은 시점별 도구 유지·점수 연결을 검토하고 언어검사 초점도 수용어휘에서 독해로 옮길 계획을 설명한다.',
        '전체 점수로 개별 덧셈 전략·도형 설명을 판정하지 않는다. 도구가 바뀐 점수를 바로 빼서 개인 성장으로 읽지 않으며 연결 계획만으로 측정동일성·국내 번역 타당도·전이를 입증하지 않는다. 계획된 추적을 전원 자료 확보나 최종 장기 결과로 쓰지 않는다.'),
      'MPCD-04':('취학전69기관(공립47·CBO22)을 배정하고 High5s는24MPC공립학교의 동의한 잔류 아동을 학교 내 재배정했다.25진행자·5감독·79클럽·300명 초과 아동은 운영 규모다. 정규수업/MPC/MPC+High5s의 세 비교가 가능하지만 High5s만 받는 네번째 셀은 없다.',
        '배정·운영·관찰 단위와 잔류 조건을 유지한다. 완전2×2설계의 상호작용·상승작용이나 수학능력 자체의 인과매개를 분리하지 않았다. 기관 탈락0은 아동 탈락0이 아니다.2017블록4–6기관/2021보고서4–5기관 및PDF22의BB유치원 이수 표기/다른 쪽의취학전 이수 표기를 출처별 보존한다.2017초기·예비 결과는 후속 최종 결과와 다르다.')}
    extra={'MPCD-01':[9,10],'MPCD-02':[10],'MPCD-03':[20,25],'MPCD-04':[3,4,5,14,21,22,26]}
    for c in l['claims']:
        if c['id'] in updates:
            c.update(zip(['support','does_not_establish'],updates[c['id']]))
            c['locations']=list(dict.fromkeys(c['locations']+[f'https://files.eric.ed.gov/fulltext/ED651010.pdf#page={v}' for v in extra[c['id']]]))
    bib=read('data/sources.json');b=next(v for v in bib if v['id']==SID)
    b.update(review_scope=SCOPE,does_not_establish=LIMIT,next_review='2017설계 장 전체를 읽었다.2023설계논문 전체·2026후속 출판판 전체·인용 원전·원자료·공식 정오표·국내 검증은 별도 미완료다.')
    s['bibliography_snapshot']=digest(b)
    q=read('data/content_review_queue.json');row=next(v for v in q['literature_review'] if v['source']['id']==SID)
    row.update(source=copy.deepcopy(b))
    reviews=read('data/relation_literature_reviews.json');assert not any(x['claim_id'] in updates for x in reviews['records'])
    assert s['observations']==old['sources'][SID]['observations']
    for p,d in [('data/sources.json',bib),('data/content_review_queue.json',q),('data/literature_claim_reviews.json',l)]:write(p,d)
    load_registry()
    print(json.dumps(dict(status='recorded',total_visual_pages=28,new_visual_pages=23,new_text_pages=0,changed_claims=4,new_claims=0,new_tasks=0,prior_tasks_preserved=1240,contexts_preserved=875)))

if __name__=='__main__':main()

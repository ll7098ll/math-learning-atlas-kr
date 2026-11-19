"""Guarded whole-report review migration; imports perform no private-file I/O."""
import copy, hashlib, json
from literature_review import ROOT, load_registry, digest, target_value
from relation_literature_review import claim_snapshot
from check_mpc_measurement_models import check

SID='MATTERA_ET_AL_2021_MPC_THIRD_GRADE'
NOTE=f'data/literature_evidence/{SID}_complete_visual_review_notes.json'
PDF='https://www.mdrc.org/sites/default/files/MPC_High5-3yr_Impact_Report.pdf'
DATE='2026-11-19'
SCOPE='MDRC 공식 PDF의 101판면 전체를 읽었다. 표지·공백·목차·요약·본문·부록A–F·24표·1그림·참고문헌을 포함하며 본문101쪽이라는 뜻은 아니다. 기존12판면과 새89판면을 합친 범위다. 새 전문 추출문 독해는0쪽이고 종전 선정 추출문23쪽 및 사전등록·후속 논문·WWC 대조 이력을 보존한다.'
LIMIT='세 비교는 대조군·배정 단위·분모가 다르고 High 5s 중재군이 겹친다. 지도 묶음·학교 잔류 선택·결과 미확보를 고려한다. 집단 추정치를 개인 숙달·국내 특정 과제의 효과·필수 순서로 확대하지 않는다. 원 분석 코드·학생 원자료·공식 정오표와 국내 검증은 미확인이다.'

def read(p):return json.loads((ROOT/p).read_bytes())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def write(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def links(*pages):return [PDF+f'#page={p}' for p in pages]

def main():
    l=load_registry();old=copy.deepcopy(l);s=l['sources'][SID];prior=read(s['snapshot_file'])
    assert s['snapshot_sha256']=='fc41cf267055b92c6a18174f2a4b366e043145be17175d283414f6ba61cfe2a9'
    assert not (ROOT/NOTE).exists() and len(l['claims'])==1055
    p=read('tmp/literature/mpc-complete-20261119/reading-progress.json')
    a=read('tmp/literature/mpc-complete-20261119/acquisition.json')
    assert p['reading_completed'] and p['actually_viewed_pdf_pages_this_turn']==list(range(1,102))
    assert len(p['new_visual_pdf_pages'])==89 and len(p['previous_visual_pdf_pages'])==12
    assert p['source_pdf_sha256']==s['source_pdf_sha256']==sha('tmp/literature/mpc-complete-20261119/source.pdf')
    for page,h in p['rendered_page_sha256'].items():
        assert sha(f'tmp/literature/mpc-complete-20261119/rendered/page-{int(page):03d}.png')==h
    empirical=copy.deepcopy(s['empirical_scope']);empirical['inference_limit']=LIMIT
    s['snapshot_history'].append({k:s[k] for k in ['snapshot_file','snapshot_sha256','date','read_scope']})
    s.update(date=DATE,read_scope=SCOPE,limits=LIMIT,empirical_scope=empirical,
        scope_note='세 비교의 배정·분모·결과 척도와 확증·탐색 분석을 구별한다. 출석 경계 및 표·본문의 다른 표기는 자체 검산과 함께 보존한다. 개인별 효과나 국내 검증을 입증하지 않았다.',
        method_note='공식 PDF101판면 전체를 읽고 정수 경계·비율·집계 분모를 검산했다. 학생 원자료·분류 코드·회귀 모형을 재분석하지 않았다.',
        editorial_action='2026-11-19: 전체 보고서 대조로 기존10주장을 보완하고 자료 분류 경계·하위집단 검정의 주장2건 및 가상 과제2개를 추가했다.')
    n=copy.deepcopy(prior);n.update(date=DATE,read_scope=SCOPE,empirical_scope=empirical,
        previous_snapshot_file=old['sources'][SID]['snapshot_file'],previous_snapshot_sha256=old['sources'][SID]['snapshot_sha256'],
        previous_review=old['sources'][SID],visual_pdf_pages=list(range(1,102)),new_visual_pdf_pages=p['new_visual_pdf_pages'],
        previous_visual_pdf_pages=p['previous_visual_pdf_pages'],previous_rendered_page_sha256=prior['rendered_page_sha256'],
        rendered_page_sha256=p['rendered_page_sha256'],new_text_pdf_pages=[],new_full_extracted_text_pages=0,
        whole_report_visual_read=True,whole_report_includes_covers_blanks_frontmatter=True,
        all_cited_originals_read=False,raw_student_data_read=False,classification_code_verified=False,
        official_erratum_verified=False,independent_review=False,student_validated=False,
        exact_own_checks=check(),source_pdf_redistributed=False,contains_source_full_text=False)
    # Keep former notes and hashes intact; new findings are our paraphrases.
    findings=[
        ([13,14,19,20,23,24,25], '세 비교와 배정: 69기관(공립47·CBO22)을35/34기관으로 배정했다. High 5s는24MPC공립학교 잔류 아동320/335명 재배정이다. 대조군도 정규 취학 전·유치원 수학지도를 받았다. 교사 훈련2년을 같은 아동의MPC2년 이수로 바꾸지 않는다. 이 보고서는 같은 연구 계열의 다섯번째 보고서이지 독립 연구5편이 아니다.'),
        ([25,27,32,41,42,53,58,61,73,74], '명부2819/동의2717/연령적격2702/어떤 결과2277/수학1844를 구별한다. MPC결과별N은 수학1844·문해1849·만성결석1788·유급2166·특수교육2276이다. 추가/결합 수학226명은 공통 중재군이다. High5s655명을 모두 프로그램군으로 쓴 부록A 본문은 같은 문단의320/335배정과 구별한다.'),
        ([28,32,40,41,43,74,79,81,83,90,95], '만성결석 본문은 출석90%이하/결석10%이상이지만 표는 출석90%미만으로 쓴다. 180일중18일 결석은 정확히90%출석이어서 두 기준이 다르다. 178일 예시의19일 이상은 두 정의 모두에서 최소18일이라는 정수 검산과 다르다. 실제 분류 코드가 어느 기준을 썼는지는 미확인이다.'),
        ([16,17,33,34,48,49], '수학효과.10/.34를 외부2000NAEP4학년 소득 격차.85SD와 나눈 약12%/40%는 점수 상승률·관측된 격차 해소율이 아니다. 결석23.6/32.6의 차9%p와 상대감소약27.6%도 다르다. 도시78141명에9%p를 적용한 약7033명은 외삽한 가정 계산이지 새 관측 결과가 아니다.'),
        ([32,33,34,37,38,39,40,73], '표의별표1/2/3은10/5/1%수준이다. 문해p.12를marginally significant라고 하고 모든 탐색결과가 유리하다고 쓴 본문 요약은 문해 무별표 및 유급+.4%p와 맞지 않는다. 수치·표기 귀속을 보존하며 비유의를 정확히 효과0·동등성·비열등성으로 바꾸지 않는다. p0.00은 반올림값이다.'),
        ([35,36,37,39,77,78,80,82,84,85], '집단내 수학p.02/.31과 집단간p.65를 구별한다. 낮은/높은 자기조절집단의 수학p.01/.28과 집단차p.24도 다르다. D4문해의 자기조절집단차p.04와 언어집단차p.58을 함께 보존한다. 모든 하위집단 분석은 탐색이며 유의/비유의 차이가 유의한 효과차이는 아니다. 비유의 집단차이도 동등성을 입증하지 않는다.'),
        ([27,28,65,66,67,68], 'MPC/결합은 원preK기관·블록을 유지한2수준모형이고 High5s추가는학교지표를 포함한1수준모형이다. High5s의preK말 공변량은High5s배정 전이지만MPC후 측정이다. 다중대치는 기초평가 결측을 대상으로 하며 최종 수학결과 대치를 확인한 것은 아니다. 다중비교 개수를 제한하고 역할을 구별한 것을 공식 다중검정 보정이라고 하지 않는다.'),
        ([53,54,55,56,57,58,59,60,61,62,71,72,73,74], '유치원분석 하위표본의 적격1325/어떤 결과1180/수학974와soft동의1911/어떤 결과1520/수학1295를 나눈다. 비동의 공립1060명을 더한soft표본은 비동의CBO를 포함하지 않는다. pooled5790은 명부2819+1911+1060과 일치하며 full적격2702를 넣은5673과 다르다. 어떤 결과4670과수학3846은 연도별 표본 합과 맞지만 서로 분모가 다르다. F/Wald통계량을 p값으로 읽지 않는다.'),
        ([59,60,61,62], 'A6수학456명과 완전 공변량Wald210명 및Arrows225명은 다른 분모다. PencilTap행의0–1비율과16시행정답총수 주석은 척도 대응이 미확인이다. 비동의18명 사후배정과 유치원 당시 민감도 분석을3학년 실제 프로그램 이수 또는 새로운 독립 무작위 표본으로 세지 않는다.'),
        ([41,42,43,44,45,47,48,49], '두해결합.34·MPC공립.16·추가.02는 대상·대조군이 달라 효과의 가산성이나 상승작용 검정이 아니다. 표3.7대조군의 서로 다른3학년 평균은 사전 기초점수나 개인 성장량이 아니다. 위험집단·가정참여·유지환경·비인지매개 논의는 직접 검정된 중재 기전이 아니다. 중고등학교 효과 가능성을 이미 관측한 결과로 쓰지 않는다.'),
        ([89,90], 'E1의유치원~3학년N1877/1819/1790/1788과 p.27/.02/.01/.00을 보존한다. 동일 완전패널이나 모든 학년 유의한 결과가 아니다. 표 제목/행의4시점과 모든 행을3학년처럼 쓴 공통 주석을 구별한다.'),
        ([93,94,95], 'F1의2013/2019학교 평균은 같은 아동의 종단변화가 아니다. 장애/빈곤행의d/e주석 설명이 교차한다. F2제목은 결합 비교이나 주석은MPC만 언급한다. 학교기초수행을 추가 통제한 수학.37·문해.32·결석-11.3%p는 주표.34/.29/-9.5와 다른 민감도 추정이며 새 표본·독립 재현이 아니다.'),
        ([3,4,7,11,97,98,99,100,101], '서지·연구 지원·참고문헌 및MDRC소개를 읽었다. 원 보고서의 감독·감사·지원기관을 본 프로젝트의 외부 독립검토로 세지 않는다. 인용목록 읽기는 인용 원전 전체 독해를 뜻하지 않는다. 원문 PDF·판면은 비공개로 보존하고 자체 검토노트만 공개한다.')]
    n['audit_findings']=[dict(pdf_pages=pages,finding=f) for pages,f in findings]
    n['reading_log']=prior['reading_log']+[SCOPE]+[f for _,f in findings]
    n['source_corrections'] += [dict(location='PDF '+','.join(map(str,pages)),issue=f,status='own_bounded_audit_not_official_erratum') for pages,f in findings]
    n['whole_report_tables']=dict(count=24,figures=1,appendices=list('ABCDEF'))
    write(NOTE,n);s.update(snapshot_file=NOTE,snapshot_sha256=sha(NOTE))
    updates={
      'MPC21-01':('취학 전69기관(공립47·CBO22)을35/34기관으로 배정했고 High 5s는24MPC공립학교 잔류 아동을 개별 배정했다. 어떤3학년 결과라도 있는 세 비교는1165/1112·274/282·274/313명이며 수학 분모는 각각945/899·226/230·226/255명이다.', '추가와 결합 비교의274명(수학226명)은 같은 중재군이다. 명부·적격·결과별 분모를 구별하며 대조군도 정규 수학지도를 받았다. 같은 연구 계열의 여러 보고서를 독립 표본으로 세지 않는다.'),
      'MPC21-02':('MPC 대 정규 수업의3학년 수학은945/899명에서 효과크기.10(p=.19)이었다. 적격2702명 중1844명의 수학 점수로 약32%미확보를 기록했다. 표3.1의 문해p=.12와 만성결석23.6/32.6%,차-9.0%p는 탐색 결과다.', '3학년 시험은 취학 전ECLS-B·유치원REMA-K와 다르다. 비유의는 정확한 효과0·동등성·개별 세기 효과 유지의 입증이 아니다. 문해를marginally significant·모든 탐색 결과를 유리하다고 쓴 요약은 문해 무별표·유급차+.4%p와 구별한다. 표시p0.00은 정확한0이 아니다.'),
      'MPC21-03':('High 5s 추가 대 MPC의3학년 수학은226/230명에서.02(p=.82)였다. 설계와 표2.1 및 표3.5첫 주석은 양쪽 모두MPC를 받은 비교임을 보여 주지만 표3.5뒤 설명은 대조군이MPC도 안 받은 것처럼 써서 상충한다.', '결합 대 정규 수업과 혼합하지 않으며 비유의를 정확한0·동등성으로 바꾸지 않는다. 상충 주석에 대한 자체 판면 대조는 공식 정오표나 분석 코드 확인이 아니다.'),
      'MPC21-04':('두해 결합 대 정규 수업의3학년 수학은 같은 공립학교에 남아 점수가 확보된226/255명에서.34(p=.01)였다. 보고서는 이를 외부2000년NAEP4학년 소득 집단 성취 격차.85SD의40%와 비교했다.', '40%는.34/.85의 맥락 비교이며 시험점수40%상승·관측된 격차40%해소·개인 성장률이 아니다. MPC전체.10·공립.16·추가.02는 대상·대조군이 달라 가산성이나 상승작용 검정으로 쓰지 않는다. 국내 특정 수행의 장기 효과·비인지 매개 기전을 분리하지 않았다.'),
      'MPC21-05':('부록B는 아동이 다른 학교로 이동해도 원preK기관·배정블록을 유지한다. 부록F의2013/2019학교 평균과F2학교기초성과 보정은 아동 개인의 변화와 다르다. E1은 시점별N1877/1819/1790/1788의 결석 분석을 제시한다.', '학교 평균을 같은 학생의 성장으로, 시점별 결석 분석을 동일 완전패널·모든 학년 유의성으로 바꾸지 않는다. F1장애/빈곤d/e주석 교차와F2제목/설명 충돌을 보존한다. F2수학.37은 주표.34와 다른 조정모형이며 독립 재현이 아니다.'),
      'MPC21-06':('2021보고서의MPC수학.10(p=.19)과 별도 후속 권호 논문의.10(p=.18), WWC90485의2026년 세 비교 심사에서 결측 처리 방법 미충족 및 결과 내보내기0행을 구별한다. 이번101판면 읽기는2021보고서 자체의 전체 대조다.', '효과 추정·표시p·심사 등급·제공되지 않은 결과는 다른 정보다. WWC미충족이나 결과0행을 효과0으로 치환하지 않으며, 종전 후속 논문·사전등록·WWC선정 대조를 그 자료들의 전체 판면 읽기로 확대하지 않는다.'),
      'MPC21-07':('사전등록의 명부2819명과 최종 보고서의 동의2717/연령적격2702/어떤 결과2277/수학1844명을 구별한다. 표C.2의 문해1849·결석1788·유급2166·특수교육2276명도 각각의 결과 분모다.', '명부 기준34.6%와 적격 기준약32%는 다른 분모다. 수학 표본을 모든 결과에 공통으로 쓰지 않는다. pooled5790은 명부2819+soft동의1911+추가공립1060과 맞지만 full적격2702를 넣은 합과 다르므로 표본 정의를 혼합하지 않는다.'),
      'MPC21-08':('High 5s추가는MPC공립 잔류 아동의 개인 배정이고 결합 비교는 최초 기관 배정도 반영한다. 사전등록617/651명과 보고서655/665명은 다른 표본 표기다. 보고서655명은High5s320명과대조335명의 전체다.', '두 비교에 겹친 중재군을 더하지 않는다. 모든655명이High5s를 받았다고 쓰거나 비동의18명 사후배정·유치원 당시 민감도 검사를3학년 실제 이수·새 독립 표본으로 바꾸지 않는다. 배정과 관측·이수를 나눠 기록한다.'),
      'MPC21-09':('사전등록3편과 최종 보고서의 다중대치는 빠진 기초평가·공변량을 대상으로 한다. High5s의preK말 공변량은High5s배정 전이지만MPC처치 후 측정이다. WWC4.1은 결측 처리 방법의 적합성과 추적 탈락 수준 검토를 나눈다.', '기초 대치를3학년 수학결과 대치로 간주하지 않는다. High5s사전 공변량을MPC의처치 전 공변량과 동일시하지 않는다. 공개 심사 이유만으로 미공개 세부 요구의 실패 원인을 확정하거나 공변량 민감도 결과를 원자료 재분석으로 쓰지 않는다.'),
      'MPC21-10':('표C.1의 full시행연도 주 수학분석1844명 p=.19와 같은 연도 유치원 검사 하위표본974명 탐색p=.03을 구별한다. soft2002명p=.12·그중동의1295명p=.03·pooled3846명p=.17도 별도 역할과 분모의 행이다.', '작은p로 사전 지정한 주 분석을 대체하거나 겹치는 표본을 독립 재현으로 세지 않는다. 주/탐색 역할 구분과 결과 개수 제한은 공식 다중검정 보정이 아니다. 표본 구성·조정모형·검사 시점을 함께 확인한다.')}
    cs={c['id']:c for c in l['claims']}
    for cid,(support,limit) in updates.items():
        cs[cid].update(support=support,does_not_establish=limit,empirical_scope=copy.deepcopy(empirical))
    extra_pages={'MPC21-01':[24,53,58,61],'MPC21-02':[28,33,73,74],'MPC21-03':[41],
        'MPC21-04':[16,43,44,48,49],'MPC21-05':[89,90,94,95],'MPC21-06':[97,100],
        'MPC21-07':[53,56,57,58,73,74],'MPC21-08':[58,61,62],
        'MPC21-09':[65,67,68],'MPC21-10':[55,56,57,58,72]}
    for cid,pages in extra_pages.items():cs[cid]['locations']=list(dict.fromkeys(cs[cid]['locations']+links(*pages)))
    new_claims=[('MPC21-11','12실통02-02',links(28,32,40,90),
        '보고서의 만성결석 본문 정의는 출석90%이하·결석10%이상이지만 표 주석은 출석90%미만이다. 178일 수업에서19일 이상 결석이라는 본문 예시는 두 정의 모두의 최소18일과 어긋난다.',
        '180일 중18일 결석처럼 정확히90%경계인 사례에서는 두 정의의 분류가 다르다. 이는 명시된 규칙의 자체 정수 검산이며 실제 학생 분류 코드·효과 추정의 오류나 공식 정정값을 확인한 것은 아니다.'),
        ('MPC21-12','12실통03-04',links(35,36,39,78,80,82,84,85),
        '낮은/높은 자기조절집단의 수학 효과 검정은 각각p=.01/.28이고 효과의 집단차 검정은p=.24다. D4문해에서는 자기조절집단차p=.04·언어집단차p=.58로 결과가 다르다.',
        '한 집단 유의·다른 집단 비유의를 유의한 효과차이로 바꾸지 않는다. 집단차 검정은 다른 귀무가설이며 비유의도 동등성의 증명이 아니다. 모든 하위집단은 탐색 분석이고 국내 학생 집단의 차이를 입증하지 않았다.')]
    for cid,code,locations,support,limit in new_claims:
        l['claims'].append(dict(id=cid,source_id=SID,role='empirical_result_with_scope',standard_codes=[code],
            locations=locations,support=support,does_not_establish=limit,empirical_scope=copy.deepcopy(empirical),
            independent_review=False,student_validated=False,target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}'))}))
    s['observations'] += [
        dict(id='MPC21-P7',standard_codes=['12실통02-02'],
            question='가상 출석 자료에서 수업180일 중18일 결석한 가 학생,178일 중18일 결석한 나 학생이 있다. 출석률90%이하와90%미만을 각각 기준으로 자료를 분류하고,178일 수업에서 필요한 최소 결석일도 구하라.',
            expected='가 학생의 출석률은162/180=90%로 이하 기준에만 해당한다. 나 학생은160/178≈89.89%로 두 기준 모두에 해당한다.178일에서는 두 기준 모두 최소18일 결석이다.180일에서는 이하 기준18일·미만 기준19일이다.',
            interpretation='자료를 모으기 전에 경계 포함 여부와 수업일·결석일의 정의를 정한다. 가상 규칙 검산을 보고서 학생의 실제 분류나 효과 재분석으로 바꾸지 않는다.',student_validated=False),
        dict(id='MPC21-P8',standard_codes=['12실통03-04'],
            question='가상 탐색 분석에서 낮은 기초집단의 효과 검정p=.01, 높은 기초집단p=.28, 두 집단의 효과차 검정p=.24다. 유의수준5%에서 각 검정의 결론을 쓰고 낮은 집단에 효과가 더 크다고 판정할 수 있는지 설명하라.',
            expected='낮은 집단의 효과0 가설은 기각하고 높은 집단의 효과0 가설과 두 집단의 효과차0 가설은 기각하지 않는다. 유의/비유의가 나뉜 사실만으로 효과차가 유의하다고 할 수 없다. 효과차가 없다는 동등성도 입증되지 않았다.',
            interpretation='집단별 효과와 효과의 집단차라는 서로 다른 귀무가설을 구별한다. 탐색 결과를 확증·독립 재현·국내 학생 검증으로 확대하지 않는다.',student_validated=False)]
    bib=read('data/sources.json');b=next(v for v in bib if v['id']==SID)
    b.update(review_scope=SCOPE,does_not_establish=LIMIT,next_review='학생 원자료·실제 만성결석 분류 코드·공식 정오표·미공개WWC세부 산출·후속 출판판 전체와 인용원전 및 국내 검증은 미완료다.')
    s['bibliography_snapshot']=digest(b)
    q=read('data/content_review_queue.json');row=next(v for v in q['literature_review'] if v['source']['id']==SID)
    row.update(source=copy.deepcopy(b),claim_ids=[c['id'] for c in l['claims'] if c['source_id']==SID])
    reviews=read('data/relation_literature_reviews.json');oldcs={c['id']:c for c in old['claims']};count=0
    for row in reviews['records']:
        if row['claim_id'] in updates:
            assert row['claim_snapshot']==claim_snapshot(oldcs[row['claim_id']],old['sources'][SID])
            row['claim_snapshot']=claim_snapshot(cs[row['claim_id']],s);count+=1
    assert count==0 and len(l['claims'])==1057 and len(s['observations'])==8
    protocol=ROOT/'docs/분수단위조정관찰기록.md'
    body=protocol.read_text(encoding='utf-8')
    if '| MPC21-P7 |' not in body:
        anchor='| MPC21-P6 | 같은 연구의 주 분석과 하위표본 탐색 분석의 검정 결과를 구별 |'
        assert body.count(anchor)==1
        body=body.replace(anchor,anchor+'\n| MPC21-P7 | 가상 출석 자료에서 90% 이하·미만의 경계와 수업일별 최소 결석일을 구별 |\n| MPC21-P8 | 가상 탐색 분석에서 집단별 효과 검정과 효과의 집단차 검정을 구별 |')
        protocol.write_text(body,encoding='utf-8')
    for p,d in [('data/sources.json',bib),('data/content_review_queue.json',q),('data/literature_claim_reviews.json',l),('data/relation_literature_reviews.json',reviews)]:write(p,d)
    load_registry()
    print(json.dumps(dict(status='recorded',total_visual_pages=101,new_visual_pages=89,new_text_pages=0,
        changed_claims=10,new_claims=2,new_tasks=2,prior_tasks_preserved=1238,contexts_preserved=875)))

if __name__=='__main__':main()

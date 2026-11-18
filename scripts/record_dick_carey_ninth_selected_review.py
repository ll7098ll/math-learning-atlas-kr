"""Read selected ninth-edition pages without completing the missing seventh-edition body."""
import copy,hashlib,json
from literature_review import ROOT,digest,target_value,load_registry,build_report
from relation_analysis_review import load_reviews

SOURCE='DICK_CAREY_2022_SELECTED'
URL='https://www.pearson.com/en-us/subject-catalog/p/systematic-design-of-instruction-the/P200000000952?view=educator'
REPOSITORY='https://elibrary.upi.edu/3739/'
ASSET='https://elibrary.upi.edu/3739/1/The%20Systematic%20Design%20of%20Instruction%20%28Dick%2C%20Carey%2C%20Carey%29.pdf'
SHA='8caf4d487388ac41a016d3d34857a246abdfd4712d4ad6b783c69271e721a04a'
NOTES='data/literature_evidence/DICK_CAREY_2022_selected_review_notes.json'
TEXT=[2,3,8]+list(range(73,95))+list(range(224,234))
VISUAL=[3,84,85,87,88,89,91,92,93,227,228,229,230,231,232,233]
SCOPE='9판의 불완전한 대학 저장소 파일에서 지정35쪽 텍스트·16쪽 이미지를 확인. 서지·간략 목차,목표 분석 장 전체(인쇄48–69),부록 도입·A–E(439–448)다.7판 검토·9판 전권 확보/정독이 아니다.'
INTEGRITY=dict(status='incomplete_repeated_segments',whole_book_obtained=False,physical_pdf_pages=439,unique_segment_pdf_pages=178,missing_printed_body_range=[71,405],publisher_authenticated_distribution=False)
OBSERVATIONS=[
 dict(id='D9-P1',standard_codes=['6수04-01','6수04-03'],question='가상 독서 기록 네 개가0분·10분·10분·20분으로 주어졌다. 평균을 구하고 무엇을 확인한 활동인지 설명하라. 이 답만으로 우리 반의 실제 독서 시간을 조사했고 통계적 탐구 전체를 수행했다고 판정할 수 있는가?',expected='합40분을 네 기록에 균등하게 나누면 평균10분이다.0분은 제공된 실제0이라는 가상 조건이고 무응답으로 바꿔 빼지 않는다. 확인한 것은 주어진 자료의 계산·해석이며 조사 질문 설정·대상/기간/기준 합의·실제 수집·누락 확인의 수행은 아직 관찰하지 않았다. 원래 자료의 개인차0·10·10·20도 평균 하나만으로 없어지지 않는다.',interpretation='가상 자료에 대한 기대 설명이며 실제 조사나 학생 응답이 아니다. 평균 계산의 부분 목표와 통계적 탐구 전체의 관찰 범위를 구별한다. 이미 주어진 자료를 읽는 부분 목표에서 그래프를 먼저 새로 그리는 일을 유일한 필수 경로로 강제하지 않는다. 전체 탐구의 표현·비교 활동이 불필요하다고 해석하지 않고,관찰하지 않은 수행은 실패 대신 미확인으로 기록한다.',student_validated=False),
 dict(id='D9-P2',standard_codes=['2수03-10'],question='cm의 이름을 말하기,0부터7cm까지 놓인 막대의 길이 읽기,2cm부터9cm까지 놓인 막대의 길이 설명하기는 무엇을 각각 확인하는가? 마지막 경우 눈금점과1cm 간격을 구별해 길이를 확인하라.',expected='단위의 이름을 아는 것과 시작점·끝점·단위 간격을 연결하는 수행을 각각 확인한다. 첫 막대와 둘째 막대는 모두7cm다.2부터9까지 눈금점은8개지만 사이1cm 간격은7개다. 끝 눈금9cm는 자 위 위치이며 막대 길이 자체는 아니다.0에 다시 맞추거나 같은 크기의1cm 간격을 세어 확인할 수 있다.',interpretation='수치가 주어진 가상 배치의 해석이며 실제 자를 놓고 잰 관찰을 대신하지 않는다. 단위 이름·두 끝 읽기·간격 세기·도구 놓기를 따로 기록하고,그림 설명만 관찰했으면 실물 측정은 미확인으로 둔다.0 맞추기를 교사가 알려 주었다면 도움 뒤 수행으로 남긴다. 이 활동이나 교재의 영어 작문 평가 예는 한국어 측정 과제의 진단 타당성을 검증하지 않는다.',student_validated=False)]
MAPPINGS=[
 ('D9G01',['6수04-01','6수04-03'],['PDF79–94 / printed54–69 / goal-analysis rubric and Figures3.1,3.4–3.12','PDF227–228 / printed442–443 / AppendicesB–C'],'수업 순서·수행 절차·정보 묶음·하위 기능 도식을 구별하고,평균 계산이라는 부분 목표와 실제 통계적 탐구 전체의 확인 범위를 구체화하는 설계에 참고한다.','부분 파일에 실린 설계 논의다. 예시의 모든 화살표·번호를 보편적 선수 관계로 옮기지 않는다. 제공된 자료의 정답만으로 실제 수집·표현·정당화 전체를 확인했다고 하지 않는다.9판의 해당 대목을 읽은 일이7판 미확보 장·9판 하위 기능 분석 장 전체의 검토나 현재 학생의 필수 순서 검증을 뜻하지 않는다.'),
 ('D9G02',['2수03-10'],['PDF229–233 / printed444–448 / AppendicesD–E'],'목표·조건·실제 평가 과제의 요구를 나란히 대조하고,단위 이름의 회상·구간 해석·실물 측정에서 확인한 증거와 미확인 수행을 구별하는 설계에 참고한다.','학교 작문 설계 예를 측정 수업의 효과·진단 규준으로 전용하지 않는다.평행 문항이라는 명칭만으로 측정 동등성이 입증되지 않으며 도구·응답 방식·도움과 수학적 수행을 구별한다. 부록의 출발 기능 선·학교 환경·기기 보급률은 그 사례의 가정이며 현재 학생 집단의 사전 능력·환경으로 확정하지 않는다.')]

def verify():
 assert len(TEXT)==35 and len(VISUAL)==16 and set(VISUAL)<=set(TEXT)
 assert set(TEXT)<=set(range(1,96))|set(range(191,274))
 values=[0,10,10,20];assert sum(values)==40 and sum(values)/len(values)==10
 assert 7-0==9-2==7 and len(range(2,10))==8 and len(range(2,9))==7

def main():
 verify();registry=load_registry()
 if SOURCE in registry['sources']:
  print('Selected ninth-edition reading remains current; no automatic refresh');build_report();return
 old=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews())
 assert not {m[0] for m in MAPPINGS}&{v['id'] for v in registry['claims']}
 pdf=ROOT/'tmp/literature/DICK_CAREY_2022_9ed.pdf';assert hashlib.sha256(pdf.read_bytes()).hexdigest()==SHA
 audit_path='data/literature_evidence/DICK_CAREY_2022_candidate_asset_audit.json';audit=json.loads((ROOT/audit_path).read_text(encoding='utf-8'))
 assert audit['integrity_status']==INTEGRITY['status'] and audit['whole_book_obtained'] is False
 corrections=[
  dict(kind='asset_integrity_and_edition',locations=['PDF2–3','PDF95/190 → PDF191','candidate_asset_audit'],action='9판2022년·인쇄ISBN9780135824146/전자ISBN9780135824139를7판 국제판과 분리했다. 파일439쪽은95쪽 두 묶음과83쪽 세 묶음의 반복이며 인쇄71–405가 빠져 있다. 중복을 읽기 쪽으로 더하지 않고 전체 정식 판본 확보·동일성 인증을 주장하지 않는다.'),
  dict(kind='diagram_not_universal_prerequisite',locations=['PDF85,87–93,227–228'],action='정보 묶음의 번호와 순서 화살표·병행 활동·분기·회귀를 구별했다. 그림3.7의5/6은 병행 배치이며 번호만으로5후6의 필수 순서를 만들지 않는다. 부록C의V 표시·출발 기능 선은 해당 작문 설계의 사례이고 현재 수학의 AND/OR 위계나 학생 발달 단계의 검증이 아니다.'),
  dict(kind='performance_scope_and_alignment',locations=['PDF83–88,229–233'],action='교사의 설명·학습자의 수행·용어 회상·분류·생산을 구별한다. 동사 목록만으로 수학적 설명을 낮은 수준으로 판정하지 않고 실제 요구와 조건을 본다. PDF231의 밑줄은 텍스트 추출에 보존되지 않아 이미지에서 확인했다. 원문의 영어 문항을 한국어 수학 평가로 복사하지 않는다.'),
  dict(kind='example_bound_not_empirical_effect',locations=['PDF89,229–230'],action='Bloom–Gagne 대응표는 원문도 예시라고 제한한다. 학교·기기 작동률 약90%·Canvas 사용은 부록 사례의 서술이며 현재 환경 조사나 수업 효과 연구가 아니다. 최신 안전 규정·건강 권고·소프트웨어 사용법을 제공하는 자료로 쓰지 않는다.')]
 log=['PDF2·3·8의 표제/서지/간략 목차,PDF73–94 목표 분석 장 전체,PDF224–233 부록 도입과A–E를 읽었다. 총35쪽이며 목표 분석 참고문헌을 읽은 일은 인용 원연구를 읽은 것이 아니다.',
 '선정16쪽 전체 페이지 이미지에서 목표 평가 표·교정 전후 도식·분기/병행·목차식 정보 묶음·위계/출발 기능 선·학습자/맥락 표·평행 문항 표와 밑줄을 대조했다. 다른 쪽의 전체 이미지 확인으로 확대하지 않는다.',
 '서지는 출판사9판 페이지와 파일PDF2–3의 저자·판·저작권연도·인쇄ISBN을 대조했다. 대학 저장소 복사본의 완전성·출판사 인증 배포 여부는 별도 한계다.7판 국제판의 누락 본문으로 대체하지 않는다.']
 notes=dict(source_id=SOURCE,source_url=URL,source_pdf_url=ASSET,repository_url=REPOSITORY,source_pdf_sha256=SHA,date='2026-11-06',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,reading_log=log,source_corrections=corrections,read_scope=SCOPE,text_pdf_pages=TEXT,visual_pdf_pages=VISUAL,source_integrity=INTEGRITY,asset_audit_file=audit_path,asset_audit_sha256=hashlib.sha256((ROOT/audit_path).read_bytes()).hexdigest(),visually_reviewed_pages=[dict(pdf_page=p,sha256=hashlib.sha256((ROOT/f'tmp/literature/dick9-goal-p{p}.png').read_bytes()).hexdigest()) for p in VISUAL],unread_followups=['파일에 없는 인쇄71–405의4–12장 핵심 본문은 미확보다. 부록C와E를 보았어도 하위 기능 분석·학습자/맥락·수행목표·평가·형성평가 장 전체를 읽은 것이 아니다.','파일 내 다른 유일 구간인 도입·요구 분석·총괄평가와 부록F–M·용어집·색인은 후속 검토다. 누락 본문·공식 판본 동일성·원연구·실제 독립/학생 검증을 별도로 남긴다.'])
 npath=ROOT/NOTES;npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 b=dict(id=SOURCE,title='The Systematic Design of Instruction, ninth edition — selected goal analysis and appendices',authors=['Walter Dick','Lou Carey','James O. Carey'],year=2022,edition='9th',print_isbn='9780135824146',epub_isbn='9780135824139',kind='교수설계 교재의 선정 대목; 불완전한 저장소 복사본',url=URL,review_scope=SCOPE,supports=['수업 순서·수행 절차·하위 기능의 구별','목표·조건·평가 과제의 대응과 부분 수행의 관찰 범위'],does_not_establish='전체 원전 확보·7판 누락 장의 검토·한국 수학 과제의 교수 효과·진단 타당성',next_review='7판 국제판과9판을 분리한다.9판 인쇄71–405는 미확보이며 공식 판본의 해당 대목과 동일성 대조가 남는다. 파일 내 총괄평가·부록F–M 등은 실제 읽은 범위부터 후속 확인한다. 원연구·독립 검토·현재 학생 응답은 별도 근거가 필요하다.')
 registry['sources'][SOURCE]=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-06',snapshot_kind='authored_review_notes',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),source_pdf_sha256=SHA,redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),display=dict(title=b['title'],url=URL,authors_year='Dick·Carey·Carey,2022,9판의 선정 대목'),read_scope=SCOPE,text_pdf_pages=TEXT,visual_pdf_pages=VISUAL,source_integrity=INTEGRITY,scope_note='9판 목표 분석·부록의 지정 범위 읽기다.7판과 구별하며 전권 확보·독립 검토·학생 검증으로 합산하지 않는다. 불완전한 대학 저장소 복사본의 출판사 인증 배포 여부는 확인되지 않았다.',method_note='목표의 절차·정보 묶음·하위 기능 예,목표/조건/평가의 대응을 설계 참고로 읽었다. 현재 수학 과제는 자체 변형이며 인과 효과 연구나 표준화된 검사 결과가 아니다.',limits='파일439쪽에는 중복과 인쇄71–405의 누락이 있다. 선정35쪽·16쪽 이미지만 확인했다. 해당 원판과의 전체 동일성·미확보 장·원연구·한국어 과제의 타당성·실제 학생 수행은 미검증이며 부분 과제를 성취기준 전체 숙달로 승격하지 않는다.',editorial_action='현재3개 기준에 설계 참고 주장2건·자체 관찰2건을 대응했다. 실제 자료 수집과 제공 자료의 계산,단위 회상과 구간/실물 측정을 구별했다. 기존 대표 원고·과제·관계 검토 근거와7판 기록은 보존한다.',independent_review=False,student_validated=False,observations=OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 p=ROOT/'data/sources.json';sources=json.loads(p.read_text(encoding='utf-8'));assert SOURCE not in {s['id'] for s in sources};sources.append(b);p.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'data/content_review_queue.json';q=json.loads(p.read_text(encoding='utf-8'));row=copy.deepcopy(q['literature_review'][-1]);row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[m[0] for m in MAPPINGS]);q['literature_review'].append(row);p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])]==old['claims'] and all(registry['sources'][k]==v for k,v in old['sources'].items())
 assert load_reviews()==relations
 build_report();print('Added ninth-edition selected reading:35 text pages,16 images,2 scoped context claims,2 own observations; no relation approvals')

if __name__=='__main__':main()

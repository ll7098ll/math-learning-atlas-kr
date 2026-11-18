"""Read all unique available segments, retaining the missing-body boundary."""
import copy
import hashlib
import json
from fractions import Fraction
from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews
from record_dick_carey_ninth_selected_review import SOURCE, URL, ASSET, SHA, INTEGRITY
from extend_dick_carey_ninth_summative_review import NOTES as PRIOR_NOTES, TEXT as PRIOR_TEXT, VISUAL as PRIOR_VISUAL

NOTES='data/literature_evidence/DICK_CAREY_2022_available_segments_review_notes.json'
PRIOR_SHA='67e2fb6206014dd60b76843d8320be67418ad7b3b525ba6c6f129d53c75ccb14'
TEXT=list(range(1,96))+list(range(191,274))
NEW_TEXT=sorted(set(TEXT)-set(PRIOR_TEXT))
NEW_VISUAL=[1,27,28,30,31,43,44,47,48,49,50,51,52,53,54,55,58,59,60,62,63,64,65,66,67,68,69,70,71,95]
VISUAL=sorted(PRIOR_VISUAL+NEW_VISUAL)
SCOPE='불완전한9판 대학 저장소 파일의 중복을 제외한 유일178쪽 내용(텍스트·표지·서지·목차·명시된 빈 쪽)을 모두 확인하고 선정98쪽 이미지를 대조했다. PDF1–95와191–273이며 도입/요구 분석/목표 분석 장(인쇄2–69),하위 기능 분석 장의 제목·목표만 있는70쪽,총괄평가(406–437),부록 도입/A–M(439–474),용어집/색인(475–481/483–488)과 빈438·482쪽 등이다. 인쇄71–405의335쪽은 파일에 없다. 확보 구간의 읽기 완료이며9판 전권 확보/정독·7판 검토가 아니다. 목차·참고문헌·색인 확인은 누락 본문이나 인용 원연구 읽기가 아니다.'

OBSERVATIONS=[
 dict(id='D9-P7',standard_codes=['6수04-01'],question='가상 활동의 조건은“평균 소요 시간이8분 이하”다. 현재 기록의 평균이12분이면 목표값−현재값=8−12=−4라는 이유로 보완할 필요가 없는가? 또[8,8,8,8]분과[2,2,2,26]분은 같은 평균이므로“모든 기록이8분 이하”라는 조건도 똑같이 만족하는가?',expected='작을수록 좋은 소요 시간에서 평균12분은8분 이하 조건을 만족하지 않으며4분을 줄여야 한다. 차가 음수라는 사실을 필요 없음으로 읽지 않고 원하는 비교 방향을 먼저 정한다. 두 자료는 모두 합32분·평균8분이어서 평균 조건을 만족하지만,둘째 자료의26분은 개별8분 이하 조건을 만족하지 않는다. 평균 목표와 모든 개별 기록의 목표는 다른 조건이다.',interpretation='요구 분석의목표−현재 상태라는 식을 비교 방향·단위·관찰 단위와 함께 사용하는 교사용 가상 예다. 평균8분이라는 조건은 이 활동에서 정한 것이며 교육과정의시간 제한·학생 속도 규준·수업 효과 기준이 아니다. 소요 시간만으로 수학적 이해를 판정하지 않는다. 집단 평균을 개인별 수행으로 바꾸지 않고,같은 과제/집단/기간/측정 기준인지 확인한다. 실제 참여자 자료나 효율 개선 결과로 집계하지 않는다.',student_validated=False),
 dict(id='D9-P8',standard_codes=['2수03-10'],question='관찰 목표가“학생이 실물 막대와cm 눈금 자를 사용해 양 끝을 맞추고 길이를 재며 단위 간격으로 설명한다”인데 자가 준비되지 않아 실물 측정을 하지 못했다. 이때0점이나 측정 기능 부족으로 판정해도 되는가? 별도 그림에서 막대가4cm부터13cm까지 놓인 것을 설명한 답과,실물에서 스스로 도구를 놓은 수행을 어떻게 구별하는가?',expected='도구가 없어 실시하지 못한 실물 측정은 미확인으로 남기고 준비/접근 조건을 기록한다. 그림의두 끝 위치 차는13−4=9cm이며 눈금점10개가 아닌1cm 간격9개다. 이 답은 주어진 그림의구간 해석을 보여 주지만 실물에서 자를 나란히 놓고 시작/끝점을 읽은 수행을 대신하지 않는다. 자를 사용하는 것이 목표에서 허용된 조건이면 자 사용 자체를 교사의정답 도움과 동일시하지 않는다.',interpretation='목표의학습자·수행·맥락·도구를 명시하는 자체 관찰이다. 장비/시간/소통 조건을 수학적 결손과 구별하고,도구 확보 뒤 실제 실시한 기록은 새 시행으로 남긴다. 목표와 다른 조건에서의정답을 원래 목표의성취로 소급하지 않는다. 시작점을 교사가 알려 주거나 올바른 배치를 보여 주었다면 그 구체적 도움을 별도로 적는다. 지원 없이 암산하는 새 목표로 바꾸거나 실물 수행을 관찰했다고 꾸미지 않는다.',student_validated=False),
 dict(id='D9-P9',standard_codes=['4수01-06'],question='수업 계획의“교사가나눗셈을7분 설명한다”와“학생이67개를4모임에 똑같이 나누고 몫·나머지와복원식을 설명한다”는 무엇이 다른가? 학생에게 십/일 블록과종이를 허용하고 처음 선택한 방법을 관찰한다.4×10을먼저 빼는 방법과십/일을나누는 방법 중 하나만 정해진 순서대로 해야 목표를 달성한 것인가?',expected='첫 문장은 교사의활동 시간이고 학생의성취를 말하지 않는다. 둘째 목표는 주어진 양/4모임/허용 도구에서 학생의분배와설명을 관찰하게 한다.67=4×10+27,27=4×6+3이므로 각 모임에16개·나머지3개다. 십블록6개와일블록7개를4모임에1십씩 나누고 남은2십을20일로 바꿔27일에서6일씩 나누어도 같은 결과다.4×16+3=67과0≤3<4를 함께 확인한다. 한 방법의성공과두 방법을비교해 양의보존을설명하는 별도 요구를 구별한다.',interpretation='모호한 계획을구체적 수행·맥락·도구로 명료화하고,현재 부분 목표의필수 조건과대안 풀이를구별하는 자체 설계다.7분은 가상 교사 활동의시간이며 숙달 기한이 아니다. 관찰 시간이 짧아 계산만 확인했다면 설명/단위 교환/상황 해석은 미확인으로 둔다. 시간을맞추려고 목표를줄인 경우 원래 목표 전체를달성했다고 하지 않는다. 설계의반복/병행 도식을학생의보편적 선수 순서로바꾸지 않으며 실제 학생의최초 방법이나 이해로집계하지 않는다.',student_validated=False),
]

MAPPINGS=[
 ('D9G07',['6수04-01'],['PDF49–54 / printed24–29 / Table2.2 and needs assessment examples'], '요구 분석에서 목표값/현재값의비교 방향·단위·관찰 단위를 명시하고,집단 평균 조건과각 기록 조건을구별하는 설계에참고한다.', '원전의단순 차이 식은 모든 지표에서양수만 부족을뜻한다는 일반 규칙이아니다. 기관 목표·사례 비율·대기시간을현재 학생의시간 규준/성취 수준으로전용하지 않고,집단 평균으로개인별 성취나인과 효과를확정하지 않는다.'),
 ('D9G08',['2수03-10'],['PDF27–37,51–60 / printed2–12,26–35 / systems view, school setting, goal rubric'], '학생의수학적 수행과도구/시간/환경 조건을구별하고,학습자·수행·실제 맥락·허용 도구를목표와관찰 기록에명시하는 설계에참고한다.', '학교 사례의해결 계획은현재 학생/교사의능력이나수업 효과 근거가아니다. 도구 미비/미실시를오답으로채우거나그림 해석을실물 측정으로승격하지 않는다. 모형의전체 효과에대한서술은현재 한국어 과제의진단 타당성을검증하지 않는다.'),
 ('D9G09',['4수01-06'],['PDF30–35,56–65,67–71 / printed5–10,31–40,42–46 / iterative design and goal clarification'], '교사 활동과학습자 성취,부분 목표와전체 목표,현재 경로의필수 수행과대안 풀이를구별하고목표 명료화/수정의범위를남기는 설계에참고한다.', '설계 단계의순서/동시 작업/수정 화살표는현재 학생의필수 발달 위계가아니다. 첫 목표문장이모호하다는이유로목표자체를버리거나하나의알고리즘만강제하지 않는다. 제한 시간에부분목표만확인했으면전체숙달로처리하지 않는다.'),
]

def verify():
 assert len(NEW_TEXT)==70 and len(NEW_VISUAL)==30
 assert len(TEXT)==len(set(TEXT))==178 and len(VISUAL)==len(set(VISUAL))==98
 assert set(VISUAL)<=set(TEXT) and set(NEW_TEXT).isdisjoint(PRIOR_TEXT) and set(NEW_VISUAL).isdisjoint(PRIOR_VISUAL)
 assert set(TEXT)==set(range(1,96))|set(range(191,274))
 assert Fraction(sum([8,8,8,8]),4)==Fraction(sum([2,2,2,26]),4)==8
 assert all(x<=8 for x in [8,8,8,8]) and not all(x<=8 for x in [2,2,2,26])
 assert 8-12==-4 and 12>8 and 12-8==4
 assert 13-4==9 and len(range(4,14))==10 and len(range(4,13))==9
 assert 67==4*10+27 and 27==4*6+3 and divmod(67,4)==(16,3)
 assert 6*10+7==67 and (6-4)*10+7==27 and 0<=3<4
 assert Fraction(5,2)*60==150 and 150-90==60 and 151-90>60
 assert Fraction(90-77,77)*100!=13 and Fraction(96-76,76)*100!=20

def main():
 verify();registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:
  assert {m[0] for m in MAPPINGS}<={c['id'] for c in registry['claims']}
  print('Available ninth-edition segments remain reviewed; no automatic refresh');build_report();return
 assert s['snapshot_file']==PRIOR_NOTES and s['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 assert hashlib.sha256((ROOT/'tmp/literature/DICK_CAREY_2022_9ed.pdf').read_bytes()).hexdigest()==SHA
 old=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews());prior=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'))
 assert s['source_integrity']==prior['source_integrity']==INTEGRITY
 assert not {m[0] for m in MAPPINGS}&{v['id'] for v in registry['claims']}
 plan=json.loads((ROOT/'tmp/literature/dick9-front/reading-plan.json').read_text(encoding='utf-8'))
 assert plan['source_pdf_sha256']==SHA and plan['text_pdf_pages']==NEW_TEXT and plan['visual_pdf_pages']==NEW_VISUAL
 for a in plan['images']:assert hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256']
 assert {a['pdf_page'] for a in plan['images']}==set(NEW_VISUAL)
 images=sorted(prior['visually_reviewed_pages']+[dict(pdf_page=a['pdf_page'],sha256=a['sha256']) for a in plan['images']],key=lambda a:a['pdf_page'])
 corrections=[
  dict(kind='available_segment_completion_not_whole_book',locations=['PDF1–95,191–273','PDF95 / printed70 / Chapter4 opening'],action='남은70쪽은 앞부분의표지·서문·상세목차·교수자안내,도입/요구분석장과참고문헌,4장제목/목표쪽이다. 인쇄70쪽은빈쪽이아니지만이어지는71–405본문은파일에없다. PDF1은추출본문이없어표지이미지를확인했다. 유일178쪽확인은정식전권확보/독해나7판누락본문해결이아니다. 상세목차에있는미확보장의제목/쪽수를실제내용독해로더하지않는다.'),
  dict(kind='waiting_time_strict_inequality',locations=['PDF49,51 / printed24,26 / Table2.2'],action='실제평균을2분30초초과,기준을90초라고서술했으므로차는60초초과다. 표의60초차라는요약을정확한등식으로옮기지않고초과/근사와단위를보존한다. 본문은기업사례의설계논의이며실제현재콜센터/학생관찰자료로집계하지않는다. 원문파일은보존하고공식정오표나저자의반올림의도는미확인으로둔다.'),
  dict(kind='needs_metric_direction_and_percentage_points',locations=['PDF49–54 / printed24–29'],action='96%−76%는20퍼센트포인트다.90%와77%,95%와81%의차도13/14퍼센트포인트이며현재값대비상대증가율과다르다.40%목표보다43%현재가크다는예는높을수록좋다는맥락의판정이고낮을수록좋은시간에그대로적용하지않는다. 서로다른분모인전체전화중약1/4와전체고장시간중20%도더하지않는다. 비교대상/방향/단위/기간/조건을명시한다.'),
  dict(kind='systems_diagram_not_student_prerequisite',locations=['PDF27–35 / printed2–10','PDF47,67–69 / printed22,42–44'],action='9판본문은점선수정경로가목표설정까지돌아가며각단계에양방향화살표로연결됨을설명한다. 이전판그림을봤다는이유로같은도식으로단정하지않는다. 선호되는설계순서와동시/반복개선을구별하며학생의유일학습순서로옮기지않는다. 그림2.4의목표상태/현재상태는병행입력이고2.5의전문가관찰/업무자목록은본문의두가능한시작방법과함께읽어언제나둘다필수인AND조건으로바꾸지않는다. A는흐름연결자이지추가학생기능이아니다.'),
  dict(kind='resource_constraint_not_skill_diagnosis',locations=['PDF51–60 / printed26–35'],action='학교사례의주40분배정과실제15–20분교수시간,교사내용지식과학생적용연습기회를구별했다. 시간/도구/일정/인력의조건을확인하기전교사/학생결손이나추가강의만이해결책이라고단정하지않는다. 사례의실행계획/확신을실제효과검증으로전용하지않는다. 현재원고의실제응답/진단타당성은별도자료가필요하다.'),
  dict(kind='goal_clarity_feasibility_and_partial_scope',locations=['PDF56–65,69–71 / printed31–40,44–46'],action='목표의추상어를삭제하는대신수행·학습자·맥락·도구를명료화한다. 수업배정/교사행동·학생행동·기관성과를구별하고목표적합성/실행가능성/명료성을따로본다. No열에NA를넣으라는원문지시를NA=부족으로읽지않는다. 시간추정은시행전확정된숙달규준이아니고부분목표로조정하면원래범위와의차이를남긴다. 적절한학습자접근없이전체형성평가과정을완료할수없다는원문의한계도현재자체점검완료와구별한다.'),
  dict(kind='history_citation_and_incidental_content_limits',locations=['PDF29,36–42,66,71–72 / printed4,11–17,41,46–47'],action='건강/제동장치예·법률/자격/소프트웨어/역사적서술을현재의료·안전·법률·제품안내로제공하지않는다. 본문인용Atkinson/Shiffrin의1960표기와참고문헌1968표기는일치하지않아해당연구를확인한것으로쓰지않는다. 참고문헌두단과색인/목차는인용문헌목록범위로만확인했으며모든원연구·전체모형의현재효과·특정이론분류의합의를검증하지않는다.'),
 ]
 p=ROOT/'data/sources.json';bibliography=json.loads(p.read_text(encoding='utf-8'));b=next(v for v in bibliography if v['id']==SOURCE);previous_b=copy.deepcopy(b)
 b.update(title='The Systematic Design of Instruction, ninth edition — all unique available segments of an incomplete copy',review_scope=SCOPE,next_review='불완전한복사본의유일178쪽내용과선정98쪽이미지를확인했다. 파일내유일구간의미확인쪽은0이지만인쇄71–405의335쪽은여전히미확보다.7판의추가본문·9판공식판본과의동일성/배포인증·정오표/미해결집계·인용원연구·한국어과제의실제독립/학생검증을별도로확인한다. 출판사인증전권을확보하면누락핵심장부터대조한다.')
 log=[
  '이전108쪽에남은70쪽을추가해PDF1–95와191–273의유일178쪽을확인했다. 표지1·서문4–6·빈7/9/25·상세목차10–24·교수자안내26·도입/요구분석27–72·4장제목/목표95다. 이미읽은2/3/8,73–94와뒤191–273은중복으로더하지않는다.',
  '새선정30쪽전체페이지PNG를각각시각확인했다.30쪽그림1.1도추가로렌더링해31쪽그림1.2와함께반복/동시개선경로를대조했다. 누적98쪽의이미지해시를보존한다. 모든178쪽을이미지대조했다고확대하지않는다.',
  '본문의목표/기관결과/교사활동/학생수행,문제원인/훈련외해결,비교방향과단위/분모,학교자원조건,명료화/실행가능성,수정/병행/분기도식을대조했다. 참고문헌은목록/주석범위이고각원연구를읽은것이아니다. 역사서술의두단은66쪽이미지에서독립된열로대조했다.',
  '첫구간의마지막95쪽은인쇄70쪽으로4장의제목/목표가있다. 다음구간은반복된앞95쪽뒤총괄평가인쇄406쪽부터시작한다.4장의학습목표를읽어도누락된하위/출발기능분석의본문을읽은것으로표시하지않는다. 유일구간읽기완료와전권미확보를함께보존한다.',
 ]
 notes=dict(source_id=SOURCE,source_url=URL,source_pdf_url=ASSET,repository_url=prior['repository_url'],source_pdf_sha256=SHA,date='2026-11-06',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,read_scope=SCOPE,text_pdf_pages=TEXT,visual_pdf_pages=VISUAL,new_text_pdf_pages=NEW_TEXT,new_visual_pdf_pages=NEW_VISUAL,source_integrity=INTEGRITY,asset_audit_file=prior['asset_audit_file'],asset_audit_sha256=prior['asset_audit_sha256'],previous_review=copy.deepcopy(s),previous_bibliography=previous_b,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,visually_reviewed_pages=images,reading_log=prior['reading_log']+log,source_corrections=prior['source_corrections']+corrections,available_segment_coverage=dict(unique_pdf_pages=178,read_unique_pdf_pages=178,unread_available_pdf_pages=[],missing_printed_body_range=[71,405],missing_printed_body_pages=335,whole_book_read=False,cover_page_without_extracted_body=1,marked_blank_pdf_pages=[7,9,25,223,267]),unread_followups=[b['next_review'],'원문 PDF·렌더링 이미지·추출 전체 텍스트는 이식용 묶음에 복제하지 않는다. 원문 표의 불일치와 공식 정오표 확인은 새 근거가 생길 때 별도로 대조한다.'])
 npath=ROOT/NOTES;npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=s['date'],read_scope=s['read_scope'])]
 s.update(date='2026-11-06',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),snapshot_history=history,bibliography_snapshot=digest(b),display=dict(title=b['title'],url=URL,authors_year='Dick·Carey·Carey,2022,9판불완전복사본의확보구간'),read_scope=SCOPE,text_pdf_pages=TEXT,visual_pdf_pages=VISUAL,method_note='남은70쪽의내용과선정30쪽이미지를읽어파일의유일178쪽내용확인을마쳤다. 표지/서지/목차/빈쪽과4장제목/목표쪽의범위를명시하고전권/누락본문으로확대하지않는다. 요구분석의비교방향·원인/환경·목표명료화/실행가능성을현재수학관찰과대응했다.',limits='파일439쪽은반복을제외하면178쪽이고그구간만읽었다. 인쇄71–405의335쪽은미확보이며7판추가본문·정식9판전권확보/독해가아니다. 선정98쪽외의이미지전체대조·배포인증·공식판본전체동일성·정오표/인용원연구·한국어과제의진단타당성/효과·실제학생수행은미검증이다.',editorial_action='이전6개주장/6개관찰을보존하고3개기준에새3개주장/3개자체관찰을대응했다. 누적주장9개·관찰9개·기준4개다. 관계검토·독립검토·학생검증에추가하지않는다.',observations=s['observations']+OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 p.write_text(json.dumps(bibliography,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'data/content_review_queue.json';q=json.loads(p.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE]);p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])]==old['claims'] and s['observations'][:6]==old['sources'][SOURCE]['observations']
 assert all(registry['sources'][k]==v for k,v in old['sources'].items() if k!=SOURCE) and load_reviews()==relations
 assert s['source_integrity']==INTEGRITY and s['independent_review'] is False and s['student_validated'] is False
 build_report();print('Completed unique available DICK9 segments:178 content pages,98 images;3 new claims/probes;335 printed body pages still missing')

if __name__=='__main__':main()

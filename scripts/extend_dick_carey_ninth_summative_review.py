"""Extend the incomplete ninth-edition reading, preserving earlier evidence."""
import copy
import hashlib
import json
from fractions import Fraction
from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews
from record_dick_carey_ninth_selected_review import SOURCE, URL, ASSET, SHA, INTEGRITY, NOTES as PRIOR_NOTES, TEXT as PRIOR_TEXT, VISUAL as PRIOR_VISUAL

NOTES='data/literature_evidence/DICK_CAREY_2022_summative_review_notes.json'
PRIOR_SHA='90b1d1a5925abfb022b73b540cd9fc3dab125296ab40053eebeed5243d0f3884'
NEW_TEXT=list(range(191,224))+list(range(234,274))
NEW_VISUAL=[191,192,194,199,203,204,205,206,208,209,210,211,212,213,214,215,216,217,218,219,220]+list(range(234,260))+[260,264,266,268,273]
TEXT=sorted(PRIOR_TEXT+NEW_TEXT)
VISUAL=sorted(PRIOR_VISUAL+NEW_VISUAL)
SCOPE='9판의 불완전한 대학 저장소 파일에서 누적 지정108쪽 텍스트·68쪽 이미지를 확인했다. 이전 서지·간략 목차·목표 분석 장(인쇄48–69)·부록 도입/A–E(439–448)에 총괄평가 장(406–437),부록F–M(449–474),용어집(475–481),색인(483–488)과 명시된 빈438·482쪽을 더했다. 참고문헌/색인 읽기는 인용 원연구/해당 본문 읽기가 아니다. 중복 쪽을 합산하지 않으며7판 검토·9판 전권 확보/정독이 아니다.'

OBSERVATIONS=[
 dict(id='D9-P3',standard_codes=['4수01-06'],question='교사는 이 나눗셈 관찰의 세 요소를 계산,복원식과 나머지 조건의 설명,상황에서 나머지 처리로 정한다. 가상 기록에는53÷4=13 나머지1과58÷4=14 나머지2의 답만 맞았다고 적혀 있다. 두 답의 정답률이 높으면 세 요소를 모두 확인했다고 할 수 있는가?53=4×12+5도 올바른 최종 몫·나머지인가?',expected='응답한 두 계산은 모두 맞아2문항 중2문항 정답이다. 그러나 이 기록으로 확인한 요소는 계산 하나뿐이고 설명과 상황 해석은 미확인이다.53=4×12+5라는 복원 등식은 참이지만5는 제수4보다 크므로 최종 나머지가 될 수 없다.4개로 한 묶음을 더 만들면13 나머지1이다. 분모가 응답 문항 수인지 계획한 요소 수인지 명시해야 한다.',interpretation='교사용 가상 자료로 정답률2/2와 계획 요소의 관찰 범위1/3을 구별한다. 이 세 요소는 해당 관찰의 설계이며 성취기준 전체를 대표하는 검증된 배점이 아니다. 관찰하지 않은 설명/상황 해석을 오답0으로 채우거나 계산 정답을 전체 숙달로 올리지 않는다. 초등3~4학년에게 백분율 계산을 새 필수로 요구하지 않는다. 원문 그림13.2의79%/64%는 전체 행·산출 규칙이 없어 현재 학생 비율로 전용하지 않는다.',student_validated=False),
 dict(id='D9-P4',standard_codes=['2수03-10'],question='교사는 가상 길이 기록의1·2번을 주어진 두 끝 눈금에서 길이 설명하기,3·4번을 실물에서 자를 나란히 놓고 시작점/끝점을 맞추기 과제로 정했다. A의 기록은[맞음,맞음,틀림,틀림],B는[틀림,틀림,맞음,맞음]이다. 같은2개 정답이라는 이유로 같은 후속 활동을 줄 수 있는가? C의3·4번을 실시하지 않았다면 어떻게 적는가?',expected='두 기록 모두4문항 중2문항 정답이지만A는 실물 정렬과 측정 과정,B는 눈금 위치와 길이의 관계를 더 확인해야 한다. 예를 들어4cm부터10cm까지는6cm이며 눈금점7개가 아닌 단위 간격6개다. 각 영역의 두 문항을 모두 맞히면 그 영역을 이번 기록에서 확인했다는 임시 기준을 쓰면A와B가 확인한 영역은 서로 반대다. C의 미실시 항목은 미확인으로 남긴다.',interpretation='학생×문항×목표 배열의 자체 예다. 원문 부록L의빈칸=오답이라는 코딩은 그 표의 명시된 약속이므로 현재 미실시/결측에 복사하지 않는다. 같은 총점이 같은 어려움이나 교수 처방을 뜻하지 않는다. 두 문항 모두 정답이라는 기준은 이 가상 관찰의 임시 기준이며 진단 정확도가 입증된 숙달 절단점이 아니다. 도구/읽기/소통/제작 오차와 수학적 설명을 추가 확인하고 실제 학생 자료로 집계하지 않는다.',student_validated=False),
 dict(id='D9-P5',standard_codes=['6수04-01','6수04-03'],question='가상 수업에서 제공된0·6·12분의 평균을6분이라고 답했다. 이후 설문에“생활에서도 쓸 수 있다”고 답하면 실제 적용까지 확인한 것인가? 나중에 제공된3·9·15분의 평균을 구하는 과제와 직접 조사 질문·기간·대상·기록 기준을 정하고 자료를 수집하는 과제는 어떤 증거를 각각 남겨야 하는가?',expected='처음 자료의 합18분을3기록에 균등하게 나누면6분이고,나중 자료는합27분을3기록으로 나누어9분이다. 주어진 다른 수의 계산을 성공한 기록,시간을 두고 다시 설명한 기록,실제 질문에 맞게 수집/표현/해석한 기록,쓸 수 있다는 자기보고는 각각 다른 증거다. 설문만으로 실제 적용이나 수업 때문에 생긴 효과를 확정할 수 없다. 실수집에는 질문·대상·기간·같은 기록 기준·미응답 처리·원자료와 질문에 대한 해석을 남긴다.',interpretation='자체 가상 계산과 실시 계획이며 실제 후속 조사 결과가 아니다. 재확인 시점·자료/도구·허용 도움·참여자와 각 시행을 연결하고 같은 참여자의 여러 시행을 독립 학생 수로 세지 않는다.0이라는 기록과 미응답을 구별한다. 수집 기회/도구/언어/환경의 제약을 곧 수학적 결손으로 단정하지 않으며 모든 수집을 거치지 않은 계산 과제는 그 부분 범위로 해석한다. 원문30명/1년 사례를 현재 참여자 수·고정 추적 기간·현재 효과로 전용하지 않는다.',student_validated=False),
 dict(id='D9-P6',standard_codes=['4수01-06'],question='가상 최초 답은57÷4=13 나머지5다. 교사가 정답만 알려 주는 대신 남은5개에서4개를 한 묶음 더 만들게 했다. 그 뒤의 수정 답과,다른 수62÷4의 재확인 답을 어떤 구분으로 기록하는가? 계산은 맞아도“62명을4명씩 태우는 차”라는 상황의 차 수가 같은가?',expected='57=4×13+5는 양을 복원하지만 나머지5≥4이므로 한 묶음을 더 만들어14 나머지1로 수정해야 한다.62÷4=15 나머지2이고4×15+2=62,0≤2<4를 함께 확인한다.62명을 모두 태우려면4명 정원의 차15대로는2명이 남아16대가 필요하다. 최초 답,구체적 도움,도움 뒤 수정,새 수/맥락에서의 재확인을 따로 남긴다.',interpretation='문제 발견→근거→구체적 수정→새 조건에서 재확인으로 연결한 자체 설계다. 정답을 보고 고친 답을 최초 독립 수행으로 바꾸거나 수정안을 작성했다는 이유로 효과가 검증됐다고 하지 않는다. 가상 오답 하나로 선수 기능 부재를 확정하지 않고 묶음 구성·단위·언어·상황 이해를 대조한다. 원문 부록M의영어 작문 집단에서 제안한 기능 제외/분기를 한국 수학 학생 전체의 선수 목록 변경으로 옮기지 않는다.',student_validated=False),
]

MAPPINGS=[
 ('D9G03',['4수01-06'],['PDF193–206 / printed408–421 / Table13.1,Figure13.2'], '내용의 정확성·평가 범위·학습자의 정답률을 구별하고,부분 계산만 맞은 기록에서 미확인 설명/상황 해석을 찾아 후속 관찰을 설계한다.', '원전의형성/총괄 구별과 설계 예는 현재 학생의 숙달·유일한 학습 순서·수업 효과를 입증하지 않는다. 누락 행의79%/64%를 학생 비율이나 검증된 배점으로 전용하지 않는다.'),
 ('D9G04',['2수03-10'],['PDF234–235,245,247,253–255 / printed449–450,460,462,468–470 / AppendicesF,I,J,L'], '문항을목표에 연결한 개별 배열에서 같은 총점의 다른 수행을 구별하고,실물 측정과 눈금 해석을 분리해 후속 관찰을 정한다.', '부록의영어 작문 예는 한국어 수학 검사의 타당성/규준이 아니다. 표별문항 수·시점·범례·숙달 기준이 같다는 확인 없이 표를 통합하지 않으며 원문의빈칸=오답을 미실시/미응답에 복사하지 않는다.'),
 ('D9G05',['6수04-01','6수04-03'],['PDF199–204,211–219,239–241 / printed414–419,426–434,454–456 / impact forms and AppendixH'], '즉시 계산·시간을 둔 재확인·실제 맥락 적용·자기보고·실행 환경을 나누어 기록하는 평가 계획에 참고한다.', '자기보고/만족도·전문가 평정·새 수의 정답만으로 실제 탐구 전체나 인과 효과를 확정하지 않는다. 원전의성인/학교 작문 집단·30명/1년·설문 양식은 현재 한국 학생 관찰 결과가 아니다.'),
 ('D9G06',['4수01-06'],['PDF208–211,236–238,248–259 / printed423–426,451–453,463–474 / feedback and AppendicesG,K–M'], '정답 전달과 이유를 확인하는 피드백을 구별하고,관찰 근거→수정 내용→새 수/맥락의 재확인으로 이어지는 기록을 설계한다.', '원전의수정 제안은 현재 과제에서 실행/효과가 입증됐다는 뜻이 아니다. 한 집단의사전 결과를 근거로 기능을 출발 조건으로 옮긴 예를 모든 학생의 보편적 위계로 전용하지 않는다. 도움 전후·검사 시점·목표별 결과를 유지한다.'),
]

def verify():
 assert len(NEW_TEXT)==73 and len(NEW_VISUAL)==52
 assert len(TEXT)==len(set(TEXT))==108 and len(VISUAL)==len(set(VISUAL))==68
 assert set(VISUAL)<=set(TEXT) and set(TEXT)<=set(range(1,96))|set(range(191,274))
 assert set(NEW_TEXT).isdisjoint(PRIOR_TEXT) and set(NEW_VISUAL).isdisjoint(PRIOR_VISUAL)
 assert divmod(53,4)==(13,1) and divmod(58,4)==(14,2) and 4*12+5==53 and 5>=4
 a=[1,1,0,0];b=[0,0,1,1]
 assert sum(a)==sum(b)==2 and [all(a[:2]),all(a[2:])]==[True,False] and [all(b[:2]),all(b[2:])]==[False,True]
 assert 10-4==6 and len(range(4,11))==7
 assert Fraction(sum([0,6,12]),3)==6 and Fraction(sum([3,9,15]),3)==9
 assert divmod(57,4)==(14,1) and 4*13+5==57 and divmod(62,4)==(15,2) and (62+3)//4==16
 assert Fraction(12-5,15)*100==Fraction(140,3) and Fraction(10-5,15)*100==Fraction(100,3)

def main():
 verify();registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:
  assert {m[0] for m in MAPPINGS}<={c['id'] for c in registry['claims']}
  print('Ninth-edition summative reading remains current; no automatic refresh');build_report();return
 assert s['snapshot_file']==PRIOR_NOTES and s['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 assert hashlib.sha256((ROOT/'tmp/literature/DICK_CAREY_2022_9ed.pdf').read_bytes()).hexdigest()==SHA
 old=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews());prior=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'))
 assert s['source_integrity']==prior['source_integrity']==INTEGRITY
 assert not {m[0] for m in MAPPINGS}&{v['id'] for v in registry['claims']}
 plan=json.loads((ROOT/'tmp/literature/dick9-summative/reading-plan.json').read_text(encoding='utf-8'))
 assert plan['source_pdf_sha256']==SHA and plan['text_pdf_pages']==NEW_TEXT and plan['visual_pdf_pages']==NEW_VISUAL
 for a in plan['images']:assert hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256']
 assert {a['pdf_page'] for a in plan['images']}==set(NEW_VISUAL)
 images=prior['visually_reviewed_pages']+[dict(pdf_page=a['pdf_page'],sha256=a['sha256']) for a in plan['images']]
 images=sorted(images,key=lambda a:a['pdf_page'])
 # The authored notes below state discrepancies without altering the source PDF.
 corrections=[
  dict(kind='formative_stage_source_mismatch',locations=['PDF193–194 / printed408–409 / Table13.1','PDF262 / printed477 / glossary'],action='인접 본문은 형성평가를 일대일·소집단·현장 시행으로 설명하지만 표13.1의해당 세 번째 행은Impact evaluation이다. 용어집은field trial을형성평가의세 번째이자총괄평가의두 번째로 정의한다. 총괄평가의실제 적용 분석과 형성평가의현장 시행을 목적/설계로 구별하고 표의단어 하나로 동일시하지 않는다. 공식 정오표는 미확인이고 원문 파일은 보존한다.'),
  dict(kind='coverage_rating_denominator_limit',locations=['PDF205–206 / printed420–421 / Figure13.2'],action='도식의전체 기능 수22와 평정1/2/3,요약100/79/79/64%를 확인했다. 표는1.0–2.2 뒤Etc.로 생략되므로 전체 행/집계 규칙을 재구성할 수 없다.79%/64%를22개 중 이진 개수로 역산하거나 현재 학생 정답률로 쓰지 않는다. 내용 정확성·완전성·직무 연결·사후검사 포함을 별개로 유지한다.'),
  dict(kind='appendix_item_count_and_timepoint_mismatch',locations=['PDF245,253–255 / printed460,468–470 / AppendicesI,L'],action='부록I의선수 검사 문항은11개지만 부록L의선수 배열은10개다. L의사후 문항 배열에서14/15로 제시된5.11목표 비율과 시점별목표 배열의사후10/15는 같지 않다. 다른 판/검사/숙달 기준인지 명시된 연결이 없어 하나의 정합 원자료로 통합하지 않는다. 시점별배열의5.10은사전5/15→중간15/15→사후12/15,5.11은5/15→14/15→10/15다. 표시 백분율의차는 각각33→100→80,33→93→66으로,Diff행의+67/−20과+60/−27은인접 시점 차에 대응하지만 주석은사전/사후라고 설명한다. 사전→사후의실제 개수 차는7/15·5/15이며약46.67·33.33퍼센트포인트다. 정오표나 저자 의도를 단정하지 않고 원문의절사/반올림도 통일됐다고 가정하지 않는다.'),
  dict(kind='subgroup_denominator_and_missingness',locations=['PDF253–255,258 / printed468–470,473 / AppendicesL,M'],action='전체15명과하위그림4명(1–4)/10명(6–15)의합14명을 구별한다.5번의일부 선수 기능 결손을M이별도로설명하며5번을조용히삭제하거나4+10을전체15로바꾸지 않는다. 원문 표의빈칸=오답은그표의코딩이고 현재 미실시/미응답은미확인으로둔다. 목표별판정/문항정답/집단비율/시점별같은참여자를구별한다.'),
  dict(kind='ratings_self_report_and_transfer_boundary',locations=['PDF203–219 / printed418–434'],action='No/Some/Yes와NA,1–3·1–4평정의대상/척도,이미사용중/새사용/미사용과복수선택이유를구별한다. 자기보고와관찰/산출물,즉시/지연/실맥락수행,개인/조직효과를구별하며설문의인과표현이인과추론을입증하지않는다. 전문가체크리스트만으로현재독립검토/학생검증을완료하지않는다.'),
  dict(kind='feedback_revision_and_entry_conditions',locations=['PDF234–259 / printed449–474 / AppendicesF–M'],action='선수/사전/중간/사후/실제산출물의역할과다른예문,분류와생산,정답과설명피드백,문제/수정안/근거열을대조했다. 시간표의빈시간은0분으로채우지않고절차도번호를보편적선수관계로전용하지않는다. 예시집단에서선수로옮긴5.8/5.9를현재수학학생모두의이미숙달한기능으로가정하지않는다. 수정안과실제재시행결과를구별한다.'),
  dict(kind='incidental_content_and_index_boundary',locations=['PDF243,250 / printed458,465','PDF260–273 / printed475–488'],action='동기유발글의달/태양계설명과소프트웨어/역사적예측은현재과학·기기안내의근거로전용하지않는다. 문장유형예의기준은영어작문사례이고수학적설명분류로복사하지않는다. 용어집의간략정의와색인위치를읽었어도누락된71–405쪽본문·표준최신버전·인용원연구를읽은것으로집계하지않는다.'),
 ]
 log=[
  '새PDF191–223의총괄평가장/참고문헌/빈438쪽,234–259의부록F–M,260–266의용어집,267의빈482쪽,268–273의색인을실제로읽었다. 새73쪽중명시된빈쪽2개가포함된다. 이전35쪽과합108쪽이고뒤반복구간은더하지않았다.',
  '새선정52쪽을Poppler110dpi전체페이지PNG로렌더링하고각이미지를개별확인했다. 최초4개동시출력은컨텍스트제한으로보이지않아읽기완료로세지않았고191/192/194/199를개별재확인했다. 누적68쪽이미지해시를보존한다. 본문추출은pypdf이며Poppler텍스트추출이라고표시하지않는다.',
  '총괄평가의두단계/의사결정,도식의분기/병행/연결자,평정척도,설문시점/복수응답/사전사용,부록의목표/문항/검사시점/개별배열/하위집단/수정근거를대조했다. 도식번호를현재학생의보편적발달위계로바꾸지않는다.',
  '파일내유일178쪽중108쪽의지정읽기다. 앞부분유일70쪽은아직미검토이며중간인쇄71–405는파일에없다.7판미확보본문·공식판본과전체동일성·현재독립/학생검증은해결되지않았다.',
 ]
 p=ROOT/'data/sources.json';bibliography=json.loads(p.read_text(encoding='utf-8'));b=next(v for v in bibliography if v['id']==SOURCE);previous_b=copy.deepcopy(b)
 b.update(title='The Systematic Design of Instruction, ninth edition — selected goal analysis, summative evaluation and appendices',review_scope=SCOPE,next_review='현재유일178쪽중지정108쪽텍스트·68쪽이미지를확인했다. 앞부분도입/요구분석등남은70쪽은미검토이며인쇄71–405는미확보다.7판의누락본문·공식판본과전체동일성·정오표/미해결집계·인용원연구·한국어과제의실제독립/학생검증을별도로대조한다.')
 notes=dict(source_id=SOURCE,source_url=URL,source_pdf_url=ASSET,repository_url=prior['repository_url'],source_pdf_sha256=SHA,date='2026-11-06',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,read_scope=SCOPE,text_pdf_pages=TEXT,visual_pdf_pages=VISUAL,new_text_pdf_pages=NEW_TEXT,new_visual_pdf_pages=NEW_VISUAL,source_integrity=INTEGRITY,asset_audit_file=prior['asset_audit_file'],asset_audit_sha256=prior['asset_audit_sha256'],previous_review=copy.deepcopy(s),previous_bibliography=previous_b,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,visually_reviewed_pages=images,reading_log=prior['reading_log']+log,source_corrections=prior['source_corrections']+corrections,unread_followups=[b['next_review'],'용어집/색인/참고문헌의목록은해당미확보본문이나인용연구의실제읽기를대신하지않는다. 원문PDF/렌더링이미지/추출전체텍스트는이식용묶음에포함하지않는다.'])
 npath=ROOT/NOTES;npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=s['date'],read_scope=s['read_scope'])]
 s.update(date='2026-11-06',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),snapshot_history=history,bibliography_snapshot=digest(b),display=dict(title=b['title'],url=URL,authors_year='Dick·Carey·Carey,2022,9판의선정대목'),read_scope=SCOPE,text_pdf_pages=TEXT,visual_pdf_pages=VISUAL,method_note='총괄평가장·부록F–M·용어집/색인과빈쪽의새73쪽텍스트·선정52쪽이미지를추가대조했다. 평가범위/정답률·개별목표배열·시점/자기보고/실제적용·수정/재확인을구별한다.',limits='불완전한439쪽파일의유일178쪽중지정108쪽텍스트·68쪽이미지다. 앞70쪽미검토·인쇄71–405미확보이며7판전권/9판전권확보나공식배포인증이아니다. 원문표의일부단계명·문항수·시점별집계불일치와분모/집계규칙의한계를보존한다. 현재한국학생의진단타당성·효과·실제수행은미검증이다.',editorial_action='이전2개주장/2개관찰을보존하고4개기준에새4개주장/4개자체관찰을대응했다. 누적주장6개·관찰6개·기준4개다. 관계검토·독립검토·학생검증에는더하지않는다.',observations=s['observations']+OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 p.write_text(json.dumps(bibliography,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'data/content_review_queue.json';q=json.loads(p.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE]);p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])]==old['claims'] and s['observations'][:2]==old['sources'][SOURCE]['observations']
 assert all(registry['sources'][k]==v for k,v in old['sources'].items() if k!=SOURCE) and load_reviews()==relations
 assert s['source_integrity']==INTEGRITY and s['independent_review'] is False and s['student_validated'] is False
 build_report();print('Added ninth-edition summative/appendices:73 new text pages,52 new images,4 claims,4 own probes;70 available unique front pages pending')

if __name__=='__main__':main()

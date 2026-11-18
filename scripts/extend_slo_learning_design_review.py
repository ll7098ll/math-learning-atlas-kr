"""Extend the same SLO source to the complete learning-design chapter."""
import copy
from literature_review import ROOT,load_registry,build_report,digest,target_value
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,relation_snapshot,apply_literature_context
SOURCE='SLO_EDR_2013_INQUIRY_SELECTED';DATE='2026-11-17';CACHE=ROOT/'tmp/literature/slo-learning-design-20261117'
PRIOR='data/literature_evidence/SLO_EDR_2013_formative_followup_review_notes.json'
PRIOR_SHA='5eb1463a01695b54064c161c02e2e70efe9e4cae38e36f790ab8236d931aab98'
PRIOR_BIB='e55a84296c8cbfc96b1a1b209561067ffa1e306d8a77e9d661ae0f9ca69fe19c'
NOTES='data/literature_evidence/SLO_EDR_2013_learning_design_review_notes.json'
SHA='952ca654a1d44ed91cd9304e7d8386b3b7bbd0d7364a61c2c60dd41600f18110'
NEW_TEXT=list(range(74,114));NEW_VISUAL=list(range(73,115))
TITLE='Educational Design Research Part A: complete learning-design chapter3 and formative-evaluation chapter6, plus selected introduction, revised November2013'
SCOPE='개정2013년 Part A206쪽 중 누적 추출문70쪽·판면73쪽을 대조했다. 새3장PDF73–114의 본문/참고문헌40쪽과 삽화/본문/그림1–11/표/마지막 머리말 쪽을 포함한42판면을 읽었다. 저자는 Gravemeijer/Cobb이며2013장과 인용된2006이전 장·원논문은 구별한다. PDF73은 삽화,114는 머리말/쪽번호만 있어 추출문 독해 쪽에 넣지 않는다. 기존6장전체·선정 도입 읽기와30텍스트/31판면의 이력을 보존했다.3·6장 이외는 선정 범위로 전권 독해가 아니다.'
LIMITS='수학 수업 설계의 방법론과 저자가 보고한 수업 사례를 읽은 것이다. 원자료·원논문·2006이전 장·Minitool실행·Part A전권/Part B51사례·현재 국내 학생의 효과는 검증하지 않았다. 예상 경로와 실제 사고, 전체 자료와 선택 장면, 재구성한 수정 경로와 시행 버전을 구별한다. 원문의 미국 연령/기간·이론 개발·영상 기록을 학교 탐구의 고정 요구로 쓰지 않는다. 과정 설명을 단일 요소의 평균 인과 효과나 통계적 대표성으로 바꾸지 않는다. 자체 수치 반례·발문·기록지는 학생 자료가 아니다.'
LI='12수과02-01';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04';BX='9수04-08';SC='9수04-09';CO='12실통02-02';DA='12실통02-03';AN='12실통02-04'
def c(n,codes,pages,support,limit):return dict(id=f'SLD17-{n:02d}',source_id=SOURCE,role='related_theoretical_context',standard_codes=codes,locations=[f'PDF{p} / 인쇄{p-1}' for p in pages],support=support,does_not_establish=limit,independent_review=False,student_validated=False)
CLAIMS=[
 c(1,[PL,RU],[77,78,79,82,83,86,87],'목표·시작점·과제·예상한 사고와 지원을 연결해 계획하고, 실제 설명/다른 풀이를 보고 경로를 수정하는 자체 활동에 참고한다. 예상 사고·활동 순서와 실제 관찰 근거를 따로 남긴다.','가설적 학습 경로를 모든 학생의 고정 선수 사슬로 바꾸지 않는다. 정답·도구 작동만으로 예상 사고나 학습의 부재/완료를 판정하지 않으며 원문 기간·참여 방식·새 이론 개발을 학생의 의무로 만들지 않는다.'),
 c(2,[LI,RU],[74,78,79,83,84,87,109,110,111,112,113],'문헌에서 가져온 방법·자신이 바꾼 활동·자료의 생성/측정 맥락과 실제 수행을 구별해 기록한다. 원문은 이 통계 사례에서 자료 생성 과정을 토의했지만 학생이 자료를 직접 수집한 것은 아니라고 설명한다.','학생의 자료 수집을 했다고 덧붙이거나 참고문헌 목록을 원논문 독해로 세지 않는다. 이 장의 사례·2006이전 장·인용 논문·자체 수학 예를 같은 원자료로 합치지 않는다.'),
 c(3,[OU,RE],[96,97,101,102,103,104,106,107],'전체 기록과 경쟁 설명·반박·실패를 대조하고 주장에서 원근거까지 추적할 수 있게 발표/성찰을 구성한다. 수정 전후 버전과 실제 시행 범위를 연결하며 새 경로의 재확인 계획을 남긴다.','몇 개의 보기 좋은 발언을 전체 학습의 증거로 바꾸지 않는다. 이전 사전/사후 결과가 아직 시행하지 않은 재구성 수업안을 직접 검증하지 않는다. 추적 가능성을 동일 결론의 강요·통계적 대표성으로 바꾸지 않는다.'),
 c(4,[BX,AN],[77,84,93,94,95,98,99,100],'중심·퍼짐·분포를 함께 비교하고 한 막대가 측정값인지 도수인지 구별하는 자체 과제에 참고한다. 사분 구분·상자그림은 내부 값과 형태 일부를 잃는 요약임을 확인한다.','원문의 단봉 가정·도식·생략된 점을 무시해 다섯 수만으로 유일한 밀도/봉우리·정규성을 확정하지 않는다. 원자료 없이 그림의 평균·모양을 재현하거나 학생 이해를 입증했다고 하지 않는다.'),
 c(5,[CO,AN],[83,84,98,99,100],'측정 단위·자료 생성·비교 기준을 먼저 정하고 평균·기준 초과 비율·퍼짐 등 서로 다른 기준을 구별한다. 전후 두 집단의 분포 비교와 같은 개인의 변화·원인 주장을 나누는 자체 과제를 설계한다.','그림7의 역슬래시+s 표기를 그림2와 발언의 hours 대신 seconds로 임의 전용하지 않는다. 선택 기준·미대응 전후 자료·역사적 임상 예시의 학생 발언을 모집단 결론·단일 원인·현재 치료의 권고로 바꾸지 않는다.'),
 c(6,[SC,DA],[100,101],'두 변수의 짝과 단위·집단 맥락을 유지하며, 설명변수 구간별로 다른 변수의 중심뿐 아니라 퍼짐도 비교하는 자체 교사용 확장에 참고한다.','원문의 역사적 성별/소득 자료를 현재 수치로 쓰거나 그림에서 원자료를 역산하지 않는다. 산점도를 직선 하나로 환원하지 않으며 회귀 기울기0을 무관계·독립·인과 부재의 증명으로 바꾸지 않는다. 국내 필수 통계 개념을 새로 강제하지 않는다.'),
 c(7,[PL,RE],[79,80,88,89,90,105,106,108],'과제·도구뿐 아니라 질문·설명/반론의 규범·교사의 지원을 함께 계획하고 실제로 어떻게 쓰였는지 성찰한다. 집단의 공유된 설명과 개별 학생의 생각을 구별한다.','설명 규칙을 적거나 도구를 제공한 사실이 모든 학생에게 같은 이해를 보장하지 않는다. 교사 연수·전문 연구의 영상/면담 방식을 학교 탐구에 일률적으로 강제하지 않는다.'),
 c(8,[LI,RE],[91,92,93,104,105,107,108],'학생에게 의미 있는 문제와 기존 비형식 풀이에 맞는 모형을 검토하고, 한 상황을 나타내던 모형을 다른 수학적 설명에 어떻게 쓰는지 관찰하는 자체 질문에 참고한다. 다른 수업에 적용할 때는 맥락과 지원의 차이를 기록한다.','RME의 현실을 생활 소재만으로 제한하거나 모형을 고정 절차로 강제하지 않는다. 다른 반/나라의 적용 가능성을 실제 국내 효과로 세지 않고, 이 장의 이론적 설명을 모든 학습자의 보편 경로로 바꾸지 않는다.')]
def p(n,code,q,e,i):return dict(id=f'SLD-P{n:02d}',standard_codes=[code],question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS=[
 p(1,PL,'목표·과제·예상한 풀이를 적은 계획과 실제 학생의 설명은 어떤 관계인가?','목표를 향한 한 가설로 적고 과제/질문/지원·예상 사고를 나눈다. 실제 설명·다른 풀이·막힌 곳의 근거를 보고 다음 활동과 경로를 수정한다.','계획을 실제 응답으로 채우지 않는다. 같은 순서·기간·풀이를 모든 학생에게 요구하는 선수 사슬이나 학습 효과 검증으로 확대하지 않는다.'),
 p(2,RU,'가상으로, 정답은 같지만 한 사람은 그림을 나누고 다른 사람은 식을 계산했다. 정답만 보고 같은 생각을 했거나 한 경로를 모른다고 해도 되는가?','풀이·설명·사용한 기준물과 단위·질문에 대한 반응을 더 확인한다. 수행에서 본 사실과 사고에 대한 해석·대안 설명을 구분한다.','이 가상 상황과 기대 설명은 실제 학생 사례가 아니다. 관찰하지 않은 사고를 확정하거나 선택하지 않은 경로의 부재를 판정하지 않는다.'),
 p(3,LI,'배터리 사례를 소개하며 학생들이 자료를 직접 수집했다고 쓰려 한다. 이 장에서 실제로 확인한 범위는 무엇인가?','자료 생성·측정 방법을 토의한 뒤 제공된 자료를 분석한 사례로 구분한다. 학생이 수집하지 않았다는 본문을 유지하고 출처·원자료 미확인·자신의 새 수집 계획을 나눠 적는다.','참고문헌이나 그림을 봤다는 사실을 원논문·원자료·도구 실행의 확인으로 바꾸지 않는다.'),
 p(4,RE,'좋은 설명 한 장면을 골랐지만 나머지 기록에 다른 풀이·반박이 있다. 어떻게 분석할 것인가?','전체 자료·시점·과제·버전을 확인하고 처음 해석·반박·수정 이유·경쟁 설명을 추적한다. 선택한 장면은 전체 검토 뒤의 예시인지 명시하고 다른 해석 가능성을 남긴다.','전문 연구의 전체 자료 분석을 학교 탐구에 참고하는 자체 설계다. 소수의 선택 장면이나 가상 피드백을 실제 외부 독립 검토로 세지 않는다.'),
 p(5,OU,'v1수업 뒤 검사 결과가 있고 실패 활동을 뺀v2를 만들었지만 시행하지 않았다. v2의 효과가 확인됐다고 보고할 수 있는가?','v1의 실제 시행·검사와v2의 재구성·수정 이유를 구별한다. 빠진 활동도 당시 학습에 영향을 줬을 수 있어v1결과가v2전체의 직접 검증은 아니며v2의 재확인을 계획한다.','원문에 기초한 가상 버전 예다. 근거가 있는 설계 개선과 아직 시행하지 않은 새 경로의 실제 효과를 구별한다.'),
 p(6,BX,'자체 자료 A=[0,1,2,2,3,4,6,7,8,8,9,10],B=[0,0,1,3,5,5,5,5,7,9,10,10]을 비교하라. 하위/상위6개의 중앙값을Q1/Q3로 정하면 상자그림이 내부 분포를 유일하게 정하는가?','두 자료의 다섯 수는0,2,5,8,10이고 평균도5다. 그러나5인 값은A에0개,B에4개다. IQR=6이라1.5IQR수염을 써도 둘 다0~10이며 같은 상자그림에서 내부 값·봉우리를 유일하게 복원하지 못한다.','이12개씩의 수는 자체 반례다. 원문 그림의 원자료나 학생 응답이 아니며 사분위수 관례·수염 규칙을 먼저 밝힌다.'),
 p(7,AN,'자체 가상 수명 A=[1,9,9,9]시간,B=[7,7,7,7]시간에서 평균과6시간 초과 비율을 비교하라. 어느 것이 무조건 더 좋은가?','평균은 둘 다7시간이다.6시간 초과는A가3/4,B가4/4이고 최대는A가9,B가7이다. 쓸 목적·사전 기준에 따라 요약과 결론이 달라지며 기준 선택 이유를 설명한다.','원문의 두 배터리 자료와 다른 자체 예다. 표본의 비율을 모집단 확률이나 실제 상품 성능으로 일반화하지 않는다.'),
 p(8,CO,'자체 가상 같은3대의 속도가40,50,90km/h에서 차례대로45,55,60km/h가 됐다. 평균 감소는 대부분의 차가 느려졌다는 뜻인가?','평균은60에서160/3km/h로 낮아졌지만 두 대는 빨라지고 한 대만 느려졌다. 평균·개별 변화·짝 여부를 구별한다. 실제 자료에 동일 차량ID가 없으면 개인별 변화를 재구성할 수 없다.','가상 반례이며 실제 교통 관측이 아니다. 전후 집단 차이만으로 캠페인의 인과 효과나 같은 사람 대부분의 변화를 확정하지 않는다.'),
 p(9,SC,'교사용 자체 확장: 짝(1,0),(1,10),(2,4),(2,6)에서x별y평균과 퍼짐을 비교하라. 회귀 기울기0이면 아무 관계도 없는가?','x=1,2에서y평균은 각각5이며 전체 회귀 기울기는0이다. 범위는각각10,2로 달라 같은 평균/직선이 분포의 모든 차이를 설명하지 않는다.','국내 필수 조건부 분포 공식으로 강제하지 않는 자체 확장이다. 가상 네 점을 원문의 소득 자료·인과·독립의 검증으로 쓰지 않는다.'),
 p(10,LI,'RME의 의미 있는 현실과 모형은 생활 소재 문제와 따라 할 정해진 절차만을 뜻하는가?','학생에게 의미 있게 다룰 수 있는 수학적 대상·비형식 풀이도 검토하고, 같은 모형을 쓸 때와 쓰지 않을 때 설명이 맞는지 관찰할 질문을 만든다. 적용할 반·목적·지원의 차이도 적는다.','이론적 관점을 자체 질문에 확장한다. 특정 모형을 모두의 필수 경로로 고정하거나 실제 학생 자료 없이 학습이 일어났다고 결론내리지 않는다.')]
INTERPRETATIONS={}
for rid in ['SEC_12수과03-01_C04','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'SLD17-01']=('activity_context','목표·과제·예상 사고의 계획과 실제 설명/다른 풀이를 대조해 다음 활동과 경로를 수정하는 맥락에 참고한다.','예상 경로를 실제 학생의 고정 선수 사슬·같은 풀이/기간의 의무로 바꾸지 않는다. 계획과 실제 수행 근거를 나눈다.')
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1']:
 INTERPRETATIONS[rid,'SLD17-02']=('activity_context','읽은 문헌·가져와 바꾼 활동·자료 생성 맥락·실제 수행을 연결하며 제공 자료와 직접 수집 자료를 구분한다.','참고 목록·그림 확인을 원논문/원자료 독해나 실제 학생 수집으로 세지 않는다. 저자 사례와 자체 적용은 다른 근거다.')
for rid in ['SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'SLD17-03']=('inference_limit','전체 기록·반박·수정·경쟁 설명을 대조하고 실제 시행 버전과 재구성한 버전을 구분해 성찰한다.','선택 장면을 전체 학습으로 일반화하거나v1결과를 미시행v2전체의 직접 효과로 바꾸지 않는다. 근거 추적은 외부 검토의 수행과 다르다.')
INTERPRETATIONS['SEC_9수04-08_C04','SLD17-04']=('inference_limit','중심·퍼짐·사분 요약을 함께 비교하고 상자그림이 내부 값·분포 일부를 잃는다는 자체 반례를 대조한다.','원문 단봉 가정·도식에서 유일한 밀도/봉우리·정규성을 복원하지 않는다. 자체 수치 예는 원자료·실제 학생 검증이 아니다.')
def main():
 registry=load_registry();known={c['id'] for c in registry['claims']};newids={c['id'] for c in CLAIMS}
 if newids<=known:
  assert registry['sources'][SOURCE]['snapshot_file']==NOTES;build_report();return
 assert not newids&known
 s=registry['sources'][SOURCE];assert s['snapshot_file']==PRIOR and s['snapshot_sha256']==PRIOR_SHA and s['bibliography_snapshot']==PRIOR_BIB
 assert sha(ROOT/PRIOR)==PRIOR_SHA and sha(CACHE/'slo-design-part-a-2013.pdf')==SHA
 acquisition=load(CACHE/'acquisition.json');assert acquisition['reading_completed'] and acquisition['images_viewed'] and acquisition['read_text_pages']==NEW_TEXT and acquisition['viewed_image_pages']==NEW_VISUAL
 old_source=copy.deepcopy(s);old_notes=load(ROOT/PRIOR);old_claims=[copy.deepcopy(c) for c in registry['claims'] if c['source_id']==SOURCE];assert len(old_claims)==14 and len(s['observations'])==24
 assert not set(NEW_TEXT)&set(old_notes['selected_text_pages']) and not set(NEW_VISUAL)&set(old_notes['visual_pdf_pages'])
 images={str(p):sha(CACHE/f'rendered/slo-design-part-a-2013-{p}.png') for p in NEW_VISUAL}
 assert not {o['id'] for o in OBSERVATIONS}&{o['id'] for src in registry['sources'].values() for o in src.get('observations',[])}
 relations=load(ROOT/'data/revised_relations.json')['relations'];pairs={(x['id'],c['id']) for x in relations for c in CLAIMS if all(x[k].startswith('standard:') for k in ['from','to']) and {x[k][9:] for k in ['from','to']}<=set(c['standard_codes'])};assert pairs==INTERPRETATIONS.keys() and len(pairs)==8
 reviewed=load(ROOT/FILE);old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in {c['id'] for c in old_claims}];assert len(old_rows)==17
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry);entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review=LIMITS)
 notes=copy.deepcopy(old_notes);notes.update(date=DATE,read_scope=SCOPE,selected_text_pages=sorted(old_notes['selected_text_pages']+NEW_TEXT),visual_pdf_pages=sorted(old_notes['visual_pdf_pages']+NEW_VISUAL),rendered_page_sha256={**old_notes['rendered_page_sha256'],**images},previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=copy.deepcopy(s['observations']),previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,reading_log=old_notes['reading_log']+['2026-11-17:3장 전체의 새 본문/참고문헌40쪽·판면42쪽을 실제 읽고 그림1–11과 표·각주를 대조했다. PDF73삽화·114머리말 전용 쪽은 추출문 독해에 넣지 않는다.'],learning_design_followup=dict(new_text_pages=NEW_TEXT,new_visual_pages=NEW_VISUAL,cumulative_text_pages=70,cumulative_visual_pages=73,chapter3_all_pdf_pages=NEW_VISUAL,chapter3_complete=True,chapter6_complete_with_prior_reading=True,all_part_a_read=False,part_b_read=False,cited_originals_read=False,earlier_2006_chapter_read=False,raw_data_reanalyzed=False,minitool_executed=False,author_reported_classroom_cases=True,local_student_validation=False,figure_rechecks=[95,98,100,101]),source_corrections=old_notes['source_corrections']+[dict(location='PDF73/114',issue='73은 교량 삽화,114는 머리말/쪽번호만 있는 마지막 쪽이다. 본문 추출문 독해 쪽에 합산하지 않는다.'),dict(location='PDF95/99/100 Figures6/9/10 and footnote4',issue='사분 요약에서 모양을 유일하게 복원하지 않는다. 단봉 가정은 각주/본문에 명시되어 있다.46/186 표본을 정수로 같은4집단으로 나누었다고 역산하지 않는다.'),dict(location='PDF84 Figure2 and PDF98 Figure7/dialogue',issue='그림7 축의 역슬래시+s와 다른 곳의hours 표기를 구별한다. seconds로 임의 전용하거나 그림에서 원자료의 정확한 수치를 재현하지 않는다. 정오표·작성 의도는 미확인이다.'),dict(location='PDF101–104 retrospective reconstruction',issue='재구성한 최종 경로와 실제 시행 경로가 달라 이전 사전/사후 결과가 새 경로 전체의 직접 검증은 아니다.')])
 write(ROOT/NOTES,notes)
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])]
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=history,bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,method_note='3장 전체·6장 기존 읽기·표/그림/각주와 저자 보고 수업 사례를 대조했다. 원자료 재분석·원논문·도구 실행·실제 국내 검증은 아니다.',editorial_action='새 주장8건·자체 과제10개를 더하고 기존14주장·24과제와17개 관계 해석의 이전 원장을 보존했다.',observations=s['observations']+copy.deepcopy(OBSERVATIONS),display={**s['display'],'title':TITLE})
 for claim in copy.deepcopy(CLAIMS):claim.update(empirical_scope=copy.deepcopy(s['empirical_scope']),target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in claim['standard_codes']});registry['claims'].append(claim)
 by_claim={c['id']:c for c in registry['claims']};by_relation={x['id']:x for x in relations}
 for row in reviewed['records']:
  if row['claim_id'] in {c['id'] for c in old_claims}:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 for (rid,cid),(role,finding,limit) in INTERPRETATIONS.items():reviewed['records'].append(dict(relation_id=rid,claim_id=cid,role=role,finding=finding,limit=limit,relation_snapshot=relation_snapshot(by_relation[rid]),claim_snapshot=claim_snapshot(by_claim[cid],s)))
 apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');row=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);row.update(source=entry,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE])
 write(ROOT/'data/sources.json',bibliography);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report();print('Extended same SLO source:8 claims,10 own tasks,8 relation entries;all prior claims/tasks preserved')
if __name__=='__main__':main()

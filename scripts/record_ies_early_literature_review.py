"""Selected early-math guide pages: scoped recommendations, not certified prerequisites."""
import copy,hashlib,json,shutil
from literature_review import ROOT,digest,target_value,load_registry,build_report
from relation_analysis_review import load_reviews

SOURCE='IES_EARLY_2013'
URL='https://ies.ed.gov/ncee/wwc/PracticeGuide/18'
PDF_URL='https://ies.ed.gov/ncee/WWC/Docs/PracticeGuide/early_math_pg_111313.pdf'
SHA='2cb8b9d2e406c72107c435bbbecf6a6f7101cb1e07cefb1fd8dd96f59aeb03bf'
PAGES=[2,4,10,13,17,18,19,20,22,23,24,25,26,29,31,32,33,34,36,37,38,39,40,42,43,44,45,46,71,72,75,76,96,97,107,108]
VISUAL=[17,25,32,34,46,96]
RATINGS={'1':'Moderate','2':'Minimal','3':'Minimal','4':'Minimal','5':'Minimal'}

MAPPINGS=[
('IE01',['2수01-01'],[1],['PDF18–20 / printed12–14','PDF22–26 / printed16–20','PDF75–76 / printed69–70'],
 '작은 수의 모임에서 일대일 대응·마지막 수와 전체 개수·재배치 뒤 개수를 구별해 관찰하는 자체 활동 설계에 참고한다.',
 '권고1은 Moderate이지만 특정 발달 경로의 직접 비교 근거는 없다고 명시한다. 가이드의 3–6세·작은 수 활동을 한국 초등 0~100 전체나 모든 학생의 유일한 필수 순서·현재 진단 정확도의 근거로 확대하지 않는다.'),
('IE02',['2수01-04','2수01-05'],[1],['PDF29 / printed23','PDF20 / printed14','PDF75–76 / printed69–70'],
 '보이는 집합과 가려진 집합의 합성·분해를 비교하고,전체·보이는 부분·가려진 부분과 추가·제거를 구별하는 자체 발문에 참고한다.',
 '기본 기능을 모두 끝낸 뒤에만 문제 해결을 시작해야 한다는 주장을 가이드가 요구하지 않는다. 다요소 수업의 결과를 가리기 활동 하나의 효과나 20 이하 전체·두 자리 계산의 검증으로 바꾸지 않는다.'),
('IE03',['2수03-03','2수03-05'],[2],['PDF31–34 / printed25–28','PDF96–97 / printed90–91'],
 '크기·색·방향이 다른 모양의 예·비예와 결합·분할을 비교해 유지되는 변·꼭짓점 등 특징을 설명하는 자체 설계에 참고한다.',
 '권고2는 Minimal이며 다요소 개입·비교 조건·측정 영역의 불일치로 특정 요소에 효과를 귀속하기 어렵다. 원문의 정사각형·직사각형 포함 관계를 한국 초등 초기 도형의 새 필수 수행으로 옮기지 않는다.'),
('IE04',['2수03-06','2수03-10'],[2],['PDF38–39 / printed32–33','PDF32–33 / printed26–27','PDF96–97 / printed90–91'],
 '직접 비교할 속성·기준 끝과 비표준 단위의 크기·반복 수를 구별하고,표준 단위와 도구의 역할을 설명하는 설계에 참고한다.',
 '권고2는 Minimal이다. 미국의 인치·피트·파운드를 현재 cm·m 과제의 단위로 복사하지 않으며 표준 단위 사용이 모든 측정 오차를 없앤다고 하지 않는다. 측정 연구 수의 본문·부록 불일치는 해결 전 수치 인용을 보류한다.'),
('IE05',['2수02-01','2수02-02'],[2],['PDF36–37 / printed30–31','PDF32–33 / printed26–27','PDF96–97 / printed90–91'],
 '반복 묶음을 명시해 이어 놓기·오류 고치기·자기 규칙 만들기·다른 재료로 표현하기를 구별하는 자체 설계에 참고한다.',
 '규칙 지도만의 인과 효과나 현재 생성 경로의 필수성은 입증하지 않는다. 유한 배열의 다음 항만으로 규칙이 유일하다고 하지 않으며,미리 정한 규칙과 관찰 뒤에 만든 설명을 구별한다.'),
('IE06',['2수04-01','2수04-02','2수04-03'],[2],['PDF39–40 / printed33–34','PDF32–33 / printed26–27','PDF96–97 / printed90–91'],
 '익숙한 대상의 분류 기준·범주별 수와 그림 표현을 연결하고,원기록을 한 번씩 보존해 같은 기호 단위로 비교하는 자체 설계에 참고한다.',
 '원문 즐겨 찾는 음식 활동은 수업 예시이며 현재 한국어 조사·그래프 발문의 효과나 측정 동등성을 검증한 자료가 아니다. 한 사람 한 응답·기호 한 개 한 기록이라는 자체 조건을 유지하고 다요소 개입의 전체 효과를 자료 활동만의 효과로 옮기지 않는다.'),
('IE07',['2수01-01','2수01-04'],[3],['PDF42–46 / printed36–40','PDF107–108 / printed101–102'],
 '최초 반응·수행 방법·주어진 도움·재관찰을 기록해 다음 활동의 수량·자료·질문을 조정하는 관찰 절차의 설계에 참고한다.',
 '권고3은 Minimal이며 관찰·평가 요소의 고유 효과를 다른 수업 요소와 분리하지 못했다. 원문의 예시 체크리스트나 현재 기록 양식을 표준화된 인지 단계 검사·현재 학생 자료·자체 수업 효과 검증으로 사용하지 않는다.')]

# The source's English wording is not copied as an assessment. These are local, unvalidated tasks.

OBSERVATIONS=[
 dict(id='IE-P1',standard_codes=['2수01-01'],
  question='같은 구슬 5개를 하나씩 옮기며 세고 모두 몇 개인지 말하라. 구슬을 더하거나 빼지 않고 넓게 펼친 뒤 개수가 같은지 설명하고 확인하라.',
  expected='각 구슬을 한 번씩 세면 모두 5개다. 마지막에 말한 5는 마지막 구슬만의 이름이 아니라 전체 개수다. 늘리거나 줄이지 않아 넓게 펼쳐도 같은 다섯 구슬이며,다시 세어 확인하는 방법도 가능하다.',
  interpretation='수 이름·가리키기·중복·누락·전체 개수·배열 변화의 설명을 따로 기록한다. 다시 세었다는 이유만으로 개념 결손을 단정하지 않고 처음 반응과 힌트 뒤 반응을 구별한다. 유아 가이드의 참고 활동이며 0~100 전체나 고정된 발달 단계를 검증하지 않는다.',student_validated=False),
 dict(id='IE-P2',standard_codes=['2수01-04','2수01-05'],
  question='처음에 구슬 5개를 함께 확인했다. 2개만 보이게 두고 나머지를 가렸다. 가린 구슬은 몇 개인가? 가린 쪽의 1개를 보이는 쪽으로 옮기면 두 부분과 전체는 어떻게 바뀌는가?',
  expected='처음 가린 부분은 3개다. 1개를 옮기면 보이는 부분은 3개·가린 부분은 2개이고 전체는 여전히 5개다. 가린 부분의 개수와 전체 개수를 구별하며 다시 합쳐 확인할 수 있다.',
  interpretation='처음 전체를 기억했는지·보이는 부분을 셌는지·부분의 보상 관계를 설명하는지 구별한다. 전체 5를 다시 알려주었으면 도움으로 기록한다. 가리기 성공·실패를 일반 계산 능력이나 모든 연산의 필수 단계로 판정하지 않는다.',student_validated=False),
 dict(id='IE-P3',standard_codes=['2수03-03','2수03-05'],
  question='같은 종이 삼각형을 돌리고 뒤집었다. 여전히 같은 종류의 모양인가? 테두리를 따라 곧은 변과 꼭짓점을 세어 설명하라. 곧은 선분 세 개가 닫히지 않고 벌어져 있어도 삼각형인가?',
  expected='돌리거나 뒤집어도 곧은 변 3개·꼭짓점 3개로 닫힌 삼각형이다. 벌어진 세 선분은 닫힌 모양이 아니라 같은 삼각형으로 분류하지 않는다. 위쪽에 뾰족한 점이 있는지는 고정된 공통 특징이 아니다.',
  interpretation='방향·색·크기 같은 외형과 유지되는 경계의 특징을 구별한다. 엄밀한 정의 암기나 사각형의 포함 관계를 요구하지 않고 실제 어떤 경계를 셌는지 관찰한다. 현재 학생 반응이나 언어 동등성은 검증하지 않았다.',student_validated=False),
 dict(id='IE-P4',standard_codes=['2수03-06','2수03-10'],
  question='막대 A를 길이 2cm인 조각 6개로,B를 길이 3cm인 조각 4개로 빈틈·겹침 없이 덮었다. 조각 수가 6>4라 A가 더 긴가? 한쪽 끝을 맞추어 비교하고 이유를 말하라.',
  expected='두 길이는 각각 12cm로 같다. 단위 조각의 크기가 달라 조각 수만 비교하면 안 된다. 실물을 끝 맞춰 비교하거나 같은 단위 조각으로 다시 덮어 같은 길이임을 설명할 수 있다.',
  interpretation='곱셈식 암기 대신 직접 비교·같은 단위·빈틈과 겹침·단위 크기와 반복 수의 관계를 관찰한다. cm 수치는 한국어 자체 예의 조건이며 미국 가이드의 단위를 복사한 것이 아니다. 표준 단위여도 놓기·눈금 읽기 오차가 없어지는 것은 아니다.',student_validated=False),
 dict(id='IE-P5',standard_codes=['2수02-01','2수02-02'],
  question='빨강·빨강·파랑 세 개를 한 묶음으로 반복하기로 했다. 두 묶음 뒤에 이어질 세 개를 놓아라. 둘째 묶음의 두 번째를 파랑으로 놓았다면 어떻게 고치는가? 같은 규칙을 박수·발구르기로 바꾸어 보라.',
  expected='다음 세 개도 빨강·빨강·파랑이다. 잘못 둔 둘째 묶음 두 번째는 빨강으로 고친다. 빨강을 박수,파랑을 발구르기에 대응하면 박수·박수·발구르기 묶음이 반복된다.',
  interpretation='반복 묶음·시작 위치·재료 대응·오류 위치·자기 설명을 따로 기록한다. 이 과제는 세 개짜리 규칙을 미리 정했으며,규칙이 없는 유한 배열에서 유일한 다음 항을 확정하는 활동과 구별한다. 한 번의 이어 놓기를 모든 규칙의 숙달로 판정하지 않는다.',student_validated=False),
 dict(id='IE-P6',standard_codes=['2수04-01','2수04-02','2수04-03'],
  question='가상 카드 5장에 한 사람당 좋아하는 과일 한 가지가 사과·사과·바나나·사과·바나나로 적혀 있다. 분류해 표와 기호 하나=카드 한 장인 그래프로 옮겨라. 같은 카드를 두 범주에 넣어도 되는가?',
  expected='사과 3장·바나나 2장이고 합은 5장이다. 그래프도 같은 단위 기호를 각각 3개·2개로 시작선을 맞춰 놓는다. 현재 한 응답 조건에서 같은 카드를 중복해 넣으면 원자료 한 번씩 보존이 깨진다.',
  interpretation='가상 카드임을 표시하고 분류 기준·원기록·범주별 수·기호 단위를 추적한다. 실제 학생 선호를 조사한 결과가 아니다. 무응답·복수응답이 있으면 원래 조건과 다름을 기록하고 규칙을 정한 뒤 다시 세며 사람 수를 임의로 맞추지 않는다.',student_validated=False)]

def verify():
 assert len(PAGES)==36 and len(set(PAGES))==36 and set(VISUAL)<=set(PAGES)
 original=[1,2,3,4,5];rearranged=[3,5,1,4,2]
 assert len(set(original))==len(set(rearranged))==5 and set(original)==set(rearranged)
 assert 2+3==3+2==5 and 3-1==2 and 2+1==3
 triangle=[(0,0),(3,0),(1,2)];rotated=[(-y,x) for x,y in triangle]
 area2=lambda p:sum(p[i][0]*p[(i+1)%3][1]-p[(i+1)%3][0]*p[i][1] for i in range(3))
 assert len(triangle)==len(rotated)==3 and abs(area2(triangle))==abs(area2(rotated))==6
 assert 2*6==3*4==12
 unit=['R','R','B'];sequence=unit*3;assert sequence[6:9]==unit and sequence[4]=='R'
 bad=unit+['R','B','B'];bad[4]='R';assert bad==unit*2
 cards=['apple','apple','banana','apple','banana'];assert cards.count('apple')==3 and cards.count('banana')==2 and len(cards)==5

def main():
 verify();registry=load_registry();before_relations=set(load_reviews()['records'])
 if SOURCE in registry['sources']:
  print('Selected early-math guide and targets remain current; no automatic refresh');build_report();return
 assert not {v[0] for v in MAPPINGS}&{v['id'] for v in registry['claims']}
 raw=ROOT/'tmp/literature/ies-early-2013.pdf';assert hashlib.sha256(raw.read_bytes()).hexdigest()==SHA
 snapshot='data/literature_evidence/IES_EARLY_2013.pdf';destination=ROOT/snapshot
 if destination.exists():assert hashlib.sha256(destination.read_bytes()).hexdigest()==SHA
 else:shutil.copyfile(raw,destination)
 path=ROOT/'data/sources.json';sources=json.loads(path.read_text(encoding='utf-8'));b=next(v for v in sources if v['id']==SOURCE);previous=copy.deepcopy(b)
 b.update(review_scope='2013년 가이드165쪽 중 명시한36쪽 텍스트·6쪽 이미지와 미주78/252를 확인. 대상3–6세·권고별 등급·선정 교수 예·근거 부록을 대응. 전권·원연구 전체 대조가 아님.',next_review='미검토 본문·연구표·원연구·당시 프로토콜과 실제 학생 반응은 후속 대조. 측정 연구 수 본문9/부록10 불일치는 구성 연구·정오표 확인 전 수치 인용 보류. 유아 연구를 한국 초등 전체·필수 선수 순서로 일반화하지 않음.')
 registry['sources'][SOURCE]=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-05',snapshot_kind='source_pdf',snapshot_file=snapshot,snapshot_sha256=SHA,
  redistribution_license='Public domain (explicit report declaration)',license_location='PDF4 / publication information',license_statement='This report is in the public domain.',bibliography_snapshot=digest(b),previous_bibliography=previous,
  display=dict(title=b['title'],url=URL,authors_year='Frye 외, IES/WWC 2013'),source_pdf_url=PDF_URL,pdf_pages_total=165,text_pdf_pages=PAGES,visual_pdf_pages=VISUAL,
  read_scope='선정36쪽 텍스트·6쪽 이미지와 미주78/252만 확인. 전체165쪽·모든 원연구 정독이 아님.',
  intended_learner_scope=dict(ages=[3,6],schooling=['preschool','prekindergarten','kindergarten'],korean_elementary_full_scope_established=False),direct_particular_progression_comparison_established=False,
  reading_log=['text_pdf_pages에 명시한 36쪽을 실제 읽고 표2·세기 오류 표4·도형 분할 그림4·관찰 체크리스트와 본문/부록 수치의 6쪽 이미지를 대조했다.',
   '권고1의 Moderate,권고2–5의 Minimal을 확인했다. 현재 주장 대응은 권고1–3의 읽은 대목에 한정하며 권고4–5 본문 전체를 검토한 것으로 표시하지 않는다.',
   'PDF20/75–76과32/96은 특정 발달 경로와 다른 순서를 직접 비교하지 못했다는 한계를 밝힌다. 다요소 수업과 비교 처치·결과 영역·권고별 재인용을 구별했다.',
   'PDF32와96의 측정 연구 수9/10을 이미지로 확인했다. PDF142 미주78과 PDF151 미주252의 해당 개입 목록만 추가로 읽었고,그 목록의 같음만으로 연구 수 차이가 해결되었다고 하지 않는다.',
   'PDF42–46/107–108의 관찰·조정·재평가를 자체 기록 절차에 참고했다. 원문 예시의 아동 이름·체크리스트는 현재의 실제 학생 반응이나 표준화된 검사 결과로 옮기지 않았다.'],
  additional_read_sections=['PDF142 / endnote78 only','PDF151 / endnote252 only'],evidence_ratings=RATINGS,search_period='1989–2011 initial search plus panel-recommended supplements as described in Appendix D',
  scope_note='가이드의 의도된 대상은3–6세의 preschool·prekindergarten·kindergarten이다. 권고1은 Moderate,2–5는 Minimal이며 한국 초등 전체의 효과 등급이 아니다. 특정 발달 경로를 유일한 필수 순서로 직접 입증한 연구가 없다는 한계를 유지한다.',
  method_note='선정 근거 부록은 검색·WWC 검토·다요소 개입과 비교 처치의 차이,결과 영역의 맞음 여부를 구분한다. 같은 연구가 여러 권고에 기여할 수 있어 독립 표본으로 합산하지 않는다. 수·연산 전체 권고의 등급을 숨기기·그림·규칙·관찰 요소 하나의 고유 효과로 옮기지 않는다.',
  limits='전체165쪽·연구표 전체·개별 원논문·원자료·당시 프로토콜은 미검토다. 한국 초등의 수 범위·미터법·도형 범위와3–6세 가이드를 구별한다. 현재 발문의 진단 정확도·번역 동등성·인지 단계·학생 효과·특정 선수 방향을 입증하지 않는다. 측정 연구 수9/10은 해결 전 숫자 인용을 보류한다.',
  source_discrepancies=[dict(locations=['PDF32 / printed26','PDF96 / printed90','PDF142 endnote78','PDF151 endnote252'],issue='7개 측정 개입을 평가한 연구 수가 본문9편·부록10편으로 다름',status='unresolved_count_not_used',followup='TableD5의 구성 연구·미주·원연구·정오표를 추가 대조하기 전 어느 숫자도 확정 인용하지 않는다. 동일 개입 목록은 연구 수의 차이를 해소하는 증거가 아니다.')],
  editorial_action='현재12개 기준에 권고별 주장7건과 자체 관찰6건을 대응했다. 조건·기대 설명·도움 전후 기록과 한계를 더했으며 기존 대표 원고·과제·관계 검토 근거는 바꾸지 않았다. 신규 관계 검토·독립 검토·학생 검증으로 합산하지 않았다.',independent_review=False,student_validated=False,observations=OBSERVATIONS)
 for cid,codes,recs,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='instructional_recommendation_with_evidence_scope',locations=locations,support=support,does_not_establish=limit,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},standard_codes=codes,independent_review=False,student_validated=False,local_effect_tested=False,recommendations=[dict(number=n,evidence_rating=RATINGS[str(n)],application_limit=limit) for n in recs]))
 path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 path=ROOT/'data/content_review_queue.json';q=json.loads(path.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[v[0] for v in MAPPINGS]);path.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert set(load_reviews()['records'])==before_relations
 build_report();print('Added early-math guide: 7 scoped claims and 6 own observations; no relation approvals')

if __name__=='__main__':main()

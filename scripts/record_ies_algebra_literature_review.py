"""Bind selected pages of the January 2019 revised algebra guide to scoped claims."""
import copy,hashlib,json,shutil
from fractions import Fraction as F
from literature_review import ROOT,digest,target_value,load_registry,build_report

SOURCE='IES_ALGEBRA_2015'
URL='https://ies.ed.gov/ncee/wwc/practiceguide/20'
PDF_URL='https://ies.ed.gov/ncee/WWC/Docs/PracticeGuide/WWC_Algebra_PG_Revised_02022018.pdf'
SHA='83f6f973eb79caa2170f2818034d533322258708d38a777620862b95a9cbc730'
PAGES=list(range(1,12))+[15,16,22,23,24,26,27,32,33,35,36,37,52,53,54,56,57,59,60,64,70]
RATINGS={'1':'Minimal','2':'Minimal','3':'Moderate'}

# id, bound authored targets, associated standards, recommendations, actual locations, support, limit
MAPPINGS=[
('IA01',['revision:9수02-03'],['9수02-03'],[1],['PDF11 / printed5','PDF15–16 / printed9–10','PDF53–54 / printed47–48'],
 '정답·오답 풀이를 명확히 표시하고 최초로 해 보존이 깨지는 단계·그 이유·원식 대입을 설명하도록 하는 자체 설계에 참고한다.',
 '권고1은 Minimal이다. 비교 처치·짧은 개입·일반화 한계가 있으며 현재 가역 변형 진단의 정확도나 특정 오류의 원인·학생 효과를 입증하지 않는다.'),
('IA02',['revision:9수02-02'],['9수02-02'],[2],['PDF22–24 / printed16–18','PDF56–57 / printed50–51'],
 '괄호 전체의 분배·동류항·식 다시 쓰기를 연산 구조와 정확한 언어로 설명하는 설계에 참고한다.',
 '권고2는 Minimal이며 정확한 수학 언어 요소 자체를 직접 평가한 적격 연구가 없다고 가이드가 명시한다. 언어 표현을 바꾼 것만으로 이 과제의 학습 효과가 실증되었다고 하지 않는다.'),
('IA03',['revision:9수02-22','revision:10공수1-02-04'],['9수02-22','10공수1-02-04'],[2],['PDF26–27 / printed20–21','PDF56–57 / printed50–51'],
 '동치인 전개형·인수분해형·완전제곱형이 같은 함수를 표현하면서 영점·축·꼭짓점 정보를 다르게 드러냄을 비교하는 설계에 참고한다.',
 '미국 6–12학년의 가이드와 한국 과목 범위를 구별한다. 원문 말굽의 수치·피트 단위를 현재 과제에 복사하지 않으며 중학교 제한 구간 최적화를 새로 요구하지 않는다. 권고2의 등급은 Minimal이다.'),
('IA04',['revision:9수02-04'],['9수02-04'],[3],['PDF9 / printed3','PDF32–33 / printed26–27','PDF35–36 / printed29–30','PDF59–60 / printed53–54'],
 '학생이 알고 있는 전략에서 출발해 같은 방정식의 다른 경로·첫 연산의 적절성·선택 이유를 비교하는 설계에 참고한다.',
 '권고3은 Moderate이지만 근거는 특히 절차적 유연성에 집중되며 개념·절차 지식의 결과는 덜 일관된다. 대수 사전 지식이 거의 없는 집단의 부정·혼재 결과도 있어 모든 전략의 동시 숙달이나 현재 과제 효과로 일반화하지 않는다.'),
('IA05',['revision:9수02-13'],['9수02-13'],[1,3],['PDF15 / printed9','PDF35–36 / printed29–30','PDF53–54 / printed47–48','PDF59–60 / printed53–54'],
 '연립식 풀이에서 대입·가감의 같은 동시 조건을 유지하고,두 경로를 비교하거나 오답의 첫 잘못된 연산을 설명하도록 하는 설계에 참고한다.',
 '풀이 사례 분석은 Minimal,전략 선택은 Moderate의 서로 다른 권고다. 두 등급을 더하거나 같은 연구를 독립 표본으로 중복 집계하지 않는다. 현재 장수 모형·학생 응답·필수 경로의 효과를 검증한 기록이 아니다.'),
('IA06',['revision:9수02-19','revision:10공수1-01-03'],['9수02-19','10공수1-01-03'],[1,2],['PDF16 / printed10 Example1.6','PDF24 / printed18','PDF53–54 / printed47–48','PDF56 / printed50'],
 '인수분해의 올바른 예·잘못된 예를 구별해 전개로 모든 항과 계수를 복원하고,값 하나의 검산과 항등적 설명을 구별하는 설계에 참고한다.',
 '두 관련 권고 모두 Minimal이다. 원문 예시의 정오 표시는 학습 자료이며 현재 인수분해 과제나 오류 분류의 타당성을 입증한 학생 자료가 아니다. 공통수학 공식을 중학교의 추가 필수 내용으로 소급하지 않는다.')]

OBSERVATIONS=[
 dict(id='IA-P1',standard_codes=['9수02-03','9수02-20'],
  question='다음은 검토할 잘못된 풀이다: x(x−1)=0에서 양변을 x로 나누어 x=1만 얻었다. 처음 추가한 조건과 빠진 해를 설명하고 원식으로 확인하라.',
  expected='x로 나누려면 x≠0이 필요하다. 원식에서는 x=0 또는 x=1이므로 나눗셈에서 0을 잃었다. 두 값을 원식에 대입하면 모두 0이다.',
  interpretation='오답 예임을 먼저 명시하고 단계·조건·대입 검산을 따로 관찰한다. 한 반응으로 학생의 일반 능력이나 오류 원인을 확정하지 않는다. 원문의 교수 권고를 재구성한 자체 발문이며 현재 학생 검증은 없다.',student_validated=False),
 dict(id='IA-P2',standard_codes=['9수02-01','9수02-03','9수02-04'],
  question='2(x+1)+8=14와 2(3x+4)+8=14에서 괄호 전체가 맡는 같은 역할을 설명하라. 구조가 같으니 x의 해도 같은가?',
  expected='두 식은 모두 괄호 전체를 u로 두면 2u+8=14여서 u=3이다. 첫 식은 x+1=3에서 x=2,둘째는 3x+4=3에서 x=−1/3이다. 같은 바깥 연산 구조가 같은 x해를 뜻하지 않는다.',
  interpretation='문자·부분식·전체 식의 역할과 수치 해를 분리해 기록한다. 정확한 언어를 쓰게 하는 설계는 권고2의 참고이며 그 언어 요소만의 인과 효과나 출발 기준 전체의 숙달을 입증하지 않는다.',student_validated=False),
 dict(id='IA-P3',standard_codes=['9수02-19','9수02-22','10공수1-02-04'],
  question='실수 전체에서 x²−4x+3,(x−1)(x−3),(x−2)²−1을 비교하라. 서로 같은지 설명하고 영점·축·꼭짓점·최솟값을 가장 쉽게 읽는 표현을 골라 이유를 말하라.',
  expected='전개하면 세 식은 같다. 인수분해형은 영점 1·3을,완전제곱형은 축 x=2·꼭짓점 (2,−1)·최솟값 −1을 드러낸다. 표현을 고르는 이유가 다르며 x=2는 영점이 아니다.',
  interpretation='같은 함수의 동치와 표현별 정보의 차이를 관찰한다. 정의역은 실수 전체로 명시하고 중학교에 제한 구간 최적화를 추가하지 않는다. 원문의 말굽 모형·값·단위와 다른 자체 예이며 도구 실행·학생 효과를 새로 검증하지 않았다.',student_validated=False),
 dict(id='IA-P4',standard_codes=['9수02-04'],
  question='4(x+2)=20을 먼저 전개하는 방법과 먼저 4로 나누는 방법으로 풀어라. 각 첫 단계의 근거와 이 문제에서의 편리함을 설명하라. 모든 문제에 같은 전략이 가장 좋은가?',
  expected='전개하면 4x+8=20→4x=12→x=3이다. 먼저 나누면 x+2=5→x=3으로 단계가 짧다. 양변을 같은 0 아닌 4로 나누므로 해가 보존된다. 다른 식의 구조·조건에서는 다른 전략이 더 적합할 수 있다.',
  interpretation='학생이 이미 이해한 전략에서 한두 경로를 비교하고 선택 이유를 묻는다. 권고3은 모든 가능한 전략의 숙달을 요구하지 않으며 사전 지식·문제·비교 처치에 따른 한계를 갖는다. 수행 성공을 현재 활동 효과나 필수 선수성으로 승격하지 않는다.',student_validated=False)]

def verify():
 assert len(PAGES)==32 and len(set(PAGES))==32
 assert {x for x in range(-3,4) if x*(x-1)==0}=={0,1}
 assert 2*(2+1)+8==14 and 2*(3*F(-1,3)+4)+8==14
 for x in range(-9,10):
  assert x*x-4*x+3==(x-1)*(x-3)==(x-2)**2-1
  assert x*x-10*x-24==(x-12)*(x+2)
  assert (x-4)*(x+6)==x*x+2*x-24
 assert 4*(3+2)==20
 # The visually checked horseshoe example uses feet, unlike our own quadratic.
 h=lambda t:F(19,16)+18*t-16*t*t
 for t in [F(0),F(1,4),F(9,16),F(19,16)]:
  assert h(t)==-16*(t-F(19,16))*(t+F(1,16))==-16*(t-F(9,16))**2+F(100,16)
 assert h(F(9,16))==F(100,16)

def main():
 verify();registry=load_registry()
 if SOURCE in registry['sources']:
  print('Selected revised algebra guide and targets remain current; no automatic refresh');build_report();return
 raw=ROOT/'tmp/literature/ies-algebra-2019.pdf';assert hashlib.sha256(raw.read_bytes()).hexdigest()==SHA
 snapshot='data/literature_evidence/IES_ALGEBRA_2015.pdf';shutil.copyfile(raw,ROOT/snapshot)
 path=ROOT/'data/sources.json';sources=json.loads(path.read_text(encoding='utf-8'));b=next(v for v in sources if v['id']==SOURCE);previous=copy.deepcopy(b)
 b.update(reviewed_edition='January 2019 revised PDF; original release April 2015',review_scope='공식 안내와 2019년 1월 개정 PDF 71쪽 중 명시한 32쪽 텍스트 및 표1·예1.6/2.7/3.5의 4쪽 이미지. 권고별 근거 요약·부록의 선정 대목·개정 주석 대조. 전체 71쪽·모든 원연구를 읽은 것은 아님.',next_review='미검토 본문·연구표의 나머지 행·당시 프로토콜·모든 개별 원논문과 실제 학생 반응은 후속 대조. 현행 WWC 기준·한국 학년·현재 과제 효과로 자동 전용하지 않음.')
 registry['sources'][SOURCE]=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-05',snapshot_kind='source_pdf',snapshot_file=snapshot,snapshot_sha256=SHA,
  redistribution_license='Public domain (explicit report declaration)',license_location='PDF4 / publication information',license_statement='This report is in the public domain.',bibliography_snapshot=digest(b),previous_bibliography=previous,
  display=dict(title=b['title'],url=URL,authors_year='Star 외, IES/WWC 2015; 2019년 1월 개정판 확인'),source_pdf_url=PDF_URL,reviewed_revision='2019-01',pdf_pages_total=71,text_pdf_pages=PAGES,visual_pdf_pages=[9,16,27,37],
  read_scope='선정 32쪽 텍스트와 4쪽 이미지 및 공식 안내. 전체 71쪽 정독·원연구 전체 대조가 아님.',
  reading_log=['공식 페이지의 2015년 발행·2019년 1월 개정과 PDF3–4의 판본 표기를 대조했다. 파일명의 2018을 발행·개정연도로 대신하지 않았다.',
   'text_pdf_pages에 나열한 32쪽을 실제 읽었다. 표1·인수분해 정오 예·동치 포물선·이차방정식 전략 표는 PDF9/16/27/37 이미지도 확인했다.',
   '권고1·2·3의 본문 근거 요약과 부록 D의 PDF52–54,56–57,59–60,64를 읽었다. D2·D3 첫 페이지의 행과 D4 뒤 주석은 읽었지만 연구표 전체·원연구 전체를 읽은 것은 아니다.',
   'PDF70은 2018년 1월31일의 Ives·Rittle-Johnson and Star·Mevarech 관련 효과크기·유의성 표시 정정을 기록한다. 2019년 개정 표기가 2019년까지의 새 문헌 검색을 뜻한다고 하지 않는다.'],
  evidence_ratings=RATINGS,search_period='1993–2013; guide search and panel supplements as described in Appendix D',
  scope_note='권고1·2는 Minimal,권고3은 Moderate다. 권고3의 근거는 특히 절차적 유연성에 집중되며 모든 전략의 숙달을 요구하지 않는다. 원문 6–12학년 범위·개정판과 현재 한국 과목·자체 과제를 구별한다.',
  method_note='가이드는 1993–2013년 검색과 패널 보완,WWC 심사를 설명한다. 권고1의 비교 처치·짧은 개입과 일반화 한계,권고2의 정확한 언어 요소 직접 근거 부재,권고3의 사전 대수 지식에 따른 부정·혼재 결과를 대조했다. 개념·절차·유연성 측정이 경험적으로 완전히 독립이라고 가정하지 않는다.',
  limits='모든 71쪽·프로토콜·개별 원연구·원자료를 검토하지 않았다. 권고 등급은 현재 과제의 효과·진단 정확도·필수 선수 경로의 등급이 아니다. 같은 연구의 권고별 재인용을 독립 표본으로 합산하지 않는다. 모든 학생의 사전 지식·한국 교육과정 범위에 동일하게 적용된다고 확정하지 않는다.',
  editorial_action='현재 원고 8개 기준에 6건의 권고별 주장 대응,자체 발문 4건에 조건·기대 설명·적용 한계를 추가했다. 기존 원고·과제·관계 검토의 근거 해시는 바꾸지 않고 독립·학생 검증으로 승격하지 않았다.',independent_review=False,student_validated=False,observations=OBSERVATIONS)
 for cid,targets,codes,recs,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='instructional_recommendation_with_evidence_scope',locations=locations,support=support,does_not_establish=limit,target_snapshots={target:digest(target_value(target)) for target in targets},standard_codes=codes,independent_review=False,student_validated=False,local_effect_tested=False,recommendations=[dict(number=n,evidence_rating=RATINGS[str(n)],application_limit=limit) for n in recs]))
 path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 path=ROOT/'data/content_review_queue.json';q=json.loads(path.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[v[0] for v in MAPPINGS]);path.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 from relation_analysis_review import load_reviews
 assert len(load_reviews()['records'])==673
 build_report();print('Added algebra guide: 6 scoped claims and 4 own observations; no relation approvals')

if __name__=='__main__':main()

"""Record the actually read 2010 guide; retain recommendation-level evidence limits."""
import hashlib,json,shutil
from literature_review import ROOT,digest,target_value,load_registry,build_report
SOURCE='IES_FRACTIONS_2010'
URL='https://ies.ed.gov/ncee/WWC/PracticeGuide/15'
PDF_URL='https://ies.ed.gov/ncee/WWC/Docs/PracticeGuide/fractions_pg_093010.pdf'
SHA='ed94a5ee4127a32240fd0114d2afc025c15ba8233014da3c07601157b770c252'
PROTOCOL_SHA='6e68bc533fee2fa0f02c5327a7a02f9e2c122907afc93dbf30926aa7c804891e'
RATINGS={'1':'Minimal','2':'Moderate','3':'Moderate','4':'Minimal','5':'Minimal'}
MAPPINGS=[
 ('IF01','family:fraction',['4수01-09','4수01-10','4수01-11','6수01-06','6수01-07'],[2],['PDF25–31 / printed19–25','AppendixD PDF62–65'],
  '분수를 수로 다루며 수직선에서 기준 단위·등간격·동치 위치를 확인하는 활동의 교수 설계 근거다.',
  '근거의 상당 부분은 자연수·소수 연구다. 현재 분수 과제의 효과나 모든 학생에게 필요한 단일 선수 경로를 입증하지 않는다. 미국K–8의 음수 분수·조밀성을 한국 초등 필수 내용으로 옮기지 않는다.'),
 ('IF02','family:fracop',['6수01-08','6수01-09','6수01-11'],[3],['PDF32–40 / printed26–34','AppendixD PDF66–68'],
  '계산 절차의 이유를 표현·어림·단위와 연결하고 개념·절차 활동을 오가며 설명하도록 하는 설계에 참고한다.',
  '근거에는 소수 중심의 단기·소표본 연구와 여러 요소를 함께 적용한 수업이 있다. 모든 분수 연산의 효과나 개념을 전부 끝낸 뒤 절차를 시작해야 한다는 순서를 확정하지 않는다.'),
 ('IF03','family:ratio',['6수02-02','6수02-03','6수02-04','6수02-05'],[4],['PDF41–47 / printed35–41','AppendixD PDF68–70'],
  '단위 비율·비례표·배율 등 전략을 비교하고 비례 관계의 의미를 설명한 뒤 교차 곱 절차를 사용하는 설계에 참고한다.',
  '권고 전체의 근거는Minimal이다. 함께 증가하는 모든 양이 비례하는 것은 아니며 특정 전략의 모든 상황 전이나 현재 경로의 보편적 필수성을 입증하지 않는다.'),
 ('IF04','pilot:fraction-10',['6수01-10'],[3],['PDF32–40 / printed26–34','AppendixD PDF66–68'],
  '분수 곱셈에서 무엇의 몇 배인지 설명하고 답을 예상한 크기와 대조하는 과제 설계에 참고한다.',
  '현재4×3/4 과제의 수치·발문·경로는 원연구의 검증 대상과 다르다. 권고의Moderate를 이 과제의 효과 판정으로 옮기지 않는다.'),
 ('IF05','pilot:fraction-02',['4수01-09','6수01-10'],[1],['PDF18–24 / printed12–18','AppendixD PDF61–62'],
  '동등한 나눔과 비례 직관을 다양한 재료·수치로 살피며 조각 수와 실제 양을 구별하도록 하는 설계에 참고한다.',
  'Minimal은 중요하지 않다는 뜻이 아니라 인과 근거의 제약을 뜻한다. 물리적으로 자르는 경험이 모든 학생의 필수 선행 조건이라는 증거로 사용하지 않는다.'),
 ('IF06','family:decimal',['4수01-13','4수01-14','6수01-12','6수01-13','6수01-15'],[2,3],['PDF26 / printed20','PDF33 / printed27','AppendixD PDF64–67'],
  '소수의 자릿값·수직선 위치와 계산 절차의 의미를 연결하고 개념·절차 활동을 반복하는 설계에 참고한다.',
  '수직선을 양쪽 집단 모두 사용한 연구에서는 실제 비교가 질문·눈금 단서의 차이였다. 이를 수직선 사용 대 미사용의 인과 효과로 바꾸거나 모든 소수 연산·학습자에 일반화하지 않는다.')]

OBSERVATIONS=[
 dict(id='IF-P1',standard_codes=['4수01-10','6수01-06'],question='0, 1, 2, 3이 표시된 수직선에서0에서1까지를 기준 한 단위로 삼아3/4, 6/8, 7/4의 위치를 표시하라. 한 단위를4등분할 때 간격과 내부 눈금은 각각 몇 개인지 설명하라.',
  expected='3/4와6/8은0과1 사이의 같은 점이고7/4는1과2 사이에 있다. 한 단위의4등분 간격은4개, 양 끝을 제외한 내부 눈금은3개다. 수직선 전체0–3을 한 단위로 삼지 않는다.',
  interpretation='기준 단위 선택·간격 세기·동치 위치를 구별해 관찰한다. 눈금을 먼저 알려 준 뒤의 응답과 최초 반응을 분리한다. 원문의 권고와 현재 활동의 검증을 구별하며 한 번의 성공으로 단계나 필수 경로를 확정하지 않는다.',student_validated=False),
 dict(id='IF-P2',standard_codes=['6수01-08'],question='1/2+2/7을 정확히 계산하기 전에 합이3/4보다 큰지, 1보다 작은지 예상하고 이유를 설명하라. 그다음 정확히 계산하고(1+2)/(2+7)=3/9라는 풀이를 검토하라.',
  expected='1/4<2/7<1/2이므로3/4<1/2+2/7<1이다. 정확한 합은11/14이다.3/9=1/3은 첫째 양1/2보다도 작으므로 양수를 더한 결과일 수 없다.',
  interpretation='어림의 이유·공통 단위로 바꾸는 계산·결과 검토를 따로 기록한다. 어림에서 정확한 답을 요구하지 않는다. 오답만으로 단위 개념의 결손을 확정하지 않고 계산 착오·발문 해석도 확인한다.',student_validated=False),
 dict(id='IF-P3',standard_codes=['6수01-08','6수01-09'],question='원래 오렌지 한 개의 양을A라 하고 현재3/4 A를 갖고 있다. 첫 경우에는 원래A의1/3을 주고, 둘째 경우에는 현재 가진3/4 A의1/3을 준다. 각 경우에 남은 양을A를 기준으로 나타내고 두 발문의 차이를 설명하라.',
  expected='첫 경우 남은 양은(3/4−1/3)A=5/12 A다. 둘째 경우 주는 양은(1/3×3/4)A=1/4 A이므로 남는 양은1/2 A다.1/3의 기준이 원래 전체인지 현재 가진 양인지 다르다.',
  interpretation='원문PDF38의of it 표현은 기준을 달리 읽을 여지가 있어 자체 발문에서는 두 기준을 명시했다. 원문을 확정적인 계산 오류로 분류하지 않는다. 기준을 알려 주기 전후의 응답을 구별하고 식·설명·양을 함께 확인한다.',student_validated=False),
 dict(id='IF-P4',standard_codes=['6수02-03','6수02-04'],question='다음은 실제 요금이 아닌 가상 상황이다. 같은 병의 단가가 일정하고 다른 비용이 없을 때3병4500원이면5병은 얼마인가? 또 배달료가 기본2000원에1km마다500원씩 붙으면2km와4km의 요금은 얼마인가? 어느 상황에서 양이2배이면 금액도2배인지 설명하라.',
  expected='병당1500원이므로5병은7500원이고 병 수와 금액이 비례한다. 배달료는2km3000원,4km4000원으로 거리가2배여도 요금은2배가 아니다. 함께 증가한다는 사실만으로 일정한 비율이라고 판단할 수 없다.',
  interpretation='단위 비율이 일정한 조건과 기본 비용이 있는 조건을 구별한다. 비례인지 판단하기 전에 교차 곱을 적용하지 않도록 이유를 묻는다. 한국 초등 기준을 넘어 형식적 함수식을 요구하지 않으며 이 가상 계산을 실제 가격 정보로 사용하지 않는다.',student_validated=False)]

def main():
 registry=load_registry()
 if SOURCE in registry['sources']:
  print('Reviewed source and targets remain current; no automatic refresh');build_report();return
 raw=ROOT/'tmp/literature/ies-fractions-2010.pdf'
 assert hashlib.sha256(raw.read_bytes()).hexdigest()==SHA
 assert hashlib.sha256((ROOT/'tmp/literature/ies-fractions-review-protocol-2010.pdf').read_bytes()).hexdigest()==PROTOCOL_SHA
 snapshot='data/literature_evidence/IES_FRACTIONS_2010.pdf';shutil.copyfile(raw,ROOT/snapshot)
 sp=ROOT/'data/sources.json';sources=json.loads(sp.read_text(encoding='utf-8'));b=next(s for s in sources if s['id']==SOURCE);previous=dict(b)
 b['review_scope']='公式 안내·2010 실천 가이드90쪽 전체 텍스트, 그림1–10·예1–5·표2/D1/D2/E1 및 주요 수식·재배포 문구의 실제 이미지23쪽, 당시 검토 프로토콜8쪽 전체 텍스트와 탈락률 곡선 이미지 확인.'.replace('公式','공식')
 b['next_review']='권고 근거의 모든 개별 원연구는 별도 대조 대상.26명 연구 효과크기의 본문2.38/표D2 2.83 불일치는 원논문·정오표 확인 전 보류. 자체 활동 효과·한국 학년별 적합성·현행WWC기준 검증으로 전용하지 않음.'
 source=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-04',snapshot_kind='source_pdf',snapshot_file=snapshot,snapshot_sha256=SHA,
  redistribution_license='Public domain (explicit report declaration)',license_location='PDF4 / printed ii',license_statement='This report is in the public domain.',bibliography_snapshot=digest(b),previous_bibliography=previous,
  display=dict(title='Developing Effective Fractions Instruction for Kindergarten Through 8th Grade',url=URL,authors_year='Siegler 외, IES/WWC 2010'),
  source_pdf_url=PDF_URL,read_scope='가이드90쪽 전체 텍스트와 지정한23쪽 이미지, 공식 안내 및 당시 프로토콜8쪽',
  reading_log=['가이드PDF1–90 텍스트 전체 확인. 표본·방법·권고 근거는AppendixD, 효과크기는표D2와 본문 대조.',
   '그림1–10·예1–5와 기준 단위·혼합수·분수 나눗셈·교차 곱 수식을 실제 이미지로 확인.90쪽 전체를 이미지 대조한 것은 아님.',
   '프로토콜8쪽 전체 텍스트 및PDF4 탈락률 곡선 확인.2010판WWC v2.0 검토와 현행 기준을 구별.',
   '공식 프로토콜의 초기 비포함 범위와 최종 가이드의교사연수 권고 차이는AppendixD의추가 검색으로 설명됨.125+7=132편,26+7=33편을 서로 모순된 합계로 분류하지 않음.'],
  visual_pdf_pages=[4,17,20,21,22,27,28,29,30,34,35,36,37,38,39,44,45,46,64,66,67,74,75],
  additional_read_artifacts=[dict(url='https://ies.ed.gov/ncee/wwc/Docs/ReferenceResources/wwc_fractions_pg_protocol_v2.0.pdf',sha256=PROTOCOL_SHA,pages=8,redistributed=False)],
  evidence_ratings=RATINGS,
  scope_note='권고1·4·5는Minimal,2·3은Moderate다. 이는2010년 패널이 권고 전체에 부여한 등급이며 자체 활동 효과의 검증 등급이 아니다. Minimal은 중요하지 않다는 뜻이 아니다. 원문 미국K–8 범위와 한국 성취기준의 범위를 구별한다.',
  method_note='당시WWC v2.0 기준의 인과 연구 심사와 이론·상관·사례 근거를 구별했다. 권고2의 근거 상당 부분은 자연수·소수, 권고3의 핵심 실험은 소수 절차 학습이다. 수직선을 두 집단 모두 사용한 연구의 실제 비교는 질문·눈금 단서였다. 교사연수의 결과는 혼재한다. 본 작업은 새로운 체계적 문헌 고찰이 아니다.',
  limits='모든 개별 원연구·원자료를 재분석하지 않았다. 수업 묶음의 결과를 요소 하나의 효과로 단정하지 않는다.26명 연구의 효과크기는본문2.38과표D2 2.83이 달라 수치 인용을 보류한다. 학급 수와 학생 수를 합치거나 여러 권고에 재인용한 연구를 독립 표본으로 중복 합산하지 않는다. 권고를 보편적 필수 선수 경로나 자체 학생 검증으로 승격하지 않는다.',
  source_discrepancies=[dict(locations=['PDF66 / printed60','PDF67 TableD2 / printed61'],issue='같은26명 연구의 효과크기2.38 대2.83',status='unresolved_do_not_select_one',followup='원연구Rittle-Johnson and Koedinger2009 및 정오표 대조. 미주210은sig/ns정의로 불일치 해소 근거가 아님.')],
  editorial_action='관계·분석군6건에 권고 등급과 적용 한계, 자체 관찰4건에 기준 단위·어림 검산·분수의 기준·비례 조건을 추가. 독립 검토·학생 검증은 완료로 표시하지 않음.',independent_review=False,student_validated=False,observations=OBSERVATIONS)
 registry['sources'][SOURCE]=source
 for cid,target,codes,recs,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='instructional_recommendation_with_evidence_scope',locations=locations,support=support,does_not_establish=limit,target_snapshots={target:digest(target_value(target))},standard_codes=codes,independent_review=False,student_validated=False,local_effect_tested=False,
   recommendations=[dict(number=n,evidence_rating=RATINGS[str(n)],application_limit=limit) for n in recs]))
 sp.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 qp=ROOT/'data/content_review_queue.json';queue=json.loads(qp.read_text(encoding='utf-8'));row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE);row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[c[0] for c in MAPPINGS]);qp.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 build_report()
if __name__=='__main__':main()

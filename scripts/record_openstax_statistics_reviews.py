"""Record complete statistics web sections without promoting textbook examples to evidence of learning."""
import hashlib,json,math
from fractions import Fraction
from statistics import NormalDist
from literature_review import ROOT,digest,target_value,load_registry,build_report

P='OPENSTAX_STATS_INTERVAL';T='OPENSTAX_STATS_TEST'
S='12실통';Q='12확통'
CONFIG={P:dict(stem='openstax-proportion',sha='a147d032e44eef0fedb68600356ce9a7dc438dc21dad812558acbea94a58290b',
 scope='8.3절 전체 웹본문·수식·예8.10~8.14·확인8.10~8.14·계산기 안내·표본 크기 설계',
 reading_log=['공식8.3절의 도입, 이항모형과 표본비율의 정규근사, 표준오차·오차한계·신뢰구간 공식을 읽고 수식의 분자·분모·모수와 관측값을 대조했다.',
  '예8.10~8.14와 확인8.10~8.14, 계산기 입력 안내, plus-four 조정, 표본 크기 공식과 올림을 모두 읽었다. 이 절에는 본문 삽입 이미지가 없으며 수식은MathML이다. 원책의 장말 연습 전체나PDF 판면을 읽은 것은 아니다.',
  '예8.10·8.11·8.12·8.13의 구간과8.14의 표본 수를 별도 계산했다. 특정 계산기 화면을 실제 실행하거나 모든 확인 문항의 해답을 검산한 것으로 표시하지 않는다.',
  '정규근사는 이산 통계량의 정확한 연속 분포가 아니다. 참p와 추정p-hat, 표본 선택과 편향, 관측 응답과plus-four 조정 수를 구별했다.'],
 corrections=[dict(kind='source_formula_transcription_inconsistency',location='8.3절 예8.13의q-prime 계산',observation='p-prime=15/54≈0.278 다음 줄에q-prime=1−0.241=0.722로 적혀 있다.1−0.241은0.759이며 앞의p-prime 및0.722와 일치하지 않는다.',action='정확히q-prime=39/54=13/18≈0.72222임을 확인했다. 자체 설명에서는 관측 비율과 조정 비율을 명시한다. 출판 정오표의 공식 정정은 미확인이고 원문 파일은 고치지 않는다.'),
  dict(kind='source_parameter_qualification',location='8.3절 예8.10의X~B(500,421/500)',observation='관측 비율421/500을 이항모형의 확률 자리에 직접 적었다. 뒤 문단은 이것이 모비율의 추정값이라고 설명한다.',action='자체 설명은X~Bin(n,p)의 참p가 미지임을 유지하고,421/500은 표준오차를 추정할 때 대입한 값으로 구별한다. 표본비율의 정규분포 표기도 근사임을 명시한다.'),
  dict(kind='source_sampling_scope_qualification',location='8.3절 확인8.11·8.13와예8.14',observation='한 학교 응답으로 교육구 전체를 묻거나 포커스그룹·전화 응답에 곧바로 구간 공식을 적용하는 예가 있다. 표본 크기 공식도 선택편향을 제거하는 절차는 아니다.',action='모집단·표집틀·선택/무응답·독립 조건을 따로 확인한다. 원문 >5 성공/실패 기준과plus-four 권고를 보편적인 정확도 보장으로 확대하지 않는다.')]),
 T:dict(stem='openstax-errors',sha='47fa4fd55cb97efe0464c78d1671ecf8882ce622b954acd5b7395051e7c81558',
 scope='9장 도입 전체·목표·그림9.1 및9.2절 전체·표9.2·예9.5~9.8·확인9.5~9.8',
 reading_log=['공식9장 도입의 목표·모수에 대한 주장·검정의5단계를 모두 읽었다. 그림9.1의 실제 사진 한 개를 시각적으로 확인했고 주소·해시를 기록했다. 사진으로 모든 개의 반점 수를 셀 수 있는 것은 아니다.',
  '9.2절 전체, 표9.2의 참/거짓과 기각/기각하지 않음 네 조합,α·β·검정력의 정의, 예9.5~9.8과 확인9.5~9.8을 모두 읽었다.9.2에는 별도 삽입 이미지가 없으며 표9.2는HTML 표다.',
  '오류 확률은 귀무모형 또는 특정 대립 모형을 조건으로 한다. 기각 뒤 귀무가설의 확률이나 개별 판단이 틀렸을 확률과 구별했다. β·검정력은 참 모수·표본 수·검정 규칙에 따라 달라진다.',
  '원문이 제시한 오류 비용의 맥락을 제1종/제2종 중 어느 것이 항상 심각하다는 보편 순위로 전용하지 않았다. 자체 활동은 중립적인 가상 빈도·동전 모형·수 자료를 사용한다.9장 다른 절의 검정 계산법·부록·장말 연습 전체는 미대조다.'],
 corrections=[dict(kind='source_claim_scope_qualification',location='9장 도입 그림9.1의every Dalmatian has35spots 설명',observation='모든 개체가 같은 반점 수를 갖는다는 주장과 모집단 평균에 대한 주장은 다르다.',action='자체 활동은 개별 값·표본평균·모평균·모든 개체에 관한 명제를 구별한다. 평균 검정으로 모든 개체의 동일한 값을 입증하지 않는다. 공식 정오표의 확인이나 실제 동물 집단 조사로 표시하지 않는다.'),
  dict(kind='source_decision_language_qualification',location='9.2절 표9.2와예9.6~9.8',observation='사례의 일상어로 귀무가설을 믿는다는 설명을 쓰더라도 검정에서 기각하지 않음은 귀무가설의 증명이 아니다.',action='자체 발문에는기각/기각하지 않음과 참/거짓을 별도로 명시한다. 특정 오류의 비용과 실제 상태를 확인하지 못한 판단을 구별한다.')])}

CLAIMS=[
 ('OP01',P,[S+'03-03',Q+'03-06'],['8.3절 도입의X/n·정규근사·표준오차','예8.10~8.11'],
  '독립 이항모형의 참 모비율p와 관측 표본비율x/n을 구별한다. 표본비율의 표준오차√[p(1−p)/n]와 대입 추정값, 이산 표집분포와 정규근사도 구별한다.',
  '정규근사를 정확한 연속 분포라고 쓰지 않는다. 원문의 성공·실패>5 기준은 그 교재의 근사 점검 관례이며 모든 표집설계·경계 비율의 정확도를 보장하지 않는다. 이 절로 모평균의t절차까지 검토했다고 표시하지 않는다.'),
 ('OP02',P,[S+'03-03',Q+'03-07'],['8.3절 예8.10~8.11의신뢰수준 설명'],
  '신뢰수준은 같은 표집·구간 생성 절차를 반복했을 때 고정된 모비율을 포함하는 비율로 설명한다. 모비율의 구간과 개별 응답의 비율, 한 번 얻은 구간에 대한 사후확률을 구별한다.',
  '작은 유한 반복에서 포함 비율이 반드시95%일 필요는 없다. 근사 구간의 실제 포함률은 조건과 방법에 따라 달라진다. 이 절은 모비율의 예이며 모평균 구간의 분포·조건을 대신 검증하지 않는다.'),
 ('OP03',P,[S+'03-03'],['8.3절 Plus Four·예8.12~8.13·확인8.12~8.13'],
  '관측 비율과 방법이 조정한 비율을 구별하고 선택한 구간 방법을 보고한다. 관측 성공0의Wald 폭0을 확실성으로 읽지 않으며, plus-four의x+2·n+4는 실제 관측 네 건의 추가가 아니다.',
  'plus-four·다른 경계 처리 방법을 모든 표본의 정확한 해법이나 새 필수 계산법으로 추가하지 않는다. 교재의 모의실험 효과 서술을 자체 학생 활동의 효과로 사용하지 않는다. 자체 경계 예는 교사용 선택 확장이다.'),
 ('OP04',P,[S+'01-03',Q+'03-05'],['8.3절 확인8.11·8.13','Calculating the Sample Size n·예8.14'],
  '허용 오차와 신뢰수준의 표본 수 계산은 정한 표집모형 안의 정밀도 계획이다. 표본 수 확대와 모집단 대표성·표집틀·무응답의 문제를 별도로 확인한다.',
  '계산한n이 선택편향이나 모집단 범위의 불일치를 제거하지 않는다. p(1−p)≤1/4의보수적 설계와 실제 비응답 수·유한 모집단/군집 설계의 조정은 구별한다.'),
 ('OT01',T,[S+'03-04'],['9.2절 표9.2와네 가능한 결과','예9.5~9.8·확인9.5~9.8'],
  '실제 귀무가설의 참/거짓과 데이터에 따른 기각/기각하지 않음을 네 조합으로 구별한다. 제1종 오류는 참인 귀무가설의 기각이고 제2종 오류는 거짓인 귀무가설을 기각하지 않는 것이다.',
  '기각하지 않음을 귀무가설의 증명으로 바꾸지 않는다. 어느 오류가 더 심각한지는 주어진 비용과 맥락에 달려 있으며 오류 이름만으로 순위를 정하지 않는다.'),
 ('OT02',T,[S+'03-04'],['9.2절α·β·Power정의·표본 크기에 관한 설명'],
  'α는 참 귀무모형 아래의 기각 확률이고β는 특정 대립 모형 아래의 비기각 확률이다. 같은 대립 모형의 검정력은1−β이며α만으로β나검정력이 정해지지 않는다.',
  'α·β를 조건을 뒤집은 확률이나p값으로 읽지 않는다. β는 복합 대립가설 전체에 하나로 고정된 수가 아니다. 자체 이항 예는 정의를 확인하는 선택 확장이며 교육과정에 검정력 이론 전개를 필수화하지 않는다.'),
 ('OT03',T,[S+'01-01',S+'01-02',S+'03-04'],['9장 도입의모수 주장·검정5단계','그림9.1설명과9.2절 판정의 구별'],
  '통계적 질문을 모평균·모비율 같은 모수의 주장으로 명확히 하고, 모든 개체의 값에 관한 명제와 구별한다. 표집·모형·판정 뒤에는 원래 질문과 범위로 돌아가 결론을 쓴다.',
  '평균에 관한 검정이 모든 개체의 동일한 값이나 인과 효과를 입증하지 않는다. 사진·일상 사례·유한 표본의 계산을 모집단 전수조사나 실제 학생 검증으로 바꾸지 않는다.')]

OBS={P:[
 dict(id='OP-P1',standard_codes=[S+'03-03',Q+'03-06'],question='가상 독립 이항 표본200건 중 정한 사건이120건 관측됐다. 참 모비율p·표본비율·표준오차의 참값 식과 대입 추정식을 구별하고, 양측95% 정규근사 구간을 구하라. 참p도0.6이라고 확정할 수 있는가?',
  expected='표본비율은0.6이며참p는미지다. 참 표준오차는√[p(1−p)/200], 대입 추정값은√(0.6×0.4/200)≈0.03464다.1.96을 사용한 근사 구간은약[0.5321,0.6679]다. 관측 성공120·실패80과 무작위성·독립/표집설계를 확인하며 참p를0.6으로 확정하지 않는다.',
  interpretation='관측값·모수·추정 표준오차·근사 조건·방법 이름을 각각 기록한다. 통계량은이산값을 가지며 정규근사는 정확한 정규분포 동일성이 아니다. 실제 조사나 특정 도구 화면을 실행한 자료로 표시하지 않는다.',student_validated=False),
 dict(id='OP-P2',standard_codes=[S+'03-03',Q+'03-07'],question='참 모비율p=0.60을 아는 가상 반복 실험에서 예시 구간세 개가[0.53,0.67],[0.45,0.59],[0.59,0.73]으로 주어졌다. 포함하는 구간 수와 이세 번의 포함 비율을 구하라.95% 신뢰수준이면 모든 유한 반복에서도 반드시95%를 포함하는가?',
  expected='첫째·셋째 두 구간이0.60을 포함하므로 이표의 포함 비율은2/3이다.95%는 정한 절차를 반복하는 모형에서의 포함 성질이며 세 구간에서 정확히95%가 나와야 한다는 뜻이 아니다. 고정된p의 위치와 반복마다 달라지는 구간을 구별한다.',
  interpretation='구간에 포함되는 사건과 사람/개별 응답을 포함하는 비율을 구별한다. 예시 세 구간을 실제95% 절차의 성능 검증 자료나 자체 학생 실험으로 사용하지 않는다. 근사 절차의 실제 포함률도 별도 확인 대상이다.',student_validated=False),
 dict(id='OP-P3',standard_codes=[S+'03-03'],question='교사용 방법 비교 확장이다. 독립 이항모형의20건 중 성공0이면Wald 식에 그대로 넣은 구간은무엇인가? 이것이참p=0의증명인가? plus-four 방법의 조정 성공 수·전체 수와 실제 관측 수를 구별하라.',
  expected='단순 대입은표본비율0·추정 표준오차0이어서[0,0]이 된다. 하지만참p=0.1이어도성공0의확률은0.9²⁰≈0.1216으로양수이므로p=0을 증명하지 않는다. plus-four에서는조정 성공2·전체24·조정비율1/12지만 실제 관측은여전히20건·성공0건이다.',
  interpretation='경계의 근사 실패와 실측/조정 수를 구별한다. 한 대안 방법의 구간을 모든 상황의 정확한 답으로 간주하지 않는다. 이 비교는 교사가 선택하는 확장이며plus-four나이항 검정 이론을 학생의 새 필수 목표로 추가하지 않는다.',student_validated=False),
 dict(id='OP-P4',standard_codes=[S+'01-03',Q+'03-05'],question='독립 이항 표집모형에서 참p를 모를 때p(1−p)≤1/4를 사용하고z=1.96·오차한계0.05로 계획 표본 수를 계산하라. 그 수만큼 자원 응답을 모으면 목표 모집단을 대표한다고 보장되는가? 같은 조건에서n을4배하면 계산식의 오차한계는 어떻게 되는가?',
  expected='n≥1.96²×0.25/0.05²=384.16이므로올림한385건이다. 표본 수만으로자원 응답의 선택편향·표집틀 누락·무응답을 제거하지 못한다. 같은p·신뢰수준·표집모형에서는오차한계가1/√n에 비례하므로n을4배하면반으로 줄어든다.',
  interpretation='모형 안의 정밀도·모집단 대표성·실제 응답 확보를 구별한다. 유한 모집단 비복원·군집 설계·비응답 보정에는 다른 점검이 필요하다. 모비율 표본 수 계산은 도구 결과의 조건을 살피는 자체 확장으로 사용한다.',student_validated=False)],
 T:[
 dict(id='OT-P1',standard_codes=[S+'03-04'],question='다음은 실제 응답이 아닌 가상 반복 결과표다. 참귀무모형1000회에서기각50·비기각950, 특정대립모형100회에서기각80·비기각20이다. 네칸의 정오와 각 모형 안의오류/검정력 비율을 구하라.5%가 기각된경우 귀무가설이참일 비율인가?',
  expected='참귀무의기각50은제1종 오류, 비기각950은정판정이다. 대립모형의비기각20은제2종 오류, 기각80은정판정이다. 표 안의조건부 비율은50/1000=0.05,20/100=0.20,80/100=0.80이다. 기각된130회중 참귀무모형의50회 비율은5/13이며0.05와 다르다. 이값은가상 표의 모형 구성비에 의존한다.',
  interpretation='오류 이름·조건 집단·분모·기각 후의구성 비율을 구별한다. 이가상 표의빈도를 실제 검정의 이론적 오류율이나 귀무가설의 일반적인 사후확률로 확정하지 않는다. p값도귀무가설이참일 확률이 아니다.',student_validated=False),
 dict(id='OT-P2',standard_codes=[S+'03-04'],question='교사가선택하는 정확한 유한모형 확장이다. 독립동전4회의H0:p=1/2,H1:p>1/2에서앞면4개일 때만기각하는 규칙을 정했다. H0 아래기각 확률과p=3/4·9/10일 때각기각 확률을 구하라. 같은α이면검정력도같은가? 앞면3개로비기각하면H0가증명되는가?',
  expected='α=(1/2)⁴=1/16이다. p=3/4에서검정력은81/256·β는175/256이고,p=9/10에서는검정력6561/10000·β3439/10000이다. 같은규칙과α여도 대립모수에따라 검정력이달라진다. 비기각은p=1/2의증명이 아니다.',
  interpretation='참모수·규칙·기각 사건과1−β를 같은모형 안에서 대응시킨다. 정규근사를사용하지 않은 자체예이며검정력의 일반이론·공식 증명을 새필수 내용으로 요구하지 않는다. 한 번의결과로 모형의진위를 확정하지 않는다.',student_validated=False),
 dict(id='OT-P3',standard_codes=[S+'01-01',S+'01-02',S+'03-04'],question='가상 관측값2,4,6,8의평균을 구하라. 이값들이모평균μ=5라는귀무가설을 검정하는 자료라면, 이를모든개체의값이5라는주장과 같은것으로볼수 있는가? 기각하지못한 경우의결론도구별하라.',
  expected='표본평균은5지만 관측값중5는없다. 모평균5라는주장과모든개체가5라는주장은다르며 평균이5인 자료도개별값은다를수 있다. 모평균에대한비기각은μ=5의증명이아니며 모든개체의값이5라는보장도아니다. 실제검정에는표집·모형·규칙이따로필요하다.',
  interpretation='표본요약·모수·모든개체에관한명제·판정을구별한다. 네값의평균만으로p값이나 모집단진위를정하지 않는다. 실제집단전수·인과효과·학생검증의근거로바꾸지 않는다.',student_validated=False)]}

def verify_calculations():
 assert abs(NormalDist().inv_cdf(.975)-1.95996398454)<1e-10
 p=120/200;se=math.sqrt(p*(1-p)/200)
 assert abs(se-.0346410161514)<1e-12 and abs(p-1.96*se-.5321036083433)<1e-12
 for n,x,critical,expected in [(500,421,1.96,(.81003,.87397)),(500,300,1.645,(.56396,.63604)),(29,8,1.96,(.113,.439)),(54,15,1.645,(.178,.378))]:
  ph=x/n;e=critical*math.sqrt(ph*(1-ph)/n);tol=.0006
  assert abs(ph-e-expected[0])<tol and abs(ph+e-expected[1])<tol
 assert math.ceil(1.645**2*.25/.03**2)==752 and math.ceil(1.96**2*.25/.05**2)==385
 assert Fraction(39,54)==1-Fraction(15,54) and 1-Fraction(241,1000)!=Fraction(722,1000)
 assert math.isclose(.9**20,.12157665459056935)
 assert Fraction(50,1000)==Fraction(1,20) and Fraction(20,100)==Fraction(1,5) and Fraction(50,130)==Fraction(5,13)
 assert Fraction(1,2)**4==Fraction(1,16) and Fraction(3,4)**4==Fraction(81,256) and Fraction(9,10)**4==Fraction(6561,10000)
 assert sum([2,4,6,8])/4==5

def main():
 registry=load_registry();verify_calculations()
 if all(sid in registry['sources'] for sid in CONFIG):
  print('Reviewed sources and targets remain current; no automatic refresh');build_report();return
 assert not any(sid in registry['sources'] for sid in CONFIG),'Review a partial batch explicitly'
 assets=json.loads((ROOT/'tmp/literature/openstax-statistics-assets.json').read_text(encoding='utf-8'));assert len(assets)==3
 images=json.loads((ROOT/'tmp/literature/openstax-statistics-image-provenance.json').read_text(encoding='utf-8'));assert len(images)==1
 for a in assets:assert hashlib.sha256((ROOT/f"tmp/literature/{a['stem']}.html").read_bytes()).hexdigest()==a['sha256']
 for a in images:assert hashlib.sha256((ROOT/'tmp/literature'/a['file']).read_bytes()).hexdigest()==a['sha256']
 sources=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'));queue=json.loads((ROOT/'data/content_review_queue.json').read_text(encoding='utf-8'))
 for sid,cfg in CONFIG.items():
  b=next(s for s in sources if s['id']==sid);previous=dict(b)
  assert next(a['sha256'] for a in assets if a['stem']==cfg['stem'])==cfg['sha']
  b.update(review_scope=cfg['scope']+' 전체 읽기·수식/표 대조. PDF판면·원책 전권·장말 연습 전체·실제 계산기 화면 실행은 미대조.',next_review='관련 검정 계산 절·추정 방법 비교의 원연구·출판 정오표·판본 변경은 추가 대조 대상. 자체 한국어 과제의 독립 검토와 실제 학생 반응 검증은 별도.')
  relevant=[a for a in assets if a['stem']==cfg['stem'] or (sid==T and a['stem']=='openstax-test-intro')]
  notes=dict(source_id=sid,source_url=b['url'],source_asset_kind='publisher_html',source_asset_sha256=cfg['sha'],source_asset_redistributed=False,date='2026-11-05',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,reading_log=cfg['reading_log'],source_corrections=cfg['corrections'],observed_html_assets=[dict(url=a['url'],sha256=a['sha256']) for a in relevant],observed_image_assets=images if sid==T else [],
   own_calculation_checks='지정한 원문 예제의 구간·표본 수와 자체 과제의 정확한 분수·조건부 분모·이항 확률을 별도 계산했다. 모든 해답·실제 도구 화면·학생 반응의 검증은 아니다.',
   interpretation_limits=['교재의 수학적 설명을 지원하는 자료이며 독립 학생 실험·교수 효과 연구가 아니다.','신뢰수준·오류율의 모형 조건을 유지한다. 방법 비교·검정력 유한 예는 교사의 선택 확장이며 새 필수 이론을 추가하지 않는다.'])
  file=ROOT/f'data/literature_evidence/{sid}_review_notes.json';file.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  registry['sources'][sid]=dict(source_id=sid,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-05',snapshot_kind='authored_review_notes',snapshot_file=file.relative_to(ROOT).as_posix(),snapshot_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),source_asset_kind='publisher_html',source_asset_sha256=cfg['sha'],redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,display=dict(title=b['title'],url=b['url'],authors_year='Illowsky·Dean,OpenStax,Introductory Statistics2e,2023／확인한 공식 웹본문'),read_scope=cfg['scope'],scope_note='웹본문의 수학적 설명·수식·표·예시를 대조했다. PDF판면·원책 전권과 구별하며 교재 예시를 자체 활동의 효과나 학생 검증으로 전용하지 않는다.',method_note='모수/통계량·근사/정확·모형/표집·고정 모수/반복 구간 또는 참/거짓·기각/비기각·조건부 오류율의 차이를 대조했다. 선택한 예제와 자체 과제의 계산을 별도 확인했으며 모든 장말 해답·원연구·실제 계산기 화면을 검증하지 않았다.',limits='한국2022개정 과목의 범위를 유지하며plus-four·검정력 이론을 새 필수 내용으로 추가하지 않는다. 수학 교재를 교수 효과·진단 타당성·실제 학생 반응의 실증으로 사용하지 않는다. 확인한 웹 자산의 주소·해시를 보존하며 이후 원격 변경을 실시간 확인하지 않는다.',editorial_action=('모비율·근사/신뢰수준·방법/경계·표집 정밀도 주장4건과 자체 관찰4건을 보완. 예8.13의 뺄셈 표기 불일치와 모수/표집 조건을 기록.' if sid==P else '참/거짓과 판정·조건부 오류율/검정력·모수 주장 범위의 근거3건과 자체 관찰3건을 보완. 평균과 모든 개체 주장·비기각의 의미를 구별.')+'독립 검토·학생 검증은 완료로 표시하지 않음.',independent_review=False,student_validated=False,observations=OBS[sid])
  for cid,source,codes,locations,support,limit in CLAIMS:
   if source!=sid:continue
   registry['claims'].append(dict(id=cid,source_id=sid,role='mathematical_explanation',locations=locations,support=support,does_not_establish=limit,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},standard_codes=codes,independent_review=False,student_validated=False))
  row=next(r for r in queue['literature_review'] if r['source']['id']==sid);row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[c[0] for c in CLAIMS if c[1]==sid])
 for file,value in [('data/sources.json',sources),('data/literature_claim_reviews.json',registry),('data/content_review_queue.json',queue)]:
  (ROOT/file).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 load_registry();build_report()
if __name__=='__main__':main()

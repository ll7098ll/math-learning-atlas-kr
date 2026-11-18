"""Seven explicitly read primary 3-4 outgoing data links; no promotion."""
import json
from fractions import Fraction as F
from relation_analysis_review import ROOT,FILE,materials,source_value,digest,load_reviews

LIMIT='양쪽 기준 문장·대표 의미·풀이·조건과 기존 이유·조건·질문, 새 진단·기대 설명·계산·반례의 명시한 범위만 자체 점검했다. 후속 분포·기울기·가중 평균을 초등의 새 필수 수행으로 요구하지 않는다. 가상 자료는 실제 조사·직무 도구 실행·건강 판정·학생 반응이 아니며 독립 검토·학생 검증으로 집계하지 않는다.'
REVIEWS=[]

def add(rid,reason,conditions,question,expected,check,learning):
 REVIEWS.append((rid,reason,conditions,question,expected,check,learning))

add('SEC_12직수04-03_C03','그림·막대의 단위 읽기를 직무 질문에 맞는 관찰 단위·집계·그래프 선택으로 연결한다.',
 ['가상 주문 월10·화12·수8·목15·금5건과 별도 배타적 품목 집계 A20·B15·C15건을 사용한다.'],
 '그림 하나가 5건이면 20·35·15건의 그림 수는? 일별 변화와 품목 비교에 같은 그래프를 쓰는가? 복수 품목이면 합을 주문 수로 읽는가?',
 '그림 수는 4·7·3개이며 범례 없이는 건수를 읽을 수 없다. 일별 변화는 날짜 순 꺾은선, 품목 비교는 막대가 적합하다. 두 집계가 모두 50이어도 같은 기록 구조라는 뜻은 아니며 한 주문의 복수 품목은 주문 수와 다를 수 있다.',
 '20/5=4,35/5=7,15/5=3과 일별 합50·품목 합50을 검산했다. 배타적 단일 분류일 때만 품목 비율40%·30%·30%를 전체 주문의 구성으로 읽는다.',
 ['범례와 관찰 단위','시간 순서와 범주 비교'])
add('SEC_9수04-02_C03','범주의 막대 비교와 수량 구간에 묶은 분포 표현의 축·경계·정보 손실을 구별한다.',
 ['가상 통학시간 5,8,10,12,14,15,18,21,25,27분을 폭10의 계급 0≤t<10,10≤t<20,20≤t<30으로 나눈다.'],
 '10분을 어느 계급에 넣는가? 도수 합과 다각형의 점을 구하고 첫 계급의 정확한 두 값을 히스토그램만으로 복원할 수 있는지 말하라.',
 '10분은 두 번째 계급에만 들어간다. 도수는2·5·3, 합10이고 다각형의 점은(5,2),(15,5),(25,3)이다. 첫 계급의 두 값이5·8인지2·9인지는 도수만으로 복원되지 않는다.',
 '범주의 이름을 놓는 막대와 연속된 수량 구간을 놓는 히스토그램을 구별한다. 같은 폭에서 높이로 도수를 읽으며 보조계급의 도수0을 실제 관측값0과 혼동하지 않는다.',
 ['계급 경계','집계와 원자료의 차이'])
add('SEC_12수문04-02_C03','시간 변화 그래프의 점값·간격·관측 범위를 농도 자료의 가중 요약과 연결한다.',
 ['가상 값10,20,30이 각각1,1,2시간을 대표하며 같은 농도 단위를 쓴다. 실제 건강·환경 기준은 제시하지 않는다.'],
 '세 값의 평균20이 시간 평균인가? 연결선만 보고 중간 시각의 실제 농도나 전체 지역의 상태를 확정하는가?',
 '동일 시간 간격을 대표하면20이지만 주어진 지속 시간에서는(10+20+60)/4=22.5다. 연결선은 관측하지 않은 중간값의 실제 측정이 아니며 한 지점의 값으로 지역 전체를 확정하지 않는다.',
 '단순 평균20과 시간 가중 평균22.5를 계산했다. 농도·배출 총량·노출 시간은 다른 양이며 이 가상 계산으로 건강 영향이나 개선책의 실제 효과를 검증하지 않는다.',
 ['관측과 보간','시간 가중과 적용 범위'])
add('AN_4수04-02_C04','시간 순서의 꺾은선 해석을 관찰 단위·변수 종류·질문에 따른 그래프 선택과 연결한다.',
 ['가상 월~금 주문10,12,8,15,5건과 범주별 교통수단12,18,10명을 구별한다. 도착 기준은 그래프 선택·작성이며 평균변화율·극한의 필수 수행을 포함시키지 않는다.'],
 '날짜 순 주문 자료와 교통수단 범주를 모두 선으로 잇는가? 기존 연결 이유의 평균변화율·극한이 이 통계 기준의 수행인가?',
 '날짜 순 변화에는 꺾은선이 적합하다. 교통수단 범주 비교에는 막대를 쓰며 임의의 범주 순서로 이은 기울기를 시간 변화로 읽지 않는다. 도착 기준은 자료 특성에 맞는 그래프 선택이므로 평균변화율·극한을 그 기준의 요구라고 쓰지 않는다.',
 '주문 변화량은+2,−4,+7,−10건이며 최고값15와 최대 증가+7은 다른 정보다. 기존 이유에 섞인 다른 후속 수학 범위를 제거하고 통계 그래프 선택이라는 양쪽의 공통 활동을 명시했다.',
 ['도착 기준의 실제 범위','변수와 그래프 선택'])
add('SEC_12직수02-04_C03','시간 그래프의 값·변화·반복을 직무 자료의 축에 기록된 양과 단위에 맞추어 해석한다.',
 ['모의 시각0,1,2,3,4시간의 전력 수준2,4,6,4,2kW를 사용한다. 실제 작업·안전 기준이 아니다.'],
 '2시간의6과 앞 구간의2는 무엇의 값인가? 이 감소 그래프를 누적 사용 에너지로 그대로 읽거나4시간 주기를 확정하는가?',
 '6kW는2시간의 전력 수준이고 앞 두 구간은 각각2kW/시간으로 증가한다. 순소비만 누적하는 에너지라면 감소로 읽을 수 없으며 kWh와도 구별한다. 한 번의 봉우리만으로 미래4시간 주기를 확정하지 않는다.',
 '차분은+2,+2,−2,−2kW다. 같은 간격의 추가 반복 관측이 있어야 관측 범위의 주기를 논의하며 이 점값들만으로 실제 구간 에너지를 확정하지 않는다.',
 ['축의 양과 단위','한 번의 변화와 주기'])
add('SEC_9수02-06_C03','꺾은선의 점값·구간 변화를 두 양의 대응·수평 구간·직선 가정과 연결한다.',
 ['가상 물 높이는0,1,2,3분에0,2,4,6cm, 이후5분까지6cm다. 앞 구간은 일정한 높이 변화율을 가정한다.'],
 '3~5분의 수평선은 높이0인가? 반드시 유입 중단인가? 관측점만으로 모든 중간값이 확정되는가?',
 '높이는6cm로 유지되고 변화량은0이다. 유입과 유출이 같은 경우도 있어 높이 유지가 유입 중단만을 뜻하지 않는다. 점 사이 직선은 일정 변화율이라는 추가 가정이며 통의 단면적이나 유출 조건이 바뀌면 유지되지 않을 수 있다.',
 '앞 구간의 높이 변화율은(6−0)/(3−0)=2cm/분, 뒤 구간은(6−6)/(5−3)=0이다. 점값·변화율·원인 설명의 근거를 구별했다.',
 ['높이와 수평 구간','직선 가정과 원인'])
add('AN_4수04-02_C02','같은 시간 간격에서의 변화량 비교와 서로 다른 간격의 기울기·시작값 해석을 구별한다.',
 ['가상 관측(0,10),(1,13),(3,17)과 별도 요금 모형 y=1000x+3000, x≥0을 비교한다.'],
 '뒤 구간의 증가4가 앞의3보다 크니 더 빠른가? 요금(2,5000),(5,8000)에서8000/5가 기울기인가?',
 '앞은3/1=3, 뒤는4/2=2라 뒤의 증가량이 커도 평균 변화율은 낮다. 요금 기울기는(8000−5000)/(5−2)=1000원/km이고8000/5=1600원/km는 기본료가 포함된 평균 비용이다.',
 '불규칙 관측 세 점의 구간 기울기3·2를 전체 하나의 일차함수로 단정하지 않는다. 별도 요금식의 시작값3000과 일정 기울기1000을 분리하며 실제 제도나 초등의 필수 기울기 수행으로 쓰지 않는다.',
 ['변화량과 시간 간격','기울기와 시작값'])

def verify():
 assert len(REVIEWS)==len({r[0] for r in REVIEWS})==7
 assert [F(x,5) for x in [20,35,15]]==[4,7,3]
 assert sum([10,12,8,15,5])==sum([20,15,15])==50
 assert [F(x,50) for x in [20,15,15]]==[F(2,5),F(3,10),F(3,10)]
 values=[5,8,10,12,14,15,18,21,25,27]
 assert [sum(a<=v<b for v in values) for a,b in [(0,10),(10,20),(20,30)]]==[2,5,3]
 assert not 0<=10<10 and 10<=10<20
 assert [sum(a<=v<b for v in [2,9]+values[2:]) for a,b in [(0,10),(10,20),(20,30)]]==[2,5,3]
 assert F(10+20+30,3)==20 and F(10+20+60,4)==F(45,2)
 assert [b-a for a,b in zip([10,12,8,15],[12,8,15,5])]==[2,-4,7,-10]
 assert [b-a for a,b in zip([2,4,6,4],[4,6,4,2])]==[2,2,-2,-2]
 assert F(6,3)==2 and F(6-6,5-3)==0
 assert F(13-10,1-0)==3>F(17-13,3-1)==2
 assert F(8000-5000,5-2)==1000 and F(8000,5)==1600

def main():
 verify();registry=load_reviews();ids={r[0] for r in REVIEWS}
 if ids<=set(registry['records']):print('Seven primary 3-4 data links remain current; no automatic refresh');return
 assert not ids&set(registry['records']),'A partly recorded batch needs explicit review'
 queue=json.loads((ROOT/'data/relation_analysis_scope_queue.json').read_text(encoding='utf-8'))
 assert ids=={r['relation_id'] for r in queue['records'] if r['from_code'].startswith('4수04')}
 data=materials()
 for rid,reason,conditions,question,expected,check,learning in REVIEWS:
  raw=data['raw'][rid];assert raw['type']=='meaning_connection' and raw['from'][9:].startswith('4수04')
  review=dict(relation_id=rid,state='self_checked_scope_math',reviewer='Codex',date='2026-11-06',to=raw['to'],type='meaning_connection',
   scope='초등3~4학년 자료 출발 연결의 양쪽 공식 문장·대표 의미·풀이·조건과 기존 이유·조건·질문을 실제 대조했다. 그래프 선택·축·분포·시간 간격·점값과 변화의 가상 계산 범위를 자체 점검했다.',
   rationale=reason,conditions=conditions,diagnostic=question,expected_response=expected,mathematical_check=check,additional_learning=learning,limit=LIMIT,
   type_decision_reason='자료의 관찰 단위·표현·변화 해석이라는 공통 활동과 분포·가중 시간·기울기·직무 양의 추가 조건을 명시한 의미 연결로 유지한다. 통계 그래프 기준에 평균변화율·극한을 필수 요구로 덧붙인 기존 이유는 범위에 맞게 교정한다.',
   independent_review=False,student_validated=False,source_snapshot=digest(source_value(rid,ROOT,data)),
   read_scope='양쪽 statement_display와 대표 원고 mathematicalMeaning/taskSolution/conditions, 기존 관계 이유·조건·질문을 읽었다. 목표·과제·자료 전체 해시는 변경 추적이며 모든 연계 자료의 신규 정독·실제 측정·직무 실행·학생 반응을 검토했다는 뜻이 아니다.')
  review['from']=raw['from'];registry['records'][rid]=review
 (ROOT/FILE).write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');load_reviews()
 print(json.dumps(dict(reviewed_relations=7,total_scoped_reviews=len(registry['records']),new_type_corrections=0,independent_review=False,student_validated=False)))

if __name__=='__main__':main()

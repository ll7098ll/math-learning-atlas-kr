"""Complete the currently listed LT2 level texts; keep activity/assets pending."""
import copy
import hashlib
import json
from collections import Counter
from fractions import Fraction
from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews
from record_lt2_public_review import SOURCE, URL
from extend_lt2_pattern_spatial_review import NOTES as PRIOR_NOTES

NOTES='data/literature_evidence/CLEMENTS_SARAMA_LT_level_text_completion_review_notes.json'
PRIOR_SHA='28ea590ce6de2ba0ef0aa04909004bc3bad95b08bf28ac298fe29d5164e9dd6d'
DOMAINS=['counting','2d-shapes','measurement-length','fractions']
ACTIVITIES=['shopkeeper--fill-orders-to-10-counter-and-producer-10','counting-forward-and-back-with-the-hundreds-chart','build-shapes-constructor-of-shapes-from-partsexact','mr-mix-up-congruence-representer','order-by-length-6','broken-ruler','parts-of-wholes-and-parts-of-groups','rainbow-arrays']
SCOPE='공식 공개HTML 누적296개 지정 영어 본문: 일반6·영역 개요20·현재 목록의 수준224개 전부·활동45·교사자료1. 초기4영역의 남은52수준(세기15·평면도형20·길이9·분수8)과 선정8활동을 추가로 읽었다. 별도 삽입 그림은 누적43개다. 현재 공개20영역의 개요/수준 본문 읽기 완료이며 전체 사이트/활동/그림/영상/첨부PDF/게임/원연구 검토 완료가 아니다. 수준 본문의 활동/교사자료 링크824개 중46개 본문을 읽고 나머지778개는 목록만 확인했다.'
OBSERVATIONS=[
 dict(id='LT-P25',standard_codes=['2수01-01','2수01-06'],question='①같은 크기 물체19개에서14개를 골라 주문 모임을 만들고 남은 모임과 함께 확인한다. 먼저 주문 수를 유지하며 멈추는 모습을 기록하고,필요할 때 숫자14카드를 보여 준 뒤의 수행을 따로 기록한다.②왼쪽부터1~10,다음 줄11~20의 순서로 놓인1~100숫자판에서33에26을 더한다. 십2개·일6개로 나누어 이동하고,왜30+26을 계산한 결과와 다른지 설명하라.',expected='①주문 모임14개와 남은5개는 서로 겹치지 않고 합19개다. 이미 있는 모임을 세는 수행과 목표 수만큼 새 모임을 만들어 멈추는 수행은 별도로 확인한다.②33에서10씩 두 번 이동하면43·53이고,여기서1씩6번 이동하면54·55·56·57·58·59다. 따라서33+26=59다.30+26=56은 출발량이3작은 다른 식이다. 십 단위 두 번과 일 단위 여섯 번은 이동 횟수로는8번이지만 더한 양은26이며8을 더한 것이 아니다.',interpretation='자체 주문/숫자판 활동이다. 첫 세기·목표 유지·멈춤·기수 설명·단위 전환을 구별하고 기억/언어/소통과 수 개념을 한 번의 실패로 동일시하지 않는다.1~100판의 배열·한 줄10개·출발점·허용 결과 범위를 명시한다. 원문 본문의33과 식30+26을 섞지 않으며 판의 열 끝에서는 오른쪽 이웃이라는 위치와 다음 수 규칙을 구별한다. 원문의 미국 화폐에서 지폐 수와 금액은 다를 수 있어 이 자체 과제는 물체 하나를 단위 하나로 정했다. 작은 모임 생산의 성공을100까지 모든 세기·연산 숙달로 판정하지 않고 도움 뒤 응답을 처음 독립 응답으로 소급하지 않는다.',student_validated=False),
 dict(id='LT-P26',standard_codes=['2수03-04','6수03-01'],question='교사는 구부러지지 않고 길이가 정해진2cm·3cm 막대에 각각4cm,5cm,6cm 막대를 짝지은 세 꾸러미를 준비한다. 막대를 겹치거나 늘이지 않고 끝끼리 연결해 닫힌 삼각형을 만들 수 있는지 실제로 살핀다. 길이가 가장 긴 한 막대가 다른 막대 각각보다 길면 언제나 만들 수 없는가?5~6학년에서는 정확히 만든 같은 크기의 두 삼각형 모형을 방향을 바꾸어 포개며 대응하는 변과 각을 확인한다.',expected='2·3·4cm는 삼각형을 만들 수 있다.4는2와3 각각보다 길지만 그 합5보다는 짧다.2·3·5cm는 세 막대가 일직선으로만 만나 넓이가 있는 삼각형이 되지 않고,2·3·6cm는 두 짧은 막대로 긴 막대의 두 끝을 연결할 수 없다. 길이 비교는 긴 막대와 나머지 둘의 합을 구별해야 한다. 방향이 다른 두 모형도 완전히 겹치면 합동이며 이름이 같다는 사실이나 길이 하나만으로 합동을 판정하지 않는다.',interpretation='자체 막대/포개기 활동이다. 저학년에서는 열린 경계·일직선·닫힌 삼각형의 차이를 직관적으로 확인하고 제작 오차와 개념을 구별한다. 엄밀한 삼각형 부등식·원의 교점 작도·합동 판정 조건의 정리 증명을 저학년이나 초등의 새 필수로 넣지 않는다.5~6학년의 합동은 실제 포개기와 대응 확인에 한정하며 중학교의 작도/합동 조건 전체를 확인했다고 하지 않는다. 원문의longer than the other two는 각 길이와 합 중 무엇인지 명시하지 않으면 오해할 수 있어 조건을 정확히 쓴다. 원문의 사각형 계급 포함·다른 크기의 같은 종류 모양 맞추기와 합동을 구별한다.',student_validated=False),
 dict(id='LT-P27',standard_codes=['2수03-06','2수03-10','2수03-13'],question='길이가 각각2·4·5·7·9·11cm인 막대6개를 한 끝을 맞춰 짧은 것부터 놓는다. 새 막대는 같은 단위cm 눈금의2위치에서8위치까지 놓인다. 길이를 구하고 원래 줄에 끼워 넣어라. 새 막대가 왼쪽과 오른쪽의 모든 막대보다 길어야 한다는 설명이 맞는가? 같은 길이가 하나 더 있으면 어떻게 기록할 것인가?',expected='새 막대의 길이는8-2=6cm다.2부터8까지 눈금점은7개지만 사이1cm 간격은6개다. 증가 순서는2·4·5·6·7·9·11cm이고6cm는5cm보다 길고7cm보다 짧은 곳에 들어간다. 왼쪽은 모두6보다 짧고 오른쪽은 모두6보다 길다. 양쪽보다 모두 길면 가운데에 들어갈 수 없다. 같은 길이 막대가 더 있다면 동률을 보존하고 임의로 더 길거나 짧다고 하지 않는다.',interpretation='주어진 눈금 수의 차를 계산한 가상 측정과 실제 자의 배치/눈금 읽기를 구별한다. 실제 막대·자의 단위·나란함·두 끝·공유한 기준 끝·제작 오차·도움을 확인한다. 직접 비교를 먼저 할 수도 있고 필요한 경우 같은 기준 끈으로 간접 비교할 수 있으나 서로 다른 끈의 길이가 바뀌면 비교 근거가 사라진다. 원문의 증가 순서 삽입 설명 중 양쪽보다 길다는 문구를 복사하지 않는다. 원문의inch·속력/파생 단위·고급 둘레/삼각형 예를1~2학년 새 필수로 전용하지 않으며 이 한 길이 활동이 들이·무게·넓이 비교까지 검증하지 않는다.',student_validated=False),
 dict(id='LT-P28',standard_codes=['4수01-09','6수01-09'],question='3~4학년의 선택 확장:같은 칸12개로 된4열3행 종이에서 맨아래 한 줄4칸과 맨왼쪽 줄의 위2칸을 한 부분으로 칠한다. 나머지 부분과 모양이 달라도 각각 전체의반이라고 할 수 있는가?5~6학년의 별도 곱셈:새4열3행 종이 한 장에서3열을 빨강,1행을 파랑으로 칠해 겹친 부분을 찾는다. 전체 종이·빨간 부분·파란 부분 중 무엇을 기준으로 분수를 말하는지 설명하라.',expected='첫 종이의 두 부분은 각각 같은 크기 칸6개여서 각각 전체12칸의1/2다. 하나는ㄴ 모양,나머지는3×2직사각형이므로 모양이 같지 않아도 넓이는 같다. 새 곱셈 종이에서 빨강은9/12=3/4,파랑은4/12=1/3이고 겹친 부분은3칸이다. 전체 종이를 기준으로3/12=1/4=(3/4)×(1/3)이다. 같은 겹친 부분도 빨강만을 기준으로는3/9=1/3,파랑만을 기준으로는3/4이므로 기준 전체를 바꾸지 않는다.',interpretation='자체 격자/부분 활동이며 칸이 같은 넓이·빈틈과 겹침 없이 전체12개를 이룬 조건을 명시한다. 양의 등분은 같은 넓이를 뜻할 수 있고 항상 합동 조각을 요구하지 않는다. 연속 넓이의 분수와 대상 개수의 분수는 단위를 확인하고,일부 물체가 남을 때 자를 수 있는지도 별도로 정한다.3~4학년에는 분수 곱셈·약분 공식·둘레/넓이 공식을 새 요구로 넣지 않는다.5~6학년에는 같은 전체 안의 두 방향 분할과 겹침으로 곱셈을 설명하고,분수라는 이유로 항상 곱이 작아진다고 하지 않는다. 원문Rainbow 삽입 사진은 무지개 장식이며 실제 배열이나 학생 반응의 검증 자료가 아니다.',student_validated=False),
]
MAPPINGS=[
 ('LT25',OBSERVATIONS[0]['standard_codes'],['Counting의 남은15수준 본문과 이전4수준 기록','Shopkeeper - Fill Orders to10 / Counting Forward and Back with the Hundreds Chart 본문·삽입 그림'], '이미 있는 수량 세기·목표 수량 만들기/멈춤·십/일 이동과 출발량을 구별하는 자체 설계 참고다.', '숫자판 본문33에서26더하기를 식30+26으로 바꾸어 옮기지 않는다. 암송·숫자 읽기·개수 생산·횟수 추적은 별도다. 지폐 수와 금액·도움/기억 조건·교구 범위를 확인하며 작은 과제 하나나 단계 이름을 현재 학생의 전체 숙달/효과로 쓰지 않는다.'),
 ('LT26',OBSERVATIONS[1]['standard_codes'],['2D Shapes의 남은20수준 본문과 이전2수준 기록','Build Shapes [Constructor of Shapes from Parts—Exact] / Mr. Mix Up [Congruence Representer] 본문·삽입 그림'], '닫힘·직선성·길이 조합의 구성 가능성과 같은 종류/같은 크기·대응/합동을 구별하는 자체 설계 참고다.', '가장 긴 변이 다른 변 각각보다 길다는 것과 그 합 이상이라는 것은 다르며 합과 같은 퇴화 경우도 제외한다. 원문의 위계 분류를 국내 초등의 새 필수로 넣지 않고 다른 크기의 같은 종류 모양과 합동·근사 제작과 이상적 성질을 구별한다. 정리 증명/작도·현재 진단 단계의 검증이 아니다.'),
 ('LT27',OBSERVATIONS[2]['standard_codes'],['Measurement: Length의 남은9수준 본문과 이전3수준 기록','Order By Length6+ / Broken Ruler 본문·삽입 그림'], '공유한 기준 끝·증가 순서의 양쪽 조건·동률·눈금 위치/단위 간격/길이를 구별하는 자체 설계 참고다.', '수준의 양쪽보다 길다는 삽입 문구는 활동의 왼쪽보다 길고 오른쪽보다 짧다는 설명과 대조해 복사하지 않는다. 부러진 자의 끝 눈금과 길이·꺾인 경로와 직선 거리·변하지 않는 간접 기준·국내 단위를 구별하며 모든 비교/측정 능력이나 교수 효과로 확대하지 않는다.'),
 ('LT28',OBSERVATIONS[3]['standard_codes'],['Fractions의 남은8수준 본문과 이전3수준 기록','Parts of Wholes and Parts of Groups / Rainbow Arrays 본문·삽입 그림'], '같은 양/다른 모양의 등분·개수와 연속량·기준 전체와 부분의 부분·같은 전체 안의 두 방향 분할을 구별하는 자체 설계 참고다.', '분수 기호가 같다고 실제 양/단위가 같거나 등분 조각이 항상 합동인 것은 아니다. 곱의 크기는 양과 곱하는 수에 따른다.3~4학년에 곱셈/다른 분모 계산·음수/백분율 범위를 새 필수로 넣지 않고 X/÷라는 수준명만으로 나눗셈 교수 본문까지 읽었다고 하지 않는다. 원문 장식/자료 그림과 첨부/현재 학생 검증도 구별한다.'),
]

def verify():
 assert len(MAPPINGS)==len(OBSERVATIONS)==4 and len({c for m in MAPPINGS for c in m[1]})==9
 original=set(range(19));order=set(range(14));left=original-order
 assert len(order)==14 and len(left)==5 and order.isdisjoint(left) and order|left==original
 assert 33+26==59 and 30+26==56 and 59-56==3
 chart=lambda n:((n-1)%10,(n-1)//10)
 assert chart(33)==(2,3) and chart(43)==(2,4) and chart(53)==(2,5)
 route=[33,43,53]+list(range(54,60));assert route[-1]==59 and sum(b-a for a,b in zip(route,route[1:]))==26 and len(route)-1==8
 assert {a+b for a in [45,54] for b in [56,65]}=={101,110,119}
 for base,possible in [(4,True),(5,False),(6,False)]:
  x=Fraction(2**2+base**2-3**2,2*base);height_squared=4-x*x
  assert (height_squared>0)==possible
  assert x*x+height_squared==4 and (x-base)**2+height_squared==9
  if base==5:assert height_squared==0
 assert 4>2 and 4>3 and 4<2+3
 lengths=[2,4,5,7,9,11];new=8-2;positions=[i for i in range(7) if all(v<new for v in lengths[:i]) and all(v>new for v in lengths[i:])]
 assert positions==[3] and lengths[:3]+[new]+lengths[3:]==[2,4,5,6,7,9,11]
 assert len(range(2,9))==7 and len(range(2,8))==6
 cells={(x,y) for x in range(4) for y in range(3)}
 A={p for p in cells if p[1]==0 or p[0]==0};B=cells-A
 assert len(A)==len(B)==6 and A|B==cells and A.isdisjoint(B)
 perimeter=lambda region:sum((x+dx,y+dy) not in region for x,y in region for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])
 assert perimeter(A)==14 and perimeter(B)==10
 red={p for p in cells if p[0]<3};blue={p for p in cells if p[1]==0};both=red&blue
 assert (len(red),len(blue),len(both),len(cells))==(9,4,3,12)
 assert Fraction(3,4)*Fraction(1,3)==Fraction(len(both),len(cells))==Fraction(1,4)
 assert Fraction(len(both),len(red))==Fraction(1,3) and Fraction(len(both),len(blue))==Fraction(3,4)
 assert Fraction(3,4)*Fraction(1,3)<Fraction(3,4) and 2*Fraction(3,2)==3>2

def main():
 verify();registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:
  assert {m[0] for m in MAPPINGS}<={c['id'] for c in registry['claims']}
  print('LT2 listed level texts remain reviewed; no automatic refresh');build_report();return
 assert s['snapshot_file']==PRIOR_NOTES and s['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 old=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews());prior=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'))
 assert not {m[0] for m in MAPPINGS}&{v['id'] for v in registry['claims']}
 cache=ROOT/'tmp/literature/lt2-initial-level-completion'
 pages=json.loads((cache/'manifest.json').read_text(encoding='utf-8'));activities=json.loads((cache/'activity-manifest.json').read_text(encoding='utf-8'));images=json.loads((cache/'image-manifest.json').read_text(encoding='utf-8'))
 catalog=json.loads((cache/'level-catalog-manifest.json').read_text(encoding='utf-8'));followup=json.loads((cache/'activity-catalog.json').read_text(encoding='utf-8'))
 assert len(pages)==52 and len(activities)==8 and len(images)==18
 assert Counter(a['url'].split('/math/')[1].split('/')[0] for a in pages)==dict(zip(DOMAINS,[15,20,9,8]))
 assert {a['url'].split('/math-activities/')[1] for a in activities}==set(ACTIVITIES)
 assert {a['url'] for a in pages}=={u for d in prior['initial_domain_level_gap_audit']['domains'] for u in d['unread']}
 for a in pages+activities+images:
  assert a['url'].startswith(URL) and a['status']==200
  assert hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256']
  if 'final_url' in a:assert a['url']==a['final_url']
 fields=['key','url','title','sha256','status'];all_assets=prior['observed_html_assets']+[{k:a[k] for k in fields} for a in pages+activities]
 assert len(all_assets)==len({a['url'] for a in all_assets})==len({a['key'] for a in all_assets})==296
 image_fields=['page_url','url','status','sha256','dimensions','content_type']
 image_manifest=prior['image_read_manifest']+[dict(**{k:a[k] for k in image_fields},read_kind='inline_image_visual_review',redistributed=False) for a in images]
 assert len(image_manifest)==len({a['url'] for a in image_manifest})==43
 groups=copy.deepcopy(prior['read_groups']);groups['levels'] += [a['key'] for a in pages];groups['activities'] += [a['key'] for a in activities]
 assert {k:len(v) for k,v in groups.items()}==dict(general=6,domain_overviews=20,levels=224,activities=45,teacher_resources=1)
 read_urls={a['url'] for a in all_assets};level_urls={a['url'] for a in all_assets if a['key'] in groups['levels']}
 assert len(catalog)==20 and {a['url'] for a in catalog}==set(prior['catalog_recheck']['domain_urls'])
 assert level_urls=={u for a in catalog for u in a['level_urls']} and len(level_urls)==224
 for a in catalog:assert a['sha256']==next(p['sha256'] for p in all_assets if p['url']==a['url'])
 assert followup['listed_activity_urls']==len(followup['records'])==824
 assert sum(a['body_read'] for a in followup['records'])==followup['listed_body_read']==46
 assert sum(not a['body_read'] for a in followup['records'])==followup['listed_body_pending']==778
 assert not followup['selected_body_reads_not_linked_here']
 assert len({a['url'] for a in followup['records']})==824
 assert all(a['body_read']==(a['url'] in read_urls) and set(a['linked_level_urls'])<=level_urls for a in followup['records'])
 corrections=[
  dict(kind='hundreds_chart_changed_start_guard',locations=['Counting Forward and Back with the Hundreds Chart / Activity'],action='본문은33에서26을 더한다고 했지만 기록할 식은30+26으로 적혀 있다. 자체 활동은33→43→53→59로 출발량33을 유지하고33+26=59와30+26=56을 구별한다. 숫자판의 범위·행/열 배치·십과일 이동 단위를 명시한다.45와56의 주사위 예는 두 자리 순서를 바꿔도 가능한 합이101/110/119라 모두100을 넘으므로 순서 교환이 언제나 범위를 해결한다고 하지 않는다. 빼기에서도 허용 범위를 정한다.'),
  dict(kind='length_insertion_both_sides_error',locations=['Measurement: Length / Serial Orderer to6+ / Help','Order By Length6+ / Scaffolding'],action='수준 설명은 끼울 길이가 한쪽보다 길고 다른 쪽보다도 길어야 한다고 적지만,증가 순서의 중간 삽입에는 왼쪽보다 길고 오른쪽보다 짧아야 한다. 활동 본문은 이를 맞게 설명한다. 자체6cm 삽입은5<6<7과 양쪽 전체를 확인한다. 같은 길이는 동률로 보존하고 긴/짧은 방향을 섞지 않는다. 원문 파일은 수정하지 않으며 저자 정오표는 미확인이다.'),
  dict(kind='triangle_longest_side_sum_and_equality',locations=['2D Shapes / Constructor of Shapes from Parts-Exact','Measurement: Length / Abstract Length Measurer'],action='한 막대가the other two보다 길다는 표현은 각각과 비교하는지 합과 비교하는지 명시해야 한다.2·3·4는 가장 긴4가 각각보다 길어도 삼각형이 가능하고,2·3·5는 합과 같아 퇴화하며2·3·6은 불가능하다. 원문의5·7·12도 등호 경계다. 말의 의도를 임의로 확정한 정오표로 분류하지 않고 엄밀한 합 조건과 퇴화를 구별한다.'),
  dict(kind='counting_producing_and_unit_limits',locations=['Counting / Counter10,Counter and Producer10+,Counter fromN,Counter On Keeping Track,Counter Beyond100','Shopkeeper'],action='암송·있는 모임 세기·목표 수량 생산/멈춤·말한 수 개수 추적을 구별한다. Counter10과 작은 수 Producer는 병행하거나 순서가 바뀔 수 있다는 원문 제한을 보존한다. 지폐 수와 금액·목표 기억 도움·제시 범위를 기록하며 제목to10과 실제12개/10이상 예를 일률적인10개 제한으로 읽지 않는다.100이상/음수/0의 원문 범위와 국내 목표를 구별한다.'),
  dict(kind='shape_category_congruence_and_school_scope',locations=['2D Shapes / Shape Matcher,Shape Recognizer,Property Class Identifier,Congruence levels','Build Shapes / Mr. Mix Up'],action='같은 종류의 모양을 다른 크기로 맞추는 것과 합동은 다르다. 형상/각/변/대응·닫힘·일직선 중간점을 확인하고 비슷해 보이는 제작 오차와 이상적인 성질을 구별한다. 원문의 사각형 위계 포함과 다각형/각도 확장을 국내 저학년 새 필수로 전용하지 않는다. 활동별2020/2021/2026서지 표시는 원교재 판본 읽기나 효과 검증으로 합산하지 않는다.'),
  dict(kind='length_reference_path_and_unit_scope',locations=['Measurement: Length / direct,indirect,path,abstract levels','Broken Ruler'],action='직접 비교의 기준 끝·간접 비교의 변하지 않는 같은 기준·단위 반복·눈금점/간격/위치·꺾인 경로의 길이/두 끝 직선 거리를 구별한다. 부러진 자의0이 없어도 두 끝의 위치 차와 단위 간격으로 잰다. inch·파생 속력 단위·복잡한 둘레/삼각형을 국내1~2학년 새 요구로 넣지 않는다. 가상 위치 차 계산과 실제 자 측정을 구별한다.'),
  dict(kind='fraction_quantity_unit_whole_and_product',locations=['Fractions / remaining levels','Parts of Wholes and Parts of Groups','Rainbow Arrays'],action='넓이 등분은 같은 넓이를 요구하지만 항상 같은 모양을 요구하지 않는다. 대상 개수의 분수와 연속량의 분수·같은 분수 기호와 실제 양·전체와 부분을 기준으로 한 분수를 구별한다. 격자곱은 같은 전체 안의 두 방향 분할/겹침 조건에서 설명한다. 분수라는 이유만으로 항상 곱이 작아지는 것은 아니며 원문의 X/÷수준 본문은 곱셈만 명시해 나눗셈 교수 전체 검토로 확대하지 않는다.'),
  dict(kind='level_text_completion_not_all_materials',locations=['20영역 개요와224수준 목록·선정8활동/18그림'],action='남은52수준 본문은 이제 읽었지만 전체 사이트/활동을 읽은 것은 아니다.224수준의 링크를 전수 대조해 활동/교사자료824개 중46개 본문 읽기·778개 목록 확인만으로 구별했다. 새18그림에는 사진·자료 아이콘·인쇄물 표지가 섞여 있고 Rainbow 사진은 장식 무지개다. 표지·사진으로 첨부 퍼즐/학생 응답/전략/단계/시각 상태/효과를 판정하지 않는다.'),
 ]
 p=ROOT/'data/sources.json';bibliography=json.loads(p.read_text(encoding='utf-8'));b=next(v for v in bibliography if v['id']==SOURCE);previous_b=copy.deepcopy(b)
 b.update(review_scope=SCOPE,next_review='현재20개 개요와 목록224개 수준 본문 읽기 대기는0개다. 수준에 연결된 활동/교사자료824개 중46개 본문을 읽었고778개는 링크 목록만 확인했다. 남은 활동의 수학적 조건·발문/자료 불일치·표현/그림을 우선 대조한다. 누적43삽입 그림 외의 그림·영상·첨부PDF·게임·인용 원연구/교재·정오표와 실제 한국어 과제 반응·진단 정확도·효과는 별도다.')
 image_log=[
  '1579215838678:가게 놀이 사진에서 지폐가 보이지만 금액/교환 단위·개별 수행을 판정하지 않는다.',
  '1747948923899:동물/사람/차 자료 이미지이며 전체 수나 실제 주문 결과가 아니다.',
  '1750697446153:1단위10장·5단위2장·10단위1장 자료 아이콘은 지폐13장과 금액30의 차이를 보여 주며 국내 화폐 규준으로 쓰지 않는다.',
  '1743450846125:1~100숫자판 미리보기이며10열 배치를 확인했지만 첨부 전체/실제 출력 크기는 미검토다.',
  '1768499558112:그리기 도구 아이콘이며 숫자판 결과가 아니다.',
  '1770766044693:미술 활동 사진이며33+26의 실제 숫자판 수행이나 반응 자료가 아니다.',
  '1578521666691:막대 구성 활동 사진이며 각 길이·직각·학생의 독립 전략을 판정하지 않는다.',
  '1748635335366:삼각형 형태의 빨대 자료 아이콘이며 모든 길이 조합의 구성 가능성을 보장하지 않는다.',
  '1628021379809:그림을 그리는 사진에 오각형/육각형이 보이며 같은 도형 둘의 합동 검증 자료가 아니다.',
  '1730171042668:인형 자료 아이콘이며 오답/학생 반응이 아니다.',
  '1730171112341:자/각도기 도구 아이콘이며 실제 측정값이나 정확도 자료가 아니다.',
  '1730171152832:여러 도형 조각 자료 이미지이며 개별 모양의 정밀 치수/합동을 전사하지 않는다.',
  '1580237994588:같은 밑선에서 높아지는 다섯 블록 탑 사진이다. 원근 길이를cm값으로 전사하거나6~10개 대상 전체 수행의 증거로 삼지 않는다.',
  '1615904248312:자와 조각을 사용하는 사진이며 양 끝 눈금/측정값·독립 수행을 읽을 수 없다.',
  '1732917593268:종이/메모 도구 아이콘이며 측정 결과가 아니다.',
  '1788386175705:Broken Ruler 인쇄물 표지이며 첨부 전체의 눈금/해답을 검토한 것으로 세지 않는다.',
  '1598456314004:사각형/원과 방향을 바꾼 사각형에서 네 칸 중 한 칸을 칠한 예와 빈 틀을 확인했다. 대상 모임의 모든 예를 대신하지 않는다.',
  '1618413650809:무지개 장식 사진이며3/4×1/3배열 그림이나 학생 결과가 아니다.',
 ]
 updates=dict(zip(ACTIVITIES,['2026-04-07','2026-03-10','2025-07-01','2025-07-01','2025-07-23','2026-09-21','2025-07-27','2025-07-28']))
 log=['남은52수준 본문 전부를 읽었다. 세기15·평면도형20·길이9·분수8개이며 이전172개와 합해 현재 목록224개다. 수준 설명·텍스트 예·교수 도움·활동 목록을 포함하되 원본 영상/첨부는 포함하지 않는다.', '선정8활동의 영어 목표·절차·팁·자료·차별화·표시 참고문헌과 삽입 그림18개를 읽었다. 도구 출력에서 잘린Order By Length의 절차는 별도로 전체를 다시 출력해 누락 없이 읽었다.', '20개 개요에 연결된 수준URL을 원본HTML에서 다시 추출해224개 읽기URL과 전수 비교했다.224수준의 활동/교사자료 링크는824개 고유URL이고46개 읽기·778개 목록만 확인으로 구별했다.', '이전236개HTML에52수준·8활동을 더해296개이며 삽입 그림은25+18=43개다. URL/그림 수는 독립 단계·연구·학생 수가 아니다. 기존 홈페이지 기준HTML 해시·모든 이전 주장/관찰·읽기 기록을 보존한다.']
 coverage=dict(domain_overviews_read=20,listed_level_urls=224,read_level_urls=224,unread_level_urls=0,listed_activity_urls=824,read_activity_bodies=46,pending_activity_bodies=778,interpretation='현재 공개 목록의URL별 범위다. 수준 본문 읽기와 모든 활동/자산 읽기는 다르다.')
 notes=dict(source_id=SOURCE,source_url=URL,source_asset_kind='publisher_html',source_asset_sha256=s['source_asset_sha256'],source_asset_redistributed=False,contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,date='2026-11-06',reviewer='Codex',read_scope=SCOPE,previous_review=copy.deepcopy(s),previous_bibliography=previous_b,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,observed_html_assets=all_assets,html_read_manifest=all_assets,image_read_manifest=image_manifest,image_reading_log=prior['image_reading_log']+image_log,read_groups=groups,new_read_groups=dict(domain_overviews=0,levels=52,activities=8,teacher_resources=0),reading_log=prior['reading_log']+log,source_corrections=prior['source_corrections']+corrections,activity_update_dates={**prior['activity_update_dates'],**updates},catalog_recheck=prior['catalog_recheck'],crosslisted_level_groups=prior['crosslisted_level_groups'],initial_domain_level_gap_audit_history=prior['initial_domain_level_gap_audit'],completed_initial_domain_level_urls=sorted(a['url'] for a in pages),level_catalog_manifest=catalog,activity_followup_catalog=followup,catalog_coverage=coverage,unread_followups=[b['next_review'],'남은778개 활동/교사자료 본문은 아직 읽지 않았다. 링크 목록·자료 아이콘·사진·인쇄물 표지를 원문 첨부 전체나 실제 학생 검증으로 바꾸지 않는다.'])
 npath=ROOT/NOTES;npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=s['date'],read_scope=s['read_scope'])]
 s.update(date='2026-11-06',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),snapshot_history=history,bibliography_snapshot=digest(b),html_read_manifest=all_assets,image_read_manifest=image_manifest,read_scope=SCOPE,method_note='남은52수준·선정8활동·삽입 그림18개를 읽어 현재20개 개요/224수준 본문을 모두 대조했다. 활동/교사자료824개 링크를 전수 대조하되46개 본문 읽기와778개 목록 확인만으로 구분하고 이전 근거를 보존한다.',limits='누적296개 지정 영어 본문과 삽입 그림43개다. 현재 공개 목록의224수준 본문은 모두 읽었으나778활동/교사자료 본문·미선정 그림·영상·첨부PDF·게임·원연구·교재 전권은 미검토다.0–8세 자원을 국내 학년 전체·현재 효과·진단 규준·유일한 경로로 사용하지 않는다. 본문/식의 출발값·삽입 순서·길이 합/퇴화·기준 전체/단위/합동과 교수 범위를 구별한다.',editorial_action='기존 주장24건·자체 관찰24건을 보존하고9개 기준에 새 주장4건·자체 관찰4건을 추가했다. 누적47개 기준·주장28건·관찰28건이며 관계 검토·독립 검토·학생 검증으로 합산하지 않는다.',observations=s['observations']+OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 assert len({c for v in registry['claims'] if v['source_id']==SOURCE for c in v['standard_codes']})==47
 p.write_text(json.dumps(bibliography,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'data/content_review_queue.json';q=json.loads(p.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE]);p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])]==old['claims'] and s['observations'][:24]==old['sources'][SOURCE]['observations']
 assert all(registry['sources'][k]==v for k,v in old['sources'].items() if k!=SOURCE) and load_reviews()==relations
 build_report();print('Completed listed224 LT2 level texts:60 new HTML bodies,18 new images,4 claims,4 own probes;778 linked activity bodies pending')

if __name__=='__main__':main()

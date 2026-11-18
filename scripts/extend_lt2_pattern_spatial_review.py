"""Extend LT2 subitizing, patterns and spatial text/image evidence with explicit gaps."""
import copy
import hashlib
import json
from collections import Counter
from itertools import combinations
from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews
from record_lt2_public_review import SOURCE, URL
from extend_lt2_shape_composition_review import NOTES as PRIOR_NOTES

NOTES='data/literature_evidence/CLEMENTS_SARAMA_LT_pattern_spatial_review_notes.json'
PRIOR_SHA='f7a0634cc05fc8b8cfcef2a04e911350a30e2bacb4a605180fc0db2e076994f0'
DOMAINS=['subitizing','patterns-structure-and-algebraic-thinking','spatial-orientation','spatial-visualization-and-imagery']
ACTIVITIES=['snapshots-conceptual-subitizer-to-10','dice-race-conceptual-subitizer-with-multiplicative-thinking','pattern-strips-pattern-translator-and-unit-recognizer','function-train','introductory-barrier-game','coordinate-game--coordinate-plotter','picture-it-then-turn-turn-turn','building-with-the-minds-eye-mental-mover']
SCOPE='공식 공개HTML 누적236개 지정 영어 본문: 일반6·영역 개요20·수준172·활동37·교사자료1. 수량 즉지·규칙/구조/대수·공간 방향·공간 시각화의 새4개 개요·공개40수준·선정8활동을 추가했다. 별도 삽입 그림은 기존8개와 새17개를 합한25개다. 현재20개 개요는 모두 읽었으나 전체 수준/활동 검토 완료가 아니다. 초기4영역의 미검토 수준52개를 링크 목록으로만 확인했고 본문 읽기로 세지 않았다. 나머지 그림·영상·첨부PDF·게임·원연구는 미대조다.'
OBSERVATIONS=[
 dict(id='LT-P20',standard_codes=['2수01-01','2수01-04','2수01-10'],question='교사는 같은 크기의 점9개를 세 줄에3개씩 놓은 카드와,같은9개를5개 부분/4개 부분으로 나눈 카드를 준비한다. 먼저 한 카드를 짧게 보여 주고 전체 개수의 최초 반응을 기록한다. 그 뒤 카드를 다시 보여 주며 어떤 부분을 보았는지 설명하거나 가리키게 한다. 다른 카드에서도 전체와 부분을 구별하고,필요하면 점을 하나씩 세어 확인하라.',expected='두 카드 모두 점9개다. 첫 카드에서는3+3+3 또는3개씩3묶음으로9를 볼 수 있고,다른 카드에서는5+4로9를 볼 수 있다. 부분을 나눈 방식은 달라도 점을 더하거나 빼지 않아 전체가 같다.3개씩3묶음이라는 곱셈 설명에서는 한 묶음의 점 수와 묶음 수를 구별한다. 다른 올바른 분해나 직접 세기로 확인한 응답도 원래 방법대로 기록한다.',interpretation='자체 점 배열이며 원문 카드/주사위나 실제 학생 반응의 복사가 아니다. 개념적 수량 파악에서는 전체를 먼저 답한 뒤 부분의 설명을 확인한다. 지각적 수량 파악의 순간 반응을 볼 때 같은 설명 요구를 미리 주어 전략을 바꾸지 않는다.2초 또는 빠른 반응을 한국 학생의 진단 기준으로 쓰지 않고 실제 노출 시간·시야·크기·대비·소통 방식·도움을 기록한다. 빠른 정답만으로 비계수/묶음 전략을 추정하지 않으며,말하기가 어려워도 가리키기·조작·수 카드로 따로 확인한다. 한9개 과제의 성공은100까지 세기·모든20 이하 조합·곱셈 전체 숙달을 증명하지 않는다.',student_validated=False),
 dict(id='LT-P21',standard_codes=['2수02-01','2수02-02'],question='빨강·빨강·파랑을 세 번 반복한9개 배열을 준비한다. 이 묶음을 계속 반복하기로 약속했을 때 가장 짧은 반복 묶음을 표시하고,동그라미·동그라미·세모 또는두 번 두드리기·한 번 박수로 같은 구조를 만들어라. 약속을 알려 주지 않고 앞의9개만 보여 주었다면 다음 항은 반드시 하나로 정해지는가?',expected='정한 반복 규칙의 가장 짧은 묶음은빨강·빨강·파랑,즉AAB다. 종류가2개라는 이유로 반복 길이가2가 되는 것은 아니다. 표현을 바꾸어도 두A 다음 한B라는 순서를 보존한다. AAB를 계속 반복하기로 약속했다면10번째는A다. 그러나 앞9개만으로 모든 가능한 규칙을 하나로 확정할 수 없다. 예를 들어AABAABAABB라는10개 묶음을 반복하는 규칙도 처음9개는 같지만10번째는B다.',interpretation='자체 배열이며 원문 AB사진을 복사한 것이 아니다. 시작 위치·읽는 방향·허용한 재료·정한 규칙과실제 배열을 대조한다. 세 번의 완전한 반복을 보여 주는 교수 지침과 유한 예만으로 수학적 유일성이 보장된다는 주장을 구별한다. 손가락/구분자 도움 뒤의 단위 찾기와 스스로 만든 배열을 따로 기록한다. 알파벳 표기는 교사용 구조 이름으로 쓸 수 있고 저학년의 영어 문자 읽기를 수학 이해의 선행 관문으로 요구하지 않는다. 다음 색 맞히기만으로 가장 짧은 단위 인식·다른 재료로의 번역을 모두 확인했다고 하지 않는다.',student_validated=False),
 dict(id='LT-P22',standard_codes=['4수02-03','6수02-01'],question='3~4학년에서는9+빈칸=10+6의 양쪽 양을 같게 하는 수를 계산 또는 보상으로 설명한다.5~6학년의 별도 상황:처음 객차0개이고 정차할 때마다 객차2개씩을 붙이며 기관차는 세지 않는다. 정차0·1·2·3회에 대응하는 객차 수를 표로 만들고6회일 때와 대응식을 설명하라. 기관차도1대로 센다는 조건으로 바꾸면6회 뒤 세는 대상의 수는 같은가?',expected='빈칸은7이며9에서10으로1이 늘어난 만큼 다른 더하는 수는7에서6으로1이 줄어 합16이 같다. 열차는 정차0·1·2·3회에 객차0·2·4·6개가 대응하고,6회에는12개다. 정차 수를□,객차 수를△라 하면□×2=△다. 단지 표의 다음 행을 이어 쓰는 것과 같은 행의 두 양을 대응시키는 것은 다르다. 기관차1대를 포함하면6회 뒤 전체 차량은13대이고,객차12개라는 답과 세는 대상이 다르다.',interpretation='자체 수치/열차 조건이다. 표 몇 줄만으로 모든 가능한 대응식을 확정하지 않고 처음0개·정차당2개 추가·제거 없음·기관차 제외 조건을 사용한다. 국내5~6학년의 한 연산으로 나타내는 간단한 관계는객차 수의□×2=△로 대응한다. 기관차를 더한13대 비교는 조건 변화 확인용이며두 연산의 일반식이나영문 변수 함수 기호를 새 필수로 요구하지 않는다. 등호를 계산 진행 화살표로 쓰지 않고 양쪽 전체 값을 비교한다. 실제 장난감 조작과 가상 표 계산·최초 설명과 교사/짝 도움 뒤 설명을 구별하며 원문 사진의 차량 수에서 정차 이력을 역추정하지 않는다.',student_validated=False),
 dict(id='LT-P23',standard_codes=['2수03-02','4수03-05'],question='1~2학년에서는 모형의 앞을 화살표로 고정하고 파란 블록의 오른쪽에 노란 블록,파란 블록의 위에 빨간 블록을 연결한3개 모형을 설명하고 재현한다. 처음에는 두 사람이 같은 방향을 보게 하고,이후 마주 앉아도 ‘모형의 오른쪽’과‘내 오른쪽’이 같은지 비교한다.3~4학년에서는 종이에 고정한 오른쪽/위쪽 화살표를 기준으로 점P에서 오른쪽3칸·위쪽2칸 이동한 점을 찾고,같은 길을 거꾸로 돌아오는 방법을 설명하라.',expected='모형에서 노란 블록은 파란 블록의 정한 오른쪽,빨간 블록은 위에 있다. 관찰자가 반대편으로 가도 모형의 연결은 같고 자기 몸 기준의 좌우 표현이 달라질 수 있다. 점의 같은 경로를 거꾸로 가려면 도착점에서 아래2칸·왼쪽3칸 이동한다. 오른쪽3칸은 출발점을 포함한 격자점4개를 만나는3번의 이동이며 출발점을 첫 이동으로 세지 않는다. 왼쪽3칸·아래2칸도 같은 출발점에는 오지만 원래 지나온 길의 정확한 역순은 아니다.',interpretation='자체 모형/격자 활동이며 블록의 크기·공유한 앞 방향·종이 방향·출발점·칸 간격·설명 순서·가림막과 도움을 기록한다. 원문 좌표 활동의축교점이라는 표현을 모든 격자점이 x축/y축 자체의 교점이라는 뜻으로 옮기지 않는다. 두 축 자체는 원점에서만 만나며 일반 위치는 각 좌표를 지나는 축과 평행한 선들의 교점으로 정한다. 좌표식은 교사용 검산에만 쓰고 국내3~4학년에 형식적 순서쌍·좌표평면이나 꼭짓점 이동으로 도형 변환을 설명하는 새 요구를 넣지 않는다. 듣기·기억·소통/운동 접근과 수학적 위치 이해를 한 번의 재현 실패로 동일시하지 않는다.',student_validated=False),
 dict(id='LT-P24',standard_codes=['4수03-04','6수03-01'],question='교사는 같은 정사각형 칸4개로 세로3칸과 맨아래칸 오른쪽1칸이 붙은ㄴ 모양을 만든다. 맨아래 왼쪽칸 중심을O로 정하고 맨위칸의 양면에 같은 점표식을 두거나 투명 조각을 쓴다. 조각을 움직이기 전에①O를 중심으로 시계방향 직각 한 번 돌릴 때와②O를 지나는 세로선을 기준으로 뒤집을 때의 모양과 표식 위치를 각각 예상한다. 그 뒤 실제 조작이나 투명 종이로 확인하고 예상과 달라진 부분을 설명하라.',expected='①돌리면 세로로 올라간3칸이O에서 오른쪽으로 뻗고,원래 오른쪽 한 칸은O 아래로 간다. 맨위 표식은O에서 오른쪽2칸 위치로 간다.②세로선으로 뒤집으면 세로3칸은 같은 위치에 있고,아래 오른쪽 한 칸은왼쪽으로 간다. 맨위 표식은 그대로다. 두 움직임은 다른 결과지만 각 결과는 원래 조각과 모양·크기가 같아 겹쳐 볼 수 있다. 위치나 향하는 방향이 다르다는 사실을 크기 변화나 합동이 아님으로 결론 내리지 않는다.',interpretation='자체 네 칸 조각이며 회전 중심·방향·양·반사 기준과 표식을 명시한다.3~4학년은 조작 변화와 예상을 보고,5~6학년은 대응하는 칸/점과 합동을 확인한다. 교사용 좌표 변환 공식·임의 각도 회전 계산을 새 요구로 넣지 않는다. 실제로 옮겨 맞춘 결과를 처음부터 머릿속으로 예상했다고 소급하지 않고,관찰 시간·모델 제시·언어 지시·짝 도움·수정 전후를 따로 기록한다. 선대칭과 회전대칭도 같은 성질이 아니며 색/표식이 없는 대칭 조각의 우연히 같은 외형만으로 뒤집기와 돌리기를 구별했다고 하지 않는다. 한 조작 성공으로 원문의 모든 방향/양을 예상하는 단계나 진단 효과를 확정하지 않는다.',student_validated=False),
]
MAPPINGS=[
 ('LT20',OBSERVATIONS[0]['standard_codes'],['Subitizing 개요와 공개12수준 본문','Snapshots [Conceptual Subitizer to 10] / Dice Race [Conceptual Subitizer with Multiplicative Thinking] 본문·삽입 그림'], '전체를 먼저 파악한 반응과 부분 설명·직접 세기·같은 크기 묶음의 역할을 나누어 기록하는 자체 수량 활동 설계에 참고한다.', '짧은 노출·빠른 정답·말하기만으로 비계수 전략이나 수량 이해 전체를 판정하지 않는다. 원문의 최상 효과 표현·연령/정확도 수치·단계 이름을 현재 한국 학생 규준/인과 효과로 쓰지 않으며 자료 아이콘·주사위 표지의 점 수를 실제 과제/첨부 전체 검증으로 합산하지 않는다.'),
 ('LT21',OBSERVATIONS[1]['standard_codes'],['Patterns, Structure, and Algebraic Thinking 개요와 Intuitive Patterner~Pattern Translator/Unit Recognizer 본문','Pattern Strips [Pattern Translator and Unit Recognizer] 본문·삽입 그림'], '반복의 가장 짧은 단위·시작/방향·다른 재료로의 구조 번역과 유한 배열에서의 규칙 선택을 구별하는 자체 설계 참고다.', '세 번 완전 반복은 교수 지침이며 모든 유한 배열의 다음 항이 유일하다는 정리가 아니다. 종류의 수와 단위 길이·다음 항과 단위 설명·성인 구분자 도움과 독립 수행을 구별하며 반복 패턴 예측의 연관성을 현재 수업의 인과 효과로 바꾸지 않는다.'),
 ('LT22',OBSERVATIONS[2]['standard_codes'],['Patterns, Structure, and Algebraic Thinking / Numeric Patterner~Functional Algebraic Thinker 본문','Function Train 본문·삽입 사진'], '각 열의 증가와 같은 행 두 양의 대응·초기값/변화 조건·세는 대상·등호 양쪽 값의 보상을 구별하는 자체 설계 참고다.', '처음 객차 수와 정차당 증가·기관차 포함 여부가 같아야 같은 관계다. 단편 표나 사진만으로 보편식을 확정하지 않는다. 영문 변수·함수 용어·두 연산으로 된 기관차 포함 일반식을 국내 초등의 새 필수로 적용하지 않고 외부 원연구/현재 과제 효과로 집계하지 않는다.'),
 ('LT23',OBSERVATIONS[3]['standard_codes'],['Spatial Orientation 개요와 공개10수준 본문','Introductory Barrier Game / Coordinate Game [Coordinate Plotter] 본문·삽입 사진'], '모형/관찰자 기준의 방향·공유 관점·점의 이동량/지나간 점·같은 도착과 같은 경로를 구별하는 자체 설계 참고다.', '축 자체의 교점과 각 좌표의 평행선 교점을 구별한다. 유아 지도의 좌표/지도 범위를 국내3~4학년의 형식적 좌표평면이나 점 이동을 통한 도형 변환의 새 필수로 옮기지 않는다. 가림막·언어/기억/운동·도움 조건을 통제하지 않은 실패를 공간 이해 부재로 확정하지 않는다.'),
 ('LT24',OBSERVATIONS[4]['standard_codes'],['Spatial Visualization and Imagery 개요와 공개7수준 본문','Picture It, Then Turn, Turn, Turn / Building with the Mind\'s Eye [Mental Mover] 본문·삽입 그림'], '실제 이동 전의 예상·이동 종류/기준/양·표식의 대응과 합동·도움 뒤 수행을 구별하는 자체 설계 참고다.', '퍼즐 완성·단계별 말 지시 따라 만들기를 모든 정신적 이동의 사전 예측으로 바꾸지 않는다. 선대칭·회전대칭·반복 선형 패턴은 서로 다르며 모양이 대칭이라는 이유로 서로 다른 움직임의 이해가 검증되지 않는다. 임의 각도 공식·원문 첨부 퍼즐 전체·현재 교수 효과/단계 진단은 미확인이다.'),
]

def verify():
 assert len(MAPPINGS)==len(OBSERVATIONS)==5 and len({c for m in MAPPINGS for c in m[1]})==11
 dots={(x,y) for x in range(3) for y in range(3)}
 rows=[{p for p in dots if p[1]==y} for y in range(3)]
 cross={p for p in dots if p[0]==1 or p[1]==1};corners=dots-cross
 assert len(dots)==9 and [len(x) for x in rows]==[3,3,3]
 assert len(cross)==5 and len(corners)==4 and cross.isdisjoint(corners) and cross|corners==dots
 assert set.union(*rows)==dots and sum(map(len,rows))==9
 seq='AAB'*3
 periods=[p for p in range(1,len(seq)+1) if all(seq[i]==seq[i%p] for i in range(len(seq)))]
 assert min(periods)==3
 other=('AAB'*3+'B')*3
 assert seq==other[:9] and ('AAB'*4)[9]=='A' and other[9]=='B'
 shapes={'A':'circle','B':'triangle'}
 assert [shapes[x] for x in seq]==['circle','circle','triangle']*3
 carts=[0]
 for n in range(1,7):carts.append(carts[-1]+2)
 assert carts==[2*n for n in range(7)] and carts[6]==12 and carts[6]+1==13
 assert [n for n in range(100) if 9+n==10+6]==[7]
 alternative=lambda n:2*n if n<=3 else 2*n+1
 assert all(alternative(n)==carts[n] for n in range(4)) and alternative(6)!=carts[6]
 cubes={'blue':(0,0,0),'yellow':(1,0,0),'red':(0,0,1)}
 opposite=lambda p:(-p[0],-p[1],p[2])
 assert opposite(cubes['yellow'])==(-1,0,0) and opposite(cubes['red'])==(0,0,1)
 path=[(1,1),(2,1),(3,1),(4,1),(4,2),(4,3)]
 back=[(4,3),(4,2),(4,1),(3,1),(2,1),(1,1)]
 assert back==list(reversed(path)) and len(path)-1==5
 different=[(4,3),(3,3),(2,3),(1,3),(1,2),(1,1)]
 assert different[-1]==back[-1] and different!=back
 L={(0,0),(0,1),(0,2),(1,0)};turn=lambda p:(p[1],-p[0]);flip=lambda p:(-p[0],p[1])
 assert {turn(p) for p in L}=={(0,0),(1,0),(2,0),(0,-1)}
 assert {flip(p) for p in L}=={(0,0),(0,1),(0,2),(-1,0)}
 assert turn((0,2))==(2,0) and flip((0,2))==(0,2)
 distance=lambda p,q:sum((a-b)**2 for a,b in zip(p,q))
 for transform in [turn,flip]:
  assert all(distance(p,q)==distance(transform(p),transform(q)) for p,q in combinations(L,2))
 assert all(turn(turn(turn(turn(p))))==flip(flip(p))==p for p in L)

def main():
 verify();registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:
  assert {m[0] for m in MAPPINGS}<={c['id'] for c in registry['claims']}
  print('LT2 pattern/spatial extension remains current; no automatic refresh');build_report();return
 assert s['snapshot_file']==PRIOR_NOTES and s['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 old=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews());prior=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'))
 assert not {m[0] for m in MAPPINGS}&{v['id'] for v in registry['claims']}
 cache=ROOT/'tmp/literature/lt2-pattern-spatial'
 pages=json.loads((cache/'manifest.json').read_text(encoding='utf-8'));activities=json.loads((cache/'activity-manifest.json').read_text(encoding='utf-8'));images=json.loads((cache/'image-manifest.json').read_text(encoding='utf-8'))
 gap=json.loads((ROOT/'tmp/literature/lt2-initial-domain-gap-audit/gap-audit.json').read_text(encoding='utf-8'))
 assert len(pages)==44 and len(activities)==8 and len(images)==17
 levels=[a for a in pages if '/math/learning-trajectories/' not in a['url']]
 assert Counter(a['url'].split('/math/')[1].split('/')[0] for a in levels)==dict(zip(DOMAINS,[12,11,10,7]))
 assert {a['url'].split('/math-activities/')[1] for a in activities}==set(ACTIVITIES)
 for a in pages+activities+images:
  assert a['url'].startswith(URL) and a['status']==200
  assert hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256']
  if 'final_url' in a:assert a['url']==a['final_url']
 fields=['key','url','title','sha256','status']
 all_assets=prior['observed_html_assets']+[{k:a[k] for k in fields} for a in pages+activities]
 assert len(all_assets)==len({a['url'] for a in all_assets})==len({a['key'] for a in all_assets})==236
 image_fields=['page_url','url','status','sha256','dimensions','content_type']
 new_images=[dict(**{k:a[k] for k in image_fields},read_kind='inline_image_visual_review',redistributed=False) for a in images]
 image_manifest=prior['image_read_manifest']+new_images
 assert len(image_manifest)==len({a['url'] for a in image_manifest})==25
 groups=copy.deepcopy(prior['read_groups'])
 groups['domain_overviews'] += [a['key'] for a in pages if '/math/learning-trajectories/' in a['url']]
 groups['levels'] += [a['key'] for a in levels];groups['activities'] += [a['key'] for a in activities]
 assert {k:len(v) for k,v in groups.items()}==dict(general=6,domain_overviews=20,levels=172,activities=37,teacher_resources=1)
 assert gap['unread_levels']==52 and [len(x['unread']) for x in gap['domains']]==[15,20,9,8]
 read_urls={a['url'] for a in all_assets};unread_urls={u for x in gap['domains'] for u in x['unread']}
 assert len(unread_urls)==52 and not unread_urls&read_urls
 assert all(x['overview']['sha256']==x['previous_overview_sha256'] and x['audit_kind']=='link_catalog_only_not_level_body_reading' for x in gap['domains'])
 assert {a['url'] for a in all_assets if a['key'] in groups['domain_overviews']}==set(prior['catalog_recheck']['domain_urls'])
 read_level_urls={a['url'] for a in all_assets if a['key'] in groups['levels']}
 assert len(read_level_urls)==172 and len(read_level_urls|unread_urls)==224
 corrections=[
  dict(kind='subitizing_response_protocol_not_strategy_proof',locations=['Subitizing / perceptual and conceptual levels','Snapshots [Conceptual Subitizer to 10]','Dice Race [Conceptual Subitizer with Multiplicative Thinking]'],action='지각적 즉지와 개념적 부분/전체 설명의 요청 순서를 구별한다. 개념적 즉지는 전체를 먼저 답하고 부분을 나중에 설명하게 하며 첫 반응 전에 부분을 알려 주지 않는다.2초 이하/2~3초 제시·10~30초 기록·재노출·선택지·짝 설명·경쟁 점수는 서로 다른 조건이다. 빠른 정답/게임 승리만으로 세지 않았거나 모든 조합을 안다고 추정하지 않는다. Snapshots의5~10 목표와 절차의 최대7개 문구도 실제 제시 범위를 기록해 구별한다.'),
  dict(kind='site_assertion_age_and_causality_limits',locations=['Subitizing / Practice-based Research,Very Small Number Recognizer','Patterns overview'],action='가장 효과적이라는 사이트 서술과 연령별 개월/정확도 수치,다른 능력을 통제한 패턴의 예측 관계를 현재 한국 학생의 진단 규준·이 활동의 인과 효과·모든 방법보다 우수함의 직접 증거로 사용하지 않는다. 원연구를 새로 읽거나 재분석한 것이 아니며언어 산출과 수량 파악·한 예의 성공과 전체 수준을 구별한다.'),
  dict(kind='pattern_core_unit_and_finite_prefix',locations=['Patterns overview,Patterner AB,Pattern Translator and Unit Recognizer','Pattern Strips'],action='세 번의 완전 반복은 반복 단위 파악을 돕는 지침이며 유한 접두열의 미래가 논리적으로 유일하다는 뜻이 아니다. 고정한 시작/방향·허용 재료·최소 단위·선택한 규칙을 명시한다. Pattern Translator 페이지 본문의Abstract Patterner라는 다른 이름도 별도 단계로 중복 집계하지 않는다.'),
  dict(kind='equality_and_function_initial_value_scope',locations=['Patterns / Beginning Arithmetic Patterner~Functional Algebraic Thinker','Function Train'],action='각 열이2씩 늘어난다는 관찰과 정차/객차의 같은 행 대응을 구별한다. 처음 객차 수·정차당2개 추가·기관차 포함 여부가 식을 결정한다. 표 몇 줄이나 장난감 사진만으로 전 범위 식을 확정하지 않는다. 교환/결합의 성질을 뺄셈에 무조건 전용하지 않으며 국내 단일 연산 관계 범위와 기관차 포함의 추가 연산 비교를 구별한다.'),
  dict(kind='coordinate_axes_and_reference_frame_guard',locations=['Spatial Orientation / Coordinate Plotter,Map User,framework levels','Coordinate Game [Coordinate Plotter]','Introductory Barrier Game'],action='x축/y축 자체는 원점 한 곳에서 만나므로 일반 좌표를 축들의 다른 교점으로 설명하지 않는다. 각 좌표를 지나는 축과 평행한 선의 교점·원점·단위·순서·점과칸을 구별한다. 가림막 활동은 처음에 나란히 앉아 같은 관점을 공유하는 조건이 있다. 자료10개와 절차7개는 가용 재료/사용량으로 구별할 수 있어 곧바로 계산 오류로 단정하지 않는다. 자체 활동의 사용량은 명시한다.'),
  dict(kind='mental_prediction_task_and_help_boundaries',locations=['Spatial Visualization / Simple Slider and Turner~Mental Mover','Picture It, Then Turn, Turn, Turn','Building with the Mind\'s Eye [Mental Mover]'],action='퍼즐의 시행착오 완성과 단계별 언어 지시 재현을 모든 이동의 사전 심상 예측으로 해석하지 않는다. 조작 전에 예상한 것·실제 이동·재질문·모델을 보며 따라 하기·여러 지시를 기억해 재현한 것을 구별한다. 활동의 단계 링크가 보편적 선수성이나 한국 학년의 필수 경로를 입증하지 않는다.'),
  dict(kind='geometric_motion_and_symmetry_scope',locations=['Spatial Visualization / motion and Practice-based Research'],action='밀기/뒤집기/돌리기의 종류와 방향·양·중심/기준선을 명시한다. 선대칭·회전대칭·줄의 반복 패턴은 다르며 일반 평행사변형의 회전대칭을 곧 선대칭이라고 하지 않는다. 작은 표식·부분 대응을 추적하며 대각선/임의각도 예를 국내 새 공식 계산 요구로 전용하지 않는다. 위치 변화와 모양/크기 보존도 구별한다.'),
  dict(kind='image_previews_updates_and_unread_assets',locations=['선정8활동의17삽입 그림·Last updated·References'],action='새17개에는 자료 사진·아이콘·인쇄물/주사위 표지·활동 사진이 섞여 있다. 표지 점10개·자료 아이콘100개 표시·사진의2객차를 실제 검사 문항이나 첨부 전체/정차 이력의 검증으로 사용하지 않는다. Pattern Strips의2026-11-03 등 갱신일과2015/2016/2021/2026서지는 페이지 표기로 보존하며 해당 교재/원연구 읽기와 구별한다. 사진에서 개별 학생 단계·독립 수행·시각 상태·현재 효과를 추정하지 않는다.'),
 ]
 p=ROOT/'data/sources.json';bibliography=json.loads(p.read_text(encoding='utf-8'));b=next(v for v in bibliography if v['id']==SOURCE);previous_b=copy.deepcopy(b)
 b.update(review_scope=SCOPE,next_review='현재20개 개요는 모두 읽었고 공개 수준224개URL 중172개 본문을 읽었다. 초기4영역의 남은52개(세기15·평면도형20·길이9·분수8) 본문과 모든 영역의 미선정 활동을 우선 대조한다. 목록/해시 확인을 해당 수준 본문 읽기로 세지 않는다. 누적25삽입 그림 외의 그림·영상·첨부PDF·게임·인용 원연구/교재·정오표와 실제 한국어 과제 반응·진단 정확도·효과는 별도다.')
 image_log=[
  '1721848071876:겹친 빨간 카운터의 자료 이미지다. 가려진 조각을 포함한 정확한 수나 학생 반응 자료로 사용하지 않는다.',
  '1744417549134:천/덮개 자료 사진이며 과제 수행이나 노출 시간의 증거가 아니다.',
  '1753996649530:Paper Plates 아이콘으로 실제 점 배열 문항이 아니다.',
  '1753998293230:Snapshots 인쇄물 표지에10개 점이 보이지만 첨부PDF의 모든 배열/난도를 읽은 것으로 세지 않는다.',
  '1758141619019:가린 점판을 보여 주는 활동 사진이다. 개별 응답·2초 노출·사용한 전략이나 효과를 판정하지 않는다.',
  '1755555245472:Cloth or Paper 아이콘이며 수량 문항이나 결과가 아니다.',
  '1791861277257:Custom Dice 표지/아이콘이며 그려진 주사위의 일부 면만 보인다. 실제 주사위 자료의 모든 면을 검증하지 않았다.',
  '1791861365713:Challenge Set 표지는 유사한 주사위 그림이지만 다른 자산이다. 추가 난도/모든 면 배열을 그 표지로 확정하지 않는다.',
  '1687288184618:노란 육각형/빨간 사다리꼴의AB 세 번과 다른 재료의AB 세 번을 대조했다. 자체AAB 배열의 사진으로 사용하지 않는다.',
  '1732917532740:Up to5 different colors/shape/type 자료 이미지의5는 전체 물체5개를 뜻하는 실측값이 아니다.',
  '1748636743610:막대 자료 아이콘에10묶음/100총수가 표시돼 있으나 실제 과제의 개수/묶음 이해를 확인한 자료가 아니다.',
  '1617385315874:기관차1대와 객차2개가 보이는 장난감 사진이다. 한 정차의 실행/정차당 항상2개 추가/초기값을 그 사진만으로 확정하지 않는다.',
  '1566312706783:두 학생과 가림막·타일 구성 사진이다. 독립 설명/재현 성공·정확한 대화/도움 조건을 사진에서 판정하지 않는다.',
  '1580248345944:격자와 연결 블록을 조작하는 사진이다. 축/원점의 세부 표시가 충분히 읽히지 않아 수치 좌표를 전사하거나 일반 점의 축 교점이라고 하지 않는다.',
  '1580851434100:Pattern Block Puzzle8표시와 내부 선/패턴 블록 조작이 보인다.8~13전체 퍼즐/해답·이동 전 예상을 검증한 것은 아니다.',
  '1596473072884:여러 색 연결 큐브의 자료 사진이며 본문의 지시대로 학생이 완성한 구조의 결과가 아니다.',
  '1744668205347:흩어진 연결 큐브 자료 사진이다. 총수/공간 단계/원활한 소통을 판정하지 않는다.',
 ]
 updates=dict(zip(ACTIVITIES,['2025-09-18','2026-10-15','2026-11-03','2025-07-16','2025-07-29','2026-02-25','2025-07-25','2025-07-24']))
 log=[
  '새4개 개요·공개40수준의 설명·텍스트 예·교수 도움·활동 목록을 읽었다. 수량 즉지12·규칙/구조/대수11·공간 방향10·공간 시각화7개다. 선정8활동의 영어 목표·절차·팁·자료·차별화·표시 참고문헌과 삽입 그림17개를 실제 대조했다.',
  '이전184개HTML에 새52개를 더해236개다. 그림은 기존8개와 새17개를 합한25개이며 HTML/독립 단계/연구 수에 합산하지 않는다. 반복되는 영어/스페인어 표제 부분과 같은 이미지URL은 한 번만 센다.',
  '현재20개 영역 개요를 모두 읽었지만 전체 수준 검토가 아니다. 초기4개 개요HTML은 기존 해시와 같음을 재확인하고 수준 목록만 대조했다. 남은52개URL의 본문은 읽지 않았으며 세기15·평면도형20·길이9·분수8개로 후속 목록에 유지한다.',
  '기존 홈페이지 기준HTML 해시·모든 이전 주장/관찰·읽기 기록을 보존한다. 원본 첨부PDF·수준 영상·게임·교재/인용 원연구는 읽거나 실행한 것으로 확대하지 않는다.',
 ]
 notes=dict(source_id=SOURCE,source_url=URL,source_asset_kind='publisher_html',source_asset_sha256=s['source_asset_sha256'],source_asset_redistributed=False,contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,date='2026-11-06',reviewer='Codex',read_scope=SCOPE,previous_review=copy.deepcopy(s),previous_bibliography=previous_b,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,observed_html_assets=all_assets,html_read_manifest=all_assets,image_read_manifest=image_manifest,image_reading_log=prior['image_reading_log']+image_log,read_groups=groups,new_read_groups=dict(domain_overviews=4,levels=40,activities=8,teacher_resources=0),reading_log=prior['reading_log']+log,source_corrections=prior['source_corrections']+corrections,activity_update_dates={**prior['activity_update_dates'],**updates},catalog_recheck=prior['catalog_recheck'],crosslisted_level_groups=prior['crosslisted_level_groups'],initial_domain_level_gap_audit=gap,catalog_coverage=dict(domain_overviews_read=20,listed_level_urls=224,read_level_urls=172,unread_level_urls=52,interpretation='URL별 페이지 수이며 독립 단계/연구 수가 아니다. 링크 목록 확인은 본문 읽기가 아니다.'),unread_followups=[b['next_review'],'자체 점/규칙/열차/모형/표식 활동은 원문 문항/사진/실제 학생 응답의 복사가 아니다. 사진·자료 아이콘·인쇄물 표지는 원문 첨부 전체나 실제 수행 검증을 대신하지 않는다.'])
 npath=ROOT/NOTES;npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=s['date'],read_scope=s['read_scope'])]
 s.update(date='2026-11-06',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),snapshot_history=history,bibliography_snapshot=digest(b),html_read_manifest=all_assets,image_read_manifest=image_manifest,read_scope=SCOPE,observations=s['observations']+OBSERVATIONS)
 s.update(method_note='기존184개HTML에 수량 즉지·규칙/구조·공간 방향·공간 시각화의 개요4·수준40·활동8을 더하고 삽입 그림17개를 시각 대조했다.최소 반복 단위/유한 접두열·등호/두 양 대응·기준 방향/좌표·이동 전 예상/이후 조작의 조건을 구별한다.',limits='누적236개 지정 영어 본문과 삽입 그림25개다.20개 개요는 모두 읽었으나 공개 수준224개 중52개 본문과미선정활동/자산은미검토다.0–8세자원을국내학년전체·현재효과·진단규준·유일한경로로쓰지않는다.말하기/반응속도·사진/자료아이콘·퍼즐완성만으로전략·단계·교수효과를판정하지않으며형식적좌표·임의각도공식·기관차포함두연산일반식을새필수로요구하지않는다.',editorial_action='기존주장19건·자체 관찰19건을보존하고11개기준에새주장5건·자체관찰5건을추가했다.누적44개기준·주장24건·관찰24건이며관계검토·독립검토·학생검증으로합산하지않는다.')
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 assert len({c for v in registry['claims'] if v['source_id']==SOURCE for c in v['standard_codes']})==44
 p.write_text(json.dumps(bibliography,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'data/content_review_queue.json';q=json.loads(p.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE]);p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])]==old['claims'] and s['observations'][:19]==old['sources'][SOURCE]['observations']
 assert all(registry['sources'][k]==v for k,v in old['sources'].items() if k!=SOURCE) and load_reviews()==relations
 build_report();print('Extended LT2:52 new public HTML bodies,17 new inline images,5 claims,5 own observations;52 level bodies still unread')

if __name__=='__main__':main()

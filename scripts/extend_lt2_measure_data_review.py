"""Extend four LT2 domains using public English text; preserve prior scoped evidence."""
import copy,hashlib,json
from collections import Counter
from fractions import Fraction
from literature_review import ROOT,digest,target_value,load_registry,build_report
from relation_analysis_review import load_reviews
from record_lt2_public_review import SOURCE,URL,NOTES as PRIOR_NOTES,GROUPS as PRIOR_GROUPS

NOTES='data/literature_evidence/CLEMENTS_SARAMA_LT_measure_data_review_notes.json'
PRIOR_SHA='296a8e86696950f7b74da637b69c632d52ddb5ba6737bad91c58cf969e4b7916'
DOMAINS=['measurement-area','measurement-volume','measurement-angle-and-turn','classification-and-data-analysis']
ACTIVITIES=['measure-areas','creating-grids','how-many-blocks-fit-in-the-box','water-volume-play','angle-measuring','researcher-note--angle-misconceptions-angle-measurer','our-data','shape-matrices-multiple-attribute-classifier']
SCOPE='공식 공개HTML 누적73개 지정 영어 본문: 일반6·영역 개요8·수준45·활동13·교사자료1. 새4영역의 공개 수준 설명33개 전부와 선정8개 활동/교사자료를 추가했다. 원본 그림·영상·첨부PDF·게임·인용 원연구는 미대조다.'
OBSERVATIONS=[
 dict(id='LT-P7',standard_codes=['6수03-12','6수03-13'],question='가로6cm·세로4cm인 같은 직사각형을 빈틈·겹침 없이 덮는다. 한 변1cm인 정사각형과 한 변2cm인 정사각형으로 각각 덮을 때 필요한 조각 수와 넓이를 설명하라. 조각 수가 줄면 원래 넓이도 줄어드는가?',expected='1cm² 조각은 한 줄6개씩4줄로24개다. 한 변2cm인 조각은 넓이가4cm²여서 한 줄3개씩2줄로6개이며 전체는6×4=24cm²다. 같은 영역을 덮었으므로 넓이는 같다. 길이 단위가2배인 정사각형의 넓이는4배여서 필요한 조각 수는4분의1이다. 둘레의 길이나 가로·세로의 합을 넓이로 쓰지 않는다.',interpretation='자체 수치의 가상 활동이다. 단위의 변 길이·넓이·조각 수·행/열 수를 구별하고 두 방향을 맞추어 덮었는지 확인한다. 더 큰 조각으로 정확히 덮이는 조건을 명시했으며 어떤 모양에서도 항상 조각 수가 정수로 나눈다고 일반화하지 않는다. 도식 도움·직접 덮기·반복 덧셈·곱셈 중 사용한 방법을 기록하고 수준 이름이나 공식 답 하나로 현재 학생의 단계를 판정하지 않는다.',student_validated=False),
 dict(id='LT-P8',standard_codes=['6수03-09','6수03-18','6수03-19'],question='안쪽의 가로·세로·높이가 모두6cm인 공간을 한 변2cm인 정육면체로 빈틈·겹침 없이 꽉 채운다. 한 층의 개수와 층 수·전체 개수·cm³로 나타낸 부피를 설명하라. 겉에 있는 블록26개나 드러난 작은 정사각형 면54개를 전체 블록 수로 써도 되는가?',expected='각 방향3개씩이므로 한 층9개·3층·전체27개다. 각 큰 블록은1cm³ 정육면체8개와 같은 부피여서 전체216cm³이며6×6×6과 같다. 한 층9개에 층 수3을 한 번 곱한다. 한가운데 숨은 블록1개를 포함해27개이고 겉 블록26개·노출 단위 면54개·합쳐진 정육면체의 면6개는 서로 다른 수다.',interpretation='꽉 채웠다는 조건과 안쪽 치수·동일한 단위·숨은 자리·한 층을 기록한다. 표면 모습만으로 내부가 채워졌다고 추정하지 않는다. 한 줄·한 층·전체의 단위를 섞어 높이나 층 수를 두 번 곱하지 않는다. 바깥 치수로 용량을 계산하거나 같은 부피면 어떤 선물도 들어간다고 결론 내리지 않는다. 자체 모형이며 실제 채우기·학생 반응·유아 자료의 한국 고학년 효과를 검증한 것은 아니다.',student_validated=False),
 dict(id='LT-P9',standard_codes=['4수03-02','4수03-24'],question='종이의 직각 모서리를 두 방향이 정확히 겹치도록 반으로 접어 각A를 만든다. 같은 모양을 돌려 놓고 두 변을 방향 그대로 길게 그린 각B를 만든다. 각도기로 재기 전에 두 각의 크기를 어림해 기록하고,측정한 뒤 접기·포개기로 확인하라. 변을 길게 그리거나 돌리면 각도 커지는가?',expected='직각90°를 같은 크기로 나눈 각이므로 A와B는 모두45°인 예각이다. 모형 전체를 돌리거나 변을 같은 방향으로 연장해도 두 반직선의 벌어짐은 유지된다. 각도기 중심을 꼭짓점에 맞추고 한 변의0에서 시작하는 눈금을 읽는다.135°를 읽었다면 직각보다 작다는 어림과 비교해 시작 눈금과 읽는 방향을 다시 확인한다.',interpretation='학생에게 답45°를 먼저 알려 주지 않고 어림·도구 배치·눈금 읽기·설명을 각각 기록한다. 실제로 만든 접은 각의 정확성과 각도기 배치도 확인하며 종이 제작 오차를 학생의 개념 결손으로 단정하지 않는다. 미리 준 수치의 계산과 실제 각도 측정은 구별한다. 원문의360°각도기·270°회전·거북이 예를 국내3~4학년의 새 필수 범위로 넣지 않고 실제 학생 수행이나 원문 영상 검증으로 집계하지 않는다.',student_validated=False),
 dict(id='LT-P10',standard_codes=['2수04-01','2수04-02'],question='가상 카드6장은 빨간 삼각형2장·빨간 원2장·파란 삼각형2장이다. 먼저 색으로 분류하고,다음에는 색과 모양을 함께 쓴 표에 한 장씩 넣어라. 빨간 카드4장과 삼각형 카드4장을 더해 카드가8장이라고 해도 되는가?',expected='색만으로 나누면 빨강4장·파랑2장으로 합6장이다. 두 기준의 표는 빨간 삼각형2·빨간 원2·파란 삼각형2·파란 원0이고 합6장이다. 빨강과 삼각형을 함께 만족하는2장을 두 목록에서 다시 셌으므로4+4를 서로 겹치지 않는 범주들의 합으로 사용할 수 없다. 같은 모양의 카드도 서로 다른 두 장이면 원기록 두 개를 보존한다.',interpretation='분류 기준·카드 한 장의 기록·겹치는 목록과 중복 없는 표의 칸을 구별한다.0장은 이 가상 모임에 없다는 뜻이며 무응답을 임의로0으로 만든 것이 아니다. 학생에게 집합 공식·정식 행렬 연산·사각형 포함 관계·평균이나 확률 공식을 새 필수로 요구하지 않고 각 카드를 직접 추적해 설명하게 한다. 이 기록은 실제 선호 조사나 현재 학생 응답이 아니다.',student_validated=False),
 dict(id='LT-P11',standard_codes=['4수03-17','4수03-18'],question='높고 좁은 용기A와 낮고 넓은 용기B를 실제로 비교할 때 먼저 어느 쪽의 들이가 더 클지 예상해 기록한다. 다음 가상 기록은 예상 뒤에 따로 제시한다:비운 용기에 매번250mL를 정확히 채운 같은 컵으로 물을 넣어 정한 가득 참 기준까지 A는4번,B는6번이 들었다. 들이를 L와mL로 표현하고,높이나 채운 시간만으로 같은 결론을 내려도 되는지 설명하라.',expected='가상 기록에서 A는1000mL=1L,B는1500mL=1L500mL여서 B의 들이가500mL 더 크다. 키가 더 높은 A가 더 많이 담는다고 할 수 없다. 현재 들어 있는 물의 양과 용기 전체의 들이는 다르며,한 번씩 같은250mL를 넣고 흘림·잔류·채움 기준을 확인해야 한다. 채운 시간은 유량 등이 달라지면 들이의 직접 비교값이 아니다.',interpretation='실제 용기와 측정 전 예상을 제공/수집한 경우와 가상 기록의 계산을 구별한다. 눈금컵 단위·간격·수평·눈높이·단위 양의 일정함·가득 참 기준·흘림과 도움을 기록한다. 가상 수치로 실제 측정 수행을 확인했다고 하지 않고,같은 양을 다른 모양 용기에 옮길 때의 물 높이 변화도 양의 증가로 단정하지 않는다. 미국 단위나1mL=1cm³ 관계를 이 활동의 새 필수로 요구하지 않는다.',student_validated=False)]
MAPPINGS=[
 ('LT07',OBSERVATIONS[0]['standard_codes'],['Measurement: Area 개요와 공개8수준 본문','Measure Areas / Creating Grids 영어 본문'],'같은 단위의 완전 덮기·행과 열·단위 크기와 조각 수를 구별해 넓이의 곱셈 구조를 설명하는 자체 설계에 참고한다.','수준 이름을 정확한 개수 세기·현재 한국 학생의 단계·필수 경로의 검증으로 쓰지 않는다.0–8세 자원에 있는 배열 설명을 고학년 넓이 단위 전체의 효과로 확대하지 않으며 같은 개수라도 단위 넓이가 다르면 같은 넓이라고 하지 않는다.'),
 ('LT08',OBSERVATIONS[1]['standard_codes'],['Measurement: Volume 개요와 공개8수준 본문','How Many Blocks Fit In The Box? / Water Volume Play 영어 본문'],'같은 단위로 채우는 양·한 줄/한 층/전체·숨은 블록·단위 부피와 개수를 구별하는 자체 설계에 참고한다.','원문3D설명의 넓이 용어와 한 줄/전체 예시의 불명확한 높이 반복을 그대로 옮기지 않는다. 어림·수면 높이·채우는 시간·다른 블록 수만으로 정확한 용량을 확정하지 않으며 동일 단위·안쪽 치수·빈틈 없는 채움 조건을 확인한다. 현재 학생 효과나 한국 고학년의 보편적 발달 순서 근거가 아니다.'),
 ('LT09',OBSERVATIONS[2]['standard_codes'],['Measurement: Angle and Turn 개요와 공개6수준 본문','Angle Measuring / Researcher Note - Angle Misconceptions [Angle Measurer] 영어 본문'],'변 길이·방향과 각의 크기를 구별하고,꼭짓점·시작0선·측정 방향과 측정 전 어림을 관찰하는 자체 설계에 참고한다.','원문에 제시된 학생 비율을 현재 집단의 진단 규준으로 쓰지 않는다. 원문의360°각도기·270°회전 예와 국내 각 측정 범위를 구별하고 방향·시작선·어느 각인지 없이 회전량과 내각을 같은 값으로 단정하지 않는다. 도구 도움 뒤 성공을 독립 측정의 증거로 바꾸지 않는다.'),
 ('LT10',OBSERVATIONS[3]['standard_codes'],['Classification and Data Analysis 개요와 공개11수준 본문','Our Data / Shape Matrices [Multiple Attribute Classifier] 영어 본문'],'원기록의 개별 대상·분류 기준·동시 속성·중복 없는 표의 칸과 집계 전체를 구별하는 자체 설계에 참고한다.','두 속성에 속한다는 이유로 원기록 수를 늘리거나 비슷한 값을 한 기록으로 합치지 않는다. 원문 수준의 평균·확률·행렬·위계 포함을 국내1~2학년의 새 필수로 적용하지 않는다. 원문의11/23은 반 미만이며 최다·거의 반·과반수를 구별하고 현재 조사·학생 효과 자료로 쓰지 않는다.'),
 ('LT11',OBSERVATIONS[4]['standard_codes'],['Measurement: Volume / Volume Filler,Volume Unit Relater and Repeater','Water Volume Play 영어 본문'],'용기 전체가 담는 양·현재 담긴 양·같은 단위의 반복과 측정 전 예상/측정 뒤 확인을 구별하는 들이 활동 설계에 참고한다.','가상 기록 계산·물 높이·채우는 시간은 실제 들이 측정 수행이나 정확한 용량을 대신하지 않는다. 동일한 단위 양·같은 채움 기준·흘림/잔류·도구 읽기를 확인하고 현재 한국 학생의 교수 효과·진단 규준으로 확대하지 않는다.')]

def verify():
 assert len(MAPPINGS)==len(OBSERVATIONS)==5
 assert len({c for m in MAPPINGS for c in m[1]})==11
 assert 6*4==24 and (6//2)*(4//2)==6 and 6*2**2==24
 cubes={(x,y,z) for x in range(3) for y in range(3) for z in range(3)}
 boundary={p for p in cubes if any(v in [0,2] for v in p)}
 exposed=sum((x+dx,y+dy,z+dz) not in cubes for x,y,z in cubes for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)])
 assert len(cubes)==27 and len(boundary)==26 and exposed==54 and len(cubes-boundary)==1
 assert 3*3==9 and 9*3==27 and 27*2**3==6**3==216 and 27*3!=27
 assert Fraction(90,2)==45 and 180-45==135
 # Rotation and positive scaling preserve the angle between (1,0) and (1,1).
 dot=lambda a,b:sum(x*y for x,y in zip(a,b))
 cos_squared=lambda a,b:Fraction(dot(a,b)**2,dot(a,a)*dot(b,b))
 assert cos_squared((1,0),(1,1))==cos_squared((0,5),(-5,5))==Fraction(1,2)
 assert dot((1,0),(1,1))>0 and dot((0,5),(-5,5))>0
 cards=[('red','triangle'),('red','triangle'),('red','circle'),('red','circle'),('blue','triangle'),('blue','triangle')]
 cells=Counter(cards);assert [cells[c] for c in [('red','triangle'),('red','circle'),('blue','triangle'),('blue','circle')]]==[2,2,2,0]
 assert sum(cells.values())==6 and sum(c=='red' for c,s in cards)==sum(s=='triangle' for c,s in cards)==4
 assert Fraction(11,23)<Fraction(1,2)
 assert 4*250==1000 and 6*250==1500 and 1500-1000==500

def main():
 verify();registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:
  assert {m[0] for m in MAPPINGS}<={c['id'] for c in registry['claims']}
  print('LT2 measurement/data extension remains current; no automatic refresh');build_report();return
 assert s['snapshot_file']==PRIOR_NOTES and s['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 old=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews());prior=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'))
 assert not {m[0] for m in MAPPINGS}&{v['id'] for v in registry['claims']}
 cache=ROOT/'tmp/literature/lt2-measure-data';pages=json.loads((cache/'manifest.json').read_text(encoding='utf-8'));activities=json.loads((cache/'activity-manifest.json').read_text(encoding='utf-8'));catalog=json.loads((cache/'catalog-recheck.json').read_text(encoding='utf-8'))
 assert len(pages)==37 and len(activities)==8 and len(catalog['domain_urls'])==20
 assert len([a for a in pages if '/math/learning-trajectories/' in a['url']])==4
 assert {a['url'].split('/math-activities/')[1] for a in activities}==set(ACTIVITIES)
 for a in pages+activities+[catalog]:
  assert a['url'].startswith(URL) and a['url']==a['final_url'] and a['status']==200
  assert hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256']
 fields=['key','url','title','sha256','status'];new_assets=[{k:a[k] for k in fields} for a in pages+activities];all_assets=prior['observed_html_assets']+new_assets
 assert len(all_assets)==len({a['url'] for a in all_assets})==73
 groups=copy.deepcopy(PRIOR_GROUPS);groups['domain_overviews'] += [a['key'] for a in pages if '/math/learning-trajectories/' in a['url']];groups['levels'] += [a['key'] for a in pages if '/math/learning-trajectories/' not in a['url']]
 groups['activities'] += [a['key'] for a in activities if 'researcher-note--' not in a['url']];groups['teacher_resources']=[a['key'] for a in activities if 'researcher-note--' in a['url']]
 assert {k:len(v) for k,v in groups.items()}==dict(general=6,domain_overviews=8,levels=45,activities=13,teacher_resources=1)
 log=['새4영역 개요·공개33수준 본문과 선정7활동/1교사자료의 영어 목표·절차·교수 팁·자료·차별화·표시 참고문헌을 읽었다. 영역별 수준은 넓이8·부피8·각6·분류/자료11이다. 목록만 확인한 활동은 읽기 수에 넣지 않았다.',
 '기존28개URL에 새45개URL을 더해 누적73개 지정 영어 본문이다. 기존 일반6·개요4·수준12·활동6의 기록과 주장은 보존했다. 다른 원문 버전과 현재 원고의 추가 대응을 혼합하지 않는다.',
 '현재 공개 목록을 다시 확인해 영역20개 중 개요를 읽은8개와 남은12개를 구별했다. 재확인한 목록은 기존URL의 추가 스냅샷이며 새URL 수에 중복 합산하지 않았다.',
 '기존 홈페이지HTML의 해시는 기준 자산 한 파일로 유지한다. 새45개HTML과 목록 재확인 파일은 각각의 주소·해시로 기록하며 홈페이지 해시를 전체 사이트 해시로 쓰지 않는다.',
 '원본 그림·영상·첨부PDF·게임 실행과 인용 원논문/교재는 대조하지 않았다. 영어 본문이 스페인어 표제 아래에도 반복되는 부분은 독립 번역 검토나 별도 활동으로 집계하지 않는다.']
 corrections=[
  dict(kind='volume_dimension_word_guard',locations=['Measurement: Volume / 3D Array Structurer'],action='세 방향 정육면체 반복을 설명하는 본문에 area가 섞여 있으나 이어지는 문장과V=l*w*h는 부피다. 현재 원고에서는 세는 대상·단위cm³와 한 층/전체를 구별하고 넓이라고 복사하지 않는다.'),
  dict(kind='volume_layer_double_count_guard',locations=['Measurement: Volume / 3D Row and Column Structurer / Other Examples'],action='가로·세로·높이를 곱한 것을 한 줄의 개수라고 부른 뒤 층 수를 다시 곱하는 것으로 읽히는 예가 있다. 본문의 한 층 개수×층 수와 대조해 높이를 두 번 곱하지 않는다. 자체 예는3×3=9개/층,3층이27개이며27×3이 아니다. 원문 저자의 수정 의도나 정오표는 확인 전이다.'),
  dict(kind='measurement_conditions_guard',locations=['Measurement: Area / Area Unit Relater and Repeater','How Many Blocks Fit In The Box?','Water Volume Play'],action='동일 개수는 같은 단위·빈틈 없는 덮기/채움 조건에서만 같은 측정값이다. 일반 상자는 단위 블록이 남김없이 들어맞는지 확인한다. 물 높이·채우기/비우기 시간은 용기 형태·유량·출구 등에 영향을 받으므로 용량과 같다고 하지 않는다. 서로 다른 재료의 빈틈·다짐도 구별한다. 부피만으로 특정 선물의 세 치수가 들어맞는다고 하지 않는다.'),
  dict(kind='angle_context_and_school_scope',locations=['Measurement: Angle and Turn / Angle Measurer','Angle Measuring','Researcher Note - Angle Misconceptions [Angle Measurer]'],action='270°회전 뒤 두 반직선 사이의 작은 각90°를 말하는 예는 시작 방향·회전 방향·어느 각인지가 필요하다. 모든 회전량/내각/외각의 동일성으로 전용하지 않는다.360°각도기와 각 오개념의 학생 비율을 국내3~4학년 필수 범위나 현재 진단 규준으로 옮기지 않는다.'),
  dict(kind='case_unit_and_category_overlap_guard',locations=['Classification and Data Analysis / Data Case Viewer,Data Classifier,Data Aggregator,Hierarchical Classifier','Our Data','Shape Matrices [Multiple Attribute Classifier]'],action='비슷한 값을 같은 범주로 묶어도 원기록 개수를 지우지 않는다. 대상·응답·속성의 단위를 정하고 겹치는 속성 목록과 중복 없는 분류표를 구별한다.11/23은 반 미만이며 최다·거의 반·과반수를 같은 말로 쓰지 않는다. 원문의 행렬/평균/확률/위계 포함을 국내1~2학년 새 필수로 요구하지 않는다.'),
  dict(kind='activity_version_and_progression_limits',locations=['활동8개 / Last updated와References','Complete Coverer and Counter','Simple Sorter'],action='갱신일은2025/2026으로 다르고 참고문헌도2·3·4판 및2020/2021/2026을 다르게 표시한다. 페이지의 표기를 기록했으며 해당 책의 전권/판본을 직접 검토했다고 하지 않는다. Complete Coverer도 개수 중복/누락이 가능하고 Simple Sorter는 성인 도움이 포함된다. 이름·한 번의 성공·도움 뒤 수행을 검증된 학생 단계로 판정하지 않는다.')]
 p=ROOT/'data/sources.json';bibliography=json.loads(p.read_text(encoding='utf-8'));b=next(v for v in bibliography if v['id']==SOURCE);previous_b=copy.deepcopy(b)
 b.update(review_scope=SCOPE,next_review='현재 공개20영역 중 미검토12영역과 기존/신규 영역의 미선정 수준·활동을 후속 대조한다. 원본 그림·영상·첨부PDF·게임·인용 원연구/교재·수치/서지의 정오표와 현재 한국어 과제의 실제 반응·진단 정확도·교수 효과는 별도다. 새4영역의 공개33수준 본문 읽기와 모든 활동/전체 사이트 검토를 구별한다.')
 updates={'measure-areas':'2025-07-29','creating-grids':'2025-07-29','how-many-blocks-fit-in-the-box':'2025-07-16','water-volume-play':'2025-07-24','angle-measuring':'2025-07-28','researcher-note--angle-misconceptions-angle-measurer':'2026-09-10','our-data':'2026-02-04','shape-matrices-multiple-attribute-classifier':'2026-02-04'}
 notes=dict(source_id=SOURCE,source_url=URL,source_asset_kind='publisher_html',source_asset_sha256=s['source_asset_sha256'],source_asset_redistributed=False,contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,date='2026-11-06',reviewer='Codex',read_scope=SCOPE,previous_review=copy.deepcopy(s),previous_bibliography=previous_b,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,observed_html_assets=all_assets,html_read_manifest=all_assets,read_groups=groups,new_read_groups=dict(domain_overviews=4,levels=33,activities=7,teacher_resources=1),reading_log=prior['reading_log']+log,source_corrections=prior['source_corrections']+corrections,activity_update_dates={**prior['activity_update_dates'],**updates},catalog_recheck={k:catalog[k] for k in fields+['domain_urls']},unread_followups=[b['next_review'],'목록과 첨부 링크의 존재는 그 내용의 읽기·도구 실행·현재 학생 검증을 뜻하지 않는다. 자체 수치·카드·접기 활동은 원문 문항/영상/학생 자료의 복사가 아니다.'])
 npath=ROOT/NOTES;npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=s['date'],read_scope=s['read_scope'])]
 s.update(date='2026-11-06',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),snapshot_history=history,bibliography_snapshot=digest(b),html_read_manifest=all_assets,read_scope=SCOPE,method_note='기존4영역의 선정 범위에 넓이·부피·각/회전·분류/자료의 개요와 공개33수준 본문·선정8활동/교사자료를 더했다. 실제 읽은 페이지별 주소·해시와 기존 기록을 보존하며 목록·원연구·교재 전권의 검증과 구별한다.',limits='누적73개 지정 영어 본문이다.0–8세 자원을 국내 학년 전체·현재 과제 효과·진단 규준·유일한 경로로 사용하지 않는다. 새4영역의 수준 설명은 모두 읽었지만 모든 활동이나20영역 전체를 읽은 것이 아니다. 원본 그림·영상·첨부PDF·게임·원연구·교재 전권·번역 동등성은 미대조다. 부피의 용어/예시와 각의 회전 조건,자료 수/범주의 겹침을 자체 검산하고 의심 표현을 복사하지 않는다.',editorial_action='기존11개 기준의 주장6건·자체 관찰6건을 보존하고 새11개 기준에 주장5건·자체 관찰5건을 추가했다. 누적22개 기준·주장11건·관찰11건이며 신규 관계 검토·독립 검토·학생 검증으로 합산하지 않는다.',observations=s['observations']+OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 p.write_text(json.dumps(bibliography,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'data/content_review_queue.json';q=json.loads(p.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE]);p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])]==old['claims'] and s['observations'][:6]==old['sources'][SOURCE]['observations']
 assert all(registry['sources'][k]==v for k,v in old['sources'].items() if k!=SOURCE) and load_reviews()==relations
 build_report();print('Extended LT2:45 new public HTML bodies,5 claims,5 own observations; prior claims/history preserved')

if __name__=='__main__':main()

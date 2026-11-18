"""Review LT2 solid shapes, composition and disembedding with bounded image QA."""
import copy
import hashlib
import json
from collections import Counter
from itertools import combinations, product
from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews
from record_lt2_public_review import SOURCE, URL
from extend_lt2_number_operations_review import NOTES as PRIOR_NOTES

NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_shape_composition_review_notes.json'
PRIOR_SHA = '801c165d5984ed6d59d52bae21e931f715115c6dc930032a881c645994be9af7'
DOMAINS = ['3d-shapes','composing-2d-shapes','composing-3d-shapes','disembedding-shapes']
ACTIVITIES = ['toothpick-builder','making-boxes-3d-shape-identifier','can-you-find-another-way','super-shape-shape-decomposer-with-imagery','build-a-block','find-another-way','find-the-figure','whats-the-smallest-shape-on-the-geoboard-stemie']
SCOPE = '공식 공개HTML 누적184개 지정 영어 본문: 일반6·영역 개요16·수준132·활동29·교사자료1. 입체도형·평면 합성·입체 합성·숨은 도형 찾기의 새4개 개요·공개32수준 본문·선정8활동을 추가했다. 별도로 해당8활동의 서로 다른 삽입 그림8개를 시각 대조했다. 그림 수를 HTML/독립 단계/연구 수에 합산하지 않는다. 나머지 원본 그림·영상·첨부PDF·게임·인용 원연구는 미대조다.'
OBSERVATIONS = [
 dict(id='LT-P16',standard_codes=['2수03-01','6수03-03','6수03-05'],question='낮은 학년에서는 상자 전체와 손으로 짚은 한 면의 모양을 구별하고 상자를 돌려 다시 확인한다.5~6학년의 별도 질문:정확한 정육면체 모형의 면·모서리·꼭짓점을 표시하며 세어라. 면마다 모서리4개씩을 세어24개라고 해도 되는가? 정사각형 한 밑면과 한 꼭짓점으로 모이는 삼각형 옆면4개인 모형은 삼각기둥인가?',expected='상자 전체의 입체 모양과 한 면의 평면 모양은 다르며 돌려도 그 관계는 유지된다. 정확한 정육면체는 면6·모서리12·꼭짓점8개다. 각 모서리가 두 면에 공유되어 면별로 센24에는 같은 모서리가 두 번씩 들어 있다. 정사각형 밑면과 삼각형 옆면4개가 한 꼭짓점에 모이는 것은 사각뿔이다. 삼각기둥은 평행하고 합동인 삼각형 밑면2개와 직사각형 옆면3개이며 면5·모서리9·꼭짓점6개다. 사각뿔은 면5·모서리8·꼭짓점5개로 면 수만 같다고 같은 입체가 아니다.',interpretation='정육면체가 정확히 구성됐다는 조건 아래 요소의 공유와 숨은 부분을 확인하는 자체 활동이다. 막대12개·연결점8개나 직사각형 면6개라는 수만으로 정육면체가 보장되지 않으며 모서리 길이·직각·면 연결을 확인한다. 실제 막대를 면마다 중복 사용한 재료 수와 기하적 모서리 수도 다르다. 사각뿔/삼각기둥의 비교는5~6학년 범위의 모형 관찰이며 각뿔 전개도 제작을 요구하지 않는다.1~2학년에는 형식적 요소 개수·각기둥/각뿔 명칭·사각형 포함 관계를 새 필수로 넣지 않는다. 사진의 완성품만으로 실제 학생의 독립 구성과 설명을 확인했다고 하지 않는다.',student_validated=False),
 dict(id='LT-P17',standard_codes=['2수03-03','4수03-04','4수03-12'],question='교사가 정사각형 종이를 한 대각선으로 잘라 만든 똑같은 직각이등변삼각형 조각2개를 제공한다. 먼저 두 조각으로 원래 정사각형을 복원하고,다음에는 같은 조각으로 더 큰 삼각형 모양을 만들어 보라. 한 조각에 점을 표시해 밀기·돌리기·뒤집기에서 점과 변의 위치를 추적한다. 두 조각을 썼다는 사실만으로 같은 외형이거나 빈틈 없이 채웠다고 해도 되는가?',expected='두 조각의 긴 변을 맞추면 원래 정사각형을 복원할 수 있다. 짧은 변을 맞추고 다른 짧은 두 변이 한 직선을 이루게 놓으면 더 큰 삼각형을 만들 수 있다. 조각을 모두 한 번씩 겹침 없이 사용했으므로 종이 전체의 양은 같지만 바깥 경계는 사각형과 삼각형으로 다르다. 정해진 윤곽을 채우는 과제라면 조각의 수·변 길이뿐 아니라 각·방향·윤곽 안의 빈틈·겹침을 확인해야 한다. 밀기·돌리기·뒤집기는 조각의 크기를 늘이거나 줄이지 않는다.',interpretation='자체 절단/합성 활동이며 교사가 자른 선과 실제 조각의 정확성을 확인한다.2수03-03에서는 모양 찾기/구성을,3~4학년에서는 이동과 채우기/설명을 관찰한다. 대각선·직각이등변삼각형은 교사용 제작 설명이며 저학년 학생의 용어 암기를 전제하지 않는다. 아무 두 직각삼각형이나 정사각형이 되는 것은 아니며 이 활동의 합동·같은 길이 조건을 보존한다. 원문의 종이 자르기 활동은 별도 규칙의 과제여서 현재의 주어진 조각을 자르지 않는 채우기 과제에 절단을 몰래 허용하지 않는다. 어림/계획과 실제 조작·시행착오·도움 뒤 설명을 구별하고 모든 학생에게 여러 전략을 동시에 요구하지 않는다.',student_validated=False),
 dict(id='LT-P18',standard_codes=['2수03-02','6수03-09','6수03-19'],question='같은 공간인2cm×2cm×2cm 정육면체를 빈틈·겹침 없이 채운다.①한 변1cm 정육면체,②2cm×1cm×1cm 블록,③2cm×2cm×1cm 판 모양 블록으로 각각 몇 조각이 필요한가? 모두 한 변1cm 정육면체의 양으로 세면 얼마인가? 같은8개의 단위 정육면체를1cm×2cm×4cm로 쌓아도 원래 정육면체와 같은 모양인가?',expected='각각8개·4개·2개 조각으로 채울 수 있다.①의 한 층4개·두 층은8개다.②의 한 조각은 단위 정육면체2개,③의 한 조각은4개와 같아서 각각 전체8개분,부피8cm³다. 물리적 조각 수와 단위 정육면체의 수는 다르다.1×2×4도 부피8cm³지만 세 방향 길이가2·2·2와 달라 같은 공간을 그대로 대체하는 모양은 아니다. 같은 부피만으로 같은 외형·같은 치수의 빈자리 적합성을 결론 내릴 수 없다.',interpretation='교사가 정확한 치수의 모형을 제공하거나 해당 치수를 가정한 가상 과제로 구별해 기록한다.1~2학년은 블록의 위/옆 위치와 간단한 구성 설명을 보고,단위 정육면체 환산·부피 계산은5~6학년에서 확인한다. 같은 단위·모든 블록의 사용·내부 빈 공간 없음·방향과 세 치수·접촉면을 명시한다. 바닥/벽을 만드는 확장을 원문이1차원/2차원 구조라 부르더라도 실제 블록의 두께가0이라는 뜻은 아니다. 외곽 그림에 층 선이나 대각선이 있다는 것만으로 숨은 내부가 꽉 찼다고 확정하지 않는다. 현재 학생의 직접 쌓기 수행이나 효과 자료가 아니다.',student_validated=False),
 dict(id='LT-P19',standard_codes=['2수03-04','4수03-12'],question='교사는 아래왼쪽부터 반시계방향으로A·B·C·D라 이름 붙인 정사각형을 준비한다. 아래 변AB와 위 변DC의 가운데에 각각E·F를 표시하고,EF와 대각선AC를 그어 교점을O라 둔다. 먼저 단순한 모양에서 닫힌 삼각형과 끝이 벌어진 세 선을 구별한다. 확장 그림에서는A-E-O-A와A-B-C-A의 경계를 손가락이나 색연필로 따라가라. 중간에 선이 만나는 점이 있다는 이유만으로 큰 삼각형의 변이 새 방향으로 꺾였다고 할 수 있는가?',expected='삼각형이라고 답하려면 곧은 세 변이 끝끼리 이어져 닫힌 경계를 이루어야 한다. A-E-O-A는 작은 삼각형이고 A-B-C-A는 더 큰 삼각형이며 선의 일부를 공유해도 각각의 닫힌 경계를 찾을 수 있다. 큰 삼각형의AB 위E,AC 위O는 중간 점이며 경계가 꺾이는 새 꼭짓점은 아니다. 전체 정사각형의 바깥 경계도 내부 선이 추가됐다고 없어지지 않는다. 실제로 그은 선만 사용한다는 조건에서 삼각형을 전부 찾는 교사용 확인 결과는AEO·CFO·ABC·ACD의4개다.',interpretation='단순 닫힘/그리기는1~2학년,겹친 그림 속 부분과 전체 찾기/채우기 설명은3~4학년의 선택 확장으로 구별한다. 정사각형 제작·중점·교점·문자 표시는 교사용 자료 준비이며 좌표나 용어 암기를 저학년에게 요구하지 않는다. 학생이 찾은 경계를 실제로 따라 기록하고 유도/강조한 뒤의 성공을 최초 발견으로 바꾸지 않는다. 모든 삼각형4개를 찾는 것을1~2학년 필수나 새로운 단계 진단으로 사용하지 않는다. 원문의Primary/Secondary는 해당 구성의 선 구조 구분이며 도형 계급의 포함 관계가 아니다. 열린 선 구조도 자료에 등장하므로 모든 찾기 대상을 닫힌 다각형이라고 일반화하지 않고,삼각형을 묻는 경우에 닫힘을 확인한다. 시각·촉각 접근과 운동/기억 조건을 별도로 기록한다.',student_validated=False),
]
MAPPINGS = [
 ('LT16',OBSERVATIONS[0]['standard_codes'],['3D Shapes 개요와 공개7수준 본문','Toothpick Builder / Making Boxes [3D Shape Identifier] 영어 본문·삽입 사진'], '입체 전체와 면·막대 재료와 모서리·요소 공유·각기둥/각뿔의 실제 면 구성을 구별하는 자체 설계 참고다.', '원문 Constructor의정사각형+삼각형4개를triangular prism이라 부른 예를 복사하지 않는다. 모서리 수나 직각 사각형 면 수만으로 정육면체를 확정하지 않으며 사진·일반적인 합동 도움 문구를 해당 수준의 진단/효과 검증으로 사용하지 않는다. 각뿔 전개도와저학년 요소 개수 암기를 새 요구로 넣지 않는다.'),
 ('LT17',OBSERVATIONS[1]['standard_codes'],['Composing 2D Shapes 개요와 공개11수준 본문','Can You Find Another Way? / Super Shape! [Shape Decomposer with Imagery] 영어 본문·삽입 사진'], '같은 조각·다른 합성 외형,변/각의 적합성·방향 이동·분해 계획과 실제 절단 조건을 구별하는 자체 설계 참고다.', '아무 두 삼각형이나 정사각형이 된다고 일반화하지 않는다. 절단을 허용하는 원문 과제와 주어진 조각을 자르지 않고 채우는 현재 과제는 규칙이 다르다. 시행착오와 의도적 계획의 긴장을 고정 능력/필수 순서로 판정하지 않고 외부 연구나 첨부 퍼즐 전체의 읽기·한국 학생 효과로 집계하지 않는다.'),
 ('LT18',OBSERVATIONS[2]['standard_codes'],['Composing 3D Shapes 개요와 공개9수준 본문','Build a Block / Find Another Way 영어 본문·삽입 도식/사진'], '합성 블록의 반복·동일 공간의 대체·물리적 조각과 단위 입방체·내부 채움과 세 치수를 구별하는 자체 설계 참고다.', '같은 부피가 같은 모양/치수나 특정 빈자리 적합성을 뜻하지 않는다. 원문의1차원/2차원 구조 언어를 실제 블록의 길이/두께가 없다는 뜻으로 쓰지 않는다. 도식의 대각선/층 선과 정확한 내부 구성·단위·수치를 구별하며 현재 학생의 수행/효과로 확대하지 않는다.'),
 ('LT19',OBSERVATIONS[3]['standard_codes'],['Disembedding Shapes 개요와 공개5수준 본문','Find the Figure / What\'s the Smallest Shape on the Geoboard? [STEMIE] 영어 본문·삽입 도식/사진'], '그림의 부분과 전체·공유 선분·경계 추적·보조선의 교점과 실제 꼭짓점·도움과 접근 방식을 구별하는 자체 설계 참고다.', 'Primary/Secondary를 사각형 계급 포함이나 모든 그림의 유일한 분해로 사용하지 않는다. 열린 선 구조와 삼각형의 닫힘을 구별한다. 작은 그림8개 대조를 첨부PDF/영상 전체 읽기나 촉각 과제의 동등성·한국 학생 진단 규준 검증으로 바꾸지 않는다.'),
]

def verify():
 assert len(MAPPINGS)==len(OBSERVATIONS)==4
 assert len({c for m in MAPPINGS for c in m[1]})==10
 cube=set(product(range(2),repeat=3))
 edges={frozenset((p,q)) for p,q in combinations(cube,2) if sum(abs(a-b) for a,b in zip(p,q))==1}
 faces=[frozenset(p for p in cube if p[axis]==v) for axis in range(3) for v in range(2)]
 assert (len(cube),len(edges),len(faces))==(8,12,6)
 assert all(sum(e<=f for f in faces)==2 for e in edges)
 assert all(sum(p in f for f in faces)==3 for p in cube)
 def mesh(fs):
  es={frozenset((f[i],f[(i+1)%len(f)])) for f in fs for i in range(len(f))}
  assert all(sum(e<=set(f) for f in fs)==2 for e in es)
  return len(fs),len(es),len({v for f in fs for v in f})
 assert mesh([(0,1,2,3),(0,1,4),(1,2,4),(2,3,4),(3,0,4)])==(5,8,5)
 assert mesh([(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)])==(5,9,6)
 # A coordinate witness has the same incidence graph and rectangular faces, but unequal edges.
 scaled={p:tuple(x*s for x,s in zip(p,(2,3,4))) for p in cube}
 edge_lengths_squared={sum((a-b)**2 for a,b in zip(scaled[p],scaled[q])) for edge in edges for p,q in [tuple(edge)]}
 assert len(set(scaled.values()))==8 and len(edges)==12 and len(faces)==6
 assert edge_lengths_squared=={4,9,16}
 area2=lambda ps:abs(sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(ps,ps[1:]+ps[:1])))
 assert area2([(0,0),(2,0),(0,2)])==4
 assert area2([(2,2),(0,2),(2,0)])==4
 assert area2([(0,0),(2,0),(2,2),(0,2)])==area2([(0,-2),(2,0),(0,2)])==8
 assert area2([(0,0),(2,0),(0,2)])+area2([(0,0),(2,0),(0,-2)])==8
 # The two triangles share only their boundary segment; their open interiors have opposite y signs.
 cells=set(product(range(2),repeat=3))
 bricks=[{(x,y,z) for x in range(2)} for y in range(2) for z in range(2)]
 slabs=[{(x,y,z) for x in range(2) for y in range(2)} for z in range(2)]
 assert len(bricks)==4 and {len(b) for b in bricks}=={2}
 assert len(slabs)==2 and {len(b) for b in slabs}=={4}
 assert set.union(*bricks)==set.union(*slabs)==cells and sum(map(len,bricks))==sum(map(len,slabs))==8
 assert 2*2*2==1*2*4==8 and 2**2+2**2+2**2!=1**2+2**2+4**2
 pts=dict(A=(0,0),B=(4,0),C=(4,4),D=(0,4),E=(2,0),F=(2,4),O=(2,2))
 segments=[(pts[a],pts[b]) for a,b in ['AB','BC','CD','DA','EF','AC']]
 cross=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 on=lambda p,a,b:cross(a,b,p)==0 and all(min(x,y)<=z<=max(x,y) for z,x,y in zip(p,a,b))
 joined=lambda p,q:any(on(p,a,b) and on(q,a,b) for a,b in segments)
 triangles={''.join(sorted(names)) for names in combinations(pts,3) if cross(*(pts[n] for n in names)) and all(joined(pts[a],pts[b]) for a,b in combinations(names,2))}
 assert triangles=={'AEO','CFO','ABC','ACD'}

def main():
 verify();registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:
  assert {m[0] for m in MAPPINGS}<={c['id'] for c in registry['claims']}
  print('LT2 shape composition extension remains current; no automatic refresh');build_report();return
 assert s['snapshot_file']==PRIOR_NOTES and s['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 old=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews());prior=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'))
 assert not {m[0] for m in MAPPINGS}&{v['id'] for v in registry['claims']}
 cache=ROOT/'tmp/literature/lt2-shape-composition'
 pages=json.loads((cache/'manifest.json').read_text(encoding='utf-8'));activities=json.loads((cache/'activity-manifest.json').read_text(encoding='utf-8'));images=json.loads((cache/'image-manifest.json').read_text(encoding='utf-8'))
 assert len(pages)==36 and len(activities)==len(images)==8
 levels=[a for a in pages if '/math/learning-trajectories/' not in a['url']]
 assert Counter(a['url'].split('/math/')[1].split('/')[0] for a in levels)==dict(zip(DOMAINS,[7,11,9,5]))
 assert {a['url'].split('/math-activities/')[1] for a in activities}==set(ACTIVITIES)
 for a in pages+activities+images:
  assert a['url'].startswith(URL) and a['status']==200
  assert hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256']
  if 'final_url' in a:assert a['url']==a['final_url']
 fields=['key','url','title','sha256','status']
 all_assets=prior['observed_html_assets']+[{k:a[k] for k in fields} for a in pages+activities]
 assert len(all_assets)==len({a['url'] for a in all_assets})==len({a['key'] for a in all_assets})==184
 image_fields=['page_url','url','status','sha256','dimensions','content_type']
 image_manifest=[dict(**{k:a[k] for k in image_fields},read_kind='inline_image_visual_review',redistributed=False) for a in images]
 assert len({a['url'] for a in image_manifest})==8
 groups=copy.deepcopy(prior['read_groups'])
 groups['domain_overviews'] += [a['key'] for a in pages if '/math/learning-trajectories/' in a['url']]
 groups['levels'] += [a['key'] for a in levels];groups['activities'] += [a['key'] for a in activities]
 assert {k:len(v) for k,v in groups.items()}==dict(general=6,domain_overviews=16,levels=132,activities=29,teacher_resources=1)
 corrections=[
  dict(kind='pyramid_prism_name_error',locations=['3D Shapes / 3D Constructor of Shapes from Parts / Other Examples','Toothpick Builder / Set Up'],action='정사각형 밑면에 삼각형4개를 붙인 것을triangular prism이라고 한 수준 예는 면 구성과 명칭이 맞지 않는다. 옆면4개가 한 꼭짓점에 모이면 사각뿔이다. 활동 본문은 삼각기둥의 면이 직사각형과 삼각형이라 말한다. 현재 원고에서는 두 자료를 섞지 않고 밑면/옆면·연결·수량을 확인한다. 공식 정오표/저자의 수정 의도는 미확인이다.'),
  dict(kind='cube_sufficient_conditions_and_material_count',locations=['3D Constructor of Shapes from Parts / cube example','Toothpick Builder','Making Boxes'],action='직각 사각형 면6개라는 조건만으로 정육면체가 되지는 않는다. 같은 크기 정사각형 면·모서리 길이·각·접합·닫힘을 확인한다.24면별 모서리 출현과 공유한12모서리,면별로 따로 쓴 막대 수를 구별한다. 카드 목록의 숫자에는 단위가 명시되지 않아cm로 단정하지 않고,주어진 카드를 전부 사용해야 한다는 규칙도 덧붙이지 않는다. 모양과 수가 맞아도 접힌 위치가 맞는지 실제로 확인한다.'),
  dict(kind='generic_congruence_help_scope',locations=['3D Perceiver,3D Face Counter,3D Shape Recognizer,3D Shape Identifier,3D Shape Class Identifier / Help'],action='서로 다른 수준에 같은 합동/포개기 도움 문구가 반복된다. 그 문장 하나를 영아의 합동 정리 이해나 각 수준의 고유 진단/효과 근거로 사용하지 않는다. 개요/수준의 실제 설명과 활동을 별도로 확인하고 연령/하위 명칭을 한국 고정 학년으로 전용하지 않는다.'),
  dict(kind='composition_rule_and_triangle_shape_conditions',locations=['Composing 2D Shapes / Substitution Composer,Shape Composer','Can You Find Another Way?','Super Shape! [Shape Decomposer with Imagery]'],action='수준 설명의 의도적 대체와활동의 시행착오 탐색 권장은 성공/실패 한 번으로 분리할 절대 단계가 아니다. 두 직각삼각형으로 정사각형을 만드는 예는 합동/직각이등변/맞는 변과 배치 등의 조건이 필요하다. 자르기를 허용하는Super Shape의3종 절단 규칙은 자르지 않고 주어진 조각으로 채우는 과제와 구별한다. 첨부 퍼즐을 읽지 않아 최소 종이 수나 모든 해답을 검증했다고 하지 않는다.'),
  dict(kind='same_volume_not_same_shape_and_dimension_language',locations=['Composing 3D Shapes / Line Maker,Piece Assembler,Substitution Composer','Build a Block / inline diagram','Find Another Way'],action='선/바닥/벽의1차원/2차원 구조는 공간 확장의 표현이며 블록 자체의 두께가 없다는 뜻이 아니다. 같은 양의 블록을 다른 배치로 놓는 것과 같은 공간을 대체하는 합동 합성은 다르다. 삽입 도식의 표면 대각선/층 선에는 치수와 숨은 절단면이 모두 제시되지 않아 정확한 채움/부피의 증거로 쓰지 않는다. 두 삼각기둥도 합동/길이/방향 조건 없이 언제나 직육면체로 결합하지 않는다.'),
  dict(kind='embedded_structures_open_lines_and_help',locations=['Disembedding Shapes / levels','Find the Figure / inline Primary/Secondary diagram','What\'s the Smallest Shape on the Geoboard? [STEMIE]'],action='삽입 도식에는 별 모양의 원래 삼각형들과 선분을 빌린 마름모/사다리꼴,정사각형과 열린 선 구조가 함께 있다. Primary/Secondary를 전부 닫힌 다각형이나 사각형 계급 포함으로 읽지 않는다. 삼각형을 묻는 경우 닫힌 경계를 확인하고 교점/일직선 중간점과 꼭짓점을 구별한다.2초 제시·추적/강조·촉각 안내는 기억/시각/운동·도움 조건이 달라 처음 독립 수행과 따로 기록한다. 도구를 바꾸었다는 것만으로 측정 동등성/현재 진단 정확도를 검증하지 않는다.'),
  dict(kind='selected_images_not_student_outcome_or_full_attachments',locations=['선정8활동의 삽입 그림·Last updated·References'],action='삽입 그림8개는 사진6개와 도식2개다. 제작/조작 사진에서 개별 학생의 최초 전략·독립 성공·장기 효과·장애/시각 상태를 판정하지 않는다. 같은 그림이 영어/반복 부분에 두 번 나와도 한 URL로 센다. 갱신일2024/2025와 인용1997/2002/2020/2021 및©표시는 서로 다르며 해당 교재/원연구 읽기로 합산하지 않는다. PDF·영상·가상 지오보드 실행은 확인 전이다.'),
 ]
 p=ROOT/'data/sources.json';bibliography=json.loads(p.read_text(encoding='utf-8'));b=next(v for v in bibliography if v['id']==SOURCE);previous_b=copy.deepcopy(b)
 b.update(review_scope=SCOPE,next_review='현재20영역 중 미검토4영역(수량 즉지·규칙/구조/대수·공간 방향·공간 시각화)의 개요/수준과 초기4영역의 미선정 수준·모든 영역의 미선정 활동을 후속 대조한다. 이번8개 삽입 그림 외의 그림·영상·첨부PDF·게임·원연구/교재·정오표와 현재 한국어 과제의 실제 반응·진단 정확도·효과는 별도다.')
 image_log=[
  'Toothpick Builder 사진:막대/연결점으로 만든 평면 틀과 입체 골격이 함께 보인다. 물질로 덮인 면과 기하적 면을 구별하며 사진만으로 각 틀의 정확한 직각/같은 길이·개별 학생의 단계를 판정하지 않는다.',
  'Making Boxes 사진:성인과 아동이 판지를 재고 자르는 장면이다. 정확한 치수/접합/완성된 닫힌 상자의 검증이나 본문 카드 규칙의 실행 결과가 아니다.',
  'Can You Find Another Way? 사진:패턴 블록 조작 장면이며 모든 조각/경계가 보이지 않는다. 모든 빈틈/겹침·독립 계획·모든 대체 해답을 검증한 자료로 쓰지 않는다.',
  'Super Shape 사진:종이와 자르기 도구를 사용하는 장면이다. 본문3종 절단의 실제 순서·최소 종이 수·그 퍼즐 해답을 확정하지 않는다.',
  'Build a Block 도식:왼쪽 직육면체 앞면 대각선과 오른쪽 가로 층 선을 비교했다. 분할 의도를 참고하되 길이/내부 절단면/동일 단위는 수치와 조건으로 따로 정해야 한다.',
  'Find Another Way 사진:여러 크기 블록과 삼각 모양 단면의 블록이 보인다. 사진의 원근 길이를 정확한 치수/단위로 사용하지 않고 같은 공간 대체를 별도 검사한다.',
  'Find the Figure 도식220×95:행1의 별/두 삼각형/마름모·사다리꼴,행2의 정사각형/열린 꺾인 선/삼각형 및 열린 선 구조를 확인했다. 모든 자료가 닫힌 다각형을 뜻하지 않으며 첨부PDF 전체 예는 미검토다.',
  'Geoboard 사진:여러 색 고무줄과 핀 보드의 도형 조작 장면이다. 촉각 수행의 성공·개별 아동의 시각 상태·가상 도구 실행이나 측정 동등성을 사진에서 추정하지 않는다.',
 ]
 updates=dict(zip(ACTIVITIES,['2025-07-17','2025-07-17','2025-07-03','2025-07-02','2025-07-17','2025-07-17','2025-07-28','2024-11-18']))
 log=['새4개 개요·공개32수준의 설명·텍스트 예·교수 도움·활동 목록 본문을 읽었다. 입체도형7·평면 합성11·입체 합성9·숨은 도형 찾기5개다. 선정8활동의 목표·절차·팁·자료·차별화·표시 참고문헌을 읽고 삽입 그림8개를 별도로 시각 대조했다.', '이전140개HTML에 새44개HTML을 더해184개다. 삽입 그림은8개 별도 자산으로 기록하며 HTML/활동/단계/연구 수에 중복 합산하지 않는다. 공개20영역 목록과 대조해 개요 읽기16개·남은4개를 구분했다.', '기존 홈페이지의 기준HTML 해시와 모든 이전 주장/관찰·읽기 기록을 보존한다. 첨부PDF·수준 영상·가상 게임과 교재/인용 원연구는 읽거나 실행한 것으로 확대하지 않는다.']
 notes=dict(source_id=SOURCE,source_url=URL,source_asset_kind='publisher_html',source_asset_sha256=s['source_asset_sha256'],source_asset_redistributed=False,contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,date='2026-11-06',reviewer='Codex',read_scope=SCOPE,previous_review=copy.deepcopy(s),previous_bibliography=previous_b,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,observed_html_assets=all_assets,html_read_manifest=all_assets,image_read_manifest=image_manifest,image_reading_log=image_log,read_groups=groups,new_read_groups=dict(domain_overviews=4,levels=32,activities=8,teacher_resources=0),reading_log=prior['reading_log']+log,source_corrections=prior['source_corrections']+corrections,activity_update_dates={**prior['activity_update_dates'],**updates},catalog_recheck=prior['catalog_recheck'],crosslisted_level_groups=prior['crosslisted_level_groups'],unread_followups=[b['next_review'],'이번8개 삽입 그림 외의 원본 자산과 첨부PDF는 별도다. 자체 모형/수치/교사용 제작 지침을 실제 학생의 활동이나 외부 원문 그림의 복사로 집계하지 않는다.'])
 npath=ROOT/NOTES;npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=s['date'],read_scope=s['read_scope'])]
 s.update(date='2026-11-06',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),snapshot_history=history,bibliography_snapshot=digest(b),html_read_manifest=all_assets,image_read_manifest=image_manifest,read_scope=SCOPE,method_note='기존140개HTML에 입체도형·평면/입체 합성·숨은 도형 찾기의 개요4·수준32·활동8을 더하고 활동 삽입 그림8개를 시각 대조했다. 명칭 오류·충분조건·공유 요소·같은 양/다른 외형·닫힘/도움의 한계를 기록한다.',limits='누적184개 지정 영어 본문과 별도 삽입 그림8개다.20영역 중16개 개요를 읽었고 새4영역32수준 본문은 모두 읽었으나 전체 사이트·모든 활동/그림·영상·첨부PDF·게임·원연구·교재 전권은 미검토다.0–8세 자원을 국내 학년 전체·현재 효과·진단 규준·유일한 경로로 쓰지 않는다. 사진만으로 개별 학생의 수행/단계/시각 상태를 판정하지 않고 같은 양과 같은 모양,재료와 기하적 요소,도형과 선 구조를 구별한다.',editorial_action='기존주장15건·자체 관찰15건을 보존하고10개 기준에 새 주장4건·자체 관찰4건을 추가했다. 누적37개 기준·주장19건·관찰19건이며 관계 검토·독립 검토·학생 검증으로 합산하지 않는다.',observations=s['observations']+OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 assert len({c for v in registry['claims'] if v['source_id']==SOURCE for c in v['standard_codes']})==37
 p.write_text(json.dumps(bibliography,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'data/content_review_queue.json';q=json.loads(p.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE]);p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])]==old['claims'] and s['observations'][:15]==old['sources'][SOURCE]['observations']
 assert all(registry['sources'][k]==v for k,v in old['sources'].items() if k!=SOURCE) and load_reviews()==relations
 build_report();print('Extended LT2:44 new public HTML bodies,8 inline images,4 claims,4 own observations; prior evidence preserved')

if __name__=='__main__':main()

"""Scope selected geometry teacher references and preserve prior source snapshots."""
from math import sqrt
from record_conic_representation_research import probe
from record_middle_number_system_research import amsi
from record_scoped_pdf_research import ROOT, record
from extend_lt2_length_assets_review import load, sha, write
from literature_review import build_report, digest, load_registry, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot

DATE='2026-11-13'
CACHE=ROOT/'tmp/literature/middle-geometry'
PL='AMSI_2011_PLANE_GEOMETRY'
CT='AMSI_2011_CONSTRUCTION'
CG='AMSI_2011_CONGRUENCE'
SM='AMSI_2011_SIMILARITY'
CI='AMSI_2011_CIRCLE_GEOMETRY'
SO='AMSI_2011_CONES_PYRAMIDS_SPHERES'
NS='NSW_STAGE4_CIRCLE_MEASUREMENT'
SA='NCETM_2019_SURFACE_AREA'
P,L,C,D,A,M,V,I,T,R,H,U=[f'9수03-{i:02d}' for i in [1,2,3,5,6,7,8,9,10,14,18,19]]

SPECS={
 PL:amsi('Introduction to plane geometry',9,'7–8','amsi-plane-geometry-2011','introduction_to_plane_geometry',
  '9308b7c339d67674189b42cf44e03da459e1600d385283da91c0388a36bdc8db',20,
  [1,2,3,5,6,7,9,10,11,12,14,15,16],[6,11,14,15,16],
  '표지·서지와 이상적인 점·직선, 평면에서의 위치·각, 평행선의 동위각·엇각과 역, 삼각형·사각형 내각합의 지정 본문·도식을 읽었다.',
  '평면의 두 직선 설명을 공간의 꼬인 위치까지 확장한 정리로 읽지 않는다. 11쪽 동측내각이 같지 않다는 문장은 수직 횡단선의 90°·90° 예외가 있다. 볼록 n각형 일반화와 정육면체 위치 과제는 자체 확장이다.',
  ['평면 위치 관계와 공간 확장의 한계','평행 각의 성질·역·조건','내각합의 분할 설명']),
 CT:amsi('Construction',13,'7–8','amsi-construction-2011','Construction',
  '0ad4edbcbe87d15dbcd766f967add2b4a4b7bb208aadb219f5015eeba39f358c',30,
  [1,2,3,6,9,10,11,12,21],[9,10,11,21],
  '서지, 컴퍼스의 같은 거리, 정삼각형·각의 이등분과 복사, 수직이등분선·수선 및 외심·내심의 지정 절차와 도식을 대조했다.',
  '그림을 보고 같은 듯하다고 판단하는 것과 합동으로 정당화하는 것을 나눈다. 수직이등분선의 두 원 교점에는 공통 반지름이 선분 절반보다 커야 한다. 무게중심·수심·구점원은 추가 필수로 삼지 않는다.',
  ['작도 단계가 보존하는 거리·각','외심과 내심의 서로 다른 등거리 조건']),
 CG:amsi('Congruence',14,'8','amsi-congruence-2011','Congruence',
  'f2ea12394a9a44eda7aefade8deb57b7be7408bba8c75b3fe2d3be49160921b5',28,
  [1,2,3,8,9,10,11,12,14,15,16,18,19,20,21,22],[9,14,15,19,20,21],
  '합동의 대응 순서, 세 변·끼인각·두 각 조건의 작도와 가능 조건, 잘못된 SAS 적용 반례, 외심·내심과 이등변삼각형 성질·역의 지정 설명을 대조했다.',
  '유일성은 위치 하나가 아니라 합동을 제외한 유일성이다. 15쪽 잘못된 SAS는 의도적 반례다. 일반 SSA와 둔각 확장을 국내 합동 조건으로 올리지 않고 두 각과 한 변은 국내 ASA 범위에서 설명한다.',
  ['삼각형 작도의 가능성과 합동 조건','이등변 성질·역과 등거리의 정당화']),
 SM:amsi('Scale drawings and similarity',22,'8–10','amsi-similarity-2011','Scale_drawings_and_similarity',
  '42cb25e9713b58d20e9ceed8b390dda9cfbc11f31d3a7b85568465af45afc16c',42,
  [1,2,3,14,15,16,17,21,22,23,24],[17,21,23,24],
  '닮음의 대응 순서와 두 종류의 비, 평행선의 각으로 보이는 닮음 예, 중점과 일반 선분 분할비·전체 길이비 및 역의 지정 본문·도식을 대조했다.',
  '부분 대 나머지와 부분 대 전체를 구별한다. 원문은 중점 사례의 합동 풀이도 허용하므로 닮음이 모든 학생의 유일한 필수 선행이라는 근거가 아니다. 세 평행선의 두 횡단선 과제는 삼각형 설명을 이용한 자체 확장이다.',
  ['평행 각과 닮음의 대응','분할비와 전체에 대한 비의 차이']),
 CI:amsi('Circle geometry',26,'9–10','amsi-circle-geometry-2011','Circle_Geometry',
  'bc40c70857258e19ca7f13c9b021dc296156f70cbf3d7ec8258ded7b8cde2942',46,
  [1,2,3,6,7,8,9,11,12,13,18,19,20,21],[7,8,11,12,18,19],
  '서지·원주와 넓이, 반지름·현·큰 호와 작은 호, 지름 및 같은 호의 원주각과 세 중심 위치, 접선의 수직 성질·외부점 작도·접선 길이의 지정 설명을 읽었다.',
  '현의 중점이 중심인 지름 예외와 같은 현의 두 호를 구별한다. 12쪽 첫 줄의 이등변삼각형 OAQ 표기는 뒤 증명의 OBP와 다르다. 원의 비례·할선 거듭제곱·접현각 및 고급 삼각·해석기하 확장은 국내 추가 필수로 삼지 않는다.',
  ['현의 수직이등분과 지름 예외','반지름과 접선·접선 선분','같은 호의 원주각과 중심 위치']),
 SO:amsi('Cones, pyramids and spheres',12,'9–10','amsi-cones-pyramids-spheres-2011','Cones_Pyramids_and_Spheres',
  'd9b4eb1e6ad57c22644bed8e62d8f7a5c8fa13cd71ab7c0185b0f3130821f38d',24,
  [1,2,3,4,6,7,8,9,10,11,12,13,14],[7,8,10,12,14],
  '서지와 기둥·원기둥 복습, 각뿔·직원뿔의 높이와 옆면·전개도, 부채꼴 비율 및 구의 겉넓이·부피의 지정 본문·그림을 대조했다.',
  '높이와 모선·옆면 높이를 나누고 원뿔의 전개도는 직원뿔에 한정한다. 12쪽 부피 단위 cm²와 밑변 c,d·높이 h인 각뿔의 잔존 x 표기는 옮기지 않는다. 유한 다각형·작은 각뿔 근사를 엄밀한 증명으로 세지 않고 사선 입체·적분·절두체는 추가 요구하지 않는다.',
  ['다면체와 회전체의 표현','부채꼴 호와 원뿔 전개도','겉넓이·부피의 길이와 단위']),
}

CLAIMS=[
 (PL,'PLG11-01',[P],[5,6,7],
  '점과 직선을 크기·두께 없는 수학적 대상으로 설명하고, 평면의 서로 다른 두 직선은 만나거나 평행하다는 위치 관계와 선분·반직선·각을 구별한다.',
  '같은 평면이라는 조건이 필요하다. 자체 정육면체 과제의 꼬인 위치와 직선·평면 및 두 평면 관계는 이 설명을 국내 기준으로 확장한 과제이며 원문이 공간 위치 전부를 증명한 것은 아니다.'),
 (PL,'PLG11-02',[L],[10,11,12,14,15],
  '평행한 두 직선을 한 직선이 가로지를 때 동위각·엇각이 같고 동측내각은 합이 180°임을 설명하며 각의 같음에서 평행을 판단하는 역을 구별한다.',
  '각의 위치와 두 직선·횡단선의 조건을 먼저 확인한다. 원문 11쪽의 동측내각이 같지 않다는 문장은 횡단선이 수직이면 90°씩 같을 수 있어 그대로 옮기지 않는다.'),
 (PL,'PLG11-03',[D],[15,16],
  '평행선의 각을 이용해 삼각형 내각합을 설명하고 대각선으로 사각형을 두 삼각형으로 나누어 내각합을 구하도록 제안한다.',
  '볼록 n각형의 삼각형 n−2개, 내각합 (n−2)×180°, 대각선 n(n−3)/2의 일반화는 자체 확장이다. 일반 다각형의 각이 모두 같거나 내각 하나가 정해진다는 뜻이 아니다.'),
 (CT,'CTG11-01',[C],[6,9,10,11],
  '컴퍼스가 같은 거리를 보존한다는 성질로 정삼각형·각 복사·각의 이등분과 수직이등분선을 작도하고, 단계의 이유와 합동을 통한 정당화를 구별한다.',
  '수직이등분선의 두 원 교점을 얻으려면 같은 반지름뿐 아니라 선분 절반보다 큰 반지름이 필요하다. 눈금 측정이나 각도기 확인을 자·컴퍼스 작도의 증명과 같게 처리하지 않는다.'),
 (CT,'CTG11-02',[C,T],[9,10,11,21],
  '변의 수직이등분선의 교점인 외심과 내각 이등분선의 교점인 내심을 서로 다른 작도 절차로 연결하고 예각·직각·둔각 삼각형을 비교하도록 제안한다.',
  '외심은 꼭짓점까지의 거리, 내심은 변까지 내린 수선의 길이가 같다. 작도 활동이 등거리 성질을 자동 입증하지 않으므로 합동 등 이유를 별도로 설명한다. 중심이 항상 내부라는 판단은 외심에 일반화할 수 없다.'),
 (CG,'CONGR11-01',[C],[8,9,10,11,12,14,15,16],
  '세 변 또는 두 변과 끼인각, 한 변과 양 끝 각을 정한 삼각형 작도에서 대응과 합동을 제외한 유일성을 설명하고, 두 변과 끼이지 않은 각은 일반적인 합동 조건이 아님을 반례로 보인다.',
  '양수 길이·삼각부등식과 각의 합을 확인해야 한다. 대칭 위치의 두 작도 결과는 서로 다른 합동 종류가 아니다. 원문의 AAS는 국내 ASA로 바꿔 설명하며 새로운 합동 공리를 필수로 더하지 않는다.'),
 (CG,'CONGR11-02',[I,T],[14,18,19,20,21],
  '이등변삼각형의 꼭지각 이등분선으로 얻은 두 삼각형의 SAS 합동에서 밑각의 같음을 정당화하고 역도 살핀다. 외심·내심은 수직이등분선 또는 각 이등분선과 합동으로 서로 다른 등거리 조건을 설명한다.',
  '증명할 중점·수직 성질을 미리 가정하지 않는다. 15쪽의 끼이지 않은 각을 쓴 잘못된 SAS는 의도적 반례다. 이 설명의 연결을 학생의 보편적인 필수 학습 순서나 작도 도구의 효과로 세지 않는다.'),
 (SM,'SIM11-01',[R],[14,15,16,21,22,23,24],
  '삼각형의 두 변을 같은 부분 대 나머지 비 1:k로 나눈 점을 이으면 나머지 변과 평행이고 길이비는 1:(k+1)임을 설명하며, 평행일 때의 역방향 비 계산도 대응시킨다.',
  '길이는 양수이고 대응점과 같은 쪽의 부분을 확인한다. 부분/나머지와 부분/전체를 바꾸지 않는다. 교차하거나 회전한 그림에서도 대응을 다시 확인하며 원의 비례를 추가 요구하지 않는다.'),
 (SM,'SIM11-02',[L,R],[17,21,23,24],
  '평행선의 동위각·엇각과 공통각·맞꼭지각으로 닮음을 보인 뒤 대응변의 비를 쓰는 삼각형·교차형 예를 제시하고 중점 사례와 일반 분할비를 구별한다.',
  '중점 사례는 원문이 합동만으로도 설명하므로 닮음이 모든 풀이의 유일한 필요 조건이라는 근거가 아니다. 세 평행선 두 횡단선 과제는 삼각형의 대응을 이용한 자체 확장이다.'),
 (CI,'CGEOM11-01',[H],[6,7,8],
  '중심을 지나지 않는 현의 두 끝점과 중심을 이은 이등변삼각형에서 현의 수직이등분 성질을 설명하고 같은 원의 같은 현과 중심각을 합동으로 연결한다.',
  '지름이면 현의 중점과 중심이 같아 두 점으로 정하는 선 OM을 그대로 쓸 수 없다. 지름 자체의 수직이등분선은 존재한다. 호는 작은 호·큰 호를 구별하며 선분 합동을 곡선인 호에 직접 적용하지 않는다.'),
 (CI,'CGEOM11-02',[H],[18,19,20],
  '원의 한 점에서 반지름에 수직인 직선이 그 원의 유일한 접선임을 피타고라스 정리로 정당화하고, 외부 한 점에서 두 접선 선분의 길이가 같음을 설명한다.',
  '원에 관한 접선 정의를 모든 곡선에 일반화하지 않는다. 길이를 비교하는 대상은 무한 직선이 아니라 외부점에서 접점까지의 선분이다. 외부점 조건과 반지름>0을 유지한다.'),
 (CI,'CGEOM11-03',[U],[9,11,12,13],
  '원주각은 같은 호가 만드는 중심각의 절반임을 중심이 삼각형 내부·변 위·외부인 경우로 나누어 설명하고, 같은 호의 두 원주각과 지름에 대한 직각을 연결한다.',
  '같은 현이라는 말만으로 양쪽 호 위의 원주각을 모두 같다고 하지 않는다. 큰 호에는 큰 중심각을 대응시킨다. 12쪽 첫 줄 OAQ는 뒤 증명에서 쓰는 이등변삼각형 OBP와 달라 자체 설명은 OAP·OBP로 쓴다.'),
 (SO,'SOLID11-01',[M],[4,6,7,9,10],
  '각뿔의 다각형 밑면과 꼭짓점에 모인 삼각형 옆면, 직원뿔의 밑면·높이·모선과 전개도를 서로 다른 표현으로 설명한다.',
  '실제 모형을 조작하도록 설계한 자체 과제와 실제 학생이 조작했다는 자료를 구별한다. 정각뿔이 반드시 정다면체는 아니며 볼록 다면체·단순 회전체의 국내 범위에 한정한다. 사선 원뿔 전개도로 확대하지 않는다.'),
 (SO,'SOLID11-02',[V],[4,6,7,8,9,10,11,12,13,14],
  '기둥·뿔의 부피에 쓰는 수직 높이와 겉넓이에 쓰는 옆면 높이·모선을 구별하고 밑면을 포함한 면의 넓이 합, 구의 겉넓이와 부피를 다른 단위로 설명한다.',
  '12쪽 375π의 부피 단위 cm²는 cm³이어야 하며 밑변 c,d·높이 h인 각뿔 부피는 cdh/3이다. 구를 유한 개의 작은 각뿔로 나눈 근사나 한 번의 물 붓기를 일반 공식의 엄밀한 증명으로 세지 않는다.'),
 (SO,'SOLID11-03',[A,M,V],[10,11],
  '직원뿔 옆면을 모선 길이를 반지름으로 하는 부채꼴로 펼치면 호의 길이는 밑면 원주 2πr이며, 이 비율로 옆넓이 πrl을 설명한다.',
  '전개도 부채꼴의 반지름 l과 밑면 반지름 r, 수직 높이 h를 구별한다. 원문 circumference of the sector는 여기서 호 길이를 뜻하며 두 반지름까지 더한 전체 둘레와 다르다. 전개도 접근을 유일한 필수 학습 순서로 세지 않는다.'),
]
REUSED_CLAIMS=[
 (NS,'NSW-MG11-01',[A],[40,41],
  '접은 원의 반원·사분원·팔분원에 대해 중심각이 전체 회전에서 차지하는 몫과 넓이의 몫을 연결하고 유한 부채꼴 조각의 재배열을 비교하도록 제안한다.',
  '일반 각도 θ의 호 길이·넓이 및 둘레 과제는 AMSI 원의 원주·넓이와 원뿔 전개도 설명을 함께 참고한 자체 중학교 확장이다. 유한 조각은 정확한 직사각형이 아니며 원문 전체 정독·학생 실험을 뜻하지 않는다.'),
 (SA,'SA-MG11-01',[M,V],[8,29,32],
  '같은 개수의 단위 정육면체로 만든 서로 다른 직육면체를 모형과 여섯 면의 합으로 비교해 같은 부피라도 겉넓이가 달라질 수 있음을 탐구하도록 제안한다.',
  '원문은 24개 모형이고 자체 중학교 과제는 12개로 바꾸었다. 29쪽의 빠진 면은 의도적 오류이며 정답으로 옮기지 않는다. 모형·전개도 방법을 모든 학생의 필수 선행이나 효과 검증으로 세지 않는다.'),
]

OBSERVATIONS={
 PL:[
  probe('PLG-P1',P,'정육면체의 아래 면을 차례로 A,B,C,D, 위 면을 E,F,G,H라 하고 AE,BF,CG,DH가 모서리다. 직선 AB와 EF, CG, BC의 위치를 비교하라. AB와 평면 ABCD, AE와 평면 ABCD, EF와 평면 ABCD 및 평면 ABCD와 EFGH, BCGF의 관계도 설명하라.',
   'AB와 EF는 평행, AB와 CG는 같은 평면에 있지 않고 만나지 않는 꼬인 위치, AB와 BC는 B에서 만난다. AB는 평면 ABCD에 포함되고 AE는 A에서 만나며 EF는 그 평면과 평행이다. 평면 ABCD와 EFGH는 평행, ABCD와 BCGF의 교선은 BC다.',
   '평면의 만나거나 평행인 두 직선 설명을 공간에 무조건 옮기지 않는 자체 확장이다. 그려진 선의 굵기·끝과 수학적 직선 전체를 구별한다.'),
  probe('PLG-P2',L,'서로 다른 평행선 l,m과 횡단선 t에서 한 동위각 쌍의 한 각이 65°다. 다른 동위각, 그와 엇각인 각, 그 각과 같은 쪽의 동측내각을 구하라. t가 두 평행선에 수직이면 동측내각 두 개는 서로 다른가? 동위각이 같은 조건에서 평행을 판단하는 역도 설명하라.',
   '대응 위치의 동위각·엇각은 65°이고 그와 합이 180°인 동측내각은 115°다. t가 수직이면 동측내각은 90°씩 같으므로 항상 다르다는 문장은 거짓이다. 두 직선을 가로지르는 횡단선의 동위각이 같으면 두 직선은 평행이다.',
   '각의 위치·성질·역을 구별하고 원문 11쪽의 항상 다르다는 단정을 반례로 점검한다.'),
  probe('PLG-P3',D,'볼록 팔각형의 한 꼭짓점에서 모든 대각선을 그으면 몇 개의 삼각형이 생기는가? 내각합과 전체 대각선 수를 설명하고, 모든 내각이 135°인지 판단하라.',
   '한 꼭짓점의 대각선 5개로 삼각형 6개가 생겨 내각합은 1080°다. 각 꼭짓점에서 5개씩 세되 두 번 세므로 전체 대각선은 8×5/2=20개다. 내각이 모두 135°인 것은 정팔각형 등 등각 조건이 있을 때이며 일반 볼록 팔각형에 단정하지 않는다.',
   '원문의 삼각형·사각형 분할을 볼록 다각형으로 자체 확장했다. 전체 합과 개별 각, 대각선 중복 계산을 구별한다.'),
 ],
 CT:[
  probe('CTG-P1',C,'AB=6cm, AC=5cm, BC=4cm인 삼각형을 자·컴퍼스로 작도하고 두 원이 AB 양쪽에서 만나는 경우를 설명하라. 길이 3,3,6인 삼각형도 가능한가? 길이 6인 선분의 수직이등분선에 쓰는 두 원의 공통 반지름은 얼마보다 커야 하는가?',
   'AB를 그린 뒤 A 중심 반지름 5, B 중심 반지름 4인 원의 교점을 C로 정한다. 양쪽 교점은 대칭인 합동 삼각형이다. 3+3=6이면 일직선이 되어 삼각형이 아니다. 수직이등분선의 두 교점에는 공통 반지름이 3보다 커야 한다.',
   '작도 가능한 길이와 합동을 제외한 유일성, 공통 반지름만으로 충분하지 않은 두 교점 조건을 확인한다.'),
  probe('CTG-P2',C,'크기가 50°·60°인 각의 본이 주어져 있다. 이를 자·컴퍼스로 복사해 AB=5cm, AC=4cm와 끼인각 A=60°로 작도하는 과정과 AB=5cm, A=50°, B=60°로 작도하는 과정을 설명하라. 두 변과 끼이지 않은 각이면 항상 같은 모양 하나가 정해지는가?',
   '첫 작도는 주어진 60° 각을 A에 복사한 반직선에 AC=4인 점을 잡고 B와 잇는다. 둘째는 A,B에서 같은 반평면 안에 주어진 50°,60° 각을 각각 복사한 반직선의 교점을 C로 잡고 세 번째 각은 70°다. 첫 각은 0°보다 크고 180°보다 작으며 둘째 두 각의 합은 180°보다 작아야 한다. 두 변과 끼이지 않은 각은 일반 합동 조건이 아니다.',
   '작도·각 복사 절차와 SAS·ASA의 유일성 근거를 연결한 자체 과제이며 원문이 쓰는 AAS나 둔각 확장을 추가 공리로 요구하지 않는다.'),
  probe('CTG-P3',T,'예각·직각·둔각 삼각형을 각각 그려 외심과 내심을 작도하라. 각 중심에서 같아야 하는 거리는 무엇이며 항상 삼각형 내부에 있는가?',
   '외심은 변의 수직이등분선의 교점으로 세 꼭짓점까지 거리가 같다. 예각이면 내부, 직각이면 빗변의 중점, 둔각이면 외부다. 내심은 내각 이등분선의 교점으로 세 변까지의 수선 길이가 같고 항상 내부다. 눈으로 같아 보이는 것 외에 수직이등분선·각 이등분선과 합동의 이유를 설명한다.',
   '외심의 꼭짓점 거리와 내심의 변에 대한 수직 거리를 구별하며 한 종류의 삼각형 그림을 모든 경우로 확대하지 않는다.'),
 ],
 CG:[
  probe('CONGR-P1',I,'AB=AC인 삼각형에서 꼭지각 A의 이등분선이 BC와 M에서 만난다. M이 중점이라는 가정 없이 밑각의 같음과 BM=CM, AM⊥BC를 정당화하라. 밑각이 같을 때의 역도 설명하라.',
   'AB=AC, AM 공통, 각 BAM=CAM이므로 두 삼각형은 SAS 합동이다. 대응하는 밑각과 BM,CM이 같고 BMA,CMA는 같은 크기로 합이 180°라 각각 90°다. 역은 밑각이 같은 삼각형과 꼭짓점 B,C의 대응을 바꾼 자기 삼각형에 ASA를 적용해 AB=AC로 정당화할 수 있다.',
   '증명할 중점·수직을 미리 가정하지 않는다. 역의 자기 대응에서는 밑변 BC와 그 양 끝 각을 써 ASA를 적용한다.'),
  probe('CONGR-P2',I,'AB=AC=5, BC=6인 이등변삼각형에서 X가 BC 위에 있고 BX=1이다. AB=AC, AX 공통, 밑각 B=C를 근거로 AXB와 AXC가 SAS 합동이라는 주장을 판단하라.',
   'CX=5이므로 BX와 CX가 달라 두 삼각형은 합동이 아니다. 같은 밑각 B,C는 주어진 두 변 AB·AX 및 AC·AX 사이의 각이 아니므로 SAS를 적용할 수 없다.',
   '원문의 의도적 잘못된 논증을 자체 수치 반례로 바꾸었다. 이런 주장이 실제 학생에게 얼마나 나타나는지는 아직 조사하지 않았다.'),
 ],
 SM:[
  probe('SIM-P1',R,'삼각형 ABC의 변 AB,AC 위에 F,G가 있고 FG∥BC다. AF:FB=2:3, AC=15, BC=20일 때 AG,GC,FG를 구하고 닮음의 대응과 비를 설명하라.',
   '평행선의 동위각과 공통각으로 AFG와 ABC는 A↔A,F↔B,G↔C로 닮는다. AF/AB=2/5이므로 AG=6, GC=9, FG=8이다. 부분 대 나머지 2/3을 부분 대 전체 2/5와 바꾸지 않는다.',
   '같은 대응 순서와 전체 길이의 기준을 확인한다. 그림의 겉모양이나 원문 1:k의 숫자만 복사해 계산하지 않는다.'),
  probe('SIM-P2',R,'세 평행선 l,m,n이 첫 횡단선과 차례로 A,B,C, 둘째 횡단선과 D,E,F에서 만난다. AB:BC=2:3, DE=4일 때 EF를 구하고 대응 선분과 이유를 설명하라.',
   '대응하는 두 평행선 사이의 선분 비가 같아 DE:EF=2:3이므로 EF=6이다. D를 지나 첫 횡단선과 평행한 보조선을 긋고 생기는 평행사변형으로 대응 길이를 옮기면 삼각형의 평행선 분할비로 설명할 수 있다. 전체 DF=10과 나머지 EF=6을 구별한다.',
   '원문 삼각형 분할 설명을 세 평행선으로 확장한 자체 과제다. 횡단선이 세 평행선을 차례로 만나는 비퇴화 조건을 유지한다.'),
 ],
 CI:[
  probe('CGEOM-P1',H,'반지름 13인 원에서 중심 O와 현 AB 사이의 수직 거리가 5다. 수선의 발 M이 현을 이등분함을 설명하고 AB를 구하라. 현이 지름이면 직선 OM이라는 설명을 그대로 쓸 수 있는가?',
   'OA=OB, OM 공통, 두 직각삼각형의 빗변과 한 변이 같아 AM=BM이다. AM²=13²−5²=144이므로 AM=12, AB=24다. 지름이면 M=O라 서로 다른 두 점으로 정하는 직선 OM은 쓸 수 없지만 지름의 중점을 지나는 수직이등분선은 존재한다.',
   '중심과 현의 거리의 정의, 반 길이와 전체, 지름 경계를 구별한다. 직접 수치 검산과 일반 합동 정당화를 나눈다.'),
  probe('CGEOM-P2',H,'중심 O, 반지름 6인 원 밖의 점 P에서 OP=10이고 접점은 T,U다. 접선 선분 PT,PU의 길이와 같음의 이유를 설명하라. OP가 6보다 작아도 이런 두 접선을 그릴 수 있는가?',
   '반지름은 접선에 수직이므로 PT²=PU²=10²−6²=64, PT=PU=8이다. 직각삼각형의 공통 빗변 OP와 같은 반지름 OT,OU로도 합동을 설명한다. OP<6인 내부점에서는 그 점을 지나는 원의 접선이 없다.',
   '원의 접선 직선과 길이를 갖는 접선 선분, 외부점 조건을 구별하고 원의 비례나 접현각을 추가 요구하지 않는다.'),
  probe('CGEOM-P3',U,'원에서 작은 호 AB에 대한 중심각이 120°다. 큰 호 AB 위의 점 P와 작은 호 AB 위의 점 Q에서 만든 APB,AQB를 비교하라. 지름인 경우와 중심이 삼각형 내부·변 위·외부인 경우의 설명도 비교하라.',
   'P는 작은 호 120°를 바라보아 APB=60°, Q는 큰 호 240°를 바라보아 AQB=120°다. 같은 현만으로 두 각이 같다고 할 수 없다. 지름을 바라보는 원주각은 90°다. 중심과 원주 위 꼭짓점을 이으면 이등변삼각형의 밑각·외각을 이용해 내부에서는 각을 합하고 변 위에서는 한 삼각형으로, 외부에서는 각을 빼서 같은 호의 두 배 관계를 설명한다.',
   '각이 바라보는 호를 먼저 고른다. 원문 12쪽 OAQ의 문자 불일치를 되풀이하지 않고 OAP·OBP의 반지름이 같은 이유를 쓴다.'),
 ],
 SO:[
  probe('SOLID-P1',M,'정육면체·정사각뿔·직원뿔의 구체 모형을 준비해 면·모서리·꼭짓점과 곡면을 비교하라. 정사각뿔은 항상 정다면체인가? 직각삼각형을 한 직각변 둘레로 한 바퀴 돌리면 어떤 입체가 생기는가?',
   '정육면체는 평면인 6면·12모서리·8꼭짓점이다. 정사각뿔은 밑면 정사각형과 삼각형 옆면 4개로 되어 모든 면이 합동인 정다각형이라는 정다면체 조건을 만족하지 않는다. 직각삼각형을 한 직각변 둘레로 회전하면 그 변이 높이, 다른 직각변이 밑면 반지름, 빗변이 모선인 직원뿔이 생긴다.',
   '볼록 다면체와 회전체를 구체 모형으로 탐구하도록 만든 과제다. 모형을 실제로 학생에게 제시하고 반응을 얻은 기록은 아직 없다.'),
  probe('SOLID-P2',V,'밑면 반지름 3cm, 수직 높이 4cm, 모선 5cm인 직원뿔의 옆넓이·겉넓이·부피를 구하라. 전개도 부채꼴의 반지름·호 길이·중심각·전체 둘레는 각각 무엇인가?',
   '옆넓이 15πcm², 겉넓이 24πcm², 부피 12πcm³다. 전개도 부채꼴의 반지름은 5cm, 호 길이는 밑면 원주 6πcm이며 전체 원주 10π의 3/5라 중심각은 216°다. 부채꼴의 전체 둘레는 10+6πcm로 호 길이와 다르다.',
   '겉넓이에는 밑면을 포함하고 부피에는 모선이 아니라 수직 높이를 쓴다. 서로 다른 두 반지름·호와 둘레를 구별한다.'),
  probe('SOLID-P3',V,'반지름 3cm인 구의 겉넓이와 부피를 구하라. 수치가 같으면 같은 양인가? 반지름을 두 배로 하면 각각 몇 배인가?',
   '겉넓이는 36πcm², 부피는 36πcm³로 숫자만 같고 측정량과 단위가 다르다. 반지름 두 배에서 겉넓이는 4배, 부피는 8배다. 구의 공식을 유한 개의 각뿔 합으로 정확히 증명했다고 말하지 않는다.',
   '제곱·세제곱 단위와 확대에 따른 변화를 나눈다. 원문 부피 예의 cm² 오기를 자체 답에 옮기지 않는다.'),
 ],
}
REUSED_OBSERVATIONS={
 NS:[
  probe('NSWMG-P1',A,'반지름 3cm, 중심각 120°인 부채꼴의 호 길이·넓이·전체 둘레를 구하고 전체 원에서 차지하는 몫으로 설명하라.',
   '120/360=1/3이므로 호 길이는 2πcm, 넓이는 3πcm²다. 전체 둘레는 호 길이에 반지름 두 개를 더한 6+2πcm다.',
   '접은 원의 분수 몫 활동과 AMSI 원주·넓이 및 원뿔의 호 비율 설명을 함께 참고한 자체 중학교 확장이다. 호와 둘레를 구별한다.'),
  probe('NSWMG-P2',A,'중심각이 같은 두 부채꼴의 반지름이 3cm와 6cm다. 호 길이와 넓이는 같은가? 배율로 설명하라.',
   '같은 중심각이라 전체 원의 같은 몫이지만 원의 크기가 다르다. 반지름 6인 쪽의 호 길이는 2배, 넓이는 4배다. 같은 원 또는 반지름이 같은 원이라는 조건 없이 각만으로 길이·넓이 같음을 단정할 수 없다.',
   '동일한 각의 몫과 실제 길이·넓이의 크기를 구별하며 일반 각도 계산은 자체 중학교 확장임을 유지한다.'),
 ],
 SA:[
  probe('SAMG-P1',M,'모서리 1cm인 단위 정육면체 12개로 2×2×3과 1×2×6 직육면체 모형을 만들어 부피와 겉넓이를 비교하라. 두 모형의 면·모서리·꼭짓점 수도 비교하라.',
   '두 부피는 모두 12cm³지만 겉넓이는 각각 2(4+6+6)=32cm², 2(2+12+6)=40cm²다. 두 직육면체 모두 면 6개·모서리 12개·꼭짓점 8개이며 각 면 안에 보이는 단위 정육면체 경계선을 새 모서리로 세지 않는다.',
   '원문 24개 과제를 자체 12개 모형으로 바꾸었다. 같은 부피와 같은 겉넓이 및 다면체의 면·모서리 수를 구별한다. 실제 학생 조작·응답 기록은 아직 없다.'),
 ],
}
DETAILS={
 PL:dict(plane_context_not_all_space=True,page_11_cointerior_unequal_has_90_degree_exception=True,convex_polygon_generalisation_is_own=True),
 CT:dict(perpendicular_bisector_common_radius_greater_than_half_segment=True,circumcenter_vertex_distances=True,incenter_perpendicular_side_distances=True,circumcenter_three_triangle_types=True),
 CG:dict(unique_up_to_congruence=True,triangle_inequality_required=True,page_15_wrong_SAS_is_deliberate=True,SSA_not_general_test=True,ASA_used_in_own_tasks=True,obtuse_extension_not_required=True),
 SM:dict(part_remainder_ratio='1:k',part_whole_ratio='1:(k+1)',midpoint_congruence_alternative_retained=True,three_parallel_transversals_is_own_extension=True),
 CI:dict(diameter_midpoint_equals_center_exception=True,page_12_printed_triangle='OAQ',page_12_proof_uses_triangle='OBP',same_intercepted_arc_required=True,major_arc_reflex_angle=True,tangent_segment_not_infinite_line=True,circle_proportionality_not_required=True),
 SO:dict(right_cones_only_in_net_tasks=True,perpendicular_height_distinct_from_slant_height=True,page_10_sector_circumference_means_arc=True,page_12_volume_unit_printed='cm2',correct_volume_unit='cm3',page_12_pyramid_height_printed='x',correct_pyramid_height='h',finite_pyramid_approximation_not_rigorous_proof=True),
}
CORRECTIONS={
 PL:'평면 문맥의 두 직선 위치를 공간 전체에 확장하지 않았다. 11쪽 co-interior angles are not equal은 수직 횡단선의 90°·90°에서 맞지 않으며 합 180°를 정확한 성질로 썼다. 16쪽 사각형 분할에서 볼록 n각형으로의 일반화는 자체 설명이다.',
 CT:'수직이등분선의 교점 작도에는 두 반지름이 같다는 것과 선분 절반보다 크다는 조건을 함께 명시했다. 외심의 꼭짓점 거리와 내심의 변에 내린 수선 거리를 구별했다. 수심·무게중심·구점원은 이번 추가 필수로 옮기지 않았다.',
 CG:'9쪽의 유일성은 up to congruence이며 대칭인 두 교점의 위치가 하나라는 말이 아니다. 14·15쪽의 끼이지 않은 각 반례와 의도적 wrong SAS를 문서 오류로 잘못 집계하지 않았다. 길이·각의 비퇴화 조건과 국내 ASA 범위를 유지했다.',
 SM:'1:k인 부분 대 나머지와 1:(k+1)인 부분 대 전체를 원문 23·24쪽 판면에서 구별했다. 중점 사례를 합동만으로도 증명할 수 있다는 설명을 보존해 닮음의 보편적 필요성을 주장하지 않았다. 세 평행선은 자체 확장이다.',
 CI:'7쪽은 중심을 지나지 않는 현으로 시작한다. 지름에서 O=M인 경계를 별도 명시했다. 11·12쪽의 세 중심 위치·큰 호의 큰 각을 읽었고, 12쪽 첫 줄 OAP and OAQ는 이어지는 밑각·외각 증명의 OAP와 OBP에 맞지 않아 문자 불일치로 기록했다. 같은 현과 같은 호를 바꾸지 않는다. 접선의 길이는 선분 길이다.',
 SO:'10쪽 circumference of the sector는 문맥상 호 길이로, 전체 둘레와 다르다. 12쪽 원기둥 부피 375π cm²는 cm³이어야 하고 밑변 c,d·높이 h인 각뿔은 cdh/3이지 cdx/3이 아니다. 사선 입체·카발리에리 증명·적분은 국내 추가 필수로 요구하지 않는다. 유한 근사 그림과 엄밀한 증명을 구별한다.',
}
INTERPRETATIONS={
 ('SEC_9수03-09_C04','CONGR11-02'):('activity_context',
  '반지름이나 수직이등분선에서 얻는 등거리를 이등변삼각형·합동으로 설명하고 외심의 꼭짓점 거리와 내심의 수선 거리를 대조한다.',
  '원문 지정 증명과 이 관계의 대표 거리 설명에 한정한다. 같은 거리라는 말만으로 거리 대상을 바꾸거나 한 중심이 항상 내부에 있다고 일반화하지 않는다.'),
 ('SEC_9수03-02_C04','SIM11-02'):('activity_context',
  '실제 평행 조건에서 얻은 동위각·엇각을 닮음의 대응 근거로 쓰고 부분 대 나머지와 부분 대 전체의 비를 나눈다.',
  '원문 삼각형·교차형 예와 자체 대응 과제의 참고다. 평행을 확인하지 않은 그림의 같은 위치 각을 같다고 가정하지 않는다.'),
 ('REV-9수03-02-1','SIM11-02'):('inference_limit',
  '평행선의 각은 여기 기록한 AA 닮음 풀이의 근거지만 중점 사례에는 합동을 이용하는 다른 설명도 있다.',
  '교사 자료의 풀이 연결을 모든 학생에게 필요한 유일한 선행 숙달·수업 순서나 교수 효과를 검증한 연구로 해석하지 않는다.'),
 ('REV-9수03-06-1','SOLID11-03'):('activity_context',
  '직원뿔 전개도의 부채꼴 반지름은 모선, 호 길이는 밑면 원주라는 대응으로 옆넓이를 설명한다.',
  '호에 두 모선을 더한 전체 둘레를 원주와 같다고 놓지 않는다. 밑면 반지름·모선·수직 높이를 구별하며 이 방법을 유일한 필수 순서로 삼지 않는다.'),
 ('REV-9수03-07-1','SOLID11-03'):('activity_context',
  '직원뿔의 옆면·모선과 밑면을 구별해 부채꼴 전개도와 원인 밑면의 넓이 합을 설명한다.',
  '이 직원뿔 전개도 과제의 표현 대응에 한정한다. 구·사선 원뿔의 전개도나 모든 입체의 측정을 이 방법으로 처리할 수 있다는 뜻은 아니다.'),
}
REUSED_INTERPRETATIONS={
 ('REV-9수03-07-1','SA-MG11-01'):('inference_limit',
  '단위 정육면체 모형은 같은 부피와 다른 겉넓이를 비교하는 한 방법이며 원문 24개 과제를 자체 12개로 바꾸었다.',
  '모형·전개도 설명을 모든 학생의 유일한 선행 숙달이나 국내 학생에게 확인한 교수 효과로 세지 않는다. 다면체의 모서리와 단위 정육면체의 겉면 경계선을 구별한다.'),
}


def extend_existing():
    registry=load_registry()
    ids={cid for _,cid,*_ in REUSED_CLAIMS}
    present=ids & {r['id'] for r in registry['claims']}
    if present:
        assert present==ids
        return
    queue=load(ROOT/'data/content_review_queue.json')
    previous_sources={sid:dict(snapshot_sha256=registry['sources'][sid]['snapshot_sha256'],
                               bibliography_snapshot=registry['sources'][sid]['bibliography_snapshot']) for sid in REUSED_OBSERVATIONS}
    reuse={NS:('nsw-stage4-measurement',[40,41]),SA:('ncetm-surface-area-2019',[8,29,32])}
    for sid,(stem,pages) in reuse.items():
        source=registry['sources'][sid]
        note=load(ROOT/source['snapshot_file'])
        assert sha(ROOT/source['snapshot_file'])==source['snapshot_sha256']
        assert sha(ROOT/'tmp/literature/upper-primary-gaps'/f'{stem}.pdf')==source['source_pdf_sha256']
        assert set(pages)<=set(note['selected_text_pages'])
        assert not source['empirical_scope']['student_outcome_study']
        assert not {r['id'] for r in REUSED_OBSERVATIONS[sid]} & {r['id'] for r in source['observations']}
        source['observations'].extend(REUSED_OBSERVATIONS[sid])
        row=next(r for r in queue['literature_review'] if r['source']['id']==sid)
        row['claim_ids'].extend(cid for src,cid,*_ in REUSED_CLAIMS if src==sid)
    new={}
    for sid,cid,codes,pages,support,limit in REUSED_CLAIMS:
        source=registry['sources'][sid];note=load(ROOT/source['snapshot_file'])
        new[cid]=dict(id=cid,source_id=sid,role='mathematical_explanation',empirical_scope=source['empirical_scope'],
          standard_codes=codes,locations=[f'{note["source_pdf_url"]}#page={p}' for p in pages],support=support,does_not_establish=limit,
          independent_review=False,student_validated=False,target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes})
    registry['claims'].extend(new.values())
    relations=load(ROOT/'data/revised_relations.json')['relations'];by_relation={r['id']:r for r in relations}
    pairs={(r['id'],cid) for r in relations for cid,c in new.items() if all(r[k].startswith('standard:') for k in ('from','to')) and {r[k][9:] for k in ('from','to')}<=set(c['standard_codes'])}
    assert pairs==REUSED_INTERPRETATIONS.keys(),pairs
    reviewed=load(ROOT/FILE)
    for (rid,cid),(role,finding,limit) in REUSED_INTERPRETATIONS.items():
        c=new[cid]
        reviewed['records'].append(dict(relation_id=rid,claim_id=cid,role=role,finding=finding,limit=limit,
          relation_snapshot=relation_snapshot(by_relation[rid]),claim_snapshot=claim_snapshot(c,registry['sources'][c['source_id']])))
    apply_literature_context(relations,registry,registry=reviewed)
    assert all(previous_sources[sid]=={k:registry['sources'][sid][k] for k in previous_sources[sid]} for sid in previous_sources)
    write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed)
    build_report()


if __name__=='__main__':
    assert sqrt(13**2-5**2)*2==24 and sqrt(10**2-6**2)==8
    assert (8-2)*180==1080 and 8*(8-3)//2==20
    assert 2*(2*2+2*3+2*3)==32 and 2*(1*2+1*6+2*6)==40
    assert 360*3/5==216 and 3*5+3**2==24 and 3**2*4/3==12
    record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,
      interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='중학교 도형·측정의 교사용 수학·표현 참고',
      detail_key='middle_geometry_review',roles={cid:'mathematical_explanation' for _,cid,*_ in CLAIMS})
    extend_existing()

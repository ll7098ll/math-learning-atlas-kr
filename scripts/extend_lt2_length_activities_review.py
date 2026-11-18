"""Review every pending length-linked public body, keeping attachments separate."""
import copy,hashlib,json,re
from decimal import Decimal
from urllib.parse import urljoin
from literature_review import ROOT,digest,target_value,load_registry,build_report
from relation_analysis_review import load_reviews
from record_lt2_public_review import SOURCE,URL
from extend_lt2_measurement_pdf_review import NOTES as PRIOR_NOTES

NOTES='data/literature_evidence/CLEMENTS_SARAMA_LT_length_activities_review_notes.json'
PRIOR_SHA='2aa2183f8dc7932bd299f844812147484494015733e4c403b47a46a893de6172'
NIST='https://www.nist.gov/pml/owm/si-units-length'
INTRO_SLUGS=['math-at-home-measurement','measurement-talk']
TEACHER_SLUG='researcher-note-building-blocks-measures'
SCOPE='공식 공개HTML 누적405개 지정 영어 본문: 일반6·영역 개요20·수준224·활동153·교사자료2. 기록된224수준의 목록에서 길이에 연결된 미검토61페이지를 추가로 읽었다. 실제 활동 설명58개·첨부 소개2개·교사 해설1개를 구별한다. 이전110개 삽입 이미지URL과 수학PDF16URL/19쪽의 확인을 보존했으며 이번 길이 페이지의 그림/첨부/영상은 새로 읽은 것으로 세지 않는다.824개 활동/교사자료URL 중155개 공개 영어페이지 본문 읽기·669개 본문 대기다. 보조로 NIST 길이FAQ의 인치 정의를 확인했으며 의학 원연구/신체 규준을 검증한 것이 아니다. 전체사이트·모든 첨부/교재/원연구·번역·실제 독립/학생 검증 완료가 아니다.'

READING_NOTES=[
 '실물 크기 그림책의 이빨4인치와 상어21피트는 서로 다른 단위다. 복사 배율·두 끝·직선 배치를 확인하고 책 본문/실제 동물을 측정한 것으로 세지 않는다.',
 '만들기 놀이의 길다/짧다·크다/작다 어휘와 정확한 정량 측정을 구별한다. 큰 손자국은 특정 한 방향 길이가 아니다.',
 '어깨/손끝 등 공통 끝을 정한다.13.4인치와25cm 병기는 환산상 일치하지 않는다. 원연구의 팔/아래팔 구간·합산 표준편차·현재 학생 규준은 미검토다.',
 '화상/사진 속 장난감의 상대 크기는 촬영 거리와 배율에 좌우된다. 실제 같은 장난감의 지정 길이와 화면에서 보이는 크기를 구별한다.',
 '같은 블록의1–6 계단은 총21개다. 두 번째 위치와 블록2개가 일치하는 것은 제시한 이 배열의 조건이다. 수와 길이·모터 조작 도움을 구별한다.',
 '1–5 계단은 총15개다. 시작 기준과 같은 블록·순서를 명시하고,조립해 준 계단을 순서대로 놓기와 직접 수량을 만드는 수행을 따로 기록한다.',
 '측정 도구를 줄여도 대상 길이는 그대로다. 남은 물리 막대 수와 반복한 단위 수를 구별하고 다음 시작 위치를 보존한다.',
 '같은 크기 블록을 쌓고 한 끝을 맞출 때 높이와 개수를 연결한다. 더 큰 블록/다른 방향/빈틈에서는 높이만으로 개수를 판정하지 않는다.',
 '쌓기 놀이의 높이/길이 비교다. 서로 다른 모양 블록의 개수를 정량 길이로 바꾸지 않는다.',
 '건설물과 보이는 기준물을 비교하는 안내다. 사진 재현·수학 어휘를 실제 측정/현재 학생의 독립 설명으로 세지 않는다.',
 '생활 놀이의 길이 어휘와 참여 안내다. 속도/낮잠 시간/재료 양 등 다른 속성을 길이와 구별하고 언어 반응만으로 단계나 효과를 판정하지 않는다.',
 '같은 크기 버스/트럭을 단위로 끝끼리 잰다.8이라는 수뿐 아니라8버스라는 단위와 대상 끝을 기록한다.',
 '처음 점프의 시각 비교 뒤 다시 점프해 측정한다. 서로 다른 시행을 같은 점프의 검산으로 기록하지 않고 출발/착지 기준을 고정한다.',
 '동물집의 높이와 길이를 구별한다. 한 방향이 충분한 것과 입구/안쪽 공간 전체에 실제로 들어가는 조건은 다르다.',
 '왕/견습생의 서로 다른 발 단위로 같은6×3을 만들면 실제 길이/넓이는 달라진다. 이야기의 발과 표준피트·그림책 전체 읽기를 구별한다.',
 '지도에서 선 끝을 기준으로 끈을 옮기는 간접 비교다. 인쇄100%와 끈 길이 보존을 확인한다. 끝이 끊긴 추가 발판 문장은 임의 복원하지 않는다.',
 '8등분7점·4등분3점·2등분1점과 간격 수를 구별한다. 종이 전체를 접은 자국은 임의 위치/길이 선분의 등분점을 자동으로 검증하지 않는다.',
 '블록 놀이의 어휘/참여 안내다. 접착/큰 블록/사전 그림/성인 서술과 독립 수학 수행을 구별하며 첨부 사회적 이야기는 미검토다.',
 '길이 수수께끼는 정수 단위에 거의 정확히 맞는 물건을 의도한다. 정확히/약/남은 부분을 구별하고 다른 단위나 반 단위를 임의로 정수 처리하지 않는다.',
 '한두 블록으로 단위를 반복하는 수수께끼다. 실제 블록 수1/2개와 이동/배치한 단위 수를 구별하고 남은 구간을 표시한다.',
 '같은 정사각형6개로 도서관 외곽을 구성한다. 겹침/모서리 접촉/구멍을 허용하는지 정하고 안쪽 공유변을 외곽 둘레에 더하지 않는다.',
 '블록 높이와 연속 길이 띠의 순서를 구별한다. 이야기의 가족 나이/역할과 실제 키의 순서는 일반적으로 같다고 하지 않는다.',
 '둘레를 유지한 다른 모양 구성이다. 같은 둘레는 같은 넓이/같은 단위 조각 수/합동을 보장하지 않으며 첨부 전체 예는 미검토다.',
 '빨간 막대 한 개를1로 표시한 자는 막대 단위 자다.1을1cm로 바꾸지 않고0부터 한 간격이 뜻하는 길이를 명시한다.',
 '가정용 측정 안내의 소개만 있고 실제 활동 절차가 없다. 공개페이지 읽기와 배포 자료 전체 읽기를 구별한다.',
 '7×5 직사각형의 둘레는24다. 다른24둘레의 직사각형/다각형과 비교할 때 길이 단위와 양의 변 길이를 명시한다.',
 '발자국 띠의 묶음 단위와 남은 부분을 구별한다.30개 작은 단위는15개 묶음으로2개다. 사람별 발 크기 차이를 오차나 능력 차이로만 해석하지 않는다.',
 '같은 길이 벌레에 빈틈을 둔2개 단위를 놓는 오류와 정확히 이어3개를 놓는 수정을 대조한다. 벌레 모양/자세가 바뀌면 측정하는 경로와 높이를 구별한다.',
 '출발선과 착지 기준을 먼저 정한다. 실제 비행 경로·시작점에서의 직선·출발선으로부터의 수직 거리는 다른 측정량이며 끈 하나로 비행 궤적을 복원하지 않는다.',
 '개인별 신체 기준의 길이 차이와 약15cm 예를 구별한다. 물건 선택·가족 도움·실제 측정을 따로 기록하고 문화/소유물에서 능력을 추정하지 않는다.',
 'Activity 표제는 있으나 측정 말하기 배포 자료를 소개하는 문장뿐이다. 첨부를 읽은 것으로 세지 않는다.',
 '신발 뒤꿈치/같은 끝을 맞춰 길이를 비교한다. 외부 밑창 길이만으로 실제 착용감/발 전체 크기를 판정하지 않는다.',
 '한 블록의 끝을 표시하며 반복한다. 책의 지정 변을 정하고 단순 미끄러뜨리기/말한 수와 정확한 반복을 구별한다.',
 '제목/목표는 모임 비교지만 실제 절차는4인치 띠를1인치/2인치 단위로 재는 역관계다. 인형의 큰 단위면 큰 수라는 말은 의도한 오답이다.',
 '1인치 블록 네 개라는 맥락과4인치 블록이라는 모호한 표기를 구별한다. 부족한 도구·혼합 단위·빈틈·끝 불일치·잘못된 자 사용을 각각 기록한다.',
 '한 블록 미끄러뜨리기/불규칙 반복/단위 크기 변경의 오류를 구별한다. 인형의 큰 단위면 더 많다는 주장은 의도한 오답이며 실제 단위 규격을 확인한다.',
 '야외의 보폭/팔 뻗기/점프 길이 어휘다. 다른 사람의 보폭 수를 같은 표준 길이로 합산하지 않는다.',
 '같은 둘레의 직사각형 구성이다. 양의 정수 변으로 제한한 유한 경우와 실수 길이까지 허용한 모든 경우를 구별한다.',
 '같은 줄 길이를 갈색4/보라8/빨강16 막대로 나타내는 예다. 색 이름이 아니라 실제 단위 길이의 두 배 관계를 확인한다. 그림/결과표는 별도다.',
 '구멍과 끼울 띠의 길이 맞춤으로 확인한다. 같은 길이만으로 폭/두께/모양까지 들어맞는 것은 아니며 도움 후 다시 예상한 값은 최초 예상과 다르다.',
 '교사자료1개다. 높이/덮은 바닥/블록 수라는 서로 다른 큰 속성을 구별하는 해설과 서술 사례를 읽었으며 인용 원연구나 실제 관찰 원자료를 읽지 않았다.',
 '일상 루틴에는 길이뿐 아니라 온도/들이/시간/속도/무게 어휘도 섞인다. 수학 속성을 지정하고 반복한 발화를 실제 측정으로 세지 않는다.',
 '같은 우주선 길이의 파란9/초록18단위는 단위 크기 차이다. 선형 단위와 정사각형 칸 넓이를 구별하고 실제 첨부 배율은 미검토다.',
 '높이/폭/길이는 한 방향의 길이 속성이지만 전체 크기/면적/부피와 다르다. 관찰 어휘와 수치 측정·장식 사진의 길이를 구별한다.',
 '이동할 수 없는 틈을 여러 단위로 재어 같은 단위의 테이프를 가져온다. 벽/바닥 서술 차이·정수 길이·도구/도움과 다시 확인하는 시점을 구별한다.',
 '틈 길이를 끈/띠로 보존해 옮기는 간접 비교다. 운반하며 늘거나 표시가 바뀌지 않는 같은 기준물을 사용하며 붙임 면적/보수 성능을 판정하지 않는다.',
 '한두 단위 반복과 자체 자 제작의 예다. 정수5–8인치 틈·늘어나지 않는 테이프 조건이 명시돼 있다. 실제 복사 단위와 동작 도움을 따로 확인한다.',
 '같은 지도 길이를 단위 블록으로 재며 수와 단위를 말한다. 도로 선의 끝과 건물 그림을 구별하고 인쇄 배율을 확인한다.',
 '간접 비교는 블록 묶음의 길이를 옮겨 비교하며 개수 세기를 새 필수로 요구하지 않는다. 다음 단계의 단위 세기와 같은 수행으로 집계하지 않는다.',
 '직각 경로의 구간 길이를 합산한다. 꺾임 수만으로 긴 길을 고르지 않으며 되돌아감 없는 경로와 우회/후진을 구별한다.12달러 요금은 실제 요금 규칙 없이 거리가 같다는 이유만으로 확정하지 않는다.',
 '같은 보물상자를 이동시켜도 길이는 보존되며 오른쪽 눈금값이 길이와 항상 같지는 않다. 실제 단위 간격과 두 끝을 확인한다.',
 '과자 띠의 길이를 같은 기준 끈으로 옮긴다. 길이가 같다는 것은 폭/두께/밀도/재료 양이나 실제 음식 분배가 같다는 뜻이 아니다.',
 '한두 단위로 과자 띠 길이를 반복해 복제한다. 같은 단위 규격과 끝 표시·공급된 도구·도움 뒤 수정/확인을 구별한다.',
 '여러 단위로 과자 띠를 재어 복제한다. 정수 길이/긴 공급 띠/같은 단위·그림과 실제 음식의 차이를 명시한다.',
 '식물 높이를 자기 몸에 비추어 말한다. 기준 사람/자세/촬영 배율이 달라질 때 식물 성장량을 역산하지 않으며 책/영상/국가별 농사 속담을 현재 규준으로 전용하지 않는다.',
 '1–10–1의19위치에는9개 높이 막대가 두 번 나온다. 높이9와 왼쪽9번째 위치를 구별하며 두 번째9는 원래11번째다. 준비 블록은 총100개다.',
 '2cm 단위를 반복하는 자전거길 과제다.7단위와8단위가 다르면 실제 도구 크기/끝/반복 위치부터 확인하며 다수의 일치를 정밀 측정 증거로 바꾸지 않는다.',
 '탁자 폭과 문 폭의 간접 비교다. 폭 하나가 맞는다는 사실만으로 높이/깊이/기울임/회전/통로 조건까지 통과한다고 하지 않는다.',
 '구부러진 길은 지정 경로의 구간 길이를 합한다. 아래에서 위 높이나 양 끝을 이은 직선으로 대체하지 않고 곡선의 직선 조각 근사는 정확한 경로 길이와 구별한다.',
 '단위 자 제작과 빈 선로에 맞는 조각 찾기를 서로 다른 날 실시한다.1막대 눈금은1cm와 다르다. Letter/Legal 이름과 표기 치수만으로 실제 PDF 배율/조각 맞음을 확정하지 않는다.',
 '야드 단위의 시각적 분절 어림 안내다. 첨부의 실제 분절 예는 미검토이며 미국 길이 체계를 국내 저학년 새 필수로 넣지 않는다.',
]

OBSERVATIONS=[
 dict(id='LT-P37',standard_codes=['2수01-01','2수03-06'],question='같은 크기 블록으로 높이가1·2·3·4·5·4·3·2·1개인 계단9개를 왼쪽부터 놓는다. 먼저 블록4개 높이인 계단을 모두 짚고 각각 왼쪽에서 몇 번째인지 말하라. 원래 여섯 번째 계단을 가리고 빈 자리도 없애면,빠진 계단의 높이와 원래 위치를 모두“4”라고 기록해도 되는가?',expected='블록4개 높이인 계단은 원래 왼쪽4번째와6번째다. 가린 계단은 높이4개·원래위치6번째이며 두 수의 뜻이 다르다. 빈 자리를 없앤 뒤 남은 계단은8개지만 원래 위치를 말하는 약속은 바뀌지 않는다. 한 기준 끝을 맞춘 같은 블록의 높이를 비교하며 전체 계단9개와 준비한 블록25개도 구별한다.',interpretation='같은 높이가 두 번 나오는 자체 배열이다. 길이/블록 수/위치/원래와 현재 순서를 구별하고 방향·가림·교사의 간격 도움을 기록한다. 원문의1–10–1에서 두 번째9개 높이는 원래11번째이며9번째로 소급하지 않는다. 눈감기나 말하기를 필수 반응 방식으로 요구하지 않고 가리키기/카드로도 뜻을 확인한다. 이 작은 범위 성공을100까지 세기 전체의 검증으로 쓰지 않는다.',student_validated=False),
 dict(id='LT-P38',standard_codes=['4수01-09','4수01-10'],question='교사가 가로16cm 종이에 왼쪽 끝에서2cm 떨어진 곳부터10cm 떨어진 곳까지 길이8cm 선분을 그렸다. 이 선분을 같은 길이4부분으로 나누려고 종이 전체를 두 번 반으로 접어4·8·12cm 위치에 접는 자국을 만들었다. 이 자국이 모두 선분의4등분점인가? 선분을 기준으로 한 등분점과 한 부분의 분수를 설명하라.',expected='선분의 두 끝은2·10cm이고 길이는8cm다. 같은 길이4부분은2cm씩이므로 선분의 안쪽 등분점은4·6·8cm이며 한 부분은 이 선분 전체의1/4이다. 종이의4·8·12cm 자국은 종이 전체의4등분점이고12cm는 선분 밖이다. 선분 가운데는6cm로 종이 가운데8cm와 다르다. 안쪽 점3개가 간격4개를 만들며,선분을8등분하려면 안쪽 점7개가 필요하다.',interpretation='3~4학년 등분할을 위한 자체 치수/전체 조건이다. 위치 수는 교사가 자로 확인할 수 있으나 좌표 체계나 외국 길이 단위를 새 필수로 요구하지 않는다. 종이를 접어 임의 선분의 등분을 확인하려면 선분 양 끝과 접을 기준을 먼저 맞춘다. 최초 눈대중 표시·기준 맞추기 도움·접은 뒤 수정을 따로 기록하고 종이 전체와 선분 전체를 섞지 않는다.',student_validated=False),
 dict(id='LT-P39',standard_codes=['2수03-10','2수03-13'],question='한 칸의 길이가1cm인 모눈 길에서 같은 출발점으로부터 A는오른쪽6칸·위4칸, B는오른쪽2칸·위1칸·오른쪽4칸·위3칸, C는오른쪽7칸·왼쪽1칸·위4칸을 간다. 각 구간은 모눈 선을 따라 이동한다. 꺾인 횟수가 많으면 반드시 더 긴가? 도착점이 같으면 세 경로 길이도 같은가?',expected='A와B는 각각6+4=10cm,2+1+4+3=10cm로 길이가 같다. C는7+1+4=12cm여서2cm더 길지만 세 도착점은 모두 출발점에서 오른쪽6칸·위4칸인 같은 곳이다. 꺾인 횟수와 경로 길이는 다르고, C는 오른쪽으로 간 뒤1칸 되돌아오는 구간을 길이에 더해야 한다. 출발선에서 위로4칸이라는 거리나 양 끝을 바로 잇는 길이로 실제 경로 합을 대체하지 않는다.',interpretation='자체cm 모눈 경로이며 좌표식/직선 거리 공식·속력·실제 택시 요금을 요구하지 않는다. 오른쪽/위로만 진행한 경우의 같은 수평/수직 합과 되돌아감 있는 경우를 구별한다. 실제 운임은 요금 규칙·대기 등 조건 없이는 정하지 않는다. 첫 점프의 시각 예상과 다시 점프해 측정한 값을 같은 시행으로 합치지 않고 시행ID·시작/착지 기준·허용 경로를 따로 기록한다.',student_validated=False),
 dict(id='LT-P40',standard_codes=['6수03-11','6수03-13'],question='한 변1cm인 같은 정사각형으로 겹침·빈틈 없이5행1열 직사각형A와4행2열 직사각형B를 만든다. 각 직사각형의 바깥 경계를 따라 둘레를 재고,내부에 덮인 단위 정사각형 수로 넓이를 확인하라. 같은 둘레라는 이유로 같은 넓이·같은 모양·같은 타일 수라고 해도 되는가?',expected='A의둘레는2×(5+1)=12cm·넓이5cm²이고 B의둘레는2×(4+2)=12cm·넓이8cm²다. 둘레는 같아도 넓이·대응 변 길이·필요한 타일 수는 다르다. 타일 사이에 공유하는 내부 변은 바깥 둘레에 더하지 않는다. 같은 넓이여도 둘레가 다를 수 있다는 이전12타일 비교와,같은 둘레여도 넓이가 다를 수 있다는 이번 비교는 서로 다른 방향의 판단이다.',interpretation='자체12cm 둘레 예이며 구멍/겹침/모서리만 접한 배열은 제외했다. 같은 둘레 도서관 활동에서 허용 도형·변 길이/단위·바깥 경계를 먼저 정한다. 직사각형의 양의 정수 변으로 제한하면 유한한 경우를 확인할 수 있지만 모든 실수 변 길이까지 전수 확인했다고 하지 않는다. 원본 첨부의 전체 예/실제 제작/학생 설명은 별도다.',student_validated=False),
]

MAPPINGS=[
 ('LT37',['2수03-06','2수03-10','2수03-12','2수03-13'],[0,2,6,7,11,14,15,18,19,23,26,27,29,31,32,33,34,35,38,39,40,42,44,45,46,50,51,52,53,54,56,57,59,60],'같은 단위의 규격·반복 위치·공통 끝·도구 수/단위 수·기준물 보존과 지정 길이를 구별하는 기존 자체 설계를 보완한다.','13.4인치=25cm라는 원문 병기를 그대로 옮기지 않는다. NIST의1인치=25.4mm 정의로 환산하면34.036cm다. 의학 원연구/현재 아동 규준은 미검토이며 국내 저학년의 외국 단위 환산을 새 필수로 넣지 않는다. 한 방향 길이/화면 크기/사진 수만으로 실제3차원 맞음·부피·음식 양을 확정하지 않는다.'),
 ('LT38',OBSERVATIONS[0]['standard_codes'],[4,5,21,55],'반복된 같은 높이의 양과 순서 위치,공유한 길이 기준과 배열의 전후 상태를 구별하는 자체 설계에 참고한다.','원문의1–10–1에서9개 높이의 두 위치9/11을 같은9번째로 통합하지 않는다. 가족 나이/역할·블록 수·계단 위치·물리적 높이는 서로 다른 속성이며 한 과제의 성공으로 전체 단계/연령 규준을 판정하지 않는다.'),
 ('LT39',OBSERVATIONS[1]['standard_codes'],[16,23,60],'단위 전체의 양 끝·등분점과 간격 수·종이 전체/선분 전체·도움 전후를 구별하는 자체 등분할 설계에 참고한다.','종이 전체의 접는 자국이 임의로 그린 선분의 등분점이라는 보장은 없다. 처음 눈대중 예상과 접어 확인한 뒤 답을 구별하고 야드/피트/8등분을 국내 저학년의 새 필수로 전용하지 않는다.'),
 ('LT40',OBSERVATIONS[2]['standard_codes'],[12,15,28,47,48,49,56,58],'지정 경로의 구간 합·직선/수직 거리·되돌아감·공통 끝/배율·같은 시행의 예상/측정을 구별하는 자체 설계에 참고한다.','직각/같은 도착점/꺾임 수만으로 모든 경로가 같은 길이라고 하지 않는다. 실제 비행 경로를 착지점의 끈 측정으로 복원하거나 같은 거리에서 실제 요금을 확정하지 않는다. 끊긴 절차·첨부 지도·현재 학생 수행/교수 효과는 별도다.'),
 ('LT41',OBSERVATIONS[3]['standard_codes'],[20,22,25,37],'같은 둘레의 다른 직사각형과 넓이·합동·타일 수,바깥 경계와 내부 공유변의 조건을 구별하는 자체 설계에 참고한다.','같은 넓이⇒같은 둘레와 같은 둘레⇒같은 넓이는 각각 성립하지 않을 수 있다. 허용 도형/빈틈/겹침/구멍·변의 수 범위를 지정하고 일부 정수 예를 모든 실수 도형의 전수 탐색으로 승격하지 않는다.'),
]

def verify():
 assert len(READING_NOTES)==61 and len(OBSERVATIONS)==4 and len(MAPPINGS)==5
 assert Decimal('13.4')*Decimal('2.54')==Decimal('34.036')!=Decimal('25')
 assert sum(range(1,11))+sum(range(1,10))==100
 heights=[1,2,3,4,5,4,3,2,1];assert sum(heights)==25 and [i for i,v in enumerate(heights,1) if v==4]==[4,6]
 assert (10-2)/4==2 and [2+2*i for i in range(1,4)]==[4,6,8] and 2+(10-2)/2==6
 routes=[[(6,0),(0,4)],[(2,0),(0,1),(4,0),(0,3)],[(7,0),(-1,0),(0,4)]]
 assert [(sum(x for x,y in r),sum(y for x,y in r)) for r in routes]==[(6,4)]*3
 assert [sum(abs(x)+abs(y) for x,y in r) for r in routes]==[10,10,12]
 assert 2*(5+1)==2*(4+2)==12 and 5*1==5 and 4*2==8
 assert sum(range(1,7))==21 and sum(range(1,6))==15 and 7*5==35 and 2*(7+5)==24
 assert 30/15==2 and 32/8==4 and 32/4==8 and 32/2==16

def main():
 verify();registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:
  assert {m[0] for m in MAPPINGS}<={c['id'] for c in registry['claims']}
  print('LT2 length activity reading remains current; no automatic refresh');build_report();return
 assert s['snapshot_file']==PRIOR_NOTES and s['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 old=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews());prior=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'));D=ROOT/'tmp/literature/lt2-length-activities'
 pages=json.loads((D/'activity-manifest.json').read_text(encoding='utf-8'));selection=json.loads((D/'selection.json').read_text(encoding='utf-8'))
 expected=[a for a in prior['activity_followup_catalog']['records'] if not a['body_read'] and any('/measurement-length/' in u for u in a['linked_level_urls'])]
 assert expected==selection and len(pages)==len(selection)==61 and {a['url'] for a in pages}=={a['url'] for a in selection}
 assert [a['url'].split('/')[-1] for a in pages]==[a['url'].split('/')[-1] for a in selection]
 kinds={};attachments={};unread_images={};logs=[];dates={}
 for a,note in zip(pages,READING_NOTES):
  assert a['status']==200 and a['url']==a['final_url'] and a['url'].startswith(URL) and hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256']
  text=(ROOT/a['file']).with_suffix('.txt').read_text(encoding='utf-8');slug=a['url'].split('/')[-1]
  kind='teacher_resource' if slug==TEACHER_SLUG else 'introduction_only' if slug in INTRO_SLUGS else 'activity_description'
  if kind=='teacher_resource':assert 'Type:\nTeacher Resources' in text
  if kind=='activity_description':assert '\nActivity\n' in text
  kinds[a['url']]=kind;logs.append(dict(url=a['url'],page_kind=kind,note=note))
  attachments[a['url']]=sorted(u for u in a['links'] if '.pdf' in u.lower() and '/downloads/' not in u)
  unread_images[a['url']]=sorted({urljoin(a['url'],v['src']) for v in a['images'] if '/upload/' in v.get('src','')}-{v['url'] for v in prior['image_read_manifest']})
 assert list(kinds.values()).count('activity_description')==58 and list(kinds.values()).count('introduction_only')==2 and list(kinds.values()).count('teacher_resource')==1
 assert len({u for v in attachments.values() for u in v})==8
 fields=['key','url','title','sha256','status'];assets=prior['html_read_manifest']+[{k:a[k] for k in fields} for a in pages]
 assert len(assets)==len({a['url'] for a in assets})==405
 groups=copy.deepcopy(prior['read_groups']);groups['activities'] += [a['key'] for a in pages if kinds[a['url']]!='teacher_resource'];groups['teacher_resources'] += [a['key'] for a in pages if kinds[a['url']]=='teacher_resource']
 assert {k:len(v) for k,v in groups.items()}==dict(general=6,domain_overviews=20,levels=224,activities=153,teacher_resources=2)
 followup=copy.deepcopy(prior['activity_followup_catalog']);read_urls={a['url'] for a in assets}
 for a in followup['records']:a['body_read']=a['url'] in read_urls
 followup.update(listed_body_read=sum(a['body_read'] for a in followup['records']),listed_body_pending=sum(not a['body_read'] for a in followup['records']))
 assert followup['listed_body_read']==155 and followup['listed_body_pending']==669
 assert not [a for a in followup['records'] if not a['body_read'] and any('/measurement-length/' in u for u in a['linked_level_urls'])]
 corrections=[dict(kind='unit_conversion_and_reference_scope',locations=[pages[i]['url'] for i in [0,2,14,29,54,59]],action='NIST길이FAQ의1인치=25.4mm정의를확인해13.4인치와25cm가같지않음을계산했다.13.4×2.54=34.036cm라는산술대조이며원문인체측정연구의평균/표준편차/구간/연령규준을확정하지않는다. 자기몸/사진/출력의공통기준·지정끝·측정방향을확인하고외국단위를국내새필수로추가하지않는다.'),dict(kind='repetition_tool_and_measurand',locations=[pages[i]['url'] for i in [6,11,18,19,23,26,27,32,33,34,35,38,42,44,45,46,50,51,52,53,56,57,58,59]],action='도구한개와반복단위수,눈금값과길이,막대1단위와1cm,고정길이/다른단위개수,높이/경로/폭/넓이/부피·실제맞음을구별한다. Mr.MixUp의4-inch모호표기는문맥상1인치블록네개라는조건으로명확히한다. 원문인형의의도한오답을저자의측정법으로복사하지않는다. 같은길이과자도폭/두께/밀도없이는재료양이같다고하지않는다.'),dict(kind='repeated_height_and_ordinal_position',locations=[pages[i]['url'] for i in [4,5,21,55]],action='1–10–1의19위치/블록100개/두9높이의위치9와11을구별한다. 두번째9를9번째로기록하지않고제거전후위치/현재남은수/방향을명시한다. 이야기속나이순과실제키순을보편규칙으로바꾸지않는다.'),dict(kind='subdivision_reference_endpoints',locations=[pages[i]['url'] for i in [16,23,60]],action='종이전체의접는자국과그위임의선분의등분점은다를수있다. 같은전체/끝을맞춘뒤등분하며내부점3개/4간격·7개/8간격을구별한다.6개선을그리라는준비문구와실제로비교하는선/접기단계를임의로새절차로복원하지않는다.'),dict(kind='path_trial_metric_and_fare',locations=[pages[i]['url'] for i in [12,15,28,47,48,49,56,58]],action='구간길이합·비행궤적·출발점직선·출발선수직거리는다른측정량이다. 같은끝점/직각/꺾임수만으로모든경로길이가같다고하지않고되돌아간길이도더한다. 다시점프한시행은첫시행의측정검산이아니다.12달러예는요금규칙/대기조건없이실제동일요금으로일반화하지않는다. IceCream의추가발판문장이중간에끊긴점과본문/지도끝/인쇄배율을분리기록한다.'),dict(kind='equal_perimeter_not_equal_area',locations=[pages[i]['url'] for i in [20,22,25,37]],action='같은넓이와같은둘레의서로다른방향판단을나누고내부공유변/바깥경계·양의정수변/실수변·겹침/구멍/모서리접촉을지정한다.7×5둘레24와5×1/4×2둘레12의자체대조를검산하며미검토첨부의정답을복원하지않는다.'),dict(kind='page_description_not_handout_or_study',locations=list(kinds),action='61공개페이지는활동설명58·소개2·교사해설1이다. MathAtHome과MeasurementTalk은배포자료소개뿐이며Activity표제유무만으로전체절차읽기를판정하지않는다. 교사해설의서술사례·일상어휘·사진·가족도움·블록조작/소통도움과실제독립수학수행을구별한다. 새그림/첨부8PDF/영상/그림책/원연구는별도다.')]
 p=ROOT/'data/sources.json';bibliography=json.loads(p.read_text(encoding='utf-8'));b=next(v for v in bibliography if v['id']==SOURCE);previous_b=copy.deepcopy(b)
 next_review='기록된824개활동/교사자료중155개공개영어본문읽기·669개대기다. 길이에연결된미검토61본문을확인했으나새그림/첨부8PDF·소개2페이지의실제배포자료/야드안내·인쇄지도/철도조각·영상/게임/그림책/원연구는별도다. 외부수학놀이매뉴얼2기존링크와교육청대체링크는직접파일요청403으로전체확보/이미지대조를완료하지못했다. 단위/전체/끝/제시조건/도움·순서/경로와요금가정을우선대조하고실제독립/학생검증으로승격하지않는다.'
 b.update(review_scope=SCOPE,next_review=next_review)
 notes=copy.deepcopy(prior);notes.update(date='2026-11-06',read_scope=SCOPE,previous_review=copy.deepcopy(s),previous_bibliography=previous_b,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,html_read_manifest=assets,observed_html_assets=assets,read_groups=groups,new_read_groups=dict(domain_overviews=0,levels=0,activities=60,teacher_resources=1,inline_images=0,supplementary_pdf_urls=0),reading_log=prior['reading_log']+['길이연결미검토61개공개페이지의지정영어본문을읽었다. 활동설명58·소개2·교사해설1을구별하며첨부/사진/원연구읽기로승격하지않는다.'],length_page_reading_log=logs,source_corrections=prior['source_corrections']+corrections,activity_followup_catalog=followup,catalog_coverage={**prior['catalog_coverage'],'read_activity_bodies':155,'pending_activity_bodies':669},completed_length_activity_records=selection,length_page_kinds=kinds,length_procedure_coverage=dict(selected_public_pages=61,activity_descriptions=58,introduction_only_pages=[URL+'math-activities/'+v for v in INTRO_SLUGS],teacher_resource_pages=[URL+'math-activities/'+TEACHER_SLUG],whole_linked_material_review=False),linked_length_attachments_not_read={k:v for k,v in attachments.items() if v},linked_length_inline_images_not_reviewed={k:v for k,v in unread_images.items() if v},unit_definition_fact_check=dict(url=NIST,selected_section='FAQ: When did the metric redefinition of the inch occur?',observed_definition='1 international inch =25.4mm exactly',own_calculation='13.4×2.54=34.036cm; not25cm',medical_original_study_read=False,whole_nist_site_review=False),external_manual_access_followup=dict(date='2026-11-06',urls_http_403=['https://nt.gov.au/__data/assets/pdf_file/0006/815568/maths-learning-games.pdf','https://nt.gov.au/_media/docs/education-and-learning/documents/preschool/maths-learning-games.pdf','https://education.nt.gov.au/__data/assets/pdf_file/0003/444567/nt-maths-games.pdf','https://education.nt.gov.au/media/docs/support-for-teachers/nt-maths-games.pdf'],official_landing_page='https://education.nt.gov.au/support-for-teachers/preschool-stem-games',web_cached_text_seen_scope='표지/소개/목차와일부초기세기본문을확인했으나40쪽전체/이미지는미검토다.',binary_file_obtained=False,identity_between_aliases_verified=False),unread_followups=[next_review,'이전16개수학PDF의19쪽확인만보존했고이번길이첨부8링크는미검토다. 원본HTML/그림/추출전체텍스트를이식용묶음에복제하지않는다.'])
 npath=ROOT/NOTES;npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=s['date'],read_scope=s['read_scope'])]
 s.update(date='2026-11-06',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),snapshot_history=history,bibliography_snapshot=digest(b),html_read_manifest=assets,read_scope=SCOPE,method_note='길이목록의남은61개공개본문을읽고활동설명58/소개2/교사자료1·단위환산/끝점/단위반복/등분전체/높이와위치/경로합/둘레와넓이를구별했다. 원문사진/새첨부/원연구는별도다.',limits='누적405개HTML/이전110개삽입이미지URL/이전수학PDF16URL19쪽범위다. 이번길이페이지의그림/첨부8PDF/영상/소개2실제자료/그림책/원연구·669개미검토공개본문·의학규준/현재학생능력·한국어진단정확도/효과는별도다. 외부매뉴얼은파일요청403으로별칭동일성/전권확보/이미지대조를완료하지못했다.',editorial_action='이전주장36건/관찰36건을보존하고9개기준에새주장5건/자체관찰4건을대응했다. 누적주장41건·관찰40건·기준48개다. 새본문읽기와관계검토·독립검토·학생검증을합산하지않는다.',observations=s['observations']+OBSERVATIONS)
 for cid,codes,positions,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=[pages[i]['url']+' English body' for i in positions],support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 assert len({code for c in registry['claims'] if c['source_id']==SOURCE for code in c['standard_codes']})==48
 p.write_text(json.dumps(bibliography,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'data/content_review_queue.json';q=json.loads(p.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE]);p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])]==old['claims'] and s['observations'][:36]==old['sources'][SOURCE]['observations']
 assert all(registry['sources'][k]==v for k,v in old['sources'].items() if k!=SOURCE) and load_reviews()==relations
 build_report();print('Added61 length-linked public bodies:58 activity descriptions,2 introductions,1 teacher resource;5 claims/4 probes;669 public bodies pending')

if __name__=='__main__':main()

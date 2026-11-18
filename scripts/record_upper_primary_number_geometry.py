"""Scope large-number, rounding, divisibility, circle and surface-area references."""
from decimal import Decimal
from math import gcd

from record_conic_representation_research import probe
from record_scoped_pdf_research import ROOT, record

DATE='2026-11-13'
CACHE=ROOT/'tmp/literature/upper-primary-gaps'
PV='NCETM_2018_LARGE_NUMBERS_130'
RA='NCETM_2022_ROUNDING_AUDIT'
ZC='ZAZKIS_CAMPBELL_ERIC_ED370932'
NS='NSW_STAGE4_CIRCLE_MEASUREMENT'
SA='NCETM_2019_SURFACE_AREA'
BIG,ORDER,ROUND,DIV,PI,CIRCLE,SURFACE='4수01-01','4수01-02','6수01-03','6수01-04','6수03-15','6수03-16','6수03-17'
SPECS={
 PV:dict(year=2018,authors=['National Centre for Excellence in the Teaching of Mathematics'],
  title='1.30 Composition and calculation: numbers up to 10,000,000, Teacher guide, Summer 2018 pilot',
  url='https://www.ncetm.org.uk/classroom-resources/primm-130-composition-and-calculation-numbers-up-to-10-000-000/',
  pdf_url='https://www.ncetm.org.uk/media/sbrc5pmz/ncetm_mm_sp1_y6_se30_teach.pdf',
  stem='ncetm-place-value-130',render_stem='ncetm-place-130',sha256='01a5f28f3a4b03ed977a862bb56746b6de694ea3f505711f37d8f91b6151de15',
  total=54,pages=[1,2,16,18,20,21,22],text_pages=[],visuals=[1,2,16,18,20,21,22],student_outcome_study=False,
  scope='표지와 개요, 자릿값 표·0을 포함한 카운터, 각 숫자의 값과 큰 자리부터 비교하는 지정 판면을 직접 읽었다. 기계적 글자 추출은 불완전하다.',
  limit='영국 Year 6 교사용 2018년 시범 자료다. 영어의 million·thousand 묶음을 한국어 만·억의 읽기와 동일시하지 않으며 한국 3~4학년의 교수 효과를 입증하지 않는다.',
  design='큰 수의 표기·구성·비교를 위한 교사 전문성 개발 자료.',sample='학생 표본 없음. 지정 PDF 판면의 과제 설계와 설명만 대조.',
  supports=['내부 0과 자릿값의 구별','수의 자리 수와 큰 자리부터의 비교']),
 RA:dict(year=2022,authors=['National Centre for Excellence in the Teaching of Mathematics'],
  title='Subject Knowledge Audit, Number, Question 7: Estimating and rounding',
  url='https://www.ncetm.org.uk/media/plwiuq5p/pska-num-q7.pdf',pdf_url='https://www.ncetm.org.uk/media/plwiuq5p/pska-num-q7.pdf',
  stem='ncetm-number-rounding',render_stem='ncetm-rounding',sha256='273fe96a95bab65cc219b7fd35259ada84f8a30c6434085a12c78a1520711d53',
  total=3,pages=[1,2,3],visuals=[1,2,3],student_outcome_study=False,
  scope='수직선의 앞뒤 배수와 452의 반올림, 두 수를 먼저 어림한 합의 세 응답, 교사용 예상 오류와 확인 질문을 대조했다.',
  limit='교사용 점검 문항이다. 예상 오류 목록은 실제 관찰한 학생의 빈도가 아니며 올림·버림의 자체 과제는 이 자료에서 실험한 결과가 아니다.',
  design='교사용 내용 지식 점검과 예시·해설.',sample='학생 표본 없음. 교사가 자신감을 표시하는 1~4 점검과 예시 응답을 포함.',
  supports=['반올림할 자리와 수직선의 구간','각 수를 먼저 어림한 합과 정확한 합의 반올림']),
 ZC:dict(year=1994,authors=['Rina Zazkis','Stephen Campbell'],
  title='Divisibility and Multiplicative Structure of Natural Numbers: Preservice Teachers’ Understanding, ERIC ED370932',
  url='https://eric.ed.gov/?id=ED370932',pdf_url='https://files.eric.ed.gov/fulltext/ED370932.pdf',
  stem='zazkis-campbell-eric-1994',render_stem='zc1994',sha256='41d9471cb755b24938a320338272b394498c79be4cd3bea7598a828a354a27e8',
  total=24,pages=[1,2,3,5,6,7,8],visuals=[1,2,8],student_outcome_study=True,
  scope='ERIC 서지와 제목 쪽의 연도 불일치, 예비 교사 21명의 표집·면담 문항 및 Nicole·Armin 사례의 지정 부분을 대조했다.',
  limit='예비 교사의 선별 면담 자료다. 국내 초등학생의 빈도로 해석하지 않는다. 소인수분해의 지수 표기를 초등 필수 과제로 추가하지 않는다. 서지 1994와 제목 1995 표기는 함께 보존한다.',
  design='수론 수업을 들은 자원자를 대상으로 한 유연한 개별 면담과 질적 분석.',sample='교사 전문성 과정의 예비 초등교사 자원자 21명.',
  supports=['나눗셈의 계산과 약수 관계의 설명','모든 약수의 열거와 공약수·최대공약수의 자체 확장']),
 NS:dict(year=None,authors=['NSW Department of Education'],title='Teaching Measurement Stage 4: selected circle lessons',
  url='https://education.nsw.gov.au/content/dam/main-education/teaching-and-learning/curriculum/key-learning-areas/mathematics/media/documents/mathematics-s4-teaching-measurement.pdf',
  pdf_url='https://education.nsw.gov.au/content/dam/main-education/teaching-and-learning/curriculum/key-learning-areas/mathematics/media/documents/mathematics-s4-teaching-measurement.pdf',
  stem='nsw-stage4-measurement',render_stem='nsw-stage4',sha256='7ddd5dda9dec1786909290c96222d0432010ca3c19ecbc9c2333995f5a83c850',
  total=109,pages=[1,2,3,17,18,40,41],visuals=[17,18,41],student_outcome_study=False,
  scope='표지·2012 교육과정 판권·목차와 원주 측정 및 부채꼴 조각 재배열의 지정 본문·그림을 대조했다.',
  limit='Stage 4 교사용 수업 설계다. 발행 연도는 본문에서 확정하지 않았고 교육과정 판권 2012를 발행 연도로 쓰지 않는다. 일반 부채꼴 공식·무리수 증명·극한의 엄밀한 증명은 자체 초등 과제에 추가하지 않는다.',
  design='길이·넓이·부피·시간의 교사용 수업 자료 중 원의 지정 부분.',sample='학생 표본 없음. 활동 지시와 기록표 및 도식.',
  supports=['원주와 지름의 측정과 오차','원주·반지름을 원의 넓이와 연결한 직관적 설명']),
 SA:dict(year=2019,authors=['National Centre for Excellence in the Teaching of Mathematics'],
  title='6.2 Perimeter, area and volume: Mastery Professional Development, Key Stage 3',
  url='https://www.ncetm.org.uk/media/1qabpyac/ncetm_ks3_cc_6_2.pdf',pdf_url='https://www.ncetm.org.uk/media/1qabpyac/ncetm_ks3_cc_6_2.pdf',
  stem='ncetm-surface-area-2019',render_stem='ncetm-sa',sha256='51a9789e14470d13442e04ed80031c995bd9b9346a624836b0b00e65c261ff05',
  total=33,pages=[1,2,8,29,32],visuals=[29,32],student_outcome_study=False,
  scope='교사 개발 자료의 목적, 겉넓이 정의, 면이 빠진 의도적 오류 예와 24개 연결 정육면체로 만든 직육면체 과제를 대조했다.',
  limit='영국 KS3 교사 개발 자료다. 원문의 삼각기둥·육각기둥 계산은 국내 초등 필수 범위로 옮기지 않는다. 의도적 오답 예와 문서의 정답을 구별한다.',
  design='교사 전문성 개발을 위한 개념 설명·예시·의도적 오류와 토의 질문.',sample='학생 표본 없음. 자체 과제는 직육면체와 정육면체의 여섯 면으로 한정.',
  supports=['보이지 않는 면까지 포함한 겉넓이','같은 개수의 정육면체와 서로 다른 겉넓이']),
}
CLAIMS=[
 (PV,'PV18-01',[BIG],[16,18,20],
  '가이드는 자리 표와 카운터로 큰 수를 표현하고, 비어 있는 자리에 0을 써야 한다는 점 및 각 숫자가 나타내는 값을 따로 묻는다.',
  '표시된 숫자와 그 자리의 값을 구별한다. 세 자리씩 묶는 영어 표현을 한국어 만·억 묶음의 검증 근거로 사용하지 않는다.'),
 (PV,'PV18-02',[BIG,ORDER],[20,21,22],
  '비교 과제는 자리 수가 다른 경우를 먼저 다룬 뒤, 큰 자리부터 처음 달라지는 자릿값을 찾아 같은 자리의 숫자를 비교하게 한다.',
  '가이드가 제안한 설계다. 첫 숫자만 보거나 오른쪽 끝부터 비교하지 않도록 이유를 듣되 이 순서가 보편적 필수 선수라고 확정하지 않는다.'),
 (RA,'RA22-01',[ROUND],[1,2,3],
  '452를 가장 가까운 10의 배수로 나타내는 과제에서 440이라는 응답을 제시하고, 수직선의 바로 앞뒤 배수와 그 사이 위치를 설명하게 한다.',
  '교사용 예시 응답이다. 실제 학생의 관찰 빈도로 세지 않으며 반올림할 자리에 따라 인접한 배수가 달라짐을 확인한다.'),
 (RA,'RA22-02',[ROUND],[1,2],
  '4243+1734의 예시 어림값 5900·5970·6000은 각 수를 각각 100·10·50의 배수로 먼저 반올림한 뒤 더하면 재현된다.',
  '정확한 합 5977 자체를 같은 단위로 반올림한 값과는 다를 수 있다. 예를 들어 합의 100 단위 반올림은 6000이다. 세 방법이 언제나 같은 정확도를 보인다는 결과가 아니다.'),
 (ZC,'ZC94-01',[DIV],[3,7,8],
  'Nicole은 구간 안의 7의 배수를 찾을 때 수마다 나눗셈을 해 보려 했고, 12362를 찾은 뒤에도 다른 배수가 있는지 계속 계산하려 했다.',
  '한 예비 교사의 면담 사례다. 나눗셈으로 확인한 답과 배수 간격·약수 관계로 설명한 답을 나누며 모든 초등학생의 방식으로 일반화하지 않는다.'),
 (ZC,'ZC94-02',[DIV],[5,6],
  '문항 묶음 4는 15 또는 45의 모든 양의 약수를 나열한 뒤 같은 약수 개수를 갖는 다른 수를 찾게 하는 방식으로 설계됐다.',
  '응답에 따라 두 가지 중 하나를 제시했다. 모든 학생이 두 문항을 받은 결과가 아니며 최대공약수의 자체 문제는 별도로 설계한 확장이다.'),
 (NS,'NSW-C1',[PI],[17,18],
  '활동은 원통 밑면의 원주와 지름을 재어 그 비를 기록하고, 값의 차이가 생기는 이유로 측정 오차를 토의하도록 제안한다.',
  '유한한 측정값을 모든 원에 대한 증명으로 세지 않는다. 같은 쪽 Step 5의 C=πr은 2가 빠져 있어 앞의 C=πd=2πr과 구별하고 옮기지 않는다.'),
 (NS,'NSW-C2',[PI,CIRCLE],[40,41],
  '원 조각을 번갈아 놓아 직사각형에 가까운 모양을 만들고, 높이를 반지름·가로를 원주의 절반과 연결해 원의 넓이 공식을 직관적으로 설명한다.',
  '유한 개 조각의 경계는 곡선이 남아 정확한 직사각형이 아니다. 더 잘게 나눈 모양을 이용한 직관과 엄밀한 극한 증명을 구별한다.'),
 (SA,'SA19-01',[SURFACE],[8,29],
  '자료는 겉넓이를 보이는 면만이 아닌 모든 면의 넓이 합으로 설명하고, 일부 면을 빼먹은 계산을 의도적 오류 예로 제시한다.',
  '삼각기둥의 예는 오류를 찾도록 만든 것이다. 누락된 면의 부분합을 정답으로 옮기지 않고 자체 과제는 직육면체·정육면체로 제한한다.'),
 (SA,'SA19-02',[SURFACE],[32],
  '예시 9는 연결 정육면체 24개로 만든 직육면체의 가능한 겉넓이를 묻고, 같은 부피에도 여러 겉넓이가 가능함을 토의하게 한다.',
  '교사 개발용 설계다. 부피와 겉넓이를 같은 수치나 같은 단위로 취급하지 않으며 학생 학습 효과를 입증한 결과로 해석하지 않는다.'),
]
OBSERVATIONS={
 PV:[
  probe('PV-P1',BIG,'2,005,040을 0이 아닌 각 자리의 값의 합으로 나타내고 5의 값과 0의 역할을 설명하라. 만을 단위로도 읽어 보라.',
   '2,000,000+5,000+40이고 5는 5000을 나타낸다. 0은 해당 자리에 묶음이 없음을 나타내면서 다른 자리의 위치를 보존한다. 200만 5040, 즉 이백만 오천사십이다.',
   '숫자 5 자체와 자릿값을 구별한다. 영어 자료의 세 자리 구분과 한국어의 만 단위를 그대로 동일시하지 않는다.'),
  probe('PV-P2',ORDER,'99,999와 100,000, 그리고 2,050,004와 2,005,400을 각각 비교하고 어느 자리에서 결정되는지 설명하라.',
   '99,999<100,000이다. 두 번째는 백만·십만 자리까지 같고 만 자리에서 5>0이므로 2,050,004>2,005,400이다. 오른쪽 끝 숫자의 크기로 판단하지 않는다.',
   '자리 수를 먼저 확인한 경우와 같은 자리 수에서 큰 자리부터 비교한 경우를 구별한다.'),
 ],
 RA:[
  probe('RA-P1',ROUND,'452를 반올림해 10의 자리까지와 100의 자리까지 각각 나타내라. 440이라는 답이 왜 맞지 않는지도 설명하라.',
   '각각 450과 500이다. 10의 배수에서는 450과 460 사이에 있고 450에 더 가깝다. 100의 배수에서는 400과 500 사이에서 500에 더 가깝다. 440은 바로 앞의 10의 배수도 아니다.',
   '반올림할 자리와 인접한 두 배수, 거리의 비교를 확인한다.'),
  probe('RA-P2',ROUND,'물건 123개를 10개씩 완전히 채운 묶음만 만들면 몇 묶음과 몇 개가 남는가? 모두 옮길 상자의 용량이 10개라면 최소 몇 상자가 필요한가?',
   '완성된 묶음은 12개이고 3개가 남는다. 모두 담는 상자는 최소 13개가 필요하다. 반올림한 120개만을 기준으로 상자 12개를 준비하면 3개를 담지 못한다.',
   '올림·버림의 목적을 수량과 남는 양으로 확인하는 자체 확장 과제다. 원자료에서 이 문항을 실험한 결과로 표시하지 않는다.'),
  probe('RA-P3',ROUND,'4243과 1734를 각각 반올림해 100의 자리까지 나타낸 뒤 더하라. 정확히 더한 값을 반올림한 결과와 같은가?',
   '4200+1700=5900이다. 정확한 합은 5977이고 이를 반올림해 100의 자리까지 나타내면 6000이다. 먼저 어림해 더하는 것과 더한 뒤 어림하는 것은 순서가 달라 결과도 다를 수 있다.',
   '어림값의 산출 순서를 기록하고 어림값을 정확한 합의 반올림으로 바꾸어 부르지 않는다.'),
 ],
 ZC:[
  probe('ZC-P1',DIV,'12와 18의 모든 양의 약수를 각각 쓰고 공약수와 최대공약수를 구하라. 3도 공약수인데 왜 최대공약수는 아닌가?',
   '12의 약수는 1,2,3,4,6,12이고 18의 약수는 1,2,3,6,9,18이다. 공약수는 1,2,3,6이며 최대공약수는 6이다. 3보다 큰 공약수 6이 있다.',
   '약수 목록의 빠진 수, 두 목록의 공통 원소, 가장 큰 공약수를 나누어 확인한다.'),
  probe('ZC-P2',DIV,'사과 48개와 배 36개를 남기지 않고 같은 구성의 봉지로 나눈다. 봉지를 최대한 많이 만들 때 봉지 수와 한 봉지의 구성을 설명하라.',
   '봉지 수는 48과 36의 공약수여야 하고 최대공약수는 12다. 12봉지에 사과 4개와 배 3개씩 넣는다. 6봉지도 가능하지만 최대는 아니며, 24봉지는 배를 같은 개수로 나눌 수 없다.',
   '자체 최대공약수 적용 과제다. 봉지 수와 한 봉지의 물건 수를 뒤바꾸지 않는지 확인한다.'),
 ],
 NS:[
  probe('NSW-P1',PI,'두 원 모양 물체의 측정 기록이 (지름 6.0cm, 원주 18.9cm), (지름 12.0cm, 원주 37.6cm)다. 원주/지름을 비교하고 이것만으로 원주율이 두 값이라고 할 수 있는지 설명하라.',
   '비는 각각 3.15와 약 3.1333이다. 측정과 반올림의 오차가 있을 수 있어 두 기록만으로 원주율이 두 값이라고 할 수 없다. 정확한 원의 원주와 지름 사이의 일정한 비와 측정 기록을 구별한다.',
   '주어진 두 값은 자체 만든 측정 예다. 원 연구에서 실제 측정한 학생 자료로 표시하지 않는다.'),
  probe('NSW-P2',CIRCLE,'반지름 3cm인 원의 원주와 넓이를 원주율 3.14를 사용해 구하라. 원을 여덟 조각으로 잘라 번갈아 놓은 모양은 정확한 직사각형인가?',
   '원주는 약 18.84cm, 넓이는 약 28.26cm²다. 여덟 조각을 재배열해도 넓이는 같지만 곡선 경계가 남아 정확한 직사각형은 아니다. 더 잘게 나누면 직사각형에 가까운 모양을 보며 공식을 직관적으로 이해할 수 있다.',
   '길이·넓이 단위, 반지름의 두 배와 제곱, 근삿값 및 유한 조각의 모양을 각각 확인한다.'),
 ],
 SA:[
  probe('SA-P1',SURFACE,'가로·세로·높이가 2cm,3cm,4cm인 닫힌 직육면체의 겉넓이를 구하라. 보이는 세 면만 더하면 되는가? 한 모서리가 3cm인 정육면체와도 비교하라.',
   '직육면체는 2(2·3+2·4+3·4)=52cm²다. 보이는 세 면의 합 26cm²만으로는 반대쪽 세 면이 빠진다. 정육면체는 넓이 9cm²인 면 여섯 개여서 54cm²다.',
   '모든 면의 개수와 각 면의 넓이, 합의 단위를 확인한다. 부피의 곱셈으로 겉넓이를 대신하지 않는다.'),
  probe('SA-P2',SURFACE,'같은 크기의 단위 정육면체 24개를 각각 2×3×4와 1×4×6인 직육면체로 쌓았다. 겉넓이도 같은가?',
   '겉넓이는 각각 2(6+8+12)=52, 2(4+6+24)=68 제곱단위로 다르다. 같은 개수의 단위 정육면체를 사용해도 바깥으로 드러나는 면은 달라질 수 있다.',
   '같은 부피와 같은 겉넓이를 구별하고 두 모양의 여섯 겉면만 계산한다.'),
 ],
}
DETAILS={
 PV:dict(pilot_year=2018,school_year_label='Year 6',pdf_pages=54,printed_pages=53,text_extraction_incomplete=True,
  reviewed_via_rendered_pages=True,english_thousands_and_korean_man_groups_not_equated=True),
 RA:dict(year=2022,student_sample_exists=False,confidence_scale_is_teacher_self_report=True,
  rounded_operands_sum_100=5900,exact_sum=5977,rounded_exact_sum_100=6000,predicted_errors_not_frequencies=True),
 ZC:dict(n=21,eric_year=1994,title_page_year=1995,publication_year_discrepancy_preserved=True,
  nicole_multiple=12362,nicole_quotient=1766,armin_transcript_quotient=625,correct_quotient=675,
  quote_not_correct_answer=True,selected_task_variant_depended_on_prior_response=True),
 NS:dict(publication_year=None,syllabus_copyright_year=2012,step_5_missing_factor=2,
  step_3_and_record_sheet_correct=True,finite_sector_rearrangement_is_approximate_rectangle=True,
  general_sector_formula_and_irrationality_proof_not_required=True),
 SA:dict(year=2019,student_sample_exists=False,deliberately_incorrect_example=True,
  elementary_tasks_restricted_to_cuboids_and_cubes=True,equal_volume_cube_count=24,
  own_surface_areas=[52,68],cube_side_3_surface=54),
}
CORRECTIONS={
 PV:'표지의 Summer 2018 pilot와 PDF 54쪽/인쇄 53쪽을 구별했다. 글자 추출이 대부분 비어 있어 지정 판면으로 읽었다. 0의 자리와 큰 자리부터 비교하는 설명을 한국어 자체 과제로 연결하되 영어 묶음 읽기를 그대로 옮기지 않는다.',
 RA:'5900·5970·6000은 각 수를 먼저 반올림한 합으로 재현된다. 정확한 합 5977 자체를 반올림한 값이라고 쓰지 않는다. 교사용 가상·예시 응답을 실제 학생의 통계로 세지 않는다.',
 ZC:'ERIC 서지 1994와 제목 쪽 AERA 1995 표기를 실제 판면에서 함께 확인했다. 8쪽 Armin 인용의 625는 정확한 4725÷7=675와 다르므로 정답으로 옮기지 않는다. 소인수분해 지수 과제를 국내 초등 필수 범위로 추가하지 않는다.',
 NS:'17쪽 Step 5의 C=πr은 같은 쪽 Step 3·18쪽의 C=2πr과 다르다. 누락된 2를 옮기지 않는다. 41쪽의 유한 조각 재배열은 정확한 직사각형으로 취급하지 않는다. 판권 2012는 교육과정의 연도이며 문서 발행 연도는 미확정이다.',
 SA:'29쪽은 빠진 면을 찾게 한 의도적 오류다. 부분합을 정답으로 옮기지 않는다. 원문 고학년용 삼각·육각기둥 예와 자체 초등 직육면체·정육면체 과제를 구별한다.',
}
INTERPRETATIONS={
 ('REV-4수01-02-1','PV18-02'):('activity_context','큰 수의 각 자리 값을 설명한 뒤 자리 수와 처음 달라지는 큰 자리를 근거로 두 수를 비교한다.',
  '교사 가이드의 과제 순서다. 한국어의 만·억 읽기와 영어의 묶음 표현을 구별하고 이 순서의 교수 효과나 보편적 필수 선수성을 확정하지 않는다.'),
 ('REV-6수03-16-1','NSW-C2'):('activity_context','원의 조각을 재배열한 모양에서 반지름과 원주의 절반을 각각 찾아 길이와 넓이를 연결해 설명한다.',
  '유한 조각은 정확한 직사각형이 아니다. 직관적 설명과 엄밀한 극한 증명을 구별하며 원주의 측정만으로 원의 넓이를 모두 이해했다고 판정하지 않는다.'),
}

if __name__=='__main__':
 assert 2_005_040==2_000_000+5_000+40 and 2_050_004>2_005_400
 assert 4243+1734==5977 and sum((n+50)//100*100 for n in [4243,1734])==5900
 assert (5977+50)//100*100==6000 and gcd(48,36)==12
 assert 12362==7*1766 and 4725//7==675
 assert Decimal('3.14')*6==Decimal('18.84') and Decimal('3.14')*9==Decimal('28.26')
 assert 2*(6+8+12)==52 and 2*(4+6+24)==68 and 6*3*3==54
 roles={cid:('empirical_result_with_scope' if cid=='ZC94-01' else 'mathematical_explanation') for _,cid,*_ in CLAIMS}
 record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,
  interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='초등 큰 수·어림·약수·원·겉넓이의 문헌 참고',
  detail_key='upper_primary_review',roles=roles)

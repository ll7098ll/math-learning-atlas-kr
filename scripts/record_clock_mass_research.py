"""Map clock-hand and mass-measurement research to the elementary task scope."""
from record_conic_representation_research import probe
from record_scoped_pdf_research import ROOT, record

DATE='2026-11-13'
CACHE=ROOT/'tmp/literature/time-and-mass'
EG='EARNEST_ET_AL_2018_CLOCK_HANDS'
CMC='CHEESEMAN_ET_AL_2011_MASS'
MC='MCDONOUGH_CHEESEMAN_2014_MASS_TASK'
TREAD,TUNIT,COMP,MG,MEXPR,MADD='2수03-07','2수03-08','2수03-06','4수03-20','4수03-21','4수03-23'
SPECS={
    EG:dict(year=2018,authors=['Darrell Earnest','Alicia C. Gonzales','Anna M. Plant'],
        title='Time as a Measure: Elementary Students Positioning the Hands of an Analog Clock',
        url='https://doi.org/10.5964/jnc.v4i1.94',
        pdf_url='https://jnc.psychopen.eu/index.php/jnc/article/download/5793/5793.pdf/',
        stem='earnest-et-al-2018',sha256='bfa74fe0a058b7fc49e391e92be88300aaf8fe216b0983ffc0dd737e85d57778',
        total=27,pages=[1,8,9,10,11,12,13,17],visuals=[11,13,17],
        scope='독립적으로 움직이는 두 바늘의 일곱 시각 과제, 학년별 평균과 672건의 바늘 반응 분류, 두 바늘의 관계를 설명한 사례를 대조했다.',
        limit='2·4학년 각 24명을 선택한 면담이다. 672는 48명×7문항×2바늘의 반응 수이며, 전략별 정답 비율은 전략 지도의 효과가 아니다.',
        design='여섯 학교의 사전 검사에서 선정한 학생의 개별 면담·영상·행동·설명 분석.',
        sample='미국 매사추세츠 여섯 초등학교의 2학년 24명과 4학년 24명. 전체 사전 검사 612명 중 본 논문 조건은 48명.',
        supports=['시침과 분침의 서로 다른 역할','한 시간과 분의 관계를 함께 설명하기','학생 수와 바늘별 반응 수의 구별']),
    CMC:dict(year=2011,authors=['Jill Cheeseman','Andrea McDonough','Doug Clarke'],
        title='Investigating Children’s Understanding of the Measurement of Mass',
        url='https://merga.net.au/publications/annual-conference-proceedings/2011-conference-proceedings/',
        pdf_url='https://www2.merga.net.au/documents/RP_CHEESMAN%26McDONOUGH%26CLARKE_MERGA34-AAMT.pdf',
        stem='cheeseman-mcdonough-clarke-2011',sha256='595e563fedd3de74e3975cfe48925b7fa598ab531263f78675de40e9523a192d',
        total=9,pages=[1,3,4,5,6,7],visuals=[4,5,6],
        scope='비교·비표준 단위·10g 추·1kg 기준·주방저울 면담 과제, Jack의 중단 사례와 시점별 표 1을 대조했다.',
        limit='성공에 따라 후속 문항을 진행하는 면담이다. 미제시와 실제 오답을 구별한다. 네 열의 분모 합 1806을 고유 학생 수나 개인별 성장 추적으로 확정하지 않는다.',
        design='초기 수학 면담의 무게 영역 과제와 학년·시점별 성장점 분포, 별도 학생 사례.',
        sample='2001년 Prep 3월 533명·11월 538명, 1학년 11월 479명, 2학년 11월 256명의 표 1 기록. Jack은 2학년 시작 때 면담한 한 사례.',
        supports=['비교와 단위로 양을 재는 수행의 구별','단위 개수와 g으로 나타낸 양','문항 중단과 시점별 분모']),
    MC:dict(year=2014,authors=['Andrea McDonough','Jill Cheeseman'],
        title='Young Learners’ Understandings About Mass Measurement: Insights from an Open-Ended Task',
        url='https://eric.ed.gov/?id=ED599902',pdf_url='https://files.eric.ed.gov/fulltext/ED599902.pdf',
        stem='mcdonough-cheeseman-open-mass',sha256='245986d154baa7f55bafbbd98d8015067ddaa9906bdb79fdb0a4cc0d6f824a12',
        total=8,pages=[1,2,3,4,5,6,7],visuals=[5,6],
        scope='다섯 수업 뒤 그리기·쓰기 과제의 방법, 무게의 같음과 정밀성 및 크기만으로 무게를 판단하지 않는 학생 설명을 대조했다.',
        limit='13학급 282명의 개방형 응답에서 제시한 사례다. 그림·문장을 면담 없이 단정하지 않으며, 다른 검사 논문의 295명과 독립 표본으로 합산하지 않는다.',
        design='연구자가 제공한 다섯 수업 후 A3 종이에 표현한 개방형 자기 설명의 질적 주제 분석.',
        sample='호주 빅토리아 도시·농촌 세 학교의 1·2학년 6~8세 282명, 13학급.',
        supports=['겉크기와 무게 판단','측정 도구와 정밀성에 관한 학생의 생각']),
}
CLAIMS=[
    (EG,'EG18-01',[TREAD,TUNIT],[8,9,11],
     '독립적으로 움직이는 두 바늘을 놓는 일곱 문항에서, 2학년 24명의 정답 수 평균은 시침 2.88·분침 5.04, 4학년 24명은 시침 4.54·분침 6.42였다.',
     '시침·분침별 일곱 문항 정답 수 평균이다. 두 학년 비교를 개인의 성장이나 수업의 인과 효과로 읽지 않는다.'),
    (EG,'EG18-02',[TREAD,TUNIT],[12,13],
     '표 2는 48명에게 일곱 시각의 두 바늘을 놓게 한 672건의 반응을 분류했다. 수량적으로 두 바늘을 연결한 분류는 101건이며 그 안의 정답 비율은 91.1%였다.',
     '101명이나 학생 전체의 91.1%가 아니다. 같은 학생의 여러 반응이 포함되고 관찰된 전략별 비율은 해당 전략을 가르친 효과가 아니다.'),
    (EG,'EG18-03',[TREAD],[17],
     '한 학생은 11시 반의 분침을 시계의 반 바퀴에, 시침을 11과 12 사이의 절반에 놓고 두 위치를 함께 설명했다.',
     '두 바늘을 수량적으로 연결한 101건 중 시침 반응 36건의 29건은 4시 반 또는 11시 반이었다. 이 사례를 다른 모든 시각의 숙달로 확장하지 않는다.'),
    (CMC,'CMC11-01',[COMP,MG],[3,4,5],
     'Jack은 두 용기를 손과 양팔저울로 비교했지만, 물체와 같은 무게가 되도록 비표준 단위를 사용하는 다음 과제에서는 단위를 계속 더했고 면담이 중단됐다.',
     '한 학생의 비교와 수량화 수행을 구별한다. 중단 뒤의 g·kg 문항을 실제 오답으로 기록하지 않는다.'),
    (CMC,'CMC11-02',[MG,MEXPR,MADD],[4,5],
     '면담 설계는 10g 추 네 개에 대응하는 무게를 40g으로 말하게 하고, 135g의 쌀에서 1kg이 되려면 얼마나 더 필요한지 묻는다.',
     '채점 지침과 과제 설계다. 추 네 개라는 타당한 단위 개수 설명과 지침이 요구한 40g 표현을 구별하며 실제 정답률로 해석하지 않는다.'),
    (CMC,'CMC11-03',[MG],[6,7],
     '표 1은 2001년 Prep 3월·11월과 1·2학년 11월을 각각 분모 533·538·479·256으로 제시한다. 2학년 열의 표준 단위 사용은 38%, 적용은 6%다.',
     '각 열의 분포 범주와 시점별 분모를 유지한다. 표준 단위 이상 44%와 표준 단위 범주 38%를 구별하고, 네 열을 같은 학생의 개별 추적 결과로 단정하지 않는다.'),
    (MC,'MC14-01',[COMP,MG],[3,4,6],
     '그리기·쓰기 사례에서 학생들은 작은 물체가 큰 물체보다 무거울 수 있으며 보기만으로 무거운지 정할 수 없다고 설명했다.',
     '다른 재료의 겉크기만으로 무게를 정할 수 없다는 사례다. 같은 재료와 조건에서도 부피와 무게가 언제나 무관하다고 가르치지 않는다.'),
    (MC,'MC14-02',[MG],[3,5,6],
     '학생들은 작은 비표준 단위를 섞어 균형을 맞추거나, 대략 같음과 g의 차이를 말하는 등 측정의 정밀성에 관해 서로 다른 설명을 했다.',
     '저울의 정확성에 관한 학생의 표현은 기기 교정 실험의 결론이 아니다. 원문은 이 주제 안에 위계를 가정하지 않으며 모든 학생이 같은 설명을 했다는 결과도 아니다.'),
]
OBSERVATIONS={
    EG:[
        probe('EG-P1',TREAD,'움직임이 서로 독립인 모형 시계에 2시 50분과 9시 3분을 각각 나타내고 두 바늘의 위치를 설명하라.',
              '2시 50분의 분침은 10, 시침은 2와 3 사이에서 3에 가깝다. 9시 3분의 분침은 12에서 작은 눈금 세 칸 지난 곳, 시침은 9를 조금 지난 곳이다. 분침을 숫자 3에 놓으면 15분을 가리킨다.',
              '두 바늘의 최초 위치와 설명을 따로 기록하고 모형이 실제 시계와 다른 배치를 허용함을 고려한다.'),
        probe('EG-P2',TUNIT,'2시간 15분은 215분인가? 전부 분으로 나타내고 135분을 다시 시간과 분으로 설명하라.',
              '1시간은 60분이므로 2시간 15분은 120+15=135분이다. 135분에서는 60분을 두 번 묶고 15분이 남아 2시간 15분이다.',
              '시각의 숫자를 이어 쓴 것과 시간의 양을 같은 단위로 바꾼 것을 구별한다.'),
        probe('EG-P3','4수03-14','같은 날 오전 8시 45분 40초에 시작해 9시 10분 15초에 끝난 활동은 몇 분 몇 초 걸렸는가? 9시를 경계로 설명하라.',
              '8시 45분 40초에서 9시까지 14분 20초, 9시부터 9시 10분 15초까지 10분 15초이므로 모두 24분 35초다. 1분은 60초이며 시작과 끝의 시각과 그 사이 시간의 길이는 다른 양이다.',
              '3~4학년의 초 단위 시간 덧셈·뺄셈에 맞춘 자체 확장 과제다. 이 논문에서 분석한 바늘 배치 문항의 결과를 시간 간격 문항의 정답률로 사용하지 않는다.'),
    ],
    CMC:[
        probe('CMC-P1',MG,'양팔저울의 한쪽 물체가 다른 쪽의 10g 추 네 개와 균형을 이뤘다. 무게를 말하고 20g 추로 바꾸면 몇 개가 필요한지 설명하라.',
              '10g이 네 개여서 물체는 40g이다. 20g 추는 두 개가 필요하다. 추의 개수는 바뀌어도 균형을 이루는 무게는 같다.',
              '단위의 크기·단위 개수·g으로 나타낸 양을 따로 듣는다. 네 개라는 답을 개념 부재로 단정하지 않는다.'),
        probe('CMC-P2',MEXPR,'쌀 135g이 있다. 1kg을 만들려면 몇 g을 더해야 하는가? 같은 양을 기준 단위로 설명하라.',
              '1kg=1000g이므로 1000−135=865g을 더한다. 135g과 865g을 합하면 1000g, 즉 1kg이다.',
              '주어진 무게로 계산한 답과 실제 저울로 135g을 재는 수행을 구별한다.'),
        probe('CMC-P3',MADD,'상자 자체의 무게를 빼고 잰 쌀이 1kg 250g, 추가할 쌀이 850g이다. 합친 무게를 kg과 g으로 나타내라.',
              '1250g+850g=2100g이고 2kg 100g이다. 1000g을 1kg으로 다시 묶는다.',
              '자체 복합 단위 과제다. 용기의 무게를 제외한 조건과 1000g의 재묶음을 확인한다.'),
    ],
    MC:[
        probe('MC-P1',COMP,'큰 스펀지와 작은 금속 조각이 있다. 보기만으로 어느 것이 더 무거운지 확정할 수 있는가? 확인 방법을 설명하라.',
              '겉크기만으로 확정할 수 없다. 손으로 어림한 뒤 양팔저울 양쪽에 하나씩 놓아 내려가는 쪽이 더 무거운지 확인한다. 균형이면 무게가 같다.',
              '실제 측정 전에 특정 물체가 반드시 더 무겁다고 답을 정하지 않는다. 크기와 무게를 나누어 설명하게 한다.'),
        probe('MC-P2',MG,'디지털저울에 한 번 40g이 나왔다. 이것만으로 이 저울이 다른 모든 저울보다 언제나 정확하다고 할 수 있는가?',
              '한 번의 표시만으로는 단정할 수 없다. 영점과 놓는 방법을 확인하고 다시 재거나 기준 추와 비교해야 한다. 표시 단위가 작다는 것과 실제 정확함은 구별한다.',
              '과제에서 얻은 학생의 의견과 저울의 실제 성능 검증을 분리한다.'),
    ],
}
DETAILS={
    EG:dict(n=48,grade_2_n=24,grade_4_n=24,screening_n=612,tasks=7,hands=2,response_instances=672,
        hour_means=[2.88,4.54],minute_means=[5.04,6.42],quantitative_instances=101,
        quantitative_percent_correct=91.1,quantitative_hour_instances=36,half_hour_subset=29,
        clock_hands_independent=True,strategy_rates_are_not_treatment_effects=True),
    CMC:dict(table_column_n=[533,538,479,256],table_column_n_sum=1806,
        unique_child_total_not_established=True,individual_longitudinal_changes_not_established=True,
        grade_2_standard_category_percent=38,grade_2_applying_percent=6,grade_2_standard_or_above_percent=44,
        jack_interview_stopped_after_informal_unit_task=True,unadministered_not_incorrect=True,
        ten_gram_weight_count=4,standard_grams=40,rice_grams=135,needed_for_one_kg_grams=865),
    MC:dict(n=282,classes=13,schools=3,ages=[6,8],lessons_before_task=5,
        responses_per_child_may_have_multiple_elements=True,photo_test_295_sample_independence_not_established=True,
        paragraph_figure_1_grams=50,visible_figure_1_grams=20,numeric_discrepancy_not_used_as_result=True,
        theme_hierarchy_not_claimed=True,student_instrument_opinions_not_calibration_results=True),
}
CORRECTIONS={
    EG:'표 1은 일곱 과제의 바늘별 정답 수 평균이다. 표 2의 672건은 학생 수가 아니며 전략별 비율에 학생당 독립 표본을 가정하지 않는다. 독립 바늘 도구는 실제 시계에 불가능한 배치도 허용한다.',
    CMC:'표의 네 분모를 합한 1806과 고유 학생 수를 구별한다. 38%의 표준 단위 범주와 적용 6%를 합친 44%를 구별한다. 지침이 요구하는 40g 표기와 추 네 개라는 수량 설명을 별도로 관찰한다.',
    MC:'4쪽의 그림 1 소개는 50g이라고 하지만 5쪽 실제 학생 그림은 20으로 보인다. 이 수치를 근거 주장과 자체 정답으로 사용하지 않는다. 원문의 부피와 무게가 무관하다는 서술은 다른 재료의 겉크기만으로 판단하지 않는 범위로 제한한다. 295건 검사 논문과의 표본 중복은 미확인이다.',
}
INTERPRETATIONS={
    ('REV-2수03-08-1','EG18-01'):('activity_context',
        '같은 시각을 두 바늘로 나타내고, 분침이 움직인 분만큼 시침도 한 시간 구간에서 이동했음을 설명한다.',
        '시침·분침의 일곱 과제 평균을 따로 유지한다. 시각 읽기만으로 모든 시간 단위 변환이 보장된다는 결과가 아니다.'),
    ('REV-2수03-08-1','EG18-02'):('inference_limit',
        '한 시간과 분을 연결한 설명인지, 시계 숫자를 대응시킨 설명인지를 바늘별로 기록한다.',
        '672건은 반복된 바늘 반응이다. 전략별 정답 비율을 학생 전체의 성취 비율이나 전략 지도의 효과로 올리지 않는다.'),
    ('REV-4수03-20-1','CMC11-01'):('activity_context',
        '물체의 무게를 직접 비교한 뒤 같은 비표준 단위로 균형을 맞추게 해 두 수행을 나누어 듣는다.',
        'Jack 한 사례다. 비교 성공을 단위 사용의 충분조건으로 보지 않으며 면담 중단 뒤 과제를 실제 오답으로 기록하지 않는다.'),
    ('REV-4수03-21-1','CMC11-02'):('activity_context',
        '10g 추의 개수와 g으로 나타낸 무게를 둘 다 말하고, 1000g을 1kg이라는 다른 단위로 표현한다.',
        '원문의 채점 지침과 실제 수학적 설명의 범위를 구별한다. 이 문항 설계 자체는 단위 변환의 학습 효과 자료가 아니다.'),
    ('REV-4수03-23-1','CMC11-02'):('activity_context',
        '135g에 더해 1kg을 만드는 과제에서 먼저 단위를 g으로 통일하고 덧셈과 뺄셈으로 서로 검산한다.',
        '주어진 수의 계산과 저울에서 양을 맞추는 수행을 구별한다. 자체 복합 단위 덧셈의 검증 자료로 확장하지 않는다.'),
    ('REV-4수03-20-1','MC14-01'):('activity_context',
        '서로 다른 재료의 크기와 무게를 예상한 이유를 듣고 실제 비교와 단위를 사용한 측정을 이어 실시한다.',
        '개방형 과제의 일부 사례다. 겉크기만으로 판단할 수 없다는 설명을 같은 재료의 부피와 무게도 무관하다는 주장으로 바꾸지 않는다.'),
}

if __name__=='__main__':
    assert 48*7*2==672 and 533+538+479+256==1806
    assert 38+6==44 and 1000-135==865 and 1250+850==2100
    assert 2*60+15==135 and (9*3600+10*60+15)-(8*3600+45*60+40)==24*60+35
    record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,
           interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='초등 시계·시간 단위와 무게 측정 연구',
           detail_key='clock_mass_review',roles={'CMC11-02':'mathematical_explanation'})

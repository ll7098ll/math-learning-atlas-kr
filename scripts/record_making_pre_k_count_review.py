"""Register three MDRC reports from the same Making Pre-K Count evaluation."""
from extend_lt2_length_assets_review import load, write
from literature_review import ROOT, build_report, load_registry
from record_direct_learning_trajectory_trials import register, verify_pdf


CACHE = ROOT / 'tmp/literature/making-prek-count'
FAMILY = 'MDRC_MAKING_PRE_K_COUNT_HIGH_5S'
MDRC = 'https://www.mdrc.org/work/publications/'
PRE = MDRC + 'making-pre-k-count'
KINDERGARTEN = MDRC + 'strengthening-childrens-math-skills-enhanced-instruction'
THIRD = MDRC + 'long-term-effects-enhanced-early-childhood-math-instruction'

PRE_K = dict(
    id='MORRIS_ET_AL_2016_MAKING_PRE_K_COUNT', year=2016, file='mdrc-2016-pre-k',
    title='Making Pre-K Count: Improving Math Instruction in New York City',
    authors=['Pamela A. Morris', 'Shira K. Mattera', 'Michelle F. Maier'],
    canonical_url=PRE, publisher=PRE, url=PRE + '/file-full',
    sha256='aebe0b9640288a6cd4cac239c3a6ee49057b5332780fbd97e78c56943e4c76b3',
    pdf_pages=118, printed_pages=[38, 44], text_pages=[5, 62, 67, 68], visual_pages=[62, 68],
    scope='연구기관 보고서의 개요와 표 4.1·4.4, 검사 설명, 분모와 주석을 지정 PDF 4쪽에서 읽고 판면 2쪽을 대조했다.',
    kind='MPC 동일 평가의 취학 전 추적 보고서', study_family=FAMILY,
    design='뉴욕시 69개 취학 전 기관을 프로그램과 정규 수업에 블록 안에서 무작위 배정한 비교.',
    sample='프로그램 35개 기관과 정규 수업 34개 기관. 표 4.1은 87·86학급, 표 4.4는 698·691명.',
    limit='이 보고서의 관찰 시간과 종합 점수를 국내 특정 세기·연산·도형·규칙 과제의 효과나 지도 순서로 해석할 수 없다. 유치원·3학년 보고서는 같은 평가의 후속 자료다.',
    next_review='교실 관찰의 영역별 분류, 표 4.7 하위집단과 후속 논문의 모형을 대조한다.',
    supports=['취학 전 기관 배정', '교실 활동 시간과 아동 검사 결과의 구별'],
    checks={62: ['46.80 34.85 11.95', '87 86'], 68: ['26.94 26.63 0.31', '698 691']},
    results=dict(sites=[35, 34], classrooms=[87, 86], tested_children=[698, 691],
                 teacher_led_and_informal_minutes=[46.80, 34.85], minutes_difference=11.95,
                 child_assessment_effect_sizes={'ECLS-B': .05, 'WJ-III': .06}),
    corrections=[('PDF 62쪽 표 4.1 주석 e', '평균 활동 질은 교사 주도 활동이 관찰된 학급만의 값이며 조건별 포함 비율이 달라 같은 해석을 적용하지 않는다.')],
    claims=[
        ('MPC16-01', ['2수01-01'], [5, 62, 68],
         '69개 기관을 35개 MPC와 34개 정규 수업에 배정했다. 세 시간 관찰에서 교사 주도 및 비형식 수학 활동 시간 차이는 11.95분이었다. 학급 관찰 87·86개와 아동 검사 698·691명을 구별한다.',
         '활동 시간이 늘었다는 결과를 아동의 세기 능력 향상으로 해석하지 않는다. 교사 주도 활동이 실제 관찰된 학급만 비교한 질 점수는 포함 비율도 달랐다.'),
        ('MPC16-02', ['2수01-01', '2수01-05'], [67, 68],
         '취학 전 말 ECLS-B 수학과 WJ-III 응용문제의 효과크기는 각각 .05와 .06으로 보고됐고 유의하지 않았다. ECLS-B는 수 감각, 연산, 측정, 도형, 공간과 규칙을 함께 다룬 검사다.',
         '종합 검사에서 차이가 뚜렷하지 않았다는 결과로 개별 수학 활동의 동등성이나 덧셈·뺄셈 상황 이해의 효과를 판정할 수 없다.'),
    ],
)

KINDER = dict(
    id='MATTERA_ET_AL_2018_MPC_KINDERGARTEN', year=2018, file='mdrc-2018-kindergarten',
    title='Strengthening Children’s Math Skills with Enhanced Instruction: The Impacts of Making Pre-K Count and High 5s on Kindergarten Outcomes',
    authors=['Shira K. Mattera', 'Robin Jacob', 'Pamela A. Morris'],
    canonical_url=KINDERGARTEN, publisher=KINDERGARTEN, url=KINDERGARTEN + '/file-full',
    sha256='50c594c85f62a2806a85ffb533f083b7cc9e36211c7db666b5197092ad9d8794',
    pdf_pages=142, printed_pages=['ES-6', 19, 22, 26, 29, 77, 78],
    text_pages=[5, 20, 45, 48, 52, 55, 103, 104], visual_pages=[45, 48, 52, 55, 104],
    scope='개요, 검사 설명, 주 결과 세 표, 원점수 민감도와 부록 F의 하위 영역을 지정 PDF 8쪽에서 읽고 판면 5쪽을 확인했다.',
    kind='MPC 동일 평가의 유치원 추적 보고서', study_family=FAMILY,
    design='취학 전 기관 배정과 MPC 공립학교에 남은 유치원 아동의 High 5s 개별 배정을 사용한 세 비교.',
    sample='표 3.1은 641·684명, 표 3.2는 303·310명, 표 3.3은 303·345명.',
    limit='REMA-K T점수, 원점수, 하위 영역과 WJ-III는 같은 결과가 아니다. 유치원 보고서를 취학 전·3학년 보고서와 독립 반복 실험으로 합산할 수 없다.',
    next_review='부록 D·E 전체와 High 5s 동반 보고서, 검사 문항과 시행·중단 규칙을 대조한다.',
    supports=['세 비교와 검사별 효과크기', 'REMA-K 민감도와 하위 영역의 한계'],
    checks={45: ['38.35 37.61 0.73 0.11 0.08'], 48: ['0.12', '0.47'],
            52: ['39.47 37.90 1.57 0.01', '303 310'], 55: ['39.12 36.50 2.63 0.00', '303 345'],
            104: ['Patterning 1.53 1.43', 'Measurement 0.40 0.34']},
    results=dict(compared_children=[[641, 684], [303, 310], [303, 345]],
                 rema_k_T_effect_sizes=[.08, .19, .30], rema_k_T_printed_p=['.11', '.01', '.00'],
                 WJ_effect_sizes=[.00, .09, .09], WJ_p=[.96, .18, .40],
                 rema_k_raw_effect_sizes=[.12, .22, .43], rema_k_raw_minus_five_effect_sizes=[.12, .23, .47]),
    corrections=[('PDF 55·104쪽', 'p=.00은 보고서의 인쇄 정밀도다. 정확한 영으로 취급하지 않는다.'),
                 ('PDF 103·104쪽', '검사의 문항 제시 규칙으로 도형 문항에 도달한 여부와 도형 점수가 얽혀 있다.')],
    claims=[
        ('MPC18-01', ['2수01-01'], [45, 48],
         '유치원 말 MPC 대 정규 취학 전 비교는 641·684명이다. 주 분석의 REMA-K T점수 효과크기는 .08(p=.11), WJ 응용문제는 .00(p=.96)이었다.',
         'REMA-K 원점수 분석과 점수 척도를 구별한다. 효과크기 .00의 인쇄 표기나 비유의 결과로 두 조건의 동등성을 판단하지 않는다.'),
        ('MPC18-02', ['2수01-01', '2수01-05'], [20, 52, 55],
         'High 5s 추가 대 MPC는 303·310명으로 REMA-K .19(p=.01), WJ .09(p=.18)이었다. 두 해 결합 대 정규 수업은 303·345명으로 REMA-K .30(표에 p=.00, 1% 유의 표시), WJ .09(p=.40)이었다.',
         '두 비교의 대조군이 다르다. 두 검사의 결과를 하나의 효과로 묶거나 전체 점수로 국내 상황제의 덧셈·뺄셈 이해를 판정하지 않는다.'),
        ('MPC18-03', ['2수01-01'], [20, 45, 48],
         '연구진은 REMA-K 48문항 중 프로그램 활동과 유사하다고 분류한 5문항을 뺐다. 세 비교의 원점수 효과크기 .12·.22·.43은 제거 후 .12·.23·.47이었다. MPC 단독 원점수의 p=.04와 주 분석 T점수의 p=.11을 구별한다.',
         '특정 5문항을 제거한 민감도 분석이다. 검사 전체와 프로그램의 독립성이나 국내 번역 문항의 동등성을 보장하지 않는다.'),
        ('MPC18-04', ['2수01-01', '2수02-01', '2수03-10'], [103, 104],
         'MPC 단독의 부록 F 원점수 하위 영역에서 수 영역은 .09(p=.10), 규칙은 .13(p=.03), 측정은 .08(p=.28)로 보고됐다. 표는 10% 유의 표시도 사용한다.',
         '서로 다른 문항과 제시 조건의 하위 영역이다. 한 결과가 유의하고 다른 결과가 비유의라는 사실만으로 영역별 효과 차이가 검정됐다고 볼 수 없다.'),
        ('MPC18-05', ['2수03-03'], [103, 104],
         '부록 F의 도형 원점수 효과크기는 .19이며 표는 p=.00으로 인쇄했다. 보고서는 도형 문항에 도달할 만큼 검사에 응답한 여부가 결과의 일부를 설명할 수 있다고 적었다.',
         '도형 문항 도달과 도형 수행의 효과를 분리할 수 없다. 원·삼각형·사각형에 대한 각각의 효과로 해석하지 않는다.'),
    ],
)

GRADE_3 = dict(
    id='MATTERA_ET_AL_2021_MPC_THIRD_GRADE', year=2021, file='mdrc-2021-third-grade',
    title='Long-Term Effects of Enhanced Early Childhood Math Instruction: The Impacts of Making Pre-K Count and High 5s on Third-Grade Outcomes',
    authors=['Shira K. Mattera', 'Robin Jacob', 'Cullen MacDowell', 'Pamela A. Morris'],
    canonical_url=THIRD, publisher=THIRD, url='https://www.mdrc.org/sites/default/files/MPC_High5-3yr_Impact_Report.pdf',
    sha256='ea7abc1ea2297859160b470098b262b3dbc10d2c732d276b7a9acbb0defc9fb8',
    pdf_pages=101, printed_pages=[6, 7, 9, 14, 23, 24, 25],
    text_pages=[5, 24, 25, 27, 32, 38, 41, 42, 43], visual_pages=[24, 25, 32, 41, 42],
    scope='기관·아동 배정도, 분석 표본, 탈락 설명, 3학년 수학 결과와 상충하는 표 주석을 지정 PDF 9쪽과 판면 5쪽에서 대조했다.',
    kind='MPC 동일 평가의 초등 3학년 추적 보고서', study_family=FAMILY,
    design='취학 전 기관 무작위 배정과 공립학교 잔류 아동의 유치원 개별 배정을 사용한 추적. 결과는 3학년 행정 자료.',
    causal_effect_established=False,
    sample='수학 점수가 있는 표본은 MPC 대 정규 945·899명, High 5s 추가 226·230명, 두 해 결합 대 정규 226·255명.',
    limit='세 비교는 동일 분모가 아니며 추가와 결합 비교의 중재군은 겹친다. 학교에 남은 아동의 선택과 결과 미확보를 고려하며 국내 특정 초등 과제의 장기 효과로 해석하지 않는다.',
    next_review='부록 B·F의 분석 사양과 후속 권호 논문의 p=.18을 표 3.1의 p=.19와 대조한다.',
    supports=['기관·아동 배정 단위', '비교별 분석 및 수학 검사 분모', '표 주석 내부 불일치'],
    checks={25: ['1,165 1,112 274 282 274 313'], 32: ['0.10 0.19 0.08 0.10', '945 899'],
            41: ['0.02 0.82 0.08 0.02', '226 230'], 42: ['0.34 0.01', '226 255']},
    results=dict(any_outcome=[[1165, 1112], [274, 282], [274, 313]], math_outcome=[[945, 899], [226, 230], [226, 255]],
                 math_effect_sizes=[.10, .02, .34], math_p=[.19, .82, .01], MPC_math_eligible=2702,
                 MPC_math_observed=1844, reported_overall_attrition_pct={'MPC': 32, 'High 5s': 30}),
    corrections=[('PDF 41쪽 표 3.5', '대조군을 MPC 이후 정규 유치원이라고 설명한 첫 주석과 바로 뒤의 MPC 미수혜 추정 문장이 서로 다르다. 그림 2.1·표 2.1·본문·요약의 일치에 따라 이 표를 High 5s 추가 비교로 분류한다.')],
    claims=[
        ('MPC21-01', ['2수01-01'], [24, 25, 27],
         '취학 전에는 기관을 배정했고 High 5s는 MPC를 실시한 공립학교에 남은 아동을 개별 배정했다. 3학년 결과가 하나라도 있는 세 비교의 분모는 1,165·1,112명, 274·282명, 274·313명이다.',
         '뒤의 두 비교 중재군 274명은 같은 아동이다. 분석 분모와 수학 점수가 실제 확보된 분모를 구별한다.'),
        ('MPC21-02', ['2수01-01'], [27, 32],
         'MPC 대 정규 수업의 3학년 주 수학 검사는 점수가 있는 945·899명을 비교해 효과크기 .10(p=.19)을 보고했다. 보고서는 적격 2,702명 중 1,844명의 수학 점수로 약 32% 탈락을 기록했다.',
         '3학년 주 시험은 취학 전 ECLS-B나 유치원 REMA-K와 다르다. 장기 효과가 정확히 영이거나 개별 세기 과제의 효과가 유지됐다고 판정하지 않는다.'),
        ('MPC21-03', ['2수01-01'], [24, 25, 38, 41],
         'High 5s 추가 대 MPC의 3학년 수학은 226·230명에서 .02(p=.82)였다. 표 3.5 첫 주석과 이어지는 추정 설명의 대조군 문구가 상충한다. 설계 그림과 표 2.1은 양쪽 모두 MPC를 받은 비교임을 보여 준다.',
         '결합 대 정규 수업의 결과와 혼합하지 않는다. 상충하는 주석을 출판사 정정으로 처리하지 않는다.'),
        ('MPC21-04', ['2수01-01'], [25, 42, 43],
         '두 해 결합 대 정규 수업의 3학년 수학은 같은 공립학교에 남은 아동 중 점수가 확보된 226·255명에서 .34(p=.01)였다.',
         '세 비교의 대조군과 분석 대상이 달라 .34를 .10과 .02의 합과 비교해 상승 작용을 추정할 수 없다. 종합 점수에서 국내 특정 수행의 장기 효과를 분리할 수 없다.'),
    ],
)


def main():
    registry = load_registry()
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography, queue = load(bibliography_path), load(queue_path)
    pending = []
    for spec in (PRE_K, KINDER, GRADE_3):
        if spec['id'] in registry['sources']:
            recorded = {c['id'] for c in registry['claims'] if c['source_id'] == spec['id']}
            assert {row[0] for row in spec['claims']} <= recorded
        else:
            pending.append((spec, verify_pdf(spec, CACHE)))
    if pending:
        assert sum(GRADE_3['results']['math_outcome'][0]) == GRADE_3['results']['MPC_math_observed']
        for spec, images in pending:
            register(spec, images, bibliography, queue, registry)
        write(bibliography_path, bibliography)
        write(queue_path, queue)
        write(ROOT / 'data/literature_claim_reviews.json', registry)
    build_report()


if __name__ == '__main__':
    main()

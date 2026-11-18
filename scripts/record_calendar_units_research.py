"""Bind calendar assessment text and SI unit definitions to scoped elementary tasks."""
import calendar

from record_conic_representation_research import probe
from record_scoped_pdf_research import ROOT, record

DATE='2026-11-13'
CACHE=ROOT/'tmp/literature/time-and-mass'
TK='LABRELL_ET_AL_2020_TIME_KNOWLEDGE'
SI='BIPM_2026_SI_9_V401'
READ,HOUR,CAL,SEC,TADD,CAP,CADD,KG,TON='2수03-07','2수03-08','2수03-09','4수03-13','4수03-14','4수03-18','4수03-19','4수03-21','4수03-22'
SPECS={
    TK:dict(year=2020,authors=['Florence Labrell','H. Câmara Costa','H. Perdry','G. Dellatolas'],
        title='The Time Knowledge Questionnaire for children',url='https://doi.org/10.1016/j.heliyon.2020.e03331',
        doi='10.1016/j.heliyon.2020.e03331',asset_kind='repository_xml',repository='Europe PMC',article_identifier='PMC7011039',
        xml_url='https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7011039/fullTextXML',
        stem='time-knowledge-2020',sha256='68d9e2bac886283544a0d710422ff92460875ddcd89818f8a76b721b84750ee5',
        section_ids=['sec4','sec5.1.1','sec5.2','sec5.3','appsec1','fig1'],
        scope='공식 저장소 XML의 검사 구성, 학교 표본과 면담 절차, 관습적 시간의 채점 및 부록 A의 달력·시각 문항을 읽었다. 그림 1은 설명 문장만 대조했다.',
        limit='프랑스 한 도시권 학교 표본 105명에 관한 검사 설계다. 임상 표본과 규준의 국내 적용은 다루지 않는다. XML 읽기를 PDF 판면이나 시계 그림 자체의 시각 대조로 표시하지 않는다.',
        design='시간 지식의 여러 하위 검사를 구별한 개별 면담형 평가. 여기서는 문항 구성·채점·표본 범위만 대조.',
        sample='프랑스 파리 인근 도시권 1~5학년 105명, 만 6.2~11.1세. 별도 임상 표본은 이 대조에서 제외.',
        supports=['기간 비교와 날짜·시각 읽기의 구별','거친 시간대 채점과 분 단위 시각 읽기의 구별']),
    SI:dict(year=2026,authors=['Bureau International des Poids et Mesures'],
        title='The International System of Units (SI), 9th edition, V4.01, June 2026',
        url='https://doi.org/10.59161/AUEZ1291',
        pdf_url='https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf',
        stem='bipm-si-9-en-20261113',render_stem='bipm-si-2026',
        sha256='5442eea2c680caf77a9d96879205a97f57c7c270b98a0bd0126c18fefe47e02c',
        total=102,pages=[1,28,29,30,31],visuals=[1,28,29,30,31],student_outcome_study=False,
        scope='V4.01의 표지, 접두어 표 7, 질량의 접두어 사용, 비SI 단위의 표 8과 L·t 주석을 실제 판면으로 대조했다.',
        limit='단위 정의와 환산의 참고 문서다. 학생의 난점 빈도나 교수 효과를 연구한 자료가 아니다. 표 8의 하루는 24시간의 단위이며 달을 고정된 일수로 정의하지 않는다.',
        design='국제도량형국의 단위 정의·표기·환산 설명 문서.',sample='학생 표본 없음. 2026년 6월 개정 V4.01의 지정 부분.',
        supports=['kg·g와 t·kg의 서로 다른 1000배 관계','L·mL의 관계','시간 단위의 60과 24 관계']),
}
CLAIMS=[
    (TK,'TK20-01',[CAL],['sec4','appsec1'],
     '부록 A의 시간 단위 문항은 분과 초, 주와 월, 월과 년의 길이를 비교하고 어느 날 아침부터 다음 날 아침까지 몇 시간인지 묻는다.',
     '문항 설계의 참고다. 단위의 크기를 비교한 답과 달력에서 실제 날짜 수를 센 답을 구별하며 한 달을 언제나 30일로 환산하지 않는다.'),
    (TK,'TK20-02',[READ,CAL],['sec5.1.1','sec5.3','appsec1','fig1'],
     '방향 파악 하위 검사의 현재 시각 문항은 같은 반나절 안의 답을 맞다고 처리하지만, 별도의 시계 읽기 하위 검사는 바늘의 구체적 시각을 묻는다.',
     '해당 검사의 채점 목적이 서로 다르다. 같은 반나절 응답을 분 단위 읽기의 정답으로 옮기지 않고, 학교 표본 105명의 규준을 국내 성취 기준으로 사용하지 않는다.'),
    (SI,'SI26-01',[KG,TON],[28,29,30],
     '표 8은 1t=1000kg을 제시하며, 접두어 표와 질량 표기 규칙에서는 kg와 g의 1000배 관계를 구별할 수 있다.',
     '같은 무게의 단위를 바꿀 때 수치와 단위가 함께 바뀐다. 1t를 1000g으로 쓰지 않으며 이 환산 정의를 학생의 실제 수행 근거로 세지 않는다.'),
    (SI,'SI26-02',[CAP,CADD],[28,30,31],
     '표 8의 리터 L와 표 7의 milli를 함께 읽으면 1L=1000mL이다. 대문자 L는 숫자 1과 소문자 l의 혼동을 줄이기 위해 허용됐다.',
     '들이의 양을 같은 단위로 바꾼 뒤 더하고 뺀다. 1000mL와 1L는 같은 양이며 L를 질량 단위 kg으로 바로 바꾸지 않는다.'),
    (SI,'SI26-03',[HOUR,CAL,SEC,TADD],[30],
     '표 8의 시간 단위는 1분=60초, 1시간=60분, 1일=24시간이다. 시간의 분·초와 각도의 분·초는 같은 표 안에서도 서로 다른 양으로 구별돼 있다.',
     '시간 계산에서 60을 기준으로 묶는다. L·mL나 kg·g의 1000배 관계를 분·초에 적용하지 않으며, 고정된 일 단위에서 달의 일수를 추정하지 않는다.'),
]
OBSERVATIONS={
    TK:[
        probe('TK-P1',CAL,'한 주는 7일이다. 2026년 2월은 28일, 3월은 31일인 달력을 보고 각 달이 몇 주 며칠인지 설명하라. 한 달을 언제나 30일이라고 할 수 있는가?',
              '2월은 4주, 3월은 4주 3일이다. 달력의 날짜 수가 다르므로 한 달을 언제나 30일이라고 할 수 없다. 1년의 달 수 12와 각 달의 날짜 수를 구별한다.',
              '원문의 기간 비교를 참고한 자체 달력 과제다. 단위 이름을 말한 답과 실제 날짜를 세고 묶은 답을 나누어 기록한다.'),
        probe('TK-P2',READ,'오전 수업 중이다. 모형 시계의 시침은 10을 조금 지났고 분침은 2를 가리킨다. 오전·오후 중 어느 시간대인지와 몇 시 몇 분인지를 각각 말하라.',
              '오전이라는 것은 주어진 수업 맥락에서 알 수 있다. 바늘은 10시 10분을 나타낸다. 시계판과 바늘만으로는 오전인지 오후인지 정할 수 없다.',
              '맥락에서 시간대를 정한 답과 바늘을 분 단위로 읽은 답을 구별한다. 원논문의 거친 시간대 채점을 분 단위 정답으로 대신하지 않는다.'),
    ],
    SI:[
        probe('SI-P1',TON,'2t 300kg은 몇 kg인가? 단위를 kg으로 바꾸면 물체의 무게 자체가 커지는지 설명하라.',
              '2t는 2000kg이므로 모두 2300kg이다. 나타내는 수치는 커져도 무게의 양은 같다. 1t=1000kg이며 1000g과는 다르다.',
              '단위 크기와 수치의 변화를 무게 자체의 변화와 구별한다.'),
        probe('SI-P2',CADD,'들이 2L인 용기에 물 1L 750mL가 있다. 물 650mL를 더 부을 때 모두 담을 수 있는가? 넘친 것 외의 손실은 없다고 하고 합친 양과 넘치는 양을 구하라.',
              '1750mL+650mL=2400mL로 2L 400mL다. 용기에는 모두 담을 수 없고 400mL가 넘친다.',
              '합친 물의 양, 용기에 담기는 양과 용기의 최대 들이를 구별한다. 1000mL를 1L로 다시 묶는 과정을 듣는다.'),
        probe('SI-P3',SEC,'2분 5초는 205초인가? 초로 바꾸고 그 과정을 1분과 1초의 관계로 설명하라.',
              '1분은 60초이므로 2분 5초는 120+5=125초다. 시간 표기의 숫자를 이어 쓴 205와 다르다.',
              '60초 묶음 두 개와 남은 5초를 설명하게 한다. 십진 단위의 1000배 관계와 구별한다.'),
        probe('SI-P4',TADD,'2분 50초 걸린 활동과 1분 25초 걸린 활동을 쉼 없이 이어 했다. 총 시간을 분과 초로 나타내라.',
              '3분 75초이고 75초 중 60초를 1분으로 묶어 4분 15초다. 초로 바꾸어 170+85=255초로도 확인할 수 있다.',
              '문맥의 이어진 시간과 60초의 재묶음을 확인한다. 3분 75초는 계산 중 표현이며 정리된 분·초 표기와 구별한다.'),
    ],
}
DETAILS={
    TK:dict(school_n=105,ages_years=[6.2,11.1],clinical_sample_excluded=True,domestic_norms_not_inferred=True,
        selected_scope_is_design_and_scoring=True,or_time_accepts_same_half_day=True,
        or_and_clock_scores_not_interchangeable=True,figure_caption_item_4_hour=11,appendix_item_4_hour=1,
        figure_visual_review=False,whole_pdf_obtained=False,calendar_month_fixed_days_not_assumed=True),
    SI:dict(edition=9,version='4.01',version_month='2026-06',printed_pages=[138,139,140,141],
        tonne_kg=1000,kilogram_g=1000,litre_ml=1000,minute_seconds=60,hour_minutes=60,day_hours=24,
        month_days_not_defined=True,student_sample_exists=False,non_si_status_distinguished=True),
}
CORRECTIONS={
    TK:'XML의 부록은 app 요소가 아닌 appsec1 절이다. 방향 파악의 같은 반나절 채점을 분 단위 시각 읽기에 적용하지 않는다. 시계 문항 4의 설명은 그림 1 캡션에서 11시 10분, 부록 A에서 1시 10분이며 불일치가 있다. 그림 자체를 본 것으로 표시하지 않는다.',
    SI:'검색 캐시의 V3.02 제목을 쓰지 않고 실제 표지의 V4.01·2026년 6월을 확인했다. 비SI 단위의 지위 설명을 이전 판본의 문구로 대신하지 않는다. 단위 정의를 학생 학습 효과로 표시하지 않으며 달의 고정된 일수는 이 표에 없다.',
}
INTERPRETATIONS={
    ('REV-4수03-22-1','SI26-01'):('activity_context',
        'kg와 g, t와 kg에서 각각 같은 양을 다른 단위로 바꾸고 수치가 달라지는 이유를 설명한다.',
        '정의와 환산의 참고다. 단위 관계를 말한 수행만으로 어림·측정의 숙달을 판정하지 않는다.'),
    ('REV-4수03-19-1','SI26-02'):('activity_context',
        '같은 물의 양을 L와 mL로 바꾼 뒤 덧셈·뺄셈하고 용기의 최대 들이와 비교한다.',
        '단위 정의는 과제 설계의 근거다. 실제 물 붓기나 눈금 읽기의 학생 수행은 별도로 확인한다.'),
    ('REV-2수03-09-1','SI26-03'):('activity_context',
        '분·시간·일의 고정된 관계로 같은 기간을 표현한 뒤 달력의 달 길이는 따로 확인한다.',
        '표의 24시간은 일 단위의 정의다. 한 달의 일수를 언제나 30일로 정하는 근거가 아니다.'),
    ('REV-4수03-13-2','SI26-03'):('inference_limit',
        '1분=60초와 1시간=60분이 어떤 두 단위를 비교하는지 각각 말하게 한다.',
        '단위 정의를 함께 적은 문서다. 초 단위 지식이 1시간·1분 관계 이해의 보편적 필수 선수라는 결과가 아니며 기존 관계의 방향을 바꾸지 않는다.'),
    ('REV-4수03-14-1','SI26-03'):('activity_context',
        '초를 더해 60초가 넘으면 분으로 다시 묶고 초만으로 계산한 결과와 대조한다.',
        '단위 환산의 수학적 근거다. 실제 경과 시간 추정이나 시계 읽기 정확성의 검증 자료는 아니다.'),
}

if __name__=='__main__':
    assert calendar.monthrange(2026,2)[1]==28 and calendar.monthrange(2026,3)[1]==31
    assert 28//7==4 and divmod(31,7)==(4,3)
    assert 2*1000+300==2300 and 1750+650-2000==400
    assert 2*60+5==125 and 170+85==4*60+15
    roles={cid:('related_theoretical_context' if sid==TK else 'mathematical_explanation') for sid,cid,*_ in CLAIMS}
    record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,
           interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='달력·시간 검사 설계와 단위 정의 참고',
           detail_key='calendar_units_review',roles=roles)

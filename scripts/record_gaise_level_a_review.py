"""Register a bounded GAISE II reading and independently calculated teaching examples."""
import copy
import hashlib
import json
from fractions import Fraction
from statistics import mean, median

from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews

SOURCE = 'GAISE_2020'
URL = 'https://www.amstat.org/asa/files/pdfs/GAISE/GAISEIIPreK-12_Full.pdf'
SHA = '085497d12a2822262de7c68ee7f65c102ba65cd8a523f7a91e01d2fd6119351f'
NOTES = 'data/literature_evidence/GAISE_2020_review_notes.json'
TEXT_PAGES = [3, 4, 5, 6] + list(range(21, 50))
VISUAL_PAGES = [24, 25, 26, 27, 28, 34, 36, 37, 38, 40, 41, 42, 43, 44, 46, 49]

MAPPINGS = [
    ('G2A01', ['6수04-03', '12실통01-02'], ['인쇄13–19 / PDF21–27', '인쇄22–23 / PDF30–31'],
     '변이를 예상하는 질문·자료·분석·맥락 해석을 연결하는 자체 설계에 참고한다.',
     'A/B/C는 고정 학년이 아니다. B·C가 앞선 경험을 발전시키는 설명을 한국 성취기준 사이의 단일 필수 선수 관계나 현재 학생의 단계 판정으로 바꾸지 않는다.'),
    ('G2A02', ['6수04-03', '12실통02-02'], ['인쇄24–25 / PDF32–33', '인쇄31–35 / PDF39–43'],
     '자료 한 행의 관찰 단위·변수 정의·누락과0의 구별을 확인하는 발문에 참고한다.',
     '관찰·설문·실험의 설계와 결론 범위를 구별한다. 무당벌레 표4와 그림11의 수치 차이는 미해결이므로 두 표현의 수치·중앙값을 섞어 사용하지 않는다.'),
    ('G2A03', ['6수04-01', '9수04-01'], ['인쇄28–30 / PDF36–38', '인쇄33–36 / PDF41–44'],
     '균등 분배의 평균과 분포 비교를 연결하되 자체 수치로 검산한다.',
     '원문 이동 steps의 계산 규칙을 분산·절대편차로 간주하지 않는다. 표·그림·본문의 중앙값 불일치는 인용 보류한다. Level A의 중앙값을 국내 초등의 새 필수 내용으로 넣지 않는다.'),
    ('G2A04', ['6수04-03'], ['인쇄24–27 / PDF32–35'],
     '그림기호의 단위·자료의 전체·표현 선택의 이유를 확인하는 자체 활동에 참고한다.',
     '근사 그림과 정확한 비를 구별한다. 제한된 응답 범주·한 학급의 조사 범위를 보존하고 비례 추론을 확인하지 않은 원그래프 활동을 일괄 요구하지 않는다.'),
    ('G2A05', ['6수04-05', '6수04-06'], ['인쇄22–23 / PDF30–31', '인쇄34–35 / PDF42–43'],
     '관찰한 비율과 자료 조건에 근거한 비형식적 가능성 판단을 구별하는 설계에 참고한다.',
     '이 틀은 현재 동전 모형의 공정성·독립성이나 실제 과제 효과를 검증하지 않는다. 아래 카드 모형은 자체 예이며 초등의0·반·1 범위를 일반 확률 공식의 필수 수행으로 확장하지 않는다.'),
    ('G2A06', ['6수04-03', '9수04-09'], ['인쇄37–41 / PDF45–49'],
     '시간의 간격·누락·축과 같은 대상의 짝 자료를 보존하는 자체 발문에 참고한다.',
     '시간 사이의 연결선은 미관측 날짜의 실제 값을 입증하지 않는다. 산점도의 경향·이상점 확인과 인과 주장을 구별하며 이상값을 자동 삭제하지 않는다.')
]

OBSERVATIONS = [
    dict(id='GA-P1', standard_codes=['6수04-01', '6수04-03', '12실통01-02', '12실통02-02'],
         question='가상 네 사람의 어제 독서 시간 기록은0분·10분·미응답·20분이다. 조사 질문·하루와 독서의 기준을 정하고0분과 미응답을 구별하라. 응답자의 평균과 네 사람 전체의 평균을 각각 알 수 있는가?',
         expected='기록된 세 응답의 평균은(0+10+20)÷3=10분이다.0분도 관측값으로 포함한다. 미응답을0분으로 채운7.5분을 네 사람 전체의 실제 평균이라고 할 수 없다. 네 사람 전체의 평균은 추가 정보 없이는 결정되지 않는다.',
         interpretation='누구의 어느 날 무엇을 기록했는지, 실제0과 누락, 응답자와 조사대상의 범위를 따로 기록한다. 교사가 미응답 처리법을 알려 주기 전과 후의 반응을 구별한다. 가상 자료이며 실제 수집·학생 응답이 아니다.', student_validated=False),
    dict(id='GA-P2', standard_codes=['6수04-03'],
         question='가상 자료 카드10장을 한 그림기호가4장인 그림그래프로 나타내라.2.5개 기호와 약3개 기호를 구별하고 각 표현에서 원래 카드 수를 정확히 되찾을 수 있는지 설명하라.',
         expected='10÷4=2.5이므로 온전한 기호2개와 반 기호1개가 정확한 표현이다. 약3개는 근사임을 표시해야 하며3개를 정확한 기호로 읽으면12장이 된다. 기호를 나눌 수 있는 디자인인지와 범례를 확인한다.',
         interpretation='기호 개수와 기호가 나타내는 카드 수, 정확한 값과 근사를 구별한다. 반 기호를 사용할 수 없는 표현이면 다른 단위나 그래프를 선택할 수 있다. 원문 버스 예의 근사 표현을 이 자체 예의 정확한 계산과 혼동하지 않는다.', student_validated=False),
    dict(id='GA-P3', standard_codes=['6수04-01', '9수04-01'],
         question='가상 블록 모임A는2·4·6개,B는1·4·7개다. 각각 같은 수로 나누어 평균을 구하고, 평균이 같다는 이유로 퍼진 모습도 같은지 설명하라. 실제 옮기는 블록 수와 평균에서 떨어진 거리의 합도 구별하라.',
         expected='두 모임 모두 합12개·자료3개·평균4개다. A는6개인 곳에서2개를2개인 곳으로,B는7개인 곳에서3개를1개인 곳으로 옮기면 된다. 최소 옮긴 블록은2개·3개이고 평균과 차이의 절댓값 합은4·6이다. 같은 평균이어도 자료와 퍼짐은 다르다.',
         interpretation='합·자료 수·균등한 양과 퍼짐을 따로 기록한다. 최소 이전 개수와 절대차 합을 원문의 steps라고 이름 붙이지 않는다. 절대차 계산은 교사용 확인이며 새로운 초등 공식이나 형식적 분산을 필수 요구하지 않는다.', student_validated=False),
    dict(id='GA-P4', standard_codes=['6수04-03', '6수04-05', '6수04-06'],
         question='가상20명의 한 가지 선호 응답이A10명·B6명·C4명이다. 가장 많은 범주A를 과반수라고 해도 되는가? 이20장의 같은 카드 중 한 장을 같은 가능성으로 뽑는 모형에서A가 나올 가능성과,새 학생이A를 고를지에 대한 판단을 구별하라.',
         expected='A가 가장 많지만10명은20명의 반이고 과반수는 아니다. 같은 가능성의20장 중A10장이므로 카드 모형의A 가능성은반이다. 이것이 새 학생의 응답이나 두 번 추출에서 반드시 한 번A라는 보장은 아니다. 새 집단 판단에는 조사 범위와 추가 자료가 필요하다.',
         interpretation='최다 범주·반·과반수,유한 카드 모형·관찰 비율·새 사람의 예측을 구별한다. 추출을 반복한다면 복원 여부도 먼저 정한다.10/20의 약분 공식을 초등의 새 필수 목표로 요구하지 않고 같은 카드의 절반이라는 설명을 허용한다.', student_validated=False),
    dict(id='GA-P5', standard_codes=['6수04-03'],
         question='가상 식물 높이가1일째2cm,2일째미측정,3일째8cm다. 가로축의 날짜 간격을 유지해 표시하고1일째부터3일째까지의 변화·하루 평균 변화와2일째 실제 높이를 구별하라.',
         expected='2일 동안6cm 증가했으므로 이 구간의 하루 평균 변화는3cm다.2일째 실제 높이는 알 수 없다. 직선 연결로5cm를 예상하려면 일정하게 자랐다는 추가 가정을 밝혀야 하며 측정값으로 기록하지 않는다. 미측정을0cm로 표시하지 않는다.',
         interpretation='날짜 차이·전체 변화·구간 평균·실제 관측을 구별한다. 하루 평균 변화의 형식 계산은 교사용 확장이며 초등에는 시간 간격과 미관측 표시를 중심으로 확인한다. 식물의 성장 원인이나 실제 학생의 이해를 검증한 자료가 아니다.', student_validated=False),
    dict(id='GA-P6', standard_codes=['9수04-09'],
         question='가상 대상별 짝 자료(1,2),(2,4),(3,6)과(1,6),(2,4),(3,2)를 비교하라. 각 열의 평균이 같으면 산점도의 경향도 같은가? 각 열을 따로 정렬한 뒤 다시 묶어도 같은 대상의 자료인가?',
         expected='두 자료 모두 첫 열 평균2·둘째 열 평균4지만 앞은 양의 경향,뒤는 음의 경향이다. 뒤 자료의 둘째 열을 따로 오름차순 정렬해 새로 묶으면 대상별 짝이 바뀌어 앞 자료처럼 된다. 대상ID와 짝을 함께 보존해야 하며 경향만으로 인과를 말하지 않는다.',
         interpretation='개별 열의 요약과 두 변수의 짝 관계,축·단위·대상ID를 따로 확인한다. 자체 수치 점검에는 중심화한 곱의 합을 사용하되 학생에게 상관계수 공식을 필수로 요구하지 않는다. 가상 모형이고 실제 사람을 조사한 자료가 아니다.', student_validated=False)
]


def numerical_guards():
    ladybug_table = dict(red=[6,16,6,16,18,18,16,0,16], orange=[10,10,20,20,20], black=[4,2,4,2,4])
    ladybug_figure = dict(red=[0,6,8,14,14,16,16,16,18], orange=[10,10,18,18,18], black=[2,2,4,4,4])
    dark = [1,1,1,1,2,3,3,4,4,5]
    light = [5,5,6,6,6,7,7,8,9,10]
    groups = [[2,4,5,5,6,7,8,8,9], [2,3,4,6,6,6,8,9,10]]
    assert {k: median(v) for k,v in ladybug_table.items()} == dict(red=16, orange=20, black=4)
    assert {k: median(v) for k,v in ladybug_figure.items()} == dict(red=14, orange=18, black=4)
    assert sum(map(len, ladybug_table.values())) == sum(map(len, ladybug_figure.values())) == 19
    assert median(dark) == 2.5 and median(light) == 6.5 and median(light)-median(dark) == 4
    assert [mean(v) for v in groups] == [6,6]
    assert [sum(max(x-6,0) for x in v) for v in groups] == [8,9]
    assert [sum(abs(x-6) for x in v) for v in groups] == [16,18]
    assert [sum((x-6)**2 for x in v) for v in groups] == [40,58]
    assert Fraction(13,5) == Fraction(26,10) and Fraction(5,2)*5 == Fraction(25,2)
    return [
        dict(kind='approximation_guard', location='인쇄26 / PDF34', observed='13명·기호당5명에 약2.5개라고 표현한다.', recomputed_exact_ratio='13/5=2.6', action='원문은 근사라고 명시하므로 오자로 확정하지 않는다.2.5개를 정확한13명의 비율로 복사하지 않는다.'),
        dict(kind='within_source_table_figure_mismatch', location='인쇄32–34 / PDF40–42', table_vectors=ladybug_table, figure_vectors=ladybug_figure,
             table_medians={k:median(v) for k,v in ladybug_table.items()}, figure_medians={k:median(v) for k,v in ladybug_figure.items()},
             action='본문 중앙값14·18·4는 그림11과 맞지만 표4와 다르다. 주황 범위도10–20과10–18로 달라진다. 원표와 그림 요약값을 혼용하지 않고 수치 전용은 보류한다. 정오표·작성 의도는 미확인이다.'),
        dict(kind='undefined_transfer_metric_guard', location='인쇄30 / PDF38', observed_groups=groups, source_steps=[48,58], minimum_cubes_transferred=[8,9], total_absolute_deviation=[16,18], sum_squared_deviation=[40,58],
             action='steps 계산 규칙이 재사용할 만큼 명시되지 않았다. 옮긴 큐브 수·절대차·제곱차와 동일시하거나48을40으로 고치지 않는다. 오자라고 확정하지 않는다.'),
        dict(kind='within_source_figure_text_median_mismatch', location='인쇄35–36 / PDF43–44', figure_dark=dark, figure_light=light, figure_medians=[median(dark),median(light)], source_text_light_median=7.5, source_text_difference=5,
             action='그림13의 점과 중앙선은 밝은 곳6.5·어두운 곳2.5,차4다. 본문7.5·차5와 불일치해 수치 인용을 보류한다. 질문2주와 분석8일의 시점도 구별한다. 원자료·정오표는 미확인이다.'),
        dict(kind='missing_timepoint_rate_guard', location='인쇄37–38 / PDF45–46', observed_day8=7, missing_day9=True, observed_day10=10, two_day_change=3, interval_daily_average=1.5,
             action='8→10일의3cm 변화는2일 간격이다.9일 실제 값과 각 하루 증가량은 미관측이며0으로 채우거나 연결선 값을 실측으로 제시하지 않는다. 확인한 연속 날짜의 증가와 누락 구간 평균을 구별한다.')
    ]


def verify():
    numerical_guards()
    assert mean([0,10,20]) == 10 and mean([0,10,0,20]) == 7.5
    assert Fraction(10,4) == Fraction(5,2) and 3*4 == 12
    for values, moved in [([2,4,6],2), ([1,4,7],3)]:
        assert len(values)==3 and sum(values)==12 and mean(values)==4
        assert sum(max(x-4,0) for x in values)==moved
        assert sum(abs(x-4) for x in values)==2*moved
    assert 10+6+4==20 and 10==20/2 and not 10>20/2
    assert (8-2)/(3-1)==3
    for pairs, expected in [([(1,2),(2,4),(3,6)],4), ([(1,6),(2,4),(3,2)],-4)]:
        assert mean([x for x,y in pairs])==2 and mean([y for x,y in pairs])==4
        assert sum((x-2)*(y-4) for x,y in pairs)==expected
    assert len(TEXT_PAGES)==33 and len(VISUAL_PAGES)==16 and set(VISUAL_PAGES)<=set(TEXT_PAGES)


def main():
    verify()
    registry=load_registry(); before=set(load_reviews()['records'])
    if SOURCE in registry['sources']:
        print('GAISE bounded reading and targets remain current; no automatic refresh')
        build_report(); return
    assert not {m[0] for m in MAPPINGS}&{c['id'] for c in registry['claims']}
    raw=ROOT/'tmp/literature/GAISE_2020.pdf'
    assert hashlib.sha256(raw.read_bytes()).hexdigest()==SHA
    pages=json.loads((ROOT/'tmp/literature/GAISE_2020_pages.json').read_text(encoding='utf-8'))
    assert len(pages)==126 and all(pages[p-1]['pdf_page']==p for p in TEXT_PAGES)
    images=[]
    for p in VISUAL_PAGES:
        file=ROOT/f'tmp/literature/GAISE_2020-p{p}.png'
        images.append(dict(pdf_page=p,local_temporary_file=file.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
    notes=dict(source_id=SOURCE,source_url=URL,source_pdf_sha256=SHA,date='2026-11-06',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,pdf_pages_total=126,
        read_pdf_pages=TEXT_PAGES,visually_reviewed_pages=images,source_corrections=numerical_guards(),
        reading_log=['PDF3–6의 표제·저작권·목차를 확인했다.',
            'PDF21–27의 프레임워크와 표1의 모든 열,PDF28의 빈 쪽,PDF29–49의Level A 본문을 읽었다. 본문은 인쇄13–19·21–41에 해당한다.',
            '텍스트33쪽과 선정16쪽의 전체 페이지 이미지를 확인했다. 표4·그림11·그림13·시계열 표6을 본문과 대조하고 수치는 자체 재계산했다.'],
        unread_followups=['서문·도입 본문,Level B/C 장,Assessment,참고문헌 본문은 미독이다. 표1의B/C 열을 읽은 것을 해당 장의 독해로 집계하지 않는다.','More4U·인용 원연구·공식 정오표·원자료는 미확인이다. 전체126쪽 독해나 현재 한국어 과제 효과로 표시하지 않는다.'],
        interpretation_limits=['A/B/C는 통계적 경험의 발전을 다루며 고정된 나이·학년 배치가 아니다. 앞선 경험을 발전시키는 틀을 국내 기준 전체의 단일 필수 경로로 바꾸지 않는다.','이 문헌은 교육 프레임워크다. IES식 권고 근거 등급·현재 과제의 효과 크기·독립 검토·학생 검증을 부여하지 않는다.','원문은 저작권 유보 판본이므로 PDF·페이지 이미지는 임시 확인용으로만 두고 자체 읽기 기록·주소·해시를 보존한다.'])
    (ROOT/NOTES).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'data/sources.json'; sources=json.loads(path.read_text(encoding='utf-8'))
    b=next(v for v in sources if v['id']==SOURCE); previous=copy.deepcopy(b)
    b.update(title='Pre-K–12 Guidelines for Assessment and Instruction in Statistics Education II (GAISE II): A Framework for Statistics and Data Science Education',
        authors=['Anna Bargagliotti','Christine Franklin','Pip Arnold','Sheri Johnson','Leticia Perez','Denise A. Spangler','Rob Gould'],publisher='American Statistical Association',isbn='9781734223514',
        review_scope='126쪽 PDF 중 표제·서지·목차와 프레임워크·Level A의33쪽 텍스트,선정16쪽 이미지를 확인. 표1의B/C 열만 확인했으며 B/C 본문·평가 장·참고문헌·원연구·More4U는 미대조.',
        next_review='서문·도입 및Level B/C·Assessment·참고문헌의 본문 독해,원연구·정오표·표/그림 수치와 한국어 과제의 실제 반응을 추가 대조한다.')
    registry['sources'][SOURCE]=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-06',snapshot_kind='authored_review_notes',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256((ROOT/NOTES).read_bytes()).hexdigest(),source_pdf_sha256=SHA,redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,
        display=dict(title=b['title'],url=URL,authors_year='Bargagliotti 외,2020,ASA,GAISE II'),read_scope='PDF3–6·21–49의33쪽 텍스트(빈28쪽 포함),선정16쪽 이미지;프레임워크·Level A 범위',
        scope_note='통계 탐구 설계의 참고 틀이다. 수준의 고정 학년 대응·유일한 선수 경로·현재 학생의 단계나 과제 효과를 입증하지 않는다.',
        method_note='표1과Level A를 대조하고 자체 관찰의 수치를 별도 계산했다. 표제·목차 확인과 본문 독해를 구별하며 B/C는 표1의 열만 읽었다.',
        limits='전체126쪽 중 지정33쪽 범위다. 원문 표4와 그림11,그림13과 본문의 수치 불일치는 전용을 보류했다. 근사 그림과 정의가 충분하지 않은 steps를 별도 표시했다. 정오표·원자료·인용 연구는 미확인이다. PDF·페이지 이미지는 재배포하지 않는다.',
        editorial_action='현재8개 기준에 주장6건과 가상 자체 관찰6건을 대응했다. 관찰 단위·누락·기호 단위·균등화·가능성 모형·날짜 간격·짝 보존을 점검했다. 관계 승인·독립 검토·실제 학생 검증 수는 늘리지 않았다.',independent_review=False,student_validated=False,observations=OBSERVATIONS)
    for cid,codes,locations,support,limit in MAPPINGS:
        registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,
            target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},standard_codes=codes,independent_review=False,student_validated=False))
    path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'data/content_review_queue.json'; queue=json.loads(path.read_text(encoding='utf-8'))
    row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE)
    row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[m[0] for m in MAPPINGS])
    path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert set(load_reviews()['records'])==before
    load_registry(); build_report()
    print('Added GAISE II bounded review: 6 claims / 6 own observations; relation reviews unchanged')


if __name__=='__main__':
    main()

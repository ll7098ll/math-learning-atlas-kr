"""Freeze an editorial classification of all standards; maintain the resulting JSON.

Uses the existing analysis families as a starting point and explicit code-level
decisions for mixed families. It never classifies by keyword or invents edges.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT / 'data' / (name + '.json')).read_text(encoding='utf-8'))

groups = []
def group(id, title, domain, labels, question):
    groups.append(dict(id=id, title=title, domain=domain, stage_labels=labels.split('|'), question=question,
                       primary_codes=[], additional_codes=[]))

N, A, G, S, X = '수와 연산', '변화와 관계', '도형과 측정', '자료와 가능성', '활용과 탐구'
group('number','수·자릿값·수의 확장',N,'자연수와 자릿값|정수·실수의 의미와 순서|복소수와 연산','새로운 수와 표현은 왜 필요할까요?')
group('operations','사칙연산과 연산의 관계',N,'덧셈·뺄셈·곱셈·나눗셈|부호 있는 수의 연산|직무 상황의 수와 연산','계산의 의미와 연산 관계는 어떻게 유지될까요?')
group('fraction','분수·소수·유리수',N,'분수·소수의 의미와 계산|유리수와 순환소수|분수 표현과 이어지는 내용','같은 양과 몫을 어떻게 다른 수로 표현할까요?')
group('divisibility','약수·배수·소인수분해',N,'약수·배수와 공통 관계|소인수분해와 공약수·공배수|인수 구조와의 연결','공통된 인수를 어떻게 찾고 활용할까요?')
group('estimate','어림·근삿값',N,'계산의 어림과 올림·버림·반올림|어림을 활용하는 사고|직무 상황의 큰 수 어림','목적에 맞는 정밀도와 어림값은 무엇일까요?')
group('radical','제곱근·근호·무리함수',N,'제곱과 크기 비교의 기초|제곱근과 근호식의 연산|거듭제곱근과 무리함수','제곱의 역과 새 수 표현을 어떻게 해석할까요?')
group('exponential','거듭제곱·지수·로그',A,'묶음과 자릿값의 기초|지수법칙|지수의 확장·로그·함수','반복되는 곱을 어떻게 표현하고 역으로 읽을까요?')
group('expression','문자식·다항식·인수분해',A,'혼합 계산과 식의 구조|문자식·다항식·인수분해|다항식 연산과 이항정리','수식의 구조를 보며 같은 표현으로 바꿀 수 있을까요?')
group('equation','등식·방정식·항등식',A,'등호·빈칸·역관계|등식의 성질과 방정식|방정식과 항등식의 확장','어떤 값에서 식이 참이며 같은 관계를 유지할까요?')
group('inequality','수의 범위·부등식',A,'이상·이하·초과·미만|일차부등식과 해의 범위|연립·절댓값·이차부등식','조건을 만족하는 값의 범위는 어떻게 나타낼까요?')
group('sequence','규칙·수열·급수',A,'배열과 변화 규칙|규칙을 일반화하는 사고|수열·극한·급수','순서에 따른 규칙과 부분합은 어떻게 일반화될까요?')
group('function','대응·함수·그래프',A,'두 양의 대응과 식|함수·일차함수·이차함수|함수의 합성·역함수·모델링','입력과 출력의 관계를 표·식·그래프로 읽을 수 있을까요?')
group('ratio','비·비율·비례·유리함수',A,'비·백분율·비례식·비례배분|정비례·반비례·상대도수|유리함수와 비율의 활용','비교의 기준과 불변량은 무엇일까요?')
group('limit','함수의 극한·연속',A,'가까워짐과 변화의 기초|함수 관계를 읽는 사고|함수의 극한·연속·미분가능성','가까워지는 값과 실제 함숫값은 어떻게 다를까요?')
group('derivative','기울기·변화율·미분',A,'변화를 비교하는 기초|일차함수의 기울기|미분계수·도함수·미분의 활용','변화량의 비에서 국소 변화율로 무엇이 더해질까요?')
group('integral','누적·적분',A,'부분과 전체를 구성하는 사고|측정과 함수의 기초|부정적분·정적분·누적','부분의 합과 변화의 누적을 어떻게 연결할까요?')
group('optimization','최대·최소·최적화',A,'목적에 따른 비교의 기초|함수와 조건의 해석|최대·최소·손실함수·경사하강법','목표와 조건을 수학적으로 어떻게 정할까요?')
group('matrix','행렬과 행렬 연산',A,'표와 수의 연산 기초|자료·연산의 구조|행렬·역행렬·이미지 변환','자료의 배열과 연산은 어떻게 연결될까요?')
group('sets','집합과 집합의 연산',A,'분류와 기준의 기초|대상의 관계를 읽는 사고|집합·포함·연산·데이터 표현','같은 기준으로 모은 대상을 어떻게 다룰까요?')
group('logic','명제·논증·증명·귀납',A,'조건을 설명하는 기초|수학적 정당화|명제·조건·증명·수학적 귀납법','성립 조건과 참인 이유를 어떻게 설명할까요?')
group('plane','평면도형·성질·작도',G,'평면 모양·분류·구성|도형의 성질·작도·정당화|도형의 성질을 활용하는 내용','도형을 정의하고 성질을 정당화할 수 있을까요?')
group('lines','직선·평행·수직',G,'직선·선분·수직·평행|평행선과 각의 관계|직선의 방정식·위치·거리','도형의 위치 관계를 어떻게 표현할까요?')
group('circle','원·부채꼴·이차곡선',G,'원의 구성과 넓이|부채꼴·원의 성질|원의 방정식과 이차곡선','기하적 성질을 측정과 방정식으로 어떻게 넓힐까요?')
group('symmetry','이동·합동·대칭',G,'밀기·뒤집기·돌리기·합동·대칭|합동 조건|좌표의 이동과 직무 적용','옮겨도 유지되는 성질은 무엇일까요?')
group('similarity','닮음과 길이의 비',G,'비와 대응의 기초|닮음·길이비·닮음 조건|닮음의 직무 적용','같은 모양에서 길이와 크기는 어떻게 달라질까요?')
group('trig','각도·삼각비·삼각함수',G,'각의 측정과 내각|피타고라스 정리와 삼각비|일반각·삼각함수·법칙','각과 길이의 관계는 어떻게 함수가 될까요?')
group('coordinate','위치·좌표·벡터',G,'격자에서 위치와 이동|순서쌍과 좌표|내분·공간좌표·벡터','위치와 방향을 수와 식으로 나타낼 수 있을까요?')
group('solid','입체·공간도형',G,'입체의 모양과 구성|공간 위치·다면체·회전체|공간 위치의 논증·정사영','공간의 대상을 구성하고 위치를 설명할 수 있을까요?')
group('spatial','전개도·공간 시각화',G,'쌓기나무·전개도·여러 방향의 모습|입체 이해와의 연결|겨냥도·전개도·직무 도면','평면의 표현에서 공간의 전체를 추론할 수 있을까요?')
group('units','길이·들이·무게·단위',G,'직접 비교·측정·표준 단위·환산|측정과 단위의 활용|직무의 표준 단위와 환산','무엇을 어떤 단위로 재고 비교할까요?')
group('time','시각과 시간',G,'시계·시간 단위·시간의 계산|시간과 변화의 연결|직무의 시간 단위 환산','시각과 경과 시간을 어떻게 구별하고 나타낼까요?')
group('area','둘레와 넓이',G,'둘레·넓이 단위·분해와 합성|부채꼴의 넓이|직무의 넓이·곡선 영역','부분을 나누고 합하면서 무엇이 보존될까요?')
group('volume','겉넓이와 부피',G,'겉넓이·부피 단위·입체 측정|입체의 겉넓이와 부피|직무 측정·단면의 누적','면을 덮는 양과 공간을 채우는 양은 어떻게 다를까요?')
group('collection','자료의 분류·수집',S,'기준에 따른 분류와 자료 수집|탐구에 맞는 자료 수집|자료의 종류·수집 방법·표집','질문에 맞는 자료를 어떻게 얻을까요?')
group('graphs','표·그래프·자료 표현',S,'표와 여러 그래프|분포의 표·그래프·상자그림|목적에 맞는 자료 표현과 해석','자료의 무엇을 보여주기 위해 어떤 표현을 고를까요?')
group('average','평균·대푯값·산포',S,'평균의 의미|중심과 퍼짐|기댓값·대푯값·산포의 선택','하나의 수로 요약하면 무엇이 보이고 가려질까요?')
group('association','상관·추세·예측',S,'변화를 표현하는 기초|산점도와 상관관계|추세선과 데이터 예측','자료 사이의 관계를 어디까지 해석할 수 있을까요?')
group('counting','경우의 수·순열·조합',S,'대상을 세고 분류하는 기초|경우의 수의 구조|합·곱의 법칙·순열·조합','빠짐과 중복 없이 가능한 경우를 셀 수 있을까요?')
group('probability','가능성·확률·조건부확률',S,'가능성의 비교와 수 표현|확률과 기본 성질|확률 모형·조건·독립·예측','조건과 모형에 따라 가능성은 어떻게 달라질까요?')
group('distribution','확률변수와 확률분포',S,'자료와 가능성의 기초|확률과 분포의 이해|확률변수·이항분포·정규분포','불확실한 결과를 수와 분포로 어떻게 나타낼까요?')
group('inference','표본·추정·검정',S,'자료에 근거한 예상의 기초|통계적 탐구와 변동|표집·추정·가설검정','일부 자료로 전체에 대해 무엇을 말할 수 있을까요?')
group('inquiry','통계적 탐구와 의사결정',S,'질문·수집·표현·해석|통계적 탐구의 순환|탐구의 실행·성찰·의사결정','자료로 질문에 답하고 판단을 되돌아볼 수 있을까요?')
group('ai','데이터와 인공지능 학습',X,'자료·분류·규칙의 기초|자료와 함수의 연결|데이터의 특성·분석·인공지능','데이터에서 규칙을 학습한다는 것은 무엇일까요?')
group('finance','경제지표와 금융수학',X,'수·비율·단위의 기초|함수와 수량 관계|경제지표·환율·세금·이자·연금','경제 상황에서 수와 관계는 어떻게 쓰일까요?')
group('culture','생활·문화·환경의 수학',X,'수와 도형·자료의 활용|관계와 수학적 설명|문화·생활·환경의 수학적 탐구','맥락에 맞는 수학을 선택하고 해석할 수 있을까요?')
group('research','수학 탐구·설계·성찰',X,'질문과 설명의 기초|탐구와 수학적 논증|연구 방법·윤리·실행·평가','수학적 질문을 어떻게 연구하고 공유할까요?')

elementary=read('analysis_details')['analyses']
secondary=read('secondary_analysis_details')['analyses']
families={a['code']:a['family'] for a in elementary+secondary}
families.update({'6수01-10':'fraction','6수02-03':'ratio','6수03-14':'area'})
family_map={
 'count':'number','place':'number','order':'number','add':'operations','multiply':'operations','divide':'operations',
 'equality':'equation','fraction':'fraction','decimal':'fraction','fracop':'fraction','estimate':'estimate',
 'divisibility':'divisibility','expression':'expression','pattern':'sequence','ratio':'ratio',
 'plane':'plane','line':'lines','motion':'symmetry','solid':'solid','nets':'spatial','compare':'units',
 'measure':'units','time':'time','area':'area','surface':'volume','volume':'volume','mean':'average','data':'graphs','chance':'probability',
 'number':'number','algebra':'expression','equation':'equation','inequality':'inequality','coordinate':'coordinate',
 'function':'function','geometry':'plane','trig':'trig','stats':'graphs','counting':'counting','probability':'probability',
 'optimization':'optimization','matrix':'matrix','logic':'logic','exponential':'exponential','sequence':'sequence',
 'limit':'limit','derivative':'derivative','integral':'integral','conic':'circle','vectors':'coordinate',
 'finance':'finance','ai':'ai','research':'research','culture':'culture','inference':'inference','job':None}
assignment={code:family_map[f] for code,f in families.items()}
def codes(spec):
    result=[]
    for token in spec.split():
        if ':' not in token:result.append(token);continue
        prefix,nums=token.split(':')
        for part in nums.split(','):
            lo,_,hi=part.partition('-')
            result.extend(prefix+f'{n:02d}' for n in range(int(lo),int(hi or lo)+1))
    return result
def assign(id,spec):
    for code in codes(spec):
        assert code in assignment,code
        assignment[code]=id

assign('inequality','6수01-02')
assign('divisibility','9수01-01 9수01-02')
assign('operations','9수01-05')
assign('fraction','9수01-06')
assign('radical','9수01-07 9수01-10 12대수01-01 10공수2-03-05 10기수2-03-05')
assign('exponential','9수02-08')
assign('function','6수02-01 12경수02-:01-05 12직수02-03 12직수02-04')
assign('ratio','9수02-07 9수04-03 10공수2-03-04 10기수2-03-04 12직수02-01 12직수02-02 6수03-15')
assign('equation','10공수1-01-02 12직수02-05')
assign('derivative','9수02-16')
assign('limit','12미적Ⅰ-02-02')
assign('sequence','12미적Ⅱ-01-:01-05')
assign('sets','10공수2-02-:01-03 10기수2-02-:01-03')
assign('lines','9수03-02 10공수2-01-02 10공수2-01-03 10기수2-01-02 10기수2-01-03')
assign('circle','4수03-06 4수03-07 6수03-16 9수03-06 9수03-10 9수03-18 9수03-19 10공수2-01-04 10공수2-01-05 10기수2-01-04 10기수2-01-05')
assign('symmetry','10공수2-01-06 10공수2-01-07 10기수2-01-06 10기수2-01-07 12직수03-03')
assign('symmetry','9수03-04')
assign('coordinate','4수03-05')
assign('trig','4수03-02 4수03-24 4수03-25 9수03-15')
assign('similarity','9수03-:12-14')
assign('solid','9수03-01 9수03-07 12기하02-:01-03')
assign('volume','9수03-08 12직수03-05')
assign('area','12직수03-04')
assign('spatial','12직수03-01 12직수03-02')
assign('units','12직수01-03')
assign('operations','12직수01-01')
assign('estimate','12직수01-02')
assign('collection','2수04-01 12실통02-01 12실통02-02')
assign('average','9수04-01 9수04-07 12확통03-02 12실통02-04')
assign('association','9수04-09 12인수04-02')
assign('distribution','12확통03-01 12확통03-03 12확통03-04')
assign('inquiry','4수04-03 6수04-03 9수04-04 12실통01-01 12실통01-02 12실통04-01 12실통04-02 12직수04-05')
assign('graphs','12수문03-03')
assign('coordinate','12인수02-01 12인수02-02')

by_id={g['id']:g for g in groups}
inventory=read('standards')['standards']
for s in inventory:
    code=s['code'];id=assignment[code]
    assert id in by_id,(code,id)
    by_id[id]['primary_codes'].append(code)
def additional(id,spec):
    by_id[id]['additional_codes']=[c for c in codes(spec) if c not in by_id[id]['primary_codes']]
additional('operations','4수01-15 4수01-16 6수01-08 6수01-09 6수01-11 6수01-13 6수01-14 6수01-15')
additional('fraction','9수01-03 9수01-04 9수01-05')
additional('inequality','12직수02-05 12경수02-06')
additional('sets','12인수02-01')
additional('coordinate','10공수2-01-:02-07 10기수2-01-:02-07')
additional('logic','9수03-09 9수03-15')
additional('similarity','12직수03-03')
additional('time','12직수01-03')
additional('area','6수03-16 9수03-06 12미적Ⅰ-03-05 12미적Ⅱ-03-05')
additional('volume','12미적Ⅱ-03-06')
additional('trig','12미적Ⅱ-02-03')
additional('collection','4수04-03 6수04-03 9수04-04 12실통01-03')
additional('average','12확통03-06')
additional('association','12인수04-03')
additional('distribution','12확통03-02')
additional('graphs','4수04-03 6수04-03 9수04-04 12직수04-05')

result=dict(schema_version='2.0',title='전체 성취기준의 개념별 연결 지도',
 classification='435개 성취기준의 내용을 검토한 연구용 개념 분류',
 interpretation='각 기준에 주 개념을 하나 지정하고, 여러 개념을 함께 다루면 추가 묶음에도 표시한다. 연결은 기존 관계 기록을 사용하며 학교급 배치를 필수 이수 순서로 해석하지 않는다.',
 assignment_basis='기존 개별 분석의 사고 유형을 출발점으로 성취기준의 원문과 내용을 대조하여 코드별로 분류했다. 키워드나 관계 수로 자동 배정하지 않는다.',
 groups=groups)
assert len(assignment)==len(inventory)==435
assert sum(len(g['primary_codes']) for g in groups)==435
(ROOT/'data/concept_taxonomy.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'concepts':len(groups),'primary_standards':435,'additional_memberships':sum(len(g['additional_codes']) for g in groups)},ensure_ascii=False))

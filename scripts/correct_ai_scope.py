"""Reconcile three AI entries with the official course's explicit scope limits."""
from pathlib import Path
from datetime import date
from copy import deepcopy
import json

root=Path(__file__).resolve().parents[1]
path=root/'data/revisions_high.json'
data=json.loads(path.read_text(encoding='utf-8'));stamp=date.today().isoformat()
for code,pages,reason in [
 ('12인수02-03',[193],'코사인 유사도는 성분 계산으로 표현하고 이 과목에서 사용하지 않는 기하의 용어·기호를 기본 해설에서 분리한다.'),
 ('12인수04-01',[194,195],'상대도수로 확률을 계산하는 범위를 유지하고 다른 과목의 조건부확률 용어·기호는 선택적 비교 연결로 구별한다.'),
 ('12인수04-03',[194,195],'손실 최적화의 기본 범위를 y=ax의 일변수 손실함수로 바로잡고 이전 기울기·절편 동시 최적화 원고를 이력에 보존한다.')]:
    entry=data[code]
    if entry.get('review',{}).get('scope_revision')=='ai-official-scope-2026-11-04':continue
    assert not entry['review'].get('independentReview') and not entry['review'].get('studentValidated')
    old=deepcopy({k:v for k,v in entry.items() if k!='scopeCorrections'})
    entry.setdefault('scopeCorrections',[]).append(dict(date=stamp,reviewer='Codex',source_id='CURRICULUM_2022_33',pdf_pages=pages,reason=reason,previous_record=old))
    if code=='12인수02-03':
        solution='u=(1,1),v=(2,0)에서 같은 위치의 성분끼리 곱해 더하면 1×2+1×0=2다. 두 길이는 √(1²+1²)=√2,√(2²+0²)=2다. 코사인 유사도는 2/(2√2)=1/√2≈0.7071이다. v를 양수배하면 분자와 분모 배율이 상쇄되어 같다. 영벡터는 분모 0이므로 별도 처리한다.'
        entry['taskSolution']=solution;entry['paths']=[solution]
        entry['thinking'][0].update(meaning='같은 위치 성분 곱의 합과 두 길이를 계산한다.',observable='1×2+1×0=2,두 길이는 √2와 2다.')
        entry['representations']=['공통 어휘 순서,성분별 곱의 합,두 길이,정규화 비율을 기록한다.']
        relation=entry['internalRelations'][0]
        relation.update(rationale='기하의 벡터 연산과 인공지능의 성분 기반 유사도를 선택적으로 비교한다.',
            conditions=['공통 어휘 순서와 비영 벡터를 사용한다. 인공지능 수학의 기본 해설은 성분 곱의 합과 길이로 계산하고 기하의 추가 용어·기호를 필수로 요구하지 않는다.'],
            diagnostic='공통 어휘 순서를 다르게 만든 두 벡터의 같은 위치 곱을 유사도로 해석할 수 있는가?')
    elif code=='12인수04-01':
        entry['mathematicalMeaning']='관측 상대도수는 자료 생성 과정과 모형 가정에 의존하는 예측이다. 가상 센서의 같은 운영 상태 기록 20건 중 알림 발생 6건을 사용한다.'
        solution='상대도수는 6/20=0.3이다. 같은 운영 상태와 측정 기준이 유지된다는 모형 아래 다음 알림 발생 확률을 0.3으로 추정한다. 새 자료에서 발생률과 예측오차를 다시 비교하며 관찰 0건을 불가능한 사건으로 단정하지 않는다.'
        entry['taskSolution']=solution;entry['paths']=[solution];entry['conditions']=['같은 운영 상태와 측정 기준에서 얻은 가상 관측 20건 중 알림 6건이다.']
        entry['thinking'][0].update(meaning='전체 관측 수와 발생 수를 센다.',observable='알림 상대도수는 6/20=0.3이다.',reason='분자와 분모가 같은 관측 기간과 대상을 가리켜야 한다.')
        entry['representations']=['관측 수 20,발생 수 6,상대도수 0.3과 자료 생성 상태를 기록한다.']
        entry['review']['scope']='이 과목은 상대도수로 예측을 다룬다. 다른 과목의 추가 용어·기호를 이 과목의 필수 수행으로 요구하지 않는다.'
        entry['internalRelations'][0].update(rationale='인공지능의 상대도수 예측을 확률과 통계의 기준 집단 재설정과 선택적으로 비교한다.',
            conditions=['인공지능 수학의 기본 경로는 상대도수를 사용한다. 확률과 통계 과목의 용어·기호를 이미 배운 경우에만 별도 연결로 비교하고 이를 인공지능 수학의 필수 선수로 삼지 않는다.'],
            diagnostic='관측 기록의 대상이나 기간을 바꾸면 상대도수 예측의 분모도 함께 다시 정해야 하는가?')
    else:
        entry['mathematicalMeaning']='원점을 지나는 추세선 y=ax에서 기울기 a 하나에 따른 제곱오차 합을 비교하고 최소를 구한다. 가상 자료는 (1,2),(2,3),(3,5)다.'
        solution='a=1이면 제곱오차 합은 6,a=2이면 2다. 전체 손실은 L(a)=(a−2)²+(2a−3)²+(3a−5)²=14a²−46a+38=14(a−23/14)²+3/14다. 따라서 모든 실수 a에서 최소는 3/14이며 a=23/14에서만 달성된다. 이 과목의 기본 최적화 대상은 y=ax의 일변수 손실이며 훈련 손실의 최소와 새 자료 예측 성능은 구별한다.'
        entry['taskSolution']=solution;entry['paths']=[solution]
        entry['conditions']=['가상 자료 (1,2),(2,3),(3,5)에 y=ax를 적용하고 기울기 a 하나만 바꾼다. 절편은 0으로 고정한다.']
        entry['thinking']=[dict(label='잔차',meaning='같은 자료에서 예측값과 관측값의 차를 구한다.',observable='세 잔차를 a−2,2a−3,3a−5로 표현한다.',reason='다른 후보를 같은 데이터와 척도로 비교한다.'),
            dict(label='손실',meaning='잔차를 제곱하여 하나의 일변수함수로 모은다.',observable='L(a)=14a²−46a+38을 얻는다.',reason='잔차의 양·음 상쇄를 막고 매개변수 하나의 변화를 비교한다.'),
            dict(label='최적해',meaning='모든 매개변수 값에서 성립하는 하한과 달성점을 찾는다.',observable='완전제곱식에서 최소 3/14와 a=23/14를 확인한다.',reason='두 후보 중 작은 값이라는 사실과 전역 최소의 증명을 구별한다.'),
            dict(label='평가',meaning='훈련 손실과 새 자료 성능을 구별한다.',observable='선택한 a를 별도 평가 자료에 적용하고 오차를 비교한다.',reason='학습 자료에 맞는 것만으로 일반화를 입증할 수 없다.')]
        entry['diagnostics'][-1].update(question='두 후보 중 손실이 작다는 사실만으로 모든 a 중 최소를 보였는가?',expected='아니다. L=14(a−23/14)²+3/14의 비음수와 등호 조건으로 확인한다.',followup='제곱항이 0이 되는 a를 구한다.')
        entry['review']['scope']='y=ax 형태 추세선의 일변수 손실만 기본 범위로 다룬다. 절편을 함께 최적화한 이전 원고는 수정 이력에 보존한다.'
    entry['review']['scope_revision']='ai-official-scope-2026-11-04'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Reconciled 3 AI entries; previous complete records retained')

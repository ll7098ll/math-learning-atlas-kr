"""Author scoped middle-school connections; preserve existing relation records."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADDITIONS = [
    ('9수03-03', 'internalRelations', {
        'from': '9수03-01', 'target': '9수03-03', 'kind': 'requires_for_task',
        'scope': '두 변의 길이와 끼인각이 주어진 삼각형을 자와 컴퍼스로 작도하는 경로',
        'rationale': '주어진 각의 두 반직선에 각각 지정한 길이를 옮겨 두 꼭짓점을 잡고 연결한다. 반직선과 선분 및 각의 의미를 유지해야 주어진 조건을 만족한 삼각형인지 설명할 수 있다.',
        'conditions': ['두 변의 길이는 양수이고 끼인각은 0도보다 크고 180도보다 작다.', '자의 눈금으로 길이를 재는 것과 컴퍼스로 길이를 옮기는 조작을 구별한다.'],
        'additionalLearning': '컴퍼스의 벌어진 폭을 보존하여 선분 길이를 옮기고, 각을 복사한 뒤 교점을 꼭짓점으로 정한다.',
        'diagnostic': '길이 4cm, 5cm인 두 변과 끼인각 60도를 작도할 때 두 길이를 어느 반직선에 옮기며, 각이 끼인각이라는 조건을 어디에서 확인하는가?',
        'limit': '선분·각의 해석에 관한 조건이다. 위치 관계 기준 전체의 사전 숙달이나 이 작도 경로만을 요구하지 않는다. 세 변이 주어진 경로는 별도로 비교한다.',
    }),
    ('9수03-15', 'internalRelations', {
        'from': '9수03-13', 'target': '9수03-15', 'kind': 'requires_for_task',
        'scope': '빗변에 내린 높이와 삼각형 닮음을 이용해 피타고라스 정리를 정당화하는 경로',
        'rationale': '직각삼각형 ABC에서 C가 직각이고 CH가 빗변 AB에 수직이면 세 삼각형의 두 각이 각각 같다. 닮음에서 AC²=AB·AH, BC²=AB·BH를 얻고 합하면 AC²+BC²=AB²이다.',
        'conditions': ['H는 빗변 AB 위에서 C의 수선의 발이다.', '닮은 삼각형의 대응 꼭짓점과 대응변을 일치시키고 양의 길이로 비례식을 세운다.'],
        'additionalLearning': '두 비례식을 변 길이의 제곱 관계로 바꾼 뒤 AH+BH=AB를 적용한다.',
        'diagnostic': 'AC²=AB·AH를 주는 두 삼각형의 대응을 쓰고, BH 대신 AH를 두 번 쓰면 합의 어느 단계가 성립하지 않는지 설명한다.',
        'limit': '닮음에 의한 정당화 경로의 조건이다. 넓이 재배치로 정당화하는 경로에는 삼각형 닮음의 선행 숙달을 강제하지 않는다.',
    }),
    ('9수04-08', 'internalRelations', {
        'from': '9수04-01', 'target': '9수04-08', 'kind': 'requires_for_task',
        'scope': '정렬한 자료의 중앙값과 하위·상위 절반의 중앙값을 도구의 상자 경계와 대조하는 경로',
        'rationale': '예시 관례에서 중앙값은 전체의 가운데, Q1과 Q3는 하위·상위 절반의 가운데를 요약한다. 중앙값의 위치 의미를 유지해 공학 도구가 그린 세 경계가 어떤 값을 나타내는지 확인한다.',
        'conditions': ['자료의 정렬 순서를 유지한다.', '사분위수 계산과 수염 규칙은 도구마다 다를 수 있으므로 설정을 기록하며, 예시 관례와 도구 설정을 대조한다.'],
        'additionalLearning': '사분위범위와 전체 범위를 구별하고 같은 축에서 두 분포를 비교한다. 공학 도구를 실제로 사용하는 수행도 포함한다.',
        'diagnostic': '5,8,10,12,14,16,18,21에서 전체 중앙값은 13이다. 하위·상위 네 값씩의 중앙값을 사용하는 관례에서 Q1=9, Q3=17임을 표시하고 도구의 계산 설정과 비교한다.',
        'limit': '중앙값 대조 경로에 한정된다. 손계산만으로 공학 도구 사용 목표를 대체하거나 모든 도구가 같은 사분위수를 산출한다고 주장하지 않는다.',
    }),
    ('9수04-09', 'internalRelations', {
        'from': '9수02-05', 'target': '9수04-09', 'kind': 'requires_for_task',
        'scope': '같은 관찰 대상에서 얻은 두 변수의 값을 순서쌍으로 옮겨 산점도를 그리는 경로',
        'rationale': '산점도의 한 점은 같은 대상의 두 관측값을 순서를 유지한 좌표로 표현한다. 축의 역할과 단위를 고정해야 점들의 경향을 원래 변수의 관계로 해석할 수 있다.',
        'conditions': ['두 값은 같은 관찰 대상에서 얻은 짝 자료이다.', '가로·세로축의 변수와 눈금 및 단위를 명시한다.'],
        'additionalLearning': '개별 점이 아닌 점 전체의 경향과 이상점을 살피고, 상관을 인과와 구별한다.',
        'diagnostic': '수면시간 5시간과 피로도 8인 학생을 (5,8)에 표시한다. 각 열을 따로 정렬한 뒤 다시 짝지으면 원래 학생의 점이 유지되는가? 유지되지 않는 이유를 설명한다.',
        'limit': '짝 자료를 좌표로 표현하는 경로의 필요 조건이다. 좌표 이해만으로 상관 해석이나 인과 추론이 완성되는 것은 아니다.',
    }),
    ('9수02-07', 'externalRelations', {
        'from': '9수02-07', 'target': '10공수2-03-04', 'kind': 'generalizes',
        'scope': '반비례 y=k/x의 역수항을 평행이동하여 유리함수의 그래프를 해석하는 경로',
        'rationale': 'c≠0일 때 (ax+b)/(cx+d)=a/c+(bc-ad)/(c²(x+d/c))로 정리할 수 있다. 역수항의 그래프를 가로 -d/c, 세로 a/c만큼 옮기는 관점으로 반비례의 두 갈래와 점근선을 해석한다.',
        'conditions': ['c≠0이며 원래 분모의 영점 x=-d/c를 정의역에서 제외한다.', 'ad-bc≠0인 비퇴화 경우를 먼저 다룬다. ad-bc=0이면 제외점이 있는 상수함수로 따로 해석한다.'],
        'additionalLearning': '문자식 변형, 함수의 평행이동과 정의역 및 점근선 해석을 추가한다.',
        'diagnostic': '(2x+1)/(x-1)=2+3/(x-1)에서 가로 이동량, 세로 이동량, 제외값을 각각 설명한다. 분자가 2x-2라면 왜 같은 두 갈래 그래프가 아닌가?',
        'limit': '반비례 부분에서 유리함수의 비퇴화 부분으로 확장한다. 정비례와 반비례 기준 전체를 고교 함수의 필수 선수 조건으로 취급하지 않는다.',
    }),
]


def main():
    path = ROOT / 'data/revisions_middle.json'
    revisions = json.loads(path.read_text(encoding='utf-8'))
    for code, field, link in ADDITIONS:
        links = revisions[code].setdefault(field, [])
        # The scope identifies this authored claim across reruns.
        old = next((i for i, value in enumerate(links) if value.get('scope') == link['scope']), None)
        if old is None:
            links.append(link)
        else:
            links[old] = link
    path.write_text(json.dumps(revisions, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Authored {len(ADDITIONS)} scoped connections')


if __name__ == '__main__':
    main()

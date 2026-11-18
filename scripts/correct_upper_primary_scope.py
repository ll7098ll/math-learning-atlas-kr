"""Preserve and correct two legacy paths that described a different quantity."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/revisions_elementary.json'
data=json.loads(path.read_text(encoding='utf-8'))
corrections={
    '6수03-11':(
        ['끈으로 도형의 바깥 경계를 한 바퀴 따라가 곧게 편 길이를 재고 둘레의 뜻을 설명한다.',
         '같은 단위로 나타낸 각 변을 한 번씩 더한다. 직사각형의 마주 보는 변을 묶으면 2×(6+4)=20cm이며 정사각형은 4×3=12cm이다.',
         '직사각형의 6×4로 내부를 덮는 단위 정사각형 수를 구하는 일과, 6+4+6+4로 바깥 경계 길이를 구하는 일을 비교하여 넓이와 둘레를 구별한다.'],
        '기존의 내부를 단위 정사각형으로 덮기와 넓이 재배치는 둘레 길이를 구하는 대안 경로가 아니므로 경계 길이 측정·합산으로 정정한다.'),
    '6수03-15':(
        ['여러 원의 한 바퀴 길이를 실로 재고 중심을 지나는 지름과 같은 단위로 기록한다. 실을 곧게 펼쳤을 때 지름 길이가 약 세 번 조금 넘게 들어감을 비교한다.',
         '각 원의 원주÷지름을 표로 나타내고 계산기로 비교한다. 측정 오차로 값이 조금 달라도 이상적인 원의 원주율이 일정하다는 수학적 관계와 구별한다.',
         '원주율의 근삿값을 3.14로 정해 지름 8cm인 원의 원주를 약 25.12cm로 구한다. 3.14를 정확한 원주율 전체로 취급하지 않는다.'],
        '기존 비례배분 경로는 전체를 나누는 다른 목표이며 원주율 측정의 대안이 아니므로 원주·지름의 측정과 같은 단위의 비 비교로 정정한다.'),
}
changed=[]
for code,(paths,reason) in corrections.items():
    record=data[code]
    if record['paths']==paths:continue
    record.setdefault('scopeCorrections',[]).append(dict(date='2026-10-30',reviewer='Codex',
        source_id='CURRICULUM_2022_33',pdf_pages=[35,36],reason=reason,previous_paths=record['paths']))
    record['paths']=paths
    changed.append(code)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(corrected=changed),ensure_ascii=True))

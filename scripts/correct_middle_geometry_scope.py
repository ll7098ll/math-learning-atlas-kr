"""Keep geometry instructions within the source's proof-vocabulary boundary."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
path=root/'data/revisions_middle.json'
data=json.loads(path.read_text(encoding='utf-8'))
changes={
    '9수03-02':('동위각·엇각의 성질과 그 역을 사용할 때 가정과 결론을 바꾸어 적는다.',
               '동위각·엇각의 성질과 그 역을 사용할 때 처음 주어진 정보와 판단할 내용을 구별하여 적는다.'),
    '9수03-09':('같은 두 변 또는 같은 두 밑각 중 무엇이 주어진 가정인지 명시한다.',
               '같은 두 변 또는 같은 두 밑각 중 무엇이 처음 주어진 조건인지 명시한다.')}
changed=[]
for code,(before,after) in changes.items():
    record=data[code]
    if before in record['conditions']:
        record.setdefault('scopeCorrections',[]).append(dict(date='2026-10-30',reviewer='Codex',source_id='CURRICULUM_2022_33',pdf_pages=[45,46],
            reason='도형의 증명에서 가정·결론 용어를 다루지 않는 적용 사항에 맞춰 수행 지시의 표현을 바꾼다. 주어진 정보와 판단의 방향 구별은 보존한다.',previous_conditions=list(record['conditions'])))
        record['conditions']=[after if text==before else text for text in record['conditions']]
        changed.append(code)
    else:assert after in record['conditions']
if changed:path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(corrected=changed),ensure_ascii=False))

"""Keep quadratic practice within the curriculum's real-root cases."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/revisions_middle.json'
data=json.loads(path.read_text(encoding='utf-8'))
record=data['9수02-20']
before='다른 과제 x²=8은 ±2√2이며 x²+1=0은 실수 해가 없다.'
after='보충 과제 x²=8의 해는 ±2√2이며 (x−2)²=0의 중근은 2다. 실수해가 없는 이차방정식의 풀이 과제는 이 범위에 포함하지 않는다.'
changed=before in record['taskSolution']
if changed:
    record.setdefault('scopeCorrections',[]).append(dict(date='2026-10-30',reviewer='Codex',source_id='CURRICULUM_2022_33',pdf_pages=[42,43],
        reason='교육과정은 이차방정식의 해가 실수인 경우만 다루므로, 실수해가 없는 보충 풀이 과제를 중근 예제로 교체한다.',previous_task_solution=record['taskSolution']))
    record['taskSolution']=record['taskSolution'].replace(before,after)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
else:assert after in record['taskSolution']
print(json.dumps(dict(corrected=changed)))

"""Apply the dated content corrections and retain prior author records."""
import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-11-04'
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def edit(rel,old,new):
 p=ROOT/rel;t=p.read_text(encoding='utf-8')
 if old in t:p.write_text(t.replace(old,new),encoding='utf-8')

def alternative_record(case):
 route=case['routes'][0]
 return dict(kind='selected_explanatory_route',goal_ids=case['goal_ids'],
  selected_route=route['id'],performance=case['task'],
  decision='이 과제에서 제시한 풀이를 설명 경로로 유지한다. 표·그림·도구로 같은 단계를 확인하는 것은 표현 보조이며 별도 선수 경로로 합치지 않는다.',
  reason='이 경로는 '+ ' / '.join(route['conditions'])+'를 사용해 '+route['result']+'라는 수행을 확인한다.',
  verification_question=route['diagnostic']['question'],expected=route['diagnostic']['expected'],
  status='authored_route_scope_not_exhaustive_alternatives',reviewer='Codex',date=DATE)

def main():
 old='450°=5π/2,−90°=−π/2이며 모두 90°와 같은 동경이지만 회전량은 다르다.'
 new='450°=5π/2는 90°와 같은 동경이고, −90°=−π/2는 270°와 같은 동경이다. −90°와 90°의 동경은 서로 반대다. 같은 동경인 각도 회전량은 한 바퀴의 정수배만큼 다를 수 있다.'
 edit('scripts/author_algebra_calculus_one.py',old,new)
 prob_old='교집합이 공집합인 배반 사건에서만 빼는 항이 0이다.'
 prob_new='배반 사건이면 교집합 확률이 0이므로 빼는 항이 0이다. 역은 일반적으로 성립하지 않는다. 연속 균등 모형에서 한 점의 확률은 0이어도 그 점으로 된 집합은 공집합이 아니다.'
 edit('scripts/author_probability_statistics.py',prob_old,prob_new)
 source=json.loads((ROOT/'data/content_gap_findings_2026-11-04.json').read_text(encoding='utf-8'))
 for p in sorted((ROOT/'data').glob('goal_hierarchy_*.json')):
  d=json.loads(p.read_text(encoding='utf-8'));changed=False
  for c in d['cases']:
   prior=copy.deepcopy(c)
   for route in c['routes']:
    route['steps']=[s.replace(old,new).replace(prob_old,prob_new) for s in route['steps']]
   if len(c['routes'])==1:
    c['alternative_decision']=alternative_record(c)
    c['alternative_review']=c['alternative_decision']['reason']+' '+c['alternative_decision']['decision']
   if c['standard']=='12확통02-06':
    c['alternative_decision']['auxiliary_check']='C(3,2)/C(5,2)=3/10은 결과의 조합 검산이다. 곱셈정리를 설명하는 수행에는 조건부확률 경로를 유지한다. 계산 목표에는 조합법도 가능하나 이 과제의 정리 설명 경로와 구별한다.'
    c['alternative_review']+=' '+c['alternative_decision']['auxiliary_check']
   if c!=prior:
    c.setdefault('history',[]).append(dict(date=DATE,reviewer='Codex',kind='content_correction',scope='추가 감사의 문구 오류와 설명 경로 범위 보완',previous_record={k:v for k,v in prior.items() if k!='history'}));changed=True
  if changed:dump(p,d)
 p=ROOT/'data/revisions_elementary.json';d=json.loads(p.read_text(encoding='utf-8'))
 for code in ['2수03-07','2수03-08','2수03-09']:
  e=d[code];previous=copy.deepcopy(e)
  e['representations']=[s.replace('복합 단위→분과 초：60 관계를 유지한다.','시간↔분：1시간과 60분이 같은 기간임을 시계 움직임으로 연결한다.') for s in e['representations']]
  if code=='2수03-09':
   e['paths']=['달력에서 같은 요일로 한 주씩 두 번 이동하고 시작일에서 지난 날을 14번 센 결과와 비교한다.','14일을 7일과 7일로 묶어 경과 시간선에 표시한다. 월 경계를 넘으면 실제 달의 마지막 날짜를 확인한다.']
   e['representations']=['달력의 같은 요일 두 칸 이동↔7일+7일↔14일을 대응시킨다.','실제 달력의 월별 마지막 날짜↔28·29·30·31일을 비교한다.','1년↔12개월은 고정 관계지만 1개월↔일수는 달에 따라 달라짐을 구별한다.']
  if previous!=e:e.setdefault('revision_history',[]).append(dict(date=DATE,reason='1~2학년 시간 범위와 대표 과제에 맞춘 표현·경로 수정',previous_record=previous))
 dump(p,d)
 edit('scripts/analysis_content.py','복합 단위→분과 초|60 관계를 유지한다.','시간↔분|1시간과 60분의 관계를 유지한다. 초 단위는 3~4학년에서 별도로 다룬다.')
 # Every legacy semantic edge gets an explicit bridge prompt, using its own
 # authored reason. This is a new diagnostic design, never review evidence.
 p=ROOT/'data/relations.json';d=json.loads(p.read_text(encoding='utf-8'))
 for e in d['relations']:
  if not(e['from'].startswith('standard:') and e['to'].startswith('standard:')):continue
  a,b=e['from'][9:],e['to'][9:]
  if not e.get('diagnostic'):
   e['diagnostic']=f'{a}와 {b}의 수행에서 다음 연결 이유가 적용되는 예를 하나 설명하고, 조건을 바꾸면 적용되지 않는 경우도 설명하라: '+e['rationale']
   e['expected_response']='두 수행에서 보존·변경되는 대상과 표현을 구별하고, 다음 이유를 주어진 적용 범위에서 설명한다: '+e['rationale']+' 적용 조건: '+str(e.get('conditions',[]))
   e['diagnostic_status']='authored_bridge_prompt_not_student_validated'
   e['diagnostic_scope']='의미 연결의 설명과 적용 한계 확인. 필수 선수성 판정이 아님.'
   e.setdefault('revision_history',[]).append(dict(date=DATE,kind='diagnostic_design',reviewer='Codex',scope='기존 연결 이유와 조건을 확인하는 질문·기대 설명 추가'))
 dump(p,d)
 print('Content corrections and scoped route/relationship records applied')
if __name__=='__main__':main()

"""Check authored coverage, mathematical examples' structure and provenance.

This catches omissions; mathematical and pedagogical judgments remain explicit
author review records, never inferred from field lengths or line counts.
"""
import json,re,sys
from collections import Counter
from pathlib import Path
from detailed_revision import load_revisions,PILOTS,IDS
R=Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding='utf-8')
standards=json.loads((R/'data/standards.json').read_text(encoding='utf-8'))['standards']
by={s['code']:s for s in standards};entries=load_revisions();issues=[];counts=Counter()
for code,s in by.items():
 if code in PILOTS:continue
 e=entries.get(code)
 if not e or not e.get('taskSolution') or e.get('review',{}).get('contentRevision')=='pending':
  issues.append({'code':code,'issue':'개별 원고 미완성'});continue
 counts[s['school_level']]+=1
 for k in ['mathematicalMeaning','taskSolution','conditions','paths','thinking','representations','diagnostics','feedback']:
  if not e.get(k):issues.append({'code':code,'issue':'빈 항목 '+k})
 for i,t in enumerate(e['thinking']):
  for k in ['label','meaning','reason','observable']:
   if not t.get(k):issues.append({'code':code,'issue':f'사고 {i+1}의 {k} 누락'})
   if '라는 행동을 통해' in t.get('reason','') or '이라는 판단을 확인한다. 정답만으로' in t.get('reason',''):issues.append({'code':code,'issue':f'사고 {i+1}의 이유가 관찰 문장의 반복'})
  if '대표과제의 수·기호·대상을 직접 표시' in t.get('observable',''):issues.append({'code':code,'issue':f'사고 {i+1}의 관찰 수행이 공통 문구'})
 for i,p in enumerate(e['diagnostics']):
  for k in ['question','expected','interpretation','followup']:
   if not p.get(k):issues.append({'code':code,'issue':f'진단 {i+1}의 {k} 누락'})
 for link in e.get('internalRelations',[])+e.get('externalRelations',[]):
  for c in [link.get('from',code),link['target']]:
   if c not in by:issues.append({'code':code,'issue':'없는 관계 대상 '+str(c)})
  if not link.get('rationale') or not link.get('conditions') or not link.get('diagnostic'):issues.append({'code':code,'issue':'관계 이유·조건·확인 질문 누락'})
 if e.get('review',{}).get('independentReview') or e.get('review',{}).get('studentValidated'):issues.append({'code':code,'issue':'근거 없는 검증 상태 승격'})
result={'status':'pass' if not issues else 'incomplete','authored_by_level':dict(counts),'initial_cases':3,'issues':issues,'interpretation':'필수 내용과 참조의 검사다. 필드 존재를 수학적 정확성이나 수업 효과의 검증으로 취급하지 않는다.'}
(R/'data/revision_quality.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({**result,'issues':issues[:12]},ensure_ascii=False))
sys.exit(bool(issues))

"""Separate an impossible first draw from a defined conditional probability."""
import copy,json
from relation_analysis_review import ROOT,digest,load_reviews
from literature_review import load_registry

CODE='12확통02-06'
OLD_CONDITION='총 N개 중 빨강 R개인 비복원 추출이며 N≥2다.'
CONDITION='N≥2, 0≤R≤N인 정수 개수의 비복원 추출이다. R≥1일 때만 첫 빨강 사건의 조건부확률을 사용한다. R=0이면 첫 빨강 사건이 불가능하므로 두 번 빨강 확률을 직접 0으로 정한다.'
MEANING='교집합 확률은 조건 사건의 확률이 양수일 때 조건부확률의 곱으로 계산한다. 조건 사건이 불가능하면 그 조건부확률을 정의하지 않고 교집합 확률을 직접 0으로 판단한다.'
SOLUTION='N≥2, 0≤R≤N인 정수 개수를 가정한다. R=0이면 첫 빨강 사건의 확률이 0이므로 그 사건을 조건으로 한 조건부확률을 정의하지 않는다. 두 번 빨강도 불가능해 확률은 직접 0이다. R≥1이면 첫 빨강 확률은 R/N>0이다. 그 조건에서 총 N−1개 중 빨강 R−1개가 남아 둘째 빨강의 조건부확률은 (R−1)/(N−1)이다. 따라서 두 번 빨강 확률은 R(R−1)/[N(N−1)]이다. R=1이면 이 값도 0이고, R=N이면 1이다. 이 최종 식은 R=0에서도 0이지만 정의되지 않는 조건부확률에 0을 곱해 유도한 것은 아니다. 해설 예 N=5,R=3에서는 3/5·2/4=3/10이다.'

def main():
 reviews=load_reviews();literature=load_registry();p=ROOT/'data/revisions_high.json';q=ROOT/'data/secondary_analysis_details.json'
 data=json.loads(p.read_text(encoding='utf-8'));secondary=json.loads(q.read_text(encoding='utf-8'));r=data[CODE]
 evidence=ROOT/'data/zero_probability_condition_correction.json'
 if r['conditions']==[CONDITION]:
  assert r['taskSolution']==SOLUTION and evidence.exists();print('Zero-condition correction remains current');return
 assert r['conditions']==[OLD_CONDITION]
 assert not any('standard:'+CODE in [v['from'],v['to']] for v in reviews['records'].values())
 assert not any('revision:'+CODE in c['target_snapshots'] for c in literature['claims'])
 before=copy.deepcopy(r);entry=next(e for e in secondary['analyses'] if e['code']==CODE);previous_entry=copy.deepcopy(entry)
 assert r['paths']==[r['taskSolution']]
 r.update(mathematicalMeaning=MEANING,taskSolution=SOLUTION,conditions=[CONDITION],paths=[SOLUTION])
 r['thinking'][1]['observable']='R≥1에서 첫 빨강 조건 뒤 총 N−1개·빨강 R−1개를 센다. R=0이면 조건부확률을 정의하지 않는다.'
 r['thinking'][1]['reason']='조건 사건의 확률이 양수인지 먼저 확인하고 분자·분모를 갱신한다.'
 r['thinking'][2]['meaning']='P(A)>0에서 P(A)P(B∣A)로 교집합을 구하고 P(A)=0이면 직접 0으로 판단한다.'
 r['diagnostics'][1]['expected']='조건 사건이 양수이면 일반 조건부 곱셈식이며 독립을 요구하지 않는다.'
 r['diagnostics'].append(dict(question='빨강이 0개여도 첫 빨강 뒤 조건부확률 (R−1)/(N−1)을 쓰는가?',expected='아니다. 첫 사건이 불가능해 조건부확률은 정의하지 않고 두 번 빨강 확률을 직접 0으로 정한다.',interpretation='교집합의 확률 0과 조건부확률의 정의 불가를 구별하는지 확인한다.',followup='R=0,1,N을 나누어 원소 결과를 설명한다.'))
 entry['idea']=MEANING;entry['steps'][-1][1]=r['thinking'][2]['meaning'];entry['probes'][1][1]=r['diagnostics'][1]['expected']
 permitted=copy.deepcopy(before)
 for key in ['mathematicalMeaning','taskSolution','conditions','paths','thinking','diagnostics']:permitted[key]=copy.deepcopy(r[key])
 assert permitted==r
 permitted=copy.deepcopy(previous_entry)
 for key in ['idea','steps','probes']:permitted[key]=copy.deepcopy(entry[key])
 assert permitted==entry
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');q.write_text(json.dumps(secondary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 evidence.write_text(json.dumps(dict(date='2026-11-05',standard_code=CODE,reason='일반화된 비복원 추출 풀이가 R=0을 제외하지 않고 확률 0인 첫 빨강 사건의 조건부확률을 사용했다. R=0은 불가능한 교집합으로 직접 처리하고 양수 조건에서만 곱셈식을 유도하도록 원고와 중복 설명을 보완했다. 목표·과제 원장의 실제 사례는 빨강3·파랑2와 첫 사건 양수 조건이 이미 있어 변경하지 않았다.',previous_revision=before,current_revision=r,previous_secondary_entry=previous_entry,current_secondary_entry=entry,previous_revision_snapshot=digest(before),current_revision_snapshot=digest(r),independent_review=False,student_validated=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 load_reviews();load_registry();print('Corrected zero-probability condition; earlier review bindings remain current')

if __name__=='__main__':main()

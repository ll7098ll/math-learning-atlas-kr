"""Explicitly reconcile the projection revision with its 0/90 degree cases."""
import copy,json
from relation_analysis_review import ROOT,digest,load_reviews
from literature_review import load_registry
CODE='12기하02-03'
OLD='선과 평면의 예각 θ,두 평면의 예각 φ를 각각 사용한다.'
NEW='선분의 지지 직선과 평면 사이의 각 θ, 두 평면 사이의 각 φ는 각각 0°≤θ≤90°, 0°≤φ≤90°인 작은 각으로 정한다. 0°의 크기 유지와 90°의 퇴화도 포함한다.'
REASON='대표 풀이와 목표별 과제는 평행한 경우0°와 수직인 경우90°를 포함하지만 상세 원고의 조건은 예각으로 한정하여 모순되었다. 직선-평면각과 두 평면의 작은 각을 각각 닫힌 범위[0°,90°]로 명시했다. 길이 Lcosθ·넓이 Scosφ는 이 범위에서 음이 아니며0°에서는 유지,90°에서는 해당 길이·넓이가0이 된다. 목표·과제 원장과 풀이·관찰 활동은 변경하지 않았다.'

def main():
 load_reviews();literature=load_registry();p=ROOT/'data/revisions_high.json';data=json.loads(p.read_text(encoding='utf-8'));r=data[CODE]
 record=ROOT/'data/projection_angle_scope_correction.json'
 if r['conditions']==[NEW]:
  assert r['mathematicalMeaning'].endswith(NEW) and record.exists()
  print('Projection boundary correction remains current');return
 assert r['conditions']==[OLD] and r['mathematicalMeaning'].endswith(OLD)
 assert not any('revision:'+CODE in c['target_snapshots'] for c in literature['claims'])
 before=copy.deepcopy(r);r['conditions']=[NEW];r['mathematicalMeaning']=r['mathematicalMeaning'][:-len(OLD)]+NEW
 permitted=copy.deepcopy(before);permitted.update(conditions=[NEW],mathematicalMeaning=r['mathematicalMeaning']);assert permitted==r
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 record.write_text(json.dumps(dict(date='2026-11-05',standard_code=CODE,reason=REASON,previous_fields={k:before[k] for k in ['conditions','mathematicalMeaning']},current_fields={k:r[k] for k in ['conditions','mathematicalMeaning']},previous_revision_snapshot=digest(before),current_revision_snapshot=digest(r),independent_review=False,student_validated=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 load_reviews();load_registry();print('Corrected projection angle scope; existing reviews remain current')
if __name__=='__main__':main()

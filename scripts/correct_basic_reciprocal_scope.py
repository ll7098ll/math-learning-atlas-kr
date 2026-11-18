"""Keep the basic reciprocal course within y=k/x and preserve re-review history."""
import copy,json
from relation_analysis_review import ROOT,FILE,load_reviews,materials,source_value,digest
from literature_review import load_registry

CODE='10기수2-03-04'
RID='SEC_10기수2-03-04_C04'
OLD_MEANING='나눗셈 구조와 반비례의 이동이 정의역과 점근선을 드러낸다. 기본형 y=2/x로 제한하며 x=0의 나눗셈은 정의되지 않는다.'
NEW_MEANING='기본형 반비례의 곱 일정과 분모 제한으로 정의역·치역과 그래프의 위치를 설명한다. 기본형 y=2/x로 제한하며 x=0의 나눗셈은 정의되지 않는다.'
OLD_PRIOR='반비례에 이동과 상수항을 추가한다.'
NEW_PRIOR='중학교 반비례와 y=k/x 기본형의 곱 일정·분모 제한·그래프를 비교한다. 평행이동과 상수항은 이 기본수학 기준에 추가하지 않는다.'
REASON='공식 기준은 y=k/x 기본형이다. 대표 수행 y=2/x는 x≠0,y≠0,xy=2이며 이동이 없다. 공통수학의 y=2+3/(x−1)은 별도 범위로 유지한다. 양쪽 공식 문장·대표 의미·풀이·조건과 기존 검토의 진단·기대 설명·수학 근거를 다시 읽었다. 기본수학의 의미 첫 문장과 중복 prior 이유만 고쳤고 계산·목표·과제·자료는 유지했다.'

def finish_secondary_copies(secondary,path,evidence_path):
 entry=next(v for v in secondary['analyses'] if v['code']==CODE)
 old=dict(title='일차식 비의 유리함수',idea='나눗셈 구조와 반비례의 이동이 정의역과 점근선을 드러낸다.')
 new=dict(title='기본형 유리함수',idea=NEW_MEANING.split('. ')[0]+'.')
 evidence=json.loads(evidence_path.read_text(encoding='utf-8'))
 if all(entry[k]==v for k,v in new.items()):
  assert 'secondary_copy_followup' in evidence;return
 assert all(entry[k]==v for k,v in old.items())
 before=copy.deepcopy(entry);entry.update(new)
 allowed=copy.deepcopy(before);allowed.update(new);assert allowed==entry
 path.write_text(json.dumps(secondary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 evidence['secondary_copy_followup']=dict(date='2026-11-05',reason='중복 원고의 제목·idea도 다시 읽고 기본형으로 맞췄다. 풀이·조건·발문·목표·과제와 공통수학 원고는 유지했다.',previous=old,current=new,previous_entry_digest=digest(before),current_entry_digest=digest(entry),source_bindings_unchanged=True)
 evidence['changed_sources']+=['data/secondary_analysis_details.json:'+CODE+'/'+k for k in new]
 evidence_path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
 registry=load_reviews();literature=load_registry()
 p=ROOT/'data/revisions_high.json';q=ROOT/'data/secondary_analysis_details.json'
 revisions=json.loads(p.read_text(encoding='utf-8'));secondary=json.loads(q.read_text(encoding='utf-8'))
 revision=revisions[CODE];entry=next(v for v in secondary['analyses'] if v['code']==CODE)
 evidence=ROOT/'data/basic_reciprocal_scope_correction.json'
 assert entry['prior'][0][0]=='9수02-07'
 if revision['mathematicalMeaning']==NEW_MEANING and entry['prior'][0][1]==NEW_PRIOR:
  assert evidence.exists();finish_secondary_copies(secondary,q,evidence);load_reviews();load_registry();print('Basic reciprocal scope and duplicated title/idea remain current');return
 assert revision['mathematicalMeaning']==OLD_MEANING and entry['prior'][0][1]==OLD_PRIOR
 affected={rid for rid,r in registry['records'].items() if 'standard:'+CODE in (r['from'],r['to'])}
 assert affected=={RID},affected
 assert not any('revision:'+CODE in claim['target_snapshots'] for claim in literature['claims'])
 data=materials();before=source_value(RID,data=data);review=registry['records'][RID]
 assert digest(before)==review['source_snapshot']
 previous_revision=copy.deepcopy(revision);previous_entry=copy.deepcopy(entry)
 revision['mathematicalMeaning']=NEW_MEANING;entry['prior'][0][1]=NEW_PRIOR
 allowed=copy.deepcopy(previous_revision);allowed['mathematicalMeaning']=NEW_MEANING;assert allowed==revision
 allowed=copy.deepcopy(previous_entry);allowed['prior'][0][1]=NEW_PRIOR;assert allowed==entry
 # Mathematical witnesses for the retained basic and additional common-course models.
 for x in [-4,-2,-1,1,2,4]:
  from fractions import Fraction as F
  y=F(2,x);assert x*y==2 and y!=0
 assert F(2,2)==1 and F(2*2+1,2-1)==5
 assert F(2*0+1,0-1)==2+F(3,0-1)==-1
 p.write_text(json.dumps(revisions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 q.write_text(json.dumps(secondary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 after=source_value(RID)
 allowed=copy.deepcopy(before);allowed['endpoints'][CODE]['revision']['value']['mathematicalMeaning']=NEW_MEANING
 assert allowed==after,'Only the explicitly re-read meaning may change in this source binding'
 previous_review=copy.deepcopy(review);previous_review.pop('history',None)
 review.setdefault('history',[]).append(dict(date='2026-11-05',reviewer='Codex',reason=REASON,previous_review=previous_review,source_change=dict(path='endpoints/'+CODE+'/revision/value/mathematicalMeaning',previous=OLD_MEANING,current=NEW_MEANING)))
 review['source_snapshot']=digest(after)
 (ROOT/FILE).write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 evidence.write_text(json.dumps(dict(date='2026-11-05',code=CODE,relation_id=RID,reason=REASON,original_meaning=OLD_MEANING,corrected_meaning=NEW_MEANING,original_prior=OLD_PRIOR,corrected_prior=NEW_PRIOR,changed_sources=['data/revisions_high.json:'+CODE+'/mathematicalMeaning','data/secondary_analysis_details.json:'+CODE+'/prior/0/1'],previous_source_snapshot=digest(before),current_source_snapshot=digest(after),re_reviewed_relations=[RID],independent_review=False,student_validated=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 finish_secondary_copies(secondary,q,evidence)
 load_reviews();load_registry()
 print('Basic reciprocal meaning and duplicated prior corrected; one existing binding explicitly re-reviewed')

if __name__=='__main__':main()

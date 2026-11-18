"""Correct both authored copies and explicitly re-review the one affected binding."""
import copy,json
from relation_analysis_review import ROOT,FILE,digest,materials,source_value,load_reviews
from literature_review import load_registry

CODE='10공수2-01-06'
RID='SEC_10공수2-01-06_C04'
OLD='중심이 옮겨진 이차곡선 해석에 사용한다.'
REASON='포물선에는 중심대칭의 중심이 없다. 고정된 좌표축에서 꼭짓점·초점·준선을 함께 평행이동한다고 고친다. x²=4y를 오른쪽 2, 위로 1 옮기면 (x−2)²=4(y−1), 꼭짓점 (2,1), 초점 (2,2), 준선 y=0이다. (4,2)는 곡선 위에 있지만 꼭짓점에 대한 대칭점 (0,0)은 곡선 위에 없다. 위로 무한히 뻗고 아래로 유계인 포물선은 다른 점에 대해서도 중심대칭일 수 없다. 기존 수행·풀이·조건·진단은 유지하고 두 원본의 연결 이유만 수정한 뒤 영향을 받는 한 검토를 다시 대조했다.'

def main():
 registry=load_reviews();literature=load_registry();review=registry['records'][RID];new=review['rationale']
 p=ROOT/'data/revisions_high.json';q=ROOT/'data/secondary_analysis_details.json'
 revisions=json.loads(p.read_text(encoding='utf-8'));secondary=json.loads(q.read_text(encoding='utf-8'))
 revision=revisions[CODE];link=revision['internalRelations'][0]
 entry=next(e for e in secondary['analyses'] if e['code']==CODE)
 evidence=ROOT/'data/parabola_translation_source_correction.json'
 assert link['target']==entry['onward'][0][0]=='12기하01-01'
 if link['rationale']==entry['onward'][0][1]==new:
  assert evidence.exists();print('Parabola source correction remains current');return
 assert link['rationale']==entry['onward'][0][1]==OLD
 data=materials();affected={rid for rid,r in registry['records'].items() if 'standard:'+CODE in (r['from'],r['to'])}
 assert affected=={RID},affected
 assert not any('revision:'+CODE in c['target_snapshots'] for c in literature['claims'])
 before=source_value(RID,data=data);assert digest(before)==review['source_snapshot']
 previous_revision=copy.deepcopy(revision);previous_entry=copy.deepcopy(entry)
 link['rationale']=new;entry['onward'][0][1]=new
 permitted=copy.deepcopy(previous_revision);permitted['internalRelations'][0]['rationale']=new;assert permitted==revision
 permitted=copy.deepcopy(previous_entry);permitted['onward'][0][1]=new;assert permitted==entry
 p.write_text(json.dumps(revisions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 q.write_text(json.dumps(secondary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 after=source_value(RID)
 permitted=copy.deepcopy(before);permitted['endpoints'][CODE]['revision']['value']['internalRelations'][0]['rationale']=new
 assert permitted==after,'Only the re-read authored rationale may change'
 previous=copy.deepcopy(review);previous.pop('history',None)
 review.setdefault('history',[]).append(dict(date='2026-11-05',reviewer='Codex',reason=REASON,previous_review=previous,source_change=dict(path='endpoints/'+CODE+'/revision/value/internalRelations/0/rationale',previous=OLD,current=new)))
 review['source_snapshot']=digest(after)
 (ROOT/FILE).write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 evidence.write_text(json.dumps(dict(date='2026-11-05',relation_id=RID,reason=REASON,original_rationale=OLD,corrected_rationale=new,changed_sources=['data/revisions_high.json:'+CODE+'/internalRelations/0/rationale','data/secondary_analysis_details.json:'+CODE+'/onward/0/1'],previous_source_snapshot=digest(before),current_source_snapshot=digest(after),re_reviewed_relations=[RID],independent_review=False,student_validated=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 load_reviews();load_registry();print('Corrected two authored sources; explicitly re-reviewed one binding')

if __name__=='__main__':main()

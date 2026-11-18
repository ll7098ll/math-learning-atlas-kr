"""Correct a strategy necessity claim and explicitly re-review affected bindings."""
import copy,json
from relation_analysis_review import ROOT,FILE,digest,materials,source_value,load_reviews
from literature_review import load_registry

CODE='12미적Ⅰ-03-02'
RID='SEC_12미적Ⅰ-03-02_C04'
OLD='곱 구조에는 부분적분이라는 별도 전략이 필요하다.'
IDS={'SEC_12미적Ⅰ-03-02_C03','SEC_12미적Ⅱ-03-01_C03',RID}
REASON='곱꼴이라는 사실만으로 부분적분이 필요한 것은 아니다. ∫x(x+1)dx는 전개하여 x³/3+x²/2+C로 계산할 수 있다. 부분적분은 곱미분의 역관계를 이용하는 선택 전략으로 고쳤다. 두 원본의 연결 이유 한 곳씩만 수정하고 양의 정수 거듭제곱 역미분·함수 종류 확장·전략 선택의 세 검토를 다시 대조했다. 각 풀이·조건·진단과 수학적 근거는 변하지 않았다.'

def main():
 registry=load_reviews();literature=load_registry();new=registry['records'][RID]['rationale']
 p=ROOT/'data/revisions_high.json';q=ROOT/'data/secondary_analysis_details.json'
 revisions=json.loads(p.read_text(encoding='utf-8'));secondary=json.loads(q.read_text(encoding='utf-8'))
 revision=revisions[CODE];link=revision['internalRelations'][1]
 entry=next(e for e in secondary['analyses'] if e['code']==CODE)
 evidence=ROOT/'data/integration_product_strategy_source_correction.json'
 assert link['target']==entry['onward'][0][0]=='12미적Ⅱ-03-03'
 if link['rationale']==entry['onward'][0][1]==new:
  assert evidence.exists();print('Integration strategy source correction remains current');return
 assert link['rationale']==entry['onward'][0][1]==OLD
 data=materials();affected={rid for rid,r in registry['records'].items() if 'standard:'+CODE in (r['from'],r['to'])}
 assert affected==IDS,affected
 assert not any('revision:'+CODE in c['target_snapshots'] for c in literature['claims'])
 before={rid:source_value(rid,data=data) for rid in IDS}
 assert all(digest(before[rid])==registry['records'][rid]['source_snapshot'] for rid in IDS)
 previous_revision=copy.deepcopy(revision);previous_entry=copy.deepcopy(entry)
 link['rationale']=new;entry['onward'][0][1]=new
 permitted=copy.deepcopy(previous_revision);permitted['internalRelations'][1]['rationale']=new;assert permitted==revision
 permitted=copy.deepcopy(previous_entry);permitted['onward'][0][1]=new;assert permitted==entry
 p.write_text(json.dumps(revisions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 q.write_text(json.dumps(secondary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 data=materials();changes=[]
 for rid in sorted(IDS):
  after=source_value(rid,data=data)
  permitted=copy.deepcopy(before[rid]);permitted['endpoints'][CODE]['revision']['value']['internalRelations'][1]['rationale']=new
  assert permitted==after,'Only the explicitly re-read rationale may change'
  review=registry['records'][rid];previous=copy.deepcopy(review);previous.pop('history',None)
  review.setdefault('history',[]).append(dict(date='2026-11-05',reviewer='Codex',reason=REASON,previous_review=previous,source_change=dict(path='endpoints/'+CODE+'/revision/value/internalRelations/1/rationale',previous=OLD,current=new)))
  review['source_snapshot']=digest(after)
  changes.append(dict(relation_id=rid,previous_source_snapshot=digest(before[rid]),current_source_snapshot=digest(after),unchanged_math_check=review['mathematical_check']))
 (ROOT/FILE).write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 evidence.write_text(json.dumps(dict(date='2026-11-05',relation_id=RID,reason=REASON,original_rationale=OLD,corrected_rationale=new,changed_sources=['data/revisions_high.json:'+CODE+'/internalRelations/1/rationale','data/secondary_analysis_details.json:'+CODE+'/onward/0/1'],re_reviewed_relations=changes,independent_review=False,student_validated=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 load_reviews();load_registry();print('Corrected two strategy source copies; explicitly re-reviewed three bindings')

if __name__=='__main__':main()

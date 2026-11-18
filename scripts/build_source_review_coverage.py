"""Separate full-scope image review from legacy statement-only corrections."""
from pathlib import Path
from collections import Counter
import hashlib,json
from mapping_review_author import changed_targets
R=Path(__file__).resolve().parents[1]
def build():
 load=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
 inventory=load('data/standards.json');ledger=load('data/curriculum_standard_image_reviews.json')
 assert ledger['source_sha256']==inventory['source_sha256']==hashlib.sha256((R/inventory['source_file']).read_bytes()).hexdigest()
 entries={};cases={}
 for p in (R/'data').glob('goal_hierarchy_*.json'):
  d=json.loads(p.read_text(encoding='utf-8'));entries.update({v['code']:v for v in d['entries']});cases.update({v['id']:v for v in d['cases']})
 reviews={v['code']:v for v in ledger['reviews']};records=[]
 for s in inventory['standards']:
  code=s['code'];review=reviews.get(code);changes=[]
  if review:
   changes=changed_targets(review,entries,cases)
   for v in review['evidence']:
    p=R/v['file']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=v['sha256']:changes.append('image:'+v['file'])
   state='needs_re_review' if changes else 'self_checked_source_image'
  else:state='statement_image_only_requires_full_scope_review' if s['source_review_status']!='미대조' else 'unreviewed'
  records.append(dict(code=code,state=state,required_scope=['원문 문장과 수식','성취기준 해설의 제한 조건','적용 시 고려 사항','목표·과제·보완 활동의 반영 위치'],
   pdf_pages=entries[code]['source_review']['pdf_pages'],legacy_source_status=s['source_review_status'],
   evidence=dict(file='data/curriculum_standard_image_reviews.json',code=code) if review else None,changed_since_review=changes))
 counts=dict(Counter(r['state'] for r in records));complete=counts.get('self_checked_source_image',0)
 summary=dict(total=len(records),full_scope_reviewed=complete,statement_only=counts.get('statement_image_only_requires_full_scope_review',0),
  no_image_review=counts.get('unreviewed',0),needs_re_review=counts.get('needs_re_review',0),full_scope_pending=len(records)-complete)
 qp=R/'data/content_review_queue.json';queue=load('data/content_review_queue.json')
 queue['full_scope_source_review']=records;queue['source_review_scope_summary']=summary
 qp.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 lines=['# 原文 이미지 대조 범위와 남은 검토'.replace('原文','원문'),'','이미지 대조 이력과 문장·해설·고려 사항의 전 범위 대조를 구별한다. 이전 문장 보정 이력을 해설 검토 완료로 올려 세지 않는다.','','| 구분 | 기준 수 |','|---|---:|',f'| 문장·해설·고려 사항과 반영 위치 자체 대조 | {complete} |',f"| 기존 문장·수식 이미지 대조만 확인, 전 범위 추가 확인 필요 | {summary['statement_only']} |",f"| 이미지 대조 이력 없음 | {summary['no_image_review']} |",f"| 변경 후 재대조 필요 | {summary['needs_re_review']} |",f"| 전 범위 대조 대기 합계 | {summary['full_scope_pending']} |",'',
  '기존 문장 보정은 [보정 원장](../data/source_corrections.json)의 방법과 범위를 따른다. 전 범위 대조는 [이미지 검토 원장](../data/curriculum_standard_image_reviews.json)의 코드별 실제 근거를 따른다. 전체435개와 필요한 쪽수는 [검토 대장](../data/content_review_queue.json)에 빠짐없이 기록한다. 외부 독립 검토와 학생 반응 검증은 별도다.','']
 (R/'docs/원문이미지대조범위.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False));return records,summary
if __name__=='__main__':build()

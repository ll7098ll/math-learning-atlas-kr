"""Persist decisions made after visual source review; never infer a review."""
from pathlib import Path
import hashlib,json
from mapping_review_author import digest,entry_digest,resource_file,changed_targets
R=Path(__file__).resolve().parents[1]

def record_reviews(subject,prefix,corpus,notes,image_prefix,report_name,reviewed_changes=None):
 data=json.loads((R/corpus).read_text(encoding='utf-8'))
 entries={v['code']:v for v in data['entries']};cases={v['id']:v for v in data['cases']}
 assert {prefix+n for n in notes}=={code for code in entries if code.startswith(prefix)}
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 pdf_sha=sha(R/'[별책8] 수학과 교육과정.pdf');out=R/'data/curriculum_standard_image_reviews.json'
 ledger=json.loads(out.read_text(encoding='utf-8'));assert ledger['source_sha256']==pdf_sha
 prior={v['code']:v for v in ledger['reviews']};reviews=[]
 for suffix,note in notes.items():
  code=prefix+suffix;e=entries[code];ids=list(dict.fromkeys(cid for g in e['goals'] for cid in g['case_ids']))
  evidence=[]
  for page in e['source_review']['pdf_pages']:
   p=R/f'data/source_review_images/{image_prefix}-{page:03}.png'
   evidence.append(dict(pdf_page=page,printed_page=page-6,file=p.relative_to(R).as_posix(),sha256=sha(p)))
  resources={resource_file(v['path']) for cid in ids for v in cases[cid].get('resources',[])}
  record=dict(code=code,state='self_checked_source_image',reviewer='Codex',date='2026-11-04',
   scope='실제 저장 이미지를 시각적으로 읽고 원문 문장·해설·적용 시 고려 사항을 목표·과제 및 보완 발문과 대조. 독립 검토·학생 검증과 별도.',
   official_goal=e['official_goal'],findings=note,evidence=evidence,
   entry_snapshots={code:entry_digest(e)},case_snapshots={cid:digest(cases[cid]) for cid in ids},
   resource_snapshots={p.relative_to(R).as_posix():sha(p) for p in sorted(resources)},
   content_locations=[corpus,'analyses/'+code+'.md','data/curriculum_mapping_reviews.json'],independent_review=False,student_validated=False)
  old=prior.get(code)
  if old:
   changes=changed_targets(old,entries,cases)
   assert not changes or (reviewed_changes or {}).get(code),'Changed reviewed target needs explicit source re-review: '+code
   assert old['evidence']==record['evidence'] or (reviewed_changes or {}).get(code),'Changed source image needs explicit re-review: '+code
   record['history']=old.get('history',[])
   if {k:v for k,v in old.items() if k!='history'}!={k:v for k,v in record.items() if k!='history'}:
    record['history'].append(dict(date='2026-11-04',reason=(reviewed_changes or {}).get(code,'검토 근거 기록 보강'),previous_record={k:v for k,v in old.items() if k!='history'}))
  reviews.append(record)
 ledger['reviews']=[v for v in ledger['reviews'] if v['code'] not in {r['code'] for r in reviews}]+reviews
 out.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 qp=R/'data/content_review_queue.json';queue=json.loads(qp.read_text(encoding='utf-8'));new=0
 for record in queue['source_image_review']:
  if record['code'] not in {v['code'] for v in reviews}:continue
  review=next(v for v in reviews if v['code']==record['code']);new+=record['status']=='미대조'
  record.update(status='원문 이미지 자체 대조',pdf_pages=[v['pdf_page'] for v in review['evidence']],
   evidence=dict(file=out.relative_to(R).as_posix(),code=record['code'],reviewer='Codex',date=review['date'],scope=review['scope']))
 qp.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 cp=R/'data/source_corrections.json';corrections=json.loads(cp.read_text(encoding='utf-8'))
 corrections['additional_reviewed_codes']=list(dict.fromkeys(corrections.get('additional_reviewed_codes',[])+[v['code'] for v in reviews]))
 for review in reviews:
  corrections.setdefault('additional_review_evidence',{})[review['code']]=dict(file=out.relative_to(R).as_posix(),code=review['code'],date=review['date'],scope='문장·해설·적용 시 고려 사항의 자체 이미지 대조')
 cp.write_text(json.dumps(corrections,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 pages=sorted({v['pdf_page'] for r in reviews for v in r['evidence']})
 lines=['# '+subject+' 원문 이미지 대조','','2026년 11월 4일. PDF '+', '.join(map(str,pages))+'쪽의 실제 이미지를 읽고 '+str(len(reviews))+'개 기준의 문장·해설·적용 시 고려 사항과 반영 위치를 자체 대조했다. 외부 독립 검토와 실제 학생 반응 검증을 뜻하지 않는다.','','[검토 원장](../data/curriculum_standard_image_reviews.json)에 PDF·이미지·목표·과제·자료 해시를 보존하고 [후속 검토 대장](../data/content_review_queue.json)에 상태를 반영했다.','','| 기준 | 확인한 조건과 반영 위치 |','|---|---|']
 lines+=['| ['+v['code']+'](../analyses/'+v['code']+'.md) | '+v['findings']+' |' for v in reviews]
 (R/'docs'/report_name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(subject,': image-reviewed',len(reviews),'newly cleared',new,'pending',sum(v['status']=='미대조' for v in queue['source_image_review']))

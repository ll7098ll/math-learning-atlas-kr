"""Record the actual 2026-11-04 review of the four saved economy page images."""
from pathlib import Path
import hashlib,json
from mapping_review_author import digest,entry_digest,resource_file
R=Path(__file__).resolve().parents[1]
NOTES={
'01-01':'PDF178의 문장·해설 일치. 생활 경제지표를 단순화하며 수학 표현으로 변화를 설명한다. 가상 지수 과제와 공식 항목423의 실제 통계 발문·CSV, 항목433의 표현 비교에 반영.',
'01-02':'PDF178의 환율 실생활 문제 문장 일치. 단위·매매 방향·수수료의 가상 과제와 항목432의 선택 근거에 반영. 현재 환율로 주장하지 않는다.',
'01-03':'PDF178의 세금 실생활 문제 문장 일치. 구간 세율·평균세율·한계세율을 가상 과제로 다루고 현행 세법으로 주장하지 않는다.',
'01-04':'PDF178의 단리·복리 이자·원리합계·현재가치 문장과 시점 해설 일치. 같은 원금·기간 비교에 반영. 연속복리는 미적분Ⅱ 이수 학생의 선택 확장이므로 필수 과제와 구별.',
'01-05':'PDF178은 시점별 현재가치의 등비수열과 등비수열의 합 또는 등비급수를 명시. 유한 기말 연금·기초 지급 비교와 i>0 영구연금의 별도 과제로 구별해 반영.',
'02-01':'PDF179의 경제 현상 함수 표현 문장과 다른 변수를 고정한 일변수 함수 고려 사항 일치. 비용·수입·이익의 정의역·단위와 모형 가정에 반영.',
'02-02':'PDF179의 수요·공급 곡선 의미 탐구 문장 일치. 가격 세로축·수량 가로축과 곡선 위 이동 및 곡선 자체 이동을 구별하는 과제에 반영.',
'02-03':'PDF179의 효용 의미·함수·그래프 문장 일치. 가상 효용의 총량·추가 소비 기여를 q범위와 함께 해석하는 과제에 반영.',
'02-04':'PDF179의 상호 작용과 균형가격 문장 일치. 수요량·공급량 일치 및 초과수요·초과공급을 가상 모형 안에서 설명.',
'02-05':'PDF179의 세금·소득에 따른 균형가격 변화와 평행이동 해설 일치. 세금의 구매·판매 가격 차 및 소득에 따른 절편 이동을 별도 과제로 반영.',
'02-06':'PDF179은 다항식 곱의 영역을 제외하고 최대·최소의 경제 함수는 일차식만 다룬다. 비음수 수량·일차 제약·일차 목적함수 과제로 반영.',
'03-01':'PDF180의 m×n 행렬 표현 및 덧셈·뺄셈·실수배·곱셈 해설 일치. 판매수량·가격 과제와 항목425의 네 연산 수치 발문에 반영.',
'03-02':'PDF180의 2×2 역행렬 문장 일치. 행렬식0 반례와 곱이 단위행렬인지 확인하며 복잡한 형식 논리·엄밀 대수 증명을 요구하지 않는다.',
'03-03':'PDF180의 행렬 연산·역행렬로 경제 문제 해결 문장 일치. 연립식·역행렬 계산의 대수적 해와 경제적 가능성 확인에 반영.',
'04-01':'PDF180–181은 직관적 극한·접선 기울기·다항함수 미분을 다루고 미분가능성은 제외. 평균변화율→접선·한계비용 과제와 항목427의 한계효용·수입·생산량에 반영.',
'04-02':'PDF180 문장과 PDF181의 다항함수·도구 고려 사항 일치. 이익 개형의 증감·최댓값 음수 사례 및 정의역·끝점 해석에 반영.',
'04-03':'PDF180의 탄력성 탐구 문장과 PDF181의 한계 개념 고려 사항 일치. 상대변화율의 비·부호 관례·양의 가격과 수요량 조건에 반영.',
'04-04':'PDF180–181의 최적화·다른 변수 고정·합리적 선택 해설 일치. 제약이 다른 이익 최적화와 항목435의 선택 근거에 반영. 실제 경제 효과로 일반화하지 않는다.'}

def main():
 data=json.loads((R/'data/goal_hierarchy_economy_ai.json').read_text(encoding='utf-8'))
 entries={e['code']:e for e in data['entries']};cases={c['id']:c for c in data['cases']}
 pdf_sha=hashlib.sha256((R/'[별책8] 수학과 교육과정.pdf').read_bytes()).hexdigest()
 reviews=[]
 for suffix,note in NOTES.items():
  code='12경수'+suffix;e=entries[code];ids=list(dict.fromkeys(cid for g in e['goals'] for cid in g['case_ids']))
  evidence=[]
  for page in e['source_review']['pdf_pages']:
   path=R/f'data/source_review_images/economy-{page:03}.png'
   evidence.append(dict(pdf_page=page,printed_page=page-6,file=path.relative_to(R).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
  resources={resource_file(v['path']) for cid in ids for v in cases[cid].get('resources',[])}
  reviews.append(dict(code=code,state='self_checked_source_image',reviewer='Codex',date='2026-11-04',
   scope='실제 저장 이미지를 시각적으로 읽고 원문 문장·해설·적용 시 고려 사항을 목표·과제 및 내용 체계의 보완 발문과 대조. 외부 독립 검토나 학생 반응 검증과 구별.',
   official_goal=e['official_goal'],findings=note,evidence=evidence,
   entry_snapshots={code:entry_digest(e)},case_snapshots={cid:digest(cases[cid]) for cid in ids},
   resource_snapshots={path.relative_to(R).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(resources)},
   content_locations=['data/goal_hierarchy_economy_ai.json','analyses/'+code+'.md','data/curriculum_mapping_reviews.json'],independent_review=False,student_validated=False))
 out=R/'data/curriculum_standard_image_reviews.json'
 ledger=json.loads(out.read_text(encoding='utf-8')) if out.exists() else dict(source_file='[별책8] 수학과 교육과정.pdf',source_sha256=pdf_sha,reviews=[])
 assert ledger['source_sha256']==pdf_sha
 ledger['reviews']=[v for v in ledger['reviews'] if v['code'] not in {r['code'] for r in reviews}]+reviews
 out.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 qp=R/'data/content_review_queue.json';queue=json.loads(qp.read_text(encoding='utf-8'));updated=0
 for record in queue['source_image_review']:
  if record['code'] not in {v['code'] for v in reviews}:continue
  review=next(v for v in reviews if v['code']==record['code'])
  record.update(status='원문 이미지 자체 대조',pdf_pages=[v['pdf_page'] for v in review['evidence']],
   evidence=dict(file=out.relative_to(R).as_posix(),code=record['code'],reviewer='Codex',date='2026-11-04',scope=review['scope']))
  updated+=1
 qp.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 # The original inventory generator and the portal read this status registry.
 # Preserve the correction wording for the two previously corrected records.
 cp=R/'data/source_corrections.json';corrections=json.loads(cp.read_text(encoding='utf-8'))
 corrections['additional_reviewed_codes']=list(dict.fromkeys(corrections.get('additional_reviewed_codes',[])+[v['code'] for v in reviews]))
 for review in reviews:
  corrections.setdefault('additional_review_evidence',{})[review['code']]=dict(file=out.relative_to(R).as_posix(),code=review['code'],date=review['date'],scope='문장·해설・적용 시 고려 사항의 자체 이미지 대조')
 cp.write_text(json.dumps(corrections,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 lines=['# 경제 수학 원문 이미지 대조','','2026년 11월 4일. 제공 PDF178–181쪽(인쇄172–175쪽)의 실제 이미지를 읽고 18개 기준의 문장·해설·적용 시 고려 사항을 자체 대조했다. 기존에 이미지 수정 이력이 있던 두 기준을 포함하므로 미대조 감소는16개다. 외부 독립 검토·학생 반응 검증과 구별한다.','','[검토 원장](../data/curriculum_standard_image_reviews.json)에 PDF·이미지·목표·과제·자료 해시를 보존한다. 기존 기록과 통합한 미대조 현황은 [후속 검토 대장](../data/content_review_queue.json)에 남긴다.','','| 기준 | 확인한 조건과 반영 위치 |','|---|---|']
 lines += ['| ['+r['code']+'](../analyses/'+r['code']+'.md) | '+r['findings']+' |' for r in reviews]
 (R/'docs/경제수학원문이미지대조.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print('Image-reviewed economy standards:',len(reviews),'queue records:',updated,'pending:',sum(v['status']=='미대조' for v in queue['source_image_review']))
if __name__=='__main__':main()

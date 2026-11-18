"""Record the project resources and full 2015 paper actually read."""
import csv,hashlib,json
from literature_review import ROOT,digest,target_value,load_registry,build_report
from units_coordination_evidence import CSV,NOTES,build_report as recalculate
SOURCE='VT_ASSESSMENT'
URL='https://math.vt.edu/research/math-ed-research/scheme-assessment-project.html'
BASE='https://math.vt.edu/content/math_vt_edu/en/research/math-ed-research/scheme-assessment-project/_jcr_content/content/vtmultitab/'
PDF_URL=BASE+'vt-items_0/download_294947592/file.res/uc-paper.pdf'
SHA='4e73064758316faead10f2182c04cc045b61cc32095a6fd1d82bc9a922db44cd'
MAPPINGS=[
 ('UC01','family:multiply',['4수01-04','4수01-05'],['2015 PDF3 Table1','PDF6–7','PDF20–26 AppendixA/B'],
  '낱개·묶음·묶음의 묶음의 관계와 정답에 이르는 과정을 별도로 관찰할 이유를 제공한다.',
  '15라는 정답이나 풀이 속도 하나만으로 세 수준의 동시 조정을 판정하지 않는다.'),
 ('UC02','pilot:fraction-06',['6수01-10'],['2015 PDF12–16','PDF25–26'],
  '같은 수치와 완성된 그림이라도 풀이를 구성하는 과정과 설명을 함께 기록하도록 한다.',
  '3m의1/4을3/4m로 쓰는 자체 과제는 원도구7문항과 같지 않으며 기존 경로의 필수 선수성도 미검증이다.'),
 ('UC03','pilot:fraction-09',['4수01-10','6수01-10'],['2015 PDF2,7–8','2015 PDF26 Task7','Grade8 items6–9,19–22'],
  '가분수 생성·전체 복원·남은 단위의 기준 유지를 다른 관찰로 구별한다.',
  '5÷3의 정답 하나를 원도구의 단계 판정으로 바꾸지 않는다. 문항 변경·번역의 타당성은 별도다.'),
 ('UC04','family:fraction',['4수01-09','4수01-10','4수01-11','6수01-06','6수01-07'],['2015 PDF8–17 Tables2–5','Project Grade6/7/8, Chinese tasks'],
  '서면·설명·추가 관찰을 함께 보고 근거 부족과 서로 다른 반응을 남기는 진단 설계에 참고한다.',
  '검증 연구는 미국 한 지역의 소표본이며 수정 채점표도 같은20명을 재평정했다. 공개 문항의 학년 표기가 한국 학년별 필수 경로를 뜻하지 않는다.'),
 ('UC05','family:fracop',['6수01-09','6수01-11'],['2015 PDF24 Task7','PDF26 revised rubric','Grade8 items19–22'],
  '나눗셈의 남은 양을 전체의 일부인지 측정 단위의 일부인지 구별해 설명하도록 한다.',
  '계산 착오·무응답·설명 부족을 같은 인지 결손으로 확정하지 않는다. 원도구의 점수를 자체 관찰 점수로 전용하지 않는다.')]

def main():
 registry=load_registry()
 if SOURCE in registry['sources']:
  print('Reviewed source and targets remain current; no automatic refresh');build_report();recalculate();return
 assert hashlib.sha256((ROOT/'tmp/literature/units-coordination-instrument-2015.pdf').read_bytes()).hexdigest()==SHA
 # Transcribed only the anonymous numeric ratings of published Table4, visually checked on PDF15.
 columns={
  'R5':[2,1,1,1,1,2,1,2,1,2,2,1,1,3,1,1,2,1,2,3],
  'R6':[2,1,1,1,1,1,1,2,1,3,3,1,1,3,1,1,2,2,2,2],
  'R7':[2,1,2,1,1,2,1,2,1,2,3,1,2,3,1,1,2,1,2,3],
  'R8':[2,1,1,1,1,1,1,2,1,3,3,1,1,3,1,1,2,1,2,3],
  'VideoFinal':[2,1,1,1,1,2,1,2,2,2,2,1,1,3,1,1,2,1,2,3]}
 with (ROOT/CSV).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['published_case',*columns,'source_table','data_kind']);w.writeheader()
  for i in range(20):w.writerow(dict(published_case=i+1,**{k:v[i] for k,v in columns.items()},source_table='Norton_et_al_2015_Table4_PDF15',data_kind='published_ratings_not_local_student_responses'))
 artifacts=[dict(file='units-coordination-instrument-2015.pdf',url=PDF_URL)]
 artifacts += [dict(file=f'grade{g}-pool.doc',url=BASE+f'vt-items_1/vtmultitab/vt-items_{g-6}/download/file.res/grade{g}-pool.doc') for g in [6,7,8]]
 artifacts += [dict(file='chinese-fraction-tasks.pdf',url=BASE+'vt-items_1/vtmultitab/vt-items_3/download/file.res/chinese-tasks.pdf')]
 for a in artifacts:a['sha256']=hashlib.sha256((ROOT/'tmp/literature'/a['file']).read_bytes()).hexdigest()
 notes=dict(source_id=SOURCE,source_url=URL,source_pdf_url=PDF_URL,source_pdf_sha256=SHA,reviewer='Codex',date='2026-11-04',contains_source_full_text=False,source_pdf_redistributed=False,
  reading_log=['공식 프로젝트 안내 전체와 도구별 범주·원연구 참조를 확인.',
   '2015 논문 PDF1–19 본문·참고문헌 전체 텍스트, 그림1–5·표1–5의 이미지 확인.',
   'PDF20–24 부록A의 원문7문항과 그림, PDF25–26 수정 채점표 전체를 실제 이미지로 확인.',
   'grade6/7/8-pool.doc는 실제RTF. 본문20/23/22문항 및 추출한 내장 그림21/22/22개를 확인. 원래Word쪽 레이아웃의 재현 확인과는 구별.',
   'Chinese tasks PDF7쪽22문항을 모두 이미지로 읽고, 이미 분할된 도형과 분할되지 않은 도형·기준 전체 복원을 구별. 번역의 측정 동등성 검증은 수행하지 않음.'],
  visual_pdf_pages=[3,6,8,12,13,14,15,16,20,21,22,23,24,25,26],source_corrections=[],observed_source_files=artifacts,
  published_ratings_csv=CSV,published_ratings_csv_sha256=hashlib.sha256((ROOT/CSV).read_bytes()).hexdigest(),
  assessment_limits=['주 검증은 미국 남부 농촌6학년20명(합의평정1단계10명·2단계8명·3단계2명). 수정 전후 같은20명이며 새 표본 실험이 아니다.',
   '추가7학년20명에서 높은 일치도를 보고했으나3단계가 없어2↔3구별의 검증을 대신하지 못함.',
   '영상 합의평정은 연구자가 정한 준거이며 외부의 완전한 정답이 아니다. 학생9의 서면 오판 사례와 그림의 사용 과정에 따른 다른 해석을 확인.',
   '상관과 정확 일치는 다르다. 표4의 평정 수치만 자체 재계산하며 원녹화·전체응답·모든 통계분석은 재검토하지 않음.'])
 (ROOT/NOTES).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 sp=ROOT/'data/sources.json';sources=json.loads(sp.read_text(encoding='utf-8'));b=next(s for s in sources if s['id']==SOURCE);previous=dict(b)
 b['review_scope']='공식 안내 전체, 2015 단위 조정 검증 논문26쪽(과제7개·수정 채점표 포함), 6/7/8학년 분수 도구 본문65문항·내장그림65개, 중문7쪽22문항 확인. 원Word쪽 재현·번역 동등성·인용된 모든 분수 검증 원연구 대조와는 구별.'
 b['next_review']='2013 분수 스킴 검증 연구와2011/2012 원연구는 추가 대조 대상. 자체 번역·수치변경 과제와 실제 학생에 대한 타당성은 별도 검증.'
 source=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-04',snapshot_kind='authored_review_notes',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256((ROOT/NOTES).read_bytes()).hexdigest(),source_pdf_sha256=SHA,
  redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,
  display=dict(title='Virginia Tech 공개 도구 및 Norton 외(2015) 단위 조정 검증 연구',url=URL,authors_year='Norton, Boyce, Phillips, Anwyll, Ulrich and Wilkins 2015; VT project resources'),
  read_scope='공식 안내·공개5파일과 논문 부록까지 위 읽기 기록의 범위로 확인',
  scope_note='자체 진단에서는 정답·그림의 외관·반응 속도만으로 단계를 확정하지 않는다. 최초 반응과 도움 후 반응을 구별하고 설명·단위·풀이 순서를 기록하며 근거가 부족하면 판단을 보류한다.',
  method_note='2015 논문의6학년20명을 채점표 개발·수정 및 반복 평정에 사용했고 별도7학년20명도 살폈다. 원자료 전체가 아닌 표4의 공개 평정만 재계산했다. 서면평정과 영상 합의평정의 상관을 자체 과제의 효과로 옮기지 않는다.',
  limits='3단계는 주표본2명, 추가표본0명이며 지역·표본 제한이 있다. 영어·중문 도구 읽기를 번역 동등성이나 한국 학년별 타당성 검증으로 보지 않는다. 분수 도구의 모든 인용 검증 연구와 원영상은 추가 대조 대상이다.',
  editorial_action='자체 관찰2건과 분수 관찰 기록 절차를 보완. 공개 평정20행의 출처를 구별하고 일치도·상관을 재계산. 독립/학생 검증 완료로 승격하지 않음.',independent_review=False,student_validated=False,
  observations=[
   dict(id='UC-P1',standard_codes=['4수01-04','4수01-05'],question='중간 띠M은 작은 띠S의5배, 긴 띠L은M의3배다. L은S의 몇 배인가? 이어L이S의15배이고M이S의5배일 때L이M의 몇 배인지 설명하라.',
    expected='L은S의15배이며 역질문에서는M의3배다.15개의S·3개의M·M마다5개의S를 연결하고 각각의 수가 어떤 단위를 세는지 설명한다.',
    interpretation='같은 정답에 이르는 세기·묶음 반복·관계의 직접 조정을 관찰할 수 있는 자체 과제다. 최초 풀이를 보존하고 그림의 제작 순서와 설명을 중립적으로 묻는다. 한 답·속도·그림만으로 단계 분류를 하지 않는다.',student_validated=False),
   dict(id='UC-P2',standard_codes=['4수01-10','6수01-10','6수01-11'],question='띠L은 같은 작은 띠S13개 길이이고 띠M은S5개 길이다. L을M단위로 나타내고, 남은S3개의 길이를M과L을 각각 기준으로 표현하라.',
    expected='L은M의13/5배로2와3/5단위다. 남은S3개는M의3/5이면서L의3/13이다. 같은 남은 길이에 붙은 분수의 기준이 다름을 설명한다.',
    interpretation='나머지 수치3과 새 단위의3/5를 구별하는 자체 확장 관찰이다. 틀린 수치·무응답만으로 인지 결손을 확정하지 않으며 원문7문항 채점표의 점수를 그대로 부여하지 않는다.',student_validated=False)])
 registry['sources'][SOURCE]=source
 for cid,target,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,target_snapshots={target:digest(target_value(target))},standard_codes=codes,independent_review=False,student_validated=False))
 sp.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 qp=ROOT/'data/content_review_queue.json';queue=json.loads(qp.read_text(encoding='utf-8'));row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE);row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[c[0] for c in MAPPINGS]);qp.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 build_report();recalculate()
if __name__=='__main__':main()

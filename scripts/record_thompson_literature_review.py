"""Persist the author draft actually read, using authored notes rather than redistributing it."""
import hashlib,json
from literature_review import ROOT,digest,target_value,load_registry,build_report
SOURCE='THOMPSON_SALDANHA_2003'
SHA='e2ae664fde46d2d56dd730085b19f98ab7f392f0dea233694b6e0b97e4c5343a'
URL='https://pat-thompson.net/PDFversions/2004FracsMultRsng.pdf'
MAPPINGS=[
 ('TS01','relation:L005',['6수01-10','6수02-03'],['PDF28–32 Division/Fraction schemes','PDF34'],
  '같은 몫의 수치에서도 분배량·측정 단위 수·상대 크기를 구별하는 개념 분석에 참고한다.',
  '자체3m÷4 과제나 한국 학생의 필수 숙달 순서를 직접 검증하지 않는다.'),
 ('TS02','relation:L022',['4수01-10','6수01-10','6수03-12','6수03-13'],['PDF15–19 Measurement schemes','PDF17 Fig1','PDF23 Fig4'],
  '양의 크기와 단위에 따른 측정 수치를 구별하는 공통 분석 관점이다.',
  '길이·넓이의 속성과 단위를 유지해야 하며 두 능력 사이의 필수 선수성은 미검증이다.'),
 ('TS03','family:ratio',['6수02-02','6수02-03','6수02-04','6수02-05'],['PDF7','PDF19–20','PDF31–33'],
  '차에 의한 비교와 배에 의한 비교, 기준량·비교 방향의 구별에 참고한다.',
  '초고PDF7의 증가량은 실제3000명이다. 모든 상황이 정비례이거나 모든 비 과제가 동일한 스킴을 요구하는 것은 아니다.'),
 ('TS04','family:measure',['4수03-16','4수03-18','4수03-21','6수03-12'],['PDF15–19','PDF17 Fig1'],
  '같은 양을 더 작은 단위로 재면 수치가 커지는 단위 조정 관점에 대응한다.',
  '온도처럼 원점이 다른 환산이나 길이·넓이·부피 사이에 같은 환산 배율을 적용하지 않는다.'),
 ('TS05','family:fracop',['6수01-08','6수01-09','6수01-11'],['PDF24–27 Multiplication schemes','PDF28–34 Division/Fraction schemes'],
  '계산 명령과 배율의 의미를 구별하고 분수 나눗셈의 역수 곱셈을 측정 단위의 크기로 설명한다.',
  '양의 양과0이 아닌 나누는 수의 맥락이다. 음의 유리수나 모든 문자식으로의 확장은 별도 정당화한다.')]

def main():
 registry=load_registry()
 if SOURCE in registry['sources']:
  print('Existing reviewed source and targets remain current; no automatic refresh');build_report();return
 pdf=ROOT/'tmp/literature/fractions-multiplicative-reasoning-draft.pdf'
 assert hashlib.sha256(pdf.read_bytes()).hexdigest()==SHA
 notes=dict(source_id=SOURCE,source_url=URL,source_pdf_sha256=SHA,date='2026-11-04',reviewer='Codex',
  contains_source_full_text=False,source_pdf_redistributed=False,
  visual_pdf_pages=[7,17,18,20,21,22,23,24,25,26,27,30,31,32,33,34,35],
  source_corrections=[dict(pdf_page=7,printed_page=6,kind='source_draft_arithmetic_error',
   observation='표의5000→8000,6000→9000은 각각3000명 증가다. 원문 설명의1000명과 불일치하며 이미지로도 확인했다.',
   verified_math='8000-5000=9000-6000=3000; 8000/5000=1.6, 9000/6000=1.5; 증가율60%,50%.',
   action='원문 파일은 보존하고 자체 발문·기대 설명은3000명 증가로 작성한다. 최종 출판본의 정정 여부는 미확인.')])
 # The log is our own prose, not an extract or replacement copy of the chapter.
 notes['reading_log']=[
  'PDF1의DRAFT와 출판 예정95–114쪽 표기를 확인. 최종 출판본과 미대조.',
  'PDF2–14 본문 텍스트: 문제 제기·역사적 조사 인용·개념 분석. 성숙한 의미의 목표와 발달 경로의 실증을 구별.',
  'PDF15–23 본문과 그림1–4: 측정 단위·양의 크기·이중 비례·곱의 단위.',
  'PDF24–35 본문과 그림5–8: 배율·등분/포함·기준 전체·역수에 의한 나눗셈. 분수식은 이미지로 확인.',
  'PDF36–38 본문: 종합·결론·행동으로 개념 조작을 추정하는 평가의 한계. PDF39–45참고문헌,46마지막 빈 쪽 확인.']
 file='data/literature_evidence/THOMPSON_SALDANHA_2003_review_notes.json'
 (ROOT/file).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 sp=ROOT/'data/sources.json';sources=json.loads(sp.read_text(encoding='utf-8'));b=next(s for s in sources if s['id']==SOURCE);previous=dict(b)
 b['review_scope']='저자 공개 DRAFT46쪽 전체 텍스트와 그림1~8·분수식·표의 이미지 확인. L005/L022와 비·측정·분수 연산 분석군의 주장5건을 대조. 최종 출판본·인용 원연구 전부는 미대조.'
 b['next_review']='최종 출판본의 내용·정정과 인용 원연구를 별도 확인. 자체 과제의 실제 학생 응답은 미검증.'
 source=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-04',
  snapshot_kind='authored_review_notes',snapshot_file=file,snapshot_sha256=hashlib.sha256((ROOT/file).read_bytes()).hexdigest(),source_pdf_sha256=SHA,
  redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,
  display=dict(title=b['title']+' (저자 공개 DRAFT)',url=URL,authors_year='Thompson and Saldanha, bibliography year 2003'),
  read_scope='46쪽 전체 텍스트(표지·본문·참고문헌·마지막 빈 쪽), 그림1~8 및 주요 수식/표17쪽의 이미지 확인',
  scope_note='성숙한 분수 의미의 개념 분석이다. 현재 학생의 학습 순서나 필수 선수성을 입증한 독립 실험으로 사용하지 않는다.',
  method_note='선행 연구와 설명 사례·일부 면담을 활용한 이론 장의 초고다. 인용된 조사·교사/학생 연구의 원자료를 모두 재검토한 것은 아니다.',
  limits='최종 출판본과 미대조이며 현재 한국 학생에 대한 효과·발달 일반화는 하지 않는다. 원문PDF7의 인구 증가량1000은 표와 모순되어3000으로 따로 검산했다. 원문을 재배포하지 않고 자체 읽기 기록·원문 해시·공식 주소를 보존한다.',
  editorial_action='몫과 비율의 단위, 단위 교환, 분수 나눗셈의 크기, 증가량과 증가율을 확인하는 자체 관찰4건 추가. 기존 방향·조건·판정 상태는 유지.',
  independent_review=False,student_validated=False,
  observations=[
   dict(id='TS-P1',standard_codes=['6수01-10','6수02-03'],question='3m를4명에게 똑같이 나눈 한 사람의 몫과,3m를4m와 비교한 비율을 각각 구하라. 같은3/4이 나타나도 답의 단위·기준·비교 방향이 어떻게 다른가?',
    expected='분배한 한 사람의 몫은3/4m이고 사람당 배분량은3/4m/명이다. 두 길이의 비율은(3m)/(4m)=3/4로 공통 단위가 소거된다. 기준을 바꾸면(4m)/(3m)=4/3이다.',
    interpretation='같은 수치와 같은 의미를 구별하는 자체 관찰이다. 한 응답으로 두 개념 사이의 필수 선수성을 판정하지 않는다.',student_validated=False),
   dict(id='TS-P2',standard_codes=['4수01-10','6수01-10','6수03-12'],question='3/4m인 같은 띠를1m 단위와1/4m 단위로 각각 나타내라. 이어 같은1cm² 정사각형을 한 변1/2cm인 정사각형으로 덮을 때 단위 넓이와 필요한 개수를 설명하라.',
    expected='띠의 측정 수치는3/4에서3으로 바뀌지만 길이는 같다. 작은 정사각형의 넓이는1/4cm²이고4개로 원래 영역을 덮는다. 변이1/2배라고 넓이도1/2배인 것은 아니다.',
    interpretation='길이와 넓이를 별도로 확인하는 확장 활동이다. 단위 길이·단위 넓이를 구별하고 두 수행 사이의 인지적 전이를 자동 인정하지 않는다.',student_validated=False),
   dict(id='TS-P3',standard_codes=['6수01-11'],question='3/4L인 주스를1/2L들이 용량 단위로 재면 몇 단위인가? 계산 전에1단위보다 큰지 예측하고, 남은 양의 분수는 무엇을 기준으로 한 것인지 설명하라.',
    expected='(3/4L)/(1/2L)=3/2단위다.1단위인1/2L와 남은1/4L를 합친 양이며, 남은 양은1L의1/4이면서1/2L 단위의1/2이다. 실물 용기가1.5개 생긴다는 뜻과 구별한다.',
    interpretation='양의 분수 나눗셈에서 재설정한 측정 단위를 확인한다. 계산 정답만으로 개념 조작을 확정하지 않는다.',student_validated=False),
   dict(id='TS-P4',standard_codes=['6수02-02','6수02-03'],question='두 지역의 인구가 각각5000→8000명,6000→9000명으로 변했다. 증가량이 같다는 말과 첫 지역이 더 크게 증가했다는 말이 어떤 비교 기준에서 성립하는지 설명하라.',
    expected='증가량은 둘 다3000명이다. 처음 인구에 대한 증가율은60%,50%이므로 상대 증가는 첫 지역이 크다. 새 인구가 처음의160%,150%라는 비율과 증가율60%,50%를 구별한다.',
    interpretation='출처 초고의 증가량 오기를 그대로 옮기지 않고 검산한 발문이다. 실제 지역 통계가 아닌 수학적 설명 사례이며 학생 응답 검증은 아직 없다.',student_validated=False)])
 registry['sources'][SOURCE]=source
 for cid,target,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,target_snapshots={target:digest(target_value(target))},standard_codes=codes,independent_review=False,student_validated=False))
 sp.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 qp=ROOT/'data/content_review_queue.json';queue=json.loads(qp.read_text(encoding='utf-8'));row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE)
 row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[c[0] for c in MAPPINGS])
 qp.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');build_report()
if __name__=='__main__':main()

"""Record historical textbook models and their limits without claiming pupil effects."""
import hashlib,json
from literature_review import ROOT,digest,target_value,load_registry,build_report
SOURCE='PARK_LEE_2018'
URL='https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART002345499'
PDF_URL='https://www.kci.go.kr/kciportal/co/download/popup/poDownload.kci?storFileBean.orteFileId=KCI_FI002345499'
SHA='5403932dac15be1f6f830dc229a1fd91b9587ebb5afd1d95c2f1843b913b5eee'
NOTES='data/literature_evidence/PARK_LEE_2018_review_notes.json'
SCOPE=dict(design='comparative_textbook_content_analysis',sample_description='2015년판5·6학년 주교과서8종: 한국1종·일본3종·싱가포르3종·미국1종의 모델이 제시된 문제 상황을 비교.',inference_limit='국가별 선정 수가 다르며 현행 교과서 전수 조사·학생 반응 실험이 아니다. 원교과서 전권과 인용 원연구를 재검토한 것도 아니다.',student_outcome_study=False,causal_effect_established=False,local_effect_tested=False)
MAPPINGS=[
 ('PL01',['6수02-04','6수02-05'],['PDF4–5 / printed240–241 Figs4–6','PDF12–15 / printed248–251 Figs26–33'],
  '고정된 한 묶음의 수를 늘리는 관점과, 부분 수를 유지하고 공통 부분의 크기를 바꾸는 관점을 비교하는 수업 설계에 참고한다.',
  '일부 교과서의 제시 순서는 모든 학생의 필수 발달 순서가 아니다. 이중수직선은 다중묶음만, 테이프는 변동부분만 표현한다는 일대일 분류도 하지 않는다. 비례식 계산 성공만으로 두 관점의 이해를 확정하지 않는다.'),
 ('PL02',['6수02-02','6수02-03','6수02-04'],['PDF5 / printed241 Fig7','PDF15–16 / printed251–252 Figs34–37','PDF18 / printed254 Table4'],
  '비표의 화살표가 같은 양의 서로 다른 크기를 잇는지, 서로 다른 양을 대응시키는지에 따라 배율의 의미를 구별한다.',
  '두 양의 단위가 같다는 사실만으로 측정공간 내의 비교라고 분류하지 않는다. 표4의일본 열 설명은 본문·그림35와 명칭이 충돌하므로 화살표의 출발량·도착량을 기준으로 해석한다. 교과서 분석이 현재 활동의 학습 효과를 입증하지 않는다.'),
 ('PL03',['6수02-02','6수02-03','6수02-04'],['PDF3 / printed239 Fig2','PDF7–12 / printed243–248 Figs8–25','PDF17,19–20 / printed253,255–256'],
  '그림·비표·이중수직선에서 단위·기준·대응쌍을 보존하고, 비례에 따른 크기와 표시 간격을 학생이 설명하도록 하는 설계에 참고한다.',
  '비표의 칸 간격과 수직선의 수치 간격은 다르다. 그림의 색·길이·눈금이나 모델 이름 하나만으로 학생 이해를 판정하지 않는다.2015년판 선정 교과서의 특징을2026년 현재 각국 전체 교과서의 특징이나 모델별 효과 순위로 옮기지 않는다.')]
OBSERVATIONS=[
 dict(id='PL-P1',standard_codes=['6수02-04','6수02-05'],question='A액6mL와B액10mL를 한 묶음으로 준비했다. 같은 비율로 두 액의 양을 각각2배로 늘리는 방법을 두 그림으로 설명하라. 첫 그림은 원래 묶음2개, 둘째 그림은A3칸·B5칸을 유지하고 모든 칸의 양을 바꾸는 테이프로 나타내라. 각 그림에서 변하는 것과 고정된 것을 말하라.',
  expected='두 방법 모두A12mL·B20mL, 준비한 총량32mL다. 첫 방법은 한 묶음의6mL·10mL를 고정하고 묶음 수를1→2로 늘린다. 둘째는A3칸·B5칸을 고정하고 한 칸의 양을2mL→4mL로 늘린다.2묶음과4mL/칸은 역할이 다르며A:B=3:5는 유지된다.',
  interpretation='동일한 수치 답에서도 무엇을 세고 무엇의 크기를 바꾸었는지 설명을 따로 기록한다. 두 관점을 반드시 정해진 순서로 가르치거나 같은 그림을 한 관점에만 배정하지 않는다. 두 답을 한 번 맞혔다는 이유로 전이·단계·장기 숙달을 인정하지 않는다.',student_validated=False),
 dict(id='PL-P2',standard_codes=['6수02-02','6수02-03','6수02-04'],question='A액2mL에B액5mL가 대응하는 일정 비율이다. A액이6mL일 때B액을 구하고, 비표에 두 풀이의 화살표를 그려 설명하라. 한 풀이는A액끼리와B액끼리 비교하고, 다른 풀이는A액에서B액으로 대응시킨다. 두 액 모두mL 단위를 쓴다는 사실만으로 같은 종류의 화살표인가?',
  expected='B액은15mL다. 같은 양 안에서는A2→6과B5→15에 각각×3을 쓴다. 양 사이에서는A액1mL당B액5/2mL이므로A6→B15에×5/2를 쓴다. 모두mL로 적어도A액과B액은 다른 양이므로 화살표의 출발·도착이 다르다.',
  interpretation='화살표의 위치와 배율의 의미를 함께 확인한다. 원문 표4의명칭을 그대로 채점표로 쓰지 않고 실제 연결한 양을 묻는다. 두 양을 같은 배로 조정하는 방법과 단위 비율로 대응시키는 방법은 모두 유효하다. 교사가 화살표를 먼저 제시했다면 그 전후의 반응을 구별한다.',student_validated=False),
 dict(id='PL-P3',standard_codes=['6수02-03','6수02-04'],question='가상 지도에서 지도상1cm가 실제4km에 대응하고 축척은 일정하다. 대응쌍(0cm,0km), (1cm,4km), (2.5cm,10km), (5cm,20km)를 비표와 이중수직선으로 나타내라. 네 대응쌍을 수직선에서 모두 같은 간격으로 찍었다면 무엇을 수정해야 하는가?',
  expected='위아래 선의 원점과 대응 위치를 맞춘다. 각 선에서 수의 차이에 비례해 눈금 간격을 정하므로 지도상 값의 차이1cm·1.5cm·2.5cm에 대응하는 간격은1:1.5:2.5이고 실제 값의 차이는4km·6km·10km다. 비표의 칸은 같은 폭이어도 되지만 수직선의 네 대응쌍을 같은 간격으로 찍으면 등간격 척도에 맞지 않는다.',
  interpretation='대응값 계산과 각 선의 척도 해석을 따로 확인한다. 두 선의숫자 증가량이 같아야 한다고 요구하지 않는다. 눈금이 없는 개략도와 수치 간격을 나타낸 수직선도 구별한다. 화살표나 색의 외관만으로 이해를 판정하지 않는 자체 설계이며 원문 교과서의 효과 검증을 전용하지 않는다.',student_validated=False)]

def main():
 registry=load_registry()
 if SOURCE in registry['sources']:
  print('Reviewed source and targets remain current; no automatic refresh');build_report();return
 assert hashlib.sha256((ROOT/'tmp/literature/park-lee-2018.pdf').read_bytes()).hexdigest()==SHA
 conflict=dict(pdf_page=18,printed_page=254,kind='table_body_label_conflict',
  observation='표4의일본 행에서 측정공간 내의 분석 열에 놓인 보조화살표 설명이 측정공간 사이의 분석으로 적혀 있다. PDF15본문은그림35(a)를내,35(b)를사이로 구별하고PDF16그림의동일양배율/서로다른양대응과 일치한다.',
  action='자체 설명은 화살표의 출발량·도착량에 따라 구별한다. 원문 파일은 고치지 않으며 출판 정오표의 공식 정정 여부는 미확인.')
 notes=dict(source_id=SOURCE,source_url=URL,source_pdf_url=PDF_URL,source_pdf_sha256=SHA,date='2026-11-04',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,
  visual_pdf_pages=list(range(1,25)),source_corrections=[conflict],empirical_scope=SCOPE,
  reading_log=['KCI서지·초록·원문24쪽 전체 텍스트와 전24쪽 실제 이미지 확인. 표4는180dpi추가 이미지로 열·설명·그림을 재대조.',
   'PDF1–5 이론·그림1–7: 다중묶음/변동부분과 측정공간 내/사이의 구분. 모델 형태와 사고 관점의 일대일 대응은 아님.',
   'PDF6방법·표1–2: 한국1·일본3·싱가포르3·미국1의총8종2015년판 주교과서. 국가별 선정 수가 다르고 보조교과서·워크북·저널은 제외. 모델과 함께 제시된 문제 상황을 분석.',
   'PDF7–12 그림8–27: 그림에서 수나양의 표현, 비표 보조화살표, 이중척도·테이프·비례식의 결합을 확인. 인용 교과서의 전권을 읽은 것은 아님.',
   'PDF13–16 그림28–37: 부분 수/크기·묶음 수, 두 유형의 화살표와 직접 대응을 확인. 이중수직선의 변동부분 해석 사례도 확인.',
   'PDF17–18 표3–4와 본문 비교: 일본 내/사이 설명 충돌을 따로 기록. PDF19–20결론은 한국 학생에게의 효과와 지도 방법을 추가 검증할 필요를 제언.',
   'PDF20–24 참고문헌·영문 초록 확인. 모든 인용 원연구와 원교과서의 재분석·현재 판본 전수 대조는 수행하지 않음.'],
  corpus=dict(publication_year=2015,series_by_country={'한국':1,'일본':3,'싱가포르':3,'미국':1},series_total=8,unit='textbook_series_not_student_sample',includes_original_textbook_full_read=False),
  interpretation_limits=['연구 대상은 교과서의 모델이며 학생 표본에 대한 처치·반응·효과의 비교가 아니다.',
   '일본·싱가포르는각3종,한국·미국은각1종으로 균형 대표 표본이 아니다. 국가 전체·현행 판본·2022개정 교육과정에 대한 일괄 주장을 하지 않음.',
   '교과서의 흐름과 이론적 제언을 개별 학생의 보편적인 필수 학습 순서나 자체 진단의 타당성으로 옮기지 않음.',
   '원문의숫자·색·그림·화살표의 교수 가능성과 실제 학생 수행을 구별. 교과서에 모델이 없다는 관찰을 학생에게 관련 사고가 없다는 뜻으로 사용하지 않음.'])
 (ROOT/NOTES).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 sp=ROOT/'data/sources.json';sources=json.loads(sp.read_text(encoding='utf-8'));b=next(s for s in sources if s['id']==SOURCE);previous=dict(b)
 b.update(review_scope='원문24쪽 전체 텍스트·전24쪽 이미지, 표1–4·그림1–37·방법·결론·참고문헌 확인.2015년판4개국8종 주교과서의 모델 비교 범위를 주장3건에 대응. 원교과서 전권·학생 효과·현행 판본은 미검증.',next_review='인용 원연구와 원교과서 전권·현행 판본은 별도 대조 대상. 표4일본 행의측정공간 내/사이 명칭 충돌은 출판 정오표 확인 전 원문을 그대로 보존. 자체 과제의 실제 학생 반응은 미검증.')
 source=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-04',snapshot_kind='authored_review_notes',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256((ROOT/NOTES).read_bytes()).hexdigest(),source_pdf_sha256=SHA,redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,
  display=dict(title=b['title'],url=URL,authors_year='박선영·이광호,2018,초등수학교육21(2),237–260'),read_scope='원문24쪽 전체 텍스트·전24쪽 이미지, 표1–4·그림1–37·방법·결론·참고문헌',
  scope_note='2015년판4개국8종 주교과서의 모델 비교다. 모델과 사고 관점을 일대일로 고정하지 않고 그림·식·표·수직선이 보존하는 양·단위·배율을 설명하도록 하는 설계에 참고한다. 국가 전체·현행 교과서·학생 효과의 비교로 일반화하지 않는다.',
  method_note='한국1종·일본3종·싱가포르3종·미국1종의5·6학년 주교과서에서 시각적 모델과 함께 제시된 문제 상황을 분석했다. 보조교과서·워크북·저널은 제외했다. 문헌에 실린 사례와 분석틀을 읽었으며 원교과서 전권을 독립 재분석한 것은 아니다.',
  limits='교과서 모델의 분포·제시 방식에 대한 분석이며 학생을 대상으로 한 인과 연구가 아니다. 국가별 선정 수가 다르고2015년판이므로 현재 모든 교과서의 특징이나 모델의 효과 순위를 입증하지 않는다. 표4일본 내/사이 설명 충돌은 본문·그림과 대조해 보존하며 정오표는 미확인이다. 자체 과제의 필수 순서·효과·진단 타당성을 검증하지 않는다.',
  empirical_scope=SCOPE,editorial_action='비례 분석군의 주장3건에 문헌 위치·모델 해석·한계를 연결. 묶음 수/부분 크기, 화살표의 출발·도착량, 비표와 수직선 간격의 차이를 확인하는 자체 활동3건 추가. 독립 검토·학생 검증은 완료로 표시하지 않음.',independent_review=False,student_validated=False,observations=OBSERVATIONS)
 registry['sources'][SOURCE]=source
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='empirical_result_with_scope',locations=locations,support=support,does_not_establish=limit,target_snapshots={'family:ratio':digest(target_value('family:ratio'))},standard_codes=codes,independent_review=False,student_validated=False,empirical_scope=dict(SCOPE)))
 sp.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 qp=ROOT/'data/content_review_queue.json';queue=json.loads(qp.read_text(encoding='utf-8'));row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE);row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[c[0] for c in MAPPINGS]);qp.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 build_report()
if __name__=='__main__':main()

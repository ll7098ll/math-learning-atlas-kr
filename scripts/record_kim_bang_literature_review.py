"""Record the full paper without converting grade differences into a causal result."""
import hashlib,json
from literature_review import ROOT,digest,target_value,load_registry,build_report
SOURCE='KIM_BANG_2014'
URL='https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART001849840'
PDF_URL='https://www.kci.go.kr/kciportal/co/download/popup/poDownload.kci?storFileBean.orteFileId=KCI_FI001849840'
SHA='4b9fcf3f800b8ec88e6cdeb3c8c3db81e602f2f1e8aec0083899d1f7a35680e7'
NOTES='data/literature_evidence/KIM_BANG_2014_review_notes.json'
SCOPE=dict(design='cross_sectional_with_selected_interviews',sample_description='수원 한 학교의 서로 다른2·4·6학년 한 학급씩, 분석34·32·34명(총100명), 그중 목적 선정 면담6명.',inference_limit='학년 간 차이는 같은 학생의 종단 변화나 무작위 수업 효과가 아니다. 단서 후 답의 수정도 독립 수행·장기 전이를 입증하지 않는다.',local_effect_tested=False,causal_effect_established=False,longitudinal_cohort=False)
MAPPINGS=[
 ('KB01','family:multiply',['2수01-10','2수01-11','4수01-04'],'related_theoretical_context',['PDF2–4 / printed58–60 Tables1–3, Figs1–3'],
  '낱개·묶음·전체와 기준량에 대한 배 비교를 구별하는 곱셈 분석 틀에 참고한다.',
  '반복 덧셈은 양의 자연수 묶음 과제의 유효한 방법이다. 그 식이나 답만으로 학생의 사고를 덧셈적 결손으로 분류하거나 모든 곱셈 상황을 같은 모델로 환원하지 않는다.'),
 ('KB02','family:fraction',['4수01-09','4수01-10','6수01-10'],'empirical_result_with_scope',['PDF9–11 / printed65–67 Figs7–10, Episode1','PDF14–15 / printed70–71'],
  '조각 수·기준 전체·부분끼리의 비교에서 서로 다른 반응을 보인 사례를 참고해, 숫자와 그림 외에 무엇을 기준으로 삼았는지 질문한다.',
  '1조각이라는 개수와 전체의1/6이라는 양은 서로 다른 단위의 설명이다. 답의 수치 하나만으로 양 보존이나 분수 개념의 부재를 확정하지 않는다. 표4의자연수/분수 대비를 자연수는 연속량 측정에 못 쓴다거나 분수의 수값이 임의로 바뀐다는 일반명제로 옮기지 않는다.'),
 ('KB03','family:ratio',['6수02-02','6수02-03','6수02-04','6수02-05'],'empirical_result_with_scope',['PDF7–9 / printed63–65 Tables5–6','PDF11–15 / printed67–71 Figs11–14, Episode2'],
  '비율 기호 없이 같은 배로 맞춘 비교, 분수·비례식 풀이 등 서로 다른 전략을 관찰하고 선행·후속 개념을 다시 연결할 수업 설계에 참고한다.',
  '일부 비례 문항의 성공을 모든 비례 상황의 숙달로 보지 않는다. 학년별 정답률 차이를 비례식 학습의 인과 효과나 전국 발달 단계로 해석하지 않는다. 동일한 차이와 동일한 비율을 구별하되 유효한 덧셈 분해 전략까지 오개념으로 묶지 않는다.'),
 ('KB04','pilot:fraction-09',['4수01-10','6수01-10'],'empirical_result_with_scope',['PDF8 / printed64 Table5','PDF11 / printed67 Fig10','PDF14–15 / printed70–71'],
  '자연수 나눗셈으로 생기는1보다 큰 몫과, 전체를 무엇으로 정했는지의 설명을 따로 확인하는 설계에 참고한다.',
  '연구의쿠키4개÷3명 과제와 현재5m÷3명은 같지 않다. 원문은 이 자체 과제의 효과·최적 순서·전이를 검증하지 않았다. 한 개 기준의 몫과 배분 전 전체에 대한 몫의 비율은 다른 응답이므로 단위를 먼저 확인한다.'),
 ('KB05','family:multiply',['2수01-10','2수01-11','4수01-04'],'empirical_result_with_scope',['PDF7–9 / printed63–65 Tables5–6','PDF13 / printed69 Episode2'],
  '곱의 전체량을 구하는 수행과 묶음·낱개를 섞어 주고받는 수행을 구별하고, 단서를 받은 반응과 최초 반응을 따로 남긴다.',
  '에피소드2에서 단서 뒤C는22개를 유지하고D는24개로 바꾸었다. 함께 답한 반응이나 도움 후 한 번의 성공을 두 학생 모두의 독립 숙달로 기록하지 않는다. 내적 일관성α=.867은 현재 활동의 타당도·진단 정확도가 아니다.')]
OBSERVATIONS=[
 dict(id='KB-P1',standard_codes=['2수01-10','2수01-11','4수01-04'],question='쿠키가4개씩 든 봉지6개가 있다. 먼저 쿠키 전체 수를 구하라. 이어 봉지2개를 주고 낱개 쿠키3개를 받으면 쿠키는 모두 몇 개인가? 식에 쓴 각 수가 봉지 수인지 쿠키 수인지 설명하라.',
  expected='처음에는24개다. 봉지2개에 든8개를 주고 낱개3개를 받아19개가 된다.4×(6−2)+3 또는24−8+3으로 설명할 수 있고, 같은 크기 봉지를 반복해서 더하는 방법도 가능하다. 받은3개를3봉지로 바꾸어 세지 않는다.',
  interpretation='먼저 전체량 계산과 다음 묶음·낱개 구별을 각각 기록한다. 반복 덧셈을 썼다는 사실만으로 결손을 판정하지 않는다. 단위 표시나 재질문을 제공했다면 그 전후를 구별한다. 학년이나 속도로 인지 단계를 확정하지 않는 자체 활동이다.',student_validated=False),
 dict(id='KB-P2',standard_codes=['6수02-02','6수02-03'],question='같은 크기 구슬이 빨강9개, 파랑6개 있다. 빨강 수는 파랑 수의 몇 배인가? 파랑 수는 빨강 수의 몇 배인가? 빨강 수는 전체 구슬 수의 얼마인가? 각 답에서 기준이 된 구슬을 표시하라.',
  expected='빨강/파랑=9/6=3/2배, 파랑/빨강=6/9=2/3배, 빨강/전체=9/15=3/5다. 차는3개로 같아도 비교 방향이나 전체를 바꾸면 기준과 비율이 달라진다.',
  interpretation='부분끼리의 두 비교와 전체에 대한 비율을 구별한다. 숫자 순서만 보고 분모를 정하는지, 실제 기준을 가리킬 수 있는지 묻는다.3/5는 세 번째 질문에서는 맞는 답이므로 앞의 질문에 썼다는 이유로 모든 분수 이해를 부정하지 않는다.',student_validated=False),
 dict(id='KB-P3',standard_codes=['6수01-10'],question='크기가 같은 쿠키7개를4명이 똑같이 나누어 먹는다. 한 사람의 몫은 쿠키 한 개를 기준 단위로 하면 얼마인가? 그 한 사람의 몫은 배분 전 전체7개 양의 얼마인가? 두 답이 달라도 같은 몫을 가리키는 이유를 설명하라.',
  expected='한 사람은쿠키7/4개=1과3/4개를 받는다. 이것은 배분 전 전체7개 양의1/4이다.1/4×7개=7/4개이며 기준 단위가 한 개인지 전체7개인지 다르다.',
  interpretation='가분수인 몫과 전체에 대한 진분수 비율을 함께 확인하는 자체 활동이다.1/4만 쓴 경우 먼저 무엇의1/4인지 중립적으로 묻는다. 단위를 정당하게 바꾼 설명과 계산 오류·발문 오해를 구별하고 원문 과제의 판정 기준을 그대로 전용하지 않는다.',student_validated=False),
 dict(id='KB-P4',standard_codes=['6수02-03','6수02-04'],question='가상 교환소에서 쿠폰8장으로 스티커12개를 받을 수 있고, 교환 비율은 일정하며 기본 지급이나 추가 보너스가 없다. 쿠폰16장,24장,4장으로 각각 몇 개를 받는가? 같은 차이를 유지하는 방법과 같은 비율을 유지하는 방법을 비교하라.',
  expected='각각24개,36개,6개다.8장과12개의 묶음을2배·3배·1/2배로 조정한다.16장일 때20개라는 답은12−8=4의 차이를 유지한 것이며 주어진 일정 비율을 만족하지 않는다. 묶음을 반복해 더해24개나36개를 구하는 것은 유효하다.',
  interpretation='최초 답과 이유를 개인별로 보존한 후 필요한 재질문·묶음 단서를 제공한다. 도움 후 답을 바꾸어도 다른 수치에서 독립 설명이 유지되는지 별도로 확인한다. 짝의 답변이나 한 번의 수정은 두 사람 모두의 숙달·장기 전이를 입증하지 않는다.',student_validated=False)]

def main():
 registry=load_registry()
 if SOURCE in registry['sources']:
  print('Reviewed source and targets remain current; no automatic refresh');build_report();return
 assert hashlib.sha256((ROOT/'tmp/literature/kim-bang-2014.pdf').read_bytes()).hexdigest()==SHA
 notes=dict(source_id=SOURCE,source_url=URL,source_pdf_url=PDF_URL,source_pdf_sha256=SHA,reviewer='Codex',date='2026-11-04',contains_source_full_text=False,source_pdf_redistributed=False,
  reading_log=['KCI서지·공개 초록·다운로드로 확인한 원문17쪽의 전체 텍스트 및 전17쪽 실제 이미지를 읽음.',
   'PDF1–6 이론·표1–4·그림1–5: 단위의 포함·관계·분수 의미를 구별. 자연수/분수의 교수 비교를 배타적인 수학적 정의로 전용하지 않음.',
   'PDF7–9 방법·표5–6·그림6–7: 최초104명에서4명 제외한100명, 목적 선정 면담6명, 제외한 고무줄 문항과13개 분석 문항을 구별.',
   'PDF10–13 학생 답안그림8–14·에피소드1–2: 기준 전환과 단서 전후의 개인 반응을 대조. 에피소드2에서C는22를 유지하고D는24로 바꿈.',
   'PDF14–17 결론·일반화 제한·참고문헌·영문 초록 확인. 같은 학생을 추적한 종단 연구·통제 실험으로 해석하지 않음.'],
  visual_pdf_pages=list(range(1,18)),source_corrections=[],empirical_scope=SCOPE,
  sample=dict(initial_by_grade={'2':36,'4':33,'6':35},excluded_by_grade={'2':2,'4':1,'6':1},analyzed_by_grade={'2':34,'4':32,'6':34},interviewed=6,interviews_are_subset=True,selection='선행 개념은 비교적 이해하나 후속 개념에 어려움이 있고 의사소통이 가능한 학생을 담임 추천으로 학년당2명 선정'),
  interpretation_limits=['학년별로 한 학급씩 조사한 횡단 비교이며 수업 처치의 무작위 배정·동일 학생의 학년간 추적은 없음. 논문의 당시 교과서 학습 시점과2022개정의 학년 배치를 구별.',
   '면담6명은100명 중 선정되며 새 독립 표본으로 더하지 않음. 사례에서 제공한 단서·그룹 상호작용과 자발적 반응을 구별.',
   '원문은내적 일관성α=.867을 보고하나 원응답·문항간 공분산이 없어 재계산하지 않았으며 현재 자체 활동에 전용하지 않음.',
   '비례식으로 분수 문제를 푼 사례는 관찰 근거다. 후속 학습의 인과 효과·전국 학년 규준·모든 문항의 필수 경로를 입증하지 않음.',
   '표4의자연수와분수의 대비는 교수적 요약이다. 자연수의 연속량 측정·다양한 동치 표현을 배제하거나 분수의 수값과 기준에 따른 양을 혼동하지 않음.'])
 (ROOT/NOTES).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 sp=ROOT/'data/sources.json';sources=json.loads(sp.read_text(encoding='utf-8'));b=next(s for s in sources if s['id']==SOURCE);previous=dict(b)
 b.update(title='곱셈적 구조에 대한 2, 4, 6학년 학생들의 수학적 사고의 연결성 분석',doi='10.7468/mathedu.2014.53.1.57',review_scope='KCI 서지와 원문17쪽 전체 텍스트·전17쪽 이미지. 표1–6·그림1–14·에피소드1–2·방법·결론·참고문헌 대조. 분석100명과 선정 면담6명, 단서 전후·학년간 횡단 비교를 구별.',next_review='인용된 개별 원연구와 원응답·원영상은 별도 대조 대상. 현재 한국어 변형 과제의 타당성·독립 검토·학생 응답 검증은 별도.')
 source=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-04',snapshot_kind='authored_review_notes',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256((ROOT/NOTES).read_bytes()).hexdigest(),source_pdf_sha256=SHA,redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,
  display=dict(title=b['title'],url=URL,authors_year='김유경·방정숙,2014,수학교육53(1),57–73'),
  read_scope='원문17쪽의 전체 텍스트·전17쪽 실제 이미지, 표1–6·그림1–14·에피소드1–2',
  scope_note='국내 학생 반응에서 곱셈·분수·비례를 연결해 살펴본 관찰 연구다. 학년별 집단의 차이·목적 선정 면담·단서 후 반응을 구별하고, 한 답이나 그림만으로 인지적 결손을 확정하지 않는다.',
  method_note='수원 한 학교에서2·4·6학년 각각 한 학급을 조사했다. 최초36·33·35명에서 해결 과정을 거의 적지 않은2·1·1명을 제외해34·32·34명, 총100명을 분석했다. 이 중 학년당2명씩6명을 목적 선정해 반구조화 면담을 실시했다. 원문이 보고한α=.867은 현재 검사로 전용하지 않는다.',
  limits='서로 다른 학년 집단의 횡단 비교이며 무작위 처치·동일 학생의 장기 추적이 아니다. 당시 교과서의 학습 시점을2022개정 학년 배치로 옮기지 않는다. 면담6명을 새 표본으로 더하지 않는다. 원문 전체 응답·영상·문항 수준 공분산은 미확보로 모든 비율·내적 일관성을 재계산한 것은 아니다. 자체 과제의 타당성과 필수 선수성·전이를 입증하지 않는다.',
  empirical_scope=SCOPE,editorial_action='주장5건의 이론/관찰 근거와 한계를 연결하고 묶음·낱개, 비교의 기준, 가분수 몫과 전체 비율, 일정 비율과 도움 전후를 확인하는 자체 활동4건 추가. 독립 검토·학생 검증은 완료로 표시하지 않음.',independent_review=False,student_validated=False,observations=OBSERVATIONS)
 registry['sources'][SOURCE]=source
 for cid,target,codes,role,locations,support,limit in MAPPINGS:
  claim=dict(id=cid,source_id=SOURCE,role=role,locations=locations,support=support,does_not_establish=limit,target_snapshots={target:digest(target_value(target))},standard_codes=codes,independent_review=False,student_validated=False)
  if role=='empirical_result_with_scope':claim['empirical_scope']=dict(SCOPE)
  registry['claims'].append(claim)
 sp.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 qp=ROOT/'data/content_review_queue.json';queue=json.loads(qp.read_text(encoding='utf-8'));row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE);row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[c[0] for c in MAPPINGS]);qp.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 build_report()
if __name__=='__main__':main()

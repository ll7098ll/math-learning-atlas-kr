"""Record two complete web-section readings and bind their authored calculus targets."""
import hashlib,json
from literature_review import ROOT,digest,target_value,load_registry,build_report

D='OPENSTAX_CALC_DERIVATIVE';F='OPENSTAX_CALC_FTC'
I='12미적Ⅰ-';II='12미적Ⅱ-'
CONFIG={
 D:dict(stem='openstax-derivative',sha='192b3c82fce0dfafe7c092e092c2cc173899aeb5cfb4a7c971a370a11ee9c008',images=12,
  scope='3.1절 웹본문 전체·식3.1~3.8·예3.1~3.10·확인3.1~3.5·연습1~53, 그림3.2~3.10과 연습 그래프3개',
  reading_log=['공식3.1절의 도입·학습목표·정의·식3.1~3.8·예3.1~3.10·확인3.1~3.5·연습1~53을 모두 읽었다. 모든 연습의 해답을 독립 계산했다는 뜻은 아니다.',
   '그림3.2~3.10의9개 자산과 연습39·40·47의3개 그래프, 합계12개를 각각 시각적으로 확인했다. 차분몫·좌우 접근·접선·속도·가속도와 단위를 대조했다.',
   '유한 표·그래프 확대는 극한을 추정하는 자료이며 극한의 존재 증명과 구별했다. 연속·유한한 미분가능·수직 접선·접선의 곡선 횡단을 구별했다.',
   '예3.8의 유한 구간 평균가속도 비교를 임의 보간 곡선의 순간가속도 단조성 증명으로 옮기지 않았다. 외부 애플릿·영상·전기 링크는 실행하지 않았다.'],
  corrections=[dict(kind='observed_image_alt_text_conflict',location='3.1절 연습39 / openstax-derivative-img10.webp',observation='첫 선분의 시작점이 대체설명에는(1,0)으로 적혀 있으나 실제 그림 눈금에서는(0,1)로 보인다.',action='좌표 충돌을 기록하고 자체 과제는 명시한 식으로 구성했다. 출판 정오표의 공식 정정은 확인하지 않았다.')]),
 F:dict(stem='openstax-ftc',sha='7ef62f4b28ce316524985288945f7c0b5aa91cea2ce9c8e8cbb88025aab42982',images=11,
  scope='5.3절 웹본문 전체·정리5.3~5.5와 증명·예5.15~5.22·확인5.14~5.20·학생 프로젝트7문항·연습144~206, 그림5.26~5.31과 연습 그래프5개',
  reading_log=['공식5.3절의 도입·목표·정리5.3~5.5와 증명·예5.15~5.22·확인5.14~5.20·학생 프로젝트의7문항·연습144~206을 모두 읽었다. 연습63개의 해답 전체를 독립 검산한 것은 아니다.',
   '그림5.26~5.31의6개 자산과 연습160~163·202의5개 그래프, 합계11개를 각각 시각적으로 확인했다. 연습160~163에서 그래프는 피적분함수가 아니라 누적함수임을 구별했다.',
   '정리5.4의 연속인 피적분함수·구간 내부 미분, 정리5.5의 전체 구간 조건·원시함수 끝점 차, 합성함수의 변화율·부호 있는 적분과 넓이를 확인했다.',
   '예5.17의1/(t³+1)은 적분 경로 전체가 특이점−1을 피해야 하므로∫₁ˣ의 보통 정의역은x>−1임을 확인했다. 자체 과제는1/t²로 변형했다.',
   '평균값 정리의a<b와 연속 조건을 유지했다. 학생 프로젝트의 낙하 모델은 읽은 수학적 모형이며 실제 실험이나 안전 지침으로 사용하지 않았다. 외부 매체는 실행하지 않았다.'],
  corrections=[dict(kind='source_condition_qualification',location='5.3절 정리5.4 뒤의 설명 문단',observation='적분가능한 함수라면 원시함수를 갖는다는 설명은 앞 정리의 연속 조건을 생략하면 지나치게 넓게 읽힌다. 정리5.4 자체에는 연속 조건이 명시되어 있다.',action='자체 설명에는 연속이라는 충분조건과 구간 내부를 명시했다. 교사용 조건 점검: g(t)=0(t<0),1(t≥0)이면 G(x)=∫₋₁ˣg(t)dt=max(x,0)이고0에서 좌우 미분계수0·1로 다르다. 적분가능만으로 모든 점의G′=g를 보장하지 않는다. 모든 불연속점에서 반드시 미분 불가능하다는 결론이나 연속이 모든 형태의 기본정리에 필요하다는 결론은 내리지 않는다. 이 반례를 미적분Ⅰ 학생의 필수 불연속 적분 과제로 추가하지 않는다.')])}

# Each mapping is tied to the actual authored high-school revision, rather than a primary-school family.
MAPPINGS=[
 ('OD01',D,[I+'02-01',I+'02-02'],['3.1절 미분계수 정의·식3.1~3.2','예3.1~3.4·3.6~3.7'],
  '차분몫은h≠0이고a+h가 정의역에 있을 때 구성하며, 유한한 양쪽 극한과 함수의 연속을 구별한다. 수치 표나 확대 그래프는 추정을 돕지만 극한 존재의 증명은 아니다.',
  '교재의 예시를 국내 학생의 발달 순서·효과 검증으로 사용하지 않는다. 보통의 유한한 미분계수와 수직 접선을 구별하며, 연속이면 언제나 미분가능하다고 결론짓지 않는다.'),
 ('OD02',D,[I+'02-05'],['3.1절 접선 정의·그림3.2~3.3','예3.2·그림3.6'],
  '접선은 접점과 그 점의 미분계수로 정한다. 곡선을 가로지르는x³의 원점 접선도 가능하므로 접선 여부를 곡선과 만나는 횟수나 한쪽에 놓이는 외관으로만 판정하지 않는다.',
  '한 점의 기울기만으로 직선의 위치가 정해지지 않는다. 원의 접선 성질을 일반 함수에 그대로 옮기거나 그림의 해상도만으로 접선을 증명하지 않는다.'),
 ('OD03',D,[I+'02-10',I+'03-06'],['3.1절 Velocity and Other Rates of Change·식3.3~3.8','예3.5·3.8~3.10'],
  '위치 변화의 평균변화율과 순간속도를 구별하고 위치·시간·속도·가속도의 단위를 유지한다. 자체 왕복 예에서는 부호 있는 속도·변위와 속력·이동거리도 별도로 확인한다.',
  '왕복 거리 과제는 자체 확장이다.3.1절만으로 적분에 의한 거리 계산을 모두 지원한다고 표시하지 않는다. 유한 평균가속도 표는 순간가속도의 단조성이나 실제 운동의 측정 결과가 아니다.'),
 ('OF01',F,[I+'03-04'],['5.3절 정리5.4와 증명','예5.15~5.17·확인5.14~5.15'],
  '연속인f에 대해F(x)=∫ₐˣf(t)dt를 두면 구간 내부에서F′(x)=f(x)이다. 누적함수의 값과 그 기울기를 구별하며, 원시함수 끝점 차에서는 같은 적분상수가 상쇄된다.',
  '연속은 여기서 사용하는 충분조건이다. 적분가능하다는 사실만으로 모든 점에서F′=f가 성립한다고 확대하지 않는다. 미적분Ⅰ에서 구분구적·불연속 적분을 새 필수 선수 내용으로 추가하지 않는다.'),
 ('OF02',F,[I+'03-03',I+'03-05'],['5.3절 정리5.5·예5.19~5.22','그림5.26~5.27·5.30~5.31'],
  '정적분은 부호 있는 누적이며 기하적 넓이와 구별한다. 부호가 바뀌는 곳에서 구간을 나누어 넓이를 구하고, 원시함수의 위끝값에서 아래끝값을 뺀다.',
  '정적분이0이라고 영역이나 이동이 없다고 결론짓지 않는다. 연습160~163의 누적함수 그래프 높이를 피적분함수 값으로 읽지 않는다. 구간 방향과 함수 부호를 유지한다.'),
 ('OF03',F,[II+'02-05',II+'03-01'],['5.3절 예5.18·확인5.16','연습166~179'],
  '적분의 위끝이u(x)이면 누적함수와u의 합성으로 보고f(u(x))u′(x)를 구한다. 자체 다항 예에서 원시함수 대입 후 미분하는 경로와 비교하고 음의x에서도 안쪽 변화율의 부호를 유지한다.',
  '안쪽 도함수를 생략하지 않는다. 해당 입력과 적분 경로의 정의역 조건을 먼저 확인한다. 이 연결을 학생의 보편적인 선수 숙달 순서나 자체 과제의 효과 근거로 사용하지 않는다.'),
 ('OF04',F,[II+'03-01'],['5.3절 정리5.5의 가정과 증명','예5.17의 정의역·예5.22의 부호 구분'],
  '끝점 차 공식은 적분 경로 전체에서 정리의 조건을 만족할 때 적용한다.1/t²의 원시함수가 양·음 구간에 각각 존재해도∫₁ˣ의 구간이0을 가로지르면 보통의 유한 정적분으로 계산할 수 없다.',
  '자체1/t² 예는 적용 구간을 확인하는 변형이다. 원시함수의 두 끝값만 존재한다는 이유로 중간 특이점을 무시하지 않는다. 이상적분·주값 계산을 교육과정의 필수 과제로 추가하지 않는다.')]

OBSERVATIONS={D:[
 dict(id='OD-P1',standard_codes=[I+'02-01',I+'02-02'],question='f(x)=x²의x=2에서 차분몫을 구하라. h=0일 때 몫과h→0일 때 극한을 구별하라. 이어g(x)는x≠2에서x²이고g(2)=5다. 같은 주변 값 표를 보고g′(2)도 같다고 할 수 있는가?',
  expected='f의 차분몫은h≠0에서4+h이고 극한은4다. 원래 몫에h=0을 대입할 수 없다. g의 몫은4+h−1/h이므로 유한한 양쪽 극한이 없다. 점의 값이 달라지면 같은 주변 표만으로 같은 미분계수를 결론낼 수 없다.',
  interpretation='대입·극한·점의 함수값을 따로 기록한다. 유한 표의 수치 접근만으로 극한의 존재를 확정하지 않는다. 교사가 먼저 약분이나g(2)를 알려 준 경우 그 전후 응답을 구별한다.',student_validated=False),
 dict(id='OD-P2',standard_codes=[I+'02-02',I+'02-05'],question='p(x)=|x|와q(x)=x³를x=0에서 비교하라. 각각의 연속과 미분가능을 차분몫으로 판단하고, q의 원점 접선이 곡선을 가로지르므로 접선이 아니라는 말을 검토하라.',
  expected='둘 다0에서 연속이다. p의 차분몫은왼쪽−1·오른쪽1이어서 미분 불가능하다. q의 몫은h²→0이므로q′(0)=0이고 접선은y=0이다. 이 접선은 곡선을 가로질러도 접선이다.',
  interpretation='함수값의 극한과 차분몫의 극한, 접점과 접선 기울기를 구별한다. 접선은 곡선과 오직 한 번 만나야 한다거나 절대로 가로지르면 안 된다는 조건을 추가하지 않는다. 한 반례의 정답으로 논리 이해 전체를 판정하지 않는다.',student_validated=False),
 dict(id='OD-P3',standard_codes=[I+'02-10',I+'03-06'],question='가상 직선 운동에서0≤t≤2초의 위치는s(t)=(t−1)²m다. 평균속도와t=0.5초·1.5초의 순간속도, 전체 이동거리와 평균속력을 구하라. 출발·도착 위치가 같으면 움직이지 않았다는 말도 검토하라.',
  expected='s(0)=s(2)=1m이므로 평균속도는0m/s다. v(t)=2(t−1)m/s이므로두 순간속도는−1m/s와1m/s다.1m에서0m로 갔다가1m로 돌아와 이동거리는2m·평균속력은1m/s다. 변위0은 정지했다는 뜻이 아니다.',
  interpretation='평균속도·순간속도·속력·시간 단위·방향 전환을 각각 기록한다. 거리 비교는 자체 확장이며 실제 측정이나 해당 교재3.1절의 적분 수업 효과를 나타내지 않는다.',student_validated=False)],
 F:[
 dict(id='OF-P1',standard_codes=[I+'03-04'],question='연속함수f(t)=3t²−1에 대해F(x)=∫₀ˣf(t)dt라 하자. 원시함수로F를 구하고F(0)·F(1)과F′(0)·F′(1)을 비교하라. 누적값이 같으면 그곳의 기울기도 같다는 말을 검토하라.',
  expected='F(x)=x³−x이며F(0)=F(1)=0이다. F′(x)=3x²−1이므로F′(0)=−1·F′(1)=2다. 같은 누적값도 서로 다른 기울기를 가질 수 있다. f가 연속이고 해당 점이 적분함수를 정의한 구간 내부일 때 기본정리를 적용한다.',
  interpretation='원시함수·누적값·피적분함수 값·기울기를 구별한다. 적분가능만으로 모든 점의 미분 관계를 보장한다고 확대하지 않는다. 불연속 반례는 교사용 조건 점검으로 따로 두며 새 학생 필수 과제로 요구하지 않는다.',student_validated=False),
 dict(id='OF-P2',standard_codes=[I+'03-03',I+'03-04',I+'03-05'],question='f(t)=2t−2의[0,2] 정적분과 그래프·t축 사이 넓이를 각각 구하라.0에서1까지와1에서2까지를 나누어 부호를 설명하고,∫₀¹f(t)dt와∫₁⁰f(t)dt도 비교하라.',
  expected='[0,1]의 적분은−1·[1,2]의 적분은1이므로전체 정적분은0이다. 두 삼각형 넓이는각1이어서 넓이 합은2다. ∫₁⁰f(t)dt=1로∫₀¹의부호가 바뀐다. 누적의 상쇄와 영역이 없는 것을 구별한다.',
  interpretation='영점1·구간 방향·부호 있는 누적·양의 넓이를 따로 기록한다. 전체 적분이0인 대칭 사례만으로 방향 전환의 부호를 확인하지 않고,0이 아닌 부분 적분도 비교한다.',student_validated=False),
 dict(id='OF-P3',standard_codes=[II+'02-05',II+'03-01'],question='H(x)=∫₁^(x²)(t+1)dt의 도함수를 합성함수 미분과 원시함수 대입 후 미분의 두 방법으로 구하라. x=−1과1에서 값을 비교하고 음의x도 허용되는지 설명하라.',
  expected='H(x)=x⁴/2+x²−3/2이고H′(x)=2x(x²+1)이다. 두 방법이 같으며H′(−1)=−4·H′(1)=4다. 피적분함수가 다항함수이므로 모든 실수x의 적분 구간에서 정의된다. 위끝x²는 같아도 안쪽 변화율2x의 부호가 다르다.',
  interpretation='f(x²)와f(x²)·2x를 구별하고 도함수 평가점을 유지한다. 음의x를 적분 위끝의 음수 여부와 혼동하지 않는다. 교사가2x를 알려 준 후의 성공은 독립 수행과 따로 남긴다.',student_validated=False),
 dict(id='OF-P4',standard_codes=[II+'03-01'],question='J(x)=∫₁ˣ1/t²dt를 보통의 유한 정적분으로 정의하려 한다. 허용되는x를 찾고 그 구간에서J와J′를 구하라. x=−1에서 원시함수 끝점 차만 계산해2라고 해도 되는가?',
  expected='허용 범위는x>0이다. 그 범위에서J(x)=1−1/x이고J′(x)=1/x²다. x=−1이면 적분 구간이함수가 정의되지 않는0을 가로지른다. 두 끝값의 차2를 구해도 보통의 유한 정적분 값이라고 할 수 없다.',
  interpretation='두 끝점의 정의 여부와 경로 전체의 조건을 구별하는 자체 확장이다. 음의 구간 자체에는 원시함수가 있더라도1에서 그 구간까지0을 가로지를 수 없다. 이상적분·주값의 계산을 요구하지 않는다.',student_validated=False)]}

def main():
 registry=load_registry()
 if all(s in registry['sources'] for s in CONFIG):
  print('Reviewed sources and targets remain current; no automatic refresh');build_report();return
 assert not any(s in registry['sources'] for s in CONFIG),'Review the partially recorded batch explicitly'
 sources=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))
 queue=json.loads((ROOT/'data/content_review_queue.json').read_text(encoding='utf-8'))
 assets=json.loads((ROOT/'tmp/literature/openstax-calculus-image-provenance.json').read_text(encoding='utf-8'));assert len(assets)==23
 for sid,cfg in CONFIG.items():
  assert hashlib.sha256((ROOT/f"tmp/literature/{cfg['stem']}.html").read_bytes()).hexdigest()==cfg['sha']
  figures=[a for a in assets if a['file'].startswith(cfg['stem']+'-img')];assert len(figures)==cfg['images']
  for a in figures:assert hashlib.sha256((ROOT/'tmp/literature'/a['file']).read_bytes()).hexdigest()==a['sha256']
  b=next(b for b in sources if b['id']==sid);previous=dict(b);url=b['url']
  b.update(review_scope=cfg['scope']+' 전체 읽기·모든 삽입 자산 시각 확인. 연습 해답 전체 검산·책 전권·PDF 판면·외부 매체 실행은 별도.',next_review='교재 다른 절과 연결되는 적용 조건, 출판 정오표·판본 변경은 추가 대조 대상. 자체 과제의 독립 검토와 실제 학생 응답 검증은 별도.')
  notes=dict(source_id=sid,source_url=url,source_asset_kind='publisher_html',source_asset_sha256=cfg['sha'],source_asset_redistributed=False,date='2026-11-04',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,reading_log=cfg['reading_log'],source_corrections=cfg['corrections'],observed_image_assets=figures,
   interpretation_limits=['수학 교재의 설명과 예시를 실제 학생 반응·학습 효과·국내 인지 발달 순서의 실증으로 사용하지 않는다.','두 절의 웹본문과 삽입 자산을 읽었으며 원책 전권·PDF 판면·연습 해답 전체를 검증한 것이 아니다.','교육과정Ⅰ·Ⅱ의 범위를 유지한다. 구분구적·불연속 함수 적분·이상적분을 미적분Ⅰ의 필수 선수로 추가하지 않는다.'])
  file=ROOT/f'data/literature_evidence/{sid}_review_notes.json';file.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  registry['sources'][sid]=dict(source_id=sid,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-04',snapshot_kind='authored_review_notes',snapshot_file=file.relative_to(ROOT).as_posix(),snapshot_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),source_asset_kind='publisher_html',source_asset_sha256=cfg['sha'],redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,
   display=dict(title=b['title'],url=url,authors_year='OpenStax,Calculus Volume1,2016／확인한 공식 웹본문'),read_scope=cfg['scope'],scope_note='공식 교재의 수학적 설명·정리·예시를 대조했다. 웹본문과 삽입 그림을 읽은 범위이며 PDF 판면이나 책 전권의 검토와 구별한다.',method_note='차분몫과 연속, 접선·속도 또는 누적·기울기·넓이·합성·정의역의 조건을 원문 수식 및 그림과 대조했다. 모든 연습문항을 읽되 해답 전체를 독립 검산한 것은 아니다. 자체 과제는 별도 계산으로 확인한다.',limits='수학적 설명을 지원하는 교재다. 실증적 교수 효과·진단 타당성·보편적 선수 숙달 순서·현재 국내 학생의 반응을 입증하지 않는다. 원격 원문의 이후 변경을 실시간 확인하지 않는다.',editorial_action=('극한·연속·접선·순간/평균속도 주장3건과 자체 관찰3건을 보완.' if sid==D else '연속 조건·부호 있는 적분·합성의 변화율·경로 전체 정의역 주장4건과 자체 관찰4건을 보완.')+'원문 관찰 충돌과 자체 적용 조건을 읽기 기록에 보존. 독립 검토·학생 검증은 완료로 표시하지 않음.',independent_review=False,student_validated=False,observations=OBSERVATIONS[sid])
  for cid,source,codes,locations,support,limit in MAPPINGS:
   if source!=sid:continue
   targets=['revision:'+code for code in codes]
   registry['claims'].append(dict(id=cid,source_id=sid,role='mathematical_explanation',locations=locations,support=support,does_not_establish=limit,target_snapshots={t:digest(target_value(t)) for t in targets},standard_codes=codes,independent_review=False,student_validated=False))
  row=next(r for r in queue['literature_review'] if r['source']['id']==sid)
  row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[m[0] for m in MAPPINGS if m[1]==sid])
 for path,value in [('data/sources.json',sources),('data/literature_claim_reviews.json',registry),('data/content_review_queue.json',queue)]:
  (ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 load_registry();build_report()
if __name__=='__main__':main()

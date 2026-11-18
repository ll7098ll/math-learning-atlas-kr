"""Extend a scoped GAISE reading; preserve earlier notes, claims and source asset."""
import copy
import hashlib
import json
from fractions import Fraction
from statistics import median
from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews
from record_gaise_level_a_review import SOURCE, URL, SHA, NOTES as PRIOR_NOTES

NOTES='data/literature_evidence/GAISE_2020_level_b_review_notes.json'
PRIOR_SHA='dbe0c4b6fb3c4ac919d60d715f20441c77db91a9d6a2fda0dc04e7712829cc1f'
CURRENT_URL='https://www.amstat.org/docs/default-source/amstat-documents/gaiseiiprek-12_full.pdf'
CURRENT_SHA='01bddb5f52750e3c698e2610fa12e04861db1b1740e684660283ea43cf6b01db'
NEW_TEXT=list(range(7,21))+list(range(50,79))
NEW_VISUAL=[16,55,57,58,59,60,61,63,64,65,66,67,68,69,70,74,76]

MAPPINGS=[
 ('G2B01',['9수04-03','12실통02-03'],['인쇄46–51 / PDF54–59'],
  '한 가지 최선호와 복수 선호를 구별하고,집단 크기가 다른 비율과 합친 비율의 분모를 명시하는 자체 활동에 참고한다.',
  '복수응답의 범주별 비율을 배타적인 원그래프 조각으로 만들지 않는다. 큰 표본이나 두 학급 합산만으로 학교 전체의 대표성을 입증하지 않는다.'),
 ('G2B02',['12확통02-04'],['인쇄51–53 / PDF59–61'],
  '조건 집단·교집합·전체를 구별하고 역조건의 분모가 달라짐을 확인하는 자체 가상 분할표에 참고한다.',
  '원문 일부 조건 설명과 모자이크 그림의 변수 표기는 주변 설명과 맞지 않아 전용하지 않는다. 비율 차는 퍼센트포인트로 쓰며 관찰된 연관을 인과로 바꾸지 않는다.'),
 ('G2B03',['9수04-08','12실통02-04'],['인쇄54–59 / PDF62–67'],
  '분포의 중심·전체 범위·중간 절반의 폭을 별도로 비교하고,사분위수·수염 규칙을 기록하는 자체 활동에 참고한다.',
  '상자 중첩의 비형식적 비교를 정식 유의성 판정 규칙으로 사용하지 않는다. MAD는 여기서 평균으로부터의 절대편차 평균이며 국내 새 필수 공식으로 넣지 않는다. 원자료 없이 원문 요약값을 재현했다고 하지 않는다.'),
 ('G2B04',['9수04-09','12실통02-03'],['인쇄59–62 / PDF67–70'],
  '같은 대상의 짝·축 단위·범위와 선형 여부를 보존하고,시간별 집단 평균을 개체 성장과 구별하는 발문에 참고한다.',
  'QCR과 Pearson 계수를 동일시하지 않고 QCR은 교사용 확장으로만 다룬다. 원문54개 분모와59개 MGF 표본의 관계는 원자료 미확인으로 보류한다. 연결선·평균 변화만으로 미측정 값·개체 성장·원인을 확정하지 않는다.'),
 ('G2B05',['12실통01-02','12실통02-02'],['인쇄63–67 / PDF71–75'],
  '사진도 자료가 될 수 있지만 사진·가구의 단위와 참여·선택·분류 기준을 확인해야 한다는 자체 활동에 참고한다.',
  '원문의300가구 등은2020년 서술의 역사적 수치다. 사진 수를 독립 가구 표본 수로 세거나 외모·사진만으로 가족관계·소득을 확정하지 않는다. 원 사이트·월소비 추정의 원설명·영상은 미검토다.'),
 ('G2B06',['12실통02-02'],['인쇄1–12 / PDF9–20','인쇄67–69 / PDF75–77'],
  '질문·측정·수집과 결론 범위를 맞추며 무작위표집과 무작위배정을 구별하는 자체 설계 비교에 참고한다.',
  'A/B/C를 고정 한국 학년으로 대응하지 않는다. 예시 실험은 현재 수업 효과의 증거가 아니다. 무작위배정이 각 집단의 사전 능력을 반드시 같게 만들거나 모집단 일반화를 보장하지 않는다. 짝·홀 비율만으로 주사위 여섯 면의 공정성을 증명하지 않는다.')
]

OBSERVATIONS=[
 dict(id='GB-P1',standard_codes=['9수04-03','12실통02-03'],
  question='가상1반10명에게A와B 각각의 선호를 묻자A8명·B6명이다.80%와60%의 합140%는 오류인가? 같은 문항의2반30명 중A12명을 더하면 전체A 비율은60%인가?',
  expected='복수 선호를 허용하므로 두 비율의 합140%는 가능하고 한 사람의 중복 선택을 뜻할 수 있다. 두 비율을 배타적인 원그래프 조각으로 쓰지 않는다. 전체A는(8+12)/(10+30)=20/40=50%다.80%와40%의 단순 평균60%는 두 학급에 같은 가중을 준 다른 요약이다.',
  interpretation='응답자 수·선택 수·범주별 분모·학급 가중을 따로 설명하게 한다. 문항당 누락 없이10명과30명 모두 응답한 가정이다. 가상 계산이며 학교 전체의 대표성이나 실제 학생 반응을 입증하지 않는다.',student_validated=False),
 dict(id='GB-P2',standard_codes=['12확통02-04'],
  question='가상30명의 두 예/아니오 응답을 행B예·B아니오,열A예·A아니오의 표[[12,3],[4,11]]로 기록했다. 이30명 중 한 명을 같은 가능성으로 뽑을 때P(B|A),P(A|B),P(A∩B)를 비교하라.',
  expected='A예는16명,B예는15명,두 예는12명이다. P(B|A)=12/16=75%,P(A|B)=12/15=80%,P(A∩B)=12/30=40%다.75%와80%의 차는5퍼센트포인트이며 같은 분모의 비율이 아니다.',
  interpretation='조건 사건을 먼저 말하고 표에서 그 집단만 테두리 친 뒤 분모를 적는다. 둘의 연관과 원인 주장을 구별하고 조건 집단이0명이면 조건부확률을 정의하지 않는다. 가상 표이며 실제 설문이나 학생 검증 자료가 아니다.',student_validated=False),
 dict(id='GB-P3',standard_codes=['9수04-08','12실통02-04'],
  question='같은 단위의 가상 자료A=[0,4,4,4,4,4,4,8],B=[1,2,3,4,5,6,7,8]을 비교하라. 하위·상위 네 값 각각의 중앙값을Q1·Q3로 정하고,전체 범위가 더 크면 사분위범위도 더 큰지 설명하라.',
  expected='A의 범위8,Q1=4,Q3=4,사분위범위0이다. B의 범위7,Q1=2.5,Q3=6.5,사분위범위4다. 전체 범위는A가 크고 중간 절반의 폭은B가 크다. 퍼짐이라는 말만으로 비교 순위를 하나로 정할 수 없다.',
  interpretation='비교할 요약의 정의·단위·사분위수 관례를 먼저 적는다. 수염을 최솟값·최댓값까지 그리는 관례와1.5IQR 규칙의 수염을 구별하며,극단값을 이유 없이 삭제하지 않는다. 가상 자료이고 정식 유의성 검정이나 학생 반응 기록이 아니다.',student_validated=False),
 dict(id='GB-P4',standard_codes=['9수04-09','12실통02-03'],
  question='가상 짝 자료(1,1),(2,4),(3,9),(4,16)를 같은 대상ID로 산점도에 나타내라. y축의 표시 범위를 바꾸면 원자료나 직선 위에 있는지가 달라지는가? 교사용 확장으로 두 중앙선의 사분면 부호 요약만으로 직선성을 보장할 수 있는가?',
  expected='짝과 수치는 그대로이고 양의 경향이지만 점들은 한 직선 위에 있지 않다. 이웃 기울기는3·5·7로 다르다. 중앙선x=2.5,y=6.5에서는 네 점 모두 제1·제3영역에 있어 이 축 위 점이 없는 자체 예의QCR은1이지만 완전한 직선 관계는 아니다.',
  interpretation='축의 눈금·단위·관측값과 시각 인상을 대조한다. QCR 계산은 교사용 반례 확인이고 중등 학생에게 필수 상관계수로 요구하지 않는다. 다른 자료의 중앙선 위 점은 처리 규칙·분모를 먼저 정한다. 가상 예이며 원자료 수집·인과·학생 검증은 아니다.',student_validated=False),
 dict(id='GB-P5',standard_codes=['12실통01-02','12실통02-02'],
  question='가상 참여 가구A·B·C·D의 현관문 사진이 각각10·2·2·2장이다. A만 나무문이고 나머지는 금속문이라면 나무문 가구 비율은10/16인가? 이 네 참여 가구의 결론을 세계 모든 가구로 일반화할 수 있는가?',
  expected='사진을 세면 나무문 사진은10/16=62.5%지만,가구별 문 종류를 하나로 정의한 이 예에서 나무문 가구는1/4=25%다. 사진16장은 독립 가구16곳이 아니다. 네 가구의 참여·선정 방식 정보만으로 세계 가구 비율을 추정하지 않는다.',
  interpretation='관찰 단위·대상ID·중복 사진·가구당 분류 규칙을 기록한다. 실제 사진을 다룰 때는 촬영·사용 동의와 관찰 가능한 특징·추정한 배경을 구별한다. 사진 자체는 제시하지 않은 가상 기록이며 실제 가족관계·소비·학생 반응 자료가 아니다.',student_validated=False),
 dict(id='GB-P6',standard_codes=['12실통02-02'],
  question='가상 연구계획에서 한 반30명을15명씩 무작위배정해 같은 단어 목록을 음악·무음 조건으로 비교한다. 다른 계획은 학교에서30명을 무작위표집하고 원래 음악을 듣는 학생과 듣지 않는 학생을 비교한다. 어느 무작위 절차가 일반화와 처리 효과 비교를 돕는가?',
  expected='첫 계획의 배정은 처리 비교의 교란 통제를 돕지만 반 자체가 무작위표본은 아니다. 둘째 계획의 표집은 학교 모집단으로의 추론을 돕지만 원래의 청취 선택에는 능력·습관 등 교란이 남는다. 어느 절차도 사전 능력의 정확한 같음이나 결과를 보장하지 않는다. 실제 효과 판정에는 시행 절차·누락·변이·분석을 추가 확인해야 한다.',
  interpretation='표집→배정→측정→응답완료를 따로 표시하고 동의·측정시간·조건 간 간섭을 점검한다. 원문 예의 요약값을 현재 설계의 관측 결과로 사용하지 않는다. 실행하지 않은 가상 계획이며 실제 학생 수집·효과·독립 검토를 추가하지 않는다.',student_validated=False)
]

def verify():
 assert len(NEW_TEXT)==43 and len(NEW_VISUAL)==17 and set(NEW_VISUAL)<=set(NEW_TEXT)
 assert Fraction(8+12,10+30)==Fraction(1,2) and (Fraction(8,10)+Fraction(12,30))/2==Fraction(3,5)
 assert Fraction(12,16)==Fraction(3,4) and Fraction(12,15)==Fraction(4,5) and Fraction(12,30)==Fraction(2,5)
 for v,expected in [([0,4,4,4,4,4,4,8],(8,0)),([1,2,3,4,5,6,7,8],(7,4))]:
  assert (max(v)-min(v),median(v[4:])-median(v[:4]))==expected
 pairs=[(1,1),(2,4),(3,9),(4,16)]
 assert [pairs[i+1][1]-pairs[i][1] for i in range(3)]==[3,5,7]
 assert all((x-Fraction(5,2))*(y-Fraction(13,2))>0 for x,y in pairs)
 assert Fraction(10,16)!=Fraction(1,4)
 assert sum([Fraction(1,10),Fraction(2,10),Fraction(1,10),Fraction(2,10),Fraction(3,10),Fraction(1,10)])==1
 assert Fraction(2+2+1,10)==Fraction(1,2)
 assert 36+4+5+9==54 and Fraction(36,41)-Fraction(4,13)==Fraction(304,533)
 assert (Fraction(36,41)-Fraction(4,13))/Fraction(4,13)==Fraction(76,41)
 assert Fraction(44-10,54)==Fraction(17,27) and 2012-1973==39

def new_guards():
 return [
  dict(kind='conditioning_wording_and_plot_label_guard',location='인쇄51–53 / PDF59–61',table_rows_RB_yes_no_columns_Rap_yes_no=[[36,4],[5,9]],
   action='36/41과4/13은Rap예/아니오 각각에서R&B예 비율이다. PDF60의 일부 문장은 조건 방향을 뒤집고,그림8의 축 변수명은 열 너비와 비율에 대한 본문 설명과 맞지 않는다. PDF61의 역조건36/40과 구별한다. 원그림·문장을 복제하지 않고 자체 표에서 조건·분모를 명시한다. 공식 정오표는 확인하지 못했다.'),
  dict(kind='percentage_point_guard',location='인쇄53 / PDF61',exact_difference_percentage_points=str(100*Fraction(304,533)),relative_increase=str(Fraction(76,41)),
   action='88%와31%의 반올림 비율 차57은57퍼센트포인트로 표시한다. 정확한 차는약57.04퍼센트포인트이며31% 근처를 기준으로 한 상대 증가와 다르다.'),
  dict(kind='dispersion_definition_guard',location='인쇄56–59 / PDF64–67',
   action='부리 길이의 전체 범위MGF4.03·CF3.2와IQR1.03·1.24는 비교 순서가 다르다. MAD의 기준은 평균이며 중앙값 절대편차·표준편차와 구별한다. PDF66말미의길이 표현은앞의깊이 질문과 구별하고 원자료 없는 재계산·형식 검정은 주장하지 않는다.'),
  dict(kind='qcr_denominator_guard',location='인쇄54·60–61 / PDF62·68–69',reported_MGF_n=59,reported_quadrant_counts=[44,10],reported_qcr_denominator=54,
   action='중앙선 위 점의 처리와 원자료는 미확인이다.59와54의 차5를 자동으로 축 위 점 수나 누락 오류라고 확정하지 않는다. QCR은Pearson 계수나 직선성의 보장이 아니며 국내 새 필수 공식으로 넣지 않는다.'),
  dict(kind='time_window_and_aggregate_guard',location='인쇄62 / PDF70',figure_years=[1973,2012],elapsed_years=39,source_prose_years=35,
   action='그림17·18의1973–2012와 본문35년 표기는 맞지 않아35년 서술을 전용하지 않는다.39년 간격과 모든 해가 포함될 때40개 연도 표지를 구별한다. 실제 관측 연도 수·연도별 표본 수·같은 개체의 성장은 원자료 없이 확정하지 않는다.'),
  dict(kind='historical_photo_sample_guard',location='인쇄63–67 / PDF71–75',
   action='300가구·56개국 등의 수는2020년 서술 범위로 제한한다. 사진을 독립 가구 수로 세거나 외형만으로 가족관계·소비를 확정하지 않는다. 소비 추정의 원설명·사진 원자료·영상은 열람하지 않았다.'),
  dict(kind='probability_model_guard',location='인쇄9–10 / PDF17–18',
   action='짝수 비율이 공정 주사위와 맞는다고 여섯 면이 동등하다는 증명은 아니다. 자체 모형(0.1,0.2,0.1,0.2,0.3,0.1)도짝수확률은1/2다. 원문은 차이가 크면 의심할 수 있다고 설명하며 일치가 공정성의 증명이라고 주장하지 않는다.10회 묶음100개의 뜻을100회 단일 시행과 혼동하지 않는다.'),
  dict(kind='experimental_example_and_whisker_guard',location='인쇄67–68 / PDF75–76',
   action='원문은예시자료라고명시한다. 음악/무음 중앙값7/10·IQR3/4의 차이를 실제 현재 수업 결과로 옮기지 않는다. 그림28의음악최대15는별도점이며수염끝과최댓값을동일시하지 않는다. 배정과 표집의 결론 범위를 구별한다.')
 ]

def main():
 verify();registry=load_registry();prior=copy.deepcopy(registry['sources'][SOURCE]);before=copy.deepcopy(load_reviews()['records'])
 old_claims=copy.deepcopy([c for c in registry['claims'] if c['source_id']==SOURCE])
 ids={m[0] for m in MAPPINGS};existing={c['id'] for c in registry['claims']}
 if ids<=existing:
  assert {p['id'] for p in OBSERVATIONS}<={p['id'] for p in prior['observations']}
  build_report();print('GAISE Level B scope remains current; no automatic refresh');return
 assert not ids&existing
 assert prior['snapshot_file']==PRIOR_NOTES and prior['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 assert hashlib.sha256((ROOT/'tmp/literature/GAISE_2020.pdf').read_bytes()).hexdigest()==SHA
 assert hashlib.sha256((ROOT/'tmp/literature/GAISE_2020_current_official.pdf').read_bytes()).hexdigest()==CURRENT_SHA
 old_pages=json.loads((ROOT/'tmp/literature/GAISE_2020_pages.json').read_text(encoding='utf-8'))
 new_pages=json.loads((ROOT/'tmp/literature/GAISE_2020_current_official.pages.json').read_text(encoding='utf-8'))
 changed=[a['pdf_page'] for a,b in zip(old_pages,new_pages) if ''.join(a['text'].split())!=''.join(b['text'].split())]
 assert len(old_pages)==len(new_pages)==126 and not changed
 old_notes=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'))
 images=[]
 for p in NEW_VISUAL:
  f=ROOT/f'tmp/literature/GAISE_2020-p{p}.png'
  images.append(dict(pdf_page=p,local_temporary_file=f.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 notes=dict(source_id=SOURCE,source_url=URL,source_pdf_sha256=SHA,date='2026-11-06',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,
  previous_review=prior,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,
  pdf_pages_total=126,read_pdf_pages=list(range(3,79)),new_read_pdf_pages=NEW_TEXT,
  visually_reviewed_pages=old_notes['visually_reviewed_pages']+images,new_visually_reviewed_pages=images,
  official_asset_comparison=dict(url=CURRENT_URL,sha256=CURRENT_SHA,pages=126,whitespace_normalized_text_changed_pdf_pages=changed,method='전체126쪽의 추출 텍스트 공백 정규화 비교다. 새 파일의 픽셀·그림 동등성이나 미독 장의 독해를 입증하지 않는다. 실제 읽기·이미지는 기존SHA 원문에 묶고 기본 출처 해시는 교체하지 않았다.'),
  source_corrections=old_notes['source_corrections']+new_guards(),
  reading_log=['기존PDF3–6·21–49의33쪽 텍스트·16쪽 이미지 검토를 이전 기록으로 보존했다.',
   '이번에는PDF7–20과50–78의43쪽을 읽었다. 감사·서문·도입·Level B 목차·본문9예·요약과 빈8·12·50·78쪽을 포함한다. PDF79의C목차 확인은 누적 본문 범위에 합산하지 않았다.',
   '선정17쪽 전체 페이지 이미지를 직접 확인했다. 누적 텍스트 지정 범위는PDF3–78의76쪽,이미지는33쪽이다. 빈 쪽은 추출 텍스트가 비어 있음만 확인했고 이번 새 이미지17쪽에는 포함하지 않았다.',
   '표1·2·3·5·6·7,그림8·15·16·17·18·28의 수치·축·범례·분모를 본문과 대조하고 자체 수치 활동6건을 별도로 검산했다.'],
  unread_followups=['Level C 본문PDF80–111,Assessment PDF113–121,참고문헌PDF123–124와뒤표지·빈쪽PDF112·122·125–126은 미검토다. C목차PDF79의 확인은 C본문 독해가 아니다.',
   'More4U 접근은402로 본문 미확인이다. 인용 원연구·Dryad 원자료·소비 추정 원설명·영상·공식 정오표와 수치 불일치의 작성 의도는 미확인이다.'],
  interpretation_limits=old_notes['interpretation_limits']+['현재ASA 다른주소의PDF는추출본문이같았지만선정이미지를새파일로재대조하지않아기존출처해시를교체하지않았다.','추가6활동은가상자체설계다. 독립검토·실제학생응답·효과·도구화면실행완료를추가하지않는다.'])
 (ROOT/NOTES).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 path=ROOT/'data/sources.json';sources=json.loads(path.read_text(encoding='utf-8'));b=next(s for s in sources if s['id']==SOURCE)
 b.update(review_scope='126쪽PDF 중PDF3–78의76쪽 텍스트(서지·목차·빈 쪽 포함)와선정33쪽 이미지를 확인. 프레임워크·Level A/B와서문·도입의범위다. Level C·평가·참고문헌·More4U·원연구·원자료는미검토.',
  next_review='Level C·Assessment·참고문헌 본문,원연구·정오표·원자료와표/그림 수치 불일치,한국어과제의실제반응을추가대조한다.')
 review=registry['sources'][SOURCE]
 review.update(snapshot_file=NOTES,snapshot_sha256=hashlib.sha256((ROOT/NOTES).read_bytes()).hexdigest(),bibliography_snapshot=digest(b),
  snapshot_history=prior.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=prior['date'],read_scope=prior['read_scope'])],
  read_scope='PDF3–78의76쪽 텍스트(서지·목차·빈 쪽 포함),선정33쪽 이미지;프레임워크·Level A/B·서문·도입 범위',
  method_note='기존A의주장6건·관찰6건과읽기기록을보존하고새B주장6건·자체관찰6건을추가했다. 본문과선정표·그림을직접대조하고분모·비율차·범위·사분위범위·축·표집/배정을구별했다.',
  limits='전체126쪽독해가아니다. C본문·평가·참고문헌·More4U·원연구·원자료는미검토다. A수치불일치와B조건설명·그림변수명·시간 범위의불일치는전용을보류한다. QCR분모의원자료상원인과공식정오표는미확인이다. PDF·페이지이미지는재배포하지않는다.',
  editorial_action='기존8개기준의6주장·6관찰에B의6주장·6가상관찰을더했다. 복수응답·합산가중·조건분모·퍼짐의기준·짝과축·사진의관찰단위·표집과배정을보완했다. 관계승인·독립검토·실제학생검증수는늘리지않았다.',
  observations=prior['observations']+OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,
   target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 path=ROOT/'data/content_review_queue.json';queue=json.loads(path.read_text(encoding='utf-8'));row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE)
 row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE])
 path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert load_reviews()['records']==before
 assert old_claims==[c for c in load_registry()['claims'] if c['id'] in {c['id'] for c in old_claims}]
 build_report();print('Extended GAISE: 6 claims / 6 own observations; prior notes and relation records preserved')

if __name__=='__main__':main()

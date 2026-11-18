"""Bind an official HTML chapter reading without claiming a PDF or pupil validation."""
import hashlib,json
from literature_review import ROOT,digest,target_value,load_registry,build_report
SOURCE='NRC_MEASUREMENT_2001'
URL='https://www.nationalacademies.org/read/9822/chapter/10'
SHA='73e2387e821c7301794ae2f575b39870f3313ba979ade2edab538b7c1584cdbe'
NOTES='data/literature_evidence/NRC_MEASUREMENT_2001_review_notes.json'
MAPPINGS=[
 ('NB01','measure',['2수03-10','2수03-11','2수03-13','4수03-15','4수03-16'],['인쇄281–282 / Measurement and Geometry, Length Measure','미주75–86 / 인쇄297'],
  '측정 속성·동일 단위·단위의 반복과 간격을 구별하고,0이 아닌 시작점에서도 두 위치 사이의 길이를 설명하도록 하는 설계에 참고한다.',
  '눈금을 읽는 한 반응이나 보존 과제의 성공을 측정 이해 전체로 판정하지 않는다. 인용 연구의 학년·개입 결과를 현재 한국 학생의 규준·필수 순서로 옮기지 않는다.'),
 ('NB02','area',['6수03-12','6수03-13','6수03-14'],['인쇄281,283 / Area Measure','미주76,87–90 / 인쇄297'],
  '동일한 단위 넓이로 빈틈·겹침 없이 덮기, 배열 구조, 잘라 재배치할 때 보존되는 넓이와 달라질 수 있는 둘레를 함께 확인한다.',
  '정사각형만이 가능한 넓이 단위라고 정의하지 않는다. 서로 다른 크기의 조각 수를 그대로 넓이로 더하지 않는다. 길이·넓이 보존의 이해가 항상 하나의 고정 단계로 함께 발달한다는 결론도 내리지 않는다.'),
 ('NB03','volume',['6수03-18','6수03-19'],['인쇄284 / Volume Measure','미주91–92 / 인쇄297'],
  '삼차원 단위를 한 층의 배열과 층 수로 조직하고, 겉으로 보이는 면·외곽 치수와 실제로 채워진 내부를 구별하는 설계에 참고한다.',
  '부피 개념의 보편적인 연령별 순서를 확정하지 않는다. 가로×세로×높이는 빈틈 없이 채워진 직육면체 조건에서 사용하며 내부가 빈 물체의 재료 부피에 외형 공식을 그대로 적용하지 않는다.'),
 ('NB04','line',['4수03-24'],['인쇄284–287 / Developing Geometric Reasoning, Angle','미주93–128 / 인쇄297–298'],
  '각의 벌어진 정도·그려진 변의 길이·그림의 방향·회전량을 구별해 설명하고 조작과 정적인 그림을 연결하는 설계에 참고한다.',
  '한 그림이나 도구 조작의 성공을 모든 각 모델의 이해로 보지 않는다. 도형 사고를 나이에 고정된 한 단계로 분류하거나2001년의 도구 연구를 현행 도구의 효과 검증으로 바꾸지 않는다.'),
 ('NB05','equality',['4수02-03'],['인쇄261–263 / Representational Activities','인쇄270–275 / Transformational Activities','미주21–27,53–65 / 인쇄295–296'],
  '등호를 양쪽의 같은 값을 나타내는 관계로 보고, 계산의 순서와 참인 등식의 연결을 구별하는 설계에 참고한다.',
  '기호 변형의 정답만으로 의미 이해·장기 기억을 확정하지 않는다. 구체물·비형식 풀이·형식 풀이에 모든 학생이 따라야 할 단일 필수 순서를 부여하지 않는다.'),
 ('NB06','mean',['6수04-01'],['인쇄288–291 / Learning to Use Data, Organizing Data','미주135–152 / 인쇄298–299'],
  '평균 계산과 자료 전체의 대표,0인 값과 누락된 값, 같은 평균을 가진 서로 다른 자료를 구별하는 설계에 참고한다.',
  '자료 읽기·표현·해석을 한 능력으로 묶지 않는다. 평균이 언제나 가장 좋은 대표값이라고 하거나 한 계산의 성공으로 자료 해석까지 검증했다고 보지 않는다. 다른 대표값을 초등 필수 내용으로 추가하지 않는다.')]
OBSERVATIONS=[
 dict(id='NB-P1',standard_codes=['2수03-10','2수03-13'],question='막대의 양 끝이 자의3cm 눈금과8cm 눈금에 놓여 있다. 막대 길이는 얼마인가?0에 놓지 않아도 길이를 잴 수 있는 이유를1cm 간격과 연결해 설명하라.',
  expected='길이는8−3=5cm다.3에서8까지1cm 간격이5개이며 끝점의 숫자8을 길이로 읽는 것이 아니다. 같은1cm 단위로 빈틈·겹침 없이 잰다.',
  interpretation='끝의 숫자 읽기와 두 위치 사이 거리 해석을 구별한다. 오답이면 시작점·간격·단위를 중립적으로 물으며 한 반응으로 측정 능력의 부재나 인지 단계를 확정하지 않는다. 자를0으로 옮겨 주었다면 그 전후를 따로 기록한다.',student_validated=False),
 dict(id='NB-P2',standard_codes=['6수03-12','6수03-13','6수03-14'],question='6cm×4cm 직사각형을3cm×4cm 두 조각으로 잘라, 겹침 없이3cm×8cm 직사각형으로 재배치했다. 넓이와 둘레가 어떻게 변했는가? 처음 영역을1cm² 정사각형으로 덮은 수와, 그 정사각형을 각각 반으로 나눈 삼각형으로 덮은 수도 비교하라.',
  expected='넓이는두 경우 모두24cm²이고 둘레는20cm에서22cm로 변한다. 같은 조각을 빠짐없이 겹침 없이 옮겼으므로 넓이는 보존된다.1cm² 정사각형24개와1/2cm² 삼각형48개가 같은 넓이를 덮으며48조각이라고48cm²인 것은 아니다.',
  interpretation='보존되는 영역의 양·경계 길이·단위 조각 수를 각각 기록한다. 잘라 옮길 수 있다는 사실만으로 모든 보존·배열 과제를 이해했다고 판정하지 않는다. 삼각형 단위도 같은 크기로 빈틈 없이 덮으면 사용할 수 있음을 확인하는 자체 활동이다.',student_validated=False),
 dict(id='NB-P3',standard_codes=['6수03-18','6수03-19'],question='한 모서리1cm인 블록을 가로4개·세로3개·높이3층으로 빈틈 없이 채웠다. 한 층과 전체의 블록 수·부피를 설명하라. 이어 겉에서 보이지 않는 내부 블록2개만 빼고 외형을 유지했다면, 같은 외형만으로 재료 부피도 같다고 할 수 있는가?',
  expected='한 층12개·3층36개이므로 채운 경우36cm³다. 내부2개를 빼면 블록 재료의 부피는34cm³다. 외곽 상자의 공간은36cm³로 같아도 채워진 재료의 부피와 다르다. 직육면체 공식을 물체의 재료 부피에 적용하려면 빈틈 없이 채워졌다는 조건이 필요하다.',
  interpretation='층의 배열·층 수·가려진 블록·내부 충전 조건을 구별한다. 외형만 주어진 상황에서는 필요한 조건을 말하도록 한다. 단순 세기나 공식 결과 하나로 삼차원 구조 이해를 확정하지 않는다. 속이 빈 물체는 공식의 적용 조건을 대조하는 확장 사례다.',student_validated=False),
 dict(id='NB-P4',standard_codes=['4수03-24'],question='벌어진 각이30°인 그림에서 그려진 두 변의 길이를 각각2cm에서8cm로 늘렸다. 이어 그림 전체를 같은 방향으로45° 돌렸다. 각의 크기는 어떻게 되는가? 변의 길이·전체 그림의 방향·회전량과 구별해 설명하라.',
  expected='두 방향 사이의 벌어짐이 같으므로 각은계속30°다. 변이4배 길어져도 각이4배가 되지 않는다. 그림 전체를45° 돌린 것은 각의 두 방향을 함께 바꾼 것이며 두 변 사이 각이45°가 되었다는 뜻이 아니다.',
  interpretation='각의 정적인 벌어짐과 물체 전체의 회전량을 구별한다. 한 상황의 답을 돌기·각도기 눈금·도형 내부 각 모두의 이해로 확대하지 않는다. 교사가 회전이나 길이의 불변을 먼저 알려 준 경우 도움 후 반응으로 남긴다.',student_validated=False),
 dict(id='NB-P5',standard_codes=['4수02-03'],question='9+6=□+8에서 빈칸을 찾고 이유를 설명하라. 또 이를 풀면서9+6=15−8=7이라고 이어 쓴 기록은 참인 등식인가? 계산 결과를 유지하면서 올바르게 고쳐라.',
  expected='빈칸은7이며9+6과7+8이 모두15다. 원래 기록은15와7을 같다고 연결하므로 참인 등식이 아니다.9+6=15와15−8=7을 나누어 쓰거나(9+6)−8=7로 쓸 수 있다.',
  interpretation='계산의 진행 순서와 양쪽 값이 같다는 관계를 구별한다. 빈칸의 정답·등호 설명·기록의 수정은 따로 본다. 기호의 실수 하나만으로 양의 비교 능력이나 장기 이해를 부정하지 않는 자체 활동이다.',student_validated=False),
 dict(id='NB-P6',standard_codes=['6수04-01'],question='다음은 가상 자료다. A는0,2,6,8이고B는4,4,4,4다.0은 자료값이며 누락 표시가 아니다. 각 평균을 구하고, 평균이 같으면 자료도 같다는 말과 평균은 반드시 실제 자료값 중 하나라는 말을 검토하라.',
  expected='두 자료 모두합16·자료 수4이므로 평균4다. A의0을 자료 수에서 빼면 안 된다. A에는4가 실제 자료값으로 없으며 같은 평균이어도 값의 퍼짐과 구성이 다르다. B의값은 모두4지만 A는그렇지 않다.',
  interpretation='합계와 자료 수·균등 재분배·개별 값과 평균의 차이를 구별한다. 초등 활동에서 분산 같은 형식 계산을 요구하지 않는다. 평균 계산 성공만으로 적절한 그래프 구성·대표성·예측의 타당성이 확인됐다고 보지 않는다.',student_validated=False)]

def main():
 registry=load_registry()
 if SOURCE in registry['sources']:
  print('Reviewed source and targets remain current; no automatic refresh');build_report();return
 html=ROOT/'tmp/literature/adding-it-up-ch8.html';assert hashlib.sha256(html.read_bytes()).hexdigest()==SHA
 pages=json.loads((ROOT/'tmp/literature/adding-it-up-ch8-pages.json').read_text(encoding='utf-8'));assert set(pages)=={str(n) for n in range(255,313)}
 figures=json.loads((ROOT/'tmp/literature/adding-it-up-ch8-image-provenance.json').read_text(encoding='utf-8'));assert len(figures)==7
 for a in figures:assert hashlib.sha256((ROOT/'tmp/literature'/a['file']).read_bytes()).hexdigest()==a['sha256']
 notes=dict(source_id=SOURCE,source_url=URL,source_asset_kind='publisher_html',source_asset_sha256=SHA,source_asset_redistributed=False,date='2026-11-04',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,
  source_corrections=[dict(kind='workspace_bibliography_title_correction',observation='기존 서지는8장을Measurement and Geometry라고 적었으나 실제8장은Developing Mathematical Proficiency Beyond Number이고Measurement and Geometry는인쇄281–288쪽의절이다.',action='장 제목과 절 범위를 바로잡고 기존 식별자는 유지한다. 원문 내용의 오류 정정이나 PDF 판면 대조로 표시하지 않는다.')],
  reading_log=['출판사 공식HTML의인쇄255–312쪽58쪽을 모두 읽음. PDF를 다운로드하거나 전58쪽 인쇄 판면 이미지를 본 것은 아님.',
   '인쇄255–280: 표현·변형·일반화/정당화, 등호·미지수/변수·식의 구조·도구 연구 및상자8–1~8–8 대조. 예의 계산·표·일반식과 개별 사례/집단 비교의 한계를 구별.',
   '인쇄281–288측정·기하 절 전체: 동일 단위·시작점·길이 간격, 넓이 덮기/분해/재구성, 삼차원 단위, 도형 속성·각의 여러 모델·이동과대칭의 과제 의존성을 확인.',
   '인쇄288–294자료·가능성 및종합: 읽기/정리/표현/해석·대표값·표본공간·복원/비복원·독립의 개념을 구별. 한국 초등 학년의 필수 범위를 뜻하지 않음.',
   '인쇄294–300미주1–173과300–312참고문헌을 모두 읽고 본문과 출처의 연결을 확인. 인용된 원연구·원자료를 모두 읽거나 재분석한 것은 아님.',
   '웹본문의삽입 이미지7개를 각각 시각적으로 확인: 인쇄257점 배열,258분수해,260표,271동치분수3개,277삼각수 배열. 원격 자산의 주소·확인한 파일 해시를 기록.'],
  observed_image_assets=figures,read_printed_pages=list(range(255,313)),pdf_read=False,original_page_layout_review=False,
  interpretation_limits=['2001년 연구 종합의 실제 서술 범위다. 오늘날 모든 학습자·교육과정·디지털 도구의 효과에 관한 규준이나 최신 체계적 문헌 고찰로 취급하지 않음.',
   '개념 이해·절차·표현·정당화의 연결을 설계에 참고하되, 학년·도구·한 반응을 인지 단계나 보편적 선수 순서로 고정하지 않음.',
   '기술 활용 비교에서도 과제의맥락·도구 허용·숙달한 기능에 따라 결과가 달랐다. 연구가 보고한 인과·상관·사례를 구별하며 모든 도구가 모든 기능을 개선한다고 결론짓지 않음.',
   '서로 다른 연구의 표본·백분율을 합치지 않고, 현재 자체 과제의 효과·독립 검토·학생 검증으로 전용하지 않음.'])
 (ROOT/NOTES).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 sp=ROOT/'data/sources.json';sources=json.loads(sp.read_text(encoding='utf-8'));b=next(s for s in sources if s['id']==SOURCE);previous=dict(b)
 b.update(title='Adding It Up Chapter 8: Developing Mathematical Proficiency Beyond Number',doi='10.17226/9822',review_scope='출판사 공식HTML 인쇄255–312쪽58쪽 전체·상자8–1~8–8·미주1–173·참고문헌, 삽입 그림/수식7개 확인. 측정·기하는281–288쪽의절이며 실제 장명으로서지 정정. PDF판면·모든 인용 원연구·원자료는 미대조.',next_review='인용된 배열 구조·면적 재분배·기하 사고·등호·자료 해석 원연구의 과제·표본·실제 반응은 추가 대조 대상. 자체 관찰의 독립 검토·학생 반응 검증은 별도.')
 source=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-04',snapshot_kind='authored_review_notes',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256((ROOT/NOTES).read_bytes()).hexdigest(),source_asset_kind='publisher_html',source_asset_sha256=SHA,redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,
  display=dict(title=b['title'],url=URL,authors_year='National Research Council,2001,Adding It Up,Chapter8,255–312'),read_scope='공식웹본문 인쇄255–312쪽 전체·상자8–1~8–8·미주1–173·참고문헌과 삽입 그림/수식7개',
  scope_note='2001년의 연구 종합이다. 등호·표현·정당화, 측정·기하, 자료·가능성의 연결을 살피되 개별 학생의 발달 순서나 자체 과제 효과를 확정하지 않는다. 출판사 웹본문과 삽입 자산을 읽었으며 PDF 판면 대조와 구별한다.',
  method_note='여러 시대·표본·과제의 연구를 서술적으로 종합한다. 인용 원연구와 원응답을 모두 독립 재검토한 것은 아니다. 측정/보존·기하 사고의 단일 단계 가정, 도구 사용과 과제의 조건, 자료 읽기와 해석의 차이를 구별했다. 서로 다른 연구의 수치를 독립 표본처럼 합산하지 않는다.',
  limits='미국pre-K–8을 주로 다루는 역사적 연구 종합이며 한국2022개정 학년별 필수 범위·현재 도구의 효과 규준이 아니다. 원문이 제시한 사례를 현재 관찰의 학생 검증으로 바꾸지 않는다. 공식HTML과그림의확인 해시를 자체 기록에 보존하며 원격 원문의 이후 변경을 실시간 확인하지 않는다.',
  editorial_action='잘못 적힌 장명을 정정하고 기존 식별자는 유지. 측정·넓이·부피·각·등호·평균의 주장6건과 자체 관찰6건을 보완. 독립 검토·학생 검증은 완료로 표시하지 않음.',independent_review=False,student_validated=False,observations=OBSERVATIONS)
 registry['sources'][SOURCE]=source
 for cid,family,codes,locations,support,limit in MAPPINGS:
  target='family:'+family
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,target_snapshots={target:digest(target_value(target))},standard_codes=codes,independent_review=False,student_validated=False))
 sp.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 qp=ROOT/'data/content_review_queue.json';queue=json.loads(qp.read_text(encoding='utf-8'));row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE);row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[c[0] for c in MAPPINGS]);qp.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 build_report()
if __name__=='__main__':main()

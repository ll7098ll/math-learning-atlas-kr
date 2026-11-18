"""Bind a publisher HTML chapter and checked local arithmetic, without promoting validation."""
import copy,hashlib,json
from literature_review import ROOT,digest,target_value,load_registry,build_report
from relation_analysis_review import load_reviews

SOURCE='NRC_WHOLE_2001'
URL='https://www.nationalacademies.org/read/9822/chapter/8'
SHA='ba98b8057e9c466a7970ec34b2ed3055ebd668ab9557aed5e08a8e76a6fab05e'
NOTES='data/literature_evidence/NRC_WHOLE_2001_review_notes.json'
MAPPINGS=[
 ('NW01',['2수01-05','2수01-07','2수01-09'],['인쇄183–186 / Word Problems, Table6–1','인쇄190–191 / Single-Digit Subtraction','인쇄218–219 / 미주6–11,24–28'],
  '합치기·덜어내기·부분과 전체·비교의 수량 역할과 미지의 위치를 구별하고 덧셈·뺄셈의 역관계로 확인하는 자체 발문에 참고한다.',
  '낱말만으로 연산을 정하지 않는다. 원문의 문제 유형·아동 반응은 한국어 과제의 난도·진단 정확도·현재 학생 반응이 아니며 모든 문제를 한 풀이로 강제하지 않는다.'),
 ('NW02',['2수01-04','2수01-06'],['인쇄187–190 / Box6–1~6–3','인쇄193–195 / practice and summary','인쇄217 / Developmental Themes','미주13–23,31–45'],
  '합의 전체를 보존하는 분해·10 만들기·알고 있는 합의 활용과 여러 전략의 설명을 연결한다.',
  '방법들이 공존하고 문제·시점에 따라 달라질 수 있다. 속도만으로 회상·이해를 판정하거나 모든 학생에게 모든 전략의 동시 숙달·한 필수 경로를 요구하지 않는다. 연습을 없애야 한다는 결론도 내리지 않는다.'),
 ('NW03',['2수01-02','2수01-06','4수01-03'],['인쇄195–206 / Multidigit Calculations, Box6–6~6–10','인쇄213 / summary','미주47–73'],
  '십진 단위 교환으로 전체를 보존하고 구체물·그림의 동작과 같은 자리의 수치 기록을 대응하는 설계에 참고한다.',
  '자릿값의 완전 숙달을 모든 계산 시작의 선행 관문으로 고정하지 않는다. 도구는 자동으로 의미를 전달하지 않는다. 초등1~2학년의 두 자리 계산과3~4학년의 세 자리 계산을 구별하며 기호 절차 하나를 이해 전체로 보지 않는다.'),
 ('NW04',['2수01-10','2수01-11','4수01-04'],['인쇄184,186,191–192 / equal groups and Box6–4','인쇄206–210 / Box6–11~6–13','미주29–30,74–76'],
  '같은 크기 묶음·알려진 곱·배열 분할의 부분곱을 수치 기록에 대응하고 십의 자리 값과 교차 부분곱을 보존하는 설계에 참고한다.',
  '당시 여러 자리 곱셈의 발달 경로 연구는 충분하지 않다고 원문이 밝힌다. 원문의 대안 알고리즘을 유일한 교수 순서로 채택하지 않으며 두 인수의 상황 역할과 원문·현재 교육과정의 수 범위를 구별한다.'),
 ('NW05',['4수01-05','4수01-06','4수01-07'],['인쇄184,186,192–193 / division meanings','인쇄210–213 / Box6–14~6–16','미주9–11,77–82'],
  '한 묶음의 크기·묶음 수·몫의 단위를 구별하고 부분 몫의 합과 남은 양을 연결하는 자체 발문에 참고한다.',
  '당시 나눗셈 학습 연구의 제한을 유지한다. 현재 자연수 과제에는 양수 제수·복원식·0 이상 제수 미만의 나머지를 별도로 검산했다. 웹본문의 빠진 인수 수식 기호를 그대로 복사하지 않으며 현재 과제 효과를 입증한 것으로 보지 않는다.'),
 ('NW06',['4수01-08'],['인쇄214–216 / Mental Arithmetic and Estimation','인쇄221 / 미주83–92'],
  '편리한 수·연산 성질·어림의 목적과 오차 조정을 구별하고 예상과 정확한 계산 뒤 검토를 연결한다.',
  '어림을 한 반올림 절차로 고정하지 않는다. 인수를 반대 방향으로 바꾸면 오차 방향은 자동 확정되지 않는다. 계산 결과의 규모 점검과 정해진 정확도 보장을 구별하며 현재 학생·계산기 사용 효과로 확대하지 않는다.')]

OBSERVATIONS=[
 dict(id='NW-P1',standard_codes=['2수01-05','2수01-07','2수01-09'],
  question='가상 이야기다. 민서에게 구슬13개가 있고 그중5개를 주었다. 남은 수를 구하라. 또 민서는13개이고 준보다5개 더 많다면 준은 몇 개인가? 두 이야기의 수량 역할을 그리고5+□=13과 연결하라.',
  expected='두 질문의 답은 모두8개다. 첫 이야기는13개 중 덜어낸5개와 남은8개이고,둘째는민서13개와 준8개의 차이가5개다.13−5=8과5+8=13이 성립한다. 더 많다는 낱말이 있어도 준을 묻는 질문에13+5로 답하지 않는다.',
  interpretation='구한 수·그린 대상·전체/부분/차이·미지의 위치를 따로 기록한다. 같은 계산이 서로 다른 상황을 나타낼 수 있다. 교사가 식을 먼저 제시한 경우와 학생이 식을 구성한 경우를 구별한다. 현재 한국어 발문의 난도·인지 단계는 검증하지 않았다.',student_validated=False),
 dict(id='NW-P2',standard_codes=['2수01-04','2수01-06'],
  question='9+7을 구하고 구슬이나 그림으로 설명하라.7을1과6으로 나누는 방법과9에서1을7로 옮기는 방법에서 전체가 같은 이유를 말하라. 자신이 먼저 사용한 방법도 남겨라.',
  expected='9+(1+6)=10+6=16이다. 다른 방법은(9−1)+(7+1)=8+8=16이다. 같은 구슬을 한 번씩 세고 한 부분에서 다른 부분으로 옮기므로 전체는 보존된다. 두 방법 모두 옳으며 반드시 둘 다 최초에 사용해야 하는 것은 아니다.',
  interpretation='최초 방법·이후 비교·도움 뒤 설명과 연습 결과를 구별한다. 빠른 답만으로 암기인지 빠른 계산인지 판정하지 않고 다시 세는 방법도 기록한다. 모든 학생에게 모든 전략의 동시 숙달을 요구하지 않는다.',student_validated=False),
 dict(id='NW-P3',standard_codes=['4수01-03'],
  question='402−175를 구하라.4백0십2일을3백9십12일로 바꾼 값이 같은지 확인하라. 각 자리의 큰 숫자에서 작은 숫자를 빼어373이라고 쓴 오답 예를 검토하고 원식으로 검산하라.',
  expected='300+90+12=402다. 같은 단위끼리 빼면2백2십7일,곧227이고227+175=402다.373은 어느 수에서 어느 수를 빼는지 보존하지 않아 오답이다.425−125처럼 같은 자리 값이 같은 경우에도 뺄 수 있으며 차이는0이다.',
  interpretation='백→십→일의 교환·왼쪽 자리 감소·양 보존·검산을 관찰한다. 이 계산은3~4학년의 자체 활동이고1~2학년 자릿값 기준에 세 자리 뺄셈을 새 필수 수행으로 넣지 않는다. 오답 예는 가상 기록이며 실제 학생 반응이 아니다.',student_validated=False),
 dict(id='NW-P4',standard_codes=['4수01-04'],
  question='가로24칸·세로13줄의 같은 크기 칸 배열을20+4와10+3으로 나누어 전체 칸 수를 구하라.20×10+4×3=212라는 오답 예에 빠진 부분을 표시하고 세로셈의 부분곱과 연결하라.',
  expected='부분은20×10=200,20×3=60,4×10=40,4×3=12이며 합312칸이다.212는교차 부분60칸·40칸을 빠뜨렸다.24×13=24×10+24×3=240+72=312로도 확인한다. 배열 부분은 겹치지 않고 전체를 덮어야 한다.',
  interpretation='부분곱의 수·십의 값·빠진 부분·합을 구별한다. 길이×길이의 넓이 단위 계산을 새로 요구하는 활동이 아니라 같은 칸의 배열을 세는 자체 과제다. 설명과 기록을 대응하며 특정 알고리즘만 유일하게 허용하지 않는다.',student_validated=False),
 dict(id='NW-P5',standard_codes=['4수01-05','4수01-06','4수01-07'],
  question='85개를4명에게 똑같이 주거나4개씩 포장할 때 몫의 단위를 구별하라.85=4×20+5이므로 몫20·나머지5라는 오답 예는 왜 끝난 나눗셈이 아닌가? 이어157÷12를 부분 몫으로 구하고 확인하라.',
  expected='85÷4의 몫21·나머지1이다. 첫 상황은21개/명·남은1개,둘째는21포장·남은1개다. 나머지5는4개를 한 번 더 나눌 수 있어 허용되지 않는다.157−120=37,37−36=1이므로157÷12는몫10+3=13·나머지1이며12×13+1=157과0≤1<12를 만족한다.',
  interpretation='몫의 수치·단위·복원식·나머지의 범위·부분 몫을 따로 기록한다. 제수는 양수인 자연수이고 이 과제는 자연수 몫·나머지를 묻는다. 분수 몫을 틀렸다고 일반화하지 않으며 물건·사람을 실제로 조사한 자료로 표시하지 않는다.',student_validated=False),
 dict(id='NW-P6',standard_codes=['4수01-08'],
  question='정확히 계산하기 전에51×19와54×19를 각각50×20=1000으로 어림하는 이유와 목적을 적어라. 두 어림값이 모두 정확한 값보다 큰지 예상한 뒤 정확히 계산해 확인하라.',
  expected='정확한 값은969와1026이다.1000은앞 계산보다31크고 뒤 계산보다26작다. 두 경우 첫 인수는 줄이고 둘째 인수는 늘렸으므로 방향만으로 곱의 오차 방향이 정해지지 않는다. 결과의 규모를 미리 점검할 수 있지만 정확한 값과는 ≈와 =를 구별한다.',
  interpretation='예상한 시점·바꾼 수·어림의 목적·실제 오차를 기록한다. 정확한 답을 먼저 구한 뒤의 반올림과 계산 전 예상을 구별한다. 한 방식만 요구하거나 이 예로 모든 반대 방향 어림의 오차를 결정하지 않는다.',student_validated=False)]

def verify():
 assert 13-5==8 and 5+8==13
 assert 9+7==10+6==8+8==16
 assert 3*100+9*10+12==402 and 402-175==227 and 227+175==402
 assert 425-125==300 and 373+175!=402
 cells={(x,y) for x in range(24) for y in range(13)}
 parts=[{(x,y) for x in xs for y in ys} for xs in [range(20),range(20,24)] for ys in [range(10),range(10,13)]]
 assert set.union(*parts)==cells and sum(map(len,parts))==len(cells)==312
 assert sorted(map(len,parts))==[12,40,60,200] and 24*10+24*3==312 and 200+12==212
 assert divmod(85,4)==(21,1) and 4*20+5==85 and not 0<=5<4
 assert divmod(157,12)==(13,1) and 10+3==13 and 12*13+1==157
 assert 51*19==969<1000<1026==54*19
 assert 72//9==8 and 9*8==72 and 9/8!=72

def main():
 verify();registry=load_registry();before=set(load_reviews()['records'])
 if SOURCE in registry['sources']:
  print('Whole-number chapter and targets remain current; no automatic refresh');build_report();return
 assert not {m[0] for m in MAPPINGS}&{c['id'] for c in registry['claims']}
 raw=ROOT/'tmp/literature/adding-it-up-ch6.html';assert hashlib.sha256(raw.read_bytes()).hexdigest()==SHA
 pages=json.loads((ROOT/'tmp/literature/adding-it-up-ch6-text-pages.json').read_text(encoding='utf-8'));assert set(pages)=={str(i) for i in range(181,231)}
 assets=json.loads((ROOT/'tmp/literature/adding-it-up-ch6-image-provenance.json').read_text(encoding='utf-8'));assert len(assets)==22
 for a in assets:assert hashlib.sha256((ROOT/'tmp/literature'/a['file']).read_bytes()).hexdigest()==a['sha256']
 corrections=[dict(kind='publisher_html_caption_image_mismatch',location='인쇄189 / Box6–2',observed='웹본문 제목은B+6이지만 삽입 그림은8+6과10+4=14를 보여 준다.',action='문자B를 수로 인용하지 않고 확인한 삽입 그림과 자체 수치 검산을 구별한다. PDF 인쇄 판면의 오자라고 확정하지 않는다.'),
  dict(kind='publisher_html_math_transcription_guard',location='인쇄192 / Single-Digit Division',observed='72÷9의 빠진 인수를 설명하는 웹본문에9÷?=72라고 적혀 있다.',action='자연수 나눗셈의 역관계는9×8=72로 검산했다. 의심스러운 기호를 복사하지 않으며 원 PDF 판면·정오표를 확인하기 전 원책 오자 또는 웹 전사 오류의 원인을 확정하지 않는다.'),
  dict(kind='publisher_html_internal_wording_guard',location='인쇄196–199,205–206',observed='다자리 계산 관찰 목록의 앞선7개와 뒤의6개 표기,재묶기 설명의 엄격한 큼 표현을 확인했다.',action='목록 수를 근거 수로 인용하지 않는다. 자체 뺄셈은 같은 자리 값이 같아도 뺄 수 있다는 이상 조건으로 검산하며 원문의 부등호식 표현을 그대로 규칙화하지 않는다.')]
 notes=dict(source_id=SOURCE,source_url=URL,source_asset_kind='publisher_html',source_asset_sha256=SHA,source_asset_redistributed=False,date='2026-11-05',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,source_corrections=corrections,read_printed_pages=list(range(181,231)),observed_image_assets=assets,
  reading_log=['공식HTML 인쇄181–230의50쪽을 모두 읽었다.230쪽은 원문 공백 안내이며 실제 수학 본문·미주·참고문헌은181–229쪽이다. PDF 다운로드·50쪽 인쇄 판면 대조가 아니다.',
   '181–194쪽의 문제 유형 표6–1·단일 자리 계산과 전략의 공존,195–213쪽의 십진 단위·다자리 계산 및 연구의 차이,214–218쪽의 암산·어림·발달 주제를 읽었다.',
   '218–221쪽 미주1–92와221–229쪽 참고문헌을 읽고 본문과 연결했다. 인용 원논문·실제 원응답·현행 후속 연구 전체를 재검토한 것은 아니다.',
   '본문의 삽입 자산22개를 모두 시각적으로 확인했다. 상자6–1~6–16의 세기·10 만들기·단위 교환·배열·부분곱·부분 몫과 작은 분수/나눗셈 기호를 대조하고 확인 주소·해시를 남겼다.'],
  interpretation_limits=['2001년 연구 종합이며 현재 한국 학생의 학년별 규준·최신 체계적 고찰·도구 효과·인지 단계 검사와 구별한다.',
   '덧셈·뺄셈에 비해 곱셈·나눗셈의 발달 연구가 제한적이라는 원문 범위를 유지한다. 개념 이해·유창성은 함께 발달할 수 있고 자릿값 완전 숙달을 모든 계산의 선행 관문으로 삼지 않는다.',
   '인용 연구의 표본·효과를 합산하지 않으며 자체 과제의 독립 검토·학생 반응·번역 동등성·교수 효과로 전용하지 않는다.'])
 (ROOT/NOTES).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 path=ROOT/'data/sources.json';sources=json.loads(path.read_text(encoding='utf-8'));b=next(v for v in sources if v['id']==SOURCE);previous=copy.deepcopy(b)
 b.update(title='Adding It Up Chapter 6: Developing Proficiency with Whole Numbers',doi='10.17226/9822',review_scope='공식HTML 인쇄181–230쪽50쪽(230쪽 공백 안내),표6–1·상자6–1~6–16·미주1–92·참고문헌과 삽입 자산22개 확인. PDF 판면·원연구 전체·현행 후속 연구 미대조.',next_review='개별 원연구의 과제·표본·실제 반응,PDF 판면과 웹 수식 전사·목록 표기의 차이,후속 연구·한국어 측정 동등성·실제 학생 반응은 추가 대조 대상.')
 registry['sources'][SOURCE]=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-05',snapshot_kind='authored_review_notes',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256((ROOT/NOTES).read_bytes()).hexdigest(),source_asset_kind='publisher_html',source_asset_sha256=SHA,redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,
  display=dict(title=b['title'],url=URL,authors_year='National Research Council,2001,Adding It Up,Chapter6,181–230'),read_scope='공식HTML 인쇄181–230쪽50쪽·표6–1·상자6–1~6–16·미주1–92·참고문헌과 삽입 자산22개;마지막230쪽은 공백 안내',
  scope_note='2001년의 자연수 연산 연구 종합이다. 수량의 역할·단위 교환·전략의 설명을 연결하되 단일 필수 순서·현재 과제 효과·학생의 인지 단계를 확정하지 않는다. 공식HTML과 삽입 자산을 확인했으며 PDF 인쇄 판면을 대조한 것은 아니다.',
  method_note='여러 연구와 교수 예를 서술적으로 종합한다. 연구별 과제·방법의 차이와 덧셈/뺄셈에 비해 적은 곱셈/나눗셈 근거를 구별하고,미주·참고문헌의 확인을 개별 원연구 재검토로 집계하지 않는다. 여러 전략의 공존·도구와 수치 기록의 연결·개념과 절차의 상호 발달을 구별했다.',
  limits='한국2022개정 학년별 필수 범위·현재 수업 효과·진단 규준·언어 동등성의 직접 근거가 아니다. 웹본문과 삽입 그림의 표기 차이와 의심스러운 나눗셈 기호는 읽기 기록에 남겼고 원 PDF·정오표 대조 전 원책/전사 오류의 원인은 확정하지 않는다. 원문 HTML은 재배포하지 않고 자체 기록·해시·주소를 보존한다.',
  editorial_action='현재14개 기준에 주장6건·자체 관찰6건을 대응했다. 수량 역할·10 만들기·0을 거치는 단위 교환·모든 부분곱·몫 단위와 나머지·어림 오차를 보완했다. 기존 대표 원고와 관계 검토를 바꾸거나 신규 관계 검토·독립 검토·학생 검증으로 합산하지 않았다.',independent_review=False,student_validated=False,observations=OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},standard_codes=codes,independent_review=False,student_validated=False))
 path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 path=ROOT/'data/content_review_queue.json';queue=json.loads(path.read_text(encoding='utf-8'));row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE);row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[m[0] for m in MAPPINGS]);path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert set(load_reviews()['records'])==before
 build_report();print('Added whole-number chapter: 6 scoped claims / 6 own observations; no relation approvals')

if __name__=='__main__':main()

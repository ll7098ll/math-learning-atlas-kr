"""Extend LT2 number-domain reading without promoting page counts to validation."""
import copy
import hashlib
import json
from collections import Counter
from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews
from record_lt2_public_review import SOURCE, URL
from extend_lt2_measure_data_review import NOTES as PRIOR_NOTES

NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_number_operations_review_notes.json'
PRIOR_SHA = '4d3d474c234040f6f70060a8312c30694ca9fc9cbc7fed0adc05504836549b6b'
DOMAINS = ['comparing-and-ordering-number', 'adding-subtracting', 'composing-numbers', 'multiplying-dividing']
ACTIVITIES = ['flip-to-compare-to-10', 'line-up--whos-next', 'make-the-sum-composer-using-tens-and-ones', 'hidden-10s-and-1s', 'how-many-now-hidden-version-counting-strategies-', 'mystery-change-game', 'make-equal-groups', 'skip-counting-with-cubes-skip-counter']
SCOPE = '공식 공개HTML 누적140개 지정 영어 본문: 일반6·영역 개요12·수준100·활동21·교사자료1. 수 비교/순서·덧셈/뺄셈·수 합성·곱셈/나눗셈의 새4개 개요·공개55수준 본문·선정8활동을 추가했다. 서로 겹치는 수준 설명도 URL별 읽기 수이며 독립 단계/연구 수가 아니다. 원본 그림·영상·첨부PDF·게임·인용 원연구는 미대조다.'
OBSERVATIONS = [
 dict(id='LT-P12', standard_codes=['2수01-01', '2수01-03'], question='큰 단추5개와 작은 단추6개를 놓고 어느 쪽의 개수가 더 많은지 확인하라. 단추를 더하거나 빼지 않고 간격만 벌렸을 때도 같은가? 다음에 왼쪽부터 A·B·C·D·E·F인 카드6장을 놓는다. 왼쪽에서 셋째와 오른쪽에서 셋째는 각각 누구인가? 방향을 바꾸면 전체 카드 수도 달라지는가?', expected='단추 크기나 차지한 공간과 관계없이 작은 단추 쪽이6개로1개 더 많다. 하나씩 짝지으면 작은 단추1개가 남는다. 간격만 바꾸어도 같은 단추를 한 번씩 세므로 각각5개·6개다. 카드의 왼쪽 셋째는C,오른쪽 셋째는D다. 세는 시작 방향에 따라 순서는 바뀌지만 전체는6장이다.', interpretation='자체 실물/카드 활동이다. 크기·공간·기수·서수와 방향을 나누어 기록한다. 일대일 짝짓기·직접 세기·구조로 파악하기 중 최초 방법을 보존하고 모두를 동시에 요구하지 않는다. 카드 글자 읽기나 방향 지시의 어려움은 개수 이해와 별도로 확인하며 가리키기 등도 허용한다.6까지의 이 과제 성공을100까지 세기나 네 자리 수 비교 전체의 숙달로 판정하지 않는다. 비교/서수/배열/어림의 다섯 하위 경로를 한 줄의 필수 순서로 만들지 않는다.', student_validated=False),
 dict(id='LT-P13', standard_codes=['2수01-02', '2수01-06'], question='십 묶음과 낱개로47+38을 나타내고 합을 구하라. 낱개10개를 십 묶음1개로 교환하기 전후에 묶음과 낱개의 수·물리적 조각 수·전체 양을 각각 설명하라. 십 묶음7개와 낱개15개를75로 적어도 되는가?', expected='47은4십7일,38은3십8일이다. 합치면7십15일이며 낱개10개를 십1개로 교환하면8십5일,85다. 교환 전 물리적 조각은7+15=22개이고 교환 뒤는8+5=13개지만,한 십 묶음이 낱개10개의 양을 나타내므로 전체는85로 같다.7십15일은70+15여서85이며75가 아니다. 다른 올바른 방법의 예는47에3을 더해50을 만든 뒤 남은35를 더하는 것이다.', interpretation='십 블록은 낱개10개와 같은 양이라는 약속/실제 교환을 먼저 확인한다. 조각 수와 나타내는 수량·받아올린1의 단위·남은 부분을 구별하고 최초 계산과 도움 뒤 비교를 따로 기록한다. 자체 두 자리 계산이며 네 자리 수 표기 전체의 숙달로 확대하지 않는다.20 이하 분해/합성 성취기준의 필수 과제로47+38을 붙이지 않는다. 원문 활동의 목표/절차가 다른 게임을 혼합하지 않고 카드 최적화나 속도 경쟁도 이 과제의 요구로 추가하지 않는다.', student_validated=False),
 dict(id='LT-P14', standard_codes=['2수01-05', '2수01-07'], question='①처음 사과7개에 몇 개를 더했더니12개가 되었다. ②처음 몇 개에5개를 더했더니12개가 되었다. ③민수의12개는 지수보다5개 더 많다. 지수는 몇 개인가? 각 이야기에서 아는 양과 묻는 양을 표시하고 식·그림·실물 중 편한 방법으로 설명하라. 필요할 때7+5 또는12-5의 세기 과정을 따로 확인하라.', expected='①7+빈칸=12에서 더한 양은5개다. ②빈칸+5=12에서 처음 양은7개다. ③지수의 양+5=12이므로12-5=7개다. 더 많다는 말만으로12+5를 고르지 않는다.7에서5개를 더 세면 새 단계는8·9·10·11·12이고 시작값7은 첫 추가가 아니다.12에서5개를 덜어 세면11·10·9·8·7이다.12-5를5에서12까지 세어7단계를 얻는 방법도 가능하다.', interpretation='가상 이야기이며 실제 학생 오답 기록이 아니다. 미지의 위치·변화량·전체·비교 기준을 구별하고 정답 수만으로 어떤 양을 구했는지 추측하지 않는다. 처음부터 전체 세기·이어 세기·맞춰 세기·알고 있는 조합 등 최초 선택을 기록한 뒤 필요할 때 비교한다. 목표 수까지 채울 수 있다는 것과 추가한 개수를 별도로 추적하는 수행은 다르다. 가림막 뒤 수량 유지에는 시각 접근·기억·도움 조건도 영향을 주므로 한 번의 실패를 연산 이해의 부재로 확정하지 않는다.', student_validated=False),
 dict(id='LT-P15', standard_codes=['2수01-10', '2수01-11', '4수01-05', '4수01-06'], question='물체18개를 ①봉지3개에 같은 수로 남김없이 넣을 때 한 봉지의 수,②한 봉지에3개씩 넣을 때 필요한 봉지 수를 각각 구하라.18÷3=6에서3과6이 무엇을 세는지 설명하고 곱셈으로 확인하라.3~4학년의 추가 상황에서는 자르지 않는 물체19개를 같은 방식으로 나눌 때 남는 양도 설명하라.', expected='①3봉지에 각6개,②각3개씩6봉지다. 같은18÷3=6이어도①의3은 봉지 수·6은 개/봉지,②의3은 개/봉지·6은 봉지 수다. 한 묶음 크기를 먼저 쓰면①6×3=18,②3×6=18이며 각각의 인수 역할을 붙인다.19개는①각6개에1개 남고,②3개씩6봉지에1개 남는다.3×6+1=19이고0≤1<3이다. 한 봉지에 같은 수로 다 넣었다고 하거나 남은1개를 임의로 없애지 않는다.', interpretation='앞의 곱셈 장면은1~2학년에서 같은 크기 묶음·구구의 설명을 볼 수 있지만 나눗셈식·몫/나머지는3~4학년 범위의 대응이다. 자르지 않는 물체·동일한 봉지·빈틈없는 개수 배분 조건에서 자연수 몫과 나머지를 다룬다. 과일을 자르거나 남은 것을 따로 나누는 조건이면 답의 의미가 바뀌므로 조건을 먼저 정한다. 소수/분수 나눗셈이나 반비례 공식을 새 요구로 넣지 않는다. 묶음 수가 늘면 몫이 줄어든다는 설명도 전체를 고정하고 같은 수로 나눈 조건을 확인한다. 등분제와 포함제를 원문 말미의 엇갈린 수치 식으로 구별하지 않는다.', student_validated=False),
]
MAPPINGS = [
 ('LT12', OBSERVATIONS[0]['standard_codes'], ['Comparing and Ordering Number 개요와 공개23수준 본문', 'Flip to Compare [to 10] / Line Up - Who\'s Next? 영어 본문'], '물체 크기·배열 공간과 개수,기수와 시작 방향에 따른 서수,일대일 대응과 비교 판단을 구별하는 자체 활동의 설계 참고다.', '원문의 비교·서수·배열·수량 어림·수직선 어림 하위 경로를 한 줄의 필수 순서로 쓰지 않는다. 어림 예의 부정확한 답·연령·수준 이름을 정답이나 현재 한국 학생의 단계/진단 규준으로 사용하지 않는다. 작은 수 과제만으로 네 자리 수 비교 전체를 검증하지 않는다.'),
 ('LT13', OBSERVATIONS[1]['standard_codes'], ['Composing Numbers 개요와 공개11수준 본문', 'Make the Sum [Composer Using Tens and Ones] / Hidden 10s and 1s 영어 본문'], '같은 수의 부분·전체와 십/일의 단위 교환·부분의 보상·양 보존을 구별하는 자체 두 자리 계산 설계에 참고한다.', 'Make the Sum의 목표와 절차는 서로 다른 게임으로 읽혀 그대로 혼합하지 않는다. 부분이0이면 전체와 다른 부분은 같을 수 있어 전체가 언제나 각 부분보다 엄밀히 크다고 일반화하지 않는다.47+38은20 이하 분해/합성 기준의 새 필수 과제가 아니며 네 자리 수 숙달이나 책 전권의 효과 검증도 아니다.'),
 ('LT14', OBSERVATIONS[2]['standard_codes'], ['Adding / Subtracting 개요와 공개12수준 본문', 'How Many Now? Hidden Version [Counting Strategies +/-] / Mystery Change Game 영어 본문'], '결과·변화·처음 양·부분·비교 상황에서 미지의 역할과 이어 세기의 시작값/이동 수를 구별하는 자체 발문 설계에 참고한다.', '더 많다/더하다 같은 낱말을 연산 선택 규칙으로 쓰지 않는다. 목표까지 채우기와 추가한 수를 추적하기는 다르고 가림막 활동의 결과 미지를 변화 미지로 바꾸어 읽지 않는다. 모든 전략의 동시 숙달·보편적인 경로·현재 과제의 효과를 입증하지 않는다.'),
 ('LT15', OBSERVATIONS[3]['standard_codes'], ['Multiplying / Dividing 개요와 공개9수준 본문', 'Make Equal Groups / Skip Counting with Cubes [Skip Counter] 영어 본문'], '전체·묶음 수·한 묶음의 수와 인수/몫의 단위,같은 크기 묶음의 반복·등분/포함 상황·나머지 조건을 구별하는 자체 설계 참고다.', 'Partitive Divisor와 Skip Counter 본문 끝의 식은 앞의 주어진 수/미지 역할과 맞지 않아 복사하지 않는다. 자연수의 같은 크기 묶음에서 반복 덧셈을 쓰는 것과 모든 곱셈을 반복 덧셈으로 정의하는 것은 다르다. 나머지/분할·국내 학년별 범위·고정 전체 조건을 확인하며 실제 학생/원연구 효과를 추가하지 않는다.'),
]

def verify():
 assert len(MAPPINGS) == len(OBSERVATIONS) == 4
 assert len({c for m in MAPPINGS for c in m[1]}) == 10
 assert 6 - 5 == 1 and list('ABCDEF')[2] == 'C' and list(reversed('ABCDEF'))[2] == 'D'
 assert 4*10+7 + 3*10+8 == 7*10+15 == 8*10+5 == 85
 assert 7+15 == 22 and 8+5 == 13 and 47+3+35 == 85
 assert 0+6 == 6 and not 6 > 6
 assert list(range(8, 13)) == [8,9,10,11,12] and len(range(8, 13)) == 5
 assert list(range(11, 6, -1)) == [11,10,9,8,7] and len(range(6, 13)) == 7
 assert [n for n in range(13) if 7+n == 12] == [5]
 assert [n for n in range(13) if n+5 == 12] == [7]
 groups = [[i for i in range(k*6, (k+1)*6)] for k in range(3)]
 packs = [list(range(k*3, (k+1)*3)) for k in range(6)]
 assert len(groups) == 3 and {len(g) for g in groups} == {6}
 assert len(packs) == 6 and {len(g) for g in packs} == {3}
 assert sorted(i for g in groups for i in g) == sorted(i for g in packs for i in g) == list(range(18))
 assert divmod(19,3) == (6,1) and 0 <= 1 < 3 and 3*6+1 == 19
 assert 24//4 == 6 and 4*6 == 24 and 6*4 == 24
 assert abs(3-2.5) == 0.5 and abs(3500-2000) < abs(3500-7000)

def main():
 verify()
 registry = load_registry(); s = registry['sources'][SOURCE]
 if s['snapshot_file'] == NOTES:
  assert {m[0] for m in MAPPINGS} <= {c['id'] for c in registry['claims']}
  print('LT2 number extension remains current; no automatic refresh'); build_report(); return
 assert s['snapshot_file'] == PRIOR_NOTES and s['snapshot_sha256'] == PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest() == PRIOR_SHA
 old = copy.deepcopy(registry); relations = copy.deepcopy(load_reviews())
 prior = json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'))
 assert not {m[0] for m in MAPPINGS} & {v['id'] for v in registry['claims']}
 cache = ROOT/'tmp/literature/lt2-number-operations'
 pages = json.loads((cache/'manifest.json').read_text(encoding='utf-8'))
 activities = json.loads((cache/'activity-manifest.json').read_text(encoding='utf-8'))
 assert len(pages) == 59 and len(activities) == 8
 levels = [a for a in pages if '/math/learning-trajectories/' not in a['url']]
 assert Counter(a['url'].split('/math/')[1].split('/')[0] for a in levels) == dict(zip(DOMAINS,[23,12,11,9]))
 assert {a['url'].split('/math-activities/')[1] for a in activities} == set(ACTIVITIES)
 for a in pages+activities:
  assert a['url'].startswith(URL) and a['url'] == a['final_url'] and a['status'] == 200
  assert hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest() == a['sha256']
 fields = ['key','url','title','sha256','status']
 all_assets = prior['observed_html_assets'] + [{k:a[k] for k in fields} for a in pages+activities]
 assert len(all_assets) == len({a['url'] for a in all_assets}) == 140
 assert len({a['key'] for a in all_assets}) == 140
 groups = copy.deepcopy(prior['read_groups'])
 groups['domain_overviews'] += [a['key'] for a in pages if '/math/learning-trajectories/' in a['url']]
 groups['levels'] += [a['key'] for a in levels]
 groups['activities'] += [a['key'] for a in activities]
 assert {k:len(v) for k,v in groups.items()} == dict(general=6,domain_overviews=12,levels=100,activities=21,teacher_resources=1)
 # Authored Korean notes record uncertainties without modifying the public source.
 corrections = [
  dict(kind='comparison_subtrajectories_and_estimation_guard', locations=['Comparing and Ordering Number / overview,Spatial Extent Estimator,Mental Number Line to 5/1000'], action='비교·서수·배열·수량 어림·수직선 어림의 다섯 하위 경로를 한 줄의 필수 순서로 읽지 않는다.13개를30이라 하거나9개를14라 하는 예는 기술된 어림 반응이며 정확한 정답이 아니다.0~5의 중점은2.5여서3은 정확한 중점이 아니고,1000이라는 수준명 아래3500/2000/7000 및10000도 언급되므로 이름만으로 본문 수 범위를 제한하지 않는다. 분수/소수를 유아의 새 요구로 넣지 않는다.'),
  dict(kind='number_estimation_area_text_mismatch', locations=['Comparing and Ordering Number / Scanning with Intuitive Quantification Estimator / Help'], action='수량 어림 수준의 교수 도움 본문이 표면 덮기·넓이와 높이 구별을 말한다. 해당 넓이 문장을 수량 어림 효과나 수직선 어림의 직접 근거로 옮기지 않는다. 본문 불일치로 기록하고 저자의 수정 의도/정오표는 미확인으로 둔다.'),
  dict(kind='zero_part_and_whole_guard', locations=['Composing Numbers / overview,Part-Whole Recognizer'], action='개요의0+6=6과 대조하면 전체가 부분보다 언제나 엄밀히 크다는 표현은0인 부분을 허용할 때 일반화할 수 없다. 서로 겹치지 않는 비음수 부분의 합에서 전체는 각 부분 이상이며 다른 부분이 양수일 때 엄밀히 크다. 자체 저학년 활동에서는 실물과0의 뜻으로 확인한다.'),
  dict(kind='make_sum_objective_procedure_mismatch', locations=['Make the Sum [Composer Using Tens and Ones] / Learning Objective,Preparation,Activity,Materials'], action='목표는1~10 카드 여섯 벌·주사위3개 합 만들기·카드 소진 게임이고,절차는1~9 카드 중5장을 뽑아 두 자리 수2개로100에 가까운 합 만들기다. 자료 목록0~10도 다르다. 동일 게임으로 합쳐 복사하지 않고 자체47+38의 단위 교환만 설계했다.5장 중4장 선택/재사용/동점 규칙도 원문에서 확인 전이다.'),
  dict(kind='count_on_unknown_role_and_hidden_task_guard', locations=['Adding / Subtracting / overview,Make It N,Find Change,Numbers-in-Numbers','How Many Now? Hidden Version [Counting Strategies +/-]','Mystery Change Game'], action='4에서2개를 이어 세면 새 단계는5·6이며 시작4를 첫 추가로 세지 않는다. 목표 수 만들기와 추가한 수를 추적하기는 별개다. Mystery Change의 경로 표시는Make It N이지만 절차는 보이는 변화 뒤 숨은 최종 수를 재현한다. 명칭만으로 변화 미지 과제로 판정하지 않는다. 결과·처음·변화·비교에서 묻는 양을 실제 발문으로 확인한다.'),
  dict(kind='division_equation_role_mismatch', locations=['Multiplying / Dividing / Partitive Divisor / Help','Multiplying / Dividing / Skip Counter X/÷ / Help'], action='Partitive의24개/4명 설명 뒤6×빈칸=24는 계산상 빈칸4를 주어,구하는6개/명과 역할이 맞지 않는다. 묶음 수를 앞에 쓰면4×빈칸=24이며 국내 원고의 묶음 크기 우선 관례로는빈칸×4=24다. Skip Counter의한 묶음4개/전체24개 설명 뒤빈칸×6=24도 원래 미지인6묶음과 맞지 않는다. 크기 우선으로4×빈칸=24를 써야 한다. 단순 인수 교환과 주어진 수/미지의 바뀜을 구별한다. 원문 식을 현재 과제에 복사하지 않는다.'),
  dict(kind='equal_groups_scope_remainder_and_fixed_total', locations=['Multiplying / Dividing / overview,Concrete Modeler,Parts and Wholes,Deriver','Make Equal Groups','Skip Counting with Cubes [Skip Counter]'], action='같은 수의 묶음을 반복 덧셈/건너뛰기로 세는 설명은 자연수 묶음 맥락에 한정한다.11장을2명에게 모두 나누어 한 사람이 더 가진 예는 같은 수 배분 성공이 아니다. 나머지·물체를 자를 수 있는지·전체 고정·동일 배분·묶음 크기를 확인하고 더 많은 사람→더 적은 몫을 무조건 일반화하지 않는다. 원문의Confrey2014와2017논문 표시는 원논문 읽기/효과 검증에 합산하지 않는다.'),
  dict(kind='crosslisted_levels_versions_and_access_support', locations=['Adding / Subtracting 및Composing Numbers의Deriver,Problem Solver,Multidigit','선정8활동 / Last updated,References,Differentiating Instructions'], action='두 영역의Deriver/Problem Solver/Multidigit은 예와 설명이 크게 겹치지만 도움 문구·일부 수치/서술·연결 활동은 다르다.6개URL을 읽기 페이지로 보존하되6개 독립 단계/연구로 합산하지 않는다. 선행/후속 활동 링크도 하위 경로 간 이동을 포함해 보편적 선수성을 입증하지 않는다.2025/2026갱신일과2014/2021/2026책·2017논문·2020교육과정 표기를 각각 보존하며 책 전권/원연구 읽기로 바꾸지 않는다. 수어·가리키기·접근 도구/재료 변경 후 수행을 처음 독립 수행과 구별한다.'),
 ]
 p = ROOT/'data/sources.json'; bibliography = json.loads(p.read_text(encoding='utf-8'))
 b = next(v for v in bibliography if v['id'] == SOURCE); previous_b = copy.deepcopy(b)
 b.update(review_scope=SCOPE, next_review='현재20영역 중 미검토8영역(입체도형·평면/입체 합성·도형 분리·규칙/구조/대수·공간 방향·공간 시각화·수량 즉지) 개요/수준과 기존4영역의 미선정 수준·모든 영역의 미선정 활동을 후속 대조한다. 원본 그림·영상·첨부PDF·게임·인용 원연구/교재·정오표와 실제 한국어 과제의 학생 반응·진단 정확도·교수 효과는 별도다.')
 updates = dict(zip(ACTIVITIES,['2026-04-02','2025-11-28','2026-09-29','2025-07-21','2025-10-13','2025-07-18','2025-07-25','2025-07-25']))
 new_log = [
  '새4개 개요와 공개55수준의 설명·텍스트 예·교수 도움·활동 목록 본문을 읽었다. 비교/순서23·덧셈/뺄셈12·수 합성11·곱셈/나눗셈9개다. Nonquantitative Sharer의Whe operating 오자를 포함해 본문 전체를 읽었으며 추출 표제 검색의 일시 오류로 나머지5쪽을 빼놓지 않았다.',
  '선정8활동의 영어 목표·절차·팁·자료·차별화·참고문헌을 실제 읽었다. Special Thanks 뒤에도 본문이 이어지므로 그 위치에서 잘라 읽지 않았다. 영어가 스페인어 표제 아래 반복된 부분은 별도 번역 검토/활동으로 세지 않았다.',
  '기존73개URL에 새67개URL을 더해 누적140개다. 현재20영역 목록에 대조하면 개요 읽기12개·남은8개다. 다른 영역/미선정 활동과 원본 이미지·영상·첨부·게임 실행은 새 읽기로 집계하지 않는다.',
  '두 영역의서로 겹치는Deriver/Problem Solver/Multidigit 설명은 동일한 연구나 독립 단계 수로 늘리지 않는다. 기존 홈페이지 해시는 한 기준 자산으로 유지하며140개 각HTML의 주소·해시를 따로 묶는다.',
 ]
 notes = dict(source_id=SOURCE,source_url=URL,source_asset_kind='publisher_html',source_asset_sha256=s['source_asset_sha256'],source_asset_redistributed=False,contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,date='2026-11-06',reviewer='Codex',read_scope=SCOPE,previous_review=copy.deepcopy(s),previous_bibliography=previous_b,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,observed_html_assets=all_assets,html_read_manifest=all_assets,read_groups=groups,new_read_groups=dict(domain_overviews=4,levels=55,activities=8,teacher_resources=0),reading_log=prior['reading_log']+new_log,source_corrections=prior['source_corrections']+corrections,activity_update_dates={**prior['activity_update_dates'],**updates},catalog_recheck=prior['catalog_recheck'],crosslisted_level_groups=[dict(level=name,urls=[URL+'math/'+d+'/'+name+'--'+suffix for d,suffix in [('adding-subtracting','addingsubtracting'),('composing-numbers','composing-numbers')]],independent_stages_counted=False) for name in ['deriver','problem-solver','multidigit']],unread_followups=[b['next_review'],'URL 수는 읽은 본문의 위치 수이며 독립 발달 단계·독립 연구 수가 아니다. 자체 수치·카드·봉지 활동은 원문 문항/영상/학생 반응의 복사가 아니다.'])
 for row in notes['crosslisted_level_groups']:
  assert set(row['urls']) <= {a['url'] for a in all_assets}
 npath = ROOT/NOTES; npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 history = s.get('snapshot_history',[]) + [dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=s['date'],read_scope=s['read_scope'])]
 s.update(date='2026-11-06',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),snapshot_history=history,bibliography_snapshot=digest(b),html_read_manifest=all_assets,read_scope=SCOPE,method_note='기존73개 본문에 수 비교/순서·덧셈/뺄셈·수 합성·곱셈/나눗셈의 개요4·수준55·활동8을 더했다. 본문 불일치·수치/미지 역할·중복 경로를 기록하고 이전 주장/관찰과 페이지별 주소·해시를 보존한다.',limits='누적140개 지정 영어 본문이다.20영역 중12개 개요를 읽었고 새4영역55수준 본문은 모두 읽었으나 전체 사이트·모든 활동·원본 그림/영상/첨부·게임·원연구·교재 전권은 미검토다. 겹치는 수준 URL은 독립 단계/연구로 세지 않으며0–8세 자원을 국내 학년 전체·현재 효과·진단 규준·유일한 경로로 사용하지 않는다. 원문 수/미지 역할·목표/절차·넓이 도움 문구의 불일치를 복사하지 않는다.',editorial_action='기존주장11건·자체 관찰11건을 보존하고10개 기준에 새 주장4건·자체 관찰4건을 추가했다. 누적30개 기준·주장15건·관찰15건이며 관계 검토·독립 검토·학생 검증으로 합산하지 않는다.',observations=s['observations']+OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 assert len({c for v in registry['claims'] if v['source_id'] == SOURCE for c in v['standard_codes']}) == 30
 p.write_text(json.dumps(bibliography,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p = ROOT/'data/content_review_queue.json'; q = json.loads(p.read_text(encoding='utf-8'))
 row = next(v for v in q['literature_review'] if v['source']['id'] == SOURCE)
 row.update(source=b,claim_ids=[c['id'] for c in registry['claims'] if c['source_id'] == SOURCE])
 p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])] == old['claims']
 assert s['observations'][:11] == old['sources'][SOURCE]['observations']
 assert all(registry['sources'][k] == v for k,v in old['sources'].items() if k != SOURCE)
 assert load_reviews() == relations
 build_report(); print('Extended LT2:67 new public HTML bodies,4 claims,4 own observations; prior evidence preserved')

if __name__ == '__main__':
 main()

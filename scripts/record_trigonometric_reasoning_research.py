"""Map angle, trigonometric graph, and triangle-law studies to scoped evidence."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from extend_making_pre_k_count_appendices_review import DATE
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_conic_representation_research import probe
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


CACHE = ROOT / 'tmp/literature/trigonometric-reasoning'
AG = 'AKKOC_GUL_2010_RADIAN'
MA = 'MOORE_2013_ANGLE_MEASURE'
MZ = 'MOORE_2014_SINE_FUNCTION_ZAC'
WB = 'WEBER_2005_TRIGONOMETRIC_FUNCTIONS'
HZ = 'HERIZAL_2025_TRIANGLE_PROOFS'
MK = 'MAKNUN_ET_AL_2020_TRIGONOMETRIC_GRAPHS'
ANGLE, GRAPH, LAWS = [f'12대수02-0{i}' for i in range(1, 4)]
SPECS = {
    AG: dict(year=2010, authors=['Hatice Akkoç', 'Nihal Akbaş Gül'],
        title='Analysis of a Teaching Approach Aiming at Eliminating Student Difficulties with Radian',
        url='https://doi.org/10.1501/Egifak_0000001192',
        pdf_url='https://dergipark.org.tr/download/article-file/508917',
        stem='akkoc-gul-2010', sha256='0f453087c2d8cbffc1066f575ed29c4452975d77b81afb47ae31c1ab66d1b03a',
        total=33, pages=[1, 2, 9, 10, 16, 23, 24, 28], visuals=[16, 23],
        scope='두 반의 설계와 호도법 면담에서 도 기호 유무와 단위원을 연결한 사례, 표 11의 설명 범위를 확인했다.',
        limit='세 쌍을 선별해 비교했다. 개별 대화를 전체 분반의 빈도나 국내 학생의 학습 효과로 해석하지 않는다.',
        design='같은 교사가 두 방식으로 가르친 두 반의 선정 사례를 질적으로 비교.',
        sample='튀르키예 고교 10학년 두 반 14명과 11명. 주요 사례는 두 반에서 뽑은 세 쌍.',
        supports=['도 기호가 없는 삼각함수 입력', '호도법의 정의와 적용']),
    MA: dict(year=2013, authors=['Kevin C. Moore'],
        title='Making Sense by Measuring Arcs: A Teaching Experiment in Angle Measure',
        url='https://doi.org/10.1007/s10649-012-9450-6',
        pdf_url='https://www.squaresandcircles.me/_files/ugd/bcc7ab_846fcb44a701452cadcdb32f675006dc.pdf',
        stem='moore-2013', sha256='93c7d161064c445010e38162e7eddce18fadc168a40a190570ef57c865c49183',
        total=22, pages=[1, 2, 6, 13, 14, 18, 20], visuals=[14],
        scope='참가자와 각 측정 과제, 원의 크기와 관계없이 호 길이를 반지름의 몇 배인지 설명하는 면담을 대조했다.',
        limit='두 학생에 초점을 둔 대학 수업 사례이며 2014년 사인함수 보고의 한 사례와 겹친다.',
        design='예비 미적분 수강생이 각을 수량화하는 방식을 관찰한 수업 실험.',
        sample='미국 대학 자원자 3명 가운데 본문은 두 학생을 중심으로 분석.',
        supports=['원의 크기와 무관한 호 길이와 반지름의 비']),
    MZ: dict(year=2014, authors=['Kevin C. Moore'],
        title='Quantitative Reasoning and the Sine Function: The Case of Zac',
        url='https://doi.org/10.5951/jresematheduc.45.1.0102',
        pdf_url='https://www.squaresandcircles.me/_files/ugd/bcc7ab_a7049a81ff8a4abc9f35fc95e0e42421.pdf',
        stem='moore-zac-2014', sha256='ceb90daf3d1b2556b522fb70c11228203ef0994635832b781ee74f4d2f874d2f',
        total=38, pages=[1, 2, 12, 13, 21, 22, 32], visuals=[21, 32],
        scope='같은 수업 실험의 Zac 사례에서 호 길이로 각을 구하고 사인·코사인을 좌표로 바꾸는 그림 12·13과 직각삼각형 설명을 대조했다.',
        limit='한 학생의 수행이다. 2013년 각 측정 연구와 참가 사례를 합산하지 않으며 모든 사분면이나 세 함수의 주기 성취를 입증하지 않는다.',
        design='다섯 차례 수업 실험에 참여한 학생 한 명의 사인 의미를 상세 분석.',
        sample='미국 대학 예비 미적분 수강생 한 명. 앞선 각 측정 논문에 포함된 동일 사례.',
        supports=['호 길이와 사인 입력의 연결', '단위원 좌표와 직각삼각형의 비']),
    WB: dict(year=2005, authors=['Keith Weber'],
        title="Students' Understanding of Trigonometric Functions",
        url='https://eric.ed.gov/?id=EJ747914',
        pdf_url='https://files.eric.ed.gov/fulltext/EJ747914.pdf',
        stem='weber-trig-2005', sha256='dce7a5ee9c4d0a3ead4f18a40199ffe6c1fdf1ecb8c272343f81473f3cd966d9',
        total=22, pages=[1, 5, 12, 13, 14, 15], visuals=[14],
        scope='두 대학 강좌의 연구 배치와 교수 실험 반의 사후 검사 표 4, 단위원 좌표의 정당화 사례를 확인했다.',
        limit='서로 다른 강좌의 비교다. 사후 검사 40명 중 사전 0점인 26명은 같은 표본의 일부다.',
        design='두 대학 삼각함수 강좌의 면담과 지필 과제를 이용한 분석.',
        sample='사후 검사 표 4의 교수 실험 반 40명. 사전 0점인 하위 집단은 26명.',
        supports=['사인·코사인의 부호와 값', '값의 선택과 정당화']),
    HZ: dict(year=2025, authors=['Herizal'],
        title='Identifikasi kesalahan pembuktian matematis siswa pada materi aplikasi trigonometri',
        url='https://doi.org/10.61291/jpi.v6i2.74',
        pdf_url='https://jurnalpendidikindonesia.com/index.php/jpi/article/download/80/64/266',
        stem='herizal-2025', sha256='6489af913269b00babd5444bca72190c70edd07ac40585bb16035288f82ee177',
        total=11, pages=[1, 3, 4, 5, 6, 7, 8], visuals=[5, 7, 8],
        scope='사인법칙의 각·대변 대응, 넓이의 끼인각, 코사인법칙을 변형한 학생 풀이와 후속 면담을 확인했다.',
        limit='인도네시아 한 학교의 지필·면담 사례다. 각 오류의 일반 빈도나 SSA 비유일성에 관한 결과를 확인한 연구가 아니다.',
        design='네 증명 문항과 일부 응답에 대한 후속 면담.',
        sample='인도네시아 반둥의 고교 10학년 30명.',
        supports=['사인법칙과 넓이 공식의 서로 다른 각', '코사인법칙의 분모와 이항 부호']),
    MK: dict(year=2020, authors=['Churun Lu’lu’il Maknun', 'Rizky Rosjanuardi', 'Al Jupri'],
        title='Didactical Design on Drawing and Analysing Trigonometric Functions Graph through a Unit Circle Approach',
        url='https://doi.org/10.29333/iejme/9275',
        pdf_url='https://www.iejme.com/download/didactical-design-on-drawing-and-analysing-trigonometric-functions-graph-through-a-unit-circle-9275.pdf',
        stem='maknun-et-al-2020', sha256='a4fdaf6d2a59d35e378a5446a9a3c622e62e33d3216de818ad0ca26dded7fd1b',
        total=19, pages=[1, 5, 7, 8, 10, 11, 13, 14, 16], visuals=[7, 14],
        scope='단위원에서 그래프로 옮기는 사전 과제와 수업 대화, 사인과 탄젠트의 반복 간격에 대한 답변을 확인했다.',
        limit='수업 설계와 관찰 사례다. 대화에 나온 응답을 참가자 65명의 비율로 환산하지 않는다.',
        design='교수 설계와 수업 관찰 및 면담·학생 산출물의 질적 분석.',
        sample='인도네시아 공립 고교 10학년 65명.',
        supports=['각과 단위원 좌표를 함수 그래프로 옮기기', '주기와 최소 양의 주기']),
}

CLAIMS = [
    (AG, 'AG10-01', [ANGLE, GRAPH], [16, 23],
     '면담에서 도 표시가 없는 sin 30을 처음에 1/2로 답한 뒤 도 기호가 없다는 지적을 받고 라디안으로 해석한 사례가 있다.',
     '도 기호의 유무를 스스로 확인한 반응과 연구자 질문 뒤의 반응을 구별한다. 참가자 전체의 오류율로 쓰지 않는다.'),
    (AG, 'AG10-02', [ANGLE], [9, 23, 24],
     '표 11의 비교에서는 두 학생이 라디안의 정의를 말했지만, 그 정의를 1라디안과 단위원에 대한 설명에 사용한 응답은 한쪽에서만 나왔다.',
     '선정 사례의 과제별 관찰이다. 호의 길이와 각의 크기를 구별하고 정의 회상을 적용 능력으로 대신 판정하지 않는다.'),
    (MA, 'MA13-01', [ANGLE], [6, 14, 18, 20],
     '학생들은 서로 다른 크기의 원에서 반지름 길이의 끈으로 원둘레를 재고 같은 수의 반지름으로 잰 호가 같은 크기의 각을 만든다고 설명했다.',
     '측정과 대화에 기반한 두 학생 사례다. 같은 각에서 실제 호 길이와 호 길이의 반지름에 대한 비를 구별한다.'),
    (MZ, 'MZ14-01', [ANGLE, GRAPH], [12, 21, 22],
     'Zac은 반지름 2 km인 원에서 이동 거리 2.2 km를 반지름으로 나눈 값 1.1을 각의 입력으로 쓰고, 사인·코사인에서 구한 비를 실제 좌표로 바꿨다.',
     '각의 라디안 수치와 좌표의 반지름에 대한 비는 뜻이 다르다. 2013년 연구와 같은 학생의 사례다.'),
    (MZ, 'MZ14-02', [GRAPH], [21, 32],
     'Zac은 직각삼각형에서 빗변을 원의 반지름으로 보고, 각에 대응하는 변 길이의 비를 원에서 쓴 사인 의미와 연결했다.',
     '한 학생의 연결이다. 빗변을 기준 길이로 쓰는 설명과 사인 그래프의 주기나 탄젠트의 정의역 설명을 구분한다.'),
    (WB, 'WB05-01', [GRAPH], [13, 14, 15],
     '교수 실험 반 40명의 사후 검사에서 sin 270°를 −1로 답한 학생은 36명이고 그중 34명이 단위원에 근거한 타당한 이유를 제시했다.',
     '표 4의 정답 수와 이어지는 이유의 수를 구별한다. 사전 점수 0인 26명은 같은 40명에 포함된다.'),
    (HZ, 'HZ25-01', [LAWS], [3, 4, 5],
     '그림 1에는 사인법칙에서 한 변을 다른 각의 사인과 연결하고, 넓이 공식에서도 두 변의 끼인각이 아닌 각을 사용한 응답이 있다.',
     '대변과 끼인각은 서로 다른 역할이다. 면담에서 고친 설명을 최초 지필 답과 구분한다.'),
    (HZ, 'HZ25-02', [LAWS], [7, 8],
     '코사인법칙으로 각을 나타내는 과제에서 제곱항의 이항 부호를 틀리거나, 그림 3처럼 각이 달라져도 분모에 같은 두 변을 사용한 예가 보고됐다.',
     '대수 변형과 각 주변의 변 선택을 따로 관찰한다. 이 연구가 SSA의 두 해를 검사한 것으로 해석하지 않는다.'),
    (MK, 'MK20-01', [ANGLE, GRAPH], [5, 7, 10, 11],
     '표 2에서는 단위원 점의 좌표를 읽고 각과 함수값을 새로운 좌표평면으로 옮기는 순서를 제시한다. 사전 예상에는 두 좌표의 순서를 바꿀 가능성이 포함돼 있다.',
     '예상 오류와 실제 학생 응답을 구별한다. 원 위의 점과 그래프의 점을 동일한 두 좌표로 취급하지 않는다.'),
    (MK, 'MK20-02', [GRAPH], [13, 14],
     '사인 그래프의 반복 간격으로 π를 고른 응답이 있었고, 탄젠트에서는 먼저 2π를 답한 뒤 그래프를 다시 보고 π를 답하는 수업 대화가 제시됐다.',
     '탄젠트에서 2π도 주기이며 최소 양의 주기는 π다. 단일 점이나 한 구간의 모양만으로 반복을 판단하지 않는다.'),
]

OBSERVATIONS = {
    AG: [
        probe('AG-P1', ANGLE, '각 3과 3°가 표준 위치의 어느 사분면에 있는지 비교하고 두 코사인 값의 부호를 말하라.',
              '도 기호가 없는 3은 3라디안이다. π/2<3<π이므로 제2사분면이고 코사인은 음수다. 3°는 제1사분면이고 코사인은 양수다.',
              '수치와 단위를 먼저 읽고, 도와 라디안에서 부호가 달라지는 이유를 확인한다.'),
        probe('AG-P2', ANGLE, '반지름 4인 원에서 양의 x축을 기준으로 −π/2와 3π/2만큼 회전할 때 동경, 회전 방향, 각각 지나간 호의 길이를 비교하라.',
              '동경은 둘 다 음의 y축이다. 첫째는 시계 방향이고 길이 2π, 둘째는 반시계 방향이고 길이 6π다.',
              '끝 위치와 회전 방향 및 호의 길이를 나눈다. 음의 각에서도 실제 길이는 음수가 아니다.'),
    ],
    MA: [
        probe('MA-P1', ANGLE, '반지름 2 cm에서 길이 3 cm인 호와 반지름 6 cm에서 길이 9 cm인 호의 각을 비교하라. 두 번째 원에서 호 길이를 3 cm로 바꾸면 어떻게 되는가?',
              '처음 두 각은 둘 다 1.5라디안이다. 반지름 6 cm에 호 길이 3 cm이면 0.5라디안이다.',
              '같은 길이와 같은 각이 성립하는 조건을 구별하고 길이 단위가 비에서 없어지는 이유를 확인한다.'),
    ],
    MZ: [
        probe('MZ-P1', GRAPH, '반지름 6 m인 원에서 (6,0)부터 반시계 방향으로 호를 2π m만큼 따라갔다. 각의 라디안 수치, 단위원에서의 점, 실제 원에서의 점을 각각 구하라.',
              '각은 π/3라디안이다. 단위원에서는 (1/2,√3/2), 실제 좌표는 (3,3√3) m다. 각의 수치는 호 길이와 반지름의 비이고 좌표는 그 각에 대한 코사인·사인으로 정해진다.',
              '라디안 입력, 단위원의 좌표, 실제 길이 좌표를 분리한다.'),
    ],
    WB: [
        probe('WB-P1', GRAPH, '단위원에서 각 7π/6의 점을 표시하고 코사인, 사인, 탄젠트의 값을 설명하라. 같은 각에 대응하는 사인 그래프의 점도 적어라.',
              '제3사분면에서 기준각 π/6이므로 원 위의 점은 (−√3/2,−1/2)다. 코사인·사인은 각각 가로·세로좌표이며 탄젠트는 세로를 가로로 나눈 √3/3이다. 사인 그래프의 점은 (7π/6,−1/2)다.',
              '단위원 좌표와 부호의 근거, 탄젠트의 분모가 0이 아닌 조건을 따로 확인한다.'),
    ],
    HZ: [
        probe('HZ-P1', LAWS, '삼각형에서 b=5, c=7, 끼인각 A=60°다. 대변 a와 넓이를 구하고, 사인법칙에서 a가 어느 각의 사인과 짝인지 설명하라.',
              'a²=25+49−70·(1/2)=39여서 a=√39다. 넓이는 (1/2)·5·7·(√3/2)=35√3/4다. 사인법칙에서 a는 대각 A의 사인과 짝을 이룬다.',
              '두 변의 끼인각을 쓰는 과제와 각의 대변을 쓰는 과제를 구분한다.'),
        probe('HZ-P2', LAWS, '삼각형에서 A=30°, a=5, b=5√2다. 사인법칙으로 얻는 B의 후보를 모두 구하고 두 후보가 각각 실제 삼각형을 만드는지 설명하라.',
              'sin B=√2/2여서 B는 45° 또는 135°다. C는 각각 105°와 15°로 모두 양수이고, 각 후보에서 사인법칙으로 양의 c를 얻으므로 두 삼각형이 가능하다.',
              '각과 대변을 맞춘 뒤 사인 값이 같은 두 각과 내각 합 조건을 확인한다.'),
    ],
    MK: [
        probe('MK-P1', GRAPH, 'π만큼 옮기는 것이 사인의 주기인지 예를 들어 판단하라. 탄젠트에서는 π와 2π 중 어느 것이 최소 양의 주기이며, 다른 값도 주기인지 설명하라.',
              'sin(π/2)=1, sin(3π/2)=−1이므로 π는 사인의 주기가 아니다. 탄젠트는 π를 더하면 분자와 분모가 함께 부호를 바꿔 값과 정의역을 보존한다. 양의 주기는 tan 0=0을 유지해야 하고 가장 작은 양의 영점은 π이므로 π가 최소다. 2π도 주기다.',
              '같은 함수값이 나오는 한 점과 전체 정의역의 반복, 그리고 최소 양의 주기를 구별한다.'),
    ],
}

def main():
    registry = load_registry()
    if set(SPECS) <= registry['sources'].keys():
        build_report()
        return
    assert not set(SPECS).intersection(registry['sources'])
    image_hashes = {}
    for sid, spec in SPECS.items():
        path = CACHE / f'{spec["stem"]}.pdf'
        assert sha(path) == spec['sha256']
        reader = PdfReader(path)
        assert len(reader.pages) == spec['total']
        assert all(reader.pages[p - 1].extract_text().strip() for p in spec['pages'])
        image_hashes[sid] = {str(p): sha(CACHE / 'rendered' / f'{spec["stem"]}-{p}.png') for p in spec['visuals']}
    details = {
        AG: dict(class_sizes=[14, 11], qualitative_pairs=3, hours_per_class=8,
                 prompted_reinterpretation_of_unmarked_input=True, table_11_comparison_students=2),
        MA: dict(enrolled=3, focus_students=2, participant_overlap_with_moore_2014=True),
        MZ: dict(focus_students=1, sessions=5, overlap_source=MA, radius_km=2, arc_km=2.2, angle_rad=1.1,
                 radian_and_coordinate_ratio_terminology_separated=True),
        WB: dict(posttest_n=40, zero_pretest_subset_n=26, sin_270_correct_n=36, sin_270_justification_n=34),
        HZ: dict(n=30, proof_items=4, ssa_ambiguity_tested=False, observed_error_figures=[1, 3]),
        MK: dict(n=65, grade=10, separates_anticipated_and_observed=True, least_tangent_period='π',
                 two_pi_is_also_tangent_period=True),
    }
    corrections = {
        AG: '분반 수 14·11과 두 반에서 고른 사례 세 쌍을 구별한다. 도 기호가 없다는 질문 후의 반응을 별도로 기록했다.',
        MA: '둘레의 실제 길이와 반지름을 단위로 삼은 2π를 구별했다. 2014년 논문과 겹치는 사례를 합산하지 않는다.',
        MZ: '그림 13과 각주 5에 따라 각의 단위 라디안과 좌표 길이의 비를 구별했다. 이 논문은 2013년 논문과 같은 수업 실험의 분석이다.',
        WB: '표 4의 26명은 40명 안의 하위 집단이다. sin 270°의 정답 36명과 정당화 34명을 구별했다.',
        HZ: '그림 1의 각·대변 대응 오류와 그림 3의 코사인법칙 분모 오류를 구별했다. PDF 7쪽의 문항 제목은 3번이고 첫 문단 끝의 2번 표기는 그대로 확인하되 집계 근거로 삼지 않는다.',
        MK: '본문의 탄젠트 2π에서 π로 바뀐 답은 최소 양의 주기를 구하는 상황으로 읽었다. 2π 자체도 탄젠트의 주기다.',
    }
    bibliography, queue = load(ROOT / 'data/sources.json'), load(ROOT / 'data/content_review_queue.json')
    assert not set(SPECS).intersection(row['id'] for row in bibliography)
    assert not set(SPECS).intersection(row['source']['id'] for row in queue['literature_review'])
    pdf_urls = {}
    for sid, spec in SPECS.items():
        url = spec['url']
        pdf_urls[sid] = spec['pdf_url']
        empirical = dict(design=spec['design'], sample_description=spec['sample'], inference_limit=spec['limit'],
            student_outcome_study=True, causal_effect_established=False, local_effect_tested=False)
        entry = dict(id=sid, year=spec['year'], url=url, title=spec['title'], authors=spec['authors'], kind='각의 측정과 삼각함수의 학생 추론 연구',
            review_scope=spec['scope'], does_not_establish=spec['limit'], supports=spec['supports'],
            next_review='자체 과제의 실제 응답을 확인하고 다른 표본의 삼각함수 과제를 추가 대조한다.')
        bibliography.append(entry)
        note = f'data/literature_evidence/{sid}_review_notes.json'
        write(ROOT / note, dict(source_id=sid, source_url=url, source_pdf_url=pdf_urls[sid],
            source_asset_kind='pdf', source_pdf_sha256=spec['sha256'], pdf_pages=spec['total'],
            selected_text_pages=spec['pages'], visual_pdf_pages=spec['visuals'], rendered_page_sha256=image_hashes[sid],
            date=DATE, reviewer='Codex', read_scope=spec['scope'], empirical_scope=empirical,
            contains_source_full_text=False, source_pdf_redistributed=False,
            reading_log=[spec['scope']], source_corrections=[dict(location='정의·표·학생 응답', issue=corrections[sid])],
            trigonometry_review=details[sid]))
        registry['sources'][sid] = dict(source_id=sid, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
            snapshot_kind='authored_review_notes', source_asset_kind='pdf', source_pdf_sha256=spec['sha256'],
            snapshot_file=note, snapshot_sha256=sha(ROOT / note), redistribution_license='workspace_authored_notes',
            bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=url,
                authors_year=f'{spec["authors"][0]}{" 외" if len(spec["authors"]) > 1 else ""}, {spec["year"]}'),
            read_scope=spec['scope'], limits=spec['limit'], empirical_scope=empirical, scope_note='표현과 문항 및 응답 범위를 구별한다.',
            method_note='출판 원문과 지정 판면에서 분석 표본·문항별 응답·설명 범위를 대조했다.',
            editorial_action='문헌 근거와 자체 관찰 과제를 반영했다.',
            independent_review=False, student_validated=False, observations=OBSERVATIONS[sid])
        queue['literature_review'].append(dict(source=entry, status='self_read_claim_mapping',
            evidence_file='data/literature_claim_reviews.json', claim_evidence_fields=spec['supports'],
            claim_ids=[cid for src, cid, *_ in CLAIMS if src == sid]))
    new = {}
    for sid, cid, codes, pages, support, limit in CLAIMS:
        new[cid] = dict(id=cid, source_id=sid, role='empirical_result_with_scope',
            empirical_scope=registry['sources'][sid]['empirical_scope'], standard_codes=codes,
            locations=[f'{pdf_urls[sid]}#page={p}' for p in pages], support=support, does_not_establish=limit,
            independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes})
    registry['claims'].extend(new.values())
    relations = load(ROOT / 'data/revised_relations.json')['relations']
    pairs = {(r['id'], cid) for r in relations for cid, claim in new.items()
             if all(r[k].startswith('standard:') for k in ('from', 'to'))
             and {r[k][9:] for k in ('from', 'to')} <= set(claim['standard_codes'])}
    interpretations = {
        ('HA-trig-graphs', 'AG10-01'): ('inference_limit',
            '같은 숫자라도 도 기호가 있는 입력과 라디안 입력을 서로 다르게 해석해야 한다. 면담에서는 익숙한 수의 단위를 바꿔 읽은 사례가 있었다.',
            '단위를 확인한 뒤의 응답을 자발적 판단이나 그래프 전반의 숙달로 해석하지 않는다.'),
        ('HA-trig-graphs', 'MZ14-01'): ('activity_context',
            '호 길이를 반지름으로 나누어 회전각을 구하고, 단위원 좌표에 반지름을 곱해 실제 좌표로 되돌린다.',
            '같은 수업 실험의 한 학생 사례다. 좌표의 비를 라디안으로 부른 표현은 수업용 예로 옮기지 않는다.'),
        ('HA-trig-graphs', 'MK20-01'): ('activity_context',
            '단위원의 점 (cos θ,sin θ)와 사인 그래프의 점 (θ,sin θ)를 각각 쓰고 가로좌표의 의미를 설명한다.',
            '저자의 사전 예상과 수업에서 관찰된 연결을 구분한다. 이 사례로 일반각이 그래프 이해의 필수 선수임을 확정하지 않는다.'),
    }
    assert pairs == interpretations.keys()
    reviewed = load(ROOT / FILE)
    by_relation = {r['id']: r for r in relations}
    for (rid, cid), (role, finding, limit) in interpretations.items():
        claim = new[cid]
        reviewed['records'].append(dict(relation_id=rid, claim_id=cid, role=role, finding=finding, limit=limit,
            relation_snapshot=relation_snapshot(by_relation[rid]),
            claim_snapshot=claim_snapshot(claim, registry['sources'][claim['source_id']])))
    apply_literature_context(relations, registry, registry=reviewed)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviewed)
    build_report()
    print('Trigonometry: 6 sources, 10 claims, 8 tasks, 3 relation entries')


if __name__ == '__main__':
    main()






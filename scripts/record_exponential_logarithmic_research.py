"""Map reviewed exponent and logarithm studies to scoped claims and original probes."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from extend_making_pre_k_count_appendices_review import DATE
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_conic_representation_research import probe
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


CACHE = ROOT / 'tmp/literature/exponential-logarithmic-reasoning'
WL = 'WEBER_2002_EXPONENTIAL_LOG_INTERVIEWS'
WT = 'WEBER_2002_EXPONENT_LOG_PILOT'
KL = 'KASTBERG_2002_LOGARITHMIC_FUNCTION'
EG = 'ELLIS_ET_AL_2016_EXPONENTIAL_GROWTH'
ROOTS, EXT, LAW, LOG, COMMON, INV, GRAPH, MODEL = [f'12대수01-0{i}' for i in range(1, 9)]
SPECS = {
    WL: dict(year=2002, authors=['Keith Weber'],
        title="Students' Understanding of Exponential and Logarithmic Functions",
        url='https://eric.ed.gov/?id=ED477690',
        pdf_url='https://files.eric.ed.gov/fulltext/ED477690.pdf',
        stem='weber-ed477690', sha256='14f63e74dcac27b5466de992b930b483b3aec23ba1898a7c7362f18c8ee8a8ec',
        total=10, pages=[1, 4, 5, 6, 7], visuals=[5, 6, 7],
        scope='ERIC 원문에서 지수·로그법칙 회상과 설명, 감소함수 판단과 이유, 계산기 없이 로그를 구하는 면담을 대조했다.',
        limit='미국 대학의 자원자 15명이다. 같은 저자의 교수 실험과 참여자 중복을 확인하지 못해 합산하지 않는다.',
        design='예비 미적분 수업에서 해당 내용을 배운 뒤 3주 후 시행한 면담.',
        sample='미국 남부 한 대학의 예비 미적분 수강생 자원자 15명.',
        supports=['지수법칙과 로그법칙의 연결 설명', '지수함수의 감소 판단과 이유']),
    WT: dict(year=2002, authors=['Keith Weber'],
        title="Developing Students' Understanding of Exponents and Logarithms",
        url='https://eric.ed.gov/?id=ED471763',
        pdf_url='https://files.eric.ed.gov/fulltext/ED471763.pdf',
        stem='weber-ed471763', sha256='a853e0d7b8d62a6caa486bf0b0baa997ce9c70641a4a8f90f9825e0760920bcf',
        total=11, pages=[1, 5, 6, 7, 8, 9], visuals=[6, 7, 8],
        scope='문항지, 그림 1과 본문의 계산·설명 범위, 교수 실험 두 반의 배치와 저자 지적 한계를 대조했다.',
        limit='담당 교사가 다른 두 분반의 자원자 비교다. 자료 자체의 인과 효과나 다른 Weber 연구와의 표본 독립성은 확인하지 못했다.',
        design='교수 실험과 기존 수업의 두 분반에서 3주 뒤 개별 면담.',
        sample='미국 남부 지역 대학의 대학 대수·삼각함수 수강생, 반별 자원자 15명.',
        supports=['제곱근을 분수 지수로 쓰는 이유', '지수 연산을 거꾸로 사용해 로그 찾기']),
    KL: dict(year=2002, authors=['Signe Elizabeth Kastberg'],
        title='Understanding Mathematical Concepts: The Case of the Logarithmic Function',
        url='https://openscholar.uga.edu/record/9605?ln=en',
        pdf_url='https://openscholar.uga.edu/record/9605/files/kastberg_signe_e_200205_phd.pdf',
        stem='kastberg-2002', sha256='a1bb119f57c2f7e8efe6dae436690c7d0708c768450b8a00f3a08d0f3233cb91',
        total=216, pages=[1, 175, 176, 177], visuals=[176, 177],
        scope='학위논문의 초록과 PDF 175~177쪽의 5~7차 면담 정리에서 지수식 역변환, 근사, 선형 보간과 반례 반응을 확인했다.',
        limit='전문대 두 분반에서 선발한 네 명의 사례다. 선정한 면담 분석 범위로 해석하고 학위논문 전체나 일반적 효과로 확대하지 않는다.',
        design='수업 전·중·후의 면담과 관찰 등을 사용한 네 학생 사례 연구.',
        sample='미국 남동부 농촌 지역의 전문대 대수 두 반에 속한 학생 네 명.',
        supports=['상용로그와 밑 10 지수식의 왕복', '로그를 선형으로 보간하는 오류']),
    EG: dict(year=2016, authors=['Amy B. Ellis', 'Zekiye Ozgur', 'Torrey Kulow', 'Muhammed F. Dogan', 'Joel Amidon'],
        title="An Exponential Growth Learning Trajectory: Students’ Emerging Understanding of Exponential Growth Through Covariation",
        url='https://doi.org/10.1080/10986065.2016.1183090',
        pdf_url='https://pat-thompson.net/RUME1F18Public/files/349436.pdf',
        stem='ellis-et-al-2016', sha256='908bc73187427ca0c6ba2f1fea4e9b059849fb4febb38cb25a928c2be8c4bfba',
        total=32, pages=[1, 2, 7, 13, 25, 26], visuals=[7, 25, 26],
        scope='두 수업 실험의 참가 범위, 초기 성장률 설명, 그림 8~10에서 대응식과 공변 추론의 변화와 차이를 대조했다.',
        limit='미국 중학생의 수업 사례다. 개인별 경로와 수업 활동의 순서를 구별하며 고교에서 보편적인 단계나 효과로 적용하지 않는다.',
        design='서로 다른 두 수업 실험에서 높이와 시간의 공변을 분석.',
        sample='첫 실험은 8학년 5명 참여·3명 정기 참여 자료 분석, 둘째는 8학년을 마친 8명 참여.',
        supports=['같은 입력 간격과 일정 배율', '여러 단위 시간의 배율에서 한 단위 배율을 구하는 추론']),
}

CLAIMS = [
    (WL, 'WL02-01', [LAW, LOG], [5],
     '예비 미적분 자원자 15명의 면담에서 같은 밑의 거듭제곱 곱 법칙과 로그 합 법칙을 각각 6명이 답했다. 두 규칙의 연결을 설명한 참여자는 없었다.',
     '각각 6명이라는 값은 두 문항의 집계다. 동일한 6명이 두 규칙을 답했는지와 학습 순서는 알 수 없다.'),
    (WL, 'WL02-02', [GRAPH], [6, 7],
     '밑이 1/2인 지수함수의 감소 여부를 15명 모두 답했고, 저자가 수학적 이유를 들었다고 분류한 응답은 2명이었다.',
     '감소 판단, 정수 지수 예시, 모든 실수 입력의 감소를 보이는 이유를 구분한다. 보고된 두 설명을 실수 전체에서의 증명으로 세지 않는다.'),
    (WT, 'WT02-01', [ROOTS, EXT], [5, 6, 8],
     '교수 실험 분반의 면담에서 6명이 제곱근을 1/2제곱으로 나타내는 이유를 설명했다. 문항지에는 식과 이유를 함께 묻는 항목이 있다.',
     '분반 비교로 임의의 유리·실수 지수 일반화나 음수 밑 거듭제곱 설명을 검증한 것으로 보지 않는다.'),
    (WT, 'WT02-02', [LOG, INV], [5, 6, 8],
     '밑 5의 로그 문항에서 비교 분반 8명은 대응하는 지수방정식으로 바꿨으나 구하는 방법을 제시하지 못했다. 교수 실험 분반에서는 4명이 반복 곱셈을, 한 명은 반복 나눗셈을 제안했다.',
     '정수 지수에 해당하는 특정 진수의 응답이다. 대응식 쓰기와 계산 전략, 모든 양수 진수에서의 역함수 설명을 따로 판단한다.'),
    (KL, 'KL02-01', [COMMON, INV], [175, 176, 177],
     '7차 면담에서 네 학생은 상용로그 1의 값이 0임을 밑 10 지수식으로 바꾼 뒤, 지수방정식과 계산기로 표의 다른 값을 차례로 근사했다.',
     '이 사례가 상용로그의 성질이나 자릿수·생활 문제 전반의 수행을 보여 주지는 않는다.'),
    (KL, 'KL02-02', [LOG, GRAPH], [176, 177],
     '세 참여자가 수직선에서의 덧셈 간격을 로그 값에도 그대로 적용하는 선형 보간을 사용했다. 한 참여자는 연구자의 반례를 보고 자신의 로그 곱 규칙과 보간 결과의 불일치를 알아차렸다.',
     '최초 반응, 반례 제시, 수정 뒤 설명을 구분한다. 상용로그에서 본 사례를 밑이 다른 모든 함수의 오류율로 확대하지 않는다.'),
    (EG, 'EG16-01', [GRAPH, MODEL], [7, 13, 25, 26],
     '초기에는 빠르거나 몇 배라는 말에서 시간이 빠진 응답이 있었다. 한 사례에서는 이후 시작점에 제한하지 않고 두 시점의 시간 차만큼 성장 인수를 거듭제곱해 값을 비교했다.',
     '해당 사례에서 보인 공변과 대응 추론은 각각 관찰된 수행이다. 모형이 맞는 구간, 성장 인수의 단위, 학생별 변화 경로를 구별한다.'),
    (EG, 'EG16-02', [EXT, MODEL], [7, 25, 26],
     '상세하게 제시된 세 사례 중 한 학생에게서 두 시점의 출력 비에 시간 차의 차수로 근을 취해 한 단위 성장 인수를 구하는 추론이 보고됐다.',
     '나머지 두 사례에 같은 추론이 관찰되지 않았다는 사실을 전체 참여자의 실패 비율로 해석하지 않는다. 일정 배율이라는 모형 조건이 필요하다.'),
]

OBSERVATIONS = {
    WL: [
        probe('WL-P1', LAW, '2ᵘ·2ᵛ와 2ᵘ+2ᵛ 중 어느 식에 지수의 합 법칙을 쓸 수 있는가? u=2, v=3으로 두 식을 확인하고 곱에서 두 지수가 더해지는 이유를 설명하라.',
              '곱에서만 2ᵘ⁺ᵛ를 얻는다. 예에서 곱은 4·8=32, 합은 4+8=12다. 두 양의 정수 지수에서 밑 2의 인수 개수를 합하는 설명이 가능하다.',
              '곱·합을 구별하고 자연수에서 인수 개수 설명과 일반 지수에서의 법칙 사용을 나누어 기록한다.'),
        probe('WL-P2', GRAPH, 'f(x)=(1/3)ˣ에서 x가 1 증가할 때의 비를 구하라. 이어 임의의 두 실수 s<t에 대해 f(s)와 f(t)의 대소를 설명하라.',
              '단위 간격의 비는 1/3이다. h=t−s>0이면 f(t)/f(s)=(1/3)ʰ<1이므로 f(t)<f(s)다.',
              '정수 간격의 예시와 양의 실수 간격을 이용한 일반 설명을 구별한다.'),
    ],
    WT: [
        probe('WT-P1', ROOTS, '√16, 16의 1/2제곱, x²=16의 실수해를 각각 말하고 16의 1/2제곱에 4가 선택되는 이유를 설명하라.',
              '√16과 16의 1/2제곱은 모두 4다. 16의 1/2제곱을 제곱하면 16이 되고 양의 밑의 실수 거듭제곱은 양수다. 방정식의 실수해는 ±4다.',
              '대표 근호값·거듭제곱의 양수 조건·방정식의 두 해를 각각 확인한다.'),
        probe('WT-P2', INV, '계산기 없이 log₃(1/27)을 구하고 지수식으로 확인하라. 이어서 log₃0도 같은 방식으로 정의할 수 있는지 설명하라.',
              '3을 세 번 곱하면 27이므로 3⁻³=1/27이고 답은 −3이다. 모든 실수 x에 대해 3ˣ>0이므로 log₃0은 실수에서 정의되지 않는다.',
              '지수의 음수와 진수의 양수 조건을 구별하고, 역관계에서 입력 집합을 확인한다.'),
    ],
    KL: [
        probe('KL-P1', COMMON, '양의 정수 n이 10²≤n<10³이면 상용로그 log n이 어느 범위에 있는지 설명하라. n=999와 n=1000의 자릿수를 비교하고 경계에서 바뀌는 이유를 말하라.',
              '2≤log n<3이다. 999는 세 자리이고 1000=10³은 네 자리다. 상용로그를 거꾸로 10의 지수와 연결하면 경계의 포함 여부를 알 수 있다.',
              '로그를 지수식으로 바꾸는 절차와 정수 자릿수 경계의 부등호를 따로 확인한다.'),
        probe('KL-P2', LOG, 'log₂5가 log₂2와 log₂8의 평균인지 판단하라. 두 로그의 평균에 해당하는 진수를 찾아 그 이유를 설명하라.',
              '두 로그는 1과 3이라 평균은 2이고 그 진수는 4다. 두 로그의 합을 2로 나누면 log₂(√(2·8))이다. 5는 두 진수의 산술평균이고 log₂4<log₂5다.',
              '진수의 산술평균을 그대로 옮기는 반응과 로그법칙으로 기하평균을 유도하는 반응을 구별한다.'),
    ],
    EG: [
        probe('EG-P1', MODEL, '높이가 2일째 100, 4일째 400인 모형에서 하루 배율이 일정하다고 가정하자. 하루 배율과 5일째 높이를 구하고 단순히 하루마다 같은 양을 더한 모형과 비교하라.',
              '이틀 동안 4배이므로 하루 배율은 2다. 지수 모형의 5일째 값은 800이다. 두 관측값을 잇는 선형 모형은 하루 150씩 더해 5일째 값이 550이다.',
              '두 점에 모두 맞는 서로 다른 모형을 비교하고 관측 범위 밖의 값이 가정에 의존함을 설명한다.'),
        probe('EG-P2', EXT, '같은 길이의 시간 구간에 같은 배율을 적용하는 연속 지수 모형에서 하루 배율이 9라면 반나절 배율을 구하라. 하루 배율을 2로 나누지 않는 이유도 설명하라.',
              '반나절 배율의 제곱이 9이고 배율은 양수이므로 9의 1/2제곱인 3이다. 두 시간 구간의 배율은 더하는 대신 곱한다.',
              '시간 간격은 덧셈으로, 배율은 곱셈으로 결합하며 양의 값을 선택하는지 확인한다.'),
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
        WL: dict(n=15, postinstruction_weeks=3, power_product_rule_correct=6, log_sum_rule_correct=6,
                 rule_connection_explanations=0, decreasing_judgment=15, decrease_explanations_author_classification=2,
                 overlap_with_pilot_verified=False),
        WT: dict(arm_sizes=[15, 15], postinstruction_weeks=3, different_instructors=True,
                 square_root_explanations_experimental=6, log_equation_only_control=8,
                 log_repeat_multiply_experimental=4, log_repeat_divide_experimental=1,
                 overlap_with_interviews_verified=False),
        KL: dict(n=4, study_interviews=9, topic_approximation_interview=7,
                 selected_pdf_to_printed_pages={175:168, 176:169, 177:170},
                 whole_dissertation_reviewed=False),
        EG: dict(first_experiment_enrolled=5, first_experiment_regular_analyzed=3,
                 second_experiment_enrolled=8, detailed_trajectory_cases=3,
                 unit_multiplier_root_reasoning_reported_cases=1),
    }
    corrections = {
        WL: '스캔에서 근호·위첨자가 잘못 추출되는 부분은 판면과 구별했다. 규칙별 6명은 교차표가 아니며, 수학적 설명 2명은 원저자의 분류다.',
        WT: '그림 1의 정답과 PDF 6·8쪽 본문의 설명 사례는 다른 결과로 기록했다. 저자가 교수 실험 반의 교사와 연구자를 겸했다는 한계를 남겼다.',
        KL: 'PDF 176쪽의 인쇄 169쪽을 확인했다. √2 표기와 보간에 사용한 숫자를 PDF 텍스트에서 탈락한 근호 없이 추정하지 않는다.',
        EG: '첫 실험의 참여 5명과 정기 참여로 분석한 3명을 구별했다. 상세 경로 그림에 포함된 세 학생의 사례를 전체 참여자 집계로 사용하지 않는다.',
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
        entry = dict(id=sid, year=spec['year'], url=url, title=spec['title'], authors=spec['authors'], kind='지수와 로그의 학생 추론 연구',
            review_scope=spec['scope'], does_not_establish=spec['limit'], supports=spec['supports'],
            next_review='자체 과제의 실제 응답을 확인하고 다른 표본의 지수와 로그 과제를 추가 대조한다.')
        bibliography.append(entry)
        note = f'data/literature_evidence/{sid}_review_notes.json'
        write(ROOT / note, dict(source_id=sid, source_url=url, source_pdf_url=pdf_urls[sid],
            source_asset_kind='pdf', source_pdf_sha256=spec['sha256'], pdf_pages=spec['total'],
            selected_text_pages=spec['pages'], visual_pdf_pages=spec['visuals'], rendered_page_sha256=image_hashes[sid],
            date=DATE, reviewer='Codex', read_scope=spec['scope'], empirical_scope=empirical,
            contains_source_full_text=False, source_pdf_redistributed=False,
            reading_log=[spec['scope']], source_corrections=[dict(location='정의·표·학생 응답', issue=corrections[sid])],
            exponential_review=details[sid]))
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
        ('HA-log-laws', 'WL02-01'): ('activity_context',
            '두 양수를 같은 밑의 거듭제곱으로 나타내고, 곱의 지수가 더해지는 이유에서 로그의 합 공식을 유도한다.',
            '같은 집단에서 두 규칙의 연결 설명이 나오지 않았다는 보고다. 지수법칙 숙달이 로그법칙 이해를 보장하는지 검증하지 않았다.'),
        ('SEC_12대수01-01_C04', 'WT02-01'): ('activity_context',
            '양수의 제곱근 중 양의 값과 1/2제곱을 연결하고, 방정식의 두 해와 구분한다.',
            '양의 밑에서 설명하는 범위다. 음수 밑의 유리 지수나 임의의 실수 거듭제곱으로 확대하지 않는다.'),
        ('REV-12대수01-01-1', 'WT02-01'): ('inference_limit',
            '한 분반에서 제곱근을 거듭제곱으로 나타내는 이유를 설명한 사례가 보고됐다.',
            '분반과 교사가 다른 소규모 시행이다. 근호 과제에서 실수 지수 일반화로 가는 필수 선수성을 확정하지 않는다.'),
        ('SEC_12대수01-04_C04', 'KL02-02'): ('activity_context',
            '입력의 산술평균과 기하평균을 비교해 어느 쪽의 로그가 두 로그의 산술평균인지 그래프와 식으로 확인한다.',
            '면담 중 반례를 본 후의 설명과 최초 판단을 구별한다. 증가 여부만으로 평균의 관계를 판단할 수 없다.'),
        ('REV-12대수01-04-2', 'KL02-02'): ('inference_limit',
            '로그 값을 선형 보간하려 한 사례와 반례 뒤 이를 다시 검토한 사례가 있다.',
            '네 명의 대학 대수 면담이다. 법칙을 설명하는 능력이 곧 그래프를 해석하는 능력인지를 검증하지 않았다.'),
        ('SEC_12대수01-07_C04', 'EG16-01'): ('activity_context',
            '같은 시간 간격마다 높이의 비를 비교하고 처음 높이 또는 다른 시점의 높이에서 예측한 두 값을 검산한다.',
            '식과 그래프의 비교는 가정한 성장 모형의 범위다. 실제 식물 성장의 법칙을 실험으로 확인한 과제가 아니다.'),
        ('REV-12대수01-07-2', 'EG16-01'): ('inference_limit',
            '처음 값에 대한 대응식과 두 시점의 비를 함께 사용한 학생 사례가 보고됐다.',
            '학생별로 나타난 추론과 과제 순서가 일치하지 않아 하나의 순서를 필수 경로로 적용하지 않는다.'),
        ('HA-growth-model', 'EG16-01'): ('activity_context',
            '지수 그래프에서 같은 길이의 입력 구간을 두 개 골라 증가량과 배율을 모두 구한다.',
            '유한한 관측 구간에서 나타난 배율을 관측 밖까지 쓰려면 지수 모형 가정을 따로 명시한다.'),
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
    print('Exponential and logarithmic reasoning: 4 sources, 8 claims, 8 tasks, 8 relation entries')


if __name__ == '__main__':
    main()





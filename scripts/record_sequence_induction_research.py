"""Read scoped sequence and induction evidence without promoting local validity."""
from fractions import Fraction
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_conic_representation_research import probe
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot

DATE = '2026-11-12'
CACHE = ROOT / 'tmp/literature/sequence-and-induction'
HS = 'HILMIY_ET_AL_2026_SEQUENCES'
ND = 'NICCHIOTTI_ET_AL_2024_RECURSION'
BK = 'BAKER_1996_INDUCTION'
AF = 'ALARFAJ_2024_INDUCTION_ASSESSMENT'
SEQ, ARITH, GEO, SIGMA, SUM, REC, IND = [f'12대수03-0{i}' for i in range(1, 8)]
SPECS = {
    HS: dict(year=2026, authors=['Naufal Hilmiy', 'Lilis Marina Angraini', 'Muhammad Sajjad'],
        title='Tracing Conceptual Errors in Grade 11 Students’ Reasoning About Sequences and Series',
        url='https://doi.org/10.56855/algebra.v3i2.2021',
        pdf_url='https://journals.eduped.org/index.php/Algebra/article/download/2021/1472/13202',
        stem='hilmiy-et-al-2026', sha256='f77a2e34d2fc66e3a42736dc6435661fc0ea7c31ac8d7cc762ff164ea9e2d695',
        total=18, pages=[1, 4, 5, 8, 9, 10, 11], visuals=[8, 10],
        scope='표 1의 문항별 분류와 등차수열 일반항에서 합을 구하는 그림 2, 계산 오류의 그림 3 및 곱셈 구조의 문항 5를 대조했다.',
        limit='한 학급의 진단 자료다. 표의 백분율은 문항별 분류이며 전체 학생의 능력 수준이나 수업 효과가 아니다.',
        design='서면 진단 후 응답에 따라 일부 학생을 선정한 질적 면담.',
        sample='인도네시아 페칸바루 공립 고교 11학년 한 학급 33명.',
        supports=['항 생성 규칙과 적합한 합 공식', '개념·절차·계산 오류의 구별']),
    ND: dict(year=2024, authors=['Bianca Nicchiotti', 'Angela Donatiello', 'Giuseppe Bianco'],
        title='A Narrative Approach to Foster the Construction of Recursive Thinking in High School Students',
        url='https://doi.org/10.3390/educsci14040350',
        pdf_url='https://mdpi-res.com/d_attachment/education/education-14-00350/article_deploy/education-14-00350.pdf',
        stem='recursion-2024', sha256='a7d3f2566e54cd8dc050b75fdd714e55b20a712785535055544e350d14e15ac3',
        total=15, pages=[1, 9, 10, 11], visuals=[11],
        scope='두 학급 34명의 모둠 활동 방법과 유한 단계의 넓이를 앞 단계와 비교한 설명, 서로 다른 표현을 조정한 대화를 대조했다.',
        limit='4~5명 모둠의 설명을 개인 성취로 판정하지 않는다. 원문의 무한 과정과 재귀식에서 일반항을 찾는 활동은 자체 대수 과제에서 요구하지 않는다.',
        design='이야기와 동적 기하를 사용한 모둠 산출물·학급 토의·개인 설문 질적 분석.',
        sample='이탈리아 4년제 과학고 11·12학년 두 학급 총 34명.',
        supports=['단계·항의 순서와 앞 항의 관계', '초기 단계와 일정한 비율']),
    BK: dict(year=1996, authors=['John Douglas Baker'],
        title='Students’ Difficulties with Proof by Mathematical Induction',
        url='https://eric.ed.gov/?id=ED396931', pdf_url='https://files.eric.ed.gov/fulltext/ED396931.pdf',
        stem='baker-1996', sha256='7229f27a3c692bf05ea748e5c8219a778f7dfcc368208d6333f6d2bced0b872b',
        total=21, pages=[1, 7, 8, 9, 10, 11, 12], visuals=[10, 11],
        scope='서면 증명 작성·분석과 21명 후속 면담의 방법, 표 1의 기호 해석, 시작 단계 누락 및 일반적 연결에 대한 결과를 확인했다.',
        limit='고교 40명 중 해당 시작 단계 분석 문항 완료자는 39명이다. 대학생 13명과 분모를 합치지 않으며 복수 시작 단계·복잡한 계승 과제를 국내 필수 범위로 추가하지 않는다.',
        design='초기 학습자의 증명 작성·네 증명 분석 과제와 선별 면담.',
        sample='미국 인디애나 고교 심화 대수 40명과 대학 디지털 컴퓨팅 기초 13명, 후속 면담 21명.',
        supports=['Σ 해석과 증명할 명제', '시작 단계와 임의 단계의 연결', '예시 확인과 일반적 증명']),
    AF: dict(year=2024, authors=['Maryam Khalid H Alarfaj'],
        title='Computer aided assessment of mathematical proof by varying the format of students’ answers and the structure of assessment design by STACK',
        url='https://doi.org/10.7488/era/4392',
        pdf_url='https://era.ed.ac.uk/bitstreams/fa809dcf-fdd9-40f9-b29d-a768b1b88315/download',
        stem='alarfaj-2024', sha256='da7658abf61df99224a9d1381d2e6e7320620ab30ad01c2331c8f483a411a56c',
        total=147, pages=[1, 2, 89, 90, 99, 101, 102, 103, 104, 106, 107], visuals=[89, 102],
        scope='학위논문 셋째 연구의 유한 합 차와 P(n+1) 분리 문항, 그림 7.6·7.7의 응답 분류와 표 7.10의 다른 분석 표본을 확인했다.',
        limit='2023년 표지의 에든버러대 학위논문이 2024년에 저장소에 게시됐다. 대학 온라인 응답·시도 수와 동의 표본은 분모가 다르다. 참여 여부의 비교는 인과 효과가 아니다.',
        design='온라인 귀납법 문항의 응답 재분류와 자발적 강의 퀴즈 참여의 관찰적 비교. 여기서는 셋째 연구의 지정 문항만 대조.',
        sample='첫 코호트 수강 470명 중 분석 동의 414명. 그림 7.6·7.7은 별도로 제시한 426개 기록이며 표 7.10은 207개 분석 사례.',
        supports=['유한 합의 마지막 항 분리', '목표 명제와 한쪽 식의 구별', '표본과 채점 분류의 구별']),
}

CLAIMS = [
    (HS, 'HS26-01', [SEQ, GEO], [8, 9],
     '문항 5는 매분 속도가 앞선 속도의 일정 배가 되는 상황에서 첫 여섯 분의 거리를 묻는다. 제시된 사례에서는 곱셈 구조에 맞지 않는 관계를 먼저 선택했다.',
     '식을 고르기 전 각 양의 뜻과 시간 구간을 확인한다. 자기 보고한 흥미·집중을 오류의 직접 원인으로 확정하지 않는다.'),
    (HS, 'HS26-02', [SEQ, ARITH], [8, 10],
     '그림 2의 학생은 일반항에서 첫째·둘째 항을 구했지만, 첫 12항의 합 공식에 대입하는 과정은 끝까지 올바르게 수행하지 못했다.',
     '일반항을 읽은 수행, 공차와 끝 항 결정, 유한 합 계산을 나누어 확인한다. 이 사례를 항 개념 자체의 부재로 단정하지 않는다.'),
    (HS, 'HS26-03', [ARITH], [11],
     '첫째 항 9, 셋째 항 17로 30번째 항을 찾는 문항의 대표 응답은 등차 관계와 절차가 적절해도 수치 계산에서 오류가 날 수 있음을 보였다.',
     '정답 여부만으로 개념 오류를 판정하지 않는다. 해당 문항의 계산 오류 분류 27%를 전체 수열의 오류율로 쓰지 않는다.'),
    (ND, 'ND24-01', [SEQ, GEO, REC], [9, 10, 11],
     '모둠들은 유한 단계 넓이를 앞 단계 넓이의 3/4로 설명하거나 처음 넓이를 사용한 식으로 표현했다. 토의에서 두 표현이 같은 단계의 넓이를 가리킴을 조정했다.',
     '모둠의 조정과 개인의 독립 수행을 구별한다. 초기값을 주어 앞 항에서 다음 항을 생성하는 자체 과제로 한정하며 재귀식의 일반항 구하기는 요구하지 않는다.'),
    (BK, 'BK96-01', [SIGMA, IND], [7, 8, 10],
     '표 1에는 합 기호를 해석하지 못해 증명할 식을 잘못 나타내고, 그 결과 증명 작성을 진행하지 못한 사례가 기록돼 있다.',
     '기호 해석과 귀납법 원리의 판단을 구분한다. Σ 학습을 마치면 귀납 증명이 보장된다는 결과가 아니다.'),
    (BK, 'BK96-02', [IND], [11],
     '시작 단계가 빠진 증명 분석 문항을 완료한 고교생 39명 중 30명이 누락을 인식하지 못했다. 연구의 고교 모집 인원은 40명이었다.',
     '이 문항의 완료자 분모를 유지한다. 시작 단계 확인과 임의 단계의 연결을 각각 요구하며 대학생 결과와 합산하지 않는다.'),
    (BK, 'BK96-03', [IND], [8, 11, 12],
     '연구는 몇몇 특정 수의 확인을 일반적 귀납 단계 대신 제시한 논증을 분석하게 했고, 일반적으로 성립하는 연결의 필요성을 놓친 응답을 보고했다.',
     '예시로 명제를 탐색하는 활동과 모든 자연수에 대한 증명을 구분한다. 원문의 복잡한 증명 과제를 그대로 필수 과제로 옮기지 않는다.'),
    (AF, 'AF24-01', [SIGMA, SUM, IND], [89, 90],
     '저자는 홀수 제곱의 유한 합 문항을 P(n+1) 쓰기, 연속한 두 부분합의 차, 우변 두 식의 차로 나누어 설계했다.',
     '저자의 문항 설계 예이지 각 단계의 교수 효과를 입증한 결과가 아니다. 목표 명제를 쓰는 일과 그 명제를 이미 참으로 가정하는 일을 구별한다.'),
    (AF, 'AF24-02', [IND], [99, 101, 102, 107],
     '그림 7.6·7.7의 426개 기록에서 등식을 입력한 것은 258개, 완전 정답은 203개다. 한쪽 식만 쓴 응답과 목표 명제를 등식으로 쓴 응답을 별도로 분류했다.',
     '102쪽 요약은 258개를 정답으로 표현하지만 그림의 분류와 같지 않다. 표 7.10의 207개 사례와 다른 분모이며, 여기의 등식 과제를 모든 귀납 명제의 형식으로 일반화하지 않는다.'),
]
OBSERVATIONS = {
    HS: [
        probe('HS-P1', SEQ, '처음 세 항이 3,5,7인 수열의 네 번째 항은 반드시 9인가? n=1부터인 a_n=2n+1과 b_n=2n+1+(n−1)(n−2)(n−3)을 비교하라.',
              '두 식은 처음 세 항이 모두 3,5,7이다. 네 번째 항은 a_4=9, b_4=15다. 일반항 등의 추가 규칙 없이 유한한 앞 항만으로 뒤 항이 유일하게 정해지지 않는다.',
              '항의 차례와 생성 규칙을 확인한다. 두 식은 반례를 주며 특정 규칙을 가장 자연스럽다고 고르는 판단과 구별한다.'),
        probe('HS-P2', ARITH, '첫째 항 9, 셋째 항 17인 등차수열의 공차와 30번째 항, 첫 30항의 합을 구하고 변화 횟수를 설명하라.',
              '두 번의 변화로 8이 늘어 공차는 4다. 30번째 항은 9+29·4=125, 합은 30(9+125)/2=2010이다.',
              '공차 결정, n−1번 증가, 항과 합, 수치 계산을 따로 기록한다.'),
        probe('HS-P3', GEO, 'a_1=2, 공비 q인 등비수열의 첫 4항과 합을 q=−1,1,0 각각에서 구하라. q=0일 때 a_2/a_1과 a_3/a_2를 비교하라.',
              'q=−1이면 2,−2,2,−2로 합 0, q=1이면 2,2,2,2로 합 8, q=0이면 2,0,0,0으로 합 2다. q=1은 분모 1−q인 합 공식을 바로 쓰지 않는다. q=0에서 0/2=0이나 0/0은 정의되지 않으므로 곱셈 관계로 항을 생성한다.',
              '자체 확장 과제다. 이 특수 공비들을 원연구에서 학생에게 검사한 것으로 표시하지 않는다.'),
    ],
    ND: [probe('ND-P1', REC, '수열 a_1=16, a_(n+1)=(3/4)a_n의 첫 4항을 구하라. 같은 관계에 b_1=8을 주면 무엇이 달라지는가?',
               'a는 16,12,9,27/4이고 b는 8,6,9/2,27/8이다. 같은 다음 항 생성 관계여도 초기값이 다르면 항이 달라진다.',
               '초기값과 항 생성 범위를 확인한다. 재귀적으로 정의한 수열의 일반항을 구하도록 요구하지 않는다.')],
    BK: [
        probe('BK-P1', IND, 'P(n)을 1+3+⋯+(2n−1)=n²이라 하자. n=1,2,3의 확인만으로 증명이 되는가? 임의의 k에서 가정을 쓰는 위치와 다음 단계를 완성하라.',
              '유한 대입만으로는 증명이 아니다. P(1)은 1=1이다. 임의 k≥1에서 합이 k²라 가정하고 다음 항 2k+1을 더하면 k²+2k+1=(k+1)²다. 앞부분 합을 k²로 바꾸는 곳에서 가정을 쓴다.',
              '시작 단계, 임의 k의 조건, 가정의 실제 사용과 다음 목표를 구분한다.'),
        probe('BK-P2', IND, 'P(n)을 n+1=n이라 하자. P(k)를 가정하고 양변에 1을 더하면 P(k+1)을 얻는다. 이것으로 모든 n≥1에 대한 증명이 되는가?',
              '연결의 조건문만으로는 부족하다. 시작 단계 P(1)은 2=1로 거짓이다. 따라서 귀납 증명이 성립하지 않는다.',
              '명제의 거짓을 지적한 뒤 논증에서 시작 단계가 빠졌음을 명시하게 한다. 거짓 가정을 실제 참이라고 받아들이지 않는다.'),
    ],
    AF: [
        probe('AF-P1', SIGMA, 'n≥1에서 Σ(k=1..n+1)(2k−1)²−Σ(j=1..n)(2j−1)²를 간단히 하고, 두 합의 항수와 문자 k,j의 역할을 설명하라.',
              '각각 n+1개와 n개 항이다. k,j는 합 안의 더미 첨자여서 같은 범위의 항은 상쇄된다. 남는 것은 (2n+1)²이고 제곱합 (n+1)²−n²가 아니다.',
              '위 첨자와 피합수의 구분, 더미 문자 변경, 마지막 항 분리를 확인한다.'),
        probe('AF-P2', SUM, 'Σk=n(n+1)/2, Σk²=n(n+1)(2n+1)/6을 써서 Σ(k=1..n)(2k−1)²를 구하라. n+1일 때의 목표도 등식 전체로 적어라.',
              '4Σk²−4Σk+Σ1=n(2n−1)(2n+1)/3이다. 다음 목표는 Σ(k=1..n+1)(2k−1)²=(n+1)(2n+1)(2n+3)/3이다. 목표를 적는 것 자체는 그 참을 증명한 것이 아니다.',
              '합의 선형성, 상수항 n개, 부분합의 값과 증명할 명제를 구분한다.'),
    ],
}

def main():
    registry = load_registry()
    if set(SPECS) <= registry['sources'].keys():
        build_report()
        return
    assert not set(SPECS).intersection(registry['sources'])
    details = {
        HS: dict(n=33, items=5, item_1_procedural_percent=52, item_2_operational_percent=27,
                 frequencies_are_item_specific=True, figure_2_general_term='5n−3'),
        ND: dict(n=34, group_sizes=[4, 5], grades=[11, 12], no_individual_outcome_inferred=True,
                 finite_stages_only=True, general_term_from_recurrence_required=False),
        BK: dict(high_school_n=40, university_n=13, interview_n=21,
                 missing_base_item_high_school_completed_n=39, missing_base_not_recognized_n=30),
        AF: dict(cover_year=2023, repository_date='2024-03-26', thesis_institution='University of Edinburgh',
                 third_study_only=True, figure_7_6_records=426, equation_entered=258, fully_correct=203,
                 lhs_only=49, rhs_only=46, no_equation=137, blank=31, table_7_10_n=207,
                 course_n=470, consenting_n=414, denominators_not_combined=True,
                 design_example_claim='AF24-01', assuming_target_is_not_a_valid_forward_induction_step=True),
    }
    corrections = {
        HS: '10쪽 그림 2의 일반항은 5n−3이다. 앞서 준비 메모의 두 항을 주었다는 추정은 사용하지 않는다. 표 1 백분율을 정확한 정수 빈도로 역산하지 않았다.',
        ND: '모둠 답과 개인 익명 설문을 구별한다. 이 대조는 유한 단계와 항 생성 관계에 한정하며 무한 넓이·둘레 결론을 추가하지 않는다.',
        BK: '시작 단계 누락 결과의 분모는 고교 모집 40명이 아니라 문항 완료 39명이다. 원문의 about half라는 대학생 기술을 임의 정수로 만들지 않는다.',
        AF: '그림 7.6의 완전 정답 203/426과 그림 7.7의 등식 입력 258/426을 구별한다. 99쪽의 425 표기와 102쪽의 258 정답 요약을 분모나 정답 수로 채택하지 않는다. 103쪽 문항의 계승 합은 원문 스스로 상수 −1 누락을 밝힌다. 89~90쪽에서 목표 명제를 참으로 놓는 설계 설명은 순방향 귀납 증명의 정당화로 옮기지 않는다.',
    }
    bibliography, queue = load(ROOT / 'data/sources.json'), load(ROOT / 'data/content_review_queue.json')
    assert not set(SPECS).intersection(row['id'] for row in bibliography)
    for sid, spec in SPECS.items():
        pdf = CACHE / f'{spec["stem"]}.pdf'
        assert sha(pdf) == spec['sha256']
        reader = PdfReader(pdf)
        assert len(reader.pages) == spec['total']
        assert all(reader.pages[p-1].extract_text().strip() for p in spec['pages'])
        images = {str(p): sha(CACHE / 'rendered' / f'{spec["stem"]}-{p}.png') for p in spec['visuals']}
        empirical = dict(design=spec['design'], sample_description=spec['sample'], inference_limit=spec['limit'],
                         student_outcome_study=True, causal_effect_established=False, local_effect_tested=False)
        entry = dict(id=sid, year=spec['year'], url=spec['url'], title=spec['title'], authors=spec['authors'],
                     kind='수열·유한 합·수학적 귀납법의 과제와 학생 추론 연구', review_scope=spec['scope'],
                     does_not_establish=spec['limit'], supports=spec['supports'],
                     next_review='자체 과제의 실제 학생 응답과 다른 표본의 문항을 대조한다.')
        bibliography.append(entry)
        note = f'data/literature_evidence/{sid}_review_notes.json'
        write(ROOT / note, dict(source_id=sid, source_url=spec['url'], source_pdf_url=spec['pdf_url'],
            source_asset_kind='pdf', source_pdf_sha256=spec['sha256'], pdf_pages=spec['total'],
            selected_text_pages=spec['pages'], visual_pdf_pages=spec['visuals'], rendered_page_sha256=images,
            date=DATE, reviewer='Codex', read_scope=spec['scope'], empirical_scope=empirical,
            contains_source_full_text=False, source_pdf_redistributed=False, reading_log=[spec['scope']],
            source_corrections=[dict(location='방법·문항·표·요약의 대조', issue=corrections[sid])],
            sequence_induction_review=details[sid]))
        registry['sources'][sid] = dict(source_id=sid, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
            snapshot_kind='authored_review_notes', source_asset_kind='pdf', source_pdf_sha256=spec['sha256'],
            snapshot_file=note, snapshot_sha256=sha(ROOT / note), redistribution_license='workspace_authored_notes',
            bibliography_snapshot=digest(entry), display=dict(title=spec['title'], url=spec['url'],
                authors_year=f'{spec["authors"][0]}{" 외" if len(spec["authors"]) > 1 else ""}, {spec["year"]}'),
            read_scope=spec['scope'], limits=spec['limit'], empirical_scope=empirical,
            scope_note='문항 설계·최초 응답·수정 응답과 자체 설계 과제를 구별한다.',
            method_note='지정 본문과 표·그림의 실제 판면을 대조했다. 대학 문항·모둠 관찰은 국내 고교 개인 성취로 환산하지 않는다.',
            editorial_action='문헌 근거와 유한 합·초기값·귀납 증명의 자체 관찰 과제를 보완했다.',
            independent_review=False, student_validated=False, observations=OBSERVATIONS[sid])
        queue['literature_review'].append(dict(source=entry, status='self_read_claim_mapping',
            evidence_file='data/literature_claim_reviews.json', claim_evidence_fields=spec['supports'],
            claim_ids=[cid for src, cid, *_ in CLAIMS if src == sid]))
    new = {}
    for sid, cid, codes, pages, support, limit in CLAIMS:
        new[cid] = dict(id=cid, source_id=sid,
            role='mathematical_explanation' if cid == 'AF24-01' else 'empirical_result_with_scope',
            empirical_scope=registry['sources'][sid]['empirical_scope'], standard_codes=codes,
            locations=[f'{SPECS[sid]["pdf_url"]}#page={p}' for p in pages], support=support, does_not_establish=limit,
            independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes})
    registry['claims'].extend(new.values())
    relations = load(ROOT / 'data/revised_relations.json')['relations']
    pairs = {(r['id'], cid) for r in relations for cid, claim in new.items()
             if all(r[k].startswith('standard:') for k in ('from','to'))
             and {r[k][9:] for k in ('from','to')} <= set(claim['standard_codes'])}
    interpretations = { (rid,'ND24-01'): ('activity_context',
        '초기 단계의 넓이와 앞 단계의 3/4라는 관계를 주고 다음 몇 단계의 값을 차례대로 생성해 항의 순서와 관계를 설명한다.',
        '모둠 토의의 사례다. 같은 규칙에서 초기값을 바꾼 자체 과제와 구별하고 재귀식의 일반항 구하기를 요구하지 않는다.')
        for rid in ['SEC_12대수03-01_C03', 'REV-12대수03-01-1'] }
    assert pairs == interpretations.keys(), pairs
    reviewed = load(ROOT / FILE)
    by_relation = {r['id']:r for r in relations}
    for (rid,cid),(role,finding,limit) in interpretations.items():
        claim = new[cid]
        reviewed['records'].append(dict(relation_id=rid,claim_id=cid,role=role,finding=finding,limit=limit,
            relation_snapshot=relation_snapshot(by_relation[rid]),
            claim_snapshot=claim_snapshot(claim,registry['sources'][claim['source_id']])))
    apply_literature_context(relations, registry, registry=reviewed)
    # Finite witnesses supplement the algebraic explanations; they are not universal proofs.
    assert 30*(9+125)//2 == 2010
    assert sum(9+4*k for k in range(30)) == 2010
    assert [16*Fraction(3,4)**k for k in range(4)] == [16,12,9,Fraction(27,4)]
    assert 258+137+31 == 426 and 203 < 258
    for n in [1,2,7,30]:
        assert sum((2*k-1)**2 for k in range(1,n+1)) == n*(2*n-1)*(2*n+1)//3
    for file, value in [('sources.json',bibliography),('content_review_queue.json',queue),
                        ('literature_claim_reviews.json',registry),(FILE.removeprefix('data/'),reviewed)]:
        write(ROOT / 'data' / file, value)
    build_report()
    print('Sequences and induction: 4 sources, 9 claims, 8 tasks, 2 relation entries')

if __name__ == '__main__':
    main()

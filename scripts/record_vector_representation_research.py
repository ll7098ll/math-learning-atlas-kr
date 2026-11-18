"""Map vector representation research to scoped claims and original probes."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from extend_making_pre_k_count_appendices_review import DATE
from literature_review import ROOT, build_report, digest, load_registry, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


CACHE = ROOT / 'tmp/literature/vector-representations'
TUV = 'BARNIOL_ZAVALA_2014_TUV'
CONTEXT = 'BARNIOL_ZAVALA_2014_VECTOR_CONTEXT'
RASCH = 'SUSAC_ET_AL_2018_VECTOR_RASCH'
OPS, COORD, DOT, DATA, TEST = '12기하03-01', '12기하03-02', '12기하03-03', '12실통02-02', '12실통03-04'
AUTHORS = ['Pablo Barniol', 'Genaro Zavala']
SPECS = {
    TUV: dict(year=2014, authors=AUTHORS, doi='10.1103/PhysRevSTPER.10.010121',
        title='Test of understanding of vectors: A reliable multiple-choice vector concept test',
        stem='barniol-zavala-2014-tuv', sha256='5d93625545e4f5b83de3f0c1c362ee8621a4b5ad48c821d91ac57a4ee750df08',
        total=14, pages=[1, 2, 3, 5, 7, 8, 9, 10, 12], visuals=[5],
        scope='검사 개발의 서술형 응답과 20문항 시행을 구별하고, 표 IV의 벡터 연산·성분·내적 응답을 확인했다.',
        limit='멕시코 대학 입문 물리 수강생의 문항별 응답이다. 국내 고등학생의 오류 빈도와 학습 순서는 별도 검증이 필요하다.',
        design='서술형 오류 자료를 이용한 객관식 검사 개발과 문항별 응답 분석.',
        sample='서술형 개발 시행 참여 2,067명과 객관식 분석 423명.',
        supports=['벡터 그림 연산', '성분과 좌표 표현', '내적 해석과 계산']),
    CONTEXT: dict(year=2014, authors=AUTHORS, doi='10.1103/PhysRevSTPER.10.020115',
        title='Force, velocity, and work: The effects of different contexts on students’ understanding of vector concepts using isomorphic problems',
        stem='barniol-zavala-2014-context', sha256='11da2a2e2a716faa9975dec2fd800bb44e86cbf6554d83ac628a1f0b64d08d05',
        total=15, pages=[2, 3, 4, 5, 6, 8, 9, 10, 11, 12], visuals=[3, 4, 5, 11],
        scope='두 맥락의 12문항 검사와 별도 설명 응답, 표 III·IV·XV 및 본문 표기를 대조했다.',
        limit='일반 수학과 역학의 선택 반응 비교다. 수업 효과나 국내 고등학생의 전략을 검증한 자료로 쓰지 않는다.',
        design='역학 맥락과 비맥락 검사를 비교하고 일부 문항의 설명을 별도 시행에서 수집.',
        sample='최초 선택 응답 608명, 일부 문항에 설명을 쓴 별도 시행 203명.',
        supports=['표현 맥락과 정답률', '오답 선택과 풀이 설명', '총점과 문항별 검정']),
    RASCH: dict(year=2018, authors=['Ana Sušac', 'Maja Planinić', 'Damjan Klemencic', 'Željka Milin Šipuš'],
        doi='10.1103/PhysRevPhysEducRes.14.023101', title='Using the Rasch model to analyze the test of understanding of vectors',
        stem='susac-et-al-2018-rasch', sha256='4b65c4ca8d04eea09f49f498535220d54ffa5b6746c2e908aaf6506bfe302e36',
        total=6, pages=[1, 2, 3, 4, 5], visuals=[2, 3],
        scope='동일 TUV의 자그레브 대학 시행에서 문항과 개인의 신뢰도 및 난이도 분포를 확인했다.',
        limit='특정 대학 표본에서의 검사 적합성이다. 국내 학생 자료와 자체 과제의 진단 적합성은 따로 확인한다.',
        design='기존 벡터 이해 검사에 대한 라시 모형 분석.', sample='자그레브 대학 1학년 889명.',
        supports=['문항·개인 신뢰도', '표본 능력과 문항 난이도의 대응']),
}

CLAIMS = [
    (TUV, 'VEC14-01', [OPS], [5, 7, 8],
     '423명 TUV 시행에서 2차원 그림 덧셈 정답은 74%, 그림 뺄셈은 56%, 음의 실수배는 71%였다.',
     '정답률은 제시한 그림과 문항에 귀속한다. 동일한 성취 순서나 모든 학생에게 공통인 오류로 옮기지 않는다.'),
    (TUV, 'VEC14-02', [COORD], [5, 6],
     '같은 TUV 표에서 단위벡터 기호로 주어진 벡터의 그림 선택은 92%, 각을 y축과 이루는 각으로 준 x성분 계산은 73%였다.',
     '성분을 옮기는 수행, 각의 기준축 해석, 위치벡터에서 원점을 정하는 수행을 따로 살핀다.'),
    (TUV, 'VEC14-03', [OPS, DOT], [5, 8, 9],
     '벡터 그림 덧셈과 내적은 같은 검사에서 별도 문항이었다. 내적 정사영 해석은 33%, 두 벡터 크기와 끼인각을 쓰는 문항은 78%, 단위벡터 기호로 제시한 성분 계산은 42%였다.',
     '덧셈에서 벡터를 만드는 수행과 내적의 스칼라 산출을 구별한다. 문항별 집계로 특정 학생의 수행이나 필수 선수성을 추론하지 않는다.'),
    (CONTEXT, 'VECC-01', [DOT], [3, 4, 5, 6, 11],
     '비맥락·역학 검사의 정답률은 내적의 기하적 해석에서 27%·52%, 각을 이용한 계산에서 60%·81%, 성분 계산에서 30%·30%였다.',
     '일의 맥락에서 정답을 골랐다는 사실로 내적의 일반 조건이나 성분 계산까지 설명할 수 있다고 판단하지 않는다. 표 XV와 본문의 벡터 표기는 따로 보존한다.'),
    (CONTEXT, 'VECC-02', [OPS], [4, 8, 9, 10],
     '그림 덧셈, 음의 실수배, 1차원 뺄셈에서는 두 맥락 사이에 정답 선택의 유의한 차이가 보고되지 않았으나 일부 오답 선택은 달랐다.',
     '정답률, 오답의 형태, 학생이 쓴 이유를 구별한다. 한 과제에서의 오답 선택만으로 다른 표현의 이해를 판정하지 않는다.'),
    (CONTEXT, 'VECC-03', [DATA, TEST], [3, 4, 5, 11],
     '두 12문항 검사의 첫 시행은 608명이고 두 총점 중앙값은 각각 7, 비교 p는 .578이다. 일부 문항의 풀이 근거는 별도 시행 203명에게 받았다.',
     '총점 검정과 문항별 선택 분포 검정, 별도 시행의 설명을 분리한다. 귀무가설을 기각하지 않은 결과로 두 검사가 동등하다고 판정하지 않는다.'),
    (RASCH, 'VECR-01', [DATA], [1, 2],
     '자그레브 대학 1학년 889명의 TUV에서 문항 신뢰도는 .99, 개인 신뢰도는 .60으로 보고됐다. 20문항 정답자는 102명, 19문항 정답자는 118명이었다.',
     '문항 난이도 순위의 안정성과 개인을 구별하는 정도는 다른 지표다. 높은 점수 집중을 다른 집단의 특성으로 옮기지 않는다.'),
    (RASCH, 'VECR-02', [COORD, DOT, DATA], [2, 3, 4],
     '문항 난이도 평균보다 학생 능력 평균이 약 2로짓 높았다. y축 기준 각에서 x성분을 구하는 문항의 오답자 중 70%는 사인 대신 코사인을 쓴 보기를 골랐다. 내적 문항도 요구한 해석과 계산 방식이 달랐다.',
     '문항 난이도와 학생 수준을 함께 확인한다. 70%의 분모는 해당 문항의 오답자이며, 선택 반응만으로 오류 원인을 확정하지 않는다.'),
]
OBSERVATIONS = {
    TUV: [
        dict(id='VEC-P1', standard_codes=[OPS], question='a=(2,1), b=(1,−2)를 같은 시작점에서 그려 a−b와 −2a를 나타내고, 화살표의 방향과 길이가 어떻게 정해지는지 설명하라.',
             expected='a−b=(1,3)이고 같은 시작점에서 b의 끝에서 a의 끝으로 향한다. −2a=(−4,−2)는 a와 반대 방향이며 길이는 두 배다.',
             interpretation='뺄셈의 화살표 방향과 음의 실수배의 방향·크기를 따로 기록한다.', student_validated=False),
        dict(id='VEC-P2', standard_codes=[COORD], question='P=(1,2)에서 Q=(5,−1)로 향하는 벡터를 원점으로 옮겨 Q의 위치벡터와 비교하라. 또 제1사분면에서 길이 10이고 양의 y축과 30°를 이루는 벡터의 x성분을 구하라.',
             expected='PQ는 성분 (4,−3)이고 Q의 위치벡터는 (5,−1)이다. 두 번째 벡터의 x성분은 y축 기준 각의 맞은편 길이인 10sin30°=5다.',
             interpretation='끝점 좌표와 성분 차를 구별하고, 각을 어느 축에서 재었는지 확인한다.', student_validated=False),
        dict(id='VEC-P3', standard_codes=[DOT], question='a=(2,1), b=(4,0)에서 a·b, b 방향의 부호 있는 성분, b 방향의 정사영 벡터를 각각 구하라. b가 영벡터일 때도 세 대상을 같은 방법으로 설명할 수 있는가?',
             expected='내적은 8, 부호 있는 성분은 2, 정사영 벡터는 (2,0)이다. b가 영벡터면 내적은 0이지만 b가 정하는 단위 방향은 없다.',
             interpretation='스칼라 값 두 가지와 정사영 벡터를 구별하고 영벡터에서 방향 조건을 확인한다.', student_validated=False),
    ],
    CONTEXT: [
        dict(id='VECC-P1', standard_codes=[DOT], question='벡터 (3,−2)와 (−2,0)의 내적을 구하라. 같은 성분을 힘과 변위로 제시하면 일의 부호와 단위는 어떻게 되는가?',
             expected='내적은 −6이다. 성분이 뉴턴과 미터라면 일은 −6 J다. 변위 방향의 부호 있는 힘 성분은 −3 N이고 변위 길이 2 m를 곱한다.',
             interpretation='기호 문제와 일의 맥락에서 부호와 스칼라 산출의 근거를 각각 적는다.', student_validated=False),
        dict(id='VECC-P2', standard_codes=[DATA, TEST], question='가상 검사에서 두 집단의 총점 비교 p=.58이며 한 문항의 선택 분포 비교 p=.008이다. 유의수준 5%에서 두 비교를 각각 해석하라.',
             expected='총점 비교의 귀무가설은 기각하지 않고, 해당 문항의 선택 분포 귀무가설은 기각한다. 여러 문항을 함께 검정했다면 전체 오류율 처리도 확인한다.',
             interpretation='총점과 문항별 질문을 구별하고 비유의를 동등성으로 해석하지 않는지 확인한다.', student_validated=False),
    ],
    RASCH: [dict(id='VECR-P1', standard_codes=[DATA], question='가상 검사에서 120명 중 24명이 만점, 18명이 한 문항만 틀렸다. 두 부류의 비율을 구하고 만점 집단 안의 수행 차이를 알려면 어떤 자료가 필요한지 설명하라.',
        expected='합계는 42명이고 42/120=35%다. 만점 기록만으로 만점 학생 간 차이를 구분할 수 없으므로 더 어려운 문항이나 별도의 수행 자료를 확인한다.',
        interpretation='최고점 부근의 집중과 개인의 실제 수행을 구별한다.', student_validated=False)],
}


def verify_pdf(spec):
    file = CACHE / f'{spec["stem"]}.pdf'
    assert sha(file) == spec['sha256']
    reader = PdfReader(file)
    assert len(reader.pages) == spec['total']
    assert all(reader.pages[p - 1].extract_text().strip() for p in spec['pages'])
    return {str(p): sha(CACHE / 'rendered' / f'{spec["stem"]}-{p}.png') for p in spec['visuals']}


def main():
    registry = load_registry()
    if set(SPECS) <= registry['sources'].keys():
        build_report()
        return
    assert not set(SPECS).intersection(registry['sources'])
    image_hashes = {sid: verify_pdf(spec) for sid, spec in SPECS.items()}
    details = {
        TUV: dict(open_response_participants=2067, multiple_choice_n=423, items=20,
            table_iv_correct_percent={1:74, 3:33, 6:78, 8:42, 10:92, 11:71, 13:56, 14:73}),
        CONTEXT: dict(first_groups=[304,304], reasoning_groups=[103,100], items=12, total_medians=[7,7], total_p=.578,
            table_iii_correct_percent={2:[27,52], 4:[60,81], 6:[30,30]}, item_distribution_alpha=.05, choice_alpha=.01,
            supplement_verified=False, table_xv_dot=5, body_printed_context_vectors=[[5,3],[5,0]]),
        RASCH: dict(n=889, item_reliability=.99, person_reliability=.60, all_correct=102, nineteen_correct=118,
            person_mean_above_item_mean_logits_approx=2, item_14_cosine_choice_percent_among_incorrect=70),
    }
    assert 304 + 304 == 608 and 103 + 100 == 203 and 102 + 118 == 220
    assert 1 * 5 == details[CONTEXT]['table_xv_dot'] and 5 * 5 != details[CONTEXT]['table_xv_dot']
    corrections = {
        TUV: '검사 개발 참여자와 표 IV의 객관식 표본, 문항별 집계와 실제 풀이 설명을 나눈다.',
        CONTEXT: 'PDF 5쪽의 각 공식 문항 번호 11과 표 II·III의 4번을 따로 보존했다. PDF 11쪽 본문의 힘 (5,3)과 표 XV의 (1,3)은 서로 다르다. 보충자료를 확보하지 못해 맥락 문항의 성분을 확정하지 않았다.',
        RASCH: '문항 신뢰도와 개인 신뢰도 및 최고점 집중을 다른 근거로 기록했다.',
    }
    bibliography, queue = load(ROOT / 'data/sources.json'), load(ROOT / 'data/content_review_queue.json')
    assert not set(SPECS).intersection(row['id'] for row in bibliography)
    assert not set(SPECS).intersection(row['source']['id'] for row in queue['literature_review'])
    pdf_urls = {}
    for sid, spec in SPECS.items():
        doi = f'https://doi.org/{spec["doi"]}'
        pdf_urls[sid] = f'https://harvest.aps.org/v2/journals/articles/{spec["doi"]}/fulltext'
        empirical = dict(design=spec['design'], sample_description=spec['sample'], inference_limit=spec['limit'],
            student_outcome_study=True, causal_effect_established=False, local_effect_tested=False)
        entry = dict(id=sid, year=spec['year'], url=doi, title=spec['title'], authors=spec['authors'], kind='벡터 표현의 학생 응답 연구',
            review_scope=spec['scope'], does_not_establish=spec['limit'], supports=spec['supports'],
            next_review='검사 원형과 보충자료의 문항을 추가 대조하고 자체 과제의 실제 응답을 확인한다.')
        bibliography.append(entry)
        note = f'data/literature_evidence/{sid}_review_notes.json'
        write(ROOT / note, dict(source_id=sid, source_url=doi, source_pdf_url=pdf_urls[sid],
            source_asset_kind='pdf', source_pdf_sha256=spec['sha256'], pdf_pages=spec['total'],
            selected_text_pages=spec['pages'], visual_pdf_pages=spec['visuals'], rendered_page_sha256=image_hashes[sid],
            date=DATE, reviewer='Codex', read_scope=spec['scope'], empirical_scope=empirical,
            contains_source_full_text=False, source_pdf_redistributed=False,
            reading_log=[spec['scope']], source_corrections=[dict(location='표와 시행 설명', issue=corrections[sid])],
            vector_review=details[sid]))
        registry['sources'][sid] = dict(source_id=sid, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
            snapshot_kind='authored_review_notes', source_asset_kind='pdf', source_pdf_sha256=spec['sha256'],
            snapshot_file=note, snapshot_sha256=sha(ROOT / note), redistribution_license='workspace_authored_notes',
            bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=doi, authors_year=f'{spec["authors"][0].split()[-1]} 외, {spec["year"]}'),
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
        'SEC_12기하03-01_C04': ('activity_context', '화살표의 방향·길이를 설명한 뒤 내적의 부호·값을 따로 설명하게 한다.',
                               '그림 연산과 내적 문항의 정답률 차이는 필수 선수성의 증거가 아니다.'),
        'REV-12기하03-01-1': ('inference_limit', '그림 덧셈과 내적 해석·계산은 검사에서 다른 문항으로 다뤄졌다.',
                             '집계된 정답률로 같은 학생의 숙달 순서나 영벡터의 방향각 이해를 판단할 수 없다.'),
    }
    assert pairs == {(rid, 'VEC14-03') for rid in interpretations}
    reviewed = load(ROOT / FILE)
    for rid, (role, finding, limit) in interpretations.items():
        relation = next(r for r in relations if r['id'] == rid)
        reviewed['records'].append(dict(relation_id=rid, claim_id='VEC14-03', role=role, finding=finding, limit=limit,
            relation_snapshot=relation_snapshot(relation), claim_snapshot=claim_snapshot(new['VEC14-03'], registry['sources'][TUV])))
    apply_literature_context(relations, registry, registry=reviewed)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviewed)
    build_report()
    print('Vector representations: 3 sources, 8 claims, 6 tasks, 2 relation entries')


if __name__ == '__main__':
    main()

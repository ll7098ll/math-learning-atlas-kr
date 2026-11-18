"""Map spatial coordinates, sphere equations, and vector equations to scoped evidence."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from extend_making_pre_k_count_appendices_review import DATE
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_conic_representation_research import probe
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


CACHE = ROOT / 'tmp/literature/spatial-geometry'
SM = 'SILITONGA_ET_AL_2023_SPATIAL_COORDINATES'
DG = 'DORUK_BAYRAM_GUN_2026_SURFACE_REPRESENTATIONS'
TL = 'TURGUT_ET_AL_2022_VECTOR_EQUATIONS'
COORD, SPH, LINE, PLANE = '12기하02-04', '12기하02-05', '12기하03-04', '12기하03-05'
SPECS = {
    SM: dict(year=2023, authors=['R. H. Yanti Silitonga', 'Juliana Selvina Molle', 'Darma Andreas Ngilawajan'],
        title='Increasing Mathematical Problem-Solving Abilities Using Video Tutorials of the Three-Dimensional Coordinate System in Spatial Analytic Geometry',
        url='https://doi.org/10.19166/johme.v7i2.7575',
        pdf_url='https://ojs.uph.edu/index.php/JOHME/article/download/7575/pdf/24601',
        stem='silitonga-et-al-2023', sha256='4956c8d28a5cb861f25ebf105230db90d556ba3284793c85439dc9f588780292',
        total=15, pages=[1, 5, 6, 7, 8, 9, 10, 11, 12], visuals=[5, 8, 11],
        scope='공간좌표 강좌 성과, 두 반의 준실험 배치, 표 1·2·6·7과 본문 수치의 보고 범위를 대조했다.',
        limit='두 대학 수업 반의 문제 해결 총점 보고다. 개별 좌표·거리·내분 문항 성취나 국내 고교 수업 효과를 입증하지 않는다.',
        design='영상 활용 반과 기존 수업 반의 사전·사후 검사를 비교한 준실험.',
        sample='인도네시아 대학에서 영상 활용 반 19명, 기존 수업 반 17명.',
        supports=['공간좌표·거리·분점의 학습 성과 목록', '총점과 문항별 근거 및 표의 수치 비교']),
    DG: dict(year=2026, authors=['Muhammet Doruk', 'Gül Mine Bayram Gün'],
        title='Pre-Service Mathematics Teachers’ Transformation Skills: A Focus on Algebraic and Graphical Representations',
        url='https://doi.org/10.3390/higheredu5010027',
        pdf_url='https://mdpi-res.com/d_attachment/higheredu/higheredu-05-00027/article_deploy/higheredu-05-00027.pdf',
        stem='doruk-gun-2026', sha256='cc1ceb660cbf667e4a17ef667d5851455a9bffce7ca565f9dad6e19adf30268b',
        total=26, pages=[1, 6, 7, 9, 10, 11, 12, 13], visuals=[11, 12],
        scope='그림 3의 구 식 선택과 미응답, 그림 4·5의 축 절편 확인과 비슷한 곡면의 혼동을 대조했다.',
        limit='예비 교사가 원점 중심 구를 고른 응답이다. 이동된 구의 중심·반지름 설명과 벡터식, 평면의 식은 따로 확인한다.',
        design='식과 그래프의 대응 과제를 사용한 질적 사례 연구.',
        sample='튀르키예 국립대 두 곳의 초등 수학교육 전공 2학년 예비 교사 85명.',
        supports=['구의 그림과 표준식 대응', '식 선택과 절편·중심에 관한 설명']),
    TL: dict(year=2022, authors=['Melih Turgut', 'Jessica Lynn Smith', 'Christine Andrews-Larson'],
        title='Symbolizing lines and planes as linear combinations in a dynamic geometry environment',
        url='https://doi.org/10.1016/j.jmathb.2022.100948',
        pdf_url='https://hdl.handle.net/11250/2988285',
        stem='turgut-et-al-2022', sha256='21cec1574fd59667fad594c44fb19414ed696031e8ef829592796d2105110b39',
        total=20, pages=[1, 7, 8, 9, 13, 14, 15, 16, 17, 18], visuals=[8, 15, 16, 17],
        scope='대학 저장소의 출판본에서 동적 기하 도구 활용, 직선·평면 과제, 연구자 질문 전후의 표현을 대조했다.',
        limit='대학 선형대수 소표본 면담이다. 유한한 도구 화면에서 얻은 점, 모든 실수 매개변수의 점집합, 일반화한 수행을 구별한다.',
        design='동적 기하 네 과제에 대한 소표본 개별 면담과 표현 분석.',
        sample='선형대수 수강생 두 명의 개별 면담 여섯 차례.',
        supports=['유한한 매개변수 범위와 전체 직선', '두 독립 방향이 생성한 점과 평면의 좌표식']),
}

CLAIMS = [
    (SM, 'SC23-01', [COORD], [5, 6, 7],
     '강좌의 공간좌표 학습 성과에는 세 축에서 점을 표시하기, 두 점 사이의 거리, 주어진 비로 선분을 나누는 점의 좌표가 함께 나온다.',
     '학습 성과 목록과 실제 총점 검사를 구별한다. 좌표·거리·내분 항목별 성공률이 보고됐다고 해석하지 않는다.'),
    (SM, 'SC23-02', [COORD], [6, 8, 11],
     '표 1의 사후 평균은 기존 수업 반 61.06, 영상 활용 반 70.79다. 두 평균을 빼면 9.73점인데 바로 아래 본문은 3.58점이라고 서술한다.',
     '표와 본문의 수치가 달라 원자료 없이 단일 효과값을 확정하지 않는다. 총점 차이를 내분이나 공간거리만의 변화로 해석하지 않는다.'),
    (DG, 'DO26-01', [SPH, PLANE], [7, 11, 12],
     '그림 3에서 원점 중심·반지름 5인 구의 식 대응은 정답 72, 오답 8, 미응답 5였다. 본문은 다수의 선택에 이유가 붙지 않았다고 설명한다.',
     '이 연결은 벡터식으로 표현하는 대상 중 구에만 해당한다. 평면의 법선, 이동된 구, 식을 스스로 만드는 수행을 확인한 자료는 아니다.'),
    (DG, 'DO26-02', [SPH], [11, 12],
     '그림 4에는 구의 좌표축 절편을 확인한 응답이 있고, 그림 5에는 다른 곡면을 구의 방정식과 연결한 예가 있다.',
     '절편은 후보를 확인하는 일부 정보다. 같은 절편을 가진 다른 점집합도 있으므로 거리 조건까지 설명하는지 따로 확인한다.'),
    (TL, 'LP22-01', [LINE], [13, 14, 15],
     '한 참여자는 슬라이더를 움직여 생긴 선분과 모든 실수 값을 허용할 때 얻는 전체 직선을 구별했다. 두 참여자는 한 매개변수로 직선 위 점을 표현했다.',
     '해당 과제는 원점을 지나는 직선이다. 기준점을 옮긴 식의 해석이나 임의 직선의 독립 수행은 따로 확인한다.'),
    (TL, 'LP22-02', [LINE, PLANE], [15, 16, 17],
     '직선 과제에서는 한 방향의 실수배를, 평면 과제에서는 독립인 두 방향의 실수배 합을 사용했다. 두 참여자는 연구자의 단서 뒤 평면의 예를 x+z=0으로 나타냈으며 한 참여자는 방법의 일반화에 확신을 유보했다.',
     '단서 전의 식과 단서 뒤의 소거를 구별한다. 대학의 생성과 매개변수 표현을 고교에서 평면의 법선 조건을 배우는 필수 경로로 적용하지 않는다.'),
]

OBSERVATIONS = {
    SM: [
        probe('SC-P1', COORD, 'A=(1,2,3)과 B=(1,2,7)을 xy평면에 정사영하고 공간에서의 거리를 구하라. 정사영이 같아도 두 점이 다른 이유를 설명하라.',
              '두 정사영은 (1,2)로 같다. z좌표가 4만큼 달라 공간거리는 4다. 정사영에는 z좌표가 남지 않는다.',
              '정사영 좌표가 같다는 사실과 공간의 세 좌표가 모두 같다는 조건을 구분한다.'),
        probe('SC-P2', COORD, 'A=(−2,1,4)와 B=(4,−2,−2) 사이의 거리와 AP:PB=1:2인 내분점 P를 구하라. 비를 2:1로 바꾼 점과 비교하라.',
              '거리의 제곱은 36+9+36=81이어서 거리는 9다. 1:2는 A에서 B로 1/3 이동한 (0,0,2), 2:1은 2/3 이동한 (2,−1,0)이다.',
              '세 좌표의 차, 비가 가리키는 출발점, 내분점의 방향을 구별한다.'),
    ],
    DG: [
        probe('DO-P1', SPH, 'x²+y²+z²=25와 x⁴+y⁴+z⁴=625의 좌표축 절편을 비교하라. 점 (3,4,0)을 이용해 절편이 같아도 두 점집합이 같은지 판단하라.',
              '두 식 모두 각 좌표축에 ±5에서 만난다. (3,4,0)은 제곱의 합이 25지만 네제곱의 합은 337이라 첫 식에만 속한다.',
              '절편이 같다는 확인과 모든 점의 거리 조건이 같다는 확인을 구별한다.'),
        probe('DO-P2', SPH, '중심 C=(1,−2,3), 반지름 5인 구의 방정식을 쓰고 z=6, z=8, z=9에서 각 단면을 설명하라.',
              '(x−1)²+(y+2)²+(z−3)²=25다. z=6에서는 중심 (1,−2,6), 반지름 4인 원이다. z=8에서는 (1,−2,8) 한 점이고 z=9에서는 공통점이 없다.',
              '좌표 차의 부호, 단면의 중심, 원에서 점을 거쳐 공집합으로 바뀌는 경계 조건을 확인한다.'),
    ],
    TL: [
        probe('LP-P1', LINE, '(x,y,z)=(1,2,−1)+t(2,0,−3)에서 t가 모든 실수인 경우와 −1≤t≤1인 경우를 그려 비교하고 (5,2,−7)의 소속을 확인하라.',
              '모든 실수를 쓰면 직선이고, −1≤t≤1이면 끝점 (−1,2,2), (3,2,−4)를 잇는 선분이다. (5,2,−7)은 t=2에서만 나오므로 직선에만 속한다.',
              '고정 좌표와 변화하는 좌표, 매개변수의 한 값과 정의역 전체를 구별한다.'),
        probe('LP-P2', LINE, '위치벡터가 (1,2,−1)+t(2,0,−3)인 직선을 방향벡터 (−2,0,3)으로 다시 나타내고 같은 직선인 이유를 설명하라. 방향벡터를 (0,0,0)으로 바꾸면 무엇이 되는가?',
              't를 −t로 대응시키면 두 비영 방향벡터의 식이 같은 점을 모두 나타낸다. 영벡터를 쓰면 모든 t에서 (1,2,−1) 한 점만 나온다.',
              '매개변수의 부호가 달라져도 전체 점집합이 같은 경우와 방향이 사라지는 경우를 구별한다.'),
        probe('LP-P3', PLANE, 'A=(1,0,2)를 지나고 법선벡터가 (2,−1,1)인 평면을 내적 식과 좌표식으로 각각 써라. B=(2,1,1), C=(2,1,2)의 소속을 판정하고 방향벡터 (1,2,0)이 평면과 평행한 이유를 설명하라.',
              '법선과 점 (x,y,z)에서 A를 뺀 벡터의 내적이 0이다. 좌표식은 2x−y+z=4다. B는 속하고 C는 속하지 않는다. (1,2,0)은 법선과의 내적이 0이므로 평면과 평행한 방향이다.',
              '점의 위치벡터와 두 점의 차를 구별하고, 법선 방향과 평면에 평행한 방향을 비교한다.'),
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
        SM: dict(class_sizes=dict(video=19, conventional=17), post_means=dict(video=70.79, conventional=61.06),
                 post_mean_difference_from_table_1=9.73, post_mean_difference_in_prose=3.58,
                 conventional_n_gain_classifications_printed=14, conventional_n=17,
                 table_6_printed_row_label='Gain', table_6_printed_mean_difference=.72727,
                 separate_item_outcomes_verified=False),
        DG: dict(n=85, sphere_center=[0, 0, 0], radius=5, sphere_matching=dict(correct=72, incorrect=8, no_response=5),
                 sphere_vector_equation_tested=False),
        TL: dict(n=2, interviews=6, tasks=4, task_3_origin_line=True, task_4_example_plane='x+z=0',
                 task_4_teacher_hint_before_elimination=True, generalization_uncertainty_reported=True,
                 repository_published_pdf=True),
    }
    corrections = {
        SM: '표 1에서 계산한 사후 평균 차 9.73과 본문 3.58을 나누어 기록했다. 표 2의 기존 수업 반은 표시된 범주 합이 14명이며 표 1의 17명과 다르다. 표 6 제목은 사후 검사지만 행 이름은 Gain이고 평균 차는 .72727로 인쇄됐다. 원자료로 차이를 확인하지 못했다.',
        DG: '그림 3의 구 정답·오답·미응답을 그대로 기록하고, 식 선택의 수와 선택 이유가 설명된 범위를 구별했다.',
        TL: '한 매개변수 과제의 원점을 지나는 직선과 두 독립 방향으로 생성한 특정 평면을 구별하고, 매개변수 소거 전 연구자 질문과 일반화에 대한 유보를 남겼다.',
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
        entry = dict(id=sid, year=spec['year'], url=url, title=spec['title'], authors=spec['authors'], kind='공간좌표와 벡터식의 표현 연구',
            review_scope=spec['scope'], does_not_establish=spec['limit'], supports=spec['supports'],
            next_review='자체 과제의 실제 응답을 확인하고 다른 표본의 공간좌표와 벡터식 과제를 추가 대조한다.')
        bibliography.append(entry)
        note = f'data/literature_evidence/{sid}_review_notes.json'
        write(ROOT / note, dict(source_id=sid, source_url=url, source_pdf_url=pdf_urls[sid],
            source_asset_kind='pdf', source_pdf_sha256=spec['sha256'], pdf_pages=spec['total'],
            selected_text_pages=spec['pages'], visual_pdf_pages=spec['visuals'], rendered_page_sha256=image_hashes[sid],
            date=DATE, reviewer='Codex', read_scope=spec['scope'], empirical_scope=empirical,
            contains_source_full_text=False, source_pdf_redistributed=False,
            reading_log=[spec['scope']], source_corrections=[dict(location='정의·표·학생 응답', issue=corrections[sid])],
            analytic_review=details[sid]))
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
        ('SEC_12기하03-05_C03', 'DO26-01'): (
            'activity_context', '구의 방정식과 중심을 뺀 위치벡터의 길이 조건을 서로 바꾸고 같은 점을 두 식에서 확인한다.',
            '논문의 문항은 원점 중심 구의 식 선택이며 이동한 구나 벡터식의 직접 성취 자료는 아니다.'),
        ('REV-12기하03-05-1', 'DO26-01'): (
            'inference_limit', '원점 중심 구의 표준식 선택과 선택 이유를 구별해 분석했다.',
            '구의 식을 선택한 응답으로 평면의 벡터식까지 설명할 수 있거나 필수 학습 순서가 정해진다고 판단하지 않는다.'),
        ('SEC_12기하03-04_C04', 'LP22-02'): (
            'activity_context', '한 방향으로 움직일 때 얻는 직선과 법선에 수직인 방향으로 움직일 때의 평면을 점의 소속 조건으로 비교한다.',
            '연구의 두 매개변수 표현은 대학 면담에 나온다. 고교 과제는 주어진 법선과 점을 이용하는 범위로 둔다.'),
        ('REV-12기하03-04-2', 'LP22-02'): (
            'inference_limit', '교사 단서 뒤 두 학생이 매개변수 표현을 좌표식과 연결했으며 한 학생은 일반화 가능성을 유보했다.',
            '직선 과제와 평면 과제의 순서로 고교에서의 필수 선수성이나 다른 학생에 대한 인과 효과를 추론하지 않는다.'),
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
    print('Analytic geometry: 3 sources, 6 claims, 7 tasks, 4 relation entries')


if __name__ == '__main__':
    main()




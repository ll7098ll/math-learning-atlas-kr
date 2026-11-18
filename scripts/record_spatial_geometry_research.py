"""Map spatial geometry studies to authored position, distance, and projection probes."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from extend_making_pre_k_count_appendices_review import DATE
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_conic_representation_research import probe
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


CACHE = ROOT / 'tmp/literature/spatial-geometry'
GJ = 'GUTIERREZ_JAIME_2015_SPATIAL_RELATIONS'
RG = 'RAMIREZ_ET_AL_2023_ORTHOGONAL_VIEWS'
PD = 'PERTIWI_ET_AL_2024_SOLID_GEOMETRY'
REL, DIST, PROJ = [f'12기하02-0{i}' for i in range(1, 4)]
SPECS = {
    GJ: dict(year=2015, authors=['Ángel Gutiérrez', 'Adela Jaime'],
        title='Análisis del aprendizaje de geometría espacial en un entorno de geometría dinámica 3-dimensional',
        url='https://doi.org/10.30827/pna.v9i2.6106',
        pdf_url='https://funes.uniandes.edu.co/wp-content/uploads/tainacan-items/32454/1213506/Gutierrez2015PNA92Analisis.pdf',
        stem='gutierrez-jaime-2015', sha256='f8fd0842416ca2b868e36358afeb7c6a302dc76e39f40510912caafde4270477',
        total=31, pages=[1, 9, 16, 18, 21, 22, 26], visuals=[16, 22],
        scope='동적 공간기하 활동의 구성, 평행한 두 직선의 공면성, 서로 다른 평행 평면에 놓인 직선에 대한 대화를 대조했다.',
        limit='수학적 재능을 보인 학생 한 명의 사례다. 질문과 수정 뒤의 설명을 일반 학생의 자발적 수행으로 확대할 수 없다.',
        design='Cabri 3D를 사용한 수업 실험에서 학생 한 명의 활동·면담을 분석.',
        sample='수학적 재능을 보인 학생 한 명.',
        supports=['소프트웨어 객체 수와 기하적 유일성', '평행 평면에 놓인 직선의 비평행 가능성']),
    RG: dict(year=2023, authors=['Brahiam Ramírez Jofré', 'Marcelo González Díaz', 'Ricardo Zambrano Reyes'],
        title='Errores que cometen los estudiantes de tercero y cuarto año de enseñanza media en vistas ortogonales de figuras geométricas 3D',
        url='https://doi.org/10.46219/rechiem.v15i2.125',
        pdf_url='https://funes.uniandes.edu.co/wp-content/uploads/tainacan-items/32454/1567424/1791381548573477_Ramirez2023Errores.pdf',
        stem='ramirez-et-al-2023', sha256='e4727247972be7637d76d36a4d196f6fdbcbccba213c235804c8e451385f2629',
        total=17, pages=[1, 5, 6, 9, 10, 11, 12, 15], visuals=[10, 12],
        scope='정사영 응답의 표 3~5, 정사영을 그리고 그 그림에서 입체를 재구성하는 두 과제, 깊이와 방향의 오류 예를 확인했다.',
        limit='칠레 두 학교의 해당 응답에서 나타난 오류율이다. 길이·넓이의 코사인 비나 국내 고교생 오류의 비율로 사용하지 않는다.',
        design='정육면체 조합의 그림에 관한 네 부분 설문과 개별 응답 유형 분류.',
        sample='칠레 두 학교의 고교 3·4학년 학생 30명.',
        supports=['관찰 방향별 정사영 응답', '서로 다른 방향에서 본 모양의 통합']),
    PD: dict(year=2024, authors=['S Pertiwi', 'D Dasari', 'E Sumiaty'],
        title='High School Students’ Ontogenic Obstacles in Solving Solid Geometry Problems Viewed from Spatial Ability',
        url='https://doi.org/10.17501/26307413.2023.6101',
        pdf_url='https://tiikmpublishing.com/proceedings/index.php/foe/article/download/1340/1026/3808',
        stem='pertiwi-et-al', sha256='d21ed8b8e0f50b61a22bfb34122b015bee0b6b8dbd7b02b5c7bbad380cfb0a36',
        total=11, pages=[1, 4, 5, 6, 7, 8, 9], visuals=[8],
        scope='6문항 검사에서 공간거리와 평면 표현을 다룬 사례, 그림 4·5, 점에서 평면까지의 거리 문항 결과를 대조했다.',
        limit='인도네시아 한 학교의 질적 사례 연구다. 삼수선 정리 숙달과 표현 사이의 인과 경로를 검증한 자료는 아니다.',
        design='피타고라스 관련 3문항과 공간도형 3문항의 검사, 관찰, 일부 학생 면담.',
        sample='인도네시아 세랑의 공립 고교 12학년 44명.',
        supports=['관찰 방향과 평면 표현', '점에서 직선·평면까지의 거리에서 수선의 발 선택']),
}

CLAIMS = [
    (GJ, 'SP15-01', [REL], [9, 16],
     '학생은 두 평행 직선을 선택하는 도구 동작을 네 번 반복한 뒤 네 개의 평면을 만들었다고 말했다. 서로 다른 평면의 수를 묻는 과정에서 네 번 모두 같은 평면이라고 설명했다.',
     '도구의 객체 생성 횟수와 서로 다른 점집합의 수를 구별한다. 별도 조건 없이 세 점이 임의의 포물선을 유일하게 정한다는 학생의 비유까지 사용하지 않는다.'),
    (GJ, 'SP15-02', [REL], [18, 21, 22],
     '평행한 두 평면에 각각 속한 직선에 대해 학생은 잠시 두 직선도 평행하다고 답했다. 연구자의 질문 뒤 두 평면이 만나지 않아 두 직선의 공통점도 없다고 설명했다.',
     '교점 없음과 방향이 같은지를 따로 묻는다. 연구자가 개입한 한 학생의 응답이므로 단서 없는 숙달로 판정하지 않는다.'),
    (RG, 'SP23-01', [PROJ], [5, 6, 10, 12],
     '표 3에서 P3의 정사영 응답 중 정답 유형은 43.6%다. 표 5에서 오류율은 위에서 본 모양 66.4%, 뒤에서 본 모양 63.2%, 오른쪽에서 본 모양 36.0%로 집계됐다.',
     '표 3은 응답 유형, 표 5는 보는 방향별 응답 비율이다. 30명 중 같은 수의 학생이 틀렸다는 뜻으로 환산하지 않는다.'),
    (RG, 'SP23-02', [PROJ], [10, 11, 12],
     'P4는 주어진 여러 정사영에서 입체를 그리는 과제다. 표 4에서 정답 유형은 51.8%이고, 본문에는 한 방향의 모양만 입체로 옮긴 뒤 다른 방향을 통합하지 않은 응답이 있다.',
     '한 방향의 윤곽과 여러 방향에서 동시에 성립하는 조건을 구별한다. 같은 입체와 정답 비율을 가정해 P3·P4를 직접 비교하지 않는다.'),
    (PD, 'SP24-01', [DIST, PROJ], [6, 7, 8],
     '같은 검사에서 위·왼쪽 모양을 바꾸어 그린 4a 사례와, 점 V에서 직선 QS까지의 거리에 끝점 R이 QS 위에 없는 모서리 VR을 고른 5a 사례가 제시됐다.',
     '그림 4와 5는 과제별 발췌다. 한 학생이 두 오류를 모두 보였다거나 해당 오류를 바로잡으면 다른 과제로 전이된다고 추론하지 않는다.'),
    (PD, 'SP24-02', [DIST], [6, 9],
     '점에서 평면까지의 거리를 다룬 6a에서 어려움을 보인 학생 9명이 보고됐다. 저자는 거리 선택과 이후의 계산 및 설명을 구별해 서술했다.',
     '특정 문항에 대한 보고다. 점에서 평면까지의 거리와 점에서 그 평면 안의 직선까지의 거리, 삼수선 정리의 정당화를 별도로 살핀다.'),
]

OBSERVATIONS = {
    GJ: [
        probe('SPG-P1', REL, '직선 l은 (0,0,0)을 지나 x축 방향, m은 (0,0,2)를 지나 y축 방향이다. xy평면에 비춘 두 직선과 공간에서 두 직선의 위치 관계를 각각 말하라.',
              'xy평면에서 두 정사영은 원점에서 만난다. 공간에서 l은 z=0, m은 z=2에 있으므로 만나지 않으며 방향도 달라 꼬인 위치다.',
              '평면에 비친 교점과 실제 공간의 공통점을 구별한다.'),
        probe('SPG-P2', REL, '평면 z=0에 대해 l=(t,0,0), m=(t,0,2), n=(1,1,t)의 위치를 각각 말하고 교점의 개수를 설명하라. t는 모든 실수다.',
              'l은 평면에 포함되어 공통점이 무수히 많고, m은 교점이 없이 평행하며, n은 (1,1,0)에서 한 번 만난다. n의 방향은 평면에 수직이다.',
              '직선과 평면의 포함·평행·교차를 그림의 인상 대신 모든 점의 z좌표로 구별한다.'),
    ],
    RG: [
        probe('SPR-P1', PROJ, '단위 정육면체의 중심이 (0,0,0), (1,0,0), (0,0,1)인 조립물을 xy평면과 xz평면에 각각 정사영하라. 맨 위의 정육면체를 빼면 어느 정사영이 달라지는가?',
              'xy평면에는 중심 (0,0), (1,0)의 두 칸이 보인다. xz평면에는 (0,0), (1,0), (0,1)의 세 칸이 보인다. 맨 위를 빼면 xz 정사영만 바뀐다.',
              '투영 방향에 놓인 두 칸의 겹침과, 한 정사영만으로 높이를 알 수 없는 이유를 기록한다.'),
        probe('SPR-P2', PROJ, '원점에서 (3,4,12)까지의 선분 길이와 xy평면에 정사영한 길이를 구하라. 원점과 (3,0,0), (3,4,3), (0,4,3)을 꼭짓점으로 하는 직사각형의 넓이와 정사영 넓이도 비교하라.',
              '선분의 길이는 13, 정사영 길이는 5다. 직사각형의 두 변 길이는 3과 5라 넓이는 15이고, 정사영은 3×4=12다. 선분의 기울기에 따른 5/13과 두 평면 사이 각에 따른 4/5를 구별한다.',
              '보는 방향별 윤곽 문제와 길이·넓이 비율을 계산하는 과제를 따로 판정한다.'),
    ],
    PD: [
        probe('SPD-P1', DIST, 'P=(2,3,6), 평면 z=0, 그 평면 안의 x축이 주어졌다. 평면으로 내린 발 H와 x축에 내린 발 Q를 찾아 두 거리를 구하고, 원점 O까지의 거리가 x축까지의 거리와 왜 다른지 설명하라.',
              'H=(2,3,0), Q=(2,0,0)이다. PH=6, HQ=3이고 PQ=3√5다. PO=7이며 O는 x축 위에 있지만 PO가 x축에 수직이 아니므로 최단 거리가 아니다.',
              '평면의 발, 직선 위 점, 직선에 대한 수직성을 별도로 확인한다.'),
        probe('SPD-P2', DIST, 'P=(2,0,6)을 평면 z=0과 그 안의 x축에 각각 수직으로 내리자. 두 수선의 발이 같아지는 이유와 이때 거리 두 개를 설명하라.',
              '두 발은 (2,0,0)으로 같다. 평면의 수선의 발이 이미 x축 위에 있고 P에서 그 점까지의 선분은 x축에도 수직이므로 두 거리가 모두 6이다.',
              '평면의 발이 목표 직선 위에 있는 경계 사례에서, 길이 0인 보조 선분에 방향을 부여하지 않는지 확인한다.'),
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
        GJ: dict(n=1, software='Cabri 3D', repeated_plane_constructions=4, distinct_planes=1,
                 interviewer_prompt_before_corrected_answer=True),
        RG: dict(n=30, schools=2, p3_correct_response_percent=43.6, p4_correct_response_percent=51.8,
                 p3_errors_by_view=dict(right=36.0, front=56.3, left=55.6, top=66.4, back=63.2)),
        PD: dict(n=44, grade=12, prerequisites_items=3, spatial_items=3, problem_6a_reported_difficulties=9,
                 participant_level_crosstab_for_examples=False, proceedings_issue_year=2023),
    }
    corrections = {
        GJ: '소프트웨어 동작의 반복과 기하적 평면의 수를 분리하고, 평행 평면 사례는 연구자 개입 전후를 구별했다.',
        RG: '표 3~5의 응답 비율은 학생 30명에 대한 개인별 정답률이 아니다. 정사영의 종류와 역방향 재구성 과제를 분리했다.',
        PD: '그림 5의 R이 QS에 속하지 않으므로 VR을 목표 직선까지의 거리로 사용할 수 없다. 보고서의 사례 발췌를 개인별 교차표처럼 사용하지 않는다.',
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
        entry = dict(id=sid, year=spec['year'], url=url, title=spec['title'], authors=spec['authors'], kind='공간도형 표현과 거리 연구',
            review_scope=spec['scope'], does_not_establish=spec['limit'], supports=spec['supports'],
            next_review='자체 과제의 실제 응답을 확인하고 다른 표본의 공간도형 과제를 추가 대조한다.')
        bibliography.append(entry)
        note = f'data/literature_evidence/{sid}_review_notes.json'
        write(ROOT / note, dict(source_id=sid, source_url=url, source_pdf_url=pdf_urls[sid],
            source_asset_kind='pdf', source_pdf_sha256=spec['sha256'], pdf_pages=spec['total'],
            selected_text_pages=spec['pages'], visual_pdf_pages=spec['visuals'], rendered_page_sha256=image_hashes[sid],
            date=DATE, reviewer='Codex', read_scope=spec['scope'], empirical_scope=empirical,
            contains_source_full_text=False, source_pdf_redistributed=False,
            reading_log=[spec['scope']], source_corrections=[dict(location='정의·표·학생 응답', issue=corrections[sid])],
            spatial_review=details[sid]))
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
        'SEC_12기하02-02_C04': ('activity_context', '평면 정사영을 그린 뒤 목표 직선 위의 수선의 발을 따로 표시하고 서로 다른 두 거리를 비교한다.',
                               '연구는 표현과 거리 문항의 사례를 제공한다. 정사영을 활용한 삼수선 정리 수업의 효과를 확인한 자료는 아니다.'),
        'REV-12기하02-02-1': ('inference_limit', '같은 검사에 방향별 평면도와 점에서 직선까지의 거리 문항이 포함됐고 서로 다른 응답 사례가 제시됐다.',
                              '두 문항의 개인별 교차표가 제시되지 않아 수행 전이나 필수 선수성을 판단할 수 없다.'),
    }
    assert pairs == {(rid, 'SP24-01') for rid in interpretations}
    reviewed = load(ROOT / FILE)
    for rid, (role, finding, limit) in interpretations.items():
        relation = next(r for r in relations if r['id'] == rid)
        reviewed['records'].append(dict(relation_id=rid, claim_id='SP24-01', role=role, finding=finding, limit=limit,
            relation_snapshot=relation_snapshot(relation), claim_snapshot=claim_snapshot(new['SP24-01'], registry['sources'][PD])))
    apply_literature_context(relations, registry, registry=reviewed)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviewed)
    build_report()
    print('Spatial representations: 3 sources, 6 claims, 6 tasks, 2 relation entries')


if __name__ == '__main__':
    main()



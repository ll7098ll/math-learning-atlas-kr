"""Map three conic representation studies to scoped claims and original probes."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from extend_making_pre_k_count_appendices_review import DATE
from literature_review import ROOT, build_report, digest, load_registry, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


CACHE = ROOT / 'tmp/literature/conic-representations'
VAL = 'VALBUENA_ET_AL_2021_CONIC_REPRESENTATIONS'
KB = 'KONDRATIEVA_BERGSTEN_2021_PARABOLA'
SB = 'SANCHEZ_BARON_2015_PARABOLA'
PAR, ELL, HYP, TAN = [f'12기하01-0{i}' for i in range(1, 5)]
SPECS = {
    VAL: dict(year=2021, authors=['Sonia Valbuena-Duarte', 'Yilmar Tamara-Gutiérrez', 'Jesús D. Berrio-Valbuena'],
        title='Intervención didáctica tecnológica para el estudio de las secciones cónicas basada en el potencial semiótico',
        url='https://doi.org/10.4067/S0718-50062021000100181',
        pdf_url='https://scielo.conicyt.cl/pdf/formuniv/v14n1/0718-5006-formuniv-14-01-181.pdf',
        stem='valbuena-et-al-2021', sha256='1ea3097393c1c7c1866aff5832ee2b3cc8ac4846e1bc5ddece3f56302c469d28',
        total=14, pages=[1, 4, 5, 6, 8, 9, 10, 11], visuals=[6, 8, 11],
        scope='표 1의 표현 분류와 그림 4의 포물선 활동, 네 응답 발췌, 그림 5의 사전·사후 점수 비교를 확인했다.',
        limit='콜롬비아 예비 수학교사 한 집단의 비교다. 국내 고등학생의 난점 빈도와 도구 자체의 효과는 별도로 검증한다.',
        design='의도 표집한 단일 집단의 사전·사후 서면 검사와 수업 중 관찰.',
        sample='해석기하 수강 중인 예비 수학교사 38명.',
        supports=['거리 자취·원뿔 절단·좌표의 표현', '그래프를 매개로 한 방정식 변환', '사전·사후 변환 점수']),
    KB: dict(year=2021, authors=['Margo Kondratieva', 'Christer Bergsten'],
        title='Secondary School Mathematics Students Exploring the Connectedness of Mathematics: The Case of the Parabola and its Tangent in a Dynamic Geometry Environment',
        url='https://doi.org/10.54870/1551-3440.1520',
        pdf_url='https://www.diva-portal.org/smash/get/diva2%3A1442299/FULLTEXT01.pdf',
        stem='kondratieva-bergsten-2021', sha256='fea72dd4c635f8102f29a06fae57615dcb9f7a1a5c151604b37ac306789018ef',
        total=28, pages=[2, 11, 12, 13, 14, 15, 16, 17, 18], visuals=[13, 17],
        scope='11학년 두 수업의 자발적 정의, 교사 시범, 수직이등분선을 이용한 설명 사례를 확인했다.',
        limit='선발·심화 교육을 하는 한 학교의 사례다. 보고한 설명의 빈도는 일반 학생의 비율이나 수업 효과로 해석하지 않는다.',
        design='동적 기하 환경에서 두 집단에 실시한 수업의 학생 작업과 대화 사례.',
        sample='모스크바의 수학 선발 학교 11학년 학생 20명과 12명.',
        supports=['이차함수 그래프와 거리 자취', '교사 시범 뒤의 포물선 접선 근거']),
    SB: dict(year=2015, authors=['Ever Hernán Sánchez Barón'],
        title='Algunas dificultades de aprendizaje presentes en el estudio de la parábola en un grupo de estudiantes de grado once del Colegio María Cano J.T.',
        url='https://funes.uniandes.edu.co/funes-documentos/algunas-dificultades-de-aprendizaje-presentes-en-el-estudio-de-la-parabola-en-un-grupo-de-estudiantes-de-grado-once-del-colegio-maria-cano-j-t/',
        pdf_url='https://funes.uniandes.edu.co/wp-content/uploads/tainacan-items/32454/1244795/S25C325A1nchez2015Algunas.pdf',
        stem='sanchez-et-al-2015', sha256='5a9082a57791d42b61d08c26d65b711d4a3e2d77b4651258a384e7f86d479ce7',
        total=7, pages=[1, 3, 4, 5, 6], visuals=[6],
        scope='보고서의 표집, 종이와 GeoGebra 활동, 명령 사용 관찰과 사전·사후 그래프의 표기를 확인했다.',
        limit='여섯 학생의 사례 보고다. 그래프는 하위 범주 이름과 채점 대응을 제시하지 않아 개별 개념의 점수로 해석할 수 없다.',
        design='사전 검사, 종이와 도구를 이용한 수업 활동, 사후 검사의 질적 사례 연구.',
        sample='보고타 María Cano 학교 11학년 한 반 30명에서 학업 성취를 고려해 선택한 6명.',
        supports=['도구 명령과 포물선 개념 수행의 분리']),
}

CLAIMS = [
    (VAL, 'CON21-01', [PAR, ELL, HYP], [4, 6, 9],
     '예비 교사의 사전 검사에서 자취·원뿔 절단·방정식 사이를 오가는 어려움이 보고됐다. 표 1은 언어, 대수, 그림 표현을 나누고 본문은 네 사람의 정의 발췌를 제시한다.',
     '네 발췌는 곡선별 오답률이 아니다. 쌍곡선의 두 가지를 다룰 때는 표의 거리 차 표현을 절댓값 조건으로 명확히 한다.'),
    (VAL, 'CON21-02', [PAR], [8],
     '계수가 소수인 포물선을 표준형으로 쓰는 데 어려움이 보고됐고, 일부 참여자는 그래프에서 꼭짓점·초점·준선을 찾아 식을 설명했다.',
     '그래프를 조작해 본 수행과 거리 식을 역으로 유도한 수행을 따로 확인한다. 이동된 예의 접선 계산은 여기서 다루지 않는다.'),
    (VAL, 'CON21-03', [PAR, ELL, HYP], [4, 9, 10, 11],
     '예비 교사 38명의 사전·사후 검사에서 표현 변환 점수 평균은 2.11에서 3.08로 보고됐다. 그림 5는 변환과 전체 점수의 분포를 구별한다.',
     '동일 집단에서 시간에 따라 나타난 변화다. 프로그램 자체의 효과나 포물선·타원·쌍곡선 각각의 점수 차이는 이 평균으로 판단할 수 없다.'),
    (KB, 'PAR21-01', [PAR], [11, 12, 13],
     '수업에서 처음 쓴 포물선 정의는 함수 그래프를 사용했다. 다른 정의를 묻자 몇몇 학생이 점과 직선까지의 거리가 같다는 성질을 설명했다.',
     '자발적 정의와 질문 뒤의 응답을 구분한다. 한 학교의 사례이며 이차함수에 대한 모든 학생의 이해를 대표하지 않는다.'),
    (KB, 'PAR21-02', [PAR, TAN], [12, 15, 16, 17, 18],
     '처음에는 학생이 수직이등분선 구성을 제안하지 않았다. 교사 시범 뒤 여러 설명이 나왔고, 접선임을 더 설명하라는 질문 뒤 다섯 학생이 정당화를 제시했다.',
     '구성 시범과 후속 설명을 구별한다. 그림이나 단일 교점만으로 모든 직선의 접선을 판정할 수 없고 판별식 풀이를 국내 범위에 추가하지 않는다.'),
    (SB, 'PAR15-01', [PAR], [4, 5, 6],
     '보고타 11학년 6명 사례에서 종이와 GeoGebra를 사용했고, 도구 명령 사용이 자주 보고된 어려움이었다.',
     '막대 그림의 범주는 번호로만 표시된다. 명령 수행의 어려움이나 막대 높이를 특정 포물선 개념의 부족으로 직접 판정하지 않는다.'),
]

def probe(id, code, question, expected, interpretation):
    return dict(id=id, standard_codes=[code], question=question, expected=expected,
                interpretation=interpretation, student_validated=False)

OBSERVATIONS = {
    VAL: [
        probe('CON-P1', ELL, '타원 x²/25+y²/9=1의 두 초점을 찾고, (0,3)이 두 거리의 합 조건을 만족하는지 확인하라. 같은 거리 합을 만족하는 모든 점이 이 식을 만족하는 이유도 설명하라.',
              '초점은 (±4,0)이다. (0,3)에서 각 초점까지 5이므로 합은 10이다. 왼쪽·오른쪽 초점까지의 거리를 d₁,d₂라 하면 d₁+d₂=10, d₁²−d₂²=16x에서 d₁−d₂=8x/5다. d₁=5+4x/5를 제곱해 정리하면 타원 식이 나온다.',
              '특정 점 검산과 자취 전체에 대한 추론을 구분하고 초점 거리 4와 장반축 길이 5를 구별한다.'),
        probe('CON-P2', HYP, '초점 F₋=(−5,0), F₊=(5,0), 거리 차의 절댓값 8인 자취를 생각하자. (4,0)과 (−4,0)을 각각 검사하고, PF₋−PF₊=8만 사용하면 어느 쪽이 빠지는지 설명하라.',
              '(4,0)의 부호 있는 차는 9−1=8, (−4,0)의 차는 1−9=−8이어서 두 점 모두 자취에 속한다. +8만 쓰면 왼쪽 가지가 빠진다. 표준형은 x²/16−y²/9=1이다.',
              '거리 차의 부호, 식의 두 가지와 초점 위치를 각각 확인한다.'),
        probe('CON-P3', PAR, '그래프 y=−0.25x²의 초점과 준선을 찾아라. 그래프 위의 모든 점이 거리 조건을 만족하고 그 거리 조건을 만족하는 점은 그래프 위에 있음을 보여라.',
              '초점 (0,−1), 준선 y=1이다. 초점까지 거리의 제곱 x²+(y+1)²와 준선까지 거리의 제곱 (y−1)²의 같음은 x²=−4y와 동치다. 두 거리가 음이 아니므로 제곱의 같음에서 거리의 같음을 되찾을 수 있다.',
              '소수 계수의 크기와 부호를 읽는 수행 및 식과 자취 사이의 두 방향을 따로 확인한다.'),
    ],
    KB: [
        probe('PAR-P1', PAR, '포물선 y²=12x의 초점과 준선을 정하고 x=3인 두 점을 그려라. 이 곡선이 포물선이면서 x를 입력으로 한 y의 함수 그래프가 아닌 이유를 설명하라.',
              '초점 (3,0), 준선 x=−3이다. x=3일 때 y=±6이며 두 점 모두 초점과 준선까지의 거리가 6이다. 같은 x에 서로 다른 두 y가 있어 y=f(x)로 나타낼 수 없다.',
              '함수 표현의 방향과 포물선의 거리 정의를 구별한다.'),
        probe('PAR-P2', TAN, 'x²=4y의 점 P=(2,1)에서 초점 F=(0,1)와 P에서 준선에 내린 수선의 발 B=(2,−1)를 이용해 접선을 찾아라. 직선 x=2도 교점이 하나인데 접선인지 비교하라.',
              'FB의 수직이등분선 y=x−1은 P를 지난다. 곡선의 y값과 이 직선의 차이는 (x−2)²/4로 P에서만 0이고 양옆에서 양수다. 다른 기울기 m의 직선은 그 차이가 (x−2)((x−2)/4+1−m)이므로 P 가까이에서 곡선을 가로지른다. x=2도 곡선이 그 양쪽으로 이어져 접선이 아니다.',
              '접점 구성과 대수적 정당화, 축 방향 직선의 단일 교점 반례를 분리해서 기록한다.'),
    ],
    SB: [
        probe('PAR-P3', PAR, '초점 (2,0), 준선 x=−2인 포물선에서 x=2인 점을 종이에서 먼저 구하라. 도구로 자취를 표시한 뒤 화면에서 확인한 것과 손으로 보인 이유를 따로 적어라.',
              '준선까지 거리가 4이므로 초점과 x좌표가 같은 점의 y는 ±4다. 식은 y²=8x이며, 도구의 표시와 등거리 조건에서 식을 유도한 근거를 따로 남긴다.',
              '명령을 사용한 결과와 수학적 설명을 분리해 기록한다.'),
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
        VAL: dict(n=38, questions_per_test=12, comparator_group_reported=False,
                  excerpt_count=4, conversion_means=[2.11, 3.08], conversion_mean_difference=.97,
                  shapiro_wilk_p=.005, wilcoxon_z=-5.259),
        KB: dict(group_sizes=[20, 12], grade=11, school_selective=True,
                 construction_2_proposed_before_demo=False, tangency_justifications_after_prompt=5),
        SB: dict(class_n=30, cases=6, grade=11, graph_subcategories=7, graph_subcategory_labels_named=False),
    }
    corrections = {
        VAL: '표 1의 쌍곡선 거리 차는 절댓값으로 보완해야 두 가지가 포함된다. 타원 예시 그림은 기울어져 있으므로 좌표축에 평행한 표준형과 같은 그림으로 보지 않는다. 본문의 Shapiro–Wilk p=.005와 윌콕슨 z=−5.259를 별개로 기록했다.',
        KB: '논문의 판별식 학생 풀이와 미적분 접근은 관찰 사실로만 기록했다. 자체 접선 과제는 이동되지 않은 곡선에서 거리와 완전제곱으로 정당화하고 단일 교점 반례를 포함했다.',
        SB: 'PDF 6쪽 그림의 하위 범주 1~7과 수준의 대응 원자료는 확인하지 못했다. 막대 높이에 개념 이름을 부여하거나 효과량을 추정하지 않았다.',
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
        entry = dict(id=sid, year=spec['year'], url=url, title=spec['title'], authors=spec['authors'], kind='이차곡선 표현의 학습 연구',
            review_scope=spec['scope'], does_not_establish=spec['limit'], supports=spec['supports'],
            next_review='자체 과제의 실제 응답을 확인하고 다른 표본의 이차곡선 과제를 추가 대조한다.')
        bibliography.append(entry)
        note = f'data/literature_evidence/{sid}_review_notes.json'
        write(ROOT / note, dict(source_id=sid, source_url=url, source_pdf_url=pdf_urls[sid],
            source_asset_kind='pdf', source_pdf_sha256=spec['sha256'], pdf_pages=spec['total'],
            selected_text_pages=spec['pages'], visual_pdf_pages=spec['visuals'], rendered_page_sha256=image_hashes[sid],
            date=DATE, reviewer='Codex', read_scope=spec['scope'], empirical_scope=empirical,
            contains_source_full_text=False, source_pdf_redistributed=False,
            reading_log=[spec['scope']], source_corrections=[dict(location='정의·표·학생 응답', issue=corrections[sid])],
            conic_review=details[sid]))
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
        'SEC_12기하01-01_C04': ('activity_context', '초점과 준선의 거리로 접점을 만든 뒤 수선과 선분의 수직이등분선을 이용해 접선임을 설명한다.',
                               '시범 후의 설명을 독립 구성과 구별하고, 교점이 하나인 축 방향 직선도 비교한다.'),
        'REV-12기하01-01-2': ('inference_limit', '교사의 구성을 본 뒤 일부 학생이 등거리 조건으로 직선과 곡선의 관계를 정당화했다.',
                              '선발된 한 학교의 사례로 포물선 정의에서 세 이차곡선의 접선으로 가는 필수 학습 순서를 정할 수 없다.'),
    }
    assert pairs == {(rid, 'PAR21-02') for rid in interpretations}
    reviewed = load(ROOT / FILE)
    for rid, (role, finding, limit) in interpretations.items():
        relation = next(r for r in relations if r['id'] == rid)
        reviewed['records'].append(dict(relation_id=rid, claim_id='PAR21-02', role=role, finding=finding, limit=limit,
            relation_snapshot=relation_snapshot(relation), claim_snapshot=claim_snapshot(new['PAR21-02'], registry['sources'][KB])))
    apply_literature_context(relations, registry, registry=reviewed)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviewed)
    build_report()
    print('Conic representations: 3 sources, 6 claims, 6 tasks, 2 relation entries')


if __name__ == '__main__':
    main()


"""Record form-specific assessment evidence, scoring units, and score equating."""
from decimal import Decimal

from extend_lt2_length_assets_review import load, sha, write
from extend_making_pre_k_count_appendices_review import DATE, inspect_pdf
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_making_pre_k_count_review import KINDER
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


ORIGINAL = 'CLEMENTS_SARAMA_LIU_2008_REMA'
SHORT = 'DONG_ET_AL_2021_REMA_SHORT_FORM'
TRIAD = 'DUMAS_ET_AL_2019_TRIAD_MEASUREMENT'
AUTHOR = 'https://www.researchgate.net/publication/247513640_Development_of_a_measure_of_early_mathematics_achievement_using_the_Rasch_model_The_Research-Based_Early_Maths_Assessment'
ADD, SUB, SHAPE, DATA, TEST = '2수01-05', '2수01-06', '2수03-03', '12실통02-02', '12실통03-04'
SOURCES = {
    ORIGINAL: dict(year=2008, doi='10.1080/01443410701777272',
        title='Development of a measure of early mathematics achievement using the Rasch model: the Research-Based Early Maths Assessment',
        authors=['Douglas H. Clements', 'Julie H. Sarama', 'Xiufeng H. Liu'],
        scope='저자가 공개한 웹 본문에서 채점 범주와 도형 과제, 항목 유지 기준 및 모형 적합성을 설명한 선정 대목을 확인했다.',
        limit='초기 REMA의 문항 개발 결과다. MPC의 48문항 판본이나 단축형의 전체 시행 절차를 확인한 자료로 쓰지 않는다.',
        design='초기 수학 검사 개발과 문항 반응 모형 검증.', sample='초기 236개 채점 항목 중 199개를 유지했다.',
        supports=['과제와 채점 항목의 구별', '도형 문항의 오답 해석']),
    SHORT: dict(year=2021, doi='10.1177/07342829211037195',
        title='Measuring Early Childhood Mathematical Cognition: Validating and Equating Two Forms of the Research-Based Early Mathematics Assessment',
        authors=['Yixiao Dong', 'Douglas H. Clements', 'Crystal A. Day-Hess', 'Julie Sarama', 'Denis Dumas'],
        scope='REMA-SF의 시행, 부분 정답과 전략 기록, 표본별 신뢰도와 두 판본 점수 변환을 ERIC 판면과 대조했다.',
        limit='80문항 REMA-SF와 이 연구의 REMA-Full에 한정한다. 48문항 REMA-K와의 점수 비교, 모든 집단의 점수 불변성 및 국내 적용은 별도다.',
        design='단축형 개발·별도 표본 검증과 공통 문항을 사용한 두 판본 점수 동등화.',
        sample='본 연구 1,912개 관측, 외부 표본 181명, 정식형 점수 비교 자료 1,305명.',
        supports=['판본별 시행', '정답과 전략', '공통 문항과 점수 동등화']),
    TRIAD: dict(year=2019, doi='10.1177/2332858419879446',
        title='A Preschool Mathematics Intervention Can Significantly Improve Student Learning Trajectories Through Elementary School',
        authors=['Denis Dumas', 'Daniel McNeish', 'Julie Sarama', 'Douglas H. Clements'],
        scope='TRIAD 종단 재분석에서 REMA의 영역별 시작·중단 규칙과 이후 TEAM 3–5 검사 도구를 확인했다.',
        limit='같은 TRIAD 코호트의 재분석이다. 이 시행 절차를 다른 REMA 판본에 적용하거나 MPC의 별도 효과로 합산하지 않는다.',
        design='TRIAD 자료의 종단 재분석. 여기서는 도구와 시행을 대조했다.',
        sample='원 TRIAD 1,305명, 5학년 말까지 전체 검사 완료 781명.',
        supports=['영역별 시행과 기록', '시점별 검사 도구']),
}
PDFS = {
    SHORT: ('rema-short-form-2021', 'https://files.eric.ed.gov/fulltext/EJ1316908.pdf',
            '37813176f543b77013bcf4da74941bf8cd020ae274e52460770034970befb980', 16, [4, 5, 6, 8, 10, 11, 12, 13], [4, 10, 11, 12]),
    TRIAD: ('rema-dumas-2019', 'https://files.eric.ed.gov/fulltext/EJ1238415.pdf',
            'b1af9e64246793ba345be3cec2f6c4945cfbb5b188adfcb9ffc34268e480e9f0', 15, [1, 5, 6], [6]),
}
CLAIMS = [
    (ORIGINAL, 'REMA08-01', [SHAPE, DATA], [AUTHOR],
     '개발 연구는 초기 236개 채점 항목 가운데 199개를 유지했고, 도형 과제 4개에서 채점 항목 104개가 나왔다고 설명했다. 변의 길이가 비슷한 평행사변형 문항을 뺀 이유도 실제 설명과 함께 기록했다.',
     '학생에게 제시한 과제 수와 채점 항목 수를 구별한다. 시각적 구분이 어려운 제시 방식의 영향을 도형 개념 오류로만 해석하지 않는다.'),
    (SHORT, 'REMASF-01', [DATA, SHAPE], [4, 6, f'{KINDER["url"]}#page=103'],
     'REMA-SF는 80문항과 133개 채점 지표로 기술됐다. 학년별로 시작점을 정하고, 연속 세 문항 정답으로 기초 수준을 확인하며 연속 세 문항 오답에 중단한다. 일부 어려운 문항은 도달자가 적었다.',
     '문항 미제시, 실제 오답, 부분 정답을 따로 기록한다. MPC REMA-K 48문항의 정확한 중단 횟수는 확인되지 않았다.'),
    (SHORT, 'REMASF-02', [ADD, SUB], [4],
     '단축형은 정답 여부를 기록하고 일부 문항에는 부분 점수를 사용한다. 덧셈에서는 같은 정답을 내더라도 어느 수부터 이어 셌는지 등 관찰된 전략을 따로 부호화했다.',
     '정답만으로 풀이를 복원하지 않는다. 덧셈에서 관찰한 전략을 뺄셈 수행으로 일반화하지 않는다.'),
    (SHORT, 'REMASF-03', [DATA], [5, 6, 8],
     '개발 분석은 1,912개 관측을 사용했고 관측 시점이 여섯 개였다. 별도 표본은 유치원 101명과 1학년 80명이며, 개인 측정치의 신뢰도는 개발 표본 .93, 별도 표본 .90이었다.',
     '반복 측정 관측 수를 고유 학생 수로 읽지 않는다. 신뢰도 수치는 해당 표본과 점수에 관한 것이며 자체 과제의 타당성 검증이 아니다.'),
    (SHORT, 'REMASF-04', [DATA, TEST], [8, 10, 11, 12, 13],
     '두 판본의 점수 대조에서 정제한 공통 문항 29개를 사용했다. 논문의 근사 변환은 단축형 로짓에 .32를 더한다. 그림 3의 두 축에 REMA-SF가 인쇄됐으나 그림 설명과 표 1은 두 판본을 비교한다.',
     '변환을 이 두 판본의 로짓 범위로 한정한다. 원점수나 MPC REMA-K에는 적용하지 않는다. 집단별 동등화 불변성은 별도 검증 항목이다.'),
    (TRIAD, 'REMAT-01', [DATA, SHAPE], [6],
     'TRIAD 재분석은 225문항 REMA를 수와 도형 영역 각각 연속 네 문항 오답에서 중단했다. 1학년 시작점은 수 30번과 도형 6번이었다.',
     '시행 규칙은 연구와 판본에 귀속한다. 어떤 아동이 받은 문항 수를 검사의 전체 문항 수와 구별한다.'),
    (TRIAD, 'REMAT-02', [DATA], [5, 6],
     'TRIAD 재분석은 취학 전부터 1학년까지 REMA를, 4~5학년 시점에는 TEAM 3–5를 사용했다. 연구는 시점 간 비교에 문항 반응 모형의 척도화를 적용했다.',
     '시점별 검사 내용과 척도화 절차를 확인한다. 서로 다른 검사 원점수를 직접 빼거나 같은 코호트를 새 실험으로 센 근거로 쓰지 않는다.'),
]
OBSERVATIONS = {
    ORIGINAL: [dict(id='REMA08-P1', standard_codes=[SHAPE, DATA],
        question='네 번의 도형 분류 활동에서 활동마다 응답 표시를 5개씩 기록했다. 활동 수와 기록 수를 각각 구하고, 변 길이 비교가 어려웠을 때 어떤 정보를 더 남길지 설명하라.',
        expected='활동은 4개, 기록은 20개다. 아동이 실제로 한 분류와 설명, 그림에서 길이를 구별했는지, 도구를 제시했는지를 각각 기록한다.',
        interpretation='활동·채점 항목의 단위와 제시 방식이 응답 해석에 미치는 영향을 구별한다.', student_validated=False)],
    SHORT: [
        dict(id='REMASF-P1', standard_codes=[DATA],
            question='연속 오답 3개에서 멈추는 가상 검사에서 1~4번은 정답·오답·오답·오답이고, 5~6번은 제시하지 않았다. 관찰한 오답과 미제시 문항을 세어라.',
            expected='오답 3개와 미제시 2개다. 제시된 문항은 4개이고 전체는 6개다.',
            interpretation='중단 규칙을 적용하고 미제시를 실제 오답과 구별하는지 확인한다.', student_validated=False),
        dict(id='REMASF-P2', standard_codes=[ADD, SUB],
            question='7+5를 구할 때 두 학생이 모두 12라고 답했다. 한 학생은 두 묶음을 합쳐 1부터 모두 셌고, 다른 학생은 7에서 이어 셌다. 정답과 풀이를 따로 기록하고 12−5도 설명하도록 요청하라.',
            expected='덧셈 정답은 같고 첫 전략은 모두 세기, 둘째는 이어 세기다. 뺄셈은 7이며 아동이 실제로 설명한 방법을 추가로 기록한다.',
            interpretation='정답, 시작 수, 더 센 횟수, 뺄셈의 독립 수행을 구별한다.', student_validated=False),
        dict(id='REMASF-P3', standard_codes=[DATA, TEST],
            question='두 가상 검사 형태의 로짓 척도를 연결하는 식이 x′=x+.32일 때 x=−.12를 바꾸어라. 원점수 14점과 다른 판본 로짓에도 같은 식을 쓰는지 설명하라.',
            expected='연결한 두 형태에서 변환값은 .20이다. 원점수 또는 다른 형태의 로짓에는 해당 변환의 적용 근거가 필요하다.',
            interpretation='원점수·로짓·동등화 범위를 구별한다.', student_validated=False),
    ],
    TRIAD: [dict(id='REMAT-P1', standard_codes=[DATA, SHAPE],
        question='수와 도형 영역을 각각 시행하는 가상 검사에서 수 영역이 먼저 중단됐다. 도형 응답은 아직 없다. 이를 도형 오답으로 기록해도 되는지 설명하라.',
        expected='수 영역의 중단만 확인됐다. 도형은 실제 제시 여부를 확인하고, 제시하지 않았다면 미제시로 남긴다.',
        interpretation='영역별 시행·중단·응답 상태를 확인한다.', student_validated=False)],
}


def provenance(sid):
    if sid == ORIGINAL:
        scope = dict(url=AUTHOR, uploaded_by='Douglas H. Clements', article_pdf_obtained=False,
            article_printed_pages=[457, 482], selected_sections=[
                dict(section='채점 범주와 항목 제거', printed_pages=[461, 465]),
                dict(section='보존 항목과 적합성 요약', printed_pages=[477, 478])])
        return dict(source_asset_kind='author_web_text', author_text_review=scope), dict(original_page_layout_review=False)
    stem, url, fingerprint, total, pages, visuals = PDFS[sid]
    images = inspect_pdf(stem, fingerprint, total, pages, visuals)
    return dict(source_asset_kind='pdf', source_pdf_sha256=fingerprint), dict(source_pdf_url=url, pdf_pages=total,
        selected_text_pages=pages, visual_pdf_pages=visuals, rendered_page_sha256=images)


def main():
    registry = load_registry()
    if all(sid in registry['sources'] for sid in SOURCES):
        build_report()
        return
    assert not set(SOURCES).intersection(registry['sources'])
    assert 236 - 37 == 199 and 101 + 80 == 181
    assert Decimal('.58') - Decimal('.26') == Decimal('.32')
    details = {
        ORIGINAL: dict(initial_items=236, retained_items=199, geometry_tasks=4, geometry_indicators=104),
        SHORT: dict(items=80, scoring_indicators=133, basal_consecutive_correct=3, stop_consecutive_errors=3,
            development_observations=1912, external_students=[101, 80], person_reliability=[.93, .90],
            refined_anchors=29, short_anchor_mean=.26, full_anchor_mean=.58, short_to_full_logit_addition=.32,
            figure_3_printed_axis_labels=['REMA-SF', 'REMA-SF'], table_1_form_labels=['REMA-SF', 'REMA-Full'],
            mpc_rema_k_stop_rule_verified=False, subgroup_equating_invariance_verified=False),
        TRIAD: dict(rema_items=225, stop_consecutive_errors_by_section=4, grade_one_start={'number': 30, 'geometry': 6},
                    later_measure='TEAM 3–5', existing_cohort_source='CLEMENTS_ET_AL_2013_TRIAD_FOLLOWTHROUGH'),
    }
    assets = {sid: provenance(sid) for sid in SOURCES}
    bibliography = load(ROOT / 'data/sources.json')
    queue = load(ROOT / 'data/content_review_queue.json')
    assert not set(SOURCES).intersection(row['id'] for row in bibliography)
    assert not set(SOURCES).intersection(row['source']['id'] for row in queue['literature_review'])
    for sid, spec in SOURCES.items():
        asset, scope = assets[sid]
        doi = 'https://doi.org/' + spec['doi']
        note = f'data/literature_evidence/{sid}_review_notes.json'
        empirical = dict(design=spec['design'], sample_description=spec['sample'], inference_limit=spec['limit'],
                         student_outcome_study=True, causal_effect_established=False, local_effect_tested=False)
        entry = dict(id=sid, year=spec['year'], url=doi, title=spec['title'], authors=spec['authors'], kind='초기 수학 평가 검토',
            review_scope=spec['scope'], does_not_establish=spec['limit'], supports=spec['supports'],
            next_review='판본별 시행과 채점 자료 및 우리말 적용 범위를 확인한다.')
        bibliography.append(entry)
        correction = ('그림 3의 두 축에 REMA-SF가 인쇄됐다. 축 방향을 확정하지 않고 표 1과 본문에서 두 판본을 대조한다.'
                      if sid == SHORT else '이 출처의 문항·채점·검사 시행 범위를 다른 판본과 구별한다.')
        write(ROOT / note, dict(source_id=sid, source_url=doi, date=DATE, reviewer='Codex', read_scope=spec['scope'],
            contains_source_full_text=False, source_pdf_redistributed=False, empirical_scope=empirical,
            reading_log=[spec['scope']], source_corrections=[dict(location='측정과 시행', issue=correction)],
            form_review=details[sid], **asset, **scope))
        registry['sources'][sid] = dict(source_id=sid, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
            snapshot_kind='authored_review_notes', snapshot_file=note, snapshot_sha256=sha(ROOT / note),
            redistribution_license='workspace_authored_notes', bibliography_snapshot=digest(entry),
            display=dict(title=entry['title'], url=doi, authors_year=f'{spec["authors"][0].split()[-1]} 외, {spec["year"]}'),
            read_scope=spec['scope'], limits=spec['limit'], empirical_scope=empirical, scope_note='판본과 시행 조건을 기록한다.',
            method_note='원논문의 확인 범위 안에서 검사 양식과 채점·분석 단위를 대조했다.',
            editorial_action='검사 양식의 근거와 자체 관찰 과제를 반영했다.',
            independent_review=False, student_validated=False, observations=OBSERVATIONS[sid], **asset)
        queue['literature_review'].append(dict(source=entry, status='self_read_claim_mapping',
            evidence_file='data/literature_claim_reviews.json', claim_evidence_fields=spec['supports'],
            claim_ids=[cid for src, cid, *_ in CLAIMS if src == sid]))

    new = {}
    for sid, cid, codes, refs, support, limit in CLAIMS:
        locations = [f'{PDFS[sid][1]}#page={p}' if isinstance(p, int) else p for p in refs]
        new[cid] = dict(id=cid, source_id=sid, role='empirical_result_with_scope',
            empirical_scope=registry['sources'][sid]['empirical_scope'], standard_codes=codes,
            locations=locations, support=support, does_not_establish=limit, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes})
    registry['claims'].extend(new.values())
    relations = load(ROOT / 'data/revised_relations.json')['relations']
    pairs = {(r['id'], cid) for r in relations for cid, claim in new.items()
             if all(r[k].startswith('standard:') for k in ('from', 'to'))
             and {r[k][9:] for k in ('from', 'to')} <= set(claim['standard_codes'])}
    relation_id, claim_id = 'REV-2수01-06-2', 'REMASF-02'
    assert pairs == {(relation_id, claim_id)}
    relation = next(r for r in relations if r['id'] == relation_id)
    reviewed = load(ROOT / FILE)
    reviewed['records'].append(dict(relation_id=relation_id, claim_id=claim_id, role='activity_context',
        finding='덧셈의 정답과 시작 수·이어 세기를 따로 관찰하고, 뺄셈에서는 별도의 풀이 설명을 받는다.',
        limit='덧셈 전략 관찰을 뺄셈 전략의 증거나 두 기준의 필수 순서로 사용하지 않는다.',
        relation_snapshot=relation_snapshot(relation), claim_snapshot=claim_snapshot(new[claim_id], registry['sources'][SHORT])))
    apply_literature_context(relations, registry, registry=reviewed)
    write(ROOT / 'data/sources.json', bibliography)
    write(ROOT / 'data/content_review_queue.json', queue)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(ROOT / FILE, reviewed)
    build_report()
    print('REMA form crosscheck: 3 sources, 7 claims, 5 tasks, 1 relation entry')


if __name__ == '__main__':
    main()

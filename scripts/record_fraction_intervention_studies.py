"""Register the two original studies linked from LT2 fraction activities."""
from collections import Counter

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value


DATE = '2026-11-09'
CACHE = ROOT / 'tmp/literature/lt2-fractions-activities'
HAMDAN = 'HAMDAN_GUNDERSON_2017'
BOYER = 'BOYER_LEVINE_2015'
STUDIES = [
    dict(id=HAMDAN, stem='hamdan-gunderson', year=2017,
         title='The Number Line Is a Critical Spatial-Numerical Representation: Evidence From a Fraction Intervention',
         authors=['Noora Hamdan', 'Elizabeth A. Gunderson'], display='Hamdan·Gunderson, 2017',
         pdf_hash='4da7b9fbf2d395e0bb280270498dacbf81e8b0a1f4593c82ce31a5cca4bea292',
         scope='인쇄 588~594쪽의 방법·결과와 그림 1~5·표 1~2를 대조하고 공식 부록의 두 표, 수직선·원 훈련 절차와 넓이 채점 화면을 확인했다.',
         scope_note='수직선과 원 모형이 같은 분수를 다루되 표식의 의미가 다르다. 훈련 직후의 분수 크기 비교를 각 모형에서 훈련한 과제와 구별한다.',
         limits='한 도시의 초등 2·3학년에게 약 15분간 훈련했다. 장기 유지, 전체 분수 연산, 모든 수직선 및 국내 수업 효과는 후속 범위다.',
         empirical=dict(design='classroom_stratified_randomized_pretest_posttest',
                        sample_description='초등 2·3학년 114명을 학급 안에서 수직선 39명, 원 모형 37명, 낱말 퍼즐 38명에 배정했다.',
                        inference_limit='정해진 재료와 훈련 직후의 수행에 한정한다. 조건 간 보정 비교와 집단 안 사전·사후 비교는 서로 다른 검정이다.',
                        student_outcome_study=True, local_effect_tested=False),
         mappings=[
             ('HG01', 'empirical_result_with_scope', ['4수01-11','6수01-07'], [6, 7, 8],
              '훈련 직후 분수 크기 비교의 보정 정답률은 수직선 44.8%, 원 모형 38.7%, 낱말 퍼즐 40.9%였다.',
              '집단 간 보정 비교에서 수직선과 원의 p는 .002, 수직선과 퍼즐의 p는 .045였다. 수직선 집단 안의 보정하지 않은 사전·사후 비교 p=.086과 구별한다.'),
             ('HG02', 'related_theoretical_context', ['4수01-09','4수01-10','4수01-11'], [3, 4, 5],
              '수직선은 0에서 시작해 분모만큼 등분하고 분자만큼 칠한 구간의 끝점에 분수를 놓는다. 원에서는 색칠한 영역을 가리킨다.',
              '실험은 가느다란 직사각형 수직선을 사용했다. 특정 절차를 모든 모형과 모든 분수 문항의 우위로 확대하지 않는다.'),
         ],
         observation=dict(id='HG-P1', standard_codes=['4수01-09','4수01-10','4수01-11'],
             question='같은 분수 3/4을 0에서 1까지의 수직선과 원에 각각 나타내라. 수직선에서 분수를 적는 위치와 원에서 가리키는 부분은 무엇인가?',
             expected='수직선은 0~1을 네 등분하고 0에서 세 간격 떨어진 점에 적는다. 원은 넓이가 같은 네 부분 중 세 부분을 가리킨다.',
             interpretation='간격과 끝점, 원의 영역을 구별하고 표시하기 전후에 무엇을 근거로 삼았는지 기록한다.', student_validated=False)),
    dict(id=BOYER, stem='boyer-levine', year=2015,
         title='Prompting Children to Reason Proportionally: Processing Discrete Units as Continuous Amounts',
         authors=['Ty W. Boyer', 'Susan C. Levine'], display='Boyer·Levine, 2015',
         pdf_hash='9c640079bd52c35bf6a88af15b077525076310244ba473cc7a6b0ca2bc5d2591',
         scope='인쇄 616~619쪽의 방법·결과와 논의를 읽고 그림 1·2 및 검정 표기가 있는 PDF 2·3·4쪽을 이미지로 확인했다.',
         scope_note='주스의 절대량이 같은 선택지와 전체에서 차지하는 비율이 같은 선택지를 구별하는 과제를 검토했다.',
         limits='같은 시간에 이어진 구획 비교 문항과 보고된 학년 차이에 한정한다. 선택지는 1/2을 제외했고 오답은 기준과 1/2의 반대쪽이었다.',
         empirical=dict(design='classroom_randomized_presentation_order',
                        sample_description='여섯 학교의 유치원 64명·2학년 66명·4학년 64명이 연속량 8문항 뒤 구획 8문항 또는 구획 16문항 조건에 배정됐다.',
                        inference_limit='직접 가르치거나 정답을 알려 준 처치가 아니다. 후반 조건 차이를 다른 학년, 더 근접한 비율 또는 장기 성취로 일반화하지 않는다.',
                        student_outcome_study=True, local_effect_tested=False),
         mappings=[
             ('BL01', 'empirical_result_with_scope', ['6수02-02','6수02-04'], [3, 4],
              '두 조건이 공통으로 본 후반 구획 문항에서 4학년의 그림상 평균은 연속량 먼저 .80, 구획만 .64였고 보고된 p는 .03이다.',
              '유치원과 2학년에서는 같은 조건 차이가 보고되지 않았다. 같은 수업의 장기 효과를 측정한 비교가 아니다.'),
             ('BL02', 'related_theoretical_context', ['6수02-02','6수02-03','6수02-04'], [2, 3, 5],
              '주스 4/전체 10과 주스 2/전체 5는 주스의 절대량은 달라도 전체에서 차지하는 비율이 같다. 주스 대 물은 두 경우 모두 2:3이다.',
              '주스의 절대량이나 혼합물 전체량 하나만으로 같은 비를 판단하지 않는다. 활동용 정답표와 연구의 선택지를 별도로 대조한다.'),
         ],
         observation=dict(id='BL-P1', standard_codes=['6수02-02','6수02-03','6수02-04'],
             question='주스 4컵과 물 6컵을 섞었다. 가는 주스 2컵과 물 3컵, 나는 주스 4컵과 물 3컵이다. 같은 비의 혼합물을 고르고 각각 주스가 전체에서 차지하는 비율을 말하라.',
             expected='기준은 4/10이고 가는 2/5라서 같은 비다. 나는 4/7이라 다르다. 주스의 절대량이 같아도 주스가 전체에서 차지하는 비율은 달라질 수 있다.',
             interpretation='눈금이 없는 그림에서 처음 한 선택과, 수량을 표시한 뒤 비를 비교해 확인한 설명을 나누어 적는다.', student_validated=False)),
]


def notes_file(source_id):
    return f'data/literature_evidence/{source_id}_review_notes.json'


def verify_evidence(study, evidence):
    stem = study['stem']
    assert evidence['source_pdf_sha256'] == sha(CACHE / f"{stem}-{study['year']}.pdf") == study['pdf_hash']
    for page, page_hash in evidence['checked_render_hashes'].items():
        filename = f'{stem}-{int(page):02}.png' if study['id'] == HAMDAN else f'{stem}-{page}.png'
        assert sha(CACHE / filename) == page_hash
    participants = evidence['participants']
    if study['id'] == BOYER:
        assert sum(participants[k] for k in ('kindergarten','grade_two','grade_four')) == participants['total'] == 194
        f = evidence['discrepancy']
        assert f['reported_df'] == [1, 187]
        assert round(f['computed_with_numerator_df_two'], 3) == f['reported_partial_eta2']
        assert round(f['computed_given_reported_df'], 3) != f['reported_partial_eta2']
        return {}, [f]
    assert sum(participants[k] for k in ('line','area','crossword')) == participants['total'] == 114
    supplement = evidence['supplemental']
    assert supplement['sha256'] == sha(CACHE / 'hamdan-gunderson-supplement.docx')
    text = (CACHE / 'hamdan-gunderson-supplement.txt').read_text(encoding='utf-8')
    rows = [line.split(' | ')[1:] for line in text.splitlines() if ' versus ' in line and ' | ' in line]
    assert Counter(x[0] for x in rows) == {'Consistent': 6, 'Inconsistent': 10, 'Ambiguous': 4}
    assert Counter(x[1] for x in rows) == {'Trained': 10, 'Untrained': 10}
    assert all(t in text for t in ('Trained (6 items)', 'Untrained (8 items)', 'starting from zero', 'Area Model Scoring Instructions'))
    supplemental = dict(supplement, content_reviewed=True, reading_scope='표 A·B와 수직선·원 절차, 넓이 채점 절차 및 수록 화면',
                        comparison_items=dict(consistent=6, inconsistent=10, ambiguous=4, trained_fractions=10, other_fractions=10),
                        estimation_items=dict(trained=6, untrained=8), redistributed=False,
                        screen_review_sha256=sha(CACHE / 'hamdan-supplement-figures.png'))
    return supplemental, []


def main():
    registry = load_registry()
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    for study in STUDIES:
        sid = study['id']
        observation = study['observation']
        notes_path = notes_file(sid)
        if sid in registry['sources']:
            current = registry['sources'][sid]
            assert current['snapshot_sha256'] == sha(ROOT / notes_path) and current['observations'] == [observation]
            continue
        evidence = load(CACHE / (study['stem'] + '-preliminary-review.json'))
        supplemental, corrections = verify_evidence(study, evidence)
        url, pdf_url = evidence['source_url'], evidence['source_pdf_url']
        empirical = study['empirical']
        entry = dict(id=sid, title=study['title'], authors=study['authors'], year=study['year'], kind='무작위 배정 실험 연구',
                     url=url, review_scope=study['scope'], next_review=study['limits'],
                     supports=[study['scope_note']], does_not_establish=study['limits'])
        bibliography.append(entry)
        notes = dict(source_id=sid, source_url=url, source_pdf_url=pdf_url, source_pdf_sha256=study['pdf_hash'],
                     source_asset_kind='pdf', date=DATE, reviewer='Codex', read_scope=study['scope'],
                     contains_source_full_text=False, source_pdf_redistributed=False,
                     pdf_pages=evidence['pdf_pages'], printed_pages=evidence['print_pages'],
                     text_pdf_pages=evidence['reviewed_method_and_result_pdf_pages'],
                     visual_pdf_pages=sorted(map(int,evidence['checked_render_hashes'])),
                     visual_pdf_page_hashes=evidence['checked_render_hashes'], empirical_scope=empirical,
                     participants=evidence['participants'], source_corrections=corrections,
                     supplemental=supplemental, reading_log=evidence['scope_notes'])
        write(ROOT / notes_path, notes)
        registry['sources'][sid] = dict(source_id=sid, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
            snapshot_kind='authored_review_notes', source_asset_kind='pdf', snapshot_file=notes_path,
            snapshot_sha256=sha(ROOT / notes_path), source_pdf_sha256=study['pdf_hash'],
            redistribution_license='workspace_authored_notes', bibliography_snapshot=digest(entry),
            display=dict(title=entry['title'], url=url, authors_year=study['display']),
            read_scope=study['scope'], scope_note=study['scope_note'], empirical_scope=empirical, limits=study['limits'],
            method_note='분수 활동 안내와 분리해 원연구의 실험 조건, 사용 문항과 보고 결과를 대조했다.',
            editorial_action='원연구 근거 2건과 관찰 과제 1개를 추가했다.',
            independent_review=False, student_validated=False, observations=[observation])
        for cid, role, codes, pages, support, limit in study['mappings']:
            claim = dict(id=cid, source_id=sid, role=role, standard_codes=codes,
                locations=[f'{pdf_url}#page={page}' for page in pages], support=support, does_not_establish=limit,
                independent_review=False, student_validated=False,
                target_snapshots={'revision:'+code:digest(target_value('revision:'+code)) for code in codes})
            if role == 'empirical_result_with_scope':
                claim['empirical_scope'] = empirical
            registry['claims'].append(claim)
        queue['literature_review'].append(dict(source=entry, status='self_read_claim_mapping',
            claim_evidence_fields=['참가자와 실험 조건','측정과 비교 결과','적용 한계'],
            evidence_file='data/literature_claim_reviews.json', claim_ids=[row[0] for row in study['mappings']]))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()


if __name__ == '__main__':
    main()

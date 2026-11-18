"""Register the longitudinal puzzle-play study cited by LT2."""
from math import sqrt

from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value


SOURCE = 'LEVINE_RATLIFF_HUTTENLOCHER_CANNON_2012'
DATE = '2026-11-09'
URL = 'https://doi.org/10.1037/a0025913'
PDF_URL = 'https://cpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/5/1727/files/2019/06/Levine-Ratliff-Early-Puzzle-Play.pdf'
PDF_SHA = '66e4efe9dfa1988b16aac5e310a378fe808a6813c680f22b9f43d149537d6b12'
LT2_URL = 'https://www.learningtrajectories.org/math-activities/putting-the-pieces-together-simple-turner'
CACHE = ROOT / 'tmp/literature/levine-2012-puzzle-play'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
READ_SCOPE = '인쇄 530~542쪽의 본문과 부록 및 참고문헌 목록을 대조했다. PDF 4·6~10·13쪽의 그림 1~3, 표 1~6과 사례를 실제 이미지에서 확인했다.'
LIMITS = '가정 방문 때 관찰한 놀이와 이후 점수의 관련이다. 방문 밖의 놀이, 이미 형성된 공간 능력, 교실 활동의 인과 효과 및 한국어 과제 타당성은 확인하지 않았다.'
EMPIRICAL_SCOPE = dict(
    design='naturalistic_longitudinal_home_observation',
    sample_description='64가정 중 방문 여섯 번의 자료와 54개월 과제가 모두 있는 53가정을 분석했다. 방문 중 퍼즐 놀이가 관찰된 아동은 27명이다.',
    inference_limit=LIMITS, student_outcome_study=True, causal_effect_established=False, local_effect_tested=False,
)
MAPPINGS = [
    ('LRP01', ['4수03-04'], [3,4,6,7,8,10],
     '26~46개월에 각 90분씩 여섯 차례 자연스러운 가정 활동을 관찰했다. 방문 중 퍼즐 놀이가 관찰된 27명은 관찰되지 않은 26명보다 54개월의 평면 조각 변환 과제 점수가 높았다. 분석에서는 보호자의 어휘 유형 수, 소득과 학력을 보정했다.',
     '가정에서 놀이를 무작위 배정하지 않았다. 관찰되지 않은 26명이 평소에 퍼즐을 하지 않았다고 단정할 수 없으며 기존 공간 능력이나 다른 경험의 영향을 배제하지 못한다.'),
    ('LRP02', ['2수03-03','4수03-04','6수03-01'], [3,4,5,8,9,10,13],
     '가정 놀이에서는 조각마다 정확한 위치가 하나인 퍼즐을 코딩했고, 이후 과제는 조각을 움직이지 않고 네 보기에서 고르는 10문항이었다. 부록 사례에서는 아동이 조각을 놓았어도 어른이 모서리나 직선 경계를 직접 알려 준 경우가 있다.',
     '여러 배치가 가능한 탱그램 활동이나 조각을 직접 맞추는 능력 전체에 결과를 확대하지 않는다. 부모 참여·퍼즐 난이도·공간말의 합성 지표로 공간말만의 효과를 분리할 수 없다.'),
]
OBSERVATION = dict(
    id='LRP-P1', standard_codes=['2수03-03','4수03-04','6수03-01'],
    question='정사각형 퍼즐 조각의 위쪽 변에 점을 찍어 놓았다. 조각을 시계 방향으로 90° 돌리면 점이 어느 쪽 변에 오겠는가? 조각을 먼저 돌리지 말고 말하거나 가리킨 뒤 실제로 확인한다.',
    expected='중심을 기준으로 시계 방향으로 90° 돌리면 원래 위쪽 변이 오른쪽 변으로 간다. 정사각형의 전체 외곽은 그대로 포개지지만 점의 위치는 바뀐다.',
    interpretation='처음 예상, 경계나 방향을 알려 준 뒤의 반응, 실제 조작 후 확인을 구별한다. 한 번의 정답을 공간 능력의 종합 점수로 해석하지 않는다.',
    student_validated=False,
)


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert registry['sources'][SOURCE]['snapshot_sha256'] == sha(ROOT / NOTES)
        assert registry['sources'][SOURCE]['observations'] == [OBSERVATION]
        build_report()
        return
    pdf = CACHE / 'published-author-lab.pdf'
    assert sha(pdf) == PDF_SHA and len(PdfReader(pdf).pages) == 13
    body = pdf.with_suffix('.txt').read_text(encoding='utf-8')
    assert all(marker in body for marker in ('10.1037/a0025913', '27 out of 53', '2.94', '1.88', '1.62'))
    visual_pages = [4,6,7,8,9,10,13]
    max_session_sd = sqrt(27/26) * (6-1)/2
    assert max_session_sd < 2.55 < 2.94
    notes = dict(
        source_id=SOURCE, source_url=URL, source_pdf_url=PDF_URL, source_pdf_sha256=PDF_SHA,
        date=DATE, reviewer='Codex', read_scope=READ_SCOPE, contains_source_full_text=False,
        source_pdf_redistributed=False, publication='Developmental Psychology, 48(2), 530–542',
        pdf_pages=13, printed_pages=[530,542], text_pdf_pages=list(range(1,14)), visual_pdf_pages=visual_pages,
        visual_pdf_page_hashes={str(p):sha(CACHE / f'page-{p:02d}.png') for p in visual_pages},
        linking_lt2_pages=[LT2_URL], empirical_scope=EMPIRICAL_SCOPE,
        reading_log=[
            'PDF 1~3쪽에서 연구 질문과 직접 가정 관찰, 분석 표본의 선정, 이후 네 보기 과제의 변환 조건을 확인했다.',
            'PDF 4~5쪽에서 방문 일정, 고유한 조각 자리, 시작·종료 코딩, 보호자와 아동의 공간말 및 채점자 일치를 확인했다. 단축 과제의 보정 반분 신뢰도는 .55다.',
            'PDF 6~9쪽의 표 1~6과 그림 2~3에서 전체 비교와 퍼즐 놀이를 한 27명의 빈도·합성 품질 분석을 구별했다.',
            'PDF 10~13쪽에서 교란 가능성과 인과 검증의 필요성, 참고문헌 목록, 직소와 꼭지 퍼즐에서 부모 도움의 네 사례를 확인했다.',
        ],
        source_corrections=[
            dict(location='PDF 3~4 / 인쇄 532~533 / 그림 1',issue='그림 1의 D가 대각 평행이동으로 적혔지만 그림과 방법은 대각 이동 및 회전을 보여 준다.',status='caption_and_method_conflict'),
            dict(location='PDF 6 / 인쇄 535 / 방문 중 놀이 빈도',issue='최대 여섯 방문 중 한 번 이상 관찰된 27명의 방문 횟수에 SD 2.94를 인쇄했다. 1~6의 값이면 표본 SD 상한은 2.55 미만이다.',max_sample_sd_bound=max_session_sd,status='printed_value_held_pending_original_data_or_erratum'),
            dict(location='PDF 8~9 / 인쇄 537~538 / 표 4와 표 5',issue='여아의 퍼즐당 공간말 평균이 표 4에서는 1.88, 표 5에서는 1.62다.',status='reported_values_differ'),
        ],
    )
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = dict(
        id=SOURCE,title='Early Puzzle Play: A Predictor of Preschoolers’ Spatial Transformation Skill',
        authors=['Susan C. Levine','Kristin R. Ratliff','Janellen Huttenlocher','Joanna Cannon'],
        year=2012,kind='퍼즐 놀이의 종단 관찰 연구',url=URL,review_scope=READ_SCOPE,next_review=LIMITS,
        supports=['관찰한 놀이와 후속 과제의 관련','예상·조작·성인 도움의 구별'],
        does_not_establish='퍼즐의 인과 효과 또는 국내 수업 및 진단의 타당성',
    )
    assert all(row['id'] != SOURCE for row in bibliography)
    bibliography.append(entry)
    path = ROOT / NOTES
    write(path, notes)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date=DATE,
        snapshot_kind='authored_review_notes',source_asset_kind='pdf',snapshot_file=NOTES,
        snapshot_sha256=sha(path),source_pdf_sha256=PDF_SHA,redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry),display=dict(title=entry['title'],url=URL,authors_year='Levine 외, 2012'),
        read_scope=READ_SCOPE,empirical_scope=EMPIRICAL_SCOPE,limits=LIMITS,
        scope_note='가정 놀이 관찰과 네 보기 정신적 변환 과제의 조건을 구별한다.',
        method_note='LT2의 인용 설명을 원문 방법·표·과제 그림과 대조했다.',
        editorial_action='문헌 대응 2건과 자체 관찰 과제 1개를 추가했다.',
        independent_review=False,student_validated=False,observations=[OBSERVATION],
    )
    for cid,codes,pages,support,limit in MAPPINGS:
        registry['claims'].append(dict(
            id=cid,source_id=SOURCE,role='empirical_result_with_scope',standard_codes=codes,
            locations=[f'{PDF_URL}#page={p}' for p in pages],support=support,does_not_establish=limit,
            independent_review=False,student_validated=False,empirical_scope=EMPIRICAL_SCOPE,
            target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    queue['literature_review'].append(dict(
        source=entry,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',
        claim_evidence_fields=['방문 중 놀이와 미관찰','후속 과제','보정과 적용 한계'],
        claim_ids=[row[0] for row in MAPPINGS],
    ))
    write(bibliography_path,bibliography)
    write(ROOT / 'data/literature_claim_reviews.json',registry)
    write(queue_path,queue)
    build_report()
    print('Registered the puzzle-play study with two claims and one observation.')


if __name__ == '__main__':
    main()

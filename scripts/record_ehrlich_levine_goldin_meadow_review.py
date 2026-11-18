"""Register the spatial-transformation experiment cited by LT2."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value


SOURCE = 'EHRLICH_LEVINE_GOLDIN_MEADOW_2006'
DATE = '2026-11-09'
URL = 'https://doi.org/10.1037/0012-1649.42.6.1259'
PDF_URL = 'https://cpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/c/1286/files/2018/09/The-importance-of-gesture-in-childrens-spatial-reasoning-23clak2.pdf'
PDF_SHA = '7b7e063aab554c6c31c68a4b35f26e53e685a6ae507dd638c5f5cc09365521b2'
CACHE = ROOT / 'tmp/literature/lt2-composing-2d-studies'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
READ_SCOPE = '인쇄 1259~1268쪽의 본문과 참고문헌을 텍스트로 확인하고 PDF 1·3~8쪽의 과제 그림·표·결과를 이미지로 대조했다.'
SCOPE_NOTE = '네 보기에서 답을 고르는 정신적 변환과 조각을 손으로 맞추는 수업 과제를 분리한다. 답을 고른 뒤 말과 손짓으로 나타낸 설명을 구별한다.'
LIMITS = '짧은 연습과 두 지도 조건을 비교했다. 손짓을 가르치는 조건이나 LT2 활동의 수업 효과는 이 실험에서 직접 검증하지 않았다.'
EMPIRICAL_SCOPE = dict(
    design='randomized_conditions_matched_pretest_subset_and_postanswer_probe',
    sample_description='5세 유아 80명이 사전검사를 받았다. 사전 점수와 성별을 기준으로 세 조건에 걸쳐 대응시킨 63명을 사전·사후 및 설명 분석에 사용했다.',
    inference_limit='조각을 직접 만지지 않고 네 보기에서 고른다. 정답을 고른 뒤의 설명에서 손짓과 점수의 관련을 확인했으며 손짓 자체의 인과 효과는 검증하지 않았다.',
    student_outcome_study=True, causal_effect_established=False, local_effect_tested=False,
)
MAPPINGS = [
    ('ELG01', ['4수03-04', '4수03-12'], [3, 4, 5, 8],
     '두 조각의 평행이동 또는 회전을 예상해 네 보기에서 답을 골랐다. 움직임 상상, 실험자의 움직임 관찰, 연습의 세 조건을 비교했다. 대응 표본의 전체 평균은 62.72%에서 68.78%로 올랐다.',
     '두 지도 조건이 연습보다 전체적으로 더 효과적이라는 결과는 없었다. 조각을 직접 맞춘 수행과는 과제 조건이 다르다.'),
    ('ELG02', ['4수03-04', '6수03-01'], [4, 6, 7, 8],
     '정답 선택 뒤의 설명 8문항에서 움직임이 나타난 문항은 말만 코딩하면 평균 3.48개, 말 또는 손짓을 코딩하면 4.99개였다. 움직임 손짓과 이 문항들의 정답 점수 사이 상관은 r=0.299였다.',
     '답을 고른 뒤에 나온 설명이며 풀기 전의 전략을 직접 관찰한 자료는 아니다. 상관으로 손짓 지도의 효과를 판단하지 않는다.'),
]
OBSERVATION = dict(
    id='ELG-P1', standard_codes=['4수03-04', '4수03-12', '6수03-01'],
    question='한 변이 4 cm인 정사각형을 대각선으로 자른 두 조각의 그림이 있다. 맞댈 긴 변은 가로와 세로로 놓여 있다. 조각을 움직이기 전에 어떤 회전과 이동이 필요한지 말이나 손짓으로 나타낸다. 실제 조각으로 맞춰 본 뒤 설명을 비교한다.',
    expected='긴 변의 방향을 90° 돌려 나란히 하고 두 긴 변이 정확히 포개지도록 옮긴다. 두 직각 꼭짓점이 긴 변의 서로 반대쪽에 오도록 조각을 놓으면 정사각형이 된다.',
    interpretation='예상한 회전과 이동, 실제 조작, 조작 뒤 설명을 순서대로 기록한다. 사전 설명에서는 말과 손짓을 따로 기록한다.',
    student_validated=False,
)


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert registry['sources'][SOURCE]['snapshot_sha256'] == sha(ROOT / NOTES)
        assert registry['sources'][SOURCE]['observations'] == [OBSERVATION]
        build_report()
        return
    pdf = CACHE / 'ehrlich-lab-alt.pdf'
    assert sha(pdf) == PDF_SHA and len(PdfReader(pdf).pages) == 10
    body = (CACHE / 'ehrlich-lab-alt.txt').read_text(encoding='utf-8')
    assert all(marker in body for marker in ('Stacy B. Ehrlich', '62.72%', '68.78%', '4.99', '3.48', '.299'))
    visual_pages = [1, 3, 4, 5, 6, 7, 8]
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    assert all(row['id'] != SOURCE for row in bibliography)
    entry = dict(id=SOURCE, title='The Importance of Gesture in Children’s Spatial Reasoning',
                 authors=['Stacy B. Ehrlich', 'Susan C. Levine', 'Susan Goldin-Meadow'], year=2006,
                 kind='공간 변환 과제의 실험·설명 분석', url=URL, review_scope=READ_SCOPE, next_review=LIMITS,
                 supports=['보기 선택과 조작 과제의 구별', '답을 고른 뒤 말과 손짓의 별도 기록'],
                 does_not_establish='손짓 훈련의 인과 효과, LT2 과제 또는 국내 수업의 효과')
    bibliography.append(entry)
    notes = dict(source_id=SOURCE, source_url=URL, source_pdf_url=PDF_URL, source_pdf_sha256=PDF_SHA,
                 date=DATE, reviewer='Codex', read_scope=READ_SCOPE, contains_source_full_text=False,
                 source_pdf_redistributed=False, publication='Developmental Psychology, 42(6), 1259–1268',
                 pdf_pages=10, printed_pages=[1259, 1268], text_pdf_pages=list(range(1, 11)),
                 visual_pdf_pages=visual_pages,
                 visual_pdf_page_hashes={str(page): sha(CACHE / f'ehrlich-{page}.png') for page in visual_pages},
                 empirical_scope=EMPIRICAL_SCOPE, source_corrections=[],
                 reading_log=[
                     'PDF 1~3쪽에서 서지·연구 질문·80명의 참여자와 네 종류의 변환 과제를 확인했다. 그림 1은 조각 두 개와 선택지 네 개를 보여 준다.',
                     'PDF 4~5쪽에서 사전·사후 각각 16문항, 중간 연습 또는 지도 12문항, 사후 설명 8문항을 확인했다. 세 조건 배정 뒤 사전 점수로 맞춘 표본을 분석했다.',
                     'PDF 6~8쪽의 설명 분석과 논의에서 말과 손짓의 코딩 범주, 이동 손짓의 상관, 별도 손짓 지도 조건이 없었다는 한계를 확인했다.',
                     'PDF 9~10쪽에서 후속 연구 제안과 참고문헌을 확인했다.',
                 ])
    path = ROOT / NOTES
    write(path, notes)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
        snapshot_kind='authored_review_notes', source_asset_kind='pdf', snapshot_file=NOTES,
        snapshot_sha256=sha(path), source_pdf_sha256=PDF_SHA, redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=URL, authors_year='Ehrlich·Levine·Goldin-Meadow, 2006'),
        read_scope=READ_SCOPE, scope_note=SCOPE_NOTE, empirical_scope=EMPIRICAL_SCOPE, limits=LIMITS,
        method_note='조각 맞추기 활동의 인용을 논문 그림과 실험 절차 및 결과에 대조했다.',
        editorial_action='연구 근거 2건과 예상·실제 조작·사후 설명을 구별하는 자체 관찰 과제 1개를 추가했다.',
        independent_review=False, student_validated=False, observations=[OBSERVATION],
    )
    for cid, codes, pages, support, limit in MAPPINGS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='empirical_result_with_scope', standard_codes=codes,
            locations=[f'{PDF_URL}#page={page}' for page in pages], support=support, does_not_establish=limit,
            independent_review=False, student_validated=False, empirical_scope=EMPIRICAL_SCOPE,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    queue['literature_review'].append(dict(
        source=entry, status='self_read_claim_mapping',
        claim_evidence_fields=['표본과 배정', '과제와 비교 조건', '말과 손짓의 코딩', '적용 한계'],
        evidence_file='data/literature_claim_reviews.json', claim_ids=[row[0] for row in MAPPINGS],
    ))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Registered the spatial-transformation study, 2 claims and 1 observation.')


if __name__ == '__main__':
    main()

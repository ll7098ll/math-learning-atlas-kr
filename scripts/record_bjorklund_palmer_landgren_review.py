"""Register the MADIF13 study cited by LT2's What Changed activity."""
from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value


SOURCE = 'BJORKLUND_PALMER_LANDGREN_2022'
DATE = '2026-11-09'
PDF_URL = 'https://matematikdidaktik.org/wp-content/uploads/2022/07/MADIF13_final.pdf'
URL = PDF_URL + '#page=21'
PDF_SHA = '2370cc1ac0977687d644d0cd0a654f25168d40b4f47a88e6342539a0265b6990'
CACHE = ROOT / 'tmp/literature/lt2-subitizing-activities'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
READ_SCOPE = '학술대회 자료의 PDF 21~31쪽, 인쇄 11~21쪽 논문 본문과 참고문헌을 읽었다. 그림·표·주석의 PDF 25·27·31쪽과 본문이 없는 구분 쪽 32쪽을 이미지로 확인했다.'
SCOPE_NOTE = '같은 놀이에서 물건 종류와 색, 개수 중 무엇에 주목했는지 분석했다. 아이가 수 이름을 말한 경우에도 어느 부분과 전체를 가리켰는지 관찰한다.'
LIMITS = '세 유아기관에서 자연스럽게 진행한 놀이를 분석했다. 반복 반응과 조건별 노출 차이가 있으며 조건 간 인과 효과, 국내 학생 진단 정확도, 학생별 발달 순서를 추정하지 않는다.'
EMPIRICAL_SCOPE = dict(
    design='naturalistic_observational_video_coding',
    sample_description='시작할 때 12~27개월인 유아 27명과 교사 3명이 참여한 179개 영상이다. 수 말과 손가락 표현을 비교한 세부 분석은 영상 14개를 대상으로 한다.',
    inference_limit='한 영상에서 여러 반응이 나올 수 있다. 표의 빈도는 반응 수에 한정하며 아동별 비율이나 고정된 발달 순서를 뜻하지 않는다.',
    student_outcome_study=True,
    causal_effect_established=False,
    local_effect_tested=False,
)
MAPPINGS = [
    ('BPL01', 'empirical_result_with_scope', ['2수01-01', '2수01-04', '2수01-05'],
     [PDF_URL + '#page=25', PDF_URL + '#page=26', PDF_URL + '#page=27'],
     '수 이름 또는 손가락을 쓴 반응은 다른 종류 1/65, 색만 다른 경우 16/74, 같은 물건 40/120으로 보고된다. 분모는 조건별 반응 건수다.',
     '동일 영상의 복수 반응과 조건별 노출 차이가 있다. 후속 분석 수는 인쇄 17쪽 본문과 인쇄 21쪽 주석을 함께 기록하며, 원자료 없이 수를 정정하지 않는다.'),
    ('BPL02', 'related_theoretical_context', ['2수01-01', '2수01-04', '2수01-05', '2수01-07'],
     [PDF_URL + '#page=28', PDF_URL + '#page=29', PDF_URL + '#page=30'],
     '물건의 이름, 현재 보이는 수, 가려진 수, 처음 전체 사이의 관계를 구별한다. 같은 수 이름도 어느 모임에 붙였는지 확인하며 말과 손가락 표현을 함께 기록할 수 있다.',
     '교사의 질문과 물건의 친숙함이 반응에 영향을 줄 수 있다. 한 번의 수 이름이나 정확한 답으로 부분과 전체의 관계 이해를 확정하지 않는다.'),
]
OBSERVATION = dict(
    id='BPL-P1', standard_codes=['2수01-04', '2수01-05', '2수01-07'],
    question='처음에 작은 곰 세 개가 있다. 한 개를 가리고 두 개를 보인다. 곰의 색이 서로 다른 경우와 모두 같은 경우에 각각 어느 곰이 없어졌는지, 몇 개가 가려졌는지, 몇 개가 보이는지 말하라.',
    expected='두 경우 모두 보이는 곰은 2개이고 가려진 곰은 1개다. 색이 서로 다르면 처음과 비교해 가려진 곰의 색을 말할 수 있다. 모두 같은 색이면 색으로 어떤 곰인지 구별할 수 없다. 2와 1을 합치면 처음의 3개가 된다.',
    interpretation='처음 물건과 남은 물건의 색·위치를 대조한 답과 수로 설명한 답을 따로 적는다. 교사가 처음 수를 알려 주거나 두 부분을 가리킨 뒤 답이 어떻게 달라졌는지 기록한다.',
    student_validated=False,
)


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert registry['sources'][SOURCE]['snapshot_sha256'] == sha(ROOT / NOTES)
        assert registry['sources'][SOURCE]['observations'] == [OBSERVATION]
        build_report()
        return
    evidence = load(CACHE / 'madif13-bjorklund-preliminary-review.json')
    assert evidence['source_url'] == PDF_URL and evidence['source_sha256'] == sha(CACHE / 'MADIF13_final.pdf') == PDF_SHA
    assert evidence['source_pdf_total_pages'] == 154 and evidence['article_print_pages'] == [11, 21]
    assert evidence['article_text_read_pdf_pages'] == list(range(21, 32))
    assert evidence['blank_separator_pdf_page'] == 32 and evidence['next_article_starts_pdf_page'] == 33
    renders = evidence['visually_checked_pages']
    assert [r['pdf_page'] for r in renders] == [25, 27, 31, 32]
    for r in renders:
        assert sha(CACHE / f"madif13-{r['pdf_page']:03}.png") == r['sha256']
    counts = evidence['table_1_response_counts']
    assert [sum(row[i] for key, row in counts.items() if key != 'totals') for i in range(3)] == counts['totals'] == [65, 74, 120]
    number_responses = counts['number_word_or_fingers']
    assert number_responses == [1, 16, 40] and sum(number_responses) == 57 and sum(number_responses[1:]) == 56
    assert [evidence['participants'][key] for key in ('toddlers', 'recordings', 'selected_recordings')] == [27, 179, 14]

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    assert all(row['id'] != SOURCE for row in bibliography)
    entry = dict(id=SOURCE, title='Who or how many are missing? Toddlers experiencing numerical meaning in a game',
                 authors=['Camilla Björklund', 'Hanna Palmér', 'Lena Landgren'], year=2022,
                 kind='유아 놀이 영상 관찰 학술대회 논문', url=URL, review_scope=READ_SCOPE, next_review=LIMITS,
                 supports=['수 이름과 개수의 관계', '숨긴 부분과 보이는 부분을 구별하는 관찰 설계'],
                 does_not_establish='국내 과제의 학생 검증, 조건별 인과 효과, 개인별 발달 경로')
    bibliography.append(entry)
    notes = dict(source_id=SOURCE, source_url=URL, source_pdf_url=PDF_URL, source_pdf_sha256=PDF_SHA,
                 source_asset_kind='pdf', date=DATE, reviewer='Codex', read_scope=READ_SCOPE,
                 contains_source_full_text=False, source_pdf_redistributed=False,
                 pdf_pages=154, printed_pages=[11, 21], bibliographic_extent_including_separator=[11, 22],
                 blank_separator_pdf_page=32, text_pdf_pages=evidence['article_text_read_pdf_pages'],
                 visual_pdf_pages=[r['pdf_page'] for r in renders],
                 visual_pdf_page_hashes={str(r['pdf_page']): r['sha256'] for r in renders}, empirical_scope=EMPIRICAL_SCOPE,
                 participants=evidence['participants'], conditions=evidence['condition_labels'], table_1_response_counts=counts,
                 source_corrections=evidence['source_discrepancies'], reading_log=evidence['scope_observations'])
    path = ROOT / NOTES
    write(path, notes)
    registry['sources'][SOURCE] = dict(source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
                                       snapshot_kind='authored_review_notes', source_asset_kind='pdf', snapshot_file=NOTES,
                                       snapshot_sha256=sha(path), source_pdf_sha256=PDF_SHA, redistribution_license='workspace_authored_notes',
                                       bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=URL, authors_year='Björklund·Palmér·Landgren, 2022'),
                                       read_scope=READ_SCOPE, scope_note=SCOPE_NOTE, empirical_scope=EMPIRICAL_SCOPE, limits=LIMITS,
                                       method_note='활동 안내와 분리해 세 가지 놀이 조건, 영상 선별, 복수 반응, 표와 주석을 대조했다.',
                                       editorial_action='연구 근거 2건과 가린 수·보이는 수·처음 수를 구별하는 자체 관찰 과제 1개를 추가했다.',
                                       independent_review=False, student_validated=False, observations=[OBSERVATION])
    for cid, role, codes, locations, support, limit in MAPPINGS:
        claim = dict(id=cid, source_id=SOURCE, role=role, standard_codes=codes, locations=locations,
                     support=support, does_not_establish=limit, independent_review=False, student_validated=False,
                     target_snapshots={'revision:' + code: digest(target_value('revision:' + code)) for code in codes})
        if role == 'empirical_result_with_scope':
            claim['empirical_scope'] = EMPIRICAL_SCOPE
        registry['claims'].append(claim)
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    queue['literature_review'].append(dict(source=entry, status='self_read_claim_mapping',
                                           claim_evidence_fields=['표본과 조건', '영상과 반응의 단위', '표와 주석', '적용 한계'],
                                           evidence_file='data/literature_claim_reviews.json', claim_ids=[row[0] for row in MAPPINGS]))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Registered the separate MADIF13 study, 2 mappings and 1 observation.')


if __name__ == '__main__':
    main()

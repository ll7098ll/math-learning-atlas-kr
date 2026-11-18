"""Register the separate empirical study cited in the LT2 matching activity."""
from math import erfc, sqrt

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value


SOURCE = 'MIX_MOORE_HOLCOMB_2011'
DATE = '2026-11-09'
URL = 'https://doi.org/10.1080/15248372.2011.554928'
PDF_URL = 'https://education.umd.edu/sites/default/files/uploads/Mix%20et%20al.%202011%20One-to-One%20Play.pdf'
PDF_SHA = 'f036cc5ec4b25e42709ea4e5074566c77724dc4664acf7eb3a24bd525e23bf26'
CACHE = ROOT / 'tmp/literature/lt2-comparing-number-assets'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
READ_SCOPE = '인쇄 463~480쪽의 본문·부록과 제공본 표지의 서지를 확인했다. 그림 1~3, 표 1~2와 부록이 있는 PDF 7·8·11·12·19쪽은 이미지를 대조했다.'
SCOPE_NOTE = '같은 종류의 물건과 같은 개수의 물건을 구별하는 유아 과제를 검토했다. 두 가지 가정 놀이 조건에서의 점수 변화는 연구가 사용한 문항과 표본의 범위로 해석한다.'
LIMITS = '사전 성적을 기준으로 선별한 지역 유아 표본과 6주간의 가정 놀이, 12문항의 개수 짝짓기에 한정한다. 분류 경계와 일부 검정 표기의 불일치, 장기 효과, 국내 학생 응답은 후속 검증 범위다.'
EMPIRICAL_SCOPE = dict(
    design='randomized_parallel_conditions_pre_post_selected_sample',
    sample_description='지역 유아기관에서 모집해 참여를 완료한 30명이다. 평균 3세 7개월이며, 칸이 있는 장난감 조건 16명과 낱개 장난감 조건 14명에 무작위 배정해 6주간 가정에서 놀이했다.',
    inference_limit='사전 점수에 따라 선별한 표본의 12문항 개수 짝짓기 변화에 한정한다. 사후 점수만의 집단 차이, 장기 전이, 국내 학생의 반응은 따로 검증해야 한다.',
    student_outcome_study=True,
    local_effect_tested=False,
)
MAPPINGS = [
    ('MMH01', 'empirical_result_with_scope', ['2수01-01', '2수01-03'],
     [PDF_URL + '#page=7', PDF_URL + '#page=10', PDF_URL + '#page=11'],
     '12문항 사전·사후 평균은 칸이 있는 장난감 조건에서 1.69점과 5.81점, 낱개 조건에서 2.43점과 4.00점이었다. 논문은 조건에 따른 사전·사후 변화 차이를 보고한다.',
     '사후 점수만의 비교에서 보고한 p값은 .065다. 변화의 집단 차이와 사후 한 시점의 차이를 구별하고, 표 1의 우연 수준 분류 및 일부 검정 표기의 불일치를 그대로 기록한다.'),
    ('MMH02', 'related_theoretical_context', ['2수01-01', '2수01-03', '2수03-06'],
     [PDF_URL + '#page=8', PDF_URL + '#page=9', PDF_URL + '#page=19'],
     '개수가 같은 보기와 종류는 같지만 개수가 다른 보기를 따로 둔다. 한 번 고른 답 외에 짝짓기나 세기로 확인한 근거와 사용한 도움을 기록할 수 있다.',
     '실험에서 사용한 장난감과 평가 자극의 범위는 서로 다르다. 새 관찰 과제는 논문의 12문항을 재현한 검사가 아니며, 선택 하나로 비교 전략이나 발달 단계를 확정하지 않는다.'),
]
OBSERVATION = dict(
    id='MMH-P1', standard_codes=['2수01-01', '2수01-03'],
    question='기준 카드에 종이 별이 3개 있다. 가에는 조개 그림 3개, 나에는 종이 별 4개, 다에는 구슬 그림 2개가 있다. 개수가 같은 카드를 고르고 한 개씩 짝지어 설명하라. 종류가 같은 카드를 고르면 무엇이 남는가?',
    expected='개수가 같은 것은 가다. 별과 조개가 세 짝이 된다. 종류가 같은 나는 별 네 개라서 세 짝을 만들고 나면 나에 별 하나가 남는다.',
    interpretation='종류를 보고 고른 답, 개수를 기준으로 고른 답, 짝짓기로 확인한 답을 따로 기록한다. 선택 직후와 도구를 제공한 뒤의 설명을 구별한다.',
    student_validated=False,
)


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert registry['sources'][SOURCE]['snapshot_sha256'] == sha(ROOT / NOTES)
        assert registry['sources'][SOURCE]['observations'] == [OBSERVATION]
        build_report()
        return
    evidence = load(CACHE / 'mix-study-preliminary-review.json')
    access = evidence['access']
    assert access['url'] == access['final_url'] == PDF_URL and access['sha256'] == sha(ROOT / access['file']) == PDF_SHA
    assert access['status'] == 200 and access['pdf_pages'] == 19 and access['print_pages'] == [463, 480]
    assert evidence['text_pdf_pages'] == list(range(2, 20))
    assert evidence['visual_pdf_pages'] == [7, 8, 11, 12, 19]
    assert all(sha(CACHE / f'mix-study-{page:02}.png') == evidence['render_sha256'][str(page)] for page in evidence['visual_pdf_pages'])
    assert abs(erfc(sqrt(5.83 / 2)) - evidence['discrepancies'][1]['conditional_p_value']) < 1e-10
    assert evidence['participants']['slots'] + evidence['participants']['loose'] == evidence['participants']['completed'] == 30

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    assert all(row['id'] != SOURCE for row in bibliography)
    entry = dict(id=SOURCE, title='One-to-One Play Promotes Numerical Equivalence Concepts',
                 authors=['Kelly S. Mix', 'Julie A. Moore', 'Erin Holcomb'], year=2011,
                 kind='무작위 배정 사전·사후 연구 논문', url=URL, review_scope=READ_SCOPE, next_review=LIMITS,
                 supports=['일대일 짝짓기와 개수 비교 관찰 설계', '선별 표본에서 두 놀이 조건의 변화 비교'],
                 does_not_establish='국내 과제의 진단 정확도, 학생 검증 또는 장기 효과')
    bibliography.append(entry)
    notes = dict(source_id=SOURCE, source_url=URL, source_pdf_url=PDF_URL, source_pdf_sha256=PDF_SHA,
                 source_asset_kind='pdf', date=DATE, reviewer='Codex', read_scope=READ_SCOPE,
                 contains_source_full_text=False, source_pdf_redistributed=False,
                 pdf_pages=19, bibliographic_cover_pdf_page=1, printed_pages=[463, 480],
                 text_pdf_pages=evidence['text_pdf_pages'], visual_pdf_pages=evidence['visual_pdf_pages'],
                 visual_pdf_page_hashes=evidence['render_sha256'], empirical_scope=EMPIRICAL_SCOPE,
                 participants=evidence['participants'], outcomes=evidence['outcomes'],
                 source_corrections=evidence['discrepancies'],
                 reading_log=['인쇄 463~467쪽은 같은 종류와 같은 수를 구별하는 과제와 연구 가설을 설명한다.',
                              '인쇄 467~471쪽은 사전 검사의 선별 기준, 두 놀이 조건과 가정에서의 6주 노출, 12문항의 비교 방법을 설명한다.',
                              '인쇄 471~473쪽의 집단 평균, 조건별 사전·사후 변화와 사후 비교를 구별했다. 부모 일지는 25명이 제출했다.',
                              '인쇄 472~473쪽의 우연 수준 점수 범위와 검정 표기를 대조했다. 원자료가 있어야 정정할 수 있는 값은 보류했다.',
                              '인쇄 474~480쪽의 논의·참고문헌과 부록에서 장난감 후보 및 후속 가설을 확인했다. 인용 논문의 본문 검토와 구별한다.'])
    path = ROOT / NOTES
    write(path, notes)
    registry['sources'][SOURCE] = dict(source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
                                       snapshot_kind='authored_review_notes', source_asset_kind='pdf', snapshot_file=NOTES,
                                       snapshot_sha256=sha(path), source_pdf_sha256=PDF_SHA, redistribution_license='workspace_authored_notes',
                                       bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=URL, authors_year='Mix·Moore·Holcomb, 2011'),
                                       read_scope=READ_SCOPE, scope_note=SCOPE_NOTE, empirical_scope=EMPIRICAL_SCOPE, limits=LIMITS,
                                       method_note='LT2의 활동 설명과 분리해 논문의 조건, 표본, 사전·사후 결과, 표와 본문의 불일치를 확인했다.',
                                       editorial_action='연구 근거 2건을 연결하고 비교 기준을 구별하는 자체 관찰 과제 1개를 추가했다.',
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
                                           claim_evidence_fields=['대상과 배정', '측정과 결과', '표기 불일치', '적용 한계'],
                                           evidence_file='data/literature_claim_reviews.json', claim_ids=[row[0] for row in MAPPINGS]))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Registered the separate matching study, 2 mappings and 1 observation.')


if __name__ == '__main__':
    main()

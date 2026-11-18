"""Register the Davis and Pitkethly paper cited by LT2's biscuit activity."""
from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value


SOURCE = 'DAVIS_PITKETHLY_1990'
DATE = '2026-11-09'
URL = 'https://www.jstor.org/stable/749141'
PDF_URL = 'https://bpb-us-w2.wpmucdn.com/sites.umassd.edu/dist/8/406/files/2019/02/Cognitive-Aspects-of-Sharing.pdf'
PDF_SHA = 'cc7a9f8b1c9f163fd6f464951545223b85aa0eafd9562d89d5c120061cef26a1'
CACHE = ROOT / 'tmp/literature/lt2-multiplying-dividing-activities'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
READ_SCOPE = '인쇄 145~153쪽의 논문 본문과 참고문헌을 읽었다. 서지와 과제·면담·논의의 PDF 2·3·4·8·10쪽은 이미지를 대조했다.'
SCOPE_NOTE = '같은 수를 차례로 나누는 절차와 각 몫을 다시 세는 확인을 구별한다. 영상 속 분배와 영상을 본 초등학생의 설명은 별도로 기록한다.'
LIMITS = '편집 영상을 본 한 학교의 초등 2학년 소집단 면담이다. 면담 질문과 대화의 영향을 고려하며 자연스러운 분배 행동이나 수업 효과를 일반화하지 않는다.'
EMPIRICAL_SCOPE = dict(
    design='qualitative_group_interviews_about_edited_video',
    sample_description='과자 12개를 두 인형과 세 인형에게 나눈 다섯 살 유아 3명의 편집 영상을 초등 2학년 17명이 여섯 소집단에서 보고 답했다.',
    inference_limit='같은 몫을 확인하기 위해 세어야 하는지에 대한 면담이다. 수업의 사전·사후 비교와 개인별 발달 비율은 제시하지 않는다.',
    student_outcome_study=False, causal_effect_established=False, local_effect_tested=False,
)
MAPPINGS = [
    ('DP01', 'empirical_result_with_scope', ['4수01-05'],
     [PDF_URL + '#page=4', PDF_URL + '#page=8', PDF_URL + '#page=9'],
     '연구는 동등한 분배 절차 자체가 충분하다고 명확히 설명한 초등학생 한 명과 면담 도중 생각을 바꾼 것으로 보인 사례를 구별한다.',
     '유아가 나누는 편집 영상을 본 소집단 면담의 설명이다. 이를 특정 나이의 숙달률이나 수업 효과로 옮기지 않는다.'),
    ('DP02', 'related_theoretical_context', ['2수01-03', '4수01-05', '4수01-06'],
     [PDF_URL + '#page=2', PDF_URL + '#page=3', PDF_URL + '#page=10'],
     '완전한 한 차례마다 모두에게 같은 수를 주면 다시 세기 전에도 몫의 수가 같다. 모든 사람에게 줄 수 없는 마지막 물건은 나머지로 따로 둔다.',
     '물건을 자르지 않고 개수로 공평함을 판단하는 조건이다. 높이로 개수를 비교하려면 두께와 쌓은 방식이 같아야 한다.'),
]
OBSERVATION = dict(
    id='DP-P1', standard_codes=['2수01-03', '4수01-05', '4수01-06'],
    question='과자 13개를 세 인형에게 순서대로 하나씩 준다. 세 인형 모두에게 하나씩 줄 수 있는 차례만 끝냈다면 각자 몇 개를 받고 몇 개가 남는가? 마지막 과자를 첫 인형에게 주어도 공평한가? 다시 세지 않고도 어떻게 설명할 수 있는가?',
    expected='네 차례를 끝내면 모두 4개씩 받고 1개가 남는다. 마지막 과자를 첫 인형에게 주면 5·4·4로 개수가 달라진다. 완전한 차례마다 모두가 하나씩 받았으므로 네 차례가 끝난 상태에서는 개수가 같다.',
    interpretation='순서를 기억한 답, 완전한 차례가 동등한 몫을 보장한다고 설명한 답, 다시 세어 확인한 답을 나누어 적는다.',
    student_validated=False,
)


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert registry['sources'][SOURCE]['snapshot_sha256'] == sha(ROOT / NOTES)
        assert registry['sources'][SOURCE]['observations'] == [OBSERVATION]
        build_report()
        return
    evidence = load(CACHE / 'davis-pitkethly-preliminary-review.json')
    assert evidence['source_url'] == URL and evidence['source_pdf_url'] == PDF_URL
    assert evidence['source_pdf_sha256'] == sha(CACHE / 'davis-pitkethly-1990.pdf') == PDF_SHA
    assert evidence['pdf_pages'] == 10 and evidence['printed_pages'] == [145, 153]
    assert evidence['text_pdf_pages'] == list(range(2, 11))
    renders = evidence['visual_pdf_pages']
    assert [r['pdf_page'] for r in renders] == [2, 3, 4, 8, 10]
    for r in renders:
        assert sha(CACHE / f"davis-pitkethly-{r['pdf_page']:02}.png") == r['sha256']
    roles = evidence['roles']
    assert roles['video_preschoolers'] == 3 and sum(roles['groups']) == roles['grade_two_group_interview'] == 17
    assert divmod(13, 3) == (4, 1)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    assert all(row['id'] != SOURCE for row in bibliography)
    entry = dict(id=SOURCE, title='Cognitive Aspects of Sharing',
                 authors=['Gary Ernest Davis', 'Anne Pitkethly'], year=1990,
                 kind='분배 영상을 활용한 소집단 면담 논문', url=URL, review_scope=READ_SCOPE, next_review=LIMITS,
                 supports=['순서에 따른 분배와 사후 확인의 구분', '완전한 차례와 나머지의 구별'],
                 does_not_establish='실제 수업 효과, 개인별 발달 단계, 국내 학생 검증')
    bibliography.append(entry)
    notes = dict(source_id=SOURCE, source_url=URL, source_pdf_url=PDF_URL, source_pdf_sha256=PDF_SHA,
                 source_asset_kind='pdf', date=DATE, reviewer='Codex', read_scope=READ_SCOPE,
                 contains_source_full_text=False, source_pdf_redistributed=False,
                 pdf_pages=10, printed_pages=[145, 153], text_pdf_pages=evidence['text_pdf_pages'],
                 visual_pdf_pages=[r['pdf_page'] for r in renders],
                 visual_pdf_page_hashes={str(r['pdf_page']): r['sha256'] for r in renders},
                 roles=roles, empirical_scope=EMPIRICAL_SCOPE, response_scope=evidence['response_scope'],
                 reading_log=evidence['reading_log'], math_scope=evidence['math_scope'],
                 source_corrections=[dict(kind='different_cited_authors', note=evidence['open_questions'][0])])
    path = ROOT / NOTES
    write(path, notes)
    registry['sources'][SOURCE] = dict(source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
                                       snapshot_kind='authored_review_notes', source_asset_kind='pdf', snapshot_file=NOTES,
                                       snapshot_sha256=sha(path), source_pdf_sha256=PDF_SHA, redistribution_license='workspace_authored_notes',
                                       bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=URL, authors_year='Davis·Pitkethly, 1990'),
                                       read_scope=READ_SCOPE, scope_note=SCOPE_NOTE, empirical_scope=EMPIRICAL_SCOPE, limits=LIMITS,
                                       method_note='과자 분배 활동의 안내와 분리해 유아 영상의 과제와 초등학생의 소집단 면담을 대조했다.',
                                       editorial_action='연구 근거 2건과 완전한 분배 차례를 구별하는 자체 관찰 과제 1개를 추가했다.',
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
                                           claim_evidence_fields=['영상과 면담의 표본', '관찰과 설명', '완전한 차례와 나머지', '적용 한계'],
                                           evidence_file='data/literature_claim_reviews.json', claim_ids=[row[0] for row in MAPPINGS]))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Registered the separate sharing study, 2 mappings and 1 observation.')


if __name__ == '__main__':
    main()

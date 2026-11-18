"""Register the primary number-conservation experiment cited in IES table D.7."""
from pypdf import PdfReader

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value


SOURCE = 'SIEGLER_1995_NUMBER_CONSERVATION'
DATE = '2026-11-09'
DOI = 'https://doi.org/10.1006/cogp.1995.1006'
PDF = 'https://siegler.tc.columbia.edu/wp-content/uploads/2020/10/How-does-change-occure-1995.pdf'
PDF_SHA = 'd98d6bb3e8f2dc9edcf2e3d184546ba6c75bb2a6ab852402cccca709fc9031d8'
WWC = 'https://ies.ed.gov/ncee/wwc/study/77988'
CACHE = ROOT / 'tmp/literature/siegler-1995-number-conservation'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
SOURCE_CORRECTIONS = [
    dict(location='IES 가이드 표 D.7과 원논문 인쇄 239쪽',
         issue='가이드는 평가자의 설명을 듣는 조건으로 요약했다. 원논문에서는 실험자가 정답을 알려 준 뒤 아이가 실험자의 판단 이유를 설명했다.',
         status='primary_procedure_used_in_claim'),
]
TEXT_PAGES = [1, *range(11, 19), 20, 27, 28, 34, 35, 36, 38, 39]
VISUAL_PAGES = [13, 14, 15, 17, 18, 20, 28]
READ_SCOPE = '인쇄 225·235~242·244·251~252·258~260·262~263쪽의 관련 문단을 읽고, PDF 13~15·17~18·20·28쪽에서 표 1·2, 그림 1·2와 4의 일부, 훈련 절차를 이미지로 대조했다.'
LIMITS = '선정한 유아가 최대 2주 동안 같은 큰 집합 문항을 다시 푼 단기 훈련의 조건 비교다. 설명 대상과 정답 피드백의 상대 순서가 함께 달라 두 요소의 효과를 분리할 수 없다. 지연 검사, 새 문항 전이와 국내 과제 효과는 이 연구에서 확인되지 않았다.'
SCOPE = dict(
    design='randomized_three_arm_repeated_item_experiment',
    sample_description='54~73개월 아동 97명 사전검사, 두 선정 조건을 충족한 45명 무작위 배정, 집단별 15명.',
    inference_limit=LIMITS, student_outcome_study=True,
    causal_effect_established=True, local_effect_tested=False,
)
CLAIMS = [
    ('SNC01', ['2수01-01'], [11, 14, 15],
     '세 조건 모두 정답 피드백을 받았다. 자기 설명 집단은 정답을 듣기 전에 자기 판단을 설명했고, 실험자 판단 설명 집단은 정답을 들은 뒤 실험자가 그렇게 판단한 이유를 아이가 직접 설명했다. 비교 조건은 훈련 중 정답 피드백만 받았다.',
     '설명 대상과 설명 시점이 함께 달랐다. 정답만 알려 주는 것과 이유를 말해 주는 것은 서로 다른 절차다.'),
    ('SNC02', ['2수01-01'], [13, 16, 17, 18],
     '길이 단서가 정답과 어긋나는 문항의 사전·마지막 훈련 정답률은 실험자 판단 설명 17%→72%, 자기 설명 13%→31%, 피드백만 9%→41%였다. 길이 단서가 정답과 맞는 문항은 집단 전체에서 80%→65%였고, 집단 주효과는 유의하지 않았다.',
     '정답률은 반복한 큰 집합 문항의 결과다. 모든 유형에서 성취가 개선되었다거나 72%의 아동이 수 보존을 숙달했다고 해석할 수 없다.'),
    ('SNC03', ['2수01-01', '2수01-05'], [12, 13, 20, 27, 28, 35, 36],
     '줄이 길다는 설명, 직접 센 설명, 실제로 더하거나 뺐는지에 근거한 설명을 구분해 코딩했다. 동일 문항에서도 앞서 변환을 근거로 설명한 아이가 이후 다른 설명을 했다. 실제 추가·제거와 간격만 바꾸는 상황을 각각 제시하고 최초 이유를 여러 번 확인하는 설계에 참고한다.',
     '한 번 정답을 맞히거나 설명한 것으로 모든 배열에서 같은 전략을 쓴다고 판단할 수 없다. 두 줄의 단추 과제에 한정된 결과로, 기호식 계산 숙달을 측정하지 않았다.'),
]
OBSERVATION = dict(
    id='SNC-P1', standard_codes=['2수01-01', '2수01-05'],
    question='매번 단추 7개씩 같은 두 줄에서 다시 시작하자. 첫째는 위 줄의 간격만 넓힌다. 둘째는 위 줄에 단추 한 개를 더하고 길게 배열한다. 셋째는 위 줄에서 한 개를 빼고도 아래 줄보다 길게 배열한다. 각 경우 어느 쪽이 더 많은가, 아니면 같은가? 무엇이 바뀌었는지 설명하자.',
    expected='위 줄은 차례로 7개, 8개, 6개이며 아래 줄은 언제나 7개다. 결과는 같다, 위가 더 많다, 아래가 더 많다 순이다. 실제 추가·제거를 설명하거나 일대일 짝짓기나 세기로 확인할 수 있다.',
    interpretation='세 경우에서 위 줄은 모두 더 길다. 처음 답과 이유를 도움 전에 따로 적고, 이후 짝짓기로 확인한 반응과 구별한다. 둘째만 맞히면 길이 판단으로도 나온 답인지 다른 두 경우와 대조한다. 국내 학생 반응과 과제 타당성은 별도 확인이 필요하다.',
    student_validated=False,
)


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert registry['sources'][SOURCE]['snapshot_sha256'] == sha(ROOT / NOTES)
        assert registry['sources'][SOURCE]['observations'] == [OBSERVATION]
        build_report()
        return

    pdf = CACHE / 'source.pdf'
    assert sha(pdf) == PDF_SHA and len(PdfReader(pdf).pages) == 49
    notes = dict(
        source_id=SOURCE, source_url=DOI, source_pdf_url=PDF, source_pdf_sha256=PDF_SHA,
        date=DATE, reviewer='Codex', read_scope=READ_SCOPE, contains_source_full_text=False,
        source_pdf_redistributed=False, publication='Cognitive Psychology, 28(3), 225–273',
        pdf_pages=49, text_pdf_pages=TEXT_PAGES, visual_pdf_pages=VISUAL_PAGES,
        text_read_method='저자 연구실 PDF의 웹 추출 텍스트에서 관련 문단을 대조하고 이미지로 표와 그래프를 확인했다.',
        visual_pdf_page_hashes={str(page): sha(CACHE / f'page-{page:02d}.png') for page in VISUAL_PAGES},
        source_corrections=SOURCE_CORRECTIONS,
        empirical_scope=SCOPE,
        source_comparison=dict(
            guide_source_id='IES_EARLY_2013', guide_table='D.7', existing_claim_id='IE17',
            wwc_url=WWC, wwc_review='2013년 11월, 기준 2.1에 따라 유보 없이 충족',
            guide_recommendation='권고 4의 등급은 Minimal이며 개별 연구 설계 평정과 구별한다.',
        ),
        selection=dict(
            pretested=97, randomized=45, participants_per_group=15, age_months=[54, 73],
            threshold='길이 단서 불일치 큰 집합 문항에서 정답과 변환 설명을 모두 제시한 비율이 20% 이하이고, 간격만 바꾼 길이 갈등 문항에서는 0%였다.',
            pretest_sessions=4, training_sessions=4, training_trials_per_session=12,
            pretest_set_sizes=[[2, 4], [7, 9]], training_set_size=[7, 9],
        ),
        results=dict(
            length_inconsistent_percent_correct=dict(explain_experimenter=[17, 72], explain_own=[13, 31], feedback_only=[9, 41]),
            length_consistent_percent_correct=dict(all_groups=[80, 65], explain_experimenter=[84, 67], explain_own=[82, 61], feedback_only=[75, 67]),
            checkpoints=['사전검사', '마지막 훈련'],
        ),
        reading_log=[
            'PDF 13쪽 표 1의 최종 배열은 웹 표에서 단추 간격이 보존되지 않아 실제 그림으로 대조했다. 길이와 개수의 관계를 의도적으로 교차시킨 여섯 유형이다.',
            'PDF 14~15쪽에서 선정 기준, 회차 구성, 사전검사 큰 집합 문항의 반복과 피드백 전후의 설명 순서를 확인했다.',
            'PDF 16~18쪽에서 그림 1과 그림 2의 문항군과 계열 범례를 대조했다. 도표에서 수치를 추정하는 대신 본문 인쇄 수치를 기록했다.',
            'PDF 20쪽 표 2와 27~28·34~36쪽 관련 본문에서 정답과 추론의 코딩, 사례별 변화, 동일 문항의 반응 변동을 구별했다.',
        ],
    )
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = dict(
        id=SOURCE, title='How Does Change Occur: A Microgenetic Study of Number Conservation',
        authors=['Robert S. Siegler'], year=1995, kind='유아 수 보존 무작위 비교 연구', url=DOI,
        review_scope=READ_SCOPE, next_review=LIMITS,
        supports=['세 피드백·설명 조건의 비교', '길이 단서와 수량 변화의 구별', '동일 문항의 추론 변동'],
        does_not_establish='지연 유지, 새 문항으로의 전이, 국내 과제의 효과와 타당성',
    )
    assert all(row['id'] != SOURCE for row in bibliography)
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    bibliography.append(entry)
    path = ROOT / NOTES
    write(path, notes)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE, state='self_read_claim_mapping', reviewer='Codex', date=DATE,
        snapshot_kind='authored_review_notes', source_asset_kind='pdf', snapshot_file=NOTES,
        snapshot_sha256=sha(path), source_pdf_sha256=PDF_SHA, redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry), display=dict(title=entry['title'], url=DOI, authors_year='Siegler, 1995'),
        read_scope=READ_SCOPE, empirical_scope=SCOPE, limits=LIMITS,
        scope_note='무작위 배정의 효과 범위는 해당 훈련 조건의 묶음과 반복 문항에 한정한다.',
        method_note='IES 표 D.7의 원연구에서 표본, 절차, 문항 유형별 결과와 추론 변동을 별도로 대조했다.',
        editorial_action='원연구의 문헌 대응 3건과 자체 관찰 과제 1개를 추가했다.',
        independent_review=False, student_validated=False, observations=[OBSERVATION],
    )
    for claim_id, codes, pages, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=claim_id, source_id=SOURCE, role='empirical_result_with_scope', standard_codes=codes,
            locations=[f'{PDF}#page={page}' for page in pages], support=support, does_not_establish=limit,
            independent_review=False, student_validated=False, empirical_scope=SCOPE,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue['literature_review'].append(dict(
        source=entry, status='self_read_claim_mapping', evidence_file='data/literature_claim_reviews.json',
        claim_evidence_fields=['설명 요구와 피드백 순서', '문항 유형별 효과', '추론 변동과 재관찰'],
        claim_ids=[claim[0] for claim in CLAIMS],
    ))
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Registered the number-conservation experiment with three claims and one observation.')


if __name__ == '__main__':
    main()

"""Record IES early-math appendix and evidence-table reading."""
import copy

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_ies_early_literature_review import PDF_URL, RATINGS, SHA, SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/IES_EARLY_2013_extension_review_notes.json'
PRIOR_SHA = '268e735dae49b5d48adea3223bac46044866499f05d5a979afd3b7ce98284cd0'
NOTES = 'data/literature_evidence/IES_EARLY_2013_appendix_review_notes.json'
CACHE = ROOT / 'tmp/literature/ies-early-appendix-review'
NEW_PAGES = [65,66,67,68,69,70,73,74,77,78,79,80,81,142,151]
SCOPE = '전체 PDF 165쪽 중 누적 텍스트 96쪽과 이미지 47쪽을 대조했다. 부록 A~C와 표 D.1·D.2, 미주 78·252가 실린 페이지를 추가로 확인했다.'
LIMITS = ('나머지 연구표 D.3·D.4·D.6~D.8과 연결 본문, 미주·참고문헌의 나머지 범위, 당시 프로토콜과 원연구는 후속 범위다. '
          '측정 연구 건수 9와 10은 집계 단위가 확인되기 전까지 확정 인용을 보류한다.')

TABLE_D1 = {
    'Arnold 2002':'1345', 'Aunio et al. 2005':'15', 'Barnett 2008':'1245',
    'Baroody et al. 2009':'1', 'Casey 2008':'2', 'Clements and Sarama 2007b':'12345',
    'Clements and Sarama 2008':'12345', 'Clements et al. 2011':'12345',
    'Curtis et al. 2009':'1', 'Dyson et al. 2013':'1345', 'Fantuzzo et al. 2011':'12345',
    'Fuchs et al. 2001':'4', 'Griffin et al. 1995 and related 1994 publication':'1345',
    'Jordan et al. 2012':'1345', 'Kidd et al. 2008':'12', 'Klein et al. 2008':'12345',
    'Lai et al. 2008':'1', 'Monahan 2007':'15', 'PCER 2008 ch. 2':'12345',
    'PCER 2008 ch. 3':'12345', 'Ramani and Siegler 2008':'15', 'Ramani and Siegler 2011':'5',
    'Sarama et al. 2008':'12345', 'Siegler 1995':'4', 'Siegler and Ramani 2008':'15',
    'Siegler and Ramani 2009':'5', 'Sood 2009':'1', 'Sophian 2004':'1245', 'Weaver 1991':'2',
}
TABLE_D2 = [
    ('Arnold 2002','RCT',103,'?','', [('general_numeracy',0.40,'ns')]),
    ('Clements and Sarama 2007b','RCT',68,'X','X', [('basic_number',0.75,'*'),('geometry',1.40,'*')]),
    ('Clements and Sarama 2008','RCT',201,'?','?', [('general_numeracy',1.07,'*')]),
    ('Clements et al. 2011','RCT',1305,'X','X', [('general_numeracy',0.48,'*'),('basic_number',0.39,'*'),('geometry',0.64,'*')]),
    ('Griffin et al. 1995 and related 1994 publication','QED',47,'?','?', [('basic_number',1.79,'*')]),
    ('Klein et al. 2008','RCT',278,'X','X', [('general_numeracy',0.57,'*')]),
    ('Sarama et al. 2008','RCT',200,'?','?', [('general_numeracy',0.62,'*')]),
]
OBS = dict(
    id='IE-P9', standard_codes=['2수03-10'],
    question='길이 11 cm인 종이띠 위에 1 cm 조각 11개를 빈틈 없이 놓았다. 1 cm 조각을 네 개씩 붙여 만든 새 조각으로 덮으면 새 조각 몇 개와 1 cm 조각 몇 개가 필요한가? 두 방법의 길이는 같은가?',
    expected='4 cm 조각 두 개와 1 cm 조각 세 개가 필요하다. 8 cm와 3 cm를 이으면 11 cm다. 반복하는 단위와 개수의 표현이 바뀌었지만 길이는 같다.',
    interpretation='네 작은 단위가 한 큰 단위가 된다는 설명과 남은 작은 단위의 처리를 확인한다. 계산식의 형식보다 빈틈·겹침 없이 길이가 유지되는지 관찰한다.',
    student_validated=False,
)
MAPPINGS = [
    ('IE10', OBS['standard_codes'], 2, [38,39,74,142,151],
     '부록의 측정 중심 과정은 작은 단위를 묶어 큰 단위를 만들거나 다시 나누어 보도록 한다. 동일한 길이에서 단위 수가 달라지고 묶고 남은 단위를 설명하는 과제에 참고한다.',
     '권고 2의 등급은 Minimal이다. 과정의 단위 활동 하나의 효과나 국내 학년의 진단 타당성은 검증하지 않았다. 표와 미주에서 가르친 요소와 측정한 결과를 구별한다.'),
    ('IE11', ['2수01-01','2수01-04','2수01-05'], 1, [77,78,79,80,81],
     '권고 1의 근거 표 D.2에서는 일반 수리력과 기본 수 개념 등의 총점과 하위 기능을 나눠 읽는다. 가이드는 Clements 외(2011)의 기본 수 개념 총점에서 긍정 결과를 표시했으나 수의 합성 하위척도는 뚜렷한 효과로 분류하지 않았다.',
     '권고 1의 등급은 Moderate이다. 교육과정 묶음의 비교는 단일 발달 순서나 합성 활동만의 효과를 분리하지 못한다. D.2의 Positive는 통계적으로 유의하거나 0.25 표준편차 이상이라는 당시 기준이며 항상 유의하다는 뜻이 아니다.'),
]


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['reading_extension']['file'] == NOTES:
        assert source['observations'][-1] == OBS
        assert {row[0] for row in MAPPINGS} <= {row['id'] for row in registry['claims']}
        build_report()
        return
    assert source['reading_extension'] == dict(file=PRIOR,sha256=PRIOR_SHA)
    assert sha(ROOT / PRIOR) == PRIOR_SHA and sha(ROOT / source['snapshot_file']) == SHA
    prior = load(ROOT / PRIOR)
    text_pages = sorted(set(source['text_pdf_pages']) | set(NEW_PAGES))
    visual_pages = sorted(set(source['visual_pdf_pages']) | set(NEW_PAGES))
    assert (len(text_pages),len(visual_pages)) == (96,47)
    counts = [sum(str(number) in cols for cols in TABLE_D1.values()) for number in range(1,6)]
    assert len(TABLE_D1) == 29 and counts == [23,13,12,16,20] and sum(counts) == 84
    assert len(TABLE_D2) == 7 and sum(len(row[-1]) for row in TABLE_D2) == 10
    assert 11 == 4*2+3
    d5_symbols = [row['measurement_column'] for row in prior['measurement_table_audit']['rows']]
    assert (d5_symbols.count('X'),d5_symbols.count('?')) == (6,5)
    correction = dict(
        locations=['PDF 32','PDF 96','PDF 100–106','PDF 142 note 78','PDF 151 note 252'],
        issue='본문 9연구와 부록 10연구의 차이가 남는다. 미주 78과 252 모두 일곱 개입에 EPIC을 포함한다.',
        status='epic_inclusion_resolved_study_count_open',
        followup='D.5의 X 6행과 ? 5행, D.1의 권고 2 인용행 13개는 각각 다른 단위다. 독립 표본 수나 측정 연구 9·10의 조정으로 쓰지 않는다.',
    )
    log = [
        'PDF 65~70쪽에서 지침의 등급·외부 동료 검토 과정, 집필진 역할, EPIC·Building Blocks와 평가 도구 관련 공개 사항을 대조했다.',
        'PDF 73~74쪽에서 표 D.1의 인용행 29개와 권고별 열, 프로그램 설명과 비교 조건의 도입을 대조했다.',
        'PDF 77~81쪽에서 권고 1의 교육과정 유형과 D.2의 연구 비교·하위척도·기호 및 표 주석 1~14를 대조했다. ?는 비교 집단 수업 정보 부족을 뜻한다.',
        'PDF 142쪽 미주 78과 151쪽 미주 252에서 두 목록이 동일하게 EPIC을 포함함을 확인했다. 인용 목록과 비교·결과별 행을 독립 연구로 합산하지 않는다.',
    ]
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE,next_review=LIMITS)
    notes = dict(
        source_id=SOURCE,source_url=source['display']['url'],source_pdf_sha256=SHA,contains_source_full_text=False,
        licensed_source_pdf_preserved=True,previous_review=copy.deepcopy(source),previous_bibliography=previous_entry,
        previous_reading_extension=dict(file=PRIOR,sha256=PRIOR_SHA),
        cumulative_read_scope=SCOPE,cumulative_text_pdf_pages=text_pages,cumulative_visual_pdf_pages=visual_pages,
        new_text_pdf_pages=NEW_PAGES,new_visual_pdf_pages=NEW_PAGES,unread_full_pdf_pages=sorted(set(range(1,166))-set(text_pages)),
        reading_log=log,new_image_sha256={str(p):sha(CACHE / f'page-{p}.png') for p in NEW_PAGES},
        source_corrections=[correction],evidence_ratings=RATINGS,
        table_d1=dict(location='PDF 73',citation_rows=TABLE_D1,counts_by_recommendation=counts,membership_marks=84,
                      counts_are_independent_studies=False),
        table_d2=dict(location='PDF 78–81',comparisons=[
            dict(citation=c,design=d,reported_children=n,number_operations_column=number,
                 progression_column=progression,reported_outcomes=[dict(domain=k,effect_size=e,significance=s) for k,e,s in outcomes])
            for c,d,n,number,progression,outcomes in TABLE_D2
        ],participants_are_not_summed=True),
    )
    note_path = ROOT / NOTES
    write(note_path,notes)
    source.update(
        date=DATE,bibliography_snapshot=digest(entry),reading_extension=dict(file=NOTES,sha256=sha(note_path)),
        text_pdf_pages=text_pages,visual_pdf_pages=visual_pages,read_scope=SCOPE,
        limits=LIMITS,reading_log=source['reading_log']+log,source_discrepancies=[correction],
        editorial_action='부록과 연구표 대조에서 문헌 대응 2건과 자체 관찰 과제 1개를 추가했다.',
        observations=source['observations']+[OBS],
    )
    for cid,codes,number,pages,support,limit in MAPPINGS:
        registry['claims'].append(dict(
            id=cid,source_id=SOURCE,role='instructional_recommendation_with_evidence_scope',
            locations=[f'{PDF_URL}#page={p}' for p in pages],support=support,does_not_establish=limit,
            target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes},
            standard_codes=codes,independent_review=False,student_validated=False,local_effect_tested=False,
            recommendations=[dict(number=number,evidence_rating=RATINGS[str(number)],application_limit=limit)],
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry,claim_ids=[c['id'] for c in registry['claims'] if c['source_id'] == SOURCE])
    write(bibliography_path,bibliography)
    write(ROOT / 'data/literature_claim_reviews.json',registry)
    write(queue_path,queue)
    build_report()
    print('Registered IES appendix and evidence-table reading with two claims and one observation.')


if __name__ == '__main__':
    main()

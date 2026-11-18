"""Register the routines-based guidance cited by three LT2 angle activities."""
from pypdf import PdfReader

from extend_lt2_angle_turn_review import NOTES as ANGLE_NOTES, ROUTINES_URL
from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE as LT_SOURCE


SOURCE = 'JENNINGS_HANLINE_WOODS_2012'
DATE = '2026-11-09'
PDF_SHA = 'dd3675a02e095883d357e235c8a63a58b3e8838143e2291f62b0a0c8bcc7c9d1'
CACHE = ROOT / 'tmp/literature/lt2-angle-turn-cited'
NOTES = f'data/literature_evidence/{SOURCE}_review_notes.json'
READ_SCOPE = '인쇄 13~22쪽의 일과 기반 중재 안내와 사례를 확인했다. PDF 1·7·8쪽의 서지와 표, 11쪽의 별개 서평 경계를 이미지로 대조했다.'
LIMITS = '특수교육의 일과에 중재를 포함하는 실천 지침과 사례다. 산책 활동에서 각도 이해가 향상됐는지 비교하거나 검증한 연구는 아니다.'
CODES = ['2수03-02','4수03-04']
OBSERVATION = dict(
    id='JHW-P1',standard_codes=CODES,
    question='산책이나 교실 이동에서 익숙한 갈림길에 도착했다. 같은 방향을 바라본 상태에서 어디로 돌아야 하는지 말하거나 손으로 가리키고, 다음에는 모형 인형으로 같은 방향 전환을 보여 준다.',
    expected='갈림길에 들어오는 방향을 기준으로 왼쪽이나 오른쪽을 표시한다. 실제 이동과 모형에서 기준 방향을 같게 두고 확인한다.',
    interpretation='교사가 먼저 시범을 보였는지, 학생이 말·가리키기·모형으로 무엇을 나타냈는지 구별해 기록한다.',
    student_validated=False,
)


def main():
    registry = load_registry()
    if SOURCE in registry['sources']:
        assert registry['sources'][SOURCE]['snapshot_sha256'] == sha(ROOT / NOTES)
        assert registry['sources'][SOURCE]['observations'] == [OBSERVATION]
        build_report()
        return
    pdf = CACHE/'jennings-hanline-woods-2012.pdf'
    assert sha(pdf) == PDF_SHA
    pages = PdfReader(pdf).pages
    assert len(pages) == 11
    assert 'Routines-Based' in pages[0].extract_text()
    assert 'Melissa Workman' in pages[10].extract_text()
    visual_pages = [1,7,8,11]
    lt = registry['sources'][LT_SOURCE]
    assert lt['snapshot_file'] == ANGLE_NOTES
    lt_notes = load(ROOT / ANGLE_NOTES)
    links = lt_notes['angle_turn_cited_routines_pdf']
    assert links['url'] == ROUTINES_URL and len(links['linking_pages']) == 3

    bibliography_path = ROOT/'data/sources.json'
    bibliography = load(bibliography_path)
    assert all(row['id'] != SOURCE for row in bibliography)
    entry = dict(
        id=SOURCE,title='Using Routines-Based Interventions in Early Childhood Special Education',
        authors=['Danielle Jennings','Mary Frances Hanline','Juliann Woods'],year=2012,
        kind='특수교육의 일과 기반 중재 실천 지침과 사례',url=ROUTINES_URL,
        review_scope=READ_SCOPE,next_review=LIMITS,
        supports=['일과에서 목표·단서·반응·지원을 구별해 관찰'],
        does_not_establish='각도 학습에 대한 효과, 국내 수업 효과나 실제 학생 검증',
    )
    bibliography.append(entry)
    notes = dict(
        source_id=SOURCE,source_url=ROUTINES_URL,source_pdf_url=ROUTINES_URL,source_pdf_sha256=PDF_SHA,
        date=DATE,reviewer='Codex',read_scope=READ_SCOPE,contains_source_full_text=False,
        source_pdf_redistributed=False,publication='Dimensions of Early Childhood, 40(2), 13–22',
        pdf_pages=11,printed_pages=[13,22],text_pdf_pages=list(range(1,11)),visual_pdf_pages=visual_pages,
        visual_pdf_page_hashes={str(page):sha(CACHE/f'page-{page:02d}.png') for page in visual_pages},
        linking_lt2_pages=links['linking_pages'],
        source_corrections=[
            dict(kind='citation_page_boundary',note='LT2 참고문헌에 13~23쪽으로 적혔으나 인쇄 23쪽은 Melissa Workman의 별도 서평이다. 출판사 권별 색인은 본문을 13~22쪽으로 표시한다.',
                 locations=[ROUTINES_URL+'#page=11','https://www.seca.info/_files/ugd/8f06cd_04cff77ddd174f19a98e8839fbfb36f5.pdf']),
        ],
        reading_log=[
            '인쇄 13~15쪽에서 자연스러운 생활 환경과 반복되는 일과를 안내하는 목적을 확인했다.',
            '인쇄 16~18쪽에서 개별 목표, 환경, 참여 기회, 교사의 촉진 전략을 고르는 순서와 실행 계획을 확인했다.',
            '인쇄 19~20쪽에서 실행 기준 표와 여러 일과에 의사소통·이동·식사 목표를 대응한 사례 표를 확인했다.',
            '인쇄 21~22쪽에서 가족·교사·전문가의 관찰 공유와 경과 검토, 참고 자료의 범위를 확인했다.',
        ],
    )
    path = ROOT/NOTES
    write(path,notes)
    registry['sources'][SOURCE] = dict(
        source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date=DATE,
        snapshot_kind='authored_review_notes',source_asset_kind='pdf',snapshot_file=NOTES,
        snapshot_sha256=sha(path),source_pdf_sha256=PDF_SHA,redistribution_license='workspace_authored_notes',
        bibliography_snapshot=digest(entry),display=dict(title=entry['title'],url=ROUTINES_URL,authors_year='Jennings·Hanline·Woods, 2012'),
        read_scope=READ_SCOPE,scope_note='일과와 목표를 대응하고 지원과 관찰 반응을 구별하는 실천 맥락을 확인했다.',
        limits=LIMITS,method_note='본문의 실행 순서와 일과·목표 대응표를 대조했다.',
        editorial_action='실천 지침의 대응 1건과 산책 방향 전환 자체 관찰 과제 1개를 추가했다.',
        independent_review=False,student_validated=False,observations=[OBSERVATION],
    )
    registry['claims'].append(dict(
        id='JHW01',source_id=SOURCE,role='related_theoretical_context',standard_codes=CODES,
        locations=[ROUTINES_URL+f'#page={page}' for page in (4,6,7,8)],
        support='일과에 목표를 대응하고 성인이 무엇을 지원했는지와 아동의 반응을 기록하는 절차를 제시한다. 각도 활동에는 방향을 표시하는 일과와 관찰 방식의 설계 맥락으로 연결한다.',
        does_not_establish=LIMITS,independent_review=False,student_validated=False,
        target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in CODES},
    ))
    queue_path = ROOT/'data/content_review_queue.json'
    queue = load(queue_path)
    assert all(row['source']['id'] != SOURCE for row in queue['literature_review'])
    queue['literature_review'].append(dict(
        source=entry,status='self_read_claim_mapping',
        claim_evidence_fields=['일과와 개별 목표','지원과 반응의 기록','수학 효과 연구와 적용 범위'],
        evidence_file='data/literature_claim_reviews.json',claim_ids=['JHW01'],
    ))
    write(bibliography_path,bibliography)
    write(ROOT/'data/literature_claim_reviews.json',registry)
    write(queue_path,queue)
    build_report()
    print('Registered routines-based guidance: 10 source pages, 1 claim and 1 observation.')


if __name__ == '__main__':
    main()

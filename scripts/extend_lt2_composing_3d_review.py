"""Register reviewed LT2 solid composition activity pages and their attachments."""
import copy
from itertools import combinations
from urllib.parse import urljoin, urlparse

from extend_lt2_composing_2d_assets_review import verified_assets
from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_pharaoh_blueprint_review_notes.json'
PRIOR_SHA = '4b5edf6e409bc0b1cc5b86b6894d4acf3deb604637a12c081551dbc1dfc0919a'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_composing_3d_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-composing-3d-shapes-activities'
ASSETS = ROOT / 'tmp/literature/lt2-composing-3d-shapes-assets'
SCOPE = ('공개 영어 HTML 956개를 대조했다. 활동·교사자료 목록 824개 중 706개를 확인했고 118개가 남았다. '
         '입체도형 구성의 영어 페이지 20개, PDF 1개 URL·1쪽과 이미지 22개 URL을 확인했다.')
LIMITS = ('가정 활동은 공개 페이지 소개와 삽입 그림 일부, 블록 연구는 공개 영어 페이지의 소개를 확인했다. '
          '별도 가정 안내, 연구 영상, 인용 원문과 실제 수업 결과는 후속 범위다.')

READING = """
a-bed-for-puppy--piece-assembler-3d|빈틈 없이 평평한 침대를 구성한다. 같은 단면과 길이의 조각을 맞대는 조건을 제시한다.
block-area-set-up-separate-blocks-actor-foundations|놀이 재료와 공간 지침이다. 삼각기둥 위에 쌓을 수 있는지는 평평한 면의 방향과 받침에 따라 달라진다.
block-play-3d-shape-composition-line-maker|가로 배열과 쌓기를 시범 보이고 옆·위·아래를 기준 물체와 함께 말한다.
block-play-3d-shape-composition-stacker|줄 만들기 수준과 같은 안내가 반복된다. 한 자료를 별개 효과로 세지 않는다.
block-stacker|합동 블록의 방향을 맞춰 쌓는다. 조각의 방향과 합동 여부를 구별한다.
build-a-bridge|다리의 지지대와 경사로를 계획한다. 통과 폭과 다리 조각의 전체 길이를 구별한다.
build-a-tower|판을 바닥과 층 사이에 놓고 탑을 만든다. 층을 한 단위로 볼 때도 낱개 블록은 따로 센다.
build-roads|블록을 이어 길이나 통로를 표현한다. 배열 방향과 간격을 기록한다.
building-shapes-with-blocks|지붕과 통로 높이, 아치와 벽의 구조를 실제 들어갈 모형에 맞춘다.
crash-boom-same-shape-stacker|코끼리 윤곽 높이와 탑을 비교한다. 바닥선과 높이 단위를 맞춘다.
lets-explore-with-blocks-stemie-separate-blocks-actor-foundations|굴리기·쌓기·담기를 시범 보이고 손짓과 보완대체 의사소통도 허용한다.
lets-stack-blocks-stemie-line-maker|시범과 보조 재료를 제공한다. 스스로 놓는 방향을 정한 수행을 따로 기록한다.
lets-stack-blocks-stemie-same-shape-stacker|다른 수준에 같은 절차가 있다. 합동 블록을 골라 쌓는 수행은 시범 반복과 따로 본다.
lets-stack-blocks-stemie-stacker|맞물림·벨크로를 지원으로 쓴다. 지원 여부를 비교 조건에 명시한다.
line-em-up-knock-em-down|탑을 무너뜨리는 놀이와 가로로 늘어놓은 블록 위에 장난감을 놓는 절차가 있다.
making-scenes-with-blocks|장면과 물체의 부분을 블록으로 나타낸다. 지붕처럼 한 부분에 대응시키는 표현을 살핀다.
making-things-with-blocks|두 개 이상을 묶어 장면의 한 부분을 구성하는 과제를 제시한다.
researcher-note-blocks|영어 소개가 블록 배치와 발문을 안내한다. 동반 영상과 인용 연구의 본문은 별도다.
spatial-learning-at-home-separate-blocks-actor-foundations|가정 공간놀이 자료 소개다. 공개 페이지의 소개와 삽입 안내 그림 일부를 확인했다.
stacking-numbers|색으로 다섯 개를 나눈다. 색별 개수와 쌓는 순서를 구별하고 연결 큐브와 나무 블록의 접합 조건을 구분한다.
"""
PDF_NOTES = {
    '1603809351302': [([1], '코끼리 윤곽 그림이다. 바닥 기준선과 측정 눈금이 없어서 종이를 붙인 높이와 윤곽 자체 높이를 구별한다.')],
}
IMAGE_NOTES = [
    ([0,1,2,3,4,5,6,7,9,12,13,14,15,18,19,20], '블록 배열과 놀이 장면이다. 탑의 정확한 높이와 접촉면 크기는 이미지로 정하지 않는다.'),
    ([8,10,11], '블록 연구 소개 사진, 강아지 사진, 코끼리와 블록 삽화다. 영상과 책 본문은 별도다.'),
    ([16,17,21], '맞물리지 않는 블록과 놀이 보조 도구, 위치말과 따라 그리기가 보이는 가정 안내 일부다.'),
]

CLAIMS = [
    ('LT152','LT-P143',['2수03-02','4수03-12','6수03-05'],(0,),(),
     '같은 직사각형을 대각선으로 자른 두 직각삼각형을 같은 길이로 늘인 조각은 빗변에 해당하는 직사각형 면을 맞대어 직육면체를 만들 수 있다.',
     '밑면 삼각형과 기둥의 길이 및 방향이 대응해야 한다. 삼각기둥 두 개라는 개수만으로 직육면체가 되지는 않는다.',
     '밑면이 3 cm, 4 cm, 5 cm인 합동 직각삼각기둥 두 개의 기둥 길이가 2 cm이다. 빗변에 해당하는 면을 맞추어 직육면체를 만들 때 세 변의 길이는?',
     '두 삼각형을 돌려 두 직각이 직사각형의 마주 보는 꼭짓점에 오게 맞대면 밑면은 3 cm×4 cm이고 기둥 길이는 2 cm이다.',
     '조각 수와 어느 면을 어느 방향으로 붙이는지 구별한다.'),
    ('LT153','LT-P144',['2수03-06','2수03-10','2수03-13'],(4,9),('1603809351302',),
     '같은 바닥에서 높이가 일정한 단위 블록을 빈틈 없이 한 줄로 쌓을 때 블록 수로 높이를 비교할 수 있다. 코끼리 인쇄물에는 측정 눈금과 바닥 기준선이 없다.',
     '그림의 바닥을 높여 붙이면 바닥에서 그림 꼭대기까지의 높이와 코끼리 윤곽의 높이가 달라진다.',
     '코끼리 그림은 높이가 16 cm이고 발 위치를 바닥에서 4 cm 위에 붙였다. 높이가 4 cm인 블록으로 바닥에서 그림 꼭대기까지 쌓으려면 몇 개가 필요한가? 그림 자체는 몇 개 높이인가?',
     '그림 꼭대기까지는 4+16=20 cm로 5개가 필요하다. 그림 자체는 16 cm로 4개 높이다.',
     '높이를 재기 시작하는 지점과 단위 블록의 높이를 각각 말하게 한다.'),
    ('LT154','LT-P145',['2수01-04','9수04-05'],(19,),(),
     '빨강 두 개와 파랑 세 개는 색별 개수로는 5를 만드는 한 가지 분해다. 쌓은 순서를 비교하면 빨강이 차지하는 두 위치에 따라 열 가지가 된다.',
     '색별 개수와 위치 순서에 따른 분류 기준을 먼저 명시한다. 같은 색의 조각은 구별하지 않고 아래에서 위로 읽는다.',
     '빨강 블록 2개와 파랑 블록 3개를 쌓는다. 빨강 블록이 아래에서 1·2번째인 탑과 1·3번째인 탑은 색별 개수가 같은가? 쌓는 순서는 모두 몇 가지인가?',
     '두 탑 모두 빨강 2개와 파랑 3개다. 다섯 위치 중 빨강 위치 두 개를 고르는 열 가지 순서가 가능하다.',
     '구체물로 두 탑을 비교한 뒤 위치를 고르는 방법으로 경우를 센다.'),
    ('LT155','LT-P146',['2수03-02','2수03-06','2수03-10'],(5,6,8),(),
     '다리의 경간이나 모형이 지나가는 통로는 지지대 사이의 빈 공간을 기준으로 비교한다. 다리 조각의 전체 길이는 지지대 위에 닿는 부분까지 포함한다.',
     '치수가 맞는다는 계산은 통과 공간과 겹침 길이에 관한 것이다. 실제 하중을 견디는지는 재료·접합·하중을 확인해야 한다.',
     '두 지지대 안쪽 간격이 12 cm다. 다리 조각이 양쪽 지지대 위에 각각 2 cm씩 걸쳐야 한다. 두 지지대 사이의 통과 폭과 필요한 조각 길이를 각각 구한다.',
     '통과 폭은 12 cm다. 조각 길이는 2+12+2=16 cm다.',
     '통과하는 공간과 지지대에 걸치는 구간을 손으로 짚거나 그림에 표시한다.'),
    ('LT156','LT-P147',['2수03-02','6수03-09'],(1,2,3,10,11,12,13,19),(),
     '같은 배열을 만들더라도 맞물리는 연결 큐브, 벨크로로 고정한 블록, 매끈한 블록은 접합 조건이 다르다. 모형 비교에서는 위치와 개수, 받은 도움을 따로 기록한다.',
     '자료에 같은 블록 활동이 여러 수준으로 반복된다. 반복 링크나 교구로 고정한 성공을 독립된 효과나 스스로 구성한 수행으로 세지 않는다.',
     '아래에 블록 두 개를 나란히 놓고, 왼쪽 블록 위에 한 개를 놓는 모형을 만든다. 연결 큐브로 만든 모형과 매끈한 블록으로 만든 모형에서 공통으로 기록할 것은?',
     '두 모형에 모두 블록 세 개가 있다. 위 블록이 아래 왼쪽 블록 위에 있다는 위치도 같다. 교구의 연결 방식과 도움 여부는 따로 기록한다.',
     '배치·개수와 교구 지원을 서로 다른 관찰 항목으로 적는다.'),
]
OBSERVATIONS = [
    dict(id=oid, standard_codes=codes, question=question, expected=expected,
         interpretation=interpretation, student_validated=False)
    for _, oid, codes, _, _, _, _, question, expected, interpretation in CLAIMS
]


def verify_examples():
    # A 3-by-4 rectangle is split along (0,0)–(3,4), then extruded by 2.
    triangles = (((0,0),(3,0),(3,4)), ((0,0),(0,4),(3,4)))
    assert set(triangles[0]) & set(triangles[1]) == {(0,0),(3,4)}
    assert all(abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])) == 12 for a,b,c in triangles)
    red_positions = list(combinations(range(1,6), 2))
    assert len(red_positions) == 10 and len(set(red_positions)) == 10
    assert divmod(4+16,4) == (5,0) and divmod(16,4) == (4,0)
    assert 12+2+2 == 16
    return dict(prism_planar_triangles=triangles, prism_dimensions=[3,4,2], red_positions=red_positions,
                top_from_floor_cm=20, outline_height_cm=16, bridge_span_cm=12, bridge_piece_cm=16)


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        assert source['snapshot_sha256'] == sha(ROOT / NOTES)
        assert {row[0] for row in CLAIMS} <= {row['id'] for row in registry['claims']}
        assert source['observations'][-len(OBSERVATIONS):] == OBSERVATIONS
        build_report()
        return
    assert source['snapshot_file'] == PRIOR and sha(ROOT / PRIOR) == PRIOR_SHA
    prior = load(ROOT / PRIOR)
    pages, bodies, selected = [load(CACHE / name) for name in ('activity-manifest.json','english-bodies.json','selection.json')]
    followup = copy.deepcopy(prior['activity_followup_catalog'])
    assert selected == [row for row in followup['records'] if not row['body_read']
                        and any('/math/composing-3d-shapes/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|',1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 20
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/',1)[-1] for row in pages] == [row[0] for row in reading]

    old_images = {row['url'] for row in prior['image_read_manifest']}
    old_pdfs = {row['url'] for row in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for page, body, (_, note) in zip(pages,bodies,reading,strict=True):
        url = page['url']
        assert page['status'] == 200 and page['final_url'] == url and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256']
        teacher = 'Type:\nTeacher Resources' in body['body']
        introduction = url.endswith('/spatial-learning-at-home-separate-blocks-actor-foundations')
        assert ('\nActivity\n' in body['body']) != introduction
        kind = 'teacher_resource' if teacher else 'activity_procedure'
        if introduction:
            kind = 'home_resource_intro'
        groups['teacher_resources' if teacher else 'activities'].append(page['key'])
        logs.append(dict(url=url, page_kind=kind, note=note))
        linked_images = {urljoin(url, image['src']) for image in page['images'] if '/upload/' in image.get('src','')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert [row['page_kind'] for row in logs].count('teacher_resource') == 2
    assert [row['page_kind'] for row in logs].count('home_resource_intro') == 1

    raw_pdfs, raw_images = [load(ASSETS / f'{kind}-manifest.json') for kind in ('pdf','image')]
    new_pdfs, new_images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images, PDF_NOTES, IMAGE_NOTES)
    assert len(new_pdfs) == 1 and len(new_images) == 22
    assert asset_pairs(new_pdfs) == linked_pairs(pdfs) and asset_pairs(new_images) == linked_pairs(images)
    all_pdfs = prior['supplementary_pdf_read_manifest'] + new_pdfs
    all_images = prior['image_read_manifest'] + new_images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (174,609)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (160,553)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (956,929)
    asset_urls = {'1603809351302': new_pdfs[0]['url']}

    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key','url','title','sha256','status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 956
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'],followup['listed_body_pending']) == (706,118)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE,next_review=LIMITS)
    notes = dict(prior)
    notes.update(
        date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
        observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
        catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies':706, 'pending_activity_bodies':118},
        new_read_groups=dict(domain_overviews=0,levels=0,activities=18,teacher_resources=2,inline_images=22,supplementary_pdf_urls=1),
        composing_3d_reading_log=logs, completed_composing_3d_records=selected, composing_3d_checked_examples=verify_examples(),
        composing_3d_pdf_reading_log=pdf_notes, composing_3d_image_reading_log=image_notes,
        supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
        supplementary_pdf_coverage=dict(urls=174,page_occurrences=609,distinct_sha256_files=160,
            pages_after_file_deduplication=553,all_selected_pages_visual_reviewed=True,whole_site_attachment_review=False),
        pdf_exact_reuse_groups=reuse_groups(all_pdfs),
        pdf_reading_log={**prior['pdf_reading_log'], **{
            url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows] for url,rows in pdf_notes.items()
        }},
        reading_log=prior['reading_log'] + ['입체도형 구성의 영어 페이지 20개와 PDF 1쪽·이미지 22개 URL을 대조했다.'],
        source_corrections=prior['source_corrections'] + [dict(
            kind='solid_composition_join_and_measurement_conditions',
            locations=[pages[i]['url'] for i in (0,1,5,8,9,11,19)] + [new_pdfs[0]['url']],
            action='맞대는 면과 방향, 측정 기준선, 통과 폭과 전체 길이, 개수와 순서를 구별했다.',
        )],
        unread_followups=prior['unread_followups'] + [LIMITS],
    )
    note_path = ROOT / NOTES
    write(note_path,notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=source['date'],read_scope=source['read_scope'])]
    source.update(
        date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(note_path),snapshot_history=history,
        bibliography_snapshot=digest(entry),html_read_manifest=manifest,read_scope=SCOPE,limits=LIMITS,
        method_note='입체 구성과 높이 비교의 활동 본문, 코끼리 인쇄물과 삽입 그림을 대조했다.',
        editorial_action='문헌 대응 5건과 자체 관찰 과제 5개를 추가했다.',observations=source['observations'] + OBSERVATIONS,
        image_read_manifest=all_images,supplementary_pdf_read_manifest=all_pdfs,
    )
    for cid,_,codes,indices,files,support,limit,*_ in CLAIMS:
        registry['claims'].append(dict(
            id=cid,source_id=SOURCE,role='related_theoretical_context',standard_codes=codes,
            locations=[pages[i]['url'] for i in indices]+[asset_urls[file] for file in files],
            support=support,does_not_establish=limit,independent_review=False,student_validated=False,
            target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry,claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE])
    write(bibliography_path,bibliography)
    write(ROOT / 'data/literature_claim_reviews.json',registry)
    write(queue_path,queue)
    build_report()
    print('Reviewed 20 solid composition pages, 1 PDF and 22 images; added 5 claims and 5 observations.')


if __name__ == '__main__':
    main()

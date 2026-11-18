"""Register LT2 angle and turn activities, local attachments, and checked examples."""
import copy
from math import atan, degrees
from statistics import linear_regression
from urllib.parse import urljoin, urlparse

from PIL import Image

from extend_lt2_composing_2d_assets_review import pdf_name, verified_assets
from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_composing_3d_review_notes.json'
PRIOR_SHA = '9f3838517c5f8a57c035c6903182e67be9a70af92db6c6cd61156d8ca4a1749f'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_angle_turn_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-angle-turn-activities'
ASSETS = ROOT / 'tmp/literature/lt2-angle-turn-assets'
ROUTINES_URL = 'https://www.wvsha.org/wp-content/uploads/events-manager-uploads/session-handouts/Handout%20Preschool%20Language%202.pdf'
SCOPE = ('공개 영어 HTML 978개를 대조했다. 활동·교사자료 목록 824개 중 728개를 확인했고 96개가 남았다. '
         '각도와 회전의 영어 페이지 22개, LT2 PDF 3개 URL·6쪽과 이미지 23개 URL을 확인했다.')
LIMITS = ('자료의 인쇄 각을 렌더링에서 어림했다. 실물 도구와 수업 결과는 측정하지 않았다. '
          '별도 360° 각도기, 활동 영상, 인용 원문은 별도 범위로 구분했다.')

READING = """
a-walk-in-the-park-angle-senser-foundations|산책 방향과 회전을 말과 손짓으로 나타낸다. 왼쪽과 오른쪽의 기준 방향을 확인한다.
a-walk-in-the-park-intuitive-angle-builder-stemie|산책의 방향 바꾸기와 미끄럼틀에서 물체를 놓는 활동을 구분한다.
angle-architect|판과 수평면의 각을 바꾸고 예상한다. 각도만 비교하려면 물체·표면·출발 조건을 같게 한다.
angle-matching|투명 카드를 포개어 각을 비교한다. 반직선을 그린 길이와 두 방향 사이의 벌어짐을 구별한다.
arm-angles|팔로 기준각을 어림한 뒤 각도기로 확인한다. 한 바퀴는 최종 자세만으로 판별하지 않는다.
around-every-corner|두 도로가 이루는 작은 각과 주행 방향을 바꾼 각을 비교한다.
around-every-corner-is-an-angle|시계로 회전 중심과 방향을 표시하고, 작은 각이 더 긴 선분으로 그려질 수 있음을 다룬다.
as-the-world-turns-angle-measurer|어림과 측정을 나누어 기록한다. 각도기 중심과 시작 방향 0°를 맞춘다.
as-the-world-turns-angle-size-comparer|문·가위·경사면의 두 방향을 각각 정한다. 손잡이의 실제 회전량은 기구마다 다를 수 있다.
as-the-world-turns-implicit-angle-user|직진과 평행, 꺾임과 수직을 구분한다. 만나는 두 길이 항상 직각인 것은 아니다.
blocks-and-angle|블록 놀이 환경과 관찰·발문을 안내한다. T자 예의 수직은 실제 직각을 확인해 판별한다.
discussing-angles-in-constructions|평행·수직과 구조 안정성을 나눈다. 경사진 부재가 있는 구조도 세울 수 있다.
exploring-force-and-motion-stemie|이동 방향과 회전을 보고 말하거나 손짓한다. 도움과 학습자의 선택을 따로 기록한다.
exploring-ramps-stemie|판의 기울어진 각·물체·출발점을 바꾼다. 출발 위치와 각을 동시에 바꾸면 어느 조건의 영향인지 가르기 어렵다.
in-out-and-around-stemie|통로 안팎, 직진과 회전을 신체 활동으로 탐색한다.
lets-go-for-a-drive-stemie|차가 향하는 방향의 변화와 도로가 수평면과 이루는 각을 따로 말한다. 기울기 비와 도 단위 각은 같은 양이 아니다.
maze-maker|직선 구간과 통로, 회전 구간을 만들고 통과를 확인한다. 진행 방향을 화살표로 표시한다.
pick-the-correct-rhombus|마름모 조각과 틈의 각을 맞춘다. 도형이 빈틈 없이 맞으려면 해당 변의 길이와 방향도 확인한다.
researcher-note--angle-misconceptions-angle-matcher|각을 그린 선분 길이·끝점 사이 거리·그림의 방향에 따른 판단 오류를 정리한다. 출처의 비율은 이 페이지에서 검증하지 않았다.
researcher-note--angle-misconceptions-angle-size-comparer|다른 수준의 연구자 메모에도 같은 오류 예시가 나온다. 별개 조사로 세지 않는다.
roll-slide-stay|공·블록·인형의 예측과 실제 관찰을 나누어 적는다. 예시 45°를 보편적 기준으로 쓰지 않는다.
using-angles-to-sort-shapes|직각이 하나 이상 있는 도형과 직각이 없는 도형을 나눈다. 직각의 방향이나 개수를 기준과 섞지 않는다.
"""

PDF_NOTES = {
    '1580340753001': [
        ([1], '방향을 달리한 직각 카드와 예각 카드를 두 장씩 제시한다.'),
        ([2], '비슷하게 벌어진 예각 카드 네 장이다. 렌더링의 검은 선을 맞춰 보니 위쪽은 약 21°, 아래쪽은 약 23°로 나타나 네 장 전부를 정확히 같은 각으로 채점하기 어렵다.'),
        ([3], '반대 방향으로 돌린 둔각 카드 두 장이다. 격자와 카드 틀은 각의 두 변에서 제외한다.'),
    ],
    '1603211418897': [([1], '직선 구간·각·통로 그림이다. 두 반직선의 화살표는 꼭짓점에서 나가므로 실제 주행의 들어오는 방향을 따로 표시한다.')],
    '1616771417228': [
        ([1], '공·블록·인형을 놓았을 때의 예상 1~10과 관찰 1~9를 적는다. 제시 각도는 시험 조건이며 예시 답안은 없다.'),
        ([2], '관찰 10번 기록란이 다음 쪽에 있다.'),
    ],
}
IMAGE_NOTES = [
    ([0,1,2,3,4,5,8,10,13,14,15,16,17,18,19,20], '각·방향·블록 놀이의 맥락, 재료와 탐색 사진이다. 물체의 실제 이동이나 각을 정지 사진으로 판정하지 않는다.'),
    ([6,7,9,11,12], '문·손잡이·회전과 미로, 15° 경사 설명의 그림이다. 15°는 표시 예시이며 실제 판의 경사를 재지는 않았다.'),
    ([21,22], '연구자 메모의 소개 사진이다. 영상이나 원연구를 읽은 것으로 세지 않는다.'),
]

CLAIMS = [
    ('LT157','LT-P148',['4수03-01','4수03-02','4수03-24'],(3,6,18,19),('1580340753001',),
     '두 각의 꼭짓점과 한쪽 반직선을 맞춘 뒤 나머지 방향을 비교한다. 그려진 선분의 길이나 종이의 방향은 각의 크기를 정하지 않는다.',
     '첨부 2쪽의 위·아래 카드는 인쇄 그림에서 약 2° 차이로 나타났다. 네 카드를 정확히 같은 각으로 채점하기보다 모양과 인쇄 오차를 구분한다.',
     '같은 60°를 두 장에 그린다. 첫 종이는 두 반직선의 일부를 2 cm씩, 두 번째는 5 cm씩 보이게 하고 종이를 돌려 놓는다. 각의 크기를 어떻게 비교하는가?',
     '꼭짓점과 한쪽 반직선의 방향을 맞추면 다른 반직선도 같은 방향이다. 보이는 길이와 관계없이 둘 다 60°다.',
     '겹치기에서 맞추는 점과 방향을 설명하게 한다.'),
    ('LT158','LT-P149',['4수03-02','4수03-04','4수03-24'],(0,5,14,16),('1603211418897',),
     '꺾인 길에서 꼭짓점으로 들어오는 주행 방향은 꼭짓점에서 출발점 쪽으로 그린 반직선과 반대다. 두 길 사이의 작은 각과 작은 방향 전환량을 구분한다.',
     '한 꼭짓점에서 두 직선 구간을 잇고 더 작은 방향 전환을 택할 때 두 각의 합이 180°다. 여러 번 회전하거나 방향을 지정하면 각을 따로 기록한다.',
     '두 길이 꼭짓점에서 60°의 작은 각을 이룬다. 첫 길로 꼭짓점에 들어와 둘째 길로 나갈 때 작은 방향 전환량은?',
     '직진하는 방향은 첫 길을 꼭짓점 바깥으로 그린 반직선의 반대쪽이다. 그 연장 방향에서 둘째 길까지는 180°−60°=120°다.',
     '들어오는 방향과 나가는 방향을 화살표로 표시하게 한다.'),
    ('LT159','LT-P150',['4수03-04','4수03-24'],(4,7,8),(),
     '회전은 시작 방향에서 얼마나 돌았는지를 센다. 1°는 한 바퀴를 360등분했을 때 한 부분에 해당하는 각의 크기다.',
     '반원 각도기의 두 눈금에서는 시작 반직선에 놓인 0°에서 읽는다. 시작과 끝 방향만 같다고 회전량까지 같은 것은 아니다.',
     '화살표를 그대로 둔 경우와 시계 방향으로 한 바퀴 돌린 경우에 시작과 끝은 모두 위쪽이다. 두 회전량을 비교하고, 반원 각도기의 기준 0°는 어디에 맞추는지 설명한다.',
     '회전량은 각각 0°와 360°다. 각도기 중심은 꼭짓점에, 읽을 눈금의 0°는 시작 반직선 방향에 맞춘다.',
     '정지한 모양과 실제 움직인 회전량을 구별하는지 확인한다.'),
    ('LT160','LT-P151',['4수03-02','4수03-24','9수02-16'],(1,2,13,15,20),('1616771417228',),
     '경사면의 각은 판과 수평면을 기준으로 잰다. 각의 영향을 보려면 같은 물체를 같은 표면과 출발 표시에서 밀지 않고 놓고, 예측과 관찰을 따로 기록한다.',
     '45°는 관찰지의 한 조건이다. 다른 물체와 표면에서 움직이기 시작하는 각은 달라질 수 있다. 기울기는 수직 변화량과 수평 변화량의 비다.',
     '20° 판에서 나무 블록을, 60° 판에서 공을 놓아 한쪽만 움직였다. 경사각만의 영향을 비교하려면 실험을 어떻게 다시 짜야 하는가?',
     '같은 물체를 같은 판의 같은 표시에서 같은 방식으로 놓고 각만 20°와 60°로 바꾼다. 예상과 실제로 구르거나 미끄러지거나 멈춘 결과를 각각 적는다.',
     '각 이외에 바뀐 물체와 출발 조건을 찾고 대조 실험을 설명하게 한다.'),
    ('LT161','LT-P152',['4수03-02','4수03-03','4수03-10','4수03-12'],(9,10,11,17,21),(),
     '서로 만난 길은 실제 각이 90°일 때 수직이다. 마름모 조각을 빈칸에 맞출 때는 각과 변의 길이가 모두 대응해야 한다.',
     '만났다는 사실만으로 수직이라고 할 수 없고, 한 각이 같아도 조각 전체가 빈칸에 맞는다고 할 수 없다.',
     '빈칸은 한 변이 4 cm이고 한 내각이 60°인 마름모다. 한 변 2 cm·60° 조각과 한 변 4 cm·60° 조각 중 어느 것이 틈에 맞는가?',
     '4 cm·60° 조각이다. 두 조각은 각이 같지만 2 cm 조각은 변이 짧아 빈칸 전체를 채우지 못한다.',
     '한 꼭짓점의 각 비교와 전체 경계의 일치를 구별한다.'),
]
OBSERVATIONS = [
    dict(id=oid,standard_codes=codes,question=question,expected=expected,interpretation=interpretation,student_validated=False)
    for _,oid,codes,_,_,_,_,question,expected,interpretation in CLAIMS
]


def verify_examples(raw_pdfs):
    page = next(row for row in raw_pdfs if pdf_name(row['url']) == '1580340753001')['renders'][1]
    assert page['pdf_page'] == 2
    crops = [
        ((270,411,418,478),(270,487,418,498)),
        ((801,244,970,313),(801,205,970,219)),
        ((270,924,414,1003),(270,1014,414,1027)),
        ((850,903,912,944),(850,962,912,1039)),
    ]
    with Image.open(ROOT / page['file']) as image:
        gray = image.convert('L')
    directions = []
    for pair in crops:
        slopes = []
        for x0,y0,x1,y1 in pair:
            points = [(x,y) for x in range(x0,x1) for y in range(y0,y1) if gray.getpixel((x,y)) < 100]
            assert len(points) >= 100
            slopes.append(degrees(atan(linear_regression(*zip(*points)).slope)))
        directions.append(round(abs(slopes[0]-slopes[1]),1))
    assert all(21 < value < 22 for value in directions[:2])
    assert all(23 < value < 24 for value in directions[2:])
    return dict(pdf_page=2, card_order=['top_left','top_right','bottom_left','bottom_right'],
                raster_estimates_degrees=directions, grayscale_threshold=100, fitted_crops=crops,
                estimate_method='ordinary least squares on dark pixels in selected ray interiors',
                road_included_angle=60, smaller_turn_angle=180-60,
                zero_turn_and_one_revolution=[0,360], compare_ramp_angles=[20,60])


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
                        and any('/math/measurement-angle-and-turn/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|',1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 22
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
        assert '\nActivity\n' in body['body']
        kind = 'teacher_resource' if teacher else 'activity_procedure'
        groups['teacher_resources' if teacher else 'activities'].append(page['key'])
        logs.append(dict(url=url, page_kind=kind, note=note))
        linked_images = {urljoin(url, image['src']) for image in page['images'] if '/upload/' in image.get('src','')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert [row['page_kind'] for row in logs].count('teacher_resource') == 3
    cited_routines = {page: url for page, urls in pdfs.items() for url in urls if url == ROUTINES_URL}
    assert set(cited_routines) == {pages[i]['url'] for i in (0,1,15)}
    lt2_pdfs = {page: [url for url in urls if url != ROUTINES_URL] for page, urls in pdfs.items()}

    raw_pdfs, raw_images = [load(ASSETS / f'{kind}-manifest.json') for kind in ('pdf','image')]
    new_pdfs, new_images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images, PDF_NOTES, IMAGE_NOTES)
    assert len(new_pdfs) == 3 and len(new_images) == 23
    assert asset_pairs(new_pdfs) == linked_pairs(lt2_pdfs) and asset_pairs(new_images) == linked_pairs(images)
    all_pdfs = prior['supplementary_pdf_read_manifest'] + new_pdfs
    all_images = prior['image_read_manifest'] + new_images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (177,615)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (163,559)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (979,952)
    asset_urls = {pdf_name(pdf['url']): pdf['url'] for pdf in new_pdfs}

    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key','url','title','sha256','status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 978
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'],followup['listed_body_pending']) == (728,96)

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
        catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies':728, 'pending_activity_bodies':96},
        new_read_groups=dict(domain_overviews=0,levels=0,activities=19,teacher_resources=3,inline_images=23,supplementary_pdf_urls=3),
        angle_turn_reading_log=logs, completed_angle_turn_records=selected, angle_turn_checked_examples=verify_examples(raw_pdfs),
        angle_turn_pdf_reading_log=pdf_notes, angle_turn_image_reading_log=image_notes,
        supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
        supplementary_pdf_coverage=dict(urls=177,page_occurrences=615,distinct_sha256_files=163,
            pages_after_file_deduplication=559,all_selected_pages_visual_reviewed=True,whole_site_attachment_review=False),
        pdf_exact_reuse_groups=reuse_groups(all_pdfs),
        pdf_reading_log={**prior['pdf_reading_log'], **{
            url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows] for url,rows in pdf_notes.items()
        }},
        reading_log=prior['reading_log'] + ['각도와 회전의 영어 페이지 22개와 LT2 PDF 6쪽·이미지 23개 URL을 대조했다.'],
        source_corrections=prior['source_corrections'] + [dict(
            kind='angle_matching_turn_and_experiment_conditions',
            locations=[pages[i]['url'] for i in (3,5,7,9,13,17,20)] + [pdf['url'] for pdf in new_pdfs],
            action='각의 크기와 그려진 길이, 회전량과 길 사이 각, 예측과 관찰, 맞는 각과 맞는 경계를 구별했다.',
        )],
        angle_turn_cited_routines_pdf=dict(url=ROUTINES_URL, linking_pages=sorted(cited_routines), status='separate_cited_article'),
        angle_turn_separate_material_pending=[
            dict(page=pages[i]['url'], material='360° protractor', status='named_in_body_without_direct_pdf_link') for i in (7,8,9)
        ],
        unread_followups=prior['unread_followups'] + [LIMITS],
    )
    note_path = ROOT / NOTES
    write(note_path,notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=source['date'],read_scope=source['read_scope'])]
    source.update(
        date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(note_path),snapshot_history=history,
        bibliography_snapshot=digest(entry),html_read_manifest=manifest,read_scope=SCOPE,limits=LIMITS,
        method_note='각 비교 카드, 길의 회전과 경사각의 측정·관찰 조건을 본문·첨부에서 대조했다.',
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
    print('Reviewed 22 angle and turn pages, 3 LT2 PDFs and 23 images; added 5 claims and 5 observations.')


if __name__ == '__main__':
    main()

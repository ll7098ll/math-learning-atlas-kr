"""Record the English bodies of LT2's solid-shape activity pages."""
import copy
from itertools import combinations
from urllib.parse import urljoin, urlparse

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_composing_2d_assets_review_notes.json'
PRIOR_SHA = 'af6496342e0d476d5edaaa3c43d4f9ee80761037d65181c8057e3da9d500b468'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_3d_shapes_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-3d-shapes-activities'
SCOPE = ('공개 영어 HTML 936개를 읽었다. 활동과 교사자료 목록 824개 중 686개를 확인했고 138개가 남았다. '
         '이번 입체도형 범위는 활동 절차 22개와 교사자료 1개다.')
LIMITS = ('연결 PDF 4개와 삽입 이미지 28개 URL, 별도 파라오 전개도·인쇄 안내와 인용 교재는 후속 범위다. '
          '물건의 이름·겉보기와 도형의 정의를 구별하며, 실물 굴리기·접기와 수업 결과는 측정하지 않았다.')

READING = """
block-area-set-up-3d-perceiver-foundations|블록 공간과 재료를 제안한다. 맞물리지 않는 블록의 안정성은 놓는 면과 방향에 따라 달라지므로 삼각기둥은 항상 쌓을 수 없다는 식으로 설명하지 않는다.
block-play-3d-shapes|블록을 놀이와 정리 중에 이름 붙이고 한 면을 본뜬 자리와 맞춘다. 정사각형 면과 정육면체 전체를 구별한다.
circle-sphere-story-activity-3d-prototype-recognizer|고리의 평면 윤곽과 분리된 비눗방울의 거의 구인 입체 모양을 비교한다. 붙은 막과 떨어진 방울의 조건을 구별한다.
circle-sphere-story-activity-3d-shape-recognizer|위와 같은 절차가 다른 수준에도 있다. 수준 표기가 달라도 별개 실험 결과로 세지 않는다.
circles-and-cans-3d-prototype-recognizer|깡통의 밑면을 본뜬 크기가 다른 원을 실물과 포개어 확인한다. 원 둘레, 원판, 입체인 원기둥을 구별한다.
circles-and-cans-3d-shape-recognizer|다른 수준에 같은 밑면 짝짓기가 있다. 반지름이 같고 높이가 다른 원기둥은 같은 밑면 윤곽에 맞을 수 있다.
guess-my-rule-3d-shape-class-identifier|다면체와 각기둥 등 속성으로 분류한다. 평면과 입체 예시의 분류 대상을 섞지 않으며 예가 적으면 여러 규칙이 가능하다.
how-many-sides|용기의 평평한 면을 세고 상자를 펼친다. 면의 수와 실제 접을 수 있는 전개도의 연결을 구별한다.
lets-explore-with-blocks-stemie-3d-perceiver-foundations|굴리기·쌓기·담기·쏟기와 언어·손짓·보완대체 의사소통의 접근성을 다룬다.
look-at-mystery-boxes-3d-prototype-recognizer|표시를 가린 상자의 길이·너비·높이로 내용물을 예상한다. 비슷한 치수에서 내용물이 하나로 정해지지는 않는다.
matching-faces-3d-shape-recognizer|다른 두 입체의 한 면도 합동일 수 있다. 모든 입체에 평면인 면이 있다는 안내는 구를 반례로 들어 보완한다.
playing-with-stuffed-animals|발달과 안전에 맞는 재료를 잡고 탐색하는 놀이 안내다. 재료 예시의 월령을 판정 기준으로 쓰지 않는다.
rectangles-and-boxes-3d-shape-recognizer|상자의 여섯 면을 떨어뜨려 본뜬 목록과 실제 전개도를 구별한다. 정육면체는 직육면체의 특수한 경우다.
roll-or-slide-3d-perceiver|경사판에서 물체의 구름·미끄러짐·정지를 관찰한다. 재료 예시는 일정한 시험 조건에서만 비교한다.
roll-or-slide-3d-shape-identifier|경사·표면과 놓는 방향을 바꿔 같은 원기둥의 움직임을 비교한다. 굴렀다는 사실 하나로 구를 판별할 수 없다.
shape-hunt-3d-prototype-recognizer|교실 물건을 정육면체·구·어느 쪽도 아님으로 분류한다. 직육면체인 휴지 상자가 항상 정육면체는 아니다.
shape-hunt-counting-faces|교실 물건의 평평한 면 수를 찾아 표에 적는다. 면 수가 같아도 면 모양과 배치가 다를 수 있다.
shapes-in-our-school-3d-shape-identifier|학교에서 닮은 물체를 찾아 속성으로 설명한다. 구의 곡면은 다면체의 평평한 면과 구별한다.
shapes-in-our-school-3d-shape-recognizer|위와 같은 절차다. 각기둥의 두 밑면은 합동인 평행 다각형이며, 각뿔 설명에서 밑면과 삼각형 옆면을 구별한다.
spatial-talk-3d-perceiver-foundations|놀이·식사·산책의 공간말을 제안한다. 왼쪽·오른쪽, 앞·뒤 같은 말은 기준 물체나 사람을 정한다.
the-pharaohs-prism|정삼각형 둘과 정사각형 셋의 배열을 떼지 않고 접을 수 있는지 먼저 예상한다. 본문의 A·B·D·E 해답과 실제 도안 대조는 별도다.
what-shape-am-i|예·아니요 질문으로 입체 카드의 속성을 좁힌다. 여섯 면과 같은 모서리 길이라는 단서가 식별에 충분한지는 카드 범위에 따라 다르다.
which-box-am-i-stemie|표시한 상자와 전개도를 짝짓고 면을 대어 확인한다. 각 면의 합동 여부와 접었을 때 서로 만나는 변을 모두 확인한다.
"""

CLAIMS = [
    ('LT143',['2수03-01','2수03-03','6수03-07'],[1,2,3,4,5,17,18],
     '깡통 밑면의 테두리를 본뜬 원과 원판인 밑면, 원기둥 전체를 구별한다. 지름이 같은 두 원기둥은 높이가 달라도 같은 테두리와 맞는다.',
     '비눗방울 고리의 평면 윤곽을 떠난 방울에 그대로 적용하지 않는다. 생활 물건과 비눗방울은 수학적 도형의 근사 예로 다룬다.'),
    ('LT144',['2수03-01','6수03-07'],[0,8,13,14],
     '경사판에서 원기둥의 축을 가로로 놓을 때와 밑면을 바닥에 댈 때의 움직임을 비교한다. 구름 여부는 접촉면과 방향, 경사와 마찰 등의 조건에 따라 달라진다.',
     '구름·미끄러짐·정지는 관찰값이다. 움직임만 보고 도형을 정하거나 모든 재료에서 같은 결과가 나온다고 일반화하지 않는다.'),
    ('LT145',['6수03-03','6수03-05','6수03-07'],[6,10,12,17,18,21],
     '합동인 한 면을 공유하는 입체도 서로 다른 입체일 수 있다. 각기둥은 평행하고 합동인 두 다각형 밑면으로 확인하고, 각뿔은 밑면과 한 꼭짓점으로 모이는 삼각형 옆면을 구분한다.',
     '구에는 평평한 면이 없다. 곡면을 세는 활동에서는 면이라는 낱말의 사용 범위를 따로 적고 다면체의 면 수와 섞지 않는다.'),
    ('LT146',['6수03-03','6수03-04','6수03-06'],[7,12,20,22],
     '직육면체의 떨어진 여섯 면은 면의 모양과 크기를 비교하는 목록이다. 전개도에서는 면 사이 연결과 접었을 때 서로 만나는 모서리까지 확인한다.',
     '필요한 면의 수가 모두 맞아도 접으면 겹치거나 구멍이 남을 수 있다. 활동 본문의 특정 도안 해답은 도안을 확보한 뒤 따로 대조한다.'),
    ('LT147',['2수03-01','2수04-01','6수03-03','6수03-05'],[6,9,15,16,21],
     '여섯 면이라는 단서로 정육면체와 길이가 다른 직육면체를 가르기 어렵다. 규칙 추측에서는 한 분류에 함께 들어갈 수 있는 서로 다른 입체를 놓고 새 예로 규칙을 확인한다.',
     '생활 물건의 이름이나 상자 속 예상 물건은 도형 정의의 근거가 아니다. 면 개수의 분류와 각 면의 모양·치수를 활용한 식별을 따로 본다.'),
]
OBSERVATION_DATA = [
    ('LT-P134','지름이 6 cm인 밑면을 가진 높이 4 cm와 9 cm의 원기둥을 지름 6 cm의 원에 올려 본다. 어느 것이 맞는가? 원 하나로 높이도 정해지는가?',
     '두 밑면의 테두리가 모두 맞는다. 이 원은 밑면의 지름을 정하지만 높이 4 cm와 9 cm는 모두 가능하다.', '원 둘레·원판·입체 전체를 가리키게 한다.'),
    ('LT-P135','같은 원기둥을 같은 경사판에 옆면이 닿도록 가로 방향으로 놓고, 다음에는 밑면이 닿게 세운다. 어떤 차이를 예상하는가? 움직임을 관찰해 조건과 함께 적는다.',
     '옆면이 닿고 축이 내리막 방향에 수직이면 굴러가기 쉽다. 밑면을 대면 경사와 마찰에 따라 멈추거나 미끄러질 수 있고 경사가 크면 넘어질 수도 있다.', '재료·판을 고정한 뒤 방향을 바꾼다. 예상과 실제 결과를 구별한다.'),
    ('LT-P136','모서리 4 cm인 정육면체와 4 cm×4 cm×7 cm 직육면체에서 서로 합동인 면을 골라라. 구에서도 같은 방식으로 평평한 면을 고를 수 있는가?',
     '정육면체의 어느 면이나 직육면체의 4 cm×4 cm 면과 합동이다. 두 입체 전체의 치수는 다르다. 구에는 같은 방식으로 고를 수 있는 평평한 면이 없다.', '한 면의 합동, 입체의 합동, 곡면을 구별한다.'),
    ('LT-P137','정사각형 세 개를 가로 띠로 연결한다. 합동인 정삼각형 두 개를 가운데 정사각형의 위·아래에 단 배열과, 첫째·가운데 정사각형의 위쪽에 하나씩 단 배열 중 어느 쪽을 삼각기둥으로 접을 수 있는가? 변 길이는 모두 같다.',
     '가운데 정사각형의 위·아래에 단 배열은 띠의 서로 반대쪽 끝을 막는다. 위쪽 두 칸에 단 배열은 삼각형 두 개가 같은 밑면에 포개져 다른 밑면이 열린다.', '면을 떼지 않고 접는 조건, 옆면 띠의 위·아래 경계를 각각 확인한다.'),
    ('LT-P138','면이 여섯 개라는 대답만으로 정육면체, 정육면체가 아닌 직육면체, 오각기둥 중 어느 것인지 정할 수 있는가? 한 질문을 더 고른다.',
     '오각기둥에는 면이 일곱 개이므로 빠진다. 남은 두 도형에 모든 면이 정사각형인지를 묻거나 모서리 길이가 모두 같은지를 확인한다.', '처음 단서로 탈락하는 후보와 추가 단서가 필요한 후보를 구별한다.'),
]
OBSERVATIONS = [dict(id=oid,standard_codes=claim[1],question=question,expected=expected,
                     interpretation=interpretation,student_validated=False)
                for claim,(oid,question,expected,interpretation) in zip(CLAIMS,OBSERVATION_DATA,strict=True)]


def verify_examples(bodies):
    text = [row['body'] for row in bodies]
    assert 'every 3D shape has 2D shaped faces' in text[10]
    assert 'separate rectangles that are not touching' in text[12]
    assert 'parallel to the top of the ramp' in text[14]
    assert 'one curved face' in text[17] and 'one curved face' in text[18]
    assert 'Model A, B, D, E' in text[20] and 'cannot detach' in text[20]
    assert [(n,n+2) for n in range(3,6)] == [(3,5),(4,6),(5,7)]
    face_dimensions = [tuple(pair) for pair in combinations([4,4,7],2)] * 2
    assert face_dimensions.count((4,4)) == 2 and face_dimensions.count((4,7)) == 4
    return dict(rectangular_prism_edge_lengths=[4,4,7], face_dimensions=face_dimensions,
                prism_face_counts={'triangular':5,'quadrangular':6,'pentagonal':7},
                triangular_prism_net_examples=dict(square_strip_count=3,
                    closes_both_bases=['middle_top','middle_bottom'], overlaps_one_base=['first_top','middle_top']))


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
                        and any('/math/3d-shapes/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|',1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 23
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/',1)[-1] for row in pages] == [row[0] for row in reading]
    examples = verify_examples(bodies)

    old_images = {row['url'] for row in prior['image_read_manifest']}
    old_pdfs = {row['url'] for row in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for page, body, (_, note) in zip(pages,bodies,reading,strict=True):
        url = page['url']
        assert page['status'] == 200 and page['final_url'] == url and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256']
        teacher_resource = 'Type:\nTeacher Resources' in body['body']
        assert '\nActivity\n' in body['body']
        groups['teacher_resources' if teacher_resource else 'activities'].append(page['key'])
        logs.append(dict(url=url, page_kind='teacher_resource' if teacher_resource else 'activity_procedure', note=note))
        linked_images = {urljoin(url, image['src']) for image in page['images'] if '/upload/' in image.get('src','')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert sum(row['page_kind'] == 'teacher_resource' for row in logs) == 1
    assert len({url for links in images.values() for url in links}) == 28
    assert len({url for links in pdfs.values() for url in links}) == 4
    assert {k: len(v) for k,v in groups.items()} == dict(general=6,domain_overviews=20,levels=224,activities=666,teacher_resources=20)
    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key','url','title','sha256','status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 936
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'],followup['listed_body_pending']) == (686,138)

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
        catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies':686, 'pending_activity_bodies':138},
        new_read_groups=dict(domain_overviews=0,levels=0,activities=22,teacher_resources=1,inline_images=0,supplementary_pdf_urls=0),
        geometry_3d_reading_log=logs, completed_geometry_3d_records=selected, geometry_3d_checked_examples=examples,
        geometry_3d_pdf_urls_not_reviewed=pdfs, geometry_3d_image_urls_not_reviewed=images,
        geometry_3d_separate_material_pending=[
            dict(page=pages[16]['url'], material='Counting Faces Chart', status='named_in_body_without_direct_document_link'),
            dict(page=pages[17]['url'], material='Shapes in Our School worksheet', status='named_in_body_without_direct_document_link'),
            dict(page=pages[18]['url'], material='Shapes in Our School worksheet', status='named_in_body_without_direct_document_link'),
            dict(page=pages[20]['url'], url='https://canva.link/7gq8w9nbcarg8lw', status='document_not_read'),
            dict(page=pages[20]['url'], url='https://www.perkins.org/resource/teaching-geometry-using-magnetic-tiles/',
                 status='cited_teaching_activity_not_reviewed'),
        ],
        reading_log=prior['reading_log'] + ['입체도형의 영어 활동 절차 22개와 교사자료 1개를 대조했다.'],
        source_corrections=prior['source_corrections'] + [dict(
            kind='solid_shape_faces_motion_and_net_conditions',
            locations=[pages[i]['url'] for i in (0,6,10,12,14,17,18,20,22)],
            action='한 면과 입체 전체, 평평한 면과 곡면, 이동 조건, 면 목록과 접을 수 있는 전개도를 구별했다.',
        )],
        unread_followups=prior['unread_followups'] + [LIMITS],
    )
    note_path = ROOT / NOTES
    write(note_path,notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=source['date'],read_scope=source['read_scope'])]
    source.update(
        date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
        bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
        method_note='물체의 한 면, 구름·미끄러짐, 평평한 면의 수, 전개도 조건을 영어 활동 본문과 대조했다.',
        editorial_action='문헌 대응 5건과 자체 관찰 과제 5개를 추가했다.', observations=source['observations'] + OBSERVATIONS,
    )
    for cid,codes,indices,support,limit in CLAIMS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
            locations=[pages[i]['url'] for i in indices], support=support, does_not_establish=limit,
            independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE])
    write(bibliography_path,bibliography)
    write(ROOT / 'data/literature_claim_reviews.json',registry)
    write(queue_path,queue)
    build_report()
    print('Reviewed 22 LT2 solid-shape activities and one teacher resource; added 5 claims and 5 observations.')


if __name__ == '__main__':
    main()

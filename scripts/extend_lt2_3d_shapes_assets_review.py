"""Record solid-shape print materials and correct their classification clues."""
import copy

from extend_lt2_composing_2d_assets_review import pdf_name, verified_assets
from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_3d_shapes_activities_review_notes.json'
PRIOR_SHA = 'd93d5b5184317bf8a09dcb582768f6376e03f9ed37c115fd4dd5ea73b3ee1be4'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_3d_shapes_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-3d-shapes-assets'
SCOPE = ('공개 영어 HTML 936개와 그중 활동·교사자료 686개를 확인했다. 목록에 138개가 남았다. '
         '입체도형의 연결 PDF 4개 URL·5쪽과 삽입 이미지 28개 URL을 대조했다.')
LIMITS = ('입체도형의 PDF와 페이지에 삽입된 사진·그림을 대조했다. 파라오 전개도의 별도 링크, '
          '문서 주소가 없는 활동지와 인용 자료, 실제 조작·수업 결과는 별도 범위다.')

PDF_NOTES = {
    '1603210825719': [([1], '영어 입체도형 카드 여덟 장이다. 정육면체와 정육면체가 아닌 직육면체가 게임의 서로 다른 카드다. 삼각기둥 그림은 밑면이 직각삼각형처럼 나타난다.')],
    '1603210917157': [([1], '여덟 도형의 속성 안내다. 직각삼각형을 밑면으로 하는 삼각기둥과 직각인 삼각형 면을 가진 각뿔을 배제하면 안 된다. 직육면체의 특수한 경우로 정육면체를 포함하고 원기둥의 밑면은 원판으로 확인한다.')],
    '1612485892986': [([1], '블록 놀이의 보조 인형·동물·탈것을 제안한다. 사진에는 휠체어·보행기·흰지팡이 등 여러 보조도구가 나온다.')],
    '1621435090382': [([1], '스페인어로 같은 여덟 종류의 입체 카드를 제시한다. 카드에서 도형을 구별하는 명칭과 수학의 범주 포함을 구별한다.'),
                       ([2], '인쇄 카드와 본문이 없는 빈 쪽이다.')],
}

CLAIMS = [
    ('LT148',['4수03-09','6수03-05'],['1603210825719','1603210917157'],
     '직각삼각형을 밑면으로 하는 삼각기둥에서는 두 밑면에도 직각이 있다. 삼각뿔이나 사각뿔의 옆면에 직각이 있는 경우도 가능하다.',
     '직각 유무를 도형 범주 전체를 규정하는 단서로 쓰지 않는다. 삼각기둥 카드에는 직각처럼 그려진 밑면도 보인다.'),
    ('LT149',['4수03-10','6수03-03'],['1603210825719','1603210917157','1621435090382'],
     '정육면체도 직육면체의 조건을 충족한다. 두 게임 카드를 구별하려면 다른 카드의 명칭을 정육면체가 아닌 직육면체로 구체화할 수 있다.',
     '모든 면이 정사각형이라는 단서는 정육면체를 식별하지만 정육면체를 직육면체의 범주에서 빼는 조건이 아니다.'),
    ('LT150',['6수03-07','6수03-08','6수03-11'],['1603210917157'],
     '곧은 원기둥의 옆면을 펼친 직사각형은 한 변이 밑면 원의 둘레이고 다른 변이 높이다. 두 밑면은 같은 크기의 원판이다.',
     '원판의 지름이나 넓이를 직사각형의 변 길이로 쓰지 않는다. 원기둥은 평평한 밑면 두 개와 곡면인 옆면으로 나누어 부른다.'),
]
OBSERVATION_DATA = [
    ('LT-P139','직각삼각형 두 장이 밑면인 곧은 삼각기둥을 생각한다. 두 밑면을 포함해 직각을 하나라도 가진 면은 몇 개인가?',
     '직사각형 옆면 세 개와 직각삼각형 밑면 두 개 모두 직각을 가져 다섯 개다.',
     '그림의 한 예에서 본 면의 각을 모든 삼각기둥의 성질로 적용하는지 확인한다.'),
    ('LT-P140','정육면체와 정육면체가 아닌 직육면체가 한 장씩 있다. 두 카드의 도형이 모두 직육면체인가? 두 카드를 구별할 질문을 하나 만든다.',
     '둘 다 직육면체다. 모든 면이 정사각형인지 물으면 정육면체 카드만 해당한다.',
     '상위 범주와 게임에서 카드 하나를 구별하는 추가 단서를 구분한다.'),
    ('LT-P141','밑면 반지름이 2 cm이고 높이가 5 cm인 원기둥의 옆면을 한 모선을 따라 자른다. 펼친 직사각형의 두 변의 길이를 말하라.',
     '밑면 둘레가 4π cm이고 높이가 5 cm이므로 두 변은 4π cm와 5 cm다. 지름 4 cm는 옆면의 한 변이 아니다.',
     '접합하는 경계의 길이가 원의 둘레에 대응한다고 설명하는지 확인한다.'),
]
OBSERVATIONS = [dict(id=oid,standard_codes=claim[1],question=question,expected=expected,
                     interpretation=interpretation,student_validated=False)
                for claim,(oid,question,expected,interpretation) in zip(CLAIMS,OBSERVATION_DATA,strict=True)]


def verify_examples():
    text = (CACHE/'1603210917157.txt').read_text(encoding='utf-8')
    assert all(marker in text for marker in (
        'Three faces have right angles, and two do not', 'No faces contain right angles',
        'Two faces may be square, but not all are', 'two circles and a rectangle',
    ))
    # Consecutive triangle edges meeting at the origin are perpendicular.
    xy = [(3,0),(0,4)]
    assert sum(a*b for a,b in zip(*xy)) == 0
    assert 3**2 + 4**2 == 5**2
    # Apex above a base vertex gives a right angle in each incident lateral triangle.
    apex_edge, base_edge = (0,0,2), (3,0,0)
    assert sum(a*b for a,b in zip(apex_edge,base_edge)) == 0
    return dict(right_triangle_legs=[3,4], hypotenuse=5, right_prism_faces_with_right_angles=5,
                pyramid_lateral_right_angle_incident_vectors=[apex_edge,base_edge],
                cylinder_net_radius=2, cylinder_net_height=5, cylinder_net_width_pi_coefficient=2*2)

IMAGE_NOTES = [
    ([0,1,2,3,4,6,7,8,10,11,14,16,17,20,22,23,25,26,27],
     '깡통·상자·구 모형·놀이 장면과 교구 그림이다. 0과 27은 같은 깡통 사진이다. 17은 모형을 다루는 장면이며 움직임이나 학습 결과는 이 사진만으로 정할 수 없다.'),
    ([5,9,15],
     '5는 같은 입체끼리 또는 다른 입체끼리 평평한 면을 맞추는 두 그림이다. 9는 추측용 카드의 예다. 15는 떨어져 그린 상자 면을 보여 주며 그대로 접는 전개도가 아니다.'),
    ([12,18,19,21],
     '12와 21은 학교에서 도형을 찾는 활동지의 구·정육면체 칸이 보이는 삽입 그림이다. 18은 분류판 소개, 19는 공간말 자료의 예다. 별도 배포 활동지 전체와 구별한다.'),
    ([13,24], '같은 아동용 그림책 표지 파일이다. 책 전체를 읽은 기록으로 세지 않는다.'),
]


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
    raw_pdfs, raw_images = [load(CACHE / f'{kind}-manifest.json') for kind in ('pdf','image')]
    assert len(raw_pdfs) == len(PDF_NOTES) == 4 and len(raw_images) == 28
    pdfs, images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images, PDF_NOTES, IMAGE_NOTES)
    assert asset_pairs(pdfs) == linked_pairs(prior['geometry_3d_pdf_urls_not_reviewed'])
    assert asset_pairs(images) == linked_pairs(prior['geometry_3d_image_urls_not_reviewed'])
    assert sum(a['pdf_pages'] for a in pdfs) == 5
    all_pdfs = prior['supplementary_pdf_read_manifest'] + pdfs
    all_images = prior['image_read_manifest'] + images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (173,608)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (159,552)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (934,907)
    assert images[0]['sha256'] == images[27]['sha256'] and images[13]['sha256'] == images[24]['sha256']
    names = {pdf_name(a['url']): a['url'] for a in pdfs}
    examples = verify_examples()

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(
        date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
        supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
        supplementary_pdf_coverage=dict(urls=173, page_occurrences=608, distinct_sha256_files=159,
                                        pages_after_file_deduplication=552, all_selected_pages_visual_reviewed=True,
                                        whole_site_attachment_review=False),
        pdf_exact_reuse_groups=reuse_groups(all_pdfs), geometry_3d_image_exact_reuse_groups=reuse_groups(images),
        geometry_3d_pdf_urls_not_reviewed={}, geometry_3d_image_urls_not_reviewed={},
        new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=28, supplementary_pdf_urls=4),
        geometry_3d_pdf_reading_log=pdf_notes, geometry_3d_image_reading_log=image_notes,
        geometry_3d_checked_attachments=examples,
        pdf_reading_log={**prior['pdf_reading_log'], **{
            url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows]
            for url, rows in pdf_notes.items()
        }},
        reading_log=prior['reading_log'] + ['입체도형의 PDF 4개 URL·5쪽과 이미지 28개 URL을 대조했다.'],
        source_corrections=prior['source_corrections'] + [
            dict(kind='solid_shape_attribute_guide', locations=[names['1603210917157']],
                 action='각기둥·각뿔의 직각 반례, 정육면체의 포함관계, 원기둥 밑면과 옆면 길이를 명시했다.'),
        ],
        unread_followups=prior['unread_followups'] + [LIMITS],
    )
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(
        date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
        bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
        method_note='속성 안내의 문구를 입체 카드와 반례, 원기둥의 접합 경계 길이로 대조했다.',
        editorial_action='문헌 대응 3건과 관찰 과제 3개를 추가했다.',
        image_read_manifest=all_images, supplementary_pdf_read_manifest=all_pdfs,
        observations=source['observations'] + OBSERVATIONS,
    )
    for cid, codes, filenames, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
            locations=[names[name] for name in filenames],
            support=support, does_not_establish=limit, independent_review=False, student_validated=False,
            target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE])
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Reviewed 4 LT2 PDF URLs, 5 pages and 28 images; added 3 claims and 3 observations.')


if __name__ == '__main__':
    main()

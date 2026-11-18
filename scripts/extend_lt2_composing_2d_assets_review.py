"""Record LT2 planar composition attachments and their mathematical checks."""
import copy
from pathlib import PurePosixPath
from urllib.parse import urlsplit

from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_ehrlich_levine_goldin_meadow_review import SOURCE as GESTURE_SOURCE
from record_lt2_public_review import SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_composing_2d_activities_review_notes.json'
PRIOR_SHA = 'e6bde61bb663d2900290e15c111899ad9056f7c824e375ccee7266480d00e3e5'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_composing_2d_assets_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-composing-2d-shapes-assets'
SCOPE = ('공개 영어 HTML 913개와 그중 활동·교사자료 663개를 확인했다. 목록에 161개가 남았다. '
         '평면도형 구성의 PDF 24개 URL·75쪽과 이미지 41개 URL을 대조했다. '
         '전체 누적 연결 PDF 169개 URL·603쪽과 삽입 이미지 906개 URL이다.')
LIMITS = ('인쇄 격자·윤곽과 본문의 조건을 비교했다. 실물 인쇄 크기나 수업 결과는 측정하지 않았다. '
          '별도 가정 자료, 영상, 펜토미노 퍼즐 본지, 나머지 인용 원문과 활동은 후속 범위다.')

PDF_NOTES = {
    '1575578554579': [([1], '정육면체 전개도에 여섯 결과 칸이 있다. 오각형 또는 육각형이 한 면을 공유한다.')],
    '1575578681666': [([1], '퀼트판은 3×3 빈 칸이다. 한 칸의 조각 구성과 9칸 전체 배열을 구별한다.')],
    '1575919281035': [([1], '격자 제목과 실제 칸은 가로 8칸·세로 10칸이다. 활동 본문이 묻는 8×12판과 크기가 다르다.')],
    '1581020074425': [([1,2,3], '오리, 돛단배, 동물 윤곽에 내부 경계가 없다.')],
    '1581020163036': [([1,2,3], '앞의 세 윤곽을 반복하며 조각 내부 경계를 표시한다.')],
    '1582220754762': [(list(range(1,7)), '여섯 구성 그림에 삼각형·직사각형·정사각형으로 나눈 선을 넣었다.')],
    '1582221054245': [(list(range(1,6)), '내부 안내선이 적은 다섯 그림이다. 일부 조각은 한 점으로 만나므로 모두 변을 공유한다고 해석하지 않는다.')],
    '1582221246601': [([1], '정육각형 윤곽을 점선으로 표시한 덮기판이다.')],
    '1582221570044': [([1], '정사각형을 자르는 세 그림과 안내가 있다. 점을 표시한 위치와 자를 선을 구별한다.')],
    '1587585892775': [(list(range(1,5)), '정렬한 두 조각과 같은 네 보기 윤곽을 비교한다.'),
                       (list(range(5,9)), '두 조각을 비껴 놓아도 네 보기 윤곽은 유지된다.')],
    '1587587013535': [(list(range(1,5)), '회전시킨 조각을 보고 네 보기에서 고른다.'),
                       (list(range(5,9)), '회전과 어긋남이 함께 있는 배치다.')],
    '1587587300749': [([1,2], '큰 사다리꼴 반쪽 두 장이다.'), ([3,4], '큰 삼각형 반쪽 두 장이다.'),
                       ([5,6], '뾰족한 윤곽의 반쪽 두 장이다.'), ([7,8], '불규칙한 윤곽의 반쪽 두 장이다.')],
    '1603212122784': [([1,2], '6×4 격자 네 개다. 전체 무늬를 넣을 판 하나와 반복 단위를 표시할 판 세 개가 있다.')],
    '1603212158297': [([1,2], '한 줄씩 색이 바뀌는 가로 줄무늬를 1×2, 2×2, 2×4 반복 블록으로 표현한다. 블록의 한 변의 길이와 해당 방향의 최소 주기를 구별한다.')],
    '1608667002625': [([1], '투입과 산출 카드로 규칙을 추론하는 안내다.'), ([2], '1~4번 카드다. 산출 카드에 육각형을 합동인 사다리꼴 둘로 나눈 예가 있다.'),
                       ([3], '5~8번 카드다. 8번 산출은 정육각형을 합동인 정삼각형 여섯으로 나눈다.'),
                       ([4], '9~12번 카드다. 11번 산출은 삼각형·마름모·사다리꼴, 12번 산출은 합동인 삼각형 셋과 사다리꼴이다.'),
                       ([5], '13~14번 카드다.'), ([6], '투입과 산출을 직접 그리는 빈 카드다.')],
    '1628018787050': [([1], '분할 선을 그릴 학생용 빈 정사각형 여섯 개다.')],
    '1628018807344': [([1], '교사용 정사각형 여섯 개에 서로 다른 내부 분할 선을 넣었다.')],
    '1628020201712': [([1], '사다리꼴 2개·정사각형 4개·삼각형 6개를 세 윤곽의 구성 재료로 나타낸다.')],
    '1628021821652': [([1], '안내와 표지다.'), ([2], '육각형을 자를 안내선이다.'), ([3], '꽃 윤곽이다.'),
                       ([4], '정사각형을 자를 안내선이다.'), ([5], '로켓 윤곽이다.')],
    '1642176155190': [([1], '펜토미노 과제 안내가 별도의 퍼즐 V~VIII를 언급한다. 퍼즐 본지는 이 파일에 없고, C/U와 M/W 표기는 모양을 돌려 보는 비교에 쓰인다.')],
    '1646854196532': [([1], '초기에는 첫 조각의 위치와 내부 경계를 제공하며 후반 14~18번은 바깥 윤곽만 남기는 퍼즐 안내다.')],
    '1649270639455': [([1], '영어 이야기와 수업 제안이다. 시작 장면의 네 정사각형과 세 원을 제목의 수와 혼동하지 않는다.')],
    '1663712017011': [([1,2], '스페인어 이야기와 수업 제안을 두 쪽으로 제시한다.')],
    '1710859578735': [([1], '투명지에 옮길 삼각형·정사각형·원 그림이 각각 세 개다.'),
                       ([2,3], '1단계 정사각형·삼각형 구성에서 떨어짐·포함·겹침을 나타낸다.'),
                       ([4,5,6], '2단계 원 구성에서 떨어짐, 접함, 일부 겹침, 중심이 같은 포함과 중심이 다른 포함을 비교한다. 링크의 페이지 매개변수는 4를 가리킨다.')],
}

IMAGE_NOTES = [
    ([0,1,2,3,4,5,6,7,12,13,17,19,20,23,24,25,26,27,32,38],
     '조각·도구 사진과 구성 장면이다. 사진으로 보이는 배치와 시행 횟수나 설명을 구분한다.'),
    ([8,9,10,11,14,18,21,22,36,37],
     '정사각형 배열, 테트로미노, 타일과 분할 그림이다. 9는 4×4 T 배치, 10은 3×2 퀼트 예, 37은 30칸으로 5칸 조각 6개를 만드는 예다.'),
    ([15,16,28,29,30,31,33,34,35,39,40],
     '반쪽을 회전하거나 이동하는 보기, 투명지와 탱그램의 도구·배치다. 30·39·40은 비슷하게 보이는 토끼 그림으로 파일은 서로 다르다.'),
]

CLAIMS = [
    ('LT139', ['4수01-05','4수03-12','6수03-13'], ['1575919281035'], [9],
     '첨부 8×10 격자는 80칸으로 네 칸 조각 20개가 필요하다. 본문의 8×12판은 96칸으로 24개가 필요하다.',
     '조각 수는 빈틈·겹침 없이 덮기 위한 필요조건이다. 작은 T자 배치 그림이나 이 계산만으로 다른 판을 덮을 수 있다고 결론 내리지 않는다.'),
    ('LT140', ['4수03-06','4수03-12','6수03-12'], ['1710859578735'], [28,35],
     '투명 원의 인쇄 보기에서 일부 겹침, 완전한 포함, 한 점에서 접함을 비교한다. 중심이 다른 두 원도 한 원판에 다른 원판이 완전히 들어갈 수 있다.',
     '본문의 6~16쪽 표기와 달리 연결 PDF는 6쪽이며 원 예시는 4~6쪽이다. 원판의 합집합 넓이는 양의 넓이만큼 겹칠 때 겹친 부분을 한 번 뺀다.'),
    ('LT141', ['2수02-01','2수02-02','6수03-13'], ['1603212122784','1603212158297','1575578681666'], [10],
     '가로로 같은 색, 세로로 두 색이 번갈아 나타나는 격자를 1×2 블록으로 반복할 수 있다. 같은 그림에서 2×2와 2×4도 반복 블록이 된다.',
     '가로 방향 최소 주기는 1칸이고 세로 방향은 2칸이다. 예에 나온 세 블록 중 하나만 허용하거나 퀼트 예의 크기를 모든 인쇄판에 적용하지 않는다.'),
    ('LT142', ['4수01-09','4수03-12','6수03-14'], ['1608667002625','1628020201712','1628021821652'], [21,22],
     '같은 정육각형을 합동인 사다리꼴 둘 또는 합동인 정삼각형 여섯으로 나누는 두 보기가 있다. 조각의 모양과 수는 달라도 겹침과 빈틈이 없으면 넓이의 합은 원래 넓이와 같다.',
     '각 보기는 카드가 지정한 분할이다. 가능한 모든 분할이거나 각 산출 카드의 조각이 항상 합동이라는 결론으로 확대하지 않는다.'),
]

OBSERVATION_DATA = [
    ('LT-P130', '가로 8칸·세로 10칸인 인쇄판과 8×12판에 네 칸 조각을 쓰려고 한다. 각각 몇 조각이 필요하며 그 수만으로 덮을 수 있는가?',
     '20개와 24개가 필요하다. 가능성을 보이려면 경계 안에서 겹침과 빈틈이 없는 배치를 추가로 제시해야 한다.',
     '판의 가로·세로를 읽고 구한 조각 수와 실제 덮기 가능성을 구별한다.'),
    ('LT-P131', '큰 원판 안에 작은 원판을 완전히 넣되 두 중심을 다르게 놓아라. 작은 원판의 위치를 옮겨 바깥에서 한 점만 접하게 하면 두 원판을 합친 넓이는 어떻게 달라지는가?',
     '완전히 포함하면 합친 넓이는 큰 원판의 넓이다. 바깥에서 한 점만 접하면 겹친 부분의 넓이가 0이므로 두 원판 넓이의 합이다.',
     '중심이 같은지와 포함되는지를 구별하며 경계에서 접하는 경우와 양의 넓이만큼 겹치는 경우를 따로 본다.'),
    ('LT-P132', '6×4 격자에서 한 행은 노란색, 다음 행은 파란색이고 이 순서를 반복한다. 가로 1칸·세로 2칸과 가로 2칸·세로 4칸 중 어느 블록을 반복해 같은 격자를 채울 수 있는가?',
     '둘 다 가능하다. 앞의 블록은 가로 여섯 번·세로 두 번, 뒤의 블록은 가로 세 번·세로 한 번 놓는다. 가로와 세로의 최소 주기는 각각 1칸과 2칸이다.',
     '반복할 수 있는 단위와 가장 작은 단위를 구별한다.'),
    ('LT-P133', '같은 크기의 정육각형 두 장을 각각 합동인 사다리꼴 둘과 합동인 정삼각형 여섯으로 자른다. 어느 분할에서 한 조각이 더 넓으며 모든 조각을 합하면 어느 쪽이 더 넓은가?',
     '사다리꼴 한 조각은 전체의 1/2, 작은 정삼각형 한 조각은 전체의 1/6이라 사다리꼴이 세 배다. 두 분할 모두 모든 조각 넓이의 합이 처음의 정육각형 넓이다.',
     '각 분할 내부에서 합동인 조각을 세어 전체에 대한 넓이 비를 설명한다.'),
]
OBSERVATIONS = [
    dict(id=oid, standard_codes=claim[1], question=question, expected=expected,
         interpretation=interpretation, student_validated=False)
    for claim, (oid, question, expected, interpretation) in zip(CLAIMS, OBSERVATION_DATA, strict=True)
]


def pdf_name(url):
    return PurePosixPath(urlsplit(url).path).stem


def verified_assets(raw_pdfs, raw_images, pdf_entries, image_groups):
    pdfs, images, pdf_notes = [], [], {}
    for row in raw_pdfs:
        pages = list(range(1, row['pdf_pages'] + 1))
        entries = pdf_entries[pdf_name(row['url'])]
        assert [p for group, _ in entries for p in group] == pages
        assert row['status'] == 200 and sha(ROOT / row['file']) == row['sha256']
        assert [a['pdf_page'] for a in row['renders']] == pages
        assert all(sha(ROOT / a['file']) == a['sha256'] for a in row['renders'])
        asset = {k: row[k] for k in ('url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'pdf_pages')}
        pdfs.append(dict(asset, read_kind='linked_pdf_content_and_visual_review', redistributed=False,
                         content_read_method='visual_pages_and_available_text', content_pdf_pages=pages, visual_pdf_pages=pages,
                         rendered_pages=[{k: a[k] for k in ('pdf_page', 'sha256')} for a in row['renders']]))
        pdf_notes[row['url']] = [dict(pdf_pages=group, note=note) for group, note in entries]
    for index, row in enumerate(raw_images):
        assert row['index'] == index and row['status'] == 200 and sha(ROOT / row['file']) == row['sha256']
        asset = {k: row[k] for k in ('url', 'page_url', 'linked_page_urls', 'status', 'content_type', 'sha256', 'dimensions')}
        images.append(dict(asset, read_kind='inline_image_visual_review', redistributed=False))
    assert sorted(i for group, _ in image_groups for i in group) == list(range(len(images)))
    return pdfs, images, pdf_notes, [dict(image_urls=[images[i]['url'] for i in group], note=note) for group, note in image_groups]


def verify_examples(names, raw_images, prior):
    assert (CACHE / '1575919281035.txt').read_text(encoding='utf-8').count('8 by 10 Grid') == 1
    assert names['1710859578735'].endswith('.pdf#page=4.00')
    assert 'Output 12' in (CACHE / '1608667002625.txt').read_text(encoding='utf-8')
    assert len({raw_images[i]['sha256'] for i in (30,39,40)}) == 3
    assert [(width * height) // 4 for width, height in [(8,10),(8,12)]] == [20,24]
    blocks = [(1,2),(2,2),(2,4)]
    grid = [[y % 2 for x in range(6)] for y in range(4)]
    for width, height in blocks:
        assert 6 % width == 0 and 4 % height == 0
        assert grid == [[grid[y % height][x % width] for x in range(6)] for y in range(4)]
    cited = prior['composing_2d_cited_works_pending']
    gesture = next(row for row in cited if row.get('url') == 'https://doi.org/10.1037/0012-1649.42.6.1259')
    return gesture, dict(
        grid_document=[8,10], grid_activity=[8,12], required_four_cell_tiles=[20,24],
        stripe_blocks_width_height=blocks, stripe_directional_minimum=[1,2],
        transformer_circle_pdf_pages=[4,5,6], transformer_circle_body_pages=[6,16],
    )


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
    raw_pdfs, raw_images = [load(CACHE / f'{kind}-manifest.json') for kind in ('pdf', 'image')]
    assert len(raw_pdfs) == len(PDF_NOTES) == 24 and len(raw_images) == 41
    pdfs, images, pdf_notes, image_notes = verified_assets(raw_pdfs, raw_images, PDF_NOTES, IMAGE_NOTES)
    assert asset_pairs(pdfs) == linked_pairs(prior['composing_2d_pdf_urls_not_reviewed'])
    assert asset_pairs(images) == linked_pairs(prior['composing_2d_image_urls_not_reviewed'])
    assert sum(a['pdf_pages'] for a in pdfs) == 75
    all_pdfs = prior['supplementary_pdf_read_manifest'] + pdfs
    all_images = prior['image_read_manifest'] + images
    unique_pdfs = {a['sha256']: a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs), sum(a['pdf_pages'] for a in all_pdfs)) == (169,603)
    assert (len(unique_pdfs), sum(unique_pdfs.values())) == (155,547)
    assert (len(all_images), len({a['sha256'] for a in all_images})) == (906,881)
    names = {pdf_name(a['url']): a['url'] for a in pdfs}
    gesture, checked_examples = verify_examples(names, raw_images, prior)
    gesture_record = registry['sources'][GESTURE_SOURCE]

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
        supplementary_pdf_coverage=dict(urls=169, page_occurrences=603, distinct_sha256_files=155,
                                        pages_after_file_deduplication=547, all_selected_pages_visual_reviewed=True,
                                        whole_site_attachment_review=False),
        pdf_exact_reuse_groups=reuse_groups(all_pdfs),
        composing_2d_pdf_urls_not_reviewed={}, composing_2d_image_urls_not_reviewed={},
        new_read_groups=dict(domain_overviews=0, levels=0, activities=0, teacher_resources=0, inline_images=41, supplementary_pdf_urls=24),
        composing_2d_pdf_reading_log=pdf_notes, composing_2d_image_reading_log=image_notes,
        composing_2d_checked_attachments=checked_examples,
        composing_2d_cited_works_pending=[row for row in prior['composing_2d_cited_works_pending'] if row != gesture],
        composing_2d_cited_works_reviewed=[dict(
            gesture, read_scope=gesture_record['read_scope'], source_id=GESTURE_SOURCE,
            snapshot_file=gesture_record['snapshot_file'], snapshot_sha256=gesture_record['snapshot_sha256'],
            connection='첨부의 네 보기 선택과 종이 조각을 손으로 합치는 과제를 구별했다. 원연구의 손짓은 답을 고른 뒤에 기록됐다.',
        )],
        pdf_reading_log={**prior['pdf_reading_log'], **{
            url: [f"{', '.join(map(str, row['pdf_pages']))}쪽. {row['note']}" for row in rows]
            for url, rows in pdf_notes.items()
        }},
        reading_log=prior['reading_log'] + ['평면도형 구성의 PDF 24개 URL·75쪽과 이미지 41개 URL을 대조했다.'],
        source_corrections=prior['source_corrections'] + [
            dict(kind='print_grid_size_and_pdf_page_range', locations=[names['1575919281035'], names['1710859578735']],
                 action='인쇄판 8×10과 활동 본문 8×12, 원 예시의 실제 4~6쪽과 본문의 6~16쪽 표기를 구별했다.'),
        ],
        unread_followups=[LIMITS, '남은 입체도형과 공간 활동, 연결 인용의 출판 본문을 대조한다.'],
    )
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(
        date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
        bibliography_snapshot=digest(entry), read_scope=SCOPE, limits=LIMITS,
        method_note='본문과 인쇄 격자·반복 블록·분할 카드·투명지 도안을 대조하고 관련 실험의 과제 범위를 확인했다.',
        editorial_action='문헌 대응 4건과 관찰 과제 4개를 추가했다.',
        image_read_manifest=all_images, supplementary_pdf_read_manifest=all_pdfs,
        observations=source['observations'] + OBSERVATIONS,
    )
    for cid, codes, filenames, indices, support, limit in CLAIMS:
        registry['claims'].append(dict(
            id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
            locations=[names[name] for name in filenames] + [images[i]['url'] for i in indices],
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
    print('Reviewed 24 LT2 PDF URLs, 75 pages and 41 images; added 4 claims and 4 observations.')


if __name__ == '__main__':
    main()

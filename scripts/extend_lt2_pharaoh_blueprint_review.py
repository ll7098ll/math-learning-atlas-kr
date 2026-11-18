"""Register the four separately viewed LT2 Pharaoh blueprint pages."""
import copy

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_3d_shapes_assets_review_notes.json'
PRIOR_SHA = '68454aad95f535d07da297f872d26b243787c80add833a745efe5cc31bf1144d'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_pharaoh_blueprint_review_notes.json'
ACTIVITY = 'https://www.learningtrajectories.org/math-activities/the-pharaohs-prism'
SHORT_LINK = 'https://canva.link/7gq8w9nbcarg8lw'
VIEWER = 'https://www.canva.com/design/DAHC1-9m_Hk/yD1qMNRMsO7vCqWnY1fCDA/view?utm_content=DAHC1-9m_Hk&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h5c13a420c0'
CODES = ['6수03-05','6수03-06']
SCOPE = ('공개 영어 HTML 936개와 그중 활동·교사자료 686개, 연결 PDF 173개 URL·608쪽과 이미지 934개 URL을 대조했다. '
         '입체도형의 파라오 도안은 별도 공개 뷰어 네 쪽을 확인했다.')
LIMITS = ('파라오 도안의 표지·모형·배열·기록지를 공개 보기에서 확인했다. 실물 접기나 수업 검증, '
          '별도 활동지와 인용한 Perkins 자료의 그림 비교, 나머지 138개 영어 활동은 후속 범위다.')
OBSERVATION = dict(
    id='LT-P142', standard_codes=CODES,
    question='두 정삼각형이 같은 정사각형의 서로 이웃한 두 변에 하나씩 붙어 있다. 이 연결을 유지하면서 정사각형을 옆면으로, 두 삼각형을 서로 다른 밑면으로 하는 삼각기둥을 접을 수 있는가?',
    expected='접을 수 없다. 삼각기둥의 두 밑면은 떨어져 있으며, 같은 옆면과 각각 만나는 두 모서리는 서로 마주 보아야 한다. 이웃한 변을 접는다고 마주 보는 변으로 바뀌지는 않는다.',
    interpretation='면의 개수가 맞는지와 한 옆면에서 밑면에 연결되는 변이 서로 마주 보는지를 각각 설명하게 한다.',
    student_validated=False,
)


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        assert source['snapshot_sha256'] == sha(ROOT / NOTES)
        assert source['observations'][-1] == OBSERVATION
        build_report()
        return
    assert source['snapshot_file'] == PRIOR and sha(ROOT / PRIOR) == PRIOR_SHA
    prior = load(ROOT / PRIOR)
    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE,next_review=LIMITS)
    pages = [
        '표지의 학습목표는 각뿔을 적고 제목과 모형 그림은 삼각기둥을 나타낸다. 2~4쪽 안내도 삼각기둥을 지목한다.',
        '삼각기둥의 두 밑면, 면 5개·모서리 9개·꼭짓점 6개를 표시한다. 활동 본문의 선택 자료에는 삼각뿔이라고 적혀 있으나 이 쪽 제목과 그림은 삼각기둥이다. 그림의 영어 꼭짓점 단수는 vertex로 적는다.',
        'A~H의 여덟 배열이다. C의 두 삼각형은 같은 정사각형의 서로 이웃한 변에 붙어 있다. E는 정사각형 세 개의 띠 양쪽 경계에 삼각형을 달았다. G는 한 삼각형이 옆면 띠가 닫히는 경계에 붙어 있다.',
        'A~H를 두 줄의 기록 칸으로 반복한다. 기록지의 질문은 삼각기둥으로 접히는지 묻는다.',
    ]
    assert (2+3,3+3+3,3+3)==(5,9,6)
    pending = prior['geometry_3d_separate_material_pending']
    matched = [row for row in pending if row.get('url')==SHORT_LINK]
    assert len(matched)==1
    notes = dict(prior)
    notes.update(
        date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA,
        new_read_groups=dict(domain_overviews=0,levels=0,activities=0,teacher_resources=0,inline_images=0,supplementary_pdf_urls=0),
        geometry_3d_separate_material_pending=[row for row in pending if row not in matched],
        geometry_3d_separate_material_reviewed=[dict(
            url=SHORT_LINK, viewer_url=VIEWER, linking_page=ACTIVITY, read_kind='public_viewer_visual_and_visible_text',
            source_redistributed=False, visual_pages=list(range(1,5)),
            page_notes=[dict(page=i,location=f'{VIEWER}#{i}',note=note) for i,note in enumerate(pages,1)],
            source_answer_key=['A','B','D','E'],
            layout_conditions_checked_by_reviewer={'C':'같은 정사각형의 서로 이웃한 변에 각각 연결', 'E':'띠의 서로 다른 끝을 닫음', 'F':'옆면 연결 변의 맞은편에 삼각형을 붙임', 'G':'띠의 연결 모서리에 삼각형을 붙임', 'H':'옆면 연결 변의 맞은편에 삼각형을 붙임'},
        )],
        source_corrections=prior['source_corrections'] + [
            dict(kind='blueprint_prism_pyramid_mismatch',locations=[ACTIVITY,f'{VIEWER}#1',f'{VIEWER}#2'],
                 action='표지와 본문의 각뿔 표기에도 불구하고 도안과 기록지의 목표는 삼각기둥이다.'),
        ],
        reading_log=prior['reading_log'] + ['파라오 삼각기둥 공개 뷰어의 표지·모형·배열·기록지 네 쪽을 대조했다.'],
        unread_followups=prior['unread_followups'] + [LIMITS],
    )
    note_path = ROOT / NOTES
    write(note_path,notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=source['date'],read_scope=source['read_scope'])]
    source.update(
        date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(note_path),snapshot_history=history,
        bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,
        method_note='입체도형 본문과 인쇄물에 이어 공개 뷰어에서 표지·모형·도안·기록지를 읽었다.',
        editorial_action='도안의 삼각기둥·삼각뿔 표기를 대조해 근거 1건과 관찰 과제 1개를 반영했다.',
        observations=source['observations']+[OBSERVATION],
    )
    registry['claims'].append(dict(
        id='LT151',source_id=SOURCE,role='related_theoretical_context',standard_codes=CODES,
        locations=[ACTIVITY]+[f'{VIEWER}#{page}' for page in range(1,5)],
        support='도안의 목표는 합동이고 평행한 삼각형 두 개가 양 끝을 닫는 삼각기둥이다. C의 두 삼각형은 같은 정사각형의 이웃한 두 변에 붙어 있다. 두 밑면은 같은 옆면의 마주 보는 두 변에서 만나야 하므로 C는 이 연결을 유지해 접을 수 없다.',
        does_not_establish='표지의 각뿔 표기는 모형·기록지의 삼각기둥과 다르다. 본문의 전체 해답과 직접 조건을 검산한 도안을 구별한다.',
        independent_review=False,student_validated=False,
        target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in CODES},
    ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id']==SOURCE)
    row.update(source=entry,claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id']==SOURCE])
    write(bibliography_path,bibliography)
    write(ROOT/'data/literature_claim_reviews.json',registry)
    write(queue_path,queue)
    build_report()
    print('Reviewed the four Pharaoh blueprint pages; added 1 claim and 1 observation.')


if __name__ == '__main__':
    main()

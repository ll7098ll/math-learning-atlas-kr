"""Apply a bounded reading of the seventh international edition transcription."""
import copy
import hashlib
import json
from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


SOURCE = 'DICK_CAREY_2014'
NOTES = 'data/literature_evidence/DICK_CAREY_2014_subskills_context_review_notes.json'
TRANSCRIPT = 'tmp/dick-carey-7-international-candidate-20261109.html'
TRANSCRIPT_URL = ('https://dokumen.pub/systematic-design-of-instruction-an-introductory-text-for-the-21st-century-'
                  '7th-ed-1292041250-1269374508-9781292041254-9781269374507-9781292052663-129205266x.html')
TRANSCRIPT_SHA = 'ad64b171d9b7d02d6eb0172727c770a6128ac1708afcb334313dd4f53d924bf2'
SCOPE = ('공식 미리보기·발췌 46쪽 추출문과 선정 23쪽 이미지에 더해, 동일 인쇄 ISBN의 비공식 HTML 전사본에서 '
         '국제판 47~61쪽 및 71~73쪽의 하위·출발 기능 분석과 79~87쪽의 학습자·맥락 분석 중 선정 대목을 대조했다.')
LIMIT = ('전사본에서 읽은 선정 본문과 공식 PDF의 이미지 대조 범위를 구분한다. 공식 판면, 도식의 연결선과 '
         '전사본의 전체 동일성, 인용 원연구, 국내 과제의 진단 정확도와 효과는 확인 전이다.')

# Claim, endpoint codes, international edition location, bounded support, limit.
MAPPINGS = [
    ('DC07', ['2수03-10', '2수03-12'], '국제판 50~52쪽, 선형 눈금 읽기 본문과 그림 4.3·4.4 설명',
     '측정값을 얻는 절차와 어림의 기준 길이를 실제로 알아보는 기능을 분리해 관찰한다. 같은 기능도 과제에서 취한 절차에 따라 다르게 배열할 수 있다.',
     '원문의 십분·백분 눈금 과제를 국내 저학년 요구로 추가하지 않는다. 전사본에서 도식 연결선을 판면으로 확인하지 않았다.'),
    ('DC08', ['2수01-02', '2수01-06'], '국제판 51~53쪽·71~73쪽, 하위 절차와 하위 기능 및 분석 점검',
     '받아내림 절차에서 일어나는 십의 교환을, 계산 전에 별도로 확인할 수 있는 양 보존 설명과 구분한다. 필요 여부는 주어진 풀이와 과제로 한정한다.',
     '한 풀이를 분석한 결과로 보상 전략을 배제하거나 자릿값 기준 전체를 뺄셈의 필수 선수로 설정하지 않는다.'),
    ('DC09', ['4수03-08', '4수03-09'], '국제판 53~54쪽·56~58쪽, 절차·정보 묶음과 독립 기능',
     '이름을 기억하는 일, 변 길이를 기준으로 분류하는 일, 각 크기를 기준으로 분류하는 일을 따로 확인한다. 같은 삼각형에 서로 다른 기준의 이름을 붙일 수 있다.',
     '이름이나 상자 번호의 배열에서 두 분류의 학습 순서를 도출하지 않는다. 제시한 각을 비교하는 과제로 한정하며 미지각 계산을 추가하지 않는다.'),
    ('DC10', ['4수01-06'], '국제판 57~61쪽, 도식 번호·출발 기능 경계와 여러 시작점',
     '나눗셈의 부분 배분, 남은 양의 검산, 교사가 이미 안다고 가정한 곱셈 기능을 분리한다. 선택한 풀이에서 실제로 사용한 기능을 답과 함께 기록한다.',
     '올바른 몫으로 암산이나 유일한 계산 절차를 확인했다고 판단하지 않는다. 시작점은 실제 초기 반응에 따라 검토할 설계 가정이다.'),
    ('DC11', ['6수04-01'], '국제판 58~61쪽·79~82쪽, 잠정적 출발 기능과 사전 수행 자료',
     '균등화 활동 전에 합을 보존하는 이동을 독립적으로 설명하는지 관찰하고, 단서 뒤 수행과 나누어 기록하는 데 참고한다.',
     '가상 예나 자기보고만으로 출발 기능을 확인하지 않는다. 평균 계산에 조작 활동의 선행을 일률적으로 요구하지 않는다.'),
    ('DC12', ['4수03-15', '4수03-16'], '국제판 82~87쪽, 수행·학습 맥락의 물리적 조건과 학교 적용',
     '연습에서 제공한 눈금이나 경로 자료와 실제 측정에서 주어진 도구를 각각 기록한다. 단위 교환과 같은 길이의 끝점을 정하는 측정 수행을 구별한다.',
     '단위 환산을 맞힌 결과를 실제 길이 측정, 축척 해석이나 다른 도구에서의 전이 검증으로 합산하지 않는다.'),
    ('DC13', ['9수03-15'], '국제판 79~82쪽·86~87쪽, 목표 집단과 시범 참여자 및 분석의 예비 점검',
     '직각 조건의 확인, 수치 적용, 일반 정당화를 별도 수행으로 정의한다. 제시한 도식과 단서, 최초 설명을 구별하고 새 예에서 설명을 다시 확인할 수 있다.',
     '예비 점검 절차는 실제 참여자나 정리의 교수 효과에 대한 근거가 아니다. 한 삼각형의 계산은 일반 정당화를 입증하지 않는다.'),
]


def probe(suffix, codes, question, expected, interpretation):
    return dict(id=f'DC-P{suffix}', standard_codes=codes, question=question, expected=expected,
                interpretation=interpretation, student_validated=False)


OBSERVATIONS = [
    probe(7, MAPPINGS[0][1], '실제로 확인한 10cm 띠를 책의 긴 변에 대기 전에 눈으로 비교한다. 두 번과 세 번 중 어느 쪽에 가까울지 예상하고, 이후 자의 3cm와 27cm 눈금에 양 끝이 놓였을 때 실제 길이를 설명한다.',
          '재고 나면 두 끝 사이가 27−3=24cm다. 24cm는 20cm와 4cm 차이, 30cm와 6cm 차이이므로 두 번 쪽에 가깝다. 재기 전 예상에서 사용한 기준은 따로 설명한다.',
          '재기 전 답과 이유, 기준 띠를 실제로 댄 뒤 답, 눈금으로 재고 난 답을 구분한다. 27cm라는 끝 눈금만 읽으면 시작을 어디로 잡았는지 다시 묻는다.'),
    probe(8, MAPPINGS[1][1], '십 하나와 일 열 개가 같은 양인지 설명한다. 그 뒤 52−28에서 십을 교환하는 풀이와 30을 빼는 풀이를 비교한다.',
          '52는 5십 2일이나 4십 12일로 나타낼 수 있다. 교환 뒤 빼면 2십 4일이다. 30을 먼저 빼면 2를 더 많이 뺐으므로 52−30+2=24로 보상한다.',
          '십 교환을 보여 주기 전 반응과 이후 설명을 구별한다. 가르쳐 준 뒤에는 61−27 같은 새 수로 확인하고, 보상으로 풀면 그 이유를 별도로 남긴다.'),
    probe(9, MAPPINGS[2][1], '두 변의 길이가 같은 두 삼각형이 있다. 각은 각각 45°, 45°, 90°와 40°, 40°, 100°라고 주어졌다. 두 삼각형을 변의 길이와 각의 크기로 각각 분류한다.',
          '두 삼각형 모두 이등변삼각형이다. 첫째는 직각삼각형이고 둘째는 둔각삼각형이다. 각각의 이름에서 사용한 기준을 말한다.',
          '변 길이 조건과 각 크기는 제시한다. 이등변삼각형의 성질을 정당화하거나 미지각을 계산하는 수행은 이 분류 문항에서 평가하지 않는다.'),
    probe(10, MAPPINGS[3][1], '67개를 다섯 모임에 똑같이 나눈다. 50개, 15개 순서로 나눌 수 있는지 살펴보고, 67=5×12+7만으로 몫이 12라고 할 수 있는지 설명한다.',
          '각 모임에 10개와 3개를 주면 2개가 남아 몫은 13이다. 67=5×12+7은 맞지만 남은 7개 중 5개를 다시 나눌 수 있으므로 최종 나머지가 될 수 없다.',
          '실물 배분, 부분 몫, 반복 뺄셈 중 선택한 방법과 나머지 조건을 기록한다. 교사가 제시한 부분 몫을 그대로 쓴 반응과 처음부터 직접 선택한 반응을 구별한다.'),
    probe(11, MAPPINGS[4][1], '자료 2, 6, 10을 계산으로 평균 내고, 말의 이동으로 각 값이 평균과 같아지는 이유도 설명한다. 교사가 이동할 양을 말해 줬다면 기록에 무엇을 남기는가?',
          '합 18을 자료 세 개에 나누어 평균은 6이다. 10에서 2 쪽으로 4개를 옮기면 6, 6, 6이고 합과 자료 수가 유지된다.',
          '계산, 총량 보존 설명, 도움 종류를 따로 기록한다. 자료를 직접 수집하는 수행이나 보존의 독립 설명을 계산 정답에서 추정하지 않는다.'),
    probe(12, MAPPINGS[5][1], '띠의 길이 기록 3cm 7mm와 걸은 길이 기록 2km 350m를 각각 단일 단위로 나타낸다. 같은 거리를 실제로 확인할 때 어느 두 끝과 어떤 도구를 정해야 하는지도 말한다.',
          '3cm 7mm는 37mm이고 2km 350m는 2350m다. 띠는 양쪽 끝 사이를 재고, 걸은 길이는 정한 출발점부터 도착점까지 실제로 따른 경로를 대상으로 한다.',
          '교실에서 환산한 결과와 현장에서 잰 결과를 구별한다. 도구가 경로 길이와 두 점 사이 직선거리를 어느 쪽으로 제공하는지 확인한다.'),
    probe(13, MAPPINGS[6][1], '직각변 8cm와 15cm로 빗변을 구한다. 이어 직각변 a, b인 합동 직각삼각형 네 개를 바깥 정사각형에 배치하는 도식에서 안쪽 도형이 정사각형인 이유와 넓이 관계를 설명한다.',
          '빗변은 양의 길이 17cm다. 안쪽 네 변은 같은 빗변이고 인접한 두 예각의 합이 90°여서 안쪽 각도 직각이다. 넓이는 (a+b)²−4×ab/2=a²+b²로, 안쪽 정사각형의 넓이 c²와 같다.',
          '수치 계산, 안쪽 도형의 정당화, 넓이 관계를 따로 본다. 배치가 주어졌는지 직접 구성했는지와 단서 여부를 기록한다.'),
]

RELATIONS = [
    ('REV-2수03-12-1', 'DC07', '10cm를 기준으로 어림하는 과제에서는 기준 길이를 알아보는 수행과 두 끝의 눈금 차로 측정하는 수행을 따로 본다.',
     '손뼘처럼 다른 기준을 쓰는 어림을 배제하지 않는다. 원문의 십분·백분 눈금은 현재 과제의 조건으로 옮기지 않는다.'),
    ('REV-2수01-06-1', 'DC08', '십을 풀어 빼는 경로에서는 교환 전후 양을 확인한다. 52에서 30을 빼고 2를 더하는 경로에는 같은 교환 절차가 등장하지 않는다.',
     '설계 분석은 교환 풀이에서 사용할 기능을 밝힌다. 공식 자릿값 기준 전체를 필수 선수로 바꾸지 않는다.'),
    ('REV-4수03-09-2', 'DC09', '같은 삼각형에서 두 변이 같은지와 직각이 있는지를 독립적으로 확인한다. 이등변 직각삼각형은 두 분류에 모두 속한다.',
     '분류의 질문 순서에서 분류 기준 간 선수 관계를 도출하지 않는다. 각의 크기는 비교 자료로 제공한다.'),
    ('REV-4수03-16-1', 'DC12', '측정한 구간이나 경로를 고정한 뒤 3cm 7mm와 37mm, 2km 350m와 2350m가 같은 길이인지 확인한다.',
     '기록 단위를 바꿔도 측정 대상이 같아야 한다. 직선거리와 실제 경로가 다르면 환산으로 그 차이가 없어지지 않는다.'),
]


def write(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        build_report()
        return

    asset = (ROOT / TRANSCRIPT).read_bytes()
    assert len(asset) == 1382505 and hashlib.sha256(asset).hexdigest() == TRANSCRIPT_SHA
    assert 27 - 3 == 24 and abs(24 - 20) < abs(24 - 30)
    assert 52 == 40 + 12 and 52 - 28 == 52 - 30 + 2 == 24 and 61 - 27 == 34
    assert sum((45, 45, 90)) == sum((40, 40, 100)) == 180
    assert divmod(67, 5) == (13, 2) and 5 * 12 + 7 == 67 and 7 >= 5
    assert sum((2, 6, 10)) == 3 * 6 and (2 + 4, 6, 10 - 4) == (6, 6, 6)
    assert 3 * 10 + 7 == 37 and 2 * 1000 + 350 == 2350
    assert 8 ** 2 + 15 ** 2 == 17 ** 2

    previous = copy.deepcopy(source)
    prior_notes = read(ROOT, previous['snapshot_file'])
    assert previous['snapshot_sha256'] == '799ee7529eafaf13f530c768f4b2da5c8237189d3ab53a477676e7eed4e1e848'
    bibliography = read(ROOT, 'data/sources.json')
    book = next(row for row in bibliography if row['id'] == SOURCE)
    prior_book = copy.deepcopy(book)
    book.update(kind='교수설계 원전의 공식 미리보기·발췌와 같은 ISBN의 비공식 전사본 선정 대조',
                review_scope=SCOPE, next_review=LIMIT + ' 목표 분석 뒷부분과 다른 장·부록의 미검토 본문을 이어서 대조한다.')
    notes = dict(prior_notes, date='2026-11-09', read_scope=SCOPE,
                 previous_review=previous, previous_bibliography=prior_book,
                 transcript=dict(url=TRANSCRIPT_URL, bytes=len(asset), sha256=TRANSCRIPT_SHA, format='html',
                                 status='unofficial_transcription', redistributed=False,
                                 official_preview_matching_8grams=[17108, 18215],
                                 publisher_extract_matching_8grams=[2070, 2367],
                                 page_layout_verified=False, whole_edition_verified=False))
    notes['reading_log'] += [
        '국제판 47~61쪽과 71~73쪽의 선정 본문에서 눈금 읽기, 절차와 하위 기능, 독립 기능, 잠정적 출발선과 분석 수정의 설명을 확인했다.',
        '국제판 79~87쪽의 선정 본문에서 목표 집단과 시범 참여자, 자기보고와 사전 수행, 학습과 수행의 맥락, 분석의 예비 점검을 구별했다.',
    ]
    notes['source_corrections'] += [
        dict(kind='chapter_number_and_layout', location='공식 미리보기 PDF 4~5쪽과 HTML 차례 및 본문',
             action='공식 미리보기와 HTML 차례에서 하위 기능 분석은 세 번째 항목이고 본문은 원서 4장이라고 표기한다. 상품 목차의 장 번호와 구별하고 HTML의 줄 순서에서 도식의 연결선을 복원하지 않는다.'),
    ]
    notes['unread_followups'] = [book['next_review'], '현재 과제의 실제 독립 검토와 익명 학생 응답을 별도 증거로 확인한다.']
    notes_text = json.dumps(notes, ensure_ascii=False, indent=2) + '\n'
    source.update(date='2026-11-09', snapshot_file=NOTES, snapshot_sha256=hashlib.sha256(notes_text.encode()).hexdigest(),
                  snapshot_history=[{key: previous[key] for key in ('snapshot_file', 'snapshot_sha256', 'date', 'read_scope')}],
                  bibliography_snapshot=digest(book), read_scope=SCOPE, limits=LIMIT,
                  method_note='출판사 미리보기와 발췌의 겹치는 본문을 전사본과 대조하고, 국제판과 원서의 장·쪽 번호를 구별했다.',
                  editorial_action='새 주장 7건과 가상 관찰 7건을 성취기준 11개에 대응했다. 그중 4개 관계에 설계 적용 범위를 기록했다.',
                  observations=previous['observations'] + OBSERVATIONS)
    assert len({code for _, codes, *_ in MAPPINGS for code in codes}) == 11
    assert len({row['id'] for row in source['observations']}) == 13
    claims = {}
    for cid, codes, location, support, limit in MAPPINGS:
        claims[cid] = dict(id=cid, source_id=SOURCE, role='related_theoretical_context',
                           locations=[f'비공식 HTML 전사본 · {location}'], support=support, does_not_establish=limit,
                           target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
                           standard_codes=codes, independent_review=False, student_validated=False)
    assert set(claims).isdisjoint({r['id'] for r in registry['claims']})
    registry['claims'].extend(claims.values())

    relations = read(ROOT, 'data/revised_relations.json')['relations']
    by_id = {row['id']: row for row in relations}
    relation_reviews = read(ROOT, FILE)
    new_pairs = {(rel['id'], claim['id'])
                 for rel in relations for claim in claims.values()
                 if all(rel[k].startswith('standard:') for k in ('from', 'to'))
                 and {rel[k][9:] for k in ('from', 'to')} <= set(claim['standard_codes'])}
    assert new_pairs == {(rid, cid) for rid, cid, *_ in RELATIONS}
    for rid, cid, finding, limit in RELATIONS:
        relation_reviews['records'].append(dict(
            relation_id=rid, claim_id=cid, role='activity_context', finding=finding, limit=limit,
            relation_snapshot=relation_snapshot(by_id[rid]), claim_snapshot=claim_snapshot(claims[cid], source),
        ))
    apply_literature_context(relations, registry, registry=relation_reviews)

    queue_path = 'data/content_review_queue.json'
    queue = read(ROOT, queue_path)
    item = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    item.update(source=book, claim_ids=[row['id'] for row in registry['claims'] if row['source_id'] == SOURCE])
    (ROOT / NOTES).write_text(notes_text, encoding='utf-8', newline='\n')
    write('data/sources.json', bibliography)
    write('data/literature_claim_reviews.json', registry)
    write(FILE, relation_reviews)
    write(queue_path, queue)
    build_report()
    print('Seventh international edition: 7 claims, 7 observation designs, 4 relation records')


if __name__ == '__main__':
    main()

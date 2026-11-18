"""Extend the licensed algebra guide's reading record and classroom mappings."""
import copy
import hashlib
import json

from literature_review import ROOT, build_report, digest, load_registry, read, target_value
from record_ies_algebra_literature_review import RATINGS, SHA, SOURCE
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot

NOTES = 'data/literature_evidence/IES_ALGEBRA_2015_full_review_notes.json'
PROTOCOL = 'tmp/literature/wwc-algebra-protocol-v3.pdf'
PROTOCOL_SHA = 'bd35777b98f253a35f3967f76610a7b6094742e81a1119a1b60815c449d15853'
VISUAL = [13, 17, 28, 29, 38, 48, 55, 57, 58, 61, 62, 63, 70]
MAPPINGS = [
    ('IA07', ['9수02-03', '9수02-20'], 1, 'PDF13,17,20–21 / 인쇄7,11,14–15, 예 1.3·1.7·1.10',
     '완전제곱 풀이에서 양변을 다르게 바꾼 오류와 음의 제곱근을 빠뜨린 오류를 구별한다. 완성 예의 설명과 도움 없는 새 풀이를 따로 기록한다.',
     '권고1은 Minimal이다. 사례 비교는 안내 방식이며 오류 유형 하나로 학생의 사고 원인을 확정할 수 없다.'),
    ('IA08', ['9수02-20', '9수02-22'], 2, 'PDF28–29 / 인쇄22–23, 예 2.8',
     '전체 넓이와 두 부분 넓이의 합을 도형과 식으로 대응시킨다. 이차식의 영점 두 개와 길이 조건을 만족하는 값 하나를 구별한다.',
     '권고2는 Minimal이다. 여러 표현을 정해진 순서로 모두 거칠 필요는 없다. 모든 실수에서 정의한 보조 함수와 길이의 허용 범위를 구별한다.'),
    ('IA09', ['9수02-13', '9수02-18'], 3, 'PDF38–42 / 인쇄32–36, 예 3.6–3.9 및 PDF68 미주41',
     '변수가 이미 고립돼 있으면 대입, 계수의 절댓값이 같고 부호가 반대면 가감, 절편을 쉽게 찾으면 그래프를 후보로 살핀다. 교점이 두 조건을 만족하는지 원식에 대입한다.',
     '권고3은 Moderate이다. 예 3.6의 그래프·대입·가감은 각각 다른 연립식에 붙은 사례다. 크라메르 공식은 중학교 성취기준 범위 밖이며 눈금으로 읽은 교점은 근삿값일 수 있다.'),
    ('IA10', ['9수02-04'], 3, 'PDF61–64 / 인쇄55–58, 표 D.4 및 각주 d·g·i–r',
     '같은 일차방정식에 여러 방법을 쓰는 비교와 여러 식에 같은 방법을 쓰는 비교를 구별한다. 전략을 설명하는 반응과 새 문제에서 전략을 고르는 반응을 따로 살핀다.',
     '권고3은 Moderate이다. 2012년 연구의 124명 비교에서 절차 유연성 0.37에만 영역 수준의 유의 표시가 있다. 높은 탈락률이 있었던 다른 115명 비교와는 조건이 달랐고 대조군을 공유했다. 현재 과제의 효과는 검증 대기다.'),
    ('IA11', ['9수02-15', '9수02-16'], 2, 'PDF29 / 인쇄23 예 2.9, PDF58–59 / 인쇄52–53 표 D.3',
     '고정량과 단위당 증가량이 더해지는 관계를 막대 도식·표·식에서 대응시킨다. 처음 값과 두 입력 사이 변화율, 입력의 허용 범위를 각각 묻는다.',
     '권고2는 Minimal이다. 도식 기반 지도, 애니메이션 추가, 여러 표현을 다룬 수업은 서로 다른 처치다. 가이드의 비용 예 자체의 효과는 측정하지 않았다.'),
]

OBSERVATIONS = [
    ('IA-P5', 0, '잘못된 풀이 A는 x²−4x=12를 (x−2)²=12로 바꾸었고, B는 (x−2)²=16에서 x−2=4만 썼다. 각 오류가 처음 생긴 단계와 이유를 말하고, 예를 가린 뒤 원식을 풀어라.',
     'A는 왼쪽에만 4를 더했다. 양변에 4를 더하면 (x−2)²=16이다. B는 x−2=−4를 빠뜨렸다. x=6과 x=−2는 모두 원식을 만족한다.',
     '오답임을 먼저 표시한다. 오류 찾기, 두 해의 근거, 예를 가린 뒤의 풀이를 구분한다.'),
    ('IA-P6', 1, '변이 x m인 정사각형과 x m×5 m인 직사각형이 변 하나를 공유하고 내부가 겹치지 않는다. 합친 넓이가 24 m²일 때 x를 구하라. y=x²+5x−24의 x절편 중 어떤 값이 길이인가?',
     'x²+5x=24이므로 (x+8)(x−3)=0이다. x절편은 (−8,0), (3,0)이다. x>0이므로 공유한 변은 3 m이고 넓이는 9+15=24 m²다.',
     '식의 두 실근, 좌표 표기, 길이의 조건을 따로 기록한다.'),
    ('IA-P7', 2, 'x+y=5와 2x−y=1을 가감 또는 대입으로 풀고 두 직선의 교점을 찾아라. (1,4)와 (1,1)은 각각 왜 연립식의 해가 아닌가?',
     '두 식을 더하면 3x=6이므로 x=2, y=3이다. y=5−x와 y=2x−1의 교점도 (2,3)이다. (1,4)는 첫째 식만, (1,1)은 둘째 식만 만족한다.',
     '전략 선택 이유와 그래프 판독, 두 원식의 정확한 검산을 구분한다.'),
    ('IA-P8', 3, '6(x−1)=4(x−1)+10을 전개하는 풀이와 (x−1)을 묶어 다루는 풀이의 첫 단계를 설명하라. 예를 가린 뒤 5(t+2)=3(t+2)+14를 풀고 첫 연산을 왜 택했는지 적어라.',
     '전개하거나 양변에서 4(x−1)을 빼면 x=6이다. 새 식은 양변에서 3(t+2)를 빼면 2(t+2)=14이므로 t=5다. 전개하는 풀이도 타당하다.',
     '예에서 전략을 알아보는 것과 새 식에서 직접 고르는 것을 구별한다.'),
    ('IA-P9', 4, '공방 이용료는 기본 2500원에 재료 한 세트당 700원을 더한 값이다. 세트 수가 0, 2, 4일 때의 이용료를 표로 쓰고 2세트에서 4세트로 갈 때 세트당 증가액을 말하라.',
     'T=2500+700n에서 이용료는 2500원, 3900원, 5300원이다. 두 세트에 1400원이 늘므로 세트당 700원이다. 세트 수는 0 이상의 정수다.',
     '기본 비용, 두 점 사이 변화율, 정수 입력과 그래프 선분을 구별한다.'),
]

RELATIONS = [
    ('REV-9수02-20-1', 'IA08', '두 실근을 그래프의 (−8,0), (3,0)과 연결한다.', '도형의 길이 조건 x>0을 별도로 적용한다.'),
    ('REV-9수02-22-1', 'IA08', '가로축 교점으로 후보를 찾고 인수분해와 넓이 식으로 확인한다.', '눈금은 근사를 줄 수 있으며 포물선 전체와 상황의 정의역을 구별한다.'),
    ('SEC_9수02-13_C04', 'IA09', '가감으로 얻은 (2,3)을 두 식에 대입해 교점임을 확인한다.', '한 직선 위의 점만으로 두 식의 공통 해를 정할 수 없다.'),
    ('SEC_9수02-18_C03', 'IA09', '교점 후보와 직선 하나에만 놓인 점을 각각 두 식에 대입한다.', '그림에서 두 점이 가까워 보여도 순서쌍이 같다는 근거는 따로 필요하다.'),
    ('REV-9수02-13-1', 'IA09', '대입이나 가감 결과와 같은 연립식의 그래프 교점을 비교한다.', '적절한 첫 연산은 식의 형태에 따라 다르며 그림의 근사 해는 검산한다.'),
    ('SEC_9수02-15_C04', 'IA11', '0세트의 기본 비용을 나타낸 뒤 두 입력 사이의 증가량을 설명한다.', '고정비가 있을 때 전체 비용을 세트 수로 나눈 값은 일정한 증가율과 다르다.'),
    ('REV-9수02-15-1', 'IA11', '2세트에서 4세트로 갈 때 늘어난 1400원을 2로 나눠 식의 계수 700과 대응시킨다.', '일정한 증가량과 실제 구매 수의 정수 조건을 구별한다.'),
]

READING = [
    'PDF12–14,17–21. 목표별 풀이 예, 정답·오답의 병렬 배치, 학급·모둠·개인의 활동, 빈칸 풀이와 유사한 독립 연습을 대조했다.',
    'PDF25,28–31. 자기 질문, 공유 변과 전체 넓이, 도형·식·그래프, 고정비와 단위당 비용, 모둠 안에서의 전략 설명을 대조했다.',
    'PDF34,38–44. 같은 식의 다른 풀이와 서로 다른 연립식에 맞는 전략을 구별했다. 용어집의 타당성·효율·유연성·해집합을 확인했다.',
    'PDF45–51. 부록 A의 권고 등급 기준, 저자와 지원 인력, 잠재적 이해관계 공개를 확인했다.',
    'PDF55,58,61–63. 표 D.2–D.4의 나머지 연구 행에서 비교 조건·결과 영역·분석 인원과 각주를 읽었다. PDF57,64,70에서 정정 표기와 지연 검사 각주를 다시 확인했다.',
    'PDF65–71. 참고문헌, 미주와 정정, 마지막 발간물 안내를 읽었다. 인용 원논문은 별도 출처로 대조한다.',
    '공식 프로토콜 PDF1–8. 학년과 공개 자료 기준, 검색 용어·기간, 처치의 재현 조건, 결과 분류, 탈락·동등성, 즉시·지연 검사와 예비 설계 기준을 확인했다.',
]
COMPARISONS = [
    'D.2 Carroll 1994 실험 2는 보충수업 학생 24명의 하루 비교다. 개념 지식 0.56에 유의 표시가 있고, 오류 감소가 양의 효과가 되도록 부호를 뒤집었다.',
    'D.2와 D.3 Mevarech·Kramarski 2003은 122명의 풀이 예와 자기 질문 비교를 반대 방향에서 요약한다. 개념·절차의 −0.60·−0.47과 0.60·0.47은 같은 비교다.',
    'D.3 Scheiter 외 32명은 같은 텍스트 풀이에 애니메이션을 더한 비교이고 절차 지식 0.87에 유의 표시가 있다. Xin 외 22명은 도식 기반 지도와 일반 전략의 비교이고 절차 지식 1.87에 유의 표시가 있다.',
    'D.3 Akkus 외와 Brenner 외는 집단설계 기준을 충족하지 않았으나 권고 근거에 고려됐다. Brenner 외의 개념 지식 0.78에는 유의 표시가 있다.',
    'D.4 Rittle-Johnson·Star 2009의 두 비교는 대조군을 공유한다. 같은 식의 두 방법 비교에서 즉시 유연성 지식 0.45는 유의, 유연성 사용 0.25는 비유의였다. 영역 값은 즉시 0.36, 지연 0.50이다.',
    'D.4 Rittle-Johnson·Star·Durkin 2012의 124명 비교는 개념 −0.12, 절차 0.13, 유연성 0.37이며 유연성에 유의 표시가 있다. 다른 115명 비교의 −0.15에는 높은 탈락으로 유보가 붙었다.',
    'D.4 Star·Rittle-Johnson 2008은 발견과 짧은 직접 설명을 공통 비교군과 별도로 비교했다. 유연성 영역 0.48·0.49와 각주 q·r의 하위 결과 유의 표기를 구별한다.',
]
DISCREPANCIES = [
    '공식 소개 페이지의 관련 자료 소개에는 2014년 4월로 적혀 있다. 가이드 PDF3–4 및 공식 페이지 발행 표기는 2015년 4월이며 프로토콜 날짜는 2014년 3월 1일이다.',
    'PDF70에서 Mevarech 2003 옆 괄호에는 권고3으로 적혔지만 인쇄 49·51쪽은 각각 권고1·2의 표다. 두 표의 해당 효과크기에는 유의 표시가 없다.',
    'PDF57·59·70에서 Ives 2007의 개정 사항을 확인했다. 개정 표의 개념 1.36에는 유의 표시가 있고 절차 0.52에는 없다. 변경은 보조 결과와 미주 19·24·79도 포함한다.',
    'PDF61·70에서 Rittle-Johnson·Star 2007의 개정 절차 지식 0.33에 유의 표시가 추가됐다. 유연성 영역 값 0.40과 하위 결과의 유의 표시는 별개다.',
]


def verify_examples():
    assert all(x*x-4*x == 12 for x in (-2, 6))
    assert all(x*(x+5) == 24 for x in (-8, 3))
    assert 2+3 == 5 and 2*2-3 == 1
    assert 1+4 == 5 and 2*1-4 != 1
    assert 1+1 != 5 and 2*1-1 == 1
    assert 6*(6-1) == 4*(6-1)+10 and 5*(5+2) == 3*(5+2)+14
    assert [2500+700*n for n in (0, 2, 4)] == [2500, 3900, 5300]
    assert 5300-3900 == 2*700
    assert all(x*(x+4) == 21 for x in (-7, 3))
    assert 5*4+10*4 == 60 and 4+4 == 8


def write(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    verify_examples()
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source.get('reading_extension', {}).get('file') == NOTES:
        build_report()
        return
    assert source['snapshot_sha256'] == SHA and len(source['text_pdf_pages']) == 32
    assert hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest() == PROTOCOL_SHA
    previous = copy.deepcopy(source)
    bibliography = read(ROOT, 'data/sources.json')
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    prior_entry = copy.deepcopy(entry)
    pages = list(range(1, 72))
    visual = sorted(set(previous['visual_pdf_pages'] + VISUAL))
    assert len(visual) == 17
    scope = '2019년 1월 개정 가이드 PDF 71쪽 추출문과 선정 판면 17쪽, 공식 연구 심사 프로토콜 v3.0 PDF 8쪽 추출문을 대조했다.'
    followup = '가이드의 나머지 판면, 관련 도구 모음·영상, WWC 3.0 일반 핸드북과 개별 원논문·원자료, 독립 검토와 실제 학생 반응을 후속 확인한다.'
    entry.update(review_scope=scope, next_review=followup)
    notes = dict(source_id=SOURCE, source_pdf_sha256=SHA, contains_source_full_text=False,
                 cumulative_read_scope=scope, cumulative_text_pdf_pages=pages, cumulative_visual_pdf_pages=visual,
                 new_text_pdf_pages=sorted(set(pages)-set(previous['text_pdf_pages'])), new_visual_pdf_pages=VISUAL,
                 previous_review=previous, previous_bibliography=prior_entry, reading_log=READING,
                 unread_followups=[followup], discrepancies=DISCREPANCIES, comparison_notes=COMPARISONS,
                 protocol=dict(url='https://ies.ed.gov/ncee/wwc/Docs/ReferenceResources/wwc_algebra_pg_protocol_v3.0.pdf',
                               version='3.0', document_date='2014-03-01', sha256=PROTOCOL_SHA,
                               pdf_pages=8, text_pdf_pages=list(range(1, 9)), visual_pdf_pages=[], redistributed=False,
                               search_through='2013-09', first_search_year=1993, panel_exceptions=True,
                               eligibility='영어로 공개된 6~12학년 연구와 재현 가능한 처치를 대상으로 했다. 수업 언어·지역은 영어권에 한정하지 않았다.',
                               outcomes='개념 지식과 절차 지식, 절차 유연성을 구분한다. 즉시 결과는 권고 등급에 반영하며 지연 및 전이 결과는 별도로 기록한다.'))
    encoded = (json.dumps(notes, ensure_ascii=False, indent=2) + '\n').encode()
    source.update(date='2026-11-10', bibliography_snapshot=digest(entry), read_scope=scope,
                  text_pdf_pages=pages, visual_pdf_pages=visual, reading_log=READING,
                  reading_extension=dict(file=NOTES, sha256=hashlib.sha256(encoded).hexdigest()),
                  search_period='1993–September 2013; panel exceptions per Protocol 3.0',
                  method_note='연구표의 처치·대조 조건·결과 영역·통계적 유의성·효과크기·측정 시점 및 공유 대조군을 구별했다.',
                  limits=followup,
                  editorial_action='권고 대응 5건, 자체 관찰 5건, 관계별 해석 7건을 추가했다.')
    old_claims = {row['id']: row for row in registry['claims'] if row['source_id'] == SOURCE}
    claims = {
        cid: dict(id=cid, source_id=SOURCE, role='instructional_recommendation_with_evidence_scope',
                  standard_codes=codes, locations=[location], support=support, does_not_establish=limit,
                  target_snapshots={f'revision:{code}': digest(target_value(f'revision:{code}')) for code in codes},
                  independent_review=False, student_validated=False, local_effect_tested=False,
                  recommendations=[dict(number=rec, evidence_rating=RATINGS[str(rec)], application_limit=limit)])
        for cid, codes, rec, location, support, limit in MAPPINGS
    }
    assert old_claims.keys().isdisjoint(claims)
    registry['claims'].extend(claims.values())
    source['observations'].extend(
        dict(id=oid, standard_codes=MAPPINGS[mapping][1], question=question, expected=expected,
             interpretation=limit + ' 자체 설계이며 학생 검증 대기다.', student_validated=False)
        for oid, mapping, question, expected, limit in OBSERVATIONS)
    relations = read(ROOT, 'data/revised_relations.json')['relations']
    by_id = {row['id']: row for row in relations}
    pairs = {(row['id'], cid) for row in relations for cid, claim in claims.items()
             if all(row[key].startswith('standard:') for key in ('from', 'to'))
             and {row[key][9:] for key in ('from', 'to')} <= set(claim['standard_codes'])}
    assert pairs == {(rid, cid) for rid, cid, _, _ in RELATIONS}
    reviews = read(ROOT, FILE)
    for row in reviews['records']:
        cid = row['claim_id']
        if cid in old_claims:
            assert row['claim_snapshot'] == claim_snapshot(old_claims[cid], previous)
            row['claim_snapshot'] = claim_snapshot(old_claims[cid], source)
    for rid, cid, finding, limit in RELATIONS:
        reviews['records'].append(dict(relation_id=rid, claim_id=cid, role='activity_context',
                                       finding=finding, limit=limit, relation_snapshot=relation_snapshot(by_id[rid]),
                                       claim_snapshot=claim_snapshot(claims[cid], source)))
    apply_literature_context(relations, registry, registry=reviews)
    queue_path = 'data/content_review_queue.json'
    queue = read(ROOT, queue_path)
    item = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    item.update(source=entry, claim_ids=list(old_claims)+list(claims))
    (ROOT / NOTES).write_bytes(encoded)
    write('data/sources.json', bibliography)
    write('data/literature_claim_reviews.json', registry)
    write(FILE, reviews)
    write(queue_path, queue)
    build_report()
    print('IES algebra guide: 71 text pages, 17 selected layouts, 8 protocol pages, 5 claims, 5 probes, 7 relation entries')


if __name__ == '__main__':
    main()

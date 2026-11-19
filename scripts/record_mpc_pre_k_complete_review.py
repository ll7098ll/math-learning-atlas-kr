"""Guarded migration; importing does not inspect private review evidence."""
import copy
import hashlib
import json
from literature_review import ROOT, load_registry, digest
from check_mpc_pre_k_models import check

SID = 'MORRIS_ET_AL_2016_MAKING_PRE_K_COUNT'
NOTE = f'data/literature_evidence/{SID}_complete_visual_review_notes.json'
SCOPE = 'MDRC2016보고서118판면 전체를 읽었다. 표지·공백·목차·요약·본문·부록A/B·19표·5그림·11상자·참고문헌·기관소개를 포함한다. 기존2·새116판면이며 새 전문 추출문 독해는0쪽이다. 종전 지정 추출문4쪽·판면2쪽의 대조 이력을 보존한다.'
LIMIT = '동일MPC·High5s평가의 취학전 보고서다. 교사가 제공한 시간·아동별 경험 시간·조건부 질 점수·운영 충실도·성취는 다른 측정이다. 종합 검사 비유의는 동등성 입증이 아니며 개별 국내 세기·연산·도형 과제나 보편적인 지도 순서의 효과로 옮기지 않는다. 후속 보고서는 독립 재현이 아니다. 원자료·원코드·공식 정오표·국내 검증은 미확인이다.'


def read(p):
    return json.loads((ROOT / p).read_bytes())


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def write(p, d):
    (ROOT / p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    l = load_registry()
    old = copy.deepcopy(l)
    s = l['sources'][SID]
    assert len(l['claims']) == 1057
    assert s['snapshot_sha256'] == '9bdc6dd8bbdf55e69188c02b1d9b29296736156530df64dc43e6221bfa064b98'
    assert not (ROOT / NOTE).exists()
    p = read('tmp/literature/mpc-prek-complete-20261119/reading-progress.json')
    assert p['reading_completed'] and p['actually_viewed_pdf_pages_this_turn'] == list(range(1, 119))
    assert len(p['new_visual_pdf_pages']) == 116
    assert p['source_pdf_sha256'] == s['source_pdf_sha256'] == sha('tmp/literature/mpc-prek-complete-20261119/source.pdf')
    for page, h in p['rendered_page_sha256'].items():
        assert sha(f'tmp/literature/mpc-prek-complete-20261119/rendered/page-{int(page):03d}.png') == h
    prior = read(s['snapshot_file'])
    findings = [dict(pdf_pages=x['pages'], finding=' '.join(x['findings'])) for x in p['reading_log']]
    n = copy.deepcopy(prior)
    n.update(date='2026-11-19', read_scope=SCOPE, previous_review=copy.deepcopy(s),
             previous_snapshot_file=s['snapshot_file'], previous_snapshot_sha256=s['snapshot_sha256'],
             previous_visual_pdf_pages=p['previous_visual_pdf_pages'],
             previous_rendered_page_sha256=prior['rendered_page_sha256'],
             visual_pdf_pages=list(range(1, 119)), new_visual_pdf_pages=p['new_visual_pdf_pages'],
             rendered_page_sha256=p['rendered_page_sha256'], new_text_pdf_pages=[],
             new_full_extracted_text_pages=0, whole_report_visual_read=True,
             whole_report_tables=dict(count=19, figures=5, boxes=11),
             audit_findings=findings, exact_own_checks=check(),
             all_cited_originals_read=False, raw_student_data_read=False,
             models_refitted=False, official_erratum_verified=False,
             independent_review=False, student_validated=False)
    n['reading_log'] = prior['reading_log'] + [SCOPE] + [x['finding'] for x in findings]
    n['source_corrections'] += [dict(location='PDF ' + ','.join(map(str, x['pdf_pages'])),
                                   issue=x['finding'], status='own_bounded_audit_not_official_erratum') for x in findings]
    n['cross_source_qualification'] = dict(claim_id='MPCD-04',
        locations=[48, 92],
        finding='2016본문 주19와 표A1은 최초70기관에서 배정 후·실시 전 대조1기관이 빠져69기관이 됐음을 기록한다.2017의 탈락 없음 설명은 시점을 구별하며 최초 배정부터 전 과정 탈락0으로 읽지 않는다.',
        official_erratum=False)
    n['empirical_scope'].update(
        design='뉴욕시 최초70기관을 블록 안에서 무작위 배정했다. 배정 후·실시 전 대조1기관이 빠져 프로그램35·정규수업34기관에서 실시했다.',
        sample_description='학급 관찰87·86개, 봄 아동 검사698·691명. 동의2715명·가을검사859명과 계획된 하위표집을 구별한다. 부록 본문의 동의2717표기는 표의2715와 다르다.',
        inference_limit=LIMIT)
    write(NOTE, n)
    s.setdefault('snapshot_history', []).append({k: s[k] for k in ['snapshot_file', 'snapshot_sha256', 'date', 'read_scope']})
    s.update(date='2026-11-19', snapshot_file=NOTE, snapshot_sha256=sha(NOTE), read_scope=SCOPE,
             limits=LIMIT, scope_note='제공 시간과 아동별 경험·조건부 질 점수·검사 및 배정 시점을 구별한다.',
             method_note='118판면 전체와 표·그림·부록모형을 읽었다. 분모·반올림·결측/0점과 가상 시간 예시를 자체 검산했으며 원자료 재분석은 수행하지 않았다.',
             editorial_action='2026-11-19: 기존MPC16주장2건과 관련MPCD-04의 기관 탈락 시점 설명을 보완했다. 새 출처·주장·과제·관계는0이며 기존 이력을 보존했다.')
    s['empirical_scope'].update(
        design='뉴욕시 최초70기관을 블록 안에서 무작위 배정했다. 배정 후·실시 전 대조1기관이 빠져 프로그램35·정규수업34기관에서 실시했다.',
        sample_description='학급 관찰87·86개, 봄 아동 검사698·691명. 동의2715명·가을검사859명과 계획된 하위표집을 구별한다. 부록 본문의 동의2717표기는 표의2715와 다르다.',
        inference_limit=LIMIT)
    updates = {
        'MPC16-01': (
            '최초70기관에서 배정 후·실시 전 대조1기관이 빠져69기관(35/34)에서 실시했다. 세 시간 관찰의 교사 제공 수학 시간 차이는11.95분, 아동당 평균 경험 시간 차이는6.43분이다. 표4.1의87/86학급과 표4.4의698/691명은 다른 분모다. 관찰된 교사 주도 활동의 질 평균1.95/1.77은 해당 활동이 있었던95.9/80.5%학급에 조건부다.',
            '시간 제공을 모든 아동의 동일한 실제 참여·세기 능력 향상·실제 연간40시간 노출로 읽지 않는다. 아동당 시간에는 독립 활동도 포함된다. 포함 학급이 달라 조건부 질 차이는 진정한 영향 추정치가 아니라는 원문 주석을 유지한다. 전체 학급의 중간 이상 질 비율50.0/29.4%와 조건부 평균의 분모도 다르다.2013의18분은 비형식 활동을 제외해2015의35분과 바로 비교할 수 없다.'),
        'MPC16-02': (
            '취학전 말 종합ECLS-B수학·WJ-III응용문제 효과크기.05/.06은 유의하지 않았다. 가을 수학 검사는 프로그램 시작 후9–11월에 실시돼 수학 결과 모형에서 동종 사전점수로 보정하지 않았다. 동의2715명에서 가을859명·봄1389명을 계획 표집했으며 가을 검사자의94%초과가 봄에 재검사를 받았다. 결과 결측은 다중대체하지 않았고, 공변량 결측 대체와 구별한다.',
            '종합 점수 비유의는 동등성·효과0·개별 세기/연산 과제의 무효를 입증하지 않는다.2715명과1389명의 차이를 전부 탈락으로 세거나 두 시점 평균을 개인 성장으로 읽지 않는다. PencilTap의10%수준 신호를 모든 아동 결과 무효라고 숨기지 않으며 연습 실패의 결측/0점 처리를 구별한다. 높은 언어 집단 내 유의성은 집단 간 효과 차이 검정과 다르다. 표4.7에서WJ만 집단 간10%표지가 있다. 원점수·코드와 분모 불일치를 임의 복원하지 않는다.')}
    extra = {'MPC16-01': [36, 38, 48, 54, 60, 61, 62, 64, 92, 95],
             'MPC16-02': [67, 68, 69, 71, 76, 77, 100, 101, 102, 103, 104, 105, 109, 110, 111]}
    for c in l['claims']:
        if c['id'] in updates:
            c.update(zip(['support', 'does_not_establish'], updates[c['id']]))
            c['empirical_scope'] = copy.deepcopy(s['empirical_scope'])
            c['locations'] = list(dict.fromkeys(c['locations'] + [f'https://www.mdrc.org/work/publications/making-pre-k-count/file-full#page={v}' for v in extra[c['id']]]))
        if c['id'] == 'MPCD-04':
            old_text = '기관 탈락0은 아동 탈락0이 아니다.'
            assert old_text in c['does_not_establish']
            c['does_not_establish'] = c['does_not_establish'].replace(old_text,
                '기관 탈락 설명은 시점을 구별한다.2016보고서 주19는 최초70기관 중 배정 후·실시 전 대조1기관 탈락을 기록하므로2017의 탈락 없음 설명을 전 과정0으로 일반화하지 않는다. 기관과 아동 탈락은 별개다.')
            c['locations'] += [f'https://www.mdrc.org/work/publications/making-pre-k-count/file-full#page={v}' for v in [48, 92]]
    bib = read('data/sources.json')
    b = next(v for v in bib if v['id'] == SID)
    b.update(review_scope=SCOPE, does_not_establish=LIMIT,
             next_review='2016보고서 전체 대조를 마쳤다. 원자료·원코드·공식 정오표,2018후속 전체·2023설계논문 전체·2026출판판 전체와 국내 검증은 별도 미완료다.')
    s['bibliography_snapshot'] = digest(b)
    q = read('data/content_review_queue.json')
    next(v for v in q['literature_review'] if v['source']['id'] == SID)['source'] = copy.deepcopy(b)
    reviews = read('data/relation_literature_reviews.json')
    assert not any(x['claim_id'] in {*updates, 'MPCD-04'} for x in reviews['records'])
    for sid, source in old['sources'].items():
        assert l['sources'][sid]['observations'] == source['observations']
        if sid != SID:
            assert l['sources'][sid] == source
    assert len([x for x, y in zip(old['claims'], l['claims']) if x != y]) == 3
    for path, value in [('data/sources.json', bib), ('data/content_review_queue.json', q), ('data/literature_claim_reviews.json', l)]:
        write(path, value)
    load_registry()
    print(json.dumps(dict(status='recorded', total_visual_pages=118, new_visual_pages=116,
                         changed_claims=3, new_claims=0, new_tasks=0)))


if __name__ == '__main__':
    main()

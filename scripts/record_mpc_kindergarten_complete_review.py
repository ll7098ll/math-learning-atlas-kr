"""Guarded one-time migration; importing performs no private-file I/O."""
import copy
import hashlib
import json
from literature_review import ROOT, load_registry, digest
from check_mpc_kindergarten_models import check

SID = 'MATTERA_ET_AL_2018_MPC_KINDERGARTEN'
NOTE = f'data/literature_evidence/{SID}_complete_visual_review_notes.json'
SCOPE = 'MDRC2018유치원 결과 보고서142판면 전체를 읽었다. 표지·공백·목차·요약·본문·부록A–H·21표·8그림·4상자·참고문헌·기관소개를 포함한다. 기존11·새131판면이며 새 전문 추출문 독해는0쪽이다. 종전 지정 추출문18쪽과 판면11쪽의 대조 이력을 보존한다.'
LIMIT = '동일MPC·High5s평가의 유치원 추적 보고서다. 세 비교의 모집단·배정 단위·분모·검사와 점수변환을 구별한다. High5s단독 셀이 없어 완전2×2상호작용을 식별하지 못한다. 외부 격차/성장 환산은 같은 집단에서 관측한 격차 감소/추가 학습기간이 아니다. 원점수·로짓·T점수의 차이를 단순 단위 변환만으로 설명하지 않는다. 후속 보고서는 독립 재현이 아니며 원자료·채점 코드·공식 정오표·국내 검증은 미확인이다.'


def read(p):
    return json.loads((ROOT/p).read_bytes())


def sha(p):
    return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()


def write(p, value):
    (ROOT/p).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def main():
    l = load_registry()
    old = copy.deepcopy(l)
    s = l['sources'][SID]
    assert len(l['claims']) == 1057 and len(s['observations']) == 4
    assert s['snapshot_sha256'] == '89a9ae887d3e289c53e7a659ea4b694c95381445289b2d1f73224037f81cfbf2'
    assert not (ROOT/NOTE).exists()
    p = read('tmp/literature/mpc-kindergarten-complete-20261119/reading-progress.json')
    assert p['reading_completed'] and p['actually_viewed_pdf_pages_this_turn'] == list(range(1,143))
    assert len(p['new_visual_pdf_pages']) == 131
    assert p['source_pdf_sha256'] == s['source_pdf_sha256'] == sha('tmp/literature/mpc-kindergarten-complete-20261119/source.pdf')
    for page, h in p['rendered_page_sha256'].items():
        assert sha(f'tmp/literature/mpc-kindergarten-complete-20261119/rendered/page-{int(page):03d}.png') == h
    empirical = copy.deepcopy(s['empirical_scope'])
    empirical.update(
        design=' 취학전 기관 무작위 배정과 MPC공립24학교의 High5s개별 배정을 사용한 세 비교. 최초69실시기관과 유치원 결과가 관측된22대조공립학교의 분모를 구별한다.'.strip(),
        sample_description='주표3.1 641/684명,3.2 303/310명,3.3 303/345명. High5s최초동의 배정655명과 부록H추적622명,잔류·미동의18명 추가배정을 포함한 주분석613명은 다른 집합이다.',
        inference_limit=LIMIT)
    prior = read(s['snapshot_file'])
    findings = [dict(pdf_pages=x['pages'], finding=' '.join(x['findings'])) for x in p['reading_log']]
    n = copy.deepcopy(prior)
    n.update(date='2026-11-19', read_scope=SCOPE, empirical_scope=empirical,
             previous_review=copy.deepcopy(s), previous_snapshot_file=s['snapshot_file'],
             previous_snapshot_sha256=s['snapshot_sha256'],
             previous_visual_pdf_pages=p['previous_visual_pdf_pages'],
             previous_rendered_page_sha256=prior['rendered_page_sha256'],
             visual_pdf_pages=list(range(1,143)), new_visual_pdf_pages=p['new_visual_pdf_pages'],
             rendered_page_sha256=p['rendered_page_sha256'], new_text_pdf_pages=[],
             new_full_extracted_text_pages=0, whole_report_visual_read=True,
             whole_report_tables=dict(count=21, figures=8, boxes=4),
             audit_findings=findings, exact_own_checks=check(),
             all_cited_originals_read=False, raw_student_data_read=False,
             models_refitted=False, official_erratum_verified=False,
             independent_review=False, student_validated=False)
    n['reading_log'] = prior.get('reading_log', []) + [SCOPE] + [x['finding'] for x in findings]
    n.setdefault('source_corrections', []).extend(dict(location='PDF '+','.join(map(str,x['pdf_pages'])), issue=x['finding'], status='own_bounded_audit_not_official_erratum') for x in findings)
    n['unresolved_source_issues'] = [
        dict(pdf_pages=[69,70], issue='취학전 관측시간의 본문32분 미만/초과와 표주31.5분 미만/이상은 같은 경계가 아니다.', resolution='실제 분류 코드 미확인;공식 정오표 아님'),
        dict(pdf_pages=[97,98,99], issue='로짓의 선형변환이라고 설명한T점수와 로짓 분석의ES·유의성이 다르다. 같은 표본·가중·모형·전역 양의 아핀변환·추론이라면 ES와 t/p가 유지되므로 단순 단위만으로 차이를 설명할 수 없다.', resolution='연령별 변환·반올림·표본/가중·채점 파이프라인은 미확인;원코드 필요'),
        dict(pdf_pages=[124,125], issue='G7 비스페인어 집단 억제와 작업기억의 양의 인쇄 영향.04/.20과 음의ES−.19/−.15는 양의SD로 나누는 주석 정의와 부호가 상충한다.', resolution='원자료/정오표 없이 어느 열 부호도 수정하지 않는다'),
        dict(pdf_pages=[18,28,36,66], issue='주3회30분·회기30–45분·추가주75분은 그대로 하나의 실제 노출량으로 합칠 수 없다.', resolution='계획/세부활동/전체회기/참여 시점 미확인'),
        dict(pdf_pages=[85], issue='절편과24학교 지시변수를 모두 쓰는 인쇄식은 기준/합계제약을 적지 않았다.', resolution='실제SAS설계행렬/제약 미확인;실제 추정 실패를 뜻하지 않음')]
    write(NOTE, n)
    s.setdefault('snapshot_history', []).append({k:s[k] for k in ['snapshot_file','snapshot_sha256','date','read_scope']})
    s.update(date='2026-11-19', snapshot_file=NOTE, snapshot_sha256=sha(NOTE), read_scope=SCOPE,
             empirical_scope=empirical, limits=LIMIT,
             scope_note='세 비교의 표본·배정·검사·점수변환과 집단내/간 검정을 구별한다.',
             method_note='142판면·21표·8그림·4상자와 부록A–H를 읽고 선형변환 불변성·분모·경계·단위·반올림을 자체 검산했다. 학생 원자료와 채점/분석 코드는 읽지 않았다.',
             editorial_action='2026-11-19: 기존MPC18주장9건을 보완했다. 새 출처·주장·과제·관계는0이며 기존1240과제·875관계 해석과 검토 이력을 보존했다.')
    additions = {
      'MPC18-01': (
        '기관 내 아동을 고려한2수준 모형과 배정블록 고정효과를 사용했다. 종합검사별 규준SD와 효과크기 분모인 실제 대조집단SD는 다르다.',
        '공립집단REMA 유의/CBO비유의만으로 장소 차이를 확정하지 않는다(표G1 집단간p.17). 표A1은 유치원 결과가 아니라 취학전 봄 결과이며 시간층화는 무작위 용량배정이 아니다. 본문32분과 표주31.5분 경계 차이는 원코드 없이 수정하지 않는다.'),
      'MPC18-02': (
        '추가High5s는 개인배정·학교고정효과,결합대정규수업은 취학전 기관 군집·배정블록 모형이다. 표3.3의 대조22학교는 최초23학교 중1학교의 아동검사가 완료되지 않아 관측된 분모다.',
        'High5s단독 셀이 없고 비교 모집단·대조SD·보정이 달라.08+.19를 결합효과로 강제하거나 시너지로 해석하지 않는다. 외부격차1.046SD대.30≈29%·.19≈18%는 다른검사/집단 비교 환산이며 실측격차감소가 아니다. 주3회30분·회기30–45분·주75분 표기의 관계는 미확인이다.'),
      'MPC18-03': (
        '48문항 중 운영팀이 지도와 유사하다고 분류한5문항을 뺀43문항 민감도다. 팀은BuildingBlocks훈련을 받았으며 독립 맹검 분류로 확인되지 않았다.',
        '유사문항5개 제거는 전체 검사 독립성·한국어 타당도·모든문항의 측정불변성 검증이 아니다. 로짓에서T로의 선형변환 설명과 분석차이는MPC18-07의 조건부 불변성 문제를 함께 확인해야 한다.'),
      'MPC18-04': (
        '하위영역 문항수는 수27·규칙/관계8·도형/기하측정9·측정4다. 표F1의 수p.10*는 보고서10%수준 표지다.',
        '영역별 유의/비유의만으로 영역간 효과차이 검정이라고 읽지 않는다. 모두가 최소한의 수/규칙 문항을 받았다는 설명은 해당영역 전체문항을 모두 실시했다는 뜻이 아니다.'),
      'MPC18-05': (
        '도형문항은 이전 수문항 등 성공에 따른 도달 여부와 얽혀 있다. 부록F는 별도 미제시 추가분석의 도형문항 도달효과ES.11도 기술한다.',
        '도형점수ES.19에서 도달효과.11을 빼 순수도형효과.08로 복원할 수 없다. 서로 다른 결과와SD이며 도달과 도형 수행을 분리한 인과 추정이 아니다.'),
      'MPC18-06': (
        'D1의REMA48/WJ31은 내용분류의 문항수이며 모든아동에게 모두 실시된 수가 아니다.3동전과6동전은9개,5페니와1니켈은6개 동전·10센트로 단위도 다르다.',
        '우리 진단과제에서 미제시를 관찰오답으로 판정하지 않는 원칙과 원연구의 집계 채점 알고리즘을 구별한다. 실제 미실시 문항이 연구점수에 반영되는 방식은 원 채점 코드 없이 단정하지 않는다. 성인의 단위/문항 제시가 수행을 바꾸므로 한국과제 개별 효과로 옮기지 않는다.'),
      'MPC18-07': (
        '부록E의 신뢰구간은90%다. 주분석의132명 대체표집과 달리 민감도1은 대체 없이 기존183명 상향가중,민감도2는 대체132명을189명 규모로 가중한다. 결측 공변량은50다중대체 자료로 통합하나 결과 결측은 대체하지 않는다.',
        '같은 관측값·가중·절편 포함 모형·추론에서 y′=a+by(b>0)인 전역 아핀변환만 하면 영향/SE/대조SD가 함께 변해 ES와t/p가 유지된다. 원문은T를 로짓의 선형변환이라고 설명하지만 분석결과가 달라 단순 단위 변화만으로 설명할 수 없다. 실제 연령별 채점·반올림·표본/가중/코드 차이는 미확인이다. 다섯 사양은 다섯 독립 실험이 아니다.'),
      'MPC18-08': (
        '최초동의 배정655명과 H1관측622명,주분석613명의 포함조건은 다르다. 학교추적 성공과 같은학교 잔류도 다른 분모다. 한 대조학교의 검사 미완료는 기관 철수와 구별한다.',
        'B4프로그램 잔류622명과H1추적622명은 수가 같아도 같은 집합으로 확인되지 않았다. 공변량 공동Wald F값을p값으로 읽거나 비유의로 동등성을 입증하지 않는다. 한표의 대조집단만의 하위집단 인원을 전체 실험표본으로 합산하지 않는다.'),
      'MPC18-09': (
        '표3.2의REMA영향1.57과H1의1.72는 각ES.19/.20,인쇄p.01과 별2개/3개다. 별은 각각5%/1%수준이며 반올림p로 정확한 미공개p를 복원하지 않는다.',
        '하위집단내 별과 집단간 차이의†기호는 다른 검정이다. 표G7 비스페인어 집단 영향+.04/+.20과ES−.19/−.15는 양의SD로 나누는 주석과 부호가 상충한다. 원자료·정오표 없이 어느 부호도 고치지 않는다. 표 평균 차이와 별도 인쇄 영향의.01차이는 독립 반올림으로 가능하다.')}
    extra = {
      'MPC18-01':[69,70,83,84,110,111], 'MPC18-02':[17,18,28,31,36,66,79,85,86],
      'MPC18-03':[47,91,92,97], 'MPC18-04':[103,104], 'MPC18-05':[103,104],
      'MPC18-06':[91,92,93,94,103,104], 'MPC18-07':[83,84,97,98,99],
      'MPC18-08':[37,39,40,73,74,75,76,77,78,79,80,135,136],
      'MPC18-09':[110,111,124,125,126,127,135,136]}
    for c in l['claims']:
        if c['id'] in additions:
            support, limit = additions[c['id']]
            c['support'] += ' '+support
            c['does_not_establish'] += ' '+limit
            c['empirical_scope'] = copy.deepcopy(empirical)
            c['locations'] = list(dict.fromkeys(c['locations']+[prior['pdf_url']+f'#page={v}' for v in extra[c['id']]]))
    bib = read('data/sources.json')
    b = next(x for x in bib if x['id'] == SID)
    b.update(review_scope=SCOPE, does_not_establish=LIMIT,
             next_review='2018효과보고서 전체 대조 완료. 별도2018실행보고서,원자료·채점/분석코드·정오표,2023설계논문/2026출판판 전체·인용 원전·국내 검증은 별도 미완료다.')
    s['bibliography_snapshot'] = digest(b)
    q = read('data/content_review_queue.json')
    next(x for x in q['literature_review'] if x['source']['id'] == SID)['source'] = copy.deepcopy(b)
    assert not any(x['claim_id'] in additions for x in read('data/relation_literature_reviews.json')['records'])
    for sid, source in old['sources'].items():
        assert l['sources'][sid]['observations'] == source['observations']
        if sid != SID:
            assert l['sources'][sid] == source
    assert [c['id'] for c,d in zip(l['claims'],old['claims']) if c != d] == list(additions)
    for path, value in [('data/sources.json',bib),('data/content_review_queue.json',q),('data/literature_claim_reviews.json',l)]:
        write(path,value)
    load_registry()
    print(json.dumps(dict(status='recorded', total_visual_pages=142,new_visual_pages=131,
                         changed_claims=9,new_claims=0,new_tasks=0)))


if __name__ == '__main__':
    main()

"""Render the 118 individually curated analyses and synchronize the project."""
from __future__ import annotations
import copy
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from analysis_content import ENTRIES, FAMILIES, CONNECTION_OVERRIDES, PATH_OVERRIDES
from build_inventory import write_indexes

ROOT = Path(__file__).resolve().parents[1]
PRESERVED = {'6수01-10', '6수02-03', '6수03-14'}
KIND = {'generalizes': '의미 확장', 'meaning_connection': '의미 연결', 'contrasts': '대조'}


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def save(path, obj):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def table(headers, rows):
    def cell(v):
        return str(v).replace('|', '\\|').replace('\n', ' ')
    return ['| ' + ' | '.join(headers) + ' |', '|' + '|'.join(['---'] * len(headers)) + '|'] + [
        '| ' + ' | '.join(cell(x) for x in row) + ' |' for row in rows]


def freeze_content():
    families, entries = copy.deepcopy(FAMILIES), copy.deepcopy(ENTRIES)
    # Whitespace-only editorial pass; no wording, numbers, formulas or official
    # curriculum statements are changed. The frozen JSON is the portable source.
    sys.path.insert(0, str(ROOT / 'tmp/korean-spacing'))
    from kiwipiepy import Kiwi
    kiwi = Kiwi()
    terms = ['직육면체','정육면체','삼각기둥','사각기둥','오각기둥','육각기둥','삼각뿔','사각뿔',
             '각기둥','각뿔','원기둥','원뿔','전개도','겨냥도','겉넓이','쌓기나무','정기둥',
             '삼각형','사각형','직사각형','정사각형','평행사변형','다각형','정다각형','마름모',
             '대응점','대응변','대응각','단위분수','자릿값','반직선','수직선','밑면','옆면','밑각',
             '공약수','공배수','최대공약수','최소공배수','등분제','포함제','나머지','원주율','원주',
             '중등','고등','절개변','내각','꼭짓점','시침','분침','초침','등식','부등식','반올림']
    for term in terms:
        kiwi.add_user_word(term, 'NNG', 5)

    def space(value):
        if isinstance(value, list):
            return [space(x) for x in value]
        chunks = value.split('|')
        formatted=[]
        for chunk in chunks:
            if chunk.count(' ') >= 2 and not re.search(r'[가-힣]{12,}', chunk):
                formatted.append(chunk)
                continue
            result=kiwi.space(chunk)
            for term in sorted(terms, key=len, reverse=True):
                result=re.sub(r'\s*'.join(map(re.escape, term)), term, result)
            result=re.sub(r'밑면\s*과\s*세\s*옆면', '밑면과 세 옆면', result)
            result=re.sub(r'(?<=[0-9])\s+(과|와|은|는|이|가|을|를|의|에|도|로|보다)(?=\s|[0-9])', r'\1', result)
            formatted.append(result)
        output = '|'.join(formatted)
        assert re.sub(r'\s', '', value) == re.sub(r'\s', '', output)
        return output

    for entry in entries:
        for key in ['task', 'idea', 'steps', 'probes', 'bridge', 'limit']:
            entry[key] = space(entry[key])
        entry['connections'] = copy.deepcopy(CONNECTION_OVERRIDES.get(entry['code'], families[entry['family']]['connections']))
        entry['paths'] = copy.deepcopy(PATH_OVERRIDES.get(entry['code'], families[entry['family']]['paths']))
    # Prefer polygon properties as the broad middle-school destination; the
    # quadrilateral and triangle cases with narrower targets are retained.
    for entry in entries:
        if entry['family'] == 'plane' and entry['code'] not in CONNECTION_OVERRIDES and entry['code'] != '4수03-10':
            entry['connections'][0] = ['9수03-05', 'generalizes', '변과 각의 조건 및 도형 구성을 다각형의 성질과 정당화로 확장한다.',
                                       '정의, 보조선, 각의 관계, 논증', '단순한 그림의 인상이나 몇 번의 측정으로 일반 명제를 확정하지 않는다.']
    save('data/analysis_details.json', {
        'scope': '기존 수작업 초안 세 개를 제외한 초등 118개 개별 분석. 수학적 분석 및 교수 설계 초안.',
        'editorial_check': '띄어쓰기 전후 공백을 제외한 문자 완전 일치를 검사했다. 공식 성취기준 문장은 변환하지 않았다.',
        'families': families, 'analyses': entries})


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if '--freeze-content' in sys.argv:
        freeze_content()
    content = load('data/analysis_details.json')
    families, entries = content['families'], content['analyses']
    inventory = load('data/standards.json')
    by_code = {r['code']: r for r in inventory['standards']}
    elementary = {r['code'] for r in inventory['standards'] if r['school_level'] == '초등학교'}
    assert len(entries) == 118 and {e['code'] for e in entries} == elementary - PRESERVED
    old_hash = {code: hashlib.sha256((ROOT / f'analyses/{code}.md').read_bytes()).hexdigest() for code in PRESERVED}
    sources = load('data/sources.json')
    additions = [
        {'id':'IES_EARLY_2013','title':'Teaching Math to Young Children','year':2013,'kind':'공식 교수 가이드',
         'url':'https://ies.ed.gov/ncee/wwc/PracticeGuide/18',
         'review_scope':'공식 소개, 대상인 취학 전 유아, 권고와 근거 수준 확인. 초등 전 학년의 효과 근거로 일반화하지 않음.',
         'supports':['초기 수와 연산 및 도형 측정 규칙 자료를 발달 관점에서 조사할 틀']},
        {'id':'NRC_WHOLE_2001','title':'Adding It Up Chapter 6 Developing Proficiency with Whole Numbers','year':2001,'kind':'연구 종합',
         'url':'https://www.nationalacademies.org/read/9822/chapter/8',
         'review_scope':'장 도입, 자릿값과 연산 성질 및 다양한 계산 전략에 관한 공개 대목. 인용된 개별 실험의 전체 검토 전.',
         'supports':['수의 구조와 계산 절차의 의미를 함께 분석하는 관점']},
        {'id':'GAISE_2020','title':'Pre K 12 Guidelines for Assessment and Instruction in Statistics Education II','year':2020,'kind':'공식 통계교육 프레임워크',
         'url':'https://www.amstat.org/asa/files/pdfs/GAISE/GAISEIIPreK-12_Full.pdf',
         'review_scope':'서지와 Framework의 네 구성 요소, Level A의 표와 그래프 및 변이·평균 관련 공개 대목. 전체 보고서 정독 전.',
         'supports':['질문 수집 분석 해석의 연결','관찰 단위와 분류','평균과 변이 및 결과 해석의 범위']}]
    known = {s['id'] for s in sources}
    sources.extend(s for s in additions if s['id'] not in known)
    save('data/sources.json', sources)
    source_map = {s['id']: s for s in sources}
    elements_data, relations_data = load('data/elements.json'), load('data/relations.json')
    # Stable identifiers let this renderer be rerun without duplicating records.
    elements = [e for e in elements_data['elements'] if not e['id'].startswith(('F_', 'A_'))]
    relations = [r for r in relations_data['relations'] if not r['id'].startswith('AN_')]
    family_codes = {key: [e['code'] for e in entries if e['family'] == key] for key in families}
    for family in families.values():
        for i, row in enumerate(family['processes'], 1):
            label, thinking, observable = row.split('|')
            elements.append({'id':f'F_{family["id"]}_{i:02}', 'label':label, 'thinking':thinking, 'observable':observable,
                             'standards':family_codes[family['id']], 'status':'분석 초안'})
    registry = [r for r in load('data/analysis_registry.json') if r['code'] in PRESERVED or r['code'] not in elementary]
    for entry in entries:
        code, family = entry['code'], families[entry['family']]
        record = by_code[code]
        assert len(entry['steps']) >= 4 and len(entry['probes']) >= 3
        assert all(len(x.split('|')) == 3 for x in entry['steps'])
        assert all(len(x.split('|')) == 4 for x in entry['probes'])
        assert set(entry['precursors']) <= set(by_code)
        for conn in entry['connections']:
            assert conn[0] in by_code and by_code[conn[0]]['school_level'] != '초등학교'
        render_entry(entry, family, record, by_code, source_map)
        registry.append({'code':code,'status':'초안','file':f'analyses/{code}.md','student_response_validation':False})
        node_ids = [f'F_{family["id"]}_{i:02}' for i in range(1, len(family['processes']) + 1)]
        for i, row in enumerate(entry['steps'], 1):
            label, thinking, observable = row.split('|')
            node_id = f'A_{code}_{i:02}'
            elements.append({'id':node_id,'label':label,'thinking':thinking,'observable':observable,'standards':[code],'status':'분석 초안'})
            node_ids.append(node_id)
        for i, node in enumerate(node_ids, 1):
            relations.append({'id':f'AN_{code}_P{i:02}','from':f'standard:{code}','to':f'element:{node}',
                'type':'has_subskill','scope':'대표 과제와 명시한 설명 경로에서의 목표 하위요소',
                'rationale':'이 목표의 수행을 구성하는 판단과 관찰 가능한 설명을 분해한다. ' + entry['idea'],
                'conditions':['대표 과제의 양과 표현 조건을 유지함'],
                'limit':'목표의 구성 분석이며 모든 학습자가 같은 순서로 획득한다는 주장이 아니다.',
                'evidence_kind':'인지적 분석 가설','source_ids':['CURRICULUM_2022_33'],'status':'초안'})
        for i, conn in enumerate(entry['connections'], 1):
            target, kind, mechanism, extra, condition = conn
            relations.append({'id':f'AN_{code}_C{i:02}','from':f'standard:{code}','to':f'standard:{target}',
                'type':kind,'scope':'초등의 출발 의미와 중고등의 추가 개념 사이 연결',
                'rationale':entry['bridge'] + ' ' + mechanism,'conditions':[condition],
                'additional_learning':[extra],
                'limit':'수학적 의미의 연결 초안이다. 이 관계만으로 선수의 필수성이나 교수 효과가 검증되지는 않는다.',
                'evidence_kind':'수학적 논증','source_ids':['CURRICULUM_2022_33'],'status':'초안'})
    registry.sort(key=lambda r:r['code'])
    save('data/analysis_registry.json', registry)
    elements_data.update(scope='초중고 분석의 공통 사고와 성취기준별 사고의 초안. 개별 학생의 발달 순서로 해석하지 않는다.', elements=elements)
    relations_data.update(scope='초중고 상세 초안의 하위요소 구성과 의미 연결. 명시한 경로와 조건을 유지한다.', relations=relations)
    save('data/elements.json', elements_data)
    save('data/relations.json', relations_data)
    for r in inventory['standards']:
        if r['code'] in elementary:
            r.update(analysis_status='초안', analysis_file=f'analyses/{r["code"]}.md')
    save('data/standards.json', inventory)
    write_indexes(inventory['standards'])
    elementary_registry = [r for r in registry if r['code'] in elementary]
    write_overview(entries, elementary_registry, by_code)
    assert all(hashlib.sha256((ROOT / f'analyses/{code}.md').read_bytes()).hexdigest() == old_hash[code] for code in PRESERVED)
    save('data/detailed_coverage.json', {'elementary_total':121,'drafts':len(elementary_registry),'new_drafts':len(entries),
        'preserved_pilots':sorted(PRESERVED),'families':len(families),'student_validated':0,
        'domain_counts':dict(Counter(by_code[r['code']]['domain'] for r in elementary_registry)),
        'content_source':'data/analysis_details.json','preserved_pilot_sha256':old_hash})
    print(json.dumps({'elementary_drafts':len(elementary_registry),'all_drafts':len(registry),'new':len(entries),'families':len(families),'elements':len(elements),'relations':len(relations)},ensure_ascii=False))


def render_entry(e, f, r, by_code, sources):
    code = e['code']
    out = [f'# {e["title"]} 상세 분석 초안','',e['idea'],'','## 교육과정과 수행 목표','',
        f'- 성취기준: **{code}**',f'- 원문: {r["statement_display"]}',
        f'- 범위: {r["grade_band"]} {r["domain"]}',
        f'- 원문 위치: PDF {r["source_pdf_pages"][0]}쪽, 인쇄 {r["source_printed_pages"][0]}쪽.',
        '- 상태: 수학적 분석과 교수 설계의 초안. 진단 과제와 학습 경로의 학생 반응 검증 전.',
        '',f'**대표 과제와 기대 수행:** {e["task"]}','',
        '[초등 전체 상세 분석](../indexes/초등전체상세분석.md) · [분석 규칙](../docs/분석규칙.md)',
        '', '## 수학적 의미와 성립 조건','', f['meaning'], '',
        '**이 성취기준의 범위와 경계:** ' + e['limit'], '',
        '## 개별 과제의 세부 사고','']
    out += table(['하위요소','판단과 구성','관찰 가능한 수행'], [x.split('|') for x in e['steps']])
    out += ['', '## 공통 사고와의 연결','']
    out += table(['공통 요소','이 과제에 적용할 관점','확인할 수행'],[x.split('|') for x in f['processes']])
    out += ['', '## 선수 조건과 대안 경로','']
    if e['precursors']:
        out += ['연결을 검토할 초등 목표: ' + ', '.join(f'[{c}]({c}.md)' for c in e['precursors']) + '.', '']
    out += ['조건 묶음은 개별 과제와 경로에서 검토한 경우에만 함께 필요한 조건으로 기록한다.', '',
        '조작으로 먼저 구성하는 경로와 관계 또는 표상에서 구성하는 경로는 대안(OR)이다. 한 경로에서 막히면 같은 의미를 다른 표현에서 구성할 수 있는지 확인한다.', '']
    out += [f'{i}. {p}' for i,p in enumerate(e.get('paths',f['paths']),1)]
    out += ['', '개별 과제 표의 판단을 이어서 말하게 하고, 중간에 기준이나 단위 및 대응 관계가 달라지지 않았는지 확인한다.']
    out += ['', '이 순서는 수업 설계의 한 선택이다. 실제 학생이 사용하는 다른 전략도 양과 관계가 유지되는지 검토한다.', '',
        '## 표현 사이의 대응','']
    out += table(['전환','유지하거나 새로 해석할 의미'],[x.split('|') for x in f['representations']])
    out += ['', '이 성취기준에 맞는 표현을 골라 양방향으로 옮겨 보게 한다. 수식이 아직 필요하지 않은 목표에서는 실물·그림·말의 대응을 먼저 본다. 읽기·그리기·도구 조작의 어려움이 개념의 어려움과 섞일 때는 같은 질문을 실물이나 구두 설명으로 확인한다.', '',
        '## 오류와 진단 및 후속 질문','']
    out += table(['진단 질문','기대하는 설명','다른 반응의 가능한 해석','후속 확인'],[x.split('|') for x in e['probes']])
    out += ['', '단일 오답에서 원인을 확정하지 않는다. 정답을 맞혀도 설명, 표현 변경, 비정형 사례에서 같은 의미를 유지하는지 추가로 확인한다.', '',
        '## 학습 활동과 발문','',
        '대표 과제를 계산이나 명칭 제시 전에 관찰·예상하게 하고, 서로 다른 두 설명을 비교한다. 피드백은 정답의 반복보다 위 표의 후속 확인으로 연결한다.', '',
        f'- 먼저 묻기: “{e["probes"][0].split("|")[0]}?”',
        f'- 뜻을 구별하기: “{e["probes"][1].split("|")[0]}?”',
        f'- 조건을 바꾸어 보기: “{e["probes"][2].split("|")[0]}?”',
        '- 돌아보기: 사용한 전략의 이유와 다른 방법을 비교하고, 답의 단위·범위·조건이 맞는지 설명한다.', '',
        '## 초등 내부와 중고등 수학의 연결','',e['bridge'],'']
    rows=[]
    for target,kind,mechanism,extra,condition in e['connections']:
        t=by_code[target]
        rows.append([f'{target} {t["subject"]} ({t["school_level"]})',KIND[kind],mechanism,extra,condition+f' 원문 PDF {t["source_pdf_pages"][0]}쪽.'])
    out += table(['도착 성취기준','관계','전환을 설명하는 구조','새로 필요한 개념','성립 조건과 원문 위치'],rows)
    out += ['', '고등 연결에서 변수·함수·논증·정의역·극한 등을 추가해야 하는 경우 그 단계를 건너뛴 직접 선수 관계로 표시하지 않는다. 직무 과목의 실제 적용과 일반 과목의 추상화를 같은 순서로 이수한다고 가정하지 않는다.', '',
        '## 근거와 후속 검토','',
        f'공식 목표와 범위의 근거는 교육부 고시 제2022-33호의 {code} 및 관련 해설이다. 세부 사고의 분해, 과제, 위 연결의 논증은 이 연구에서 작성한 분석이다.', '',
        '공통 관점의 참고 자료: ' + ', '.join(f'[{sources[s]["title"]}]({sources[s]["url"]})' for s in f['source_ids']) + '.', '',
        '[자료별 확인 범위](../docs/연구자료.md)를 함께 본다. 해당 문헌을 참고했다는 사실이 이 과제의 진단 정확도나 교수 효과를 입증하지는 않는다.', '',
        '후속 검토에서는 대표 과제와 후속 질문의 실제 반응을 비교하고, 다른 전략과 반례 및 표현의 부담을 확인한다. 검토 완료와 학생 반응 검증은 상세 초안 작성과 별도 상태로 관리한다.', '']
    (ROOT / f'analyses/{code}.md').write_text('\n'.join(out),encoding='utf-8')


def write_overview(entries, registry, by_code):
    by_entry={e['code']:e for e in entries}
    out=['# 초등 수학 전체 상세 분석 안내','',
        '초등 121개 성취기준 모두에 세부 사고와 진단 및 중고등 연결을 포함하는 상세 초안을 작성했다. 기존 세 초안은 보존하고 나머지 118개를 추가했다. 학생 반응으로 검증된 학습 경로와 진단 도구의 완료를 뜻하지 않는다.','',
        '[프로젝트 안내](../README.md) · [진행 현황](진행현황.md) · [중고등 연결 지도](초중고연결지도.md)','']
    for domain in ['수와 연산','변화와 관계','도형과 측정','자료와 가능성']:
        subset=[r for r in registry if by_code[r['code']]['domain']==domain]
        out += ['', f'## {domain}', '']
        rows=[]
        for r in subset:
            code=r['code']
            title=by_entry[code]['title'] if code in by_entry else {'6수01-10':'나눗셈의 몫과 분수','6수02-03':'비율의 여러 표현','6수03-14':'여러 평면도형의 넓이'}[code]
            rows.append([code,by_code[code]['grade_band'],f'[{title}](../{r["file"]})','초안'])
        out += table(['코드','학년군','상세 분석','상태'],rows)
    (ROOT/'indexes/초등전체상세분석.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
    out=['# 초등에서 중고등으로 이어지는 수학 연결 지도','',
         '각 출발 목표에서 어떤 사고가 유지되고 무엇이 새로 필요한지 설명하는 경로를 모았다. 의미 연결과 확장은 모든 학습자에게 필요한 고정된 선수 순서를 뜻하지 않는다. 공식 성취기준의 코드는 전체 목록과 대조했다.','',
         '[전체 상세 분석](초등전체상세분석.md) · [중학교 원문 목록](중학교성취기준.md) · [고등학교 원문 목록](고등학교성취기준.md)','']
    for domain in ['수와 연산','변화와 관계','도형과 측정','자료와 가능성']:
        out += ['', f'## {domain}', '']
        rows=[]
        for r in registry:
            code=r['code']
            if by_code[code]['domain']!=domain: continue
            if code in by_entry:
                e=by_entry[code]
                mid=[x[0] for x in e['connections'] if by_code[x[0]]['school_level']=='중학교']
                high=[x[0] for x in e['connections'] if by_code[x[0]]['school_level']=='고등학교']
                bridge=e['bridge']
            else:
                mid,high,bridge={
                  '6수01-10':(['9수01-03','9수01-05'],['10공수2-03-04'],'몫을 수로 읽기에서 유리수와 변수의 몫으로 확장하며 부호·함수·정의역을 추가한다.'),
                  '6수02-03':(['9수02-07','9수02-16','9수04-03'],['10공수2-01-01','12미적Ⅰ-02-01'],'기준량의 비에서 공변과 변화량의 비로 전환하고 함수·극한을 추가한다.'),
                  '6수03-14':(['9수03-11','9수03-12'],['12미적Ⅰ-03-05'],'분해·합성과 넓이 보존을 도형의 논증 및 곡선 영역으로 확장하고 함수·극한·정적분을 추가한다.')
                }[code]
            assert mid and high
            rows.append([f'[{code}](../analyses/{code}.md)',', '.join(mid),', '.join(high),bridge])
        out += table(['출발 성취기준','중등 도착','고등 도착','사고의 전환과 추가 학습'],rows)
    (ROOT/'indexes/초중고연결지도.md').write_text('\n'.join(out)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()

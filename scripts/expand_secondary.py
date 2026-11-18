"""Render 314 middle/high analyses without rewriting elementary analyses."""
from __future__ import annotations
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from build_inventory import write_indexes

ROOT = Path(__file__).resolve().parents[1]
MID = {'number':'9수01-03','algebra':'9수02-19','equation':'9수02-20','inequality':'9수02-12',
       'function':'9수02-14','geometry':'9수03-04','measure':'9수03-08','stats':'9수04-04',
       'probability':'9수04-06','counting':'9수04-05','matrix':'9수02-13','coordinate':'9수02-05',
       'logic':'9수03-11','exponential':'9수02-08','trig':'9수03-16','sequence':'9수02-14',
       'limit':'9수02-06','derivative':'9수02-16','integral':'9수03-08','conic':'9수03-15',
       'vectors':'9수02-05','finance':'9수02-07','optimization':'9수02-12','ai':'9수04-09',
       'job':'9수02-06','culture':'9수04-04','inference':'9수04-07','research':'9수04-04'}


def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def table(headers, rows):
    def cell(x):
        return str(x).replace('|','\\|').replace('\n',' ')
    return ['| '+' | '.join(headers)+' |','|'+'|'.join('---' for _ in headers)+'|']+[
        '| '+' | '.join(cell(c) for c in row)+' |' for row in rows]


def freeze():
    import secondary_middle, secondary_middle_space_data, secondary_common, secondary_basic
    import secondary_algebra_trig_sequence, secondary_calculus, secondary_probability_geometry
    import secondary_economy_ai, secondary_work_culture, secondary_statistics_research
    from secondary_profiles import ENTRIES, PROFILES
    from secondary_adjustments import apply_adjustments
    apply_adjustments(ENTRIES, PROFILES)
    save('data/secondary_analysis_details.json', {
        'scope':'중학교 60개와 고등학교 15과목 254개 전체의 수학적 분석 및 교수 설계 초안.',
        'source':'제공된 교육부 고시 제2022-33호에 범위를 고정한다.',
        'interpretation':'공유한 개념 관점과 목표별 과제 및 사고를 구별한다. 기본과 공통 과목은 평행 분기이며 공유 논증은 별도 표시한다.',
        'profiles':PROFILES,'analyses':ENTRIES})


def add_sources():
    sources=read('data/sources.json')
    more=[
      dict(id='IES_ALGEBRA_2015',title='Teaching Strategies for Improving Algebra Knowledge in Middle and High School Students',
           year=2015,kind='공식 교수 가이드',url='https://ies.ed.gov/ncee/wwc/practiceguide/20',
           review_scope='공식 소개와 세 권고 및 근거 수준 확인. 풀이 사례 분석과 식 구조 활용은 Minimal, 대안 전략의 의도적 선택은 Moderate로 제시됨. 개별 원연구 전부를 읽은 상태는 아님.',
           supports=['풀이 전략 비교','대수 표현의 구조 분석'],does_not_establish='이 프로젝트의 개별 과제 효과와 진단 정확도'),
      dict(id='OPENSTAX_CALC_DERIVATIVE',title='Calculus Volume 1 Section 3.1 Defining the Derivative',year=2016,
           kind='공개 수학 교재',url='https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative',
           review_scope='할선과 차분몫의 정의 및 미분계수 도입 대목 확인.',supports=['차분몫의 조건과 접선 해석'],does_not_establish='국내 학습자의 인지 발달 순서'),
      dict(id='OPENSTAX_CALC_FTC',title='Calculus Volume 1 Section 5.3 The Fundamental Theorem of Calculus',year=2016,
           kind='공개 수학 교재',url='https://openstax.org/books/calculus-volume-1/pages/5-3-the-fundamental-theorem-of-calculus',
           review_scope='정리 도입과 미분 적분의 관계 및 연속 함수의 조건 확인.',supports=['누적과 원시함수의 연결'],does_not_establish='구분구적을 미적분Ⅰ의 필수 선수로 둘 근거'),
      dict(id='OPENSTAX_STATS_INTERVAL',title='Introductory Statistics 2e Section 8.3 A Population Proportion',year=2023,
           kind='공개 통계 교재',url='https://openstax.org/books/introductory-statistics-2e/pages/8-3-a-population-proportion',
           review_scope='표본비율 모형과 표준오차 및 정규근사 신뢰구간의 조건 대목 확인.',supports=['모수와 통계량 및 비율 추정의 구별'],does_not_establish='모든 상황에서 한 근사 구간을 써도 된다는 주장'),
      dict(id='OPENSTAX_STATS_TEST',title='Introductory Statistics 2e Sections 9 Introduction and 9.2 Outcomes and Errors',year=2023,
           kind='공개 통계 교재',url='https://openstax.org/books/introductory-statistics-2e/pages/9-2-outcomes-and-the-type-i-and-type-ii-errors',
           review_scope='가설검정 도입 및 제1종 제2종 오류의 조건부 확률 정의 확인.',supports=['귀무가설 아래의 확률과 판정 오류 구별'],does_not_establish='특정 실생활 가설의 진위')]
    known={s['id'] for s in sources}
    sources.extend(s for s in more if s['id'] not in known)
    save('data/sources.json',sources)
    return {s['id']:s for s in sources}


def link(code):
    return f'[{code}]({code}.md)'


def render(e,p,s,by_code,entries,sources):
    c=e['code'];is_high=s['school_level']=='고등학교'
    out=[f'# {e["title"]} 상세 분석 초안','',e['idea'],'','## 교육과정과 수행 목표','',
         f'- 성취기준: **{c}**',f'- 원문: {s["statement_display"]}',
         f'- 범위: {s["school_level"]} {s["subject"]} {s["domain"]}',
         f'- 원문 위치: PDF {s["source_pdf_pages"][0]}쪽, 인쇄 {s["source_printed_pages"][0]}쪽.',
         '- 상태: 수학적 분석과 교수 설계의 초안. 학생 반응 검증 전。'.replace('。','.'),'',
         f'**대표 과제와 기대 수행:** {e["task"]}','',
         '[중고등 전체 상세 분석](../indexes/중고등전체상세분석.md) · [분석 규칙](../docs/분석규칙.md)','',
         '## 수학적 의미와 성립 조건','',p['meaning'],'',
         '**이 목표의 핵심:** '+e['idea'],'',
         '**대표 과제의 조건:** '+p['conditions'],'',
         '**교육과정 범위와 선택한 사례:** '+e['limit'],'','## 개별 과제의 세부 사고','']
    out+=table(['요소','구성할 사고','판단과 이해를 드러내는 수행'],[[i,name,text] for i,(name,text) in enumerate(e['steps'],1)])
    if e.get('branches'):
        out+=['','### 한 성취기준 안의 하위 목표','']
        out+=table(['하위 목표','별도로 구성할 사고','확인 과제'],e['branches'])
    out+=['','이 표는 대표 과제를 설명하기 위한 분해다. 수행의 성공은 해당 판단의 단서이며, 언어나 도구의 부담과 분리하여 해석한다.','',
          '## 선수 조건과 대안 경로','',
          '조건 묶음은 개별 과제와 경로에서 검토한 경우에만 함께 필요한 조건으로 기록한다.','',
          '다음 경로들은 선택 가능한 접근(OR)이다. 결과가 같은 이유와 유지되는 정의를 비교한다.','']
    out += [f'{i}. {path}' for i,path in enumerate(p['paths'],1)]
    if e.get('shared_argument_from'):
        out+=['',f'공유한 수학적 논증: {link(e["shared_argument_from"])}. 유사 목표의 원리를 재사용하되 대표 과제와 범위는 이 과목의 조건을 따른다. 두 과목을 순차 이수하는 선수 관계로 기록하지 않는다.']
    out+=['','관련 이전 목표는 아래 연결 표에서 확인한다. 같은 개념도 기호 계산, 도형 구성, 자료 해석 중 선택한 경로에 따라 필요한 출발점이 달라진다.','',
          '## 표현 사이의 대응','']
    out+=table(['관점','확인할 대응'],[[i,x] for i,x in enumerate(p['representations'],1)])
    out+=['','대표 과제의 결과를 한 번은 다른 표현으로 다시 구성하게 한다. 도구가 준 결과는 입력 조건과 원래 의미에 되돌려 확인하며, 설명이 어려울 때 같은 질문을 구두·그림·작은 수의 사례로 바꿔 확인한다.','',
          '## 오류와 진단 및 후속 질문','']
    out+=table(['목표별 진단 질문','기대하는 설명','다른 반응의 가능한 해석','후속 확인'],e['probes'])
    out+=['','다음은 이 개념군에서 추가로 선택할 수 있는 공통 진단이다. 대표 과제와 관련되는 경우에 사용하며, 앞의 개별 진단과 같은 지위를 가진 고정된 문항으로 강제하지 않는다.','']
    out+=table(['공통 진단 질문','판단할 의미','가능한 혼동','후속 확인'],[e.get('common_probe',p['probe'])])
    out+=['','단일 오답으로 사고의 결여를 확정하지 않는다. 정답 뒤의 이유, 조건을 바꾼 반례, 다른 표상에서의 유지 여부를 비교한다.','',
          '## 학습 활동과 발문','',
          f'1. 대표 과제를 제시하고 계산 전에 “{e["probes"][0][0]}”를 예상하게 한다.',
          f'2. **{e["steps"][0][0]} → {e["steps"][1][0]} → {e["steps"][2][0]} → {e["steps"][3][0]}**의 판단을 소리 내어 설명하고 각 변환의 근거를 표시하게 한다.',
          '3. 선택한 다른 경로와 결과를 비교하고 표현이 바뀌어도 보존되는 양이나 정의를 찾는다.',
          f'4. “{e["probes"][1][0]}”로 조건을 다시 확인하고 후속 질문의 반응에 따라 피드백을 정한다.',
          '5. 무엇이 계산 절차이고 무엇이 성립 조건인지 구별하여 새 사례에 적용한다.','',
          '## 초등에서 오는 의미와 중간 개념','',
          '아래 출발점은 의미의 계보를 설명한다. 초등 목표에서 현재 목표로 직접 건너뛰는 선수 관계가 아니다. 추가되는 정의와 표현을 중간에서 구성해야 한다.','']
    anchor_rows=[]
    for ac,why in e.get('anchors',p['anchors']):
        middle=MID[e['family']] if is_high else c
        bridge=f'{middle} {by_code[middle]["domain"]}' if is_high else '현재 목표에서 새로 정의하는 개념'
        anchor_rows.append([link(ac),by_code[ac]['statement_display'],why,bridge,e['idea']])
    out+=table(['초등 출발','실제 공식 목표','유지하거나 바꾸는 의미','중간 점검 지점','여기서 새로 구성할 사고'],anchor_rows)
    out+=['','중간 점검 지점은 선택 가능한 개념 참조다. 과목의 법정 이수 순서나 모든 학생에게 필요한 유일한 경로를 뜻하지 않는다.','',
          '## 이전 목표와 후속 및 분기 연결','']
    connection_rows=[]
    for direction,items in [('이전 의미',e['prior']),('후속 또는 분기',e['onward'])]:
        for target,why in items:
            t=by_code[target]
            extra=entries[target]['idea'] if target in entries else t['statement_display']
            connection_rows.append([direction,link(target),t['subject'],why,extra])
    if connection_rows:
        out+=table(['방향','성취기준','과목','왜 이어지는가','새로 확인할 의미와 조건'],connection_rows)
    else:
        out+=['새 공식 성취기준으로의 연결을 억지로 추가하지 않는다. 현재 수행의 다른 표현과 적용에서 전이를 검토한다.']
    if not e['onward']:
        out+=['','이 목표는 수행을 평가하고 다음 탐구 질문을 만드는 분기다. 반드시 새 내용 과목으로 진행해야 하는 종착 목표로 해석하지 않는다.']
    out+=['', '**연결을 사용할 조건:** '+p['conditions']+' '+e['limit'],'',
          '고등의 공통·기본·일반·진로·융합 과목은 분기로 본다. 같은 주제를 다뤄도 학습 깊이와 평가 범위가 달라, 코드 연결만으로 필수 선수나 수업 효과를 주장하지 않는다.','',
          '## 근거와 후속 검토','',
          f'공식 수행 목표의 근거는 교육부 고시 제2022-33호 {c}와 해당 해설이다. 대표 과제, 세부 사고, 대안 경로와 연결 설명은 자체 수학적 분석 및 교수 설계 초안이다.','']
    refs=p.get('sources',[])
    if refs:
        out+=['공통 관점의 참고 자료: '+', '.join(f'[{sources[x]["title"]}]({sources[x]["url"]})' for x in refs)+'.','']
    out+=['[자료별 확인 범위](../docs/연구자료.md)를 함께 본다. 수학 교재는 정의와 정리의 참고이며 인지 발달 순서의 실증 근거로 취급하지 않는다. 개별 문항의 진단 정확도와 교수 효과는 실제 학생 반응 자료로 별도 검토한다.','',
          '후속 검토는 수학적 반례와 원문 범위, 서로 다른 전략, 표상의 부담을 함께 확인한다. 초안 작성·검토 완료·학생 반응 검증은 별도 상태로 관리한다.','']
    (ROOT/f'analyses/{c}.md').write_text('\n'.join(out)+'\n',encoding='utf-8')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if '--freeze-content' in sys.argv:
        freeze()
    data=read('data/secondary_analysis_details.json')
    entries={e['code']:e for e in data['analyses']};profiles=data['profiles']
    inventory=read('data/standards.json');by_code={s['code']:s for s in inventory['standards']}
    expected={c for c,s in by_code.items() if s['school_level']!='초등학교'}
    assert len(data['analyses'])==len(entries)==314 and set(entries)==expected
    elementary={c for c,s in by_code.items() if s['school_level']=='초등학교'}
    hashes={c:hashlib.sha256((ROOT/f'analyses/{c}.md').read_bytes()).hexdigest() for c in elementary}
    sources=add_sources()
    element_data=read('data/elements.json');relation_data=read('data/relations.json')
    elements=[e for e in element_data['elements'] if not e['id'].startswith('S_')]
    relations=[r for r in relation_data['relations'] if not r['id'].startswith('SEC_')]
    registry=[r for r in read('data/analysis_registry.json') if r['code'] not in expected]
    for code,e in entries.items():
        p=profiles[e['family']]
        assert len(e['steps'])>=4 and all(len(r)==2 for r in e['steps']),code
        assert len(e['probes'])>=2 and all(len(r)==4 for r in e['probes']),code
        assert len(p['probe'])==4 and len(p['paths'])==2 and len(p['representations'])==3
        assert all(t in by_code and t!=code for t,m in e['prior']+e['onward']),code
        render(e,p,by_code[code],by_code,entries,sources)
        for i,(name,performance) in enumerate(e['steps'],1):
            eid=f'S_{code}_{i:02}'
            elements.append(dict(id=eid,label=name,thinking=e['idea'],observable=performance,standards=[code],status='분석 초안'))
            relations.append(dict(id=f'SEC_{code}_P{i:02}', **{'from':f'standard:{code}','to':f'element:{eid}'},
                type='has_subskill',scope='대표 과제에서 구성하는 목표의 하위요소',rationale=performance,
                conditions=[e['limit']],limit='목표 구성의 분해이며 필수적인 학습 획득 순서가 아니다.',
                evidence_kind='인지적 분석 가설',source_ids=['CURRICULUM_2022_33'],status='초안'))
        for i,(name,thinking,performance) in enumerate(e.get('branches',[]),1):
            eid=f'S_{code}_B{i:02}'
            elements.append(dict(id=eid,label=name,thinking=thinking,observable=performance,standards=[code],status='분석 초안'))
            relations.append(dict(id=f'SEC_{code}_B{i:02}', **{'from':f'standard:{code}','to':f'element:{eid}'},
                type='has_subskill',scope='복합 성취기준 안의 별도 하위 목표',rationale=thinking,
                conditions=[e['limit']],limit='목표의 내용 분기이며 단일한 수행 순서나 발달 순서가 아니다.',
                evidence_kind='인지적 분석 가설',source_ids=['CURRICULUM_2022_33'],status='초안'))
        links=[(a,code,m,'초등에서 오는 간접적 의미 연결') for a,m in e.get('anchors',p['anchors'])]
        links += [(a,code,m,'이전 목표와 의미 연결') for a,m in e['prior']]
        links += [(code,b,m,'후속 또는 평행 분기와 의미 연결') for b,m in e['onward']]
        for i,(a,b,why,scope) in enumerate(links,1):
            assert a!=b
            relations.append(dict(id=f'SEC_{code}_C{i:02}', **{'from':f'standard:{a}','to':f'standard:{b}'},
                type='meaning_connection',scope=scope,rationale=why,conditions=[p['conditions'],e['limit']],
                additional_learning=[entries[b]['idea'] if b in entries else by_code[b]['statement_display']],
                intermediate_standards=[MID[e['family']]] if scope.startswith('초등') and by_code[code]['school_level']=='고등학교' else [],
                limit='수학적 의미의 연결 초안. 필수 선수 관계나 과목의 이수 순서 및 교수 효과를 뜻하지 않는다.',
                evidence_kind='수학적 분석',source_ids=['CURRICULUM_2022_33'],status='초안'))
        registry.append(dict(code=code,status='초안',file=f'analyses/{code}.md',student_response_validation=False))
        by_code[code].update(analysis_status='초안',analysis_file=f'analyses/{code}.md')
    registry.sort(key=lambda x:x['code'])
    save('data/analysis_registry.json',registry)
    save('data/standards.json',inventory)
    element_data.update(scope='초중고 435개 상세 분석의 목표별 사고. 실제 학습자의 발달 순서는 별도 검증한다.',elements=elements)
    relation_data.update(scope='초중고의 목표 분해와 조건을 명시한 의미 연결. 과목 분기 및 중간 개념을 유지한다.',relations=relations)
    save('data/elements.json',element_data);save('data/relations.json',relation_data)
    write_indexes(inventory['standards'])
    write_secondary_indexes(entries,by_code)
    assert all(hashlib.sha256((ROOT/f'analyses/{c}.md').read_bytes()).hexdigest()==h for c,h in hashes.items())
    save('data/secondary_coverage.json',dict(middle=60,high=254,total=314,profiles=len(profiles),
        subjects=dict(Counter(by_code[c]['subject'] for c in entries if by_code[c]['school_level']=='고등학교')),
        goal_specific_steps=sum(len(e['steps']) for e in entries.values()),goal_specific_probes=sum(len(e['probes']) for e in entries.values()),
        additional_goal_branches=sum(len(e.get('branches',[])) for e in entries.values()),
        elementary_files_preserved_sha256=hashes,student_validated=0,reviewed=0,
        source_content='data/secondary_analysis_details.json'))
    print(json.dumps(dict(secondary_drafts=len(entries),all_drafts=len(registry),elements=len(elements),relations=len(relations)),ensure_ascii=False))


def write_secondary_indexes(entries,by_code):
    out=['# 중고등 수학 전체 상세 분석 안내','',
         '중학교 60개와 고등학교 15개 과목 254개 전체의 상세 분석 초안이다. 목표별 대표 과제와 사고, 조건, 진단, 초등에서 오는 의미 및 이후 분기를 정리한다.','',
         '[프로젝트 안내](../README.md) · [초등 상세 분석](초등전체상세분석.md) · [전 학교급 연결](전학교급연결지도.md) · [진행 현황](진행현황.md)','']
    for level in ['중학교','고등학교']:
        out+=['',f'## {level}','']
        groups=[]
        for c,s in by_code.items():
            if s['school_level']==level:
                group=s['domain'] if level=='중학교' else s['subject']
                if group not in groups:groups.append(group)
        for g in groups:
            out+=['',f'### {g}','']
            rows=[]
            for c,s in by_code.items():
                if c in entries and s['school_level']==level and (s['domain'] if level=='중학교' else s['subject'])==g:
                    rows.append([c,f'[{entries[c]["title"]}](../analyses/{c}.md)',s['domain'],s['source_pdf_pages'][0],'초안'])
            out+=table(['코드','목표별 상세 분석','영역','PDF 쪽','상태'],rows)
    (ROOT/'indexes/중고등전체상세분석.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
    out=['# 전 학교급 수학 연결 지도','',
         '초등의 출발 의미와 중고등 목표별 새 사고 및 후속 분기를 함께 읽는 색인이다. 표의 연결은 의미와 수학적 구조의 분석이며 모든 학생에게 같은 선수 순서를 주장하지 않는다.','',
         '[초등에서 출발하는 지도](초중고연결지도.md) · [중고등 상세 분석](중고등전체상세분석.md)','']
    profiles=read('data/secondary_analysis_details.json')['profiles']
    current=None
    for c,s in by_code.items():
        if c not in entries:continue
        g=s['school_level']+' '+(s['domain'] if s['school_level']=='중학교' else s['subject'])
        if g!=current:
            out+=['',f'## {g}','','| 현재 목표 | 초등 의미 출발 | 목표의 새 사고 | 이전 및 후속 분기 |','|---|---|---|---|'];current=g
        e=entries[c];p=profiles[e['family']]
        prior='; '.join(f'{a}: {m}' for a,m in e['prior'])
        onward='; '.join(f'{b}: {m}' for b,m in e['onward']) or '평가 후 새 탐구 질문으로 분기'
        row=[f'[{c} {e["title"]}](../analyses/{c}.md)',', '.join(a for a,m in e.get('anchors',p['anchors'])),e['idea'],prior+' → '+onward]
        out+=table(['','','',''],[row])[2:]
    (ROOT/'indexes/전학교급연결지도.md').write_text('\n'.join(out)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()

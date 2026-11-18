"""Write the completion report only after the complete corpus checks pass."""
from pathlib import Path
import json
from collections import Counter
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
coverage=read('data/revision_coverage.json');checks=read('data/revision_checks.json');quality=read('data/revision_quality.json')
assert coverage['individually_revised']==432 and checks['status']==quality['status']=='pass'
standards={s['code']:s for s in read('data/standards.json')['standards']}
relations=[r for r in read('data/revised_relations.json')['relations'] if r['from'].startswith('standard:') and r['to'].startswith('standard:')]
rows=[]
for level,n in [('초등학교',121),('중학교',60),('고등학교',254)]:
 local=[r for r in relations if standards[r['from'][9:]]['school_level']==standards[r['to'][9:]]['school_level']==level]
 directional=[r for r in local if r['type'] in ['generalizes','requires_for_task'] and r.get('review_state')=='self_checked']
 touched={r[k][9:] for r in local for k in ['from','to']}
 rows.append(f'| {level} | {n} | {len(local)} | {len(directional)} | {len(touched)} |')
text='''# 학교급별 탐색과 전체 상세 분석 정비 결과

작성일: 2026년 10월 29일

초등 121개·중학교 60개·고등학교 254개, 전체 435개 상세 분석을 공통 12개 절로 정리했다. 초기 초등 세 사례의 원문을 별도 보존하고 구체적인 과제·정당화·경로·진단을 새 체계에 유지했다. 나머지 432개는 목표별 실제 과제 풀이와 조건·사고의 이유·표현·진단·학교급 내부 관계를 개별 보강했다.

## 학교급별 보기

상단의 전체·초등·중등·고등 선택은 지도·검색·개념 목록·연결과 위계에 공통으로 적용한다. 선택 범위 밖의 노드와 양 끝이 범위에 속하지 않는 연결은 제외하며, 주소·메뉴 이동·상세 왕복에서 학교급을 유지한다. 직접 상세 링크로 범위 밖 문서를 열면 대상 학교급과 현재 범위를 구별해 안내한다.

학교급 내부 지도는 자체 분석한 의미 확장과 과제별 조건에 따라 상대 단계를 배치한다. 방향 미기록과 순환 검토 대상은 순서 미정에 둔다. 학년군·코드·과목 순서에서 화살표를 추정하지 않는다. 다른 학교급의 연결은 선택해서 펼친다. 과제별 시범 위계의 전체 AND 묶음은 일부 조건을 숨겨도 보존한다.

## 문서의 공통 체계

공식 성취기준과 범위, 핵심 의미와 목표 수행, 대표 과제와 성공한 수행, 수학적 의미와 성립 조건, 세부 사고와 관찰할 수행, 수행 과정과 대안 경로, 표현 사이의 대응, 오류와 진단, 학습 활동과 피드백, 같은 학교급 내부 관계, 다른 학교급 연결, 근거와 검토 상태를 모든 기준에 적용한다.

소인수분해에 들어간 분모·제곱근 조건을 개별 과제의 조건으로 바로잡았다. 초등·중등 측정 프로필 충돌, 첫 두 사고 요소의 자동 AND 서술, 제목 판별에 따른 중복 표시를 수정했다. 관찰 수행을 되풀이한 이유 문장을 오류·불변량·정당화에 관한 설명으로 교정했다. 복합 목표는 하위 목표별 해설과 진단을 추가했다.

## 학교급 내부 관계

| 범위 | 성취기준 | 내부 관계 기록 | 새 방향 관계 자체 점검 | 내부 관계에 닿는 기준 |
|---|---:|---:|---:|---:|
'''+ '\n'.join(rows)+f'''

전체 성취기준 간 관계 기록은 {len(relations)}건이다. 기존 1,518건의 ID·이유·한계와 수정 전 조건을 보존하며 새 기록은 별도 ID로 구별했다. 기록 수는 고유한 두 기준의 쌍 수와 다르다. 검토 후보는 방향 없는 연결로 유지한다. 접선의 대안 풀이 비교를 서로의 필수 확장처럼 표시한 관계와 구의 방정식·부피 연결의 방향을 교정했다.

## 검증과 적용 범위

자료 버전은 `{checks['version']}`이다. 전수 검사는 435개 포함, 12개 절, 원문과 출처, 필수 필드와 참조, 기존 관계 보존, 네 학교급 범위, 위치 중복과 방향 배치, 조건 묶음, 분리 로딩, 검색과 과목 필터, 상세 렌더링을 통과했다. 초기 세 사례의 보존 원본은 이전 문서의 SHA256과 일치한다.

수학적 자체 분석과 내용 보강은 초안 상태로 제공한다. 독립적인 교사·연구자 검토와 학생 반응 검증은 0건이며, 자동 검사는 그 검증을 대신하지 않는다. 순서 미정과 검토 후보를 학습 선수성이 없는 기준으로 해석하지 않는다.

## 원본과 갱신

- [개별 보강과 항목 검사](../data/revision_quality.json)
- [435개 기준별 보강 현황](../data/revision_coverage.json)
- [전체 검사 결과](../data/revision_checks.json)
- [보존한 초기 세 사례](../data/initial_case_studies.json)
- [원래 관계와 새 관계의 통합본](../data/revised_relations.json)
- [공통 상세 분석 양식](성취기준분석양식.md)

개별 편집은 `data/revisions_*.json`에 반영한다. `scripts/run_revision_checks.py`를 실행하면 내용 구조 검사, 문서·포털 동시 생성과 전체 검사를 수행한다. 기존 원고 생성기를 사용한 뒤에도 이 통합 과정을 실행하여 개별 보강을 유지한다. 배포 소스는 `tmp/pathways-release`이며 재현용 자료와 생성기는 그 저장소의 `research` 폴더에도 포함한다.
'''
(R/'docs/학교급별탐색과전체상세분석정비결과.md').write_text(text,encoding='utf-8')
print('completion report written')

index=['# 학교급 내부 관계와 위계 색인','','435개 모든 기준에서 같은 학교급 내부의 방향 관계와 의미 연결을 찾아본다. 방향은 자체 분석한 의미 확장과 과제별 조건에 한정하며 고정된 학습·이수 순서가 아니다. 연결 이유와 조건은 각 상세 문서에서 읽는다.','','[전체 정비 결과](../docs/학교급별탐색과전체상세분석정비결과.md) · [공통 분석 양식](../docs/성취기준분석양식.md)','']
for level in ['초등학교','중학교','고등학교']:
 index+=['## '+level,'','| 기준과 상세 | 앞선 의미·과제 조건 | 이후 확장·과제 조건 | 순서가 정해지지 않은 연결 |','|---|---|---|---|']
 for code,s in standards.items():
  if s['school_level']!=level:continue
  before=set();after=set();related=set()
  for r in relations:
   a,b=r['from'][9:],r['to'][9:]
   if code not in [a,b] or standards[a]['school_level']!=standards[b]['school_level']:continue
   if r['type'] in ['generalizes','requires_for_task'] and r.get('review_state')=='self_checked':
    (after if a==code else before).add(b if a==code else a)
   else:related.add(b if a==code else a)
  def links(ids):return ' · '.join('['+c+'](../analyses/'+c+'.md)' for c in sorted(ids)) or '방향 미기록' 
  index.append('| ['+code+'](../analyses/'+code+'.md) | '+links(before)+' | '+links(after)+' | '+(links(related) if related else '연결 미기록')+' |')
 index+=['']
(R/'indexes/학교급내부위계.md').write_text('\n'.join(index)+'\n',encoding='utf-8')

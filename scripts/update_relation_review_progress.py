"""Update living report counts from a verified run; this never approves a review."""
import argparse,json,re
from pathlib import Path
from relation_analysis_review import ROOT,load_reviews,materials

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--log',type=Path,required=True);parser.add_argument('--date',required=True);parser.add_argument('--batch-label',required=True);parser.add_argument('--batch-kind',choices=['relation','literature'],default='relation');args=parser.parse_args()
 assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',args.date)
 read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
 checks=read('data/revision_checks.json');audit=read('data/hierarchy_completion_audit.json');site=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
 catalog=json.loads((site/'dist/content/catalog.json').read_text(encoding='utf-8'))
 assert checks['status']=='pass' and checks['version']==audit['source_version']==catalog['version']
 log=args.log.read_text(encoding='utf-8')
 assert 'All revision checks passed' in log and checks['version'] in log,'The log must prove this content version passed'
 queue=read('data/relation_analysis_scope_queue.json');states=queue['summary']['analysis_states'];priority=queue['summary']['by_priority'];pending=queue['summary']['queued']
 assert states==audit['summary']['standard_relation_review_states'] and not states.get('missing',0)
 records=load_reviews()['records'];original=materials()['raw'];count=len(records);corrections=sum(r['type']!=original[rid]['type'] for rid,r in records.items())
 assert count==queue['summary']['durable_scoped_math_reviews'] and not set(records)&{r['relation_id'] for r in queue['records']}
 literature=read('data/literature_claim_reviews.json');sources=len(literature['sources']);claims=len(literature['claims']);observations=sum(len(s.get('observations',[])) for s in literature['sources'].values())
 review_queue=read('data/content_review_queue.json');literature_pending=sum(row['source']['id']!='CURRICULUM_2022_33' and row['status']!='self_read_claim_mapping' for row in review_queue['literature_review'])
 external_total=sum(row['source']['id']!='CURRICULUM_2022_33' for row in review_queue['literature_review']);assert sources+literature_pending==external_total
 coverage=review_queue['source_review_scope_summary'];assert coverage['full_scope_reviewed']==435 and coverage['full_scope_pending']==0
 hierarchy_count=len(read('data/hierarchy_review_registry.json')['relations']);version=checks['version']
 p=ROOT/'docs/전체자료보완진행.md';text=p.read_text(encoding='utf-8')
 year,month,day=map(int,args.date.split('-'))
 text,n=re.subn(r'\d{4}년 \d{1,2}월 \d{1,2}일 현재,',f'{year}년 {month}월 {day}일 현재,',text,count=1);assert n==1
 text=re.sub(r'최종 생성·검사 버전은 `[a-f0-9]{16}`다\.',f'최종 생성·검사 버전은 `{version}`다.',text)
 text,n=re.subn(r'교육과정 외 출처는\d+개에 명시한 읽기 범위와 주장\d+건의 근거를 대응했고, 추가 관찰\d+건을 반영했다\. (?:나머지\d+개 출처의 주장 대응과 실제 검증 등 아래 완료 조건은 계속 진행한다|초기 주장 대응 대기는\d+개이며, 출처별 미검토 범위의 후속 대조와 실제 검증 등 아래 완료 조건은 계속 진행한다)\.',f'교육과정 외 출처는{sources}개에 명시한 읽기 범위와 주장{claims}건의 근거를 대응했고, 추가 관찰{observations}건을 반영했다. 초기 주장 대응 대기는{literature_pending}개이며, 출처별 미검토 범위의 후속 대조와 실제 검증 등 아래 완료 조건은 계속 진행한다.',text);assert n==1
 literature_row=f'| 문헌의 범위별 읽기와 주장 대응 | 교육과정의 표·기준 대조 완료; 외부{external_total}개 중{sources}개 출처의 명시한 범위 읽기·주장{claims}건 대응, 나머지{literature_pending}개 초기 대응 대기; 검토한 출처의 미검토 부분·원연구 등 후속 대조도 별도 기록 | 원문 위치·연구 대상·방법·결과·한계와 관련 주장 ID |'
 text,n=re.subn(r'^\| (?:문헌 정독과 주장별 대응|문헌의 범위별 읽기와 주장 대응) \|.*$',lambda _:literature_row,text,flags=re.M);assert n==1
 row=f"| 기준 간 관계의 검토 상태 정리 | 자체 분석 표기{states.get('self_checked',0):,}건·후보{states.get('candidate',0):,}건·이전 초안{states.get('legacy_draft',0):,}건; 별도 위계 원장{hierarchy_count:,}건·개별 수학 검토{count:,}건 | [개별 범위 검토 대기{pending:,}건](../data/relation_analysis_scope_queue.json): 1순위{priority.get('1',0):,}건·2순위{priority.get('2',0):,}건·3순위{priority.get('3',0):,}건의 실제 범위·근거 확인 |"
 text,n=re.subn(r'^\| 기준 간 관계의 검토 상태 정리 \|.*$',lambda _:row,text,flags=re.M);assert n==1
 marker=f'{args.date} · {args.batch_label} 반영 후 전체 검사 버전'
 paragraph=f'{marker} `{version}`이 통과했다. 개별 수학 검토는 누적 {count}건, 원래 유형에서의 보정은 누적 {corrections}건이며 각 기록은 해당 대표 수행의 범위에 한정한다. 검토 대기는 {pending:,}건(1순위 {priority.get("1",0)}건)이다. 양쪽 기준 문서와 현재 포털의 이유·조건·질문·기대 설명·한계를 모두 검사했다. 원본/기준/원고/초기 상세 사례/목표/과제/자료 변경 시 재검토, 자체 검토의 자동 승격 금지, 기존 외부 이력 보존 검사도 통과했다. 문헌 주장 {claims}건·문헌 관찰 {observations}건·교육과정 발문 156건·별도 위계 검토 {hierarchy_count}건과 합산하지 않는다. 이번 자체 점검을 독립 검토·학생 검증으로 집계하지 않는다.'
 if args.batch_kind=='literature':
  paragraph=f'{marker} `{version}`이 통과했다. 명시한 읽기 범위의 출처는 {sources}개,주장 대응은 {claims}건,자체 관찰은 {observations}건이며 초기 문헌 대응 대기는 {literature_pending}개다. 각 출처의 미검토 부분·원연구·판본 대조는 별도다. 신규 관계 검토로 합산하지 않아 누적 관계 검토 {count}건·유형 보정 {corrections}건·관계 대기 {pending}건은 유지된다. 모든 문헌 대상 해시와 기존 관계 검토 근거가 현재이며,각 문헌의 지원 범위와 자체 관찰의 상세 문서·포털 반영을 검사했다. 근거 등급은 이를 명시한 IES 출처에만 적용한다. 독립 검토·학생 검증으로 승격하지 않는다.'
 pattern='^'+re.escape(marker)+r'.*$'
 if re.search(pattern,text,re.M):text=re.sub(pattern,lambda _:paragraph,text,flags=re.M)
 else:text+='\n'+paragraph+'\n'
 p.write_text(text,encoding='utf-8')
 p=ROOT/'docs/내용체계보완결과20261104.md';parts=p.read_text(encoding='utf-8').split('\n\n');assert parts[1].startswith('최신 결과')
 relation_note=f'이번 보완({args.batch_label})을 포함한 개별 관계 수학 검토는 누적 {count}건이며 유형 보정은 누적 {corrections}건이다.' if args.batch_kind=='relation' else f'이번 보완({args.batch_label})은 문헌 대응이다. 개별 관계 수학 검토 누적 {count}건·유형 보정 {corrections}건에는 추가 집계하지 않았다.'
 literature_backlog=f'초기 대응 대기 문헌 {literature_pending}개·' if literature_pending else ''
 parts[1]=f'최신 결과 ({args.date}): 보고서의 내용 오류 3건과 공식 표 추출의 열 혼합·범주명 혼입·내부 가운데 점 오분리를 수정했고, 571개 세부 항목의 의미 대응을 자체 점검했다. 초등 121개·중학교 60개·고교 254개, 합계 435개 기준의 문장·해설·고려 사항을 원문 86쪽의 이미지로 대조했다. 교육과정 대응 발문 156개, 교육과정 외 {sources}개 출처의 주장 {claims}건·관찰 {observations}건을 반영했다. {relation_note} 관계의 이유·조건·질문·기대 설명·반례를 명시한 범위로 보완했고, 이전 문구와 실제 검토 근거·대상 해시를 보존했다. 현재 개별 범위 검토 대기는 {pending:,}건, 그중 1순위는 {priority.get("1",0)}건이다. 전체 검사 버전 `{version}` 통과. 관계 근거의 후속 점검·{literature_backlog}검토 출처별 미검토 부분과 후속 대조·실제 독립/학생 검증은 남아 있으며 [전체 자료 보완 진행](전체자료보완진행.md)에 범위와 근거를 기록한다.'
 p.write_text('\n\n'.join(parts),encoding='utf-8')
 p=ROOT/'data/content_completion_result_2026-11-04.json';result=read(p.relative_to(ROOT));result.update(checks=checks,latest_update_date=args.date,latest_progress=f'{args.batch_label}: 실제 기준 문장·양쪽 대표 원고·새 진단·반례로 자체 수학 검토. 누적{count}건·유형 보정{corrections}건. 원본/기준/원고/목표/과제/자료 변경시 명시 재검토. 개별 범위 대기{pending}건·1순위{priority.get("1",0)}건. 기존435개 기준·571개 의미 대응·교육과정 발문156개·문헌{claims}건/관찰{observations}건 유지. 별도 위계 검토·독립/학생 검증으로 자동 승격하지 않음.',standard_relation_analysis_states=states,standard_relation_analysis_state_missing=0,relation_analysis_scope_review_pending=pending,relation_scope_queue_by_priority=priority,durable_relation_scoped_math_reviews=count,relation_type_corrections=corrections,separate_hierarchy_relation_review_records=hierarchy_count)
 result['latest_checks']=[f'Full run_revision_checks.py: pass ({version}); log {args.log.as_posix()}','Scoped relation tests: source/endpoint/resource change detection, type/mathematical witness requirements, non-promotion, external-history preservation, both endpoint documents and actual current portal','Current literature, hierarchy, IES rating and published-observation tests passed as part of the full run',f'All{count} scoped relation review snapshots current; source IDs and prior derived fields preserved',f'Standard relations2239: legacy{states.get("legacy_draft",0)}/self_checked{states.get("self_checked",0)}/candidate{states.get("candidate",0)}; type corrections{corrections}',f'Scope queue{pending}: '+', '.join('priority'+k+'='+str(v) for k,v in priority.items())+'; queue generation itself approves zero reviews','Own examples checked by the batch author script and explicit mathematical witnesses; finite examples are not universal proofs',f'All{claims} literature mappings/{observations} literature observations remain current', 'Hierarchy audit current:435 standards/870 goals/565 cases/626 routes/1481 directed pairs;1135 matching condition snapshots','Retention verification and final portable-source synchronization checked separately after regeneration','This batch adds no independent/student validation and performs no public deployment']
 if 'external_literature_entries_full_read_claim_mapped' in result:
  old=result.pop('external_literature_entries_full_read_claim_mapped')
  result.setdefault('report_field_corrections',[]).append(dict(date=args.date,previous_field='external_literature_entries_full_read_claim_mapped',previous_value=old,current_field='external_literature_entries_scoped_claim_mapped',reason='명시한 범위의 주장 대응 수를 전권 정독 수로 오해하지 않도록 집계 필드명을 고쳤다. 이전 읽기 범위·판정은 확대하지 않는다.'))
 result.update(external_literature_entries_pending=literature_pending,external_literature_entries_scoped_claim_mapped=sources,literature_claim_mappings=claims,literature_observation_extensions=observations,literature_count_scope=f'{sources}개 출처의 명시한 범위와 주장 대응이다. 파일 전체의 보관은 전권 정독을 뜻하지 않는다. 실제 텍스트·이미지·HTML 읽기 범위와 미검토 부분·원연구·판본·번역 대조는 각 source.read_scope·next_review와 구조화 원장에 유지한다. 자체 학생 검증·수업 효과와 구별한다.')
 if args.batch_kind=='literature':result['latest_progress']=f'{args.batch_label}의 명시한 원문·지원 범위·적용 한계를 주장과 대응했다. 누적 출처 {sources}개·주장 {claims}건·자체 관찰 {observations}건·초기 문헌 대응 대기 {literature_pending}개다. 관계 검토 {count}건·유형 보정 {corrections}건·관계 대기 {pending}건은 유지하며 신규 관계 검토·독립 검토·학생 검증으로 합산하지 않는다.'
 p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(version=version,scoped_math_reviews=count,type_corrections=corrections,scope_pending=pending,priority1_pending=priority.get('1',0)),ensure_ascii=False))
if __name__=='__main__':main()

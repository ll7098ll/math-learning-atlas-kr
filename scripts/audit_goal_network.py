"""Read-only reconciliation of goal dependencies and existing direction records."""
from pathlib import Path
from collections import Counter
from datetime import date
import hashlib,json
from goal_hierarchy import load_goal_hierarchies
from goal_network import build_goal_network

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
def read(path):return json.loads(path.read_text(encoding='utf-8'))
standards=read(ROOT/'data/standards.json')['standards'];by_code={s['code']:s for s in standards}
entries,cases,goals=load_goal_hierarchies(standards)
catalog=read(SITE/'dist/content/catalog.json');index=read(SITE/'dist/content/task-pathways-index.json')
digest=index['goalGraph']['hash'];path=SITE/'dist/content/task-pathways/items'/(digest+'.json')
assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
graph=read(path)
assert graph==build_goal_network(entries,cases,goals,catalog['version'])
adjacent={g:set() for g in goals};incoming={g:set() for g in goals}
standard_pairs={};transitions=Counter();kinds=Counter();entry_capabilities=[];cross_course=[]
for route in graph['routes']:
    for c in route['conditions']:
        kinds[c['kind']]+=1
        if c['kind']=='entry_capability':entry_capabilities.append(dict(case_id=route['case_id'],condition=c['text'],rationale=c['rationale'],targets=c.get('applies_to_goal_ids',route['goal_ids'])))
        if c['kind']!='goal':continue
        source=c['goal_id'];a=goals[source]['code'];b=route['standard']
        for target in c.get('applies_to_goal_ids',route['goal_ids']):
            adjacent[source].add(target);incoming[target].add(source)
            transitions[by_code[a]['school_level']+'→'+by_code[b]['school_level']]+=1
            if a!=b:standard_pairs.setdefault((a,b),[]).append(dict(source_goal=source,target_goal=target,case_id=route['case_id'],route_id=route['route_id'],rationale=c['rationale']))
            if by_code[a]['school_level']==by_code[b]['school_level']=='고등학교' and by_code[a]['subject']!=by_code[b]['subject']:
                cross_course.append(dict(source_goal=source,target_goal=target,case_id=route['case_id'],source_subject=by_code[a]['subject'],target_subject=by_code[b]['subject'],rationale=c['rationale']))
active=set();done=set()
def visit(node):
    assert node not in active,'Scoped goal dependency cycle: '+node
    if node in done:return
    active.add(node)
    for target in adjacent[node]:visit(target)
    active.remove(node);done.add(node)
for goal in goals:visit(goal)
relations=read(ROOT/'data/revised_relations.json')['relations'];directions={}
for r in relations:
    if r['type'] not in ('generalizes','requires_for_task') or r.get('review_state')=='candidate':continue
    if not r['from'].startswith('standard:') or not r['to'].startswith('standard:'):continue
    directions.setdefault((r['from'][9:],r['to'][9:]),[]).append(r['id'])
opposed=[dict(source_standard=a,target_standard=b,existing_reverse_ids=directions[b,a],goal_evidence=evidence) for (a,b),evidence in standard_pairs.items() if (b,a) in directions]
levels=['초등학교','중학교','고등학교']
higher=[dict(source_standard=a,target_standard=b,evidence=evidence) for (a,b),evidence in standard_pairs.items() if levels.index(by_code[a]['school_level'])>levels.index(by_code[b]['school_level'])]
sources=[ROOT/'data/standards.json',ROOT/'data/revised_relations.json',*(ROOT/'data').glob('goal_hierarchy_*.json')]
result=dict(date=date.today().isoformat(),kind='structural_and_direction_reconciliation',
    interpretation='원장·생성 자료와 목표별 연결의 범위·방향을 대조한다. 역방향 충돌이 없다는 사실만으로 모든 연결의 수학적 타당성·필수 선수성·수업 효과가 증명되는 것은 아니다.',
    catalog_version=catalog['version'],task_dataset_version=index['datasetVersion'],graph_hash=digest,
    source_hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    coverage={**graph['coverage'], 'cross_standard_pairs':len(standard_pairs),'condition_clauses':sum(kinds.values()),'condition_kinds':dict(kinds),'scoped_link_occurrences':sum(transitions.values())},
    checks=dict(export_matches_authored_goals_and_all_route_conditions=True,goal_conditions_acyclic=True),
    school_transition_occurrences=dict(transitions),opposing_existing_direction_candidates=opposed,higher_school_source_candidates=higher,
    cross_course_condition_applications=cross_course,entry_capability_conditions=entry_capabilities,
    goals_without_linked_predecessor=[g for g in goals if not incoming[g]],goals_without_outgoing_reference=[g for g in goals if not adjacent[g]],
    absence_interpretation='직접 참조가 없는 목표도 과제 안 구성·가정·출발 능력과 대표 수행을 갖는다. 후속 참조 미기록은 활용되지 않음을 뜻하지 않는다.')
(ROOT/'data/goal_network_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status='pass',**graph['coverage'],cross_standard_pairs=len(standard_pairs),opposing_existing_direction_candidates=len(opposed),higher_school_source_candidates=len(higher),entry_capability_conditions=len(entry_capabilities),cross_course_condition_applications=len(cross_course))))

"""Export every authored goal and route; formal AND/OR requires explicit cases."""
import hashlib
import json
import re
import shutil
from urllib.parse import urlparse
from pathlib import Path
from detailed_revision import load_revisions
from goal_hierarchy import load_goal_hierarchies, write_goal_report
from content_objects import write_content_object
from goal_network import build_goal_network

ROOT=Path(__file__).resolve().parents[1]


def build(site):
    content=site/'dist/content'
    example_dir=site/'dist/examples'
    example_dir.mkdir(parents=True,exist_ok=True)
    for example in (ROOT/'data/teaching_examples').glob('*.csv'):
        shutil.copyfile(example,example_dir/example.name)
    shutil.copyfile(ROOT/'scripts/statistical_tools.py',example_dir/'stats-inference.py')
    shutil.copyfile(ROOT/'scripts/economy_ai_models.py',example_dir/'economy-ai-models.py')
    catalog=json.loads((content/'catalog.json').read_text(encoding='utf-8'))
    revisions=load_revisions()
    cases=json.loads((ROOT/'data/task_route_cases.json').read_text(encoding='utf-8'))['cases']
    goal_entries, goal_cases, goals=load_goal_hierarchies(catalog['standards'])
    write_goal_report(goal_entries,goal_cases,goals)
    cases += goal_cases
    pilots=json.loads((ROOT/'data/hierarchy_pilot.json').read_text(encoding='utf-8'))['maps']
    codes={s['code'] for s in catalog['standards']}
    taxonomy=json.loads((ROOT/'data/concept_taxonomy.json').read_text(encoding='utf-8'))['groups']
    assert set(revisions)==codes
    assert len({c['id'] for c in cases})==len(cases)
    by_case={c['id']:c for c in cases}
    for case in cases:
        for replacement in case.get('superseded_by_case_ids',[]):
            assert replacement!=case['id'] and replacement in by_case
            assert by_case[replacement]['standard']==case['standard']
            assert by_case[replacement].get('goal_ids') and not by_case[replacement].get('superseded_by_case_ids')
        assert case['standard'] in codes and case['goal'] and case['task'] and case['shared_conditions']
        assert case['route_relationship']=='alternative_explanations'
        assert case['routes'] and len({r['id'] for r in case['routes']})==len(case['routes'])
        for resource in case.get('resources',[]):
            assert resource['label'] and (re.fullmatch(r'examples/[a-z0-9-]+\.csv',resource['path']) or resource['path'] in ('examples/stats-inference.py','examples/economy-ai-models.py'))
            assert (site/'dist'/resource['path']).is_file(),resource
        for reference in case.get('references',[]):
            parsed=urlparse(reference['url'])
            assert reference['title'] and reference['accessed'] and parsed.scheme=='https' and parsed.hostname
            assert not parsed.username and not parsed.password
        for route in case['routes']:
            assert route['operator']=='AND' and route['conditions'] and route['steps']
            assert route['result'] and all(route['diagnostic'].get(k) for k in ('question','expected'))
    datasets={}
    for s in catalog['standards']:
        code=s['code'];rev=revisions[code]
        refs=[{'id':m['id'],'title':m['title'],'route_relationship':'different_goals' if m['id']=='ratio' else 'alternative_explanations'} for m in pilots if code in m['standards'] or any(code in n['standards'] for n in m['nodes'])]
        datasets[code]={
            'version':catalog['version'],'code':code,'official_goal':s['statement'],'title':s['title'],
            'concept_id':next(g['id'] for g in taxonomy if code in g['primary_codes']),
            'source_file':'data/'+rev['_source_file'],'goal_branches':rev.get('goalBranches',[]),
            'task_solution':rev.get('taskSolution',''),'thinking':rev.get('thinking',[]),
            'recorded_conditions':rev.get('conditions',[]),'source_routes':rev.get('paths',[]),
            'diagnostics':rev.get('diagnostics',[]),'cases':[c for c in cases if c['standard']==code],
            'pilots':refs,
            'goal_analysis':goal_entries.get(code),
            'goal_references':{source['goal_id']:goals[source['goal_id']] for c in cases if c['standard']==code for r in c['routes'] for source in r.get('condition_sources',[]) if source['kind']=='goal'},
            'scope_note':'기록된 사고 요소의 나열은 학습 선후나 AND 조건이 아니다. 경로별 조건 묶음은 명시적으로 작성한 과제 또는 기존 시범에서만 판정한다.',
        }
    goal_graph=build_goal_network(goal_entries,goal_cases,goals,catalog['version'])
    version=hashlib.sha256(json.dumps(dict(records=datasets,goal_graph=goal_graph),ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:16]
    def write(path,data):
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    files={code:write_content_object(content,'task-pathways',data) for code,data in datasets.items()}
    graph_hash=write_content_object(content,'task-pathways',goal_graph)
    summary={'standards':len(codes),'explicit_cases':len(cases),
             'active_cases':sum(not c.get('superseded_by_case_ids') for c in cases),
             'preserved_previous_cases':sum(bool(c.get('superseded_by_case_ids')) for c in cases),
             'goal_decomposed_standards':len(goal_entries),'constituent_goals':len(goals),
             'explicit_case_standards':sum(bool(d['cases']) for d in datasets.values()),
             'pilot_referenced_standards':sum(bool(d['pilots']) for d in datasets.values()),
             'source_only_standards':sum(not d['cases'] and not d['pilots'] for d in datasets.values()),
             'entries':[{'code':code,'cases':len(d['cases']),'pilots':len(d['pilots']),'goal_branches':len(d['goal_branches']),'constituent_goals':len(d['goal_analysis']['goals']) if d['goal_analysis'] else 0,'goal_decomposition_review':'self_checked' if d['goal_analysis'] else 'not_formalized','route_condition_review': 'explicit_task_cases' if d['cases'] else 'pilot_scope_only' if d['pilots'] else 'not_formalized'} for code,d in datasets.items()]}
    write(content/'task-pathways-index.json',{'version':catalog['version'],'datasetVersion':version,'files':files,'goalGraph':{'hash':graph_hash,**goal_graph['coverage']},'codes':list(datasets),'coverage':{k:v for k,v in summary.items() if k!='entries'}})
    (ROOT/'data/task_pathway_coverage.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {k:v for k,v in summary.items() if k!='entries'}

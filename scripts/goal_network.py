"""Export scoped goal dependencies without promoting them to course prerequisites."""
def build_goal_network(entries,cases,goals,version):
    routes=[];active_cases=[]
    for case in cases:
        if case.get('superseded_by_case_ids'):continue
        active_cases.append(case)
        for route in case['routes']:
            sources={s['condition_index']:s for s in route['condition_sources']}
            routes.append(dict(id=case['id']+'::'+route['id'],case_id=case['id'],standard=case['standard'],
                case_title=case['title'],case_goal=case['goal'],goal_ids=case['goal_ids'],route_id=route['id'],
                title=route['title'],operator=route['operator'],shared_conditions=case['shared_conditions'],
                conditions=[dict(text=text,**sources[i]) for i,text in enumerate(route['conditions'])],
                alternative_review=case['alternative_review']))
    links={(c['goal_id'],target) for route in routes for c in route['conditions'] if c['kind']=='goal' for target in c.get('applies_to_goal_ids',route['goal_ids'])}
    assert all(a in goals and b in goals and a!=b for a,b in links)
    return dict(version=version,kind='scoped_goal_network',
        interpretation='각 과제·경로에 적용되는 부분 수행의 연결이다. 한 경로의 전체 AND 조건과 다른 경로·목표의 구별을 보존하며 과목 전체의 필수 이수나 유일한 학습 순서로 해석하지 않는다.',
        goals=list(goals.values()),routes=routes,
        coverage=dict(standards=len(entries),goals=len(goals),cases=len(active_cases),routes=len(routes),directed_pairs=len(links)))

"""Independent witnesses for geometry, units and data; source-scope regressions."""
from collections import Counter
from fractions import Fraction as F
import json
from math import atan2,pi
from pathlib import Path
from goal_hierarchy import load_goal_hierarchies

ROOT=Path(__file__).resolve().parents[1]
standards=json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s['code'].startswith(('4수03-','4수04-'))}
selected={code:e for code,e in entries.items() if code in codes}
selected_cases=[case for case in cases if case['standard'] in codes]
by_case={case['id']:case for case in selected_cases}
assert len(selected)==28 and sum(len(e['goals']) for e in selected.values())==69 and len(selected_cases)==32

# Coordinates verify mathematical witnesses, not prerequisites imposed on learners.
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
assert dot((1,1),(-1,1))==0 and cross((1,2),(2,4))==0
assert (0+3,0+2)==(3,2) and (3-3,2-2)==(0,0)
assert len(range(4))==4 and len(range(3))==3  # Four positions span three intervals.
assert all(x*x+y*y==9 for x,y in [(3,0),(0,3),(-3,0),(0,-3)])
assert (3-(-3))==6 and 3*2==6
assert ((3+0)/2,(0+3)/2)!=(0,0)  # A chord need not pass through the centre.
assert 2*2<3*3  # Compass radius witnesses.
assert 3+3>4 and F(3*3+4*4-3*3,2*3*4)==F(2,3)
assert F(3*3+3*3-3*3,2*3*3)==F(1,2)
assert [90,50,40][0]==90 and all(x<90 for x in [70,60,50]) and max([110,40,30])>90

shapes={
 'rectangle':[(0,0),(4,0),(4,2),(0,2)],
 'square':[(0,0),(2,0),(2,2),(0,2)],
 'trapezoid':[(0,0),(6,0),(4,2),(1,2)],
 'parallelogram':[(0,0),(4,0),(5,2),(1,2)],
 'rhombus':[(0,0),(2,1),(4,0),(2,-1)],
}
def properties(poly):
    edges=[(poly[(i+1)%4][0]-poly[i][0],poly[(i+1)%4][1]-poly[i][1]) for i in range(4)]
    return dict(lengths=[dot(e,e) for e in edges],parallel=sum(cross(edges[i],edges[i+2])==0 for i in (0,1)),right=sum(dot(edges[i-1],edges[i])==0 for i in range(4)))
p={name:properties(poly) for name,poly in shapes.items()}
assert p['rectangle']['right']==4 and p['square']['right']==4
assert len(set(p['square']['lengths']))==1
assert p['trapezoid']['parallel']==1 and p['parallelogram']['parallel']==2
assert len(set(p['rhombus']['lengths']))==1 and p['rhombus']['right']==0
assert len({(x,y) for x in range(3) for y in range(2)})==6

assert 60==1*60 and 3*3600+7*60+12==11232
assert 165+90==255==4*60+15
assert 310-155==155==2*60+35
unit_witnesses=0
for factor in (10,1000,60):
    for amount in range(4000):
        whole,part=divmod(amount,factor)
        assert factor*whole+part==amount and 0<=part<factor
        unit_witnesses+=1
assert 10+7==17 and divmod(205,10)==(20,5)
assert 2000+35==2035 and divmod(2050,1000)==(2,50)
assert 2000+350==2350 and 3000+75==3075
assert 1000==1*1000 and 2000==2*1000
assert 1750+650==2400 and 3100-1750==1350
assert 2350+1780==4130 and 650+350==1000
assert 75+105==180 and 75<90<105
assert sum([60,60,60])==sum([90,50,40])==180
assert sum([90]*4)==sum([60,120,60,120])==2*180==360
assert 4*180-360==360  # Two diagonals introduce a full turn of extra central angles.
for poly in shapes.values():
    total=0
    for i in range(4):
        a=(poly[i-1][0]-poly[i][0],poly[i-1][1]-poly[i][1])
        b=(poly[(i+1)%4][0]-poly[i][0],poly[(i+1)%4][1]-poly[i][1])
        total+=atan2(abs(cross(a,b)),dot(a,b))
    assert abs(total-2*pi)<1e-10

responses=['apple']*6+['pear']*4+['mandarin']*8
counts=Counter(responses)
assert len(responses)==18 and counts=={'apple':6,'pear':4,'mandarin':8}
pictures={key:value//2 for key,value in counts.items()}
assert pictures=={'apple':3,'pear':2,'mandarin':4}
assert {key:value*2 for key,value in pictures.items()}==counts
assert counts['mandarin']-counts['apple']==2
heights=[4,6,5,9];changes=[b-a for a,b in zip(heights,heights[1:])]
assert changes==[2,-1,4] and changes.index(max(changes))==2 and heights[-1]-heights[0]==5

# Scope of conditions includes siblings only when the actual target differs.
graph={goal:set() for goal in goals};refs=sibling_refs=0
for case in cases:
    for route in case['routes']:
        for source in route['condition_sources']:
            if source['kind']=='goal':
                targets=source.get('applies_to_goal_ids',case['goal_ids'])
                assert source['goal_id'] not in targets
                for target in targets:graph[source['goal_id']].add(target)
                if case['standard'] in codes:
                    refs+=1
                    sibling_refs+=source['goal_id'] in case['goal_ids']
active=set();done=set()
def visit(node):
    assert node not in active,'Review a conditional reference cycle: '+node
    if node in done:return
    active.add(node)
    for following in graph[node]:visit(following)
    active.remove(node);done.add(node)
for goal in graph:visit(goal)
assert '4수03-06:diameter' in graph['4수03-06:radius']
assert '4수03-06:radius' not in graph['4수03-06:radius']
assert '4수03-11:regular' in graph['4수03-11:polygon']
assert '4수03-15:estimate' not in graph['2수03-10:measure']
quad_goals=set(g['id'] for g in selected['4수03-10']['goals'])
assert all(not (graph[g]&quad_goals) for g in quad_goals),'Do not introduce quadrilateral inclusion goals'
assert '4수04-03:plan' not in graph['4수04-02:interpret']
revisions=json.loads((ROOT/'data/revisions_elementary.json').read_text(encoding='utf-8'))
assert revisions['4수03-05']['scopeCorrections'][-1]['previous_paths']
assert all('투명 종이' not in text and '회전' not in text and '도형' not in text for text in revisions['4수03-05']['paths'])
assert '꼭짓점 이동으로 도형 변환' in revisions['4수03-05']['conditions'][0]
assert '포함 관계' in selected['4수03-10']['scope']
assert '한 점' in selected['4수03-05']['scope']
assert '1km와1cm' in by_case['early-4수03-16-km-m']['notes']
assert '−1' not in ''.join(by_case['early-4수04-03-time-inquiry']['routes'][0]['steps'])
assert len(by_case['early-4수03-25-triangle-sum']['routes'])==2
assert len(by_case['early-4수03-25-quadrilateral-sum']['routes'])==2
assert all(e['history'] for e in selected.values())
print(json.dumps(dict(status='pass',standards=28,goals=69,cases=32,scoped_goal_references=refs,sibling_condition_references=sibling_refs,unit_witnesses=unit_witnesses,checks='geometric witnesses; units and operations; graph legends and time changes; source-scope correction; exact sibling targets; conditional references')))

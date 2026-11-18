"""Independent geometric and numeric witnesses; no learner coordinate prerequisites."""
from fractions import Fraction as F
from collections import deque,Counter
from itertools import product
from math import sqrt,cos,sin,pi,isclose
from pathlib import Path
import json
from goal_hierarchy import load_goal_hierarchies

ROOT=Path(__file__).resolve().parents[1]
standards=json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s['code'].startswith(('6수03-','6수04-'))}
selected={code:e for code,e in entries.items() if code in codes}
selected_cases=[case for case in cases if case['standard'] in codes]
by_case={case['id']:case for case in selected_cases}
assert len(selected)==25 and sum(len(e['goals']) for e in selected.values())==57 and len(selected_cases)==33
assert len({code for code in entries if code.startswith(('2수','4수','6수'))})==121

neg=lambda v:tuple(-x for x in v)
def folds_to_cube(cells):
    if len(cells)!=6:return False
    states={next(iter(cells)):((1,0,0),(0,1,0),(0,0,1))}
    queue=deque(states)
    while queue:
        x,y=queue.popleft();right,up,normal=states[(x,y)]
        transitions=[((1,0),(neg(normal),up,right)),((-1,0),(normal,up,neg(right))),
                     ((0,1),(right,neg(normal),up)),((0,-1),(right,normal,neg(up)))]
        for (dx,dy),state in transitions:
            neighbor=(x+dx,y+dy)
            if neighbor not in cells:continue
            if neighbor in states:
                if states[neighbor]!=state:return False
            else:states[neighbor]=state;queue.append(neighbor)
    return len(states)==6 and len({state[2] for state in states.values()})==6
cube_net={(0,0),(1,0),(2,0),(3,0),(1,1),(1,-1)}
box_net={(0,0),(1,0),(2,0),(3,0),(0,1),(0,-1)}
invalid_net={(x,y) for x in range(3) for y in range(2)}
assert folds_to_cube(cube_net) and folds_to_cube(box_net) and not folds_to_cube(invalid_net)
assert [w*4 for w in [2,3,2,3]]==[8,12,8,12]
assert sum(w*4 for w in [2,3,2,3])+2*(2*3)==52
assert 3*5+4*5+5*5+2*(3*4/2)==72  # Five prism faces, not a learner formula prerequisite.

def mesh_counts(faces):
    edges=Counter(tuple(sorted((face[i],face[(i+1)%len(face)]))) for face in faces for i in range(len(face)))
    assert all(times==2 for times in edges.values())
    return len(faces),len(edges),len({v for face in faces for v in face})
assert mesh_counts([(0,1,2,3),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])==(6,12,8)
assert mesh_counts([(0,1,2),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)])==(5,9,6)
assert mesh_counts([(0,1,2,3),(0,1,4),(1,2,4),(2,3,4),(3,0,4)])==(5,8,5)
for x,y in [(2,1),(1,3)]:
    reflected=(-x,y);central=(-x,-y)
    assert reflected==({(2,1):(-2,1),(1,3):(-1,3)}[(x,y)])
    assert (x+central[0],y+central[1])==(0,0)
    assert (reflected[0]-x,reflected[1]-y)==(-2*x,0)
for t in [0,pi/7,pi/2,pi]:
    for z in [0,1,2,3]:
        cylinder=(2*cos(t),2*sin(t),z)
        assert isclose(cylinder[0]**2+cylinder[1]**2,4)
        cone_r=2*(1-z/3)
        cone=(cone_r*cos(t),cone_r*sin(t),z)
        assert isclose(cone[0]**2+cone[1]**2,cone_r**2,abs_tol=1e-12)
        sphere_r=sqrt(9-z*z)
        sphere=(sphere_r*cos(t),sphere_r*sin(t),z)
        assert isclose(sum(v*v for v in sphere),9)

heights=((2,1),(1,2))
def silhouettes(h):
    return (tuple(tuple(v>0 for v in row) for row in h),tuple(max(row[j] for row in h) for j in range(2)),tuple(max(row) for row in h))
assert sum(map(sum,heights))==sum(sum(v>=level for row in heights for v in row) for level in [1,2])==6
assert silhouettes(heights)==silhouettes(((2,2),(2,2)))
compatible=[values for values in product([1,2],repeat=4) if silhouettes((values[:2],values[2:]))==silhouettes(heights)]
assert len(compatible)==7 and Counter(sum(values) for values in compatible)=={6:2,7:4,8:1}
visual=by_case['early-6수03-10-ambiguous']['visual']
assert visual['kind']=='block_heights' and len(visual['models'])==2 and len(visual['views'])==3
for model in visual['models']:
    h=model['heights']
    assert len(h)==2 and all(len(row)==2 and all(type(v) is int and 1<=v<=2 for v in row) for row in h)
    assert str(sum(map(sum,h))) in model['label']
    top,front,right=silhouettes(h)
    expected=[[[int(v) for v in row] for row in reversed(top)],
              [[int(front[x]>=level) for x in range(2)] for level in [2,1]],
              [[int(right[y]>=level) for y in range(2)] for level in [2,1]]]
    assert [view['cells'] for view in visual['views']]==expected

def area(poly):
    return abs(sum(F(x)*poly[(i+1)%len(poly)][1]-F(y)*poly[(i+1)%len(poly)][0] for i,(x,y) in enumerate(poly)))/2
assert 6+4+6+4==20 and 4*3==12
assert 100**2==10000 and 1000**2==1000000
assert 6*4==2*4+4*4==24 and 3*3==1*3+2*3==9
parallelogram=[(0,0),(6,0),(8,4),(2,4)]
triangle=[(0,0),(6,0),(8,4)]
trapezoid=[(0,0),(8,0),(6,3),(2,3)]
rhombus=[(-3,0),(0,-4),(3,0),(0,4)]
assert area(parallelogram)==6*4==8*4-2*4==24
assert area(triangle)==6*4/2==8*4/2-2*4/2==12
assert (0-6)*(8-6)+(0-0)*(4-0)<0  # Authored triangle is obtuse; foot x=8 is outside [0,6].
assert area(trapezoid)==F((8+4)*3,2)==4*3+2*F(2*3,2)==18
assert area(rhombus)==F(6*8,2)==6*4==6*8-4*F(3*4,2)==24
area_witnesses=0
for base in range(1,21):
    for height in range(1,16):
        for shift in [-3,-1,0,1,3,base+2]:
            p=[(0,0),(base,0),(base+shift,height),(shift,height)]
            t=[(0,0),(base,0),(base+shift,height)]
            assert area(p)==base*height and area(t)==F(base*height,2)
            area_witnesses+=1
assert F('15.7')/5==F('3.14') and F('31.5')/10==F('3.15') and F('62.8')/20==F('3.14')
assert 8*F('3.14')==F('25.12')
assert 6*F('3.14')==F('18.84') and 9*F('3.14')==F('28.26')
assert F('18.84')/2*3==F('28.26')
assert sum([12,12,8,8,6,6])==2*(12+8+6)==52 and 6*3*3==54
assert 100**3==1000000 and (3*4)*2==(3*2)*4==24 and 3**3==27
volume_witnesses=0
for x in range(1,21):
    for y in range(1,16):
        for z in range(1,11):
            assert (x*y)*z==(x*z)*y
            assert 2*(x*y+y*z+z*x)==sum([x*y,x*y,y*z,y*z,z*x,z*x])
            volume_witnesses+=1

first=[2,4,9];second=[4,5,6]
assert sum(first)==sum(second)==15 and F(sum(first),len(first))==F(sum(second),len(second))==5
assert first[0]+3==first[1]+1==first[2]-4==5 and 5 not in first
mean_witnesses=0
for values in product(range(6),repeat=3):
    avg=F(sum(values),len(values))
    assert sum(F(v)-avg for v in values)==0
    mean_witnesses+=1
counts=[8,6,4,2];rates=[40,30,20,10]
assert sum(counts)==20 and [F(v,20)*100 for v in counts]==rates and sum(rates)==100
assert [sum(rates[:i]) for i in range(5)]==[0,40,70,90,100]
assert F(14,20)==F(70,100) and [F(v,100)*360 for v in rates]==[144,108,72,36]
assert [6-4,5-6,9-5]==[2,-1,4] and 9-4==5
assert F(1,2)==F(1,1+1) and F(9,10)>F(1,2)
assert 14>6 and sum([4,6,5])==15

graph={goal:set() for goal in goals};refs=siblings=0
for case in cases:
    for route in case['routes']:
        for source in route['condition_sources']:
            if case['standard'] in codes:
                assert source['applies_to_goal_ids'] and set(source['applies_to_goal_ids'])<=set(case['goal_ids'])
            if source['kind']=='goal':
                for target in source.get('applies_to_goal_ids',case['goal_ids']):graph[source['goal_id']].add(target)
                if case['standard'] in codes:
                    refs+=1;siblings+=source['goal_id'].split(':')[0]==case['standard']
active=set();done=set()
def visit(node):
    assert node not in active,'Review conditional reference cycle: '+node
    if node in done:return
    active.add(node)
    for following in graph[node]:visit(following)
    active.remove(node);done.add(node)
for goal in graph:visit(goal)
assert '6수03-12:relations' not in graph['6수03-13:rectangle']
assert '6수03-18:relation' not in graph['6수03-19:cuboid']
assert all(s.get('goal_id')!='6수03-14:triangle' for r in by_case['early-6수03-14-parallelogram']['routes'] for s in r['condition_sources'])
assert all(s.get('goal_id')!='6수03-13:rectangle' for r in by_case['early-6수03-11-perimeter']['routes'] for s in r['condition_sources'])
assert all(s.get('goal_id')!='4수03-24:measure' for r in by_case['early-6수04-02-shares']['routes'] for s in r['condition_sources'])
assert all(s.get('goal_id')!='6수03-16:circumference' for r in by_case['early-6수03-08-cylinder-net']['routes'] for s in r['condition_sources'])
assert all('6수04-03:plan' not in graph[g] for g in ['6수04-02:represent','4수04-02:represent'])
assert all(e['source_review']['pdf_pages']==([37,38] if code.startswith('6수04-') else [34,35,36]) for code,e in selected.items())
assert all(e['history'] for e in selected.values())
legacy=json.loads((ROOT/'data/revisions_elementary.json').read_text(encoding='utf-8'))
assert legacy['6수03-11']['scopeCorrections'][-1]['previous_paths'][0].startswith('단위 정사각형')
assert '둘레' in legacy['6수03-11']['paths'][0] and '비례배분' not in ''.join(legacy['6수03-15']['paths'])
assert legacy['6수03-15']['scopeCorrections'][-1]['previous_paths']!=legacy['6수03-15']['paths']
def result(case_id,fragment):
    assert all(fragment in r['result'].replace(' ','') for r in by_case['early-'+case_id]['routes'])
for case_id,fragment in [('6수03-09-blocks','6개'),('6수03-14-parallelogram','24cm²'),('6수03-14-triangle','12cm²'),('6수03-14-trapezoid','18cm²'),('6수03-14-rhombus','24cm²'),('6수03-17-surface','52cm²'),('6수03-19-volume','24cm³'),('6수04-01-mean','5개'),('6수04-02-shares','70%')]:result(case_id,fragment)
print(json.dumps(dict(status='pass',standards=25,goals=57,cases=33,elementary_goal_standards=121,scoped_goal_references=refs,sibling_condition_references=siblings,compatible_block_models=len(compatible),area_witnesses=area_witnesses,volume_witnesses=volume_witnesses,mean_witnesses=mean_witnesses,checks='folded net consistency; solid topology; symmetry and rotation; projection ambiguity; polygon area and external height; surface versus volume; mean and graph proportions; qualitative chance; curriculum scope and references')))

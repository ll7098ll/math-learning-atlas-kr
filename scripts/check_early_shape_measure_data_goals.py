"""Independent witnesses and boundary checks for early patterns, shapes and data."""
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
from goal_hierarchy import load_goal_hierarchies

ROOT=Path(__file__).resolve().parents[1]
standards=json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s['code'].startswith('2수') and not s['code'].startswith('2수01-')}
selected_entries={code:e for code,e in entries.items() if code in codes}
selected_cases=[case for case in cases if case['standard'] in codes]
by_case={case['id']:case for case in selected_cases}
assert len(selected_entries)==18 and sum(len(e['goals']) for e in selected_entries.values())==39
assert len(selected_cases)==24

assert 'ABB'*2=='ABBABB' and ('ABB'*3)[6:]=='ABB'
assert 'ABBABB'+'A' != 'ABBABB'+'B'  # Same observed prefix admits different continuations without a chosen rule.
assert list(range(2,13,2))==[2,4,6,8,10,12]
own='AB'*4
assert own=='ABABABAB' and own[:6]+'B'+own[7:]!=own

# Coordinate witnesses check the written invariant; coordinates are not a learner prerequisite.
tri=[(0,0),(3,0),(1,2)]
quad=[(0,0),(3,0),(3,1),(0,1)]
for polygon,n in [(tri,3),(quad,4)]:
    rotated=[(-y,x) for x,y in polygon]
    assert len(set(polygon))==len(set(rotated))==n
    assert sum((polygon[(i+1)%n][0]-polygon[i][0])**2+(polygon[(i+1)%n][1]-polygon[i][1])**2 for i in range(n))==sum((rotated[(i+1)%n][0]-rotated[i][0])**2+(rotated[(i+1)%n][1]-rotated[i][1])**2 for i in range(n))
blocks={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
assert len(blocks)==4 and Counter(z for _,_,z in blocks)=={0:3,1:1}
assert all(z==0 or (x,y,z-1) in blocks for x,y,z in blocks)
for unit in [Fraction(1,3),1,3]:assert 2*unit<3*unit
assert 2*2>3*1  # Counts alone fail when the cups differ.
assert 3>2 and 3*1>2*1  # Equal-arm balance witness.
assert 3*2>2*1
assert 2*(10+1)>2*(4+4) and 10*1<4*4  # Perimeter is not area.

# All 720 displayed minutes: hour hand moves continuously; minute hand does not set the hour.
clock_states=0
for hour in range(12):
    for minute in range(60):
        hand=30*hour+Fraction(minute,2)
        assert hand//30==hour
        assert 6*minute<360
        clock_states+=1
assert (3*60+55)+5==4*60 and (3*60+50)+10==4*60
assert 60+20==80 and 11*60+20-10*60==80
assert 7*4==28 and 31!=28 and 12==len(range(1,13))
assert 29!=28 and 366!=365

assert 4*5==5*4==20  # Different handspans, same length.
assert 11-3==8 and len(range(3,12))==9
for length in range(400):
    metres,cm=divmod(length,100)
    assert 100*metres+cm==length and 0<=cm<100
assert 2*100+35==235 and 205==2*100+5 and 205!=2*100+50
assert 35+28==63 and 63-28==35
assert 120+30==150 and 120-30==90 and 120-30!=110

cards=[('red','triangle'),('red','circle'),('red','quadrilateral'),('blue','circle'),('blue','quadrilateral'),('yellow','triangle'),('yellow','circle'),('yellow','quadrilateral')]
colors=Counter(color for color,_ in cards);shapes=Counter(shape for _,shape in cards)
assert colors=={'red':3,'blue':2,'yellow':3}
assert shapes=={'triangle':2,'circle':3,'quadrilateral':3}
assert sum(colors.values())==sum(shapes.values())==8
marks={color:'○'*count for color,count in colors.items()}
assert {color:len(line) for color,line in marks.items()}==colors
assert set(colors)==set(marks) and colors['red']==colors['yellow']>colors['blue']

# Dependencies belong to a named route and specific constituent goals.
graph={goal:set() for goal in goals};refs=0
for case in cases:
    for route in case['routes']:
        for source in route['condition_sources']:
            if case['standard'] in codes:
                assert source['applies_to_goal_ids'] and set(source['applies_to_goal_ids'])<=set(case['goal_ids'])
            if source['kind']=='goal':
                for target in source.get('applies_to_goal_ids',case['goal_ids']):graph[source['goal_id']].add(target)
                if case['standard'] in codes:refs+=1
active=set();done=set()
def visit(node):
    assert node not in active,'Circular task-scoped reference: '+node
    if node in done:return
    active.add(node)
    for following in graph[node]:visit(following)
    active.remove(node);done.add(node)
for goal in graph:visit(goal)
estimate=by_case['early-2수03-12-estimate']
measure=next(s for s in estimate['routes'][0]['condition_sources'] if s.get('goal_id')=='2수03-10:measure')
assert measure['applies_to_goal_ids']==['2수03-12:calibrate']
assert '2수03-12:estimate' not in graph['2수03-10:measure']
direct=by_case['early-2수04-03-graph']['routes'][0]
assert all(s.get('goal_id')!='2수04-02:table' for s in direct['condition_sources'])
assert '항상28일' in by_case['early-2수03-09-calendar']['routes'][0]['result']
assert '8cm' in by_case['early-2수03-10-ruler']['routes'][0]['result']
assert '235cm' in by_case['early-2수03-11-convert']['routes'][0]['result']
assert all(e['history'] for e in selected_entries.values())
print(json.dumps(dict(status='pass',standards=len(codes),goals=39,cases=len(selected_cases),scoped_goal_references=refs,clock_states=clock_states,unit_conversion_witnesses=400,checks='pattern scope; geometric invariants; comparison conditions; time and calendar boundaries; units; source-data/table/graph counts; goal-specific condition application; acyclic references')))

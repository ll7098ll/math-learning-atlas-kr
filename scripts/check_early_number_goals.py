"""Independent finite-domain arithmetic and scope checks for authored early goals."""
import json
from pathlib import Path
from goal_hierarchy import load_goal_hierarchies

ROOT=Path(__file__).resolve().parents[1]
standards=json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
entries={code:e for code,e in entries.items() if code.startswith('2수01-')}
cases=[case for case in cases if case['standard'] in entries]
goals={key:g for key,g in goals.items() if g['code'] in entries}
by_case={c['id']:c for c in cases}

# These are mathematical witnesses, computed independently of the written steps.
assert 3*1000+0*100+1*10+4==3014 and 3014!=314
assert list(range(998,1002))==[998,999,1000,1001]
assert [970+10*i for i in (1,2,3)]==[980,990,1000]
assert 2098<2103 and 999<1000
assert 10+4==7+7==14 and 10+5!=14
assert 58+67==60+65==125 and 60+67!=125
assert 52-27==52-20-2-5==25 and 32-2+5!=25
assert 7+5+3==7+3+5==15
assert 32-8-4==20 and 32-(8-4)==28
assert 25-7+5==23
assert [12-5,12-5,7+5]==[7,7,12]
assert 3+3+3+3==3*4==12 and 3+3+2!=3*3
assert 3*1==1*3==3 and 0*3==3*0==0
assert 6*7==36+6==30+12==7*6==42

# Exhaust the finite stated number domains, including exchanges and zeros.
addition=0;subtraction=0
for a in range(100):
    for b in range(100):
        ta,ua=divmod(a,10);tb,ub=divmod(b,10)
        carry,u=divmod(ua+ub,10)
        h,t=divmod(ta+tb+carry,10)
        assert 100*h+10*t+u==a+b
        addition+=1
        if a>=b:
            borrow=int(ua<ub)
            assert 10*(ta-tb-borrow)+(ua+10*borrow-ub)==a-b
            subtraction+=1
for n in range(21):
    pairs,remaining=divmod(n,2)
    assert pairs*2+remaining==n and remaining in (0,1)
    for first in range(n+1):
        second=n-first
        assert first+second==n and n-first==second and n-second==first
for a in range(10):
    for b in range(10):
        assert sum(a for _ in range(b))==a*b==sum(b for _ in range(a))

# Every authored constituent goal has an actual task; each referenced capability
# is only a condition of its named route. The union is not a universal sequence.
graph={g:set() for g in goals}
references=0
for case in cases:
    for route in case['routes']:
        for source in route['condition_sources']:
            if source['kind']=='goal':
                for target in source.get('applies_to_goal_ids',case['goal_ids']):graph[source['goal_id']].add(target)
                references+=1
active=set();done=set()
def visit(node):
    assert node not in active, 'Circular source-goal references: '+node
    if node in done:return
    active.add(node)
    for following in graph[node]:visit(following)
    active.remove(node);done.add(node)
for g in graph:visit(g)

assert set(entries)=={s['code'] for s in standards if s['code'].startswith('2수01-')}
assert '20 이하' in entries['2수01-04']['scope']
assert '세 자리' in entries['2수01-06']['scope']
assert '이항' in entries['2수01-09']['scope']
assert '20 이하' in goals['2수01-01:parity']['success']
for e in entries.values():
    assert e['source_review']['pdf_pages']==[17,18]
    assert e['history']
for case_id,word in [('early-2수01-06-add','125'),('early-2수01-06-subtract','25'),('early-2수01-11-table','42')]:
    assert all(word in route['result'] for route in by_case[case_id]['routes'])
print(json.dumps(dict(status='pass',standards=len(entries),goals=len(goals),cases=len(cases),scoped_goal_references=references,addition_checks=addition,subtraction_checks=subtraction,checks='finite-domain arithmetic; scope restrictions; goal and condition provenance; complete goal-to-task mapping; acyclic source references')))

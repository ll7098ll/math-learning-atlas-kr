"""Exact geometry, set, logic and function witnesses for Common/Basic 2."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from math import sqrt,isclose,gcd
import json
from goal_hierarchy import load_goal_hierarchies

root=Path(__file__).resolve().parents[1]
standards=json.loads((root/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s.get('subject') in ('공통수학2','기본수학2')}
selected={code:entries[code] for code in codes};cohort=[c for c in cases if c['standard'] in codes];by_case={c['id']:c for c in cohort}
assert len(codes)==37 and len(cohort)==45 and sum(len(e['goals']) for e in selected.values())==69
for prefix in ('10공수2','10기수2'):
    case=by_case['early-'+prefix+'-02-05-four-even']
    for route in case['routes']:
        refs={s.get('goal_id') for s in route['condition_sources']}
        assert '6수01-05:multiple' in refs and '6수01-02:meaning' not in refs
        assert any(s['kind']=='within_task' and '정수' in route['conditions'][s['condition_index']] for s in route['condition_sources'])
    assert any(s.get('goal_id')=='6수01-02:meaning' for h in case['history'] for r in h.get('previous_record',{}).get('routes',[]) for s in r['condition_sources'])
for code,e in selected.items():
    page=(70 if code.startswith('10공수') else 89)+int(code.split('-')[1])
    assert e['source_review']['pdf_pages']==[page] and e['source_review']['printed_pages']==[page-6]
    assert e['history']
def ds(p,q):return sum((F(x)-F(y))**2 for x,y in zip(p,q))
division_witnesses=0
for m,n in product(range(1,9),repeat=2):
    aa=(-3,2);bb=(5,-4);point=tuple(F(n*aa[i]+m*bb[i],m+n) for i in range(2))
    assert ds(aa,point)*n*n==ds(point,bb)*m*m
    assert all(min(aa[i],bb[i])<point[i]<max(aa[i],bb[i]) for i in range(2))
    division_witnesses+=1
assert -2+F(2,3)*9==4 and ds((0,0),(2,1))*4==ds((2,1),(6,3))
assert ds((-1,2),(2,6))==25 and ds((2,1),(2,6))==25
for m,n in product([F(k,3) for k in range(-9,10)],repeat=2):
    assert ((m-n)**2==2+m*m+n*n)==(m*n==-1)
assert 2*F(-1,2)==-1
distance_witnesses=0
for aa,bb,cc in product(range(-3,4),range(-3,4),range(-4,5)):
    if aa==bb==0:continue
    p=(F(1),F(-2));den=aa*aa+bb*bb;num=aa*p[0]+bb*p[1]+cc;t=num/den
    h=(p[0]-t*aa,p[1]-t*bb)
    assert aa*h[0]+bb*h[1]+cc==0 and ds(p,h)==num*num/den
    for step in [-2,-1,0,1,2]:
        q=(h[0]+step*bb,h[1]-step*aa)
        assert aa*q[0]+bb*q[1]+cc==0 and ds(p,q)==ds(p,h)+step*step*den
    distance_witnesses+=1
assert ds((0,0),(F(6,5),F(8,5)))==4
for h,k,r in [(2,-1,3),(1,2,2)]:
    for point in [(h-r,k),(h+r,k),(h,k-r),(h,k+r)]:assert ds((h,k),point)==r*r
for r in [2,3]:
    for t in [F(k,2) for k in range(-9,10)]:assert (r*r-t*t>0)==(abs(t)<r)
for s in [-10,10]:
    point=(F(3*s,25),F(4*s,25));assert ds((0,0),point)==4 and 3*point[0]+4*point[1]==s
reflection_witnesses=0
for x,y in product(range(-5,6),repeat=2):
    transformations=[lambda x,y:(-x,-y),lambda x,y:(x,-y),lambda x,y:(-x,y),lambda x,y:(y,x)]
    for transform in transformations:
        mapped=transform(x,y)
        assert transform(*mapped)==(x,y) and ds((0,0),mapped)==ds((0,0),(x,y))
        reflection_witnesses+=1
assert (1+2,-2+1)==(3,-1)
for point in [(3,0),(-3,0),(0,3),(0,-3)]:
    moved=(point[0]+2,point[1]+1);assert ds((2,1),moved)==9

U=set(range(4));subsets=[set(c) for n in range(5) for c in combinations(U,n)]
set_law_witnesses=0
for A,B,C in product(subsets,repeat=3):
    assert A|B==B|A and A&B==B&A
    assert (A|B)|C==A|(B|C) and (A&B)&C==A&(B&C)
    assert A&(B|C)==(A&B)|(A&C) and A|(B&C)==(A|B)&(A|C)
    assert U-(A|B)==(U-A)&(U-B) and U-(A&B)==(U-A)|(U-B)
    set_law_witnesses+=1
for kind in ['공수','기수']:
    v=by_case['early-10'+kind+'2-02-03-operations']['visual']
    assert v['kind']=='set_operations'
    U,A,B=map(set,[v['universe'],v['left'],v['right']])
    expected=[A|B,A&B,A-B,U-A]
    assert all(set(op['result'])==result for op,result in zip(v['operations'],expected))
    regions=[A-B,A&B,B-A,U-(A|B)]
    assert set.union(*regions)==U and sum(map(len,regions))==len(U)
    assert not any(x['id'].endswith(':laws') for x in selected['10기수2-02-03']['goals'])
    assert 8 not in {2,4,6} and set()==set([]) and len({frozenset()})==1
assert {2,4}<{1,2,3,4} and 1 not in {2,4}
for p,q in product([False,True],repeat=2):
    assert ((not p) or q)==(q or (not p))  # Original and contrapositive.
for truth_values in product([False,True],repeat=4):
    assert (not all(truth_values))==any(not v for v in truth_values)
    assert (not any(truth_values))==all(not v for v in truth_values)
for n in range(-100,101):
    assert not (n%4==0 and n%2!=0)
    assert (n*n)%2==n%2
    assert (2*n+1)**2==2*(2*n*n+2*n)+1
    assert n*n!=2
assert 2%2==0 and 2%4!=0
for aa,bb in product(range(-10,11),repeat=2):assert aa*aa+bb*bb-2*aa*bb==(aa-bb)**2>=0
for aa,bb in product(range(11),repeat=2):
    assert isclose(aa+bb-2*sqrt(aa*bb),(sqrt(aa)-sqrt(bb))**2,abs_tol=1e-12)
    assert aa+bb+1e-12>=2*sqrt(aa*bb)
for pp,qq in product(range(1,31),repeat=2):
    if gcd(pp,qq)==1:assert pp*pp!=2*qq*qq

X={-1,0,1};Y={0,1,2};mapping={x:x*x for x in X}
assert set(mapping.values())=={0,1}<Y and len(set(mapping.values()))<len(X)
assert {(x,x*x) for x in X}=={(-1,1),(0,0),(1,1)}
assert {1:2,2:3,3:4}.keys()=={1,2,3}
assert {x:2*(x+1) for x in [1,2,3]}=={1:4,2:6,3:8}
function_witnesses=0
for x in [F(n,4) for n in range(-40,41)]:
    assert (2*x+1)**2==4*x*x+4*x+1 and 2*x*x+1==(2*(x*x)+1)
    assert 2*(x+1)==2*x+2
    assert ((2*x+1)-1)/2==x and 2*((x-1)/2)+1==x
    assert (x+2)-2==x and (x-2)+2==x
    assert isclose(sqrt(float(x*x)),float(abs(x)),abs_tol=1e-12)
    if x!=1:
        y=(2*x+1)/(x-1);assert y==2+3/(x-1) and y!=2
        assert (2*(2-x)+1)/((2-x)-1)+y==4
        assert (2*x-2)/(x-1)==2
    if x:
        assert x*F(2)/x==2 and (F(2)/x)*x==2
        assert ((F(2)/x)>0)==(x>0) and ((F(-2)/x)>0)==(x<0)
        assert F(0)/x==0
    assert sqrt(float(0*x))==0
    function_witnesses+=1
assert (2*1+1)**2==9 and 2*1**2+1==3 and 2*(1+1)==4
for x,y in [(F(2),1),(F(5,2),2),(F(4),3),(F(13,2),4)]:assert isclose(sqrt(float(2*x-4))+1,y)
for x,y in [(F(2),1),(F(3,2),2),(F(0),3),(F(-5,2),4)]:assert isclose(sqrt(float(-2*x+4))+1,y)
for x,y in [(F(0),0),(F(1,2),1),(F(2),2),(F(9,2),3)]:assert sqrt(float(2*x))==y
assert sqrt(4)+1==3 and sqrt(0)+1==1

graph={g:set() for g in goals};refs=siblings=0
for case in cases:
    for route in case['routes']:
        for source in route.get('condition_sources',[]):
            if source['kind']!='goal':continue
            for target in source.get('applies_to_goal_ids',case['goal_ids']):graph[source['goal_id']].add(target)
            if case['standard'] in codes:
                refs+=1;siblings+=source['goal_id'].split(':')[0]==case['standard']
                assert not (case['standard'].startswith('10기수') and source['goal_id'].startswith('10공수'))
                assert not (case['standard'].startswith('10공수') and source['goal_id'].startswith('10기수'))
active=set();done=set()
def visit(node):
    assert node not in active,'Conditional reference cycle: '+node
    if node in done:return
    active.add(node)
    for target in graph[node]:visit(target)
    active.remove(node);done.add(node)
for node in graph:visit(node)
assert all('laws' not in g['id'] for code,e in selected.items() if code.startswith('10기수') for g in e['goals'])
assert not any(s.get('goal_id','').startswith('10공수2-01-03') for case in cohort if case['standard'].startswith('10기수') for r in case['routes'] for s in r['condition_sources'])
print(json.dumps(dict(status='pass',standards=37,goals=69,cases=45,scoped_goal_references=refs,sibling_condition_references=siblings,division_witnesses=division_witnesses,point_line_witnesses=distance_witnesses,reflection_witnesses=reflection_witnesses,set_law_witnesses=set_law_witnesses,function_witnesses=function_witnesses,checks='internal ratio direction; perpendicular shortest distance; circle and line boundaries; fixed-axis motions; Venn partitions; exhaustive set and logic truth states; proof identities; composition domains; inverse bijections; rational cancellation; radical branches; alternative course isolation; acyclic references')))

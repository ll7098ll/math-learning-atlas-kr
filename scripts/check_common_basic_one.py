"""Arithmetic witnesses and scope audit for Common/Basic Mathematics 1."""
from fractions import Fraction as F
from itertools import product,permutations,combinations
from math import sqrt,perm,comb,factorial,isclose
from pathlib import Path
import json
from goal_hierarchy import load_goal_hierarchies

root=Path(__file__).resolve().parents[1]
standards=json.loads((root/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s.get('subject') in ('공통수학1','기본수학1')}
selected={code:entries[code] for code in codes};cohort=[c for c in cases if c['standard'] in codes]
by_case={c['id']:c for c in cohort}
assert len(selected)==36 and len(cohort)==47 and sum(len(e['goals']) for e in selected.values())==62
assert len([c for c in codes if c.startswith('10공수')])==19
assert len([c for c in codes if c.startswith('10기수')])==17
for code,e in selected.items():
    section=int(code.split('-')[1]);common=code.startswith('10공수')
    pages=([66] if section==1 else [67,68] if section==2 else [68] if section==3 else [69]) if common else ([85,86] if section==1 else [86,87] if section==2 else [87,88] if section==3 else [88])
    assert e['source_review']['pdf_pages']==pages and e['source_review']['printed_pages']==[p-6 for p in pages]
    assert e['history']

arithmetic=0
for x in [F(n,4) for n in range(-48,49)]:
    aa=x*x+2*x+1;bb=x*x-x+3
    assert aa+bb==2*x*x+x+4 and aa-bb==3*x-2
    assert (x+1)*(x+2)==x*x+3*x+2
    assert x**3-2*x+1==(x-2)*(x*x+2*x+2)+5
    assert (x-1)*(x+2)==x*x+x-2
    assert (x*x+2*x+1)+(2*x*x-x)==3*x*x+x+1
    assert (2*x*x+3*x-1)-(x*x-2*x+4)==x*x+5*x-5
    assert (x+1)*(x*x+2)==x**3+x*x+2*x+2
    assert 2*x*x+4*x==2*x*(x+2)
    assert 4*x*x-9==(2*x-3)*(2*x+3)
    assert x*x+5*x+6==(x+2)*(x+3)
    assert 2*x*x+5*x+3==(2*x+3)*(x+1)
    assert x**3+6*x*x+12*x+8==(x+2)**3
    assert x**3-6*x*x+12*x-8==(x-2)**3
    assert x**3+8==(x+2)*(x*x-2*x+4)
    assert x**3-8==(x-2)*(x*x+2*x+4)
    assert (-2*x+1<=5)==(x>=-2)
    assert (-2*x+1<=5 and x<3)==(-2<=x<3)
    assert (x>=-1 and 2*x<6)==(-1<=x<3)
    assert not (x<1 and x>=2)
    assert (abs(2*x-1)<=3)==(-1<=x<=2)
    assert (abs(2*x-1)>3)==(x<-1 or x>2)
    assert not abs(x-1)<-2 and abs(x-1)>=-2
    assert (abs(x-1)<=2)==(-1<=x<=3)
    assert (abs(x-1)>2)==(x<-1 or x>3)
    assert not abs(x-1)<-1
    assert ((x-2)*(x-4)<=0)==(2<=x<=4)
    assert (-(x-2)*(x-4)<0)==(x<2 or x>4)
    assert ((x-1)**2<=0)==(x==1) and ((x-1)**2>0)==(x!=1)
    assert ((x-2)*(x-4)<=0 and x*x-9>0)==(3<x<=4)
    assert (x*x-3*x+2<=0)==(1<=x<=2)
    assert (x*x-3*x+2<0)==(1<x<2)
    if x!=2:assert (x**3-2*x+1)/(x-2)==x*x+2*x+2+5/(x-2)
    if x!=-1:assert (x**3+x*x+2*x+2)/(x+1)==x*x+2
    arithmetic+=1
square_witnesses=0
for x,y,z in product(range(-4,5),repeat=3):
    assert x*x+y*y+z*z+2*x*y+2*y*z+2*z*x==(x+y+z)**2
    square_witnesses+=1
assert 2**3-2*2+1==5 and 1**3-2*1+1==0
assert (2+3j)+(1-2j)==3+1j and (2+3j)-(1-2j)==1+5j
assert (2+3j)*(1-2j)==8-1j and (1+1j)/(1-1j)==1j
for k in range(-5,7):
    d=4*(1-k)
    if k<1:
        roots=[1-sqrt(1-k),1+sqrt(1-k)]
        assert d>0 and roots[0]!=roots[1]
    elif k==1:roots=[1,1];assert d==0
    else:roots=[1-1j*sqrt(k-1),1+1j*sqrt(k-1)];assert d<0
    assert all(abs(x*x-2*x+k)<1e-10 for x in roots)
assert (1+1j)+(1-1j)==2 and (1+1j)*(1-1j)==2
assert 1+2==3 and 1*2==2 and 1+1==2 and 1*1==1
for x in [1,3]:assert x*x-4*x+3==0
for x in [1,2]:assert x*x-3*x+2==0
assert F(3,2)**2-3*F(3,2)+2==F(-1,4)
for k in range(-5,6):
    assert 4*(k+1)==(-2)**2-4*(-k)
    if k>=-1:
        for x in [1-sqrt(k+1),1+sqrt(k+1)]:assert isclose(x*x,2*x+k,abs_tol=1e-10)
assert 1*1==2*1-1
f=lambda x:(x-1)**2+2
assert [f(x) for x in [-1,1,2,4]]==[6,2,3,11]
for x in [F(n,100) for n in range(-100,401)]:
    if -1<=x<=2:assert 2<=f(x)<=6
    if 2<=x<=4:assert 3<=f(x)<=11
    if 0<=x<=3:assert 2<=f(x)<=6
assert f(0)==3 and f(3)==6
assert 5*(10-5)==25
for x in [F(n,100) for n in range(1,1000)]:assert 0<x*(10-x)<=25
assert 25-(F(1,1000)-5)**2>0
extrema_revision=json.loads((root/'data/revisions_high.json').read_text(encoding='utf-8'))['10공수1-02-06']
assert '열린 구간' in extrema_revision['conditions'][0] and '닫힌 구간' in extrema_revision['conditions'][0]
# An arbitrary interior point cannot minimize x(10-x): move toward its
# nearer endpoint while staying strictly inside the domain.
for x in [F(n,100) for n in range(1,1000)]:
    y=x/2 if x<=5 else (x+10)/2
    assert 0<y<10 and 0<y*(10-y)<x*(10-x)<=25
for x in [1,complex(-1,sqrt(3))/2,complex(-1,-sqrt(3))/2]:assert abs(x**3-1)<1e-10
for x in [-2,-1,1,2]:assert x**4-5*x*x+4==0
for x in [-1,1,-1j,1j]:assert x**4==1
assert {(x,y) for x,y in product(range(-5,6),repeat=2) if x+y==5 and x*y==6}=={(2,3),(3,2)}
assert {(x,y) for x,y in product(range(-5,6),repeat=2) if x*x-y*y==0 and x*x+y*y==18}=={(3,3),(-3,-3),(3,-3),(-3,3)}
assert all(x*x-5*x+6==0 for x in [2,3])
assert all((x-1)**2==9 for x in [-2,4])
assert all(abs(x*x-2*x-1)<1e-12 for x in [1-sqrt(2),1+sqrt(2)])
assert [-((x-1)**2)+2 for x in [-1,0,1,2,3]]==[-2,1,2,1,-2]

counting=0
for n in range(0,8):
    for r in range(0,n+1):
        ordered=list(permutations(range(n),r));unordered=list(combinations(range(n),r))
        assert len(ordered)==perm(n,r)==factorial(n)//factorial(n-r)
        assert len(unordered)==comb(n,r)==len(ordered)//factorial(r)
        assert {frozenset(x) for x in ordered}=={frozenset(x) for x in unordered}
        counting+=1
assert len(list(product('AB','123')))==6
assert len({'B1','B2'}|{'T1','T2','T3'})==5
assert perm(5,2)==20 and perm(4,2)==12 and comb(5,2)==10 and comb(4,2)==6

def mm(aa,bb):
    assert len(aa[0])==len(bb)
    return [[sum(aa[i][k]*bb[k][j] for k in range(len(bb))) for j in range(len(bb[0]))] for i in range(len(aa))]
aa=[[1,2],[3,4]];bb=[[2,0],[1,3]]
assert mm(aa,bb)==[[4,6],[10,12]] and mm(bb,aa)==[[2,4],[10,14]]
assert [[aa[i][j]+bb[i][j] for j in range(2)] for i in range(2)]==[[3,2],[4,7]]
assert [[aa[i][j]-bb[i][j] for j in range(2)] for i in range(2)]==[[-1,2],[2,1]]
assert [[2*v for v in row] for row in aa]==[[2,4],[6,8]]
matrix_witnesses=0
for values in product(range(-1,2),repeat=4):
    matrix=[list(values[:2]),list(values[2:])]
    for vector in product(range(-2,3),repeat=2):
        col=[[vector[0]],[vector[1]]]
        result=mm(matrix,col)
        assert result==[[values[0]*vector[0]+values[1]*vector[1]],[values[2]*vector[0]+values[3]*vector[1]]]
        matrix_witnesses+=1
for kind,expected in [('공수',[[1300],[800]]),('기수',[[1200],[1000]])]:
    visual=by_case['early-10'+kind+'1-04-02-sales']['visual']
    assert visual['kind']=='matrix_product'
    assert visual['left']['columns']==visual['right']['rows']
    assert mm(visual['left']['values'],visual['right']['values'])==visual['result']['values']==expected
    for matrix in [visual['left'],visual['right'],visual['result']]:
        assert 0<len(matrix['rows'])<=2 and 0<len(matrix['columns'])<=2
        assert len(matrix['values'])==len(matrix['rows'])
        assert all(len(row)==len(matrix['columns']) for row in matrix['values'])

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
    assert node not in active,'Conditional reference cycle '+node
    if node in done:return
    active.add(node)
    for target in graph[node]:visit(target)
    active.remove(node);done.add(node)
for node in graph:visit(node)
assert not any(s.get('goal_id','').startswith('10공수1-02-01') for case in cohort if case['standard'].startswith('10기수') for route in case['routes'] for s in route['condition_sources'])
assert all('0이 아니' in ' '.join(c['shared_conditions']) or c['standard']!='10공수1-02-01' for c in cohort)
print(json.dumps(dict(status='pass',standards=36,goals=62,cases=47,scoped_goal_references=refs,sibling_condition_references=siblings,arithmetic_witnesses=arithmetic,three_variable_square_witnesses=square_witnesses,counting_witnesses=counting,matrix_witnesses=matrix_witnesses,checks='polynomial identities and quotient domains; real versus complex roots; closed and open range bounds; simultaneous pairs; exact inequality endpoints; enumeration and constant multiplicity; matrix dimensions and visual data; alternative course isolation; acyclic scoped goals')))

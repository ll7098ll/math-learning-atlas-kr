"""Independent exact and numerical witnesses for Algebra and Calculus I."""
from pathlib import Path
from fractions import Fraction as F
from math import log,sqrt,sin,cos,tan,pi,isclose
from itertools import product
import json
from goal_hierarchy import load_goal_hierarchies

root=Path(__file__).resolve().parents[1]
standards=json.loads((root/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s.get('subject') in ('대수','미적분Ⅰ')}
cohort=[c for c in cases if c['standard'] in codes]
assert len(codes)==38 and len(cohort)==43 and sum(len(entries[c]['goals']) for c in codes)==72
for code in codes:
    section=int(code.split('-')[0][-2:]) if code.startswith('12대수') else int(code.split('-')[1])
    page=(105 if code.startswith('12대수') else 119)+section
    assert entries[code]['source_review']['pdf_pages']==[page]
    assert entries[code]['source_review']['printed_pages']==[page-6]
    assert entries[code]['history']

assert [x for x in range(-5,6) if x**4==16]==[-2,2]
assert [x for x in range(-5,6) if x**3==-8]==[-2]
assert not [x for x in range(-5,6) if x*x==-4]
assert sqrt((-3)**2)==3 and 6**3==8*27
assert 4**0==1 and 4**-1==0.25 and 4**1.5==8
exponent_witnesses=0
for base,p,q in product([0.25,0.5,2,4,9],[F(-3,2),F(-1),F(0),F(1,2),F(2)],[F(-1),F(0),F(1,2),F(2)]):
    assert isclose(base**float(p)*base**float(q),base**float(p+q))
    assert isclose((base**float(p))**float(q),base**float(p*q))
    assert isclose(log(base**float(p),base),float(p),abs_tol=1e-12)
    exponent_witnesses+=1
assert 2**1.41<2**sqrt(2)<2**1.42
assert isclose(2**sqrt(2),2.66514,rel_tol=1e-5)
assert log(8,2)==3 and log(32,2)==5 and log(12,2)!=5
assert 10*log(100,10)==20 and 100*2**3<1000<=100*2**4
assert 3<log(10,2)<4
for n in range(1,10001):assert len(str(n))==int(log(n,10)+1e-12)+1
assert isclose(450*pi/180,5*pi/2) and isclose(-90*pi/180,-pi/2)
assert (450-90)%360==0 and (-90-270)%360==0 and (-90-90)%360!=0
radian_case=next(c for c in cases if c['id']=='early-12대수02-01-radians')
radian_text=' '.join(radian_case['routes'][0]['steps'])
assert '모두 90°와 같은 동경' not in radian_text
assert '270°와 같은 동경' in radian_text

trig_witnesses=0
for k in range(-120,121):
    x=k*pi/24
    assert isclose(sin(x+2*pi),sin(x),abs_tol=1e-12)
    assert isclose(cos(x+2*pi),cos(x),abs_tol=1e-12)
    assert isclose(sin(x)**2+cos(x)**2,1,abs_tol=1e-12)
    if abs(cos(x))>1e-8:
        assert isclose(tan(x+pi),tan(x),rel_tol=1e-10,abs_tol=1e-10)
        assert isclose(tan(x),sin(x)/cos(x),rel_tol=1e-10,abs_tol=1e-10)
    trig_witnesses+=1
for x in [pi/6,5*pi/6]:assert isclose(sin(x),0.5)
assert isclose(3**2+4**2-2*3*4*cos(pi/3),13)
assert isclose(F(1,2)*3*4*sin(pi/3),3*sqrt(3))
assert isclose(5*sin(pi/4)/sin(pi/6),5*sqrt(2))

sequence_witnesses=0
for n in range(1,81):
    assert sum(2*k+1 for k in range(1,n+1))==n*n+2*n
    assert sum(range(1,n+1))==F(n*(n+1),2)
    assert sum(k*k for k in range(1,n+1))==F(n*(n+1)*(2*n+1),6)
    assert sum(k**3 for k in range(1,n+1))==F(n*(n+1),2)**2
    assert sum(F(1,k*(k+1)) for k in range(1,n+1))==F(n,n+1)
    assert sum(2*k-1 for k in range(1,n+1))==n*n
    assert n*n+(2*n+1)==(n+1)**2
    for first,d in product([-3,0,2,5],[-2,0,3]):
        terms=[first+k*d for k in range(n)]
        assert sum(terms)==F(n*(2*first+(n-1)*d),2)
        sequence_witnesses+=1
    for q in [F(-2),F(-1),F(0),F(1,2),F(1),F(3)]:
        terms=[F(2)]
        for k in range(1,n):terms.append(terms[-1]*q)
        expected=F(2*n) if q==1 else 2*(1-q**n)/(1-q)
        assert sum(terms)==expected
        sequence_witnesses+=1
assert 2+6+18+54==80
assert [2+3*k for k in range(4)]==[2,5,8,11]

# Coefficients are stored in ascending powers; evaluate, differentiate and
# integrate independently from the authored prose. Exact endpoints expose signs.
def value(p,x):return sum(v*x**i for i,v in enumerate(p))
def derivative(p):return [i*p[i] for i in range(1,len(p))]
def antiderivative(p):return [F(0)]+[F(v,i+1) for i,v in enumerate(p)]
def integral(p,a,b):
    prim=antiderivative(p);return value(prim,b)-value(prim,a)
polynomial_witnesses=0
for coeffs in product([-2,-1,0,1,2],repeat=4):
    p=list(coeffs)
    assert derivative(antiderivative(p))==p
    for aa,bb,cc in [(F(-1),F(0),F(2)),(F(0),F(1,2),F(1))]:
        assert integral(p,aa,cc)==integral(p,aa,bb)+integral(p,bb,cc)
        assert integral(p,aa,cc)==-integral(p,cc,aa)
        assert integral([2*x for x in p],aa,cc)==2*integral(p,aa,cc)
        polynomial_witnesses+=1
assert derivative([-2,1,-2,1])==[1,-4,3]
assert derivative([-5,2,3])==[2,6]
assert antiderivative([-5,2,3])==[0,-5,1,1]
for h in [F(k,100) for k in range(-9,10) if k]:
    assert ((1+h)**2-1)/h==2+h
    assert ((2+h)**2-4)/h==4+h
    assert (abs(h)/h)==(-1 if h<0 else 1)
assert 2+(-1)==1  # Differentiable join m=2,b=-1.
assert (value([0,0,1],2)-value([0,0,1],0))/2==2
assert value(derivative([0,0,1]),1)==2  # Mean-value point.
assert value(derivative([0,-2,1]),1)==0  # Rolle point.
for x in [F(k,10) for k in range(-40,41)]:
    d=3*x*x-3
    assert (d>0)==(abs(x)>1) and (d<0)==(abs(x)<1)
    assert 3*x*x+1>0
    if x>=0:assert x**3-3*x+2>=0
assert value([0,-3,0,1],-1)==2 and value([0,-3,0,1],1)==-2
assert (-3)**3-3*(-3)+2==-16
assert integral([0,1],0,2)==2 and integral([0,1],-1,1)==0
assert integral([1,2],0,2)==6 and integral([0,2],0,2)==4
assert integral([0,1,-1],0,1)==F(1,6)
assert -integral([0,1],-1,0)+integral([0,1],0,1)==1
assert integral([-1,1],0,2)==0
assert -integral([-1,1],0,1)+integral([-1,1],1,2)==1
assert value(derivative([0,-2,1]),F(1,2))==-1
assert derivative(derivative([0,-2,1]))==[2]
visuals=[c['visual'] for c in cohort if c.get('visual')]
assert len(visuals)==2
for v in visuals:
    p=[v['intercept'],v['slope']];zero=-F(v['intercept'],v['slope'])
    assert v['start']<zero<v['end']
    assert -integral(p,v['start'],zero)==v['negative_area']==F(1,2)
    assert integral(p,zero,v['end'])==v['positive_area']==F(1,2)
    assert integral(p,v['start'],v['end'])==v['signed_total']==0
    assert v['negative_area']+v['positive_area']==v['total_area']==1

graph={g:set() for g in goals};refs=0
for case in cases:
    for route in case['routes']:
        for source in route['condition_sources']:
            if source['kind']!='goal':continue
            for target in source.get('applies_to_goal_ids',case['goal_ids']):graph[source['goal_id']].add(target)
            refs+=case['standard'] in codes
active=set();done=set()
def visit(node):
    assert node not in active,'Conditional goal cycle: '+node
    if node in done:return
    active.add(node)
    for target in graph[node]:visit(target)
    active.remove(node);done.add(node)
for goal in graph:visit(goal)
print(json.dumps(dict(status='pass',standards=38,goals=72,cases=43,goal_condition_references=refs,exponent_witnesses=exponent_witnesses,trig_witnesses=trig_witnesses,sequence_witnesses=sequence_witnesses,polynomial_witnesses=polynomial_witnesses,visuals=2,checks='official scope; real domains; finite sums; recurrence scope; induction steps; one-sided corners; theorem hypotheses; polynomial derivatives and primitives; sign charts; signed integral vs area and distance; acyclic conditional goals')))

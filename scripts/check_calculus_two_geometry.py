"""Independent analytical identities, exact conic geometry and limit witnesses."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import exp,log,sin,cos,sqrt,pi,isclose
import json
from goal_hierarchy import load_goal_hierarchies

root=Path(__file__).resolve().parents[1]
standards=json.loads((root/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s.get('subject') in ('미적분Ⅱ','기하')}
cohort=[case for case in cases if case['standard'] in codes]
assert len(codes)==37 and len(cohort)==44 and sum(len(entries[c]['goals']) for c in codes)==66
for code in codes:
    section=int(code.split('-')[1]) if code.startswith('12미적') else int(code.split('-')[0][-2:])
    page=(149 if code.startswith('12미적') else 163)+section
    assert entries[code]['source_review']['pdf_pages']==[page]
    assert entries[code]['source_review']['printed_pages']==[page-6]
    assert entries[code]['history']

# Two-point distance is not the official segment-division goal. The conic and
# angle-addition tasks derive it from coordinates and the Pythagorean theorem.
distance_cases={'early-12미적Ⅱ-02-02-addition','early-12기하01-01-parabola',
                'early-12기하01-02-ellipse','early-12기하01-03-hyperbola'}
for case in cohort:
    if case['id'] not in distance_cases:continue
    for route in case['routes']:
        sources=route['condition_sources']
        refs={s.get('goal_id') for s in sources}
        assert {'9수02-05:coordinates','9수03-15:understand'}<=refs
        assert '10공수2-01-01:meaning' not in refs
        assert any(s['kind']=='within_task' and '거리식' in route['conditions'][s['condition_index']] for s in sources)
    assert any(s.get('goal_id')=='10공수2-01-01:meaning'
               for h in case['history'] for r in h.get('previous_record',{}).get('routes',[]) for s in r['condition_sources'])

for n in range(1,101):
    assert 2-F(2*n+1,n+3)==F(5,n+3)>0
    assert abs(F((-1)**n,n))==F(1,n)
    assert sum(F(1,2**k) for k in range(1,n+1))==1-F(1,2**n)
    assert sum(F(3,10**k) for k in range(1,n+1))==F(1,3)*(1-F(1,10**n))
    lower=sum(F(1,k) for k in range(2**n+1,2**(n+1)+1)) if n<9 else F(1,2)
    assert lower>=F(1,2)
    for q in [F(-2),F(-1),F(-1,2),F(0),F(1,2),F(1),F(2)]:
        terms=[F(2)]
        for k in range(1,n):terms.append(terms[-1]*q)
        if abs(q)<1 and n>20:assert abs(terms[-1])<=2*F(1,2)**(n-1)
        if q==1:assert terms[-1]==2
        if q==0 and n>1:assert terms[-1]==0
        if q==-1:assert abs(terms[-1])==2
        if abs(q)>1:assert abs(terms[-1])==2**n

# Central difference and composite Simpson estimates are independent numerical
# checks of stated derivatives/primitives, restricted away from singularities.
def diff(f,x,h=1e-5):return (f(x+h)-f(x-h))/(2*h)
def simpson(f,a,b,n=2000):
    h=(b-a)/n
    return h/3*(f(a)+f(b)+sum((4 if k%2 else 2)*f(a+k*h) for k in range(1,n)))
derivative_witnesses=0
functions=[(exp,exp),(log,lambda x:1/x),(lambda x:2**x,lambda x:2**x*log(2)),
 (sin,cos),(cos,lambda x:-sin(x)),
 (lambda x:(x*x+1)/(x+1),lambda x:(x*x+2*x-1)/(x+1)**2),
 (lambda x:sin(x*x),lambda x:2*x*cos(x*x)),
 (lambda x:sqrt(x),lambda x:1/(2*sqrt(x))),
 (lambda x:x*exp(-x),lambda x:exp(-x)*(1-x)),
 (lambda x:exp(-x)*(1-x),lambda x:exp(-x)*(x-2)),
 (lambda x:sin(x*x),lambda x:2*x*cos(x*x)),
 (lambda x:(x-1)*exp(x),lambda x:x*exp(x)),
 (lambda x:sin(x)/cos(x),lambda x:1/cos(x)**2),
 (lambda x:cos(x)/sin(x),lambda x:-1/sin(x)**2),
 (lambda x:1/cos(x),lambda x:sin(x)/cos(x)**2),
 (lambda x:1/sin(x),lambda x:-cos(x)/sin(x)**2)]
for f,df in functions:
    for x in [0.2,0.5,1,1.5,2,3]:
        assert isclose(diff(f,x),df(x),rel_tol=1e-6,abs_tol=1e-7)
        derivative_witnesses+=1
for h in [1e-3,-1e-3,1e-5,-1e-5]:
    assert isclose(sin(h)/h,1,rel_tol=1e-6)
    assert abs((cos(h)-1)/h)<0.001
    assert isclose((exp(h)-1)/h,1,rel_tol=0.001)
    assert isclose(log(1+h)/h,1,rel_tol=0.001)
for alpha,beta in product([k*pi/12 for k in range(-12,13)],repeat=2):
    assert isclose(sin(alpha+beta),sin(alpha)*cos(beta)+cos(alpha)*sin(beta),abs_tol=1e-12)
    assert isclose(cos(alpha-beta),cos(alpha)*cos(beta)+sin(alpha)*sin(beta),abs_tol=1e-12)
assert isclose(sin(5*pi/12),(sqrt(6)+sqrt(2))/4)
for x in [k/10 for k in range(-60,61)]:
    assert exp(x)>=x+1-1e-12
    assert isclose(sin(x)**2+cos(x)**2,1,abs_tol=1e-12)
assert isclose(simpson(lambda x:1/x,1,exp(1)),1,rel_tol=1e-10)
assert isclose(simpson(exp,0,1),exp(1)-1,rel_tol=1e-10)
assert isclose(simpson(sin,0,pi),2,rel_tol=1e-10)
assert isclose(simpson(lambda x:2*x*cos(x*x),1,2),sin(4)-sin(1),abs_tol=1e-10)
assert isclose(simpson(lambda x:x*exp(x),0,1),1,rel_tol=1e-10)
assert isclose(simpson(abs_sin:=lambda x:abs(sin(x)),0,2*pi),4,rel_tol=1e-10)
assert isclose(simpson(sin,0,2*pi),0,abs_tol=1e-10)
for radius in [0.5,1,2,3]:assert isclose(simpson(lambda x:pi*(radius*radius-x*x),-radius,radius),4*pi*radius**3/3,rel_tol=1e-10)

rectangle_witnesses=0
for n in range(1,101):
    left=sum(F(k*k,n**3) for k in range(n));right=sum(F(k*k,n**3) for k in range(1,n+1))
    assert left==F((n-1)*(2*n-1),6*n*n)
    assert right==F((n+1)*(2*n+1),6*n*n)
    assert left<F(1,3)<right and right-left==F(1,n)
    rectangle_witnesses+=1
visual=next(c for c in cohort if c['id']=='early-12미적Ⅱ-03-04-rectangles')['visual']
assert visual['partitions']==[4,8] and visual['integral']=='1/3'
assert F(5*9,6*16)==F(15,32) and F(9*17,6*64)==F(51,128)

def ds(p,q):return sum((F(x)-F(y))**2 for x,y in zip(p,q))
def dot(p,q):return sum(x*y for x,y in zip(p,q))
conic_witnesses=0
for t in [F(k,12) for k in range(-30,31)]:
    p=(t,t*t/4)
    assert ds(p,(0,1))==(p[1]+1)**2 and p[1]>=0
    x=5*(1-t*t)/(1+t*t);y=8*t/(1+t*t)
    assert x*x/25+y*y/16==1
    assert ds((x,y),(-3,0))==(5+3*x/5)**2
    assert ds((x,y),(3,0))==(5-3*x/5)**2
    assert 5+3*x/5>0 and 5-3*x/5>0
    conic_witnesses+=2
for t in [F(k,20) for k in range(-19,20)]:
    for sign in [-1,1]:
        x=sign*3*(1+t*t)/(1-t*t);y=8*t/(1-t*t)
        assert x*x/9-y*y/16==1 and abs(x)>=3
        assert ds((x,y),(-5,0))==(5*x/3+3)**2
        assert ds((x,y),(5,0))==(5*x/3-3)**2
        conic_witnesses+=1
# Discriminants computed directly from substitution coefficients, including the
# degree-dropping asymptotes; a zero formal discriminant alone is insufficient.
for m,b in product([F(k,2) for k in range(-6,7)],[F(k,3) for k in range(-9,10)]):
    aa=m*m;bb=2*m*b-4;cc=b*b
    assert bb*bb-4*aa*cc==16*(1-m*b)
    aa=1+4*m*m;bb=8*m*b;cc=4*b*b-4
    assert bb*bb-4*aa*cc==16*(1+4*m*m-b*b)
    aa=1-4*m*m;bb=-8*m*b;cc=-4*b*b-4
    assert bb*bb-4*aa*cc==16*(1-4*m*m+b*b)
    if m in [F(-1,2),F(1,2)] and b==0:assert aa==bb==0 and cc==-4
assert isclose((4/sqrt(3))**2/4-(1/sqrt(3))**2,1)
assert isclose(4/sqrt(3)-sqrt(3),1/sqrt(3))
assert (1-4*1)**2==3*(4*1**2-1)
point_case=next(c for c in cohort if c['id']=='early-12기하01-04-point-tangent')
assert [r['id'] for r in point_case['routes']]==['discriminant','implicit']
assert not any(s.get('goal_id','').startswith('12미적') for s in point_case['routes'][0]['condition_sources'])
assert any(s.get('goal_id')=='12미적Ⅱ-02-07:implicit' for s in point_case['routes'][1]['condition_sources'])

space_witnesses=0
for x,y,z in product(range(-3,4),repeat=3):
    p=(F(x),F(y),F(z));q=(F(-2),F(1),F(4))
    for m,n in [(1,2),(2,1),(3,4)]:
        point=tuple((n*p[i]+m*q[i])/(m+n) for i in range(3))
        assert ds(p,point)*n*n==ds(point,q)*m*m
        space_witnesses+=1
    assert dot(p,q)==sum(p[i]*q[i] for i in range(3))
for h,d,t in product(range(1,6),range(1,6),range(-5,6)):
    P=(0,0,h);H=(0,0,0);Q=(d,0,0);R=(d,t,0)
    assert ds(P,R)==ds(P,H)+ds(H,R)==ds(P,Q)+ds(Q,R)
assert ds((0,0,0),(2,4,4))==36
assert ds((0,0,0),(F(2,3),F(4,3),F(4,3)))==4
assert ds((2,4,4),(F(2,3),F(4,3),F(4,3)))==16
assert isclose(6*cos(pi/3),3) and isclose(10*cos(pi/3),5)
projection_revision=json.loads((root/'data/revisions_high.json').read_text(encoding='utf-8'))['12기하02-03']
assert '0°≤θ≤90°' in projection_revision['conditions'][0] and '0°≤φ≤90°' in projection_revision['conditions'][0]
assert '예각' not in projection_revision['conditions'][0]
assert isclose(6*cos(0),6) and isclose(10*cos(0),10)
assert isclose(6*cos(pi/2),0,abs_tol=1e-12) and isclose(10*cos(pi/2),0,abs_tol=1e-12)
for height,r2 in [(3,4),(4,3),(5,0),(6,-5)]:assert 4-(height-3)**2==r2
assert dot((1,2),(2,-1))==0 and dot((1,2,0),(0,-1,3))==-2
for t in [F(k,2) for k in range(-10,11)]:
    p=(1,2+2*t,3-t)
    assert p[0]==1 and (p[1]-2)/2==-(p[2]-3)
for y,z in product(range(-5,6),repeat=2):
    p=(1-2*y+z,y,z)
    assert dot((1,2,-1),(p[0]-1,p[1],p[2]))==0
for p in [(3,2,3),(-1,2,3),(1,4,3),(1,2,1)]:assert ds(p,(1,2,3))==4

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
print(json.dumps(dict(status='pass',standards=37,goals=66,cases=44,scoped_goal_references=refs,derivative_witnesses=derivative_witnesses,rectangle_witnesses=rectangle_witnesses,conic_witnesses=conic_witnesses,space_witnesses=space_witnesses,checks='partial sums; geometric boundaries; derivative limits; domain exclusions; quadrature; Riemann widths; conic distance and discriminant degree; optional OR route; three perpendiculars; projection limits; vector domains; acyclic goal conditions')))

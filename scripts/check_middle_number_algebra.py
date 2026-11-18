"""Independent arithmetic/identity witnesses and scoped reference regressions."""
from fractions import Fraction as F
from math import gcd,lcm,prod,isclose,sqrt
from pathlib import Path
import json
from goal_hierarchy import load_goal_hierarchies

ROOT=Path(__file__).resolve().parents[1]
standards=json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={'9수01-'+str(i).zfill(2) for i in range(1,11)}|{'9수02-'+str(i).zfill(2) for i in [1,2,3,4,8,9,10,11,12,13,19,20]}
selected={code:e for code,e in entries.items() if code in codes}
selected_cases=[case for case in cases if case['standard'] in codes]
by_case={case['id']:case for case in selected_cases}
assert len(selected)==22 and sum(len(e['goals']) for e in selected.values())==49 and len(selected_cases)==37
substitution=by_case['early-9수02-01-substitute']
assert {'9수01-05:multiply','9수01-05:add'}<={s.get('goal_id') for r in substitution['routes'] for s in r['condition_sources']}
polynomial=by_case['early-9수02-09-polynomial-sums']
applications={s['goal_id']:s['applies_to_goal_ids'] for r in polynomial['routes'] for s in r['condition_sources'] if s['kind']=='goal'}
assert applications['9수02-02:add']==['9수02-09:add']
assert applications['9수02-02:subtract']==['9수02-09:subtract']

def factors(n):
    result={};p=2
    while p*p<=n:
        while n%p==0:result[p]=result.get(p,0)+1;n//=p
        p+=1
    if n>1:result[n]=result.get(n,0)+1
    return result
assert factors(60)=={2:2,3:1,5:1} and 6*10==4*15==60
assert factors(36)=={2:2,3:2} and gcd(36,60)==12 and lcm(36,60)==180
factor_checks=0
for x in range(1,81):
    fx=factors(x)
    assert prod(p**e for p,e in fx.items())==x
    assert all(p>1 and all(p%d for d in range(2,p)) for p in fx)
    for y in range(1,81):
        fy=factors(y);primes=fx.keys()|fy.keys()
        assert prod(p**min(fx.get(p,0),fy.get(p,0)) for p in primes)==gcd(x,y)
        assert prod(p**max(fx.get(p,0),fy.get(p,0)) for p in primes)==lcm(x,y)
        factor_checks+=1
assert F(-3,4)<F(-1,2)<0<2 and -5<-2
assert -3+5==2 and F(-3,4)+F(1,2)==F(-1,4)
assert 2-(-3)==5 and F(-1,2)-F(3,4)==F(-5,4)
assert -3*(-2)==6 and F(-2,3)*F(3,4)==F(-1,2)
assert F(-3,4)/F(-1,2)==F(3,2) and F(0,2)==0
try:F(2)/0
except ZeroDivisionError:pass
else:raise AssertionError('Division by zero must remain undefined')
signed_pairs=0
values=sorted({F(n,d) for n in range(-8,9) for d in range(1,6)})
for x in values:
    for y in values:
        assert (x-y)+y==x and x-y==x+(-y)
        assert (-x)*(-y)==x*y and x*(y-y)==x*y+x*(-y)==0
        if y:assert (x/y)*y==x and x/y==x*F(y.denominator,y.numerator)
        signed_pairs+=1
assert F(1,3)!=F('0.333') and F(27,99)==F(3,11)!=F('0.27')
assert 100*F(3,11)-F(3,11)==27 and F('0.125')==F(1,8)
assert (-3)**2==3**2==9 and sqrt(9)==3 and sqrt((-3)**2)==abs(-3)
for n in range(-100,101):
    assert (n*n)%2==n%2 and sqrt(n*n)==abs(n)
assert F('1.4')**2==F('1.96')<2 and F('1.41')**2==F('1.9881')<2
assert F('1.7')**2<3 and F('2.3')**2>5 and F('1.4')+F('1.7')>F('2.3')
assert -sqrt(5)<-2 and sqrt(2)+1>sqrt(5)
assert isclose(sqrt(12)+sqrt(27)-sqrt(3),4*sqrt(3))
assert isclose(sqrt(6)*sqrt(3),3*sqrt(2)) and isclose(sqrt(18)/sqrt(2),3)
assert isclose(1/sqrt(2),sqrt(2)/2)
assert 3*(-2)+2==-4 and (-2)**2==4 and -((-2)**2)==-4

# Coefficient algebra verifies the identities for all real x, rather than only examples.
def clean(poly):
    poly=list(map(F,poly))
    while len(poly)>1 and not poly[-1]:poly.pop()
    return poly
def add(a,b):return clean([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def scale(a,k):return clean([F(v)*k for v in a])
def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=F(x)*y
    return clean(out)
def evaluate(a,x):return sum(F(v)*x**i for i,v in enumerate(a))
assert add([3,2],[5,-1])==[8,1] and add([3,2],scale([5,-1],-1))==[-2,3]
A=[3,-1,2];B=[-5,4,-1]
assert add(A,B)==[-2,3,1] and add(A,scale(B,-1))==[8,-5,3]
assert mul([0,3],[-3,2])==[0,-9,6]
forms=[([3],[2,1],[6,3]),([2,1],[2,1],[4,4,1]),([-2,1],[-2,1],[4,-4,1]),([2,1],[-2,1],[-4,0,1]),([2,1],[3,1],[6,5,1]),([1,2],[-2,3],[-2,-1,6])]
for left,right,expected in forms:assert mul(left,right)==expected
assert mul([0,1],[-3,1])==[0,-3,1] and mul([-2,1],[-2,1])==[4,-4,1]
assert mul([-3,1],[4,1])==[-12,1,1]
assert evaluate([0,-3,1],0)==evaluate([0,-3,1],3)==0
assert evaluate([4,-4,1],2)==0
assert evaluate([-12,1,1],3)==evaluate([-12,1,1],-4)==0
assert 3*4==12 and 4-3==1
# Exact Q(sqrt(5)) arithmetic for both irrational quadratic roots.
def root_mul(p,q):return (p[0]*q[0]+5*p[1]*q[1],p[0]*q[1]+p[1]*q[0])
for root in [(F(2),F(1)),(F(2),F(-1))]:
    squared=root_mul(root,root)
    assert (squared[0]-4*root[0]-1,squared[1]-4*root[1])==(0,0)
assert (-4)**2-4*1*(-1)==20 and 2*1!=0

exponent_checks=0
for a_ in range(-5,6):
    for m in range(1,7):
        for n in range(1,7):
            assert a_**m*a_**n==a_**(m+n) and (a_**m)**n==a_**(m*n)
            if a_ and m>=n:assert F(a_**m,a_**n)==(1 if m==n else a_**(m-n))
            exponent_checks+=1
assert (2*3**2)**3==8*3**6
assert evaluate([3,1],4)==7 and evaluate([3,1],2)!=7
assert 2*(3*4-1)==4*4+6==22 and 2*6+3==15
inequality_checks=0
for x in [F(n,4) for n in range(-40,41)]:
    assert (-2*x+3<=7)==(x>=-2)
    for y in [F(n,2) for n in range(-10,11)]:
        for k in [-3,-1,1,3]:
            assert (x<y)==(k*x<k*y if k>0 else k*x>k*y)
            inequality_checks+=1
assert [n for n in range(9) if 3*n+2<=17]==list(range(6))
assert [(x,y) for x in range(-10,11) for y in range(-10,11) if x+y==7 and 2*x-y==2]==[(3,4)]
assert [(x,y) for x in range(8) for y in range(8) if x+y==7 and 2*x+y==10]==[(3,4)]
assert [2,2]==[2*v for v in [1,1]] and 5!=2*2
for x in [F(n,3) for n in range(-20,21)]:
    y=2-x
    assert x+y==2 and 2*x+2*y==4 and 2*x+2*y!=5

graph={goal:set() for goal in goals};refs=siblings=0
for case in cases:
    for route in case['routes']:
        for source in route['condition_sources']:
            if case['standard'] in codes:assert source['applies_to_goal_ids'] and set(source['applies_to_goal_ids'])<=set(case['goal_ids'])
            if source['kind']=='goal':
                for target in source.get('applies_to_goal_ids',case['goal_ids']):graph[source['goal_id']].add(target)
                if case['standard'] in codes:refs+=1;siblings+=source['goal_id'].split(':')[0]==case['standard']
active=set();done=set()
def visit(node):
    assert node not in active,'Review conditional reference cycle: '+node
    if node in done:return
    active.add(node)
    for following in graph[node]:visit(following)
    active.remove(node);done.add(node)
for goal in graph:visit(goal)
assert '9수01-02:gcd' in graph['6수01-04:greatest']
assert all('6수01-04:greatest' not in graph[goal['id']] for goal in selected['9수01-01']['goals'])
assert all(s.get('goal_id')!='9수02-19:factor' for r in by_case['early-9수02-04-solve']['routes'] for s in r['condition_sources'])
assert all(s.get('goal_id')!='9수02-20:solve' for r in by_case['early-9수02-19-factor']['routes'] for s in r['condition_sources'])
assert all(e['source_review']['pdf_pages']==([39,40] if code.startswith('9수01-') else [40,41,42,43]) for code,e in selected.items())
assert all(e['history'] for e in selected.values())
assert any('a≠0' in text for text in by_case['early-9수02-10-distribute']['shared_conditions'])
legacy=json.loads((ROOT/'data/revisions_middle.json').read_text(encoding='utf-8'))['9수02-20']
assert 'x²+1=0은 실수 해가 없다' not in legacy['taskSolution']
assert '(x−2)²=0의 중근은 2' in legacy['taskSolution']
assert 'x²+1=0은 실수 해가 없다' in legacy['scopeCorrections'][-1]['previous_task_solution']
def result(case_id,fragment):assert all(fragment in r['result'].replace(' ','') for r in by_case['early-'+case_id]['routes'])
for case_id,fragment in [('9수01-02-gcd-lcm','180'),('9수01-05-divide','3/2'),('9수01-06-fraction','3/11'),('9수01-10-add-subtract','4√3'),('9수02-04-solve','x=4'),('9수02-12-solve','x≥−2'),('9수02-13-solve','x=3,y=4'),('9수02-20-irrational-roots','2')]:result(case_id,fragment)
print(json.dumps(dict(status='pass',standards=22,goals=49,cases=37,scoped_goal_references=refs,sibling_condition_references=siblings,factor_pairs=factor_checks,signed_pairs=signed_pairs,exponent_witnesses=exponent_checks,inequality_witnesses=inequality_checks,polynomial_identities=len(forms),checks='prime structure; signed rational operations; repeating decimal fractions; radical domains; coefficient identities; exact quadratic roots; inequality direction; model restrictions; scoped acyclic references')))

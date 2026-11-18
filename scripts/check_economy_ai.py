"""Independent exact calculations, official scope and goal graph checks."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import sqrt,isclose
import csv,json
from goal_hierarchy import load_goal_hierarchies
from economy_ai_models import fit_origin,fit_affine,loss,descent,cosine_components,run

root=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
entries,cases,goals=load_goal_hierarchies(read('data/standards.json')['standards'])
codes={s['code'] for s in read('data/standards.json')['standards'] if s.get('subject') in ('경제 수학','인공지능 수학')}
cohort=[case for case in cases if case['standard'] in codes]
assert len(codes)==33 and len(cohort)==40 and sum(len(entries[c]['goals']) for c in codes)==58
for code in codes:
    section=int(code.split('-')[0][-2:])
    pages=([177+section] if section<4 else [180,181]) if code.startswith('12경수') else {1:[192],2:[193],3:[194],4:[194,195],5:[195]}[section]
    assert entries[code]['source_review']['pdf_pages']==pages
    assert entries[code]['history']
assert F(121-100,100)==F(21,100) and F(5-4,4)==F(1,4)
assert 10*1200==12000 and F(24000,1200)==20 and 12000*F(101,100)==12120
tax=lambda x:F(x,10) if x<=100 else 10+F(x-100,5)
assert tax(100)==10 and tax(150)==20 and tax(150)/150==F(2,15)
assert 100+2*10==120 and 100*F(11,10)**2==121 and 121/F(11,10)**2==100
end=sum(10/F(11,10)**k for k in (1,2,3));early=sum(10/F(11,10)**k for k in (0,1,2))
assert end*F(11,10)==early and sum(10 for k in range(3))==30
assert isclose(float(end),24.86851990984222)
for n in range(1,30):assert sum(F(10)*F(10,11)**k for k in range(1,n+1))==100*(1-F(10,11)**n)
assert 3*33-100<0<3*34-100
assert 100-2*F(80,3)==20+F(80,3)==F(140,3)
for t in [F(0),F(6),F(40)]:
    ps=(80-2*t)/3;pb=(80+t)/3;q=(140-2*t)/3
    assert pb-ps==t and 100-2*pb==20+ps==q and min(ps,pb,q)>=0
assert F(68,3)+6==F(86,3) and 100-2*F(86,3)==F(128,3)
assert F(100+3-20,3)-F(100-20,3)==1
feasible=[(F(x,2),F(y,2)) for x,y in product(range(21),repeat=2) if x+2*y<=20]
assert max(3*x+4*y for x,y in feasible)==30
assert [(x,y) for x,y in feasible if 3*x+4*y==30]==[(10,0)]
mul=lambda A,B:[[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
assert mul([[4,2],[3,5]],[[10],[20]])==[[80],[130]]
A=[[2,1],[1,1]];inverse=[[1,-1],[-1,2]]
assert mul(A,inverse)==mul(inverse,A)==[[1,0],[0,1]]
assert mul(inverse,[[5],[3]])==[[2],[1]] and 1*4-2*2==0
polynomial_witnesses=0
for q,h in product(range(13),[F(1),F(1,2),F(-1,4)]):
    C=lambda z:z*z+10*z+100
    assert (C(q+h)-C(q))/h==2*q+h+10 and C(q+1)-C(q)==2*q+11
    assert -q*q+10*q-100==-(q-5)**2-75
    assert -q*q+20*q-30==70-(q-10)**2
    polynomial_witnesses+=1
assert max(-q*q+20*q-30 for q in range(13))==70
assert max(-q*q+20*q-30 for q in range(9))==66
elasticity=lambda p:F(-2)*p/(100-2*p)
assert elasticity(F(10))==F(-1,4) and elasticity(F(25))==-1
step=lambda z:int(z>=0);bits=list(product([0,1],repeat=2))
assert [step(x+y-F(3,2)) for x,y in bits]==[0,0,0,1]
assert [step(step(x+y-F(1,2))-step(x+y-F(3,2))-F(1,2)) for x,y in bits]==[0,1,1,0]
assert 100*60*60*24==8640000 and F(9,10)*F(95,100)+F(1,10)*F(1,2)==F(905,1000)
docs=[['cat','cat','sleep'],['cat','play'],['play','play']];vocab=['cat','sleep','play']
df=[sum(word in d for d in docs) for word in vocab]
assert df==[2,1,2] and [F(docs[0].count(w),df[i]) for i,w in enumerate(vocab)]==[1,1,0]
assert isclose(cosine_components([1,1],[2,0]),1/sqrt(2))
for u,v in [([0,0],[1,0]),([1],[1,0])]:
    try:cosine_components(u,v)
    except ValueError:pass
    else:raise AssertionError('invalid vectors accepted')
pixels=[[20,100,240],[0,180,255]]
assert [[min(255,v+30) for v in row] for row in pixels]==[[50,130,255],[30,210,255]]
assert [row[::-1] for row in pixels]==[[240,100,20],[255,180,0]]
assert [[min(255,2*v) for v in row] for row in pixels]==[[40,200,255],[0,255,255]] and F(90,9)==10
hamming=lambda u,v:sum(a!=b for a,b in zip(u,v))
assert hamming([1,0,0,0],[1,0,0,1])==1 and hamming([1,0,0,0],[0,1,1,0])==3
assert hamming([0,0,0,0],[1,0,0,1])==hamming([0,0,0,0],[0,1,1,0])==2
points=[(1,2),(2,3),(3,5)];best=F(23,14)
assert fit_origin([(F(x),F(y)) for x,y in points])==best
assert fit_affine([(F(x),F(y)) for x,y in points])==(F(3,2),F(1,3))
for a in [F(k,7) for k in range(-20,30)]:assert sum((a*x-y)**2 for x,y in points)==14*(a-best)**2+F(3,14)
assert loss(points,1)==6 and loss(points,2)==2
stable=descent(points,F(1,56),steps=6,start=F(0));large=descent(points,F(1,10),steps=6,start=F(0))
for rows,factor in [(stable,F(1,2)),(large,F(-9,5))]:
    for a,b in zip(rows,rows[1:]):assert b['coefficient']-best==factor*(a['coefficient']-best)
assert [row['coefficient'] for row in stable[:4]]==[0,F(23,28),F(69,56),F(161,112)]
assert all(a['loss']>b['loss'] for a,b in zip(stable,stable[1:]))
assert all(a['loss']<b['loss'] for a,b in zip(large,large[1:]))
with (root/'data/teaching_examples/model-ai-regression.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==3 and all(row['data_kind']=='fictional' for row in rows)
saved=read('data/economy_ai_teaching_results.json');actual=run(root/'data/teaching_examples/model-ai-regression.csv')
assert {k:v for k,v in saved.items() if k!='date'}==actual
raw=read('data/revisions_high.json')
for code in ['12인수02-03','12인수04-01','12인수04-03']:
    correction=raw[code]['scopeCorrections'][-1]
    assert correction['previous_record'] and correction['reason']
assert '내적' not in raw['12인수02-03']['mathematicalMeaning']
assert '조건부확률' not in raw['12인수04-01']['mathematicalMeaning']
assert '14a' in str(raw['12인수04-03']['taskSolution']) and '23/14' in str(raw['12인수04-03']['taskSolution'])
assert {c['visual']['kind'] for c in cohort if c.get('visual')}=={'matrix_product','image_matrix_panels','loss_descent'}
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
print(json.dumps(dict(status='pass',standards=33,goals=58,cases=40,scoped_goal_references=refs,polynomial_witnesses=polynomial_witnesses,visuals=3,checks='exact units and timing; boundary optima; matrices; truth tables; default IDF; pixel clipping; one-variable loss; GD contraction and divergence; scope history; acyclic goals')))

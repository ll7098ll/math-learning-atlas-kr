"""Independent function, distribution, chance and authored diagram witnesses."""
from pathlib import Path
from fractions import Fraction as F
from statistics import mean,median,multimode,quantiles
from itertools import product
from math import sqrt,isclose
import csv,json
from goal_hierarchy import load_goal_hierarchies

ROOT=Path(__file__).resolve().parents[1]
standards=json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={'9수02-'+str(i).zfill(2) for i in [5,6,7,14,15,16,17,18,21,22]}|{'9수04-'+str(i).zfill(2) for i in range(1,10)}
selected={code:e for code,e in entries.items() if code in codes}
selected_cases=[case for case in cases if case['standard'] in codes]
by_case={case['id']:case for case in selected_cases}
assert len(selected)==19 and sum(len(e['goals']) for e in selected.values())==46 and len(selected_cases)==25
assert F(2,2)==1 and (2,-1)!=(-1,2)  # Coordinate value 2 is one cell when each cell is 2 units.
assert [2*t if t<=3 else 6 for t in range(6)]==[0,2,4,6,6,6]
assert [3*x for x in [-2,-1,0,1,2]]==[-6,-3,0,3,6]
assert [F(12,x) for x in [-6,-3,-2,-1,1,2,3,6]]==[-2,-4,-6,-12,12,6,4,2]
assert F(12,2)*2==F(12,4)*4==12 and F(12,4)==F(12,2)/2
assert 1*(12-1)!=2*(12-2)
assert {1:2,2:2,3:4}[1]=={1:2,2:2,3:4}[2]
assert len({2,3})!=1
assert [x*x+1 for x in [-2,0,2]]==[5,1,5]
assert [2*x+3 for x in [-1,0,1,2]]==[1,3,5,7]
assert F(5-3,1-0)==2 and 2*F(-3,2)+3==0 and 2*0+3==3
assert 2*4+3==11 and F(11-3,4)==2!=F(11,4)
assert [(x,6-2*x) for x in range(4)]==[(0,6),(1,4),(2,2),(3,0)]
assert 2*1+5!=6
assert 2+1==-2+5==3
assert [x+3-(x+1) for x in range(-5,6)]==[2]*11
assert 2*(3)==2*2+2
function_witnesses=0
for x in [F(n,4) for n in range(-80,81)]:
    assert (2*x+3)-(2*x-1)==4
    assert (2*x+(6-2*x)==6)
    assert (x+1==-x+5)==(x==2)
    assert 2*(x+1)==2*x+2
    assert (x+1)**2-x*x==2*x+1
    assert 2*x*x-4*x-1==2*(x-1)**2-3
    assert 2*(x-1)**2-3>=-3 and -2*(x-1)**2-3<=-3
    if x:assert x*F(12)/x==12 and (F(12)/x)*x==12
    function_witnesses+=1
assert [2*(x-1)**2-3 for x in [-1,0,1,2,3]]==[5,-1,-3,-1,5]
assert [-2*(x-1)**2-3 for x in [-1,0,1,2,3]]==[-11,-5,-3,-5,-11]
assert 2*(100-1)**2-3>5 and -2*(100-1)**2-3<-11
visual=by_case['early-9수02-18-intersection']['visual']
assert visual['kind']=='linear_intersection' and visual['intersection']==[2,3]
assert visual['x_range']==[-1,5] and visual['y_range']==[-1,7]
for line in visual['lines']:
    assert line['slope']*visual['intersection'][0]+line['intercept']==visual['intersection'][1]
    assert all(visual['y_range'][0]<=line['slope']*x+line['intercept']<=visual['y_range'][1] for x in visual['x_range'])

values=[1,2,2,3,20]
assert F(sum(values),len(values))==F('5.6') and median(values)==2 and multimode(values)==[2]
assert median([1,2,3,20])==F(5,2) and multimode([1,1,2,2,3])==[1,2]
assert mean([1,2,2,3,200])==41.6 and median([1,2,2,3,200])==2
times=[5,8,10,12,14,15,18,21,25,27]
def histogram(values):return [sum(lo<=v<hi for v in values) for lo,hi in [(0,10),(10,20),(20,30)]]
assert histogram(times)==[2,5,3] and sum(histogram(times))==10
assert {stem:[v%10 for v in times if v//10==stem] for stem in range(3)}=={0:[5,8],1:[0,2,4,5,8],2:[1,5,7]}
assert [5,15,25]==[(a+b)/2 for a,b in [(0,10),(10,20),(20,30)]]
assert histogram([13 if v==12 else v for v in times])==histogram(times)
assert [F(n,20) for n in [4,8,8]]==[F('0.2'),F('0.4'),F('0.4')]
assert [F(n,50) for n in [10,15,25]]==[F('0.2'),F('0.3'),F('0.5')]
assert 15>8 and F(8,20)>F(15,50) and F(8,20)-F(15,50)==F('0.1')
example_dir=ROOT/'data/teaching_examples'
commute=list(csv.DictReader((example_dir/'middle-commute.csv').open(encoding='utf-8',newline='')))
assert len(commute)==8 and len({row['synthetic_id'] for row in commute})==8
groups={g:[int(row['minutes']) for row in commute if row['group']==g] for g in ['walk','bus']}
assert groups=={'walk':[8,10,12,14],'bus':[15,20,20,25]}
assert [(mean(v),median(v)) for v in groups.values()]==[(11,11),(20,20)]
outfits=set(product('ABC',[1,2]))
assert len(outfits)==6 and len(outfits-{('C',2)})==5
assert len(set('ABC')|{1,2})==5
assert {2,4,6}|{4,5,6}=={2,4,5,6}
die=set(range(1,7));even={2,4,6};odd=die-even
assert F(len(even),len(die))==F(len(odd),len(die))==F(1,2)
assert F(8,12)==F(2,3)!=F(1,2)
assert F(len({1,2}),6)==F(1,3) and F(len(even|{4,5,6}),6)==F(2,3)
assert len(list(product(['H','T'],repeat=2)))==4 and F(1,4)==F(1,2)**2

def variance(data):
    avg=F(sum(data),len(data))
    return sum((F(v)-avg)**2 for v in data)/len(data)
assert variance([2,4,6])==F(8,3) and variance([0,4,8])==F(32,3)
assert isclose(sqrt(F(8,3)),1.632993161855452) and isclose(sqrt(F(32,3)),3.265986323710904)
variance_witnesses=0
for data in product(range(-2,3),repeat=3):
    assert variance([v+10 for v in data])==variance(data)
    assert variance([2*v for v in data])==4*variance(data)
    assert sum(F(v)-F(sum(data),len(data)) for v in data)==0
    variance_witnesses+=1
box=by_case['early-9수04-08-boxplots']['visual']
assert box['kind']=='boxplots' and box['range']==[0,10]
box_rows=list(csv.DictReader((example_dir/'middle-boxplots.csv').open(encoding='utf-8',newline='')))
assert len(box_rows)==18
for g in box['groups']:
    data=g['values']
    expected=[min(data),quantiles(data,n=4,method='exclusive')[0],median(data),quantiles(data,n=4,method='exclusive')[2],max(data)]
    assert g['five_numbers']==expected
    assert [int(row['minutes']) for row in box_rows if row['synthetic_group']==g['label']]==data
    assert box['range'][0]<=min(data)<=max(data)<=box['range'][1]
assert box['groups'][0]['five_numbers']==[1,2.5,5,7.5,9]
assert box['groups'][1]['five_numbers']==[3,4,5,6,7]
quartile_witnesses=0
for n in range(5,22,2):
    data=list(range(1,n+1));mid=n//2
    assert median(data[:mid])==quantiles(data,n=4,method='exclusive')[0]
    assert median(data[mid+1:])==quantiles(data,n=4,method='exclusive')[2]
    quartile_witnesses+=1
def centered_product(pairs):
    xm=F(sum(x for x,y in pairs),len(pairs));ym=F(sum(y for x,y in pairs),len(pairs))
    return sum((x-xm)*(y-ym) for x,y in pairs)
assert centered_product([(1,2),(2,4),(3,5),(4,7),(5,8)])>0
assert centered_product([(1,8),(2,7),(3,5),(4,4),(5,2)])<0
u=[(-2,4),(-1,1),(0,0),(1,1),(2,4)]
assert centered_product(u)==0 and all(y==x*x for x,y in u)

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
    for target in graph[node]:visit(target)
    active.remove(node);done.add(node)
for goal in graph:visit(goal)
assert '9수02-18:relation' in graph['9수02-13:solve']
assert '9수02-13:solve' not in graph['9수02-18:relation']
assert all(s.get('goal_id')!='9수02-14:concept' for case in selected_cases if case['standard']=='9수02-07' for r in case['routes'] for s in r['condition_sources'])
assert all(s.get('goal_id')!='9수04-07:variance' for r in by_case['early-9수04-08-boxplots']['routes'] for s in r['condition_sources'])
assert all('9수04-04:plan' not in graph[g] for g in ['9수04-01:choose','9수04-02:histogram'])
assert all(s.get('goal_id')!='9수02-15:graph' for r in by_case['early-9수04-09-scatter']['routes'] for s in r['condition_sources'])
assert all(e['source_review']['pdf_pages']==([46,47,48] if code.startswith('9수04-') else [40,41,42,43]) for code,e in selected.items())
assert all(e['history'] for e in selected.values())
for case in selected_cases:
    for resource in case.get('resources',[]):
        assert '가상' in resource['label'] and (example_dir/Path(resource['path']).name).is_file()
def result(case_id,fragment):assert all(fragment in r['result'].replace(' ','') for r in by_case['early-'+case_id]['routes'])
for case_id,fragment in [('9수02-18-intersection','(2,3)'),('9수02-22-parabolas','−3'),('9수04-05-product','5가지'),('9수04-08-boxplots','5분')]:result(case_id,fragment)
print(json.dumps(dict(status='pass',standards=19,goals=46,cases=25,scoped_goal_references=refs,sibling_condition_references=siblings,function_witnesses=function_witnesses,variance_witnesses=variance_witnesses,quartile_witnesses=quartile_witnesses,commute_csv_rows=len(commute),boxplot_csv_rows=len(box_rows),checks='domains and representations; exact line intersection; full-real quadratic bounds; histogram boundaries; relative frequency; exhaustive small outcomes; spread units; explicit quartile method; paired-data trends; CSV/visual agreement; scoped acyclic references')))

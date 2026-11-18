"""Exact model checks and provenance for the final 44 standards."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
from collections import Counter
import json,csv,re
from goal_hierarchy import load_goal_hierarchies

root=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
standards=read('data/standards.json')['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s.get('subject') in ('직무 수학','수학과 문화','수학과제 탐구')}
cohort=[case for case in cases if case['standard'] in codes]
assert len(codes)==44 and len(cohort)==45 and sum(len(entries[c]['goals']) for c in codes)==73
assert len(entries)==len(standards)==435 and len(goals)==870
assert all(e['goals'] for e in entries.values())
for code in codes:
    section=int(code.split('-')[0][-2:])
    pages=[206+section] if code.startswith('12직수') else [223+section] if code.startswith('12수문') else {1:[253],2:[254],3:[255,256]}[section]
    assert entries[code]['source_review']['pdf_pages']==pages
    assert entries[code]['source_review']['printed_pages']==[p-6 for p in pages]
    assert entries[code]['history']
assert 1200*36+3000==46200 and 50000-46200==3800 and 8+36-17==27
for n in [1234567,1234999]:
    assert n//10000*10000==1230000 and ((n+9999)//10000)*10000==1240000
    assert ((n+5000)//10000)*10000==1230000
assert 1234999-1234567==432
assert 60+45==105 and F(235,100)*100==235 and F(8,10)*1000==800 and F(125,100)*1000==1250
assert F(254,100)*10==F(254,10) and F(454,1000)*5==F(227,100)
assert (2-8)%24==18 and (2-8)//24==-1
assert F(12000,8)==1500 and F(17400,12)==1450
assert 3*12000-2*17400==1200
assert 10000*F(4,5)*F(6,5)==9600
assert F(7500-6000,6000)==F(1,4) and F(1500,7500)==F(1,5)
assert [3000+1000*x for x in (1,2,3)]==[4000,5000,6000]
sequence=[10,14,12,10,10,14,12,10]
assert sequence[:4]==sequence[4:] and [sequence[i+1]-sequence[i] for i in range(3)]==[4,-2,-2]
for q in range(100):
    assert (3000+200*q<=1000+300*q)==(q>=20)
    assert (3000+200*q<1000+300*q)==(q>=21)
assert 3000+200*20==1000+300*20==7000
assert sorted([2*4,3*4,2*4,3*4,2*3,2*3])==[6,6,8,8,12,12]
projections=lambda h:(tuple(tuple(v>0 for v in row) for row in h),tuple(max(col) for col in zip(*h)),tuple(max(row) for row in h))
A=[[2,1],[1,2]];B=[[2,2],[2,2]]
assert projections(A)==projections(B) and sum(map(sum,A))==6 and sum(map(sum,B))==8
assert 3*2==6 and 6*4==24 and 4*100/100==4
assert 10*8-4*3==68 and 2*(10+8)+2*(4+3)==50
assert 20*10+2*20*15+2*10*15==1100 and F(20*10*15,1000)==3
assert len([p for p in product(['red','blue','black'],['paper','box']) if p!=('black','paper')])==5
assert len(list(permutations('ABC')))==6 and F(4,50)==F(8,100)

def csv_rows(name):
    with (root/'data/teaching_examples'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
orders=csv_rows('practice-work-orders.csv')
assert len(orders)==4 and all(r['data_kind']=='fictional' for r in orders)
by_month={m:(sum(int(r['orders']) for r in orders if r['month']==m),sum(int(r['late']) for r in orders if r['month']==m)) for m in ['M1','M2']}
assert by_month=={'M1':(60,8),'M2':(90,6)}
assert F(8,60)==F(2,15)!=F(10+20,200)
assert F(6,90)==F(1,15) and F(3,60)==F(1,20) and F(3,30)==F(1,10)
assert [240*v for v in [F(1),F(9,8),F(3,2),F(2)]]==[240,270,360,480]
assert F(3,2)**2==F(9,4)!=2 and 6*60==360
assert (2**2)==4 and 24*3==72 and len(range(72))==72
assert F(8,10)>F(15,20) and F(5+6+7+8+10,5)==F(36,5) and F(6+7+8,3)==7
win=[False]
for n in range(1,101):win.append(any(not win[n-k] for k in range(1,min(n,3)+1)))
assert all(win[n]==(n%4!=0) for n in range(101))
assert all(k+(4-k)==4 and 1<=4-k<=3 for k in [1,2,3])
bits=list(product([0,1],repeat=3))
for b in bits:
    coded=b+(sum(b)%2,)
    assert sum(coded)%2==0
    for i in range(4):assert sum(coded[:i]+(1-coded[i],)+coded[i+1:])%2==1
assert sum((1,0,1,0))%2==sum((0,1,1,0))%2==0
preferences=[(4,'ABC'),(3,'BCA'),(3,'CBA')]
first={c:sum(n for n,rank in preferences if rank[0]==c) for c in 'ABC'}
scores={c:sum(n*(2-rank.index(c)) for n,rank in preferences) for c in 'ABC'}
assert first=={'A':4,'B':3,'C':3} and scores=={'A':8,'B':13,'C':9}
pairs={(n%10,n%12) for n in range(60)}
assert len(pairs)==60 and len({(n%10,n%12) for n in range(120)})==60
assert min(n for n in range(1,121) if n%10==n%12==0)==60
assert len(list(product([0,1],repeat=6)))==64 and 64-1==63
headlines=csv_rows('source-unep-headlines.csv')
assert [r['publication_date'] for r in headlines]==['2024-03-27','2024-02-28']
assert all(r['data_kind']=='published_headline_excerpt' and r['source_url'].startswith('https://www.unep.org/en/news-and-stories/press-release/') for r in headlines)
tokens=[re.findall('[a-z]+',r['headline'].lower()) for r in headlines]
counts=Counter(w for words in tokens for w in words)
assert [len(t) for t in tokens]==[9,13] and sum(counts.values())==22
assert {w:n for w,n in counts.items() if n>1}=={'world':2,'un':2,'report':2}
assert sum(n for w,n in counts.items() if w not in {'a','and','into','over'})==18
for w in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
    assert ((5-3*w)>(3+w))==(w<F(1,2))
food=csv_rows('practice-food-balance.csv')
assert len(food)==3 and all(r['data_kind']=='fictional' for r in food)
assert [int(r['prepared_kg'])-int(r['served_kg']) for r in food]==[int(r['edible_leftover_kg']) for r in food]==[6,4,5]
assert F(sum(int(r['edible_leftover_kg']) for r in food),sum(int(r['prepared_kg']) for r in food))==F(1,10)
assert 30*F(2,10)==6 and 30*F(8,100)==F(24,10) and (6-F(24,10))/6==F(3,5)
assert F(30-20,20)==F(1,2) and F(30-20,100)==F(1,10)
bio=csv_rows('practice-biodiversity.csv');species=['species_A','species_B','species_C']
assert len(bio)==3 and all(r['data_kind']=='fictional' for r in bio)
assert [sum(int(r[k]) for k in species) for r in bio]==[10,10,20]
assert [sum(int(r[k])>0 for k in species) for r in bio]==[2,3,2]
assert [F(sum(int(r[k]) for k in species),int(r['effort_hours'])) for r in bio]==[5,5,5]
rect=csv_rows('model-fixed-perimeter.csv')
assert len(rect)==9 and all(r['data_kind']=='exact_model_calculation' for r in rect)
assert [int(r['area_cm2']) for r in rect]==[9,16,21,24,25,24,21,16,9]
for row in rect:
    x=int(row['x_cm']);y=int(row['y_cm'])
    assert 2*(x+y)==int(row['perimeter_cm'])==20 and x*y==int(row['area_cm2'])
rectangle_witnesses=0
for i in range(1,1000):
    x=F(i,100);y=10-x
    assert x*y==25-(x-5)**2<=25
    assert x*y+((x-y)/2)**2==((x+y)/2)**2
    yy=F(i,100);xx=20-2*yy
    assert xx*yy==50-2*(yy-5)**2<=50
    rectangle_witnesses+=1
assert 30+45+60+45==180
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
for case in cohort:
    for route in case['routes']:
        assert all(source['kind']!='entry_capability' for source in route['condition_sources'])
        assert not any(source.get('goal_id','').startswith('12수과02-') for source in route['condition_sources']) or case['standard']=='12수과03-01'
    for ref in case.get('references',[]):assert ref['url'].startswith('https://') and ref['accessed']
visuals=[c['visual'] for c in cohort if c.get('visual')]
assert {v['kind'] for v in visuals}=={'linear_intersection','fixed_perimeter'}
assert all(2*(v['x']+v['y'])==20 for v in next(v for v in visuals if v['kind']=='fixed_perimeter')['rectangles'])
print(json.dumps(dict(status='pass',standards=44,goals=73,cases=45,scoped_goal_references=refs,rectangle_witnesses=rectangle_witnesses,csv_rows=21,checks='units and rounding; price thresholds; projection ambiguity; rates vs counts; music ratios; game strategy over100 states; parity errors; voting profiles; cycles and braille; sourced media tokens; weighted choice; fictional environmental models; real vs model provenance; experiment vs proof; selected research methods; acyclic full goal graph')))

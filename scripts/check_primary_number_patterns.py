"""Independent arithmetic witnesses for the authored years 3–4 number goals."""
from fractions import Fraction as F
import json
from pathlib import Path
from goal_hierarchy import load_goal_hierarchies

ROOT=Path(__file__).resolve().parents[1]
standards=json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s['code'].startswith(('4수01-','4수02-'))}
selected={code:e for code,e in entries.items() if code in codes}
selected_cases=[case for case in cases if case['standard'] in codes]
by_case={case['id']:case for case in selected_cases}
assert len(selected)==19 and sum(len(e['goals']) for e in selected.values())==43 and len(selected_cases)==34

assert 3*10000+50==30050
assert 3*100000000+502*10000+7==305020007
assert 99999+1==100000 and 100000+1==100001
assert [98000+1000*i for i in (1,2,3)]==[99000,100000,101000]
assert 205030<205300 and 99999<100000
assert 785+678==1463 and 402-178==402-200+22==224
assert 24*3==72 and 236*4==944 and 236+236+236+236==944
assert 324*0==0 and 324*1==324 and divmod(0,3)==(0,0)
assert 24*13==240+72==312 and 236*24==4720+944==5664
assert 12//3==4 and 3*4==4*3==12
assert divmod(84,4)==(21,0) and divmod(85,4)==(21,1)
assert divmod(304,3)==(101,1) and 3*11+1!=304
assert divmod(84,12)==(7,0) and divmod(347,15)==(23,2)
assert 15*22+17==347 and 17>=15  # Reconstruction alone does not validate a remainder.
assert 198+304==502 and 602-297==305 and 49*21==1029
assert 8*49<=398<8*50 and divmod(398,8)==(49,6)

# Finite stated natural-number domains, independently of the Korean written steps.
additions=subtractions=0
for x in range(100,1000):
    hx,tux=divmod(x,100);tx,ux=divmod(tux,10)
    for y in range(100,1000):
        hy,tuy=divmod(y,100);ty,uy=divmod(tuy,10)
        cu,u=divmod(ux+uy,10);ct,t=divmod(tx+ty+cu,10);k,h=divmod(hx+hy+ct,10)
        assert 1000*k+100*h+10*t+u==x+y
        additions+=1
        if x>=y:
            borrow_u=int(ux<uy);borrow_t=int(tx-borrow_u<ty)
            assert 100*(hx-hy-borrow_t)+10*(tx-borrow_u+10*borrow_t-ty)+(ux+10*borrow_u-uy)==x-y
            subtractions+=1
multiplications=divisions=0
for x in range(10,1000):
    for y in range(100):
        tens,ones=divmod(y,10)
        assert x*y==x*(10*tens)+x*ones
        multiplications+=1
        if y:
            q,rem=divmod(x,y)
            assert y*q+rem==x and 0<=rem<y
            divisions+=1

assert F(15,20)==F(3,4) and F(1,5)<1 and F(5,5)==1 and F(7,5)>1
assert F(7,5)==1+F(2,5) and 2+F(2,5)==F(12,5)
assert F(3,7)<F(5,7) and F(1,3)>F(1,5)
assert F('0.3')==F(3,10) and F('1.3')==1+F(3,10)
assert F('0.27')==2*F(1,10)+7*F(1,100)
assert F('1.04')==1+4*F(1,100) and F('1.04')!=F('1.4')
assert F('0.205')==2*F(1,10)+5*F(1,1000) and F('0.205')!=F('0.25')
assert F('1.030')==F('1.03')>F('1.003') and F('0.9')>F('0.12') and F('0.4')==F('0.40')
assert F(2,5)+F(4,5)==1+F(1,5) and 2+F(1,5)-F(3,5)==1+F(3,5)
assert F('1.27')+F('0.86')==F('2.13') and F('1.2')+F('0.35')==F('1.55')
assert F('2.04')-F('0.87')==F('1.17') and F('1.2')-F('0.35')==F('0.85')
fraction_pairs=0
for d in range(2,21):
    for x in range(1,3*d+1):
        for y in range(1,3*d+1):
            assert F(x,d)+F(y,d)==F(x+y,d)
            if x>=y:assert F(x,d)-F(y,d)==F(x-y,d)
            assert (F(x,d)<F(y,d))==(x<y)
            fraction_pairs+=1
    for e in range(2,21):assert (F(1,d)<F(1,e))==(d>e)
assert [4+3*i for i in range(5)]==[4,7,10,13,16]
assert [12*i for i in range(1,5)]==[12,24,36,48]
assert 27+15==30+12==42 and 17+14==12+19==31

# Goal references are explicitly scoped to target goals in the named route.
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
    assert node not in active,'Review conditional reference cycle: '+node
    if node in done:return
    active.add(node)
    for following in graph[node]:visit(following)
    active.remove(node);done.add(node)
for goal in graph:visit(goal)
assert '4수01-05:share' not in graph['2수01-10:groups']
assert '4수01-08:add' not in graph['4수01-03:add']
assert '4수02-02:find' not in graph['4수01-04:single']
assert '4수01-01:need' not in graph['2수01-02:place']
assert '4수01-09:need' not in graph['2수03-10:measure']
share=by_case['early-4수01-05-share']
inverse_source=next(s for s in share['routes'][0]['condition_sources'] if s.get('goal_id')=='2수01-10:groups')
assert inverse_source['applies_to_goal_ids']==['4수01-05:inverse']
fraction_case=by_case['early-4수01-09-fraction']
assert len(fraction_case['routes'])==2
assert all(s.get('goal_id')!='2수03-10:measure' for s in fraction_case['routes'][0]['condition_sources'])
assert all(e['source_review']['pdf_pages'] in ([23,24,25],[25,26]) for e in selected.values())
assert all(e['history'] for e in selected.values())
def result(case_id,fragment):
    assert all(fragment in r['result'].replace(' ','') for r in by_case[case_id]['routes'])
result('early-4수01-03-add','1463');result('early-4수01-03-subtract','224')
result('early-4수01-04-single','944');result('early-4수01-04-double','5664')
result('early-4수01-06-zero','101');result('early-4수01-07-double','23')
result('early-4수01-15-add','6/5');result('early-4수01-16-subtract','1.17')
print(json.dumps(dict(status='pass',standards=19,goals=43,cases=34,scoped_goal_references=refs,natural_addition_checks=additions,natural_subtraction_checks=subtractions,multiplication_checks=multiplications,division_checks=divisions,fraction_pairs=fraction_pairs,checks='curriculum number ranges; worked examples; quotient/remainder and zero boundaries; exact fraction and decimal arithmetic; distinct goal scopes; source-reference integrity')))

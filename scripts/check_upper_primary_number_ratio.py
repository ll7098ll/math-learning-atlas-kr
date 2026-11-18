"""Arithmetic witnesses and scope regressions for years 5–6 number and ratio."""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json
from goal_hierarchy import load_goal_hierarchies

ROOT=Path(__file__).resolve().parents[1]
standards=json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s['code'].startswith(('6수01-','6수02-'))}
selected={code:e for code,e in entries.items() if code in codes}
selected_cases=[case for case in cases if case['standard'] in codes]
by_case={case['id']:case for case in selected_cases}
assert len(selected)==20 and sum(len(e['goals']) for e in selected.values())==49 and len(selected_cases)==33

assert 24//6*2+5==13 and 24//(6*2)+5==7
assert [x for x in [119,120,149,F('149.5'),150] if 120<=x<150]==[120,149,F('149.5')]
def up(n,unit):return ((n+unit-1)//unit)*unit
def down(n,unit):return n//unit*unit
def nearest(n,unit):return ((2*n+unit)//(2*unit))*unit
assert (up(237,10),down(237,10),nearest(237,10))==(240,230,240)
assert (up(230,10),down(230,10),nearest(230,10))==(230,230,230)
assert nearest(235,10)==240
assert up(237,10)//10==24 and divmod(237,10)==(23,7)
rounding_witnesses=0
for unit in [10,100,1000]:
    for n in range(10001):
        lo,hi,near=down(n,unit),up(n,unit),nearest(n,unit)
        assert lo<=n<=hi and all(v%unit==0 for v in [lo,hi,near])
        assert hi-lo in [0,unit]
        assert 2*abs(near-n)<=unit
        if n%unit==0:assert lo==hi==near==n
        if 2*(n%unit)==unit:assert near==hi
        rounding_witnesses+=1

def divisors(n):return [k for k in range(1,n+1) if n%k==0]
assert divisors(12)==[1,2,3,4,6,12] and divisors(18)==[1,2,3,6,9,18]
assert sorted(set(divisors(12))&set(divisors(18)))==[1,2,3,6] and gcd(12,18)==6
assert [4*k for k in range(1,7)]==[4,8,12,16,20,24]
assert [6*k for k in range(1,5)]==[6,12,18,24] and lcm(4,6)==12
divisor_pairs=0
for x in range(1,41):
    for y in range(1,41):
        common=sorted(set(divisors(x))&set(divisors(y)))
        assert common and common[-1]==gcd(x,y)
        # Listing each positive multiple set to their guaranteed common product.
        common_multiples=set(range(x,x*y+1,x))&set(range(y,x*y+1,y))
        assert min(common_multiples)==lcm(x,y)
        assert (x%y==0)==(x in range(y,x*y+1,y))
        divisor_pairs+=1

assert F(2,3)==F(4,6) and F(2,3)!=F(3,4)
assert F(12,18)==F(6,9)==F(2,3)
assert F(2,3)==F(8,12)==F(16,24) and F(3,4)==F(9,12)==F(18,24)
assert F(3,8)==F(9,24)<F(1,2)<F(2,3)==F(16,24)
assert F(2,3)+F(3,4)==F(17,12)==1+F(5,12)
assert 1+F(1,2)+F(2,3)==F(13,6)==2+F(1,6)
assert 2+F(1,4)-F(5,6)==F(17,12)==1+F(5,12)
assert F(2,5)*3==3*F(2,5)==F(6,5)
assert F(2,3)*F(3,4)==F(6,12)==F(1,2)
assert (1+F(1,2))*F(2,3)==F(3,2)*F(2,3)==F(2,3)+F(1,3)==1
assert F(3,2)*2==3 and F(5,2)*2==5 and F(4,2)==2
assert F(3,4)/2==F(3,8)
assert 2/F(3,4)==F(8,3)==2+F(2,3)
assert 2-2*F(3,4)==F(1,2) and F(1,2)/F(3,4)==F(2,3)
assert F(5,6)/F(2,3)==F(5,4)==F(5,6)*F(3,2)
assert F(3,2)/F(3,4)==2
fraction_witnesses=0
for b in range(1,13):
    for d in range(1,13):
        common=b*d  # Valid without requiring the least common multiple.
        for a_ in range(1,9):
            for c_ in range(1,9):
                left,right=F(a_,b),F(c_,d)
                assert (left<right)==(a_*d<c_*b)
                assert left+right==F(a_*d+c_*b,common)
                if left>=right:assert left-right==F(a_*d-c_*b,common)
                assert left*right==F(a_*c_,b*d)
                assert left/right==F(a_*d,b*c_)
                assert left/right==F(a_*d,common)/F(c_*b,common)
                fraction_witnesses+=1

assert F(3,4)==F('0.75') and F(1,8)==F('0.125')
assert F('0.7')==F(14,20)<F(15,20)==F(3,4)
assert F('0.24')*3==3*F('0.24')==F('0.72')
assert F('1.2')*F('0.4')==F('0.48')<F('1.2')
assert F('0.06')*F('0.3')==F('0.018')
assert F(3,4)==F('0.75') and F(7,2)==F('3.5')
assert F('0.84')/4==F('0.21')
assert 3/F('0.4')==F('7.5') and 3-7*F('0.4')==F('0.2')
assert F('1.26')/F('0.3')==F('0.126')/F('0.03')==F('12.6')/3==F('4.2')
decimal_witnesses=0
for left_scale in [10,100,1000]:
    for right_scale in [10,100,1000]:
        for x in range(1,31):
            for y in range(1,21):
                left,right=F(x,left_scale),F(y,right_scale)
                assert left*right==F(x*y,left_scale*right_scale)
                factor=right_scale
                assert left/right==(left*factor)/(right*factor)
                assert left/right==F(x*right_scale,y*left_scale)
                decimal_witnesses+=1

assert [x*3 for x in [1,2,3,4,5]]==[3,6,9,12,15]
assert [x+3 for x in [1,2,3,4,5]]==[4,5,6,7,8]
assert F(4,1)!=F(5,2)  # An additive correspondence need not be proportional.
assert 3-2==5-4==1 and F(2,3)!=F(4,5)
assert F(15,20)==F(3,4)==F('0.75')==F(75,100)
assert F('0.75')/100!=F('0.75')
assert F(2,3)==F(8,12) and 2*12==3*8==24
assert F(3,5)==F(12,20) and 3*20==5*12==60
assert 30*F(2,5)==12 and 30*F(3,5)==18 and 12+18==30 and F(12,18)==F(2,3)
allocation_witnesses=0
for p in range(1,13):
    for q in range(1,13):
        for unit in range(1,21):
            whole=unit*(p+q)
            first,second=whole*F(p,p+q),whole*F(q,p+q)
            assert first+second==whole and first/second==F(p,q)
            allocation_witnesses+=1

# References describe particular routes, rather than universal prerequisites.
graph={goal:set() for goal in goals};refs=siblings=0
for case in cases:
    for route in case['routes']:
        for source in route['condition_sources']:
            if case['standard'] in codes:
                assert source['applies_to_goal_ids'] and set(source['applies_to_goal_ids'])<=set(case['goal_ids'])
            if source['kind']=='goal':
                for target in source.get('applies_to_goal_ids',case['goal_ids']):graph[source['goal_id']].add(target)
                if case['standard'] in codes:
                    refs+=1
                    siblings+=source['goal_id'].split(':')[0]==case['standard']
active=set();done=set()
def visit(node):
    assert node not in active,'Review conditional reference cycle: '+node
    if node in done:return
    active.add(node)
    for following in graph[node]:visit(following)
    active.remove(node);done.add(node)
for goal in graph:visit(goal)
assert '6수01-06:common' not in graph['6수01-05:least']
assert '6수01-06:reduce' not in graph['6수01-04:greatest']
assert all(s.get('goal_id')!='6수01-06:common' for s in by_case['early-6수01-07-compare']['routes'][1]['condition_sources'])
assert all(s.get('goal_id')!='6수01-10:quotient' for s in by_case['early-6수01-14-decimal-quotient']['routes'][0]['condition_sources'])
assert all(s.get('goal_id')!='6수02-04:property' for s in by_case['early-6수02-04-solve']['routes'][0]['condition_sources'])
assert all(s.get('goal_id')!='6수02-04:solve' for route in by_case['early-6수02-05-allocate']['routes'] for s in route['condition_sources'])
rate=by_case['early-6수02-03-rate']
hundredths=next(s for s in rate['routes'][0]['condition_sources'] if s.get('goal_id')=='4수01-13:hundredths')
assert hundredths['applies_to_goal_ids']==['6수02-03:decimal']
assert all(e['source_review']['pdf_pages']==([33,34] if code.startswith('6수02-') else [31,32,33]) for code,e in selected.items())
assert all(e['history'] for e in selected.values())

def result(case_id,fragment):
    assert all(fragment in route['result'].replace(' ','') for route in by_case['early-'+case_id]['routes'])
for case_id,fragment in [('6수01-01-order','13'),('6수01-04-factors','6'),('6수01-05-multiples','12'),('6수01-07-compare','3/8<2/3'),('6수01-08-subtract','17/12'),('6수01-09-mixed','1m'),('6수01-11-fraction-by-fraction','5/4'),('6수01-12-compare','0.7<3/4'),('6수01-14-decimal-quotient','0.75'),('6수01-15-decimal-by-decimal','4.2'),('6수02-04-solve','12'),('6수02-05-allocate','12')]:result(case_id,fragment)
print(json.dumps(dict(status='pass',standards=20,goals=49,cases=33,scoped_goal_references=refs,sibling_condition_references=siblings,rounding_witnesses=rounding_witnesses,divisor_pairs=divisor_pairs,fraction_witnesses=fraction_witnesses,decimal_witnesses=decimal_witnesses,allocation_witnesses=allocation_witnesses,checks='exact arithmetic and boundaries; listed gcd/lcm; fraction/decimal division units; ratio versus whole; scoped alternatives; reference cycles; curriculum scope')))

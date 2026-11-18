"""Enumerated probability and independent checks of teaching inference results."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations,combinations
from collections import Counter
from math import comb,sqrt,isclose,atan,pi
from statistics import mean,variance,median
import csv,json
from goal_hierarchy import load_goal_hierarchies
from statistical_tools import NORMAL,t_cdf,t_pdf,t_quantile,normal_pdf,mean_interval,proportion_interval,mean_test,run

root=Path(__file__).resolve().parents[1]
standards=json.loads((root/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={s['code'] for s in standards if s.get('subject') in ('확률과 통계','실용 통계')}
cohort=[case for case in cases if case['standard'] in codes]
assert len(codes)==29 and len(cohort)==33 and sum(len(entries[c]['goals']) for c in codes)==57
for code in codes:
    section=int(code.split('-')[0][-2:])
    expected=([133+section]+([137] if section==3 else [])) if code.startswith('12확통') else {1:[239],2:[240],3:[241],4:[241,242]}[section]
    assert entries[code]['source_review']['pdf_pages']==expected
    assert entries[code]['source_review']['printed_pages']==[page-6 for page in expected]
    assert entries[code]['review']['date']>='2026-11-04'
    assert entries[code]['history']
assert entries['12대수01-01']['review']['date']=='2026-10-30'
assert len(list(product('01',repeat=3)))==8
assert len(set(permutations('AAB')))==3
allocations=[v for v in product(range(6),repeat=3) if sum(v)==5]
assert len(allocations)==21 and sum(all(x>=1 for x in v) for v in allocations)==6
for n in range(0,10):
    coefficients=Counter(sum(bits) for bits in product([0,1],repeat=n))
    assert all(coefficients[k]==comb(n,k) for k in range(n+1))
    assert sum(coefficients.values())==2**n
assert comb(4,2)*2**2==24
U=set(range(1,7));A={2,4,6};B={3,6}
assert F(len(A|B),6)==F(len(A),6)+F(len(B),6)-F(len(A&B),6)==F(2,3)
assert F(8-1,8)==F(7,8)
assert F(10,40)==F(1,4) and F(10,30)==F(1,3)
assert 10+20+30+40==100
assert F(2,3)*F(1,2)==F(1,3)!=F(2,3)**2
draws=list(permutations(range(5),2))
assert F(sum(i<3 and j<3 for i,j in draws),len(draws))==F(3,10)
# Boundary audit: the joint event is defined at R=0; conditioning on the first
# red event is not. Enumerate ordered draws without evaluating that condition.
revision=json.loads((root/'data/revisions_high.json').read_text(encoding='utf-8'))['12확통02-06']
assert 'R=0' in revision['taskSolution'] and '조건부확률을 정의하지 않는다' in revision['taskSolution']
for total in range(2,12):
    outcomes=list(permutations(range(total),2))
    for red in range(total+1):
        joint=F(sum(i<red and j<red for i,j in outcomes),len(outcomes))
        assert joint==F(red*(red-1),total*(total-1))
        if red:
            assert joint==F(red,total)*F(red-1,total-1)
        else:
            assert not any(i<red for i,j in outcomes) and joint==0
coin_counts=Counter(sum(bits) for bits in product([0,1],repeat=2))
probabilities={k:F(v,4) for k,v in coin_counts.items()}
assert probabilities=={0:F(1,4),1:F(1,2),2:F(1,4)}
mu=sum(k*p for k,p in probabilities.items());var=sum((k-mu)**2*p for k,p in probabilities.items())
assert mu==1 and var==F(1,2)
binomial_witnesses=0
for n,p in product(range(1,13),[F(1,5),F(1,2),F(4,5)]):
    dist=[comb(n,k)*p**k*(1-p)**(n-k) for k in range(n+1)]
    assert sum(dist)==1
    assert sum(k*prob for k,prob in enumerate(dist))==n*p
    assert sum((k-n*p)**2*prob for k,prob in enumerate(dist))==n*p*(1-p)
    binomial_witnesses+=1
assert F(comb(5,2),2**5)==F(5,16)
assert isclose(NORMAL.cdf(1)-NORMAL.cdf(-1),0.6826894921370859)
exact=sum(F(comb(100,k),2**100) for k in range(45,56))
approx=NORMAL.cdf(1.1)-NORMAL.cdf(-1.1)
assert abs(float(exact)-approx)<0.003 and float(exact)!=approx
means=[F(x+y,2) for x,y in product([40,60],repeat=2)]
props=[F(x+y,2) for x,y in product([0,1],repeat=2)]
assert sum(means)/4==50 and sum((m-50)**2 for m in means)/4==50
assert sum(props)/4==F(1,2) and sum((p-F(1,2))**2 for p in props)/4==F(1,8)
assert F(1,2)*F(2,5)+F(1,3)*F(3,5)+F(1,6)*F(4,5)==F(8,15)
for start in range(1,11):
    selected=list(range(start,601,10));assert len(selected)==60 and len(set(selected))==60

# Cauchy and df=2 have independent closed-form t CDFs; df=8 has a
# polynomial in u=x/sqrt(8+x^2), obtained by integrating cos(theta)^7.
for x in [-8,-3,-1,-0.5,0,0.5,1,3,8]:
    assert isclose(t_cdf(x,1),0.5+atan(x)/pi,abs_tol=2e-10)
    assert isclose(t_cdf(x,2),0.5+x/(2*sqrt(x*x+2)),abs_tol=2e-10)
def t8(x):
    u=x/sqrt(8+x*x)
    return .5+35/32*(u-u**3+3*u**5/5-u**7/7)
for x in [-4,-2,0,1,3.273268353539886,4]:assert isclose(t_cdf(x,8),t8(x),abs_tol=2e-11)
assert isclose(t8(t_quantile(.975,8)),.975,abs_tol=2e-11)
assert abs(t_quantile(.975,9)-2.262)<.0005  # NIST published df=9 table precision.
assert t_quantile(.975,5)>t_quantile(.975,30)>NORMAL.inv_cdf(.975)
assert t_pdf(0,5)<normal_pdf(0) and t_pdf(4,5)>normal_pdf(4)
assert abs(t_pdf(0,30)-normal_pdf(0))<abs(t_pdf(0,5)-normal_pdf(0))

example=root/'data/teaching_examples'
with (example/'practice-refill-time.csv').open(encoding='utf-8',newline='') as f:time_rows=list(csv.DictReader(f))
with (example/'practice-preference.csv').open(encoding='utf-8',newline='') as f:response_rows=list(csv.DictReader(f))
assert len(time_rows)==9 and len(response_rows)==200
assert all(r['data_kind']=='fictional' for r in [*time_rows,*response_rows])
values=[int(r['seconds']) for r in time_rows]
assert mean(values)==median(values)==25 and variance(values)==21 and max(values)-min(values)==14
assert sum((x-25)**2 for x in values)==168
assert sum(int(r['reuse']) for r in response_rows)==120
assert sum(int(r['reuse']) for r in response_rows if r['cohort']=='A')==70
assert sum(int(r['reuse']) for r in response_rows if r['cohort']=='B')==50
assert mean([1,2,3,4,20])==6 and median([1,2,3,4,20])==3
assert mean(values[:-1])==F(193,8)
results=run(example/'practice-refill-time.csv',example/'practice-preference.csv')
saved=json.loads((root/'data/statistical_teaching_results.json').read_text(encoding='utf-8'))
assert {k:v for k,v in saved.items() if k!='date'}==results
known=results['mean_known_sigma6'];unknown=results['mean_unknown_sigma'];prop=results['proportion'];test=results['test_mu20']
assert isclose(known['lower'],25-2*NORMAL.inv_cdf(.975))
assert isclose(unknown['lower'],21.47752049918185,abs_tol=1e-8)
assert isclose(prop['lower'],0.5321048559554297) and prop['upper']>.6
assert isclose(test['statistic'],sqrt(F(75,7)))
assert isclose(test['p_value'],2*(1-t8(sqrt(F(75,7)))),abs_tol=2e-11)
assert .01<test['p_value']<.05 and unknown['lower']>20 and unknown['upper']<30
for call in [lambda:proportion_interval(0,5),lambda:proportion_interval(201,200),lambda:mean_interval([1]),lambda:mean_interval([1,2],known_sigma=0),lambda:mean_test([2,2,2],2),lambda:t_quantile(1,5)]:
    try:call()
    except ValueError:pass
    else:raise AssertionError('Invalid teaching model accepted')
for case in cohort:
    for reference in case.get('references',[]):
        assert reference['url'].startswith(('https://kosis.kr/','https://www.itl.nist.gov/','https://itl.nist.gov/'))
visuals={case['visual']['kind']:case['visual'] for case in cohort if case.get('visual')}
assert set(visuals)=={'statistics_summary','distribution_curves','binomial_normal'}
summary=visuals['statistics_summary'];assert sum(x['count'] for x in summary['categories'])==200
assert [sum(b['lower']<=x<b['upper'] for x in values) for b in summary['bins']]==[b['count'] for b in summary['bins']]==[1,3,3,2]
for curve in visuals['distribution_curves']['curves']:
    assert len(curve['points'])==161 and all(y>0 for x,y in curve['points'])
    assert all(isclose(curve['points'][i][1],curve['points'][-1-i][1]) for i in range(161))
for panel in visuals['binomial_normal']['panels']:
    assert panel['n'] in (10,30,100)
    assert len(panel['bins'])==panel['n']+1
    assert isclose(sum(b['height']*b['width'] for b in panel['bins']),1)
    assert isclose(sum(b['center']*b['height']*b['width'] for b in panel['bins']),0,abs_tol=1e-12)
with (example/'model-binomial.csv').open(encoding='utf-8',newline='') as f:model_rows=list(csv.DictReader(f))
with (example/'model-distribution-curves.csv').open(encoding='utf-8',newline='') as f:curve_rows=list(csv.DictReader(f))
assert len(model_rows)==143 and len(curve_rows)==161
assert all(r['data_kind']=='model_calculation' for r in [*model_rows,*curve_rows])
assert isclose(results['binomial100']['exact_45_to_55'],float(exact))
assert isclose(results['binomial100']['normal_with_correction'],approx)
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
print(json.dumps(dict(status='pass',standards=29,goals=57,cases=33,scoped_goal_references=refs,binomial_witnesses=binomial_witnesses,fictional_csv_rows=209,model_csv_rows=304,visuals=3,checks='enumerated counts; conditional denominators; independence vs disjointness; exact probability moments; normal approximation; sampling variability; closed-form t CDF checks; confidence and test interpretation; CSV provenance; graph bins and mass-preserving standardization; preserved review dates; acyclic goals')))

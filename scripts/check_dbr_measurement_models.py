"""Exact checks of own examples; no fabricated classroom measurements."""
from fractions import Fraction as F
from itertools import product
import json

def check():
 # A complete group answer can coexist with radically different individual knowledge.
 all_know=tuple((1,1,1,1) for _ in range(4))
 one_knows=((1,1,1,1),(0,0,0,0),(0,0,0,0),(0,0,0,0))
 group=lambda m:tuple(max(row[j] for row in m) for j in range(4))
 assert group(all_know)==group(one_knows)==(1,1,1,1)
 assert sum(map(sum,all_know))==16 and sum(map(sum,one_knows))==4
 # Check every feasible overlap of the reported two phase counts.
 a=set(range(33));unions=[]
 for overlap in range(11):
  b=set(range(overlap))|set(range(33,43-overlap))
  assert len(b)==10 and len(a&b)==overlap
  unions.append(len(a|b))
 assert set(unions)==set(range(33,44))
 assert F(3,20)==F(15,100)
 assert sum([100,30,20])==150 and F(100,150)==F(2,3)
 # Similarity gives a cubic volume factor; it does not identify growth over time.
 for k in [F(1,2),F(1),F(2),F(3)]:
  sides=(F(2),F(3),F(5));v=sides[0]*sides[1]*sides[2]
  assert (sides[0]*k)*(sides[1]*k)*(sides[2]*k)/v==k**3
 assert F(2)**3==8 and 8!=2
 # Algebraic identity and its equality condition, including noninteger inputs.
 for x in [F(n,10) for n in range(1,100)]:
  assert x*(10-x)==25-(x-5)**2<=25
  assert (x*(10-x)==25)==(x==5)
 # With simultaneous support/context changes, a single observed improvement
 # has at least two observationally indistinguishable explanations.
 outcomes=[a+b for a,b in [(2,0),(0,2)]]
 assert outcomes==[2,2]
 return dict(status='pass',unique_phase_union_bounds=[33,43],possible_overlaps=11,group_measurement_counterexamples=2,rectangle_rational_inputs=99,similarity_scales=4,reported_cost_partial_total=150,scope='Exact own model examples only;no student responses,causal effect or validated instrument.')

if __name__=='__main__':print(json.dumps(check()))

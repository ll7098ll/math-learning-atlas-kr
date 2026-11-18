"""Exact own examples; polynomial identities cover arbitrary n, not just samples."""
from fractions import Fraction as Q
from math import comb,prod
import json

def check():
 def pad(p,n):return list(p)+[Q(0)]*(n-len(p))
 def add(a,b):return [x+y for x,y in zip(pad(a,max(len(a),len(b))),pad(b,max(len(a),len(b))))]
 def shift(p):return [sum(p[k]*comb(k,j) for k in range(j,len(p))) for j in range(len(p))]
 # F(n)=n²(n+1)²/4, coefficients in ascending order.
 f=[Q(0),Q(0),Q(1,4),Q(1,2),Q(1,4)]
 diff=add(shift(f),[-x for x in f]);assert diff==[1,3,3,1,0]
 evaluate=lambda p,n:sum(a*Q(n)**k for k,a in enumerate(p))
 assert evaluate(f,1)==1
 # The exact coefficient identity proves F(n+1)-F(n)=(n+1)³ for every n.
 # Together with the n=1 base and the sum's recurrence, this is induction.
 assert add(shift(add(f,[1])),[-x for x in add(f,[1])])==diff
 assert evaluate(add(f,[1]),1)==2!=1 # a step alone does not prove the base
 false=lambda n:evaluate(f,n)+prod(n-k for k in range(1,7))
 assert all(false(n)==sum(k**3 for k in range(1,n+1)) for n in range(1,7))
 assert false(7)==1504 and sum(k**3 for k in range(1,8))==784
 # An arbitrary point Q on a directrix is not the perpendicular foot H.
 r=(Q(2),Q(0));focus=(Q(0),Q(1));q=(Q(0),Q(-1));foot=(Q(2),Q(-1))
 distance2=lambda a,b:sum((x-y)**2 for x,y in zip(a,b))
 assert distance2(r,focus)==distance2(r,q)==5 and distance2(r,foot)==1
 # Square-minus-rectangle = (a-b)²/4, including the equality case.
 for a,b in [(Q(3),Q(3)),(Q(2),Q(4))]:
  assert ((a+b)/2)**2-a*b==(a-b)**2/4
 assert Q(3)**2-Q(3)*3==0 and Q(3)**2-Q(2)*4==1
 assert 3*4==12 and 3**2+4**2+12**2==13**2
 # Source's exponential example, recovered with exact positive substitutions.
 zs={Q(5,2),Q(17,4)};ys={Q(1,4),Q(1,2),Q(2),Q(4)}
 assert {y+1/y for y in ys}==zs and all(z>=2 for z in zs)
 assert all(8*z*z-54*z+85==0 for z in zs)
 assert all(8*(y*y+1/y**2)-54*(y+1/y)+101==0 for y in ys)
 assert {Q(2)**x for x in [-2,-1,1,2]}==ys
 return dict(status='pass',own_exact_models=True,actual_student_data=False,
  induction_step='exact polynomial coefficient identity for arbitrary n',
  induction_base=1,step_only_offset_rejected=True,
  false_formula_first_six_matches=True,false_formula_at_seven=1504,correct_sum_at_seven=784,
  directrix_arbitrary_point_squared_distance=5,perpendicular_squared_distance=1,
  rectangle_equality_case=True,source_exponential_roots=[-2,-1,1,2],
  limit='Own coordinates/counterexamples and source-example arithmetic; not actual learner records, field validation, all-quadrilateral proof or verification of historical originals.')

if __name__=='__main__':print(json.dumps(check(),ensure_ascii=False))

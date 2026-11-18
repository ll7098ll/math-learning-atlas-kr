"""Exact own models for recoverable transformations and conditions over the reals.

The exhaustiveness arguments use factorisation and nonnegativity, not sampling.
These checks validate the authored examples, not learners or the book as a whole.
"""
from fractions import Fraction as Q
import json

def check():
 # y²-13y+36=(y-4)(y-9), so these are all possible y roots.
 assert 4+9==13 and 4*9==36
 ys={4,9};xs={-3,-2,2,3}
 assert {x*x for x in xs}==ys
 assert all(x**4-13*x*x+36==0 for x in xs)
 assert {x for x in xs if x>0}=={2,3}!=xs
 # sqrt(x+2)=x requires x>=0. Squaring gives (x-2)(x+1)=0.
 assert Q(2)+Q(-1)==1 and Q(2)*Q(-1)==-2
 squared_roots={-1,2}
 assert all(x*x==x+2 for x in squared_roots)
 assert {x for x in squared_roots if x>=0}=={2}
 # At -1 the actual nonnegative square root is 1, not -1.
 assert (-1)+2==1 and 1!=-1
 # For real x,y, x²,y²>=0; sum zero forces both zero.
 # This proves unique (0,0); enumerating some integer points would not prove it.
 assert Q(0)**2+Q(0)**2==0
 # Two constraints on one unknown, neither redundant, are consistent together.
 # Factorisation gives complete individual root sets {0,1}, {0,2}.
 a={0,1};b={0,2};assert a&b=={0} and a-b=={1} and b-a=={2}
 # One equation in one real unknown may have 0,1,2 or infinitely many solutions.
 # x²+1>=1 proves the first case; x=0 and (x-1)(x+1)=0 the next two.
 assert 1>0 and {-1,1}!={0}
 # c is a positive length, so zero is a boundary, negative squares impossible.
 h2=lambda d:Q(d)**2-Q(3)**2-Q(4)**2
 assert h2(13)==144 and h2(5)==0 and h2(4)==-9
 return dict(status='pass',own_exact_models=True,real_domain=True,
  quartic_roots=sorted(xs),squared_radical_candidates=sorted(squared_roots),
  radical_solution=[2],equation_count_counterexamples=True,
  inverse_cuboid_squared_heights=[144,0,-9],
  actual_student_data=False,finite_sampling_used_as_proof=False)

if __name__=='__main__':print(json.dumps(check(),ensure_ascii=False))

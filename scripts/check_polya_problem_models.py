"""Own exact counterexamples for conditions, verification and related rates."""
from fractions import Fraction as Q
from itertools import permutations
import json

def check():
 def true_square(a,b,c):return a*a+b*b+c*c
 def false_square(a,b,c):
  # Deliberately wrong: symmetric, homogeneous, positive, with correct zero-face limits.
  return true_square(a,b,c)+a*b*c/(a+b+c)
 a,b,c=Q(3),Q(4),Q(12)
 assert true_square(a,b,c)==169 and false_square(a,b,c)==Q(3355,19)!=169
 for v in permutations((a,b,c)):
  assert false_square(*v)==Q(3355,19)
  assert false_square(*(12*x for x in v))==144*false_square(*v)
 assert false_square(a,b,Q(0))==true_square(a,b,Q(0))==25
 # The three edge lengths alone do not specify a skew parallelepiped's diagonal.
 u=(Q(3),Q(0),Q(0));v=(Q(12,5),Q(16,5),Q(0));w=(Q(0),Q(0),Q(12))
 norm2=lambda x:sum(t*t for t in x)
 assert [norm2(x) for x in [u,v,w]]==[9,16,144]
 assert norm2(tuple(sum(z) for z in zip(u,v,w)))==Q(917,5)!=169
 direction=(Q(3,5),Q(4,5));assert norm2(direction)==1
 assert sum(x*y for x,y in zip((Q(1),Q(0)),direction))==Q(3,5)
 assert sum(x*y for x,y in zip((Q(-1),Q(0)),direction))==Q(-3,5)
 # In the cone x=(a/b)y; dV/dt = pi*a^2*y^2/b^2 * dy/dt.
 a,b,r,y=Q(4),Q(3),Q(2),Q(1)
 rate_times_pi=r*b*b/(a*a*y*y)
 assert rate_times_pi==Q(9,8)
 assert r*b*b/(a*a*(2*y)**2)==rate_times_pi/4
 assert 3*rate_times_pi==Q(27,8) # wrong if the changing surface radius is held constant
 assert Q(21,2)**2+Q(8)**2+Q(6)**2==Q(29,2)**2 # source's cable example
 return dict(status='pass',own_exact_models=True,actual_student_data=False,
             correct_cuboid_diagonal=13,wrong_formula_squared='3355/19',
             wrong_formula_passes=['permutation symmetry','uniform scaling','zero-height plane limit'],
             same_edge_lengths_skew_diagonal_squared='917/5',
             cone_rise_rate='9/(8*pi) ft/min',wrong_constant_radius_rate='27/(8*pi) ft/min',
             source_cable_length='29/2 yards',
             limit='Own calculations and deliberately false counterexample; not reconstructed learner data, a field test, or proof that finitely many checks establish a formula.')

if __name__=='__main__':print(json.dumps(check(),ensure_ascii=False))

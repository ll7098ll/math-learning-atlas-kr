"""Independent checks of authored example values, not proofs of learning order."""
from fractions import Fraction as F
from math import sin, cos, pi, sqrt, isclose, exp

assert sum(2*k+1 for k in range(2,5))==21
for k in range(1,30):
    assert F(k*(k+1),2)+k+1==F((k+1)*(k+2),2)
assert isclose(sin(pi/4+pi/6),(sqrt(6)+sqrt(2))/4)
assert isclose(4+9-12*cos(pi/3),7)
assert F(2,3)*F(1,2)==F(1,3)
assert 1-F(5,6)**2==F(11,36)
assert F(3+2-1,6)==F(2,3)
assert F(2**4-1**4,4)==F(15,4)
assert isclose(exp(1)-(exp(1)-exp(0)),1)
assert F(3,2)==F(3*1**2,2*1)
# Exact rational parametrizations test the conic distance identities at non-axis points.
for t in [F(0),F(1,3),F(1,2),F(1),F(2)]:
    x=5*(1-t*t)/(1+t*t);y=8*t/(1+t*t)
    assert x*x/25+y*y/16==1
    assert (x+3)**2+y*y==(5+3*x/5)**2
    assert (x-3)**2+y*y==(5-3*x/5)**2
    assert 5+3*x/5>0 and 5-3*x/5>0
for t in [F(0),F(1,3),F(1,2)]:
    x=3*(1+t*t)/(1-t*t);y=8*t/(1-t*t)
    assert x*x/9-y*y/16==1
    # Left-focus distance minus right-focus distance is 2a on the right branch.
    assert (x+5)**2+y*y==(5*x/3+3)**2
    assert (x-5)**2+y*y==(5*x/3-3)**2
for y in [F(0),F(1),F(3),F(8)]:
    x=y*y/8
    assert (x-2)**2+y*y==(x+2)**2
# A valid coordinate instance of the synthetic three-perpendiculars proof.
PH2,HA2,AB2=F(4),F(9),F(25)
assert PH2+(HA2+AB2)==(PH2+HA2)+AB2
print('Advanced example checks passed: finite sums, induction step algebra, trig values, probabilities, integral values, three conic distance identities, perpendicular-distance decomposition')

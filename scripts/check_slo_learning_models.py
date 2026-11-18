"""Check the mathematical counterexamples independently of source diagrams."""
from fractions import Fraction as F
from statistics import median
from itertools import permutations
import json
A=[0,1,2,2,3,4,6,7,8,8,9,10];B=[0,0,1,3,5,5,5,5,7,9,10,10]
def five(x):
 x=sorted(x);return [x[0],median(x[:6]),median(x),median(x[6:]),x[-1]]
assert five(A)==five(B)==[0,2,5,8,10] and A.count(5)==0 and B.count(5)==4
assert F(sum(A),12)==F(sum(B),12)==5
assert F(2)-F(3,2)*6==-7 and F(8)+F(3,2)*6==17
assert all(-7<=v<=17 for v in A+B)
a=[1,9,9,9];b=[7,7,7,7]
assert F(sum(a),4)==F(sum(b),4)==7 and sum(x>6 for x in a)==3 and sum(x>6 for x in b)==4
before=[40,50,90];after=[45,55,60]
assert F(sum(before),3)==60 and F(sum(after),3)==F(160,3)<60
assert sum(y<x for x,y in zip(before,after))==1
changes={sum(y<x for x,y in zip(before,order)) for order in permutations(after)}
assert changes=={1,2} # Marginals cannot reconstruct even the number decreasing.
xs=[F(1),F(1),F(2),F(2)];ys=[F(0),F(10),F(4),F(6)]
assert sum((x-F(3,2))*(y-5) for x,y in zip(xs,ys))==0
assert max(ys[:2])-min(ys[:2])==10 and max(ys[2:])-min(ys[2:])==2
assert sum(ys[:2])/2==sum(ys[2:])/2==5
print(json.dumps(dict(status='pass',counterexamples=4,pairing_permutations=6,scope='same five-number summaries with different inner values; mean vs threshold; aggregate change vs paired change; zero slope vs unequal conditional spread. Own synthetic models, not reconstructed source or learner data.')))

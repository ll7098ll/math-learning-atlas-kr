"""Exact own models for the online guide corrections; no learner data."""
from fractions import Fraction as Q
import json

def check():
 # Positive-side rectangle 9 by 4, diameter 13; altitude of its semicircle is 6.
 B,E,F,G,H=(Q(0),Q(0)),(Q(9),Q(0)),(Q(13),Q(0)),(Q(13,2),Q(0)),(Q(9),Q(6))
 def d2(p,q):return sum((a-b)**2 for a,b in zip(p,q))
 def shape(*ps):
  sides=sorted(d2(ps[i],ps[j]) for i,j in [(0,1),(1,2),(0,2)])
  return [x/sides[0] for x in sides]
 assert d2(G,H)==d2(G,B)==d2(G,F)==Q(169,4)
 assert Q(9,6)==Q(6,4) and Q(6)**2==Q(9)*4
 assert shape(B,F,H)==shape(B,H,E)==shape(H,F,E)
 assert shape(H,G,E)!=shape(B,F,H)
 # A square's side is a mean proportional, not an arithmetic mean.
 assert Q(6)**2==36 and Q(13,2)**2==Q(169,4)!=36
 # Similar 3-4-5 triangles: doubling lengths quadruples area.
 assert Q(3)*4/2==6 and Q(6)*8/2==24
 assert Q(24,6)==Q(2)**2 and Q(12)*16/2==96
 # A fixed 2:1 rectangular remainder has height/base k=1/2.
 for a in [Q(2),Q(10),Q(13,2)]:
  for k in [Q(1,2),Q(1),Q(3,2)]:
   bound=k*a*a/4
   for i in range(1,40):
    x=a*i/40;area=k*x*(a-x)
    assert area==bound-k*(x-a/2)**2 and area<=bound
    assert (area==bound)==(x==a/2)
   assert k*0*(a-0)==k*a*(a-a)==0
 assert Q(1,2)*Q(10)**2/4==Q(25,2)<20<Q(10)**2/4
 # Interior chords, including one diameter and one non-diameter.
 assert Q(8)*2==Q(4)*4==Q(5)**2-Q(3)**2==16
 assert Q(5)*5==25  # intersection at the center
 # An external point is outside III.35's interior-segment hypothesis.
 assert Q(1)*11==Q(6)**2-Q(5)**2==11
 assert Q(5)**2-Q(6)**2==-11
 return dict(status='pass',own_exact_rational_models=True,actual_student_data=False,
             ii14_correct_triangles=['BFH','BHE','HFE'],ii14_rejects_hge=True,
             rectangle_area=36,mean_proportional=6,similarity_area_factor=4,
             rectangular_remainder_maximum='25/2',square_remainder_maximum=25,
             interior_chord_product=16,external_positive_distance_product=11,
             limit='Exact examples/counterexamples and a displayed square identity; not a complete independent reconstruction of Euclid, actual compass execution, historical originals or learner evidence.')

if __name__=='__main__':print(json.dumps(check(),ensure_ascii=False))

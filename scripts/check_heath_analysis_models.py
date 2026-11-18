"""Exact checks of authored examples; no student observations are simulated."""
from fractions import Fraction as F
import json

def check():
    dot=lambda u,v:sum(x*y for x,y in zip(u,v))
    sub=lambda p,q:tuple(x-y for x,y in zip(p,q))
    norm=lambda u:dot(u,u)
    a,b=(F(-1),F(0)),(F(1),F(0))
    def angle(p):
        u,v=sub(a,p),sub(b,p)
        return dot(u,v),norm(u)*norm(v)
    # Multiplication by a possibly zero factor loses the reverse implication.
    candidates=[x for x in range(-10,11) if x*(x-1)==2*(x-1)]
    assert candidates==[1,2]
    assert [x for x in candidates if x==2]==[2]
    assert all((not (x==2)) or x*(x-1)==2*(x-1) for x in range(-10,11))
    assert 1*(1-1)==2*(1-1) and 1!=2
    # Logical forms are checked exhaustively, apart from the numeric sample.
    implies=lambda p,q:not p or q
    rows=[(p,q) for p in [False,True] for q in [False,True]]
    assert all(not(implies(p,q) and not q) or not p for p,q in rows)
    assert any(implies(p,q) and q and not p for p,q in rows)
    o=(F(0),F(4,3));p=(F(0),F(3));q=(F(0),F(-1,3))
    assert all(norm(sub(x,o))==F(25,9) for x in [a,b,p,q])
    dp,np=angle(p);dq,nq=angle(q)
    assert (dp,np)==(F(8),F(100))
    assert (dq,nq)==(F(-8,9),F(100,81))
    assert dp/10==F(4,5) and dq/F(10,9)==F(-4,5)
    assert p[1]>0>q[1]
    # Same circle and same side fail when the base endpoints miss the circle.
    p2=(F(0),F(2));r=(F(6,5),F(8,5))
    assert norm(p2)==norm(r)==4 and norm(a)==norm(b)==1
    assert p2[1]>0 and r[1]>0
    d2,n2=angle(p2);dr,nr=angle(r)
    assert d2>0 and dr>0
    assert d2*d2/n2==F(9,25) and dr*dr/nr==F(225,481)
    assert F(9,25)!=F(225,481)
    return dict(status='pass',zero_factor_candidates=candidates,original_solution=[2],
        logical_truth_rows=4,opposite_arc_cosines=['4/5','-4/5'],
        missing_base_incidence_squared_cosines=['9/25','225/481'],
        exact_rational_models=True,synthetic_examples=True,student_data=False)

if __name__=='__main__':print(json.dumps(check()))

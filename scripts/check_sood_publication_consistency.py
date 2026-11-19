"""Check reported arithmetic and the limits of candidate sample reconstructions."""
from fractions import Fraction as F
from decimal import Decimal,localcontext
import json

def pooled_t(n1,n2,m1,m2,s1,s2):
    with localcontext() as ctx:
        ctx.prec=40
        n1,n2=Decimal(n1),Decimal(n2)
        var=((n1-1)*s1*s1+(n2-1)*s2*s2)/(n1+n2-2)
        return abs(m1-m2)/(var*(1/n1+1/n2)).sqrt()

def check():
    assert 77+58==135 and 77+40==117 and 77+27+21==125
    assert 38+39==77 and 31+27==58 and 27+50==77 and 25+33==58
    assert 61+40==101 and 5+4==9 and 135-2!=99 and 101-2==99
    assert (5+5+4+4)==18 and 40+20==60
    # Rounded source means/SDs. These are hypotheses about two summary models,
    # not a reconstructed sample or the author's actual analysis.
    m1,m2,s1,s2=map(Decimal,['65.22','67.49','4.32','3.90'])
    candidates={str((a,b)):str(pooled_t(a,b,m1,m2,s1,s2)) for a,b in [(61,40),(77,58)]}
    assert Decimal('2.67')<Decimal(candidates['(61, 40)'])<Decimal('2.69')
    assert Decimal(candidates['(77, 58)'])>3
    # A nonsignificant change is compatible with change; it is not an
    # equivalence test. Equal means can also hide individual changes.
    before=[F(2),F(8)];after=[F(8),F(2)]
    assert sum(before)==sum(after) and before!=after
    return dict(status='pass',reported_total_arithmetic=[135,117,125,101],candidate_pooled_t=candidates,actual_sample_reconstructed=False,original_thesis_read=False,official_erratum_verified=False,student_data=False)

if __name__=='__main__':print(json.dumps(check()))

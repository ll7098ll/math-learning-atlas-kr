"""Bounded mathematical checks; no MPC student records or models are reanalysed."""
from fractions import Fraction as F
import json


def check():
    # Exact synthetic two-group OLS with an intercept and one treatment indicator.
    # A common positive affine change preserves standardized effects and t^2.
    def fit(a, b):
        ma, mb = sum(a) / len(a), sum(b) / len(b)
        impact = mb - ma
        va = sum((x-ma)**2 for x in a) / (len(a)-1)
        vb = sum((x-mb)**2 for x in b) / (len(b)-1)
        pooled = ((len(a)-1)*va + (len(b)-1)*vb) / (len(a)+len(b)-2)
        se2 = pooled * (F(1, len(a)) + F(1, len(b)))
        return impact, se2, impact**2 / va, impact**2 / se2
    a, b = list(map(F, [1, 2, 5, 6])), list(map(F, [2, 4, 6, 8]))
    base = fit(a, b)
    scale, shift = F(7, 3), F(41, 5)
    transformed = fit([shift+scale*x for x in a], [shift+scale*x for x in b])
    assert transformed[0] == scale*base[0]
    assert transformed[1] == scale**2*base[1]
    assert transformed[2:] == base[2:]
    # With an intercept, all exhaustive site dummies require a coding constraint.
    for site in range(3):
        d = [int(i == site) for i in range(3)]
        assert sum(d) == 1
        assert F(2) + sum(F(i+1)*d[i] for i in range(3)) == F(7) + sum(F(i-4)*d[i] for i in range(3))
    # Distinct printed cutoffs leave a genuine interval, including the endpoint.
    assert F('31.5') < 32 and not F('31.5') < F('31.5')
    assert F('31.75') < 32 and not F('31.75') < F('31.5')
    assert 3*30 == 90 and 3*30 != 75  # plans do not identify observed exposure
    assert 641+684 == 1325 and 303+310 == 613 and 303+345 == 648
    assert 320+335 == 655 and 307+315 == 622
    assert 522 != 622  # B4 stayers; equal counts elsewhere do not imply equal sets
    assert sum([7,20,5,4,4,4,4,0]) == 48
    assert sum([9,17,2,1,0,0,1,1]) == 31
    assert 3+6 == 9 and 5+1 == 6 and 5+5 == 10  # coins versus cents
    assert F('.30')/F('1.046') == F(150,523)
    assert F('.19')/F('1.046') == F(95,523)
    assert F('.30')/F('.556') > F(1,2)
    growth = [str(F(v)/F('.63')) for v in ['.73','1.57','2.63']]
    assert growth == ['73/63','157/63','263/63']
    # Independent rounding can explain small mean/impact discrepancies.
    for x,y,z in [('38.35','37.61','.73'),('39.12','36.50','2.63'),('6.29','5.91','.37')]:
        assert abs(F(x)-F(y)-F(z)) < F('.015')
    # Positive SD cannot reverse a strictly positive impact's sign (Table G.7).
    for impact, es in [('.04','-.19'),('.20','-.15')]:
        assert F(impact) > 0 > F(es)
    return dict(status='pass', hypothetical=True, affine_invariance_conditional=True,
                actual_scoring_pipeline_identified=False, printed_cutoffs_reconciled=False,
                official_erratum=False, observed_trial_records_used=False,
                models_refitted=False, student_validated=False,
                benchmark_months_exact=growth)


if __name__ == '__main__':
    print(json.dumps(check()))

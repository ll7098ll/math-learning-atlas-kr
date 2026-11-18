"""Own exact checks of paired quantities and analysis units, not raw student data."""
from fractions import Fraction
from math import sqrt
import json

def check():
    assert Fraction(3,12)!=Fraction(12,80)
    assert Fraction(3,20)==Fraction(12,80)
    assert Fraction(3,12)==Fraction(20,80)
    assert Fraction(12,36)==Fraction(1,3)
    # A sample with an unknown cannot be solved by cue word alone.
    assert 12/Fraction(1,3)==36
    assert Fraction(1,3)*36==12
    checked=0
    for eggs in range(1,13):
        for cakes in range(1,25):
            for scale in range(1,7):
                assert Fraction(eggs,cakes)==Fraction(eggs*scale,cakes*scale)
                assert Fraction(eggs,eggs*scale)==Fraction(cakes,cakes*scale)
                checked+=1
    assert 18+1+3==22 and 8+14==22 and 11+11==22
    assert 9+11==20 and 9+10==19 and 11+10==21
    # Missing values are not zero and a four-wave complete-case denominator
    # does not overwrite the immediate-post denominator.
    assert Fraction(2,11)!=Fraction(3,22)
    assert Fraction(1,2)/16*100==Fraction(25,8)
    assert Fraction(1,2)/10*100==5
    pooled=sqrt((13.92**2+22.70**2)/2)
    post_d=(79.41-47.55)/pooled
    did_d=((79.41-25.19)-(47.55-29.85))/pooled
    approximate_small_sample_factor=1-3/(4*(11+11-2)-1)
    baseline_difference_corrected_g=did_d*approximate_small_sample_factor
    assert round(post_d,2)==1.69 and round(baseline_difference_corrected_g,2)==1.87
    return dict(status='pass',own_pair_checks=checked,
        displayed_equation_false=True,correct_within_pair_equation='3/20=12/80',
        valid_across_pair_equation='3/12=20/80',initial_n=22,
        maintenance_n=20,followup_complete_case_n=19,generalization_post_n=21,
        raw_post_d=post_d,own_rounded_summary_baseline_corrected_g=baseline_difference_corrected_g,
        exact_wwc_reanalysis_verified=False,raw_student_data=False,
        official_erratum_confirmed=False,student_validation=False)

if __name__=='__main__':print(json.dumps(check()))

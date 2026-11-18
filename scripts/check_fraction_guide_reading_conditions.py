"""Exact own counterexamples; these are not student data or source errata."""
from fractions import Fraction
import json

def check():
    # Comparing the unnormalised integers is not a test for value >= 1.
    assert -3 >= -5 and Fraction(-3,-5)<1
    assert not (-5 >= -3) and Fraction(-5,-3)>1
    assert Fraction(1,2)==Fraction(2,4)
    values=sorted({Fraction(n,d) for n in range(-3,4) for d in range(1,6)})
    count=0
    for a in values:
        for b in values:
            if a<b:
                assert a<(a+b)/2<b
                count+=1
    # The value per one unit depends on which quantity is named first.
    assert Fraction(3,9)==Fraction(1,3)==Fraction(2,6)
    assert Fraction(9,3)==3 and Fraction(1,3)*3==1
    return dict(status='pass',negative_denominator_counterexamples=2,equal_value_endpoints=True,
        finite_distinct_endpoint_pairs=count,unit_ratio_direction_distinguished=True,
        general_argument='For a<b, subtracting a from (a+b)/2 and subtracting (a+b)/2 from b both give (b-a)/2>0. Equal values do not satisfy this strict premise.',
        student_data=False,official_erratum_confirmed=False,all_guide_mathematics_independently_proved=False)

if __name__=='__main__':print(json.dumps(check()))

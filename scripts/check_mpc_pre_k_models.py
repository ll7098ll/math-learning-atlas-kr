"""Exact checks of measurement examples, not a reanalysis of MPC records."""
from fractions import Fraction as F
import json


def check():
    # A hypothetical twelve-minute group of three in a class of eighteen.
    provided = 12
    child_minutes = provided * 3
    assert F(child_minutes, 18) == 2 and provided != F(child_minutes, 18)
    # A failed practice screen is not automatically an observed zero.
    complete_a, complete_b = F(2, 3), F(2, 2)
    zero_a, zero_b = F(2, 4), F(2, 4)
    assert complete_a - complete_b == -F(1, 3)
    assert zero_a - zero_b == 0
    # Rounded display means may differ from an independently rounded impact.
    def compatible(a, b, impact):
        return abs(F(a) - F(b) - F(impact)) < F('0.015')
    assert compatible('3.59', '1.84', '1.74')
    assert compatible('31.85', '25.41', '6.43')
    # Four exclusive, exhaustive categories with a common denominator cannot
    # sum to 100.5 solely from nearest-tenth rounding; those premises are unverified.
    assert sum(map(F, ['32.1', '34.2', '26.1', '8.1'])) == F('100.5')
    assert F('.5') > 4 * F('.05')
    assert 35 + 35 == 70 and 35 + 34 == 69
    assert 1408 + 1307 == 2715 and 433 + 426 == 859
    assert 698 + 691 == 1389 and 209 + 158 + 220 + 256 == 843
    # Planned subsampling prevents interpreting consent minus testing as attrition.
    assert 859 < 1389 < 2715
    # This is a transport assumption, not observed annual child exposure.
    assert F('11.95') * 200 / 60 == F(239, 6)
    return dict(status='pass', hypothetical=True,
                provided_minutes=12, child_minutes=36, mean_minutes_per_child=2,
                practice_complete_difference='-1/3', practice_zero_difference='0',
                initial_sites=70, implemented_sites=69,
                observed_trial_records_used=False, models_refitted=False,
                official_erratum=False, student_validated=False)


if __name__ == '__main__':
    print(json.dumps(check()))

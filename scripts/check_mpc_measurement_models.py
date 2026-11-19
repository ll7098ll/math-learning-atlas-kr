"""Own exact checks of displayed rules and aggregates, without student records."""
from fractions import Fraction as F
import json


def minimum_absent(days, strict=False):
    assert isinstance(days, int) and days > 0
    # Attendance <90% means absence >10%; attendance <=90% means >=10%.
    return days // 10 + 1 if strict else (days + 9) // 10


def check():
    # Exhaustively compare integer thresholds with the stated rational rules.
    for days in range(1, 367):
        inclusive = [a for a in range(days + 1) if F(days-a, days) <= F(9, 10)]
        strict = [a for a in range(days + 1) if F(days-a, days) < F(9, 10)]
        assert min(inclusive) == minimum_absent(days)
        assert min(strict) == minimum_absent(days, True)
    assert minimum_absent(178) == minimum_absent(178, True) == 18
    assert minimum_absent(180) == 18 and minimum_absent(180, True) == 19
    assert F(162, 180) == F(9, 10) and F(160, 178) < F(9, 10)
    assert 19 != minimum_absent(178)  # report's illustrative footnote
    assert 945+899 == 1844 and 226+230 == 456 and 226+255 == 481
    assert 1165+1112 == 2277 and 274+282 == 556 and 274+313 == 587
    assert len({1844, 1849, 1788, 2166, 2276}) == 5
    assert 1007+995 == 2002 and 1844+2002 == 3846
    assert 2277+2393 == 4670 and 2819+1911+1060 == 5790
    assert 2702+1911+1060 != 5790  # eligibility versus roster definition
    assert round(100*F(2702-1844, 2702), 2) == F('31.75')
    assert round(100*F(2819-1844, 2819), 2) == F('34.59')
    assert F('.34')/F('.85') == F('0.40')
    assert round(100*F('.10')/F('.85'), 2) == F('11.76')
    assert F('32.6')-F('23.6') == 9
    assert round(100*F(9, 1)/F('32.6'), 1) == F('27.6')
    assert 78141*F('.09') == F('7032.69')  # hypothetical transport, not new N
    assert F('.10')+F('.02') != F('.34')  # unequal samples, not synergy proof
    # Within-group tests and moderation test address different nulls.
    assert F('.01') < F('.05') < F('.28') and F('.24') > F('.05')
    assert F('.04') < F('.05') < F('.58')  # D4's distinct literacy contrasts
    # A rounded p=0.00 can be a strictly positive number.
    assert round(F('0.004'), 2) == 0 and F('0.004') > 0
    return dict(status='pass',attendance_integer_years_checked=366,
        minimum_absent_178_inclusive=18,minimum_absent_178_strict=18,
        printed_178_example=19,minimum_absent_180_inclusive=18,
        minimum_absent_180_strict=19,mpc_outcome_denominators=[1844,1849,1788,2166,2276],
        math_benchmark_ratio='0.34/0.85=0.40',attendance_difference_percentage_points=9,
        attendance_relative_reduction_percent='27.6',hypothetical_city_reduction='7032.69',
        subgroup_within_p=['.28','.01'],subgroup_difference_p='.24',
        raw_student_data_reanalyzed=False,models_refitted=False,
        classification_code_verified=False,official_erratum=False,student_validated=False)


if __name__ == '__main__':
    print(json.dumps(check()))

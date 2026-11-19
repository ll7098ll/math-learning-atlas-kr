"""Own rule and identification checks; no trial records or model reanalysis."""
from fractions import Fraction as F
import json


def selected(significant, preschool, normed=None, developer=None):
    return significant and preschool and (
        (normed is not None and normed >= F('0.2')) or
        (developer is not None and developer >= F('0.5')))


def check():
    # Selection requires significant preschool evidence and either measure gate.
    assert selected(True, True, normed=F('.2'))
    assert selected(True, True, developer=F('.5'))
    assert not selected(False, True, normed=F('.3'))
    assert not selected(True, False, developer=F('.8'))
    assert not selected(True, True, normed=F('.19'), developer=F('.49'))
    # Days, children, sessions and minutes have distinct denominators.
    assert F(4, 5) >= F(66, 100) and F(14, 20) < F(75, 100)
    for denominator in range(1, 367):
        for numerator in range(denominator + 1):
            assert (F(numerator, denominator) >= F(66, 100)) == (100*numerator >= 66*denominator)
            assert (F(numerator, denominator) >= F(75, 100)) == (4*numerator >= 3*denominator)
    assert F(149, 180) != F(96, 100)
    assert F(99, 120) != F(98, 100)
    assert F(99, 2) == F('49.5')  # biweekly mean expressed per week, hypothetically
    # Hypothetical means: only three cells are observed. Varying the missing
    # High5s-only cell changes the interaction while those three remain fixed.
    mu00, mu10, mu11 = 10, 12, 15
    interactions = [mu11-mu10-mu01+mu00 for mu01 in [10, 15]]
    assert interactions == [3, -2]
    return dict(status='pass',integer_denominators_checked=366,
        selection_rule='significant AND preschool AND (normed>=.2 OR developer>=.5)',
        coaching_minutes_fractions=['149/180 weekly', '99/120 biweekly'],
        session_occurrence_percent=[96, 98],
        missing_cell_example=dict(hypothetical=True, observed_means=[10, 12, 15],
            alternative_missing_means=[10, 15], interactions=interactions),
        raw_student_data_reanalyzed=False, models_refitted=False,
        official_erratum=False, student_validated=False)


if __name__ == '__main__':
    print(json.dumps(check()))

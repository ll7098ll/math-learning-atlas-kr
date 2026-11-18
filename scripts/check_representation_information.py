"""Check the own workbook example: information depends on the stated purpose."""
from fractions import Fraction
from collections import defaultdict
import json

def check():
    groups=defaultdict(list)
    for x in range(1,10):groups[x*(10-x)].append(x)
    assert dict(groups)=={9:[1,9],16:[2,8],21:[3,7],24:[4,6],25:[5]}
    # Labelled x cannot be recovered uniquely from area; swapping x/y still
    # describes congruent, unlabelled rectangles, not a new geometric shape.
    assert all(len({tuple(sorted((x,10-x))) for x in xs})==1 for xs in groups.values())
    assert len({(x,x*(10-x)) for x in range(1,10)})==9
    for denominator in range(1,11):
        for numerator in range(1,10*denominator):
            x=Fraction(numerator,denominator)
            assert x*(10-x)==10*x-x*x==25-(x-5)**2
            assert x*(10-x)==(10-x)*x and x*(10-x)<=25
            assert (x*(10-x)==25)==(x==5)
    # Changing from four fenced sides to three changes the model, not the
    # correctness of the old conditional proof.
    assert 25-(Fraction(5)-5)**2==25
    assert 50-2*(Fraction(5)-5)**2==50
    return dict(status='pass',area_groups={str(a):xs for a,xs in groups.items()},
                own_model=True,actual_student_data=False,claim='Area alone loses labelled-side information; each collision swaps congruent rectangle sides. Polynomial identities and maximum equality hold on the sampled rational domain; the displayed square identity supplies the general argument.')

if __name__=='__main__':print(json.dumps(check(),ensure_ascii=False))

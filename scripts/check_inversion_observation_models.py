"""Exact synthetic contrasts: identity, response bias and the stated chance model."""
from fractions import Fraction as F
from math import comb
import json

def tail(n,k,p):return sum((F(comb(n,j))*p**j*(1-p)**(n-j) for j in range(k,n+1)),F(0))
def check():
    witnesses=0
    for initial in range(5,26):
        for change in range(2,6):
            assert initial+change-change==initial and initial-change+change==initial
            witnesses+=2
    # Neither an exact starting count nor the same individual objects is required.
    assert all(n+3-2==n+1 for n in range(5,26))
    inverse_answers=['same']*8;control_answers=['more']*4+['fewer']*4
    constant=['same']*16
    inverse_correct=sum(a==b for a,b in zip(constant[:8],inverse_answers))
    control_correct=sum(a==b for a,b in zip(constant[8:],control_answers))
    assert (inverse_correct,control_correct)==(8,0)
    inverse_tail=tail(8,6,F(1,3));assert inverse_tail<F(2,100)
    broad_control_tail=tail(8,7,F(2,3));binary_tail=tail(8,7,F(1,2));direction_tail=tail(8,7,F(1,3))
    assert broad_control_tail==F(1280,6561) and broad_control_tail>F(19,100)
    assert binary_tail==F(9,256) and direction_tail==F(17,6561)
    assert F(5,10)!=1 and 60-8==52 and 60-9==51
    return dict(status='pass',identity_witnesses=witnesses,constant_same_correct=[inverse_correct,control_correct],inverse_six_of_eight_p=str(inverse_tail),control_seven_of_eight_p={'any_non_same_uniform_three_choices':str(broad_control_tail),'correct_direction_binary_choices':str(binary_tail),'correct_direction_uniform_three_choices':str(direction_tail)},pdf_text_discrepancy_not_official_erratum=True,authors_raw_data_reanalysed=False,student_data=False)

if __name__=='__main__':print(json.dumps(check()))

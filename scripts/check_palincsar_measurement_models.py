"""Exact checks for our counterexamples; not reanalysis of original students."""
from fractions import Fraction
import json

def months(grade, month):
    assert isinstance(grade,int) and isinstance(month,int) and grade>=0 and 0<=month<12
    return grade*12+month

def check():
    # A single counterexample disproves an alleged identity; the expanded identity
    # remains true over these exact rational instances, with its algebraic reason.
    assert (1+1)**2 != 1**2+1
    for x in [Fraction(n,d) for n in range(-7,8) for d in range(1,8)]:
        assert (x+1)**2==x*x+2*x+1
    assert months(5,0)-months(4,2)==10
    assert Fraction('5.0')-Fraction('4.2')==Fraction(4,5)
    assert Fraction(4,5)*12==Fraction(48,5)!=10
    # Same 33/36 total accuracy; completely different anomaly detection.
    a=dict(tp=0,tn=33,fp=0,fn=3)
    b=dict(tp=3,tn=30,fp=3,fn=0)
    for row in [a,b]:
        assert sum(row.values())==36 and row['tp']+row['fn']==3 and row['tn']+row['fp']==33
        assert Fraction(row['tp']+row['tn'],36)==Fraction(11,12)
    assert Fraction(a['tp'],3)==0 and Fraction(b['tp'],3)==1
    assert sum([6,6,6,6])+13==37 and sum([7,5,5,4])==21
    # Missing test results cannot be interpreted as observed zero scores.
    transfer={'RT':[7,8],'control':[3,4],'LI':None,'test_only':None}
    assert len([x for x in transfer.values() if x is not None])==2
    return dict(status='pass',rational_identity_instances=105,grade_month_difference=10,
                same_accuracy='33/36',anomaly_detection=['0/3','3/3'],study1_groups=[6,6,6,6],
                study1_normative=13,study1_total=37,study2_groups=[7,5,5,4],study2_total=21,
                synthetic=True,raw_student_data_reanalysed=False)

if __name__=='__main__':print(json.dumps(check()))

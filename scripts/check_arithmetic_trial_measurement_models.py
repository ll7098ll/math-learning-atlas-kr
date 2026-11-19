"""Check displayed arithmetic and decision rules; never reconstruct student data."""
from fractions import Fraction as F
import json

def qualifies(levels):
    return all(F(correct,total)>=F(3,4) for correct,total in levels)

def check():
    # A good target performance does not erase failure at an earlier level.
    assert not qualifies([(1,4),(4,4)]) and qualifies([(3,4),(4,4)])
    # The pilot's all-but-one rule is different from the trial's 75% rule.
    assert 2>=3-1 and F(2,3)<F(3,4)
    lt=[2,4,0,7,0,0];skip=[0,0,1,5,5,1]
    assert sum(lt)==13 and sum(skip)==12 and 13-sum(lt[:3])==7
    assert 7!=6 # neutral count in Table2/AppendixC versus prose645
    # Three-level growth at any teaching session is not independent retention.
    assert 8+5==13 and (8,5)!=(sum(lt[:3]),sum(lt[3:]))
    # Model values are all positive but not equal; one interval contains zero.
    grid=[F(x) for x in ['.96','.78','.59','.51','.54','.57','.05','.30','.55']]
    assert min(grid)>0 and len(set(grid))>1 and F('-.47')<0<F('.51')
    # Displayed WAIC rounded to nearest 0.1 cannot yield the reported 8.74.
    displayed=F('478.1')-F('469.6');assert displayed==F('8.5')
    possible=(displayed-F('.1'),displayed+F('.1'))
    assert not possible[0]<=F('8.74')<=possible[1]
    # Target-item example: separate baseline subgroup denominators, not all N.
    assert round(100*F(46,93),1)==F('49.5') and round(100*F(30,114),1)==F('26.3')
    assert F(46,93)!=F(46,143) and F(30,114)!=F(30,148)
    assert 39+7+6+0==52 and 40+11+8+2==61
    assert 41+1+45+4==91 and 53+3+30+1==87
    assert 52+91==143 and 61+87==148
    assert 52+41==93 and 61+53==114
    assert 34-22==12 and 34-21==13 # unresolved body/supplement item counts
    assert F('14.3')-F('13.4')==F('.9')
    assert F('1.43')>F('.37') # source prints interval endpoints in reverse order
    # Counting-on: anchor retained, only the increments are counted as added.
    assert list(range(4+1,4+7+1))==[5,6,7,8,9,10,11]
    assert len(list(range(4+1,4+7+1)))==7
    return dict(status='pass',pilot_neutral_count=7,pilot_prose_count=6,
                trial_displayed_waic_difference=str(displayed),
                trial_reported_waic_difference='8.74',
                nearest_tenth_rounding_assumption=True,
                trial_subgroup_denominators=[93,114],
                official_supplement_counting_rows=9,body_counting_items=8,
                official_supplement_arithmetic_rows=[22,34],body_pre_items=21,
                actual_administered_item_correspondence_verified=False,
                all_prior_levels_required_for_research_75_percent_rule=True,
                pilot_all_but_one_rule_is_not_75_percent=True,
                raw_student_data_reanalyzed=False,models_refitted=False,
                official_erratum=False,local_student_validation=False)

if __name__=='__main__':print(json.dumps(check()))

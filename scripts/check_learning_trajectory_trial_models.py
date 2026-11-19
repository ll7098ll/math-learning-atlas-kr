"""Check displayed aggregates and own examples, without reconstructing trial data."""
from fractions import Fraction as F
from statistics import median
import json

def nearest(x):
    return (x.numerator*2+x.denominator)//(2*x.denominator)

def compatible_denominators(count,percent,maximum=200):
    return [n for n in range(count,maximum+1) if nearest(F(100*count,n))==percent]

def check():
    length_cells={
        'BAU':[2,3,3,2,1,2,2,8,2,5,6,4,4,4,5,4],
        'LT':[4,2,4,1,1,4,2,4,6,7,4,4,6,6,7,7],
        'REV':[2,3,3,1,2,0,3,4,5,4,8,3,8,4,5,4]}
    assert {k:sum(v) for k,v in length_cells.items()}==dict(BAU=57,LT=69,REV=59)
    assert sum(map(sum,length_cells.values()))==185
    assert 22+63+65==150 and 26+11==37 and 150+37==52+135==187
    assert (150,37)!=(52,135)
    percent=F(39*100,185)
    assert nearest(percent*100)==2108 and nearest(percent*100)!=2008
    # Nearest-integer percentage rounding is an explicit assumption for this check.
    lt=compatible_denominators(44,59);skip=compatible_denominators(23,35)
    skip_incorrect=compatible_denominators(9,13)
    assert lt==[74,75] and skip==[65,66] and skip_incorrect==list(range(67,73))
    assert not set(skip)&set(skip_incorrect) and not [n for n in skip if n<=63]
    # Own counterexample: passing an isolated higher level is not passing all prior levels.
    accuracy=[F(3,4),F(2,4),F(4,4)]
    standalone=[x>=F(3,4) for x in accuracy]
    prefix=[all(standalone[:n+1]) for n in range(3)]
    assert standalone==[True,False,True] and prefix==[True,False,False]
    # Official loo definition: WAIC = -2 * elpd_waic. No model is re-estimated here.
    waic=[F('429.6'),F('433.9'),F('435.1'),F('433.4')]
    elpd=[-x/2 for x in waic]
    assert waic.index(min(waic))==elpd.index(max(elpd))==0
    # Own paired draws: a median contrast need not equal a contrast of marginal medians.
    x,y=[0,0,2],[0,1,1]
    assert median([a-b for a,b in zip(x,y)])==0 and median(x)-median(y)==-1
    # Own illustrative strategy codes: 9 denotes no response, not a high strategy score.
    assert F(sum([2,1,9]),3)==4 and F(sum([2,1]),2)==F(3,2)
    # Source rounded table2 values: descriptive contrasts, without inferred standard errors.
    far9=(F('.34')-F('.32'))-(F('.38')-F('.29'))
    far10=(F('.20')-F('.17'))-(F('.17')-F('.16'))
    assert far9==F(-7,100) and far10==F(2,100)
    assert F(24,100)<F(1,2) and 100-24==76
    return dict(status='pass',data_kind='displayed source aggregates plus explicitly synthetic counterexamples',
                length_posttest_n=185,length_school_counts_table1=[150,37],length_school_counts_prose=[52,135],
                table4_count39_of185_percent_nearest_cent='21.08',printed_table4_percent='20.08',
                shape_rounding_assumption='nearest whole percent;not established author rounding policy',
                shape_complete_correct_compatible_n=dict(LT=lt,skip=skip),skip_incorrect_compatible_n=skip_incorrect,
                common_skip_item_denominator_under_rounding_assumption=False,all_prior_levels_required_in_starting_rule=True,
                waic_direction_reference='https://mc-stan.org/loo/reference/waic.html',waic_minimizes_negative_twice_elpd=True,
                median_contrast_not_forced_to_difference_of_medians=True,missing_strategy_code_not_numeric_score=True,
                descriptive_far_transfer_change_contrasts=[str(far9),str(far10)],icc24_percent_is_majority=False,
                original_child_data_reconstructed=False,model_reestimated=False,official_erratum_verified=False)

if __name__=='__main__':print(json.dumps(check(),ensure_ascii=False,indent=2))

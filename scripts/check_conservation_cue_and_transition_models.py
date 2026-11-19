"""Exact illustrative checks; these are not reconstructed child-level data."""
from fractions import Fraction as F
from math import comb
import json


def fisher_two_sided(a, b, c, d):
    first, second, successes = a+b, c+d, a+c
    denominator = comb(first+second, successes)
    mass = lambda x: F(comb(first, x)*comb(second, successes-x), denominator)
    observed = mass(a)
    return sum((mass(x) for x in range(max(0, successes-second), min(first, successes)+1) if mass(x) <= observed), F(0))


def check():
    # Arbitrary length units, not the original physical layout or coding records.
    variants = {'equal': [(8,8),(8,8)], 'length': [(9,9),(7,7)],
                'density': [(9,8),(7,8)], 'conflict_length': [(9,10),(7,6)],
                'conflict_density': [(9,6),(7,10)], 'conflict_equal': [(8,10),(8,6)]}
    compare = lambda a,b: (a>b)-(a<b)
    cue = {}
    for kind, rows in variants.items():
        length, density = [], []
        for n, size in rows:
            truth = compare(n,8)
            length.append(compare(size,8)==truth)
            density.append(compare(F(n,size),1)==truth)
            # Counting and tracking the actual change have the same answer.
            assert compare(8+(n-8),8)==truth
        assert len(set(length))==len(set(density))==1
        cue[kind] = dict(length_correct=length[0], density_correct=density[0])
    assert [k for k,v in cue.items() if v['length_correct']]==['equal','length','conflict_length']
    assert [k for k,v in cue.items() if v['density_correct']]==['equal','density','conflict_density']
    assert [k for k,v in cue.items() if v['length_correct']==v['density_correct']]==['equal','conflict_equal']
    # A conditional error share can fall while its joint frequency rises.
    assert F(3,4)>F(2,5) and F(1,5)*F(3,4)<F(1,2)*F(2,5)
    # Equal aggregate accuracy does not determine the number of perfect children.
    scores_a, scores_b = [5]*13+[0]*2, [6]*10+[5]+[0]*4
    assert len(scores_a)==len(scores_b)==15 and sum(scores_a)==sum(scores_b)==65
    assert scores_a.count(6)==0 and scores_b.count(6)==10
    whole = fisher_two_sided(8,0,3,4)
    baseline = fisher_two_sided(6,2,3,4)
    assert whole==F(1,39) and baseline==F(45,143)
    # One candidate compatible with rounded panel labels, not recovered observations.
    pre, final = [9,10,13,12,16,10,13,12], [11,9,11,11,9,9,11,12]
    nearest = lambda value: (value.numerator*2+value.denominator)//(value.denominator*2)
    assert [nearest(F(n*100,24)) for n in pre]==[38,42,54,50,67,42,54,50]
    assert [nearest(F(n*100,12)) for n in final]==[92,75,92,92,75,75,92,100]
    assert nearest(F(sum(pre)*100,192))==49 and nearest(F(sum(final)*100,96))==86
    return dict(status='pass',data_kind='exact illustrative models;not raw student/coder data',cue_patterns=cue,
                full_six_type_density_inverse=False,conditional_denominators_distinct=True,
                hypothetical_accuracy=str(F(65,90)),hypothetical_perfect_child_counts=[0,10],
                whole_experiment_fisher_two_sided=str(whole),baseline_fisher_two_sided=str(baseline),
                rounded_figure4_compatible_with_text=True,causal_variability_effect_verified=False)


if __name__=='__main__':
    print(json.dumps(check(),ensure_ascii=False,indent=2))

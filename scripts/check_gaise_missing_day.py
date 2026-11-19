"""Exact counterexamples for the guide's missing ninth observation; no new data."""
from fractions import Fraction as F
import json

OBSERVED={1:F('.75'),2:F(1),3:F(1),4:F('2.2'),5:F(4),6:F(6),7:F('6.5'),8:F(7),10:F(10),11:F(10),12:F(12),13:F(13),14:F(14),15:F(16)}

def check():
    known={d:OBSERVED[d+1]-v for d,v in OBSERVED.items() if d+1 in OBSERVED}
    assert max(known.values())==2
    assert [d for d,v in known.items() if v==2]==[5,11,14]
    assert (OBSERVED[10]-OBSERVED[8])/2==F(3,2)
    possibilities=[]
    for height in [F(7),F(17,2),F(10)]:
        completed={**OBSERVED,9:height}
        changes=[completed[d+1]-completed[d] for d in range(1,15)]
        assert all(v>=0 for v in changes)
        assert all(completed[d]==v for d,v in OBSERVED.items())
        possibilities.append(dict(hypothetical_day9=str(height),day8_to9=str(changes[7]),day9_to10=str(changes[8]),maximum_daily_change=str(max(changes))))
    assert [x['maximum_daily_change'] for x in possibilities]==['3','2','3']
    # Identical observed values permit different true maxima even under monotonicity.
    return dict(status='pass',known_consecutive_pair_maximum='2',missing_day=9,two_day_change='3',interval_daily_mean='3/2',counterexamples=possibilities,student_data=False,additional_observations=False,official_erratum_verified=False)

if __name__=='__main__':print(json.dumps(check()))

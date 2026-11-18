"""Recalculate manuscript chart units and rounding; no learner data are inferred."""
from fractions import Fraction as F
import json
SERIES={
 'country':[1,1,1,1,2,1,2,1,1,2,34],
 'discipline':[3,6,2,2,4,23,4,1],
 'sector':[15,14,9,10,7],
 'iterations':[6,8,6,3,2,3,3,2,1],
 'outcomes':[7,12,12,5],
 'annual_search_2000_2010':[5,14,35,50,122,179,196,264,318,317,372]}

def rounded_percent(c,n):
 x=F(100*c,n)+F(1,2)
 return x.numerator//x.denominator

def check():
 totals={k:sum(v) for k,v in SERIES.items()}
 assert totals==dict(country=47,discipline=45,sector=55,iterations=34,outcomes=36,annual_search_2000_2010=1872)
 iterations=[rounded_percent(c,34) for c in SERIES['iterations']]
 outcomes=[rounded_percent(c,36) for c in SERIES['outcomes']]
 sectors=[rounded_percent(c,55) for c in SERIES['sector']]
 assert iterations==[18,24,18,9,6,9,9,6,3] and sum(iterations)==102
 assert outcomes==[19,33,33,14] and sum(outcomes)==99
 assert sectors==[27,25,16,18,13] and sum(sectors)==99
 assert sum(F(c,34) for c in SERIES['iterations'])==1
 assert sum(F(c,36) for c in SERIES['outcomes'])==1
 assert 2+9*5==47 and 1872+118==1990 and 1990!=1940
 assert F(12,36)==F(1,3) and F(12,31)!=F(1,3)
 return dict(status='pass',source_series_totals=totals,iteration_display_percentages=iterations,iteration_display_total=102,outcome_display_percentages=outcomes,outcome_display_total=99,sector_display_total=99,exact_category_fractions_sum_to_one=True,selected_articles=47,search_screenshot_2011=118,reported_whole_search=1940,forced_annual_plus_screenshot=1990,forced_search_reconciliation_rejected=True,source_data_reconstruction=False,student_data=False,scope='Exact arithmetic on source chart caches and actually read displayed labels. Rounded percentages differ from100without proving duplicate categories;36outcome assignments still differ from31abstracts. Different search periods/snapshots are not forced into one population;no official erratum or independent original-study reconstruction.')

if __name__=='__main__':print(json.dumps(check()))

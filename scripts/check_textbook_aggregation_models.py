"""Exact comparisons of denominators used in a textbook content analysis.

These reproduce arithmetic from printed summaries and construct witnesses;
they do not reconstruct the coders' item records or student outcomes.
"""
from fractions import Fraction as F
from decimal import Decimal,ROUND_HALF_UP,localcontext
import json

def rounded(value):
 with localcontext() as context:
  context.prec=40
  return str((Decimal(value.numerator)/Decimal(value.denominator)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))

def rates(counts,denominators):
 assert len(counts)==len(denominators) and all(d>0 for d in denominators)
 return dict(pooled=F(sum(counts),sum(denominators)),mean_of_book_rates=sum((F(n,d) for n,d in zip(counts,denominators)),F(0))/len(counts))

def check():
 lessons=[11,6,9]
 relations=rates([93,56,118],lessons)
 review=rates([114,76,73],lessons)
 assert sum(lessons)==26 and sum(lessons)+8==34
 assert rounded(relations['pooled'])=='10.27' and rounded(relations['mean_of_book_rates'])=='10.30'
 assert rounded(review['pooled'])=='10.12' and rounded(review['mean_of_book_rates'])=='10.38'
 # A conditional share of feedback-bearing lessons is not a share of all
 # lessons, and neither quantity is a student success rate.
 assert F(4,8)*F(2,4)==F(2,8)==F(1,4) and F(2,4)!=F(2,8)
 assert F(50,2)==25 and rounded(F(50,6))=='8.33'
 # Two printed percentages summing to98 cannot sum to100 merely because
 # each was independently rounded to the nearest hundredth.
 printed=[Decimal('43.83'),Decimal('54.17')]
 assert sum(printed)==98 and sum(printed)+Decimal('.01')<100
 # The same marginal representation counts can arise from very different
 # overlaps. These are synthetic sets, not the books' actual coded items.
 nested=[set(range(23)),set(range(9)),set(range(2))]
 disjoint=[set(range(23)),set(range(23,32)),set(range(32,34))]
 assert [len(s) for s in nested]==[len(s) for s in disjoint]==[23,9,2]
 assert len(set.union(*nested))==23 and len(set.union(*disjoint))==34
 # Classifying a nonexistent subset leaves its conditional mean undefined;
 # it does not forbid a zero numerator over a positive all-lesson denominator.
 def mean_or_none(total,denominator):return F(total,denominator) if denominator else None
 assert mean_or_none(0,0) is None and mean_or_none(0,8)==0
 return dict(status='pass',number_relationship_rates={k:dict(exact=str(v),rounded=rounded(v)) for k,v in relations.items()},within_lesson_review_rates={k:dict(exact=str(v),rounded=rounded(v)) for k,v in review.items()},feedback_conditional_share='1/2',feedback_all_lesson_share='1/4',representation_union_bounds=[23,34],printed_percentage_sum='98.00',actual_coder_records_reconstructed=False,student_data=False,official_erratum_verified=False,universal_review_dose_established=False)

if __name__=='__main__':print(json.dumps(check()))

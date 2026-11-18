"""Own counterexamples for citation selection and nonexclusive category totals."""
from fractions import Fraction
import json

def check():
 candidates=[dict(id=i,citations=100-i,positive_report=i<5) for i in range(50)]
 selected=sorted(candidates,key=lambda r:r['citations'],reverse=True)[:5]
 assert Fraction(sum(r['positive_report'] for r in selected),len(selected))==1
 assert Fraction(sum(r['positive_report'] for r in candidates),len(candidates))==Fraction(1,10)
 # Identical marginal category counts do not identify the union of coded items.
 separate=[set(range(7)),set(range(7,19)),set(range(19,31)),set(range(5))]
 nested=[set(range(7)),set(range(12)),set(range(12)),set(range(5))]
 assert [len(s) for s in separate]==[len(s) for s in nested]==[7,12,12,5]
 assert sum(map(len,separate))==36 and len(set.union(*separate))==31
 assert sum(map(len,nested))==36 and len(set.union(*nested))==12
 assert Fraction(12,36)==Fraction(1,3) and Fraction(12,31)!=Fraction(1,3)
 assert 2+9*5==47 and sum([15,14,9,10,7])==55
 assert sum([6,8,6,3,2,3,3,2,1])==34
 return dict(status='pass',own_synthetic_models=True,actual_student_data=False,authors_dataset_reconstructed=False,citation_selection=dict(selected_positive_percent=100,whole_pool_positive_percent=10),same_category_margins=[7,12,12,5],same_assignment_total=36,possible_distinct_item_totals=[31,12],denominators=dict(assignment_fraction='12/36=1/3',item_fraction='12/31'),limit='Constructed counterexamples show insufficiency, not the actual amount/direction of bias, actual category overlap or educational effects in either source.')
if __name__=='__main__':print(json.dumps(check(),ensure_ascii=False))

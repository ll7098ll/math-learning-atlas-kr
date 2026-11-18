import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import goal_hierarchy

class ReviewTransitions(unittest.TestCase):
 def test_measurement_prompt_contains_its_given_quantities(self):
  d=json.loads((goal_hierarchy.ROOT/'data/goal_hierarchy_primary_3_4_geometry_measure_data.json').read_text(encoding='utf-8'))
  for case in d['cases']:
   if case['standard'] in ('4수03-19','4수03-23'):
    self.assertIn(case['goal'],case['task'])
 def test_external_state_needs_traceable_evidence(self):
  with self.assertRaises(AssertionError):
   goal_hierarchy.validate_review(dict(state='independently_reviewed',independent_review=True))
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);(root/'review.txt').write_text('Review fixture')
   review=dict(state='independently_reviewed',independent_review=True,
    independent_review_evidence=dict(reviewer='External teacher',date='2026-11-04',scope='Task A',file='review.txt'))
   with patch.object(goal_hierarchy,'ROOT',root):
    goal_hierarchy.validate_review(review)
    review['state']='student_validated';review['student_validated']=True
    with self.assertRaises(AssertionError):goal_hierarchy.validate_review(review)
    review['student_validated_evidence']=dict(reviewer='Teacher',date='2026-11-04',scope='Task A anonymized responses',file='review.txt')
    goal_hierarchy.validate_review(review)
    review['student_validated_evidence']['file']='missing.txt'
    with self.assertRaises(AssertionError):goal_hierarchy.validate_review(review)

 def test_no_seconds_in_early_time_representations(self):
  data=json.loads((goal_hierarchy.ROOT/'data/revisions_elementary.json').read_text(encoding='utf-8'))
  for code in ['2수03-07','2수03-08','2수03-09']:
   self.assertNotIn('분과 초',' '.join(data[code]['representations']))
  self.assertTrue(all('시계' not in s and '세로셈' not in s for s in data['2수03-09']['paths']))

if __name__=='__main__':unittest.main()

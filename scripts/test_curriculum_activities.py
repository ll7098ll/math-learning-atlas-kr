"""Ensure the authored curriculum activities reach the actual reading corpus."""
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class ActivityPublication(unittest.TestCase):
 def test_portal_exposes_full_scope_and_statement_only_reviews_separately(self):
  site=R.parent if R.name=='research' else R/'tmp/pathways-release'
  catalog=json.loads((site/'dist/content/catalog.json').read_text(encoding='utf-8'))
  queue=json.loads((R/'data/content_review_queue.json').read_text(encoding='utf-8'))
  states={r['code']:r['state'] for r in queue['full_scope_source_review']}
  self.assertEqual({r['code'] for r in catalog['standards']},set(states))
  for standard in catalog['standards']:
   state=states[standard['code']];self.assertEqual(standard['sourceReviewState'],state)
   if state=='self_checked_source_image':self.assertIn('문장·해설·고려 사항 자체 대조',standard['sourceReview'])
   elif state=='statement_image_only_requires_full_scope_review':self.assertIn('해설·고려 사항 확인 전',standard['sourceReview'])
   elif state=='unreviewed':self.assertEqual(standard['sourceReview'],'미대조')
 def test_every_new_observation_is_readable_in_its_target_document(self):
  records=json.loads((R/'data/curriculum_mapping_reviews.json').read_text(encoding='utf-8'))['reviews']
  checked=0
  for review in records.values():
   activity=review.get('observation_extension')
   if not activity:continue
   for code in review['standard_codes']:
    text=(R/'analyses'/f'{code}.md').read_text(encoding='utf-8')
    self.assertIn(activity['question'],text,code)
    self.assertIn(activity['expected'],text,code)
    self.assertIn('실제 학생의 반응·선택·수정 기록',text,code)
    checked+=1
  self.assertGreater(checked,0)
if __name__=='__main__':unittest.main()

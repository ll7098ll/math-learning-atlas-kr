"""Evidence must remain tied to the reviewed source, images and target content."""
import hashlib,json,unittest
from pathlib import Path
from mapping_review_author import changed_targets
R=Path(__file__).resolve().parents[1]
class ImageReviewIntegrity(unittest.TestCase):
 def test_full_scope_queue_covers_every_standard_without_promoting_legacy_reviews(self):
  queue=json.loads((R/'data/content_review_queue.json').read_text(encoding='utf-8'))
  standards=json.loads((R/'data/standards.json').read_text(encoding='utf-8'))['standards']
  reviews=json.loads((R/'data/curriculum_standard_image_reviews.json').read_text(encoding='utf-8'))['reviews']
  records=queue['full_scope_source_review'];complete={r['code'] for r in records if r['state']=='self_checked_source_image'}
  self.assertEqual({r['code'] for r in records},{s['code'] for s in standards})
  self.assertEqual(len(records),len(standards));self.assertEqual(complete,{r['code'] for r in reviews})
  for r in records:
   if r['legacy_source_status']!='미대조' and r['code'] not in complete:self.assertEqual(r['state'],'statement_image_only_requires_full_scope_review')
  self.assertEqual(queue['source_review_scope_summary']['full_scope_pending'],len(standards)-len(complete))
 def test_pdf_images_and_target_snapshots(self):
  ledger=json.loads((R/'data/curriculum_standard_image_reviews.json').read_text(encoding='utf-8'))
  self.assertEqual(ledger['source_sha256'],hashlib.sha256((R/ledger['source_file']).read_bytes()).hexdigest())
  entries={};cases={}
  for path in (R/'data').glob('goal_hierarchy_*.json'):
   data=json.loads(path.read_text(encoding='utf-8'));entries.update({v['code']:v for v in data['entries']});cases.update({v['id']:v for v in data['cases']})
  self.assertEqual(len({v['code'] for v in ledger['reviews']}),len(ledger['reviews']))
  for review in ledger['reviews']:
   self.assertEqual(changed_targets(review,entries,cases),[],review['code'])
   self.assertEqual({v['pdf_page'] for v in review['evidence']},set(entries[review['code']]['source_review']['pdf_pages']))
   self.assertTrue(review['findings'] and review['content_locations'])
   for item in review['evidence']:self.assertEqual(hashlib.sha256((R/item['file']).read_bytes()).hexdigest(),item['sha256'])
 def test_queue_has_traceable_evidence_for_changed_states(self):
  queue=json.loads((R/'data/content_review_queue.json').read_text(encoding='utf-8'))
  ledger=json.loads((R/'data/curriculum_standard_image_reviews.json').read_text(encoding='utf-8'))
  for record in queue['source_image_review']:
   if record['status']=='미대조':continue
   self.assertEqual(record['evidence']['file'],'data/curriculum_standard_image_reviews.json')
   self.assertIn(record['code'],{r['code'] for r in ledger['reviews']})
 def test_inventory_and_generator_registry_agree_with_evidence(self):
  standards={v['code']:v for v in json.loads((R/'data/standards.json').read_text(encoding='utf-8'))['standards']}
  corrections=json.loads((R/'data/source_corrections.json').read_text(encoding='utf-8'))
  ledger=json.loads((R/'data/curriculum_standard_image_reviews.json').read_text(encoding='utf-8'))
  for record in ledger['reviews']:
   code=record['code']
   self.assertIn(code,corrections['additional_reviewed_codes'])
   self.assertNotEqual(standards[code]['source_review_status'],'미대조')
   self.assertEqual(standards[code]['source_review_evidence'],corrections['additional_review_evidence'][code])
if __name__=='__main__':unittest.main()

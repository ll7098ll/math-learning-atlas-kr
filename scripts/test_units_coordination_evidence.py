"""Published ratings and rank association must not become local student validation."""
import csv,json,re,tempfile,unittest
from pathlib import Path
from units_coordination_evidence import ROOT,CSV,NOTES,build_report,kappa,rho

class PublishedRatingEvidence(unittest.TestCase):
 def test_published_results_and_sample_scope(self):
  report=build_report()
  self.assertEqual(report['reconciled_stage_counts'],{'1':10,'2':8,'3':2})
  self.assertEqual([p['exact_agreements'] for p in report['pair_agreement']],[15,16])
  self.assertFalse(report['local_student_validation']);self.assertFalse(report['independent_review'])
 def test_perfect_rank_association_is_not_exact_agreement(self):
  a=[1,1,2,2];b=[2,2,3,3]
  self.assertAlmostEqual(rho(a,b),1)
  self.assertLess(kappa(a,b),0)
 def fixture(self,root):
  for relative in [CSV,NOTES]:
   p=root/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/relative).read_bytes())
 def test_changed_transcription_is_rejected(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);self.fixture(root)
   p=root/CSV;s=p.read_text(encoding='utf-8');s=s.replace('1,2,2,2,2,2,','1,1,2,2,2,2,',1);self.assertNotEqual(s,p.read_text(encoding='utf-8'));p.write_text(s,encoding='utf-8')
   with self.assertRaises(AssertionError):build_report(root)
 def test_published_rows_cannot_be_relabelled_as_local_responses(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);self.fixture(root);p=root/CSV
   p.write_text(p.read_text(encoding='utf-8').replace('published_ratings_not_local_student_responses','local_responses'),encoding='utf-8')
   with self.assertRaises(AssertionError):build_report(root)
 def test_every_protocol_observation_is_current_and_still_unvalidated(self):
  registry=json.loads((ROOT/'data/literature_claim_reviews.json').read_text(encoding='utf-8'))
  ids=[p['id'] for s in registry['sources'].values() for p in s.get('observations',[])]
  protocol=(ROOT/'docs/분수단위조정관찰기록.md').read_text(encoding='utf-8')
  documented=set(re.findall(r'^\| ([A-Z][A-Z0-9]*-P\d+) \|',protocol,re.M))
  self.assertEqual(documented,set(ids))
  self.assertFalse(any(p['student_validated'] for s in registry['sources'].values() for p in s.get('observations',[])))
if __name__=='__main__':unittest.main()

"""Check attribution, exact source preservation and the teaching distinction."""
from pathlib import Path
from decimal import Decimal
import csv,hashlib,json,unittest
from source_economy_data import SOURCE,R,URL
class SourceDataTests(unittest.TestCase):
 def setUp(self):
  self.raw=json.loads(SOURCE.read_text(encoding='utf-8'),parse_float=Decimal)
  with (R/'data/teaching_examples/source-korea-gdp-growth.csv').open(encoding='utf-8',newline='') as f:self.rows=list(csv.DictReader(f))
 def test_exact_values_and_attribution(self):
  originals={r['date']:r['value'] for r in self.raw[1]}
  self.assertEqual([r['year'] for r in self.rows],list(map(str,range(2020,2025))))
  for r in self.rows:
   self.assertEqual(Decimal(r['value']),originals[r['year']]);self.assertEqual(r['source_url'],URL)
   self.assertEqual(r['data_kind'],'published_statistic');self.assertEqual(r['unit'],'percent_per_year')
 def test_frozen_source_integrity(self):
  meta=json.loads((SOURCE.parent/'world-bank-korea-gdp-growth-provenance.json').read_text(encoding='utf-8'))
  self.assertEqual(meta['raw_sha256'],hashlib.sha256(SOURCE.read_bytes()).hexdigest())
  self.assertEqual(meta['api_lastupdated'],self.raw[0]['lastupdated'])
  self.assertEqual(meta['license'],'CC BY 4.0')
 def test_growth_slowdown_is_not_level_decline(self):
  values={r['year']:Decimal(r['value']) for r in self.rows}
  self.assertGreater(values['2022'],0);self.assertLess(values['2022'],values['2021'])
  self.assertAlmostEqual(float(values['2022']-values['2021']),-1.88540338745296,places=10)
if __name__=='__main__':unittest.main()

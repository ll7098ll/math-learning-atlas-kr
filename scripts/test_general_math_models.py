import csv,math,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class FunctionExperiments(unittest.TestCase):
 def setUp(self):
  with (R/'data/teaching_examples/model-general-functions.csv').open(encoding='utf-8',newline='') as f:self.rows=list(csv.DictReader(f))
 def table(self,name):return [r for r in self.rows if r['function_id']==name]
 def test_model_provenance_and_undefined_inputs(self):
  self.assertTrue(all(r['data_kind']=='model_calculation' for r in self.rows))
  self.assertEqual(len(self.rows),len({(r['function_id'],r['x']) for r in self.rows}))
  for row in self.rows:self.assertEqual(row['y']=='',row['defined']=='false')
  for name,excluded in [('log_2',0),('log_half',0),('secant_square_at_1',0),('limit_hole',1)]:
   self.assertEqual(next(r for r in self.table(name) if float(r['x'])==excluded)['defined'],'false')
 def test_exponent_log_inverse_and_base_direction(self):
  for base in ['2','half']:
   logs={float(r['x']):float(r['y']) for r in self.table('log_'+base) if r['defined']=='true'}
   for row in self.table('exp_'+base):self.assertAlmostEqual(logs[float(row['y'])],float(row['x']))
  self.assertLess(float(self.table('exp_2')[0]['y']),float(self.table('exp_2')[-1]['y']))
  self.assertGreater(float(self.table('exp_half')[0]['y']),float(self.table('exp_half')[-1]['y']))
 def test_tangent_poles_are_not_joined(self):
  rows=self.table('tan')
  for index,row in enumerate(rows):
   k=int(row['parameter'].split('=')[1].split('*')[0])
   if k%4==2:
    self.assertEqual(row['defined'],'false')
    if 0<index<len(rows)-1:self.assertNotEqual(rows[index-1]['domain_component'],rows[index+1]['domain_component'])
  self.assertAlmostEqual(float(next(r['y'] for r in rows if r['parameter']=='x=1*pi/4')),1)
 def test_difference_quotient_and_hole(self):
  for row in self.table('secant_square_at_1'):
   if row['defined']=='true':self.assertAlmostEqual(float(row['y'])-2,float(row['x']))
  for row in self.table('limit_hole'):
   if row['defined']=='true':self.assertAlmostEqual(float(row['y']),float(row['x'])+1)
 def test_signed_integral_is_not_geometric_area(self):
  pts=[(float(r['x']),float(r['y'])) for r in self.table('signed_line') if -1<=float(r['x'])<=1]
  signed=sum((b[0]-a[0])*(a[1]+b[1])/2 for a,b in zip(pts,pts[1:]))
  area=sum((b[0]-a[0])*(abs(a[1])+abs(b[1]))/2 for a,b in zip(pts,pts[1:]))
  self.assertAlmostEqual(signed,0);self.assertAlmostEqual(area,1)
if __name__=='__main__':unittest.main()

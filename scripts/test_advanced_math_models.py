import csv,math,unittest
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(name):
 with (R/'data/teaching_examples'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
class AdvancedExperiments(unittest.TestCase):
 def test_partial_sums_and_rounding(self):
  rows=read('model-advanced-calculus.csv');self.assertTrue(all(r['data_kind']=='model_calculation' for r in rows))
  geometric={int(r['n']):F(r['exact_value']) for r in rows if r['object']=='geometric_partial'}
  for n,value in geometric.items():self.assertEqual(1-value,F(1,2**n))
  self.assertLess(geometric[64],1) # A decimal display of 1 is not exact equality.
  harmonic={int(r['n']):F(r['exact_value']) for r in rows if r['object']=='harmonic_partial'}
  for n in harmonic:
   if 2*n in harmonic:self.assertGreaterEqual(harmonic[2*n]-harmonic[n],F(1,2))
 def test_riemann_width_and_bounds(self):
  rows=read('model-advanced-calculus.csv')
  left={int(r['n']):F(r['exact_value']) for r in rows if r['object']=='riemann_left'}
  right={int(r['n']):F(r['exact_value']) for r in rows if r['object']=='riemann_right'}
  for n in left:
   self.assertEqual(right[n],F((n+1)*(2*n+1),6*n*n))
   self.assertEqual(right[n]-left[n],F(1,n))
   self.assertLess(left[n],F(1,3));self.assertGreater(right[n],F(1,3))
 def test_conic_focus_definitions(self):
  rows=read('model-geometry-tools.csv');self.assertTrue(all(r['data_kind']=='model_calculation' for r in rows))
  for r in rows:
   if r['object'] not in ('parabola','ellipse','hyperbola'):continue
   x,y=float(r['x']),float(r['y'])
   if r['object']=='parabola':self.assertAlmostEqual(math.hypot(x,y-1),y+1)
   if r['object']=='ellipse':self.assertAlmostEqual(math.hypot(x+3,y)+math.hypot(x-3,y),10)
   if r['object']=='hyperbola':self.assertAlmostEqual(abs(math.hypot(x+5,y)-math.hypot(x-5,y)),6)
  branches={r['domain_component'] for r in rows if r['object']=='hyperbola'}
  self.assertEqual(branches,{'left','right'})
 def test_sphere_sections(self):
  for r in read('model-geometry-tools.csv'):
   if r['object']!='sphere_section':continue
   if r['defined']=='false':
    self.assertEqual(float(r['z']),6);self.assertEqual(r['x'],'');continue
   x,y,z=map(float,(r['x'],r['y'],r['z']))
   self.assertAlmostEqual((x-1)**2+(y-2)**2+(z-3)**2,4)
 def test_projection_lengths_and_areas(self):
  rows=read('model-geometry-tools.csv')
  pts=lambda obj,component:[tuple(float(r[k]) for k in ('x','y','z')) for r in rows if r['object']==obj and r['domain_component']==component]
  length=lambda a,b:math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
  a,b=pts('projection_segment','spatial');self.assertAlmostEqual(length(a,b),6)
  a,b=pts('projection_segment','projected');self.assertAlmostEqual(length(a,b),3)
  a,b,_,d,_=pts('projection_rectangle','spatial')
  u=tuple(x-y for x,y in zip(b,a));v=tuple(x-y for x,y in zip(d,a))
  cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
  self.assertAlmostEqual(math.sqrt(sum(x*x for x in cross)),10)
  points=pts('projection_rectangle','projected')
  self.assertAlmostEqual(abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(points,points[1:])))/2,5)
 def test_decision_tolerance_boundary(self):
  error=lambda n:2-F(2*n+1,n+3)
  self.assertEqual(error(497),F(1,100));self.assertLess(error(498),F(1,100))
if __name__=='__main__':unittest.main()

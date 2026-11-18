"""Exact finite-sequence witnesses and geometric model coordinates for tools."""
import csv,math
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def calculus_rows():
 rows=[]
 for n in [1,2,3,4,8,16,32,64]:
  values={'reciprocal':F(1,n),'unbounded':F(n),'alternating':F((-1)**n),
   'shrinking_oscillation':1+F((-1)**n,n),'geometric_partial':1-F(1,2**n),
   'harmonic_partial':sum((F(1,k) for k in range(1,n+1)),F(0)),
   'riemann_left':sum((F(k*k,n**3) for k in range(n)),F(0)),
   'riemann_right':sum((F(k*k,n**3) for k in range(1,n+1)),F(0))}
  for name,value in values.items():rows.append(dict(data_kind='model_calculation',object=name,n=n,value=float(value),exact_value=str(value),note='finite exact rational model; decimal display may round; finite observations are not a convergence proof'))
 return rows
def geometry_rows():
 rows=[]
 def add(obj,label,x,y,z=0,component='0',note=''):
  rows.append(dict(data_kind='model_calculation',object=obj,point_id=label,x='' if x is None else float(x),y='' if y is None else float(y),z=float(z),defined='false' if x is None else 'true',domain_component=component,note=note))
 for k,t in enumerate(map(F,[-4,-2,0,2,4])):add('parabola',str(k),t,t*t/4,note='x^2=4y; focus (0,1); directrix y=-1; selected points')
 add('ellipse','0',-5,0,note='x^2/25+y^2/16=1; foci (+/-3,0)')
 for k,t in enumerate([F(-2),F(-1),F(-1,2),F(0),F(1,2),F(1),F(2)],1):add('ellipse',str(k),5*(1-t*t)/(1+t*t),8*t/(1+t*t),note='selected rational points; foci (+/-3,0), distance sum 10')
 add('ellipse','8',-5,0,note='closure point; not a claim that a point plot proves the locus')
 for sign,component in [(-1,'left'),(1,'right')]:
  for k,t in enumerate([F(-3,4),F(-1,2),F(0),F(1,2),F(3,4)]):add('hyperbola',component+str(k),sign*3*(1+t*t)/(1-t*t),8*t/(1-t*t),component=component,note='x^2/9-y^2/16=1; do not connect the two branches')
 for z in [3,4,5,6]:
  r2=4-(z-3)**2
  if r2<0:add('sphere_section',str(z),None,None,z,component='none',note='plane does not meet sphere');continue
  angles=[0] if r2==0 else [0,math.pi/2,math.pi,3*math.pi/2,2*math.pi]
  for k,angle in enumerate(angles):add('sphere_section',f'{z}-{k}',1+math.sqrt(r2)*math.cos(angle),2+math.sqrt(r2)*math.sin(angle),z,component='z='+str(z),note='center (1,2,3), radius 2; decimal coordinates approximate')
 for component,points in [('spatial',[(0,0,0),(3,0,3*math.sqrt(3))]),('projected',[(0,0,0),(3,0,0)])]:
  for k,(x,y,z) in enumerate(points):add('projection_segment',str(k),x,y,z,component=component,note='xy-plane projection; original length 6, angle 60 degrees')
 original=[(0,0,0),(2,0,0),(2,2.5,2.5*math.sqrt(3)),(0,2.5,2.5*math.sqrt(3)),(0,0,0)]
 for component in ['spatial','projected']:
  for k,(x,y,z) in enumerate(original):add('projection_rectangle',str(k),x,y,z if component=='spatial' else 0,component=component,note='original rectangle area 10; xy-plane projection area 5')
 return rows
def build():
 for filename,rows in [('model-advanced-calculus.csv',calculus_rows()),('model-geometry-tools.csv',geometry_rows())]:
  with (R/'data/teaching_examples'/filename).open('w',encoding='utf-8',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
  print(filename,len(rows))
if __name__=='__main__':build()

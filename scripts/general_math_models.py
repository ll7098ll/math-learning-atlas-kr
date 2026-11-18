"""Generate reusable function/limit experiments, explicitly model calculations."""
import csv,math
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parents[1]
FIELDS=['data_kind','function_id','x','y','defined','domain_component','parameter','meaning']
def rows():
 out=[]
 def add(name,x,y,component='0',parameter='',meaning=''):
  out.append(dict(data_kind='model_calculation',function_id=name,x=x,y='' if y is None else y,defined='false' if y is None else 'true',domain_component=component,parameter=parameter,meaning=meaning))
 for base,label in [(2,'2'),(.5,'half')]:
  for x in [-2,-1,0,1,2,3]:add('exp_'+label,x,base**x,parameter='base='+str(base),meaning='y=base^x')
  for x in [0,.125,.25,.5,1,2,4,8]:add('log_'+label,x,None if x<=0 else math.log(x,base),parameter='base='+str(base),meaning='y=log_base(x); x>0')
 for k in range(-4,9):
  x=k*math.pi/4
  add('sin',x,math.sin(x),parameter=f'x={k}*pi/4',meaning='angle in radians')
  add('cos',x,math.cos(x),parameter=f'x={k}*pi/4',meaning='angle in radians')
  pole=k%4==2
  add('tan',x,None if pole else math.tan(x),component='' if pole else str((k+2)//4),parameter=f'x={k}*pi/4',meaning='do not connect different domain components')
 for h in map(Fraction,['-1','-0.5','-0.1','-0.01','-0.001','0','0.001','0.01','0.1','0.5','1']):
  add('secant_square_at_1',float(h),None if h==0 else float(((1+h)**2-1)/h),component='left' if h<0 else 'right' if h>0 else '',meaning='x column is h; y=[(1+h)^2-1]/h; h!=0')
 for x in [-1,-.5,0,.5,1,1.5,2]:
  add('signed_line',x,x,meaning='y=x; signed integral and geometric area differ')
 for x in [0,.5,.9,.99,1,1.01,1.1,1.5,2]:
  add('limit_hole',x,None if x==1 else x+1,component='left' if x<1 else 'right' if x>1 else '',meaning='y=(x^2-1)/(x-1); x!=1')
 return out
def build():
 target=R/'data/teaching_examples/model-general-functions.csv'
 with target.open('w',encoding='utf-8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows(rows())
 print('Model calculation rows:',len(rows()))
if __name__=='__main__':build()

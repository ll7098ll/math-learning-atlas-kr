"""Reproduce small fictional economy/AI course examples with standard Python.

python economy-ai-models.py model-ai-regression.csv
Numbers are task-defined models, not current rates or a deployed AI system.
"""
from math import sqrt
import csv,json,sys

def fit_origin(points):
    denominator=sum(x*x for x,y in points)
    if denominator==0:raise ValueError('nonzero input energy required')
    return sum(x*y for x,y in points)/denominator
def fit_affine(points):
    n=len(points)
    if n<2:raise ValueError('at least two points required')
    mx=sum(x for x,y in points)/n;my=sum(y for x,y in points)/n
    d=sum((x-mx)**2 for x,y in points)
    if d==0:raise ValueError('distinct x values required')
    slope=sum((x-mx)*(y-my) for x,y in points)/d
    return slope,my-slope*mx
def loss(points,a):return sum((a*x-y)**2 for x,y in points)
def descent(points,eta,steps=6,start=0.):
    if eta<=0 or steps<0:raise ValueError('positive learning rate and nonnegative steps required')
    coefficient=start;rows=[]
    for k in range(steps+1):
        gradient=2*sum(x*(coefficient*x-y) for x,y in points)
        rows.append(dict(step=k,coefficient=coefficient,loss=loss(points,coefficient),gradient=gradient))
        coefficient-=eta*gradient
    return rows
def cosine_components(u,v):
    if len(u)!=len(v):raise ValueError('same coordinates required')
    length1=sqrt(sum(x*x for x in u));length2=sqrt(sum(x*x for x in v))
    if not length1 or not length2:raise ValueError('zero vector requires separate handling')
    return sum(x*y for x,y in zip(u,v))/(length1*length2)
def run(filename):
    with open(filename,encoding='utf-8-sig',newline='') as f:points=[(float(r['x']),float(r['y'])) for r in csv.DictReader(f)]
    slope=fit_origin(points);affine=fit_affine(points)
    return dict(data_kind='fictional_teaching_model',origin_fit=dict(slope=slope,loss=loss(points,slope)),
        affine_comparison_only=dict(slope=affine[0],intercept=affine[1],scope='trendline comparison, outside the one-variable y=ax loss task'),
        stable_descent=descent(points,1/56),large_step_descent=descent(points,.1),
        annuity_three_end_payments=sum(10/1.1**k for k in range(1,4)),cosine_example=cosine_components([1,1],[2,0]))
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python economy-ai-models.py model-ai-regression.csv')
    print(json.dumps(run(sys.argv[1]),ensure_ascii=False,indent=2))

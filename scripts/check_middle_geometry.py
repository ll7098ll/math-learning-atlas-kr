"""Exact and geometric witnesses for the authored middle geometry cohort."""
from fractions import Fraction as F
from itertools import combinations,product
from math import sin,cos,tan,radians,acos,degrees,sqrt,isclose
from pathlib import Path
import json
from goal_hierarchy import load_goal_hierarchies

root=Path(__file__).resolve().parents[1]
standards=json.loads((root/'data/standards.json').read_text(encoding='utf-8'))['standards']
entries,cases,goals=load_goal_hierarchies(standards)
codes={'9수03-'+str(i).zfill(2) for i in range(1,20)}
selected={code:entries[code] for code in codes}
cohort=[case for case in cases if case['standard'] in codes]
by_case={case['id']:case for case in cohort}
assert len(selected)==19 and sum(len(e['goals']) for e in selected.values())==38 and len(cohort)==32
assert len([s for s in standards if s['code'].startswith('9수')])==60
assert all(s['code'] in entries for s in standards if s['code'].startswith('9수'))
assert all(e['source_review']['pdf_pages']==[43,44,45,46] for e in selected.values())
assert all(e['history'] for e in selected.values())
proof=by_case['early-9수03-15-proof']
assert not any(s.get('goal_id')=='9수03-14:ratios' for r in proof['routes'] for s in r['condition_sources'])
assert any(s['kind']=='within_task' and 'p+q' in r['conditions'][s['condition_index']] for r in proof['routes'] for s in r['condition_sources'])
rotation=by_case['early-9수03-07-rotate']
assert {'6수03-07:cylinder','6수03-07:cone','6수03-07:sphere'}<={s.get('goal_id') for r in rotation['routes'] for s in r['condition_sources']}
volume=by_case['early-9수03-08-prisms-pyramids']
assert {'6수03-18:units','6수03-19:cuboid'}<={s.get('goal_id') for r in volume['routes'] for s in r['condition_sources']}

def sub(p,q):return tuple(a-b for a,b in zip(p,q))
def dot(p,q):return sum(a*b for a,b in zip(p,q))
def sq(p):return dot(p,p)
def distance_sq(p,q):return sq(sub(p,q))
def polygon_area(points):
    return abs(sum(points[i][0]*points[(i+1)%len(points)][1]-points[(i+1)%len(points)][0]*points[i][1] for i in range(len(points))))/F(2)

# A cube's skew pair has no common point and no common plane.
ab=(1,0,0);cg=(0,0,1);offset=(1,1,0)
cross=(ab[1]*cg[2]-ab[2]*cg[1],ab[2]*cg[0]-ab[0]*cg[2],ab[0]*cg[1]-ab[1]*cg[0])
assert dot(cross,offset)!=0 and dot((1,0,0),(0,1,0))==0
assert 180-65==115 and 180-50-60==70 and 50+60==110
assert 3+4>5 and 3+4<8 and 3+4==7
assert 180-40-60==80 and (180-40)/2==70

polygon_witnesses=0
for n in range(3,51):
    assert (n-2)*180==n*180-360
    assert n*180-(n-2)*180==360
    diagonals={pair for pair in combinations(range(n),2) if (pair[1]-pair[0]) not in (1,n-1)}
    assert len(diagonals)==n*(n-3)//2
    polygon_witnesses+=1
assert (5-2)*180==540 and 540/5==108 and 360/5==72
assert F(60,360)*2*6==2 and F(60,360)*6**2==6
assert F(60,360)*2*12==4 and F(60,360)*12**2==24

platonic=[(4,6,4,3,3),(6,12,8,4,3),(8,12,6,3,4),(12,30,20,5,3),(20,30,12,3,5)]
for faces,edges,vertices,p,q in platonic:
    assert faces*p==2*edges==vertices*q and vertices-edges+faces==2
for n in range(3,13):
    assert 2*n-3*n+(n+2)==2  # n-gonal prism.
    assert (n+1)-2*n+(n+1)==2  # n-gonal pyramid.
assert 2*(2*3+3*4+4*2)==52 and 2*3*4==24
assert 6**2+4*(6*5/2)==96 and F(6**2*4,3)==48
assert 2*3**2+2*3*4==42 and 3**2*4==36
assert 3**2+3*5==24 and F(3**2*4,3)==12
assert 4*3**2==36 and F(4*3**3,3)==36

center_witnesses=0
for height in range(1,31):
    a=(-3,0);b=(3,0);cc=(0,height);o=(0,F(height**2-9,2*height))
    assert distance_sq(o,a)==distance_sq(o,b)==distance_sq(o,cc)
    if height==3:assert o==(0,0)
    if height<3:assert o[1]<0
    k=F(height);i=(k,k)
    assert i[0]==i[1]==abs(3*i[0]+4*i[1]-12*k)/5
    foot=(F(8,5)*k,F(9,5)*k)
    assert 3*foot[0]+4*foot[1]==12*k and distance_sq(i,foot)==k*k
    assert 0<foot[0]<4*k and 0<foot[1]<3*k
    center_witnesses+=1

quad_witnesses=0
for a,b in product(range(1,21),repeat=2):
    rect=[(0,0),(a,0),(a,b),(0,b)]
    assert distance_sq(rect[0],rect[2])==distance_sq(rect[1],rect[3])
    rhomb=[(-a,0),(0,b),(a,0),(0,-b)]
    assert len({distance_sq(rhomb[i],rhomb[(i+1)%4]) for i in range(4)})==1
    assert dot(sub(rhomb[2],rhomb[0]),sub(rhomb[3],rhomb[1]))==0
    quad_witnesses+=1
trap=[(-2,0),(2,0),(1,1),(-1,1)]
assert distance_sq(trap[0],trap[2])==distance_sq(trap[1],trap[3])
assert tuple(F(trap[0][j]+trap[2][j],2) for j in range(2))!=tuple(F(trap[1][j]+trap[3][j],2) for j in range(2))
assert F(2,4)==F(3,6)==F(1,2) and 2*3*4==24 and 4*6*8==192
assert 2*(4*6+6*8+8*4)==4*52
assert F(3,6)==F(4,8)==F(5,10)==F(1,2) and 8*F(3,2)==12
assert not isclose(2**2+3**2-2*2*3*cos(radians(50)),2**2+3**2-2*2*3*cos(radians(80)))
assert F(2,6)==F(3,9)==F(4,12) and F(2,4)==F(3,6)!=F(2,6)
for k in range(-10,11):
    # Horizontal parallels y=0,2,6, transversals x=0 and x=k*y+1.
    d=(1,0);e=(2*k+1,2);f=(6*k+1,6)
    assert distance_sq(d,e)/F(distance_sq(e,f))==F(1,4)

tile_witnesses=0
for av,bv in product(range(1,21),repeat=2):
    a,b=F(av),F(bv);side=a+b
    p,q,rr,s=(a,0),(side,a),(b,side),(0,b)
    central=[p,q,rr,s]
    sides=[sub(central[(i+1)%4],central[i]) for i in range(4)]
    assert all(sq(v)==a*a+b*b for v in sides)
    assert all(dot(sides[i],sides[(i+1)%4])==0 for i in range(4))
    tiles=[[(0,0),p,s],[(side,0),q,p],[(side,side),rr,q],[(0,side),s,rr]]
    assert all(polygon_area(t)==a*b/2 for t in tiles)
    assert polygon_area(central)+sum(polygon_area(t) for t in tiles)==side**2
    assert all(0<=x<=side and 0<=y<=side for x,y in central)
    tile_witnesses+=1
p,q=F(16,5),F(9,5);height=F(12,5)
assert p+q==5 and p*p+height*height==16 and q*q+height*height==9
assert 3**2==5*q and 4**2==5*p
assert 5**2+12**2==13**2 and 2**2+3**2!=4**2
visual=by_case['early-9수03-15-proof']['visual']
assert visual['kind']=='pythagoras_tiles' and (visual['a'],visual['b'],visual['c'])==(3,4,5)
assert visual['a']**2+visual['b']**2==visual['c']**2

expected={30:(F(1,2),sqrt(3)/2,sqrt(3)/3),45:(sqrt(2)/2,sqrt(2)/2,1),60:(sqrt(3)/2,F(1,2),sqrt(3))}
for angle,values in expected.items():
    actual=[sin(radians(angle)),cos(radians(angle)),tan(radians(angle))]
    assert all(isclose(x,float(y),abs_tol=1e-12) for x,y in zip(actual,values))
assert round(1.5+10*sqrt(3)/3,2)==7.27 and 8*F(1,2)==4 and 10*4/2==20
assert 4*sqrt(3)<10 and F(3,5)==F(9,15) and F(3,4)==F(9,12)
assert 2*sqrt(25-9)==8 and 2*sqrt(25-16)==6 and sqrt(169-25)==12

tangent_witnesses=0
for u,v in product(range(-5,6),repeat=2):
    if u==0:continue
    point=(F(5),F(0));direction=(u,v);param=-dot(point,direction)/F(sq(direction))
    foot=tuple(point[j]+param*direction[j] for j in range(2))
    other=tuple(2*foot[j]-point[j] for j in range(2))
    assert other!=point and sq(other)==25
    assert (other[0]-point[0])*v==(other[1]-point[1])*u
    tangent_witnesses+=1
for v in range(1,51):assert distance_sq((5,v),(0,0))>25

def circlepoint(angle):return (cos(radians(angle)),sin(radians(angle)))
inscribed_witnesses=0
for aa in range(0,360,30):
    for delta in range(30,360,30):
        bb=(aa+delta)%360
        for cc in range(0,360,15):
            if cc in (aa,bb):continue
            aa_point,bb_point,cc_point=map(circlepoint,[aa,bb,cc])
            u,v=sub(aa_point,cc_point),sub(bb_point,cc_point)
            angle=degrees(acos(max(-1,min(1,dot(u,v)/sqrt(sq(u)*sq(v))))))
            intercepted=360-delta if 0<(cc-aa)%360<delta else delta
            assert isclose(2*angle,intercepted,abs_tol=1e-8),(aa,bb,cc,angle,intercepted)
            inscribed_witnesses+=1
assert 80/2==40 and 280/2==140 and 180/2==90

graph={goal:set() for goal in goals};refs=siblings=0
for case in cases:
    for route in case['routes']:
        for source in route['condition_sources']:
            if source['kind']!='goal':continue
            for target in source.get('applies_to_goal_ids',case['goal_ids']):graph[source['goal_id']].add(target)
            if case['standard'] in codes:
                refs+=1;siblings+=source['goal_id'].split(':')[0]==case['standard']
active=set();done=set()
def visit(node):
    assert node not in active,'Conditional goal reference cycle: '+node
    if node in done:return
    active.add(node)
    for target in graph[node]:visit(target)
    active.remove(node);done.add(node)
for node in graph:visit(node)
area_route=by_case['early-9수03-15-proof']['routes'][0]
assert not any(s.get('goal_id','').startswith('9수03-13:') for s in area_route['condition_sources'])
assert not any(s.get('goal_id','').startswith(('9수03-15:','9수03-16:','9수03-18:')) for r in by_case['early-9수03-19-diameter-proof']['routes'] for s in r['condition_sources'])
assert '정의하지 않는다' in by_case['early-9수03-16-special-values']['routes'][0]['result']
legacy=json.loads((root/'data/revisions_middle.json').read_text(encoding='utf-8'))
for code in ['9수03-02','9수03-09']:
    assert legacy[code]['scopeCorrections'][-1]['previous_conditions']
    assert all('가정' not in s and '결론' not in s for s in legacy[code]['conditions'])
print(json.dumps(dict(status='pass',standards=19,goals=38,cases=32,middle_goal_standards=60,scoped_goal_references=refs,sibling_condition_references=siblings,polygon_witnesses=polygon_witnesses,center_witnesses=center_witnesses,quadrilateral_witnesses=quad_witnesses,tile_witnesses=tile_witnesses,tangent_witnesses=tangent_witnesses,inscribed_angle_witnesses=inscribed_witnesses,checks='construction existence; convex polygon counts; solid incidence; areas and units; centers and distances; diagonal scope; similarity correspondence; area tiling; special-angle values; tangent reflection; inscribed arc selection; acyclic goal references; retained source corrections')))

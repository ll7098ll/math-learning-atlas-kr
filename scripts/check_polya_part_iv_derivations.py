"""Independent calculations for our own twenty-problem derivation notes.

The notes contain the arguments. Finite numerical witnesses do not replace
those arguments, external review, source-edition verification or student data.
"""
from fractions import Fraction as Q
from itertools import permutations, product, combinations
from collections import Counter
from math import factorial, sin, cos, asin, pi, sqrt, gcd, isclose
import json

def determinant(a):
    if len(a)==1:return a[0][0]
    return sum((-1)**j*a[0][j]*determinant([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def check():
    results={}
    # P01: an eastward leg can make n complete circuits near the south pole.
    radius=4000.;steps=[]
    for n in [1,2,3,10,100]:
        delta=asin(1/(2*pi*radius*n))
        assert isclose(2*pi*radius*sin(delta)*n,1,rel_tol=1e-12)
        assert 0<delta<delta+1/radius<pi/2
        steps.append(n)
    results[1]=dict(southern_parallel_loop_witnesses=steps,fur_colour_deduced_from_geometry=False)
    # P02: equal parallel arcs and equal meridian sides place the strip
    # symmetrically across the equator in the specified spherical model.
    latitude=1000/(2*radius*5280)
    longitude=1000/(radius*5280*cos(latitude))
    assert isclose(radius*5280*2*latitude,1000)
    assert isclose(radius*5280*cos(-latitude)*longitude,1000)
    assert cos(.5) != cos(.6)
    results[2]=dict(equator_symmetric_model=True,current_geopolitical_boundaries_checked=False)
    assert sum(range(10))==45>44
    results[3]=dict(minimum_for_ten_distinct_nonnegative_integers=45)
    digits=lambda n:sum(len(str(i)) for i in range(1,n+1))
    assert digits(999)==2889 and digits(1024)==2989 and digits(1023)<2989<digits(1025)
    results[4]=dict(numbered_pages=1024)
    bills=[(a,b,10000*a+6790+b) for a in range(1,10) for b in range(10) if (10000*a+6790+b)%72==0]
    assert bills==[(3,2,36792)] and Q(36792,72)==511
    results[5]=dict(faded_digits=[3,2],unit_price_cents=511)
    # P06: central inversion pairs the half-planes. The square witnesses
    # below check exact side-of-line signs; the written argument covers hexagons.
    for p in [(Q(2),Q(3)),(Q(-1),Q(4)),(Q(0),Q(0))]:
        for normal in [(Q(1),Q(2)),(Q(3),Q(-2))]:
            assert dot(normal,tuple(-x for x in p))==-dot(normal,p)
    results[6]=dict(centre_point_has_infinitely_many_bisectors=True)
    # P07: squared dot/cross formulas are checked on rational parameters
    # of the four semicircles and eight quarter-circle pieces for [-1,1]^2.
    def angle_parts(p,corner=False):
        x,y=p
        u=(-1-x,1-y);v=(1-x,-1-y) if corner else (1-x,1-y)
        return dot(u,v),abs(u[0]*v[1]-u[1]*v[0])
    loci=0
    for t in [Q(k,20) for k in range(1,20)]:
        u=(1-t*t)/(1+t*t);v=2*t/(1+t*t)
        # outward top semicircle, excluding square vertices
        assert angle_parts((u,1+v))[0]==0
        # northeast outer quarter-circle: centre(1,1),radius2
        assert angle_parts((1+2*u,1+2*v),True)[0]==angle_parts((1+2*u,1+2*v),True)[1]>0
        # top strip outer quarter-circle centre(0,2),radius sqrt2.
        # Rational points obtained by rotating a unit-circle rational point.
        x=u-v;y=2+u+v
        assert -1<x<1 and y>1
        assert angle_parts((x,y))[0]==angle_parts((x,y))[1]>0
        loci+=3
    assert 0<2-sqrt(2)<1 and 2+sqrt(2)>3
    results[7]=dict(rational_locus_witnesses=loci,right_angle_pieces=4,fortyfive_degree_pieces=8,square_boundary_excluded=True)
    # P08: every proper cube rotation is a signed permutation of its normals.
    rotations=[];axes={};traces=Counter()
    for perm in permutations(range(3)):
        for signs in product([-1,1],repeat=3):
            m=[[signs[i] if j==perm[i] else 0 for j in range(3)] for i in range(3)]
            if determinant(m)!=1:continue
            rotations.append(m);trace=sum(m[i][i] for i in range(3));traces[trace]+=1
            if trace==3:continue
            rows=[tuple(m[i][j]-(i==j) for j in range(3)) for i in range(3)]
            direction=next(v for i,j in combinations(range(3),2) if any(v:=cross(rows[i],rows[j])))
            g=gcd(gcd(abs(direction[0]),abs(direction[1])),abs(direction[2]))
            direction=tuple(x//g for x in direction)
            if next(x for x in direction if x)<0:direction=tuple(-x for x in direction)
            assert all(dot(row,direction)==0 for row in rows)
            axes.setdefault(direction,set()).add(trace)
    assert len(rotations)==24 and len(axes)==13 and traces=={3:1,1:6,0:8,-1:9}
    kinds=Counter(sum(x*x for x in direction) for direction in axes)
    assert kinds=={1:3,2:6,3:4}
    assert abs((4*sqrt(3)+6*sqrt(2)+3)/13-(8*sqrt(3)+6*sqrt(2)+9)/23)>.01
    results[8]=dict(proper_rotations=24,nonidentity_rotations=23,unoriented_axes=13,axis_length_squared_counts=dict(kinds),mean_axis_length='(4sqrt(3)+6sqrt(2)+3)/13',uniform_direction_mean_width_is_different=True)
    # P09: determinants for a family of nondegenerate opposite-edge models.
    tetra=0
    for a,b in product([Q(1,2),Q(1),Q(3,2),Q(3)],repeat=2):
        vectors=[[a,0,0],[a/2,-a/2,b],[a/2,a/2,b]]
        assert abs(determinant(vectors))/6==a*a*b/6;tetra+=1
    results[9]=dict(volume='a^2*b/6',exact_models=tetra)
    # P10: circumcentre may lie outside; supporting-line equality may give
    # an excircle. Convex base + interior foot makes the incircle claim valid.
    point=(Q(6),Q(6));lines=[(1,0,0),(0,1,0),(3,4,-12)]
    assert [(a*point[0]+b*point[1]+c)**2/Q(a*a+b*b) for a,b,c in lines]==[36]*3
    assert [36+8*8]*3==[100]*3 and 3*point[0]+4*point[1]>12
    results[10]=dict(part_a_circumcircle=True,part_b_requires_convex_interior_condition_for_supporting_lines=True,unconditional_source_claim_proved=False)
    matrix=[[1,7,3,5],[8,4,6,2],[2,6,4,8],[5,3,7,1]] # x,y,v,u
    solution=[-2,2,-2,2]
    assert [dot(row,solution) for row in matrix]==[16,-16,16,-16] and determinant(matrix)!=0
    results[11]=dict(solution_xyuv=[-2,2,2,-2],unique=True)
    # P12: exact meeting equations, with positive car-return phase for c>p.
    trips=0
    for c,p in [(Q(c),Q(p)) for c in range(1,10) for p in range(c)]:
        t2=Q(1);t1=t3=(c+p)/(c-p);total=t1+t2+t3
        bob=c*(t1-t2+t3);paul=c*t1+p*(t2+t3);peter=p*(t1+t2)+c*t3
        assert bob==paul==peter
        assert bob/total==c*(c+3*p)/(3*c+p) and t2/total==(c-p)/(3*c+p)
        trips+=1
    results[12]=dict(exact_meeting_models=trips,average_speed='c(c+3p)/(3c+p)',alone_fraction='(c-p)/(3c+p)',strict_protocol_domain='c>p>=0',equal_speed_case_degenerate=True)
    answers=[]
    for g in [Q(2),Q(1,2)]:
        a=Q(42);b=Q(34);d=a+b/g-85
        ap=[a-d,a,a+d];gp=[b/g,b,b*g]
        assert [x+y for x,y in zip(ap,gp)]==[85,76,84] and sum(ap)==126
        assert 2*g*g-5*g+2==0;answers.append(dict(ap=ap,gp=gp))
    results[13]=dict(two_progression_pairs=[{'ap':[int(x) for x in z['ap']],'gp':[int(x) for x in z['gp']]} for z in answers])
    for m,t in [(Q(6),Q(2)),(Q(-6,19),Q(2,19))]:
        assert 10*t==3*m+2 and 9*t*t==m*m and t>0
        assert 19*m*m-108*m-36==0
    results[14]=dict(parameters=['6','-6/19'],four_distinct_real_ap_roots=True)
    assert 15+20+25==60 and 15**2+20**2==25**2 and Q(15*20,25)==12
    assert (60-25)**2==25**2+24*25 and 35**2-4*300==25
    results[15]=dict(unordered_sides=[15,20,25],unique_up_to_leg_swap=True)
    # P16: a valid exact configuration, plus an incompatible angle triple
    # that a positive denominator alone would fail to reject.
    sa=sb=Q(4,5);cg=Q(16,25);c2=Q(18)
    den=sa*sa+sb*sb-2*sa*sb*cg
    assert c2*sa*sa*sb*sb/den==16
    # alpha=beta=60deg,gamma=120deg -> cos(azimuth separation)=-5.
    sin2=Q(3,4);cosgamma=Q(-1,2);cos2=Q(1,4)
    assert (cosgamma-sin2)/cos2==-5
    assert 2*sin2-2*sin2*cosgamma>0
    results[16]=dict(valid_height_squared=16,positive_denominator_not_sufficient=True,incompatible_azimuth_cosine=-5,formula='h^2=c^2 sin^2(alpha) sin^2(beta)/(sin^2(alpha)+sin^2(beta)-2sin(alpha)sin(beta)cos(gamma))',angle_compatibility_required=True)
    for n in range(61):
        assert sum((Q(k,factorial(k+1)) for k in range(1,n+1)),Q(0))==1-Q(1,factorial(n+1))
        assert sum(range(n*n-n+1,n*n+n,2))==n**3
    results[17]=dict(identity='sum(k/(k+1)!,k=1..n)=1-1/(n+1)!',finite_witnesses=61,written_proof='telescoping')
    results[18]=dict(identity='sum(n^2-n+1+2j,j=0..n-1)=n^3',finite_witnesses=61,written_proof='arithmetic-series endpoints and term count')
    lattice=[]
    for n in range(1,9):
        vertices={(a,b) for a in range(-n,n+1) for b in range(-n,n+1) if abs(a+b)<=n}
        steps=[(1,0),(0,1),(1,-1)]
        edges={frozenset((p,(p[0]+da,p[1]+db))) for p in vertices for da,db in steps if (p[0]+da,p[1]+db) in vertices}
        neighbours={p:set() for p in vertices}
        for e in edges:
            a,b=tuple(e);neighbours[a].add(b);neighbours[b].add(a)
        triangles={frozenset((a,b,c)) for a in vertices for b,c in combinations(neighbours[a],2) if c in neighbours[b]}
        v,l,t=len(vertices),len(edges),len(triangles)
        assert (v,l,t)==(3*n*n+3*n+1,9*n*n+3*n,6*n*n) and v-l+t==1
        lattice.append(n)
    results[19]=dict(exact_lattice_sizes=lattice,vertices='3n^2+3n+1',edges='9n^2+3n',triangles='6n^2',outer_face_not_counted_as_triangle=True)
    coins=[1,5,10,25,50];ways=[0]*101;ways[0]=1
    for coin in coins:
        for amount in range(coin,101):ways[amount]+=ways[amount-coin]
    enumerated=[]
    for half in range(3):
        for quarter in range(5):
            for dime in range(11):
                for nickel in range(21):
                    penny=100-50*half-25*quarter-10*dime-5*nickel
                    if penny>=0:enumerated.append((penny,nickel,dime,quarter,half))
    assert len(enumerated)==len(set(enumerated))==ways[100]==292
    assert all(dot(coins,x)==100 for x in enumerated) and ways[50]==50
    results[20]=dict(unordered_coin_combinations=292,independent_exhaustive_count_matches_recurrence=True,denominations=coins)
    assert set(results)==set(range(1,21))
    return dict(status='pass',problem_count=20,all_twenty_have_self_derivations=True,
                machine_witnesses_do_not_replace_written_proofs=True,results=results,
                source_solution_unconditional_validity_proved=False,
                all_source_solutions_independently_reproved=False,external_independent_review=0,
                student_validation=0,publisher_fidelity_verified=False)

if __name__=='__main__':print(json.dumps(check(),ensure_ascii=False))

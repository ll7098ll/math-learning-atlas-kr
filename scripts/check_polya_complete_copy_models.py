"""Own exact domain counterexamples and selected source-example recalculations.

These do not independently reprove every solution or validate any learner.
"""
from fractions import Fraction as Q
from math import factorial,isqrt,prod
import json

def check():
 # Unsigned decimal concatenations preserve the sum of digits modulo 9.
 assert 10%9==1 and sum(range(10))%9==0 and 100%9==1
 signed=[70,9,8,6,5,3,2,1,-4]
 assert sum(signed)==100 and sorted(''.join(str(abs(n)) for n in signed))==list('0123456789')
 def reflect(point,line):
  a,b,c=map(Q,line);x,y=map(Q,point);den=a*a+b*b;assert den>0
  d=(a*x+b*y+c)/den
  return x-2*d*a,y-2*d*b
 for p,line,expected in [((3,5),(0,1,-2),(3,-1)),((6,-1),(1,0,-4),(2,-1)),((3,2),(0,1,-2),(3,2)),((2,5),(1,-1,0),(5,2))]:
  image=reflect(p,line);assert image==expected and reflect(image,line)==p
  a,b,c=map(Q,line);mid=tuple((Q(x)+y)/2 for x,y in zip(p,image));assert a*mid[0]+b*mid[1]+c==0
 # Arithmetic in Q(sqrt(177)) validates both positive source prism branches.
 def add(x,y):return x[0]+y[0],x[1]+y[1]
 def mul(x,y):return x[0]*y[0]+177*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
 def scale(x,k):return x[0]*k,x[1]*k
 zero=(Q(0),Q(0));one=(Q(1),Q(0))
 for x,y in [((Q(3),Q(0)),(Q(7),Q(0))),((Q(-3,2),Q(1,2)),(Q(93,56),Q(3,56)))]:
  assert mul(mul(x,x),y)==(63,0)
  assert add(scale(mul(x,x),2),scale(mul(x,y),4))==(102,0)
  assert add(add(mul(mul(x,x),x),scale(x,-51)),(126,0))==zero
 assert 13**2<177<14**2 # second x in (5,11/2), third (-3-sqrt177)/2 negative
 # (x-3)(x²+3x-42)=x³-51x+126; no omitted positive roots.
 assert [-3*(-42),-42-9,3-3,1]==[126,-51,0,1]
 def closest(r,v):
  r=tuple(map(Q,r));v=tuple(map(Q,v));vv=sum(x*x for x in v)
  if not vv:return None,sum(x*x for x in r)
  t=max(Q(0),-sum(x*y for x,y in zip(r,v))/vv)
  return t,sum((x+t*y)**2 for x,y in zip(r,v))
 assert closest((1,1),(1,0))==(0,2)
 assert closest((1,1),(-1,0))==(1,1)
 assert closest((1,1),(0,0))==(None,2)
 assert sum((Q(x)-y)**2 for x,y in zip((1,1),(1,0)))==1 # full-line t=-1,excluded for future
 sides=[Q(13),Q(13),Q(24)];s=sum(sides)/2;area=Q(60)
 assert area**2==s*prod(s-x for x in sides) and all(sum(sides)-2*x>0 for x in sides)
 r=area/s;radius=prod(sides)/(4*area);height=max(2*area/x for x in sides)
 assert (r,radius,height)==(Q(12,5),Q(169,10),Q(120,13)) and r+radius>height
 possible=lambda a,c,b,d:a>c>0 and abs(b-d)<a-c<b+d
 assert possible(10,4,5,5) and not possible(10,7,6,3) and not possible(10,10,5,3)
 assert 5**2-3**2==4**2 and (10+4)*4/2==28
 assert 3**2+4**2==0**2+5**2==25 and 10*4!=10*5 # equal-base parallelograms not unique
 # Quadratic examples distinguish the real domain and multiplicity conventions.
 assert (1-1)**2==0 and complex(0,1)**2+1==complex(0,-1)**2+1==0
 # SourceP10(b): equal distances to side-supporting lines give an excircle if
 # the altitude foot lies outside. Distances to closed segments are different.
 foot=(Q(6),Q(6));lines=[(Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),(Q(3),Q(4),Q(-12))]
 distances=[(a*foot[0]+b*foot[1]+c)**2/(a*a+b*b) for a,b,c in lines]
 assert distances==[36,36,36] and [x+8**2 for x in distances]==[100]*3
 assert 3*foot[0]+4*foot[1]>12 and 6>4 and 6>3 # outside triangle and two side feet
 assert (6-4)**2+6**2+8**2==104!=100 # distance to closed horizontal segment
 # Further source examples: these checks are not an exhaustive solution audit.
 primes=[2,3,5,7,11,13];candidate=prod(primes)+1
 assert candidate==30031==59*509 and all(candidate%p==1 for p in primes)
 assert all(all(p%d for d in range(2,isqrt(p)+1)) for p in [59,509])
 jug_states=[(0,0),(9,0),(5,4),(5,0),(1,4),(1,0),(0,1),(9,1),(6,4),(6,0)]
 for (a,b),following in zip(jug_states,jug_states[1:]):
  d=min(a,4-b);e=min(b,9-a)
  assert following in {(9,b),(a,4),(0,b),(a,0),(a-d,b+d),(a+e,b-e)}
 assert 9+90*2+900*3+25*4==2989 and Q(36792,72)==511
 matrix=[[1,7,3,5],[8,4,6,2],[2,6,4,8],[5,3,7,1]]
 assert [sum(a*b for a,b in zip(row,[-2,2,-2,2])) for row in matrix]==[16,-16,16,-16] # x,y,v,u
 for ap,gp in [([68,42,16],[17,34,68]),([17,42,67],[68,34,17])]:
  assert ap[1]-ap[0]==ap[2]-ap[1] and Q(gp[1],gp[0])==Q(gp[2],gp[1])
  assert [x+y for x,y in zip(ap,gp)]==[85,76,84] and sum(ap)==126
 for m,t in [(Q(6),Q(2)),(Q(-6,19),Q(2,19))]:assert 10*t==3*m+2 and 9*t*t==m*m and t>0
 assert 15+20+25==60 and 15**2+20**2==25**2 and Q(15*20,25)==12
 for n in range(1,21):
  assert sum(Q(k,factorial(k+1)) for k in range(1,n+1))==1-Q(1,factorial(n+1))
  assert sum(range(n*n-n+1,n*n+n,2))==n**3
  assert 6*n*n+(3*n*n+3*n+1)==(9*n*n+3*n)+1
 ways=[0]*101;ways[0]=1
 for coin in [1,5,10,25,50]:
  for amount in range(coin,101):ways[amount]+=ways[amount-coin]
 assert ways[50]==50 and ways[100]==292
 return dict(status='pass',own_exact_models=True,actual_student_data=False,
  signed_digit_solution=signed,unsigned_digit_mod9_impossible=True,
  reflection_cases=4,positive_source_prism_branches=2,
  future_time_and_zero_velocity_checked=True,
  nondegenerate_triangle_counterexample={'sides':[13,13,24],'r_plus_R':'193/10','longest_altitude':'120/13'},
  trapezoid_feasibility_checked=True,root_domain_multiplicity_distinguished=True,
  pyramid_supporting_line_distance=10,foot_outside_base=True,
  further_source_checks={'prime_product_plus_one':30031,'jug_forward_operations':9,'source_pages_numbered':1024,'turkey_price_cents':511,'both_progressions':True,'both_quartic_parameters':['6','-6/19'],'coin_ways_100':292},
  all_source_solutions_independently_reproved=False,publisher_fidelity_verified=False)

if __name__=='__main__':print(json.dumps(check(),ensure_ascii=False))

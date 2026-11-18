"""Exact checks of synthetic teaching examples; no real rates or tax rules."""
from fractions import Fraction as F
from math import comb

assert F(121-100,100)==F(21,100)
assert 25*1200==30000
assert 100*F(1,10)+50*F(1,5)==20
assert 100-2*30==30+10
assert [10*q-q*q for q in [1,2,3]]==[9,16,21]
assert 3+2<=5 and 2*3+2<=8 and 2*4+1>8
def multiply(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(len(b[0]))] for i in range(2)]
A=[[2,1],[1,1]]; inverse=[[1,-1],[-1,2]]
assert multiply(A,inverse)==multiply(inverse,A)==[[1,0],[0,1]]
assert multiply(inverse,[[7],[4]])==[[3],[1]]
assert multiply([[2,1],[1,3]],[[4],[2]])==[[10],[10]]
assert 100+3*2+2*2==110 and F(110,2)==55
assert F(2*20,100-2*20)==F(2,3) and F(2*40,100-2*40)==4
assert [2*1-3,2*2-1]==[-1,3]
assert [[min(255,v+20) for v in row] for row in [[240,10],[0,100]]]==[[255,30],[20,120]]
assert sum(map(sum,[[1,0],[1,1]]))==3
assert F(4,80)==F(5,100) and F(4,80)>F(4,100)
assert 1000+300*13<=5000<1000+300*14
assert 4*50==200 and 50**2==2500
assert 48/24==2 and 2**6==64
assert F(5,100)>F(8,200)
assert F(5,12)<F(1,2)
assert 120/3==40 and 150/5==30
assert F(25-20,20)==F(1,4)
probability=F(sum(comb(10,k) for k in [0,1,9,10]),2**10)
assert probability==F(22,1024) and probability<F(1,20)
print('Applied example checks passed: synthetic indices and rates, matrix inversion, elasticity, pixel transformations, proportions, budgets, scales, finite arrays and exact binomial tails')

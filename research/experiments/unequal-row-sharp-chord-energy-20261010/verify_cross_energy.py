#!/usr/bin/env python3
"""Independent finite audits for the sharp two-row unequal-size chord bound.

Uses two distinct routes: sum multiplicities and direct pair-pair comparisons.
Also checks the 2 x m forbidden-quadruple formula by integer determinants.
"""
from collections import Counter
from itertools import combinations
from math import comb, isqrt
import json


def profile(points):
    return Counter(a+b for a,b in combinations(points,2))


def direct_cross(A,B):
    return sum(a+b==c+d for a,b in combinations(A,2)
               for c,d in combinations(B,2))


def energy_formula(r,t):
    return sum(min(2*r-4*i-3,2*t-4*j-3)
               for i in range(r//2) for j in range(t//2))


def equal_formula(r):
    return (2*r**3-3*r*r+4*r-3*(r%2))//12


def det4(mat):
    # independent integer Gaussian elimination (Bareiss) for 4x4
    M=[list(row) for row in mat]
    sign=1
    prev=1
    for k in range(3):
        if M[k][k]==0:
            j=next((j for j in range(k+1,4) if M[j][k]),None)
            if j is None: return 0
            M[k],M[j]=M[j],M[k]
            sign=-sign
        pivot=M[k][k]
        for i in range(k+1,4):
            for j in range(k+1,4):
                M[i][j]=(M[i][j]*pivot-M[i][k]*M[k][j])//prev
        for i in range(k+1,4): M[i][k]=0
        prev=pivot
    return sign*M[3][3]


def forbidden_direct(m):
    P=[(x,y) for y in range(2) for x in range(m)]
    return sum(det4([(x*x+y*y,x,y,1) for x,y in Q])==0
               for Q in combinations(P,4))


def audit():
    # all A,B subsets of [0,8], including empty and singleton
    universe=range(9)
    sets={r:list(combinations(universe,r)) for r in range(7)}
    profiles={A:profile(A) for ss in sets.values() for A in ss}
    checked=0
    maxima={}
    for r in range(7):
        for t in range(r,7):
            upper=energy_formula(r,t)
            mx=-1
            for A in sets[r]:
                pa=profiles[A]
                for B in sets[t]:
                    pb=profiles[B]
                    value=sum(v*pb.get(s,0) for s,v in pa.items())
                    assert value<=upper, (r,t,A,B,value,upper)
                    mx=max(mx,value)
                    checked+=1
            # Attainability inside [0,8] need not hold when parity differs:
            # optimal integer AP with step 2 can exceed this test universe.
            if (r,t) in [(3,4),(4,6),(5,6)]:
                A=tuple(2*i+t for i in range(r))
                B=tuple(2*j+r for j in range(t))
                assert direct_cross(A,B)==upper
            maxima[f'{r},{t}']={'upper':upper,'max_on_0_to_8':mx}
    assert all(energy_formula(r,r)==equal_formula(r) for r in range(50))
    det_counts={}
    for m in range(2,11):
        count=forbidden_direct(m)
        expected=2*comb(m,4) + energy_formula(m,m)
        assert count==expected,(m,count,expected)
        det_counts[str(m)]=count
    # Full pair-pair audit on nontrivial unequal row sizes, independent of Counter
    for r,t in [(2,5),(3,4),(4,6),(5,6),(5,9),(8,11)]:
        A=tuple(2*i+t for i in range(r))
        B=tuple(2*j+r for j in range(t))
        assert direct_cross(A,B)==energy_formula(r,t)
    report={'theorem':'sharp cross-row unordered distinct-pair equal-sum count',
            'exhaustive_universe':'A,B subsets of integers 0..8, 0<=|A|<=|B|<=6',
            'ordered_set_pairs_checked':checked,
            'maxima':maxima,
            'determinant_2xm_forbidden_quads':det_counts,
            'formula_equal_sizes_verified_through':49,
            'result':'all checks passed'}
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':audit()

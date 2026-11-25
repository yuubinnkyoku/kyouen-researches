#!/usr/bin/env python3
"""Independent exact-circle checks of the finite Gaussian census output.

This is NOT an independent full 100M enumeration. It independently validates
all reported circle types and their counting formula, plus a new Pell seed.
"""
from __future__ import annotations
import csv
from itertools import combinations
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / 'output/q48_gaussian_census_B100000000_20261015.csv'

def det4(mat):
    def det3(x):
        return (x[0][0]*(x[1][1]*x[2][2]-x[1][2]*x[2][1])
                - x[0][1]*(x[1][0]*x[2][2]-x[1][2]*x[2][0])
                + x[0][2]*(x[1][0]*x[2][1]-x[1][1]*x[2][0]))
    return sum((-1)**j * mat[0][j] * det3(
        [[mat[i][k] for k in range(4) if k != j] for i in range(1, 4)])
        for j in range(4))

def count(m, patterns):
    return sum(max(0, m - max(p)) for p in patterns)

def audit():
    with CSV.open(newline='', encoding='utf-8') as f:
        patterns = [tuple(map(int, (r['d0'],r['d1'],r['d2'],r['d3'])))
                    for r in csv.DictReader(f)]
    assert len(patterns) == 15 and len(set(patterns)) == 15
    assert len([p for p in patterns if p == p[::-1]]) == 1
    assert set(patterns) == {p[::-1] for p in patterns}
    for d in patterns:
        assert all(x > 0 and x % 2 for x in d)
        assert d[0]**2 - 2*d[1]**2 + d[2]**2 == -8
        assert d[1]**2 - 2*d[2]**2 + d[3]**2 == -8
        D = max(d)
        points = [(x, y) for y, length in enumerate(d)
                  for x in ((D-length)//2, (D+length)//2)]
        assert len(points) == len(set(points)) == 8
        for quad in combinations(points, 4):
            mat = [[x*x+y*y,x,y,1] for x,y in quad]
            assert det4(mat) == 0, (d, quad)
    new = (5371183,43796547,61704339,75476575)
    assert new in patterns
    a,b,c,d = new
    s,v = (a+d)//2, (c-b)//2
    h = gcd(s,v)
    A,B = s//h,v//h
    assert (A,B) == (181273,40152)
    g = gcd(A,3)
    L=s//A
    M=((b+c)//2)*g//A
    assert (L,M,g) == (223,291,1)
    P,Q = A*A-B*B,(A*A-9*B*B)//(g*g)
    assert Q*M*M-P*L*L == 8
    # Explicit independent Gaussian integer factorization certificate.
    z=complex(1,1)
    # Use integer complex multiplication, not floating point.
    def cmul(z,w): return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
    z=(1,1)
    for w in ((1,2),(2,3),(212,-793),(607,-6590)):
        z=cmul(z,w)
    assert z==(61704339,5371183)
    assert (b-2,b+2)==(5*13*673793,43796549)
    assert all((x*x+y*y)==p for x,y,p in
               ((1,2,5),(2,3,13),(212,793,673793),(607,6590,43796549)))
    # Every distinct chord tuple has exactly m-max(chords) horizontal translations.
    assert count(1000001,patterns)==6783710
    assert count(100000001,patterns)==1334910478
    print('PASS: 15 distinct patterns; 1050 exact 4-point circle determinants')
    print('PASS: fourth slope 181273/40152; Pell norm=8; Gaussian identity')
    print('PASS: 1000001-column count=6783710; 100000001-column count=1334910478')
    print('LIMIT: complete 100M census relies on Gaussian C++ enumerator;')
    print('       separate direct (d0,d1) scan reproduced B<=1000000 only.')

if __name__ == '__main__': audit()

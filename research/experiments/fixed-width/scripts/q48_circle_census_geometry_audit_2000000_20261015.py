#!/usr/bin/env python3
"""Independent exact-coordinate audit for 4-row eight-point circles."""
from itertools import combinations
from pathlib import Path

def det(a):
    # Fraction-free determinant, size four; independent of the chord identities.
    if len(a) == 1: return a[0][0]
    return sum(((-1)**j)*a[0][j]*det([row[:j]+row[j+1:] for row in a[1:]]) for j in range(len(a)))

def audit(chords):
    D=max(chords)
    points=[]
    for y,d in enumerate(chords):
        assert d>0 and (D-d)%2==0
        points += [((D-d)//2,y),((D+d)//2,y)]
    assert len(set(points))==8
    assert min(x for x,y in points)==0 and max(x for x,y in points)==D
    for four in combinations(points,4):
        assert det([[x*x+y*y,x,y,1] for x,y in four])==0
    return points

patterns=[(1,3,3,1)]
for line in (Path(__file__).resolve().parent.parent/'output/q48_circle_census_2000000_20261015.csv').read_text().splitlines():
    p=tuple(map(int,line.split(',')))
    patterns.extend([p,p[::-1]])
for p in patterns:
    pts=audit(p)
    print('chords',p,'first_m',max(p)+1,'determinants_checked',70,'points',pts)
print('patterns',len(patterns),'determinants_checked',len(patterns)*70)

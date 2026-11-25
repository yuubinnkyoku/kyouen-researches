#!/usr/bin/env python3
"""Enumerate long circles using pairs of chords in distinct rows."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
import json


def long_circles(width):
    pairs = defaultdict(list)
    for a,b in combinations(range(width),2):
        pairs[a+b].append((a,b))
    circles = {}
    for y1,y2 in combinations(range(5),2):
        for chord_pairs in pairs.values():
            for x1,x2 in chord_pairs:
                for x3,x4 in chord_pairs:
                    # The two horizontal chords have the same midpoint x-coordinate.
                    ux = Fraction(x1+x2,2)
                    uy = Fraction(y1*y1-y2*y2-x1*x2+x3*x4,2*(y1-y2))
                    radius = (Fraction(x1)-ux)**2+(Fraction(y1)-uy)**2
                    key = (ux,uy,radius)
                    if key in circles:
                        continue
                    members = tuple((x,y) for y in range(5) for x in range(width)
                                    if (Fraction(x)-ux)**2+(Fraction(y)-uy)**2==radius)
                    circles[key] = members
    long_circles = [points for points in circles.values() if len(points) >= 7]
    # A circle meets each horizontal line at most twice. Seven points across
    # five rows force at least two distinct rows with two points each.
    assert len(long_circles) == len(set(long_circles))
    return long_circles


def census(width):
    circles = long_circles(width)
    distribution = Counter(map(len,circles))
    return {'rows':5,'columns':width,'circles_at_least_seven':len(circles),
            'counts_by_size':{str(k):v for k,v in sorted(distribution.items())}}


if __name__ == '__main__':
    print(json.dumps([census(18),census(19)],indent=2))

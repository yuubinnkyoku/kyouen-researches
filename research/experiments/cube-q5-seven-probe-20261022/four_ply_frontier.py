#!/usr/bin/env python3
"""Exact terminal-four response coverage for one pair, without game search."""
from itertools import combinations, product
import json
import sys

side, a, b = map(int, sys.argv[1:])
assert 3 <= side <= 7
points = list(product(range(side), repeat=3))
assert 0 <= a < len(points) and 0 <= b < len(points) and a != b
lifts = [(sum(x*x for x in p), *p) for p in points]
base = lifts[a]
v = tuple(x-y for x, y in zip(lifts[b], base))
cols = list(combinations(range(4), 3))
responses = {}
uncovered = []
for c in range(len(points)):
    if c in (a, b):
        continue
    w = tuple(x-y for x, y in zip(lifts[c], base))
    for d in range(len(points)):
        if d in (a, b, c):
            continue
        t = tuple(x-y for x, y in zip(lifts[d], base))
        if all(v[i]*(w[j]*t[k]-w[k]*t[j])-v[j]*(w[i]*t[k]-w[k]*t[i])
               +v[k]*(w[i]*t[j]-w[j]*t[i]) == 0 for i, j, k in cols):
            responses[str(c)] = d
            break
    else:
        uncovered.append(c)
print(json.dumps({"side": side, "pair": [a, b], "third_moves": len(points)-2,
                  "terminal_four_responses": responses,
                  "uncovered_thirds": uncovered}, indent=2))

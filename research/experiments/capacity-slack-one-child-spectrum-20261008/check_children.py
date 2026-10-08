#!/usr/bin/env python3
"""Exhaustive labelled-move child nimber counts: odd n, slack exactly one."""
from itertools import combinations_with_replacement as combs
from functools import lru_cache
from collections import Counter
counts = Counter()
examples = {}
for w in range(3, 9):
 for h in range(2, w):
  if (w-h)%2 == 0: continue
  for m in range(2, 7):
   for r in range(1, h*m):
    @lru_cache(None)
    def g(x):
     vals = set()
     for i,v in enumerate(x):
      if v == m: continue
      y = list(x); y[i] += 1; y = tuple(sorted(y, reverse=True))
      if sum(y[:h]) <= r: vals.add(g(y))
     mex = 0
     while mex in vals: mex += 1
     return mex
    for a in combs(range(m+1), w):
     x = tuple(reversed(a))
     if sum(x[:h]) != r-1 or not (x[h-2]>x[h-1] and x[h-2]<m): continue
     b = x[h-1]; R = (w-h)*b-sum(x[h:])
     u = sum(b<v<m for v in x[:h-1])
     c = sum(v==b for v in x)
     ell = sum(v<b for v in x[h:])
     observed = Counter(); point_counts = Counter()
     for i,v in enumerate(x):
      if v == m: continue
      y = list(x); y[i] += 1; y = tuple(sorted(y, reverse=True))
      if sum(y[:h]) <= r: observed[g(y)] += 1; point_counts[g(y)] += (m-v)
     expected = Counter({0:u,1:c,3:ell} if R%2==0 else {0:c,1:u,2:ell})
     expected = +expected
     assert observed == expected, (w,h,m,r,x,observed,expected)
     up = sum(m-v for v in x[:h-1] if b<v<m)
     cp = c*(m-b)
     ep = sum(m-v for v in x[h:] if v<b)
     expected_points = +Counter({0:up,1:cp,3:ep} if R%2==0 else {0:cp,1:up,2:ep})
     assert point_counts == expected_points, (w,h,m,r,x,point_counts,expected_points)
     assert g(x) == 2 + R%2
     counts['positions'] += 1; counts['g'+str(g(x))] += 1
     counts['winning_moves'] += observed[0]; counts['point_winning_moves'] += point_counts[0]
     if R%2==0 and u<h-1 and 'example' not in examples:
      examples['example']=(w,h,m,r,x,u,h-1)
print('PASS', dict(counts)); print('EXAMPLE', examples)

#!/usr/bin/env python3
"""Independent component-multiset count using grouped stars-and-bars."""
from collections import defaultdict
from math import comb
from pathlib import Path
import re

rows = Path(__file__).with_name("results.txt").read_text().splitlines()
groups = []
expected = {}
for row in rows:
    if not row.startswith("edges="):
        continue
    m = re.fullmatch(
        r"edges=(\d+) connected_classes=(\d+) connected_hist=([^ ]+) "
        r"all_classes=(\d+) all_hist=([^ ]+) max=(\d+)", row)
    assert m, row
    edge, nconn, hist, count, all_hist, maximum = m.groups()
    edge = int(edge)
    ch = {int(a): int(b) for a, b in
          (x.split(":") for x in hist.strip(",").split(","))}
    assert sum(ch.values()) == int(nconn)
    groups.extend((edge, g, n) for g, n in ch.items())
    expected[edge] = tuple(map(int, all_hist.split(",")))
    assert sum(expected[edge]) == int(count)
    assert len(expected[edge]) == int(maximum) + 1

# For c distinct connected types with identical (edge, SG), choosing k
# with repetition has comb(c+k-1,k) possibilities and SG=(k mod 2)*g.
dp = {(0, 0): 1}
for edge, g, c in groups:
    nxt = defaultdict(int)
    for (used, nim), ways in dp.items():
        for k in range((12-used)//edge+1):
            multiplicity = comb(c+k-1, k) if k else 1
            nxt[(used+k*edge, nim^(g if k%2 else 0))] += ways*multiplicity
    dp = nxt

for e, hist in expected.items():
    got = tuple(dp.get((e, g), 0) for g in range(len(hist)))
    assert got == hist, (e, got, hist)
    assert all(v == 0 for (n, g), v in dp.items()
               if n == e and g >= len(hist))
    print(f"edges={e} classes={sum(got)} max={len(hist)-1}")
print("All grouped-multiset histograms match the C++ per-type DP.")

#!/usr/bin/env python3
"""w-general (q=4) blocking-counting class table: for w in {3..7}.

Extends the K1202 w=3 captable mechanism to w rows. For w>=4, non-horizontal
lines CAN block (<= w slab points); both circle and line blocker coverage on a
deficient row i is bounded by max(0, 2-u_i) (lines hit a row <= once and a line
blocker of row i carries u_i=0 on it; circles meet a row <= 2 points), so the
CAPS supply formula sum_triples sum_def max(0,2-u_i) is a valid upper bound for
all w. Triples with 3 stones on one row (horizontal lines of full rows) never
cover deficient-row cells (deficient rows have <=2 stones) and are excluded.
"""
import itertools, math, json

def class_bound(r):
    w = len(r)
    defrows = [i for i in range(w) if r[i] <= 2]
    if not defrows:
        return (None, None)
    demand_r = sum(r[i] for i in defrows)
    d = len(defrows)
    caps = 0
    for u in itertools.product(*[range(min(ri,3)+1) for ri in r]):
        if sum(u) != 3 or max(u) > 2:
            continue
        mult = 1
        for i in range(w):
            mult *= math.comb(r[i], u[i])
        if mult == 0:
            continue
        cap = sum(max(0, 2 - u[i]) for i in defrows)
        caps += mult * cap
    real_ub = (caps + demand_r) // d
    return (caps, real_ub if caps > 0 else 0)

def lit_cap(r):
    """literal stone-triple enumeration (cross-check multiplicities)."""
    w = len(r)
    defrows = [i for i in range(w) if r[i] <= 2]
    stones = []
    for i in range(w):
        stones += [i]*r[i]
    caps = 0
    for T in itertools.combinations(range(len(stones)), 3):
        u = [0]*w
        for t in T:
            u[stones[t]] += 1
        if max(u) > 2:
            continue  # 3-on-one-row: horizontal line of a full row, weight 0 for def rows
        cap = sum(max(0, 2-u[i]) for i in defrows)
        caps += cap
    return caps

out = {}
for w in [3,4,5,6,7]:
    table = {}
    for r in itertools.product(range(4), repeat=w):
        if all(x == 3 for x in r):
            continue
        cls = tuple(sorted(r))
        caps, ub = class_bound(r)
        lcap = lit_cap(r)
        assert caps == lcap, (r, caps, lcap)
        if cls not in table:
            table[cls] = (caps, ub)
        else:
            assert table[cls] == (caps, ub), (r, cls, table[cls], (caps,ub))
    out[w] = table
    tops = max(table.items(), key=lambda kv: kv[1][1])
    print(f"== w={w}: {len(table)} classes, top class {tops[0]} caps={tops[1][0]} B={tops[1][1]}")

json.dump({str(w): {str(k): v for k, v in t.items()} for w, t in out.items()}, open("captable_q4.json","w"), indent=0)

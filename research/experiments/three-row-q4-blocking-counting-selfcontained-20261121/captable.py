#!/usr/bin/env python3
"""Cap-table computation: per-profile-class blocking-counting bounds for w=3, q=4.

For a def-mode maximal safe config S on the 3xm slab (rows y in {0,1,2},
cells x in {0..m-1}, win = 4 points on a common circle or line), with row
stone counts (r0,r1,r2), deficient rows are those with r_i <= 2 (q-2).
Every empty cell of a deficient row must lie on a blocker object: a circle
through the cell and >= 3 stones of S (horizontal row line: r_i+1 <= 3 < 4;
non-horizontal lines: <= 3 slab cells). By safety, every blocker circle carries
EXACTLY 3 stones (4 would be a win) => blockers inject into non-collinear
stone triples. A circle meets any horizontal row line in <= 2 points, of
which u_i are stones of S on that row => relevant hits on deficient row i
<= 2 - u_i. So:

    demand = sum_{i def} (m - r_i)  <=  sum over stone triples T  of  sum_{i def} (2 - u_i(T))

where u_i(T) = #stones of T on row i, compositions with rows holding 3 stones
of T (u_i = 3) are collinear triples (no circle; never blockers) and are
excluded. Solving for m gives the class bound B(class).
"""
import itertools, json, math

def class_bound(r):
    """r = tuple of 3 row stone counts (multiset). Returns (caps, ubound)."""
    defrows = [i for i in range(3) if r[i] <= 2]
    if not defrows:
        return (None, None)
    demand_r = sum(r[i] for i in defrows)            # demand = d*m - demand_r <= caps
    d = len(defrows)
    caps = 0
    comps = {}
    for u in itertools.product(range(min(r[0],3)+1), range(min(r[1],3)+1), range(min(r[2],3)+1)):
        if sum(u) != 3 or max(u) > 2:
            continue                                # 3-on-one-row = collinear, no circle
        mult = math.comb(r[0],u[0]) * math.comb(r[1],u[1]) * math.comb(r[2],u[2])
        if mult == 0:
            continue
        cap = sum(max(0, 2 - u[i]) for i in defrows)
        comps[u] = (mult, cap)
        caps += mult * cap
    # demand d*m - demand_r <= caps  =>  m <= (caps + demand_r)/d
    ub = (caps + demand_r) // d if caps >= 0 else 0
    if caps == 0:
        ub = None                                    # impossible for any m >= 1
        real_ub = 0
    else:
        real_ub = (caps + demand_r) // d
    return (caps, comps, real_ub)

# second path: literal stone-combination enumeration (verify multiplicities)
def mult_by_compositions_lit(r):
    # a placeholder pool: r[i] distinct stones in row i (any positions)
    comp = {}
    stones = []
    for i in range(3):
        stones += [(i, j) for j in range(r[i])]
    for T in itertools.combinations(range(len(stones)), 3):
        u = [0,0,0]
        for t in T:
            u[stones[t][0]] += 1
        if max(u) > 2:
            continue
        comp[tuple(u)] = comp.get(tuple(u), 0) + 1
    return comp

table = {}
for r in itertools.product(range(4), repeat=3):
    if r == (3,3,3):
        continue
    cls = tuple(sorted(r))
    caps, comps, ub = class_bound(r)
    # cross-check multiplicities by literal enumeration
    lit = mult_by_compositions_lit(r)
    for u,(mult,cap) in comps.items():
        assert lit[u] == mult, (r, u, mult, lit[u])
    assert sum(m for m,_ in comps.values()) == sum(lit.values())
    # class bound = same for any permutation of r (position-independent)
    table.setdefault(cls, set()).add(ub if ub is not None else -1)

print("class -> bounds across permutations (should be a single value each):")
bad = [c for c,v in table.items() if len(v) != 1]
assert not bad, bad
final = {str(c): list(v)[0] if list(v)[0] >= 0 else "IMPOSSIBLE" for c,v in sorted(table.items())}
for c, v in sorted(table.items()):
    print(c, list(v)[0] if list(v)[0] >= 0 else "IMPOSSIBLE")

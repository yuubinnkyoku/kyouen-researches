#!/usr/bin/env python3
"""Census 1: verify ladder law fragments on z0 face.
Claims (all z0, min = m >= 2 unless stated, row m = min(X), budget 2m+k):
  H1(m):   arm-1 mixed (mult(m)=1):          V[m,2] == 1
  L3(m):   arm-1 high-gap (no token m+1):    V[m,3] == 0
  C4(m):   arm-1 gap>=3 (no token in {m+1,m+2}): V[m,4] != 0
  E(m):    mult(m)>=2 mixed:                 V[m,2] == 0  (LAW-C else)
  A2(m):   mult(m)>=1 mixed with max<=m+1, mult(m+1)=1 (arm-2): V[m,2] == 1
  II(m):   arm-1 with c1>=1 tokens of (m+1) and >=1 token >= m+2: V[m,3] != 0
  Q(m):    mixed front: V[m,1] == 2 ; allm (m^a>=2) front: V[m,1] == 0
Row-1 bases (z0, min=1):
  R4:  X=(1, 2^u, s_1..s_v) with u>=0, v>=1, s_i>=3: H(4;X;0)==1
  L3(1): X=(1, s_1..s_v), s_i>=3, v>=1: H(5;X;0)==0
  H1(1): X=(1, t_1..t_r), t_i>=2: H(4;X;0)==1
"""
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)

def mex(values):
    values = set(values); m = 0
    while m in values: m += 1
    return m

@lru_cache(maxsize=8_000_000)
def H(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0: return 0
    opts = set(); i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            opts.add(H(R-1, tuple(sorted(X[:i]+(v-1,)+X[i+1:], reverse=True)), z))
        else:
            opts.add(H(R-1, tuple(sorted(X[:i]+X[i+1:], reverse=True)), z+1))
        while i+1 < len(X) and X[i+1] == v: i += 1
        i += 1
    if z >= 1: opts.add(1 ^ H(R-1, X, z-1))
    return mex(opts)

from itertools import combinations_with_replacement

def mixed_shapes(m, tmax, amax):
    """arm-1 and mult>=2 mixed shapes, min exactly m"""
    out = []
    vals = list(range(m, tmax+1))
    for a in range(2, amax+1):
        for combo in combinations_with_replacement(vals, a):
            if combo[0] == m:  # min exactly m
                if len(set(combo)) > 1:  # mixed
                    out.append(tuple(sorted(combo)))
    return out

def allm_shapes(m, amax):
    return [tuple([m]*a) for a in range(2, amax+1)]

def sig(X, m):
    c1 = sum(1 for t in X if t == m+1)
    c2 = sum(1 for t in X if t == m+2)
    b  = sum(1 for t in X if t >= m+3)
    return (c1, c2, b)

def main():
    M = 6           # rows 2..M
    TMAXOFF = 6     # tokens up to m+TMAXOFF
    AMAX = 5
    counters = {}
    def rec(name, ok, detail=None):
        key = name
        counters[key] = counters.get(key, [0, 0])
        counters[key][0] += 1
        if not ok: counters[key][1] += 1
        if not ok and counters[key][1] <= 5:
            print(f"VIOLATION {name}: {detail}")
        return ok

    for m in range(2, M+1):
        for X in mixed_shapes(m, m+TMAXOFF, AMAX):
            s = sig(X, m); mm = X.count(m)
            arm1 = (mm == 1)
            # H1: arm-1 -> V[m,2] == 1
            if arm1:
                rec(f"H1[{m}]", H(2*m+2, X, 0) == 1, (X, H(2*m+2, X, 0)))
                # L3: high gap (c1==0) -> V[m,3]==0
                if s[0] == 0:
                    rec(f"L3[{m}]", H(2*m+3, X, 0) == 0, (X, H(2*m+3, X, 0)))
                    if s[1] == 0:  # gap>=3
                        rec(f"C4[{m}]", H(2*m+4, X, 0) != 0, (X, H(2*m+4, X, 0)))
                # Q front mixed
                rec(f"Q[{m}]", H(2*m+1, X, 0) == 2, (X, H(2*m+1, X, 0)))
                # II: c1>=1 and c2+b>=1 -> V[m,3] != 0
                if s[0] >= 1 and s[1]+s[2] >= 1:
                    rec(f"II[{m}]", H(2*m+3, X, 0) != 0, (X, H(2*m+3, X, 0)))
            else:
                # mult>=2 mixed -> V[m,2] == 0  (LAW-C else)
                big = max(X)
                if not (big <= m+1 and X.count(m+1) == 1):
                    rec(f"E[{m}]", H(2*m+2, X, 0) == 0, (X, H(2*m+2, X, 0)))
                else:
                    rec(f"A2[{m}]", H(2*m+2, X, 0) == 1, (X, H(2*m+2, X, 0)))
                rec(f"Q[{m}]", H(2*m+1, X, 0) == 2, (X, H(2*m+1, X, 0)))
        for X in allm_shapes(m, AMAX):
            rec(f"Qallm[{m}]", H(2*m+1, X, 0) == 0, (X, H(2*m+1, X, 0)))

    # row-1 bases
    r4_bad = 0; l31_bad = 0; h11_bad = 0; r4_n = l31_n = h11_n = 0
    for u in range(0, 5):
        for v in range(1, 4):
            for combo in combinations_with_replacement(range(3, 12), v):
                X = tuple(sorted([1] + [2]*u + list(combo)))
                val = H(4, X, 0)
                r4_n += 1
                if val != 1:
                    r4_bad += 1
                    if r4_bad <= 8: print("R4 VIOLATION", X, val)
                if u == 0:
                    val5 = H(5, X, 0)
                    l31_n += 1
                    if val5 != 0:
                        l31_bad += 1
                        if l31_bad <= 8: print("L3(1) VIOLATION", X, val5)
    for r in range(1, 4):
        for combo in combinations_with_replacement(range(2, 12), r):
            X = tuple(sorted([1] + list(combo)))
            h11_n += 1
            val = H(4, X, 0)
            if val != 1:
                h11_bad += 1
                if h11_bad <= 8: print("H1(1) VIOLATION", X, val)

    print("\n=== z0 fragment counts (total, violations): n_pts = sum of totals ===")
    tot_pts = 0
    for k in sorted(counters.keys()):
        t, b = counters[k]
        tot_pts += t
        flag = "OK " if b == 0 else "BAD"
        print(f"{flag} {k:12s} {t:6d} {b:5d}")
    print(f"row1: R4 {r4_n}/{r4_bad}  L3(1) {l31_n}/{l31_bad}  H1(1) {h11_n}/{h11_bad}")
    tot_pts += r4_n + l31_n + h11_n
    print("TOTAL POINTS:", tot_pts)

if __name__ == "__main__":
    main()

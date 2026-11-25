#!/usr/bin/env python3
from functools import lru_cache
from itertools import combinations_with_replacement
import sys
"""explore5_tables.py -- dump readable tables for beyond-frontier mining.
z=0 d=2,3 and z=1 d=3, m=1..3, small shapes. Also test FB0 identity D'=1-c
and C-absorption lemma (min>=2). Observation only.
"""
import hashlib
ENGINE_SHA = hashlib.sha256(open('engine_block.py','rb').read()).hexdigest()
assert ENGINE_SHA == 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
exec(open("engine_block.py").read())  # H_canonical, H_ordered, single_token=v
v = single_token

def test_fb0(mu_max=7):
    ok = bad = 0
    badex = []
    for mu in range(2, mu_max + 1):
        R = 2 * mu + 1
        # all mixed parents with min mu, tokens<=R+1, arity<=4
        from itertools import combinations_with_replacement
        for k in range(2, 5):
            for c in combinations_with_replacement(range(mu, R + 2), k):
                if c[0] != mu or max(c) == mu:
                    continue
                X = tuple(reversed(c))
                S = sum(X)
                cc = v(S - 1, 0, R - 1)
                Xp = list(X); Xp.remove(mu); Xp.append(mu - 1); Xp.sort(reverse=True)
                Dp = H_canonical(R - 1, tuple(Xp), 0)
                if Dp == 1 - cc: ok += 1
                else:
                    bad += 1
                    badex.append((mu, X, cc, Dp))
        H_canonical.cache_clear(); H_ordered.cache_clear()
    return ok, bad, badex[:10]

def c_absorption_check():
    # min>=2: H(R;X;1) == H(R;X;0) iff (1^H(R-1;X;0)) in A-opt values
    ok = bad = 0
    from itertools import combinations_with_replacement
    for m in range(2, 5):
        for R in range(2 * m + 1, 2 * m + 5):
            for k in range(2, 5):
                for c in combinations_with_replacement(range(m, R + 2), k):
                    if c[0] != m: continue
                    X = tuple(reversed(c))
                    h0 = H_canonical(R, X, 0)
                    h1 = H_canonical(R, X, 1)
                    aopts = set()
                    for t in set(X):
                        Y = list(X); Y.remove(t); Y.append(t - 1); Y.sort(reverse=True)
                        aopts.add(H_canonical(R - 1, tuple(Y), 0))
                    ch = 1 ^ H_canonical(R - 1, X, 0)
                    pred = h1 if (ch in aopts) else None
                    if ch in aopts:
                        if h1 == h0: ok += 1
                        else: bad += 1
            H_canonical.cache_clear(); H_ordered.cache_clear()
    return ok, bad

def mixed_table(z, m, d, amax=4):
    from itertools import combinations_with_replacement
    R = 2 * m + d
    rows = []
    for k in range(2, amax + 1):
        for c in combinations_with_replacement(range(m, R + 2), k):
            if c[0] != m or max(c) == m: continue
            X = tuple(reversed(c))
            S = sum(X)
            h = H_canonical(R, X, z)
            rows.append((X, S, h))
    H_canonical.cache_clear(); H_ordered.cache_clear()
    return rows

print("FB0 identity test (D' == 1-c):")
ok, bad, ex = test_fb0()
print("  ok=%d bad=%d" % (ok, bad), "badex:", ex)

print("C-absorption spot-check:")
print("  absorption-holds=%d violated=%d" % c_absorption_check())

for (z, m, d) in [(0, 2, 2), (0, 2, 3), (0, 3, 2), (1, 2, 3), (1, 3, 3)]:
    print("z=%d m=%d d=%d" % (z, m, d))
    rows = mixed_table(z, m, d)
    # group by value
    from collections import defaultdict
    gv = defaultdict(list)
    for X, S, h in rows: gv[h].append((X, S))
    for h in sorted(gv):
        lst = gv[h]
        print("  H=%d n=%d" % (h, len(lst)), "ex:", [(list(x), s) for x, s in lst[:8]])

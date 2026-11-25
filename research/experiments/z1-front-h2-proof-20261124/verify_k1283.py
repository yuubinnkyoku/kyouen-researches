#!/usr/bin/env python3
"""
verify_k1283.py -- official verifier kit for K1283
(z1 flank closure: H2 proved universal -> z1 delta-2 plane fully
classified: mixed via T-H2 (H=1 iff X=(m,m+1), else 0), allm via T-E1
(a>=2 -> 0); T-B1 upgraded to unconditional (T-B1': z1 band+diagonal
collapse + frontier classification); T-N0z1 (z1 delta-3 mixed never 0);
T-IIz1 (z1 delta-3 class E >= 2); row-1 base H2(1) + G3z2 floor
classification (budget-3 z2: value 1 except X in {(2,), (1,1)} -> 2)).
All clauses are UNCONDITIONAL universal claims on the declared grids;
no hypothesis remains. Engine block embedded verbatim, sha256-gated
against the published pin
bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92
(the K1138/K1257/K1281/K1282 provenance chain).
Batteries D1..D10 (+declared comparison counts cf. the predeclaration note).
TAMPER: --tamper-engine (rc 2), --tamper=h2|e1|q1|band|lzf|ls|n0|ii (rc 1).
Determinism: official runs byte-identical on stdout (volatile timestamps and
elapsed are emitted on stderr only); no wall-clock in the stdout audit JSON.
"""
import json, hashlib, sys, time
from functools import lru_cache
from itertools import combinations_with_replacement

ENGINE_BLOCK = 'def mex(values):\n    values = set(values)\n    m = 0\n    while m in values:\n        m += 1\n    return m\n\n# ------------------------------------------------------------------\n# Raw engines (verbatim from the published K1138 verifier block; the same\n# transcription is embedded in the published y22 machine K1257).\n# ------------------------------------------------------------------\n@lru_cache(maxsize=6_000_000)\ndef H_ordered(R, X, z):\n    if R == 0:\n        return 0\n    opts = set()\n    for i, v in enumerate(X):\n        if v > 1:\n            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))\n        else:\n            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))\n    if z >= 1:\n        opts.add(1 ^ H_ordered(R - 1, X, z - 1))\n    return mex(opts)\n\n@lru_cache(maxsize=6_000_000)\ndef H_canonical(R, X, z):\n    X = tuple(sorted(X, reverse=True))\n    if R == 0:\n        return 0\n    opts = set()\n    i = 0\n    while i < len(X):\n        v = X[i]\n        if v > 1:\n            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))\n            opts.add(H_canonical(R - 1, child, z))\n        else:\n            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))\n            opts.add(H_canonical(R - 1, child, z + 1))\n        while i + 1 < len(X) and X[i + 1] == v:\n            i += 1\n        i += 1\n    if z >= 1:\n        opts.add(1 ^ H_canonical(R - 1, X, z - 1))\n    return mex(opts)\n\ndef vC(x, z, R):  # canonical-engine single token\n    return H_canonical(R, (x,), z)\ndef vO(x, z, R):  # ordered-engine single token\n    return H_ordered(R, (x,), z)\n\n# ------------------------------------------------------------------\n# Published K0832 single-token closed form (transcription of the published\n# single_token block in the y22 machine K1257; see report provenance).\n# ------------------------------------------------------------------\ndef q_odd(k):\n    return k if k % 2 else k - 1\n\ndef single_token(x, z, R):\n    if R == 0 or x <= 0:\n        return 0\n    if z == 0:\n        return min(R, x) % 2\n    if z == x:\n        if R % 2 and R <= 2 * x - 1:\n            return 2\n        if R % 2 == 0 and R <= x - 1:\n            return 0\n        return x % 2\n    if 1 <= z <= x - 1:\n        m = q_odd(z)\n        if R <= m:\n            return 2 if R % 2 else 0\n        if m < R < x + z:\n            return (R + z) % 2\n        return x % 2\n    if z >= x + 1:\n        m = q_odd(x)\n        if R <= m:\n            return 2 if R % 2 else 0\n        return x % 2\n    raise ValueError((x, z, R))\n'

ENGINE_SHA = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
if '--tamper-engine' in sys.argv:
    tmp = ENGINE_BLOCK.replace('return k if k % 2 else k - 1', 'return k if k % 2 else k')
    sha2 = hashlib.sha256(tmp.encode('utf-8')).hexdigest()
    assert sha2 != PIN, 'tamper must change the sha'
    print('TAMPER-ENGINE: sha mismatch: %s != %s' % (sha2, PIN))
    sys.exit(2)
assert ENGINE_SHA == PIN, 'engine sha256 gate FAILED: %s' % ENGINE_SHA
exec(ENGINE_BLOCK)
v = single_token

TAMPER = None
for a in sys.argv[1:]:
    if a.startswith('--tamper='):
        TAMPER = a.split('=', 1)[1]

def shapes(m, hi, amax):
    for k in range(2, amax + 1):
        for c in combinations_with_replacement(range(m, hi + 1), k):
            if c[0] == m and max(c) > m:
                yield tuple(reversed(c))

def shapes1(m, hi, amax, mult):
    """arm-`mult` mixed shapes: exactly `mult` copies of the min token m"""
    for c in shapes(m, hi, amax):
        if c.count(m) == mult:
            yield c

def allm(m, a):
    return tuple([m] * a)

def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()

def main():
    t0 = time.time()
    res = {'kit': 'verify_k1283', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS'}
    ND = 10
    counts = [0] * ND
    bad = [0] * ND
    ex = [[] for _ in range(ND)]
    h2_ones = 0
    n0_hist = {}
    ii_hist = {}
    # tamper expectations
    h2flip = (TAMPER == 'h2')
    e1_exp = 1 if TAMPER == 'e1' else 0
    q1_exp = 1 if TAMPER == 'q1' else 2
    lzf_flip = (TAMPER == 'lzf')   # D5 claim check flips to h==0
    lzf_anchor = 0 if TAMPER == 'lzf' else 1
    ls_bound = 4 if TAMPER == 'ls' else 2
    ls_stair = 0 if TAMPER == 'ls' else 1
    n0_flip = (TAMPER == 'n0')
    ii_flip = (TAMPER == 'ii')   # D8 claim check flips to h<=1

    def cmpd(i, ok, note):
        counts[i] += 1
        if not ok:
            bad[i] += 1
            if len(ex[i]) < 6: ex[i].append(note)

    # -------- D1: H2 census (z=1, delta=2 mixed -> min(sum,R)%2, m=1..7) ----
    # row-1 wide: X=(1^q, t_i>=2), q<=4, sums<=26, arity<=5
    for q in range(1, 5):
        for k in range(1, 5):
            for c in combinations_with_replacement(range(2, 12), k):
                X = tuple(sorted([1] * q + list(c), reverse=True))
                h = H_canonical(4, X, 1)
                exp = min(sum(X), 4) % 2
                if h2flip: exp = 1 - exp
                if exp == 1 and not h2flip: h2_ones += 1
                cmpd(0, h == exp, [1, 'm1', 4, list(X), h, exp])
            clear()
    for m in range(2, 8):
        R = 2 * m + 2
        for X in shapes(m, m + 7, 5):
            h = H_canonical(R, X, 1)
            exp = min(sum(X), R) % 2
            if h2flip: exp = 1 - exp
            if exp == 1 and not h2flip: h2_ones += 1
            cmpd(0, h == exp, [1, 'mixed', R, list(X), h, exp])
        clear()
    # tall giants: uniformity pointers at huge inert tokens
    for (m, bigs) in [(2, (22,)), (2, (23,)), (2, (22, 23)), (3, (25,)),
                      (3, (22, 26)), (4, (30,)), (4, (22, 31))]:
        X = tuple(sorted((m,) + bigs, reverse=True))
        R = 2 * m + 2
        h = H_canonical(R, X, 1)
        exp = min(sum(X), R) % 2
        if h2flip: exp = 1 - exp
        cmpd(0, h == exp, [1, 'tall', R, list(X), h, exp])
        clear()

    # -------- D2: T-E1 allm census (z=1 delta-2: a=1 -> v; a>=2 -> 0) ------
    for m in range(1, 9):
        R = 2 * m + 2
        for a in range(1, 9):
            h = H_canonical(R, allm(m, a), 1)
            exp = v(m, 1, R) if a == 1 else e1_exp
            cmpd(1, h == exp, [2, m, a, h, exp])
            clear()

    # -------- D3: z1 frontier classification (m=2..7) --------
    for m in range(2, 8):
        Rp = 2 * m + 1
        for X in shapes(m, m + 7, 5):
            h = H_canonical(Rp, X, 1)
            cmpd(2, h == q1_exp, [3, 'frontier', Rp, list(X), h])
            clear()
        for a in range(2, 8):
            h = H_canonical(Rp, allm(m, a), 1)
            exp = 0 if a == 2 else 2
            cmpd(2, h == exp, [3, 'frontier-allm', Rp, a, h, exp])
            clear()

    # -------- D4: z1 band+diagonal collapse (m=2..7, sum>=R regime) --------
    for m in range(2, 8):
        for R in range(m + 2, 2 * m + 1):
            for X in shapes(m, R + 2, 4):
                if sum(X) < R:
                    continue
                h = H_canonical(R, X, 1)
                exp = v(sum(X), 1, R) ^ (1 if TAMPER == 'band' else 0)
                cmpd(3, h == exp, [4, 'band', R, list(X), h, exp])
                clear()
            for a in range(2, 6):
                X = allm(m, a)
                if sum(X) < R:
                    continue
                h = H_canonical(R, X, 1)
                exp = v(sum(X), 1, R) ^ (1 if TAMPER == 'band' else 0)
                cmpd(3, h == exp, [4, 'band-allm', R, a, h, exp])
                clear()
        # diagonal R=2m
        R = 2 * m
        for X in shapes(m, R + 2, 4):
            if sum(X) < R:
                continue
            h = H_canonical(R, X, 1)
            exp = v(sum(X), 1, R) ^ (1 if TAMPER == 'band' else 0)
            cmpd(3, h == exp, [4, 'diag', R, list(X), h, exp])
            clear()
        for a in range(2, 6):
            X = allm(m, a)
            if sum(X) < R:
                continue
            h = H_canonical(R, X, 1)
            exp = v(sum(X), 1, R) ^ (1 if TAMPER == 'band' else 0)
            cmpd(3, h == exp, [4, 'diag-allm', R, a, h, exp])
            clear()

    # -------- D5: L-Z1F (z1 delta-3 arm-1 -> >=1) + T-H1 C-anchor --------
    # row-1 wide: X=(1, s_i>=2), budget 5
    for k in range(1, 5):
        for c in combinations_with_replacement(range(2, 10), k):
            X = (1,) + tuple(reversed(c))
            h = H_canonical(5, X, 1)
            cmpd(4, (h == 0) == lzf_flip, [5, 'm1', 5, list(X), h])
            a0 = H_canonical(4, X, 0)
            cmpd(4, a0 == lzf_anchor, [5, 'm1-anchor', 4, list(X), a0])
            clear()
    for m in range(2, 7):
        R = 2 * m + 3
        for X in shapes1(m, m + 7, 5, 1):
            h = H_canonical(R, X, 1)
            cmpd(4, (h == 0) == lzf_flip, [5, 'lzf', R, list(X), h])
            a0 = H_canonical(R - 1, X, 0)
            cmpd(4, a0 == lzf_anchor, [5, 'anchor', R - 1, list(X), a0])
            clear()

    # -------- D6: L-S ((j,j+2) @ z1 delta-3 -> >=2) + stair/anchors --------
    for j in range(1, 8):
        R = 2 * j + 3
        h = H_canonical(R, (j, j + 2), 1)
        cmpd(5, h >= ls_bound, [6, 'LS', R, j, h])
        sc = H_canonical(R - 1, (j, j + 1), 1)
        cmpd(5, sc == ls_stair, [6, 'LS-stair', R - 1, j, sc])
        a0 = H_canonical(R - 1, (j, j + 2), 0)
        cmpd(5, a0 == 1, [6, 'LS-anchor', R - 1, j, a0])
        clear()

    # -------- D7: T-N0z1 (z1 delta-3 mixed never 0) + histogram --------
    for q in range(1, 3):
        for k in range(1, 3):
            for c in combinations_with_replacement(range(2, 9), k):
                X = tuple(sorted([1] * q + list(c), reverse=True))
                h = H_canonical(5, X, 1)
                n0_hist[str(h)] = n0_hist.get(str(h), 0) + 1
                cmpd(6, (h == 0) == n0_flip, [7, 'm1', 5, list(X), h])
                clear()
    for m in range(2, 7):
        R = 2 * m + 3
        for X in shapes(m, m + 6, 4):
            h = H_canonical(R, X, 1)
            n0_hist[str(h)] = n0_hist.get(str(h), 0) + 1
            cmpd(6, (h == 0) == n0_flip, [7, 'n0', R, list(X), h])
            clear()

    # -------- D8: T-IIz1 (z1 delta-3 class E -> >=2) + histogram --------
    for m in range(2, 7):
        R = 2 * m + 3
        for X in shapes(m, m + 7, 5):
            if X.count(m) < 2:
                continue
            mult1 = X.count(m + 1)
            hasD = max(X) >= m + 2
            if (not hasD) and mult1 == 1:
                continue  # arm-2 fall class
            h = H_canonical(R, X, 1)
            ii_hist[str(h)] = ii_hist.get(str(h), 0) + 1
            cmpd(7, (h <= 1) == ii_flip, [8, R, list(X), h])
            clear()

    # -------- D9: G3z2 floor classification (budget-3 z2) + v identities --
    for k in range(2, 6):
        for c in combinations_with_replacement(range(1, 12), k):
            X = tuple(reversed(c))
            h = H_canonical(3, X, 2)
            exp = 2 if TAMPER == 'g3' else (2 if X == (1, 1) else 1)
            cmpd(8, h == exp, [9, 'g3-multi', list(X), h, exp])
            clear()
    # singles: x=1 -> 1, x=2 -> 2, x>=3 -> 1 (v(x,2,3) identity)
    for x in range(1, 16):
        h = H_canonical(3, (x,), 2)
        exp = 2 if x == 2 else 1
        cmpd(8, h == exp and v(x, 2, 3) == h, [9, 'g3-single', x, h, exp])
        clear()
    # budget-2 z3 anchors (B-child bases in the row-1 analysis)
    cmpd(8, H_canonical(2, (1,), 3) == 1, [9, 'b2z3-single-1'])
    clear()
    for x in range(2, 16):
        cmpd(8, H_canonical(2, (x,), 3) == 0, [9, 'b2z3-single-ge2', x])
        clear()
    for k in range(2, 6):
        for c in combinations_with_replacement(range(1, 12), k):
            X = tuple(reversed(c))
            cmpd(8, H_canonical(2, X, 3) == 0, [9, 'b2z3-multi', list(X)])
            clear()
    # v identities used by the proof text
    cmpd(8, v(1, 2, 2) == 1, [9, 'v122'])
    for x in range(2, 16):
        cmpd(8, v(x, 2, 2) == 0, [9, 'v-x22', x])

    # -------- D10: published anchors (both planes) --------
    def g(R, X, z):
        r = H_canonical(R, tuple(sorted(X, reverse=True)), z)
        clear(); return r
    cmpd(9, g(5, (2, 3), 1) == 2, [10, 'K1278-TB-witness'])
    cmpd(9, v(5, 1, 5) == 0, [10, 'K1278-TB-single'])
    cmpd(9, g(5, (3, 2), 0) == 2, [10, 'K1278-TA3-witness'])
    cmpd(9, v(5, 0, 5) == 1, [10, 'K1278-TA3-single'])
    cmpd(9, all(g(R, (1, 1), 0) == v(2, 0, R) for R in range(1, 8)),
         [10, 'K1265-ones-pair'])
    cmpd(9, all(g(3, tuple([1] * t), 1) == (v(t, 1, 3) if t <= 2 else 2)
                for t in range(1, 7)), [10, 'K1269-T2-ones-z1'])
    cmpd(9, all(g(3, tuple([1] * t), 0) == (v(t, 0, 3) if t <= 2 else 0)
                for t in range(1, 7)), [10, 'K1267-T1-ones-z0'])
    for m in range(2, 6):
        for X in shapes(m, m + 3, 4):
            cmpd(9, H_canonical(m + 2, X, 1) == v(sum(X), 1, m + 2),
                 [10, 'K1270-z1', m, list(X)])
            clear()
    # z0 regression anchors consumed by the z1 proof (T-LC/T-Q, m=2..4)
    for m in range(2, 5):
        R = 2 * m + 2
        for X in shapes(m, m + 5, 4):
            mult0 = X.count(m); mult1 = X.count(m + 1)
            hasD = max(X) >= m + 2
            if mult0 == 1:
                pred = 1
            elif (not hasD) and mult1 == 1:
                pred = 1
            else:
                pred = 0
            cmpd(9, H_canonical(R, X, 0) == pred, [10, 'z0-LC', R, list(X)])
            clear()
        Rp = 2 * m + 1
        for X in shapes(m, m + 5, 4):
            cmpd(9, H_canonical(Rp, X, 0) == 2, [10, 'z0-Q', Rp, list(X)])
            clear()
    # z0 diagonal mixed -> 0 (m=2..5, sum>=R regime)
    for m in range(2, 6):
        R = 2 * m
        for X in shapes(m, R + 2, 4):
            if sum(X) < R:
                continue
            cmpd(9, H_canonical(R, X, 0) == 0, [10, 'z0-diag', R, list(X)])
            clear()
    # singles vs closed form: x<=15, z<=7, R<=19, both engines
    for x in range(1, 16):
        for z in range(0, 8):
            for R in range(0, 20):
                cmpd(9, H_canonical(R, (x,), z) == v(x, z, R),
                     [10, 'singles-v', x, z, R])
                cmpd(9, H_ordered(R, (x,), z) == v(x, z, R),
                     [10, 'singles-v-ord', x, z, R])
            clear()

    # volatile run info (timestamps/elapsed) goes to stderr ONLY so that
    # the canonical stdout audit document is byte-identical across runs.
    info = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['h2_ones'] = h2_ones
    res['n0_hist'] = n0_hist
    res['ii_hist'] = ii_hist
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)

main()

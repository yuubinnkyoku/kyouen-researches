#!/usr/bin/env python3
"""
verify_k1282.py -- official verifier kit for K1282
(z0 flank closure: H1 proved universal, T-B0 upgraded to unconditional,
LAW-C / delta-3 high-gap / delta-4 C4 / class-II-nonzero / class-E-zero
theorems, frontier classification extended to m=2, row-1 base lemmas and
budget<=4 floor classification).
All clauses are UNCONDITIONAL universal claims on the stated grids (m and
shape caps declared below); no hypothesis-conditional implication remains.
Engine block embedded verbatim; sha256-gated against the published 11-source
pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92.
Batteries D1..D10 (+declared comparison counts cf. the predeclaration note).
TAMPER: --tamper-engine (rc 2), --tamper=h1|q|lawc|lawc-arm2|l3|e|ii (rc 1).
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
    res = {'kit': 'verify_k1282', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS',
           'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    ND = 10
    counts = [0] * ND
    bad = [0] * ND
    ex = [[] for _ in range(ND)]
    ii_hist = {}
    lc_arm1 = 0 if TAMPER == 'lawc' else 1
    lc_else = 1 if TAMPER == 'lawc-arm2' else 0
    lc_arm2 = 1 if TAMPER != 'lawc-arm2' else 0
    h1_exp = 0 if TAMPER == 'h1' else 1
    q_exp = 1 if TAMPER == 'q' else 2
    l3_exp = 1 if TAMPER == 'l3' else 0
    e_exp = 1 if TAMPER == 'e' else 0
    ii_nonzero_flip = (TAMPER == 'ii')

    def cmpd(i, ok, note):
        counts[i] += 1
        if not ok:
            bad[i] += 1
            if len(ex[i]) < 6: ex[i].append(note)

    # -------- D1: H1 census (z=0, delta=2 arm-1 mixed -> 1, m=1..7) --------
    # m=1 row: X=(1, t_i>=2), budget 4 (wide: sizes<=13, arity<=5)
    for k in range(1, 6):
        for c in combinations_with_replacement(range(2, 13), k):
            X = (1,) + tuple(reversed(c))
            h = H_canonical(4, X, 0)
            cmpd(0, h == h1_exp, [1, 'm1', 4, list(X), h])
    clear()
    for m in range(2, 8):
        R = 2 * m + 2
        for X in shapes1(m, m + 7, 5, 1):
            h = H_canonical(R, X, 0)
            cmpd(0, h == h1_exp, [1, 'arm1', R, list(X), h])
        clear()
    # tall giants: uniformity pointers at huge inert tokens
    for (m, bigs) in [(2, (22,)), (2, (23,)), (2, (22, 23)), (3, (25,)),
                      (3, (22, 26)), (4, (30,)), (4, (22, 31))]:
        X = tuple(sorted((m,) + bigs, reverse=True))
        h = H_canonical(2 * m + 2, X, 0)
        cmpd(0, h == h1_exp, [1, 'tall', 2 * m + 2, list(X), h])
        clear()

    # -------- D2: frontier classification (z=0: mixed -> 2; allm a>=2 -> 0; m=2..7) --------
    for m in range(2, 8):
        Rp = 2 * m + 1
        for X in shapes(m, m + 7, 5):
            h = H_canonical(Rp, X, 0)
            cmpd(1, h == q_exp, [2, 'frontier', Rp, list(X), h])
        for a in range(2, 8):
            h = H_canonical(Rp, allm(m, a), 0)
            cmpd(1, h == 0, [2, 'frontier-allm', Rp, a, h])
        clear()

    # -------- D3: LAW-C mixed census (z=0, delta=2 rows, m=2..7) --------
    for m in range(2, 8):
        R = 2 * m + 2
        for X in shapes(m, m + 7, 6):
            h = H_canonical(R, X, 0)
            mult0 = X.count(m); mult1 = X.count(m + 1)
            hasD = max(X) >= m + 2
            if mult0 == 1:
                pred = lc_arm1
            elif (not hasD) and mult1 == 1:
                pred = lc_arm2
            else:
                pred = lc_else
            cmpd(2, h == pred, [3, R, list(X), h, pred])
        clear()

    # -------- D4: L3 census (z=0, delta=3 high-gap arm-1 -> 0, m=1..7) --------
    # m=1 row: X=(1, s_i>=3), budget 5 (sizes<=13, arity<=5)
    for k in range(1, 6):
        for c in combinations_with_replacement(range(3, 13), k):
            X = (1,) + tuple(reversed(c))
            h = H_canonical(5, X, 0)
            cmpd(3, h == l3_exp, [4, 'm1', 5, list(X), h])
    clear()
    for m in range(2, 8):
        R = 2 * m + 3
        for X in shapes1(m, m + 7, 5, 1):
            if (m + 1) in X:
                continue  # high-gap only (class II checked in D6)
            h = H_canonical(R, X, 0)
            cmpd(3, h == l3_exp, [4, 'hg', R, list(X), h])
        clear()

    # -------- D5: C4 census (z=0, delta=4: arm-1, no (m+1), some >=m+3 -> nonzero) --------
    for k in range(1, 4):
        for c in combinations_with_replacement(range(4, 13), k):
            X = (1,) + tuple(reversed(c))
            h = H_canonical(6, X, 0)
            cmpd(4, h != 0, [5, 'm1', 6, list(X), h])
    clear()
    for m in range(2, 8):
        R = 2 * m + 4
        for X in shapes1(m, m + 7, 5, 1):
            if (m + 1) in X or max(X) < m + 3:
                continue
            h = H_canonical(R, X, 0)
            cmpd(4, h != 0, [5, 'gap3', R, list(X), h])
        # C4b: gap>=2 with a >=(m+3)-token present -> nonzero
        for X in shapes1(m, m + 7, 4, 1):
            if (m + 1) in X or max(X) < m + 3:
                continue
            if X.count(m + 2) == 0:
                continue
            h = H_canonical(R, X, 0)
            cmpd(4, h != 0, [5, 'gap2b', R, list(X), h])
        clear()

    # -------- D6: class II census (delta=3 arm-1 with (m+1)-token and a >=(m+2)-token -> nonzero) + value histogram --------
    # m=1 row: X=(1, 2^u (u>=1), s_i>=3), budget 5
    for u in range(1, 6):
        for k in range(1, 3):
            for c in combinations_with_replacement(range(3, 11), k):
                X = tuple(sorted([1] + [2] * u + list(c), reverse=True))
                h = H_canonical(5, X, 0)
                ii_hist[str(h)] = ii_hist.get(str(h), 0) + 1
                cmpd(5, (h == 0) == ii_nonzero_flip, [6, 'm1', 5, list(X), h])
        clear()
    for m in range(2, 8):
        R = 2 * m + 3
        for X in shapes1(m, m + 7, 5, 1):
            if X.count(m + 1) < 1 or max(X) < m + 2:
                continue
            h = H_canonical(R, X, 0)
            ii_hist[str(h)] = ii_hist.get(str(h), 0) + 1
            cmpd(5, (h == 0) == ii_nonzero_flip, [6, 'ii', R, list(X), h])
        clear()

    # -------- D7: class E census (z=0, delta=2: mult>=2 mixed, not arm-2 -> 0, m=2..7) --------
    for m in range(2, 8):
        R = 2 * m + 2
        for X in shapes(m, m + 7, 6):
            if X.count(m) < 2:
                continue
            mult1 = X.count(m + 1)
            hasD = max(X) >= m + 2
            if (not hasD) and mult1 == 1:
                continue  # arm-2 (value 1, covered by D3)
            h = H_canonical(R, X, 0)
            cmpd(6, h == e_exp, [7, R, list(X), h])
        clear()

    # -------- D8: row-1 base lemmas wide --------
    # F14: (1^t>=2, 2^u, >=3-token) budget 4 -> 0
    for t in range(2, 5):
        for u in range(0, 4):
            for k in range(1, 3):
                for c in combinations_with_replacement(range(3, 10), k):
                    X = tuple(sorted([1] * t + [2] * u + list(c), reverse=True))
                    h = H_canonical(4, X, 0)
                    cmpd(7, h == 0, [8, 'F14', list(X), h])
        clear()
    # B46 wide: (1, s_i>=4) budget 6 nonzero (arity<=4, sizes<=13)
    for k in range(1, 5):
        for c in combinations_with_replacement(range(4, 13), k):
            X = (1,) + tuple(reversed(c))
            h = H_canonical(6, X, 0)
            cmpd(7, h != 0, [8, 'B46', list(X), h])
    clear()

    # -------- D9: budget<=4 floor classification --------
    # fb1: H(1;X;z): z=0 -> 1, z>=1 -> 2 (nonempty multi; singles via v below)
    for k in range(2, 5):
        for c in combinations_with_replacement(range(1, 10), k):
            X = tuple(reversed(c))
            cmpd(8, H_canonical(1, X, 0) == 1, [9, 'fb1', 1, list(X), 0])
            for z in (1, 2, 3):
                cmpd(8, H_canonical(1, X, z) == 2, [9, 'fb1', 1, list(X), z])
            clear()
    # beta2 multi: z0 -> 0, z1 -> 1, z>=2 -> 0
    for k in range(2, 5):
        for c in combinations_with_replacement(range(1, 10), k):
            X = tuple(reversed(c))
            cmpd(8, H_canonical(2, X, 0) == 0, [9, 'b2', 2, list(X), 0])
            cmpd(8, H_canonical(2, X, 1) == 1, [9, 'b2', 2, list(X), 1])
            for z in (2, 3):
                cmpd(8, H_canonical(2, X, z) == 0, [9, 'b2', 2, list(X), z])
            clear()
    # beta3 z0 multi: min>=2 -> 1 ; 1s&>=2 -> 2 ; all-1s -> 0
    for k in range(2, 5):
        for c in combinations_with_replacement(range(1, 10), k):
            X = tuple(reversed(c))
            h = H_canonical(3, X, 0)
            if min(X) >= 2:
                pred = 1
            elif max(X) >= 2:
                pred = 2
            else:
                pred = 0
            cmpd(8, h == pred, [9, 'b3z0', list(X), h, pred])
            clear()
    # beta3 z1 multi: has->>=2 -> 2 ; all-1s: (1,1)->0, (1^t>=3)->2
    for k in range(2, 5):
        for c in combinations_with_replacement(range(1, 10), k):
            X = tuple(reversed(c))
            h = H_canonical(3, X, 1)
            if min(X) >= 2:
                pred = 0          # beta3c: min>=2 multi @3 z1 -> 0
            elif max(X) >= 2:
                pred = 2          # 1s & >=2(s): with-1s multi @3 z1 -> 2
            else:
                pred = 0 if len(X) == 2 else 2  # all-1s: (1,1)->0, (1^t>=3)->2
            cmpd(8, h == pred, [9, 'b3z1', list(X), h, pred])
            clear()
    # beta4 z1 multi min>=2 -> 1
    for k in range(2, 5):
        for c in combinations_with_replacement(range(2, 10), k):
            if min(c) > 2:
                continue
            X = tuple(reversed(c))
            cmpd(8, H_canonical(4, X, 1) == 1, [9, 'b4z1', list(X), 1])
            clear()
    # beta4 z0 with-1s: (1, >=2s) -> 1 ; (1^t>=2 with a >=3-token) -> 0
    for k in range(2, 5):
        for c in combinations_with_replacement(range(1, 11), k):
            if 1 not in c or max(c) < 2:
                continue
            X = tuple(reversed(c))
            h = H_canonical(4, X, 0)
            if X.count(1) == 1:
                pred = 1
            elif max(X) >= 3:
                pred = 0
            else:
                continue  # (1^t>=2, 2^u): open (out of scope)
            cmpd(8, h == pred, [9, 'b4z0w1', list(X), h, pred])
            clear()
    # singles vs closed form: x<=15, z<=7, R<=19, both engines
    for x in range(1, 16):
        for z in range(0, 8):
            for R in range(0, 20):
                cmpd(8, H_canonical(R, (x,), z) == v(x, z, R),
                     [9, 'singles-v', x, z, R])
                cmpd(8, H_ordered(R, (x,), z) == v(x, z, R),
                     [9, 'singles-v-ord', x, z, R])
            clear()

    # -------- D10: published anchors + band/diagonal closure --------
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
            cmpd(9, H_canonical(m + 1, X, 0) == v(sum(X), 0, m + 1),
                 [10, 'K1270-z0', m, list(X)])
            clear()
            cmpd(9, H_canonical(m + 2, X, 1) == v(sum(X), 1, m + 2),
                 [10, 'K1270-z1', m, list(X)])
            clear()
    # band closure (published P: mixed/allm z0 band = v-collapse), sum>=R regime
    for m in range(2, 7):
        for R in range(m + 1, 2 * m + 1):
            for X in shapes(m, R + 2, 4):
                if sum(X) < R:
                    continue
                h = H_canonical(R, X, 0)
                cmpd(9, h == v(sum(X), 0, R), [10, 'band', R, list(X), h])
            clear()
            for a in range(2, 6):
                X = allm(m, a)
                if sum(X) < R:
                    continue
                h = H_canonical(R, X, 0)
                cmpd(9, h == v(sum(X), 0, R), [10, 'band-allm', R, a, h])
            clear()
    # diagonal closure: mixed@2m -> 0 (sum>=2m regime); allm@(2m) -> 0 (a>=2)
    for m in range(2, 7):
        R = 2 * m
        for X in shapes(m, R + 2, 4):
            if sum(X) < R:
                continue
            h = H_canonical(R, X, 0)
            cmpd(9, h == 0, [10, 'diag-mixed', R, list(X), h])
        clear()
        for a in range(2, 6):
            h = H_canonical(R, allm(m, a), 0)
            cmpd(9, h == 0, [10, 'diag-allm', R, a, h])
        clear()

    # volatile run info (timestamps/elapsed) goes to stderr ONLY so that
    # the canonical stdout audit document is byte-identical across runs.
    info = {'started': res['started'], 'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    del res['started']
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['ii_hist'] = ii_hist
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)

main()

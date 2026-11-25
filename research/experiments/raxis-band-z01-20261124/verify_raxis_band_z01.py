#!/usr/bin/env python3
"""
verify_raxis_band_z01.py -- official verifier kit for K1281
(low-z R-axis band z in {0,1}: interior band collapse through the diagonal,
frontier classification conditional package T-B0/T-B1, delta=2 laws).
Observation-only laws are machine-checked on the stated finite grids; the
conditional theorems are implications whose hypotheses are census-observed.
Engine block embedded verbatim; sha256-gated against the published 11-source
pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92.
Batteries D1..D8 (+declared comparison counts cf. the predeclaration note).
TAMPER: --tamper-engine (rc 2), --tamper=lawc, --tamper=lawc-allm (rc 1).
Determinism: 4 official runs byte-identical (volatile timestamps/elapsed are
emitted on stderr only; the canonical stdout JSON is run-independent).
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

def allm(m, a):
    return tuple([m] * a)

def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()

def main():
    t0 = time.time()
    res = {'kit': 'verify_raxis_band_z01', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS',
           'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    counts = [0] * 8
    bad = [0] * 8
    ex = [[] for _ in range(8)]

    def cmpd(i, ok, note):
        counts[i] += 1
        if not ok:
            bad[i] += 1
            if len(ex[i]) < 6: ex[i].append(note)

    # -------- D1: H2 census (z=1, delta=2 rows) --------
    for m in range(1, 9):
        R = 2 * m + 2
        for X in shapes(m, R + 2, 5):
            h = H_canonical(R, X, 1)
            cmpd(0, h == min(sum(X), R) % 2, [1, R, list(X), h])
        for a in range(1, 9):
            pred = v(m, 1, R) if a == 1 else 0
            h = H_canonical(R, allm(m, a), 1)
            cmpd(0, h == pred, [1, 'allm', R, a, h, pred])
        clear()

    # -------- D2: LAW-C census (z=0, delta=2 rows) --------
    for m in range(1, 8):
        R = 2 * m + 2
        for X in shapes(m, R + 2, 6):
            h = H_canonical(R, X, 0)
            mult0 = X.count(m); mult1 = X.count(m + 1)
            hasD = max(X) >= m + 2
            if TAMPER == 'lawc':
                pred = 1
            else:
                pred = 1 if (mult0 == 1 or (not hasD and mult1 == 1)) else 0
            cmpd(1, h == pred, [2, R, list(X), h, pred])
        for a in range(1, 9):
            h = H_canonical(R, allm(m, a), 0)
            pred = v(m, 0, R) if a == 1 else (1 if a == 3 else 0)
            if TAMPER == 'lawc-allm':
                pred = 1 - pred
            cmpd(1, h == pred, [2, 'allm', R, a, h, pred])
        clear()

    # -------- D3: z=0 frontier classification + FB0 identity --------
    for mu in range(2, 9):
        Rp = 2 * mu + 1
        for X in shapes(mu, Rp + 2, 5):
            S = sum(X)
            h = H_canonical(Rp, X, 0)
            cmpd(2, h == 2, [3, 'frontier', Rp, list(X), h])
            c = v(S - 1, 0, Rp - 1)
            cmpd(2, c == 0, [3, 'cval', Rp, list(X), c])
            Xp = list(X); Xp.remove(mu); Xp.append(mu - 1); Xp.sort(reverse=True)
            Dp = H_canonical(Rp - 1, tuple(Xp), 0)
            cmpd(2, Dp == 1 - c, [3, 'fb0', Rp, list(X), Dp])
        for a in range(1, 9):
            h = H_canonical(Rp, allm(mu, a), 0)
            pred = v(mu, 0, Rp) if a == 1 else 0
            cmpd(2, h == pred, [3, 'frontier-allm', Rp, a, h, pred])
        clear()

    # -------- D4: z=1 frontier classification + typed inputs --------
    for mu in range(2, 9):
        Rp = 2 * mu + 1
        for X in shapes(mu, Rp + 2, 5):
            S = sum(X)
            h = H_canonical(Rp, X, 1)
            cmpd(3, h == 2, [4, 'frontier', Rp, list(X), h])
            b = max(X)
            Yb = list(X); Yb.remove(b); Yb.append(b - 1); Yb.sort(reverse=True)
            ab = H_canonical(Rp - 1, tuple(Yb), 1)
            cmpd(3, ab == v(S - 1, 1, Rp - 1) and ab == 1, [4, 'a1', Rp, list(X), ab])
            cc = H_canonical(Rp - 1, X, 0)
            cmpd(3, cc == 0, [4, 'cbase', Rp, list(X), cc])
            Xm = list(X); Xm.remove(mu); Xm.append(mu - 1); Xm.sort(reverse=True)
            am = H_canonical(Rp - 1, tuple(Xm), 1)
            cmpd(3, am == 0, [4, 'sigma', Rp, list(X), am])
        for a in range(1, 9):
            h = H_canonical(Rp, allm(mu, a), 1)
            pred = v(mu, 1, Rp) if a == 1 else (0 if a == 2 else 2)
            cmpd(3, h == pred, [4, 'frontier-allm', Rp, a, h, pred])
        clear()

    # -------- D5: band collapse census --------
    for m in range(2, 8):
        for R in range(m + 1, 2 * m + 1):
            for X in shapes(m, R + 2, 5):
                h = H_canonical(R, X, 0)
                cmpd(4, h == v(sum(X), 0, R), [5, 0, R, list(X), h])
            for a in range(1, 7):
                h = H_canonical(R, allm(m, a), 0)
                cmpd(4, h == v(m * a, 0, R), [5, 0, R, 'a%d' % a, h])
            clear()
        for R in range(m + 2, 2 * m + 1):
            for X in shapes(m, R + 2, 5):
                h = H_canonical(R, X, 1)
                cmpd(4, h == v(sum(X), 1, R), [5, 1, R, list(X), h])
            for a in range(1, 7):
                h = H_canonical(R, allm(m, a), 1)
                cmpd(4, h == v(m * a, 1, R), [5, 1, R, 'a%d' % a, h])
            clear()

    # -------- D6: typed-child structural grid --------
    for m in range(2, 7):
        R = 2 * m
        for X in shapes(m, R + 2, 4):
            h0 = H_canonical(R, X, 0)
            a0 = v(sum(X) - 1, 0, R - 1)
            Mn = list(X); mn = min(X); Mn.remove(mn); Mn.append(mn - 1)
            Mn.sort(reverse=True)
            hc = H_canonical(R - 1, tuple(Mn), 0)
            if hc == 2:
                cmpd(5, h0 == 1 - a0 % 2, [6, 'diag0', R, list(X), h0, a0, hc])
            else:
                cmpd(5, h0 == mex0([a0, hc]), [6, 'diag0*', R, list(X), h0, a0, hc])
            h1 = H_canonical(R, X, 1)
            b1 = v(sum(X) - 1, 1, R - 1)
            cbase = 1 ^ v(sum(X), 0, R - 1)
            cmpd(5, h1 == mex0([b1, hc, cbase]), [6, 'diag1', R, list(X), h1, b1, hc, cbase])
        clear()

    # -------- D7: delta=3 / delta=4 parity batteries --------
    for m in range(2, 7):
        R = 2 * m + 3
        for X in shapes(m, R + 2, 5):
            h = H_canonical(R, X, 1)
            cmpd(6, h != 0, [7, R, list(X), h])
        clear()
    for z in (0, 1):
        for m in range(2, 5):
            R = 2 * m + 4
            for X in shapes(m, R + 2, 4):
                h = H_canonical(R, X, z)
                cmpd(6, h != 2, [7, 'par', z, R, list(X), h])
            clear()
    hist3 = {}
    for m in (2, 3):
        R = 2 * m + 3
        for X in shapes(m, R + 2, 4):
            h = H_canonical(R, X, 0)
            hist3['m%d_h%d' % (m, h)] = hist3.get('m%d_h%d' % (m, h), 0) + 1
        clear()
    cmpd(6, hist3.get('m2_h2', 0) >= 1, [7, 'hist3-2s-present', hist3])

    # -------- D8: published anchors --------
    def g(R, X, z):
        r = H_canonical(R, tuple(sorted(X, reverse=True)), z)
        clear(); return r
    cmpd(7, g(5, (2, 3), 1) == 2, [8, 'K1278-TB-witness'])
    cmpd(7, v(5, 1, 5) == 0, [8, 'K1278-TB-single'])
    cmpd(7, g(5, (3, 2), 0) == 2, [8, 'K1278-TA3-witness'])
    cmpd(7, v(5, 0, 5) == 1, [8, 'K1278-TA3-single'])
    cmpd(7, all(g(R, (1, 1), 0) == v(2, 0, R) for R in range(1, 8)),
         [8, 'K1265-ones-pair'])
    # K1269 (z=1): t=1,2 collapse to v; t>=3 separate with H=2 vs v=0
    cmpd(7, all(g(3, tuple([1] * t), 1) == (v(t, 1, 3) if t <= 2 else 2)
                for t in range(1, 7)), [8, 'K1269-T2-ones-z1'])
    # K1267 (z=0): t=1,2 collapse to v; t>=3 separate with H=0 vs v=1
    cmpd(7, all(g(3, tuple([1] * t), 0) == (v(t, 0, 3) if t <= 2 else 0)
                for t in range(1, 7)), [8, 'K1267-T1-ones-z0'])
    for m in range(2, 6):
        for X in shapes(m, m + 3, 4):
            cmpd(7, H_canonical(m + 1, X, 0) == v(sum(X), 0, m + 1),
                 [8, 'K1270-z0', m, list(X)])
            clear()
            cmpd(7, H_canonical(m + 2, X, 1) == v(sum(X), 1, m + 2),
                 [8, 'K1270-z1', m, list(X)])
            clear()

    # volatile run info (timestamps/elapsed) goes to stderr ONLY so that
    # the canonical stdout audit document is byte-identical across runs.
    info = {'started': res['started'], 'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    del res['started']
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['hist3_z0d3'] = hist3
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)

def mex0(vs):
    s = set(vs)
    m = 0
    while m in s:
        m += 1
    return m

main()

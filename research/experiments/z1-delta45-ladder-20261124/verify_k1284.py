#!/usr/bin/env python3
"""verify_k1284: machine audit for the z1 delta-4/delta-5 ladder package.

Theorems under audit (declarations and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses, it does NOT replace the proofs):

  T-L4z1   for every j>=1 and every arm-1 mixed Y (min=j, mult(j)=1, |Y|>=2)
           with max(Y) >= j+2:  H(2j+4; Y; 1) = 0            [D1]
  L-Z5F    for every m>=1 and U<= [m+2,inf), max(U)>=m+3:
           H(2m+5; (m,U); 1) != 0                            [D2]
  T-LS2    for every j>=1:  H(2j+3; (j,j+2); 1) = 2  (C-LS2 closed)  [D3]
  T-IIz1-2 for every m>=2 class E (mult(m)>=2 mixed non-arm-2):
           H(2m+3; X; 1) = 2 exactly  (C-IIz1-2 closed)      [D4]
  T-ALPHA  for every m>=1 arm-1 mixed Y @ z1-delta-3:
           H = 2 iff Y == (m, m+2), else H = 1               [D5]
  floors   G4z2 (multi min>=2 @ (4,z2) -> 0), W411 ((1,1)@4z1 -> 0),
           BC5-S (v(x,2,5)=1 for x>=3), BC5-M (multi min>=2 @ (5,z2) != 0),
           v(x,2,4)=0 (x>=2), (1,2)@5z1 -> 1                [D6]
  anchors  published K1283 (z1 plane) / K1282 (z0 plane) points re-checked [D7/D8]
  singles  closed form v vs both engines x<=15, z<=7, R<=19 [D9]
  cross-engine canonical vs ordered agreement sweep          [D10]

Engine block embedded verbatim from the published K1283/K1282/K1138 chain,
sha256-gated at startup. TAMPER modes: --tamper-engine (rc 2),
--tamper=l4|z5f|ls2|ii12|alpha|fl (rc 1). Determinism: official runs are
byte-identical on stdout (volatile timestamps/elapsed on stderr only).
"""
import json, hashlib, sys, time
from functools import lru_cache
from itertools import combinations_with_replacement

ENGINE_BLOCK = 'def mex(values):\n    values = set(values)\n    m = 0\n    while m in values:\n        m += 1\n    return m\n\n# ------------------------------------------------------------------\n# Raw engines (verbatim from the published K1138 verifier block; the same\n# transcription is embedded in the published y22 machine K1257).\n# ------------------------------------------------------------------\n@lru_cache(maxsize=6_000_000)\ndef H_ordered(R, X, z):\n    if R == 0:\n        return 0\n    opts = set()\n    for i, v in enumerate(X):\n        if v > 1:\n            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))\n        else:\n            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))\n    if z >= 1:\n        opts.add(1 ^ H_ordered(R - 1, X, z - 1))\n    return mex(opts)\n\n@lru_cache(maxsize=6_000_000)\ndef H_canonical(R, X, z):\n    X = tuple(sorted(X, reverse=True))\n    if R == 0:\n        return 0\n    opts = set()\n    i = 0\n    while i < len(X):\n        v = X[i]\n        if v > 1:\n            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))\n            opts.add(H_canonical(R - 1, child, z))\n        else:\n            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))\n            opts.add(H_canonical(R - 1, child, z + 1))\n        while i + 1 < len(X) and X[i + 1] == v:\n            i += 1\n        i += 1\n    if z >= 1:\n        opts.add(1 ^ H_canonical(R - 1, X, z - 1))\n    return mex(opts)\n\ndef vC(x, z, R):  # canonical-engine single token\n    return H_canonical(R, (x,), z)\ndef vO(x, z, R):  # ordered-engine single token\n    return H_ordered(R, (x,), z)\n\n# ------------------------------------------------------------------\n# Published K0832 single-token closed form (transcription of the published\n# single_token block in the y22 machine K1257; see report provenance).\n# ------------------------------------------------------------------\ndef q_odd(k):\n    return k if k % 2 else k - 1\n\ndef single_token(x, z, R):\n    if R == 0 or x <= 0:\n        return 0\n    if z == 0:\n        return min(R, x) % 2\n    if z == x:\n        if R % 2 and R <= 2 * x - 1:\n            return 2\n        if R % 2 == 0 and R <= x - 1:\n            return 0\n        return x % 2\n    if 1 <= z <= x - 1:\n        m = q_odd(z)\n        if R <= m:\n            return 2 if R % 2 else 0\n        if m < R < x + z:\n            return (R + z) % 2\n        return x % 2\n    if z >= x + 1:\n        m = q_odd(x)\n        if R <= m:\n            return 2 if R % 2 else 0\n        return x % 2\n    raise ValueError((x, z, R))\n'

ENGINE_SHA = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'

if '--tamper-engine' in sys.argv:
    tmp = ENGINE_BLOCK.replace('return k if k % 2 else k - 1',
                               'return k if k % 2 else k')
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

def shapes1(m, hi, amax, mult=1):
    """arm-`mult` mixed shapes (mult copies of the min token m)"""
    for c in shapes(m, hi, amax):
        if c.count(m) == mult:
            yield c

def allm(m, a):
    return tuple([m] * a)

def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()

def main():
    t0 = time.time()
    res = {'kit': 'verify_k1284', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS'}
    ND = 10
    counts = [0] * ND
    bad = [0] * ND
    ex = [[] for _ in range(ND)]
    l4_hist = {}
    z5f_hist = {}
    ls2_val = {}
    alpha_hist = {}

    # tamper expectations
    l4_exp = 1 if TAMPER == 'l4' else 0
    z5f_flip = (TAMPER == 'z5f')      # D2 claim check flips to h == 0
    ls2_exp = 3 if TAMPER == 'ls2' else 2
    ii12_exp = 3 if TAMPER == 'ii12' else 2
    alpha_swap = (TAMPER == 'alpha')  # D5 expectations 1<->2 swapped
    g4_exp = 1 if TAMPER == 'fl' else 0

    def cmpd(i, ok, note):
        counts[i] += 1
        if not ok:
            bad[i] += 1
            if len(ex[i]) < 6: ex[i].append(note)

    # -------- D1: T-L4z1 census (arm-1, max>=j+2 @ z1-delta-4 -> 0) -------
    for j in range(1, 8):
        R = 2 * j + 4
        for Y in shapes1(j, j + 7, 4):
            if max(Y) < j + 2:
                continue
            h = H_canonical(R, Y, 1)
            l4_hist[str(h)] = l4_hist.get(str(h), 0) + 1
            cmpd(0, h == l4_exp, [1, j, list(Y), h, l4_exp])
        clear()
    for j in range(1, 5):
        R = 2 * j + 4
        for extra in [(), (j + 1,), (j + 1, j + 1)]:
            for big in [10, 15, 25, 40]:
                Y = tuple(sorted((j,) + extra + (big,), reverse=True))
                h = H_canonical(R, Y, 1)
                l4_hist[str(h)] = l4_hist.get(str(h), 0) + 1
                cmpd(0, h == l4_exp, [1, 'tall', j, list(Y), h, l4_exp])
            clear()

    # -------- D2: L-Z5F census ((m,U) @ z1-delta-5, max(U)>=m+3 -> != 0) ---
    for m in range(1, 7):
        R = 2 * m + 5
        for k in range(1, 4):
            for c in combinations_with_replacement(range(m + 2, m + 8), k):
                U = tuple(sorted(c, reverse=True))
                if max(U) < m + 3:
                    continue
                X = (m,) + U
                h = H_canonical(R, X, 1)
                z5f_hist[str(h)] = z5f_hist.get(str(h), 0) + 1
                ok = (h == 0) if z5f_flip else (h != 0)
                cmpd(1, ok, [2, m, list(X), h])
            clear()

    # -------- D3: T-LS2 ((j,j+2) @ z1-delta-3 = 2) + child anchors ---------
    for j in range(1, 12):
        R = 2 * j + 3
        h = H_canonical(R, (j + 2, j), 1)
        ls2_val[str(j)] = h
        cmpd(2, h == ls2_exp, [3, 'main', j, h, ls2_exp])
        hs = H_canonical(R - 1, (j + 1, j), 1)   # stair child = 1 (T-H2 sp.)
        cmpd(2, hs == 1, [3, 'stair', j, hs])
        hc = H_canonical(R - 1, (j + 2, j), 0)   # C-plane = 1 (T-H1)
        cmpd(2, hc == 1, [3, 'cplane', j, hc])
        if j >= 2:
            hf = H_canonical(R - 1, (j + 2, j - 1), 1)  # fall child = 0
            cmpd(2, hf == 0, [3, 'fall', j, hf])
        clear()

    # -------- D4: T-IIz1-2 census (class E @ z1-delta-3 = 2 exactly) -------
    for m in range(2, 7):
        R = 2 * m + 3
        for q in range(2, 5):
            for k in range(0, 4):
                for c in combinations_with_replacement(range(m + 1, m + 6), k):
                    Y = tuple(sorted((m,) * q + c, reverse=True))
                    if max(Y) == m:
                        continue
                    if max(Y) <= m + 1 and Y.count(m + 1) == 1:
                        continue  # arm-2 excluded (class E = non-arm-2)
                    h = H_canonical(R, Y, 1)
                    cmpd(3, h == ii12_exp, [4, m, list(Y), h, ii12_exp])
                clear()
    # child anchors: fall child = 0 (T-L4z1 at row m-1), C-plane = 0 (T-E),
    # allm corner (m^(q+1)) @ z1-delta-2 = 0 (T-E1)
    for m in range(2, 6):
        R = 2 * m + 3
        for (q, c) in [(2, ()), (2, (m + 2,)), (3, (m + 1, m + 1)),
                       (2, (m + 1, m + 2)), (4, (m + 3,))]:
            Y = tuple(sorted((m,) * q + c, reverse=True))
            if max(Y) == m or (max(Y) <= m + 1 and Y.count(m + 1) == 1):
                continue
            fall = tuple(sorted((m - 1,) + (m,) * (q - 1) + c, reverse=True))
            hf = H_canonical(R - 1, fall, 1)
            cmpd(3, hf == 0, [4, 'fall', m, list(fall), hf])
            hc = H_canonical(R - 1, Y, 0)
            cmpd(3, hc == 0, [4, 'cplane', m, list(Y), hc])
            hallm = H_canonical(R - 1, allm(m, q + 1), 1)
            cmpd(3, hallm == 0, [4, 'allm-corner', m, q, hallm])
        clear()

    # -------- D5: T-ALPHA census (arm-1 @ z1-delta-3: 2 iff (m,m+2)) ------
    for m in range(1, 8):
        R = 2 * m + 3
        for Y in shapes1(m, m + 7, 5):
            h = H_canonical(R, Y, 1)
            exp = 2 if Y == (m + 2, m) else 1
            if alpha_swap:
                exp = 1 if exp == 2 else 2
            alpha_hist[str(h)] = alpha_hist.get(str(h), 0) + 1
            cmpd(4, h == exp, [5, m, list(Y), h, exp])
        clear()
    for k in range(2, 5):
        for c in combinations_with_replacement(range(2, 8), k):
            Y = tuple(sorted((1,) + c, reverse=True))
            h = H_canonical(5, Y, 1)
            exp = 2 if Y == (3, 1) else 1
            if alpha_swap:
                exp = 1 if exp == 2 else 2
            alpha_hist[str(h)] = alpha_hist.get(str(h), 0) + 1
            cmpd(4, h == exp, [5, 1, list(Y), h, exp])
        clear()

    # -------- D6: floors G4z2 / W411 / BC5 / v identities ------------------
    for k in range(2, 5):
        for c in combinations_with_replacement(range(2, 9), k):
            X = tuple(sorted(c, reverse=True))
            h4 = H_canonical(4, X, 2)
            cmpd(5, h4 == g4_exp, [6, 'G4z2', list(X), h4, g4_exp])
            h5 = H_canonical(5, X, 2)
            cmpd(5, h5 != 0, [6, 'BC5-M', list(X), h5])
        clear()
    cmpd(5, H_canonical(4, (1, 1), 1) == 0, [6, 'W411', H_canonical(4, (1, 1), 1)])
    cmpd(5, H_canonical(5, (1, 2), 1) == 1, [6, 'A12-d5z1', H_canonical(5, (1, 2), 1)])
    for x in range(2, 21):
        cmpd(5, H_canonical(4, (x,), 2) == 0, [6, 'v2R4', x, H_canonical(4, (x,), 2)])
    for x in range(3, 21):
        cmpd(5, H_canonical(5, (x,), 2) == 1, [6, 'BC5-S', x, H_canonical(5, (x,), 2)])
    clear()

    # -------- D7: published K1283 anchors (z1 plane) ----------------------
    for m in range(1, 8):
        cmpd(6, H_canonical(2 * m + 2, (m + 1, m), 1) == 1,
             [7, 'H2-special', m])
        clear()
    for m in range(1, 5):
        for a in range(2, 6):
            cmpd(6, H_canonical(2 * m + 2, allm(m, a), 1) == 0,
                 [7, 'T-E1', m, a])
            clear()
    for m in range(2, 5):
        Rf = 2 * m + 1
        for X in shapes(m, m + 3, 3):
            cmpd(6, H_canonical(Rf, X, 1) == 2, [7, 'Q1-mixed', m, list(X)])
            clear()
        cmpd(6, H_canonical(Rf, allm(m, 2), 1) == 0, [7, 'Q1-allm2', m])
        for a in range(3, 5):
            cmpd(6, H_canonical(Rf, allm(m, a), 1) == 2, [7, 'Q1-allm', m, a])
        clear()
    for m in range(1, 6):
        R = 2 * m + 3
        for X in shapes(m, m + 4, 3):
            h = H_canonical(R, X, 1)
            cmpd(6, h != 0, [7, 'N0', m, list(X), h])
            clear()
    cmpd(6, H_canonical(3, (1, 1), 2) == 2, [7, 'G3z2-11'])
    cmpd(6, H_canonical(3, (2, 1), 2) == 1, [7, 'G3z2-12'])
    cmpd(6, H_canonical(3, (2, 2), 2) == 1, [7, 'G3z2-22'])
    cmpd(6, H_canonical(3, (1, 1, 1), 2) == 1, [7, 'G3z2-111'])
    cmpd(6, H_canonical(2, (1,), 3) == 1, [7, 'B2z3-1'])
    cmpd(6, H_canonical(2, (2,), 3) == 0, [7, 'B2z3-2'])
    cmpd(6, H_canonical(2, (1, 1), 3) == 0, [7, 'B2z3-11'])
    for m in range(2, 6):
        for R in range(m + 2, 2 * m + 1):
            for X in shapes(m, R + 2, 3):
                if sum(X) < R:
                    continue
                cmpd(6, H_canonical(R, X, 1) == v(sum(X), 1, R),
                     [7, 'band', m, R, list(X)])
                clear()

    # -------- D8: published K1282 anchors (z0 plane) ----------------------
    for m in range(1, 6):
        R = 2 * m + 2
        for X in shapes1(m, m + 3, 3):
            cmpd(7, H_canonical(R, X, 0) == 1, [8, 'T-H1', m, list(X)])
            clear()
    for m in range(1, 6):
        R = 2 * m + 3
        for X in shapes1(m, m + 4, 3):
            if X.count(m + 1) > 0 or max(X) < m + 2:
                continue
            cmpd(7, H_canonical(R, X, 0) == 0, [8, 'T-L3', m, list(X)])
            clear()
    for m in range(1, 6):
        R = 2 * m + 4
        for c in combinations_with_replacement(range(m + 2, m + 6), 2):
            X = tuple(sorted((m,) + c, reverse=True))
            if max(X) < m + 3:
                continue
            h = H_canonical(R, X, 0)
            cmpd(7, h != 0, [8, 'T-C4', m, list(X), h])
            clear()
    for m in range(2, 5):
        Rf = 2 * m + 1
        for X in shapes(m, m + 3, 3):
            cmpd(7, H_canonical(Rf, X, 0) == 2, [8, 'T-Q', m, list(X)])
            clear()
        for a in range(2, 4):
            cmpd(7, H_canonical(Rf, allm(m, a), 0) == 0, [8, 'T-Qallm', m, a])
        clear()
    for m in range(2, 5):
        R = 2 * m + 2
        for X in shapes(m, m + 4, 4):
            mult0 = X.count(m); mult1 = X.count(m + 1)
            if mult0 == 1:
                pred = 1
            elif max(X) <= m + 1 and mult1 == 1:
                pred = 1
            else:
                pred = 0
            cmpd(7, H_canonical(R, X, 0) == pred, [8, 'T-LC', m, list(X)])
            clear()
    for m in range(1, 5):
        R = 2 * m + 3
        for X in shapes1(m, m + 5, 4):
            if X.count(m + 1) == 0 or max(X) < m + 2:
                continue
            h = H_canonical(R, X, 0)
            cmpd(7, h >= 2, [8, 'T-II', m, list(X), h])
            clear()
    for m in range(2, 5):
        R = 2 * m + 2
        for X in shapes(m, m + 4, 4):
            if X.count(m) >= 2 and not (max(X) <= m + 1 and X.count(m + 1) == 1):
                cmpd(7, H_canonical(R, X, 0) == 0, [8, 'T-E', m, list(X)])
            clear()
    for t in range(2, 7):
        cmpd(7, H_canonical(4, (t, 1), 0) == 1, [8, 'J1', t])
        clear()
    for s in range(3, 8):
        cmpd(7, H_canonical(5, (s, 1), 0) == 0, [8, 'J2', s])
        clear()

    # -------- D9: singles vs closed form, both engines --------------------
    for x in range(1, 16):
        for z in range(0, 8):
            for R in range(0, 20):
                cmpd(8, H_canonical(R, (x,), z) == v(x, z, R),
                     [9, 'singles-v', x, z, R])
                cmpd(8, H_ordered(R, (x,), z) == v(x, z, R),
                     [9, 'singles-v-ord', x, z, R])
            clear()

    # -------- D10: cross-engine agreement sweep ----------------------------
    for R in range(1, 9):
        for k in range(1, 4):
            for c in combinations_with_replacement(range(1, 7), k):
                X = tuple(sorted(c, reverse=True))
                for z in range(0, 3):
                    hc = H_canonical(R, X, z)
                    ho = H_ordered(R, X, z)
                    cmpd(9, hc == ho, [10, 'xeng', R, list(X), z, hc, ho])
            clear()
    for (R, X) in [(6, (40, 1)), (6, (10, 11, 2)), (9, (15, 2)),
                   (9, (15, 1)), (8, (2, 2, 14))]:
        for z in range(0, 3):
            hc = H_canonical(R, X, z)
            ho = H_ordered(R, tuple(sorted(X)), z)
            cmpd(9, hc == ho, [10, 'xeng-tall', R, list(X), z, hc, ho])
        clear()

    # volatile run info (timestamps/elapsed) goes to stderr ONLY so that
    # the canonical stdout audit document is byte-identical across runs.
    info = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['l4_hist'] = l4_hist
    res['z5f_hist'] = z5f_hist
    res['ls2_val'] = ls2_val
    res['alpha_hist'] = alpha_hist
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)

main()

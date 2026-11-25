#!/usr/bin/env python3
"""verify_k1286: machine audit for the border-slices / pre-diagonal package.

Theorems under audit (declarations and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of the
hand proofs, it does NOT replace the proofs; all quantifiers in the theorems
are UNBOUNDED, censuses are consistency checks only):

  D1  T-PD0  z0 pre-diagonal pair law:
               H(R; (m, m+g); 0) = f0(R-2m) for every m>=1, g>=1,
               0 <= R <= 2m+g, where f0(d) = 2 if d==1; [d odd] if d<=0;
               [d even] if d>=2.   Battery: m<=14, g<=21, k in
               [max(-26,-2m-g), 0]                                  [6719]
  D2  typed-proof z0 + uniformity lemmas:
               (a) typed-children mex == f0 claim == engine on the
                   z0 pre-diagonal band m<=12, g<=15, k>=-15         [2677]
               (b) typed z0 beds (m,m)@2m+j, j in [-12..0]            [126]
               (c) L-BU0: single_token(w,1,t) == f0(t) == engine,
                   w 2..30, t 0..w (m=1 B-child of the z0 law)        [493]
               (d) L-BU1: single_token(w,2,w+k) == z1k(k,w)
                   == engine, w 2..30, k in {-1,0,1}                  [87]
               (e) L-BU2: single_token(w,3,w+k) == z2k(k,w)
                   == engine, w 2..30, k in {0,1,2}                    [87]
  D3  Z1[-1,0,1] z1 border slices:
               k=1: g=1->1, g=2->2, g>=3->[g even]
               k=0: g=1->2,        g>=2->[g odd]
               k=-1: g=1->1, g=2->2, g>=3->[g even]
               engine AND typed mex on m<=14, g<=21                    [882]
  D4  z1 beds b1(j): j=1 -> 0 (published front line, all m>=1),
               j=0 -> 1, j=-1 -> 0 (m>=2) / 2 (m=1);
               typed == claim == engine, m 1..14                       [42]
  D5  Z2[0,1,2] z2 border slices:
               k=2: g=1->1, g=2->0, g=3->2, g>=4->[g even]
               k=1: [g odd] (clean; promotes K1285 OBS z2k1)
               k=0: g=1->1, g=2->0, g=3->2, g>=4->[g even]
               engine AND typed mex on m<=14, g<=21                    [882]
  D6  z2 beds b2(j): j=2 -> 0, j=1 -> 2, j=0 -> 0;
               typed == claim == engine, m 1..14                        [42]
  D7  z0 beds b0(j) = f0(j) for j in [-12..0] (R>=0), m<=14,
               engine vs claim                                        [152]
  D8  published anchor recheck: interior 7 slice families [g odd]
               (T-PS0/1/2, K1285) m<=20 g<=16; T-ALM 6 allm-zeros
               m<=20; T-Q corner (m,m)@2m+1 z0 = 0 m<=20; K1285 floors
               and L-EMPTY grid; singles closed form vs BOTH engines;
               C-PB2/C-PC pre-band corollaries                        [2910]
  D9  cross-engine canonical vs ordered on pre-diag band, borders,
               beds; drift check of the K1285 OBS pattern functions
               P0/P1/P2/z2k1-clean against the new proven tables
               (function identity g<=200 + engine recheck m<=8 g<=14) [2353]
  D10 OBS    finite observations (NO universal claims): F2 spread web
               F_d(m,c)/G_d(m,c), d in {1,2,3}, m<=8, c<=6; z1-k(-2)
               nucleation rows; z2-k(-1) m-uniform rows; z2-k(-2)
               pattern rows, m 1..9, g 1..14                            [666]

Totals: 18118 comparisons, expected overall_bad == 0.

Engine block embedded verbatim from the published K1138/K1282/K1283/K1284/
K1285 chain, sha256-gated at startup. TAMPER modes: --tamper-engine (rc 2),
--tamper=f0|z1|z2|bed1|bed2 (rc 1; flips the claim in the engine-vs-claim
batteries D1/D3/D4/D5/D6/D7 only, as in K1285). Determinism: official runs
are byte-identical on stdout (volatile timestamps/elapsed on stderr only).
"""
import json, hashlib, sys, time
from functools import lru_cache

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

FAMS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (2, 4)]

def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()

def godd(g):
    return 1 if g % 2 == 1 else 0

def IND(b):
    return 1 if b else 0

# ---- claim tables (the universal laws proven in the declaration note) ----
def f0(d):
    if d == 1:
        return 2
    if d <= 0:
        return IND(d % 2 == 1)
    return IND(d % 2 == 0)

def z1k(k, g):
    if k == 1:
        if g == 1: return 1
        if g == 2: return 2
        return IND(g % 2 == 0)
    if k == 0:
        if g == 1: return 2
        return IND(g % 2 == 1)
    if k == -1:
        if g == 1: return 1
        if g == 2: return 2
        return IND(g % 2 == 0)
    raise ValueError((k, g))

def z2k(k, g):
    if k in (0, 2):
        if g == 1: return 1
        if g == 2: return 0
        if g == 3: return 2
        return IND(g % 2 == 0)
    if k == 1:
        return IND(g % 2 == 1)
    raise ValueError((k, g))

def bed0(j, m):
    return f0(j)

def bed1(j, m):
    if j == 1: return 0
    if j == 0: return 1
    if j == -1: return 0 if m >= 2 else 2
    raise ValueError((j, m))

def bed2(j, m):
    if j == 2: return 0
    if j == 1: return 2
    if j == 0: return 0
    raise ValueError((j, m))

def flipC(val):
    # tamper flip for engine-vs-claim batteries (K1285 semantics)
    return 1 - val if val in (0, 1) else 1

def mexs(vals):
    s = set(vals)
    x = 0
    while x in s:
        x += 1
    return x

# ---- typed-children analysis (children valued by the CLAIM tables and the
# published K0832 closed form only; no engine recursion for children) -----
def typed_pair(R, m, g, z):
    """mex of claimed child values for pair (m, m+g) @ (R, z)."""
    if R == 0:
        return 0
    k = R - 2 * m - g
    d = R - 2 * m
    kids = []
    # move on the lower token m (fall / B-removal)
    if m >= 2:
        if z == 0:
            kids.append(f0(d + 1))
        elif z == 1:
            kids.append(z1k(k, g + 1))
        else:
            kids.append(z2k(k, g + 1))
    else:
        kids.append(v(g + 1, z + 1, R - 1))  # B-child, K0832 closed form
    # move on the upper token m+g (compress / corner bed)
    if g >= 2:
        if z == 0:
            kids.append(f0(d - 1))
        elif z == 1:
            kids.append(z1k(k, g - 1))
        else:
            kids.append(z2k(k, g - 1))
    else:
        if z == 0:
            kids.append(bed0(k, m))
        elif z == 1:
            kids.append(bed1(k, m))
        else:
            kids.append(bed2(k, m))
    # C move
    if z >= 1:
        if z == 1:
            kids.append(1 ^ f0(d - 1))
        else:
            kids.append(1 ^ z1k(k - 1, g))
    return mexs(kids)

def typed_bed(R, m, j, z):
    """mex of claimed child values for bed (m,m) @ (R=2m+j, z)."""
    if R == 0:
        return 0
    kids = []
    if m >= 2:
        if z == 0:
            kids.append(f0(j + 1))   # A-child pair (m-1, m)
        elif z == 1:
            kids.append(z1k(j, 1))   # A-child pair (m-1, m), gap 1
        else:
            kids.append(z2k(j, 1))
    else:
        kids.append(v(1, z + 1, R - 1))  # B-child single token 1
    if z >= 1:
        if z == 1:
            kids.append(1 ^ bed0(j - 1, m))
        else:
            kids.append(1 ^ bed1(j - 1, m))
    return mexs(kids)

def main():
    t0 = time.time()
    res = {'kit': 'verify_k1286', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS', 'tamper': TAMPER}
    ND = 10
    counts = [0] * ND
    bad = [0] * ND
    ex = [[] for _ in range(ND)]
    hists = {}
    obs = {}

    f0_flip = (TAMPER == 'f0')
    z1_flip = (TAMPER == 'z1')
    z2_flip = (TAMPER == 'z2')
    b1_flip = (TAMPER == 'bed1')
    b2_flip = (TAMPER == 'bed2')

    def cmpd(i, ok, note):
        counts[i] += 1
        if not ok:
            bad[i] += 1
            if len(ex[i]) < 6: ex[i].append(note)

    def pairR(z, k, m, g):
        R = 2 * m + g + k
        return H_canonical(R, tuple(sorted([m, m + g], reverse=True)), z)

    # -------- D1: T-PD0 z0 pre-diagonal band ----------------------------
    for m in range(1, 15):
        for g in range(1, 22):
            for k in range(max(-26, -2 * m - g), 1):
                R = 2 * m + g + k
                h = pairR(0, k, m, g)
                hists.setdefault('D1_f0_class', {})
                hists['D1_f0_class'][str(h)] = hists['D1_f0_class'].get(str(h), 0) + 1
                exp = flipC(f0(R - 2 * m)) if f0_flip else f0(R - 2 * m)
                cmpd(0, h == exp, [1, m, g, k, h, exp])
        clear()

    # -------- D2: typed-proof z0 + uniformity lemmas ---------------------
    # (a) typed z0 pre-diagonal band
    for m in range(1, 13):
        for g in range(1, 16):
            for k in range(max(-15, -2 * m - g), 1):
                R = 2 * m + g + k
                exp = f0(R - 2 * m)
                mx = typed_pair(R, m, g, 0)
                h = H_canonical(R, tuple(sorted([m, m + g], reverse=True)), 0)
                cmpd(1, mx == exp == h, [2, 'a', m, g, k, exp, mx, h])
        clear()
    # (b) typed z0 beds j in [-12..0]
    for m in range(1, 13):
        for j in range(-12, 1):
            R = 2 * m + j
            if R < 0:
                continue
            exp = bed0(j, m)
            mx = typed_bed(R, m, j, 0)
            h = H_canonical(R, (m, m), 0)
            cmpd(1, mx == exp == h, [2, 'b', m, j, exp, mx, h])
        clear()
    # (c) L-BU0 uniformity: V(w,1,t) == f0(t) == engine, 0 <= t <= w
    for w in range(2, 31):
        for t in range(0, w + 1):
            vc = v(w, 1, t)
            hc = vC(w, 1, t)
            cmpd(1, vc == f0(t) and hc == f0(t), [2, 'c', w, t, vc, hc, f0(t)])
        clear()
    # (d) L-BU1: V(w,2,w+k) == z1k(k,w) == engine, k in {-1,0,1}
    for w in range(2, 31):
        for k in (-1, 0, 1):
            t = w + k
            vc = v(w, 2, t)
            hc = vC(w, 2, t)
            cmpd(1, vc == z1k(k, w) and hc == z1k(k, w),
                 [2, 'd', w, k, vc, hc, z1k(k, w)])
        clear()
    # (e) L-BU2: V(w,3,w+k) == z2k(k,w) == engine, k in {0,1,2}
    for w in range(2, 31):
        for k in (0, 1, 2):
            t = w + k
            vc = v(w, 3, t)
            hc = vC(w, 3, t)
            cmpd(1, vc == z2k(k, w) and hc == z2k(k, w),
                 [2, 'e', w, k, vc, hc, z2k(k, w)])
        clear()

    # -------- D3: z1 border slices k in {-1,0,1} ------------------------
    for m in range(1, 15):
        for g in range(1, 22):
            for k in (-1, 0, 1):
                R = 2 * m + g + k
                h = pairR(1, k, m, g)
                exp = flipC(z1k(k, g)) if z1_flip else z1k(k, g)
                mx = typed_pair(R, m, g, 1)
                cmpd(2, h == exp and mx == z1k(k, g),
                     [3, m, g, k, h, exp, mx])
        clear()

    # -------- D4: z1 beds j in {-1,0,1} ---------------------------------
    for m in range(1, 15):
        for j in (-1, 0, 1):
            R = 2 * m + j
            h = H_canonical(R, (m, m), 1)
            exp = flipC(bed1(j, m)) if b1_flip else bed1(j, m)
            mx = typed_bed(R, m, j, 1)
            cmpd(3, h == exp and mx == bed1(j, m), [4, m, j, h, exp, mx])
        clear()

    # -------- D5: z2 border slices k in {0,1,2} -------------------------
    for m in range(1, 15):
        for g in range(1, 22):
            for k in (0, 1, 2):
                R = 2 * m + g + k
                h = pairR(2, k, m, g)
                exp = flipC(z2k(k, g)) if z2_flip else z2k(k, g)
                mx = typed_pair(R, m, g, 2)
                cmpd(4, h == exp and mx == z2k(k, g),
                     [5, m, g, k, h, exp, mx])
        clear()

    # -------- D6: z2 beds j in {0,1,2} ----------------------------------
    for m in range(1, 15):
        for j in (0, 1, 2):
            R = 2 * m + j
            h = H_canonical(R, (m, m), 2)
            exp = flipC(bed2(j, m)) if b2_flip else bed2(j, m)
            mx = typed_bed(R, m, j, 2)
            cmpd(5, h == exp and mx == bed2(j, m), [6, m, j, h, exp, mx])
        clear()

    # -------- D7: z0 beds b0(j) = f0(j), j in [-12..0], engine ----------
    for m in range(1, 15):
        for j in range(-12, 1):
            R = 2 * m + j
            if R < 0:
                continue
            h = H_canonical(R, (m, m), 0)
            exp = flipC(f0(j)) if f0_flip else f0(j)
            cmpd(6, h == exp, [7, m, j, h, exp])
        clear()

    # -------- D8: published anchor recheck ------------------------------
    for (z, k) in FAMS:
        for m in range(1, 21):
            for g in range(1, 17):
                h = pairR(z, k, m, g)
                cmpd(7, h == godd(g), [8, 'FAM', z, k, m, g, h, godd(g)])
            clear()
    for m in range(1, 21):
        for (off, z) in [(2, 0), (3, 0), (2, 1), (3, 1), (3, 2), (4, 2)]:
            h = H_canonical(2 * m + off, (m, m), z)
            cmpd(7, h == 0, [8, 'ALM', m, off, z, h, 0])
        clear()
    for m in range(1, 21):  # T-Q corner: (m,m)@2m+1 z0 = 0
        h = H_canonical(2 * m + 1, (m, m), 0)
        cmpd(7, h == 0, [8, 'TQ', m, h, 0])
    clear()
    for (R, X, z, val) in [(3, (1, 1), 0, 0), (4, (1, 1), 0, 0),
                           (2, (1,), 1, 1), (3, (1,), 1, 1), (4, (1,), 1, 1)]:
        h = H_canonical(R, X, z)
        cmpd(7, h == val, [8, 'FLOOR', R, list(X), z, h, val])
    for R in range(0, 7):
        for z in range(0, 5):
            h = H_canonical(R, (), z)
            cmpd(7, h == 0, [8, 'EMPTY', R, z, h])
    clear()
    for x in range(2, 17):
        for z in (1, 2, 3):
            for R in range(x + 1, x + 5):
                hc = vC(x, z, R)
                ho = vO(x, z, R)
                cmpd(7, hc == v(x, z, R), [8, 'SVC', x, z, R, hc, v(x, z, R)])
                cmpd(7, ho == v(x, z, R), [8, 'SVO', x, z, R, ho, v(x, z, R)])
            clear()
    for x in range(2, 15):
        for c in range(1, 6):
            exp = (x % 2) if c == 1 else (1 - x % 2)
            X = tuple([x] * c)
            h1 = H_canonical(x + 2, X, 1)
            cmpd(7, h1 == exp, [8, 'PB2', x, c, h1, exp])
            h0 = H_canonical(x + 1, X, 0)
            cmpd(7, h0 == exp, [8, 'PC', x, c, h0, exp])
            clear()

    # -------- D9: cross-engine + K1285 OBS drift check ------------------
    for m in range(1, 9):
        for g in range(1, 12):
            for k in range(max(-4, -2 * m - g), 1):
                R = 2 * m + g + k
                X = tuple(sorted([m, m + g], reverse=True))
                hc = H_canonical(R, X, 0)
                ho = H_ordered(R, X, 0)
                cmpd(8, hc == ho, [9, 'PD0', m, g, k, hc, ho])
        clear()
    for z in (1, 2):
        for k in ((-1, 0, 1) if z == 1 else (0, 1, 2)):
            for m in range(1, 9):
                for g in range(1, 12):
                    R = 2 * m + g + k
                    X = tuple(sorted([m, m + g], reverse=True))
                    hc = H_canonical(R, X, z)
                    ho = H_ordered(R, X, z)
                    cmpd(8, hc == ho, [9, 'SL', z, k, m, g, hc, ho])
                clear()
    for m in range(1, 9):
        for z in (0, 1, 2):
            for j in range(-4, 2):
                R = 2 * m + j
                if R < 0:
                    continue
                hc = H_canonical(R, (m, m), z)
                ho = H_ordered(R, (m, m), z)
                cmpd(8, hc == ho, [9, 'BED', m, z, j, hc, ho])
        clear()
    # K1285 OBS pattern functions must EQUAL the new proven tables:
    def P0(g):  # K1285 observed z0-k0 pattern
        if g == 1: return 2
        if g == 2: return 1
        if g == 3: return 0
        return 0 if g % 2 == 1 else 1
    def P1(g):  # K1285 observed z1-k1 pattern
        if g == 1: return 1
        if g == 2: return 2
        if g == 3: return 0
        return 0 if g % 2 == 1 else 1
    def P2(g):  # K1285 observed z2-k2 pattern
        if g == 1: return 1
        if g == 2: return 0
        if g == 3: return 2
        return 0 if g % 2 == 1 else 1
    for g in range(1, 201):
        cmpd(8, P0(g) == f0(g), [9, 'DRIFT-P0', g, P0(g), f0(g)])
        cmpd(8, P1(g) == z1k(1, g), [9, 'DRIFT-P1', g, P1(g), z1k(1, g)])
        cmpd(8, P2(g) == z2k(2, g), [9, 'DRIFT-P2', g, P2(g), z2k(2, g)])
        cmpd(8, godd(g) == z2k(1, g), [9, 'DRIFT-C1', g, godd(g), z2k(1, g)])
    for (z, k, fn, tag) in [(0, 0, P0, 'z0k0'), (1, 1, P1, 'z1k1'),
                            (2, 1, godd, 'z2k1'), (2, 2, P2, 'z2k2')]:
        match = 0; mism = 0
        for m in range(1, 9):
            for g in range(1, 15):
                h = pairR(z, k, m, g)
                ok = (h == fn(g))
                if ok: match += 1
                else:
                    mism += 1
                    if len(ex[8]) < 6: ex[8].append([9, tag, m, g, h, fn(g)])
                cmpd(8, ok, [9, tag, m, g, h, fn(g)])
            clear()
        obs['recheck_' + tag] = {'matches': match, 'mismatches': mism,
                                 'm': '1..8', 'g': '1..14',
                                 'claim': 'K1285 OBS promotion: engine rows '
                                          'agree with the now-proven tables'}

    # -------- D10: finite observations (NO universal claims) ------------
    # F2 web: F_d(m,c) = H(2m+d+3; {m} U {(m+d)^c}; 1)
    #         G_d(m,c) = H(2m+d+2; {m} U {(m+d)^c}; 0),  d in {1,2,3}
    def Fexp(d, c):
        if d == 1: return 1 if c == 1 else 0
        if d == 2: return 0 if c == 1 else 1
        return 1 if c == 1 else 0  # d == 3
    def Gexp(d, c):
        if d == 1:
            return 1 if c == 1 else (0 if c == 2 else 2)
        if d == 2: return 0 if c == 1 else 1
        return 1 if c == 1 else 0   # d == 3
    matchF = mismF = matchG = mismG = 0
    for d in (1, 2, 3):
        for m in range(1, 9):
            for c in range(1, 7):
                X = tuple(sorted([m] + [m + d] * c, reverse=True))
                hF = H_canonical(2 * m + d + 3, X, 1)
                eF = Fexp(d, c)
                if hF == eF: matchF += 1
                else:
                    mismF += 1
                    if len(ex[9]) < 6: ex[9].append([10, 'F', d, m, c, hF, eF])
                cmpd(9, hF == eF, [10, 'F', d, m, c, hF, eF])
                hG = H_canonical(2 * m + d + 2, X, 0)
                eG = Gexp(d, c)
                if hG == eG: matchG += 1
                else:
                    mismG += 1
                    if len(ex[9]) < 6: ex[9].append([10, 'G', d, m, c, hG, eG])
                cmpd(9, hG == eG, [10, 'G', d, m, c, hG, eG])
            clear()
    obs['F2web_F'] = {'matches': matchF, 'mismatches': mismF,
                      'd': '1..3', 'm': '1..8', 'c': '1..6',
                      'claim': 'finite observation only (c>=2 columns new; '
                               'c=1 columns are published slice instances)'}
    obs['F2web_G'] = {'matches': matchG, 'mismatches': mismG,
                      'd': '1..3', 'm': '1..8', 'c': '1..6',
                      'claim': 'finite observation only (G_1 c>=3 -> 2)'}
    # z1-k(-2): m=1 nucleation vs m>=2 rows
    def z1km2(m, g):
        if g == 1: return 2 if m == 1 else 0
        if g == 2: return 1
        if g == 3: return 2
        return IND(g % 2 == 1)
    mm = 0
    for m in range(1, 10):
        for g in range(1, 15):
            h = pairR(1, -2, m, g)
            e = z1km2(m, g)
            cmpd(9, h == e, [10, 'z1km2', m, g, h, e])
            mm += 1
        clear()
    obs['z1km2'] = {'points': mm, 'm': '1..9', 'g': '1..14',
                    'claim': 'finite observation only (m=1,g=1 nucleation; '
                             'z1 pre-diag is NOT delta-1D)'}
    # z2-k(-1): m-uniform rows
    def z2km1(m, g):
        if g == 1: return 0
        if g == 2: return 1
        if g == 3: return 0
        if g == 4: return 2
        return IND(g % 2 == 1)
    for m in range(1, 10):
        for g in range(1, 15):
            h = pairR(2, -1, m, g)
            e = z2km1(m, g)
            cmpd(9, h == e, [10, 'z2km1', m, g, h, e])
        clear()
    obs['z2km1'] = {'points': 126, 'm': '1..9', 'g': '1..14',
                    'claim': 'finite observation only (rows appear '
                             'm-uniform for all tested m; candidate next '
                             'typed target)'}
    # z2-k(-2): m=1 vs m>=2 one-point split
    def z2km2(m, g):
        if g == 1: return 2 if m == 1 else 1
        if g == 2: return 0
        if g == 3: return 1
        if g == 4: return 0
        if g == 5: return 2
        return IND(g % 2 == 0)
    for m in range(1, 10):
        for g in range(1, 15):
            h = pairR(2, -2, m, g)
            e = z2km2(m, g)
            cmpd(9, h == e, [10, 'z2km2', m, g, h, e])
        clear()
    obs['z2km2'] = {'points': 126, 'm': '1..9', 'g': '1..14',
                    'claim': 'finite observation only (g=5 value-2 spike; '
                             'm=1,g=1 split)'}

    info = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['hists'] = hists
    res['obs'] = obs
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)

main()

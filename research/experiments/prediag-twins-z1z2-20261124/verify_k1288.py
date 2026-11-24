#!/usr/bin/env python3
"""verify_k1288: machine audit for the pre-diagonal twins package (z1/z2).

Theorems under audit (declarations and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of the
hand proofs, it does NOT replace the proofs; all quantifiers in the theorems
are UNBOUNDED, censuses are consistency checks only):

  CLAIMED (universal, note T-PDT1/T-BDT1/T-PDT2/T-BDT2), for pairs
  (m, m+g) and beds (m, m), band k <= 0 (slices) / j <= 0 (beds),
  R = 2m+g+k >= 0 resp. R = 2m+j >= 0:

  T-PDT1 z1 band slices: H(R; (m,m+g); 1) = 0 (R=0); 2 (R=1);
        g1(R-2m) (R>=2), where g1(d) = 2 (d=1); [d even] (d<=0);
        [d odd] (d>=2)  -- the parity TWIN of f0.
  T-BDT1 z1 beds (j<=0): same shape with g1(j) at R>=2.
  T-PDT2 z2 band slices: H(R; (m,m+g); 2) = 2 (R=1); f0(R-2m-2) otherwise
        (R=0 gives f0(-2m-2)=0 automatically).
  T-BDT2 z2 beds (j<=0): 2 (R=1); f0(j-2) otherwise.

  C1: K1286 T-Z1 slices k in {-1,0} = g1(g+k) (subsumption/identity);
  C2: K1286 T-B1 beds j in {-1,0} subsumed (the m=1/m>=2 split of
      b1(-1) is exactly the R=1 exception layer);
  C3: K1286 T-Z2 slice k=0 = f0(g-2) (identity); T-B2 b2(0) subsumed;
  C4: K1286 open O1/O2/O4 RESOLVED: all reported m-splits and spikes
      (z1-k(-2) nucleation; z2-k(-1) rows; z2-k(-2) g=5 spike and
      m=1/g=1 split) are the R in {0,1} layer and the delta nucleation,
      no m-dependence survives at R>=2.

Batteries (counts declared in the single-owner note; expected overall_bad
== 0; stdout deterministic byte-identical, volatile info on stderr only):

  D1  z1 band slices census engine vs claim, m<=14, g<=25,
      k in [max(-30,-2m-g),0]                                [see note]
  D2  z1 beds census engine vs claim, m<=18, j in [-36..0]   [see note]
  D3  z2 band slices census engine vs claim (same box as D1) [see note]
  D4  z2 beds census engine vs claim (same box as D2)         [see note]
  D5  typed z1 slices: claims-only children mex == claim ==
      engine, m<=10, g<=14, k>=-14                            [see note]
  D6  typed z1 beds: typed == claim == engine, m<=10, j>=-16  [see note]
  D7  typed z2 slices: typed == claim == engine (D5 box)      [see note]
  D8  typed z2 beds: typed == claim == engine (D6 box)       [see note]
  D9  uniformity lemmas + published anchors:
      (a) L-BU0 v(w,1,t)==f0(t)==engine (w<=30, t<=w)
      (b) L-BU1G v(w,2,t)==g1(t)==engine (w<=30, 1<=t<=w)
      (c) L-BU2G v(w,3,t)==(2@t=1 else f0(t-2))==engine (w<=30,1<=t<=w)
      (d) T-PD0 slices recheck m<=10 g<=18 k<=0
      (e) T-B0 beds recheck m<=10 j in [-12..0]
      (f) K1286 published-table identity checks (Z1(k in {-1,0}) ==
          g1(g+k), Z2(k=0) == f0(g-2), beds) + engine overlaps
      (g) single-token closed form vs BOTH engines anchor
      (h) algebraic twin identity g1(d) == 1^f0(d) for d != 1
  D10 cross-engine canonical vs ordered on z1/z2 band + beds subsample
  D11 OBS registrations (NO universal claims): z3/z4 far-row delta
      tables g1(delta-2) / f0(delta-4) at representative m=12 rows,
      k in [-12..-1], g in [1..18]  (z3/z4 exception layers unresolved)

Engine block embedded verbatim from the published K1138/K1282..K1287
chain, sha256-gated at startup. TAMPER modes: --tamper-engine (rc 2),
--tamper=z1s|z1b|z2s|z2b (rc 1; flips the claim in the Census batteries
D1/D2/D3/D4 only). Determinism: official runs are byte-identical on
stdout (volatile timestamps/elapsed on stderr only).
"""
import json, hashlib, sys, time
from functools import lru_cache

ENGINE_BLOCK = '''def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

# ------------------------------------------------------------------
# Raw engines (verbatim from the published K1138 verifier block; the same
# transcription is embedded in the published y22 machine K1257).
# ------------------------------------------------------------------
@lru_cache(maxsize=6_000_000)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(maxsize=6_000_000)
def H_canonical(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def vC(x, z, R):  # canonical-engine single token
    return H_canonical(R, (x,), z)
def vO(x, z, R):  # ordered-engine single token
    return H_ordered(R, (x,), z)

# ------------------------------------------------------------------
# Published K0832 single-token closed form (transcription of the published
# single_token block in the y22 machine K1257; see report provenance).
# ------------------------------------------------------------------
def q_odd(k):
    return k if k % 2 else k - 1

def single_token(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))
'''

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


def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()


def IND(b):
    return 1 if b else 0

# ---- claims (the universal laws proven in the declaration note) --------
def f0(d):
    if d == 1:
        return 2
    if d <= 0:
        return IND(d % 2 == 1)
    return IND(d % 2 == 0)


def g1(d):
    if d == 1:
        return 2
    if d <= 0:
        return IND(d % 2 == 0)
    return IND(d % 2 == 1)


def z1_pair_claim(R, m, g, k):
    """T-PDT1: band slice value at (m, m+g) @ (R, 1), k = R-2m-g <= 0."""
    if R == 0:
        return 0
    if R == 1:
        return 2
    return g1(R - 2 * m)


def z1_bed_claim(R, m, j):
    """T-BDT1: bed (m,m) @ (R, 1), j = R-2m <= 0."""
    if R == 0:
        return 0
    if R == 1:
        return 2
    return g1(j)


def z2_pair_claim(R, m, g, k):
    """T-PDT2: band slice value at (m, m+g) @ (R, 2), k <= 0."""
    if R == 1:
        return 2
    return f0(R - 2 * m - 2)


def z2_bed_claim(R, m, j):
    """T-BDT2: bed (m,m) @ (R, 2), j <= 0."""
    if R == 1:
        return 2
    return f0(j - 2)


def flipC(val):
    # tamper flip for engine-vs-claim batteries (K1285/K1286 semantics)
    return 1 - val if val in (0, 1) else 1


def mexs(vals):
    s = set(vals)
    x = 0
    while x in s:
        x += 1
    return x

# ---- typed-children analysis (children valued by the CLAIM tables and
# the published K0832 closed form + published T-PD0/T-B0 only) -----------
def typed_z1_pair(R, m, g):
    """mex of claimed child values for band pair (m,m+g) @ (R,1), k<=0."""
    if R == 0:
        return 0
    k = R - 2 * m - g
    assert k <= 0
    d = R - 2 * m
    kids = []
    # lower token: fall (m>=2) / B-exit (m=1)
    if m >= 2:
        kids.append(z1_pair_claim(R - 1, m - 1, g + 1, k))
    else:
        kids.append(v(g + 1, 2, R - 1))       # K0832 closed form
    # upper token: compress (g>=2) / corner bed (g=1)
    if g >= 2:
        kids.append(z1_pair_claim(R - 1, m, g - 1, k))
    else:
        kids.append(z1_bed_claim(R - 1, m, k))
    # C move: z0 same pair, budget R-1, slice k-1 (T-PD0)
    kids.append(1 ^ f0(d - 1))
    return mexs(kids)


def typed_z1_bed(R, m, j):
    """mex of claimed child values for band bed (m,m) @ (R,1), j<=0."""
    if R == 0:
        return 0
    assert j == R - 2 * m and j <= 0
    kids = []
    # A child: pair (m-1, m) gap 1 at slice j (m>=2) / B-exit (m=1)
    if m >= 2:
        kids.append(z1_pair_claim(R - 1, m - 1, 1, j))
    else:
        kids.append(v(1, 2, R - 1))
    # C child: z0 bed (m,m) @ (R-1, 0) slice j-1 (T-B0)
    kids.append(1 ^ f0(j - 1))
    return mexs(kids)


def typed_z2_pair(R, m, g):
    """mex of claimed child values for band pair (m,m+g) @ (R,2), k<=0."""
    if R == 0:
        return 0
    k = R - 2 * m - g
    assert k <= 0
    d = R - 2 * m
    kids = []
    if m >= 2:
        kids.append(z2_pair_claim(R - 1, m - 1, g + 1, k))
    else:
        kids.append(v(g + 1, 3, R - 1))
    if g >= 2:
        kids.append(z2_pair_claim(R - 1, m, g - 1, k))
    else:
        kids.append(z2_bed_claim(R - 1, m, k))
    # C child: z1 same pair budget R-1 slice k-1 (T-PDT1)
    kids.append(1 ^ z1_pair_claim(R - 1, m, g, k - 1))
    return mexs(kids)


def typed_z2_bed(R, m, j):
    """mex of claimed child values for band bed (m,m) @ (R,2), j<=0."""
    if R == 0:
        return 0
    assert j == R - 2 * m and j <= 0
    kids = []
    if m >= 2:
        kids.append(z2_pair_claim(R - 1, m - 1, 1, j))
    else:
        kids.append(v(1, 3, R - 1))
    # C child: z1 bed (m,m) @ (R-1, 1) slice j-1 (T-BDT1)
    kids.append(1 ^ z1_bed_claim(R - 1, m, j - 1))
    return mexs(kids)


def main():
    t0 = time.time()
    res = {'kit': 'verify_k1288', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS', 'tamper': TAMPER}
    ND = 11
    counts = [0] * ND
    bad = [0] * ND
    ex = [[] for _ in range(ND)]
    hists = {}
    obs = {}

    z1s_flip = (TAMPER == 'z1s')
    z1b_flip = (TAMPER == 'z1b')
    z2s_flip = (TAMPER == 'z2s')
    z2b_flip = (TAMPER == 'z2b')

    def cmpd(i, ok, note):
        counts[i] += 1
        if not ok:
            bad[i] += 1
            if len(ex[i]) < 6: ex[i].append(note)

    def pairX(z, k, m, g):
        R = 2 * m + g + k
        return H_canonical(R, tuple(sorted([m, m + g], reverse=True)), z)

    # -------- D1: z1 band slices census --------------------------------
    for m in range(1, 15):
        for g in range(1, 26):
            for k in range(max(-30, -2 * m - g), 1):
                R = 2 * m + g + k
                h = pairX(1, k, m, g)
                exp = z1_pair_claim(R, m, g, k)
                if z1s_flip:
                    exp = flipC(exp)
                w = (R - 2 * m)
                key = 'R0' if R == 0 else ('R1' if R == 1 else
                      ('dl%d' % -1 if (R >= 2 and w <= 0) else 'hi'))
                hists.setdefault('D1_class', {})
                hists['D1_class'][key] = hists['D1_class'].get(key, 0) + 1
                cmpd(0, h == exp, [1, m, g, k, h, exp])
        clear()

    # -------- D2: z1 beds census ---------------------------------------
    for m in range(1, 19):
        for j in range(-36, 1):
            R = 2 * m + j
            if R < 0:
                continue
            h = H_canonical(R, (m, m), 1)
            exp = z1_bed_claim(R, m, j)
            if z1b_flip:
                exp = flipC(exp)
            cmpd(1, h == exp, [2, m, j, h, exp])
        clear()

    # -------- D3: z2 band slices census --------------------------------
    for m in range(1, 15):
        for g in range(1, 26):
            for k in range(max(-30, -2 * m - g), 1):
                R = 2 * m + g + k
                h = pairX(2, k, m, g)
                exp = z2_pair_claim(R, m, g, k)
                if z2s_flip:
                    exp = flipC(exp)
                cmpd(2, h == exp, [3, m, g, k, h, exp])
        clear()

    # -------- D4: z2 beds census ---------------------------------------
    for m in range(1, 19):
        for j in range(-36, 1):
            R = 2 * m + j
            if R < 0:
                continue
            h = H_canonical(R, (m, m), 2)
            exp = z2_bed_claim(R, m, j)
            if z2b_flip:
                exp = flipC(exp)
            cmpd(3, h == exp, [4, m, j, h, exp])
        clear()

    # -------- D5: typed z1 band slices ---------------------------------
    for m in range(1, 11):
        for g in range(1, 15):
            for k in range(max(-14, -2 * m - g), 1):
                R = 2 * m + g + k
                exp = z1_pair_claim(R, m, g, k)
                mx = typed_z1_pair(R, m, g)
                h = pairX(1, k, m, g)
                cmpd(4, mx == exp == h, [5, m, g, k, exp, mx, h])
        clear()

    # -------- D6: typed z1 beds ---------------------------------------
    for m in range(1, 11):
        for j in range(-16, 1):
            R = 2 * m + j
            if R < 0:
                continue
            exp = z1_bed_claim(R, m, j)
            mx = typed_z1_bed(R, m, j)
            h = H_canonical(R, (m, m), 1)
            cmpd(5, mx == exp == h, [6, m, j, exp, mx, h])
        clear()

    # -------- D7: typed z2 band slices ---------------------------------
    for m in range(1, 11):
        for g in range(1, 15):
            for k in range(max(-14, -2 * m - g), 1):
                R = 2 * m + g + k
                exp = z2_pair_claim(R, m, g, k)
                mx = typed_z2_pair(R, m, g)
                h = pairX(2, k, m, g)
                cmpd(6, mx == exp == h, [7, m, g, k, exp, mx, h])
        clear()

    # -------- D8: typed z2 beds ---------------------------------------
    for m in range(1, 11):
        for j in range(-16, 1):
            R = 2 * m + j
            if R < 0:
                continue
            exp = z2_bed_claim(R, m, j)
            mx = typed_z2_bed(R, m, j)
            h = H_canonical(R, (m, m), 2)
            cmpd(7, mx == exp == h, [8, m, j, exp, mx, h])
        clear()

    # -------- D9: uniformity lemmas + published anchors ----------------
    # (a) L-BU0 (published): v(w,1,t) == f0(t) == engine, 0 <= t <= w
    for w in range(2, 31):
        for t in range(0, w + 1):
            vc = v(w, 1, t)
            hc = vC(w, 1, t)
            cmpd(8, vc == f0(t) and hc == f0(t), [9, 'a', w, t, vc, hc, f0(t)])
        clear()
    # (b) L-BU1G: v(w,2,t) == g1(t) == engine, 1 <= t <= w
    for w in range(2, 31):
        for t in range(1, w + 1):
            vc = v(w, 2, t)
            hc = vC(w, 2, t)
            cmpd(8, vc == g1(t) and hc == g1(t), [9, 'b', w, t, vc, hc, g1(t)])
        clear()
    # (c) L-BU2G: v(w,3,t) == (2 if t==1 else f0(t-2)) == engine, 1<=t<=w
    for w in range(2, 31):
        for t in range(1, w + 1):
            want = 2 if t == 1 else f0(t - 2)
            vc = v(w, 3, t)
            hc = vC(w, 3, t)
            cmpd(8, vc == want and hc == want, [9, 'c', w, t, vc, hc, want])
        clear()
    # (d) T-PD0 slices recheck (published z0 band = f0(R-2m))
    for m in range(1, 11):
        for g in range(1, 19):
            for k in range(max(-12, -2 * m - g), 1):
                R = 2 * m + g + k
                h = pairX(0, k, m, g)
                cmpd(8, h == f0(R - 2 * m), [9, 'd', m, g, k, h, f0(R - 2 * m)])
        clear()
    # (e) T-B0 beds recheck (published: b0(j) = f0(j), j <= 0)
    for m in range(1, 11):
        for j in range(-12, 1):
            R = 2 * m + j
            if R < 0:
                continue
            h = H_canonical(R, (m, m), 0)
            cmpd(8, h == f0(j), [9, 'e', m, j, h, f0(j)])
        clear()
    # (f) K1286 published-table identity (Z1 border k in {-1,0} == claims;
    #     Z2 k=0 == f0(g-2); beds j in {-1,0} identity with engines)
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

    for g in range(1, 201):
        for k in (-1, 0):
            cmpd(8, z1k(k, g) == g1(g + k), [9, 'f', 'Z1identity', k, g])
        cmpd(8, z2k(0, g) == f0(g - 2), [9, 'f', 'Z2k0identity', g])
    for m in range(1, 12):
        for g in range(1, 15):
            for k in (-1, 0):
                R = 2 * m + g + k
                h = pairX(1, k, m, g)
                cmpd(8, h == z1k(k, g) == z1_pair_claim(R, m, g, k),
                     [9, 'f', 'Z1ov', m, g, k, h])
            clear()
            h0 = pairX(2, 0, m, g)
            cmpd(8, h0 == z2k(0, g) == z2_pair_claim(2 * m + g, m, g, 0),
                 [9, 'f', 'Z2ov', m, g, h0])
        # bed identities: K1286 b1(-1)/b1(0) and b2(0) vs claims + engine
        for j in (-1, 0):
            R = 2 * m + j
            h = H_canonical(R, (m, m), 1)
            kb = 0 if (j == -1 and m >= 2) else (2 if (j == -1 and m == 1) else 1)
            cmpd(8, h == kb == z1_bed_claim(R, m, j), [9, 'f', 'b1ov', m, j, h])
        h = H_canonical(2 * m, (m, m), 2)
        cmpd(8, h == 0 == z2_bed_claim(2 * m, m, 0), [9, 'f', 'b2ov', m, h])
        clear()
    # (g) single-token closed form vs BOTH engines (published anchor)
    for x in range(2, 17):
        for z in (1, 2, 3):
            for R in range(x + 1, x + 5):
                hc = vC(x, z, R)
                ho = vO(x, z, R)
                cmpd(8, hc == v(x, z, R), [9, 'g', 'SVC', x, z, R, hc])
                cmpd(8, ho == v(x, z, R), [9, 'g', 'SVO', x, z, R, ho])
            clear()
    # (h) algebraic twin identity: g1(d) == 1 ^ f0(d) iff d != 1
    tw = 0
    for d in range(-60, 61):
        if d == 1:
            cmpd(8, g1(d) == 2 == f0(d), [9, 'h', 'core', d])
        else:
            cmpd(8, g1(d) == (1 ^ f0(d)), [9, 'h', 'twin', d])
        tw += 1
    # K1286 OBS pattern identity: the K1286-observed m-split slices are the
    # exception layer (z1-k(-2): m=1,g=1 -> R=1; rows m>=2 -> g1(delta))
    for m in range(1, 10):
        for g in range(1, 15):
            R = 2 * m + g - 2
            h = pairX(1, -2, m, g)
            exp = z1_pair_claim(R, m, g, -2)
            cmpd(8, h == exp, [9, 'h', 'z1km2ov', m, g, h, exp])
        clear()
    for m in range(1, 10):
        for g in range(1, 15):
            R = 2 * m + g - 1
            h = pairX(2, -1, m, g)
            cmpd(8, h == z2_pair_claim(R, m, g, -1),
                 [9, 'h', 'z2km1ov', m, g, h])
            R2 = 2 * m + g - 2
            h2 = pairX(2, -2, m, g)
            cmpd(8, h2 == z2_pair_claim(R2, m, g, -2),
                 [9, 'h', 'z2km2ov', m, g, h2])
        clear()

    # -------- D10: cross-engine canonical vs ordered --------------------
    for z in (1, 2):
        for m in range(1, 8):
            for g in range(1, 11):
                for k in range(max(-8, -2 * m - g), 1):
                    R = 2 * m + g + k
                    X = tuple(sorted([m, m + g], reverse=True))
                    hc = H_canonical(R, X, z)
                    ho = H_ordered(R, X, z)
                    cmpd(9, hc == ho, [10, 'PD', z, m, g, k, hc, ho])
                clear()
    for m in range(1, 8):
        for z in (1, 2):
            for j in range(-8, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                hc = H_canonical(R, (m, m), z)
                ho = H_ordered(R, (m, m), z)
                cmpd(9, hc == ho, [10, 'BED', m, z, j, hc, ho])
        clear()

    # -------- D11: OBS registrations (NO universal claims) --------------
    # z3/z4 far-row delta tables (finite observation; exception layers of
    # z3/z4 unresolved; the far rows at representative m=12 read off as
    # g1(delta-2) (z3) / f0(delta-4) (z4) over the census box)
    for (z, fn, tag) in [(3, lambda d: g1(d - 2), 'z3far'),
                         (4, lambda d: f0(d - 4), 'z4far')]:
        mm = 0
        for k in range(-12, 0):
            for g in range(1, 19):
                R = 24 + g + k
                if R < 0:
                    continue
                h = pairX(z, k, 12, g)
                exp = fn(R - 24)
                cmpd(10, h == exp, [11, tag, k, g, h, exp])
                mm += 1
            clear()
        obs[tag] = {'points': mm, 'm': '12', 'k': '-12..-1', 'g': '1..18',
                    'claim': 'finite far-row observation only; NOT universal.'
                             ' Exception layer of plane %d unresolved; typed '
                             'proof is a later target' % z}
    # z3 exception-layer probe: cells at R<=3 recorded (not claimed)
    z3_lowR = {}
    for m in range(1, 7):
        for g in range(1, 13):
            for k in range(-2 * m - g, 1):
                R = 2 * m + g + k
                if R > 3:
                    continue
                h = H_canonical(R, (m, m + g), 3)
                z3_lowR[str(h)] = z3_lowR.get(str(h), 0) + 1
                cmpd(10, h in (0, 1, 2), [11, 'z3low', m, g, k, h])
        clear()
    obs['z3_lowR_hist'] = {'hist': z3_lowR, 'R': '0..3',
                           'claim': 'finite observation of the z3 exception '
                                    'layer only (expectation h in {0,1,2})'}

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

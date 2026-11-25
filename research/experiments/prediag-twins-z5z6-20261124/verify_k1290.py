#!/usr/bin/env python3
"""verify_k1290: machine audit for the pre-diagonal twins z5/z6 package.

Theorems under audit (claims and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of
the hand proofs, it does NOT replace the proofs; all quantifiers are
UNBOUNDED, censuses are consistency checks only):

  CLAIMED (universal, note T-PDT5/T-BDT5/T-PDT6/T-BDT6), for pairs
  (m, m+g) and beds (m, m), band k <= 0 (slices) / j <= 0 (beds),
  R = 2m+g+k >= 0 resp. R = 2m+j >= 0:

  T-PDT5 z5 band slices: H(R; (m,m+g); 5) = 2*[R odd] (R<6, the
        pre-diag exception layer of thickness L(5)=2*ceil(5/2)=6);
        g1(R-2m-4) (R>=6).
  T-BDT5 z5 beds (j<=0): 2*[R odd] (R<6); g1(j-4) (R>=6).
  T-PDT6 z6 band slices: H(R; (m,m+g); 6) = 2*[R odd] (R<6, of which
        the even R cells coincide with the main law f0(delta-6) on
        this box); f0(R-2m-6) (R>=6).
  T-BDT6 z6 beds (j<=0): 2*[R odd] (R<6); f0(j-6) (R>=6).

  L-BU5G (uniformity lemma): v(w,6,t) = 2*[t odd] (t<6);
        g1(t-4) (6<=t<=w), all w>=2 (K0832 closed form + engines).
  L-BU6G: v(w,7,t) = 2*[t odd] (t<6); f0(t-6) (6<=t<=w), all w>=2.
  COROLLARY: the sharpened plane-shift family C-PSF' (layer
        2*[R odd] for R < 2*ceil(w/2), main T_w(delta-2*floor(w/2)))
        reproduces the proved plane laws w=0 (K1286), w=1,2 (K1288),
        w=3,4 (K1289), w=5,6 (this package) exactly; z7/z8 are
        registered as FINITE OBSERVATION ONLY (D11, NO universal
        claims).

Batteries (counts declared in the single-owner note; expected
overall_bad == 0; stdout deterministic byte-identical, volatile info on
stderr only):

  D1  z5 band slices census engine vs claim, m<=14, g<=25,
      k in [max(-30,-2m-g),0]                                [8928]
  D2  z5 beds census engine vs claim, m<=18, j in [-36..0]   [360]
  D3  z6 band slices census engine vs claim (D1 box)         [8928]
  D4  z6 beds census engine vs claim (D2 box)                [360]
  D5  typed z5 slices: claims-only children mex == claim ==
      engine, m<=10, g<=14, k>=-14                           [1939]
  D6  typed z5 beds: typed == claim == engine, m<=10,
      j>=-16                                                 [114]
  D7  typed z6 slices (D5 box)                              [1939]
  D8  typed z6 beds (D6 box)                                 [114]
  D9  uniformity lemmas + published anchors:
      (a) L-BU5G v(w,6,t) == plane-5 law == closed form == engine
          (w<=30, 0<=t<=w)                                   [493]
      (b) L-BU6G v(w,7,t) == plane-6 law (w<=30)            [493]
      (c) K1289 anchors T-PDT3/T-BDT3/T-PDT4/T-BDT4 recheck
          (pairs m<=10 g<=18 k>=-12; beds m<=10 j>=-12)      [4690]
      (d) K1288 anchors T-PDT1/T-BDT1/T-PDT2/T-BDT2 recheck  [4690]
      (e) K1286 anchors T-PD0/T-B0 recheck (same boxes)       [2345]
      (f) sharpened C-PSF identity sweep w=0..6 (cpsf == engine
          == plane claim, pair box + bed box)
      (g) T-TWIN algebra identity sweep d in [-100..100]      [201]
      (h) single-token closed form vs BOTH engines anchor
          (x<=16, z in 2..7, R in x+1..x+4)                   [720]
      (i) B-exit w=1 edge values (v(1,6,t)/v(1,7,t), t<=1)     [4]
  D10 cross-engine canonical vs ordered on z5/z6 band + beds
      subsample                                             [1516]
  D11 OBS registrations (NO universal claims): z7/z8 band
      census m<=10 g<=20 k>=-50 vs sharpened C-PSF prediction,
      beds m<=10 j>=-24, far rows m=12, low-R layer hists
      (R<8), L-BU7G/L-BU8G plane-token discovery sweeps
      (z=8/9, w<=30) and a multi-plane dedup (R,delta) sweep
      z=0..10 for the future w-induction (O9).

Engine block embedded verbatim from the published K1138/K1282..K1289
chain, sha256-gated at startup. TAMPER modes: --tamper-engine (rc 2),
--tamper=z5s|z5b|z6s|z6b (rc 1; flips the claim in the census batteries
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


# published claims reused as anchors (K1286/K1288/K1289)
def z0_pair_claim(R, m, g, k):
    return f0(R - 2 * m)


def z0_bed_claim(R, m, j):
    return f0(j)


def z1_pair_claim(R, m, g, k):
    if R == 0:
        return 0
    if R == 1:
        return 2
    return g1(R - 2 * m)


def z1_bed_claim(R, m, j):
    if R == 0:
        return 0
    if R == 1:
        return 2
    return g1(j)


def z2_pair_claim(R, m, g, k):
    if R == 1:
        return 2
    return f0(R - 2 * m - 2)


def z2_bed_claim(R, m, j):
    if R == 1:
        return 2
    return f0(j - 2)


def z3_pair_claim(R, m, g, k):
    if R <= 3:
        return 2 * (R % 2)
    return g1(R - 2 * m - 2)


def z3_bed_claim(R, m, j):
    if R <= 3:
        return 2 * (R % 2)
    return g1(j - 2)


def z4_pair_claim(R, m, g, k):
    if R < 4:
        return 2 * (R % 2)
    return f0(R - 2 * m - 4)


def z4_bed_claim(R, m, j):
    if R < 4:
        return 2 * (R % 2)
    return f0(j - 4)


# the NEW claims of this package (T-PDT5/T-BDT5/T-PDT6/T-BDT6)
def z5_pair_claim(R, m, g, k):
    if R < 6:
        return 2 * (R % 2)
    return g1(R - 2 * m - 4)


def z5_bed_claim(R, m, j):
    if R < 6:
        return 2 * (R % 2)
    return g1(j - 4)


def z6_pair_claim(R, m, g, k):
    if R < 6:
        return 2 * (R % 2)
    return f0(R - 2 * m - 6)


def z6_bed_claim(R, m, j):
    if R < 6:
        return 2 * (R % 2)
    return f0(j - 6)


def cpsf(w, R, d):
    """Sharpened C-PSF' (proved for w=0..6; OBS for z7/z8 batteries)."""
    L = 2 * ((w + 1) // 2)
    shift = 2 * (w // 2)
    if R < L:
        return 2 * (R % 2)
    return g1(d - shift) if w % 2 else f0(d - shift)


def plane_claim(w):
    if w == 0:
        return (z0_pair_claim, z0_bed_claim)
    if w == 1:
        return (z1_pair_claim, z1_bed_claim)
    if w == 2:
        return (z2_pair_claim, z2_bed_claim)
    if w == 3:
        return (z3_pair_claim, z3_bed_claim)
    if w == 4:
        return (z4_pair_claim, z4_bed_claim)
    if w == 5:
        return (z5_pair_claim, z5_bed_claim)
    if w == 6:
        return (z6_pair_claim, z6_bed_claim)
    raise ValueError(w)


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
# the K0832 closed form + published z1..z4 claims only) ----------------
def typed_z5_pair(R, m, g):
    """mex of claimed child values for band pair (m,m+g) @ (R,5), k<=0."""
    if R == 0:
        return 0
    k = R - 2 * m - g
    assert k <= 0
    kids = []
    # lower token: fall (m>=2) / B-exit (m=1 -> single token w=g+1,
    # plane 6, L-BU5G / closed form)
    if m >= 2:
        kids.append(z5_pair_claim(R - 1, m - 1, g + 1, k))
    else:
        kids.append(v(g + 1, 6, R - 1))
    # upper token: compress (g>=2) / corner bed (g=1)
    if g >= 2:
        kids.append(z5_pair_claim(R - 1, m, g - 1, k))
    else:
        kids.append(z5_bed_claim(R - 1, m, k))
    # C move: z4 same pair, budget R-1 (T-PDT4, published K1289)
    kids.append(1 ^ z4_pair_claim(R - 1, m, g, k - 1))
    return mexs(kids)


def typed_z5_bed(R, m, j):
    """mex of claimed child values for bed (m,m) @ (R,5), j<=0."""
    if R == 0:
        return 0
    assert j == R - 2 * m and j <= 0
    kids = []
    if m >= 2:
        kids.append(z5_pair_claim(R - 1, m - 1, 1, j))
    else:
        kids.append(v(1, 6, R - 1))
    kids.append(1 ^ z4_bed_claim(R - 1, m, j - 1))
    return mexs(kids)


def typed_z6_pair(R, m, g):
    """mex of claimed child values for band pair (m,m+g) @ (R,6), k<=0."""
    if R == 0:
        return 0
    k = R - 2 * m - g
    assert k <= 0
    kids = []
    if m >= 2:
        kids.append(z6_pair_claim(R - 1, m - 1, g + 1, k))
    else:
        kids.append(v(g + 1, 7, R - 1))       # L-BU6G / closed form
    if g >= 2:
        kids.append(z6_pair_claim(R - 1, m, g - 1, k))
    else:
        kids.append(z6_bed_claim(R - 1, m, k))
    # C move: z5 same pair, budget R-1 (T-PDT5, same packet, lower budget)
    kids.append(1 ^ z5_pair_claim(R - 1, m, g, k - 1))
    return mexs(kids)


def typed_z6_bed(R, m, j):
    """mex of claimed child values for bed (m,m) @ (R,6), j<=0."""
    if R == 0:
        return 0
    assert j == R - 2 * m and j <= 0
    kids = []
    if m >= 2:
        kids.append(z6_pair_claim(R - 1, m - 1, 1, j))
    else:
        kids.append(v(1, 7, R - 1))
    kids.append(1 ^ z5_bed_claim(R - 1, m, j - 1))
    return mexs(kids)


def main():
    t0 = time.time()
    res = {'kit': 'verify_k1290', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS', 'tamper': TAMPER}
    ND = 11
    counts = [0] * ND
    bad = [0] * ND
    ex = [[] for _ in range(ND)]
    hists = {}
    obs = {}

    z5s_flip = (TAMPER == 'z5s')
    z5b_flip = (TAMPER == 'z5b')
    z6s_flip = (TAMPER == 'z6s')
    z6b_flip = (TAMPER == 'z6b')

    def cmpd(i, ok, note):
        counts[i] += 1
        if not ok:
            bad[i] += 1
            if len(ex[i]) < 6: ex[i].append(note)

    def pairX(z, k, m, g):
        R = 2 * m + g + k
        return H_canonical(R, tuple(sorted([m, m + g], reverse=True)), z)

    # -------- D1: z5 band slices census --------------------------------
    for m in range(1, 15):
        for g in range(1, 26):
            for k in range(max(-30, -2 * m - g), 1):
                R = 2 * m + g + k
                h = pairX(5, k, m, g)
                exp = z5_pair_claim(R, m, g, k)
                if z5s_flip:
                    exp = flipC(exp)
                d = (R - 2 * m) - 4
                key = ('R%d' % R) if R < 6 else ('core' if d == 1 else
                                                 ('dl' if d <= 0 else 'hi'))
                hists.setdefault('D1_class', {})
                hists['D1_class'][key] = hists['D1_class'].get(key, 0) + 1
                cmpd(0, h == exp, [1, m, g, k, h, exp])
        clear()

    # -------- D2: z5 beds census ---------------------------------------
    for m in range(1, 19):
        for j in range(-36, 1):
            R = 2 * m + j
            if R < 0:
                continue
            h = H_canonical(R, (m, m), 5)
            exp = z5_bed_claim(R, m, j)
            if z5b_flip:
                exp = flipC(exp)
            cmpd(1, h == exp, [2, m, j, h, exp])
        clear()

    # -------- D3: z6 band slices census --------------------------------
    for m in range(1, 15):
        for g in range(1, 26):
            for k in range(max(-30, -2 * m - g), 1):
                R = 2 * m + g + k
                h = pairX(6, k, m, g)
                exp = z6_pair_claim(R, m, g, k)
                if z6s_flip:
                    exp = flipC(exp)
                cmpd(2, h == exp, [3, m, g, k, h, exp])
        clear()

    # -------- D4: z6 beds census ---------------------------------------
    for m in range(1, 19):
        for j in range(-36, 1):
            R = 2 * m + j
            if R < 0:
                continue
            h = H_canonical(R, (m, m), 6)
            exp = z6_bed_claim(R, m, j)
            if z6b_flip:
                exp = flipC(exp)
            cmpd(3, h == exp, [4, m, j, h, exp])
        clear()

    # -------- D5: typed z5 band slices ---------------------------------
    for m in range(1, 11):
        for g in range(1, 15):
            for k in range(max(-14, -2 * m - g), 1):
                R = 2 * m + g + k
                exp = z5_pair_claim(R, m, g, k)
                mx = typed_z5_pair(R, m, g)
                h = pairX(5, k, m, g)
                cmpd(4, mx == exp == h, [5, m, g, k, exp, mx, h])
        clear()

    # -------- D6: typed z5 beds ----------------------------------------
    for m in range(1, 11):
        for j in range(-16, 1):
            R = 2 * m + j
            if R < 0:
                continue
            exp = z5_bed_claim(R, m, j)
            mx = typed_z5_bed(R, m, j)
            h = H_canonical(R, (m, m), 5)
            cmpd(5, mx == exp == h, [6, m, j, exp, mx, h])
        clear()

    # -------- D7: typed z6 band slices ----------------------------------
    for m in range(1, 11):
        for g in range(1, 15):
            for k in range(max(-14, -2 * m - g), 1):
                R = 2 * m + g + k
                exp = z6_pair_claim(R, m, g, k)
                mx = typed_z6_pair(R, m, g)
                h = pairX(6, k, m, g)
                cmpd(6, mx == exp == h, [7, m, g, k, exp, mx, h])
        clear()

    # -------- D8: typed z6 beds ----------------------------------------
    for m in range(1, 11):
        for j in range(-16, 1):
            R = 2 * m + j
            if R < 0:
                continue
            exp = z6_bed_claim(R, m, j)
            mx = typed_z6_bed(R, m, j)
            h = H_canonical(R, (m, m), 6)
            cmpd(7, mx == exp == h, [8, m, j, exp, mx, h])
        clear()

    # -------- D9: uniformity lemmas + published anchors ----------------
    # (a) L-BU5G: v(w,6,t) == plane-5 law == closed form == engine
    for w in range(2, 31):
        for t in range(0, w + 1):
            want = 2 * (t % 2) if t < 6 else g1(t - 4)
            vc = v(w, 6, t)
            hc = vC(w, 6, t)
            cmpd(8, vc == want and hc == want, [9, 'a', w, t, vc, hc, want])
        clear()
    # (b) L-BU6G: v(w,7,t) == plane-6 law
    for w in range(2, 31):
        for t in range(0, w + 1):
            want = 2 * (t % 2) if t < 6 else f0(t - 6)
            vc = v(w, 7, t)
            hc = vC(w, 7, t)
            cmpd(8, vc == want and hc == want, [9, 'b', w, t, vc, hc, want])
        clear()
    # (c) K1289 anchors recheck (T-PDT3/T-BDT3/T-PDT4/T-BDT4)
    for (z, pc, bc) in [(3, z3_pair_claim, z3_bed_claim),
                       (4, z4_pair_claim, z4_bed_claim)]:
        for m in range(1, 11):
            for g in range(1, 19):
                for k in range(max(-12, -2 * m - g), 1):
                    R = 2 * m + g + k
                    h = pairX(z, k, m, g)
                    exp = pc(R, m, g, k)
                    cmpd(8, h == exp, [9, 'c', z, m, g, k, h, exp])
            for j in range(-12, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = H_canonical(R, (m, m), z)
                exp = bc(R, m, j)
                cmpd(8, h == exp, [9, 'c', z, m, j, h, exp])
            clear()
    # (d) K1288 anchors recheck (T-PDT1/T-BDT1/T-PDT2/T-BDT2)
    for (z, pc, bc) in [(1, z1_pair_claim, z1_bed_claim),
                       (2, z2_pair_claim, z2_bed_claim)]:
        for m in range(1, 11):
            for g in range(1, 19):
                for k in range(max(-12, -2 * m - g), 1):
                    R = 2 * m + g + k
                    h = pairX(z, k, m, g)
                    exp = pc(R, m, g, k)
                    cmpd(8, h == exp, [9, 'd', z, m, g, k, h, exp])
            for j in range(-12, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = H_canonical(R, (m, m), z)
                exp = bc(R, m, j)
                cmpd(8, h == exp, [9, 'd', z, m, j, h, exp])
            clear()
    # (e) K1286 anchors recheck (T-PD0/T-B0)
    for m in range(1, 11):
        for g in range(1, 19):
            for k in range(max(-12, -2 * m - g), 1):
                R = 2 * m + g + k
                h = pairX(0, k, m, g)
                cmpd(8, h == f0(R - 2 * m), [9, 'e', m, g, k, h, f0(R - 2 * m)])
        for j in range(-12, 1):
            R = 2 * m + j
            if R < 0:
                continue
            h = H_canonical(R, (m, m), 0)
            cmpd(8, h == f0(j), [9, 'e', m, j, h, f0(j)])
        clear()
    # (f) sharpened C-PSF identity sweep on the PROVED planes w=0..6
    for w in range(0, 7):
        pc, bc = plane_claim(w)
        for m in range(1, 11):
            for g in range(1, 19):
                for k in range(max(-12, -2 * m - g), 1):
                    R = 2 * m + g + k
                    d = R - 2 * m
                    h = pairX(w, k, m, g)
                    c = cpsf(w, R, d)
                    e = pc(R, m, g, k)
                    cmpd(8, h == c == e, [9, 'f', w, m, g, k, h, c, e])
            for j in range(-12, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = H_canonical(R, (m, m), w)
                c = cpsf(w, R, j)
                e = bc(R, m, j)
                cmpd(8, h == c == e, [9, 'f-b', w, m, j, h, c, e])
            clear()
    # (g) T-TWIN algebra identity
    for d in range(-100, 101):
        if d == 1:
            cmpd(8, g1(d) == 2 == f0(d), [9, 'g', 'core', d])
        else:
            cmpd(8, g1(d) == (1 ^ f0(d)), [9, 'g', 'twin', d])
    # (h) single-token closed form vs BOTH engines (published anchor)
    for x in range(2, 17):
        for z in (2, 3, 4, 5, 6, 7):
            for R in range(x + 1, x + 5):
                hc = vC(x, z, R)
                ho = vO(x, z, R)
                cmpd(8, hc == v(x, z, R), [9, 'h', 'SVC', x, z, R, hc])
                cmpd(8, ho == v(x, z, R), [9, 'h', 'SVO', x, z, R, ho])
            clear()
    # (i) B-exit w=1 edge values (bed typed proofs read only t<=1)
    for z in (6, 7):
        for t in (0, 1):
            cmpd(8, v(1, z, t) == vC(1, z, t) == 2 * (t % 2),
                 [9, 'i', z, t, v(1, z, t)])
        clear()

    # -------- D10: cross-engine canonical vs ordered --------------------
    for z in (5, 6):
        for m in range(1, 9):
            for g in range(1, 11):
                for k in range(max(-8, -2 * m - g), 1):
                    R = 2 * m + g + k
                    X = tuple(sorted([m, m + g], reverse=True))
                    hc = H_canonical(R, X, z)
                    ho = H_ordered(R, X, z)
                    cmpd(9, hc == ho, [10, 'PD', z, m, g, k, hc, ho])
                clear()
            for j in range(-8, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                hc = H_canonical(R, (m, m), z)
                ho = H_ordered(R, (m, m), z)
                cmpd(9, hc == ho, [10, 'BED', m, z, j, hc, ho])
            clear()

    # -------- D11: OBS registrations (NO universal claims) --------------
    # z7/z8 band/bed census vs the sharpened C-PSF' PREDICTION (finite
    # observation only; the w-induction of C-PSF' is NOT proved here)
    for (z, tag) in [(7, 'z7band'), (8, 'z8band')]:
        mm = 0
        for m in range(1, 11):
            for g in range(1, 21):
                for k in range(max(-50, -2 * m - g), 1):
                    R = 2 * m + g + k
                    d = R - 2 * m
                    h = pairX(z, k, m, g)
                    exp = cpsf(z, R, d)
                    cmpd(10, h == exp, [11, tag, m, g, k, h, exp])
                    mm += 1
            clear()
        obs[tag] = {'points': mm,
                    'box': 'm<=10, g<=20, k in [max(-50,-2m-g),0]',
                    'claim': 'finite observation only; NOT universal.'}
    for (z, tag) in [(7, 'z7bed'), (8, 'z8bed')]:
        mm = 0
        for m in range(1, 11):
            for j in range(-24, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = H_canonical(R, (m, m), z)
                exp = cpsf(z, R, j)
                cmpd(10, h == exp, [11, tag, m, j, h, exp])
                mm += 1
            clear()
        obs[tag] = {'points': mm, 'box': 'm<=10, j in [-24..0]',
                    'claim': 'finite observation only; NOT universal.'}
    for (z, fn, tag) in [(7, lambda d: g1(d - 6), 'z7far'),
                         (8, lambda d: f0(d - 8), 'z8far')]:
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
                    'claim': 'finite far-row observation only; NOT universal.'}
    # z7/z8 exception-layer low-R hists (R < 2*ceil(w/2) = 8 cells)
    for z in (7, 8):
        hist = {}
        for m in range(1, 7):
            for g in range(1, 13):
                for k in range(-2 * m - g, 1):
                    R = 2 * m + g + k
                    if R >= 8:
                        continue
                    h = H_canonical(R, (m, m + g), z)
                    key = str(h)
                    hist[key] = hist.get(key, 0) + 1
                    cmpd(10, h == cpsf(z, R, R - 2 * m),
                         [11, 'lowR', z, m, g, k, h, cpsf(z, R, R - 2 * m)])
            clear()
        obs['z%d_lowR_hist' % z] = {'hist': hist, 'R': '0..7',
                                    'claim': 'finite observation only'}
    # L-BU7G/L-BU8G plane-token discovery sweeps (OBS for K1291+): the
    # plane-7/8 single-token laws predicted by closed-form structure
    for (z, law, tag) in [
            (8, lambda t: 2 * (t % 2) if t < 8 else g1(t - 6), 'lbu7g'),
            (9, lambda t: 2 * (t % 2) if t < 8 else f0(t - 8), 'lbu8g')]:
        mm = 0
        for w in range(2, 31):
            for t in range(0, w + 1):
                hc = vC(w, z, t)
                cf = v(w, z, t)
                want = law(t)
                cmpd(10, hc == cf == want, [11, tag, w, t, hc, cf, want])
                mm += 1
            clear()
        obs[tag] = {'points': mm,
                    'law': 'plane-%d law on token plane %d'
                           % (z - 1, z),
                    'claim': 'finite observation only; NOT universal.'}
    # multi-plane dedup (R,delta) sweep z=0..10 (O9 w-induction support)
    for z in range(0, 11):
        tab = {}
        for m in range(1, 11):
            for g in range(1, 21):
                for k in range(max(-50, -2 * m - g), 1):
                    R = 2 * m + g + k
                    if R < 0:
                        continue
                    d = R - 2 * m
                    h = pairX(z, k, m, g)
                    tab.setdefault((R, d), set()).add(h)
            clear()
        mixed = sum(1 for s in tab.values() if len(s) > 1)
        bb = 0
        for (R, dd), vals in tab.items():
            c = cpsf(z, R, dd)
            for x in vals:
                if x != c:
                    bb += 1
        obs['z%02d_dedup' % z] = {'cells': len(tab), 'mixed': mixed,
                                  'cpsf_bad': bb,
                                  'claim': 'finite observation only.'}
        for (R, dd), vals in sorted(tab.items()):
            c = cpsf(z, R, dd)
            for x in vals:
                cmpd(10, x == c, [11, 'dedup', z, R, dd, x, c])

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

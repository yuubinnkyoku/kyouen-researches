#!/usr/bin/env python3
"""verify_k1303: machine audit for the GENERAL-w pre-diagonal induction
package (sharpened C-PSF' universal for ALL planes w >= 0).

Theorems under audit (claims and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of
the hand proof pointwise, it does NOT replace the proofs; all quantifiers
are UNBOUNDED, censuses are consistency checks only):

  CPSF-GEN(w) (universal, all w >= 0), pair positions (m, m+g), band
        k = R-2m-g <= 0, delta := R-2m:
        H(R; (m,m+g); w) = 2*[R odd]        if R <  L(w) = 2*ceil(w/2)
                           T_w(delta-s(w))  if R >= L(w),  s(w) = 2*floor(w/2)
  BED-GEN(w) (universal): beds (m,m), j = R-2m <= 0:
        H(R; (m,m); w)    = 2*[R odd]      if R <  L(w)
                           T_w(j - s(w))   if R >= L(w)
  L-BU-GEN(w) (universal): v(x, w+1, t) = 2*[t odd] (t < L(w));
        T_w(t - s(w)) (t >= L(w)), all x >= 1, 0 <= t <= x.
  T_w := g1 (w odd) / f0 (w even); f0 (K1286), g1 (K1288, T-TWIN).

  SUBSUMPTION: every per-plane law T-PD0..T-PDT14 / T-B0..T-BDT14
  (K1286/K1288/K1289/K1290/K1294/K1299/K1301/K1302) is the w-instance of
  CPSF-GEN/BED-GEN; the never-observed planes w=17..20 are instances too
  (universal claim, census-checked here; K1301/K1302 dedup reached z=16).

Batteries (counts declared in the single-owner note; expected
overall_bad == 0; stdout deterministic byte-identical, volatile info on
stderr only). ALL batteries run on ALL planes w=0..16 (or wider) with
the SAME general claim function - there are no per-plane special cases
in the machine:

  D1  general band census engine vs CPSF-GEN planes w=0..16,
      m<=12, g<=25, k in [max(-60,-2m-g),0]
  D2  general bed census engine vs BED-GEN planes w=0..16,
      m<=14, j in [-30..0]
  D3  typed general self-check (children built ONLY from
      CPSF-GEN/BED-GEN(w and w-1) tables + K0832 closed form):
      typed mex == claim == engine, planes w=0..16, m<=10, g<=14,
      k>=-14; beds m<=10, j>=-16
  D4  crossing/seam row census R in [max(0,L-2), L+4] planes w=0..16,
      m<=18, g<=26, k in [-26..0] (k<=0 enforcement); bed rows
      m<=18, j in [-30..0] restricted to the same R window (R>=0)
  D5  L-BU-GEN: closed form == CPSF-GEN(w,t,t) == canonical engine,
      w<=30, x<=34 (covers the 3 closed-form regions of K0832)
  D6  single-token closed form vs BOTH engines anchor (x<=16,
      z in 2..13, R in x+1..x+4)   [published K0832 anchor box]
  D7  subsumption identity sweep: published per-plane claims
      (K1286..K1302 transcriptions z0..z14) == CPSF-GEN == engine,
      pairs m<=10, g<=18, k>=-12; beds m<=10, j>=-12 (w=0..14)
  D8  NEW-plane census w=17..20 (never observed pre-K1303)
  D9  T-TWIN algebra identity sweep d in [-260..260]
  D10 cross-engine canonical vs ordered subsample planes
      {0,5,11,13,16,19}
  D11 stress: far-m rows m in 13..32 (planes {3,9,13,16}), dedup
      (R,delta) sweep z=0..20 (mixed-cell + cpsf agreement), spot
      planes w=21..24.

Engine block embedded verbatim from the published K1138/K1282..K1302
chain, sha256-gated at startup (identical bytes as K1282..K1302 kits).
TAMPER modes: --tamper-engine (rc 2), --tamper=hl (flip band census
claims D1), --tamper=hbd (flip bed census claims D2), --tamper=ws
(swap T_w parity globally), --tamper=Ls (layer L(w)+2 shift globally)
- all rc 1 with exact pre-declared bad counts. Determinism: official
runs byte-identical on stdout (volatile timestamps/elapsed stderr only).
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

# ---- the two published 1-D laws (K1286 f0; K1288 g1) -------------------
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


# ---- the NEW general-w claims of this package ---------------------------
WSWAP = (TAMPER == 'ws')
LSHIFT = (TAMPER == 'Ls')


def Lw(w):
    return 2 * ((w + 1) // 2) + (2 if LSHIFT else 0)


def sw(w):
    return 2 * (w // 2)


def Tw(w, d):
    if WSWAP:
        return f0(d) if w % 2 else g1(d)
    return g1(d) if w % 2 else f0(d)


def cpsfG(w, R, d):
    """CPSF-GEN(w): pair claim (delta d) AND bed claim (j d) - same law."""
    if R < Lw(w):
        return 2 * (R % 2)
    return Tw(w, d - sw(w))


# published per-plane claims (K1286..K1302 transcriptions) for the
# subsumption identity sweep D7
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


def z7_pair_claim(R, m, g, k):
    if R < 8:
        return 2 * (R % 2)
    return g1(R - 2 * m - 6)


def z7_bed_claim(R, m, j):
    if R < 8:
        return 2 * (R % 2)
    return g1(j - 6)


def z8_pair_claim(R, m, g, k):
    if R < 8:
        return 2 * (R % 2)
    return f0(R - 2 * m - 8)


def z8_bed_claim(R, m, j):
    if R < 8:
        return 2 * (R % 2)
    return f0(j - 8)


def z9_pair_claim(R, m, g, k):
    if R < 10:
        return 2 * (R % 2)
    return g1(R - 2 * m - 8)


def z9_bed_claim(R, m, j):
    if R < 10:
        return 2 * (R % 2)
    return g1(j - 8)


def z10_pair_claim(R, m, g, k):
    if R < 10:
        return 2 * (R % 2)
    return f0(R - 2 * m - 10)


def z10_bed_claim(R, m, j):
    if R < 10:
        return 2 * (R % 2)
    return f0(j - 10)


def z11_pair_claim(R, m, g, k):
    if R < 12:
        return 2 * (R % 2)
    return g1(R - 2 * m - 10)


def z11_bed_claim(R, m, j):
    if R < 12:
        return 2 * (R % 2)
    return g1(j - 10)


def z12_pair_claim(R, m, g, k):
    if R < 12:
        return 2 * (R % 2)
    return f0(R - 2 * m - 12)


def z12_bed_claim(R, m, j):
    if R < 12:
        return 2 * (R % 2)
    return f0(j - 12)


# T-PDT13/T-BDT13/T-PDT14/T-BDT14 (published by the sibling lane as K1302)
def z13_pair_claim(R, m, g, k):
    if R < 14:
        return 2 * (R % 2)
    return g1(R - 2 * m - 12)


def z13_bed_claim(R, m, j):
    if R < 14:
        return 2 * (R % 2)
    return g1(j - 12)


def z14_pair_claim(R, m, g, k):
    if R < 14:
        return 2 * (R % 2)
    return f0(R - 2 * m - 14)


def z14_bed_claim(R, m, j):
    if R < 14:
        return 2 * (R % 2)
    return f0(j - 14)


PLANE_CLAIMS = [(z0_pair_claim, z0_bed_claim), (z1_pair_claim, z1_bed_claim),
                (z2_pair_claim, z2_bed_claim), (z3_pair_claim, z3_bed_claim),
                (z4_pair_claim, z4_bed_claim), (z5_pair_claim, z5_bed_claim),
                (z6_pair_claim, z6_bed_claim), (z7_pair_claim, z7_bed_claim),
                (z8_pair_claim, z8_bed_claim), (z9_pair_claim, z9_bed_claim),
                (z10_pair_claim, z10_bed_claim), (z11_pair_claim, z11_bed_claim),
                (z12_pair_claim, z12_bed_claim), (z13_pair_claim, z13_bed_claim),
                (z14_pair_claim, z14_bed_claim)]


def flipC(val):
    # tamper flip for engine-vs-claim batteries (K1285..K1302 semantics)
    return 1 - val if val in (0, 1) else 1


def mexs(vals):
    s = set(vals)
    x = 0
    while x in s:
        x += 1
    return x

# ---- typed-children analysis (children valued by the GENERAL claim
# tables CPSF-GEN/BED-GEN at planes w and w-1 + K0832 closed form only) --
def typed_pair(R, m, g, w):
    """mex of children for band pair (m,m+g) @ (R,w), k<=0, from claims only."""
    if R == 0:
        return 0
    kids = []
    # lower token: fall (m>=2) / B-exit (m=1 -> token g+1 @ plane w+1, t<=g+1)
    if m >= 2:
        kids.append(cpsfG(w, R - 1, (R - 1) - 2 * (m - 1)))
    else:
        t = R - 1
        assert t <= g + 1, (w, m, g, R)
        kids.append(v(g + 1, w + 1, t))
    # upper token: compress (g>=2, pair) / corner (g=1, bed) - same table
    kids.append(cpsfG(w, R - 1, (R - 1) - 2 * m))
    # C move: plane w-1 same pair, budget R-1
    if w >= 1:
        kids.append(1 ^ cpsfG(w - 1, R - 1, (R - 1) - 2 * m))
    return mexs(kids)


def typed_bed(R, m, j, w):
    """mex of children for bed (m,m) @ (R,w), j<=0, from claims only."""
    if R == 0:
        return 0
    assert j == R - 2 * m and j <= 0
    kids = []
    if m >= 2:
        kids.append(cpsfG(w, R - 1, (R - 1) - 2 * (m - 1)))
    else:
        t = R - 1  # = j+1 <= 1
        assert t <= 1
        kids.append(v(1, w + 1, t))
    if w >= 1:
        kids.append(1 ^ cpsfG(w - 1, R - 1, j - 1))
    return mexs(kids)


def main():
    t0 = time.time()
    res = {'kit': 'verify_k1303', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS', 'tamper': TAMPER}
    ND = 11
    counts = [0] * ND
    bad = [0] * ND
    ex = [[] for _ in range(ND)]
    hists = {}
    obs = {}

    hl_flip = (TAMPER == 'hl')
    hbd_flip = (TAMPER == 'hbd')

    def cmpd(i, ok, note):
        counts[i] += 1
        if not ok:
            bad[i] += 1
            if len(ex[i]) < 6: ex[i].append(note)

    def pairX(z, k, m, g):
        R = 2 * m + g + k
        return H_canonical(R, tuple(sorted([m, m + g], reverse=True)), z)

    # -------- D1: general band census, planes w=0..16 -------------------
    for w in range(0, 17):
        for m in range(1, 13):
            for g in range(1, 26):
                for k in range(max(-60, -2 * m - g), 1):
                    R = 2 * m + g + k
                    h = pairX(w, k, m, g)
                    exp = cpsfG(w, R, R - 2 * m)
                    if hl_flip:
                        exp = flipC(exp)
                    cmpd(0, h == exp, [1, w, m, g, k, h, exp])
            clear()

    # -------- D2: general bed census, planes w=0..16 ---------------------
    for w in range(0, 17):
        for m in range(1, 15):
            for j in range(-30, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = H_canonical(R, (m, m), w)
                exp = cpsfG(w, R, j)
                if hbd_flip:
                    exp = flipC(exp)
                cmpd(1, h == exp, [2, w, m, j, h, exp])
            clear()

    # -------- D3: typed general self-check, planes w=0..16 ---------------
    for w in range(0, 17):
        for m in range(1, 11):
            for g in range(1, 15):
                for k in range(max(-14, -2 * m - g), 1):
                    R = 2 * m + g + k
                    exp = cpsfG(w, R, R - 2 * m)
                    mx = typed_pair(R, m, g, w)
                    h = pairX(w, k, m, g)
                    cmpd(2, mx == exp == h, [3, w, m, g, k, exp, mx, h])
            for j in range(-16, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                exp = cpsfG(w, R, j)
                mx = typed_bed(R, m, j, w)
                h = H_canonical(R, (m, m), w)
                cmpd(2, mx == exp == h, [3, w, m, j, R, exp, mx, h])
            clear()

    # -------- D4: crossing/seam row census, planes w=0..16 ---------------
    for w in range(0, 17):
        L = Lw(w)
        for R in range(max(0, L - 2), L + 5):
            for m in range(1, 19):
                for g in range(1, 27):
                    k = R - 2 * m - g
                    if k < -26 or k > 0:
                        continue
                    h = pairX(w, k, m, g)
                    exp = cpsfG(w, R, R - 2 * m)
                    cmpd(3, h == exp, [4, w, R, m, g, k, h, exp])
                clear()
                for j in range(-30, 1):
                    Rb = 2 * m + j
                    if Rb < 0 or not (max(0, L - 2) <= Rb <= L + 4):
                        continue
                    h = H_canonical(Rb, (m, m), w)
                    exp = cpsfG(w, Rb, j)
                    cmpd(3, h == exp, [4, w, Rb, m, j, h, exp])
                clear()

    # -------- D5: L-BU-GEN, w<=30, x<=34 ---------------------------------
    for w in range(0, 31):
        for x in range(1, 35):
            for t in range(0, min(x, 36) + 1):
                cf = v(x, w + 1, t)
                want = cpsfG(w, t, t)
                hc = vC(x, w + 1, t)
                cmpd(4, cf == want == hc, [5, w, x, t, cf, want, hc])
            clear()

    # -------- D6: closed form vs both engines (published anchor box) -----
    for x in range(2, 17):
        for z in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13):
            for R in range(x + 1, x + 5):
                hc = vC(x, z, R)
                ho = vO(x, z, R)
                cmpd(5, hc == v(x, z, R), [6, 'C', x, z, R, hc])
                cmpd(5, ho == v(x, z, R), [6, 'O', x, z, R, ho])
            clear()

    # -------- D7: subsumption identity sweep, planes w=0..14 --------------
    # (published per-plane claims K1286/K1288/K1289/K1290/K1294/K1299/
    #  K1301/K1302 z13z14 transcriptions == CPSF-GEN == engine)
    for w in range(0, 15):
        pc, bc = PLANE_CLAIMS[w]
        for m in range(1, 11):
            for g in range(1, 19):
                for k in range(max(-12, -2 * m - g), 1):
                    R = 2 * m + g + k
                    d = R - 2 * m
                    h = pairX(w, k, m, g)
                    c = cpsfG(w, R, d)
                    e = pc(R, m, g, k)
                    cmpd(6, h == c == e, [7, w, m, g, k, h, c, e])
            for j in range(-12, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = H_canonical(R, (m, m), w)
                c = cpsfG(w, R, j)
                e = bc(R, m, j)
                cmpd(6, h == c == e, [7, w, m, j, h, c, e])
            clear()

    # -------- D8: NEW-plane census w=17..20 ------------------------------
    for w in range(17, 21):
        mm = 0
        for m in range(1, 13):
            for g in range(1, 17):
                for k in range(max(-40, -2 * m - g), 1):
                    R = 2 * m + g + k
                    if R < 0:
                        continue
                    h = pairX(w, k, m, g)
                    exp = cpsfG(w, R, R - 2 * m)
                    cmpd(7, h == exp, [8, w, m, g, k, h, exp])
                    mm += 1
            clear()
            for j in range(-24, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = H_canonical(R, (m, m), w)
                exp = cpsfG(w, R, j)
                cmpd(7, h == exp, [8, w, m, j, h, exp])
                mm += 1
        obs['w%d_newplane' % w] = {'points': mm,
                                   'claim': 'census of the PROVED general law '
                                            'on a plane never observed '
                                            'pre-K1303.'}

    # -------- D9: T-TWIN algebra identity --------------------------------
    for d in range(-260, 261):
        if d == 1:
            cmpd(8, g1(d) == 2 == f0(d), [9, 'core', d])
        else:
            cmpd(8, g1(d) == (1 ^ f0(d)), [9, 'twin', d])

    # -------- D10: cross-engine canonical vs ordered ---------------------
    for z in (0, 5, 11, 13, 16, 19):
        for m in range(1, 8):
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
                cmpd(9, hc == ho, [10, 'BED', z, m, j, hc, ho])
            clear()

    # -------- D11: stress (census beyond the audit boxes) ----------------
    # far-m rows
    fmn = 0
    for w in (3, 9, 13, 16):
        for m in range(13, 33):
            for g in range(1, 15):
                for k in range(-20, 1):
                    R = 2 * m + g + k
                    if R < 0:
                        continue
                    h = pairX(w, k, m, g)
                    exp = cpsfG(w, R, R - 2 * m)
                    cmpd(10, h == exp, [11, 'farm', w, m, g, k, h, exp])
                    fmn += 1
            clear()
    obs['far_m_rows'] = {'points': fmn, 'm': '13..32',
                         'planes': [3, 9, 13, 16],
                         'claim': 'census stress beyond the D-boxes.'}
    # dedup (R,delta) sweep z=0..20
    for z in range(0, 21):
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
        for (R, dd), vals in sorted(tab.items()):
            c = cpsfG(z, R, dd)
            for x in vals:
                cmpd(10, x == c, [11, 'dedup', z, R, dd, x, c])
                if x != c:
                    bb += 1
        obs['z%02d_dedup' % z] = {'cells': len(tab), 'mixed': mixed,
                                  'cpsf_bad': bb,
                                  'claim': 'census of the PROVED general law; '
                                           'not a new claim.'}
    # spot planes w=21..24
    spn = 0
    for w in range(21, 25):
        for m in range(1, 9):
            for g in range(1, 13):
                for k in range(max(-18, -2 * m - g), 1):
                    R = 2 * m + g + k
                    if R < 0:
                        continue
                    h = pairX(w, k, m, g)
                    exp = cpsfG(w, R, R - 2 * m)
                    cmpd(10, h == exp, [11, 'spot', w, m, g, k, h, exp])
                    spn += 1
            clear()
            for j in range(-12, 1):
                R = 2 * m + j
                if R < 0:
                    continue
                h = H_canonical(R, (m, m), w)
                exp = cpsfG(w, R, j)
                cmpd(10, h == exp, [11, 'spot-b', w, m, j, h, exp])
                spn += 1
    obs['w2124_spot'] = {'points': spn, 'w': '21..24',
                         'claim': 'census of the PROVED general law.'}

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

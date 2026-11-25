#!/usr/bin/env python3
"""verify_k1309: machine audit for the WINDOW-CONGRUENT COLLAPSE package
(the congruent half of the transition window 1 <= k <= z-1, k congruent
z (mod 2); K1308 open registration O1, observation OBS-WC).

Theorems under audit (claims and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of
the hand proofs pointwise, it does NOT replace the proofs; all quantifiers
are UNBOUNDED, censuses are consistency checks only):

  T-WC  (universal): for all z>=3, m>=1, g>=1, k in [1, z-1] with
        k congruent z (mod 2):
        H(2m+g+k; (m, m+g); z) = ZDIAG(g, z) = [g odd] (g<=z) / 2 (g=z+1)
        / [g even] (g>=z+2)  -- the published K1308 Z-DIAG law, here
        extended from the k=z row to EVERY congruent window row: the
        value is independent of k (and of m).
  T-WBC (universal): for all z>=3, a>=1, k congruent as above:
        H(2a+k; (a, a); z) = 0.
  L-BE (B-exit table, derived from the published K0832 closed form):
        for m=1 window pairs the B-exit single token v(g+1, z+1, g+k+1)
        equals [g even] (g<=z-1) / 2 (g=z) / [z even] (g=z+1) /
        [g odd] (g>=z+2)  -- k-independent on the window.
  L-C  (C-child table, derived from the published K1303 band T-GEPSF):
        the C-child value of a window pair is D(g, z-1) (= ZDIAG at the
        plane below) EXCEPT the explicit small-band exception cells
        (k=1 and 2m+g <= z-2), where the band sub-law gives 2*[g odd].
        For window beds the C-child value is 0 in both band subcases.
  Typed child identities (engine-free position equalities): every option
        of a window pair lands in {window pair (k same, z same),
        window bed (g=1 corner), single token (m=1 B-exit), window pair
        one plane down (C), band k=0 row (C from k=1)}; every option of a
        window bed lands in {window pair gap 1 (A), single token (a=1 B),
        window/band bed one plane down (C)}.
  SUBSUMPTION: the K1308 E4b census box (z3..13, m<=3, g<=12, 1,296 pts)
        is T-WC instances; OBS-WC is thereby universalized (the
        surviving congruent half of the refuted window-alternation
        conjecture).

Batteries (counts and the mutation table are declared in the single-owner
note; expected overall_bad == 0; stdout deterministic byte-identical,
volatile info on stderr only):

  D1  T-WC pair census engine vs claim: z3..16, m<=8, g<=24.
  D2  T-WC far stress: z in {18,20,22}, m<=4, g<=32.
  D3  T-WC m-distance stress: z in {5,8,11,14}, m<=20, g<=12.
  D4  T-WBC census: z3..16 a<=12; far z in {18,20,22} a<=8.
  D5  typed self-check (children built ONLY from the hand tables: T-WC /
      T-WBC / L-BE / L-C + the published K0832 closed form; mex must
      equal the claim AND the engine): z3..16, m<=6, g<=24, a<=12.
  D6  L-BE vs the published closed form vs BOTH engines, full box.
  D7  band + L-C engine gates: k=0 pair band rows vs cpsfG (K1303
      transcription), k=0 bed band rows vs cpsfG, and the L-C hand table
      vs the engine on all k=1 C-children (z odd 3..21).
  D8  published anchors: K1308 Z-DIAG (k=z), T-DU' (k>=z beds), T-UH
      (k>=z+1 pairs).
  D9  cross-engine canonical vs ordered, window samples.
  D10 the non-congruent window census (NO claim, observation only):
      the frozen 35-row value-distribution table must reproduce exactly.
  D11 k=1 row stress: z odd 3..27, m<=12, g<=30, engine vs claim
      (covers the exception cells).

TAMPER modes: --tamper-engine (rc 2), --tamper=<wc1|wc2|wc3|bw|ty|be|cp|
ps|xg|rw|ex> (flip exactly one battery's expectation; all rc 1 with the
exact pre-declared bad counts). Determinism: official runs
byte-identical on stdout.
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


# ---- claims under audit (with per-battery tamper flips) ------------------
if TAMPER in ('wc1', 'wc2', 'wc3', 'ty'):
    FLIP = True
else:
    FLIP = False


def flipC(c):
    return c ^ 1


def zdiag(g, z):
    """Published K1308 Z-DIAG law (transcription)."""
    if g <= z:
        return IND(g % 2 == 1)
    if g == z + 1:
        return 2
    return IND(g % 2 == 0)


def zdiagT(g, z):
    """claim used by the TYPED construction (battery D5) - flippable."""
    c = zdiag(g, z)
    return flipC(c) if FLIP else c


def bedwT(k, z):
    """T-WBC claim used by the TYPED construction - flippable."""
    return (1 if FLIP else 0)


def window_ks(z):
    return [kk for kk in range(1, z) if (kk % 2) == (z % 2)]


def bexit(g, z, k):
    """L-BE hand table: B-exit single token for m=1 window pairs."""
    if g <= z - 1:
        return IND(g % 2 == 0)
    if g == z:
        return 2
    if g == z + 1:
        return IND(z % 2 == 0)
    return IND(g % 2 == 1)


def bexitT(g, z, k):
    c = bexit(g, z, k)
    return flipC(c) if FLIP else c


def cval_pair(m, g, k, z):
    """L-C hand table: C-child VALUE (before the 1 XOR) of a window pair."""
    if k == 1:
        if 2 * m + g <= z - 2:
            return 2 * IND(g % 2 == 1)   # small-band exception sub-law
        return zdiag(g, z - 1)
    return zdiag(g, z - 1)


def cval_pairT(m, g, k, z):
    """flippable variant for battery D5 (children from flipped tables)."""
    if k == 1:
        if 2 * m + g <= z - 2:
            return flipC(2 * IND(g % 2 == 1)) if FLIP else 2 * IND(g % 2 == 1)
        c = zdiag(g, z - 1)
    else:
        c = zdiag(g, z - 1)
    return flipC(c) if FLIP else c


# K1303 general-w band transcription (T-GEPSF / T-GEBED; cpsfG).
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


def Lw(w):
    return 2 * ((w + 1) // 2)


def sw(w):
    return 2 * (w // 2)


def Tw(w, d):
    return g1(d) if w % 2 else f0(d)


def cpsfG(w, R, d):
    if R < Lw(w):
        return 2 * (R % 2)
    return Tw(w, d - sw(w))


def mexs(vals):
    s = set(vals)
    i = 0
    while i in s:
        i += 1
    return i


def typed_pair_children(m, g, k, z, table=False):
    """values of ALL options of window pair (m,m+g)@(2m+g+k) plane z,
    built ONLY from the hand tables (table=True: the flippable variant
    used by battery D5); the engine plays no role here."""
    if table:
        zd = zdiagT
        bd = bedwT
        be = bexitT
        cv = cval_pairT
    else:
        zd = zdiag
        bd = lambda kk, zz: 0
        be = bexit
        cv = cval_pair
    kids = []
    if m >= 2:
        kids.append(zd(g + 1, z))            # A-fall pair (m-1, m+g), k same
    if g >= 2:
        kids.append(zd(g - 1, z))            # A-compress pair, k same
    else:
        kids.append(bd(k, z))                # corner: T-WBC window bed
    if m == 1:
        kids.append(be(g, z, k))             # B-exit single token (L-BE)
    kids.append(1 ^ cv(m, g, k, z))          # C one plane down (L-C)
    return kids


def typed_bed_children(a, k, z, table=False):
    """values of ALL options of window bed (a,a)@(2a+k) plane z."""
    kids = []
    if a >= 2:
        kids.append(zdiagT(1, z) if table else zdiag(1, z))  # A: pair g=1
    else:
        kids.append(v(1, z + 1, k + 1))      # B: single 1, K0832 closed form
    kids.append(1 ^ 0)                       # C: window/band bed -> 0 (L-C)
    return kids


def pairX(z, k, m, g):
    R = 2 * m + g + k
    return H_canonical(R, tuple(sorted([m, m + g], reverse=True)), z)


def bedX(z, k, a):
    R = 2 * a + k
    return H_canonical(R, (a, a), z)


def main():
    t0 = time.time()
    res = {'kit': 'verify_k1309', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS', 'tamper': TAMPER}
    ND = 11
    counts = [0] * ND
    bad = [0] * ND
    ex = [[] for _ in range(ND)]
    obs = {}

    def cmpd(i, ok, note):
        counts[i] += 1
        if not ok:
            bad[i] += 1
            if len(ex[i]) < 6:
                ex[i].append(note)

    # -------- D1: T-WC pair census, z=3..16 ------------------------------
    for z in range(3, 17):
        for m in range(1, 9):
            for g in range(1, 25):
                for k in window_ks(z):
                    e = pairX(z, k, m, g)
                    if TAMPER == 'wc1':
                        exp = flipC(zdiag(g, z))
                    else:
                        exp = zdiag(g, z)
                    cmpd(0, e == exp, [1, z, m, g, k, e, exp])
        clear()

    # -------- D2: T-WC far stress, z in {18,20,22} ------------------------
    for z in (18, 20, 22):
        for m in range(1, 5):
            for g in range(1, 33):
                for k in window_ks(z):
                    e = pairX(z, k, m, g)
                    if TAMPER == 'wc2':
                        exp = flipC(zdiag(g, z))
                    else:
                        exp = zdiag(g, z)
                    cmpd(1, e == exp, [2, z, m, g, k, e, exp])
        clear()

    # -------- D3: T-WC m-distance stress, m<=20 ---------------------------
    for z in (5, 8, 11, 14):
        for m in range(1, 21):
            for g in range(1, 13):
                for k in window_ks(z):
                    e = pairX(z, k, m, g)
                    if TAMPER == 'wc3':
                        exp = flipC(zdiag(g, z))
                    else:
                        exp = zdiag(g, z)
                    cmpd(2, e == exp, [3, z, m, g, k, e, exp])
        clear()

    # -------- D4: T-WBC census z3..16 a<=12; far z{18,20,22} a<=8 ---------
    for z in range(3, 17):
        for a in range(1, 13):
            for k in window_ks(z):
                e = bedX(z, k, a)
                exp = 1 if TAMPER == 'bw' else 0
                cmpd(3, e == exp, [4, z, a, k, e, exp])
        clear()
    for z in (18, 20, 22):
        for a in range(1, 9):
            for k in window_ks(z):
                e = bedX(z, k, a)
                exp = 1 if TAMPER == 'bw' else 0
                cmpd(3, e == exp, [4, z, a, k, e, exp])
        clear()

    # -------- D5: typed self-check (hand tables only) ---------------------
    for z in range(3, 17):
        for m in range(1, 7):
            for g in range(1, 25):
                for k in window_ks(z):
                    kids = typed_pair_children(m, g, k, z, table=(TAMPER == 'ty'))
                    mx = mexs(kids)
                    claim = zdiagT(g, z) if TAMPER == 'ty' else zdiag(g, z)
                    e = pairX(z, k, m, g)
                    ok = (mx == claim) and (e == mx)
                    cmpd(4, ok, [5, z, m, g, k, e, mx, claim, kids])
        for a in range(1, 13):
            for k in window_ks(z):
                kids = typed_bed_children(a, k, z, table=(TAMPER == 'ty'))
                mx = mexs(kids)
                claim = bedwT(k, z)
                e = bedX(z, k, a)
                ok = (mx == claim) and (e == mx)
                cmpd(4, ok, [5, z, a, k, e, mx, claim, kids])
        clear()

    # -------- D6: L-BE vs published closed form vs BOTH engines -----------
    for z in range(3, 17):
        for g in range(1, 25):
            for k in window_ks(z):
                b = bexit(g, z, k)
                if TAMPER == 'be':
                    b = flipC(b)
                st = v(g + 1, z + 1, g + k + 1)
                e1 = vC(g + 1, z + 1, g + k + 1)
                e2 = vO(g + 1, z + 1, g + k + 1)
                cmpd(5, b == st == e1 == e2, [6, g, z, k, b, st, e1, e2])
        clear()

    # -------- D7: band + L-C engine gates ---------------------------------
    # (a) k=0 pair band rows vs cpsfG (K1303 transcription)
    for w in range(2, 16):
        for m in range(1, 7):
            for g in range(1, 21):
                e = pairX(w, 0, m, g)
                cp = cpsfG(w, 2 * m + g, g)
                if TAMPER == 'cp':
                    cp = flipC(cp)
                cmpd(6, e == cp, [7, 'pairband', w, m, g, e, cp])
        clear()
    # (b) k=0 bed band rows vs cpsfG
    for w in range(2, 16):
        for a in range(1, 11):
            e = bedX(w, 0, a)
            cp = cpsfG(w, 2 * a, 0)
            if TAMPER == 'cp':
                cp = flipC(cp)
            cmpd(6, e == cp, [7, 'bedband', w, a, e, cp])
        clear()
    # (c) L-C hand table vs engine on ALL k=1 C-children (z odd 3..21)
    for z in range(3, 22, 2):
        for m in range(1, 9):
            for g in range(1, 25):
                e = pairX(z - 1, 0, m, g)          # the C-child cell itself
                cv = cval_pair(m, g, 1, z)
                if TAMPER == 'cp':
                    cv = flipC(cv)
                cmpd(6, e == cv, [7, 'lc', z, m, g, e, cv])
        clear()

    # -------- D8: published anchors ---------------------------------------
    # (a) K1308 Z-DIAG (k=z rows), z3..10, m<=6, g<=18
    for z in range(3, 11):
        for m in range(1, 7):
            for g in range(1, 19):
                e = pairX(z, z, m, g)
                exp = flipC(zdiag(g, z)) if TAMPER == 'ps' else zdiag(g, z)
                cmpd(7, e == exp, [8, 'zdiag', z, m, g, e, exp])
        clear()
    # (b) K1308 T-DU' beds k=z..z+3, z0..6, a<=8
    for z in range(0, 7):
        for a in range(1, 9):
            for k in range(z, z + 4):
                e = bedX(z, k, a)
                exp = 1 if TAMPER == 'ps' else 0
                cmpd(7, e == exp, [8, 'tdu', z, a, k, e, exp])
        clear()
    # (c) K1308 T-UH pairs k=z+1..z+3, z0..6, m<=6, g<=12
    for z in range(0, 7):
        for m in range(1, 7):
            for g in range(1, 13):
                for k in range(z + 1, z + 4):
                    e = pairX(z, k, m, g)
                    exp = IND(g % 2 == 1)
                    if TAMPER == 'ps':
                        exp = flipC(exp)
                    cmpd(7, e == exp, [8, 'tuh', z, m, g, k, e, exp])
        clear()

    # -------- D9: cross-engine canonical vs ordered, window samples -------
    tot9 = bad9 = 0
    for z in (3, 5, 8, 11):
        for m in range(1, 4):
            for g in range(1, 10):
                for k in window_ks(z):
                    c = pairX(z, k, m, g)
                    o = H_ordered(2 * m + g + k, (m, m + g), z)
                    ok = c == o
                    if TAMPER == 'xg':
                        ok = not ok
                    cmpd(8, ok, [9, z, m, g, k, c, o])
        for a in range(1, 5):
            for k in window_ks(z):
                c = bedX(z, k, a)
                o = H_ordered(2 * a + k, (a, a), z)
                ok = c == o
                if TAMPER == 'xg':
                    ok = not ok
                cmpd(8, ok, [9, z, a, k, c, o])
        clear()

    # -------- D10: non-congruent window census (OBS, no claim) -----------
    frozen = {
        '3,2': {0: 18, 1: 18}, '4,1': {0: 17, 1: 16, 2: 3},
        '4,3': {0: 18, 1: 18}, '5,2': {0: 18, 1: 16, 2: 2},
        '5,4': {0: 18, 1: 18}, '6,1': {0: 16, 1: 16, 2: 4},
        '6,3': {0: 18, 1: 18}, '6,5': {0: 18, 1: 18},
        '7,2': {0: 17, 1: 16, 2: 3}, '7,4': {0: 18, 1: 18},
        '7,6': {0: 18, 1: 18}, '8,1': {0: 15, 1: 16, 2: 5},
        '8,3': {0: 17, 1: 18, 2: 1}, '8,5': {0: 18, 1: 18},
        '8,7': {0: 18, 1: 18}, '9,2': {0: 17, 1: 16, 2: 3},
        '9,4': {0: 18, 1: 18}, '9,6': {0: 18, 1: 18},
        '9,8': {0: 18, 1: 18}, '10,1': {0: 15, 1: 16, 2: 5},
        '10,3': {0: 17, 1: 18, 2: 1}, '10,5': {0: 18, 1: 18},
        '10,7': {0: 18, 1: 18}, '10,9': {0: 18, 1: 18},
        '11,2': {0: 17, 1: 16, 2: 3}, '11,4': {0: 18, 1: 18},
        '11,6': {0: 18, 1: 18}, '11,8': {0: 18, 1: 18},
        '11,10': {0: 18, 1: 18}, '12,1': {0: 15, 1: 16, 2: 5},
        '12,3': {0: 17, 1: 18, 2: 1}, '12,5': {0: 18, 1: 18},
        '12,7': {0: 18, 1: 18}, '12,9': {0: 18, 1: 18},
        '12,11': {0: 18, 1: 18},
    }
    from collections import defaultdict
    rows = defaultdict(dict)
    for z in range(3, 13):
        for m in range(1, 4):
            for g in range(1, 13):
                for k in range(1, z):
                    if (k % 2) == (z % 2):
                        continue
                    e = pairX(z, k, m, g)
                    d = rows['%d,%d' % (z, k)]
                    d[e] = d.get(e, 0) + 1
        clear()
    rows = {kk: dict(vv) for kk, vv in rows.items()}
    if TAMPER == 'rw':
        rows = dict(rows)
        rows['3,2'] = {0: 18, 1: 17}
    obs['noncongruent_window_rows'] = {kk: rows[kk] for kk in sorted(rows)}
    for kk in sorted(frozen):
        cmpd(9, rows.get(kk) == frozen[kk], [10, kk, rows.get(kk), frozen[kk]])
    obs['noncongruent_row_count'] = len(rows)

    # -------- D11: k=1 row stress (exception cells incl.), z odd 3..27 ----
    n_exc = 0
    for z in range(3, 28, 2):
        for m in range(1, 13):
            for g in range(1, 31):
                e = pairX(z, 1, m, g)
                if 2 * m + g <= z - 2:
                    n_exc += 1
                exp = flipC(zdiag(g, z)) if TAMPER == 'ex' else zdiag(g, z)
                cmpd(10, e == exp, [11, z, m, g, e, exp])
        clear()
    obs['k1_exception_cells_in_box'] = n_exc

    info = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['obs'] = obs
    res['battery_names'] = ['D1_twc_census', 'D2_twc_far', 'D3_twc_mdistance',
                            'D4_twc_bed_census', 'D5_typed_selfcheck',
                            'D6_lbe_closed_engines', 'D7_band_lc_engine',
                            'D8_published_anchors', 'D9_cross_engine',
                            'D10_noncongruent_obs', 'D11_k1row_stress']
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)


main()

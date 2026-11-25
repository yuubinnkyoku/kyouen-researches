#!/usr/bin/env python3
"""verify_k1310: machine audit for the NON-CONGRUENT WINDOW COLLAPSE package
(the non-congruent half of the transition window 1 <= k <= z-1, k NOT
congruent z (mod 2); the K1309 open registrations O1' and O2, observation
OBS-NCW).

Theorems under audit (claims and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of
the hand proofs pointwise, it does NOT replace the proofs; all quantifiers
are UNBOUNDED, censuses are consistency checks only):

  T-NCW-P (universal): for all z >= 2, m >= 1, g >= 1, k in [1, z-1] with
        k NOT congruent z (mod 2), let g* = z-2k:
        H(2m+g+k; (m, m+g); z) =
          [g odd]   if g* <= 0 or g > g* or 2m+g < z
          2         if g <= g* and 2m+g >= z and (g = g* or g = z-2m)
          [g even]  otherwise (the flip wedge g < g*, 2m+g > z).
        In the anomaly wedge {(m,g): 1 <= g <= g*, 2m+g >= z} the value m
        is automatically >= k; the 2s lie EXACTLY on the dominant column
        g = g* and the diagonal g = z-2m; everything else in the wedge is
        the parity-flipped [g even]. Outside the wedge the row never sees
        a 2 (in particular NO Z-DIAG superdiagonal 2 at g = z+1: the
        non-congruent rows carry a genuinely different law from T-WC).
  T-NCW-B (universal): for all z >= 2, a >= 1, k as above, g* = z-2k,
        r = (z-1)//2:
        H(2a+k; (a, a); z) =
          0                     if g* < 0 (2k > z; includes every
                                k = z-1 top row = the OBS-BW resolution)
          [a <= r] 0, [a >= r+1] 2        if g* = 0 (z even, k = z/2)
          [a <= r] 0, [a = r+1] 2, [a >= r+2] 1    if z even, g* > 0
          [a <= r] 0, [a >= r+1] 1         if z odd (g* > 0).
  Typed child identities (engine-free position equalities): every option
        of a non-congruent window pair lands in {window pair (k, z) same
        (A), window bed same (k, z) at the g=1 corner (A), single token
        (m=1 B-exit, K0832 closed form), non-congruent window pair
        (k-1, z-1) (C, k >= 2 -- the C-descent PRESERVES non-congruence:
        this packet closes on the single-R strong induction where the
        K1309 congruent packet could not), band k=0 row plane z-1
        (C from k=1, K1303)}; every option of a non-congruent window bed
        lands in {window pair g=1 (A, a >= 2), single token (a=1 B),
        non-congruent window bed (k-1, z-1) or band bed (C)}.
  SUBSUMPTION: the K1309 OBS-NCW frozen 35-row value-distribution table
        (z3..12 m1..3 g1..12, engine census) reproduces exactly AND equals
        the T-NCW-P claim cellwise — the observation register is thereby
        universalized to the theorem. The z=2 base rows (pair k=1 = [g odd]
        and bed k=1 = 2 for all a) are consistent with the published K1286
        z=2 rows (b2(1)=2; z2-k1 pair row).

Batteries (counts and the mutation table are declared in the single-owner
note; expected overall_bad == 0; stdout deterministic byte-identical,
volatile info on stderr only):

  D1  T-NCW-P pair census engine vs claim: z3..16, m<=8, g<=24.
  D2  T-NCW-P far stress: z in {18,20,22}, m<=4, g<=48.
  D3  T-NCW-P m-distance stress: z in {5,8,11,14}, m<=20, g<=12 (all
      diagonal cells of those planes reachable within g<=12).
  D4  T-NCW-B census: z3..16 a<=26; far z{18,20,22} a<=14.
  D5  typed self-check (children built ONLY from the claims + published
      K0832/K1303 closed forms; mex must equal the claim AND the engine),
      including the z=2 induction-base rows: pairs z2..14 m<=6 g<=28,
      beds z2..14 a<=16.
  D6  B-exit triple check: single_token closed form vs BOTH engines on
      every m=1 NCW B-exit (z3..16, g<=24, all NCW k).
  D7  band k=0 gates (K1303 transcription cpsfG): pair band w1..15 m<=6
      g<=20; bed band w1..15 a<=10; and the k=1 C-child cells vs cpsfG
      (z even 4..22, m<=8, g<=24 — the NCW counterpart of the K1309
      congruent L-C gate).
  D8  published anchors: K1309 T-WC (z3..10 congruent rows), T-WBC beds,
      K1308 Z-DIAG k=z rows z3..10, T-UH z0..6 k=z+1..z+3, T-DU'
      z0..6 k=z..z+3.
  D9  cross-engine canonical vs ordered, NCW samples.
  D10 OBS-NCW subsumption: engine re-census must reproduce the frozen
      35-row distributions AND the claim cellwise.
  D11 k=1 row stress: z even 4..28, m<=12, g<=30.
  D12 bed tail & k=z-1 stress: k=z-1 rows z3..20 a<=30; deep tails
      a<=40 at z in {6,10,14,18}.

TAMPER modes: --tamper-engine (rc 2), --tamper=<np1|np2|np3|bd|ty|be|
cp|ps|xg|rw|ex|bs> (flip exactly one battery's expectation; all rc 1 with
the exact pre-declared bad counts). Determinism: official runs
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


# ---- claims under audit ---------------------------------------------------
if TAMPER == 'ty':
    FLIP = True
else:
    FLIP = False


def flipC(c):
    return c ^ 1


def P(k, z, m, g):
    """T-NCW-P claim."""
    gs = z - 2 * k
    if gs <= 0 or g > gs or 2 * m + g < z:
        c = IND(g % 2 == 1)
    elif g == gs or g == z - 2 * m:
        c = 2
    else:
        c = IND(g % 2 == 0)
    return flipC(c) if FLIP else c


def Bm(k, z, a):
    """T-NCW-B claim."""
    gs = z - 2 * k
    if gs < 0:
        c = 0
    else:
        r = (z - 1) // 2
        if a <= r:
            c = 0
        elif z % 2 == 1:
            c = 1
        elif gs == 0:
            c = 2
        elif a == r + 1:
            c = 2
        else:
            c = 1
    return flipC(c) if FLIP else c


def ncw_ks(z):
    return [kk for kk in range(1, z) if (kk % 2) != (z % 2)]


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


def zdiag(g, z):
    """Published K1308 Z-DIAG law (transcription)."""
    if g <= z:
        return IND(g % 2 == 1)
    if g == z + 1:
        return 2
    return IND(g % 2 == 0)


def mexs(vals):
    s = set(vals)
    i = 0
    while i in s:
        i += 1
    return i


# ---- typed children (ONLY claims + published closed forms) -----------------
def typed_pair_children(m, g, k, z):
    kids = []
    if m >= 2:
        kids.append(P(k, z, m - 1, g + 1))          # A-fall
    else:
        kids.append(v(g + 1, z + 1, g + k + 1))     # B-exit single token
    if g >= 2:
        kids.append(P(k, z, m, g - 1))              # A-compress
    else:
        kids.append(Bm(k, z, m))                    # corner -> bed claim
    if k >= 2:
        kids.append(1 ^ P(k - 1, z - 1, m, g))      # C, NCW row below
    else:
        kids.append(1 ^ cpsfG(z - 1, 2 * m + g, g))  # C, band k=0
    return kids


def typed_bed_children(a, k, z):
    kids = []
    if a >= 2:
        kids.append(P(k, z, a - 1, 1))               # A-fall -> pair g=1
    else:
        kids.append(v(1, z + 1, k + 1))             # B single 1
    if k >= 2:
        kids.append(1 ^ Bm(k - 1, z - 1, a))        # C, NCW bed below
    else:
        kids.append(1 ^ cpsfG(z - 1, 2 * a, 0))     # C, band bed
    return kids


def pairX(z, k, m, g):
    R = 2 * m + g + k
    return H_canonical(R, tuple(sorted([m, m + g], reverse=True)), z)


def bedX(z, k, a):
    R = 2 * a + k
    return H_canonical(R, (a, a), z)


def main():
    t0 = time.time()
    res = {'kit': 'verify_k1310', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS', 'tamper': TAMPER}
    ND = 12
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

    # -------- D1: T-NCW-P pair census, z3..16 ------------------------------
    for z in range(3, 17):
        for m in range(1, 9):
            for g in range(1, 25):
                for k in ncw_ks(z):
                    e = pairX(z, k, m, g)
                    exp = flipC(P(k, z, m, g)) if TAMPER == 'np1' else P(k, z, m, g)
                    cmpd(0, e == exp, [1, z, m, g, k, e, exp])
        clear()

    # -------- D2: T-NCW-P far stress, z {18,20,22} ------------------------
    for z in (18, 20, 22):
        for m in range(1, 5):
            for g in range(1, 49):
                for k in ncw_ks(z):
                    e = pairX(z, k, m, g)
                    exp = flipC(P(k, z, m, g)) if TAMPER == 'np2' else P(k, z, m, g)
                    cmpd(1, e == exp, [2, z, m, g, k, e, exp])
        clear()

    # -------- D3: T-NCW-P m-distance stress, m<=20 ------------------------
    for z in (5, 8, 11, 14):
        for m in range(1, 21):
            for g in range(1, 13):
                for k in ncw_ks(z):
                    e = pairX(z, k, m, g)
                    exp = flipC(P(k, z, m, g)) if TAMPER == 'np3' else P(k, z, m, g)
                    cmpd(2, e == P(k, z, m, g) if TAMPER != 'np3' else None or (e == flipC(P(k, z, m, g))), [3, z, m, g, k, e])
        clear()

    # -------- D4: T-NCW-B census ------------------------------------------
    for z in range(3, 17):
        for a in range(1, 27):
            for k in ncw_ks(z):
                e = bedX(z, k, a)
                exp = flipC(Bm(k, z, a)) if TAMPER == 'bd' else Bm(k, z, a)
                cmpd(3, e == exp, [4, z, a, k, e, exp])
        clear()
    for z in (18, 20, 22):
        for a in range(1, 15):
            for k in ncw_ks(z):
                e = bedX(z, k, a)
                exp = flipC(Bm(k, z, a)) if TAMPER == 'bd' else Bm(k, z, a)
                cmpd(3, e == exp, [4, z, a, k, e, exp])
        clear()

    # -------- D5: typed self-check (claims + closed forms only) -----------
    for z in range(2, 15):
        for m in range(1, 7):
            for g in range(1, 29):
                for k in ncw_ks(z):
                    kids = typed_pair_children(m, g, k, z)
                    mx = mexs(kids)
                    claim = P(k, z, m, g)
                    e = pairX(z, k, m, g)
                    ok = (mx == claim) and (e == mx)
                    cmpd(4, ok, [5, z, m, g, k, e, mx, claim, kids])
        for a in range(1, 17):
            for k in ncw_ks(z):
                kids = typed_bed_children(a, k, z)
                mx = mexs(kids)
                claim = Bm(k, z, a)
                e = bedX(z, k, a)
                ok = (mx == claim) and (e == mx)
                cmpd(4, ok, [5, z, a, k, e, mx, claim, kids])
        clear()

    # -------- D6: B-exit triple check (closed form vs both engines) -------
    for z in range(3, 17):
        for g in range(1, 25):
            for k in ncw_ks(z):
                stv = v(g + 1, z + 1, g + k + 1)
                if TAMPER == 'be':
                    stv = flipC(stv)
                e1 = vC(g + 1, z + 1, g + k + 1)
                e2 = vO(g + 1, z + 1, g + k + 1)
                cmpd(5, stv == e1 == e2, [6, z, g, k, stv, e1, e2])
        clear()

    # -------- D7: band k=0 gates + k=1 C-child cells ----------------------
    for w in range(1, 16):
        for m in range(1, 7):
            for g in range(1, 21):
                e = pairX(w, 0, m, g)
                cp = cpsfG(w, 2 * m + g, g)
                if TAMPER == 'cp':
                    cp = flipC(cp)
                cmpd(6, e == cp, [7, 'pairband', w, m, g, e, cp])
        for a in range(1, 11):
            e = bedX(w, 0, a)
            cp = cpsfG(w, 2 * a, 0)
            if TAMPER == 'cp':
                cp = flipC(cp)
            cmpd(6, e == cp, [7, 'bedband', w, a, e, cp])
        clear()
    for z in range(4, 23, 2):
        for m in range(1, 9):
            for g in range(1, 25):
                e = pairX(z - 1, 0, m, g)       # the k=1 C-child cell itself
                cp = cpsfG(z - 1, 2 * m + g, g)
                if TAMPER == 'cp':
                    cp = flipC(cp)
                cmpd(6, e == cp, [7, 'cchild', z, m, g, e, cp])
        clear()

    # -------- D8: published anchors ---------------------------------------
    for z in range(3, 11):   # K1309 T-WC congruent rows
        for m in range(1, 7):
            for g in range(1, 19):
                for k in [kk for kk in range(1, z) if (kk % 2) == (z % 2)]:
                    e = pairX(z, k, m, g)
                    exp = flipC(zdiag(g, z)) if TAMPER == 'ps' else zdiag(g, z)
                    cmpd(7, e == exp, [8, 'twc', z, m, g, k, e, exp])
        for a in range(1, 11):
            for k in [kk for kk in range(1, z) if (kk % 2) == (z % 2)]:
                e = bedX(z, k, a)
                exp = 1 if TAMPER == 'ps' else 0
                cmpd(7, e == exp, [8, 'twbc', z, a, k, e, exp])
        for m in range(1, 7):  # K1308 Z-DIAG k=z rows
            for g in range(1, 19):
                e = pairX(z, z, m, g)
                exp = flipC(zdiag(g, z)) if TAMPER == 'ps' else zdiag(g, z)
                cmpd(7, e == exp, [8, 'zdiag', z, m, g, e, exp])
        clear()
    for z in range(0, 7):    # K1308 T-UH pairs k=z+1..z+3
        for m in range(1, 7):
            for g in range(1, 13):
                for k in range(z + 1, z + 4):
                    e = pairX(z, k, m, g)
                    exp = IND(g % 2 == 1)
                    if TAMPER == 'ps':
                        exp = flipC(exp)
                    cmpd(7, e == exp, [8, 'tuh', z, m, g, k, e, exp])
        for a in range(1, 9):  # K1308 T-DU' beds k=z..z+3
            for k in range(z, z + 4):
                e = bedX(z, k, a)
                exp = 1 if TAMPER == 'ps' else 0
                cmpd(7, e == exp, [8, 'tdup', z, a, k, e, exp])
        clear()

    # -------- D9: cross-engine canonical vs ordered, NCW samples ----------
    for z in (3, 5, 8, 11):
        for m in range(1, 4):
            for g in range(1, 10):
                for k in ncw_ks(z):
                    c = pairX(z, k, m, g)
                    o = H_ordered(2 * m + g + k, (m, m + g), z)
                    ok = c == o
                    if TAMPER == 'xg':
                        ok = not ok
                    cmpd(8, ok, [9, z, m, g, k, c, o])
        for a in range(1, 5):
            for k in ncw_ks(z):
                c = bedX(z, k, a)
                o = H_ordered(2 * a + k, (a, a), z)
                ok = c == o
                if TAMPER == 'xg':
                    ok = not ok
                cmpd(8, ok, [9, z, a, k, c, o])
        clear()

    # -------- D10: OBS-NCW subsumption (frozen 35-row table) -------------
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
                    ok = e == P(k, z, m, g)
                    if TAMPER == 'rw':
                        ok = not ok
                    cmpd(9, ok, [10, 'claim', z, m, g, k, e])
        clear()
    obs['ncw_row_count'] = len(rows)
    for kk in sorted(frozen):
        target = dict(frozen[kk])
        if TAMPER == 'rw' and kk == '3,2':
            target = {0: 18, 1: 17}
        cmpd(9, rows.get(kk) == target, [10, 'frozen', kk, rows.get(kk), target])

    # -------- D11: k=1 row stress, z even 4..28 --------------------------
    for z in range(4, 29, 2):
        for m in range(1, 13):
            for g in range(1, 31):
                e = pairX(z, 1, m, g)
                exp = flipC(P(1, z, m, g)) if TAMPER == 'ex' else P(1, z, m, g)
                cmpd(10, e == exp, [11, z, m, g, e, exp])
        clear()

    # -------- D12: bed k=z-1 + deep-tail stress --------------------------
    for z in range(3, 21):
        for a in range(1, 31):
            k = z - 1
            e = bedX(z, k, a)
            exp = flipC(Bm(k, z, a)) if TAMPER == 'bs' else Bm(k, z, a)
            cmpd(11, e == exp, [12, 'km1', z, a, k, e, exp])
        clear()
    for z in (6, 10, 14, 18):
        for a in range(1, 41):
            for k in ncw_ks(z):
                e = bedX(z, k, a)
                exp = flipC(Bm(k, z, a)) if TAMPER == 'bs' else Bm(k, z, a)
                cmpd(11, e == exp, [12, 'tail', z, a, k, e, exp])
        clear()

    info = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['obs'] = obs
    res['battery_names'] = ['D1_tncwp_census', 'D2_tncwp_far', 'D3_tncwp_mdistance',
                            'D4_tncwb_census', 'D5_typed_selfcheck', 'D6_bexit_engines',
                            'D7_band_cchild_gates', 'D8_published_anchors',
                            'D9_cross_engine', 'D10_obsncw_subsumption',
                            'D11_k1row_stress', 'D12_bed_km1_tail']
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)


main()

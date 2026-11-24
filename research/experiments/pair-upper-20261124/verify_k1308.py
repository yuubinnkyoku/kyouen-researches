#!/usr/bin/env python3
"""verify_k1308: machine audit for the UPPER-HALF COLLAPSE package
(pairs k >= z diagonal-and-above, beds k >= z, single-token tail readings;
K1303 open registration O-G4 'far above-diagonal k > 0').

Theorems under audit (claims and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of the
hand proofs pointwise, it does NOT replace the proofs; all quantifiers are
UNBOUNDED, censuses are consistency checks only):

  T-UH (universal): for all z>=0, m>=1, g>=1, k>=z+1:
        H(2m+g+k; (m, m+g); z) = [g odd]   (independent of m, k, z).
  T-DU' (universal): for all z>=0, a>=1, k>=z:
        H(2a+k; (a, a); z) = 0.
        SHARP: k>=z is the exact threshold (z=1,k=0 -> 1; z=2,k=1 -> 2:
        the published K1286 T-B1/T-B2 rows b1(0)=1, b2(1)=2).
  Z-DIAG (universal): for all z>=0, m>=1, g>=1, k=z (the diagonal row):
        H(2m+g+z; (m, m+g); z) = [g odd]  (g <= z)
                                = 2       (g = z+1)
                                = [g even] (g >= z+2).
        Anchors: z=0 -> the f0 diagonal (= K1286 C1), z=1 -> Z1(1,·)
        (= K1286 C2), z=2 -> Z2(2,·) (= K1286 C3).
  L-SB (corollary of the published K0832 closed form): for x>=2, p>=1,
        j>=p: v(x, p, x+j) = x%2;  B-exit readings v(z+2, z+1, 2z+2)
        = (z+1)%2,  v(z+1, z+1, 2z+1) = 2,  v(1, p, R) = 1 for R>=2.
  Together with the published K1303 band (k <= 0, all planes) and the
        K1286 z2-k1 row, the pair planes z in {0,1,2} are CLOSED for ALL
        k; for z>=3 the only undetermined pair rows are the transition
        window 1 <= k <= z-1.

  C-SUM (CONJECTURE, census only, NO universal claim): in the tail the
        value is [S odd], S = token sum: triples/mixed/quad census boxes
        frozen from the pre-declaration exploration.

  REFUTED (honest record): the transition-window parity-alternation
        conjecture 'rows k not congruent z (mod 2) in 1<=k<=z-1 have the
        tail value [g odd]' FAILS from z=4 (29 counters on the frozen
        census); the surviving half (congruent rows follow Z-DIAG) is
        clean on the z3..13 census (observation only, unproved).

Batteries (counts and the mutation table are declared in the single-owner
note; expected overall_bad == 0; stdout deterministic byte-identical,
volatile info on stderr only):

  D1  T-UH census engine vs claim: z0..7, m<=10, g<=12, k=z+1..z+6.
  D2  T-DU' census: z0..8, a<=12, k=z..z+8.
  D3  Z-DIAG census: z0..8, m<=10, g<=14.
  D4  typed self-check (children built ONLY from the claim tables
      T-UH/Z-DIAG/T-DU' + the published K0832 closed form; the engine only
      arbitrates): pairs m<=6, g<=8, z<=6, k in {z..z+3} with the
      tail-uniformity assertion set(children) == {1-claim} for k>=z+1;
      beds a<=8, z<=6, k in {z..z+2} with the no-0-child assertion.
  D5  L-SB + B-exit readings vs BOTH engines vs the closed form.
  D6  published anchors: K1285 T-PS0/1/2 slices + T-ALM six beds;
      K1286 Z1(1,·)/z2-k1 [g odd]/Z2(2,·) rows + T-B1/T-B2/T-B0 beds.
  D7  plane-closure census z in {0,1,2}, k=1..8 (with the z2-k1 row).
  D8  C-SUM census boxes (CONJECTURE, clearly labeled in obs).
  D9  REFUTED recheck: the frozen window census must reproduce the
      'z=3 clean, z>=4 counters' pattern; full counter list in obs.
  D10 cross-engine canonical vs ordered, tail/diag/bed/triple samples.
  D11 stress beyond the audit boxes: far-m rows, high planes z<=24,
      far diagonal, far L-SB.

TAMPER modes: --tamper-engine (rc 2), --tamper=uh / du / zd / ty / sb /
ps / cs / rw (flip exactly one battery's expectations; all rc 1 with the
exact pre-declared bad counts = the full battery counts). Determinism:
official runs byte-identical on stdout.
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

# ---- the three new claims (flippable via TAMPER for the census
# batteries; the typed battery D4 flips only the target claim) -------


def tail(g):
    return IND(g % 2 == 1)


def zdiag(g, z):
    if g <= z:
        return IND(g % 2 == 1)
    if g == z + 1:
        return 2
    return IND(g % 2 == 0)


def bed0():
    return 0


def flipC(val):
    # tamper flip (K1285..K1303 semantics)
    return 1 - val if val in (0, 1) else 1


def pair_claim(k, z, g):
    """claim for a pair (m, m+g) at plane z, diagonal coordinate k>=z."""
    assert k >= z
    if k >= z + 1:
        c = tail(g)
    else:
        c = zdiag(g, z)
    if TAMPER == 'ty':
        c = flipC(c)
    return c


def bed_claim(k, z):
    assert k >= z
    return flipC(0) if TAMPER == 'ty' else 0


def mexs(vals):
    s = set(vals)
    x = 0
    while x in s:
        x += 1
    return x

# ---- typed children (children valued ONLY from the claim tables and
# the published K0832 closed form -- the engine never values a child) --


def typed_pair(R, m, g, z):
    """children of pair (m, m+g) at (R, z), k = R-2m-g >= z, from claims."""
    k = R - 2 * m - g
    assert k >= z
    kids = []
    # lower token: fall (m>=2) / B-exit (m=1 -> single token g+1 @ z+1)
    if m >= 2:
        kids.append(pair_claim(k, z, g + 1))
    else:
        kids.append(v(g + 1, z + 1, R - 1))
    # upper token: compress (g>=2) / corner (g=1 -> bed (m,m), k'=k)
    if g >= 2:
        kids.append(pair_claim(k, z, g - 1))
    else:
        kids.append(bed_claim(k, z))
    # C move: same pair, plane z-1, k-1 >= z-1 (diagonal or tail)
    if z >= 1:
        kids.append(1 ^ pair_claim(k - 1, z - 1, g))
    return kids


def typed_bed(R, a, z):
    """children of bed (a,a) at (R, z), k = R-2a >= z, from claims."""
    k = R - 2 * a
    assert k >= z
    kids = []
    if a >= 2:
        kids.append(pair_claim(k, z, 1))   # fall: pair (a-1, a), gap 1
    else:
        kids.append(v(1, z + 1, R - 1))    # B: single 1 @ plane z+1
    if z >= 1:
        kids.append(1 ^ bed_claim(k - 1, z - 1))
    return kids


def main():
    t0 = time.time()
    res = {'kit': 'verify_k1308', 'engine_sha': ENGINE_SHA,
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

    def pairX(z, k, m, g):
        R = 2 * m + g + k
        return H_canonical(R, tuple(sorted([m, m + g], reverse=True)), z)

    # -------- D1: T-UH census, z=0..7 ------------------------------------
    for z in range(0, 8):
        for m in range(1, 11):
            for g in range(1, 13):
                for k in range(z + 1, z + 7):
                    h = pairX(z, k, m, g)
                    exp = tail(g) if TAMPER != 'uh' else flipC(tail(g))
                    cmpd(0, h == exp, [1, z, m, g, k, h, exp])
            clear()

    # -------- D2: T-DU' census, z=0..8 -----------------------------------
    for z in range(0, 9):
        for a in range(1, 13):
            for k in range(z, z + 9):
                R = 2 * a + k
                h = H_canonical(R, (a, a), z)
                exp = 0 if TAMPER != 'du' else 1
                cmpd(1, h == exp, [2, z, a, k, h, exp])
            clear()

    # -------- D3: Z-DIAG census, z=0..8 ----------------------------------
    for z in range(0, 9):
        for m in range(1, 11):
            for g in range(1, 15):
                h = pairX(z, z, m, g)
                exp = zdiag(g, z) if TAMPER != 'zd' else flipC(zdiag(g, z))
                cmpd(2, h == exp, [3, z, m, g, h, exp])
            clear()

    # -------- D4: typed self-check (claims-only children) ----------------
    for z in range(0, 7):
        for m in range(1, 7):
            for g in range(1, 9):
                for k in range(z, z + 4):
                    R = 2 * m + g + k
                    kids = typed_pair(R, m, g, z)
                    mx = mexs(kids)
                    claim = pair_claim(k, z, g)
                    h = pairX(z, k, m, g)
                    ok = (mx == claim == h)
                    if k >= z + 1:
                        ok = ok and (set(kids) == {1 - claim})
                    cmpd(3, ok, [4, z, m, g, k, mx, claim, h, kids])
                clear()
        for a in range(1, 9):
            for kk in range(z, z + 3):
                R = 2 * a + kk
                kids = typed_bed(R, a, z)
                mx = mexs(kids)
                h = H_canonical(R, (a, a), z)
                ok = (mx == 0 == h) and (0 not in kids)
                cmpd(3, ok, [4, 'bed', z, a, kk, mx, h, kids])
            clear()

    # -------- D5: L-SB + B-exit readings ---------------------------------
    for x in range(1, 21):
        for p in range(1, 15):
            for j in range(p, p + 9):
                R = x + j
                a1 = v(x, p, R)
                h1 = vC(x, p, R)
                h2 = vO(x, p, R)
                exp = x % 2 if TAMPER != 'sb' else flipC(x % 2)
                cmpd(4, a1 == h1 == h2 == exp, [5, 'lsb', x, p, j, a1, h1, h2])
        clear()
    for z in range(0, 11):
        want = (z + 1) % 2 if TAMPER != 'sb' else flipC((z + 1) % 2)
        a1 = v(z + 2, z + 1, 2 * z + 2)
        h1 = vC(z + 2, z + 1, 2 * z + 2)
        h2 = vO(z + 2, z + 1, 2 * z + 2)
        cmpd(4, a1 == h1 == h2 == want, [5, 's1', z, a1, h1, h2])
        want = 2 if TAMPER != 'sb' else 1
        a1 = v(z + 1, z + 1, 2 * z + 1)
        h1 = vC(z + 1, z + 1, 2 * z + 1)
        h2 = vO(z + 1, z + 1, 2 * z + 1)
        cmpd(4, a1 == h1 == h2 == want, [5, 's2', z, a1, h1, h2])
        clear()
    for p in range(0, 9):
        for R in range(2, 11):
            want = 1 if TAMPER != 'sb' else 0
            a1 = v(1, p, R)
            h1 = vC(1, p, R)
            h2 = vO(1, p, R)
            cmpd(4, a1 == h1 == h2 == want, [5, 's3', p, R, a1, h1, h2])
        clear()

    # -------- D6: published anchors --------------------------------------
    # (a) K1285 T-PS0/1/2 slices = [g odd], m<=12, g<=15
    for (z, ks) in ((0, (1, 2, 3)), (1, (2, 3)), (2, (3, 4))):
        for m in range(1, 13):
            for g in range(1, 16):
                for k in ks:
                    h = pairX(z, k, m, g)
                    exp = tail(g) if TAMPER != 'ps' else flipC(tail(g))
                    cmpd(5, h == exp, [6, 'tps', z, k, m, g, h])
            clear()
    # (b) K1285 T-ALM six beds = 0
    for (dk, z) in ((2, 0), (3, 0), (2, 1), (3, 1), (3, 2), (4, 2)):
        for m in range(1, 13):
            R = 2 * m + dk
            h = H_canonical(R, (m, m), z)
            exp = 0 if TAMPER != 'ps' else 1
            cmpd(5, h == exp, [6, 'alm', dk, z, m, h])
    # (c) K1286 rows: Z1(1,·) z1-k1 / z2-k1 [g odd] / Z2(2,·) z2-k2
    for (z, k) in ((1, 1), (2, 1), (2, 2)):
        for m in range(1, 13):
            for g in range(1, 16):
                h = pairX(z, k, m, g)
                if (z == 2 and k == 1):
                    exp = tail(g)          # K1286 C4 clean row
                elif k == z:
                    exp = zdiag(g, z)      # diagonal
                else:
                    exp = tail(g)          # K1286 Z1(1,·) is the diagonal
                if TAMPER == 'ps':
                    exp = flipC(exp)
                cmpd(5, h == exp, [6, 'k1286', z, k, m, g, h, exp])
            clear()
    # (c') K1286 beds: b1(1)=0, b2(1)=2, b2(2)=0; K1286 T-B0 f0 rows
    for m in range(1, 11):
        h = H_canonical(2 * m + 1, (m, m), 1)
        cmpd(5, h == (0 if TAMPER != 'ps' else 1), [6, 'b11', m, h])
        h = H_canonical(2 * m + 1, (m, m), 2)
        cmpd(5, h == (2 if TAMPER != 'ps' else 1), [6, 'b21', m, h])
        h = H_canonical(2 * m + 2, (m, m), 2)
        cmpd(5, h == (0 if TAMPER != 'ps' else 1), [6, 'b22', m, h])
        for j in (-3, -2, -1, 0):
            R = 2 * m + j
            if R < 0:
                continue   # published T-B0 domain requires 2m+j >= 0
            want = (2 if j == 1 else (IND(j % 2 == 1) if j <= 0
                                      else IND(j % 2 == 0)))
            if TAMPER == 'ps':
                want = flipC(want)
            h = H_canonical(R, (m, m), 0)
            cmpd(5, h == want, [6, 'b0', m, j, h, want])
        clear()

    # -------- D7: plane-closure census z in {0,1,2}, k=1..8 -------------
    for z in (0, 1, 2):
        for m in range(1, 7):
            for g in range(1, 11):
                for k in range(1, 9):
                    if z == 2 and k == 1:
                        pred = tail(g)   # K1286 C4
                    elif k == z:
                        pred = zdiag(g, z)
                    elif k >= z + 1:
                        pred = tail(g)
                    else:
                        if z != 0:
                            continue
                        pred = tail(g)   # unreachable: z=0 has no window
                    h = pairX(z, k, m, g)
                    cmpd(6, h == pred, [7, z, k, m, g, h, pred])
            clear()

    # -------- D8: C-SUM census boxes (CONJECTURE, labeled) --------------
    for a in range(1, 9):
        for b in range(a + 1, 9):
            for c in range(b + 1, 9):
                S = a + b + c
                for z in range(0, 6):
                    for k in range(z + 2, z + 6):
                        h = H_canonical(S + k, (a, b, c), z)
                        exp = S % 2 if TAMPER != 'cs' else flipC(S % 2)
                        cmpd(7, h == exp, [8, 'tri', a, b, c, z, k, h])
                    clear()
    for a in range(1, 8):
        for b in range(a + 1, 8):
            for (x, y, w) in ((a, a, b), (a, b, b)):
                S = x + y + w
                for z in range(0, 5):
                    for k in range(z + 2, z + 6):
                        h = H_canonical(S + k, (x, y, w), z)
                        exp = S % 2 if TAMPER != 'cs' else flipC(S % 2)
                        cmpd(7, h == exp, [8, 'mix', x, y, w, z, k, h])
                    clear()
    for a in range(1, 7):
        for b in range(a + 1, 7):
            for c in range(b + 1, 7):
                for d in range(c + 1, 7):
                    S = a + b + c + d
                    for z in range(0, 3):
                        for k in range(z + 3, z + 7):
                            h = H_canonical(S + k, (a, b, c, d), z)
                            exp = S % 2 if TAMPER != 'cs' else flipC(S % 2)
                            cmpd(7, h == exp, [8, 'quad', a, b, c, d, z, k, h])
                        clear()

    # -------- D9: REFUTED refutation recheck -----------------------------
    counters = []
    clean_by_z = {}
    for z in range(3, 9):
        mz = 0
        for m in range(1, 4):
            for g in range(1, 13):
                for k in range(1, z):
                    if (k % 2) == (z % 2):
                        continue
                    e = pairX(z, k, m, g)
                    if e != tail(g):
                        mz += 1
                        counters.append([z, k, m, g, e, tail(g)])
            clear()
        clean_by_z[z] = mz
        if TAMPER == 'rw':
            cmpd(8, False, [9, z, mz])   # forced fail for the mutation device
        else:
            cmpd(8, (mz > 0) == (z >= 4), [9, z, mz])
    obs['refuted_alternation'] = {
        'claim': 'REFUTED: window rows k not congruent z (mod 2) having '
                 'the tail value [g odd] FAILS; recheck expectation: '
                 'z=3 clean, z>=4 counters (census z3..8 m1..3 g1..12).',
        'mismatch_by_z': clean_by_z,
        'counters': counters}
    # congruent-row survival census (observation only)
    surv = 0
    survbad = 0
    for z in range(3, 14):
        for m in range(1, 4):
            for g in range(1, 13):
                for k in range(1, z):
                    if (k % 2) != (z % 2):
                        continue
                    e = pairX(z, k, m, g)
                    surv += 1
                    survbad += IND(e != zdiag(g, z))
            clear()
    obs['window_congruent_rows_follow_zdiag'] = {
        'claim': 'OBSERVATION only (unproved): rows k = z-2, z-4, ... in '
                 'the window agree with Z-DIAG(g,z); census z3..13, '
                 'm1..3, g1..12.',
        'points': surv, 'mismatches': survbad}

    # -------- D10: cross-engine canonical vs ordered ----------------------
    for z in (0, 3, 7, 12):
        for m in range(1, 7):
            for g in range(1, 10):
                for k in range(z + 1, z + 4):
                    R = 2 * m + g + k
                    X = tuple(sorted([m, m + g], reverse=True))
                    hc = H_canonical(R, X, z)
                    ho = H_ordered(R, X, z)
                    cmpd(9, hc == ho, [10, 'PD', z, m, g, k, hc, ho])
            clear()
    for z in (0, 4, 9):
        for m in range(1, 7):
            for g in range(1, 13):
                R = 2 * m + g + z
                X = tuple(sorted([m, m + g], reverse=True))
                hc = H_canonical(R, X, z)
                ho = H_ordered(R, X, z)
                cmpd(9, hc == ho, [10, 'ZD', z, m, g, hc, ho])
            clear()
    for z in (0, 5, 11):
        for a in range(1, 9):
            for k in range(z, z + 3):
                R = 2 * a + k
                hc = H_canonical(R, (a, a), z)
                ho = H_ordered(R, (a, a), z)
                cmpd(9, hc == ho, [10, 'BED', z, a, k, hc, ho])
            clear()
    for (a, b, c) in ((1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 5), (2, 4, 6),
                      (3, 4, 7), (1, 5, 7), (2, 5, 8), (4, 5, 6), (1, 6, 8),
                      (3, 5, 7), (2, 6, 7)):
        S = a + b + c
        for z in range(0, 5):
            for k in range(z + 2, z + 5):
                R = S + k
                X = (a, b, c)
                hc = H_canonical(R, X, z)
                ho = H_ordered(R, X, z)
                cmpd(9, hc == ho, [10, 'TRI', a, b, c, z, k, hc, ho])
            clear()

    # -------- D11: stress beyond the audit boxes -------------------------
    for z in (0, 4, 9):
        for m in range(13, 26):
            for g in range(1, 11):
                for k in range(z + 1, z + 3):
                    h = pairX(z, k, m, g)
                    cmpd(10, h == tail(g), [11, 'farm', z, m, g, k, h])
            clear()
    for z in (15, 17, 19, 21, 24):
        for m in range(1, 6):
            for g in range(1, 9):
                for k in range(z + 1, z + 3):
                    h = pairX(z, k, m, g)
                    cmpd(10, h == tail(g), [11, 'spot', z, m, g, k, h])
            clear()
        for a in range(1, 7):
            for k in range(z, z + 2):
                if z in (15, 19, 24):
                    h = H_canonical(2 * a + k, (a, a), z)
                    cmpd(10, h == 0, [11, 'spotb', z, a, k, h])
            clear()
    for z in (9, 11, 13):
        for m in range(1, 5):
            for g in range(1, 25):
                h = pairX(z, z, m, g)
                cmpd(10, h == zdiag(g, z), [11, 'zfar', z, m, g, h])
            clear()
    for x in range(21, 31):
        for p in range(1, 4):
            for j in range(p, p + 3):
                R = x + j
                cmpd(10, v(x, p, R) == vC(x, p, R) == vO(x, p, R) == x % 2,
                     [11, 'lsbf', x, p, j])
        clear()

    info = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['obs'] = obs
    res['battery_names'] = ['D1_tuh_census', 'D2_tdu_census', 'D3_zdiag_census',
                            'D4_typed_selfcheck', 'D5_lsb_both_engines',
                            'D6_published_anchors', 'D7_plane_closure',
                            'D8_csum_census', 'D9_refuted_recheck',
                            'D10_cross_engine', 'D11_stress']
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)


main()

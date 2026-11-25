#!/usr/bin/env python3
"""verify_k1314: machine audit for T-BB2, the SECOND below-band row
(k = z+n-4) of the n-mountain faces, together with its 4 base lemmas
(L-2, PB2, L-BR2, L-0), the K0832 3-token transient-band corollaries
(conjectures A/B/C at k=0), and the published-row anchors.

Theorems under audit (claims and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of
the hand proof pointwise; censuses are consistency checks and do NOT
replace the proofs; all quantifiers are UNBOUNDED):

  T-BB2 (universal): for every n >= 3, every z >= 0, every multiset X of
      n heaps (each >= 1) with S = sum(X), E := 2*max(X) - S (K1311
      convention) on the SECOND below-band row k := z+n-4 (R = S+k >= 2):
          E <= z+n-4   ->  H(S+k; X; z) = [E odd]        (region 1)
          E == z+n-3   ->  H(S+k; X; z) = 2             (2-line)
          E >= z+n-2   ->  H(S+k; X; z) = 1 - [E odd]   (region 3)
      with exactly two exception cells, both X = (1,1,1):
          z = 0 -> 0   and   z = 1 -> 2
      (for z >= 2 the generic region-1 law [E odd] = 1 applies again).
      In (E, w) coordinates, w := E+z+n-5, the value is a function of
      (E, w) merged across ALL n >= 3 on the whole census domain, with
      the ONLY multivalue cells (-1,-3) -> {0,1} and (-1,-2) -> {1,2},
      the second entry of each pair coming exactly from the (1,1,1)
      exception cells (frozen pre-declaration exploration WA).
  L-2 (universal, n=2, plane Z >= 1, row k = Z-2):
      beds (a,a):        2 iff (a,Z) = (1,1), else 0
      pairs (m+g,m), g>=1:
          Z <= g-2 -> [g even]; Z == g-1 -> 2; Z >= g -> [g odd]
  PB2 (universal, n=2, plane 0, wall row k = -2):
      gap g = a-b:  g <= 2 -> [g odd]; g == 3 -> 2; g >= 4 -> [g even]
  L-BR2 (base lemma, a slice of the published K0832 single-token closed
      form): for all x >= 1, Z >= 0 with row k = Z-3 (R = x+Z-3 >= 0):
          R == 0 -> 0;
          2 at (Z == x >= 2) or (1,3) or (3,1);
          Z >= x+1 -> [x odd]; Z <= x-1 -> [x even]
  L-0 (universal, empty multiset): identically 0 for all R, z.
  Typed child identities (engine-free): every option of a second-row
  cell is EXACTLY one of
    { A-a: unique-top reduce -> (n, z, k, E-1)  [claim row cell]
    , A-b: tied-top/tail reduce -> (n, z, k, E+1)
    , B:   1-heap removal -> (n-1, plane z+1, same k, E+1)
           n-1 = 1 heirs by L-BR2 (published K0832 slice),
           n-1 = 2 heirs by L-2 (plane z+1 >= 1) or PB2 (z+1 = 0 wall)
    , C:   z >= 1 plane-down -> option value 1 XOR claim(n, z-1, k-1, E) }
  and each child is again a second-row cell of its own face/plane, so a
  single strong induction on the budget R across ALL domains closes the
  whole packet (T-BB2 rows n>=3, L-2 planes Z>=1, PB2 wall, L-BR2, L-0).
  COROLLARIES (K0832 3-token transient band, k=0 odd slice R = 2x-1):
      conjecture A (j=0): X = (y+w+z, y, w) -> value 2 ALWAYS
          (E = z = the T-BB2 2-line; band condition x < R < S+z+2
           automatic; (1,1,1) unreachable) — RESOLVED by T-BB2.
      conjecture B (j=2): X = (y+w+z+2, y, w) -> value 2 ALWAYS
          (k = z+1 boundary row of the n=3 face, E = p+1: the published
           K1311 T-DB 2-line) — transcribed D8, applied D10.
      conjecture C (j=1): X = (y+w+z+1, y, w) -> value 2 iff z = 0,
          never 2 for z >= 1 (E = z+1 on the published K1313 T-BB top
          row k=z: u = 2z; u=0 -> 2; u>=1 -> [z+1 odd] != 2) — RESOLVED
          as a corollary of the published T-BB (K1313).
      The unified conjecture U (k >= 1 slices) lives on rows
      k = z-1-2k <= z+n-5 and remains OPEN (O-BBL3, unchanged).

Batteries (counts and bad counts are printed as JSON on stdout):
  D1  T-BB2 census n=3 (heaps<=8, z<=11, negative E included)
  D2  census n=4 (heaps<=6, z<=10) + n=5 (heaps<=5, z<=9)
  D3  census n=6 (heaps<=5, z<=8) + n=7 (heaps<=4, z<=8)
  D4  exception + interface families census: (1^n) n=3..7 z<=40,
      (2,1,1) z<=40, (a,1,1) and (a,a,1) a<=12 z<=30
  D5  typed-children closure: children built ONLY from the claim tables,
      mex == claim == engine (rows n=2..6, z<=8)
  D6  L-2 census (pairs m<=11 g<=14 Z<=14, beds a<=13 Z<=14)
  D7  PB2 census (a,b<=20) + L-BR2 census (x<=29, Z<=19, claim ==
      engine == published K0832 closed form) + L-0 census (R,z<=7)
  D8  published anchors byte-faithful: T-BB (K1313) rows n=2..3,
      T-DB (K1311) boundary slice, T-CSUM (K1312) tail slice,
      K0832 single-token closed-form replication sweep
  D9  cross-engine (canonical vs ordered vs claim)
  D10 WA watershed reproduction: merged (E,w) collapse on n=3..6 census,
      the only multivalue cells are exactly (-1,-3)->{0,1},(-1,-2)->{1,2}
      (frozen pre-declaration exploration outcome)
  D11 corollary A/B/C sweep (K0832 3-token transient band, k=0)
  D12 two-layer adjacency: published top row (K1313 T-BB) + second row
      (T-BB2) swept simultaneously n=3..5
  D13 deep-negative-E families (a^n), (a+1,a^{n-1}), n=3..5, a<=8, z<=40
  D14 seeded random sweep (seed 1314)

TAMPER modes: --tamper-engine (rc 2, mutated block sha), --tamper=
ty|d2|d3|ex|tt|l2|pb|ps|ce|wa|ab|db|zz|rs (flip exactly one battery's
expectation; all rc 1 with the exact pre-declared bad counts).
Determinism: official runs byte-identical on stdout.
"""
import json, hashlib, sys, time, random
from functools import lru_cache
from itertools import combinations_with_replacement

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

TAMPER = None
for a in sys.argv[1:]:
    if a.startswith('--tamper='):
        TAMPER = a.split('=', 1)[1]


def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()


# ---- published K1311/K1308 Z-DIAG 3-branch law (transcription) ----------
def Dlaw(g, p):
    if g <= p:
        return 1 if g % 2 == 1 else 0
    if g == p + 1:
        return 2
    return 1 if g % 2 == 0 else 0


# ---- published K1313 T-BB top-row law (transcription) --------------------
def TBB1(n, E, z):
    """Published T-BB: value on the top below-band row k = z+n-3."""
    u = E + z + n - 4
    if u >= 1:
        return E % 2
    if u == 0:
        return 2
    return 1 - (E % 2)


# ---- the claims under audit -----------------------------------------------
def TB2(Xd, z):
    """T-BB2 claim: second below-band row k = z+n-4, n >= 3."""
    n = len(Xd)
    assert n >= 3
    if Xd == (1, 1, 1) and z in (0, 1):
        return 0 if z == 0 else 2
    E = 2 * Xd[0] - sum(Xd)
    if E <= z + n - 4:
        return E % 2
    if E == z + n - 3:
        return 2
    return 1 - (E % 2)


def L2(Xd, Z):
    """L-2 claim: n=2, plane Z >= 1, row k = Z-2."""
    a, b = Xd
    g = a - b
    if g == 0:
        return 2 if (a, Z) == (1, 1) else 0
    if Z <= g - 2:
        return 1 if g % 2 == 0 else 0
    if Z == g - 1:
        return 2
    return g % 2


def PB2(Xd):
    """PB2 claim: n=2, plane 0, wall row k = -2."""
    g = Xd[0] - Xd[1]
    if g <= 2:
        return g % 2
    if g == 3:
        return 2
    return 1 if g % 2 == 0 else 0


def LBR2(x, Z):
    """L-BR2 claim: n=1, plane Z >= 0, row k = Z-3 (R = x+Z-3)."""
    R = x + Z - 3
    if R == 0:
        return 0
    if Z == x and x >= 2:
        return 2
    if (x, Z) == (1, 3) or (x, Z) == (3, 1):
        return 2
    if Z >= x + 1:
        return x % 2
    return 1 if x % 2 == 0 else 0


def claim(Xd, z):
    """Dispatch the second-row claim system by heap count."""
    n = len(Xd)
    if n == 0:
        return 0
    if n == 1:
        return LBR2(Xd[0], z)
    if n == 2:
        return PB2(Xd) if z == 0 else L2(Xd, z)
    return TB2(Xd, z)


def flipC(val):
    return 1 - val if val in (0, 1) else 1


def E_of(Xd):
    return 2 * Xd[0] - sum(Xd)


def mexs(vals):
    s = set(vals)
    x = 0
    while x in s:
        x += 1
    return x


def typed_kids(Xd, z):
    """Option VALUES of a second-row cell from the claim tables ONLY.

    A-reduce children stay (n, z, same k) — second row of the same face
    for n>=3 / same-plane second row for n=2; B-children move to
    (n-1, plane z+1, same k) — L-BR2 cells for n-1=1 (row k = (z+1)-3
    when k = z-2, wall rows handled by R=0), L-2/PB2 cells for n-1=2,
    T-BB2 cells for n-1>=3; C-children move to (n, plane z-1, k-1)."""
    n = len(Xd)
    k = z + n - 4 if n >= 3 else z - 2 if z >= 1 else -2
    R = sum(Xd) + k
    if R == 0:
        return []          # terminal cell (only PB2 (1,1)): no options
    kids = []
    for i, v in enumerate(Xd):
        if v > 1:
            kid = tuple(sorted(Xd[:i] + (v - 1,) + Xd[i + 1:], reverse=True))
            kids.append(claim(kid, z))
        else:
            kid = tuple(sorted(Xd[:i] + Xd[i + 1:], reverse=True))
            if len(kid) == 1:
                # single token, plane z+1, budget R-1, row k = (z+1)-3
                assert k == z - 2, (Xd, z, k)
                kids.append(LBR2(kid[0], z + 1))
            else:
                kids.append(claim(kid, z + 1))
    if z >= 1:
        kids.append(1 ^ claim(Xd, z - 1))
    return kids


def multisets(n, hi):
    return list(combinations_with_replacement(range(1, hi + 1), n))


def main():
    t0 = time.time()
    res = {'kit': 'verify_k1314', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS', 'tamper': TAMPER}
    ND = 14
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

    # -------- D1: T-BB2 census n=3 (negative E included) ------------------
    sys.stderr.write('D1\n'); sys.stderr.flush()
    for z in range(0, 12):
        for X in multisets(3, 8):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            exp = TB2(Xd, z)
            if TAMPER == 'ty':
                exp = flipC(exp)
            h = H_canonical(S + z - 1, Xd, z)
            cmpd(0, h == exp, [1, z, Xd, E_of(Xd), h, exp])
        clear()

    # -------- D2: census n=4 + n=5 ----------------------------------------
    sys.stderr.write('D2\n'); sys.stderr.flush()
    for z in range(0, 11):
        for X in multisets(4, 6):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            exp = TB2(Xd, z)
            if TAMPER == 'd2':
                exp = flipC(exp)
            h = H_canonical(S + z, Xd, z)
            cmpd(1, h == exp, [2, 4, z, Xd, E_of(Xd), h, exp])
        clear()
    for z in range(0, 10):
        for X in multisets(5, 5):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            exp = TB2(Xd, z)
            if TAMPER == 'd2':
                exp = flipC(exp)
            h = H_canonical(S + z + 1, Xd, z)
            cmpd(1, h == exp, [2, 5, z, Xd, E_of(Xd), h, exp])
        clear()

    # -------- D3: census n=6 + n=7 ----------------------------------------
    sys.stderr.write('D3\n'); sys.stderr.flush()
    for z in range(0, 9):
        for X in multisets(6, 5):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            exp = TB2(Xd, z)
            if TAMPER == 'd3':
                exp = flipC(exp)
            h = H_canonical(S + z + 2, Xd, z)
            cmpd(2, h == exp, [3, 6, z, Xd, E_of(Xd), h, exp])
        clear()
    for z in range(0, 9):
        for X in multisets(7, 4):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            exp = TB2(Xd, z)
            if TAMPER == 'd3':
                exp = flipC(exp)
            h = H_canonical(S + z + 3, Xd, z)
            cmpd(2, h == exp, [3, 7, z, Xd, E_of(Xd), h, exp])
        clear()

    # -------- D4: exception + interface families --------------------------
    sys.stderr.write('D4\n'); sys.stderr.flush()
    # (a) all-ones families (1^n), n = 3..7, z = 0..40
    for n in range(3, 8):
        Xd = (1,) * n
        S = n
        for z in range(0, 41):
            exp = TB2(Xd, z)
            if TAMPER == 'ex':
                exp = flipC(exp)
            h = H_canonical(S + z + n - 4, Xd, z)
            cmpd(3, h == exp, [4, 'ones', n, z, h, exp])
        clear()
    # (b) (2,1,1) z = 0..40
    for z in range(0, 41):
        Xd = (2, 1, 1)
        exp = TB2(Xd, z)
        if TAMPER == 'ex':
            exp = flipC(exp)
        h = H_canonical(4 + z - 1, Xd, z)
        cmpd(3, h == exp, [4, '211', z, h, exp])
        clear()
    # (c) (a,1,1) and (a,a,1), a = 2..12, z = 0..30
    for a in range(2, 13):
        for Xd in ((a, 1, 1), (a, a, 1)):
            S = sum(Xd)
            for z in range(0, 31):
                exp = TB2(Xd, z)
                if TAMPER == 'ex':
                    exp = flipC(exp)
                h = H_canonical(S + z - 1, Xd, z)
                cmpd(3, h == exp, [4, Xd[1] == 1 and 'a11' or 'aa1',
                                   a, z, h, exp])
            clear()

    # -------- D5: typed self-check ----------------------------------------
    sys.stderr.write('D5\n'); sys.stderr.flush()
    for n in (2, 3, 4, 5, 6):
        hi = {2: 9, 3: 8, 4: 6, 5: 5, 6: 4}[n]
        for z in range(0, 9):
            for X in combinations_with_replacement(range(1, hi + 1), n):
                if sum(X) > 30:
                    continue
                Xd = tuple(sorted(X, reverse=True))
                S = sum(X)
                k = z + n - 4 if n >= 3 else (z - 2 if z >= 1 else -2)
                exp = claim(Xd, z)
                if TAMPER == 'tt':
                    exp = flipC(exp)
                kids = typed_kids(Xd, z)
                assert kids is not None
                mx = mexs(kids)
                h = H_canonical(S + k, Xd, z)
                cmpd(4, (mx == exp) and (h == exp),
                     [5, n, z, Xd, k, mx, exp, h, kids])
            clear()

    # -------- D6: L-2 census ----------------------------------------------
    sys.stderr.write('D6\n'); sys.stderr.flush()
    for g in range(1, 15):
        for m in range(1, 12):
            for Z in range(1, 15):
                Xd = (m + g, m)
                exp = L2(Xd, Z)
                if TAMPER == 'l2':
                    exp = flipC(exp)
                h = H_canonical(2 * m + g + Z - 2, Xd, Z)
                cmpd(5, h == exp, [6, 'pair', m, g, Z, h, exp])
    for a in range(1, 14):
        for Z in range(1, 15):
            Xd = (a, a)
            exp = L2(Xd, Z)
            if TAMPER == 'l2':
                exp = flipC(exp)
            h = H_canonical(2 * a + Z - 2, Xd, Z)
            cmpd(5, h == exp, [6, 'bed', a, Z, h, exp])
    clear()

    # -------- D7: PB2 + L-BR2 + L-0 censuses ------------------------------
    sys.stderr.write('D7\n'); sys.stderr.flush()
    for a in range(1, 21):
        for b in range(1, a + 1):
            Xd = (a, b)
            exp = PB2(Xd)
            if TAMPER == 'pb':
                exp = flipC(exp)
            h = H_canonical(a + b - 2, Xd, 0)
            cmpd(6, h == exp, [7, 'pb2', a, b, h, exp])
    clear()
    for x in range(1, 30):
        for Z in range(0, 20):
            R = x + Z - 3
            if R < 0:
                continue
            exp = LBR2(x, Z)
            if TAMPER == 'pb':
                exp = flipC(exp)
            st = single_token(x, Z, R)
            h1 = vC(x, Z, R)
            h2 = vO(x, Z, R)
            cmpd(6, exp == h1 == h2 == st,
                 [7, 'lbr2', x, Z, R, exp, h1, h2, st])
        clear()
    for R in range(0, 8):
        for z in range(0, 8):
            exp = 0
            if TAMPER == 'pb':
                exp = 1
            v = H_canonical(R, (), z) if R > 0 else 0
            cmpd(6, v == exp, [7, 'l0', R, z, v, exp])
    clear()

    # -------- D8: published anchors ---------------------------------------
    sys.stderr.write('D8\n'); sys.stderr.flush()
    # (a) published T-BB (K1313) top row k = z+n-3, n = 3
    for z in range(0, 9):
        for X in multisets(3, 6):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            E = E_of(Xd)
            exp = TBB1(3, E, z)
            if TAMPER == 'ps':
                exp = flipC(exp)
            h = H_canonical(S + z, Xd, z)
            cmpd(7, h == exp, [8, 'tbb', 3, z, Xd, h, exp])
        clear()
    # (b) published T-BB n=2 slice: beds + NCW-P + wall row z=0..12
    for z in range(0, 13):
        for a in range(1, 9):
            for g in range(0, 17):
                Xd = (a + g, a)
                if a + g > 24:
                    continue
                S = sum(Xd)
                exp = TBB1(2, g, z)
                if TAMPER == 'ps':
                    exp = flipC(exp)
                h = H_canonical(S + z - 1 if z >= 1 else S - 1, Xd, z)
                cmpd(7, h == exp, [8, 'tbb2', z, a, g, h, exp])
        clear()
    # (c) published T-DB (K1311) boundary slice k = z+n-2, n = 3
    for z in range(0, 9):
        for X in multisets(3, 6):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            E = E_of(Xd)
            exp = Dlaw(E, z + 1)
            if TAMPER == 'ps':
                exp = (exp + 1) % 3
            h = H_canonical(S + z + 1, Xd, z)
            cmpd(7, h == exp, [8, 'tdb', 3, z, Xd, E, h, exp])
        clear()
    # (d) published K1312 tail [S mod 2] slice, k = z+n-1 and z+n, n = 3
    for z in range(0, 5):
        for X in multisets(3, 5):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            for k in (z + 2, z + 3):
                exp = S % 2
                if TAMPER == 'ps':
                    exp = flipC(exp)
                h = H_canonical(S + k, Xd, z)
                cmpd(7, h == exp, [8, 'tail', 3, z, Xd, k, h, exp])
        clear()
    # (e) published K0832 single-token closed-form replication sweep
    for x in range(1, 16):
        for z in range(0, 13):
            for R in range(0, x + z + 6):
                exp = single_token(x, z, R)
                if TAMPER == 'ps':
                    exp = flipC(exp) if exp in (0, 1) else (exp % 2)
                h1 = vC(x, z, R)
                h2 = vO(x, z, R)
                cmpd(7, h1 == h2 == exp, [8, 'rep', x, z, R, h1, h2, exp])
            clear()

    # -------- D9: cross-engine --------------------------------------------
    sys.stderr.write('D9\n'); sys.stderr.flush()
    for (n, hi, zs) in ((2, 8, (0, 5, 10)), (3, 6, (0, 3, 7, 11)),
                        (4, 5, (0, 4, 9))):
        for z in zs:
            for X in multisets(n, hi):
                if sum(X) > 28:
                    continue
                S = sum(X)
                Xd = tuple(sorted(X, reverse=True))
                k = z + n - 4 if n >= 3 else (z - 2 if z >= 1 else -2)
                exp = claim(Xd, z)
                if TAMPER == 'ce':
                    exp = flipC(exp)
                hc = H_canonical(S + k, Xd, z)
                ho = H_ordered(S + k, Xd, z)
                cmpd(8, hc == ho == exp, [9, n, z, Xd, k, hc, ho, exp])
            clear()

    # -------- D10: WA watershed reproduction ------------------------------
    sys.stderr.write('D10\n'); sys.stderr.flush()
    amb = {}
    for (n, hi, zmax) in ((3, 9, 12), (4, 7, 11), (5, 6, 10), (6, 5, 9)):
        for X in multisets(n, hi):
            Xd = tuple(sorted(X, reverse=True))
            S = sum(Xd)
            E = E_of(Xd)
            for z in range(0, zmax + 1):
                k = z + n - 4
                if S + k < 0:
                    continue
                w = E + z + n - 5
                v = H_canonical(S + k, Xd, z)
                amb.setdefault((E, w), set()).add(v)
                exp = TB2(Xd, z)
                if TAMPER == 'wa':
                    exp = flipC(exp)
                cmpd(9, v == exp, [10, n, z, Xd, E, w, v, exp])
        clear()
    multi = {f'{kk[0]},{kk[1]}': sorted(vv)
             for kk, vv in sorted(amb.items()) if len(vv) > 1}
    exp_multi = {'-1,-3': [0, 1], '-1,-2': [1, 2]}
    ok_multi = (multi == exp_multi)
    obs['wa_multivalue_cells'] = multi
    if TAMPER == 'wa' and ok_multi:
        ok_multi = False   # claim flips already bad; force the observer
    cmpd(9, ok_multi, [10, 'multivalue', multi])

    # -------- D11: corollary A/B/C sweep ------------------------------------
    sys.stderr.write('D11\n'); sys.stderr.flush()
    for y in range(1, 11):
        for w in range(1, y + 1):
            for z in range(0, 13):
                # conjecture A: X = (y+w+z, y, w), j=0, k=0 slice R=2x-1
                x = y + w + z
                Xd = (x, y, w)
                S = sum(Xd)
                R = 2 * x - 1
                assert x < R < S + z + 2, (y, w, z)
                exp = 2
                if TAMPER == 'ab':
                    exp = 0
                h = H_canonical(R, Xd, z)
                cmpd(10, h == exp, [11, 'A', y, w, z, h, exp])
                # conjecture B: x = y+w+z+2 -> boundary row k = z+1
                x2 = y + w + z + 2
                Xd2 = (x2, y, w)
                S2 = sum(Xd2)
                R2 = 2 * x2 - 1
                assert x2 < R2 < S2 + z + 2, (y, w, z)
                exp2 = Dlaw(E_of(Xd2), z + 1)
                if TAMPER == 'ab':
                    exp2 = 0
                h2v = H_canonical(R2, Xd2, z)
                cmpd(10, h2v == exp2 == 2, [11, 'B', y, w, z, h2v, exp2])
                # conjecture C: x = y+w+z+1 -> top row k = z (K1313 T-BB)
                x1 = y + w + z + 1
                Xd1 = (x1, y, w)
                S1 = sum(Xd1)
                R1 = 2 * x1 - 1
                assert x1 < R1 < S1 + z + 2, (y, w, z)
                exp1 = 2 if z == 0 else (z + 1) % 2
                if TAMPER == 'ab':
                    exp1 = flipC(exp1)
                h1v = H_canonical(R1, Xd1, z)
                cmpd(10, h1v == exp1 and (z == 0 or h1v != 2),
                     [11, 'C', y, w, z, h1v, exp1])
        clear()

    # -------- D12: two-layer adjacency --------------------------------------
    sys.stderr.write('D12\n'); sys.stderr.flush()
    for n in (3, 4, 5):
        hi = {3: 6, 4: 5, 5: 4}[n]
        for z in range(0, 8):
            for X in multisets(n, hi):
                if sum(X) > 26:
                    continue
                S = sum(X)
                Xd = tuple(sorted(X, reverse=True))
                E = E_of(Xd)
                expB = TBB1(n, E, z)
                if TAMPER == 'db':
                    expB = flipC(expB)
                hB = H_canonical(S + z + n - 3, Xd, z)
                cmpd(11, hB == expB, [12, n, z, Xd, 'top', hB, expB])
                expT = TB2(Xd, z)
                if TAMPER == 'db':
                    expT = flipC(expT)
                hT = H_canonical(S + z + n - 4, Xd, z)
                cmpd(11, hT == expT, [12, n, z, Xd, 'row2', hT, expT])
            clear()

    # -------- D13: deep-negative-E -----------------------------------------
    sys.stderr.write('D13\n'); sys.stderr.flush()
    for n in (3, 4, 5):
        for a in range(1, 9):
            Xe = tuple(sorted([a] * n, reverse=True))
            Xn = tuple(sorted([a + 1] + [a] * (n - 1), reverse=True))
            for X in (Xe, Xn):
                for z in range(0, 41):
                    S = sum(X)
                    exp = TB2(X, z)
                    if TAMPER == 'zz':
                        exp = flipC(exp)
                    h = H_canonical(S + z + n - 4, X, z)
                    cmpd(12, h == exp, [13, n, a, z, E_of(X), h, exp])
                clear()

    # -------- D14: seeded random sweep -------------------------------------
    sys.stderr.write('D14\n'); sys.stderr.flush()
    rng = random.Random(1314)
    for _ in range(700):
        n = rng.randint(2, 7)
        z = rng.randint(0, 10)
        maxh = {2: 14, 3: 12, 4: 10, 5: 9, 6: 7, 7: 6}[n]
        heaps = []
        for _i in range(n):
            heaps.append(rng.randint(1, maxh))
        Xd = tuple(sorted(heaps, reverse=True))
        S = sum(Xd)
        k = z + n - 4 if n >= 3 else (z - 2 if z >= 1 else -2)
        exp = claim(Xd, z)
        if TAMPER == 'rs':
            exp = flipC(exp)
        h = H_canonical(S + k, Xd, z)
        cmpd(13, h == exp, [14, n, z, Xd, E_of(Xd), h, exp])
        if _ % 25 == 24:
            clear()
    clear()

    info = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['obs'] = obs
    res['battery_names'] = ['D1_census_n3', 'D2_census_n45',
                            'D3_census_n67', 'D4_exception_families',
                            'D5_typed_selfcheck', 'D6_l2_census',
                            'D7_pb2_lbr2_l0', 'D8_published_anchors',
                            'D9_cross_engine', 'D10_wa_watershed',
                            'D11_corollary_ABC', 'D12_two_layer',
                            'D13_deep_negE', 'D14_random_sweep']
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)


main()

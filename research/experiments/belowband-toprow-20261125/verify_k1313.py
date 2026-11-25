#!/usr/bin/env python3
"""verify_k1313: machine audit for T-BB, the TOP ROW of the BELOW BAND
(k = z+n-3) of every n-mountain face, ALL token multiplicities n >= 2.

Theorems under audit (claims and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of
the hand proof pointwise; censuses are consistency checks and do NOT
replace the proofs; all quantifiers are UNBOUNDED):

  T-BB (universal): for every n >= 2, every z >= 0, every multiset X of
      n heaps (each >= 1) with S = sum(X), E := 2*max(X) - S (K1311
      convention) on the row k := z+n-3 (R = S+k; for n=2, z=0 this is
      the wall row k=-1):
          u := E + z + n - 4
          H(S+k; X; z) = [E odd]    if u >= 1
                       = 2          if u == 0
                       = 1 - [E odd] if u <= -1
      The value depends on the single coordinate pair (E, z) ONLY (not
      on the individual heaps) — the below-band counterpart of the
      published K1311 boundary-row collapse T-DB. E is unbounded below
      for n >= 3 (e.g. X = (a,a,a): E = -a), so the 2-line E+z = 4-n
      and the flip region E+z <= 3-n are infinite. For n=2 the domain
      E >= 0 truncates them to six exceptional cells, reproducing the
      published K1310 T-NCW-B bed constants (z>=3 -> 0, z=2 -> 2,
      z=1 -> 1) and the T-NCW-P g*<=0 branch ([g odd]) as corollaries.
      This RESOLVES the open O-BBL top layer registered in K1311
      (SS5)/K1312 (SS5): with the published boundary law T-DB
      (k = z+n-2), the tail law T-CSUM (k >= z+n-1, K1312) and this
      row, every n-mountain face is closed for all k >= z+n-3; the
      only remaining open layer per n >= 3 becomes k <= z+n-4.
      The OBS-BBL "watershed" frozen observation of K1311 (naive-law
      mismatch counts collapsing (80,80,68)->(80,0,0) on the triples
      k=z row, z=1..7) is REPRODUCED in D9 and explained: the naive
      comparisons miss exactly the transient/flip cells, and T-BB
      matches the engine with bad 0 on that whole domain.
  L-BR1 (base, derived from the published K0832 single-token closed
      form): for all x >= 1, Z >= 1: v(x, Z, x+Z-2) = PB1(x, Z) with
      t := x+Z-3: t >= 1 -> [x odd]; t = 0 -> 2; t <= -1 -> 1-[x odd].
      Used by the proof for the B-heirs of n=2 (single tokens at
      plane Z=z+1 >= 1, row k=Z-2).
  Typed child identities (engine-free): every option of a row cell
      (n >= 2, k = z+n-3) is EXACTLY one of
        { A-a: unique-top reduce  -> (n, z, k, E-1)
        , A-b: tied-top/tail reduce -> (n, z, k, E+1)
        , B:    1-heap removal  -> (n-1, z+1, k, E+1), n-1 = 1 heirs
               evaluated by the published K0832 closed form
        , C:    z >= 1 plane-down -> option value 1 XOR PB(n, E, z-1)
               (child row k-1, same E) }
      and each child is again a row cell of its own face, so T-BB +
      L-BR1 close by a SINGLE strong induction on R (all children at
      budget R-1). D5 machine-checks mex(children) == claim == engine
      pointwise with children built ONLY from the claim tables.

Batteries (counts and the mutation table declared in the single-owner
note; expected overall_bad == 0; stdout deterministic byte-identical,
volatile info on stderr only):

  D1  T-BB census n=3: full multisets heaps<=8, z<=11, negative E incl.
  D2  census n=4 (heaps<=6, z<=10) + n=5 (heaps<=5, z<=9).
  D3  census n=6 (heaps<=5, z<=8) + n=7 (heaps<=4, z<=8).
  D4  census n=2: rows k=z-1 (z>=1) AND the wall row (z=0, k=-1): all
      (a+g, a), a<=8, g<=16, z<=12.
  D5  typed self-check n=2..6, z<=8: children built ONLY from the claim
      tables (PB + published single-token closed form for n=1 heirs),
      mex == claim == engine.
  D6  base lemma L-BR1 (x<=20, Z=1..15, both engines + published closed
      form) and single-token closed-form replication sweep (x<=15,
      z<=12, all R <= x+z+5, both engines).
  D7  published anchors (byte-faithful transcriptions): T-DB boundary
      law D(E,k) at k=z+n-2 (n=2..4), the published K1310 T-NCW-B bed
      constants on k=z-1 rows (z=1 -> 1, z=2 -> 2, z>=3 -> 0), the
      published K1310 T-NCW-P g*<=0 branch at k=z-1, z>=2 (value
      [g odd]), and the published K1312 tail row [S mod 2] at
      k=z+n-1, z+n (connection box).
  D8  cross-engine canonical vs ordered AND claim (sampled n=2..4).
  D9  OBS-BBL watershed reproduction: triples k=z row, heaps<=8,
      S<=15, z=1..7 — frozen naive mismatch pairs of K1311 (D11 table)
      reproduced + PB bad 0 on the same domain.
  D10 deep-negative-E families: all-equal (a^n) and near-equal
      (a+1, a^(n-1)) rows, n=3..5, a<=8, z<=40 (probes the u>=1 region
      far below E=2-n and the deep 2-line/flip tails).
  D11 T-DB adjacency: boundary row k=z+n-2 (published D law) and top
      below row k=z+n-3 (T-BB) evaluated side by side (n=2..4) — the
      two-layer interface.
  D12 seeded random multiset sweep (seed 1313, n=2..7, z=0..10,
      heaps<=20).

TAMPER modes: --tamper-engine (rc 2, mutated block sha), --tamper=
ty|h2|in|wl|tt|lm|ps|ce|ob|db|zz|rs (flip exactly one battery's
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


# ---- published K1308/K1311 Z-DIAG 3-branch law (transcription) ----------
def Dlaw(g, p):
    if g <= p:
        return 1 if g % 2 == 1 else 0
    if g == p + 1:
        return 2
    return 1 if g % 2 == 0 else 0


# ---- the claim under audit ----------------------------------------------
def PB(n, E, z):
    """T-BB claim (mutation hooks are applied at battery level)."""
    u = E + z + n - 4
    if u >= 1:
        return E % 2
    if u == 0:
        return 2
    return 1 - (E % 2)


def PB1(x, Z):
    """L-BR1 claim."""
    t = x + Z - 3
    if t >= 1:
        return x % 2
    if t == 0:
        return 2
    return 1 - (x % 2)


def flipC(val):
    return 1 - val if val in (0, 1) else 1


def E_of(X):
    return 2 * X[0] - sum(X)


def mexs(vals):
    s = set(vals)
    x = 0
    while x in s:
        x += 1
    return x


def typed_kids(Xd, z, k):
    """Option VALUES of a row cell (n>=2) from the claim tables ONLY:
    T-BB for multi-token heirs + the published K0832 closed form for
    the single-token heirs of n=2 B-exits."""
    n = len(Xd)
    R = sum(Xd) + k
    kids = []
    tied = (Xd[1] == Xd[0])
    for i, v in enumerate(Xd):
        if v > 1:
            kid = tuple(sorted(Xd[:i] + (v - 1,) + Xd[i + 1:], reverse=True))
            # every A-reduce child is a row cell of the same face
            # (unique-top: E-1, tied/tail: E+1 — one claim lookup each)
            kids.append(PB(n, E_of(kid), z))
        else:
            kid = tuple(sorted(Xd[:i] + Xd[i + 1:], reverse=True))
            if len(kid) == 1:
                # B-heir single token at plane z+1, budget R-1 (k same,
                # row of the n=1 hierarchy): published closed form.
                kids.append(single_token(kid[0], z + 1, R - 1))
            else:
                # B-heir (n-1, plane z+1, same k): its own row
                assert k == (z + 1) + (n - 1) - 3
                kids.append(PB(n - 1, E_of(kid), z + 1))
    if z >= 1:
        # C-heir: (n, z-1, k-1, same E)
        kids.append(1 ^ PB(n, E_of(Xd), z - 1))
    return kids


def multisets(n, hi):
    return list(combinations_with_replacement(range(1, hi + 1), n))


# ---- frozen pre-declaration data (explore_k1313.py/.out 正本) ------------
# K1311 OBS-BBL frozen naive mismatch counts on the triples k=z row
# (heaps<=8, S<=15, 80 cells per z): [z, total, bad_D(E,z-1), bad_D(E,z)].
OBS_BBL = [[1, 80, 80, 68], [2, 80, 56, 47], [3, 80, 31, 25],
           [4, 80, 16, 12], [5, 80, 6, 4], [6, 80, 2, 1], [7, 80, 0, 0]]


def main():
    t0 = time.time()
    res = {'kit': 'verify_k1313', 'engine_sha': ENGINE_SHA,
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

    # -------- D1: T-BB census n=3 (negative E included) ------------------
    sys.stderr.write('D1\n'); sys.stderr.flush()
    for z in range(0, 12):
        for X in multisets(3, 8):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            E = E_of(Xd)
            exp = PB(3, E, z)
            if TAMPER == 'ty':
                exp = flipC(exp)
            if TAMPER == 'h2' and E + z == 1:
                exp = 0        # hypotenuse cells only
            if TAMPER == 'in' and E + z <= 0:
                exp = flipC(exp)
            h = H_canonical(S + z, Xd, z)
            cmpd(0, h == exp, [1, z, Xd, E, h, exp])
        clear()

    # -------- D2: census n=4 + n=5
    sys.stderr.write('D2\n'); sys.stderr.flush()
    for z in range(0, 11):
        for X in multisets(4, 6):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            E = E_of(Xd)
            exp = PB(4, E, z)
            if TAMPER == 'ty':
                exp = flipC(exp)
            h = H_canonical(S + z + 1, Xd, z)
            cmpd(1, h == exp, [2, 4, z, Xd, E, h, exp])
        clear()
    for z in range(0, 10):
        for X in multisets(5, 5):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            E = E_of(Xd)
            exp = PB(5, E, z)
            if TAMPER == 'ty':
                exp = flipC(exp)
            h = H_canonical(S + z + 2, Xd, z)
            cmpd(1, h == exp, [2, 5, z, Xd, E, h, exp])
        clear()

    # -------- D3: census n=6 + n=7
    sys.stderr.write('D3\n'); sys.stderr.flush()
    for z in range(0, 9):
        for X in multisets(6, 5):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            E = E_of(Xd)
            exp = PB(6, E, z)
            if TAMPER == 'ty':
                exp = flipC(exp)
            h = H_canonical(S + z + 3, Xd, z)
            cmpd(2, h == exp, [3, 6, z, Xd, E, h, exp])
        clear()
    for z in range(0, 9):
        for X in multisets(7, 4):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            E = E_of(Xd)
            exp = PB(7, E, z)
            if TAMPER == 'ty':
                exp = flipC(exp)
            h = H_canonical(S + z + 4, Xd, z)
            cmpd(2, h == exp, [3, 7, z, Xd, E, h, exp])
        clear()

    # -------- D4: census n=2 incl. wall row
    sys.stderr.write('D4\n'); sys.stderr.flush()
    for z in range(0, 13):
        k = z - 1
        for a in range(1, 9):
            for g in range(0, 17):
                Xd = (a + g, a)
                if a + g > 24:
                    continue
                exp = PB(2, g, z)
                if TAMPER == 'wl':
                    exp = flipC(exp)
                h = H_canonical(2 * a + g + k, Xd, z)
                cmpd(3, h == exp, [4, z, a, g, k, h, exp])
        clear()

    # -------- D5: typed self-check
    sys.stderr.write('D5\n'); sys.stderr.flush()
    for n in (2, 3, 4, 5, 6):
        hi = {2: 9, 3: 8, 4: 6, 5: 5, 6: 4}[n]
        for z in range(0, 9):
            for X in combinations_with_replacement(range(1, hi + 1), n):
                if sum(X) > 30:
                    continue
                S = sum(X)
                k = z + n - 3
                Xd = tuple(sorted(X, reverse=True))
                exp = PB(n, E_of(Xd), z)
                if TAMPER == 'tt':
                    exp = flipC(exp)
                kids = typed_kids(Xd, z, k)
                mx = mexs(kids)
                h = H_canonical(S + k, Xd, z)
                cmpd(4, (mx == exp) and (h == exp),
                     [5, n, z, Xd, k, mx, exp, h, kids])
            clear()

    # -------- D6: base lemma L-BR1
    sys.stderr.write('D6\n'); sys.stderr.flush()
    for x in range(1, 21):
        for Z in range(1, 16):
            R = x + Z - 2
            exp = PB1(x, Z)
            if TAMPER == 'lm':
                exp = flipC(exp)
            a1 = single_token(x, Z, R)
            h1 = vC(x, Z, R)
            h2 = vO(x, Z, R)
            cmpd(5, a1 == h1 == h2 == exp, [6, 'lbr1', x, Z, R, a1, h1, h2, exp])
        clear()
    for x in range(1, 16):
        for z in range(0, 13):
            for R in range(0, x + z + 6):
                exp = single_token(x, z, R)
                if TAMPER == 'lm':
                    exp = flipC(exp) if exp in (0, 1) else (exp % 2)
                h1 = vC(x, z, R)
                h2 = vO(x, z, R)
                cmpd(5, h1 == h2 == exp, [6, 'rep', x, z, R, h1, h2, exp])
            clear()

    # -------- D7: published anchors
    sys.stderr.write('D7\n'); sys.stderr.flush()
    # (a) T-DB boundary law at k = z+n-2 (published K1311/K1308)
    for n in (2, 3, 4):
        hi = {2: 8, 3: 6, 4: 5}[n]
        if TAMPER == 'ps':
            pass
        for z in range(0, 9):
            for X in multisets(n, hi):
                if n == 2 and sum(X) > 30:
                    continue
                S = sum(X)
                Xd = tuple(sorted(X, reverse=True))
                E = E_of(Xd)
                k = z + n - 2
                exp = Dlaw(E, k)
                if TAMPER == 'ps':
                    exp = (exp + 1) % 3
                h = H_canonical(S + k, Xd, z)
                cmpd(6, h == exp, [7, 'tdb', n, z, Xd, k, h, exp, E])
            clear()
    # (b) published K1310 T-NCW-B bed constants on the rows k=z-1
    for z in (1, 2, 3, 4, 5, 6):
        exp = {1: 1, 2: 2}.get(z, 0)
        if TAMPER == 'ps':
            exp = flipC(exp)
        for a in range(1, 10):
            Xd = (a, a)
            h = H_canonical(2 * a + z - 1, Xd, z)
            cmpd(6, h == exp, [7, 'beds', z, a, h, exp])
        clear()
    # (c) published K1310 T-NCW-P g*<=0 branch at k=z-1, z>=2: [g odd]
    for z in range(2, 13):
        for m in range(1, 11):
            for g in range(1, 13):
                Xd = (m + g, m)
                exp = g % 2
                if TAMPER == 'ps':
                    exp = flipC(exp)
                h = H_canonical(2 * m + g + z - 1, Xd, z)
                cmpd(6, h == exp, [7, 'ncwp', z, m, g, h, exp])
        clear()
    # (d) published K1312 tail row [S mod 2] at k=z+n-1, z+n (connection)
    for n in (2, 3, 4):
        hi = {2: 6, 3: 5, 4: 4}[n]
        for z in range(0, 5):
            for X in multisets(n, hi):
                S = sum(X)
                Xd = tuple(sorted(X, reverse=True))
                for k in (z + n - 1, z + n):
                    exp = S % 2
                    if TAMPER == 'ps':
                        exp = flipC(exp)
                    h = H_canonical(S + k, Xd, z)
                    cmpd(6, h == exp, [7, 'tail', n, z, Xd, k, h, exp])
            clear()

    # -------- D8: cross-engine
    sys.stderr.write('D8\n'); sys.stderr.flush()
    for (n, hi, zs) in ((2, 8, (0, 5, 10)), (3, 6, (0, 3, 7, 11)),
                        (4, 5, (0, 4, 9))):
        for z in zs:
            for X in multisets(n, hi):
                if n == 2 and sum(X) > 28:
                    continue
                S = sum(X)
                Xd = tuple(sorted(X, reverse=True))
                k = z + n - 3
                exp = PB(n, E_of(Xd), z)
                if TAMPER == 'ce':
                    exp = flipC(exp)
                hc = H_canonical(S + k, Xd, z)
                ho = H_ordered(S + k, Xd, z)
                cmpd(7, hc == ho == exp, [8, n, z, Xd, k, hc, ho, exp])
            clear()

    # -------- D9: OBS-BBL watershed
    sys.stderr.write('D9\n'); sys.stderr.flush()
    obs['obsbbl_rows'] = []
    for z in range(1, 8):
        cells = [X for X in multisets(3, 8) if sum(X) <= 15]
        n1 = 0; n2 = 0; pb = 0
        for X in cells:
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            E = E_of(Xd)
            h = H_canonical(S + z, Xd, z)
            n1 += 0 if h == Dlaw(E, z - 1) else 1
            n2 += 0 if h == Dlaw(E, z) else 1
            pb += 0 if h == PB(3, E, z) else 1
        clear()
        frozen = OBS_BBL[z - 1]
        exprow = [z, len(cells), n1, n2]
        if TAMPER == 'ob' and z == 3:
            exprow = [z, len(cells), n1, n2 - 1]   # corrupted frozen value
        ok = (exprow == frozen[:4]) and (pb == 0)
        cmpd(8, ok, [9, z, len(cells), n1, n2, pb, frozen])
        obs['obsbbl_rows'].append([z, len(cells), n1, n2, pb])

    # -------- D10: deep-negative-E
    sys.stderr.write('D10\n'); sys.stderr.flush()
    for n in (3, 4, 5):
        for a in range(1, 9):
            Xe = tuple(sorted([a] * n, reverse=True))
            Xn = tuple(sorted([a + 1] + [a] * (n - 1), reverse=True))
            for X in (Xe, Xn):
                for z in range(0, 41):
                    S = sum(X); E = E_of(X)
                    exp = PB(n, E, z)
                    if TAMPER == 'zz':
                        exp = flipC(exp)
                    h = H_canonical(S + z + n - 3, X, z)
                    cmpd(9, h == exp, [10, n, a, z, E, h, exp])
                clear()

    # -------- D11: T-DB adjacency
    sys.stderr.write('D11\n'); sys.stderr.flush()
    for (n, hi, zmax, amax, gmax) in ((2, None, 8, 6, 12), (3, 6, 8, None, None),
                                      (4, 5, 7, None, None)):
        if n == 2:
            for z in range(0, zmax + 1):
                for a in range(1, amax + 1):
                    for g in range(0, gmax + 1):
                        Xd = (a + g, a)
                        S = sum(Xd); E = E_of(Xd)
                        expB = Dlaw(E, z)             # boundary k=z
                        if TAMPER == 'db':
                            expB = (expB + 1) % 3
                        hB = H_canonical(S + z, Xd, z)
                        cmpd(10, hB == expB, [11, 2, z, Xd, 'bd', hB, expB])
                        expT = PB(2, E, z)
                        hT = H_canonical(S + z - 1, Xd, z)
                        cmpd(10, hT == expT, [11, 2, z, Xd, 'tb', hT, expT])
                clear()
        else:
            for z in range(0, zmax + 1):
                for X in multisets(n, hi):
                    if sum(X) > 26:
                        continue
                    S = sum(X)
                    Xd = tuple(sorted(X, reverse=True))
                    E = E_of(Xd)
                    expB = Dlaw(E, z + n - 2)
                    if TAMPER == 'db':
                        expB = (expB + 1) % 3
                    hB = H_canonical(S + z + n - 2, Xd, z)
                    cmpd(10, hB == expB, [11, n, z, Xd, 'bd', hB, expB])
                    expT = PB(n, E, z)
                    hT = H_canonical(S + z + n - 3, Xd, z)
                    cmpd(10, hT == expT, [11, n, z, Xd, 'tb', hT, expT])
                clear()

    # -------- D12: seeded random sweep
    sys.stderr.write('D12\n'); sys.stderr.flush()
    rng = random.Random(1313)
    for _ in range(700):
        n = rng.randint(2, 7)
        z = rng.randint(0, 10)
        maxh = {2: 14, 3: 12, 4: 10, 5: 9, 6: 7, 7: 6}[n]
        heaps = []
        for _i in range(n):
            heaps.append(rng.randint(1, maxh))
        Xd = tuple(sorted(heaps, reverse=True))
        S = sum(Xd); E = E_of(Xd)
        exp = PB(n, E, z)
        if TAMPER == 'rs':
            exp = flipC(exp)
        h = H_canonical(S + z + n - 3, Xd, z)
        cmpd(11, h == exp, [12, n, z, Xd, E, h, exp])
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
                            'D3_census_n67', 'D4_census_n2_wall',
                            'D5_typed_selfcheck', 'D6_lbr1_replication',
                            'D7_published_anchors', 'D8_cross_engine',
                            'D9_obsbbl_watershed', 'D10_deep_negE',
                            'D11_tdb_adjacency', 'D12_random_sweep']
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)


main()

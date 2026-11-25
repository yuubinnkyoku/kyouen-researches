#!/usr/bin/env python3
"""verify_k1311: machine audit for the BOUNDARY-BAND package (the universal
boundary-row / diagonal-band collapse for ALL token multiplicities).

Theorems under audit (claims and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of
the hand proofs pointwise; censuses are consistency checks and do NOT
replace the proofs; all quantifiers are UNBOUNDED):

  L-SDB (base, derived from the published K0832 single-token closed form):
      for all x >= 1, z >= 1:  v(x, z, x+z-1) = D(x, z-1).
  T-DB (universal): for all n >= 2, z >= 0, sorted multisets
      X = (x1 >= x2 >= ... >= xn >= 1), with the BOUNDARY row
      k := z + n - 2 (>= 0) and the single excess coordinate
      E := x1 - (x2 + ... + xn):
          H(S + k; X; z) = D(E, k)
      where D is the published K1308 Z-DIAG 3-branch law
          D(g, p) = [g odd]   (g <= p)
                  = 2          (g = p+1)
                  = [g even]   (g >= p+2)
      evaluated with python parity conventions for g <= 0 (E can be as low
      as 2-n: all-ones).  The n=2 instance IS the published Z-DIAG/T-DU'
      vertex row k = z (beds g=0 -> D(0,z)=0); the n=3 instance resolves
      the top row k = z+1 of the K0832 triple transient band, and proves
      K0832 conjecture B (kappa=0, j=2 family R = 2x-1 -> value 2) as the
      exact subfamily E = z+2 of the boundary row; n >= 4 rows are new.
  Typed child identities (engine-free position equalities): every option of
      a boundary cell (n >= 2, k >= 1) lands in
        { boundary cell (n, same k, E-1)   A, unique top x1 >= 2
        , boundary cell (n, same k, E+1)   A, tied top or any tail heap
        , boundary cell (n-1, plane z+1, same k, E+1)  A-remove of a 1-heap
        , boundary cell (n, plane z-1, k-1, same E)    C (z >= 1) }
      so the packet closes on the outer induction in n and the inner strong
      induction on R (A-reduce/A-remove heirs of n=2 pairs are single tokens
      at their own boundary = L-SDB; single-token remove-children of pairs
      reproduce their L-SDB claim = D(E+1, k)).

Batteries (counts and the mutation table are declared in the single-owner
note; expected overall_bad == 0; stdout deterministic byte-identical,
volatile info on stderr only):

  D1  L-SDB census: x<=20, z=1..12, engine vs D(x, z-1) (240 cells).
  D2  n=2 boundary anchor: pairs and beds k=z, z=0..10, a<=8, g<=20,
      S<=28 vs D(g, z).
  D3  triple boundary census k=z+1: z=0..10, S<=16 full sweep vs D(E, k).
  D4  n=4..7 boundary census: z=0..6, heaps<=8, S<= {16,15,14,13}.
  D5  typed self-check n=2..5, z<=6, heaps<=6, S<=15: children built ONLY
      from the claim/law tables (D + L-SDB), mex == claim == engine.
  D6  cross-engine canonical vs ordered AND claim, n=2..4, z<=6, S<=13.
  D7  tail interface rows k=z+n-1, z+n (published K0832 regime corollary
      transcription), n=2..4, z<=4, heaps<=6, S<=14.
  D8  far stress: triples z=7..14, quads z=7..12 (seed 1311/1312, 60 pts),
      n=5..7 z=7..9 (seed 1313, 40 pts).
  D9  K0832 conjecture-B interface: triple boundary cells with E=z+2 have
      value EXACTLY 2 and no other cell of the swept domain (z=0..8, S<=14)
      has value 2 (2-set equality).
  D10 all-ones n=2..14 x z=0..10 and near-all-ones (x,1^{n-1}) n=3..8,
      x=2..8, z=0..8 vs D(2-n, k) / D(x-n+1, k).
  D11 OBS-BBL frozen below-row table: triple rows k=z (z=1..7, S<=15,
      heaps<=8) re-census reproduces the frozen per-z mismatch counts
      against the two naive laws D(E, z-1) / D(E, z) (observation register:
      NO claim; the sub-boundary rows are registered open).
  D12 random multiset sweep n=2..6, z=0..7 (seed 1314, 500 points) vs claim.

TAMPER modes: --tamper-engine (rc 2), --tamper=<np1|np2|np3|np4|ty|ce|tl|
fs|kb|ao|ob|rs> (flip exactly one battery's expectation; all rc 1 with the
exact pre-declared bad counts). Determinism: official runs byte-identical
on stdout.
"""
import json, hashlib, sys, time
from functools import lru_cache
from itertools import combinations_with_replacement
import random

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


def IND(b):
    return 1 if b else 0


# ---- the law under audit (published K1308 Z-DIAG 3-branch function) --------
def Dlaw(g, p):
    if TAMPER == 'np2b':  # never active in official runs; placeholder guard
        g = g
    if g <= p:
        return 1 if g % 2 == 1 else 0
    if g == p + 1:
        return 2
    return 1 if g % 2 == 0 else 0


def flip(v):
    return {0: 1, 1: 0, 2: 2}[v]


def E_of(Xd):
    return Xd[0] - (sum(Xd) - Xd[0])


def claim_db(n, z, Xd):
    k = z + n - 2
    c = Dlaw(E_of(Xd), k)
    if TAMPER == 'ty':
        c = flip(c)
    return k, c


def typed_options(Xd, z, k):
    """Option VALUES of a boundary cell (n>=2) from the claim tables only:
    D-law + L-SDB (single-token heirs via their boundary claim D(x, k))."""
    n = len(Xd)
    E = E_of(Xd)
    opts = set()
    x1 = Xd[0]
    uniq_top = (n >= 2 and x1 > Xd[1])
    if uniq_top and x1 >= 2:
        opts.add(Dlaw(E - 1, k))
    for v in set(Xd[1:]):
        if v >= 2:
            opts.add(Dlaw(E + 1, k))
    if 1 in Xd:
        opts.add(Dlaw(E + 1, k))
    if z >= 1:
        opts.add(1 ^ Dlaw(E, k - 1))
    return opts


def main():
    t0 = time.time()
    res = {'kit': 'verify_k1311', 'engine_sha': ENGINE_SHA,
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

    # -------- D1: L-SDB census, n=1 --------------------------------------
    for z in range(1, 13):
        for x in range(1, 21):
            v = H_canonical(x + z - 1, (x,), z)
            exp = Dlaw(x, z - 1)
            if TAMPER == 'np1':
                exp = flip(exp)
            cmpd(0, v == exp, [1, z, x, v, exp])
        clear()

    # -------- D2: n=2 boundary anchor (pairs + beds g=0) ------------------
    for z in range(0, 11):
        for a in range(1, 9):
            for g in range(0, 21):
                S = 2 * a + g
                if S > 28:
                    continue
                v = H_canonical(S + z, (a + g, a), z)
                exp = Dlaw(g, z)
                if TAMPER == 'np2':
                    exp = flip(exp)
                cmpd(1, v == exp, [2, z, a, g, v, exp])
        clear()

    # -------- D3: triple boundary census, k=z+1 ---------------------------
    for z in range(0, 11):
        k = z + 1
        b = 0
        for S in range(3, 17):
            for x in range(1, S):
                for y in range(1, min(x, S - x) + 1):
                    w = S - x - y
                    if 1 <= w <= y:
                        Xd = (x, y, w)
                        v = H_canonical(S + k, Xd, z)
                        exp = Dlaw(x - y - w, k)
                        if TAMPER == 'np3':
                            exp = flip(exp)
                        cmpd(2, v == exp, [3, z, x, y, w, v, exp])
        clear()

    # -------- D4: n=4..7 boundary census -----------------------------------
    for n in (4, 5, 6, 7):
        Smax = {4: 16, 5: 15, 6: 14, 7: 13}[n]
        for z in range(0, 7):
            k = z + n - 2
            for X in combinations_with_replacement(range(1, 9), n):
                S = sum(X)
                if S > Smax:
                    continue
                Xd = tuple(sorted(X, reverse=True))
                v = H_canonical(S + k, Xd, z)
                exp = Dlaw(E_of(Xd), k)
                if TAMPER == 'np4':
                    exp = flip(exp)
                cmpd(3, v == exp, [4, n, z, Xd, v, exp])
            clear()

    # -------- D5: typed self-check (claims only) ---------------------------
    for n in (2, 3, 4, 5):
        for z in range(0, 7):
            k = z + n - 2
            if k < 1:
                continue
            for X in combinations_with_replacement(range(1, 7), n):
                if sum(X) > 15:
                    continue
                Xd = tuple(sorted(X, reverse=True))
                k2, exp = claim_db(n, z, Xd)
                opts = typed_options(Xd, z, k)
                m = 0
                while m in opts:
                    m += 1
                v = H_canonical(sum(Xd) + k, Xd, z)
                if TAMPER == 'ty':
                    cmpd(4, False, [5, n, z, Xd, m, exp, v])
                else:
                    cmpd(4, m == exp == v, [5, n, z, Xd, m, exp, v])
            clear()

    # -------- D6: cross-engine canonical vs ordered AND claim --------------
    for n in (2, 3, 4):
        for z in range(0, 7):
            k = z + n - 2
            for X in combinations_with_replacement(range(1, 7), n):
                if sum(X) > 13:
                    continue
                Xd = tuple(sorted(X, reverse=True))
                vC = H_canonical(sum(Xd) + k, Xd, z)
                vO = H_ordered(sum(Xd) + k, Xd, z)
                exp = Dlaw(E_of(Xd), k)
                if TAMPER == 'ce':
                    exp = flip(exp)
                cmpd(5, vC == vO == exp, [6, n, z, Xd, vC, vO, exp])
            clear()

    # -------- D7: tail interface rows (published regime corollary) ---------
    for n in (2, 3, 4):
        for z in range(0, 5):
            for kk in (z + n - 1, z + n):
                for X in combinations_with_replacement(range(1, 7), n):
                    S = sum(X)
                    if S > 14:
                        continue
                    Xd = tuple(sorted(X, reverse=True))
                    v = H_canonical(S + kk, Xd, z)
                    exp = S % 2
                    if TAMPER == 'tl':
                        exp = 1 - exp
                    cmpd(6, v == exp, [7, n, z, kk, Xd, v, exp])
            clear()

    # -------- D8: far stress (seeded) ---------------------------------------
    random.seed(1311)
    for z in range(7, 15):
        k = z + 1
        for _ in range(60):
            X = tuple(sorted((random.randint(1, 12) for _ in range(3)), reverse=True))
            v = H_canonical(sum(X) + k, X, z)
            exp = Dlaw(E_of(X), k)
            if TAMPER == 'fs':
                exp = flip(exp)
            cmpd(7, v == exp, [8, 3, z, X, v, exp])
        clear()
    random.seed(1312)
    for z in range(7, 13):
        k = z + 2
        for _ in range(60):
            X = tuple(sorted((random.randint(1, 12) for _ in range(4)), reverse=True))
            v = H_canonical(sum(X) + k, X, z)
            exp = Dlaw(E_of(X), k)
            if TAMPER == 'fs':
                exp = flip(exp)
            cmpd(7, v == exp, [8, 4, z, X, v, exp])
        clear()
    random.seed(1313)
    for n in (5, 6, 7):
        for z in range(7, 10):
            k = z + n - 2
            for _ in range(40):
                X = tuple(sorted((random.randint(1, 9) for _ in range(n)), reverse=True))
                v = H_canonical(sum(X) + k, X, z)
                exp = Dlaw(E_of(X), k)
                if TAMPER == 'fs':
                    exp = flip(exp)
                cmpd(7, v == exp, [8, n, z, X, v, exp])
            clear()

    # -------- D9: K0832 conjecture-B interface (2-set equality) ------------
    frozen2 = 0
    for z in range(0, 9):
        k = z + 1
        for S in range(3, 15):
            for x in range(1, S):
                for y in range(1, min(x, S - x) + 1):
                    w = S - x - y
                    if 1 <= w <= y:
                        v = H_canonical(S + k, (x, y, w), z)
                        Eb = x - y - w
                        if TAMPER == 'kb':
                            ok = (v == 2) if Eb != z + 2 else (v != 2)
                        else:
                            ok = (v == 2) if Eb == z + 2 else (v != 2)
                        cmpd(8, ok, [9, z, x, y, w, Eb, v])
                        if v == 2:
                            frozen2 += 1
        clear()
    obs['D9_value2_cells'] = frozen2

    # -------- D10: all-ones and near-all-ones -------------------------------
    for n in range(2, 15):
        for z in range(0, 11):
            k = z + n - 2
            v = H_canonical(n + k, tuple([1] * n), z)
            exp = Dlaw(2 - n, k)
            if TAMPER == 'ao':
                exp = flip(exp)
            cmpd(9, v == exp, [10, 'a', n, z, v, exp])
        clear()
    for n in range(3, 9):
        for x in range(2, 9):
            for z in range(0, 9):
                k = z + n - 2
                Xd = tuple([x] + [1] * (n - 1))
                v = H_canonical(x + n - 1 + k, Xd, z)
                exp = Dlaw(x - (n - 1), k)
                if TAMPER == 'ao':
                    exp = flip(exp)
                cmpd(9, v == exp, [10, 'n', n, x, z, v, exp])
            clear()

    # -------- D11: OBS-BBL frozen below-row table (no claim) ----------------
    frozen = {1: (80, 80, 68), 2: (80, 56, 47), 3: (80, 31, 25),
              4: (80, 16, 12), 5: (80, 6, 4), 6: (80, 2, 1), 7: (80, 0, 0)}
    bowls = []
    for z in range(1, 8):
        tot = 0; b1 = 0; b2 = 0
        for X in combinations_with_replacement(range(1, 9), 3):
            if sum(X) > 15:
                continue
            Xd = tuple(sorted(X, reverse=True))
            E = E_of(Xd)
            v = H_canonical(sum(Xd) + z, Xd, z)   # k = z, one below boundary
            tot += 1
            if v != Dlaw(E, z - 1):
                b1 += 1
            if v != Dlaw(E, z):
                b2 += 1
        clear()
        entry = (tot, b1, b2)
        exp = frozen[z]
        if TAMPER == 'ob':
            exp = (exp[0], exp[1] + 7, exp[2] + 7)
        cmpd(10, entry == exp, [11, z, entry, exp])
        bowls.append((z, entry))
    obs['OBS_BBL_below_row'] = {
        'note': 'triple rows k=z (one below the boundary), heaps<=8, S<=15; '
                'mismatch counts against naive D(E, z-1) / D(E, z). '
                'Observation register ONLY: sub-boundary rows stay OPEN '
                '(registered O-BBL); the counts collapse toward 0 at large z '
                'in this finite window, no law is claimed.',
        'rows': bowls}

    # -------- D12: random multiset sweep --------------------------------------
    random.seed(1314)
    for _ in range(500):
        n = random.randint(2, 6)
        z = random.randint(0, 7)
        k = z + n - 2
        while True:
            X = tuple(sorted((random.randint(1, 10) for _ in range(n)), reverse=True))
            if sum(X) <= 22:
                break
        v = H_canonical(sum(X) + k, X, z)
        exp = Dlaw(E_of(X), k)
        if TAMPER == 'rs':
            exp = flip(exp)
        cmpd(11, v == exp, [12, n, z, X, v, exp])
        if counts[11] % 50 == 0:
            clear()

    info = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['obs'] = obs
    res['battery_names'] = ['D1_lsdb_census', 'D2_pair_zdiag_anchor',
                            'D3_triple_census', 'D4_quad_sept_census',
                            'D5_typed_selfcheck', 'D6_cross_engine',
                            'D7_tail_interface', 'D8_far_stress',
                            'D9_conjB_interface', 'D10_allones',
                            'D11_obsbbl_frozen', 'D12_random_sweep']
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)


main()

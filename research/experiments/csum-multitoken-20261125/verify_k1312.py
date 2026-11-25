#!/usr/bin/env python3
"""verify_k1312: machine audit for the MULTI-TOKEN C-SUM TAIL COLLAPSE
(the universal tail law of the residual multiset game at ALL token
multiplicities).

Theorems under audit (claims and FULL hand proofs in the single-owner
declaration note published FIRST; this machine checks the claims on wide
finite censuses and machine-checks the typed-children mex arithmetic of
the hand proofs pointwise; censuses are consistency checks and do NOT
replace the proofs; all quantifiers are UNBOUNDED):

  T-CSUM (universal): for every n >= 1, every multiset X of n tokens
      (each >= 1) with S = sum(X), every z >= 0 and every
      k >= z + n - 1:
          H(S + k; X; z) = S mod 2.
      The threshold z+n-1 is SHARP for n >= 3: on the boundary row
      k = z+n-2 the frozen witness lists below (149 certified cells,
      n=3..7) hold engine values != [S odd], and every one of them
      satisfies the published K1311 T-DB boundary law D(E, k) with
      E = 2*max(X) - S (machine-checked in D11: the two theorems close
      the whole region k >= z+n-2 for every multiset, n>=2, plus the
      n=1 base L-1). Subsumes the published n=2 vertex (K1308 T-UH /
      T-DU'), the published K0832 all-ones tail corollary (X = 1^n:
      R = n+k >= 2n+z-1 <-> k >= z+n-1, value [n odd]), and resolves
      K1308 O3/F1 (the C-SUM census conjecture becomes a theorem).
  L-1 (base, corollary of the published K0832 closed form): in the
      n=1 region k >= z, single_token(x, z, x+k) = x%2 = both engines.
  L-2 (empty positions): H(R; (); z) = 0 for all R, z >= 0
      (mex{1} = 0 induction; used by the proof's B-exit base).
  Typed child identities (engine-free): every option of a tail cell
      (n >= 1, k >= z+n-1) is one of
        { A-reduce: (n, S-1, same k, same z)        token v > 1
        , B-remove: (n-1, S-1, same k, z+1)         token v = 1
        , C:        (n, S, k-1, z-1)   value 1^    if z >= 1 }
      and each child is again in-region for its own threshold, so
      T-CSUM + L-1/L-2 close by double induction (outer n, inner R).
      D5 machine-checks mex(children) == claim == engine and the
      uniformity set(children) == {1-claim} pointwise.

Batteries (counts and the mutation table declared in the single-owner
note; expected overall_bad == 0; stdout deterministic byte-identical,
volatile info on stderr only):

  D1  T-CSUM census n=3: z=0..12, tokens<=6, k=z+2..z+4 (2184).
  D2  census n=4 (z=0..9, tokens<=5, k=z+3..z+5, 2100) + far n=3
      stress (z=15/18/21, tokens<=5, k=z+2/z+3, 210).
  D3  census n=5: z=0..7, tokens<=5, k=z+4..z+6.
  D4  census n=6 (z=0..6, tokens<=4, k=z+5/z+6) + n=7 (z=0..5,
      tokens<=3, k=z+6/z+7) + far n=4 stress (z=15/18, tokens<=4,
      k=z+3/z+4).
  D5  typed self-check n=2..5, z<=8, tokens<=5, k=z+n-1..z+n+1:
      children built ONLY from the claim tables (csum + the published
      single-token closed form for B-heirs of n=2), mex == claim ==
      engine, uniformity set(children) == {1-claim}.
  D6  base lemmas: L-2 empties R<=19 x z<=9; L-1 n=1 closed form vs
      BOTH engines (x<=12, z<=9, k=z..z+2); n=1 engine-children
      uniformity (z<=8, x<=10, k=z..z+3).
  D7  published anchors (transcriptions, byte-faithful boxes): K1308
      D8 C-SUM census boxes (triples 1344 / mixed 840 / quads 180,
      published there as OBSERVED conjecture, here theorem instances),
      K1308 D1 T-UH tail box 5760 ([g odd]), L-SB spot 264 (x%2).
  D8  cross-engine canonical vs ordered AND claim (E9 boxes: n=3
      z=0/3/7/11, n=4 z=0/4/9, n=2 z=0/5/10; k=z+n-1, z+n+1).
  D9  sharpness witnesses: the 149 frozen boundary-row counters
      (k=z+n-2, n=3..7) re-evaluated: engine == recorded AND
      engine != [S odd] (finite certification of the witnesses; the
      sharpness STATEMENT is the finite existence claim, the universal
      law at k=z+n-2 belongs to K1311 T-DB).
  D10 OBS tables (NO claim): near-threshold row k=z+n-2 value
      distributions n=3 (z=0..10, tokens<=6) and n=4 (z=0..8,
      tokens<=5), and pure-family (a,...,a) bad counts vs [S odd] for
      n=3 z<=12 a<=9, n=4 z<=10 a<=9, n=5 z<=8 a<=8, koff=0..n-1
      (the non-monotone pure stabilization pattern; observation
      register only).
  D11 T-DB interlock: the same 149 witnesses satisfy the published
      K1311 boundary law D(E, k), E = 2*max(X) - S, k = z+n-2
      (adjacent-row interface between the two theorems).
  D12 sharpness construction (finite check of Corollary C-SHARP,
      which follows rigorously from the published T-DB): for
      n = 2..11, z = 0..6 the family X = (z+2n-1, 1^(n-1)) at
      k = z+n-2 has E = z+n >= k+2, engine value == D(E,k) == 1-[S odd]
      (unequal to the T-CSUM claim), and the family
      X = (z+2n-2, 1^(n-1)) has E = k+1, engine value == 2. So the
      threshold k >= z+n-1 cannot be lowered for any n >= 2.

TAMPER modes: --tamper-engine (rc 2, mutated block sha), --tamper=
c3|c4|c5|c67|ty|lm|ps|ce|sw|ob|db|sc (flip exactly one battery's
expectation; all rc 1 with the exact pre-declared bad counts).
Determinism: official runs byte-identical on stdout.
"""
import json, hashlib, sys, time
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
v = single_token

TAMPER = None
for a in sys.argv[1:]:
    if a.startswith('--tamper='):
        TAMPER = a.split('=', 1)[1]


def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()


def IND(b):
    return 1 if b else 0


# ---- published K1308/K1311 Z-DIAG 3-branch law (transcription) ----------
def Dlaw(g, p):
    if g <= p:
        return 1 if g % 2 == 1 else 0
    if g == p + 1:
        return 2
    return 1 if g % 2 == 0 else 0


def flipC(val):
    return 1 - val if val in (0, 1) else 1


# ---- the claim under audit ----------------------------------------------
def csum(n, z, k, Xd):
    """T-CSUM claim (with the ty mutation hook). Region-guarded."""
    assert k >= z + n - 1, ('region violation', n, z, k, Xd)
    c = sum(Xd) % 2
    if TAMPER == 'ty':
        c = flipC(c)
    return c


def mexs(vals):
    s = set(vals)
    x = 0
    while x in s:
        x += 1
    return x


def typed_kids(Xd, z, k):
    """Option VALUES of a tail cell (n>=2) from the claim tables ONLY:
    T-CSUM for multi-token heirs + the published closed form for the
    single-token heirs of n=2 B-exits."""
    n = len(Xd)
    R = sum(Xd) + k
    kids = []
    for val in sorted(set(Xd)):
        lst = list(Xd)
        lst.remove(val)
        if val > 1:
            # A-reduce ONE heap val -> val-1 (n unchanged, k/z unchanged)
            lst.append(val - 1)
            kid = tuple(sorted(lst, reverse=True))
            kids.append(csum(n, z, k, kid))
        else:
            # B-remove ONE heap of value 1: n-1 heaps, plane z+1, k same
            kid = tuple(sorted(lst, reverse=True))
            if len(kid) == 1:
                # B-heir single token at plane z+1, budget R-1 (k same):
                # in-region (k >= z+1) published closed form = x%2.
                assert k >= z + 1
                kids.append(single_token(kid[0], z + 1, R - 1))
            else:
                kids.append(csum(n - 1, z + 1, k, kid))
    if z >= 1:
        kids.append(1 ^ csum(n, z - 1, k - 1, Xd))
    return kids


def multisets(n, hi):
    return list(combinations_with_replacement(range(1, hi + 1), n))


# ---- frozen pre-declaration data (explore_csum.py/.out, E-wave 正本) ----
WIT_N3 = [[[1,1,4],0,1,2,0],[[1,1,5],0,1,0,1],[[1,1,6],0,1,1,0],[[1,1,7],0,1,0,1],[[1,1,8],0,1,1,0],[[1,1,9],0,1,0,1],[[1,2,5],0,1,2,0],[[1,2,6],0,1,0,1],[[1,2,7],0,1,1,0],[[1,2,8],0,1,0,1],[[1,2,9],0,1,1,0],[[1,3,6],0,1,2,0],[[1,3,7],0,1,0,1],[[1,3,8],0,1,1,0],[[1,3,9],0,1,0,1],[[1,4,7],0,1,2,0],[[1,4,8],0,1,0,1],[[1,4,9],0,1,1,0],[[1,5,8],0,1,2,0],[[1,5,9],0,1,0,1],[[1,6,9],0,1,2,0],[[2,2,6],0,1,2,0],[[2,2,7],0,1,0,1],[[2,2,8],0,1,1,0],[[2,2,9],0,1,0,1],[[2,3,7],0,1,2,0],[[2,3,8],0,1,0,1],[[2,3,9],0,1,1,0],[[2,4,8],0,1,2,0],[[2,4,9],0,1,0,1],[[2,5,9],0,1,2,0],[[3,3,8],0,1,2,0],[[3,3,9],0,1,0,1],[[3,4,9],0,1,2,0],[[1,1,5],1,2,2,1],[[1,1,6],1,2,1,0],[[1,1,7],1,2,0,1],[[1,1,8],1,2,1,0],[[1,1,9],1,2,0,1],[[1,2,6],1,2,2,1],[[1,2,7],1,2,1,0],[[1,2,8],1,2,0,1],[[1,2,9],1,2,1,0],[[1,3,7],1,2,2,1],[[1,3,8],1,2,1,0],[[1,3,9],1,2,0,1],[[1,4,8],1,2,2,1],[[1,4,9],1,2,1,0],[[1,5,9],1,2,2,1],[[2,2,7],1,2,2,1],[[2,2,8],1,2,1,0],[[2,2,9],1,2,0,1],[[2,3,8],1,2,2,1],[[2,3,9],1,2,1,0],[[2,4,9],1,2,2,1],[[3,3,9],1,2,2,1],[[1,1,6],2,3,2,0],[[1,1,7],2,3,0,1],[[1,1,8],2,3,1,0],[[1,1,9],2,3,0,1],[[1,2,7],2,3,2,0],[[1,2,8],2,3,0,1],[[1,2,9],2,3,1,0],[[1,3,8],2,3,2,0],[[1,3,9],2,3,0,1],[[1,4,9],2,3,2,0],[[2,2,8],2,3,2,0],[[2,2,9],2,3,0,1],[[2,3,9],2,3,2,0],[[1,1,7],3,4,2,1],[[1,1,8],3,4,1,0],[[1,1,9],3,4,0,1],[[1,2,8],3,4,2,1],[[1,2,9],3,4,1,0],[[1,3,9],3,4,2,1],[[2,2,9],3,4,2,1],[[1,1,8],4,5,2,0],[[1,1,9],4,5,0,1],[[1,2,9],4,5,2,0],[[1,1,9],5,6,2,1]]
WIT_N4 = [[[1,1,1,6],0,2,2,1],[[1,1,1,7],0,2,1,0],[[1,1,1,8],0,2,0,1],[[1,1,1,9],0,2,1,0],[[1,1,1,10],0,2,0,1],[[1,1,2,7],0,2,2,1],[[1,1,2,8],0,2,1,0],[[1,1,2,9],0,2,0,1],[[1,1,2,10],0,2,1,0],[[1,1,3,8],0,2,2,1],[[1,1,3,9],0,2,1,0],[[1,1,3,10],0,2,0,1],[[1,1,4,9],0,2,2,1],[[1,1,4,10],0,2,1,0],[[1,1,5,10],0,2,2,1],[[1,2,2,8],0,2,2,1],[[1,2,2,9],0,2,1,0],[[1,2,2,10],0,2,0,1],[[1,2,3,9],0,2,2,1],[[1,2,3,10],0,2,1,0],[[1,2,4,10],0,2,2,1],[[1,3,3,10],0,2,2,1],[[2,2,2,9],0,2,2,1],[[2,2,2,10],0,2,1,0],[[2,2,3,10],0,2,2,1],[[1,1,1,7],1,3,2,0],[[1,1,1,8],1,3,0,1],[[1,1,1,9],1,3,1,0],[[1,1,1,10],1,3,0,1],[[1,1,2,8],1,3,2,0],[[1,1,2,9],1,3,0,1],[[1,1,2,10],1,3,1,0],[[1,1,3,9],1,3,2,0],[[1,1,3,10],1,3,0,1],[[1,1,4,10],1,3,2,0],[[1,2,2,9],1,3,2,0],[[1,2,2,10],1,3,0,1],[[1,2,3,10],1,3,2,0],[[2,2,2,10],1,3,2,0],[[1,1,1,8],2,4,2,1],[[1,1,1,9],2,4,1,0],[[1,1,1,10],2,4,0,1],[[1,1,2,9],2,4,2,1],[[1,1,2,10],2,4,1,0],[[1,1,3,10],2,4,2,1],[[1,2,2,10],2,4,2,1],[[1,1,1,9],3,5,2,0],[[1,1,1,10],3,5,0,1],[[1,1,2,10],3,5,2,0]]
WIT_N5 = [[[1,1,1,1,8],0,3,2,0]]
WIT_N6 = [[[1,1,1,1,1,10],0,4,2,1],[[1,1,1,1,1,11],0,4,1,0],[[1,1,1,1,1,12],0,4,0,1],[[1,1,1,1,2,11],0,4,2,1],[[1,1,1,1,2,12],0,4,1,0],[[1,1,1,1,3,12],0,4,2,1],[[1,1,1,2,2,12],0,4,2,1],[[1,1,1,1,1,11],1,5,2,0],[[1,1,1,1,1,12],1,5,0,1],[[1,1,1,1,2,12],1,5,2,0],[[1,1,1,1,1,12],2,6,2,1]]
WIT_N7 = [[[1,1,1,1,1,1,12],0,5,2,0],[[1,1,1,1,1,1,13],0,5,0,1],[[1,1,1,1,1,1,14],0,5,1,0],[[1,1,1,1,1,2,13],0,5,2,0],[[1,1,1,1,1,2,14],0,5,0,1],[[1,1,1,1,1,3,14],0,5,2,0],[[1,1,1,1,2,2,14],0,5,2,0],[[1,1,1,1,1,1,13],1,6,2,1]]
E7_N3 = {"0":{"0":25,"1":27,"2":4},"1":{"0":27,"1":27,"2":2},"2":{"0":27,"1":28,"2":1},"3":{"0":28,"1":28},"4":{"0":28,"1":28},"5":{"0":28,"1":28},"6":{"0":28,"1":28},"7":{"0":28,"1":28},"8":{"0":28,"1":28},"9":{"0":28,"1":28},"10":{"0":28,"1":28}}      # k=z+1 n=3 value distributions per z
E7_N4 = {"0":{"0":38,"1":32},"1":{"0":38,"1":32},"2":{"0":38,"1":32},"3":{"0":38,"1":32},"4":{"0":38,"1":32},"5":{"0":38,"1":32},"6":{"0":38,"1":32},"7":{"0":38,"1":32},"8":{"0":38,"1":32}}      # k=z+2 n=4 value distributions per z
E8_PURE = {"n3":{"koff0":[117,63],"koff1":[117,0],"koff2":[117,0]},"n4":{"koff0":[99,0],"koff1":[99,79],"koff2":[99,0],"koff3":[99,0]},"n5":{"koff0":[72,49],"koff1":[72,0],"koff2":[72,63],"koff3":[72,0],"koff4":[72,0]}}      # pure family (a,...,a) bad counts per koff


def main():
    t0 = time.time()
    res = {'kit': 'verify_k1312', 'engine_sha': ENGINE_SHA,
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

    # -------- D1: T-CSUM census, n=3, k=z+2..z+4 ------------------------
    for z in range(0, 13):
        for X in multisets(3, 6):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            for k in range(z + 2, z + 5):
                exp = csum(3, z, k, Xd)
                if TAMPER == 'c3':
                    exp = flipC(exp)
                h = H_canonical(S + k, Xd, z)
                cmpd(0, h == exp, [1, z, Xd, k, h, exp])
        clear()

    # -------- D2: census n=4 + far n=3 stress -----------------------------
    for z in range(0, 10):
        for X in multisets(4, 5):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            for k in range(z + 3, z + 6):
                exp = csum(4, z, k, Xd)
                if TAMPER == 'c4':
                    exp = flipC(exp)
                h = H_canonical(S + k, Xd, z)
                cmpd(1, h == exp, [2, z, Xd, k, h, exp])
        clear()
    for z in (15, 18, 21):
        for X in multisets(3, 5):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            for k in (z + 2, z + 3):
                exp = csum(3, z, k, Xd)
                if TAMPER == 'c4':
                    exp = flipC(exp)
                h = H_canonical(S + k, Xd, z)
                cmpd(1, h == exp, [2, 'far', z, Xd, k, h, exp])
        clear()

    # -------- D3: census n=5, k=z+4..z+6 ----------------------------------
    for z in range(0, 8):
        for X in multisets(5, 5):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            for k in range(z + 4, z + 7):
                exp = csum(5, z, k, Xd)
                if TAMPER == 'c5':
                    exp = flipC(exp)
                h = H_canonical(S + k, Xd, z)
                cmpd(2, h == exp, [3, z, Xd, k, h, exp])
        clear()

    # -------- D4: census n=6,7 + far n=4 stress ----------------------------
    for z in range(0, 7):
        for X in multisets(6, 4):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            for k in (z + 5, z + 6):
                exp = csum(6, z, k, Xd)
                if TAMPER == 'c67':
                    exp = flipC(exp)
                h = H_canonical(S + k, Xd, z)
                cmpd(3, h == exp, [4, 6, z, Xd, k, h, exp])
        clear()
    for z in range(0, 6):
        for X in multisets(7, 3):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            for k in (z + 6, z + 7):
                exp = csum(7, z, k, Xd)
                if TAMPER == 'c67':
                    exp = flipC(exp)
                h = H_canonical(S + k, Xd, z)
                cmpd(3, h == exp, [4, 7, z, Xd, k, h, exp])
        clear()
    for z in (15, 18):
        for X in multisets(4, 4):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            for k in (z + 3, z + 4):
                exp = csum(4, z, k, Xd)
                if TAMPER == 'c67':
                    exp = flipC(exp)
                h = H_canonical(S + k, Xd, z)
                cmpd(3, h == exp, [4, 'far', z, Xd, k, h, exp])
        clear()

    # -------- D5: typed self-check (claims-only children) -----------------
    for n in (2, 3, 4, 5):
        for z in range(0, 9):
            for X in combinations_with_replacement(range(1, 6), n):
                S = sum(X)
                Xd = tuple(sorted(X, reverse=True))
                for k in range(z + n - 1, z + n + 2):
                    exp = csum(n, z, k, Xd)
                    kids = typed_kids(Xd, z, k)
                    mx = mexs(kids)
                    h = H_canonical(S + k, Xd, z)
                    ok = (mx == exp) and (h == exp) and (set(kids) == {1 - exp})
                    cmpd(4, ok, [5, n, z, Xd, k, mx, exp, h, kids])
                clear()

    # -------- D6: base lemmas ----------------------------------------------
    for R in range(0, 20):
        for z in range(0, 10):
            exp = 1 if TAMPER == 'lm' else 0
            h = H_canonical(R, (), z)
            cmpd(5, h == exp, [6, 'L2', R, z, h, exp])
        clear()
    for x in range(1, 13):
        for z in range(0, 10):
            for k in range(z, z + 3):
                R = x + k
                exp = x % 2
                if TAMPER == 'lm':
                    exp = flipC(exp)
                a1 = single_token(x, z, R)
                h1 = vC(x, z, R)
                h2 = vO(x, z, R)
                cmpd(5, a1 == h1 == h2 == exp, [6, 'L1', x, z, k, a1, h1, h2])
            clear()
    for z in range(0, 9):
        for x in range(1, 11):
            for k in range(z, z + 4):
                R = x + k
                vals = set()
                if x >= 2:
                    vals.add(H_canonical(R - 1, (x - 1,), z))
                else:
                    vals.add(H_canonical(R - 1, (), z + 1))
                if z >= 1:
                    vals.add(1 ^ H_canonical(R - 1, (x,), z - 1))
                expset = {x % 2} if TAMPER == 'lm' else {1 - x % 2}
                cmpd(5, vals == expset,
                     [6, 'U1', x, z, k, sorted(vals), sorted(expset)])
            clear()

    # -------- D7: published anchors (byte-faithful transcription) ----------
    # (a,b,c) K1308 D8 triple box: theorem instance (published as obs there)
    for a in range(1, 9):
        for b in range(a + 1, 9):
            for c in range(b + 1, 9):
                S = a + b + c
                for z in range(0, 6):
                    for k in range(z + 2, z + 6):
                        h = H_canonical(S + k, (a, b, c), z)
                        exp = csum(3, z, k, (a, b, c))
                        if TAMPER == 'ps':
                            exp = flipC(exp)
                        cmpd(6, h == exp, [7, 'tri', a, b, c, z, k, h])
                    clear()
    for a in range(1, 8):
        for b in range(a + 1, 8):
            for (x, y, w) in ((a, a, b), (a, b, b)):
                S = x + y + w
                for z in range(0, 5):
                    for k in range(z + 2, z + 6):
                        h = H_canonical(S + k, (x, y, w), z)
                        exp = csum(3, z, k, (x, y, w))
                        if TAMPER == 'ps':
                            exp = flipC(exp)
                        cmpd(6, h == exp, [7, 'mix', x, y, w, z, k, h])
                    clear()
    for a in range(1, 7):
        for b in range(a + 1, 7):
            for c in range(b + 1, 7):
                for d in range(c + 1, 7):
                    S = a + b + c + d
                    for z in range(0, 3):
                        for k in range(z + 3, z + 7):
                            h = H_canonical(S + k, (a, b, c, d), z)
                            exp = csum(4, z, k, (a, b, c, d))
                            if TAMPER == 'ps':
                                exp = flipC(exp)
                            cmpd(6, h == exp, [7, 'quad', a, b, c, d, z, k, h])
                        clear()
    # K1308 D1 T-UH tail box (transcription, [g odd] = [S odd] for pairs)
    for z in range(0, 8):
        for m in range(1, 11):
            for g in range(1, 13):
                for k in range(z + 1, z + 7):
                    Xd = tuple(sorted([m, m + g], reverse=True))
                    h = H_canonical(2 * m + g + k, Xd, z)
                    exp = csum(2, z, k, Xd)
                    if TAMPER == 'ps':
                        exp = flipC(exp)
                    cmpd(6, h == exp, [7, 'tuh', z, m, g, k, h])
            clear()
    # L-SB spot (transcription of the published K1308 L-SB readings)
    for x in range(2, 13):
        for p in range(1, 7):
            for j in range(p, p + 4):
                R = x + j
                exp = x % 2
                if TAMPER == 'ps':
                    exp = flipC(exp)
                a1 = single_token(x, p, R)
                cmpd(6, a1 == exp == vC(x, p, R) == vO(x, p, R),
                     [7, 'lsb', x, p, j, a1])
        clear()

    # -------- D8: cross-engine canonical vs ordered AND claim --------------
    for (n, hi, zs) in ((3, 5, (0, 3, 7, 11)), (4, 4, (0, 4, 9)),
                        (2, 6, (0, 5, 10))):
        for z in zs:
            for X in multisets(n, hi):
                S = sum(X)
                Xd = tuple(sorted(X, reverse=True))
                for k in (z + n - 1, z + n + 1):
                    exp = csum(n, z, k, Xd)
                    if TAMPER == 'ce':
                        exp = flipC(exp)
                    hc = H_canonical(S + k, Xd, z)
                    ho = H_ordered(S + k, Xd, z)
                    cmpd(7, hc == ho == exp, [8, n, z, Xd, k, hc, ho, exp])
            clear()

    # -------- D9: sharpness witnesses (boundary row k=z+n-2) ---------------
    WitnessList = [('n3', 3, WIT_N3), ('n4', 4, WIT_N4), ('n5', 5, WIT_N5),
                  ('n6', 6, WIT_N6), ('n7', 7, WIT_N7)]
    obs['sharpness_witnesses'] = {}
    for (tag, n, wl) in WitnessList:
        nb = 0
        for (X, z, k, hrec, claim) in wl:
            Xd = tuple(sorted(X, reverse=True))
            S = sum(Xd)
            assert k == z + n - 2
            exp = (hrec + 1) % 3 if TAMPER == 'sw' else hrec
            h = H_canonical(S + k, Xd, z)
            ok = (h == exp) and (h != claim)
            cmpd(8, ok, [9, tag, Xd, z, k, h, hrec, claim])
            nb += 1
        obs['sharpness_witnesses'][tag] = nb
        clear()

    # -------- D10: OBS near-threshold tables (NO claim) ---------------------
    obs['OBS_near_threshold_dist_n3'] = {}
    for z in range(0, 11):
        d = {}
        for X in multisets(3, 6):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            h = H_canonical(S + z + 1, Xd, z)
            d[h] = d.get(h, 0) + 1
        clear()
        exp = {int(kk): vv for kk, vv in E7_N3[str(z)].items()}
        cmpd(9, d == exp, [10, 'n3', z, d, exp])
        obs['OBS_near_threshold_dist_n3'][z] = d
    obs['OBS_near_threshold_dist_n4'] = {}
    for z in range(0, 9):
        d = {}
        for X in multisets(4, 5):
            S = sum(X)
            Xd = tuple(sorted(X, reverse=True))
            h = H_canonical(S + z + 2, Xd, z)
            d[h] = d.get(h, 0) + 1
        clear()
        exp = {int(kk): vv for kk, vv in E7_N4[str(z)].items()}
        cmpd(9, d == exp, [10, 'n4', z, d, exp])
        obs['OBS_near_threshold_dist_n4'][z] = d
    for (tag, n, zmax, amax) in (('n3', 3, 12, 9), ('n4', 4, 10, 9),
                                 ('n5', 5, 8, 8)):
        for koff in range(0, n):
            nb = 0
            tot = 0
            for z in range(0, zmax + 1):
                for a in range(1, amax + 1):
                    X = tuple([a] * n)
                    S = n * a
                    h = H_canonical(S + z + koff, X, z)
                    tot += 1
                    nb += 0 if h == S % 2 else 1
                clear()
            exp = list(E8_PURE[tag]['koff%d' % koff])
            if TAMPER == 'ob' and tag == 'n4' and koff == 1:
                exp = [exp[0], exp[1] - 1]   # single corrupted frozen value
            cmpd(9, [tot, nb] == exp, [10, 'pure', tag, koff, [tot, nb], exp])
        clear()

    # -------- D11: T-DB interlock (published K1311 boundary law) -----------
    for (tag, n, wl) in WitnessList:
        for (X, z, k, hrec, claim) in wl:
            Xd = tuple(sorted(X, reverse=True))
            S = sum(Xd)
            E = 2 * Xd[0] - S
            exp = Dlaw(E, k)
            if TAMPER == 'db':
                exp = (exp + 1) % 3
            h = H_canonical(S + k, Xd, z)
            cmpd(10, h == exp, [11, tag, Xd, z, k, h, exp, E])
        clear()

    # -------- D12: sharpness construction (Corollary C-SHARP) --------------
    for n in range(2, 12):
        for z in range(0, 7):
            k = z + n - 2
            # family 1: E = z+n >= k+2 -> boundary value 1-[S odd]
            X = tuple([z + 2 * n - 1] + [1] * (n - 1))
            S = sum(X)
            h = H_canonical(S + k, X, z)
            E = 2 * X[0] - S
            exp = Dlaw(E, k)
            assert E >= k + 2
            ok = (h == exp) and (h == 1 - (S % 2))
            if TAMPER == 'sc':
                ok = False
            cmpd(11, ok, [12, 'f1', n, z, k, h, exp, S % 2])
            # family 2: E = k+1 -> boundary value 2
            X = tuple([z + 2 * n - 2] + [1] * (n - 1))
            S = sum(X)
            h = H_canonical(S + k, X, z)
            E = 2 * X[0] - S
            assert E == k + 1
            ok = (h == Dlaw(E, k)) and (h == 2)
            if TAMPER == 'sc':
                ok = False
            cmpd(11, ok, [12, 'f2', n, z, k, h, 2])
            clear()

    info = {'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'elapsed_s': round(time.time() - t0, 1)}
    info['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['obs'] = obs
    res['battery_names'] = ['D1_census_n3', 'D2_census_n4_far', 'D3_census_n5',
                            'D4_census_n67_far', 'D5_typed_selfcheck',
                            'D6_base_lemmas', 'D7_published_anchors',
                            'D8_cross_engine', 'D9_sharpness_witnesses',
                            'D10_obs_tables', 'D11_tdb_interlock',
                            'D12_sharp_construction']
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)


main()

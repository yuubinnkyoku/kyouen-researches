#!/usr/bin/env python3
"""explore_k1314: FROZEN pre-declaration exploration for the K1314 packet
(second below-band row k = z+n-4, all n>=3; base lemmas L-2 / PB2 / L-BR2 / L-0).

Waves (deterministic output, JSON on stdout; frozen as explore_k1314.out):
  WA  collapse census: value of the row as a function of (E, w), w = E+z+n-5,
      merged over n=3..6: multivalue cells must be exactly {(-1,-3), (-1,-2)}
      with the all-ones split reported.
  WB  T-BB2 wide census (n=3..7) vs claim, exceptions included.
  WC  base-lemma fits: L-2 (pairs g<=14 m<=11 Z<=14, beds a<=13 Z<=14),
      PB2 (a,b<=15), L-BR2 (x<=29, Z<=19), L-0 (R<=7, z<=7).
  WD  typed-children closure: children built ONLY from the claim tables,
      mex == claim == engine (n=3..6 band cells, n=2 planes, plane-0 pairs,
      single tokens).
  WE  region-structure witnesses: the exact 2-line families (s+1,1,1) at
      E = s-1 (z = sweep, line hits at E = z for n=3), deep negative-E
      families (a^n), (a+1,a^{n-1}) z<=40.
  WF  K0832 conjecture-A interface slice: X = (y+w+z+j, y, w) on the row
      (R = S+z-1): j=0 must be all-2 (the conjecture's 2-line), j>=1
      region III, j<=-1 region I; plus the (1,1,1) exception accounting.
  WG  seeded random sweep (seed 1314).

Claims under exploration (machine mirrors of the hand proofs in the
single-owner declaration note):
  T-BB2 (n>=3, row k=z+n-4):
      E <= z+n-4          -> [E odd]
      E == z+n-3          -> 2
      E >= z+n-2          -> 1 - [E odd]
      exceptions: X=(1,1,1): z=0 -> 0, z=1 -> 2   (forced by the L-2 bed
      corner; z>=2 rejoins the generic law because 1 XOR 2 = 3)
  L-2 (n=2, plane Z>=1, row k=Z-2):
      beds (a,a): 2 iff (a,Z)=(1,1), else 0
      pairs (m+g,m), g>=1: Z<=g-2 -> [g even]; Z==g-1 -> 2; Z>=g -> [g odd]
  PB2 (n=2, plane 0, row k=-2): g<=2 -> [g odd]; g==3 -> 2; g>=4 -> [g even]
  L-BR2 (n=1, plane Z>=0, row k=Z-3): R=0 -> 0;
      2 at (Z==x>=2) or (1,3) or (3,1); Z>=x+1 -> [x odd]; Z<=x-1 -> [x even]
  L-0 (empty multiset): identically 0.
"""
import json, sys, random
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
import hashlib
sha = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
assert sha == PIN, sha
exec(ENGINE_BLOCK)


def E_of(X):
    return 2 * X[0] - sum(X)


def TB2(Xd, z):
    n = len(Xd)
    E = E_of(Xd)
    if Xd == (1, 1, 1) and z in (0, 1):
        return 0 if z == 0 else 2
    if E <= z + n - 4:
        return E % 2
    if E == z + n - 3:
        return 2
    return 1 - (E % 2)


def L2(kid, Z):
    a, b = kid
    g = a - b
    if g == 0:
        return 2 if (a, Z) == (1, 1) else 0
    if Z == g - 1:
        return 2
    if Z <= g - 2:
        return 1 if g % 2 == 0 else 0
    return 1 if g % 2 == 1 else 0


def PB2(kid):
    g = kid[0] - kid[1]
    if g <= 2:
        return g % 2
    if g == 3:
        return 2
    return 1 if g % 2 == 0 else 0


def LBR2(x, Z):
    R = x + Z - 3
    if R == 0:
        return 0
    if Z == x and x >= 2:
        return 2
    if (x, Z) == (1, 3):
        return 2
    if (x, Z) == (3, 1):
        return 2
    if Z >= x + 1:
        return x % 2
    return 1 if x % 2 == 0 else 0


def claim_any(n, Xd, z):
    if n == 0:
        return 0
    if n == 1:
        return LBR2(Xd[0], z)
    if n == 2:
        if z == 0:
            return PB2(Xd)
        return L2(Xd, z)
    return TB2(Xd, z)


def multisets(n, hi):
    return list(combinations_with_replacement(range(1, hi + 1), n))


def typed_kids(n, Xd, z, k):
    kids = []
    R = sum(Xd) + k
    if R == 0:
        return None
    for i, v in enumerate(Xd):
        if v > 1:
            kid = tuple(sorted(Xd[:i] + (v - 1,) + Xd[i + 1:], reverse=True))
            kids.append(claim_any(n, kid, z))
        else:
            kid = tuple(sorted(Xd[:i] + Xd[i + 1:], reverse=True))
            kids.append(0 if len(kid) == 0 else claim_any(len(kid), kid, z + 1))
    if z >= 1:
        kids.append(1 ^ claim_any(n, Xd, z - 1))
    return kids


def mexs(vals):
    s = set(vals)
    x = 0
    while x in s:
        x += 1
    return x


def main():
    out = {}

    # ---- WA: (E,w) collapse census ---------------------------------------
    from collections import defaultdict
    amb = defaultdict(set)
    allones = defaultdict(dict)   # (E,w) -> {z: value} for X=(1^n) families
    generic = defaultdict(set)
    for n, hi, zmax in ((3, 9, 12), (4, 7, 11), (5, 6, 10), (6, 5, 9)):
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
                amb[(E, w)].add(v)
                if all(t == 1 for t in Xd):
                    allones[(E, w)][z] = v
                else:
                    generic[(E, w)].add(v)
            H_canonical.cache_clear()
    multi = {f'{k[0]},{k[1]}': sorted(v) for k, v in sorted(amb.items()) if len(v) > 1}
    out['WA'] = {
        'cells': len(amb),
        'multivalue_cells': multi,
        'exception_cells_expected': {'-1,-3': [0, 1], '-1,-2': [1, 2]},
        'allones_values': {f'{k[0]},{k[1]}': v for k, v in allones.items()
                           if k in ((-1, -3), (-1, -2))},
        'generic_values_at_exception_cells':
            {f'{k[0]},{k[1]}': sorted(v) for k, v in generic.items()
             if k in ((-1, -3), (-1, -2))},
        'collapse_OK': multi == {'-1,-3': [0, 1], '-1,-2': [1, 2]},
    }

    # ---- WB: T-BB2 wide census ------------------------------------------
    bad = 0
    cnt = 0
    per = {}
    for n, hi, zmax in ((3, 11, 16), (4, 9, 14), (5, 7, 12), (6, 6, 11), (7, 5, 10)):
        b = 0
        for X in multisets(n, hi):
            Xd = tuple(sorted(X, reverse=True))
            S = sum(Xd)
            for z in range(0, zmax + 1):
                k = z + n - 4
                v = H_canonical(S + k, Xd, z)
                e = TB2(Xd, z)
                cnt += 1
                if v != e:
                    b += 1
            H_canonical.cache_clear()
        per[f'n{n}'] = b
        bad += b
    out['WB'] = {'cells': cnt, 'bad': bad, 'per_n': per}

    # ---- WC: base-lemma fits ---------------------------------------------
    res = {}
    b = c = 0
    for g in range(1, 15):
        for m in range(1, 12):
            for Z in range(1, 15):
                Xd = (m + g, m)
                v = H_canonical(2 * m + g + Z - 2, Xd, Z)
                e = L2(Xd, Z)
                c += 1
                b += 0 if v == e else 1
    for a in range(1, 14):
        for Z in range(1, 15):
            Xd = (a, a)
            v = H_canonical(2 * a + Z - 2, Xd, Z)
            e = L2(Xd, Z)
            c += 1
            b += 0 if v == e else 1
    res['L2'] = {'cells': c, 'bad': b}
    b = c = 0
    for a in range(1, 16):
        for b2 in range(1, a + 1):
            Xd = (a, b2)
            v = H_canonical(a + b2 - 2, Xd, 0)
            e = PB2(Xd)
            c += 1
            b += 0 if v == e else 1
    res['PB2'] = {'cells': c, 'bad': b}
    b = c = 0
    st = 0
    for x in range(1, 30):
        for Z in range(0, 20):
            R = x + Z - 3
            if R < 0:
                continue
            v = H_canonical(R, (x,), Z)
            e = LBR2(x, Z)
            s = single_token(x, Z, R)
            c += 1
            if v == e == s:
                pass
            else:
                b += 1
            st += 1
    res['LBR2'] = {'cells': c, 'bad': b, 'published_K0832_slice_also': st}
    b = c = 0
    for R in range(0, 8):
        for z in range(0, 8):
            if R > 0:
                v = H_canonical(R, (), z)
            else:
                v = 0
            c += 1
            b += 0 if v == 0 else 1
    res['L0'] = {'cells': c, 'bad': b}
    out['WC'] = res

    # ---- WD: typed closure ------------------------------------------------
    b = c = 0
    ex = []
    for n, hi, zmax in ((3, 8, 8), (4, 6, 7), (5, 5, 6), (6, 5, 6)):
        for X in multisets(n, hi):
            Xd = tuple(sorted(X, reverse=True))
            S = sum(Xd)
            for z in range(0, zmax + 1):
                k = z + n - 4
                R = S + k
                if R <= 0:
                    continue
                kids = typed_kids(n, Xd, z, k)
                if kids is None:
                    continue
                mx = mexs(kids)
                h = H_canonical(R, Xd, z)
                e = claim_any(n, Xd, z)
                c += 1
                if not (mx == e == h):
                    b += 1
                    if len(ex) < 5:
                        ex.append([n, Xd, z, kids, mx, e, h])
            H_canonical.cache_clear()
    for Z in range(1, 9):
        for a in range(1, 8):
            for g in range(0, 8):
                Xd = (a + g, a)
                k = Z - 2
                R = sum(Xd) + k
                if R <= 0:
                    continue
                kids = typed_kids(2, Xd, Z, k)
                mx = mexs(kids)
                h = H_canonical(R, Xd, Z)
                e = claim_any(2, Xd, Z)
                c += 1
                if not (mx == e == h):
                    b += 1
                    if len(ex) < 8:
                        ex.append([2, Xd, Z, kids, mx, e, h])
        H_canonical.cache_clear()
    for a in range(1, 9):
        for b2 in range(1, a + 1):
            Xd = (a, b2)
            R = a + b2 - 2
            if R <= 0:
                continue
            kids = typed_kids(2, Xd, 0, -2)
            mx = mexs(kids)
            h = H_canonical(R, Xd, 0)
            e = PB2(Xd)
            c += 1
            if not (mx == e == h):
                b += 1
                ex.append([2, Xd, 0, kids, mx, e, h])
    H_canonical.cache_clear()
    for x in range(1, 10):
        for Z in range(0, 10):
            R = x + Z - 3
            if R <= 0:
                continue
            kids = typed_kids(1, (x,), Z, Z - 3)
            mx = mexs(kids)
            h = H_canonical(R, (x,), Z)
            e = LBR2(x, Z)
            c += 1
            if not (mx == e == h):
                b += 1
                ex.append([1, (x,), Z, kids, mx, e, h])
    H_canonical.cache_clear()
    out['WD'] = {'cells': c, 'bad': b, 'examples': ex}

    # ---- WE: region-structure witnesses ------------------------------------
    b = c = 0
    per = {}
    s_line = 0
    for s in range(1, 25):           # X=(s+1,1,1): E=s-1, n=3, exact 2-line at z=s-1
        Xd = (s + 1, 1, 1)
        S = s + 3
        for z in range(0, 27):
            k = z - 1
            v = H_canonical(S + k, Xd, z)
            e = TB2(Xd, z)
            c += 1
            if E_of(Xd) == z:
                s_line += 1
            b += 0 if v == e else 1
        H_canonical.cache_clear()
    per['dominant_family_linehits'] = s_line
    for n in (3, 4, 5):
        for a in range(1, 7):
            Xe = tuple(sorted([a] * n, reverse=True))
            Xn = tuple(sorted([a + 1] + [a] * (n - 1), reverse=True))
            for Xd in (Xe, Xn):
                for z in range(0, 41):
                    k = z + n - 4
                    v = H_canonical(sum(Xd) + k, Xd, z)
                    e = TB2(Xd, z)
                    c += 1
                    b += 0 if v == e else 1
                H_canonical.cache_clear()
    for a in range(2, 9):
        for b2 in range(1, 7):       # (a,a,b): E=-b family
            Xd = (a, a, b2)
            for z in range(0, 31):
                Xd = tuple(sorted((a, a, b2), reverse=True))
                if Xd[0] != a:
                    continue
                k = z - 1
                v = H_canonical(sum(Xd) + k, Xd, z)
                e = TB2(Xd, z)
                c += 1
                b += 0 if v == e else 1
            H_canonical.cache_clear()
    out['WE'] = {'cells': c, 'bad': b, 'per': per}

    # ---- WF: K0832 conjecture-A interface -----------------------------------
    res = {'j0_two_cells': 0, 'j0_bad': 0, 'other_bad': 0, 'cells': 0}
    for j in range(-4, 5):
        for z in range(0, 11):
            for y in range(1, 5):
                for w in range(1, 5):
                    x = y + w + z + j
                    if x < y or x < w or x < 1:
                        continue
                    if not (x >= y >= w):
                        x, y2, w2 = sorted((x, y, w), reverse=True)
                    else:
                        y2, w2 = y, w
                    Xd = (x, y2, w2)
                    S = x + y2 + w2
                    R = S + z - 1           # the row k = z+n-4 with n=3
                    if R < 0:
                        continue
                    v = H_canonical(R, Xd, z)
                    e = TB2(Xd, z)
                    res['cells'] += 1
                    if E_of(Xd) == z:      # j == 0 exactly when E == z
                        res['j0_two_cells'] += 1
                        if v != 2 or e != 2:
                            res['j0_bad'] += 1
                    elif v != e:
                        res['other_bad'] += 1
            H_canonical.cache_clear()
    res['all_ok'] = (res['j0_bad'] == 0 and res['other_bad'] == 0)
    out['WF'] = res

    # ---- WG: seeded random ---------------------------------------------------
    rng = random.Random(1314)
    b = c = 0
    for _ in range(400):
        n = rng.randint(3, 7)
        z = rng.randint(0, 12)
        maxh = {3: 13, 4: 11, 5: 9, 6: 8, 7: 7}[n]
        heaps = [rng.randint(1, maxh) for _ in range(n)]
        Xd = tuple(sorted(heaps, reverse=True))
        S = sum(Xd)
        k = z + n - 4
        v = H_canonical(S + k, Xd, z)
        e = TB2(Xd, z)
        c += 1
        b += 0 if v == e else 1
        if _ % 25 == 24:
            H_canonical.cache_clear()
    H_canonical.cache_clear()
    out['WG'] = {'cells': c, 'bad': b}

    ok = (out['WA']['collapse_OK'] and out['WB']['bad'] == 0
          and out['WC']['L2']['bad'] == 0 and out['WC']['PB2']['bad'] == 0
          and out['WC']['LBR2']['bad'] == 0 and out['WC']['L0']['bad'] == 0
          and out['WD']['bad'] == 0 and out['WE']['bad'] == 0
          and out['WF']['all_ok'] and out['WG']['bad'] == 0)
    out['ALL_WAVES_OK'] = ok
    print(json.dumps(out, indent=1, sort_keys=True))


main()

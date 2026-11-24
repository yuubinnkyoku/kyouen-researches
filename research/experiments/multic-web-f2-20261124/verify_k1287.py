#!/usr/bin/env python3
"""verify_k1287: machine audit for the multi-c web F2 spread package.

Position convention (identical to the published chain since K1138):
H(R, X, z) where X is a token multiset (sorted descending tuple), R the
remaining budget, z the plane; moves: A(v>1 -> v-1, R-1), B(v==1 removed,
z+1, R-1), C(z>=1 -> same X, z-1, R-1); Grundy value = mex of option values.

Family points (min gap band of the spread web future F2, multi-c):
  W(d,c,m)  X={m,(m+d)^c}             budget 2m+d+2+z
  D(d,c,m)  X={m,m+d-1,(m+d)^(c-1)}   budget 2m+d+1+z
  E(d,c,m)  X={m,m+d-2,(m+d)^(c-1)}   budget 2m+d+z      (d>=3)
  Ap(d,c,m) X={m,(m+d-1)^2,(m+d)^(c-2)} budget 2m+d+z    (d>=2, c>=2)
  A(m,s)    X={m^2,(m+1)^s}          budget 2m+2+z
  Am(m,h,s) X={m^2,(m+h)^s}          budget 2m+2+z      (frontier)
  SLB2 x^c@(x+3) z2, SLB3 x^c@(x+4) z3, L {d,(d+1)^s}@(d+2+z) plane z+1

Gates (all finite censuses; universal status per the declaration note:
D8 identities are algebraic theorems proved in the note, all value laws
are CONJECTURES verified on the census boxes, published items are
re-checked as consistency rows):
  D1 W-law    z in {0,1,2}, d 1..8, c 2..6, m 1..10
  D2 D-law    z in {0,1,2}, d 2..8, c 2..6, m 1..10
  D3 E-law    z in {0,1,2}, d 3..8, c 2..6, m 1..9
  D4 Ap-law   z in {0,1,2}, d 2..8, c 3..7, m 1..9
  D5 A-law    z in {0,1,2}, s 0..6, m 1..12
  D6 frontier obs: Am h2..5 m1..8 / SLB2/3 x2..12 c1..8 / L zp{0,1} d1..8
  D7 published consistency: pure-c1 ladders [d odd] (K1285 T-L),
     D-c1 pair slices via K1285 T-PS, T-ALM floors,
     C-PC (x^c)@(x+1) z0, C-PB2 (x^c)@(x+2) z1
  D8 T-RC child identities (engine-free position algebra):
     I1  A-top(W_z)     = D_z            (all d, c>=2)
     I2  A-min(W_z)     = W_z(d+1,c,m-1) (m>=2)
     I3  C(W_z)         = W_(z-1)(d,c,m) (z>=1)
     I4  A-mid(D_z)     = E_z            (d>=3)
     I5  A-top(D_z)     = Ap_z           (d>=2, c>=2)
     I6  C(D_z)         = D_(z-1)
     I7  C(E_z)         = E_(z-1)
     I8  C(Ap_z)        = Ap_(z-1)
     I9  C(A_z)         = A_(z-1)
     I10 B-min(D_z(d,c,m=1)) = L-point {d,(d+1)^(c-1)}@(d+2+z) plane z+1
     I11 B-min(W_z(d,c,m=1)) = ((m+d)^c, budget (m+d)+2+z, plane z+1)
  D9 mex fixed point: law value == H(point) == mex(engine children)
     for W/D/E/Ap/A box points
  D10 cross-engine canonical vs ordered on web spot points
  D11 published K0832 single-token closed form vs both engines

Engine block embedded verbatim from the published K1138/K1282/K1283/K1284/
K1285 chain, sha256-gated at startup. TAMPER modes: --tamper-engine (rc 2),
--tamper=wlaw|dlaw|elaw|aplaw|alaw|amlaw|identity|mex (rc 1; per-flag
expected bad counts pre-declared in the note). Determinism: official runs
are byte-identical on stdout (volatile timestamps on stderr only).
"""
import json, hashlib, sys, time
from functools import lru_cache

ENGINE_BLOCK = 'def mex(values):\n    values = set(values)\n    m = 0\n    while m in values:\n        m += 1\n    return m\n\n# ------------------------------------------------------------------\n# Raw engines (verbatim from the published K1138 verifier block; the same\n# transcription is embedded in the published y22 machine K1257).\n# ------------------------------------------------------------------\n@lru_cache(maxsize=6_000_000)\ndef H_ordered(R, X, z):\n    if R == 0:\n        return 0\n    opts = set()\n    for i, v in enumerate(X):\n        if v > 1:\n            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))\n        else:\n            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))\n    if z >= 1:\n        opts.add(1 ^ H_ordered(R - 1, X, z - 1))\n    return mex(opts)\n\n@lru_cache(maxsize=6_000_000)\ndef H_canonical(R, X, z):\n    X = tuple(sorted(X, reverse=True))\n    if R == 0:\n        return 0\n    opts = set()\n    i = 0\n    while i < len(X):\n        v = X[i]\n        if v > 1:\n            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))\n            opts.add(H_canonical(R - 1, child, z))\n        else:\n            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))\n            opts.add(H_canonical(R - 1, child, z + 1))\n        while i + 1 < len(X) and X[i + 1] == v:\n            i += 1\n        i += 1\n    if z >= 1:\n        opts.add(1 ^ H_canonical(R - 1, X, z - 1))\n    return mex(opts)\n\ndef vC(x, z, R):  # canonical-engine single token\n    return H_canonical(R, (x,), z)\ndef vO(x, z, R):  # ordered-engine single token\n    return H_ordered(R, (x,), z)\n\n# ------------------------------------------------------------------\n# Published K0832 single-token closed form (transcription of the published\n# single_token block in the y22 machine K1257; see report provenance).\n# ------------------------------------------------------------------\ndef q_odd(k):\n    return k if k % 2 else k - 1\n\ndef single_token(x, z, R):\n    if R == 0 or x <= 0:\n        return 0\n    if z == 0:\n        return min(R, x) % 2\n    if z == x:\n        if R % 2 and R <= 2 * x - 1:\n            return 2\n        if R % 2 == 0 and R <= x - 1:\n            return 0\n        return x % 2\n    if 1 <= z <= x - 1:\n        m = q_odd(z)\n        if R <= m:\n            return 2 if R % 2 else 0\n        if m < R < x + z:\n            return (R + z) % 2\n        return x % 2\n    if z >= x + 1:\n        m = q_odd(x)\n        if R <= m:\n            return 2 if R % 2 else 0\n        return x % 2\n    raise ValueError((x, z, R))\n'

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
H = H_canonical

TAMPER = None
for a in sys.argv[1:]:
    if a.startswith('--tamper='):
        TAMPER = a.split('=', 1)[1]

def clear():
    H_canonical.cache_clear(); H_ordered.cache_clear()

# ------------------------------------------------------------------ families
def S(xs):
    return tuple(sorted(xs, reverse=True))

def XW(m, d, c):   return S([m] + [m + d] * c)
def XD(m, d, c):   return S([m, m + d - 1] + [m + d] * (c - 1))
def XE(m, d, c):   return S([m, m + d - 2] + [m + d] * (c - 1))
def XAp(m, d, c):  return S([m] + [m + d - 1] * 2 + [m + d] * (c - 2))
def XA(m, s):      return S([m, m] + [m + 1] * s)
def XAm(m, h, s):  return S([m, m] + [m + h] * s)

def RW(z, d, c, m):  return 2 * m + d + 2 + z
def RD(z, d, c, m):  return 2 * m + d + 1 + z
def RE(z, d, c, m):  return 2 * m + d + z
def RAp(z, d, c, m): return 2 * m + d + z
def RA(z, m, s):     return 2 * m + 2 + z

# ------------------------------------------------------------------ value laws
def WL(z, d, c, m):
    # multi-c web main band, c >= 2; conjecture (census-verified), see note
    if z == 1:
        if TAMPER == 'wlaw':
            return 1 if d % 2 else 0        # flipped (wrong d-parity)
        return 1 if d % 2 == 0 else 0
    if d == 1:
        if z == 2 and m == 1:
            return 2
        if c == 2:
            return 0
        return 2
    return 1 if d % 2 == 0 else 0

def DL(z, d, c, m):
    if z == 1:
        return 1 if d % 2 == 1 else 0
    if d == 2:
        if z == 2 and m == 1 and c == 2:
            return 0
        return 2
    if TAMPER == 'dlaw':
        return 1 if d % 2 == 0 else 0        # flipped for d>=3
    return 1 if d % 2 == 1 else 0

def EL(z, d, c, m):
    if d % 2 == 0:
        return 1
    if TAMPER == 'elaw':
        return 2                            # pre-fix wrong law (odd d -> 2)
    if d == 3:
        return 0 if z == 1 else 2
    return 0

def ApL(z, d, c, m):
    if TAMPER == 'aplaw':
        return 1 if d % 2 == 1 else 0        # flipped
    return 1 if d % 2 == 0 else 0

def AL(z, m, s):
    if z == 0:
        if TAMPER == 'alaw':
            return 0 if s == 1 else 1        # flipped (z0 plane)
        return 1 if s == 1 else 0
    if z == 2:
        if m == 1:
            return 0
        return 1 if s == 1 else 0
    # z == 1
    if s == 0:
        return 0
    if m == 1:
        return 2
    if s == 1:
        return 1
    return 2

def AmL(z, m, h, s):
    # h >= 2 rows (h == 1 is the A family, covered by AL); census-verified obs
    if z == 0:
        return 0
    if z == 1:
        if TAMPER == 'amlaw':
            return 1 if s >= 1 else 0       # wrong value (1 instead of 2)
        return 2 if s >= 1 else 0
    # z == 2
    if TAMPER == 'amlaw':
        return 1 if (m == 1 and h == 2 and s == 1) else 0
    return 1 if (m == 1 and h == 2 and s == 1) else 0

def SLB2L(x, c):
    if x == 2:
        if c == 1: return 0
        if c == 2: return 2
        return 1
    if c == 1:
        return 1 if x % 2 == 1 else 0
    return 1 if x % 2 == 0 else 0

def SLB3L(x, c):
    if x == 2:
        if c <= 2: return 0
        return 1
    if c == 1:
        return 1 if x % 2 == 1 else 0
    return 1 if x % 2 == 0 else 0

def LL(zplane, d, s):
    # plane zz := zplane + 1, budget d + 2 + zplane
    if d == 1 and zplane == 0:
        return 2
    if d == 1 and zplane == 1:
        return 1 if s == 1 else 0
    return 1 if d % 2 == 0 else 0

# ---------------------------------------------------------------- identity
def child_A(X, v):
    i = X.index(v)
    return S(X[:i] + (v - 1,) + X[i + 1:])

def child_B(X, v):
    i = X.index(v)
    return S(X[:i] + X[i + 1:])

def main():
    t0 = time.time()
    res = {'kit': 'verify_k1287', 'engine_sha': ENGINE_SHA,
           'engine_gate': 'PASS', 'tamper': TAMPER}
    ND = 11
    counts = [0] * ND
    bad = [0] * ND
    ex = [[] for _ in range(ND)]

    def rec(gate, tag, params, got, want):
        counts[gate] += 1
        if got != want:
            bad[gate] += 1
            if len(ex[gate]) < 6:
                ex[gate].append([gate, tag] + list(params) + [got, want])

    # ---------------- D1 W-law
    for z in (0, 1, 2):
        for d in range(1, 9):
            for c in range(2, 7):
                for m in range(1, 11):
                    v = H(RW(z, d, c, m), XW(m, d, c), z)
                    rec(0, 'W', (z, d, c, m), v, WL(z, d, c, m))
        clear()

    # ---------------- D2 D-law
    for z in (0, 1, 2):
        for d in range(2, 9):
            for c in range(2, 7):
                for m in range(1, 11):
                    v = H(RD(z, d, c, m), XD(m, d, c), z)
                    rec(1, 'D', (z, d, c, m), v, DL(z, d, c, m))
        clear()

    # ---------------- D3 E-law
    for z in (0, 1, 2):
        for d in range(3, 9):
            for c in range(2, 7):
                for m in range(1, 10):
                    v = H(RE(z, d, c, m), XE(m, d, c), z)
                    rec(2, 'E', (z, d, c, m), v, EL(z, d, c, m))
        clear()

    # ---------------- D4 Ap-law
    for z in (0, 1, 2):
        for d in range(2, 9):
            for c in range(3, 8):
                for m in range(1, 10):
                    v = H(RAp(z, d, c, m), XAp(m, d, c), z)
                    rec(3, 'Ap', (z, d, c, m), v, ApL(z, d, c, m))
        clear()

    # ---------------- D5 A-law
    for z in (0, 1, 2):
        for s in range(0, 7):
            for m in range(1, 13):
                v = H(RA(z, m, s), XA(m, s), z)
                rec(4, 'A', (z, m, s), v, AL(z, m, s))
        clear()

    # ---------------- D6 frontier observations
    for z in (0, 1, 2):
        for h in range(2, 6):
            for s in range(0, 6):
                for m in range(1, 9):
                    v = H(RA(z, m, s), XAm(m, h, s), z)
                    rec(5, 'Am', (z, m, h, s), v, AmL(z, m, h, s))
        clear()
    for x in range(2, 13):
        for c in range(1, 9):
            v = H(x + 3, S([x] * c), 2)
            rec(5, 'SLB2', (x, c), v, SLB2L(x, c))
        clear()
    for x in range(2, 13):
        for c in range(1, 9):
            v = H(x + 4, S([x] * c), 3)
            rec(5, 'SLB3', (x, c), v, SLB3L(x, c))
        clear()
    for zp in (0, 1):
        for d in range(1, 9):
            for s in range(1, 6):
                v = H(d + 2 + zp, S([d] + [d + 1] * s), zp + 1)
                rec(5, 'L', (zp, d, s), v, LL(zp, d, s))
        clear()

    # ---------------- D7 published consistency
    for z in (0, 1, 2):
        for d in range(1, 9):
            for m in range(1, 13):
                v = H(2 * m + d + 2 + z, XW(m, d, 1), z)
                rec(6, 'c1-ladder', (z, d, m), v, 1 if d % 2 == 1 else 0)
        clear()
    for z in (0, 1, 2):
        for d in range(2, 9):
            for m in range(1, 11):
                v = H(2 * m + d + 1 + z, S([m, m + d - 1]), z)
                want = 1 if d % 2 == 0 else 0   # K1285 T-PS via g=d-1
                rec(6, 'D-c1-PS', (z, d, m), v, want)
        clear()
    for m in range(1, 13):
        XX = S([m, m])
        floors = [(2 * m + 2, 0), (2 * m + 3, 0), (2 * m + 2, 1),
                  (2 * m + 3, 1), (2 * m + 3, 2), (2 * m + 4, 2)]
        for (rr, zz) in floors:
            v = H(rr, XX, zz)
            rec(6, 'T-ALM', (m, rr, zz), v, 0)
        clear()
    for x in range(2, 13):
        for c in range(1, 7):
            v = H(x + 1, S([x] * c), 0)
            want = (1 if x % 2 == 1 else 0) if c == 1 else (1 if x % 2 == 0 else 0)
            rec(6, 'C-PC', (x, c), v, want)
        clear()
    for x in range(2, 13):
        for c in range(1, 7):
            v = H(x + 2, S([x] * c), 1)
            want = (1 if x % 2 == 1 else 0) if c == 1 else (1 if x % 2 == 0 else 0)
            rec(6, 'C-PB2', (x, c), v, want)
        clear()

    # ---------------- D8 T-RC child identities (engine-free)
    def ident(gate, tag, params, child, declared):
        # child: (X, R, plane) constructed by the move; declared likewise
        rec(gate, tag, params, child, declared)

    for z in (0, 1, 2):
        for d in range(1, 7):
            for c in range(2, 6):
                for m in range(1, 8):
                    X = XW(m, d, c); R = RW(z, d, c, m)
                    tgt = XE(m, d, c) if (TAMPER == 'identity' and d >= 3) else XD(m, d, c)
                    ident(7, 'I1', (z, d, c, m),
                          (child_A(X, m + d), R - 1, z), (tgt, RD(z, d, c, m), z))
                    if m >= 2:
                        ident(7, 'I2', (z, d, c, m),
                              (child_A(X, m), R - 1, z),
                              (XW(m - 1, d + 1, c), RW(z, d + 1, c, m - 1), z))
                    if z >= 1:
                        ident(7, 'I3', (z, d, c, m),
                              (X, R - 1, z - 1),
                              (XW(m, d, c), RW(z - 1, d, c, m), z - 1))
    for z in (0, 1, 2):
        for d in range(2, 7):
            for c in range(2, 6):
                for m in range(1, 8):
                    X = XD(m, d, c); R = RD(z, d, c, m)
                    if d >= 3:
                        ident(7, 'I4', (z, d, c, m),
                              (child_A(X, m + d - 1), R - 1, z),
                              (XE(m, d, c), RE(z, d, c, m), z))
                    ident(7, 'I5', (z, d, c, m),
                          (child_A(X, m + d), R - 1, z),
                          (XAp(m, d, c), RAp(z, d, c, m), z))
                    if z >= 1:
                        ident(7, 'I6', (z, d, c, m),
                              (X, R - 1, z - 1),
                              (XD(m, d, c), RD(z - 1, d, c, m), z - 1))
    for z in (1, 2):
        for d in range(3, 8):
            for c in range(2, 6):
                for m in range(1, 8):
                    ident(7, 'I7', (z, d, c, m),
                          (XE(m, d, c), RE(z, d, c, m) - 1, z - 1),
                          (XE(m, d, c), RE(z - 1, d, c, m), z - 1))
    for z in (1, 2):
        for d in range(2, 7):
            for c in range(2, 6):
                for m in range(1, 8):
                    ident(7, 'I8', (z, d, c, m),
                          (XAp(m, d, c), RAp(z, d, c, m) - 1, z - 1),
                          (XAp(m, d, c), RAp(z - 1, d, c, m), z - 1))
    for z in (1, 2):
        for s in range(0, 6):
            for m in range(1, 11):
                ident(7, 'I9', (z, m, s),
                      (XA(m, s), RA(z, m, s) - 1, z - 1),
                      (XA(m, s), RA(z - 1, m, s), z - 1))
    for z in (0, 1, 2):
        for d in range(1, 7):
            for c in range(2, 6):
                X = XD(1, d, c); R = RD(z, d, c, 1)
                ident(7, 'I10', (z, d, c),
                      (child_B(X, 1), R - 1, z + 1),
                      (S([d] + [d + 1] * (c - 1)), d + 2 + z, z + 1))
    for z in (0, 1, 2):
        for d in range(1, 7):
            for c in range(2, 6):
                X = XW(1, d, c); R = RW(z, d, c, 1)
                ident(7, 'I11', (z, d, c),
                      (child_B(X, 1), R - 1, z + 1),
                      (S([(1 + d)] * c), (1 + d) + 2 + z, z + 1))

    # ---------------- D9 mex fixed point
    def point_children(X, R, z):
        # returns list of (Xc, Rc, zc, xor): option value = xor ^ H(Rc,Xc,zc)
        ch = []
        for v in sorted(set(X)):
            if v > 1:
                ch.append((child_A(X, v), R - 1, z, 0))
            else:
                ch.append((child_B(X, v), R - 1, z + 1, 0))
        if z >= 1:
            ch.append((X, R - 1, z - 1, 1))
        if TAMPER == 'mex':
            ch = ch[:1]
        return ch

    def child_values(X, R, z):
        return set(x ^ H(rr, xx, zz)
                   for (xx, rr, zz, x) in point_children(X, R, z))

    for z in (0, 1, 2):
        for d in range(1, 7):
            for c in range(2, 5):
                for m in range(1, 9):
                    X = XW(m, d, c); R = RW(z, d, c, m)
                    rec(8, 'mexW', (z, d, c, m),
                        mex(child_values(X, R, z)), WL(z, d, c, m))
        clear()
    for z in (0, 1, 2):
        for d in range(2, 7):
            for c in range(2, 5):
                for m in range(1, 9):
                    X = XD(m, d, c); R = RD(z, d, c, m)
                    rec(8, 'mexD', (z, d, c, m),
                        mex(child_values(X, R, z)), DL(z, d, c, m))
        clear()
    for z in (0, 1, 2):
        for d in range(3, 7):
            for c in range(2, 5):
                for m in range(1, 7):
                    X = XE(m, d, c); R = RE(z, d, c, m)
                    rec(8, 'mexE', (z, d, c, m),
                        mex(child_values(X, R, z)), EL(z, d, c, m))
        clear()
    for z in (0, 1, 2):
        for d in range(2, 7):
            for c in range(3, 6):
                for m in range(1, 7):
                    X = XAp(m, d, c); R = RAp(z, d, c, m)
                    rec(8, 'mexAp', (z, d, c, m),
                        mex(child_values(X, R, z)), ApL(z, d, c, m))
        clear()
    for z in (0, 1, 2):
        for s in range(0, 6):
            for m in range(1, 11):
                X = XA(m, s); R = RA(z, m, s)
                rec(8, 'mexA', (z, m, s),
                    mex(child_values(X, R, z)), AL(z, m, s))
        clear()

    # ---------------- D10 cross-engine web spots
    spots = [((0, 3, 3, 3), 'W'), ((1, 4, 2, 5), 'W'), ((2, 5, 4, 2), 'W'),
             ((0, 2, 3, 4), 'D'), ((1, 5, 2, 3), 'D'), ((2, 6, 3, 6), 'D'),
             ((0, 4, 2, 4), 'E'), ((1, 3, 4, 2), 'E'), ((2, 7, 2, 3), 'E'),
             ((0, 3, 4, 3), 'Ap'), ((1, 5, 5, 2), 'Ap'), ((2, 4, 6, 5), 'Ap'),
             ((0, 2, 1), 'A'), ((1, 3, 3), 'A'), ((2, 6, 4), 'A'),
             ((0, 4, 3, 2), 'Am'), ((1, 5, 4, 3), 'Am'), ((2, 3, 2, 4), 'Am')]
    for p, kind in spots:
        if kind == 'W':
            z, d, c, m = p; X, R = XW(m, d, c), RW(z, d, c, m)
        elif kind == 'D':
            z, d, c, m = p; X, R = XD(m, d, c), RD(z, d, c, m)
        elif kind == 'E':
            z, d, c, m = p; X, R = XE(m, d, c), RE(z, d, c, m)
        elif kind == 'Ap':
            z, d, c, m = p; X, R = XAp(m, d, c), RAp(z, d, c, m)
        elif kind == 'A':
            z, m, s = p; X, R = XA(m, s), RA(z, m, s)
        else:
            z, m, h, s = p; X, R = XAm(m, h, s), RA(z, m, s)
        vc = H_canonical(R, X, z)
        vo = H_ordered(R, X, z)
        rec(9, 'xeng', (kind,) + tuple(p), vc, vo)
        clear()

    # ---------------- D11 single-token closed form vs both engines
    for x in range(2, 10):
        for z in range(0, 4):
            for R in range(1, 22):
                rec(10, 'sing', (x, z, R), vC(x, z, R),
                    single_token(x, z, R))
                rec(10, 'singO', (x, z, R), vO(x, z, R),
                    single_token(x, z, R))
            clear()

    res['counts'] = counts
    res['bad'] = bad
    res['examples'] = ex
    res['total_comparisons'] = sum(counts)
    res['overall_bad'] = sum(bad)
    print(json.dumps(res, indent=1, sort_keys=True))
    info = {'elapsed_s': round(time.time() - t0, 1),
            'finished': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    print(json.dumps(info, sort_keys=True), file=sys.stderr)
    if res['overall_bad'] != 0:
        sys.exit(1)

main()

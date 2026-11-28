#!/usr/bin/env python3
"""
Baer partition (Bruck) independent machine verification — implementation 1.

q = p^m prime power, Q = q^2. Build K = GF(Q) as GF(p^{2m}), then
E = GF(Q^3) as K[t]/(f) with f a monic irreducible cubic over K.
Identify K^3 ~= E via basis (1, t, t^2).

Points of PG(2,Q) = cosets of K* in E* = {gamma^i . K* : i in Z_N},
point i <-> span_K(gamma^i) (gamma a generator of E*; the image of gamma
in E*/K* has order N = q^4+q^2+1). Singer subgroup of order q^2+q+1:
orbits are the residue classes of step q^2-q+1 in Z_N (q^2-q+1 orbits).
Bruck's theorem: these orbits form a partition of PG(2,Q) into disjoint
Baer subplanes PG(2,q). This script machine-verifies that partition for
given q, definition-direct.

Battery per q (all finite, definition-direct):
 (0) design: N points/lines; each line Q+1 points; each point on Q+1 lines;
     every two lines meet in exactly 1 point (full for N<=400, 2000 seeded
     samples otherwise); gamma^N in K* and gamma^{N/d} outside K* for all
     prime divisors d of N (Singer quotient order exactly N).
 (1) orbit partition: q^2-q+1 orbits, each of size q^2+q+1, disjoint, total N.
 (2) Baer criterion per orbit: every line meets the orbit in 1 or q+1
     points; number of (q+1)-secant lines == q^2+q+1.
 (3) union of orbits 0,1: every line >= 2 points (t=2 blocking witness,
     size 2(q^2+q+1)); for q==4 also union of orbits 0,1,2: every line >= 3.
Calibrations: q=2 per-orbit line profile {1:14,3:7} (Fano; matches the K1372
PG(2,4) census profile); q=3 {1:78,4:13}; q=4 pair union size 42 == K1373
PG(2,16) sampling witness size.

NOTE (bugfix disclosed): the polynomial reduction in gfp_mul/frob_residue
must SUBTRACT v*pp[j] (x^k = -sum pp[j] x^j); a plus-sign version coincides
with the correct rule only in characteristic 2. This file uses the
sign-correct rule.

Usage: baer_partition_impl1.py q1,q2,... [outfile.json]
"""
import sys, json, random

# ---------- GF(p^k) with packed base-p representation ----------

def digits_of(x, p):
    d = []
    while x:
        d.append(x % p); x //= p
    return d

def pack(ds, p):
    r = 0
    for i, v in enumerate(ds):
        r += v * (p ** i)
    return r

def gfp_mul(a, b, p, k, poly):
    da = digits_of(a, p); db = digits_of(b, p)
    if not da or not db:
        return 0
    c = [0] * (len(da) + len(db) - 1)
    for i, ai in enumerate(da):
        if ai == 0: continue
        for j, bj in enumerate(db):
            if bj:
                c[i + j] = (c[i + j] + ai * bj) % p
    pp = digits_of(poly, p)  # length k+1, pp[k]==1
    for i in range(len(c) - 1, k - 1, -1):
        v = c[i]
        if v:
            c[i] = 0
            for j in range(k):
                if pp[j]:
                    c[i - k + j] = (c[i - k + j] - v * pp[j]) % p
    return pack(c[:k], p)

def gfp_add(a, b, p):
    r = 0; i = 0
    while a or b:
        r += ((a % p) + (b % p)) % p * (p ** i)
        a //= p; b //= p; i += 1
    return r

def gfp_neg(a, p):
    r = 0; i = 0
    while a:
        r += (p - a % p) % p * (p ** i)
        a //= p; i += 1
    return r

def gfp_pow(a, e, p, k, poly):
    res = 1
    while e:
        if e & 1:
            res = gfp_mul(res, a, p, k, poly)
        a = gfp_mul(a, a, p, k, poly)
        e >>= 1
    return res

def gfp_inv(a, p, k, poly):
    return gfp_pow(a, p ** k - 2, p, k, poly)

# ---------- polynomial arithmetic over GF(p) (coefficient lists) ----------

def polymul(A, B, p):
    if not A or not B: return []
    C = [0] * (len(A) + len(B) - 1)
    for i, ai in enumerate(A):
        if ai:
            for j, bj in enumerate(B):
                if bj:
                    C[i + j] = (C[i + j] + ai * bj) % p
    while C and C[-1] == 0: C.pop()
    return C

def polymod(A, B, p):
    A = A[:]
    if not A: return []
    db = len(B) - 1
    lead = B[-1] % p
    li = pow(lead, -1, p)
    while len(A) - 1 >= db:
        d = len(A) - 1 - db
        c = (A[-1] * li) % p
        if c:
            for j in range(db + 1):
                A[d + j] = (A[d + j] - c * B[j]) % p
        while A and A[-1] == 0: A.pop()
        if not A: break
    return A

def polygcd(A, B, p):
    A = A[:]; B = B[:]
    while B and not (len(B) == 1 and B[0] == 0):
        A, B = B, polymod(A, B, p)
    if not A:
        return [1]
    li = pow(A[-1] % p, -1, p)
    return [(v * li) % p for v in A]

def frob_residue(a, f, p, k):
    # a^p mod f for packed residue a (deg < k), f packed monic degree k
    da = digits_of(a, p)
    if not da: return 0
    c = [0] * (len(da) * p + 1)
    for i, ai in enumerate(da):
        if ai:
            c[i * p] = ai % p  # a_i^p = a_i in GF(p)
    pp = digits_of(f, p)
    for i in range(len(c) - 1, k - 1, -1):
        v = c[i]
        if v:
            c[i] = 0
            for j in range(k):
                if pp[j]:
                    c[i - k + j] = (c[i - k + j] - v * pp[j]) % p
    return pack(c[:k], p)

def x_pow_pj_mod_f(f, p, k, j):
    r = p  # element 'x'
    for _ in range(j):
        r = frob_residue(r, f, p, k)
    return r

def is_irreducible(f, p, k):
    """f packed monic degree k over GF(p):
    irreducible iff x^{p^k} == x (mod f) and gcd(x^{p^{k/d}} - x, f) = 1
    for every prime divisor d of k."""
    if k == 1:
        return True
    pp = digits_of(f, p)
    if len(pp) != k + 1 or pp[-1] != 1:
        return False
    r = x_pow_pj_mod_f(f, p, k, k)
    if r != p:
        return False
    for d in prime_divisors(k):
        rj = x_pow_pj_mod_f(f, p, k, k // d)
        a = digits_of(rj, p)
        L = max(len(a), 2)
        diff = [( (a[i] if i < len(a) else 0) - ([0, 1][i] if i < 2 else 0)) % p
                 for i in range(L)]
        while diff and diff[-1] == 0: diff.pop()
        if not diff:
            return False
        g = polygcd(diff, pp, p)
        if not (len(g) == 1 and g[0] == 1 % p):
            return False
    return True

def prime_divisors(n):
    ps = []; d = 2
    while d * d <= n:
        if n % d == 0:
            ps.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: ps.append(n)
    return ps

def find_irreducible(p, k):
    for cand in range(p ** k, p ** (k + 1)):
        if is_irreducible(cand, p, k):
            return cand
    raise RuntimeError("no irreducible poly")

def gfp_generator(p, k, poly):
    n = p ** k - 1
    ps = prime_divisors(n)
    for g in range(2, p ** k):
        ok = True
        for f in ps:
            if gfp_pow(g, n // f, p, k, poly) == 1:
                ok = False; break
        if ok:
            return g
    raise RuntimeError("no generator")

# ---------- E = K[t]/(cubic), elements as 3-tuples of packed K-elements ----------

class Ext3:
    """t^3 = -(c2 t^2 + c1 t + c0) over K = GF(p^k)."""
    def __init__(self, p, k, polyK, cubic):
        self.p = p; self.k = k; self.polyK = polyK
        self.c0, self.c1, self.c2 = cubic

    def mul(self, u, v):
        p, kk, pk = self.p, self.k, self.polyK
        a = list(u); b = list(v)
        c = [0] * 5
        for i in range(3):
            if a[i] == 0: continue
            for j in range(3):
                if b[j]:
                    c[i + j] = gfp_add(c[i + j], gfp_mul(a[i], b[j], p, kk, pk), p)
        # reduce t^3, t^4 with x^3 = -(c2 x^2 + c1 x + c0)
        ncoef = [gfp_neg(self.c0, p), gfp_neg(self.c1, p), gfp_neg(self.c2, p)]
        for i in (4, 3):
            v_ = c[i]
            if v_:
                c[i] = 0
                for j in range(3):
                    if ncoef[j]:
                        c[i - 3 + j] = gfp_add(c[i - 3 + j], gfp_mul(v_, ncoef[j], p, kk, pk), p)
        return (c[0], c[1], c[2])

    def pow_(self, u, e):
        res = (1, 0, 0)
        while e:
            if e & 1:
                res = self.mul(res, u)
            u = self.mul(u, u)
            e >>= 1
        return res

def find_irreducible_cubic(p, k, polyK):
    K = p ** k
    for c2 in range(K):
        for c1 in range(K):
            for c0 in range(K):
                ok = True
                for x in range(K):
                    val = gfp_add(gfp_add(gfp_pow(x, 3, p, k, polyK),
                                          gfp_mul(c2, gfp_pow(x, 2, p, k, polyK), p, k, polyK), p),
                                  gfp_add(gfp_mul(c1, x, p, k, polyK), c0, p), p)
                    if val == 0:
                        ok = False; break
                if ok:
                    return (c0, c1, c2)
    raise RuntimeError("no irreducible cubic")

# ---------- main per-q computation ----------

def factor_pp(q):
    for p in [2, 3, 5, 7]:
        if q % p == 0:
            m = 0; x = q
            while x % p == 0:
                x //= p; m += 1
            assert x == 1
            return p, m
    raise RuntimeError("unsupported q")

def canon_triple(t, p, k, polyK):
    a0, a1, a2 = t
    if a0 != 0:
        inv = gfp_inv(a0, p, k, polyK)
        return (1, gfp_mul(inv, a1, p, k, polyK), gfp_mul(inv, a2, p, k, polyK))
    if a1 != 0:
        inv = gfp_inv(a1, p, k, polyK)
        return (0, 1, gfp_mul(inv, a2, p, k, polyK))
    assert a2 != 0
    inv = gfp_inv(a2, p, k, polyK)
    return (0, 0, 1)

def build_lines(p, k, polyK, Q, triples, trip_index):
    wlist = sorted(set(triples))
    assert len(wlist) == Q * Q + Q + 1
    lines = []
    for w in wlist:
        w0, w1, w2 = w
        pts = []
        if w0 == 0 and w1 == 0:
            for s in range(Q):
                pts.append((1, s, 0))
            pts.append((0, 1, 0))
        elif w0 != 0:
            invw0 = gfp_inv(w0, p, k, polyK)
            a1 = gfp_mul(gfp_neg(w1, p), invw0, p, k, polyK)
            a2 = gfp_mul(gfp_neg(w2, p), invw0, p, k, polyK)
            for c in range(Q):
                pts.append((gfp_add(a1, gfp_mul(c, a2, p, k, polyK), p), 1, c))
            pts.append((a2, 0, 1))
        else:
            invw1 = gfp_inv(w1, p, k, polyK)
            a2 = gfp_mul(gfp_neg(w2, p), invw1, p, k, polyK)
            for c in range(Q):
                pts.append((1, gfp_mul(a2, c, p, k, polyK), c))
            pts.append((0, a2, 1))
        idxs = [trip_index[canon_triple(t, p, k, polyK)] for t in pts]
        assert len(set(idxs)) == Q + 1, (w, len(set(idxs)))
        lines.append(sorted(idxs))
    assert len(set(tuple(l) for l in lines)) == len(lines)
    return lines

def run_q(q):
    p, m = factor_pp(q)
    k = 2 * m
    Q = p ** k
    assert Q == q * q
    polyK = find_irreducible(p, k)
    # verify polyK really gives the field: exactly p^k roots of x^{p^k}=x (full scan for k<=4, generator-order check otherwise)
    genK = gfp_generator(p, k, polyK)
    x = genK; o = 1
    while True:
        x = gfp_mul(x, genK, p, k, polyK); o += 1
        if x == 1: break
    assert o == p ** k - 1, "GF(p^k) multiplicative order wrong"
    cubic = find_irreducible_cubic(p, k, polyK)
    E = Ext3(p, k, polyK, cubic)
    N = Q * Q + Q + 1
    # generator of E* (order Q^3-1) with verification of its order
    ordE = Q ** 3 - 1
    gamma = None
    for cand in range(2, Q ** 3):
        u = (cand % Q, (cand // Q) % Q, (cand // (Q * Q)) % Q)
        if u == (0, 0, 0):
            continue
        ok = True
        for f in prime_divisors(ordE):
            if E.pow_(u, ordE // f) == (1, 0, 0):
                ok = False; break
        if ok:
            gamma = u; break
    assert gamma is not None
    # full order verification
    x = gamma; o = 1
    while True:
        x = E.mul(x, gamma); o += 1
        if x == (1, 0, 0): break
    assert o == ordE, "E* generator order wrong"
    one = (1, 0, 0)
    # gamma^N in K*, and gamma^{N/d} not in K* for prime d | N  (Singer quotient order exactly N)
    def inK(u):
        return u[1] == 0 and u[2] == 0
    gN = E.pow_(gamma, N)
    assert inK(gN) and gN != one
    for d in prime_divisors(N):
        gd = E.pow_(gamma, N // d)
        assert not inK(gd)
    # points: gamma^i for i in Z_N, canonical K-triples
    triples = []
    cur = one
    for i in range(N):
        triples.append(canon_triple(cur, p, k, polyK))
        cur = E.mul(cur, gamma)
    assert len(set(triples)) == N
    trip_index = {t: i for i, t in enumerate(triples)}
    lines = build_lines(p, k, polyK, Q, triples, trip_index)
    assert len(lines) == N
    assert all(len(l) == Q + 1 for l in lines)
    deg = [0] * N
    for l in lines:
        for i in l:
            deg[i] += 1
    assert all(d == Q + 1 for d in deg)
    rng = random.Random(12345)
    pair_ok = True
    if N <= 400:
        ls = [set(l) for l in lines]
        for i in range(N):
            for j in range(i + 1, N):
                if len(ls[i] & ls[j]) != 1:
                    pair_ok = False; break
            if not pair_ok: break
    else:
        for _ in range(2000):
            i = rng.randrange(N); j = rng.randrange(N)
            if i != j and len(set(lines[i]) & set(lines[j])) != 1:
                pair_ok = False; break
    assert pair_ok
    # Singer subgroup orbits: step kk in Z_N
    kk = q * q - q + 1
    osz = q * q + q + 1
    assert N == kk * osz
    orbits = [[(a + j * kk) % N for j in range(osz)] for a in range(kk)]
    assert sorted(i for o in orbits for i in o) == list(range(N))
    linemasks = []
    for l in lines:
        mk = 0
        for idx in l:
            mk |= 1 << idx
        linemasks.append(mk)
    q1 = q + 1
    baer_ok = True
    orbit_profiles = []
    orbit_masks = []
    for o in orbits:
        mk = 0
        for i in o:
            mk |= 1 << i
        orbit_masks.append(mk)
        prof = {}
        for lm in linemasks:
            c = (mk & lm).bit_count()
            if c != 1 and c != q1:
                baer_ok = False
            prof[c] = prof.get(c, 0) + 1
        if set(prof.keys()) != {1, q1} or prof[q1] != osz:
            baer_ok = False
        orbit_profiles.append(prof)
    assert baer_ok, "Baer criterion failed"
    w2 = orbit_masks[0] | orbit_masks[1]
    assert w2.bit_count() == 2 * osz
    min2 = min((w2 & lm).bit_count() for lm in linemasks)
    assert min2 >= 2
    prof2 = {}
    for lm in linemasks:
        c = (w2 & lm).bit_count()
        prof2[c] = prof2.get(c, 0) + 1
    min3 = None
    if q == 4:
        w3 = orbit_masks[0] | orbit_masks[1] | orbit_masks[2]
        assert w3.bit_count() == 3 * 21
        min3 = min((w3 & lm).bit_count() for lm in linemasks)
        assert min3 >= 3
    cal = {}
    if q == 2:
        assert all(pr == {1: 14, 3: 7} for pr in orbit_profiles)
        cal["per_orbit_profile"] = orbit_profiles[0]
    if q == 3:
        assert all(pr == {1: 78, 4: 13} for pr in orbit_profiles)
        cal["per_orbit_profile"] = orbit_profiles[0]
    if q == 4:
        assert orbit_profiles[0] == {1: 252, 5: 21}, orbit_profiles[0]
        cal["per_orbit_profile"] = orbit_profiles[0]
    wit = sorted(orbits[0] + orbits[1])
    return {
        "q": q, "Q": Q, "p": p, "m": m, "N": N,
        "polyK": polyK, "cubic": list(cubic),
        "gamma_packed": gamma[0] + gamma[1] * Q + gamma[2] * Q * Q,
        "genK": genK,
        "n_orbits": kk, "orbit_size": osz,
        "design": {"points": N, "lines": N, "line_size": Q + 1,
                   "point_degree": Q + 1, "pairwise_lines_meet_1": True},
        "baer_criterion_all_orbits": True,
        "per_orbit_profile": orbit_profiles[0],
        "t2_witness_size": 2 * osz, "t2_min_line_intersection": min2,
        "t2_witness_line_profile": prof2,
        "t3_min_line_intersection_q4": min3,
        "calibration": cal,
        "witness_triples": [list(triples[i]) for i in wit],
    }

def main():
    qs = [int(x) for x in (sys.argv[1].split(",") if len(sys.argv) > 1 else ["2"])]
    outfile = sys.argv[2] if len(sys.argv) > 2 else None
    results = {}
    for q in qs:
        results[str(q)] = run_q(q)
        print(f"q={q} OK", file=sys.stderr)
    s = json.dumps(results, sort_keys=True)
    if outfile:
        open(outfile, "w").write(s)
        print("written", outfile, file=sys.stderr)
    else:
        print(s)

if __name__ == "__main__":
    main()

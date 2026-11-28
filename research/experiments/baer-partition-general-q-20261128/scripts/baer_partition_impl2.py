#!/usr/bin/env python3
"""
Baer partition (Bruck) independent machine verification — implementation 2
(independent field construction; shares only the sign-corrected GF(p^k)
primitives with impl1, each re-verified here by order/design checks).

Construction: E' = GF(p^{6m}) built DIRECTLY over GF(p) with its own
irreducible polynomial of degree 6m (impl1 instead towers
GF(p^{2m})[t]/(cubic)). K' = the subfield GF(p^{2m}) = <gamma^{(Q^3-1)/(Q-1)}>
(gamma a generator of E'*). beta = any element outside K'; {1, beta, beta^2}
is automatically a K'-basis (no intermediate field between GF(p^{2m}) and
GF(p^{6m}), degree 3 prime). Coordinates in E' are recovered by GF(p)
linear algebra (precomputed matrix inverse).

Points of PG(2,Q) = cosets of K'* in E'* = {gamma^i . K'* : i in Z_N};
point i <-> span_{K'}(gamma^i); canonical triples normalized in K'.
Singer subgroup orbits = residue classes of step q^2-q+1 in Z_N.
Same battery as impl1 (design checks, orbit partition, Baer criterion,
t=2 witness, t=3 for q==4, calibrations).

Usage: baer_partition_impl2.py q1,q2,... [outfile.json]
"""
import sys, json, random
from baer_partition_impl1 import (
    gfp_mul, gfp_add, gfp_neg, gfp_pow, digits_of, pack,
    find_irreducible, gfp_generator, prime_divisors, factor_pp)

def rank_inv_matrix(M, n, p):
    A = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(M)]
    for col in range(n):
        piv = None
        for r in range(col, n):
            if A[r][col] % p:
                piv = r; break
        if piv is None:
            raise RuntimeError("singular")
        A[col], A[piv] = A[piv], A[col]
        inv = pow(A[col][col], -1, p)
        A[col] = [(v * inv) % p for v in A[col]]
        for r in range(n):
            if r != col and A[r][col] % p:
                f = A[r][col] % p
                A[r] = [(v - f * w) % p for v, w in zip(A[r], A[col])]
    return [row[n:] for row in A]

def run_q(q, seed_beta=2):
    p, m = factor_pp(q)
    kE = 6 * m
    Q = p ** (2 * m)
    assert Q == q * q
    polyE = find_irreducible(p, kE)
    ordE = p ** kE - 1
    assert ordE == Q ** 3 - 1
    gamma = gfp_generator(p, kE, polyE)
    # full order verification of gamma
    x = gamma; o = 1
    while True:
        x = gfp_mul(x, gamma, p, kE, polyE); o += 1
        if x == 1: break
    assert o == ordE, "E'* generator order wrong"
    # K'* = <gamma^{(Q^3-1)/(Q-1)}>, order Q-1
    gK = gfp_pow(gamma, (Q ** 3 - 1) // (Q - 1), p, kE, polyE)
    assert gfp_pow(gK, Q - 1, p, kE, polyE) == 1
    for f in prime_divisors(Q - 1):
        assert gfp_pow(gK, (Q - 1) // f, p, kE, polyE) != 1
    Kelts = [1]
    cur = 1
    for _ in range(Q - 2):
        cur = gfp_mul(cur, gK, p, kE, polyE)
        Kelts.append(cur)
    assert len(Kelts) == Q - 1 and len(set(Kelts)) == Q - 1 and Kelts[-1] != 1
    Kset = set(Kelts)
    assert len(Kset) == Q - 1
    # closure + Frobenius fixed-point checks (full: Q<=81)
    for a in Kelts:
        assert gfp_pow(a, Q, p, kE, polyE) == a
    rng = random.Random(999)
    for _ in range(500):
        a = Kelts[rng.randrange(Q - 1)]; b = Kelts[rng.randrange(Q - 1)]
        assert gfp_mul(a, b, p, kE, polyE) in Kset
        s = gfp_add(a, b, p)
        assert s == 0 or s in Kset
    # beta outside K'
    beta = seed_beta
    while beta == 0 or beta in Kset:
        beta += 1
    assert beta not in Kset and beta != 0
    def vec(x):
        ds = digits_of(x, p)
        return [ds[i] if i < len(ds) else 0 for i in range(kE)]
    beta2 = gfp_mul(beta, beta, p, kE, polyE)
    # GF(p)-basis of K' over GF(p)
    kappa = None; kbasis = None
    for j in range(1, 4 * Q):
        cand = gfp_pow(gK, j, p, kE, polyE)
        rows = []
        cur = 1
        for _ in range(2 * m):
            rows.append(vec(cur))
            cur = gfp_mul(cur, cand, p, kE, polyE)
        rr = [r[:] for r in rows]
        r = 0
        for c in range(kE):
            piv = None
            for i in range(r, len(rr)):
                if rr[i][c] % p:
                    piv = i; break
            if piv is None:
                continue
            rr[r], rr[piv] = rr[piv], rr[r]
            inv = pow(rr[r][c], -1, p)
            rr[r] = [(v * inv) % p for v in rr[r]]
            for i in range(len(rr)):
                if i != r and rr[i][c] % p:
                    f = rr[i][c] % p
                    rr[i] = [(v - f * w) % p for v, w in zip(rr[i], rr[r])]
            r += 1
            if r == 2 * m:
                break
        if r == 2 * m:
            kappa = cand
            kbasis = []
            cur = 1
            for _ in range(2 * m):
                kbasis.append(cur)
                cur = gfp_mul(cur, cand, p, kE, polyE)
            break
    assert kappa is not None
    # GF(p)-coordinate matrix of the K'^3 -> E' map in the bases
    # (kappa-basis of K') x (1, beta, beta^2)
    B = [[0] * kE for _ in range(kE)]
    for j, bj in enumerate((1, beta, beta2)):
        for d in range(2 * m):
            v = gfp_mul(kbasis[d], bj, p, kE, polyE)
            vv = vec(v)
            for r in range(kE):
                B[r][j * (2 * m) + d] = vv[r]
    Binv = rank_inv_matrix(B, kE, p)
    def coords(x):
        vx = vec(x)
        return [sum(Binv[c][r] * vx[r] for r in range(kE)) % p for c in range(kE)]
    def unpack_coords(x):
        cs = coords(x)
        res = []
        for j in range(3):
            val = 0
            for d in range(2 * m):
                cd = cs[j * (2 * m) + d]
                if cd:
                    val = gfp_add(val, gfp_mul(cd, kbasis[d], p, kE, polyE), p)
            res.append(val)
        return tuple(res)
    # roundtrip samples
    for _ in range(50):
        c0 = Kelts[rng.randrange(Q - 1)]; c1 = Kelts[rng.randrange(Q - 1)]; c2 = Kelts[rng.randrange(Q - 1)]
        x = gfp_add(gfp_add(gfp_mul(c0, 1, p, kE, polyE), gfp_mul(c1, beta, p, kE, polyE), p),
                    gfp_mul(c2, beta2, p, kE, polyE), p)
        assert unpack_coords(x) == (c0, c1, c2)
    def Kinv(a):
        return gfp_pow(a, Q - 2, p, kE, polyE)
    def canon(t):
        a0, a1, a2 = t
        if a0 != 0:
            inv = Kinv(a0)
            return (1, gfp_mul(inv, a1, p, kE, polyE), gfp_mul(inv, a2, p, kE, polyE))
        if a1 != 0:
            inv = Kinv(a1)
            return (0, 1, gfp_mul(inv, a2, p, kE, polyE))
        assert a2 != 0
        inv = Kinv(a2)
        return (0, 0, 1)
    N = Q * Q + Q + 1
    # gamma^N in K'* (or 1) and no smaller divisor power
    gN = gfp_pow(gamma, N, p, kE, polyE)
    assert gN == 1 or gN in Kset
    for d in prime_divisors(N):
        gd = gfp_pow(gamma, N // d, p, kE, polyE)
        assert gd != 1 and gd not in Kset
    # points
    triples = []
    cur = 1
    for i in range(N):
        triples.append(canon(unpack_coords(cur)))
        cur = gfp_mul(cur, gamma, p, kE, polyE)
    assert len(set(triples)) == N
    trip_index = {t: i for i, t in enumerate(triples)}
    # lines
    Kelts0 = [0] + Kelts
    wlist = sorted(set(triples))
    assert len(wlist) == N
    lines = []
    for w in wlist:
        w0, w1, w2 = w
        pts = []
        if w0 == 0 and w1 == 0:
            for s in Kelts0:
                pts.append((1, s, 0))
            pts.append((0, 1, 0))
        elif w0 != 0:
            invw0 = Kinv(w0)
            a1 = gfp_mul(gfp_neg(w1, p), invw0, p, kE, polyE)
            a2 = gfp_mul(gfp_neg(w2, p), invw0, p, kE, polyE)
            for c in Kelts0:
                pts.append((gfp_add(a1, gfp_mul(c, a2, p, kE, polyE), p), 1, c))
            pts.append((a2, 0, 1))
        else:
            invw1 = Kinv(w1)
            a2 = gfp_mul(gfp_neg(w2, p), invw1, p, kE, polyE)
            for c in Kelts0:
                pts.append((1, gfp_mul(a2, c, p, kE, polyE), c))
            pts.append((0, a2, 1))
        idxs = [trip_index[canon(t)] for t in pts]
        assert len(set(idxs)) == Q + 1, (w, len(set(idxs)))
        lines.append(sorted(idxs))
    assert len(set(tuple(l) for l in lines)) == N
    deg = [0] * N
    for l in lines:
        for i in l:
            deg[i] += 1
    assert all(d == Q + 1 for d in deg)
    rng2 = random.Random(4242)
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
            i = rng2.randrange(N); j = rng2.randrange(N)
            if i != j and len(set(lines[i]) & set(lines[j])) != 1:
                pair_ok = False; break
    assert pair_ok
    # orbits
    kk = q * q - q + 1
    osz = q * q + q + 1
    assert N == kk * osz
    orbits = [[(a + j * kk) % N for j in range(osz)] for a in range(kk)]
    linemasks = []
    for l in lines:
        mk = 0
        for idx in l:
            mk |= 1 << idx
        linemasks.append(mk)
    q1 = q + 1
    baer_ok = True
    profiles = []
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
        profiles.append(prof)
    assert baer_ok
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
        assert all(pr == {1: 14, 3: 7} for pr in profiles)
        cal["per_orbit_profile"] = profiles[0]
    if q == 3:
        assert all(pr == {1: 78, 4: 13} for pr in profiles)
        cal["per_orbit_profile"] = profiles[0]
    if q == 4:
        assert profiles[0] == {1: 252, 5: 21}, profiles[0]
        cal["per_orbit_profile"] = profiles[0]
    wit = sorted(orbits[0] + orbits[1])
    return {
        "q": q, "Q": Q, "p": p, "m": m, "N": N,
        "polyE": polyE, "beta": beta,
        "n_orbits": kk, "orbit_size": osz,
        "design": {"points": N, "lines": N, "line_size": Q + 1,
                   "point_degree": Q + 1, "pairwise_lines_meet_1": True},
        "baer_criterion_all_orbits": True,
        "per_orbit_profile": profiles[0],
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
        print(f"q={q} OK (impl2)", file=sys.stderr)
    s = json.dumps(results, sort_keys=True)
    if outfile:
        open(outfile, "w").write(s)
        print("written", outfile, file=sys.stderr)
    else:
        print(s)

if __name__ == "__main__":
    main()

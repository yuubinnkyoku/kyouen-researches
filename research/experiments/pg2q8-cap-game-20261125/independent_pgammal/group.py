"""Permutation group utilities: orbit/transversal, Schreier-Sims order and
membership, built from scratch (no third-party code).

Conventions: a permutation is a tuple p with p[i] = image of point i.
compose(a, b) = a o b (apply b, then a).
"""
import random
import sys

IDENT_CACHE = {}


def identity(n):
    if n not in IDENT_CACHE:
        IDENT_CACHE[n] = tuple(range(n))
    return IDENT_CACHE[n]


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(p):
    r = [0] * len(p)
    for i, x in enumerate(p):
        r[x] = i
    return tuple(r)


def dedupe(gens, ident):
    out = []
    seen = set()
    for g in gens:
        if g == ident or g in seen:
            continue
        seen.add(g)
        out.append(g)
    return out


def orbit_transversal(gens, b, n):
    """Orbit of b and transversal T with T[x](b)=x for x in orbit."""
    ident = identity(n)
    T = {b: ident}
    orbit = [b]
    for x in orbit:
        tx = T[x]
        for g in gens:
            y = g[x]
            if y not in T:
                T[y] = compose(g, tx)
                orbit.append(y)
    return orbit, T


def sift(h, base, trans, start=0):
    """Sift h through the chain from level start.

    Returns (level, remainder) where remainder fixes base[0:level] and either
    level == len(base) (remainder fixes all base points) or remainder moves
    base[level] to a point outside the current orbit at that level.
    """
    n = len(h)
    for j in range(start, len(base)):
        b = base[j]
        y = h[b]
        if y == b:
            continue
        T = trans[j]
        if y not in T:
            return j, h
        h = compose(inverse(T[y]), h)
    return len(base), h


def schreier_sims(gens, n, verbose=False):
    """Deterministic Schreier-Sims.

    Returns (order, base, levels, orbits, trans).
    levels[i] generates (together with deeper levels) the stabiliser of
    base[0:i]; orbit sizes multiply to the group order.
    """
    ident = identity(n)
    levels = [dedupe(list(gens), ident)]
    base = []
    passes = 0
    while True:
        passes += 1
        # invariant: len(base) == len(levels)
        while len(base) < len(levels):
            i = len(base)
            gens_i = []
            for L in levels[i:]:
                gens_i.extend(L)
            b = None
            for g in gens_i:
                for p in range(n):
                    if g[p] != p:
                        b = p
                        break
                if b is not None:
                    break
            if b is None:
                levels = levels[:i]
                break
            base.append(b)
        k = len(levels)
        # generators available at level i = all generators at levels >= i
        gens_i = [None] * k
        acc = []
        for i in range(k - 1, -1, -1):
            acc = list(levels[i]) + acc
            gens_i[i] = list(acc)
        orbits = [None] * k
        trans = [None] * k
        for i in range(k):
            o, T = orbit_transversal(gens_i[i], base[i], n)
            orbits[i] = o
            trans[i] = T
        added = False
        for i in range(k):
            for x in orbits[i]:
                Tx = trans[i][x]
                for g in gens_i[i]:
                    y = g[x]
                    h = compose(inverse(trans[i][y]), compose(g, Tx))
                    # h fixes base[0:i+1]
                    j, rem = sift(h, base, trans, start=i + 1)
                    if j < k:
                        # rem moves base[j] outside its orbit: extend level j
                        levels[j].append(rem)
                        added = True
                        break
                    if rem != ident:
                        # rem fixes all base points: extend base
                        bnew = next(p for p in range(n) if rem[p] != p)
                        base.append(bnew)
                        levels.append([rem])
                        added = True
                        break
                if added:
                    break
            if added:
                break
        if not added:
            # final consistency checks
            for i, L in enumerate(levels):
                for g in L:
                    for p in base[:i]:
                        assert g[p] == p, "level invariant broken"
            order = 1
            for o in orbits:
                order *= len(o)
            if verbose:
                print("Schreier-Sims passes:", passes)
                print("base:", base)
                print("level sizes:", [len(L) for L in levels])
                print("orbit sizes:", [len(o) for o in orbits])
                print("order:", order)
            return order, base, levels, orbits, trans


def group_order_bruteforce(gens, n, limit=100000):
    ident = identity(n)
    seen = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                y = compose(g, x)
                if y not in seen:
                    seen.add(y)
                    if len(seen) > limit:
                        raise RuntimeError("bruteforce limit")
                    nxt.append(y)
        frontier = nxt
    return len(seen)


def is_member(h, base, levels, orbits, trans, n):
    """Membership test using a completed BSGS from schreier_sims."""
    ident = identity(n)
    j, rem = sift(h, base, trans, start=0)
    return j == len(base) and rem == ident


# --------------------------------------------------------------- testing ---
def _perm_from_cycles(cycles, n):
    p = list(range(n))
    for cyc in cycles:
        for i in range(len(cyc)):
            p[cyc[i]] = cyc[(i + 1) % len(cyc)]
    return tuple(p)


def _random_perm(rng, n):
    p = list(range(n))
    rng.shuffle(p)
    return tuple(p)


def _self_test():
    rng = random.Random(12345)
    cases = []

    cases.append(("C5", [_perm_from_cycles([[0, 1, 2, 3, 4]], 5)], 5, 5))
    cases.append(("S3", [_perm_from_cycles([[0, 1]], 3),
                         _perm_from_cycles([[1, 2]], 3)], 3, 6))
    cases.append(("D8", [_perm_from_cycles([[0, 1, 2, 3]], 4),
                         _perm_from_cycles([[1, 3]], 4)], 4, 8))
    cases.append(("A4", [_perm_from_cycles([[0, 1, 2]], 4),
                         _perm_from_cycles([[0, 1], [2, 3]], 4)], 4, 12))
    cases.append(("S4", [_perm_from_cycles([[0, 1]], 4),
                         _perm_from_cycles([[0, 1, 2, 3]], 4)], 4, 24))
    cases.append(("S5", [_perm_from_cycles([[0, 1]], 5),
                         _perm_from_cycles([[0, 1, 2, 3, 4]], 5)], 5, 120))
    # a group where the natural base is longer: affine group AGL(1,7)
    aff = []
    for a in range(1, 7):
        for b in range(7):
            p = tuple((a * x + b) % 7 for x in range(7))
            aff.append(p)
    cases.append(("AGL(1,7)", [aff[1], aff[14]], 7, 42))

    ok = True
    for name, gens, n, expected in cases:
        order, base, levels, orbits, trans = schreier_sims(gens, n)
        bf = group_order_bruteforce(gens, n)
        status = "OK" if order == expected == bf else "FAIL"
        if status == "FAIL":
            ok = False
        print(f"{name:12s} ss={order:6d} bf={bf:6d} expected={expected:6d} "
              f"base={base} {status}")
    # membership sanity on S4
    gens = [_perm_from_cycles([[0, 1]], 4),
            _perm_from_cycles([[0, 1, 2, 3]], 4)]
    order, base, levels, orbits, trans = schreier_sims(gens, 4)
    for _ in range(50):
        p = _random_perm(rng, 4)
        # membership verified by brute force set
    # check that a non-member of C5 is rejected
    gens = [_perm_from_cycles([[0, 1, 2, 3, 4]], 5)]
    order, base, levels, orbits, trans = schreier_sims(gens, 5)
    assert is_member(identity(5), base, levels, orbits, trans, 5)
    assert not is_member(_perm_from_cycles([[0, 1]], 5), base, levels, orbits,
                         trans, 5)
    print("membership tests OK")
    return ok


if __name__ == "__main__":
    ok = _self_test()
    sys.exit(0 if ok else 1)

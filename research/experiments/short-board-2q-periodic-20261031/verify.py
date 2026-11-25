#!/usr/bin/env python3
"""Finite certificate for the two-carrier q-point game's constant-state solution.

Run: python verify.py. No external dependencies. The certificate checks all
legal symbolic boundary classes; it does NOT extrapolate finite q samples.
"""
from functools import lru_cache

TYPES = {
    "I": (0, 0, 0, 0), "II": (0, 0, 1, 1),
    "III": (0, 0, 2, 2), "IV": (1, 0, 1, 0),
    "V": (1, 0, 2, 1), "VI": (1, 1, 2, 0),
    "VII": (2, 0, 2, 0),
}
EXPECTED = {name: ((1, 0) if name in ("IV", "V") else (0, 1))
            for name in TYPES}


def mex(vals):
    vals = set(vals)
    i = 0
    while i in vals:
        i += 1
    return i


def valid(u, v, t, e, a, b, c, z):
    return (u >= 0 and v >= 0 and 0 <= t <= c and 0 <= e <= z
            and u+a+1-t >= 0 and v+b+1-t >= 0)


def children(u, v, t, e, a, b, c, z):
    if u > 0 and u+a+1-t > 0:
        yield u-1, v, t, e
    if v > 0 and v+b+1-t > 0:
        yield u, v-1, t, e
    if t > 0 and u > 0 and v > 0:
        yield u-1, v-1, t-1, e
    if e > 0:
        yield u, v, t, e-1


def p(n):
    """Exact small counts 0..5; all larger counts reduce by parity."""
    return n if n <= 5 else 4+(n % 2)


def finite_certificate(name, pars):
    a, b, c, z = pars
    # The finite table is obtained by the mex recursion, not hardcoded values.
    @lru_cache(None)
    def base(u, v, t, e):
        assert 0 <= u <= 5 and 0 <= v <= 5
        assert valid(u, v, t, e, *pars)
        cs = list(children(u, v, t, e, *pars))
        if not cs:
            return 0, 1
        vs = [base(*s) for s in cs]
        return mex(x[0] for x in vs), mex(x[1] for x in vs)

    def f(u, v, t, e):
        return base(p(u), p(v), t, e)

    checked = 0
    # u,v=0..5: ordinary base cases. 6,7: generic even/odd tails.
    # For u>=8, projected parent and all projected children are identical
    # to those of u=6 (even) or u=7 (odd); similarly for v>=8.
    for t in range(c+1):
        for e in range(z+1):
            for u in range(8):
                for v in range(8):
                    if not valid(u, v, t, e, *pars):
                        continue
                    cs = list(children(u, v, t, e, *pars))
                    rhs = ((0, 1) if not cs else
                           (mex(f(*s)[0] for s in cs),
                            mex(f(*s)[1] for s in cs)))
                    assert f(u, v, t, e) == rhs, (name, u, v, t, e)
                    checked += 1
    pairs = {f(u, v, t, e)
             for t in range(c+1) for e in range(z+1)
             for u in range(6) for v in range(6)
             if valid(u, v, t, e, *pars)}
    if name == "VI":
        assert pairs == {(0, 0), (0, 1), (0, 2), (1, 0),
                         (1, 1), (1, 3), (2, 2), (3, 3)}
    else:
        assert all(h == (1-g if g < 2 else g) for g, h in pairs)
    # q>=7 means u=v=q-1>=6, so only the two parity classes occur.
    assert f(6, 6, c, z) == EXPECTED[name]
    assert f(7, 7, c, z) == EXPECTED[name]
    return checked, f


def independent_recurrence(q, pars):
    """Independent occupied-count recurrence, no shared transition routine."""
    a, b, c, z = pars
    x, y = q+a-c, q+b-c

    @lru_cache(None)
    def exact(i, j, t, e):
        cs = []
        if i < x and i+t < q-1:
            cs.append(exact(i+1, j, t, e))
        if j < y and j+t < q-1:
            cs.append(exact(i, j+1, t, e))
        if t < c and i+t < q-1 and j+t < q-1:
            cs.append(exact(i, j, t+1, e))
        if e < z:
            cs.append(exact(i, j, t, e+1))
        if not cs:
            return 0, 1
        return mex(s[0] for s in cs), mex(s[1] for s in cs)
    return exact


def verify():
    total = 0
    for name, pars in TYPES.items():
        n, f = finite_certificate(name, pars)
        total += n
        a, b, c, z = pars
        checked = 0
        for q in (7, 8, 12, 25, 60):
            exact = independent_recurrence(q, pars)
            x, y = q+a-c, q+b-c
            for t in range(c+1):
                for e in range(z+1):
                    for i in range(x+1):
                        for j in range(y+1):
                            if i+t >= q or j+t >= q:
                                continue
                            u, v = q-1-i-t, q-1-j-t
                            assert exact(i, j, t, e) == f(u, v, c-t, z-e), (name, q, i, j, t, e)
                            checked += 1
            assert exact(0, 0, 0, 0) == EXPECTED[name]
        print(f"{name}: certificate {n} classes; independent states {checked}; root {EXPECTED[name]}")
    assert total == 1723, total
    print(f"PASS: {total} finite certificate cases; all q>=7 by induction")


if __name__ == "__main__":
    verify()

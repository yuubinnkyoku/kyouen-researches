#!/usr/bin/env python3
"""Independent modular audits of the absent q48 mod-27 chord class.

The witnesses are only congruence solutions, NOT exact integer chords/circles.
"""
from math import gcd, lcm


def sqrt73_mod_3power(k):
    """Digit-by-digit Hensel lifting, starting with root 1 modulo 3."""
    assert k >= 1
    r, p = 1, 3
    for _ in range(1, k):
        opts = [r + a * p for a in range(3) if ((r + a * p)**2 - 73) % (3*p) == 0]
        assert len(opts) == 1
        r = opts[0]
        p *= 3
    assert (r*r - 73) % p == 0
    return r


def crt(a, m, b, n):
    assert gcd(m, n) == 1
    return (a + m * (((b - a) * pow(m, -1, n)) % n)) % (m*n)


def construct(N):
    """Find odd positive residues with the absent class and both equations mod N."""
    assert N >= 1
    L = lcm(N, 54)  # force both the mod-27 class and oddness
    p, other, k = 1, L, 0
    while other % 3 == 0:
        p *= 3
        other //= 3
        k += 1
    assert k >= 3 and other % 2 == 0
    root = sqrt73_mod_3power(k)
    local = (root, 9, 9, root)
    baseline = (1, 3, 3, 1)
    vals = tuple(crt(a, p, b, other) for a, b in zip(local, baseline))
    vals = tuple((v if v > 0 else L) + (i+1)*L for i,v in enumerate(vals))
    a, b, c, d = vals
    assert a < b < c < d
    assert all(v % 2 for v in vals)
    assert (a*a % 27, b*b % 27, c*c % 27, d*d % 27) == (19, 0, 0, 19)
    assert (a*a - 2*b*b + c*c + 8) % N == 0
    assert (b*b - 2*c*c + d*d + 8) % N == 0
    return L, vals


def independent_roots(max_k=8):
    """Separate exhaustive square-residue enumeration (not Hensel or CRT)."""
    for k in range(1, max_k + 1):
        mod = 3**k
        brute = {v for v in range(mod) if (v*v - 73) % mod == 0}
        r = sqrt73_mod_3power(k)
        assert brute == {r, (-r) % mod}, (k, brute, r)
        if k >= 3:
            assert r*r % 27 == 19
        print(f"3^{k}: {len(brute)} roots; least={min(brute)}; Hensel={r}")


def audit():
    independent_roots()
    cases = [1,2,3,4,5,7,9,16,27,54,81,243,729,2187,6561,
             2016,4032,12096,1000000,1000003,3**10,2**15*3**8*5]
    for n in cases:
        L, vals = construct(n)
        # Independent check: recompute the original circle row polynomial
        # using the common root sum S and the coefficients obtained at y=0,1.
        # Checking modulo n only when the equalities are known modulo 4n.
        _, vals4 = construct(4*n)
        a,b,c,d = vals4
        S = max(vals4)
        assert (S-a)%2==0
        X = (S*S - a*a)//4
        Y = (a*a - b*b)//4 - 1
        for y, width in enumerate(vals4):
            x1, x2 = (S-width)//2, (S+width)//2
            for x in (x1,x2):
                assert (x*x + y*y - S*x + Y*y + X) % n == 0
        print(f"N={n}: PASS (modulus={L}, chords={vals})")
    print(f"ALL {len(cases)} modulus tests passed")


if __name__ == '__main__':
    audit()

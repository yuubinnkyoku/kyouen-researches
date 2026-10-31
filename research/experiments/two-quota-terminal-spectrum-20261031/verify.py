"""Independent point-labelled audit for K0588. Run: python verify.py."""
from collections import Counter
from math import comb
from random import Random


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def formula(x, y, c, z, p, r):
    out = Counter()
    for t in range(c + 1):
        w = choose(c, t)
        both = w * choose(x, p - t) * choose(y, r - t)
        if both:
            out[p + r - t + z] += both
        if y + t < r:
            a_only = w * choose(x, p - t)
            if a_only:
                out[p + y + z] += a_only
        if x + t < p:
            b_only = w * choose(y, r - t)
            if b_only:
                out[r + x + z] += b_only
    return out


def direct(x, y, c, z, p, r):
    n = x + y + c + z
    a = ((1 << x) - 1) | (((1 << c) - 1) << (x + y))
    b = (((1 << y) - 1) << x) | (((1 << c) - 1) << (x + y))
    full = (1 << n) - 1
    out = Counter()
    for mask in range(1 << n):
        if (mask & a).bit_count() > p or (mask & b).bit_count() > r:
            continue
        missing = full ^ mask
        maximal = True
        while missing:
            bit = missing & -missing
            missing -= bit
            candidate = mask | bit
            if (candidate & a).bit_count() <= p and (candidate & b).bit_count() <= r:
                maximal = False
                break
        if maximal:
            out[mask.bit_count()] += 1
    return out


def run():
    tested = subsets = multi = 0
    for x in range(5):
        for y in range(5):
            for c in range(6):
                if x + y + c > 11 or not (x + c and y + c):
                    continue
                for p in range(x + c):
                    for r in range(y + c):
                        for z in (0, 1):
                            if x + y + c + z > 12:
                                continue
                            got = formula(x, y, c, z, p, r)
                            want = direct(x, y, c, z, p, r)
                            assert got == want, (x, y, c, z, p, r, got, want)
                            assert got
                            ks = sorted(got)
                            assert ks == list(range(ks[0], ks[-1] + 1))
                            tested += 1
                            subsets += 1 << (x + y + c + z)
                            multi += len(ks) > 1

    rng = Random(20261031)
    for _ in range(20000):
        x, y, c = (rng.randrange(70) for _ in range(3))
        if not (x + c and y + c):
            continue
        p = rng.randrange(x + c)
        r = rng.randrange(y + c)
        got = formula(x, y, c, 0, p, r)
        assert got
        ks = sorted(got)
        assert ks == list(range(ks[0], ks[-1] + 1))

    assert formula(3, 3, 3, 0, 3, 3) == Counter({3: 1, 4: 27, 5: 27, 6: 1})
    print(f"exhaustive={tested}, point-labelled subsets={subsets}, multilength={multi}, random=20000; all passed")


if __name__ == "__main__":
    run()

#!/usr/bin/env python3
"""Independent exhaustive and named-vertex checks of fixed-witness apex extensions."""
from collections import Counter
from functools import lru_cache

BASE = (3, 3, 5, 9, 9, 20, 20, 32, 36, 36, 48, 65, 65)
EXT = (128, 129, 130, 132, 136, 144, 160, 192)


def decode(code):
    sig = list(BASE)
    for s in EXT:
        code, digit = divmod(code, 3)
        sig.extend([s] * digit)
    assert code == 0
    return sig


def solve(signatures):
    # Count named independent vertices directly, not using the C++ degree-parity table.
    signatures = tuple(signatures)
    active = [0] * 256
    for x in range(1, 256):
        active[x] = sum(bool(x & s) for s in signatures)
    grundy = [0] * 256
    for x in range(1, 256):
        children = set()
        for i in range(8):
            if x >> i & 1:
                children.add(sum(not (s >> i & 1) and bool(s & x)
                                 for s in signatures) % 2)
        for s in set(signatures):
            if s & x:
                y = x & ~s
                newly_isolated = active[x] - active[y] - 1
                children.add(grundy[y] ^ (newly_isolated % 2))
        g = 0
        while g in children:
            g += 1
        grundy[x] = g
    children = set()
    for i in range(8):
        children.add(sum(not (s >> i & 1) for s in signatures) % 2)
    for s in set(signatures):
        y = 255 & ~s
        children.add(grundy[y] ^ ((active[255] - active[y] - 1) % 2))
    return grundy[255], children


def direct_named(signatures):
    # Completely different recurrence: remove closed neighborhoods of named vertices.
    k = 8
    n = k + len(signatures)
    neighbors = [0] * n
    for c in range(k):
        neighbors[c] = ((1 << k) - 1) ^ (1 << c)
    for j, s in enumerate(signatures):
        for c in range(k):
            if s & (1 << c):
                neighbors[c] |= 1 << (k + j)
                neighbors[k + j] |= 1 << c

    @lru_cache(None)
    def grundy(x):
        opts = set()
        y = x
        while y:
            b = y & -y
            y -= b
            c = b.bit_length() - 1
            opts.add(grundy(x & ~(neighbors[c] | b)))
        g = 0
        while g in opts:
            g += 1
        return g

    return grundy((1 << n) - 1)


def main():
    hist = Counter()
    with7 = 0
    joint67 = 0
    representatives = {}
    first_child7 = None
    for code in range(3 ** len(EXT)):
        sig = decode(code)
        g, children = solve(sig)
        hist[g] += 1
        if g not in representatives:
            representatives[g] = (code, sig)
        if 7 in children:
            with7 += 1
            if first_child7 is None:
                first_child7 = (code, sig)
            if 6 in children:
                joint67 += 1
    assert sum(hist.values()) == 6561
    assert dict(sorted(hist.items())) == {
        0: 24, 2: 3257, 3: 3191, 4: 24, 5: 18, 6: 8, 7: 39
    }
    assert with7 == 44 and joint67 == 0
    print("hist", dict(sorted(hist.items())))
    print("child7", with7, "child6+7", joint67)
    assert set(representatives) == {0, 2, 3, 4, 5, 6, 7}
    for g, (code, sig) in sorted(representatives.items()):
        got = direct_named(sig)
        assert got == g, (code, g, got)
        print("named-check", "code", code, "g", got, "vertices", 8 + len(sig))
    code, sig = first_child7
    assert direct_named(sig) == solve(sig)[0]
    print("named-check-child7", "code", code, "vertices", 8 + len(sig))


if __name__ == "__main__":
    main()

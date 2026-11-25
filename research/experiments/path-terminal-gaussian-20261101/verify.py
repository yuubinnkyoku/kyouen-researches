#!/usr/bin/env python3
"""Independent checks for K0609: path graph-star terminal polynomials."""
from collections import Counter
from itertools import product


def plus(a, b):
    c = Counter(a)
    c.update(b)
    return +c


def shift(a, k, factor=1):
    return Counter({j + k: factor * v for j, v in a.items()})


def scalar_S(t, r):
    s = {
        2: Counter({3: r + 2}),
        3: Counter({4: (r + 1) ** 2, 5: 1}),
        4: Counter({5: r * (r + 1) ** 2, 6: 2 * r + 3}),
    }
    for i in range(5, t + 1):
        s[i] = plus(plus(shift(s[i - 1], 1, r), shift(s[i - 2], 3)), shift(s[i - 3], 4))
    return s[t]


def transfer_S(t, r):
    current = {(0, 0): Counter({3: r}), (0, 1): Counter({3: 1}),
               (1, 0): Counter({3: 1})}
    for _ in range(t - 2):
        nxt = {}
        for (a, b), polynomial in current.items():
            for c in (0, 1):
                if a == b == c == 1:
                    continue
                edge00 = (b == 0 and c == 0)
                key = (b, c)
                nxt[key] = plus(nxt.get(key, {}), shift(polynomial, 2 - c - edge00, r if edge00 else 1))
        current = nxt
    out = Counter()
    for (a, b), polynomial in current.items():
        if (a, b) != (1, 1):
            out = plus(out, polynomial)
    return out


def binary_P(t, r):
    n = 1 + t + r * (t - 1)
    result = Counter({n - 1: 1})
    for x in product((0, 1), repeat=t):
        if any(x[i] and not ((i > 0 and not x[i - 1]) or (i + 1 < t and not x[i + 1])) for i in range(t)):
            continue
        edge00 = sum(not x[i] and not x[i + 1] for i in range(t - 1))
        result[n - sum(x) - edge00] += r ** edge00
    return result


def formula_P(t, r, implementation):
    n = 1 + t + r * (t - 1)
    return plus(Counter({n - 1: 1}), shift(implementation(t, r), n - 2 * t))


def hyperedges_P(t, r):
    n = 1 + t + r * (t - 1)
    forbidden = []
    for i in range(t - 1):
        edge = (1 << 0) | (1 << (1 + i)) | (1 << (2 + i))
        for j in range(r):
            edge |= 1 << (1 + t + i * r + j)
        forbidden.append(edge)
    result = Counter()
    for mask in range(1 << n):
        if any(mask & edge == edge for edge in forbidden):
            continue
        missing = ((1 << n) - 1) ^ mask
        maximal = True
        while missing:
            bit = missing & -missing
            missing ^= bit
            if not any((mask | bit) & edge == edge for edge in forbidden):
                maximal = False
                break
        if maximal:
            result[mask.bit_count()] += 1
    return result


def main():
    comparisons = 0
    for t in range(2, 13):
        for r in range(1, 5):
            expected = binary_P(t, r)
            assert expected == formula_P(t, r, scalar_S), (t, r, "scalar")
            assert expected == formula_P(t, r, transfer_S), (t, r, "transfer")
            comparisons += 2
    subsets = 0
    cases = 0
    for t in range(2, 8):
        for r in (1, 2):
            n = 1 + t + r * (t - 1)
            if n > 17:
                continue
            assert hyperedges_P(t, r) == binary_P(t, r), (t, r, "hyperedges")
            subsets += 1 << n
            cases += 1
    print(f"OK: {comparisons} scalar/transfer comparisons; {cases} direct hypergraph games; {subsets} subsets")
    for t, r in ((3, 2), (5, 2), (6, 2)):
        print(f"P_{{{t},{r}}}(u) =", dict(sorted(binary_P(t, r).items())))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent exact checks for K0618: one macroscopic arm and n length-two arms.

Weighted four-state transfer, direct binary words, and independent graph
vertex-deletion enumeration. Finite checks do not replace the limit proof.
"""
from collections import Counter
from itertools import product


def transfer(length, center, first=None):
    assert length >= 1 and center in (0, 1)
    states = Counter()
    for b in (0, 1):
        if first is None or first == b:
            states[(center, b, int(center == 0 and b == 1))] += 1
    for _ in range(1, length):
        nxt = Counter()
        for (a, b, k), count in states.items():
            for c in (0, 1):
                if a == b == c == 0:
                    continue
                nxt[(b, c, k + int(b == 0 and c == 1))] += count
        states = nxt
    out = Counter()
    for (a, b, k), count in states.items():
        if a or b:
            out[k - int(center == 0)] += count
    assert all(k >= 0 for k in out)
    return +out


def words(length, center, first=None):
    out = Counter()
    for word in product((0, 1), repeat=length):
        if first is not None and word[0] != first:
            continue
        chain = (center,) + word + (0,)
        if any(chain[i] == 0 and chain[i - 1] == 0 and chain[i + 1] == 0
               for i in range(1, length + 1)):
            continue
        starts = sum(chain[i - 1] == 0 and chain[i] == 1
                     for i in range(1, length + 1))
        out[starts - int(center == 0)] += 1
    return +out


def mul(a, b):
    out = Counter()
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] += x * y
    return +out


def power(a, n):
    out = Counter({0: 1})
    for _ in range(n):
        out = mul(out, a)
    return out


def predicted(n, length):
    s = 2 + 2 * n + length
    f = mul(power(transfer(2, 1), n), transfer(length, 1))
    g = mul(power(transfer(2, 0), n), transfer(length, 0))
    j = mul(power(transfer(2, 0, first=0), n), transfer(length, 0, first=0))
    out = Counter()
    for k, count in f.items():
        out[s + k] += count
    for k, count in g.items():
        out[s + n + k] += count
    for k, count in j.items():
        out[s + n + k] -= count
    out[s + 2 * n + length - 1] += 1
    return +out


def graph_enumeration(n, length):
    lengths = [2] * n + [length]
    edges = []
    nv = 1
    for ell in lengths:
        parent = 0
        for _ in range(ell):
            edges.append((parent, nv))
            parent = nv
            nv += 1
    neighbors = [0] * nv
    for a, b in edges:
        neighbors[a] |= 1 << b
        neighbors[b] |= 1 << a
    N = 1 + nv + len(edges)
    out = Counter({N - 1: 1})
    full = (1 << nv) - 1
    for deleted in range(1 << nv):
        kept = full ^ deleted
        if any(deleted & (1 << i) and not (neighbors[i] & kept)
               for i in range(nv)):
            continue
        kept_edges = sum(bool(kept & (1 << a)) and bool(kept & (1 << b))
                         for a, b in edges)
        out[N - deleted.bit_count() - kept_edges] += 1
    return +out


def moments(poly):
    z = sum(poly.values())
    mean = sum(k * v for k, v in poly.items()) / z
    variance = sum((k - mean) ** 2 * v for k, v in poly.items()) / z
    return mean, variance


def main():
    assert transfer(2, 1) == Counter({0: 2, 1: 1})
    assert transfer(2, 0) == Counter({0: 3})
    assert transfer(2, 0, first=0) == Counter({0: 1})
    for length in range(1, 14):
        for center, first in ((1, None), (0, None), (0, 0)):
            assert transfer(length, center, first) == words(length, center, first)
    graph_cases = 0
    checked_subsets = 0
    for n in range(1, 4):
        for length in range(1, 7):
            assert predicted(n, length) == graph_enumeration(n, length), (n, length)
            graph_cases += 1
            checked_subsets += 1 << (1 + 2 * n + length)
    A = [1] + [sum(transfer(length, 1).values()) for length in range(1, 151)]
    B = [1] + [sum(transfer(length, 0).values()) for length in range(1, 151)]
    for length in range(3, 151):
        assert A[length] - B[length] == A[length - 3]
    root = 1.8392867552141612
    d = 3 * root * root - 2 * root - 1
    lam_prime = (root + 1) / d
    lam_second = (2 * lam_prime - (6 * root - 2) * lam_prime**2) / d
    alpha = lam_prime / root
    beta = (lam_second + lam_prime) / root - alpha**2
    assert beta > 0
    for length in (100, 250, 500):
        f_mean, f_var = moments(transfer(length, 1))
        g_mean, g_var = moments(transfer(length, 0))
        assert abs(f_mean / length - alpha) < 2 / length
        assert abs(g_mean / length - alpha) < 2 / length
        assert abs(f_var / length - beta) < 2 / length
        assert abs(g_var / length - beta) < 2 / length
    ratio = 1 - root**(-3)
    assert abs(B[150] / A[150] - ratio) < 1e-10
    print(f"PASS: 39 word checks, {graph_cases} direct graph cases / {checked_subsets:,} subsets")
    print("PASS: 150 exact recurrences; long-arm moments at lengths 100, 250, 500")
    print(f"alpha={alpha:.12f}, beta={beta:.12f}, B/A limit={ratio:.12f}")


if __name__ == '__main__':
    main()

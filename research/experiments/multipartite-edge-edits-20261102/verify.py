#!/usr/bin/env python3
"""Independent audits for bounded edge edits of complete multipartite graph-star games.

Run: python3 verify.py  (standard library only).
"""
from collections import Counter
from itertools import combinations
from math import comb
from random import Random


def part_labels(parts):
    return tuple(i for i, m in enumerate(parts) for _ in range(m))


def edges(parts, toggles):
    labels = part_labels(parts)
    flips = {tuple(sorted(x)) for x in toggles}
    return [(a, b) for a in range(len(labels)) for b in range(a + 1, len(labels))
            if (labels[a] != labels[b]) != ((a, b) in flips)]


def fast_polynomial(parts, toggles, r):
    """Sum over exceptional vertices; DP on outside retained counts A,Q,support."""
    labels = part_labels(parts)
    n, k = len(labels), len(parts)
    flips = {tuple(sorted(x)) for x in toggles}
    assert all(0 <= a < b < n for a, b in flips)
    B = sorted({v for edge in flips for v in edge})
    m = [size - sum(labels[b] == i for b in B) for i, size in enumerate(parts)]
    e = len(edges(parts, flips))
    assert e > 0
    N = 1 + n + r * e
    out = Counter({N-1: 1})
    powers = [r**j for j in range(e + 1)]

    for bits in range(1 << len(B)):
        T = {B[j] for j in range(len(B)) if bits >> j & 1}
        t = [sum(labels[v] == i for v in T) for i in range(k)]
        t_total = len(T)
        delta = sum((1 if labels[a] == labels[b] else -1)
                    for a, b in flips if a in T and b in T)

        def add(a, multiplicity):
            # a_i = retained vertices outside B in part i.
            Aout = sum(a)
            for b in B:
                if b in T:
                    continue
                if any(((labels[b] != labels[v]) != ((min(b, v), max(b, v)) in flips))
                       for v in T):
                    continue
                if Aout - a[labels[b]] == 0:
                    return
            for i in range(k):
                if a[i] < m[i] and (t_total - t[i]) + (Aout - a[i]) == 0:
                    return
            A = t_total + Aout
            Q = sum((t[i] + a[i])**2 for i in range(k))
            eR = (A*A-Q)//2 + delta
            assert 0 <= eR <= e
            out[N-n+A-eR] += multiplicity * powers[eR]

        # Zero or exactly one outside part: exceptional domination must be tested.
        add([0]*k, 1)
        for i in range(k):
            for a in range(1, m[i]+1):
                vec = [0]*k
                vec[i] = a
                add(vec, comb(m[i], a))

        # At least two outside parts: every deleted vertex sees an outside
        # retained vertex from a different part, irrespective of edits in B.
        states = {(t_total, sum(x*x for x in t), 0): 1}
        for i, size in enumerate(m):
            nxt = Counter()
            for (A, Q, support), c in states.items():
                for a in range(size + 1):
                    nxt[A+a, Q+2*t[i]*a+a*a, min(2, support+(a>0))] += c*comb(size, a)
            states = nxt
        for (A, Q, support), c in states.items():
            if support < 2:
                continue
            eR = (A*A-Q)//2 + delta
            assert 0 <= eR <= e
            out[N-n+A-eR] += c*powers[eR]
    return +out


def direct_deleted_sets(parts, toggles, r):
    n = sum(parts)
    E = edges(parts, toggles)
    N = 1+n+r*len(E)
    neighbors = [0]*n
    for a,b in E:
        neighbors[a] |= 1<<b
        neighbors[b] |= 1<<a
    out = Counter({N-1: 1})
    for retained in range(1 << n):
        if any(not (retained & neighbors[v]) for v in range(n)
               if not (retained >> v & 1)):
            continue
        eR = sum(bool(retained >> a & 1) and bool(retained >> b & 1) for a,b in E)
        out[N-n+retained.bit_count()-eR] += r**eR
    return +out


def direct_hyperedges(parts, toggles, r):
    n = sum(parts)
    E = edges(parts, toggles)
    N = 1+n+r*len(E)
    forbidden = []
    for j,(a,b) in enumerate(E):
        forbidden.append((1<<0)|(1<<(a+1))|(1<<(b+1))|
                         sum(1<<(1+n+r*j+h) for h in range(r)))
    out = Counter()
    for s in range(1 << N):
        if any((s & f) == f for f in forbidden):
            continue
        if all(any(((s | (1<<p)) & f) == f for f in forbidden)
               for p in range(N) if not (s >> p & 1)):
            out[s.bit_count()] += 1
    return +out, 1 << N


def compositions(n):
    if n == 0:
        yield ()
    else:
        for i in range(1, n+1):
            for tail in compositions(n-i):
                yield (i,)+tail


def run():
    cases = 0
    for n in range(2, 7):
        for parts in compositions(n):
            if len(parts) < 2:
                continue
            pairs = list(combinations(range(n), 2))
            for edits in ((), *[(x,) for x in pairs], *combinations(pairs, 2)):
                if not edges(parts, edits):
                    continue
                for r in (1,2):
                    x = fast_polynomial(parts, edits, r)
                    y = direct_deleted_sets(parts, edits, r)
                    assert x == y, (parts, edits, r, x, y)
                    cases += 1
    print(f"all compositions n<=6, at most two toggles, r=1,2: {cases} cases, zero mismatches")

    rng = Random(20261102)
    extra = 0
    for _ in range(500):
        n = rng.randrange(7, 11)
        cuts = sorted(rng.sample(range(1,n),rng.randrange(1,min(n,5))))
        boundaries = [0]+cuts+[n]
        parts = tuple(boundaries[i+1]-boundaries[i] for i in range(len(boundaries)-1))
        pairs = list(combinations(range(n),2))
        edits = rng.sample(pairs, rng.randrange(0, min(5,len(pairs)+1)))
        if not edges(parts, edits):
            continue
        r = rng.randrange(1,5)
        assert fast_polynomial(parts, edits, r) == direct_deleted_sets(parts, edits, r)
        extra += 1
    print(f"seeded independent larger deleted-set audits: {extra} cases, zero mismatches")

    hypers, subsets = 0, 0
    for n in range(2, 7):
        for parts in compositions(n):
            if len(parts)<2:
                continue
            pairs = list(combinations(range(n),2))
            for edits in ((), *[(x,) for x in pairs]):
                for r in (1,2,3):
                    e = len(edges(parts, edits))
                    N = 1+n+r*e
                    if e == 0 or N>14:
                        continue
                    a = fast_polynomial(parts, edits, r)
                    b, count = direct_hyperedges(parts, edits, r)
                    assert a == b, (parts, edits, r, a, b)
                    hypers += 1
                    subsets += count
    print(f"direct forbidden-hyperedge enumeration: {hypers} cases, {subsets} point subsets, zero mismatches")

    # Specialize to existing K0625 formula with no edits and many parts.
    for n in range(2, 14):
        parts = (1,)*n
        for r in (1,2,3):
            assert fast_polynomial(parts, (), r) == direct_deleted_sets(parts, (), r)
    print("complete-graph specialization n<=13, r=1..3: zero mismatches")
    parts=(2,2,2)
    for edits in ((),((0,2),),((0,1),),((0,2),(1,3))):
        for r in (1,2):
            print(f"example parts={parts} toggles={edits} r={r}: {sorted(fast_polynomial(parts, edits, r).items())}")


if __name__ == "__main__":
    run()

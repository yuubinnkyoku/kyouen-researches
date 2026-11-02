#!/usr/bin/env python3
"""Independent audit of a three-state nice-tree-decomposition terminal DP."""
from collections import defaultdict
from itertools import combinations

# 0=kept, 1=deleted/uncovered, 2=deleted/covered.
def plus(dst, src, shift=0, factor=1):
    for degree, count in src.items():
        dst[degree + shift] += factor * count

def introduce(dp, bag, v):
    assert v not in bag
    new = defaultdict(lambda: defaultdict(int))
    for state, poly in dp.items():
        plus(new[state + (0,)], poly)
        plus(new[state + (1,)], poly)
    return dict(new), bag + [v]

def edge(dp, bag, a, b, r):
    i, j = bag.index(a), bag.index(b)
    out = defaultdict(lambda: defaultdict(int))
    for state, poly in dp.items():
        s = list(state)
        if s[i] == 0 and s[j] == 0:
            plus(out[state], poly, -1, r)
        else:
            if s[i] == 1 and s[j] == 0: s[i] = 2
            if s[j] == 1 and s[i] == 0: s[j] = 2
            plus(out[tuple(s)], poly)
    return dict(out)

def forget(dp, bag, v):
    i = bag.index(v)
    out = defaultdict(lambda: defaultdict(int))
    for state, poly in dp.items():
        if state[i] == 1: continue
        plus(out[state[:i] + state[i + 1:]], poly,
             -1 if state[i] == 2 else 0)
    return dict(out), bag[:i] + bag[i + 1:]

def combine(a, b, bag):
    out = defaultdict(lambda: defaultdict(int))
    for sa, pa in a.items():
        for sb, pb in b.items():
            state = []
            for x, y in zip(sa, sb):
                if (x == 0) != (y == 0): break
                state.append(0 if x == 0 else max(x, y))
            else:
                dest = out[tuple(state)]
                for i, c in pa.items():
                    for j, d in pb.items(): dest[i + j] += c * d
    return dict(out)

def finish(dp, n, edges, r):
    assert set(dp) == {()}
    N = 1 + n + r * len(edges)
    out = defaultdict(int)
    out[N - 1] += 1
    for degree, count in dp[()].items(): out[N + degree] += count
    return {i: v for i, v in sorted(out.items()) if v}

def path_dp(n, edges, r, order=None):
    assert edges and r >= 1
    if order is None: order = list(range(n))
    assert sorted(order) == list(range(n))
    index = {v: i for i, v in enumerate(order)}
    last = {v: index[v] for v in order}
    for a, b in edges:
        last[a] = max(last[a], index[b])
        last[b] = max(last[b], index[a])
    bag, dp, maxbag = [], {(): {0: 1}}, 0
    for v in order:
        dp, bag = introduce(dp, bag, v)
        maxbag = max(maxbag, len(bag))
        for a, b in edges:
            if v == a and index[b] < index[v]:
                dp = edge(dp, bag, a, b, r)
            elif v == b and index[a] < index[v]:
                dp = edge(dp, bag, a, b, r)
        for x in list(bag):
            if last[x] <= index[v]:
                dp, bag = forget(dp, bag, x)
    return finish(dp, n, edges, r), maxbag - 1

def join_dp(n, edges, r):
    # Deliberately wide bag; exercises the join rule, not the path routine.
    children = []
    for half in (edges[::2], edges[1::2]):
        bag, dp = [], {(): {0: 1}}
        for v in range(n): dp, bag = introduce(dp, bag, v)
        for a, b in half: dp = edge(dp, bag, a, b, r)
        children.append(dp)
    bag = list(range(n))
    dp = combine(children[0], children[1], bag)
    for v in range(n): dp, bag = forget(dp, bag, v)
    return finish(dp, n, edges, r)

def direct(n, edges, r):
    adj = [0] * n
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    N = 1 + n + r * len(edges)
    out = defaultdict(int)
    out[N - 1] += 1
    for mask in range(1 << n):
        kept = ((1 << n) - 1) ^ mask
        if any((mask >> v & 1) and not (adj[v] & kept)
               for v in range(n)): continue
        e = sum(not (mask >> a & 1) and not (mask >> b & 1)
                for a, b in edges)
        out[N - mask.bit_count() - e] += r ** e
    return dict(sorted(out.items()))

def hypergraph(n, edges, r):
    N = 1 + n + r * len(edges)
    assert N <= 17
    forbidden = []
    for j, (a, b) in enumerate(edges):
        mask = 1 | (1 << (1 + a)) | (1 << (1 + b))
        for t in range(r): mask |= 1 << (1 + n + r * j + t)
        forbidden.append(mask)
    out = defaultdict(int)
    for mask in range(1 << N):
        if any(mask & f == f for f in forbidden): continue
        if all(any(((mask | (1 << i)) & f) == f for f in forbidden)
               for i in range(N) if not (mask >> i & 1)):
            out[mask.bit_count()] += 1
    return dict(sorted(out.items()))

def main():
    cases = joins = hyp = hyper_masks = 0
    for n in range(2, 7):
        pairs = list(combinations(range(n), 2))
        for bits in range(1, 1 << len(pairs)):
            if n == 6 and bits % 31: continue
            edges = [e for j, e in enumerate(pairs) if bits >> j & 1]
            for r in (1, 2, 3):
                got, width = path_dp(n, edges, r)
                expected = direct(n, edges, r)
                assert got == expected, (n, edges, r, got, expected)
                cases += 1
                if n <= 5 or bits % 7 == 0:
                    assert join_dp(n, edges, r) == expected
                    joins += 1
                if n <= 4 and 1 + n + r * len(edges) <= 17 and hyp < 80:
                    assert hypergraph(n, edges, r) == expected
                    hyp += 1
                    hyper_masks += 1 << (1 + n + r * len(edges))
    from math import comb
    multi = 0
    for m in (3, 4, 5, 8, 13, 20, 40):
        edges = ([(0, v) for v in range(2, m + 2)] +
                 [(1, v) for v in range(2, m + 2)])
        for r in (1, 2, 3):
            got, width = path_dp(m + 2, edges, r)
            assert width == 2
            N = 3 + m + 2 * r * m
            want = defaultdict(int)
            want[N - 1] += 1
            for j in range(m + 1):
                want[N - 2 * m + j] += comb(m, j) * r ** (2 * (m - j))
            want[N - m - 1] += 2 * ((r + 1) ** m - 1)
            want[N - 2] += 1
            assert got == dict(sorted(want.items()))
            multi += 1
    print(f"PASS path cases={cases}, join cases={joins}, "
          f"hypergraph cases={hyp}, hypergraph masks={hyper_masks}, "
          f"K2m cases={multi}")

if __name__ == "__main__":
    main()

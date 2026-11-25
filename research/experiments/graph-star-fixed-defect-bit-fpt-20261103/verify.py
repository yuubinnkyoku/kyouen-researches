#!/usr/bin/env python3
"""Independent integer-scaling audit, without reusing the connected-support FPT solver."""
from itertools import combinations
from math import lcm
from random import Random


def graph_data(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def direct(n, edges, q, d):
    r, e = q - 3, len(edges)
    if not e:
        return int(d == 0)
    adj = graph_data(n, edges)
    ans = int(d == e - 1)
    for mask in range(1 << n):
        X = {i for i in range(n) if mask >> i & 1}
        if any(not (adj[v] - X) for v in X):
            continue
        R = set(range(n)) - X
        er = sum(u in R and v in R for u, v in edges)
        if e - len(X) - er == d:
            ans += r ** er
    return ans


def scaled(n, edges, q, d):
    r, e = q - 3, len(edges)
    if not e:
        return int(d == 0), 0, 0
    if d > e - 1:
        return 0, 0, 0
    adj = graph_data(n, edges)
    H = [v for v in range(n) if len(adj[v]) >= 2]
    L = sum(len(adj[v]) == 1 and len(adj[next(iter(adj[v]))]) >= 2
            for v in range(n))
    h = sum(len(adj[u]) == len(adj[v]) == 1 for u, v in edges)
    C = e - L - h
    A = (r + 2) ** h * r ** C * (r + 1) ** L
    T = 2 * d * (d + 1) + 3 * d
    D = r ** T * (r + 1) ** T
    candidates = []
    for mask in range(1, 1 << len(H)):
        B = {H[j] for j in range(len(H)) if mask >> j & 1}
        if len(B) > 2 * d or any(len(adj[v]) > d + 1 for v in B):
            continue
        if any(not (adj[v] - B) for v in B):
            continue
        stack = [next(iter(B))]
        reached = {stack[0]}
        while stack:
            for v in (adj[stack.pop()] & B) - reached:
                reached.add(v)
                stack.append(v)
        if reached != B:
            continue
        internal = sum(len(adj[v] & B) for v in B) // 2
        defect = sum(len(adj[v]) - 1 for v in B) - internal
        if not 1 <= defect <= d:
            continue
        a = sum(len(adj[v]) == 1 and next(iter(adj[v])) in B
                for v in range(n) if adj[v])
        U = r ** (T * defect + a - len(B) - defect) * (r + 1) ** (T * defect - a)
        assert 0 < U <= D ** defect
        candidates.append((B, defect, U))
    k = len(candidates)
    Q = [0] * (d + 1)
    Q[0] = 1
    for count in range(1, min(d, k) + 1):
        for ids in combinations(range(k), count):
            deg = sum(candidates[i][1] for i in ids)
            if deg > d:
                continue
            if any(candidates[i][0] & candidates[j][0] or
                   any(v in adj[u] for u in candidates[i][0]
                       for v in candidates[j][0])
                   for i, j in combinations(ids, 2)):
                continue
            weight = 1
            for i in ids:
                weight *= candidates[i][2]
            Q[deg] += weight
    numerator = A * Q[d]
    assert numerator % D ** d == 0, (n, edges, q, d, numerator, D)
    result = numerator // D ** d + int(d == e - 1)
    Hden = lcm(*range(1, d + 1)) if d else 1
    power = [1] + [0] * d
    log_scaled = [0] * (d + 1)
    for order in range(1, d + 1):
        nxt = [0] * (d + 1)
        for i in range(d + 1):
            for j in range(1, d - i + 1):
                nxt[i + j] += power[i] * Q[j]
        power = nxt
        for j in range(1, d + 1):
            log_scaled[j] += (1 if order % 2 else -1) * (Hden // order) * power[j]
    recovered = [1] + [0] * d
    for j in range(1, d + 1):
        rhs = sum(t * log_scaled[t] * recovered[j - t]
                  for t in range(1, j + 1))
        assert rhs % (j * Hden) == 0
        recovered[j] = rhs // (j * Hden)
    assert recovered == Q
    return result, k, max(x.bit_length() for x in Q + log_scaled)


def test():
    comparisons, peak_k, peak_bits = 0, 0, 0
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            edges = [p for i, p in enumerate(pairs) if mask >> i & 1]
            if not edges:
                continue
            for q in (4, 5, 8, 19):
                for d in range(min(3, len(edges) - 1) + 1):
                    got, k, bits = scaled(n, edges, q, d)
                    want = direct(n, edges, q, d)
                    assert got == want, (n, edges, q, d, got, want)
                    comparisons += 1
                    peak_k = max(peak_k, k)
                    peak_bits = max(peak_bits, bits)
    rng = Random(20261103)
    for n in (6,):
        pairs = list(combinations(range(n), 2))
        for _ in range(30):
            edges = [p for p in pairs if rng.random() < .3]
            if not edges:
                continue
            for q in (4, 8):
                for d in range(min(3, len(edges) - 1) + 1):
                    got, k, bits = scaled(n, edges, q, d)
                    want = direct(n, edges, q, d)
                    assert got == want, (n, edges, q, d, got, want)
                    comparisons += 1
                    peak_k = max(peak_k, k)
                    peak_bits = max(peak_bits, bits)
    n = 5
    pairs = list(combinations(range(n), 2))
    for _ in range(40):
        edges = [p for p in pairs if rng.random() < .45]
        if not edges:
            continue
        q = 10 ** 40 + 3
        for d in range(min(2, len(edges) - 1) + 1):
            got, k, bits = scaled(n, edges, q, d)
            want = direct(n, edges, q, d)
            assert got == want, (n, edges, q, d, got, want)
            comparisons += 1
            peak_k = max(peak_k, k)
            peak_bits = max(peak_bits, bits)
    print(f"PASS {comparisons} integer-scaled coefficients, "
          f"max_candidates={peak_k}, max_intermediate_bits={peak_bits}")


if __name__ == "__main__":
    test()

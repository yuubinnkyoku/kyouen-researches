#!/usr/bin/env python3
"""Independent checks of the ternary signature theorem for cograph Node Kayles.

The theoretical proof is in the companion report; these checks do not replace it.
"""
from __future__ import annotations
import argparse
import itertools
import json
from functools import lru_cache
from pathlib import Path


def F(x: int) -> int:
    r = 0
    power = 1
    while x:
        if x & 1:
            r += power
        x >>= 1
        power *= 3
    return r


def signature_from_rank(n: int) -> tuple[frozenset[int], int, int, int]:
    assert n >= 0
    t = g = 0
    bit = 1
    m = n
    while m:
        d = m % 3
        if d:
            t |= bit
        if d == 1:
            g |= bit
        m //= 3
        bit *= 2
    options = frozenset(
        g ^ x
        for j in range(t.bit_length()) if t & (1 << j)
        for x in range(1 << j, 1 << (j + 1))
    )
    assert n == F(t) + F(t ^ g)
    assert mex(options) == g
    return options, t, g, F(t) + F(t ^ g)


def mex(values) -> int:
    values = set(values)
    i = 0
    while i in values:
        i += 1
    return i


def join(a, b):
    return a | b


def disjoint_sum(a, b):
    ga, gb = mex(a), mex(b)
    return frozenset({x ^ gb for x in a} | {ga ^ y for y in b})


def verify_closure(max_power: int) -> dict:
    totals = []
    for k in range(1, max_power + 1):
        N = 3 ** k
        rank_by_sig = {signature_from_rank(n)[0]: n for n in range(2 * N + 1)}
        assert len(rank_by_sig) == 2 * N + 1
        inputs = [signature_from_rank(n)[0] for n in range(N + 1)]
        # Empty signature is the empty graph, and its mex=0.
        checks = 0
        for a, b in itertools.product(inputs, repeat=2):
            for operation in (join, disjoint_sum):
                c = operation(a, b)
                assert c in rank_by_sig, (k, operation.__name__, a, b, c)
                assert rank_by_sig[c] <= rank_by_sig[a] + rank_by_sig[b], (k, operation.__name__, a, b, c)
                checks += 1
        totals.append({"k": k, "signatures_including_empty": N + 1, "ordered_pair_operations": checks})
    return {"closure": totals}


def verify_cograph_cpp_dump(path: Path, max_n: int) -> dict:
    observed: dict[int, set[frozenset[int]]] = {}
    for line in path.read_text().splitlines():
        n, mask = map(int, line.split())
        if n > max_n:
            continue
        sig = frozenset(i for i in range(mask.bit_length()) if (mask >> i) & 1)
        observed.setdefault(n, set()).add(sig)
    assert set(observed) == set(range(1, max_n + 1))
    expected: set[frozenset[int]] = set()
    comparisons = 0
    for n in range(1, max_n + 1):
        expected.add(signature_from_rank(n)[0])
        assert observed[n] == expected, (n, len(observed[n]), len(expected), observed[n] ^ expected)
        comparisons += len(expected)
    return {"cpp_dump_max_n": max_n, "cpp_dump_signature_pairs": comparisons}


def verify_small_graphs(max_vertices: int) -> dict:
    counts = {}
    for n in range(1, max_vertices + 1):
        edges = list(itertools.combinations(range(n), 2))
        total = 0
        cog = 0
        for mask in range(1 << len(edges)):
            total += 1
            adj = [0] * n
            for i, (u, v) in enumerate(edges):
                if mask >> i & 1:
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
            # P4-free test on each four-subset: exactly 3 edges and degree multiset 1,1,2,2.
            is_cograph = True
            for vs in itertools.combinations(range(n), 4):
                degrees = [sum(bool(adj[u] >> v & 1) for v in vs) for u in vs]
                if sorted(degrees) == [1, 1, 2, 2]:
                    is_cograph = False
                    break
            if not is_cograph:
                continue
            cog += 1
            @lru_cache(None)
            def sg(vmask: int) -> int:
                return mex(sg(vmask & ~(adj[v] | (1 << v))) for v in range(n) if vmask >> v & 1)
            full = (1 << n) - 1
            sig = frozenset(sg(full & ~(adj[v] | (1 << v))) for v in range(n))
            assert sig in {signature_from_rank(i)[0] for i in range(1, n + 1)}, (n, mask, sig)
        counts[str(n)] = {"all_labeled_graphs": total, "cographs_checked": cog}
    return {"small_graphs": counts}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--max-power', type=int, default=4)
    p.add_argument('--max-vertices', type=int, default=6)
    p.add_argument('--cpp-dump', type=Path)
    p.add_argument('--max-n', type=int, default=400)
    args = p.parse_args()
    result = {"claim": "cograph option signatures indexed bijectively by positive ternary ranks", **verify_closure(args.max_power), **verify_small_graphs(args.max_vertices)}
    if args.cpp_dump:
        result.update(verify_cograph_cpp_dump(args.cpp_dump, args.max_n))
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Independent audit: misere h, two isolates, and arbitrary-rank twin compression."""
from functools import lru_cache
from random import Random

def mex(values):
    i = 0
    while i in values:
        i += 1
    return i

def antichains(n):
    candidates = [x for x in range(1, 1 << n) if x.bit_count() >= 2]
    def walk(todo, chosen):
        if not todo:
            yield tuple(sorted(chosen))
            return
        edge, rest = todo[0], todo[1:]
        yield from walk(rest, chosen)
        yield from walk([f for f in rest if (edge & f) != edge
                         and (edge & f) != f], chosen + [edge])
    yield from walk(candidates, [])

def minimal(edges):
    result = []
    for edge in sorted(set(edges), key=lambda x: (x.bit_count(), x)):
        if not any(edge & other == other for other in result):
            result.append(edge)
    return tuple(sorted(result))

def occupied_misere(n, edges):
    @lru_cache(None)
    def solve(occupied):
        children = []
        for v in range(n):
            bit = 1 << v
            if occupied & bit or any(e & (occupied | bit) == e for e in edges):
                continue
            children.append(solve(occupied | bit))
        return mex(children) if children else 1
    return solve(0)

def residual_misere(n, edges):
    @lru_cache(None)
    def solve(vertices, edges_now):
        if not vertices:
            return 1
        children = []
        for v in range(n):
            bit = 1 << v
            if not vertices & bit:
                continue
            remain = vertices ^ bit
            reduced = minimal((e ^ bit if e & bit else e) for e in edges_now)
            banned = 0
            for e in reduced:
                if e.bit_count() == 1:
                    banned |= e
            remain &= ~banned
            new_edges = minimal(e for e in reduced if e.bit_count() >= 2
                                and e & remain == e)
            children.append(solve(remain, new_edges))
        return mex(children)
    return solve((1 << n) - 1, tuple(edges))

def twin_classes(n, edges):
    groups = {}
    for v in range(n):
        bit = 1 << v
        link = tuple(sorted(e ^ bit for e in edges if e & bit))
        groups.setdefault(link, []).append(v)
    return [group for group in groups.values() if len(group) >= 3]

def compress(n, edges):
    retained = set(range(n))
    for group in twin_classes(n, edges):
        keep = 1 if len(group) % 2 else 2
        retained.difference_update(group[keep:])
    mapping = {v: i for i, v in enumerate(sorted(retained))}
    out = []
    for edge in edges:
        if any(edge >> v & 1 and v not in retained for v in range(n)):
            continue
        out.append(sum(1 << mapping[v] for v in retained if edge >> v & 1))
    return len(retained), tuple(sorted(out))

def audit():
    total = reduced = nonempty = 0
    for n in range(1, 6):
        t = r = q = 0
        for edges in antichains(n):
            t += 1
            original = occupied_misere(n, edges)
            assert original == residual_misere(n, edges)
            assert original == occupied_misere(n + 2, edges)
            m, compressed = compress(n, edges)
            if m < n:
                r += 1
                q += any(any(e >> group[0] & 1 for e in edges)
                         for group in twin_classes(n, edges))
                assert original == occupied_misere(m, compressed)
                assert original == residual_misere(m, compressed)
        print(f"clutters n={n}: {t} total, {r} compressed, {q} nonempty links")
        total += t
        reduced += r
        nonempty += q
    assert (total, reduced, nonempty) == (7020, 72, 59)

    rng = Random(20261031)
    checked = 0
    for outside in range(1, 6):
        for _ in range(400):
            base = minimal(e for e in range(1, 1 << outside)
                           if e.bit_count() >= 2 and rng.random() < 0.15)
            links = [e for e in range(1, 1 << outside)
                     if rng.random() < 0.08]
            for copies in (3, 4, 5, 6):
                edges = minimal(list(base) + [
                    (1 << (outside + j)) | e
                    for j in range(copies) for e in links
                ])
                n = outside + copies
                m, compressed = compress(n, edges)
                assert occupied_misere(n, edges) == occupied_misere(m, compressed)
                checked += 1
    assert checked == 8000
    print(f"PASS: {total} clutters; {reduced} reductions; {checked} extra cases")

if __name__ == "__main__":
    audit()

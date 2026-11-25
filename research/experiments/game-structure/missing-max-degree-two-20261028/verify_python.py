#!/usr/bin/env python3
"""Independent parity-quotient SG recurrence for degree-two missing graph.

Run four separate processes: python3 verify_python.py 4 / 5 / 6a / 6b.
"""
from functools import lru_cache
from itertools import combinations, permutations, product
from time import monotonic


@lru_cache(None)
def grundy(t, r):
    k = len(t)
    if k == 0:
        return 0
    edges = list(combinations(range(k), 2))
    R = dict(zip(edges, r))
    u = (sum(t) + sum(r)) & 1
    z = [(t[i] + sum(R[e] for e in edges if i in e)) & 1 for i in range(k)]
    values = {u ^ v for v in z}  # direct clique moves, not the proposed formula
    choices = [(i,) for i in range(k) if t[i]] + [e for e in edges if R[e]]
    for B in choices:
        B = set(B)
        remain = [i for i in range(k) if i not in B]
        nt = [t[i] for i in remain]
        nr = [R[(i, j)] for i, j in combinations(remain, 2)]
        isolated = sum(t[i] for i in B)
        if len(B) == 1:
            isolated -= 1
        else:
            a, b = sorted(B)
            isolated += R[(a, b)] - 1
        for a, b in edges:
            if a in B and b in B:
                continue
            if a in B:
                nt[remain.index(b)] += R[(a, b)]
            elif b in B:
                nt[remain.index(a)] += R[(a, b)]
        norm = lambda x: 0 if x == 0 else (1 if x & 1 else 2)
        nt = tuple(map(norm, nt))
        nr = tuple(map(norm, nr))
        values.add(grundy(nt, nr) ^ (isolated & 1))
    mex = 0
    while mex in values:
        mex += 1
    return mex


def predicted(t, r):
    k = len(t)
    edges = list(combinations(range(k), 2))
    u = (sum(t) + sum(r)) & 1
    z = [(t[i] + sum(v for e, v in zip(edges, r) if i in e)) & 1
         for i in range(k)]
    return (1 ^ u ^ z[0]) if len(set(z)) == 1 else 2 + u


def canonical_masks(k):
    edges = list(combinations(range(k), 2))
    index = {e: i for i, e in enumerate(edges)}
    maps = [tuple(index[tuple(sorted((p[a], p[b])))] for a, b in edges)
            for p in permutations(range(k))]
    representatives = set()
    for mask in range(1 << len(edges)):
        missing = [e for i, e in enumerate(edges) if mask >> i & 1]
        if any(sum(v in e for e in missing) > 2 for v in range(k)):
            continue
        representatives.add(min(
            sum(1 << mapping[i] for i in range(len(edges)) if mask >> i & 1)
            for mapping in maps))
    return sorted(representatives)


def check(k, mask, expected_failures=0):
    edges = list(combinations(range(k), 2))
    present = [i for i in range(len(edges)) if not (mask >> i & 1)]
    checked = failures = 0
    for leaves in product(range(3), repeat=k):
        for values in product((1, 2), repeat=len(present)):
            pairs = [0] * len(edges)
            for j, v in zip(present, values):
                pairs[j] = v
            pairs = tuple(pairs)
            got = grundy(leaves, pairs)
            want = predicted(leaves, pairs)
            checked += 1
            if got != want:
                failures += 1
    assert failures == expected_failures, (k, mask, failures)
    return checked, failures


def main():
    import sys
    if len(sys.argv) != 2:
        raise SystemExit("run each of: python3 verify_python.py 4, 5, 6a, 6b")
    part = sys.argv[1]
    start = monotonic()
    if part == "4":
        edges = list(combinations(range(4), 2))
        total = failures = 0
        for mask in range(1 << 6):
            missing = [e for i, e in enumerate(edges) if mask >> i & 1]
            if any(sum(v in e for e in missing) > 2 for v in range(4)):
                continue
            expected = int(len(missing) == 3 and
                           len({v for e in missing for v in e}) == 3)
            c, f = check(4, mask, expected)
            total += c
            failures += f
        assert (total, failures) == (51516, 4)
        print(f"k4 labelled: {total} configurations, {failures} counterexamples")
    elif part == "5":
        reps = canonical_masks(5)
        assert len(reps) == 11
        total = sum(check(5, mask)[0] for mask in
                    sorted(reps, key=int.bit_count, reverse=True))
        assert total == 645408
        print(f"k5: {len(reps)} missing-graph classes, {total} configurations, 0 failures")
    elif part in ("6a", "6b"):
        edges = list(combinations(range(6), 2))
        missing = ({(0,1),(1,2),(2,3),(3,4),(4,5),(0,5)} if part == "6a"
                   else {(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)})
        mask = sum(1 << i for i, e in enumerate(edges) if e in missing)
        total, failures = check(6, mask)
        assert (total, failures) == (373248, 0)
        print(f"k6 {part}: {total} configurations, 0 failures")
    else:
        raise SystemExit("expected 4, 5, 6a or 6b")
    print(f"elapsed {monotonic()-start:.1f}s")


if __name__ == "__main__":
    main()

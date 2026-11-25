#!/usr/bin/env python3
"""Exact all-d counterexample for the dense binary-hypercube hyperplane game.

Two independent safe-position predicates are compared: a five-clause
Boolean reduction and direct evaluation of every coordinate/XOR face.
Only 2**7 local positions are needed, even when the dimension is large.
"""
from collections import Counter

A = (1, 2, 6, 7, 9, 11, 16)
Y = 3
CLAUSES = ((16,), (6, 7), (9, 11), (2, 6), (1, 9))
MINIMAL = ((6, 9, 16), (2, 7, 9, 16),
           (1, 6, 11, 16), (1, 2, 7, 11, 16))


def clause_safe(mask):
    u = {A[i] for i in range(7) if mask & (1 << i)}
    return all(u.intersection(clause) for clause in CLAUSES)


def direct_safe(mask, n):
    """Hit all 2*d coordinate and d*(d-1) diagonal forbidden faces."""
    assert n >= 0
    d = 5 + n
    t = [x for i, x in enumerate(A) if mask & (1 << i)]
    t += [Y | (1 << (5 + j)) for j in range(n)]
    for i in range(d):
        vals = {(x >> i) & 1 for x in t}
        if len(vals) != 2:
            return False
    for i in range(d):
        for j in range(i):
            vals = {((x >> i) ^ (x >> j)) & 1 for x in t}
            if len(vals) != 2:
                return False
    return True


def mex(values):
    x = 0
    while x in values:
        x += 1
    return x


def nimbers(predicate):
    values = [None] * 128
    for size in range(8):
        for mask in range(128):
            if mask.bit_count() != size or not predicate(mask):
                continue
            children = [values[mask ^ (1 << i)] for i in range(7)
                        if mask & (1 << i) and values[mask ^ (1 << i)] is not None]
            values[mask] = ((mex({v[0] for v in children}),
                             mex({v[1] for v in children})) if children else (0, 1))
    return values


def main():
    reference = nimbers(clause_safe)
    safe_masks = [mask for mask, val in enumerate(reference) if val is not None]
    assert len(safe_masks) == 25
    minimal_masks = [mask for mask in safe_masks
                     if not any(reference[mask ^ (1 << i)] is not None
                                for i in range(7) if mask & (1 << i))]
    minimal_sets = {frozenset(A[i] for i in range(7) if mask & (1 << i))
                    for mask in minimal_masks}
    assert minimal_sets == {frozenset(s) for s in MINIMAL}
    assert reference[127] == (0, 0)
    assert {A[i]: reference[127 ^ (1 << i)] for i in range(7)} == {
        1: (3, 3), 2: (3, 3), 6: (2, 2), 7: (3, 3),
        9: (2, 2), 11: (3, 3), 16: None}
    expected = {3: Counter({(0, 1): 1}),
                4: Counter({(1, 0): 4, (0, 1): 2}),
                5: Counter({(0, 1): 5, (1, 0): 4, (2, 2): 2}),
                6: Counter({(3, 3): 4, (2, 2): 2}),
                7: Counter({(0, 0): 1})}
    for size in range(3, 8):
        got = Counter(reference[mask] for mask in safe_masks
                      if mask.bit_count() == size)
        assert got == expected[size], (size, got)
        print(f'|U|={size}: {dict(sorted(got.items()))}')

    base = nimbers(lambda mask: direct_safe(mask, 0))
    assert sum(v is not None for v in base) == 18
    assert base[127] == (0, 0)
    assert {A[i]: base[127 ^ (1 << i)] for i in range(7)} == {
        1: (2, 2), 2: (2, 2), 6: (2, 2), 7: (2, 2),
        9: (2, 2), 11: (2, 2), 16: None}
    print('d=5: 18 safe subpositions, root=(0,0)')

    for n in (1, 2, 3, 4, 5, 6, 7, 10, 20):
        actual = nimbers(lambda mask: direct_safe(mask, n))
        assert actual == reference, (n, [(m, actual[m], reference[m])
                                        for m in range(128) if actual[m] != reference[m]])
        print(f'd={5+n}: all 128 predicates and 25 Grundy pairs agree; '
              'root=(0,0)')
    print('PASS: counterexample and exact finite game certificate for every d >= 5')


if __name__ == '__main__':
    main()

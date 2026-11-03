#!/usr/bin/env python3
"""Independent finite checks for the cycle-terminal real-rootedness proof.

Pure Python, no third-party packages. This does NOT prove real-rootedness;
the universal proof uses the claw-free independence-polynomial theorem.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb


def arcs(n):
    return [(s, length, frozenset((s + j) % n for j in range(length)))
            for s in range(n) for length in (2, 3)]


def find_claw(arc_list):
    for center, (_, _, support) in enumerate(arc_list):
        neighbors = [j for j, (_, _, other) in enumerate(arc_list)
                     if j != center and support & other]
        for triple in combinations(neighbors, 3):
            if all(not (arc_list[a][2] & arc_list[b][2])
                   for a, b in combinations(triple, 2)):
                return center, triple
    return None


def from_independent_arcs(n, r):
    arc_list = arcs(n)
    assert len(arc_list) == 2 * n
    occupied = [sum(1 << v for v in a[2]) for a in arc_list]
    deleted = [sum(1 << ((a[0] + j) % n) for j in range(a[1] - 1))
               for a in arc_list]
    coeff = defaultdict(int)
    seen_deleted = set()
    for selection in range(1 << len(arc_list)):
        union, zeros, short, k = 0, 0, 0, 0
        for i, (start, length, support) in enumerate(arc_list):
            if not ((selection >> i) & 1):
                continue
            if union & occupied[i]:
                break
            union |= occupied[i]
            zeros |= deleted[i]
            short += (length == 2)
            k += 1
        else:
            assert zeros not in seen_deleted, (n, selection, zeros)
            seen_deleted.add(zeros)
            # r^n I(H_r, u/r^3), after true-twin blowups.
            assert n + short - 3 * k >= 0
            coeff[k] += r ** (n + short - 3 * k)
    return [coeff[k] for k in range(n // 2 + 1)], seen_deleted


def from_dominating_sets(n, r):
    coeff = defaultdict(int)
    dominating_deleted = set()
    for deleted in range(1 << n):
        # Deleted vertices must have at least one retained neighbor.
        if any((deleted >> v) & 1 and
               (deleted >> ((v - 1) % n)) & 1 and
               (deleted >> ((v + 1) % n)) & 1
               for v in range(n)):
            continue
        retained_edges = sum(not ((deleted >> v) & 1) and
                             not ((deleted >> ((v + 1) % n)) & 1)
                             for v in range(n))
        defect = n - deleted.bit_count() - retained_edges
        assert 0 <= defect <= n // 2
        coeff[defect] += r ** retained_edges
        dominating_deleted.add(deleted)
    return [coeff[k] for k in range(n // 2 + 1)], dominating_deleted


def closed_formula(n, r):
    ans = [r ** n]
    for k in range(1, n // 2 + 1):
        value = sum(Fraction(n, k) * comb(k, j) *
                    comb(n - k - j - 1, k - 1) * r ** (n - 2*k - j)
                    for j in range(min(k, n - 2*k) + 1))
        assert value.denominator == 1
        ans.append(int(value))
    return ans


def check_newton(coeff):
    h = len(coeff) - 1
    for k in range(1, h):
        assert (coeff[k] ** 2 * k * (h - k) >=
                coeff[k - 1] * coeff[k + 1] *
                (k + 1) * (h - k + 1))


def main():
    claws = 0
    for n in range(3, 41):
        assert find_claw(arcs(n)) is None, n
        claws += 1
    cases = 0
    for n in range(3, 10):
        for r in (1, 2, 3, 5):
            from_arcs, arc_deleted = from_independent_arcs(n, r)
            from_sets, all_deleted = from_dominating_sets(n, r)
            assert arc_deleted == all_deleted, (n, r, 'bijection')
            assert from_arcs == from_sets == closed_formula(n, r), (n, r)
            check_newton(from_sets)
            cases += 1
    larger = 0
    for n in range(10, 121):
        for r in (1, 2, 3, 7):
            check_newton(closed_formula(n, r))
            larger += 1
    print(f'PASS: {claws} conflict graphs claw-free; '
          f'{cases} independent-arcs/direct-domination/formula exact comparisons; '
          f'{larger} exact Newton-inequality checks; zero mismatches.')


if __name__ == '__main__':
    main()

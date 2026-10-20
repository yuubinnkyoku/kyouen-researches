#!/usr/bin/env python3
"""Independent exact checks for history-adaptive local play under global scheduling.

No third-party packages. Python 3.11+. Uses exact rational arithmetic.
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
import random


def all_complexes(n):
    """All labelled downward-closed families of subsets of [n], with empty set."""
    subsets = 1 << n
    for family in range(1, 1 << subsets, 2):
        if all(not ((family >> mask) & 1) or all((family >> (mask ^ (1 << j))) & 1 for j in range(n) if mask >> j & 1) for mask in range(subsets)):
            yield frozenset(mask for mask in range(subsets) if family >> mask & 1)


def legal(complex_, history, n):
    occupied = sum(1 << x for x in history)
    return tuple(v for v in range(n) if not (occupied >> v & 1) and (occupied | (1 << v)) in complex_)


def local_weights(i, history, choices, seed):
    # Strictly positive, dependent on both the order of earlier local moves and
    # the candidate move. No other component's history enters this formula.
    h = (seed + 17 * (i + 1) + 29 * len(history)) % 97
    for x in history:
        h = (h * 23 + 11 * (x + 1)) % 97
    return tuple(1 + (h + 7 * (v + 1) + v * h) % 9 for v in choices)


def local_distribution(complex_, n, i, seed):
    @lru_cache(None)
    def rec(history):
        choices = legal(complex_, history, n)
        if not choices:
            return {frozenset(history): Fraction(1)}
        weights = local_weights(i, history, choices, seed)
        denominator = sum(weights)
        ans = defaultdict(Fraction)
        for v, w in zip(choices, weights):
            for terminal, prob in rec(history + (v,)).items():
                ans[terminal] += Fraction(w, denominator) * prob
        return dict(ans)
    return rec(())


def scheduler_weights(histories, available, seed):
    # Global scheduling can depend arbitrarily on *observed* local histories.
    h = seed * 13 + 1
    for i, history in enumerate(histories):
        h = (h * 31 + 19 * i + len(history)) % 997
        for v in history:
            h = (h * 37 + 7 * v + 1) % 997
    return tuple(1 + (h + i * 13 + len(histories[i]) * 5) % 11 for i in available)


def direct_global_distribution(complexes, sizes, seed):
    k = len(complexes)
    @lru_cache(None)
    def rec(histories):
        choices = [legal(complexes[i], histories[i], sizes[i]) for i in range(k)]
        available = tuple(i for i in range(k) if choices[i])
        if not available:
            return {tuple(frozenset(h) for h in histories): Fraction(1)}
        sw = scheduler_weights(histories, available, seed)
        sden = sum(sw)
        ans = defaultdict(Fraction)
        for i, cw in zip(available, sw):
            lw = local_weights(i, histories[i], choices[i], seed)
            lden = sum(lw)
            for v, vw in zip(choices[i], lw):
                child = list(histories)
                child[i] += (v,)
                p = Fraction(cw, sden) * Fraction(vw, lden)
                for terminal, prob in rec(tuple(child)).items():
                    ans[terminal] += p * prob
        return dict(ans)
    return rec(tuple(() for _ in range(k)))


def product_distribution(complexes, sizes, seed):
    local = [local_distribution(c, n, i, seed) for i, (c, n) in enumerate(zip(complexes, sizes))]
    ans = {}
    for tup in product(*(list(d.items()) for d in local)):
        terminal = tuple(x[0] for x in tup)
        prob = Fraction(1)
        for _, p in tup:
            prob *= p
        ans[terminal] = prob
    return ans


def length_poly(dist):
    p = defaultdict(Fraction)
    for terminal, weight in dist.items():
        p[sum(map(len, terminal))] += weight
    return dict(sorted(p.items()))


def check_case(complexes, sizes, seed):
    expected = product_distribution(complexes, sizes, seed)
    actual = direct_global_distribution(complexes, sizes, seed)
    assert expected == actual, (sizes, seed, expected, actual)
    assert sum(actual.values()) == 1
    return len(actual)


def main():
    counts = {}
    by_n = {n: list(all_complexes(n)) for n in (1, 2, 3, 4)}
    counts['downward_closed_families'] = {str(n): len(v) for n, v in by_n.items()}
    tests = 0
    max_terminals = 0
    for n in (1, 2, 3):
        for j, a in enumerate(by_n[n]):
            for h, b in enumerate(by_n[n]):
                max_terminals = max(max_terminals, check_case((a, b), (n, n), seed=23 + 7 * j + 11 * h))
                tests += 1
    counts['all_pairs_n1_to_n3'] = tests
    rng = random.Random(20261020)
    for _ in range(180):
        n1, n2 = rng.choice((2, 3, 4)), rng.choice((2, 3, 4))
        a, b = rng.choice(by_n[n1]), rng.choice(by_n[n2])
        max_terminals = max(max_terminals, check_case((a, b), (n1, n2), seed=rng.randrange(10000)))
        tests += 1
    counts['random_pairs_n2_to_n4'] = 180
    for _ in range(120):
        sizes = (rng.choice((2, 3)), rng.choice((2, 3)), rng.choice((2, 3)))
        complexes = tuple(rng.choice(by_n[n]) for n in sizes)
        max_terminals = max(max_terminals, check_case(complexes, sizes, seed=rng.randrange(10000)))
        tests += 1
    counts['random_triples_n2_to_n3'] = 120
    counts['total_cases'] = tests
    counts['max_terminal_tuples'] = max_terminals

    # Two independent path-of-three components, with local centre probabilities
    # 1/2 and 1/3 respectively. Scheduler remains history-adaptive.
    path3 = frozenset((0, 1, 2, 4, 5)) # {}, {0},{1},{2},{0,2}; binary 101=5
    # This test uses explicit fixed probabilities to make a human-readable example.
    def explicit_example():
        @lru_cache(None)
        def rec(histories):
            opts = [legal(path3, h, 3) for h in histories]
            avail = [i for i in (0, 1) if opts[i]]
            if not avail:
                return {tuple(frozenset(h) for h in histories): Fraction(1)}
            # Nonuniform, adaptive scheduling: prefer the component with fewer
            # occupied vertices, but still give the other a positive chance.
            sch = [1 + 2 * (len(histories[i]) == min(map(len, histories))) for i in avail]
            ans = defaultdict(Fraction)
            for i, sw in zip(avail, sch):
                if not histories[i]:
                    w = [2 if v == 1 else 1 for v in opts[i]] if i == 0 else [1, 1, 1]
                else:
                    w = [1] * len(opts[i])
                for v, vw in zip(opts[i], w):
                    child = list(histories)
                    child[i] += (v,)
                    for t, prob in rec(tuple(child)).items():
                        ans[t] += Fraction(sw, sum(sch)) * Fraction(vw, sum(w)) * prob
            return dict(ans)
        return length_poly(rec(((), ())))
    example = explicit_example()
    assert example == {2: Fraction(1, 6), 3: Fraction(1, 2), 4: Fraction(1, 3)}, example
    counts['path3_two_component_length_probability'] = {str(k): str(v) for k, v in example.items()}
    counts['path3_r3_loser_probability_from_player0'] = {str(k % 3): str(v) for k, v in example.items()}

    # Counterexample: component B resolves first with centre probability 1/2;
    # component A then chooses centre iff B chose centre. Cross-component
    # dependence of *within-A* probabilities breaks product factorisation.
    actual = defaultdict(Fraction)
    for b_first, p in ((1, Fraction(1, 2)), (0, Fraction(1, 4)), (2, Fraction(1, 4))):
        b_size = 1 if b_first == 1 else 2
        a_size = 1 if b_size == 1 else 2  # A reacts to B's outcome
        actual[a_size + b_size] += p
    actual = dict(actual)
    falsely_factored = {2: Fraction(1, 4), 3: Fraction(1, 2), 4: Fraction(1, 4)}
    assert actual != falsely_factored
    counts['cross_dependent_counterexample'] = {
        'actual': {str(k): str(v) for k, v in actual.items()},
        'product_of_marginals': {str(k): str(v) for k, v in falsely_factored.items()},
    }
    print(json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

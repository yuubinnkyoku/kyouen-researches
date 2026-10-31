#!/usr/bin/env python3
"""Independent bit-mask enumeration of terminal sets in two-carrier q-point games.

Only Python's standard library is required. The reference enumerator uses
point-labelled masks and tests maximality by trying every absent point; it
never uses the carrier-count classification in the proposed theorem.
"""
from collections import Counter
from itertools import product
from math import comb, factorial
from functools import lru_cache


def formula(q: int, a: int, b: int, c: int, z: int) -> Counter:
    assert q >= 4 and a >= 0 and b >= 0 and z >= 0 and 0 <= c <= 2
    x, y = q + a - c, q + b - c
    out = Counter()
    for t in range(c + 1):
        i = q - 1 - t
        if 0 <= i <= x and 0 <= i <= y:
            out[2 * (q - 1) - t + z] += comb(c, t) * comb(x, i) * comb(y, i)
    if c == 2 and a >= 1 and b == 0:
        out[2 * q - 3 + z] += comb(x, q - 1)
    if c == 2 and b >= 1 and a == 0:
        out[2 * q - 3 + z] += comb(y, q - 1)
    return +out


def independent_bruteforce(q: int, a: int, b: int, c: int, z: int) -> Counter:
    x, y = q + a - c, q + b - c
    n = x + y + c + z
    assert n <= 18
    mask_a = ((1 << x) - 1) | (((1 << c) - 1) << (x + y))
    mask_b = (((1 << y) - 1) << x) | (((1 << c) - 1) << (x + y))
    all_mask = (1 << n) - 1
    result = Counter()
    for state in range(1 << n):
        if (state & mask_a).bit_count() >= q or (state & mask_b).bit_count() >= q:
            continue
        # Check each candidate extension independently of the saturation formula.
        rest = all_mask ^ state
        maximal = True
        while rest:
            bit = rest & -rest
            rest -= bit
            child = state | bit
            if (child & mask_a).bit_count() < q and (child & mask_b).bit_count() < q:
                maximal = False
                break
        if maximal:
            result[state.bit_count()] += 1
    return +result


def independent_histories(q: int, a: int, b: int, c: int, z: int) -> Counter:
    """Enumerate ordered legal move sequences without terminal-set counts."""
    x, y = q + a - c, q + b - c
    n = x + y + c + z
    mask_a = ((1 << x) - 1) | (((1 << c) - 1) << (x + y))
    mask_b = (((1 << y) - 1) << x) | (((1 << c) - 1) << (x + y))
    all_mask = (1 << n) - 1

    @lru_cache(None)
    def visit(state: int) -> Counter:
        total = Counter()
        rest = all_mask ^ state
        found = False
        while rest:
            bit = rest & -rest
            rest -= bit
            child = state | bit
            if (child & mask_a).bit_count() >= q or (child & mask_b).bit_count() >= q:
                continue
            found = True
            total.update(visit(child))
        if not found:
            total[state.bit_count()] += 1
        return total

    return visit(0)


def main() -> None:
    cases = []
    for q in (4, 5):
        cases += [(q, a, b, c, z) for a, b, c, z in product(range(3), range(3), range(3), range(2))]
    for q in (6, 7):
        cases += [(q, a, b, c, z) for a, b, c, z in product(range(2), range(2), range(3), range(2))]
    total_states = 0
    total_terminals = 0
    for case in cases:
        q, a, b, c, z = case
        n = 2 * q + a + b - c + z
        total_states += 1 << n
        got = independent_bruteforce(*case)
        expected = formula(*case)
        assert got == expected, (case, got, expected)
        total_terminals += sum(got.values())
        expected_support = {2*q-2+z} if c == 0 else (
            {2*q-3+z, 2*q-2+z} if c == 1 else
            ({2*q-4+z, 2*q-3+z, 2*q-2+z} if a > 0 and b > 0
             else {2*q-4+z, 2*q-3+z}))
        assert set(got) == expected_support, (case, got, expected_support)
        assert sum(v * factorial(k) for k, v in got.items()) > 0
    histories_checked = 0
    for a, b, c, z in product(range(2), range(2), range(3), range(2)):
        case = (4, a, b, c, z)
        direct = independent_histories(*case)
        predicted = Counter({k: v * factorial(k) for k, v in formula(*case).items()})
        assert direct == predicted, (case, direct, predicted)
        histories_checked += 1
    print(f'PASS boards={len(cases)} all_subsets_examined={total_states} '
          f'maximal_sets={total_terminals} ordered_history_boards={histories_checked} mismatches=0')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Independent labelled-subset audit of sunflower quota parity/modulus laws."""
from functools import lru_cache
from itertools import product
from math import gcd, comb, factorial


def predicted(c, xs, ps, z=0):
    J = min(c, *ps)
    j0 = min(J, max(0, min(p - x for p, x in zip(ps, xs))))
    F = [z + j + sum(min(x, p - j) for x, p in zip(xs, ps))
         for j in range(j0, J + 1)]
    steps = [sum(p - x <= j for p, x in zip(ps, xs)) - 1
             for j in range(j0, J)]
    delta = 0
    for d in steps:
        delta = gcd(delta, d)
    return F, delta, steps


def brute(c, xs, ps, z=0, full_values=False):
    n = c + sum(xs) + z
    assert n <= 12
    carriers = []
    off = c
    core = (1 << c) - 1
    for x in xs:
        carriers.append(core | (((1 << x) - 1) << off))
        off += x
    legal = [all((mask & A).bit_count() <= p for A, p in zip(carriers, ps))
             for mask in range(1 << n)]
    nexts = [[] for _ in legal]
    terminals = []
    for mask, ok in enumerate(legal):
        if not ok:
            continue
        nexts[mask] = [mask | (1 << i) for i in range(n)
                       if not (mask >> i & 1) and legal[mask | (1 << i)]]
        if not nexts[mask]:
            terminals.append(mask)
    lengths = sorted({mask.bit_count() for mask in terminals}, reverse=True)
    delta = 0
    for x in lengths[1:]:
        delta = gcd(delta, lengths[0] - x)

    @lru_cache(None)
    def values(mask):
        children = nexts[mask]
        if not children:
            return (0, 1)
        gs = {values(ch)[0] for ch in children}
        hs = {values(ch)[1] for ch in children}
        g = h = 0
        while g in gs:
            g += 1
        while h in hs:
            h += 1
        return (g, h)

    if full_values:
        all_values = {mask: values(mask) for mask, ok in enumerate(legal) if ok}
    else:
        all_values = {0: values(0)}
    return lengths, delta, all_values, len(terminals), sum(legal), carriers


def nonredundant(c, xs, ps):
    n = c + sum(xs)
    core = (1 << c) - 1
    carriers = []
    off = c
    for x in xs:
        carriers.append(core | (((1 << x) - 1) << off))
        off += x
    for i in range(len(xs)):
        if not any((s & carriers[i]).bit_count() > ps[i] and
                   all((s & carriers[j]).bit_count() <= ps[j]
                       for j in range(len(xs)) if j != i)
                   for s in range(1 << n)):
            return False
    return True


def run():
    boards = states = parity_boards = mixed_boards = 0
    for r in (2, 3, 4):
        for c in range(4):
            for xs in product(range(3), repeat=r):
                for ps in product(range(1, 4), repeat=r):
                    n = c + sum(xs)
                    if n > 9:
                        continue
                    for z in (0, 1):
                        F, d, steps = predicted(c, xs, ps, z)
                        lens, d2, vals, terminals, safe, carriers = brute(c, xs, ps, z, True)
                        assert lens == sorted(set(F), reverse=True), (c, xs, ps, z, lens, F)
                        assert d == d2, (c, xs, ps, z, d, d2)
                        assert (d % 2 == 0) == all(g <= 1 for g, h in vals.values()), (c, xs, ps, z)
                        if d % 2 == 0:
                            eps = F[0] % 2
                            assert all((g, h) == ((eps - mask.bit_count()) % 2,
                                                   1 - (eps - mask.bit_count()) % 2)
                                       for mask, (g, h) in vals.items())
                            parity_boards += 1
                        else:
                            mixed_boards += 1
                        boards += 1
                        states += safe
    print(f'PASS general boards={boards} safe_states={states} parity={parity_boards} mixed={mixed_boards}')

    # Every three-carrier irredundant short-petal example with fewer than 8
    # named points, positive core and nonempty petals, is tested exhaustively.
    checked = 0
    counter = None
    for n in range(4, 9):
        for c in range(1, n - 2):
            for xs in product(range(1, n), repeat=3):
                if c + sum(xs) != n:
                    continue
                for ps in product(*(range(1, c + x) for x in xs)):
                    if all(x >= p for x, p in zip(xs, ps)):
                        continue
                    if not nonredundant(c, xs, ps):
                        continue
                    checked += 1
                    lens, d, vals, *_ = brute(c, xs, ps)
                    g = vals[0][0]
                    if g != sum(ps) % 2:
                        item = (n, c, xs, ps, g, sum(ps) % 2, lens)
                        if counter is None or item < counter:
                            counter = item
        if counter is not None:
            break
    print(f'PASS minimality checked_irredundant_short={checked} first_counterexample={counter}')
    assert counter == (8, 3, (1, 2, 2), (3, 3, 3), 3, 1, [6, 5, 3])
    lens, d, vals, terminal_count, safe, _ = brute(3, (1, 2, 2), (3, 3, 3), full_values=True)

    # Enumerate ordered maximal plays, independently of the binomial
    # maximal-set formula. Compare the total and the losing player by modulus.
    n = 8
    all_safe = set(vals)
    by_length = {}
    by_loser = {t: {} for t in range(2, 6)}
    def walk(mask, length):
        children = [mask | (1 << i) for i in range(n)
                    if not (mask >> i & 1) and (mask | (1 << i)) in all_safe]
        if not children:
            by_length[length] = by_length.get(length, 0) + 1
            for t in by_loser:
                j = length % t
                by_loser[t][j] = by_loser[t].get(j, 0) + 1
        else:
            for child in children:
                walk(child, length + 1)
    walk(0, 0)
    F, _, _ = predicted(3, (1, 2, 2), (3, 3, 3))
    formula_hist = {}
    for j in range(1, 4):
        length = F[j - 1]
        count = comb(3, j)
        for x, p in zip((1, 2, 2), (3, 3, 3)):
            count *= comb(x, min(x, p - j))
        formula_hist[length] = formula_hist.get(length, 0) + count * factorial(length)
    assert by_length == formula_hist == {6: 2160, 5: 1440, 3: 6}
    for t, actual in by_loser.items():
        expected = {}
        for length, count in formula_hist.items():
            expected[length % t] = expected.get(length % t, 0) + count
        assert actual == expected
    print(f'PASS witness terminal_lengths={lens} delta={d} root={vals[0]} safe_states={safe} terminal_sets={terminal_count} histories={by_length}')
    print('PASS all')


if __name__ == '__main__':
    run()

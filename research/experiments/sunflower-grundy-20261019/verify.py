#!/usr/bin/env python3
"""Two independent checks: closed form vs literal occupied-subset game tree."""
from functools import lru_cache
from itertools import combinations_with_replacement
import json


def formula(c, petals, free=0):
    h = len(petals)
    assert h >= 1 and all(p > 0 for p in petals) and c >= 0
    n = c + sum(petals)
    if h & 1:
        ans = (n - 1) & 1
    elif c < min(petals):
        ans = n & 1
    elif c > min(petals):
        ans = (n - 1) & 1
    else:
        ans = 2 + (sum(petals) & 1)
    return ans ^ (free & 1)


def compressed(c, petals):
    """Recurrence on remaining block sizes, independent of formula."""
    @lru_cache(None)
    def rec(k, p):
        if k == 0:
            return sum((x - 1) & 1 for x in p) & 1
        opts = {rec(k - 1, p)}
        for i, x in enumerate(p):
            if x == 1:
                # A completed petal bans the last core point; other petals free.
                opts.add((k + sum(p)) & 1)
            else:
                q = list(p)
                q[i] -= 1
                opts.add(rec(k, tuple(sorted(q))))
        g = 0
        while g in opts:
            g += 1
        return g
    return rec(c, tuple(sorted(petals)))


def literal(c, petals, free=0):
    """Enumerate all safe occupied subsets, with geometric-free hyperedges."""
    n = c + sum(petals) + free
    core = (1 << c) - 1
    edges = []
    start = c
    for p in petals:
        edge = core | (((1 << p) - 1) << start)
        edges.append(edge)
        start += p
    total = 1 << n
    safe = bytearray(total)
    for s in range(total):
        safe[s] = int(not any((s & e) == e for e in edges))
    grundy = [-1] * total
    count = 0
    for s in range(total - 1, -1, -1):
        if not safe[s]:
            continue
        count += 1
        options = set()
        unplayed = (total - 1) ^ s
        while unplayed:
            bit = unplayed & -unplayed
            unplayed ^= bit
            t = s | bit
            if safe[t]:
                options.add(grundy[t])
        g = 0
        while g in options:
            g += 1
        grundy[s] = g
        # Independent check at EVERY safe state, including degenerate states.
        rem_core = c - (s & core).bit_count()
        rem = []
        start = c
        for p in petals:
            mask = ((1 << p) - 1) << start
            rem.append(p - (s & mask).bit_count())
            start += p
        rem_free = free - ((s >> start).bit_count())
        if rem_core == 0:
            # Each petal is now an independent edge.
            expected = (sum((p - 1) & 1 for p in rem) & 1) ^ (rem_free & 1)
        elif 0 in rem:
            # A completed petal forces the core to remain incomplete;
            # all other petal vertices are now unconstrained.
            expected = ((rem_core - 1) & 1) ^ ((sum(rem)) & 1) ^ (rem_free & 1)
        else:
            expected = formula(rem_core, rem, rem_free)
        if g != expected:
            raise AssertionError((c, petals, free, s, g, expected))
    if grundy[0] != formula(c, petals, free):
        raise AssertionError((c, petals, free, grundy[0]))
    return count, max(grundy)


def main():
    cases = 0
    states = 0
    maxima = {}
    by_h = {}
    # Exhaustive parameters in specified bounded ranges; not a proof of unbounded theorem.
    for h in range(1, 5):
        for c in range(0, 4):
            for petals in combinations_with_replacement(range(1, 4), h):
                for free in range(0, 2):
                    n = c + sum(petals) + free
                    if n > 15:
                        continue
                    direct, maximum = literal(c, petals, free)
                    if compressed(c, petals) ^ (free & 1) != formula(c, petals, free):
                        raise AssertionError(('compressed', c, petals, free))
                    cases += 1
                    states += direct
                    by_h[h] = by_h.get(h, 0) + 1
                    maxima[maximum] = maxima.get(maximum, 0) + 1
    # Additional larger-h coverage, all petal sizes in {1,2}.
    for h in (5, 6, 7):
        for c in (0, 1, 2):
            for petals in combinations_with_replacement((1, 2), h):
                n = c + sum(petals)
                if n > 16:
                    continue
                direct, maximum = literal(c, petals)
                if compressed(c, petals) != formula(c, petals):
                    raise AssertionError(('compressed', c, petals))
                cases += 1
                states += direct
                by_h[h] = by_h.get(h, 0) + 1
                maxima[maximum] = maxima.get(maximum, 0) + 1
    # Sharpness for all even h: one singleton core, h-1 singleton petals,
    # one 2-vertex petal => Grundy 3.
    for h in range(2, 101, 2):
        petals = (1,) * (h - 1) + (2,)
        assert formula(1, petals) == 3
        assert compressed(1, petals) == 3
    result = dict(cases=cases, safe_states_checked=states,
                  cases_by_edge_count=by_h, max_nimber_histogram=maxima,
                  even_h_sharpness_range=[2, 100], status='PASS')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

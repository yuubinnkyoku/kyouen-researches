#!/usr/bin/env python3
"""Independent full-state mex audit of the all-slack top-h/tail-parity kernel.

No use of the kernel in the reference evaluator; it enumerates actual sorted
occupancy vectors and follows every legal coordinate increment.
"""

import argparse
from functools import lru_cache
from itertools import combinations_with_replacement


def mex(values):
    values = set(values)
    k = 0
    while k in values:
        k += 1
    return k


def make_kernel(w, h, m, r):
    n = w - h

    @lru_cache(None)
    def f(top):
        successors = set()
        if sum(top) < r:
            for i in range(h):
                if top[i] < m:
                    nxt = list(top)
                    nxt[i] += 1
                    successors.add(f(tuple(sorted(nxt, reverse=True))))
        parity = (n * top[-1]) & 1
        return mex(v ^ parity for v in successors) ^ parity

    return f


def make_reference(w, h, m, r):
    @lru_cache(None)
    def grundy(x):
        successors = set()
        for i in range(w):
            if x[i] == m:
                continue
            nxt = list(x)
            nxt[i] += 1
            nxt.sort(reverse=True)
            nxt = tuple(nxt)
            if sum(nxt[:h]) <= r:
                successors.add(grundy(nxt))
        return mex(successors)

    return grundy


def audit(max_w, max_m):
    cases = states = h3_states = max_h3 = 0
    for w in range(2, max_w + 1):
        for h in range(1, w):
            for m in range(1, max_m + 1):
                all_states = [tuple(reversed(t)) for t in combinations_with_replacement(range(m + 1), w)]
                for r in range(h * m + 1):
                    cases += 1
                    f = make_kernel(w, h, m, r)
                    reference = make_reference(w, h, m, r)
                    for x in all_states:
                        if sum(x[:h]) > r:
                            continue
                        states += 1
                        actual = reference(x)
                        predicted = f(x[:h]) ^ (sum(x[h:]) & 1)
                        if predicted != actual:
                            raise AssertionError((w, h, m, r, x, predicted, actual))
                        bound = h + (h % 2 == 0)
                        if actual > bound:
                            raise AssertionError(('bound', w, h, m, r, x, actual, bound))
                        if h == 3:
                            h3_states += 1
                            max_h3 = max(max_h3, actual)
    print(f'PASS cases={cases} states={states} h3_states={h3_states} max_h3={max_h3}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--extended', action='store_true', help='w<=8, m<=7 rather than w<=7, m<=6')
    args = parser.parse_args()
    audit(8 if args.extended else 7, 7 if args.extended else 6)

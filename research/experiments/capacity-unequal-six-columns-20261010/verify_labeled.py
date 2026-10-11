#!/usr/bin/env python3
"""Independent labeled-state, reverse-index mex scan (no symmetry quotient, no recursion)."""
from itertools import combinations_with_replacement
from math import prod
from collections import defaultdict
import sys


def evaluate(c, h, r):
    w = len(c)
    strides = [prod(t + 1 for t in c[:i]) for i in range(w)]
    n = prod(t + 1 for t in c)
    sg = [-1] * n
    nstates = 0
    max_g = 0
    example = None
    for idx in range(n - 1, -1, -1):
        x = tuple((idx // strides[i]) % (c[i] + 1) for i in range(w))
        if sum(sorted(x, reverse=True)[:h]) > r:
            continue
        child_values = set()
        for i in range(w):
            if x[i] == c[i]:
                continue
            y = x[:i] + (x[i] + 1,) + x[i + 1:]
            if sum(sorted(y, reverse=True)[:h]) <= r:
                g = sg[idx + strides[i]]
                assert g >= 0, (c, h, r, x, y)
                child_values.add(g)
        g = 0
        while g in child_values:
            g += 1
        sg[idx] = g
        nstates += 1
        if g > max_g:
            max_g, example = g, x
    return max_g, nstates, example


def main():
    maxcap = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    assert 1 <= maxcap <= 5
    summary = defaultdict(lambda: [0, 0, 0, None])
    for c in combinations_with_replacement(range(1, maxcap + 1), 6):
        for h in range(2, 6):
            for r in range(2, sum(c[-h:])):
                g, states, example = evaluate(c, h, r)
                rec = summary[h]
                rec[0] += 1
                rec[1] += states
                if g > rec[2]:
                    rec[2] = g
                    rec[3] = (c, r, example)
                assert g <= 5
    for h in range(2, 6):
        rec = summary[h]
        print(f'h={h}; configs={rec[0]}; labeled_states={rec[1]}; max_g={rec[2]}; example={rec[3]}')
    print('VERIFIED: no six-column state with g>=6 for capacities<=', maxcap)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Exact all-real-parameter classification for det[x²+lambda*y²,x,y,1]."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json


def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def coefficients(points):
    x, y = points[-1]
    b = det3(*[(u*u-x*x, u-x, v-y) for u, v in points[:-1]])
    a = det3(*[(v*v-y*y, u-x, v-y) for u, v in points[:-1]])
    return a, b


def partition(points):
    universal, exceptional = [], {}
    for ids in combinations(range(len(points)), 4):
        a, b = coefficients([points[i] for i in ids])
        mask = sum(1 << i for i in ids)
        if a:
            exceptional.setdefault(Fraction(-b, a), []).append(mask)
        elif not b:
            universal.append(mask)
    return universal, exceptional


def solve(n, edges):
    """Bottom-up subset DP; unsafe supersets are marked before mex evaluation."""
    size = 1 << n
    safe = bytearray([1])*size
    for edge in edges:
        complement = (size-1) ^ edge
        sub = complement
        while True:
            safe[edge | sub] = 0
            if not sub:
                break
            sub = (sub-1) & complement
    values = bytearray(size)
    histogram, terminal = Counter(), Counter()
    for state in range(size-1, -1, -1):
        if not safe[state]:
            continue
        options = 0
        remaining = (size-1) ^ state
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            child = state | bit
            if safe[child]:
                options |= 1 << values[child]
        g = 0
        while options >> g & 1:
            g += 1
        values[state] = g
        histogram[g] += 1
        if not options:
            terminal[state.bit_count()] += 1
    return {
        'edges': len(edges), 'safe_states': sum(safe), 'root_grundy': values[0],
        'first_move_grundy': [values[1 << i] for i in range(n)],
        'maximum_safe_size': max(terminal),
        'terminal_size_histogram': dict(sorted(terminal.items())),
        'grundy_histogram': dict(sorted(histogram.items())),
    }, safe, values


def main():
    report = {'rule': 'det[x^2+lambda*y^2,x,y,1]=0; all degeneracies included',
              'parameter_domain': 'all real numbers', 'boards': []}
    for n in (2, 3, 4):
        points = [(x, y) for y in range(n) for x in range(n)]
        universal, exceptional = partition(points)
        generic, _, _ = solve(n*n, universal)
        cases = []
        for value, added in sorted(exceptional.items()):
            profile, _, _ = solve(n*n, universal+added)
            cases.append({'lambda': str(value), 'added_edges': len(added), **profile})
        board = {'n': n, 'point_order': points, 'universal_edges': len(universal),
                 'exception_count': len(cases), 'generic': generic, 'exceptions': cases}
        report['boards'].append(board)
        print(f'n={n}: {len(cases)} exceptional values; generic g={generic["root_grundy"]}', flush=True)
    destination = Path(__file__).with_name('results.json')
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')


if __name__ == '__main__':
    main()

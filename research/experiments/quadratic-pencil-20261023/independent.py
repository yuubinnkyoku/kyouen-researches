#!/usr/bin/env python3
"""Permutation 4x4 determinants + top-down legal-move recursion, independent audit."""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from pathlib import Path
import json

from classify import partition, solve


PERMS = [(p, (-1)**sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4)))
         for p in permutations(range(4))]


def determinant(matrix):
    result = 0
    for p, sign in PERMS:
        term = sign
        for i in range(4):
            term *= matrix[i][p[i]]
        result += term
    return result


def independent_partition(points):
    universal, exceptional = set(), {}
    for ids in combinations(range(len(points)), 4):
        selected = [points[i] for i in ids]
        b = determinant([[x*x, x, y, 1] for x, y in selected])
        a = determinant([[y*y, x, y, 1] for x, y in selected])
        mask = sum(1 << i for i in ids)
        if a:
            exceptional.setdefault(Fraction(-b, a), set()).add(mask)
        elif b == 0:
            universal.add(mask)
    return universal, exceptional


def audit(n, edges, safe, expected):
    by_point = [[] for _ in range(n)]
    for edge in edges:
        for p in range(n):
            if edge >> p & 1:
                by_point[p].append(edge)

    @lru_cache(None)
    def grundy(state):
        children = set()
        for p in range(n):
            if state >> p & 1:
                continue
            child = state | (1 << p)
            if all(child & edge != edge for edge in by_point[p]):
                children.add(grundy(child))
        value = 0
        while value in children:
            value += 1
        assert safe[state] and expected[state] == value, (n, state, value, expected[state])
        return value

    grundy(0)
    # Every safe subset is reachable because forbidden-set safety is hereditary.
    assert grundy.cache_info().currsize == sum(safe)
    return grundy.cache_info().currsize


def main():
    original = json.loads(Path(__file__).with_name('results.json').read_text())
    receipt = {'determinant': '24-term 4x4 permutation expansion',
               'game': 'top-down recursion with per-point forbidden-edge lists', 'boards': []}
    for board in original['boards']:
        n = board['n']
        points = [(x, y) for y in range(n) for x in range(n)]
        universal, exceptions = independent_partition(points)
        first, second = partition(points)
        assert universal == set(first)
        assert exceptions == {k: set(v) for k, v in second.items()}
        profiles = [(None, board['generic'])] + [(Fraction(c['lambda']), c) for c in board['exceptions']]
        states = 0
        for value, saved in profiles:
            edges = sorted(universal | (exceptions[value] if value is not None else set()))
            profile, safe, expected = solve(n*n, edges)
            # JSON changes integer histogram keys to strings.
            profile = json.loads(json.dumps(profile))
            assert all(profile[k] == saved[k] for k in profile)
            states += audit(n*n, edges, safe, expected)
        # Coordinate exchange proves reciprocal parameters have isomorphic games.
        by_value = {Fraction(c['lambda']): c for c in board['exceptions']}
        for value, case in by_value.items():
            if value:
                other = by_value[1/value]
                for key in ('root_grundy', 'safe_states', 'maximum_safe_size',
                            'terminal_size_histogram', 'grundy_histogram'):
                    assert case[key] == other[key]
                for y in range(n):
                    for x in range(n):
                        assert case['first_move_grundy'][y*n+x] == other['first_move_grundy'][x*n+y]
        receipt['boards'].append({'n': n, 'parameter_types': len(profiles),
                                   'all_safe_state_comparisons': states, 'passed': True})
        print(receipt['boards'][-1], flush=True)
    Path(__file__).with_name('audit.json').write_text(json.dumps(receipt, indent=2)+'\n')


if __name__ == '__main__':
    main()

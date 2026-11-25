#!/usr/bin/env python3
"""Finite audit of exact winning-move classification (physical columns and cells)."""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement


def run(wmax=8, mmax=6):
    stats = Counter()
    examples = {}
    for w in range(3, wmax + 1):
        for h in range(2, w):
            n = w - h
            for m in range(1, mmax + 1):
                states = [tuple(reversed(z)) for z in combinations_with_replacement(range(m + 1), w)]
                for r in range(1, h * m):
                    @lru_cache(None)
                    def signature(u):
                        sigma = r - sum(u)
                        if sigma == 0:
                            return ('even', 0)
                        children = set()
                        for i, v in enumerate(u):
                            if v < m:
                                z = list(u)
                                z[i] += 1
                                children.add(tuple(sorted(z, reverse=True)))
                        assert children
                        if sigma % 2:
                            phases = set()
                            for v in children:
                                typ, a = signature(v)
                                assert typ == 'even'
                                phases.add((n * (v[-1] - u[-1]) + a) % 2)
                            return ('odd-single', next(iter(phases))) if len(phases) == 1 else ('odd-mixed', None)
                        phases = set()
                        for v in children:
                            typ, a = signature(v)
                            if typ == 'odd-single':
                                phases.add((n * (v[-1] - u[-1]) + a + 1) % 2)
                        assert len(phases) <= 1
                        return ('even', (next(iter(phases)) + 1) % 2 if phases else 0)

                    @lru_cache(None)
                    def direct_g(x):
                        values = set()
                        for i in range(w):
                            if x[i] == m:
                                continue
                            z = list(x)
                            z[i] += 1
                            z.sort(reverse=True)
                            if sum(z[:h]) <= r:
                                values.add(direct_g(tuple(z)))
                        mex = 0
                        while mex in values:
                            mex += 1
                        return mex

                    for x in states:
                        if sum(x[:h]) > r:
                            continue
                        u = x[:h]
                        b = u[-1]
                        R = n * b - sum(x[h:])
                        sigma = r - sum(u)
                        typ, a = signature(u)
                        g = direct_g(x)
                        pred_g = ((R + a) % 2 if typ == 'even' else
                                  (R + a + 1) % 2 if typ == 'odd-single' else 2 + R % 2)
                        assert g == pred_g
                        stats['positions'] += 1
                        stats[f'g{g}'] += 1
                        wins = 0
                        win_cells = 0
                        lower_wins = 0
                        upper_wins = 0
                        lower_moves = 0
                        upper_moves = 0
                        for i, height in enumerate(x):
                            if height == m:
                                continue
                            z = list(x)
                            z[i] += 1
                            z.sort(reverse=True)
                            if sum(z[:h]) > r:
                                continue
                            z = tuple(z)
                            child_g = direct_g(z)
                            lower = height < b
                            if lower:
                                lower_moves += 1
                                # The central theorem: every legal lower move wins iff g=1.
                                assert (child_g == 0) == (g == 1), (w,h,m,r,x,i,g,child_g)
                                # When g=2/3 the lower child must have the other value 3/2.
                                if g >= 2:
                                    assert child_g == 5 - g
                            else:
                                upper_moves += 1
                                v = z[:h]
                                child_type, child_a = signature(v)
                                if sigma % 2:
                                    assert child_type == 'even'
                                    phase = (n * (v[-1] - b) + child_a) % 2
                                    expected_win = (R + phase) % 2 == 0
                                else:
                                    expected_win = (child_type == 'odd-single' and g == 1)
                                assert (child_g == 0) == expected_win, (w,h,m,r,x,i,g,child_g)
                            if child_g == 0:
                                wins += 1
                                win_cells += m - height
                                if lower:
                                    lower_wins += 1
                                else:
                                    upper_wins += 1
                        assert (wins > 0) == (g != 0)
                        if typ == 'odd-single' and g == 1:
                            assert wins == lower_moves + upper_moves
                        if typ == 'odd-mixed':
                            assert g in (2,3)
                            assert lower_wins == 0 and 0 < upper_wins < upper_moves
                        if g == 1:
                            assert lower_wins == lower_moves
                        stats['legal_columns'] += lower_moves + upper_moves
                        stats['winning_columns'] += wins
                        stats['winning_cells'] += win_cells
                        stats['lower_columns'] += lower_moves
                        stats['lower_winning'] += lower_wins
                        stats['upper_winning'] += upper_wins
                        if g in (2,3) and f'g{g}' not in examples:
                            examples[f'g{g}'] = (w,h,m,r,x,wins,upper_moves,lower_moves)
    print('PASS', dict(stats))
    print('EXAMPLES', examples)


if __name__ == '__main__':
    run()

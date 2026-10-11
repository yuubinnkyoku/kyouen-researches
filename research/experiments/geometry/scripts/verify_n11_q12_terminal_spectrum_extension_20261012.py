#!/usr/bin/env python3
"""Verify every missing maximal-safe size on the 11x11 q=12 board.

The existing extrema verifier supplies TWO independently enumerated sets
of all 21 forbidden circles and the complete 7..18 transversal bounds.
This verifier checks ten additional coordinate witnesses via bit masks.
"""
from pathlib import Path
from runpy import run_path

N = 11
WITNESSES = {
 8: [(4,0),(4,6),(4,10),(6,2),(6,8),(6,10),(8,1),(8,5)],
 9: [(1,1),(2,8),(3,6),(3,10),(4,1),(5,10),(6,8),(8,3),(10,2)],
10: [(1,0),(1,1),(1,2),(1,3),(2,4),(4,4),(6,4),(7,2),(7,8),(9,6)],
11: [(2,4),(4,6),(6,4),(6,6),(7,2),(7,5),(7,8),(8,3),(8,9),(9,9),(10,2)],
12: [(0,2),(0,3),(0,5),(2,4),(2,7),(2,8),(3,5),(3,10),(4,4),(4,6),(8,3),(10,2)],
13: [(0,2),(1,7),(1,8),(2,3),(3,10),(4,4),(4,6),(6,6),(7,2),(8,2),(8,3),(9,7),(10,2)],
14: [(0,2),(1,3),(2,0),(2,8),(3,1),(3,5),(3,10),(4,4),(4,6),(5,8),(5,10),(6,6),(8,8),(10,2)],
15: [(0,2),(0,3),(1,0),(1,3),(2,2),(2,8),(3,1),(3,5),(4,4),(4,6),(5,10),(6,4),(8,2),(8,8),(10,2)],
16: [(0,2),(1,0),(1,3),(2,0),(2,2),(2,8),(3,1),(3,5),(4,4),(4,6),(5,10),(6,4),(6,6),(8,2),(8,8),(10,2)],
17: [(1,0),(2,1),(2,2),(2,8),(3,9),(4,4),(4,6),(5,7),(6,4),(6,6),(7,1),(7,5),(7,9),(8,2),(8,8),(8,10),(10,8)],
}


def verify():
    prior = run_path(str(Path(__file__).with_name(
        'verify_n11_q12_terminal_extremes_20261012.py')))
    edges = [sum(1 << p for p in edge) for edge in prior['EDGES']]
    assert len(edges) == 21 and all(e.bit_count() == 12 for e in edges)
    for k, points in sorted(WITNESSES.items()):
        assert len(points) == len(set(points)) == k
        assert all(0 <= x < N and 0 <= y < N for x, y in points)
        mask = sum(1 << (N*y+x) for x, y in points)
        assert all(mask & e for e in edges), ('unhit circle', k)
        for x, y in points:
            p = 1 << (N*y+x)
            assert any((mask & e) == p for e in edges), ('redundant point', k, (x,y))
        print(f'k={k:2d}, maximal-safe={N*N-k:3d}: verified')
    print('COMPLETE spectrum of maximal-safe sizes: all integers 103..114')


if __name__ == '__main__':
    verify()

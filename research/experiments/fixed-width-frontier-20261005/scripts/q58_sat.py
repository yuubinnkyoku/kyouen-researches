#!/usr/bin/env python3
"""Exact necessary-condition SAT search for deficient maximal 5xm, q=8.

Geometry generation uses chord differences, not floating point.  SAT UNSAT
is reported as computation, not as an independently checked proof artifact.
The python-sat dependency is external to the repository's locked environment.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from math import isqrt
from pathlib import Path
import sys
import time

if not __debug__:
    raise SystemExit('Exact validation requires assertions; do not run Python with -O.')


def chord_profiles(span: int) -> list[tuple[int, ...]]:
    """Every 8-point circle in five rows has four double rows.

    Four chosen rows in 0..4 always contain adjacent rows, whose positive
    chord differences determine the integer y coefficient and squared radius.
    """
    profiles = set()
    for i in range(4):
        for a in range(1, span + 1):
            for b in range(1, span + 1):
                if (a - b) % 2:
                    continue
                c = (a*a - b*b - 4*(2*i+1)) // 4
                n = a*a + (2*i+c)**2
                profile = []
                for y in range(5):
                    square = n - (2*y+c)**2
                    d = isqrt(square) if square > 0 else 0
                    profile.append(d if d and d*d == square
                                   and d <= span and (d-a) % 2 == 0 else 0)
                if sum(d > 0 for d in profile) >= 4:
                    assert sum(d > 0 for d in profile) == 4
                    profiles.add(tuple(profile))
    return sorted(profiles)


def circles(m: int) -> list[tuple[int, ...]]:
    found = set()
    for ds in chord_profiles(m-1):
        biggest = max(ds)
        for total in range(biggest, 2*(m-1)-biggest+1, 2):
            points = tuple(y*m+(total+sign*d)//2
                           for y, d in enumerate(ds) if d for sign in (-1, 1))
            assert len(set(points)) == 8
            assert all(0 <= p % m < m for p in points)
            found.add(points)
    return sorted(found)


def encode(m: int, target: int):
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    pool = IDPool(start_from=5*m+1)
    clauses = []
    cs = circles(m)
    for y in range(5):
        row = list(range(y*m+1, (y+1)*m+1))
        clauses += CardEnc.atmost(lits=row, bound=6 if y == target else 7,
                                 encoding=EncType.seqcounter, vpool=pool).clauses
    for curve in cs:
        clauses.append([-p-1 for p in curve])
    blockers = [[] for _ in range(m)]
    for curve in cs:
        for p in curve:
            if p//m != target:
                continue
            v = pool.id()
            blockers[p % m].append(v)
            for other in curve:
                if other != p:
                    clauses.append([-v, other+1])
    for x, choices in enumerate(blockers):
        clauses.append([target*m+x+1] + choices)
    return clauses, pool.top, cs


def solve(m: int, target: int, seconds: float, engine: str):
    from pysat.solvers import Solver
    clauses, variables, cs = encode(m, target)
    start = time.monotonic()
    result = None
    with Solver(name=engine, bootstrap_with=clauses) as solver:
        while result is None and time.monotonic()-start < seconds:
            solver.conf_budget(20000)
            result = solver.solve_limited()
        stats = solver.accum_stats()
        model = set(solver.get_model()) if result is True else None
    rows = [[x for x in range(m) if y*m+x+1 in model] for y in range(5)] if model else None
    if rows is not None:
        occupied = {y*m+x for y, row in enumerate(rows) for x in row}
        assert len(rows[target]) <= 6
        assert all(len(row) <= 7 for row in rows)
        assert all(len(occupied & set(c)) <= 7 for c in cs)
        assert all(any(p in c and len(occupied & set(c)) == 7 for c in cs)
                   for p in range(target*m, (target+1)*m) if p not in occupied)
    return dict(m=m, target=target, engine=engine,
                status='SAT' if result is True else 'UNSAT' if result is False else 'UNKNOWN',
                wall_seconds=round(time.monotonic()-start, 6),
                variables=variables, clauses=len(clauses), circles=len(cs),
                profiles=chord_profiles(m-1), rows=rows, solver_statistics=stats,
                scope='All safe target-saturated states; other rows need not be saturated')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pysat-path', default='/workspace/research-tools/python-sat')
    ap.add_argument('--m', type=int, nargs='+', required=True)
    ap.add_argument('--target', type=int, nargs='+', default=[0, 1, 2])
    ap.add_argument('--seconds', type=float, default=20)
    ap.add_argument('--engine', default='cadical195')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    sys.path.insert(0, args.pysat_path)
    results = []
    for m in args.m:
        for target in args.target:
            result = solve(m, target, args.seconds, args.engine)
            results.append(result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    main()

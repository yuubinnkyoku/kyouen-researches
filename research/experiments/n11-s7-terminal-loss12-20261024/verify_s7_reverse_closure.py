#!/usr/bin/env python3
"""Independent geometry/edge audit for the S7 LOSS reverse closure of K0528.

This is a structural consequence of three previously terminal-certified
S8 LOSS roots, NOT a replacement for the S10 terminal verifier. All verdicts
use the original first player's perspective (S7 AND, S8 OR).
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

N = 11
ROOTS = (
    '00000000100000021081004020000020',
    '00000100100000021081000020000020',
    '00008000100000021081000020000020',
)
S7_ROOT = '00000000100000021081000020000020'


def coords(board: int):
    return [(p % N, p // N) for p in range(N*N) if board >> p & 1]


def mask(pts):
    return sum(1 << (N*y+x) for x, y in pts)


def canonical(board: int) -> int:
    ps = coords(board)
    transformations = (
        lambda x, y: (x, y), lambda x, y: (N-1-y, x),
        lambda x, y: (N-1-x, N-1-y), lambda x, y: (y, N-1-x),
        lambda x, y: (N-1-x, y), lambda x, y: (N-1-y, N-1-x),
        lambda x, y: (x, N-1-y), lambda x, y: (y, x),
    )
    return min(mask(f(x, y) for x, y in ps) for f in transformations)


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
          - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
          + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))


def circle4(a, b, c, d):
    # Subtract the last row of the 4x4 determinant, then take 3x3.
    rows = [(x-d[0], y-d[1], x*x+y*y-d[0]*d[0]-d[1]*d[1])
            for x, y in (a, b, c)]
    return det3(rows) == 0


def forbidden_four(a, b, c, d):
    # Any collinear triple makes the circle determinant identically zero;
    # only four collinear points are forbidden in that degenerate case.
    four = (a, b, c, d)
    if any(cross(*t) == 0 for t in itertools.combinations(four, 3)):
        return cross(a, b, c) == 0 and cross(a, b, d) == 0
    return circle4(a, b, c, d)


def safe(board: int) -> bool:
    return all(not forbidden_four(*four)
               for four in itertools.combinations(coords(board), 4))


@lru_cache(maxsize=None)
def legal_children(board: int):
    ps = coords(board)
    triples = list(itertools.combinations(ps, 3))
    occupied = set(ps)
    result = set()
    for y in range(N):
        for x in range(N):
            p = (x, y)
            if p not in occupied and all(not forbidden_four(*t, p) for t in triples):
                result.add(canonical(board | (1 << (N*y+x))))
    return result


def reverse_parents(board: int):
    return {canonical(board ^ (1 << (N*y+x))) for x, y in coords(board)}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read_keys(path: Path, n: int, stones: int):
    values = path.read_text().splitlines()
    need(len(values) == n and values == sorted(set(values)), f'bad key list {path}')
    need(all(len(k) == 32 and int(k, 16).bit_count() == stones for k in values),
         f'bad keys {path}')
    return {int(k, 16) for k in values}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--frozen-s7-loss', type=Path)
    parser.add_argument('--frozen-s7-win', type=Path)
    parser.add_argument('--previous-s8-loss-roots', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.certificate:
        cert = json.loads(args.certificate.read_text())
        need(cert['s7'] == S7_ROOT, 'S7 root changed')
        need(cert['s8_loss'] == list(ROOTS), 'S8 LOSS evidence changed')
    roots = {int(s, 16) for s in ROOTS}
    target = int(S7_ROOT, 16)
    need(len(roots) == 3, 'S8 count changed')
    need(all(r.bit_count() == 8 and canonical(r) == r and safe(r) for r in roots),
         'bad S8 roots')
    need(target in set.union(*(reverse_parents(r) for r in roots)),
         'S7 target not a parent')
    need(roots <= legal_children(target), 'S8 root not legal from S7')

    witness = defaultdict(list)
    for r in sorted(roots):
        for p in sorted(reverse_parents(r)):
            need(p.bit_count() == 7 and canonical(p) == p and safe(p), 'bad S7 parent')
            need(r in legal_children(p), 'invalid legal reverse edge')
            witness[p].append(r)
    need(len(witness) == 22, 'S7 reverse closure changed')
    need(all(len(v) >= 1 for v in witness.values()), 'missing S8 witness')
    s6_edges = {(q, p) for p in witness for q in reverse_parents(p)}
    s6 = {q for q, _ in s6_edges}
    need(all(p in legal_children(q) for q, p in s6_edges),
         'invalid S6->S7 edge')
    need((len(s6), len(s6_edges), sum(map(len, witness.values()))) ==
         (70, 154, 24), 'S6 reverse closure changed')

    # Degenerate geometry must not be mistaken for four cocircular points.
    need(not forbidden_four((0, 0), (1, 0), (2, 0), (0, 1)),
         'collinear triple false positive')
    need(forbidden_four((0, 0), (1, 0), (2, 0), (3, 0)),
         'four collinear missed')
    need(forbidden_four((0, 0), (1, 0), (0, 1), (1, 1)),
         'square circle missed')
    report = {
        'board': '11x11 q=4, fixed original-first-player perspective',
        'source_s8_loss_roots': list(ROOTS),
        's7_loss_certified_by_reverse_edges': len(witness),
        's7_reverse_edges': sum(map(len, witness.values())),
        's6_parents': len(s6),
        's6_to_s7_loss_edges': len(s6_edges),
        's6_closed_from_this_evidence': sum(legal_children(q) <= set(witness)
                                            for q in s6),
        's7_witnesses': {f'{p:032x}': [f'{r:032x}' for r in rs]
                         for p, rs in sorted(witness.items())},
        'empty_outcome': 'UNKNOWN',
    }
    if args.frozen_s7_loss:
        old = read_keys(args.frozen_s7_loss, 2232, 7)
        report['s7_overlap_frozen_2232'] = len(set(witness) & old)
        report['s7_added_vs_frozen_2232'] = len(set(witness) - old)
        need((report['s7_overlap_frozen_2232'],
              report['s7_added_vs_frozen_2232']) == (1, 21),
             'frozen S7 overlap changed')
    if args.frozen_s7_win:
        wins = read_keys(args.frozen_s7_win, 17, 7)
        need(not wins & set(witness), 'S7 WIN/LOSS conflict')
        report['s7_conflicts_frozen_win17'] = 0
    if args.previous_s8_loss_roots:
        older_roots = read_keys(args.previous_s8_loss_roots, 35, 8)
        prior = set().union(*(reverse_parents(r) for r in older_roots))
        need(not set(witness) & prior, 'overlap with previous 35-root closure')
        report['s7_overlap_previous_35_root_closure'] = 0
        if args.frozen_s7_loss:
            baseline = old | prior
            after = baseline | set(witness)
            gained = 0
            missing = []
            for q in s6:
                cs = legal_children(q)
                gained += len(cs & after) - len(cs & baseline)
                missing.append(len(cs - after))
            need((gained, min(missing), sum(n == 0 for n in missing)) ==
                 (147, 51, 0), 'conditional S6 coverage changed')
            report['s6_new_edges_vs_frozen2232_and_previous35'] = gained
            report['s6_min_missing_conditional'] = min(missing)
            report['s6_closed_conditional'] = 0
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('PASS', json.dumps({k: v for k, v in report.items()
                              if k != 's7_witnesses'}, sort_keys=True))


if __name__ == '__main__':
    main()

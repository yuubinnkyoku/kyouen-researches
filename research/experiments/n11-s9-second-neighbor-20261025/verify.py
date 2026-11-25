#!/usr/bin/env python3
"""Cache-free S9 AND certificate for a second one-stone-swap neighbor."""
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'n11-s9-terminal-neighbor-20261025' / 'verify.py'
spec = importlib.util.spec_from_file_location('n11_terminal_geometry', PREVIOUS)
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)
ROOT = int('00000000040400111000010a00001000', 16)


def verify(cpp_tsv=None):
    g = geometry
    g.need(ROOT.bit_count() == 9 and g.safe(ROOT) and g.canonical(ROOT) == ROOT,
           'invalid S9 root')
    leaves = g.read_keys(HERE / 's10-win17.keys', 17, 10)
    parents = g.read_keys(HERE / 's8-win9.keys', 9, 8)
    moves = g.legal(ROOT)
    actual = {g.canonical(ROOT | (1 << p)) for p in range(121)
              if moves >> p & 1}
    g.need(actual == leaves, 'incomplete S9 AND boundary')
    actual_parents = {g.canonical(ROOT ^ (1 << p)) for p in g.points(ROOT)}
    g.need(actual_parents == parents, 'incorrect S8 parent set')
    for parent in parents:
        options = g.legal(parent)
        g.need(any(g.canonical(parent | (1 << p)) == ROOT
                   for p in range(121) if options >> p & 1),
               'missing legal S8-to-S9 witness')
    leaf_moves = {}
    states = 0
    for leaf in sorted(leaves):
        verdict, visited = g.solve(leaf)
        g.need(verdict, 'S10 leaf is not WIN to move')
        leaf_moves[f'{leaf:032x}'] = g.legal(leaf).bit_count()
        states += visited
    g.need(not g.solve(ROOT)[0], 'S9 is not LOSS to move')
    g.need(states == 1745, 'independent terminal-state count changed')
    if cpp_tsv is not None:
        rows = {}
        for line in cpp_tsv.read_text(encoding='utf-8').splitlines():
            fields = line.split()
            g.need(len(fields) == 4, 'malformed C++ row')
            key, verdict, visited, count = fields
            g.need(key not in rows and verdict == 'WIN' and int(visited) > 0,
                   'C++ duplicate or non-WIN leaf')
            rows[key] = int(count)
        g.need(rows == leaf_moves, 'C++/Python geometry or verdict mismatch')
        g.need(dict(list(rows.items())[:-1]) != leaf_moves,
               'missing C++ leaf accepted')
        corrupted = dict(rows)
        corrupted[next(iter(corrupted))] += 1
        g.need(corrupted != leaf_moves, 'tampered C++ legal count accepted')
    print('VERIFIED S9 FIRST_WIN, 17/17 terminal S10 WIN, '
          '9 S8 WIN parents, 1745 independent Python leaf states; '
          'empty=UNKNOWN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpp-tsv', type=Path)
    args = parser.parse_args()
    verify(args.cpp_tsv)

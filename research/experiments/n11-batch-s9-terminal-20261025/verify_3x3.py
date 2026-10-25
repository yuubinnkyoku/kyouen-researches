#!/usr/bin/env python3
"""Cross-check six S9 AND roots using the separately implemented 3x3 geometry."""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'n11-s9-terminal-neighbor-20261025' / 'verify.py'
spec = importlib.util.spec_from_file_location('n11_three_by_three', SOURCE)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def verify():
    roots = g.read_keys(HERE / 's9-roots.keys', 6, 9)
    leaves = g.read_keys(HERE / 's10-win.keys', 106, 10)
    parents = g.read_keys(HERE / 's8-win.keys', 54, 8)
    children = set()
    ancestors = set()
    for root in roots:
        children.update(g.canonical(root | (1 << p))
                        for p in range(121) if g.legal(root) >> p & 1)
        ancestors.update(g.canonical(root ^ (1 << p)) for p in g.points(root))
        g.need(not g.solve(root)[0], 'S9 is not LOSS to move')
    g.need(children == leaves and ancestors == parents,
           '3x3 independent boundary mismatch')
    for parent in parents:
        g.need(any(g.canonical(parent | (1 << p)) in roots
                   for p in range(121) if g.legal(parent) >> p & 1),
               '3x3 parent witness mismatch')
    states = 0
    for leaf in sorted(leaves):
        verdict, visited = g.solve(leaf)
        g.need(verdict, '3x3 S10 non-WIN leaf')
        states += visited
    g.need(states == 12604, '3x3 terminal-state count changed')
    print('VERIFIED independent 3x3 geometry: 6 roots, 106 leaves, '
          '54 parents, 12604 states; empty=UNKNOWN')


if __name__ == '__main__':
    verify()

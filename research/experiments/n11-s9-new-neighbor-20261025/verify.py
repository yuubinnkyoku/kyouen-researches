#!/usr/bin/env python3
"""Cache-free, two-geometry terminal certificate for an N11 nine-stone root.

The two solvers use independently written 3x3 and 4x4 integer determinants.
No cached verdict, frozen outcome, or df-pn node estimate proves a leaf.
"""
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = int('00000000000400111000030800011000', 16)
FINGERPRINT = (41, 68, 130, 41, 142, 145, 62, 106, 103, 150, 69,
               182, 55, 29, 46, 55, 77, 114, 68, 153, 128, 59)


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


THREE = load_module('n11_s9_neighbor_3x3',
    HERE.parent / 'n11-s9-terminal-neighbor-20261025' / 'verify.py')
FOUR = load_module('n11_s9_batch_4x4',
    HERE.parent / 'n11-batch-s9-terminal-20261025' / 'verify.py')


def read_keys(filename, count, stones):
    lines = (HERE / filename).read_text(encoding='utf-8').splitlines()
    need(len(lines) == count and lines == sorted(set(lines)),
         'missing, unsorted or repeated key in ' + filename)
    need(all(len(s) == 32 and set(s) <= set('0123456789abcdef')
             for s in lines), 'invalid key syntax: ' + filename)
    values = {int(s, 16) for s in lines}
    for g in (THREE, FOUR):
        need(all(s.bit_count() == stones and g.safe(s) and
                 g.canonical(s) == s for s in values),
             'unsafe/noncanonical key: ' + filename)
    return values


def boundary(roots, leaves, parents):
    need(roots == {ROOT}, 'wrong nine-stone root')
    for g in (THREE, FOUR):
        children = {g.canonical(ROOT | (1 << p))
                    for p in range(121) if g.legal(ROOT) >> p & 1}
        need(children == leaves, 'incomplete S9 AND boundary')
        reverse = {g.canonical(ROOT ^ (1 << p)) for p in g.points(ROOT)}
        need(reverse == parents, 'incomplete S8 parent set')
        for parent in parents:
            moves = g.legal(parent)
            need(any(g.canonical(parent | (1 << p)) == ROOT
                     for p in range(121) if moves >> p & 1),
                 'S8 parent lacks legal S9 witness')


def verify(negative=False):
    roots = read_keys('s9-roots.keys', 1, 9)
    leaves = read_keys('s10-win.keys', 22, 10)
    parents = read_keys('s8-win.keys', 9, 8)
    boundary(roots, leaves, parents)
    fingerprints = []
    for leaf in sorted(leaves):
        verdict3, states3 = THREE.solve(leaf)
        verdict4, states4 = FOUR.solve(leaf)
        need(verdict3 and verdict4, 'unproved S10 WIN leaf: %032x' % leaf)
        need(THREE.legal(leaf) == FOUR.legal(leaf),
             'independent legal-move disagreement: %032x' % leaf)
        need(states3 == states4, 'independent search disagreement: %032x' % leaf)
        fingerprints.append(states4)
    need(tuple(fingerprints) == FINGERPRINT,
         'S10 per-leaf terminal-state fingerprint changed')
    for g in (THREE, FOUR):
        need(not g.solve(ROOT)[0], 'S9 is not LOSS to move')
    if negative:
        mutations = ((roots, leaves - {min(leaves)}, parents),
                     (roots, leaves, parents - {min(parents)}),
                     (roots, leaves | {ROOT}, parents))
        for bad in mutations:
            try:
                boundary(*bad)
            except ValueError:
                pass
            else:
                raise ValueError('mutated proof boundary accepted')
    print('VERIFIED N11 S9 FIRST_WIN: 22/22 S10 terminal WIN leaves, '
          '9 S8 WIN parents, %d states per independent integer-geometry '
          'solver; empty=UNKNOWN' % sum(fingerprints))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--negative', action='store_true')
    verify(ap.parse_args().negative)

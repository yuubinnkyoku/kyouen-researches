#!/usr/bin/env python3
"""Independent N11 S9 AND certificates: 2 roots, all terminal S10 children.

No cached outcome, incomplete df-pn run, or frozen verdict is used as proof.
Both 3x3 and 4x4 integer-geometry solvers re-evaluate every terminal leaf.
"""
import argparse
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOTS = {
    int('00000000000000111000030800011040', 16),
    int('00000000000000111000030800015000', 16),
}
MANIFESTS = {
    's9-roots.keys': (2, 9, '6822e87666c33b4e194d4a390cc94258518331a36c8811d5862dea75fe54a94d'),
    's10-win.keys': (58, 10, 'aec2ee7b08b720296d9f68ccd7e657b10b6be3539c32f23585224d9a36b9066c'),
    's8-win.keys': (17, 8, 'b73b8f9fee6309532e592d0a1cbe9c998536f039dc3ca8f0b08684f282c6f1b1'),
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


THREE = load_module(
    'n11_two_neighbors_3x3',
    HERE.parent / 'n11-s9-terminal-neighbor-20261025' / 'verify.py')
FOUR = load_module(
    'n11_two_neighbors_4x4',
    HERE.parent / 'n11-batch-s9-terminal-20261025' / 'verify.py')


def read_keys(name):
    count, stones, digest = MANIFESTS[name]
    raw = (HERE / name).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == digest, 'manifest SHA-256 mismatch: ' + name)
    rows = raw.decode('ascii').splitlines()
    need(len(rows) == count and rows == sorted(set(rows)),
         'missing, repeated or unsorted key: ' + name)
    need(all(len(h) == 32 and set(h) <= set('0123456789abcdef') for h in rows),
         'invalid key syntax: ' + name)
    values = {int(h, 16) for h in rows}
    for g in (THREE, FOUR):
        need(all(v.bit_count() == stones and g.safe(v) and g.canonical(v) == v
                 for v in values), 'unsafe or noncanonical key: ' + name)
    return values


def boundary(roots, leaves, parents):
    need(roots == ROOTS, 'S9 roots changed')
    for g in (THREE, FOUR):
        all_children = set()
        all_parents = set()
        incidence = 0
        for root in roots:
            legal = g.legal(root)
            children = {g.canonical(root | (1 << p))
                        for p in range(121) if legal >> p & 1}
            incidence += len(children)
            all_children.update(children)
            all_parents.update(g.canonical(root ^ (1 << p))
                               for p in g.points(root))
        need(incidence == 59 and all_children == leaves,
             'incomplete or contaminated S9 AND boundary')
        need(len(all_parents) == 17 and all_parents == parents,
             'incomplete or contaminated S8 witness parents')
        for parent in parents:
            legal = g.legal(parent)
            need(any(g.canonical(parent | (1 << p)) in roots
                     for p in range(121) if legal >> p & 1),
                 'S8 parent lacks legal S9 WIN witness')


def verify(negative=False):
    roots = read_keys('s9-roots.keys')
    leaves = read_keys('s10-win.keys')
    parents = read_keys('s8-win.keys')
    boundary(roots, leaves, parents)
    states3 = states4 = 0
    for leaf in sorted(leaves):
        win3, n3 = THREE.solve(leaf)
        win4, n4 = FOUR.solve(leaf)
        need(win3 and win4, 'unproved terminal S10 WIN: %032x' % leaf)
        need(THREE.legal(leaf) == FOUR.legal(leaf),
             'independent legal-move disagreement: %032x' % leaf)
        need(n3 == n4, 'independent terminal search disagreement: %032x' % leaf)
        states3 += n3
        states4 += n4
    # State counts are implementation fingerprints, not game-theoretic distances.
    need(states3 == states4 == 13596, 'terminal search-state regression')
    if negative:
        bad = (
            (roots, leaves - {min(leaves)}, parents),
            (roots, leaves, parents - {min(parents)}),
            (roots, leaves | {min(roots)}, parents),
            (roots - {min(roots)}, leaves, parents),
        )
        for mutation in bad:
            try:
                boundary(*mutation)
            except ValueError:
                continue
            raise ValueError('tampered proof boundary accepted')
    print('VERIFIED N11: S9 original-first WIN roots=2, S10 terminal WIN '
          'incidences=59, distinct S10 leaves=58, S8 WIN parents=17, '
          'distinct terminal states per solver=%d, empty=UNKNOWN' % states3)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--negative', action='store_true')
    verify(ap.parse_args().negative)

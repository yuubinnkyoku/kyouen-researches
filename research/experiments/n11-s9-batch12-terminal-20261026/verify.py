#!/usr/bin/env python3
"""Cache-free, two-geometry terminal certificate for twelve N11 S9 roots.

S9 is an AND node for original-first WIN: all legal S10 children must be
WIN to move. S8 is an OR node: one legal S9 WIN witness suffices.
No frozen verdict table or incomplete search is used as proof.
"""
import argparse
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
ROOT_HASH = 'd72f0c7e204502cc6ae442955cf2558d11964cff3443c2ad15683243d2d78a05'
LEAF_HASH = 'b39045f33e288c424747df293131d7aaa50678d1e09493fe4baa35ea5d7af231'
PARENT_HASH = 'aa53bb0c49fba88ada30ce366eee3dd71331eb0dd5da0e2b38bc9b59254311ac'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


THREE = load_module('n11_batch12_three',
                    EXPERIMENTS / 'n11-s9-terminal-neighbor-20261025' / 'verify.py')
FOUR = load_module('n11_batch12_four',
                   EXPERIMENTS / 'n11-batch-s9-terminal-20261025' / 'verify.py')


def digest(values):
    data = ''.join(f'{x:032x}\n' for x in sorted(values)).encode('ascii')
    return hashlib.sha256(data).hexdigest()


def load_roots():
    raw = (HERE / 's9-roots.keys').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == ROOT_HASH,
         'S9 certificate root hash mismatch')
    lines = raw.decode('ascii').splitlines()
    need(len(lines) == 12 and lines == sorted(set(lines)),
         'missing/duplicate/unsorted S9 roots')
    need(all(len(x) == 32 and set(x) <= set('0123456789abcdef')
             for x in lines), 'invalid S9 root syntax')
    return {int(x, 16) for x in lines}


def child_keys(geometry, board):
    allowed = geometry.legal(board)
    return {geometry.canonical(board | (1 << p))
            for p in range(121) if allowed >> p & 1}


def boundary(roots, leaves, parents):
    for geometry in (THREE, FOUR):
        actual_leaves = set()
        actual_parents = set()
        incidences = 0
        for root in roots:
            need(root.bit_count() == 9 and geometry.safe(root)
                 and geometry.canonical(root) == root,
                 'unsafe/noncanonical S9 root')
            children = child_keys(geometry, root)
            incidences += len(children)
            actual_leaves.update(children)
            actual_parents.update(geometry.canonical(root ^ (1 << p))
                                  for p in geometry.points(root))
        need(incidences == 270 and len(actual_leaves) == 264,
             'S9 legal-child census changed')
        need(actual_leaves == leaves, 'incomplete/contaminated S10 boundary')
        need(len(actual_parents) == 101 and actual_parents == parents,
             'incomplete/contaminated S8 parent boundary')
        for parent in parents:
            need(parent.bit_count() == 8 and geometry.safe(parent)
                 and geometry.canonical(parent) == parent,
                 'unsafe/noncanonical S8 parent')
            need(any(w in roots for w in child_keys(geometry, parent)),
                 'S8 parent has no legal S9 WIN witness')
        for leaf in leaves:
            need(leaf.bit_count() == 10 and geometry.safe(leaf)
                 and geometry.canonical(leaf) == leaf,
                 'unsafe/noncanonical S10 leaf')


def verify(negative=False):
    roots = load_roots()
    leaves = set()
    parents = set()
    for root in roots:
        leaves.update(child_keys(THREE, root))
        parents.update(THREE.canonical(root ^ (1 << p))
                       for p in THREE.points(root))
    need(digest(leaves) == LEAF_HASH and digest(parents) == PARENT_HASH,
         'derived certificate boundary digest changed')
    boundary(roots, leaves, parents)
    if negative:
        mutations = (
            (roots - {min(roots)}, leaves, parents),
            (roots, leaves - {min(leaves)}, parents),
            (roots, leaves, parents - {min(parents)}),
            (roots, leaves | {min(roots)}, parents),
        )
        for altered in mutations:
            try:
                boundary(*altered)
            except ValueError:
                continue
            raise ValueError('tampered proof boundary accepted')
    states3 = states4 = 0
    for leaf in sorted(leaves):
        win3, n3 = THREE.solve(leaf)
        win4, n4 = FOUR.solve(leaf)
        need(win3 and win4, 'terminal S10 WIN not proved: %032x' % leaf)
        need(THREE.legal(leaf) == FOUR.legal(leaf),
             'independent legal-move disagreement: %032x' % leaf)
        need(n3 == n4, 'independent terminal-state disagreement: %032x' % leaf)
        states3 += n3
        states4 += n4
    # Search-state counts are regression fingerprints, NOT proof distances.
    need(states3 == states4 == 39067, 'terminal-state fingerprint changed')
    print('VERIFIED N11: 12 S9 original-first WIN roots, 270 legal S10 '
          'incidences, 264 distinct terminal S10 WIN leaves, 101 S8 WIN '
          'witness parents, 39067 states per independent solver; '
          'empty=UNKNOWN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    verify(args.negative)

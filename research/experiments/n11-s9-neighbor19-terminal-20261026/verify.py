#!/usr/bin/env python3
"""Cache-free N11 S9 terminal proof: nineteen new original-first WIN roots.

Independently enumerate the AND boundary and solve each S10 leaf to
terminal using the existing 3x3 and 4x4 integer-geometry implementations.
"""
import argparse
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
ROOT_HASH = 'cfa9bd4d727e4650da3a8e0c1cefe682c64a8622680121cc119c092cf8c50e4c'
LEAF_HASH = '2cd86d1b91f9e25bfcff11e522276d51dd9bcc35c3baad67becd5a69f7a44ad2'
PARENT_HASH = '46572c1f6e2a38edb8776c3b25fcd1677516b948cb2f07ad8964738618164828'
STATE_HASH = '70c9c2580b860713d1ffbce3ff372d32d9890e4a25dd3d0a063f00dbeb797467'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


THREE = load_module('n11_neighbor19_three',
                    EXP / 'n11-s9-terminal-neighbor-20261025' / 'verify.py')
FOUR = load_module('n11_neighbor19_four',
                   EXP / 'n11-batch-s9-terminal-20261025' / 'verify.py')


def digest(values):
    return hashlib.sha256(''.join('%032x\n' % v for v in sorted(values))
                          .encode('ascii')).hexdigest()


def roots_from_file():
    raw = (HERE / 's9-roots.keys').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == ROOT_HASH,
         'S9 root file SHA-256 mismatch')
    rows = raw.decode('ascii').splitlines()
    need(len(rows) == 19 and rows == sorted(set(rows)),
         'missing, duplicate or unsorted S9 root')
    need(all(len(h) == 32 and set(h) <= set('0123456789abcdef')
             for h in rows), 'invalid S9 root syntax')
    return {int(h, 16) for h in rows}


def child_keys(geometry, board):
    mask = geometry.legal(board)
    return {geometry.canonical(board | (1 << p))
            for p in range(121) if mask >> p & 1}


def boundary(roots, leaves, parents):
    need(len(roots) == 19 and len(leaves) == 314 and len(parents) == 164,
         'certificate boundary size changed')
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
            actual_parents.update(
                geometry.canonical(root ^ (1 << p))
                for p in geometry.points(root))
        need(incidences == 319 and actual_leaves == leaves,
             'S9 universal legal S10 boundary incomplete or contaminated')
        need(actual_parents == parents,
             'S8 reverse-witness parent boundary incomplete')
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
    roots = roots_from_file()
    leaves = set()
    parents = set()
    for root in roots:
        leaves.update(child_keys(THREE, root))
        parents.update(THREE.canonical(root ^ (1 << p))
                       for p in THREE.points(root))
    need(digest(leaves) == LEAF_HASH and digest(parents) == PARENT_HASH,
         'derived S10/S8 boundary SHA-256 mismatch')
    boundary(roots, leaves, parents)
    if negative:
        mutations = (
            (roots - {min(roots)}, leaves, parents),
            (roots, leaves - {min(leaves)}, parents),
            (roots, leaves, parents - {min(parents)}),
            (roots, leaves | {min(roots)}, parents),
        )
        for changed in mutations:
            try:
                boundary(*changed)
            except ValueError:
                continue
            raise ValueError('tampered certificate boundary accepted')
    states3 = states4 = 0
    state_rows = []
    for leaf in sorted(leaves):
        win3, n3 = THREE.solve(leaf)
        win4, n4 = FOUR.solve(leaf)
        need(win3 and win4, 'unproved terminal S10 WIN: %032x' % leaf)
        mask3, mask4 = THREE.legal(leaf), FOUR.legal(leaf)
        need(mask3 == mask4, 'independent legal-move disagreement: %032x' % leaf)
        need(n3 == n4, 'independent state-count disagreement: %032x' % leaf)
        state_rows.append('%032x %d %d\n' % (leaf, n3, mask3.bit_count()))
        states3 += n3
        states4 += n4
    need(hashlib.sha256(''.join(state_rows).encode('ascii')).hexdigest()
         == STATE_HASH, 'per-leaf terminal fingerprint changed')
    need(states3 == states4 == 25435, 'terminal state-count regression')
    print('VERIFIED N11: 19 S9 original-first WIN, 319 legal S10 incidences, '
          '314 distinct terminal S10 WIN, 164 S8 witness parents, '
          '25435 states per independent solver; empty=UNKNOWN')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--negative', action='store_true')
    verify(ap.parse_args().negative)

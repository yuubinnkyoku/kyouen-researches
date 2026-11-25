#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cross-check: does the Python canonical key equal the solver's?

The s4 manifest verifier recomputes canonical keys and legal-move sets in
Python and compares them to what the C++ wrote. If the two conventions ever
differ, the verifier would report a proved class as non-existent, or worse
accept a bogus one. So this compares them directly, class by class, on the
coordinator's own `s4table` dump -- which needs no search at all, because
`--coord-max=0` stops before working on any class.

Compared per class: the canonical key, the coverage vertex set, and the raw
edge list. All three come from the solver and are recomputed here from the
board alone, using the concyclic rule reimplemented in
dfpn_edge_classes.py.

Usage:
    dfpn_canonical_xcheck.py <s4table dump> [--first=60] [--r2=0]
"""
import argparse
import collections
import io
import sys

from dfpn_edge_classes import (d4_canonical, d4_canonical_key,  # noqa: E402
                               legal_after)

sys.path.insert(0, __file__.rsplit('/', 1)[0])


def load_table(path):
    rows = []
    header = None
    for line in io.open(path, encoding='utf-8', errors='replace'):
        line = line.strip()
        if line.startswith('#') and line.lstrip('#').lstrip().startswith('s4table'):
            # "# s4table,first,r2,vertices,classes"
            f = line.lstrip('#').strip().split(',')
            header = {'first': int(f[1]), 'r2': int(f[2]),
                      'vertices': int(f[3]), 'classes': int(f[4])}
            continue
        f = line.split(',')
        if f[0] != 's4table':
            continue
        # s4table,slot,lo,hi,cov_size,unknown_s5,verdict,<verts...>,<edges...>
        # The two trailing lists are variable length, so they are sliced by
        # cov_size rather than read to the end of the line.
        if len(f) < 8:
            continue
        slot = int(f[1])
        lo, hi = int(f[2]), int(f[3])
        cov_size = int(f[4])
        unk = int(f[5])
        verdict = f[6]
        vs = f[7:7 + cov_size]
        rest = f[7 + cov_size:]
        verts = [int(x) for x in vs if x]
        edges = []
        for tok in rest:
            if not tok or ':' not in tok:
                continue
            a, b = tok.split(':')
            edges.append((int(a), int(b)))
        rows.append({'slot': slot, 'key': (lo, hi), 'cov_size': cov_size,
                     'unk': unk, 'verdict': verdict, 'verts': verts,
                     'edges': edges})
    return header, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dump')
    ap.add_argument('--first', type=int, default=60)
    ap.add_argument('--r2', type=int, default=0)
    args = ap.parse_args()

    header, rows = load_table(args.dump)
    if header is None:
        print('NO_HEADER: no "# s4table,..." header in %s' % args.dump)
        return 2
    first, r2 = header['first'], header['r2']
    if (first, r2) != (args.first, args.r2):
        print('root differs: dump says {%d,%d}, asked for {%d,%d}'
              % (first, r2, args.first, args.r2))
        return 2

    print('root                 : {%d,%d}' % (first, r2))
    print('vertices claimed     : %d' % header['vertices'])
    print('classes claimed      : %d' % header['classes'])
    print('classes in dump      : %d' % len(rows))

    base = {first, r2}
    verts = legal_after(base)
    print('vertices recomputed  : %d' % len(verts))
    if len(verts) != header['vertices']:
        print('VERTEX_MISMATCH')
        return 1

    edge_set = set()
    for a in verts:
        for b in legal_after(base | {a}):
            if b == a:
                continue
            edge_set.add((min(a, b), max(a, b)))

    py = collections.defaultdict(set)
    py_edges = collections.defaultdict(list)
    for (a, b) in edge_set:
        k = d4_canonical_key([first, r2, a, b])
        py[k].update((a, b))
        py_edges[k].append((a, b))

    print('classes recomputed   : %d' % len(py))

    bad_key = bad_cov = bad_edges = 0
    examples = []
    for r in rows:
        k = r['key']
        if k not in py:
            bad_key += 1
            if len(examples) < 5:
                examples.append('slot %d: key %d,%d not produced by python'
                                % (r['slot'], k[0], k[1]))
            continue
        if set(r['verts']) != py[k]:
            bad_cov += 1
            if len(examples) < 5:
                examples.append('slot %d: coverage %s vs %s'
                                % (r['slot'], sorted(r['verts']),
                                   sorted(py[k])))
        if r['cov_size'] != len(py[k]):
            bad_cov += 1
        if sorted(r['edges']) != sorted(py_edges[k]):
            bad_edges += 1
            if len(examples) < 5:
                examples.append('slot %d: edges %s vs %s'
                                % (r['slot'], sorted(r['edges']),
                                   sorted(py_edges[k])))

    print('key mismatches       : %d' % bad_key)
    print('coverage mismatches  : %d' % bad_cov)
    print('edge-list mismatches : %d' % bad_edges)
    if examples:
        print()
        for e in examples:
            print('  %s' % e)

    ok = (bad_key == 0 and bad_cov == 0 and bad_edges == 0
          and len(rows) == len(py)
          and set(r['key'] for r in rows) == set(py))
    if ok:
        print()
        print('every class key, coverage and edge list agrees between the')
        print('solver and the independent Python reimplementation')
    print('CANONICAL_AGREE' if ok else 'CANONICAL_MISMATCH')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
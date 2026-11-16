#!/usr/bin/env python3
"""Pre-fold cover map for the 17 cost-65j WIN7-D10 receipt roots (2026-11-16).

The cost-65j sweep of child 00000000000000809102000080000000 (65 legal
candidates) is complete: 17 WIN7-D10 receipt roots (bits 4,15,18,20,21,23,
25,28,66,79,91,101,109 from the cost-65f raw batches 1-7, v15 engine, plus
bits 112,116,118,119 from the cost-65j raw batch 8, v16 engine), 48
REFUTED-D10 (43 from cost-65f, bit 113 by the published canonical identity
transfer, bits 111,114,117,120 from cost-65j batch 8/9), 0 capped.

This script computes, for every one of the 17 WIN roots, the D4-canonical
hex of each of its 7 one-stone deletions (the receipt's cover set) and
reports which deletions are rows of the MS5 S6 manifest
(hex,cost,classes).  It also re-derives, with the same independent
implementation, the session observation that the unswept cost-64 rows
00000000000000003800000008002002 and 00000000000000003800000008003000 are
covered by the cost-65f bit-21 / bit-20 receipts respectively.

Independent stdlib implementation: exact-integer Bareiss 4x4 determinants
for legality re-verification of all 17 WIN bits and the D4 canonical form
(8 transforms, lexicographically minimal 32-hex).  Bookkeeping only: the
cover map predicts which rows the pending fold can close and says nothing
about the game-theoretic value of any position beyond the published
depth-10 verdicts; which of the covered rows are still open is decided by
the fold against the head-1410 remaining set.  REFUTED-D10 is not a loss
proof and the 11x11 empty board remains UNKNOWN.
"""
import csv
import json
import os
import sys

CHILD = '00000000000000809102000080000000'
WIN_BITS_65F = [4, 15, 18, 20, 21, 23, 25, 28, 66, 79, 91, 101, 109]
WIN_BITS_65J = [112, 116, 118, 119]
MANIFEST_GLOB = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', '..', 'n11-s2-5960-milestone5-20261112', 'output',
    'ms5_s6_manifest_part%d.csv')
KNOWN_65F_COVERED_ROWS = {
    '00000000000000003800000008002002': 21,
    '00000000000000003800000008003000': 20,
}


def bareiss4(m):
    m = [row[:] for row in m]
    prev = 1
    for k in range(3):
        if m[k][k] == 0:
            for r in range(k + 1, 4):
                if m[r][k] != 0:
                    m[k], m[r] = m[r], m[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                m[i][j] = (m[i][j] * m[k][k] - m[i][k] * m[k][j]) // prev
            m[i][k] = 0
        prev = m[k][k]
    return m[3][3]


def row_of(cell):
    x, y = cell % 11, cell // 11
    return [x * x + y * y, x, y, 1]


def det4(cells):
    return bareiss4([row_of(c) for c in cells])


def stones(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(121) if (v >> i) & 1]


def enumerate_legal(hexstr):
    st = stones(hexstr)
    assert len(st) == 6
    legal = []
    for p in range(121):
        if p in st:
            continue
        bad = False
        for i in range(6):
            for j in range(i + 1, 6):
                for k in range(j + 1, 6):
                    if det4([st[i], st[j], st[k], p]) == 0:
                        bad = True
                        break
                if bad:
                    break
            if bad:
                break
        if not bad:
            legal.append(p)
    return st, legal


def d4_canon(hexstr):
    st = stones(hexstr)
    best = None
    for swap in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                t = []
                for c in st:
                    x, y = c % 11, c // 11
                    a, b = (y, x) if swap else (x, y)
                    if fx:
                        a = 10 - a
                    if fy:
                        b = 10 - b
                    t.append(a + 11 * b)
                v = 0
                for i in t:
                    v |= 1 << i
                h = format(v, '032x')
                if best is None or h < best:
                    best = h
    return best


def main():
    st, legal = enumerate_legal(CHILD)
    assert len(legal) == 65, len(legal)
    manifest = {}
    for i in range(1, 7):
        with open(MANIFEST_GLOB % i) as f:
            for row in csv.DictReader(f):
                manifest[row['hex']] = (row['cost'], row['classes'])
    assert len(manifest) == 7867, len(manifest)

    receipts = {}
    covered_rows = {}
    for bit in WIN_BITS_65F + WIN_BITS_65J:
        assert bit in legal, bit
        root = int(CHILD, 16) | (1 << bit)
        root_hex = format(root, '032x')
        st7 = stones(root_hex)
        dels = {}
        for s in st7:
            d = d4_canon(format(root & ~(1 << s), '032x'))
            dels[d] = dels.get(d, 0) + 1
        in_man = sorted(d for d in dels if d in manifest)
        receipts[bit] = {
            'source': 'cost-65f batches 1-7 (v15)' if bit in WIN_BITS_65F
                      else 'cost-65j batch 8 (v16)',
            'root_hex': root_hex,
            'root_d4_canon': d4_canon(root_hex),
            'in_manifest_deletions': {d: {'cost': manifest[d][0],
                                         'classes': manifest[d][1]}
                                      for d in in_man},
        }
        for d in in_man:
            covered_rows.setdefault(d, []).append(bit)

    # re-derive the session observation: the two cost-64 rows are covered
    # by the 65f bit-21 / bit-20 receipts
    checks = {}
    for row, bit in KNOWN_65F_COVERED_ROWS.items():
        ok = row in receipts[bit]['in_manifest_deletions']
        checks[row] = {'covered_by_65f_bit': bit, 'verified': ok}
        assert ok, (row, bit)

    # cross-root root-canon distinctness of the 17 receipts
    canons = [receipts[b]['root_d4_canon'] for b in receipts]
    assert len(set(canons)) == len(canons), 'duplicate root canon'

    out = {
        'schema': 'n11-class2-lane-cost65j-win-marginals-20261116-v1',
        'date': '2026-11-16',
        'child': CHILD,
        'method': ('independent stdlib re-derivation: Bareiss 4x4 legality of all '
                   '17 WIN bits, D4 canonicalization (8 transforms), MS5 S6 manifest '
                   'lookup; no engine, no float'),
        'receipts': receipts,
        'covered_manifest_rows_union': {
            d: {'cost': manifest[d][0], 'classes': manifest[d][1],
                'covered_by_bits': sorted(bs)}
            for d, bs in sorted(covered_rows.items())},
        'known_65f_covered_rows_check': checks,
        'note': ('pre-fold bookkeeping: which of these covered rows are still '
                 'open is decided by the pending cost-65j fold against the '
                 'head-1410 remaining set; REFUTED-D10 is not a loss proof and '
                 'the 11x11 empty board remains UNKNOWN'),
    }
    op = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                      'output', 'class2-lane-cost65j-win-marginals-20261116.json')
    with open(op, 'w') as f:
        f.write(json.dumps(out, indent=1) + '
')
    print('receipts:', len(receipts), 'covered manifest rows (union):',
          len(out['covered_manifest_rows_union']))
    print('65f-covered-row checks:', all(c['verified'] for c in checks.values()))
    print('written', op)


if __name__ == '__main__':
    main()

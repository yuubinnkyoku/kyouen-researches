#!/usr/bin/env python3
"""Independent audit of round-9 S7 LOSS -> S6 WIN polarity error.

Checks finite reverse geometry and fixed-first-player AND/OR semantics.
Does not independently certify the underlying S8 terminal verdicts.
"""
import argparse
import json
from itertools import combinations
from pathlib import Path

N = 11

def points(mask):
    return [i for i in range(121) if mask & (1 << i)]

def canonical(mask):
    result = None
    for t in range(8):
        v = 0
        for p in points(mask):
            x, y = p % N, p // N
            xx, yy = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                      (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[t]
            v |= 1 << (N * yy + xx)
        result = v if result is None else min(result, v)
    return result

def det(a, b, c, d):
    def row(p):
        x, y = p % N, p // N
        return (x, y, x*x + y*y)
    A, B, C, D = map(row, (a, b, c, d))
    u = [x-y for x,y in zip(A,D)]
    v = [x-y for x,y in zip(B,D)]
    w = [x-y for x,y in zip(C,D)]
    return u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0])

def safe(mask):
    return all(det(*q) != 0 for q in combinations(points(mask), 4))

def children(mask):
    triples = list(combinations(points(mask), 3))
    return {canonical(mask | (1 << i)) for i in range(121)
            if not (mask & (1 << i)) and
            all(det(a, b, c, i) != 0 for a,b,c in triples)}

def read_masks(path, count, stones):
    lines = Path(path).read_text().splitlines()
    assert len(lines) == len(set(lines)) == count, path
    assert all(len(s) == 32 and s == s.lower() and all(c in '0123456789abcdef' for c in s) for s in lines)
    masks = {int(s, 16) for s in lines}
    assert all(m.bit_count() == stones and canonical(m) == m and safe(m) for m in masks)
    return masks

def fixed_first(stones, child_values):
    assert all(v in ('WIN', 'LOSS', 'UNKNOWN') for v in child_values)
    if stones % 2 == 0:
        if 'WIN' in child_values: return 'WIN'
        if all(v == 'LOSS' for v in child_values): return 'LOSS'
    else:
        if 'LOSS' in child_values: return 'LOSS'
        if all(v == 'WIN' for v in child_values): return 'WIN'
    return 'UNKNOWN'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--round9', type=Path, required=True)
    parser.add_argument('--old-loss', type=Path, help='frozen 2232 S7 LOSS positions')
    parser.add_argument('--known-win', type=Path, help='frozen 17 S7 WIN positions')
    a = parser.parse_args()
    assert fixed_first(6, ['LOSS', 'UNKNOWN']) == 'UNKNOWN'
    assert fixed_first(6, ['LOSS', 'WIN']) == 'WIN'
    assert fixed_first(6, ['LOSS', 'LOSS']) == 'LOSS'
    assert fixed_first(7, ['LOSS', 'UNKNOWN']) == 'LOSS'
    assert fixed_first(7, ['WIN', 'UNKNOWN']) == 'UNKNOWN'
    s8 = []
    for row in (a.round9 / 'round9_proof_optimized.tsv').read_text().splitlines():
        cols = row.split('\t')
        if cols[0] == 'ROOT' and cols[2] == 'LOSS':
            s8.append(int(cols[1], 16))
    assert len(s8) == len(set(s8)) == 6
    assert all(x.bit_count() == 8 and canonical(x) == x and safe(x) for x in s8)
    s7 = {canonical(r ^ (1 << p)) for r in s8 for p in points(r)}
    assert s7 == read_masks(a.round9 / 'round9_s7_parents.txt', 44, 7)
    assert all(any(r in children(s) for r in s8) for s in s7)
    s6 = {canonical(s ^ (1 << p)) for s in s7 for p in points(s)}
    # Historical filename is misleading: these are NOT 139 proved WIN positions.
    assert s6 == read_masks(a.round9 / 'round9_s6_win_parents.txt', 139, 6)
    old = read_masks(a.old_loss, 2232, 7) if a.old_loss else set()
    known_win = read_masks(a.known_win, 17, 7) if a.known_win else set()
    assert not (old | s7) & known_win, 'S7 WIN/LOSS conflict'
    counts = []
    for p in s6:
        ch = children(p)
        lc = len(ch & (old | s7))
        wc = len(ch & known_win)
        unknown = len(ch) - lc - wc
        verdict = fixed_first(6, ['LOSS']*lc + ['WIN']*wc + ['UNKNOWN']*unknown)
        assert ch & s7, 'missing actual S7 LOSS child'
        assert verdict == 'UNKNOWN', 'new proof or evidence conflict: inspect explicitly'
        counts.append((unknown, lc, wc, len(ch)))
    out = dict(s8_loss_roots=len(s8), s7_loss_parents=len(s7),
               s6_parent_candidates=len(s6), s6_win_certified_by_this_propagation=0,
               s6_loss_certified_by_this_propagation=0,
               s6_evidence_limited_unknown=len(counts),
               min_unknown_s7=min(x[0] for x in counts),
               max_unknown_s7=max(x[0] for x in counts),
               s7_win_witness_parent_count=sum(x[2] > 0 for x in counts),
               historical_s6_filename='round9_s6_win_parents.txt (NOT a verdict cache)',
               empty_board='UNKNOWN')
    print(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()

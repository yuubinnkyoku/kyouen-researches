#!/usr/bin/env python3
"""Seven S9 WIN roots, all S10 children, and 63 S8 WIN parents.

C++ uses 4x4 determinants; Python uses 3x3 determinants.
Frozen verdicts are not proof inputs.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-s8-to-s7-lift238-20261020'))
from terminal_geometry import canonical, children, legal, next_player_wins_at_s10, points, safe


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path, n, stones):
    raw = Path(path).read_text(encoding='utf-8').splitlines()
    need(len(raw) == n and raw == sorted(set(raw)), 'key count/order/duplicate: ' + str(path))
    need(all(len(x) == 32 and set(x) <= set('0123456789abcdef') for x in raw), 'bad hex')
    vals = {int(x, 16) for x in raw}
    need(all(x.bit_count() == stones and canonical(x) == x and safe(x) for x in vals),
         'unsafe/noncanonical: ' + str(path))
    return vals


def fmt(values):
    return [f'{x:032x}' for x in sorted(values)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cpp-tsv', type=Path, required=True)
    ap.add_argument('--emit-s10', type=Path)
    ap.add_argument('--s10-manifest', type=Path, default=HERE / 's10-win89.keys')
    ap.add_argument('--s8-manifest', type=Path, default=HERE / 's8-win63.keys')
    ap.add_argument('--frozen-win', type=Path)
    ap.add_argument('--frozen-loss', type=Path)
    args = ap.parse_args()
    roots = read(HERE / 's9-win7.keys', 7, 9)
    child_sets = {root: children(root) for root in roots}
    need([len(child_sets[root]) for root in sorted(roots)] == [12, 14, 12, 10, 15, 7, 19],
         'S9 AND boundary changed')
    leaves = set().union(*child_sets.values())
    need(len(leaves) == 89 and fmt(leaves) == args.s10_manifest.read_text().splitlines(),
         'S10 child manifest changed')
    parents = {canonical(root ^ (1 << p)) for root in roots for p in points(root)}
    need(len(parents) == 63 and fmt(parents) == args.s8_manifest.read_text().splitlines(),
         'S8 parent manifest changed')
    for parent in parents:
        need(safe(parent) and bool(children(parent) & roots), 'invalid S8->S9 witness')
    stats = {}
    for leaf in sorted(leaves):
        need(safe(leaf), 'unsafe S10 leaf')
        outcome, states = next_player_wins_at_s10(leaf)
        need(outcome, f'S10 LOSS at {leaf:032x}')
        stats[f'{leaf:032x}'] = len(legal(leaf))
    rows = {}
    for line in args.cpp_tsv.read_text().splitlines():
        key, verdict, states, moves = line.split()
        need(key not in rows and verdict == 'WIN', 'duplicate/LOSS C++ leaf')
        rows[key] = int(moves)
    need(rows == stats, 'C++/Python key, outcome or legal-move disagreement')
    if args.frozen_win:
        need(not parents & read(args.frozen_win, 13501, 8), 'frozen WIN overlap')
    if args.frozen_loss:
        need(not parents & read(args.frozen_loss, 294, 8), 'WIN/LOSS conflict')
    if args.emit_s10:
        args.emit_s10.write_text('\n'.join(fmt(leaves)) + '\n')
    print('PASS 7 S9 WIN, 89 S10 WIN leaves, 63 S8 WIN; empty=UNKNOWN')


if __name__ == '__main__':
    main()

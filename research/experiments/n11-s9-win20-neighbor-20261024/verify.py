#!/usr/bin/env python3
"""Independent S10 terminal verification for 20 S9 WIN roots (fixed first-player polarity)."""
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


def fmt(boards):
    return [f'{b:032x}' for b in sorted(boards)]


def read_keys(path, n, stones):
    raw = path.read_text(encoding='utf-8').splitlines()
    need(len(raw) == n and raw == sorted(set(raw)), f'count/order/duplicate: {path}')
    need(all(len(k) == 32 and set(k) <= set('0123456789abcdef') for k in raw),
         f'bad hex: {path}')
    boards = {int(k, 16) for k in raw}
    need(all(b.bit_count() == stones and canonical(b) == b and safe(b) for b in boards),
         f'noncanonical/unsafe: {path}')
    return boards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cpp-tsv', type=Path, required=True)
    ap.add_argument('--emit-s10', type=Path)
    ap.add_argument('--s10-manifest', type=Path, default=HERE / 's10-win233.keys')
    ap.add_argument('--s8-manifest', type=Path, default=HERE / 's8-win167.keys')
    ap.add_argument('--frozen-win', type=Path)
    ap.add_argument('--frozen-loss', type=Path)
    args = ap.parse_args()
    roots = read_keys(HERE / 's9-win20.keys', 20, 9)
    child_sets = {r: children(r) for r in roots}
    need(sum(map(len, child_sets.values())) == 246, 'S9->S10 edges changed')
    leaves = set().union(*child_sets.values())
    need(len(leaves) == 233 and fmt(leaves) == args.s10_manifest.read_text().splitlines(),
         'S10 complete-child manifest changed')
    parents = {canonical(r ^ (1 << p)) for r in roots for p in points(r)}
    need(len(parents) == 167 and fmt(parents) == args.s8_manifest.read_text().splitlines(),
         'S8 parent manifest changed')
    for p in parents:
        need(safe(p) and bool(children(p) & roots), 'invalid S8->S9 witness')
    cpp = {}
    for line in args.cpp_tsv.read_text().splitlines():
        key, verdict, states, moves = line.split()
        need(key not in cpp and verdict in ('WIN', 'LOSS'), 'duplicate/bad C++ row')
        cpp[key] = (verdict, int(states), int(moves))
    need(set(cpp) == set(fmt(leaves)), 'C++ leaf list differs')
    need(sum(row[1] for row in cpp.values()) == 4985, 'C++ state total differs')
    for leaf in sorted(leaves):
        key = f'{leaf:032x}'
        need(safe(leaf), f'unsafe S10: {key}')
        outcome, _ = next_player_wins_at_s10(leaf)
        need(outcome and cpp[key][0] == 'WIN' and cpp[key][2] == len(legal(leaf)),
             f'Python/C++ terminal disagreement: {key}')
    if args.frozen_win:
        need(not parents & read_keys(args.frozen_win, 13501, 8), 'frozen WIN overlap')
    if args.frozen_loss:
        need(not parents & read_keys(args.frozen_loss, 294, 8), 'frozen LOSS conflict')
    if args.emit_s10:
        args.emit_s10.write_text('\n'.join(fmt(leaves)) + '\n', encoding='utf-8')
    print('PASS 20 S9 WIN, 246 edges, 233 S10 WIN, 167 S8 WIN; empty=UNKNOWN')


if __name__ == '__main__':
    main()

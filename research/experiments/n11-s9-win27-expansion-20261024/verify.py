#!/usr/bin/env python3
"""Independent exact terminal proof: 27 S9 WIN and their S8 WIN parents.

Uses the existing 3x3 integer circle implementation, not C++ verdicts or
persistent S5/S4 caches. Optional C++ TSV is checked row by row.
"""
import argparse
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-four-s8-joint-terminal52-20261023'))
from terminal_geometry import (canonical, children, legal, points, safe,
                               next_player_wins_at_s10)


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def keys(path):
    rows = Path(path).read_text().split()
    require(all(len(s) == 32 and all(c in '0123456789abcdef' for c in s)
                for s in rows), f'bad hex key in {path}')
    require(rows == sorted(set(rows)), f'keys not sorted and unique: {path}')
    return [int(s, 16) for s in rows]


def boundary():
    roots = keys(HERE / 's9-win27.keys')
    require(len(roots) == 27, 'expected 27 S9 roots')
    for board in roots:
        require(board.bit_count() == 9 and safe(board)
                and canonical(board) == board, 'invalid S9 root')
    s10 = sorted(set().union(*(children(board) for board in roots)))
    require(len(s10) == 503, 'expected 503 unique S10 children')
    require(sum(len(legal(board)) for board in roots) == 513,
            'expected 513 legal S9 -> S10 edges')
    parents = {canonical(board ^ (1 << p))
               for board in roots for p in points(board)}
    require(len(parents) == 231, 'expected 231 S8 parents')
    for board in parents:
        require(board.bit_count() == 8 and safe(board), 'invalid S8 parent')
        require(any(board in {canonical(root ^ (1 << p))
                              for p in points(root)} for root in roots),
                'S8 parent lacks a legal S9 WIN child')
    return roots, s10, parents


def baseline(roots, parents):
    data = EXP / 'n11-targeted-terminal-lift-20261015' / 'data'
    prior9 = set(keys(data / 'lifted_s9_win_51571.txt'))
    prior8 = set(keys(data / 'lifted_s8_win_51571.txt'))
    prior8loss = set(keys(data / 'all_s8_loss_294.txt'))
    old29 = keys(EXP / 'n11-s9-win29-lift-20261023' / 's9-win29.keys')
    old8 = {canonical(board ^ (1 << p))
            for board in old29 for p in points(board)}
    require((len(prior9), len(prior8), len(prior8loss), len(old29), len(old8))
            == (1611, 13501, 294, 29, 231), 'baseline count mismatch')
    require(len(set(roots) & prior9) == 2, 'S9 baseline overlap changed')
    require(not set(roots) & set(old29), 'S9 overlap with 29 roots')
    require(len(parents & prior8) == 24, 'S8 baseline overlap changed')
    require(len(parents & old8) == 19, 'S8 overlap with 29-root parents changed')
    require(len(parents - (prior8 | old8)) == 191,
            'expected 191 S8 additions against frozen union')
    require(not parents & prior8loss, 'known S8 WIN/LOSS conflict')
    print('BASELINE S9=25 new vs 1611+29; S8=191 new vs 13501+231; '
          'S8 LOSS conflicts=0')


def check_cpp(path, s10, computed):
    rows = Path(path).read_text().splitlines()
    require(len(rows) == len(s10), 'C++ row count mismatch')
    for i, (line, board) in enumerate(zip(rows, s10)):
        fields = line.split()
        require(len(fields) == 4, f'C++ malformed row {i}')
        key, verdict, states, count = fields
        require(key == f'{board:032x}', f'C++ key mismatch at {i}')
        require(verdict == 'WIN', f'C++ opposite verdict at {i}')
        require((int(states), int(count)) == computed[i],
                f'C++ / Python mismatch at {i}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--emit-s10', type=Path)
    ap.add_argument('--cpp-tsv', type=Path)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    roots, s10, parents = boundary()
    if args.emit_s10:
        args.emit_s10.write_text(''.join(f'{m:032x}\n' for m in s10))
        print('EMITTED 503 S10 keys')
        return
    require(args.check, 'use --emit-s10 or --check')
    baseline(roots, parents)
    computed = []
    for board in s10:
        require(board.bit_count() == 10 and safe(board)
                and canonical(board) == board, 'invalid S10 leaf')
        win, states = next_player_wins_at_s10(board)
        require(win, f'S10 LOSS child: {board:032x}')
        computed.append((states, len(legal(board))))
    require(sum(s for s, _ in computed) == 53984,
            'S10 state count differs from recorded independent proof')
    if args.cpp_tsv:
        check_cpp(args.cpp_tsv, s10, computed)
    print('PASS 27 S9 WIN, 513 edges, 503 unique S10 WIN, '
          '53984 individual terminal states, 231 S8 WIN, empty=UNKNOWN')


if __name__ == '__main__':
    main()

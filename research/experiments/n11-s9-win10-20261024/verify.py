#!/usr/bin/env python3
"""Independent terminal certificate: ten S9 WIN roots, all S10 children, S8 lift.

Fixed original-first-player perspective, normal play, standard 11x11, q=4.
Selection-stage verdicts and persistent search caches are never read.
"""
import argparse
import hashlib
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-four-s8-joint-terminal52-20261023'))
from terminal_geometry import canonical, children, legal, next_player_wins_at_s10, points, safe


def need(ok, message):
    if not ok:
        raise ValueError(message)


def keys(path):
    data = Path(path).read_text()
    lines = data.splitlines()
    need(lines == sorted(set(lines)), f'unsorted/duplicate keys: {path}')
    need(all(len(h) == 32 and set(h) <= set('0123456789abcdef') for h in lines),
         f'invalid hex keys: {path}')
    return [int(h, 16) for h in lines]


def digest(items):
    data = ''.join(f'{m:032x}\n' for m in items).encode()
    return hashlib.sha256(data).hexdigest()


def boundary():
    roots = keys(HERE / 's9-win10.keys')
    need(len(roots) == 10, 'expected ten S9 roots')
    need(all(m.bit_count() == 9 and safe(m) and canonical(m) == m for m in roots),
         'unsafe or noncanonical S9 root')
    s10 = sorted(set().union(*(children(m) for m in roots)))
    edges = sum(len(legal(m)) for m in roots)
    need((len(s10), edges) == (186, 187), 'S9 full legal boundary changed')
    need(digest(s10) == '7a55f59d52a27d2cfb739460fb6666f7aebbce1ad9f3eae28af482f825d4374a',
         'S10 boundary digest changed')
    parents = sorted({canonical(m ^ (1 << p)) for m in roots for p in points(m)})
    need(len(parents) == 88, 'expected 88 S8 parents')
    need(digest(parents) == '15677eab68b7e46630a06e89fe63a0f06f4e622484e9e49645e3ecdc81cd26e5',
         'S8 parent digest changed')
    need(all(m.bit_count() == 8 and safe(m) for m in parents), 'unsafe S8 parent')
    return roots, s10, parents


def baseline(roots, parents):
    data = EXP / 'n11-targeted-terminal-lift-20261015' / 'data'
    old9 = set(keys(data / 'lifted_s9_win_51571.txt'))
    old8 = set(keys(data / 'lifted_s8_win_51571.txt'))
    old8loss = set(keys(data / 'all_s8_loss_294.txt'))
    oldroots = []
    for folder, name in [('n11-s9-win29-lift-20261023', 's9-win29.keys'),
                         ('n11-s9-win27-expansion-20261024', 's9-win27.keys'),
                         ('n11-s9-win2-followup-20261024', 's9-win2.keys')]:
        oldroots += keys(EXP / folder / name)
    oldparents = {canonical(m ^ (1 << p)) for m in oldroots for p in points(m)}
    need((len(old9), len(old8), len(old8loss), len(oldroots), len(oldparents)) ==
         (1611, 13501, 294, 58, 458), 'frozen comparison sets changed')
    need(not set(roots) & (old9 | set(oldroots)), 'S9 already known in baseline')
    need(not set(parents) & old8loss, 'S8 WIN/LOSS conflict')
    need(len(set(parents) & old8) == 1, 'S8 baseline overlap changed')
    need(len(set(parents) & oldparents) == 8, 'S8 recent-parent overlap changed')
    need(len(set(parents) - (old8 | oldparents)) == 80,
         'S8 new-parent count changed')
    print('BASELINE +10 S9 vs 1611+58; +80 S8 vs 13501+458; conflicts=0')


def verify_cpp(path, s10, computed):
    rows = Path(path).read_text().splitlines()
    need(len(rows) == len(s10), 'C++ TSV row count mismatch')
    for i, (line, board) in enumerate(zip(rows, s10)):
        cols = line.split()
        need(len(cols) == 4, f'C++ malformed row {i}')
        key, verdict, states, moves = cols
        need(key == f'{board:032x}', f'C++ S10 key mismatch at {i}')
        need(verdict == 'WIN', f'C++ S10 LOSS at {i}')
        need((int(states), int(moves)) == computed[i],
             f'C++/Python independent mismatch at {i}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--emit-s10', type=Path)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--cpp-tsv', type=Path)
    ap.add_argument('--skip-baseline', action='store_true',
                    help='local smoke only; full reproduce checks baseline')
    args = ap.parse_args()
    roots, s10, parents = boundary()
    if args.emit_s10:
        args.emit_s10.write_text(''.join(f'{m:032x}\n' for m in s10))
        print('EMITTED 186 canonical S10 children')
        return
    need(args.check, 'use --emit-s10 or --check')
    if not args.skip_baseline:
        baseline(roots, parents)
    computed = []
    for board in s10:
        need(board.bit_count() == 10 and safe(board) and canonical(board) == board,
             'invalid S10 leaf')
        win, states = next_player_wins_at_s10(board)
        need(win, f'S10 LOSS contradicts S9 WIN: {board:032x}')
        computed.append((states, len(legal(board))))
    need(sum(s for s, _ in computed) == 18513, 'S10 state sum changed')
    if args.cpp_tsv:
        verify_cpp(args.cpp_tsv, s10, computed)
    print('PASS 10 S9 WIN, 187 edges, 186 S10 WIN, 18513 individual terminal states, '
          '88 S8 WIN parents; empty=UNKNOWN')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Independent exact certificate for two S9 WIN roots and seventeen S8 parents.

Standard 11x11, q=4, normal play, original first-player fixed viewpoint.
"""
import argparse
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-four-s8-joint-terminal52-20261023'))
from terminal_geometry import canonical, children, legal, next_player_wins_at_s10, points, safe


def require(condition, msg):
    if not condition:
        raise ValueError(msg)


def load_keys(path):
    lines = Path(path).read_text().splitlines()
    require(lines == sorted(set(lines)), f'keys not sorted and unique: {path}')
    require(all(len(h) == 32 and set(h) <= set('0123456789abcdef') for h in lines),
            f'invalid key: {path}')
    return [int(h, 16) for h in lines]


def boundary():
    roots = load_keys(HERE / 's9-win2.keys')
    require(len(roots) == 2, 'expected two S9 roots')
    for root in roots:
        require(root.bit_count() == 9 and safe(root) and canonical(root) == root,
                'invalid S9 root')
    s10 = sorted(set().union(*(children(root) for root in roots)))
    require(len(s10) == 42, 'expected 42 unique S10 children')
    require(sum(len(legal(root)) for root in roots) == 42, 'expected 42 legal edges')
    parents = sorted({canonical(root ^ (1 << p)) for root in roots for p in points(root)})
    require(len(parents) == 17, 'expected 17 S8 parents')
    require(parents == load_keys(HERE / 's8-win17.keys'), 'S8 parent certificate mismatch')
    for parent in parents:
        require(parent.bit_count() == 8 and safe(parent), 'invalid S8 parent')
    return roots, s10, parents


def baseline(roots, parents):
    data = EXP / 'n11-targeted-terminal-lift-20261015' / 'data'
    old8 = set(load_keys(data / 'lifted_s8_win_51571.txt'))
    old8loss = set(load_keys(data / 'all_s8_loss_294.txt'))
    old9 = set(load_keys(data / 'lifted_s9_win_51571.txt'))
    old29 = load_keys(EXP / 'n11-s9-win29-lift-20261023' / 's9-win29.keys')
    old27 = load_keys(EXP / 'n11-s9-win27-expansion-20261024' / 's9-win27.keys')
    prior8 = {canonical(root ^ (1 << p)) for root in old29 + old27
              for p in points(root)}
    require((len(old8), len(old8loss), len(old9), len(prior8)) ==
            (13501, 294, 1611, 443), 'frozen baseline size changed')
    require(not set(roots) & (old9 | set(old29) | set(old27)),
            'S9 root already in specified baseline')
    require(len(set(parents) - old8) == 17, 'S8 baseline addition mismatch')
    require(len(set(parents) - (old8 | prior8)) == 15,
            'S8 addition versus earlier 56 roots mismatch')
    require(not set(parents) & old8loss, 'known S8 WIN/LOSS conflict')
    print('BASELINE 2 S9 not in 1611+56; S8 +17 vs 13501; '
          '+15 vs 13501+443; conflict 0')


def check_tsv(path, s10, computed):
    lines = Path(path).read_text().splitlines()
    require(len(lines) == len(s10), 'terminal row count mismatch')
    for i, (line, board) in enumerate(zip(lines, s10)):
        fields = line.split()
        require(len(fields) == 4, f'bad terminal row {i}')
        h, verdict, states, moves = fields
        require(h == f'{board:032x}', f'terminal key mismatch {i}')
        require(verdict == 'WIN', f'terminal LOSS contradicts S9 WIN {i}')
        require((int(states), int(moves)) == computed[i],
                f'terminal independent mismatch {i}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--emit-s10', type=Path)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--cpp-tsv', type=Path)
    ap.add_argument('--skip-baseline', action='store_true',
                    help='local standalone test only; full reproduce checks baseline')
    args = ap.parse_args()
    roots, s10, parents = boundary()
    if args.emit_s10:
        args.emit_s10.write_text(''.join(f'{m:032x}\n' for m in s10))
        print('EMITTED 42 S10 keys')
        return
    require(args.check, 'use --emit-s10 or --check')
    if not args.skip_baseline:
        baseline(roots, parents)
    computed = []
    for board in s10:
        require(board.bit_count() == 10 and safe(board) and canonical(board) == board,
                'invalid S10 child')
        win, states = next_player_wins_at_s10(board)
        require(win, f'S10 LOSS child: {board:032x}')
        computed.append((states, len(legal(board))))
    require(sum(states for states, _ in computed) == 4995,
            'independent terminal state sum changed')
    check_tsv(HERE / 's10-win42.tsv', s10, computed)
    if args.cpp_tsv:
        check_tsv(args.cpp_tsv, s10, computed)
    print('PASS 2 S9 WIN, 42 S10 WIN leaves, 4995 individual terminal states, '
          '17 S8 WIN parents, empty=UNKNOWN')


if __name__ == '__main__':
    main()

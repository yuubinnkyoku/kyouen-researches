#!/usr/bin/env python3
"""Exact 11x11 S9 terminal certificates and reverse-frontier audit.

All WIN/LOSS labels are from the original first player's perspective.
The C++ checker uses 4x4 determinants; this Python checker uses an
independent integer 3x3 determinant and subset-game recurrence.
Neither checker trusts historical solver verdicts.
"""
import argparse
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-four-s8-joint-terminal52-20261023'))
from terminal_geometry import canonical, children, legal, points, safe, next_player_wins_at_s10

BASE = EXP / 'n11-targeted-terminal-lift-20261015/data'
PRIOR_WIN9 = [
    'n11-s9-win29-lift-20261023/s9-win29.keys',
    'n11-s9-win27-expansion-20261024/s9-win27.keys',
    'n11-s9-win2-followup-20261024/s9-win2.keys',
    'n11-s9-win10-20261024/s9-win10.keys',
    'n11-s9-win7-expansion-20261024/s9-win7.keys',
    'n11-s9-win20-neighbor-20261024/s9-win20.keys',
]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read_keys(path):
    lines = Path(path).read_text(encoding='utf-8').splitlines()
    need(lines == sorted(set(lines)), f'unsorted or duplicate keys: {path}')
    need(all(re.fullmatch(r'[0-9a-f]{32}', s) for s in lines),
         f'invalid hex key: {path}')
    return {int(s, 16) for s in lines}


def reverse(boards):
    return {canonical(b ^ (1 << p)) for b in boards for p in points(b)}


def boundary():
    wins = read_keys(HERE / 's9-win7.keys')
    need(len(wins) == 7, 'S9 WIN count')
    for b in wins:
        need(b.bit_count() == 9 and canonical(b) == b and safe(b),
             'invalid S9 WIN root')
    win_leaves = set().union(*(children(b) for b in wins))
    need(len(win_leaves) == 63 and sum(len(children(b)) for b in wins) == 79,
         'S9 WIN boundary changed')
    lines = (HERE / 's9-loss6-witness.tsv').read_text().splitlines()
    pairs = [line.split() for line in lines]
    need(len(pairs) == 6 and all(len(row) == 2 for row in pairs),
         'S9 LOSS witness count')
    need([row[0] for row in pairs] == sorted(set(row[0] for row in pairs)),
         'S9 LOSS roots not sorted and distinct')
    loss_roots, loss_leaves = set(), set()
    for root, leaf in pairs:
        need(re.fullmatch(r'[0-9a-f]{32}', root) and
             re.fullmatch(r'[0-9a-f]{32}', leaf), 'bad witness hex')
        b, c = int(root, 16), int(leaf, 16)
        need(b.bit_count() == 9 and canonical(b) == b and safe(b),
             'invalid S9 LOSS root')
        need(c in children(b), 'LOSS witness is not a legal S10 child')
        loss_roots.add(b)
        loss_leaves.add(c)
    need(len(loss_roots) == 6 and len(loss_leaves) == 5,
         'LOSS witness deduplication changed')
    need(not (loss_roots & wins) and not (loss_leaves & win_leaves),
         'WIN/LOSS contradiction within certificate')
    for leaf in win_leaves | loss_leaves:
        need(leaf.bit_count() == 10 and canonical(leaf) == leaf and safe(leaf),
             'invalid canonical S10 leaf')
    return wins, win_leaves, loss_roots, loss_leaves


def verify_terminal(win_leaves, loss_leaves, cpp_path):
    cpp = {}
    for line in Path(cpp_path).read_text().splitlines():
        row = line.split()
        need(len(row) == 4, 'malformed C++ row')
        key, verdict, states, moves = row
        need(re.fullmatch(r'[0-9a-f]{32}', key) and key not in cpp,
             'invalid or duplicate C++ key')
        need(verdict in ('WIN', 'LOSS') and states.isdecimal() and
             moves.isdecimal(), 'malformed C++ verdict')
        cpp[key] = (verdict, int(states), int(moves))
    leaves = win_leaves | loss_leaves
    need(set(cpp) == {f'{b:032x}' for b in leaves},
         'missing or extra C++ leaf')
    state_sum = 0
    for b in sorted(leaves):
        win, states = next_player_wins_at_s10(b)
        need(win == (b in win_leaves), f'opposite Python terminal verdict {b:032x}')
        need(cpp[f'{b:032x}'] == ('WIN' if win else 'LOSS',
                                  states, len(legal(b))),
             f'C++/Python terminal mismatch {b:032x}')
        state_sum += states
    need(state_sum == 3122, 'independent terminal state total changed')
    return state_sum


def audit(wins, loss_leaves):
    prior9 = set().union(*(read_keys(EXP / p) for p in PRIOR_WIN9))
    old_cert = json.loads((EXP / 'n11-s7-terminal-loss12-20261024/certificate.json').read_text())
    prior9 |= {int(s, 16) for s in old_cert['new_s9_win']}
    need(len(prior9) == 113 and not (wins & prior9),
         '113 earlier terminal S9 WIN roots changed')
    frozen9 = read_keys(BASE / 'lifted_s9_win_51571.txt')
    need(len(frozen9) == 1611 and len(wins & frozen9) == 5,
         'frozen S9 WIN overlap changed')
    prior8, new8 = reverse(prior9), reverse(wins)
    need((len(prior8), len(new8), len(prior8 & new8)) == (904, 57, 0),
         'terminal S8 parent counts changed')
    frozen8win = read_keys(BASE / 'lifted_s8_win_51571.txt')
    frozen8loss = read_keys(BASE / 'all_s8_loss_294.txt')
    need((len(frozen8win), len(frozen8loss)) == (13501, 294),
         'frozen S8 comparison counts changed')
    need(not (new8 & frozen8loss), 'new S8 WIN contradicts frozen LOSS')
    new8_only = new8 - prior8 - frozen8win
    need(len(new8 & frozen8win) == 43 and len(new8_only) == 14,
         'new S8 WIN delta changed')
    edges = {(canonical(b ^ (1 << p)), b)
             for b in new8_only for p in points(b)}
    need(len(edges) == 112 and len({p for p, _ in edges}) == 63,
         'new terminal-backed S7 coverage changed')
    need(int('00000000041000001000501000102000', 16) in new8,
         'target S8 WIN witness lost')

    old10loss = read_keys(EXP / 'n11-s8-to-s7-lift238-20261020/selected385.txt')
    old10loss |= {int(s, 16) for s in old_cert['s10_loss_cover39']}
    old10loss |= {int(s, 16) for s in old_cert['s10_loss_cover12']}
    old10loss |= read_keys(EXP / 'n11-s9-loss12-frontier-20261024/s10-loss12.keys')
    need(len(old10loss) == 439 and not (old10loss & loss_leaves),
         'S10 LOSS source overlap changed')
    old9loss, new9loss = reverse(old10loss), reverse(old10loss | loss_leaves)
    need((len(old9loss), len(new9loss)) == (4273, 4319),
         'S9 LOSS reverse closure changed')
    need(not (new9loss & (prior9 | wins)),
         'S9 WIN/LOSS conflict')
    old8front, new8front = reverse(old9loss), reverse(new9loss)
    need((len(old8front), len(new8front)) == (17798, 17978),
         'S8 LOSS candidate frontier changed')
    affected = reverse(new9loss - old9loss)
    changed, gain, closed = 0, 0, 0
    for b in affected:
        cs = children(b)
        before, after = len(cs & old9loss), len(cs & new9loss)
        need(before <= after, 'coverage regression')
        if after > before:
            changed += 1
            gain += after - before
            closed += after == len(cs)
    need((changed, gain, closed) == (197, 414, 0),
         'S8 LOSS coverage audit changed')
    return {'s9_win_terminal': 7, 's9_win_new_vs_frozen': 2,
            's10_win_leaves': 63, 's8_win_parents': 57,
            's8_win_new_vs_frozen_and_prior': 14,
            'new_s7_covered_edges': 112, 's9_loss_witnesses': 6,
            's10_loss_leaves': 5, 's9_loss_reverse_gain': 46,
            's8_loss_frontier_gain': 180, 's8_loss_coverage_gain': 414,
            's8_loss_changed': 197, 'new_s8_loss_closed': 0,
            'new_s7_closed': 'not established', 'empty_winner': 'UNKNOWN'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit-s10', type=Path)
    parser.add_argument('--cpp-tsv', type=Path)
    parser.add_argument('--s10-manifest', type=Path)
    args = parser.parse_args()
    wins, win_leaves, loss_roots, loss_leaves = boundary()
    leaves = win_leaves | loss_leaves
    if args.emit_s10:
        args.emit_s10.write_text(''.join(f'{b:032x}\n' for b in sorted(leaves)))
        print('EMIT 68 unique S10 leaves')
        return
    need(args.cpp_tsv is not None, '--cpp-tsv required for independent check')
    if args.s10_manifest is not None:
        need(read_keys(args.s10_manifest) == leaves, 'S10 manifest incomplete')
    state_sum = verify_terminal(win_leaves, loss_leaves, args.cpp_tsv)
    result = audit(wins, loss_leaves)
    result['s10_individual_terminal_states'] = state_sum
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()

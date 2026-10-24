#!/usr/bin/env python3
"""Recompute 12 S10 LOSS leaves and verify their S9 LOSS witnesses.

Standard q=4 11x11, original first-player WIN/LOSS. At S10, LOSS is
verified by independent terminal minimax; S9 is an AND node, so one S10
LOSS child suffices to certify S9 LOSS.
"""
from pathlib import Path
import argparse
import sys

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-s8-to-s7-lift238-20261020'))
from terminal_geometry import canonical, legal, next_player_wins_at_s10, points, safe


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read_keys(path):
    lines = path.read_text(encoding='utf-8').splitlines()
    need(lines == sorted(set(lines)), f'unsorted or duplicate keys: {path}')
    need(all(len(k) == 32 and set(k) <= set('0123456789abcdef') for k in lines),
         f'invalid key: {path}')
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cpp-tsv', type=Path, default=HERE / 's10-loss12-cpp.tsv')
    ap.add_argument('--witness', type=Path, default=HERE / 's9-loss12-witness.tsv')
    args = ap.parse_args()
    keys = read_keys(HERE / 's10-loss12.keys')
    need(len(keys) == 12, 'expected 12 leaves')
    witness = [line.split() for line in args.witness.read_text().splitlines()]
    need(len(witness) == 12 and all(len(row) == 2 for row in witness), 'bad witness rows')
    need([r for r, _ in witness] == sorted(set(r for r, _ in witness)), 'duplicate S9 roots')
    need(sorted(k for _, k in witness) == keys, 'witness/leaf manifest mismatch')
    cpp = {}
    for line in args.cpp_tsv.read_text().splitlines():
        k, verdict, states, moves = line.split()
        need(k not in cpp and verdict == 'LOSS' and int(states) > 0, 'bad C++ row')
        cpp[k] = (int(states), int(moves))
    need(sorted(cpp) == keys and sum(v[0] for v in cpp.values()) == 338,
         'C++ list or state total mismatch')
    for key in keys:
        leaf = int(key, 16)
        need(leaf.bit_count() == 10 and canonical(leaf) == leaf and safe(leaf),
             f'invalid S10 leaf {key}')
        verdict, _ = next_player_wins_at_s10(leaf)
        need(not verdict and len(legal(leaf)) == cpp[key][1], f'Python/C++ disagreement {key}')
    for r, k in witness:
        root, leaf = int(r, 16), int(k, 16)
        need(root.bit_count() == 9 and canonical(root) == root and safe(root),
             f'invalid S9 root {r}')
        need(any(canonical(leaf ^ (1 << p)) == root for p in points(leaf)),
             f'S10 LOSS leaf is not a legal S9 child {r}')
    print('PASS 12 independent S10 LOSS leaves, 12 S9 LOSS witnesses; empty=UNKNOWN')


if __name__ == '__main__':
    main()

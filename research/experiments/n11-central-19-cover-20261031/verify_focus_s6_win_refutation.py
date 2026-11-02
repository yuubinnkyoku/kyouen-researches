#!/usr/bin/env python3
"""Independently certify a WIN7 child refuting the central49 S6 LOSS plan.

At seven stones the original second player moves first and is losing.
The original first player's strategy must answer *every* second-player move.
The verifier uses 4x4 integer Bareiss geometry from verify_five_terminal_loss7,
not the 3x3 generator or any historical verdict cache.
"""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys

from verify_five_terminal_loss7 import det4, legal, parse, require, verify

S6 = int('0000000000000020380a000000000000', 16)
MOVE = 44
ROOT = '0000000000000020380a100000000000'
HEADER = 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS'
SHA256 = '072454b7a4c72ebf68095d0b90a6c7665a9cef521325435012ac2341a32b9635'
EXPECTED = (7182, 10762, 1255, 9334, (13, 17))


def audit(path):
    root = int(ROOT, 16)
    require(root == S6 | (1 << MOVE), 'root is not the intended S6 child')
    require(S6.bit_count() == 6, 'wrong S6 stone count')
    points = [i for i in range(121) if S6 & (1 << i)]
    require(all(det4(q) != 0 for q in combinations(points, 4)),
            'illegal six-stone witness')
    require(legal(S6) & (1 << MOVE), 'refuting S6 move is illegal')
    data = path.read_bytes()
    require(hashlib.sha256(data).hexdigest() == SHA256, 'certificate hash changed')
    strategy = parse(data, ROOT, header=HEADER)
    stats = verify(root, strategy, winner_parity=1)
    require(stats == EXPECTED, f'changed strategy proof shape: {stats}')
    return {'schema':'n11-central49-focus-s6-win6-terminal-refutation-v1',
            'six_stone_witness':f'{S6:032x}',
            'original_first_winning_move':MOVE,
            'seven_stone_child':ROOT,
            'seven_stone_verdict':'original_first_WIN7',
            'six_stone_verdict':'original_first_WIN6',
            'strategy_states':stats[0],
            'reachable_states':stats[1],
            'terminal_states':stats[2],
            'opponent_reply_edges':stats[3],
            'terminal_stones':list(stats[4]),
            'two_stone_root':'UNKNOWN',
            'empty_board':'UNKNOWN'}


def self_test(path):
    data = path.read_bytes()
    strategy = parse(data, ROOT, header=HEADER)
    lines = data.decode('ascii').splitlines()
    def reject(test, name):
        try:
            test()
        except (ValueError, KeyError, UnicodeError):
            return
        raise AssertionError('accepted invalid certificate: ' + name)
    reject(lambda: parse(('\n'.join(lines[:3]+lines[2:])+'\n').encode(),
                         ROOT, header=HEADER), 'duplicate row')
    reject(lambda: verify(int(ROOT,16),
                          {k:v for i,(k,v) in enumerate(strategy.items()) if i!=0},
                          winner_parity=1), 'missing strategy move')
    reject(lambda: verify(int(ROOT,16),
                          {**strategy, next(iter(strategy)):49},
                          winner_parity=1), 'occupied strategy move')
    reject(lambda: parse(data, ROOT), 'incorrect winning player')
    return 4


if __name__ == '__main__':
    folder = Path(sys.argv[1]) if len(sys.argv)>1 and not sys.argv[1].startswith('--') else Path('.')
    path = folder / ('n11_s7_' + ROOT + '.cert')
    print(json.dumps(audit(path), indent=2))
    if '--self-test' in sys.argv:
        print('negative_tests_rejected', self_test(path))

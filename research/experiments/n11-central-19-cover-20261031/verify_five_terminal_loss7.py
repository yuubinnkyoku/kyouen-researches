#!/usr/bin/env python3
"""Independent five-root terminal strategy auditor for standard 11x11 Kyouen.

The strategy generator uses a 3x3 difference determinant and minimax.
This verifier does not import the generator, its game tree, or any verdict
cache. It recomputes all legal replies with an exact 4x4 integer Bareiss
determinant. No unproved S6/S4/S2 verdict is inferred.
"""
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys

N = 121
FULL = (1 << N) - 1
SCHEMA = 'n11-central49-1985-five-terminal-loss7-v1'
HEADER = 'n11-terminal-strategy-v1 original_first_LOSS7 second_to_move_WIN'
EXPECTED = {
    '00000000000000203808000000000120': (2804, 4239, 510, 3572, (14, 18), 'f8f9dac57ed8708002531ff70312947be37295ab9bd54ebe6172e8e8a20bac66'),
    '0000000000000020380a000000004000': (1208, 1877, 323, 1488, (14, 16), '6203f7fbd8efd3c6cc41db9c7fba4373f806603282b02e3ca6a30fecf631b1cb'),
    '00000000000000a03808100000000000': (786, 1226, 245, 916, (12, 16), '3319b1e1ed6b2f5cd4baf7e7e8107c85fe228ba0caef78351e7eb6aa4c3f0ac1'),
    '00000000000002043800800000040000': (1189, 1851, 318, 1460, (14, 16), 'da05795d8b5c71b70324b403767eb3c721db0d0d7a3d2ba22d117dc46f0e541d'),
    '00000000000200801082008100000000': (2700, 4100, 505, 3484, (14, 18), '3f00b670315509018744d9822f37f9f7fa05be9cd79739b446d478dfd5a9bf8d'),
}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def det4(points):
    # Rows (x*x+y*y, x, y, 1): 4x4 determinant, not the solver's
    # 3x3 difference formula. Bareiss divisions are checked exactly.
    a = []
    for p in points:
        x, y = p % 11, p // 11
        a.append([x*x + y*y, x, y, 1])
    sign, divisor = 1, 1
    for k in range(3):
        if not a[k][k]:
            for j in range(k+1, 4):
                if a[j][k]:
                    a[k], a[j] = a[j], a[k]
                    sign = -sign
                    break
            else:
                return 0
        pivot = a[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                v = a[i][j]*pivot - a[i][k]*a[k][j]
                require(v % divisor == 0, 'non-integral Bareiss step')
                a[i][j] = v // divisor
            a[i][k] = 0
        divisor = pivot
    return sign * a[3][3]


@lru_cache(maxsize=None)
def forbidden_by_triple(a, b, c):
    mask = 0
    for d in range(N):
        if d != a and d != b and d != c and det4((a,b,c,d)) == 0:
            mask |= 1 << d
    return mask


@lru_cache(maxsize=None)
def legal(mask):
    require(0 <= mask <= FULL, 'board out of bounds')
    points = [i for i in range(N) if mask & (1 << i)]
    banned = mask
    for triple in combinations(points, 3):
        banned |= forbidden_by_triple(*triple)
    return FULL & ~banned


def parse(data, expected_root):
    lines = data.decode('ascii').splitlines()
    require(len(lines) >= 3 and lines[0] == HEADER, 'wrong certificate header')
    require(lines[1] == 'root ' + expected_root, 'wrong certificate root')
    strategy = {}
    prev = ''
    for line in lines[2:]:
        parts = line.split(' ')
        require(len(parts) == 2, 'bad strategy row')
        key, move = parts
        require(len(key) == 32 and all(c in '0123456789abcdef' for c in key),
                'bad board encoding')
        require(key > prev, 'unsorted or duplicate board')
        prev = key
        require(move.isdecimal() and 0 <= int(move) < N, 'bad move')
        board = int(key, 16)
        require(board <= FULL, 'out-of-board bit')
        strategy[board] = int(move)
    return strategy


def verify(root, strategy):
    require(root.bit_count() == 7, 'root must have seven stones')
    points = [i for i in range(N) if root & (1 << i)]
    require(all(det4(q) != 0 for q in combinations(points, 4)),
            'illegal seven-stone root')
    seen = set()
    winner_states = set()
    terminals = []
    opponent_edges = 0
    stack = [(root, 0)]
    while stack:
        board, depth = stack.pop()
        if board in seen:
            continue
        seen.add(board)
        options = legal(board)
        if options == 0:
            require(depth % 2 == 1, 'second player has no move')
            require(board not in strategy, 'terminal has strategy move')
            terminals.append(board.bit_count())
            continue
        if depth % 2 == 0:
            require(board in strategy, 'missing second-player move')
            winner_states.add(board)
            move = strategy[board]
            require(options & (1 << move), 'illegal strategy move')
            stack.append((board | (1 << move), depth + 1))
        else:
            require(board not in strategy, 'strategy provided on opponent turn')
            while options:
                bit = options & -options
                options -= bit
                opponent_edges += 1
                stack.append((board | bit, depth + 1))
    require(winner_states == set(strategy), 'unreachable or missing strategy rows')
    require(terminals, 'no terminals')
    return (len(strategy), len(seen), len(terminals), opponent_edges,
            (min(terminals), max(terminals)))


def audit(folder):
    results = {}
    for key, expected in EXPECTED.items():
        path = folder / ('n11_s7_' + key + '.cert')
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected[5],
                'certificate SHA256 mismatch for ' + key)
        strategy = parse(data, key)
        stats = verify(int(key, 16), strategy)
        require(stats == expected[:5], f'changed proof shape for {key}: {stats}')
        results[key] = {'strategy_states':stats[0], 'reachable_states':stats[1],
                        'terminals':stats[2], 'opponent_edges':stats[3],
                        'terminal_stones':list(stats[4]),
                        'verdict':'original_first_LOSS7'}
    return {'schema':SCHEMA,'certificates':results,
            'total_reachable_states':sum(x['reachable_states'] for x in results.values()),
            'total_terminal_states':sum(x['terminals'] for x in results.values()),
            'selected_s6':'UNKNOWN', 'two_stone_root':'UNKNOWN',
            'empty_board':'UNKNOWN'}


def self_test(folder):
    key = next(iter(EXPECTED))
    data = (folder / ('n11_s7_' + key + '.cert')).read_bytes()
    lines = data.decode('ascii').splitlines()
    strategy = parse(data, key)
    def reject(test, label):
        try:
            test()
        except (ValueError, KeyError, UnicodeError, OSError):
            return
        raise AssertionError('failed to reject ' + label)
    reject(lambda: parse(('\n'.join(lines[:3]+lines[2:])+'\n').encode(),key),
           'duplicate strategy row')
    reject(lambda: verify(int(key,16),
                          {k:v for i,(k,v) in enumerate(strategy.items()) if i!=0}),
           'missing strategy row')
    reject(lambda: verify(int(key,16), {**strategy, int(key,16): 49}),
           'occupied move')
    reject(lambda: parse(data.replace(b'original_first_LOSS7',
                                      b'original_first_WIN7'),key),
           'incorrect proof orientation')
    return 4


if __name__ == '__main__':
    folder = Path(sys.argv[1]) if len(sys.argv)>1 and not sys.argv[1].startswith('--') else Path(__file__).parent
    print(json.dumps(audit(folder), indent=2))
    if '--self-test' in sys.argv:
        print('negative_tests_rejected', self_test(folder))

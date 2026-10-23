#!/usr/bin/env python3
"""Independent 3x3 integer-geometry audit of 29 S9 WIN -> 231 S8 WIN.

Uses complete-call standard 11x11 rules and fixed original-first WIN/LOSS.
All S10 leaves are recomputed from terminal positions, without trusting caches.
"""
import argparse
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import sys

P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'n11-four-s8-joint-terminal52-20261023'))
from terminal_geometry import canonical, children, circle, legal, points, safe


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def terminal_s10(m):
    """Independent Python integer-bitset recursion; supports up to 63 legal moves."""
    need(m.bit_count() == 10 and safe(m), 'illegal S10 leaf')
    base = points(m)
    moves = legal(m)
    n = len(moves)
    need(n <= 63, 'unsupported legal move count')
    forbidden = set()
    for i, j in combinations(range(n), 2):
        if any(circle(a, b, moves[i], moves[j]) for a, b in combinations(base, 2)):
            forbidden.add((1 << i) | (1 << j))
    for i, j, k in combinations(range(n), 3):
        e = (1 << i) | (1 << j) | (1 << k)
        if any((e & f) == f for f in forbidden):
            continue
        if any(circle(a, moves[i], moves[j], moves[k]) for a in base):
            forbidden.add(e)
    for ids in combinations(range(n), 4):
        e = sum(1 << i for i in ids)
        if any((e & f) == f for f in forbidden):
            continue
        if circle(*(moves[i] for i in ids)):
            forbidden.add(e)
    blockers = [[] for _ in range(n)]
    for f in forbidden:
        for i in range(n):
            if f & (1 << i):
                blockers[i].append(f ^ (1 << i))

    @lru_cache(None)
    def win(mask):
        for i in range(n):
            bit = 1 << i
            if mask & bit or any((mask & b) == b for b in blockers[i]):
                continue
            if not win(mask | bit):
                return True
        return False
    return win(0), win.cache_info().currsize, n


def read_keys(path):
    rows = Path(path).read_text().split()
    need(all(len(s) == 32 and all(c in '0123456789abcdef' for c in s) for s in rows), 'bad hex keys')
    need(rows == sorted(set(rows)), 'unsorted or duplicate keys')
    return [int(s, 16) for s in rows]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--end', type=int, default=1000000)
    ap.add_argument('--cpp', type=Path)
    ap.add_argument('--check-prior', action='store_true')
    ap.add_argument('--emit-s10', type=Path)
    ap.add_argument('--emit-s8', type=Path)
    args = ap.parse_args()
    s9 = read_keys(P / 's9-win29.keys')
    need(len(s9) == 29, 'S9 count')
    for m in s9:
        need(m.bit_count() == 9 and safe(m) and canonical(m) == m, 'illegal S9 root')
    all_s10 = sorted(set().union(*(children(m) for m in s9)))
    s8 = {canonical(m ^ (1 << p)) for m in s9 for p in points(m)}
    need(len(all_s10) == 734 and len(s8) == 231, 'boundary count')
    need(sum(len(children(m)) for m in s9) == 802, 'S9 edge count')
    for m in s8:
        need(m.bit_count() == 8 and safe(m), 'illegal S8 parent')
    if args.check_prior:
        data = P.parent / 'n11-targeted-terminal-lift-20261015' / 'data'
        old9 = set(read_keys(data / 'lifted_s9_win_51571.txt'))
        old8 = set(read_keys(data / 'lifted_s8_win_51571.txt'))
        loss8 = set(read_keys(data / 'all_s8_loss_294.txt'))
        need(len(old9) == 1611 and len(old8) == 13501 and len(loss8) == 294, 'prior sizes')
        need(len(set(s9) & old9) == 1, 'S9 old overlap')
        need(len(s8 & old8) == 12 and not s8 & loss8, 'S8 overlap or conflict')

    if args.emit_s10:
        args.emit_s10.write_text(''.join(f'{m:032x}\n' for m in all_s10))
    if args.emit_s8:
        args.emit_s8.write_text(''.join(f'{m:032x}\n' for m in sorted(s8)))
    if args.emit_s10 or args.emit_s8:
        print(f'EMITTED s10={len(all_s10)} s8={len(s8)}')
        return
    cpp = None
    if args.cpp:
        cpp = {}
        for line in args.cpp.read_text().splitlines():
            h, verdict, states, legal_count = line.split()
            need(h not in cpp, 'duplicate C++ key')
            cpp[h] = (verdict, int(states), int(legal_count))
        need(set(cpp) == {f'{m:032x}' for m in all_s10}, 'C++ leaf boundary mismatch')
    start = max(0, args.start)
    end = min(len(all_s10), args.end)
    need(0 <= start <= end <= len(all_s10), 'invalid range')
    states_sum = 0
    for m in all_s10[start:end]:
        need(m.bit_count() == 10 and safe(m) and canonical(m) == m, 'illegal canonical S10')
        verdict, states, nlegal = terminal_s10(m)
        need(verdict, f'LOSS child refutes S9 WIN: {m:032x}')
        if cpp is not None:
            need(cpp[f'{m:032x}'] == ('WIN', states, nlegal), f'C++/Python mismatch: {m:032x}')
        states_sum += states
    digest = hashlib.sha256(''.join(f'{m:032x}\n' for m in all_s10).encode()).hexdigest()
    print(f'PASS range={start}:{end} S9_WIN={len(s9)} S10_WIN_total={len(all_s10)} S8_WIN={len(s8)} S9_edges=802 checked={end-start} individual_states={states_sum} s10_sha256={digest} empty=UNKNOWN')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Cache-free terminal proof of one standard 11x11 S7 LOSS.

All verdicts use the original first player's viewpoint. Odd layers are AND,
even layers OR. Previously published S9 roots are independently re-proved.
"""
import argparse
import hashlib
import json
from functools import lru_cache
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / 'n11-s7-coverage-audit-20261024'))
from analyze import canonical, is_safe as safe, legal_points as legal, points  # noqa: E402

def need(ok, msg):
    if not ok:
        raise ValueError(msg)

def children(board):
    return {canonical(board | (1 << p)) for p in legal(board)}

def terminal(board):
    need(board.bit_count() == 10 and safe(board), 'bad S10 root')
    @lru_cache(None)
    def visit(b):
        cs = sorted(children(b))
        return (any(visit(c) for c in cs) if b.bit_count() % 2 == 0
                else all(visit(c) for c in cs))
    result = visit(board)
    return result, visit.cache_info().misses

OLD = (
    ('n11-s9-win29-lift-20261023', 's9-win29.keys', 29),
    ('n11-s9-win27-expansion-20261024', 's9-win27.keys', 27),
    ('n11-s9-win2-followup-20261024', 's9-win2.keys', 2),
    ('n11-s9-win10-20261024', 's9-win10.keys', 10),
)
S10_SHA = '441abd000aa8fddb431f09767b3759e75456a94296aa658867dad980e95fbd74'

def keys(items, expected, name):
    need(isinstance(items, list) and len(items) == expected and
         items == sorted(set(items)), f'{name}: count/order/duplicates')
    need(all(isinstance(s, str) and len(s) == 32 and
             set(s) <= set('0123456789abcdef') for s in items),
         f'{name}: malformed hex')
    return {int(s, 16) for s in items}

def read_old():
    roots = set()
    for folder, filename, count in OLD:
        path = EXP / folder / filename
        values = keys(path.read_text().splitlines(), count, str(path))
        need(not roots & values, 'duplicate old S9 root')
        roots |= values
    need(len(roots) == 68, 'old S9 root count')
    return roots

def parent8(roots):
    return {canonical(m ^ (1 << p)) for m in roots for p in points(m)}

def boundary(cert):
    s7 = int(cert['s7'], 16)
    need(cert['s7'] == '00000000100000021081000020000020', 'S7 key changed')
    old9 = read_old()
    new9 = keys(cert['new_s9_win'], 18, 'new S9')
    loss8 = keys(cert['s8_loss'], 3, 'S8 LOSS')
    cover39 = keys(cert['s10_loss_cover39'], 39, 'LOSS cover39')
    cover12 = keys(cert['s10_loss_cover12'], 12, 'LOSS cover12')
    need(not old9 & new9, 'new S9 overlaps old roots')
    need(all(m.bit_count() == 9 and canonical(m) == m and safe(m)
             for m in old9 | new9), 'unsafe/noncanonical S9 root')
    need(s7.bit_count() == 7 and canonical(s7) == s7 and safe(s7),
         'unsafe/noncanonical S7')
    children8 = children(s7)
    old_win8 = children8 & parent8(old9)
    new_win8 = (children8 & parent8(new9)) - old_win8
    need((len(children8), len(old_win8), len(new_win8), len(loss8)) ==
         (36, 10, 23, 3), 'S7 boundary counts changed')
    need(children8 == old_win8 | new_win8 | loss8,
         'S7 children not partitioned into 33 WIN and 3 LOSS')
    need(all(m.bit_count() == 8 and canonical(m) == m and safe(m)
             for m in loss8), 'unsafe/noncanonical S8 LOSS')
    loss9_by_s8 = {m: children(m) for m in loss8}
    need(sorted(map(len, loss9_by_s8.values())) == [22, 23, 31],
         'S8 LOSS full S9 boundaries changed')
    obligations = set().union(*loss9_by_s8.values())
    need(len(obligations) == 74, 'unique S9 LOSS obligations changed')
    loss10_candidates = {s9: children(s9) for s9 in obligations}
    need(all(loss10_candidates[s9] & cover39 for s9 in obligations),
         '39 LOSS leaves do not cover every S9')
    need(cover39 <= set().union(*loss10_candidates.values()),
         '39 cover contains unrelated S10 leaf')
    first8 = int('00000000100000021081004020000020', 16)
    first9 = loss9_by_s8[first8]
    first10 = set().union(*(loss10_candidates[m] for m in first9))
    need(len(first10) == 181, 'minimality candidate universe changed')
    need(cover12 <= first10 and
         all(loss10_candidates[s9] & cover12 for s9 in first9),
         '12-leaf S8 LOSS cover invalid')
    win9 = old9 | new9
    win10 = set().union(*(children(m) for m in win9))
    need((len(win9), len(win10)) == (86, 1762), 'WIN S9/S10 boundary changed')
    need(not win10 & (cover39 | cover12), 'WIN/LOSS S10 conflict')
    all10 = sorted(win10 | cover39 | cover12 | first10)
    need(len(all10) == 1963, 'terminal verification leaf count changed')
    digest = hashlib.sha256(''.join(f'{m:032x}\n' for m in all10).encode()).hexdigest()
    need(digest == S10_SHA, 'S10 boundary digest changed')
    dual = cert['dual_half_units']
    need(isinstance(dual, dict) and len(dual) == 14 and
         all(type(v) is int and v in (1, 2) for v in dual.values()) and
         sum(dual.values()) == 23, 'dual certificate weight sum changed')
    need(set(int(k, 16) for k in dual) <= first9,
         'dual weights refer to wrong S9 obligations')
    return all10, win10, cover39, cover12, first9, first10, dual

def check_cpp(path, all10, results):
    lines = path.read_text().splitlines()
    need(len(lines) == len(all10), 'C++ row count changed')
    for i, (line, m) in enumerate(zip(lines, all10)):
        cols = line.split()
        need(len(cols) == 4, f'C++ malformed row {i}')
        h, verdict, states, moves = cols
        need(h == f'{m:032x}', f'C++ key mismatch {i}')
        need(verdict == ('WIN' if results[m][0] else 'LOSS'),
             f'C++/Python verdict conflict at {h}')
        need(int(moves) == results[m][2], f'C++/Python legal move conflict at {h}')
        need(int(states) == results[m][1], f'C++/Python state-count mismatch at {h}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--emit-s10', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--cpp-tsv', type=Path)
    parser.add_argument('--check-cpp-known', action='store_true',
                        help='quick negative-control precheck, not independent proof')
    args = parser.parse_args()
    cert = json.loads(args.certificate.read_text())
    all10, win10, cover39, cover12, first9, first10, dual = boundary(cert)
    if args.emit_s10:
        args.emit_s10.write_text(''.join(f'{m:032x}\n' for m in all10))
        print('EMITTED 1963 terminal S10 keys')
        return
    if args.check_cpp_known:
        need(args.cpp_tsv is not None, '--check-cpp-known needs --cpp-tsv')
        rows = args.cpp_tsv.read_text().splitlines()
        need(len(rows) == len(all10), 'C++ row count changed')
        for m, row in zip(all10, rows):
            cols = row.split()
            need(len(cols) == 4 and cols[0] == f'{m:032x}', 'C++ key mismatch')
            if m in win10:
                need(cols[1] == 'WIN', 'known S10 WIN row tampered')
            if m in cover39 | cover12:
                need(cols[1] == 'LOSS', 'known S10 LOSS row tampered')
        print('PASS quick known-leaf precheck (not a terminal proof)')
        return
    need(args.check, 'use --emit-s10 or --check')
    results = {}
    for m in all10:
        need(m.bit_count() == 10 and canonical(m) == m and safe(m),
             f'invalid S10 leaf {m:032x}')
        win, states = terminal(m)
        results[m] = win, states, len(legal(m))
    need(all(results[m][0] for m in win10), 'a certified S9 WIN child is LOSS')
    need(all(not results[m][0] for m in cover39 | cover12),
         'a claimed S10 LOSS witness is WIN')
    loss_candidates = {m for m in first10 if not results[m][0]}
    need((len(first10), len(loss_candidates)) == (181, 49),
         'first S8 complete S10 candidate classification changed')
    # Dual half-units sum to 23; each LOSS leaf covers at most 2.
    # Thus any S8 LOSS certificate of this form needs at least 12 leaves.
    for m in loss_candidates:
        weight = sum(dual.get(f'{s9:032x}', 0)
                     for s9 in first9 if m in children(s9))
        need(weight <= 2, f'dual constraint failed at {m:032x}')
    if args.cpp_tsv:
        check_cpp(args.cpp_tsv, all10, results)
    print('PASS 7-stone LOSS: 36 S8 children = 33 WIN + 3 LOSS; '
          '86 S9 WIN roots, 74 distinct S9 LOSS obligations, '
          '1762 S10 WIN, 39 S10 LOSS cover; 12-leaf minimal '
          'S8 LOSS proof (dual lower bound 11.5); '
          '1963 S10 independent terminal checks; empty=UNKNOWN')

if __name__ == '__main__':
    main()

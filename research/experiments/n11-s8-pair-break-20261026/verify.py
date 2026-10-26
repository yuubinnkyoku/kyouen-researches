#!/usr/bin/env python3
"""Cache-free, dual-geometry N11 S8 LOSS proof and S5 conditional replan.

All WIN/LOSS labels are from the original first player's perspective.
The S10 terminal solver starts from an EMPTY memo table for each geometry.
The 13 proposed S7 roots have no verdict assigned by this verifier.
"""
import argparse
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
ROOT = int('00000410000000821080000002000020', 16)
S5 = int('00000000000000821080000000000020', 16)
NEW7 = int('00000000000100001000000042401008', 16)
FROZEN = EXP / 'n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt'
FROZEN_SHA = '17282f84fd65ad20ac58ef794449a52bcc796d8129a1a3a58d726a305fbeb21e'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Independent 3x3 and 4x4 integer geometry implementations already used
# by terminal-certificate verification elsewhere in this repository.
SOURCE = load('n11_pair_break_source',
              EXP / 'n11-s9-neighbor23-terminal-20261026/verify.py')
THREE, FOUR = SOURCE.THREE, SOURCE.FOUR


def read_certificate():
    lines = (HERE / 'certificate.tsv').read_text(encoding='ascii').splitlines()
    need(len(lines) == 35 and lines[0] == '# n11-s8-pair-break-loss-v1'
         and lines[1] == f'# root {ROOT:032x}'
         and lines[3] == '# s9 s10_loss legal_s10_classes',
         'certificate frame changed')
    weights = [int(x) for x in lines[2].removeprefix('# dual2 ').split()]
    need(lines[2].startswith('# dual2 ') and len(weights) == 31
         and all(x in (0, 1, 2) for x in weights)
         and sum(weights) == 34, 'invalid half-integral dual')
    rows = []
    for line in lines[4:]:
        parts = line.split()
        need(len(parts) == 3 and all(len(s) == 32 and
             set(s) <= set('0123456789abcdef') for s in parts[:2])
             and parts[2].isdecimal(), 'malformed certificate row')
        rows.append((int(parts[0], 16), int(parts[1], 16), int(parts[2])))
    need(len(rows) == 31 and [r[0] for r in rows] ==
         sorted(set(r[0] for r in rows)), 'duplicate/missing S9 row')
    return rows, weights


def reverse(geom, boards):
    return {geom.canonical(b ^ (1 << p))
            for b in boards for p in geom.points(b)}


def boundary(rows, weights):
    need(len(rows) == 31 and len(weights) == 31 and
         sum(weights) == 34 and all(x in (0, 1, 2) for x in weights),
         'invalid certificate shape/dual')
    witnesses = {r[1] for r in rows}
    need(len(witnesses) == 17, 'expected 17 distinct S10 LOSS witnesses')
    for geom in (THREE, FOUR):
        need(ROOT.bit_count() == 8 and geom.safe(ROOT) and
             geom.canonical(ROOT) == ROOT, 'invalid S8 root')
        need(SOURCE.children(geom, ROOT) == {r[0] for r in rows},
             'S8 AND boundary incomplete')
        for s9, s10, n in rows:
            need(s9.bit_count() == 9 and geom.safe(s9) and
                 geom.canonical(s9) == s9, 'invalid S9 child')
            legal10 = SOURCE.children(geom, s9)
            need(len(legal10) == n and s10 in legal10,
                 'invalid S10 LOSS witness / legal child count')
            need(s10.bit_count() == 10 and geom.safe(s10) and
                 geom.canonical(s10) == s10, 'invalid S10 leaf')
    return witnesses


def terminal(witnesses, optimality=False, rows=None, weights=None):
    solvers = [SOURCE.terminal_solver(geom) for geom in (THREE, FOUR)]
    states = [0, 0]
    for leaf in sorted(witnesses):
        r = [solve(leaf) for solve in solvers]
        need(r[0][0] is False and r[1][0] is False,
             f'false S10 LOSS witness: {leaf:032x}')
        need(r[0][1] == r[1][1], 'independent terminal state mismatch')
        need(THREE.legal(leaf) == FOUR.legal(leaf),
             'independent S10 legal moves disagree')
        for i in range(2):
            states[i] += r[i][1]
    if optimality:
        # Dual certificate: weight units are halves. Every *actual LOSS*
        # S10 child may cover at most weight 2, while total S9 weight is 34.
        # Thus >=17 distinct LOSS leaves are required. The certificate has 17.
        by_leaf = {}
        for i, (s9, _, _) in enumerate(rows):
            for leaf in SOURCE.children(THREE, s9):
                by_leaf.setdefault(leaf, set()).add(i)
        need(len(by_leaf) == 352, 'complete S10 candidate universe changed')
        loss = 0
        for leaf in sorted(by_leaf):
            r = [solve(leaf) for solve in solvers]
            need(r[0][0] == r[1][0], 'independent candidate verdict mismatch')
            need(THREE.legal(leaf) == FOUR.legal(leaf),
                 'independent candidate legal moves disagree')
            if r[0][0] is False:
                loss += 1
                need(sum(weights[i] for i in by_leaf[leaf]) <= 2,
                     f'dual infeasible at S10 LOSS leaf {leaf:032x}')
        need(loss == 79, 'S10 LOSS candidate census changed')
    return {'terminal_leaves': len(witnesses),
            'states_per_independent_solver_on_selected_leaves': states[0],
            'optimality_verified': optimality}


def lift_and_replan():
    raw = FROZEN.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == FROZEN_SHA,
         'frozen S7 comparison source changed')
    old7 = {int(h, 16) for h in raw.decode('ascii').split()} | {NEW7}
    need(len(old7) == 18, 'frozen S7 WIN inventory changed')
    results = []
    for geom in (THREE, FOUR):
        loss7 = reverse(geom, {ROOT})
        win6 = reverse(geom, loss7)
        need(len(loss7) == 8 and len(win6) == 28,
             'new S7 LOSS / S6 WIN reverse boundaries changed')
        for s7 in loss7:
            need(ROOT in SOURCE.children(geom, s7),
                 'S7 LOSS lacks legal S8 LOSS witness')
        for s6 in win6:
            need(SOURCE.children(geom, s6) & loss7,
                 'S6 WIN lacks legal S7 LOSS witness')
        old6 = reverse(geom, old7)
        legal6 = SOURCE.children(geom, S5)
        known = legal6 & old6
        extra = (legal6 & win6) - known
        need(len(old6) == 110 and len(legal6) == 32 and
             len(known) == 5 and len(extra) == 2,
             'S5 baseline or new WIN witness coverage changed')
        missing = legal6 - old6 - win6
        need(len(missing) == 25, 'S5 remaining uncovered count changed')
        plan = (HERE / 's7-plan13.keys').read_text('ascii').splitlines()
        need(len(plan) == 13 and plan == sorted(set(plan)) and
             all(len(h) == 32 for h in plan), 'invalid S7 plan')
        proposed = {int(h, 16) for h in plan}
        need(all(p.bit_count() == 7 and geom.safe(p) and
                 geom.canonical(p) == p for p in proposed),
             'invalid candidate S7 root')
        incidence = {s6: SOURCE.children(geom, s6) & proposed
                     for s6 in missing}
        need(all(incidence.values()), 'uncovered S6 in proposed 13-root plan')
        need(all(sum(p in SOURCE.children(geom, s6) for s6 in missing) <= 2
                 for p in proposed), 'unexpected >2-way witness')
        all8 = [SOURCE.children(geom, p) for p in proposed]
        frozen_loss8 = {int(h, 16) for h in (EXP /
            'n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt')
            .read_text('ascii').split()}
        need(len(frozen_loss8) == 294 and
             all(not (children & frozen_loss8) for children in all8),
             'proposed S7 WIN has frozen S8 LOSS child')
        need(sum(map(len, all8)) == 558 and
             len(set().union(*all8)) == 558,
             'S7->S8 conditional plan boundary changed')
        need(all(ROOT not in c for c in all8),
             'already proven LOSS S8 contradicts proposed S7 WIN')
        results.append((sorted(missing), sorted(proposed)))
    need(results[0] == results[1], 'independent S5/plan geometries disagree')
    return {'new_s7_loss_parents': 8, 'new_s6_win_witness_parents': 28,
            'newly_secured_s5_children_against_18_s7_win': 2,
            's5_secured_children': 7, 's5_uncovered_children': 25,
            'conditional_s7_plan_roots': 13, 'conditional_s7_to_s8_edges': 558,
            'conditional_distinct_s8_children': 558,
            's5_outcome': 'UNPROVEN', 'empty_board': 'UNKNOWN'}


def verify(negative=False, optimality=False):
    rows, weights = read_certificate()
    leaves = boundary(rows, weights)
    if negative:
        tests = [
            (rows[:-1], weights),
            ([rows[0]] + rows[:-1], weights),
            ([(rows[0][0], rows[0][0], rows[0][2])] + rows[1:], weights),
            ([(rows[0][0], rows[0][1], rows[0][2]+1)] + rows[1:], weights),
            (rows, [0]+weights[1:]),
        ]
        for bad_rows, bad_weights in tests:
            try:
                boundary(bad_rows, bad_weights)
            except ValueError:
                continue
            raise ValueError('tampered S8 LOSS certificate accepted')
    a = terminal(leaves, optimality, rows, weights)
    b = lift_and_replan()
    print({'s8_loss_root': f'{ROOT:032x}', 's9_obligations': 31, **a, **b})
    if negative:
        print('PASS five S8 LOSS certificate mutation rejections')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--negative', action='store_true')
    ap.add_argument('--optimality', action='store_true')
    args = ap.parse_args()
    verify(args.negative, args.optimality)

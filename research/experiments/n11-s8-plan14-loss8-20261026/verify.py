#!/usr/bin/env python3
"""Independent S8 LOSS terminal proof, dual minimum and corrected S7 plan.

All verdicts are from the ORIGINAL first player's perspective. A LOSS S8
child proves its S7 parent LOSS, not any S6 parent WIN. No cached verdict is
trusted for the new S8/S7 proof. Two exact integer geometries independently
recompute all legal boundaries and terminal outcomes from empty memo tables.
"""
import argparse
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
ROOT = int('00004000000000821080000040400020', 16)
BAD7 = int('00004000000000821080000040000020', 16)
REPLACEMENT = int('00004000000000821080000001000020', 16)
S5 = int('00000000000000821080000000000020', 16)
NEW7 = int('00000000000100001000000042401008', 16)
FROZEN7 = EXP / 'n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt'
FROZEN7_SHA256 = '17282f84fd65ad20ac58ef794449a52bcc796d8129a1a3a58d726a305fbeb21e'
FROZEN_LOSS8 = EXP / 'n11-targeted-terminal-lift-20261015/data/all_s8_loss_294.txt'
OLD_PLAN = EXP / 'n11-s8-pair-break-20261026/s7-plan14.keys'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SOURCE = load('n11_plan14_loss8_source',
              EXP / 'n11-s9-neighbor23-terminal-20261026/verify.py')
THREE, FOUR = SOURCE.THREE, SOURCE.FOUR


def read_certificate():
    lines = (HERE / 'certificate.tsv').read_text('ascii').splitlines()
    need(len(lines) == 20 and lines[:2] == [
        '# n11-s8-loss-plan14-v1', f'# root {ROOT:032x}']
        and lines[3] == '# s9 s10_loss legal_s10_classes',
        'invalid certificate header/row count')
    need(lines[2].startswith('# dual2 '), 'missing dual weights')
    weights = [int(x) for x in lines[2][8:].split()]
    need(len(weights) == 16 and sum(weights) == 16 and
         all(x in (0, 1, 2) for x in weights), 'invalid dual weights')
    rows = []
    for line in lines[4:]:
        cells = line.split()
        need(len(cells) == 3 and all(len(h) == 32 and
             set(h) <= set('0123456789abcdef') for h in cells[:2])
             and cells[2].isdecimal(), 'invalid certificate row')
        rows.append((int(cells[0], 16), int(cells[1], 16), int(cells[2])))
    need(len(rows) == 16 and [r[0] for r in rows] ==
         sorted({r[0] for r in rows}), 'missing/duplicate/unsorted S9 rows')
    return rows, weights


def boundary(rows, weights):
    need(len(rows) == len(weights) == 16 and sum(weights) == 16 and
         all(w in (0, 1, 2) for w in weights), 'certificate dimensions changed')
    selected = {r[1] for r in rows}
    need(len(selected) == 8, 'expected eight distinct S10 LOSS leaves')
    universes = []
    for geom in (THREE, FOUR):
        need(ROOT.bit_count() == 8 and geom.safe(ROOT) and
             geom.canonical(ROOT) == ROOT, 'invalid S8 root')
        need(SOURCE.children(geom, ROOT) == {r[0] for r in rows},
             'incomplete S8 universal S9 boundary')
        by_leaf = {}
        for i, (s9, s10, n) in enumerate(rows):
            need(s9.bit_count() == 9 and geom.safe(s9) and
                 geom.canonical(s9) == s9, 'invalid S9 obligation')
            children10 = SOURCE.children(geom, s9)
            need(len(children10) == n and s10 in children10,
                 'invalid S10 witness or legal child count')
            need(s10.bit_count() == 10 and geom.safe(s10) and
                 geom.canonical(s10) == s10, 'invalid S10 LOSS witness')
            for leaf in children10:
                by_leaf.setdefault(leaf, set()).add(i)
        need(len(by_leaf) == 86, 'S10 candidate universe changed')
        universes.append(by_leaf)
    need(universes[0] == universes[1], '3x3/4x4 boundary disagreement')
    return selected, universes[0]


def terminal(selected, by_leaf, weights, optimality=True):
    states = []
    for geom in (THREE, FOUR):
        counts = []
        for leaf in sorted(selected):
            # Each leaf starts from a NEW, empty terminal search memo.
            verdict, count = SOURCE.terminal_solver(geom)(leaf)
            need(verdict is False, f'false S10 LOSS witness: {leaf:032x}')
            counts.append(count)
        states.append(counts)
    need(states[0] == states[1] and sum(states[0]) == 192,
         'independent terminal search mismatch')
    if optimality:
        verdicts = []
        for geom in (THREE, FOUR):
            solve = SOURCE.terminal_solver(geom)
            out = {}
            for leaf in sorted(by_leaf):
                outcome, _ = solve(leaf)
                out[leaf] = outcome
                if outcome is False:
                    need(sum(weights[i] for i in by_leaf[leaf]) <= 2,
                         'dual infeasible at actual LOSS S10 leaf')
            verdicts.append(out)
        need(verdicts[0] == verdicts[1], 'S10 candidate verdict conflict')
        need(sum(not v for v in verdicts[0].values()) == 47,
             'S10 LOSS candidate census changed')
        # Each S10 LOSS leaf can cover at most 2 half-weight units.
        # Total S9 weight is 16, so >=8 distinct LOSS leaves are necessary.
        # Eight selected witnesses attain this bound.
    return {'selected_s10_loss_leaves': len(selected),
            'terminal_states_per_independent_solver': sum(states[0]),
            'candidate_s10_classes': len(by_leaf),
            'loss_s10_candidates': 47 if optimality else None,
            'minimum_loss_leaves_by_dual': 8 if optimality else None}


def reverse(geom, boards):
    return {geom.canonical(b ^ (1 << p))
            for b in boards for p in geom.points(b)}


def read_keys(path):
    lines = path.read_text('ascii').splitlines()
    need(lines == sorted(set(lines)) and all(len(h) == 32 and
         set(h) <= set('0123456789abcdef') for h in lines),
         'invalid/unsorted position keys: ' + str(path))
    return {int(h, 16) for h in lines}


def plan_audit(plan):
    need(len(plan) == 14 and BAD7 not in plan and REPLACEMENT in plan,
         'refuted S7 candidate still in plan')
    old = read_keys(OLD_PLAN)
    need(len(old) == 14 and old - plan == {BAD7} and
         plan - old == {REPLACEMENT}, 'unexpected 14-root replan')
    raw = FROZEN7.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == FROZEN7_SHA256,
         'frozen S7 comparison source changed')
    known7 = {int(h, 16) for h in raw.decode('ascii').split()} | {NEW7}
    need(len(known7) == 18, 'known S7 witness inventory changed')
    frozen_loss = read_keys(FROZEN_LOSS8)
    need(len(frozen_loss) == 294, 'frozen LOSS8 comparison source changed')
    audits = []
    for geom in (THREE, FOUR):
        loss7 = reverse(geom, {ROOT})
        need(len(loss7) == 8 and BAD7 in loss7 and
             not (loss7 & plan), 'new S7 LOSS parent in proposed WIN plan')
        need(ROOT in SOURCE.children(geom, BAD7),
             'illegal S7 LOSS witness')
        known6 = reverse(geom, known7)
        legal6 = SOURCE.children(geom, S5)
        missing6 = legal6 - known6
        need(len(known6) == 110 and len(legal6) == 32 and
             len(missing6) == 27, 'S5 proof-only baseline changed')
        coverage = {s6: SOURCE.children(geom, s6) & plan
                    for s6 in missing6}
        need(all(coverage.values()), 'revised plan leaves S6 uncovered')
        boundaries = []
        for p in plan:
            need(p.bit_count() == 7 and geom.safe(p) and
                 geom.canonical(p) == p, 'invalid proposed S7 root')
            cs = SOURCE.children(geom, p)
            need(not (cs & frozen_loss) and ROOT not in cs,
                 'proposed S7 WIN root has known S8 LOSS child')
            boundaries.append(cs)
        edges = sum(map(len, boundaries))
        distinct = len(set().union(*boundaries))
        need(edges == 554 and distinct == 553,
             'revised S7->S8 obligations changed')
        audits.append((sorted(missing6), sorted(loss7), edges, distinct))
    need(audits[0] == audits[1], '3x3/4x4 replan mismatch')
    return {'new_s7_loss_parents': 8, 'invalidated_old_s7_plan_roots': 1,
            'replacement_s7': f'{REPLACEMENT:032x}',
            'conditional_s7_plan_roots': 14,
            'conditional_s7_to_s8_edges': 554,
            'conditional_distinct_s8': 553,
            's5_uncovered_s6': 27, 'new_s6_win_from_s7_loss': 0,
            'new_s5_verdicts': 0, 'new_two_stone_closures': 0}


def verify(negative=False, optimality=True):
    rows, weights = read_certificate()
    selected, by_leaf = boundary(rows, weights)
    if negative:
        tests = [
            (rows[:-1], weights),
            ([rows[0]] + rows[:-1], weights),
            ([(rows[0][0], rows[0][0], rows[0][2])] + rows[1:], weights),
            ([(rows[0][0], rows[0][1], rows[0][2] + 1)] + rows[1:], weights),
            (rows, [0] + weights[1:]),
        ]
        for changed_rows, changed_weights in tests:
            try:
                boundary(changed_rows, changed_weights)
            except ValueError:
                continue
            raise ValueError('tampered S8 LOSS certificate accepted')
    result = terminal(selected, by_leaf, weights, optimality)
    plan = read_keys(HERE / 's7-plan14-revised.keys')
    plan_result = plan_audit(plan)
    if negative:
        for changed in (plan - {REPLACEMENT},
                        (plan - {REPLACEMENT}) | {BAD7}):
            try:
                plan_audit(changed)
            except ValueError:
                continue
            raise ValueError('tampered 14-root plan accepted')
    print({'s8_loss': f'{ROOT:032x}', 's9_obligations': 16,
           **result, **plan_result, 'empty_board': 'UNKNOWN'})
    if negative:
        print('PASS seven certificate/plan mutation rejections')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--negative', action='store_true')
    ap.add_argument('--no-optimality', action='store_true')
    args = ap.parse_args()
    verify(args.negative, not args.no_optimality)

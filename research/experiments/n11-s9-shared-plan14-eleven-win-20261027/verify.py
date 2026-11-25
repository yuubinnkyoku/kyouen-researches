#!/usr/bin/env python3
"""Independent full-terminal recheck of eleven 11x11 nine-stone WIN witnesses."""
import copy
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'n11-s9-shared-plan14-20261027' / 'verify.py'
spec = importlib.util.spec_from_file_location('n11_shared9_geometry', OLD)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

def need(ok, msg):
    if not ok:
        raise ValueError(msg)

def verify(cert, negative=False):
    need(cert.get('format') == 'n11-s9-shared-plan14-eleven-win-v1'
         and cert.get('board') == 11
         and cert.get('perspective') == 'original-first-player'
         and cert.get('empty_board') == 'UNKNOWN', 'invalid header')
    rows = cert.get('witnesses')
    need(isinstance(rows, list) and len(rows) == 11, 'expected 11 roots')
    roots = base.keys([r['s9_win'] for r in rows], 9)
    plan = base.keys((HERE.parent / 'n11-s5-pair-cover-20261026'
                      / 's7-plan14-remaining.keys').read_text().split(), 7)
    need(len(plan) == 14, 'changed plan')
    outputs = []
    for det in (base.det3, base.det4):
        safe, children, terminal = base.solver(det)
        plan8 = set().union(*(children(p) for p in plan))
        union8, hit8 = set(), set()
        total_leaves = total_states = 0
        for root, row in zip(roots, rows):
            need(safe(root) and base.canonical(root) == root,
                 'unsafe/noncanonical nine-stone root')
            leaves = set(base.keys(row['s10_win_children'], 10))
            need(leaves == children(root), 'incomplete universal S10 boundary')
            all8 = {base.canonical(root ^ (1 << p))
                    for p in base.points(root)}
            listed = set(base.keys(row['s8_all_parents'], 8))
            selected = set(base.keys(row['s8_plan_parents'], 8))
            need(len(all8) == 9 and listed == all8
                 and selected == all8 & plan8
                 and len(selected) in (3, 4), 'incorrect reverse S8 boundary')
            for parent in all8:
                need(safe(parent) and root in children(parent),
                     'invalid reverse-parent witness')
            subtotal = 0
            for leaf in sorted(leaves):
                need(safe(leaf) and base.canonical(leaf) == leaf,
                     'unsafe/noncanonical S10 leaf')
                result, states = terminal(leaf)
                need(result, 'false S10 WIN terminal leaf')
                subtotal += states
            need(subtotal == row['terminal_states'],
                 'S10 terminal state count mismatch')
            total_leaves += len(leaves)
            total_states += subtotal
            union8.update(all8)
            hit8.update(selected)
        need(total_leaves == 225 and total_states == 24952,
             'terminal count regression')
        need(len(union8) == 96 and len(hit8) == 38,
             'reverse proof union regression')
        outputs.append((total_leaves, total_states, len(union8), len(hit8)))
    need(outputs[0] == outputs[1], 'independent geometries disagree')
    if negative:
        def reject(modify):
            altered = copy.deepcopy(cert)
            modify(altered)
            try:
                verify(altered)
            except (ValueError, KeyError, TypeError, AssertionError):
                return
            raise AssertionError('modified certificate accepted')
        reject(lambda c: c['witnesses'][0]['s10_win_children'].pop())
        reject(lambda c: c['witnesses'][0]['s8_plan_parents'].pop())
        reject(lambda c: c['witnesses'][0].__setitem__('terminal_states', 0))
        reject(lambda c: c['witnesses'][0].__setitem__(
            's9_win', c['witnesses'][1]['s9_win']))
        reject(lambda c: c.__setitem__('empty_board', 'WIN'))
    return {'independent_geometries': 2, 's9_win_witnesses': 11,
            's10_win_leaves': 225, 'terminal_states_per_geometry': 24952,
            'derived_s8_win_classes': 96, 'plan_s8_touched': 38,
            'new_s7_verdicts': 0, 'new_s5_verdicts': 0,
            'empty_board': 'UNKNOWN'}

if __name__ == '__main__':
    print(json.dumps(verify(json.loads((HERE / 'certificate.json').read_text()),
                            negative='--negative' in sys.argv), sort_keys=True))

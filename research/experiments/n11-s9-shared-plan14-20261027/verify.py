#!/usr/bin/env python3
"""Five N11 S9 WIN certificates, independently re-solved to terminal.

All S10 leaves are re-evaluated from empty memo tables by both the 3x3
difference determinant and independent 4x4 Bareiss integer determinant.
Neither existing verdict cache nor pn/dn values are used as proof leaves.
"""
import copy
import json
import sys
from functools import lru_cache
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
XY = [(i % 11, i // 11) for i in range(121)]

def det3(p):
    a, b, c, d = p
    x, y = XY[d]
    rows = [(XY[i][0]-x, XY[i][1]-y,
             XY[i][0]**2+XY[i][1]**2-x*x-y*y) for i in (a, b, c)]
    (u,v,w), (r,s,t), (f,g,h) = rows
    return u*(s*h-t*g)-v*(r*h-t*f)+w*(r*g-s*f)


def det4(p):
    m = [[XY[i][0], XY[i][1], XY[i][0]**2+XY[i][1]**2, 1] for i in p]
    sign, prev = 1, 1
    for k in range(3):
        if m[k][k] == 0:
            for j in range(k+1, 4):
                if m[j][k]:
                    m[k], m[j] = m[j], m[k]
                    sign = -sign
                    break
            else:
                return 0
        pivot = m[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                numerator = m[i][j]*pivot-m[i][k]*m[k][j]
                assert numerator % prev == 0
                m[i][j] = numerator//prev
        for i in range(k+1, 4):
            m[i][k] = 0
        prev = pivot
    return sign*m[3][3]


def points(b):
    return tuple(i for i in range(121) if b>>i&1)


def canonical(b):
    result = None
    for k in range(8):
        out = 0
        for p in points(b):
            x,y=XY[p]
            q=((x,y),(10-y,x),(10-x,10-y),(y,10-x),
               (10-x,y),(10-y,10-x),(x,10-y),(y,x))[k]
            out |= 1 << (q[0]+11*q[1])
        if result is None or out < result:
            result=out
    return result


def solver(det):
    @lru_cache(maxsize=None)
    def bad(q):
        return det(q) == 0
    @lru_cache(maxsize=None)
    def legal(b):
        pp = points(b)
        triples = tuple(combinations(pp, 3))
        return tuple(i for i in range(121) if not (b>>i)&1
                     and all(not bad(tuple(sorted(t+(i,)))) for t in triples))
    def safe(b):
        return all(not bad(q) for q in combinations(points(b), 4))
    def children(b):
        return {canonical(b|(1<<p)) for p in legal(b)}
    def terminal(b):
        @lru_cache(maxsize=None)
        def win(board):
            for p in legal(board):
                if not win(board|(1<<p)):
                    return True
            return False
        result=win(b)
        return result,win.cache_info().currsize
    return safe,children,terminal



def need(condition, message):
    if not condition:
        raise ValueError(message)


def keys(values, stones):
    need(isinstance(values, list) and all(isinstance(x, str) and
         len(x) == 32 and set(x) <= set('0123456789abcdef') and
         int(x, 16).bit_count() == stones for x in values),
         'invalid position key')
    need(values == sorted(set(values)), 'duplicate or unordered keys')
    return [int(x, 16) for x in values]


def verify(cert, negative=False):
    need(cert.get('format') == 'n11-s9-shared-plan14-win-v1' and
         cert.get('board') == 11 and
         cert.get('perspective') == 'original-first-player' and
         cert.get('empty_board') == 'UNKNOWN', 'certificate header changed')
    rows = cert.get('witnesses')
    need(isinstance(rows, list) and len(rows) == 5,
         'expected five S9 WIN witnesses')
    witnesses = keys([r['s9_win'] for r in rows], 9)
    plan_path = HERE.parent / 'n11-s5-pair-cover-20261026' / 's7-plan14-remaining.keys'
    plan = keys(plan_path.read_text('ascii').split(), 7)
    need(len(plan) == 14, '14-root plan changed')
    results = []
    for det in (det3, det4):
        safe, children, terminal = solver(det)
        plan_edges = {p: children(p) for p in plan}
        plan8 = set().union(*plan_edges.values())
        secured8, derived8 = set(), set()
        total_states = total_leaves = 0
        for root, row in zip(witnesses, rows):
            need(safe(root) and canonical(root) == root,
                 'unsafe or noncanonical S9 witness')
            leaves = keys(row['s10_win_children'], 10)
            need(set(leaves) == children(root),
                 'incomplete S9 -> S10 universal boundary')
            all8 = {canonical(root ^ (1 << p)) for p in points(root)}
            listed8 = set(keys(row['s8_all_parents'], 8))
            selected = set(keys(row['s8_plan_parents'], 8))
            need(len(all8) == 9 and all8 == listed8 and
                 len(selected) == 4 and selected == all8 & plan8,
                 'missing or extraneous S8 parent')
            need(not (secured8 & selected) and not (derived8 & all8),
                 'duplicate S8 parent across S9 witnesses')
            for parent in all8:
                need(safe(parent) and root in children(parent),
                     'invalid S8 -> S9 legal witness')
            counts = []
            for leaf in leaves:
                need(safe(leaf) and canonical(leaf) == leaf,
                     'unsafe or noncanonical S10 leaf')
                verdict, states = terminal(leaf)
                need(verdict, 'false S10 WIN leaf')
                counts.append(states)
            need(sum(counts) == row['terminal_states'],
                 'terminal state count mismatch')
            total_states += sum(counts)
            total_leaves += len(leaves)
            secured8.update(selected)
            derived8.update(all8)
        secured_edges = sum(len(cs & secured8) for cs in plan_edges.values())
        need(len(derived8) == 45 and len(secured8) == 20 and
             secured_edges == 20 and total_leaves == 85 and
             total_states == 4269, 'joint proof coverage changed')
        results.append((total_states, total_leaves, secured_edges))
    need(results[0] == results[1], 'independent geometries disagree')
    if negative:
        def reject(modify):
            bad = copy.deepcopy(cert)
            modify(bad)
            try:
                verify(bad)
            except (ValueError, KeyError, TypeError, AssertionError):
                return
            raise AssertionError('modified certificate accepted')
        reject(lambda c: c['witnesses'][0]['s10_win_children'].pop())
        reject(lambda c: c['witnesses'][0]['s10_win_children'].__setitem__(
            0, c['witnesses'][0]['s10_win_children'][1]))
        reject(lambda c: c['witnesses'][0]['s8_plan_parents'].pop())
        reject(lambda c: c['witnesses'][0].__setitem__('terminal_states', 0))
        reject(lambda c: c['witnesses'][0].__setitem__(
            's9_win', c['witnesses'][1]['s9_win']))
    return {'s9_win_witnesses': 5, 's10_win_leaves': 85,
            'terminal_states_per_geometry': results[0][0],
            's8_win_derived': 45, 's8_plan_classes': 20,
            's7_to_s8_plan_edges': results[0][2],
            'new_s7_verdicts': 0, 'new_s5_verdicts': 0,
            'empty_board': 'UNKNOWN'}


if __name__ == '__main__':
    print(json.dumps(verify(json.loads(
        (HERE / 'certificate.json').read_text('utf-8')),
        negative='--negative' in sys.argv), sort_keys=True))

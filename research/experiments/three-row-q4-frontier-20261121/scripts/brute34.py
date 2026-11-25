#!/usr/bin/env python3
"""Exhaustive classifier of maximal safe sets on w x m q=4 boards (small m).
Independent third system (geometry: K0318 curve_key lift via pycensus helpers).
Enumerates ALL safe sets by pruned DFS (adding points in index order, pruning when
any forbidden curve reaches q stones), then classifies each as maximal/deficient.
Outputs: counts of maximal sets by stone count, row profiles of maximal sets,
deficiency summary, and the exact witness-band truth (P(m) = no deficient maximal)."""
import sys
import importlib.util
import itertools
import os
import json

CP_CANDIDATES = [
    '/home/user/work/curve_packing_fixed_width.py',
    os.path.expanduser('~/knowledge/kyouen-research/q34-lane-kit/curve_packing_fixed_width.py'),
]


def load_cp():
    for c in CP_CANDIDATES:
        if os.path.exists(c):
            spec = importlib.util.spec_from_file_location('cp', c)
            cp = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cp)
            return cp
    raise SystemExit('curve_packing not found')


cp = load_cp()

w, m, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
points = [(x, y) for y in range(w) for x in range(m)]
n = len(points)
keys = set()
for tri in itertools.combinations(points, 3):
    keys.add(cp.curve_key(tri))
curves = []  # (mask, list of member indices, row_number or None)
for k in keys:
    idxs = [i for i, p in enumerate(points) if cp.on_curve(k, p)]
    if len(idxs) >= q:
        curves.append(idxs)
rows_of = [p[1] for p in points]

# per-point: curves containing the point
cover = [[] for _ in range(n)]
for ci, idxs in enumerate(curves):
    for i in idxs:
        cover[i].append(ci)

count_curves = [0] * len(curves)
maximal_by_size = {}
maximal_rows = {}
deficient_count = 0
deficient_min_size = None
witness = None
sets_safe = 0

# DFS over points in index order
sel = []


def dfs(start):
    global sets_safe, deficient_count, deficient_min_size, witness
    sets_safe += 1
    # classify current safe set
    maximal = True
    for i in range(n):
        if i in sel_set:
            continue
        cov = False
        for ci in cover[i]:
            if count_curves[ci] >= q - 1:
                cov = True
                break
        if not cov:
            maximal = False
            break
    if maximal:
        sz = len(sel)
        maximal_by_size[sz] = maximal_by_size.get(sz, 0) + 1
        rcnt = [0] * w
        for i in sel:
            rcnt[rows_of[i]] += 1
        key = tuple(rcnt)
        maximal_rows[key] = maximal_rows.get(key, 0) + 1
        if min(rcnt) <= q - 2:
            deficient_count += 1
            if deficient_min_size is None or sz < deficient_min_size:
                deficient_min_size = sz
                witness = sorted(points[i] for i in sel)
    for i in range(start, n):
        # adding point i keeps safety?
        ok = True
        for ci in cover[i]:
            if count_curves[ci] == q - 1:
                ok = False
                break
        if not ok:
            continue
        for ci in cover[i]:
            count_curves[ci] += 1
        sel.append(i)
        sel_set.add(i)
        dfs(i + 1)
        sel.pop()
        sel_set.remove(i)
        for ci in cover[i]:
            count_curves[ci] -= 1


sel_set = set()
dfs(0)

print(json.dumps({
    'w': w, 'm': m, 'q': q, 'curves': len(curves), 'safe_sets': sets_safe,
    'maximal_by_size': {str(k): v for k, v in sorted(maximal_by_size.items())},
    'maximal_row_profiles': {str(k): v for k, v in sorted(maximal_rows.items())},
    'deficient_maximal': deficient_count,
    'min_deficient_size': deficient_min_size,
    'witness': witness,
    'P_m_true': deficient_count == 0,
}))

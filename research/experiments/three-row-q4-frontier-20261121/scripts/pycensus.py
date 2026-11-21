#!/usr/bin/env python3
"""Independent forbidden-curve census for w x m q-point boards (lattice circles+lines),
built ONLY from K0318's curve_packing_fixed_width.py geometry helpers (curve_key lift
covers both circles and lines: collinear triples give A=0). System #2 for cross-validation.
Dumps canonical text identical in format to census_dump.js output."""
import sys
import importlib.util
import itertools

CP_PATH = '/home/user/work/curve_packing_fixed_width.py'  # K0318 verbatim, re-fetch on reset


def load_cp():
    import os
    for cand in [CP_PATH, os.path.expanduser('~/knowledge/kyouen-research/q34-lane-kit/curve_packing_fixed_width.py')]:
        if os.path.exists(cand):
            spec = importlib.util.spec_from_file_location('cp', cand)
            cp = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cp)
            return cp
    raise SystemExit('curve_packing_fixed_width.py not found; re-fetch from repo commit 49891aaf')


cp = load_cp()


def dump(w, m, q):
    points = [(x, y) for y in range(w) for x in range(m)]
    keys = {}
    for tri in itertools.combinations(points, 3):
        if len(set(tri)) < 3:
            continue
        k = cp.curve_key(tri)
        keys[k] = 1
    rows = []
    for k in keys:
        pts = [f"{x},{y}" for (x, y) in points if cp.on_curve(k, (x, y))]
        if len(pts) < q:
            continue
        typ = 'circle' if k[0] != 0 else 'line'
        # curve_key returns (A,B,C,D) primitive; lines have A=0 with (B,C,D).
        co = k if k[0] != 0 else k[1:]
        rows.append(typ + '|' + '/'.join(map(str, co)) + '|' + ';'.join(sorted(pts)))
    rows.sort()
    return rows


w, m, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rows = dump(w, m, q)
with open(sys.argv[4], 'w') as f:
    f.write('\n'.join(rows) + '\n')
print(f'{{"w": {w}, "m": {m}, "q": {q}, "curves": {len(rows)}}}')

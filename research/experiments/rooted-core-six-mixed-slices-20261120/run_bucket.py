#!/usr/bin/env python3
"""Run/certify one mixed bucket j (six-vertex cores, exactly j triples).

Resume-capable: progress stored in bucket_j{N}_prog.json (per-state prefix +
last_fail). Repeat invocations until it prints FINAL. Time-guarded.

Certification rule (K0682 window theorem): with N = max(500, last_fail+1)
and T = 34, if f(n+34)==f(n) holds for every state over the comparison
window N..2N+T+1 (values needed through 2N+2T+1), then it holds for all
n >= N. The run computes needed = 2N+69, certifies the window, and records
each type's prefix, joint start, minimal tail period and a raw subset-game
sample audit."""
import ast
import json
import os
import sys
import time
from collections import Counter

import mixedlib as M

LIMIT0 = 1069
MINLIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else 0
MAXNEEDED = 2600

j = int(sys.argv[1])
budget = float(sys.argv[2]) if len(sys.argv) > 2 else 240.0
T0 = time.time()


def _load_keys(d):
    return {(kk[0], tuple(kk[1])): v for kk, v in
            ((ast.literal_eval(s), v) for s, v in d.items())}


types, labeled, reps = M.bucket_types(j)
print(f'bucket j={j}: labeled {labeled}, reps {reps}, types {len(types)}', flush=True)
known = M.load_base()
prog_path = f'bucket_j{j}_prog.json'
prog = {}
if os.path.exists(prog_path):
    prog = _load_keys(json.load(open(prog_path))['states'])

todo = [s for s in types if (s not in prog) or (MINLIMIT and len(prog[s][0]) <= MINLIMIT)]
print('todo', len(todo), 'progress', len(prog), flush=True)
if todo:
    limit = max(LIMIT0, MINLIMIT)
    path = M.path_table(limit)
    for i, s in enumerate(todo):
        if time.time() - T0 > budget:
            print('TIME GUARD: stopping with', i, 'states done this invocation', flush=True)
            break
        seq, lf = M.solve_state(s, limit, known, path)
        prog[s] = [seq, lf]
        if i % 200 == 199:
            with open(prog_path + '.tmp', 'w') as fh:
                json.dump({'states': {str(list(k)): v for k, v in prog.items()}}, fh)
            os.replace(prog_path + '.tmp', prog_path)
    with open(prog_path + '.tmp', 'w') as fh:
        json.dump({'states': {str(list(k)): v for k, v in prog.items()}}, fh)
    os.replace(prog_path + '.tmp', prog_path)
    print('progress saved:', len(prog), '/', len(types), flush=True)

if len(prog) < len(types):
    print('NOT FINISHED, rerun to continue', flush=True)
    sys.exit(0)

values = {s: prog[s][0] for s in types}
last_fail0 = {s: prog[s][1] for s in types}
worst = max(last_fail0.values())
start = max(500, worst + 1)
needed = 2 * start + 69
print('worst last_fail', worst, 'start', start, 'needed', needed,
      'elapsed', round(time.time() - T0, 1), flush=True)

ext_condition = needed > LIMIT0 and needed <= MAXNEEDED
if ext_condition:
    ext = f'bucket_j{j}_ext.json'
    # prefixes already solved at >= needed can be reused directly
    extp = {s: prog[s][0] for s in types if len(prog[s][0]) > needed}
    if os.path.exists(ext):
        extp = {**extp, **_load_keys(json.load(open(ext)))}
    todo = [s for s in types if s not in extp or len(extp[s]) <= needed]
    pfull = M.path_table(needed)
    for i, s in enumerate(todo):
        if time.time() - T0 > budget:
            print('EXT TIME GUARD', flush=True)
            with open(ext + '.tmp', 'w') as fh:
                json.dump({str(list(k)): v for k, v in extp.items()}, fh)
            os.replace(ext + '.tmp', ext)
            sys.exit(0)
        seq, _ = M.solve_state(s, needed, known, pfull)
        extp[s] = seq
        if i % 100 == 99:
            with open(ext + '.tmp', 'w') as fh:
                json.dump({str(list(k)): v for k, v in extp.items()}, fh)
            os.replace(ext + '.tmp', ext)
    with open(ext + '.tmp', 'w') as fh:
        json.dump({str(list(k)): v for k, v in extp.items()}, fh)
    os.replace(ext + '.tmp', ext)
    if len(extp) < len(types):
        print('EXT NOT FINISHED, rerun to continue', flush=True)
        sys.exit(0)
    values = {s: extp[s] for s in types}
    last_fail = {}
    for s in types:
        seq = values[s]
        lf = -1
        for L in range(34, needed + 1):
            if seq[L] != seq[L - 34]:
                lf = L - 34
        last_fail[s] = lf
    worst2 = max(last_fail.values())
    if worst2 + 1 != start:
        assert worst2 + 1 <= start, 'extension found later failures; investigate!'
        start = max(500, worst2 + 1)
        needed = 2 * start + 69
        print('RECOMPUTED start', start, 'needed', needed, flush=True)
else:
    last_fail = last_fail0

pathfull = M.path_table(needed)
ok = all(pathfull[i] == pathfull[i + 34] for i in range(start, 2 * start + 36))
ok = ok and all(values[s][i] == values[s][i + 34]
                for s in types for i in range(start, 2 * start + 36))
print('window check:', ok, flush=True)
assert ok, 'window NOT certified — investigate (possible counterexample!)'


def min_tail_period(seq, tail):
    t_seq = seq[len(seq) - tail:]
    for t in range(1, 35):
        if all(t_seq[k] == t_seq[k + t] for k in range(len(t_seq) - t)):
            return t
    return None


minperiods = Counter(min_tail_period(values[s], 400) for s in types)
by_edges = {}
for s in types:
    by_edges.setdefault(len(s[1]), []).append(s)
sample = []
for e in sorted(by_edges):
    g = sorted(by_edges[e])
    step = max(1, len(g) // 6)
    sample += g[::step][:6]
checks = total = 0
for s in sample:
    for length in range(7):
        g, count = M.direct(s, length)
        assert g == values[s][length], (s, length)
        checks += 1
        total += count
print('direct checks', checks, 'safe', total, flush=True)
hist = Counter(last_fail[s] + 1 for s in types)
out = dict(j=j, labeled=labeled, burnside_reps=reps, types=len(types),
           joint_start=start, needed=needed, certified=True,
           max_grundy=max(max(v[:needed + 1]) for v in values.values()),
           min_tail_period_histogram={str(k): v for k, v in minperiods.items()},
           worst_starts=sorted([(last_fail[s] + 1, list(s)) for s in types], reverse=True)[:8],
           direct_checks=checks, direct_safe_states=total, direct_types=len(sample),
           start_histogram={str(k): v for k, v in sorted(hist.items())})
json.dump(out, open(f'bucket_j{j}_head.json', 'w'))
pair_path = f'bucket_j{j}_records.jsonl'
with open(pair_path, 'w') as fh:
    for s in types:
        fh.write(json.dumps(dict(n=s[0], forbidden=list(s[1]),
                                 prefix_start=last_fail[s] + 1,
                                 prefix=values[s][:needed + 1])) + '
')
print(json.dumps(out)[:1400])
print('FINAL j=' + str(j), 'elapsed', round(time.time() - T0, 1), 's', flush=True)

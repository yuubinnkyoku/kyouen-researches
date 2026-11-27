#!/usr/bin/env python3
"""Joint adaptive solver for the complete 6-vertex pure-two-edge (graph) core family.

Family: every clutter on vertices {0..5} whose edges are all 2-point (i.e. every
simple graph on 6 rooted vertices, root 0 = path attachment). 2^15 = 32768 raw
inputs, 544 rooted canonical types (Burnside-confirmed). Structure-adapted from
rooted-core-seven-pure-triple-five-edges-20261125/solve_core.py (K0684 lineage):
reuse of the K0682 certified <=5-vertex table (period-34 block extension from
500), exact rooted-clutter + path recurrence via the pinned engine
(rooted-core-tail-periodicity-20261107/engine.py, byte-clone usage), and the
K0682 finite-window certification rule
(N = max(500, last_failure+1), T = 34, needed = 2N + 2T + 1 = 2N + 69).
Standard library only. Deterministic (no RNG).
"""
from functools import lru_cache
from itertools import combinations, permutations
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import canonical, closure, delete_root, mex, ordinary, play


def graph_initial_types(n=6):
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
    reps = set()
    for mask in range(1 << len(pairs)):
        edges = tuple(sorted(1 << a | 1 << b
                             for i, (a, b) in enumerate(pairs) if mask >> i & 1))
        reps.add(canonical(n, edges))
    return sorted(reps), 1 << len(pairs)


def load_known():
    base_path = ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107/output/audit.json'
    base = json.loads(base_path.read_text(encoding='utf-8'))
    return {(row['n'], tuple(row['forbidden'])): row['prefix'] for row in base['records']}


def solve(initial, maxlen, progress=None):
    known = load_known()
    states = closure(initial)
    new = sorted(set(states) - set(known))
    values = {state: list(prefix) for state, prefix in known.items()}
    values.update({state: [] for state in new})
    known_list = sorted(known)
    known_block = {state: known[state][500:534] for state in known_list}
    data = {}
    for state in new:
        after = ordinary(play(state, 0)[0])
        deleted = ordinary(delete_root(state))
        retained, detached = set(), set()
        for v in range(1, state[0]):
            child, alive = play(state, v)
            (retained if alive else detached).add(child if alive else ordinary(child))
        data[state] = after, deleted, retained, detached
    last_fail = {state: -1 for state in new}
    path = []
    start = needed = None
    certified = False
    for length in range(0, maxlen + 1):
        path.append(mex({path[max(j - 1, 0)] ^ path[max(length - j - 2, 0)]
                         for j in range(length)}))
        for state in known_list:
            seq = values[state]
            if len(seq) <= length:
                seq.append(known_block[state][(length - 500) % 34])
        for state in new:
            after, deleted, retained, detached = data[state]
            seq = values[state]
            options = {after ^ path[max(length - 1, 0)]}
            options.update(values[child][length] for child in retained)
            options.update(g ^ path[length] for g in detached)
            if length:
                options.add(deleted ^ path[max(length - 2, 0)])
            if length >= 2:
                options.add(seq[length - 2])
                options.update(seq[i] ^ path[length - 3 - i] for i in range(length - 2))
            seq.append(mex(options))
            if length >= 34 and seq[length] != seq[length - 34]:
                last_fail[state] = length - 34
        if length >= 534:
            start = max(500, max(last_fail.values()) + 1)
            needed = 2 * start + 69
            if length >= needed:
                ok = all(path[i] == path[i + 34] for i in range(start, 2 * start + 36))
                ok = ok and all(values[state][i] == values[state][i + 34]
                                for state in new for i in range(start, 2 * start + 36))
                if ok:
                    certified = True
                    if progress:
                        progress('CERTIFIED', length, dict(start=start, needed=needed))
                    break
        if length % 100 == 0 and progress:
            progress('length', length, dict(maxnew=max(values[s][-1] for s in new),
                                            start=start, needed=needed))
    return dict(states=states, new=new, values=values, known=known_list,
                path=path, start=start, needed=needed, certified=certified,
                last_fail=last_fail, initial=initial)


def emit_records(result, out_path, raw):
    new = result['new']
    needed = result['needed']
    head = dict(audit='PASS',
                family='six-vertex complete pure-two-edge (graph) core family',
                vertices=6, raw_inputs=raw,
                distinct_initial_types=len(result['initial']),
                closure_states=len(result['states']),
                new_closure_states=len(new),
                known_closure_states=len(result['states']) - len(new),
                joint_start_candidate=result['start'],
                values_needed_through=result['needed'],
                jointly_certified=result['certified'],
                maximum_grundy_in_prefix=max(max(result['values'][s][:needed + 1]) for s in new),
                worst_prefix_starts=sorted([(result['last_fail'][s] + 1,
                                             [s[0], list(s[1])]) for s in new],
                                           reverse=True)[:15])
    records = [dict(n=s[0], forbidden=list(s[1]), prefix_start=result['last_fail'][s] + 1,
                    prefix=result['values'][s][:needed + 1]) for s in new]
    text = json.dumps(head, indent=2)
    text = text[:-2] + ',\n  "records": [\n' + ',\n'.join(
        '    ' + json.dumps(row, separators=(',', ':')) for row in records) + '\n  ]\n}\n'
    json.loads(text)
    out_path.write_text(text, encoding='utf-8')
    return head


if __name__ == '__main__':
    t0 = time.time()
    initial, raw = graph_initial_types(6)
    print('initial types', len(initial), 'raw', raw, flush=True)
    result = solve(initial, 4000, progress=lambda tag, v, d: print(tag, v, d,
                                                                    't=%.1f' % (time.time() - t0), flush=True))
    head = emit_records(result, HERE / 'output' / 'audit.json', raw)
    print(json.dumps({k: head[k] for k in head if k != 'worst_prefix_starts'}, indent=2), flush=True)
    print('worst15', head['worst_prefix_starts'][:5], flush=True)
    print('elapsed %.1fs' % (time.time() - t0))

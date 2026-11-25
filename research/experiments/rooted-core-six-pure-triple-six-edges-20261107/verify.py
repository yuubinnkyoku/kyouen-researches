#!/usr/bin/env python3
"""Complete six-vertex pure-three-edge clutter family (<=6 edges) for K0684.

Extends rooted-core-larger-periods-20261107 (which covered <=3 edges, 1351 raw
inputs / 100 rooted types) to ALL six-vertex 3-uniform clutters with at most six
edges: sum_{k=0}^{6} C(20,k) = 60460 raw inputs. Up to rooted isomorphism this is
732 types; the root-retaining closure adds only <=5-vertex states (already certified
by K0682), so exactly 732 new six-vertex states are solved here.

The <=5 certified table is reused verbatim (full-length proved values, not prefix
extrapolation). New states are computed by the exact rooted-clutter + path recurrence
and certified by the K0682 finite-window theorem (N=500, T=34). Independent raw
subset-mex checks (length 0..6, every type) validate the recurrence at the base.

This is a complete finite family, NOT a proof of the unbounded-core conjecture K0684.
"""
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import canonical, closure, delete_root, last_period_failure, mex, ordinary, path_values, play


def inputs():
    triples = [sum(1 << i for i in edge) for edge in combinations(range(6), 3)]
    return [(6, tuple(sorted(group)))
            for size in range(7) for group in combinations(triples, size)]


def solve_seeded(initial, limit):
    base_path = ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107/output/audit.json'
    base = json.loads(base_path.read_text(encoding='utf-8'))
    known = {(row['n'], tuple(row['forbidden'])): row['prefix'] for row in base['records']}
    initial = sorted({canonical(n, tuple(sorted(edges))) for n, edges in initial})
    states = closure(initial)
    new = [state for state in states if state not in known]
    path = path_values(limit + 1)
    values = {state: [prefix[i] if i < len(prefix) else prefix[500 + (i - 500) % 34]
                      for i in range(limit + 1)] for state, prefix in known.items()}
    values.update({state: [] for state in new})
    data = {}
    for state in new:
        after = ordinary(play(state, 0)[0])
        deleted = ordinary(delete_root(state))
        retained, detached = set(), set()
        for v in range(1, state[0]):
            child, alive = play(state, v)
            (retained if alive else detached).add(child if alive else ordinary(child))
        data[state] = after, deleted, retained, detached
    print('initial types', len(initial), 'new closure states', len(new), flush=True)
    for length in range(limit + 1):
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
        if length % 200 == 0:
            print('length', length, 'current maximum',
                  max(values[state][-1] for state in new), flush=True)
    return initial, states, new, values, path


def direct(state, length):
    n, forbidden = state
    edges = list(forbidden)
    if length:
        edges += [1 | (1 << n)] + [(1 << v) | (1 << (v + 1)) for v in range(n, n + length - 1)]

    @lru_cache(None)
    def game(s):
        return mex({game(s | (1 << v)) for v in range(n + length)
                    if not s >> v & 1 and not any((s | (1 << v)) & edge == edge for edge in edges)})
    value = game(0)
    return value, game.cache_info().currsize


def main():
    cases = inputs()
    limit = 1400
    initial, states, new, values, path = solve_seeded(cases, limit)
    starts = {state: last_period_failure(values[state], 34) + 1 for state in new}
    start = max(500, *starts.values())
    needed = 2 * start + 69
    certified = needed <= limit
    if certified:
        assert all(path[i] == path[i + 34] for i in range(start, 2 * start + 36))
        assert all(values[state][i] == values[state][i + 34]
                   for state in new for i in range(start, 2 * start + 36))
    checks = total = 0
    for state in initial:
        for length in range(7):
            g, count = direct(state, length)
            assert g == values[state][length], (state, length, g, values[state][length])
            checks += 1
            total += count
    output = dict(audit='PASS',
                  family='all six-vertex pure-three-edge clutters with at most six edges',
                  raw_inputs=len(cases),
                  distinct_initial_types=len(initial), new_closure_states=len(new),
                  prefix_through=limit, joint_start_candidate=start,
                  values_needed_through=needed, jointly_certified=certified,
                  maximum_grundy_in_prefix=max(max(values[state]) for state in initial),
                  direct_subset_checks=checks, direct_safe_states=total,
                  worst_prefix_starts=sorted([(n, state) for state, n in starts.items()], reverse=True)[:15],
                  records=[dict(n=state[0], forbidden=state[1], prefix_start=starts[state],
                                prefix=values[state][:needed + 1 if certified else limit + 1]) for state in new])
    head = {key: value for key, value in output.items() if key != 'records'}
    text = json.dumps(head, indent=2)
    text = text[:-2] + ',\n  "records": [\n' + ',\n'.join('    ' + json.dumps(row, separators=(',', ':')) for row in output['records']) + '\n  ]\n}\n'
    json.loads(text)
    target = Path(__file__).with_name('output') / 'audit.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(text, encoding='utf-8')
    print(json.dumps(head, indent=2), flush=True)


if __name__ == '__main__':
    main()
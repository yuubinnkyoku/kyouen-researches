#!/usr/bin/env python3
"""Bounded larger-core challenge to K0684, seeded by the certified <=5 table."""
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import canonical, closure, delete_root, last_period_failure, mex, ordinary, path_values, play


def inputs():
    triples = [sum(1 << i for i in edge) for edge in combinations(range(6), 3)]
    cases = [(6, tuple(group)) for size in range(4) for group in combinations(triples, size)]
    # All pure-three-edge six-vertex clutters with at most three edges are above.
    pairs = [sum(1 << i for i in edge) for edge in combinations(range(6), 2)]
    rng = random.Random(20261107)
    for _ in range(64):
        chosen = [edge for edge in pairs if rng.randrange(5) == 0]
        allowed = [edge for edge in triples if not any(pair & edge == pair for pair in chosen)]
        cases.append((6, tuple(sorted(chosen + [edge for edge in allowed if rng.randrange(3) == 0]))))
    cases += [(6, tuple(triples)),
              (6, tuple(sum(1 << i for i in edge) for edge in [(0,1,2),(0,3,4),(1,3,5),(2,4,5)])),
              (7, tuple(sum(1 << i for i in edge) for edge in
                        [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]))]
    return cases


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
    print('initial types',len(initial),'new closure states',len(new),flush=True)
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
            print('length',length,'current maximum',max(values[state][-1] for state in new),flush=True)
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
    limit = 2200
    initial, states, new, values, path = solve_seeded(cases, limit)
    starts = {state: last_period_failure(values[state],34) + 1 for state in new}
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
            assert g == values[state][length]
            checks += 1
            total += count
    output = dict(audit='PASS', complete_pure_triple_six_vertex_up_to_three_edges=1351,
                  additional_seeded_and_structured_inputs=len(cases)-1351,
                  distinct_initial_types=len(initial), new_closure_states=len(new),
                  prefix_through=limit, joint_start_candidate=start,
                  values_needed_through=needed, jointly_certified=certified,
                  maximum_grundy_in_prefix=max(max(values[state]) for state in initial),
                  direct_subset_checks=checks, direct_safe_states=total,
                  worst_prefix_starts=sorted([(n, state) for state,n in starts.items()],reverse=True)[:15],
                  records=[dict(n=state[0],forbidden=state[1],prefix_start=starts[state],
                                prefix=values[state][:needed+1 if certified else limit+1]) for state in new])
    head = {key:value for key,value in output.items() if key!='records'}
    text=json.dumps(head,indent=2)
    text=text[:-2]+',\n  "records": [\n'+',\n'.join('    '+json.dumps(row,separators=(',',':')) for row in output['records'])+'\n  ]\n}\n'
    json.loads(text)
    target=Path(__file__).with_name('output')/'audit.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(text,encoding='utf-8')
    print(json.dumps(head,indent=2),flush=True)


if __name__=='__main__':
    main()

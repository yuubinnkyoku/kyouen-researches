#!/usr/bin/env python3
"""Complete six-vertex pure-three-edge family (ALL 2^20 subsets) for K0684.

Every 3-uniform family on six vertices is automatically a clutter (no edge can
contain another of equal size), so all 2^20 = 1048576 subsets of the 20 triples
are legal pure-three-edge cores. Up to rooted isomorphism (root 0 fixed, S5)
Burnside's lemma gives exactly 10688 types. This certifies the FULL six-vertex
pure-three-edge case, extending rooted-core-six-pure-triple-six-edges-20261107
(which covered the 732 types with at most six edges).

Method is identical to the validated <=6 experiment: reuse the K0682 certified
<=5-vertex table verbatim, solve the 10688 new six-vertex states by the exact
rooted-clutter + path recurrence, and certify via the K0682 finite-window theorem
(N=max(500,last_failure+1), T=34). The solver stops adaptively as soon as the
window is certified (needed = 2*N+69 values), since K0682 then guarantees all
longer lengths. Independent raw subset-mex checks on a stratified sample validate
the recurrence beyond the already-audited <=6 family.

This is a complete finite-family theorem, NOT the unbounded-core proof of K0684.
"""
from functools import lru_cache
from itertools import combinations, permutations
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import canonical, closure, delete_root, mex, ordinary, path_values, play

TRIPLES = list(combinations(range(6), 3))
IDX = {t: i for i, t in enumerate(TRIPLES)}
VMASK = [sum(1 << v for v in t) for t in TRIPLES]
PERMS = []
for _p in permutations(range(1, 6)):
    _vmap = (0,) + _p
    PERMS.append(tuple(IDX[tuple(sorted(_vmap[v] for v in t))] for t in TRIPLES))


def remap_mask(mask, tab):
    out = 0
    m = mask
    while m:
        b = m & -m
        out |= 1 << tab[b.bit_length() - 1]
        m ^= b
    return out


def orbit_representatives():
    # Ascending scan: the first unseen member of each orbit is its minimum.
    # Mark all 120 images so each orbit is represented exactly once.
    seen = bytearray(1 << 20)
    reps = []
    for mask in range(1 << 20):
        if seen[mask]:
            continue
        reps.append(mask)
        for tab in PERMS:
            seen[remap_mask(mask, tab)] = 1
    return reps


def initial_types():
    reps = orbit_representatives()
    types = set()
    for m in reps:
        forb = tuple(sorted(VMASK[i] for i in range(20) if m >> i & 1))
        types.add(canonical(6, forb))
    return sorted(types), len(reps)


def solve_adaptive(initial, maxlen):
    base_path = ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107/output/audit.json'
    base = json.loads(base_path.read_text(encoding='utf-8'))
    known = {(row['n'], tuple(row['forbidden'])): row['prefix'] for row in base['records']}
    states = closure(initial)
    new = [state for state in states if state not in known]
    values = {state: list(prefix) for state, prefix in known.items()}
    values.update({state: [] for state in new})
    known_list = list(known)
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
    print('initial types', len(initial), 'closure states', len(states),
          'new states', len(new), flush=True)
    ckpt = Path(__file__).with_name('_checkpoint.pkl')
    begin = 0
    if ckpt.exists():
        import pickle
        with ckpt.open('rb') as fh:
            saved = pickle.load(fh)
        if saved['new'] == new:
            begin = saved['length'] + 1
            path = saved['path']
            values = saved['values']
            last_fail = saved['last_fail']
            print('RESUME from length', begin, flush=True)
    start = needed = None
    certified = False
    for length in range(begin, maxlen + 1):
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
                    print('CERTIFIED at length', length, 'start', start,
                          'needed', needed, flush=True)
                    break
        if length % 100 == 0:
            print('length', length, 'max', max(values[state][-1] for state in new),
                  'joint start', start, 'needed', needed,
                  'elapsed', round(time.time() - T0, 1), flush=True)
            import pickle
            tmp = ckpt.with_suffix('.tmp')
            with tmp.open('wb') as fh:
                pickle.dump(dict(length=length, path=path, values=values,
                                 last_fail=last_fail, new=new), fh)
            tmp.replace(ckpt)
    return states, new, values, path, start, needed, certified, last_fail


def direct(state, length):
    n, forbidden = state
    edges = list(forbidden)
    if length:
        edges += [1 | (1 << n)] + [(1 << v) | (1 << (v + 1)) for v in range(n, n + length - 1)]

    @lru_cache(None)
    def game(s):
        return mex({game(s | (1 << v)) for v in range(n + length)
                    if not s >> v & 1 and not any((s | (1 << v)) & edge == edge for edge in edges)})
    return game(0), game.cache_info().currsize


T0 = time.time()


def main():
    import pickle
    cache = Path(__file__).with_name('_initial.pkl')
    if cache.exists():
        with cache.open('rb') as fh:
            initial, raw_orbits = pickle.load(fh)
    else:
        initial, raw_orbits = initial_types()
        with cache.open('wb') as fh:
            pickle.dump((initial, raw_orbits), fh)
    assert len(initial) == 10688, len(initial)
    states, new, values, path, start, needed, certified, last_fail = solve_adaptive(initial, 2200)
    assert certified, 'window not certified within maxlen'
    checks = total = 0
    rng = random.Random(20261108)
    # Stratified independent sample: all <=6-edge types are already audited in the
    # sibling experiment; here sample the >=7-edge types across edge counts.
    big = [s for s in initial if len(s[1]) >= 7]
    sample = rng.sample(big, min(400, len(big)))
    for state in sample:
        for length in range(7):
            g, count = direct(state, length)
            assert g == values[state][length], (state, length, g, values[state][length])
            checks += 1
            total += count
    output = dict(audit='PASS',
                  family='all six-vertex pure-three-edge clutters (full 2^20)',
                  raw_subsets=1 << 20, burnside_orbits=raw_orbits,
                  distinct_initial_types=len(initial), closure_states=len(states),
                  new_closure_states=len(new),
                  joint_start_candidate=start, values_needed_through=needed,
                  jointly_certified=certified,
                  maximum_grundy_in_prefix=max(max(values[state]) for state in initial),
                  direct_subset_checks=checks, direct_safe_states=total,
                  direct_sample_edge_count_min=7,
                  worst_prefix_starts=sorted([(last_fail[s] + 1, s) for s in new], reverse=True)[:15],
                  records=[dict(n=s[0], forbidden=s[1], prefix_start=last_fail[s] + 1,
                                prefix=values[s][:needed + 1]) for s in new])
    head = {k: v for k, v in output.items() if k != 'records'}
    text = json.dumps(head, indent=2)
    text = text[:-2] + ',\n  "records": [\n' + ',\n'.join(
        '    ' + json.dumps(row, separators=(',', ':')) for row in output['records']) + '\n  ]\n}\n'
    json.loads(text)
    target = Path(__file__).with_name('output') / 'audit.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(text, encoding='utf-8')
    ckpt = Path(__file__).with_name('_checkpoint.pkl')
    if ckpt.exists():
        ckpt.unlink()
    print(json.dumps(head, indent=2), flush=True)
    print('TOTAL elapsed', round(time.time() - T0, 1), 's', flush=True)


if __name__ == '__main__':
    main()
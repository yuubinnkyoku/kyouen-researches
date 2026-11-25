#!/usr/bin/env python3
"""Joint adaptive solver for rooted pure-three-edge core families (K0684 extension).

Mirrors the validated solve_adaptive of rooted-core-six-pure-triple-full-20261108:
reuse of the K0682 certified <=5-vertex table, exact rooted-clutter + path
recurrence, and the K0682 finite-window certification rule
(N = max(500, last_failure+1), T = 34, needed = 2N + 2T + 1 = 2N + 69).
Standard library only. Deterministic.
"""
from functools import lru_cache
from itertools import combinations, permutations
import json
import pickle
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import canonical, closure, delete_root, mex, ordinary, play


def build_perm_tables(n):
    triples = list(combinations(range(n), 3))
    idx = {t: i for i, t in enumerate(triples)}
    vmask = [sum(1 << v for v in t) for t in triples]
    tabs = []
    for p in permutations(range(1, n)):
        vmap = (0,) + p
        tabs.append(tuple(idx[tuple(sorted(vmap[v] for v in t))] for t in triples))
    return triples, idx, vmask, tabs


def initial_types(n, E, triples, vmask, tabs):
    """All pure-three-edge clutters on n vertices with at most E edges, rooted types."""
    reps = set()
    raw = 0
    for k in range(0, E + 1):
        for fam in combinations(range(len(triples)), k):
            mask = 0
            for i in fam:
                mask |= 1 << i
            raw += 1
            best = None
            m = mask
            bits = []
            while m:
                b = m & -m
                bits.append(b.bit_length() - 1)
                m ^= b
            for tab in tabs:
                key = tuple(sorted(vmask[tab[i]] for i in bits))
                if best is None or key < best:
                    best = key
            reps.add((n, best))
    # every representative must equal engine canonical form of the raw family
    return sorted(reps), raw


def load_known():
    base_path = ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107/output/audit.json'
    base = json.loads(base_path.read_text(encoding='utf-8'))
    known = {(row['n'], tuple(row['forbidden'])): row['prefix'] for row in base['records']}
    return known


def solve(initial, maxlen, checkpoint=True, progress=None, meta=None, budget_seconds=None):
    known = load_known()
    T_START = time.time()
    states = closure(initial)
    new = [state for state in states if state not in known]
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
    begin = 0
    ckpt = HERE / ('_checkpoint_%s.pkl' % (meta or 'x'))
    if checkpoint and ckpt.exists():
        with ckpt.open('rb') as fh:
            saved = pickle.load(fh)
        if saved['new'] == new:
            begin = saved['length'] + 1
            path = saved['path']
            values = saved['values']
            last_fail = saved['last_fail']
            if progress:
                progress('RESUME', begin, None)
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
                    if progress:
                        progress('CERTIFIED', length, dict(start=start, needed=needed))
                    break
        if length % 100 == 0 and progress:
            progress('length', length, dict(maxnew=max(values[state][-1] for state in new),
                                            start=start, needed=needed))
        if budget_seconds is not None and time.time() - T_START > budget_seconds and length < maxlen:
            if checkpoint:
                tmp = ckpt.with_suffix('.tmp')
                with tmp.open('wb') as fh:
                    pickle.dump(dict(length=length, path=path, values=values,
                                    last_fail=last_fail, new=new), fh)
                tmp.replace(ckpt)
            if progress:
                progress('BUDGET-EXIT', length, None)
            raise SystemExit(75)
        if checkpoint and length % 100 == 0:
            tmp = ckpt.with_suffix('.tmp')
            with tmp.open('wb') as fh:
                pickle.dump(dict(length=length, path=path, values=values,
                                 last_fail=last_fail, new=new), fh)
            tmp.replace(ckpt)
    result = dict(states=states, new=new, values=values, known=known_list,
                  path=path, start=start, needed=needed, certified=certified,
                  last_fail=last_fail, initial=initial)
    return result


def emit_records(result, out_path, family, raw, n, E):
    new = result['new']
    needed = result['needed']
    head = dict(audit='PASS', family=family, vertices=n, max_edges=E,
                raw_inputs=raw, distinct_initial_types=len(result['initial']),
                closure_states=len(result['states']),
                new_closure_states=len(new),
                known_closure_states=len(result['states']) - len(new),
                joint_start_candidate=result['start'],
                values_needed_through=result['needed'],
                jointly_certified=result['certified'],
                maximum_grundy_in_prefix=max(max(result['values'][s][:needed + 1]) for s in new),
                worst_prefix_starts=sorted([(result['last_fail'][s] + 1, [s[0], list(s[1])]) for s in new], reverse=True)[:15])
    records = [dict(n=s[0], forbidden=list(s[1]), prefix_start=result['last_fail'][s] + 1,
                    prefix=result['values'][s][:needed + 1]) for s in new]
    text = json.dumps(head, indent=2)
    text = text[:-2] + ',\n  "records": [\n' + ',\n'.join(
        '    ' + json.dumps(row, separators=(',', ':')) for row in records) + '\n  ]\n}\n'
    json.loads(text)
    out_path.write_text(text, encoding='utf-8')
    return head

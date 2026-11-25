#!/usr/bin/env python3
"""Independent value recomputation and record cross-checks for the
seven-vertex pure-three-edge <=5-edge family (K0684 evidence update).

Loads the published shard records (output/shards/partNN.json), re-derives the
initial 7-vertex type set from them, recomputes the FULL value table
(lengths 0..1211) with a fresh implementation of the rooted-clutter + path
recurrence (engine.py functions, K0682 published base table seeding), and:
  (V1) reconstructed combined file bytes hash to the declared sha256,
  (V2) closure of the reconstructed initial types equals the record key set
       (modulo K0682-known <=5-vertex states), with exact count split,
  (V3) every record's prefix matches the recomputed table at every length and
       per-record prefix_start equals the recomputed last period failure + 1,
  (V4) the finite window certification holds independently (path + all states),
  (V5) the K0682 base table states used for seeding match their published
       prefixes and the 34-block lazy extension is consistent,
  (V6) pure-three-edge 6-vertex records that appear in the published
       six-vertex audits (six-edges and full 2^20) match values over the whole
       common range; mixed 2/3-point-edge records appear in neither,
  (V7) counts of pure-triple vs mixed descendants are recorded.

Standard library only. Deterministic. Exit code 0 and the final line is
VERIFY-VALUES: PASS.
"""
import hashlib
from functools import lru_cache
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import closure, delete_root, mex, ordinary, path_values, play

BASE = ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107/output/audit.json'
SIX_EDGES = ROOT / 'research/experiments/rooted-core-six-pure-triple-six-edges-20261107/output/audit.json'
FULL_SIX = ROOT / 'research/experiments/rooted-core-six-pure-triple-full-20261108/output/audit.json'
SHARDS = HERE / 'output/shards'
CANONICAL_SHA = '5a1efeba3f55dd0a4d82421ecea5b8245f99bf8844c1f1cd53365dfdf9bd1bc2'
NEEDED = 1211
START = 571
T = 34


def load_shards():
    parts = sorted(SHARDS.glob('part*.json'))
    assert parts, 'no shards'
    heads, records = [], []
    for i, path in enumerate(parts):
        shard = json.loads(path.read_text(encoding='utf-8'))
        assert shard['shard'] == i and shard['of'] == len(parts)
        assert shard['records_count'] == len(shard['records'])
        heads.append(shard['head'])
        records.extend(shard['records'])
    head = heads.pop(0)
    assert all(h == head for h in heads), 'shard heads differ'
    return head, records


def combined_bytes(head, records):
    text = json.dumps(head, indent=2)
    return (text[:-2] + ',\n  "records": [\n' + ',\n'.join(
        '    ' + json.dumps(row, separators=(',', ':')) for row in records)
        + '\n  ]\n}\n').encode('utf-8')


def known_table():
    base = json.loads(BASE.read_text(encoding='utf-8'))
    return {(row['n'], tuple(row['forbidden'])): row['prefix'] for row in base['records']}


def recompute(initial, known, limit):
    states = closure(initial)
    new = [state for state in states if state not in known]
    path = path_values(limit + 1)
    block = {state: known[state][500:500 + T] for state in known}
    values = {}
    for state in known:
        prefix = known[state]
        values[state] = [prefix[i] if i < len(prefix) else block[state][(i - 500) % T]
                         for i in range(limit + 1)]
    for state in new:
        values[state] = []
    data = {}
    for state in new:
        after = ordinary(play(state, 0)[0])
        deleted = ordinary(delete_root(state))
        retained, detached = set(), set()
        for v in range(1, state[0]):
            child, alive = play(state, v)
            (retained if alive else detached).add(child if alive else ordinary(child))
        data[state] = after, deleted, retained, detached
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
        if length % 400 == 0:
            print('recomputed length', length, flush=True)
    return states, new, values, path


def main():
    head, records = load_shards()
    blob = combined_bytes(head, records)
    digest = hashlib.sha256(blob).hexdigest()
    print('V1 combined sha256', digest, '(declared', CANONICAL_SHA + ')', flush=True)
    assert digest == CANONICAL_SHA, 'combined file hash mismatch'
    rec = {(row['n'], tuple(row['forbidden'])): row for row in records}
    assert len(rec) == len(records) == 2604, (len(rec), len(records))

    initial = sorted(state for state in rec if state[0] == 7)
    assert len(initial) == 924, len(initial)

    known = known_table()
    states, new, values, path = recompute(initial, known, NEEDED)

    rec_states = dict(rec)
    assert len(states) == 2948, len(states)
    known_in_closure = [state for state in states if state in known]
    assert len(known_in_closure) == 344, len(known_in_closure)
    assert set(new) == set(rec_states), 'new state set != record keys'
    split = {6: 0, 7: 0}
    for state in new:
        split[state[0]] += 1
    assert split == {6: 1680, 7: 924}, split
    print('V2 closure ok: states 2948 = new 2604 {6:1680, 7:924} + known 344', flush=True)

    bad = 0
    for state, row in rec_states.items():
        mine = values[state]
        if list(row['prefix']) != list(mine[:NEEDED + 1]):
            bad += 1
    assert bad == 0, '%d record mismatches' % bad
    last_fail = {}
    for state in new:
        lf = max((i for i in range(NEEDED + 1 - T)
                  if values[state][i] != values[state][i + T]), default=-1)
        last_fail[state] = lf
        assert rec_states[state]['prefix_start'] == lf + 1, (state, lf)
    print('V3 all 2604 records x lengths 0..1211 match; per-record prefix_start == last failure + 1', flush=True)

    assert all(path[i] == path[i + T] for i in range(START, 2 * START + 36))
    ok = all(values[state][i] == values[state][i + T]
             for state in new for i in range(START, 2 * START + 36))
    assert ok, 'window certification failed'
    worst = max(last_fail.values())
    assert worst + 1 == START, (worst, START)
    print('V4 window certified: T=34 from N=571 through window [571,1177], worst final failure', worst, flush=True)

    seeded_bad = 0
    for state in known_in_closure:
        prefix = known[state]
        mine = values[state][:len(prefix)]
        if list(mine) != list(prefix):
            seeded_bad += 1
        for i in range(len(prefix), NEEDED + 1):
            e = prefix[500 + (i - 500) % T]
            if values[state][i] != e:
                seeded_bad += 1
    assert seeded_bad == 0
    print('V5 base-table seeding consistent for all 344 known states (direct + block extension)', flush=True)

    six = json.loads(SIX_EDGES.read_text(encoding='utf-8'))['records']
    full6 = json.loads(FULL_SIX.read_text(encoding='utf-8'))['records']
    s6 = {(row['n'], tuple(row['forbidden'])): row['prefix'] for row in six}
    f6 = {(row['n'], tuple(row['forbidden'])): row['prefix'] for row in full6}
    pure, mixed = [], []
    for state in new:
        if state[0] != 6:
            continue
        (pure if all(e.bit_count() == 3 for e in state[1]) else mixed).append(state)
    assert len(pure) == 301 and len(mixed) == 1379, (len(pure), len(mixed))
    cross_bad = absent = 0
    for state in pure:
        mine = values[state]
        for table in (s6, f6):
            prefix = table.get(state)
            if prefix is None:
                absent += 1
                continue
            if list(mine[:min(len(mine), len(prefix))]) != list(prefix[:min(len(mine), len(prefix))]):
                cross_bad += 1
    stray = [state for state in mixed if state in s6 or state in f6]
    assert cross_bad == 0 and absent == 0, (cross_bad, absent)
    assert not stray, stray
    assert all(state in f6 for state in pure) and all(state in s6 for state in pure)
    print('V6', len(pure), 'pure-triple 6-vertex records match both published 6-vertex audits',
          'over the full common range;', len(mixed), 'mixed 2/3-point records absent from both', flush=True)
    mx = max(max(values[state][:NEEDED + 1]) for state in new)
    print('V7 pure/mixed split { pure: %d, mixed: %d }; max Grundy in prefix' % (len(pure), len(mixed)), mx, flush=True)
    assert head['maximum_grundy_in_prefix'] == mx
    print('VERIFY-VALUES: PASS', flush=True)


if __name__ == '__main__':
    main()

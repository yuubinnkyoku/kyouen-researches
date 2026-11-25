#!/usr/bin/env python3
"""Fail-closed tamper battery for the published shard records
(seven-vertex pure-three-edge <=5-edge family, K0684 evidence update).

Loads the shards and checks the shard-internal invariants on the genuine data
(all must hold):
  (T0) headers: shard sequence/count consistency, identical heads,
       counts 2604 records {6: 1680, 7: 924}, head joint_start 571,
       values_needed_through 1211, jointly_certified true,
       head worst entry == max record prefix_start, distinct record keys,
  (T1) each record prefix length == 1212,
  (T2) each record is 34-periodic on its whole certified tail
       [571, 1211] (window theorem consequence),
  (T3) each record prefix_start equals its own last tail failure + 1,
       and never exceeds 571.

Then applies structured tampers and asserts EVERY tampered structure FAILS the
invariants (fail-closed):
  (T4) single value flip inside a record's certified tail,
  (T5) two adjacent-tail value swap inside one record,
  (T6) record prefix truncation by one value,
  (T7) prefix_start field corruption (+1),
  (T8) duplicate record injection,
  (T9) head joint_start corruption (571 -> 500),
  (T10) records_count corruption (off by one).

Standard library only. Deterministic. Ends with VERIFY-TAMPER: PASS.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARDS = HERE / 'output/shards'
NEEDED = 1211
START = 571
T = 34


def load():
    parts = sorted(SHARDS.glob('part*.json'))
    assert parts, 'no shards found'
    heads, records = [], []
    for i, path in enumerate(parts):
        shard = json.loads(path.read_text(encoding='utf-8'))
        assert shard['shard'] == i and shard['of'] == len(parts)
        assert shard['records_count'] == len(shard['records'])
        heads.append(shard['head'])
        records.extend(shard['records'])
    head = heads[0]
    assert all(h == head for h in heads), 'shard heads differ'
    return head, records


def invariants(head, records):
    """Return None if all invariants hold, else a failure reason string."""
    if head['joint_start_candidate'] != START:
        return 'joint_start != 571'
    if head['values_needed_through'] != NEEDED:
        return 'needed != 1211'
    if head['jointly_certified'] is not True:
        return 'jointly_certified != true'
    keys = [(r['n'], tuple(r['forbidden'])) for r in records]
    if len(set(keys)) != len(keys):
        return 'duplicate record keys'
    if len(records) != head['new_closure_states']:
        return 'new_closure_states != len(records)'
    counts = {6: 0, 7: 0}
    for r in records:
        counts.setdefault(r['n'], 0)
        counts[r['n']] += 1
    if counts != {6: 1680, 7: 924}:
        return 'vertex split != {6: 1680, 7: 924}'
    worst = None
    for r in records:
        prefix = r['prefix']
        if len(prefix) != NEEDED + 1:
            return 'prefix length != 1212 for %r' % ((r['n'], r['forbidden']),)
        if not all(prefix[i] == prefix[i + T] for i in range(START, NEEDED + 1 - T)):
            return 'tail periodicity broken for %r' % ((r['n'], r['forbidden']),)
        lf = max((i for i in range(NEEDED + 1 - T)
                  if prefix[i] != prefix[i + T]), default=-1)
        if r['prefix_start'] != lf + 1:
            return 'prefix_start != last failure + 1 for %r' % ((r['n'], r['forbidden']),)
        if r['prefix_start'] > START or r['prefix_start'] < 0:
            return 'prefix_start out of range for %r' % ((r['n'], r['forbidden']),)
        worst = lf if worst is None else max(worst, lf)
    if worst + 1 != head['joint_start_candidate']:
        return 'head joint start != max record prefix_start'
    if head['worst_prefix_starts'][0][0] != head['joint_start_candidate']:
        return 'head worst entry mismatch'
    return None


def expect_fail(name, head, records):
    reason = invariants(head, records)
    assert reason is not None, 'tamper %s was NOT detected' % name
    assert isinstance(reason, str) and reason
    print('  tamper %-22s detected: %s' % (name, reason), flush=True)


def main():
    head, records = load()
    import copy
    reason = invariants(head, records)
    assert reason is None, 'genuine data failed: %s' % reason
    print('T0-T3 genuine shard data satisfies all shard-internal invariants', flush=True)

    r0 = records[7]
    prefix = list(r0['prefix'])
    mid = 700
    assert prefix[mid] != 0 or True
    t4 = copy.deepcopy(records)
    t4[7]['prefix'][mid] = (t4[7]['prefix'][mid] + 1) % 5
    expect_fail('T4 tail value flip', head, t4)

    t5 = copy.deepcopy(records)
    p = t5[7]['prefix']
    i = next(j for j in range(START, NEEDED - T) if p[j] != p[j + 1])
    p[i], p[i + 1] = p[i + 1], p[i]
    expect_fail('T5 tail value swap', head, t5)

    t6 = copy.deepcopy(records)
    t6[7]['prefix'] = t6[7]['prefix'][:-1]
    t6[7]['prefix_start'] = t6[7]['prefix_start']
    expect_fail('T6 prefix truncation', head, t6)

    t7 = copy.deepcopy(records)
    t7[7]['prefix_start'] = t7[7]['prefix_start'] + 1
    expect_fail('T7 prefix_start +1', head, t7)

    t8 = copy.deepcopy(records)
    t8[7] = copy.deepcopy(records[8])
    expect_fail('T8 duplicate record', head, t8)

    t9 = copy.deepcopy(head)
    t9['joint_start_candidate'] = 500
    expect_fail('T9 head joint_start', t9, records)

    t10 = copy.deepcopy(head)
    t10['new_closure_states'] = t10['new_closure_states'] + 1
    expect_fail('T10 counts off-by-one', t10, records)

    print('T4-T10 all structured tampers detected (fail-closed)', flush=True)
    print('VERIFY-TAMPER: PASS', flush=True)


if __name__ == '__main__':
    main()

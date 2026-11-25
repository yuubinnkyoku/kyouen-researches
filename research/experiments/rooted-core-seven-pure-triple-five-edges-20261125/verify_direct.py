#!/usr/bin/env python3
"""Primitive direct game verification for the seven-vertex pure-three-edge
<=5-edge family (K0684 evidence update).

For a fixed-seed stratified sample of 400 new closure states (strata: vertex
count x edge count x pure/mixed-edge class) and every path length 0..6, the
Grundy value of the composite position (core clutter + two-point forbidden path
attached at the root) is recomputed by brute-force exploration of the full
game graph (the same "direct" primitive used by the published
rooted-core-six-pure-triple-six-edges-20261107 verifier) and compared with the
published shard record values.

The check is keyed off the ORIGINAL game definition (fill vertices, never
complete a forbidden edge), not off the algebraic recurrence, so it validates
the recurrence at short lengths independently.

Resumable: progress is checkpointed to output/_direct_progress.json; rerun
until the final line reads VERIFY-DIRECT: PASS.
Standard library only. Deterministic.
"""
from functools import lru_cache
import json
from pathlib import Path
import random
import sys
import time

HERE = Path(__file__).resolve().parent
SHARDS = HERE / 'output/shards'
PROGRESS = HERE / 'output/_direct_progress.json'
SAMPLE_SIZE = 400
SEED = 7
MAXLEN = 6


def load_records():
    records = []
    for part in sorted(SHARDS.glob('part*.json')):
        data = json.loads(part.read_text(encoding='utf-8'))
        records.extend(data['records'])
    return records


def strata_of(state):
    n, edges = state
    pure = all(e.bit_count() == 3 for e in edges)
    return (n, len(edges), 1 if pure else 0)


def stratified_sample(states, size=SAMPLE_SIZE):
    by_stratum = {}
    for state in states:
        by_stratum.setdefault(strata_of(state), []).append(state)
    for key in by_stratum:
        by_stratum[key].sort()
    keys = sorted(by_stratum)
    total = sum(len(pool) for pool in by_stratum.values())
    ideal = {key: size * len(by_stratum[key]) / total for key in keys}
    # every nonempty stratum gets at least one state
    quota = {key: 1 for key in keys}
    remaining = size - len(keys)
    order = sorted(keys, key=lambda k: (-ideal[k], k))
    for key in order:
        if remaining <= 0:
            break
        want = min(len(by_stratum[key]), max(quota[key], int(ideal[key]))) - quota[key]
        take = min(want, remaining)
        quota[key] += take
        remaining -= take
    while remaining > 0:
        spare = sorted((k for k in keys if quota[k] < len(by_stratum[k])),
                       key=lambda k: (-(ideal[k] - quota[k]), k))
        assert spare, 'cannot allocate %d' % remaining
        for key in spare:
            if remaining <= 0:
                break
            quota[key] += 1
            remaining -= 1
    sample = []
    rng = random.Random(SEED)
    for key in keys:
        pool = by_stratum[key]
        take = quota[key]
        assert 0 < take <= len(pool), (key, take, len(pool))
        if take == len(pool):
            sample.extend(pool)
        else:
            sample.extend(rng.sample(pool, take))
    assert len(sample) == size, len(sample)
    return sorted(sample), quota


def direct(n, forbidden, length):
    edges = list(forbidden)
    if length:
        edges.append(1 | (1 << n))
        edges.extend((1 << v) | (1 << (v + 1)) for v in range(n, n + length - 1))
    edges = tuple(edges)

    @lru_cache(None)
    def game(s):
        result = 0
        options = set()
        for v in range(n + length):
            if s >> v & 1:
                continue
            t = s | (1 << v)
            if any(t & edge == edge for edge in edges):
                continue
            options.add(game(t))
        while result in options:
            result += 1
        return result

    value = game(0)
    return value, game.cache_info().currsize


def main():
    records = load_records()
    states = [(row['n'], tuple(row['forbidden'])) for row in records]
    values = dict(zip(states, (row['prefix'] for row in records)))
    sample, quota = stratified_sample(states)

    done = {}
    if PROGRESS.exists():
        done = json.loads(PROGRESS.read_text(encoding='utf-8'))
    total_states = 0
    checks = 0
    resumed_states = 0
    progress = {key: value for key, value in done.items()}
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else None
    t0 = time.time()
    for si, state in enumerate(sample):
        key = '%d|%s' % (state[0], ','.join(map(str, state[1])))
        start = progress.get(key, 0)
        if start == MAXLEN + 1:
            resumed_states += 1
            checks += MAXLEN + 1
            continue
        n, forbidden = state
        for length in range(start, MAXLEN + 1):
            g, size = direct(n, forbidden, length)
            published = values[state][length]
            assert g == published, (state, length, g, published)
            checks += 1
            total_states += size
            progress[key] = length + 1
        progress[key] = MAXLEN + 1
        if si % 25 == 1:
            PROGRESS.write_text(json.dumps(progress), encoding='utf-8')
        if budget is not None and time.time() - t0 > budget and si < len(sample) - 1:
            PROGRESS.write_text(json.dumps(progress), encoding='utf-8')
            print('BUDGET-EXIT after %d states (%d checks)' % (si, checks), flush=True)
            return 75
    PROGRESS.unlink(missing_ok=True)
    strata_counts = {}
    for state in sample:
        strata_counts[str(strata_of(state))] = strata_counts.get(str(strata_of(state)), 0) + 1
    print('stratified sample %d states over %d strata (seed %d, lengths 0..%d)'
          % (len(sample), len(strata_counts), SEED, MAXLEN), flush=True)
    print('strata histogram: %s' % json.dumps(strata_counts, sort_keys=True), flush=True)
    print('direct subset checks %d, safe states explored %d' % (checks, total_states), flush=True)
    assert checks == SAMPLE_SIZE * (MAXLEN + 1), checks
    print('resumed prefilled states: %d' % resumed_states, flush=True)
    print('VERIFY-DIRECT: PASS', flush=True)


if __name__ == '__main__':
    sys.exit(main())

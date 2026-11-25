#!/usr/bin/env python3
"""Independently check each finite DAG certificate and enumerate the entire safe product."""
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def mex(vals):
    z = 0
    while z in vals:
        z += 1
    return z


def valid(t, caps, h, limit):
    if any(z < 0 or z > cap for z, cap in zip(t, caps)):
        return False
    return sum(sorted(t)[-h:]) <= limit


def successors(t, caps, h, limit):
    result = []
    for j, cap in enumerate(caps):
        if t[j] == cap:
            continue
        u = list(t)
        u[j] += 1
        if valid(u, caps, h, limit):
            result.append(tuple(u))
    return result


def check(item):
    caps = tuple(item['capacities'])
    h, limit = item['h'], item['r']
    root = tuple(item['root'])
    assert 1 <= h < len(caps)
    assert valid(root, caps, h, limit)
    states = {tuple(map(int, k.split(','))): v for k, v in item['states'].items()}
    assert len(states) == len(item['states'])
    assert all(valid(s, caps, h, limit) for s in states)
    # Check reachable closure and no extra states, independent of Grundy labels.
    reached = {root}
    todo = [root]
    while todo:
        t = todo.pop()
        for u in successors(t, caps, h, limit):
            if u not in reached:
                reached.add(u)
                todo.append(u)
    assert reached == states.keys(), ('reachability mismatch', len(reached), len(states))
    # A local certificate check: every mex equation must hold, with all legal successors present.
    for t, value in states.items():
        assert isinstance(value, int) and value >= 0
        assert value == mex({states[u] for u in successors(t, caps, h, limit)}), t
    assert states[root] == item['grundy']
    # Independent computation on the ENTIRE safe Cartesian product, not just descendants.
    all_states = [t for t in itertools.product(*(range(z + 1) for z in caps)) if valid(t, caps, h, limit)]
    all_states.sort(key=lambda t: sum(t), reverse=True)
    dp = {}
    for t in all_states:
        s = set()
        for j in range(len(caps)):
            if t[j] >= caps[j]:
                continue
            u = t[:j] + (t[j] + 1,) + t[j + 1:]
            if sum(sorted(u)[-h:]) <= limit:
                s.add(dp[u])
        dp[t] = mex(s)
    assert all(dp[t] == value for t, value in states.items())
    child = {j: dp[u] for j in range(len(caps)) for u in [tup_inc(root, j)] if u in dp and sum(u) == sum(root) + 1}
    assert set(child.values()) == set(range(item['grundy']))
    print('PASS', item['name'], 'g=', item['grundy'], 'reachable=', len(states), 'full-safe=', len(all_states), 'child=', child,
          'histogram=', dict(sorted(Counter(states.values()).items())))


def tup_inc(x, i):
    return x[:i] + (x[i] + 1,) + x[i + 1:]


def main():
    data = (HERE / 'certificates.json').read_bytes()
    print('certificate SHA256', hashlib.sha256(data).hexdigest())
    for item in json.loads(data)['witnesses']:
        check(item)


if __name__ == '__main__':
    main()

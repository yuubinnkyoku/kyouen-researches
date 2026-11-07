#!/usr/bin/env python3
"""All rooted rank<=3 clutters on at most five core vertices, one arbitrary tail."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path

from engine import canonical, closure, last_period_failure, mex, solve


def all_cores():
    labeled = []
    counts = {}
    for n in range(1, 6):
        pairs = [sum(1 << v for v in edge) for edge in combinations(range(n), 2)]
        triples = [sum(1 << v for v in edge) for edge in combinations(range(n), 3)]
        before = len(labeled)
        for mask in range(1 << len(pairs)):
            chosen = [pairs[j] for j in range(len(pairs)) if mask >> j & 1]
            available = [t for t in triples if not any(p & t == p for p in chosen)]
            for triple_mask in range(1 << len(available)):
                edges = tuple(sorted(chosen + [t for j, t in enumerate(available) if triple_mask >> j & 1]))
                labeled.append((n, edges))
        counts[n] = len(labeled) - before
    return labeled, counts


def direct(n, forbidden, length):
    """Raw safe occupied sets, without residual cleanup or path decomposition."""
    points = n + length
    edges = list(forbidden)
    if length:
        edges.append(1 | (1 << n))
        edges += [(1 << v) | (1 << (v + 1)) for v in range(n, points - 1)]

    @lru_cache(None)
    def g(s):
        options = set()
        for v in range(points):
            child = s | (1 << v)
            if s >> v & 1 or any(child & edge == edge for edge in edges):
                continue
            options.add(g(child))
        return mex(options)

    return g(0), g.cache_info().currsize


def main():
    labeled, counts = all_cores()
    unique = sorted({canonical(*state) for state in labeled})
    def progress(length, states, maximum):
        if length % 200 == 0:
            print('length', length, 'states', states, 'current maximum', maximum, flush=True)
    _, states, values, path = solve(unique, 1100, progress)
    assert len(labeled) == 6337 and len(unique) == len(states) == 513
    assert counts == {1: 1, 2: 2, 3: 9, 4: 113, 5: 6212}
    assert set(states) == set(unique)  # the whole finite state system is closed
    # The general theorem only needs values through 1069.
    start, period = 500, 34
    last_comparison = 2 * start + period + 1
    assert last_comparison + period == 1069
    assert all(path[n] == path[n + period] for n in range(start, last_comparison + 1))
    records = []
    for state in states:
        seq = values[state]
        assert all(seq[n] == seq[n + period] for n in range(start, last_comparison + 1))
        first = last_period_failure(seq, period) + 1
        block = seq[1020:1054]
        assert all(any(block[j] != block[(j + shift) % period] for j in range(period))
                   for shift in range(1, period))
        records.append(dict(n=state[0], forbidden=list(state[1]), period=period,
                            first_periodic_index=first,
                            maximum_grundy=max(seq[:1070]),
                            prefix=seq[:1070]))
    assert max(row["first_periodic_index"] for row in records) == 500
    assert max(row["maximum_grundy"] for row in records) == 23
    sharp = canonical(5, (3, 5, 9, 14, 18))
    assert values[sharp][499] != values[sharp][533]
    direct_cases = direct_states = 0
    for state in states:
        for length in range(11):
            actual, visited = direct(*state, length)
            assert actual == values[state][length]
            direct_cases += 1
            direct_states += visited
    # Check every labeled input at a nonzero tail too, not just its canonical representative.
    for state in labeled:
        actual, visited = direct(*state, 3)
        assert actual == values[canonical(*state)][3]
        direct_cases += 1
        direct_states += visited
    # K0680's triple-leaf gadget has an existing exact capacity-two reduction.
    fork = canonical(3, (3, 5))
    triple_broom = canonical(4, (3, 5, 9, 14))
    assert values[fork] == values[triple_broom]
    output = dict(audit="PASS", labeled_core_counts=counts, labeled_cores=len(labeled),
                  rooted_isomorphism_types=len(unique), closed_rooted_states=len(states),
                  joint_certificate=dict(start=start, period=period,
                      comparisons=[start, last_comparison], values_needed_through=1069),
                  exact_period_start_histogram=dict(sorted(Counter(row["first_periodic_index"] for row in records).items())),
                  maximum_grundy=23, direct_subset_checks=direct_cases,
                  direct_safe_subset_states=direct_states,
                  sharp_start_witness=dict(n=sharp[0], forbidden=sharp[1],
                      discrepancy=[499, values[sharp][499], values[sharp][533]]),
                  records=records)
    target = Path(__file__).with_name("output") / "audit.json"
    target.parent.mkdir(exist_ok=True)
    # One line per core keeps this finite certificate readable without expanding every integer.
    head = {key: value for key, value in output.items() if key != "records"}
    text = json.dumps(head, ensure_ascii=False, indent=2)
    text = text[:-2] + ',\n  "records": [\n' + ',\n'.join(
        '    ' + json.dumps(row, ensure_ascii=False, separators=(',', ':')) for row in records) + '\n  ]\n}\n'
    json.loads(text)
    target.write_text(text, encoding="utf-8")
    print(json.dumps(head, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

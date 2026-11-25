#!/usr/bin/env python3
"""Bounded diagnostic beyond the four-vertex theorem; no automatic proof claim."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import time
from engine import canonical, last_period_failure, solve


def main():
    started = time.monotonic()
    n = 5
    pairs = [sum(1 << i for i in edge) for edge in combinations(range(n), 2)]
    triples = [sum(1 << i for i in edge) for edge in combinations(range(n), 3)]
    cores, labeled = set(), 0
    for mask in range(1 << len(pairs)):
        chosen = [pairs[j] for j in range(len(pairs)) if mask >> j & 1]
        available = [t for t in triples if not any(p & t == p for p in chosen)]
        for tailmask in range(1 << len(available)):
            edges = tuple(sorted(chosen + [t for j, t in enumerate(available) if tailmask >> j & 1]))
            labeled += 1
            cores.add(canonical(n, edges))
    print('generated', labeled, 'canonical', len(cores), flush=True)
    def progress(length, states, maximum):
        print('length', length, 'states', states, 'current maximum', maximum, flush=True)
    initial, states, values, path = solve(sorted(cores), 1300, progress)
    starts = sorted([(last_period_failure(values[state], 34) + 1, state,
                      max(values[state])) for state in initial], reverse=True)
    output = dict(scope='diagnostic prefix only; joint certificate is not automatic',
                  labeled_cores=labeled, canonical_cores=len(cores), closure_states=len(states),
                  prefix_through=1300, worst_prefix_starts=starts[:30],
                  maximum_grundy_in_prefix=max(m for n, state, m in starts),
                  prefix_start_histogram=dict(sorted(Counter(n for n, state, m in starts).items())),
                  seconds=time.monotonic() - started)
    target = Path(__file__).with_name('output') / 'five_vertex_probe.json'
    target.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(output, indent=2), flush=True)


if __name__ == '__main__':
    main()

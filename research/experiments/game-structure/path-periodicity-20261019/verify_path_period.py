#!/usr/bin/env python3
"""Certified finite base of an eventual-period theorem for Node Kayles on paths.

The infinite step is proved in proof.md, not inferred from this computation.
"""
import json
import heapq
from functools import lru_cache
from pathlib import Path

PREPERIOD = 52
PERIOD = 34
INDUCTION_START = 2 * PREPERIOD + PERIOD + 2  # 140
BASE_END = INDUCTION_START - 1
MAX_REQUIRED = BASE_END + PERIOD  # 173


def mex(options):
    i = 0
    while i in options:
        i += 1
    return i


def path_values(max_n):
    g = [0]
    for n in range(1, max_n + 1):
        if n == 1:
            options = {0}
        elif n == 2:
            options = {g[0]}
        else:
            options = {g[n - 2]}
            options.update(g[a] ^ g[n - 3 - a] for a in range(n - 2))
        g.append(mex(options))
    return g


def independent_free_mask_solver(n):
    # Completely separate definition: recurse over remaining legal vertices.
    adj = []
    for i in range(n):
        m = 1 << i
        if i > 0:
            m |= 1 << (i - 1)
        if i + 1 < n:
            m |= 1 << (i + 1)
        adj.append(m)

    @lru_cache(None)
    def grundy(free):
        options = set()
        todo = free
        while todo:
            bit = todo & -todo
            i = bit.bit_length() - 1
            options.add(grundy(free & ~adj[i]))
            todo -= bit
        return mex(options)

    return grundy((1 << n) - 1), grundy.cache_info().currsize


def main():
    g = path_values(MAX_REQUIRED)
    # Finite certificate sufficient for an infinite periodicity proof.
    assert all(g[n] == g[n + PERIOD] for n in range(PREPERIOD, INDUCTION_START))
    assert g[PREPERIOD - 1] != g[PREPERIOD - 1 + PERIOD]
    # Proper divisors of 34 are 1,2,17.
    assert all(any(g[n] != g[n + d] for n in range(PREPERIOD, PREPERIOD + PERIOD))
               for d in (1, 2, 17))
    # A deliberately longer check; not used for the proof.
    g_long = path_values(2000)
    assert all(g_long[n] == g_long[n + PERIOD] for n in range(PREPERIOD, 2000 - PERIOD))
    state_counts = {}
    for n in range(0, 21):
        direct, states = independent_free_mask_solver(n)
        assert direct == g[n], (n, direct, g[n])
        state_counts[str(n)] = states
    assert max(g[:PREPERIOD + PERIOD]) == 9
    first_occurrence = {str(v): next(n for n in range(PREPERIOD + PERIOD) if g[n] == v)
                        for v in sorted(set(g[:PREPERIOD + PERIOD]))}
    assert set(map(int, first_occurrence)) == {0, 1, 2, 3, 4, 5, 7, 8, 9}
    # Every max-degree-two graph is a disjoint union of paths and cycles.
    # Shortest XOR paths on 16 states give exact minimum total vertices.
    distance = [10**9] * 16
    distance[0] = 0
    heap = [(0, 0)]
    while heap:
        d, x = heapq.heappop(heap)
        if d != distance[x]:
            continue
        for value, cost in ((int(v), c) for v, c in first_occurrence.items()):
            if value == 0:
                continue
            y = x ^ value
            if d + cost < distance[y]:
                distance[y] = d + cost
                heapq.heappush(heap, (distance[y], y))
    assert distance == [0, 1, 3, 4, 13, 14, 16, 17,
                        68, 69, 71, 72, 81, 82, 84, 85]
    assert g[68] ^ g[13] ^ g[3] ^ g[1] == 15
    # Cycle game: all first moves leave P_(n-3).
    cycle = {str(n): int(g[n - 3] == 0) for n in range(3, 90)}
    out = {
        "game": "Node Kayles / two-point forbidden-placement game on paths",
        "recurrence": "g(0)=0; g(1)=g(2)=1; for n>=3, mex({g(n-2)} union {g(a) xor g(n-3-a):0<=a<=n-3})",
        "period": PERIOD,
        "first_periodic_index": PREPERIOD,
        "induction_start": INDUCTION_START,
        "verified_base_indices": [PREPERIOD, BASE_END],
        "max_computed_index_for_proof": MAX_REQUIRED,
        "primitive_period": True,
        "max_nimber": max(g[:PREPERIOD + PERIOD]),
        "max_degree_two_nimber_bound": 15,
        "max_degree_two_bound_attained_at_vertices": 85,
        "max_degree_two_witness_paths": [68, 13, 3, 1],
        "first_occurrence_per_path_nimber": first_occurrence,
        "min_vertices_for_each_degree_two_nimber_0_to_15": distance,
        "losing_path_residues_mod_34_from_n52": [((PREPERIOD + i) % PERIOD)
               for i, v in enumerate(g[PREPERIOD:PREPERIOD + PERIOD]) if v == 0],
        "prefix_0_to_51": g[:PREPERIOD],
        "period_block_52_to_85": g[PREPERIOD:PREPERIOD + PERIOD],
        "preperiod_failure": [PREPERIOD - 1, g[PREPERIOD - 1], g[PREPERIOD - 1 + PERIOD]],
        "independent_full_state_check_n": [0, 20],
        "independent_full_state_counts": state_counts,
        "cycle_values_3_to_89": cycle,
    }
    path = Path(__file__).with_name("path_period_results.json")
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS: finite periodicity base, exact minimal onset/period, full-state audit n<=20")
    print("g(51),g(85)=", g[51], g[85], "period block", g[52:86])
    print("output:", path)


if __name__ == "__main__":
    main()

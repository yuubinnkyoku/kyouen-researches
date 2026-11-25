#!/usr/bin/env python3
"""Independent finite audit for the arbitrary-t pure-fiber Grundy bound.

The theorem is proved in report.md. This program checks a finite parameter box
by two independently generated state spaces:
  * labeled occupancy vectors;
  * sorted occupancy multisets (permutation orbits).
Neither recurrence uses the theorem's decomposition.
"""
from __future__ import annotations

import json


def mex(values):
    values = set(values)
    g = 0
    while g in values:
        g += 1
    return g


def theoretical_bound(t: int, m: int) -> int:
    if m < t or (m - t) % 2 == 0:
        return 1
    return t if t % 2 else t + 1


def solve_labeled(w: int, m: int, t: int, q: int):
    memo = {}

    def grundy(state):
        if state in memo:
            return memo[state]
        child_values = set()
        for i, c in enumerate(state):
            if c == m:
                continue
            nxt = list(state)
            nxt[i] += 1
            nxt = tuple(nxt)
            if sum(min(x, t) for x in nxt) <= q - 1:
                child_values.add(grundy(nxt))
        memo[state] = mex(child_values)
        return memo[state]

    grundy((0,) * w)
    return memo


def solve_canonical(w: int, m: int, t: int, q: int):
    memo = {}

    def grundy(state):
        if state in memo:
            return memo[state]
        child_values = set()
        previous = None
        for i, c in enumerate(state):
            if c == previous or c == m:
                previous = c
                continue
            nxt = list(state)
            nxt[i] += 1
            nxt = tuple(sorted(nxt, reverse=True))
            if sum(min(x, t) for x in nxt) <= q - 1:
                child_values.add(grundy(nxt))
            previous = c
        memo[state] = mex(child_values)
        return memo[state]

    grundy((0,) * w)
    return memo


def main():
    per_t = {}
    total_cases = 0
    total_labeled = 0
    total_canonical = 0
    global_max = 0
    max_labeled_case = 0
    max_canonical_case = 0

    for t in range(1, 6):
        t_cases = 0
        t_labeled = 0
        t_canonical = 0
        t_max = 0
        for w in range(1, 5):
            for m in range(1, 8):
                for q in range(1, t * w + 3):
                    labeled = solve_labeled(w, m, t, q)
                    canonical = solve_canonical(w, m, t, q)

                    projected = {}
                    for state, value in labeled.items():
                        key = tuple(sorted(state, reverse=True))
                        old = projected.setdefault(key, value)
                        if old != value:
                            raise AssertionError(
                                f"permutation invariance failed: "
                                f"t={t}, w={w}, m={m}, q={q}, state={key}"
                            )
                    if projected != canonical:
                        raise AssertionError(
                            f"independent state-space mismatch: "
                            f"t={t}, w={w}, m={m}, q={q}"
                        )

                    observed = max(labeled.values(), default=0)
                    bound = theoretical_bound(t, m)
                    if observed > bound:
                        raise AssertionError(
                            f"bound violated: t={t}, w={w}, m={m}, q={q}, "
                            f"observed={observed}, bound={bound}"
                        )
                    if m < t or (m - t) % 2 == 0:
                        if observed > 1:
                            raise AssertionError(
                                f"parity-one bound violated: "
                                f"t={t}, w={w}, m={m}, q={q}, observed={observed}"
                            )

                    t_cases += 1
                    t_labeled += len(labeled)
                    t_canonical += len(canonical)
                    t_max = max(t_max, observed)
                    max_labeled_case = max(max_labeled_case, len(labeled))
                    max_canonical_case = max(max_canonical_case, len(canonical))

        per_t[str(t)] = {
            "parameter_sets": t_cases,
            "labeled_states": t_labeled,
            "canonical_states": t_canonical,
            "maximum_observed_grundy": t_max,
        }
        total_cases += t_cases
        total_labeled += t_labeled
        total_canonical += t_canonical
        global_max = max(global_max, t_max)

    result = {
        "status": "PASS",
        "method": "two independently generated recursive-mex state spaces",
        "scope": {
            "t": [1, 5],
            "w": [1, 4],
            "m": [1, 7],
            "q": "1..t*w+2 for each (t,w)",
            "rule": "safe iff sum(min(c_b,t)) <= q-1; one coordinate increases by one",
        },
        "totals": {
            "parameter_sets": total_cases,
            "labeled_states": total_labeled,
            "canonical_states": total_canonical,
            "maximum_labeled_states_in_one_case": max_labeled_case,
            "maximum_canonical_states_in_one_case": max_canonical_case,
            "maximum_observed_grundy": global_max,
        },
        "per_t": per_t,
        "limitations": [
            "finite audit only; it does not prove the unbounded theorem",
            "the recurrences do not use the decomposition or the claimed bound",
            "the canonical implementation independently generates quotient transitions",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()

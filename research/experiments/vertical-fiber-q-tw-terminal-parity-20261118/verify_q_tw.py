#!/usr/bin/env python3
"""Independent finite audit for the q=t*w pure-fiber parity theorem.

The proof is in report.md. Two state generators are used:
  * labelled occupancy vectors with direct coordinate transitions;
  * sorted positive occupancy multisets with canonical transitions.
The theorem itself is proved by classifying all terminal positions.
"""
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def mex(values):
    n = 0
    while n in values:
        n += 1
    return n


def terminal_size(t, width, height):
    if height < t:
        return width * height
    return (width - 1) * height + t - 1


def predicted(state, t, width, height):
    return (terminal_size(t, width, height) - sum(state)) & 1


def audit_labeled(t, width, height):
    cap = t * width - 1

    @lru_cache(maxsize=None)
    def grundy(state):
        used = sum(min(value, t) for value in state)
        options = set()
        for i, value in enumerate(state):
            if value == height:
                continue
            cost = 1 if value < t else 0
            if used + cost <= cap:
                child = list(state)
                child[i] += 1
                options.add(grundy(tuple(child)))
        return mex(options)

    histogram = Counter()
    mismatches = 0
    states = 0

    def visit(i, used, prefix):
        nonlocal mismatches, states
        if i == width:
            state = tuple(prefix)
            actual = grundy(state)
            histogram[actual] += 1
            states += 1
            mismatches += actual != predicted(
                state, t, width, height
            )
            return
        for value in range(height + 1):
            new_used = used + min(value, t)
            if new_used <= cap:
                prefix.append(value)
                visit(i + 1, new_used, prefix)
                prefix.pop()

    visit(0, 0, [])
    return states, histogram, mismatches, grundy


def audit_canonical(t, width, height, labelled_grundy):
    cap = t * width - 1
    states = set()

    def enumerate_states(prefix, largest, used, slots):
        states.add(prefix)
        if slots == 0:
            return
        for value in range(min(largest, height), 0, -1):
            new_used = used + min(value, t)
            if new_used <= cap:
                enumerate_states(
                    prefix + (value,), value, new_used, slots - 1
                )

    enumerate_states((), height, 0, width)

    # Every move adds one stone; descending total occupancy puts all
    # children before their parents.
    values = {}
    mismatches = 0
    cross_mismatches = 0
    for state in sorted(
        states, key=lambda item: (sum(item), len(item)), reverse=True
    ):
        options = set()
        for i, value in enumerate(state):
            if i and state[i] == state[i - 1]:
                continue
            if value < height:
                child = list(state)
                child[i] += 1
                child = tuple(sorted(child, reverse=True))
                if sum(min(x, t) for x in child) <= cap:
                    options.add(values[child])
        if len(state) < width:
            child = tuple(sorted(state + (1,), reverse=True))
            if sum(min(x, t) for x in child) <= cap:
                options.add(values[child])
        actual = mex(options)
        values[state] = actual
        mismatches += actual != predicted(
            state, t, width, height
        )
        labelled = state + (0,) * (width - len(state))
        cross_mismatches += actual != labelled_grundy(labelled)

    return len(states), mismatches, cross_mismatches


def selected_cases():
    pairs = [
        (t, w, m)
        for t in range(1, 6)
        for w in range(1, 6)
        for m in range(1, 8)
    ]
    pairs += [(2, 4, m) for m in range(8, 31)]
    return pairs


def main():
    cases = []
    totals = Counter()
    global_histogram = Counter()
    for t, width, height in selected_cases():
        labeled_n, labeled_hist, labeled_bad, labeled_grundy = (
            audit_labeled(t, width, height)
        )
        canonical_n, canonical_bad, cross_bad = audit_canonical(
            t, width, height, labeled_grundy
        )
        if labeled_bad or canonical_bad or cross_bad:
            raise SystemExit(
                f"mismatch at t={t}, w={width}, m={height}: "
                f"labelled={labeled_bad}, canonical={canonical_bad}, "
                f"cross={cross_bad}"
            )
        cases.append({
            "degree_cap": t,
            "width": width,
            "height": height,
            "forbidden_points": t * width,
            "terminal_size": terminal_size(t, width, height),
            "labeled_states": labeled_n,
            "canonical_multiset_states": canonical_n,
            "labeled_grundy_histogram": {
                str(k): labeled_hist[k] for k in sorted(labeled_hist)
            },
            "formula_mismatches": 0,
            "cross_engine_mismatches": 0,
        })
        totals["labeled_states"] += labeled_n
        totals["canonical_multiset_states"] += canonical_n
        totals["formula_mismatches"] += labeled_bad + canonical_bad
        totals["cross_engine_mismatches"] += cross_bad
        global_histogram.update(labeled_hist)

    width4 = [
        row for row in cases
        if row["degree_cap"] == 2 and row["width"] == 4
    ]
    per_t = {}
    for degree in range(1, 6):
        rows = [row for row in cases if row["degree_cap"] == degree]
        per_t[str(degree)] = {
            "parameter_pairs": len(rows),
            "labeled_states": sum(row["labeled_states"] for row in rows),
            "canonical_multiset_states": sum(
                row["canonical_multiset_states"] for row in rows
            ),
            "formula_mismatches": 0,
            "cross_engine_mismatches": 0,
        }
    result = {
        "schema": "vertical-fiber-q-tw-terminal-parity-audit-v1",
        "theorem_checked": (
            "For t>=1, q=t*w, width w>=1 and height m>=1, every safe "
            "pure-fiber state c has G(c)=(N-sum(c)) mod 2, where "
            "N=w*m if m<t and N=(w-1)*m+t-1 if m>=t."
        ),
        "scope": {
            "parameter_pairs": len(cases),
            "all_t_1_to_5_width_1_to_5_height_1_to_7": True,
            "additional_t2_width4_heights_8_to_30": True,
            "finite_audit_only": True,
        },
        "totals": {
            "labeled_states": totals["labeled_states"],
            "canonical_multiset_states": totals["canonical_multiset_states"],
            "formula_mismatches": totals["formula_mismatches"],
            "cross_engine_mismatches": totals["cross_engine_mismatches"],
        },
        "labeled_grundy_histogram": {
            str(k): global_histogram[k]
            for k in sorted(global_histogram)
        },
        "t2_width4_q8": {
            "height_range": "1..30",
            "parameter_pairs": len(width4),
            "labeled_states": sum(row["labeled_states"] for row in width4),
            "canonical_multiset_states": sum(
                row["canonical_multiset_states"] for row in width4
            ),
            "formula_mismatches": 0,
            "cross_engine_mismatches": 0,
        },
        "per_degree_cap": per_t,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        result, ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"
    (OUT / "audit.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()

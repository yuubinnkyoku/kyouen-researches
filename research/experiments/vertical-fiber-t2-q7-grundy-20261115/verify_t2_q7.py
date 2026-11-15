#!/usr/bin/env python3
"""Independent mex audit for the pure t=2, q=7 fiber game."""
from collections import Counter
from functools import lru_cache
import json

CAPACITY = 6


def mex(values):
    value = 0
    while value in values:
        value += 1
    return value


@lru_cache(maxsize=None)
def resource_grundy(p, empty, single, remaining):
    if remaining == 0 or empty + single == 0:
        return 0
    options = set()
    if empty:
        options.add(resource_grundy(p, empty - 1, single + 1, remaining - 1))
    if single:
        options.add(p ^ resource_grundy(p, empty, single - 1, remaining - 1))
    return mex(options)


def structural_value(state, width, height):
    saturated = sum(value >= 2 for value in state)
    single = sum(value == 1 for value in state)
    empty = width - saturated - single
    remaining = CAPACITY - 2 * saturated - single
    tail_xor = 0
    for value in state:
        if value >= 2:
            tail_xor ^= (height - value) & 1
    return tail_xor ^ resource_grundy(height & 1, empty, single, remaining)


def audit_labeled(width, height):
    @lru_cache(maxsize=None)
    def grundy(state):
        used = sum(min(value, 2) for value in state)
        options = set()
        for index, value in enumerate(state):
            if value < height:
                new_used = used + (1 if value < 2 else 0)
                if new_used <= CAPACITY:
                    child = list(state)
                    child[index] += 1
                    options.add(grundy(tuple(child)))
        return mex(options)

    histogram = Counter()
    mismatches = []

    def enumerate_states(index, used, prefix):
        if index == width:
            state = tuple(prefix)
            actual = grundy(state)
            predicted = structural_value(state, width, height)
            histogram[actual] += 1
            if actual != predicted:
                mismatches.append((state, actual, predicted))
            return
        for value in range(height + 1):
            new_used = used + min(value, 2)
            if new_used <= CAPACITY:
                prefix.append(value)
                enumerate_states(index + 1, new_used, prefix)
                prefix.pop()

    enumerate_states(0, 0, [])
    return sum(histogram.values()), histogram, mismatches


def enumerate_canonical_states(width, height):
    states = []

    def visit(prefix, largest, used, slots):
        states.append(tuple(prefix))
        if slots == 0:
            return
        for value in range(min(largest, height), 0, -1):
            new_used = used + min(value, 2)
            if new_used <= CAPACITY:
                visit(prefix + [value], value, new_used, slots - 1)

    visit([], height, 0, width)
    return states


def audit_canonical(width, height):
    states = enumerate_canonical_states(width, height)
    values = {}
    for state in sorted(states, key=lambda item: sum(item), reverse=True):
        options = set()
        for index, value in enumerate(state):
            if index and state[index] == state[index - 1]:
                continue
            if value < height:
                child = list(state)
                child[index] += 1
                child = tuple(sorted(child, reverse=True))
                if sum(min(x, 2) for x in child) <= CAPACITY:
                    options.add(values[child])
        if len(state) < width:
            child = tuple(sorted(state + (1,), reverse=True))
            if sum(min(x, 2) for x in child) <= CAPACITY:
                options.add(values[child])
        values[state] = mex(options)

    histogram = Counter(values.values())
    mismatches = []
    for state, actual in values.items():
        predicted = structural_value(state, width, height)
        if actual != predicted:
            mismatches.append((state, actual, predicted))
    return len(states), histogram, mismatches


def main():
    cases = []
    labeled_total = 0
    canonical_total = 0
    labeled_histogram = Counter()
    canonical_histogram = Counter()
    max_table = {}

    for width in range(1, 11):
        row = []
        for height in range(2, 13):
            labeled_count, labeled_hist, labeled_bad = audit_labeled(width, height)
            canonical_count, canonical_hist, canonical_bad = audit_canonical(width, height)
            if labeled_bad or canonical_bad:
                raise SystemExit(
                    f"formula mismatch at width={width}, height={height}: "
                    f"labeled={labeled_bad[:1]}, canonical={canonical_bad[:1]}"
                )
            maximum = max(labeled_hist)
            expected = 3 if width >= 4 and height % 2 else 1
            if maximum != expected:
                raise SystemExit(
                    f"maximum mismatch at width={width}, height={height}: "
                    f"got {maximum}, expected {expected}"
                )
            row.append(maximum)
            labeled_total += labeled_count
            canonical_total += canonical_count
            labeled_histogram.update(labeled_hist)
            canonical_histogram.update(canonical_hist)
            cases.append({
                "width": width,
                "height": height,
                "labeled_states": labeled_count,
                "canonical_states": canonical_count,
                "maximum_grundy": maximum,
                "labeled_mismatches": 0,
                "canonical_mismatches": 0,
            })
        max_table[str(width)] = row

    result = {
        "capacity": CAPACITY,
        "forbidden_points": CAPACITY + 1,
        "scope": {
            "width": "1..10",
            "height": "2..12",
            "parameter_pairs": len(cases),
            "claim": "finite audit only; all-parameter theorem is proved in report.md",
        },
        "labeled_states_total": labeled_total,
        "canonical_states_total": canonical_total,
        "labeled_grundy_histogram": dict(sorted(labeled_histogram.items())),
        "canonical_grundy_histogram": dict(sorted(canonical_histogram.items())),
        "maximum_grundy_by_width_height": max_table,
        "mismatches": 0,
        "cases": cases,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

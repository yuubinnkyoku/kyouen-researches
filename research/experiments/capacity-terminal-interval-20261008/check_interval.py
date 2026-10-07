#!/usr/bin/env python3
"""Exhaustively audit terminal thresholds and binary-Grundy cones in capacity games."""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement

stats = Counter()
for w in range(3, 8):
    for h in range(2, w):
        n = w - h
        for m in range(2, 7):
            for r in range(1, h * m):

                @lru_cache(None)
                def solve(x):
                    children = []
                    for i in range(w):
                        if x[i] == m:
                            continue
                        y = list(x)
                        y[i] += 1
                        y = tuple(sorted(y, reverse=True))
                        if sum(y[:h]) <= r:
                            children.append(solve(y))
                    if not children:
                        return 0, frozenset({x[h - 1]}), 0
                    child_values = {result[0] for result in children}
                    grundy = 0
                    while grundy in child_values:
                        grundy += 1
                    terminal_thresholds = frozenset(
                        t for _, thresholds, _ in children for t in thresholds
                    )
                    max_descendant = max([grundy] + [v[2] for v in children])
                    return grundy, terminal_thresholds, max_descendant

                for asc in combinations_with_replacement(range(m + 1), w):
                    x = asc[::-1]
                    slack = r - sum(x[:h])
                    if slack < 0:
                        continue
                    b = x[h - 1]
                    c = x[:h].count(b)
                    lower_global = max(0, r - (h - 1) * m)
                    lower = max(b, lower_global)
                    upper = max(
                        t for t in range(m + 1)
                        if sum(max(v, t) for v in x[:h]) <= r
                    )
                    actual_grundy, actual_thresholds, max_descendant = solve(x)
                    assert actual_thresholds == frozenset(range(lower, upper + 1)), (
                        "terminal thresholds", w, h, m, r, x, actual_thresholds,
                    )
                    unique = lower == upper
                    local_unique_rule = (
                        slack < c if b >= lower_global
                        else r == h * m - 1 or x[h - 2] == m
                    )
                    assert unique == local_unique_rule, (
                        "unique criterion", w, h, m, r, x,
                    )
                    binary = n % 2 == 0 or unique
                    assert binary == (max_descendant <= 1), (
                        "descendant binary", w, h, m, r, x, max_descendant,
                    )
                    if binary:
                        assert actual_grundy == (r + n * lower - sum(x)) % 2, (
                            "grundy", w, h, m, r, x,
                        )
                        child_values = []
                        for i in range(w):
                            if x[i] == m:
                                continue
                            y = list(x)
                            y[i] += 1
                            y = tuple(sorted(y, reverse=True))
                            if sum(y[:h]) <= r:
                                child_values.append(solve(y)[0])
                        assert all(v == 1 - actual_grundy for v in child_values), (
                            "child values", w, h, m, r, x,
                        )
                        legal_moves = (
                            sum(v < m for v in x)
                            if slack > 0 else sum(v < b for v in x)
                        )
                        assert len(child_values) == legal_moves, (
                            "legal move count", w, h, m, r, x,
                        )
                    stats["positions"] += 1
                    stats["binary"] += binary
                    stats["nonbinary"] += not binary
                    stats["old_criterion_false_negatives"] += unique and slack >= c
print("PASS", dict(stats))

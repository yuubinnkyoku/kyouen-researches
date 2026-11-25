#!/usr/bin/env python3
"""Independent complete enumeration of all slack-one nonbinary witness spectra.

No K0358 formula is used in the mex recursion. All sorted upper-only
slack-one witnesses are enumerated rather than relying on the constructive proof.
"""
from itertools import combinations_with_replacement
from functools import lru_cache
from collections import Counter


def check():
    totals = Counter()
    examples = {}
    for w in range(3, 8):
        for h in range(2, w):
            n = w - h
            if n % 2 == 0:
                continue
            for m in range(2, 6):
                upper_options = [
                    tuple(reversed(v))
                    for v in combinations_with_replacement(range(m + 1), h)
                ]
                for r in range(1, h * m):
                    @lru_cache(None)
                    def grundy(state):
                        child_values = set()
                        for i, v in enumerate(state):
                            if v == m:
                                continue
                            y = list(state)
                            y[i] += 1
                            y.sort(reverse=True)
                            child = tuple(y)
                            if sum(child[:h]) <= r:
                                child_values.add(grundy(child))
                        g = 0
                        while g in child_values:
                            g += 1
                        return g

                    upper = [
                        y for y in upper_options
                        if sum(y) == r - 1 and y[h - 2] > y[h - 1]
                        and y[h - 2] < m
                    ]
                    for asc in combinations_with_replacement(range(m + 1), w):
                        x = tuple(reversed(asc))
                        if sum(x[:h]) > r:
                            continue
                        sigma = r - sum(x[:h])
                        if sigma == 0:
                            continue
                        a = max(x[h - 1], 0, r - (h - 1) * m)
                        b = max(
                            t for t in range(m + 1)
                            if sum(max(v, t) for v in x[:h]) <= r
                        )
                        witnesses = [
                            y for y in upper
                            if all(y[i] >= x[i] for i in range(h))
                        ]
                        observed = {y[-1] for y in witnesses}
                        predicted = set(range(a, b))
                        assert observed == predicted, (w, h, m, r, x, observed, predicted)
                        values = set()
                        for y in witnesses:
                            state = y + x[h:]
                            assert state == tuple(sorted(state, reverse=True))
                            g = grundy(state)
                            expected = 2 + ((n * y[-1] - sum(x[h:])) % 2)
                            assert g == expected, (w, h, m, r, x, state, g, expected)
                            values.add(g)
                            totals["witnesses"] += 1
                        assert values == {
                            2 + ((n * t - sum(x[h:])) % 2) for t in predicted
                        }
                        totals["positions"] += 1
                        totals["interval_width_" + str(min(b - a, 3))] += 1
                        if b - a >= 2 and "both" not in examples:
                            examples["both"] = (w, h, m, r, x, sorted(values), a, b)
                        if b - a == 1 and "single" not in examples:
                            examples["single"] = (w, h, m, r, x, sorted(values), a, b)
    print("PASS", dict(totals))
    print("EXAMPLES", examples)


if __name__ == "__main__":
    check()

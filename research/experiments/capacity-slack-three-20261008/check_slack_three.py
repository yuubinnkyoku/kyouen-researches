#!/usr/bin/env python3
"""Independent exact mex audit of the universal capacity-slack-three formula.

Finite full enumeration: 3<=w<=9, 2<=h<w, 1<=m<=8, 3<=r<h*m.
The predicted Grundy value uses K0359's slack-two closed expression;
the observed value uses a separate recursion through every legal move.
"""
from itertools import combinations_with_replacement
from functools import lru_cache
from collections import Counter


def slack_two_value(y, h, m, n):
    b = y[h - 1]
    R = n * b - sum(y[h:])
    c = sum(v == b for v in y[:h])
    free_upper = sum(m - v for v in y[:h - 1])
    eta = int(c == 1 and
              (y[h - 2] - b == 1 or free_upper == 1))
    return (R + (n % 2) * eta) % 2


def verify():
    counts = Counter()
    examples = {}
    for w in range(3, 10):
        for h in range(2, w):
            n = w - h
            for m in range(1, 9):
                states = [tuple(reversed(z)) for z in
                          combinations_with_replacement(range(m + 1), w)]
                for r in range(3, h * m):
                    @lru_cache(None)
                    def mex_recursive(x):
                        values = set()
                        for i, v in enumerate(x):
                            if v == m or (i and x[i - 1] == v):
                                continue
                            child = list(x)
                            child[i] += 1
                            child.sort(reverse=True)
                            child = tuple(child)
                            if sum(child[:h]) <= r:
                                values.add(mex_recursive(child))
                        answer = 0
                        while answer in values:
                            answer += 1
                        return answer

                    for x in states:
                        if sum(x[:h]) != r - 3:
                            continue
                        b = x[h - 1]
                        R = n * b - sum(x[h:])
                        signatures = set()
                        children = set()
                        for i, v in enumerate(x[:h]):
                            if v == m or (i and x[i - 1] == v):
                                continue
                            y = list(x)
                            y[i] += 1
                            y.sort(reverse=True)
                            y = tuple(y)
                            assert sum(y[:h]) == r - 2
                            predicted_child = slack_two_value(y, h, m, n)
                            signatures.add((predicted_child - R) % 2)
                            children.add(predicted_child)
                            assert mex_recursive(y) == predicted_child

                        assert signatures
                        assert children == {(R + e) % 2 for e in signatures}
                        if len(signatures) == 1:
                            predicted = (1 + R + next(iter(signatures))) % 2
                        else:
                            predicted = 2 + (R % 2)
                        observed = mex_recursive(x)
                        assert observed == predicted, (
                            w, h, m, r, x, signatures, observed, predicted
                        )
                        counts["positions"] += 1
                        counts["odd_n" if n % 2 else "even_n"] += 1
                        counts["mixed" if len(signatures) == 2 else "single"] += 1
                        counts["g" + str(observed)] += 1
                        if len(signatures) == 2 and "g" + str(observed) not in examples:
                            examples["g" + str(observed)] = (w, h, m, r, x, R)

    print("PASS", dict(counts))
    print("EXAMPLES", examples)


if __name__ == "__main__":
    verify()

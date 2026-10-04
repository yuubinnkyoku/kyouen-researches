#!/usr/bin/env python3
"""Independent full labeled mex versus the new two-coordinate kernel.

Labeled DP sees every coordinate and checks all pairs after each move.
No sorted-state quotient or proposed formula is used to obtain its mex.
Assertions are required, including for complete finite coverage receipts.
"""
import argparse
from collections import Counter
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

from kernel import capped_gap_formula, grundy, mex, pair_table, root_grundy

if not __debug__:
    raise SystemExit('Exact validation requires assertions; do not use -O.')


def labeled_audit(w, m, r):
    table = pair_table(m, r)
    histogram = Counter()

    @lru_cache(None)
    def labeled(x):
        options = set()
        for i in range(w):
            if x[i] >= m:
                continue
            y = x[:i] + (x[i]+1,) + x[i+1:]
            if any(y[j]+y[k] > r for j in range(w) for k in range(j)):
                continue
            options.add(labeled(y))
        value = mex(options)
        predicted = grundy(x, m, r, table)
        assert value == predicted, (w, m, r, x, value, predicted)
        assert value <= 3
        histogram[value] += 1
        a = max(x)
        if 2*a > r:
            largest = x.index(a)
            y = [r-a-count for i, count in enumerate(x) if i != largest]
            assert value == capped_gap_formula(y, m-a), (w, m, r, x, value)
        return value

    root = labeled((0,)*w)
    assert root == root_grundy(w, m, r), (w, m, r, root)
    assert labeled.cache_info().currsize == sum(histogram.values()) > 0
    # Downward closure ensures every legal vector is reachable from zero.
    # Separately count all labeled safe vectors by largest-count category.
    k = min(m, r//2)
    complete_count = (k+1)**w
    for a in range(k+1, min(m, r)+1):
        complete_count += w*(r-a+1)**(w-1)
    assert complete_count == labeled.cache_info().currsize
    return dict(w=w, m=m, r=r, pair_table_entries=len(table),
                full_labeled_safe_states=complete_count, root_grundy=root,
                grundy_histogram=dict(sorted(histogram.items())),
                all_values_kernel_matched=True,
                all_dominant_values_capped_gap_matched=True)


def gap_audit(n, largest, budget_limit):
    @lru_cache(None)
    def direct(y, budget):
        options = {direct(y[:i]+(v-1,)+y[i+1:], budget)
                   for i, v in enumerate(y) if v}
        if budget and min(y):
            options.add(direct(tuple(v-1 for v in y), budget-1))
        value = mex(options)
        assert value == capped_gap_formula(y, budget), (n, y, budget, value)
        return value

    for y in product(range(largest+1), repeat=n):
        for budget in range(budget_limit+1):
            direct(y, budget)
    expected = (largest+1)**n*(budget_limit+1)
    assert direct.cache_info().currsize == expected
    return dict(n=n, maximum_gap=largest, maximum_budget=budget_limit,
                full_labeled_states=expected, all_formula_matched=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('verified.json'))
    args = parser.parse_args()
    # Abstract parameters outside q>2w are intentional. They exercise the
    # occupancy theorem broadly, without claiming a geometric interpretation.
    audits = [labeled_audit(w, m, r)
              for w, limit in [(3, 14), (5, 10), (7, 7)]
              for r in range(limit+1) for m in range(1, r+3)]
    gaps = [gap_audit(2, 12, 13), gap_audit(4, 6, 7), gap_audit(6, 3, 4)]
    assert grundy((4, 1, 0), 4, 6) == 1
    assert grundy((4, 1, 0), 7, 6) == 3
    output = dict(
        universal_evidence='Mathematical mex induction in proof.md; these complete finite audits verify implementations.',
        scope='Odd w>=3 abstract pair-cap occupancy game, all nonnegative r and finite m; prism transfer additionally requires K0340 hypotheses.',
        labeled_occupancy_audits=audits, capped_gap_audits=gaps,
        total_labeled_occupancy_states=sum(a['full_labeled_safe_states'] for a in audits),
        total_labeled_gap_states=sum(a['full_labeled_states'] for a in gaps),
        short_board_counterexample=dict(w=3, r=6, x=[4, 1, 0],
                                        short_m=4, short_grundy=1,
                                        long_m=7, long_grundy=3))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(occupancy_audits=len(audits),
                          labeled_states=output['total_labeled_occupancy_states'],
                          gap_states=output['total_labeled_gap_states'],
                          output=str(args.output)), ensure_ascii=False))


if __name__ == '__main__':
    main()

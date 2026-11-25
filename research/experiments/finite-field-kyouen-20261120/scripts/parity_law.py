"""Test the parity hypothesis directly.

Observation: all 41 counterexamples have maximal sizes with the SAME parity
(spread 2, e.g. {3,5}).  Boards with spread 1 (different parity) have zero
counterexamples.

HYPOTHESIS: if all maximal sets have the same parity, then max Grundy <= 1.

But we saw 3,409 boards with spread 2 and max Grundy >= 2.  So the hypothesis
is FALSE as stated.

Let me test a REFINED hypothesis:

REFINED: if all maximal sets have the same parity AND the number of maximal
sets is small, then max Grundy <= 1.

Or better: let me look for the exact condition by computing, for each board,
the "parity-consistency" of the Grundy function.

Actually, let me test a cleaner statement:

CLAIM: g(S) = (T - |S|) mod 2 for all S  <=>  all maximal sets have size T.

We know => holds.  The converse fails (41 counterexamples).  But maybe:

CLAIM': if all maximal sets have the same parity, then g(S) mod 2 = (T - |S|) mod 2
for all S?  I.e., the PARITY of the Grundy value is determined even if the value
itself is not.

Let me test this!  This would be a nice weak form of the theorem.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def analyse(n: int, edges: list[tuple[int, ...]]):
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, e in enumerate(edges):
        for i in e:
            through[i].append(bi)

    def can_add(i: int, pmask: int) -> bool:
        for bi in through[i]:
            cnt = 0
            for j in edges[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= 3:
                        return False
        return True

    by_size: dict[int, list[int]] = defaultdict(list)
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size[pmask.bit_count()].append(pmask)
        for i in range(start, n):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                stack.append((i + 1, pmask | (1 << i)))

    g: dict[int, int] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            reach = set()
            for i in range(n):
                if pmask >> i & 1:
                    continue
                if can_add(i, pmask):
                    reach.add(g[pmask | (1 << i)])
            m = 0
            while m in reach:
                m += 1
            g[pmask] = m

    maximal_sizes = Counter()
    for size in by_size:
        for pmask in by_size[size]:
            if all(pmask >> i & 1 or not can_add(i, pmask) for i in range(n)):
                maximal_sizes[size] += 1

    sizes = sorted(maximal_sizes)
    same_parity = len({s % 2 for s in sizes}) == 1
    T = sizes[0] if same_parity else None

    # test: g(S) mod 2 == (T - |S|) mod 2 for all S?
    parity_ok = True
    if same_parity:
        for pmask, val in g.items():
            if val % 2 != (T - pmask.bit_count()) % 2:
                parity_ok = False
                break

    return {
        "n": n,
        "edges": len(edges),
        "maximal_sizes": dict(sorted(maximal_sizes.items())),
        "same_parity": same_parity,
        "T": T,
        "max_grundy": max(g.values()),
        "parity_law_holds": parity_ok,
        "uniform": len(sizes) == 1,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    n = args.n
    all_edges = list(itertools.combinations(range(n), 4))
    total = 1 << len(all_edges)
    print(f"n={n}: {total} hypergraphs", flush=True)

    same_parity_boards = []
    diff_parity_boards = []
    for mask in range(total):
        edges = [all_edges[i] for i in range(len(all_edges)) if mask >> i & 1]
        if not edges:
            continue
        r = analyse(n, edges)
        r["mask"] = mask
        if r["same_parity"]:
            same_parity_boards.append(r)
        else:
            diff_parity_boards.append(r)

    print(f"same parity: {len(same_parity_boards)}, "
          f"different parity: {len(diff_parity_boards)}", flush=True)
    print()
    print("PARITY LAW TEST: g(S) mod 2 == (T - |S|) mod 2 when all maximal "
          "sizes have the same parity")
    ok = [r for r in same_parity_boards if r["parity_law_holds"]]
    bad = [r for r in same_parity_boards if not r["parity_law_holds"]]
    print(f"  holds: {len(ok)}, fails: {len(bad)}")
    if bad:
        print("  failures (first 5):")
        for r in bad[:5]:
            print(f"    mask={r['mask']} maximal={r['maximal_sizes']} "
                  f"maxg={r['max_grundy']}")

    print()
    print("max Grundy distribution among same-parity boards:")
    print(f"  {dict(sorted(Counter(r['max_grundy'] for r in same_parity_boards).items()))}")
    print("max Grundy distribution among different-parity boards:")
    print(f"  {dict(sorted(Counter(r['max_grundy'] for r in diff_parity_boards).items()))}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "n": n,
            "same_parity": len(same_parity_boards),
            "diff_parity": len(diff_parity_boards),
            "parity_law_holds": len(ok),
            "parity_law_fails": len(bad),
            "failures": bad[:20],
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

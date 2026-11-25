"""What distinguishes the 41 counterexamples from the other non-uniform boards?

The converse failed: 41 of 28,815 non-uniform n=6 hypergraphs have max Grundy 1.

Question: what structural property separates them?

Hypotheses to test:
  (H1) The maximal sizes are "close" (e.g., differ by 2, not more).
  (H2) The number of maximal sets is small.
  (H3) The game tree has a special "layered" structure.
  (H4) The position set is "thin" (few safe sets).

Let me compute, for each n=6 hypergraph, a set of features and compare the
41 counterexamples against the rest.
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
    return {
        "n": n,
        "edges": len(edges),
        "safe_sets": sum(len(v) for v in by_size.values()),
        "maximal_sizes": dict(sorted(maximal_sizes.items())),
        "num_maximal": sum(maximal_sizes.values()),
        "num_distinct_sizes": len(sizes),
        "spread": sizes[-1] - sizes[0] if sizes else 0,
        "uniform": len(sizes) == 1,
        "max_grundy": max(g.values()),
        "grundy_distribution": dict(sorted(Counter(g.values()).items())),
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

    counter = []   # non-uniform, max g <= 1
    normal = []    # non-uniform, max g >= 2
    uniform = []
    for mask in range(total):
        edges = [all_edges[i] for i in range(len(all_edges)) if mask >> i & 1]
        if not edges:
            continue
        r = analyse(n, edges)
        r["mask"] = mask
        if r["uniform"]:
            uniform.append(r)
        elif r["max_grundy"] <= 1:
            counter.append(r)
        else:
            normal.append(r)

    print(f"uniform: {len(uniform)}, counterexamples: {len(counter)}, "
          f"normal non-uniform: {len(normal)}", flush=True)

    def summarize(name, rows):
        if not rows:
            return
        spreads = Counter(r["spread"] for r in rows)
        ndist = Counter(r["num_distinct_sizes"] for r in rows)
        nmax = Counter(r["num_maximal"] for r in rows)
        safe = Counter(r["safe_sets"] for r in rows)
        print(f"\n{name} ({len(rows)}):")
        print(f"  spread distribution: {dict(sorted(spreads.items()))}")
        print(f"  #distinct sizes: {dict(sorted(ndist.items()))}")
        print(f"  #maximal sets (top 5): {nmax.most_common(5)}")
        print(f"  safe sets (top 5): {safe.most_common(5)}")

    summarize("COUNTEREXAMPLES (non-uniform, max g <= 1)", counter)
    summarize("NORMAL non-uniform (max g >= 2)", normal)

    print()
    print("counterexample details:")
    for c in counter[:15]:
        print(f"  mask={c['mask']} edges={c['edges']} "
              f"maximal={c['maximal_sizes']} safe={c['safe_sets']} "
              f"gdist={c['grundy_distribution']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "n": n,
            "uniform": len(uniform),
            "counterexamples": counter,
            "normal_nonuniform": len(normal),
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

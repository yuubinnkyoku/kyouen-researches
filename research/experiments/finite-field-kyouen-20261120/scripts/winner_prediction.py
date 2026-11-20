"""Can we predict the winner of a NON-uniform board?

For uniform boards, g(empty) = K mod 2 (proved).

For non-uniform boards, the parity law does not apply.  But maybe there is a
different invariant.

Let me look at the data:
  inversive q=5: maximal {5,6}, g(empty)=1
  AG(2,5): maximal {3,5,6}, g(empty)=1
  4x4 integer: maximal {5,6,7}, g(empty)=0
  5x5 integer: maximal {5..9}, g(empty)=1

Hypothesis candidates:
  (H1) g(empty) = (number of maximal sets of even size) mod 2?
  (H2) g(empty) = (minimal maximal size) mod 2?
  (H3) g(empty) = (number of distinct maximal sizes) mod 2?
  (H4) g(empty) = 0 iff some maximal set has even size?

Let me test these on the data and on random hypergraphs.

Actually, let me think structurally.  The parity law says: if all maximal sets
have the same parity, g <= 1 and g(S) = (eps-|S|) mod 2.

If maximal sets have both parities, then g can be >= 2.  But what is g(empty)?

Let me test H4: g(empty) = 0 iff there is a maximal set of even size?
  inversive q=5: maximal {5,6}, has even (6) -> predict g=0.  Actual 1.  FAILS.

H2: g(empty) = (min maximal size) mod 2?
  inversive q=5: min=5 odd -> predict 1.  Actual 1.  OK.
  AG(2,5): min=3 odd -> predict 1.  Actual 1.  OK.
  4x4: min=5 odd -> predict 1.  Actual 0.  FAILS.

H3: g(empty) = (#distinct sizes) mod 2?
  inversive q=5: 2 -> predict 0.  Actual 1.  FAILS.

Let me just test on random hypergraphs which simple invariant predicts g(empty).

Actually, a cleaner approach: let me compute, for each board, the "Grundy value
of the empty position" and see if it correlates with anything simple.

Let me test on the n=6 exhaustive data: for each hypergraph, compute g(empty)
and various invariants, and look for a pattern.
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
        "maximal_sizes": dict(sorted(maximal_sizes.items())),
        "num_maximal": sum(maximal_sizes.values()),
        "num_sizes": len(sizes),
        "min_size": sizes[0],
        "max_size": sizes[-1],
        "same_parity": len({s % 2 for s in sizes}) == 1,
        "g_empty": g[0],
        "max_grundy": max(g.values()),
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

    rows = []
    for mask in range(total):
        edges = [all_edges[i] for i in range(len(all_edges)) if mask >> i & 1]
        if not edges:
            continue
        r = analyse(n, edges)
        r["mask"] = mask
        rows.append(r)

    nonuniform = [r for r in rows if not r["same_parity"]]
    print(f"non-uniform boards: {len(nonuniform)}")
    print()

    # test candidate invariants
    def test(name, fn):
        ok = sum(1 for r in nonuniform if fn(r) == r["g_empty"])
        print(f"  {name}: {ok}/{len(nonuniform)} correct "
              f"({100*ok/len(nonuniform):.1f}%)")

    print("candidate predictors for g(empty) on non-uniform boards:")
    test("min_size mod 2", lambda r: r["min_size"] % 2)
    test("max_size mod 2", lambda r: r["max_size"] % 2)
    test("num_sizes mod 2", lambda r: r["num_sizes"] % 2)
    test("num_maximal mod 2", lambda r: r["num_maximal"] % 2)
    test("always 0", lambda r: 0)
    test("always 1", lambda r: 1)

    print()
    print("g(empty) distribution on non-uniform boards:")
    print(f"  {dict(sorted(Counter(r['g_empty'] for r in nonuniform).items()))}")
    print()
    print("g(empty) vs (min_size, max_size):")
    cross = Counter((r["min_size"], r["max_size"], r["g_empty"]) for r in nonuniform)
    for (a, b, gv), cnt in sorted(cross.items())[:20]:
        print(f"  min={a} max={b}: g(empty)={gv} ({cnt} boards)")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "n": n,
            "nonuniform": len(nonuniform),
            "g_empty_distribution": dict(sorted(Counter(r["g_empty"] for r in nonuniform).items())),
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

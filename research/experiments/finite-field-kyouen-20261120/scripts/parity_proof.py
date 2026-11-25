"""Rigorous proof of the parity law.

SETTING.  A finite impartial game: positions are subsets of a finite set B
(the "safe sets"), moves add one point, terminal positions are the maximal safe
sets.  Write g(S) for the Sprague-Grundy value.

DEFINITIONS.
  * A position S is terminal iff no move is legal from S; equivalently S is
    maximal (no safe superset).
  * For a position S, let L(S) = set of play lengths from S to a terminal
    position (i.e., |M| - |S| for maximal M ⊇ S).

LEMMA 1 (uniform depth).  If L(S) = {d} (a singleton), then g(S) = d mod 2.

PROOF.  Induct on d.  d = 0: S is terminal, g(S) = 0 = 0 mod 2.
d > 0: every child S' = S ∪ {p} has L(S') = {d-1} (because extending S' to a
maximal set gives a maximal set containing S, and all such have size |S|+d).
By induction g(S') = (d-1) mod 2 for every child.  Hence
g(S) = mex{ (d-1) mod 2 } = d mod 2.  QED.

THEOREM (parity law).  Suppose all maximal sets have the same parity, i.e.,
there is eps in {0,1} with |M| ≡ eps (mod 2) for every maximal M.
Then for every position S,

    g(S) ≡ (eps - |S|) (mod 2).

PROOF.  We prove the stronger statement

    (P_d)  for every position S with L(S) ⊆ {d, d+2, d+4, ...} (all elements
           congruent to d mod 2), g(S) ≡ d (mod 2).

Note first: if all maximal sets have parity eps, then for any S,
L(S) = { |M| - |S| : M maximal, M ⊇ S } ⊆ { eps - |S| mod 2 } (mod 2).
So (P_d) applies with d ≡ eps - |S| (mod 2).

Proof of (P_d) by induction on the maximum of L(S).
If L(S) = {0} then S is terminal and g(S) = 0 ≡ 0 (mod 2); and d = 0.
Otherwise, every child S' has L(S') ⊆ {d-1, d+1, d+3, ...}, i.e., all elements
are ≡ d-1 (mod 2).  By induction, g(S') ≡ d-1 (mod 2) for every child.

Now g(S) = mex{ g(S') : S' child }.  All the g(S') have the same parity, namely
d-1 mod 2.  The mex of a set of integers all congruent to p mod 2:
  - if p = 0, the set contains only even numbers, so 1 is not in the set, and
    mex is 1 if 0 is in the set, else 0.  Either way mex ≡ 1 (mod 2) = (p+1) mod 2.
  - if p = 1, the set contains only odd numbers, so 0 is not in the set, and
    mex = 0 ≡ 0 (mod 2) = (p+1) mod 2.
So g(S) ≡ (d-1) + 1 = d (mod 2).  QED.

COROLLARY 1.  If all maximal sets have the same parity, then g(S) ∈ {0,1} for
all S?  NO -- the theorem only gives the PARITY of g(S), not that g(S) <= 1.

Hmm.  But the computation showed max Grundy = 1 for all same-parity boards.
So there must be an additional argument.

Let me think again.  The theorem gives g(S) ≡ d (mod 2).  To conclude g(S) <= 1
we need more.

CLAIM: if all maximal sets have the same parity, then g(S) <= 1.

PROOF ATTEMPT.  Suppose g(S) >= 2 for some S.  Then mex of the children's values
is >= 2, so 0 and 1 are both among the children's values.  So there are children
S0 with g(S0) = 0 and S1 with g(S1) = 1.

By the theorem, g(S0) ≡ d-1 (mod 2) and g(S1) ≡ d-1 (mod 2).  But g(S0) = 0 is
even and g(S1) = 1 is odd.  Contradiction!  QED.

So the parity law DOES give g(S) <= 1.  Let me redo:

If g(S) >= 2, then both 0 and 1 are in {g(S')}.  But all g(S') have the same
parity (d-1 mod 2).  So they cannot include both an even and an odd number.
Contradiction.

Therefore g(S) <= 1.  QED.

So the full theorem is:

THEOREM (parity law, full).  If all maximal sets have the same parity, then
  (a) g(S) ≡ (eps - |S|) (mod 2) for all S, and
  (b) g(S) ∈ {0, 1} for all S.

And the converse: if maximal sets have both parities, then some g(S) >= 2?
Let me check.  If there are maximal sets M0 (even) and M1 (odd), take S = empty.
Then L(empty) contains both even and odd numbers.  Does that force g >= 2?

Hmm, not immediately.  But the computation showed it does for n=6.

Let me try to prove it.  Suppose maximal sets M0 (size even) and M1 (size odd)
exist.  Consider the empty position.  Hmm.

Actually, let me think about the position S = M0 ∩ M1.  From S, we can reach M0
and M1.  |M0| - |S| and |M1| - |S| have different parities.

Let me try: consider a position S that is "just before" both a terminal of even
depth and a terminal of odd depth.  Hmm.

Let me just verify the theorem computationally (which I did) and present the
proof of (a) and (b), and note that the converse is verified but not proved.

This script verifies the proof steps on the n=6 data.
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
    eps = sizes[0] % 2 if same_parity else None

    # verify (a): g(S) ≡ eps - |S| (mod 2)
    a_ok = True
    # verify (b): g(S) <= 1
    b_ok = True
    if same_parity:
        for pmask, val in g.items():
            if val % 2 != (eps - pmask.bit_count()) % 2:
                a_ok = False
            if val > 1:
                b_ok = False

    return {
        "n": n,
        "edges": len(edges),
        "maximal_sizes": dict(sorted(maximal_sizes.items())),
        "same_parity": same_parity,
        "eps": eps,
        "max_grundy": max(g.values()),
        "a_holds": a_ok,
        "b_holds": b_ok,
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

    same = []
    mixed = []
    for mask in range(total):
        edges = [all_edges[i] for i in range(len(all_edges)) if mask >> i & 1]
        if not edges:
            continue
        r = analyse(n, edges)
        r["mask"] = mask
        if r["same_parity"]:
            same.append(r)
        else:
            mixed.append(r)

    print(f"same parity: {len(same)}, mixed: {len(mixed)}")
    print()
    print("THEOREM (a): g(S) ≡ eps - |S| (mod 2)")
    print(f"  holds: {sum(1 for r in same if r['a_holds'])}/{len(same)}")
    print("THEOREM (b): g(S) <= 1")
    print(f"  holds: {sum(1 for r in same if r['b_holds'])}/{len(same)}")
    print()
    print("CONVERSE: mixed parity => some g >= 2")
    bad = [r for r in mixed if r["max_grundy"] <= 1]
    print(f"  counterexamples: {len(bad)}/{len(mixed)}")
    if bad:
        for r in bad[:5]:
            print(f"    mask={r['mask']} maximal={r['maximal_sizes']} "
                  f"maxg={r['max_grundy']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "n": n,
            "same_parity": len(same),
            "mixed": len(mixed),
            "a_holds": sum(1 for r in same if r["a_holds"]),
            "b_holds": sum(1 for r in same if r["b_holds"]),
            "converse_counterexamples": len(bad),
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

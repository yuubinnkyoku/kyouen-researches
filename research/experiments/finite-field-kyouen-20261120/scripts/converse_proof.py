"""Attempt to PROVE the converse of the parity law.

THEOREM (proved).  If all maximal sets have the same parity eps, then
  (a) g(S) ≡ eps - |S| (mod 2), and
  (b) g(S) <= 1.

CONVERSE (to prove).  If maximal sets have both parities, then some position
has g(S) >= 2.

PROOF ATTEMPT.

Let M0, M1 be maximal with |M0| even and |M1| odd.

Consider the position S = M0 ∩ M1.  From S we can reach M0 (adding M0 \ S) and
M1 (adding M1 \ S).  The play lengths are |M0| - |S| and |M1| - |S|, which have
different parities.

Hmm, that alone does not give g >= 2.

Let me think differently.  Consider the position S = empty.  L(empty) contains
both parities.  Does that force g(empty) >= 2?  No: consider a game where the
empty position has children of Grundy 0 and 1 only.  Then g(empty) = 2.  Hmm,
that IS >= 2.

Let me think about what "both parities in L(S)" implies.

CLAIM: if L(S) contains both an even and an odd number, then g(S) >= 2.

PROOF ATTEMPT by induction on max L(S).

Base: if L(S) = {0, 1}, then S has a child that is terminal (g=0) and a child
with L = {0} (g=0)... hmm, that gives g(S) = mex{0} = 1, not 2.

Wait.  If L(S) = {0,1}, then S is NOT terminal (since 1 in L(S) means there is
a maximal set of size |S|+1, so S has a legal move).  Children S' have
L(S') ⊆ {0} or {1}... hmm, L(S') = {d-1 : d in L(S)} = {0} if 1 in L(S) and
the child leads to a maximal set of size |S|+1.

Hmm, let me be careful.  If L(S) = {0,1}, then S itself is maximal (0 in L(S)
means S is maximal).  But if S is maximal, L(S) = {0} only.  Contradiction.
So L(S) = {0,1} is impossible.

Good.  So if S is maximal, L(S) = {0}.

Now suppose L(S) contains both parities and S is not maximal.  Then L(S) has
at least two elements of different parity, so max L(S) >= 1 and there is an
element >= 1.

Children S' = S ∪ {p}.  L(S') = {d-1 : d in L(S), d >= 1}?  No: L(S') = {|M| - |S'| : M maximal, M ⊇ S'} = {d - 1 : d in L(S), and the maximal set M with |M|-|S| = d contains S'}.  So L(S') ⊆ {d-1 : d in L(S)}.

Hmm, so L(S') can be a proper subset.

Let me try a cleaner approach: use the "height" function h(S) = max L(S) and
the "min height" m(S) = min L(S).

CLAIM: if m(S) < h(S), then g(S) >= 2?  Let me test computationally.

Actually, let me test the specific claim: is it true that
  (both parities in L(S)) => g(S) >= 2?
for all S, not just the empty position?

Let me check computationally on the n=6 data.
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

    maximal = set()
    for size in by_size:
        for pmask in by_size[size]:
            if all(pmask >> i & 1 or not can_add(i, pmask) for i in range(n)):
                maximal.add(pmask)

    # for each position, compute L(S) parities
    # L(S) = {|M| - |S| : M maximal, M ⊇ S}
    # We compute by: for each maximal M, for each subset S of M that is safe,
    # add |M|-|S| to L(S).  That is expensive; instead compute recursively.
    # L(S) = {0} if S maximal, else union over children of {d+1 : d in L(S')}.
    L: dict[int, set] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            if pmask in maximal:
                L[pmask] = {0}
            else:
                s = set()
                for i in range(n):
                    if pmask >> i & 1:
                        continue
                    if can_add(i, pmask):
                        for d in L[pmask | (1 << i)]:
                            s.add(d + 1)
                L[pmask] = s

    # test: both parities in L(S) => g(S) >= 2
    violations = 0
    examples = []
    for pmask, ls in L.items():
        parities = {d % 2 for d in ls}
        if len(parities) == 2 and g[pmask] <= 1:
            violations += 1
            if len(examples) < 5:
                examples.append({
                    "mask": pmask,
                    "L": sorted(ls),
                    "g": g[pmask],
                })
    return {
        "n": n,
        "edges": len(edges),
        "positions": len(L),
        "violations": violations,
        "examples": examples,
        "max_grundy": max(g.values()),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--limit", type=int, default=2000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    n = args.n
    all_edges = list(itertools.combinations(range(n), 4))
    total = 1 << len(all_edges)
    print(f"n={n}: {total} hypergraphs, sampling {args.limit}", flush=True)

    total_viol = 0
    checked = 0
    all_examples = []
    for mask in range(min(total, args.limit)):
        edges = [all_edges[i] for i in range(len(all_edges)) if mask >> i & 1]
        if not edges:
            continue
        r = analyse(n, edges)
        checked += 1
        total_viol += r["violations"]
        all_examples.extend(r["examples"])

    print(f"checked {checked} hypergraphs")
    print(f"VIOLATIONS of 'both parities in L(S) => g(S) >= 2': {total_viol}")
    for e in all_examples[:10]:
        print(f"  L={e['L']} g={e['g']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "n": n,
            "checked": checked,
            "violations": total_viol,
            "examples": all_examples[:20],
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

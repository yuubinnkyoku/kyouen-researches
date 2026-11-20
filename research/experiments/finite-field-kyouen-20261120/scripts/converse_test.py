"""Is the triviality theorem's converse true?

Theorem (proved): uniform maximal sets => g(S) = (T-|S|) mod 2, so max g <= 1.

Converse candidate: max g <= 1 => uniform maximal sets?

If true, "max Grundy <= 1" and "uniform maximal sets" are equivalent, which
would be a clean characterisation.

Let me look for a counterexample: a board with non-uniform maximal sets but
max Grundy = 1.

From the data:
  inversive q=5: maximal {5,6}, max g = 2.  Not a counterexample.
  AG(2,5): maximal {3,5,6}, max g = 2.  Not a counterexample.
  4x4: maximal {5,6,7}, max g = 5.
  5x5: maximal {5..9}, max g = 6.

So all non-uniform boards found have max g >= 2.  But that is only 4 boards.

Let me construct a test: take a board and REMOVE some blocks so that maximal
sets become non-uniform, then check whether max g stays 1.

Actually, a cleaner test: consider a board where the game is a disjoint sum of
two components with different "heights".  Then maximal sets have different
sizes, but the Grundy value could still be small.

Let me test on the inversive plane q=5 with one circle removed, etc.

Actually, let me think about it theoretically.

CLAIM: if max g <= 1, then all maximal sets have the same size.

PROOF ATTEMPT.  Suppose S is maximal with |S| = s.  Then g(S) = 0.
Suppose S' is maximal with |S'| = s' > s.  Consider a position T on a path from
the empty set to S' ... hmm, this does not immediately give a contradiction.

Counterexample attempt: a game that is a disjoint sum of a path of length 1 and
a path of length 2.  Positions: (0,0), (1,0), (0,1), (0,2), (1,1), (1,2).
Maximal: (1,0) [size 1], (0,2) [size 2], (1,2) [size 3].  Non-uniform.
Grundy: g(1,2)=0, g(1,1)=mex{g(1,2)}=1, g(0,2)=0, g(0,1)=mex{g(0,2)}=1,
g(1,0)=0, g(0,0)=mex{g(1,0),g(0,1)}=mex{0,1}=2.
So max g = 2.  Consistent with the conjecture.

Another: disjoint sum of two paths of length 1.  Maximal: (1,1) only, size 2.
Uniform.  g(0,0)=mex{g(1,0),g(0,1)}=mex{1,1}=0.  Max g=1.  Consistent.

Another: a single path of length 3.  Maximal: size 3 only.  Uniform.  g = 3 mod 2.
Max g = 1.  Consistent.

Hmm, so far consistent.  Let me try to PROVE the converse.

CLAIM: if all maximal sets have size T, then g = (T-|S|) mod 2.  (proved)
CONVERSE: if some two maximal sets have different sizes, then some position has
g >= 2.

PROOF ATTEMPT.  Let A, B be maximal with |A| = a < b = |B|.
Consider the game tree.  Hmm.

Let me think about it via the "height" function.  Define h(S) = the set of
possible play lengths from S.  If all maximal sets have size T, then h(S) = {T-|S|}
(singleton).  If not, h(S) can have multiple values.

CLAIM: if h(S) has two values differing by >= 2, then g(S) >= 2?  Not obviously.

Let me just test computationally on many small boards (including artificial ones)
to see whether the converse holds.

I'll generate random hypergraph games (not necessarily geometric) and check.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path


def analyse_hypergraph(n: int, edges: list[tuple[int, ...]]):
    """Game: place points, no edge fully contained.  Max 3 per edge assumed."""
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

    return {
        "n": n,
        "edges": len(edges),
        "maximal_sizes": dict(sorted(maximal_sizes.items())),
        "uniform": len(maximal_sizes) == 1,
        "max_grundy": max(g.values()),
        "grundy_distribution": dict(sorted(Counter(g.values()).items())),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20261120)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = []
    counterexamples = []

    for trial in range(args.trials):
        n = rng.randint(4, 8)
        # random 4-uniform hypergraph
        all_edges = list(itertools.combinations(range(n), 4))
        m = rng.randint(1, min(len(all_edges), 12))
        edges = rng.sample(all_edges, m)
        r = analyse_hypergraph(n, edges)
        r["trial"] = trial
        rows.append(r)
        # check the converse: non-uniform => max g >= 2
        if not r["uniform"] and r["max_grundy"] <= 1:
            counterexamples.append(r)

    print(f"trials: {len(rows)}")
    uniform = [r for r in rows if r["uniform"]]
    nonuniform = [r for r in rows if not r["uniform"]]
    print(f"  uniform: {len(uniform)}")
    print(f"  non-uniform: {len(nonuniform)}")
    print()
    print("uniform boards: max Grundy distribution")
    print(f"  {dict(sorted(Counter(r['max_grundy'] for r in uniform).items()))}")
    print("non-uniform boards: max Grundy distribution")
    print(f"  {dict(sorted(Counter(r['max_grundy'] for r in nonuniform).items()))}")
    print()
    print(f"COUNTEREXAMPLES to the converse (non-uniform but max g <= 1): "
          f"{len(counterexamples)}")
    for c in counterexamples[:5]:
        print(f"  n={c['n']} edges={c['edges']} maximal={c['maximal_sizes']} "
              f"gdist={c['grundy_distribution']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "trials": len(rows),
            "uniform": len(uniform),
            "nonuniform": len(nonuniform),
            "counterexamples": counterexamples,
            "rows": rows,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

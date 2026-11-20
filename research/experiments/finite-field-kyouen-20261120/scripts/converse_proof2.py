"""The converse needs a sharper condition.

Test showed: "both parities in L(S)" does NOT imply g(S) >= 2.
Counterexamples: L=[2,3] with g=1, L=[3,4] with g=0.

So the converse of the parity law must be about the WHOLE board, not a single
position.

Let me look for the right condition.  The parity law says:
  all maximal sizes same parity => g(S) <= 1 for all S.

The converse would be:
  some g(S) >= 2 => maximal sizes have both parities.

Let me test the contrapositive directly: is there a board with all maximal sizes
same parity but some g >= 2?  (We know: no, 4018/4018.)

And: is there a board with mixed parity but all g <= 1?  (We know: no, 0/28749.)

So the equivalence holds at the BOARD level.  The proof must use the board-level
structure, not a single position.

Let me think about why.

Suppose all maximal sizes have the same parity eps.  Then by the proved theorem,
g(S) <= 1 for all S.  Done.

Conversely, suppose some g(S) >= 2.  Then by the contrapositive of the theorem,
maximal sizes do NOT all have the same parity.  Done!

Wait -- that IS the converse, and it follows immediately from the theorem!

THEOREM: (all maximal sizes same parity) => (all g <= 1).
CONTRAPOSITIVE: (some g >= 2) => (maximal sizes have both parities).

That is logically identical!  So the converse is PROVED, not just observed.

Let me double-check: the theorem says
  P => Q, where P = "all maximal sizes same parity", Q = "all g(S) <= 1".
The contrapositive is
  not Q => not P, i.e., "some g(S) >= 2" => "maximal sizes have both parities".

Yes!  The contrapositive is logically equivalent to the theorem.  So the
"converse" I was trying to prove is just the contrapositive, which is
automatically true.

Hmm, but wait.  Is that the converse?  The converse of P => Q is Q => P.
Q => P is "all g <= 1" => "all maximal sizes same parity".
The contrapositive of Q => P is "not P => not Q" = "mixed parity => some g >= 2".

So "mixed parity => some g >= 2" is the contrapositive of "all g <= 1 => all
maximal sizes same parity", which is the CONVERSE of the theorem.

So to prove "mixed parity => some g >= 2", I need to prove "all g <= 1 => all
maximal sizes same parity", which is NOT automatic.

Let me redo.  The theorem is P => Q.  Its contrapositive (not Q => not P) is
equivalent.  The CONVERSE (Q => P) is a different statement.

What I verified computationally is:
  P => Q  (4018/4018)  -- proved
  not P => not Q  (28749/28749)  -- this is the contrapositive of Q => P

So "not P => not Q" is what I need to prove, and it is equivalent to "Q => P".

Let me try to prove Q => P: if all g(S) <= 1, then all maximal sizes have the
same parity.

PROOF ATTEMPT.  Suppose all g(S) <= 1.  Let M be maximal.  g(M) = 0.

Consider a position S with a move to M.  Then g(S) = mex{..., 0, ...} >= 1.
Since g(S) <= 1, g(S) = 1.  So every predecessor of a maximal set has g = 1.

Now consider a maximal set M' with |M'| = |M| + 1 (different parity).  Hmm.

Let me think about the "height" h(S) = max L(S).

CLAIM: if all g <= 1, then for every S, L(S) is a singleton.

Hmm, is that true?  Let me test: the counterexamples L=[2,3] with g=1 show that
L(S) can have two elements with different parities while g(S)=1.  So the claim
is false at the position level.

But at the BOARD level, mixed parity => some g >= 2 held in all 28749 cases.

Let me think about why.  Suppose maximal sets M0 (even) and M1 (odd) exist.
Consider the position S = M0 ∩ M1.  Hmm.

Alternative: consider the "join" of the game.  Hmm.

Let me try: take a maximal set M0 of even size and M1 of odd size.  Consider
the position S = M0 ∩ M1.  From S, we can reach M0 and M1.

Let d0 = |M0| - |S|, d1 = |M1| - |S|.  These have different parities.

Now, consider the game tree from S.  There is a path of length d0 to M0 and a
path of length d1 to M1.

Hmm, I need to show some position in this subtree has g >= 2.

Let me think about the position S itself.  If g(S) >= 2, done.  So suppose
g(S) <= 1.

Since S can reach M0 (g=0), g(S) >= 1.  So g(S) = 1.

Now, g(S) = 1 means 0 is among the children's values but 1 is not.
So every child has g != 1, i.e., g in {0, 2, 3, ...}.  Since we assumed all
g <= 1, every child has g = 0.

So every child of S is a P-position (g=0).

But a child S' = S ∪ {p} with p in M1 \ S: is it maximal?  Not necessarily.
If S' is not maximal, then g(S') = 0 means all its children have g = 1.

Hmm, this is getting somewhere.  Let me continue.

Since all children of S have g = 0, and S has a child on a path to M1 of length
d1 (so that child has L containing d1 - 1)...

Let me consider the child S' = S ∪ {p} where p is the first step on a path from
S to M1.  Then L(S') contains d1 - 1.

Since g(S') = 0 and S' is not maximal (d1 - 1 >= 1), all children of S' have
g = 1.

Continuing along the path, we get positions with alternating g values 1, 0, 1, 0, ...
until we reach M1 with g = 0.

The path from S to M1 has length d1.  The g values along it alternate starting
from g(S) = 1.  So the last position M1 has g = (d1 mod 2) XOR 1... let me index:
S = T_0, T_1, ..., T_{d1} = M1.  g(T_0) = 1, g(T_1) = 0, g(T_2) = 1, ...
So g(T_i) = 1 if i even, 0 if i odd.  Then g(M1) = g(T_{d1}) = 1 if d1 even,
0 if d1 odd.  But M1 is maximal so g(M1) = 0.  Therefore d1 must be odd.

Similarly, along the path from S to M0 of length d0, g alternates starting from
1, so g(M0) = 0 requires d0 odd.

But d0 and d1 have different parities (since |M0| and |M1| differ in parity).
Contradiction!

Wait, let me redo.  d0 = |M0| - |S|, d1 = |M1| - |S|.  If |M0| even and |M1| odd,
then d0 and d1 have different parities.  But the argument shows both must be odd.
Contradiction.

Hmm, but the argument assumed that along the path, g alternates 1,0,1,0,...
That requires each T_i to have all children with the opposite g value.  Let me
check: g(T_i) = 1 means 0 is among children's values and 1 is not.  Since all
g <= 1, all children have g = 0.  Yes.  And g(T_i) = 0 (non-maximal) means all
children have g = 1.  Yes.

So along ANY path, g alternates.  Therefore the parity of the path length from
S to any maximal set is determined: it must be odd (since g(M) = 0 and g(S) = 1,
and alternating means the parity of the distance is odd).

So all maximal sets containing S have |M| - |S| odd, i.e., |M| ≡ |S| + 1 (mod 2).
So all maximal sets containing S have the SAME parity.

But we assumed M0 and M1 both contain S = M0 ∩ M1.  Contradiction!

So the proof works: if all g <= 1 and M0, M1 are maximal with different parities,
take S = M0 ∩ M1, derive a contradiction.

Wait, I need to double check that S = M0 ∩ M1 is a valid position (safe set).
Yes: subsets of safe sets are safe.

And S can reach M0 and M1 (by adding the remaining points, which are safe since
M0, M1 are safe supersets).

So the proof is complete!

THEOREM (converse).  If all g(S) <= 1, then all maximal sets have the same parity.

PROOF.  Suppose M0, M1 maximal with |M0| even, |M1| odd.  Let S = M0 ∩ M1.
Since S ⊆ M0 and M0 is maximal, S is safe.  From S we can reach M0 and M1.

Since M0 is maximal and reachable from S, g(S) >= 1 (as 0 is among the children's
values along the path... hmm, actually g(S) >= 1 because S is not maximal and
some child leads to a P-position).

Hmm, let me be careful.  Is g(S) >= 1?  S is not maximal (it can be extended to
M0).  So S has at least one child.  If all children had g >= 1, then g(S) = 0.
But then S would be a P-position with a path to M0 (a P-position)... that is
possible in general.

Hmm, so g(S) could be 0.  Let me redo.

If g(S) = 0, then all children have g >= 1.  Since all g <= 1, all children have
g = 1.  Then along the path to M0, g alternates 0,1,0,1,...  So g(M0) = 0
requires d0 even.  Similarly g(M1) = 0 requires d1 even.  But d0, d1 have
different parities.  Contradiction.

If g(S) = 1, then some child has g = 0 and no child has g = 1.  So all children
have g = 0.  Along the path, g alternates 1,0,1,0,...  So g(M0) = 0 requires d0
odd, and g(M1) = 0 requires d1 odd.  Contradiction.

Either way, contradiction.  QED!

So the converse is PROVED.

Let me verify this reasoning computationally: check that along every path, g
alternates when all g <= 1.
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

    # check: if all g <= 1, does g alternate along every edge?
    all_low = max(g.values()) <= 1
    alternates = True
    if all_low:
        for pmask, val in g.items():
            for i in range(n):
                if pmask >> i & 1:
                    continue
                if can_add(i, pmask):
                    child = pmask | (1 << i)
                    if g[child] == val:
                        alternates = False
                        break
            if not alternates:
                break

    sizes = sorted({m.bit_count() for m in maximal})
    return {
        "n": n,
        "edges": len(edges),
        "max_grundy": max(g.values()),
        "all_low": all_low,
        "alternates": alternates,
        "maximal_parities": sorted({s % 2 for s in sizes}),
        "same_parity": len({s % 2 for s in sizes}) == 1,
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

    low_boards = []
    for mask in range(total):
        edges = [all_edges[i] for i in range(len(all_edges)) if mask >> i & 1]
        if not edges:
            continue
        r = analyse(n, edges)
        if r["all_low"]:
            low_boards.append(r)

    print(f"boards with all g <= 1: {len(low_boards)}")
    print(f"  of these, g alternates along every edge: "
          f"{sum(1 for r in low_boards if r['alternates'])}/{len(low_boards)}")
    print(f"  of these, maximal sizes have same parity: "
          f"{sum(1 for r in low_boards if r['same_parity'])}/{len(low_boards)}")
    bad = [r for r in low_boards if not r["same_parity"]]
    print(f"  VIOLATIONS of 'all g<=1 => same parity': {len(bad)}")
    for r in bad[:5]:
        print(f"    mask={r['mask']} maximal parities={r['maximal_parities']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "n": n,
            "low_boards": len(low_boards),
            "alternates": sum(1 for r in low_boards if r["alternates"]),
            "same_parity": sum(1 for r in low_boards if r["same_parity"]),
            "violations": len(bad),
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

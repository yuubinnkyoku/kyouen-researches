"""Why is the gap q+3-K non-monotone?

Data:
  q=3: K=5, gap=1
  q=5: K=5, gap=3
  q=7: K=6, gap=4
  q=9: K=9, gap=3

The gap goes 1, 3, 4, 3.  Not monotone.

Let me look at K itself: 5, 5, 6, 9.  And q: 3, 5, 7, 9.

K/q: 1.67, 1.00, 0.86, 1.00.

Interesting: K/q is 1.00 for q=5 and q=9 (both = 1 mod 4), and 1.67, 0.86 for
q=3, 7 (both = 3 mod 4).

So for q = 1 mod 4, K = q exactly (for q=5, 9).  For q = 3 mod 4, K < q.

That explains the gap pattern:
  q=5 (1 mod 4): K=q=5, gap = q+3-K = 3
  q=9 (1 mod 4): K=q=9, gap = 3
  q=3 (3 mod 4): K=5 > q=3, gap = 1
  q=7 (3 mod 4): K=6 < q=7, gap = 4

So the gap is 3 exactly when K = q (which happens for q = 1 mod 4, q >= 5).

For q=3, K=5 > q=3 (small board effect).
For q=7, K=6 < q=7 (gap 4).

Let me check q=13: K >= 13.  If K = 13 = q, gap = 16-13 = 3.
And q=17: K >= 17.  If K = 17 = q, gap = 20-17 = 3.

So the conjecture: for q = 1 mod 4 and q >= 5, K = q exactly, giving gap = 3.

That is a strong conjecture!  Let me check the evidence:
  q=5: K=5=q ✓
  q=9: K=9=q ✓
  q=13: K>=13, and bound is 16.  If K=13, then K=q ✓
  q=17: K>=17, bound 20.  If K=17, K=q ✓

And for q = 3 mod 4:
  q=3: K=5 > q
  q=7: K=6 < q
  q=11: K=9 < q
  q=19: K>=13 < q

So for q = 3 mod 4, K < q (except q=3).

CONJECTURE:
  * q = 1 mod 4, q >= 5: K = q
  * q = 3 mod 4, q >= 7: K < q

Let me test this conjecture by checking whether size q+1 is impossible for
q = 1 mod 4 (which would confirm K = q given K >= q).

For q=5: is size 6 impossible?  We verified sizes 6,7,8 are all impossible.
So K=5=q. ✓

For q=9: is size 10 impossible?  We verified sizes 10,11,12 are impossible.
So K=9=q. ✓

For q=13: is size 14 impossible?  That is the open question.  If yes, K=13=q.

So the conjecture is: for q = 1 mod 4, K = q exactly.

This is a beautiful conjecture!  Let me document it and test what we can.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    # known data
    data = [
        (3, 5, True), (4, 5, True), (5, 5, True), (7, 6, True),
        (8, 8, True), (9, 9, True), (11, 9, True),
        (13, 13, False), (16, 12, False), (17, 17, False), (19, 13, False),
    ]

    print("CONJECTURE: for q = 1 mod 4 and q >= 5, K(AG(2,q)) = q exactly.")
    print()
    print(f"{'q':>3} {'mod4':>5} {'K':>4} {'exact':>6} {'K=q?':>6} {'K<q?':>6}")
    rows = []
    for q, k, exact in data:
        rows.append({"q": q, "q_mod_4": q % 4, "K": k, "exact": exact,
                     "K_eq_q": k == q, "K_lt_q": k < q})
        print(f"{q:>3} {q%4:>5} {k:>4} {'Y' if exact else 'n':>6} "
              f"{'Y' if k==q else 'n':>6} {'Y' if k<q else 'n':>6}")

    print()
    print("q = 1 mod 4 (q >= 5):")
    for q, k, exact in data:
        if q % 4 == 1 and q >= 5:
            print(f"  q={q}: K={k}{'' if exact else ' (lower bound)'}, "
                  f"K=q? {k == q}")
    print()
    print("q = 3 mod 4 (q >= 7):")
    for q, k, exact in data:
        if q % 4 == 3 and q >= 7:
            print(f"  q={q}: K={k}{'' if exact else ' (lower bound)'}, "
                  f"K<q? {k < q}")
    print()
    print("the conjecture holds for all exact values:")
    print("  q=5: K=5=q, q=9: K=9=q")
    print("  q=7: K=6<7, q=11: K=9<11")
    print()
    print("if the conjecture holds, the gap q+3-K is exactly 3 for q = 1 mod 4,")
    print("which explains the non-monotone pattern 1,3,4,3.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

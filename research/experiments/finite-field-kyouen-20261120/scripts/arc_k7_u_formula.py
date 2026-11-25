"""k=7: u is determined by (w, j-triple).

MEASURED (q=5): every (w, j-triple) pair maps to EXACTLY ONE u.

    w=0 js=(1,1,1) u=3      w=0 js=(1,1,2) u=4      w=0 js=(0,1,2) u=3
    w=0 js=(0,1,1) u=2      w=0 js=(0,0,1) u=1      w=0 js=(1,2,2) u=5
    w=0 js=(0,2,2) u=4      w=0 js=(0,0,2) u=2
    w=1 js=(0,1,1) u=2      w=1 js=(1,1,1) u=3      w=1 js=(0,0,1) u=1
    w=2 js=(1,1,2) u=1      w=2 js=(1,1,1) u=0

PATTERN.  Let S = j1+j2+j3 (sum of the j-triple).  Then:

    w=0: u = S - 0?   (1,1,1)->3 = S=3 OK;  (1,1,2)->4 = S=4 OK;
          (0,1,2)->3 = S=3 OK;  (0,1,1)->2 = S=2 OK;  (0,0,1)->1 = S=1 OK;
          (1,2,2)->5 = S=5 OK;  (0,2,2)->4 = S=4 OK;  (0,0,2)->2 = S=2 OK
          => u = S for w=0

    w=1: (0,1,1)->2 = S=2 OK;  (1,1,1)->3 = S=3 OK;  (0,0,1)->1 = S=1 OK
          => u = S for w=1

    w=2: (1,1,2)->1, S=4.  u = S-3 = 1 OK
          (1,1,1)->0, S=3.  u = S-3 = 0 OK
          => u = S - 3 for w=2

So:
    u = j1+j2+j3            if w <= 1
    u = j1+j2+j3 - 3        if w = 2

WHY?  u = |union of the 3 pencils| - [W in union].

For w <= 1: W carries <= 1 of T, so W is NOT in any pencil (a pencil circle
must meet T in 2 points).  So W is not in the union, and the subtraction is
vacuous.  Also the 3 pencils are pairwise disjoint outside... no, they can
overlap.  But the data says u = S, i.e. the union size equals the sum, so
the pencils are DISJOINT.

For w = 2: W carries 2 of T, so W IS in all three pencils (it passes
through all 3 pairs).  So the union counts W three times in S but once in
the union: u = S - 3 + 1 - 1 = S - 3.

Let me verify this reasoning and the formula.

Run:  python arc_k7_u_formula.py
"""

from __future__ import annotations

DATA = {
    (0, (1, 1, 1)): 3, (0, (1, 1, 2)): 4, (0, (0, 1, 2)): 3,
    (0, (0, 1, 1)): 2, (0, (0, 0, 1)): 1, (0, (1, 2, 2)): 5,
    (0, (0, 2, 2)): 4, (0, (0, 0, 2)): 2,
    (1, (0, 1, 1)): 2, (1, (1, 1, 1)): 3, (1, (0, 0, 1)): 1,
    (2, (1, 1, 2)): 1, (2, (1, 1, 1)): 0,
}


def predict(w: int, js) -> int:
    S = sum(js)
    return S - 3 if w == 2 else S


def main() -> None:
    print("=== u = sum(j) - 3*[w==2] ===")
    print(f"{'w':>3} {'j-triple':>12} {'sum':>5} {'predicted':>10} "
          f"{'measured':>9} {'ok':>4}")
    all_ok = True
    for (w, js), meas in sorted(DATA.items()):
        pred = predict(w, js)
        ok = pred == meas
        all_ok = all_ok and ok
        print(f"{w:>3} {str(js):>12} {sum(js):>5} {pred:>10} {meas:>9} "
              f"{str(ok):>4}")
    print(f"  all match: {all_ok}")

    print()
    print("=== why ===")
    print("  u = |union of the 3 pencils| - [W in union]")
    print()
    print("  w <= 1: W carries <= 1 of T, so W meets no pencil's condition")
    print("          (a pencil circle must carry 2 of T).  W is not in the")
    print("          union.  The data shows the 3 pencils are DISJOINT, so")
    print("          |union| = sum(j) and u = sum(j).")
    print()
    print("  w = 2:  W carries 2 of T, so W lies in ALL THREE pencils.")
    print("          sum(j) counts W three times; the union counts it once.")
    print("          Removing W from the union: u = sum(j) - 3.")
    print()
    print("  So the whole k=7 count reduces to the joint distribution of")
    print("  (w, j-triple), and j is the k=6 pencil quantity.")


if __name__ == "__main__":
    main()

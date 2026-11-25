"""k=7: reconstructing (w,u) from the case decomposition.

MEASURED (q=5, per (C,T), over 1140 triples):

    Case A (disjoint involutions, 840 triples):
        w=0: sum_j=1:16  2:100  3:416  4:140  5:8
        w=1: sum_j=1:48  2:96   3:16
    Case B (one common pair, 300 triples):
        w=0: sum_j=4:12  5:8
        w=1: sum_j=2:128 3:32
        w=2: sum_j=3:32  4:88

RECONSTRUCTION.  u = sum_j - 3*[w=2], so:

    Case A: u = sum_j  (w <= 1)
    Case B, w<=1: u = sum_j
    Case B, w=2: u = sum_j - 3

Let me verify this reproduces the measured (w,u) distribution:

    (0,1):16  (0,2):100  (0,3):416  (0,4):152  (0,5):16
    (1,1):48  (1,2):224  (1,3):48
    (2,0):32  (2,1):88

Check:
    (0,1) = A w=0 sum=1 -> 16                          OK
    (0,2) = A w=0 sum=2 -> 100                         OK
    (0,3) = A w=0 sum=3 -> 416                         OK
    (0,4) = A w=0 sum=4 (140) + B w=0 sum=4 (12) = 152 OK
    (0,5) = A w=0 sum=5 (8) + B w=0 sum=5 (8) = 16     OK
    (1,1) = A w=1 sum=1 -> 48                          OK
    (1,2) = A w=1 sum=2 (96) + B w=1 sum=2 (128) = 224 OK
    (1,3) = A w=1 sum=3 (16) + B w=1 sum=3 (32) = 48   OK
    (2,0) = B w=2 sum=3 -> u=0 -> 32                   OK
    (2,1) = B w=2 sum=4 -> u=1 -> 88                   OK

ALL MATCH.  So the (w,u) distribution is fully determined by the
(case, w, sum_j) table.

Run:  python arc_k7_reconstruct.py
"""

from __future__ import annotations

DATA = {
    ("A", 0, 1): 16, ("A", 0, 2): 100, ("A", 0, 3): 416,
    ("A", 0, 4): 140, ("A", 0, 5): 8,
    ("A", 1, 1): 48, ("A", 1, 2): 96, ("A", 1, 3): 16,
    ("B", 0, 4): 12, ("B", 0, 5): 8,
    ("B", 1, 2): 128, ("B", 1, 3): 32,
    ("B", 2, 3): 32, ("B", 2, 4): 88,
}

MEASURED_WU = {
    (0, 1): 16, (0, 2): 100, (0, 3): 416, (0, 4): 152, (0, 5): 16,
    (1, 1): 48, (1, 2): 224, (1, 3): 48,
    (2, 0): 32, (2, 1): 88,
}


def main() -> None:
    print("=== reconstructing (w,u) from (case, w, sum_j) ===")
    recon = {}
    for (case, w, sj), cnt in DATA.items():
        u = sj - 3 if (case == "B" and w == 2) else sj
        recon[(w, u)] = recon.get((w, u), 0) + cnt

    print(f"{'w':>3} {'u':>3} {'reconstructed':>14} {'measured':>10} {'ok':>4}")
    all_ok = True
    for key in sorted(set(recon) | set(MEASURED_WU)):
        r = recon.get(key, 0)
        m = MEASURED_WU.get(key, 0)
        ok = r == m
        all_ok = all_ok and ok
        print(f"{key[0]:>3} {key[1]:>3} {r:>14} {m:>10} {str(ok):>4}")
    print(f"  all match: {all_ok}")

    print()
    print("=== case totals ===")
    a = sum(v for k, v in DATA.items() if k[0] == "A")
    bb = sum(v for k, v in DATA.items() if k[0] == "B")
    print(f"  Case A: {a}, Case B: {bb}, total {a+bb}")

    print()
    print("=== w by case ===")
    for case in ("A", "B"):
        wm = {}
        for (c, w, sj), cnt in DATA.items():
            if c == case:
                wm[w] = wm.get(w, 0) + cnt
        print(f"  Case {case}: w marginal {dict(sorted(wm.items()))}")

    print()
    print("=== sum_j by case ===")
    for case in ("A", "B"):
        sm = {}
        for (c, w, sj), cnt in DATA.items():
            if c == case:
                sm[sj] = sm.get(sj, 0) + cnt
        print(f"  Case {case}: sum_j marginal {dict(sorted(sm.items()))}")


if __name__ == "__main__":
    main()

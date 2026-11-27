"""Direct PGammaL orbit BFS for the maximal 6-cap triple.

Uses the verified PGL generators plus the Frobenius permutation phi, and shows
that the PGammaL orbit of the maximal 6-cap A is exactly the union of the three
PGL orbits (size 3*686,784 = 2,060,352).
"""
import gc
import sys
import time
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import bfs as B
import reps as R

APPLIES3 = B.APPLIES + [B.make_apply(C.PHI)]


def main():
    A = R.MAXA
    print("PGammaL orbit BFS from maximal 6-cap A =", A)
    t0 = time.time()
    seen, orb = B.orbit_bfs(A, applies=APPLIES3, progress=500000,
                            label="PGammaL(A)")
    print("size:", len(seen), "expected:", 3 * 686784,
          "in %.1fs" % (time.time() - t0))
    assert len(seen) == 3 * 686784, len(seen)
    for name, pts in [("A", R.MAXA), ("B", R.MAXB), ("C", R.MAXC),
                      ("phi(A)", [C.PHI[p] for p in R.MAXA]),
                      ("phi^2(A)", [C.PHI[C.PHI[p]] for p in R.MAXA])]:
        m = B.mask_of(pts)
        print(f"  {name:8s} in PGammaL(A): {m in seen}")
        assert m in seen
    # and it is not a single PGL orbit
    assert len(seen) != 686784
    del seen, orb
    gc.collect()
    print("PGammaL maximal-6 orbit check PASSED")


if __name__ == "__main__":
    main()

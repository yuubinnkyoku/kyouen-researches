"""Quick board + claim-(B) reconnaissance (independent)."""
import os
import sys
import time
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boardlib

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.normpath(os.path.join(HERE, boardlib.BOARD_REL))


def mask_of(pts):
    m = 0
    for p in pts:
        m |= 1 << p
    return m


def main():
    n, lines = boardlib.load_board(BOARD)
    plane = boardlib.Plane(n, lines)
    print("board:", BOARD)
    print("axioms:", plane.validate_plane())

    print("building standard PG(2,9) and testing isomorphism ...")
    t0 = time.time()
    ok, info, err = boardlib.is_isomorphic_to_pg29(plane)
    print("isomorphic:", ok, "info:", info, "err:", err,
          "time %.2fs" % (time.time() - t0))
    if not ok:
        print("ISOMORPHISM FAILED")
        return 1

    # known complete 7-arcs taken from the parent repository reports/logs
    known = [
        [3, 25, 26, 31, 37, 39, 75],
        [16, 47, 51, 56, 60, 80, 82],
        [33, 39, 57, 70, 74, 80, 89],
    ]
    print("\n=== known 7-arcs: addable sets of the 6-subsets ===")
    for arc in known:
        A = mask_of(arc)
        print("A =", arc, "is_cap:", plane.is_cap(A),
              "addable(A):", plane.mask_points(plane.addable(A)))
        for p in arc:
            X = A & ~(1 << p)
            add = plane.addable(X)
            addp = plane.mask_points(add)
            print("  X=A-%2d  |X|=%d cap=%s  |add|=%2d  add=%s  add&A=%s  add-X=%s"
                  % (p, X.bit_count(), plane.is_cap(X), len(addp), addp,
                     sorted(set(addp) & set(arc)),
                     sorted(set(addp) - set(arc))))
    return 0


if __name__ == "__main__":
    sys.exit(main())

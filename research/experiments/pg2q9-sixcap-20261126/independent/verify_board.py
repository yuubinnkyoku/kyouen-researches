"""Task 1 (board part): verify the board is a projective plane of order 9 and
is isomorphic to PG(2,9) by an explicit incidence isomorphism.

The isomorphism test is constructive: map a board quadrangle to the standard
frame of PG(2,9) over GF(9), close under forced line/point images (this yields
the PG(2,3) subplane), then map one further point and close again.  The result
is a bijection on all 91 points and 91 lines whose images are checked against
every incidence.  An explicit isomorphism is a proof that the board is PG(2,9).
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boardlib


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.normpath(os.path.join(here, boardlib.BOARD_REL))
    n, lines = boardlib.load_board(path)
    plane = boardlib.Plane(n, lines)
    print("board file:", path)
    print("axiom checks:", plane.validate_plane())

    print("building standard PG(2,9) over GF(9) ...")
    ol = len(plane.lines)
    deg = sorted(set(sum(1 for ln in plane.lines if p in ln) for p in range(n)))
    print("lines=%d  line_sizes=%s  point_degrees=%s" %
          (ol, sorted(set(len(ln) for ln in plane.lines)), deg))

    t0 = time.time()
    ok, info, err = boardlib.is_isomorphic_to_pg29(plane)
    print("isomorphism test:", "PASS" if ok else "FAIL")
    for k, v in info.items():
        print("  %s: %s" % (k, v))
    print("error:", err if err else "(none)")
    print("time %.3fs" % (time.time() - t0))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

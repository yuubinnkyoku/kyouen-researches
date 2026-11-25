"""Task 1: verify the board itself, GF(8) construction, the Frobenius map and
the four explicit 6-point sets in the claim."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import conic as Q


def main():
    board = C.load_board(C.BOARD_PATH)
    print("board:", C.BOARD_PATH)
    print("lines read:", len(board), " each of size",
          sorted({len(L) for L in board}))
    gen = C.LINES
    print("lines generated from GF(8) 2-D subspaces:", len(gen))
    assert len(board) == 73 and len(gen) == 73
    assert sorted(board, key=sorted) == gen
    print("board == generated line set: True")

    # projective plane axioms
    assert len(C.PAIR_LINE) == 73 * 72 // 2
    print("point pairs:", len(C.PAIR_LINE), "each on exactly one line")
    ok = True
    for i in range(len(gen)):
        for j in range(i + 1, len(gen)):
            if len(gen[i] & gen[j]) != 1:
                ok = False
                print("bad line intersection", i, j, len(gen[i] & gen[j]))
    assert ok
    print("any two distinct lines meet in exactly one point: True")
    print("points on each line: 9; lines through each point: 9 (duality)")

    # GF(8) sanity
    print("GF(8) elements 0..7, x^3+x+1=0; x*x =", C.gf_mul(2, 2),
          " x^3 =", C.gf_mul(2, C.gf_mul(2, 2)))
    assert C.gf_mul(2, C.gf_mul(2, 2)) == 3
    for a in range(8):
        for b in range(8):
            assert C.gf_mul(a, b) == C.gf_mul(b, a)
    print("multiplication commutative on all 64 pairs: True")

    # canonical points / rank
    print("first 11 canonical points:",
          [(i, C.POINT[i]) for i in range(11)])
    assert C.POINT[0] == (0, 0, 1)
    assert C.POINT[1] == (0, 1, 0) and C.POINT[8] == (0, 1, 7)
    assert C.POINT[9] == (1, 0, 0)

    # Frobenius
    phi = C.PHI
    print("phi is a permutation:", len(set(phi)) == 73)
    print("phi^3 == id:", C.PHI3 == C.IDENT)
    print("phi != id:", phi != C.IDENT)
    assert len(set(phi)) == 73 and C.PHI3 == C.IDENT and phi != C.IDENT
    # phi maps lines to lines
    lineset = set(gen)
    assert all(frozenset(phi[p] for p in L) in lineset for L in gen)
    print("phi maps every line to a line (collineation): True")

    # the explicit sets
    C6 = [2, 3, 10, 16, 18, 21]
    PHI_C6 = [2, 5, 10, 12, 18, 23]
    D6 = [1, 10, 12, 59, 62, 65]
    PHI_D6 = [1, 10, 14, 29, 32, 33]
    for name, pts in [("C6", C6), ("phi(C6)", PHI_C6),
                      ("D6", D6), ("phi(D6)", PHI_D6)]:
        print(f"{name:9s} = {pts}  cap={C.is_cap(pts)}")
        assert C.is_cap(pts)
    assert sorted(phi[p] for p in C6) == PHI_C6
    assert sorted(phi[p] for p in D6) == PHI_D6
    print("phi(C6) and phi(D6) match the stated sets: True")
    # phi is a bijection, so applying it to the 6-element sets preserves size
    assert len(set(PHI_C6)) == 6 and len(set(PHI_D6)) == 6

    # conic / non-conic character (also needed for the orbit labels)
    co, conic9 = Q.conic_of_cap(C6)
    print("unique conic through C6 has points:", conic9)
    print("C6 subset of that conic:", set(C6) <= set(conic9))
    print("D6 lies on a conic:", Q.is_conic_set(D6))
    assert set(C6) <= set(conic9)
    assert not Q.is_conic_set(D6)
    # both are non-maximal (extendable)
    print("C6 addable points:", len([p for p in range(73)
                                     if p not in C6 and C.is_cap(C6 + [p])]))
    print("D6 addable points:", len([p for p in range(73)
                                     if p not in D6 and C.is_cap(D6 + [p])]))
    print("TASK 1 CHECKS PASSED")


if __name__ == "__main__":
    main()

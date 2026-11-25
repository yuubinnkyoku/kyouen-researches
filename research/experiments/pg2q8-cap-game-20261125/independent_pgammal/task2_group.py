"""Task 2: construct PGL(3,8) from elementary matrices and verify group orders."""
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import group as G


def det3(M):
    # determinant over GF(2) (all permutation signs are +1)
    import itertools
    total = 0
    for perm in itertools.permutations(range(3)):
        prod = 1
        for i in range(3):
            prod = C.gf_mul(prod, M[3 * i + perm[i]])
        total = C.gf_add(total, prod)
    return total


ALPHA = 2          # x
ALPHA2 = 4         # x^2

# Elementary transvections E_ij(1) for all i != j, plus E_12(alpha), E_12(alpha^2).
MATS = []
NAMES = []
for (i, j) in [(0, 1), (1, 2), (0, 2), (1, 0), (2, 0), (2, 1)]:
    MATS.append(C.mat_elementary(i, j, 1))
    NAMES.append(f"E{i+1}{j+1}(1)")
for a, nm in [(ALPHA, "a"), (ALPHA2, "a2")]:
    MATS.append(C.mat_elementary(0, 1, a))
    NAMES.append(f"E12({nm})")

GENS = [C.perm_from_matrix(M) for M in MATS]

if __name__ == "__main__":
    print("number of generators:", len(GENS))
    for nm, M, g in zip(NAMES, MATS, GENS):
        print(f"  {nm:10s} det={det3(M)} nontrivial={g != C.IDENT}")
    assert all(det3(M) == 1 for M in MATS)
    assert all(g != C.IDENT for g in GENS)

    t0 = time.time()
    order, base, levels, orbits, trans = G.schreier_sims(GENS, C.N, verbose=True)
    print("time %.1fs" % (time.time() - t0))
    print("computed |<gens>| =", order)
    print("expected |PGL(3,8)| =", 16482816)
    assert order == 16482816, order
    gl = (8**3 - 1) * (8**3 - 8) * (8**3 - 8**2)
    print("|GL(3,8)| = (8^3-1)(8^3-8)(8^3-8^2) =", gl)
    print("scalars in GL: 7; |GL|/7 =", gl // 7)
    assert gl == 115379712 and gl // 7 == 16482816
    # scalar subgroup: lambda*I, lambda in GF(8)^*; only lambda=1 has lambda^3=1
    assert [a for a in range(1, 8) if C.gf_pow(a, 3) == 1] == [1]
    # independent frame count: ordered quadruples with no three collinear
    # 73 points, 72 second points, 64 third points off the first line,
    # 49 fourth points off the union of the three lines.
    L = C.PAIR_LINE[(0, 1)] | C.PAIR_LINE[(0, 9)] | C.PAIR_LINE[(1, 9)]
    print("union of the 3 frame lines has", len(L), "points ->",
          73 - len(L), "choices for the 4th point")
    assert len(L) == 24
    frames = 73 * 72 * 64 * 49
    print("ordered projective frames:", frames)
    assert frames == 16482816

    # Frobenius normalisation: phi g phi^-1 = entrywise square of the matrix
    phi = C.PHI
    phi_inv = G.inverse(phi)
    for nm, M, g in zip(NAMES, MATS, GENS):
        conj = G.compose(phi, G.compose(g, phi_inv))
        M2 = tuple(C.GF_SQUARE[x] for x in M)
        expected = C.perm_from_matrix(M2)
        print(f"  phi {nm} phi^-1 == matrix^2 action: {conj == expected}")
        assert conj == expected

    # phi not in PGL (membership test against the BSGS)
    print("phi member of <gens>:", G.is_member(phi, base, levels, orbits, trans, C.N))
    assert not G.is_member(phi, base, levels, orbits, trans, C.N)
    # second, matrix-level proof: phi fixes the three basis points e1,e2,e3
    # projectively, so any matrix inducing phi would be diagonal; no diagonal
    # matrix induces phi.
    assert [C.PHI[i] for i in (0, 1, 9)] == [0, 1, 9]
    import itertools
    found = None
    for l1, l2, l3 in itertools.product(range(1, 8), repeat=3):
        M = (l1, 0, 0, 0, l2, 0, 0, 0, l3)
        if C.perm_from_matrix(M) == phi:
            found = (l1, l2, l3)
            break
    print("diagonal matrix inducing phi:", found)
    assert found is None
    print("phi moves point 25 (1,x,0) to point", phi[25],
          "(expected 41 = (1,x^2,0))")
    assert phi[25] == 41

    t0 = time.time()
    order_full, base2, levels2, orbits2, trans2 = G.schreier_sims(
        GENS + [phi], C.N, verbose=True)
    print("time %.1fs" % (time.time() - t0))
    print("computed |<PGL,phi>| =", order_full)
    print("expected 3*|PGL| =", 3 * 16482816)
    assert order_full == 3 * 16482816
    assert C.PHI3 == C.IDENT
    print("ALL TASK-2 CHECKS PASSED")

"""Task 3: PGL(2,8) from 2x2 matrices, parameterisation of the conic C by
PG(1,8), and orbits of k-subsets of C for k = 3..8.

Run:  python task3_pgl.py
"""

from __future__ import annotations

import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pg8

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(HERE, os.pardir, "output", "board_pg2q8.txt")

GF_MUL = pg8.GF_MUL
GF_INV = pg8.GF_INV


# --------------------------------------------------------------------------
# PGL(2,8)
# --------------------------------------------------------------------------
def mat2_canon(M):
    for x in M:
        if x:
            inv = GF_INV[x]
            return tuple(GF_MUL[inv][y] for y in M)
    return None


def mat2_mul(A, B):
    return (GF_MUL[A[0]][B[0]] ^ GF_MUL[A[1]][B[2]],
            GF_MUL[A[0]][B[1]] ^ GF_MUL[A[1]][B[3]],
            GF_MUL[A[2]][B[0]] ^ GF_MUL[A[3]][B[2]],
            GF_MUL[A[2]][B[1]] ^ GF_MUL[A[3]][B[3]])


def build_pgl2():
    seen = set()
    for a, b, c, d in itertools.product(range(8), repeat=4):
        if GF_MUL[a][d] ^ GF_MUL[b][c] == 0:
            continue
        seen.add(mat2_canon((a, b, c, d)))
    return sorted(seen)


PG1 = [(1, 0)] + [(s, 1) for s in range(8)]
PG1_INDEX = {v: i for i, v in enumerate(PG1)}


def pg1_canon(v):
    """Normalise (s,t) to the list PG1: t != 0 -> (s/t, 1); t == 0 -> (1, 0)."""
    s, t = v
    if t:
        inv = GF_INV[t]
        return (GF_MUL[inv][s], 1)
    return (1, 0)


def pg1_action(M, p):
    a, b, c, d = M
    s, t = PG1[p]
    return PG1_INDEX[pg1_canon((GF_MUL[a][s] ^ GF_MUL[b][t],
                                GF_MUL[c][s] ^ GF_MUL[d][t]))]


def main():
    print("=" * 78)
    print("TASK 3 - PGL(2,8), parameterisation of C, orbits of k-subsets")
    print("=" * 78)
    board = pg8.Board(BOARD)

    info = pg8.find_conic_through(pg8.BASE_5CAP)
    C = sorted(info["zero_set"])
    assert len(C) == 9 and board.is_cap(C)
    print("conic C (board indices):", C)
    print("           (vectors)    :", [pg8.POINTS[p] for p in C])

    # ---------------- PGL(2,8) as 2x2 matrices over GF(8) -----------------
    pgl2 = build_pgl2()
    print("\n-- PGL(2,8) from 2x2 matrices over GF(8) ---------------------")
    print("  |GL(2,8)| = (8^2-1)(8^2-8) =", (64 - 1) * (64 - 8))
    print("  |PGL(2,8)| = |GL|/(8-1)    =", (64 - 1) * (64 - 8) // 7)
    print("  distinct matrices mod scalars:", len(pgl2))
    index = {M: i for i, M in enumerate(pgl2)}
    # closure / group laws
    closed = all(mat2_canon(mat2_mul(A, B)) in index for A in pgl2 for B in pgl2)
    print("  closed under multiplication:", closed)
    print("  identity present           :", (1, 0, 0, 1) in index)
    # every element has an inverse in the set
    has_inv = all(
        any(mat2_canon(mat2_mul(A, B)) == (1, 0, 0, 1) for B in pgl2) for A in pgl2
    )
    print("  every element invertible   :", has_inv)

    # permission of PG(1,8)
    perms = []
    for M in pgl2:
        perms.append(tuple(pg1_action(M, p) for p in range(9)))
    print("  distinct permutations of PG(1,8):", len(set(perms)))
    hom = True
    for A in pgl2:
        iA = index[A]
        for B in pgl2:
            iB = index[B]
            iAB = index[mat2_canon(mat2_mul(A, B))]
            # (AB).x = A.(B.x)
            if any(perms[iAB][x] != perms[iA][perms[iB][x]] for x in range(9)):
                hom = False
                break
        if not hom:
            break
    print("  action is a homomorphism (checked on all 504^2 pairs):", hom)
    transl = len({perms[m][0] for m in range(len(pgl2))})
    print("  2-transitive? |orbit of 0| =", transl, "; |orbit of (0,1)| =",
          len({(perms[m][0], perms[m][1]) for m in range(len(pgl2))}))
    triples = {(perms[m][0], perms[m][1], perms[m][2]) for m in range(len(pgl2))}
    print("  sharply 3-transitive: #distinct images of (0,1,2) =", len(triples),
          "= 9*8*7 =", 9 * 8 * 7)

    # ---------------- parameterise C by PG(1,8) ---------------------------
    P0 = C[0]
    P0v = pg8.POINTS[P0]
    # line L not through P0: smallest line whose point set avoids P0
    Lidx = None
    for li, LS in enumerate(board.line_sets):
        if P0 not in LS:
            Lidx = li
            break
    Lpts = sorted(board.line_sets[Lidx])
    print("\n-- parameterisation of C by PG(1,8) --------------------------")
    print(f"  P0 = {P0} {P0v};  L = line {Lidx} = {Lpts} (P0 not on L)")
    lines_through_P0 = board.point_lines[P0]
    print("  #lines through P0:", len(lines_through_P0))

    # bijection: point Q of L  <->  line P0 Q
    bij = {}
    for Q in Lpts:
        bij[Q] = board.line_of_pair[P0][Q]
    print("  Q in L |-> line(P0,Q) is a bijection L -> pencil at P0:",
          len(set(bij.values())) == 9)

    # projective coordinates on L from a basis of its 2-dim vector space
    u, v = pg8.POINTS[Lpts[0]], pg8.POINTS[Lpts[1]]
    coords = {}
    for Q in Lpts:
        w = pg8.POINTS[Q]
        sol = None
        for i, j in itertools.permutations(range(3), 2):
            det = GF_MUL[u[i]][v[j]] ^ GF_MUL[u[j]][v[i]]
            if det == 0:
                continue
            detinv = GF_INV[det]
            al = GF_MUL[detinv][GF_MUL[w[i]][v[j]] ^ GF_MUL[w[j]][v[i]]]
            be = GF_MUL[detinv][GF_MUL[u[i]][w[j]] ^ GF_MUL[u[j]][w[i]]]
            if (GF_MUL[al][u[0]] ^ GF_MUL[be][v[0]],
                GF_MUL[al][u[1]] ^ GF_MUL[be][v[1]],
                GF_MUL[al][u[2]] ^ GF_MUL[be][v[2]]) == w:
                sol = (al, be)
                break
        assert sol is not None
        coords[Q] = PG1_INDEX[pg1_canon(sol)]
    print("  coordinates on L used for PG(1,8) (basis u,v =", u, v, ")")
    print("  coordinate map L -> PG(1,8) bijective:", len(set(coords.values())) == 9)

    # psi: PG(1,8) -> L, and phi: L -> C (second intersection)
    L_of_pg1 = {coords[Q]: Q for Q in Lpts}
    phi = {}
    tangent_Q = None
    for Q in Lpts:
        li = bij[Q]
        inter = board.line_sets[li] & set(C)
        if inter == {P0}:
            phi[Q] = P0
            tangent_Q = Q
        else:
            assert len(inter) == 2 and P0 in inter, (Q, inter)
            phi[Q] = next(iter(inter - {P0}))
    print("  lines through P0 meeting C in 2 points:", sum(1 for q in Lpts if phi[q] != P0),
          "; tangent direction Q =", tangent_Q)
    print("  phi: L -> C bijective:", len(set(phi.values())) == 9,
          "and image = C:", set(phi.values()) == set(C))
    print("  parameter table  [t] in PG(1,8) -> P in C:")
    inv_coords = {coords[Q]: Q for Q in Lpts}
    for t in range(9):
        Q = L_of_pg1[t]
        print(f"      t={t}  (s,t)={PG1[t]}  Q={Q:2d}  ->  P={phi[Q]:2d} {pg8.POINTS[phi[Q]]}")
    # nucleus check: tangent at P0 passes through the nucleus (sanity)
    nucleus = 31
    print("  tangent at P0 = line through P0 and nucleus(31)?",
          board.line_of_pair[P0][nucleus] == board.line_of_pair[P0][tangent_Q])

    # ---------------- induced action on C ---------------------------------
    Cpos = {p: i for i, p in enumerate(C)}
    permC = []
    for m in range(len(pgl2)):
        pm = perms[m]
        arr = [None] * 9
        for Q in Lpts:
            Q2 = L_of_pg1[pm[coords[Q]]]
            arr[Cpos[phi[Q]]] = Cpos[phi[Q2]]
        assert None not in arr
        permC.append(tuple(arr))
    print("\n-- induced action of PGL(2,8) on the 9 points of C ------------")
    print("  distinct permutations of C:", len(set(permC)))
    print("  faithful & transitive     :", len(set(permC)) == 504
          and len({p[0] for p in permC}) == 9)

    # each induced permutation must come from an actual projectivity of
    # PG(2,8) that maps C onto C
    a4 = [pg8.POINTS[p] for p in C[:4]]
    lifted = 0
    bad = []
    for m, pm in enumerate(permC):
        b4 = [pg8.POINTS[C[pm[i]]] for i in range(4)]
        M3 = pg8.projectivity_from_four(a4, b4)
        if M3 is None:
            bad.append(m)
            continue
        img = pg8.apply_projectivity_to_points(M3, C)
        if img is not None and sorted(img) == C:
            lifted += 1
        else:
            bad.append(m)
    print("  induced perms realised by a projectivity of PG(2,8) fixing C:",
          lifted, "/ 504", "" if not bad else f"  (failures {bad[:5]})")

    # ---------------- orbits of k-subsets of C ----------------------------
    print("\n-- orbits of k-subsets of C under PGL(2,8) -------------------")
    orbreport = {}
    allok = True
    for k in range(3, 9):
        visited = set()
        orbits = []
        for sub in itertools.combinations(range(9), k):
            if sub in visited:
                continue
            orb = set()
            stack = [sub]
            while stack:
                cur = stack.pop()
                if cur in orb:
                    continue
                orb.add(cur)
                visited.add(cur)
                for pm in permC:
                    nxt = tuple(sorted(pm[i] for i in cur))
                    if nxt not in orb:
                        stack.append(nxt)
            orbits.append(len(orb))
        from math import comb
        target = comb(9, k)
        ok = (len(orbits) == 1 and orbits[0] == target)
        allok = allok and ok
        orbreport[k] = (len(orbits), sorted(orbits), target, ok)
        print(f"  k={k}: #orbits={len(orbits)}  sizes={sorted(orbits)}  "
              f"C(9,{k})={target}  {'OK' if ok else 'MISMATCH'}")

    # ---------------- supplementary: conic orbit under PGL(3,8) -----------
    print("\n-- [supplement] orbit of C under PGL(3,8) --------------------")
    gens = [
        # elementary transvections x_i -> x_i + x_j  (i != j)
        [[1, 1, 0], [0, 1, 0], [0, 0, 1]],
        [[1, 0, 0], [1, 1, 0], [0, 0, 1]],
        [[1, 0, 1], [0, 1, 0], [0, 0, 1]],
        [[1, 0, 0], [0, 1, 1], [0, 0, 1]],
        [[1, 0, 0], [0, 1, 0], [1, 0, 1]],
        [[1, 0, 0], [0, 1, 0], [0, 1, 1]],
        # diagonal scalings (x is a generator of GF(8)^*) and a coordinate swap;
        # the transvections alone only generate the SL(3,2)-image (orbit 168).
        [[2, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[1, 0, 0], [0, 2, 0], [0, 0, 1]],
        [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
    ]
    gen_perms = []
    for M in gens:
        perm = pg8.apply_projectivity_to_points(M, list(range(73)))
        assert perm is not None and sorted(perm) == list(range(73))
        gen_perms.append(tuple(perm))
    start = frozenset(C)
    seen = {start}
    frontier = [start]
    while frontier:
        nxt = []
        for S in frontier:
            for gp in gen_perms:
                T = frozenset(gp[p] for p in S)
                if T not in seen:
                    seen.add(T)
                    nxt.append(T)
        frontier = nxt
    print("  |orbit of C under <6 elementary transvections>| =", len(seen))
    print("  total non-degenerate conics (task 2 census)     = 32704")
    all_conics = all(len(S) == 9 and board.is_cap(S) for S in seen)
    print("  every image is a 9-point cap (a conic)          :", all_conics)
    pgl3 = (8**3 - 1) * (8**3 - 8) * (8**3 - 8**2) // 7
    print("  |PGL(3,8)| = (8^3-1)(8^3-8)(8^3-8^2)/(8-1)     =", pgl3)
    print("  |PGL(3,8)|/32704 (=> stabiliser order)          =", pgl3 // 32704)
    trans = len(seen) == 32704
    stab_ok = (pgl3 // 32704) == 504

    ok = (
        len(pgl2) == 504
        and closed
        and len(set(perms)) == 504
        and hom
        and len(triples) == 504
        and len(set(coords.values())) == 9
        and set(phi.values()) == set(C)
        and len(set(permC)) == 504
        and lifted == 504
        and allok
        and trans
        and all_conics
        and stab_ok
    )
    print("\nTASK 3:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

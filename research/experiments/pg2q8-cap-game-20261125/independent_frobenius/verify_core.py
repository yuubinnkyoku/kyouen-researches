"""Independent verification of K1329 -- core part (tasks 1,2,3 and the
arithmetic of task 5).  Standard library only.

Run:  python verify_core.py [board_path]
Writes core_results.json next to this script.
"""

import json
import os
import sys
import time
import math

import pg2q8 as G

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "output", "board_pg2q8.txt")

A = (10, 47, 49, 55, 61, 64)
B = (17, 27, 30, 44, 52, 70)
C = (8, 48, 50, 51, 58, 61)
PHI_A_CLAIM = (10, 28, 31, 59, 65, 67)
PHI2_A_CLAIM = (10, 29, 33, 37, 43, 46)

results = {}
checks = []          # (name, passed, detail)

def check(name, passed, detail=""):
    checks.append((name, bool(passed), detail))
    print(("PASS " if passed else "FAIL ") + name + (("  [" + str(detail) + "]") if detail != "" else ""))
    return passed

def main():
    t_start = time.time()

    # ---------------------------------------------------------- field
    print("== GF(8) = GF(2)[x]/(x^3+x+1) ==")
    field_ok = True
    for a in range(8):
        for b in range(8):
            assert G.MUL[a][b] == G.MUL[b][a]
            field_ok &= (G.MUL[a][b] == G.MUL[b][a])
    for a in range(8):
        for b in range(8):
            for c in range(8):
                if G.MUL[G.MUL[a][b]][c] != G.MUL[a][G.MUL[b][c]]:
                    field_ok = False
                if G.MUL[a][b ^ c] != (G.MUL[a][b] ^ G.MUL[a][c]):
                    field_ok = False
    field_ok &= all(G.MUL[1][a] == a for a in range(8))
    field_ok &= all(G.MUL[a][G.INV[a]] == 1 for a in range(1, 8))
    field_ok &= G.MUL[2][2] == 4 and G.MUL[4][2] == 3          # x^3 = x+1
    powers = []
    v = 1
    for _ in range(7):
        powers.append(v)
        v = G.MUL[v][2]
    field_ok &= v == 1 and sorted(powers) == list(range(1, 8))  # 2 generates F_8^*
    check("GF(8): commutative/associative/distributive/inverses, x=2 primitive", field_ok)
    results["field_ok"] = field_ok
    results["gl_order"] = G.gl_order_formula()

    # ---------------------------------------------------------- board
    print("\n== board / PG(2,8) reconstruction ==")
    board = G.read_board(BOARD)
    gen_lines = G.generated_lines()
    board_sets = [frozenset(L) for L in board]
    gen_sets = [frozenset(L) for L in gen_lines]
    check("board: 73 rows of 9 points", len(board) == 73 and all(len(set(L)) == 9 for L in board))
    check("rank convention: generated 73 lines == board rows (as sets)",
          set(gen_sets) == set(board_sets))
    check("board lines are 73 distinct lines", len(set(board_sets)) == 73)
    # plane axioms
    point_line_count = [0] * 73
    for L in board_sets:
        for p in L:
            point_line_count[p] += 1
    check("each point lies on exactly 9 lines", set(point_line_count) == {9})
    line_of_pair = [[None] * 73 for _ in range(73)]
    pair_ok = True
    for li, L in enumerate(board_sets):
        for p in L:
            for q in L:
                if p != q:
                    if line_of_pair[p][q] is not None:
                        pair_ok = False
                    line_of_pair[p][q] = li
    pair_ok &= all(line_of_pair[p][q] is not None for p in range(73) for q in range(73) if p != q)
    check("every pair of points lies on a unique line", pair_ok)
    meet_ok = True
    for i in range(73):
        for j in range(i + 1, 73):
            if len(board_sets[i] & board_sets[j]) != 1:
                meet_ok = False
    check("every pair of lines meets in a unique point", meet_ok)
    results["board_ok"] = all(c[1] for c in checks if c[0].startswith(("board", "rank", "each point", "every pair")))

    # ---------------------------------------------------------- Frobenius
    print("\n== Frobenius phi ==")
    ph = G.phi_perm()
    check("phi is a bijection on the 73 points", sorted(ph) == list(range(73)))
    ph2 = G.perm_mul(ph, ph)
    ph3 = G.perm_mul(ph2, ph)
    check("phi^3 = identity on all 73 points", ph3 == G.IDENT)
    check("phi != identity (order exactly 3)",
          ph != G.IDENT and ph2 != G.IDENT and ph3 == G.IDENT)
    # field automorphism: additive and multiplicative, fixed field GF(2)
    sq = G.SQ
    autom = all(sq[a ^ b] == (sq[a] ^ sq[b]) for a in range(8) for b in range(8))
    autom &= all(sq[G.MUL[a][b]] == G.MUL[sq[a]][sq[b]] for a in range(8) for b in range(8))
    autom &= [a for a in range(8) if sq[a] == a] == [0, 1]
    check("phi is a field automorphism with fixed field GF(2)", autom)
    # phi is a collineation (maps lines to lines)
    line_set = set(board_sets)
    phi_lines_ok = True
    for L in board_sets:
        img = frozenset(ph[p] for p in L)
        if img not in line_set:
            phi_lines_ok = False
    check("phi maps every board line to a board line (collineation)", phi_lines_ok)
    phi_line_perm = []
    idx = {L: i for i, L in enumerate(board_sets)}
    for L in board_sets:
        phi_line_perm.append(idx[frozenset(ph[p] for p in L)])
    check("phi induces a bijection (order 3) on the 73 lines",
          sorted(phi_line_perm) == list(range(73))
          and all(phi_line_perm[phi_line_perm[phi_line_perm[i]]] == i for i in range(73)))
    results["phi_ok"] = all(c[1] for c in checks if c[0].startswith("phi"))

    # ---------------------------------------------------------- caps
    print("\n== maximal 6-caps ==")
    phiA = tuple(sorted(ph[p] for p in A))
    phi2A = tuple(sorted(ph2[p] for p in A))
    check("phi(A) equals claimed set", phiA == PHI_A_CLAIM,
          f"computed {phiA} claimed {PHI_A_CLAIM}")
    check("phi^2(A) equals claimed set", phi2A == PHI2_A_CLAIM,
          f"computed {phi2A} claimed {PHI2_A_CLAIM}")
    sets = {"A": A, "B": B, "C": C, "phi(A)": phiA, "phi^2(A)": phi2A}
    caps_ok = True
    maximal_ok = True
    cap_detail = {}
    for name, S in sets.items():
        S = tuple(S)
        ok6 = len(set(S)) == 6 and all(0 <= p < 73 for p in S)
        cap = ok6 and G.is_cap(S, line_of_pair)
        add = G.addable_points(S, line_of_pair, board_sets) if ok6 else set()
        cap_detail[name] = {"points": list(S), "six_distinct": ok6, "cap": bool(cap),
                            "addable": sorted(add), "n_addable": len(add)}
        caps_ok &= cap
        maximal_ok &= ok6 and len(add) == 0
        print(f"  {name:8s} {tuple(sorted(S))}  cap={cap}  addable={sorted(add)}")
    check("A, B, C, phi(A), phi^2(A) are 6-caps", caps_ok)
    check("A, B, C, phi(A), phi^2(A) are maximal (no addable point)", maximal_ok)
    results["caps"] = cap_detail

    # ---------------------------------------------------------- PGL
    print("\n== PGL(3,8) from explicit generators ==")
    mats = G.pgl_generators()
    check("generator matrices are invertible (det != 0)",
          all(G.gf_det(M) != 0 for M in mats),
          [G.gf_det(M) for M in mats])
    check("no generator matrix is scalar", not any(G.mat_is_scalar(M) for M in mats))
    gens = [G.mat_perm(M) for M in mats]
    check("generator permutations are non-identity",
          all(g != G.IDENT for g in gens))
    coll = True
    for gi, g in enumerate(gens):
        for L in board_sets:
            if frozenset(g[p] for p in L) not in line_set:
                coll = False
                print("   line not mapped to line by generator", gi)
    check("every generator maps every line to a line (collineation group)", coll)
    # induced line permutations are bijections
    check("every generator induces a permutation of the 73 lines",
          all(sorted(idx[frozenset(g[p] for p in L)] for L in board_sets) == list(range(73))
              for g in gens))
    # scalars act trivially
    scalar_id = True
    for a in range(1, 8):
        M = [[a, 0, 0], [0, a, 0], [0, 0, a]]
        if G.mat_perm(M) != G.IDENT:
            scalar_id = False
    check("all 7 scalar matrices act trivially on points", scalar_id)

    t0 = time.time()
    order = G.group_order(gens, verbose=True)
    dt = time.time() - t0
    expected = G.gl_order_formula() // 7
    check(f"generated permutation group has order {order} (= |GL|/7 = {expected})",
          order == expected, f"time {dt:.2f}s")
    results["pgl_order"] = order
    results["pgl_order_expected"] = expected
    results["gl_order"] = G.gl_order_formula()
    check("|GL(3,8)| = (8^3-1)(8^3-8)(8^3-8^2) = 115379712",
          G.gl_order_formula() == 115379712)
    check("115379712 / 7 = 16482816", 115379712 // 7 == 16482816)

    # point / line transitivity and point stabiliser
    tr = G.orbit_transversal(gens, 0)
    check("group is transitive on the 73 points", len(tr) == 73)
    H = set()
    for g in gens:
        for p, t in tr.items():
            q = g[p]
            h = G.perm_mul(G.perm_mul(t, g), G.perm_inv(tr[q]))
            if h != G.IDENT:
                H.add(h)
    stab_order = G.group_order(list(H))
    check(f"point stabiliser order {stab_order} = |PGL|/73 = 225792",
          stab_order == expected // 73 == 225792)
    # line orbit: use induced permutations on line indices
    line_perms = []
    for g in gens:
        line_perms.append(tuple(idx[frozenset(g[p] for p in L)] for L in board_sets))
    check("group is transitive on the 73 lines",
          len(G.orbit_transversal(line_perms, 0)) == 73)
    results["point_stabilizer"] = stab_order

    # ---------------------------------------------------------- arithmetic
    print("\n== arithmetic (task 5) ==")
    check("3*16,482,816 = 49,448,448", 3 * 16_482_816 == 49_448_448)
    check("2,060,352*24 = 49,448,448", 2_060_352 * 24 == 49_448_448)
    check("49,448,448/24 = 2,060,352 (exact)", 49_448_448 % 24 == 0 and 49_448_448 // 24 == 2_060_352)
    check("3*686,784 = 2,060,352", 3 * 686_784 == 2_060_352)
    check("16,482,816/686,784 = 24 (exact)", 16_482_816 % 686_784 == 0 and 16_482_816 // 686_784 == 24)
    check("49,448,448/2,060,352 = 24 (exact)", 49_448_448 // 2_060_352 == 24 and 49_448_448 % 2_060_352 == 0)
    results["arithmetic"] = {
        "3_times_pgl": 3 * 16_482_816,
        "pgl_times_24": 16_482_816 * 24,
        "total_times_24": 2_060_352 * 24,
        "total_over_24": 49_448_448 // 24,
        "orbit3": 3 * 686_784,
        "pgl_over_orbit": 16_482_816 // 686_784,
    }

    # ---------------------------------------------------------- phi vs PGL
    print("\n== phi and PGL (support for task 5) ==")
    # phi normalises PGL: conjugate every generator by phi and test membership
    # by comparing generated-group orders (rigorous: G subset <G,h>, equal
    # orders => <G,h> = G).
    norm_ok = True
    for gi, g in enumerate(gens):
        conj = G.perm_mul(G.perm_mul(G.perm_inv(ph), g), ph)   # phi^-1 g phi
        ord2 = G.group_order(gens + [conj])
        if ord2 != expected:
            norm_ok = False
            print(f"   generator {gi} conjugate not in PGL (order {ord2})")
    check("phi normalises the generated PGL group (all 8 conjugates in PGL)", norm_ok)
    ord_phi = G.group_order(gens + [ph])
    check(f"<PGL, phi> has order {ord_phi} = 3*|PGL| = 49,448,448",
          ord_phi == 3 * expected == 49_448_448)
    check("phi is not in PGL (|PGL| != |<PGL,phi>|)", ord_phi != expected)
    results["pgamma_order"] = ord_phi
    results["phi_normalises_pgl"] = norm_ok
    results["phi_in_pgl"] = (ord_phi == expected)

    # ---------------------------------------------------------- summary
    failed = [c for c in checks if not c[1]]
    results["checks"] = [{"name": n, "passed": p, "detail": d} for n, p, d in checks]
    results["n_checks"] = len(checks)
    results["n_failed"] = len(failed)
    results["elapsed_sec"] = time.time() - t_start
    with open(os.path.join(HERE, "core_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    print(f"\n{len(checks)} checks, {len(failed)} failed, {results['elapsed_sec']:.1f}s")
    print("core_results.json written")
    return 0 if not failed else 1

if __name__ == "__main__":
    sys.exit(main())

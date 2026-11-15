#!/usr/bin/env python3
"""ge20 + intersection cuts from the published local-exclusion theorems.

Cuts (all rigorous, from saturation-20261003-extra.md complete enumerations):
  (X1) no safe 20-set S with |S ∩ T| >= 10  (T = 19-stone safe maximal set)
  (X2) no safe 20-set S with |S ∩ U| >= 10  (U = near-safe 20-set)
By D4 symmetry of B_10 (bijections preserve safety and size), (X1)/(X2)
hold for every D4 image g(T), g(U). We encode at-most-9 over each distinct
D4 image of T and of U as biconditional sequential counters with a negative
unit on the final at-least-10 node.

Controls:
  (K1) K0035 19-witness: 0 violations over quad+cut clauses.
  (K2) T itself violates the T-image cut (|T ∩ T| = 19 > 9).
  (K3) U itself violates the U-image cut (|U ∩ U| = 20 > 9).
  (K4) T is safe (0 quad-clause violations).
"""
from build_n10_sat import N, NUM, forbidden_quadruples, write_cnf, build

T = [0, 7, 8, 14, 16, 20, 21, 31, 35, 42, 47, 67, 69, 70, 73, 82, 89, 93, 99]
U = [2, 6, 16, 18, 21, 25, 32, 35, 40, 59, 62, 67, 74, 77, 78, 80, 81, 83, 97, 99]
WIT = [9, 15, 16, 18, 20, 22, 30, 36, 44, 58, 62, 65, 67, 70, 71, 87, 91, 93, 97]


def d4_images(cells):
    """All D4 images of a cell set on the (N-1)x(N-1) square, as frozensets."""
    pts = [(c % N, c // N) for c in cells]
    imgs = set()
    for k in range(4):
        rot = [(y, N - 1 - x) for (x, y) in pts]
        pts = rot
        for refl in [False, True]:
            final = [(N - 1 - x, y) for (x, y) in rot] if refl else rot
            imgs.add(frozenset(x + N * y for (x, y) in final))
    return imgs


def at_most_clauses(varlist, m, voff):
    """at-most-m over the given variable list (1-based var = cell+1).
    Biconditional at-least-(m+1) counter with negative unit on the final node."""
    n = len(varlist)
    k = m + 1

    def s(i, j):
        return voff + (i - 1) * k + j

    clauses = []
    for j in range(1, k + 1):
        if j == 1:
            clauses.append([-varlist[0], s(1, 1)])
            clauses.append([-s(1, 1), varlist[0]])
        else:
            clauses.append([-s(1, j)])
    for i in range(2, n + 1):
        for j in range(1, k + 1):
            clauses.append([-s(i - 1, j), s(i, j)])
            if j == 1:
                clauses.append([-varlist[i - 1], s(i, 1)])
            else:
                clauses.append([-varlist[i - 1], -s(i - 1, j - 1), s(i, j)])
            clauses.append([-s(i, j), s(i - 1, j), varlist[i - 1]])
            if j >= 2:
                clauses.append([-s(i, j), s(i - 1, j), s(i - 1, j - 1)])
    clauses.append([-s(n, k)])
    return clauses, s, n * k


def main():
    quads = forbidden_quadruples(N)
    quad_clauses = [[-(q[0] + 1), -(q[1] + 1), -(q[2] + 1), -(q[3] + 1)] for q in quads]

    t_imgs = d4_images(T)
    u_imgs = d4_images(U)
    print("distinct D4 images: T=%d, U=%d" % (len(t_imgs), len(u_imgs)))

    nvars, base_clauses, s20 = build(NUM, 20)
    clauses = list(base_clauses) + quad_clauses

    voff = nvars
    cut_count = 0
    for imgset in sorted(t_imgs | u_imgs, key=lambda f: sorted(f)[:1]):
        cells = sorted(imgset)
        assert all(0 <= c < NUM for c in cells), "image outside board"
        assert len(cells) in (19, 20), "unexpected image size %d" % len(cells)
        cls, sfn, used = at_most_clauses([c + 1 for c in cells], 9, voff)
        clauses += cls
        voff += used
        cut_count += 1
    total_vars = voff
    write_cnf("n10_ge20_cuts.cnf", total_vars, clauses)
    print("n10_ge20_cuts.cnf: vars=%d clauses=%d cuts=%d" % (total_vars, len(clauses), cut_count))

    # ---- controls ----
    witset = set(WIT)
    tset, uset = set(T), set(U)

    cut_specs = [sorted(g) for g in sorted(t_imgs | u_imgs, key=lambda f: sorted(f)[:1])]
    blocks = []
    off = 2100  # voff convention: first counter var = off+1
    for cells in cut_specs:
        blocks.append((off, cells))
        off += len(cells) * 10

    def eval_cuts(cells_set, clause_pool):
        viol = 0
        for cl in clause_pool:
            sat_flag = False
            for v in cl:
                a = abs(v)
                neg = v < 0
                if a <= NUM:
                    val = (a - 1) in cells_set
                else:
                    found = False
                    for (boff, cells) in blocks:
                        if boff < a <= boff + len(cells) * 10:
                            j = (a - boff - 1) % 10 + 1
                            i = (a - boff - 1) // 10 + 1
                            cnt = sum(1 for t in range(i) if cells[t] in cells_set)
                            val = cnt >= j
                            found = True
                            break
                    if not found:
                        raise RuntimeError("unknown var %d" % a)
                if (not val) if neg else val:
                    sat_flag = True
                    break
            if not sat_flag:
                viol += 1
        return viol

    cut_clauses = []
    for i, cells in enumerate(cut_specs):
        cls, _, _ = at_most_clauses([c + 1 for c in cells], 9, blocks[i][0])
        cut_clauses += cls

    v1 = eval_cuts(witset, quad_clauses + cut_clauses)
    print("K1 witness vs quads+cuts violations: %d (expect 0)" % v1)
    v2 = eval_cuts(tset, cut_clauses)
    print("K2 T vs all cuts violations: %d (expect >=1; T hits its own image cut)" % v2)
    v3 = eval_cuts(uset, cut_clauses)
    print("K3 U vs all cuts violations: %d (expect >=1; U hits its own image cut)" % v3)
    v4 = eval_cuts(tset, quad_clauses)
    print("K4 T safe check (quads only): %d (expect 0)" % v4)


if __name__ == "__main__":
    main()

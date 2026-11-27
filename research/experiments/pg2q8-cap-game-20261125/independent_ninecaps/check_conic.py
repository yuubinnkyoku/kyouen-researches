"""Task 2: conics in PG(2,8) via quadratic forms.

Q(x,y,z) = a x^2 + b y^2 + c z^2 + d xy + e xz + f yz  (characteristic 2:
each cross term once; x^2 are Frobenius squares, not bilinear).

All projective quadratic forms are enumerated; a conic is a form whose zero
set is a 9-cap.  Also checks that the example 9-cap is NOT a conic by showing
the 9x6 evaluation matrix has rank 6 over GF(8).
"""
import json
import os

from pg8 import MUL, INV, PTS, inc

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")


def mono(p):
    x, y, z = p
    return (MUL[x][x], MUL[y][y], MUL[z][z],
            MUL[x][y], MUL[x][z], MUL[y][z])


MONO = [mono(p) for p in PTS]


def eval_form(coef, pidx):
    m = MONO[pidx]
    return (MUL[coef[0]][m[0]] ^ MUL[coef[1]][m[1]] ^ MUL[coef[2]][m[2]]
            ^ MUL[coef[3]][m[3]] ^ MUL[coef[4]][m[4]] ^ MUL[coef[5]][m[5]])


def rref_rank(rows, ncols):
    """Rank over GF(8) of a list of rows (mutable copy inside)."""
    A = [list(r) for r in rows]
    nrows = len(A)
    rank = 0
    for col in range(ncols):
        piv = None
        for r in range(rank, nrows):
            if A[r][col]:
                piv = r
                break
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        invc = INV[A[rank][col]]
        A[rank] = [MUL[invc][v] for v in A[rank]]
        for r in range(nrows):
            if r != rank and A[r][col]:
                f = A[r][col]
                A[r] = [a ^ MUL[f][b] for a, b in zip(A[r], A[rank])]
        rank += 1
        if rank == nrows:
            break
    return rank


def solve_kernel(rows, ncols):
    """Dimension of the solution space of rows * v = 0 over GF(8)."""
    return ncols - rref_rank(rows, ncols)


def main():
    I = inc()
    out = {}
    os.makedirs(ART, exist_ok=True)

    # ---------- 1. the example is not a conic ----------
    S = [2, 3, 10, 12, 21, 45, 47, 50, 52]
    rows = [MONO[p] for p in S]
    rank = rref_rank(rows, 6)
    out["example_rows_rank"] = rank
    out["example_kernel_dim"] = 6 - rank
    out["example_not_conic"] = (rank == 6)
    # explicit: the only form vanishing on all nine points is 0
    out["example_forms_vanishing"] = 1 if rank == 6 else None  # only zero form

    # ---------- 2. all projective quadratic forms ----------
    forms = []
    # canonical: first nonzero coefficient in order (a,b,c,d,e,f) equals 1
    for a in range(8):
        for b in range(8):
            for c in range(8):
                for d in range(8):
                    for e in range(8):
                        for f in range(8):
                            coef = (a, b, c, d, e, f)
                            if coef == (0, 0, 0, 0, 0, 0):
                                continue
                            first = next(v for v in coef if v)
                            if first != 1:
                                continue
                            forms.append(coef)
    out["n_projective_forms"] = len(forms)
    assert len(forms) == (8 ** 6 - 1) // 7

    size_hist = {}
    conic_masks = {}
    zero_of_form = {}
    nine_point_sets = []
    for coef in forms:
        z = tuple(p for p in range(73) if eval_form(coef, p) == 0)
        size_hist[len(z)] = size_hist.get(len(z), 0) + 1
        if len(z) == 9:
            m = 0
            for p in z:
                m |= 1 << p
            zero_of_form[coef] = z
            nine_point_sets.append((coef, z, m))

    out["zero_set_size_histogram"] = {str(k): v for k, v in sorted(size_hist.items())}

    n_cap = 0
    for coef, z, m in nine_point_sets:
        if I.is_cap(z):
            n_cap += 1
            conic_masks.setdefault(m, []).append(coef)
    out["n_forms_with_9point_cap_zero_set"] = n_cap
    out["n_distinct_conics"] = len(conic_masks)
    out["conic_multiplicities"] = sorted({len(v) for v in conic_masks.values()})
    out["expected_conics_8_5_minus_8_2"] = 8 ** 5 - 8 ** 2
    out["conic_count_ok"] = (len(conic_masks) == 8 ** 5 - 8 ** 2 == n_cap)

    # each conic is a 9-cap: already checked by construction; double check all
    all_caps = all(I.is_cap(tuple(sorted(z))) for z in
                   ([p for p in range(73) if (m >> p) & 1] for m in conic_masks))
    out["each_conic_is_9cap"] = all_caps

    # every 9-point zero set that is not a cap must be a line (repeated line)
    noncap_9 = []
    for coef, z, m in nine_point_sets:
        if not I.is_cap(z):
            noncap_9.append((coef, z))
    out["n_forms_9point_noncap"] = len(noncap_9)
    # verify each such zero set is a line
    is_lines = []
    for coef, z in noncap_9:
        lens = {I.lof[z[i]][z[j]] for i in range(9) for j in range(i + 1, 9)}
        is_lines.append(len(lens) == 1)
    out["all_9point_noncap_are_lines"] = all(is_lines)

    # save conic masks (as point tuples) for task 4
    conics = [tuple(sorted(p for p in range(73) if (m >> p) & 1)) for m in conic_masks]
    conics.sort()
    with open(os.path.join(ART, "conics.txt"), "w") as f:
        for c in conics:
            f.write(" ".join(map(str, c)) + "\n")
    out["saved_conics"] = len(conics)

    print("== example ==")
    print("  evaluation matrix rank:", rank, "kernel dim:", 6 - rank,
          "=> only zero form vanishes:", rank == 6)
    print("== quadratic forms ==")
    print("  projective forms:", len(forms))
    print("  zero-set size histogram:", out["zero_set_size_histogram"])
    print("  9-point zero sets that are caps (forms):", n_cap)
    print("  distinct conics:", len(conic_masks),
          "expected 8^5-8^2 =", 8 ** 5 - 8 ** 2, "ok:", out["conic_count_ok"])
    print("  each conic is a 9-cap:", all_caps)
    print("  nonzero-form multiplicity per conic:", out["conic_multiplicities"])
    print("  forms with 9-point non-cap zero sets:", len(noncap_9),
          "all lines:", out["all_9point_noncap_are_lines"])

    with open(os.path.join(ART, "task2.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print("\nPASS task2:", out["example_not_conic"] and out["conic_count_ok"]
          and all_caps)


if __name__ == "__main__":
    main()

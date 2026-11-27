"""Task 3: PGL(3,8) from GF(8) -- group order, collineation action, cap orbits.

Group order is obtained two independent ways:
  (A) exact Schreier stabilizer chain (Schreier's lemma; the final stabilizer
      generators all become identity, so the product of orbit lengths is the
      exact order);
  (B) a constructive certificate: the generated matrix group contains all 42
      transvections of SL(3,8) (conjugacy orbit of one generator transvection),
      hence contains SL(3,8), hence its projective image is PGL(3,8).
"""
import json
import os
import time

from pg8 import MUL, INV, PTS, PTIDX, canon, inc

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")
N = 73


# ------------------------------------------------------------- matrices ----
def mat_apply(M, v):
    return tuple(
        MUL[v[0]][M[0][j]] ^ MUL[v[1]][M[1][j]] ^ MUL[v[2]][M[2][j]]
        for j in range(3))


def mat_mul(A, B):
    return tuple(tuple(
        MUL[A[i][0]][B[0][j]] ^ MUL[A[i][1]][B[1][j]] ^ MUL[A[i][2]][B[2][j]]
        for j in range(3)) for i in range(3))


def mat_inv(M):
    # over GF(8): invertible; use cofactors (char 2)
    (a, b, c), (d, e, f), (g, h, i) = M
    A = (MUL[e][i] ^ MUL[f][h], MUL[c][h] ^ MUL[b][i], MUL[b][f] ^ MUL[c][e])
    B = (MUL[f][g] ^ MUL[d][i], MUL[a][i] ^ MUL[c][g], MUL[c][d] ^ MUL[a][f])
    C = (MUL[d][h] ^ MUL[e][g], MUL[b][g] ^ MUL[a][h], MUL[a][e] ^ MUL[b][d])
    det = (MUL[a][A[0]] ^ MUL[b][B[0]] ^ MUL[c][C[0]])
    det_inv = INV[det]
    return tuple(tuple(MUL[det_inv][x] for x in row) for row in (A, B, C))


def mat_perm(M):
    """Permutation of the 73 board points induced by v -> v M."""
    perm = []
    for p in range(N):
        w = mat_apply(M, PTS[p])
        assert w != (0, 0, 0)
        perm.append(PTIDX[canon(w)])
    assert len(set(perm)) == N
    return tuple(perm)


def mat_det(M):
    (a, b, c), (d, e, f), (g, h, i) = M
    return (MUL[a][MUL[e][i] ^ MUL[f][h]]
            ^ MUL[b][MUL[f][g] ^ MUL[d][i]]
            ^ MUL[c][MUL[d][h] ^ MUL[e][g]])


# --------------------------------------------------------- permutations -----
def compose(f, g):
    """(f o g)(i) = f[g[i]]  (apply g then f)."""
    return tuple(f[g[i]] for i in range(N))


def inverse(p):
    q = [0] * N
    for i, v in enumerate(p):
        q[v] = i
    return tuple(q)


IDENT = tuple(range(N))


def orbit_transversal(gens, b):
    orb = {b: IDENT}
    queue = [b]
    while queue:
        x = queue.pop()
        ux = orb[x]
        for g in gens:
            y = g[x]
            if y not in orb:
                orb[y] = compose(g, ux)
                queue.append(y)
    return orb


def schreier_chain_order(gens, base):
    """Exact |<gens>| via a stabilizer chain (Schreier's lemma).

    base may be extended automatically until the final stabilizer generators
    are all the identity, so the product of orbit lengths is exact.
    """
    levels = []
    cur = list(dict.fromkeys(gens))
    order = 1
    b_idx = 0
    while True:
        if b_idx < len(base):
            b = base[b_idx]
        else:
            # find a point moved by some remaining generator
            b = None
            for g in cur:
                if g != IDENT:
                    b = next(i for i in range(N) if g[i] != i)
                    break
            if b is None:
                break  # cur = {identity}: final stabilizer trivial
        orb = orbit_transversal(cur, b)
        order *= len(orb)
        levels.append((b, len(orb), len(cur)))
        # Schreier generators of the stabilizer of everything fixed so far + b
        new = []
        seen = set()
        for x, ux in orb.items():
            for g in cur:
                y = g[x]
                s = compose(inverse(orb[y]), compose(g, ux))
                if s != IDENT and s not in seen:
                    seen.add(s)
                    new.append(s)
        cur = new
        b_idx += 1
        if b_idx > 40:
            raise RuntimeError("chain failed to terminate")
    return order, levels, cur


# ------------------------------------------------------------- checks ------
def main():
    t0 = time.time()
    I = inc()
    out = {}
    os.makedirs(ART, exist_ok=True)

    # Generators, chosen by hand:
    #   P : (a,b,c) -> (b,c,a)          coordinate 3-cycle
    #   S12 : (a,b,c) -> (a+b,b,c)      transvection x12(1)
    #   S23 : (a,b,c) -> (a,b+c,c)      transvection x23(1)
    #   S13 : (a,b,c) -> (a+c,b,c)      transvection x13(1)
    #   D : (a,b,c) -> (a,2b,c)         diagonal scaling
    P = ((0, 0, 1), (1, 0, 0), (0, 1, 0))
    S12 = ((1, 0, 0), (1, 1, 0), (0, 0, 1))
    S23 = ((1, 0, 0), (0, 1, 0), (0, 1, 1))
    S13 = ((1, 0, 0), (0, 1, 0), (1, 0, 1))
    D = ((1, 0, 0), (0, 2, 0), (0, 0, 1))
    mats = {"P": P, "S12": S12, "S23": S23, "S13": S13, "D": D}

    out["generators"] = {k: v for k, v in mats.items()}
    dets = {k: mat_det(v) for k, v in mats.items()}
    out["determinants"] = dets
    out["all_invertible"] = all(d != 0 for d in dets.values())

    gens = []
    for name, M in mats.items():
        p = mat_perm(M)
        gens.append(p)
        # collineation check against the board line set
        blines = {frozenset(L) for L in I.board_lines}
        img = {frozenset(p[i] for i in L) for L in I.board_lines}
        assert img <= blines, name
        assert len(img) == 73
    out["all_generators_are_collineations"] = True
    out["generator_orders"] = {}
    for name, p in zip(mats, gens):
        q = IDENT
        k = 0
        while True:
            k += 1
            q = compose(p, q)
            if q == IDENT:
                break
            if k > 100:
                break
        out["generator_orders"][name] = k
    print("generator orders:", out["generator_orders"])

    # ---------- (A) exact order via Schreier chain ----------
    base = [9, 1, 17, 0, 10]  # [1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1]
    t1 = time.time()
    order, levels, resid = schreier_chain_order(gens, base)
    out["schreier_order"] = order
    out["schreier_levels"] = [{"base": b, "orbit": o, "ngen": n} for b, o, n in levels]
    out["schreier_all_residual_identity"] = all(g == IDENT for g in resid)
    out["schreier_seconds"] = round(time.time() - t1, 2)
    pgl = ((8 ** 3 - 1) * (8 ** 3 - 8) * (8 ** 3 - 8 ** 2)) // 7
    out["formula_PGL_order"] = pgl
    out["order_ok"] = (order == pgl == 16482816)
    print("Schreier chain:", [(b, o) for b, o, n in levels])
    print("order =", order, " formula =", pgl, " ok:", out["order_ok"],
          f" ({out['schreier_seconds']}s)")

    # ---------- (B) transvection certificate ----------
    # conjugacy orbit of S12 under the generator matrices
    inv_mats = {k: mat_inv(v) for k, v in mats.items()}
    start = S12
    seen = {start}
    frontier = [start]
    while frontier:
        nf = []
        for A in frontier:
            for name, G in mats.items():
                B = mat_mul(mat_mul(G, A), inv_mats[name])
                if B not in seen:
                    seen.add(B)
                    nf.append(B)
        frontier = nf
    # Elations of PG(2,8) = (centre, axis through centre, lambda in GF(8)*)
    #                         = 73 * 9 * 7 = 4599; these are exactly the
    #                         transvections of SL(3,8).
    n_elations = 73 * 9 * 7
    out["transvection_orbit_size"] = len(seen)
    out["expected_all_elations"] = n_elations
    out["transvection_orbit_is_all_elations"] = (len(seen) == n_elations)
    # each conjugate should be an involutory elation with exactly 9 fixed points
    ok_elation = True
    ok_det1 = True
    for B in seen:
        if mat_det(B) != 1:
            ok_det1 = False
        BB = mat_mul(B, B)
        # projective order 2: BB is a scalar matrix
        lam = BB[0][0]
        if not (lam != 0 and all(BB[i][j] == (lam if i == j else 0)
                                for i in range(3) for j in range(3))):
            ok_elation = False
            break
        p = mat_perm(B)
        fix = sum(1 for i in range(N) if p[i] == i)
        if fix != 9:
            ok_elation = False
            break
    out["all_conjugates_are_elations_fixing_a_line"] = ok_elation
    out["all_conjugates_in_SL"] = ok_det1
    print("transvection conjugacy orbit:", len(seen),
          "(expected all elations", n_elations, ":",
          out["transvection_orbit_is_all_elations"],
          ", all elations:", ok_elation, ", det 1:", ok_det1, ")")
    out["lower_bound_SL_PSL_PGL"] = (
        out["transvection_orbit_is_all_elations"] and ok_elation and ok_det1)

    # second chain with a different base point order (sanity)
    order2, levels2, resid2 = schreier_chain_order(gens, [0, 9, 10, 1, 17])
    out["schreier_order_alt_base"] = order2
    out["schreier_orders_agree"] = (order2 == order)

    # ---------- orbits of caps ----------
    def image_mask(perm, mask):
        out_m = 0
        m = mask
        while m:
            b = m & -m
            p = b.bit_length() - 1
            out_m |= 1 << perm[p]
            m ^= b
        return out_m

    def orbit_of_mask(mask, gens_used):
        seen = {mask}
        queue = [mask]
        qi = 0
        while qi < len(queue):
            x = queue[qi]
            qi += 1
            for g in gens_used:
                y = image_mask(g, x)
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        return seen

    example = (2, 3, 10, 12, 21, 45, 47, 50, 52)
    emask = 0
    for p in example:
        emask |= 1 << p
    t2 = time.time()
    eorb = orbit_of_mask(emask, gens)
    with open(os.path.join(ART, "orbit_example.pkl"), "wb") as f:
        import pickle
        pickle.dump(sorted(eorb), f)
    out["example_cap"] = list(example)
    out["example_orbit_size"] = len(eorb)
    out["example_orbit_seconds"] = round(time.time() - t2, 2)
    out["expected_nonconic"] = 294336
    out["stabilizer_order_example"] = order // len(eorb)
    out["example_orbit_ok"] = (len(eorb) == 294336)
    print("example 9-cap orbit:", len(eorb),
          " stabilizer:", out["stabilizer_order_example"],
          f" ({out['example_orbit_seconds']}s)")

    # orbit of a conic (first conic from task 2)
    conics_file = os.path.join(ART, "conics.txt")
    if os.path.exists(conics_file):
        with open(conics_file) as f:
            first = tuple(int(t) for t in f.readline().split())
        cmask = 0
        for p in first:
            cmask |= 1 << p
        t3 = time.time()
        corb = orbit_of_mask(cmask, gens)
        with open(os.path.join(ART, "orbit_conic.pkl"), "wb") as f:
            import pickle
            pickle.dump(sorted(corb), f)
        out["conic_orbit_size"] = len(corb)
        out["stabilizer_order_conic"] = order // len(corb)
        out["conic_orbit_ok"] = (len(corb) == 32704)
        out["conic_orbit_seconds"] = round(time.time() - t3, 2)
        print("conic orbit:", len(corb), " stabilizer:", order // len(corb),
              f" ({out['conic_orbit_seconds']}s)")
    else:
        out["conic_orbit_size"] = None

    with open(os.path.join(ART, "task3.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print("\nPASS task3:", out["all_generators_are_collineations"] and out["order_ok"]
          and out["example_orbit_ok"] and out.get("conic_orbit_ok"))
    print("elapsed", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()

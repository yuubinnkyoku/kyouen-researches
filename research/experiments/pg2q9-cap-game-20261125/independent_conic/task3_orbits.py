"""Task 3 - PGL(2,9) orbits on k-subsets of 10 points, for k = 3..9:
the abstract PGL(2,9) action on PG(1,9) and the stabiliser of C acting on C."""
import itertools
import json

import conic as K
import gf9 as F
import pg9 as P

OUT = "results_task3.json"


# ---------------------------------------------------------------- PGL(2,9)
def pgl2_perms():
    """All 720 projectivities of PG(1,9) as permutations of labels 0..8
    (t -> (1:t)) and 9 (the point at infinity (0:1))."""
    perms = set()
    for a in range(9):
        for b in range(9):
            for c in range(9):
                for d in range(9):
                    if F.sub(F.MUL[a][d], F.MUL[b][c]) == 0:
                        continue
                    perm = []
                    for lab in range(10):
                        if lab < 9:
                            num = F.ADD[F.MUL[a][lab]][b]
                            den = F.ADD[F.MUL[c][lab]][d]
                        else:
                            num, den = a, c
                        if den == 0:
                            perm.append(9)
                        else:
                            perm.append(F.MUL[num][F.INV[den]])
                    perms.add(tuple(perm))
    return sorted(perms)


def orbit_partition(perms, n, k):
    """Orbits of the permutation group on k-subsets of {0..n-1}.

    Returns a list of dicts {"size", "members" (frozenset of frozensets),
    "rep" (the lexicographically smallest member as a tuple)}, sorted by
    decreasing size then by representative."""
    subsets = [frozenset(s) for s in itertools.combinations(range(n), k)]
    seen = set()
    orbits = []
    for s in subsets:
        if s in seen:
            continue
        orb = set()
        stack = [s]
        while stack:
            cur = stack.pop()
            if cur in orb:
                continue
            orb.add(cur)
            for g in perms:
                img = frozenset(g[x] for x in cur)
                if img not in orb:
                    stack.append(img)
        seen |= orb
        orbits.append({"size": len(orb),
                       "members": frozenset(orb),
                       "rep": min(tuple(sorted(x)) for x in orb)})
    orbits.sort(key=lambda o: (-o["size"], o["rep"]))
    return orbits


def apply_perm_group(perms, s):
    return {frozenset(g[x] for x in s) for g in perms}


def main():
    res = {}
    # ---- the Möbius / 2x2 group --------------------------------------
    perms = pgl2_perms()
    res["pgl2_9"] = {
        "order": len(perms),
        "expected": 720,
        "faithful": len({p[0] for p in perms}) == 10,
        "triples_images_distinct": len({(p[0], p[1], p[2]) for p in perms}) == 720,
        "sharply_3_transitive": len({(p[0], p[1], p[2]) for p in perms}) == 10 * 9 * 8,
    }

    # ---- consistency with the explicit Moebius matrices on the standard
    #      conic: both must give the same permutation group on 10 points.
    S = K.standard_conic_mask()
    tlabel = {}
    for t in range(9):
        pt = F.normalise((F.MUL[t][t], t, 1))
        tlabel[P.LABEL[pt]] = t
    tlabel[P.LABEL[(1, 0, 0)]] = 9
    mats = K.mobius_matrices()
    perms2 = set()
    for M in mats:
        perm = []
        for lab in range(10):
            # point of S with label lab (tlabel is a bijection)
            src = next(i for i, t in tlabel.items() if t == lab)
            dst = P.LABEL[F.normalise(P.mat_vec(M, P.POINTS[src]))]
            perm.append(tlabel[dst])
        perms2.add(tuple(perm))
    res["pgl2_9"]["explicit_matrix_action_matches"] = (perms2 == set(perms))
    res["pgl2_9"]["explicit_matrix_count"] = len(mats)
    res["pgl2_9"]["explicit_matrix_group_order"] = len(perms2)

    # ---- orbits on k-subsets of PG(1,9) ------------------------------
    abstract = {}
    for k in range(3, 10):
        orbits = orbit_partition(perms, 10, k)
        abstract[k] = [o["size"] for o in orbits]
        res.setdefault("pg19_orbits", {})[k] = {
            "sizes": [o["size"] for o in orbits],
            "total": sum(o["size"] for o in orbits),
            "expected_total": len(list(itertools.combinations(range(10), k))),
            "representatives": [list(o["rep"]) for o in orbits],
        }

    # ---- the stabiliser of C acting on C ----------------------------
    stabmats = K.stabiliser(K.C_MASK, cache=K.STAB_CACHE)
    stab_perms = K.permutations_on(K.C_MASK, stabmats)
    Cpts = P.bits(K.C_MASK)
    res["stab_C"] = {
        "order": len(stabmats),
        "distinct_perms": len(set(stab_perms)),
        "perm_group_equals_pgl2_9_up_to_relabelling": None,
    }
    # explicit relabelling via the parameterisation T: standard conic -> C
    T, Tinv = K.parameterisation()
    psi = {}
    for lab in range(10):
        src = next(i for i, t in tlabel.items() if t == lab)
        psi[lab] = P.LABEL[F.normalise(P.mat_vec(T, P.POINTS[src]))]
    # psi maps a PG(1,9) label to a point of C; conjugate the abstract group
    conj = set()
    for g in perms:
        perm = []
        for i in Cpts:
            lab = next(l for l in range(10) if psi[l] == i)
            j = psi[g[lab]]
            perm.append(Cpts.index(j))
        conj.add(tuple(perm))
    res["stab_C"]["perm_group_equals_pgl2_9_up_to_relabelling"] = (
        conj == set(stab_perms))
    res["stab_C"]["psi_is_bijection_onto_C"] = sorted(psi.values()) == sorted(Cpts)

    # ---- orbits on k-subsets of C (claim's orbits) -------------------
    c_orbits = {}
    for k in range(3, 10):
        orbits = orbit_partition(stab_perms, 10, k)
        sizes = [o["size"] for o in orbits]
        # representatives as board point labels
        reps = [sorted(Cpts[i] for i in o["rep"]) for o in orbits]
        c_orbits[k] = {"sizes": sizes, "representatives": reps}
        res.setdefault("C_orbits", {})[k] = {
            "sizes": sizes,
            "total": sum(sizes),
            "expected_total": len(list(itertools.combinations(range(10), k))),
            "representatives_board_labels": reps,
            "matches_pg19_abstract": sizes == abstract[k],
        }
        # also check the transported abstract orbits coincide with the C-orbits
        transported = []
        for o in orbit_partition(perms, 10, k):
            transported.append(frozenset(frozenset(psi[x] for x in s)
                                        for s in o["members"]))
        direct = []
        for o in orbits:
            direct.append(frozenset(frozenset(Cpts[x] for x in s)
                                    for s in o["members"]))
        res["C_orbits"][k]["transported_equals_direct"] = (
            set(transported) == set(direct))

    # ---- claimed orbit sizes -----------------------------------------
    claim = {3: [120], 4: [180, 30], 5: [180, 72], 6: [180, 30],
             7: [120], 8: [45], 9: [10]}
    ok = True
    detail = {}
    for k in range(3, 10):
        got = res["C_orbits"][k]["sizes"]
        exp = claim[k]
        detail[k] = {"computed": got, "claimed": exp,
                     "match": got == exp or sorted(got) == sorted(exp)}
        ok = ok and (sorted(got) == sorted(exp))
    res["claim_check"] = {"ok": ok, "detail": detail}

    # ---- orbit-stabiliser arithmetic, complement symmetry, cross-ratio
    extra = {}
    # (1) |orbit| * |stabiliser| = 720 for every orbit
    os_ok = True
    os_detail = {}
    for k in range(3, 10):
        rows = []
        for orb in orbit_partition(stab_perms, 10, k):
            rep = orb["rep"]
            stab = sum(1 for g in stab_perms
                       if tuple(sorted(g[x] for x in rep)) == rep)
            rows.append({"orbit": orb["size"], "stab": stab,
                         "product": orb["size"] * stab})
            os_ok = os_ok and orb["size"] * stab == 720
        os_detail[k] = rows
    extra["orbit_stabiliser"] = {"ok": os_ok, "detail": os_detail}

    # (2) complement symmetry: k <-> 10-k
    comp_ok = True
    comp_detail = {}
    for k in range(3, 8):
        part_k = orbit_partition(stab_perms, 10, k)
        part_c = orbit_partition(stab_perms, 10, 10 - k)
        # the complement of an orbit of k-subsets is an orbit of (10-k)-subsets
        comps = {frozenset(frozenset(set(range(10)) - set(s))
                           for s in orb["members"]) for orb in part_k}
        part_c_sets = {orb["members"] for orb in part_c}
        comp_detail[k] = {
            "sizes_k": sorted(o["size"] for o in part_k),
            "sizes_10-k": sorted(o["size"] for o in part_c),
            "complements_match": comps == part_c_sets,
        }
        comp_ok = comp_ok and comps == part_c_sets
    extra["complement_symmetry"] = {"ok": comp_ok, "detail": comp_detail}

    # (3) cross-ratio check of the k=4 split: harmonic 4-subsets (cross-ratio
    # class of -1) form the orbit of size 30.
    tlabel = {}
    for t in range(9):
        pt = F.normalise((F.MUL[t][t], t, 1))
        tlabel[P.LABEL[pt]] = t
    tlabel[P.LABEL[(1, 0, 0)]] = 9
    psi4 = {}
    for lab in range(10):
        src = next(i for i, tt in tlabel.items() if tt == lab)
        psi4[lab] = P.LABEL[F.normalise(P.mat_vec(T, P.POINTS[src]))]
    inv_psi4 = {v: k for k, v in psi4.items()}
    triple_to_inv = {}
    for g in perms:
        ginv = [0] * 10
        for xx in range(10):
            ginv[g[xx]] = xx
        triple_to_inv[(g[0], g[1], g[9])] = ginv
    Cpts4 = P.bits(K.C_MASK)
    harm = set()
    for quad in itertools.combinations(range(10), 4):
        labs = [inv_psi4[Cpts4[i]] for i in quad]
        ginv = triple_to_inv[(labs[0], labs[1], labs[2])]
        if ginv[labs[3]] == 2:          # cross-ratio -1
            harm.add(frozenset(Cpts4[i] for i in quad))
    thirty = [orb for orb in orbit_partition(stab_perms, 10, 4)
              if orb["size"] == 30][0]
    thirty = {frozenset(Cpts4[i] for i in s) for s in thirty["members"]}
    extra["cross_ratio_k4"] = {
        "harmonic_count": len(harm),
        "equals_30_orbit": harm == thirty,
        "harmonic_rep_is_{0,1,10,45}": frozenset([0, 1, 10, 45]) in harm,
        "generic_rep_is_{0,1,10,20}": frozenset([0, 1, 10, 20]) not in harm,
    }
    res["extra_checks"] = extra

    res["pass"] = (res["pgl2_9"]["order"] == 720
                   and res["pgl2_9"]["sharply_3_transitive"]
                   and res["pgl2_9"]["explicit_matrix_action_matches"]
                   and res["stab_C"]["order"] == 720
                   and res["stab_C"]["perm_group_equals_pgl2_9_up_to_relabelling"]
                   and all(res["C_orbits"][k]["matches_pg19_abstract"]
                           and res["C_orbits"][k]["transported_equals_direct"]
                           for k in range(3, 10))
                   and extra["orbit_stabiliser"]["ok"]
                   and extra["complement_symmetry"]["ok"]
                   and extra["cross_ratio_k4"]["equals_30_orbit"]
                   and extra["cross_ratio_k4"]["harmonic_count"] == 30
                   and ok)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))
    print("\nTASK3:", "PASS" if res["pass"] else "FAIL")


if __name__ == "__main__":
    main()

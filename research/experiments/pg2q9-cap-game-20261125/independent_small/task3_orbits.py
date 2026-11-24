"""Task 3: PGL(3,9) generators, |PGL(3,9)|, and the orbits of {0,1,10}, {0,1,10,20}.

* |PGL(3,9)| from ordered bases: (9^3-1)(9^3-9)(9^3-9^2)/(9-1)
* a certificate that the 14 explicit generators generate all of PGL(3,9):
  a Schreier stabilizer chain whose orbit-length product reaches 42,456,960
  (a lower bound for |<gens>|; combined with <gens> <= PGL(3,9) it is equality)
* orbit BFS over 91-bit masks
* stabilizer orders by direct enumeration of the matrices fixing the cap
"""
import json
import time

import core

N = 91
CAP3 = (0, 1, 10)
CAP4 = (0, 1, 10, 20)


# ------------------------------------------------------------------ group order
def pgl_order():
    q = 9
    n_bases = (q ** 3 - 1) * (q ** 3 - q) * (q ** 3 - q ** 2)
    return n_bases // (q - 1), n_bases


# ------------------------------------------------------------------ Schreier chain
def orbit_transversal(gens, beta):
    """orbit of beta and a transversal: u[delta] maps beta -> delta"""
    uid = tuple(range(N))
    u = {beta: uid}
    order = [beta]
    queue = [beta]
    while queue:
        nxt = []
        for delta in queue:
            ud = u[delta]
            for g in gens:
                img = g[delta]
                if img not in u:
                    # u[img] = g * u[delta]
                    u[img] = tuple(g[ud[x]] for x in range(N))
                    order.append(img)
                    nxt.append(img)
        queue = nxt
    return order, u


def stabilizer_gens(gens, beta):
    order, u = orbit_transversal(gens, beta)
    uid = tuple(range(N))
    out = []
    seen = {uid}
    for delta in order:
        ud = u[delta]
        for g in gens:
            img = g[delta]
            ui = u[img]
            inv_ui = [0] * N
            for x in range(N):
                inv_ui[ui[x]] = x
            # s(x) = u[img]^{-1}( g( u[delta](x) ) )   fixes beta
            s = tuple(inv_ui[g[ud[x]]] for x in range(N))
            assert s[beta] == beta
            if s in seen:
                continue
            seen.add(s)
            out.append(s)
    return out, len(order)


def group_order_via_chain(gens, max_levels=8):
    chain = []
    cur = list(gens)
    while True:
        moved = set()
        for g in cur:
            moved.update(i for i in range(N) if g[i] != i)
        if not moved:
            break
        beta = min(moved)
        stab, osize = stabilizer_gens(cur, beta)
        chain.append({"base": beta, "orbit": osize, "n_stab_gens": len(stab)})
        cur = stab
        if len(chain) > max_levels:
            raise RuntimeError("chain too long")
    prod = 1
    for c in chain:
        prod *= c["orbit"]
    return prod, chain


# ------------------------------------------------------------------ orbits
def act(mask, g, bit):
    r = 0
    m = mask
    while m:
        b = m & -m
        r |= bit[g[b.bit_length() - 1]]
        m ^= b
    return r


def orbit_size_bfs(start, perms):
    bit = [1 << i for i in range(N)]
    seen = {start}
    frontier = [start]
    while frontier:
        nxt = []
        for m in frontier:
            for g in perms:
                im = act(m, g, bit)
                if im not in seen:
                    seen.add(im)
                    nxt.append(im)
        frontier = nxt
    return len(seen), seen


# ------------------------------------------------------------------ stabilizers
def vectors_of_cap(cap):
    return [core.PTS[p] for p in cap]


def _matrix_from_columns(cols):
    return tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))


def stabilizer_order_by_matrices(cap):
    """number of projectivities M (matrices modulo scalars) with M(cap) == cap"""
    vecs = vectors_of_cap(cap)
    k = len(vecs)
    # first three points of a cap are never collinear -> a basis
    basis = vecs[:3]
    B = _matrix_from_columns(basis)
    Binv = core.mat_inv(B)
    capset = set()
    for v in vecs:
        capset.add(core.canon(v))
    scalars = [s for s in range(1, 9)]
    count = 0
    from itertools import product
    for targets in product(range(k), repeat=3):
        for lam1, lam2 in product(scalars, repeat=2):
            cols = [core.vsmul(lam1, vecs[targets[0]]),
                    core.vsmul(lam2, vecs[targets[1]]),
                    core.vsmul(core.ONE, vecs[targets[2]])]
            M = core.matmul(_matrix_from_columns(cols), Binv)
            if core.det(M) == 0:
                continue
            img = {core.canon(core.matvec(M, v)) for v in vecs}
            if img == capset:
                count += 1
    return count


def main():
    import sys
    t0 = time.time()
    order, n_bases = pgl_order()
    rest = {
        "n_ordered_bases_GL39": n_bases,
        "pgl_order_formula": order,
        "pgl_order_expected": 42456960,
        "pgl_order_ok": order == 42456960,
    }
    print("|GL(3,9)| =", n_bases, " |PGL(3,9)| =", order)

    gs, names = core.generators()
    perms = [core.mat_perm(M) for M in gs]
    ls = set(core.LINES)
    autos = all({tuple(sorted(p[x] for x in L)) for L in core.LINES} == ls for p in perms)
    rest["generators"] = names
    rest["all_generators_are_collineations"] = autos
    print("generators:", len(names), "all collineations:", autos)

    chain_prod, chain = group_order_via_chain(perms)
    rest["schreier_chain"] = chain
    rest["schreier_chain_product"] = chain_prod
    rest["schreier_chain_reaches_pgl_order"] = chain_prod == order
    rest["seconds_chain"] = round(time.time() - t0, 1)
    print("Schreier chain:", chain, "product =", chain_prod)

    # ---- orbits ----
    t = time.time()
    m3 = core.cap_mask(CAP3)
    assert core.is_cap(CAP3)
    n3, orb3 = orbit_size_bfs(m3, perms)
    rest["cap3"] = {"cap": list(CAP3), "orbit_size": n3,
                    "orbit_is_all_3caps": n3 == 110565,
                    "seconds": round(time.time() - t, 1)}
    print("orbit of", CAP3, "=", n3, " (all 3-caps: 110565)")
    t = time.time()
    m4 = core.cap_mask(CAP4)
    assert core.is_cap(CAP4)
    n4, orb4 = orbit_size_bfs(m4, perms)
    rest["cap4"] = {"cap": list(CAP4), "orbit_size": n4,
                    "orbit_is_all_4caps": n4 == 1769040,
                    "seconds": round(time.time() - t, 1)}
    print("orbit of", CAP4, "=", n4, " (all 4-caps: 1769040)")

    # orbit members are caps (spot-check + full size argument)
    rest["orbit3_sizes_ok"] = all(bin(m).count("1") == 3 for m in orb3)
    rest["orbit4_sizes_ok"] = all(bin(m).count("1") == 4 for m in orb4)
    rest["orbit3_all_caps"] = all(core.is_cap(core.mask_points(m)) for m in list(orb3)[:3000])
    rest["orbit4_all_caps"] = all(core.is_cap(core.mask_points(m)) for m in list(orb4)[:3000])

    # ---- exact set comparison with the enumerated census ----
    import task2_counts as T2
    caps3 = T2.enumerate_caps3()
    set3 = {core.cap_mask(c) for c in caps3}
    caps4 = T2.enumerate_caps4(caps3)
    set4 = {core.cap_mask(c) for c in caps4}
    rest["orbit3_equals_enumerated_3caps"] = orb3 == set3
    rest["orbit4_equals_enumerated_4caps"] = orb4 == set4
    rest["orbit3_symmetric_difference"] = len(orb3 ^ set3)
    rest["orbit4_symmetric_difference"] = len(orb4 ^ set4)
    print("orbit3 == all enumerated 3-caps:", orb3 == set3)
    print("orbit4 == all enumerated 4-caps:", orb4 == set4)

    # ---- stabilizer orders by matrix enumeration ----
    t = time.time()
    s3 = stabilizer_order_by_matrices(CAP3)
    rest["stab_order_cap3"] = s3
    rest["stab3_expected_384"] = s3 == 384
    print("|Stab({0,1,10})| =", s3)
    s4 = stabilizer_order_by_matrices(CAP4)
    rest["stab_order_cap4"] = s4
    rest["stab4_expected_24"] = s4 == 24
    print("|Stab({0,1,10,20})| =", s4)
    rest["orbit_x_stab_cap3"] = n3 * s3
    rest["orbit_x_stab_cap4"] = n4 * s4
    rest["orbit_stab_identity_3"] = n3 * s3 == order
    rest["orbit_stab_identity_4"] = n4 * s4 == order
    rest["seconds_stab"] = round(time.time() - t, 1)

    with open("out_task3.json", "w", encoding="utf-8") as fh:
        json.dump(rest, fh, indent=1)
    print(json.dumps(rest, indent=1))


if __name__ == "__main__":
    main()

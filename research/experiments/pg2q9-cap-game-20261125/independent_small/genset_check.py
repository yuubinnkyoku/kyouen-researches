"""Which generator sets generate all of PGL(3,9)?

The task suggests transvections E_ij(1), E_ij(i), diag(i,1,1) and a 3-cycle.
We test that set and a small 5-element set, using the Schreier chain of
task3_orbits (product of orbit lengths along the stabiliser chain, which is a
lower bound for the order of the generated group).
"""
import json

import core
import task3_orbits as T3

PGL = 42456960


def order_of(mats):
    perms = [core.mat_perm(M) for M in mats]
    prod, chain = T3.group_order_via_chain(perms)
    return prod, [(c["base"], c["orbit"]) for c in chain]


def main():
    gs, names = core.generators()
    out = {}
    # (a) the set suggested by the verification task: diag(i,1,1)
    sug = [M for M, nm in zip(gs, names) if not nm.startswith("diag")]
    sug.append(((core.I, 0, 0), (0, core.ONE, 0), (0, 0, core.ONE)))   # diag(i,1,1)
    p, ch = order_of(sug)
    out["task_suggested_set"] = {
        "n_generators": len(sug), "order": p, "chain_orbits": ch,
        "generates_full_pgl": p == PGL, "index": PGL // p if PGL % p == 0 else None}
    # (b) my set: diag(1+i,1,1), a primitive element
    p2, ch2 = order_of(gs)
    out["my_set"] = {"n_generators": len(gs), "order": p2, "chain_orbits": ch2,
                     "generates_full_pgl": p2 == PGL}
    # (c) a small 5-element set
    small = [core.transvection(0, 1, core.ONE), core.transvection(1, 2, core.ONE),
             core.transvection(0, 2, core.I),
             ((core.PRIM, 0, 0), (0, core.ONE, 0), (0, 0, core.ONE)),
             ((0, 0, core.ONE), (core.ONE, 0, 0), (0, core.ONE, 0))]
    p3, ch3 = order_of(small)
    out["small_5_set"] = {"n_generators": len(small), "order": p3,
                          "chain_orbits": ch3, "generates_full_pgl": p3 == PGL}
    print(json.dumps(out, indent=1))
    with open("out_gensets.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()

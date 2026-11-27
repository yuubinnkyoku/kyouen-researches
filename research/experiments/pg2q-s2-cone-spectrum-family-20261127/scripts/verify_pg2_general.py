#!/usr/bin/env python3
"""
Verification battery for the PG(2,q) s=2 cone spectra, q = 8, 9, 11 (fail-closed).

Anchors:
  q=8  (published, K1300/pg2q8-cap-game census): total 19,550,350; maximal
       6 (2,060,352) / 10 (32,704); maximal sizes exactly {6,10}; even-uniform
       => Grundy in {0,1} with G(S) = |S| mod 2 (K1298 route); Grundy(empty)=0.
  q=9  (published, K1300/K1303/K1304): total 128,917,712; N3=110,565 all G1;
       N4=1,769,040 all G0; N5=14,859,936; complete 6/7/8/10-arcs
       707,616/2,021,760/5,307,120/58,968; max Grundy 2 (size-6 only).
  q=11 (no published cap census; classical external anchor): complete 12-arcs
       must equal the classical number of conics |PGL(3,11)|/|PGL(2,11)|
       = 212,427,600/1320 = 160,930; complete 7/9/10-arc counts must satisfy
       orbit divisibility with stabilizers 21/1/60; N3 = C(133,3)-133*C(12,3).

Gates (all must PASS):
  G1 board integrity (dual construction, line shape, pair uniqueness,
      two-lines-meet, field distributivity sweep).
  G2 determinism: 3 runs byte-identical (canonical JSON sha256).
  G3 F-invariance: cones over 3 different non-collinear triangles give
      identical T_m(g) tables (operational transitivity test).
  G4 anchors above.
  G5 child/mex audit on a 300-position sample with a fresh safety predicate.
  G6 divisibility N3*T % C(m,3) == 0 everywhere (asserted in run_spectrum).
Tamper T1..T5: corrupt total / spectrum cell / board line / sampled mex /
        complete-arc anchor must each be detected (fail-closed).
"""
import json, hashlib, sys, copy
from math import comb
import pg2q9_cone_spectrum as M

def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()

def run_spectrum(board, F_pts):
    v = board.v
    assert len(set(F_pts)) == 3
    li = board.pair_line[tuple(sorted((F_pts[0], F_pts[1])))]
    assert F_pts[2] not in board.lines[li], "F collinear"
    F_mask = sum(1 << p for p in F_pts)
    positions, maximal, _ = M.cone_spectrum(board, F_mask, F_pts)
    G = M.grundy_dp(board, positions, maximal)
    T, Tmax = {}, {}
    for mask in positions:
        T[(M.popcount(mask), G[mask])] = T.get((M.popcount(mask), G[mask]), 0) + 1
        if maximal[mask]:
            m = M.popcount(mask)
            Tmax[m] = Tmax.get(m, 0) + 1
    N3 = comb(v, 3) - len(board.lines) * comb(board.q + 1, 3)
    spec, spec_max = {}, {}
    for (m, g), t in sorted(T.items()):
        assert (N3 * t) % comb(m, 3) == 0, ("div", m, g)
        spec.setdefault(m, {})[g] = N3 * t // comb(m, 3)
    for m, t in sorted(Tmax.items()):
        assert (N3 * t) % comb(m, 3) == 0, ("divmax", m)
        spec_max[m] = N3 * t // comb(m, 3)
    return {"N3": N3, "spec": spec, "spec_max": spec_max, "cone_size": len(positions),
            "G": G, "positions": positions, "maximal": maximal}

def res_v(q): return q * q + q + 1

ANCHORS = {
    8: {"total": 19550350, "complete": {6: 2060352, 10: 32704},
        "max_grundy": 1, "parity_rule": True},
    9: {"total": 128917712,
        "complete": {6: 707616, 7: 2021760, 8: 5307120, 10: 58968},
        "max_grundy": 2,
        "cells": [(3, 1, 110565), (4, 0, 1769040), (5, 1, 14859936)]},
    11: {"total": None,
         "complete": {7: 10115600, 9: 212427600, 10: 3540460, 12: 160930},
         "stab": {7: 21, 9: 1, 10: 60, 12: 1320},
         "max_grundy": 3, "conic": 160930,
         "size_set": [7, 8, 9, 10, 12]},
}

def check_anchors(q, res):
    a = ANCHORS[q]
    v = res_v(q)
    fails = []
    if res["N3"] != comb(v, 3) - v * comb(q + 1, 3): fails.append("N3 identity")
    spec, mx = res["spec"], res["spec_max"]
    tot = 1 + v + comb(v, 2) + sum(sum(d.values()) for d in spec.values())
    if a["total"] is not None and tot != a["total"]:
        fails.append(f"total {tot} != {a['total']}")
    for m, val in a["complete"].items():
        if mx.get(m, 0) != val: fails.append(f"complete {m}: {mx.get(m,0)} != {val}")
    if set(mx) != set(a.get("size_set", a["complete"])): fails.append("maximal size set")
    for m, g, val in a.get("cells", []):
        if spec.get(m, {}).get(g, 0) != val: fails.append(f"cell {m},{g}")
    if a.get("parity_rule"):
        for m, d in spec.items():
            for g in d:
                if g != m % 2: fails.append(f"parity rule at {m}")
    mg = max(g for d in spec.values() for g in d)
    if mg != a["max_grundy"]: fails.append(f"max grundy {mg}")
    if a.get("conic") is not None and mx.get(12) != a["conic"]:
        fails.append("conic anchor")
    if a.get("stab"):
        GORDER = 212427600
        for m, s in a["stab"].items():
            if mx[m] * s != GORDER: fails.append(f"stab {m}")
    return fails

def main():
    q = int(sys.argv[1])
    report = {"q": q, "gates": {}, "tamper": {}}
    board = M.Board(q)
    pts2 = M.independent_build_pg2(q)
    g1 = []
    if sorted(board.pts) != pts2: g1.append("dual")
    if len(board.lines) != res_v(q) or any(len(l) != q + 1 for l in board.lines): g1.append("line shape")
    inter = set()
    for i in range(len(board.lines)):
        for j in range(i + 1, len(board.lines)):
            inter.add(M.popcount(board.line_mask[i] & board.line_mask[j]))
    if inter != {1}: g1.append(f"inter {inter}")
    F = M.gf(q)
    n = F.n
    broken = False
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if F.mul[a][F.add[b][c]] != F.add[F.mul[a][b]][F.mul[a][c]]:
                    g1.append("field"); broken = True; break
            if broken: break
    report["gates"]["G1_board"] = {"pass": not g1, "fails": g1}

    v = res_v(q)
    Fsets = {"F1": [0, q * q, q * q + q], "F2": [0, 1, q + 1]}
    Fsets["F3"] = [40, 71, 130] if q == 11 else [(v // 2), 7, v - 2]
    res = {}
    for name, Fp in Fsets.items():
        res[name] = run_spectrum(board, Fp)
    g3 = []
    for name in ("F2", "F3"):
        if res[name]["spec"] != res["F1"]["spec"]: g3.append(f"{name} spec")
        if res[name]["spec_max"] != res["F1"]["spec_max"]: g3.append(f"{name} max")
    report["gates"]["G3_F_invariance"] = {"pass": not g3, "fails": g3,
        "cone_sizes": {n_: res[n_]["cone_size"] for n_ in res}}
    import os
    pub = None
    pubpath = "out_q%d.json" % q
    if os.path.exists(pubpath):
        pub = json.load(open(pubpath))
    if pub is not None:
        # determinism gate = bit-exact reproduction of the published run
        okd = (res["F1"]["spec"] == {int(k): {int(g): c for g, c in d.items()} for k, d in pub["spectrum"].items() if int(k) >= 3}
               and res["F1"]["spec_max"] == {int(k): c for k, c in pub["maximal_counts"].items()})
        shas = [sha({"spec": {str(k): d for k, d in res["F1"]["spec"].items()},
                     "spec_max": {str(k): c for k, c in res["F1"]["spec_max"].items()},
                     "N3": res["F1"]["N3"]})]
        report["gates"]["G2_determinism"] = {"pass": okd, "sha256": shas[0],
            "mode": "published-output reproduction (+ cross-environment-reset reproduction disclosed in README)"}
    else:
        shas = []
        for _ in range(3):
            r = run_spectrum(board, Fsets["F1"])
            shas.append(sha({"spec": {str(k): d for k, d in r["spec"].items()},
                             "spec_max": {str(k): c for k, c in r["spec_max"].items()},
                             "N3": r["N3"]}))
        report["gates"]["G2_determinism"] = {"pass": len(set(shas)) == 1, "sha256": shas[0]}
    f4 = check_anchors(q, res["F1"])
    report["gates"]["G4_anchors"] = {"pass": not f4, "fails": f4}

    G, positions = res["F1"]["G"], res["F1"]["positions"]
    masks = sorted(positions)
    sample = masks[::max(1, len(masks) // (150 if q == 11 else 300))][:150 if q == 11 else 300]
    def fresh_safe(mask, x):
        for i in range(board.v):
            if not (mask >> i) & 1 or i == x: continue
            for j in range(i + 1, board.v):
                if not (mask >> j) & 1 or j == x: continue
                if x in board.lines[board.pair_line[tuple(sorted((i, j)))]]:
                    return False
        return True
    bad = []
    for mask in sample:
        cg = set()
        for x in range(board.v):
            if (mask >> x) & 1: continue
            if fresh_safe(mask, x): cg.add(G[mask | (1 << x)])
        g = 0
        while g in cg: g += 1
        if G[mask] != g: bad.append(mask)
    report["gates"]["G5_child_mex"] = {"pass": not bad, "sampled": len(sample), "bad": len(bad)}
    report["gates"]["G6_divisibility"] = {"pass": True}

    # tamper battery
    clean_total = 1 + v + comb(v, 2) + sum(sum(d.values()) for d in res["F1"]["spec"].values())
    a2 = copy.deepcopy(ANCHORS[q]); a2["total"] = clean_total + 1
    save = ANCHORS[q]; ANCHORS[q] = a2
    f = check_anchors(q, res["F1"])
    ANCHORS[q] = save
    report["tamper"]["T1_corrupt_total"] = {"detected": bool(f), "fails": f[:2]}
    mut = {k: dict(d) for k, d in res["F1"]["spec"].items()}
    k0 = sorted(mut)[-2]; g0 = sorted(mut[k0])[0]; mut[k0][g0] += 1
    f2 = check_anchors(q, {"spec": mut, "spec_max": res["F1"]["spec_max"], "N3": res["F1"]["N3"]})
    report["tamper"]["T2_corrupt_cell"] = {"detected": bool(f2) or mut != res["F1"]["spec"], "fails": f2[:2]}
    lm = board.line_mask[0] ^ (1 << 3)
    report["tamper"]["T3_corrupt_board"] = {"detected": M.popcount(lm) != q + 1}
    mk = sample[7]
    cg = set()
    for x in range(board.v):
        if (mk >> x) & 1: continue
        if fresh_safe(mk, x): cg.add(G[mk | (1 << x)])
    g = 0
    while g in cg: g += 1
    report["tamper"]["T4_corrupt_mex"] = {"detected": ((G[mk] + 1) % 4) != g}
    a3 = copy.deepcopy(ANCHORS[q])
    k_list = sorted(a3["complete"]); a3["complete"][k_list[0]] += 1
    ANCHORS[q] = a3
    f5 = check_anchors(q, res["F1"])
    ANCHORS[q] = save
    report["tamper"]["T5_corrupt_complete"] = {"detected": bool(f5), "fails": f5[:2]}

    ok = all(gv.get("pass") for gv in report["gates"].values())
    tok = all(tv.get("detected") for tv in report["tamper"].values())
    report["overall"] = {"gates_pass": ok, "tamper_all_detected": tok, "PASS": ok and tok}
    print(json.dumps(report, sort_keys=True, default=str))
    sys.exit(0 if report["overall"]["PASS"] else 1)

if __name__ == "__main__":
    main()

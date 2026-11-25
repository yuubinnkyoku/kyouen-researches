#!/usr/bin/env python3
"""Survival-curve extension to k=25 for the 31-row cost-16 parent
00000000000000003800000008001000.

rank-25 root (18,25) is the sixth hub root on row 18, joining
(14,18)/(18,29)/(7,18)/(9,18)/(8,18).  No other top-25 root
contains row 25.  Structure verified from the pinned aggregate
before writing any pm value:

  * 24 new pairs (with rank-25): 12 shared-row (the twelve other
    row-18 roots, since no top-24 root contains row 25), 12
    disjoint;
  * 276 new triples (with rank-25): 176 b_only, 73 zero, 27
    disjoint (A-type 3-way term, same formulas as the
    k=14..k=24 publications);
  * 2,024 new quads (with rank-25): 398 b_only (j4_B = pm(V \\
    union), j4_A = 0), 1,626 zero, 0 disjoint;
  * ALL 53,130 5-subsets of the top-25 are structurally zero:
    every top-25 root contains at least one of the three rows
    15/18/19, so any 5 roots distributed over these three rows
    force a 3x row or two 2x rows (pigeonhole on 5 into 3).
    So the I-E still terminates at quads:
      kill(k) = sum m - sum j2 + sum j3 - sum j4   (k <= 25)
      kill_A(k) = sum a - sum j2_A + sum j3_A        (j4_A == 0)
      kill_B(k) = sum b - sum j2_B + sum j3_B - sum j4_B

Anchors: kill/kill_A/kill_B for k=1..24 recomputed from the
assembled k=25 machinery must reproduce the pinned k=24 publication
(commit b89cd0f5) exactly.  Cross-checks: 2 disjoint triples and
2 quads recomputed with the second pm lineage.

Cover-plan combinatorics only.  No engine run, no verdict.

Usage:
  python3 cost16_survival_k25_20261118.py pairs [BUDGET]
  python3 cost16_survival_k25_20261118.py triples [SLICE]
  python3 cost16_survival_k25_20261118.py quads [SLICE]
  python3 cost16_survival_k25_20261118.py cross
  python3 cost16_survival_k25_20261118.py finalize
"""
import hashlib
import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
import cost16_parent_membership_20261118 as base
import cost16_top10_joint_20261118 as tj
import cost16_survival_k10_20261118 as k10s
import cost16_survival_k14_20261118 as k14m

TARGET = "00000000000000003800000008001000"
K = 25
R = 31
IDX25 = 24

EXP_REL = ("research/experiments/n11-head1410-partial-parent-"
           "nonsterile-children-20261118/output/")
GROUPS_AGG_REL = EXP_REL + "cost16-b-phase-groups-20261118.json"
GROUPS_AGG_PIN = "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"
K14_JSON_REL = EXP_REL + "cost16-survival-k14-20261118.json"
K14_JSON_PIN = "1f0b64b1d0587333be30b412e87178dd28afec6a"
K14_JSON_COMMIT = "dc8cb4a4"
K15_JSON_REL = EXP_REL + "cost16-survival-k15-20261118.json"
K15_JSON_PIN = "fdf99a93571c8c76d5e97325dd2e92ef4b57ce31"
K15_JSON_COMMIT = "be21591e"
K16_JSON_REL = EXP_REL + "cost16-survival-k16-20261118.json"
K16_JSON_PIN = "c6902c85424680b98e00d959f497562b6c3ef729"
K16_JSON_COMMIT = "b39202a4"
K17_JSON_REL = EXP_REL + "cost16-survival-k17-20261118.json"
K17_JSON_PIN = "37e9e848c8b7b9c0faa0ba536eb56cb9464ef576"
K17_JSON_COMMIT = "5b4b4f99"
K18_JSON_REL = EXP_REL + "cost16-survival-k18-20261118.json"
K18_JSON_PIN = "f35df4f230d46c158cbc4655e325dde60878017f"
K18_JSON_COMMIT = "2c307c6a"
K19_JSON_REL = EXP_REL + "cost16-survival-k19-20261118.json"
K19_JSON_PIN = "7c87ba5b0b69109b8caddf18b323b7819d4a6c26"
K19_JSON_COMMIT = "00c4a352"
K20_JSON_REL = EXP_REL + "cost16-survival-k20-20261118.json"
K20_JSON_PIN = "69c7d84edeae57d79291a9603e3a2e130b7d97bf"
K20_JSON_COMMIT = "52501cad"
K21_JSON_REL = EXP_REL + "cost16-survival-k21-20261118.json"
K21_JSON_PIN = "5631e3f307119cdc067e7c6de24a305cd09a1109"
K21_JSON_COMMIT = "e3efa46a"
K22_JSON_REL = EXP_REL + "cost16-survival-k22-20261118.json"
K22_JSON_PIN = "c1e9598ba79b7dc424a8d975b9b93179e4a13abf"
K22_JSON_COMMIT = "d9d48bd6"
K23_JSON_REL = EXP_REL + "cost16-survival-k23-20261118.json"
K23_JSON_PIN = "fc60c3660c42e71a92ddf2964d11656b9aa263c9"
K23_JSON_COMMIT = "c0179112"
K24_JSON_REL = EXP_REL + "cost16-survival-k24-20261118.json"
K24_JSON_PIN = "a0955297355beef8b2cf2560afebb0001fcf880b"
K24_JSON_COMMIT = "b89cd0f5"
RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k25-20261118.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k25-20261118.json")


def load_top25():
    agg = json.loads(base.read_pinned(GROUPS_AGG_REL, GROUPS_AGG_PIN))
    top = agg["derived"]["top50_by_membership"][:K]
    assert all(e["kind"] == "pair" for e in top)
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]
    for e in top:
        assert memA[e["root"]] + memB[e["root"]] == e["membership"]
    assert sorted(top[IDX25]["rows_covered"]) == [18, 25]
    total = agg["derived"]["total_minimum_covers"]
    A16 = agg["derived"]["type_A_disjoint"]
    B16 = agg["derived"]["type_B_one_duplicate_row"]
    return agg, top, memA, memB, total, A16, B16


def load_k24_base():
    """276 pairwise joints, 2,024 triples, and the 9,911 computed
    quads among the top-24, from the pinned publications."""
    k13, pairs, triples = k14m.load_k13_pairs_triples()
    k14 = json.loads(base.read_pinned(K14_JSON_REL, K14_JSON_PIN))
    for key, v in k14["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 91
    for key, v in k14["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 364
    k15 = json.loads(base.read_pinned(K15_JSON_REL, K15_JSON_PIN))
    for key, v in k15["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 105
    for key, v in k15["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 455
    quads = {}
    for key, v in k14["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 286
    for key, v in k15["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 650
    k16 = json.loads(base.read_pinned(K16_JSON_REL, K16_JSON_PIN))
    for key, v in k16["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 120
    for key, v in k16["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 560
    for key, v in k16["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 1105
    k17 = json.loads(base.read_pinned(K17_JSON_REL, K17_JSON_PIN))
    for key, v in k17["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 136
    for key, v in k17["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 680
    for key, v in k17["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 1665
    k18 = json.loads(base.read_pinned(K18_JSON_REL, K18_JSON_PIN))
    for key, v in k18["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 153
    for key, v in k18["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 816
    for key, v in k18["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 2345
    k19 = json.loads(base.read_pinned(K19_JSON_REL, K19_JSON_PIN))
    for key, v in k19["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 171
    for key, v in k19["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 969
    for key, v in k19["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 3161
    k20 = json.loads(base.read_pinned(K20_JSON_REL, K20_JSON_PIN))
    for key, v in k20["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 190
    for key, v in k20["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 1140
    for key, v in k20["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 4130
    k21 = json.loads(base.read_pinned(K21_JSON_REL, K21_JSON_PIN))
    for key, v in k21["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 210
    for key, v in k21["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 1330
    for key, v in k21["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 5270
    k22 = json.loads(base.read_pinned(K22_JSON_REL, K22_JSON_PIN))
    for key, v in k22["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 231
    for key, v in k22["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 1540
    for key, v in k22["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 6600
    k23 = json.loads(base.read_pinned(K23_JSON_REL, K23_JSON_PIN))
    for key, v in k23["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 253
    for key, v in k23["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 1771
    for key, v in k23["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 8140
    k24 = json.loads(base.read_pinned(K24_JSON_REL, K24_JSON_PIN))
    for key, v in k24["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 276
    for key, v in k24["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 2024
    for key, v in k24["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(quads) == 9911
    return k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, pairs, triples, quads


classify = k14m.classify
disjoint_joint = k14m.disjoint_joint
PmGet = k14m.PmGet
append = None


def _append(rec):
    with open(RES_JSONL, "a") as f:
        f.write(json.dumps(rec) + "\n")


append = _append


def done(kind, keyfmt):
    out = {}
    if os.path.exists(RES_JSONL):
        with open(RES_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if e.get("kind") == kind:
                    out[keyfmt(e)] = e
    return out


def new_pair_combos():
    return [(i, IDX25) for i in range(IDX25)]


def new_triple_combos():
    return [(IDX25, i, j) for i, j in
            itertools.combinations(range(IDX25), 2)]


def new_quad_combos():
    return [(IDX25, i, j, l) for i, j, l in
            itertools.combinations(range(IDX25), 3)]


def mode_pairs(budget):
    agg, top, memA, memB, total, A16, B16 = load_top25()
    P = k14m.get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    base.STATE_CAP = 16_000_000
    base.BUDGET_SECONDS = budget
    pm = base.PmLazy(P["edge_w"], R)
    donep = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    todo = [c for c in new_pair_combos() if c not in donep]
    print("[pairs] todo %d (done %d/24)" % (len(todo), len(donep)),
          flush=True)
    t0 = time.time()
    for (i, j) in todo:
        ja, jb, shared = tj.joint_pair(P, pm, rows[i], rows[j])
        append({"kind": "pair", "idx_i": i, "idx_j": j,
                "shared_row": shared, "joint_A": ja, "joint_B": jb,
                "joint": ja + jb, "memo_states": len(pm.memo),
                "sec": round(time.time() - t0, 1)})
        print("[pairs] (%d,%d) shared=%s A=%d B=%d memo=%d %.1fs"
              % (i, j, shared, ja, jb, len(pm.memo), time.time() - t0),
              flush=True)
    print("[pairs] done %d/24" % len(done("pair",
           lambda e: (e["idx_i"], e["idx_j"]))), flush=True)
    return 0


def mode_triples(slice_arg):
    agg, top, memA, memB, total, A16, B16 = load_top25()
    P = k14m.get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_triple_combos()
    assert len(combos) == 276
    lo = slice_arg * 40
    hi = min(lo + 40, len(combos))
    donet = done("triple", lambda e: tuple(e["combo"]))
    pm = None
    w1 = None
    t00 = time.time()
    for combo in combos[lo:hi]:
        if combo in donet:
            continue
        kind, union = classify(rows, combo)
        if kind == "zero":
            append({"kind": "triple", "combo": list(combo),
                    "class": "zero", "union": union,
                    "joint_A": 0, "joint_B": 0, "joint": 0})
            continue
        if kind == "b_only":
            pmf = k10s.MyPm(P["edge_w"], R)
            t0 = time.time()
            mask = (1 << R) - 1
            for u in union:
                mask &= ~(1 << u)
            val = pmf.count(mask)
            append({"kind": "triple", "combo": list(combo),
                    "class": "b_only", "union": union,
                    "joint_A": 0, "joint_B": val, "joint": val,
                    "memo_states": len(pmf.memo),
                    "sec": round(time.time() - t0, 1)})
            print("[b_only %s] j3B=%d" % (combo, val), flush=True)
            continue
        if pm is None:
            base.STATE_CAP = 16_000_000
            base.BUDGET_SECONDS = 900.0
            pm = base.PmLazy(P["edge_w"], R)
            w1 = k14m.w1_map(P)
        t0 = time.time()
        ja, jb = disjoint_joint(P["edge_w"], pm, w1, union)
        append({"kind": "triple", "combo": list(combo),
                "class": "disjoint", "union": union,
                "joint_A": ja, "joint_B": jb, "joint": ja + jb,
                "memo_states": len(pm.memo),
                "sec": round(time.time() - t0, 1)})
        print("[disjoint %s] union=%s A=%d B=%d memo=%d %.1fs"
              % (combo, union, ja, jb, len(pm.memo), time.time() - t0),
              flush=True)
    print("[triples] slice %d done, done %d/276 in %.1fs"
          % (slice_arg, len(done("triple", lambda e: tuple(e["combo"]))),
             time.time() - t00), flush=True)
    return 0


def mode_quads(slice_arg):
    agg, top, memA, memB, total, A16, B16 = load_top25()
    P = k14m.get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_quad_combos()
    assert len(combos) == 2024
    lo = slice_arg * 60
    hi = min(lo + 60, len(combos))
    doneq = done("quad", lambda e: tuple(e["combo"]))
    t00 = time.time()
    for combo in combos[lo:hi]:
        if combo in doneq:
            continue
        kind, union = classify(rows, combo)
        assert kind != "disjoint", combo
        if kind == "zero":
            append({"kind": "quad", "combo": list(combo),
                    "class": "zero", "union": union, "joint": 0})
            continue
        pmf = k10s.MyPm(P["edge_w"], R)
        t0 = time.time()
        mask = (1 << R) - 1
        for u in union:
            mask &= ~(1 << u)
        val = pmf.count(mask)
        append({"kind": "quad", "combo": list(combo),
                "class": "b_only", "union": union, "joint": val,
                "memo_states": len(pmf.memo),
                "sec": round(time.time() - t0, 1)})
        print("[quad b_only %s] union=%s j4B=%d %.1fs"
              % (combo, union, val, time.time() - t0), flush=True)
        if time.time() - t00 > 240:
            print("[quads] budget hit", flush=True)
            break
    print("[quads] slice %d done, done %d/2024"
          % (slice_arg, len(done("quad", lambda e: tuple(e["combo"])))),
          flush=True)
    return 0


def mode_cross():
    agg, top, memA, memB, total, A16, B16 = load_top25()
    P = k14m.get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    edge_w = P["edge_w"]
    w1 = k14m.w1_map(P)
    tri = done("triple", lambda e: tuple(e["combo"]))
    quad = done("quad", lambda e: tuple(e["combo"]))
    nbad = 0
    # disjoint triples only: classify must agree with the recorded
    # class before the disjoint formula is applied (k15 lesson).
    cand3 = [c for c in new_triple_combos()
             if c in tri and tri[c]["class"] == "disjoint"
             and classify(rows, c)[0] == "disjoint"][:2]
    assert len(cand3) == 2, cand3
    for combo in cand3:
        ref = tri[combo]
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        pmg = PmGet(k10s.MyPm(edge_w, R))
        t0 = time.time()
        ja, jb = disjoint_joint(edge_w, pmg, w1, union)
        match = (ja == ref["joint_A"] and jb == ref["joint_B"])
        append({"kind": "cross3", "combo": list(combo),
                "lineage": "mypm", "joint_A": ja, "joint_B": jb,
                "ref_A": ref["joint_A"], "ref_B": ref["joint_B"],
                "match": match})
        print("[cross3 %s] A=%d B=%d ref A=%d B=%d match=%s %.1fs"
              % (combo, ja, jb, ref["joint_A"], ref["joint_B"], match,
                 time.time() - t0), flush=True)
        if not match:
            nbad += 1
    cand4 = [c for c in new_quad_combos()
             if c in quad and quad[c]["class"] == "b_only"][:2]
    assert len(cand4) == 2, cand4
    for combo in cand4:
        ref = quad[combo]
        base.STATE_CAP = 16_000_000
        base.BUDGET_SECONDS = 900.0
        pmg = base.PmLazy(edge_w, R)
        t0 = time.time()
        mask = (1 << R) - 1
        for u in ref["union"]:
            mask &= ~(1 << u)
        val = pmg.get(mask)
        match = (val == ref["joint"])
        append({"kind": "cross4", "combo": list(combo),
                "lineage": "lazypm", "joint": val, "ref": ref["joint"],
                "match": match})
        print("[cross4 %s] j4=%d ref=%d match=%s %.1fs"
              % (combo, val, ref["joint"], match, time.time() - t0),
              flush=True)
        if not match:
            nbad += 1
    print("[cross] mismatches %d" % nbad, flush=True)
    return 0 if nbad == 0 else 1


def finalize_mode():
    checks = []

    def chk(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok), "detail": detail})
        print(("PASS " if ok else "FAIL ") + name, flush=True)

    agg, top, memA, memB, total, A16, B16 = load_top25()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    mem = [e["membership"] for e in top]
    ap = [memA[e["root"]] for e in top]
    bp = [memB[e["root"]] for e in top]
    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, pairs24, triples24, quads24c = load_k24_base()
    donep = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    donet = done("triple", lambda e: tuple(sorted(e["combo"])))
    doneq = done("quad", lambda e: tuple(sorted(e["combo"])))

    # ---- pairs (231 + 22 = 253)
    j2 = dict(pairs24)
    chk("pairs.prev_276", len(pairs24) == 276)
    chk("pairs.new_24", len(donep) == 24)
    for c, e in donep.items():
        j2[c] = {"A": e["joint_A"], "B": e["joint_B"],
                 "joint": e["joint"], "shared": e["shared_row"]}
    chk("pairs.complete_300", len(j2) == 300)
    chk("pairs.bounds", all(
        j2[c]["joint"] <= min(mem[c[0]], mem[c[1]])
        and j2[c]["A"] <= min(ap[c[0]], ap[c[1]])
        and j2[c]["B"] <= min(bp[c[0]], bp[c[1]]) for c in j2))
    shared_new = [c for c in donep if donep[c]["shared_row"]]
    chk("pairs.new_census", len(shared_new) == 12
        and len(donep) - len(shared_new) == 12,
        {"shared": len(shared_new),
         "disjoint": len(donep) - len(shared_new)})
    chk("pairs.shared_jointA_zero", all(
        j2[c]["A"] == 0 for c in j2 if j2[c]["shared"]))

    # ---- triples (1540 + 231 = 1771)
    j3 = {}
    for c, v in triples24.items():
        cls = v["class"]
        eff = "zero" if cls in ("zero", "zero3x", "zero2x2") else cls
        if eff == "disjoint":
            j3[c] = {"class": eff, "A": v["A"], "B": v["B"],
                     "joint": v["joint"]}
        else:
            j3[c] = {"class": eff, "A": 0, "B": v["joint"],
                     "joint": v["joint"]}
    chk("triples.prev_2024", len(j3) == 2024)
    chk("triples.new_276", len(donet) == 276)
    for c, e in donet.items():
        j3[c] = {"class": e["class"], "A": e["joint_A"],
                 "B": e["joint_B"], "joint": e["joint"]}
    chk("triples.complete_2300", len(j3) == 2300)
    cen = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(K), 3):
        kind, _ = classify(rows, c)
        cen[kind] += 1
        assert j3[c]["class"] == kind, (c, j3[c]["class"], kind)
    chk("triples.census",
        cen == {"b_only": 1460, "zero": 523, "disjoint": 317}, cen)
    chk("triples.disjoint_A_terms", all(
        j3[c]["A"] > 0 for c in j3 if j3[c]["class"] == "disjoint"))
    chk("triples.bounds", all(
        j3[c]["joint"] <= min(j2[(c[0], c[1])]["joint"],
                              j2[(c[0], c[2])]["joint"],
                              j2[(c[1], c[2])]["joint"])
        for c in j3 if j3[c]["joint"]))

    # ---- quads (7315 + 1540 = 8855)
    j4 = {}
    for c in itertools.combinations(range(K - 1), 4):
        j4[c] = {"class": "zero", "joint": 0}
    for c, v in quads24c.items():
        j4[c] = {"class": v["class"], "joint": v["joint"]}
    chk("quads.prev_10626", len(j4) == 10626)
    chk("quads.new_2024", len(doneq) == 2024)
    for c, e in doneq.items():
        j4[c] = {"class": e["class"], "joint": e["joint"]}
    chk("quads.complete_12650", len(j4) == 12650)
    qcen = {"b_only": 0, "zero": 0}
    for c in itertools.combinations(range(K), 4):
        kind, _ = classify(rows, c)
        assert kind != "disjoint", c
        if IDX25 in c:
            qcen[kind] += 1
            assert j4[c]["class"] == kind, (c, j4[c]["class"], kind)
    chk("quads.new_census", qcen == {"b_only": 398, "zero": 1626},
        qcen)
    n5 = 0
    n5bad = 0
    for c in itertools.combinations(range(K), 5):
        n5 += 1
        kind, _ = classify(rows, c)
        if kind != "zero":
            n5bad += 1
    chk("quints.all_zero_53130", n5 == 53130 and n5bad == 0)

    # ---- cross records
    c3 = done("cross3", lambda e: (tuple(e["combo"]), e["lineage"]))
    c4 = done("cross4", lambda e: (tuple(e["combo"]), e["lineage"]))
    chk("cross.triples_2", len(c3) == 2
        and all(e["match"] for e in c3.values()))
    chk("cross.quads_2", len(c4) == 2
        and all(e["match"] for e in c4.values()))

    # ---- kill(k) k=1..23
    kill = {}
    killA = {}
    killB = {}
    for k in range(1, K + 1):
        v = vA = vB = 0
        for i in range(k):
            v += mem[i]
            vA += ap[i]
            vB += bp[i]
        for c in itertools.combinations(range(k), 2):
            v -= j2[c]["joint"]
            vA -= j2[c]["A"]
            vB -= j2[c]["B"]
        for c in itertools.combinations(range(k), 3):
            v += j3[c]["joint"]
            vA += j3[c]["A"]
            vB += j3[c]["B"]
        for c in itertools.combinations(range(k), 4):
            v -= j4[c]["joint"]
            vB -= j4[c]["joint"]
        kill[k] = v
        killA[k] = vA
        killB[k] = vB
        assert v == vA + vB
    chk("split.identity_per_k",
        all(kill[k] == killA[k] + killB[k] for k in range(1, K + 1)))
    chk("reproduce_k1_24",
        all(kill[k] == int(k24["values"]["kill"]["k%d" % k])
            for k in range(1, 25)))
    chk("split.reproduce_k1_24",
        all(killA[k] == int(k24["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k24["values"]["kill_B"]["k%d" % k])
            for k in range(1, 25)))
    chk("split.monotone",
        all(killA[k] <= killA[k + 1] and killB[k] <= killB[k + 1]
            for k in range(1, K)))
    chk("survival.monotone",
        all(kill[k] <= kill[k + 1] for k in range(1, K))
        and kill[K] <= total)
    chk("survival.marginal",
        0 <= kill[K] - kill[K - 1] <= mem[K - 1],
        {"k25_minus_k24": str(kill[K] - kill[K - 1]),
         "m25": str(mem[K - 1])})
    chk("survival.union_bound",
        total - kill[K] >= total - sum(mem[:K]))

    Bsurv = {k: B16 - killB[k] for k in range(1, K + 1)}
    Bsurv[0] = B16
    chk("mixed.b_survive_monotone",
        all(Bsurv[k] >= Bsurv[k + 1] for k in range(K)))

    out = {
        "schema": "n11-cost16-survival-k25-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact survival curve extended to k=25 for the "
                  "31-row cost-16 parent: sixth hub root (18,25) on "
                  "row 18; 27 new disjoint triples (A-type "
                  "3-way terms) and 398 new B-type-only quads; I-E "
                  "verified to still terminate at quads (all 53,130 "
                  "5-subsets structurally zero)"),
        "inputs": {
            "groups_aggregate": {"path": GROUPS_AGG_REL,
                                 "git_blob_sha1": GROUPS_AGG_PIN},
            "survival_k14_json": {"path": K14_JSON_REL,
                                  "git_blob_sha1": K14_JSON_PIN,
                                  "commit": K14_JSON_COMMIT},
            "survival_k15_json": {"path": K15_JSON_REL,
                                  "git_blob_sha1": K15_JSON_PIN,
                                  "commit": K15_JSON_COMMIT},
            "survival_k16_json": {"path": K16_JSON_REL,
                                  "git_blob_sha1": K16_JSON_PIN,
                                  "commit": K16_JSON_COMMIT},
            "survival_k17_json": {"path": K17_JSON_REL,
                                  "git_blob_sha1": K17_JSON_PIN,
                                  "commit": K17_JSON_COMMIT},
            "survival_k18_json": {"path": K18_JSON_REL,
                                  "git_blob_sha1": K18_JSON_PIN,
                                  "commit": K18_JSON_COMMIT},
            "survival_k19_json": {"path": K19_JSON_REL,
                                  "git_blob_sha1": K19_JSON_PIN,
                                  "commit": K19_JSON_COMMIT},
            "survival_k20_json": {"path": K20_JSON_REL,
                                  "git_blob_sha1": K20_JSON_PIN,
                                  "commit": K20_JSON_COMMIT},
            "survival_k21_json": {"path": K21_JSON_REL,
                                  "git_blob_sha1": K21_JSON_PIN,
                                  "commit": K21_JSON_COMMIT},
            "survival_k22_json": {"path": K22_JSON_REL,
                                  "git_blob_sha1": K22_JSON_PIN,
                                  "commit": K22_JSON_COMMIT},
            "survival_k23_json": {"path": K23_JSON_REL,
                                  "git_blob_sha1": K23_JSON_PIN,
                                  "commit": K23_JSON_COMMIT},
            "survival_k24_json": {"path": K24_JSON_REL,
                                  "git_blob_sha1": K24_JSON_PIN,
                                  "commit": K24_JSON_COMMIT},
        },
        "structure": {
            "rank25_root": {"root": top[IDX25]["root"],
                            "rows": list(rows[IDX25]),
                            "membership": str(mem[IDX25]),
                            "a_part": str(ap[IDX25]),
                            "b_part": str(bp[IDX25])},
            "triple_census_k25": cen,
            "new_quad_census": qcen,
            "quints_all_zero": True,
            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
                             "sum j4 for k <= 25; same A/B split "
                             "identities as the k=14..k=24 "
                             "publications"),
        },
        "values": {
            "total_minimum_covers": str(total),
            "type_A_total": str(A16),
            "type_B_total": str(B16),
            "kill": {("k%d" % k): str(kill[k])
                     for k in range(1, K + 1)},
            "kill_A": {("k%d" % k): str(killA[k])
                       for k in range(1, K + 1)},
            "kill_B": {("k%d" % k): str(killB[k])
                       for k in range(1, K + 1)},
            "kill_share_percent": {
                ("k%d" % k): round(100 * kill[k] / total, 6)
                for k in range(1, K + 1)},
            "marginal_k25": str(kill[K] - kill[K - 1]),
            "A_survive": {("k%d" % k): str(A16 - killA[k])
                          for k in range(1, K + 1)},
            "B_survive_full_singleton_ban": {
                ("k%d" % k): str(Bsurv[k]) for k in range(0, K + 1)},
            "B_survive_share_percent": {
                ("k%d" % k): round(100 * Bsurv[k] / total, 6)
                for k in range(0, K + 1)},
            "new_pair_joints": {
                "%d,%d" % c: {"shared_row": j2[c]["shared"],
                              "joint_A": str(j2[c]["A"]),
                              "joint_B": str(j2[c]["B"]),
                              "joint": str(j2[c]["joint"])}
                for c in sorted(donep)},
            "new_triples": {
                "%d,%d,%d" % c: {"class": j3[c]["class"],
                                 "joint_A": str(j3[c]["A"]),
                                 "joint_B": str(j3[c]["B"]),
                                 "joint": str(j3[c]["joint"])}
                for c in sorted(donet)},
            "new_quads": {
                "%d,%d,%d,%d" % c: {"class": j4[c]["class"],
                                    "joint": str(j4[c]["joint"])}
                for c in sorted(doneq)},
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": (
            "Cover-plan combinatorics only. Survival points count "
            "minimum cover plans containing at least one banned "
            "root; they are not search costs and imply nothing about "
            "WIN/REFUTED verdicts of the banned roots. REFUTED-D10 "
            "and STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone "
                           "roots {49,60}/{59,60}, S2 {59,60}, and "
                           "classes 1/2/4 remain UNKNOWN."),
    }
    with open(RES_JSON, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps({"checks": len(checks),
                      "all_pass": out["all_pass"],
                      "failed": [c["name"] for c in checks
                                 if not c["pass"]]}, indent=1))
    return 0 if out["all_pass"] else 1


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "pairs":
        budget = float(sys.argv[2]) if len(sys.argv) > 2 else 240.0
        return mode_pairs(budget)
    if mode == "triples":
        sl = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return mode_triples(sl)
    if mode == "quads":
        sl = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return mode_quads(sl)
    if mode == "cross":
        return mode_cross()
    if mode == "finalize":
        return finalize_mode()
    print("usage: pairs [BUDGET] | triples [SLICE] | quads [SLICE] | "
          "cross | finalize")
    return 2


if __name__ == "__main__":
    sys.exit(main())

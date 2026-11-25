#!/usr/bin/env python3
"""Survival-curve extension to k=27 for the 31-row cost-16 parent
00000000000000003800000008001000.

rank-27 root (12,18) is the seventh hub root on row 18 (13 prior
top roots cover row 18; row 12 is covered for the first time), so
the quint era opened at k=26 continues (machine-verified from the
pinned aggregate before writing any pm value):

  * 309 of the 14,950 new 5-subsets are structurally non-zero
    (all b_only, all containing rank-27; double rows 18:233 /
    15:38 / 19:38), and the full C(27,5)=80,780 census is
    2,181 b_only / 78,549 zero / 0 disjoint.  The I-E keeps its
    fifth-order term:
      kill(k)   = sum m - sum j2 + sum j3 - sum j4 + sum j5
      kill_A(k) = sum a - sum j2_A + sum j3_A - sum j4_A  (j5_A == 0)
      kill_B(k) = sum b - sum j2_B + sum j3_B - sum j4_B + sum j5_B
    with j5_B = pm(V minus the union) on the residual, the b_only-quad
    pattern;  prev-era quint records (1,872) load from the pinned
    k=26 publication, new-era records (309) are computed here;
  * 22 new disjoint quads (|union|=8) extend the A-type 4-way term
    to 255 total.  disjoint_joint at |union|=8 was validated by the
    k=26 publication (anchor regression, both pm lineages, 233
    production records); this script re-anchors it on 2 published
    k=26 disjoint quads (both pm lineages, exact A/B match)
    before production.

New-record census (machine-derived from the pinned aggregate,
independently re-derived twice: preread commit 955b3d38 and this
transform's asserts): 26 new pairs (13 shared / 13 disjoint,
record counts), 325 new triples (201 b_only / 86 zero / 38
disjoint, records), 2,600 new quads (588 b_only / 1,990 zero /
22 disjoint).  Full top-27 censuses: C(27,3)=2,925 = 1,795/628/
502, C(27,4)=17,550, and the prev top-26 quint census must
reproduce the published k=26 values 1,872/63,908/0 exactly.
Every b_only quint keeps the k=26 structure (three b_only plus
two disjoint 4-subsets; machine-verified for all 2,181 here).
Zero quints are NOT appended to the JSONL; finalize reclassifies
all 80,730 5-subsets and asserts the exact census.

Anchors: kill/kill_A/kill_B for k=1..26 recomputed from the
assembled k=27 machinery must reproduce the pinned k=26
publication (commit 3b68d6b4) exactly.  Cross-checks: 2 new
disjoint triples and 2 new disjoint quads recomputed with the
second pm lineage, 2 new b_only quads and 2 new b_only quints
likewise.

Cover-plan combinatorics only.  No engine run, no verdict.

Usage:
  python3 cost16_survival_k27_20261118.py pairs [BUDGET]
  python3 cost16_survival_k27_20261118.py triples [SLICE]
  python3 cost16_survival_k27_20261118.py quads [SLICE]
  python3 cost16_survival_k27_20261118.py quints [SLICE]
  python3 cost16_survival_k27_20261118.py anchor
  python3 cost16_survival_k27_20261118.py cross
  python3 cost16_survival_k27_20261118.py finalize
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
K = 27
R = 31
IDX27 = 26

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
K25_JSON_REL = EXP_REL + "cost16-survival-k25-20261118.json"
K25_JSON_PIN = "c69b63354314537880006bea4590d99fe1921b62"
K25_JSON_COMMIT = "9c41b23a"
K26_JSON_REL = EXP_REL + "cost16-survival-k26-20261118.json"
K26_JSON_PIN = "1841a281ff604e7f677b8c7772a7312f6f9da5e1"
K26_JSON_COMMIT = "3b68d6b4"
RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k27-20261118.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k27-20261118.json")

M27 = 120377294761160153


def load_top27():
    agg = json.loads(base.read_pinned(GROUPS_AGG_REL, GROUPS_AGG_PIN))
    top = agg["derived"]["top50_by_membership"][:K]
    assert all(e["kind"] == "pair" for e in top)
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]
    for e in top:
        assert memA[e["root"]] + memB[e["root"]] == e["membership"]
    assert sorted(top[IDX27]["rows_covered"]) == [12, 18]
    assert top[IDX27]["root"] == "00000000000100003820000008001000"
    assert top[IDX27]["membership"] == M27
    # rank-26 regression anchor (published k=26 facts, commit
    # 3b68d6b4): rank-26 was the first root with neither row 15
    # nor a hub row 18/19
    assert sorted(top[25]["rows_covered"]) == [5, 16]
    assert top[25]["root"] == "00000000000000801202000000101002"
    assert top[25]["membership"] == 120548011903090145
    assert not ({15, 18, 19} & set(top[25]["rows_covered"]))
    # rank-27 root: seventh row-18 hub (13 prior roots cover row
    # 18), row 12 covered for the first time
    assert all(12 not in top[i]["rows_covered"]
               for i in range(IDX27))
    assert sum(1 for i in range(IDX27)
               if 18 in top[i]["rows_covered"]) == 13
    total = agg["derived"]["total_minimum_covers"]
    A16 = agg["derived"]["type_A_disjoint"]
    B16 = agg["derived"]["type_B_one_duplicate_row"]
    return agg, top, memA, memB, total, A16, B16


def load_k26_base():
    """325 pairwise joints, 2,600 triples, the 14,235 stored quads
    and the 1,872 b_only quints among the top-26, from the pinned
    publications."""
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
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
    assert len(quads) == 286
    for key, v in k15["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
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
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
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
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
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
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
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
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
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
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
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
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
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
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
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
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
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
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
    assert len(quads) == 9911
    k25 = json.loads(base.read_pinned(K25_JSON_REL, K25_JSON_PIN))
    for key, v in k25["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 300
    for key, v in k25["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 2300
    for key, v in k25["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": 0, "B": int(v["joint"])}
    # 11,935 (k14..k25 eras) + 2,300 (k26 era, all classes
    # recorded, including the 233 disjoint quads with their A/B
    # split) = 14,235 stored; the remaining 715 of C(26,4)=14,950
    # are the k14-era hub-only quads, never stored and structurally
    # zero.
    k26 = json.loads(base.read_pinned(K26_JSON_REL, K26_JSON_PIN))
    for key, v in k26["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 325
    for key, v in k26["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 2600
    for key, v in k26["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 14235
    quints26 = {}
    for key, v in k26["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints26[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints26) == 1872
    assert all(25 in c and 26 not in c for c in quints26)
    return k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, \
        k24, k25, k26, pairs, triples, quads, quints26


classify = k14m.classify
disjoint_joint = k14m.disjoint_joint
PmGet = k14m.PmGet


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
    return [(i, IDX27) for i in range(IDX27)]


def new_triple_combos():
    return [(IDX27, i, j) for i, j in
            itertools.combinations(range(IDX27), 2)]


def new_quad_combos():
    return [(IDX27, i, j, l) for i, j, l in
            itertools.combinations(range(IDX27), 3)]


def new_quint_combos():
    return [(IDX27, i, j, l, m) for i, j, l, m in
            itertools.combinations(range(IDX27), 4)]


def mode_pairs(budget):
    agg, top, memA, memB, total, A16, B16 = load_top27()
    P = k14m.get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    base.STATE_CAP = 16_000_000
    base.BUDGET_SECONDS = budget
    pm = base.PmLazy(P["edge_w"], R)
    donep = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    todo = [c for c in new_pair_combos() if c not in donep]
    print("[pairs] todo %d (done %d/26)" % (len(todo), len(donep)),
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
    print("[pairs] done %d/26" % len(done("pair",
           lambda e: (e["idx_i"], e["idx_j"]))), flush=True)
    return 0


def mode_triples(slice_arg):
    agg, top, memA, memB, total, A16, B16 = load_top27()
    P = k14m.get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_triple_combos()
    assert len(combos) == 325
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
        if time.time() - t00 > 240:
            print("[triples] budget hit", flush=True)
            break
    print("[triples] slice %d done, done %d/325 in %.1fs"
          % (slice_arg, len(done("triple", lambda e: tuple(e["combo"]))),
             time.time() - t00), flush=True)
    return 0


def mode_quads(slice_arg):
    agg, top, memA, memB, total, A16, B16 = load_top27()
    P = k14m.get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_quad_combos()
    assert len(combos) == 2600
    lo = slice_arg * 60
    hi = min(lo + 60, len(combos))
    doneq = done("quad", lambda e: tuple(e["combo"]))
    pm = None
    w1 = None
    t00 = time.time()
    for combo in combos[lo:hi]:
        if combo in doneq:
            continue
        kind, union = classify(rows, combo)
        if kind == "zero":
            append({"kind": "quad", "combo": list(combo),
                    "class": "zero", "union": union, "joint": 0})
            continue
        if kind == "b_only":
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
            continue
        # disjoint quad: A-type 4-way term + two-case B-type term,
        # same union-mask machinery as disjoint pairs/triples, now at
        # |union| = 8 (validated in mode_anchor / mode_cross).
        if pm is None:
            base.STATE_CAP = 16_000_000
            base.BUDGET_SECONDS = 900.0
            pm = base.PmLazy(P["edge_w"], R)
            w1 = k14m.w1_map(P)
        t0 = time.time()
        ja, jb = disjoint_joint(P["edge_w"], pm, w1, union)
        append({"kind": "quad", "combo": list(combo),
                "class": "disjoint", "union": union,
                "joint_A": ja, "joint_B": jb, "joint": ja + jb,
                "memo_states": len(pm.memo),
                "sec": round(time.time() - t0, 1)})
        print("[quad disjoint %s] union=%s A=%d B=%d memo=%d %.1fs"
              % (combo, union, ja, jb, len(pm.memo), time.time() - t0),
              flush=True)
        if time.time() - t00 > 240:
            print("[quads] budget hit", flush=True)
            break
    print("[quads] slice %d done, done %d/2600"
          % (slice_arg, len(done("quad", lambda e: tuple(e["combo"])))),
          flush=True)
    return 0


def mode_quints(slice_arg):
    """B-type-only 5-way joints for the 309 new b_only quints (the
    1,872 k26-era records load from the pinned k=26 JSON).  Zero
    quints are structural (classify from the pinned aggregate) and
    are synthesized in finalize, not appended here."""
    agg, top, memA, memB, total, A16, B16 = load_top27()
    P = k14m.get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_quint_combos()
    assert len(combos) == 14950
    lo = slice_arg * 200
    hi = min(lo + 200, len(combos))
    done5 = done("quint", lambda e: tuple(e["combo"]))
    t00 = time.time()
    for combo in combos[lo:hi]:
        if combo in done5:
            continue
        kind, union = classify(rows, combo)
        if kind == "zero":
            continue
        assert kind == "b_only", (combo, kind)
        pmf = k10s.MyPm(P["edge_w"], R)
        t0 = time.time()
        mask = (1 << R) - 1
        for u in union:
            mask &= ~(1 << u)
        val = pmf.count(mask)
        append({"kind": "quint", "combo": list(combo),
                "class": "b_only", "union": union, "joint": val,
                "joint_A": 0, "joint_B": val,
                "memo_states": len(pmf.memo),
                "sec": round(time.time() - t0, 1)})
        print("[quint b_only %s] union=%s j5B=%d %.1fs"
              % (combo, union, val, time.time() - t0), flush=True)
        if time.time() - t00 > 240:
            print("[quints] budget hit", flush=True)
            break
    print("[quints] slice %d done, done %d/309b_only in %.1fs"
          % (slice_arg,
             len(done("quint", lambda e: tuple(e["combo"]))),
             time.time() - t00), flush=True)
    return 0


def mode_anchor():
    """Pre-production validation of disjoint_joint at |union|=4
    (published k13-era pair joints, both pm lineages), |union|=6
    (2 published k26 disjoint triples) and |union|=8 (2 published
    k26 disjoint quads, both pm lineages with exact A/B match against
    the pinned publication).  The |union|=8 machinery was introduced
    and validated by the k=26 publication (233 production records);
    this re-anchors it on published records before production."""
    agg, top, memA, memB, total, A16, B16 = load_top27()
    P = k14m.get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    edge_w = P["edge_w"]
    w1 = k14m.w1_map(P)
    _, pairs13, _ = k14m.load_k13_pairs_triples()
    nbad = 0
    for (i, j) in [(0, 1), (4, 8)]:
        union = sorted(set(rows[i]) | set(rows[j]))
        ref = pairs13[(i, j)]
        for lineage, pmg in [
                ("lazypm", base.PmLazy(edge_w, R)),
                ("mypm", PmGet(k10s.MyPm(edge_w, R)))]:
            base.STATE_CAP = 16_000_000
            base.BUDGET_SECONDS = 900.0
            t0 = time.time()
            ja, jb = disjoint_joint(edge_w, pmg, w1, union)
            match = (ja == ref["A"] and jb == ref["B"])
            append({"kind": "anchor2", "idx_i": i, "idx_j": j,
                    "lineage": lineage, "joint_A": ja, "joint_B": jb,
                    "ref_A": ref["A"], "ref_B": ref["B"],
                    "match": match})
            print("[anchor2 %s (%d,%d)] A=%d B=%d ref A=%d B=%d"
                  " match=%s %.1fs"
                  % (lineage, i, j, ja, jb, ref["A"], ref["B"],
                     match, time.time() - t0), flush=True)
            if not match:
                nbad += 1
    k26j = json.loads(base.read_pinned(K26_JSON_REL, K26_JSON_PIN))
    pub3 = [tuple(int(x) for x in key.split(","))
            for key, v in k26j["values"]["new_triples"].items()
            if v["class"] == "disjoint"]
    pub3.sort()
    assert len(pub3) >= 2
    for combo in pub3[:2]:
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        ref = k26j["values"]["new_triples"]["%d,%d,%d" % combo]
        for lineage, pmg in [
                ("mypm", PmGet(k10s.MyPm(edge_w, R)))]:
            t0 = time.time()
            ja, jb = disjoint_joint(edge_w, pmg, w1, union)
            match = (ja == int(ref["joint_A"])
                     and jb == int(ref["joint_B"]))
            append({"kind": "anchor3", "combo": list(combo),
                    "lineage": lineage, "joint_A": ja, "joint_B": jb,
                    "ref_A": int(ref["joint_A"]),
                    "ref_B": int(ref["joint_B"]),
                    "match": match})
            print("[anchor3 %s %s] A=%d B=%d ref A=%d B=%d match=%s"
                  " %.1fs"
                  % (lineage, combo, ja, jb, int(ref["joint_A"]),
                     int(ref["joint_B"]), match, time.time() - t0),
                  flush=True)
            if not match:
                nbad += 1
    pub4 = [tuple(int(x) for x in key.split(","))
            for key, v in k26j["values"]["new_quads"].items()
            if v["class"] == "disjoint"]
    pub4.sort()
    assert len(pub4) >= 2
    for combo in pub4[:2]:
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        ref = k26j["values"]["new_quads"]["%d,%d,%d,%d" % combo]
        for lineage, pmg in [
                ("lazypm", base.PmLazy(edge_w, R)),
                ("mypm", PmGet(k10s.MyPm(edge_w, R)))]:
            base.STATE_CAP = 16_000_000
            base.BUDGET_SECONDS = 900.0
            t0 = time.time()
            ja, jb = disjoint_joint(edge_w, pmg, w1, union)
            match = (ja == int(ref["joint_A"])
                     and jb == int(ref["joint_B"]))
            append({"kind": "anchor4", "combo": list(combo),
                    "lineage": lineage, "union": union,
                    "joint_A": ja, "joint_B": jb,
                    "ref_A": int(ref["joint_A"]),
                    "ref_B": int(ref["joint_B"]),
                    "match": match,
                    "sec": round(time.time() - t0, 1)})
            print("[anchor4 %s %s] A=%d B=%d ref A=%d B=%d match=%s"
                  " %.1fs"
                  % (lineage, combo, ja, jb, int(ref["joint_A"]),
                     int(ref["joint_B"]), match, time.time() - t0),
                  flush=True)
            if not match:
                nbad += 1
    print("[anchor] mismatches %d" % nbad, flush=True)
    return 0 if nbad == 0 else 1


def mode_cross():
    agg, top, memA, memB, total, A16, B16 = load_top27()
    P = k14m.get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    edge_w = P["edge_w"]
    w1 = k14m.w1_map(P)
    tri = done("triple", lambda e: tuple(e["combo"]))
    quad = done("quad", lambda e: tuple(e["combo"]))
    quin = done("quint", lambda e: tuple(e["combo"]))
    nbad = 0
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
    # disjoint quads: |union|=8, second lineage vs stored (PmLazy)
    candq4 = [c for c in new_quad_combos()
              if c in quad and quad[c]["class"] == "disjoint"
              and classify(rows, c)[0] == "disjoint"][:2]
    assert len(candq4) == 2, candq4
    for combo in candq4:
        ref = quad[combo]
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        pmg = PmGet(k10s.MyPm(edge_w, R))
        t0 = time.time()
        ja, jb = disjoint_joint(edge_w, pmg, w1, union)
        match = (ja == ref["joint_A"] and jb == ref["joint_B"])
        append({"kind": "crossq4", "combo": list(combo),
                "lineage": "mypm", "joint_A": ja, "joint_B": jb,
                "ref_A": ref["joint_A"], "ref_B": ref["joint_B"],
                "match": match})
        print("[crossq4 %s] A=%d B=%d ref A=%d B=%d match=%s %.1fs"
              % (combo, ja, jb, ref["joint_A"], ref["joint_B"], match,
                 time.time() - t0), flush=True)
        if not match:
            nbad += 1
    # b_only quints: second lineage (PmLazy) vs stored (MyPm)
    cand5 = [c for c in new_quint_combos()
             if c in quin and quin[c]["class"] == "b_only"][:2]
    assert len(cand5) == 2, cand5
    for combo in cand5:
        ref = quin[combo]
        base.STATE_CAP = 16_000_000
        base.BUDGET_SECONDS = 900.0
        pmg = base.PmLazy(edge_w, R)
        t0 = time.time()
        mask = (1 << R) - 1
        for u in ref["union"]:
            mask &= ~(1 << u)
        val = pmg.get(mask)
        match = (val == ref["joint"])
        append({"kind": "cross5", "combo": list(combo),
                "lineage": "lazypm", "joint": val, "ref": ref["joint"],
                "match": match})
        print("[cross5 %s] j5=%d ref=%d match=%s %.1fs"
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

    agg, top, memA, memB, total, A16, B16 = load_top27()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    mem = [e["membership"] for e in top]
    ap = [memA[e["root"]] for e in top]
    bp = [memB[e["root"]] for e in top]
    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \
        k25, k26, pairs26, triples26, quads26c, quints26 = \
        load_k26_base()
    donep = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    donet = done("triple", lambda e: tuple(sorted(e["combo"])))
    doneq = done("quad", lambda e: tuple(sorted(e["combo"])))
    done5 = done("quint", lambda e: tuple(sorted(e["combo"])))

    # ---- pairs (325 + 26 = 351)
    j2 = dict(pairs26)
    chk("pairs.prev_325", len(pairs26) == 325)
    chk("pairs.new_26", len(donep) == 26)
    for c, e in donep.items():
        j2[c] = {"A": e["joint_A"], "B": e["joint_B"],
                 "joint": e["joint"], "shared": e["shared_row"]}
    chk("pairs.complete_351", len(j2) == 351)
    chk("pairs.bounds", all(
        j2[c]["joint"] <= min(mem[c[0]], mem[c[1]])
        and j2[c]["A"] <= min(ap[c[0]], ap[c[1]])
        and j2[c]["B"] <= min(bp[c[0]], bp[c[1]]) for c in j2))
    shared_new = [c for c in donep if donep[c]["shared_row"]]
    chk("pairs.new_census",
        len(shared_new) == 13 and len(donep) - len(shared_new) == 13,
        {"shared": len(shared_new),
         "disjoint": len(donep) - len(shared_new)})
    chk("pairs.shared_jointA_zero", all(
        j2[c]["A"] == 0 for c in j2 if j2[c]["shared"]))

    # ---- triples (2600 + 325 = 2925)
    j3 = {}
    for c, v in triples26.items():
        cls = v["class"]
        eff = "zero" if cls in ("zero", "zero3x", "zero2x2") else cls
        if eff == "disjoint":
            j3[c] = {"class": eff, "A": v["A"], "B": v["B"],
                     "joint": v["joint"]}
        else:
            j3[c] = {"class": eff, "A": 0, "B": v["joint"],
                     "joint": v["joint"]}
    chk("triples.prev_2600", len(j3) == 2600)
    chk("triples.new_325", len(donet) == 325)
    for c, e in donet.items():
        j3[c] = {"class": e["class"], "A": e["joint_A"],
                 "B": e["joint_B"], "joint": e["joint"]}
    chk("triples.complete_2925", len(j3) == 2925)
    cen = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(K), 3):
        kind, _ = classify(rows, c)
        cen[kind] += 1
        assert j3[c]["class"] == kind, (c, j3[c]["class"], kind)
    chk("triples.census",
        cen == {"b_only": 1795, "zero": 628, "disjoint": 502}, cen)
    chk("triples.disjoint_A_terms", all(
        j3[c]["A"] > 0 for c in j3 if j3[c]["class"] == "disjoint"))
    chk("triples.bounds", all(
        j3[c]["joint"] <= min(j2[(c[0], c[1])]["joint"],
                              j2[(c[0], c[2])]["joint"],
                              j2[(c[1], c[2])]["joint"])
        for c in j3 if j3[c]["joint"]))

    # ---- quads (14950 prev + 2600 new = 17550)
    j4 = {}
    for c in itertools.combinations(range(K - 1), 4):
        j4[c] = {"class": "zero", "joint": 0, "A": 0, "B": 0}
    for c, v in quads26c.items():
        j4[c] = {"class": v["class"], "joint": v["joint"],
                 "A": v["A"], "B": v["B"]}
    chk("quads.prev_14950_stored_14235",
        len(j4) == 14950 and len(quads26c) == 14235,
        {"stored": len(quads26c)})
    chk("quads.new_2600", len(doneq) == 2600)
    for c, e in doneq.items():
        if e["class"] == "disjoint":
            j4[c] = {"class": "disjoint", "joint": e["joint"],
                     "A": e["joint_A"], "B": e["joint_B"]}
        else:
            j4[c] = {"class": e["class"], "joint": e["joint"],
                     "A": 0, "B": e["joint"]}
    chk("quads.complete_17550", len(j4) == 17550)
    qcen = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(K), 4):
        kind, _ = classify(rows, c)
        if IDX27 in c:
            qcen[kind] += 1
        # exact class match for every quad, new and prev alike:
        # the prev classes were census-verified by the k=25
        # publication and must reproduce on this assembly.
        assert j4[c]["class"] == kind, (c, j4[c]["class"], kind)
    chk("quads.new_census",
        qcen == {"b_only": 588, "zero": 1990, "disjoint": 22}, qcen)
    chk("quads.disjoint_A_terms", all(
        j4[c]["A"] > 0 for c in j4 if j4[c]["class"] == "disjoint"))
    chk("quads.disjoint_bounds", all(
        j4[c]["joint"] <= min(
            j3[tuple(sorted(set(c) - {x}))]["joint"] for x in c)
        for c in j4 if j4[c]["class"] == "disjoint"))
    prev_disjoint = [c for c in j4 if all(i != IDX27 for i in c)
                     and j4[c]["class"] == "disjoint"]
    chk("quads.prev_disjoint_233", len(prev_disjoint) == 233)

    # ---- quints (63,908 top-26 zeros + 1,872 prev b_only +
    #      14,641 new zeros + 309 new b_only = 80,730)
    j5 = {}
    n5 = 0
    cen5 = {"b_only": 0, "zero": 0, "disjoint": 0}
    dbl_hist = {}
    for c in itertools.combinations(range(K), 5):
        n5 += 1
        kind, union = classify(rows, c)
        cen5[kind] += 1
        if kind == "zero":
            j5[c] = {"class": "zero", "joint": 0, "A": 0, "B": 0}
            continue
        assert kind == "b_only", (c, kind)
        from collections import Counter
        cnt = Counter(r for i in c for r in rows[i])
        d = [r for r, v in cnt.items() if v == 2][0]
        dbl_hist[d] = dbl_hist.get(d, 0) + 1
        if IDX27 in c:
            assert c in done5, ("missing new b_only quint record", c)
            j5v = done5[c]["joint"]
        else:
            assert c in quints26, ("missing prev b_only quint "
                                   "record", c)
            j5v = quints26[c]["joint"]
        j5[c] = {"class": "b_only", "joint": j5v,
                 "A": 0, "B": j5v}
    chk("quints.census_80730",
        n5 == 80730 and cen5 == {"b_only": 2181, "zero": 78549,
                                 "disjoint": 0},
        {"census": cen5, "double_rows": dbl_hist})
    chk("quints.double_rows_hist",
        dbl_hist == {18: 1354, 15: 417, 19: 410}, dbl_hist)
    prev_cen5 = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(K - 1), 5):
        prev_cen5[classify(rows, c)[0]] += 1
    chk("quints.prev_census_matches_k26",
        prev_cen5 == {"b_only": 1872, "zero": 63908, "disjoint": 0},
        prev_cen5)
    chk("quints.new_records_309", len(done5) == 309)
    chk("quints.new_b_only_contain_rank27", all(
        IDX27 in c for c in j5
        if j5[c]["class"] == "b_only" and 25 not in c))
    chk("quints.prev_b_only_contain_rank26", all(
        25 in c for c in j5
        if j5[c]["class"] == "b_only" and IDX27 not in c))
    chk("quints.bounds", all(
        j5[c]["joint"] <= min(
            j4[tuple(sorted(set(c) - {x}))]["joint"] for x in c)
        for c in j5 if j5[c]["joint"]))
    # every b_only quint has exactly three b_only 4-subsets (remove
    # one of the three fresh roots) and two disjoint 4-subsets
    # (remove one of the two doubled-row sharers); every disjoint
    # quad has four disjoint 3-subsets (structure of the new era,
    # machine-verified)
    sub_ok = True
    for c in j5:
        if j5[c]["class"] != "b_only":
            continue
        kinds = [j4[tuple(sorted(set(c) - {x}))]["class"] for x in c]
        if sorted(kinds) != ["b_only", "b_only", "b_only",
                             "disjoint", "disjoint"]:
            sub_ok = False
    for c in j4:
        if j4[c]["class"] != "disjoint":
            continue
        kinds = [j3[tuple(sorted(set(c) - {x}))]["class"] for x in c]
        if set(kinds) != {"disjoint"}:
            sub_ok = False
    chk("quints.disjoint_quad_subset_structure", sub_ok)

    # ---- anchors and cross-lineage
    a2 = done("anchor2", lambda e: (e["idx_i"], e["idx_j"],
                                    e["lineage"]))
    a3 = done("anchor3", lambda e: (tuple(e["combo"]), e["lineage"]))
    a4 = done("anchor4", lambda e: (tuple(e["combo"]), e["lineage"]))
    chk("anchors.pairs_2x2lineages", len(a2) == 4
        and all(e["match"] for e in a2.values()),
        {"checked": sorted(a2)})
    chk("anchors.triples_2", len(a3) == 2
        and all(e["match"] for e in a3.values()))
    a4_ok = len(a4) == 4
    if a4_ok:
        by_quad = {}
        for e in a4.values():
            key = tuple(sorted(e["combo"]))
            by_quad.setdefault(key, {})[e["lineage"]] = e
        all_keys = sorted(by_quad)
        a4_ok = (len(all_keys) == 2)
        for key in all_keys:
            by_lin = by_quad[key]
            if not (set(by_lin) == {"lazypm", "mypm"}
                    and by_lin["lazypm"]["joint_A"]
                    == by_lin["mypm"]["joint_A"]
                    and by_lin["lazypm"]["joint_B"]
                    == by_lin["mypm"]["joint_B"]
                    and by_lin["lazypm"]["joint_A"]
                    == by_lin["lazypm"]["ref_A"]
                    and by_lin["lazypm"]["joint_B"]
                    == by_lin["lazypm"]["ref_B"]):
                a4_ok = False
    chk("anchors.quad_union8_published_2x2", a4_ok)
    c3 = done("cross3", lambda e: (tuple(e["combo"]), e["lineage"]))
    c4 = done("cross4", lambda e: (tuple(e["combo"]), e["lineage"]))
    cq4 = done("crossq4", lambda e: (tuple(e["combo"]),
                                      e["lineage"]))
    c5 = done("cross5", lambda e: (tuple(e["combo"]), e["lineage"]))
    chk("cross.triples_2", len(c3) == 2
        and all(e["match"] for e in c3.values()))
    chk("cross.quads_2", len(c4) == 2
        and all(e["match"] for e in c4.values()))
    chk("cross.disjoint_quads_2", len(cq4) == 2
        and all(e["match"] for e in cq4.values()))
    chk("cross.quints_2", len(c5) == 2
        and all(e["match"] for e in c5.values()))

    # ---- kill(k) k=1..26 with the fifth-order I-E
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
            vA -= j4[c]["A"]
            vB -= j4[c]["B"]
        for c in itertools.combinations(range(k), 5):
            v += j5[c]["joint"]
            vA += j5[c]["A"]
            vB += j5[c]["B"]
        kill[k] = v
        killA[k] = vA
        killB[k] = vB
        assert v == vA + vB
    chk("split.identity_per_k",
        all(kill[k] == killA[k] + killB[k] for k in range(1, K + 1)))
    chk("reproduce_k1_26",
        all(kill[k] == int(k26["values"]["kill"]["k%d" % k])
            for k in range(1, 27)))
    chk("split.reproduce_k1_26",
        all(killA[k] == int(k26["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k26["values"]["kill_B"]["k%d" % k])
            for k in range(1, 27)))
    chk("split.monotone",
        all(killA[k] <= killA[k + 1] and killB[k] <= killB[k + 1]
            for k in range(1, K)))
    chk("survival.monotone",
        all(kill[k] <= kill[k + 1] for k in range(1, K))
        and kill[K] <= total)
    chk("survival.marginal",
        0 <= kill[K] - kill[K - 1] <= mem[K - 1],
        {"k27_minus_k26": str(kill[K] - kill[K - 1]),
         "m27": str(mem[K - 1])})
    chk("survival.union_bound",
        total - kill[K] >= total - sum(mem[:K]))

    Bsurv = {k: B16 - killB[k] for k in range(1, K + 1)}
    Bsurv[0] = B16
    chk("mixed.b_survive_monotone",
        all(Bsurv[k] >= Bsurv[k + 1] for k in range(K)))

    new5 = {c: e for c, e in done5.items()}
    out = {
        "schema": "n11-cost16-survival-k27-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact survival curve extended to k=27 for the "
                  "31-row cost-16 parent: rank-27 (12,18) is the "
                  "seventh row-18 hub root (13 prior roots cover "
                  "row 18) and covers row 12 for the first time, "
                  "so the quint era opened at k=26 continues (309 "
                  "of the C(27,5)=80,780 5-subsets are 309 new "
                  "non-zero b_only quints on top of the 1,872 "
                  "published ones) and the A-type 4-way term keeps "
                  "growing (22 new disjoint quads, 255 total); 38 "
                  "new disjoint triples and 13 new disjoint pairs "
                  "add further record counts"),
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
            "survival_k25_json": {"path": K25_JSON_REL,
                                  "git_blob_sha1": K25_JSON_PIN,
                                  "commit": K25_JSON_COMMIT},
            "survival_k26_json": {"path": K26_JSON_REL,
                                  "git_blob_sha1": K26_JSON_PIN,
                                  "commit": K26_JSON_COMMIT},
        },
        "structure": {
            "rank27_root": {"root": top[IDX27]["root"],
                            "rows": list(rows[IDX27]),
                            "membership": str(mem[IDX27]),
                            "a_part": str(ap[IDX27]),
                            "b_part": str(bp[IDX27]),
                            "note": "seventh row-18 hub root (13 "
                                    "prior roots cover row 18); "
                                    "row 12 is covered for the "
                                    "first time"},
            "triple_census_k27": cen,
            "new_quad_census": qcen,
            "quint_census_k27": cen5,
            "new_quint_census": {"b_only": 309, "zero": 14641,
                                 "disjoint": 0},
            "quint_b_only_double_rows": dbl_hist,
            "quints_zero_synth_count": 14641,
            "quints_jsonl_note": ("zero quints are structural "
                                  "(classify from the pinned "
                                  "aggregate) and are not appended "
                                  "to the JSONL; finalize "
                                  "reclassifies all 65,780 "
                                  "5-subsets and asserts the exact "
                                  "census and the presence of every "
                                  "b_only record"),
            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
                             "sum j4 + sum j5 for k <= 27; "
                             "kill_A(k) = sum a - sum j2_A + "
                             "sum j3_A - sum j4_A (j5_A == 0); "
                             "kill_B(k) = sum b - sum j2_B + "
                             "sum j3_B - sum j4_B + sum j5_B; "
                             "j4_A comes from the 255 disjoint "
                             "quads (233 published at k=26, 22 new "
                             "at k=27), j5_B from the 2,181 b_only "
                             "quints (1,872 prev, 309 new)"),
            "formulas": {
                "j4_A_disjoint": ("sum_{s not in union} w1[s] * "
                                  "pm(V \\ union \\ {s}) at "
                                  "|union|=8, same union-mask "
                                  "machinery as k=14, validated by "
                                  "anchor regression and both pm "
                                  "lineages"),
                "j4_B_disjoint": ("two-case (doubled row inside / "
                                  "outside the union) at |union|=8"),
                "j5_B_b_only": ("pm(V \\ union) on the 22-row "
                               "residual, the b_only-quad pattern"),
            },
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
            "marginal_k27": str(kill[K] - kill[K - 1]),
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
                                     "joint_A": str(j4[c]["A"]),
                                     "joint_B": str(j4[c]["B"]),
                                     "joint": str(j4[c]["joint"])}
                for c in sorted(doneq)},
            "new_quints_b_only": {
                "%d,%d,%d,%d,%d" % c: {"class": "b_only",
                                        "union": done5[c]["union"],
                                        "joint_A": "0",
                                        "joint_B": str(j5[c]["B"]),
                                        "joint": str(j5[c]["joint"])}
                for c in sorted(new5)},
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
    if mode == "quints":
        sl = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return mode_quints(sl)
    if mode == "anchor":
        return mode_anchor()
    if mode == "cross":
        return mode_cross()
    if mode == "finalize":
        return finalize_mode()
    print("usage: pairs [BUDGET] | triples [SLICE] | quads [SLICE] | "
          "quints [SLICE] | anchor | cross | finalize")
    return 2


if __name__ == "__main__":
    sys.exit(main())

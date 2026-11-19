#!/usr/bin/env python3
"""Survival-curve extension to k=36 for the 31-row cost-16 parent
00000000000000003800000008001000.

rank-36 root (19,22) is the first root to cover row 22: row 22
has zero prior sharers among the top-35 roots, so it can never
double in any layer, while row 19 is now a ten-sharer hub band
row (prior sharers 0,2,3,8,9,10,15,29,32,33).  The new pair
census is 10 shared / 25 disjoint (the shared pairs are exactly
the ten row-19 sharers).  The quint era opened at k=26
continues (machine-verified from the pinned aggregate and the
k=36 preread JSON, commit 67985e92c9, before writing any pm
value):

  * 2,835 of the 52,360 new 5-subsets are structurally non-zero
    (all b_only, all containing rank-36; double rows 18:1200 /
    19:1195 / 15:364 / 16:76).  Row 22 never doubles (zero
    prior sharers) and the quint double-row histogram stays
    within the four hub rows 15/16/18/19.  The full
    C(36,5)=376,992 census is 17,434 b_only / 359,558 zero /
    0 disjoint, extending the published k=35 census
    14,599/310,033/0 exactly.  The full C(36,6)=1,947,792
    sextet census is all zero (finalize check below, extending
    the published k=26..k=35 sextet censuses), so the I-E keeps
    its fifth-order term with no sixth-order term:
      kill(k)   = sum m - sum j2 + sum j3 - sum j4 + sum j5
      kill_A(k) = sum a - sum j2_A + sum j3_A - sum j4_A  (j5_A == 0)
      kill_B(k) = sum b - sum j2_B + sum j3_B - sum j4_B + sum j5_B
    with j5_B = pm(V minus the union) on the residual, the b_only-quad
    pattern;  prev-era quint records (14,599 = 1,872 k26-era +
    309 k27-era + 331 k28-era + 2,128 k29-era + 1,328 k30-era +
    819 k31-era + 2,010 k32-era + 2,036 k33-era + 2,171 k34-era +
    1,595 k35-era) load from the pinned k=26/k=27/k=28/k=29/
    k=30/k=31/k=32/k=33/k=34/k=35 publications, new-era records
    (2,835) are computed here;
  * 168 new disjoint quads (|union|=8) extend the A-type 4-way
    term to 1,363 total.  disjoint_joint at |union|=8 was validated
    by the k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35
    publications (anchor regression, both pm lineages, 1,195
    production records); this script re-anchors it on 2 published
    k=35 disjoint quads (both pm lineages, exact A/B match)
    before production.

New-record census (machine-derived from the pinned aggregate,
independently re-derived by the k=36 preread (commit 67985e92c9,
pure Python with exact integer serialization) and asserted as
literals at load): 35 new pairs (10 shared / 25 disjoint), 595
new triples (391 b_only / 63 zero / 141 disjoint), 6,545 new
quads (2,458 b_only / 3,919 zero / 168 disjoint).  Full top-36
censuses prove C(36,3)=7,140 = 4,361/1,320/1,459, C(36,4)=58,905,
and the prev top-35 quint census must reproduce the published
k=35 values 14,599/310,033/0 exactly.  Every b_only quint keeps
the k=26 structure (three b_only plus two disjoint 4-subsets;
machine-verified for all 17,434 here).  Zero quints are NOT
appended to the JSONL; finalize reclassifies all 376,992
5-subsets and asserts the exact census.

Preload style: the k=36 preread's structural fields are
asserted as literals at load (schema, root hex, rows, prior
hit indices, censuses, histograms, disjoint quad tally and the
b_only-quint four-subset profile), and its big-integer fields
(membership/a_part/b_part = 120046727515486665 /
92003630985566871 / 28043096529919794) equal the pinned
aggregate exactly because the preread is pure Python with exact
integer serialization (no Node-era rounding erratum).

Anchors: kill/kill_A/kill_B for k=1..35 recomputed from the
assembled k=36 machinery must reproduce the pinned k=35
publication (commit 572b1365) exactly.  Cross-checks: 2 new
disjoint triples and 2 new disjoint quads recomputed with the
second pm lineage, 2 new b_only quads and 2 new b_only quints
likewise.  R stays 31: the parent is the fixed 31-row cost-16
parent (asserted at every get_parent call site); K=36 bans 36
pair roots drawn from it.

Cover-plan combinatorics only.  No engine run, no verdict.

Usage:
  python3 cost16_survival_k36_20261118.py pairs [BUDGET]
  python3 cost16_survival_k36_20261118.py triples [SLICE]
  python3 cost16_survival_k36_20261118.py quads [SLICE]
  python3 cost16_survival_k36_20261118.py quints [SLICE]
  python3 cost16_survival_k36_20261118.py anchor
  python3 cost16_survival_k36_20261118.py cross
  python3 cost16_survival_k36_20261118.py finalize
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
K = 36
# R stays 31: the parent is the fixed 31-row cost-16 parent
# (len(P["target"]) == 31, asserted at every get_parent call
# site); K=36 bans 36 pair roots drawn from it.  A wrong R
# here would silently zero every b_only joint.
R = 31
IDX36 = 35

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
K27_JSON_REL = EXP_REL + "cost16-survival-k27-20261118.json"
K27_JSON_PIN = "3dc30ad6c51cc2d7678cc8777e4af2376267ddb8"
K27_JSON_COMMIT = "9b804a9c"
K28_JSON_REL = EXP_REL + "cost16-survival-k28-20261118.json"
K28_JSON_PIN = "99db3a9a48d044727b3a4d83fb7fc97daa7513d2"
K28_JSON_COMMIT = "efc500fa"
K29_JSON_REL = EXP_REL + "cost16-survival-k29-20261118.json"
K29_JSON_PIN = "795665316c300a186979bafd2817b6961de2de60"
K29_JSON_COMMIT = "29fb9f92"
K30_JSON_REL = EXP_REL + "cost16-survival-k30-20261118.json"
K30_JSON_PIN = "9c24e7a30ad213d3b7675e620ec606b00f73a330"
K30_JSON_COMMIT = "f6a08dc5"
K31_JSON_REL = EXP_REL + "cost16-survival-k31-20261118.json"
K31_JSON_PIN = "0d9f67ee69ad4fb8aa37904ddbf6666745786807"
K31_JSON_COMMIT = "5da4cc6c"
K32_JSON_REL = EXP_REL + "cost16-survival-k32-20261118.json"
K32_JSON_PIN = "6bf47e8745300ae6235180591978daf9d7fe09e5"
K32_JSON_COMMIT = "595f0a2795"
K33_JSON_REL = EXP_REL + "cost16-survival-k33-20261118.json"
K33_JSON_PIN = "3446e9a0aec2d4cc01cbb8f062db0a36d660a65a"
K33_JSON_COMMIT = "b7ec3ebd"
K34_JSON_REL = EXP_REL + "cost16-survival-k34-20261118.json"
K34_JSON_PIN = "d485914cf7f6198a2fbb05b09d778ecec510343f"
K34_JSON_COMMIT = "b64d8fe128"
K35_JSON_REL = EXP_REL + "cost16-survival-k35-20261118.json"
K35_JSON_PIN = "80a22ac77cdc0ba0a99643e3f1be13b71565a1b7"
K35_JSON_COMMIT = "572b1365b"
K36_PREREAD_REL = EXP_REL + "cost16-survival-k36-preread-20261118.json"
K36_PREREAD_PIN = "760aa396361cc7d2ea8bc371f4dd673d962f07fe"
K36_PREREAD_COMMIT = "67985e92c9"
RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k36-20261118.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k36-20261118.json")

M36 = 120046727515486665


def load_top36():
    agg = json.loads(base.read_pinned(GROUPS_AGG_REL, GROUPS_AGG_PIN))
    top = agg["derived"]["top50_by_membership"][:K]
    assert all(e["kind"] == "pair" for e in top)
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]
    for e in top:
        assert memA[e["root"]] + memB[e["root"]] == e["membership"]
    # rank-36 root: (19,22), the first root to cover row 22; row
    # 22 has zero prior sharers among the top-35, so it can never
    # double in any layer, while row 19 is now a ten-sharer hub
    # band row (prior sharers 0,2,3,8,9,10,15,29,32,33)
    assert sorted(top[IDX36]["rows_covered"]) == [19, 22]
    assert top[IDX36]["root"] == "00000000000000801212020000001000"
    assert top[IDX36]["membership"] == M36
    # rank-35 regression anchor (published k=35 facts, commit
    # 572b1365b): first root to cover row 21 (18,21); row 21 has
    # zero prior sharers, so it can never double in any layer,
    # while row 18 is a 16-sharer hub band row
    assert sorted(top[IDX36 - 1]["rows_covered"]) == [18, 21]
    assert top[IDX36 - 1]["root"] == \
        "00000000000000801202090000001000"
    assert top[IDX36 - 1]["membership"] == 120058481266728720
    assert [i for i in range(IDX36 - 1)
            if 18 in top[i]["rows_covered"]] == [1, 4, 5, 6, 7, 11,
                                                 12, 18, 19, 20, 21,
                                                 23, 24, 26, 27, 30]
    assert [i for i in range(IDX36 - 1)
            if 21 in top[i]["rows_covered"]] == []
    assert [i for i in range(IDX36)
            if 18 in top[i]["rows_covered"]] == [1, 4, 5, 6, 7, 11,
                                                 12, 18, 19, 20, 21,
                                                 23, 24, 26, 27, 30,
                                                 34]
    assert [i for i in range(IDX36)
            if 21 in top[i]["rows_covered"]] == [34]
    # row 22 has zero prior sharers among the top-35; row 19 has
    # exactly the ten listed ones (the rank-36 root joins the nine
    # published ones)
    assert [i for i in range(IDX36)
            if 22 in top[i]["rows_covered"]] == []
    assert [i for i in range(IDX36)
            if 19 in top[i]["rows_covered"]] == [0, 2, 3, 8, 9, 10,
                                                 15, 29, 32, 33]
    total = agg["derived"]["total_minimum_covers"]
    A16 = agg["derived"]["type_A_disjoint"]
    B16 = agg["derived"]["type_B_one_duplicate_row"]
    # preread structural pins (commit 67985e92c9); the k=36
    # preread is pure Python with exact integer serialization
    # (like the k=32/k=33/k=34/k=35 prereads), so its big-integer
    # fields equal the pinned aggregate exactly and need no erratum
    pre = json.loads(base.read_pinned(K36_PREREAD_REL, K36_PREREAD_PIN))
    assert pre["schema"] == "n11-cost16-k36-preread-20261119-v1"
    assert pre["check_count"] == 33 and pre["all_pass"] is True
    r36 = pre["rank36"]
    assert r36["root"] == top[IDX36]["root"]
    assert r36["rows"] == [19, 22]
    assert r36["membership"] == M36
    assert r36["a_part"] == memA[top[IDX36]["root"]]
    assert r36["b_part"] == memB[top[IDX36]["root"]]
    assert memA[top[IDX36]["root"]] + memB[top[IDX36]["root"]] == M36
    assert r36["prior_hits"] == {"19": 10, "22": 0}
    assert r36["prior_hit_indices"]["19"] == [0, 2, 3, 8, 9, 10,
                                              15, 29, 32, 33]
    assert r36["prior_hit_indices"]["22"] == []
    # the pair layer reports shared/disjoint (same spelling as
    # the rank-35 body of the k=35 preread); the regression
    # layers below keep the older b_only/zero pair spelling
    _pc = r36["new_census"]["pair"]
    assert _pc == {"shared": 10, "disjoint": 25, "total": 35,
                   "expected_total": 35}
    assert _pc["shared"] + _pc["disjoint"] == _pc["total"]
    assert _pc["total"] == _pc["expected_total"] == 35
    assert r36["new_census"]["triple"] == {"b_only": 391, "zero": 63,
                                           "disjoint": 141,
                                           "total": 595,
                                           "expected_total": 595}
    assert r36["new_census"]["quad"] == {"b_only": 2458,
                                         "zero": 3919,
                                         "disjoint": 168,
                                         "total": 6545,
                                         "expected_total": 6545}
    assert r36["new_census"]["quint"] == {"b_only": 2835,
                                          "zero": 49525,
                                          "disjoint": 0,
                                          "total": 52360,
                                          "expected_total": 52360}
    assert r36["new_triple_double_row_histogram"] == {
        "0": 1, "4": 1, "15": 15, "16": 3, "18": 136,
        "19": 232, "23": 1, "24": 1, "30": 1}
    assert r36["new_quad_double_row_histogram"] == {
        "0": 16, "4": 2, "15": 260, "16": 32, "18": 992,
        "19": 1150, "23": 2, "24": 2, "30": 2}
    assert r36["new_quint_double_row_histogram"] == {
        "15": 364, "16": 76, "18": 1200, "19": 1195}
    assert r36["b_only_quint_four_subset_profiles"] == {
        "3/2/0": 2835}
    assert r36["disjoint_quad_count"] == 168
    assert r36["disjoint_quad_union_sizes"] == {"8": 168}
    assert r36["cumulative_disjoint_quads"] == 1363
    assert r36["full_triples"]["counts"] == {"b_only": 4361,
                                             "zero": 1320,
                                             "disjoint": 1459}
    assert r36["full_triples"]["total"] == 7140
    assert r36["full_triples"]["compared"] == 7140
    assert r36["full_triples"]["mismatches"] == 0
    assert r36["full_quints"]["counts"] == {"b_only": 17434,
                                            "zero": 359558,
                                            "disjoint": 0}
    assert r36["full_quints"]["total"] == 376992
    assert r36["full_quints"]["double_row_histogram"] == {
        "15": 2785, "16": 545, "18": 9217, "19": 4887}
    assert r36["sextet_census"]["total"] == 1947792
    assert r36["sextet_census"]["counts"] == {"b_only": 0,
                                              "zero": 1947792,
                                              "disjoint": 0}
    # rank-35 regression layer of the k=36 preread (machine
    # re-derived from the same pinned aggregate against the
    # published k=35 preread, commit 90fc51c9); note the older
    # b_only/zero pair spelling here (b_only:16, zero:0), and
    # that this layer has no disjoint_quad_count key
    r35 = pre["rank35_regression"]
    assert r35["root"] == top[IDX36 - 1]["root"]
    assert r35["rows"] == [18, 21]
    assert r35["membership"] == 120058481266728720
    assert r35["a_part"] == memA[top[IDX36 - 1]["root"]]
    assert r35["b_part"] == memB[top[IDX36 - 1]["root"]]
    assert r35["prior_hits"] == {"18": 16, "21": 0}
    assert r35["prior_hit_indices"]["18"] == [1, 4, 5, 6, 7, 11, 12,
                                              18, 19, 20, 21, 23, 24,
                                              26, 27, 30]
    assert r35["prior_hit_indices"]["21"] == []
    assert r35["new_census"]["pair"] == {"b_only": 16, "zero": 0,
                                         "disjoint": 18, "total": 34,
                                         "expected_total": 34}
    assert r35["new_census"]["triple"] == {"b_only": 348, "zero": 133,
                                           "disjoint": 80,
                                           "total": 561,
                                           "expected_total": 561}
    assert r35["new_census"]["quad"] == {"b_only": 1612,
                                         "zero": 4289,
                                         "disjoint": 83,
                                         "total": 5984,
                                         "expected_total": 5984}
    assert r35["new_census"]["quint"] == {"b_only": 1595,
                                          "zero": 44781,
                                          "disjoint": 0,
                                          "total": 46376,
                                          "expected_total": 46376}
    assert r35["new_triple_double_row_histogram"] == {
        "0": 3, "4": 1, "5": 1, "15": 21, "16": 1, "18": 275,
        "19": 45, "30": 1}
    assert r35["new_quad_double_row_histogram"] == {
        "0": 14, "4": 2, "5": 6, "15": 156, "16": 13, "18": 1155,
        "19": 264, "30": 2}
    assert r35["new_quint_double_row_histogram"] == {
        "15": 177, "16": 33, "18": 1112, "19": 273}
    assert r35["b_only_quint_four_subset_profiles"] == {
        "3/2/0": 1595}
    assert r35["full_triples"]["counts"] == {"b_only": 3970,
                                             "zero": 1257,
                                             "disjoint": 1318}
    assert r35["full_triples"]["total"] == 6545
    assert r35["full_quints"]["counts"] == {"b_only": 14599,
                                            "zero": 310033,
                                            "disjoint": 0}
    assert r35["full_quints"]["total"] == 324632
    assert r35["full_quints"]["double_row_histogram"] == {
        "15": 2421, "16": 469, "18": 8017, "19": 3692}
    assert r35["sextet_census"]["total"] == 1623160
    assert r35["sextet_census"]["counts"] == {"b_only": 0,
                                              "zero": 1623160,
                                              "disjoint": 0}
    assert r35["mismatches"] == 0
    # rank-34 regression layer (light): still pinned against the
    # published k=34 preread facts (commit 2a14f351)
    r34 = pre["rank34_regression"]
    assert r34["root"] == "00000000080000003800000088001000"
    assert r34["rows"] == [9, 19]
    assert r34["membership"] == 120079520746539458
    assert r34["a_part"] == 92056115579095019
    assert r34["b_part"] == 28023405167444439
    assert r34["mismatches"] == 0
    return agg, top, memA, memB, total, A16, B16, pre


def load_k36_base():
    """595 pairwise joints, 6,545 triples, the 51,645 stored quads
    and the 14,599 b_only quints among the top-35, from the pinned
    k14..k34 publications plus the pinned k=35 result."""
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
    # k=27 era: 26 pairs, 325 triples, 2,600 quads (all classes
    # recorded, including the 22 disjoint quads with their A/B
    # split): cumulative stored 14,235 + 2,600 = 16,835 of the
    # C(27,4)=17,550 prev quads; the remaining 715 are the
    # k14-era hub-only quads, never stored and structurally zero.
    k27 = json.loads(base.read_pinned(K27_JSON_REL, K27_JSON_PIN))
    for key, v in k27["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 351
    for key, v in k27["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 2925
    for key, v in k27["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 16835
    # k=28 era: 27 pairs, 351 triples, 2,925 quads (all classes
    # recorded, including the 22 disjoint quads with their A/B
    # split): cumulative stored 16,835 + 2,925 = 19,760 of the
    # C(28,4)=20,475 prev quads; the remaining 715 are the
    # k14-era hub-only quads, never stored and structurally zero.
    k28 = json.loads(base.read_pinned(K28_JSON_REL, K28_JSON_PIN))
    for key, v in k28["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 378
    for key, v in k28["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 3276
    for key, v in k28["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 19760
    # k=29 era: 28 pairs, 378 triples, 3,276 quads (all classes
    # recorded, including the 225 disjoint quads with their A/B
    # split): cumulative stored 19,760 + 3,276 = 23,036 of the
    # C(29,4)=23,751 prev quads; the remaining 715 are the
    # k14-era hub-only quads, never stored and structurally zero.
    k29 = json.loads(base.read_pinned(K29_JSON_REL, K29_JSON_PIN))
    for key, v in k29["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 406
    for key, v in k29["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 3654
    for key, v in k29["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 23036
    k30 = json.loads(base.read_pinned(K30_JSON_REL, K30_JSON_PIN))
    for key, v in k30["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 435
    for key, v in k30["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 4060
    for key, v in k30["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 26690
    k31j = json.loads(base.read_pinned(K31_JSON_REL, K31_JSON_PIN))
    for key, v in k31j["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        assert 30 in (i, j) and 31 not in (i, j), (i, j)
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 465
    for key, v in k31j["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 30 in c and 31 not in c, c
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 4495
    for key, v in k31j["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 30 in c and 31 not in c, c
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 30750
    # k=32 era: 31 pairs, 465 triples, 4,495 quads (all classes
    # recorded, including the 158 disjoint quads with their A/B
    # split): cumulative stored 30,750 + 4,495 = 35,245 of the
    # C(32,4)=35,960 prev quads; the remaining 715 are the
    # k14-era hub-only quads, never stored and structurally zero.
    k32j = json.loads(base.read_pinned(K32_JSON_REL, K32_JSON_PIN))
    for key, v in k32j["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        assert 31 in (i, j) and 32 not in (i, j), (i, j)
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 496
    for key, v in k32j["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 31 in c and 32 not in c, c
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 4960
    for key, v in k32j["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 31 in c and 32 not in c, c
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 35245
    # k=33 era: 32 pairs, 496 triples, 4,960 quads (all classes
    # recorded, including the 146 disjoint quads with their A/B
    # split): cumulative stored 35,245 + 4,960 = 40,205 of the
    # C(33,4)=40,920 prev quads; the remaining 715 are the
    # k14-era hub-only quads, never stored and structurally zero.
    k33j = json.loads(base.read_pinned(K33_JSON_REL, K33_JSON_PIN))
    for key, v in k33j["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        assert 32 in (i, j) and 33 not in (i, j), (i, j)
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 528
    for key, v in k33j["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 32 in c and 33 not in c, c
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 5456
    for key, v in k33j["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 32 in c and 33 not in c, c
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 40205
    # k=34 era: 33 pairs, 528 triples, 5,456 quads (all classes
    # recorded, including the 146 disjoint quads with their A/B
    # split): cumulative stored 40,205 + 5,456 = 45,661 of the
    # C(34,4)=46,376 prev quads; the remaining 715 are the
    # k14-era hub-only quads, never stored and structurally zero.
    k34j = json.loads(base.read_pinned(K34_JSON_REL, K34_JSON_PIN))
    for key, v in k34j["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        assert 33 in (i, j) and 34 not in (i, j), (i, j)
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 561
    for key, v in k34j["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 33 in c and 34 not in c, c
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 5984
    for key, v in k34j["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 33 in c and 34 not in c, c
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 45661
    # k=35 era: 34 pairs, 561 triples, 5,984 quads (all classes
    # recorded, including the 83 disjoint quads with their A/B
    # split): cumulative stored 45,661 + 5,984 = 51,645 of the
    # C(35,4)=52,360 prev quads; the remaining 715 are the
    # k14-era hub-only quads, never stored and structurally zero.
    k35j = json.loads(base.read_pinned(K35_JSON_REL, K35_JSON_PIN))
    for key, v in k35j["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        assert 34 in (i, j) and 35 not in (i, j), (i, j)
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 595
    for key, v in k35j["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 34 in c and 35 not in c, c
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 6545
    for key, v in k35j["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 34 in c and 35 not in c, c
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 51645
    quints26 = {}
    for key, v in k26["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints26[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints26) == 1872
    assert all(25 in c and 26 not in c for c in quints26)
    quints27 = {}
    for key, v in k27["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints27[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints27) == 309
    assert all(26 in c and 27 not in c for c in quints27)
    quints28 = {}
    for key, v in k28["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints28[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints28) == 331
    assert all(27 in c and 28 not in c for c in quints28)
    quints29 = {}
    for key, v in k29["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints29[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints29) == 2128
    assert all(28 in c and 29 not in c for c in quints29)
    quints30 = {}
    for key, v in k30["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints30[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints30) == 1328
    assert all(29 in c and 30 not in c for c in quints30)
    quints31 = {}
    for key, v in k31j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints31[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints31) == 819
    assert all(30 in c and 31 not in c for c in quints31)
    quints32 = {}
    for key, v in k32j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints32[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints32) == 2010
    assert all(31 in c and 32 not in c for c in quints32)
    quints33 = {}
    for key, v in k33j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints33[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints33) == 2036
    assert all(32 in c and 33 not in c for c in quints33)
    quints34 = {}
    for key, v in k34j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints34[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints34) == 2171
    assert all(33 in c and 34 not in c for c in quints34)
    quints35 = {}
    for key, v in k35j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints35[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints35) == 1595
    assert all(34 in c and 35 not in c for c in quints35)
    quints_prev = {}
    quints_prev.update(quints26)
    quints_prev.update(quints27)
    quints_prev.update(quints28)
    quints_prev.update(quints29)
    quints_prev.update(quints30)
    quints_prev.update(quints31)
    quints_prev.update(quints32)
    quints_prev.update(quints33)
    quints_prev.update(quints34)
    quints_prev.update(quints35)
    assert len(quints_prev) == 14599
    return k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, \
        k24, k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, \
        pairs, triples, quads, quints_prev


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
    return [(i, IDX36) for i in range(IDX36)]


def new_triple_combos():
    return [(IDX36, i, j) for i, j in
            itertools.combinations(range(IDX36), 2)]


def new_quad_combos():
    return [(IDX36, i, j, l) for i, j, l in
            itertools.combinations(range(IDX36), 3)]


def new_quint_combos():
    return [(IDX36, i, j, l, m) for i, j, l, m in
            itertools.combinations(range(IDX36), 4)]


def mode_pairs(budget):
    agg, top, memA, memB, total, A16, B16, pre = load_top36()
    P = k14m.get_parent()
    assert len(P["target"]) == R
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    base.STATE_CAP = 16_000_000
    base.BUDGET_SECONDS = budget
    pm = base.PmLazy(P["edge_w"], R)
    donep = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    todo = [c for c in new_pair_combos() if c not in donep]
    print("[pairs] todo %d (done %d/35)" % (len(todo), len(donep)),
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
    print("[pairs] done %d/35" % len(done("pair",
           lambda e: (e["idx_i"], e["idx_j"]))), flush=True)
    return 0


def mode_triples(slice_arg):
    agg, top, memA, memB, total, A16, B16, pre = load_top36()
    P = k14m.get_parent()
    assert len(P["target"]) == R
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_triple_combos()
    assert len(combos) == 595
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
    print("[triples] slice %d done, done %d/595 in %.1fs"
          % (slice_arg, len(done("triple", lambda e: tuple(e["combo"]))),
             time.time() - t00), flush=True)
    return 0


def mode_quads(slice_arg):
    agg, top, memA, memB, total, A16, B16, pre = load_top36()
    P = k14m.get_parent()
    assert len(P["target"]) == R
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_quad_combos()
    assert len(combos) == 6545
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
    print("[quads] slice %d done, done %d/6545"
          % (slice_arg, len(done("quad", lambda e: tuple(e["combo"])))),
          flush=True)
    return 0


def mode_quints(slice_arg):
    """B-type-only 5-way joints for the 2,835 new b_only quints
    (the 14,599 prev-era records load from the pinned
    k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35 JSONs).
    Zero
    quints are structural (classify from the pinned aggregate) and
    are synthesized in finalize, not appended here."""
    agg, top, memA, memB, total, A16, B16, pre = load_top36()
    P = k14m.get_parent()
    assert len(P["target"]) == R
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_quint_combos()
    assert len(combos) == 52360
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
    print("[quints] slice %d done, done %d/2835b_only in %.1fs"
          % (slice_arg,
             len(done("quint", lambda e: tuple(e["combo"]))),
             time.time() - t00), flush=True)
    return 0


def mode_anchor():
    """Pre-production validation of disjoint_joint at |union|=4
    (published k13-era pair joints, both pm lineages), |union|=6
    (2 published k35 disjoint triples) and |union|=8 (2 published
    k35 disjoint quads, both pm lineages with exact A/B match
    against the pinned publication).  The |union|=8 machinery was
    introduced at k=26 and extended by the k=27/k=28/k=29/k=30/
    k=31/k=32/k=33/k=34/k=35 publications (1,195 production
    records); this re-anchors it on published records before
    production."""
    agg, top, memA, memB, total, A16, B16, pre = load_top36()
    P = k14m.get_parent()
    assert len(P["target"]) == R
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
    k35ja = json.loads(base.read_pinned(K35_JSON_REL, K35_JSON_PIN))
    pub3 = [tuple(int(x) for x in key.split(","))
            for key, v in k35ja["values"]["new_triples"].items()
            if v["class"] == "disjoint"]
    pub3.sort()
    assert len(pub3) >= 2
    for combo in pub3[:2]:
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        ref = k35ja["values"]["new_triples"]["%d,%d,%d" % combo]
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
            for key, v in k35ja["values"]["new_quads"].items()
            if v["class"] == "disjoint"]
    pub4.sort()
    assert len(pub4) >= 2
    for combo in pub4[:2]:
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        ref = k35ja["values"]["new_quads"]["%d,%d,%d,%d" % combo]
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
    agg, top, memA, memB, total, A16, B16, pre = load_top36()
    P = k14m.get_parent()
    assert len(P["target"]) == R
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

    agg, top, memA, memB, total, A16, B16, pre = load_top36()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    mem = [e["membership"] for e in top]
    ap = [memA[e["root"]] for e in top]
    bp = [memB[e["root"]] for e in top]
    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, \
        pairs_prev, triples_prev, quads_prev, quints_prev \
        = load_k36_base()
    donep = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    donet = done("triple", lambda e: tuple(sorted(e["combo"])))
    doneq = done("quad", lambda e: tuple(sorted(e["combo"])))
    done5 = done("quint", lambda e: tuple(sorted(e["combo"])))

    # ---- pairs (595 + 35 = 630)
    j2 = dict(pairs_prev)
    chk("pairs.prev_595", len(pairs_prev) == 595)
    chk("pairs.new_35", len(donep) == 35)
    for c, e in donep.items():
        j2[c] = {"A": e["joint_A"], "B": e["joint_B"],
                 "joint": e["joint"], "shared": e["shared_row"]}
    chk("pairs.complete_630", len(j2) == 630)
    chk("pairs.bounds", all(
        j2[c]["joint"] <= min(mem[c[0]], mem[c[1]])
        and j2[c]["A"] <= min(ap[c[0]], ap[c[1]])
        and j2[c]["B"] <= min(bp[c[0]], bp[c[1]]) for c in j2))
    shared_new = [c for c in donep if donep[c]["shared_row"]]
    chk("pairs.new_census",
        len(shared_new) == 10 and len(donep) - len(shared_new) == 25,
        {"shared": len(shared_new),
         "disjoint": len(donep) - len(shared_new)})
    chk("pairs.shared_jointA_zero", all(
        j2[c]["A"] == 0 for c in j2 if j2[c]["shared"]))

    # ---- triples (6545 + 595 = 7140)
    j3 = {}
    for c, v in triples_prev.items():
        cls = v["class"]
        eff = "zero" if cls in ("zero", "zero3x", "zero2x2") else cls
        if eff == "disjoint":
            j3[c] = {"class": eff, "A": v["A"], "B": v["B"],
                     "joint": v["joint"]}
        else:
            j3[c] = {"class": eff, "A": 0, "B": v["joint"],
                     "joint": v["joint"]}
    chk("triples.prev_6545", len(j3) == 6545)
    chk("triples.new_595", len(donet) == 595)
    for c, e in donet.items():
        j3[c] = {"class": e["class"], "A": e["joint_A"],
                 "B": e["joint_B"], "joint": e["joint"]}
    chk("triples.complete_7140", len(j3) == 7140)
    cen = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(K), 3):
        kind, _ = classify(rows, c)
        cen[kind] += 1
        assert j3[c]["class"] == kind, (c, j3[c]["class"], kind)
    chk("triples.census",
        cen == {"b_only": 4361, "zero": 1320, "disjoint": 1459}, cen)
    chk("preread_match.triple_census", cen == {
        "b_only": pre["rank36"]["full_triples"]["counts"]["b_only"],
        "zero": pre["rank36"]["full_triples"]["counts"]["zero"],
        "disjoint":
            pre["rank36"]["full_triples"]["counts"]["disjoint"]})
    chk("triples.disjoint_A_terms", all(
        j3[c]["A"] > 0 for c in j3 if j3[c]["class"] == "disjoint"))
    chk("triples.bounds", all(
        j3[c]["joint"] <= min(j2[(c[0], c[1])]["joint"],
                              j2[(c[0], c[2])]["joint"],
                              j2[(c[1], c[2])]["joint"])
        for c in j3 if j3[c]["joint"]))

    # ---- quads (52360 prev + 6545 new = 58905)
    j4 = {}
    for c in itertools.combinations(range(K - 1), 4):
        j4[c] = {"class": "zero", "joint": 0, "A": 0, "B": 0}
    for c, v in quads_prev.items():
        j4[c] = {"class": v["class"], "joint": v["joint"],
                 "A": v["A"], "B": v["B"]}
    chk("quads.prev_52360_stored_51645",
        len(j4) == 52360 and len(quads_prev) == 51645,
        {"stored": len(quads_prev)})
    chk("quads.new_6545", len(doneq) == 6545)
    for c, e in doneq.items():
        if e["class"] == "disjoint":
            j4[c] = {"class": "disjoint", "joint": e["joint"],
                     "A": e["joint_A"], "B": e["joint_B"]}
        else:
            j4[c] = {"class": e["class"], "joint": e["joint"],
                     "A": 0, "B": e["joint"]}
    chk("quads.complete_58905", len(j4) == 58905)
    qcen = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(K), 4):
        kind, _ = classify(rows, c)
        if IDX36 in c:
            qcen[kind] += 1
        # exact class match for every quad, new and prev alike:
        # the prev classes were census-verified by the k=26
        # publication and must reproduce on this assembly.
        assert j4[c]["class"] == kind, (c, j4[c]["class"], kind)
    chk("quads.new_census",
        qcen == {"b_only": 2458, "zero": 3919, "disjoint": 168},
        qcen)
    chk("preread_match.new_quad_census", qcen == {
        "b_only": pre["rank36"]["new_census"]["quad"]["b_only"],
        "zero": pre["rank36"]["new_census"]["quad"]["zero"],
        "disjoint": pre["rank36"]["new_census"]["quad"]["disjoint"]})
    chk("quads.disjoint_A_terms", all(
        j4[c]["A"] > 0 for c in j4 if j4[c]["class"] == "disjoint"))
    chk("quads.disjoint_bounds", all(
        j4[c]["joint"] <= min(
            j3[tuple(sorted(set(c) - {x}))]["joint"] for x in c)
        for c in j4 if j4[c]["class"] == "disjoint"))
    prev_disjoint = [c for c in j4 if all(i != IDX36 for i in c)
                     and j4[c]["class"] == "disjoint"]
    chk("quads.prev_disjoint_1195", len(prev_disjoint) == 1195)
    # new b_only quads double-row histogram (machine-derived;
    # row 22 cannot double (zero prior sharers among the top-35);
    # rows 18 and 19 are the dominant new double rows (992 and
    # 1,150 of the 2,458 new b_only quads), while the four hub
    # rows keep their families); the b_only triple double-row
    # histogram is recorded as a computed fact too
    from collections import Counter
    triple_dbl_hist = {}
    for c, e in donet.items():
        if e["class"] != "b_only":
            continue
        cnt = Counter(r for i in c for r in rows[i])
        d = [r for r, v in cnt.items() if v == 2][0]
        triple_dbl_hist[d] = triple_dbl_hist.get(d, 0) + 1
    chk("triples.new_b_only_double_rows",
        triple_dbl_hist == {0: 1, 4: 1, 15: 15, 16: 3,
                            18: 136, 19: 232, 23: 1, 24: 1, 30: 1},
        triple_dbl_hist)
    quad_dbl_hist = {}
    for c, e in doneq.items():
        if e["class"] != "b_only":
            continue
        cnt = Counter(r for i in c for r in rows[i])
        d = [r for r, v in cnt.items() if v == 2][0]
        quad_dbl_hist[d] = quad_dbl_hist.get(d, 0) + 1
    chk("quads.new_b_only_double_row_22_absent",
        quad_dbl_hist.get(22, 0) == 0, quad_dbl_hist)
    chk("quads.new_b_only_double_rows",
        quad_dbl_hist == {0: 16, 4: 2, 15: 260, 16: 32,
                          18: 992, 19: 1150, 23: 2, 24: 2, 30: 2},
        quad_dbl_hist)

    # ---- quints (310,033 top-35 zeros + 14,599 prev b_only +
    #      49,525 new zeros + 2,835 new b_only = 376,992)
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
        if IDX36 in c:
            assert c in done5, ("missing new b_only quint record", c)
            j5v = done5[c]["joint"]
        else:
            assert c in quints_prev, ("missing prev b_only quint "
                                   "record", c)
            j5v = quints_prev[c]["joint"]
        j5[c] = {"class": "b_only", "joint": j5v,
                 "A": 0, "B": j5v}
    chk("quints.census_376992",
        n5 == 376992 and cen5 == {"b_only": 17434, "zero": 359558,
                                  "disjoint": 0},
        {"census": cen5, "double_rows": dbl_hist})
    chk("quints.double_rows_hist",
        dbl_hist == {15: 2785, 16: 545, 18: 9217, 19: 4887},
        dbl_hist)
    chk("preread_match.quint_census", cen5 == {
        "b_only": pre["rank36"]["full_quints"]["counts"]["b_only"],
        "zero": pre["rank36"]["full_quints"]["counts"]["zero"],
        "disjoint": pre["rank36"]["full_quints"]["counts"]["disjoint"]})
    chk("preread_match.quint_double_rows", dbl_hist == {
        int(r): v for r, v in
        pre["rank36"]["full_quints"]["double_row_histogram"].items()})
    prev_cen5 = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(K - 1), 5):
        prev_cen5[classify(rows, c)[0]] += 1
    chk("quints.prev_census_matches_k35",
        prev_cen5 == {"b_only": 14599, "zero": 310033,
                     "disjoint": 0},
        prev_cen5)
    chk("quints.new_records_2835", len(done5) == 2835)
    chk("quints.new_b_only_contain_rank35", all(
        IDX36 in c for c in j5
        if j5[c]["class"] == "b_only" and 25 not in c
        and 26 not in c and 27 not in c and 28 not in c
        and 29 not in c and 30 not in c and 31 not in c
        and 32 not in c and 33 not in c and 34 not in c))
    chk("quints.prev_b_only_contain_rank26_through_35", all(
        (25 in c) or (26 in c) or (27 in c) or (28 in c)
        or (29 in c) or (30 in c) or (31 in c) or (32 in c)
        or (33 in c) or (34 in c)
        for c in j5
        if j5[c]["class"] == "b_only" and IDX36 not in c))
    chk("quints.bounds", all(
        j5[c]["joint"] <= min(
            j4[tuple(sorted(set(c) - {x}))]["joint"] for x in c)
        for c in j5 if j5[c]["joint"]))
    # new-era b_only quints never double row 22: row 22 has
    # zero prior sharers among the top-35 (the rank-36 root
    # is its first and so far only member), so it cannot
    # double in any layer; the new-era double-row histogram
    # stays within the four hub rows 15/16/18/19
    # (machine-derived from the 2,835 computed records; the
    # preread new_quint histogram agrees)
    new5_dbl = {}
    for c, e in done5.items():
        cnt = Counter(r for i in c for r in rows[i])
        d = [r for r, v in cnt.items() if v == 2][0]
        new5_dbl[d] = new5_dbl.get(d, 0) + 1
    chk("quints.new_era_double_row_22_absent",
        new5_dbl == {15: 364, 16: 76, 18: 1200, 19: 1195}, new5_dbl)
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

    # ---- sextets: the quint-order I-E truncation stays closed at
    # k=36.  The published sextet census (commit 583b0bf1) proved
    # C(26,6)/C(27,6)/C(28,6) all zero, and the k=29/k=30/k=31/
    # k=32/k=33/k=34/k=35 publications reclassified C(29,6)/
    # C(30,6)/C(31,6)/C(32,6)/C(33,6)/C(34,6)/C(35,6) all zero
    # (zero is superset-closed); a 6-subset of the top-36 either
    # lies inside the top-35 (already zero) or contains the
    # rank-36 root, so the full C(36,6) reclassification here
    # closes the k=36 truncation (also cross-checked against
    # the k=36 preread sextet census, commit 67985e92c9).
    cen6 = {"b_only": 0, "zero": 0, "disjoint": 0}
    n6 = 0
    for c in itertools.combinations(range(K), 6):
        n6 += 1
        cen6[classify(rows, c)[0]] += 1
    chk("sextet_census_k36",
        n6 == 1947792 and cen6 == {"b_only": 0, "zero": 1947792,
                                   "disjoint": 0}, cen6)
    chk("preread_match.sextet_census", cen6 == {
        "b_only": pre["rank36"]["sextet_census"]["counts"]["b_only"],
        "zero": pre["rank36"]["sextet_census"]["counts"]["zero"],
        "disjoint":
            pre["rank36"]["sextet_census"]["counts"]["disjoint"]})

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

    # ---- kill(k) k=1..34 with the fifth-order I-E
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
    chk("reproduce_k1_35",
        all(kill[k] == int(k35j["values"]["kill"]["k%d" % k])
            for k in range(1, 36)))
    chk("split.reproduce_k1_35",
        all(killA[k] == int(k35j["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k35j["values"]["kill_B"]["k%d" % k])
            for k in range(1, 36)))
    chk("split.monotone",
        all(killA[k] <= killA[k + 1] and killB[k] <= killB[k + 1]
            for k in range(1, K)))
    chk("survival.monotone",
        all(kill[k] <= kill[k + 1] for k in range(1, K))
        and kill[K] <= total)
    chk("survival.marginal",
        0 <= kill[K] - kill[K - 1] <= mem[K - 1],
        {"k36_minus_k35": str(kill[K] - kill[K - 1]),
         "m36": str(mem[K - 1])})
    chk("survival.union_bound",
        total - kill[K] >= total - sum(mem[:K]))

    Bsurv = {k: B16 - killB[k] for k in range(1, K + 1)}
    Bsurv[0] = B16
    chk("mixed.b_survive_monotone",
        all(Bsurv[k] >= Bsurv[k + 1] for k in range(K)))

    new5 = {c: e for c, e in done5.items()}
    out = {
        "schema": "n11-cost16-survival-k36-20261119-v1",
        "date": "2026-11-19",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact survival curve extended to k=36 for the "
                  "31-row cost-16 parent: rank-36 (19,22) is the "
                  "first root to cover row 22 (zero prior sharers, "
                  "so it can never double in any layer), row 19 is "
                  "now a ten-sharer hub band row, the new pair "
                  "census is 10 shared / 25 disjoint (the shared "
                  "pairs are exactly the ten row-19 sharers), and "
                  "the quint era opened at k=26 continues with "
                  "2,835 new non-zero b_only quints of the "
                  "C(36,5)=376,992 5-subsets on top of the 14,599 "
                  "published ones (the quint double-row histogram "
                  "stays within the four hub rows 15/16/18/19: "
                  "15:2785 / 16:545 / 18:9217 / 19:4887) and the "
                  "A-type 4-way term grows to 1,363 (168 new "
                  "disjoint quads on top of the 1,195 published); "
                  "141 new disjoint triples, 25 new disjoint pairs "
                  "and 10 shared ones; the full C(36,6)=1,947,792 "
                  "sextet census is all zero so the I-E stays "
                  "closed at the fifth order"),
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
            "survival_k27_json": {"path": K27_JSON_REL,
                                  "git_blob_sha1": K27_JSON_PIN,
                                  "commit": K27_JSON_COMMIT},
            "survival_k28_json": {"path": K28_JSON_REL,
                                  "git_blob_sha1": K28_JSON_PIN,
                                  "commit": K28_JSON_COMMIT},
            "survival_k29_json": {"path": K29_JSON_REL,
                                  "git_blob_sha1": K29_JSON_PIN,
                                  "commit": K29_JSON_COMMIT},
            "survival_k30_json": {"path": K30_JSON_REL,
                                  "git_blob_sha1": K30_JSON_PIN,
                                  "commit": K30_JSON_COMMIT},
            "survival_k31_json": {"path": K31_JSON_REL,
                                  "git_blob_sha1": K31_JSON_PIN,
                                  "commit": K31_JSON_COMMIT},
            "survival_k32_json": {"path": K32_JSON_REL,
                                  "git_blob_sha1": K32_JSON_PIN,
                                  "commit": K32_JSON_COMMIT},
            "survival_k33_json": {"path": K33_JSON_REL,
                                  "git_blob_sha1": K33_JSON_PIN,
                                  "commit": K33_JSON_COMMIT},
            "survival_k34_json": {"path": K34_JSON_REL,
                                  "git_blob_sha1": K34_JSON_PIN,
                                  "commit": K34_JSON_COMMIT},
            "survival_k35_json": {"path": K35_JSON_REL,
                                  "git_blob_sha1": K35_JSON_PIN,
                                  "commit": K35_JSON_COMMIT},
            "k36_preread": {"path": K36_PREREAD_REL,
                            "git_blob_sha1": K36_PREREAD_PIN,
                            "commit": K36_PREREAD_COMMIT},
        },
        "structure": {
            "rank36_root": {"root": top[IDX36]["root"],
                            "rows": list(rows[IDX36]),
                            "membership": str(mem[IDX36]),
                            "a_part": str(ap[IDX36]),
                            "b_part": str(bp[IDX36]),
                            "note": "rank-36 (19,22): row 22 "
                                    "has zero prior sharers among "
                                    "the top-35 (first covered at "
                                    "rank-36, so it can never "
                                    "double in any layer), while "
                                    "row 19 is now a ten-sharer "
                                    "hub band row (indices 0,2,3,"
                                    "8,9,10,15,29,32,33); 25 "
                                    "disjoint and 10 shared "
                                    "partners"},
            "preread_exact_integers": (
                {"note": "the k=36 preread (commit 67985e92c9) is "
                         "pure Python with exact integer "
                         "serialization (same toolchain as the "
                         "k=32/k=33/k=34/k=35 prereads, commits "
                         "490a3e44 / 67068e07 / 2a14f351 / "
                         "90fc51c9), so it needs no big-integer "
                         "erratum, and its "
                         "membership/a_part/b_part "
                         "(120046727515486665 / 92003630985566871 / "
                         "28043096529919794) equal the pinned "
                         "aggregate exactly (asserted at load); "
                         "the structural fields (rows, hex, prior "
                         "hit indices, censuses, histograms) are "
                         "cross-checked at load and by the "
                         "preread_match.* finalize checks"}),"triple_census_k36": cen,
            "new_quad_census": qcen,
            "quint_census_k36": cen5,
            "new_quint_census": {"b_only": 2835, "zero": 49525,
                                 "disjoint": 0},
            "new_quad_b_only_double_row_histogram": (
                {"note": "row 22 cannot double (zero "
                         "prior sharers); rows 18 and 19 are the "
                         "dominant new double rows (992 and 1,150 "
                         "of the 2,458 new b_only quads), "
                         "machine-derived from the computed new "
                         "quads in this finalize",
                 "histogram": quad_dbl_hist}),
            "new_triple_b_only_double_row_histogram": (
                {"note": "computed fact: 136 of the 391 new b_only "
                         "triples double row 18 and 232 double "
                         "row 19; row 22 never doubles",
                 "histogram": triple_dbl_hist}),
            "sextet_census_k36": cen6,
            "quint_b_only_double_rows": dbl_hist,
            "quints_zero_synth_count": 49525,
            "quints_jsonl_note": ("zero quints are structural "
                                  "(classify from the pinned "
                                  "aggregate) and are not appended "
                                  "to the JSONL; finalize "
                                  "reclassifies all 376,992 "
                                  "5-subsets and asserts the exact "
                                  "census and the presence of every "
                                  "b_only record; the full "
                                  "C(36,6) sextet census is "
                                  "reclassified and asserted "
                                  "all-zero (truncation "
                                  "justification)"),
            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
                             "sum j4 + sum j5 for k <= 36; "
                             "kill_A(k) = sum a - sum j2_A + "
                             "sum j3_A - sum j4_A (j5_A == 0); "
                             "kill_B(k) = sum b - sum j2_B + "
                             "sum j3_B - sum j4_B + sum j5_B; "
                             "j4_A comes from the 1,363 disjoint "
                             "quads (1,195 published at k=35, 168 "
                             "new at k=36), j5_B from the 17,434 "
                             "b_only quints (14,599 prev, 2,835 "
                             "new); the sixth order stays "
                             "structurally zero (sextet_census_k36)"),
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
            "marginal_k36": str(kill[K] - kill[K - 1]),
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


#!/usr/bin/env python3
"""Survival-curve extension to k=39 for the 31-row cost-16 parent
00000000000000003800000008001000.

rank-39 root (5,24) has no fresh row and no single-sharer row:
both rows arrive with exactly two prior sharers (row 5 via
index 2 = the rank-3 root (5,19) and index 25 = the rank-26 root
(5,16); row 24 via index 4 = the rank-5 root (18,24) and index
14 = the rank-15 root (15,24)), so both double for the first
time in the triple layer (54 and 46 records), the quad layer
(391 and 259 records) and the quint layer (763 and 179
records) -- the first generation whose double-row family gains
two rows at once.  The new pair census is 4 shared / 34
disjoint, the fewest shared of the post-fresh-row era (the
shared pairs are exactly the four prior sharers of rows 5 and
24: indices 2, 25, 4, 14).

STRUCTURAL BREAK AT k=39 (machine-verified from the pinned
aggregate and the k=39 preread JSON, commit 848727f1, before
writing any pm value):

  * the new quint layer contains 508 disjoint records (all
    with 10-row unions), the first disjoint quints ever
    (every C(k,5) census for k <= 38 was disjoint-zero);
    13,658 of the 73,815 new 5-subsets are b_only (all
    containing rank-39; double rows 18:6562 / 19:4267 /
    5:763 / 15:1561 / 24:179 / 23:10 / ...).  The full
    C(39,5)=575,757 census is 36,682 b_only / 538,567 zero /
    508 disjoint, extending the published k=38 census
    23,024/478,918/0 exactly;
  * the sextet layer turns non-zero for the first time: the
    full C(39,6)=3,262,623 census is 5,852 b_only (all
    containing the rank-39 root) / 3,256,771 zero / 0
    disjoint, breaking the k=26..k=38 all-zero sextet era.
    The level-7 closure of the k=39 preread (99,122-candidate
    monotone extension scan of the 5,852 b_only sextets, all
    zero) pins the truncation at level 6, so the marginal I-E
    gains a level-5 disjoint term and a level-6 b_only term:
      kill(k)   = sum m - sum j2 + sum j3 - sum j4 + sum j5
                  - sum j6
      kill_A(k) = sum a - sum j2_A + sum j3_A - sum j4_A
                  + sum j5_A                      (j6_A == 0)
      kill_B(k) = sum b - sum j2_B + sum j3_B - sum j4_B
                  + sum j5_B - sum j6_B
    with j5_A = disjoint_joint at |union|=10 on the 508 new
    disjoint quints (the same union-mask machinery as the
    disjoint pairs/triples/quads, re-anchored on 2 published
    k=38 disjoint quads at |union|=8 and cross-checked with
    both pm lineages before publication), j5_B = pm(V minus
    the union) on the residual for the b_only quints (the
    23,024 prev-era records load from the pinned k=26/k=27/
    k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/k=36/k=37/k=38
    publications; 13,658 new-era records are computed here) and
    j6_B = pm(V minus the union) on the residual for the 5,852
    new b_only sextets;
  * 1,009 new disjoint quads (|union|=8) extend the A-type
    4-way term to 2,686 total (1,677 published at k=38).

New-record census (machine-derived from the pinned aggregate,
independently re-derived by the k=39 preread (commit 848727f1,
pure Python with exact integer serialization) and asserted as
literals at load): 38 new pairs (4 shared / 34 disjoint), 703
new triples (319 b_only / 42 zero / 342 disjoint), 8,436 new
quads (4,398 b_only / 3,029 zero / 1,009 disjoint), 73,815 new
quints (13,658 b_only / 59,649 zero / 508 disjoint) and 501,942
new sextets (5,852 b_only / 496,090 zero / 0 disjoint).  Full
top-39 censuses prove C(39,3)=9,139 = 5,497/1,575/2,067,
C(39,4)=82,251, and the prev top-38 quint census must
reproduce the published k=38 values 23,024/478,918/0 exactly.
Every b_only record keeps its structure (b_only quint: three
b_only plus two disjoint 4-subsets; b_only sextet: four b_only
plus two disjoint 5-subsets); the disjoint quints have five
disjoint 4-subsets (machine-verified for all 508 here).
Zero quints and zero sextets are NOT appended to the JSONL;
finalize reclassifies all 575,757 5-subsets and all 3,262,623
6-subsets and asserts the exact censuses (zero records of the
triple/quad layers keep the k=38 house style and are
appended to the JSONL).

Preload style: the k=39 preread's structural fields are
asserted as literals at load (schema, check_count 35, root hex,
rows, prior hit indices, censuses, histograms, the disjoint
quint/sextet tallies, the level-7 closure), and its
big-integer fields
(membership/a_part/b_part = 119883868794265826 /
91824665662421012 / 28059203131844814) equal the pinned
aggregate exactly because the preread is pure Python with exact
integer serialization (no Node-era rounding erratum).

Anchors: kill/kill_A/kill_B for k=1..38 recomputed from the
assembled k=39 machinery must reproduce the pinned k=38
publication (commit 78b6f1bd) exactly.  Cross-checks: 2 new
disjoint triples and 2 new disjoint quads recomputed with the
second pm lineage, 2 new disjoint quints recomputed with both
pm lineages, 2 new b_only quads, 2 new b_only quints and 2 new
b_only sextets likewise.
R stays 31: the parent is the fixed 31-row cost-16 parent
(asserted at every get_parent call site); K=39 bans 39
pair roots drawn from it.

Cover-plan combinatorics only.  No engine run, no verdict.

Usage:
  python3 cost16_survival_k39_20261119.py pairs [BUDGET]
  python3 cost16_survival_k39_20261119.py triples [SLICE]
  python3 cost16_survival_k39_20261119.py quads [SLICE]
  python3 cost16_survival_k39_20261119.py quints [SLICE]
  python3 cost16_survival_k39_20261119.py sextets [SLICE]
  python3 cost16_survival_k39_20261119.py anchor
  python3 cost16_survival_k39_20261119.py cross
  python3 cost16_survival_k39_20261119.py finalize
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
K = 39
# R stays 31: the parent is the fixed 31-row cost-16 parent
# (len(P["target"]) == 31, asserted at every get_parent call
# site); K=39 bans 39 pair roots drawn from it.  A wrong R
# here would silently zero every b_only joint.
R = 31
IDX39 = 38

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
K36_JSON_REL = EXP_REL + "cost16-survival-k36-20261118.json"
K36_JSON_PIN = "b7a78e79bdc82c8097222ef2fd057e6b1a4b9350"
K36_JSON_COMMIT = "6fcea02c"
K37_JSON_REL = EXP_REL + "cost16-survival-k37-20261119.json"
K37_JSON_PIN = "03084d81674e829015561351be799c8a757e7c7e"
K37_JSON_COMMIT = "a4a7ce31"
K37_PREREAD_REL = EXP_REL + "cost16-survival-k37-preread-20261119.json"
K37_PREREAD_PIN = "b98ed685e772eacbd28dc3100e9813e81c27040a"
K37_PREREAD_COMMIT = "98321003"
K38_PREREAD_REL = EXP_REL + "cost16-survival-k38-preread-20261119.json"
K38_PREREAD_PIN = "3fa8297990d8e9880f386a0cfa075e3a95f226fd"
K38_PREREAD_COMMIT = "75fabfd0"
K38_JSON_REL = EXP_REL + "cost16-survival-k38-20261119.json"
K38_JSON_PIN = "c45ea8d0a11f009343c0736f6b98b5e4d06e8d4e"
K38_JSON_COMMIT = "78b6f1bd"
K39_PREREAD_REL = EXP_REL + "cost16-survival-k39-preread-20261119.json"
K39_PREREAD_PIN = "6056bd831d4ea32212f39016455078ff0557573c"
K39_PREREAD_COMMIT = "848727f192"
RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k39-20261119.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k39-20261119.json")

M39 = 119883868794265826


def load_top39():
    agg = json.loads(base.read_pinned(GROUPS_AGG_REL, GROUPS_AGG_PIN))
    top = agg["derived"]["top50_by_membership"][:K]
    assert all(e["kind"] == "pair" for e in top)
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]
    for e in top:
        assert memA[e["root"]] + memB[e["root"]] == e["membership"]
    # rank-39 root: (5,24), the first two-sharer/two-sharer root
    # (no fresh row and no single-sharer row: row 5 arrives via
    # prior sharers 2 = the rank-3 root (5,19) and 25 = the
    # rank-26 root (5,16); row 24 via 4 = the rank-5 root
    # (18,24) and 14 = the rank-15 root (15,24)), so both rows
    # double for the first time in the triple, quad and quint
    # layers (54/391/763 records for row 5 and 46/259/179 for
    # row 24) -- the first generation whose double-row family
    # gains two rows at once
    assert sorted(top[IDX39]["rows_covered"]) == [5, 24]
    assert top[IDX39]["root"] == "00000000000000889002000000100200"
    assert top[IDX39]["membership"] == M39
    # rank-38 regression anchor (published k=38 facts, commit
    # 78b6f1bd): the fourth single-share doubling root; row 29
    # has the single prior sharer index 19 among the top-37,
    # while row 19 is a twelve-sharer hub band row and gains
    # the rank-38 root itself as a sharer
    assert sorted(top[IDX39 - 1]["rows_covered"]) == [19, 29]
    assert top[IDX39 - 1]["root"] == \
        "00000008800000003800000008100000"
    assert top[IDX39 - 1]["membership"] == 119940649042609991
    assert [i for i in range(IDX39 - 1)
            if 19 in top[i]["rows_covered"]] == [0, 2, 3, 8, 9, 10,
                                                 15, 29, 32, 33, 35,
                                                 36]
    assert [i for i in range(IDX39 - 1)
            if 29 in top[i]["rows_covered"]] == [19]
    assert [i for i in range(IDX39)
            if 19 in top[i]["rows_covered"]] == [0, 2, 3, 8, 9, 10,
                                                 15, 29, 32, 33, 35,
                                                 36, 37]
    assert [i for i in range(IDX39)
            if 29 in top[i]["rows_covered"]] == [19, 37]
    # rows 5 and 24 have exactly the two listed prior sharers
    # each among the top-38 (row 5: index 2 = the rank-3 root
    # (5,19) and index 25 = the rank-26 root (5,16); row 24:
    # index 4 = the rank-5 root (18,24) and index 14 = the
    # rank-15 root (15,24)); the doublings of rows 5 and 24
    # start only with the rank-39 root in the member set
    assert [i for i in range(IDX39)
            if 5 in top[i]["rows_covered"]] == [2, 25]
    assert [i for i in range(IDX39)
            if 24 in top[i]["rows_covered"]] == [4, 14]
    total = agg["derived"]["total_minimum_covers"]
    A16 = agg["derived"]["type_A_disjoint"]
    B16 = agg["derived"]["type_B_one_duplicate_row"]
    # preread structural pins (commit 75fabfd0); the k=38
    # preread is pure Python with exact integer serialization
    # (like the k=32/k=33/k=34/k=35/k=36/k=37 prereads), so its
    # big-integer fields equal the pinned aggregate exactly
    # and need no erratum
    # preread structural pins (commit 848727f192); the k=39
    # preread is pure Python with exact integer serialization
    # (like the k=32/k=33/k=34/k=35/k=36/k=37/k=38 prereads),
    # so its big-integer fields equal the pinned aggregate
    # exactly and need no erratum
    pre = json.loads(base.read_pinned(K39_PREREAD_REL, K39_PREREAD_PIN))
    assert pre["schema"] == "n11-cost16-k39-preread-20261119-v1"
    assert pre["check_count"] == 35 and pre["all_pass"] is True
    r39 = pre["rank39"]
    assert r39["root"] == top[IDX39]["root"]
    assert r39["rows"] == [5, 24]
    assert r39["membership"] == M39
    assert r39["a_part"] == memA[top[IDX39]["root"]]
    assert r39["b_part"] == memB[top[IDX39]["root"]]
    assert memA[top[IDX39]["root"]] + memB[top[IDX39]["root"]] == M39
    assert r39["prior_hits"] == {"5": 2, "24": 2}
    assert r39["prior_hit_indices"]["5"] == [2, 25]
    assert r39["prior_hit_indices"]["24"] == [4, 14]
    # the pair layer reports shared/disjoint (same spelling as
    # the k=37/k=38 prereads); the regression layers below keep
    # the older b_only/zero pair spelling
    _pc = r39["new_census"]["pair"]
    assert _pc == {"shared": 4, "disjoint": 34, "total": 38,
                   "expected_total": 38}
    assert _pc["shared"] + _pc["disjoint"] == _pc["total"]
    assert _pc["total"] == _pc["expected_total"] == 38
    assert r39["new_census"]["triple"] == {"b_only": 319,
                                           "zero": 42,
                                           "disjoint": 342,
                                           "total": 703,
                                           "expected_total": 703}
    assert r39["new_census"]["quad"] == {"b_only": 4398,
                                         "zero": 3029,
                                         "disjoint": 1009,
                                         "total": 8436,
                                         "expected_total": 8436}
    assert r39["new_census"]["quint"] == {"b_only": 13658,
                                          "zero": 59649,
                                          "disjoint": 508,
                                          "total": 73815,
                                          "expected_total": 73815}
    assert r39["new_triple_double_row_histogram"] == {
        "0": 3, "1": 1, "4": 3, "5": 54, "7": 1, "8": 1, "9": 1,
        "11": 1, "14": 1, "15": 15, "16": 1, "18": 120, "19": 66,
        "23": 1, "24": 46, "29": 1, "30": 3}
    assert r39["new_quad_double_row_histogram"] == {
        "0": 60, "1": 6, "4": 32, "5": 391, "7": 6, "8": 6, "9": 6,
        "11": 6, "14": 6, "15": 333, "16": 15, "18": 1965,
        "19": 1257, "23": 12, "24": 259, "29": 6, "30": 32}
    assert r39["new_quint_double_row_histogram"] == {
        "0": 198, "1": 4, "4": 26, "5": 763, "7": 4, "8": 4, "9": 4,
        "11": 4, "14": 4, "15": 1561, "16": 38, "18": 6562,
        "19": 4267, "23": 10, "24": 179, "29": 4, "30": 26}
    assert r39["b_only_quint_four_subset_profiles"] == {
        "3/2/0": 13658}
    assert r39["disjoint_quad_count"] == 1009
    assert r39["disjoint_quad_union_sizes"] == {"8": 1009}
    assert r39["cumulative_disjoint_quads"] == 2686
    assert r39["disjoint_quint_count"] == 508
    assert r39["disjoint_quint_union_sizes"] == {"10": 508}
    assert r39["b_only_sextet_count"] == 5852
    assert r39["b_only_sextet_all_include_new_root"] is True
    assert r39["b_only_sextet_double_row_histogram"] == {
        "15": 682, "18": 3147, "19": 2023}
    assert r39["sextet_census"]["total"] == 3262623
    assert r39["sextet_census"]["counts"] == {"b_only": 5852,
                                              "zero": 3256771,
                                              "disjoint": 0}
    # level-7 closure of the k=39 preread: zero is upward closed
    # and disjoint sextets do not exist at k=39, so the
    # 99,122-candidate monotone extension scan over the 5,852
    # b_only sextets covers every possible non-zero 7-combo;
    # all zero, so the marginal I-E truncates at level 6
    assert r39["septet_zero_closure"][
        "non_zero_class_seven_combos"] == 0
    assert r39["septet_zero_closure"][
        "distinct_combos_checked"] == 99122
    assert r39["full_triples"]["counts"] == {"b_only": 5497,
                                             "zero": 1575,
                                             "disjoint": 2067}
    assert r39["full_triples"]["total"] == 9139
    assert r39["full_triples"]["compared"] == 9139
    assert r39["full_triples"]["mismatches"] == 0
    assert r39["full_quints"]["counts"] == {"b_only": 36682,
                                            "zero": 538567,
                                            "disjoint": 508}
    assert r39["full_quints"]["total"] == 575757
    assert r39["full_quints"]["double_row_histogram"] == {
        "0": 198, "1": 4, "4": 26, "5": 763, "7": 4, "8": 4, "9": 4,
        "11": 4, "14": 4, "15": 5024, "16": 725, "18": 17865,
        "19": 11838, "23": 10, "24": 179, "29": 4, "30": 26}
    # rank-38 regression layer of the k=39 preread (machine
    # re-derived from the same pinned aggregate against the
    # published k=38 preread, commit 75fabfd0); note the older
    # b_only/zero pair spelling here (b_only:13, zero:0)
    r38 = pre["rank38_regression"]
    assert r38["root"] == top[IDX39 - 1]["root"]
    assert r38["rows"] == [19, 29]
    assert r38["membership"] == 119940649042609991
    assert r38["a_part"] == memA[top[IDX39 - 1]["root"]]
    assert r38["b_part"] == memB[top[IDX39 - 1]["root"]]
    assert r38["prior_hits"] == {"19": 12, "29": 1}
    assert r38["prior_hit_indices"]["19"] == [0, 2, 3, 8, 9, 10,
                                              15, 29, 32, 33, 35,
                                              36]
    assert r38["prior_hit_indices"]["29"] == [19]
    assert r38["new_census"]["pair"] == {"b_only": 13, "zero": 0,
                                         "disjoint": 24, "total": 37,
                                         "expected_total": 37}
    assert r38["new_census"]["quint"] == {"b_only": 2868,
                                          "zero": 63177,
                                          "disjoint": 0,
                                          "total": 66045,
                                          "expected_total": 66045}
    assert r38["full_quints"]["counts"] == {"b_only": 23024,
                                            "zero": 478918,
                                            "disjoint": 0}
    assert r38["full_quints"]["total"] == 501942
    assert r38["sextet_census"]["total"] == 2760681
    assert r38["sextet_census"]["counts"] == {"b_only": 0,
                                              "zero": 2760681,
                                              "disjoint": 0}
    assert r38["mismatches"] == 0
    # rank-37 regression layer (light): still pinned against the
    # published k=37 preread facts (commit 98321003)
    r37 = pre["rank37_regression"]
    assert r37["root"] == "00000000080000003800000108001000"
    assert r37["rows"] == [8, 19]
    assert r37["membership"] == 119973409932394637
    assert r37["mismatches"] == 0
    return agg, top, memA, memB, total, A16, B16, pre


def load_k39_base():
    """703 pairwise joints, 8,436 triples, the 73,100 stored quads
    and the 23,024 b_only quints among the top-38, from the pinned
    k14..k36 publications plus the pinned k=37/k=38 results."""
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
    # k=36 era: 35 pairs, 595 triples, 6,545 quads (all classes
    # recorded, including the 168 disjoint quads with their A/B
    # split): cumulative stored 51,645 + 6,545 = 58,190 of the
    # C(36,4)=58,905 prev quads; the remaining 715 are the
    # k14-era hub-only quads, never stored and structurally zero.
    k36j = json.loads(base.read_pinned(K36_JSON_REL, K36_JSON_PIN))
    for key, v in k36j["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        assert 35 in (i, j) and 36 not in (i, j), (i, j)
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 630
    for key, v in k36j["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 35 in c and 36 not in c, c
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 7140
    for key, v in k36j["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 35 in c and 36 not in c, c
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 58190
    # k=37 era: 36 pairs, 630 triples, 7,140 quads (all classes
    # recorded, including the 157 disjoint quads with their A/B
    # split): cumulative stored 58,190 + 7,140 = 65,330 of the
    # C(37,4)=66,045 prev quads; the remaining 715 are the
    # k14-era hub-only quads, never stored and structurally zero.
    k37j = json.loads(base.read_pinned(K37_JSON_REL, K37_JSON_PIN))
    for key, v in k37j["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        assert 36 in (i, j) and 37 not in (i, j), (i, j)
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 666
    for key, v in k37j["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 36 in c and 37 not in c, c
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 7770
    for key, v in k37j["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 36 in c and 37 not in c, c
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 65330
    k38j = json.loads(base.read_pinned(K38_JSON_REL, K38_JSON_PIN))
    for key, v in k38j["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in key.split(","))
        assert 37 in (i, j) and 38 not in (i, j), (i, j)
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    assert len(pairs) == 703
    for key, v in k38j["values"]["new_triples"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 37 in c and 38 not in c, c
        triples[c] = {"class": v["class"], "joint": int(v["joint"]),
                      "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(triples) == 8436
    for key, v in k38j["values"]["new_quads"].items():
        c = tuple(int(x) for x in key.split(","))
        assert 37 in c and 38 not in c, c
        quads[c] = {"class": v["class"], "joint": int(v["joint"]),
                    "A": int(v["joint_A"]), "B": int(v["joint_B"])}
    assert len(quads) == 73100
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
    quints36 = {}
    for key, v in k36j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints36[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints36) == 2835
    assert all(35 in c and 36 not in c for c in quints36)
    quints37 = {}
    for key, v in k37j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints37[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints37) == 2722
    assert all(36 in c and 37 not in c for c in quints37)
    quints38 = {}
    for key, v in k38j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints38[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints38) == 2868
    assert all(37 in c and 38 not in c for c in quints38)
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
    quints_prev.update(quints36)
    quints_prev.update(quints37)
    quints_prev.update(quints38)
    assert len(quints_prev) == 23024
    return k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \
        k37j, k38j, pairs, triples, quads, quints_prev


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
    return [(i, IDX39) for i in range(IDX39)]


def new_triple_combos():
    return [(IDX39, i, j) for i, j in
            itertools.combinations(range(IDX39), 2)]


def new_quad_combos():
    return [(IDX39, i, j, l) for i, j, l in
            itertools.combinations(range(IDX39), 3)]


def new_quint_combos():
    return [(IDX39, i, j, l, m) for i, j, l, m in
            itertools.combinations(range(IDX39), 4)]


def new_sextet_combos():
    return [(IDX39, i, j, l, m, n) for i, j, l, m, n in
            itertools.combinations(range(IDX39), 5)]


def mode_pairs(budget):
    agg, top, memA, memB, total, A16, B16, pre = load_top39()
    P = k14m.get_parent()
    assert len(P["target"]) == R
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    base.STATE_CAP = 16_000_000
    base.BUDGET_SECONDS = budget
    pm = base.PmLazy(P["edge_w"], R)
    donep = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    todo = [c for c in new_pair_combos() if c not in donep]
    print("[pairs] todo %d (done %d/38)" % (len(todo), len(donep)),
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
    print("[pairs] done %d/38" % len(done("pair",
           lambda e: (e["idx_i"], e["idx_j"]))), flush=True)
    return 0


def mode_triples(slice_arg):
    agg, top, memA, memB, total, A16, B16, pre = load_top39()
    P = k14m.get_parent()
    assert len(P["target"]) == R
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_triple_combos()
    assert len(combos) == 703
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
    print("[triples] slice %d done, done %d/703 in %.1fs"
          % (slice_arg, len(done("triple", lambda e: tuple(e["combo"]))),
             time.time() - t00), flush=True)
    return 0


def mode_quads(slice_arg):
    agg, top, memA, memB, total, A16, B16, pre = load_top39()
    P = k14m.get_parent()
    assert len(P["target"]) == R
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_quad_combos()
    assert len(combos) == 8436
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
    print("[quads] slice %d done, done %d/8436"
          % (slice_arg, len(done("quad", lambda e: tuple(e["combo"])))),
          flush=True)
    return 0


def mode_quints(slice_arg):
    """5-way joints for the 73,815 new quints: 13,658 b_only
    (B-type residual count, MyPm) and 508 disjoint (A-type 5-way
    term at |union|=10 plus the two-case B-type term, the same
    union-mask machinery as the disjoint pairs/triples/quads,
    PmLazy).  The 23,024 prev-era b_only records load from the
    pinned k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/
    k=36/k=37/k=38 publications.  Zero quints are structural
    (classify from the pinned aggregate) and are synthesized in
    finalize, not appended here."""
    agg, top, memA, memB, total, A16, B16, pre = load_top39()
    P = k14m.get_parent()
    assert len(P["target"]) == R
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_quint_combos()
    assert len(combos) == 73815
    lo = slice_arg * 200
    hi = min(lo + 200, len(combos))
    done5 = done("quint", lambda e: tuple(e["combo"]))
    pm = None
    w1 = None
    t00 = time.time()
    for combo in combos[lo:hi]:
        if combo in done5:
            continue
        kind, union = classify(rows, combo)
        if kind == "zero":
            continue
        if kind == "disjoint":
            # disjoint quint (the first ever): A-type 5-way term
            # plus two-case B-type term, same union-mask machinery
            # as the disjoint pairs/triples/quads, now at
            # |union| = 10 (re-anchored in mode_anchor /
            # mode_cross)
            if pm is None:
                base.STATE_CAP = 16_000_000
                base.BUDGET_SECONDS = 900.0
                pm = base.PmLazy(P["edge_w"], R)
                w1 = k14m.w1_map(P)
            t0 = time.time()
            ja, jb = disjoint_joint(P["edge_w"], pm, w1, union)
            append({"kind": "quint", "combo": list(combo),
                    "class": "disjoint", "union": union,
                    "joint_A": ja, "joint_B": jb, "joint": ja + jb,
                    "memo_states": len(pm.memo),
                    "sec": round(time.time() - t0, 1)})
            print("[quint disjoint %s] union=%s A=%d B=%d memo=%d"
                  " %.1fs"
                  % (combo, union, ja, jb, len(pm.memo),
                     time.time() - t0), flush=True)
            if time.time() - t00 > 240:

#!/usr/bin/env python3
"""Anchored-rep transformation: k37 main script -> k38 main script.

Reads base/k37main.py (published k=37 main computation script, git
blob f30cde0f05160b994f727e766773af4818e1bada) and writes
cost16_survival_k38_20261119.py.  Mirrors the published k36->k37
transformation (patch_k37.py): pinned k=37 result JSON
(03084d81674e829015561351be799c8a757e7c7e, commit a4a7ce31) and
k=38 preread (3fa8297990d8e9880f386a0cfa075e3a95f226fd, commit
75fabfd0) join the pin set; load_top38 asserts the rank-38 root
(19,29) facts plus the rank-37/rank-36 regression layers of the
k=38 preread; load_k38_base appends the k=37 era records (666
pairs / 7,770 triples / 65,330 stored quads / 2,722 quints ->
quints_prev 20,156); finalize's censuses move to the C(38,3)=8,436
/ C(38,4)=73,815 / C(38,5)=501,942 / C(38,6)=2,760,681 values and
the reproduce band extends to kill(1..37) vs the pinned k=37
publication; the single-share structural check moves from row 8 to
row 29 (single prior sharer index 19 = the rank-20 root (18,29);
triple 8 records / quad 11 records / quint absent, the same pattern
as row 7 at k=33, row 9 at k=34 and row 8 at k=37).

Every replacement asserts exact occurrence counts, so a drifted
base file aborts before writing anything.
"""
import hashlib
import sys

SRC = "base/k37main.py"
DST = "cost16_survival_k38_20261119.py"
EXPECT_BASE_BLOB = "f30cde0f05160b994f727e766773af4818e1bada"

reps = []


def rep(old, new, count=1):
    reps.append((old, new, count))


def sub(src):
    for old, new, count in reps:
        got = src.count(old)
        if got != count:
            raise SystemExit(f"FAIL anchor x{got} != {count}: {old[:100]!r}")
        src = src.replace(old, new)
    return src


# ---- 1. module docstring ----
rep('''"""Survival-curve extension to k=37 for the 31-row cost-16 parent
00000000000000003800000008001000.

rank-37 root (8,19) has no fresh row: row 8 arrives with a single
prior sharer (index 23, the rank-24 root (8,18)), so it doubles
for the first time ever in the triple layer (8 records) and the
quad layer (11 records), never in the quint layer (the same
single-share doubling pattern as row 7 at rank-33 and row 9 at
rank-34), while row 19 becomes an eleven-sharer hub band row
(prior sharers 0,2,3,8,9,10,15,29,32,33,35 -- rank-36 itself is
a sharer).  The new pair census is 12 shared / 24 disjoint (the
shared pairs are exactly the one row-8 sharer plus the eleven
row-19 sharers).  The quint era opened at k=26 continues
(machine-verified from the pinned aggregate and the k=37 preread
JSON, commit 98321003, before writing any pm value):

  * 2,722 of the 58,905 new 5-subsets are structurally non-zero
    (all b_only, all containing rank-37; double rows 18:1043 /
    19:1269 / 15:339 / 16:71).  Row 8 never doubles in the quint
    layer (single prior sharer) and the quint double-row
    histogram stays within the four hub rows 15/16/18/19.  The
    full C(37,5)=435,897 census is 20,156 b_only / 415,741 zero
    / 0 disjoint, extending the published k=36 census
    17,434/359,558/0 exactly.  The full C(37,6)=2,324,784
    sextet census is all zero (finalize check below, extending
    the published k=26..k=36 sextet censuses), so the I-E keeps
    its fifth-order term with no sixth-order term:
      kill(k)   = sum m - sum j2 + sum j3 - sum j4 + sum j5
      kill_A(k) = sum a - sum j2_A + sum j3_A - sum j4_A  (j5_A == 0)
      kill_B(k) = sum b - sum j2_B + sum j3_B + sum j4_B + sum j5_B
    with j5_B = pm(V minus the union) on the residual, the b_only-quad
    pattern;  prev-era quint records (17,434 = 1,872 k26-era +
    309 k27-era + 331 k28-era + 2,128 k29-era + 1,328 k30-era +
    819 k31-era + 2,010 k32-era + 2,036 k33-era + 2,171 k34-era +
    1,595 k35-era + 2,835 k36-era) load from the pinned k=26/
    k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/k=36
    publications, new-era records (2,722) are computed here;
  * 157 new disjoint quads (|union|=8) extend the A-type 4-way
    term to 1,520 total.  disjoint_joint at |union|=8 was validated
    by the k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/k=36
    publications (anchor regression, both pm lineages, 1,363
    production records); this script re-anchors it on 2 published
    k=36 disjoint quads (both pm lineages, exact A/B match)
    before production.

New-record census (machine-derived from the pinned aggregate,
independently re-derived by the k=37 preread (commit 98321003,
pure Python with exact integer serialization) and asserted as
literals at load): 36 new pairs (12 shared / 24 disjoint), 630
new triples (397 b_only / 100 zero / 133 disjoint), 7,140 new
quads (2,394 b_only / 4,589 zero / 157 disjoint).  Full top-37
censuses prove C(37,3)=7,770 = 4,758/1,420/1,592, C(37,4)=66,045,
and the prev top-36 quint census must reproduce the published
k=36 values 17,434/359,558/0 exactly.  Every b_only quint keeps
the k=26 structure (three b_only plus two disjoint 4-subsets;
machine-verified for all 20,156 here).  Zero quints are NOT
appended to the JSONL; finalize reclassifies all 435,897
5-subsets and asserts the exact census.

Preload style: the k=37 preread's structural fields are
asserted as literals at load (schema, check_count 34, root hex,
rows, prior hit indices, censuses, histograms, disjoint quad
tally and the b_only-quint four-subset profile), and its
big-integer fields
(membership/a_part/b_part = 119973409932394637 /
91996175553485330 / 27977234378909307) equal the pinned
aggregate exactly because the preread is pure Python with exact
integer serialization (no Node-era rounding erratum).

Anchors: kill/kill_A/kill_B for k=1..36 recomputed from the
assembled k=37 machinery must reproduce the pinned k=36
publication (commit 6fcea02c) exactly.  Cross-checks: 2 new
disjoint triples and 2 new disjoint quads recomputed with the
second pm lineage, 2 new b_only quads and 2 new b_only quints
likewise.  R stays 31: the parent is the fixed 31-row cost-16
parent (asserted at every get_parent call site); K=37 bans 37
pair roots drawn from it.

Cover-plan combinatorics only.  No engine run, no verdict.

Usage:
  python3 cost16_survival_k37_20261119.py pairs [BUDGET]
  python3 cost16_survival_k37_20261119.py triples [SLICE]
  python3 cost16_survival_k37_20261119.py quads [SLICE]
  python3 cost16_survival_k37_20261119.py quints [SLICE]
  python3 cost16_survival_k37_20261119.py anchor
  python3 cost16_survival_k37_20261119.py cross
  python3 cost16_survival_k37_20261119.py finalize
"""''',
    '''"""Survival-curve extension to k=38 for the 31-row cost-16 parent
00000000000000003800000008001000.

rank-38 root (19,29) has no fresh row: row 29 arrives with a
single prior sharer (index 19, the rank-20 root (18,29)), so it
doubles for the first time ever in the triple layer (8 records)
and the quad layer (11 records), never in the quint layer (the
same single-share doubling pattern as row 7 at rank-33, row 9 at
rank-34 and row 8 at rank-37), while row 19 becomes a
twelve-sharer hub band row (prior sharers
0,2,3,8,9,10,15,29,32,33,35,36 -- rank-37 itself is a sharer).
The new pair census is 13 shared / 24 disjoint (the shared pairs
are exactly the twelve row-19 sharers plus the one row-29
sharer, index 19).  The quint era opened at k=26 continues
(machine-verified from the pinned aggregate and the k=38 preread
JSON, commit 75fabfd0, before writing any pm value):

  * 2,868 of the 66,045 new 5-subsets are structurally non-zero
    (all b_only, all containing rank-38; double rows 18:1043 /
    19:1415 / 15:339 / 16:71).  Row 29 never doubles in the quint
    layer (single prior sharer) and the quint double-row
    histogram stays within the four hub rows 15/16/18/19.  The
    full C(38,5)=501,942 census is 23,024 b_only / 478,918 zero
    / 0 disjoint, extending the published k=37 census
    20,156/415,741/0 exactly.  The full C(38,6)=2,760,681
    sextet census is all zero (finalize check below, extending
    the published k=26..k=37 sextet censuses), so the I-E keeps
    its fifth-order term with no sixth-order term:
      kill(k)   = sum m - sum j2 + sum j3 - sum j4 + sum j5
      kill_A(k) = sum a - sum j2_A + sum j3_A - sum j4_A  (j5_A == 0)
      kill_B(k) = sum b - sum j2_B + sum j3_B + sum j4_B + sum j5_B
    with j5_B = pm(V minus the union) on the residual, the b_only-quad
    pattern;  prev-era quint records (20,156 = 1,872 k26-era +
    309 k27-era + 331 k28-era + 2,128 k29-era + 1,328 k30-era +
    819 k31-era + 2,010 k32-era + 2,036 k33-era + 2,171 k34-era +
    1,595 k35-era + 2,835 k36-era + 2,722 k37-era) load from the
    pinned k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/
    k=36/k=37 publications, new-era records (2,868) are computed
    here;
  * 157 new disjoint quads (|union|=8) extend the A-type 4-way
    term to 1,677 total.  disjoint_joint at |union|=8 was validated
    by the k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/
    k=36/k=37 publications (anchor regression, both pm lineages,
    1,520 production records); this script re-anchors it on 2
    published k=37 disjoint quads (both pm lineages, exact A/B
    match) before production.

New-record census (machine-derived from the pinned aggregate,
independently re-derived by the k=38 preread (commit 75fabfd0,
pure Python with exact integer serialization) and asserted as
literals at load): 37 new pairs (13 shared / 24 disjoint), 666
new triples (420 b_only / 113 zero / 133 disjoint), 7,770 new
quads (2,519 b_only / 5,094 zero / 157 disjoint).  Full top-38
censuses prove C(38,3)=8,436 = 5,178/1,533/1,725,
C(38,4)=73,815, and the prev top-37 quint census must reproduce
the published k=37 values 20,156/415,741/0 exactly.  Every
b_only quint keeps the k=26 structure (three b_only plus two
disjoint 4-subsets; machine-verified for all 23,024 here).
Zero quints are NOT appended to the JSONL; finalize
reclassifies all 501,942 5-subsets and asserts the exact census.

Preload style: the k=38 preread's structural fields are
asserted as literals at load (schema, check_count 34, root hex,
rows, prior hit indices, censuses, histograms, disjoint quad
tally and the b_only-quint four-subset profile), and its
big-integer fields
(membership/a_part/b_part = 119940649042609991 /
91876760891572775 / 28063888151037216) equal the pinned
aggregate exactly because the preread is pure Python with exact
integer serialization (no Node-era rounding erratum).

Anchors: kill/kill_A/kill_B for k=1..37 recomputed from the
assembled k=38 machinery must reproduce the pinned k=37
publication (commit a4a7ce31) exactly.  Cross-checks: 2 new
disjoint triples and 2 new disjoint quads recomputed with the
second pm lineage, 2 new b_only quads and 2 new b_only quints
likewise.  R stays 31: the parent is the fixed 31-row cost-16
parent (asserted at every get_parent call site); K=38 bans 38
pair roots drawn from it.

Cover-plan combinatorics only.  No engine run, no verdict.

Usage:
  python3 cost16_survival_k38_20261119.py pairs [BUDGET]
  python3 cost16_survival_k38_20261119.py triples [SLICE]
  python3 cost16_survival_k38_20261119.py quads [SLICE]
  python3 cost16_survival_k38_20261119.py quints [SLICE]
  python3 cost16_survival_k38_20261119.py anchor
  python3 cost16_survival_k38_20261119.py cross
  python3 cost16_survival_k38_20261119.py finalize
"""''')

# ---- 2. constants and pins ----
rep('''K = 37''', '''K = 38''')
rep('''# (len(P["target"]) == 31, asserted at every get_parent call
# site); K=37 bans 37 pair roots drawn from it.  A wrong R
# here would silently zero every b_only joint.
R = 31
IDX37 = 36''',
    '''# (len(P["target"]) == 31, asserted at every get_parent call
# site); K=38 bans 38 pair roots drawn from it.  A wrong R
# here would silently zero every b_only joint.
R = 31
IDX38 = 37''')
rep('''K36_JSON_REL = EXP_REL + "cost16-survival-k36-20261118.json"
K36_JSON_PIN = "b7a78e79bdc82c8097222ef2fd057e6b1a4b9350"
K36_JSON_COMMIT = "6fcea02c"
K37_PREREAD_REL = EXP_REL + "cost16-survival-k37-preread-20261119.json"
K37_PREREAD_PIN = "b98ed685e772eacbd28dc3100e9813e81c27040a"
K37_PREREAD_COMMIT = "98321003"
RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k37-20261119.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k37-20261119.json")

M37 = 119973409932394637''',
    '''K36_JSON_REL = EXP_REL + "cost16-survival-k36-20261118.json"
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
RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k38-20261119.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k38-20261119.json")

M38 = 119940649042609991''')

# ---- 3. load_top37 -> load_top38 ----
rep("def load_top37():", "def load_top38():")
rep('''    # rank-37 root: (8,19), the first root ever to double row 8;
    # row 8 has a single prior sharer among the top-36 (index 23,
    # the rank-24 root (8,18)), so it doubles for the first time
    # in the triple layer (8 records) and the quad layer (11
    # records) but never in the quint layer (the same
    # single-share doubling pattern as row 7 at rank-33 and row 9
    # at rank-34), while row 19 is now an eleven-sharer hub band
    # row (prior sharers 0,2,3,8,9,10,15,29,32,33,35 -- rank-36
    # itself is a sharer; the rank-37 root joins the ten published
    # row-19 sharers)
    assert sorted(top[IDX37]["rows_covered"]) == [8, 19]
    assert top[IDX37]["root"] == "00000000080000003800000108001000"
    assert top[IDX37]["membership"] == M37
    # rank-36 regression anchor (published k=36 facts, commit
    # 6fcea02c): first root to cover row 22 (19,22); row 22 has
    # zero prior sharers, so it can never double in any layer,
    # while row 19 is a ten-sharer hub band row
    assert sorted(top[IDX37 - 1]["rows_covered"]) == [19, 22]
    assert top[IDX37 - 1]["root"] == \\
        "00000000000000801212020000001000"
    assert top[IDX37 - 1]["membership"] == 120046727515486665
    assert [i for i in range(IDX37 - 1)
            if 19 in top[i]["rows_covered"]] == [0, 2, 3, 8, 9, 10,
                                                 15, 29, 32, 33]
    assert [i for i in range(IDX37 - 1)
            if 22 in top[i]["rows_covered"]] == []
    assert [i for i in range(IDX37)
            if 19 in top[i]["rows_covered"]] == [0, 2, 3, 8, 9, 10,
                                                 15, 29, 32, 33, 35]
    assert [i for i in range(IDX37)
            if 22 in top[i]["rows_covered"]] == [35]
    # row 8 has exactly the one listed prior sharer among the
    # top-36 (index 23, the rank-24 root (8,18)); the doubling of
    # row 8 starts only with the rank-37 root in the member set
    assert [i for i in range(IDX37)
            if 8 in top[i]["rows_covered"]] == [23]''',
    '''    # rank-38 root: (19,29), the fourth single-sharer doubling
    # root; row 29 has a single prior sharer among the top-37
    # (index 19, the rank-20 root (18,29)), so it doubles for
    # the first time in the triple layer (8 records) and the
    # quad layer (11 records) but never in the quint layer (the
    # same single-share doubling pattern as row 7 at rank-33,
    # row 9 at rank-34 and row 8 at rank-37), while row 19 is
    # now a twelve-sharer hub band row (prior sharers
    # 0,2,3,8,9,10,15,29,32,33,35,36 -- rank-37 itself is a
    # sharer; the rank-38 root joins the eleven published
    # row-19 sharers)
    assert sorted(top[IDX38]["rows_covered"]) == [19, 29]
    assert top[IDX38]["root"] == "00000008800000003800000008100000"
    assert top[IDX38]["membership"] == M38
    # rank-37 regression anchor (published k=37 facts, commit
    # a4a7ce31): first root ever to double row 8 (8,19); row 8
    # has the single prior sharer index 23 among the top-36,
    # while row 19 is an eleven-sharer hub band row and gains
    # the rank-37 root itself as a sharer
    assert sorted(top[IDX38 - 1]["rows_covered"]) == [8, 19]
    assert top[IDX38 - 1]["root"] == \\
        "00000000080000003800000108001000"
    assert top[IDX38 - 1]["membership"] == 119973409932394637
    assert [i for i in range(IDX38 - 1)
            if 19 in top[i]["rows_covered"]] == [0, 2, 3, 8, 9, 10,
                                                 15, 29, 32, 33, 35]
    assert [i for i in range(IDX38 - 1)
            if 8 in top[i]["rows_covered"]] == [23]
    assert [i for i in range(IDX38)
            if 19 in top[i]["rows_covered"]] == [0, 2, 3, 8, 9, 10,
                                                 15, 29, 32, 33, 35,
                                                 36]
    assert [i for i in range(IDX38)
            if 8 in top[i]["rows_covered"]] == [23, 36]
    # row 29 has exactly the one listed prior sharer among the
    # top-37 (index 19, the rank-20 root (18,29)); the doubling
    # of row 29 starts only with the rank-38 root in the member
    # set
    assert [i for i in range(IDX38)
            if 29 in top[i]["rows_covered"]] == [19]''')
rep('''    # preread structural pins (commit 98321003); the k=37
    # preread is pure Python with exact integer serialization
    # (like the k=32/k=33/k=34/k=35/k=36 prereads), so its
    # big-integer fields equal the pinned aggregate exactly
    # and need no erratum
    pre = json.loads(base.read_pinned(K37_PREREAD_REL, K37_PREREAD_PIN))
    assert pre["schema"] == "n11-cost16-k37-preread-20261119-v1"
    assert pre["check_count"] == 34 and pre["all_pass"] is True
    r37 = pre["rank37"]
    assert r37["root"] == top[IDX37]["root"]
    assert r37["rows"] == [8, 19]
    assert r37["membership"] == M37
    assert r37["a_part"] == memA[top[IDX37]["root"]]
    assert r37["b_part"] == memB[top[IDX37]["root"]]
    assert memA[top[IDX37]["root"]] + memB[top[IDX37]["root"]] == M37
    assert r37["prior_hits"] == {"8": 1, "19": 11}
    assert r37["prior_hit_indices"]["8"] == [23]
    assert r37["prior_hit_indices"]["19"] == [0, 2, 3, 8, 9, 10,
                                              15, 29, 32, 33, 35]
    # the pair layer reports shared/disjoint (same spelling as
    # the rank-36 body of the k=36 preread); the regression
    # layers below keep the older b_only/zero pair spelling
    _pc = r37["new_census"]["pair"]
    assert _pc == {"shared": 12, "disjoint": 24, "total": 36,
                   "expected_total": 36}
    assert _pc["shared"] + _pc["disjoint"] == _pc["total"]
    assert _pc["total"] == _pc["expected_total"] == 36
    assert r37["new_census"]["triple"] == {"b_only": 397, "zero": 100,
                                           "disjoint": 133,
                                           "total": 630,
                                           "expected_total": 630}
    assert r37["new_census"]["quad"] == {"b_only": 2394,
                                         "zero": 4589,
                                         "disjoint": 157,
                                         "total": 7140,
                                         "expected_total": 7140}
    assert r37["new_census"]["quint"] == {"b_only": 2722,
                                          "zero": 56183,
                                          "disjoint": 0,
                                          "total": 58905,
                                          "expected_total": 58905}
    assert r37["new_triple_double_row_histogram"] == {
        "0": 1, "4": 1, "8": 8, "15": 15, "16": 3,
        "18": 120, "19": 246, "23": 1, "24": 1, "30": 1}
    assert r37["new_quad_double_row_histogram"] == {
        "0": 15, "4": 2, "8": 11, "15": 245, "16": 31,
        "18": 870, "19": 1214, "23": 2, "24": 2, "30": 2}
    assert r37["new_quint_double_row_histogram"] == {
        "15": 339, "16": 71, "18": 1043, "19": 1269}
    assert r37["b_only_quint_four_subset_profiles"] == {
        "3/2/0": 2722}
    assert r37["disjoint_quad_count"] == 157
    assert r37["disjoint_quad_union_sizes"] == {"8": 157}
    assert r37["cumulative_disjoint_quads"] == 1520
    assert r37["full_triples"]["counts"] == {"b_only": 4758,
                                             "zero": 1420,
                                             "disjoint": 1592}
    assert r37["full_triples"]["total"] == 7770
    assert r37["full_triples"]["compared"] == 7770
    assert r37["full_triples"]["mismatches"] == 0
    assert r37["full_quints"]["counts"] == {"b_only": 20156,
                                            "zero": 415741,
                                            "disjoint": 0}
    assert r37["full_quints"]["total"] == 435897
    assert r37["full_quints"]["double_row_histogram"] == {
        "15": 3124, "16": 616, "18": 10260, "19": 6156}
    assert r37["sextet_census"]["total"] == 2324784
    assert r37["sextet_census"]["counts"] == {"b_only": 0,
                                              "zero": 2324784,
                                              "disjoint": 0}''',
    '''    # preread structural pins (commit 75fabfd0); the k=38
    # preread is pure Python with exact integer serialization
    # (like the k=32/k=33/k=34/k=35/k=36/k=37 prereads), so its
    # big-integer fields equal the pinned aggregate exactly
    # and need no erratum
    pre = json.loads(base.read_pinned(K38_PREREAD_REL, K38_PREREAD_PIN))
    assert pre["schema"] == "n11-cost16-k38-preread-20261119-v1"
    assert pre["check_count"] == 34 and pre["all_pass"] is True
    r38 = pre["rank38"]
    assert r38["root"] == top[IDX38]["root"]
    assert r38["rows"] == [19, 29]
    assert r38["membership"] == M38
    assert r38["a_part"] == memA[top[IDX38]["root"]]
    assert r38["b_part"] == memB[top[IDX38]["root"]]
    assert memA[top[IDX38]["root"]] + memB[top[IDX38]["root"]] == M38
    assert r38["prior_hits"] == {"19": 12, "29": 1}
    assert r38["prior_hit_indices"]["19"] == [0, 2, 3, 8, 9, 10,
                                              15, 29, 32, 33, 35, 36]
    assert r38["prior_hit_indices"]["29"] == [19]
    # the pair layer reports shared/disjoint (same spelling as
    # the k=37 preread); the regression layers below keep the
    # older b_only/zero pair spelling
    _pc = r38["new_census"]["pair"]
    assert _pc == {"shared": 13, "disjoint": 24, "total": 37,
                   "expected_total": 37}
    assert _pc["shared"] + _pc["disjoint"] == _pc["total"]
    assert _pc["total"] == _pc["expected_total"] == 37
    assert r38["new_census"]["triple"] == {"b_only": 420, "zero": 113,
                                           "disjoint": 133,
                                           "total": 666,
                                           "expected_total": 666}
    assert r38["new_census"]["quad"] == {"b_only": 2519,
                                         "zero": 5094,
                                         "disjoint": 157,
                                         "total": 7770,
                                         "expected_total": 7770}
    assert r38["new_census"]["quint"] == {"b_only": 2868,
                                          "zero": 63177,
                                          "disjoint": 0,
                                          "total": 66045,
                                          "expected_total": 66045}
    assert r38["new_triple_double_row_histogram"] == {
        "0": 1, "4": 1, "15": 15, "16": 3,
        "18": 120, "19": 269, "23": 1, "24": 1, "29": 8, "30": 1}
    assert r38["new_quad_double_row_histogram"] == {
        "0": 15, "4": 2, "15": 245, "16": 31,
        "18": 870, "19": 1339, "23": 2, "24": 2, "29": 11, "30": 2}
    assert r38["new_quint_double_row_histogram"] == {
        "15": 339, "16": 71, "18": 1043, "19": 1415}
    assert r38["b_only_quint_four_subset_profiles"] == {
        "3/2/0": 2868}
    assert r38["disjoint_quad_count"] == 157
    assert r38["disjoint_quad_union_sizes"] == {"8": 157}
    assert r38["cumulative_disjoint_quads"] == 1677
    assert r38["full_triples"]["counts"] == {"b_only": 5178,
                                             "zero": 1533,
                                             "disjoint": 1725}
    assert r38["full_triples"]["total"] == 8436
    assert r38["full_triples"]["compared"] == 8436
    assert r38["full_triples"]["mismatches"] == 0
    assert r38["full_quints"]["counts"] == {"b_only": 23024,
                                            "zero": 478918,
                                            "disjoint": 0}
    assert r38["full_quints"]["total"] == 501942
    assert r38["full_quints"]["double_row_histogram"] == {
        "15": 3463, "16": 687, "18": 11303, "19": 7571}
    assert r38["sextet_census"]["total"] == 2760681
    assert r38["sextet_census"]["counts"] == {"b_only": 0,
                                              "zero": 2760681,
                                              "disjoint": 0}''')
rep('''    # rank-36 regression layer of the k=37 preread (machine
    # re-derived from the same pinned aggregate against the
    # published k=36 preread, commit 67985e92c9); note the older
    # b_only/zero pair spelling here (b_only:10, zero:0), and
    # that this layer has no disjoint_quad_count key
    r36 = pre["rank36_regression"]
    assert r36["root"] == top[IDX37 - 1]["root"]
    assert r36["rows"] == [19, 22]
    assert r36["membership"] == 120046727515486665
    assert r36["a_part"] == memA[top[IDX37 - 1]["root"]]
    assert r36["b_part"] == memB[top[IDX37 - 1]["root"]]
    assert r36["prior_hits"] == {"19": 10, "22": 0}
    assert r36["prior_hit_indices"]["19"] == [0, 2, 3, 8, 9, 10,
                                              15, 29, 32, 33]
    assert r36["prior_hit_indices"]["22"] == []
    assert r36["new_census"]["pair"] == {"b_only": 10, "zero": 0,
                                         "disjoint": 25, "total": 35,
                                         "expected_total": 35}
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
    assert r36["full_triples"]["counts"] == {"b_only": 4361,
                                             "zero": 1320,
                                             "disjoint": 1459}
    assert r36["full_triples"]["total"] == 7140
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
    assert r36["mismatches"] == 0
    # rank-35 regression layer (light): still pinned against the
    # published k=35 preread facts (commit 90fc51c991)
    r35 = pre["rank35_regression"]
    assert r35["root"] == "00000000000000801202090000001000"
    assert r35["rows"] == [18, 21]
    assert r35["membership"] == 120058481266728720
    assert r35["a_part"] == 92036253749417268
    assert r35["b_part"] == 28022227517311452
    assert r35["mismatches"] == 0''',
    '''    # rank-37 regression layer of the k=38 preread (machine
    # re-derived from the same pinned aggregate against the
    # published k=37 preread, commit 98321003); note the older
    # b_only/zero pair spelling here (b_only:12, zero:0), and
    # that this layer has no disjoint_quad_count key
    r37 = pre["rank37_regression"]
    assert r37["root"] == top[IDX38 - 1]["root"]
    assert r37["rows"] == [8, 19]
    assert r37["membership"] == 119973409932394637
    assert r37["a_part"] == memA[top[IDX38 - 1]["root"]]
    assert r37["b_part"] == memB[top[IDX38 - 1]["root"]]
    assert r37["prior_hits"] == {"8": 1, "19": 11}
    assert r37["prior_hit_indices"]["8"] == [23]
    assert r37["prior_hit_indices"]["19"] == [0, 2, 3, 8, 9, 10,
                                              15, 29, 32, 33, 35]
    assert r37["new_census"]["pair"] == {"b_only": 12, "zero": 0,
                                         "disjoint": 24, "total": 36,
                                         "expected_total": 36}
    assert r37["new_census"]["triple"] == {"b_only": 397, "zero": 100,
                                           "disjoint": 133,
                                           "total": 630,
                                           "expected_total": 630}
    assert r37["new_census"]["quad"] == {"b_only": 2394,
                                         "zero": 4589,
                                         "disjoint": 157,
                                         "total": 7140,
                                         "expected_total": 7140}
    assert r37["new_census"]["quint"] == {"b_only": 2722,
                                          "zero": 56183,
                                          "disjoint": 0,
                                          "total": 58905,
                                          "expected_total": 58905}
    assert r37["new_triple_double_row_histogram"] == {
        "0": 1, "4": 1, "8": 8, "15": 15, "16": 3,
        "18": 120, "19": 246, "23": 1, "24": 1, "30": 1}
    assert r37["new_quad_double_row_histogram"] == {
        "0": 15, "4": 2, "8": 11, "15": 245, "16": 31,
        "18": 870, "19": 1214, "23": 2, "24": 2, "30": 2}
    assert r37["new_quint_double_row_histogram"] == {
        "15": 339, "16": 71, "18": 1043, "19": 1269}
    assert r37["b_only_quint_four_subset_profiles"] == {
        "3/2/0": 2722}
    assert r37["full_triples"]["counts"] == {"b_only": 4758,
                                             "zero": 1420,
                                             "disjoint": 1592}
    assert r37["full_triples"]["total"] == 7770
    assert r37["full_quints"]["counts"] == {"b_only": 20156,
                                            "zero": 415741,
                                            "disjoint": 0}
    assert r37["full_quints"]["total"] == 435897
    assert r37["full_quints"]["double_row_histogram"] == {
        "15": 3124, "16": 616, "18": 10260, "19": 6156}
    assert r37["sextet_census"]["total"] == 2324784
    assert r37["sextet_census"]["counts"] == {"b_only": 0,
                                              "zero": 2324784,
                                              "disjoint": 0}
    assert r37["mismatches"] == 0
    # rank-36 regression layer (light): still pinned against the
    # published k=36 preread facts (commit 67985e92c9)
    r36 = pre["rank36_regression"]
    assert r36["root"] == "00000000000000801212020000001000"
    assert r36["rows"] == [19, 22]
    assert r36["membership"] == 120046727515486665
    assert r36["a_part"] == 92003630985566871
    assert r36["b_part"] == 28043096529919794
    assert r36["mismatches"] == 0''')

# ---- 4. load_k37_base -> load_k38_base ----
rep('''def load_k37_base():
    """630 pairwise joints, 7,140 triples, the 58,190 stored quads
    and the 17,434 b_only quints among the top-36, from the pinned
    k14..k35 publications plus the pinned k=36 result."""''',
    '''def load_k38_base():
    """666 pairwise joints, 7,770 triples, the 65,330 stored quads
    and the 20,156 b_only quints among the top-37, from the pinned
    k14..k36 publications plus the pinned k=37 result."""''')
rep('''    # k=36 era: 35 pairs, 595 triples, 6,545 quads (all classes
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
    quints26 = {}''',
    '''    # k=36 era: 35 pairs, 595 triples, 6,545 quads (all classes
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
    quints26 = {}''')
rep('''    quints36 = {}
    for key, v in k36j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints36[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints36) == 2835
    assert all(35 in c and 36 not in c for c in quints36)
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
    assert len(quints_prev) == 17434
    return k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, \\
        k24, k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \\
        pairs, triples, quads, quints_prev''',
    '''    quints36 = {}
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
    assert len(quints_prev) == 20156
    return k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, \\
        k24, k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \\
        k37j, pairs, triples, quads, quints_prev''')

# ---- 5. load_top37 callers (global renames) ----
rep("load_top37()", "load_top38()", 7)
rep("IDX37", "IDX38", 18)

# ---- 6. mode pairing literals ----
rep('''    print("[pairs] todo %d (done %d/36)" % (len(todo), len(donep)),
          flush=True)''',
    '''    print("[pairs] todo %d (done %d/37)" % (len(todo), len(donep)),
          flush=True)''')
rep('''    print("[pairs] done %d/36" % len(done("pair",
           lambda e: (e["idx_i"], e["idx_j"]))), flush=True)''',
    '''    print("[pairs] done %d/37" % len(done("pair",
           lambda e: (e["idx_i"], e["idx_j"]))), flush=True)''')
rep('''def mode_triples(slice_arg):''', '''def mode_triples(slice_arg):''')
rep('''    combos = new_triple_combos()
    assert len(combos) == 630''',
    '''    combos = new_triple_combos()
    assert len(combos) == 666''')
rep('''    print("[triples] slice %d done, done %d/630 in %.1fs"''',
    '''    print("[triples] slice %d done, done %d/666 in %.1fs"''')
rep('''    combos = new_quad_combos()
    assert len(combos) == 7140''',
    '''    combos = new_quad_combos()
    assert len(combos) == 7770''')
rep('''    print("[quads] slice %d done, done %d/7140"''',
    '''    print("[quads] slice %d done, done %d/7770"''')
rep('''    (the 17,434 prev-era records load from the pinned
    k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/k=36
    JSONs).  Zero''',
    '''    (the 20,156 prev-era records load from the pinned
    k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/k=36/k=37
    JSONs).  Zero''')
rep('''    """B-type-only 5-way joints for the 2,722 new b_only quints''',
    '''    """B-type-only 5-way joints for the 2,868 new b_only quints''')
    # (the quint-era TODO count changes from 58,905 to 66,045:
    #  C(37,4) prev quads were 66,045; the new k=38 combos are
    #  the 5-subsets containing rank-38 = C(37,4) = 66,045)
rep('''    combos = new_quint_combos()
    assert len(combos) == 58905''',
    '''    combos = new_quint_combos()
    assert len(combos) == 66045''')
rep('''    print("[quints] slice %d done, done %d/2722b_only in %.1fs"''',
    '''    print("[quints] slice %d done, done %d/2868b_only in %.1fs"''')

# ---- 7. mode_anchor: re-anchor on the k=37 publication ----
rep('''    """Pre-production validation of disjoint_joint at |union|=4
    (published k13-era pair joints, both pm lineages), |union|=6
    (2 published k36 disjoint triples) and |union|=8 (2 published
    k36 disjoint quads, both pm lineages with exact A/B match
    against the pinned publication).  The |union|=8 machinery was
    introduced at k=26 and extended by the k=27/k=28/k=29/k=30/
    k=31/k=32/k=33/k=34/k=35/k=36 publications (1,363 production
    records); this re-anchors it on published records before
    production."""''',
    '''    """Pre-production validation of disjoint_joint at |union|=4
    (published k13-era pair joints, both pm lineages), |union|=6
    (2 published k37 disjoint triples) and |union|=8 (2 published
    k37 disjoint quads, both pm lineages with exact A/B match
    against the pinned publication).  The |union|=8 machinery was
    introduced at k=26 and extended by the k=27/k=28/k=29/k=30/
    k=31/k=32/k=33/k=34/k=35/k=36/k=37 publications (1,520
    production records); this re-anchors it on published records
    before production."""''')
rep('''    k36ja = json.loads(base.read_pinned(K36_JSON_REL, K36_JSON_PIN))
    pub3 = [tuple(int(x) for x in key.split(","))
            for key, v in k36ja["values"]["new_triples"].items()
            if v["class"] == "disjoint"]
    pub3.sort()
    assert len(pub3) >= 2
    for combo in pub3[:2]:
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        ref = k36ja["values"]["new_triples"]["%d,%d,%d" % combo]''',
    '''    k37ja = json.loads(base.read_pinned(K37_JSON_REL, K37_JSON_PIN))
    pub3 = [tuple(int(x) for x in key.split(","))
            for key, v in k37ja["values"]["new_triples"].items()
            if v["class"] == "disjoint"]
    pub3.sort()
    assert len(pub3) >= 2
    for combo in pub3[:2]:
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        ref = k37ja["values"]["new_triples"]["%d,%d,%d" % combo]''')
rep('''    pub4 = [tuple(int(x) for x in key.split(","))
            for key, v in k36ja["values"]["new_quads"].items()
            if v["class"] == "disjoint"]
    pub4.sort()
    assert len(pub4) >= 2
    for combo in pub4[:2]:
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        ref = k36ja["values"]["new_quads"]["%d,%d,%d,%d" % combo]''',
    '''    pub4 = [tuple(int(x) for x in key.split(","))
            for key, v in k37ja["values"]["new_quads"].items()
            if v["class"] == "disjoint"]
    pub4.sort()
    assert len(pub4) >= 2
    for combo in pub4[:2]:
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        ref = k37ja["values"]["new_quads"]["%d,%d,%d,%d" % combo]''')

# ---- 8. finalize: load unpack ----
rep('''    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \\
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \\
        pairs_prev, triples_prev, quads_prev, quints_prev \\
        = load_k37_base()''',
    '''    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \\
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \\
        k37j, pairs_prev, triples_prev, quads_prev, quints_prev \\
        = load_k38_base()''')

# ---- 9. finalize: pairs ----
rep('''    # ---- pairs (630 + 36 = 666)
    j2 = dict(pairs_prev)
    chk("pairs.prev_630", len(pairs_prev) == 630)
    chk("pairs.new_36", len(donep) == 36)''',
    '''    # ---- pairs (666 + 37 = 703)
    j2 = dict(pairs_prev)
    chk("pairs.prev_666", len(pairs_prev) == 666)
    chk("pairs.new_37", len(donep) == 37)''')
rep('''    chk("pairs.complete_666", len(j2) == 666)''',
    '''    chk("pairs.complete_703", len(j2) == 703)''')
rep('''    chk("pairs.new_census",
        len(shared_new) == 12 and len(donep) - len(shared_new) == 24,''',
    '''    chk("pairs.new_census",
        len(shared_new) == 13 and len(donep) - len(shared_new) == 24,''')

# ---- 10. finalize: triples ----
rep('''    # ---- triples (7140 + 630 = 7770)''',
    '''    # ---- triples (7770 + 666 = 8436)''')
rep('''    chk("triples.prev_7140", len(j3) == 7140)
    chk("triples.new_630", len(donet) == 630)''',
    '''    chk("triples.prev_7770", len(j3) == 7770)
    chk("triples.new_666", len(donet) == 666)''')
rep('''    chk("triples.complete_7770", len(j3) == 7770)''',
    '''    chk("triples.complete_8436", len(j3) == 8436)''')
rep('''    chk("triples.census",
        cen == {"b_only": 4758, "zero": 1420, "disjoint": 1592}, cen)
    chk("preread_match.triple_census", cen == {
        "b_only": pre["rank37"]["full_triples"]["counts"]["b_only"],
        "zero": pre["rank37"]["full_triples"]["counts"]["zero"],
        "disjoint":
            pre["rank37"]["full_triples"]["counts"]["disjoint"]})''',
    '''    chk("triples.census",
        cen == {"b_only": 5178, "zero": 1533, "disjoint": 1725}, cen)
    chk("preread_match.triple_census", cen == {
        "b_only": pre["rank38"]["full_triples"]["counts"]["b_only"],
        "zero": pre["rank38"]["full_triples"]["counts"]["zero"],
        "disjoint":
            pre["rank38"]["full_triples"]["counts"]["disjoint"]})''')

# ---- 11. finalize: quads ----
rep('''    # ---- quads (58905 prev + 7140 new = 66045)''',
    '''    # ---- quads (66045 prev + 7770 new = 73815)''')
rep('''    chk("quads.prev_58905_stored_58190",
        len(j4) == 58905 and len(quads_prev) == 58190,''',
    '''    chk("quads.prev_66045_stored_65330",
        len(j4) == 66045 and len(quads_prev) == 65330,''')
rep('''    chk("quads.new_7140", len(doneq) == 7140)''',
    '''    chk("quads.new_7770", len(doneq) == 7770)''')
rep('''    chk("quads.complete_66045", len(j4) == 66045)''',
    '''    chk("quads.complete_73815", len(j4) == 73815)''')
rep('''    chk("quads.new_census",
        qcen == {"b_only": 2394, "zero": 4589, "disjoint": 157},
        qcen)
    chk("preread_match.new_quad_census", qcen == {
        "b_only": pre["rank37"]["new_census"]["quad"]["b_only"],
        "zero": pre["rank37"]["new_census"]["quad"]["zero"],
        "disjoint": pre["rank37"]["new_census"]["quad"]["disjoint"]})''',
    '''    chk("quads.new_census",
        qcen == {"b_only": 2519, "zero": 5094, "disjoint": 157},
        qcen)
    chk("preread_match.new_quad_census", qcen == {
        "b_only": pre["rank38"]["new_census"]["quad"]["b_only"],
        "zero": pre["rank38"]["new_census"]["quad"]["zero"],
        "disjoint": pre["rank38"]["new_census"]["quad"]["disjoint"]})''')
rep('''    chk("quads.prev_disjoint_1363", len(prev_disjoint) == 1363)''',
    '''    chk("quads.prev_disjoint_1520", len(prev_disjoint) == 1520)''')
rep('''    # new b_only quads double-row histogram (machine-derived;
    # row 8 doubles here for the first time in the quad layer
    # (11 records; single prior sharer index 23 -- the same
    # single-share doubling pattern as row 7 at rank-33 and row
    # 9 at rank-34), while row 19 is the dominant new double
    # row (1,214 of the 2,394 new b_only quads)); the b_only
    # triple double-row histogram is recorded as a computed
    # fact too''',
    '''    # new b_only quads double-row histogram (machine-derived;
    # row 29 doubles here for the first time in the quad layer
    # (11 records; single prior sharer index 19 -- the same
    # single-share doubling pattern as row 7 at rank-33, row 9
    # at rank-34 and row 8 at rank-37), while row 19 is the
    # dominant new double row (1,339 of the 2,519 new b_only
    # quads)); the b_only triple double-row histogram is
    # recorded as a computed fact too''')
rep('''    chk("triples.new_b_only_double_rows",
        triple_dbl_hist == {0: 1, 4: 1, 8: 8, 15: 15, 16: 3,
                            18: 120, 19: 246, 23: 1, 24: 1, 30: 1},
        triple_dbl_hist)''',
    '''    chk("triples.new_b_only_double_rows",
        triple_dbl_hist == {0: 1, 4: 1, 15: 15, 16: 3,
                            18: 120, 19: 269, 23: 1, 24: 1, 29: 8,
                            30: 1},
        triple_dbl_hist)''')
rep('''    chk("quads.new_b_only_double_row_8_first_quad_doubling",
        quad_dbl_hist.get(8, 0) == 11, quad_dbl_hist)
    chk("quads.new_b_only_double_rows",
        quad_dbl_hist == {0: 15, 4: 2, 8: 11, 15: 245, 16: 31,
                          18: 870, 19: 1214, 23: 2, 24: 2, 30: 2},
        quad_dbl_hist)''',
    '''    chk("quads.new_b_only_double_row_29_first_quad_doubling",
        quad_dbl_hist.get(29, 0) == 11, quad_dbl_hist)
    chk("quads.new_b_only_double_rows",
        quad_dbl_hist == {0: 15, 4: 2, 15: 245, 16: 31,
                          18: 870, 19: 1339, 23: 2, 24: 2, 29: 11,
                          30: 2},
        quad_dbl_hist)''')

# ---- 12. finalize: quints ----
rep('''    # ---- quints (359,558 top-36 zeros + 17,434 prev b_only +
    #      56,183 new zeros + 2,722 new b_only = 435,897)''',
    '''    # ---- quints (415,741 top-37 zeros + 20,156 prev b_only +
    #      63,177 new zeros + 2,868 new b_only = 501,942)''')
rep('''    chk("quints.census_435897",
        n5 == 435897 and cen5 == {"b_only": 20156, "zero": 415741,
                                  "disjoint": 0},
        {"census": cen5, "double_rows": dbl_hist})
    chk("quints.double_rows_hist",
        dbl_hist == {15: 3124, 16: 616, 18: 10260, 19: 6156},
        dbl_hist)
    chk("preread_match.quint_census", cen5 == {
        "b_only": pre["rank37"]["full_quints"]["counts"]["b_only"],
        "zero": pre["rank37"]["full_quints"]["counts"]["zero"],
        "disjoint": pre["rank37"]["full_quints"]["counts"]["disjoint"]})
    chk("preread_match.quint_double_rows", dbl_hist == {
        int(r): v for r, v in
        pre["rank37"]["full_quints"]["double_row_histogram"].items()})''',
    '''    chk("quints.census_501942",
        n5 == 501942 and cen5 == {"b_only": 23024, "zero": 478918,
                                  "disjoint": 0},
        {"census": cen5, "double_rows": dbl_hist})
    chk("quints.double_rows_hist",
        dbl_hist == {15: 3463, 16: 687, 18: 11303, 19: 7571},
        dbl_hist)
    chk("preread_match.quint_census", cen5 == {
        "b_only": pre["rank38"]["full_quints"]["counts"]["b_only"],
        "zero": pre["rank38"]["full_quints"]["counts"]["zero"],
        "disjoint": pre["rank38"]["full_quints"]["counts"]["disjoint"]})
    chk("preread_match.quint_double_rows", dbl_hist == {
        int(r): v for r, v in
        pre["rank38"]["full_quints"]["double_row_histogram"].items()})''')
rep('''    chk("quints.prev_census_matches_k36",
        prev_cen5 == {"b_only": 17434, "zero": 359558,
                     "disjoint": 0},
        prev_cen5)
    chk("quints.new_records_2722", len(done5) == 2722)''',
    '''    chk("quints.prev_census_matches_k37",
        prev_cen5 == {"b_only": 20156, "zero": 415741,
                     "disjoint": 0},
        prev_cen5)
    chk("quints.new_records_2868", len(done5) == 2868)''')
rep('''    chk("quints.new_b_only_contain_rank37", all(
        IDX38 in c for c in j5
        if j5[c]["class"] == "b_only" and 25 not in c
        and 26 not in c and 27 not in c and 28 not in c
        and 29 not in c and 30 not in c and 31 not in c
        and 32 not in c and 33 not in c and 34 not in c
        and 35 not in c))
    chk("quints.prev_b_only_contain_rank26_through_36", all(
        (25 in c) or (26 in c) or (27 in c) or (28 in c)
        or (29 in c) or (30 in c) or (31 in c) or (32 in c)
        or (33 in c) or (34 in c) or (35 in c)
        for c in j5
        if j5[c]["class"] == "b_only" and IDX38 not in c))''',
    '''    chk("quints.new_b_only_contain_rank38", all(
        IDX38 in c for c in j5
        if j5[c]["class"] == "b_only" and 25 not in c
        and 26 not in c and 27 not in c and 28 not in c
        and 29 not in c and 30 not in c and 31 not in c
        and 32 not in c and 33 not in c and 34 not in c
        and 35 not in c and 36 not in c))
    chk("quints.prev_b_only_contain_rank26_through_37", all(
        (25 in c) or (26 in c) or (27 in c) or (28 in c)
        or (29 in c) or (30 in c) or (31 in c) or (32 in c)
        or (33 in c) or (34 in c) or (35 in c) or (36 in c)
        for c in j5
        if j5[c]["class"] == "b_only" and IDX38 not in c))''')
rep('''    # new-era b_only quints never double row 8: row 8 has a
    # single prior sharer among the top-36 (index 23), so its
    # first doublings stay in the triple layer (8 records) and
    # the quad layer (11 records) and never reach the quint
    # layer (the same single-share doubling pattern as row 7
    # at rank-33 and row 9 at rank-34); the new-era double-row
    # histogram stays within the four hub rows 15/16/18/19
    # (machine-derived from the 2,722 computed records; the
    # preread new_quint histogram agrees)
    new5_dbl = {}
    for c, e in done5.items():
        cnt = Counter(r for i in c for r in rows[i])
        d = [r for r, v in cnt.items() if v == 2][0]
        new5_dbl[d] = new5_dbl.get(d, 0) + 1
    chk("quints.new_era_double_row_8_absent",
        new5_dbl == {15: 339, 16: 71, 18: 1043, 19: 1269}, new5_dbl)''',
    '''    # new-era b_only quints never double row 29: row 29 has a
    # single prior sharer among the top-37 (index 19), so its
    # first doublings stay in the triple layer (8 records) and
    # the quad layer (11 records) and never reach the quint
    # layer (the same single-share doubling pattern as row 7
    # at rank-33, row 9 at rank-34 and row 8 at rank-37); the
    # new-era double-row histogram stays within the four hub
    # rows 15/16/18/19 (machine-derived from the 2,868
    # computed records; the preread new_quint histogram agrees)
    new5_dbl = {}
    for c, e in done5.items():
        cnt = Counter(r for i in c for r in rows[i])
        d = [r for r, v in cnt.items() if v == 2][0]
        new5_dbl[d] = new5_dbl.get(d, 0) + 1
    chk("quints.new_era_double_row_29_absent",
        new5_dbl == {15: 339, 16: 71, 18: 1043, 19: 1415}, new5_dbl)''')

# ---- 13. finalize: sextets ----
rep('''    # ---- sextets: the quint-order I-E truncation stays closed at
    # k=37.  The published sextet census (commit 583b0bf1) proved
    # C(26,6)/C(27,6)/C(28,6) all zero, and the k=29/k=30/k=31/
    # k=32/k=33/k=34/k=35/k=36 publications reclassified C(29,6)/
    # C(30,6)/C(31,6)/C(32,6)/C(33,6)/C(34,6)/C(35,6)/C(36,6)
    # all zero (zero is superset-closed); a 6-subset of the
    # top-37 either lies inside the top-36 (already zero) or
    # contains the rank-37 root, so the full C(37,6)
    # reclassification here closes the k=37 truncation (also
    # cross-checked against the k=37 preread sextet census,
    # commit 98321003).''',
    '''    # ---- sextets: the quint-order I-E truncation stays closed at
    # k=38.  The published sextet census (commit 583b0bf1) proved
    # C(26,6)/C(27,6)/C(28,6) all zero, and the k=29/k=30/k=31/
    # k=32/k=33/k=34/k=35/k=36/k=37 publications reclassified
    # C(29,6)/C(30,6)/C(31,6)/C(32,6)/C(33,6)/C(34,6)/C(35,6)/
    # C(36,6)/C(37,6) all zero (zero is superset-closed); a
    # 6-subset of the top-38 either lies inside the top-37
    # (already zero) or contains the rank-38 root, so the full
    # C(38,6) reclassification here closes the k=38 truncation
    # (also cross-checked against the k=38 preread sextet
    # census, commit 75fabfd0).''')
rep('''    chk("sextet_census_k37",
        n6 == 2324784 and cen6 == {"b_only": 0, "zero": 2324784,
                                   "disjoint": 0}, cen6)
    chk("preread_match.sextet_census", cen6 == {
        "b_only": pre["rank37"]["sextet_census"]["counts"]["b_only"],
        "zero": pre["rank37"]["sextet_census"]["counts"]["zero"],
        "disjoint":
            pre["rank37"]["sextet_census"]["counts"]["disjoint"]})''',
    '''    chk("sextet_census_k38",
        n6 == 2760681 and cen6 == {"b_only": 0, "zero": 2760681,
                                   "disjoint": 0}, cen6)
    chk("preread_match.sextet_census", cen6 == {
        "b_only": pre["rank38"]["sextet_census"]["counts"]["b_only"],
        "zero": pre["rank38"]["sextet_census"]["counts"]["zero"],
        "disjoint":
            pre["rank38"]["sextet_census"]["counts"]["disjoint"]})''')

# ---- 14. finalize: kill reproduce band ----
rep('''    chk("reproduce_k1_36",
        all(kill[k] == int(k36j["values"]["kill"]["k%d" % k])
            for k in range(1, 37)))
    chk("split.reproduce_k1_36",
        all(killA[k] == int(k36j["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k36j["values"]["kill_B"]["k%d" % k])
            for k in range(1, 37)))''',
    '''    chk("reproduce_k1_37",
        all(kill[k] == int(k37j["values"]["kill"]["k%d" % k])
            for k in range(1, 38)))
    chk("split.reproduce_k1_37",
        all(killA[k] == int(k37j["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k37j["values"]["kill_B"]["k%d" % k])
            for k in range(1, 38)))''')
rep('''    chk("survival.marginal",
        0 <= kill[K] - kill[K - 1] <= mem[K - 1],
        {"k37_minus_k36": str(kill[K] - kill[K - 1]),
         "m37": str(mem[K - 1])})''',
    '''    chk("survival.marginal",
        0 <= kill[K] - kill[K - 1] <= mem[K - 1],
        {"k38_minus_k37": str(kill[K] - kill[K - 1]),
         "m38": str(mem[K - 1])})''')

# ---- 15. finalize: out dict ----
rep('"schema": "n11-cost16-survival-k37-20261119-v1",',
    '"schema": "n11-cost16-survival-k38-20261119-v1",')
rep('''        "title": ("Exact survival curve extended to k=37 for the "
                  "31-row cost-16 parent: rank-37 (8,19) has no "
                  "fresh row -- row 8 arrives with a single prior "
                  "sharer and doubles for the first time in the "
                  "triple layer (8 records) and the quad layer "
                  "(11 records) but never in the quint layer (the "
                  "same single-share pattern as row 7 at rank-33 "
                  "and row 9 at rank-34), while row 19 becomes an "
                  "eleven-sharer hub band row, the new pair census "
                  "is 12 shared / 24 disjoint (the shared pairs "
                  "are exactly the one row-8 sharer plus the "
                  "eleven row-19 sharers), and the quint era "
                  "opened at k=26 continues with 2,722 new "
                  "non-zero b_only quints of the C(37,5)=435,897 "
                  "5-subsets on top of the 17,434 published ones "
                  "(the quint double-row histogram stays within "
                  "the four hub rows 15/16/18/19: 15:3124 / 16:616 "
                  "/ 18:10260 / 19:6156) and the A-type 4-way term "
                  "grows to 1,520 (157 new disjoint quads on top "
                  "of the 1,363 published); 133 new disjoint "
                  "triples, 24 new disjoint pairs and 12 shared "
                  "ones; the full C(37,6)=2,324,784 sextet census "
                  "is all zero so the I-E stays closed at the "
                  "fifth order"),''',
    '''        "title": ("Exact survival curve extended to k=38 for the "
                  "31-row cost-16 parent: rank-38 (19,29) has no "
                  "fresh row -- row 29 arrives with a single prior "
                  "sharer and doubles for the first time in the "
                  "triple layer (8 records) and the quad layer "
                  "(11 records) but never in the quint layer (the "
                  "same single-share pattern as row 7 at rank-33 "
                  "row 9 at rank-34 and row 8 at rank-37), while "
                  "row 19 becomes a twelve-sharer hub band row, "
                  "the new pair census is 13 shared / 24 disjoint "
                  "(the shared pairs are exactly the twelve "
                  "row-19 sharers plus the one row-29 sharer, "
                  "index 19), and the quint era opened at k=26 "
                  "continues with 2,868 new non-zero b_only "
                  "quints of the C(38,5)=501,942 5-subsets on top "
                  "of the 20,156 published ones (the quint "
                  "double-row histogram stays within the four "
                  "hub rows 15/16/18/19: 15:3463 / 16:687 / "
                  "18:11303 / 19:7571) and the A-type 4-way term "
                  "grows to 1,677 (157 new disjoint quads on top "
                  "of the 1,520 published); 133 new disjoint "
                  "triples, 24 new disjoint pairs and 13 shared "
                  "ones; the full C(38,6)=2,760,681 sextet census "
                  "is all zero so the I-E stays closed at the "
                  "fifth order"),''')
rep('''            "k37_preread": {"path": K37_PREREAD_REL,
                            "git_blob_sha1": K37_PREREAD_PIN,
                            "commit": K37_PREREAD_COMMIT},
        },''',
    '''            "k37_preread": {"path": K37_PREREAD_REL,
                            "git_blob_sha1": K37_PREREAD_PIN,
                            "commit": K37_PREREAD_COMMIT},
            "survival_k37_json": {"path": K37_JSON_REL,
                                  "git_blob_sha1": K37_JSON_PIN,
                                  "commit": K37_JSON_COMMIT},
            "k38_preread": {"path": K38_PREREAD_REL,
                            "git_blob_sha1": K38_PREREAD_PIN,
                            "commit": K38_PREREAD_COMMIT},
        },''')
rep('''            "rank37_root": {"root": top[IDX38]["root"],
                            "rows": list(rows[IDX38]),
                            "membership": str(mem[IDX38]),
                            "a_part": str(ap[IDX38]),
                            "b_part": str(bp[IDX38]),
                            "note": "rank-37 (8,19): row 8 "
                                    "has a single prior sharer "
                                    "among the top-36 (index 23, "
                                    "the rank-24 root (8,18)), so "
                                    "it doubles for the first time "
                                    "in the triple and quad layers "
                                    "but never in the quint layer "
                                    "(the same single-share "
                                    "pattern as row 7 at rank-33 "
                                    "and row 9 at rank-34), while "
                                    "row 19 is now an eleven-sharer "
                                    "hub band row (indices 0,2,3,"
                                    "8,9,10,15,29,32,33,35); 24 "
                                    "disjoint and 12 shared "
                                    "partners"},''',
    '''            "rank38_root": {"root": top[IDX38]["root"],
                            "rows": list(rows[IDX38]),
                            "membership": str(mem[IDX38]),
                            "a_part": str(ap[IDX38]),
                            "b_part": str(bp[IDX38]),
                            "note": "rank-38 (19,29): row 29 "
                                    "has a single prior sharer "
                                    "among the top-37 (index 19, "
                                    "the rank-20 root (18,29)), "
                                    "so it doubles for the first "
                                    "time in the triple and quad "
                                    "layers but never in the "
                                    "quint layer (the same "
                                    "single-share pattern as "
                                    "row 7 at rank-33, row 9 at "
                                    "rank-34 and row 8 at "
                                    "rank-37), while row 19 is "
                                    "now a twelve-sharer hub "
                                    "band row (indices 0,2,3,8,"
                                    "9,10,15,29,32,33,35,36); 24 "
                                    "disjoint and 13 shared "
                                    "partners"},''')
rep('''            "preread_exact_integers": (
                {"note": "the k=37 preread (commit 98321003) is "
                         "pure Python with exact integer "
                         "serialization (same toolchain as the "
                         "k=32/k=33/k=34/k=35/k=36 prereads, "
                         "commits 490a3e44 / 67068e07 / "
                         "2a14f351 / 90fc51c9 / 67985e92c9), it "
                         "carries 34 checks all pass, and it "
                         "needs no big-integer erratum; its "
                         "membership/a_part/b_part "
                         "(119973409932394637 / 91996175553485330 / "
                         "27977234378909307) equal the pinned "
                         "aggregate exactly (asserted at load); "
                         "the structural fields (rows, hex, prior "
                         "hit indices, censuses, histograms) are "
                         "cross-checked at load and by the "
                         "preread_match.* finalize checks"}),''',
    '''            "preread_exact_integers": (
                {"note": "the k=38 preread (commit 75fabfd0) is "
                         "pure Python with exact integer "
                         "serialization (same toolchain as the "
                         "k=32/k=33/k=34/k=35/k=36/k=37 prereads, "
                         "commits 490a3e44 / 67068e07 / "
                         "2a14f351 / 90fc51c9 / 67985e92c9 / "
                         "98321003), it carries 34 checks all "
                         "pass, and it needs no big-integer "
                         "erratum; its membership/a_part/b_part "
                         "(119940649042609991 / 91876760891572775 / "
                         "28063888151037216) equal the pinned "
                         "aggregate exactly (asserted at load); "
                         "the structural fields (rows, hex, prior "
                         "hit indices, censuses, histograms) are "
                         "cross-checked at load and by the "
                         "preread_match.* finalize checks"}),''')
rep('finalize checks"}),"triple_census_k37": cen,',
    'finalize checks"}),"triple_census_k38": cen,')
rep('''            "quint_census_k37": cen5,
            "new_quint_census": {"b_only": 2722, "zero": 56183,
                                 "disjoint": 0},''',
    '''            "quint_census_k38": cen5,
            "new_quint_census": {"b_only": 2868, "zero": 63177,
                                 "disjoint": 0},''')
rep('''            "new_quad_b_only_double_row_histogram": (
                {"note": "row 8 doubles here for the first time "
                         "in the quad layer (11 records; single "
                         "prior sharer, the same single-share "
                         "pattern as row 7 at rank-33 and row 9 "
                         "at rank-34), while row 19 is the "
                         "dominant new double row (1,214 of the "
                         "2,394 new b_only quads), "
                         "machine-derived from the computed new "
                         "quads in this finalize",
                 "histogram": quad_dbl_hist}),
            "new_triple_b_only_double_row_histogram": (
                {"note": "computed fact: 120 of the 397 new b_only "
                         "triples double row 18, 246 double "
                         "row 19 and 8 double row 8 (row 8's "
                         "first doubling, mirroring row 7 at "
                         "rank-33 and row 9 at rank-34); rows 21 "
                         "and 22 never double",
                 "histogram": triple_dbl_hist}),
            "sextet_census_k37": cen6,''',
    '''            "new_quad_b_only_double_row_histogram": (
                {"note": "row 29 doubles here for the first time "
                         "in the quad layer (11 records; single "
                         "prior sharer, the same single-share "
                         "pattern as row 7 at rank-33, row 9 at "
                         "rank-34 and row 8 at rank-37), while "
                         "row 19 is the dominant new double row "
                         "(1,339 of the 2,519 new b_only quads), "
                         "machine-derived from the computed new "
                         "quads in this finalize",
                 "histogram": quad_dbl_hist}),
            "new_triple_b_only_double_row_histogram": (
                {"note": "computed fact: 120 of the 420 new b_only "
                         "triples double row 18, 269 double "
                         "row 19 and 8 double row 29 (row 29's "
                         "first doubling, mirroring row 7 at "
                         "rank-33, row 9 at rank-34 and row 8 at "
                         "rank-37); rows 21 and 22 never double",
                 "histogram": triple_dbl_hist}),
            "sextet_census_k38": cen6,''')
rep('''            "quints_zero_synth_count": 56183,''',
    '''            "quints_zero_synth_count": 63177,''')
rep('''            "quints_jsonl_note": ("zero quints are structural "
                                  "(classify from the pinned "
                                  "aggregate) and are not appended "
                                  "to the JSONL; finalize "
                                  "reclassifies all 435,897 "
                                  "5-subsets and asserts the exact "
                                  "census and the presence of every "
                                  "b_only record; the full "
                                  "C(37,6) sextet census is "
                                  "reclassified and asserted "
                                  "all-zero (truncation "
                                  "justification)"),''',
    '''            "quints_jsonl_note": ("zero quints are structural "
                                  "(classify from the pinned "
                                  "aggregate) and are not appended "
                                  "to the JSONL; finalize "
                                  "reclassifies all 501,942 "
                                  "5-subsets and asserts the exact "
                                  "census and the presence of every "
                                  "b_only record; the full "
                                  "C(38,6) sextet census is "
                                  "reclassified and asserted "
                                  "all-zero (truncation "
                                  "justification)"),''')
rep('''            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
                             "sum j4 + sum j5 for k <= 37; "
                             "kill_A(k) = sum a - sum j2_A + "
                             "sum j3_A - sum j4_A (j5_A == 0); "
                             "kill_B(k) = sum b - sum j2_B + "
                             "sum j3_B - sum j4_B + sum j5_B; "
                             "j4_A comes from the 1,520 disjoint "
                             "quads (1,363 published at k=36, 157 "
                             "new at k=37), j5_B from the 20,156 "
                             "b_only quints (17,434 prev, 2,722 "
                             "new); the sixth order stays "
                             "structurally zero (sextet_census_k37)"),''',
    '''            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
                             "sum j4 + sum j5 for k <= 38; "
                             "kill_A(k) = sum a - sum j2_A + "
                             "sum j3_A - sum j4_A (j5_A == 0); "
                             "kill_B(k) = sum b - sum j2_B + "
                             "sum j3_B - sum j4_B + sum j5_B; "
                             "j4_A comes from the 1,677 disjoint "
                             "quads (1,520 published at k=37, 157 "
                             "new at k=38), j5_B from the 23,024 "
                             "b_only quints (20,156 prev, 2,868 "
                             "new); the sixth order stays "
                             "structurally zero (sextet_census_k38)"),''')
rep('''            "marginal_k37": str(kill[K] - kill[K - 1]),''',
    '''            "marginal_k38": str(kill[K] - kill[K - 1]),''')


def main() -> int:
    src = open(SRC, encoding="utf-8").read()
    base_bytes = open(SRC, "rb").read()
    blob = hashlib.sha1(b"blob %d\x00" % len(base_bytes) + base_bytes).hexdigest()
    if blob != EXPECT_BASE_BLOB:
        raise SystemExit(f"FAIL base blob {blob}")
    out = sub(src)

    # residual sanity probes
    for stale in ("IDX37", "M37 = 119973409932394637", "load_top37",
                  "load_k37_base", "pre[\"rank37\"][", "k36ja",
                  "reproduce_k1_36", "marginal_k37", "sextet_census_k37",
                  "quints.census_435897", '"rank37_root"',
                  "triple_census_k37", "quint_census_k37"):
        if stale in out:
            raise SystemExit(f"FAIL stale token {stale!r} survived")
    # the m37 literal must survive exactly twice (rank-37
    # regression assertions: top-level and preread layer)
    if out.count("119973409932394637") != 2:
        raise SystemExit("FAIL m37 literal count %d != 2"
                         % out.count("119973409932394637"))
    if out.count("119940649042609991") != 3:
        raise SystemExit("FAIL m38 literal count %d != 3"
                         % out.count("119940649042609991"))
    open(DST, "w", encoding="utf-8").write(out)
    data = open(DST, "rb").read()
    print("wrote", DST, len(data), "bytes")
    print("git_blob_sha1:", hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest())
    print("sha256:", hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())

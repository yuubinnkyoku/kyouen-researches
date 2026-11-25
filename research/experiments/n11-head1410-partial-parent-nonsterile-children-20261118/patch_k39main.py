#!/usr/bin/env python3
"""Anchored-rep transformation: k38 main script -> k39 main script.

Reads base/k38main.py (published k=38 main computation script, git
blob 565f72934842be687cc05e30df7a6d532f795ea1, sha256
08b68449c961d03cea519e7b85239d081a498d62976233e93772cafc83848784)
and writes cost16_survival_k39_20261119.py.  Mirrors the published
k37->k38 transformation (patch_k38main.py): pinned k=38 result JSON
(c45ea8d0a11f009343c0736f6b98b5e4d06e8d4e, commit 78b6f1bd) and
k=39 preread (6056bd831d4ea32212f39016455078ff0557573c, commit
848727f192) join the pin set; load_top39 asserts the rank-39 root
(5,24) facts plus the rank-38/rank-37 regression layers of the
k=39 preread; load_k39_base appends the k=38 era records (37
pairs / 666 triples / 7,770 stored quads / 2,868 b_only quints ->
quints_prev 23,024, so every era merge downstream moves to the
703 / 8,436 / 73,100 totals); the first disjoint quints ever (508,
|union|=10, opening the A-type 5-way term) make mode_quints
three-class and the first non-zero sextet layer (5,852 b_only of
C(39,6)=3,262,623, all containing rank-39) adds the new
mode_sextets plus a j6 B-type term: kill(k) = sum m - sum j2 +
sum j3 - sum j4 + sum j5 - sum j6 with the k=39 preread level-7
closure (99,122 candidate septets, all zero) pinning the
truncation at level 6; finalize's censuses move to C(39,3)=9,139
/ C(39,4)=82,251 / C(39,5)=575,757 / C(39,6)=3,262,623 and the
reproduce band extends to kill(1..38) vs the pinned k=38
publication; the structural double-row checks move from row 29
to rows 5 and 24 (the first two-sharer/two-sharer generation:
triple 54/46, quad 391/259, quint 763/179 records).  The
rewritten docstring also fixes the k=38 docstring sign erratum
(kill_B has - sum j4_B at the fourth order; the k=38
implementation and published 315-check crosscheck all
used the minus sign).

Every replacement asserts exact occurrence counts, so a drifted
base file aborts before writing anything.
"""
import hashlib
import sys

SRC = "base/k38main.py"
DST = "cost16_survival_k39_20261119.py"
EXPECT_BASE_BLOB = "565f72934842be687cc05e30df7a6d532f795ea1"
EXPECT_BASE_SHA256 = ("08b68449c961d03cea519e7b85239d081a498d62976"
                     "233e93772cafc83848784")

reps = []


def rep(old, new, count=1):
    reps.append((old, new, count))


rep(r'''"""Survival-curve extension to k=38 for the 31-row cost-16 parent
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
"""''',
    r'''"""Survival-curve extension to k=39 for the 31-row cost-16 parent
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
"""''', 1)

rep(r'''K = 38
# R stays 31: the parent is the fixed 31-row cost-16 parent
# (len(P["target"]) == 31, asserted at every get_parent call
# site); K=38 bans 38 pair roots drawn from it.  A wrong R
# here would silently zero every b_only joint.
R = 31
IDX38 = 37''',
    r'''K = 39
# R stays 31: the parent is the fixed 31-row cost-16 parent
# (len(P["target"]) == 31, asserted at every get_parent call
# site); K=39 bans 39 pair roots drawn from it.  A wrong R
# here would silently zero every b_only joint.
R = 31
IDX39 = 38''', 1)

rep(r'''K38_PREREAD_REL = EXP_REL + "cost16-survival-k38-preread-20261119.json"
K38_PREREAD_PIN = "3fa8297990d8e9880f386a0cfa075e3a95f226fd"
K38_PREREAD_COMMIT = "75fabfd0"
RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k38-20261119.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k38-20261119.json")

M38 = 119940649042609991''',
    r'''K38_PREREAD_REL = EXP_REL + "cost16-survival-k38-preread-20261119.json"
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

M39 = 119883868794265826''', 1)

rep(r'''    # rank-38 root: (19,29), the fourth single-sharer doubling
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
    assert top[IDX38 - 1]["root"] == \
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
            if 29 in top[i]["rows_covered"]] == [19]''',
    r'''    # rank-39 root: (5,24), the first two-sharer/two-sharer root
    # (no fresh row and no single-sharer row: row 5 arrives via
    # prior sharers 2 = the rank-3 root (5,19) and 25 = the
    # rank-26 root (5,16); row 24 via 4 = the rank-5 root
    # (18,24) and 14 = the rank-15 root (15,24)), so both rows
    # double for the first time in the triple, quad and quint
    # layers (54/391/763 records for row 5 and 46/259/179 for
    # row 24) -- the first generation whose double-row family
    # gains two rows at once
    assert sorted(top[IDX38]["rows_covered"]) == [5, 24]
    assert top[IDX38]["root"] == "00000000000000889002000000100200"
    assert top[IDX38]["membership"] == M39
    # rank-38 regression anchor (published k=38 facts, commit
    # 78b6f1bd): the fourth single-share doubling root; row 29
    # has the single prior sharer index 19 among the top-37,
    # while row 19 is a twelve-sharer hub band row and gains
    # the rank-38 root itself as a sharer
    assert sorted(top[IDX38 - 1]["rows_covered"]) == [19, 29]
    assert top[IDX38 - 1]["root"] == \
        "00000008800000003800000008100000"
    assert top[IDX38 - 1]["membership"] == 119940649042609991
    assert [i for i in range(IDX38 - 1)
            if 19 in top[i]["rows_covered"]] == [0, 2, 3, 8, 9, 10,
                                                 15, 29, 32, 33, 35,
                                                 36]
    assert [i for i in range(IDX38 - 1)
            if 29 in top[i]["rows_covered"]] == [19]
    assert [i for i in range(IDX38)
            if 19 in top[i]["rows_covered"]] == [0, 2, 3, 8, 9, 10,
                                                 15, 29, 32, 33, 35,
                                                 36, 37]
    assert [i for i in range(IDX38)
            if 29 in top[i]["rows_covered"]] == [19, 37]
    # rows 5 and 24 have exactly the two listed prior sharers
    # each among the top-38 (row 5: index 2 = the rank-3 root
    # (5,19) and index 25 = the rank-26 root (5,16); row 24:
    # index 4 = the rank-5 root (18,24) and index 14 = the
    # rank-15 root (15,24)); the doublings of rows 5 and 24
    # start only with the rank-39 root in the member set
    assert [i for i in range(IDX38)
            if 5 in top[i]["rows_covered"]] == [2, 25]
    assert [i for i in range(IDX38)
            if 24 in top[i]["rows_covered"]] == [4, 14]''', 1)

rep(r'''    pre = json.loads(base.read_pinned(K38_PREREAD_REL, K38_PREREAD_PIN))
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
                                              "disjoint": 0}
    # rank-37 regression layer of the k=38 preread (machine
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
    assert r36["mismatches"] == 0
    return agg, top, memA, memB, total, A16, B16, pre''',
    r'''    # preread structural pins (commit 848727f192); the k=39
    # preread is pure Python with exact integer serialization
    # (like the k=32/k=33/k=34/k=35/k=36/k=37/k=38 prereads),
    # so its big-integer fields equal the pinned aggregate
    # exactly and need no erratum
    pre = json.loads(base.read_pinned(K39_PREREAD_REL, K39_PREREAD_PIN))
    assert pre["schema"] == "n11-cost16-k39-preread-20261119-v1"
    assert pre["check_count"] == 35 and pre["all_pass"] is True
    r39 = pre["rank39"]
    assert r39["root"] == top[IDX38]["root"]
    assert r39["rows"] == [5, 24]
    assert r39["membership"] == M39
    assert r39["a_part"] == memA[top[IDX38]["root"]]
    assert r39["b_part"] == memB[top[IDX38]["root"]]
    assert memA[top[IDX38]["root"]] + memB[top[IDX38]["root"]] == M39
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
    assert r38["root"] == top[IDX38 - 1]["root"]
    assert r38["rows"] == [19, 29]
    assert r38["membership"] == 119940649042609991
    assert r38["a_part"] == memA[top[IDX38 - 1]["root"]]
    assert r38["b_part"] == memB[top[IDX38 - 1]["root"]]
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
    return agg, top, memA, memB, total, A16, B16, pre''', 1)

rep(r'''def load_k38_base():
    """666 pairwise joints, 7,770 triples, the 65,330 stored quads
    and the 20,156 b_only quints among the top-37, from the pinned
    k14..k36 publications plus the pinned k=37 result."""''',
    r'''def load_k39_base():
    """703 pairwise joints, 8,436 triples, the 73,100 stored quads
    and the 23,024 b_only quints among the top-38, from the pinned
    k14..k36 publications plus the pinned k=37/k=38 results."""''', 1)

rep(r'''    quints26 = {}''',
    r'''    k38j = json.loads(base.read_pinned(K38_JSON_REL, K38_JSON_PIN))
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
    quints26 = {}''', 1)

rep(r'''    quints_prev = {}''',
    r'''    quints38 = {}
    for key, v in k38j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints38[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints38) == 2868
    assert all(37 in c and 38 not in c for c in quints38)
    quints_prev = {}''', 1)

rep(r'''    quints_prev.update(quints37)
    assert len(quints_prev) == 20156
    return k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, \
        k24, k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \
        k37j, pairs, triples, quads, quints_prev''',
    r'''    quints_prev.update(quints37)
    quints_prev.update(quints38)
    assert len(quints_prev) == 23024
    return k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \
        k37j, k38j, pairs, triples, quads, quints_prev''', 1)

rep(r'''def new_quint_combos():
    return [(IDX38, i, j, l, m) for i, j, l, m in
            itertools.combinations(range(IDX38), 4)]''',
    r'''def new_quint_combos():
    return [(IDX38, i, j, l, m) for i, j, l, m in
            itertools.combinations(range(IDX38), 4)]


def new_sextet_combos():
    return [(IDX38, i, j, l, m, n) for i, j, l, m, n in
            itertools.combinations(range(IDX38), 5)]''', 1)

rep(r'''    print("[pairs] todo %d (done %d/37)" % (len(todo), len(donep)),''',
    r'''    print("[pairs] todo %d (done %d/38)" % (len(todo), len(donep)),''', 1)

rep(r'''    print("[pairs] done %d/37" % len(done("pair",''',
    r'''    print("[pairs] done %d/38" % len(done("pair",''', 1)

rep(r'''    assert len(combos) == 666''',
    r'''    assert len(combos) == 703''', 1)

rep(r'''    print("[triples] slice %d done, done %d/666 in %.1fs"''',
    r'''    print("[triples] slice %d done, done %d/703 in %.1fs"''', 1)

rep(r'''    assert len(combos) == 7770''',
    r'''    assert len(combos) == 8436''', 1)

rep(r'''    print("[quads] slice %d done, done %d/7770"''',
    r'''    print("[quads] slice %d done, done %d/8436"''', 1)

rep(r'''def mode_quints(slice_arg):
    """B-type-only 5-way joints for the 2,868 new b_only quints
    (the 20,156 prev-era records load from the pinned
    k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/k=36/k=37
    JSONs).  Zero
    quints are structural (classify from the pinned aggregate) and
    are synthesized in finalize, not appended here."""
    agg, top, memA, memB, total, A16, B16, pre = load_top38()
    P = k14m.get_parent()
    assert len(P["target"]) == R
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_quint_combos()
    assert len(combos) == 66045
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
    print("[quints] slice %d done, done %d/2868b_only in %.1fs"
          % (slice_arg,
             len(done("quint", lambda e: tuple(e["combo"]))),
             time.time() - t00), flush=True)
    return 0''',
    r'''def mode_quints(slice_arg):
    """5-way joints for the 73,815 new quints: 13,658 b_only
    (B-type residual count, MyPm) and 508 disjoint (A-type 5-way
    term at |union|=10 plus the two-case B-type term, the same
    union-mask machinery as the disjoint pairs/triples/quads,
    PmLazy).  The 23,024 prev-era b_only records load from the
    pinned k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/
    k=36/k=37/k=38 publications.  Zero quints are structural
    (classify from the pinned aggregate) and are synthesized in
    finalize, not appended here."""
    agg, top, memA, memB, total, A16, B16, pre = load_top38()
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
                print("[quints] budget hit", flush=True)
                break
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
    donen = done("quint", lambda e: tuple(e["combo"]))
    nb = sum(1 for e in donen.values() if e["class"] == "b_only")
    nd = sum(1 for e in donen.values()
             if e["class"] == "disjoint")
    print("[quints] slice %d done, done b_only %d/13658 disjoint"
          " %d/508 in %.1fs"
          % (slice_arg, nb, nd, time.time() - t00), flush=True)
    return 0


def mode_sextets(slice_arg):
    """B-type-only 6-way joints for the 5,852 new b_only sextets
    (C(39,6) census 5,852 b_only / 3,256,771 zero / 0 disjoint --
    the first non-zero sextet layer ever; all 5,852 contain the
    rank-39 root).  Zero sextets are structural (classify from
    the pinned aggregate) and are synthesized in finalize, not
    appended here."""
    agg, top, memA, memB, total, A16, B16, pre = load_top38()
    P = k14m.get_parent()
    assert len(P["target"]) == R
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_sextet_combos()
    assert len(combos) == 501942
    lo = slice_arg * 200
    hi = min(lo + 200, len(combos))
    done6 = done("sextet", lambda e: tuple(e["combo"]))
    t00 = time.time()
    for combo in combos[lo:hi]:
        if combo in done6:
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
        append({"kind": "sextet", "combo": list(combo),
                "class": "b_only", "union": union, "joint": val,
                "joint_A": 0, "joint_B": val,
                "memo_states": len(pmf.memo),
                "sec": round(time.time() - t0, 1)})
        print("[sextet b_only %s] union=%s j6B=%d %.1fs"
              % (combo, union, val, time.time() - t0), flush=True)
        if time.time() - t00 > 240:
            print("[sextets] budget hit", flush=True)
            break
    print("[sextets] slice %d done, done %d/5852b_only in %.1fs"
          % (slice_arg,
             len(done("sextet", lambda e: tuple(e["combo"]))),
             time.time() - t00), flush=True)
    return 0''', 1)

rep(r'''    """Pre-production validation of disjoint_joint at |union|=4
    (published k13-era pair joints, both pm lineages), |union|=6
    (2 published k37 disjoint triples) and |union|=8 (2 published
    k37 disjoint quads, both pm lineages with exact A/B match
    against the pinned publication).  The |union|=8 machinery was
    introduced at k=26 and extended by the k=27/k=28/k=29/k=30/
    k=31/k=32/k=33/k=34/k=35/k=36/k=37 publications (1,520
    production records); this re-anchors it on published records
    before production."""''',
    r'''    """Pre-production validation of disjoint_joint at |union|=4
    (published k13-era pair joints, both pm lineages), |union|=6
    (2 published k38 disjoint triples) and |union|=8 (2 published
    k38 disjoint quads, both pm lineages with exact A/B match
    against the pinned publication).  The |union|=8 machinery was
    introduced at k=26 and extended by the k=27/k=28/k=29/k=30/
    k=31/k=32/k=33/k=34/k=35/k=36/k=37/k=38 publications (1,677
    production records); this re-anchors it on published records
    before production.  The |union|=10 extension for the new
    disjoint quints has no published analogue to anchor on
    (k=26..k=38 produced no |union|>8 record), so it is validated
    by the mainline disjoint-quad chain (subset structure and
    bounds asserted in finalize) plus the double-lineage crossq5
    check instead."""''', 1)

rep(r'''    k37ja = json.loads(base.read_pinned(K37_JSON_REL, K37_JSON_PIN))''',
    r'''    k38ja = json.loads(base.read_pinned(K38_JSON_REL, K38_JSON_PIN))''', 1)

rep(r'''k37ja''',
    r'''k38ja''', 4)

rep(r'''    print("[cross] mismatches %d" % nbad, flush=True)''',
    r'''    # new disjoint quints: |union|=10, both pm lineages vs stored
    # (the |union|=10 machinery has no published reference, so it
    # gets the strongest available cross-check here)
    candq5 = [c for c in new_quint_combos()
              if c in quin and quin[c]["class"] == "disjoint"
              and classify(rows, c)[0] == "disjoint"][:2]
    assert len(candq5) == 2, candq5
    for combo in candq5:
        ref = quin[combo]
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        for lineage, pmg in [
                ("lazypm", base.PmLazy(edge_w, R)),
                ("mypm", PmGet(k10s.MyPm(edge_w, R)))]:
            base.STATE_CAP = 16_000_000
            base.BUDGET_SECONDS = 900.0
            t0 = time.time()
            ja, jb = disjoint_joint(edge_w, pmg, w1, union)
            match = (ja == ref["joint_A"] and jb == ref["joint_B"])
            append({"kind": "crossq5", "combo": list(combo),
                    "lineage": lineage, "union": union,
                    "joint_A": ja, "joint_B": jb,
                    "ref_A": ref["joint_A"], "ref_B": ref["joint_B"],
                    "match": match,
                    "sec": round(time.time() - t0, 1)})
            print("[crossq5 %s %s] A=%d B=%d ref A=%d B=%d"
                  " match=%s %.1fs"
                  % (lineage, combo, ja, jb, ref["joint_A"],
                     ref["joint_B"], match, time.time() - t0),
                  flush=True)
            if not match:
                nbad += 1
    # new b_only sextets: second lineage (PmLazy) vs stored (MyPm)
    done6 = done("sextet", lambda e: tuple(e["combo"]))
    cand6 = [c for c in new_sextet_combos()
             if c in done6 and done6[c]["class"] == "b_only"][:2]
    assert len(cand6) == 2, cand6
    for combo in cand6:
        ref = done6[combo]
        base.STATE_CAP = 16_000_000
        base.BUDGET_SECONDS = 900.0
        pmg = base.PmLazy(edge_w, R)
        t0 = time.time()
        mask = (1 << R) - 1
        for u in ref["union"]:
            mask &= ~(1 << u)
        val = pmg.get(mask)
        match = (val == ref["joint"])
        append({"kind": "cross6", "combo": list(combo),
                "lineage": "lazypm", "joint": val,
                "ref": ref["joint"], "match": match})
        print("[cross6 %s] j6=%d ref=%d match=%s %.1fs"
              % (combo, val, ref["joint"], match, time.time() - t0),
              flush=True)
        if not match:
            nbad += 1
    print("[cross] mismatches %d" % nbad, flush=True)''', 1)

rep(r'''    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \
        k37j, pairs_prev, triples_prev, quads_prev, quints_prev \
        = load_k38_base()''',
    r'''    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \
        k37j, k38j, pairs_prev, triples_prev, quads_prev, quints_prev \
        = load_k39_base()''', 1)

rep(r'''    done5 = done("quint", lambda e: tuple(sorted(e["combo"])))''',
    r'''    done5 = done("quint", lambda e: tuple(sorted(e["combo"])))
    done6 = done("sextet", lambda e: tuple(sorted(e["combo"])))''', 1)

rep(r'''    # ---- pairs (666 + 37 = 703)
    j2 = dict(pairs_prev)
    chk("pairs.prev_666", len(pairs_prev) == 666)
    chk("pairs.new_37", len(donep) == 37)''',
    r'''    # ---- pairs (703 + 38 = 741)
    j2 = dict(pairs_prev)
    chk("pairs.prev_703", len(pairs_prev) == 703)
    chk("pairs.new_38", len(donep) == 38)''', 1)

rep(r'''    chk("pairs.complete_703", len(j2) == 703)''',
    r'''    chk("pairs.complete_741", len(j2) == 741)''', 1)

rep(r'''    chk("pairs.new_census",
        len(shared_new) == 13 and len(donep) - len(shared_new) == 24,
        {"shared": len(shared_new),
         "disjoint": len(donep) - len(shared_new)})''',
    r'''    chk("pairs.new_census",
        len(shared_new) == 4 and len(donep) - len(shared_new) == 34,
        {"shared": len(shared_new),
         "disjoint": len(donep) - len(shared_new)})''', 1)

rep(r'''    # ---- triples (7770 + 666 = 8436)''',
    r'''    # ---- triples (8436 + 703 = 9139)''', 1)

rep(r'''    chk("triples.prev_7770", len(j3) == 7770)
    chk("triples.new_666", len(donet) == 666)''',
    r'''    chk("triples.prev_8436", len(j3) == 8436)
    chk("triples.new_703", len(donet) == 703)''', 1)

rep(r'''    chk("triples.complete_8436", len(j3) == 8436)''',
    r'''    chk("triples.complete_9139", len(j3) == 9139)''', 1)

rep(r'''    chk("triples.census",
        cen == {"b_only": 5178, "zero": 1533, "disjoint": 1725}, cen)
    chk("preread_match.triple_census", cen == {
        "b_only": pre["rank38"]["full_triples"]["counts"]["b_only"],
        "zero": pre["rank38"]["full_triples"]["counts"]["zero"],
        "disjoint":
            pre["rank38"]["full_triples"]["counts"]["disjoint"]})''',
    r'''    chk("triples.census",
        cen == {"b_only": 5497, "zero": 1575, "disjoint": 2067}, cen)
    chk("preread_match.triple_census", cen == {
        "b_only": pre["rank39"]["full_triples"]["counts"]["b_only"],
        "zero": pre["rank39"]["full_triples"]["counts"]["zero"],
        "disjoint":
            pre["rank39"]["full_triples"]["counts"]["disjoint"]})''', 1)

rep(r'''    # ---- quads (66045 prev + 7770 new = 73815)''',
    r'''    # ---- quads (73815 prev + 8436 new = 82251)''', 1)

rep(r'''    chk("quads.prev_66045_stored_65330",
        len(j4) == 66045 and len(quads_prev) == 65330,
        {"stored": len(quads_prev)})
    chk("quads.new_7770", len(doneq) == 7770)''',
    r'''    chk("quads.prev_73815_stored_73100",
        len(j4) == 73815 and len(quads_prev) == 73100,
        {"stored": len(quads_prev)})
    chk("quads.new_8436", len(doneq) == 8436)''', 1)

rep(r'''    chk("quads.complete_73815", len(j4) == 73815)''',
    r'''    chk("quads.complete_82251", len(j4) == 82251)''', 1)

rep(r'''    chk("quads.new_census",
        qcen == {"b_only": 2519, "zero": 5094, "disjoint": 157},
        qcen)
    chk("preread_match.new_quad_census", qcen == {
        "b_only": pre["rank38"]["new_census"]["quad"]["b_only"],
        "zero": pre["rank38"]["new_census"]["quad"]["zero"],
        "disjoint": pre["rank38"]["new_census"]["quad"]["disjoint"]})''',
    r'''    chk("quads.new_census",
        qcen == {"b_only": 4398, "zero": 3029, "disjoint": 1009},
        qcen)
    chk("preread_match.new_quad_census", qcen == {
        "b_only": pre["rank39"]["new_census"]["quad"]["b_only"],
        "zero": pre["rank39"]["new_census"]["quad"]["zero"],
        "disjoint": pre["rank39"]["new_census"]["quad"]["disjoint"]})''', 1)

rep(r'''    chk("quads.prev_disjoint_1520", len(prev_disjoint) == 1520)''',
    r'''    chk("quads.prev_disjoint_1677", len(prev_disjoint) == 1677)''', 1)

rep(r'''    # new b_only quads double-row histogram (machine-derived;
    # row 29 doubles here for the first time in the quad layer
    # (11 records; single prior sharer index 19 -- the same
    # single-share doubling pattern as row 7 at rank-33, row 9
    # at rank-34 and row 8 at rank-37), while row 19 is the
    # dominant new double row (1,339 of the 2,519 new b_only
    # quads)); the b_only triple double-row histogram is
    # recorded as a computed fact too''',
    r'''    # new b_only double-row histograms (machine-derived from
    # the computed records; rows 5 and 24 double here for the
    # first time in the quad layer (391 and 259 records, the
    # first generation with two new double rows at once), while
    # row 19 stays the dominant new double row (1,257 of the
    # 4,398 new b_only quads) and row 18 follows with 1,965);
    # the b_only triple double-row histogram is recorded as a
    # computed fact too''', 1)

rep(r'''    chk("triples.new_b_only_double_rows",
        triple_dbl_hist == {0: 1, 4: 1, 15: 15, 16: 3,
                            18: 120, 19: 269, 23: 1, 24: 1, 29: 8,
                            30: 1},
        triple_dbl_hist)''',
    r'''    chk("triples.new_b_only_double_rows",
        triple_dbl_hist == {0: 3, 1: 1, 4: 3, 5: 54, 7: 1, 8: 1,
                            9: 1, 11: 1, 14: 1, 15: 15, 16: 1,
                            18: 120, 19: 66, 23: 1, 24: 46, 29: 1,
                            30: 3},
        triple_dbl_hist)''', 1)

rep(r'''    chk("quads.new_b_only_double_row_29_first_quad_doubling",
        quad_dbl_hist.get(29, 0) == 11, quad_dbl_hist)
    chk("quads.new_b_only_double_rows",
        quad_dbl_hist == {0: 15, 4: 2, 15: 245, 16: 31,
                          18: 870, 19: 1339, 23: 2, 24: 2, 29: 11,
                          30: 2},
        quad_dbl_hist)''',
    r'''    chk("quads.new_b_only_double_rows_5_24_first_quad_doubling",
        quad_dbl_hist.get(5, 0) == 391
        and quad_dbl_hist.get(24, 0) == 259, quad_dbl_hist)
    chk("quads.new_b_only_double_rows",
        quad_dbl_hist == {0: 60, 1: 6, 4: 32, 5: 391, 7: 6, 8: 6,
                          9: 6, 11: 6, 14: 6, 15: 333, 16: 15,
                          18: 1965, 19: 1257, 23: 12, 24: 259,
                          29: 6, 30: 32},
        quad_dbl_hist)''', 1)

rep(r'''    # ---- quints (415,741 top-37 zeros + 20,156 prev b_only +
    #      63,177 new zeros + 2,868 new b_only = 501,942)
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
        if IDX38 in c:
            assert c in done5, ("missing new b_only quint record", c)
            j5v = done5[c]["joint"]
        else:
            assert c in quints_prev, ("missing prev b_only quint "
                                   "record", c)
            j5v = quints_prev[c]["joint"]
        j5[c] = {"class": "b_only", "joint": j5v,
                 "A": 0, "B": j5v}
    chk("quints.census_501942",
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
        pre["rank38"]["full_quints"]["double_row_histogram"].items()})
    prev_cen5 = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(K - 1), 5):
        prev_cen5[classify(rows, c)[0]] += 1
    chk("quints.prev_census_matches_k37",
        prev_cen5 == {"b_only": 20156, "zero": 415741,
                     "disjoint": 0},
        prev_cen5)
    chk("quints.new_records_2868", len(done5) == 2868)
    chk("quints.new_b_only_contain_rank38", all(
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
        if j5[c]["class"] == "b_only" and IDX38 not in c))
    chk("quints.bounds", all(
        j5[c]["joint"] <= min(
            j4[tuple(sorted(set(c) - {x}))]["joint"] for x in c)
        for c in j5 if j5[c]["joint"]))
    # new-era b_only quints never double row 29: row 29 has a
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
        new5_dbl == {15: 339, 16: 71, 18: 1043, 19: 1415}, new5_dbl)
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
    chk("quints.disjoint_quad_subset_structure", sub_ok)''',
    r'''    # ---- quints (478,918 top-38 zeros + 23,024 prev b_only +
    #      59,649 new zeros + 13,658 new b_only + 508 new
    #      disjoint = 575,757)
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
        if kind == "disjoint":
            # the first disjoint quints ever (every C(k,5)
            # census for k <= 38 was disjoint-zero), so every
            # disjoint quint must contain rank-39
            assert IDX38 in c, ("prev-era disjoint quint", c)
            assert c in done5, ("missing new disjoint quint "
                                "record", c)
            j5[c] = {"class": "disjoint",
                     "joint": done5[c]["joint"],
                     "A": done5[c]["joint_A"],
                     "B": done5[c]["joint_B"]}
            continue
        assert kind == "b_only", (c, kind)
        from collections import Counter
        cnt = Counter(r for i in c for r in rows[i])
        d = [r for r, v in cnt.items() if v == 2][0]
        dbl_hist[d] = dbl_hist.get(d, 0) + 1
        if IDX38 in c:
            assert c in done5, ("missing new b_only quint record", c)
            j5v = done5[c]["joint"]
        else:
            assert c in quints_prev, ("missing prev b_only quint "
                                   "record", c)
            j5v = quints_prev[c]["joint"]
        j5[c] = {"class": "b_only", "joint": j5v,
                 "A": 0, "B": j5v}
    chk("quints.census_575757",
        n5 == 575757 and cen5 == {"b_only": 36682, "zero": 538567,
                                  "disjoint": 508},
        {"census": cen5, "double_rows": dbl_hist})
    chk("quints.double_rows_hist",
        dbl_hist == {0: 198, 1: 4, 4: 26, 5: 763, 7: 4, 8: 4, 9: 4,
                     11: 4, 14: 4, 15: 5024, 16: 725, 18: 17865,
                     19: 11838, 23: 10, 24: 179, 29: 4, 30: 26},
        dbl_hist)
    chk("preread_match.quint_census", cen5 == {
        "b_only": pre["rank39"]["full_quints"]["counts"]["b_only"],
        "zero": pre["rank39"]["full_quints"]["counts"]["zero"],
        "disjoint": pre["rank39"]["full_quints"]["counts"]["disjoint"]})
    chk("preread_match.quint_double_rows", dbl_hist == {
        int(r): v for r, v in
        pre["rank39"]["full_quints"]["double_row_histogram"].items()})
    prev_cen5 = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(K - 1), 5):
        prev_cen5[classify(rows, c)[0]] += 1
    chk("quints.prev_census_matches_k38",
        prev_cen5 == {"b_only": 23024, "zero": 478918,
                     "disjoint": 0},
        prev_cen5)
    chk("quints.new_records_14166", len(done5) == 14166,
        {"b_only": sum(1 for e in done5.values()
                       if e["class"] == "b_only"),
         "disjoint": sum(1 for e in done5.values()
                         if e["class"] == "disjoint")})
    chk("quints.new_b_only_contain_rank39", all(
        IDX38 in c for c in j5
        if j5[c]["class"] == "b_only" and 25 not in c
        and 26 not in c and 27 not in c and 28 not in c
        and 29 not in c and 30 not in c and 31 not in c
        and 32 not in c and 33 not in c and 34 not in c
        and 35 not in c and 36 not in c and 37 not in c))
    chk("quints.prev_b_only_contain_rank26_through_38", all(
        (25 in c) or (26 in c) or (27 in c) or (28 in c)
        or (29 in c) or (30 in c) or (31 in c) or (32 in c)
        or (33 in c) or (34 in c) or (35 in c) or (36 in c)
        or (37 in c)
        for c in j5
        if j5[c]["class"] == "b_only" and IDX38 not in c))
    chk("quints.disjoint_union_size_10", all(
        len(done5[c]["union"]) == 10
        for c in j5 if j5[c]["class"] == "disjoint"))
    chk("quints.bounds", all(
        j5[c]["joint"] <= min(
            j4[tuple(sorted(set(c) - {x}))]["joint"] for x in c)
        for c in j5 if j5[c]["joint"]))
    # new-era double-row histogram (machine-derived from the
    # 14,166 computed records; the 508 disjoint records have no
    # doubled row, so the histogram counts b_only records only):
    # rows 5 and 24 double for the first time in the quint layer
    # (763 and 179 records -- the first generation with two new
    # double rows at once); the preread new_quint histogram
    # agrees
    new5_dbl = {}
    for c, e in done5.items():
        if e["class"] != "b_only":
            continue
        cnt = Counter(r for i in c for r in rows[i])
        d = [r for r, v in cnt.items() if v == 2][0]
        new5_dbl[d] = new5_dbl.get(d, 0) + 1
    chk("quints.new_era_double_rows",
        new5_dbl == {0: 198, 1: 4, 4: 26, 5: 763, 7: 4, 8: 4, 9: 4,
                     11: 4, 14: 4, 15: 1561, 16: 38, 18: 6562,
                     19: 4267, 23: 10, 24: 179, 29: 4, 30: 26},
        new5_dbl)
    # every b_only quint has exactly three b_only 4-subsets
    # (remove one of the three fresh roots) and two disjoint
    # 4-subsets (remove one of the two doubled-row sharers);
    # every disjoint quint has five disjoint 4-subsets (the
    # first disjoint quints ever, machine-verified for all 508);
    # every disjoint quad has four disjoint 3-subsets
    sub_ok = True
    for c in j5:
        if j5[c]["class"] not in ("b_only", "disjoint"):
            continue
        kinds = [j4[tuple(sorted(set(c) - {x}))]["class"] for x in c]
        if j5[c]["class"] == "b_only":
            if sorted(kinds) != ["b_only", "b_only", "b_only",
                                 "disjoint", "disjoint"]:
                sub_ok = False
        else:
            if set(kinds) != {"disjoint"}:
                sub_ok = False
    for c in j4:
        if j4[c]["class"] != "disjoint":
            continue
        kinds = [j3[tuple(sorted(set(c) - {x}))]["class"] for x in c]
        if set(kinds) != {"disjoint"}:
            sub_ok = False
    chk("quints.subset_structure", sub_ok)
    chk("quints.disjoint_A_terms", all(
        done5[c]["joint_A"] > 0
        for c in j5 if j5[c]["class"] == "disjoint"))''', 1)

rep(r'''    # ---- sextets: the quint-order I-E truncation stays closed at
    # k=38.  The published sextet census (commit 583b0bf1) proved
    # C(26,6)/C(27,6)/C(28,6) all zero, and the k=29/k=30/k=31/
    # k=32/k=33/k=34/k=35/k=36/k=37 publications reclassified
    # C(29,6)/C(30,6)/C(31,6)/C(32,6)/C(33,6)/C(34,6)/C(35,6)/
    # C(36,6)/C(37,6) all zero (zero is superset-closed); a
    # 6-subset of the top-38 either lies inside the top-37
    # (already zero) or contains the rank-38 root, so the full
    # C(38,6) reclassification here closes the k=38 truncation
    # (also cross-checked against the k=38 preread sextet
    # census, commit 75fabfd0).
    cen6 = {"b_only": 0, "zero": 0, "disjoint": 0}
    n6 = 0
    for c in itertools.combinations(range(K), 6):
        n6 += 1
        cen6[classify(rows, c)[0]] += 1
    chk("sextet_census_k38",
        n6 == 2760681 and cen6 == {"b_only": 0, "zero": 2760681,
                                   "disjoint": 0}, cen6)
    chk("preread_match.sextet_census", cen6 == {
        "b_only": pre["rank38"]["sextet_census"]["counts"]["b_only"],
        "zero": pre["rank38"]["sextet_census"]["counts"]["zero"],
        "disjoint":
            pre["rank38"]["sextet_census"]["counts"]["disjoint"]})''',
    r'''    # ---- sextets: the level-6 I-E term breaks open at k=39.
    # The published k=26..k=38 sextet censuses proved C(k,6) all
    # zero for every k <= 38 (zero is superset-closed); at k=39
    # the full C(39,6)=3,262,623 census is 5,852 b_only /
    # 3,256,771 zero / 0 disjoint -- the first non-zero sextet
    # layer ever, all 5,852 containing the rank-39 root -- and
    # the k=39 preread's level-7 closure scan (99,122 candidate
    # monotone 7-extensions of the 5,852 b_only sextets, all
    # zero; commit 848727f1) pins the I-E truncation at level 6.
    j6 = {}
    n6 = 0
    cen6 = {"b_only": 0, "zero": 0, "disjoint": 0}
    dbl6 = {}
    for c in itertools.combinations(range(K), 6):
        n6 += 1
        kind, union = classify(rows, c)
        cen6[kind] += 1
        if kind == "zero":
            j6[c] = {"class": "zero", "joint": 0, "A": 0, "B": 0}
            continue
        if kind == "disjoint":
            raise AssertionError(("disjoint sextet at k=39, but "
                                  "the preread census pins 0", c))
        assert kind == "b_only", (c, kind)
        # the k=26..k=38 censuses were disjoint- and b_only-zero,
        # so every b_only sextet must contain rank-39
        assert IDX38 in c, ("prev-era b_only sextet", c)
        assert c in done6, ("missing new b_only sextet record", c)
        cnt = Counter(r for i in c for r in rows[i])
        d = [r for r, v in cnt.items() if v == 2][0]
        dbl6[d] = dbl6.get(d, 0) + 1
        j6v = done6[c]["joint"]
        j6[c] = {"class": "b_only", "joint": j6v,
                 "A": 0, "B": j6v}
    chk("sextet_census_k39",
        n6 == 3262623 and cen6 == {"b_only": 5852, "zero": 3256771,
                                   "disjoint": 0}, cen6)
    chk("preread_match.sextet_census", cen6 == {
        "b_only": pre["rank39"]["sextet_census"]["counts"]["b_only"],
        "zero": pre["rank39"]["sextet_census"]["counts"]["zero"],
        "disjoint":
            pre["rank39"]["sextet_census"]["counts"]["disjoint"]})
    chk("sextets.double_rows_hist",
        dbl6 == {15: 682, 18: 3147, 19: 2023}, dbl6)
    # every b_only sextet has four b_only 5-subsets and two
    # disjoint 5-subsets (machine-verified for all 5,852)
    sub6_ok = True
    for c in j6:
        if j6[c]["class"] != "b_only":
            continue
        kinds = [j5[tuple(sorted(set(c) - {x}))]["class"] for x in c]
        if sorted(kinds) != ["b_only", "b_only", "b_only",
                            "b_only", "disjoint", "disjoint"]:
            sub6_ok = False
    chk("sextets.subset_structure", sub6_ok)
    chk("sextets.bounds", all(
        j6[c]["joint"] <= min(
            j5[tuple(sorted(set(c) - {x}))]["joint"] for x in c)
        for c in j6 if j6[c]["joint"]))''', 1)

rep(r'''    c3 = done("cross3", lambda e: (tuple(e["combo"]), e["lineage"]))
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
        and all(e["match"] for e in c5.values()))''',
    r'''    c3 = done("cross3", lambda e: (tuple(e["combo"]), e["lineage"]))
    c4 = done("cross4", lambda e: (tuple(e["combo"]), e["lineage"]))
    cq4 = done("crossq4", lambda e: (tuple(e["combo"]),
                                      e["lineage"]))
    c5 = done("cross5", lambda e: (tuple(e["combo"]), e["lineage"]))
    cq5 = done("crossq5", lambda e: (tuple(e["combo"]),
                                      e["lineage"]))
    c6 = done("cross6", lambda e: (tuple(e["combo"]), e["lineage"]))
    chk("cross.triples_2", len(c3) == 2
        and all(e["match"] for e in c3.values()))
    chk("cross.quads_2", len(c4) == 2
        and all(e["match"] for e in c4.values()))
    chk("cross.disjoint_quads_2", len(cq4) == 2
        and all(e["match"] for e in cq4.values()))
    chk("cross.quints_2", len(c5) == 2
        and all(e["match"] for e in c5.values()))
    cq5_ok = len(cq5) == 4
    if cq5_ok:
        by_quint = {}
        for e in cq5.values():
            key = tuple(sorted(e["combo"]))
            by_quint.setdefault(key, {})[e["lineage"]] = e
        keys5 = sorted(by_quint)
        cq5_ok = (len(keys5) == 2)
        for key in keys5:
            by_lin = by_quint[key]
            if not (set(by_lin) == {"lazypm", "mypm"}
                    and by_lin["lazypm"]["joint_A"]
                    == by_lin["mypm"]["joint_A"]
                    and by_lin["lazypm"]["joint_B"]
                    == by_lin["mypm"]["joint_B"]
                    and by_lin["lazypm"]["joint_A"]
                    == by_lin["lazypm"]["ref_A"]
                    and by_lin["lazypm"]["joint_B"]
                    == by_lin["lazypm"]["ref_B"]):
                cq5_ok = False
    chk("cross.disjoint_quints_2x2", cq5_ok)
    chk("cross.sextets_2", len(c6) == 2
        and all(e["match"] for e in c6.values()))''', 1)

rep(r'''    # ---- kill(k) k=1..34 with the fifth-order I-E''',
    r'''    # ---- kill(k) k=1..39 with the sixth-order I-E (the
    #      level-6 term is B-only: j6_A == 0 for every sextet)''', 1)

rep(r'''        for c in itertools.combinations(range(k), 5):
            v += j5[c]["joint"]
            vA += j5[c]["A"]
            vB += j5[c]["B"]
        kill[k] = v''',
    r'''        for c in itertools.combinations(range(k), 5):
            v += j5[c]["joint"]
            vA += j5[c]["A"]
            vB += j5[c]["B"]
        for c in itertools.combinations(range(k), 6):
            v -= j6[c]["joint"]
            vA -= j6[c]["A"]
            vB -= j6[c]["B"]
        kill[k] = v''', 1)

rep(r'''    chk("reproduce_k1_37",
        all(kill[k] == int(k37j["values"]["kill"]["k%d" % k])
            for k in range(1, 38)))
    chk("split.reproduce_k1_37",
        all(killA[k] == int(k37j["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k37j["values"]["kill_B"]["k%d" % k])
            for k in range(1, 38)))''',
    r'''    chk("reproduce_k1_38",
        all(kill[k] == int(k38j["values"]["kill"]["k%d" % k])
            for k in range(1, 39)))
    chk("split.reproduce_k1_38",
        all(killA[k] == int(k38j["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k38j["values"]["kill_B"]["k%d" % k])
            for k in range(1, 39)))''', 1)

rep(r'''    chk("survival.marginal",
        0 <= kill[K] - kill[K - 1] <= mem[K - 1],
        {"k38_minus_k37": str(kill[K] - kill[K - 1]),
         "m38": str(mem[K - 1])})''',
    r'''    chk("survival.marginal",
        0 <= kill[K] - kill[K - 1] <= mem[K - 1],
        {"k39_minus_k38": str(kill[K] - kill[K - 1]),
         "m39": str(mem[K - 1])})''', 1)

rep(r'''    new5 = {c: e for c, e in done5.items()}''',
    r'''    new5 = {c: e for c, e in done5.items()
            if e["class"] == "b_only"}
    new5d = {c: e for c, e in done5.items()
             if e["class"] == "disjoint"}''', 1)

rep(r'''        "schema": "n11-cost16-survival-k38-20261119-v1",''',
    r'''        "schema": "n11-cost16-survival-k39-20261119-v1",''', 1)

rep(r'''        "title": ("Exact survival curve extended to k=38 for the "
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
                  "fifth order"),''',
    r'''        "title": ("Exact survival curve extended to k=39 for the "
                  "31-row cost-16 parent: rank-39 (5,24) has no "
                  "fresh row and no single-sharer row -- both "
                  "rows arrive with exactly two prior sharers "
                  "(row 5 via indices 2 and 25, row 24 via "
                  "indices 4 and 14) and double together for the "
                  "first time in the triple (54 and 46 records), "
                  "quad (391 and 259 records) and quint (763 and "
                  "179 records) layers -- the first generation "
                  "whose double-row family gains two rows at "
                  "once; the new pair census is 4 shared / 34 "
                  "disjoint (the shared pairs are exactly the "
                  "four prior sharers of rows 5 and 24), 1,009 "
                  "new disjoint quads extend the A-type 4-way "
                  "term to 2,686, the first disjoint quints ever "
                  "appear (508, all 10-row unions) opening the "
                  "A-type 5-way term, and the sextet layer turns "
                  "non-zero for the first time (5,852 b_only "
                  "among the C(39,6)=3,262,623 6-subsets, all "
                  "containing rank-39) opening the B-type 6-way "
                  "term with the preread level-7 closure pinning "
                  "the I-E truncation at level 6"),''', 1)

rep(r'''            "k38_preread": {"path": K38_PREREAD_REL,
                            "git_blob_sha1": K38_PREREAD_PIN,
                            "commit": K38_PREREAD_COMMIT},''',
    r'''            "k38_preread": {"path": K38_PREREAD_REL,
                            "git_blob_sha1": K38_PREREAD_PIN,
                            "commit": K38_PREREAD_COMMIT},
            "survival_k38_json": {"path": K38_JSON_REL,
                                  "git_blob_sha1": K38_JSON_PIN,
                                  "commit": K38_JSON_COMMIT},
            "k39_preread": {"path": K39_PREREAD_REL,
                            "git_blob_sha1": K39_PREREAD_PIN,
                            "commit": K39_PREREAD_COMMIT},''', 1)

rep(r'''            "rank38_root": {"root": top[IDX38]["root"],
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
                                    "partners"},''',
    r'''            "rank39_root": {"root": top[IDX38]["root"],
                            "rows": list(rows[IDX38]),
                            "membership": str(mem[IDX38]),
                            "a_part": str(ap[IDX38]),
                            "b_part": str(bp[IDX38]),
                            "note": "rank-39 (5,24): the first "
                                    "two-sharer/two-sharer root "
                                    "with no fresh row and no "
                                    "single-sharer row (row 5 "
                                    "has the prior sharers "
                                    "index 2 = the rank-3 root "
                                    "(5,19) and index 25 = the "
                                    "rank-26 root (5,16); row "
                                    "24 has index 4 = the "
                                    "rank-5 root (18,24) and "
                                    "index 14 = the rank-15 root "
                                    "(15,24)); 4 shared and 34 "
                                    "disjoint partners"},''', 1)

rep(r'''            "preread_exact_integers": (
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
                         "preread_match.* finalize checks"}),"triple_census_k38": cen,''',
    r'''            "preread_exact_integers": (
                {"note": "the k=39 preread (commit 848727f1) is "
                         "pure Python with exact integer "
                         "serialization (same toolchain as the "
                         "k=32/k=33/k=34/k=35/k=36/k=37/k=38 "
                         "prereads, commits 490a3e44 / 67068e07 / "
                         "2a14f351 / 90fc51c9 / 67985e92c9 / "
                         "98321003 / 75fabfd0), it carries 35 "
                         "checks all pass, and it needs no "
                         "big-integer erratum; its "
                         "membership/a_part/b_part "
                         "(119883868794265826 / 91824665662421012 "
                         "/ 28059203131844814) equal the pinned "
                         "aggregate exactly (asserted at load); "
                         "the structural fields (rows, hex, prior "
                         "hit indices, censuses, histograms, the "
                         "disjoint quint/sextet tallies, the "
                         "level-7 septet closure) are "
                         "cross-checked at load and by the "
                         "preread_match.* finalize checks"}),
            "triple_census_k39": cen,''', 1)

rep(r'''            "new_quint_census": {"b_only": 2868, "zero": 63177,
                                 "disjoint": 0},''',
    r'''            "new_quint_census": {"b_only": 13658,
                                 "zero": 59649,
                                 "disjoint": 508},''', 1)

rep(r'''            "quint_census_k38": cen5,''',
    r'''            "quint_census_k39": cen5,''', 1)

rep(r'''            "new_quad_b_only_double_row_histogram": (
                {"note": "row 29 doubles here for the first time "
                         "in the quad layer (11 records; single "
                         "prior sharer, the same single-share "
                         "pattern as row 7 at rank-33, row 9 at "
                         "rank-34 and row 8 at rank-37), while "
                         "row 19 is the dominant new double row "
                         "(1,339 of the 2,519 new b_only quads), "
                         "machine-derived from the computed new "
                         "quads in this finalize",
                 "histogram": quad_dbl_hist}),''',
    r'''            "new_quad_b_only_double_row_histogram": (
                {"note": "rows 5 and 24 double here for the first "
                         "time in the quad layer (391 and 259 "
                         "records, the first generation with two "
                         "new double rows at once), while row 19 "
                         "stays the dominant new double row "
                         "(1,257 of the 4,398 new b_only quads) "
                         "and row 18 follows with 1,965, "
                         "machine-derived from the computed new "
                         "quads in this finalize",
                 "histogram": quad_dbl_hist}),''', 1)

rep(r'''            "new_triple_b_only_double_row_histogram": (
                {"note": "computed fact: 120 of the 420 new b_only "
                         "triples double row 18, 269 double "
                         "row 19 and 8 double row 29 (row 29's "
                         "first doubling, mirroring row 7 at "
                         "rank-33, row 9 at rank-34 and row 8 at "
                         "rank-37); rows 21 and 22 never double",
                 "histogram": triple_dbl_hist}),''',
    r'''            "new_triple_b_only_double_row_histogram": (
                {"note": "computed fact: 120 of the 319 new b_only "
                         "triples double row 18, 66 double row 19 "
                         "and rows 5 and 24 double here for the "
                         "first time in the triple layer (54 and "
                         "46 records, the first generation with "
                         "two new double rows at once), alongside "
                         "15 records of row 15",
                 "histogram": triple_dbl_hist}),''', 1)

rep(r'''            "sextet_census_k38": cen6,''',
    r'''            "sextet_census_k39": cen6,
            "new_sextet_census": {"b_only": 5852, "zero": 496090,
                                  "disjoint": 0},
            "quint_disjoint_count": 508,
            "quint_disjoint_union_sizes": {"10": 508},
            "sextet_b_only_double_rows": dbl6,
            "septet_zero_closure": (
                {"note": "the k=39 preread level-7 closure scan "
                         "(commit 848727f1) enumerated the "
                         "99,122 candidate monotone 7-extensions "
                         "of the 5,852 b_only sextets and found "
                         "all zero (non_zero_class_seven_combos "
                         "== 0), pinning the marginal I-E "
                         "truncation at level 6"}),''', 1)

rep(r'''            "quints_zero_synth_count": 63177,''',
    r'''            "quints_zero_synth_count": 59649,''', 1)

rep(r'''            "quints_jsonl_note": ("zero quints are structural "
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
                                  "justification)"),''',
    r'''            "quints_jsonl_note": ("zero quints are structural "
                                  "(classify from the pinned "
                                  "aggregate) and are not appended "
                                  "to the JSONL; finalize "
                                  "reclassifies all 575,757 "
                                  "5-subsets and asserts the exact "
                                  "census and the presence of every "
                                  "b_only and disjoint record; the "
                                  "full C(39,6)=3,262,623 sextet "
                                  "census is reclassified and "
                                  "asserted at 5,852 b_only / "
                                  "3,256,771 zero / 0 disjoint "
                                  "(level-6 truncation "
                                  "justification)"),''', 1)

rep(r'''            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
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
                             "structurally zero (sextet_census_k38)"),''',
    r'''            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
                             "sum j4 + sum j5 - sum j6 for "
                             "k <= 39; kill_A(k) = sum a - "
                             "sum j2_A + sum j3_A - sum j4_A + "
                             "sum j5_A (j6_A == 0); kill_B(k) = "
                             "sum b - sum j2_B + sum j3_B - "
                             "sum j4_B + sum j5_B - sum j6_B; "
                             "j4_A comes from the 2,686 disjoint "
                             "quads (1,677 published at k=38, "
                             "1,009 new at k=39), j5_A from the "
                             "508 new disjoint quints at "
                             "|union|=10 (the first disjoint "
                             "quints ever), j5_B from the 36,682 "
                             "b_only quints (23,024 prev, 13,658 "
                             "new), j6_B from the 5,852 new b_only "
                             "sextets; the seventh order stays "
                             "structurally zero "
                             "(septet_zero_closure)"),''', 1)

rep(r'''            "formulas": {
                "j4_A_disjoint": ("sum_{s not in union} w1[s] * "
                                  "pm(V \\ union \\ {s}) at "
                                  "|union|=8, same union-mask "
                                  "machinery as k=14, validated by "
                                  "anchor regression and both pm "
                                  "lineages"),
                "j4_B_disjoint": ("two-case (doubled row inside / "
                                  "outside the union) at |union|=8"),
                "j5_B_b_only": ("pm(V \\ union) on the 22-row "
                               "residual, the b_only-quad pattern"),''',
    r'''            "formulas": {
                "j4_A_disjoint": ("sum_{s not in union} w1[s] * "
                                  "pm(V \\ union \\ {s}) at "
                                  "|union|=8, same union-mask "
                                  "machinery as k=14, validated by "
                                  "anchor regression and both pm "
                                  "lineages"),
                "j4_B_disjoint": ("two-case (doubled row inside / "
                                  "outside the union) at |union|=8"),
                "j5_A_disjoint": ("sum_{s not in union} w1[s] * "
                                  "pm(V \\ union \\ {s}) at "
                                  "|union|=10, the same union-mask "
                                  "machinery extended one level "
                                  "(no published |union|>8 record "
                                  "exists to anchor on: re-anchored "
                                  "on the published |union|=8 chain "
                                  "and cross-checked with both pm "
                                  "lineages, crossq5)"),
                "j5_B_b_only": ("pm(V \\ union) on the 22-row "
                                "residual, the b_only-quad pattern"),
                "j6_B_b_only": ("pm(V \\ union) on the 20-row "
                                "residual for the 5,852 b_only "
                                "sextets (11-row unions)"),''', 1)

rep(r'''            "marginal_k38": str(kill[K] - kill[K - 1]),''',
    r'''            "marginal_k39": str(kill[K] - kill[K - 1]),''', 1)

rep(r'''                for c in sorted(new5)},
        },''',
    r'''                for c in sorted(new5)},
            "new_quints_disjoint": {
                "%d,%d,%d,%d,%d" % c: {"class": "disjoint",
                                        "union": done5[c]["union"],
                                        "joint_A": str(j5[c]["A"]),
                                        "joint_B": str(j5[c]["B"]),
                                        "joint": str(j5[c]["joint"])}
                for c in sorted(new5d)},
            "new_sextets_b_only": {
                "%d,%d,%d,%d,%d,%d" % c: {"class": "b_only",
                                          "union": done6[c]["union"],
                                          "joint_A": "0",
                                          "joint_B": str(j6[c]["B"]),
                                          "joint": str(j6[c]["joint"])}
                for c in sorted(done6)},
        },''', 1)

rep(r'''    if mode == "quints":
        sl = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return mode_quints(sl)
    if mode == "anchor":''',
    r'''    if mode == "quints":
        sl = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return mode_quints(sl)
    if mode == "sextets":
        sl = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return mode_sextets(sl)
    if mode == "anchor":''', 1)

rep(r'''    print("usage: pairs [BUDGET] | triples [SLICE] | quads [SLICE] | "
          "quints [SLICE] | anchor | cross | finalize")''',
    r'''    print("usage: pairs [BUDGET] | triples [SLICE] | quads [SLICE] | "
          "quints [SLICE] | sextets [SLICE] | anchor | cross | "
          "finalize")''', 1)

rep(r'''IDX38''',
    r'''IDX39''', 42)

rep(r'''load_top38''',
    r'''load_top39''', 9)


def sub(src):
    for old, new, count in reps:
        got = src.count(old)
        if got != count:
            raise SystemExit(f"FAIL anchor x{got} != {count}: {old[:100]!r}")
        src = src.replace(old, new)
    return src


def main() -> int:
    src = open(SRC, encoding="utf-8").read()
    base_bytes = open(SRC, "rb").read()
    blob = hashlib.sha1(b"blob %d\x00" % len(base_bytes)
                  + base_bytes).hexdigest()
    sha256 = hashlib.sha256(base_bytes).hexdigest()
    if blob != EXPECT_BASE_BLOB:
        raise SystemExit(f"FAIL base blob {blob}")
    if sha256 != EXPECT_BASE_SHA256:
        raise SystemExit(f"FAIL base sha256 {sha256}")
    out = sub(src)
    # residual sanity probes
    for stale in (
                  'IDX38',
                  'M38',
                  'load_top38',
                  'load_k38_base',
                  'pre["rank38"]["',
                  'k37ja',
                  'reproduce_k1_37',
                  '"marginal_k38"',
                  '"triple_census_k38"',
                  '"quint_census_k38"',
                  '"sextet_census_k38"',
                  'quints.census_501942',
                  'done %d/37',
                  'done %d/666',
                  '%d/7770',
                  'len(combos) == 666',
                  'len(combos) == 7770',
                  'len(combos) == 66045',
                  '== 20156',
                  'quints_zero_synth_count\\": 63177',
    ):
        if stale in out:
            raise SystemExit(f"FAIL stale token {stale!r} survived")
    assert out.count("119940649042609991") == 2, \
        out.count("119940649042609991")
    assert out.count("119883868794265826") == 3
    open(DST, "w", encoding="utf-8").write(out)
    data = open(DST, "rb").read()
    print("wrote", DST, len(data), "bytes")
    print("git_blob_sha1:", hashlib.sha1(
        b"blob %d\x00" % len(data) + data).hexdigest())
    print("sha256:", hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())

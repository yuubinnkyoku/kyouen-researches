#!/usr/bin/env python3
"""Machine transformation: k=36 published survival script -> k=37.

Anchored stepwise replacements, every replacement with an exact
expected occurrence count; the script aborts on any mismatch so
the output file is only written when the whole chain succeeds.
Facts come from the pinned k=37 preread JSON (commit 98321003,
blob b98ed685) and the pinned k=36 result JSON (commit 6fcea02c,
blob b7a78e79).

Rebuild note (sandbox reset 2026-11-19 03:42Z): this file is the
identical final version of the original transform; the generated
k37 script must again be byte-identical to the pre-reset one
(100,932 bytes; the pre-reset run already produced 46 verified
records: 10 anchor + 36 pairs, checkpointed in artifacts/k37).
"""
import sys

SRC = "exp/cost16_survival_k36_20261118.py"
DST = "exp/cost16_survival_k37_20261119.py"

text = open(SRC, encoding="utf-8").read()
fails = []


def rep(old, new, n, name):
    global text
    got = text.count(old)
    if got != n:
        fails.append((name, old[:70], got, n))
        return
    text = text.replace(old, new)


def splice(start, end, new, name):
    """Replace text[start:end) (by markers) with new."""
    global text
    if text.count(start) != 1 or text.count(end) != 1:
        fails.append((name, "marker not unique", text.count(start),
                      text.count(end)))
        return
    i = text.index(start)
    j = text.index(end)
    if j <= i:
        fails.append((name, "end before start", 0, 0))
        return
    text = text[:i] + new + text[j:]


# ---- phase 1: module docstring
i0 = text.index('"""')
i1 = text.index('"""', i0 + 3) + 3
NEW_DOC = '''"""Survival-curve extension to k=37 for the 31-row cost-16 parent
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
"""
'''
text = text[:i0] + NEW_DOC + text[i1:]

# ---- phase 2: constants
rep("K = 36\n", "K = 37\n", 1, "K")
rep("# site); K=36 bans 36 pair roots drawn from it.  A wrong R",
    "# site); K=37 bans 37 pair roots drawn from it.  A wrong R",
    1, "K-comment")
rep("IDX36 = 35\n", "IDX37 = 36\n", 1, "IDX-def")
rep('''K36_PREREAD_REL = EXP_REL + "cost16-survival-k36-preread-20261118.json"
K36_PREREAD_PIN = "760aa396361cc7d2ea8bc371f4dd673d962f07fe"
K36_PREREAD_COMMIT = "67985e92c9"
''', '''K36_JSON_REL = EXP_REL + "cost16-survival-k36-20261118.json"
K36_JSON_PIN = "b7a78e79bdc82c8097222ef2fd057e6b1a4b9350"
K36_JSON_COMMIT = "6fcea02c"
K37_PREREAD_REL = EXP_REL + "cost16-survival-k37-preread-20261119.json"
K37_PREREAD_PIN = "b98ed685e772eacbd28dc3100e9813e81c27040a"
K37_PREREAD_COMMIT = "98321003"
''', 1, "preread-pins")
rep('''RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k36-20261118.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k36-20261118.json")''',
    '''RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k37-20261119.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k37-20261119.json")''',
    1, "res-paths")
rep("M36 = 120046727515486665", "M37 = 119973409932394637", 1, "M-def")

# ---- phase 3: load_top37 root asserts (span A)
SPAN_A_START = '    # rank-36 root: (19,22), the first root to cover row 22; row'
SPAN_A_END = '    total = agg["derived"]["total_minimum_covers"]'
SPAN_A_NEW = '''    # rank-37 root: (8,19), the first root ever to double row 8;
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
            if 8 in top[i]["rows_covered"]] == [23]
'''
splice(SPAN_A_START, SPAN_A_END, SPAN_A_NEW, "spanA")

# ---- phase 4: load_top37 preread asserts (span B)
SPAN_B_START = '    # preread structural pins (commit 67985e92c9); the k=36'
SPAN_B_END = '    return agg, top, memA, memB, total, A16, B16, pre'
SPAN_B_NEW = '''    # preread structural pins (commit 98321003); the k=37
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
                                              "disjoint": 0}
    # rank-36 regression layer of the k=37 preread (machine
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
    assert r35["mismatches"] == 0
'''
splice(SPAN_B_START, SPAN_B_END, SPAN_B_NEW, "spanB")

# ---- phase 5: load_k37_base
rep('''def load_k36_base():
    """595 pairwise joints, 6,545 triples, the 51,645 stored quads
    and the 14,599 b_only quints among the top-35, from the pinned
    k14..k34 publications plus the pinned k=35 result."""''',
    '''def load_k37_base():
    """630 pairwise joints, 7,140 triples, the 58,190 stored quads
    and the 17,434 b_only quints among the top-36, from the pinned
    k14..k35 publications plus the pinned k=36 result."""''',
    1, "base-docstring")
rep('''    assert len(quads) == 51645
    quints26 = {}''',
    '''    assert len(quads) == 51645
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
    quints26 = {}''', 1, "k36-era-block")
rep('''    assert all(34 in c and 35 not in c for c in quints35)
    quints_prev = {}''',
    '''    assert all(34 in c and 35 not in c for c in quints35)
    quints36 = {}
    for key, v in k36j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints36[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints36) == 2835
    assert all(35 in c and 36 not in c for c in quints36)
    quints_prev = {}''', 1, "quints36-block")
rep('''    quints_prev.update(quints34)
    quints_prev.update(quints35)
    assert len(quints_prev) == 14599''',
    '''    quints_prev.update(quints34)
    quints_prev.update(quints35)
    quints_prev.update(quints36)
    assert len(quints_prev) == 17434''', 1, "quints-prev-17434")
rep('''        k24, k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, \\
        pairs, triples, quads, quints_prev''',
    '''        k24, k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \\
        pairs, triples, quads, quints_prev''', 1, "base-return")
rep('''    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \\
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, \\
        pairs_prev, triples_prev, quads_prev, quints_prev \\
        = load_k36_base()''',
    '''    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \\
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, k36j, \\
        pairs_prev, triples_prev, quads_prev, quints_prev \\
        = load_k36_base()''', 1, "finalize-unpack")

# ---- phase 6: mode functions
rep('    print("[pairs] todo %d (done %d/35)" % (len(todo), len(donep)),',
    '    print("[pairs] todo %d (done %d/36)" % (len(todo), len(donep)),',
    1, "pairs-todo-print")
rep('    print("[pairs] done %d/35" % len(done("pair",',
    '    print("[pairs] done %d/36" % len(done("pair",',
    1, "pairs-done-print")
rep("    assert len(combos) == 595", "    assert len(combos) == 630",
    1, "triples-assert")
rep('    print("[triples] slice %d done, done %d/595 in %.1fs"',
    '    print("[triples] slice %d done, done %d/630 in %.1fs"',
    1, "triples-print")
rep("    assert len(combos) == 6545", "    assert len(combos) == 7140",
    1, "quads-assert")
rep('    print("[quads] slice %d done, done %d/6545"',
    '    print("[quads] slice %d done, done %d/7140"',
    1, "quads-print")
rep('''    """B-type-only 5-way joints for the 2,835 new b_only quints
    (the 14,599 prev-era records load from the pinned
    k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35 JSONs).
    Zero''',
    '''    """B-type-only 5-way joints for the 2,722 new b_only quints
    (the 17,434 prev-era records load from the pinned
    k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35/k=36
    JSONs).  Zero''', 1, "quints-docstring")
rep("    assert len(combos) == 52360", "    assert len(combos) == 58905",
    1, "quints-assert")
rep('    print("[quints] slice %d done, done %d/2835b_only in %.1fs"',
    '    print("[quints] slice %d done, done %d/2722b_only in %.1fs"',
    1, "quints-print")
rep('''    """Pre-production validation of disjoint_joint at |union|=4
    (published k13-era pair joints, both pm lineages), |union|=6
    (2 published k35 disjoint triples) and |union|=8 (2 published
    k35 disjoint quads, both pm lineages with exact A/B match
    against the pinned publication).  The |union|=8 machinery was
    introduced at k=26 and extended by the k=27/k=28/k=29/k=30/
    k=31/k=32/k=33/k=34/k=35 publications (1,195 production
    records); this re-anchors it on published records before
    production."""''',
    '''    """Pre-production validation of disjoint_joint at |union|=4
    (published k13-era pair joints, both pm lineages), |union|=6
    (2 published k36 disjoint triples) and |union|=8 (2 published
    k36 disjoint quads, both pm lineages with exact A/B match
    against the pinned publication).  The |union|=8 machinery was
    introduced at k=26 and extended by the k=27/k=28/k=29/k=30/
    k=31/k=32/k=33/k=34/k=35/k=36 publications (1,363 production
    records); this re-anchors it on published records before
    production."""''', 1, "anchor-docstring")
rep("    k35ja = json.loads(base.read_pinned(K35_JSON_REL, K35_JSON_PIN))",
    "    k36ja = json.loads(base.read_pinned(K36_JSON_REL, K36_JSON_PIN))",
    1, "anchor-k36ja-load")
rep("k35ja", "k36ja", 4, "anchor-k36ja-refs")

# ---- phase 7: finalize checks
rep("    # ---- pairs (595 + 35 = 630)",
    "    # ---- pairs (630 + 36 = 666)", 1, "pairs-comment")
rep('    chk("pairs.prev_595", len(pairs_prev) == 595)',
    '    chk("pairs.prev_630", len(pairs_prev) == 630)', 1, "prev-pairs")
rep('    chk("pairs.new_35", len(donep) == 35)',
    '    chk("pairs.new_36", len(donep) == 36)', 1, "new-pairs")
rep('    chk("pairs.complete_630", len(j2) == 630)',
    '    chk("pairs.complete_666", len(j2) == 666)', 1, "complete-pairs")
rep("        len(shared_new) == 10 and len(donep) - len(shared_new) == 25,",
    "        len(shared_new) == 12 and len(donep) - len(shared_new) == 24,",
    1, "pairs-census")
rep("    # ---- triples (6545 + 595 = 7140)",
    "    # ---- triples (7140 + 630 = 7770)", 1, "triples-comment")
rep('    chk("triples.prev_6545", len(j3) == 6545)',
    '    chk("triples.prev_7140", len(j3) == 7140)', 1, "prev-triples")
rep('    chk("triples.new_595", len(donet) == 595)',
    '    chk("triples.new_630", len(donet) == 630)', 1, "new-triples")
rep('    chk("triples.complete_7140", len(j3) == 7140)',
    '    chk("triples.complete_7770", len(j3) == 7770)', 1, "complete-triples")
rep('        cen == {"b_only": 4361, "zero": 1320, "disjoint": 1459}, cen)',
    '        cen == {"b_only": 4758, "zero": 1420, "disjoint": 1592}, cen)',
    1, "triple-census")
rep("    # ---- quads (52360 prev + 6545 new = 58905)",
    "    # ---- quads (58905 prev + 7140 new = 66045)", 1, "quads-comment")
rep('''    chk("quads.prev_52360_stored_51645",
        len(j4) == 52360 and len(quads_prev) == 51645,''',
    '''    chk("quads.prev_58905_stored_58190",
        len(j4) == 58905 and len(quads_prev) == 58190,''',
    1, "prev-quads")
rep('    chk("quads.new_6545", len(doneq) == 6545)',
    '    chk("quads.new_7140", len(doneq) == 7140)', 1, "new-quads")
rep('    chk("quads.complete_58905", len(j4) == 58905)',
    '    chk("quads.complete_66045", len(j4) == 66045)', 1, "complete-quads")
rep('        qcen == {"b_only": 2458, "zero": 3919, "disjoint": 168},',
    '        qcen == {"b_only": 2394, "zero": 4589, "disjoint": 157},',
    1, "quad-census")
rep('    chk("quads.prev_disjoint_1195", len(prev_disjoint) == 1195)',
    '    chk("quads.prev_disjoint_1363", len(prev_disjoint) == 1363)',
    1, "prev-disjoint")
rep('''    # new b_only quads double-row histogram (machine-derived;
    # row 22 cannot double (zero prior sharers among the top-35);
    # rows 18 and 19 are the dominant new double rows (992 and
    # 1,150 of the 2,458 new b_only quads), while the four hub
    # rows keep their families); the b_only triple double-row
    # histogram is recorded as a computed fact too''',
    '''    # new b_only quads double-row histogram (machine-derived;
    # row 8 doubles here for the first time in the quad layer
    # (11 records; single prior sharer index 23 -- the same
    # single-share doubling pattern as row 7 at rank-33 and row
    # 9 at rank-34), while row 19 is the dominant new double
    # row (1,214 of the 2,394 new b_only quads)); the b_only
    # triple double-row histogram is recorded as a computed
    # fact too''',
    1, "quad-hist-comment")
rep('''        triple_dbl_hist == {0: 1, 4: 1, 15: 15, 16: 3,
                            18: 136, 19: 232, 23: 1, 24: 1, 30: 1},''',
    '''        triple_dbl_hist == {0: 1, 4: 1, 8: 8, 15: 15, 16: 3,
                            18: 120, 19: 246, 23: 1, 24: 1, 30: 1},''',
    1, "triple-dbl-hist")
rep('''    chk("quads.new_b_only_double_row_22_absent",
        quad_dbl_hist.get(22, 0) == 0, quad_dbl_hist)''',
    '''    chk("quads.new_b_only_double_row_8_first_quad_doubling",
        quad_dbl_hist.get(8, 0) == 11, quad_dbl_hist)''',
    1, "quad-8-first-doubling")
rep('''        quad_dbl_hist == {0: 16, 4: 2, 15: 260, 16: 32,
                          18: 992, 19: 1150, 23: 2, 24: 2, 30: 2},''',
    '''        quad_dbl_hist == {0: 15, 4: 2, 8: 11, 15: 245, 16: 31,
                          18: 870, 19: 1214, 23: 2, 24: 2, 30: 2},''',
    1, "quad-dbl-hist")
rep('''    # ---- quints (310,033 top-35 zeros + 14,599 prev b_only +
    #      49,525 new zeros + 2,835 new b_only = 376,992)''',
    '''    # ---- quints (359,558 top-36 zeros + 17,434 prev b_only +
    #      56,183 new zeros + 2,722 new b_only = 435,897)''',
    1, "quints-comment")
rep('''    chk("quints.census_376992",
        n5 == 376992 and cen5 == {"b_only": 17434, "zero": 359558,
                                  "disjoint": 0},''',
    '''    chk("quints.census_435897",
        n5 == 435897 and cen5 == {"b_only": 20156, "zero": 415741,
                                  "disjoint": 0},''',
    1, "quint-census")
rep("        dbl_hist == {15: 2785, 16: 545, 18: 9217, 19: 4887},",
    "        dbl_hist == {15: 3124, 16: 616, 18: 10260, 19: 6156},",
    1, "dbl-hist")
rep('''    chk("quints.prev_census_matches_k35",
        prev_cen5 == {"b_only": 14599, "zero": 310033,
                     "disjoint": 0},''',
    '''    chk("quints.prev_census_matches_k36",
        prev_cen5 == {"b_only": 17434, "zero": 359558,
                     "disjoint": 0},''',
    1, "prev-census5")
rep('    chk("quints.new_records_2835", len(done5) == 2835)',
    '    chk("quints.new_records_2722", len(done5) == 2722)', 1, "new5-records")
# naming repair: the published k=36 script kept the stale chk
# name "new_b_only_contain_rank35" while its content already
# checked IDX36; the k=37 transform fixes the name to the rank
# the content actually checks
rep('    chk("quints.new_b_only_contain_rank35", all(',
    '    chk("quints.new_b_only_contain_rank37", all(',
    1, "contain-name")
rep("        and 32 not in c and 33 not in c and 34 not in c))",
    "        and 32 not in c and 33 not in c and 34 not in c\n"
    "        and 35 not in c))", 1, "contain1")
rep('    chk("quints.prev_b_only_contain_rank26_through_35", all(',
    '    chk("quints.prev_b_only_contain_rank26_through_36", all(',
    1, "contain2-name")
rep("        or (33 in c) or (34 in c)\n",
    "        or (33 in c) or (34 in c) or (35 in c)\n", 1, "contain2")
rep('''    # new-era b_only quints never double row 22: row 22 has
    # zero prior sharers among the top-35 (the rank-36 root
    # is its first and so far only member), so it cannot
    # double in any layer; the new-era double-row histogram
    # stays within the four hub rows 15/16/18/19
    # (machine-derived from the 2,835 computed records; the
    # preread new_quint histogram agrees)''',
    '''    # new-era b_only quints never double row 8: row 8 has a
    # single prior sharer among the top-36 (index 23), so its
    # first doublings stay in the triple layer (8 records) and
    # the quad layer (11 records) and never reach the quint
    # layer (the same single-share doubling pattern as row 7
    # at rank-33 and row 9 at rank-34); the new-era double-row
    # histogram stays within the four hub rows 15/16/18/19
    # (machine-derived from the 2,722 computed records; the
    # preread new_quint histogram agrees)''',
    1, "new5-dbl-comment")
rep('''    chk("quints.new_era_double_row_22_absent",
        new5_dbl == {15: 364, 16: 76, 18: 1200, 19: 1195}, new5_dbl)''',
    '''    chk("quints.new_era_double_row_8_absent",
        new5_dbl == {15: 339, 16: 71, 18: 1043, 19: 1269}, new5_dbl)''',
    1, "new5-dbl")
rep('''    # ---- sextets: the quint-order I-E truncation stays closed at
    # k=36.  The published sextet census (commit 583b0bf1) proved
    # C(26,6)/C(27,6)/C(28,6) all zero, and the k=29/k=30/k=31/
    # k=32/k=33/k=34/k=35 publications reclassified C(29,6)/
    # C(30,6)/C(31,6)/C(32,6)/C(33,6)/C(34,6)/C(35,6) all zero
    # (zero is superset-closed); a 6-subset of the top-36 either
    # lies inside the top-35 (already zero) or contains the
    # rank-36 root, so the full C(36,6) reclassification here
    # closes the k=36 truncation (also cross-checked against
    # the k=36 preread sextet census, commit 67985e92c9).''',
    '''    # ---- sextets: the quint-order I-E truncation stays closed at
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
    1, "sextet-comment")
rep('''    chk("sextet_census_k36",
        n6 == 1947792 and cen6 == {"b_only": 0, "zero": 1947792,
                                   "disjoint": 0}, cen6)''',
    '''    chk("sextet_census_k37",
        n6 == 2324784 and cen6 == {"b_only": 0, "zero": 2324784,
                                   "disjoint": 0}, cen6)''',
    1, "sextet-census")
rep('''    chk("reproduce_k1_35",
        all(kill[k] == int(k35j["values"]["kill"]["k%d" % k])
            for k in range(1, 36)))
    chk("split.reproduce_k1_35",
        all(killA[k] == int(k35j["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k35j["values"]["kill_B"]["k%d" % k])
            for k in range(1, 36)))''',
    '''    chk("reproduce_k1_36",
        all(kill[k] == int(k36j["values"]["kill"]["k%d" % k])
            for k in range(1, 37)))
    chk("split.reproduce_k1_36",
        all(killA[k] == int(k36j["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k36j["values"]["kill_B"]["k%d" % k])
            for k in range(1, 37)))''',
    1, "reproduce")
rep('''        {"k36_minus_k35": str(kill[K] - kill[K - 1]),
         "m36": str(mem[K - 1])})''',
    '''        {"k37_minus_k36": str(kill[K] - kill[K - 1]),
         "m37": str(mem[K - 1])})''',
    1, "marginal-detail")

# ---- phase 8: output JSON
rep('''        "schema": "n11-cost16-survival-k36-20261119-v1",
        "date": "2026-11-19",''',
    '''        "schema": "n11-cost16-survival-k37-20261119-v1",
        "date": "2026-11-19",''', 1, "schema-date")
rep('''        "title": ("Exact survival curve extended to k=36 for the "
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
                  "closed at the fifth order"),''',
    '''        "title": ("Exact survival curve extended to k=37 for the "
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
    1, "title")
rep('''            "k36_preread": {"path": K36_PREREAD_REL,
                            "git_blob_sha1": K36_PREREAD_PIN,
                            "commit": K36_PREREAD_COMMIT},''',
    '''            "survival_k36_json": {"path": K36_JSON_REL,
                                  "git_blob_sha1": K36_JSON_PIN,
                                  "commit": K36_JSON_COMMIT},
            "k37_preread": {"path": K37_PREREAD_REL,
                            "git_blob_sha1": K37_PREREAD_PIN,
                            "commit": K37_PREREAD_COMMIT},''',
    1, "inputs-block")
rep('''            "rank36_root": {"root": top[IDX36]["root"],
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
                                    "partners"},''',
    '''            "rank37_root": {"root": top[IDX37]["root"],
                            "rows": list(rows[IDX37]),
                            "membership": str(mem[IDX37]),
                            "a_part": str(ap[IDX37]),
                            "b_part": str(bp[IDX37]),
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
    1, "rank-root-block")
rep('''                {"note": "the k=36 preread (commit 67985e92c9) is "
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
                         "preread_match.* finalize checks"}),''',
    '''                {"note": "the k=37 preread (commit 98321003) is "
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
    1, "preread-note")
rep('"triple_census_k36": cen,', '"triple_census_k37": cen,', 1, "triple-census-out")
rep('"quint_census_k36": cen5,', '"quint_census_k37": cen5,', 1, "quint-census-out")
rep('''            "new_quint_census": {"b_only": 2835, "zero": 49525,
                                 "disjoint": 0},''',
    '''            "new_quint_census": {"b_only": 2722, "zero": 56183,
                                 "disjoint": 0},''',
    1, "new-quint-out")
rep('''                {"note": "row 22 cannot double (zero "
                         "prior sharers); rows 18 and 19 are the "
                         "dominant new double rows (992 and 1,150 "
                         "of the 2,458 new b_only quads), "
                         "machine-derived from the computed new "
                         "quads in this finalize",''',
    '''                {"note": "row 8 doubles here for the first time "
                         "in the quad layer (11 records; single "
                         "prior sharer, the same single-share "
                         "pattern as row 7 at rank-33 and row 9 "
                         "at rank-34), while row 19 is the "
                         "dominant new double row (1,214 of the "
                         "2,394 new b_only quads), "
                         "machine-derived from the computed new "
                         "quads in this finalize",''',
    1, "quad-note-out")
rep('''                {"note": "computed fact: 136 of the 391 new b_only "
                         "triples double row 18 and 232 double "
                         "row 19; row 22 never doubles",''',
    '''                {"note": "computed fact: 120 of the 397 new b_only "
                         "triples double row 18, 246 double "
                         "row 19 and 8 double row 8 (row 8's "
                         "first doubling, mirroring row 7 at "
                         "rank-33 and row 9 at rank-34); rows 21 "
                         "and 22 never double",''',
    1, "triple-note-out")
rep('"sextet_census_k36": cen6,', '"sextet_census_k37": cen6,', 1, "sextet-out")
rep('"quints_zero_synth_count": 49525,', '"quints_zero_synth_count": 56183,',
    1, "zero-synth")
rep('''            "quints_jsonl_note": ("zero quints are structural "
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
                                  "justification)"),''',
    '''            "quints_jsonl_note": ("zero quints are structural "
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
    1, "jsonl-note")
rep('''            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
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
                             "structurally zero (sextet_census_k36)"),''',
    '''            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
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
    1, "ie-mechanism")
rep('"marginal_k36": str(kill[K] - kill[K - 1]),',
    '"marginal_k37": str(kill[K] - kill[K - 1]),', 1, "marginal-out")

# ---- phase 9: global renames
if "IDX36" in text:
    rep("IDX36", "IDX37", text.count("IDX36"), "IDX-rename")
if "load_top36" in text:
    rep("load_top36", "load_top37", text.count("load_top36"),
        "loadtop-rename")
if "load_k36_base" in text:
    rep("load_k36_base", "load_k37_base", text.count("load_k36_base"),
        "loadbase-rename")
rep('pre["rank36"]', 'pre["rank37"]', 13, "preread-rank-refs")

if fails:
    print("FAILED anchors:")
    for f in fails:
        print(" ", f)
    sys.exit(1)

# final sanity: no stale k36-era references outside the intentional
stale = []
for probe, allowed in [("IDX36", 0), ("K36_PREREAD", 0), ("M36", 0),
                       ('pre["rank36"]', 0), ("2835b_only", 0),
                       ("k35ja", 0),
                       ("cost16_survival_k36_20261118.py", 0),
                       ("cost16-survival-k36-20261118.jsonl", 0),
                       # 52360 survives twice in the rank-36
                       # regression-layer quint census asserts
                       ("52360", 2),
                       # the rank-36 regression comment cites the
                       # published k=36 preread commit once and the
                       # preread-note toolchain list cites it once
                       ("67985e92c9", 2)]:
    got = text.count(probe)
    if got != allowed:
        stale.append((probe, got, allowed))
if stale:
    print("STALE references:", stale)
    sys.exit(1)

open(DST, "w", encoding="utf-8").write(text)
print("OK: wrote %s (%d bytes)" % (DST, len(text)))

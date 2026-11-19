#!/usr/bin/env python3
"""Machine transformation: k=35 published survival script -> k=36.

Anchored stepwise replacements, every replacement with an exact
expected occurrence count; the script aborts on any mismatch so
the output file is only written when the whole chain succeeds.
Facts come from the pinned k=36 preread JSON (commit 67985e92c9,
blob 760aa396) and the pinned k=35 result JSON (commit 572b1365b,
blob 80a22ac7).
"""
import sys

SRC = "exp/cost16_survival_k35_20261118.py"
DST = "exp/cost16_survival_k36_20261118.py"

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
NEW_DOC = '''"""Survival-curve extension to k=36 for the 31-row cost-16 parent
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
'''
text = text[:i0] + NEW_DOC + text[i1:]

# ---- phase 2: constants
rep("K = 35\n", "K = 36\n", 1, "K")
rep("# site); K=35 bans 35 pair roots drawn from it.  A wrong R",
    "# site); K=36 bans 36 pair roots drawn from it.  A wrong R",
    1, "K-comment")
rep("IDX35 = 34\n", "IDX36 = 35\n", 1, "IDX-def")
rep('''K35_PREREAD_REL = EXP_REL + "cost16-survival-k35-preread-20261118.json"
K35_PREREAD_PIN = "490fa3a00b8e0b19229c94aa6b1aba4a5604ec13"
K35_PREREAD_COMMIT = "90fc51c991"
''', '''K35_JSON_REL = EXP_REL + "cost16-survival-k35-20261118.json"
K35_JSON_PIN = "80a22ac77cdc0ba0a99643e3f1be13b71565a1b7"
K35_JSON_COMMIT = "572b1365b"
K36_PREREAD_REL = EXP_REL + "cost16-survival-k36-preread-20261118.json"
K36_PREREAD_PIN = "760aa396361cc7d2ea8bc371f4dd673d962f07fe"
K36_PREREAD_COMMIT = "67985e92c9"
''', 1, "preread-pins")
rep('''RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k35-20261118.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k35-20261118.json")''',
    '''RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k36-20261118.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k36-20261118.json")''',
    1, "res-paths")
rep("M35 = 120058481266728720", "M36 = 120046727515486665", 1, "M-def")

# ---- phase 3: load_top36 root asserts (span A)
SPAN_A_START = '    # rank-35 root: (18,21), the first root to cover row 21; row 21'
SPAN_A_END = '    total = agg["derived"]["total_minimum_covers"]'
SPAN_A_NEW = '''    # rank-36 root: (19,22), the first root to cover row 22; row
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
    assert top[IDX36 - 1]["root"] == \\
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
'''
splice(SPAN_A_START, SPAN_A_END, SPAN_A_NEW, "spanA")

# ---- phase 4: load_top36 preread asserts (span B)
SPAN_B_START = '    # preread structural pins (commit 90fc51c991); the k=35 preread'
SPAN_B_END = '    return agg, top, memA, memB, total, A16, B16, pre'
SPAN_B_NEW = '''    # preread structural pins (commit 67985e92c9); the k=36
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
'''
splice(SPAN_B_START, SPAN_B_END, SPAN_B_NEW, "spanB")

# ---- phase 5: load_k36_base
rep('''def load_k35_base():
    """561 pairwise joints, 5,984 triples, the 45,661 stored quads
    and the 13,004 b_only quints among the top-34, from the pinned
    k14..k33 publications plus the pinned k=34 result."""''',
    '''def load_k36_base():
    """595 pairwise joints, 6,545 triples, the 51,645 stored quads
    and the 14,599 b_only quints among the top-35, from the pinned
    k14..k34 publications plus the pinned k=35 result."""''',
    1, "base-docstring")
rep('''    assert len(quads) == 45661
    quints26 = {}''',
    '''    assert len(quads) == 45661
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
    quints26 = {}''', 1, "k35-era-block")
rep('''    assert all(33 in c and 34 not in c for c in quints34)
    quints_prev = {}''',
    '''    assert all(33 in c and 34 not in c for c in quints34)
    quints35 = {}
    for key, v in k35j["values"]["new_quints_b_only"].items():
        c = tuple(int(x) for x in key.split(","))
        quints35[c] = {"class": "b_only", "joint": int(v["joint"]),
                       "union": v["union"]}
    assert len(quints35) == 1595
    assert all(34 in c and 35 not in c for c in quints35)
    quints_prev = {}''', 1, "quints35-block")
rep('''    quints_prev.update(quints34)
    assert len(quints_prev) == 13004''',
    '''    quints_prev.update(quints34)
    quints_prev.update(quints35)
    assert len(quints_prev) == 14599''', 1, "quints-prev-14599")
rep('''        k24, k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, \\
        pairs, triples, quads, quints_prev''',
    '''        k24, k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, \\
        pairs, triples, quads, quints_prev''', 1, "base-return")
rep('''    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \\
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, \\
        pairs_prev, triples_prev, quads_prev, quints_prev \\
        = load_k35_base()''',
    '''    k13, k14, k15, k16, k17, k18, k19, k20, k21, k22, k23, k24, \\
        k25, k26, k27, k28, k29, k30, k31j, k32j, k33j, k34j, k35j, \\
        pairs_prev, triples_prev, quads_prev, quints_prev \\
        = load_k35_base()''', 1, "finalize-unpack")

# ---- phase 6: mode functions
rep('    print("[pairs] todo %d (done %d/34)" % (len(todo), len(donep)),',
    '    print("[pairs] todo %d (done %d/35)" % (len(todo), len(donep)),',
    1, "pairs-todo-print")
rep('    print("[pairs] done %d/34" % len(done("pair",',
    '    print("[pairs] done %d/35" % len(done("pair",',
    1, "pairs-done-print")
rep("    assert len(combos) == 561", "    assert len(combos) == 595",
    1, "triples-assert")
rep('    print("[triples] slice %d done, done %d/561 in %.1fs"',
    '    print("[triples] slice %d done, done %d/595 in %.1fs"',
    1, "triples-print")
rep("    assert len(combos) == 5984", "    assert len(combos) == 6545",
    1, "quads-assert")
rep('    print("[quads] slice %d done, done %d/5984"',
    '    print("[quads] slice %d done, done %d/6545"',
    1, "quads-print")
rep('''    """B-type-only 5-way joints for the 1,595 new b_only quints
    (the 13,004 prev-era records load from the pinned
    k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34 JSONs).  Zero''',
    '''    """B-type-only 5-way joints for the 2,835 new b_only quints
    (the 14,599 prev-era records load from the pinned
    k=26/k=27/k=28/k=29/k=30/k=31/k=32/k=33/k=34/k=35 JSONs).
    Zero''', 1, "quints-docstring")
rep("    assert len(combos) == 46376", "    assert len(combos) == 52360",
    1, "quints-assert")
rep('    print("[quints] slice %d done, done %d/1595b_only in %.1fs"',
    '    print("[quints] slice %d done, done %d/2835b_only in %.1fs"',
    1, "quints-print")
rep('''    """Pre-production validation of disjoint_joint at |union|=4
    (published k13-era pair joints, both pm lineages), |union|=6
    (2 published k34 disjoint triples) and |union|=8 (2 published
    k34 disjoint quads, both pm lineages with exact A/B match
    against the pinned publication).  The |union|=8 machinery was
    introduced at k=26 and extended by the k=27/k=28/k=29/k=30/
    k=31/k=32/k=33/k=34 publications (1,112 production
    records); this re-anchors it on published records before
    production."""''',
    '''    """Pre-production validation of disjoint_joint at |union|=4
    (published k13-era pair joints, both pm lineages), |union|=6
    (2 published k35 disjoint triples) and |union|=8 (2 published
    k35 disjoint quads, both pm lineages with exact A/B match
    against the pinned publication).  The |union|=8 machinery was
    introduced at k=26 and extended by the k=27/k=28/k=29/k=30/
    k=31/k=32/k=33/k=34/k=35 publications (1,195 production
    records); this re-anchors it on published records before
    production."""''', 1, "anchor-docstring")
rep("    k34ja = json.loads(base.read_pinned(K34_JSON_REL, K34_JSON_PIN))",
    "    k35ja = json.loads(base.read_pinned(K35_JSON_REL, K35_JSON_PIN))",
    1, "anchor-k35ja-load")
rep("k34ja", "k35ja", 4, "anchor-k35ja-refs")

# ---- phase 7: finalize checks
rep("    # ---- pairs (561 + 34 = 595)",
    "    # ---- pairs (595 + 35 = 630)", 1, "pairs-comment")
rep('    chk("pairs.prev_561", len(pairs_prev) == 561)',
    '    chk("pairs.prev_595", len(pairs_prev) == 595)', 1, "prev-pairs")
rep('    chk("pairs.new_34", len(donep) == 34)',
    '    chk("pairs.new_35", len(donep) == 35)', 1, "new-pairs")
rep('    chk("pairs.complete_595", len(j2) == 595)',
    '    chk("pairs.complete_630", len(j2) == 630)', 1, "complete-pairs")
rep("        len(shared_new) == 16 and len(donep) - len(shared_new) == 18,",
    "        len(shared_new) == 10 and len(donep) - len(shared_new) == 25,",
    1, "pairs-census")
rep("    # ---- triples (5984 + 561 = 6545)",
    "    # ---- triples (6545 + 595 = 7140)", 1, "triples-comment")
rep('    chk("triples.prev_5984", len(j3) == 5984)',
    '    chk("triples.prev_6545", len(j3) == 6545)', 1, "prev-triples")
rep('    chk("triples.new_561", len(donet) == 561)',
    '    chk("triples.new_595", len(donet) == 595)', 1, "new-triples")
rep('    chk("triples.complete_6545", len(j3) == 6545)',
    '    chk("triples.complete_7140", len(j3) == 7140)', 1, "complete-triples")
rep('        cen == {"b_only": 3970, "zero": 1257, "disjoint": 1318}, cen)',
    '        cen == {"b_only": 4361, "zero": 1320, "disjoint": 1459}, cen)',
    1, "triple-census")
rep("    # ---- quads (46376 prev + 5984 new = 52360)",
    "    # ---- quads (52360 prev + 6545 new = 58905)", 1, "quads-comment")
rep('''    chk("quads.prev_46376_stored_45661",
        len(j4) == 46376 and len(quads_prev) == 45661,''',
    '''    chk("quads.prev_52360_stored_51645",
        len(j4) == 52360 and len(quads_prev) == 51645,''',
    1, "prev-quads")
rep('    chk("quads.new_5984", len(doneq) == 5984)',
    '    chk("quads.new_6545", len(doneq) == 6545)', 1, "new-quads")
rep('    chk("quads.complete_52360", len(j4) == 52360)',
    '    chk("quads.complete_58905", len(j4) == 58905)', 1, "complete-quads")
rep('        qcen == {"b_only": 1612, "zero": 4289, "disjoint": 83},',
    '        qcen == {"b_only": 2458, "zero": 3919, "disjoint": 168},',
    1, "quad-census")
rep('    chk("quads.prev_disjoint_1112", len(prev_disjoint) == 1112)',
    '    chk("quads.prev_disjoint_1195", len(prev_disjoint) == 1195)',
    1, "prev-disjoint")
rep('''    # new b_only quads double-row histogram (machine-derived;
    # row 21 cannot double (zero prior sharers among the top-34);
    # row 18 is the dominant new double row (1,155 of the 1,612
    # new b_only quads), while the four hub rows keep their
    # families); the b_only triple double-row histogram is
    # recorded as a computed fact too''',
    '''    # new b_only quads double-row histogram (machine-derived;
    # row 22 cannot double (zero prior sharers among the top-35);
    # rows 18 and 19 are the dominant new double rows (992 and
    # 1,150 of the 2,458 new b_only quads), while the four hub
    # rows keep their families); the b_only triple double-row
    # histogram is recorded as a computed fact too''',
    1, "quad-hist-comment")
rep('''        triple_dbl_hist == {0: 3, 4: 1, 5: 1, 15: 21, 16: 1,
                            18: 275, 19: 45, 30: 1},''',
    '''        triple_dbl_hist == {0: 1, 4: 1, 15: 15, 16: 3,
                            18: 136, 19: 232, 23: 1, 24: 1, 30: 1},''',
    1, "triple-dbl-hist")
rep('''    chk("quads.new_b_only_double_row_21_absent",
        quad_dbl_hist.get(21, 0) == 0, quad_dbl_hist)''',
    '''    chk("quads.new_b_only_double_row_22_absent",
        quad_dbl_hist.get(22, 0) == 0, quad_dbl_hist)''',
    1, "quad-22-absent")
rep('''        quad_dbl_hist == {0: 14, 4: 2, 5: 6, 15: 156, 16: 13,
                          18: 1155, 19: 264, 30: 2},''',
    '''        quad_dbl_hist == {0: 16, 4: 2, 15: 260, 16: 32,
                          18: 992, 19: 1150, 23: 2, 24: 2, 30: 2},''',
    1, "quad-dbl-hist")
rep('''    # ---- quints (265,252 top-34 zeros + 13,004 prev b_only +
    #      44,781 new zeros + 1,595 new b_only = 324,632)''',
    '''    # ---- quints (310,033 top-35 zeros + 14,599 prev b_only +
    #      49,525 new zeros + 2,835 new b_only = 376,992)''',
    1, "quints-comment")
rep('''    chk("quints.census_324632",
        n5 == 324632 and cen5 == {"b_only": 14599, "zero": 310033,
                                  "disjoint": 0},''',
    '''    chk("quints.census_376992",
        n5 == 376992 and cen5 == {"b_only": 17434, "zero": 359558,
                                  "disjoint": 0},''',
    1, "quint-census")
rep("        dbl_hist == {15: 2421, 16: 469, 18: 8017, 19: 3692},",
    "        dbl_hist == {15: 2785, 16: 545, 18: 9217, 19: 4887},",
    1, "dbl-hist")
rep('''    chk("quints.prev_census_matches_k34",
        prev_cen5 == {"b_only": 13004, "zero": 265252,
                     "disjoint": 0},''',
    '''    chk("quints.prev_census_matches_k35",
        prev_cen5 == {"b_only": 14599, "zero": 310033,
                     "disjoint": 0},''',
    1, "prev-census5")
rep('    chk("quints.new_records_1595", len(done5) == 1595)',
    '    chk("quints.new_records_2835", len(done5) == 2835)', 1, "new5-records")
rep("        and 32 not in c and 33 not in c))",
    "        and 32 not in c and 33 not in c and 34 not in c))", 1, "contain1")
rep('''    chk("quints.prev_b_only_contain_rank26_through_34", all(
        (25 in c) or (26 in c) or (27 in c) or (28 in c)
        or (29 in c) or (30 in c) or (31 in c) or (32 in c)
        or (33 in c)''',
    '''    chk("quints.prev_b_only_contain_rank26_through_35", all(
        (25 in c) or (26 in c) or (27 in c) or (28 in c)
        or (29 in c) or (30 in c) or (31 in c) or (32 in c)
        or (33 in c) or (34 in c)''', 1, "contain2")
rep('''    # new-era b_only quints never double row 21: row 21 has
    # zero prior sharers among the top-34 (the rank-35 root
    # is its first and so far only member), so it cannot
    # double in any layer; the new-era double-row histogram
    # stays within the four hub rows 15/16/18/19
    # (machine-derived from the 1,595 computed records; the
    # preread new_quint histogram agrees)''',
    '''    # new-era b_only quints never double row 22: row 22 has
    # zero prior sharers among the top-35 (the rank-36 root
    # is its first and so far only member), so it cannot
    # double in any layer; the new-era double-row histogram
    # stays within the four hub rows 15/16/18/19
    # (machine-derived from the 2,835 computed records; the
    # preread new_quint histogram agrees)''',
    1, "new5-dbl-comment")
rep('''    chk("quints.new_era_double_row_21_absent",
        new5_dbl == {15: 177, 16: 33, 18: 1112, 19: 273}, new5_dbl)''',
    '''    chk("quints.new_era_double_row_22_absent",
        new5_dbl == {15: 364, 16: 76, 18: 1200, 19: 1195}, new5_dbl)''',
    1, "new5-dbl")
rep('''    # ---- sextets: the quint-order I-E truncation stays closed at
    # k=35.  The published sextet census (commit 583b0bf1) proved
    # C(26,6)/C(27,6)/C(28,6) all zero, and the k=29/k=30/k=31/
    # k=32/k=33/k=34 publications reclassified C(29,6)/C(30,6)/
    # C(31,6)/C(32,6)/C(33,6)/C(34,6) all zero (zero is
    # superset-closed); a 6-subset of the top-35 either lies
    # inside the top-34 (already zero) or contains the rank-35
    # root, so the full C(35,6) reclassification here closes
    # the k=35 truncation (also cross-checked against the k=35
    # preread sextet census, commit 90fc51c991).''',
    '''    # ---- sextets: the quint-order I-E truncation stays closed at
    # k=36.  The published sextet census (commit 583b0bf1) proved
    # C(26,6)/C(27,6)/C(28,6) all zero, and the k=29/k=30/k=31/
    # k=32/k=33/k=34/k=35 publications reclassified C(29,6)/
    # C(30,6)/C(31,6)/C(32,6)/C(33,6)/C(34,6)/C(35,6) all zero
    # (zero is superset-closed); a 6-subset of the top-36 either
    # lies inside the top-35 (already zero) or contains the
    # rank-36 root, so the full C(36,6) reclassification here
    # closes the k=36 truncation (also cross-checked against
    # the k=36 preread sextet census, commit 67985e92c9).''',
    1, "sextet-comment")
rep('''    chk("sextet_census_k35",
        n6 == 1623160 and cen6 == {"b_only": 0, "zero": 1623160,
                                   "disjoint": 0}, cen6)''',
    '''    chk("sextet_census_k36",
        n6 == 1947792 and cen6 == {"b_only": 0, "zero": 1947792,
                                   "disjoint": 0}, cen6)''',
    1, "sextet-census")
rep('''    chk("reproduce_k1_34",
        all(kill[k] == int(k34j["values"]["kill"]["k%d" % k])
            for k in range(1, 35)))
    chk("split.reproduce_k1_34",
        all(killA[k] == int(k34j["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k34j["values"]["kill_B"]["k%d" % k])
            for k in range(1, 35)))''',
    '''    chk("reproduce_k1_35",
        all(kill[k] == int(k35j["values"]["kill"]["k%d" % k])
            for k in range(1, 36)))
    chk("split.reproduce_k1_35",
        all(killA[k] == int(k35j["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k35j["values"]["kill_B"]["k%d" % k])
            for k in range(1, 36)))''',
    1, "reproduce")
rep('''        {"k35_minus_k34": str(kill[K] - kill[K - 1]),
         "m35": str(mem[K - 1])})''',
    '''        {"k36_minus_k35": str(kill[K] - kill[K - 1]),
         "m36": str(mem[K - 1])})''',
    1, "marginal-detail")

# ---- phase 8: output JSON
rep('''        "schema": "n11-cost16-survival-k35-20261119-v1",
        "date": "2026-11-19",''',
    '''        "schema": "n11-cost16-survival-k36-20261119-v1",
        "date": "2026-11-19",''', 1, "schema-date")
rep('''        "title": ("Exact survival curve extended to k=35 for the "
                  "31-row cost-16 parent: rank-35 (18,21) is the "
                  "first root to cover row 21 (zero prior sharers, "
                  "so it can never double in any layer), row 18 is "
                  "a 16-sharer hub band row, the new pair census is "
                  "16 shared / 18 disjoint (the shared pairs are "
                  "exactly the 16 row-18 sharers, the first "
                  "heavy-share rank), and the quint era opened at "
                  "k=26 continues with 1,595 new non-zero b_only "
                  "quints of the C(35,5)=324,632 5-subsets on top "
                  "of the 13,004 published ones (the quint "
                  "double-row histogram stays within the four hub "
                  "rows 15/16/18/19: 15:2421 / 16:469 / 18:8017 / "
                  "19:3692) and the A-type 4-way term grows to "
                  "1,195 (83 new disjoint quads on top of the "
                  "1,112 published); 80 new disjoint triples, 18 "
                  "new disjoint pairs and 16 shared ones; the "
                  "full C(35,6)=1,623,160 sextet census is all "
                  "zero so the I-E stays closed at the fifth "
                  "order"),''',
    '''        "title": ("Exact survival curve extended to k=36 for the "
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
    1, "title")
rep('''            "survival_k34_json": {"path": K34_JSON_REL,
                                  "git_blob_sha1": K34_JSON_PIN,
                                  "commit": K34_JSON_COMMIT},
            "k35_preread": {"path": K35_PREREAD_REL,
                            "git_blob_sha1": K35_PREREAD_PIN,
                            "commit": K35_PREREAD_COMMIT},''',
    '''            "survival_k34_json": {"path": K34_JSON_REL,
                                  "git_blob_sha1": K34_JSON_PIN,
                                  "commit": K34_JSON_COMMIT},
            "survival_k35_json": {"path": K35_JSON_REL,
                                  "git_blob_sha1": K35_JSON_PIN,
                                  "commit": K35_JSON_COMMIT},
            "k36_preread": {"path": K36_PREREAD_REL,
                            "git_blob_sha1": K36_PREREAD_PIN,
                            "commit": K36_PREREAD_COMMIT},''',
    1, "inputs-block")
rep('''            "rank35_root": {"root": top[IDX35]["root"],
                            "rows": list(rows[IDX35]),
                            "membership": str(mem[IDX35]),
                            "a_part": str(ap[IDX35]),
                            "b_part": str(bp[IDX35]),
                            "note": "rank-35 (18,21): row 21 "
                                    "has zero prior sharers among "
                                    "the top-34 (first covered at "
                                    "rank-35, so it can never "
                                    "double in any layer), while "
                                    "row 18 is a 16-sharer hub "
                                    "band row (indices 1,4,5,6,7,"
                                    "11,12,18,19,20,21,23,24,26,27,"
                                    "30); 18 disjoint and 16 "
                                    "shared partners"},''',
    '''            "rank36_root": {"root": top[IDX36]["root"],
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
    1, "rank-root-block")
rep('''                {"note": "the k=35 preread (commit 90fc51c991) is "
                         "pure Python with exact integer "
                         "serialization (same toolchain as the "
                         "k=32/k=33/k=34 prereads, commits "
                         "490a3e44 / 67068e07 / 2a14f351), so it "
                         "needs no big-integer erratum, and its "
                         "membership/a_part/b_part "
                         "(120058481266728720 / 92036253749417268 / "
                         "28022227517311452) equal the pinned "
                         "aggregate exactly (asserted at load); "
                         "the structural fields (rows, hex, prior "
                         "hit indices, censuses, histograms) are "
                         "cross-checked at load and by the "
                         "preread_match.* finalize checks"}),''',
    '''                {"note": "the k=36 preread (commit 67985e92c9) is "
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
    1, "preread-note")
rep('"triple_census_k35": cen,', '"triple_census_k36": cen,', 1, "triple-census-out")
rep('"quint_census_k35": cen5,', '"quint_census_k36": cen5,', 1, "quint-census-out")
rep('''            "new_quint_census": {"b_only": 1595, "zero": 44781,
                                 "disjoint": 0},''',
    '''            "new_quint_census": {"b_only": 2835, "zero": 49525,
                                 "disjoint": 0},''', 1, "new-quint-out")
rep('''                {"note": "row 21 cannot double (zero "
                         "prior sharers); row 18 is the dominant "
                         "new double row (1,155 of the 1,612 new "
                         "b_only quads double row 18), "
                         "machine-derived from the computed new "
                         "quads in this finalize",''',
    '''                {"note": "row 22 cannot double (zero "
                         "prior sharers); rows 18 and 19 are the "
                         "dominant new double rows (992 and 1,150 "
                         "of the 2,458 new b_only quads), "
                         "machine-derived from the computed new "
                         "quads in this finalize",''',
    1, "quad-note-out")
rep('''                {"note": "computed fact: 275 of the 348 new b_only "
                         "triples double row 18 and 45 double "
                         "row 19; row 21 never doubles",''',
    '''                {"note": "computed fact: 136 of the 391 new b_only "
                         "triples double row 18 and 232 double "
                         "row 19; row 22 never doubles",''',
    1, "triple-note-out")
rep('"sextet_census_k35": cen6,', '"sextet_census_k36": cen6,', 1, "sextet-out")
rep('"quints_zero_synth_count": 44781,', '"quints_zero_synth_count": 49525,',
    1, "zero-synth")
rep('''            "quints_jsonl_note": ("zero quints are structural "
                                  "(classify from the pinned "
                                  "aggregate) and are not appended "
                                  "to the JSONL; finalize "
                                  "reclassifies all 324,632 "
                                  "5-subsets and asserts the exact "
                                  "census and the presence of every "
                                  "b_only record; the full "
                                  "C(35,6) sextet census is "
                                  "reclassified and asserted "
                                  "all-zero (truncation "
                                  "justification)"),''',
    '''            "quints_jsonl_note": ("zero quints are structural "
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
    1, "jsonl-note")
rep('''            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
                             "sum j4 + sum j5 for k <= 35; "
                             "kill_A(k) = sum a - sum j2_A + "
                             "sum j3_A - sum j4_A (j5_A == 0); "
                             "kill_B(k) = sum b - sum j2_B + "
                             "sum j3_B - sum j4_B + sum j5_B; "
                             "j4_A comes from the 1,195 disjoint "
                             "quads (1,112 published at k=34, 83 "
                             "new at k=35), j5_B from the 14,599 "
                             "b_only quints (13,004 prev, 1,595 "
                             "new); the sixth order stays "
                             "structurally zero (sextet_census_k35)"),''',
    '''            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
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
    1, "ie-mechanism")
rep('"marginal_k35": str(kill[K] - kill[K - 1]),',
    '"marginal_k36": str(kill[K] - kill[K - 1]),', 1, "marginal-out")

# ---- phase 9: global renames
if "IDX35" in text:
    rep("IDX35", "IDX36", text.count("IDX35"), "IDX-rename")
if "load_top35" in text:
    rep("load_top35", "load_top36", text.count("load_top35"), "loadtop-rename")
if "load_k35_base" in text:
    rep("load_k35_base", "load_k36_base", text.count("load_k35_base"),
        "loadbase-rename")
rep('pre["rank35"]', 'pre["rank36"]', 13, "preread-rank-refs")

if fails:
    print("FAILED anchors:")
    for f in fails:
        print(" ", f)
    sys.exit(1)

# final sanity: no stale k35-era references outside the intentional
stale = []
for probe, allowed in [("IDX35", 0), ("K35_PREREAD", 0), ("M35", 0),
                       ('pre["rank35"]', 0), ("1595b_only", 0),
                       ("cost16_survival_k35_20261118.py", 0),
                       ("cost16-survival-k35-20261118.jsonl", 0),
                       # 46376 survives twice in the rank-35
                       # regression-layer quint census asserts
                       ("46376", 2)]:
    got = text.count(probe)
    if got != allowed:
        stale.append((probe, got, allowed))
if stale:
    print("STALE references:", stale)
    sys.exit(1)

open(DST, "w", encoding="utf-8").write(text)
print("OK: wrote %s (%d bytes)" % (DST, len(text)))


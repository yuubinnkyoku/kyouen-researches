#!/usr/bin/env python3
"""Anchored-rep transformation: k37 preread script -> k38 preread script.

Reads base/k37pre.py (the published k=37 preread script, git blob
d0155d4f953f3da1513421f0667ad3e2bede2fad) and writes
cost16_survival_k38_preread_20261119.py via a sequence of anchored
single-occurrence replacements:

  - drop the rank-35 regression layer, add a rank-37 regression layer
    (vs the pinned published k37 preread JSON, commit 98321003), keep
    the rank-36 regression layer verbatim, and reorder to ascending
    36 -> 37 -> 38;
  - all rank-38 facts machine-derived by facts_k38.py are substituted
    as literals (root rows [19,29], m38 119,940,649,042,609,991,
    A 91,876,760,891,572,775 / B 28,063,888,151,037,216, pair 13/24,
    triple 420/113/133, quad 2519/5094/157, quint 2868/63177/0,
    cumulative disjoint quads 1,520+157=1,677, C(38,3)=8,436 census
    5,178/1,533/1,725, C(38,5)=501,942 census 23,024/478,918/0, sextet
    C(38,6)=2,760,681 all zero);
  - the single-share structural check moves from row 8 to row 29
    (single prior sharer index 19 = the rank-20 root (18,29); triple
    8 records / quad 11 records / quint absent, the same pattern as
    row 7 at k=33, row 9 at k=34 and row 8 at k=37).

Every replacement asserts exactly one occurrence of its anchor in the
current text, so a drifted base file fails loudly instead of producing
a silently-wrong script.
"""
import hashlib
import sys

SRC = "base/k37pre.py"
DST = "cost16_survival_k38_preread_20261119.py"
EXPECT_BASE_BLOB = "d0155d4f953f3da1513421f0667ad3e2bede2fad"

reps = []


def rep(old, new, count=1):
    reps.append((old, new, count))


def sub(src):
    for old, new, count in reps:
        got = src.count(old)
        if got != count:
            raise SystemExit(f"FAIL anchor x{got} != {count}: {old[:90]!r}")
        src = src.replace(old, new)
    return src


# ---- 1. docstring header ----
rep('"""Rank-37 structural preread for the 31-row cost-16 parent survival lane.',
    '"""Rank-38 structural preread for the 31-row cost-16 parent survival lane.')
rep("""re-derives the full structural census of the top-37
pair roots from the pinned phase-B aggregate with two independent
row-multiplicity classifiers, regresses the published rank-35 preread
layer (pinned k35 preread JSON, commit 90fc51c9, second-derivation
verified by commit 41c4cf12) and the published rank-36 preread layer
(pinned k36 preread JSON, commit 67985e92, reproduced byte-identically
on the Proxmox runner at commit fc46f01e), and records the rank-37
facts (root rows [8,19], prior hits, membership split, new
pair/triple/quad/quint censuses, full C(37,3)/C(37,5) censuses, sextet
C(37,6) census) needed by the k=37 main computation's load/assert
chain.  The k=35 and k=36 main result JSONs are already published
(commits 572b1365 / 6fcea02c) and the k=35/k=36 crosscheck extensions
are published (latest 259 checks, all pass, 2026-11-19), so the k=37
main computation pins the published k=36 result and regresses against
it in addition to this preread.""",
    """re-derives the full structural census of the top-38
pair roots from the pinned phase-B aggregate with two independent
row-multiplicity classifiers, regresses the published rank-36 preread
layer (pinned k36 preread JSON, commit 67985e92, reproduced
byte-identically on the Proxmox runner at commit fc46f01e) and the
published rank-37 preread layer (pinned k37 preread JSON, commit
98321003, independent bit-mask-vector second-derivation lineage commit
958057fb with erratum 059db03e), and records the rank-38 facts (root
rows [19,29], prior hits, membership split, new pair/triple/quad/quint
censuses, full C(38,3)/C(38,5) censuses, sextet C(38,6) census) needed
by the k=38 main computation's load/assert chain.  The k=36 and k=37
main result JSONs are already published (commits 6fcea02c / a4a7ce31)
and the k=36/k=37 crosscheck extensions are published (latest 287
checks, all pass, 2026-11-19), so the k=38 main computation pins the
published k=37 result and regresses against it in addition to this
preread.""")
rep("Usage: python3 cost16_survival_k37_preread_20261119.py [--local DIR] [--out PATH]",
    "Usage: python3 cost16_survival_k38_preread_20261119.py [--local DIR] [--out PATH]")

# ---- 2. pins / constants ----
rep("""    "k35pre": ("cost16-survival-k35-preread-20261118.json",
               "490fa3a00b8e0b19229c94aa6b1aba4a5604ec13"),
    "k36pre": ("cost16-survival-k36-preread-20261118.json",
               "760aa396361cc7d2ea8bc371f4dd673d962f07fe"),
""",
    """    "k36pre": ("cost16-survival-k36-preread-20261118.json",
               "760aa396361cc7d2ea8bc371f4dd673d962f07fe"),
    "k37pre": ("cost16-survival-k37-preread-20261119.json",
               "b98ed685e772eacbd28dc3100e9813e81c27040a"),
""")
rep("""# sha1s the pinned k36 preread must declare as its inputs (publication
# chain: the k36 preread consumed the aggregate and the k34/k35
# preread artifacts)
K34PRE_SHA = "8dbb1bcbdaed9bee475f3b95932d35a9500e62cb\"""",
    """# sha1 the pinned k37 preread must declare for the k35 preread it
# consumed (publication chain: the k37 preread consumed the aggregate
# and the k35/k36 preread artifacts; k36 is pinned above)
K35PRE_SHA = "490fa3a00b8e0b19229c94aa6b1aba4a5604ec13\"""")
rep("""RANK = 37      # 1-based top50 rank of the new root""",
    """RANK = 38      # 1-based top50 rank of the new root""")
rep("""ap.add_argument("--out", default="output/cost16-survival-k37-preread-20261119.json",""",
    """ap.add_argument("--out", default="output/cost16-survival-k38-preread-20261119.json",""")

# ---- 3. fetch ----
rep("""    agg = fetch(*PINS["agg"], args.local)
    k35pre = fetch(*PINS["k35pre"], args.local)
    k36pre = fetch(*PINS["k36pre"], args.local)
    if not (k35pre.get("all_pass") and k35pre.get("check_count") == 33):
        print("FAIL k35 preread all_pass/check_count unexpected")
        return 1
    if not (k36pre.get("all_pass") and k36pre.get("check_count") == 33):
        print("FAIL k36 preread all_pass/check_count unexpected")
        return 1""",
    """    agg = fetch(*PINS["agg"], args.local)
    k36pre = fetch(*PINS["k36pre"], args.local)
    k37pre = fetch(*PINS["k37pre"], args.local)
    if not (k36pre.get("all_pass") and k36pre.get("check_count") == 33):
        print("FAIL k36 preread all_pass/check_count unexpected")
        return 1
    if not (k37pre.get("all_pass") and k37pre.get("check_count") == 34):
        print("FAIL k37 preread all_pass/check_count unexpected")
        return 1""")

# ---- 4. publication-chain check ----
rep("""    # 2. publication chain: the pinned k36 preread declares the pinned
    #    aggregate, k34 preread and k35 preread it consumed
    in_pins = {k: v["git_blob_sha1"] for k, v in k36pre["inputs"].items()
               if isinstance(v, dict) and "git_blob_sha1" in v}
    check("k36_preread_declares_pinned_inputs",
          in_pins.get("aggregate") == PINS["agg"][1]
          and in_pins.get("k34_preread") == K34PRE_SHA
          and in_pins.get("k35_preread") == PINS["k35pre"][1],
          {"declared": in_pins, "pinned_agg": PINS["agg"][1],
           "pinned_k34pre": K34PRE_SHA, "pinned_k35pre": PINS["k35pre"][1]})""",
    """    # 2. publication chain: the pinned k37 preread declares the pinned
    #    aggregate, k35 preread and k36 preread it consumed
    in_pins = {k: v["git_blob_sha1"] for k, v in k37pre["inputs"].items()
               if isinstance(v, dict) and "git_blob_sha1" in v}
    check("k37_preread_declares_pinned_inputs",
          in_pins.get("aggregate") == PINS["agg"][1]
          and in_pins.get("k35_preread") == K35PRE_SHA
          and in_pins.get("k36_preread") == PINS["k36pre"][1],
          {"declared": in_pins, "pinned_agg": PINS["agg"][1],
           "pinned_k35pre": K35PRE_SHA, "pinned_k36pre": PINS["k36pre"][1]})""")

# ---- 5. rank-35 regression block -> rank-37 regression block ----
rep("""    # ---- rank-35 regression (vs the pinned published k35 preread JSON)
    reg = {}
    n = 35
    idx = n - 1
    pub35 = k35pre["rank35"]""",
    """    # ---- rank-37 regression (vs the pinned published k37 preread JSON)
    n = 37
    idx = n - 1
    pub37 = k37pre["rank37"]""")
rep("""    check(f"rank{n}_root_matches_published_preread",
          pub35["root"] == "00000000000000801202090000001000" == top[idx]["root"]
          and sorted(pub35["rows"]) == sorted(rows[idx]) == [18, 21]
          and int(pub35["membership"]) == int(mem[idx]) == 120058481266728720
          and int(pub35["a_part"]) == 92036253749417268
          and int(pub35["b_part"]) == 28022227517311452,
          {"root": pub35["root"], "rows": sorted(rows[idx]), "membership": int(mem[idx])})""",
    """    check(f"rank{n}_root_matches_published_preread",
          pub37["root"] == "00000000080000003800000108001000" == top[idx]["root"]
          and sorted(pub37["rows"]) == sorted(rows[idx]) == [8, 19]
          and int(pub37["membership"]) == int(mem[idx]) == 119973409932394637
          and int(pub37["a_part"]) == 91996175553485330
          and int(pub37["b_part"]) == 27977234378909307,
          {"root": pub37["root"], "rows": sorted(rows[idx]), "membership": int(mem[idx])})""")
rep("""          prior == {18: [1, 4, 5, 6, 7, 11, 12, 18, 19, 20, 21, 23, 24, 26, 27, 30], 21: []}
          and {k: sorted(v) for k, v in pub35["prior_hit_indices"].items()}""",
    """          prior == {8: [23], 19: [0, 2, 3, 8, 9, 10, 15, 29, 32, 33, 35]}
          and {k: sorted(v) for k, v in pub37["prior_hit_indices"].items()}""")

# remaining pub35 references inside the block -> pub37 (12 census +
# 7 histogram + 5 full-census lines), asserted by exact count
rep("pub35", "pub37", 23)

rep("""          and tc == {"b_only": 348, "zero": 133, "disjoint": 80}
          and qc == {"b_only": 1612, "zero": 4289, "disjoint": 83}
          and uc == {"b_only": 1595, "zero": 44781, "disjoint": 0},""",
    """          and tc == {"b_only": 397, "zero": 100, "disjoint": 133}
          and qc == {"b_only": 2394, "zero": 4589, "disjoint": 157}
          and uc == {"b_only": 2722, "zero": 56183, "disjoint": 0},""")
rep("""          and pub37["disjoint_quad_count"] == qc["disjoint"] == 83
          and {int(k): v for k, v in pub37["disjoint_quad_union_sizes"].items()} == dusizes
          and set(dusizes) == {8}
          and pub37["cumulative_disjoint_quads"] == 1112 + qc["disjoint"] == 1195,
          {"disjoint_union_sizes": dusizes, "cumulative": 1112 + qc["disjoint"]})""",
    """          and pub37["disjoint_quad_count"] == qc["disjoint"] == 157
          and {int(k): v for k, v in pub37["disjoint_quad_union_sizes"].items()} == dusizes
          and set(dusizes) == {8}
          and pub37["cumulative_disjoint_quads"] == 1363 + qc["disjoint"] == 1520,
          {"disjoint_union_sizes": dusizes, "cumulative": 1363 + qc["disjoint"]})""")
rep("""          and ful3 == {"b_only": 3970, "zero": 1257, "disjoint": 1318}
          and {int(k): v for k, v in pub37["full_triples"]["double_row_histogram"].items()} == f3twos""",
    """          and ful3 == {"b_only": 4758, "zero": 1420, "disjoint": 1592}
          and {int(k): v for k, v in pub37["full_triples"]["double_row_histogram"].items()} == f3twos""")
rep("""          and ful5 == {"b_only": 14599, "zero": 310033, "disjoint": 0}
          and {int(k): v for k, v in pub37["full_quints"]["double_row_histogram"].items()} == f5twos""",
    """          and ful5 == {"b_only": 20156, "zero": 415741, "disjoint": 0}
          and {int(k): v for k, v in pub37["full_quints"]["double_row_histogram"].items()} == f5twos""")
rep("""          and six == {"b_only": 0, "zero": math.comb(35, 6), "disjoint": 0},""",
    """          and six == {"b_only": 0, "zero": math.comb(37, 6), "disjoint": 0},""")
rep("""    check(f"rank{n}_era_continuation_matches_k35_preread_rank34_regression",
          ful5["b_only"] - uc["b_only"] == 13004
          and k35pre["rank34_regression"]["full_quints"]["counts"]["b_only"] == 13004
          and ful5["zero"] - uc["zero"] == 265252
          and k35pre["rank34_regression"]["full_quints"]["counts"]["zero"] == 265252""",
    """    check(f"rank{n}_era_continuation_matches_k37_preread_rank36_regression",
          ful5["b_only"] - uc["b_only"] == 17434
          and k37pre["rank36_regression"]["full_quints"]["counts"]["b_only"] == 17434
          and ful5["zero"] - uc["zero"] == 359558
          and k37pre["rank36_regression"]["full_quints"]["counts"]["zero"] == 359558""")
rep("""          {"prev_b_only": 13004,
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"]})""",
    """          {"prev_b_only": 17434,
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"]})""")

# ---- 6. rank-37 facts block -> rank-38 facts block ----
rep("""    # ---- rank-37 facts (all machine-derived from the pinned aggregate)
    root = top[IDX]["root"]
    m37 = int(mem[IDX])
    a37 = int(memA[root])
    b37 = int(memB[root])""",
    """    # ---- rank-38 facts (all machine-derived from the pinned aggregate)
    root = top[IDX]["root"]
    m38 = int(mem[IDX])
    a38 = int(memA[root])
    b38 = int(memB[root])""")
rep("""    check("rank37_root_matches_top50",
          root == "00000000080000003800000108001000"
          and sorted(rows[IDX]) == [8, 19],""",
    """    check("rank38_root_matches_top50",
          root == "00000008800000003800000008100000"
          and sorted(rows[IDX]) == [19, 29],""")
rep("""    check("rank37_prior_hits_recorded",
          prior == {8: [23], 19: [0, 2, 3, 8, 9, 10, 15, 29, 32, 33, 35]},""",
    """    check("rank38_prior_hits_recorded",
          prior == {19: [0, 2, 3, 8, 9, 10, 15, 29, 32, 33, 35, 36], 29: [19]},""")
rep("""    check("rank37_membership_split_identity",
          a37 + b37 == m37
          and m37 == 119973409932394637
          and m37 < int(reg[36]["membership"]),
          {"membership": m37, "a_part": a37, "b_part": b37})""",
    """    check("rank38_membership_split_identity",
          a38 + b38 == m38
          and m38 == 119940649042609991
          and m38 < int(reg[37]["membership"]),
          {"membership": m38, "a_part": a38, "b_part": b38})""")
rep("""    check("rank37_new_pair_census",
          pc["disjoint"] == IDX - shared and shared == 12 and pc["disjoint"] == 24,""",
    """    check("rank38_new_pair_census",
          pc["disjoint"] == IDX - shared and shared == 13 and pc["disjoint"] == 24,""")
rep("""    check("rank37_new_triple_census",
          tc["b_only"] + tc["zero"] + tc["disjoint"] == math.comb(IDX, 2)
          and tc == {"b_only": 397, "zero": 100, "disjoint": 133}, tc)""",
    """    check("rank38_new_triple_census",
          tc["b_only"] + tc["zero"] + tc["disjoint"] == math.comb(IDX, 2)
          and tc == {"b_only": 420, "zero": 113, "disjoint": 133}, tc)""")
rep("""    check("rank37_new_quad_census",
          qc["b_only"] + qc["zero"] + qc["disjoint"] == math.comb(IDX, 3)
          and qc == {"b_only": 2394, "zero": 4589, "disjoint": 157}, qc)""",
    """    check("rank38_new_quad_census",
          qc["b_only"] + qc["zero"] + qc["disjoint"] == math.comb(IDX, 3)
          and qc == {"b_only": 2519, "zero": 5094, "disjoint": 157}, qc)""")
rep("""    check("rank37_new_quint_census",
          uc["b_only"] + uc["zero"] + uc["disjoint"] == math.comb(IDX, 4)
          and uc["b_only"] == len(new_quint_b_only)
          and uc["zero"] == math.comb(IDX, 4) - uc["b_only"]
          and uc == {"b_only": 2722, "zero": 56183, "disjoint": 0},""",
    """    check("rank38_new_quint_census",
          uc["b_only"] + uc["zero"] + uc["disjoint"] == math.comb(IDX, 4)
          and uc["b_only"] == len(new_quint_b_only)
          and uc["zero"] == math.comb(IDX, 4) - uc["b_only"]
          and uc == {"b_only": 2868, "zero": 63177, "disjoint": 0},""")
rep("""    check("rank37_new_quint_double_rows",
          sum(utwos.values()) == uc["b_only"] and 8 not in utwos and 19 in utwos
          and utwos == {15: 339, 16: 71, 18: 1043, 19: 1269}, utwos)""",
    """    check("rank38_new_quint_double_rows",
          sum(utwos.values()) == uc["b_only"] and 29 not in utwos and 19 in utwos
          and utwos == {15: 339, 16: 71, 18: 1043, 19: 1415}, utwos)""")
rep("""    check("rank37_b_only_quint_profiles",""",
    """    check("rank38_b_only_quint_profiles",""")
rep("""    check("rank37_disjoint_quads_union8",
          sum(dusizes.values()) == qc["disjoint"] and set(dusizes) == {8}
          and qc["disjoint"] == 157,
          {"disjoint_quad_count": qc["disjoint"], "union_sizes": dusizes,
           "cumulative_disjoint_quads": 1363 + qc["disjoint"]})""",
    """    check("rank38_disjoint_quads_union8",
          sum(dusizes.values()) == qc["disjoint"] and set(dusizes) == {8}
          and qc["disjoint"] == 157,
          {"disjoint_quad_count": qc["disjoint"], "union_sizes": dusizes,
           "cumulative_disjoint_quads": 1520 + qc["disjoint"]})""")
rep("""    dj37 = sum(1 for c in itertools.combinations(range(RANK), 4)
               if classify_a(rows, c)[0] == "disjoint")
    check("rank37_cumulative_disjoint_quads_global_recount",
          dj37 == 1520 and dj37 == 1363 + qc["disjoint"]
          and dj37 == pub36["cumulative_disjoint_quads"] + qc["disjoint"],
          {"global_C37_4": dj37, "prev_cumulative": pub36["cumulative_disjoint_quads"],
           "new": qc["disjoint"]})""",
    """    dj38 = sum(1 for c in itertools.combinations(range(RANK), 4)
               if classify_a(rows, c)[0] == "disjoint")
    check("rank38_cumulative_disjoint_quads_global_recount",
          dj38 == 1677 and dj38 == 1520 + qc["disjoint"]
          and dj38 == pub37["cumulative_disjoint_quads"] + qc["disjoint"],
          {"global_C38_4": dj38, "prev_cumulative": pub37["cumulative_disjoint_quads"],
           "new": qc["disjoint"]})""")
rep("""    check("rank37_full_census_totals",
          ful3["b_only"] + ful3["zero"] + ful3["disjoint"] == math.comb(RANK, 3)
          and ful5["b_only"] + ful5["zero"] + ful5["disjoint"] == math.comb(RANK, 5)
          and sum(f5twos.values()) == ful5["b_only"]
          and ful3 == {"b_only": 4758, "zero": 1420, "disjoint": 1592}
          and ful5 == {"b_only": 20156, "zero": 415741, "disjoint": 0}
          and f5twos == {15: 3124, 16: 616, 18: 10260, 19: 6156},""",
    """    check("rank38_full_census_totals",
          ful3["b_only"] + ful3["zero"] + ful3["disjoint"] == math.comb(RANK, 3)
          and ful5["b_only"] + ful5["zero"] + ful5["disjoint"] == math.comb(RANK, 5)
          and sum(f5twos.values()) == ful5["b_only"]
          and ful3 == {"b_only": 5178, "zero": 1533, "disjoint": 1725}
          and ful5 == {"b_only": 23024, "zero": 478918, "disjoint": 0}
          and f5twos == {15: 3463, 16: 687, 18: 11303, 19: 7571},""")
rep("""    check("rank37_quint_era_continuation",
          ful5["b_only"] - uc["b_only"] == reg[36]["full_quints"]["counts"]["b_only"]
          and ful5["zero"] - uc["zero"] == reg[36]["full_quints"]["counts"]["zero"]
          and ful5["disjoint"] == 0,
          {"prev_b_only": reg[36]["full_quints"]["counts"]["b_only"],
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"],
           "prev_zero": reg[36]["full_quints"]["counts"]["zero"],
           "new_zero": uc["zero"], "full_zero": ful5["zero"]})""",
    """    check("rank38_quint_era_continuation",
          ful5["b_only"] - uc["b_only"] == reg[37]["full_quints"]["counts"]["b_only"]
          and ful5["zero"] - uc["zero"] == reg[37]["full_quints"]["counts"]["zero"]
          and ful5["disjoint"] == 0,
          {"prev_b_only": reg[37]["full_quints"]["counts"]["b_only"],
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"],
           "prev_zero": reg[37]["full_quints"]["counts"]["zero"],
           "new_zero": uc["zero"], "full_zero": ful5["zero"]})""")
rep("""    check("rank37_single_share_row_8_doubles_triple_quad_only",
          # row 8 appears before rank-37 only via index 23 (single share):
          # it joins the double-row family for the first time here, with 8
          # records in the triple layer and 11 in the quad layer, never in
          # the quint layer (the same single-sharer doubling pattern as
          # row 7 at rank-33 and row 9 at rank-34)
          prior[8] == [23]
          and ttwos == {0: 1, 4: 1, 8: 8, 15: 15, 16: 3, 18: 120, 19: 246, 23: 1, 24: 1, 30: 1}
          and qtwos == {0: 15, 4: 2, 8: 11, 15: 245, 16: 31, 18: 870, 19: 1214, 23: 2, 24: 2, 30: 2}
          and 8 not in utwos,
          {"triple": ttwos, "quad": qtwos, "quint": utwos,
           "row8_prior_sharers": prior[8]})""",
    """    check("rank38_single_share_row_29_doubles_triple_quad_only",
          # row 29 appears before rank-38 only via index 19 (the rank-20
          # root (18,29), single share): it joins the double-row family
          # for the first time here, with 8 records in the triple layer
          # and 11 in the quad layer, never in the quint layer (the same
          # single-sharer doubling pattern as row 7 at rank-33, row 9 at
          # rank-34 and row 8 at rank-37)
          prior[29] == [19]
          and ttwos == {0: 1, 4: 1, 15: 15, 16: 3, 18: 120, 19: 269, 23: 1, 24: 1, 29: 8, 30: 1}
          and qtwos == {0: 15, 4: 2, 15: 245, 16: 31, 18: 870, 19: 1339, 23: 2, 24: 2, 29: 11, 30: 2}
          and 29 not in utwos,
          {"triple": ttwos, "quad": qtwos, "quint": utwos,
           "row29_prior_sharers": prior[29]})""")
rep("""    check("rank37_sextet_census_all_zero",""",
    """    check("rank38_sextet_census_all_zero",""")
rep("""    check("rank37_expected_totals",
          math.comb(RANK, 3) == 7770 and math.comb(IDX, 2) == 630
          and math.comb(IDX, 3) == 7140 and math.comb(IDX, 4) == 58905
          and math.comb(RANK, 5) == 435897 and math.comb(RANK, 6) == 2324784,
          {"C36_2": math.comb(IDX, 2), "C36_3": math.comb(IDX, 3), "C36_4": math.comb(IDX, 4),
           "C37_3": math.comb(RANK, 3), "C37_5": math.comb(RANK, 5), "C37_6": math.comb(RANK, 6)})""",
    """    check("rank38_expected_totals",
          math.comb(RANK, 3) == 8436 and math.comb(IDX, 2) == 666
          and math.comb(IDX, 3) == 7770 and math.comb(IDX, 4) == 66045
          and math.comb(RANK, 5) == 501942 and math.comb(RANK, 6) == 2760681,
          {"C37_2": math.comb(IDX, 2), "C37_3": math.comb(IDX, 3), "C37_4": math.comb(IDX, 4),
           "C38_3": math.comb(RANK, 3), "C38_5": math.comb(RANK, 5), "C38_6": math.comb(RANK, 6)})""")
rep("""    check("rank37_two_classifiers_agree",""",
    """    check("rank38_two_classifiers_agree",""")

# ---- 7. rank37 facts dict -> rank38 facts dict ----
rep("""    rank37 = {
        "root": root,
        "rows": sorted(rows[IDX]),
        "membership": m37,
        "a_part": a37,
        "b_part": b37,""",
    """    rank38 = {
        "root": root,
        "rows": sorted(rows[IDX]),
        "membership": m38,
        "a_part": a38,
        "b_part": b38,""")
rep('''        "note": ("rank-37 (8,19) has no fresh row: row 8 arrives with a single "
                 "prior sharer (index 23) and doubles for the first time in "
                 "the triple layer (8 records) and the quad layer (11 "
                 "records), never in the quint layer (the same single-sharer "
                 "doubling pattern as row 7 at rank-33 and row 9 at "
                 "rank-34), while row 19 becomes an eleven-sharer hub band "
                 "row (prior sharers 0,2,3,8,9,10,15,29,32,33,35 -- rank-36 "
                 "itself is a sharer). The new pair census is 12 shared / 24 "
                 "disjoint (the shared pairs are exactly the one row-8 "
                 "sharer plus the eleven row-19 sharers). Row 19 stays the "
                 "dominant double row of the new layers and the new quint "
                 "double-row histogram stays within the four hub rows "
                 "15/16/18/19 (row 8 absent, 339/71/1,043/1,269). The 157 "
                 "new disjoint quads all have 8-row unions (cumulative "
                 "1,520 = 1,363 + 157), the new b_only quints are 2,722 "
                 "(all 3/2/0 four-subset profiles, cumulative 20,156 = "
                 "17,434 + 2,722 b_only in C(37,5)), the full C(37,3)=7,770 "
                 "census is 4,758/1,420/1,592 and the C(37,6)=2,324,784 "
                 "sextet census stays all zero, so the quint "
                 "inclusion-exclusion truncation carries over to k=37. The "
                 "fresh-row series of ranks 35-36 (rows 21 and 22) ends "
                 "here. The rank-36 regression layer above re-derives the "
                 "published rank-36 preread facts from the pinned "
                 "aggregate, and row 8's pattern gives the k=37 main "
                 "computation the same single-share structural bound as "
                 "k=33/k=34."),''',
    '''        "note": ("rank-38 (19,29) has no fresh row: row 29 arrives with a "
                 "single prior sharer (index 19, the rank-20 root (18,29)) "
                 "and doubles for the first time in the triple layer (8 "
                 "records) and the quad layer (11 records), never in the "
                 "quint layer (the same single-sharer doubling pattern as "
                 "row 7 at rank-33, row 9 at rank-34 and row 8 at "
                 "rank-37), while row 19 becomes a twelve-sharer hub band "
                 "row (prior sharers 0,2,3,8,9,10,15,29,32,33,35,36 -- "
                 "rank-37 itself is a sharer). The new pair census is 13 "
                 "shared / 24 disjoint (the shared pairs are exactly the "
                 "twelve row-19 sharers plus the one row-29 sharer, index "
                 "19). Row 19 stays the dominant double row of the new "
                 "layers and the new quint double-row histogram stays "
                 "within the four hub rows 15/16/18/19 (339/71/1,043/1,415; "
                 "row 29 absent). The 157 new disjoint quads all have "
                 "8-row unions (cumulative 1,677 = 1,520 + 157), the new "
                 "b_only quints are 2,868 (all 3/2/0 four-subset "
                 "profiles, cumulative 23,024 = 20,156 + 2,868 b_only in "
                 "C(38,5)), the full C(38,3)=8,436 census is "
                 "5,178/1,533/1,725 and the C(38,6)=2,760,681 sextet "
                 "census stays all zero, so the quint inclusion-exclusion "
                 "truncation carries over to k=38. The rank-36 and "
                 "rank-37 regression layers above re-derive the published "
                 "rank-36/rank-37 preread facts from the pinned aggregate, "
                 "and row 29's pattern gives the k=38 main computation the "
                 "same single-share structural bound as "
                 "k=33/k=34/k=37."),''')
rep('"cumulative_disjoint_quads": 1363 + qc["disjoint"],',
    '"cumulative_disjoint_quads": 1520 + qc["disjoint"],')

# ---- 8. out dict ----
rep('"schema": "n11-cost16-k37-preread-20261119-v1",',
    '"schema": "n11-cost16-k38-preread-20261119-v1",')
rep('"title": "31-row cost-16 parent: rank-37 structural preread",',
    '"title": "31-row cost-16 parent: rank-38 structural preread",')
rep('''        "language_note": ("pure Python with exact integer serialization (following the "
                          "k=32/k=33/k=34/k=35/k=36 preread scripts); the rank-35 "
                          "regression layer compares against the pinned published k=35 "
                          "preread JSON and the rank-36 regression layer against the "
                          "pinned published k=36 preread JSON; the k=35 and k=36 main "
                          "result JSONs are already published (commits 572b1365 / "
                          "6fcea02c) and the k=35/k=36 crosscheck extensions are "
                          "published (latest 259 checks, all pass, 2026-11-19), so the "
                          "k=37 main computation pins the published k=36 result and "
                          "regresses against it as well; this preread adds the "
                          "single-share row-8 structural check, so check_count is 34."),''',
    '''        "language_note": ("pure Python with exact integer serialization (following the "
                          "k=32/k=33/k=34/k=35/k=36/k=37 preread scripts); the rank-36 "
                          "regression layer compares against the pinned published k=36 "
                          "preread JSON and the rank-37 regression layer against the "
                          "pinned published k=37 preread JSON; the k=36 and k=37 main "
                          "result JSONs are already published (commits 6fcea02c / "
                          "a4a7ce31) and the k=36/k=37 crosscheck extensions are "
                          "published (latest 287 checks, all pass, 2026-11-19), so the "
                          "k=38 main computation pins the published k=37 result and "
                          "regresses against it as well; this preread carries the "
                          "single-share structural check over to row 29, so "
                          "check_count stays 34."),''')
rep('''            "k35_preread": {"path": f"{PATH}/cost16-survival-k35-preread-20261118.json",
                            "git_blob_sha1": PINS["k35pre"][1],
                            "commit": "90fc51c9"},
            "k36_preread": {"path": f"{PATH}/cost16-survival-k36-preread-20261118.json",
                            "git_blob_sha1": PINS["k36pre"][1],
                            "commit": "67985e92"},
            "k35_preread_independent_verification": (
                "verify_cost16_k35_preread_independent_20261118.py, "
                "commit 41c4cf12, 30 checks 0 failures (second derivation lineage)"),
            "k36_preread_independent_verification": (
                "Proxmox runner reproduction (commit fc46f01e): the same script "
                "re-run produced byte-identical output"),''',
    '''            "k36_preread": {"path": f"{PATH}/cost16-survival-k36-preread-20261118.json",
                            "git_blob_sha1": PINS["k36pre"][1],
                            "commit": "67985e92"},
            "k37_preread": {"path": f"{PATH}/cost16-survival-k37-preread-20261119.json",
                            "git_blob_sha1": PINS["k37pre"][1],
                            "commit": "98321003"},
            "k36_preread_independent_verification": (
                "Proxmox runner reproduction (commit fc46f01e): the same script "
                "re-run produced byte-identical output"),
            "k37_preread_independent_verification": (
                "bit-mask-vector second derivation lineage (commit 958057fb, "
                "erratum 059db03e): the independent re-derivation agreed on "
                "every machine-derived fact"),''')
rep('"rank_convention": "top50_by_membership; 1-based rank 37",',
    '"rank_convention": "top50_by_membership; 1-based rank 38",')
rep('''        "rank35_regression": reg[35],
        "rank36_regression": reg[36],
        "rank37": rank37,''',
    '''        "rank36_regression": reg[36],
        "rank37_regression": reg[37],
        "rank38": rank38,''')

# ---- 9. final serialization check and prints ----
rep('''    ok = (back["rank37"]["membership"] == m37
          and back["rank37"]["a_part"] == a37 and back["rank37"]["b_part"] == b37
          and back["rank35_regression"]["membership"] == int(mem[34])
          and back["rank36_regression"]["membership"] == int(mem[35])
          and back["rank35_regression"]["a_part"] == int(memA[top[34]["root"]])
          and back["rank35_regression"]["b_part"] == int(memB[top[34]["root"]])
          and back["rank36_regression"]["a_part"] == int(memA[top[35]["root"]])
          and back["rank36_regression"]["b_part"] == int(memB[top[35]["root"]]))
    checks.append({"name": "rank37_exact_integer_json_serialization", "pass": bool(ok),
                   "detail": {"membership": m37, "a_part": a37, "b_part": b37}})''',
    '''    ok = (back["rank38"]["membership"] == m38
          and back["rank38"]["a_part"] == a38 and back["rank38"]["b_part"] == b38
          and back["rank36_regression"]["membership"] == int(mem[35])
          and back["rank37_regression"]["membership"] == int(mem[36])
          and back["rank36_regression"]["a_part"] == int(memA[top[35]["root"]])
          and back["rank36_regression"]["b_part"] == int(memB[top[35]["root"]])
          and back["rank37_regression"]["a_part"] == int(memA[top[36]["root"]])
          and back["rank37_regression"]["b_part"] == int(memB[top[36]["root"]]))
    checks.append({"name": "rank38_exact_integer_json_serialization", "pass": bool(ok),
                   "detail": {"membership": m38, "a_part": a38, "b_part": b38}})''')
rep('''    print(f"rank-37 root {root} rows {sorted(rows[IDX])} m37 {m37} (A {a37} / B {b37})")''',
    '''    print(f"rank-38 root {root} rows {sorted(rows[IDX])} m38 {m38} (A {a38} / B {b38})")''')
rep('    print(f"full C(37,5): {ful5}  sextet C(37,6): {six}")',
    '    print(f"full C(38,5): {ful5}  sextet C(38,6): {six}")')


def main() -> int:
    src = open(SRC, encoding="utf-8").read()
    base = open(SRC, "rb").read()
    blob = hashlib.sha1(b"blob %d\x00" % len(base) + base).hexdigest()
    if blob != EXPECT_BASE_BLOB:
        raise SystemExit(f"FAIL base blob {blob}")
    out = sub(src)

    # ---- reorder regression blocks to ascending 36 -> 37 ----
    m_a = out.index("    # ---- rank-37 regression (vs the pinned published k37 preread JSON)")
    m_b = out.index("    # ---- rank-36 regression (vs the pinned published k36 preread JSON)")
    m_c = out.index("    # ---- rank-38 facts (all machine-derived from the pinned aggregate)")
    assert m_a < m_b < m_c, "block order unexpected"
    blk_a = out[m_a:m_b]   # rank-37 regression (no reg init)
    blk_b = out[m_b:m_c]   # rank-36 regression
    b_head, b_rest = blk_b.split("\n", 1)
    blk_b = b_head + "\n    reg = {}\n" + b_rest
    out = out[:m_a] + blk_b + blk_a + out[m_c:]

    # residual sanity: no stale identifiers may survive
    for stale in ("pub35", 'PINS["k35pre"]', "k35pre =", "k35pre[",
                  "K34PRE_SHA", "rank37 =", "m37", "dj37",
                  "back[\"rank37\"][", "back[\"rank35_regression\"]"):
        if stale in out:
            raise SystemExit(f"FAIL stale token {stale!r} survived")
    open(DST, "w", encoding="utf-8").write(out)
    data = open(DST, "rb").read()
    print("wrote", DST, len(data), "bytes")
    print("git_blob_sha1:", hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest())
    print("sha256:", hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())

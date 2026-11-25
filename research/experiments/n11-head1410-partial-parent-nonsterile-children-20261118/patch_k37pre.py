#!/usr/bin/env python3
"""Machine transformation: published rank-36 preread script -> rank-37.

Anchored-rep patch (same practice as the published patch_cc_k36.py).
Every anchor count is asserted before replacement; the resulting
script re-derives every constant at run time from the pinned aggregate
and the pinned published k35/k36 preread JSONs (both fetched at pinned
git blob sha1s, locally sha1-verified), so a wrong constant here
cannot survive a run.

Versus the k36 script this adds one new structural check
(rank37_single_share_row_8_doubles_triple_quad_only), so check_count
moves from 33 to 34, and strengthens rank37_full_census_totals with the
full-quint double-row histogram literal (independently precomputed
from the pinned aggregate before this transformation).
"""
import re

SRC = "cost16_survival_k36_preread_20261118.py"
DST = "cost16_survival_k37_preread_20261119.py"

with open(SRC, encoding="utf-8") as fh:
    text = fh.read()


def do(old, new, count=1):
    global text
    n = text.count(old)
    assert n == count, "anchor x%d (want %d): %r" % (n, count, old[:160])
    text = text.replace(old, new)


# ------------------------------------------------------------ docstring
do('"""Rank-36 structural preread', '"""Rank-37 structural preread')
do("re-derives the full structural census of the top-36",
   "re-derives the full structural census of the top-37")
do('''row-multiplicity classifiers, regresses the published rank-34 preread
layer (pinned k34 preread JSON, commit 2a14f351, second-derivation
verified by commit a450e366) and the published rank-35 preread layer
(pinned k35 preread JSON, commit 90fc51c9, value-verified against a
second derivation lineage on 2026-11-19; the independent Python
verification script follows the k=32/k=33/k=34 pattern and will be
published), and records the rank-36 facts (root rows [19,22], prior
hits, membership split, new pair/triple/quad/quint censuses, full
C(36,3)/C(36,5) censuses, sextet C(36,6) census) needed by the k=36
main computation's load/assert chain.  The k=33 and k=34 main result
JSONs are already published (commits b7ec3ebd / b64d8fe1, crosscheck
extension d7001467), so the k=35 main computation pins the published
k=34 result and regresses against it in addition to this preread.''',
'''row-multiplicity classifiers, regresses the published rank-35 preread
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
it in addition to this preread.''')
do("Usage: python3 cost16_survival_k36_preread_20261118.py [--local DIR] [--out PATH]",
   "Usage: python3 cost16_survival_k37_preread_20261119.py [--local DIR] [--out PATH]")

# ------------------------------------------------------------ constants
do('''PINS = {
    "agg": ("cost16-b-phase-groups-20261118.json", "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"),
    "k34pre": ("cost16-survival-k34-preread-20261118.json",
               "8dbb1bcbdaed9bee475f3b95932d35a9500e62cb"),
    "k35pre": ("cost16-survival-k35-preread-20261118.json",
               "490fa3a00b8e0b19229c94aa6b1aba4a5604ec13"),
}
# sha1s the pinned k35 preread must declare as its inputs (publication
# chain: the k35 preread consumed the aggregate and the k33/k34
# preread artifacts)
K33PRE_SHA = "e4346ddd7e08799b4406dcdba930de714e4f462c"''',
'''PINS = {
    "agg": ("cost16-b-phase-groups-20261118.json", "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"),
    "k35pre": ("cost16-survival-k35-preread-20261118.json",
               "490fa3a00b8e0b19229c94aa6b1aba4a5604ec13"),
    "k36pre": ("cost16-survival-k36-preread-20261118.json",
               "760aa396361cc7d2ea8bc371f4dd673d962f07fe"),
}
# sha1s the pinned k36 preread must declare as its inputs (publication
# chain: the k36 preread consumed the aggregate and the k34/k35
# preread artifacts)
K34PRE_SHA = "8dbb1bcbdaed9bee475f3b95932d35a9500e62cb"''')
do("RANK = 36      # 1-based top50 rank of the new root",
   "RANK = 37      # 1-based top50 rank of the new root")

# ------------------------------------------------------------ fetch chain
do('''    agg = fetch(*PINS["agg"], args.local)
    k34pre = fetch(*PINS["k34pre"], args.local)
    k35pre = fetch(*PINS["k35pre"], args.local)
    if not (k34pre.get("all_pass") and k34pre.get("check_count") == 33):
        print("FAIL k34 preread all_pass/check_count unexpected")
        return 1
    if not (k35pre.get("all_pass") and k35pre.get("check_count") == 33):
        print("FAIL k35 preread all_pass/check_count unexpected")
        return 1''',
'''    agg = fetch(*PINS["agg"], args.local)
    k35pre = fetch(*PINS["k35pre"], args.local)
    k36pre = fetch(*PINS["k36pre"], args.local)
    if not (k35pre.get("all_pass") and k35pre.get("check_count") == 33):
        print("FAIL k35 preread all_pass/check_count unexpected")
        return 1
    if not (k36pre.get("all_pass") and k36pre.get("check_count") == 33):
        print("FAIL k36 preread all_pass/check_count unexpected")
        return 1''')

# ------------------------------------------------------------ declares check
do('''    # 2. publication chain: the pinned k35 preread declares the pinned
    #    aggregate, k33 preread and k34 preread it consumed
    in_pins = {k: v["git_blob_sha1"] for k, v in k35pre["inputs"].items()
               if isinstance(v, dict) and "git_blob_sha1" in v}
    check("k35_preread_declares_pinned_inputs",
          in_pins.get("aggregate") == PINS["agg"][1]
          and in_pins.get("k33_preread") == K33PRE_SHA
          and in_pins.get("k34_preread") == PINS["k34pre"][1],
          {"declared": in_pins, "pinned_agg": PINS["agg"][1],
           "pinned_k33pre": K33PRE_SHA, "pinned_k34pre": PINS["k34pre"][1]})''',
'''    # 2. publication chain: the pinned k36 preread declares the pinned
    #    aggregate, k34 preread and k35 preread it consumed
    in_pins = {k: v["git_blob_sha1"] for k, v in k36pre["inputs"].items()
               if isinstance(v, dict) and "git_blob_sha1" in v}
    check("k36_preread_declares_pinned_inputs",
          in_pins.get("aggregate") == PINS["agg"][1]
          and in_pins.get("k34_preread") == K34PRE_SHA
          and in_pins.get("k35_preread") == PINS["k35pre"][1],
          {"declared": in_pins, "pinned_agg": PINS["agg"][1],
           "pinned_k34pre": K34PRE_SHA, "pinned_k35pre": PINS["k35pre"][1]})''')

# ------------------------------------------------------------ sections: rank-34 + rank-35 -> rank-35 + rank-36
A1 = "    # ---- rank-34 regression (vs the pinned published k34 preread JSON)\n"
B1 = "    # ---- rank-36 facts (all machine-derived from the pinned aggregate)\n"
assert text.count(A1) == 1 and text.count(B1) == 1
i = text.index(A1)
j = text.index(B1)
old_sections = text[i:j]
# sanity: the replaced region contains both old sections
assert 'n = 34' in old_sections and 'n = 35' in old_sections
assert old_sections.count("reg[n] = {") == 2

SECTIONS = '''    # ---- rank-35 regression (vs the pinned published k35 preread JSON)
    reg = {}
    n = 35
    idx = n - 1
    pub35 = k35pre["rank35"]
    prior = {}
    for r in rows[idx]:
        prior[r] = [i for i in range(idx) if r in rows[i]]
    pc, _, pcmp, pmis = new_census(rows, idx, 2)
    shared = idx - pc["disjoint"]
    tc, ttwos, tcmp, tmis = new_census(rows, idx, 3)
    qc, qtwos, qcmp, qmis = new_census(rows, idx, 4)
    uc, utwos, ucmp, umis = new_census(rows, idx, 5)
    new_quint_b_only = []
    for c in itertools.combinations(range(idx), 4):
        cl, two = classify_a(rows, (idx,) + c)
        if cl == "b_only":
            new_quint_b_only.append((idx,) + c)
    profiles = {}
    for five in new_quint_b_only:
        k = profile_of(rows, five)
        profiles[k] = profiles.get(k, 0) + 1
    dusizes = {}
    for c in itertools.combinations(range(idx), 3):
        combo = (idx,) + c
        cl, _ = classify_a(rows, combo)
        if cl == "disjoint":
            u = set()
            for i in combo:
                u |= set(rows[i])
            dusizes[len(u)] = dusizes.get(len(u), 0) + 1
    ful3, f3twos, f3cmp, f3mis = census(rows, itertools.combinations(range(n), 3))
    ful5, f5twos, f5cmp, f5mis = census(rows, itertools.combinations(range(n), 5))
    six, _, s6cmp, s6mis = census(rows, itertools.combinations(range(n), 6))
    check(f"rank{n}_root_matches_published_preread",
          pub35["root"] == "00000000000000801202090000001000" == top[idx]["root"]
          and sorted(pub35["rows"]) == sorted(rows[idx]) == [18, 21]
          and int(pub35["membership"]) == int(mem[idx]) == 120058481266728720
          and int(pub35["a_part"]) == 92036253749417268
          and int(pub35["b_part"]) == 28022227517311452,
          {"root": pub35["root"], "rows": sorted(rows[idx]), "membership": int(mem[idx])})
    check(f"rank{n}_prior_hits_match_published_preread",
          prior == {18: [1, 4, 5, 6, 7, 11, 12, 18, 19, 20, 21, 23, 24, 26, 27, 30], 21: []}
          and {k: sorted(v) for k, v in pub35["prior_hit_indices"].items()}
          == {str(r): v for r, v in sorted(prior.items())},
          {str(r): v for r, v in sorted(prior.items())})
    check(f"rank{n}_new_census_matches_published_preread",
          pub35["new_census"]["pair"]["shared"] == shared
          and pub35["new_census"]["pair"]["disjoint"] == pc["disjoint"]
          and pub35["new_census"]["triple"]["b_only"] == tc["b_only"]
          and pub35["new_census"]["triple"]["zero"] == tc["zero"]
          and pub35["new_census"]["triple"]["disjoint"] == tc["disjoint"]
          and pub35["new_census"]["quad"]["b_only"] == qc["b_only"]
          and pub35["new_census"]["quad"]["zero"] == qc["zero"]
          and pub35["new_census"]["quad"]["disjoint"] == qc["disjoint"]
          and pub35["new_census"]["quint"]["b_only"] == uc["b_only"]
          and pub35["new_census"]["quint"]["zero"] == uc["zero"]
          and pub35["new_census"]["quint"]["disjoint"] == uc["disjoint"]
          and tc == {"b_only": 348, "zero": 133, "disjoint": 80}
          and qc == {"b_only": 1612, "zero": 4289, "disjoint": 83}
          and uc == {"b_only": 1595, "zero": 44781, "disjoint": 0},
          {"triple": tc, "quad": qc, "quint": uc})
    check(f"rank{n}_histograms_and_disjoint_quads_match_published_preread",
          {int(k): v for k, v in pub35["new_triple_double_row_histogram"].items()} == ttwos
          and {int(k): v for k, v in pub35["new_quad_double_row_histogram"].items()} == qtwos
          and {int(k): v for k, v in pub35["new_quint_double_row_histogram"].items()} == utwos
          and {str(k): v for k, v in pub35["b_only_quint_four_subset_profiles"].items()} == profiles
          and profiles == {"3/2/0": uc["b_only"]}
          and pub35["disjoint_quad_count"] == qc["disjoint"] == 83
          and {int(k): v for k, v in pub35["disjoint_quad_union_sizes"].items()} == dusizes
          and set(dusizes) == {8}
          and pub35["cumulative_disjoint_quads"] == 1112 + qc["disjoint"] == 1195,
          {"disjoint_union_sizes": dusizes, "cumulative": 1112 + qc["disjoint"]})
    check(f"rank{n}_full_census_matches_published_preread",
          pub35["full_triples"]["counts"] == ful3
          and ful3 == {"b_only": 3970, "zero": 1257, "disjoint": 1318}
          and {int(k): v for k, v in pub35["full_triples"]["double_row_histogram"].items()} == f3twos
          and pub35["full_quints"]["counts"] == ful5
          and ful5 == {"b_only": 14599, "zero": 310033, "disjoint": 0}
          and {int(k): v for k, v in pub35["full_quints"]["double_row_histogram"].items()} == f5twos
          and pub35["sextet_census"]["counts"] == six
          and six == {"b_only": 0, "zero": math.comb(35, 6), "disjoint": 0},
          {"full_triples": ful3, "full_quints": ful5, "sextet": six})
    check(f"rank{n}_era_continuation_matches_k35_preread_rank34_regression",
          ful5["b_only"] - uc["b_only"] == 13004
          and k35pre["rank34_regression"]["full_quints"]["counts"]["b_only"] == 13004
          and ful5["zero"] - uc["zero"] == 265252
          and k35pre["rank34_regression"]["full_quints"]["counts"]["zero"] == 265252
          and ful5["disjoint"] == 0,
          {"prev_b_only": 13004,
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"]})
    check(f"rank{n}_two_classifiers_agree",
          pmis == tmis == qmis == umis == f3mis == f5mis == s6mis == 0,
          {"comparisons": pcmp + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
           "mismatches": pmis + tmis + qmis + umis + f3mis + f5mis + s6mis})
    reg[n] = {
        "root": top[idx]["root"],
        "rows": sorted(rows[idx]),
        "membership": int(mem[idx]),
        "a_part": int(memA[top[idx]["root"]]),
        "b_part": int(memB[top[idx]["root"]]),
        "prior_hits": {str(r): len(v) for r, v in sorted(prior.items())},
        "prior_hit_indices": {str(r): v for r, v in sorted(prior.items())},
        "new_census": {
            "pair": {"b_only": shared, "zero": 0, "disjoint": pc["disjoint"],
                     "total": idx, "expected_total": idx},
            "triple": {**tc, "total": sum(tc.values()), "expected_total": math.comb(idx, 2)},
            "quad": {**qc, "total": sum(qc.values()), "expected_total": math.comb(idx, 3)},
            "quint": {**uc, "total": sum(uc.values()), "expected_total": math.comb(idx, 4)},
        },
        "new_quint_double_row_histogram": utwos,
        "new_triple_double_row_histogram": ttwos,
        "new_quad_double_row_histogram": qtwos,
        "b_only_quint_four_subset_profiles": {k: profiles[k] for k in sorted(profiles)},
        "full_triples": {"counts": ful3, "total": math.comb(n, 3),
                         "double_row_histogram": f3twos},
        "full_quints": {"counts": ful5, "total": math.comb(n, 5),
                        "double_row_histogram": f5twos},
        "sextet_census": {"total": math.comb(n, 6), "counts": six},
        "classifier_comparisons": idx + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
        "mismatches": 0,
    }

    # ---- rank-36 regression (vs the pinned published k36 preread JSON)
    n = 36
    idx = n - 1
    pub36 = k36pre["rank36"]
    prior = {}
    for r in rows[idx]:
        prior[r] = [i for i in range(idx) if r in rows[i]]
    pc, _, pcmp, pmis = new_census(rows, idx, 2)
    shared = idx - pc["disjoint"]
    tc, ttwos, tcmp, tmis = new_census(rows, idx, 3)
    qc, qtwos, qcmp, qmis = new_census(rows, idx, 4)
    uc, utwos, ucmp, umis = new_census(rows, idx, 5)
    new_quint_b_only = []
    for c in itertools.combinations(range(idx), 4):
        cl, two = classify_a(rows, (idx,) + c)
        if cl == "b_only":
            new_quint_b_only.append((idx,) + c)
    profiles = {}
    for five in new_quint_b_only:
        k = profile_of(rows, five)
        profiles[k] = profiles.get(k, 0) + 1
    dusizes = {}
    for c in itertools.combinations(range(idx), 3):
        combo = (idx,) + c
        cl, _ = classify_a(rows, combo)
        if cl == "disjoint":
            u = set()
            for i in combo:
                u |= set(rows[i])
            dusizes[len(u)] = dusizes.get(len(u), 0) + 1
    ful3, f3twos, f3cmp, f3mis = census(rows, itertools.combinations(range(n), 3))
    ful5, f5twos, f5cmp, f5mis = census(rows, itertools.combinations(range(n), 5))
    six, _, s6cmp, s6mis = census(rows, itertools.combinations(range(n), 6))
    check(f"rank{n}_root_matches_published_preread",
          pub36["root"] == "00000000000000801212020000001000" == top[idx]["root"]
          and sorted(pub36["rows"]) == sorted(rows[idx]) == [19, 22]
          and int(pub36["membership"]) == int(mem[idx]) == 120046727515486665
          and int(pub36["a_part"]) == 92003630985566871
          and int(pub36["b_part"]) == 28043096529919794,
          {"root": pub36["root"], "rows": sorted(rows[idx]), "membership": int(mem[idx])})
    check(f"rank{n}_prior_hits_match_published_preread",
          prior == {19: [0, 2, 3, 8, 9, 10, 15, 29, 32, 33], 22: []}
          and {k: sorted(v) for k, v in pub36["prior_hit_indices"].items()}
          == {str(r): v for r, v in sorted(prior.items())},
          {str(r): v for r, v in sorted(prior.items())})
    check(f"rank{n}_new_census_matches_published_preread",
          pub36["new_census"]["pair"]["shared"] == shared
          and pub36["new_census"]["pair"]["disjoint"] == pc["disjoint"]
          and pub36["new_census"]["triple"]["b_only"] == tc["b_only"]
          and pub36["new_census"]["triple"]["zero"] == tc["zero"]
          and pub36["new_census"]["triple"]["disjoint"] == tc["disjoint"]
          and pub36["new_census"]["quad"]["b_only"] == qc["b_only"]
          and pub36["new_census"]["quad"]["zero"] == qc["zero"]
          and pub36["new_census"]["quad"]["disjoint"] == qc["disjoint"]
          and pub36["new_census"]["quint"]["b_only"] == uc["b_only"]
          and pub36["new_census"]["quint"]["zero"] == uc["zero"]
          and pub36["new_census"]["quint"]["disjoint"] == uc["disjoint"]
          and tc == {"b_only": 391, "zero": 63, "disjoint": 141}
          and qc == {"b_only": 2458, "zero": 3919, "disjoint": 168}
          and uc == {"b_only": 2835, "zero": 49525, "disjoint": 0},
          {"triple": tc, "quad": qc, "quint": uc})
    check(f"rank{n}_histograms_and_disjoint_quads_match_published_preread",
          {int(k): v for k, v in pub36["new_triple_double_row_histogram"].items()} == ttwos
          and {int(k): v for k, v in pub36["new_quad_double_row_histogram"].items()} == qtwos
          and {int(k): v for k, v in pub36["new_quint_double_row_histogram"].items()} == utwos
          and {str(k): v for k, v in pub36["b_only_quint_four_subset_profiles"].items()} == profiles
          and profiles == {"3/2/0": uc["b_only"]}
          and pub36["disjoint_quad_count"] == qc["disjoint"] == 168
          and {int(k): v for k, v in pub36["disjoint_quad_union_sizes"].items()} == dusizes
          and set(dusizes) == {8}
          and pub36["cumulative_disjoint_quads"] == 1195 + qc["disjoint"] == 1363,
          {"disjoint_union_sizes": dusizes, "cumulative": 1195 + qc["disjoint"]})
    check(f"rank{n}_full_census_matches_published_preread",
          pub36["full_triples"]["counts"] == ful3
          and ful3 == {"b_only": 4361, "zero": 1320, "disjoint": 1459}
          and {int(k): v for k, v in pub36["full_triples"]["double_row_histogram"].items()} == f3twos
          and pub36["full_quints"]["counts"] == ful5
          and ful5 == {"b_only": 17434, "zero": 359558, "disjoint": 0}
          and {int(k): v for k, v in pub36["full_quints"]["double_row_histogram"].items()} == f5twos
          and pub36["sextet_census"]["counts"] == six
          and six == {"b_only": 0, "zero": math.comb(36, 6), "disjoint": 0},
          {"full_triples": ful3, "full_quints": ful5, "sextet": six})
    check(f"rank{n}_era_continuation_matches_k36_preread_rank35_regression",
          ful5["b_only"] - uc["b_only"] == 14599
          and k36pre["rank35_regression"]["full_quints"]["counts"]["b_only"] == 14599
          and ful5["zero"] - uc["zero"] == 310033
          and k36pre["rank35_regression"]["full_quints"]["counts"]["zero"] == 310033
          and ful5["disjoint"] == 0,
          {"prev_b_only": 14599,
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"]})
    check(f"rank{n}_two_classifiers_agree",
          pmis == tmis == qmis == umis == f3mis == f5mis == s6mis == 0,
          {"comparisons": pcmp + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
           "mismatches": pmis + tmis + qmis + umis + f3mis + f5mis + s6mis})
    reg[n] = {
        "root": top[idx]["root"],
        "rows": sorted(rows[idx]),
        "membership": int(mem[idx]),
        "a_part": int(memA[top[idx]["root"]]),
        "b_part": int(memB[top[idx]["root"]]),
        "prior_hits": {str(r): len(v) for r, v in sorted(prior.items())},
        "prior_hit_indices": {str(r): v for r, v in sorted(prior.items())},
        "new_census": {
            "pair": {"b_only": shared, "zero": 0, "disjoint": pc["disjoint"],
                     "total": idx, "expected_total": idx},
            "triple": {**tc, "total": sum(tc.values()), "expected_total": math.comb(idx, 2)},
            "quad": {**qc, "total": sum(qc.values()), "expected_total": math.comb(idx, 3)},
            "quint": {**uc, "total": sum(uc.values()), "expected_total": math.comb(idx, 4)},
        },
        "new_quint_double_row_histogram": utwos,
        "new_triple_double_row_histogram": ttwos,
        "new_quad_double_row_histogram": qtwos,
        "b_only_quint_four_subset_profiles": {k: profiles[k] for k in sorted(profiles)},
        "full_triples": {"counts": ful3, "total": math.comb(n, 3),
                         "double_row_histogram": f3twos},
        "full_quints": {"counts": ful5, "total": math.comb(n, 5),
                        "double_row_histogram": f5twos},
        "sextet_census": {"total": math.comb(n, 6), "counts": six},
        "classifier_comparisons": idx + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
        "mismatches": 0,
    }

'''
text = text[:i] + SECTIONS + text[j:]

# ------------------------------------------------------------ facts: rank-36 -> rank-37
A2 = "    # ---- rank-36 facts (all machine-derived from the pinned aggregate)\n"
assert text.count(A2) == 1
END2 = "\n    out = {"
assert text.count(END2) == 1
i2 = text.index(A2)
j2 = text.index(END2)

FACTS = '''    # ---- rank-37 facts (all machine-derived from the pinned aggregate)
    root = top[IDX]["root"]
    m37 = int(mem[IDX])
    a37 = int(memA[root])
    b37 = int(memB[root])
    prior = {}
    for r in rows[IDX]:
        prior[r] = [i for i in range(IDX) if r in rows[i]]

    pc, _, pcmp, pmis = new_census(rows, IDX, 2)
    shared = IDX - pc["disjoint"]
    tc, ttwos, tcmp, tmis = new_census(rows, IDX, 3)
    qc, qtwos, qcmp, qmis = new_census(rows, IDX, 4)
    uc, utwos, ucmp, umis = new_census(rows, IDX, 5)
    new_quint_b_only = []
    for c in itertools.combinations(range(IDX), 4):
        cl, two = classify_a(rows, (IDX,) + c)
        if cl == "b_only":
            new_quint_b_only.append((IDX,) + c)
    profiles = {}
    for five in new_quint_b_only:
        k = profile_of(rows, five)
        profiles[k] = profiles.get(k, 0) + 1
    dusizes = {}
    for c in itertools.combinations(range(IDX), 3):
        combo = (IDX,) + c
        cl, _ = classify_a(rows, combo)
        if cl == "disjoint":
            u = set()
            for i in combo:
                u |= set(rows[i])
            dusizes[len(u)] = dusizes.get(len(u), 0) + 1
    ful3, f3twos, f3cmp, f3mis = census(rows, itertools.combinations(range(RANK), 3))
    ful5, f5twos, f5cmp, f5mis = census(rows, itertools.combinations(range(RANK), 5))
    six, _, s6cmp, s6mis = census(rows, itertools.combinations(range(RANK), 6))

    check("rank37_root_matches_top50",
          root == "00000000080000003800000108001000"
          and sorted(rows[IDX]) == [8, 19],
          {"root": root, "rows": sorted(rows[IDX])})
    check("rank37_prior_hits_recorded",
          prior == {8: [23], 19: [0, 2, 3, 8, 9, 10, 15, 29, 32, 33, 35]},
          {str(k): v for k, v in sorted(prior.items())})
    check("rank37_membership_split_identity",
          a37 + b37 == m37
          and m37 == 119973409932394637
          and m37 < int(reg[36]["membership"]),
          {"membership": m37, "a_part": a37, "b_part": b37})
    check("rank37_new_pair_census",
          pc["disjoint"] == IDX - shared and shared == 12 and pc["disjoint"] == 24,
          {"shared": shared, "disjoint": pc["disjoint"], "total": IDX})
    check("rank37_new_triple_census",
          tc["b_only"] + tc["zero"] + tc["disjoint"] == math.comb(IDX, 2)
          and tc == {"b_only": 397, "zero": 100, "disjoint": 133}, tc)
    check("rank37_new_quad_census",
          qc["b_only"] + qc["zero"] + qc["disjoint"] == math.comb(IDX, 3)
          and qc == {"b_only": 2394, "zero": 4589, "disjoint": 157}, qc)
    check("rank37_new_quint_census",
          uc["b_only"] + uc["zero"] + uc["disjoint"] == math.comb(IDX, 4)
          and uc["b_only"] == len(new_quint_b_only)
          and uc["zero"] == math.comb(IDX, 4) - uc["b_only"]
          and uc == {"b_only": 2722, "zero": 56183, "disjoint": 0},
          {**uc, "records": len(new_quint_b_only)})
    check("rank37_new_quint_double_rows",
          sum(utwos.values()) == uc["b_only"] and 8 not in utwos and 19 in utwos
          and utwos == {15: 339, 16: 71, 18: 1043, 19: 1269}, utwos)
    check("rank37_b_only_quint_profiles",
          profiles == {"3/2/0": uc["b_only"]}, profiles)
    check("rank37_disjoint_quads_union8",
          sum(dusizes.values()) == qc["disjoint"] and set(dusizes) == {8}
          and qc["disjoint"] == 157,
          {"disjoint_quad_count": qc["disjoint"], "union_sizes": dusizes,
           "cumulative_disjoint_quads": 1363 + qc["disjoint"]})
    dj37 = sum(1 for c in itertools.combinations(range(RANK), 4)
               if classify_a(rows, c)[0] == "disjoint")
    check("rank37_cumulative_disjoint_quads_global_recount",
          dj37 == 1520 and dj37 == 1363 + qc["disjoint"]
          and dj37 == pub36["cumulative_disjoint_quads"] + qc["disjoint"],
          {"global_C37_4": dj37, "prev_cumulative": pub36["cumulative_disjoint_quads"],
           "new": qc["disjoint"]})
    check("rank37_full_census_totals",
          ful3["b_only"] + ful3["zero"] + ful3["disjoint"] == math.comb(RANK, 3)
          and ful5["b_only"] + ful5["zero"] + ful5["disjoint"] == math.comb(RANK, 5)
          and sum(f5twos.values()) == ful5["b_only"]
          and ful3 == {"b_only": 4758, "zero": 1420, "disjoint": 1592}
          and ful5 == {"b_only": 20156, "zero": 415741, "disjoint": 0}
          and f5twos == {15: 3124, 16: 616, 18: 10260, 19: 6156},
          {"full_triples": ful3, "full_quints": ful5, "quint_double_rows": f5twos})
    check("rank37_quint_era_continuation",
          ful5["b_only"] - uc["b_only"] == reg[36]["full_quints"]["counts"]["b_only"]
          and ful5["zero"] - uc["zero"] == reg[36]["full_quints"]["counts"]["zero"]
          and ful5["disjoint"] == 0,
          {"prev_b_only": reg[36]["full_quints"]["counts"]["b_only"],
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"],
           "prev_zero": reg[36]["full_quints"]["counts"]["zero"],
           "new_zero": uc["zero"], "full_zero": ful5["zero"]})
    check("rank37_single_share_row_8_doubles_triple_quad_only",
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
           "row8_prior_sharers": prior[8]})
    check("rank37_sextet_census_all_zero",
          six == {"b_only": 0, "zero": math.comb(RANK, 6), "disjoint": 0},
          {"total": math.comb(RANK, 6), **six})
    check("rank37_expected_totals",
          math.comb(RANK, 3) == 7770 and math.comb(IDX, 2) == 630
          and math.comb(IDX, 3) == 7140 and math.comb(IDX, 4) == 58905
          and math.comb(RANK, 5) == 435897 and math.comb(RANK, 6) == 2324784,
          {"C36_2": math.comb(IDX, 2), "C36_3": math.comb(IDX, 3), "C36_4": math.comb(IDX, 4),
           "C37_3": math.comb(RANK, 3), "C37_5": math.comb(RANK, 5), "C37_6": math.comb(RANK, 6)})
    check("rank37_two_classifiers_agree",
          pmis == tmis == qmis == umis == f3mis == f5mis == s6mis == 0,
          {"comparisons": pcmp + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp,
           "mismatches": pmis + tmis + qmis + umis + f3mis + f5mis + s6mis})

    rank37 = {
        "root": root,
        "rows": sorted(rows[IDX]),
        "membership": m37,
        "a_part": a37,
        "b_part": b37,
        "prior_hits": {str(r): len(v) for r, v in sorted(prior.items())},
        "prior_hit_indices": {str(r): v for r, v in sorted(prior.items())},
        "note": ("rank-37 (8,19) has no fresh row: row 8 arrives with a single "
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
                 "k=33/k=34."),
        "new_census": {
            "pair": {"shared": shared, "disjoint": pc["disjoint"],
                     "total": IDX, "expected_total": IDX},
            "triple": {**tc, "total": sum(tc.values()), "expected_total": math.comb(IDX, 2)},
            "quad": {**qc, "total": sum(qc.values()), "expected_total": math.comb(IDX, 3)},
            "quint": {**uc, "total": sum(uc.values()), "expected_total": math.comb(IDX, 4)},
        },
        "new_quint_double_row_histogram": utwos,
        "new_triple_double_row_histogram": ttwos,
        "new_quad_double_row_histogram": qtwos,
        "b_only_quint_four_subset_profiles": {k: profiles[k] for k in sorted(profiles)},
        "disjoint_quad_count": qc["disjoint"],
        "disjoint_quad_union_sizes": {str(k): v for k, v in sorted(dusizes.items())},
        "cumulative_disjoint_quads": 1363 + qc["disjoint"],
        "full_triples": {"counts": ful3, "total": math.comb(RANK, 3),
                         "double_row_histogram": f3twos,
                         "compared": math.comb(RANK, 3), "mismatches": f3mis},
        "full_quints": {"counts": ful5, "total": math.comb(RANK, 5),
                        "double_row_histogram": f5twos,
                        "compared": math.comb(RANK, 5), "mismatches": f5mis},
        "sextet_census": {"total": math.comb(RANK, 6), "counts": six,
                          "compared": math.comb(RANK, 6), "mismatches": s6mis},
    }'''
text = text[:i2] + FACTS + text[j2:]

# ------------------------------------------------------------ out dict
do('''        "schema": "n11-cost16-k36-preread-20261119-v1",''',
'''        "schema": "n11-cost16-k37-preread-20261119-v1",''')
do('"31-row cost-16 parent: rank-36 structural preread"',
   '"31-row cost-16 parent: rank-37 structural preread"')
do('''        "language_note": ("pure Python with exact integer serialization (following the "
                          "k=32/k=33/k=34/k=35 preread scripts); the rank-34 regression "
                          "layer compares against the pinned published k=34 preread JSON "
                          "and the rank-35 regression layer against the pinned published "
                          "k=35 preread JSON; the k=33 and k=34 main result JSONs are "
                          "already published (commits b7ec3ebd / b64d8fe1, crosscheck "
                          "extension d7001467), so the k=35 main computation pins the "
                          "published k=34 result and regresses against it as well; the "
                          "k=36 main computation will pin the published k=35 result and "
                          "this preread."),''',
'''        "language_note": ("pure Python with exact integer serialization (following the "
                          "k=32/k=33/k=34/k=35/k=36 preread scripts); the rank-35 "
                          "regression layer compares against the pinned published k=35 "
                          "preread JSON and the rank-36 regression layer against the "
                          "pinned published k=36 preread JSON; the k=35 and k=36 main "
                          "result JSONs are already published (commits 572b1365 / "
                          "6fcea02c) and the k=35/k=36 crosscheck extensions are "
                          "published (latest 259 checks, all pass, 2026-11-19), so the "
                          "k=37 main computation pins the published k=36 result and "
                          "regresses against it as well; this preread adds the "
                          "single-share row-8 structural check, so check_count is 34."),''')
do('''            "k34_preread": {"path": f"{PATH}/cost16-survival-k34-preread-20261118.json",
                            "git_blob_sha1": PINS["k34pre"][1],
                            "commit": "2a14f351"},
            "k35_preread": {"path": f"{PATH}/cost16-survival-k35-preread-20261118.json",
                            "git_blob_sha1": PINS["k35pre"][1],
                            "commit": "90fc51c9"},
            "k34_preread_independent_verification": (
                "verify_cost16_k34_preread_independent_20261118.py, "
                "commit a450e366, 30 checks 0 failures (second derivation lineage)"),
            "k35_preread_independent_verification": (
                "verify_cost16_k35_preread_independent Python script not yet "
                "published; the k=35 preread JSON was value-verified on 2026-11-19 "
                "against a second derivation lineage (independent re-derivation, "
                "all fields matched, two runs); the independent script follows the "
                "k=32/k=33/k=34 pattern and will be published"),''',
'''            "k35_preread": {"path": f"{PATH}/cost16-survival-k35-preread-20261118.json",
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
                "re-run produced byte-identical output"),''')
do('"rank_convention": "top50_by_membership; 1-based rank 36"',
   '"rank_convention": "top50_by_membership; 1-based rank 37"')
do('''        "rank34_regression": reg[34],
        "rank35_regression": reg[35],
        "rank36": rank36,''',
'''        "rank35_regression": reg[35],
        "rank36_regression": reg[36],
        "rank37": rank37,''')

# serialization check
do('''    back = json.loads(text)
    ok = (back["rank36"]["membership"] == m36
          and back["rank36"]["a_part"] == a36 and back["rank36"]["b_part"] == b36
          and back["rank34_regression"]["membership"] == int(mem[33])
          and back["rank35_regression"]["membership"] == int(mem[34])
          and back["rank34_regression"]["a_part"] == int(memA[top[33]["root"]])
          and back["rank34_regression"]["b_part"] == int(memB[top[33]["root"]])
          and back["rank35_regression"]["a_part"] == int(memA[top[34]["root"]])
          and back["rank35_regression"]["b_part"] == int(memB[top[34]["root"]]))
    checks.append({"name": "rank36_exact_integer_json_serialization", "pass": bool(ok),
                   "detail": {"membership": m36, "a_part": a36, "b_part": b36}})''',
'''    back = json.loads(text)
    ok = (back["rank37"]["membership"] == m37
          and back["rank37"]["a_part"] == a37 and back["rank37"]["b_part"] == b37
          and back["rank35_regression"]["membership"] == int(mem[34])
          and back["rank36_regression"]["membership"] == int(mem[35])
          and back["rank35_regression"]["a_part"] == int(memA[top[34]["root"]])
          and back["rank35_regression"]["b_part"] == int(memB[top[34]["root"]])
          and back["rank36_regression"]["a_part"] == int(memA[top[35]["root"]])
          and back["rank36_regression"]["b_part"] == int(memB[top[35]["root"]]))
    checks.append({"name": "rank37_exact_integer_json_serialization", "pass": bool(ok),
                   "detail": {"membership": m37, "a_part": a37, "b_part": b37}})''')

# final prints
do('print(f"rank-36 root {root} rows {sorted(rows[IDX])} m36 {m36} (A {a36} / B {b36})")',
   'print(f"rank-37 root {root} rows {sorted(rows[IDX])} m37 {m37} (A {a37} / B {b37})")')
do('print(f"full C(36,5): {ful5}  sextet C(36,6): {six}")',
   'print(f"full C(37,5): {ful5}  sextet C(37,6): {six}")')
do('default="output/cost16-survival-k36-preread-20261118.json"',
   'default="output/cost16-survival-k37-preread-20261119.json"')

# ------------------------------------------------------------ final sanity
assert 'PINS["k34pre"]' not in text, "leftover PINS k34pre reference"
assert "k34pre = " not in text, "leftover k34pre variable"
assert "pub34" not in text, "leftover pub34 variable"
assert "K33PRE_SHA" not in text, "leftover K33PRE_SHA"
assert '"rank34_regression":' not in text
assert "rank-36 regression" in text and "rank-35 regression" in text
assert "rank37" in text
# 34 checks + the def/append helpers
assert text.count("check(") == 34, text.count("check(")

with open(DST, "w", encoding="utf-8") as fh:
    fh.write(text)
print("wrote", DST, len(text), "bytes")

#!/usr/bin/env python3
"""Anchored-rep transformation: k38 preread script -> k39 preread script.

Reads base/k38pre.py (the published k=38 preread script, git blob
9102489ffa5bdb24b303d1fd073e20e541f1eeab) and writes
cost16_survival_k39_preread_20261119.py via a sequence of anchored
single-occurrence replacements plus marker surgery:

  - drop the rank-36 regression layer, keep the rank-37 regression
    layer verbatim (still against the pinned published k37 preread
    JSON, commit 98321003) as the first layer, add a rank-38
    regression layer (vs the pinned published k38 preread JSON,
    commit 75fabfd018), and reorder to ascending 37 -> 38 -> 39;
  - all rank-39 facts pre-derived by the second-derivation lineage
    (TypeScript sandbox, deterministic combination enumeration) are
    substituted as literals (root rows [5,24], m39
    119,883,868,794,265,826, A 91,824,665,662,421,012 / B
    28,059,203,131,844,814, pair 4/34, triple 319/42/342, quad
    4398/3029/1009, quint 13658/59649/508 -- the first disjoint
    quint records ever -- cumulative disjoint quads 1,677+1,009=2,686,
    C(39,3)=9,139 census 5,497/1,575/2,067, C(39,5)=575,757 census
    36,682/538,567/508, sextet C(39,6)=3,262,623 census with the first
    b_only sextets 5,852 and the level-7 zero closure over 99,122
    candidates);
  - the single-share structural check is replaced by a two-sharer
    all-layers doubling check (rows 5 and 24 each arrive with exactly
    two prior sharers and double in the triple, quad AND quint
    layers), and two new structural checks pin the k=39 I/E break
    (disjoint quint first appearance; b_only sextet first appearance
    with level-7 closure), so check_count goes 34 -> 35.

Every replacement asserts exactly one occurrence of its anchor in the
current text, so a drifted base file fails loudly instead of producing
a silently-wrong script.
"""
import hashlib
import sys

SRC = "base/k38pre.py"
DST = "cost16_survival_k39_preread_20261119.py"
EXPECT_BASE_BLOB = "9102489ffa5bdb24b303d1fd073e20e541f1eeab"

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
rep('"""Rank-38 structural preread for the 31-row cost-16 parent survival lane.',
    '"""Rank-39 structural preread for the 31-row cost-16 parent survival lane.')
rep("""re-derives the full structural census of the top-38
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
preread.""",
    """re-derives the full structural census of the top-39
pair roots from the pinned phase-B aggregate with two independent
row-multiplicity classifiers, regresses the published rank-37 preread
layer (pinned k37 preread JSON, commit 98321003, independent
bit-mask-vector second-derivation lineage commit 958057fb with erratum
059db03e) and the published rank-38 preread layer (pinned k38 preread
JSON, commit 75fabfd018, independently verified by the bit-mask-vector
lineage: independent verifier commit 126614cc48, result JSON commit
f37ddd047e, log commit 5e0ef79575, 48-check audit commit e824f6029b),
and records the rank-39 facts (root rows [5,24], prior hits,
membership split, new pair/triple/quad/quint censuses, full
C(39,3)/C(39,5) censuses, sextet C(39,6) census with the first b_only
sextets and the first disjoint quint records of the whole lane
history) needed by the k=39 main computation's load/assert chain.
The k=36 and k=37 main result JSONs are already published (commits
6fcea02c / a4a7ce31), the k=36/k=37 crosscheck extensions are
published (latest 287 checks, all pass, 2026-11-19), and the k=38
production script is published (commit 9d1b0a6a4c) with its
cross/finalize/publish owned by a single lane per the concurrency
note (commit 112a32470578), so the k=39 main computation pins the
published k=38 result once it lands and regresses against it in
addition to this preread.  Rank-39 breaks the two truncation premises
of the k=38 marginal I-E at once: the new quint layer contains 508
disjoint records (every published k=26..k=38 quint census had
disjoint == 0) and the C(39,6) sextet census contains 5,852 b_only
records (the C(38,6) census was all zero), while level 7 closes
(every 7-combo with a non-zero 6-subset is zero), so this preread pins
all three structural facts for the main computation.""")
rep("""Pure Python (following the k=32/k=33/k=34/k=35 preread scripts): all""",
    """Pure Python (following the k=32..k=38 preread scripts): all""")
rep("Usage: python3 cost16_survival_k38_preread_20261119.py [--local DIR] [--out PATH]",
    "Usage: python3 cost16_survival_k39_preread_20261119.py [--local DIR] [--out PATH]")

# ---- 2. pins / constants ----
rep("""    "k36pre": ("cost16-survival-k36-preread-20261118.json",
               "760aa396361cc7d2ea8bc371f4dd673d962f07fe"),
    "k37pre": ("cost16-survival-k37-preread-20261119.json",
               "b98ed685e772eacbd28dc3100e9813e81c27040a"),
""",
    """    "k37pre": ("cost16-survival-k37-preread-20261119.json",
               "b98ed685e772eacbd28dc3100e9813e81c27040a"),
    "k38pre": ("cost16-survival-k38-preread-20261119.json",
               "3fa8297990d8e9880f386a0cfa075e3a95f226fd"),
""")
rep("""# sha1 the pinned k37 preread must declare for the k35 preread it
# consumed (publication chain: the k37 preread consumed the aggregate
# and the k35/k36 preread artifacts; k36 is pinned above)
K35PRE_SHA = "490fa3a00b8e0b19229c94aa6b1aba4a5604ec13\"""",
    """# sha1 the pinned k38 preread must declare for the k36 preread it
# consumed (publication chain: the k38 preread consumed the aggregate
# and the k36/k37 preread artifacts; k37 is pinned above)
K36PRE_SHA = "760aa396361cc7d2ea8bc371f4dd673d962f07fe\"""")
rep("""RANK = 38      # 1-based top50 rank of the new root""",
    """RANK = 39      # 1-based top50 rank of the new root""")
rep("""ap.add_argument("--out", default="output/cost16-survival-k38-preread-20261119.json",""",
    """ap.add_argument("--out", default="output/cost16-survival-k39-preread-20261119.json",""")

# ---- 3. fetch / publication chain ----
rep("""    agg = fetch(*PINS["agg"], args.local)
    k36pre = fetch(*PINS["k36pre"], args.local)
    k37pre = fetch(*PINS["k37pre"], args.local)
    if not (k36pre.get("all_pass") and k36pre.get("check_count") == 33):
        print("FAIL k36 preread all_pass/check_count unexpected")
        return 1
    if not (k37pre.get("all_pass") and k37pre.get("check_count") == 34):
        print("FAIL k37 preread all_pass/check_count unexpected")
        return 1
""",
    """    agg = fetch(*PINS["agg"], args.local)
    k37pre = fetch(*PINS["k37pre"], args.local)
    k38pre = fetch(*PINS["k38pre"], args.local)
    if not (k37pre.get("all_pass") and k37pre.get("check_count") == 34):
        print("FAIL k37 preread all_pass/check_count unexpected")
        return 1
    if not (k38pre.get("all_pass") and k38pre.get("check_count") == 34):
        print("FAIL k38 preread all_pass/check_count unexpected")
        return 1
""")
rep("""    # 2. publication chain: the pinned k37 preread declares the pinned
    #    aggregate, k35 preread and k36 preread it consumed
    in_pins = {k: v["git_blob_sha1"] for k, v in k37pre["inputs"].items()
               if isinstance(v, dict) and "git_blob_sha1" in v}
    check("k37_preread_declares_pinned_inputs",
          in_pins.get("aggregate") == PINS["agg"][1]
          and in_pins.get("k35_preread") == K35PRE_SHA
          and in_pins.get("k36_preread") == PINS["k36pre"][1],
          {"declared": in_pins, "pinned_agg": PINS["agg"][1],
           "pinned_k35pre": K35PRE_SHA, "pinned_k36pre": PINS["k36pre"][1]})
""",
    """    # 2. publication chain: the pinned k38 preread declares the pinned
    #    aggregate, k36 preread and k37 preread it consumed
    in_pins = {k: v["git_blob_sha1"] for k, v in k38pre["inputs"].items()
               if isinstance(v, dict) and "git_blob_sha1" in v}
    check("k38_preread_declares_pinned_inputs",
          in_pins.get("aggregate") == PINS["agg"][1]
          and in_pins.get("k36_preread") == K36PRE_SHA
          and in_pins.get("k37_preread") == PINS["k37pre"][1],
          {"declared": in_pins, "pinned_agg": PINS["agg"][1],
           "pinned_k36pre": K36PRE_SHA, "pinned_k37pre": PINS["k37pre"][1]})
""")

# ---- 4. out meta ----
rep("""        "schema": "n11-cost16-k38-preread-20261119-v1",""",
    """        "schema": "n11-cost16-k39-preread-20261119-v1",""")
rep("""        "title": "31-row cost-16 parent: rank-38 structural preread",""",
    """        "title": "31-row cost-16 parent: rank-39 structural preread",""")
rep("""        "language_note": ("pure Python with exact integer serialization (following the "
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
                          "check_count stays 34."),""",
    """        "language_note": ("pure Python with exact integer serialization (following the "
                          "k=32..k=38 preread scripts); the rank-37 regression layer "
                          "compares against the pinned published k=37 preread JSON and "
                          "the rank-38 regression layer against the pinned published "
                          "k=38 preread JSON; the k=36 and k=37 main result JSONs are "
                          "already published (commits 6fcea02c / a4a7ce31) and the "
                          "k=36/k=37 crosscheck extensions are published (latest 287 "
                          "checks, all pass, 2026-11-19), while the k=38 main "
                          "computation is published as a production script (commit "
                          "9d1b0a6a4c) with cross/finalize/publish owned by a single "
                          "lane (concurrency note commit 112a32470578); this preread "
                          "replaces the single-share structural check with a two-sharer "
                          "all-layers doubling check for rows 5 and 24 and adds two "
                          "structural checks for the k=39 marginal I-E break (disjoint "
                          "quint first appearance; b_only sextet first appearance with "
                          "level-7 zero closure), so check_count goes 34 to 35."),""")
rep("""        "inputs": {
            "aggregate": {\"path\": f\"{PATH}/cost16-b-phase-groups-20261118.json\",
                          \"git_blob_sha1\": PINS[\"agg\"][1]},
            \"k36_preread\": {\"path\": f\"{PATH}/cost16-survival-k36-preread-20261118.json\",
                            \"git_blob_sha1\": PINS[\"k36pre\"][1],
                            \"commit\": \"67985e92\"},
            \"k37_preread\": {\"path\": f\"{PATH}/cost16-survival-k37-preread-20261119.json\",
                            \"git_blob_sha1\": PINS[\"k37pre\"][1],
                            \"commit\": \"98321003\"},
            \"k36_preread_independent_verification\": (
                \"Proxmox runner reproduction (commit fc46f01e): the same script \"
                \"re-run produced byte-identical output\"),
            \"k37_preread_independent_verification\": (
                \"bit-mask-vector second derivation lineage (commit 958057fb, \"
                \"erratum 059db03e): the independent re-derivation agreed on \"
                \"every machine-derived fact\"),
        },""",
    """        "inputs": {
            "aggregate": {\"path\": f\"{PATH}/cost16-b-phase-groups-20261118.json\",
                          \"git_blob_sha1\": PINS[\"agg\"][1]},
            \"k37_preread\": {\"path\": f\"{PATH}/cost16-survival-k37-preread-20261119.json\",
                            \"git_blob_sha1\": PINS[\"k37pre\"][1],
                            \"commit\": \"98321003\"},
            \"k38_preread\": {\"path\": f\"{PATH}/cost16-survival-k38-preread-20261119.json\",
                            \"git_blob_sha1\": PINS[\"k38pre\"][1],
                            \"commit\": \"75fabfd018\"},
            \"k37_preread_independent_verification\": (
                \"bit-mask-vector second derivation lineage (commit 958057fb, \"
                \"erratum 059db03e): the independent re-derivation agreed on \"
                \"every machine-derived fact\"),
            \"k38_preread_independent_verification\": (
                \"bit-mask-vector independent verification (independent verifier \"
                \"commit 126614cc48, result JSON commit f37ddd047e, log commit \"
                \"5e0ef79575, 48-check audit commit e824f6029b): the independent \"
                \"re-derivation agreed on every machine-derived fact\"),
        },""")
rep("""            "rank_convention": "top50_by_membership; 1-based rank 38",""",
    """            "rank_convention": "top50_by_membership; 1-based rank 39",""")
rep("""        "rank36_regression": reg[36],
        "rank37_regression": reg[37],
        "rank38": rank38,""",
    """        "rank37_regression": reg[37],
        "rank38_regression": reg[38],
        "rank39": rank39,""")

# ---- 5. final serialization check and prints ----
rep("""    ok = (back["rank38"]["membership"] == m38
          and back["rank38"]["a_part"] == a38 and back["rank38"]["b_part"] == b38
          and back["rank36_regression"]["membership"] == int(mem[35])
          and back["rank37_regression"]["membership"] == int(mem[36])
          and back["rank36_regression"]["a_part"] == int(memA[top[35]["root"]])
          and back["rank36_regression"]["b_part"] == int(memB[top[35]["root"]])
          and back["rank37_regression"]["a_part"] == int(memA[top[36]["root"]])
          and back["rank37_regression"]["b_part"] == int(memB[top[36]["root"]]))
    checks.append({"name": "rank38_exact_integer_json_serialization", "pass": bool(ok),
                   "detail": {"membership": m38, "a_part": a38, "b_part": b38}})""",
    """    ok = (back["rank39"]["membership"] == m39
          and back["rank39"]["a_part"] == a39 and back["rank39"]["b_part"] == b39
          and back["rank37_regression"]["membership"] == int(mem[36])
          and back["rank38_regression"]["membership"] == int(mem[37])
          and back["rank37_regression"]["a_part"] == int(memA[top[36]["root"]])
          and back["rank37_regression"]["b_part"] == int(memB[top[36]["root"]])
          and back["rank38_regression"]["a_part"] == int(memA[top[37]["root"]])
          and back["rank38_regression"]["b_part"] == int(memB[top[37]["root"]]))
    checks.append({"name": "rank39_exact_integer_json_serialization", "pass": bool(ok),
                   "detail": {"membership": m39, "a_part": a39, "b_part": b39}})""")
rep("""    print(f"rank-38 root {root} rows {sorted(rows[IDX])} m38 {m38} (A {a38} / B {b38})")""",
    """    print(f"rank-39 root {root} rows {sorted(rows[IDX])} m39 {m39} (A {a39} / B {b39})")""")
rep('    print(f"full C(38,5): {ful5}  sextet C(38,6): {six}")',
    """    print(f"full C(39,5): {ful5}  sextet C(39,6): {six}")
    print(f"b_only sextets {six['b_only']} double rows {sixtwos}  septet non-zero {sept_nonzero}  disjoint quints {uc['disjoint']}")""")


# ---- 6. the new rank-38 regression layer (inserted after the kept
# ----    rank-37 regression layer by the marker surgery in main) ----
LAYER38 = '''    # ---- rank-38 regression (vs the pinned published k38 preread JSON)
    n = 38
    idx = n - 1
    pub38 = k38pre["rank38"]
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
          pub38["root"] == "00000008800000003800000008100000" == top[idx]["root"]
          and sorted(pub38["rows"]) == sorted(rows[idx]) == [19, 29]
          and int(pub38["membership"]) == int(mem[idx]) == 119940649042609991
          and int(pub38["a_part"]) == 91876760891572775
          and int(pub38["b_part"]) == 28063888151037216,
          {"root": pub38["root"], "rows": sorted(rows[idx]), "membership": int(mem[idx])})
    check(f"rank{n}_prior_hits_match_published_preread",
          prior == {19: [0, 2, 3, 8, 9, 10, 15, 29, 32, 33, 35, 36], 29: [19]}
          and {k: sorted(v) for k, v in pub38["prior_hit_indices"].items()}
          == {str(r): v for r, v in sorted(prior.items())},
          {str(r): v for r, v in sorted(prior.items())})
    check(f"rank{n}_new_census_matches_published_preread",
          pub38["new_census"]["pair"]["shared"] == shared
          and pub38["new_census"]["pair"]["disjoint"] == pc["disjoint"]
          and pub38["new_census"]["triple"]["b_only"] == tc["b_only"]
          and pub38["new_census"]["triple"]["zero"] == tc["zero"]
          and pub38["new_census"]["triple"]["disjoint"] == tc["disjoint"]
          and pub38["new_census"]["quad"]["b_only"] == qc["b_only"]
          and pub38["new_census"]["quad"]["zero"] == qc["zero"]
          and pub38["new_census"]["quad"]["disjoint"] == qc["disjoint"]
          and pub38["new_census"]["quint"]["b_only"] == uc["b_only"]
          and pub38["new_census"]["quint"]["zero"] == uc["zero"]
          and pub38["new_census"]["quint"]["disjoint"] == uc["disjoint"]
          and tc == {"b_only": 420, "zero": 113, "disjoint": 133}
          and qc == {"b_only": 2519, "zero": 5094, "disjoint": 157}
          and uc == {"b_only": 2868, "zero": 63177, "disjoint": 0},
          {"triple": tc, "quad": qc, "quint": uc})
    check(f"rank{n}_histograms_and_disjoint_quads_match_published_preread",
          {int(k): v for k, v in pub38["new_triple_double_row_histogram"].items()} == ttwos
          and {int(k): v for k, v in pub38["new_quad_double_row_histogram"].items()} == qtwos
          and {int(k): v for k, v in pub38["new_quint_double_row_histogram"].items()} == utwos
          and {str(k): v for k, v in pub38["b_only_quint_four_subset_profiles"].items()} == profiles
          and profiles == {"3/2/0": uc["b_only"]}
          and pub38["disjoint_quad_count"] == qc["disjoint"] == 157
          and {int(k): v for k, v in pub38["disjoint_quad_union_sizes"].items()} == dusizes
          and set(dusizes) == {8}
          and pub38["cumulative_disjoint_quads"] == 1520 + qc["disjoint"] == 1677,
          {"disjoint_union_sizes": dusizes, "cumulative": 1520 + qc["disjoint"]})
    check(f"rank{n}_full_census_matches_published_preread",
          pub38["full_triples"]["counts"] == ful3
          and ful3 == {"b_only": 5178, "zero": 1533, "disjoint": 1725}
          and {int(k): v for k, v in pub38["full_triples"]["double_row_histogram"].items()} == f3twos
          and pub38["full_quints"]["counts"] == ful5
          and ful5 == {"b_only": 23024, "zero": 478918, "disjoint": 0}
          and {int(k): v for k, v in pub38["full_quints"]["double_row_histogram"].items()} == f5twos
          and pub38["sextet_census"]["counts"] == six
          and six == {"b_only": 0, "zero": math.comb(38, 6), "disjoint": 0},
          {"full_triples": ful3, "full_quints": ful5, "sextet": six})
    check(f"rank{n}_era_continuation_matches_k38_preread_rank37_regression",
          ful5["b_only"] - uc["b_only"] == 20156
          and k38pre["rank37_regression"]["full_quints"]["counts"]["b_only"] == 20156
          and ful5["zero"] - uc["zero"] == 415741
          and k38pre["rank37_regression"]["full_quints"]["counts"]["zero"] == 415741
          and ful5["disjoint"] == 0,
          {"prev_b_only": 20156,
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


# ---- 7. the new rank-39 facts section (replaces the old rank-38
# ----    facts section via the marker surgery in main) ----
RANK39_SECTION = '''    # ---- rank-39 facts (all machine-derived from the pinned aggregate)
    root = top[IDX]["root"]
    m39 = int(mem[IDX])
    a39 = int(memA[root])
    b39 = int(memB[root])
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
    duq = {}
    for c in itertools.combinations(range(IDX), 4):
        combo = (IDX,) + c
        cl, _ = classify_a(rows, combo)
        if cl == "disjoint":
            u = set()
            for i in combo:
                u |= set(rows[i])
            duq[len(u)] = duq.get(len(u), 0) + 1
    ful3, f3twos, f3cmp, f3mis = census(rows, itertools.combinations(range(RANK), 3))
    ful5, f5twos, f5cmp, f5mis = census(rows, itertools.combinations(range(RANK), 5))

    # ---- sextet pass: the C(39,6) census loses its all-zero property
    # for the first time, so count with both classifiers AND collect
    # the b_only records for the level-7 closure scan ----
    six = {"b_only": 0, "zero": 0, "disjoint": 0}
    sixtwos = {}
    b_only_sextets = []
    s6cmp = 0
    s6mis = 0
    for c in itertools.combinations(range(RANK), 6):
        ca, ta = classify_a(rows, c)
        cb, tb = classify_b(rows, c)
        s6cmp += 1
        if (ca, ta) != (cb, tb):
            s6mis += 1
        six[ca] += 1
        if ca == "b_only":
            sixtwos[ta] = sixtwos.get(ta, 0) + 1
            b_only_sextets.append(c)

    # ---- level-7 closure: zero class is upward closed (adding roots
    # only raises row multiplicities), so every non-zero-class 7-combo
    # must contain a non-zero-class 6-subset; disjoint sextets do not
    # exist at k=39, so extending the 5,852 b_only sextets by one root
    # covers every 7-combo candidate exactly ----
    sept_checked = 0
    sept_nonzero = 0
    sept7cmp = 0
    sept7mis = 0
    seen7 = set()
    for s in b_only_sextets:
        sm = set(s)
        for i in range(RANK):
            if i in sm:
                continue
            c7 = tuple(sorted(s + (i,)))
            if c7 in seen7:
                continue
            seen7.add(c7)
            ca, ta = classify_a(rows, c7)
            cb, tb = classify_b(rows, c7)
            sept7cmp += 1
            if (ca, ta) != (cb, tb):
                sept7mis += 1
            sept_checked += 1
            if ca != "zero":
                sept_nonzero += 1

    dj39 = sum(1 for c in itertools.combinations(range(RANK), 4)
               if classify_a(rows, c)[0] == "disjoint")

    check("rank39_root_matches_top50",
          root == "00000000000000889002000000100200"
          and sorted(rows[IDX]) == [5, 24],
          {"root": root, "rows": sorted(rows[IDX])})
    check("rank39_prior_hits_recorded",
          prior == {5: [2, 25], 24: [4, 14]},
          {str(k): v for k, v in sorted(prior.items())})
    check("rank39_membership_split_identity",
          a39 + b39 == m39
          and m39 == 119883868794265826
          and m39 < int(reg[38]["membership"]),
          {"membership": m39, "a_part": a39, "b_part": b39})
    check("rank39_new_pair_census",
          pc["disjoint"] == IDX - shared and shared == 4 and pc["disjoint"] == 34,
          {"shared": shared, "disjoint": pc["disjoint"], "total": IDX})
    check("rank39_new_triple_census",
          tc["b_only"] + tc["zero"] + tc["disjoint"] == math.comb(IDX, 2)
          and tc == {"b_only": 319, "zero": 42, "disjoint": 342}, tc)
    check("rank39_new_quad_census",
          qc["b_only"] + qc["zero"] + qc["disjoint"] == math.comb(IDX, 3)
          and qc == {"b_only": 4398, "zero": 3029, "disjoint": 1009}, qc)
    check("rank39_new_quint_census",
          uc["b_only"] + uc["zero"] + uc["disjoint"] == math.comb(IDX, 4)
          and uc["b_only"] == len(new_quint_b_only)
          and uc["zero"] == math.comb(IDX, 4) - uc["b_only"] - uc["disjoint"]
          and uc == {"b_only": 13658, "zero": 59649, "disjoint": 508},
          {**uc, "records": len(new_quint_b_only)})
    check("rank39_new_quint_double_rows",
          sum(utwos.values()) == uc["b_only"] and 5 in utwos and 24 in utwos
          and utwos == {0: 198, 1: 4, 4: 26, 5: 763, 7: 4, 8: 4, 9: 4, 11: 4,
                        14: 4, 15: 1561, 16: 38, 18: 6562, 19: 4267, 23: 10,
                        24: 179, 29: 4, 30: 26}, utwos)
    check("rank39_b_only_quint_profiles",
          profiles == {"3/2/0": uc["b_only"]}, profiles)
    check("rank39_disjoint_quints_first_appearance",
          # the quint disjoint class is non-empty for the first time in
          # the lane history: every previously published new-layer and
          # full quint census (k=26..k=38) had disjoint == 0, and the
          # k=38 main I-E therefore carried only the b_only term j5_B
          uc["disjoint"] == 508 and set(duq) == {10} and sum(duq.values()) == 508
          and reg[38]["full_quints"]["counts"]["disjoint"] == 0
          and ful5["disjoint"] == uc["disjoint"] == 508,
          {"new_disjoint_quint_count": uc["disjoint"], "union_sizes": duq,
           "prev_full_disjoint": reg[38]["full_quints"]["counts"]["disjoint"]})
    check("rank39_disjoint_quads_union8",
          sum(dusizes.values()) == qc["disjoint"] and set(dusizes) == {8}
          and qc["disjoint"] == 1009,
          {"disjoint_quad_count": qc["disjoint"], "union_sizes": dusizes,
           "cumulative_disjoint_quads": 1677 + qc["disjoint"]})
    check("rank39_cumulative_disjoint_quads_global_recount",
          dj39 == 2686 and dj39 == 1677 + qc["disjoint"]
          and dj39 == pub38["cumulative_disjoint_quads"] + qc["disjoint"],
          {"global_C39_4": dj39, "prev_cumulative": pub38["cumulative_disjoint_quads"],
           "new": qc["disjoint"]})
    check("rank39_full_census_totals",
          ful3["b_only"] + ful3["zero"] + ful3["disjoint"] == math.comb(RANK, 3)
          and ful5["b_only"] + ful5["zero"] + ful5["disjoint"] == math.comb(RANK, 5)
          and sum(f5twos.values()) == ful5["b_only"]
          and ful3 == {"b_only": 5497, "zero": 1575, "disjoint": 2067}
          and ful5 == {"b_only": 36682, "zero": 538567, "disjoint": 508}
          and f3twos == {0: 69, 1: 9, 4: 41, 5: 76, 7: 9, 8: 9, 9: 9, 11: 9,
                         14: 9, 15: 549, 16: 68, 18: 2736, 19: 1779, 23: 15,
                         24: 60, 29: 9, 30: 41}
          and f5twos == {0: 198, 1: 4, 4: 26, 5: 763, 7: 4, 8: 4, 9: 4, 11: 4,
                         14: 4, 15: 5024, 16: 725, 18: 17865, 19: 11838, 23: 10,
                         24: 179, 29: 4, 30: 26},
          {"full_triples": ful3, "full_quints": ful5, "quint_double_rows": f5twos})
    check("rank39_quint_era_continuation",
          ful5["b_only"] - uc["b_only"] == reg[38]["full_quints"]["counts"]["b_only"]
          and ful5["zero"] - uc["zero"] == reg[38]["full_quints"]["counts"]["zero"]
          and ful5["disjoint"] == uc["disjoint"],
          {"prev_b_only": reg[38]["full_quints"]["counts"]["b_only"],
           "new_b_only": uc["b_only"], "full_b_only": ful5["b_only"],
           "prev_zero": reg[38]["full_quints"]["counts"]["zero"],
           "new_zero": uc["zero"], "full_zero": ful5["zero"],
           "full_disjoint": ful5["disjoint"]})
    check("rank39_two_sharer_rows_double_all_three_layers",
          # rank-39 (5,24) has no fresh row and no single-sharer row:
          # row 5 arrives with two prior sharers (index 2 = the rank-3
          # root (5,19), index 25 = the rank-26 root (5,16)) and row 24
          # with two prior sharers (index 4 = the rank-5 root (18,24),
          # index 14 = the rank-15 root (15,24)); both double in the
          # triple, quad AND quint layers for the first time, so the
          # new-layer double-row family gains two rows in one
          # generation (the single-share pattern of rows 7/9/8/29 never
          # reached the quint layer)
          prior == {5: [2, 25], 24: [4, 14]}
          and ttwos == {0: 3, 1: 1, 4: 3, 5: 54, 7: 1, 8: 1, 9: 1, 11: 1, 14: 1,
                        15: 15, 16: 1, 18: 120, 19: 66, 23: 1, 24: 46, 29: 1, 30: 3}
          and qtwos == {0: 60, 1: 6, 4: 32, 5: 391, 7: 6, 8: 6, 9: 6, 11: 6,
                        14: 6, 15: 333, 16: 15, 18: 1965, 19: 1257, 23: 12,
                        24: 259, 29: 6, 30: 32}
          and ttwos[5] == 54 and ttwos[24] == 46
          and qtwos[5] == 391 and qtwos[24] == 259
          and utwos[5] == 763 and utwos[24] == 179,
          {"triple": ttwos, "quad": qtwos, "quint": utwos,
           "row5_prior_sharers": prior[5], "row24_prior_sharers": prior[24]})
    check("rank39_sextet_first_b_only_and_septet_zero_closure",
          # the C(39,6) census loses its all-zero property for the
          # first time: 5,852 b_only records, all containing the rank-39
          # root, double rows confined to the hub band {15, 18, 19};
          # level 7 then closes the I-E hierarchy (99,122 candidates,
          # all zero), so the k=39 marginal I-E needs the level-6 term
          # but truncates at level 6
          six == {"b_only": 5852, "zero": 3256771, "disjoint": 0}
          and six["b_only"] == len(b_only_sextets)
          and sixtwos == {15: 682, 18: 3147, 19: 2023}
          and all(IDX in s for s in b_only_sextets)
          and sept_checked == 99122 and sept_nonzero == 0
          and math.comb(RANK, 7) == 15380937,
          {"sextet": six, "b_only_double_rows": sixtwos,
           "septet_combos_checked": sept_checked,
           "septet_non_zero": sept_nonzero,
           "C39_7": math.comb(RANK, 7)})
    check("rank39_expected_totals",
          math.comb(RANK, 3) == 9139 and math.comb(IDX, 2) == 703
          and math.comb(IDX, 3) == 8436 and math.comb(IDX, 4) == 73815
          and math.comb(RANK, 5) == 575757 and math.comb(RANK, 6) == 3262623,
          {"C38_2": math.comb(IDX, 2), "C38_3": math.comb(IDX, 3), "C38_4": math.comb(IDX, 4),
           "C39_3": math.comb(RANK, 3), "C39_5": math.comb(RANK, 5), "C39_6": math.comb(RANK, 6)})
    check("rank39_two_classifiers_agree",
          pmis == tmis == qmis == umis == f3mis == f5mis == s6mis == sept7mis == 0,
          {"comparisons": pcmp + tcmp + qcmp + ucmp + f3cmp + f5cmp + s6cmp + sept7cmp,
           "mismatches": pmis + tmis + qmis + umis + f3mis + f5mis + s6mis + sept7mis})

    rank39 = {
        "root": root,
        "rows": sorted(rows[IDX]),
        "membership": m39,
        "a_part": a39,
        "b_part": b39,
        "prior_hits": {str(r): len(v) for r, v in sorted(prior.items())},
        "prior_hit_indices": {str(r): v for r, v in sorted(prior.items())},
        "note": ("rank-39 (5,24) has no fresh row and no single-sharer "
                 "row: both rows arrive with exactly two prior sharers "
                 "(row 5 via index 2 = the rank-3 root (5,19) and index "
                 "25 = the rank-26 root (5,16); row 24 via index 4 = the "
                 "rank-5 root (18,24) and index 14 = the rank-15 root "
                 "(15,24)), and both double in the triple, quad and "
                 "quint layers for the first time (54/391/763 and "
                 "46/259/179 records). The new pair census is 4 shared / "
                 "34 disjoint -- the fewest shared of the whole "
                 "post-fresh-row era -- and the new-layer double-row "
                 "family gains two rows in one generation (rows 5 and 24 "
                 "join; the quint histogram now spans 17 rows 0, 1, 4, "
                 "5, 7, 8, 9, 11, 14, 15, 16, 18, 19, 23, 24, 29, 30). "
                 "STRUCTURAL BREAK AT k=39: the new quint layer contains "
                 "508 disjoint records (all with 10-row unions), the "
                 "first disjoint quints ever (every published k=26..k=38 "
                 "quint census had disjoint == 0, which is what let the "
                 "k=38 marginal I-E carry only the b_only term j5_B at "
                 "level 5), and the C(39,6)=3,262,623 sextet census "
                 "contains 5,852 b_only records (double rows confined to "
                 "the hub band rows 15/18/19, every record containing "
                 "the rank-39 root), the first non-zero sextet layer "
                 "ever (the C(38,6) census was all zero). Both premises "
                 "of the k=38-style truncation therefore fail at k=39: "
                 "the main computation must evaluate the level-5 "
                 "disjoint-quint joints (j5_A, alternating level-5 sign) "
                 "and the level-6 b_only-sextet joints (j6_B, alternating "
                 "level-6 sign) before truncating. Level 7 closes the "
                 "hierarchy: every C(39,7)=15,380,937 7-combo with a "
                 "non-zero 6-subset was scanned (99,122 distinct "
                 "candidates via the upward closure of the zero class, "
                 "since disjoint sextets do not exist at k=39) and all "
                 "are zero, so the I-E truncation at level 6 is "
                 "well-defined. The 157 -> 1,009 jump in new disjoint "
                 "quads (all 8-row unions, cumulative 2,686 = 1,677 + "
                 "1,009 confirmed by a global C(39,4) recount) is the "
                 "same lightly-shared-root effect as the 508 disjoint "
                 "quints."),
        "ie_extension": {
            "level5_disjoint_quints": (
                "508 records, the first ever; their class no longer "
                "forces zero joints, so the k=38-style identity "
                "m - sum_j2 + sum_j3 - sum_j4 + sum_j5B no longer holds "
                "as stated: the disjoint-quint joints (j5_A) must be "
                "evaluated with the alternating level-5 sign"),
            "level6_b_only_sextets": (
                "5,852 records, the first ever (all contain the rank-39 "
                "root); their B-type joints (j6_B) must be evaluated with "
                "the alternating level-6 sign"),
            "level7_and_beyond": (
                "all zero (99,122-candidate monotone extension scan), so "
                "the marginal I-E truncates at level 6 once the two new "
                "terms are included"),
        },
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
        "cumulative_disjoint_quads": 1677 + qc["disjoint"],
        "disjoint_quint_count": uc["disjoint"],
        "disjoint_quint_union_sizes": {str(k): v for k, v in sorted(duq.items())},
        "b_only_sextet_count": six["b_only"],
        "b_only_sextet_double_row_histogram": sixtwos,
        "b_only_sextet_all_include_new_root": all(IDX in s for s in b_only_sextets),
        "septet_zero_closure": {
            "C39_7_total": math.comb(RANK, 7),
            "distinct_combos_checked": sept_checked,
            "non_zero_class_seven_combos": sept_nonzero,
            "method": ("zero class is upward closed (adding roots only raises "
                       "row multiplicities), so every non-zero-class 7-combo "
                       "must contain a non-zero-class 6-subset; disjoint "
                       "sextets do not exist at k=39, so the extension scan "
                       "over the 5,852 b_only sextets covers every candidate"),
        },
        "full_triples": {"counts": ful3, "total": math.comb(RANK, 3),
                         "double_row_histogram": f3twos,
                         "compared": math.comb(RANK, 3), "mismatches": f3mis},
        "full_quints": {"counts": ful5, "total": math.comb(RANK, 5),
                        "double_row_histogram": f5twos,
                        "compared": math.comb(RANK, 5), "mismatches": f5mis},
        "sextet_census": {"total": math.comb(RANK, 6), "counts": six,
                          "compared": s6cmp, "mismatches": s6mis},
    }

'''


def main() -> int:
    src = open(SRC, encoding="utf-8").read()
    base = open(SRC, "rb").read()
    blob = hashlib.sha1(b"blob %d\x00" % len(base) + base).hexdigest()
    if blob != EXPECT_BASE_BLOB:
        raise SystemExit(f"FAIL base blob {blob}")
    out = sub(src)

    # ---- drop the rank-36 regression layer, keep the rank-37 layer as
    # ---- the first layer (with the reg init), insert the new rank-38
    # ---- layer, and replace the old rank-38 facts section with the
    # ---- new rank-39 facts section
    m36 = out.index("    # ---- rank-36 regression (vs the pinned published k36 preread JSON)")
    m37 = out.index("    # ---- rank-37 regression (vs the pinned published k37 preread JSON)")
    m38f = out.index("    # ---- rank-38 facts (all machine-derived from the pinned aggregate)")
    m_out = out.index("    out = {")
    assert m36 < m37 < m38f < m_out, "block order unexpected"
    blk37 = out[m37:m38f]
    head, body = blk37.split("\n", 1)
    assert head == "    # ---- rank-37 regression (vs the pinned published k37 preread JSON)"
    assert '"""' not in body[:200]
    out = (out[:m36]
           + "    # ---- rank-37 regression (vs the pinned published k37 preread JSON)\n"
           + "    reg = {}\n"
           + body
           + LAYER38
           + RANK39_SECTION
           + out[m_out:])

    # residual sanity: no stale identifiers may survive
    for stale in ("pub36", 'PINS["k36pre"]', "k36pre =", "k36pre[",
                  "k36pre.get", "K35PRE_SHA", "rank38 = {", "dj38",
                  'back["rank38"][', 'back["rank36_regression"]',
                  "rank38_exact_integer_json_serialization",
                  "m38 = int(mem[IDX])", "rank-38 facts"):
        if stale in out:
            raise SystemExit(f"FAIL stale token {stale!r} survived")
    # every rep anchor count already asserted; block structure checks
    assert out.count("# ---- rank-37 regression") == 1
    assert out.count("# ---- rank-38 regression") == 1
    assert out.count("# ---- rank-39 facts") == 1
    open(DST, "w", encoding="utf-8").write(out)
    data = open(DST, "rb").read()
    print("wrote", DST, len(data), "bytes")
    print("git_blob_sha1:", hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest())
    print("sha256:", hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())

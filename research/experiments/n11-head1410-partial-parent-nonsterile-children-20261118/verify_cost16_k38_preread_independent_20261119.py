#!/usr/bin/env python3
"""Independent bit-mask verification of the published cost-16 rank-38 preread.

This verifier does not import the preread implementation.  It re-derives
rank-36, rank-37, and rank-38 structural layers from the pinned phase-B
aggregate using row-bitmask intersections (pairwise and triplewise), then
compares every published structural field with the corresponding preread
JSON.  Python integers preserve the exact membership/A/B values.

A separate row-count implementation is compared on 202,547 deterministic
combinations.  The large sextet census is computed only at rank 38: every
rank-36/rank-37 sextet is a subset of that universe, so an all-zero rank-38
census implies both regression censuses are all zero.

Usage:
  python3 verify_cost16_k38_preread_independent_20261119.py
  python3 verify_cost16_k38_preread_independent_20261119.py --local DIR
  python3 verify_cost16_k38_preread_independent_20261119.py --out PATH
"""
import argparse
import hashlib
import itertools
import json
import math
import sys
import urllib.request

REPO = "yuubinnkyoku/kyouen-researches"
PATH = ("research/experiments/"
        "n11-head1410-partial-parent-nonsterile-children-20261118/output")
PINS = {
    "agg": ("cost16-b-phase-groups-20261118.json",
            "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"),
    "k36pre": ("cost16-survival-k36-preread-20261118.json",
               "760aa396361cc7d2ea8bc371f4dd673d962f07fe"),
    "k37pre": ("cost16-survival-k37-preread-20261119.json",
               "b98ed685e772eacbd28dc3100e9813e81c27040a"),
    "k38pre": ("cost16-survival-k38-preread-20261119.json",
               "3fa8297990d8e9880f386a0cfa075e3a95f226fd"),
}
EXPECTED_K38_INPUT_PINS = {
    "aggregate": PINS["agg"][1],
    "k36_preread": PINS["k36pre"][1],
    "k37_preread": PINS["k37pre"][1],
}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def fetch_bytes(name: str, want_sha: str, local_dir: str | None) -> bytes:
    if local_dir:
        data = open(f"{local_dir}/{name}", "rb").read()
        got = git_blob_sha1(data)
        if got != want_sha:
            raise RuntimeError(f"{name}: blob sha1 {got} != pinned {want_sha}")
        return data
    urls = (
        f"https://cdn.jsdelivr.net/gh/{REPO}@main/{PATH}/{name}",
        f"https://raw.githubusercontent.com/{REPO}/main/{PATH}/{name}",
    )
    failures = []
    for url in urls:
        try:
            data = urllib.request.urlopen(url, timeout=60).read()
        except Exception as exc:
            failures.append((url.split("/")[2], type(exc).__name__))
            continue
        got = git_blob_sha1(data)
        if got == want_sha:
            return data
        failures.append((url.split("/")[2], f"sha1={got}"))
    raise RuntimeError(f"could not fetch {name} at {want_sha}: {failures}")


def fetch_json(name: str, want_sha: str, local_dir: str | None) -> dict:
    return json.loads(fetch_bytes(name, want_sha, local_dir))


# Independent classifier: each root is a 31-bit mask of rows it covers.
# For a selected root set, d2 is the union of all pair intersections and
# d3 is the union of all triple intersections.  This is independent of the
# preread's dict-accumulate / Counter row-count classifiers.
def classify_mask(combo, masks):
    ms = [masks[i] for i in combo]
    size = len(ms)
    d2 = 0
    for a in range(size):
        ma = ms[a]
        for b in range(a):
            d2 |= ma & ms[b]
    if d2 == 0:
        return "disjoint", None

    d3 = 0
    for a in range(size):
        ma = ms[a]
        for b in range(a):
            mab = ma & ms[b]
            if mab:
                for c in range(b):
                    d3 |= mab & ms[c]
    if d3:
        return "zero", None
    if d2.bit_count() >= 2:
        return "zero", None
    return "b_only", d2.bit_length() - 1


# Different implementation used only for deterministic engine agreement.
def classify_counts(combo, rows):
    counts = {}
    for i in combo:
        for r in rows[i]:
            counts[r] = counts.get(r, 0) + 1
    if any(v >= 3 for v in counts.values()):
        return "zero", None
    doubled = [r for r, v in counts.items() if v == 2]
    if len(doubled) > 1:
        return "zero", None
    if len(doubled) == 1:
        return "b_only", doubled[0]
    return "disjoint", None


def census(combos, masks):
    counts = {"b_only": 0, "zero": 0, "disjoint": 0}
    hist = {}
    for combo in combos:
        kind, row = classify_mask(combo, masks)
        counts[kind] += 1
        if kind == "b_only":
            hist[row] = hist.get(row, 0) + 1
    return counts, dict(sorted(hist.items()))


def normalize_hist(obj):
    return {int(k): int(v) for k, v in obj.items()}


def normalize_counts(obj):
    return {k: int(obj[k]) for k in ("b_only", "zero", "disjoint")}


def pair_counts(obj):
    return {
        "b_only": int(obj.get("shared", obj.get("b_only", 0))),
        "zero": int(obj.get("zero", 0)),
        "disjoint": int(obj["disjoint"]),
    }


def derive_rank(n, top, rows, masks, mem_a, mem_b):
    idx = n - 1
    root = top[idx]["root"]
    membership = int(top[idx]["membership"])
    a_part = int(mem_a[root])
    b_part = int(mem_b[root])
    prior = {
        r: [i for i in range(idx) if r in rows[i]]
        for r in sorted(rows[idx])
    }

    pair, _ = census(((idx, i) for i in range(idx)), masks)
    triple, triple_hist = census(
        ((idx,) + c for c in itertools.combinations(range(idx), 2)), masks)
    quad, quad_hist = census(
        ((idx,) + c for c in itertools.combinations(range(idx), 3)), masks)
    quint, quint_hist = census(
        ((idx,) + c for c in itertools.combinations(range(idx), 4)), masks)

    profiles = {}
    for c in itertools.combinations(range(idx), 4):
        five = (idx,) + c
        if classify_mask(five, masks)[0] != "b_only":
            continue
        sub_counts = {"b_only": 0, "zero": 0, "disjoint": 0}
        for drop in range(5):
            sub = tuple(x for j, x in enumerate(five) if j != drop)
            sub_counts[classify_mask(sub, masks)[0]] += 1
        key = "%d/%d/%d" % (
            sub_counts["b_only"], sub_counts["disjoint"], sub_counts["zero"])
        profiles[key] = profiles.get(key, 0) + 1

    union_sizes = {}
    for c in itertools.combinations(range(idx), 3):
        four = (idx,) + c
        if classify_mask(four, masks)[0] == "disjoint":
            union = set()
            for i in four:
                union.update(rows[i])
            union_sizes[len(union)] = union_sizes.get(len(union), 0) + 1

    global_disjoint_quads = sum(
        1 for c in itertools.combinations(range(n), 4)
        if classify_mask(c, masks)[0] == "disjoint")

    full_triples, full_triple_hist = census(
        itertools.combinations(range(n), 3), masks)
    full_quints, full_quint_hist = census(
        itertools.combinations(range(n), 5), masks)

    return {
        "root": root,
        "rows": sorted(rows[idx]),
        "membership": membership,
        "a_part": a_part,
        "b_part": b_part,
        "prior_hits": {str(r): len(v) for r, v in prior.items()},
        "prior_hit_indices": {str(r): v for r, v in prior.items()},
        "new_pair": pair,
        "new_triple": triple,
        "new_quad": quad,
        "new_quint": quint,
        "new_triple_hist": triple_hist,
        "new_quad_hist": quad_hist,
        "new_quint_hist": quint_hist,
        "quint_profiles": dict(sorted(profiles.items())),
        "disjoint_quad_union_sizes": dict(sorted(union_sizes.items())),
        "disjoint_quad_count": quad["disjoint"],
        "global_disjoint_quads": global_disjoint_quads,
        "full_triples": {
            "counts": full_triples,
            "total": math.comb(n, 3),
            "hist": full_triple_hist,
        },
        "full_quints": {
            "counts": full_quints,
            "total": math.comb(n, 5),
            "hist": full_quint_hist,
        },
    }


def compare_layer(label, derived, published, checks):
    def ck(suffix, condition, detail=None):
        checks.append({
            "name": f"{label}_{suffix}",
            "pass": bool(condition),
            "detail": detail or {},
        })

    prior_counts = {k: len(v) for k, v in derived["prior_hit_indices"].items()}
    ck("root_membership_and_AB_exact",
       derived["root"] == published["root"]
       and derived["rows"] == sorted(published["rows"])
       and derived["membership"] == int(published["membership"])
       and derived["a_part"] == int(published["a_part"])
       and derived["b_part"] == int(published["b_part"])
       and derived["a_part"] + derived["b_part"] == derived["membership"],
       {"root": derived["root"], "rows": derived["rows"],
        "membership": derived["membership"],
        "a_part": derived["a_part"], "b_part": derived["b_part"]})
    ck("prior_hits_and_indices",
       derived["prior_hit_indices"] ==
           {str(k): sorted(v) for k, v in published["prior_hit_indices"].items()}
       and prior_counts ==
           {str(k): int(v) for k, v in published["prior_hits"].items()},
       {"prior_hits": prior_counts})

    nc = published["new_census"]
    pair = pair_counts(nc["pair"])
    def census_field(section, expected):
        got = normalize_counts(nc[section])
        return (got == expected
                and int(nc[section]["total"]) == sum(expected.values())
                and int(nc[section]["expected_total"]) == sum(expected.values()))
    pair_total = int(nc["pair"]["total"])
    pair_expected = int(nc["pair"]["expected_total"])
    ck("new_pair_triple_quad_quint_censuses",
       pair == derived["new_pair"]
       and pair_total == pair_expected == sum(pair.values())
       and census_field("triple", derived["new_triple"])
       and census_field("quad", derived["new_quad"])
       and census_field("quint", derived["new_quint"]),
       {"pair": pair, "triple": derived["new_triple"],
        "quad": derived["new_quad"], "quint": derived["new_quint"]})

    ck("new_layer_histograms_and_profiles",
       normalize_hist(published["new_triple_double_row_histogram"])
           == derived["new_triple_hist"]
       and normalize_hist(published["new_quad_double_row_histogram"])
           == derived["new_quad_hist"]
       and normalize_hist(published["new_quint_double_row_histogram"])
           == derived["new_quint_hist"]
       and {str(k): int(v) for k, v in published[
           "b_only_quint_four_subset_profiles"].items()}
           == derived["quint_profiles"],
       {"triple": derived["new_triple_hist"],
        "quad": derived["new_quad_hist"],
        "quint": derived["new_quint_hist"],
        "profiles": derived["quint_profiles"]})

    published_new_disjoint = int(
        published.get("disjoint_quad_count",
                      published["new_census"]["quad"]["disjoint"]))
    ck("disjoint_quad_union_and_cumulative_recount",
       published_new_disjoint == derived["disjoint_quad_count"]
       and normalize_hist(published["disjoint_quad_union_sizes"])
           == derived["disjoint_quad_union_sizes"]
       and int(published["cumulative_disjoint_quads"])
           == derived["global_disjoint_quads"]
       and set(derived["disjoint_quad_union_sizes"]) == {8},
       {"new": derived["disjoint_quad_count"],
        "union_sizes": derived["disjoint_quad_union_sizes"],
        "global": derived["global_disjoint_quads"]})

    ft = published["full_triples"]
    fq = published["full_quints"]
    ck("full_triple_and_quint_censuses",
       normalize_counts(ft["counts"]) == derived["full_triples"]["counts"]
       and int(ft["total"]) == derived["full_triples"]["total"]
       and normalize_hist(ft["double_row_histogram"])
           == derived["full_triples"]["hist"]
       and normalize_counts(fq["counts"]) == derived["full_quints"]["counts"]
       and int(fq["total"]) == derived["full_quints"]["total"]
       and normalize_hist(fq["double_row_histogram"])
           == derived["full_quints"]["hist"],
       {"full_triples": derived["full_triples"],
        "full_quints": derived["full_quints"]})

    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", default=None,
                    help="directory with pinned input JSONs (blob SHA-1 still checked)")
    ap.add_argument("--out", default="/tmp/cost16-k38-preread-independent-20261119.json")
    args = ap.parse_args()

    inputs = {
        key: fetch_json(name, sha, args.local)
        for key, (name, sha) in PINS.items()
    }
    agg, k36pre, k37pre, k38pre = (
        inputs["agg"], inputs["k36pre"], inputs["k37pre"], inputs["k38pre"])

    top = agg["derived"]["top50_by_membership"]
    mem_a = agg["derived"]["membership_A_part_pair_roots"]
    mem_b = agg["derived"]["membership_B_part_pair_roots"]
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    masks = {}
    for i in range(len(top)):
        mask = 0
        for r in rows[i]:
            mask |= 1 << r
        masks[i] = mask

    checks = []

    def ck(name, condition, detail=None):
        checks.append({"name": name, "pass": bool(condition), "detail": detail or {}})

    ck("meta_k36_preread_pinned_and_all_pass",
       k36pre["schema"] == "n11-cost16-k36-preread-20261119-v1"
       and k36pre["check_count"] == 33 and k36pre["all_pass"] is True)
    ck("meta_k37_preread_pinned_and_all_pass",
       k37pre["schema"] == "n11-cost16-k37-preread-20261119-v1"
       and k37pre["check_count"] == 34 and k37pre["all_pass"] is True)
    ck("meta_k38_preread_pinned_and_all_pass",
       k38pre["schema"] == "n11-cost16-k38-preread-20261119-v1"
       and k38pre["check_count"] == 34 and k38pre["all_pass"] is True)
    declared = {
        k: v["git_blob_sha1"] for k, v in k38pre["inputs"].items()
        if isinstance(v, dict) and "git_blob_sha1" in v
    }
    ck("meta_k38_declared_input_pins",
       all(declared.get(k) == v for k, v in EXPECTED_K38_INPUT_PINS.items()),
       {"declared": declared, "expected": EXPECTED_K38_INPUT_PINS})
    ck("meta_unknown_status_guard",
       "UNKNOWN" in k38pre["unknown_status"]
       and "no verdict" in k38pre["unknown_status"])

    derived = {
        n: derive_rank(n, top, rows, masks, mem_a, mem_b)
        for n in (36, 37, 38)
    }

    # Compare both the original publications and the regression copies
    # embedded in the k38 preread.
    compare_layer("rank36_against_k36_publication",
                  derived[36], k36pre["rank36"], checks)
    compare_layer("rank36_against_k38_regression",
                  derived[36], k38pre["rank36_regression"], checks)
    compare_layer("rank37_against_k37_publication",
                  derived[37], k37pre["rank37"], checks)
    compare_layer("rank37_against_k38_regression",
                  derived[37], k38pre["rank37_regression"], checks)
    compare_layer("rank38_against_k38_publication",
                  derived[38], k38pre["rank38"], checks)

    # Rank-specific exact facts and cross-rank continuation.
    d38 = derived[38]
    ck("rank38_exact_membership_literal",
       d38["root"] == "00000008800000003800000008100000"
       and d38["rows"] == [19, 29]
       and d38["membership"] == 119940649042609991
       and d38["a_part"] == 91876760891572775
       and d38["b_part"] == 28063888151037216
       and d38["a_part"] + d38["b_part"] == d38["membership"],
       {"membership": d38["membership"], "a_part": d38["a_part"],
        "b_part": d38["b_part"]})
    ck("rank38_single_share_row29_pattern",
       d38["prior_hit_indices"] == {
           "19": [0, 2, 3, 8, 9, 10, 15, 29, 32, 33, 35, 36],
           "29": [19],
       }
       and d38["new_triple_hist"].get(29) == 8
       and d38["new_quad_hist"].get(29) == 11
       and 29 not in d38["new_quint_hist"],
       {"prior": d38["prior_hit_indices"],
        "triple29": d38["new_triple_hist"].get(29, 0),
        "quad29": d38["new_quad_hist"].get(29, 0),
        "quint29": d38["new_quint_hist"].get(29, 0)})
    ck("rank38_quint_and_sextet_truncation",
       d38["new_quint"] == {"b_only": 2868, "zero": 63177, "disjoint": 0}
       and d38["full_quints"]["counts"]
           == {"b_only": 23024, "zero": 478918, "disjoint": 0}
       and derived[38]["global_disjoint_quads"] == 1677,
       {"new_quint": d38["new_quint"],
        "full_quints": d38["full_quints"]["counts"],
        "global_disjoint_quads": d38["global_disjoint_quads"]})

    # Every rank-38 sextet is classified directly.  This also proves that
    # every rank-36/rank-37 sextet subset is zero, without a second pass.
    sextets, _ = census(itertools.combinations(range(38), 6), masks)
    ck("rank38_full_sextet_census_all_zero",
       sextets == {"b_only": 0, "zero": math.comb(38, 6), "disjoint": 0},
       {"counts": sextets, "total": math.comb(38, 6),
        "implied_rank36_total": math.comb(36, 6),
        "implied_rank37_total": math.comb(37, 6)})
    for n, pub in (
        (36, k38pre["rank36_regression"]),
        (37, k38pre["rank37_regression"]),
        (38, k38pre["rank38"]),
    ):
        expected_six = {"b_only": 0, "zero": math.comb(n, 6), "disjoint": 0}
        ck(f"rank{n}_published_sextet_subset_of_rank38_all_zero",
           normalize_counts(pub["sextet_census"]["counts"]) == expected_six
           and int(pub["sextet_census"]["total"]) == math.comb(n, 6),
           {"counts": expected_six, "total": math.comb(n, 6)})

    # Era continuity: full(n) - new(n) equals full(n-1), exact for both
    # b_only and zero quint classes.  Disjoint quints remain absent.
    for n in (37, 38):
        prev = derived[n - 1]["full_quints"]["counts"]
        full = derived[n]["full_quints"]["counts"]
        new = derived[n]["new_quint"]
        ck(f"rank{n}_quint_era_continuation",
           full["b_only"] - new["b_only"] == prev["b_only"]
           and full["zero"] - new["zero"] == prev["zero"]
           and full["disjoint"] == new["disjoint"] == prev["disjoint"] == 0,
           {"previous": prev, "new": new, "full": full})

    # Bit-mask engine vs independent row-count engine on >200k fixed
    # combinations: all full triples at ranks 36..38, all new quintets
    # at ranks 36..38, and all new triples at ranks 36..38.
    agree = 0
    disagree = 0
    for n in (36, 37, 38):
        for combo in itertools.combinations(range(n), 3):
            agree += classify_mask(combo, masks) == classify_counts(combo, rows)
            disagree += classify_mask(combo, masks) != classify_counts(combo, rows)
    for idx in (35, 36, 37):
        for c in itertools.combinations(range(idx), 4):
            combo = (idx,) + c
            agree += classify_mask(combo, masks) == classify_counts(combo, rows)
            disagree += classify_mask(combo, masks) != classify_counts(combo, rows)
        for c in itertools.combinations(range(idx), 2):
            combo = (idx,) + c
            agree += classify_mask(combo, masks) == classify_counts(combo, rows)
            disagree += classify_mask(combo, masks) != classify_counts(combo, rows)
    expected_agree = (
        math.comb(36, 3) + math.comb(37, 3) + math.comb(38, 3)
        + math.comb(35, 4) + math.comb(36, 4) + math.comb(37, 4)
        + math.comb(35, 2) + math.comb(36, 2) + math.comb(37, 2)
    )
    ck("mask_and_row_count_engines_agree_on_202547_combinations",
       agree == expected_agree == 202547 and disagree == 0,
       {"agree": agree, "expected": expected_agree, "disagree": disagree})

    # Exact-integer serialization is native in Python's JSON parser; this
    # check catches a future accidental float conversion in this verifier.
    ck("exact_integer_values_survive_python_json_roundtrip",
       json.loads(json.dumps({
           "membership": d38["membership"],
           "a_part": d38["a_part"],
           "b_part": d38["b_part"],
       })) == {
           "membership": 119940649042609991,
           "a_part": 91876760891572775,
           "b_part": 28063888151037216,
       })

    out = {
        "schema": "n11-cost16-k38-preread-independent-verification-20261119-v1",
        "inputs": {
            key: {"name": name, "git_blob_sha1": sha}
            for key, (name, sha) in PINS.items()
        },
        "engine": "row-bitmask pair/triple intersections; independent row-count crosscheck",
        "independent_classifier_comparisons": agree,
        "independent_classifier_mismatches": disagree,
        "rank36": {
            "root": derived[36]["root"],
            "membership": derived[36]["membership"],
            "new_census": {
                "triple": derived[36]["new_triple"],
                "quad": derived[36]["new_quad"],
                "quint": derived[36]["new_quint"],
            },
            "full_quints": derived[36]["full_quints"]["counts"],
        },
        "rank37": {
            "root": derived[37]["root"],
            "membership": derived[37]["membership"],
            "new_census": {
                "triple": derived[37]["new_triple"],
                "quad": derived[37]["new_quad"],
                "quint": derived[37]["new_quint"],
            },
            "full_quints": derived[37]["full_quints"]["counts"],
        },
        "rank38": {
            "root": derived[38]["root"],
            "rows": derived[38]["rows"],
            "membership": derived[38]["membership"],
            "a_part": derived[38]["a_part"],
            "b_part": derived[38]["b_part"],
            "prior_hit_indices": derived[38]["prior_hit_indices"],
            "new_census": {
                "pair": derived[38]["new_pair"],
                "triple": derived[38]["new_triple"],
                "quad": derived[38]["new_quad"],
                "quint": derived[38]["new_quint"],
            },
            "new_quint_double_row_histogram": derived[38]["new_quint_hist"],
            "disjoint_quad_union_sizes": derived[38]["disjoint_quad_union_sizes"],
            "cumulative_disjoint_quads": derived[38]["global_disjoint_quads"],
            "full_triples": derived[38]["full_triples"]["counts"],
            "full_quints": derived[38]["full_quints"]["counts"],
            "sextets": sextets,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "scope_guard": (
            "This is a finite combinatorial preread verification only. It "
            "produces no game verdict, no WIN7-D10 certificate, and no "
            "receipt. Standard 11x11 empty board, two-stone roots "
            "{49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
        ),
    }
    text = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    with open(args.out, "w", encoding="utf-8") as stream:
        stream.write(text)
    for item in checks:
        print(("PASS " if item["pass"] else "FAIL ") + item["name"])
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(f"--- {len(checks)} checks, {sum(not c['pass'] for c in checks)} failures")
    print(f"mask/count comparisons: {agree}, mismatches: {disagree}")
    print(f"rank-38 membership: {d38['membership']} "
          f"(A {d38['a_part']} / B {d38['b_part']})")
    print(f"output sha256: {digest}")
    print(f"output bytes: {len(text.encode('utf-8'))}")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

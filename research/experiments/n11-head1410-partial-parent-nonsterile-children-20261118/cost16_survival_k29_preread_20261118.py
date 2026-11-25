#!/usr/bin/env python3
"""Independent structural preread for the rank-29 cost-16 root.

Reads only the three pinned JSON inputs already published in this
experiment (phase-B aggregate, k=27 result, k=28 result). It does not
call the Pm engine and does not compute any game verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

EXP = Path("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118")
AGG_PATH = EXP / "output/cost16-b-phase-groups-20261118.json"
K27_PATH = EXP / "output/cost16-survival-k27-20261118.json"
K28_PATH = EXP / "output/cost16-survival-k28-20261118.json"
AGG_SHA1 = "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"
K27_SHA1 = "3dc30ad6c51cc2d7678cc8777e4af2376267ddb8"
K28_SHA1 = "99db3a9a48d044727b3a4d83fb7fc97daa7513d2"


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_pinned(path: Path, expected: str) -> dict:
    data = path.read_bytes()
    got = git_blob_sha1(data)
    if got != expected:
        raise RuntimeError(f"{path}: blob SHA-1 {got} != {expected}")
    return json.loads(data)


def classify_map(rows, ids):
    counts = Counter(r for i in ids for r in rows[i])
    doubled = [r for r, n in counts.items() if n == 2]
    if max(counts.values()) >= 3 or len(doubled) >= 2:
        return "zero", None
    if len(doubled) == 1:
        return "b_only", doubled[0]
    return "disjoint", None


def classify_masks(row_masks, ids):
    selected = sum(1 << i for i in ids)
    multiplicities = [(mask & selected).bit_count() for mask in row_masks]
    doubled = [r for r, n in enumerate(multiplicities) if n == 2]
    if max(multiplicities) >= 3 or len(doubled) >= 2:
        return "zero", None
    if len(doubled) == 1:
        return "b_only", doubled[0]
    return "disjoint", None


def new_census(k, rows, row_masks):
    new_index = k - 1
    result, histogram = {}, Counter()
    b_quints, disjoint_quads = [], []
    compared = mismatches = 0
    for size, name in ((2, "pair"), (3, "triple"), (4, "quad"), (5, "quint")):
        counts = Counter()
        for prior in itertools.combinations(range(new_index), size - 1):
            ids = tuple(prior) + (new_index,)
            a = classify_map(rows, ids)
            b = classify_masks(row_masks, ids)
            compared += 1
            mismatches += a != b
            kind, doubled_row = a
            counts[kind] += 1
            if name == "quint" and kind == "b_only":
                profile = Counter()
                for drop in range(5):
                    profile[classify_map(rows, ids[:drop] + ids[drop + 1:])[0]] += 1
                b_quints.append({
                    "indices": list(ids),
                    "double_row": doubled_row,
                    "four_subset_profile": {
                        "b_only": profile["b_only"],
                        "disjoint": profile["disjoint"],
                        "zero": profile["zero"],
                    },
                })
                histogram[str(doubled_row)] += 1
            if name == "quad" and kind == "disjoint":
                union = sorted({r for i in ids for r in rows[i]})
                disjoint_quads.append({"indices": list(ids), "rows_union": union})
        total = counts["b_only"] + counts["zero"] + counts["disjoint"]
        result[name] = {
            "b_only": counts["b_only"], "zero": counts["zero"],
            "disjoint": counts["disjoint"], "total": total,
            "expected_total": math.comb(new_index, size - 1),
        }
    return {
        "result": result, "hist": dict(sorted(histogram.items())),
        "b_quints": b_quints, "disjoint_quads": disjoint_quads,
        "compared": compared, "mismatches": mismatches,
    }


def full_census(n, size, rows, row_masks):
    counts = Counter()
    twos = Counter()
    compared = mismatches = 0
    for ids in itertools.combinations(range(n), size):
        a = classify_map(rows, ids)
        b = classify_masks(row_masks, ids)
        compared += 1
        mismatches += a != b
        counts[a[0]] += 1
        if a[0] == "b_only":
            twos[a[1]] += 1
    return {
        "counts": {
            "b_only": counts["b_only"], "zero": counts["zero"],
            "disjoint": counts["disjoint"], "total": sum(counts.values()),
            "expected_total": math.comb(n, size),
        },
        "double_rows": {str(k): v for k, v in sorted(twos.items())},
        "compared": compared, "mismatches": mismatches,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    agg = load_pinned(root / AGG_PATH, AGG_SHA1)
    k27 = load_pinned(root / K27_PATH, K27_SHA1)
    k28 = load_pinned(root / K28_PATH, K28_SHA1)
    top = agg["derived"]["top50_by_membership"]
    rows = [tuple(x["rows_covered"]) for x in top]
    row_count = agg["derived"]["rows"]
    if len(top) != 50 or len({x["root"] for x in top}) != 50:
        raise RuntimeError("top50 cardinality/root uniqueness failure")
    if not all(len(rs) == 2 and len(set(rs)) == 2 and all(0 <= r < row_count for r in rs) for rs in rows):
        raise RuntimeError("top50 row-pair validation failure")
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]

    row_masks = [0] * row_count
    for i, rs in enumerate(rows):
        for r in rs:
            row_masks[r] |= 1 << i

    # ---- rank-28 regression against the just-published k=28 result
    c28 = new_census(28, rows, row_masks)
    full28_triples = full_census(28, 3, rows, row_masks)
    full28_quints = full_census(28, 5, rows, row_masks)
    s27 = k27["structure"]
    s28 = k28["structure"]
    vals28 = k28["values"]
    new_pairs_28 = vals28["new_pair_joints"]
    pair_shared_28 = sum(bool(x["shared_row"]) for x in new_pairs_28.values())

    def class_census(records):
        counts = Counter(x["class"] for x in records.values())
        return {"b_only": counts["b_only"], "zero": counts["zero"],
                "disjoint": counts["disjoint"]}

    pair_records_28 = {key: {"class": "b_only" if x["shared_row"] else "disjoint"}
                       for key, x in new_pairs_28.items()}
    pairs_new_census_28 = class_census(pair_records_28)
    triple_census_28 = class_census(vals28["new_triples"])
    quad_census_28 = class_census(vals28["new_quads"])
    quint_b_only_28 = len(vals28["new_quints_b_only"])
    # expected rank-28 new b_only double-row histogram = published k28
    # full histogram minus published k27 full histogram (machine-derived
    # from the two pinned result JSONs, no hand-written table)
    hist28_expected = {}
    for rk, v28 in s28["quint_b_only_double_rows"].items():
        diff = int(v28) - int(s27["quint_b_only_double_rows"].get(rk, 0))
        if diff:
            hist28_expected[str(rk)] = diff
    k28_match = (
        len(new_pairs_28) == 27 and c28["result"]["pair"]["total"] == 27
        and c28["result"]["pair"]["b_only"] == pair_shared_28 == pairs_new_census_28["b_only"] == 14
        and c28["result"]["pair"]["disjoint"] == pairs_new_census_28["disjoint"] == 13
        and c28["result"]["triple"]["total"] == len(vals28["new_triples"]) == 351
        and all(c28["result"]["triple"][k] == triple_census_28[k]
                for k in ("b_only", "zero", "disjoint"))
        and c28["result"]["quad"]["total"] == len(vals28["new_quads"]) == 2925
        and all(c28["result"]["quad"][k] == quad_census_28[k] == s28["new_quad_census"][k]
                for k in ("b_only", "zero", "disjoint"))
        and c28["result"]["quint"]["b_only"] == quint_b_only_28 == s28["new_quint_census"]["b_only"] == 331
        and c28["result"]["quint"]["disjoint"] == s28["new_quint_census"]["disjoint"] == 0
        and c28["result"]["quint"]["zero"] == s28["new_quint_census"]["zero"]
        == int(s28["quints_zero_synth_count"]) == 17219
        and full28_triples["counts"]["b_only"] == s28["triple_census_k28"]["b_only"]
        and full28_triples["counts"]["zero"] == s28["triple_census_k28"]["zero"]
        and full28_triples["counts"]["disjoint"] == s28["triple_census_k28"]["disjoint"]
        and full28_quints["counts"]["b_only"] == s28["quint_census_k28"]["b_only"]
        and full28_quints["counts"]["zero"] == s28["quint_census_k28"]["zero"]
        and full28_quints["counts"]["disjoint"] == s28["quint_census_k28"]["disjoint"] == 0
        and full28_quints["double_rows"] == {str(r): int(v) for r, v in s28["quint_b_only_double_rows"].items()}
        and c28["hist"] == hist28_expected
    )

    # ---- rank-29 structural preread
    c29 = new_census(29, rows, row_masks)
    root29 = top[28]
    row0_prior = sum(0 in rs for rs in rows[:28])
    row16_prior = sum(16 in rs for rs in rows[:28])
    profile_counts = Counter(
        f'{q["four_subset_profile"]["b_only"]}/'
        f'{q["four_subset_profile"]["disjoint"]}/'
        f'{q["four_subset_profile"]["zero"]}'
        for q in c29["b_quints"]
    )
    profile_counts = dict(sorted(profile_counts.items()))
    full29_triples = full_census(29, 3, rows, row_masks)
    full29_quints = full_census(29, 5, rows, row_masks)
    # new = full minus prev layer: the rank-29 full quint census must
    # remove exactly the published k=28 full census as its prev layer.
    # Row 16 enters the double-row set for the first time at rank 29.
    prev_split_ok = (
        full29_quints["counts"]["b_only"] - c29["result"]["quint"]["b_only"]
        == s28["quint_census_k28"]["b_only"]
        and full29_quints["counts"]["zero"] - c29["result"]["quint"]["zero"]
        == s28["quint_census_k28"]["zero"]
        and full29_quints["counts"]["disjoint"] == 0
        and full29_quints["double_rows"] == {
            str(r): int(s28["quint_b_only_double_rows"].get(r, 0))
            + int(c29["hist"].get(r, 0)) for r in ("15", "16", "18", "19")
        }
    )
    actual_totals = [c29["result"][n]["total"] for n in ("pair", "triple", "quad", "quint")]
    expected_totals = [28, 378, 3276, 20475]

    checks = [
        {"name": "top50_has_50_rows", "pass": len(top) == 50, "detail": {"actual": len(top)}},
        {"name": "top50_root_keys_unique", "pass": len({x["root"] for x in top}) == 50,
         "detail": {"unique": len({x["root"] for x in top})}},
        {"name": "every_top50_root_covers_two_distinct_valid_rows",
         "pass": all(len(rs) == 2 and len(set(rs)) == 2 and all(0 <= r < row_count for r in rs) for rs in rows),
         "detail": {"row_count": row_count}},
        {"name": "rank28_new_and_full_census_match_published_k28", "pass": k28_match,
         "detail": {"new": c28["result"], "full_triples": full28_triples["counts"],
                    "full_quints": full28_quints["counts"], "hist_expected": hist28_expected}},
        {"name": "rank28_two_classifiers_agree_on_new_and_full_regressions",
         "pass": c28["mismatches"] == 0 and full28_triples["mismatches"] == 0 and full28_quints["mismatches"] == 0,
         "detail": {"new": c28["compared"], "new_mismatches": c28["mismatches"],
                    "full_triples": full28_triples["compared"], "full_quints": full28_quints["compared"]}},
        {"name": "rank28_root_matches_published_anchor",
         "pass": top[27]["root"] == s28["rank28_root"]["root"] and list(rows[27]) == s28["rank28_root"]["rows"],
         "detail": {"root": top[27]["root"], "rows": list(rows[27])}},
        {"name": "rank29_root_and_rows_match_preread_target",
         "pass": root29["root"] == "00000000000000801202000000101001" and list(rows[28]) == [0, 16],
         "detail": {"root": root29["root"], "rows": list(rows[28])}},
        {"name": "rank29_two_classifiers_agree_on_all_24157_combinations",
         "pass": c29["mismatches"] == 0 and c29["compared"] == 24157,
         "detail": {"compared": c29["compared"], "mismatches": c29["mismatches"]}},
        {"name": "rank29_combination_totals_match_binomial_counts",
         "pass": actual_totals == expected_totals,
         "detail": {"actual": actual_totals, "expected": expected_totals}},
        {"name": "rank29_new_pair_census_4_shared_24_disjoint",
         "pass": c29["result"]["pair"]["b_only"] == 4 and c29["result"]["pair"]["disjoint"] == 24,
         "detail": c29["result"]["pair"]},
        {"name": "rank29_new_triple_census_195_32_151",
         "pass": (c29["result"]["triple"]["b_only"], c29["result"]["triple"]["zero"],
                  c29["result"]["triple"]["disjoint"]) == (195, 32, 151),
         "detail": c29["result"]["triple"]},
        {"name": "rank29_new_quad_census_1516_1535_225",
         "pass": (c29["result"]["quad"]["b_only"], c29["result"]["quad"]["zero"],
                  c29["result"]["quad"]["disjoint"]) == (1516, 1535, 225),
         "detail": c29["result"]["quad"]},
        {"name": "rank29_disjoint_quad_census_has_225_complete_eight_row_unions",
         "pass": len(c29["disjoint_quads"]) == 225 and all(len(q["rows_union"]) == 8 for q in c29["disjoint_quads"]),
         "detail": {"count": len(c29["disjoint_quads"])}},
        {"name": "rank29_b_only_quint_census_has_2128_records",
         "pass": len(c29["b_quints"]) == 2128, "detail": {"count": len(c29["b_quints"])}},
        {"name": "rank29_b_only_quint_double_row_histogram_matches",
         "pass": c29["hist"] == {"15": 283, "16": 172, "18": 1297, "19": 376}, "detail": c29["hist"]},
        {"name": "rank29_all_b_only_quints_have_three_b_only_two_disjoint_four_subsets",
         "pass": profile_counts == {"3/2/0": 2128}, "detail": profile_counts},
        {"name": "rank29_has_no_disjoint_quints",
         "pass": c29["result"]["quint"]["disjoint"] == 0,
         "detail": {"disjoint": c29["result"]["quint"]["disjoint"]}},
        {"name": "rank29_new_row_overlap_signature",
         "pass": row0_prior == 2 and row16_prior == 2,
         "detail": {"row0_prior_hits": row0_prior, "row16_prior_hits": row16_prior}},
        {"name": "rank29_full_quint_census_prev_layer_equals_published_k28",
         "pass": prev_split_ok,
         "detail": {"full": full29_quints["counts"], "full_hist": full29_quints["double_rows"],
                    "new_quint": c29["result"]["quint"], "new_hist": c29["hist"]}},
        {"name": "rank29_full_triple_census_recorded",
         "pass": full29_triples["mismatches"] == 0
         and full29_triples["counts"]["total"] == math.comb(29, 3),
         "detail": full29_triples["counts"]},
        {"name": "rank29_membership_ab_split_recorded",
         "pass": int(memA[root29["root"]]) + int(memB[root29["root"]]) == int(root29["membership"]),
         "detail": {"m29": root29["membership"], "a_part": memA[root29["root"]],
                    "b_part": memB[root29["root"]]}},
    ]
    output = {
        "schema": "n11-cost16-k29-preread-20261118-v1", "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "31-row cost-16 parent: rank-29 structural preread",
        "inputs": {
            "aggregate": {"path": str(AGG_PATH), "git_blob_sha1": AGG_SHA1},
            "k27_result": {"path": str(K27_PATH), "git_blob_sha1": K27_SHA1},
            "k28_result": {"path": str(K28_PATH), "git_blob_sha1": K28_SHA1},
        },
        "scope": {
            "parent": "00000000000000003800000008001000", "rows": 31, "minimum_cover_size": 16,
            "rank_convention": "top50_by_membership zero-based index; k=28 is index 27 and k=29 is index 28.",
            "classifier": "zero if a row occurs at least 3 times or at least two rows occur twice; b_only if exactly one row occurs twice; disjoint if no row is repeated.",
            "warning": "Membership counts are cover-plan counts, not search costs, verdicts, or game outcomes.",
        },
        "rank28_regression": {
            "root": top[27]["root"], "rows_covered": list(rows[27]),
            "new_census": c28["result"], "full_triple_census": full28_triples["counts"],
            "full_quint_census": full28_quints["counts"],
            "new_quint_double_row_histogram": c28["hist"],
            "new_quint_double_row_histogram_expected_from_published_split": hist28_expected,
            "matches_published_k28": k28_match,
        },
        "rank29": {
            "root": root29["root"], "rows_covered": list(rows[28]),
            "membership": root29["membership"], "a_part": memA[root29["root"]],
            "b_part": memB[root29["root"]],
            "row_overlap_signature": {"row0_prior_hits": row0_prior, "row16_prior_hits": row16_prior},
            "census": c29["result"], "quint_b_only_double_row_histogram": c29["hist"],
            "quint_four_subset_profile_distribution": profile_counts,
            "full_triple_census": full29_triples["counts"],
            "full_quint_census": full29_quints["counts"],
            "full_quint_b_only_double_rows": full29_quints["double_rows"],
            "disjoint_quad_records": c29["disjoint_quads"], "b_only_quint_records": c29["b_quints"],
        },
        "checks": checks, "check_count": len(checks), "all_pass": all(x["pass"] for x in checks),
        "interpretation_guard": "Structural preread of minimum-cover ban combinations only. It does not compute k=29 inclusion-exclusion Pm joints, classify any game position, or produce WIN/LOSS evidence.",
        "unknown_status": "Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
    }
    if not output["all_pass"]:
        failed = [{x["name"]: x["detail"]} for x in checks if not x["pass"]]
        raise RuntimeError(f"preread checks failed: {json.dumps(failed, ensure_ascii=False)}")
    out = args.output or root / EXP / "output/cost16-survival-k29-preread-20261118.json"
    out = out if out.is_absolute() else root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": True, "check_count": len(checks), "output": str(out),
                      "rank29_census": c29["result"], "double_row_histogram": c29["hist"],
                      "profile_distribution": profile_counts,
                      "full_quint_census": full29_quints["counts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

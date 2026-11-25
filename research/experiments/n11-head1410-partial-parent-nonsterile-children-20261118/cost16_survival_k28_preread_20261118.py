#!/usr/bin/env python3
"""Independent structural preread for the rank-28 cost-16 root.

Reads only the three pinned JSON inputs already published in this
experiment (phase-B aggregate, k=26 result, k=27 result). It does not
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
K26_PATH = EXP / "output/cost16-survival-k26-20261118.json"
K27_PATH = EXP / "output/cost16-survival-k27-20261118.json"
AGG_SHA1 = "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"
K26_SHA1 = "1841a281ff604e7f677b8c7772a7312f6f9da5e1"
K27_SHA1 = "3dc30ad6c51cc2d7678cc8777e4af2376267ddb8"


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
    k26 = load_pinned(root / K26_PATH, K26_SHA1)
    k27 = load_pinned(root / K27_PATH, K27_SHA1)
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

    # ---- rank-27 regression against the just-published k=27 result
    c27 = new_census(27, rows, row_masks)
    full27_triples = full_census(27, 3, rows, row_masks)
    full27_quints = full_census(27, 5, rows, row_masks)
    s26 = k26["structure"]
    s27 = k27["structure"]
    vals27 = k27["values"]
    new_pairs_27 = vals27["new_pair_joints"]
    pair_shared_27 = sum(bool(x["shared_row"]) for x in new_pairs_27.values())

    def class_census(records):
        counts = Counter(x["class"] for x in records.values())
        return {"b_only": counts["b_only"], "zero": counts["zero"],
                "disjoint": counts["disjoint"]}

    pair_records_27 = {key: {"class": "b_only" if x["shared_row"] else "disjoint"}
                       for key, x in new_pairs_27.items()}
    pairs_new_census_27 = class_census(pair_records_27)
    triple_census_27 = class_census(vals27["new_triples"])
    quad_census_27 = class_census(vals27["new_quads"])
    quint_b_only_27 = len(vals27["new_quints_b_only"])
    # expected rank-27 new b_only double-row histogram = published k27
    # full histogram minus published k26 full histogram (machine-derived
    # from the two pinned result JSONs, no hand-written table)
    hist27_expected = {}
    for rk, v27 in s27["quint_b_only_double_rows"].items():
        diff = int(v27) - int(s26["quint_b_only_double_rows"].get(rk, 0))
        if diff:
            hist27_expected[str(rk)] = diff
    k27_match = (
        len(new_pairs_27) == 26 and c27["result"]["pair"]["total"] == 26
        and c27["result"]["pair"]["b_only"] == pair_shared_27 == pairs_new_census_27["b_only"] == 13
        and c27["result"]["pair"]["disjoint"] == pairs_new_census_27["disjoint"] == 13
        and c27["result"]["triple"]["total"] == len(vals27["new_triples"]) == 325
        and all(c27["result"]["triple"][k] == triple_census_27[k]
                for k in ("b_only", "zero", "disjoint"))
        and c27["result"]["quad"]["total"] == len(vals27["new_quads"]) == 2600
        and all(c27["result"]["quad"][k] == quad_census_27[k] == s27["new_quad_census"][k]
                for k in ("b_only", "zero", "disjoint"))
        and c27["result"]["quint"]["b_only"] == quint_b_only_27 == s27["new_quint_census"]["b_only"] == 309
        and c27["result"]["quint"]["disjoint"] == s27["new_quint_census"]["disjoint"] == 0
        and c27["result"]["quint"]["zero"] == s27["new_quint_census"]["zero"]
        == int(s27["quints_zero_synth_count"]) == 14641
        and full27_triples["counts"]["b_only"] == s27["triple_census_k27"]["b_only"]
        and full27_triples["counts"]["zero"] == s27["triple_census_k27"]["zero"]
        and full27_triples["counts"]["disjoint"] == s27["triple_census_k27"]["disjoint"]
        and full27_quints["counts"]["b_only"] == s27["quint_census_k27"]["b_only"]
        and full27_quints["counts"]["zero"] == s27["quint_census_k27"]["zero"]
        and full27_quints["counts"]["disjoint"] == s27["quint_census_k27"]["disjoint"] == 0
        and full27_quints["double_rows"] == {str(r): int(v) for r, v in s27["quint_b_only_double_rows"].items()}
        and c27["hist"] == hist27_expected
    )

    # ---- rank-28 structural preread
    c28 = new_census(28, rows, row_masks)
    root28 = top[27]
    row18_prior = sum(18 in rs for rs in rows[:27])
    row20_prior = sum(20 in rs for rs in rows[:27])
    profile_counts = Counter(
        f'{q["four_subset_profile"]["b_only"]}/'
        f'{q["four_subset_profile"]["disjoint"]}/'
        f'{q["four_subset_profile"]["zero"]}'
        for q in c28["b_quints"]
    )
    profile_counts = dict(sorted(profile_counts.items()))
    full28_triples = full_census(28, 3, rows, row_masks)
    full28_quints = full_census(28, 5, rows, row_masks)
    # new = full minus prev layer: the rank-28 full quint census must
    # remove exactly the published k=27 full census as its prev layer
    prev_split_ok = (
        full28_quints["counts"]["b_only"] - c28["result"]["quint"]["b_only"]
        == s27["quint_census_k27"]["b_only"]
        and full28_quints["counts"]["zero"] - c28["result"]["quint"]["zero"]
        == s27["quint_census_k27"]["zero"]
        and full28_quints["counts"]["disjoint"] == 0
        and full28_quints["double_rows"] == {
            str(r): int(s27["quint_b_only_double_rows"].get(r, 0))
            + int(c28["hist"].get(r, 0)) for r in ("15", "18", "19")
        }
    )
    actual_totals = [c28["result"][n]["total"] for n in ("pair", "triple", "quad", "quint")]
    expected_totals = [27, 351, 2925, 17550]

    checks = [
        {"name": "top50_has_50_rows", "pass": len(top) == 50, "detail": {"actual": len(top)}},
        {"name": "top50_root_keys_unique", "pass": len({x["root"] for x in top}) == 50,
         "detail": {"unique": len({x["root"] for x in top})}},
        {"name": "every_top50_root_covers_two_distinct_valid_rows",
         "pass": all(len(rs) == 2 and len(set(rs)) == 2 and all(0 <= r < row_count for r in rs) for rs in rows),
         "detail": {"row_count": row_count}},
        {"name": "rank27_new_and_full_census_match_published_k27", "pass": k27_match,
         "detail": {"new": c27["result"], "full_triples": full27_triples["counts"],
                    "full_quints": full27_quints["counts"], "hist_expected": hist27_expected}},
        {"name": "rank27_two_classifiers_agree_on_new_and_full_regressions",
         "pass": c27["mismatches"] == 0 and full27_triples["mismatches"] == 0 and full27_quints["mismatches"] == 0,
         "detail": {"new": c27["compared"], "new_mismatches": c27["mismatches"],
                    "full_triples": full27_triples["compared"], "full_quints": full27_quints["compared"]}},
        {"name": "rank27_root_matches_published_anchor",
         "pass": top[26]["root"] == s27["rank27_root"]["root"] and list(rows[26]) == s27["rank27_root"]["rows"],
         "detail": {"root": top[26]["root"], "rows": list(rows[26])}},
        {"name": "rank28_root_and_rows_match_preread_target",
         "pass": root28["root"] == "00000000000000801202050000001000" and list(rows[27]) == [18, 20],
         "detail": {"root": root28["root"], "rows": list(rows[27])}},
        {"name": "rank28_two_classifiers_agree_on_all_20853_combinations",
         "pass": c28["mismatches"] == 0 and c28["compared"] == 20853,
         "detail": {"compared": c28["compared"], "mismatches": c28["mismatches"]}},
        {"name": "rank28_combination_totals_match_binomial_counts",
         "pass": actual_totals == expected_totals,
         "detail": {"actual": actual_totals, "expected": expected_totals}},
        {"name": "rank28_new_pair_census_14_shared_13_disjoint",
         "pass": c28["result"]["pair"]["b_only"] == 14 and c28["result"]["pair"]["disjoint"] == 13,
         "detail": c28["result"]["pair"]},
        {"name": "rank28_new_triple_census_214_99_38",
         "pass": (c28["result"]["triple"]["b_only"], c28["result"]["triple"]["zero"],
                  c28["result"]["triple"]["disjoint"]) == (214, 99, 38),
         "detail": c28["result"]["triple"]},
        {"name": "rank28_new_quad_census_626_2277_22",
         "pass": (c28["result"]["quad"]["b_only"], c28["result"]["quad"]["zero"],
                  c28["result"]["quad"]["disjoint"]) == (626, 2277, 22),
         "detail": c28["result"]["quad"]},
        {"name": "rank28_disjoint_quad_census_has_22_complete_eight_row_unions",
         "pass": len(c28["disjoint_quads"]) == 22 and all(len(q["rows_union"]) == 8 for q in c28["disjoint_quads"]),
         "detail": {"count": len(c28["disjoint_quads"])}},
        {"name": "rank28_b_only_quint_census_has_331_records",
         "pass": len(c28["b_quints"]) == 331, "detail": {"count": len(c28["b_quints"])}},
        {"name": "rank28_b_only_quint_double_row_histogram_matches",
         "pass": c28["hist"] == {"15": 38, "18": 255, "19": 38}, "detail": c28["hist"]},
        {"name": "rank28_all_b_only_quints_have_three_b_only_two_disjoint_four_subsets",
         "pass": profile_counts == {"3/2/0": 331}, "detail": profile_counts},
        {"name": "rank28_has_no_disjoint_quints",
         "pass": c28["result"]["quint"]["disjoint"] == 0,
         "detail": {"disjoint": c28["result"]["quint"]["disjoint"]}},
        {"name": "rank28_new_row_overlap_signature",
         "pass": row18_prior == 14 and row20_prior == 0,
         "detail": {"row18_prior_hits": row18_prior, "row20_prior_hits": row20_prior}},
        {"name": "rank28_full_quint_census_prev_layer_equals_published_k27",
         "pass": prev_split_ok,
         "detail": {"full": full28_quints["counts"], "full_hist": full28_quints["double_rows"],
                    "new_quint": c28["result"]["quint"], "new_hist": c28["hist"]}},
        {"name": "rank28_full_triple_census_recorded",
         "pass": full28_triples["mismatches"] == 0
         and full28_triples["counts"]["total"] == math.comb(28, 3),
         "detail": full28_triples["counts"]},
        {"name": "rank28_membership_ab_split_recorded",
         "pass": int(memA[root28["root"]]) + int(memB[root28["root"]]) == int(root28["membership"]),
         "detail": {"m28": root28["membership"], "a_part": memA[root28["root"]],
                    "b_part": memB[root28["root"]]}},
    ]
    output = {
        "schema": "n11-cost16-k28-preread-20261118-v1", "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "31-row cost-16 parent: rank-28 structural preread",
        "inputs": {
            "aggregate": {"path": str(AGG_PATH), "git_blob_sha1": AGG_SHA1},
            "k26_result": {"path": str(K26_PATH), "git_blob_sha1": K26_SHA1},
            "k27_result": {"path": str(K27_PATH), "git_blob_sha1": K27_SHA1},
        },
        "scope": {
            "parent": "00000000000000003800000008001000", "rows": 31, "minimum_cover_size": 16,
            "rank_convention": "top50_by_membership zero-based index; k=27 is index 26 and k=28 is index 27.",
            "classifier": "zero if a row occurs at least 3 times or at least two rows occur twice; b_only if exactly one row occurs twice; disjoint if no row is repeated.",
            "warning": "Membership counts are cover-plan counts, not search costs, verdicts, or game outcomes.",
        },
        "rank27_regression": {
            "root": top[26]["root"], "rows_covered": list(rows[26]),
            "new_census": c27["result"], "full_triple_census": full27_triples["counts"],
            "full_quint_census": full27_quints["counts"],
            "new_quint_double_row_histogram": c27["hist"],
            "new_quint_double_row_histogram_expected_from_published_split": hist27_expected,
            "matches_published_k27": k27_match,
        },
        "rank28": {
            "root": root28["root"], "rows_covered": list(rows[27]),
            "membership": root28["membership"], "a_part": memA[root28["root"]],
            "b_part": memB[root28["root"]],
            "row_overlap_signature": {"row18_prior_hits": row18_prior, "row20_prior_hits": row20_prior},
            "census": c28["result"], "quint_b_only_double_row_histogram": c28["hist"],
            "quint_four_subset_profile_distribution": profile_counts,
            "full_triple_census": full28_triples["counts"],
            "full_quint_census": full28_quints["counts"],
            "full_quint_b_only_double_rows": full28_quints["double_rows"],
            "disjoint_quad_records": c28["disjoint_quads"], "b_only_quint_records": c28["b_quints"],
        },
        "checks": checks, "check_count": len(checks), "all_pass": all(x["pass"] for x in checks),
        "interpretation_guard": "Structural preread of minimum-cover ban combinations only. It does not compute k=28 inclusion-exclusion Pm joints, classify any game position, or produce WIN/LOSS evidence.",
        "unknown_status": "Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
    }
    if not output["all_pass"]:
        failed = [{x["name"]: x["detail"]} for x in checks if not x["pass"]]
        raise RuntimeError(f"preread checks failed: {json.dumps(failed, ensure_ascii=False)}")
    out = args.output or root / EXP / "output/cost16-survival-k28-preread-20261118.json"
    out = out if out.is_absolute() else root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": True, "check_count": len(checks), "output": str(out),
                      "rank28_census": c28["result"], "double_row_histogram": c28["hist"],
                      "profile_distribution": profile_counts,
                      "full_quint_census": full28_quints["counts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent structural preread for the rank-27 cost-16 root.

Reads only the two pinned JSON inputs already published in this experiment.
It does not call the Pm engine and does not compute any game verdict.
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
AGG_SHA1 = "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"
K26_SHA1 = "1841a281ff604e7f677b8c7772a7312f6f9da5e1"


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
    compared = mismatches = 0
    for ids in itertools.combinations(range(n), size):
        a = classify_map(rows, ids)
        b = classify_masks(row_masks, ids)
        compared += 1
        mismatches += a != b
        counts[a[0]] += 1
    return {
        "counts": {
            "b_only": counts["b_only"], "zero": counts["zero"],
            "disjoint": counts["disjoint"], "total": sum(counts.values()),
            "expected_total": math.comb(n, size),
        },
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
    top = agg["derived"]["top50_by_membership"]
    rows = [tuple(x["rows_covered"]) for x in top]
    row_count = agg["derived"]["rows"]
    if len(top) != 50 or len({x["root"] for x in top}) != 50:
        raise RuntimeError("top50 cardinality/root uniqueness failure")
    if not all(len(rs) == 2 and len(set(rs)) == 2 and all(0 <= r < row_count for r in rs) for rs in rows):
        raise RuntimeError("top50 row-pair validation failure")

    row_masks = [0] * row_count
    for i, rs in enumerate(rows):
        for r in rs:
            row_masks[r] |= 1 << i

    c26 = new_census(26, rows, row_masks)
    full26_triples = full_census(26, 3, rows, row_masks)
    full26_quints = full_census(26, 5, rows, row_masks)
    pair26 = list(k26["values"]["new_pair_joints"].values())
    pair_shared = sum(bool(x["shared_row"]) for x in pair26)
    s26 = k26["structure"]
    k26_match = (
        c26["result"]["pair"]["b_only"] == pair_shared
        and c26["result"]["pair"]["disjoint"] == len(pair26) - pair_shared
        and full26_triples["counts"] | {} == {
            "b_only": s26["triple_census_k26"]["b_only"],
            "zero": s26["triple_census_k26"]["zero"],
            "disjoint": s26["triple_census_k26"]["disjoint"],
            "total": math.comb(26, 3), "expected_total": math.comb(26, 3),
        }
        and c26["result"]["quad"]["b_only"] == s26["new_quad_census"]["b_only"]
        and c26["result"]["quad"]["zero"] == s26["new_quad_census"]["zero"]
        and c26["result"]["quad"]["disjoint"] == s26["new_quad_census"]["disjoint"]
        and full26_quints["counts"]["b_only"] == s26["quint_census_k26"]["b_only"]
        and full26_quints["counts"]["zero"] == s26["quint_census_k26"]["zero"]
        and full26_quints["counts"]["disjoint"] == s26["quint_census_k26"]["disjoint"]
        and c26["result"]["quint"]["b_only"] == s26["quint_census_k26"]["b_only"]
        and c26["result"]["quint"]["zero"] == s26["quints_zero_synth_count"]
        and c26["result"]["quint"]["disjoint"] == 0
        and c26["hist"] == {str(k): v for k, v in s26["quint_b_only_double_rows"].items()}
    )

    c27 = new_census(27, rows, row_masks)
    root27 = top[26]
    row12_prior = sum(12 in rs for rs in rows[:26])
    row18_prior = sum(18 in rs for rs in rows[:26])
    profile_counts = Counter(
        f'{q["four_subset_profile"]["b_only"]}/'
        f'{q["four_subset_profile"]["disjoint"]}/'
        f'{q["four_subset_profile"]["zero"]}'
        for q in c27["b_quints"]
    )
    profile_counts = dict(sorted(profile_counts.items()))
    actual_totals = [c27["result"][n]["total"] for n in ("pair", "triple", "quad", "quint")]
    expected_totals = [26, 325, 2600, 14950]

    checks = [
        {"name": "top50_has_50_rows", "pass": len(top) == 50, "detail": {"actual": len(top)}},
        {"name": "top50_root_keys_unique", "pass": len({x["root"] for x in top}) == 50,
         "detail": {"unique": len({x["root"] for x in top})}},
        {"name": "every_top50_root_covers_two_distinct_valid_rows",
         "pass": all(len(rs) == 2 and len(set(rs)) == 2 and all(0 <= r < row_count for r in rs) for rs in rows),
         "detail": {"row_count": row_count}},
        {"name": "rank26_new_and_full_census_match_published_k26", "pass": k26_match,
         "detail": {"new": c26["result"], "full_triples": full26_triples["counts"],
                    "full_quints": full26_quints["counts"]}},
        {"name": "rank26_two_classifiers_agree_on_new_and_full_regressions",
         "pass": c26["mismatches"] == 0 and full26_triples["mismatches"] == 0 and full26_quints["mismatches"] == 0,
         "detail": {"new": c26["compared"], "new_mismatches": c26["mismatches"],
                    "full_triples": full26_triples, "full_quints": full26_quints}},
        {"name": "rank26_root_matches_published_anchor",
         "pass": top[25]["root"] == s26["rank26_root"]["root"] and list(rows[25]) == s26["rank26_root"]["rows"],
         "detail": {"root": top[25]["root"], "rows": list(rows[25])}},
        {"name": "rank27_root_and_rows_match_preread_target",
         "pass": root27["root"] == "00000000000100003820000008001000" and list(rows[26]) == [12, 18],
         "detail": {"root": root27["root"], "rows": list(rows[26])}},
        {"name": "rank27_two_classifiers_agree_on_all_17901_combinations",
         "pass": c27["mismatches"] == 0 and c27["compared"] == 17901,
         "detail": {"compared": c27["compared"], "mismatches": c27["mismatches"]}},
        {"name": "rank27_combination_totals_match_binomial_counts",
         "pass": actual_totals == expected_totals,
         "detail": {"actual": actual_totals, "expected": expected_totals}},
        {"name": "rank27_disjoint_quad_census_has_22_complete_eight_row_unions",
         "pass": len(c27["disjoint_quads"]) == 22 and all(len(q["rows_union"]) == 8 for q in c27["disjoint_quads"]),
         "detail": {"count": len(c27["disjoint_quads"])}},
        {"name": "rank27_b_only_quint_census_has_309_records",
         "pass": len(c27["b_quints"]) == 309, "detail": {"count": len(c27["b_quints"])}},
        {"name": "rank27_b_only_quint_double_row_histogram_matches",
         "pass": c27["hist"] == {"15": 38, "18": 233, "19": 38}, "detail": c27["hist"]},
        {"name": "rank27_all_b_only_quints_have_three_b_only_two_disjoint_four_subsets",
         "pass": profile_counts == {"3/2/0": 309}, "detail": profile_counts},
        {"name": "rank27_has_no_disjoint_quints",
         "pass": c27["result"]["quint"]["disjoint"] == 0,
         "detail": {"disjoint": c27["result"]["quint"]["disjoint"]}},
        {"name": "rank27_new_row_overlap_signature",
         "pass": row12_prior == 0 and row18_prior == 13,
         "detail": {"row12_prior_hits": row12_prior, "row18_prior_hits": row18_prior}},
    ]
    output = {
        "schema": "n11-cost16-k27-preread-20261118-v1", "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "31-row cost-16 parent: rank-27 structural preread",
        "inputs": {
            "aggregate": {"path": str(AGG_PATH), "git_blob_sha1": AGG_SHA1},
            "k26_result": {"path": str(K26_PATH), "git_blob_sha1": K26_SHA1},
        },
        "scope": {
            "parent": "00000000000000003800000008001000", "rows": 31, "minimum_cover_size": 16,
            "rank_convention": "top50_by_membership zero-based index; k=26 is index 25 and k=27 is index 26.",
            "classifier": "zero if a row occurs at least 3 times or at least two rows occur twice; b_only if exactly one row occurs twice; disjoint if no row is repeated.",
            "warning": "Membership counts are cover-plan counts, not search costs, verdicts, or game outcomes.",
        },
        "rank26_regression": {
            "root": top[25]["root"], "rows_covered": list(rows[25]),
            "new_census": c26["result"], "full_triple_census": full26_triples["counts"],
            "full_quint_census": full26_quints["counts"],
            "new_quint_double_row_histogram": c26["hist"], "matches_published_k26": k26_match,
        },
        "rank27": {
            "root": root27["root"], "rows_covered": list(rows[26]),
            "row_overlap_signature": {"row12_prior_hits": row12_prior, "row18_prior_hits": row18_prior},
            "census": c27["result"], "quint_b_only_double_row_histogram": c27["hist"],
            "quint_four_subset_profile_distribution": profile_counts,
            "disjoint_quad_records": c27["disjoint_quads"], "b_only_quint_records": c27["b_quints"],
        },
        "checks": checks, "check_count": len(checks), "all_pass": all(x["pass"] for x in checks),
        "interpretation_guard": "Structural preread of minimum-cover ban combinations only. It does not compute k=27 inclusion-exclusion Pm joints, classify any game position, or produce WIN/LOSS evidence.",
        "unknown_status": "Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
    }
    if not output["all_pass"]:
        raise RuntimeError("one or more preread checks failed")
    out = args.output or root / EXP / "output/cost16-survival-k27-preread-20261118.json"
    out = out if out.is_absolute() else root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": True, "check_count": len(checks), "output": str(out),
                      "rank27_census": c27["result"], "double_row_histogram": c27["hist"],
                      "profile_distribution": profile_counts}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

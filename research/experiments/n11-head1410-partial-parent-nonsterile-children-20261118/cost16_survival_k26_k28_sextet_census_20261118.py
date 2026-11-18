#!/usr/bin/env python3
"""Sextet-era census for the 31-row cost-16 parent
00000000000000003800000008001000: machine verification that the
quint-era inclusion-exclusion truncation (kill(k) = sum m - sum j2
+ sum j3 - sum j4 + sum j5, no sixth-order term) is sound at
k = 26, 27, 28.

Why this matters.  The pre-k26 eras truncated the I-E at quads with
an explicit machine census: every C(k,5) 5-subset was structurally
zero.  The k=26 publication opened the quint era (1,872 b_only
5-subsets carry a j5 term) but the truncation beyond size 5 has so
far rested on no published size-6 census: kill(25) needed no j5,
kill(26)/kill(27) carry j5, and both implicitly need every subset of
size >= 6 to be structurally zero.  This script verifies that with
two independent classifiers over the FULL census:

  C(26,6) = 230,230   all zero  (retroactively closes kill(26))
  C(27,6) = 296,010   all zero  (retroactively closes kill(27))
  C(28,6) = 376,740   all zero  (anchors the upcoming k=28 layer)
  C(28,7) = 1,184,040 all zero  (empirical anchor one order deeper)
  C(28,8) = 3,108,105 all zero

Hereditary closure: the 'zero' class is superset-closed (adding
roots never lowers a row multiplicity; a row hit >= 3 x, or two rows
hit 2 x, stay so under supersets).  A minimum cover meeting the
parent's published structure is either A-type (15 disjoint pairs +
1 disjoint singleton: every row exactly once) or B-type (16 pairs,
exactly one doubly covered row), so any subset with a >= 3 x row or
two >= 2 x rows fits no cover and its joint is exactly 0.  Hence
all-zero C(n,6) closes every size >= 6 for the top-n, and a B-type
sextet with one doubled row cannot exist here because every 6th
root meets the 5-subset's row union:

  for every b_only quint among the top-26 / top-27 / top-28 and
  every root outside it, the 6th root shares >= 1 row with the
  quint's 9-row union (machine-verified below; the 9-row union of
  each b_only quint is a blocking set for all other top roots).

Cover-plan combinatorics only.  No engine run, no verdict.  The
membership/joint values are ban-avoidance cover counts, not search
costs, not WIN/LOSS evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from collections import Counter
from pathlib import Path

EXP = Path("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118")
AGG_PATH = EXP / "output/cost16-b-phase-groups-20261118.json"
K26_JSON_PATH = EXP / "output/cost16-survival-k26-20261118.json"
K27_JSON_PATH = EXP / "output/cost16-survival-k27-20261118.json"
AGG_SHA1 = "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"
K26_JSON_SHA1 = "1841a281ff604e7f677b8c7772a7312f6f9da5e1"
K27_JSON_SHA1 = "3dc30ad6c51cc2d7678cc8777e4af2376267ddb8"


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


def full_census(n, size, rows, row_masks):
    counts = Counter()
    compared = mismatches = 0
    for ids in itertools.combinations(range(n), size):
        a = classify_map(rows, ids)
        b = classify_masks(row_masks, ids)
        compared += 1
        mismatches += a != b
        counts[a[0]] += 1
    total = sum(counts.values())
    return {
        "b_only": counts["b_only"], "zero": counts["zero"],
        "disjoint": counts["disjoint"], "total": total,
        "expected_total": math.comb(n, size),
        "total_ok": total == math.comb(n, size),
        "compared": compared, "mismatches": mismatches,
    }


def quint_blocking_stats(n, rows, row_masks):
    """For every b_only quint among the top-n and every top-n root
    outside it, count how many share >= 1 row with the quint's
    9-row union, and how many are fully disjoint from it."""
    hits = 0
    misses = 0
    quint_count = 0
    for ids in itertools.combinations(range(n), 5):
        kind, _dbl = classify_masks(row_masks, ids)
        if kind != "b_only":
            continue
        quint_count += 1
        union = {r for i in ids for r in rows[i]}
        for j in range(n):
            if j in ids:
                continue
            if union & set(rows[j]):
                hits += 1
            else:
                misses += 1
    return {"quint_count": quint_count, "outside_root_hits_union": hits,
            "outside_root_fully_disjoint": misses,
            "every_quint_union_blocks_all_outside_roots": misses == 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    agg = load_pinned(root / AGG_PATH, AGG_SHA1)
    k26 = load_pinned(root / K26_JSON_PATH, K26_JSON_SHA1)
    k27 = load_pinned(root / K27_JSON_PATH, K27_JSON_SHA1)
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

    t0 = time.time()
    censuses = {}
    for n in (26, 27, 28):
        censuses[f"k{n}_size6"] = full_census(n, 6, rows, row_masks)
    for size in (7, 8):
        censuses[f"k28_size{size}"] = full_census(28, size, rows, row_masks)
    quint_blocking = {f"top{n}": quint_blocking_stats(n, rows, row_masks)
                      for n in (26, 27, 28)}
    elapsed = round(time.time() - t0, 1)

    s26 = k26["structure"]
    s27 = k27["structure"]
    checks = [
        {"name": "sextet_census_k26_all_zero",
         "pass": (censuses["k26_size6"]["expected_total"] == 230230
                  and censuses["k26_size6"]["zero"] == 230230
                  and censuses["k26_size6"]["b_only"] == 0
                  and censuses["k26_size6"]["disjoint"] == 0
                  and censuses["k26_size6"]["mismatches"] == 0
                  and censuses["k26_size6"]["total_ok"]),
         "detail": censuses["k26_size6"]},
        {"name": "sextet_census_k27_all_zero",
         "pass": (censuses["k27_size6"]["expected_total"] == 296010
                  and censuses["k27_size6"]["zero"] == 296010
                  and censuses["k27_size6"]["b_only"] == 0
                  and censuses["k27_size6"]["disjoint"] == 0
                  and censuses["k27_size6"]["mismatches"] == 0
                  and censuses["k27_size6"]["total_ok"]),
         "detail": censuses["k27_size6"]},
        {"name": "sextet_census_k28_all_zero",
         "pass": (censuses["k28_size6"]["expected_total"] == 376740
                  and censuses["k28_size6"]["zero"] == 376740
                  and censuses["k28_size6"]["b_only"] == 0
                  and censuses["k28_size6"]["disjoint"] == 0
                  and censuses["k28_size6"]["mismatches"] == 0
                  and censuses["k28_size6"]["total_ok"]),
         "detail": censuses["k28_size6"]},
        {"name": "septet_census_k28_all_zero",
         "pass": (censuses["k28_size7"]["expected_total"] == 1184040
                  and censuses["k28_size7"]["zero"] == 1184040
                  and censuses["k28_size7"]["mismatches"] == 0
                  and censuses["k28_size7"]["total_ok"]),
         "detail": censuses["k28_size7"]},
        {"name": "octet_census_k28_all_zero",
         "pass": (censuses["k28_size8"]["expected_total"] == 3108105
                  and censuses["k28_size8"]["zero"] == 3108105
                  and censuses["k28_size8"]["mismatches"] == 0
                  and censuses["k28_size8"]["total_ok"]),
         "detail": censuses["k28_size8"]},
        {"name": "published_k26_quint_era_census_context_matches",
         "pass": (s26["quint_census_k26"]["b_only"] == 1872
                  and s26["quint_census_k26"]["b_only"
                  ] == quint_blocking["top26"]["quint_count"]
                  and "+ sum j5" in s26["ie_mechanism"]),
         "detail": {"b_only_quint_census": s26["quint_census_k26"]["b_only"],
                    "ie_mechanism_of_k26": s26["ie_mechanism"]}},
        {"name": "published_k27_quint_era_census_context_matches",
         "pass": (s27["quint_census_k27"]["b_only"] == 2181
                  and s27["quint_census_k27"]["b_only"
                  ] == quint_blocking["top27"]["quint_count"]
                  and "+ sum j5" in s27["ie_mechanism"]),
         "detail": {"b_only_quint_census": s27["quint_census_k27"]["b_only"],
                    "ie_mechanism_of_k27": s27["ie_mechanism"]}},
        {"name": "blocking_set_property_top26",
         "pass": quint_blocking["top26"]["every_quint_union_blocks_all_outside_roots"],
         "detail": quint_blocking["top26"]},
        {"name": "blocking_set_property_top27",
         "pass": quint_blocking["top27"]["every_quint_union_blocks_all_outside_roots"],
         "detail": quint_blocking["top27"]},
        {"name": "blocking_set_property_top28",
         "pass": quint_blocking["top28"]["every_quint_union_blocks_all_outside_roots"],
         "detail": quint_blocking["top28"]},
        {"name": "hereditary_closure_statement",
         "pass": True,
         "detail": {"lemma": "zero is superset-closed: if subset S has a row hit >= 3 times, or two rows hit twice, every superset of S does too; and every subset of size >= 6 of the top-26/27/28 contains a 6-subset, which the census shows is zero.",
                    "consequence": "no subset of size >= 6 of the top-26/27/28 admits any A-type or B-type minimum cover, so every joint j(S) with |S| >= 6 is exactly 0 and the quint-order truncation of kill(k) for k = 26, 27, 28 is complete"}},
    ]
    output = {
        "schema": "n11-cost16-sextet-census-20261118-v1", "date": "2026-11-18",
        "lane": "n11 long lane (self execution)",
        "title": "31-row cost-16 parent: sextet-era census closing the quint-order I-E truncation at k = 26, 27, 28",
        "inputs": {
            "aggregate": {"path": str(AGG_PATH), "git_blob_sha1": AGG_SHA1},
            "k26_result": {"path": str(K26_JSON_PATH), "git_blob_sha1": K26_JSON_SHA1,
                            "commit": "3b68d6b4"},
            "k27_result": {"path": str(K27_JSON_PATH), "git_blob_sha1": K27_JSON_SHA1,
                            "commit": "9b804a9c"},
            "rank28_preread": {"commit": "e6cc8e05",
                               "note": "the parallel lane's rank-28 preread (census values identical to this lane's independent derivation) does not cover the size >= 6 censuses; this script adds and closes them"},
        },
        "scope": {
            "parent": "00000000000000003800000008001000", "rows": 31,
            "minimum_cover_size": 16,
            "classifier": "zero if a row occurs at least 3 times or at least two rows occur twice; b_only if exactly one row occurs twice; disjoint if no row is repeated.  A-type covers (15 disjoint pairs + 1 disjoint singleton) touch every row exactly once; B-type covers (16 pairs) touch exactly one row twice.  A zero subset therefore fits no cover and its joint is exactly 0.",
            "hereditary_lemma": "zero is superset-closed; all-zero C(n,6) therefore closes every size >= 6 for the top-n.",
            "warning": "Membership and joint counts are cover-plan counts, not search costs, verdicts, or game outcomes.",
        },
        "censuses": censuses,
        "quint_blocking_stats": quint_blocking,
        "retroactive_and_prospective_closure": {
            "kill_26": "C(26,6) all zero closes the published kill(26) quint-order truncation retroactively",
            "kill_27": "C(27,6) all zero closes the published kill(27) quint-order truncation retroactively",
            "kill_28": "C(28,6) all zero pre-approves the k=28 layer: the k=28 I-E may keep the k=27 quint mechanism and needs no sixth-order term",
            "note": "the C(28,7)/C(28,8) censuses are empirical anchors one order beyond the lemma",
        },
        "runtime_seconds": elapsed,
        "checks": checks, "check_count": len(checks),
        "all_pass": all(x["pass"] for x in checks),
        "interpretation_guard": "Structural census of minimum-cover ban combinations only. No Pm joint value was computed here for size >= 6 subsets (they are all structurally zero); no game position was classified; no engine search was started.",
        "unknown_status": "Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
    }
    if not output["all_pass"]:
        raise RuntimeError("one or more sextet-census checks failed")
    out = args.output or root / EXP / "output/cost16-survival-k26-k28-sextet-census-20261118.json"
    out = out if out.is_absolute() else root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": True, "check_count": len(checks),
                      "output": str(out), "runtime_seconds": elapsed,
                      "summarized": {k: (v["zero"], v["b_only"], v["disjoint"])
                                     for k, v in censuses.items()},
                      "quint_blocking": quint_blocking},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

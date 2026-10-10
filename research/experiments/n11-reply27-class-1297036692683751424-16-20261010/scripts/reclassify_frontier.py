"""Reclassify the complete S4 frontier from frozen geometry and exact S5 cache."""
from __future__ import annotations

import gzip
import hashlib
import json
import argparse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
BASE_AUDIT = ROOT / "research/experiments/n11-independent-exact-audit-20261010/output/audit.json"
CACHE = EXP / "output/current-exact-s5.cache"
S4_KEY = (1297036692683751424, 16)
S5_WIN_KEY = (1297036692683751424, 67108880)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_cache(path: Path) -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split(",")
        if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
            raise ValueError(f"invalid S5 cache row {line_no}: {line}")
        key, verdict = (int(fields[1]), int(fields[2])), int(fields[4])
        if verdict not in (1, 2) or (key in result and result[key] != verdict):
            raise ValueError(f"invalid/conflicting cache verdict at row {line_no}: {line}")
        result[key] = verdict
    return result


def classify_s4(row: dict, exact: dict[tuple[int, int], int]) -> str:
    vals = [exact.get(tuple(c), 0) for c in row["children"]]
    # Fixed original-player perspective: S4 is OR over its S5 children.
    return "WIN" if 1 in vals else "LOSS" if vals and all(v == 2 for v in vals) else "UNKNOWN"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, default=CACHE)
    parser.add_argument("--compare-to-cache", type=Path)
    parser.add_argument("--out", type=Path, default=EXP / "output/frontier-reclassification.json")
    args = parser.parse_args()
    cache_path = args.cache if args.cache.is_absolute() else ROOT / args.cache
    compare_path = args.compare_to_cache if args.compare_to_cache is None or args.compare_to_cache.is_absolute() else ROOT / args.compare_to_cache
    out_path = args.out if args.out.is_absolute() else ROOT / args.out
    geometry = json.loads(gzip.decompress(GEOMETRY.read_bytes()))
    exact = read_cache(cache_path)
    if len(geometry) != 3384 or len(exact) < 5735 or exact.get(S5_WIN_KEY) != 1:
        raise SystemExit(f"unexpected frozen input size: geometry={len(geometry)} exact={len(exact)}")

    counts: Counter[str] = Counter()
    secured: set[int] = set()
    records = []
    selected = None
    candidates = []
    for row in geometry:
        key = tuple(row["key"])
        children = [tuple(c) for c in row["children"]]
        if not children or len(children) != len(set(children)):
            raise SystemExit(f"invalid/empty S5 boundary for S4 {key}")
        vals = [exact.get(child, 0) for child in children]
        verdict = classify_s4(row, exact)
        counts[verdict] += 1
        boundary = dict(Counter({0: "UNKNOWN", 1: "WIN", 2: "LOSS"}[v] for v in vals))
        record = {"key": list(key), "verdict": verdict, "coverage": sorted(row["coverage"]),
                  "s5_children": len(children), "boundary": boundary}
        records.append(record)
        if verdict == "LOSS":
            secured.update(row["coverage"])
        if key == S4_KEY:
            selected = record
        if verdict == "UNKNOWN":
            unknown_children = [child for child, v in zip(children, vals) if v == 0]
            candidates.append({**record, "unknown_s5_children": len(unknown_children),
                               "known_s5_losses": boundary.get("LOSS", 0)})

    remaining = sorted(set(range(121)) - {60, 27} - secured)
    if selected is None:
        raise SystemExit("target S4 class missing from complete geometry")
    if selected["boundary"] != {"LOSS": 9, "WIN": 1, "UNKNOWN": 98}:
        raise SystemExit(f"target S4 boundary mismatch: {selected}")
    if selected["verdict"] != "WIN" or remaining != [100, 108]:
        raise SystemExit(f"unexpected target/frontier status: {selected}; remaining={remaining}")

    baseline_counts = None
    changes = []
    if compare_path:
        baseline_exact = read_cache(compare_path)
        if any(exact.get(key) != verdict for key, verdict in baseline_exact.items()):
            raise SystemExit("new exact cache conflicts with its requested baseline")
        baseline_statuses = {tuple(row["key"]): classify_s4(row, baseline_exact) for row in geometry}
        current_statuses = {tuple(row["key"]): classify_s4(row, exact) for row in geometry}
        changes = []
        for key in sorted(current_statuses):
            if baseline_statuses[key] == current_statuses[key]:
                continue
            row = next(g for g in geometry if tuple(g["key"]) == key)
            child_values = [exact.get(tuple(child), 0) for child in row["children"]]
            child_counts = dict(Counter({0: "UNKNOWN", 1: "WIN", 2: "LOSS"}[v] for v in child_values))
            changes.append({"key": list(key), "before": baseline_statuses[key], "after": current_statuses[key],
                            "coverage": sorted(row["coverage"]), "s5_children": len(child_values),
                            "boundary": child_counts})
        baseline_counts = dict(sorted(Counter(baseline_statuses.values()).items()))
        added = {key: verdict for key, verdict in exact.items() if key not in baseline_exact}
        if not added or any(verdict not in (1, 2) for verdict in added.values()):
            raise SystemExit(f"comparison cache has no positive exact delta: {added}")
        geometry_by_key = {tuple(row["key"]): row for row in geometry}
        for change in changes:
            key = tuple(change["key"])
            row = geometry_by_key[key]
            decisive_verdicts = {verdict for child, verdict in added.items() if child in {tuple(c) for c in row["children"]}}
            if change["before"] != "UNKNOWN" or change["after"] not in ({"WIN"} if 1 in decisive_verdicts else {"LOSS"}):
                raise SystemExit(f"unexpected fixed-player S4 propagation from added S5 evidence: {change}, delta={decisive_verdicts}")

    covering = [c for c in candidates if set(remaining).issubset(c["coverage"])]
    if not covering:
        raise SystemExit("no unresolved class covers every remaining third move")
    covering.sort(key=lambda c: (c["unknown_s5_children"], -c["known_s5_losses"], tuple(c["key"])))
    witness = covering[0]
    # Lower bound 1 follows from a nonempty uncovered set; witness covers both,
    # so the integer minimum and a feasible dual value are both exactly 1.
    if len(remaining) != 2:
        raise SystemExit(f"the explicit one-class / one-vertex dual check needs review: {remaining}")

    result = {
        "schema": "n11-reply27-fixed-player-frontier-reclassification-v1",
        "baseline_main_commit": "154f3b7a67b97e13acbaee8b04dc74ddca728d19",
        "geometry": {"path": GEOMETRY.relative_to(ROOT).as_posix(), "sha256": sha(GEOMETRY),
                     "classes": len(geometry), "base_independent_audit_path": BASE_AUDIT.relative_to(ROOT).as_posix(),
                     "base_independent_audit_sha256": sha(BASE_AUDIT)},
        "s5_cache": {"path": cache_path.relative_to(ROOT).as_posix(), "sha256": sha(cache_path),
                     "exact_rows": len(exact), "verdict_counts": dict(Counter(exact.values()))},
        "fixed_player_aggregation": {"S4": "OR: any S5 WIN => WIN; all S5 LOSS => LOSS; otherwise UNKNOWN"},
        "s4_class_counts": dict(sorted(counts.items())),
        "baseline_s4_class_counts_for_comparison": baseline_counts,
        "s4_classes_changed_by_new_s5_win": changes,
        "secured_third_moves": len(secured), "remaining_third_moves": remaining,
        "integer_minimum_additional_classes": 1,
        "rational_lp_dual": {"value": "1", "weights": {str(remaining[0]): "1"},
                             "feasibility": "each class covers a vertex at most once"},
        "target_s4": selected,
        "best_unresolved_class_covering_all_remaining": witness,
        "top_unresolved_cover_candidates": covering[:10],
    }
    result["s4_classes_changed_by_compared_evidence"] = result.pop("s4_classes_changed_by_new_s5_win")
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"s4_class_counts": result["s4_class_counts"],
                      "secured": result["secured_third_moves"], "remaining": remaining,
                      "integer_minimum": 1, "lp_dual": "1", "target": selected,
                      "next_class": witness, "out_sha256": sha(out_path)}, sort_keys=True))


if __name__ == "__main__":
    main()

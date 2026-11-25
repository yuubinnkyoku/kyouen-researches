#!/usr/bin/env python3
"""Validate and summarize the 81be8247 dual-tight adaptive probe checkpoint."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
REPORT = OUT / "post-81be8247-reply27-checkpoint-report.json"
PREFIX = "post-81be8247-next-class-10448351135499681792-0"
PROBE = PREFIX + "-adaptive-win-probe8"
BASE_MAIN = "81be8247e8809fcdbf6aa730adb5d50b2583e9ba"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def record(path: Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"checkpoint artifact missing: {path}")
    return {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def load(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def cache_counts(path: Path) -> tuple[dict[tuple[int, int], int], Counter]:
    rows: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise SystemExit(f"invalid exact S5 cache row {line_no}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if verdict not in (1, 2) or (key in rows and rows[key] != verdict):
                raise SystemExit(f"invalid or conflicting exact S5 row at {key}")
            rows[key] = verdict
    return rows, Counter(rows.values())


def main() -> int:
    if REPORT.exists():
        raise SystemExit(f"refusing to overwrite report: {REPORT}")

    cache_path = OUT / f"{PROBE}-merged-s5.cache"
    cache, hist = cache_counts(cache_path)
    run = load(f"{PROBE}-summary.json")
    runner = load(f"{PROBE}-runner-summary.json")
    merge = load(f"{PROBE}-merge-receipt.json")
    win = load(f"{PROBE}-s4-win-geometry-audit.json")
    boundary_doc = load(f"{PROBE}-postprobe-boundary-audit.json")
    boundary = boundary_doc["boundary"]
    history = load(f"{PREFIX}-raw-history-current.json")
    saved_s6 = load(f"{PREFIX}-saved-s6-summary.json")
    preflight = load(f"{PREFIX}-probe8-strict-preflight.json")
    probe_s6 = load(f"{PREFIX}-probe8-saved-s6-summary.json")
    cardinality = load("post-81be8247-reply27-cardinality-after-probe8-win.json")
    repair = load("post-81be8247-selected31-repair-after-probe8-win.json")
    ranking = load("post-81be8247-dual-tight-ranking-after-probe8-win.json")

    key = [10448351135499681792, 0]
    expected_boundary = {"LOSS": 14, "UNKNOWN": 91, "WIN": 1}
    if (len(cache), hist[1], hist[2]) != (5269, 132, 5137):
        raise SystemExit(f"unexpected exact S5 cache: {len(cache)} {hist}")
    witnesses = win.get("s5_win_witnesses", [])
    if (win.get("s4_class", {}).get("key") != key
            or win.get("s4_class", {}).get("status") != "WIN"
            or len(witnesses) != 1
            or not witnesses[0].get("legal_s4_parent_incidence")
            or not witnesses[0].get("safe_canonical")):
        raise SystemExit("exact S5 WIN witness failed the geometry audit")
    if (boundary.get("canonical_children") != 106
            or boundary.get("status") != "WIN"
            or boundary.get("status_counts") != expected_boundary):
        raise SystemExit("complete 106-child class boundary disagrees with cache")
    if (run.get("class_status_from_exact_witness") != "WIN"
            or run.get("dispatched_targets") != 5
            or run.get("completed_targets") != 5
            or run.get("exact_replay_counts") != {"LOSS": 3, "UNKNOWN": 1, "WIN": 1}
            or run.get("nodes_all_completed_rows") != 44310512
            or run.get("nodes_exact") != 29310512
            or len(run.get("not_dispatched_after_win", [])) != 3):
        raise SystemExit("adaptive probe summary has unexpected results or dispatch")
    if (runner.get("class_status") != "WIN"
            or runner.get("new_exact") != 4
            or runner.get("new_loss") != 3
            or runner.get("new_win") != 1
            or runner.get("nodes_total") != 44310512):
        raise SystemExit("runner summary disagrees with exact probe output")
    if (merge.get("conflicts") != 0
            or merge.get("duplicate_verdicts") != 0
            or merge.get("base_cache", {}).get("rows") != 5265
            or merge.get("delta_cache", {}).get("rows") != 4
            or merge.get("merged_cache", {}).get("rows") != 5269):
        raise SystemExit("exact-cache merge receipt has a conflict or wrong size")

    full_keys = history.get("targets", {}).get("keys", [])
    same_budget = history.get("prior_unknown_same_budget_or_higher", [])
    if (len(full_keys) != 95 or history.get("csv_files_examined") != 7719
            or len(history.get("prior_exact", {})) != 0
            or len(history.get("dispatch_ready_keys", [])) != 94
            or len(same_budget) != 2 or history.get("exact_verdict_conflicts")):
        raise SystemExit("full-class raw-history audit changed or has conflicts")
    strict_s6 = preflight.get("saved_s6", {})
    if (preflight.get("target_count") != 8
            or len(preflight.get("ready_keys", [])) != 8
            or preflight.get("blocked_same_or_higher_budget_unknown_keys")
            or preflight.get("raw_history", {}).get("conflicts") != 0
            or strict_s6.get("parents") != 8
            or strict_s6.get("unknown_parents") != 8
            or strict_s6.get("new_exact") != 0
            or strict_s6.get("conflicts") != 0):
        raise SystemExit("strict probe preflight no longer confirms 8 ready targets")
    full_s6_counts = Counter(p.get("outcome") for p in saved_s6["targets"]["parents"])
    probe_s6_counts = Counter(p.get("outcome") for p in probe_s6["targets"]["parents"])
    if (saved_s6["targets"].get("parent_count") != 95
            or full_s6_counts != Counter({"UNKNOWN": 95})
            or probe_s6["targets"].get("parent_count") != 8
            or probe_s6_counts != Counter({"UNKNOWN": 8})):
        raise SystemExit("saved-S6 intersection did not leave the target parents UNKNOWN")

    expected_classes = {"LOSS": 29, "UNKNOWN": 3116, "WIN": 239}
    if (cardinality.get("cache_entries") != 5269
            or cardinality.get("class_status_counts") != expected_classes
            or cardinality.get("secured_vertices") != 113
            or cardinality.get("uncovered_vertices") != 6
            or cardinality.get("minimum_additional_classes") != 3
            or cardinality.get("rational_dual_total") != "3"
            or not cardinality.get("dual_certificate_matches_integer_optimum")):
        raise SystemExit("all-class status or cover/dual result is inconsistent")
    additive = repair["additive_optimum"]
    if (repair.get("minimum_additional_classes") != 3
            or additive.get("repair_classes") != 3
            or additive.get("unique_unknown_s5") != 291
            or additive.get("mip_gap") != 0.0):
        raise SystemExit("reoptimized three-class repair is inconsistent")
    target = ranking.get("next_target", {})
    if (ranking.get("minimum_additional_classes") != 3
            or not ranking.get("dual_certificate_matches_integer_optimum")
            or target.get("key") != [10448351135499550721, 0]
            or target.get("unknown_s5") != 95
            or target.get("canonical_s5_children") != 105):
        raise SystemExit("current dual-tight ranking is inconsistent")

    # Capture the checkpoint's complete output set and all scripts/evidence sources.
    artifacts = [record(path) for path in sorted(OUT.glob("post-81be8247-*"))
                 if path.is_file() and path != REPORT]
    for directory in sorted(OUT.glob("post-81be8247-*")):
        if directory.is_dir():
            artifacts.extend(record(path) for path in sorted(directory.rglob("*")) if path.is_file())
    used_sources = [
        Path(__file__).resolve(),
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/collect_dual_tight_adaptive_win_probe.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_s4_win.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/adapt_repair_json_for_dual_tight_ranking.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_class_local.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py",
        ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/n11_integer_circle_geometry.py",
        ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
        ROOT / ".local/n11/reply27-probe9/dfpn.exe",
    ]

    report = {
        "schema": "n11-reply27-finite-checkpoint-v1",
        "checkpoint_base_main": BASE_MAIN,
        "claim": "Exact s5 solver verdicts and a geometry-verified legal WIN witness classify the complete s4 boundary; UNKNOWN is preserved.",
        "exact_s5_cache": {
            "entries": len(cache), "WIN": hist[1], "LOSS": hist[2], "conflict": 0,
            "path": rel(cache_path), "sha256": sha(cache_path),
        },
        "processed_class": {
            "key": key, "status": "WIN", "canonical_s5_children": 106,
            "counts": expected_boundary,
            "exact_s5_win_witnesses": [item["key"] for item in witnesses],
            "unresolved_s5_children_left_unknown": 91,
            "scheduled_targets_not_dispatched_after_win": run["not_dispatched_after_win"],
            "coverage_vertices": win["s4_class"]["coverage_vertices"],
            "other_reachable_s4_classes_won_by_witness": [
                item["key"] for item in win.get("reply27_parent_class_impacts_from_witness", [])
                if item.get("reachable_from_reply27") and item.get("status_before_probe") == "UNKNOWN"
            ],
        },
        "probe": {
            "schedule_size": run["scheduled_targets"], "dispatched": run["dispatched_targets"],
            "rows": run["exact_replay_counts"], "nodes_all_rows": run["nodes_all_completed_rows"],
            "nodes_exact_rows": run["nodes_exact"], "budget_per_target": run["budget_per_target"],
            "stop_reason": run["stop_reason"],
        },
        "preflight": {
            "full_class_s5_unknown": len(full_keys),
            "full_target_raw_csv_sources_scanned": history["csv_files_examined"],
            "full_target_exact_prior_rows": len(history.get("prior_exact", {})),
            "same_budget_or_higher_unknown_observations": len(same_budget),
            "dispatch_ready_before_probe": len(history["dispatch_ready_keys"]),
            "probe8_ready": len(preflight["ready_keys"]),
            "saved_s6_full_parent_count": saved_s6["targets"]["parent_count"],
            "saved_s6_full_outcomes": dict(sorted(full_s6_counts.items())),
            "saved_s6_probe8_outcomes": dict(sorted(probe_s6_counts.items())),
            "conflicts": 0,
        },
        "s6_descent": {"new_s6_solver_rows": 0, "reverse_propagated_s5_loss": 0,
                       "unknown_s6_propagated": False},
        "s4": cardinality["class_status_counts"],
        "secured_third_moves": cardinality["secured_vertices"],
        "remaining_third_moves": cardinality["uncovered_vertices"],
        "minimum_additional_classes": cardinality["minimum_additional_classes"],
        "rational_dual": cardinality["rational_dual_total"],
        "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
        "repair": {
            "classes": additive["repair_classes"],
            "additive_unknown_s5": additive["additive_unknown_s5"],
            "distinct_unknown_s5": additive["unique_unknown_s5"],
            "selected": additive["selected"],
        },
        "next_target": {
            "key": target["key"], "unknown_s5": target["unknown_s5"],
            "canonical_s5_children": target["canonical_s5_children"],
            "known_loss_s5": target["known_loss_s5"], "coverage": target["coverage"],
            "dual_vertex": target["dual_vertex"],
            "preflight": "pending; ranking is scheduling only",
        },
        "proof_status": {"reply27_60_27": "UNKNOWN", "empty_11x11": "UNKNOWN"},
        "bound_artifacts": artifacts,
        "bound_sources": [record(path) for path in used_sources],
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")
    print(json.dumps({
        "report": rel(REPORT), "sha256": sha(REPORT), "exact_s5_cache": report["exact_s5_cache"],
        "processed_class": report["processed_class"], "s4": report["s4"],
        "secured": report["secured_third_moves"],
        "minimum_additional_classes": report["minimum_additional_classes"],
        "repair_distinct_unknown_s5": report["repair"]["distinct_unknown_s5"],
        "next_target": report["next_target"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

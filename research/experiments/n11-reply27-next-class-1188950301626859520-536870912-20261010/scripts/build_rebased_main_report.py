"""Summarize the 10/10 continuation after importing the latest main cache."""
from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
S4 = [1188950301626859520, 536870912]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def artifact(path: Path) -> dict:
    return {"path": rel(path), "sha256": sha(path)}


def main() -> None:
    main_checkpoint = "f3c0c8ec265e034a3e69c03e6eee6d5d9a4a8e43"
    ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", main_checkpoint, "HEAD"], cwd=ROOT)
    if ancestry.returncode != 0:
        raise SystemExit("main checkpoint f3c0c8ec is not an ancestor of HEAD")
    continuation_path = OUT / "report-continuation.json"
    continuation = json.loads(continuation_path.read_text(encoding="utf-8"))
    rebase_path = OUT / "latest-main-cache-rebase.json"
    rebase = json.loads(rebase_path.read_text(encoding="utf-8"))
    cache_path = OUT / "current-exact-s5-after-probe-9-rebased-main.cache"
    frontier_path = OUT / "frontier-after-main-rebase.json"
    frontier = json.loads(frontier_path.read_text(encoding="utf-8"))
    raw_path = OUT / "raw-history-after-main-rebase.json"
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    layer_path = OUT / "saved-layer-after-main-rebase.json"
    layer = json.loads(layer_path.read_text(encoding="utf-8"))
    next_plan_path = OUT / "probe-11-plan.json"
    next_plan = json.loads(next_plan_path.read_text(encoding="utf-8"))
    upstream_audit_path = ROOT / "research/experiments/n11-two-target-design-20261010/output/probe-audit.json"
    upstream_audit = json.loads(upstream_audit_path.read_text(encoding="utf-8"))

    exact = {}
    for line_no, line in enumerate(cache_path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        f = line.split(",")
        if len(f) != 6 or f[0] != "s5verdict" or int(f[3]) != 5:
            raise SystemExit(f"malformed rebased S5 cache row {line_no}")
        key, verdict = (int(f[1]), int(f[2])), int(f[4])
        if verdict not in (1, 2) or key in exact and exact[key] != verdict:
            raise SystemExit(f"conflicting rebased cache row {line_no}")
        exact[key] = verdict
    if len(exact) != 5749 or Counter(exact.values()) != Counter({1: 158, 2: 5591}):
        raise SystemExit("unexpected latest-main rebased cache")
    if rebase["rebased_cache"]["sha256"] != sha(cache_path) or rebase["conflicts"] != 0:
        raise SystemExit("cache rebase receipt mismatch")

    target = frontier["best_unresolved_class_covering_all_remaining"]
    if (target["key"] != S4 or target["boundary"] != {"LOSS": 22, "UNKNOWN": 87}
            or target["verdict"] != "UNKNOWN"):
        raise SystemExit("unexpected latest-main S4 boundary")
    if (frontier["s4_class_counts"] != {"LOSS": 31, "WIN": 272, "UNKNOWN": 3081}
            or frontier["secured_third_moves"] != 117 or frontier["remaining_third_moves"] != [100, 108]
            or frontier["integer_minimum_additional_classes"] != 1
            or frontier["rational_lp_dual"]["value"] != "1"):
        raise SystemExit("unexpected latest-main global frontier")
    if (raw["targets"]["count"] != 109 or raw["csv_files_examined"] != 11960
            or len(raw["exact_verdict_conflicts"]) != 0
            or len(raw["dispatch_ready_keys"]) != 86
            or len(raw["prior_unknown_same_budget_or_higher"]) != 1
            or raw["current_cache"]["target_exact_intersection"] != 22):
        raise SystemExit("unexpected latest-main raw-history audit")
    if (layer["s6_boundary"]["distinct_canonical_keys"] != 5249
            or len(layer["raw_s6"]["exact_keys"]) != 13
            or len(layer["saved_cache_s6"]["exact_keys"]) != 14
            or layer["saved_cache_s7"]["target_intersections"]
            or layer["s5_results_from_raw_s6_s7_only"]
            or layer["s5_results_with_saved_cache_s6_s7"]):
        raise SystemExit("unexpected latest-main saved-layer audit")
    if (upstream_audit["new_raw_exact"] != 2 or upstream_audit["new_loss_s4_classes"] != 0
            or upstream_audit["new_win_s4_classes"] != 0
            or upstream_audit["merged_cache_sha256"] != rebase["base_cache"]["sha256"]):
        raise SystemExit("latest-main shared-probe audit is inconsistent")
    next_key = tuple(next_plan["s5_target"]["key"])
    if (next_key in exact or next_plan["s5_target"]["legal_count"] != 94
            or next_plan["prior_observations"]):
        raise SystemExit("latest next candidate is not a raw-history-clean legal-94 UNKNOWN")

    out_path = OUT / "report-after-main-rebase.json"
    report = {
        "schema": "n11-reply27-next-class-latest-main-report-v1",
        "main_commit_at_rebase": main_checkpoint,
        "old_main_checkpoint_report": artifact(continuation_path),
        "latest_main_probe_audit": artifact(upstream_audit_path),
        "cache_rebase": artifact(rebase_path),
        "cumulative_experiment": {
            "distinct_s5_positions": 12,
            "solver_runs": 24,
            "direct_s5_loss": 11,
            "unknown_at_15m": 1,
            "total_nodes": 88_242_475,
            "exact_verdict_nodes": 49_242_475,
            "details": "Includes the three direct LOSS in the prior checkpoint, six local continuation LOSS, two LOSS imported from f3c0c8ec, and the 15M UNKNOWN retained only in raw evidence.",
        },
        "latest_main_solver": {
            "local_binary_sha256": continuation["solver"]["sha256"],
            "shared_probe_binary_sha256": upstream_audit["solver_binary_sha256_from_probe_host"],
            "source_cpp_sha256": upstream_audit["source_cpp_sha256"],
        },
        "final_exact_s5_cache": {
            **artifact(cache_path), "rows": len(exact),
            "verdict_counts": {"WIN": 158, "LOSS": 5591},
            "active_quarantined_keys": 0,
        },
        "target_s4": {
            "key": S4, "children": 109, "coverage": target["coverage"],
            "boundary": target["boundary"], "status": "UNKNOWN", "unresolved_s5_children": 87,
        },
        "frontier": {
            **artifact(frontier_path), "s4_class_counts": frontier["s4_class_counts"],
            "secured_third_moves": frontier["secured_third_moves"], "total_third_moves": 119,
            "remaining_third_moves": frontier["remaining_third_moves"],
            "integer_minimum_additional_classes": frontier["integer_minimum_additional_classes"],
            "rational_lp_dual": frontier["rational_lp_dual"],
        },
        "post_probe_raw_history": {
            **artifact(raw_path), "csv_files_examined": raw["csv_files_examined"],
            "target_children": raw["targets"]["count"],
            "cache_exact_intersections": raw["current_cache"]["target_exact_intersection"],
            "prior_exact_keys": len(raw["prior_exact"]),
            "prior_exact_observation_rows": sum(raw["prior_exact"].values()),
            "same_budget_unknown_keys": len(raw["prior_unknown_same_budget_or_higher"]),
            "lower_budget_unknown_keys": len(raw["prior_unknown_below_budget"]),
            "dispatch_ready_unknown_children": len(raw["dispatch_ready_keys"]),
            "conflicts": len(raw["exact_verdict_conflicts"]),
        },
        "saved_layers": {
            **artifact(layer_path),
            "s6_boundary_keys": layer["s6_boundary"]["distinct_canonical_keys"],
            "raw_s6_exact": len(layer["raw_s6"]["exact_keys"]),
            "cache_s6_exact": len(layer["saved_cache_s6"]["exact_keys"]),
            "raw_s7_exact": len(layer["raw_s7"]["exact_keys"]),
            "s7_cache_intersections": len(layer["saved_cache_s7"]["target_intersections"]),
            "derived_s5_verdicts": 0,
        },
        "next_candidate": {
            "s4_key": S4, "s5_key": list(next_key),
            "legal_count": next_plan["s5_target"]["legal_count"],
            "raw_history_ready": True, "prior_observations": next_plan["prior_observations"],
            "saved_layer_verdict": None, "plan": artifact(next_plan_path),
        },
        "evidence_limit": (
            "All newly merged exact S5 LOSS rows are raw solver-traceable and independently "
            "checked for canonicality, safety, legal count, and S4/S5 incidence. Their solver "
            "verdicts are not terminal-only independent minimax certificates. The cache and "
            "global frontier still include earlier cache-only evidence; this is not a complete "
            "independent minimax proof DAG."
        ),
    }
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"path": rel(out_path), "sha256": sha(out_path),
                      "target_boundary": target["boundary"], "cache_rows": len(exact),
                      "next_candidate": list(next_key)}, sort_keys=True))


if __name__ == "__main__":
    main()

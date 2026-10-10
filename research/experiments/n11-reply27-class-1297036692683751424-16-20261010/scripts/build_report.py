"""Build a hash-bound summary of the 2026-10-10 reply27 probes."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
SUMMARY_PATHS = [
    "output/s5-probe2m/summary.json",
    "output/s5-probe15m-first/summary.json",
    "output/candidate-s5-probe2m/summary.json",
    "output/candidate-s5-probe15m/summary.json",
    "output/candidate-s5-probe15m-second/summary.json",
    "output/candidate-s5-probe15m-third/summary.json",
    "output/followup-s5-probe2m/summary.json",
    "output/followup-s5-probe15m/summary.json",
]


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def json_receipt(path: Path) -> dict:
    return {"path": rel(path), "sha256": sha(path)}


def main() -> None:
    probe_summaries = []
    runs = []
    for relative in SUMMARY_PATHS:
        path = EXP / relative
        data = json.loads(path.read_text(encoding="utf-8"))
        probe_summaries.append({**json_receipt(path), "total_nodes": data["total_nodes"],
                                "verdict_counts": data["verdict_counts"],
                                "history_sha256": data["history_sha256"]})
        for row in data["results"]:
            runs.append({
                "arm": row["arm"], "s5_key": row["key"], "budget": row["budget"],
                "history_sha256": data["history_sha256"],
                "legal_moves": row["legal"], "verdict": {0: "UNKNOWN", 1: "WIN", 2: "LOSS"}[row["verdict"]],
                "nodes": row["nodes"], "wall_seconds": row["wall_seconds"],
                "input": {"path": row["input"], "sha256": row["input_sha256"]},
                "raw": {"path": row["raw"], "sha256": row["raw_sha256"]},
                "log": {"path": row["log"], "sha256": row["log_sha256"]},
                "exit_code": row["exit_code"],
            })
    if len(runs) != 14:
        raise SystemExit(f"expected 14 exact replay attempts, found {len(runs)}")
    verdict_counts = Counter(row["verdict"] for row in runs)
    budget_counts = Counter(row["budget"] for row in runs)
    if verdict_counts != Counter({"UNKNOWN": 10, "WIN": 2, "LOSS": 2}):
        raise SystemExit(f"unexpected probe verdict counts: {verdict_counts}")
    if budget_counts != Counter({2_000_000: 9, 15_000_000: 5}):
        raise SystemExit(f"unexpected probe budgets: {budget_counts}")

    history_manifest_path = EXP / "output/probe-history-snapshots.json"
    history_manifest = json.loads(history_manifest_path.read_text(encoding="utf-8"))
    preserved_history_hashes = {item["copy"]["sha256"] for item in history_manifest["snapshots"]}
    run_history_hashes = {row["history_sha256"] for row in runs}
    if run_history_hashes != preserved_history_hashes:
        raise SystemExit(f"probe history snapshots do not cover the run receipts: {run_history_hashes}")

    exact_runs = [row for row in runs if row["verdict"] != "UNKNOWN"]
    total_nodes = sum(row["nodes"] for row in runs)
    exact_nodes = sum(row["nodes"] for row in exact_runs)
    if (total_nodes, exact_nodes) != (67_339_676, 34_339_676):
        raise SystemExit(f"unexpected node totals: all={total_nodes}, exact={exact_nodes}")

    cache_path = EXP / "output/current-exact-s5-after-followup-loss.cache"
    cache_counts = Counter()
    cache_rows = 0
    for line in cache_path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split(",")
        if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
            raise SystemExit(f"malformed final cache row: {line}")
        cache_rows += 1
        cache_counts[int(fields[4])] += 1
    if (cache_rows, cache_counts) != (5738, Counter({1: 158, 2: 5580})):
        raise SystemExit(f"unexpected final cache: {cache_rows} rows {cache_counts}")

    reclass_path = EXP / "output/frontier-reclassification-after-followup-loss.json"
    reclass = json.loads(reclass_path.read_text(encoding="utf-8"))
    baseline_reclass_path = EXP / "output/frontier-reclassification-from-start-final.json"
    baseline_reclass = json.loads(baseline_reclass_path.read_text(encoding="utf-8"))
    followup_preflight_path = EXP / "output/followup-after-loss-preflight.json"
    followup_raw_path = EXP / "output/followup-after-loss-raw-history-audit.json"
    followup_layer_path = EXP / "output/followup-after-loss-saved-layer-preflight.json"
    followup_preflight = json.loads(followup_preflight_path.read_text(encoding="utf-8"))
    followup_raw = json.loads(followup_raw_path.read_text(encoding="utf-8"))
    followup_layer = json.loads(followup_layer_path.read_text(encoding="utf-8"))
    target_raw_path = EXP / "output/raw-s5-history-final-target-after-followup.json"
    target_layer_path = EXP / "output/saved-layer-final-target-after-followup.json"
    target_raw = json.loads(target_raw_path.read_text(encoding="utf-8"))
    target_layer = json.loads(target_layer_path.read_text(encoding="utf-8"))

    next_child = followup_preflight["lowest_legal_unknown_s5"][0]
    next_key = tuple(next_child["key"])
    next_token = f"{next_key[0]},{next_key[1]}"
    if next_key not in {tuple(k) for k in followup_raw["dispatch_ready_keys"]}:
        raise SystemExit(f"next suggested S5 key is not dispatch-ready: {next_key}")
    if next_token in followup_layer["s5_results_from_raw_s6_s7_only"] \
            or next_token in followup_layer["s5_results_with_saved_cache_s6_s7"]:
        raise SystemExit(f"saved S6/S7 evidence resolves proposed S5 key: {next_key}")

    exact_result_details = []
    for row in sorted(exact_runs, key=lambda item: (item["s5_key"], item["budget"])):
        exact_result_details.append({
            "key": row["s5_key"], "verdict": row["verdict"], "legal_moves": row["legal_moves"],
            "budget": row["budget"], "nodes": row["nodes"], "raw": row["raw"],
            "solver": {"path": ".local/n11-independent-audit-solver.exe",
                       "sha256": "ac8f4931e4c81bd06ba1622844933962134f663d970885c2990fbb96a167677a",
                       "source_path": "cpp/solvers/kyouen_dfpn_root.cpp",
                       "source_sha256": "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"},
            "geometry_check": "independent Board: canonical, safe and legal S4-to-S5 child",
            "evidence_class": "direct positive-budget raw solver outcome; solver-trusted",
        })

    report = {
        "schema": "n11-reply27-class-probe-report-v1",
        "created_local_date": "2026-10-10",
        "starting_main_commit": "154f3b7a67b97e13acbaee8b04dc74ddca728d19",
        "latest_main_before_result_commit": "a89eecba5870f8e1743fab2b98f7fbb550bdc490",
        "intervening_main_update": "Four unrelated commits were fast-forwarded after the probes; none changed reply27 solver, frontier, or K0355 files.",
        "starting_state": {"s4_classes": {"LOSS": 31, "WIN": 268, "UNKNOWN": 3085},
                           "s5_cache_rows": 5734, "secured_third_moves": 117,
                           "remaining_third_moves": [100, 108],
                           "integer_minimum_additional_classes": 1, "rational_lp_dual": "1"},
        "solver": {"binary": ".local/n11-independent-audit-solver.exe",
                   "binary_sha256": "ac8f4931e4c81bd06ba1622844933962134f663d970885c2990fbb96a167677a",
                   "source": "cpp/solvers/kyouen_dfpn_root.cpp",
                   "source_sha256": "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e",
                   "options": ["--n=11", "--memo=22", "--exact-order=count"],
                   "workers": 1, "wall_watchdog_seconds": 180},
        "probe_history_snapshots": {**json_receipt(history_manifest_path),
                                     "snapshots": history_manifest["snapshots"],
                                     "workspace_history_file_preserved": True},
        "probe_execution": {"runs": len(runs), "unique_s5_positions": len({tuple(row["s5_key"]) for row in runs}),
                            "runs_by_budget": {str(k): v for k, v in sorted(budget_counts.items())},
                            "verdict_counts": dict(sorted(verdict_counts.items())),
                            "total_nodes": total_nodes, "exact_outcome_nodes": exact_nodes,
                            "unknown_runs_remain_unknown": True,
                            "summary_receipts": probe_summaries, "runs_detail": runs},
        "new_direct_exact_s5": exact_result_details,
        "original_target_s4": {"key": [1297036692683751424, 16], "status": "WIN",
                                "boundary": {"LOSS": 9, "WIN": 1, "UNKNOWN": 98},
                                "witness_s5_key": [1297036692683751424, 67108880],
                                "coverage": [26, 28, 100, 108],
                                "geometry_key_set_sha256": "633595fe66774ed7b4d9573e4951c0dfc038ba469d2d6778d8ba61d03d67dfa1"},
        "explored_followup_class": {"key": [1188950301626859520, 536870912],
                                    "coverage": [55, 65, 100, 108], "status": "UNKNOWN",
                                    "boundary": {"LOSS": 11, "WIN": 0, "UNKNOWN": 98},
                                    "tested_s5_key": [1188950301626859552, 536870912],
                                    "tested_s5_legal_moves": 87,
                                    "next_lowest_legal_dispatch_ready_s5": next_child,
                                    "ready_unknown_s5_children": len(followup_raw["dispatch_ready_keys"])},
        "final_s5_cache": {"path": rel(cache_path), "sha256": sha(cache_path),
                            "exact_rows": cache_rows,
                            "verdict_counts": {"WIN": cache_counts[1], "LOSS": cache_counts[2]},
                            "merge_receipt": json_receipt(EXP / "output/followup-s5-cache-merge.json")},
        "final_frontier": {"s4_class_counts": reclass["s4_class_counts"],
                            "classes_transitioned_unknown_to_win_from_start": baseline_reclass["s4_classes_changed_by_compared_evidence"],
                            "classes_changed_by_latest_followup_loss": reclass["s4_classes_changed_by_compared_evidence"],
                            "secured_third_moves": reclass["secured_third_moves"],
                            "remaining_third_moves": reclass["remaining_third_moves"],
                            "integer_minimum_additional_classes": reclass["integer_minimum_additional_classes"],
                            "rational_lp_dual": reclass["rational_lp_dual"],
                            "reclassification": json_receipt(reclass_path),
                            "reclassification_from_start": json_receipt(baseline_reclass_path)},
        "final_target_s4_raw_history": {"files_examined": target_raw["csv_files_examined"],
                                         "exact_conflicts": len(target_raw["exact_verdict_conflicts"]),
                                         "same_or_higher_budget_unknown": len(target_raw["prior_unknown_same_budget_or_higher"]),
                                         "distinct_raw_exact_s5": len(target_raw["prior_exact"]),
                                         "saved_layer": json_receipt(target_layer_path),
                                         "s6_boundary_keys": target_layer["s6_boundary"]["distinct_canonical_keys"],
                                         "s6_raw_exact": len(target_layer["raw_s6"]["exact_keys"]),
                                         "s6_cache_exact": len(target_layer["saved_cache_s6"]["exact_keys"]),
                                         "s7_raw_exact": len(target_layer["raw_s7"]["exact_keys"]),
                                         "s7_cache_intersections": len(target_layer["saved_cache_s7"]["target_intersections"]),
                                         "s5_results_from_s6_s7": len(target_layer["s5_results_from_raw_s6_s7_only"])
                                         + len(target_layer["s5_results_with_saved_cache_s6_s7"])},
        "final_followup_raw_history": {"files_examined": followup_raw["csv_files_examined"],
                                       "cache_hits": followup_raw["current_cache"]["target_exact_intersection"],
                                       "exact_conflicts": len(followup_raw["exact_verdict_conflicts"]),
                                       "same_or_higher_budget_unknown": len(followup_raw["prior_unknown_same_budget_or_higher"]),
                                       "distinct_raw_exact_s5": len(followup_raw["prior_exact"]),
                                       "dispatch_ready_s5": len(followup_raw["dispatch_ready_keys"]),
                                       "saved_layer": json_receipt(followup_layer_path),
                                       "s6_boundary_keys": followup_layer["s6_boundary"]["distinct_canonical_keys"],
                                       "s6_raw_exact": len(followup_layer["raw_s6"]["exact_keys"]),
                                       "s6_cache_exact": len(followup_layer["saved_cache_s6"]["exact_keys"]),
                                       "s7_raw_exact": len(followup_layer["raw_s7"]["exact_keys"]),
                                       "s7_cache_intersections": len(followup_layer["saved_cache_s7"]["target_intersections"]),
                                       "s5_results_from_s6_s7": len(followup_layer["s5_results_from_raw_s6_s7_only"])
                                       + len(followup_layer["s5_results_with_saved_cache_s6_s7"])},
        "independent_checking": {
            "target_win_geometry_and_minimax": json_receipt(EXP / "output/independent-win-check.json"),
            "followup_win_geometry_and_minimax": json_receipt(EXP / "output/candidate-s5-win-independent-check.json"),
            "minimax_limit": "For both S5 WIN witnesses, terminal-only independent minimax stopped at 30,000 states with UNKNOWN; it did not produce a certificate or contradict the raw solver.",
        },
        "evidence_limit": "Frontier status is computed from canonical exact cache plus direct raw outcomes. The base cache includes cache-only leaves. The two S5 WIN witnesses are direct positive-budget raw solver outcomes and geometry-checked, but no independent complete minimax proof DAG to terminal states was produced. Do not describe the {60,27} root or 11x11 empty board as solved.",
        "next_action": {"s4_key": [1188950301626859520, 536870912],
                        "s5_key": next_child["key"], "legal_moves": next_child["legal_count"],
                        "preflight_status": "raw-history ready; no same/higher-budget UNKNOWN; no S6/S7-derived S5 result"},
    }
    out = EXP / "output/report.json"
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"report": rel(out), "sha256": sha(out), "runs": len(runs),
                      "nodes": total_nodes, "exact_nodes": exact_nodes,
                      "exact_s5": len(exact_runs), "cache_rows": cache_rows}, sort_keys=True))


if __name__ == "__main__":
    main()

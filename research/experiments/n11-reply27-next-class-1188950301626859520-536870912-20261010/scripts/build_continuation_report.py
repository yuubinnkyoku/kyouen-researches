"""Validate and summarize the continuation probes after the three-result checkpoint."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from s5_evidence_policy import quarantined_cache_keys  # noqa: E402

S4 = (1188950301626859520, 536870912)
TARGETS = {
    4: ((1152921504606851072, 537001986), 90, 4_519_790, "fourth"),
    5: ((1188950301626859520, 536870976), 90, 8_361_840, "fifth"),
    6: ((1188950301626859520, 603979776), 90, None, "sixth"),
    7: ((10412322338481635328, 536870912), 91, 2_569_967, "seventh"),
    8: ((1189091039115214848, 536870912), 92, 4_808_557, "eighth"),
    9: ((1765411053930283008, 536870912), 92, 4_785_007, "ninth"),
    10: ((1152921504606851072, 570425346), 93, 6_730_471, "tenth"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_one_replay(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = [row for row in csv.reader(stream) if row and row[0] == "replay"]
    if len(rows) != 1 or len(rows[0]) != 11:
        raise SystemExit(f"expected one 11-field replay row in {rel(path)}; found {len(rows)}")
    return rows[0]


def read_cache(path: Path) -> dict[tuple[int, int], int]:
    exact: dict[tuple[int, int], int] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split(",")
        if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
            raise SystemExit(f"malformed S5 cache row {rel(path)}:{line_no}")
        key, verdict = (int(fields[1]), int(fields[2])), int(fields[4])
        if verdict not in (1, 2) or key in exact and exact[key] != verdict:
            raise SystemExit(f"invalid/conflicting S5 cache row {rel(path)}:{line_no}")
        exact[key] = verdict
    return exact


def artifact(path: Path) -> dict:
    return {"path": rel(path), "sha256": sha(path)}


def main() -> None:
    start_report_path = OUT / "report.json"
    start_report = json.loads(start_report_path.read_text(encoding="utf-8"))
    start_cache_path = OUT / "current-exact-s5-after-probe-3.cache"
    final_cache_path = OUT / "current-exact-s5-after-probe-9.cache"
    start_cache, final_cache = read_cache(start_cache_path), read_cache(final_cache_path)
    quarantine = quarantined_cache_keys()
    if set(start_cache) & quarantine or set(final_cache) & quarantine:
        raise SystemExit("active quarantined key found in a continuation cache")
    if len(start_cache) != 5741 or Counter(start_cache.values()) != Counter({1: 158, 2: 5583}):
        raise SystemExit("unexpected base cache")
    if len(final_cache) != 5747 or Counter(final_cache.values()) != Counter({1: 158, 2: 5589}):
        raise SystemExit("unexpected final cache")

    board = Board(11)
    parent_mask = S4[0] | (S4[1] << 64)
    all_children = {((mask & ((1 << 64) - 1)), mask >> 64) for mask in board.children(parent_mask)}
    geometric = json.loads((OUT / "geometric-cache-preflight.json").read_text(encoding="utf-8"))
    geometric_children = {tuple(item["key"]) for item in geometric["s5_children"]}
    if len(all_children) != 109 or geometric_children != all_children:
        raise SystemExit("independent Board geometry differs from the stored complete S5 boundary")

    new_results = []
    exact_nodes = 0
    total_nodes = 0
    exact_losses = 0
    unknown_runs = 0
    for suffix, (key, legal, expected_high_nodes, word) in TARGETS.items():
        token = f"{key[0]},{key[1]}"
        low_path = OUT / f"probe-2m-{word}.csv"
        high_path = OUT / f"probe-15m-{word}.csv"
        low = read_one_replay(low_path)
        expected_low = (5, legal, 0, 2_000_000, 0, 2_000_000, *key)
        low_fields = tuple(map(int, (low[2], low[3], low[4], low[5], low[6], low[7], low[9], low[10])))
        if low_fields != expected_low:
            raise SystemExit(f"unexpected 2M result for target {suffix}: {low}")
        high = read_one_replay(high_path)
        high_values = tuple(map(int, (high[2], high[3], high[4], high[5], high[6], high[7], high[9], high[10])))
        expected_high = (5, legal, 0, 15_000_000, 2 if expected_high_nodes is not None else 0,
                         expected_high_nodes if expected_high_nodes is not None else 15_000_000, *key)
        if high_values != expected_high:
            raise SystemExit(f"unexpected 15M result for target {suffix}: {high}")
        mask = key[0] | (key[1] << 64)
        if board.canonical(mask) != mask or mask.bit_count() != 5 or mask not in board.children(parent_mask):
            raise SystemExit(f"target {suffix} is not a safe canonical S5 child")
        if board.legal(mask).bit_count() != legal:
            raise SystemExit(f"target {suffix} legal count differs from independent geometry")

        plan_path = OUT / f"probe-{suffix}-plan.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        if tuple(plan["s5_target"]["key"]) != key or plan["s5_target"]["legal_count"] != legal:
            raise SystemExit(f"probe plan mismatch for target {suffix}")
        merge_receipt_path = OUT / f"merge-receipt-{word}.json" if expected_high_nodes is not None else None
        if expected_high_nodes is not None:
            receipt = json.loads(merge_receipt_path.read_text(encoding="utf-8"))
            if receipt["merged_verdict"] != "LOSS" or tuple(receipt["merged_key"]) != key:
                raise SystemExit(f"merge receipt mismatch for target {suffix}")
            if final_cache.get(key) != 2:
                raise SystemExit(f"exact LOSS missing from final cache for target {suffix}")
            exact_losses += 1
            exact_nodes += expected_high_nodes
        else:
            if key in final_cache:
                raise SystemExit("15M UNKNOWN must not enter the exact cache")
            unknown_runs += 1
        total_nodes += int(low[7]) + int(high[7])
        entry = {
            "key": list(key), "legal_count": legal,
            "dispatch_plan": artifact(plan_path),
            "input": artifact(ROOT / plan["preflight_sources"][2]["path"]),
            "2m": {**artifact(low_path), "verdict": "UNKNOWN", "nodes": int(low[7])},
            "15m": {**artifact(high_path),
                    "verdict": "LOSS" if expected_high_nodes is not None else "UNKNOWN",
                    "nodes": int(high[7])},
        }
        escalation_path = OUT / f"escalation-plan-{word}.json"
        if escalation_path.exists():
            entry["escalation_plan"] = artifact(escalation_path)
        if merge_receipt_path is not None:
            entry["merge_receipt"] = artifact(merge_receipt_path)
        new_results.append(entry)

    if exact_losses != 6 or unknown_runs != 1 or exact_nodes != 31_775_632 or total_nodes != 60_775_632:
        raise SystemExit("unexpected continuation probe totals")

    frontier_path = OUT / "frontier-after-probe-9.json"
    frontier = json.loads(frontier_path.read_text(encoding="utf-8"))
    target = frontier["best_unresolved_class_covering_all_remaining"]
    if target["key"] != list(S4) or target["boundary"] != {"LOSS": 20, "UNKNOWN": 89}:
        raise SystemExit("unexpected final S4 boundary")
    if target["verdict"] != "UNKNOWN" or target["s5_children"] != 109:
        raise SystemExit("unexpected final S4 status or boundary size")
    if (frontier["s4_class_counts"] != {"LOSS": 31, "WIN": 272, "UNKNOWN": 3081}
            or frontier["secured_third_moves"] != 117 or frontier["remaining_third_moves"] != [100, 108]
            or frontier["integer_minimum_additional_classes"] != 1
            or frontier["rational_lp_dual"]["value"] != "1"):
        raise SystemExit("unexpected global frontier")

    raw_path = OUT / "raw-history-after-tenth.json"
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    layer_path = OUT / "saved-layer-after-tenth.json"
    layer = json.loads(layer_path.read_text(encoding="utf-8"))
    next_plan_path = OUT / "probe-11-plan.json"
    next_plan = json.loads(next_plan_path.read_text(encoding="utf-8"))
    next_key = tuple(next_plan["s5_target"]["key"])
    if (raw["targets"]["count"] != 109 or raw["exact_verdict_conflicts"]
            or len(raw["dispatch_ready_keys"]) != 88
            or len(raw["prior_unknown_same_budget_or_higher"]) != 1
            or raw["current_cache"]["target_exact_intersection"] != 20):
        raise SystemExit("unexpected full raw-history audit")
    if (layer["s6_boundary"]["distinct_canonical_keys"] != 5283
            or len(layer["raw_s6"]["exact_keys"]) != 13
            or len(layer["saved_cache_s6"]["exact_keys"]) != 14
            or layer["saved_cache_s7"]["target_intersections"]
            or layer["s5_results_from_raw_s6_s7_only"]
            or layer["s5_results_with_saved_cache_s6_s7"]):
        raise SystemExit("unexpected saved S6/S7 layer audit")
    if next_key in final_cache or next_plan["s5_target"]["legal_count"] != board.legal(next_key[0] | (next_key[1] << 64)).bit_count():
        raise SystemExit("next candidate is already exact or has an invalid legal count")

    start_nodes = start_report["probes"]["total_nodes"]
    start_exact_nodes = start_report["probes"]["exact_nodes"]
    report = {
        "schema": "n11-reply27-next-class-continuation-report-v1",
        "main_commit_at_start": "4a9ea150faca7f49a94b453eebfb87d2c22b57b7",
        "starting_checkpoint_report": artifact(start_report_path),
        "independent_geometry": {
            "implementation": "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py",
            "complete_s5_children": 109,
            "stored_boundary_matches_board_regeneration": True,
        },
        "probes_since_checkpoint": {
            "distinct_positions": len(new_results), "runs": 14,
            "exact_s5_loss": exact_losses, "unknown_positions_at_15m": unknown_runs,
            "total_nodes": total_nodes, "exact_nodes": exact_nodes,
            "positions": new_results,
        },
        "cumulative_experiment": {
            "distinct_positions": 10, "runs": 20,
            "direct_s5_loss": start_report["probes"]["exact_s5_loss"] + exact_losses,
            "total_nodes": start_nodes + total_nodes,
            "exact_nodes": start_exact_nodes + exact_nodes,
        },
        "solver": start_report["solver"],
        "final_exact_s5_cache": {
            **artifact(final_cache_path), "rows": len(final_cache),
            "verdict_counts": {"WIN": 158, "LOSS": 5589},
            "active_quarantined_keys": 0,
        },
        "target_s4": {
            "key": list(S4), "coverage": target["coverage"], "children": 109,
            "boundary": target["boundary"], "status": "UNKNOWN",
            "unresolved_s5_children": 89,
        },
        "frontier": {
            "classes": frontier["s4_class_counts"],
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
            "s4_key": list(S4), "s5_key": list(next_key),
            "legal_count": next_plan["s5_target"]["legal_count"],
            "raw_history_ready": True, "prior_observations": next_plan["prior_observations"],
            "saved_layer_verdict": None, "plan": artifact(next_plan_path),
        },
        "evidence_limit": (
            "The six new S5 LOSS verdicts are positive-budget solver outputs with raw traces, "
            "independent geometry, and conflict checks. They are not terminal-only independent "
            "minimax certificates. The 15M UNKNOWN remains outside the exact cache. Existing "
            "cache-only evidence remains in the global frontier, so this is not a complete "
            "independent minimax proof DAG."
        ),
    }
    out_path = OUT / "report-continuation.json"
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"path": rel(out_path), "sha256": sha(out_path),
                      "new_losses": exact_losses, "unknown_15m": unknown_runs,
                      "total_nodes": total_nodes, "target_boundary": target["boundary"]}, sort_keys=True))


if __name__ == "__main__":
    main()

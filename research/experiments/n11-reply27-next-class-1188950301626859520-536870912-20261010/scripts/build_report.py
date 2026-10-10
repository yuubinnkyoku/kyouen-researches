"""Validate and summarize the bounded follow-up S5 probes."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from s5_evidence_policy import quarantined_cache_keys  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return [row for row in csv.reader(stream) if row and row[0] == "replay"]


def main() -> None:
    expected = [
        ((3494793310840553472, 536870912), 88, "probe-2m.csv", "probe-15m.csv", 3_981_449),
        ((1188950301626859520, 536936448), 89, "probe-2m-second.csv", "probe-15m-second.csv", 2_335_333),
        ((1189513251580280832, 536870912), 89, "probe-2m-third.csv", "probe-15m-third.csv", 2_457_938),
    ]
    probes = []
    for key, legal, low_name, high_name, high_nodes in expected:
        low_path, high_path = OUT / low_name, OUT / high_name
        low_rows, high_rows = read_rows(low_path), read_rows(high_path)
        if len(low_rows) != 1 or len(high_rows) != 1:
            raise SystemExit(f"expected one replay row per probe for {key}")
        low, high = low_rows[0], high_rows[0]
        low_values = tuple(map(int, (low[2], low[3], low[4], low[5], low[6], low[7], low[9], low[10])))
        high_values = tuple(map(int, (high[2], high[3], high[4], high[5], high[6], high[7], high[9], high[10])))
        if low_values != (5, legal, 0, 2_000_000, 0, 2_000_000, *key):
            raise SystemExit(f"unexpected 2M probe result for {key}: {low}")
        if high_values != (5, legal, 0, 15_000_000, 2, high_nodes, *key):
            raise SystemExit(f"unexpected 15M probe result for {key}: {high}")
        probes.append({
            "key": list(key), "legal_count": legal,
            "2m": {"path": low_path.relative_to(ROOT).as_posix(), "sha256": sha(low_path),
                   "verdict": "UNKNOWN", "nodes": 2_000_000},
            "15m": {"path": high_path.relative_to(ROOT).as_posix(), "sha256": sha(high_path),
                    "verdict": "LOSS", "nodes": high_nodes},
        })

    before = json.loads((OUT / "geometric-cache-preflight.json").read_text(encoding="utf-8"))
    after = json.loads((OUT / "geometric-preflight-after-three.json").read_text(encoding="utf-8"))
    raw_audit = json.loads((OUT / "raw-history-after-third-15m.json").read_text(encoding="utf-8"))
    layer_audit = json.loads((OUT / "saved-layer-after-third-15m.json").read_text(encoding="utf-8"))
    frontier = json.loads((OUT / "frontier-after-probe-3.json").read_text(encoding="utf-8"))
    cache_path = OUT / "current-exact-s5-after-probe-3.cache"
    exact = {}
    for line in cache_path.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            fields = line.split(",")
            exact[(int(fields[1]), int(fields[2]))] = int(fields[4])
    quarantine = quarantined_cache_keys()
    if set(exact) & quarantine:
        raise SystemExit("active quarantine key entered the merged cache")
    if len(exact) != 5741 or Counter(exact.values()) != Counter({1: 158, 2: 5583}):
        raise SystemExit("unexpected final exact cache size/verdict counts")
    if before["class"]["cache_boundary"] != {"LOSS": 11, "UNKNOWN": 98, "WIN": 0}:
        raise SystemExit("unexpected starting S4 boundary")
    if after["class"]["cache_boundary"] != {"LOSS": 14, "UNKNOWN": 95, "WIN": 0}:
        raise SystemExit("unexpected final S4 boundary")
    if after["class"]["status"] != "UNKNOWN":
        raise SystemExit("target S4 class is no longer UNKNOWN")
    if frontier["s4_class_counts"] != {"LOSS": 31, "UNKNOWN": 3081, "WIN": 272}:
        raise SystemExit("unexpected all-frontier classification")
    if frontier["secured_third_moves"] != 117 or frontier["remaining_third_moves"] != [100, 108]:
        raise SystemExit("unexpected third-move coverage")
    if frontier["integer_minimum_additional_classes"] != 1 or frontier["rational_lp_dual"]["value"] != "1":
        raise SystemExit("unexpected cover lower bound / LP dual")
    if raw_audit["exact_verdict_conflicts"] or raw_audit["prior_unknown_same_budget_or_higher"]:
        raise SystemExit("raw history has a conflict or same/higher-budget UNKNOWN")
    if layer_audit["s5_results_from_raw_s6_s7_only"] or layer_audit["s5_results_with_saved_cache_s6_s7"]:
        raise SystemExit("saved S6/S7 results derived an S5 verdict")

    next_target = after["lowest_legal_unknown_s5"][0]
    next_key = tuple(next_target["key"])
    ready = {tuple(item) for item in raw_audit["dispatch_ready_keys"]}
    token = f"{next_key[0]},{next_key[1]}"
    next_observations = raw_audit["observations"].get(token, [])
    if next_key not in ready or any(item["verdict"] in (1, 2) for item in next_observations):
        raise SystemExit("next lowest-legal S5 child is not ready")
    if token in layer_audit["s5_results_from_raw_s6_s7_only"] or token in layer_audit["s5_results_with_saved_cache_s6_s7"]:
        raise SystemExit("next candidate already has a saved-layer verdict")

    solver = ROOT / ".local/n11-independent-audit-solver.exe"
    source = ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"
    geometry_source = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
    probe_runs = 6
    total_nodes = sum(item["2m"]["nodes"] + item["15m"]["nodes"] for item in probes)
    exact_nodes = sum(item["15m"]["nodes"] for item in probes)
    report = {
        "schema": "n11-reply27-next-class-probe-report-v1",
        "main_commit_at_start": "1739ddf2f9a5ec411ad5aeb0a2d8f9259951597c",
        "target_s4": {"key": [1188950301626859520, 536870912],
                      "coverage": [55, 65, 100, 108], "children": 109,
                      "starting_boundary": before["class"]["cache_boundary"],
                      "final_boundary": after["class"]["cache_boundary"],
                      "final_status": "UNKNOWN"},
        "probes": {"runs": probe_runs, "distinct_s5_positions": 3,
                   "exact_s5_loss": 3, "unknown_runs": 3,
                   "total_nodes": total_nodes, "exact_nodes": exact_nodes,
                   "positions": probes},
        "final_exact_s5_cache": {"path": cache_path.relative_to(ROOT).as_posix(),
                                 "sha256": sha(cache_path), "rows": len(exact),
                                 "verdict_counts": {"WIN": 158, "LOSS": 5583},
                                 "active_quarantined_keys": 0},
        "frontier": {"classes": 3384, "s4_class_counts": frontier["s4_class_counts"],
                     "secured_third_moves": 117, "total_third_moves": 119,
                     "remaining_third_moves": [100, 108],
                     "integer_minimum_additional_classes": 1,
                     "rational_lp_dual": frontier["rational_lp_dual"]},
        "post_probe_raw_history": {"csv_files_examined": raw_audit["csv_files_examined"],
                                   "target_children": {"count": raw_audit["targets"]["count"]},
                                   "raw_exact_rows": len(raw_audit["prior_exact"]),
                                   "cache_hits": raw_audit["current_cache"]["target_exact_intersection"],
                                   "conflicts": len(raw_audit["exact_verdict_conflicts"]),
                                   "dispatch_ready_unknown_children": len(raw_audit["dispatch_ready_keys"]),
                                   "same_or_higher_15m_unknown": len(raw_audit["prior_unknown_same_budget_or_higher"])},
        "saved_layers": {"s6_boundary_keys": layer_audit["s6_boundary"]["distinct_canonical_keys"],
                         "raw_s6_exact": len(layer_audit["raw_s6"]["exact_keys"]),
                         "cache_s6_exact": len(layer_audit["saved_cache_s6"]["exact_keys"]),
                         "raw_s7_exact": len(layer_audit["raw_s7"]["exact_keys"]),
                         "s7_cache_intersections": len(layer_audit["saved_cache_s7"]["target_intersections"]),
                         "s5_derived": 0},
        "next_candidate": {"s4_key": [1188950301626859520, 536870912],
                           "s5_key": list(next_key), "legal_count": next_target["legal_count"],
                           "raw_history_ready": True, "saved_layer_verdict": None,
                           "prior_observations": next_observations},
        "evidence_limit": "The three new direct S5 LOSS verdicts are positive-budget solver outputs with independent geometry and history checks. They are not terminal-only independent minimax certificates. The merged cache and overall frontier retain pre-existing cache-only leaves.",
        "solver": {"path": solver.relative_to(ROOT).as_posix(), "sha256": sha(solver),
                   "source_path": source.relative_to(ROOT).as_posix(), "source_sha256": sha(source),
                   "options": ["--n=11", "--memo=22", "--exact-order=count"]},
        "independent_geometry_source": {"path": geometry_source.relative_to(ROOT).as_posix(),
                                        "sha256": sha(geometry_source)},
    }
    report_path = OUT / "report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"total_nodes": total_nodes, "exact_nodes": exact_nodes,
                      "s4_boundary": after["class"]["cache_boundary"],
                      "next_s5": [*next_key], "legal_count": next_target["legal_count"],
                      "report_sha256": sha(report_path)}, sort_keys=True))


if __name__ == "__main__":
    main()

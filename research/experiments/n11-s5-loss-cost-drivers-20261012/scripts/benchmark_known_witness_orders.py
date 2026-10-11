"""Compare supported exact child orders on the already known S6 proof roots."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmark_cost_drivers import run_one, sha256

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--schedule", type=Path, default=EXP / "input/known-witness-order-schedule.json")
    ap.add_argument("--out", type=Path, default=EXP / "output/known-witness-order-6m")
    args = ap.parse_args()
    binary, schedule_path, out = (path.resolve() for path in (args.solver, args.schedule, args.out))
    if not binary.is_file() or not schedule_path.is_file() or out.exists():
        ap.error("solver/schedule must exist and output must be new")
    schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
    if schedule.get("schema") != "n11-s5-known-s6-witness-order-schedule-v1":
        ap.error("unsupported known-witness order schedule")
    if sha256(binary) != schedule["solver_binary_sha256"]:
        ap.error("solver binary differs from the S5/S6 cost-driver benchmark")
    baseline_path = ROOT / schedule["baseline_stage1"]
    if not baseline_path.is_file() or sha256(baseline_path) != schedule["baseline_stage1_sha256"]:
        ap.error("COUNT baseline summary does not match the frozen order schedule")
    baseline_summary = json.loads(baseline_path.read_text(encoding="utf-8"))
    out.mkdir(parents=True)
    runs = []
    for target in schedule["targets"]:
        row = target["s6"]
        for order in schedule["candidate_orders"]:
            result = run_one(binary, out,
                f"{order}--{target['target_id'].replace('/', '--')}--candidate-{target['candidate_index']}",
                [row], node_cap=schedule["budget_per_witness"], share_tt=False,
                stop_on_loss=False, exact_order=order)
            actual = result["rows"][0]
            if actual["verdict"] == 1:
                raise ValueError(f"alternate order contradicts pinned S6 LOSS proof: {row['key']}")
            baseline = target["count_order_reference"]
            runs.append({
                "target_id": target["target_id"], "candidate_index": target["candidate_index"],
                "s6_key": row["key"], "legal_s7_children": target["legal_s7_children"],
                "proof_dag_nodes": target["proof_dag_nodes"],
                "proof_dag_edges": target["proof_dag_edges"],
                "order": order, "result": result,
                "count_order_reference": {"nodes": baseline["nodes"],
                    "verdict": baseline["verdict"], "wall_seconds": next(
                        run["wall_seconds"] for run in baseline_summary["per_run_results"]["B"]
                        if run["target_id"] == target["target_id"]
                        and run["candidate_index"] == target["candidate_index"])},
                "node_change_vs_count": result["total_nodes"] - baseline["nodes"],
                "node_reduction_fraction_vs_count": (
                    (baseline["nodes"] - result["total_nodes"]) / baseline["nodes"]
                    if actual["verdict"] != 0 else None),
                "count_order_verdict": baseline["verdict"],
            })
    by_order = {}
    for order in schedule["candidate_orders"]:
        selected = [run for run in runs if run["order"] == order]
        by_order[order] = {
            "runs": len(selected),
            "verdict_counts": {name: sum(run["result"]["rows"][0]["verdict"] == value
                for run in selected) for name, value in (("WIN", 1), ("LOSS", 2), ("UNKNOWN", 0))},
            "total_nodes": sum(run["result"]["total_nodes"] for run in selected),
            "total_wall_seconds": sum(run["result"]["wall_seconds"] for run in selected),
            "max_peak_rss_bytes": max((run["result"]["peak_rss_bytes"] or 0 for run in selected), default=0) or None,
            "node_reductions_vs_count": sum(run["node_reduction_fraction_vs_count"] is not None
                and run["node_reduction_fraction_vs_count"] > 0 for run in selected),
        }
    result = {
        "schema": "n11-s5-known-s6-witness-order-benchmark-v1",
        "schedule_path": str(schedule_path.relative_to(ROOT)).replace("\\", "/"),
        "schedule_sha256": sha256(schedule_path),
        "solver_binary_path": str(binary), "solver_binary_sha256": sha256(binary),
        "stage1_count_order_reference": schedule["baseline_stage1"],
        "stage1_count_order_reference_sha256": schedule["baseline_stage1_sha256"],
        "initial_cache_condition": "Each candidate/order is a new process with an empty exact TT; no external cache or proof DAG is loaded.",
        "budget_per_witness": schedule["budget_per_witness"],
        "order_aggregates": by_order,
        "per_witness": runs,
        "interpretation_limits": [
            "The correct S6 LOSS root is known from an existing independent terminal-only DAG; this reference experiment does not establish a blind witness-selection improvement.",
            "An UNKNOWN at the fixed cap has no inferred completion cost.",
            "Search-node reductions are finite to these six known S6 roots and this exact solver.",
        ],
        "trust_note": "The previously verified terminal-only proof DAGs are the independent evidence; this benchmark uses new solver outputs only as performance observations.",
    }
    summary_path = out / "summary.json"
    summary_path.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    files = []
    for path in sorted(item for item in out.rglob("*") if item.is_file()):
        files.append({"path": str(path.relative_to(out)).replace("\\", "/"),
                      "bytes": path.stat().st_size, "sha256": sha256(path)})
    (out / "artifact-manifest.json").write_text(
        json.dumps({"schema": "n11-s5-known-s6-witness-order-artifacts-v1", "files": files},
                   sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)).replace("\\", "/"),
                      "summary_sha256": sha256(summary_path), "aggregates": by_order}, sort_keys=True))


if __name__ == "__main__":
    main()

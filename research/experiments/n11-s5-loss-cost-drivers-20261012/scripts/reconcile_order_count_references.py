"""Refresh order-study COUNT timings from the schedule-pinned same-binary baseline."""
from __future__ import annotations

import json
from pathlib import Path

from benchmark_cost_drivers import ROOT, EXP, sha256


def main() -> None:
    schedule_path = EXP / "input/known-witness-order-schedule-v2.json"
    output = EXP / "output/known-witness-order-v2-6m"
    summary_path = output / "summary.json"
    schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
    baseline_path = ROOT / schedule["baseline_stage1"]
    if sha256(baseline_path) != schedule["baseline_stage1_sha256"]:
        raise ValueError("schedule-pinned COUNT baseline SHA mismatch")
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary["solver_binary_sha256"] != baseline["solver_binary_sha256"]:
        raise ValueError("order and COUNT baseline binaries differ")
    for item in summary["per_witness"]:
        match = next(run for run in baseline["per_run_results"]["B"]
                     if run["target_id"] == item["target_id"]
                     and run["candidate_index"] == item["candidate_index"])
        item["count_order_reference"]["wall_seconds"] = match["wall_seconds"]
    summary["count_order_reference_revision"] = (
        "COUNT wall timings refreshed from the exact schedule-pinned stage1 summary; node/verdict/raw results unchanged"
    )
    summary_path.write_text(json.dumps(summary, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8")
    files = [{"path": str(path.relative_to(output)).replace("\\", "/"),
              "bytes": path.stat().st_size, "sha256": sha256(path)}
             for path in sorted(p for p in output.rglob("*") if p.is_file()
                                and p.name != "artifact-manifest.json")]
    (output / "artifact-manifest.json").write_text(
        json.dumps({"schema": "n11-s5-known-s6-witness-order-artifacts-v1", "files": files},
                   sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"summary_sha256": sha256(summary_path),
                      "count_baseline": schedule["baseline_stage1"],
                      "count_baseline_sha256": schedule["baseline_stage1_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()

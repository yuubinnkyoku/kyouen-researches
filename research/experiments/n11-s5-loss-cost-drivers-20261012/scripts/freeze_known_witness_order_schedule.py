"""Select the existing certificate-backed S6 witnesses for an ordering study."""
from __future__ import annotations

import hashlib
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--comparison", type=Path, default=EXP / "input/comparison-schedule.json")
    ap.add_argument("--benchmark", type=Path, default=EXP / "output/stage1-6m/summary.json")
    ap.add_argument("--out", type=Path, default=EXP / "input/known-witness-order-schedule.json")
    args = ap.parse_args()
    out, source, benchmark = (path.resolve() for path in (args.out,args.comparison,args.benchmark))
    if sha256(source) != "b1cbb0930d594bdac9d1fd63975d53b68c4b2c37829bd470c34d945e6a4ca36d":
        raise ValueError("comparison schedule SHA-256 mismatch")
    comparison = json.loads(source.read_text(encoding="utf-8"))
    result = json.loads(benchmark.read_text(encoding="utf-8"))
    selected = []
    for target in comparison["targets"]:
        for candidate_index, candidate in enumerate(target["saved_s6_loss_candidates"]):
            selected.append({
                "target_id": target["id"], "candidate_index": candidate_index,
                "s6": {"key": candidate["s6_key"], "lo": candidate["s6_lo"],
                       "hi": candidate["s6_hi"], "stones": 6, "legal": candidate["s6_legal"]},
                "proof_dag_nodes": candidate["proof_dag_nodes"],
                "proof_dag_edges": candidate["proof_dag_edges"],
                "legal_s7_children": candidate["legal_s7_children"],
                "count_order_reference": next(
                    row for run in result["per_run_results"]["B"]
                    if run["target_id"] == target["id"]
                    and run["candidate_index"] == candidate_index for row in run["rows"]),
            })
    result = {
        "schema": "n11-s5-known-s6-witness-order-schedule-v1",
        "comparison_schedule": str(source.relative_to(ROOT)).replace("\\", "/"),
        "comparison_schedule_sha256": sha256(source),
        "baseline_stage1": str(benchmark.relative_to(ROOT)).replace("\\", "/"),
        "baseline_stage1_sha256": sha256(benchmark),
        "solver_binary_sha256": result["solver_binary_sha256"],
        "selection_rule": "Use every S6 LOSS witness already saved in the terminal-only proof DAGs for the three fixed S5 roots; the root with two witnesses contributes both. Count-order baseline costs come from the same binary and cold-cache stage-1 rows.",
        "budget_per_witness": 6_000_000,
        "candidate_orders": ["countd", "key"],
        "target_count": len(selected),
        "targets": selected,
    }
    out.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(out.relative_to(ROOT)).replace("\\", "/"),
                      "sha256": sha256(out), "targets": len(selected),
                      "orders": result["candidate_orders"]}, sort_keys=True))


if __name__ == "__main__":
    main()

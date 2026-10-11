"""Re-run the saved decisive S6 witnesses on the child-profile binary."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmark_cost_drivers import ROOT, EXP, run_one, sha256


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--build", type=Path, default=EXP / "input/child-profile-build.json")
    ap.add_argument("--schedule", type=Path, default=EXP / "input/comparison-schedule.json")
    ap.add_argument("--out", type=Path, default=EXP / "output/known-s6-costs-v2-6m")
    args = ap.parse_args()
    binary, build_path, schedule_path, out = (
        path.resolve() for path in (args.solver, args.build, args.schedule, args.out)
    )
    source = ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"
    if out.exists() or not binary.is_file() or not build_path.is_file() or not schedule_path.is_file():
        ap.error("solver/build/schedule must exist and output must be new")
    build, schedule = json.loads(build_path.read_text(encoding="utf-8")), json.loads(
        schedule_path.read_text(encoding="utf-8"))
    if schedule.get("schema") != "n11-s5-loss-cost-driver-schedule-v1":
        ap.error("unsupported frozen schedule")
    if build.get("source_sha256") != sha256(source) or build.get("binary_sha256") != sha256(binary):
        ap.error("known-witness solver does not match the source/build manifest")
    direct = json.loads((EXP / "output/direct-s5-child-profile-6m/summary.json").read_text(encoding="utf-8"))
    out.mkdir(parents=True)
    results = []
    cap = schedule["budget_protocol"]["stage1_s6_single_candidate_node_cap"]
    for target in schedule["targets"]:
        for candidate_index, candidate in enumerate(target["saved_s6_loss_candidates"]):
            row = {"key": candidate["s6_key"], "lo": candidate["s6_lo"],
                   "hi": candidate["s6_hi"], "stones": candidate["s6_stones"],
                   "legal": candidate["s6_legal"]}
            run = run_one(binary, out,
                f"{target['id'].replace('/', '--')}--candidate-{candidate_index}", [row],
                node_cap=cap, share_tt=False, stop_on_loss=False)
            actual = run["rows"][0]
            if actual["verdict"] != 2:
                raise ValueError(f"independently saved S6 LOSS witness failed exact replay: {candidate['s6_key']}")
            results.append({
                "target_id": target["id"], "candidate_index": candidate_index,
                "s5_key": target["s5"]["key"], "s6_key": candidate["s6_key"],
                "legal_s7_children": candidate["s6_legal"],
                "proof_dag_nodes": candidate["proof_dag_nodes"],
                "proof_dag_edges": candidate["proof_dag_edges"],
                "selected_by_s5_proof": candidate["is_selected_by_s5_root"],
                "run": run,
            })
    root_results = []
    for target in schedule["targets"]:
        direct_row = next(item for item in direct["rows"] if item["target_id"] == target["id"])
        witnesses = [item for item in results if item["target_id"] == target["id"]]
        root_results.append({
            "target_id": target["id"], "s5_key": target["s5"]["key"],
            "direct_s5_nodes": direct_row["total_nodes"],
            "preceding_sibling_nodes": direct_row["preceding_sibling_nodes"],
            "decisive_direct_s6_key": direct_row["decisive_s6_key"],
            "decisive_direct_s6_nodes": direct_row["decisive_s6_nodes"],
            "known_s6_candidates": [{
                "s6_key": item["s6_key"], "nodes": item["run"]["total_nodes"],
                "verdict": item["run"]["rows"][0]["verdict"],
                "wall_seconds": item["run"]["wall_seconds"],
                "peak_rss_bytes": item["run"]["peak_rss_bytes"],
                "proof_dag_nodes": item["proof_dag_nodes"],
                "proof_dag_edges": item["proof_dag_edges"],
                "legal_s7_children": item["legal_s7_children"],
                "selected_by_s5_proof": item["selected_by_s5_proof"],
            } for item in witnesses],
        })
    summary = {
        "schema": "n11-known-s6-witness-exact-cost-v2-v1",
        "solver_source_sha256": build["source_sha256"],
        "solver_binary_sha256": build["binary_sha256"],
        "schedule_sha256": sha256(schedule_path),
        "direct_s5_profile_sha256": sha256(EXP / "output/direct-s5-child-profile-6m/summary.json"),
        "node_cap_per_witness": cap,
        "cache_condition": "fresh empty exact TT for every S6 replay; no external cache or proof DAG loaded",
        "rows": results, "roots": root_results,
        "interpretation_limits": [
            "S6 roots are already known LOSS from terminal-only independent proof DAGs; these are reference costs, not blind witness-selection costs.",
            "Exact recursion node counts and proof-DAG node counts are different quantities.",
            "All solver results are observations; independent proof DAGs remain the evidence for LOSS.",
        ],
    }
    path = out / "summary.json"
    path.write_text(json.dumps(summary, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    files = [{"path": str(item.relative_to(out)).replace("\\", "/"), "bytes": item.stat().st_size,
              "sha256": sha256(item)} for item in sorted(x for x in out.rglob("*") if x.is_file())]
    (out / "artifact-manifest.json").write_text(
        json.dumps({"schema": "n11-known-s6-witness-exact-cost-artifacts-v1", "files": files},
                   sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(path.relative_to(ROOT)).replace("\\", "/"),
                      "summary_sha256": sha256(path),
                      "roots": [{"target_id": root["target_id"],
                          "direct_s5_nodes": root["direct_s5_nodes"],
                          "preceding_sibling_nodes": root["preceding_sibling_nodes"],
                          "decisive_direct_s6_nodes": root["decisive_direct_s6_nodes"],
                          "known_s6_nodes": [w["nodes"] for w in root["known_s6_candidates"]]}
                          for root in root_results]}, sort_keys=True))


if __name__ == "__main__":
    main()

"""Attribute direct exact S5 replay nodes to its ordered S6 children."""
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
    ap.add_argument("--out", type=Path, default=EXP / "output/direct-s5-child-profile-6m")
    args = ap.parse_args()
    binary, build_path, schedule_path, out = (
        path.resolve() for path in (args.solver, args.build, args.schedule, args.out)
    )
    source = ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"
    build = json.loads(build_path.read_text(encoding="utf-8"))
    schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
    if out.exists() or not binary.is_file() or not build_path.is_file() or not schedule_path.is_file():
        ap.error("solver/build/schedule must exist and output must be new")
    if schedule.get("schema") != "n11-s5-loss-cost-driver-schedule-v1":
        ap.error("unsupported frozen schedule")
    if (build.get("source_sha256") != sha256(source)
            or build.get("binary_sha256") != sha256(binary)):
        ap.error("child-profile solver does not match its source/build manifest")
    out.mkdir(parents=True)
    baseline = json.loads((EXP / "output/stage1-6m/summary.json").read_text(encoding="utf-8"))
    rows = []
    for target in schedule["targets"]:
        s5 = target["s5"]
        row = {"key": s5["key"], "lo": s5["lo"], "hi": s5["hi"],
               "stones": 5, "legal": s5["legal"]}
        run = run_one(binary, out, f"{target['id'].replace('/', '--')}", [row],
                      node_cap=schedule["budget_protocol"]["stage1_s5_root_node_cap"],
                      share_tt=False, stop_on_loss=False)
        actual = run["rows"][0]
        old = next(x for x in baseline["per_run_results"]["A"] if x["target_id"] == target["id"])
        old_row = old["rows"][0]
        if (actual["verdict"], actual["nodes"]) != (old_row["verdict"], old_row["nodes"]):
            raise ValueError(f"instrumentation changed direct S5 replay: {target['id']}")
        children = [item for item in run["profile"] if item["kind"] == "root_child"]
        loss_index = next((i for i, child in enumerate(children) if child["verdict"] == "LOSS"), None)
        if actual["verdict"] != 2 or loss_index is None:
            raise ValueError(f"direct S5 LOSS has no measured decisive S6 child: {target['id']}")
        known = {str(item["s6_key"]) for item in target["saved_s6_loss_candidates"]}
        decisive = children[loss_index]
        decisive_key = str((decisive["hi"] << 64) | decisive["lo"])
        if decisive_key not in known:
            raise ValueError(f"direct decisive S6 is not among the pinned proof-DAG witnesses: {target['id']}")
        if sum(child["nodes"] for child in children) + 1 != actual["nodes"]:
            raise ValueError(f"root and child node attribution do not sum to the direct total: {target['id']}")
        preceding = children[:loss_index]
        rows.append({
            "target_id": target["id"], "s5_key": s5["key"],
            "verdict": "LOSS", "total_nodes": actual["nodes"],
            "wall_seconds": run["wall_seconds"], "peak_rss_bytes": run["peak_rss_bytes"],
            "root_node": 1,
            "visited_s6_children": len(children), "decisive_child_index": loss_index,
            "decisive_s6_key": decisive_key,
            "decisive_s6_legal_s7": decisive["legal"],
            "decisive_s6_nodes": decisive["nodes"],
            "preceding_sibling_nodes": sum(child["nodes"] for child in preceding),
            "preceding_sibling_verdicts": {
                name: sum(child["verdict"] == name for child in preceding)
                for name in ("WIN", "LOSS", "UNKNOWN")
            },
            "all_visited_children": children,
            "rank_profile": [item for item in run["profile"] if item["kind"] == "rank"],
            "table_profile": [item for item in run["profile"] if item["kind"] == "table"],
            "run": run,
        })
    result = {
        "schema": "n11-direct-s5-s6-child-cost-attribution-v1",
        "solver_source_sha256": build["source_sha256"],
        "solver_binary_sha256": build["binary_sha256"],
        "schedule_sha256": sha256(schedule_path),
        "stage1_reference_sha256": sha256(EXP / "output/stage1-6m/summary.json"),
        "method": "At each direct S5 exact replay, count exact_nodes_ deltas around each immediate S6 child call, in the solver's deterministic count order; stop profile at first decisive S6 LOSS. The independently verified proof DAG authenticates the decisive witness; this solver run is performance observation only.",
        "rows": rows,
        "interpretation_limits": [
            "Node deltas are incremental costs in this direct root's shared TT/order, not standalone costs for each child.",
            "The direct replay uses the repository's exact_prop recursive exact-search component, not solve_root's DFPN expansion counter.",
            "UNKNOWN siblings before the decisive child remain observed costs, not solved child outcomes.",
        ],
    }
    summary_path = out / "summary.json"
    summary_path.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8")
    files = []
    for path in sorted(item for item in out.rglob("*") if item.is_file()):
        files.append({"path": str(path.relative_to(out)).replace("\\", "/"),
                      "bytes": path.stat().st_size, "sha256": sha256(path)})
    (out / "artifact-manifest.json").write_text(
        json.dumps({"schema": "n11-direct-s5-s6-child-cost-artifacts-v1", "files": files},
                   sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)).replace("\\", "/"),
                      "summary_sha256": sha256(summary_path),
                      "roots": [{key: row[key] for key in ("target_id", "total_nodes", "preceding_sibling_nodes",
                          "decisive_s6_nodes", "visited_s6_children", "decisive_s6_key")}
                          for row in rows]}, sort_keys=True))


if __name__ == "__main__":
    main()

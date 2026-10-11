"""Build a small audit from an integration plan and an independent benchmark."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
BOUNDARY_REPORT = ROOT / "research/experiments/n11-reply27-20more-20261011/output/audit.json"
THREE_ROOT_AUDIT = ROOT / "research/experiments/n11-proof-compact-20261011/output/proof-compact-audit.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build(plan_path: Path, benchmark_path: Path, three_root_path: Path,
          incremental_path: Path, optimized_path: Path,
          optimizer_benchmark_path: Path) -> dict:
    plan = read_json(plan_path)
    benchmark = read_json(benchmark_path)
    optimizer_benchmark = read_json(optimizer_benchmark_path)
    boundary_report = read_json(BOUNDARY_REPORT)
    three_root_audit = read_json(THREE_ROOT_AUDIT)
    require(plan.get("schema") == "n11-incremental-proof-integration-run-v1",
            "unsupported integration plan")
    require(plan.get("search_or_probe_launched") is False
            and plan.get("solver_or_cache_evidence_imported") is False,
            "integration plan must not contain search or solver/cache evidence")
    require(plan.get("trusted_leaves") == 0 and plan.get("final_root_count") == 6,
            "integration plan must describe six terminal-only roots")
    require(benchmark.get("schema") == "n11-proof-verifier-benchmark-v1"
            and benchmark.get("format") == "compact"
            and benchmark.get("returncode") == 0
            and benchmark.get("peak_rss_bytes") is not None
            and benchmark.get("peak_scratch_bytes") is not None,
            "independent compact verifier did not succeed with RSS and scratch measurements")
    require(optimizer_benchmark.get("schema") == "n11-proof-integration-benchmark-v1"
            and optimizer_benchmark.get("returncode") == 0
            and optimizer_benchmark.get("peak_process_tree_rss_bytes") is not None,
            "optimizer process-tree benchmark did not complete with an RSS sample")
    require(optimizer_benchmark.get("integration_plan_sha256") == sha256(plan_path),
            "optimizer benchmark does not match the supplied integration plan")

    stage_three = plan["stages"]["three_root_start"]["optimized_certificate"]
    stage_six = plan["stages"]["six_root_increment"]
    three_sha = sha256(three_root_path)
    incremental_sha = sha256(incremental_path)
    optimized_sha = sha256(optimized_path)
    require(three_sha == stage_three["certificate_sha256"],
            "three-root output hash differs from the plan")
    require(three_sha == "478fc29e51ffd7e18158f74f0032b7e7756446e11c5d0819b000e19e79474fc2",
            "three-root output no longer reproduces K0377")
    three_root_baseline = three_root_audit["optimized_compact_run"]
    require(three_root_baseline["certificate_sha256"] == three_sha
            and three_root_baseline["verifier_returncode"] == 0
            and three_root_baseline["trusted_leaves"] == 0,
            "K0377 verification baseline does not match the reproduced three-root bytes")
    require(incremental_sha == stage_six["incremental_certificate"]["certificate_sha256"],
            "incremental output hash differs from the plan")
    require(optimized_sha == stage_six["jointly_optimized_certificate"]["certificate_sha256"],
            "optimized output hash differs from the plan")
    require(incremental_sha == optimized_sha,
            "incremental and optimized certificates differ; verify both before audit")

    receipt = benchmark.get("verifier_receipt")
    require(isinstance(receipt, dict), "benchmark has no independent verifier receipt")
    expected_roots = {(entry["root"], entry["verdict"])
                      for entry in plan["final_root_masks"]}
    actual_roots = {(entry.get("root"), entry.get("verdict"))
                    for entry in receipt.get("roots", [])}
    require(actual_roots == expected_roots and len(actual_roots) == 6,
            "independent receipt does not confirm all six expected root verdicts")
    require(receipt.get("trusted_leaves") == 0
            and all(verdict == 2 for _, verdict in actual_roots),
            "independent receipt must confirm six LOSS roots and zero trusted leaves")
    expected_six = stage_six["jointly_optimized_certificate"]
    require(receipt.get("nodes") == expected_six["nodes"]
            and receipt.get("edges") == expected_six["edges"],
            "independent verifier counts differ from the optimized certificate")
    require(benchmark.get("certificate_bytes") == optimized_path.stat().st_size,
            "benchmark certificate size differs from the optimized artifact")
    benchmark_certificate = Path(benchmark["certificate"])
    require(benchmark_certificate.is_file()
            and sha256(benchmark_certificate) == optimized_sha,
            "independent verification receipt is not bound to the optimized certificate bytes")

    target_s4 = boundary_report["target_s4_after"]
    require(boundary_report["root_s4_key"] == [1297036692683752448, 0]
            and target_s4 == {"LOSS": 40, "WIN": 0, "UNKNOWN": 66},
            "latest target S4 report does not match the expected 40/0/66 boundary")

    source_bytes = sum(source["bundle_bytes"] for source in plan["sources"])
    final_bytes = optimized_path.stat().st_size
    uninterned_nodes = stage_six["source_node_sum_without_interning"]
    final_nodes = expected_six["nodes"]
    return {
        "schema": "n11-incremental-proof-integration-audit-v1",
        "date": "2026-10-11",
        "sources": [{
            "name": source["name"],
            "bundle": source["bundle"],
            "bytes": source["bundle_bytes"],
            "sha256": source["bundle_sha256"],
            "prior_verification": source["prior_verification"],
            "prior_verification_sha256": source["prior_verification_sha256"],
            "roots": source["roots"],
            "nodes": source["nodes"],
            "edges": source["edges"],
            "trusted_leaves": source["trusted_leaves"],
        } for source in plan["sources"]],
        "current_s4_boundary": {
            "root": "1297036692683752448",
            "loss": target_s4["LOSS"],
            "win": target_s4["WIN"],
            "unknown": target_s4["UNKNOWN"],
            "report": relative(BOUNDARY_REPORT),
            "report_sha256": sha256(BOUNDARY_REPORT),
            "trusted_solver_result_imported": False,
        },
        "three_root_reproduction": {
            "certificate": relative(three_root_path),
            "sha256": three_sha,
            "nodes": stage_three["nodes"],
            "edges": stage_three["edges"],
            "bytes": three_root_path.stat().st_size,
            "matches_k0377": True,
        },
            "three_root_verification_baseline": {
                "audit": relative(THREE_ROOT_AUDIT),
                "certificate_sha256": three_root_baseline["certificate_sha256"],
                "nodes": three_root_baseline["nodes"],
                "edges": three_root_baseline["edges"],
                "bytes": three_root_baseline["certificate_bytes"],
                "wall_seconds": three_root_baseline["wall_seconds"],
                "peak_rss_bytes": three_root_baseline["peak_rss_bytes"],
                "peak_scratch_bytes": three_root_baseline["peak_scratch_bytes"],
                "trusted_leaves": three_root_baseline["trusted_leaves"],
            },
        "six_root_integration": {
            "roots": plan["final_root_masks"],
            "input_node_sum": uninterned_nodes,
            "interned_candidate_nodes": stage_six["interned_candidate_nodes"],
            "duplicate_positions_shared": stage_six["duplicate_positions_shared"],
            "input_json_bytes_sum": source_bytes,
            "incremental": {
                "certificate": relative(incremental_path),
                "sha256": incremental_sha,
                "nodes": stage_six["incremental_certificate"]["nodes"],
                "edges": stage_six["incremental_certificate"]["edges"],
                "bytes": incremental_path.stat().st_size,
            },
            "jointly_optimized": {
                "certificate": relative(optimized_path),
                "sha256": optimized_sha,
                "uncompressed_sha256": stage_six["jointly_optimized_certificate"]["compact_uncompressed_sha256"],
                "nodes": expected_six["nodes"],
                "edges": expected_six["edges"],
                "bytes": final_bytes,
                "bytes_reduction_vs_two_source_json_percent": round(100 * (1 - final_bytes / source_bytes), 3),
                "node_reduction_vs_unoptimized_input_sum_percent": round(100 * (1 - final_nodes / uninterned_nodes), 3),
                "edge_reduction_vs_unoptimized_input_sum_percent": round(100 * (1 - expected_six["edges"] / stage_six["input_order_union"]["edges"]), 3),
            },
            "incremental_vs_joint_reduction": {
                "nodes": stage_six["node_reduction_vs_incremental"],
                "edges": stage_six["edge_reduction_vs_incremental"],
            },
            "duplicate_witness_candidates_added": stage_six["root_child_candidates"]["new_witness_options"],
            "greedy_root_steps": stage_six["greedy_root_add"]["root_steps"],
            "local_improvement": stage_six["local_improvement"],
            "exact_root_choice": stage_six["exact_root_choice"],
            "optimizer_seconds": plan["elapsed_optimizer_seconds"],
            "previous_source_import_seconds": stage_six["previous_source_import_seconds"],
            "six_root_stage_seconds": stage_six["six_root_stage_seconds"],
            "three_root_source_import_seconds": plan["stages"]["three_root_start"]["source_import_seconds"],
            "process_benchmark": {
                "receipt": relative(optimizer_benchmark_path),
                "wall_seconds": optimizer_benchmark["wall_seconds"],
                "peak_process_tree_rss_bytes": optimizer_benchmark["peak_process_tree_rss_bytes"],
                "peak_output_tree_bytes": optimizer_benchmark["peak_output_tree_bytes"],
                "rss_measurement": optimizer_benchmark["rss_measurement"],
            },
            "ten_root_measurement_available": False,
            "ten_root_measurement_reason": "No additional independently terminal-closed S5 root bundle was available; no search was launched.",
        },
        "independent_verification": {
            "benchmark": relative(benchmark_path),
            "certificate_sha256": optimized_sha,
            "same_certificate_as_incremental": True,
            "returncode": benchmark["returncode"],
            "wall_seconds": benchmark["wall_seconds"],
            "peak_rss_bytes": benchmark["peak_rss_bytes"],
            "rss_measurement": benchmark.get("rss_measurement"),
            "peak_scratch_bytes": benchmark["peak_scratch_bytes"],
            "nodes": receipt["nodes"],
            "edges": receipt["edges"],
            "terminal_nodes": receipt["terminal_nodes"],
            "trusted_leaves": receipt["trusted_leaves"],
            "roots": receipt["roots"],
            "growth_vs_three_root_percent": {
                "nodes": round(100 * (receipt["nodes"] / three_root_baseline["nodes"] - 1), 3),
                "edges": round(100 * (receipt["edges"] / three_root_baseline["edges"] - 1), 3),
                "certificate_bytes": round(100 * (benchmark["certificate_bytes"] / three_root_baseline["certificate_bytes"] - 1), 3),
                "wall_seconds": round(100 * (benchmark["wall_seconds"] / three_root_baseline["wall_seconds"] - 1), 3),
                "peak_rss_bytes": round(100 * (benchmark["peak_rss_bytes"] / three_root_baseline["peak_rss_bytes"] - 1), 3),
                "peak_scratch_bytes": round(100 * (benchmark["peak_scratch_bytes"] / three_root_baseline["peak_scratch_bytes"] - 1), 3),
            },
            "checks_preserved": [
                "all legal moves at universal nodes",
                "existential witness legality and fixed-first-player polarity",
                "terminal adjudication and canonicalization",
                "strict stone-rank progression and graph reachability",
                "all six roots are LOSS; trusted leaves are zero",
            ],
        },
        "scope_limit": "Six previously independently closed S5 roots only. The two source DAGs share no canonical positions; joint optimization adds no reduction beyond the reproduced K0377 witness switch. This does not prove the parent S4 boundaries or the {60,27} root.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--benchmark", type=Path, required=True)
    parser.add_argument("--three-root", type=Path, required=True)
    parser.add_argument("--incremental", type=Path, required=True)
    parser.add_argument("--optimized", type=Path, required=True)
    parser.add_argument("--optimizer-benchmark", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true", help="replace an existing output file")
    args = parser.parse_args()
    if args.output.exists() and not args.force:
        parser.error(f"refusing to overwrite {args.output}; pass --force to replace")
    try:
        audit = build(args.plan, args.benchmark, args.three_root,
                      args.incremental, args.optimized, args.optimizer_benchmark)
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"audit rejected: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, sort_keys=True, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"output": str(args.output),
                      "verified_roots": len(audit["independent_verification"]["roots"]),
                      "certificate_sha256": audit["independent_verification"]["certificate_sha256"]},
                     sort_keys=True))


if __name__ == "__main__":
    main()

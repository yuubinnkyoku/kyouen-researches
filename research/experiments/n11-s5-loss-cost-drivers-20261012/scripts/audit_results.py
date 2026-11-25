"""Audit frozen proof inputs, benchmark raw files, cross-arm counts, and hashes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmark_cost_drivers import ROOT, EXP, sha256


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_output_manifest(relative: str) -> dict:
    directory = EXP / "output" / relative
    manifest = load(directory / "artifact-manifest.json")
    verified = []
    for record in manifest["files"]:
        path = directory / record["path"]
        if not path.is_file() or path.stat().st_size != record["bytes"] or sha256(path) != record["sha256"]:
            raise ValueError(f"output artifact hash mismatch: {path}")
        verified.append(record["path"])
    return {"directory": relative, "files": len(verified),
            "manifest_sha256": sha256(directory / "artifact-manifest.json")}


def verify_profile_regression(relative: str) -> dict:
    directory = EXP / "output" / relative
    receipt_path = directory / "receipt.json"
    receipt = load(receipt_path)
    verified = ["receipt.json"]
    for run in receipt["runs"]:
        for suffix, key in (("raw.csv", "raw_sha256"), ("solver.log", "log_sha256")):
            path = directory / f"{run['name']}-{suffix}"
            if not path.is_file() or sha256(path) != run[key]:
                raise ValueError(f"profile regression artifact hash mismatch: {path}")
            verified.append(path.name)
    return {"directory": f"output/{relative}", "files": len(verified),
            "receipt_sha256": sha256(receipt_path)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", type=Path, help="optional local binary to hash against the build manifest")
    ap.add_argument("--out", type=Path, default=EXP / "output/audit.json")
    args = ap.parse_args()
    build = load(EXP / "input/child-profile-build.json")
    source = ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"
    if sha256(source) != build["source_sha256"]:
        raise ValueError("current solver source differs from child-profile build manifest")
    if args.solver and sha256(args.solver.resolve()) != build["binary_sha256"]:
        raise ValueError("local solver binary differs from child-profile build manifest")

    inventory = load(EXP / "input/proof-witness-inventory.json")
    if len(inventory["sources"]) != 2 or any(source_item["receipt_trusted_leaves"] != 0
                                             for source_item in inventory["sources"]):
        raise ValueError("proof inventory is not the expected two trusted-leaf-free inputs")
    source_audits = []
    for source_item in inventory["sources"]:
        certificate = ROOT / source_item["certificate_path"]
        receipt_path = ROOT / source_item["receipt_path"]
        if sha256(certificate) != source_item["certificate_sha256"]:
            raise ValueError(f"proof certificate hash mismatch: {certificate}")
        if sha256(receipt_path) != source_item["receipt_sha256"]:
            raise ValueError(f"independent receipt hash mismatch: {receipt_path}")
        receipt = load(receipt_path)
        if receipt.get("trusted_leaves") != 0 or receipt.get("nodes") != source_item["receipt_nodes"]:
            raise ValueError(f"independent receipt boundary mismatch: {receipt_path}")
        if any(root["verdict"] != 2 for root in receipt["roots"]):
            raise ValueError(f"independent receipt does not report all roots LOSS: {receipt_path}")
        source_audits.append({"certificate_sha256": source_item["certificate_sha256"],
                              "receipt_sha256": source_item["receipt_sha256"],
                              "nodes": receipt["nodes"], "edges": receipt["edges"],
                              "trusted_leaves": receipt["trusted_leaves"]})
    if any(sum(len(root["all_stored_s6_loss_candidates"]) for root in source_item["roots"]) < 3
           for source_item in inventory["sources"]):
        raise ValueError("proof inventory is missing stored S6 witness candidates")

    comparison_path = EXP / "input/comparison-schedule.json"
    comparison = load(comparison_path)
    if sha256(comparison_path) != "b1cbb0930d594bdac9d1fd63975d53b68c4b2c37829bd470c34d945e6a4ca36d":
        raise ValueError("frozen S5 comparison schedule hash mismatch")
    boundary_path = ROOT / comparison["independent_boundary"]["path"]
    if sha256(boundary_path) != comparison["independent_boundary"]["sha256"]:
        raise ValueError("pinned current-S4 boundary audit hash mismatch")
    boundary = load(boundary_path)
    expected_boundary = {"LOSS": 40, "WIN": 0, "UNKNOWN": 66}
    if boundary["target_s4_after"] != expected_boundary or boundary["unresolved_third_moves"] != [100, 108]:
        raise ValueError("current-S4 boundary no longer matches the frozen 40/0/66 input")

    stage1 = load(EXP / "output/stage1-v2-6m/summary.json")
    if stage1["solver_binary_sha256"] != build["binary_sha256"]:
        raise ValueError("stage1-v2 binary differs from child-profile build")
    if (stage1["schedule_path"] != comparison_path.relative_to(ROOT).as_posix()
            or stage1["schedule_sha256"] != sha256(comparison_path)):
        raise ValueError("stage1-v2 does not use the frozen comparison schedule")
    counts = {}
    for arm in ("A", "B", "C1", "C2"):
        rows = [row for run in stage1["per_run_results"][arm] for row in run["rows"]]
        counts[arm] = {"LOSS": sum(row["verdict"] == 2 for row in rows),
                       "WIN": sum(row["verdict"] == 1 for row in rows),
                       "UNKNOWN": sum(row["verdict"] == 0 for row in rows),
                       "nodes": sum(row["nodes"] for row in rows)}
    if counts["A"]["LOSS"] != 3 or counts["B"]["LOSS"] != 4:
        raise ValueError(f"known-root A/B replays differ from the fixed outcomes: {counts}")
    if counts["C1"]["LOSS"] or counts["C2"]["LOSS"]:
        raise ValueError(f"blind arms unexpectedly changed from the recorded LOSS count: {counts}")

    direct = load(EXP / "output/direct-s5-child-profile-6m/summary.json")
    attribution = []
    for row in direct["rows"]:
        if row["root_node"] + row["preceding_sibling_nodes"] + row["decisive_s6_nodes"] != row["total_nodes"]:
            raise ValueError(f"S5 root/child node attribution does not sum: {row['target_id']}")
        if any(row["preceding_sibling_verdicts"][v] for v in ("LOSS", "UNKNOWN")):
            raise ValueError(f"a pre-witness S6 child was not an exact WIN: {row['target_id']}")
        attribution.append({"target_id": row["target_id"], "total_nodes": row["total_nodes"],
                            "preceding_sibling_nodes": row["preceding_sibling_nodes"],
                            "decisive_s6_nodes": row["decisive_s6_nodes"]})

    known_s6 = load(EXP / "output/known-s6-costs-v2-6m/summary.json")
    order = load(EXP / "output/known-witness-order-v2-6m/summary.json")
    if known_s6["solver_binary_sha256"] != build["binary_sha256"] or order["solver_binary_sha256"] != build["binary_sha256"]:
        raise ValueError("comparison arms do not use the same binary")
    baseline_path = ROOT / order["stage1_count_order_reference"]
    if sha256(baseline_path) != order["stage1_count_order_reference_sha256"]:
        raise ValueError("order study COUNT baseline hash mismatch")
    order_outcomes = {order_name: dict(aggregates["verdict_counts"])
                      for order_name, aggregates in order["order_aggregates"].items()}
    if any(aggregates["verdict_counts"]["UNKNOWN"] != 4
           or aggregates["total_nodes"] != 24_000_000
           for aggregates in order["order_aggregates"].values()):
        raise ValueError(f"order results differ from the fixed 4x6M cap: {order_outcomes}")

    output_dirs = ["stage1-6m", "stage1-v2-6m", "direct-s5-child-profile-6m",
                   "known-s6-costs-v2-6m", "known-witness-order-6m",
                   "known-witness-order-v2-6m"]
    manifests = [verify_output_manifest(path) for path in output_dirs]
    manifests += [verify_profile_regression(path)
                  for path in ("profile-regression-v1", "profile-regression-v2", "profile-regression-v4")]
    receipt = load(EXP / "output/profile-regression-v4/receipt.json")
    if len(receipt["assertions"]) < 5:
        raise ValueError("profile regression receipt is incomplete")
    result = {
        "schema": "n11-s5-loss-cost-drivers-audit-v1",
        "solver_source_sha256": build["source_sha256"],
        "solver_binary_sha256": build["binary_sha256"],
        "current_s4_boundary": {"path": comparison["independent_boundary"]["path"],
                                 "sha256": sha256(boundary_path), "counts": expected_boundary,
                                 "unresolved_third_moves": [100, 108]},
        "inventory_sources": [{"group": item["source_group"], **source_audit}
                              for item, source_audit in zip(inventory["sources"], source_audits)],
        "same_binary_outcomes": counts,
        "root_cost_attribution": attribution,
        "known_witness_order_outcomes": order_outcomes,
        "profile_regression_receipt_sha256": sha256(EXP / "output/profile-regression-v4/receipt.json"),
        "verified_output_manifests": manifests,
        "interpretation": "Solver results are measurements only; independent outcome facts remain those in the pinned terminal-only DAG receipts.",
    }
    out = args.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"audit": out.relative_to(ROOT).as_posix(), "sha256": sha256(out),
                      "same_binary_outcomes": counts, "root_cost_attribution": attribution}, sort_keys=True))


if __name__ == "__main__":
    main()

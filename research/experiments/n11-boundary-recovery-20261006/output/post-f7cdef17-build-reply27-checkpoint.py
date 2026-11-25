#!/usr/bin/env python3
"""Build a compact hash-bound report for the f7cdef17 exact S5 WIN probe."""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
RUN = ROOT / ".local/n11/dual-tight-ready-1297177430172106752-0-probe8"
PREFIX = "post-f7cdef17-"
BASE = "f7cdef1714ca417a2201b68beb5a18b4b33f8fd9"
CLASS = [1297177430172106752, 0]
REPORT = OUT / f"{PREFIX}reply27-checkpoint-report.json"
SOURCE_MANIFEST = OUT / f"{PREFIX}reply27-checkpoint-source-manifest.json"
ENVIRONMENT = OUT / f"{PREFIX}optimizer-environment.json"
INVENTORY = OUT / f"{PREFIX}reply27-checkpoint-artifact-hashes.json"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(resolved)


def record(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"missing checkpoint source: {path}")
    return {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    if any(p.exists() for p in (REPORT, SOURCE_MANIFEST, ENVIRONMENT, INVENTORY)):
        raise SystemExit("refusing to overwrite an existing checkpoint report or inventory")

    paths = {
        "class_before": OUT / "post-f7cdef17-next-class-1297177430172106752-0-boundary-audit.json",
        "schedule": OUT / "post-f7cdef17-next-class-1297177430172106752-0-probe8.csv",
        "schedule_manifest": OUT / "post-f7cdef17-next-class-1297177430172106752-0-probe8-manifest.json",
        "full_history": OUT / "post-f7cdef17-next-class-1297177430172106752-0-raw-history-baseline.json",
        "probe_history": OUT / "post-f7cdef17-next-class-1297177430172106752-0-probe8-raw-history-current.json",
        "strict_preflight": OUT / "post-f7cdef17-next-class-1297177430172106752-0-probe8-strict-preflight.json",
        "saved_s6_summary": OUT / "post-f7cdef17-next-class-1297177430172106752-0-probe8-saved-s6-summary.json",
        "saved_s6_detail": OUT / "post-f7cdef17-next-class-1297177430172106752-0-probe8-saved-s6-full.json.gz",
        "saved_s6_delta": OUT / "post-f7cdef17-next-class-1297177430172106752-0-probe8-saved-s6-derived-s5.cache",
        "raw_all": OUT / f"{PREFIX}next-class-{CLASS[0]}-{CLASS[1]}-probe8-early-win-raw-all.csv",
        "raw_exact": OUT / f"{PREFIX}next-class-{CLASS[0]}-{CLASS[1]}-probe8-early-win-raw-exact.csv",
        "exact_delta": OUT / f"{PREFIX}next-class-{CLASS[0]}-{CLASS[1]}-probe8-early-win-new-exact-s5.cache",
        "merged_cache": OUT / f"{PREFIX}next-class-{CLASS[0]}-{CLASS[1]}-probe8-early-win-merged-s5.cache",
        "merge_receipt": OUT / f"{PREFIX}next-class-{CLASS[0]}-{CLASS[1]}-probe8-early-win-merge-receipt.json",
        "runner_summary": OUT / f"{PREFIX}next-class-{CLASS[0]}-{CLASS[1]}-probe8-early-win-runner-summary.json",
        "collected_summary": OUT / f"{PREFIX}next-class-{CLASS[0]}-{CLASS[1]}-probe8-early-win-summary.json",
        "class_audit": OUT / f"{PREFIX}next-class-{CLASS[0]}-{CLASS[1]}-probe8-early-win-class-boundary-audit.json",
        "history_audit": OUT / f"{PREFIX}next-class-{CLASS[0]}-{CLASS[1]}-probe8-early-win-saved-history-audit.json",
        "cardinality": OUT / f"{PREFIX}after-class-win-cardinality.json",
        "cover": OUT / f"{PREFIX}after-class-win-cover.json",
        "refined_repair": OUT / f"{PREFIX}after-class-win-repair-refined.json",
        "ranking": OUT / f"{PREFIX}after-class-win-ranking.json",
        "ranking_targets": OUT / f"{PREFIX}after-class-win-ranking-targets.csv",
        "ranking_sources": OUT / f"{PREFIX}after-class-win-ranking-sources.json",
    }
    data = {name: read_json(path) for name, path in paths.items() if path.suffix == ".json"}
    runner = data["runner_summary"]
    merge = data["merge_receipt"]
    boundary = data["class_audit"]["boundary"]
    history = data["history_audit"]
    cardinality = data["cardinality"]
    repair = data["refined_repair"]
    ranking = data["ranking"]

    expected_counts = {"LOSS": 8, "WIN": 2, "UNKNOWN": 92}
    if boundary["canonical_children"] != 102 or boundary["status_counts"] != expected_counts:
        raise SystemExit(f"class boundary mismatch: {boundary.get('canonical_children')} {boundary.get('status_counts')}")
    if history["verdict_conflict_count"] != 0 or history["status_counts"] != expected_counts:
        raise SystemExit("saved-history cross-check disagrees with geometry/cache boundary")
    if {tuple(row["key"]) for row in boundary["children"] if row["verdict"] == 1} != {
        (1297177430172106752, 64), (1297177430172106880, 0)
    }:
        raise SystemExit("exact WIN witness keys differ from the verified geometry boundary")
    if runner["scheduled"] != 8 or runner["started"] != 5 or runner["new_exact"] != 5:
        raise SystemExit("probe did not preserve the expected early-stop semantics")
    if runner["new_win"] != 2 or runner["new_loss"] != 3 or runner["not_dispatched_count"] != 3:
        raise SystemExit("probe verdict or dispatch counts mismatch")
    if merge["merged"]["rows"] != 5414 or merge["merged"]["WIN"] != 140 or merge["merged"]["LOSS"] != 5274:
        raise SystemExit("merged exact cache totals mismatch")
    if cardinality["class_status_counts"] != {"LOSS": 30, "UNKNOWN": 3106, "WIN": 248}:
        raise SystemExit("global s4 class status totals mismatch")
    if cardinality["secured_vertices"] != 114 or cardinality["uncovered_vertices"] != 5:
        raise SystemExit("secured vertex totals mismatch")
    if cardinality["minimum_additional_classes"] != 2 or cardinality["rational_dual_total"] != "2":
        raise SystemExit("integer cover and rational dual no longer agree at two")
    next_target = ranking["next_target"]
    if next_target["key"] != [10376293541461626880, 67108864] or next_target["unknown_s5"] != 97:
        raise SystemExit("reoptimized next target differs from expected dual-tight rank 1")

    environment = {
        "schema": "n11-reply27-optimizer-environment-v1",
        "python": __import__("sys").version,
        "platform": __import__("platform").platform(),
        "numpy": importlib.metadata.version("numpy"),
        "scipy": importlib.metadata.version("scipy"),
        "run_mode": "uv run --locked --with numpy --with scipy",
    }
    ENVIRONMENT.write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = {
        "schema": "n11-reply27-finite-checkpoint-v1",
        "checkpoint_base_main": BASE,
        "root": [60, 27],
        "processed_class": {
            "key": CLASS,
            "status": "WIN",
            "canonical_s5_children": 102,
            "boundary_status_counts": expected_counts,
            "exact_win_witnesses": [[1297177430172106752, 64], [1297177430172106880, 0]],
            "geometry_audit_passed": True,
            "saved_history_conflicts": history["verdict_conflict_count"],
            "unexplored_after_early_win": 92,
        },
        "s5_probe": {
            "budget_per_target": runner["budget"],
            "scheduled": runner["scheduled"],
            "started": runner["started"],
            "completed_exact": runner["new_exact"],
            "verdicts": {"LOSS": runner["new_loss"], "WIN": runner["new_win"], "UNKNOWN": runner["completed_unknown"]},
            "nodes": runner["nodes_all_completed_rows"],
            "workers": runner["workers"],
            "not_dispatched": runner["not_dispatched"],
            "stop_reason": runner["stop_reason"],
        },
        "exact_s5_cache": {
            "path": rel(paths["merged_cache"]),
            "sha256": merge["merged"]["sha256"],
            "entries": merge["merged"]["rows"],
            "WIN": merge["merged"]["WIN"],
            "LOSS": merge["merged"]["LOSS"],
            "conflict": merge["merged"]["conflict"],
            "new_exact_rows": merge["delta"]["rows"],
        },
        "saved_history_audit": {
            "files_scanned": history["scanned_files"],
            "exact_evidence_records_for_boundary": history["exact_evidence_records"],
            "same_budget_unknown_keys": history["same_budget_unknown_child_keys"],
            "conflicts": history["verdict_conflict_count"],
        },
        "s4_classes": cardinality["class_status_counts"],
        "secured_third_moves": cardinality["secured_vertices"],
        "remaining_third_moves": cardinality["uncovered_vertices"],
        "minimum_additional_classes": cardinality["minimum_additional_classes"],
        "rational_dual": cardinality["rational_dual_total"],
        "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
        "repair": {
            "classes": repair["repair_classes"],
            "distinct_unknown_s5": repair["refined_unique_unknown_s5"],
            "selected": repair["repair_selected"],
        },
        "next_target": next_target,
        "s6_descent": 0,
        "reverse_propagated_s5_loss": 0,
        "proof_status": {"reply27_root": "UNKNOWN", "empty_11x11": "UNKNOWN"},
        "report_source_manifest": rel(SOURCE_MANIFEST),
        "artifact_inventory": rel(INVENTORY),
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    input_sources = [
        paths[name] for name in paths
        if name not in {"ranking_targets", "ranking_sources"}
    ]
    input_sources += [
        OUT / "post-cddcf64c-next-class-1297036761403228160-0-probe8-completed-merged-s5.cache",
        OUT / "post-cddcf64-next96-conditional-s6-cover.csv",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_class_local.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/refine_cache_aware_reply27_cover.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
        ROOT / ".local/n11/reply27-probe9/dfpn.exe",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/output/post-f7cdef17-collect-early-win-drained.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/output/post-f7cdef17-merge-probe8-exact-cache.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/output/post-f7cdef17-audit-target-boundary-history.py",
        Path(__file__),
    ]
    input_sources += sorted(path for path in RUN.rglob("*") if path.is_file())
    sources = {item["path"]: item for item in (record(path) for path in input_sources)}
    source_doc = {
        "schema": "n11-reply27-checkpoint-source-manifest-v1",
        "checkpoint_base_main": BASE,
        "report": record(REPORT),
        "environment": record(ENVIRONMENT),
        "source_count": len(sources),
        "sources": [sources[key] for key in sorted(sources)],
    }
    SOURCE_MANIFEST.write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    artifact_paths = sorted(
        path for path in OUT.glob(f"{PREFIX}*")
        if path.is_file() and path != INVENTORY
    )
    artifact_paths += [paths["merged_cache"], paths["exact_delta"], paths["raw_exact"], REPORT, SOURCE_MANIFEST, ENVIRONMENT]
    artifacts = {item["path"]: item for item in (record(path) for path in artifact_paths)}
    parent_inventory = OUT / "post-cddcf64c-reply27-checkpoint-artifact-hashes-v3.json"
    inventory = {
        "schema": "n11-reply27-checkpoint-artifact-inventory-v1",
        "checkpoint": "post-f7cdef17 exact S5 WIN and reoptimized dual-tight repair",
        "created_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "main_commit_at_inventory": BASE,
        "parent_inventory": record(parent_inventory),
        "artifact_count": len(artifacts),
        "artifacts": [artifacts[key] for key in sorted(artifacts)],
        "source_count": len(sources),
        "manifested_sources": [sources[key] for key in sorted(sources)],
        "missing_sources": [],
        "mismatched_sources": [],
    }
    INVENTORY.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    missing: list[str] = []
    mismatched: list[str] = []
    for item in inventory["artifacts"] + inventory["manifested_sources"] + [inventory["parent_inventory"]]:
        path = ROOT / item["path"] if not Path(item["path"]).is_absolute() else Path(item["path"])
        if not path.is_file():
            missing.append(item["path"])
        elif path.stat().st_size != item["bytes"] or sha(path) != item["sha256"]:
            mismatched.append(item["path"])
    inventory["missing_sources"] = missing
    inventory["mismatched_sources"] = mismatched
    inventory["verification"] = {
        "algorithm": "SHA-256",
        "checked_artifacts": len(inventory["artifacts"]),
        "checked_sources": len(inventory["manifested_sources"]) + 1,
        "missing": len(missing),
        "mismatched": len(mismatched),
    }
    INVENTORY.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if missing or mismatched:
        raise SystemExit(json.dumps({"missing": missing, "mismatched": mismatched}, indent=2))
    print(json.dumps({
        "report": rel(REPORT), "report_sha256": sha(REPORT),
        "source_manifest": rel(SOURCE_MANIFEST), "source_count": len(sources),
        "source_manifest_sha256": sha(SOURCE_MANIFEST),
        "artifact_inventory": rel(INVENTORY), "artifact_count": len(artifacts),
        "inventory_sha256": sha(INVENTORY),
        "missing": len(missing), "mismatched": len(mismatched),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

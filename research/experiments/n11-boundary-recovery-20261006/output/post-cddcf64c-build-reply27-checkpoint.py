#!/usr/bin/env python3
"""Build a hash-bound reply27 checkpoint report and inventory."""
from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.metadata
import json
import platform
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-cddcf64c-"
BASE_MAIN = "cddcf64ccdd110eb6bfb535aaaa4b96a0f73fa43"
REPORT = OUT / "post-cddcf64c-reply27-checkpoint-report.json"
SOURCE_MANIFEST = OUT / "post-cddcf64c-reply27-checkpoint-source-manifest.json"
OPTIMIZER_ENV = OUT / "post-cddcf64c-optimizer-environment.json"
INVENTORY = OUT / "post-cddcf64c-reply27-checkpoint-artifact-hashes-v3.json"
PARENT_INVENTORY = OUT / "post-d18e1cc7-reply27-checkpoint-artifact-hashes-v2.json"
CLASS = "1297036761403228160-0"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    path = path.resolve()
    try:
        return path.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def resolve(value: str) -> Path:
    path = Path(value.replace("\\", "/"))
    return path if path.is_absolute() else ROOT / path


def record(path: Path) -> dict[str, Any]:
    path = path.resolve()
    if not path.is_file():
        raise SystemExit(f"artifact/source missing: {path}")
    return {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def load_json(path: Path) -> Any:
    if path.name.lower().endswith(".json.gz"):
        return json.loads(gzip.decompress(path.read_bytes()))
    return json.loads(path.read_text(encoding="utf-8"))


def walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def add(table: dict[str, dict[str, Any]], item: dict[str, Any]) -> None:
    old = table.get(item["path"])
    if old is not None and old != item:
        raise SystemExit(f"conflicting inventory record: {item['path']}")
    table[item["path"]] = item


def rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return [row for row in csv.reader(stream)
                if row and not row[0].lstrip().startswith("#")]


def main() -> int:
    outputs = [REPORT, SOURCE_MANIFEST, OPTIMIZER_ENV, INVENTORY]
    if any(path.exists() for path in outputs):
        raise SystemExit("refusing to overwrite checkpoint report, manifest, environment, or inventory")
    if not PARENT_INVENTORY.is_file():
        raise SystemExit(f"latest accepted parent inventory is absent: {PARENT_INVENTORY}")

    def p(suffix: str) -> Path:
        return OUT / f"post-cddcf64c-next-class-{CLASS}{suffix}"

    base_cache = OUT / "post-d18e1cc7-next-class-1297318167660462080-0-probe8-completed-merged-s5.cache"
    collected = p("-probe8-completed")
    paths = {
        "boundary_before": p("-boundary-audit.json"),
        "targets_full": p("-unknown-s5-targets.csv"),
        "target_manifest": p("-unknown-s5-manifest.json"),
        "raw_full_baseline": p("-raw-history-baseline.json"),
        "raw_full_current": p("-raw-history-current.json"),
        "raw_full_coverage": p("-raw-history-coverage.json"),
        "saved_s6_full_summary": p("-saved-s6-summary.json"),
        "saved_s6_full_detail": p("-saved-s6-full.json.gz"),
        "saved_s6_full_delta": p("-saved-s6-derived-s5.cache"),
        "schedule": p("-probe8-manifest.json"),
        "scheduled_targets": p("-probe8.csv"),
        "raw_probe_baseline": p("-probe8-raw-history-baseline.json"),
        "raw_probe_current": p("-probe8-raw-history-current.json"),
        "raw_probe_coverage": p("-probe8-raw-history-coverage.json"),
        "saved_s6_probe_summary": p("-probe8-saved-s6-summary.json"),
        "saved_s6_probe_detail": p("-probe8-saved-s6-full.json.gz"),
        "saved_s6_probe_delta": p("-probe8-saved-s6-derived-s5.cache"),
        "strict_preflight": p("-probe8-strict-preflight.json"),
        "boundary_after": collected.with_name(collected.name + "-class-boundary-audit.json"),
        "cardinality": collected.with_name(collected.name + "-cardinality.json"),
        "repair": collected.with_name(collected.name + "-repair.json"),
        "repair_targets": collected.with_name(collected.name + "-repair-targets.csv"),
        "repair_refined": collected.with_name(collected.name + "-repair-refined.json"),
        "ranking": collected.with_name(collected.name + "-ranking.json"),
        "ranking_targets": collected.with_name(collected.name + "-ranking-targets.csv"),
        "ranking_sources": collected.with_name(collected.name + "-ranking-sources.json"),
        "new_cache": collected.with_name(collected.name + "-new-exact-s5.cache"),
        "merged_cache": collected.with_name(collected.name + "-merged-s5.cache"),
        "raw_all": collected.with_name(collected.name + "-raw-all.csv"),
        "raw_exact": collected.with_name(collected.name + "-raw-exact.csv"),
        "exact_targets": collected.with_name(collected.name + "-exact-targets.csv"),
        "summary": collected.with_name(collected.name + "-summary.json"),
        "runner_summary": collected.with_name(collected.name + "-runner-summary.json"),
        "merge_receipt": collected.with_name(collected.name + "-merge-receipt.json"),
        "collector_sources": collected.with_name(collected.name + "-sources.json"),
        "probe_input_builder": ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/prepare_dual_tight_ready_subset_probe.py",
        "boundary_auditor": ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        "raw_auditor": ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py",
        "s6_auditor": ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py",
        "cardinality_script": ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        "cover_script": ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
        "refine_script": ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/refine_cache_aware_reply27_cover.py",
        "ranking_script": ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
        "solver": ROOT / ".local/n11/reply27-probe9/dfpn.exe",
        "solver_source": ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
        "runner": ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_class_local.py",
        "geometry_cache": OUT / "post-9dcb11b6-reply27-geometry-v1.json.gz",
        "base_cache": base_cache,
    }
    absent = [name for name, path in paths.items() if not path.is_file()]
    if absent:
        raise SystemExit(f"required checkpoint inputs absent: {absent}")

    cache = {}
    verdict_counts: Counter[str] = Counter()
    for line_no, row in enumerate(rows(paths["merged_cache"]), 1):
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid merged exact S5 cache row {line_no}: {row}")
        key = (int(row[1]), int(row[2]))
        verdict = int(row[4])
        if verdict not in (1, 2) or key in cache:
            raise SystemExit(f"invalid/duplicate exact cache key {key}")
        cache[key] = verdict
        verdict_counts["WIN" if verdict == 1 else "LOSS"] += 1

    summary = load_json(paths["summary"])
    runner = load_json(paths["runner_summary"])
    merge = load_json(paths["merge_receipt"])
    before = load_json(paths["boundary_before"])
    after = load_json(paths["boundary_after"])
    cardinality = load_json(paths["cardinality"])
    repair = load_json(paths["repair"])
    refined = load_json(paths["repair_refined"])
    ranking = load_json(paths["ranking"])
    raw_full = load_json(paths["raw_full_current"])
    raw_probe = load_json(paths["raw_probe_current"])
    s6_full = load_json(paths["saved_s6_full_summary"])
    s6_probe = load_json(paths["saved_s6_probe_summary"])
    strict = load_json(paths["strict_preflight"])

    boundary_counts = Counter({"WIN": 0, "LOSS": 0, "UNKNOWN": 0})
    wins = []
    for child in after["boundary"]["children"]:
        verdict = child["verdict"]
        state = {1: "WIN", 2: "LOSS", None: "UNKNOWN"}[verdict]
        boundary_counts[state] += 1
        if verdict == 1:
            wins.append(tuple(child["key"]))
        if verdict in (1, 2) and cache.get(tuple(child["key"])) != verdict:
            raise SystemExit(f"boundary exact verdict missing from merged cache: {child['key']}")

    if (len(cache) != 5409 or verdict_counts != Counter({"LOSS": 5271, "WIN": 138})
            or merge.get("conflicts") != 0 or merge.get("merged_cache", {}).get("rows") != len(cache)
            or summary.get("class_status_from_exact_witness") != "WIN"
            or summary.get("exact_replay_counts") != {"LOSS": 6, "UNKNOWN": 0, "WIN": 2}
            or summary.get("nodes_all_completed_rows") != 35894680
            or runner.get("not_dispatched") != []
            or after["boundary"].get("canonical_children") != 102
            or len(after["boundary"].get("children", [])) != 102
            or boundary_counts != Counter({"LOSS": 12, "WIN": 2, "UNKNOWN": 88})
            or len(wins) != 2 or after["cache"].get("conflicts") != 0
            or before["boundary"].get("canonical_children") != 102
            or before["boundary"].get("status_counts") != {"LOSS": 6, "UNKNOWN": 96, "WIN": 0}
            or raw_full.get("prior_exact") or raw_full.get("prior_unknown_same_budget_or_higher")
            or raw_full.get("exact_verdict_conflicts") or len(raw_full.get("dispatch_ready_keys", [])) != 96
            or raw_probe.get("prior_exact") or raw_probe.get("prior_unknown_same_budget_or_higher")
            or raw_probe.get("exact_verdict_conflicts") or len(raw_probe.get("dispatch_ready_keys", [])) != 8
            or s6_full.get("cache_comparison", {}).get("new_exact") != 0
            or s6_full.get("cache_comparison", {}).get("unknown_parents") != 96
            or s6_full.get("source_audit", {}).get("canonical_s6_count") != 4467
            or s6_full.get("source_audit", {}).get("exact_conflict_count") != 0
            or s6_full.get("source_audit", {}).get("source_hashes_validated") is not True
            or s6_probe.get("cache_comparison", {}).get("new_exact") != 0
            or s6_probe.get("cache_comparison", {}).get("unknown_parents") != 8
            or s6_probe.get("source_audit", {}).get("canonical_s6_count") != 4467
            or s6_probe.get("source_audit", {}).get("exact_conflict_count") != 0
            or s6_probe.get("source_audit", {}).get("source_hashes_validated") is not True
            or strict.get("target_count") != 8
            or strict.get("blocked_same_or_higher_budget_unknown_keys")
            or strict.get("saved_s6", {}).get("conflicts") != 0
            or strict.get("historical_source_coverage", {}).get("status") != "PASS"):
        raise SystemExit("exact result, geometry, or preflight checkpoint consistency check failed")

    optimizer_environment = {
        "schema": "n11-reply27-optimizer-environment-v1",
        "python": platform.python_version(),
        "numpy": importlib.metadata.version("numpy"),
        "scipy": importlib.metadata.version("scipy"),
        "cardinality_command_environment": "uv run --no-project --with scipy --with numpy",
        "main_commit": BASE_MAIN,
    }
    OPTIMIZER_ENV.write_text(json.dumps(optimizer_environment, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8", newline="\n")

    report = {
        "schema": "n11-reply27-finite-checkpoint-v1",
        "checkpoint_base_main": BASE_MAIN,
        "root": [60, 27],
        "exact_s5_cache": {
            "path": rel(paths["merged_cache"]), "entries": len(cache),
            "WIN": verdict_counts["WIN"], "LOSS": verdict_counts["LOSS"],
            "conflict": merge.get("conflicts"), "sha256": sha(paths["merged_cache"]),
            "new_rows": len(rows(paths["new_cache"])),
        },
        "s4_classes": cardinality["class_status_counts"],
        "secured_third_moves": cardinality["secured_vertices"],
        "remaining_third_moves": cardinality["uncovered_vertices"],
        "minimum_additional_classes": cardinality["minimum_additional_classes"],
        "rational_dual": cardinality["rational_dual_total"],
        "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
        "dual_positive_weights": cardinality["dual_positive_weights"],
        "processed_class": {
            "key": [1297036761403228160, 0],
            "status": "WIN",
            "canonical_s5_children": 102,
            "coverage_vertices": after["class"]["coverage_vertices"],
            "boundary_status_counts": dict(sorted(boundary_counts.items())),
            "exact_win_witnesses": [list(k) for k in sorted(wins)],
            "geometry_audit_passed": after["boundary"].get("status") == "WIN",
            "unexplored_children_after_probe": 88,
        },
        "s5_probe": {
            "scheduled": 8, "completed": summary["completed_targets"],
            "budget_per_target": 15000000, "workers": runner["workers"],
            "verdicts": summary["exact_replay_counts"],
            "nodes_exact": summary["nodes_exact"], "nodes_all_rows": summary["nodes_all_completed_rows"],
            "additional_class_siblings_dispatched": 0,
        },
        "raw_history_preflight": {
            "full_class_targets": raw_full.get("targets", {}).get("count"),
            "full_class_csv_files": raw_full.get("csv_files_examined"),
            "full_class_prior_exact": len(raw_full.get("prior_exact", {})),
            "full_class_same_budget_unknown": len(raw_full.get("prior_unknown_same_budget_or_higher", [])),
            "full_class_ready": len(raw_full.get("dispatch_ready_keys", [])),
            "probe_csv_files": raw_probe.get("csv_files_examined"),
            "probe_prior_exact": len(raw_probe.get("prior_exact", {})),
            "probe_same_budget_unknown": len(raw_probe.get("prior_unknown_same_budget_or_higher", [])),
            "probe_ready": len(raw_probe.get("dispatch_ready_keys", [])),
            "conflicts": 0,
        },
        "saved_s6_intersection": {
            "source_files": s6_full["source_audit"]["source_file_count"],
            "canonical_s6_keys": s6_full["source_audit"]["canonical_s6_count"],
            "full_class_parents": 96, "unknown_full_class_parents": 96,
            "probe_parents": 8, "unknown_probe_parents": 8,
            "derived_exact_s5": 0, "conflicts": 0,
        },
        "repair": {
            "classes": refined["repair_classes"],
            "additive_unknown_s5": refined["refined_additive_unknown_s5"],
            "distinct_unknown_s5": refined["refined_unique_unknown_s5"],
            "selected": refined["repair_selected"],
            "claim": "repair classes are scheduling targets and remain UNKNOWN",
        },
        "next_target": ranking["next_target"],
        "optimizer_environment": rel(OPTIMIZER_ENV),
        "proof_status": {"reply27_root": "UNKNOWN", "empty_11x11": "UNKNOWN"},
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")

    # Hash every path mentioned by the new evidence and preserve its raw source SHA.
    sources: dict[str, dict[str, Any]] = {}
    all_new_paths: set[Path] = set()
    for path in OUT.glob(f"{PREFIX}*"):
        if path.is_file() and path not in {SOURCE_MANIFEST, INVENTORY}:
            all_new_paths.add(path.resolve())
        elif path.is_dir():
            all_new_paths.update(item.resolve() for item in path.rglob("*") if item.is_file())

    for artifact in sorted(all_new_paths):
        if artifact.suffix.lower() not in {".json", ".gz"}:
            continue
        try:
            document = load_json(artifact)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, gzip.BadGzipFile):
            continue
        for item in walk(document):
            path_text = item.get("path") or item.get("artifact_path")
            expected = item.get("sha256")
            if not isinstance(path_text, str) or not isinstance(expected, str):
                continue
            source = resolve(path_text)
            item_record = record(source)
            if item_record["sha256"] != expected:
                raise SystemExit(f"manifested source hash mismatch: {item_record['path']}")
            if isinstance(item.get("bytes"), int) and item_record["bytes"] != item["bytes"]:
                raise SystemExit(f"manifested source byte count mismatch: {item_record['path']}")
            add(sources, item_record)

    # Record the preserved per-root exact solver raw outputs and logs in .local too.
    run_dir = ROOT / ".local/n11/dual-tight-ready-1297036761403228160-0-probe8"
    for source in [*run_dir.glob("*.input.csv"), *run_dir.glob("*.out.csv"),
                   *run_dir.glob("*.log"), run_dir / "summary.json",
                   run_dir / "cache-out/new-exact-s5.cache"]:
        if source.is_file():
            add(sources, record(source))
    add(sources, record(Path(__file__).resolve()))

    source_doc = {
        "schema": "n11-reply27-checkpoint-source-manifest-v1",
        "checkpoint_base_main": BASE_MAIN,
        "report": {"path": rel(REPORT), "sha256": sha(REPORT)},
        "source_count": len(sources),
        "sources": [sources[key] for key in sorted(sources)],
        "evidence_manifests": [record(path) for path in sorted(all_new_paths)
                               if path.suffix.lower() in {".json", ".gz"}],
    }
    SOURCE_MANIFEST.write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8", newline="\n")

    parent = json.loads(PARENT_INVENTORY.read_text(encoding="utf-8"))
    artifacts: dict[str, dict[str, Any]] = {}
    manifested_sources: dict[str, dict[str, Any]] = {}
    for item in parent["artifacts"]:
        add(artifacts, item)
    for item in parent["manifested_sources"]:
        add(manifested_sources, item)
    add(artifacts, record(PARENT_INVENTORY))
    for path in sorted(all_new_paths):
        add(artifacts, record(path))
    for item in source_doc["sources"]:
        add(manifested_sources, item)
    for item in source_doc["evidence_manifests"]:
        add(manifested_sources, item)

    missing, mismatched = [], []
    for table in (artifacts, manifested_sources):
        for item in table.values():
            path = resolve(item["path"])
            if not path.is_file():
                missing.append(item["path"])
            elif path.stat().st_size != item["bytes"] or sha(path) != item["sha256"]:
                mismatched.append(item["path"])
    if missing or mismatched:
        raise SystemExit(json.dumps({"missing": missing[:20], "mismatched": mismatched[:20]}))

    inventory = {
        "schema": "n11-reply27-checkpoint-artifact-inventory-v1",
        "checkpoint": "post-cddcf64c exact S5 WIN and reoptimized dual-tight repair",
        "created_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "main_commit_at_inventory": BASE_MAIN,
        "parent_inventory": {
            "path": rel(PARENT_INVENTORY), "sha256": sha(PARENT_INVENTORY),
            "artifact_count": parent["artifact_count"], "source_count": parent["source_count"],
        },
        "artifact_count": len(artifacts),
        "artifacts": [artifacts[key] for key in sorted(artifacts)],
        "source_count": len(manifested_sources),
        "manifested_sources": [manifested_sources[key] for key in sorted(manifested_sources)],
        "missing_sources": missing,
        "mismatched_sources": mismatched,
        "verification": {
            "algorithm": "SHA-256", "checked_artifacts": len(artifacts),
            "checked_sources": len(manifested_sources), "missing": 0, "mismatched": 0,
        },
    }
    INVENTORY.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n",
                         encoding="utf-8", newline="\n")
    print(json.dumps({
        "report": rel(REPORT), "report_sha256": sha(REPORT),
        "source_manifest": rel(SOURCE_MANIFEST), "source_count": len(sources),
        "source_manifest_sha256": sha(SOURCE_MANIFEST),
        "inventory": rel(INVENTORY), "artifact_count": len(artifacts),
        "source_count_total": len(manifested_sources), "missing": 0, "mismatched": 0,
        "inventory_sha256": sha(INVENTORY),
        "s5_cache": {"rows": len(cache), **dict(verdict_counts), "conflicts": 0},
        "s4_classes": cardinality["class_status_counts"],
        "secured": cardinality["secured_vertices"],
        "remaining": cardinality["uncovered_vertices"],
        "minimum_additional_classes": cardinality["minimum_additional_classes"],
        "rational_dual": cardinality["rational_dual_total"],
        "next_target": ranking["next_target"]["key"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

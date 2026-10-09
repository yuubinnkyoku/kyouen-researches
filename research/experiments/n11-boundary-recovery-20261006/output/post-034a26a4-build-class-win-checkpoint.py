#!/usr/bin/env python3
"""Build a hash-bound checkpoint for the 2026-10-09 reply27 class WIN."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-034a26a4-"
BASE_MAIN = "034a26a4c4402cd944568c484a723c34be7795d6"
REPORT = OUT / f"{PREFIX}reply27-checkpoint-report.json"
SOURCE_MANIFEST = OUT / f"{PREFIX}reply27-checkpoint-source-manifest.json"
PARENT_INVENTORY = OUT / "post-f7cdef17-reply27-checkpoint-artifact-hashes.json"
INVENTORY = OUT / f"{PREFIX}reply27-checkpoint-artifact-hashes.json"

CLASS = (10376293541461626880, 67108864)
CACHE = OUT / "post-034a26a4-next-class-10376293541461626880-67108864-probe8-early-win-merged-s5.cache"
DELTA = OUT / "post-034a26a4-next-class-10376293541461626880-67108864-probe8-early-win-new-exact-s5.cache"
RAW = OUT / "post-034a26a4-next-class-10376293541461626880-67108864-probe8-early-win-raw-exact.csv"
BOUNDARY = OUT / "post-034a26a4-next-class-10376293541461626880-67108864-probe8-early-win-class-boundary-audit.json"
RUNNER = OUT / "post-034a26a4-next-class-10376293541461626880-67108864-probe8-early-win-runner-summary.json"
MERGE = OUT / "post-034a26a4-next-class-10376293541461626880-67108864-probe8-early-win-merge-receipt.json"
CARDINALITY = OUT / f"{PREFIX}after-class-win-cardinality.json"
COVER = OUT / f"{PREFIX}after-class-win-cover.json"
REFINED = OUT / f"{PREFIX}after-class-win-repair-refined.json"
RANKING = OUT / f"{PREFIX}after-class-win-ranking.json"
SAVED_HISTORY = OUT / "post-034a26a4-next-class-10376293541461626880-67108864-probe8-early-win-saved-history-audit.json"

USED_SOURCES = [
    "research/experiments/n11-boundary-recovery-20261006/scripts/complete_class_local.py",
    "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
    "research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py",
    "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py",
    "research/experiments/n11-boundary-recovery-20261006/scripts/verify_raw_history_coverage.py",
    "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_probe_preflight.py",
    "research/experiments/n11-boundary-recovery-20261006/scripts/prepare_dual_tight_ready_subset_probe.py",
    "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
    "research/experiments/n11-boundary-recovery-20261006/scripts/merge_dual_tight_resume_outputs.py",
    "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
    "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
    "research/experiments/n11-frontier-selection-20261005/scripts/refine_cache_aware_reply27_cover.py",
    "research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py",
    "research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py",
    "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py",
    "research/experiments/n11-boundary-recovery-20261006/scripts/n11_integer_circle_geometry.py",
    ".local/n11/reply27-probe9/dfpn.exe",
]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
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
        raise SystemExit(f"missing evidence/source: {path}")
    return {"path": relative(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def read_json(path: Path) -> Any | None:
    try:
        if path.name.lower().endswith(".json.gz"):
            return json.loads(gzip.decompress(path.read_bytes()))
        if path.suffix.lower() == ".json":
            return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, gzip.BadGzipFile):
        return None
    return None


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
        raise SystemExit(f"conflicting manifest entries: {item['path']}")
    table[item["path"]] = item


def read_cache(path: Path) -> dict[tuple[int, int], int]:
    values: dict[tuple[int, int], int] = {}
    for line_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid s5 cache row {line_no}: {row}")
        key, verdict = (int(row[1]), int(row[2])), int(row[4])
        if verdict not in (1, 2) or (key in values and values[key] != verdict):
            raise SystemExit(f"invalid/conflicting exact cache row {line_no}: {row}")
        values[key] = verdict
    return values


def main() -> int:
    outputs = [CACHE, DELTA, RAW, BOUNDARY, RUNNER, MERGE, CARDINALITY, COVER, REFINED, RANKING, SAVED_HISTORY]
    for path in [*outputs, PARENT_INVENTORY, *[ROOT / p for p in USED_SOURCES]]:
        if not path.is_file():
            raise SystemExit(f"required evidence is missing: {path}")
    refresh = "--refresh" in sys.argv[1:]
    for path in (REPORT, SOURCE_MANIFEST, INVENTORY):
        if path.exists() and not refresh:
            raise SystemExit(f"refusing to overwrite checkpoint artifact: {path}")

    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    runner = json.loads(RUNNER.read_text(encoding="utf-8"))
    merge = json.loads(MERGE.read_text(encoding="utf-8"))
    cardinality = json.loads(CARDINALITY.read_text(encoding="utf-8"))
    refined = json.loads(REFINED.read_text(encoding="utf-8"))
    ranking = json.loads(RANKING.read_text(encoding="utf-8"))
    history = json.loads(SAVED_HISTORY.read_text(encoding="utf-8"))

    current = read_cache(CACHE)
    delta = read_cache(DELTA)
    counts = Counter(current.values())
    children = {tuple(item["key"]): item["verdict"] for item in boundary["boundary"]["children"]}
    if (tuple(boundary["class"]["key"]) != CLASS or boundary["boundary"]["canonical_children"] != 106
            or boundary["boundary"]["status"] != "WIN"
            or boundary["boundary"]["status_counts"] != {"LOSS": 10, "UNKNOWN": 92, "WIN": 4}
            or any(children.get(key) != verdict for key, verdict in delta.items())):
        raise SystemExit("full canonical geometry/cache audit does not support this WIN checkpoint")
    raw_rows = [row for row in csv.reader(RAW.open(newline="", encoding="utf-8-sig"))
                if row and row[0] == "replay"]
    raw_verdicts = Counter(int(row[6]) for row in raw_rows)
    raw_nodes = sum(int(row[7]) for row in raw_rows)
    if (len(current) != 5419 or counts != Counter({1: 144, 2: 5275})
            or len(delta) != 5 or raw_verdicts != Counter({1: 4, 2: 1})
            or raw_nodes != 44_498_734 or merge["verdict_conflicts"] != 0
            or ranking["minimum_additional_classes"] != 2
            or ranking["rational_dual_total"] != "2"
            or not ranking["dual_certificate_matches_integer_optimum"]):
        raise SystemExit("checkpoint totals failed cross-artifact consistency checks")

    exact_wins = sorted([list(key) for key, verdict in children.items() if verdict == 1])
    repair = [{k: row[k] for k in ("key", "coverage", "uncached_s5")} for row in refined["repair_selected"]]
    report_doc = {
        "schema": "n11-reply27-finite-checkpoint-v1",
        "checkpoint_base_main": BASE_MAIN,
        "created_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": [60, 27],
        "processed_class": {
            "key": list(CLASS), "status": "WIN", "geometry_audit_passed": True,
            "canonical_s5_children": 106,
            "boundary_status_counts": boundary["boundary"]["status_counts"],
            "coverage_vertices": boundary["class"]["coverage_vertices"],
            "exact_win_witnesses": exact_wins,
            "unexplored_after_early_win": 92,
        },
        "s5_probe": {
            "budget_per_target": 15_000_000, "workers": 4, "scheduled": 8,
            "started": 5, "completed_exact": len(raw_rows),
            "verdicts": {"WIN": raw_verdicts[1], "LOSS": raw_verdicts[2], "UNKNOWN": 0},
            "nodes": raw_nodes,
            "not_dispatched": merge["not_dispatched_keys"],
            "stop_reason": "An exact s5 WIN row appeared; no further target was dispatched, active work was drained, and three targets remained undispatched.",
        },
        "exact_s5_cache": {
            "path": relative(CACHE), "entries": len(current), "WIN": counts[1], "LOSS": counts[2],
            "conflict": 0, "new_exact_rows": len(delta), "sha256": sha(CACHE),
        },
        "saved_history_audit": {
            "files_scanned": history.get("scanned_files"),
            "rows_scanned": history.get("parsed_csv_rows"),
            "exact_boundary_keys": history.get("exact_child_keys_with_saved_evidence"),
            "exact_evidence_records": history.get("exact_evidence_records"),
            "same_budget_unknown_keys": history.get("same_budget_unknown_child_keys"),
            "verdict_conflicts": history.get("verdict_conflict_count"),
        },
        "s4_classes": cardinality["class_status_counts"],
        "secured_third_moves": cardinality["secured_vertices"],
        "remaining_third_moves": cardinality["uncovered_vertices"],
        "minimum_additional_classes": cardinality["minimum_additional_classes"],
        "rational_dual": cardinality["rational_dual_total"],
        "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
        "repair": {
            "classes": refined["repair_classes"],
            "distinct_unknown_s5": refined["refined_unique_unknown_s5"],
            "selected": repair,
        },
        "next_target": ranking["next_target"],
        "s6_descent": 0,
        "reverse_propagated_s5_loss": 0,
        "proof_status": {"reply27_root": "UNKNOWN", "empty_11x11": "UNKNOWN"},
        "claim": "This checkpoint establishes the selected s4 class as WIN from exact s5 evidence. It does not classify the reply27 root or the empty board.",
        "source_manifest": relative(SOURCE_MANIFEST),
        "artifact_inventory": relative(INVENTORY),
    }
    REPORT.write_text(json.dumps(report_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    sources: dict[str, dict[str, Any]] = {}
    for value in USED_SOURCES:
        add(sources, record(ROOT / value))
    add(sources, record(Path(__file__).resolve()))
    # Include hash-bound runner inputs, logs and per-target raw outputs.
    for item in runner.get("targets", []):
        for category in ("input", "log", "output"):
            detail = item.get(category)
            if isinstance(detail, dict) and detail.get("path"):
                path = resolve(detail["path"])
                current_record = record(path)
                if detail.get("sha256") != current_record["sha256"]:
                    raise SystemExit(f"runner manifest hash mismatch: {path}")
                add(sources, current_record)
    # Pull in any additional hash-paired source paths embedded in JSON audits.
    for artifact in sorted(OUT.glob(f"{PREFIX}*")):
        if artifact.resolve() in {REPORT.resolve(), SOURCE_MANIFEST.resolve(), INVENTORY.resolve()}:
            continue
        if artifact.is_file() and artifact.suffix.lower() in {".json", ".gz"}:
            document = read_json(artifact)
            if document is None:
                continue
            for item in walk(document):
                path_value, digest = item.get("path"), item.get("sha256")
                if not isinstance(path_value, str) or not isinstance(digest, str):
                    continue
                path = resolve(path_value)
                if path.is_file():
                    current_record = record(path)
                    if current_record["sha256"] != digest:
                        raise SystemExit(f"embedded source hash mismatch: {current_record['path']}")
                    if isinstance(item.get("bytes"), int) and item["bytes"] != current_record["bytes"]:
                        raise SystemExit(f"embedded source size mismatch: {current_record['path']}")
                    add(sources, current_record)

    source_doc = {
        "schema": "n11-reply27-checkpoint-source-manifest-v1",
        "checkpoint_base_main": BASE_MAIN,
        "report": record(REPORT),
        "source_count": len(sources),
        "sources": [sources[key] for key in sorted(sources)],
        "claim": "Hashes bind raw solver evidence, runner inputs/logs, geometry and saved-history audits, exact cache, and analysis sources.",
    }
    SOURCE_MANIFEST.write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    parent = json.loads(PARENT_INVENTORY.read_text(encoding="utf-8"))
    artifacts: dict[str, dict[str, Any]] = {}
    manifest_sources: dict[str, dict[str, Any]] = {}
    for item in parent["artifacts"]:
        add(artifacts, item)
    for item in parent["manifested_sources"]:
        add(manifest_sources, item)
    add(artifacts, record(PARENT_INVENTORY))
    for path in sorted(OUT.glob(f"{PREFIX}*")):
        if path.is_file() and path.resolve() != INVENTORY.resolve():
            add(artifacts, record(path))
    for item in source_doc["sources"]:
        add(manifest_sources, item)
    # Verify all inherited and new entries before writing the inventory.
    for table in (artifacts, manifest_sources):
        for item in table.values():
            path = resolve(item["path"])
            if not path.is_file() or path.stat().st_size != item["bytes"] or sha(path) != item["sha256"]:
                raise SystemExit(f"artifact/source hash mismatch: {item['path']}")

    inventory_doc = {
        "schema": "n11-reply27-checkpoint-artifact-inventory-v1",
        "checkpoint": "post-034a26a4 dual-tight probe8 exact S5 WIN class checkpoint",
        "created_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "main_commit_at_inventory": BASE_MAIN,
        "parent_inventory": {"path": relative(PARENT_INVENTORY), "sha256": sha(PARENT_INVENTORY),
                             "artifact_count": parent["artifact_count"], "source_count": parent["source_count"]},
        "artifact_count": len(artifacts), "artifacts": [artifacts[key] for key in sorted(artifacts)],
        "source_count": len(manifest_sources), "manifested_sources": [manifest_sources[key] for key in sorted(manifest_sources)],
        "missing_sources": [], "mismatched_sources": [],
        "verification": {"algorithm": "SHA-256", "checked_artifacts": len(artifacts),
                         "checked_sources": len(manifest_sources), "missing": 0, "mismatched": 0},
    }
    INVENTORY.write_text(json.dumps(inventory_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"report": relative(REPORT), "source_manifest": relative(SOURCE_MANIFEST),
                      "source_count": source_doc["source_count"], "inventory": relative(INVENTORY),
                      "artifact_count": len(artifacts), "manifested_source_count": len(manifest_sources),
                      "inventory_sha256": sha(INVENTORY), "missing": 0, "mismatched": 0,
                      "processed_class": report_doc["processed_class"],
                      "cache": report_doc["exact_s5_cache"], "global": {"s4_classes": report_doc["s4_classes"],
                      "secured": report_doc["secured_third_moves"], "remaining": report_doc["remaining_third_moves"],
                      "minimum_additional_classes": report_doc["minimum_additional_classes"],
                      "rational_dual": report_doc["rational_dual"], "dual_tight": report_doc["dual_tight"]},
                      "next_target": report_doc["next_target"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

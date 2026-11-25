#!/usr/bin/env python3
"""Build a hash-bound reply27 checkpoint after S6 reverse propagation."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-2f23fcb8-"
BASE_MAIN = "2f23fcb80ae853c93d31ed5d2e0f8d7d25ce757a"
CLASS = (1152921504741065728, 68719476736)
REPORT = OUT / f"{PREFIX}reply27-checkpoint-report.json"
SOURCE_MANIFEST = OUT / f"{PREFIX}reply27-checkpoint-source-manifest.json"
INVENTORY = OUT / f"{PREFIX}reply27-checkpoint-artifact-hashes.json"
PARENT_INVENTORY = OUT / "post-034a26a4-reply27-checkpoint-artifact-hashes.json"
BASE_CACHE = OUT / "post-034a26a4-next-class-10376293541461626880-67108864-probe8-early-win-merged-s5.cache"
CACHE = OUT / "post-2f23fcb8-next98-after-s6-reverse-merged-s5.cache"
BOUNDARY = OUT / "post-2f23fcb8-next98-after-s6-reverse-class-boundary-audit.json"
CARDINALITY = OUT / "post-2f23fcb8-after-s6-reverse-cardinality.json"
COVER = OUT / "post-2f23fcb8-after-s6-reverse-cover.json"
REFINED = OUT / "post-2f23fcb8-after-s6-reverse-repair-refined.json"
RANKING = OUT / "post-2f23fcb8-after-s6-reverse-ranking.json"
S6_SUMMARY = OUT / "post-2f23fcb8-next98-round2-unknown-parent-s6-descent-summary.json"
REVERSE_AUDIT = OUT / "post-2f23fcb8-next98-round2-s6-reverse-audit.json"
MERGE = OUT / "post-2f23fcb8-next98-after-s6-reverse-merge-receipt.json"
S5_SUMMARIES = [
    OUT / "post-2f23fcb8-next98-probe8-summary.json",
    OUT / "post-2f23fcb8-next98-probe-next8-summary.json",
    OUT / "post-2f23fcb8-next98-probe-next8-round2-summary.json",
]
MAIN_CONTEXT = [
    OUT / "post-b4d9b6a9-next98-conditional-s6-cover-audit.json",
    OUT / "post-b4d9b6a9-next98-conditional-s6-cover.csv",
    OUT / "post-b4d9b6a9-next98-key-precision-correction.md",
]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def resolve(value: str) -> Path:
    normalized = value.replace("\\", "/")
    path = Path(normalized)
    return path if path.is_absolute() else ROOT / path


def record(path: Path) -> dict[str, Any]:
    path = path.resolve()
    if not path.is_file():
        raise SystemExit(f"missing evidence/source: {path}")
    return {"path": relative(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def add(table: dict[str, dict[str, Any]], item: dict[str, Any]) -> None:
    old = table.get(item["path"])
    if old is not None and old != item:
        raise SystemExit(f"conflicting manifest entries: {item['path']}")
    table[item["path"]] = item


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def read_cache(path: Path) -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise SystemExit(f"invalid s5 cache row {line_no}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if verdict not in (1, 2) or (key in result and result[key] != verdict):
                raise SystemExit(f"invalid/conflicting exact cache row {line_no}: {row}")
            result[key] = verdict
    return result


def verify_record(item: dict[str, Any]) -> None:
    path = resolve(item["path"])
    if (not path.is_file() or path.stat().st_size != item["bytes"]
            or sha(path) != item["sha256"]):
        raise SystemExit(f"artifact/source hash mismatch: {item['path']}")


def main() -> int:
    fixed = [PARENT_INVENTORY, BASE_CACHE, CACHE, BOUNDARY, CARDINALITY, COVER,
             REFINED, RANKING, S6_SUMMARY, REVERSE_AUDIT, MERGE, *S5_SUMMARIES,
             *MAIN_CONTEXT]
    for path in fixed:
        if not path.is_file():
            raise SystemExit(f"required checkpoint evidence is missing: {path}")
    if any(path.exists() for path in (REPORT, SOURCE_MANIFEST, INVENTORY)):
        raise SystemExit("refusing to overwrite an existing checkpoint artifact")

    parent = read_json(PARENT_INVENTORY)
    for table_name in ("artifacts", "manifested_sources"):
        for item in parent[table_name]:
            verify_record(item)

    base, current = read_cache(BASE_CACHE), read_cache(CACHE)
    cache_counts = Counter(current.values())
    if len(base) != 5419 or Counter(base.values()) != Counter({1: 144, 2: 5275}):
        raise SystemExit("base exact cache does not match the prior accepted checkpoint")
    if len(current) != 5452 or cache_counts != Counter({1: 144, 2: 5308}):
        raise SystemExit("merged exact cache totals differ from the audited checkpoint")
    if any(key not in current or current[key] != verdict for key, verdict in base.items()):
        raise SystemExit("merged exact cache does not preserve the complete base cache")
    cache_delta = {key: verdict for key, verdict in current.items() if key not in base}
    if len(cache_delta) != 33 or Counter(cache_delta.values()) != Counter({2: 33}):
        raise SystemExit("cache delta is not 33 new exact LOSS rows")

    boundary = read_json(BOUNDARY)
    children = [item for item in boundary["boundary"]["children"]]
    child_keys = [tuple(item["key"]) for item in children]
    if (tuple(boundary["class"]["key"]) != CLASS or len(children) != 102
            or len(set(child_keys)) != 102):
        raise SystemExit("geometry audit does not give a complete unique 102-child boundary")
    for item in children:
        key, verdict = tuple(item["key"]), item["verdict"]
        if verdict is not None and current.get(key) != verdict:
            raise SystemExit(f"class boundary/cache disagreement at {key}")
        if verdict is None and key in current:
            raise SystemExit(f"UNKNOWN class child has an exact cache row at {key}")
    class_counts = Counter("UNKNOWN" if item["verdict"] is None else
                           "WIN" if item["verdict"] == 1 else "LOSS" for item in children)
    class_counts.setdefault("WIN", 0)
    expected_class_counts = {"LOSS": 31, "UNKNOWN": 71, "WIN": 0}
    if dict(class_counts) != expected_class_counts or boundary["boundary"]["status"] != "UNKNOWN":
        raise SystemExit(f"class is not the audited 31 LOSS / 71 UNKNOWN boundary: {class_counts}")

    s5_summaries = [read_json(path) for path in S5_SUMMARIES]
    exact_rows = sum(item["exact_rows"] for item in s5_summaries)
    exact_nodes = sum(item["nodes_exact"] for item in s5_summaries)
    all_nodes = sum(item["nodes_all_completed_rows"] for item in s5_summaries)
    unknown_rows = sum(item["completed_rows"] - item["exact_rows"] for item in s5_summaries)
    if ([item["exact_rows"] for item in s5_summaries] != [8, 8, 7]
            or [item["nodes_exact"] for item in s5_summaries] != [28_781_289, 48_405_642, 28_836_665]
            or unknown_rows != 1 or all_nodes - exact_nodes != 15_000_000):
        raise SystemExit("direct S5 probe summaries do not match the recorded exact/UNKNOWN runs")
    if any(item["verdict_counts"].get("WIN", 0) for item in s5_summaries):
        raise SystemExit("unexpected exact S5 WIN in a LOSS-only checkpoint")

    s6 = read_json(S6_SUMMARY)
    receipt = read_json(MERGE)
    reverse = read_json(REVERSE_AUDIT)
    if (s6["complete_canonical_s6_union"] != 90 or s6["new_s6_rows"] != 59
            or s6["new_s6_verdict_counts"] != {"LOSS": 3, "UNKNOWN": 0, "WIN": 56}
            or s6["nodes"] != 35_539_141 or s6["derived_s5_rows"] != 1
            or receipt["reverse_derived_loss_rows"] != 10 or receipt["verdict_conflicts"] != 0
            or receipt["reverse_audit"]["all_safe_parent_count"] != 52
            or receipt["reverse_audit"]["reply27_relevant_parent_count"] != 36
            or reverse["cache_comparison"]["new"] != 10
            or reverse["cache_comparison"]["opposite_verdict"] != 0):
        raise SystemExit("S6 descent or reverse-incidence audit totals failed consistency checks")
    if read_cache(OUT / "post-2f23fcb8-next98-round2-s6-reverse-derived-s5.cache") != {
            tuple(map(int, row[1:3])): int(row[4])
            for row in csv.reader((OUT / "post-2f23fcb8-next98-round2-s6-reverse-derived-s5.cache").open(encoding="utf-8-sig", newline=""))
            if row and row[0] == "s5verdict"}:
        raise SystemExit("reverse-derived S5 cache could not be read consistently")

    cardinality = read_json(CARDINALITY)
    cover = read_json(COVER)
    refined = read_json(REFINED)
    ranking = read_json(RANKING)
    if (cardinality["cache_entries"] != len(current)
            or cardinality["class_status_counts"] != {"LOSS": 30, "UNKNOWN": 3103, "WIN": 251}
            or cardinality["secured_vertices"] != 114 or cardinality["uncovered_vertices"] != 5
            or cardinality["minimum_additional_classes"] != 2
            or cardinality["rational_dual_total"] != "2"
            or not cardinality["dual_certificate_matches_integer_optimum"]
            or cover["repair_unique_unknown_s5"] != 170
            or refined["refined_unique_unknown_s5"] != 170
            or ranking["next_target"]["key"] != list(CLASS)
            or ranking["next_target"]["unknown_s5"] != 71):
        raise SystemExit("global status, cover/dual, repair, or ranking consistency failed")

    report_doc = {
        "schema": "n11-reply27-finite-checkpoint-v1",
        "checkpoint_base_main": BASE_MAIN,
        "created_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": [60, 27],
        "processed_class": {
            "key": list(CLASS), "status": "UNKNOWN", "geometry_audit_passed": True,
            "canonical_s5_children": len(children), "boundary_status_counts": expected_class_counts,
            "coverage_vertices": boundary["class"]["coverage_vertices"],
        },
        "exact_s5_cache": {
            "path": relative(CACHE), "entries": len(current), "WIN": cache_counts[1],
            "LOSS": cache_counts[2], "conflict": 0, "new_exact_rows_from_base": len(cache_delta),
            "sha256": sha(CACHE),
        },
        "s5_probe": {
            "budget_per_target": 15_000_000, "direct_exact_rows": exact_rows,
            "direct_exact_loss_rows": exact_rows, "direct_unknown_rows": unknown_rows,
            "direct_exact_nodes": exact_nodes, "unknown_solver_nodes": all_nodes - exact_nodes,
            "completed_solver_nodes": all_nodes, "summary_paths": [relative(path) for path in S5_SUMMARIES],
        },
        "s6_descent": {
            "complete_canonical_s6_boundary": s6["complete_canonical_s6_union"],
            "new_exact_s6_rows": s6["new_s6_rows"],
            "verdict_counts": s6["new_s6_verdict_counts"], "nodes": s6["nodes"],
            "derived_s5_parent_loss_rows": s6["derived_s5_rows"],
            "unknowns_propagated": s6["unknowns_propagated"], "summary": relative(S6_SUMMARY),
        },
        "s6_reverse_propagation": {
            "unique_exact_s6_loss_witnesses": receipt["reverse_audit"]["s6_loss_unique"],
            "safe_canonical_s5_parents": receipt["reverse_audit"]["all_safe_parent_count"],
            "reply27_relevant_parents": receipt["reverse_audit"]["reply27_relevant_parent_count"],
            "new_s5_loss_rows": receipt["reverse_derived_loss_rows"],
            "duplicate_s5_loss_rows": reverse["cache_comparison"]["duplicate_loss"],
            "verdict_conflicts": receipt["verdict_conflicts"], "audit": relative(REVERSE_AUDIT),
            "merge_receipt": relative(MERGE),
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
            "selected": refined["repair_selected"],
        },
        "next_target": ranking["next_target"],
        "proof_status": {"reply27_root": "UNKNOWN", "empty_11x11": "UNKNOWN"},
        "claim": "The selected S4 class remains UNKNOWN; the saved evidence establishes exact child verdicts only. This checkpoint does not classify the reply27 root or the empty board.",
        "source_manifest": relative(SOURCE_MANIFEST),
        "artifact_inventory": relative(INVENTORY),
    }
    REPORT.write_text(json.dumps(report_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    sources: dict[str, dict[str, Any]] = {}
    add(sources, record(Path(__file__)))
    add(sources, record(REPORT))
    add(sources, record(PARENT_INVENTORY))
    for path in MAIN_CONTEXT:
        add(sources, record(path))
    new_files = sorted({path.resolve() for prefix_path in OUT.glob(f"{PREFIX}*")
                        for path in ([prefix_path] if prefix_path.is_file() else prefix_path.rglob("*"))
                        if path.is_file() and path.resolve() not in {REPORT.resolve(), SOURCE_MANIFEST.resolve(), INVENTORY.resolve()}})
    for path in new_files:
        add(sources, record(path))
        if path.suffix.lower() not in {".json", ".gz"}:
            continue
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        for item in walk(document):
            value, digest = item.get("path"), item.get("sha256")
            if not isinstance(value, str) or not isinstance(digest, str):
                continue
            source_path = resolve(value)
            current_record = record(source_path)
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
        "claim": "Hashes bind exact S5/S6 outputs, solver inputs and logs, current cache, geometry and reverse-incidence audits, global optimizer outputs, and the main-selected finite-boundary evidence.",
    }
    SOURCE_MANIFEST.write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    artifacts: dict[str, dict[str, Any]] = {}
    manifest_sources: dict[str, dict[str, Any]] = {}
    for item in parent["artifacts"]:
        add(artifacts, item)
    for item in parent["manifested_sources"]:
        add(manifest_sources, item)
    add(artifacts, record(PARENT_INVENTORY))
    for path in MAIN_CONTEXT:
        add(artifacts, record(path))
    for path in new_files:
        add(artifacts, record(path))
    add(artifacts, record(REPORT))
    add(artifacts, record(SOURCE_MANIFEST))
    for item in source_doc["sources"]:
        add(manifest_sources, item)
    for table in (artifacts, manifest_sources):
        for item in table.values():
            verify_record(item)

    inventory_doc = {
        "schema": "n11-reply27-checkpoint-artifact-inventory-v1",
        "checkpoint": "post-2f23fcb8 next98 S5 probes, S6 descent and reverse LOSS checkpoint",
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
                      "inventory": relative(INVENTORY), "source_count": source_doc["source_count"],
                      "artifact_count": len(artifacts), "manifested_source_count": len(manifest_sources),
                      "inventory_sha256": sha(INVENTORY), "missing": 0, "mismatched": 0,
                      "cache": report_doc["exact_s5_cache"], "processed_class": report_doc["processed_class"],
                      "global": {"s4_classes": report_doc["s4_classes"], "secured": report_doc["secured_third_moves"],
                                 "remaining": report_doc["remaining_third_moves"],
                                 "minimum_additional_classes": report_doc["minimum_additional_classes"],
                                 "rational_dual": report_doc["rational_dual"], "dual_tight": report_doc["dual_tight"]},
                      "solver_nodes": {"s5_exact": exact_nodes, "s5_unknown": all_nodes - exact_nodes,
                                       "s6": s6["nodes"]}, "next_target": report_doc["next_target"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

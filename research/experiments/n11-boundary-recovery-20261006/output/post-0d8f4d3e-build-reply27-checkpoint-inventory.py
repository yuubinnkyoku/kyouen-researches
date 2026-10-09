#!/usr/bin/env python3
"""Build a self-contained report and SHA-256 inventory for the 0d8f4d3e checkpoint."""
from __future__ import annotations
import csv, gzip, hashlib, json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
BASE = "post-0d8f4d3e"
REPORT = OUT / f"{BASE}-reply27-checkpoint-report.json"
INVENTORY = OUT / f"{BASE}-reply27-checkpoint-artifact-hashes.json"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def record(path: Path) -> dict:
    return {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}

def read_json(path: Path):
    if path.name.endswith(".json.gz"):
        return json.loads(gzip.decompress(path.read_bytes()))
    return json.loads(path.read_text(encoding="utf-8"))

def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)

def add(table: dict[str, dict], row: dict) -> None:
    old = table.get(row["path"])
    if old is not None and old != row:
        raise SystemExit(f"conflicting hash records for {row['path']}")
    table[row["path"]] = row

def main() -> None:
    if REPORT.exists() or INVENTORY.exists():
        raise SystemExit("refusing to overwrite 0d8f4d3e checkpoint report or inventory")
    cache_path = OUT / f"{BASE}-active-class-10448351135499550722-0-merged-s5.cache"
    merge_path = OUT / f"{BASE}-active-class-10448351135499550722-0-merge-summary.json"
    boundary_path = OUT / f"{BASE}-active-class-10448351135499550722-0-class-boundary-audit.json"
    cardinality_path = OUT / f"{BASE}-reply27-cardinality.json"
    repair_path = OUT / f"{BASE}-reply27-repair.json"
    ranking_path = OUT / f"{BASE}-dual-tight-ranking.json"
    saved_s6_path = OUT / f"{BASE}-active-class-10448351135499550722-0-saved-s6-summary.json"
    history_path = OUT / f"{BASE}-active-class-10448351135499550722-0-s6-history-preflight.json"
    reverse_path = OUT / f"{BASE}-reverse210-s6-witness-geometry-audit.json"
    runner_path = OUT / "post-0148c177-active-class-10448351135499550722-0-completion87-collection-runner-summary.json"
    card, repair, ranking = map(read_json, [cardinality_path, repair_path, ranking_path])
    boundary, saved_s6, history, reverse, runner = map(read_json,
        [boundary_path, saved_s6_path, history_path, reverse_path, runner_path])
    exact = {}
    for line_no, row in enumerate(csv.reader(cache_path.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1, 2):
            raise SystemExit(f"invalid exact s5 cache row {line_no}: {row}")
        key, verdict = (int(row[1]), int(row[2])), int(row[4])
        if key in exact and exact[key] != verdict:
            raise SystemExit(f"exact s5 cache conflict for {key}")
        exact[key] = verdict
    counts = Counter(exact.values())
    child_rows = boundary["boundary"]["children"]
    child_counts = Counter(row["verdict"] for row in child_rows)
    report = {
        "schema": "n11-reply27-finite-checkpoint-v1",
        "checkpoint_base_main": "0d8f4d3e82e43c8943c91d382017402c95b5481f",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": [60, 27],
        "exact_s5_cache": {"path": rel(cache_path), "sha256": sha(cache_path), "entries": len(exact),
                           "WIN": counts[1], "LOSS": counts[2], "conflict": 0},
        "s4": card["class_status_counts"],
        "secured_third_moves": card["secured_vertices"],
        "remaining_third_moves": card["uncovered_vertices"],
        "minimum_additional_classes": card["minimum_additional_classes"],
        "rational_dual": card["rational_dual_total"],
        "dual_tight": card["dual_certificate_matches_integer_optimum"],
        "repair": {"classes": repair["repair_classes"],
                   "distinct_unknown_s5": repair["repair_unique_unknown_s5"],
                   "selected": repair["repair_selected"]},
        "active_class": {"key": boundary["class"]["key"],
                         "canonical_s5_children": boundary["boundary"]["canonical_children"],
                         "LOSS": child_counts[2], "WIN": child_counts[1], "UNKNOWN": child_counts[None],
                         "status": boundary["boundary"]["status"],
                         "coverage_vertices": boundary["class"]["coverage_vertices"]},
        "s5_completion_run": {"budget": runner["budget"], "targets": runner["targets"],
                              "exact_LOSS": runner["new_loss"], "exact_WIN": runner["new_win"],
                              "UNKNOWN": runner["unknown"], "nodes": runner["nodes_total"],
                              "undispatched": len(runner["not_dispatched"])},
        "incoming_reverse210": {"s5_rows": reverse["incoming_delta"]["rows"],
                                "exact_s6_loss_keys": reverse["saved_s6_source_audit"]["exact_s6_loss_keys"],
                                "geometry_witnessed_rows": reverse["delta_coverage"]["incoming_rows_with_exact_s6_loss_witness"],
                                "active_class_hits": reverse["active_class_intersection"]["previously_unknown_children_now_exact_loss"],
                                "conflicts": reverse["active_cache_comparison"]["opposite_verdict_conflicts"]},
        "s6_preflight": {"s5_parents": history["parent_count"],
                         "s6_boundary_union": history["s6_boundary_union"],
                         "parent_child_incidences": history["parent_child_incidences"],
                         "saved_s6_verdict_counts": history["saved_s6_verdict_counts_over_unique_union"],
                         "same_or_higher_budget_unknown_s6": history["same_or_higher_budget_unknown_s6_keys"],
                         "local_new_exact_s6": history["local_new_exact_s6_rows_requiring_reuse"],
                         "ready_unique_s6": history["direct_dispatch_ready_unique_s6_keys"],
                         "conflicts": history["conflicts"]},
        "next_target": ranking["next_target"],
        "proof_status": {"reply27_60_27": "UNKNOWN", "empty_11x11": "UNKNOWN"},
        "artifact_paths": {"merge_receipt": rel(merge_path), "class_boundary_audit": rel(boundary_path),
                           "cardinality": rel(cardinality_path), "repair": rel(repair_path),
                           "ranking": rel(ranking_path), "saved_s6_audit": rel(saved_s6_path),
                           "local_s6_history_preflight": rel(history_path),
                           "reverse210_geometry_audit": rel(reverse_path)},
        "claim": "Only exact solver s5 WIN/LOSS rows and audited exact S6 LOSS witnesses are propagated. Probe ranking and UNKNOWN remain scheduling state only.",
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    artifact_paths = set()
    explicit = [
        OUT / "post-0148c177-active-class-10448351135499550722-0-completion87.csv",
        OUT / "post-0148c177-active-class-10448351135499550722-0-completion87-class-selection-v2.json",
        OUT / "post-0148c177-active-class-10448351135499550722-0-completion87-class-boundary-audit.json",
        OUT / "post-0148c177-active-class-10448351135499550722-0-completion87-manifest.json",
        OUT / "post-0148c177-active-class-10448351135499550722-0-completion87-raw-history-baseline.json",
        OUT / "post-0148c177-active-class-10448351135499550722-0-completion87-raw-history-current.json",
        OUT / "post-0148c177-active-class-10448351135499550722-0-completion87-raw-history-coverage.json",
        OUT / "post-0148c177-active-class-10448351135499550722-0-completion87-strict-preflight.json",
        OUT / "post-1001d051-next-class-10448351135499550722-0-merged-exact-s5.cache",
        OUT / "post-1001d051-reconciliation-20261009-augmented-s6-source-audit.json",
        OUT / "post-0148c177-s6-loss-reverse210-s5-delta.cache",
        REPORT,
    ]
    artifact_paths.update(p.resolve() for p in explicit)
    for prefix in ("post-0148c177-active-class-10448351135499550722-0-completion87-collection",
                   "post-0d8f4d3e-"):
        for path in OUT.iterdir():
            if path.name.startswith(prefix):
                if path.is_file():
                    artifact_paths.add(path.resolve())
                elif path.is_dir():
                    artifact_paths.update(p.resolve() for p in path.rglob("*") if p.is_file())
    artifacts = {}
    for path in sorted(artifact_paths):
        if not path.is_file():
            raise SystemExit(f"checkpoint artifact missing: {path}")
        add(artifacts, record(path))

    sources = {}
    for artifact_path in sorted(artifact_paths):
        if artifact_path.suffix.lower() not in {".json", ".gz"}:
            continue
        try:
            document = read_json(artifact_path)
        except (OSError, ValueError, UnicodeDecodeError, gzip.BadGzipFile):
            continue
        for item in walk(document):
            source_path = item.get("path") or item.get("artifact_path")
            digest = item.get("sha256")
            if not isinstance(source_path, str) or not isinstance(digest, str):
                continue
            resolved = Path(source_path.replace("\\", "/"))
            resolved = resolved if resolved.is_absolute() else ROOT / resolved
            resolved = resolved.resolve()
            if not resolved.is_file():
                raise SystemExit(f"manifested source missing: {source_path}")
            row = record(resolved)
            if row["sha256"] != digest or (isinstance(item.get("bytes"), int) and row["bytes"] != item["bytes"]):
                raise SystemExit(f"manifested source hash/size mismatch: {source_path}")
            add(sources, row)
    direct_sources = [
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_local_s6_boundary_history.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
        ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py",
        ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
        ROOT / ".local/n11/reply27-probe9/dfpn.exe",
    ]
    for path in direct_sources:
        if not path.is_file():
            raise SystemExit(f"used source missing: {path}")
        add(sources, record(path))

    missing, mismatched = [], []
    for table in (artifacts, sources):
        for item in table.values():
            path = ROOT / item["path"]
            if not path.is_file():
                missing.append(item["path"])
            elif path.stat().st_size != item["bytes"] or sha(path) != item["sha256"]:
                mismatched.append(item["path"])
    if missing or mismatched:
        raise SystemExit(json.dumps({"missing": missing[:10], "mismatched": mismatched[:10]}))
    inventory = {
        "schema": "n11-reply27-checkpoint-artifact-inventory-v1",
        "checkpoint": "post-0d8f4d3e exact s5 merge and dual-tight 11-parent s6 preflight",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "main_commit_at_checkpoint": "0d8f4d3e82e43c8943c91d382017402c95b5481f",
        "report": record(REPORT),
        "artifact_count": len(artifacts), "artifacts": [artifacts[k] for k in sorted(artifacts)],
        "source_count": len(sources), "manifested_sources": [sources[k] for k in sorted(sources)],
        "missing_sources": missing, "mismatched_sources": mismatched,
        "verification": {"algorithm": "SHA-256", "checked_artifacts": len(artifacts),
                         "checked_sources": len(sources), "missing": 0, "mismatched": 0},
    }
    INVENTORY.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"report": rel(REPORT), "report_sha256": sha(REPORT),
                      "inventory": rel(INVENTORY), "inventory_sha256": sha(INVENTORY),
                      "artifacts": len(artifacts), "sources": len(sources),
                      "missing": 0, "mismatched": 0}, sort_keys=True))

if __name__ == "__main__":
    main()

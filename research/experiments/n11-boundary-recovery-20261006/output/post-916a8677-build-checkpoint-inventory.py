#!/usr/bin/env python3
"""Build the evidence manifest and checkpoint summary for the 916a8677 lane."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
REPORT_PATH = OUT / "post-916a8677-reply27-checkpoint-report.json"
SOURCE_PATH = OUT / "post-916a8677-reply27-checkpoint-source-manifest.json"
HASH_PATH = OUT / "post-916a8677-reply27-checkpoint-artifact-hashes.json"
FINAL_CACHE = OUT / "post-916a8677-reconstructed-s5.cache"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def exact_cache(path: Path):
    rows = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if row and not row[0].lstrip().startswith("#"):
                if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                    raise ValueError(f"invalid exact S5 row: {path}: {row}")
                key = (int(row[1]), int(row[2]))
                value = int(row[4])
                if key in rows and rows[key] != value:
                    raise ValueError(f"S5 verdict conflict: {key}")
                rows[key] = value
    return rows


def class_record(class_key, audit_path: Path, before_path: Path, runner_path: Path,
                 exact_cache_path: Path, win_audit_path: Path):
    audit = load_json(audit_path)
    before = load_json(before_path)
    runner = load_json(runner_path)
    delta = exact_cache(exact_cache_path)
    boundary = audit["boundary"]
    if boundary["status"] != "WIN":
        raise ValueError(f"expected exact WIN class boundary for {class_key}")
    return {
        "s4_class": list(class_key),
        "status_before_probe": before["boundary"]["status_counts"],
        "canonical_s5_children": boundary["canonical_children"],
        "status_after_probe": boundary["status_counts"],
        "exact_new_rows": len(delta),
        "exact_new_verdict_counts": {
            "WIN": sum(v == 1 for v in delta.values()),
            "LOSS": sum(v == 2 for v in delta.values()),
        },
        "probe": {
            "scheduled": runner["targets"],
            "dispatched": runner["new_exact"] + runner["unknown"]
                + runner.get("existing_exact", 0) + runner.get("existing_cache_exact", 0)
                + runner.get("existing_output_exact", 0),
            "not_dispatched_after_exact_win": len(runner["not_dispatched"]),
            "budget_nodes_per_target": runner["budget"],
            "total_nodes": runner["nodes_total"],
            "exact_rows": runner["new_exact"],
            "unknown_rows_excluded_from_cache": runner["unknown"],
        },
        "s6_descent_new_exact_rows": 0,
        "reverse_propagated_s5_loss_rows": 0,
        "geometry_witness_audit": rel(win_audit_path),
        "complete_boundary_audit": rel(audit_path),
    }


def main() -> None:
    cache_audit_path = OUT / "post-916a8677-s5-cache-corpus-audit.json"
    raw_audit_path = OUT / "post-916a8677-s5-raw-replay-corpus-audit.json"
    cardinality_path = OUT / "post-916a8677-cardinality.json"
    repair_path = OUT / "post-d5136a93-after-class-1297036692683759616-0-repair-refined.json"
    ranking_path = OUT / "post-916a8677-ranking.json"
    cache_audit = load_json(cache_audit_path)
    raw_audit = load_json(raw_audit_path)
    card = load_json(cardinality_path)
    repair = load_json(repair_path)
    ranking = load_json(ranking_path)
    rows = exact_cache(FINAL_CACHE)
    counts = {"WIN": sum(v == 1 for v in rows.values()),
              "LOSS": sum(v == 2 for v in rows.values())}

    if len(rows) != 5588 or counts != {"WIN": 150, "LOSS": 5438}:
        raise ValueError(f"unexpected final S5 cache totals: {len(rows)}, {counts}")
    if cache_audit["corpus_conflicts"] or cache_audit["corpus_vs_checkpoint_extra_rows"] \
            or cache_audit["checkpoint_rows_missing_from_corpus"]:
        raise ValueError("saved exact S5 cache corpus did not reconcile cleanly")
    if raw_audit["raw_exact_verdict_conflicts"] or raw_audit["cache_raw_verdict_conflicts"] \
            or raw_audit["raw_exact_not_in_cache"]:
        raise ValueError("saved raw exact S5 replay corpus did not reconcile cleanly")
    if card["class_status_counts"] != {"LOSS": 31, "WIN": 260, "UNKNOWN": 3093} \
            or card["secured_vertices"] != 117 or card["minimum_additional_classes"] != 1 \
            or not card["dual_certificate_matches_integer_optimum"]:
        raise ValueError("unexpected finite class-cover result")
    if ranking["next_target"]["key"] != [1297036692683751456, 0] \
            or ranking["next_target"]["unknown_s5"] != 98 or not ranking["dual_certificate_matches_integer_optimum"]:
        raise ValueError("unexpected next dual-tight repair target")

    class_a = class_record(
        (1585267068835463168, 0),
        OUT / "post-916a8677-reconstructed-class-1585267068835463168-0-boundary-audit.json",
        OUT / "post-d5136a93-class-1585267068835463168-0-probe9-class-boundary-before.json",
        OUT / "post-d5136a93-class-1585267068835463168-0-probe9-runner-summary.json",
        OUT / "post-d5136a93-class-1585267068835463168-0-probe9-new-exact-s5.cache",
        OUT / "post-d5136a93-class-1585267068835463168-0-probe9-win-geometry-verifier.json",
    )
    class_b = class_record(
        (1297036692683759616, 0),
        OUT / "post-916a8677-reconstructed-class-1297036692683759616-0-boundary-audit.json",
        OUT / "post-d5136a93-next-class-1297036692683759616-0-boundary-audit.json",
        OUT / "post-d5136a93-class-1297036692683759616-0-probe9-runner-summary.json",
        OUT / "post-d5136a93-class-1297036692683759616-0-probe9-new-exact-s5.cache",
        OUT / "post-d5136a93-class-1297036692683759616-0-probe9-win-geometry-audit.json",
    )
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    incoming_conditional = OUT / "post-d5136a9-next96-conditional-min48-s6.csv"
    conditional_audit_path = OUT / "post-d5136a9-next96-conditional-min48-audit.json"
    conditional_audit = load_json(conditional_audit_path)
    conditional_lines = [line for line in incoming_conditional.read_text(encoding="utf-8").splitlines()
                         if line and not line.startswith("#")]
    if len(conditional_lines) != 48:
        raise ValueError(f"expected 48 incoming conditional S6 candidates, got {len(conditional_lines)}")
    if conditional_audit["s6_verdict"] != "UNKNOWN" or conditional_audit["outcome_claim"] != \
            "Conditional cover only. No S6 outcomes asserted.":
        raise ValueError("incoming conditional S6 artifact asserts an unexpected outcome")

    report = {
        "schema": "n11-reply27-checkpoint-report-v1",
        "checkpoint_main_before_commit": head,
        "probe_base_main": "d5136a939be1a60b921f0a4eab739596684458da",
        "root": [60, 27],
        "root_status": "UNKNOWN",
        "empty_11x11_board_status": "UNKNOWN",
        "exact_s5_cache": {
            "path": rel(FINAL_CACHE), "entries": len(rows), **counts,
            "conflicts": 0, "sha256": digest(FINAL_CACHE),
            "reconstruction_comparison": "all 5,588 exact rows match the adaptive-probe merge; only the comment header differs",
        },
        "exact_s5_cache_corpus_audit": {
            "path": rel(cache_audit_path),
            "cache_files_scanned": cache_audit["cache_files_discovered"],
            "corpus_unique_rows": cache_audit["corpus_unique_exact_rows"],
            "conflicts": cache_audit["corpus_conflicts"],
            "extra_rows": len(cache_audit["corpus_vs_checkpoint_extra_rows"]),
            "missing_rows": len(cache_audit["checkpoint_rows_missing_from_corpus"]),
        },
        "raw_s5_replay_audit": {
            "path": rel(raw_audit_path),
            "csv_roots": raw_audit["roots"],
            "s5_replay_rows": raw_audit["raw_s5_replay_rows"],
            "exact_replay_rows": raw_audit["raw_exact_s5_replay_rows"],
            "unique_exact_keys": raw_audit["raw_unique_exact_s5_keys"],
            "raw_verdict_conflicts": len(raw_audit["raw_exact_verdict_conflicts"]),
            "cache_verdict_conflicts": len(raw_audit["cache_raw_verdict_conflicts"]),
            "exact_rows_missing_from_cache": len(raw_audit["raw_exact_not_in_cache"]),
            "same_or_higher_15m_budget_unknown_rows": len(raw_audit["same_budget_unknown_rows"]),
        },
        "s4_class_status_counts": card["class_status_counts"],
        "secured_third_moves": card["secured_vertices"],
        "remaining_third_moves": card["uncovered_vertices"],
        "minimum_additional_classes": card["minimum_additional_classes"],
        "rational_lp_dual_total": card["rational_dual_total"],
        "dual_tight": card["dual_certificate_matches_integer_optimum"],
        "repair_classes": repair["repair_classes"],
        "distinct_unknown_s5_union": repair["refined_unique_unknown_s5"],
        "processed_classes": [class_a, class_b],
        "next_target": ranking["next_target"],
        "incoming_main_conditional_schedule": {
            "path": rel(incoming_conditional),
            "audit_path": rel(conditional_audit_path),
            "base_main": "d5136a939be1a60b921f0a4eab739596684458da",
            "candidate_rows": len(conditional_lines),
            "conditional_lower_bound": conditional_audit["dual_certificate"]["ceil_lower_bound"],
            "s6_verdict": conditional_audit["s6_verdict"],
            "status": "schedule and lower-bound audit only; no S6 outcomes asserted; target class (1585267068835463168,0) now has exact S5 WIN witnesses, so the schedule was not dispatched",
        },
        "s6_descent_new_exact_rows": 0,
        "reverse_propagated_s5_loss_rows": 0,
        "validation": {
            "uv_sync_locked": "pass",
            "knowledge_check": "pass: 366 items; 0 errors; 0 warnings",
            "knowledge_unittest": "pass: 33 tests",
            "knowledge_build": "pass: 6 generated views and README",
            "generated_diff_review": "pass: artifacts.md has 13 added links; summary artifact count 1845 to 1858; root README unchanged",
            "artifact_hashes": "pass after inventory verification",
        },
    }

    prefixes = [
        "post-d5136a93-class-1585267068835463168-0-probe9-*",
        "post-d5136a93-class-1297036692683759616-0-probe9-*",
        "post-d5136a93-next-class-1585267068835463168-0-*",
        "post-d5136a93-next-class-1297036692683759616-0-*",
        "post-d5136a93-after-class-1297036692683759616-0-*",
        "post-d5136a93-all-saved-s6-loss*",
        "post-d5136a93-saved-s6-loss-cache-projection*",
        "post-e8d965fd-optimizer-environment.json",
        "post-916a8677-*",
    ]
    excluded = {REPORT_PATH.resolve(), SOURCE_PATH.resolve(), HASH_PATH.resolve()}
    artifact_files: set[Path] = set()
    for pattern in prefixes:
        for path in OUT.glob(pattern):
            if path.is_file() and path.resolve() not in excluded:
                artifact_files.add(path)
    raw_dirs = [
        OUT / "raw/post-d5136a93-class-1585267068835463168-0-probe9",
        OUT / "post-d5136a93-class-1297036692683759616-0-probe9-raw",
    ]
    for directory in raw_dirs:
        if not directory.is_dir():
            raise FileNotFoundError(directory)
        artifact_files.update(p for p in directory.rglob("*") if p.is_file())
    fixed = [
        OUT / "post-d5136a9-next96-conditional-min48-s6.csv",
        OUT / "post-d5136a9-next96-conditional-min48-audit.json",
        OUT / "post-67ecfaa9-class-1585267068834414720-0-after-ready83-s6-reverse-merged-s5.cache",
        ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
        ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_s4_win.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_92_win_witness.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/derive_all_saved_s6_loss_parents.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
    ]
    for path in fixed:
        if not path.is_file():
            raise FileNotFoundError(path)
        artifact_files.add(path)
    files = [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}
             for path in sorted(artifact_files)]
    source_manifest = {
        "schema": "n11-reply27-checkpoint-source-manifest-v1",
        "main_commit_at_build": head,
        "statement": "Hashes of raw archived probe inputs/outputs/logs, exact caches, geometry/S6 audits, optimization outputs, and source scripts used by this checkpoint.",
        "files": files,
    }
    SOURCE_PATH.write_text(json.dumps(source_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report["source_manifest"] = rel(SOURCE_PATH)
    report["artifact_hash_inventory"] = rel(HASH_PATH)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    hashed_paths = set(artifact_files) | {SOURCE_PATH, REPORT_PATH}
    inventory = {
        "schema": "n11-reply27-checkpoint-artifact-hashes-v1",
        "self_hash_embedded": False,
        "files": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}
                  for path in sorted(hashed_paths)],
    }
    HASH_PATH.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"report": rel(REPORT_PATH), "source_manifest": rel(SOURCE_PATH),
                      "artifact_hash_inventory": rel(HASH_PATH),
                      "artifact_count": len(inventory["files"]),
                      "cache_entries": len(rows), "cache_counts": counts,
                      "classes": [class_a["status_after_probe"], class_b["status_after_probe"]],
                      "next_target": ranking["next_target"]["key"]}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a hash-bound report for the 23b52acf reply27 S6/S7 boundary."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PREFIX = "post-23b52acf-"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def record(path: Path):
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)}


def main() -> None:
    cache = OUT / "post-23b52acf-after-round3-round4-completed-merged-s5.cache"
    boundary = load("post-23b52acf-after-round3-round4-class-boundary-audit.json")
    round3 = load("post-23b52acf-after-round2-round3-completed-summary.json")
    round4 = load("post-23b52acf-after-round3-round4-completed-summary.json")
    s6 = load("post-23b52acf-after-round4-s6-descent-summary.json")
    s7 = load("post-23b52acf-after-round4-saved-s7-s6-intersection.json")
    cache_audit = load("post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-audit.json")
    raw_audit = load("post-23b52acf-after-round4-s6-escalation-s5-raw-replay-corpus-audit.json")
    cardinality = load("post-23b52acf-after-round4-s6-escalation-cardinality.json")
    repair = load("post-23b52acf-after-round4-s6-escalation-repair.json")
    ranking = load("post-23b52acf-after-round4-s6-escalation-ranking.json")
    cls = boundary["class"]
    children = boundary["boundary"]["status_counts"]
    selected = repair["additive_optimum"]["selected"]
    if len(selected) != 1 or children != {"LOSS": 104, "UNKNOWN": 2, "WIN": 0}:
        raise SystemExit("checkpoint guard failed: selected repair or class boundary changed")
    if cache_audit["corpus_union"]["rows"] != 5700 or cache_audit["corpus_union"]["conflicts"] != 0:
        raise SystemExit("checkpoint guard failed: cache corpus is not the expected exact union")
    if raw_audit["raw_exact_not_in_cache"] or raw_audit["raw_exact_verdict_conflicts"]:
        raise SystemExit("checkpoint guard failed: raw/cache exact mismatch")

    report = {
        "schema": "n11-reply27-s6-escalation-checkpoint-v1",
        "root": [60, 27],
        "main_commit_at_dispatch": "23b52acfb96c95a258296b4ffda45562db0e74ea",
        "proof_status": {"reply27": "UNKNOWN", "n11_empty_board": "UNKNOWN"},
        "exact_s5_cache": {
            "path": cache.relative_to(ROOT).as_posix(),
            "rows": 5700, "WIN": 151, "LOSS": 5549, "conflicts": 0,
            "sha256": digest(cache), "corpus_sources": cache_audit["source_cache_files"],
        },
        "s4": {
            "class_status_counts": cardinality["class_status_counts"],
            "secured_vertices": cardinality["secured_vertices"],
            "remaining_vertices": cardinality["uncovered_vertices"],
            "minimum_additional_classes": cardinality["minimum_additional_classes"],
            "rational_dual": cardinality["rational_dual_total"],
            "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
            "repair_classes": [row["key"] for row in selected],
            "distinct_unknown_s5_union": repair["additive_optimum"]["unique_unknown_s5"],
        },
        "processed_class": {
            "key": cls["key"], "canonical_s5_children": boundary["boundary"]["canonical_children"],
            "status": boundary["boundary"]["status"], "final_child_counts": children,
            "new_exact_s5_rows_since_main": round3["new_exact"] + round4["new_exact"],
            "new_exact_s5_verdicts": {"WIN": round3["exact_replay_counts"]["WIN"] + round4["exact_replay_counts"]["WIN"],
                                       "LOSS": round3["exact_replay_counts"]["LOSS"] + round4["exact_replay_counts"]["LOSS"]},
            "round3_nodes": round3["nodes_all_completed_rows"],
            "round4_nodes_all_rows": round4["nodes_all_completed_rows"],
            "round4_exact_nodes": round4["nodes_exact"],
            "total_nodes_all_rows": round3["nodes_all_completed_rows"] + round4["nodes_all_completed_rows"],
            "total_exact_nodes": round3["nodes_all_completed_rows"] + round4["nodes_exact"],
            "unknown_s5_children": [list(key) for key in round4["unknown_keys"]],
        },
        "s6_descent": {
            "parents": s6["parent_count"], "parent_child_incidences": s6["parent_child_incidences"],
            "complete_canonical_s6_union": s6["complete_canonical_s6_union"],
            "new_exact_rows": s6["new_s6_rows"], "new_verdict_counts": s6["new_s6_verdict_counts"],
            "total_boundary_verdict_counts": s6["total_boundary_verdict_counts"],
            "nodes": s6["nodes"], "derived_s5_rows": s6["derived_s5_rows"],
            "reverse_propagated_s5_loss": s6["reverse_propagated_s5_loss"],
            "parent_outcomes": s6["s5_parent_outcomes"],
        },
        "saved_s7_intersection": {
            "canonical_s7_keys": s7["unique_canonical_s7_boundary_count"],
            "saved_exact_s7_keys": s7["saved_exact_s7_key_count"],
            "conflicts": s7["conflict_count"], "s6_unknown_parents": s7["s6_unknown_count"],
            "solver_dispatched": False,
        },
        "global_saved_evidence_audits": {
            "s5_cache_corpus": cache_audit["corpus_union"],
            "s5_raw_replay": {
                "rows": raw_audit["raw_s5_replay_rows"],
                "exact_rows": raw_audit["raw_exact_s5_replay_rows"],
                "unique_exact_keys": raw_audit["raw_unique_exact_s5_keys"],
                "same_15m_budget_unknown_observations": raw_audit["same_budget_unknown_count"],
                "exact_missing_from_cache": len(raw_audit["raw_exact_not_in_cache"]),
                "exact_conflicts": len(raw_audit["raw_exact_verdict_conflicts"]),
            },
        },
        "next_target": {
            "class_key": cls["key"], "unknown_s5_count": len(round4["unknown_keys"]),
            "unknown_s5_keys": [list(key) for key in round4["unknown_keys"]],
            "ranked_schedule": ranking["next_target"],
            "dispatch_status": "hold: six S6 UNKNOWNs have 512 canonical S7 children and no saved exact S7 verdict",
        },
        "decision": "Checkpoint exact results and stop before S7 dispatch; the existing dedicated S7 probe workflow does not cover this boundary.",
        "key_evidence": [],
        "claim_limit": "This does not prove {60,27} LOSS or solve the 11x11 empty board.",
    }
    key_names = [
        "post-23b52acf-after-round3-round4-completed-merge-receipt.json",
        "post-23b52acf-after-round3-round4-class-boundary-audit.json",
        "post-23b52acf-after-round4-s6-descent-summary.json",
        "post-23b52acf-after-round4-saved-s7-s6-intersection.json",
        "post-23b52acf-after-round4-saved-s7-s6-intersection-sources.json",
        "post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-audit.json",
        "post-23b52acf-after-round4-s6-escalation-s5-raw-replay-corpus-audit.json",
        "post-23b52acf-after-round4-s6-escalation-cardinality.json",
        "post-23b52acf-after-round4-s6-escalation-repair.json",
        "post-23b52acf-after-round4-s6-escalation-repair-targets.csv",
        "post-23b52acf-after-round4-s6-escalation-ranking.json",
        "post-23b52acf-after-round4-s6-escalation-ranking-targets.csv",
        "post-23b52acf-after-round4-s6-escalation-audit.py",
    ]
    report["key_evidence"] = [record(OUT / name) for name in key_names]
    report_path = OUT / "post-23b52acf-after-round4-s6-escalation-report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    source_code = [
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s7_s6_intersection.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/materialize_s6_descent_evidence_v2.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_s5_via_s6_local.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/adapt_repair_json_for_dual_tight_ranking.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py",
        Path(__file__).resolve(),
    ]
    lineage = [
        "post-23b52acf-after-round2-round3-completed-sources.json",
        "post-23b52acf-after-round3-round4-completed-sources.json",
        "post-23b52acf-after-round4-s6-descent-sources.json",
        "post-23b52acf-after-round4-saved-s7-s6-intersection-sources.json",
        "post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-audit.json",
        "post-23b52acf-after-round4-s6-escalation-s5-raw-replay-corpus-audit.json",
    ]
    artifacts = [p for p in sorted(OUT.glob(PREFIX + "*")) if p.is_file()
                 and p.name not in {"post-23b52acf-after-round4-s6-escalation-source-manifest.json",
                                    "post-23b52acf-after-round4-s6-escalation-artifact-hashes.json"}]
    manifest = {
        "schema": "n11-reply27-s6-escalation-source-manifest-v1",
        "main_commit_at_dispatch": report["main_commit_at_dispatch"],
        "current_s5_cache": record(cache),
        "lineage_manifests": [record(OUT / name) for name in lineage],
        "source_code": [record(path) for path in source_code],
        "checkpoint_artifacts": [record(path) for path in artifacts],
        "source_preservation": "The raw-preservation receipts in the checkpoint artifacts bind byte-identical in-repo copies to retained .local originals.",
        "verdict_policy": "Only exact WIN/LOSS verdicts enter caches; UNKNOWN rows remain in raw evidence and do not propagate.",
    }
    manifest_path = OUT / "post-23b52acf-after-round4-s6-escalation-source-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    hash_paths = {path for path in OUT.glob(PREFIX + "*") if path.is_file()
                  and path.name != "post-23b52acf-after-round4-s6-escalation-artifact-hashes.json"}
    hash_paths.update(source_code)
    inventory = {
        "schema": "n11-reply27-checkpoint-artifact-hashes-v1",
        "main_commit_at_dispatch": report["main_commit_at_dispatch"],
        "files_checked": len(hash_paths),
        "files": [record(path) for path in sorted(hash_paths)],
    }
    inventory_path = OUT / "post-23b52acf-after-round4-s6-escalation-artifact-hashes.json"
    inventory_path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"report": report_path.relative_to(ROOT).as_posix(),
                      "source_manifest": manifest_path.relative_to(ROOT).as_posix(),
                      "artifact_hashes": inventory_path.relative_to(ROOT).as_posix(),
                      "files_checked": inventory["files_checked"],
                      "cache_rows": report["exact_s5_cache"]["rows"],
                      "secured": report["s4"]["secured_vertices"],
                      "remaining": report["s4"]["remaining_vertices"],
                      "s7_boundary": report["saved_s7_intersection"]["canonical_s7_keys"]}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate and summarize the exact S6-to-S5 WIN checkpoint after a29e30e3."""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
REPORT = OUT / "post-a29e30e3-reply27-checkpoint-report.json"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def load(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def record(path: Path) -> dict:
    return {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def main() -> int:
    if REPORT.exists():
        raise SystemExit(f"refusing to overwrite report: {REPORT}")

    cache_path = OUT / "post-a29e30e3-active-class-10448351135499550722-0-merged-s5.cache"
    cache: dict[tuple[int, int], int] = {}
    for line_no, row in enumerate(csv.reader(cache_path.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1, 2):
            raise SystemExit(f"invalid exact S5 cache row {line_no}: {row}")
        key, verdict = (int(row[1]), int(row[2])), int(row[4])
        if key in cache and cache[key] != verdict:
            raise SystemExit(f"exact S5 conflict in merged cache at {key}")
        cache[key] = verdict
    from collections import Counter
    counts = Counter(cache.values())
    if (len(cache), counts[1], counts[2]) != (5260, 129, 5131):
        raise SystemExit(f"unexpected merged exact S5 cache cardinality: {len(cache)}, {counts}")

    boundary = load("post-a29e30e3-active-class-10448351135499550722-0-class-boundary-audit.json")
    if (boundary["boundary"]["canonical_children"] != 105
            or boundary["boundary"]["status"] != "WIN"
            or boundary["boundary"]["status_counts"] != {"LOSS": 94, "UNKNOWN": 10, "WIN": 1}):
        raise SystemExit("active s4 class boundary is not the expected exact WIN witness boundary")
    s6 = load("post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-summary.json")
    if (s6["complete_canonical_s6_union"] != 986 or s6["parent_child_incidences"] != 1041
            or s6["new_s6_rows"] != 653
            or s6["new_s6_verdict_counts"] != {"LOSS": 0, "UNKNOWN": 37, "WIN": 616}
            or s6["derived_s5_rows"] != 1 or s6["reverse_propagated_s5_loss"] != 0
            or s6["s5_parent_outcomes"] != {"LOSS": 0, "UNKNOWN": 10, "WIN": 1}
            or s6["conflicts"] != 0 or s6["unknowns_propagated"]):
        raise SystemExit("materialized S6 batch summary has unexpected verdicts or conflicts")
    sources = load("post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-sources.json")
    raw_source_rows = sources.get("raw_sources", [])
    if len(raw_source_rows) != 653 or sources.get("exact_conflicts") != 0:
        raise SystemExit("S6 batch source manifest has incomplete raw output coverage")
    for source in raw_source_rows:
        path = ROOT / source["artifact_path"]
        if not path.is_file() or sha(path) != source.get("sha256"):
            raise SystemExit(f"copied S6 raw output hash mismatch: {source.get('artifact_path')}")

    win_audit = load("post-a29e30e3-active-class-10448351135499550722-0-s4-win-from-s6-verification.json")
    witness = win_audit["s5_win_witness"]
    if (tuple(win_audit["s4_class"]["key"]) != (10448351135499550722, 0)
            or win_audit["s4_class"]["status"] != "WIN"
            or witness["child_count"] != 89
            or witness["complete_canonical_s6_boundary"] != "all exact WIN"
            or len(witness["solver_rows"]) != 89
            or tuple(witness["key"]) != (10448351135499550786, 0)):
        raise SystemExit("independent S6 geometry verifier did not validate the S5 WIN")

    cardinality = load("post-a29e30e3-reply27-cardinality.json")
    cover = load("post-a29e30e3-reply27-cover.json")
    ranking = load("post-a29e30e3-dual-tight-ranking.json")
    if (cardinality["cache_entries"] != 5260
            or cardinality["class_status_counts"] != {"LOSS": 29, "UNKNOWN": 3122, "WIN": 233}
            or cardinality["secured_vertices"] != 113 or cardinality["uncovered_vertices"] != 6
            or cardinality["minimum_additional_classes"] != 3
            or cardinality["rational_dual_total"] != "3"
            or not cardinality["dual_certificate_matches_integer_optimum"]):
        raise SystemExit("global cardinality or rational dual changed unexpectedly")
    if (cover["repair_classes"] != 3 or cover["repair_unique_unknown_s5"] != 291
            or cover["covered_vertices_after_repair"] != 119
            or ranking["dual_certificate_matches_integer_optimum"] is not True):
        raise SystemExit("reoptimized repair or ranking is inconsistent")

    collateral = [item for item in win_audit["reply27_parent_class_impacts_from_witness"]
                  if item["reachable_from_reply27"]]
    new_collateral = [item for item in collateral
                      if item["status_before_merge"] == "UNKNOWN"
                      and item["status_after_merge"] == "WIN"]
    if len(new_collateral) != 2:
        raise SystemExit("reply27 reverse incidence should yield exactly two newly WIN classes")

    artifact_names = [
        "post-a29e30e3-active-class-10448351135499550722-0-merged-s5.cache",
        "post-a29e30e3-active-class-10448351135499550722-0-merge-receipt.json",
        "post-a29e30e3-active-class-10448351135499550722-0-class-boundary-audit.json",
        "post-a29e30e3-active-class-10448351135499550722-0-s4-win-from-s6-verification.json",
        "post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-inputs.csv",
        "post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-raw-all.csv",
        "post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-raw-exact.csv",
        "post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-exact-s6.cache",
        "post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-derived-s5.cache",
        "post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-sources.json",
        "post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-summary.json",
        "post-a29e30e3-reply27-cardinality.json",
        "post-a29e30e3-reply27-cover.json",
        "post-a29e30e3-reply27-cover-targets.csv",
        "post-a29e30e3-dual-tight-ranking.json",
        "post-a29e30e3-dual-tight-ranking-targets.csv",
        "post-a29e30e3-dual-tight-ranking-sources.json",
        "post-a29e30e3-active-class-10448351135499550722-0-s6-win-parent-summary.json",
        "post-a29e30e3-active-class-10448351135499550722-0-s6-win-parent-sources.json",
        "post-a29e30e3-active-class-10448351135499550722-0-s6-history-preflight-adapted-v2.json",
        "post-a29e30e3-s6-batch-materialization-attempt1-incomplete.json",
    ]
    artifacts = [record(OUT / name) for name in artifact_names]
    sources_used = [
        OUT / "post-0d8f4d3e-active-class-10448351135499550722-0-merged-s5.cache",
        OUT / "post-0d8f4d3e-dual-tight-ranking-targets.csv",
        OUT / "post-1001d051-reconciliation-20261009-augmented-s6-source-audit.json",
        OUT / "post-0d8f4d3e-active-class-10448351135499550722-0-saved-s6-full.json.gz",
        ROOT / ".local/n11/dual-tight-10448351135499550722-0-s6-after-a29e30e3/summary.json",
        ROOT / ".local/n11/reply27-probe9/dfpn.exe",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_s5_via_s6_local.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/materialize_s6_descent_evidence_v2.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_s4_win_from_s6.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
        ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py",
    ]
    source_records = [record(path) for path in sources_used]
    target = ranking["next_target"]
    report = {
        "schema": "n11-reply27-finite-checkpoint-v1",
        "checkpoint_base_main": "a29e30e300f0050f0f7c1fe1de465e258483bdce",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "claim": "Only exact S5 verdicts and geometry-verified complete S6 boundary WINs are propagated; UNKNOWN remains unresolved.",
        "exact_s5_cache": {"entries": len(cache), "WIN": counts[1], "LOSS": counts[2],
                           "conflict": 0, "path": rel(cache_path), "sha256": sha(cache_path)},
        "processed_class": {
            "key": [10448351135499550722, 0], "status": "WIN",
            "canonical_s5_children": 105,
            "counts": boundary["boundary"]["status_counts"],
            "winning_s5_child": list(witness["key"]),
            "unsearched_s5_siblings_remaining_unknown": 10,
            "coverage_vertices": win_audit["s4_class"]["coverage_vertices"],
        },
        "s6_descent": {
            "parent_count": 11, "canonical_s6_union": 986, "parent_child_incidences": 1041,
            "saved_exact_s6": {"WIN": 6, "LOSS": 0, "UNKNOWN": 0},
            "new_exact_s6_rows": 616, "new_s6_rows_including_unknown": 653,
            "new_s6_verdicts": s6["new_s6_verdict_counts"], "nodes": s6["nodes"],
            "one_s5_winning_parent_boundary": 89,
            "one_s5_winning_parent_nodes": 36038482,
            "derived_exact_s5_rows": 1, "derived_s5_verdict": "WIN",
            "other_s5_parents": 10, "other_s5_parents_status": "UNKNOWN",
            "new_exact_s6_loss_for_reverse_propagation": 0,
            "reverse_propagated_s5_loss": 0, "conflicts": 0,
            "unknowns_propagated": False,
        },
        "s4": cardinality["class_status_counts"],
        "secured_third_moves": cardinality["secured_vertices"],
        "remaining_third_moves": cardinality["uncovered_vertices"],
        "minimum_additional_classes": cardinality["minimum_additional_classes"],
        "rational_dual": cardinality["rational_dual_total"],
        "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
        "repair": {"classes": cover["repair_classes"],
                   "additive_unknown_s5": cover["repair_additive_unknown_s5"],
                   "distinct_unknown_s5": cover["repair_unique_unknown_s5"],
                   "selected": cover["repair_selected"]},
        "witness_collateral": {
            "new_reply27_s4_win_classes": [item["key"] for item in new_collateral],
            "new_reply27_class_count": len(new_collateral),
            "secured_vertices_added": 0,
        },
        "next_target": {"key": target["key"], "unknown_s5": target["unknown_s5"],
                        "canonical_s5_children": target["canonical_s5_children"],
                        "known_loss_s5": target["known_loss_s5"],
                        "coverage": target["coverage"], "dual_vertex": target["dual_vertex"],
                        "preflight": "pending after checkpoint push; rank is scheduling only"},
        "proof_status": {"reply27_60_27": "UNKNOWN", "empty_11x11": "UNKNOWN"},
        "artifact_paths": {
            "s6_batch_summary": rel(OUT / "post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-summary.json"),
            "s6_batch_sources": rel(OUT / "post-a29e30e3-active-class-10448351135499550722-0-s6-batch-v2-sources.json"),
            "s4_win_verification": rel(OUT / "post-a29e30e3-active-class-10448351135499550722-0-s4-win-from-s6-verification.json"),
            "class_boundary_audit": rel(OUT / "post-a29e30e3-active-class-10448351135499550722-0-class-boundary-audit.json"),
            "merge_receipt": rel(OUT / "post-a29e30e3-active-class-10448351135499550722-0-merge-receipt.json"),
            "cardinality": rel(OUT / "post-a29e30e3-reply27-cardinality.json"),
            "repair": rel(OUT / "post-a29e30e3-reply27-cover.json"),
            "ranking": rel(OUT / "post-a29e30e3-dual-tight-ranking.json"),
            "incomplete_attempt_note": rel(OUT / "post-a29e30e3-s6-batch-materialization-attempt1-incomplete.json"),
        },
        "bound_artifacts": artifacts,
        "bound_sources": source_records,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")
    print(json.dumps({"report": rel(REPORT), "sha256": sha(REPORT),
                      "exact_s5": report["exact_s5_cache"], "s4": report["s4"],
                      "secured": report["secured_third_moves"],
                      "minimum_additional_classes": report["minimum_additional_classes"],
                      "next_target": report["next_target"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build a hash-bound report and artifact inventory for the 07f822e5 lane."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PREFIX = "post-07f822e5-"
MAIN = "07f822e56d3627701a677140d1b5a00c39f26911"

REPORT = OUT / f"{PREFIX}reply27-checkpoint-report.json"
SOURCES = OUT / f"{PREFIX}reply27-checkpoint-source-manifest.json"
HASHES = OUT / f"{PREFIX}reply27-checkpoint-artifact-hashes.json"
BASE_CACHE = OUT / "post-916a8677-reconstructed-s5.cache"
FINAL_CACHE = OUT / "post-07f822e5-after-probe8-probe8-completed-merged-s5.cache"

RUN_DIRS = [
    ROOT / ".local/n11/dual-tight-ready-1297036692683751456-0-probe8-post07f822e5",
    ROOT / ".local/n11/dual-tight-ready-1297036692683751456-0-after-probe8-probe8-post07f822e5",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def read_json(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def exact_cache(path: Path) -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise ValueError(f"invalid exact S5 row at {path}:{line_no}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if verdict not in (1, 2) or key in result and result[key] != verdict:
                raise ValueError(f"invalid/conflicting exact S5 row at {path}:{line_no}: {row}")
            result[key] = verdict
    return result


def file_record(path: Path) -> dict:
    return {"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}


def artifact_paths() -> list[Path]:
    paths = {p.resolve() for p in OUT.rglob("*")
             if p.is_file() and p.name.startswith(PREFIX) and p.resolve() != HASHES.resolve()}
    for run_dir in RUN_DIRS:
        if not run_dir.is_dir():
            raise FileNotFoundError(f"missing raw solver run directory: {run_dir}")
        paths.update(p.resolve() for p in run_dir.rglob("*") if p.is_file())
    paths.add(BASE_CACHE.resolve())
    paths.add(Path(__file__).resolve())
    return sorted(paths, key=rel)


def main() -> None:
    if any(path.exists() for path in (REPORT, SOURCES, HASHES)):
        raise SystemExit("refusing to overwrite a prior checkpoint report or manifest")

    base, final = exact_cache(BASE_CACHE), exact_cache(FINAL_CACHE)
    if any(key not in final or final[key] != value for key, value in base.items()):
        raise ValueError("merged S5 cache changed an existing exact verdict")
    delta = {key: value for key, value in final.items() if key not in base}
    delta_counts = {"WIN": sum(v == 1 for v in delta.values()),
                    "LOSS": sum(v == 2 for v in delta.values())}

    first = read_json("post-07f822e5-next-target-probe8-completed-summary.json")
    second = read_json("post-07f822e5-after-probe8-probe8-completed-summary.json")
    first_runner = read_json("post-07f822e5-next-target-probe8-completed-runner-summary.json")
    second_runner = read_json("post-07f822e5-after-probe8-probe8-completed-runner-summary.json")
    initial_boundary = read_json("post-07f822e5-next-target-boundary-before.json")
    first_boundary = read_json("post-07f822e5-next-target-probe8-completed-class-boundary-audit.json")
    final_boundary = read_json("post-07f822e5-after-probe8-probe8-class-boundary-audit.json")
    card = read_json("post-07f822e5-after-probe8-probe8-cardinality.json")
    repair = read_json("post-07f822e5-after-probe8-probe8-repair.json")
    ranking = read_json("post-07f822e5-after-probe8-probe8-ranking.json")
    cache_audit = read_json("post-07f822e5-after-probe8-probe8-s5-cache-corpus-audit.json")
    raw_audit = read_json("post-07f822e5-after-probe8-probe8-s5-raw-replay-corpus-audit.json")

    values = {1: "WIN", 2: "LOSS"}
    counts = {"WIN": sum(v == 1 for v in final.values()),
              "LOSS": sum(v == 2 for v in final.values())}
    winner_keys = [child["key"] for child in final_boundary["boundary"]["children"]
                   if child["verdict"] == 1]
    if (len(final) != 5603 or counts != {"WIN": 151, "LOSS": 5452}
            or delta_counts != {"WIN": 1, "LOSS": 14}
            or len(winner_keys) != 1
            or final_boundary["boundary"]["status"] != "WIN"
            or final_boundary["boundary"]["canonical_children"] != 104
            or final_boundary["boundary"]["status_counts"] !=
                {"LOSS": 20, "UNKNOWN": 83, "WIN": 1}
            or card["class_status_counts"] != {"LOSS": 31, "UNKNOWN": 3091, "WIN": 262}
            or card["secured_vertices"] != 117 or card["uncovered_vertices"] != 2
            or card["minimum_additional_classes"] != 1
            or not card["dual_certificate_matches_integer_optimum"]
            or cache_audit["corpus_conflicts"] != 0
            or cache_audit["corpus_unique_exact_rows"] != len(final)
            or cache_audit["corpus_vs_checkpoint_extra_rows"]
            or cache_audit["checkpoint_rows_missing_from_corpus"]
            or raw_audit["raw_exact_not_in_cache"]
            or raw_audit["raw_exact_verdict_conflicts"]
            or raw_audit["cache_raw_verdict_conflicts"]):
        raise ValueError("checkpoint verification did not match the required exact counts")

    repair_summary = repair["additive_optimum"]
    next_target = ranking["next_target"]
    report = {
        "schema": "n11-reply27-checkpoint-report-v1",
        "main_at_dispatch": MAIN,
        "root": [60, 27],
        "root_status": "UNKNOWN",
        "empty_11x11_board_status": "UNKNOWN",
        "exact_s5_cache": {"path": rel(FINAL_CACHE), "entries": len(final), **counts,
                            "conflicts": 0, "sha256": digest(FINAL_CACHE)},
        "exact_s5_cache_delta": {"rows": len(delta), **delta_counts,
                                  "nodes_by_new_exact_rows": 97_570_974},
        "class_status_counts": card["class_status_counts"],
        "secured_third_moves": card["secured_vertices"],
        "remaining_third_moves": card["uncovered_vertices"],
        "minimum_additional_classes": card["minimum_additional_classes"],
        "rational_dual_total": card["rational_dual_total"],
        "dual_tight": card["dual_certificate_matches_integer_optimum"],
        "repair": {"classes": repair_summary["repair_classes"],
                   "distinct_unknown_s5": repair_summary["unique_unknown_s5"],
                   "selected": repair_summary["selected"]},
        "processed_class": {
            "key": final_boundary["class"]["key"], "result": final_boundary["boundary"]["status"],
            "coverage_vertices": final_boundary["class"]["coverage_vertices"],
            "canonical_s5_children": final_boundary["boundary"]["canonical_children"],
            "before": initial_boundary["boundary"]["status_counts"],
            "after_first_probe": first_boundary["boundary"]["status_counts"],
            "after_second_probe": final_boundary["boundary"]["status_counts"],
            "exact_win_s5_witnesses": winner_keys,
        },
        "probe_runs": [
            {"scheduled": first["scheduled_targets"], "completed": first["completed_targets"],
             "exact_counts": first["exact_replay_counts"], "new_exact": first["new_exact"],
             "nodes": first["nodes_all_completed_rows"],
             "class_status_after": first["class_status_from_exact_witness"]},
            {"scheduled": second["scheduled_targets"], "completed": second["completed_targets"],
             "exact_counts": second["exact_replay_counts"], "new_exact": second["new_exact"],
             "nodes": second["nodes_all_completed_rows"],
             "class_status_after": second["class_status_from_exact_witness"],
             "unknown_rows_remain_unknown": second["unknown_keys"]},
        ],
        "s6_descent_new_exact_rows": 0,
        "reverse_propagated_s5_loss_rows": 0,
        "saved_cache_corpus_audit": {
            "cache_files": cache_audit["cache_files_discovered"],
            "unique_exact_rows": cache_audit["corpus_unique_exact_rows"],
            "missing": 0, "extra": 0, "conflicts": 0,
        },
        "raw_replay_corpus_audit": {
            "s5_rows": raw_audit["raw_s5_replay_rows"],
            "exact_rows": raw_audit["raw_exact_s5_replay_rows"],
            "unique_exact_keys": raw_audit["raw_unique_exact_s5_keys"],
            "same_budget_unknown_rows": len(raw_audit["same_budget_unknown_rows"]),
            "raw_conflicts": len(raw_audit["raw_exact_verdict_conflicts"]),
            "cache_conflicts": len(raw_audit["cache_raw_verdict_conflicts"]),
            "exact_not_in_cache": len(raw_audit["raw_exact_not_in_cache"]),
        },
        "next_target": next_target,
        "report_path": rel(REPORT),
        "source_manifest_path": rel(SOURCES),
        "artifact_hash_inventory_path": rel(HASHES),
        "claim": "Finite exact reply27 cache checkpoint only. {60,27} and the 11x11 empty board remain UNKNOWN.",
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")

    source_paths = [
        BASE_CACHE,
        ROOT / ".local/n11/reply27-probe9/dfpn.exe",
        ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_class_local.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/collect_dual_tight_completed_probe_v2.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/prepare_dual_tight_ready_subset_probe.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_probe_preflight.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/materialize_dual_tight_class_unknowns.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/adapt_repair_json_for_dual_tight_ranking.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/output/post-916a8677-audit-s5-cache-corpus.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/output/post-916a8677-audit-s5-raw-replay-corpus.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/output/post-67ecfaa9-class-1585267068834414720-0-after-ready83-s6-extended-source-audit.json",
    ]
    if any(not path.is_file() for path in source_paths):
        raise FileNotFoundError("one or more checkpoint source paths are missing")
    before_manifest_artifacts = artifact_paths()
    source_manifest = {
        "schema": "n11-reply27-checkpoint-source-manifest-v1",
        "main_at_dispatch": MAIN,
        "root": [60, 27],
        "current_exact_s5_cache": file_record(FINAL_CACHE),
        "class_key": [1297036692683751456, 0],
        "probe_source_manifests": [
            file_record(OUT / "post-07f822e5-next-target-probe8-completed-sources.json"),
            file_record(OUT / "post-07f822e5-after-probe8-probe8-completed-sources.json"),
        ],
        "inputs": [file_record(path) for path in source_paths],
        "artifacts": [file_record(path) for path in before_manifest_artifacts
                      if path.resolve() not in {SOURCES.resolve(), HASHES.resolve()}],
        "claim": "Hashes bind the two bounded S5 probes, full canonical class geometry, exact cache merge, saved-history audits, class-cover optimization, and preserved raw solver outputs. UNKNOWN remains unknown.",
    }
    SOURCES.write_text(json.dumps(source_manifest, indent=2, sort_keys=True) + "\n",
                       encoding="utf-8", newline="\n")

    files = [file_record(path) for path in artifact_paths()]
    inventory = {
        "schema": "n11-reply27-artifact-hash-inventory-v1",
        "main_at_dispatch": MAIN,
        "artifact_count": len(files),
        "missing_count": 0,
        "mismatch_count": 0,
        "files": files,
    }
    HASHES.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")

    for row in inventory["files"]:
        path = ROOT / Path(row["path"])
        if not path.is_file() or path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            raise ValueError(f"artifact hash verification failed: {row['path']}")
    print(json.dumps({"report": rel(REPORT), "source_manifest": rel(SOURCES),
                      "artifact_hashes": rel(HASHES), "artifact_count": len(files),
                      "inventory_sha256": digest(HASHES), "cache_rows": len(final),
                      "cache_win": counts["WIN"], "cache_loss": counts["LOSS"],
                      "new_rows": len(delta), "new_win": delta_counts["WIN"],
                      "new_loss": delta_counts["LOSS"], "class": final_boundary["boundary"]["status"],
                      "class_counts": final_boundary["boundary"]["status_counts"],
                      "conflicts": 0}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate and materialize the post-d18e1cc7 dual-tight probe checkpoint."""
from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.metadata
import json
import platform
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-d18e1cc7-next-class-1297318167660462080-0"
BASE_MAIN = "d18e1cc73c1669347be690a3d26141da9f704d99"
REPORT = OUT / "post-d18e1cc7-reply27-checkpoint-report.json"
SOURCE_MANIFEST = OUT / "post-d18e1cc7-reply27-checkpoint-source-manifest.json"
OPTIMIZER_ENV = OUT / "post-d18e1cc7-optimizer-environment.json"


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
        raise SystemExit(f"checkpoint input missing: {path}")
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


def csv_rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return [row for row in csv.reader(stream)
                if row and not row[0].lstrip().startswith("#")]


def exact_s5(path: Path) -> dict[tuple[int, int], tuple[int, int]]:
    result: dict[tuple[int, int], tuple[int, int]] = {}
    for line_no, row in enumerate(csv_rows(path), 1):
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid exact s5 row at {path}:{line_no}: {row}")
        key = (int(row[1]), int(row[2]))
        verdict, nodes = int(row[4]), int(row[5])
        if verdict not in (1, 2) or nodes < 0 or key in result:
            raise SystemExit(f"invalid or duplicate exact s5 row: {key}")
        result[key] = (verdict, nodes)
    return result


def add_source(table: dict[str, dict[str, Any]], path: Path,
               expected_sha: str | None = None, expected_bytes: int | None = None) -> None:
    item = record(path)
    if expected_sha is not None and item["sha256"] != expected_sha:
        raise SystemExit(f"source hash mismatch: {item['path']}")
    if expected_bytes is not None and item["bytes"] != expected_bytes:
        raise SystemExit(f"source byte count mismatch: {item['path']}")
    old = table.get(item["path"])
    if old is not None and old != item:
        raise SystemExit(f"source changed during report generation: {item['path']}")
    table[item["path"]] = item


def main() -> int:
    if any(path.exists() for path in (REPORT, SOURCE_MANIFEST, OPTIMIZER_ENV)):
        raise SystemExit("refusing to overwrite a checkpoint report, source manifest, or environment file")

    def p(suffix: str) -> Path:
        return OUT / f"{PREFIX}{suffix}"

    base_cache = OUT / "post-d01858aa-next-class-1297599642637172736-0-after-completion87-current-s5.cache"
    collected = p("-probe8-completed")
    paths = {
        "raw_history_full": p("-raw-history-current.json"),
        "raw_history_baseline": p("-raw-history-baseline.json"),
        "raw_history_coverage": p("-raw-history-coverage.json"),
        "saved_s6_full": p("-saved-s6-summary.json"),
        "saved_s6_probe": p("-probe8-saved-s6-summary.json"),
        "raw_history_probe": p("-probe8-raw-history-current.json"),
        "raw_history_probe_baseline": p("-probe8-raw-history-baseline.json"),
        "raw_history_probe_coverage": p("-probe8-raw-history-coverage.json"),
        "preflight": p("-probe8-strict-preflight.json"),
        "schedule": p("-probe8-manifest.json"),
        "scheduled_targets": p("-probe8.csv"),
        "full_targets": p("-unknown-s5-targets.csv"),
        "full_target_manifest": p("-unknown-s5-manifest.json"),
        "boundary": collected.with_name(collected.name + "-class-boundary-audit.json"),
        "cardinality": collected.with_name(collected.name + "-cardinality.json"),
        "repair": collected.with_name(collected.name + "-repair.json"),
        "repair_targets": collected.with_name(collected.name + "-repair-targets.csv"),
        "repair_adapted": collected.with_name(collected.name + "-repair-adapted.json"),
        "ranking": collected.with_name(collected.name + "-ranking.json"),
        "ranking_targets": collected.with_name(collected.name + "-ranking-targets.csv"),
        "ranking_sources": collected.with_name(collected.name + "-ranking-sources.json"),
        "base_cache": base_cache,
        "raw_all": collected.with_name(collected.name + "-raw-all.csv"),
        "raw_exact": collected.with_name(collected.name + "-raw-exact.csv"),
        "exact_targets": collected.with_name(collected.name + "-exact-targets.csv"),
        "new_cache": collected.with_name(collected.name + "-new-exact-s5.cache"),
        "merged_cache": collected.with_name(collected.name + "-merged-s5.cache"),
        "summary": collected.with_name(collected.name + "-summary.json"),
        "runner_summary": collected.with_name(collected.name + "-runner-summary.json"),
        "merge_receipt": collected.with_name(collected.name + "-merge-receipt.json"),
        "collector_sources": collected.with_name(collected.name + "-sources.json"),
        "saved_s6_source_audit": OUT / "post-d01858aa-next-class-1297599642637172736-0-unknown2-s6-15m-augmented-audit.json",
        "prior_s6_reverse_audit": OUT / "post-d01858aa-next-class-1297599642637172736-0-unknown2-s6-15m-reverse-audit.json",
        "prior_s6_reverse_cache": OUT / "post-d01858aa-next-class-1297599642637172736-0-unknown2-s6-15m-reverse-derived-s5.cache",
        "prior_s6_raw": OUT / "post-d01858aa-next-class-1297599642637172736-0-unknown2-s6-15m-raw-all.csv",
        "local_s6_loss_audit_script": ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_local_s5_s6_against_saved_corpus.py",
    }
    absent = [name for name, path in paths.items() if not path.is_file()]
    if absent:
        raise SystemExit(f"required checkpoint inputs absent: {absent}")

    cache = exact_s5(paths["merged_cache"])
    base = exact_s5(paths["base_cache"])
    delta = exact_s5(paths["new_cache"])
    if (len(base), Counter(v for v, _ in base.values())) != (5393, Counter({2: 5259, 1: 134})):
        raise SystemExit("unexpected base exact S5 cache")
    if (len(cache), Counter(v for v, _ in cache.values())) != (5401, Counter({2: 5265, 1: 136})):
        raise SystemExit("unexpected merged exact S5 cache")
    if len(delta) != 8 or any(key in base for key in delta):
        raise SystemExit("new exact S5 delta does not contain eight fresh rows")
    if any(cache.get(key) != value for key, value in delta.items()):
        raise SystemExit("exact S5 delta differs from merged cache")

    boundary = load_json(paths["boundary"])
    children = boundary["boundary"]["children"]
    counts = Counter({"WIN": 0, "LOSS": 0, "UNKNOWN": 0})
    wins = []
    for child in children:
        verdict = child["verdict"]
        state = {1: "WIN", 2: "LOSS", None: "UNKNOWN"}[verdict]
        counts[state] += 1
        key = tuple(child["key"]) if isinstance(child["key"], list) else tuple(map(int, child["key"].split()))
        if verdict in (1, 2) and cache.get(key, (None, None))[0] != verdict:
            raise SystemExit(f"boundary exact verdict absent from merged cache: {key}")
        if verdict == 1:
            wins.append(key)
    expected_wins = {
        (1153202979718823936, 68719476736),
        (1297318167660462080, 64),
    }
    if (boundary["class"]["key"] != [1297318167660462080, 0]
            or boundary["boundary"]["canonical_children"] != 104
            or len(children) != 104
            or counts != Counter({"LOSS": 15, "WIN": 2, "UNKNOWN": 87})
            or set(wins) != expected_wins
            or boundary["cache"]["conflicts"] != 0):
        raise SystemExit(f"full class boundary mismatch: {counts}, wins={wins}")

    probe = load_json(paths["summary"])
    runner = load_json(paths["runner_summary"])
    if (probe["class_key"] != [1297318167660462080, 0]
            or probe["scheduled_targets"] != 8
            or probe["completed_targets"] != 8
            or probe["exact_replay_counts"] != {"WIN": 2, "LOSS": 6, "UNKNOWN": 0}
            or probe["nodes_all_completed_rows"] != 54042436
            or probe["nodes_exact"] != 54042436
            or runner["not_dispatched"] != []):
        raise SystemExit("probe summary disagrees with exact raw rows")

    card = load_json(paths["cardinality"])
    repair = load_json(paths["repair"])
    ranking = load_json(paths["ranking"])
    if (card["cache_entries"] != len(cache)
            or card["class_status_counts"] != {"LOSS": 30, "UNKNOWN": 3110, "WIN": 244}
            or card["secured_vertices"] != 114
            or card["uncovered_vertices"] != 5
            or card["minimum_additional_classes"] != 2
            or card["rational_dual_total"] != "2"
            or card["dual_certificate_matches_integer_optimum"] is not True):
        raise SystemExit("cardinality or rational dual mismatch")
    additive = repair["additive_optimum"]
    next_target = ranking["next_target"]
    if (repair["minimum_additional_classes"] != 2
            or repair["minimum_additional_classes_mip_gap"] != 0.0
            or additive["repair_classes"] != 2
            or additive["unique_unknown_s5"] != 195
            or additive["additive_unknown_s5"] != 195
            or ranking["minimum_additional_classes"] != 2
            or ranking["rational_dual_total"] != "2"
            or ranking["dual_certificate_matches_integer_optimum"] is not True
            or next_target["key"] != [1297036761403228160, 0]
            or next_target["unknown_s5"] != 96
            or next_target["known_loss_s5"] != 6
            or next_target["canonical_s5_children"] != 102):
        raise SystemExit("repair or next-target ranking mismatch")

    history = load_json(paths["raw_history_full"])
    saved_s6 = load_json(paths["saved_s6_full"])
    probe_history = load_json(paths["raw_history_probe"])
    probe_saved_s6 = load_json(paths["saved_s6_probe"])
    preflight = load_json(paths["preflight"])
    raw_coverage = load_json(paths["raw_history_probe_coverage"])
    if (history["targets"]["count"] != 95
            or len(history["prior_exact"]) != 0
            or len(history["prior_unknown_same_budget_or_higher"]) != 1
            or len(history["dispatch_ready_keys"]) != 94
            or history["exact_verdict_conflicts"]):
        raise SystemExit("full raw-history audit mismatch")
    if (saved_s6["targets"]["parent_count"] != 95
            or saved_s6["cache_comparison"]["new_exact"] != 0
            or saved_s6["cache_comparison"]["opposite_verdict_conflicts"]
            or saved_s6["targets"]["status_counts"] != {"UNKNOWN": 95}):
        raise SystemExit("full saved-S6 intersection mismatch")
    if (probe_history["targets"]["count"] != 8
            or len(probe_history["prior_exact"]) != 0
            or probe_history["prior_unknown_same_budget_or_higher"]
            or probe_history["exact_verdict_conflicts"]
            or probe_saved_s6["targets"]["parent_count"] != 8
            or probe_saved_s6["cache_comparison"]["new_exact"] != 0
            or probe_saved_s6["targets"]["status_counts"] != {"UNKNOWN": 8}
            or raw_coverage["status"] != "PASS"
            or preflight["historical_source_coverage"]["status"] != "PASS"
            or preflight["ready_keys"] and len(preflight["ready_keys"]) != 8
            or preflight["blocked_same_or_higher_budget_unknown_keys"]
            or preflight["raw_history"]["conflicts"] != 0
            or preflight["saved_s6"]["conflicts"] != 0):
        raise SystemExit("probe-specific preflight evidence mismatch")

    # Two local S6 LOSS rows were detected during .local reconciliation. They
    # are already present byte-for-byte in the checkpointed raw batch and were
    # reverse-audited across all safe canonical parents before this checkpoint.
    local_s6_dir = ROOT / ".local/n11/dual-tight-s6-1297599642637172736-0-unknown2-15m"
    local_s6_losses = [
        local_s6_dir / "s6-1297604040683692032-0.out.csv",
        local_s6_dir / "s6-10377982391321890816-8192.out.csv",
    ]
    prior_reverse = load_json(paths["prior_s6_reverse_audit"])
    prior_raw = paths["prior_s6_raw"]
    prior_raw_rows = {tuple(map(int, row[9:11])): row for row in csv_rows(prior_raw)
                      if len(row) == 11 and row[0] == "replay" and row[2] == "6"}
    local_loss_keys = []
    for local_path in local_s6_losses:
        rows = csv_rows(local_path)
        if (len(rows) != 1 or rows[0][0] != "replay" or rows[0][2] != "6"
                or rows[0][6] != "2"):
            raise SystemExit(f"unexpected local S6 evidence row: {local_path}")
        key = tuple(map(int, rows[0][9:11]))
        if prior_raw_rows.get(key) != rows[0]:
            raise SystemExit(f"local S6 exact row does not match preserved checkpoint raw: {key}")
        local_loss_keys.append(key)
    reverse_cmp = prior_reverse["cache_comparison"]
    reverse_parents = prior_reverse["reverse_parents"]
    prior_delta = exact_s5(paths["prior_s6_reverse_cache"])
    if (not prior_reverse["s6"]["all_s6_exact_rows_geometry_checked"]
            or prior_reverse["s6"]["unknowns_propagated"]
            or prior_reverse["s6"]["conflicting_keys"]
            or reverse_parents["all_canonical_safe_parent_count"] != 48
            or reverse_parents["reply27_relevant_parent_count"] != 34
            or reverse_cmp["new"] != 8
            or reverse_cmp["duplicate_loss"] != 26
            or reverse_cmp["opposite_verdict"] != 0
            or any(cache.get(key, (None, None))[0] != value[0] for key, value in prior_delta.items())):
        raise SystemExit("prior local S6 LOSS reverse-incidence audit is not valid or merged")

    raw_all_rows = csv_rows(paths["raw_all"])
    raw_exact_rows = csv_rows(paths["raw_exact"])
    if len(raw_all_rows) != 8 or len(raw_exact_rows) != 8:
        raise SystemExit("collected raw S5 rows are incomplete")
    raw_counts = Counter(int(row[6]) for row in raw_all_rows)
    if raw_counts != Counter({1: 2, 2: 6}) or sum(int(row[7]) for row in raw_all_rows) != 54042436:
        raise SystemExit("collected raw S5 output counts or nodes mismatch")

    source_paths = [
        paths["base_cache"], *paths.values(),
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_local_s5_s6_against_saved_corpus.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/prepare_dual_tight_ready_subset_probe.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_probe_preflight.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_class_local.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/collect_dual_tight_completed_probe_v2.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/derive_all_saved_s6_loss_parents.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/adapt_repair_json_for_dual_tight_ranking.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/n11_integer_circle_geometry.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py",
        ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py",
        ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
        ROOT / ".local/n11/reply27-probe9/dfpn.exe",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/output/post-9dcb11b6-reply27-geometry-v1.json.gz",
        *local_s6_losses,
    ]
    sources: dict[str, dict[str, Any]] = {}
    for path in source_paths:
        add_source(sources, path)

    evidence_documents = [
        paths["raw_history_full"], paths["raw_history_baseline"], paths["raw_history_coverage"],
        paths["saved_s6_full"], paths["saved_s6_probe"], paths["raw_history_probe"],
        paths["raw_history_probe_baseline"], paths["raw_history_probe_coverage"],
        paths["preflight"], paths["schedule"], paths["full_target_manifest"],
        paths["collector_sources"], paths["boundary"], paths["cardinality"],
        paths["repair"], paths["repair_adapted"], paths["ranking_sources"],
        paths["prior_s6_reverse_audit"], paths["merge_receipt"],
        paths["saved_s6_source_audit"], paths["summary"],
    ]
    for document_path in evidence_documents:
        add_source(sources, document_path)
        document = load_json(document_path)
        for item in walk(document):
            source_path = item.get("path") or item.get("artifact_path")
            digest = item.get("sha256")
            if isinstance(source_path, str) and isinstance(digest, str):
                add_source(sources, resolve(source_path), digest,
                           item.get("bytes") if isinstance(item.get("bytes"), int) else None)

    optimizer_doc = {
        "schema": "n11-reply27-optimizer-environment-v1",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": importlib.metadata.version("numpy"),
        "scipy": importlib.metadata.version("scipy"),
        "main_at_dispatch": BASE_MAIN,
        "note": "The cache-aware class/cover/ranking scripts ran in this environment; solver verdicts came from the separately hashed native dfpn.exe.",
    }
    OPTIMIZER_ENV.write_text(json.dumps(optimizer_doc, indent=2, sort_keys=True) + "\n",
                             encoding="utf-8", newline="\n")

    cache_record = record(paths["merged_cache"])
    report = {
        "schema": "n11-reply27-finite-checkpoint-v1",
        "checkpoint": "Dual-tight class stopped at exact S5 WIN; current exact cache and minimum repair reoptimized.",
        "checkpoint_base_main": BASE_MAIN,
        "claim": "The complete canonical S5 boundary of the processed S4 class has exact WIN children. This class is WIN; {60,27} and the 11x11 empty board remain UNKNOWN.",
        "processed_class": {
            "key": [1297318167660462080, 0], "status": "WIN",
            "canonical_s5_children": 104,
            "boundary_status_counts": {"LOSS": 15, "WIN": 2, "UNKNOWN": 87},
            "coverage_vertices": boundary["class"]["coverage_vertices"],
            "exact_win_witnesses": [list(key) for key in sorted(wins)],
            "unexplored_children_after_probe": 87,
            "geometry_audit_passed": True,
        },
        "s5_probe": {
            "budget_per_target": 15000000, "scheduled": 8, "completed": 8,
            "verdicts": {"WIN": 2, "LOSS": 6, "UNKNOWN": 0},
            "nodes_exact": 54042436, "nodes_all_rows": 54042436,
            "first_win_seen_at_key": [1153202979718823936, 68719476736],
            "additional_class_siblings_dispatched": 0,
        },
        "exact_s5_cache": {
            "entries": len(cache), "WIN": 136, "LOSS": 5265, "conflict": 0,
            "new_rows": len(delta), "base_cache_entries": len(base),
            "path": cache_record["path"], "sha256": cache_record["sha256"],
        },
        "raw_history_preflight": {
            "full_class_targets": 95, "csv_files_examined": history["csv_files_examined"],
            "prior_exact": 0, "same_budget_unknown_rows": 1,
            "dispatch_ready": 94, "conflicts": 0,
            "excluded_key": history["prior_unknown_same_budget_or_higher"][0]["key"],
        },
        "saved_s6_intersection": {
            "full_class_parents": 95, "source_files": saved_s6["source_audit"]["source_file_count"],
            "canonical_s6_keys": saved_s6["source_audit"]["canonical_s6_count"],
            "derived_exact_s5": saved_s6["cache_comparison"]["new_exact"],
            "class_parents_remaining_unknown": saved_s6["targets"]["status_counts"]["UNKNOWN"],
            "conflicts": 0,
        },
        "probe_preflight": {
            "targets": 8, "ready": 8, "blocked": 0, "saved_s6_unknown": 8,
            "raw_history_coverage": "PASS", "strict_verifier": "PASS",
        },
        "local_s6_reconciliation": {
            "local_exact_loss_keys": [list(key) for key in sorted(local_loss_keys)],
            "local_audit_guard": "The read-only local reconciliation stopped after finding exact S6 LOSS rows and requires reverse incidence before acceptance; both rows match preserved checkpoint raw evidence.",
            "prior_reverse_audit": rel(paths["prior_s6_reverse_audit"]),
            "safe_canonical_parents_checked": reverse_parents["all_canonical_safe_parent_count"],
            "reply27_relevant_parents_checked": reverse_parents["reply27_relevant_parent_count"],
            "prior_new_s5_loss_rows_already_in_base_cache": len(prior_delta),
            "prior_reverse_conflicts": 0,
            "new_s6_or_reverse_loss_rows_in_this_checkpoint": 0,
        },
        "s4_classes": card["class_status_counts"],
        "secured_third_moves": card["secured_vertices"],
        "remaining_third_moves": card["uncovered_vertices"],
        "minimum_additional_classes": card["minimum_additional_classes"],
        "rational_dual": card["rational_dual_total"],
        "dual_tight": card["dual_certificate_matches_integer_optimum"],
        "repair": {
            "classes": additive["repair_classes"],
            "additive_unknown_s5": additive["additive_unknown_s5"],
            "distinct_unknown_s5": additive["unique_unknown_s5"],
            "selected": additive["selected"],
        },
        "next_target": {
            "key": next_target["key"], "unknown_s5": next_target["unknown_s5"],
            "canonical_s5_children": next_target["canonical_s5_children"],
            "known_loss_s5": next_target["known_loss_s5"],
            "coverage": next_target["coverage"],
            "dual_vertex": next_target["dual_vertex"],
            "claim": "Ranking is scheduling only; UNKNOWN remains UNKNOWN.",
        },
        "proof_status": {"reply27_root": "UNKNOWN", "empty_11x11": "UNKNOWN"},
        "source_manifest": rel(SOURCE_MANIFEST),
        "optimizer_environment": rel(OPTIMIZER_ENV),
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")

    # Re-record the report/environment and ensure every discovered path still hashes.
    add_source(sources, REPORT)
    add_source(sources, OPTIMIZER_ENV)
    source_doc = {
        "schema": "n11-reply27-checkpoint-source-manifest-v1",
        "checkpoint_base_main": BASE_MAIN,
        "claim": "Solver outcomes are bound to raw exact replay rows and source hashes. UNKNOWN is never used as a verdict.",
        "sources": [sources[key] for key in sorted(sources)],
        "evidence_manifests": [record(path) for path in evidence_documents],
        "missing_sources": [],
        "verification": {
            "algorithm": "SHA-256", "checked_sources": len(sources),
            "missing": 0, "mismatched": 0,
        },
    }
    SOURCE_MANIFEST.write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8", newline="\n")
    print(json.dumps({
        "report": rel(REPORT), "report_sha256": sha(REPORT),
        "source_manifest": rel(SOURCE_MANIFEST), "source_count": len(sources),
        "missing": 0, "mismatched": 0,
        "cache_entries": len(cache), "class_status": "WIN",
        "secured": card["secured_vertices"], "remaining": card["uncovered_vertices"],
        "next_target": next_target["key"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

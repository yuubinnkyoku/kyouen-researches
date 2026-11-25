#!/usr/bin/env python3
"""Validate and materialize the post-d01858aa reply27 class-WIN checkpoint."""
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
PREFIX = "post-d01858aa-next-class-1297599642637172736-0"
BASE_MAIN = "d01858aa1a1d5ba5843b7a71c3a1539359de5889"
REPORT = OUT / "post-d01858aa-reply27-checkpoint-report.json"
SOURCE_MANIFEST = OUT / "post-d01858aa-reply27-checkpoint-source-manifest.json"
OPTIMIZER_ENV = OUT / "post-d01858aa-optimizer-environment-after-completion87.json"


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
        raise SystemExit(f"required checkpoint input missing: {path}")
    return {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def load(name: str) -> Any:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def cache_counts(path: Path) -> tuple[dict[tuple[int, int], int], Counter[int]]:
    rows: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise SystemExit(f"invalid exact S5 cache row {line_no}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if verdict not in (1, 2):
                raise SystemExit(f"non-exact S5 verdict at {key}: {verdict}")
            if key in rows and rows[key] != verdict:
                raise SystemExit(f"conflicting exact S5 verdict at {key}")
            rows[key] = verdict
    return rows, Counter(rows.values())


def add_source(table: dict[str, dict[str, Any]], path: Path) -> None:
    item = record(path)
    old = table.get(item["path"])
    if old is not None and old != item:
        raise SystemExit(f"source hash changed during report generation: {item['path']}")
    table[item["path"]] = item


def main() -> int:
    if REPORT.exists() or SOURCE_MANIFEST.exists():
        raise SystemExit("refusing to overwrite an existing reply27 checkpoint report/manifest")

    current_cache = OUT / f"{PREFIX}-after-completion87-current-s5.cache"
    cache, hist = cache_counts(current_cache)
    if (len(cache), hist[1], hist[2]) != (5393, 134, 5259):
        raise SystemExit(f"unexpected exact S5 cache counts: {len(cache)} {hist}")

    probe = load(f"{PREFIX}-probe8-completed-summary.json")
    probe_runner = load(f"{PREFIX}-probe8-completed-runner-summary.json")
    s6_2m = load(f"{PREFIX}-unknown2-s6-summary.json")
    s6_15m = load(f"{PREFIX}-unknown2-s6-15m-summary.json")
    reverse = load(f"{PREFIX}-unknown2-s6-15m-reverse-audit.json")
    completion = load(f"{PREFIX}-completion87-collected-summary.json")
    completion_manifest = load(f"{PREFIX}-completion87-collected-manifest.json")
    merge = load(f"{PREFIX}-after-completion87-merge-receipt.json")
    boundary_doc = load(f"{PREFIX}-after-completion87-boundary-audit.json")
    cardinality = load(f"{PREFIX}-after-completion87-cardinality.json")
    repair = load(f"{PREFIX}-after-completion87-repair.json")
    ranking = load(f"{PREFIX}-after-completion87-ranking.json")
    optimizer = load(OPTIMIZER_ENV.name)

    target_class = [1297599642637172736, 0]
    boundary = boundary_doc["boundary"]
    boundary_counts = Counter(
        {"WIN": 0, "LOSS": 0, "UNKNOWN": 0}
    )
    for child in boundary["children"]:
        verdict = child["verdict"]
        boundary_counts[{1: "WIN", 2: "LOSS", None: "UNKNOWN"}[verdict]] += 1
        if verdict in (1, 2) and cache.get(tuple(child["key"])) != verdict:
            raise SystemExit(f"boundary verdict not present in exact cache: {child['key']}")
    if (boundary_doc["class"]["key"] != target_class
            or boundary.get("canonical_children") != 103
            or len(boundary["children"]) != 103
            or boundary_counts != Counter({"LOSS": 29, "WIN": 2, "UNKNOWN": 72})
            or boundary_doc["cache"]["conflicts"] != 0):
        raise SystemExit(f"target class boundary failed validation: {boundary_counts}")
    win_witnesses = [child["key"] for child in boundary["children"] if child["verdict"] == 1]
    if set(map(tuple, win_witnesses)) != {
        (1297599642637172736, 67108864),
        (1297599642637172736, 68719476736),
    }:
        raise SystemExit(f"unexpected exact WIN witnesses: {win_witnesses}")

    if (probe["class_key"] != target_class
            or probe["exact_replay_counts"] != {"LOSS": 6, "UNKNOWN": 2, "WIN": 0}
            or probe["nodes_all_completed_rows"] != 47043116
            or probe_runner["nodes_total"] != 47043116):
        raise SystemExit("probe8 results do not match the recorded raw run")
    if (s6_2m["complete_canonical_s6_union"] != 162
            or s6_2m["parent_child_incidences"] != 163
            or s6_2m["new_s6_verdict_counts"] != {"LOSS": 0, "UNKNOWN": 3, "WIN": 159}
            or s6_2m["nodes"] != 49417008
            or s6_2m["unknowns_propagated"]):
        raise SystemExit("2M S6 boundary/replay counts changed")
    if (s6_15m["new_s6_verdict_counts"] != {"LOSS": 2, "UNKNOWN": 0, "WIN": 1}
            or s6_15m["nodes"] != 9648804
            or s6_15m["s5_parent_outcomes"] != {"LOSS": 2, "UNKNOWN": 0, "WIN": 0}
            or s6_15m["unknowns_propagated"]):
        raise SystemExit("15M S6 exact outcomes do not match the saved summary")
    reverse_cmp = reverse["cache_comparison"]
    if (reverse["run_status"] != "ok"
            or reverse_cmp["new"] != 8
            or reverse_cmp["duplicate_loss"] != 26
            or reverse_cmp["opposite_verdict"] != 0
            or reverse["s6"]["conflicting_keys"]
            or reverse["s6"]["unknowns_propagated"]):
        raise SystemExit("S6 LOSS reverse-incidence audit has a conflict or changed counts")

    if (completion["class_key"] != target_class
            or completion["scheduled"] != 87
            or completion["completed_rows"] != 17
            or completion["exact_rows"] != 15
            or completion["status_counts"] != {
                "exact_LOSS": 13, "exact_WIN": 2, "completed_UNKNOWN": 2,
                "not_dispatched": 70,
            }
            or completion["nodes_all_completed_rows"] != 122175061
            or completion["nodes_exact"] != 92175061):
        raise SystemExit("adaptive 87-target completion does not match the collector")
    if (merge["unique_exact_s5"] != 5393 or merge["win"] != 134
            or merge["loss"] != 5259 or merge["conflicts"] != 0
            or merge["sources"][0]["rows"] != 5378
            or merge["sources"][1]["rows"] != 15):
        raise SystemExit("exact S5 merge receipt does not match the cache")

    classes = cardinality["class_status_counts"]
    if (classes != {"LOSS": 30, "UNKNOWN": 3112, "WIN": 242}
            or cardinality["cache_entries"] != len(cache)
            or cardinality["secured_vertices"] != 114
            or cardinality["uncovered_vertices"] != 5
            or cardinality["minimum_additional_classes"] != 2
            or cardinality["rational_dual_total"] != "2"
            or cardinality["dual_positive_weights"] != {"77": "1", "100": "1"}
            or not cardinality["dual_certificate_matches_integer_optimum"]):
        raise SystemExit("all-class cardinality or dual check does not match")
    additive = repair["additive_optimum"]
    next_target = ranking["next_target"]
    if (additive["repair_classes"] != 2 or additive["unique_unknown_s5"] != 194
            or additive["mip_gap"] != 0.0
            or next_target["key"] != [1297318167660462080, 0]
            or next_target["unknown_s5"] != 95
            or next_target["known_loss_s5"] != 9
            or next_target["canonical_s5_children"] != 104
            or not ranking["dual_certificate_matches_integer_optimum"]):
        raise SystemExit("repair/ranking changed or failed its exact cover certificate")

    source_paths = [
        Path(__file__).resolve(),
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_class_local.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/collect_dual_tight_completion_run.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/derive_all_saved_s6_loss_parents.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/augment_s6_source_audit_from_manifest.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_raw_history_coverage.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/prepare_dual_tight_ready_subset_probe.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_probe_preflight.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/adapt_repair_json_for_dual_tight_ranking.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/n11_integer_circle_geometry.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/refine_cache_aware_reply27_cover.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/merge_exact_s5_evidence.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py",
        ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py",
        ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
        ROOT / ".local/n11/reply27-probe9/dfpn.exe",
    ]
    source_table: dict[str, dict[str, Any]] = {}
    for path in source_paths:
        add_source(source_table, path)

    evidence_manifests = [
        OUT / f"{PREFIX}-probe8-manifest.json",
        OUT / f"{PREFIX}-probe8-completed-sources.json",
        OUT / f"{PREFIX}-unknown2-s6-sources.json",
        OUT / f"{PREFIX}-unknown2-s6-exact-only-sources.json",
        OUT / f"{PREFIX}-unknown2-s6-15m-sources.json",
        OUT / f"{PREFIX}-completion87-collected-manifest.json",
        OUT / f"{PREFIX}-unknown-s5-manifest.json",
        OUT / f"{PREFIX}-after-completion87-ranking-sources.json",
    ]
    missing_manifest_sources: list[str] = []
    for manifest_path in evidence_manifests:
        document = json.loads(manifest_path.read_text(encoding="utf-8"))
        for item in walk(document):
            source_path = item.get("path") or item.get("artifact_path")
            digest = item.get("sha256")
            if not isinstance(source_path, str) or not isinstance(digest, str):
                continue
            resolved = resolve(source_path)
            if not resolved.is_file():
                missing_manifest_sources.append(source_path)
                continue
            actual = record(resolved)
            if actual["sha256"] != digest:
                raise SystemExit(f"manifested evidence hash mismatch: {source_path}")
            if isinstance(item.get("bytes"), int) and actual["bytes"] != item["bytes"]:
                raise SystemExit(f"manifested evidence byte count mismatch: {source_path}")
            add_source(source_table, resolved)
    if missing_manifest_sources:
        raise SystemExit(f"missing manifested evidence files: {missing_manifest_sources[:20]}")

    source_doc = {
        "schema": "n11-reply27-checkpoint-source-manifest-v1",
        "checkpoint_base_main": BASE_MAIN,
        "claim": "Exact outcomes are bound to raw replay output, source code, and the solver binary by SHA-256. UNKNOWN rows are retained in their raw manifests and are not exact cache verdicts.",
        "sources": [source_table[key] for key in sorted(source_table)],
        "evidence_manifests": [record(path) for path in evidence_manifests],
        "missing_sources": [],
        "verification": {"algorithm": "SHA-256", "checked_sources": len(source_table), "missing": 0, "mismatched": 0},
    }
    SOURCE_MANIFEST.write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    artifact_names = [
        f"{PREFIX}-probe8-completed-raw-all.csv",
        f"{PREFIX}-probe8-completed-raw-exact.csv",
        f"{PREFIX}-probe8-completed-summary.json",
        f"{PREFIX}-probe8-completed-merge-receipt.json",
        f"{PREFIX}-unknown2-s6-raw-all.csv",
        f"{PREFIX}-unknown2-s6-summary.json",
        f"{PREFIX}-unknown2-s6-15m-raw-all.csv",
        f"{PREFIX}-unknown2-s6-15m-summary.json",
        f"{PREFIX}-unknown2-s6-15m-reverse-audit.json",
        f"{PREFIX}-completion87-collected-raw-all.csv",
        f"{PREFIX}-completion87-collected-raw-exact.csv",
        f"{PREFIX}-completion87-collected-summary.json",
        f"{PREFIX}-completion87-collected-manifest.json",
        f"{PREFIX}-after-completion87-merge-receipt.json",
        f"{PREFIX}-after-completion87-current-s5.cache",
        f"{PREFIX}-after-completion87-boundary-audit.json",
        f"{PREFIX}-after-completion87-cardinality.json",
        f"{PREFIX}-after-completion87-repair.json",
        f"{PREFIX}-after-completion87-ranking.json",
        OPTIMIZER_ENV.name,
    ]
    key_artifacts = [record(OUT / name) for name in artifact_names]
    report = {
        "schema": "n11-reply27-finite-checkpoint-v1",
        "checkpoint": "dual-tight repair class stopped at exact S5 WIN; cache, S6 reverse propagation, and repair reoptimized",
        "checkpoint_base_main": BASE_MAIN,
        "claim": "The complete canonical S5 boundary of the processed S4 class has an exact WIN child. This makes the class WIN; it does not prove the reply27 root or the empty board.",
        "exact_s5_cache": {
            "entries": len(cache), "WIN": hist[1], "LOSS": hist[2], "conflict": 0,
            "new_rows_since_base_cache": 29,
            "base_cache": {"entries": 5364, "WIN": 132, "LOSS": 5232},
            "path": rel(current_cache), "sha256": sha(current_cache),
        },
        "processed_class": {
            "key": target_class, "status": "WIN", "canonical_s5_children": 103,
            "boundary_status_counts": {"LOSS": 29, "WIN": 2, "UNKNOWN": 72},
            "coverage_vertices": boundary_doc["class"]["coverage_vertices"],
            "exact_win_witnesses": win_witnesses,
            "unexplored_children_after_first_win": 70,
            "geometry_audit_passed": True,
        },
        "s5_probe": {
            "budget_per_target": 15000000,
            "probe8": {
                "targets": probe["scheduled_targets"], "exact_rows": probe["new_exact"],
                "verdicts": probe["exact_replay_counts"],
                "nodes_all_rows": probe["nodes_all_completed_rows"], "nodes_exact_rows": probe["nodes_exact"],
            },
            "adaptive_completion87": {
                "scheduled": completion["scheduled"], "completed": completion["completed_rows"],
                "exact_rows": completion["exact_rows"], "verdicts": completion["verdict_counts"],
                "nodes_all_rows": completion["nodes_all_completed_rows"], "nodes_exact_rows": completion["nodes_exact"],
                "not_dispatched_after_win": len(completion["not_dispatched_keys"]),
            },
        },
        "s6_descent": {
            "canonical_children": s6_2m["complete_canonical_s6_union"],
            "parent_child_incidences": s6_2m["parent_child_incidences"],
            "at_2m": {"verdicts": s6_2m["new_s6_verdict_counts"], "nodes": s6_2m["nodes"]},
            "previously_unknown_replayed_at_15m": {
                "verdicts": s6_15m["new_s6_verdict_counts"], "nodes": s6_15m["nodes"],
            },
            "direct_s5_parent_losses": s6_15m["derived_s5_rows"],
            "reverse_incidence": {
                "safe_canonical_parents": reverse["reverse_parents"]["all_canonical_safe_parent_count"],
                "reply27_parents": reverse["reverse_parents"]["reply27_relevant_parent_count"],
                "new_s5_losses": reverse_cmp["new"],
                "duplicate_losses": reverse_cmp["duplicate_loss"],
                "conflicts": reverse_cmp["opposite_verdict"],
            },
            "unknown_propagated": False,
        },
        "nodes_all_solver_rows": (
            probe["nodes_all_completed_rows"] + s6_2m["nodes"] + s6_15m["nodes"]
            + completion["nodes_all_completed_rows"]
        ),
        "s4_classes": classes,
        "secured_third_moves": cardinality["secured_vertices"],
        "remaining_third_moves": cardinality["uncovered_vertices"],
        "minimum_additional_classes": cardinality["minimum_additional_classes"],
        "rational_dual": cardinality["rational_dual_total"],
        "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
        "repair": {
            "classes": additive["repair_classes"],
            "distinct_unknown_s5": additive["unique_unknown_s5"],
            "selected": additive["selected"],
        },
        "next_target": {
            "key": next_target["key"], "unknown_s5": next_target["unknown_s5"],
            "canonical_s5_children": next_target["canonical_s5_children"],
            "known_loss_s5": next_target["known_loss_s5"], "coverage": next_target["coverage"],
            "dual_vertex": next_target["dual_vertex"], "claim": "ranking is scheduling only",
        },
        "root_outcomes": {"reply27_60_27": "UNKNOWN", "empty_11x11": "UNKNOWN"},
        "source_manifest": {
            "path": rel(SOURCE_MANIFEST), "sha256": sha(SOURCE_MANIFEST),
            "source_count": len(source_table),
        },
        "optimizer_environment": record(OPTIMIZER_ENV),
        "key_artifacts": key_artifacts,
        "created_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "report": rel(REPORT), "source_manifest": rel(SOURCE_MANIFEST),
        "source_count": len(source_table), "cache_entries": len(cache),
        "WIN": hist[1], "LOSS": hist[2], "conflicts": 0,
        "class_status": boundary_counts, "next_target": next_target["key"],
        "report_sha256": sha(REPORT), "source_manifest_sha256": sha(SOURCE_MANIFEST),
    }, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the completed 105-child LOSS class checkpoint on main 2beb63af."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
REPORT = OUT / "post-2beb63af-reply27-checkpoint-report.json"
PREFIX = "post-2beb63af-next-class-10448351135499550721-0"
BASE_MAIN = "2beb63af85aa1134bc0db6dd742dc1ba7e961419"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def record(path: Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"checkpoint artifact missing: {path}")
    return {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def load(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def cache_counts(path: Path) -> tuple[dict[tuple[int, int], int], Counter]:
    rows: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise SystemExit(f"invalid exact S5 cache row {line_no}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if verdict not in (1, 2) or (key in rows and rows[key] != verdict):
                raise SystemExit(f"invalid or conflicting exact S5 row at {key}")
            rows[key] = verdict
    return rows, Counter(rows.values())


def main() -> int:
    if REPORT.exists():
        raise SystemExit(f"refusing to overwrite report: {REPORT}")

    class_key = [10448351135499550721, 0]
    cache_path = OUT / f"{PREFIX}-completion87-completed-merged-s5.cache"
    cache, hist = cache_counts(cache_path)
    initial_probe = load(f"{PREFIX}-probe8-completed-summary.json")
    initial_merge = load(f"{PREFIX}-probe8-completed-merge-receipt.json")
    initial_preflight = load(f"{PREFIX}-probe8-strict-preflight.json")
    initial_raw = load(f"{PREFIX}-probe8-raw-history-current-v2.json")
    initial_s6 = load(f"{PREFIX}-probe8-saved-s6-summary.json")
    completion = load(f"{PREFIX}-completion87-completed-summary.json")
    completion_runner = load(f"{PREFIX}-completion87-completed-runner-summary.json")
    completion_merge = load(f"{PREFIX}-completion87-completed-merge-receipt.json")
    completion_preflight = load(f"{PREFIX}-completion87-strict-preflight.json")
    completion_raw = load(f"{PREFIX}-completion87-raw-history-current.json")
    completion_s6 = load(f"{PREFIX}-completion87-saved-s6-summary.json")
    boundary_doc = load(f"{PREFIX}-completion87-completed-boundary-audit.json")
    boundary = boundary_doc["boundary"]
    cardinality = load("post-2beb63af-reply27-cardinality-after-completion87-loss.json")
    repair = load("post-2beb63af-selected31-repair-after-completion87-loss.json")
    ranking = load("post-2beb63af-dual-tight-ranking-after-completion87-loss.json")

    if (len(cache), hist[1], hist[2]) != (5364, 132, 5232):
        raise SystemExit(f"unexpected merged exact S5 cache: {len(cache)} {hist}")
    if (initial_probe.get("class_key") != class_key
            or initial_probe.get("new_exact") != 8
            or initial_probe.get("exact_replay_counts") != {"LOSS": 8, "UNKNOWN": 0, "WIN": 0}
            or initial_probe.get("nodes_exact") != 37474347
            or initial_merge.get("conflicts") != 0):
        raise SystemExit("probe8 exact rows/merge receipt do not match the run")
    if (initial_preflight.get("target_count") != 8
            or len(initial_preflight.get("ready_keys", [])) != 8
            or initial_preflight.get("blocked_same_or_higher_budget_unknown_keys")
            or initial_preflight.get("raw_history", {}).get("conflicts") != 0
            or initial_raw.get("prior_exact")
            or initial_raw.get("prior_unknown_same_budget_or_higher")
            or initial_s6.get("cache_comparison", {}).get("new_exact") != 0):
        raise SystemExit("probe8 preflight has a raw/S6 exact result or conflict")
    if (completion.get("class_key") != class_key
            or completion.get("scheduled_targets") != 87
            or completion.get("new_exact") != 87
            or completion.get("exact_replay_counts") != {"LOSS": 87, "UNKNOWN": 0, "WIN": 0}
            or completion.get("nodes_all_completed_rows") != 417376483
            or completion.get("unknown_keys") != []
            or completion_runner.get("new_exact") != 87
            or completion_runner.get("nodes_total") != 417376483
            or completion_merge.get("conflicts") != 0):
        raise SystemExit("completion87 exact rows or merge receipt do not match the run")
    if (completion_preflight.get("target_count") != 87
            or len(completion_preflight.get("ready_keys", [])) != 87
            or completion_preflight.get("blocked_same_or_higher_budget_unknown_keys")
            or completion_preflight.get("raw_history", {}).get("conflicts") != 0
            or completion_raw.get("prior_exact")
            or completion_raw.get("prior_unknown_same_budget_or_higher")
            or completion_s6.get("cache_comparison", {}).get("new_exact") != 0):
        raise SystemExit("completion87 strict preflight/raw/S6 audit changed")
    loss_verification = load(f"{PREFIX}-completion87-completed-boundary-audit.json")
    if (boundary.get("canonical_children") != 105
            or boundary.get("status") != "LOSS"
            or boundary.get("status_counts") != {"LOSS": 105, "UNKNOWN": 0, "WIN": 0}
            or loss_verification.get("boundary", {}).get("status") != "LOSS"
            or loss_verification.get("class", {}).get("key") != class_key
            or loss_verification.get("cache", {}).get("conflicts") != 0):
        raise SystemExit("complete canonical s5 boundary is not 105 exact LOSS")

    expected_classes = {"LOSS": 30, "UNKNOWN": 3115, "WIN": 239}
    if (cardinality.get("cache_entries") != 5364
            or cardinality.get("class_status_counts") != expected_classes
            or cardinality.get("secured_vertices") != 114
            or cardinality.get("uncovered_vertices") != 5
            or cardinality.get("minimum_additional_classes") != 2
            or cardinality.get("rational_dual_total") != "2"
            or not cardinality.get("dual_certificate_matches_integer_optimum")):
        raise SystemExit("all-class status, cover, or rational dual is inconsistent")
    additive = repair["additive_optimum"]
    if (repair.get("minimum_additional_classes") != 2
            or additive.get("repair_classes") != 2
            or additive.get("unique_unknown_s5") != 196
            or additive.get("mip_gap") != 0.0):
        raise SystemExit("reoptimized two-class repair is inconsistent")
    target = ranking.get("next_target", {})
    if (ranking.get("minimum_additional_classes") != 2
            or not ranking.get("dual_certificate_matches_integer_optimum")
            or target.get("key") != [1297599642637172736, 0]
            or target.get("unknown_s5") != 97
            or target.get("canonical_s5_children") != 103):
        raise SystemExit("current dual-tight ranking is inconsistent")

    artifacts = [record(path) for path in sorted(OUT.glob("post-2beb63af-*"))
                 if path.is_file() and path != REPORT]
    for directory in sorted(OUT.glob("post-2beb63af-*")):
        if directory.is_dir():
            artifacts.extend(record(path) for path in sorted(directory.rglob("*")) if path.is_file())
    used_sources = [
        Path(__file__).resolve(),
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/collect_dual_tight_completed_probe_v2.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/prepare_dual_tight_ready_subset_probe.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_dual_tight_probe_preflight.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_dual_tight_s4_boundary.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/verify_raw_history_coverage.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_saved_s6_targets.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/complete_class_local.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_loss_class_cache.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cover.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/adapt_repair_json_for_dual_tight_ranking.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/rank_dual_tight_repair_classes.py",
        ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py",
        ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py",
        ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/n11_integer_circle_geometry.py",
        ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
        ROOT / ".local/n11/reply27-probe9/dfpn.exe",
    ]

    report = {
        "schema": "n11-reply27-finite-checkpoint-v1",
        "checkpoint_base_main": BASE_MAIN,
        "claim": "The full canonical s5 boundary of the processed s4 class is exact LOSS; only exact cache verdicts and geometry verification are used.",
        "exact_s5_cache": {
            "entries": len(cache), "WIN": hist[1], "LOSS": hist[2], "conflict": 0,
            "path": rel(cache_path), "sha256": sha(cache_path),
        },
        "processed_class": {
            "key": class_key, "status": "LOSS", "canonical_s5_children": 105,
            "counts": boundary["status_counts"], "coverage_vertices": [104, 110, 120],
            "probe8_new_exact_loss": 8, "completion87_new_exact_loss": 87,
            "total_new_exact_loss": 95, "exact_win_children": 0, "unknown_children": 0,
        },
        "probe": {
            "budget_per_target": 15000000,
            "probe8_nodes": 37474347, "completion87_nodes": 417376483,
            "total_nodes": 454850830, "probe8_verdicts": {"LOSS": 8},
            "completion87_verdicts": {"LOSS": 87},
        },
        "preflight": {
            "initial_probe8_targets": 8, "initial_probe8_ready": 8,
            "initial_probe8_saved_s6_outcomes": {"UNKNOWN": 8},
            "remaining_targets": 87, "remaining_dispatch_ready": 87,
            "remaining_same_budget_unknown": 0, "remaining_prior_exact": 0,
            "remaining_raw_csv_sources_scanned": completion_raw["csv_files_examined"],
            "remaining_saved_s6_outcomes": {"UNKNOWN": 87},
            "conflicts": 0,
        },
        "s6_descent": {"new_s6_solver_rows": 0, "derived_s5_rows": 0,
                       "reverse_propagated_s5_loss": 0, "unknown_s6_propagated": False},
        "s4": cardinality["class_status_counts"],
        "secured_third_moves": cardinality["secured_vertices"],
        "remaining_third_moves": cardinality["uncovered_vertices"],
        "minimum_additional_classes": cardinality["minimum_additional_classes"],
        "rational_dual": cardinality["rational_dual_total"],
        "dual_tight": cardinality["dual_certificate_matches_integer_optimum"],
        "repair": {
            "classes": additive["repair_classes"],
            "additive_unknown_s5": additive["additive_unknown_s5"],
            "distinct_unknown_s5": additive["unique_unknown_s5"],
            "selected": additive["selected"],
        },
        "next_target": {
            "key": target["key"], "unknown_s5": target["unknown_s5"],
            "canonical_s5_children": target["canonical_s5_children"],
            "known_loss_s5": target["known_loss_s5"], "coverage": target["coverage"],
            "dual_vertex": target["dual_vertex"], "preflight": "pending; ranking is scheduling only",
        },
        "proof_status": {"reply27_60_27": "UNKNOWN", "empty_11x11": "UNKNOWN"},
        "bound_artifacts": artifacts,
        "bound_sources": [record(path) for path in used_sources],
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")
    print(json.dumps({
        "report": rel(REPORT), "sha256": sha(REPORT), "exact_s5_cache": report["exact_s5_cache"],
        "processed_class": report["processed_class"], "s4": report["s4"],
        "secured": report["secured_third_moves"],
        "minimum_additional_classes": report["minimum_additional_classes"],
        "repair_distinct_unknown_s5": report["repair"]["distinct_unknown_s5"],
        "next_target": report["next_target"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

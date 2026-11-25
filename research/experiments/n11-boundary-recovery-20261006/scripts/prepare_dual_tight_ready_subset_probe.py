#!/usr/bin/env python3
"""Select a low-cost probe only from a dual-tight class's audited ready keys."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

from audit_probe_preflight import validate_audits
from verify_raw_history_coverage import verify_coverage


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(_PolicyPath(__file__).resolve().parents[4] / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import quarantined_cache_keys

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise ValueError(f"n=11 key out of range: {key}")
    return tuple([i for i in range(64) if lo >> i & 1]
                 + [64 + i for i in range(57) if hi >> i & 1])


def read_exact_cache(path: Path) -> dict[tuple[int, int], int]:
    _s5_quarantine = quarantined_cache_keys()
    result: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise SystemExit(f"invalid cache row {line_no}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if key in _s5_quarantine:
                continue
            if verdict not in (1, 2):
                raise SystemExit(f"non-exact cache row {line_no}: {row}")
            old = result.get(key)
            if old is not None and old != verdict:
                raise SystemExit(f"cache conflict for {key}: {old} vs {verdict}")
            result[key] = verdict
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--class-lo", type=int, required=True)
    parser.add_argument("--class-hi", type=int, required=True)
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--ranking", type=Path, required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--raw-audit", type=Path, required=True)
    parser.add_argument("--historical-raw-audit", type=Path, required=True)
    parser.add_argument("--saved-s6-audit", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--solver-source", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--probe-out", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, required=True)
    parser.add_argument("--budget", type=int, default=15_000_000)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if min(args.count, args.budget, args.workers) < 1:
        parser.error("count, budget and workers must be positive")
    if args.probe_out.exists() or args.manifest_out.exists():
        raise SystemExit("refusing to overwrite existing probe input or manifest")
    if not all(path.is_file() for path in
               (args.solver, args.solver_source, args.runner)):
        raise SystemExit("solver, source, or runner file is missing")

    ranking = json.loads(args.ranking.read_text(encoding="utf-8"))
    wanted_class = [args.class_lo, args.class_hi]
    best = ranking.get("next_target", {})
    if best.get("key") != wanted_class or best.get("unknown_s5", 0) <= 0:
        raise SystemExit(f"requested class is not the saved next target: {best.get('key')}")

    with args.targets.open(newline="", encoding="utf-8-sig") as stream:
        rows = [row for row in csv.reader(stream)
                if row and not row[0].lstrip().startswith("#")]
    if len(rows) != best["unknown_s5"]:
        raise SystemExit(f"full UNKNOWN target count mismatch: {len(rows)} != {best['unknown_s5']}")
    keyed: dict[tuple[int, int], list[str]] = {}
    legal_counts: dict[tuple[int, int], int] = {}
    for line_no, row in enumerate(rows, 1):
        if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
            raise SystemExit(f"invalid s5 target row {line_no}: {row}")
        key = (int(row[3]), int(row[4]))
        pts = points(key)
        if (len(pts) != 5 or has_forbidden_quad(pts)
                or tuple(d4_canonical_key(pts)) != key):
            raise SystemExit(f"unsafe/noncanonical s5 target: {key}")
        actual_legal = len(legal_after(set(pts)))
        if int(row[5]) != actual_legal:
            raise SystemExit(f"legal-count mismatch for {key}: {row[5]} != {actual_legal}")
        if key in keyed:
            raise SystemExit(f"duplicate s5 target: {key}")
        keyed[key] = row
        legal_counts[key] = actual_legal
    target_keys = set(keyed)

    cache = read_exact_cache(args.cache)
    if target_keys & cache.keys():
        raise SystemExit(f"target unexpectedly exact in cache: {sorted(target_keys & cache.keys())[:3]}")

    raw = json.loads(args.raw_audit.read_text(encoding="utf-8"))
    historical = json.loads(args.historical_raw_audit.read_text(encoding="utf-8"))
    coverage = verify_coverage(historical, raw, ROOT)
    if coverage["status"] != "PASS":
        raise SystemExit(
            "historical replay sources incomplete: "
            f"{coverage['missing_csv']} missing, "
            f"{coverage['missing_s5_replay_rows']} s5 replay rows lost, "
            f"{coverage['altered_csv']} altered; refusing schedule"
        )
    saved = json.loads(args.saved_s6_audit.read_text(encoding="utf-8"))
    try:
        ready, same_budget_keys = validate_audits(
            target_keys, sha256(args.targets), sha256(args.cache),
            raw, saved, args.budget,
        )
    except ValueError as exc:
        raise SystemExit(f"dual-tight ready-subset preflight failed: {exc}") from exc
    if len(ready) < args.count:
        raise SystemExit(f"only {len(ready)} targets are dispatch-ready; requested {args.count}")
    same_budget_rows = raw.get("prior_unknown_same_budget_or_higher", [])

    eligible_rows = [keyed[key] for key in ready]
    chosen = sorted(eligible_rows,
                    key=lambda row: (int(row[5]), int(row[3]), int(row[4])))[:args.count]
    args.probe_out.parent.mkdir(parents=True, exist_ok=True)
    with args.probe_out.open("w", newline="", encoding="utf-8") as stream:
        stream.write("# audited dual-tight low-legal-count probe; order is scheduling only\n")
        csv.writer(stream, lineterminator="\n").writerows(chosen)

    source_paths = [args.targets, args.ranking, args.cache, args.raw_audit,
                    args.historical_raw_audit, Path(__file__).with_name("verify_raw_history_coverage.py"),
                    args.saved_s6_audit, args.solver, args.solver_source,
                    args.runner, Path(__file__).resolve()]
    manifest = {
        "schema": "n11-dual-tight-ready-subset-probe-manifest-v1",
        "class_key": wanted_class,
        "class_rank": best.get("rank"),
        "canonical_s5_children": best.get("canonical_s5_children"),
        "known_loss_s5": best.get("known_loss_s5"),
        "unknown_s5_before_probe": len(target_keys),
        "dispatch_ready_s5": len(ready),
        "probe_count": len(chosen),
        "selection_rule": "among raw-history dispatch-ready UNKNOWN parents, sort by (legal move count, canonical key), then take the first count",
        "probe_targets": [[int(row[3]), int(row[4])] for row in chosen],
        "excluded_same_or_higher_budget_unknown_keys": [list(key) for key in sorted(same_budget_keys)],
        "same_budget_unknown_observations": same_budget_rows,
        "probe_target_sha256": sha256(args.probe_out),
        "budget_per_target": args.budget,
        "workers": args.workers,
        "solver_command": f"{rel(args.runner)} --solver {rel(args.solver)} --targets {rel(args.probe_out)} --cache {rel(args.cache)} --out-dir .local/n11/dual-tight-ready-{args.class_lo}-{args.class_hi}-probe8 --workers {args.workers} --budget {args.budget}",
        "sources": [{"path": rel(path), "sha256": sha256(path)} for path in source_paths],
        "claim": "Probe order carries no verdict. Prior same-or-higher-budget UNKNOWN keys are excluded, and only exact solver results may update class status.",
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")
    print(json.dumps({"class_key": wanted_class, "unknown_targets": len(target_keys),
                      "dispatch_ready": len(ready), "excluded_unknown": sorted(same_budget_keys),
                      "probe_count": len(chosen), "probe_keys": manifest["probe_targets"],
                      "manifest": rel(args.manifest_out)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

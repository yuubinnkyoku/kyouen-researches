#!/usr/bin/env python3
"""Select a small, cache- and history-audited probe from a dual-tight class."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from audit_probe_preflight import validate_audits
from verify_raw_history_coverage import verify_coverage


ROOT = Path(__file__).resolve().parents[4]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--class-lo", type=int, required=True)
    ap.add_argument("--class-hi", type=int, required=True)
    ap.add_argument("--count", type=int, default=8)
    ap.add_argument("--targets", type=Path, required=True)
    ap.add_argument("--ranking", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--raw-audit", type=Path, required=True)
    ap.add_argument("--historical-raw-audit", type=Path, required=True)
    ap.add_argument("--saved-s6-audit", type=Path, required=True)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--solver-source", type=Path, required=True)
    ap.add_argument("--runner", type=Path, required=True)
    ap.add_argument("--probe-out", type=Path, required=True)
    ap.add_argument("--manifest-out", type=Path, required=True)
    ap.add_argument("--budget", type=int, default=15_000_000)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    if args.count < 1 or args.budget < 1 or args.workers < 1:
        ap.error("count, budget and workers must be positive")
    if args.probe_out.exists() or args.manifest_out.exists():
        raise SystemExit("refusing to overwrite existing probe input or manifest")
    if not args.solver.is_file() or not args.solver_source.is_file() or not args.runner.is_file():
        raise SystemExit("solver, source, or runner file is missing")

    ranking = json.loads(args.ranking.read_text(encoding="utf-8"))
    wanted_class = [args.class_lo, args.class_hi]
    best = ranking.get("next_target", {})
    if best.get("key") != wanted_class:
        raise SystemExit(f"requested class is not the saved next target: {best.get('key')}")
    if best.get("unknown_s5") <= 0:
        raise SystemExit("selected class has no UNKNOWN s5 targets")

    with args.targets.open(newline="", encoding="utf-8-sig") as stream:
        rows = [row for row in csv.reader(stream) if row and not row[0].lstrip().startswith("#")]
    if len(rows) != best["unknown_s5"]:
        raise SystemExit(f"target count does not match ranking: {len(rows)} != {best['unknown_s5']}")
    keyed = {}
    for line_no, row in enumerate(rows, 1):
        if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
            raise SystemExit(f"invalid s5 target row {line_no}: {row}")
        key = (int(row[3]), int(row[4]))
        if key in keyed:
            raise SystemExit(f"duplicate s5 target: {key}")
        keyed[key] = row
    target_keys = set(keyed)

    cache = {}
    for line_no, row in enumerate(csv.reader(args.cache.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid s5 cache row {line_no}: {row}")
        key, verdict = (int(row[1]), int(row[2])), int(row[4])
        old = cache.get(key)
        if old is not None and old != verdict:
            raise SystemExit(f"cache verdict conflict: {key}")
        cache[key] = verdict
    if target_keys & cache.keys():
        raise SystemExit(f"s5 target unexpectedly exact in cache: {sorted(target_keys & cache.keys())[:3]}")

    raw_audit = json.loads(args.raw_audit.read_text(encoding="utf-8"))
    historical = json.loads(args.historical_raw_audit.read_text(encoding="utf-8"))
    coverage = verify_coverage(historical, raw_audit, ROOT)
    if coverage["status"] != "PASS":
        raise SystemExit(
            "historical replay sources incomplete: "
            f"{coverage['missing_csv']} missing, "
            f"{coverage['missing_s5_replay_rows']} s5 replay rows lost, "
            f"{coverage['altered_csv']} altered; refusing schedule"
        )
    saved = json.loads(args.saved_s6_audit.read_text(encoding="utf-8"))
    try:
        ready, blocked = validate_audits(
            target_keys, sha256(args.targets), sha256(args.cache),
            raw_audit, saved, args.budget,
        )
    except ValueError as exc:
        raise SystemExit(f"dual-tight probe preflight failed: {exc}") from exc

    # A previous same-or-higher-budget UNKNOWN is not a verdict and is not
    # eligible for a repeated direct replay at the same budget.
    chosen = sorted((keyed[key] for key in ready),
                    key=lambda row: (int(row[5]), int(row[3]), int(row[4])))[:args.count]
    if not chosen:
        raise SystemExit("probe selection is empty")
    args.probe_out.parent.mkdir(parents=True, exist_ok=True)
    with args.probe_out.open("w", newline="", encoding="utf-8",) as stream:
        stream.write("# dual-tight class low-legal-count probe; order is scheduling only\n")
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerows(chosen)

    source_paths = [args.targets, args.ranking, args.cache, args.raw_audit,
                    args.historical_raw_audit, Path(__file__).with_name("verify_raw_history_coverage.py"),
                    args.saved_s6_audit, args.solver, args.solver_source,
                    args.runner, Path(__file__).resolve()]
    manifest = {
        "schema": "n11-dual-tight-class-probe-input-manifest-v1",
        "class_key": wanted_class,
        "class_rank": best.get("rank"),
        "canonical_s5_children": best.get("canonical_s5_children"),
        "known_loss_s5": best.get("known_loss_s5"),
        "unknown_s5_before_probe": len(rows),
        "dispatch_ready_count": len(ready),
        "excluded_same_budget_unknown_count": len(blocked),
        "excluded_same_budget_unknown_keys": [list(key) for key in sorted(blocked)],
        "probe_count": len(chosen),
        "selection_rule": "sort audited UNKNOWN s5 targets by (legal move count, canonical key), then take the first count; scheduling heuristic only",
        "probe_targets": [[int(row[3]), int(row[4])] for row in chosen],
        "probe_target_sha256": sha256(args.probe_out),
        "budget_per_target": args.budget,
        "workers": args.workers,
        "solver_command": f"{rel(args.runner)} --solver {rel(args.solver)} --targets {rel(args.probe_out)} --cache {rel(args.cache)} --out-dir .local/n11/dual-tight-repair-{args.class_lo}-{args.class_hi}-probe8 --workers {args.workers} --budget {args.budget}",
        "sources": [{"path": rel(path), "sha256": sha256(path)} for path in source_paths],
        "claim": "Probe order carries no verdict. Only exact solver results may update the class status.",
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")
    print(json.dumps({"class_key": wanted_class, "target_count": len(rows),
                      "probe_count": len(chosen), "probe_keys": manifest["probe_targets"],
                      "manifest": rel(args.manifest_out)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

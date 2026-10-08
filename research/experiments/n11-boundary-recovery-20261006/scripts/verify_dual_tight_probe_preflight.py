#!/usr/bin/env python3
"""Bind one scheduled s5 probe to exact-cache, replay-history, and saved-s6 audits."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"
EDGE = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(EDGE))
from audit_probe_preflight import validate_audits  # noqa: E402
from verify_raw_history_coverage import verify_coverage  # noqa: E402
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise SystemExit(f"n=11 key out of range: {key}")
    return tuple([i for i in range(64) if lo >> i & 1]
                 + [64 + i for i in range(57) if hi >> i & 1])


def read_targets(path: Path) -> tuple[list[tuple[int, int]], dict[tuple[int, int], int]]:
    keys = []
    legal_counts = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
                raise SystemExit(f"invalid scheduled s5 target at {path}:{line_no}: {row}")
            key = (int(row[3]), int(row[4]))
            occupied = set(points(key))
            legal = len(legal_after(occupied))
            if (len(occupied) != 5 or has_forbidden_quad(occupied)
                    or tuple(d4_canonical_key(occupied)) != key
                    or int(row[5]) != legal or key in legal_counts):
                raise SystemExit(f"unsafe, noncanonical, duplicate, or illegal target: {key}")
            keys.append(key)
            legal_counts[key] = legal
    if not keys:
        raise SystemExit("empty scheduled target file")
    return keys, legal_counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--schedule-manifest", type=Path, required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--raw-audit", type=Path, required=True)
    parser.add_argument("--historical-raw-audit", type=Path, required=True,
                        help="immutable earlier full-source inventory for identical targets/cache")
    parser.add_argument("--saved-s6-audit", type=Path, required=True)
    parser.add_argument("--budget", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite preflight report: {args.out}")

    target_keys, legal_counts = read_targets(args.targets)
    target_sha = sha256(args.targets)
    cache_sha = sha256(args.cache)
    schedule = json.loads(args.schedule_manifest.read_text(encoding="utf-8"))
    if (schedule.get("probe_target_sha256") != target_sha
            or schedule.get("budget_per_target") != args.budget
            or [tuple(k) for k in schedule.get("probe_targets", [])] != target_keys):
        raise SystemExit("scheduled targets differ from the immutable probe manifest")

    raw = json.loads(args.raw_audit.read_text(encoding="utf-8"))
    historical = json.loads(args.historical_raw_audit.read_text(encoding="utf-8"))
    coverage = verify_coverage(historical, raw, ROOT)
    if coverage["status"] != "PASS":
        raise SystemExit(
            "historical replay-source coverage incomplete: "
            f"{coverage['missing_csv']} missing CSV "
            f"({coverage['missing_s5_replay_rows']} s5 replay rows), "
            f"{coverage['altered_csv']} altered CSV; refusing dispatch"
        )
    # Require the audit's own recorded budget; do not invent an attestation.
    saved = json.loads(args.saved_s6_audit.read_text(encoding="utf-8"))
    ready, blocked = validate_audits(
        target_keys, target_sha, cache_sha, raw, saved, args.budget)

    raw_script = SCRIPTS / "audit_s5_raw_history.py"
    saved_script = SCRIPTS / "audit_saved_s6_targets.py"
    validator_script = SCRIPTS / "audit_probe_preflight.py"
    inputs = [args.targets, args.schedule_manifest, args.cache, args.raw_audit,
              args.historical_raw_audit, SCRIPTS / "verify_raw_history_coverage.py",
              args.saved_s6_audit, raw_script, saved_script, validator_script,
              Path(__file__).resolve(), EDGE / "dfpn_edge_classes.py"]
    report = {
        "schema": "n11-dual-tight-probe-preflight-binding-v1",
        "class_key": schedule.get("class_key"),
        "target_count": len(target_keys),
        "target_sha256": target_sha,
        "exact_cache_sha256": cache_sha,
        "budget": args.budget,
        "historical_source_coverage": {
            "reference_csv": coverage["reference_csv"],
            "current_csv": coverage["current_csv"],
            "new_csv": coverage["new_csv"],
            "normalized_crlf_to_lf": coverage["normalized_crlf_to_lf"],
            "missing_csv": coverage["missing_csv"],
            "altered_csv": coverage["altered_csv"],
            "status": coverage["status"],
        },
        "budget_binding": "The saved raw-history audit attests its own requested_budget; this value must match the dispatch budget. Legacy budgetless audits are rejected and must be regenerated.",
        "ready_keys": [list(key) for key in sorted(ready)],
        "blocked_same_or_higher_budget_unknown_keys": [list(key) for key in sorted(blocked)],
        "target_legal_counts": {f"{key[0]},{key[1]}": legal_counts[key]
                                 for key in target_keys},
        "raw_history": {
            "rows_examined": raw.get("s5_replay_rows_examined"),
            "csv_files_examined": raw.get("csv_files_examined"),
            "prior_exact": len(raw.get("prior_exact", {})),
            "same_or_higher_budget_unknown_rows": len(
                raw.get("prior_unknown_same_budget_or_higher", [])),
            "conflicts": len(raw.get("exact_verdict_conflicts", [])),
        },
        "saved_s6": {
            "source_files": saved.get("source_audit", {}).get("source_file_count"),
            "parents": len(saved.get("targets", {}).get("parents", [])),
            "unknown_parents": saved.get("cache_comparison", {}).get("unknown_parents"),
            "new_exact": saved.get("cache_comparison", {}).get("new_exact"),
            "conflicts": len(saved.get("cache_comparison", {}).get(
                "opposite_verdict_conflicts", [])),
        },
        "sources": [{"path": rel(path), "sha256": sha256(path),
                     "bytes": path.stat().st_size} for path in inputs],
        "claim": "Preflight only; it classifies no game outcomes. Same-budget UNKNOWN remains blocked and every scheduled target remains UNKNOWN until an exact replay or valid s6 witness is found.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    print(json.dumps({"schema": report["schema"], "targets": len(target_keys),
                      "ready": len(ready), "blocked": len(blocked),
                      "saved_s6_unknown": report["saved_s6"]["unknown_parents"],
                      "conflicts": 0, "out": rel(args.out)}, sort_keys=True))
    print("DUAL_TIGHT_PROBE_PREFLIGHT_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

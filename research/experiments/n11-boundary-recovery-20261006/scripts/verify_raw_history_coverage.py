#!/usr/bin/env python3
"""Require a new n11 replay-history audit to cover every historical CSV source.

A hash may differ solely because Git normalized CRLF to LF. That exception is
verified against the historical SHA-256 by restoring CRLF in memory; other
content changes, missing sources and replay-row-count changes fail closed.
The reference is a historical *source inventory*, not a verdict certificate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _indexed(audit: dict, label: str) -> dict[str, dict]:
    if audit.get("schema") != "n11-s5-raw-history-audit-v1":
        raise ValueError(f"{label}: unexpected audit schema")
    rows = audit.get("scanned_csv_sources")
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{label}: missing source inventory")
    result = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"{label}: malformed inventory entry")
        path = row.get("path")
        digest = row.get("sha256")
        size = row.get("bytes")
        count = row.get("s5_replay_rows")
        if (not isinstance(path, str) or not path.endswith(".csv")
                or not isinstance(digest, str) or len(digest) != 64
                or any(c not in "0123456789abcdef" for c in digest)
                or type(size) is not int or size < 0
                or type(count) is not int or count < 0
                or path in result):
            raise ValueError(f"{label}: duplicate/malformed inventory item: {path!r}")
        result[path] = row
    if (audit.get("csv_files_examined") != len(rows)
            or audit.get("s5_replay_rows_examined") !=
            sum(row["s5_replay_rows"] for row in rows)):
        raise ValueError(f"{label}: summary totals do not equal source inventory")
    return result


def verify_coverage(reference: dict, current: dict, root: Path) -> dict:
    """Audit published historical sources vs a new locally recomputed audit.

    Missing or changed sources are reported rather than silently excluded.
    Only *verified* CRLF -> LF normalization is accepted. The current report
    must be tied to the same targets/cache and attest its own positive budget.
    """
    previous = _indexed(reference, "reference")
    observed = _indexed(current, "current")
    if (reference.get("targets") != current.get("targets")
            or reference.get("current_cache", {}).get("sha256")
            != current.get("current_cache", {}).get("sha256")):
        raise ValueError("source inventories refer to different targets or exact cache")
    if type(current.get("requested_budget")) is not int or current["requested_budget"] < 1:
        raise ValueError("current raw audit must attest a positive requested_budget")
    root = root.resolve()
    missing = sorted(previous.keys() - observed.keys())
    added = sorted(observed.keys() - previous.keys())
    altered = []
    normalized = []
    for relpath, entry in sorted(observed.items()):
        path = Path(relpath)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"source escapes repository: {relpath}")
        full = (root / path).resolve()
        if not full.is_relative_to(root) or not full.is_file():
            altered.append(relpath + " (source absent from checkout)")
            continue
        data = full.read_bytes()
        if sha(data) != entry["sha256"] or len(data) != entry["bytes"]:
            altered.append(relpath + " (current report does not match source)")
            continue
        old = previous.get(relpath)
        if old is None:
            continue
        if entry["s5_replay_rows"] != old["s5_replay_rows"]:
            altered.append(relpath + " (s5 replay row count changed)")
        elif entry["sha256"] == old["sha256"] and entry["bytes"] == old["bytes"]:
            continue
        elif (b"\r" not in data and b"\n" in data
              and len(data) + data.count(b"\n") == old["bytes"]
              and sha(data.replace(b"\n", b"\r\n")) == old["sha256"]):
            normalized.append(relpath)
        else:
            altered.append(relpath + " (content differs beyond CRLF to LF)")
    report = {
        "schema": "n11-raw-history-source-coverage-v1",
        "reference_csv": len(previous),
        "current_csv": len(observed),
        "missing_csv": len(missing),
        "missing_s5_replay_rows": sum(previous[p]["s5_replay_rows"] for p in missing),
        "new_csv": len(added),
        "normalized_crlf_to_lf": len(normalized),
        "altered_csv": len(altered),
        "missing_paths": missing,
        "altered_paths": altered,
        "status": "PASS" if not missing and not altered else "FAIL",
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path,
                        default=Path(__file__).resolve().parents[4])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    baseline = json.loads(args.reference.read_text(encoding="utf-8"))
    now = json.loads(args.current.read_text(encoding="utf-8"))
    report = verify_coverage(baseline, now, args.repo_root)
    if args.out:
        if args.out.exists():
            parser.error(f"refusing to overwrite report: {args.out}")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("missing_paths", "altered_paths")},
                     sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

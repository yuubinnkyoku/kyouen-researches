#!/usr/bin/env python3
"""Audit saved CSV replay redundancy for vanished n11 local s5 source files.

Checks key-level evidence, not byte-level recovery or independent solver proofs.
An unresolved/UNKNOWN solver row never becomes a WIN/LOSS verdict.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad  # noqa: E402

S5_FILE = re.compile(r"(?:^|/)s5-(\d+)-(\d+)\.out\.csv$")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def geometry(key: tuple[int, int]) -> bool:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        return False
    points = [i for i in range(64) if lo >> i & 1]
    points += [i + 64 for i in range(57) if hi >> i & 1]
    return (len(points) == 5 and not has_forbidden_quad(points)
            and tuple(d4_canonical_key(points)) == key)


def missing_s5_keys(inventory: dict, *, local_prefix: str = ".local/n11/"):
    if inventory.get("schema") != "n11-s5-raw-history-audit-v1":
        raise ValueError("unexpected history audit schema")
    sources = inventory.get("scanned_csv_sources", [])
    missing = [row for row in sources if row.get("path", "").startswith(local_prefix)]
    if not missing:
        raise ValueError("reference contains no vanished local source entries")
    keys = {}
    for row in missing:
        count = row.get("s5_replay_rows")
        if type(count) is not int or count < 0:
            raise ValueError("invalid recorded s5 replay count")
        if count == 0:
            continue
        if count != 1:
            raise ValueError("non-singleton missing s5 file needs explicit reconstruction")
        m = S5_FILE.search(row["path"])
        if m is None:
            raise ValueError(f"cannot derive missing replay key: {row['path']}")
        key = int(m[1]), int(m[2])
        if not geometry(key) or key in keys:
            raise ValueError(f"unsafe, noncanonical or duplicate missing key: {key}")
        keys[key] = row["path"]
    return missing, keys


def read_exact_cache(path: Path):
    results = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for number, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or row[3] != "5":
                raise ValueError(f"malformed exact cache at {path}:{number}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if verdict not in (1, 2) or not geometry(key):
                raise ValueError(f"invalid exact s5 cache entry: {key}")
            if key in results and results[key] != verdict:
                raise ValueError(f"conflicting exact cache verdict: {key}")
            results[key] = verdict
    return results


def analyze(reference: dict, raw_root: Path, cache_file: Path, *, base: Path = ROOT):
    """Use a historical path/key inventory and current durable replay sources."""
    missing, missing_keys = missing_s5_keys(reference)
    cache = read_exact_cache(cache_file)
    rows_by_key = defaultdict(list)
    examined_csv = 0
    examined_s5_replays = 0
    for path in sorted(raw_root.rglob("*.csv")):
        if not path.is_file():
            continue
        examined_csv += 1
        matches = []
        with path.open(encoding="utf-8-sig", newline="") as stream:
            for line_no, row in enumerate(csv.reader(stream), 1):
                if not row or row[0] != "replay":
                    continue
                if len(row) != 11:
                    raise ValueError(f"malformed replay row: {path}:{line_no}")
                if row[2] != "5" or row[4] != "0":
                    continue
                examined_s5_replays += 1
                key = int(row[9]), int(row[10])
                if key not in missing_keys:
                    continue
                budget, verdict, nodes = int(row[5]), int(row[6]), int(row[7])
                if budget < 1 or verdict not in (0, 1, 2) or nodes < 0:
                    raise ValueError(f"invalid replay result: {path}:{line_no}")
                matches.append((key, {
                    "path": path.resolve().relative_to(base.resolve()).as_posix(),
                    "line": line_no, "budget": budget, "verdict": verdict,
                    "nodes": nodes, "sha256": None,
                }))
        if matches:
            hash_value = digest(path)
            for key, receipt in matches:
                receipt["sha256"] = hash_value
                rows_by_key[key].append(receipt)

    conflicts = []
    recovered = {}
    for key, oldpath in sorted(missing_keys.items()):
        saved = rows_by_key.get(key, [])
        exact = {r["verdict"] for r in saved if r["verdict"] in (1, 2)}
        value = cache.get(key)
        if len(exact) > 1 or (value is not None and exact and value not in exact):
            conflicts.append(list(key))
        recovered[f"{key[0]},{key[1]}"] = {
            "missing_path": oldpath,
            "cache_exact_verdict": value,
            "saved_replays": saved,
            "saved_exact_values": sorted(exact),
        }

    uncached = [row for row in recovered.values() if row["cache_exact_verdict"] is None]
    unresolved = [row for row in uncached if (
        not row["saved_replays"] or
        any(replay["verdict"] != 0 for replay in row["saved_replays"]) or
        any(replay["budget"] < 15_000_000 for replay in row["saved_replays"])
    )]
    unobserved = [row for row in recovered.values() if not row["saved_replays"]]
    # All original raw files remain absent: matching a canonical key elsewhere
    # does not prove that the old row bytes/verdict were identical.
    report = {
        "schema": "n11-missing-s5-replay-redundancy-v1",
        "historical_audit_sha256": None,
        "exact_cache_path": cache_file.resolve().relative_to(base.resolve()).as_posix(),
        "exact_cache_sha256": digest(cache_file),
        "replay_root": raw_root.resolve().relative_to(base.resolve()).as_posix(),
        "csv_scanned": examined_csv,
        "s5_replays_scanned": examined_s5_replays,
        "historical_missing_local_csv": len(missing),
        "historical_missing_zero_s5_csv": sum(r["s5_replay_rows"] == 0 for r in missing),
        "historical_missing_one_s5_csv": len(missing_keys),
        "missing_keys_with_saved_raw": len(recovered) - len(unobserved),
        "missing_keys_already_exact_in_cache": len(missing_keys) - len(uncached),
        "uncached_keys_with_only_saved_15m_unknown": len(uncached) - len(unresolved),
        "uncached_keys_without_sufficient_saved_raw": len(unresolved),
        "saved_exact_cache_conflicts": conflicts,
        "missing_saved_raw_keys": [
            key for key, row in recovered.items() if not row["saved_replays"]],
        "status": "KEY_EVIDENCE_COMPLETE" if not unobserved and not conflicts and not unresolved
                  else "INCOMPLETE",
        "claim_limit": "Key-level duplicate observational evidence only: no lost CSV bytes recovered, no new exact verdicts, no solver reproof, no historical source-coverage gate override.",
        "keys": recovered,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--historical-audit", type=Path, required=True)
    parser.add_argument("--saved-raw-root", type=Path, required=True)
    parser.add_argument("--exact-cache", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error(f"will not overwrite report: {args.out}")
    ref = json.loads(args.historical_audit.read_text(encoding="utf-8"))
    report = analyze(ref, args.saved_raw_root, args.exact_cache)
    report["historical_audit_sha256"] = digest(args.historical_audit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n",
                        encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items()
                      if key != "keys"}, sort_keys=True))
    return 0 if report["status"] == "KEY_EVIDENCE_COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())

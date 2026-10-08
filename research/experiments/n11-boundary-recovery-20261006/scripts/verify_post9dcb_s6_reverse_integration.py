#!/usr/bin/env python3
"""Independently bind saved next17 s6 LOSS witnesses to legal canonical s5 parents."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE = ROOT / "research/experiments/n11-search-methods/scripts"
FRONTIER = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"
sys.path.insert(0, str(EDGE))
sys.path.insert(0, str(FRONTIER))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402
from derive_shared_s6_witness_cache import canonical_safe_key, points_from_key  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def git_blob(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path)], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def read_cache(path: Path) -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.reader(stream):
            if not row or row[0].startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise ValueError(f"not an s5 cache row: {path}: {row}")
            key = (int(row[1]), int(row[2]))
            verdict = int(row[4])
            if verdict not in (1, 2) or key in result:
                raise ValueError(f"invalid or duplicate exact cache row: {path}: {row}")
            if canonical_safe_key(key, 5) != key:
                raise ValueError(f"noncanonical or unsafe s5 key: {path}: {key}")
            result[key] = verdict
    return result


def read_s6_sources(items: list[dict], *, verify_legal_counts: bool) -> tuple[dict, list[dict]]:
    observations: dict[tuple[int, int], list[dict]] = defaultdict(list)
    verified = []
    for item in items:
        source_text = item.get("path", "").replace("\\", "/")
        path = (ROOT / source_text).resolve()
        if not path.is_file() or sha(path) != item.get("sha256"):
            raise ValueError(f"saved s6 source missing or hash mismatch: {source_text}")
        row_count = 0
        per_file = Counter()
        with path.open(newline="", encoding="utf-8-sig") as stream:
            for line, row in enumerate(csv.reader(stream), 1):
                if not row or row[0] != "replay" or len(row) < 3 or row[2] != "6":
                    continue
                if len(row) != 11 or int(row[4]) != 1:
                    raise ValueError(f"invalid saved s6 OR replay: {source_text}:{line}")
                raw_key = (int(row[9]), int(row[10]))
                points = points_from_key(raw_key)
                if len(points) != 6 or has_forbidden_quad(points):
                    raise ValueError(f"unsafe saved s6: {source_text}:{line} {raw_key}")
                key = canonical_safe_key(raw_key, 6)
                if verify_legal_counts and len(legal_after(set(points))) != int(row[3]):
                    raise ValueError(f"saved s6 legal-count mismatch: {source_text}:{line}")
                verdict = int(row[6])
                nodes = int(row[7])
                if verdict not in (0, 1, 2) or nodes < 0:
                    raise ValueError(f"invalid saved s6 result: {source_text}:{line}")
                observations[key].append({"verdict": verdict, "source": source_text, "line": line})
                per_file[str(verdict)] += 1
                row_count += 1
        if row_count != item.get("s6_replay_rows"):
            raise ValueError(f"saved s6 row-count mismatch: {source_text}: {row_count}")
        verified.append({"path": source_text, "sha256": sha(path), "s6_replay_rows": row_count,
                         "verdict_counts": dict(sorted(per_file.items()))})
    return observations, verified


def summarize_s6(observations: dict) -> dict:
    counts = Counter()
    conflicts = []
    for key, rows in observations.items():
        exact = {row["verdict"] for row in rows if row["verdict"] in (1, 2)}
        if len(exact) > 1:
            conflicts.append(list(key))
        elif exact:
            counts[str(next(iter(exact)))] += 1
        else:
            counts["0"] += 1
    if conflicts:
        raise ValueError(f"saved s6 exact WIN/LOSS conflicts: {conflicts[:3]}")
    return {
        "all_s6_exact_rows_geometry_checked": True,
        "exact_conflict_count": 0,
        "unique_canonical_keys": len(observations),
        "unique_win_keys": counts["1"],
        "unique_loss_keys": counts["2"],
        "unknown_only_keys": counts["0"],
        "verdict_counts_by_unique_key": {k: counts[k] for k in ("1", "2") if counts[k]},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reverse-audit", type=Path, required=True)
    ap.add_argument("--s6-raw", type=Path, required=True)
    ap.add_argument("--baseline-cache", type=Path, required=True)
    ap.add_argument("--local-cache", type=Path, required=True)
    ap.add_argument("--delta-cache", type=Path, required=True)
    ap.add_argument("--merged-cache", type=Path, required=True)
    ap.add_argument("--previous-saved-s6-audit", type=Path, required=True)
    ap.add_argument("--combined-saved-s6-audit-out", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    report = json.loads(args.reverse_audit.read_text(encoding="utf-8"))
    if report.get("schema") != "n11-next17-partial-s6-reverse-loss-v1":
        raise ValueError("unexpected reverse-audit schema")
    if report.get("source_sha256") != sha(args.s6_raw):
        raise ValueError("reverse-audit s6 raw SHA-256 mismatch")
    if report.get("baseline_sha256") != sha(args.baseline_cache):
        raise ValueError("reverse-audit baseline cache SHA-256 mismatch")
    if report.get("source_git_blob_sha") != git_blob(args.s6_raw):
        raise ValueError("reverse-audit s6 raw Git blob mismatch")
    if report.get("delta_cache_git_blob_sha") != git_blob(args.delta_cache):
        raise ValueError("reverse-audit derived delta Git blob mismatch")

    previous_audit = json.loads(args.previous_saved_s6_audit.read_text(encoding="utf-8"))
    previous_sources = previous_audit.get("sources")
    previous_s6 = previous_audit.get("s6", {})
    if (not isinstance(previous_sources, list) or not previous_sources
            or not previous_s6.get("all_s6_exact_rows_geometry_checked")):
        raise ValueError("previous saved-s6 source audit lacks complete geometry attestation")
    new_source = {
        "path": str(report["source"]).replace("\\", "/"),
        "sha256": report["source_sha256"],
        "s6_replay_rows": report["source_replay_rows"],
    }
    source_paths = {item.get("path", "").replace("\\", "/") for item in previous_sources}
    if new_source["path"] in source_paths:
        raise ValueError("new s6 raw source is already in prior saved-s6 audit")
    old_observations, old_verified_sources = read_s6_sources(previous_sources, verify_legal_counts=False)
    old_summary = summarize_s6(old_observations)
    for key in ("unique_canonical_keys", "unique_win_keys", "unique_loss_keys", "unknown_only_keys",
                "exact_conflict_count", "verdict_counts_by_unique_key"):
        if old_summary[key] != previous_s6.get(key):
            raise ValueError(f"rehydrated previous saved-s6 summary mismatch: {key}")
    new_observations, new_verified_sources = read_s6_sources([new_source], verify_legal_counts=True)
    combined_observations: dict[tuple[int, int], list[dict]] = defaultdict(list)
    for key, rows_for_key in old_observations.items():
        combined_observations[key].extend(rows_for_key)
    for key, rows_for_key in new_observations.items():
        combined_observations[key].extend(rows_for_key)
    combined_verified_sources = old_verified_sources + new_verified_sources
    combined_s6 = summarize_s6(combined_observations)
    if args.combined_saved_s6_audit_out.exists():
        raise SystemExit(f"refusing to overwrite combined source audit: {args.combined_saved_s6_audit_out}")
    combined_sources_audit = {
        "schema": "n11-saved-s6-source-audit-with-next17-hard5-v1",
        "source_file_count": len(combined_verified_sources),
        "source_hashes_validated": True,
        "sources": combined_verified_sources,
        "s6": combined_s6,
        "augmentation_provenance": {
            "previous_source_audit": relative(args.previous_saved_s6_audit),
            "previous_source_audit_sha256": sha(args.previous_saved_s6_audit),
            "new_source": new_source,
            "geometry_check": "All source rows were re-read; canonical safety and legal counts were checked using exact n=11 integer geometry. Exact solver verdicts remain source evidence.",
        },
    }
    args.combined_saved_s6_audit_out.parent.mkdir(parents=True, exist_ok=True)
    args.combined_saved_s6_audit_out.write_text(
        json.dumps(combined_sources_audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    rows: dict[int, list[str]] = {}
    with args.s6_raw.open(newline="", encoding="utf-8") as stream:
        for line, row in enumerate(csv.reader(stream), 1):
            rows[line] = row
    delta = read_cache(args.delta_cache)
    parent_witnesses: dict[tuple[int, int], set[tuple[int, int]]] = {}
    checked_lines: set[int] = set()
    source_loss_rows: set[tuple[int, int]] = set()

    for witness in report.get("witnesses", []):
        parent = tuple(map(int, witness["s5_key"]))
        if canonical_safe_key(parent, 5) != parent:
            raise ValueError(f"noncanonical/unsafe parent in audit: {parent}")
        witnesses = witness.get("s6_loss_witnesses", [])
        if not witnesses:
            raise ValueError(f"s5 parent lacks a LOSS witness: {parent}")
        for item in witnesses:
            line = int(item["line"])
            row = rows.get(line)
            if row is None or len(row) != 11 or row[0] != "replay":
                raise ValueError(f"missing/malformed s6 replay row at line {line}")
            if int(row[2]) != 6 or int(row[4]) != 1 or int(row[6]) != 2:
                raise ValueError(f"witness row is not an exact s6 OR LOSS: line {line}")
            raw_s6 = (int(row[9]), int(row[10]))
            s6 = canonical_safe_key(raw_s6, 6)
            audited_s6 = tuple(map(int, item["s6_key"]))
            if s6 != audited_s6:
                raise ValueError(f"audit/raw s6 key mismatch at line {line}: {s6} != {audited_s6}")
            pts = set(points_from_key(s6))
            removed = int(item["removed_point"])
            if removed not in pts:
                raise ValueError(f"removed point absent from s6 key at line {line}")
            predecessor = d4_canonical_key(sorted(pts - {removed}))
            if predecessor != parent:
                raise ValueError(f"illegal parent incidence at line {line}: {parent} != {predecessor}")
            legal = legal_after(pts)
            if len(legal) != int(row[3]):
                raise ValueError(f"s6 legal-count mismatch at line {line}")
            checked_lines.add(line)
            source_loss_rows.add(s6)
            parent_witnesses.setdefault(parent, set()).add(s6)

    if set(parent_witnesses) != set(delta):
        raise ValueError("reverse audit parents and derived s5 cache keys differ")
    if any(delta[parent] != 2 for parent in parent_witnesses):
        raise ValueError("derived cache contains a non-LOSS verdict")
    if len(delta) != report.get("new_s5_loss"):
        raise ValueError("derived s5 LOSS count differs from reverse audit")
    if len(source_loss_rows) != report.get("source_s6_loss"):
        raise ValueError("distinct s6 LOSS witness count differs from reverse audit")

    baseline = read_cache(args.baseline_cache)
    local = read_cache(args.local_cache)
    merged = read_cache(args.merged_cache)
    if len(baseline) != report.get("baseline_exact_s5"):
        raise ValueError("baseline cache row count differs from reverse audit")
    if any(local.get(key) != value for key, value in baseline.items()):
        raise ValueError("current local cache does not preserve the complete audited baseline")
    overlap = set(local) & set(delta)
    conflicts = sorted(key for key in overlap if local[key] != delta[key])
    if conflicts:
        raise ValueError(f"exact cache conflict: {conflicts[:3]}")
    expected = dict(local)
    expected.update(delta)
    if merged != expected:
        differing = sorted(key for key in set(merged) | set(expected) if merged.get(key) != expected.get(key))
        raise ValueError(
            "merged current cache is not exactly local cache union reverse-derived delta: "
            f"differences={len(differing)}, sample={[(key, expected.get(key), merged.get(key)) for key in differing[:5]]}"
        )

    verdicts = Counter(merged.values())
    out = {
        "schema": "n11-post9dcb-s6-reverse-integration-audit-v1",
        "main_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip(),
        "reverse_audit": {"path": relative(args.reverse_audit), "sha256": sha(args.reverse_audit)},
        "s6_raw": {"path": relative(args.s6_raw), "sha256": sha(args.s6_raw), "git_blob_sha": git_blob(args.s6_raw)},
        "baseline_cache": {"path": relative(args.baseline_cache), "sha256": sha(args.baseline_cache), "entries": len(baseline)},
        "local_cache": {"path": relative(args.local_cache), "sha256": sha(args.local_cache), "entries": len(local)},
        "derived_delta": {"path": relative(args.delta_cache), "sha256": sha(args.delta_cache), "git_blob_sha": git_blob(args.delta_cache), "loss": len(delta)},
        "merged_cache": {"path": relative(args.merged_cache), "sha256": sha(args.merged_cache), "entries": len(merged), "win": verdicts[1], "loss": verdicts[2], "conflict": 0},
        "reverse_geometry": {"exact_s6_loss_rows": len(checked_lines), "distinct_s6_loss_keys": len(source_loss_rows), "derived_s5_loss_parents": len(parent_witnesses), "verified_legal_canonical_parent_incidences": sum(map(len, parent_witnesses.values()))},
        "cache_union": {"exact_overlap": len(overlap), "new_exact_rows": len(delta) - len(overlap), "conflicts": 0},
        "saved_s6_source_union": {"previous_files": len(previous_sources), "combined_files": len(combined_verified_sources), "previous_unique_keys": len(old_observations), "combined_unique_keys": len(combined_observations), "combined_s6_verdict_counts": combined_s6["verdict_counts_by_unique_key"], "conflicts": 0, "audit_path": relative(args.combined_saved_s6_audit_out), "audit_sha256": sha(args.combined_saved_s6_audit_out)},
        "verdict_source_limit": "Original s6 LOSS rows are saved exact solver results; this audit verifies source binding and legal geometry, not independent solver certificates.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite audit: {args.out}")
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k not in ("reverse_audit", "s6_raw", "baseline_cache", "local_cache", "derived_delta", "merged_cache")}, sort_keys=True))
    print("POST9DCB_S6_REVERSE_INTEGRATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

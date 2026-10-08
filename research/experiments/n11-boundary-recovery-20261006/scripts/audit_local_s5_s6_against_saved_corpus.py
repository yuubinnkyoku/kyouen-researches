#!/usr/bin/env python3
"""Reconcile preserved local reply27 s5/s6 replay rows with tracked exact evidence."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import legal_after  # noqa: E402
sys.path.insert(0, str(EXP / "scripts"))
from audit_saved_s6_targets import (  # noqa: E402
    points,
    read_saved_exact_s6,
    safe_canonical,
    sha256,
)


def relpath(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def read_s5_cache(path: Path) -> dict[tuple[int, int], int]:
    verdicts: dict[tuple[int, int], int] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split(",")
        if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
            raise ValueError(f"invalid exact s5 cache row {path}:{line_no}: {line}")
        key = (int(fields[1]), int(fields[2]))
        verdict = int(fields[4])
        if verdict not in (1, 2) or not safe_canonical(key, 5):
            raise ValueError(f"invalid/noncanonical exact s5 cache row {path}:{line_no}: {line}")
        if key in verdicts and verdicts[key] != verdict:
            raise ValueError(f"exact s5 cache conflict for {key}")
        verdicts[key] = verdict
    return verdicts


def read_local_replays(local_root: Path):
    observation_map: dict[int, dict[tuple[int, int], list[dict]]] = {
        5: defaultdict(list), 6: defaultdict(list)
    }
    file_reports = []
    csv_count = 0
    for path in sorted(local_root.rglob("*.csv")):
        csv_count += 1
        per_file: Counter[tuple[int, int]] = Counter()
        per_file_verdicts: Counter[str] = Counter()
        for row_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
            if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                continue
            if len(row) < 3 or not row[2].isdigit() or int(row[2]) not in (5, 6):
                continue
            stones = int(row[2])
            if len(row) != 11:
                raise ValueError(f"unexpected replay row width at {path}:{row_no}: {row}")
            legal, is_or, budget, verdict, nodes = map(int, (row[3], row[4], row[5], row[6], row[7]))
            key = (int(row[9]), int(row[10]))
            if (is_or != (1 if stones % 2 == 0 else 0) or budget <= 0 or verdict not in (0, 1, 2)
                    or nodes < 0 or not safe_canonical(key, stones)):
                raise ValueError(f"invalid/noncanonical local s{stones} replay at {path}:{row_no}: {row}")
            if len(legal_after(set(points(key)))) != legal:
                raise ValueError(f"local s{stones} legal-count mismatch at {path}:{row_no}: {row}")
            record = {
                "path": relpath(path),
                "row": row_no,
                "budget": budget,
                "verdict": verdict,
                "nodes": nodes,
                "legal": legal,
            }
            observation_map[stones][key].append(record)
            per_file[stones, verdict] += 1
            per_file_verdicts[f"s{stones}:verdict{verdict}"] += 1
        replay_rows = sum(per_file.values())
        if replay_rows:
            file_reports.append({
                "path": relpath(path),
                "sha256": sha256(path),
                "replay_rows": replay_rows,
                "counts_by_stones_and_verdict": dict(sorted(per_file_verdicts.items())),
            })
    return csv_count, observation_map, file_reports


def summarize_observations(by_key: dict[tuple[int, int], list[dict]]) -> dict:
    rows = [record for values in by_key.values() for record in values]
    row_counts = Counter(str(r["verdict"]) for r in rows)
    exact_keys = {}
    unknown_keys = set()
    conflicts = []
    for key, observations in by_key.items():
        exact_values = {r["verdict"] for r in observations if r["verdict"] in (1, 2)}
        if len(exact_values) > 1:
            conflicts.append({"key": list(key), "verdicts": sorted(exact_values)})
        elif exact_values:
            exact_keys[key] = next(iter(exact_values))
        else:
            unknown_keys.add(key)
    return {
        "replay_rows": len(rows),
        "observation_verdict_counts": dict(sorted(row_counts.items())),
        "distinct_canonical_keys": len(by_key),
        "distinct_exact_keys": len(exact_keys),
        "distinct_unknown_only_keys": len(unknown_keys),
        "exact_conflicts": conflicts,
        "exact_keys": exact_keys,
        "unknown_keys": unknown_keys,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-root", type=Path, required=True)
    parser.add_argument("--s5-cache", type=Path, required=True)
    parser.add_argument("--saved-s6-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    local_root = args.local_root.resolve()
    if not local_root.is_dir():
        raise SystemExit(f"local evidence directory not found: {local_root}")
    source_audit = json.loads(args.saved_s6_audit.read_text(encoding="utf-8"))
    if not source_audit.get("s6", {}).get("all_s6_exact_rows_geometry_checked"):
        raise SystemExit("saved s6 source audit lacks geometry/legal attestation")
    saved_s6, validated_sources = read_saved_exact_s6(source_audit)
    if source_audit.get("s6", {}).get("exact_conflict_count") != 0:
        raise SystemExit("saved s6 corpus reports exact conflicts")
    current_s5 = read_s5_cache(args.s5_cache)

    csv_count, observations, local_files = read_local_replays(local_root)
    s5 = summarize_observations(observations[5])
    s6 = summarize_observations(observations[6])
    if s5["exact_conflicts"] or s6["exact_conflicts"]:
        raise SystemExit("local raw replay observations contain an exact verdict conflict")

    s5_missing_or_mismatched = [
        {"key": list(key), "local_verdict": verdict, "cache_verdict": current_s5.get(key)}
        for key, verdict in s5["exact_keys"].items()
        if current_s5.get(key) != verdict
    ]
    if s5_missing_or_mismatched:
        raise SystemExit(f"local exact s5 evidence is absent/mismatched in merged cache: {s5_missing_or_mismatched[:5]}")

    s6_missing_or_mismatched = [
        {"key": list(key), "local_verdict": verdict,
         "saved_verdict": saved_s6.get(key, {}).get("verdict")}
        for key, verdict in s6["exact_keys"].items()
        if saved_s6.get(key, {}).get("verdict") != verdict
    ]
    if s6_missing_or_mismatched:
        raise SystemExit(f"local exact s6 evidence is absent/mismatched in saved corpus: {s6_missing_or_mismatched[:5]}")

    unknown_crosschecks = []
    for key in sorted(s6["unknown_keys"]):
        saved = saved_s6.get(key, {}).get("verdict")
        if saved in (1, 2):
            unknown_crosschecks.append({"key": list(key), "local_observation": "UNKNOWN",
                                        "saved_exact_verdict": "WIN" if saved == 1 else "LOSS",
                                        "used_for_propagation": False})

    s6_exact_local_losses = sum(value == 2 for value in s6["exact_keys"].values())
    if s6_exact_local_losses:
        raise SystemExit("local exact s6 LOSS found; run full safe-canonical reverse-parent incidence audit before accepting")

    out = {
        "schema": "n11-reply27-local-s5-s6-evidence-reconciliation-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scope": "read-only reconciliation of preserved .local replay CSVs against the merged exact s5 cache and hash-validated saved s6 corpus",
        "inputs": {
            "local_root": relpath(local_root),
            "local_csv_files_scanned": csv_count,
            "local_replay_files": local_files,
            "merged_s5_cache": {"path": relpath(args.s5_cache), "sha256": sha256(args.s5_cache),
                                "exact_rows": len(current_s5),
                                "verdict_counts": dict(sorted(Counter(map(str, current_s5.values())).items()))},
            "saved_s6_source_audit": {"path": relpath(args.saved_s6_audit),
                                      "sha256": sha256(args.saved_s6_audit),
                                      "validated_source_count": len(validated_sources),
                                      "source_hashes_validated": True,
                                      "unique_canonical_keys": len(saved_s6),
                                      "geometry_attested": True,
                                      "exact_conflicts": 0},
        },
        "local_s5": {
            key: value for key, value in s5.items() if key not in {"exact_keys", "unknown_keys"}
        } | {
            "exact_keys_all_present_with_same_verdict_in_merged_cache": True,
            "missing_or_mismatched_exact_keys": 0,
            "exact_s5_verdicts_new_to_cache": 0,
        },
        "local_s6": {
            key: value for key, value in s6.items() if key not in {"exact_keys", "unknown_keys"}
        } | {
            "exact_keys_all_present_with_same_verdict_in_saved_corpus": True,
            "missing_or_mismatched_exact_keys": 0,
            "exact_s6_verdicts_new_to_saved_corpus": 0,
            "exact_loss_rows_for_reverse_propagation": 0,
            "unknown_key_crosschecks": unknown_crosschecks,
            "unknown_crosschecks_used_for_propagation": 0,
        },
        "conflicts": 0,
        "conclusion": "all preserved local exact s5 and s6 replay rows are already represented with the same exact verdict in tracked evidence; no cache merge or reverse-propagated LOSS is added by this reconciliation",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "local_csv_files_scanned": csv_count,
        "local_replay_files": len(local_files),
        "local_s5_rows": s5["replay_rows"],
        "local_s5_exact_keys": s5["distinct_exact_keys"],
        "local_s6_rows": s6["replay_rows"],
        "local_s6_exact_keys": s6["distinct_exact_keys"],
        "saved_s6_sources": len(validated_sources),
        "local_s6_unknown_crosschecks": unknown_crosschecks,
        "conflicts": 0,
        "out": relpath(args.out),
        "out_sha256": sha256(args.out),
    }, indent=2))


if __name__ == "__main__":
    main()

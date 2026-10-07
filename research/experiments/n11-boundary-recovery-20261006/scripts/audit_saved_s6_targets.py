#!/usr/bin/env python3
"""Check whether saved exact s6 children resolve each currently remaining s5 parent."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402

EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
OUT = EXP / "output"
SOURCE_AUDIT = OUT / "s6-reverse-hard9-audit.json"
PARENT_CSV = OUT / "next3-remaining.csv"
CURRENT_CACHE = OUT / "post-hard9-reverse-s5.cache"
CACHE_OUT = OUT / "next3-saved-s6-derived-s5.cache"
SUMMARY_OUT = OUT / "next3-saved-s6-summary.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relpath(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path.resolve())


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise ValueError(f"n=11 key out of range: {key}")
    return tuple([i for i in range(64) if lo >> i & 1] + [64 + i for i in range(57) if hi >> i & 1])


def safe_canonical(key: tuple[int, int], stones: int) -> bool:
    pts = points(key)
    return len(pts) == stones and not has_forbidden_quad(pts) and tuple(d4_canonical_key(pts)) == key


def read_saved_exact_s6(source_audit: dict) -> tuple[dict, list[dict]]:
    source_items = source_audit.get("sources")
    if not isinstance(source_items, list) or not source_items:
        raise SystemExit(f"expected nonempty provenance-audited source files, got {len(source_items or [])}")
    reports = []
    raw_results: dict[tuple[int, int], list[dict]] = defaultdict(list)
    row_total = 0
    for item in source_items:
        src_path_text = item.get("path", "").replace("\\", "/")
        path = (ROOT / src_path_text).resolve()
        if not path.is_file():
            raise SystemExit(f"audited source file missing: {src_path_text}")
        digest = sha256(path)
        if digest != item.get("sha256"):
            raise SystemExit(f"audited source SHA-256 mismatch: {src_path_text}")
        file_rows = 0
        normalized_rows = 0
        verdict_counts: Counter[str] = Counter()
        for row_num, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
            if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                continue
            if len(row) < 3 or not row[2].isdigit() or int(row[2]) != 6:
                continue
            if len(row) != 11 or int(row[4]) != 1:
                raise SystemExit(f"invalid saved s6 OR replay: {src_path_text}:{row_num} {row}")
            raw_key = (int(row[9]), int(row[10]))
            raw_points = points(raw_key)
            if len(raw_points) != 6 or has_forbidden_quad(raw_points):
                raise SystemExit(f"unsafe saved s6: {src_path_text}:{row_num} {raw_key}")
            canonical = tuple(d4_canonical_key(raw_points))
            normalized_rows += canonical != raw_key
            if not safe_canonical(canonical, 6):
                raise SystemExit(f"canonicalized saved s6 is unsafe: {canonical}")
            verdict = int(row[6])
            if verdict not in (0, 1, 2):
                raise SystemExit(f"invalid saved solver verdict: {src_path_text}:{row_num} {verdict}")
            nodes = int(row[7])
            if nodes < 0:
                raise SystemExit(f"negative nodes: {src_path_text}:{row_num} {nodes}")
            legal = int(row[3])
            raw_results[canonical].append({"verdict": verdict, "nodes": nodes, "legal": legal,
                                           "source": src_path_text, "row": row_num,
                                           "raw_key": list(raw_key), "normalized": raw_key != canonical})
            verdict_counts[str(verdict)] += 1
            file_rows += 1
            row_total += 1
        expected_rows = item.get("s6_replay_rows")
        if type(expected_rows) is not int or file_rows != expected_rows:
            raise SystemExit(f"audited s6 row count mismatch: {src_path_text} {file_rows} != {expected_rows}")
        reports.append({"path": src_path_text, "sha256": digest, "s6_replay_rows": file_rows,
                        "normalized_noncanonical_rows": normalized_rows,
                        "verdict_counts": dict(sorted(verdict_counts.items()))})

    exact: dict[tuple[int, int], dict] = {}
    conflicts = []
    for key, observations in raw_results.items():
        exact_values = {x["verdict"] for x in observations if x["verdict"] in (1, 2)}
        if exact_values == {1, 2}:
            conflicts.append({"key": list(key), "verdicts": sorted(exact_values), "observations": observations})
            continue
        verdict = next(iter(exact_values)) if exact_values else 0
        exact[key] = {"verdict": verdict, "observations": observations,
                      "legal_counts": sorted({int(x["legal"]) for x in observations})}
    if conflicts:
        raise SystemExit(f"exact s6 WIN/LOSS conflicts found: {len(conflicts)}; first={conflicts[0]}")

    # The previous geometry/legal audit is reused only after every raw source hash
    # and row count above matches. Outcome values remain solver-provided evidence.
    attested = source_audit.get("s6", {})
    computed_counts = Counter(str(v["verdict"]) for v in exact.values() if v["verdict"] in (1, 2))
    if (len(exact) != attested.get("unique_canonical_keys")
            or len([v for v in exact.values() if v["verdict"] == 2]) != attested.get("unique_loss_keys")
            or len([v for v in exact.values() if v["verdict"] == 1]) != attested.get("unique_win_keys")
            or dict(sorted(computed_counts.items())) != attested.get("verdict_counts_by_unique_key")):
        raise SystemExit("rehydrated replay verdicts disagree with hash-validated source audit counts")
    return exact, reports


def read_current_cache(path: Path) -> dict[tuple[int, int], set[int]]:
    statuses: dict[tuple[int, int], set[int]] = defaultdict(set)
    for line_num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split(",")
        if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
            raise SystemExit(f"invalid current s5 cache row {line_num}: {line}")
        key = (int(fields[1]), int(fields[2]))
        if not safe_canonical(key, 5):
            raise SystemExit(f"unsafe/noncanonical current s5 key: {key}")
        verdict = int(fields[4])
        if verdict not in (1, 2):
            raise SystemExit(f"invalid current s5 verdict: {line}")
        statuses[key].add(verdict)
    conflicts = [k for k, v in statuses.items() if len(v) > 1]
    if conflicts:
        raise SystemExit(f"current cache has internal conflicts: {conflicts[:5]}")
    return statuses


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=Path, default=PARENT_CSV)
    parser.add_argument("--saved-audit", type=Path, default=SOURCE_AUDIT)
    parser.add_argument("--current-cache", type=Path, default=CURRENT_CACHE)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--cache-out", type=Path, default=CACHE_OUT)
    parser.add_argument("--compact-json", action="store_true",
                        help="write the full audit JSON without indentation to reduce storage")
    parser.add_argument("--full-detail-gzip", type=Path,
                        help="also preserve the full parent-child audit as a deterministic gzip JSON artifact")
    args = parser.parse_args()

    source_audit = json.loads(args.saved_audit.read_text(encoding="utf-8"))
    if not source_audit.get("s6", {}).get("all_s6_exact_rows_geometry_checked"):
        raise SystemExit("source audit does not attest prior s6 geometry/legal verification")
    exact, source_reports = read_saved_exact_s6(source_audit)
    parent_rows = list(csv.reader(args.targets.open(newline="", encoding="utf-8-sig")))
    parents: list[tuple[int, int]] = []
    for row_num, row in enumerate(parent_rows, 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 11 or int(row[2]) != 5 or int(row[6]) != 0 or int(row[7]) != 0:
            raise SystemExit(f"expected s5 AND parent target at {args.targets}:{row_num}: {row}")
        key = (int(row[3]), int(row[4]))
        if not safe_canonical(key, 5):
            raise SystemExit(f"unsafe/noncanonical s5 parent: {key}")
        if key in parents:
            raise SystemExit(f"duplicate parent target: {key}")
        pset = set(points(key))
        if int(row[5]) != len(legal_after(pset)):
            raise SystemExit(f"s5 target legal count mismatch for {key}")
        parents.append(key)

    cache_statuses = read_current_cache(args.current_cache)
    parent_results = []
    derived = []
    cache_conflicts = []
    for parent in parents:
        parent_points = set(points(parent))
        if len(parent_points) != 5 or has_forbidden_quad(parent_points):
            raise SystemExit(f"invalid s5 AND parent: {parent}")
        child_keys = set()
        for move in legal_after(parent_points):
            child_points = tuple(sorted((*parent_points, move)))
            if len(child_points) != 6 or has_forbidden_quad(child_points):
                raise SystemExit(f"unsafe legal s6 extension for {parent}: {move}")
            child = tuple(d4_canonical_key(child_points))
            if not safe_canonical(child, 6):
                raise SystemExit(f"unsafe canonical s6 child: {child}")
            # Direct reverse check assures the canonical parent incidence too.
            predecessors = {tuple(d4_canonical_key([p for p in child_points if p != removed]))
                            for removed in child_points}
            if parent not in predecessors:
                raise SystemExit(f"s6 child fails reverse-incidence check: {parent} -> {child}")
            child_keys.add(child)

        counts: Counter[str] = Counter()
        child_entries = []
        for child in sorted(child_keys):
            observed = exact.get(child)
            verdict = observed["verdict"] if observed is not None else None
            label = {1: "WIN", 2: "LOSS", 0: "UNKNOWN", None: "UNSEEN"}[verdict]
            counts[label] += 1
            child_entries.append({"key": list(child), "saved_verdict": verdict, "status": label,
                                  "source_rows": len(observed["observations"]) if observed else 0,
                                  "legal_count": observed["legal_counts"] if observed else None})

        if counts["LOSS"]:
            outcome = "LOSS"
        elif counts["WIN"] == len(child_keys):
            outcome = "WIN"
        else:
            outcome = "UNKNOWN"
        loss_witnesses = [list(k) for k in sorted(child_keys)
                          if exact.get(k, {}).get("verdict") == 2]
        existing = cache_statuses.get(parent, set())
        code = {"WIN": 1, "LOSS": 2}.get(outcome)
        if code is not None and existing and existing != {code}:
            cache_conflicts.append({"parent": list(parent), "derived": outcome, "existing": sorted(existing)})
        elif code is not None and not existing:
            derived.append((parent, code))
        parent_results.append({"key": list(parent), "outcome": outcome, "child_count": len(child_keys),
                               "counts": dict(sorted(counts.items())), "full_child_coverage": counts["WIN"] + counts["LOSS"] == len(child_keys),
                               "loss_witness_keys": loss_witnesses, "children": child_entries,
                               "current_cache_verdicts": sorted(existing)})

    if cache_conflicts:
        raise SystemExit(f"derived s5 results conflict with current cache: {cache_conflicts[:5]}")
    args.cache_out.parent.mkdir(parents=True, exist_ok=True)
    with args.cache_out.open("w", encoding="utf-8", newline="") as stream:
        stream.write("# s5 verdict cache: n=11 schema=1 (new exact results from saved s6 boundary coverage)\n")
        for (lo, hi), code in sorted(derived):
            stream.write(f"s5verdict,{lo},{hi},5,{code},0\n")

    parent_outcomes = Counter(row["outcome"] for row in parent_results)
    summary = {
        "schema": "n11-next3-saved-s6-parent-boundary-audit-v1",
        "outcome_provenance": "Saved s6 WIN/LOSS verdicts are trusted solver results; this audit independently regenerates each target s5 parent’s complete geometry boundary and propagates those saved verdicts only.",
        "source_audit": {"path": relpath(args.saved_audit), "sha256": sha256(args.saved_audit),
                         "source_hashes_validated": True, "source_file_count": len(source_reports),
                         "sources": source_reports, "canonical_s6_count": len(exact),
                         "s6_exact_counts": dict(sorted(Counter(str(v["verdict"]) for v in exact.values()).items())),
                         "unknown_s6_count": sum(v["verdict"] == 0 for v in exact.values()),
                         "exact_conflict_count": 0, "previous_geometry_legal_audit_reused_after_hash_match": True},
        "targets": {"path": relpath(args.targets), "sha256": sha256(args.targets), "parent_count": len(parents),
                    "status_counts": dict(sorted(parent_outcomes.items())), "parents": parent_results},
        "current_cache": {"path": relpath(args.current_cache), "sha256": sha256(args.current_cache),
                          "unique_keys": len(cache_statuses), "conflicts": 0},
        "cache_comparison": {"new_exact": len(derived), "same_verdict_existing": sum(
            1 for row in parent_results if row["outcome"] in ("WIN", "LOSS") and row["current_cache_verdicts"]),
                             "opposite_verdict_conflicts": cache_conflicts, "unknown_parents": parent_outcomes["UNKNOWN"]},
        "derived_cache": {"path": relpath(args.cache_out), "sha256": sha256(args.cache_out), "rows": len(derived)},
    }
    if args.full_detail_gzip:
        if not str(args.full_detail_gzip).lower().endswith(".json.gz"):
            raise SystemExit("--full-detail-gzip output must end in .json.gz")
        full_payload = (json.dumps(summary, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
        compressed = gzip.compress(full_payload, mtime=0)
        args.full_detail_gzip.parent.mkdir(parents=True, exist_ok=True)
        args.full_detail_gzip.write_bytes(compressed)
        summary["full_detail"] = {
            "path": relpath(args.full_detail_gzip),
            "sha256": sha256(args.full_detail_gzip),
            "bytes": args.full_detail_gzip.stat().st_size,
            "content": "full audit JSON with every canonical s6 boundary child",
        }
        summary["targets"] = dict(summary["targets"])
        summary["targets"]["parents"] = [
            {key: value for key, value in parent.items() if key != "children"}
            for parent in summary["targets"]["parents"]
        ]
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    with args.summary_out.open("w", encoding="utf-8", newline="\n") as stream:
        if args.compact_json or args.full_detail_gzip:
            stream.write(json.dumps(summary, separators=(",", ":"), sort_keys=True) + "\n")
        else:
            stream.write(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"parents": len(parents), "outcomes": dict(sorted(parent_outcomes.items())),
                      "new_exact": len(derived), "cache_conflicts": len(cache_conflicts)}, sort_keys=True))


if __name__ == "__main__":
    main()

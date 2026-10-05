#!/usr/bin/env python3
"""Derive every canonical s5 parent of saved exact s6 LOSS replays.

This script trusts saved solver verdicts and independently rechecks only their
geometry, canonicalization, source consistency, and one-ply parent relations.
"""
from __future__ import annotations

import argparse
import csv
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
SOURCES = [
    (OUT / "raw/shared-s6-0.csv", "n11 shared-s6 Actions run 37336924568 shard 0"),
    (OUT / "raw/shared-s6-1.csv", "n11 shared-s6 Actions run 37336924568 shard 1"),
    (OUT / "raw/shared-s6-2.csv", "n11 shared-s6 Actions run 37336924568 shard 2"),
    (OUT / "raw/shared-s6-3.csv", "n11 shared-s6 Actions run 37336924568 shard 3"),
    (OUT / "raw/model-hard2-reply27-model-hard2-s6-0-out.csv", "n11 model-hard2 Actions run 37339663025 shard 0"),
    (OUT / "raw/model-hard2-reply27-model-hard2-s6-1-out.csv", "n11 model-hard2 Actions run 37339663025 shard 1"),
    (OUT / "raw/model-hard2-reply27-model-hard2-s6-2-out.csv", "n11 model-hard2 Actions run 37339663025 shard 2"),
    (OUT / "raw/model-hard2-reply27-model-hard2-s6-3-out.csv", "n11 model-hard2 Actions run 37339663025 shard 3"),
    (OUT / "crosscheck-s6-out.csv", "n11 saved exact replay from incomplete cold residual cross-check; include solved rows only, not a complete run"),
]
CURRENT_CACHE = OUT / "post-next2-s5.cache"
PARENT_FILTER = {60, 27, 57, 63, 93}


def board_points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise ValueError(f"key outside n=11 board: {key}")
    return tuple([i for i in range(64) if lo >> i & 1] + [64 + i for i in range(57) if hi >> i & 1])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def display_path(path: Path) -> str:
    path = path.resolve()
    try:
        return str(path.relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def checked_canonical(key: tuple[int, int], stones: int) -> tuple[int, int]:
    pts = board_points(key)
    if len(pts) != stones or has_forbidden_quad(pts):
        raise ValueError(f"unsafe s{stones} key: {key}")
    return tuple(d4_canonical_key(pts))


def load_current_cache(path: Path) -> tuple[dict[tuple[int, int], set[int]], dict]:
    statuses: dict[tuple[int, int], set[int]] = defaultdict(set)
    rows = 0
    for line_num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split(",")
        if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
            raise SystemExit(f"unexpected row in current s5 cache at {line_num}: {line}")
        key = (int(fields[1]), int(fields[2]))
        if checked_canonical(key, 5) != key:
            raise SystemExit(f"noncanonical current s5 cache key: {key}")
        verdict = int(fields[4])
        if verdict not in (1, 2):
            raise SystemExit(f"invalid current cache verdict: {line}")
        statuses[key].add(verdict)
        rows += 1
    return statuses, {"path": display_path(path), "sha256": sha256(path), "rows": rows,
                      "unique_keys": len(statuses),
                      "conflicting_keys": [{"key": list(k), "verdicts": sorted(v)}
                                           for k, v in sorted(statuses.items()) if len(v) > 1]}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--current-cache", type=Path, default=CURRENT_CACHE)
    ap.add_argument("--extra-replay", action="append", nargs=2, metavar=("PATH", "PROVENANCE"), default=[],
                    help="add a saved replay CSV and its provenance; repeat the pair for more sources")
    ap.add_argument("--out", "--cache-out", dest="cache_out", type=Path, default=OUT / "s6-reverse-loss-s5.cache")
    ap.add_argument("--audit-out", type=Path, default=OUT / "s6-reverse-audit.json")
    args = ap.parse_args()

    sources = list(SOURCES)
    extra_source_paths = []
    for path_text, provenance in args.extra_replay:
        path = Path(path_text)
        if not path.is_absolute():
            path = ROOT / path
        if not path.is_file():
            raise SystemExit(f"extra replay source does not exist: {path}")
        sources.append((path, provenance))
        extra_source_paths.append(display_path(path))

    exact_rows: dict[tuple[int, int], list[dict]] = defaultdict(list)
    source_reports = []
    for path, provenance in sources:
        if not path.is_file():
            source_reports.append({"path": display_path(path), "provenance": provenance, "status": "missing; excluded"})
            continue
        row_count = 0
        s6_rows = 0
        verdict_counts: Counter[str] = Counter()
        node_total = 0
        normalized_rows = 0
        for row_num, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
            if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                continue
            if len(row) < 3 or not row[2].isdigit() or int(row[2]) != 6:
                continue
            row_count += 1
            if len(row) != 11 or int(row[4]) != 1:
                raise SystemExit(f"not an s6 OR replay row at {path}:{row_num}: {row}")
            raw_key = (int(row[9]), int(row[10]))
            canonical = checked_canonical(raw_key, 6)
            normalized_rows += canonical != raw_key
            pts = board_points(canonical)
            legal = int(row[3])
            geometry_legal = len(legal_after(set(pts)))
            if legal != geometry_legal:
                raise SystemExit(f"legal count mismatch at {path}:{row_num}, {canonical}: {legal} != {geometry_legal}")
            verdict = int(row[6])
            if verdict not in (0, 1, 2):
                raise SystemExit(f"invalid verdict at {path}:{row_num}: {verdict}")
            nodes = int(row[7])
            if nodes < 0:
                raise SystemExit(f"negative nodes at {path}:{row_num}: {nodes}")
            node_total += nodes
            verdict_counts[str(verdict)] += 1
            exact_rows[canonical].append({"verdict": verdict, "legal": legal, "nodes": nodes,
                                          "source": display_path(path), "row": row_num,
                                          "raw_key": list(raw_key), "normalized": raw_key != canonical})
            s6_rows += 1
        source_reports.append({"path": display_path(path), "provenance": provenance, "status": "included",
                               "source_kind": "caller_supplied_extra" if display_path(path) in extra_source_paths else "curated_saved_n11_source",
                               "sha256": sha256(path), "bytes": path.stat().st_size, "s6_replay_rows": s6_rows,
                               "verdict_counts": dict(sorted(verdict_counts.items())), "node_total": node_total,
                               "normalized_noncanonical_rows": normalized_rows})

    conflicts = []
    duplicate_same_verdict = []
    exact_loss: set[tuple[int, int]] = set()
    exact_win: set[tuple[int, int]] = set()
    unknown_only_keys = set()
    keys_with_unknown_rows = set()
    for key, observations in sorted(exact_rows.items()):
        exact_verdicts = {item["verdict"] for item in observations if item["verdict"] in (1, 2)}
        unknown_observations = [item for item in observations if item["verdict"] == 0]
        if unknown_observations:
            keys_with_unknown_rows.add(key)
        if not exact_verdicts:
            unknown_only_keys.add(key)
        if exact_verdicts == {1, 2}:
            conflicts.append({"kind": "saved_exact_verdict_conflict", "key": list(key),
                              "exact_verdicts": sorted(exact_verdicts), "unknown_rows": len(unknown_observations),
                              "sources": observations})
        else:
            if len([item for item in observations if item["verdict"] in (1, 2)]) > 1:
                duplicate_same_verdict.append({"key": list(key), "verdict": next(iter(exact_verdicts)),
                                               "unknown_rows": len(unknown_observations),
                                               "rows": [item for item in observations if item["verdict"] in (1, 2)]})
            if exact_verdicts == {2}:
                exact_loss.add(key)
            elif exact_verdicts == {1}:
                exact_win.add(key)

    # Every safe canonical one-point deletion parent is an odd s5 AND position.
    all_parent_sources: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for child in sorted(exact_loss):
        child_points = board_points(child)
        for removed in child_points:
            parent_points = tuple(p for p in child_points if p != removed)
            parent = tuple(d4_canonical_key(parent_points))
            if checked_canonical(parent, 5) != parent:
                raise SystemExit(f"invalid canonical parent generated from {child}")
            if removed not in legal_after(set(parent_points)):
                raise SystemExit(f"deleted point is not a legal extension: {parent} + {removed}")
            if tuple(d4_canonical_key((*parent_points, removed))) != child:
                raise SystemExit(f"canonical extension relation mismatch: {parent} -> {child}")
            if child not in all_parent_sources[parent]:
                all_parent_sources[parent].append(child)

    cache_statuses, cache_info = load_current_cache(args.current_cache)
    cache_conflicts = [
        {"kind": "current_cache_internal_conflict", **item}
        for item in cache_info["conflicting_keys"]
    ]
    candidates = []
    filter_excluded = []
    for parent, witnesses in sorted(all_parent_sources.items()):
        pset = set(board_points(parent))
        if 60 not in pset or not (pset & (PARENT_FILTER - {60})):
            filter_excluded.append({"key": list(parent), "witness_keys": [list(k) for k in sorted(witnesses)]})
            continue
        old = cache_statuses.get(parent, set())
        state = "new" if not old else ("duplicate_loss" if old == {2} else ("conflict" if len(old) > 1 else "opposite_verdict"))
        candidates.append({"key": list(parent), "witness_keys": [list(k) for k in sorted(witnesses)],
                           "existing_verdicts": sorted(old), "comparison": state})
        if state in ("conflict", "opposite_verdict"):
            cache_conflicts.append({"kind": "derived_loss_opposes_current_cache", "key": list(parent),
                                    "derived_verdict": 2, "existing_verdicts": sorted(old),
                                    "witness_keys": [list(k) for k in sorted(witnesses)]})

    additions = [tuple(item["key"]) for item in candidates if item["comparison"] == "new"]
    all_conflicts = conflicts + cache_conflicts
    rejected = bool(all_conflicts)
    if not rejected:
        args.cache_out.parent.mkdir(parents=True, exist_ok=True)
        with args.cache_out.open("w", encoding="utf-8", newline="") as stream:
            stream.write("# s5 verdict cache: n=11 schema=1 (new LOSS parents from all saved exact s6 LOSS replays)\n")
            for lo, hi in sorted(additions):
                stream.write(f"s5verdict,{lo},{hi},5,2,0\n")

    audit = {
        "schema": "n11-s6-reverse-loss-parents-v1",
        "outcome_provenance": "Saved exact solver verdicts are trusted as recorded; this script does not independently re-prove their game outcomes.",
        "source_scope": {"curated_files": "the fixed nine n11 saved replay CSVs listed in sources", "caller_supplied_extra_files": extra_source_paths,
                         "repository_wide_scan_claim": False},
        "sources": source_reports,
        "run_status": "rejected_conflicts" if rejected else "ok",
        "s6": {"unique_canonical_keys": len(exact_rows), "unique_loss_keys": len(exact_loss), "unique_win_keys": len(exact_win),
               "verdict_counts_by_unique_key": {"1": len(exact_win), "2": len(exact_loss)},
               "unknown_only_unique_keys": len(unknown_only_keys), "keys_with_unknown_rows": len(keys_with_unknown_rows),
               "conflicting_keys": conflicts, "same-exact-verdict-duplicate-keys": duplicate_same_verdict,
               "all_s6_exact_rows_geometry_checked": True, "unknowns_propagated": False,
               "conflicting_keys_propagated": False},
        "reverse_parents": {"all_canonical_safe_parent_count": len(all_parent_sources),
                            "all_canonical_safe_parent_witnesses": [
                                {"key": list(k), "loss_witness_keys": [list(x) for x in sorted(v)]}
                                for k, v in sorted(all_parent_sources.items())],
                            "d4_orbit_of_27": [27, 57, 63, 93],
                            "reply27_relevant_parent_count": len(candidates), "reply27_relevant_parents": candidates,
                            "filtered_non_reply27_parent_count": len(filter_excluded)},
        "current_cache": cache_info,
        "cache_comparison": {"new": sum(x["comparison"] == "new" for x in candidates),
                             "duplicate_loss": sum(x["comparison"] == "duplicate_loss" for x in candidates),
                             "opposite_verdict": sum(x["comparison"] == "opposite_verdict" for x in candidates),
                             "internal_conflict": sum(x["comparison"] == "conflict" for x in candidates),
                             "current_cache_internal_conflicts": len(cache_info["conflicting_keys"]),
                             "conflicts": all_conflicts, "opposite_or_conflict_not_adopted": True},
        "cache_out": {"path": display_path(args.cache_out), "sha256": sha256(args.cache_out) if args.cache_out.is_file() else None,
                      "rows": len(additions), "written": not rejected},
    }
    args.audit_out.parent.mkdir(parents=True, exist_ok=True)
    args.audit_out.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if rejected:
        raise SystemExit(f"refusing to write cache: {len(all_conflicts)} exact/current-cache conflict(s); see {args.audit_out}")
    print(json.dumps({"sources": len([s for s in source_reports if s["status"] == "included"]),
                      "s6_unique": len(exact_rows), "s6_loss_unique": len(exact_loss),
                      "all_parents": len(all_parent_sources), "reply27_relevant": len(candidates),
                      "cache_comparison": audit["cache_comparison"], "new_rows": len(additions)}, sort_keys=True))


if __name__ == "__main__":
    main()

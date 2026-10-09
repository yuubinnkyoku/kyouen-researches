#!/usr/bin/env python3
"""Reverse every hash-validated saved exact S6 LOSS in the current cache."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
UNION = OUT / "post-11452254-next-rank1-1585267068834414720-0-saved-s6-source-union-v3.json"
BASE = OUT / "post-9681c588-next98-round4-merged-s5.cache"
DELTA = OUT / "post-11452254-saved-s6-union-v3-reverse-loss-s5-delta.cache"
AUDIT = OUT / "post-11452254-saved-s6-union-v3-reverse-loss-audit.json"
SCRIPT = Path(__file__).resolve()
EDGE = ROOT / "research/experiments/n11-search-methods/scripts"

import sys
sys.path.insert(0, str(EDGE))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402

for path in (DELTA, AUDIT):
    if path.exists():
        raise SystemExit(f"refusing to overwrite existing artifact: {path}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise ValueError(f"n=11 key out of range: {key}")
    return tuple([i for i in range(64) if lo >> i & 1]
                 + [64 + i for i in range(57) if hi >> i & 1])


def canonical_safe(key: tuple[int, int], stones: int) -> tuple[int, int]:
    pts = points(key)
    if len(pts) != stones or has_forbidden_quad(pts):
        raise ValueError(f"unsafe s{stones} replay key: {key}")
    canonical = tuple(d4_canonical_key(pts))
    canonical_points = points(canonical)
    if len(canonical_points) != stones or has_forbidden_quad(canonical_points):
        raise ValueError(f"unsafe canonical s{stones} replay key: {canonical}")
    return canonical


def main() -> None:
    union_bytes = UNION.read_bytes()
    union = json.loads(union_bytes)
    if union.get("run_status") != "ok" or not union.get("source_hashes_validated"):
        raise SystemExit("saved S6 source union lacks successful hash and conflict validation")
    if not union.get("s6", {}).get("all_s6_exact_rows_geometry_checked"):
        raise SystemExit("saved S6 source union lacks full geometry/legal attestation")
    builder = union.get("union_provenance", {}).get("builder", {})
    builder_path = ROOT / builder.get("path", "")
    if not builder_path.is_file() or sha256(builder_path) != builder.get("sha256"):
        raise SystemExit("saved S6 union builder hash does not match its source manifest")

    observed: dict[tuple[int, int], list[dict]] = defaultdict(list)
    source_reports = []
    for item in union.get("sources", []):
        rel = item.get("path")
        path = ROOT / str(rel).replace("\\", "/")
        if not path.is_file() or sha256(path) != item.get("sha256"):
            raise SystemExit(f"saved S6 source missing or hash changed: {rel}")
        file_rows = 0
        normalized_rows = 0
        verdict_counts: Counter[str] = Counter()
        with path.open(newline="", encoding="utf-8-sig") as stream:
            for row_num, row in enumerate(csv.reader(stream), 1):
                if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                    continue
                if len(row) < 3 or not row[2].isdigit() or int(row[2]) != 6:
                    continue
                if len(row) != 11 or int(row[4]) != 1:
                    raise SystemExit(f"invalid s6 OR replay row {rel}:{row_num}: {row}")
                raw_key = (int(row[9]), int(row[10]))
                key = canonical_safe(raw_key, 6)
                verdict, legal, nodes = int(row[6]), int(row[3]), int(row[7])
                if verdict not in (0, 1, 2) or legal < 0 or nodes < 0:
                    raise SystemExit(f"invalid s6 replay fields {rel}:{row_num}: {row}")
                normalized_rows += raw_key != key
                file_rows += 1
                verdict_counts[str(verdict)] += 1
                observed[key].append({"verdict": verdict, "legal": legal, "nodes": nodes,
                                      "source": rel, "row": row_num})
        expected_normalized = item.get("normalized_noncanonical_rows")
        expected_verdicts = item.get("verdict_counts")
        if (file_rows != item.get("s6_replay_rows")
                or (expected_normalized is not None and normalized_rows != expected_normalized)
                or (expected_verdicts is not None
                    and dict(sorted(verdict_counts.items())) != expected_verdicts)):
            raise SystemExit(f"saved S6 source counts disagree with union manifest: {rel}")
        source_reports.append({"path": rel, "sha256": item["sha256"],
                               "s6_replay_rows": file_rows,
                               "normalized_noncanonical_rows": normalized_rows,
                               "verdict_counts": dict(sorted(verdict_counts.items()))})

    exact: dict[tuple[int, int], int] = {}
    conflicts = []
    for key, rows in observed.items():
        values = {x["verdict"] for x in rows if x["verdict"] in (1, 2)}
        if values == {1, 2}:
            conflicts.append({"key": list(key), "verdicts": sorted(values),
                              "sources": [{"path": x["source"], "row": x["row"],
                                           "verdict": x["verdict"]} for x in rows]})
        elif values:
            exact[key] = next(iter(values))
    if conflicts:
        raise SystemExit(f"saved exact S6 WIN/LOSS conflicts: {len(conflicts)}")

    attested = union["s6"]
    s6_counts = Counter(str(v) for v in exact.values())
    unknown_unique = sum(not any(x["verdict"] in (1, 2) for x in rows)
                         for rows in observed.values())
    if (len(observed) != attested.get("unique_canonical_keys")
            or s6_counts.get("1", 0) != attested.get("unique_win_keys")
            or s6_counts.get("2", 0) != attested.get("unique_loss_keys")
            or unknown_unique != attested.get("unknown_unique_keys")):
        raise SystemExit("rehydrated S6 verdict set disagrees with hash-validated union counts")

    # Recheck legal-extension counts specifically for every exact LOSS witness.
    loss_witness_geometry = []
    for key, verdict in sorted(exact.items()):
        if verdict != 2:
            continue
        pts = set(points(key))
        legal_counts = sorted({x["legal"] for x in observed[key]})
        geometry_legal = len(legal_after(pts))
        if legal_counts != [geometry_legal]:
            raise SystemExit(f"S6 LOSS legal-count geometry mismatch {key}: {legal_counts} != {geometry_legal}")
        loss_witness_geometry.append({"key": list(key), "legal_count": geometry_legal,
                                      "source_rows": len(observed[key])})

    all_parents: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for child, verdict in sorted(exact.items()):
        if verdict != 2:
            continue
        child_points = points(child)
        for removed in child_points:
            raw_parent_points = tuple(p for p in child_points if p != removed)
            if has_forbidden_quad(raw_parent_points):
                raise SystemExit(f"unsafe one-point parent from S6 LOSS {child}")
            if removed not in legal_after(set(raw_parent_points)):
                raise SystemExit(f"deleted point is not a legal extension: {raw_parent_points} + {removed}")
            parent = tuple(d4_canonical_key(raw_parent_points))
            if canonical_safe(parent, 5) != parent:
                raise SystemExit(f"generated S5 parent is not safe canonical: {parent}")
            if tuple(d4_canonical_key((*raw_parent_points, removed))) != child:
                raise SystemExit(f"canonical S6 witness is not a child of generated parent: {parent} -> {child}")
            all_parents[parent].add(child)

    cache_status: dict[tuple[int, int], set[int]] = defaultdict(set)
    cache_rows = 0
    for row_num, row in enumerate(csv.reader(BASE.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid current S5 cache row {row_num}: {row}")
        key, verdict = (int(row[1]), int(row[2])), int(row[4])
        if canonical_safe(key, 5) != key or verdict not in (1, 2):
            raise SystemExit(f"unsafe/noncanonical/nonexact current S5 cache row: {row}")
        cache_status[key].add(verdict)
        cache_rows += 1
    conflicts.extend({"kind": "current_cache_internal_conflict", "key": list(k),
                      "verdicts": sorted(v)} for k, v in cache_status.items() if len(v) > 1)

    orbit27 = {27, 57, 63, 93}
    reply27 = []
    for parent, witnesses in sorted(all_parents.items()):
        pset = set(points(parent))
        if 60 not in pset or not pset.intersection(orbit27):
            continue
        old = cache_status.get(parent, set())
        comparison = ("new" if not old else "duplicate_loss" if old == {2}
                      else "cache_conflict" if len(old) > 1 else "opposite_verdict")
        entry = {"key": list(parent), "loss_witness_keys": [list(k) for k in sorted(witnesses)],
                 "existing_verdicts": sorted(old), "comparison": comparison}
        reply27.append(entry)
        if comparison in ("cache_conflict", "opposite_verdict"):
            conflicts.append({"kind": "derived_S5_LOSS_opposes_current_cache", **entry})

    additions = [tuple(x["key"]) for x in reply27 if x["comparison"] == "new"]
    if conflicts:
        raise SystemExit(f"refusing to write reverse delta: {len(conflicts)} exact/cache conflicts")

    with DELTA.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# s5 verdict cache: n=11 schema=1 (new LOSS parents from audited saved exact S6 LOSS replays)\n")
        for lo, hi in sorted(additions):
            stream.write(f"s5verdict,{lo},{hi},5,2,0\n")
    audit = {
        "schema": "n11-s6-reverse-loss-parents-v1",
        "claim": "Every propagated S5 LOSS has at least one hash-validated exact S6 LOSS witness; all safe canonical one-point parents of every unique exact S6 LOSS were enumerated and geometry-checked.",
        "source_union": {"path": UNION.relative_to(ROOT).as_posix(),
                         "sha256": hashlib.sha256(union_bytes).hexdigest(),
                         "source_file_count": len(source_reports),
                         "s6_replay_rows": sum(x["s6_replay_rows"] for x in source_reports),
                         "source_hashes_revalidated": True,
                         "builder": builder},
        "saved_s6": {"unique_canonical_keys": len(observed),
                     "unique_exact_win": s6_counts.get("1", 0),
                     "unique_exact_loss": s6_counts.get("2", 0),
                     "unique_unknown_only": unknown_unique,
                     "exact_conflicts": conflicts[:0],
                     "all_exact_loss_witnesses_legal_count_rechecked": True,
                     "loss_witness_geometry": loss_witness_geometry,
                     "unknown_or_win_s6_propagated": False},
        "reverse_parents": {"all_safe_canonical_parent_count": len(all_parents),
                            "all_safe_canonical_parents": [
                                {"key": list(k), "loss_witness_keys": [list(x) for x in sorted(v)]}
                                for k, v in sorted(all_parents.items())],
                            "reply27_orbit_of_27": sorted(orbit27),
                            "reply27_parent_count": len(reply27),
                            "reply27_parents": reply27},
        "current_cache": {"path": BASE.relative_to(ROOT).as_posix(),
                          "sha256": sha256(BASE), "rows": cache_rows,
                          "unique_keys": len(cache_status),
                          "conflicts": sum(len(v) > 1 for v in cache_status.values())},
        "cache_comparison": {"new_loss": len(additions),
                             "duplicate_loss": sum(x["comparison"] == "duplicate_loss" for x in reply27),
                             "opposite_verdict": 0, "conflicts": 0},
        "delta_cache": {"path": DELTA.relative_to(ROOT).as_posix(),
                        "sha256": sha256(DELTA), "rows": len(additions)},
        "sources": source_reports,
        "audit_script": {"path": SCRIPT.relative_to(ROOT).as_posix(), "sha256": sha256(SCRIPT)},
    }
    AUDIT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"s6_unique": len(observed), "s6_loss": s6_counts.get("2", 0),
                      "all_safe_canonical_parents": len(all_parents),
                      "reply27_parents": len(reply27), "new_loss": len(additions),
                      "duplicate_loss": audit["cache_comparison"]["duplicate_loss"],
                      "conflicts": 0, "source_files": len(source_reports)}, sort_keys=True))


if __name__ == "__main__":
    main()

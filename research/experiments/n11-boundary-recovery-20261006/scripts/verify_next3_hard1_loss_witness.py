#!/usr/bin/env python3
"""Independently verify geometry incidence for a saved next3 hard s6 LOSS witness."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
DEFAULT_RAW = EXP / "output/raw/next3-hard1-hard-s6-15m-out.csv"
DEFAULT_PARENT = EXP / "output/next3-hard1-s5.csv"
DEFAULT_META = EXP / "output/next3-hard1-s6-meta.json"
DEFAULT_BOUNDARY = EXP / "output/next3-hard1-s6-boundary.csv"
DEFAULT_AUDIT = EXP / "output/next3-hard1-loss-witness-audit.json"
DEFAULT_CACHE = EXP / "output/next3-hard1-derived-s5.cache"

sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < (1 << 64) and 0 <= hi < (1 << 57)):
        raise ValueError(f"n=11 key out of range: {key}")
    return tuple([i for i in range(64) if lo >> i & 1] +
                 [64 + i for i in range(57) if hi >> i & 1])


def checked(key: tuple[int, int], stones: int) -> tuple[int, ...]:
    pts = points(key)
    if len(pts) != stones or has_forbidden_quad(pts):
        raise ValueError(f"unsafe or wrong-size s{stones} key: {key}")
    canonical = tuple(d4_canonical_key(pts))
    if canonical != key:
        raise ValueError(f"noncanonical (lo,hi) key {key}, expected {canonical}")
    return pts


def read_parent(path: Path) -> tuple[int, int]:
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
                raise ValueError(f"expected s5 AND target at {path}:{line_no}: {row}")
            key = (int(row[3]), int(row[4]))
            pts = checked(key, 5)
            if int(row[5]) != len(legal_after(set(pts))):
                raise ValueError(f"s5 parent legal count mismatch: {key}")
            rows.append(key)
    if rows != [(1297318167659941888, 0)]:
        raise ValueError(f"unexpected hard1 parent rows: {rows}")
    return rows[0]


def read_boundary(path: Path) -> dict[tuple[int, int], int]:
    children = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#") or row[0] == "tag":
                continue
            if len(row) != 11 or row[0] != "target" or int(row[2]) != 6 or int(row[6]) != 0 or int(row[7]) != 1:
                raise ValueError(f"invalid materialized s6 target at {path}:{line_no}: {row}")
            key = (int(row[3]), int(row[4]))
            checked(key, 6)
            if key in children:
                raise ValueError(f"duplicate materialized boundary key: {key}")
            children[key] = int(row[5])
    return children


def read_loss(path: Path) -> dict:
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if row[0] != "replay" or len(row) != 11:
                raise ValueError(f"unexpected raw solver row at {path}:{line_no}: {row}")
            stones, legal, is_or, budget = int(row[2]), int(row[3]), int(row[4]), int(row[5])
            verdict, nodes = int(row[6]), int(row[7])
            key = (int(row[9]), int(row[10]))
            checked(key, 6)
            if (stones, legal, is_or, budget, verdict) != (6, 81, 1, 15_000_000, 2) or nodes < 0:
                raise ValueError(f"raw replay fields do not match expected LOSS witness: {row}")
            rows.append({"seq": int(row[1]), "key": key, "stones": stones, "legal": legal,
                         "is_or": is_or, "budget": budget, "verdict": verdict, "nodes": nodes,
                         "wall_s": float(row[8])})
    if len(rows) != 1:
        raise ValueError(f"expected exactly one unique replay row, got {len(rows)}")
    return rows[0]


def atomic_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(payload, encoding="utf-8", newline="\n")
    os.replace(temp, path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    ap.add_argument("--parent", type=Path, default=DEFAULT_PARENT)
    ap.add_argument("--meta", type=Path, default=DEFAULT_META)
    ap.add_argument("--boundary", type=Path, default=DEFAULT_BOUNDARY)
    ap.add_argument("--audit-out", type=Path, default=DEFAULT_AUDIT)
    ap.add_argument("--cache-out", type=Path, default=DEFAULT_CACHE)
    args = ap.parse_args()

    parent = read_parent(args.parent)
    parent_points = set(checked(parent, 5))
    generated = {}
    for move in legal_after(parent_points):
        child_points = tuple(sorted((*parent_points, move)))
        if has_forbidden_quad(child_points):
            raise ValueError(f"geometry returned unsafe child for {parent} + {move}")
        child = tuple(d4_canonical_key(child_points))
        checked(child, 6)
        generated[child] = len(legal_after(set(checked(child, 6))))

    meta = json.loads(args.meta.read_text(encoding="utf-8"))
    metadata_children = meta.get("canonical_children", [])
    expected_meta = {tuple(item["key"]): int(item["legal_count"])
                     for item in metadata_children}
    materialized = read_boundary(args.boundary)
    if (meta.get("schema") != "n11-s6-complete-boundary-v1"
            or meta.get("parent_keys") != [list(parent)]
            or meta.get("complete_boundary_count") != 86):
        raise ValueError("boundary metadata parent/count mismatch")
    if meta.get("parent_child_relation_count") != 86:
        raise ValueError("boundary metadata relation count mismatch")
    if (len(metadata_children) != 86 or len(expected_meta) != 86
            or generated != expected_meta or generated != materialized or len(generated) != 86):
        raise ValueError("runtime geometry, metadata, and materialized 86-child boundary differ")
    if any(item.get("parent_indices") != [0] for item in meta["canonical_children"]):
        raise ValueError("metadata child-to-parent incidence is not the sole specified parent")
    expected_incidence = {f"{lo}:{hi}": [0] for lo, hi in generated}
    if meta.get("child_parent_indices") != expected_incidence:
        raise ValueError("metadata child_parent_indices map differs from regenerated incidence")

    replay = read_loss(args.raw)
    child = replay["key"]
    if child not in generated:
        raise ValueError(f"saved LOSS witness {child} is not a legal canonical child of {parent}")
    if replay["legal"] != generated[child]:
        raise ValueError(f"saved LOSS witness legal count mismatch: replay={replay['legal']} geometry={generated[child]}")
    child_points = points(child)
    reverse_parents = {tuple(d4_canonical_key([p for p in child_points if p != removed]))
                       for removed in child_points}
    if parent not in reverse_parents:
        raise ValueError(f"reverse one-point deletion does not recover parent {parent}")

    cache_text = ("# s5 verdict cache: n=11 schema=1 (one-parent canonical s6 LOSS witness)\n"
                  f"s5verdict,{parent[0]},{parent[1]},5,2,0\n")
    # Output only becomes visible after all geometry, artifact, and incidence checks pass.
    atomic_text(args.cache_out, cache_text)
    audit = {
        "schema": "n11-next3-hard1-loss-witness-independent-geometry-audit-v1",
        "claim_scope": "The s6 LOSS value is trusted as recorded in the saved solver replay. This verifier does not independently re-prove that game outcome; it independently checks replay structure, canonical/safe geometry, legal count, parent incidence, and the complete parent boundary.",
        "raw_source": {"path": str(args.raw.resolve()), "sha256": sha256(args.raw), "rows": 1,
                       "key_lo_hi": list(child), "stones": 6, "is_or": 1, "legal": 81,
                       "budget": replay["budget"], "verdict": "LOSS", "solver_result": 2,
                       "nodes": replay["nodes"], "wall_s": replay["wall_s"]},
        "parent": {"path": str(args.parent.resolve()), "sha256": sha256(args.parent),
                   "key_lo_hi": list(parent), "stones": 5, "is_or": 0,
                   "derived_verdict": "LOSS", "loss_witness_count": 1},
        "boundary": {"meta_path": str(args.meta.resolve()), "meta_sha256": sha256(args.meta),
                     "csv_path": str(args.boundary.resolve()), "csv_sha256": sha256(args.boundary),
                     "runtime_geometry_regenerated": True, "complete_canonical_safe_children": len(generated),
                     "materialized_children": len(materialized), "meta_children": len(expected_meta),
                     "geometry_meta_csv_exact_set_and_legal_counts_match": True,
                     "parent_child_relations": sum(len(item.get("parent_indices", []))
                                                   for item in meta["canonical_children"])},
        "witness_incidence": {"child_in_complete_boundary": True,
                              "parent_recovered_by_reverse_point_deletion": True,
                              "canonical_key_convention": meta.get("canonical_key_convention"),
                              "canonical_ordering": meta.get("canonical_ordering")},
        "derived_cache": {"path": str(args.cache_out.resolve()), "sha256": hashlib.sha256(cache_text.encode("utf-8")).hexdigest(),
                          "rows": 1, "verdict": "LOSS"},
    }
    atomic_text(args.audit_out, json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"parent": list(parent), "witness": list(child),
                      "complete_boundary": len(generated), "derived": "LOSS"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

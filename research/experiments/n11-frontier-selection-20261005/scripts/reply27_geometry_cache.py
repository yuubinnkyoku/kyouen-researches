#!/usr/bin/env python3
"""Optional, validated persistent geometry cache for the reply=27 s4 frontier.

Generate an index explicitly with ``python reply27_geometry_cache.py generate
--out PATH``. Consumers only load an index when passed ``--geometry-cache``;
their default remains the original cold geometry build.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))
from dfpn_edge_classes import d4_canonical_key, forbidden, legal_after  # noqa: E402

N = 11
V = N * N
FIRST, R2 = 60, 27
MAGIC = "reply27-s4-geometry-cache-v1"
MASK64 = (1 << 64) - 1


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for block in iter(lambda: fp.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def source_hashes() -> dict[str, str]:
    return {
        "reply27_geometry_cache.py": _sha256(Path(__file__).resolve()),
        "dfpn_edge_classes.py": _sha256(EDGE_DIR / "dfpn_edge_classes.py"),
    }


def _bits(points):
    lo = hi = 0
    for p in points:
        if not isinstance(p, int) or not 0 <= p < V:
            raise ValueError(f"point out of range: {p!r}")
        if p < 64:
            lo |= 1 << p
        else:
            hi |= 1 << (p - 64)
    return [lo, hi]


def _points(key, count):
    if (not isinstance(key, list) or len(key) != 2
            or any(type(x) is not int or x < 0 or x > MASK64 for x in key)):
        raise ValueError(f"invalid board key: {key!r}")
    lo, hi = key
    if hi >> (V - 64):
        raise ValueError(f"bits outside 11x11 board: {key!r}")
    pts = {p for p in range(64) if (lo >> p) & 1}
    pts.update(p + 64 for p in range(V - 64) if (hi >> p) & 1)
    if len(pts) != count or _bits(pts) != key:
        raise ValueError(f"expected {count}-stone key: {key!r}")
    return pts


def _canonical_key(key, count):
    pts = _points(key, count)
    if d4_canonical_key(sorted(pts)) != tuple(key):
        raise ValueError(f"noncanonical {count}-stone key: {key!r}")
    return pts


def build_geometry():
    """Build the complete geometry and check representative-edge invariance."""
    base = {FIRST, R2}
    verts = set(legal_after(base))
    raw = defaultdict(list)
    for a in sorted(verts):
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            raw[d4_canonical_key([FIRST, R2, a, b])].append((a, b))
    if (len(verts), sum(map(len, raw.values())), len(raw)) != (119, 6871, 3384):
        raise ValueError("cold geometry count mismatch")

    records = []
    for key, edges in sorted(raw.items()):
        coverage = sorted({p for edge in edges for p in edge})
        edge_children = []
        for a, b in edges:
            occ = base | {a, b}
            edge_children.append({
                d4_canonical_key(list(occ | {z})) for z in legal_after(occ)
            })
        representative = edge_children[0]
        if any(children != representative for children in edge_children[1:]):
            raise ValueError(f"representative child boundary differs within {key}")
        union = set().union(*edge_children) if edge_children else set()
        if union != representative:
            raise ValueError(f"raw-edge child union mismatch within {key}")
        records.append({
            "key": list(key),
            "edges": [list(e) for e in sorted(edges)],
            "coverage": coverage,
            "children": [list(k) for k in sorted(union)],
        })
    return {
        "root": [FIRST, R2],
        "verts": sorted(verts),
        "groups": records,
    }


def _canonical_json(data) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def write_cache(path: Path, data) -> None:
    payload = _canonical_json(data)
    doc = {
        "format": MAGIC,
        "n": N,
        "root": [FIRST, R2],
        "counts": {"vertices": 119, "edges": 6871, "classes": 3384},
        "source_sha256": source_hashes(),
        "data_sha256": hashlib.sha256(payload).hexdigest(),
        "data": data,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = _canonical_json(doc)
    with path.open("wb") as fp:
        fp.write(gzip.compress(encoded, compresslevel=9, mtime=0))


def _validate(data) -> None:
    if not isinstance(data, dict) or data.get("root") != [FIRST, R2]:
        raise ValueError("geometry data root mismatch")
    verts = data.get("verts")
    rows = data.get("groups")
    if not isinstance(verts, list) or len(verts) != 119 or len(set(verts)) != 119:
        raise ValueError("invalid vertex list")
    if any(type(p) is not int or not 0 <= p < V for p in verts):
        raise ValueError("invalid vertex value")
    expected_verts = set(legal_after({FIRST, R2}))
    if set(verts) != expected_verts:
        raise ValueError("vertex boundary differs from current generator")
    if not isinstance(rows, list) or len(rows) != 3384:
        raise ValueError("invalid class list")
    base = {FIRST, R2}
    seen_keys = set()
    all_edges = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"key", "edges", "coverage", "children"}:
            raise ValueError("malformed class record")
        key = row["key"]
        _canonical_key(key, 4)
        k = tuple(key)
        if k in seen_keys:
            raise ValueError(f"duplicate class key: {k}")
        seen_keys.add(k)
        edges = row["edges"]
        if not isinstance(edges, list) or not edges:
            raise ValueError(f"empty/malformed edge list: {k}")
        edge_set = set()
        for edge in edges:
            if (not isinstance(edge, list) or len(edge) != 2
                    or any(type(p) is not int or p not in expected_verts for p in edge)
                    or edge[0] >= edge[1]):
                raise ValueError(f"invalid edge: {edge!r}")
            e = tuple(edge)
            if e in edge_set or e in all_edges:
                raise ValueError(f"duplicate edge: {e}")
            if d4_canonical_key([FIRST, R2, *e]) != k:
                raise ValueError(f"edge/class mismatch: {e} -> {k}")
            if forbidden(FIRST, R2, *e):
                raise ValueError(f"unsafe edge: {e}")
            edge_set.add(e)
            all_edges.add(e)
        coverage = row["coverage"]
        expected_coverage = sorted({p for e in edge_set for p in e})
        if coverage != expected_coverage:
            raise ValueError(f"coverage mismatch: {k}")
        children = row["children"]
        if not isinstance(children, list) or not children:
            raise ValueError(f"empty/malformed child list: {k}")
        prev = None
        childset = set()
        for child in children:
            pts = _canonical_key(child, 5)
            ck = tuple(child)
            if prev is not None and ck <= prev:
                raise ValueError(f"unsorted or duplicate child list: {k}")
            prev = ck
            childset.add(ck)
            # Canonical key and exact stone count are checked above.  The data
            # digest plus generator/source hashes bind the actual boundaries;
            # recomputing every edge's legal children here would erase the
            # purpose of the cache (and repeat the multi-minute cold build).
        if not set(coverage).issubset(expected_verts):
            raise ValueError(f"coverage outside vertex set: {k}")
    if len(all_edges) != 6871:
        raise ValueError("raw edge count mismatch")


def load_cache(path: Path):
    try:
        with gzip.open(path, "rt", encoding="utf-8") as fp:
            doc = json.load(fp)
    except Exception as exc:
        raise ValueError(f"cannot read geometry cache {path}: {exc}") from exc
    if not isinstance(doc, dict) or doc.get("format") != MAGIC:
        raise ValueError("geometry cache format mismatch")
    if doc.get("n") != N or doc.get("root") != [FIRST, R2]:
        raise ValueError("geometry cache board/root mismatch")
    if doc.get("counts") != {"vertices": 119, "edges": 6871, "classes": 3384}:
        raise ValueError("geometry cache count manifest mismatch")
    if doc.get("source_sha256") != source_hashes():
        raise ValueError("geometry cache source SHA mismatch; regenerate explicitly")
    data = doc.get("data")
    if doc.get("data_sha256") != hashlib.sha256(_canonical_json(data)).hexdigest():
        raise ValueError("geometry cache data digest mismatch")
    _validate(data)
    return data


def as_cardinality(data):
    verts = set(data["verts"])
    coverage = {tuple(r["key"]): set(r["coverage"]) for r in data["groups"]}
    children = {tuple(r["key"]): {tuple(k) for k in r["children"]}
                for r in data["groups"]}
    return verts, coverage, children


def as_repair(data):
    verts = set(data["verts"])
    groups = {tuple(r["key"]): [tuple(e) for e in r["edges"]]
              for r in data["groups"]}
    coverage = {tuple(r["key"]): set(r["coverage"]) for r in data["groups"]}
    children = {tuple(r["key"]): {tuple(k) for k in r["children"]}
                for r in data["groups"]}
    return verts, groups, coverage, children


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate", help="cold-build and save a validated geometry index")
    gen.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if args.command == "generate":
        data = build_geometry()
        _validate(data)
        write_cache(args.out, data)
        print(f"REPLY27_GEOMETRY_CACHE_OK classes=3384 edges=6871 out={args.out}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

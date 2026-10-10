#!/usr/bin/env python3
"""Audit saved model-hard2 s6 replays against the independently materialized boundary."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import argparse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402

EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
ART = ROOT / ".local/n11/model-hard2-proof"
RAW = EXP / "output/raw"
PARENTS = [(1154082588886827008, 536870912), (1874623344894017536, 0)]


import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(_PolicyPath(__file__).resolve().parents[4] / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import quarantined_cache_keys

def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise ValueError(f"out of board key {key}")
    return tuple([i for i in range(64) if lo >> i & 1] + [64 + i for i in range(57) if hi >> i & 1])


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def source_file(artifact_dir: str, filename: str, saved_raw_only: bool = False) -> Path:
    local_path = ART / artifact_dir / filename
    raw_path = RAW / f"model-hard2-{artifact_dir}-{filename}"
    if not saved_raw_only and local_path.is_file():
        return local_path
    if raw_path.is_file():
        return raw_path
    raise FileNotFoundError(f"artifact source not found: {local_path} or {raw_path}")


def regenerate_boundary() -> dict[tuple[int, int], dict[str, object]]:
    """Recompute complete safe canonical s6 union and parent incidence from geometry."""
    boundary: dict[tuple[int, int], dict[str, object]] = {}
    for parent_index, parent in enumerate(PARENTS):
        parent_points = points(parent)
        if (len(parent_points) != 5 or has_forbidden_quad(parent_points)
                or tuple(d4_canonical_key(parent_points)) != parent):
            raise SystemExit(f"invalid/noncanonical parent key: {parent}")
        occupied = set(parent_points)
        for move in legal_after(occupied):
            child_points = tuple(sorted((*occupied, move)))
            if len(child_points) != 6 or has_forbidden_quad(child_points):
                raise SystemExit(f"geometry returned unsafe extension of {parent}: {move}")
            child = tuple(d4_canonical_key(child_points))
            # Audit the parent relation independently by deleting each stone.
            predecessors = {tuple(d4_canonical_key([p for p in child_points if p != removed]))
                             for removed in child_points}
            if parent not in predecessors:
                raise SystemExit(f"generated child does not have parent {parent}: {child}")
            boundary.setdefault(child, {"parent_indices": set(), "legal_count": None})["parent_indices"].add(parent_index)
    for child, item in boundary.items():
        child_points = points(child)
        if (len(child_points) != 6 or has_forbidden_quad(child_points)
                or tuple(d4_canonical_key(child_points)) != child):
            raise SystemExit(f"regenerated unsafe/noncanonical s6 key: {child}")
        item["legal_count"] = len(legal_after(set(child_points)))
    return boundary


def main() -> None:
    _s5_quarantine = quarantined_cache_keys()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--saved-raw-only", action="store_true", help="ignore downloaded .local artifacts and use output/raw copies")
    ap.add_argument("--boundary-meta", type=Path, help=argparse.SUPPRESS)
    ap.add_argument("--boundary-csv", type=Path, help=argparse.SUPPRESS)
    args = ap.parse_args()
    boundary_meta_path = args.boundary_meta or EXP / "output/next-hard2-s6-meta.json"
    boundary_csv_path = args.boundary_csv or EXP / "output/next-hard2-s6-boundary.csv"
    own_meta = json.loads(boundary_meta_path.read_text(encoding="utf-8"))
    own_rows = list(csv.reader(boundary_csv_path.open(encoding="utf-8", newline="")))
    own_boundary: set[tuple[int, int]] = set()
    own_csv_legal: dict[tuple[int, int], int] = {}
    for row in own_rows:
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 11 or row[0] != "target" or int(row[2]) != 6:
            raise SystemExit(f"unexpected row in independent boundary CSV: {row}")
        key = (int(row[3]), int(row[4]))
        if key in own_boundary:
            raise SystemExit(f"duplicate key in independent boundary CSV: {key}")
        own_boundary.add(key)
        own_csv_legal[key] = int(row[5])
    if len(own_boundary) != own_meta["complete_boundary_count"]:
        raise SystemExit("our boundary CSV count disagrees with its metadata")

    regenerated = regenerate_boundary()
    regenerated_keys = set(regenerated)
    regenerated_relations = {key: sorted(item["parent_indices"]) for key, item in regenerated.items()}
    if own_boundary != regenerated_keys:
        raise SystemExit(f"saved boundary differs from geometry: saved={len(own_boundary)}, regenerated={len(regenerated_keys)}")
    if own_meta.get("parent_keys") != [list(parent) for parent in PARENTS]:
        raise SystemExit("independent metadata parent keys mismatch")
    own_meta_children: dict[tuple[int, int], dict[str, object]] = {}
    for child_item in own_meta.get("canonical_children", []):
        key = tuple(child_item["key"])
        if key in own_meta_children:
            raise SystemExit(f"duplicate key in independent metadata: {key}")
        own_meta_children[key] = child_item
    if set(own_meta_children) != regenerated_keys:
        raise SystemExit("independent metadata keys differ from regenerated geometry")
    for key, generated_item in regenerated.items():
        saved_item = own_meta_children[key]
        if sorted(saved_item["parent_indices"]) != regenerated_relations[key]:
            raise SystemExit(f"independent metadata parent incidence mismatch: {key}")
        if int(saved_item["legal_count"]) != generated_item["legal_count"]:
            raise SystemExit(f"independent metadata legal count mismatch: {key}")
        if own_csv_legal[key] != generated_item["legal_count"]:
            raise SystemExit(f"independent CSV legal count mismatch: {key}")
    expected_parent_rows = [
        {"key": list(parent), "child_count": sum(index in indices for indices in regenerated_relations.values())}
        for index, parent in enumerate(PARENTS)
    ]
    if own_meta.get("parents") != expected_parent_rows:
        raise SystemExit("independent metadata per-parent counts mismatch")
    expected_relation_count = sum(len(indices) for indices in regenerated_relations.values())
    if int(own_meta.get("parent_child_relation_count", -1)) != expected_relation_count:
        raise SystemExit("independent metadata parent-child relation count mismatch")

    material_dir = "reply27-model-hard2-materialized"
    raw_meta_path = source_file(material_dir, "hard2-meta.json", args.saved_raw_only)
    raw_meta = json.loads(raw_meta_path.read_text(encoding="utf-8"))
    raw_relation_map = {tuple(map(int, key.split(":"))): list(value) for key, value in raw_meta["parents"].items()}
    if raw_meta["hard_s5"] != [list(p) for p in PARENTS]:
        raise SystemExit("run metadata parent keys mismatch")
    if raw_relation_map != regenerated_relations or set(raw_relation_map) != regenerated_keys:
        raise SystemExit("run materialized boundary/incidence differs from independent boundary")
    expected_per_parent = [row["child_count"] for row in expected_parent_rows]
    if raw_meta.get("per_parent_canonical_s6") != expected_per_parent:
        raise SystemExit("run metadata per-parent canonical child counts mismatch")
    if raw_meta.get("unique_canonical_s6") != len(regenerated_keys):
        raise SystemExit("run metadata unique canonical child count mismatch")

    shard_names = [f"reply27-model-hard2-s6-{i}" for i in range(4)]
    rows_by_key: dict[tuple[int, int], tuple[int, int, int, str]] = {}
    shard_stats = []
    selected_shards = []
    for shard in shard_names:
        path = source_file(shard, "out.csv", args.saved_raw_only)
        targets_path = source_file(shard, "targets.csv", args.saved_raw_only)
        time_path = source_file(shard, "time", args.saved_raw_only)
        selected_shards.append((shard, path, targets_path, time_path))
        row_count = 0
        result_counts: Counter[int] = Counter()
        with path.open(newline="", encoding="utf-8") as fp:
            for row in csv.reader(fp):
                if not row or (row[0].lstrip().startswith("#")):
                    continue
                if row[0] != "replay":
                    raise SystemExit(f"unexpected non-comment row in saved replay output: {row}")
                row_count += 1
                if len(row) != 11 or int(row[2]) != 6 or int(row[4]) != 1:
                    raise SystemExit(f"unexpected replay schema or non-s6 OR row: {row}")
                key = (int(row[9]), int(row[10]))
                pts = points(key)
                if len(pts) != 6 or has_forbidden_quad(pts):
                    raise SystemExit(f"unsafe s6 replay key {key}")
                canonical = tuple(d4_canonical_key(pts))
                if canonical != key:
                    raise SystemExit(f"noncanonical s6 replay key {key}, canonical={canonical}")
                if key not in own_boundary:
                    raise SystemExit(f"replay key outside independent boundary {key}")
                legal, verdict = int(row[3]), int(row[6])
                expected_legal = int(regenerated[key]["legal_count"])
                if legal != expected_legal:
                    raise SystemExit(f"legal count mismatch for {key}: replay={legal}, geometry={expected_legal}")
                if verdict not in (0, 1, 2):
                    raise SystemExit(f"invalid verdict {verdict}: {row}")
                prior = rows_by_key.get(key)
                item = (legal, verdict, int(row[7]), shard)
                if prior is not None and prior[:2] != item[:2]:
                    raise SystemExit(f"conflicting duplicate result for {key}: {prior} vs {item}")
                if prior is not None:
                    raise SystemExit(f"duplicate replay key across shards: {key}")
                rows_by_key[key] = item
                result_counts[verdict] += 1
        shard_stats.append({"name": shard, "rows": row_count, "results": dict(sorted(result_counts.items())),
                            "out_sha256": sha(path), "targets_sha256": sha(targets_path),
                            "time_sha256": sha(time_path)})
    missing = sorted(own_boundary - rows_by_key.keys())
    if missing:
        raise SystemExit(f"missing {len(missing)} expected boundary replay rows; first={missing[:3]}")

    parent_results = []
    cache_rows = []
    for pi, parent in enumerate(PARENTS):
        children = sorted(k for k, indices in regenerated_relations.items() if pi in indices)
        verdicts = [rows_by_key[k][1] for k in children]
        if any(v == 2 for v in verdicts):
            label, cache_code, witness = "LOSS", 2, min(k for k in children if rows_by_key[k][1] == 2)
        elif all(v == 1 for v in verdicts):
            label, cache_code, witness = "WIN", 1, None
        else:
            label, cache_code, witness = "UNKNOWN", None, None
        if cache_code is not None:
            cache_rows.append((parent[0], parent[1], cache_code))
        parent_results.append({"key": list(parent), "boundary_children": len(children), "verdict_counts": dict(sorted(Counter(verdicts).items())),
                              "derived_label": label, "loss_witness_key": list(witness) if witness else None,
                              "all_children_win": all(v == 1 for v in verdicts)})

    proof_dir = "reply27-model-hard2-s6-proof"
    source_cache_path = source_file(proof_dir, "model-hard2-s5.cache", args.saved_raw_only)
    source_cache = {}
    for line in source_cache_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("s5verdict,"):
            fields = line.split(",")
            if len(fields) != 6:
                raise SystemExit(f"invalid source parent cache row: {line}")
            if int(fields[3]) != 5 or int(fields[4]) not in (1, 2):
                raise SystemExit(f"invalid source parent cache stone count/verdict: {line}")
            key = (int(fields[1]), int(fields[2]))
            if key in _s5_quarantine:
                continue
            pts = points(key)
            if len(pts) != 5 or has_forbidden_quad(pts) or tuple(d4_canonical_key(pts)) != key:
                raise SystemExit(f"invalid/noncanonical s5 source cache key: {key}")
            if key in source_cache:
                raise SystemExit(f"duplicate s5 source cache key: {key}")
            source_cache[key] = int(fields[4])
    derived_map = {(lo, hi): verdict for lo, hi, verdict in cache_rows}
    if source_cache != derived_map:
        raise SystemExit(f"Actions parent cache disagrees with independent propagation: {source_cache} != {derived_map}")

    source_paths = [raw_meta_path, source_file(material_dir, "hard2-s6.csv", args.saved_raw_only),
                    source_file(proof_dir, "result.json", args.saved_raw_only), source_cache_path]
    source_paths += [p for _name, outp, targetp, timep in selected_shards for p in (outp, targetp, timep)]
    for p in source_paths:
        if p.resolve().is_relative_to(RAW.resolve()):
            continue
        artifact_dir = p.parent.name
        dest = RAW / f"model-hard2-{artifact_dir}-{p.name}"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(p.read_bytes())

    cache_path = EXP / "output/model-hard2-derived-s5.cache"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with cache_path.open("w", encoding="utf-8", newline="") as fp:
        fp.write("# s5 verdict cache: n=11 schema=1 (derived by complete s6 boundary AND/OR propagation)\n")
        for lo, hi, result in sorted(cache_rows):
            fp.write(f"s5verdict,{lo},{hi},5,{result},0\n")
    audit = {
        "schema": "model-hard2-independent-check-v1",
        "github_actions_run_id": 37339663025,
        "artifact_source": "saved GitHub Actions run 37339663025 files selected from .local artifacts when available, otherwise output/raw persisted copies",
        "saved_raw_only": args.saved_raw_only,
        "solver_outcome_trust": "Exact s6 verdict values are accepted from the Actions solver; this audit independently checks geometry, complete-boundary equality, replay coverage, and the specified parent propagation.",
        "boundary_comparison": {"independent_boundary_count": len(regenerated_keys), "run_metadata_boundary_count": len(raw_relation_map),
                                "same_canonical_keys_and_parent_incidence": True, "same_parent_child_counts": expected_per_parent,
                                "geometry_regenerated_at_audit_time": True, "legal_counts_regenerated_at_audit_time": True,
                                "independent_metadata_sha256": sha(boundary_meta_path), "independent_boundary_csv_sha256": sha(boundary_csv_path),
                                "run_metadata_sha256": sha(raw_meta_path),
                                "geometry_module": str((ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py").relative_to(ROOT)),
                                "geometry_module_sha256": sha(ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py")},
        "parents": parent_results,
        "actions_parent_cache_matches_independent_propagation": True,
        "replay": {"row_count": len(rows_by_key), "expected_boundary_count": len(own_boundary), "missing_count": 0,
                   "duplicate_or_conflicting_keys": 0, "result_counts": dict(sorted(Counter(v[1] for v in rows_by_key.values()).items())),
                   "shards": shard_stats},
        "sources": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size} for p in source_paths],
        "derived_cache_sha256": sha(cache_path),
    }
    (EXP / "output/model-hard2-independent-check.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"boundary": len(own_boundary), "rows": len(rows_by_key), "parents": parent_results,
                      "result_counts": audit["replay"]["result_counts"], "cache": str(cache_path)}, sort_keys=True))


if __name__ == "__main__":
    main()

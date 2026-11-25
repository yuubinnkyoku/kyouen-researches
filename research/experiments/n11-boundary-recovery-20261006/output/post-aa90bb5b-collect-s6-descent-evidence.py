#!/usr/bin/env python3
"""Archive and independently check a local canonical s6-boundary run."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    return tuple([p for p in range(64) if lo >> p & 1]
                 + [64 + p for p in range(57) if hi >> p & 1])


def checked(key: tuple[int, int], count: int) -> tuple[int, int]:
    pts = points(key)
    if (len(pts) != count or has_forbidden_quad(pts)
            or tuple(d4_canonical_key(pts)) != key):
        raise SystemExit(f"unsafe/noncanonical s{count} key: {key}")
    return key


def read_one_s5_target(path: Path) -> tuple[int, int]:
    targets = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
                raise SystemExit(f"invalid s5 AND parent {path}:{line_no}: {row}")
            key = checked((int(row[3]), int(row[4])), 5)
            if int(row[5]) != len(legal_after(set(points(key)))):
                raise SystemExit(f"s5 legal count mismatch: {key}")
            targets.append(key)
    if len(targets) != 1:
        raise SystemExit(f"expected exactly one s5 parent, found {len(targets)}")
    return targets[0]


def read_replay(path: Path) -> list[str]:
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if row[0] != "replay" or len(row) != 11 or int(row[2]) != 6 or int(row[4]) != 1:
                raise SystemExit(f"invalid s6 AND replay {path}:{line_no}: {row}")
            key = checked((int(row[9]), int(row[10])), 6)
            legal = len(legal_after(set(points(key))))
            if int(row[3]) != legal or int(row[6]) not in (0, 1, 2) or int(row[7]) < 0:
                raise SystemExit(f"s6 replay geometry/verdict invalid {path}:{line_no}: {row}")
            rows.append(row)
    if len(rows) != 1:
        raise SystemExit(f"expected one s6 replay row in {path}, found {len(rows)}")
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--parents", type=Path, required=True)
    ap.add_argument("--saved-target-audit", type=Path, required=True)
    ap.add_argument("--saved-s6-source-audit", type=Path, required=True)
    ap.add_argument("--base-s5-cache", type=Path, required=True)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--solver-source", type=Path, required=True)
    ap.add_argument("--runner", type=Path, required=True)
    ap.add_argument("--main-commit", required=True)
    ap.add_argument("--out-prefix", type=Path, required=True)
    args = ap.parse_args()

    parent = read_one_s5_target(args.parents)
    run_summary_path = args.run_dir / "summary.json"
    run = json.loads(run_summary_path.read_text(encoding="utf-8"))
    if run.get("schema") != "n11-complete-s5-via-s6-local-v1":
        raise SystemExit("unexpected s6 completion summary schema")
    if run.get("parents_sha256") != digest(args.parents) or run.get("parent_count") != 1:
        raise SystemExit("s6 completion summary is not bound to the one-parent input")
    if run.get("saved_audit_sha256") != digest(args.saved_s6_source_audit):
        raise SystemExit("s6 completion summary is not bound to the saved-source audit")

    saved_parent_audit = json.loads(args.saved_target_audit.read_text(encoding="utf-8"))
    parents = saved_parent_audit.get("targets", {}).get("parents", [])
    if (len(parents) != 1 or tuple(parents[0].get("key", [])) != parent
            or parents[0].get("outcome") != "UNKNOWN"
            or parents[0].get("counts") != {"UNSEEN": 83}
            or saved_parent_audit.get("cache_comparison", {}).get("new_exact") != 0):
        raise SystemExit("saved-s6 parent audit is not the fully unresolved 83-child boundary")

    parent_children = run.get("parents", [])
    if len(parent_children) != 1 or tuple(parent_children[0].get("key", [])) != parent:
        raise SystemExit("s6 completion output identifies a different parent")
    children = set()
    occupied = set(points(parent))
    for move in legal_after(occupied):
        child_points = tuple(sorted((*occupied, move)))
        if len(child_points) != 6 or has_forbidden_quad(child_points):
            raise SystemExit(f"unsafe s6 extension {parent} + {move}")
        child = tuple(d4_canonical_key(child_points))
        checked(child, 6)
        children.add(child)
    if len(children) != 83 or run.get("boundary_canonical_s6_count") != len(children):
        raise SystemExit("independent s6 boundary cardinality differs from runner summary")

    if run.get("saved_unknown_boundary_count") != 0 or run.get("reused_solver_sources"):
        raise SystemExit("unexpected saved or resumed s6 rows in this fresh descent")
    sources = run.get("new_solver_sources", [])
    if (len(sources) != len(children) or run.get("new_solver_exact") != len(children)
            or run.get("new_solver_unknown") != 0 or run.get("new_solver_rows") != len(children)):
        raise SystemExit("runner did not produce one exact row for every s6 child")

    raw_dir = args.out_prefix.with_name(args.out_prefix.name + "-raw")
    paths = {
        "raw_all": args.out_prefix.with_name(args.out_prefix.name + "-raw-all.csv"),
        "s6_cache": args.out_prefix.with_name(args.out_prefix.name + "-exact-s6.cache"),
        "derived_s5": args.out_prefix.with_name(args.out_prefix.name + "-derived-s5.cache"),
        "runner_summary": args.out_prefix.with_name(args.out_prefix.name + "-runner-summary.json"),
        "receipt": args.out_prefix.with_name(args.out_prefix.name + "-receipt.json"),
        "manifest": args.out_prefix.with_name(args.out_prefix.name + "-sources.json"),
    }
    for path in [raw_dir, *paths.values()]:
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing evidence: {path}")
    raw_dir.mkdir(parents=True)

    raw_rows = []
    raw_records = []
    seen = set()
    verdict_counts = Counter()
    nodes_total = 0
    for source in sources:
        key = tuple(map(int, source["key"]))
        checked(key, 6)
        if key not in children or key in seen:
            raise SystemExit(f"unexpected/duplicate s6 source key: {key}")
        seen.add(key)
        original = Path(source["path"])
        if not original.is_absolute():
            original = ROOT / original
        if digest(original) != source["sha256"]:
            raise SystemExit(f"raw solver output hash mismatch: {original}")
        rows = read_replay(original)
        row = rows[0]
        if (int(row[9]), int(row[10])) != key or int(row[6]) != source["verdict"] or int(row[7]) != source["nodes"]:
            raise SystemExit(f"runner source metadata differs from raw replay: {original}")
        copied = raw_dir / f"s6-{key[0]}-{key[1]}.out.csv"
        shutil.copyfile(original, copied)
        if digest(copied) != digest(original):
            raise SystemExit(f"archived raw copy differs from solver output: {copied}")
        raw_rows.append(row)
        verdict_counts[int(row[6])] += 1
        nodes_total += int(row[7])
        raw_records.append({
            "key": list(key), "verdict": int(row[6]), "nodes": int(row[7]),
            "legal_count": int(row[3]),
            "source": {"path": rel(original), "sha256": digest(original), "bytes": original.stat().st_size},
            "archived_copy": {"path": rel(copied), "sha256": digest(copied), "bytes": copied.stat().st_size},
        })
    if seen != children:
        raise SystemExit(f"s6 raw rows do not cover the complete canonical boundary: missing={sorted(children-seen)[:5]}")

    outcome = "LOSS" if verdict_counts[2] else ("WIN" if verdict_counts[1] == len(children) else "UNKNOWN")
    status = parent_children[0]
    if (status.get("child_count") != len(children)
            or status.get("counts") != {"0": verdict_counts[0], "1": verdict_counts[1], "2": verdict_counts[2]}
            or status.get("outcome") != outcome
            or run.get("status_counts") != {"LOSS": int(outcome == "LOSS"), "UNKNOWN": int(outcome == "UNKNOWN"), "WIN": int(outcome == "WIN")}):
        raise SystemExit("runner s5 AND outcome disagrees with every raw s6 child")

    local_derived = Path(run["derived_s5_cache"]["path"])
    if not local_derived.is_absolute():
        local_derived = ROOT / local_derived
    if digest(local_derived) != run["derived_s5_cache"]["sha256"]:
        raise SystemExit("runner-derived s5 cache hash mismatch")
    derived_rows = [row for row in csv.reader(local_derived.open(newline="", encoding="utf-8-sig"))
                    if row and not row[0].lstrip().startswith("#")]
    expected_verdict = {"WIN": 1, "LOSS": 2}.get(outcome)
    if expected_verdict is None:
        if derived_rows:
            raise SystemExit("runner asserted an exact s5 outcome for an UNKNOWN boundary")
    elif (len(derived_rows) != 1 or derived_rows[0][0] != "s5verdict"
          or (int(derived_rows[0][1]), int(derived_rows[0][2])) != parent
          or int(derived_rows[0][3]) != 5 or int(derived_rows[0][4]) != expected_verdict):
        raise SystemExit("runner-derived s5 cache differs from complete canonical s6 boundary")

    with paths["raw_all"].open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# exact s6 replay rows covering the complete canonical boundary\n")
        csv.writer(stream, lineterminator="\n").writerows(sorted(raw_rows, key=lambda row: (int(row[9]), int(row[10]))))
    with paths["s6_cache"].open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# s6 verdict cache: n=11 schema=1 (exact replay rows only)\n")
        for row in sorted(raw_rows, key=lambda row: (int(row[9]), int(row[10]))):
            stream.write(f"s6verdict,{row[9]},{row[10]},6,{row[6]},{row[7]}\n")
    shutil.copyfile(local_derived, paths["derived_s5"])
    shutil.copyfile(run_summary_path, paths["runner_summary"])

    receipt = {
        "schema": "n11-s6-descent-collection-receipt-v1",
        "main_at_dispatch": args.main_commit,
        "parent_s5": list(parent), "canonical_s6_children": len(children),
        "saved_s6_exact_intersection": 0, "solver_rows": len(raw_rows),
        "s6_verdict_counts": {str(v): verdict_counts[v] for v in (0, 1, 2)},
        "s5_outcome": outcome, "nodes": nodes_total,
        "s6_cache": {"path": rel(paths["s6_cache"]), "sha256": digest(paths["s6_cache"]), "rows": len(children)},
        "derived_s5_cache": {"path": rel(paths["derived_s5"]), "sha256": digest(paths["derived_s5"]), "rows": len(derived_rows)},
        "conflicts": 0,
    }
    paths["receipt"].write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8", newline="\n")
    inputs = [args.parents, args.saved_target_audit, args.saved_s6_source_audit,
              args.base_s5_cache, args.solver, args.solver_source, args.runner,
              run_summary_path, local_derived, Path(__file__).resolve()]
    manifest = {
        "schema": "n11-s6-descent-source-manifest-v1",
        "main_at_dispatch": args.main_commit,
        "claim": "The complete canonical s6 boundary was rebuilt from the s5 parent. Every child has one hash-attested exact solver row; s5 outcome is derived by its AND recurrence only.",
        "parent_s5": list(parent), "parent_outcome": outcome,
        "inputs": [{"path": rel(path), "sha256": digest(path), "bytes": path.stat().st_size}
                   for path in inputs],
        "s6_children": raw_records,
        "outputs": [{"path": rel(path), "sha256": digest(path), "bytes": path.stat().st_size}
                    for path in [paths["raw_all"], paths["s6_cache"], paths["derived_s5"],
                                 paths["runner_summary"], paths["receipt"]]],
    }
    manifest["outputs"].extend({"path": rel(path), "sha256": digest(path), "bytes": path.stat().st_size}
                                for path in sorted(raw_dir.iterdir()))
    paths["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")
    print(json.dumps({"parent_s5": list(parent), "canonical_s6_children": len(children),
                      "s6_verdict_counts": receipt["s6_verdict_counts"], "s5_outcome": outcome,
                      "nodes": nodes_total, "outputs": {k: rel(v) for k, v in paths.items()}}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

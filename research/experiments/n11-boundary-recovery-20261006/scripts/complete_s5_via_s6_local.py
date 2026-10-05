#!/usr/bin/env python3
"""Resolve a finite set of s5 AND parents using their complete canonical s6 boundaries."""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import json
import os
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402
sys.path.insert(0, str(EXP / "scripts"))
from audit_saved_s6_targets import points, read_saved_exact_s6, safe_canonical, sha256  # noqa: E402


def checked_key(key: tuple[int, int], stones: int) -> tuple[int, ...]:
    pts = points(key)
    if len(pts) != stones or has_forbidden_quad(pts) or tuple(d4_canonical_key(pts)) != key:
        raise ValueError(f"unsafe/noncanonical s{stones} key: {key}")
    return pts


def read_parents(path: Path) -> list[tuple[int, int]]:
    result = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11:
                raise ValueError(f"expected 11-column target row at {path}:{line_no}: {row}")
            if not row[0] or int(row[2]) != 5 or int(row[7]) != 0:
                raise ValueError(f"expected s5 AND target at {path}:{line_no}: {row}")
            key = (int(row[3]), int(row[4]))
            pts = checked_key(key, 5)
            if int(row[5]) != len(legal_after(set(pts))):
                raise ValueError(f"parent legal count mismatch at {path}:{line_no}: {key}")
            result.append(key)
    if not result or len(set(result)) != len(result):
        raise ValueError("parent CSV is empty or contains duplicate keys")
    common_classes = None
    for key in result:
        pts = checked_key(key, 5)
        classes = {tuple(d4_canonical_key([p for p in pts if p != removed])) for removed in pts}
        common_classes = classes if common_classes is None else common_classes & classes
    if not common_classes:
        raise ValueError("parent CSV must contain one canonical s4 class")
    return result


def generate_boundary(parents: list[tuple[int, int]]):
    incidence: dict[tuple[int, int], set[int]] = defaultdict(set)
    legal_counts = {}
    parent_children = []
    for pi, parent in enumerate(parents):
        pset = set(checked_key(parent, 5))
        child_keys = set()
        for move in legal_after(pset):
            child_pts = tuple(sorted((*pset, move)))
            if len(child_pts) != 6 or has_forbidden_quad(child_pts):
                raise ValueError(f"unsafe legal extension {parent} + {move}")
            child = tuple(d4_canonical_key(child_pts))
            checked_key(child, 6)
            preds = {tuple(d4_canonical_key([p for p in child_pts if p != removed]))
                     for removed in child_pts}
            if parent not in preds:
                raise ValueError(f"reverse incidence failure: {parent} -> {child}")
            child_keys.add(child)
            incidence[child].add(pi)
        parent_children.append(sorted(child_keys))
        for child in child_keys:
            count = len(legal_after(set(checked_key(child, 6))))
            if child in legal_counts and legal_counts[child] != count:
                raise ValueError(f"inconsistent legal count for shared child {child}")
            legal_counts[child] = count
    return parent_children, incidence, legal_counts


def classify(children: set[tuple[int, int]], verdicts: dict[tuple[int, int], int]) -> str:
    if any(verdicts.get(key) == 2 for key in children):
        return "LOSS"
    if all(verdicts.get(key) == 1 for key in children):
        return "WIN"  # includes the empty AND boundary
    return "UNKNOWN"


def validate_verdict_map(verdicts: dict[tuple[int, int], int]) -> None:
    if any(v not in (0, 1, 2) for v in verdicts.values()):
        raise ValueError("invalid exact/unknown verdict")


def validate_saved_audit(audit: dict) -> None:
    if audit.get("run_status") != "ok":
        raise ValueError(f"saved audit run_status is not ok: {audit.get('run_status')!r}")
    if audit.get("rejected_conflicts"):
        raise ValueError("saved audit reports rejected conflicts")
    comparison = audit.get("cache_comparison", {})
    if comparison.get("rejected_conflicts") or comparison.get("conflicts"):
        raise ValueError("saved audit reports rejected/opposite conflicts")
    for field in ("internal_conflict", "current_cache_internal_conflicts", "opposite_verdict"):
        if comparison.get(field, 0) != 0:
            raise ValueError(f"saved audit reports {field}={comparison[field]}")


def merge_verdict(verdicts: dict[tuple[int, int], int], key: tuple[int, int], value: int) -> None:
    if value not in (0, 1, 2):
        raise ValueError(f"invalid solver verdict {value}")
    old = verdicts.get(key)
    if old in (1, 2) and value in (1, 2) and old != value:
        raise ValueError(f"exact s6 conflict for {key}: {old} vs {value}")
    # Exact evidence supersedes a prior UNKNOWN; UNKNOWN never erases exact.
    if value in (1, 2) or old is None:
        verdicts[key] = value


def parse_replay(path: Path, key: tuple[int, int], expected_legal: int) -> tuple[int, int]:
    found = None
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if row[0] == "replay_error":
                raise ValueError(f"solver replay error at {path}:{line_no}: {row}")
            if row[0] != "replay" or len(row) != 11:
                raise ValueError(f"unexpected solver output row at {path}:{line_no}: {row}")
            stones, legal, is_or = int(row[2]), int(row[3]), int(row[4])
            verdict, nodes = int(row[6]), int(row[7])
            row_key = (int(row[9]), int(row[10]))
            if (stones != 6 or is_or != 1 or row_key != key or legal != expected_legal
                    or verdict not in (0, 1, 2) or nodes < 0):
                raise ValueError(f"solver replay row mismatch at {path}:{line_no}: {row}")
            checked_key(row_key, 6)
            if found is not None:
                raise ValueError(f"duplicate solver replay row for {key}: {path}")
            found = (verdict, nodes)
    if found is None:
        raise ValueError(f"missing solver replay row: {path}")
    return found


def output_path(out_dir: Path, key: tuple[int, int]) -> Path:
    return out_dir / f"s6-{key[0]}-{key[1]}.out.csv"


def solve_one(solver: Path, out_dir: Path, key: tuple[int, int], legal: int, budget: int):
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"s6-{key[0]}-{key[1]}.input.csv"
    final = output_path(out_dir, key)
    temp = final.with_suffix(final.suffix + ".tmp")
    log = out_dir / f"s6-{key[0]}-{key[1]}.log"
    with target.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream, lineterminator="\n").writerow(
            ["target", 0, 6, key[0], key[1], legal, 0, 1, 0, 0, 0])
    prefix = [sys.executable, str(solver)] if solver.suffix.lower() == ".py" else [str(solver)]
    command = prefix + ["--n=11", "--memo=22", f"--exact-replay={target}", "--only=6",
                        "--exact-order=count", f"--exact-replay-budget={budget}", f"--csv={temp}"]
    started = time.monotonic()
    with log.open("w", encoding="utf-8") as stream:
        completed = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"solver exited {completed.returncode} for {key}; see {log}")
    if not temp.is_file():
        raise RuntimeError(f"solver did not create {temp}; see {log}")
    verdict, nodes = parse_replay(temp, key, legal)
    os.replace(temp, final)
    return verdict, nodes, time.monotonic() - started


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(temp, path)


def run_adaptive(parents, parent_children, incidence, legal_counts, verdicts,
                 solve_fn, workers: int):
    validate_verdict_map(verdicts)
    active = {}
    submitted = set()
    new_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        while True:
            statuses = [classify(set(children), verdicts) for children in parent_children]
            if "WIN" in statuses:
                break
            unresolved = {i for i, status in enumerate(statuses) if status == "UNKNOWN"}
            candidates = {child for child, parents_for_child in incidence.items()
                          if child not in verdicts and child not in submitted
                          and unresolved.intersection(parents_for_child)}
            candidates = sorted(candidates, key=lambda k: (legal_counts[k], k))
            while candidates and len(active) < workers:
                key = candidates.pop(0)
                submitted.add(key)
                active[pool.submit(solve_fn, key, legal_counts[key])] = key
            if not active:
                break
            done, _ = concurrent.futures.wait(active, return_when=concurrent.futures.FIRST_COMPLETED)
            for future in done:
                key = active.pop(future)
                result = future.result()
                value, nodes = result[0], result[1]
                merge_verdict(verdicts, key, value)
                new_results[key] = {"verdict": value, "nodes": nodes}
        # Any work already in flight is preserved even when a parent is resolved.
        for future, key in list(active.items()):
            result = future.result()
            value, nodes = result[0], result[1]
            merge_verdict(verdicts, key, value)
            new_results[key] = {"verdict": value, "nodes": nodes}
    return [classify(set(children), verdicts) for children in parent_children], new_results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--parents", type=Path, required=True)
    ap.add_argument("--saved-audit", type=Path, required=True)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--budget", type=int, default=2_000_000)
    args = ap.parse_args()
    if args.workers < 1 or args.budget < 1:
        ap.error("--workers and --budget must be positive")
    if not args.solver.is_file():
        ap.error(f"solver not found: {args.solver}")

    parents = read_parents(args.parents)
    source_audit = json.loads(args.saved_audit.read_text(encoding="utf-8"))
    validate_saved_audit(source_audit)
    if not source_audit.get("s6", {}).get("all_s6_exact_rows_geometry_checked"):
        raise ValueError("saved audit does not attest s6 geometry/legal validation")
    exact, source_reports = read_saved_exact_s6(source_audit)
    verdicts = {key: rec["verdict"] for key, rec in exact.items()}
    parent_children, incidence, legal_counts = generate_boundary(parents)
    boundary = set(incidence)
    for key in boundary & exact.keys():
        if exact[key]["legal_counts"] != [legal_counts[key]]:
            raise ValueError(f"saved exact legal count mismatch for {key}: {exact[key]['legal_counts']} != {legal_counts[key]}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    reused_sources = []
    for key in sorted(boundary):
        path = output_path(args.out_dir, key)
        if not path.exists():
            continue
        value, nodes = parse_replay(path, key, legal_counts[key])
        reused_sources.append({"key": list(key), "path": str(path.resolve()), "sha256": sha256(path),
                               "verdict": value, "nodes": nodes})
        merge_verdict(verdicts, key, value)

    def solve(key, legal):
        return solve_one(args.solver, args.out_dir, key, legal, args.budget)

    outcomes, new_results = run_adaptive(parents, parent_children, incidence, legal_counts,
                                         verdicts, solve, args.workers)
    rows = []
    for i, parent in enumerate(parents):
        children = parent_children[i]
        counts = {str(v): sum(verdicts.get(k) == v for k in children) for v in (0, 1, 2)}
        rows.append({"key": list(parent), "outcome": outcomes[i], "child_count": len(children),
                     "counts": counts, "loss_witnesses": [list(k) for k in children if verdicts.get(k) == 2],
                     "unresolved_children": [list(k) for k in children if verdicts.get(k) not in (1, 2)]})

    exact_derived = [(parents[i], 1 if status == "WIN" else 2)
                     for i, status in enumerate(outcomes) if status in ("WIN", "LOSS")]
    cache_text = "# s5 verdict cache: n=11 schema=1 (complete-boundary exact results)\n"
    cache_text += "".join(f"s5verdict,{lo},{hi},5,{value},0\n" for (lo, hi), value in sorted(exact_derived))
    cache_path = args.out_dir / "derived-s5.cache"
    atomic_text(cache_path, cache_text)

    sources = []
    for key, result in sorted(new_results.items()):
        path = output_path(args.out_dir, key)
        sources.append({"key": list(key), "path": str(path.resolve()), "sha256": sha256(path),
                        "verdict": result["verdict"], "nodes": result["nodes"]})
    summary = {
        "schema": "n11-complete-s5-via-s6-local-v1",
        "outcome_provenance": "Exact s6 values are solver replay results (or hash-attested saved replay results); this runner independently regenerates safe canonical boundaries and applies AND propagation.",
        "parents_path": str(args.parents.resolve()), "parents_sha256": sha256(args.parents),
        "saved_audit_path": str(args.saved_audit.resolve()), "saved_audit_sha256": sha256(args.saved_audit),
        "saved_source_reports": source_reports, "parent_count": len(parents),
        "boundary_canonical_s6_count": len(boundary), "parent_child_relations": sum(map(len, parent_children)),
        "status_counts": {name: outcomes.count(name) for name in ("WIN", "LOSS", "UNKNOWN")},
        "parents": rows, "saved_unknown_boundary_count": sum(verdicts.get(k) == 0 for k in boundary),
        "new_solver_rows": len(new_results), "new_solver_exact": sum(x["verdict"] in (1, 2) for x in new_results.values()),
        "new_solver_unknown": sum(x["verdict"] == 0 for x in new_results.values()),
        "new_solver_sources": sources, "workers": args.workers, "budget": args.budget,
        "reused_solver_sources": reused_sources,
        "nodes_reused": sum(item["nodes"] for item in reused_sources),
        "nodes_new": sum(item["nodes"] for item in new_results.values()),
        "derived_s5_cache": {"path": str(cache_path.resolve()), "sha256": sha256(cache_path), "rows": len(exact_derived)},
    }
    atomic_text(args.out_dir / "summary.json", json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"parents": len(parents), "boundary_s6": len(boundary),
                      "outcomes": summary["status_counts"], "new_rows": len(new_results)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run a hash-bound, adaptive exact s7 witness probe for unresolved s6 OR parents."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402
sys.path.insert(0, str(ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"))
from audit_saved_s6_targets import points, safe_canonical  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_target_csv(path: Path) -> list[dict]:
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or row[0] != "target" or int(row[2]) != 7 or int(row[7]) != 0:
                raise ValueError(f"expected canonical s7 AND target at {path}:{line_no}: {row}")
            key = (int(row[3]), int(row[4]))
            pts = points(key)
            if len(pts) != 7 or has_forbidden_quad(pts) or tuple(d4_canonical_key(pts)) != key:
                raise ValueError(f"unsafe/noncanonical s7 target: {key}")
            legal = len(legal_after(set(pts)))
            if int(row[5]) != legal:
                raise ValueError(f"s7 target legal-count mismatch for {key}: {row[5]} != {legal}")
            rows.append({"id": int(row[1]), "key": key, "legal": legal, "row": row})
    if len({item["key"] for item in rows}) != len(rows):
        raise ValueError("duplicate s7 targets")
    return rows


def parse_solver_output(path: Path, target: dict, budget: int) -> tuple[int, int]:
    found = None
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                continue
            if len(row) != 11:
                raise ValueError(f"invalid s7 solver row at {path}:{line_no}: {row}")
            stones, legal, is_or, seen_budget, verdict, nodes = map(int, (row[2], row[3], row[4], row[5], row[6], row[7]))
            key = (int(row[9]), int(row[10]))
            if (stones != 7 or legal != target["legal"] or is_or != 0 or seen_budget != budget
                    or key != target["key"] or verdict not in (0, 1, 2) or nodes < 0
                    or not safe_canonical(key, 7)):
                raise ValueError(f"s7 solver row does not match scheduled target at {path}:{line_no}: {row}")
            if found is not None:
                raise ValueError(f"duplicate solver rows for s7 target {key}: {path}")
            found = (verdict, nodes)
    if found is None:
        raise ValueError(f"missing s7 solver output row: {path}")
    return found


def s6_outcome(children: set[tuple[int, int]], s7_exact: dict[tuple[int, int], int]) -> str:
    if any(s7_exact.get(child) == 2 for child in children):
        return "WIN"
    if children and all(s7_exact.get(child) == 1 for child in children):
        return "LOSS"
    return "UNKNOWN"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s5-s6-boundary-full-gzip", type=Path, required=True)
    parser.add_argument("--s7-preflight", type=Path, required=True)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--budget", type=int, default=1_000_000)
    args = parser.parse_args()
    if args.budget < 1:
        parser.error("--budget must be positive")
    if not args.solver.is_file():
        parser.error(f"solver not found: {args.solver}")
    if args.out_dir.exists():
        raise SystemExit(f"refusing to reuse existing output directory: {args.out_dir}")

    preflight = json.loads(args.s7_preflight.read_text(encoding="utf-8"))
    schedule = preflight.get("schedule", {})
    if (not schedule.get("covers_every_unresolved_s6_parent")
            or schedule.get("ready_target_count") == 0
            or schedule.get("targets_sha256") != sha256(args.targets)
            or preflight.get("inputs", {}).get("budget_for_proposed_probe") != args.budget
            or schedule.get("exact_verdict_conflicts") != 0
            or schedule.get("same_or_higher_budget_unknown_key_count") != 0):
        raise SystemExit("S7 preflight is stale, blocked, or not tied to this target/budget")
    if preflight.get("inputs", {}).get("scan_s7_replay_rows_in_target_boundaries") != 0:
        raise SystemExit("S7 boundary history is nonempty; rebuild an exact-key ready schedule before dispatch")
    targets = read_target_csv(args.targets)
    if len(targets) != schedule.get("ready_target_count"):
        raise SystemExit("target CSV row count differs from S7 preflight")
    planned = {tuple(item["key"]): set(tuple(p) for p in item["affected_s6_parents"])
               for item in schedule.get("selected_targets", [])}
    if set(planned) != {item["key"] for item in targets}:
        raise SystemExit("target CSV keys differ from S7 preflight selected targets")

    full_s5_boundary = json.loads(gzip.decompress(args.s5_s6_boundary_full_gzip.read_bytes()))
    s5_parent_rows = full_s5_boundary.get("targets", {}).get("parents", [])
    if len(s5_parent_rows) != 1 or len(s5_parent_rows[0].get("children", [])) != 90:
        raise SystemExit("expected the complete 90-child s5 boundary")
    s5_parent = tuple(s5_parent_rows[0]["key"])
    s6_children = {tuple(item["key"]): item["status"] for item in s5_parent_rows[0]["children"]}
    if Counter(s6_children.values()) != Counter({"WIN": 87, "UNKNOWN": 3}):
        raise SystemExit("s5 boundary has changed; rebuild s6 and s7 audits before dispatch")
    s6_unknowns = {key for key, status in s6_children.items() if status == "UNKNOWN"}
    if not s6_unknowns or any(not safe_canonical(key, 6) for key in s6_unknowns):
        raise SystemExit("invalid unresolved s6 parent set")

    s7_children_by_s6 = {}
    for parent in s6_unknowns:
        pts = set(points(parent))
        children = set()
        for move in legal_after(pts):
            child_pts = tuple(sorted((*pts, move)))
            child = tuple(d4_canonical_key(child_pts))
            if len(child_pts) != 7 or has_forbidden_quad(child_pts) or not safe_canonical(child, 7):
                raise SystemExit(f"invalid s7 extension while binding schedule: {parent} + {move}")
            predecessors = {tuple(d4_canonical_key([p for p in child_pts if p != removed]))
                            for removed in child_pts}
            if parent not in predecessors:
                raise SystemExit(f"s7 target fails reverse incidence: {parent} -> {child}")
            children.add(child)
        s7_children_by_s6[parent] = children

    for target in targets:
        key = target["key"]
        affected = {parent for parent, children in s7_children_by_s6.items() if key in children}
        if affected != planned[key]:
            raise SystemExit(f"S7 target incidence differs from preflight for {key}: {affected} != {planned[key]}")

    args.out_dir.mkdir(parents=True, exist_ok=False)
    s7_exact: dict[tuple[int, int], int] = {}
    new_sources = []
    skipped_targets = []
    start = time.monotonic()

    def s5_status() -> str:
        statuses = dict(s6_children)
        for parent, children in s7_children_by_s6.items():
            statuses[parent] = s6_outcome(children, s7_exact)
        if any(statuses[key] == "LOSS" for key in s6_children):
            return "LOSS"
        if all(statuses[key] == "WIN" for key in s6_children):
            return "WIN"
        return "UNKNOWN"

    for target in targets:
        if s5_status() in ("WIN", "LOSS"):
            skipped_targets.extend(list(item["key"]) for item in targets if item["key"] != target["key"]
                                   and tuple(item["key"]) not in s7_exact)
            break
        key = target["key"]
        stem = f"s7-{key[0]}-{key[1]}"
        input_path = args.out_dir / f"{stem}.input.csv"
        output_path = args.out_dir / f"{stem}.out.csv"
        temporary_output = output_path.with_suffix(output_path.suffix + ".tmp")
        log_path = args.out_dir / f"{stem}.log"
        if any(path.exists() for path in (input_path, output_path, temporary_output, log_path)):
            raise SystemExit(f"refusing to overwrite per-target output for {key}")
        with input_path.open("x", newline="", encoding="utf-8") as stream:
            csv.writer(stream, lineterminator="\n").writerow(target["row"])
        prefix = [sys.executable, str(args.solver)] if args.solver.suffix.lower() == ".py" else [str(args.solver)]
        command = prefix + ["--n=11", "--memo=22", f"--exact-replay={input_path}", "--only=7",
                            "--exact-order=count", f"--exact-replay-budget={args.budget}", f"--csv={temporary_output}"]
        with log_path.open("w", encoding="utf-8") as log:
            completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
        if completed.returncode != 0 or not temporary_output.is_file():
            raise RuntimeError(f"s7 exact replay failed for {key}; see {log_path}")
        verdict, nodes = parse_solver_output(temporary_output, target, args.budget)
        os.replace(temporary_output, output_path)
        s7_exact[key] = verdict
        new_sources.append({
            "key": list(key),
            "affected_s6_parents": [list(parent) for parent in sorted(planned[key])],
            "input_path": str(input_path.resolve()),
            "input_sha256": sha256(input_path),
            "raw_output_path": str(output_path.resolve()),
            "raw_output_sha256": sha256(output_path),
            "log_path": str(log_path.resolve()),
            "log_sha256": sha256(log_path),
            "legal": target["legal"],
            "budget": args.budget,
            "verdict": verdict,
            "nodes": nodes,
        })
        if s5_status() in ("WIN", "LOSS"):
            skipped_targets.extend(list(item["key"]) for item in targets if item["key"] != key)
            break

    s6_statuses = {}
    for parent, children in s7_children_by_s6.items():
        s6_statuses[parent] = s6_outcome(children, s7_exact)
    updated_s6_statuses = dict(s6_children)
    updated_s6_statuses.update(s6_statuses)
    counts = Counter(updated_s6_statuses.values())
    result = {
        "schema": "n11-s7-witness-probe-local-run-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "s5_parent": list(s5_parent),
        "s5_boundary_s6_count": len(s6_children),
        "s5_outcome_from_complete_s6_boundary": s5_status(),
        "s6_child_outcomes": {str(value): counts.get(value, 0) for value in ("WIN", "LOSS", "UNKNOWN")},
        "s6_unknown_parents_before": [list(key) for key in sorted(s6_unknowns)],
        "s6_unknown_parents_after": [list(key) for key in sorted(s6_unknowns) if s6_statuses[key] == "UNKNOWN"],
        "s7_boundary_counts": {str(parent[0]) + "," + str(parent[1]): len(children)
                               for parent, children in sorted(s7_children_by_s6.items())},
        "s7_probe_rows": len(new_sources),
        "s7_probe_verdict_counts": dict(sorted(Counter(str(value) for value in s7_exact.values()).items())),
        "nodes": sum(item["nodes"] for item in new_sources),
        "budget_per_target": args.budget,
        "solver": {"path": str(args.solver.resolve()), "sha256": sha256(args.solver)},
        "runner": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
        "preflight": {"path": str(args.s7_preflight.resolve()), "sha256": sha256(args.s7_preflight)},
        "targets": {"path": str(args.targets.resolve()), "sha256": sha256(args.targets)},
        "s5_s6_boundary_full_gzip": {"path": str(args.s5_s6_boundary_full_gzip.resolve()),
                                      "sha256": sha256(args.s5_s6_boundary_full_gzip)},
        "out_dir": str(args.out_dir.resolve()),
        "new_sources": new_sources,
        "not_dispatched_after_parent_resolved": skipped_targets,
        "outcome_provenance": "A s7 exact LOSS child proves its safe canonical s6 OR parent WIN; the s5 parent is classified only from all 90 canonical s6 children. UNKNOWN remains UNKNOWN.",
        "elapsed_seconds": time.monotonic() - start,
    }
    summary_path = args.out_dir / "summary.json"
    summary_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"s5_parent": list(s5_parent), "s5_outcome": result["s5_outcome_from_complete_s6_boundary"],
                      "s6_status_counts": result["s6_child_outcomes"], "new_s7_rows": len(new_sources),
                      "new_s7_verdicts": result["s7_probe_verdict_counts"], "nodes": result["nodes"],
                      "not_dispatched": skipped_targets}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

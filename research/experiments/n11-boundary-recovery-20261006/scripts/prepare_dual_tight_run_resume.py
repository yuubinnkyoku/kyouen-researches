#!/usr/bin/env python3
"""Prepare only never-completed or failed s5 rows for a safe runner resume."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--full-targets", type=Path, required=True)
    ap.add_argument("--checkpoint-summary", type=Path, required=True)
    ap.add_argument("--schedule-manifest", type=Path, required=True)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--solver-source", type=Path, required=True)
    ap.add_argument("--runner", type=Path, required=True)
    ap.add_argument("--out-targets", type=Path, required=True)
    ap.add_argument("--out-manifest", type=Path, required=True)
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--budget", type=int, default=15_000_000)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    if args.out_targets.exists() or args.out_manifest.exists():
        raise SystemExit("refusing to overwrite a resume input or manifest")

    summary = json.loads(args.checkpoint_summary.read_text(encoding="utf-8"))
    schedule = json.loads(args.schedule_manifest.read_text(encoding="utf-8"))
    if schedule.get("probe_target_sha256") != sha256(args.full_targets):
        raise SystemExit("prior schedule does not bind the supplied full target set")
    scheduled_source_hashes = {item["path"]: item["sha256"]
                               for item in schedule.get("sources", [])}
    for path in (args.solver, args.solver_source, args.runner):
        if scheduled_source_hashes.get(rel(path)) != sha256(path):
            raise SystemExit(f"prior schedule source hash mismatch: {rel(path)}")
    cache_paths = [item["path"] for item in schedule.get("sources", [])
                   if item.get("path", "").endswith(".cache")]
    if len(cache_paths) != 1:
        raise SystemExit(f"expected one bound current exact cache, got {cache_paths}")
    if summary.get("exact_win_witnesses"):
        raise SystemExit("checkpoint contains an exact WIN witness; class exploration must remain stopped")
    if summary.get("interrupted_partial_keys"):
        raise SystemExit("checkpoint has interrupted partial solver output; manual audit is required")
    if summary.get("scheduled") != summary.get("completed_rows", 0) \
            + len(summary.get("failed_no_result_keys", [])) \
            + len(summary.get("not_dispatched_keys", [])):
        raise SystemExit("checkpoint statuses do not partition scheduled targets")
    expected_budget = int(summary.get("budget_per_target", args.budget))
    if expected_budget != args.budget:
        raise SystemExit("resume budget differs from the recorded run budget")

    by_key: dict[tuple[int, int], list[str]] = {}
    for row in csv.reader(args.full_targets.open(newline="", encoding="utf-8-sig")):
        if not row or row[0].lstrip().startswith("#"):
            continue
        key = (int(row[3]), int(row[4]))
        if key in by_key:
            raise SystemExit(f"duplicate full target: {key}")
        by_key[key] = row
    full_keys = set(by_key)
    failed = {tuple(map(int, key)) for key in summary.get("failed_no_result_keys", [])}
    waiting = {tuple(map(int, key)) for key in summary.get("not_dispatched_keys", [])}
    resume_keys = failed | waiting
    if failed & waiting or not resume_keys or not resume_keys <= full_keys:
        raise SystemExit("invalid resume target set")
    completed = {tuple(map(int, row["key"])) for row in summary.get("target_statuses", [])
                 if row.get("status") in ("exact_WIN", "exact_LOSS", "completed_UNKNOWN")}
    if resume_keys & completed or resume_keys | completed != full_keys:
        raise SystemExit("resume keys and completed status keys do not partition the full target set")

    rows = [by_key[key] for key in by_key if key in resume_keys]
    args.out_targets.parent.mkdir(parents=True, exist_ok=True)
    with args.out_targets.open("w", newline="", encoding="utf-8") as stream:
        stream.write("# s5 rows with no completed result in the recorded run; exact/UNKNOWN rows excluded\n")
        csv.writer(stream, lineterminator="\n").writerows(rows)

    result = {
        "schema": "n11-dual-tight-run-resume-manifest-v1",
        "class_key": summary.get("class_key"),
        "full_targets": {"path": rel(args.full_targets), "sha256": sha256(args.full_targets),
                         "count": len(full_keys)},
        "checkpoint": {"path": rel(args.checkpoint_summary), "sha256": sha256(args.checkpoint_summary)},
        "prior_schedule": {"path": rel(args.schedule_manifest), "sha256": sha256(args.schedule_manifest)},
        "current_cache": {"path": cache_paths[0], "sha256": scheduled_source_hashes[cache_paths[0]]},
        "resume_targets": {"path": rel(args.out_targets), "sha256": sha256(args.out_targets),
                           "count": len(resume_keys), "keys": [list(key) for key in sorted(resume_keys)]},
        "excluded_completed_exact_or_UNKNOWN": len(completed),
        "failed_without_verdict": [list(key) for key in sorted(failed)],
        "never_dispatched": [list(key) for key in sorted(waiting)],
        "budget_per_target": args.budget, "workers": args.workers,
        "run_dir": args.run_dir,
        "sources": [{"path": rel(path), "sha256": sha256(path)} for path in
                    (args.solver, args.solver_source, args.runner, Path(__file__).resolve())],
        "selection_rule": "resume only keys with no completed replay row; do not rerun exact or completed UNKNOWN rows",
        "solver_command": f"{rel(args.runner)} --solver {rel(args.solver)} --targets {rel(args.out_targets)} --cache {cache_paths[0]} --out-dir {args.run_dir} --workers {args.workers} --budget {args.budget}",
        "claim": "The failed target has no solver verdict; saved exact and UNKNOWN rows are excluded from this resume input.",
    }
    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")
    print(json.dumps({"resume_count": len(resume_keys), "failed": len(failed),
                      "never_dispatched": len(waiting), "out_targets": rel(args.out_targets)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

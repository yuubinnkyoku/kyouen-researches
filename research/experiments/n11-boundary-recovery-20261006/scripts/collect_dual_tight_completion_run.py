#!/usr/bin/env python3
"""Collect exact, UNKNOWN, interrupted, failed, and undispatched s5 run states."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scheduled-targets", type=Path, required=True)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--schedule-manifest", type=Path, required=True)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--solver-source", type=Path, required=True)
    ap.add_argument("--runner", type=Path, required=True)
    ap.add_argument("--raw-all-out", type=Path, required=True)
    ap.add_argument("--raw-exact-out", type=Path, required=True)
    ap.add_argument("--exact-targets-out", type=Path, required=True)
    ap.add_argument("--exact-cache-out", type=Path, required=True)
    ap.add_argument("--summary-out", type=Path, required=True)
    ap.add_argument("--manifest-out", type=Path, required=True)
    ap.add_argument("--aux-dir", type=Path, required=True,
                    help="destination for preserved partial outputs and failed-attempt logs")
    ap.add_argument("--budget", type=int, default=15_000_000)
    args = ap.parse_args()

    outputs = [args.raw_all_out, args.raw_exact_out, args.exact_targets_out,
               args.exact_cache_out, args.summary_out, args.manifest_out]
    if any(path.exists() for path in outputs):
        raise SystemExit("refusing to overwrite an existing collection artifact")
    schedule = json.loads(args.schedule_manifest.read_text(encoding="utf-8"))
    if schedule.get("probe_target_sha256") != sha256(args.scheduled_targets):
        raise SystemExit("schedule manifest does not bind scheduled targets")
    if schedule.get("budget_per_target") != args.budget:
        raise SystemExit("schedule and collector budgets disagree")
    source_hashes = {item["path"]: item["sha256"] for item in schedule.get("sources", [])}
    for path in (args.solver, args.solver_source, args.runner):
        if source_hashes.get(rel(path)) != sha256(path):
            raise SystemExit(f"schedule source hash mismatch: {rel(path)}")

    targets: dict[tuple[int, int], list[str]] = {}
    for line_no, row in enumerate(csv.reader(args.scheduled_targets.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 11 or row[0] not in ("reply27-dual-tight", "reply27-dual-tight-repair") \
                or int(row[2]) != 5 or int(row[7]) != 0:
            raise SystemExit(f"invalid scheduled s5 target at {line_no}: {row}")
        key = (int(row[3]), int(row[4]))
        if key in targets:
            raise SystemExit(f"duplicate scheduled target: {key}")
        targets[key] = row
    if not targets:
        raise SystemExit("empty scheduled target set")

    args.aux_dir.mkdir(parents=True, exist_ok=True)
    raw_all: list[list[str]] = []
    raw_exact: list[list[str]] = []
    exact_targets: list[list[str]] = []
    exact_cache: dict[tuple[int, int], tuple[int, int]] = {}
    rows_by_verdict: Counter[int] = Counter()
    entries = []
    nodes_all = 0
    nodes_exact = 0
    for key, target in targets.items():
        stem = f"s5-{key[0]}-{key[1]}"
        input_path = args.run_dir / f"{stem}.input.csv"
        output_path = args.run_dir / f"{stem}.out.csv"
        partial_path = output_path.with_suffix(output_path.suffix + ".tmp")
        log_path = args.run_dir / f"{stem}.log"
        started = input_path.is_file()
        entry: dict[str, object] = {"key": list(key), "started": started}
        if started:
            input_rows = [row for row in csv.reader(input_path.open(newline="", encoding="utf-8-sig"))
                          if row and not row[0].lstrip().startswith("#")]
            if input_rows != [target]:
                raise SystemExit(f"run input differs from immutable schedule: {key}")
            entry["input"] = {"path": rel(input_path), "bytes": input_path.stat().st_size,
                              "sha256": sha256(input_path)}
        else:
            entry["input"] = None
        if log_path.is_file():
            entry["log"] = {"path": rel(log_path), "bytes": log_path.stat().st_size,
                            "sha256": sha256(log_path)}
        else:
            entry["log"] = None

        if output_path.is_file():
            rows = [row for row in csv.reader(output_path.open(newline="", encoding="utf-8-sig"))
                    if row and not row[0].lstrip().startswith("#")]
            if len(rows) != 1:
                raise SystemExit(f"expected one completed replay row for {key}: {output_path}")
            row = rows[0]
            if (len(row) != 11 or row[0] != "replay" or int(row[2]) != 5 or int(row[4]) != 0
                    or int(row[3]) != int(target[5]) or int(row[5]) != args.budget
                    or (int(row[9]), int(row[10])) != key or int(row[6]) not in (0, 1, 2)
                    or int(row[7]) < 0):
                raise SystemExit(f"invalid completed replay row for {key}: {row}")
            verdict, nodes = int(row[6]), int(row[7])
            raw_all.append(row)
            rows_by_verdict[verdict] += 1
            nodes_all += nodes
            entry.update(status={0: "completed_UNKNOWN", 1: "exact_WIN", 2: "exact_LOSS"}[verdict],
                         output={"path": rel(output_path), "bytes": output_path.stat().st_size,
                                 "sha256": sha256(output_path), "verdict": verdict, "nodes": nodes})
            if verdict in (1, 2):
                raw_exact.append(row)
                exact_targets.append(target)
                exact_cache[key] = (verdict, nodes)
                nodes_exact += nodes
        elif partial_path.is_file():
            if not started:
                raise SystemExit(f"partial output exists without dispatched input: {key}")
            copied = args.aux_dir / f"{stem}.partial.csv"
            if copied.exists():
                raise SystemExit(f"refusing to overwrite preserved partial: {copied}")
            shutil.copyfile(partial_path, copied)
            entry.update(status="interrupted_partial", partial={
                "source_path": rel(partial_path), "source_sha256": sha256(partial_path),
                "path": rel(copied), "sha256": sha256(copied), "bytes": copied.stat().st_size})
        elif started:
            preserved_log = None
            if log_path.is_file():
                preserved_log = args.aux_dir / f"{stem}.failed-attempt.log"
                if preserved_log.exists():
                    raise SystemExit(f"refusing to overwrite preserved failure log: {preserved_log}")
                shutil.copyfile(log_path, preserved_log)
                preserved_log = {"source_path": rel(log_path), "source_sha256": sha256(log_path),
                                 "path": rel(preserved_log), "sha256": sha256(preserved_log),
                                 "bytes": preserved_log.stat().st_size}
            entry.update(status="started_no_result", preserved_failure_log=preserved_log)
        else:
            entry["status"] = "not_dispatched"
        entries.append(entry)

    def write_rows(path: Path, rows: list[list[str]], header: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as stream:
            stream.write(header + "\n")
            csv.writer(stream, lineterminator="\n").writerows(rows)

    write_rows(args.raw_all_out, raw_all,
               "# completed replay rows; exact and UNKNOWN rows retained; source hashes in manifest")
    write_rows(args.raw_exact_out, raw_exact,
               "# completed exact replay rows only; UNKNOWN and missing rows are excluded")
    write_rows(args.exact_targets_out, exact_targets,
               "# completed exact target subset only; UNKNOWN and missing targets are excluded")
    args.exact_cache_out.parent.mkdir(parents=True, exist_ok=True)
    with args.exact_cache_out.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# s5 verdict cache: n=11 schema=1 (exact completed replay rows only)\n")
        for (lo, hi), (verdict, nodes) in sorted(exact_cache.items()):
            stream.write(f"s5verdict,{lo},{hi},5,{verdict},{nodes}\n")

    counts = Counter(str(entry["status"]) for entry in entries)
    runner_summary_path = args.run_dir / "summary.json"
    result = {
        "schema": "n11-dual-tight-completion-run-collection-v1",
        "class_key": schedule.get("class_key"),
        "scheduled": len(targets), "started": sum(bool(entry["started"]) for entry in entries),
        "completed_rows": len(raw_all), "exact_rows": len(raw_exact),
        "verdict_counts": {"WIN": rows_by_verdict[1], "LOSS": rows_by_verdict[2],
                           "UNKNOWN": rows_by_verdict[0]},
        "status_counts": dict(sorted(counts.items())),
        "nodes_all_completed_rows": nodes_all, "nodes_exact": nodes_exact,
        "exact_win_witnesses": [list(key) for key, (value, _) in sorted(exact_cache.items()) if value == 1],
        "unknown_keys": [entry["key"] for entry in entries if entry["status"] == "completed_UNKNOWN"],
        "failed_no_result_keys": [entry["key"] for entry in entries if entry["status"] == "started_no_result"],
        "interrupted_partial_keys": [entry["key"] for entry in entries if entry["status"] == "interrupted_partial"],
        "not_dispatched_keys": [entry["key"] for entry in entries if entry["status"] == "not_dispatched"],
        "runner_summary": ({"path": rel(runner_summary_path), "sha256": sha256(runner_summary_path)}
                           if runner_summary_path.is_file() else None),
        "targets": {"path": rel(args.scheduled_targets), "sha256": sha256(args.scheduled_targets)},
        "target_statuses": entries,
    }
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8", newline="\n")
    source_inputs = [args.scheduled_targets, args.schedule_manifest, args.solver,
                     args.solver_source, args.runner, Path(__file__).resolve()]
    outputs = [args.raw_all_out, args.raw_exact_out, args.exact_targets_out,
               args.exact_cache_out, args.summary_out]
    manifest = {
        "schema": "n11-dual-tight-completion-run-manifest-v1",
        "schedule_manifest": {"path": rel(args.schedule_manifest), "sha256": sha256(args.schedule_manifest)},
        "source_inputs": [{"path": rel(path), "sha256": sha256(path), "bytes": path.stat().st_size}
                          for path in source_inputs],
        "outputs": [{"path": rel(path), "sha256": sha256(path), "bytes": path.stat().st_size}
                    for path in outputs],
        "summary": result,
        "claim": "Only completed solver rows carry verdicts; failed, interrupted, undispatched, and UNKNOWN states remain unresolved.",
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")
    print(json.dumps({"scheduled": len(targets), "completed": len(raw_all),
                      "verdicts": result["verdict_counts"], "status_counts": counts,
                      "unknown": result["unknown_keys"],
                      "failed": result["failed_no_result_keys"],
                      "not_dispatched": len(result["not_dispatched_keys"]),
                      "nodes_exact": nodes_exact}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

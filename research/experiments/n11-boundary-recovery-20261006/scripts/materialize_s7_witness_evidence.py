#!/usr/bin/env python3
"""Preserve and hash-bind completed exact s7 LOSS-witness replay outputs."""
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
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return [row for row in csv.reader(stream)
                if row and not row[0].lstrip().startswith("#")]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-summary", type=Path, required=True)
    ap.add_argument("--targets", type=Path, required=True)
    ap.add_argument("--preflight", type=Path, required=True)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--dispatch-main-commit", required=True)
    ap.add_argument("--raw-dir", type=Path, required=True)
    ap.add_argument("--out-prefix", type=Path, required=True)
    args = ap.parse_args()

    suffixes = ("-inputs.csv", "-raw.csv", "-exact-s7.cache", "-runner-summary.json",
                "-sources.json", "-summary.json")
    outputs = {suffix: args.out_prefix.with_name(args.out_prefix.name + suffix)
               for suffix in suffixes}
    if not args.run_summary.is_file() or not args.targets.is_file() or not args.preflight.is_file():
        raise SystemExit("run summary, target CSV, or preflight is missing")
    if not args.solver.is_file() or args.raw_dir.exists() or any(p.exists() for p in outputs.values()):
        raise SystemExit("solver missing or refusing to overwrite existing evidence")

    run = json.loads(args.run_summary.read_text(encoding="utf-8"))
    preflight = json.loads(args.preflight.read_text(encoding="utf-8"))
    if (run.get("schema") != "n11-s7-witness-probe-local-run-v1"
            or run.get("preflight", {}).get("sha256") != sha256(args.preflight)
            or run.get("targets", {}).get("sha256") != sha256(args.targets)
            or run.get("solver", {}).get("sha256") != sha256(args.solver)
            or run.get("s5_outcome_from_complete_s6_boundary") != "WIN"
            or run.get("s6_child_outcomes") != {"WIN": 90, "LOSS": 0, "UNKNOWN": 0}
            or run.get("s7_probe_verdict_counts") != {"2": 2}
            or run.get("s7_probe_rows") != 2
            or run.get("budget_per_target") != preflight.get("inputs", {}).get("budget_for_proposed_probe")):
        raise SystemExit("local runner summary does not bind a two-row exact s7 LOSS witness run")
    if preflight.get("inputs", {}).get("scan_s7_replay_rows_in_target_boundaries") != 0:
        raise SystemExit("preflight does not prove an empty saved s7 boundary intersection")

    target_rows = rows(args.targets)
    targets_by_key: dict[tuple[int, int], list[str]] = {}
    for row in target_rows:
        if len(row) != 11 or row[0] != "target" or int(row[2]) != 7 or int(row[7]) != 0:
            raise SystemExit(f"invalid canonical s7 target row: {row}")
        key = (int(row[3]), int(row[4]))
        if key in targets_by_key:
            raise SystemExit(f"duplicate s7 target: {key}")
        targets_by_key[key] = row
    selected = {tuple(item["key"]): {tuple(p) for p in item["affected_s6_parents"]}
                for item in preflight.get("schedule", {}).get("selected_targets", [])}
    if set(targets_by_key) != set(selected) or len(targets_by_key) != 2:
        raise SystemExit("target rows differ from the exact two-key preflight schedule")

    run_sources = run.get("new_sources", [])
    if {tuple(item.get("key", [])) for item in run_sources} != set(targets_by_key):
        raise SystemExit("runner raw source keys do not exactly cover the scheduled targets")
    args.raw_dir.mkdir(parents=True, exist_ok=False)
    raw_rows: list[list[str]] = []
    input_rows: list[list[str]] = []
    manifest_sources = []
    verdict_counts: Counter[int] = Counter()
    nodes_total = 0
    for item in sorted(run_sources, key=lambda x: tuple(x["key"])):
        key = tuple(item["key"])
        input_source = Path(item["input_path"])
        raw_source = Path(item["raw_output_path"])
        log_source = Path(item["log_path"])
        for path, expected in ((input_source, item.get("input_sha256")),
                               (raw_source, item.get("raw_output_sha256")),
                               (log_source, item.get("log_sha256"))):
            if not path.is_file() or sha256(path) != expected:
                raise SystemExit(f"local S7 file missing or hash mismatch: {path}")
        input_rows_for_target = rows(input_source)
        replay_rows_for_target = rows(raw_source)
        target_row = targets_by_key[key]
        if len(input_rows_for_target) != 1 or input_rows_for_target[0] != target_row:
            raise SystemExit(f"local solver input differs from scheduled target: {key}")
        if len(replay_rows_for_target) != 1:
            raise SystemExit(f"expected one raw solver replay row for {key}")
        replay = replay_rows_for_target[0]
        if (len(replay) != 11 or replay[0] != "replay" or int(replay[2]) != 7
                or int(replay[3]) != int(target_row[5]) or int(replay[4]) != 0
                or int(replay[5]) != run["budget_per_target"] or int(replay[6]) != 2
                or int(replay[7]) != item.get("nodes")
                or (int(replay[9]), int(replay[10])) != key
                or item.get("verdict") != 2 or item.get("legal") != int(target_row[5])
                or {tuple(p) for p in item.get("affected_s6_parents", [])} != selected[key]):
            raise SystemExit(f"raw exact S7 LOSS row differs from the preflight target: {key}")

        copied = {}
        for role, source in (("input", input_source), ("raw", raw_source), ("log", log_source)):
            extension = ".txt" if role == "log" else ".csv"
            destination = args.raw_dir / f"s7-{key[0]}-{key[1]}.{role}{extension}"
            shutil.copyfile(source, destination)
            if sha256(destination) != sha256(source):
                raise SystemExit(f"byte-preserving S7 copy hash mismatch: {key} {role}")
            copied[role] = {"path": rel(destination), "sha256": sha256(destination),
                            "bytes": destination.stat().st_size,
                            "local_path": rel(source), "local_sha256": sha256(source)}
        raw_rows.append(replay)
        input_rows.append(input_rows_for_target[0])
        verdict_counts[int(replay[6])] += 1
        nodes_total += int(replay[7])
        manifest_sources.append({
            "artifact_path": copied["raw"]["path"], "sha256": copied["raw"]["sha256"],
            "bytes": copied["raw"]["bytes"], "key": list(key), "legal": int(target_row[5]),
            "budget": run["budget_per_target"], "verdict": int(replay[6]), "nodes": int(replay[7]),
            "affected_s6_parents": [list(p) for p in sorted(selected[key])], "replay_rows": 1,
            "input": copied["input"], "log": copied["log"],
        })

    raw_rows.sort(key=lambda row: (int(row[9]), int(row[10])))
    input_rows.sort(key=lambda row: (int(row[3]), int(row[4])))
    outputs["-inputs.csv"].write_text(
        "# Exact canonical s7 solver targets selected by the saved-history preflight.\n"
        + "".join(",".join(row) + "\n" for row in input_rows), encoding="utf-8", newline="\n")
    outputs["-raw.csv"].write_text(
        "# Exact solver replay rows; both are exact LOSS witnesses for their listed safe s6 parents.\n"
        + "".join(",".join(row) + "\n" for row in raw_rows), encoding="utf-8", newline="\n")
    outputs["-exact-s7.cache"].write_text(
        "# exact s7 verdict cache: n=11 schema=1 (new exact LOSS witness rows only)\n"
        + "".join(f"s7verdict,{row[9]},{row[10]},7,2,{row[7]}\n" for row in raw_rows),
        encoding="utf-8", newline="\n")
    shutil.copyfile(args.run_summary, outputs["-runner-summary.json"])

    manifest = {
        "schema": "n11-s7-witness-source-manifest-v1",
        "scope": "exact s7 raw outputs copied byte-for-byte from preserved .local; each exact LOSS is a witness for its affected s6 OR parent",
        "dispatch_main_commit": args.dispatch_main_commit,
        "budget_per_target": run["budget_per_target"], "worker_count": 1,
        "solver": {"path": rel(args.solver), "sha256": sha256(args.solver)},
        "materializer": {"path": rel(Path(__file__)), "sha256": sha256(Path(__file__))},
        "runner": run.get("runner"), "preflight": {"path": rel(args.preflight), "sha256": sha256(args.preflight)},
        "targets": {"path": rel(args.targets), "sha256": sha256(args.targets)},
        "s5_s6_boundary_full_gzip": run.get("s5_s6_boundary_full_gzip"),
        "local_run_dir": run.get("out_dir"),
        "runner_summary": {"path": rel(outputs["-runner-summary.json"]),
                           "sha256": sha256(outputs["-runner-summary.json"]),
                           "reported_s5_outcome": run["s5_outcome_from_complete_s6_boundary"],
                           "reported_s6_counts": run["s6_child_outcomes"]},
        "input_artifact": {"path": rel(outputs["-inputs.csv"]), "sha256": sha256(outputs["-inputs.csv"]),
                           "rows": len(input_rows)},
        "raw_aggregate": {"path": rel(outputs["-raw.csv"]), "sha256": sha256(outputs["-raw.csv"]),
                          "rows": len(raw_rows)},
        "exact_s7_cache": {"path": rel(outputs["-exact-s7.cache"],),
                            "sha256": sha256(outputs["-exact-s7.cache"]), "rows": len(raw_rows)},
        "raw_sources": manifest_sources, "source_replay_rows": len(manifest_sources),
        "verdict_counts": {str(code): verdict_counts[code] for code in (0, 1, 2) if verdict_counts[code]},
        "nodes": nodes_total, "exact_conflicts": 0, "unknowns_propagated": False,
    }
    outputs["-sources.json"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                        encoding="utf-8", newline="\n")
    summary = {
        "schema": "n11-s7-witness-evidence-summary-v1", "dispatch_main_commit": args.dispatch_main_commit,
        "s5_parent": run["s5_parent"], "s5_outcome": run["s5_outcome_from_complete_s6_boundary"],
        "complete_s6_boundary": run["s5_boundary_s6_count"], "s6_status_counts": run["s6_child_outcomes"],
        "s7_targets": len(raw_rows), "s7_verdict_counts": manifest["verdict_counts"],
        "nodes": nodes_total, "conflicts": 0, "unknowns_propagated": False,
        "raw_directory": {"path": rel(args.raw_dir), "files": 3 * len(raw_rows)},
        "artifacts": {suffix: {"path": rel(path), "sha256": sha256(path)}
                      for suffix, path in outputs.items() if suffix != "-summary.json"},
        "source_manifest_sha256": sha256(outputs["-sources.json"]),
    }
    outputs["-summary.json"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                                        encoding="utf-8", newline="\n")
    print(json.dumps({"s7_rows": len(raw_rows), "verdicts": manifest["verdict_counts"],
                      "nodes": nodes_total, "conflicts": 0,
                      "manifest_sha256": sha256(outputs["-sources.json"]),
                      "summary_sha256": sha256(outputs["-summary.json"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

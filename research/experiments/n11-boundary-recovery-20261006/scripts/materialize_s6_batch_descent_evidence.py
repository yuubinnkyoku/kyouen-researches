#!/usr/bin/env python3
"""Validate and preserve a completed multi-parent s5-to-s6 descent batch."""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402
sys.path.insert(0, str(EXP / "scripts"))
from audit_local_s6_boundary_history import check_full_detail, make_boundary  # noqa: E402
from audit_saved_s6_targets import points, read_saved_exact_s6, safe_canonical, sha256  # noqa: E402


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def data_rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return [row for row in csv.reader(stream)
                if row and not row[0].lstrip().startswith("#")]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parents", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--saved-audit", type=Path, required=True)
    parser.add_argument("--saved-full-detail", type=Path, required=True)
    parser.add_argument("--s5-cache", type=Path, required=True)
    parser.add_argument("--history-preflight", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--dispatch-main-commit", required=True)
    parser.add_argument("--budget", type=int, required=True)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--out-prefix", type=Path, required=True)
    args = parser.parse_args()

    suffixes = ("-inputs.csv", "-raw-all.csv", "-raw-exact.csv", "-exact-s6.cache",
                "-derived-s5.cache", "-runner-summary.json", "-sources.json", "-summary.json")
    outputs = {suffix: args.out_prefix.with_name(args.out_prefix.name + suffix)
               for suffix in suffixes}
    if args.budget <= 0:
        parser.error("--budget must be positive")
    if not args.solver.is_file() or not args.run_dir.is_dir():
        raise SystemExit("solver or completed local run directory is missing")
    if args.raw_dir.exists() or any(path.exists() for path in outputs.values()):
        raise SystemExit("refusing to overwrite an existing evidence artifact")

    history = json.loads(args.history_preflight.read_text(encoding="utf-8"))
    if (history.get("dispatch_main_commit") != args.dispatch_main_commit
            or history.get("budget") != args.budget
            or history.get("parent_targets", {}).get("sha256") != sha256(args.parents)
            or history.get("saved_source_audit", {}).get("sha256") != sha256(args.saved_audit)
            or history.get("saved_full_detail", {}).get("sha256") != sha256(args.saved_full_detail)
            or history.get("s5_cache", {}).get("sha256") != sha256(args.s5_cache)):
        raise SystemExit("S6 history preflight does not bind the dispatch inputs")
    union_summary = history.get("union", {})
    if (union_summary.get("same_or_higher_budget_unknown_keys") != 0
            or union_summary.get("conflicts") != 0):
        raise SystemExit("S6 history preflight contains a blocked key or conflict")

    parent_rows = data_rows(args.parents)
    parent_keys: list[tuple[int, int]] = []
    parent_boundaries: dict[tuple[int, int], set[tuple[int, int]]] = {}
    parent_incidence_count = 0
    for row in parent_rows:
        if len(row) != 11 or int(row[2]) != 5 or int(row[6]) != 0 or int(row[7]) != 0:
            raise SystemExit(f"invalid exact-UNKNOWN s5 AND parent row: {row}")
        parent = (int(row[3]), int(row[4]))
        if parent in parent_boundaries or not safe_canonical(parent, 5):
            raise SystemExit(f"unsafe, noncanonical, or duplicate s5 parent: {parent}")
        parent_points = set(points(parent))
        boundary = make_boundary(parent)
        if int(row[5]) != len(legal_after(parent_points)) or not boundary:
            raise SystemExit(f"s5 parent legal-count/boundary mismatch: {parent}")
        check_full_detail(args.saved_full_detail, parent, boundary)
        parent_keys.append(parent)
        parent_boundaries[parent] = boundary
        parent_incidence_count += len(boundary)
    if len(parent_keys) != 4:
        raise SystemExit(f"expected the four audited UNKNOWN s5 parents, got {len(parent_keys)}")

    audit_by_parent = {}
    for item in history.get("per_parent_history_audits", []):
        audit_path = ROOT / item["path"]
        if not audit_path.is_file() or sha256(audit_path) != item.get("sha256"):
            raise SystemExit(f"S6 per-parent history audit hash mismatch: {item.get('path')}")
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        parent = tuple(audit.get("parent", {}).get("key", []))
        if (parent not in parent_boundaries or parent in audit_by_parent
                or audit.get("requested_budget") != args.budget
                or audit.get("conflicts") != 0
                or audit.get("same_or_higher_budget_unknown_keys")):
            raise SystemExit(f"invalid or incomplete per-parent history audit: {item.get('path')}")
        audit_by_parent[parent] = audit
    if set(audit_by_parent) != set(parent_keys):
        raise SystemExit("per-parent history audits do not cover the exact S6 parent set")

    union = set().union(*parent_boundaries.values())
    if (len(union) != union_summary.get("unique_canonical_s6_keys")
            or parent_incidence_count != sum(item["boundary_child_count"]
                                             for item in history["per_parent_history_audits"])):
        raise SystemExit("S6 history preflight and rebuilt canonical geometry disagree")
    saved_audit_doc = json.loads(args.saved_audit.read_text(encoding="utf-8"))
    saved, source_reports = read_saved_exact_s6(saved_audit_doc)
    saved_counts = Counter(
        {None: "UNSEEN", 0: "UNKNOWN", 1: "WIN", 2: "LOSS"}[saved.get(key, {}).get("verdict")
          if key in saved else None]
        for key in union
    )
    if dict(sorted(saved_counts.items())) != union_summary.get("saved_status_counts"):
        raise SystemExit("saved s6 source intersection differs from pre-dispatch history audit")

    runner_summary_path = args.run_dir / "summary.json"
    runner = json.loads(runner_summary_path.read_text(encoding="utf-8"))
    if (runner.get("parent_count") != len(parent_keys)
            or runner.get("boundary_canonical_s6_count") != len(union)
            or runner.get("parent_child_relations") != parent_incidence_count
            or runner.get("budget") != args.budget
            or runner.get("retry_saved_unknown") is not False
            or runner.get("new_solver_rows") != len(runner.get("new_solver_sources", []))
            or runner.get("new_solver_unknown", 0) + runner.get("new_solver_exact", 0)
            != runner.get("new_solver_rows")):
        raise SystemExit("local S6 runner summary does not bind the completed batch")

    local_sources: dict[tuple[int, int], dict] = {}
    for item in runner.get("new_solver_sources", []):
        key = tuple(item.get("key", []))
        output = Path(item.get("path", ""))
        if key not in union or key in local_sources or key in saved:
            raise SystemExit(f"unexpected, duplicated, or previously saved S6 dispatch: {key}")
        if not output.is_file() or sha256(output) != item.get("sha256"):
            raise SystemExit(f"local S6 output missing or hash mismatch: {output}")
        input_path = output.with_name(output.name.replace(".out.csv", ".input.csv"))
        log_path = output.with_name(output.name.replace(".out.csv", ".log"))
        inputs, replays = data_rows(input_path), data_rows(output)
        if len(inputs) != 1 or len(replays) != 1:
            raise SystemExit(f"expected one S6 input/output row: {key}")
        input_row, replay = inputs[0], replays[0]
        points_for_key = points(key)
        legal = len(legal_after(set(points_for_key)))
        if (len(input_row) != 11 or input_row[0] != "target" or int(input_row[2]) != 6
                or int(input_row[5]) != legal or int(input_row[7]) != 1
                or (int(input_row[3]), int(input_row[4])) != key
                or not safe_canonical(key, 6)):
            raise SystemExit(f"invalid S6 input geometry: {key}")
        if (len(replay) != 11 or replay[0] != "replay" or int(replay[2]) != 6
                or int(replay[3]) != legal or int(replay[4]) != 1
                or int(replay[5]) != args.budget or (int(replay[9]), int(replay[10])) != key):
            raise SystemExit(f"invalid S6 replay row: {key}: {replay}")
        verdict, nodes = int(replay[6]), int(replay[7])
        if (verdict not in (0, 1, 2) or nodes < 0
                or item.get("verdict") != verdict or item.get("nodes") != nodes):
            raise SystemExit(f"S6 replay verdict/nodes mismatch: {key}")
        local_sources[key] = {"input": input_path, "output": output, "log": log_path,
                              "input_row": input_row, "replay_row": replay,
                              "verdict": verdict, "nodes": nodes}

    if len(local_sources) != runner.get("new_solver_rows"):
        raise SystemExit("local S6 raw sources do not cover every runner result")
    new_counts = Counter(source["verdict"] for source in local_sources.values())
    if (new_counts[0] != runner.get("new_solver_unknown")
            or new_counts[1] + new_counts[2] != runner.get("new_solver_exact")
            or sum(source["nodes"] for source in local_sources.values()) != runner.get("nodes_new")):
        raise SystemExit("local S6 raw rows disagree with runner verdict/node totals")

    verdicts = {key: record["verdict"] for key, record in saved.items()}
    for key, source in local_sources.items():
        old, new = verdicts.get(key), source["verdict"]
        if old in (1, 2) and new in (1, 2) and old != new:
            raise SystemExit(f"exact saved/new S6 conflict: {key}")
        if new in (1, 2) or old is None:
            verdicts[key] = new
    parent_outcomes = Counter()
    for row in runner.get("parents", []):
        parent = tuple(row.get("key", []))
        if parent not in parent_boundaries:
            raise SystemExit(f"runner reported an unexpected s5 parent: {parent}")
        children = parent_boundaries[parent]
        values = [verdicts.get(child) for child in children]
        outcome = "LOSS" if 2 in values else (
            "WIN" if all(value == 1 for value in values) else "UNKNOWN")
        child_counts = Counter("0" if value in (None, 0) else str(value) for value in values)
        child_count_map = {str(code): child_counts[str(code)] for code in (0, 1, 2)}
        if outcome != row.get("outcome") or child_count_map != row.get("counts"):
            raise SystemExit(f"S6 AND recurrence differs from runner for parent {parent}")
        parent_outcomes[outcome] += 1
    parent_outcome_counts = {name: parent_outcomes[name] for name in ("LOSS", "UNKNOWN", "WIN")}
    if parent_outcome_counts != runner.get("status_counts"):
        raise SystemExit("runner s5 parent outcome totals are inconsistent")

    local_derived = Path(runner["derived_s5_cache"]["path"])
    if (not local_derived.is_file() or sha256(local_derived) != runner["derived_s5_cache"]["sha256"]
            or runner["derived_s5_cache"]["rows"] != sum(parent_outcomes[x] for x in ("WIN", "LOSS"))):
        raise SystemExit("runner derived-s5 cache differs from the exact boundary outcomes")

    args.raw_dir.mkdir(parents=True, exist_ok=False)
    raw_rows, input_rows, raw_sources = [], [], []
    for key, source in sorted(local_sources.items()):
        copied = args.raw_dir / source["output"].name
        shutil.copyfile(source["output"], copied)
        if sha256(copied) != sha256(source["output"]):
            raise SystemExit(f"byte-preserving raw copy hash mismatch: {key}")
        raw_rows.append(source["replay_row"])
        input_rows.append(source["input_row"])
        raw_sources.append({
            "artifact_path": rel(copied), "sha256": sha256(copied), "bytes": copied.stat().st_size,
            "source_local_path": rel(source["output"]), "source_local_sha256": sha256(source["output"]),
            "input_local_path": rel(source["input"]), "input_local_sha256": sha256(source["input"]),
            "log_local_path": rel(source["log"]) if source["log"].is_file() else None,
            "log_local_sha256": sha256(source["log"]) if source["log"].is_file() else None,
            "key": list(key), "verdict": source["verdict"], "nodes": source["nodes"],
            "replay_rows": 1,
        })
    raw_rows.sort(key=lambda row: (int(row[9]), int(row[10])))
    input_rows.sort(key=lambda row: (int(row[3]), int(row[4])))
    exact_rows = [row for row in raw_rows if int(row[6]) in (1, 2)]
    verdict_counts = Counter(int(row[6]) for row in raw_rows)

    outputs["-inputs.csv"].write_text(
        "# Canonical safe/legal s6 targets from the complete boundaries of the supplied s5 parents.\n"
        + "".join(",".join(row) + "\n" for row in input_rows), encoding="utf-8", newline="\n")
    outputs["-raw-all.csv"].write_text(
        "# All new S6 replay rows; UNKNOWN is preserved and never propagated.\n"
        + "".join(",".join(row) + "\n" for row in raw_rows), encoding="utf-8", newline="\n")
    outputs["-raw-exact.csv"].write_text(
        "# Exact S6 WIN/LOSS replay rows only; UNKNOWN excluded.\n"
        + "".join(",".join(row) + "\n" for row in exact_rows), encoding="utf-8", newline="\n")
    with outputs["-exact-s6.cache"].open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("# exact s6 verdict cache: n=11 schema=1 (new exact replay rows only; UNKNOWN excluded)\n")
        for row in exact_rows:
            stream.write(f"s6verdict,{row[9]},{row[10]},6,{row[6]},{row[7]}\n")
    shutil.copyfile(local_derived, outputs["-derived-s5.cache"])
    shutil.copyfile(runner_summary_path, outputs["-runner-summary.json"])

    manifest = {
        "schema": "n11-dual-tight-s6-descent-source-manifest-v1",
        "dispatch_main_commit": args.dispatch_main_commit,
        "budget_per_target": args.budget,
        "worker_count": runner.get("workers"),
        "solver": {"path": rel(args.solver), "sha256": sha256(args.solver)},
        "runner": {"path": rel(args.runner), "sha256": sha256(args.runner)},
        "materializer": {"path": rel(Path(__file__)), "sha256": sha256(Path(__file__))},
        "local_run_dir": rel(args.run_dir),
        "parents": {"path": rel(args.parents), "sha256": sha256(args.parents),
                    "keys": [list(key) for key in parent_keys]},
        "saved_source_audit": {"path": rel(args.saved_audit), "sha256": sha256(args.saved_audit),
                               "source_count": len(source_reports)},
        "saved_full_boundary_detail": {"path": rel(args.saved_full_detail),
                                       "sha256": sha256(args.saved_full_detail),
                                       "parent_count": len(parent_keys)},
        "history_preflight": {"path": rel(args.history_preflight),
                              "sha256": sha256(args.history_preflight),
                              "unique_boundary_s6": len(union),
                              "dispatch_ready": union_summary["dispatch_ready_unique_keys"],
                              "blocked_unknown": 0},
        "s5_cache": {"path": rel(args.s5_cache), "sha256": sha256(args.s5_cache)},
        "runner_summary": {"path": rel(outputs["-runner-summary.json"]),
                           "sha256": sha256(outputs["-runner-summary.json"]),
                           "parent_outcomes": runner.get("status_counts")},
        "input_artifact": {"path": rel(outputs["-inputs.csv"]),
                           "sha256": sha256(outputs["-inputs.csv"]), "rows": len(input_rows)},
        "raw_aggregate": {"path": rel(outputs["-raw-all.csv"]),
                          "sha256": sha256(outputs["-raw-all.csv"]), "rows": len(raw_rows)},
        "exact_s6_cache": {"path": rel(outputs["-exact-s6.cache"]),
                           "sha256": sha256(outputs["-exact-s6.cache"]), "rows": len(exact_rows)},
        "derived_s5_cache": {"path": rel(outputs["-derived-s5.cache"],),
                             "sha256": sha256(outputs["-derived-s5.cache"]),
                             "rows": runner["derived_s5_cache"]["rows"]},
        "raw_sources": raw_sources,
        "source_replay_rows": len(raw_sources),
        "verdict_counts": {"WIN": verdict_counts[1], "LOSS": verdict_counts[2],
                           "UNKNOWN": verdict_counts[0]},
        "exact_conflicts": 0,
        "unknowns_propagated": False,
    }
    outputs["-sources.json"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                        encoding="utf-8", newline="\n")
    summary = {
        "schema": "n11-reply27-s6-batch-descent-evidence-summary-v1",
        "dispatch_main_commit": args.dispatch_main_commit,
        "root": [60, 27],
        "parent_keys": [list(key) for key in parent_keys],
        "parent_count": len(parent_keys),
        "complete_canonical_s6_union": len(union),
        "parent_child_incidences": parent_incidence_count,
        "saved_s6_boundary_counts": dict(sorted(saved_counts.items())),
        "new_s6_rows": len(raw_rows),
        "new_s6_verdict_counts": {"WIN": verdict_counts[1], "LOSS": verdict_counts[2],
                                  "UNKNOWN": verdict_counts[0]},
        "total_boundary_verdict_counts": {
            "WIN": saved_counts["WIN"] + verdict_counts[1],
            "LOSS": saved_counts["LOSS"] + verdict_counts[2],
            "UNKNOWN": saved_counts["UNKNOWN"] + verdict_counts[0],
        },
        "nodes": sum(int(row[7]) for row in raw_rows),
        "budget_per_target": args.budget,
        "workers": runner.get("workers"),
        "s5_parent_outcomes": runner.get("status_counts"),
        "derived_s5_rows": runner["derived_s5_cache"]["rows"],
        "new_exact_s6_loss_for_reverse_propagation": verdict_counts[2],
        "reverse_propagated_s5_loss": 0,
        "conflicts": 0,
        "unknowns_propagated": False,
        "outputs": {suffix: rel(path) for suffix, path in outputs.items()},
        "raw_directory": {"path": rel(args.raw_dir), "files": len(raw_sources)},
        "source_manifest_sha256": sha256(outputs["-sources.json"]),
    }
    outputs["-summary.json"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                                        encoding="utf-8", newline="\n")
    print(json.dumps({
        "parent_count": len(parent_keys), "boundary_s6": len(union),
        "parent_child_incidences": parent_incidence_count,
        "saved_s6": dict(saved_counts), "new_s6": summary["new_s6_verdict_counts"],
        "total_boundary": summary["total_boundary_verdict_counts"], "nodes": summary["nodes"],
        "s5_outcomes": runner.get("status_counts"), "conflicts": 0,
        "raw_sources": len(raw_sources), "manifest_sha256": sha256(outputs["-sources.json"]),
        "summary_sha256": sha256(outputs["-summary.json"]),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

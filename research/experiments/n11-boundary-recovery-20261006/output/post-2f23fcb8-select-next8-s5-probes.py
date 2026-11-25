#!/usr/bin/env python3
"""Select the next low-legal-count S5 probes from a current strict audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all-targets", type=Path, required=True)
    ap.add_argument("--raw-audit", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--count", type=int, default=8)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--solver-source", type=Path, required=True)
    ap.add_argument("--runner", type=Path, required=True)
    ap.add_argument("--targets-out", type=Path, required=True)
    ap.add_argument("--manifest-out", type=Path, required=True)
    args = ap.parse_args()
    if args.count < 1:
        raise SystemExit("count must be positive")

    audit = json.loads(args.raw_audit.read_text(encoding="utf-8"))
    if audit["targets"]["sha256"] != sha256(args.all_targets):
        raise SystemExit("raw-history audit is for a different target CSV")
    if audit["current_cache"]["sha256"] != sha256(args.cache):
        raise SystemExit("raw-history audit is for a different exact cache")
    if audit["exact_verdict_conflicts"] or audit["prior_unknown_same_budget_or_higher"]:
        raise SystemExit("raw-history audit has a conflict or same-budget UNKNOWN")

    rows: dict[tuple[int, int], list[str]] = {}
    with args.all_targets.open(newline="", encoding="utf-8-sig") as fp:
        for row in csv.reader(fp):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
                raise SystemExit(f"invalid S5 target row: {row}")
            key = (int(row[3]), int(row[4]))
            if key in rows:
                raise SystemExit(f"duplicate target key: {key}")
            rows[key] = row

    cached: dict[tuple[int, int], int] = {}
    with args.cache.open(newline="", encoding="utf-8-sig") as fp:
        for row in csv.reader(fp):
            if not row or row[0].startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise SystemExit(f"invalid exact cache row: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if verdict not in (1, 2) or key in cached:
                raise SystemExit(f"non-exact or duplicate cache row: {row}")
            cached[key] = verdict

    ready = {tuple(map(int, key)) for key in audit["dispatch_ready_keys"]}
    if not ready <= rows.keys() or ready & cached.keys():
        raise SystemExit("dispatch-ready set disagrees with target geometry or cache")
    selected = sorted(ready, key=lambda key: (int(rows[key][5]), key))[: args.count]
    if len(selected) != min(args.count, len(ready)):
        raise SystemExit("selected target count mismatch")

    args.targets_out.parent.mkdir(parents=True, exist_ok=True)
    with args.targets_out.open("w", newline="", encoding="utf-8") as fp:
        fp.write("# next low-legal-count exact S5 probes; order is scheduling only\n")
        writer = csv.writer(fp, lineterminator="\n")
        for seq, key in enumerate(selected, 1):
            row = list(rows[key])
            row[1] = str(seq)
            writer.writerow(row)

    manifest = {
        "schema": "n11-reply27-next-s5-probe-selection-v1",
        "claim": "scheduling order only; selected keys remain UNKNOWN until exact solver results",
        "selection_rule": "current raw-history dispatch-ready S5 keys ordered by legal move count ascending, then canonical key",
        "budget": audit["requested_budget"],
        "budget_per_target": audit["requested_budget"],
        "count_requested": args.count,
        "probe_count": len(selected),
        "dispatch_ready_count": len(ready),
        "probe_target_sha256": sha256(args.targets_out),
        "probe_targets": [list(key) for key in selected],
        "selected": [
            {"rank": i, "key": list(key), "legal_count": int(rows[key][5])}
            for i, key in enumerate(selected, 1)
        ],
        "sources": [
            {"path": path.resolve().relative_to(ROOT).as_posix(), "sha256": sha256(path)}
            for path in (args.all_targets, args.raw_audit, args.cache, Path(__file__).resolve(),
                         args.solver, args.solver_source, args.runner)
        ],
        "targets_out": {"path": str(args.targets_out), "sha256": sha256(args.targets_out)},
    }
    args.manifest_out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"selected": len(selected), "dispatch_ready": len(ready),
                      "keys": [list(key) for key in selected]}, indent=2))


if __name__ == "__main__":
    main()

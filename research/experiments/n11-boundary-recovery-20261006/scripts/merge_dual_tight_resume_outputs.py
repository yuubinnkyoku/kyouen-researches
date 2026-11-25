#!/usr/bin/env python3
"""Copy only completed resume outputs into a prior partial run directory."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


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


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    return tuple([i for i in range(64) if lo >> i & 1]
                 + [64 + i for i in range(57) if hi >> i & 1])


def safe(key: tuple[int, int]) -> bool:
    pts = points(key)
    return len(pts) == 5 and not has_forbidden_quad(pts) and tuple(d4_canonical_key(pts)) == key


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--resume-targets", type=Path, required=True)
    ap.add_argument("--resume-manifest", type=Path, required=True)
    ap.add_argument("--resume-run-dir", type=Path, required=True)
    ap.add_argument("--primary-run-dir", type=Path, required=True)
    ap.add_argument("--out-manifest", type=Path, required=True)
    ap.add_argument("--budget", type=int, default=15_000_000)
    args = ap.parse_args()
    if args.out_manifest.exists():
        raise SystemExit("refusing to overwrite resume merge manifest")
    resume_manifest = json.loads(args.resume_manifest.read_text(encoding="utf-8"))
    if resume_manifest.get("resume_targets", {}).get("sha256") != sha256(args.resume_targets):
        raise SystemExit("resume manifest does not bind resume target CSV")
    if resume_manifest.get("budget_per_target") != args.budget:
        raise SystemExit("resume manifest budget mismatch")

    targets = {}
    for row in csv.reader(args.resume_targets.open(newline="", encoding="utf-8-sig")):
        if not row or row[0].lstrip().startswith("#"):
            continue
        key = (int(row[3]), int(row[4]))
        if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0 or not safe(key):
            raise SystemExit(f"invalid resume target row: {row}")
        if int(row[5]) != len(legal_after(set(points(key)))) or key in targets:
            raise SystemExit(f"unsafe, wrong-legal-count or duplicate resume target: {key}")
        targets[key] = row
    expected_keys = {tuple(map(int, key)) for key in resume_manifest["resume_targets"]["keys"]}
    if set(targets) != expected_keys:
        raise SystemExit("resume targets differ from the manifest key set")

    copies = []
    for key, target in sorted(targets.items()):
        stem = f"s5-{key[0]}-{key[1]}"
        source_in = args.resume_run_dir / f"{stem}.input.csv"
        source_out = args.resume_run_dir / f"{stem}.out.csv"
        source_log = args.resume_run_dir / f"{stem}.log"
        dest_in = args.primary_run_dir / f"{stem}.input.csv"
        dest_out = args.primary_run_dir / f"{stem}.out.csv"
        dest_log = args.primary_run_dir / f"{stem}.log"
        if not all(p.is_file() for p in (source_in, source_out, source_log)):
            raise SystemExit(f"resume run did not complete key {key}")
        input_rows = [row for row in csv.reader(source_in.open(newline="", encoding="utf-8-sig"))
                      if row and not row[0].lstrip().startswith("#")]
        if input_rows != [target]:
            raise SystemExit(f"resume input mismatch: {key}")
        output_rows = [row for row in csv.reader(source_out.open(newline="", encoding="utf-8-sig"))
                       if row and not row[0].lstrip().startswith("#")]
        if len(output_rows) != 1:
            raise SystemExit(f"resume output row count mismatch: {key}")
        row = output_rows[0]
        if (len(row) != 11 or row[0] != "replay" or int(row[2]) != 5 or int(row[4]) != 0
                or int(row[3]) != int(target[5]) or int(row[5]) != args.budget
                or (int(row[9]), int(row[10])) != key or int(row[6]) not in (0, 1, 2)
                or int(row[7]) < 0):
            raise SystemExit(f"invalid completed resume row {key}: {row}")
        if dest_out.exists():
            raise SystemExit(f"refusing to overwrite a primary completed output: {key}")
        args.primary_run_dir.mkdir(parents=True, exist_ok=True)
        if dest_in.exists():
            if dest_in.read_bytes() != source_in.read_bytes():
                raise SystemExit(f"existing primary input differs for {key}")
        else:
            shutil.copyfile(source_in, dest_in)
        shutil.copyfile(source_out, dest_out)
        kept_log = dest_log.is_file()
        if not kept_log:
            shutil.copyfile(source_log, dest_log)
        copies.append({
            "key": list(key), "verdict": int(row[6]), "nodes": int(row[7]),
            "source_input": {"path": rel(source_in), "sha256": sha256(source_in)},
            "source_output": {"path": rel(source_out), "sha256": sha256(source_out)},
            "source_log": {"path": rel(source_log), "sha256": sha256(source_log)},
            "destination_input": {"path": rel(dest_in), "sha256": sha256(dest_in)},
            "destination_output": {"path": rel(dest_out), "sha256": sha256(dest_out)},
            "destination_log": {"path": rel(dest_log), "sha256": sha256(dest_log),
                                "prior_log_preserved": kept_log},
        })

    result = {
        "schema": "n11-dual-tight-resume-output-merge-v1",
        "resume_targets": {"path": rel(args.resume_targets), "sha256": sha256(args.resume_targets),
                           "count": len(targets)},
        "resume_manifest": {"path": rel(args.resume_manifest), "sha256": sha256(args.resume_manifest)},
        "resume_run_dir": str(args.resume_run_dir.resolve()),
        "primary_run_dir": rel(args.primary_run_dir),
        "budget_per_target": args.budget,
        "copied_completed_rows": len(copies),
        "verdict_counts": {"WIN": sum(row["verdict"] == 1 for row in copies),
                           "LOSS": sum(row["verdict"] == 2 for row in copies),
                           "UNKNOWN": sum(row["verdict"] == 0 for row in copies)},
        "rows": copies,
        "claim": "Completed resume rows only; existing output rows are never overwritten and a prior failed log is kept separately.",
    }
    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")
    print(json.dumps({"copied": len(copies), "verdict_counts": result["verdict_counts"],
                      "out_manifest": rel(args.out_manifest)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

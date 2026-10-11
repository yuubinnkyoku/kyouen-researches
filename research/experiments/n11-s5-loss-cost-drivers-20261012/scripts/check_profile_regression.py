"""Ensure opt-in replay profiling leaves solver outcomes and nodes unchanged."""
from __future__ import annotations

import argparse
import csv
import functools
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board, aggregate  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_output(path: Path) -> tuple[list[dict], list[str]]:
    results, profiles = [], []
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.reader(stream):
            if row and row[0] == "replay":
                if len(row) != 11:
                    raise ValueError(f"malformed replay row: {row}")
                results.append({"sequence": int(row[1]), "stones": int(row[2]),
                    "legal": int(row[3]), "is_or": int(row[4]), "budget": int(row[5]),
                    "verdict": int(row[6]), "nodes": int(row[7]),
                    "lo": int(row[9]), "hi": int(row[10])})
            elif row and row[0].startswith("# exact-profile"):
                profiles.append(",".join(row))
    return results, profiles


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--baseline-solver", type=Path,
                    default=ROOT / ".local/n11-s5-loss-witness-20261012/dfpn.exe")
    ap.add_argument("--out", type=Path, default=EXP / "output/profile-regression-v1")
    args = ap.parse_args()
    solver, baseline, out = args.solver.resolve(), args.baseline_solver.resolve(), args.out.resolve()
    if not solver.is_file() or not baseline.is_file() or out.exists():
        ap.error("new and baseline solvers must exist and output directory must be new")
    board = Board(4)
    @functools.lru_cache(maxsize=None)
    def solve(mask: int) -> int:
        children = board.children(mask)
        if not children:
            return 1 if mask.bit_count() % 2 else 2
        return aggregate(mask.bit_count(), (solve(child) for child in children))
    solve(0)
    pending, seen = [0], set()
    while pending:
        mask = board.canonical(pending.pop())
        if mask in seen:
            continue
        seen.add(mask)
        if mask.bit_count() < 6:
            pending.extend(board.children(mask))
    s6 = sorted(mask for mask in seen if mask.bit_count() == 6)
    fixtures = [next(mask for mask in s6 if solve(mask) == verdict) for verdict in (2, 1)]
    out.mkdir(parents=True)
    replay = out / "fixture-input.csv"
    with replay.open("x", encoding="utf-8", newline="") as stream:
        for sequence, mask in enumerate(fixtures):
            stream.write(",".join(map(str, (f"fixture-{sequence}", sequence, 6,
                mask & ((1 << 64) - 1), mask >> 64, board.legal(mask).bit_count(),
                0, 0, 0, 0, 0))) + "\n")
    runs = []
    outputs = []
    for name, executable, profile in (("baseline", baseline, False),
                                      ("default", solver, False), ("profile", solver, True)):
        raw, log = out / f"{name}-raw.csv", out / f"{name}-solver.log"
        command = [str(executable), "--n=4", "--memo=18", "--exact-order=count",
                   f"--exact-replay={replay}", "--only=6", "--exact-replay-budget=250000",
                   f"--csv={raw}"]
        if profile:
            command.append("--exact-replay-profile")
        started = time.perf_counter()
        with log.open("x", encoding="utf-8") as stream:
            completed = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=False)
        elapsed = time.perf_counter() - started
        if completed.returncode:
            raise RuntimeError(f"profile regression run failed: {command}")
        rows, profile_lines = read_output(raw)
        if len(rows) != 2 or [r["verdict"] for r in rows] != [2, 1]:
            raise ValueError(f"fixture solver verdicts differ from independent result: {rows}")
        if (profile and len([line for line in profile_lines if line.startswith("# exact-profile row=")]) != 2) or (
                not profile and profile_lines):
            raise ValueError(f"profile output presence mismatch for {name}: {profile_lines}")
        if profile and not any("# exact-profile-rank row=0 s6" in line for line in profile_lines):
            raise ValueError(f"rank-level exact profile is missing: {profile_lines}")
        if profile and not any(line.startswith("# exact-profile-child") for line in profile_lines):
            raise ValueError(f"root-child attribution profile is missing: {profile_lines}")
        runs.append({"name": name, "binary_sha256": sha256(executable),
                     "command": command, "elapsed_seconds": elapsed,
                     "rows": rows, "profile_lines": profile_lines,
                     "raw_sha256": sha256(raw), "log_sha256": sha256(log)})
        outputs.append(rows)
    stable_fields = ("sequence", "stones", "legal", "is_or", "budget", "verdict", "nodes", "lo", "hi")
    stable_outputs = [[{key: row[key] for key in stable_fields} for row in rows]
                      for rows in outputs]
    if not (stable_outputs[0] == stable_outputs[1] == stable_outputs[2]):
        raise ValueError("new default/profile path differs from baseline verdicts or node counts")
    result = {
        "schema": "n11-exact-replay-profile-regression-v1",
        "board_size": 4,
        "solver_sha256": sha256(solver), "baseline_solver_sha256": sha256(baseline),
        "fixture_keys": [str(mask) for mask in fixtures],
        "independent_verdicts": [2, 1],
        "runs": runs,
        "assertions": [
            "profile flag is off unless explicitly supplied",
            "profile emits rank-level exact calls/nodes/outcomes and table counters",
            "profile emits each root child's incremental node count and exact result",
            "new default solver matches pre-instrumentation binary outcomes and node counts",
            "profile on/off preserves each fixture's exact outcome and node count",
        ],
    }
    (out / "receipt.json").write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                                       encoding="utf-8")
    print(json.dumps({"receipt": str((out / "receipt.json").relative_to(ROOT)).replace("\\", "/"),
                      "sha256": sha256(out / "receipt.json"), "assertions": result["assertions"]},
                     sort_keys=True))


if __name__ == "__main__":
    main()

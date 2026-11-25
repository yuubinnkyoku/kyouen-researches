"""Check exact replay stops only after an independently known LOSS result."""
from __future__ import annotations

import argparse
import csv
import functools
import hashlib
import json
import subprocess
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board, aggregate  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fixture(board: Board) -> tuple[int, int]:
    @functools.lru_cache(maxsize=None)
    def solve(mask: int) -> int:
        mask = board.canonical(mask)
        children = board.children(mask)
        if not children:
            return 1 if mask.bit_count() % 2 else 2
        return aggregate(mask.bit_count(), (solve(child) for child in children))

    solve(0)
    # Derive all reachable S6 classes independently; the memo's keys are not
    # exposed by functools's public API.
    pending, seen = [0], set()
    while pending:
        mask = board.canonical(pending.pop())
        if mask in seen:
            continue
        seen.add(mask)
        if mask.bit_count() < 6:
            pending.extend(board.children(mask))
    s6 = sorted(mask for mask in seen if mask.bit_count() == 6)
    known = {mask: solve(mask) for mask in s6}
    loss = next(mask for mask in s6 if known[mask] == 2)
    win = next(mask for mask in s6 if known[mask] == 1)
    return loss, win


def read_results(path: Path) -> list[dict]:
    results = []
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.reader(stream):
            if row and row[0] == "replay":
                if len(row) != 11:
                    raise ValueError(f"malformed replay result: {row}")
                results.append({"verdict": int(row[6]), "nodes": int(row[7]),
                                "lo": int(row[9]), "hi": int(row[10])})
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=EXP / "output/stop-on-loss-reproduction-v1")
    args = ap.parse_args()
    solver, out = args.solver.resolve(), args.out.resolve()
    if not solver.is_file() or out.exists():
        ap.error("solver must exist and output must be new")
    board = Board(4)
    loss, win = fixture(board)
    out.mkdir(parents=True)
    incomplete = 0  # the empty 4x4 root needs more than one node for an exact result
    runs = []
    cases = [
        ("full", [loss, win], 250000, False, [2, 1]),
        ("stop-on-loss", [loss, win], 250000, True, [2]),
        ("unknown-then-loss", [incomplete, loss], 1, True, [0, 2]),
    ]
    for name, fixtures, budget, stop, expected in cases:
        case = out / name
        case.mkdir()
        replay, raw, log = case / "input.csv", case / "raw.csv", case / "solver.log"
        with replay.open("x", encoding="utf-8", newline="") as stream:
            for i, mask in enumerate(fixtures):
                stream.write(",".join(map(str, (f"fixture-{i}", i, mask.bit_count(),
                    mask & ((1 << 64) - 1), mask >> 64, board.legal(mask).bit_count(),
                    0, 0, 0, 0, 0))) + "\n")
        command = [str(solver), "--n=4", "--memo=18", "--exact-order=count",
                   f"--exact-replay={replay}", f"--exact-replay-budget={budget}", f"--csv={raw}"]
        if name != "unknown-then-loss":
            command.append("--only=6")
        if stop:
            command.append("--exact-replay-stop-on-loss")
        started = time.perf_counter()
        with log.open("x", encoding="utf-8") as stream:
            proc = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=False)
        wall = time.perf_counter() - started
        if proc.returncode:
            raise RuntimeError(f"fixture solver failed: {command}")
        rows = read_results(raw)
        if [row["verdict"] for row in rows] != expected:
            raise ValueError(f"stop behavior mismatch for {name}: {rows}")
        runs.append({"name": name, "command": command, "rows": rows, "wall_seconds": wall,
                     "input_sha256": sha256(replay), "raw_sha256": sha256(raw),
                     "log_sha256": sha256(log)})
    result = {"schema": "n11-exact-replay-stop-on-loss-regression-v1",
              "board_size": 4, "solver_sha256": sha256(solver),
              "fixture_keys": {"loss_s6": str(loss), "win_s6": str(win), "incomplete_s0": "0"},
              "independent_verdicts": {"loss_s6": 2, "win_s6": 1,
                                        "incomplete_s0": "nonterminal; exact proof cut off at one node"},
              "runs": runs,
              "assertions": ["the same exact replay returns LOSS then WIN without the flag",
                             "stop-on-loss returns only the exact LOSS prefix",
                             "UNKNOWN does not trigger the stop; a later exact LOSS is still processed"]}
    (out / "receipt.json").write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                                      encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

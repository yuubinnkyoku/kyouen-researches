"""Task B (update8): node-budget-extension 10M runs for the two candidates that
the measured eighth-update ranking selects -- 150871 and 144774.

Both are the sole pooled witness of a currently uncovered branch and both are
harmless on WIN (optimistic union delta 0 and +1 respectively).  This is a NEW
run with an expanded node budget (not a re-run of any frozen condition): no 10M
run of these indices exists, and neither index is in the conflict-candidate
pool, so the position is rebuilt from the frozen dependency graph (mask, legal
count and canonical-child count).  Verdicts are saved verbatim; an UNKNOWN row
stays UNKNOWN, is never imputed and is never re-run at this budget.  A SOLVED
row carries a captured terminal proof DAG and goes to terminal-only independent
verification (K0371: no S5 WIN is inferred from a single S6 WIN).
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_profile(csv_path: Path):
    census = {"WIN": 0, "LOSS": 0, "UNKNOWN": 0}
    table = {}
    for line in csv_path.read_text().splitlines():
        if line.startswith("# exact-profile-child "):
            fields = dict(kv.split("=", 1) for kv in line.split()[2:])
            census[fields["verdict"]] = census.get(fields["verdict"], 0) + 1
        elif line.startswith("# exact-profile "):
            table = dict(kv.split("=", 1) for kv in line.split()[2:])
    return census, table


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--solver", type=Path, default=ROOT / "build/kyouen-dfpn-root-adaptive")
    p.add_argument("--budget", type=int, default=10000000)
    p.add_argument("--memo", type=int, default=20)
    p.add_argument("--order", default="count")
    p.add_argument("--prefix", default="update8probe10m")
    p.add_argument("--indices", type=int, nargs="*", default=[150871, 144774])
    args = p.parse_args()
    assert 2000000 < args.budget <= 10000000 and 16 <= args.memo <= 24
    with gzip.open(GRAPH, "rt") as stream:
        g = json.load(stream)
    board = Board(11)
    manifest = EXP / f"output/{args.prefix}-manifest.json"
    binary = args.solver.resolve()
    trace_dir = ROOT / "build/n11-update8-traces"
    trace_dir.mkdir(exist_ok=True)
    if manifest.exists():
        result = json.loads(manifest.read_text())
        assert result["budget"] == args.budget and result["solver_binary_sha256"] == sha(binary)
        done = {r["s5_index"] for r in result["rows"]}
    else:
        result = dict(schema="n11-night-update8-task-b-v1", budget=args.budget, memo_power=args.memo,
                      order=args.order, workers=1, prefix=args.prefix,
                      kind="budget-extension-new-run (selected by measured eighth-update effect)",
                      graph=str(GRAPH.relative_to(ROOT)), graph_sha256=sha(GRAPH),
                      solver_binary_sha256=sha(binary),
                      solver_source_sha256=sha(ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"),
                      rows=[],
                      trust=("completed labels solver-trusted until independent terminal-only verification; "
                             "UNKNOWN is not evidence; NODE_LIMIT rows stay UNKNOWN and are not re-run at this budget"))
        done = set()
    for index in args.indices:
        if index in done:
            continue
        lo, hi = g["s5_masks"][index]
        mask = lo | (hi << 64)
        legal = board.legal(mask).bit_count()
        canonical_children = len(board.children(mask))
        src = EXP / f"input/s5-{index}.csv"
        src.parent.mkdir(parents=True, exist_ok=True)
        text = f"conflict,{index},5,{lo},{hi},{legal},5,0,0,0,0\n"
        if src.exists():
            assert src.read_text() == text, index
        else:
            src.write_text(text)
        out = EXP / f"output/{args.prefix}-{index}.csv"
        log = EXP / f"output/{args.prefix}-{index}.log"
        trace = trace_dir / f"{args.prefix}-{index}-proof.csv"
        if out.exists() and "# replay_done rows=1" not in out.read_text():
            out.unlink()
            if log.exists():
                log.unlink()
            if trace.exists():
                trace.unlink()
        assert not out.exists() and not log.exists() and not trace.exists()
        command = [str(binary), "--n=11", f"--memo={args.memo}", "--only=5",
                   f"--exact-order={args.order}", f"--exact-replay={src}",
                   f"--exact-replay-budget={args.budget}", f"--csv={out}",
                   "--exact-replay-profile", f"--proof-dag={trace}"]
        started = time.monotonic()
        with log.open("w") as stream:
            child = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT, text=True)
            _, status, usage = os.wait4(child.pid, 0)
            child.returncode = os.waitstatus_to_exitcode(status)
        wall = time.monotonic() - started
        item = dict(s5_index=index, mask=[lo, hi], legal=legal,
                    canonical_children=canonical_children, budget=args.budget,
                    wall_seconds=round(wall, 3), peak_rss_kib=usage.ru_maxrss,
                    returncode=child.returncode)
        if child.returncode != 0:
            item.update(status="RUN_FAILED", verdict=None, nodes=None)
            result["rows"].append(item)
            manifest.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
            print(json.dumps(item), flush=True)
            continue
        raw = out.read_text()
        assert "replay_error," not in raw and "# replay_done rows=1" in raw
        rows = [s.split(",") for s in raw.splitlines() if s.startswith("replay,")]
        assert len(rows) == 1
        r = rows[0]
        v = int(r[6])
        nodes = int(r[7])
        assert v in (0, 1, 2) and 0 < nodes <= args.budget
        assert int(r[2]) == 5 and int(r[3]) == legal and [int(r[9]), int(r[10])] == [lo, hi]
        if v == 0:
            assert nodes == args.budget and not trace.exists()
        else:
            assert trace.exists()
        census, table = parse_profile(out)
        item.update(status="SOLVED" if v else "NODE_LIMIT", verdict=v, nodes=nodes,
                    input_sha256=sha(src), output_sha256=sha(out),
                    trace_bytes=trace.stat().st_size if trace.exists() else None,
                    trace_sha256=sha(trace) if trace.exists() else None,
                    trace_path=str(trace.relative_to(ROOT)) if trace.exists() else None,
                    root_child_census=census or None, exact_profile=table or None,
                    trust_class=("solver-trusted pending terminal-only receipt" if v
                                 else "UNKNOWN (not evidence)"))
        result["rows"].append(item)
        manifest.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
        print(json.dumps(item), flush=True)
    result["counts"] = {name: sum(r.get("verdict") == v for r in result["rows"])
                        for name, v in [("UNKNOWN", 0), ("WIN", 1), ("LOSS", 2)]}
    result["completed_candidates"] = len(args.indices)
    manifest.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result["counts"]), flush=True)


if __name__ == "__main__":
    main()

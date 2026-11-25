"""Probe one blocking-set instance: does a blocking set of size <= m exist?

Prints SAT/UNSAT, wall time, and (for SAT) the witness size and a direct
independent check.  Does not write results.json (safe for parallel probes).

Usage:
    python probe_blocking.py --q 7 --m 15 --solver cadical195
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import blocking_sat as B  # noqa: E402
from pysat.card import CardEnc, EncType  # noqa: E402
from pysat.formula import CNF  # noqa: E402
from pysat.solvers import Solver  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--solver", default="cadical195")
    ap.add_argument("--encoding", default="seq")
    ap.add_argument("--write", type=Path, default=None,
                    help="write the witness JSON here when SAT")
    args = ap.parse_args()

    b = B.board(args.q)
    v, blocks = b["v"], b["blocks"]
    cnf = CNF()
    for C in blocks:
        cnf.append([p + 1 for p in C])
    card = CardEnc.atmost(lits=list(range(1, v + 1)), bound=args.m, top_id=v,
                          encoding=B.ENCODINGS[args.encoding])
    for cl in card.clauses:
        cnf.append(cl)
    t0 = time.time()
    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        res = solver.solve()
        model = solver.get_model() if res else None
    dt = time.time() - t0
    if not res:
        print(f"q={args.q} m={args.m} solver={args.solver} clauses={len(cnf.clauses)} "
              f"solve={dt:.2f}s -> UNSAT", flush=True)
        return
    X = [i - 1 for i in range(1, v + 1) if model[i - 1] > 0]
    ok = B.verify(args.q, X)
    print(f"q={args.q} m={args.m} solver={args.solver} clauses={len(cnf.clauses)} "
          f"solve={dt:.2f}s -> SAT size={len(X)} verify={ok}", flush=True)
    if args.write:
        args.write.write_text(json.dumps({"q": args.q, "n": len(X), "points": X}),
                              encoding="utf-8")
        print(f"witness -> {args.write}", flush=True)
    assert ok


if __name__ == "__main__":
    main()

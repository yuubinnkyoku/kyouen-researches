"""Probe one SAT instance for (q, s, n): encoding / solver choice and timing.

A wall-clock interrupt is implemented with a timer thread and
``Solver.interrupt()``; a solver that does not support interruption is reported
as such (never silently as UNSAT).  CaDiCaL does not support interrupt, so use
this probe under an external timeout or with glucose for limited solves.

Usage:
    python probe_instance.py --q 8 --s 4 --n 17 --solver glucose3 --encoding tot --circle card --seconds 60
"""

from __future__ import annotations

import argparse
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import spectrum_sat as S  # noqa: E402
from pysat.solvers import Solver  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--solver", default="glucose3")
    ap.add_argument("--encoding", default="tot", choices=sorted(S.ENCODINGS))
    ap.add_argument("--circle", default="card", choices=["subsets", "card"])
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--no-sym", action="store_true")
    args = ap.parse_args()

    board = S.load_board(args.q)
    cnf, _ = S.build_cnf(board, args.s, args.n, args.encoding, not args.no_sym, args.circle)
    t0 = time.time()
    ok_interrupt = True
    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        timer = threading.Timer(args.seconds, solver.interrupt)
        timer.start()
        try:
            res = solver.solve_limited(expect_interrupt=True)
        except NotImplementedError:
            ok_interrupt = False
            res = solver.solve()
        finally:
            timer.cancel()
    dt = time.time() - t0
    outcome = "TIMEOUT" if res is None else ("SAT" if res else "UNSAT")
    if not ok_interrupt:
        outcome += " (no-interrupt)"
    print(f"q={args.q} s={args.s} n={args.n} solver={args.solver} enc={args.encoding}/{args.circle} "
          f"sym={not args.no_sym} clauses={len(cnf.clauses)} solve={dt:.2f}s -> {outcome}",
          flush=True)


if __name__ == "__main__":
    main()

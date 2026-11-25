"""SAT certificate search for "does an s-arc of size >= n exist?" in M(q).

Independent of the earlier spectrum_sat.py implementation (own encoder, own
board loader).  Variables x_p (p in S).

  * circle_mode=subsets: for every circle and every (s+1)-subset, one clause.
  * circle_mode=card:    one at-most-s cardinality per circle (seqcounter).
  * at-least-n cardinality over all points.
  * symmetry breaking: x_inf = x_0 = x_1 = 1 (PGL(2,q^2) is 3-transitive and
    preserves circles, so an s-arc of size n exists iff one containing
    {inf, 0, 1} exists; valid for s >= 3).

UNSAT is a proof that no s-arc of that size exists (given the board);
SAT yields an explicit witness that must be checked by verify_arc.py.

Usage:
    python sat_arc.py --q 9 --s 4 --n 17 --solver cadical195 --max-seconds 600
"""

from __future__ import annotations

import argparse
import itertools
import json
import threading
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
REPO = EXP.parents[2]
BOARDS = EXP / "output"

ENCODINGS = {"seq": EncType.seqcounter, "tot": EncType.totalizer,
             "mtot": EncType.mtotalizer}


def load_board(q: int) -> dict:
    return json.loads((BOARDS / f"board_q{q}.json").read_text(encoding="utf-8"))


def build_cnf(board: dict, s: int, n: int, circle_mode: str,
              encoding: str, sym: bool) -> CNF:
    v = board["v"]
    cnf = CNF()
    top = v
    if circle_mode == "subsets":
        for b in board["blocks"]:
            for comb in itertools.combinations(b, s + 1):
                cnf.append([-(p + 1) for p in comb])
    elif circle_mode == "card":
        for b in board["blocks"]:
            card = CardEnc.atmost(lits=[p + 1 for p in b], bound=s,
                                  top_id=top, encoding=ENCODINGS[encoding])
            for cl in card.clauses:
                cnf.append(cl)
            top = max(top, card.nv)
    else:
        raise ValueError(circle_mode)
    card = CardEnc.atleast(lits=list(range(1, v + 1)), bound=n, top_id=top,
                           encoding=ENCODINGS[encoding])
    for cl in card.clauses:
        cnf.append(cl)
    if sym:
        for p in (board["special"]["inf"], board["special"]["zero"],
                  board["special"]["one"]):
            cnf.append([p + 1])
    return cnf


def run(q: int, s: int, n: int, solver_name: str, circle_mode: str,
        encoding: str, sym: bool, max_seconds: float) -> dict:
    board = load_board(q)
    cnf = build_cnf(board, s, n, circle_mode, encoding, sym)
    info = {"q": q, "s": s, "n": n, "solver": solver_name,
            "circle_mode": circle_mode, "encoding": encoding, "sym": sym,
            "variables": cnf.nv, "clauses": len(cnf.clauses),
            "max_seconds": max_seconds}
    t0 = time.time()
    with Solver(name=solver_name, bootstrap_with=cnf.clauses,
                use_timer=True) as solver:
        watchdog = None
        if max_seconds and max_seconds > 0:
            watchdog = threading.Timer(max_seconds, solver.interrupt)
            watchdog.start()
        try:
            status = solver.solve()
        finally:
            if watchdog is not None:
                watchdog.cancel()
        elapsed = time.time() - t0
        timed_out = elapsed >= max_seconds - 0.5
        info["seconds"] = round(elapsed, 3)
        info["timed_out"] = bool(timed_out and status is None)
        if status is None:
            info["result"] = "TIMEOUT"
            return info
        info["result"] = "SAT" if status else "UNSAT"
        if status:
            model = solver.get_model()
            chosen = [i - 1 for i in range(1, board["v"] + 1) if model[i - 1] > 0]
            info["points"] = sorted(chosen)
            info["size"] = len(chosen)
    return info


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--solver", default="cadical195")
    ap.add_argument("--circle-mode", default="subsets",
                    choices=["subsets", "card"])
    ap.add_argument("--encoding", default="seq", choices=sorted(ENCODINGS))
    ap.add_argument("--no-sym", action="store_true")
    ap.add_argument("--max-seconds", type=float, default=0)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    info = run(args.q, args.s, args.n, args.solver, args.circle_mode,
               args.encoding, not args.no_sym, args.max_seconds)
    print(json.dumps({k: v for k, v in info.items() if k != "points"}))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(info, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

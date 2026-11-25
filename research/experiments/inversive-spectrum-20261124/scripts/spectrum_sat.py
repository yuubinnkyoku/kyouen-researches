"""Exact K_s(q) for the inversive plane, via SAT with an explicit witness.

Definitions
-----------
M(q): q^2+1 points, q(q^2+1) circles of size q+1.
K_s(q) = max |S| such that |S ∩ C| <= s for every circle C.

The theorem proved in the README gives K_s(q) <= (s-2)(q+1)+2 for 2 <= s <= q+1.

Method
------
For a target n, build a CNF over x_p ("p is chosen"):
  * for every circle and every (s+1)-subset, one clause forbidding all of them;
  * a cardinality constraint sum x_p >= n (sequential counter);
  * symmetry breaking x_inf = x_0 = x_1 = 1, valid because PGL(2,q^2) is
    3-transitive and maps circles to circles (so an arc of size n exists iff one
    containing {inf,0,1} exists), used only for s >= 3.
The exact value is found by walking n upward from a greedy witness until the
instance becomes UNSAT.  The final UNSAT instance is re-solved with a second
engine.  Witnesses are written to output/witness_q<q>_s<s>_n<n>.json and must
be checked by verify_witness.py (which has no SAT dependency).

Usage:
    python spectrum_sat.py --tasks 7,3 7,4 8,4 9,4 [--restarts 2000] [--out ...]
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(HERE))
import spectrum_common as C  # noqa: E402

OUT = C.OUT
load_board = C.load_board
point_circles = C.point_circles
greedy = C.greedy

ENCODINGS = {"seq": EncType.seqcounter, "tot": EncType.totalizer,
             "mtot": EncType.mtotalizer}


def forbidden_clauses(board: dict, s: int) -> list[list[int]]:
    clauses = []
    for b in board["blocks"]:
        for comb in itertools.combinations(b, s + 1):
            clauses.append([-(p + 1) for p in comb])
    return clauses


def build_cnf(board: dict, s: int, n: int, encoding: str, sym: bool,
              circle_mode: str = "subsets") -> tuple[CNF, int]:
    v = board["v"]
    cnf = CNF()
    top = v
    if circle_mode == "subsets":
        for cl in forbidden_clauses(board, s):
            cnf.append(cl)
    elif circle_mode == "card":
        # One cardinality-at-most-s constraint per circle: stronger propagation.
        for b in board["blocks"]:
            card = CardEnc.atmost(lits=[p + 1 for p in b], bound=s, top_id=top,
                                  encoding=ENCODINGS[encoding])
            for cl in card.clauses:
                cnf.append(cl)
            top = max(top, card.nv)
    else:
        raise ValueError(circle_mode)
    if n > 0:
        card = CardEnc.atleast(lits=list(range(1, v + 1)), bound=n, top_id=top,
                               encoding=ENCODINGS[encoding])
        for cl in card.clauses:
            cnf.append(cl)
        top = max(top, card.nv)
    if sym:
        for p in (board["special"]["inf"], board["special"]["zero"], board["special"]["one"]):
            cnf.append([p + 1])
    return cnf, top


def solve_once(board: dict, s: int, n: int, solver_name: str, encoding: str,
               sym: bool) -> tuple[bool, list[int] | None, float]:
    cnf, _ = build_cnf(board, s, n, encoding, sym)
    t0 = time.time()
    with Solver(name=solver_name, bootstrap_with=cnf.clauses) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
    dt = time.time() - t0
    if not sat:
        return False, None, dt
    chosen = [i for i in range(1, board["v"] + 1) if model[i - 1] > 0]
    return True, chosen, dt


def run_task(q: int, s: int, args) -> dict:
    board = load_board(q)
    v = board["v"]
    result = {"q": q, "s": s, "v": v, "b": board["b"],
              "bound_theorem": (s - 2) * (q + 1) + 2 if 2 <= s <= q + 1 else None,
              "solver": args.solver, "second_solver": args.second_solver,
              "encoding": args.encoding, "symmetry_breaking": s >= 3}
    if s >= q + 1:
        result.update(exact=v, kind="trivial (all points)", witness=None)
        return result
    if s <= 2:
        result.update(exact=s, kind="trivial (every triple lies on a circle)", witness=None)
        return result

    t0 = time.time()
    best = greedy(q, s, board, args.restarts, args.seed)
    result["greedy_lower"] = len(best)
    n = len(best)
    calls = []
    exact = None
    final_witness = list(best)
    witness_source = "greedy"
    while True:
        if result["bound_theorem"] is not None and n > result["bound_theorem"]:
            raise AssertionError("theorem bound violated")
        target = n + 1
        sat, model, dt = solve_once(board, s, target, args.solver, args.encoding, s >= 3)
        calls.append({"n": target, "sat": sat, "seconds": round(dt, 3)})
        print(f"q={q} s={s} n={target}: {'SAT' if sat else 'UNSAT'} ({dt:.2f}s)", flush=True)
        if not sat:
            exact = n
            break
        n = target
        final_witness = model
        witness_source = "sat"
    result["calls"] = calls
    result["exact"] = exact
    result["elapsed"] = round(time.time() - t0, 2)
    if final_witness is not None:
        points = sorted(final_witness)
        wpath = OUT / f"witness_q{q}_s{s}_n{len(points)}.json"
        wpath.write_text(json.dumps({"q": q, "s": s, "n": len(points),
                                    "points": points}), encoding="utf-8")
        result["witness"] = str(wpath.relative_to(EXP.parents[2]))
        result["witness_source"] = witness_source
    # independent second engine on the final UNSAT instance
    sat2, _, dt2 = solve_once(board, s, exact + 1, args.second_solver, args.encoding, s >= 3)
    result["second_engine_unsat_confirm"] = (not sat2)
    result["second_engine_seconds"] = round(dt2, 3)
    if sat2:
        raise AssertionError("second engine disagrees: found a larger set")
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", nargs="+", required=True,
                    help="pairs q,s such as 7,4")
    ap.add_argument("--restarts", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261124)
    ap.add_argument("--solver", default="cadical195")
    ap.add_argument("--second-solver", default="glucose3")
    ap.add_argument("--encoding", default="seq", choices=sorted(ENCODINGS))
    ap.add_argument("--out", type=Path, default=OUT / "spectrum_results.json")
    ap.add_argument("--force", action="store_true",
                    help="re-run tasks already present in --out")
    args = ap.parse_args()

    tasks = []
    for t in args.tasks:
        q, s = t.split(",")
        tasks.append((int(q), int(s)))

    if args.out.exists():
        results = json.loads(args.out.read_text(encoding="utf-8"))
    else:
        results = {"experiment": "inversive-spectrum-20261124", "results": []}
    done = {(r["q"], r["s"]) for r in results["results"]}
    if args.force:
        results["results"] = [r for r in results["results"]
                              if not any((r["q"], r["s"]) == t for t in tasks)]
        done = {(r["q"], r["s"]) for r in results["results"]}
    for q, s in tasks:
        if (q, s) in done:
            print(f"skip q={q} s={s} (already done)", flush=True)
            continue
        print(f"== task q={q} s={s}", flush=True)
        results["results"].append(run_task(q, s, args))
        args.out.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()

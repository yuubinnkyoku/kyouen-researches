"""SAT search for small blocking sets of the inversive plane M(q).

A blocking set X meets every circle.  We ask for |X| <= m, starting at the
known lower bound m = 2q (Bruen--Rothschild 1985; Kiss--Marcugini--Pambianco
2005 for q >= 4).  A SAT answer at m = 2q proves tau_1(q) = 2q and hence
K_q(q) = q^2+1-2q = (q-1)^2.  UNSAT raises the lower bound.

Encoding: variables y_p; one covering clause per circle; cardinality <= m.
No symmetry breaking (a blocking set has no forced points).

Usage:
    python blocking_sat.py --q 4 5 7 8 9 11 13 --max-m 2q+2
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
REPO = EXP.parents[2]
PUBLISHED = REPO / "research/experiments/finite-field-kyouen-20261120/scripts"
OUT = EXP / "output"
sys.path.insert(0, str(PUBLISHED))

from inversive_fast import build_circles  # noqa: E402

ENCODINGS = {"seq": EncType.seqcounter, "tot": EncType.totalizer}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def board(q: int) -> dict:
    path = OUT / f"board_q{q}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    points, blocks = build_circles(q, check_orbit_size=True)
    assert len(points) == q * q + 1
    data = {"q": q, "v": len(points), "b": len(blocks),
            "block_size": q + 1,
            "builder_sha256": sha256(PUBLISHED / "inversive_fast.py"),
            "blocks": [list(b) for b in blocks]}
    OUT.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
    return data


def exists_blocking(q: int, m: int, solver_name: str, encoding: str,
                    seconds: float = 3600.0) -> tuple[bool | None, list[int] | None, float]:
    b = board(q)
    v, blocks = b["v"], b["blocks"]
    cnf = CNF()
    for C in blocks:
        cnf.append([p + 1 for p in C])
    card = CardEnc.atmost(lits=list(range(1, v + 1)), bound=m, top_id=v,
                          encoding=ENCODINGS[encoding])
    for cl in card.clauses:
        cnf.append(cl)
    t0 = time.time()
    with Solver(name=solver_name, bootstrap_with=cnf.clauses) as solver:
        res = solver.solve()
        model = solver.get_model() if res else None
    dt = time.time() - t0
    if not res:
        return False, None, dt
    X = [i - 1 for i in range(1, v + 1) if model[i - 1] > 0]
    return True, X, dt


def verify(q: int, X: list[int]) -> bool:
    b = board(q)
    S = set(X)
    return all(S.intersection(C) for C in b["blocks"])


def run(q: int, args) -> dict:
    start = 2 * q
    row = {"q": q, "v": q * q + 1, "tau_lower_known": 2 * q,
           "searches": [], "solver": args.solver, "second_solver": args.second_solver}
    if q <= 3:
        row["note"] = "q=3: tau_1=5 exact from K_3(3)=5 (not 2q)"
        start = 2 * q
    for m in range(start, start + args.extra + 1):
        sat, X, dt = exists_blocking(q, m, args.solver, args.encoding)
        row["searches"].append({"m": m, "sat": sat, "seconds": round(dt, 3),
                                "witness_size": None if X is None else len(X)})
        print(f"q={q} m={m}: {'SAT' if sat else 'UNSAT'} ({dt:.2f}s)"
              + (f" size={len(X)}" if X is not None else ""), flush=True)
        if sat:
            assert len(X) <= m and verify(q, X)
            # second engine confirmation on the same bound
            sat2, X2, dt2 = exists_blocking(q, m, args.second_solver, args.encoding)
            assert sat2 and X2 is not None and verify(q, X2)
            row["second_engine_confirm"] = True
            row["second_engine_seconds"] = round(dt2, 3)
            row["tau_upper"] = len(X)
            row["tau_exact"] = len(X) == 2 * q and q >= 4
            row["K_q"] = q * q + 1 - len(X)
            row["K_q_equals_qm1_sq"] = row["K_q"] == (q - 1) ** 2
            row["witness"] = X
            path = OUT / f"blocking_q{q}_n{len(X)}.json"
            path.write_text(json.dumps({"q": q, "n": len(X), "points": X}),
                            encoding="utf-8")
            row["witness_path"] = str(path.relative_to(REPO))
            print(f"  -> tau_1({q}) = {len(X)}; K_q = {row['K_q']}", flush=True)
            return row
    row["tau_upper"] = start + args.extra
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--extra", type=int, default=2,
                    help="try m = 2q .. 2q+extra")
    ap.add_argument("--solver", default="cadical195")
    ap.add_argument("--second-solver", default="glucose3")
    ap.add_argument("--encoding", default="seq", choices=sorted(ENCODINGS))
    ap.add_argument("--out", type=Path, default=OUT / "results.json")
    args = ap.parse_args()
    data = (json.loads(args.out.read_text(encoding="utf-8"))
            if args.out.exists() else {"experiment": "inversive-blocking-equality-20261124",
                                       "results": []})
    done = {r["q"] for r in data["results"]}
    for q in args.q:
        if q in done:
            continue
        print(f"== q={q}", flush=True)
        data["results"].append(run(q, args))
        args.out.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(json.dumps(data, indent=1))


if __name__ == "__main__":
    main()

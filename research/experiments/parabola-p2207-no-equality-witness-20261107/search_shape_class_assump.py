"""Assumption-based d sweep over one shape-class CNF (single solver, shared clauses).

The class CNF from :mod:`search_shape_class` constrains a 4-valued pair variable
per pair and asks for exactly ``c`` complete pairs.  Because ``c`` is fixed by
the cardinality constraint, assuming ``B_d`` restricts the CNF to the subproblem
"pair d is the (only) complete pair"; sweeping ``d`` therefore partitions the
class and every lemma learned under one ``d`` stays valid for the others.

Coverage: for ``c >= 1`` the sweep ``d = 1 .. h`` is a disjoint cover of the
class (exactly ``c`` of the ``B`` variables are true).  For ``c == 0`` no
complete pair exists and the single record is ``d = 0`` solved without an
assumption; ``--ds`` is ignored for that class.

Output records are rewritten to ``--output`` after every query, so an
interrupted sweep resumes by skipping ``(class, d)`` pairs already present.
Existing ``output/shape_class_*.json`` files are never touched.

Usage:
  search_shape_class_assump.py --p 2647 --size 1322 --x 1 --c 1 --e 3 \
      --budget 100000 --ds 1..5 --output out.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from search_shape_class import build  # noqa: E402

ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402


def v(pair: int, kind: str) -> int:
    return 4 * pair - 4 + {"B": 1, "N": 2, "L": 3, "H": 4}[kind]


def parse_ds(spec: str | None, h: int) -> list[int]:
    if spec is None or spec.strip() == "":
        return list(range(1, h + 1))
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if ".." in part:
            lo, hi = part.split("..", 1)
            out.update(range(int(lo), int(hi) + 1))
        else:
            out.add(int(part))
    for d in out:
        if not 1 <= d <= h:
            raise SystemExit(f"d={d} outside 1..{h}")
    return sorted(out)


def resolve_classes(p: int, size: int, x, c, e):
    h = (p - 1) // 2
    classes = []
    for xx in (0, 1):
        for cc in range(0, 2):
            ee = xx + cc + h - size
            if ee < 0 or ee > h - cc:
                continue
            if x is not None and xx != x:
                continue
            if c is not None and cc != c:
                continue
            if e is not None and ee != e:
                continue
            classes.append((xx, cc, ee))
    return classes


def decode(model, p: int, h: int, x: int) -> list[int]:
    pos = {i for i in model if i > 0}
    chosen = {0} if x else set()
    for i in range(1, h + 1):
        if v(i, "B") in pos:
            chosen.update({i, p - i})
        elif v(i, "L") in pos:
            chosen.add(i)
        elif v(i, "H") in pos:
            chosen.add(p - i)
    assert all(v(i, "N") in pos or v(i, "B") in pos or v(i, "L") in pos
               or v(i, "H") in pos for i in range(1, h + 1)), "pair unassigned in model"
    return sorted(chosen)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--size", type=int, required=True)
    ap.add_argument("--x", type=int, default=None)
    ap.add_argument("--c", type=int, default=None)
    ap.add_argument("--e", type=int, default=None)
    ap.add_argument("--budget", type=int, default=100_000,
                    help="conflict budget per single d query")
    ap.add_argument("--ds", default=None,
                    help='d selection, e.g. "1..20" or "1,50,100" (default: all 1..h)')
    ap.add_argument("--output", required=True)
    ap.add_argument("--gen", default=None,
                    help="path to forbidden_edges.exe (default: $TEMP/forbidden_edges.exe)")
    args = ap.parse_args()

    p, h = args.p, (args.p - 1) // 2
    classes = resolve_classes(p, args.size, args.x, args.c, args.e)
    if not classes:
        print("no admissible class", flush=True)
        return 1
    ds = parse_ds(args.ds, h)

    gen = args.gen or str(Path(os.environ["TEMP"]) / "forbidden_edges.exe")
    edges = run_gen(gen, p)
    edge_sets = [frozenset(q) for q in edges]

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = {"p": p, "h": h, "size": args.size, "budget": args.budget,
           "ds_spec": args.ds, "edges": len(edges), "classes": {}, "records": []}
    if out_path.exists():
        old = json.loads(out_path.read_text(encoding="utf-8"))
        doc["classes"] = old.get("classes", {})
        doc["records"] = old.get("records", [])
    done = {(tuple(r["class"]), r["d"]) for r in doc["records"]}

    def flush() -> None:
        out_path.write_text(json.dumps(doc, indent=1) + "\n",
                            encoding="utf-8", newline="\n")

    for (x, c, e) in classes:
        clauses, nv, kept = build(p, edges, x, c, e)
        meta = {"vars": nv, "clauses": len(clauses), "kept_edges": kept}
        doc["classes"][f"{x},{c},{e}"] = meta
        flush()
        print(f"class(x={x},c={c},e={e}) vars={nv} clauses={len(clauses)} "
              f"kept_edges={kept}", flush=True)
        solver = Cadical195(bootstrap_with=clauses)
        sweep = [0] if c == 0 else ds
        try:
            for d in sweep:
                if ((x, c, e), d) in done:
                    print(f"  d={d} already recorded, skip", flush=True)
                    continue
                assumptions = [] if c == 0 else [v(d, "B")]
                solver.conf_budget(args.budget)
                t0 = time.time()
                res = solver.solve_limited(assumptions=assumptions)
                dt = time.time() - t0
                rec = {"class": [x, c, e], "d": d, "sat": res,
                       "unknown": res is None, "seconds": round(dt, 3),
                       "budget": args.budget}
                if res:
                    chosen = decode(solver.get_model(), p, h, x)
                    # Ground truth against the full forbidden-quadruple list.
                    # When x == 0 the point 0 is absent, so 0-edges cannot fire.
                    cs = frozenset(chosen)
                    safe = not any(q <= cs for q in edge_sets)
                    rec.update({"witness_size": len(chosen),
                                "safe_against_edges": safe, "points": chosen})
                doc["records"].append(rec)
                flush()
                print(f"  d={d} sat={res} unknown={res is None} secs={dt:.3f}"
                      + (f" size={rec['witness_size']} safe={rec['safe_against_edges']}"
                         if res else ""), flush=True)
        finally:
            solver.delete()

    print(f"wrote {out_path} ({len(doc['records'])} records)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

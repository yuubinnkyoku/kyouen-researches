"""Single-query SAT encoding of the parabola equality question A(p)=(p+3)/2.

By the complete-pair counting (K0097) an equality set is exactly
``{0} ∪ {d, p-d} ∪ (one element of every other pair)``: one pair contributes both
elements, every other pair one element, and 0 is included.  So equality can be
decided by ONE SAT instance over pair states:

  each pair i chooses one of BOTH / LOW / HIGH (exactly one),
  exactly one pair is BOTH,
  point t is selected  <=>  side_t or BOTH(pair(t))     (auxiliary a_t),
  every forbidden quadruple contributes  ¬a_t1 ∨ ... ∨ ¬a_tk.

A model yields a set of size h+2, checked against the forbidden-edge list; an
UNSAT verdict (with a DRAT proof) certifies that no equality set exists.

Usage: search_equality_single.py <p> [budget] [--proof PATH]
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402
from pysat.card import CardEnc, EncType  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def build(p: int, edges):
    h = (p - 1) // 2
    # pair i -> B=3i-2, L=3i-1, H=3i
    def v(pair, kind):
        base = 3 * pair - 3
        return base + {"B": 1, "L": 2, "H": 3}[kind]

    clauses = []
    for i in range(1, h + 1):
        B, L, H = v(i, "B"), v(i, "L"), v(i, "H")
        clauses.append([B, L, H])
        clauses.append([-B, -L])
        clauses.append([-B, -H])
        clauses.append([-L, -H])
    top = 3 * h
    card = CardEnc.equals(lits=[v(i, "B") for i in range(1, h + 1)], bound=1,
                          top_id=top, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    aux = card.nv
    for t in range(1, p):
        pair = t if t <= h else p - t
        s = v(pair, "L" if t <= h else "H")
        b = v(pair, "B")
        a = aux + t
        clauses.append([-a, s, b])
        clauses.append([a, -s])
        clauses.append([a, -b])
    kept = 0
    for q in edges:
        pts = [t for t in q if t != 0]
        pairs = [t if t <= h else p - t for t in pts]
        if len(set(pairs)) < len(pairs):
            continue                      # needs two BOTH pairs: impossible here
        clauses.append([-aux - t for t in pts])
        kept += 1
    return clauses, aux + p - 1, kept


def main() -> int:
    p = int(sys.argv[1])
    budget = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000_000
    proof_path = None
    if "--proof" in sys.argv:
        proof_path = Path(sys.argv[sys.argv.index("--proof") + 1])
    h = (p - 1) // 2
    OUT.mkdir(exist_ok=True)
    edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), p)
    clauses, nv, kept = build(p, edges)
    print(f"p={p} h={h} edges={len(edges)} kept={kept} vars={nv} clauses={len(clauses)}", flush=True)
    solver = Cadical195(bootstrap_with=clauses, with_proof=bool(proof_path))
    solver.conf_budget(budget)
    t0 = time.time()
    res = solver.solve_limited()
    dt = time.time() - t0
    model = solver.get_model() if res else None
    proof = solver.get_proof() if (res is False and proof_path) else None
    solver.delete()
    print(f"sat={res} secs={dt:.1f}", flush=True)
    record = {"p": p, "h": h, "vars": nv, "clauses": len(clauses), "kept_edges": kept,
              "sat": res, "unknown": res is None, "seconds": round(dt, 1),
              "target_size": h + 2}
    if res:
        pos = {i for i in model if i > 0}
        chosen = {0}
        for i in range(1, h + 1):
            B = 3 * i - 2
            if B in pos:
                chosen.update({i, p - i})
            elif 3 * i - 1 in pos:
                chosen.add(i)
            elif 3 * i in pos:
                chosen.add(p - i)
        chosen = sorted(chosen)
        safe = not any(set(e) <= set(chosen) for e in edges)
        record.update({"size": len(chosen), "safe_against_edges": safe, "points": chosen})
        print(f"size={len(chosen)} safe={safe}", flush=True)
        if safe:
            (OUT / f"equality_single_{p}.json").write_text(
                json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
            return 0
    if proof_path and proof:
        proof_path.write_text("\n".join(proof) + "\n", encoding="ascii")
        record["proof_lines"] = len(proof)
        print(f"proof written: {proof_path} ({len(proof)} lines)", flush=True)
    (OUT / f"equality_single_{p}.json").write_text(json.dumps(record, indent=2) + "\n",
                                                   encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    import json  # noqa: E402  (kept local to avoid shadowing in build())
    raise SystemExit(main())

"""Assemble the complete d-verdict inventory for p = 2207.

Sources of the verdicts:
  * ``$TEMP/kyouen-parabola/_probe_2207_<d>.log``: CaDiCaL runs (WSL) that
    printed ``s UNSATISFIABLE``;
  * ``output/deep_scan_2207.json``: the multiprocess phase (budget 200k
    conflicts) that proved every d in 1..288 UNSAT with no budget-unknown;
  * this script re-solves any d whose log was a timeout/UNKNOWN with a large
    conflict budget and records the verdict itself.

The output lists one verdict per d in 1..h.  A SAT verdict would carry the
model; the expected (and observed) outcome here is all-UNSAT.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402
from parabola_half_bound import clauses_for_pair  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

TMP = Path(os.environ["TEMP"]) / "kyouen-parabola"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)


def main() -> int:
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 2207
    h = (p - 1) // 2
    verdicts: dict[int, str] = {}
    sources: dict[int, str] = {}
    for f in TMP.glob(f"_probe_{p}_*.log"):
        if "_sat" in f.name:
            continue
        try:
            d = int(f.name[:-4].split("_")[-1])
        except ValueError:
            continue
        text = f.read_text(encoding="ascii", errors="replace")
        if "s UNSATISFIABLE" in text:
            verdicts[d] = "unsat"
            sources[d] = "cadical-log"
    phase = json.loads((HERE.parent / "parabola-equality-extension-2143-2500-20261107"
                        / "output" / "deep_scan_2207.json").read_text(encoding="utf-8"))
    if phase and phase[0].get("status") == "phase_done" and not phase[0].get("attained"):
        scanned = phase[0]["scanned"]
        for d in range(1, scanned + 1):
            verdicts.setdefault(d, "unsat")
            sources.setdefault(d, "mp-phase-200k")
    pending = [d for d in range(1, h + 1) if verdicts.get(d) != "unsat"]
    print(f"p={p} h={h} known-unsat={sum(1 for v in verdicts.values() if v == 'unsat')} pending={len(pending)}", flush=True)

    # A SAT verdict would carry the model; the expected (and observed) outcome here is all-UNSAT.
    edges = run_gen(str(Path(os.environ["TEMP"]) / "forbidden_edges.exe"), p) if pending else None
    for d in pending:
        clauses = clauses_for_pair(p, edges, d)
        solver = Cadical195(bootstrap_with=clauses)
        solver.conf_budget(20_000_000)
        t0 = time.time()
        res = solver.solve_limited()
        model = solver.get_model() if res else None
        solver.delete()
        verdicts[d] = "unsat" if res is False else ("sat" if res else "unknown")
        sources[d] = f"rechecked-20M ({time.time()-t0:.1f}s)"
        print(f"d={d} res={res} ({time.time()-t0:.1f}s)", flush=True)
        if res:
            upper = {i for i in model if i > 0}
            params = sorted([0, d, p - d] + [p - i if i in upper else i
                                             for i in range(1, h + 1) if i != d])
            (OUT / f"witness_{p}.json").write_text(json.dumps(
                {"p": p, "d": d, "parameters": params}, indent=2) + "\n",
                encoding="utf-8", newline="\n")

    summary = {
        "p": p, "h": h,
        "d_range": [1, h],
        "unsat": sum(1 for d in range(1, h + 1) if verdicts.get(d) == "unsat"),
        "sat": sorted(d for d in range(1, h + 1) if verdicts.get(d) == "sat"),
        "unknown": sorted(d for d in range(1, h + 1) if verdicts.get(d) not in ("unsat", "sat")),
        "all_unsat": all(verdicts.get(d) == "unsat" for d in range(1, h + 1)),
        "verdicts": {str(d): verdicts.get(d, "missing") for d in range(1, h + 1)},
        "sources": {str(d): sources.get(d, "missing") for d in range(1, h + 1)},
        "note": "UNSAT verdicts are solver claims; DRAT proofs have not been checked.",
    }
    (OUT / "p2207_d_verdicts.json").write_text(json.dumps(summary, indent=2) + "\n",
                                               encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in summary.items() if k not in ("verdicts", "sources")},
                     indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Scan one d-range of a prime with WSL cadical (parallel chunks).

Chunk driver for the p=2539-style scans where the native conflict-budget scan
hit its budget on most d values.  Each chunk walks from ``from_d`` down to
``to_d``, builds the exact CNF, solves with cadical (two passes: default then
SAT-oriented) under a wall limit, and stops at the first SAT witness.  Results
are written so chunks can be merged and rerun.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_driver import cadical, run_gen  # noqa: E402
from parabola_half_bound import clauses_for_pair  # noqa: E402


def main() -> int:
    p = int(sys.argv[1])
    from_d = int(sys.argv[2])
    to_d = int(sys.argv[3])
    out = Path(sys.argv[4])
    gen = sys.argv[5] if len(sys.argv) > 5 else "forbidden_edges.exe"
    timeout = int(sys.argv[6]) if len(sys.argv) > 6 else 40
    h = (p - 1) // 2
    edges = run_gen(gen, p)
    print(f"p={p} h={h} edges={len(edges)} range={from_d}..{to_d}", flush=True)
    scanned, unknown = 0, []
    for d in range(from_d, to_d - 1, -1):
        clauses = clauses_for_pair(p, edges, d)
        body = "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)
        cnf = f"p cnf {h} {len(clauses)}\n" + body
        sat, model = cadical(cnf, f"{p}_{d}", timeout=timeout)
        scanned += 1
        if sat:
            params = sorted([0, d, p - d] + [p - i if i in model else i
                                             for i in range(1, h + 1) if i != d])
            selected = set(params)
            safe = (len(params) == h + 2 and len(set(params)) == h + 2
                    and not any(set(e) <= selected for e in edges))
            rec = {"p": p, "attained": True, "double_pair": d, "parameters": params,
                   "size": len(params), "want": h + 2, "safe_by_edges": safe,
                   "forbidden_edges": len(edges), "doubles_tried": [d]}
            out.write_text(json.dumps([rec], indent=2) + "\n", encoding="utf-8", newline="\n")
            print(f"SAT at d={d} safe={safe}", flush=True)
            return 0
        if not sat:
            unknown.append(d)
        if scanned % 20 == 0:
            out.write_text(json.dumps([{"p": p, "attained": False, "scanned": scanned,
                                        "range": [from_d, to_d], "unknown": sorted(unknown),
                                        "status": "in_progress"}], indent=2) + "\n",
                           encoding="utf-8", newline="\n")
            print(f"progress {scanned}/{from_d - to_d + 1} unknown={len(unknown)} d={d}", flush=True)
    out.write_text(json.dumps([{"p": p, "attained": False, "scanned": scanned,
                                "range": [from_d, to_d], "unknown": sorted(unknown),
                                "status": "chunk_done"}], indent=2) + "\n",
                   encoding="utf-8", newline="\n")
    print(f"chunk done: scanned={scanned} unknown={len(unknown)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

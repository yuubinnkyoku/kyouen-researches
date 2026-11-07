"""Continue the d-scan for one prime, skipping d values already attempted.

The driver ``probe_driver.py`` always restarts at ``d = h``; this script resumes
from the previously tried values recorded in the probe logs and walks down to a
floor.  It stops at the first SAT witness and writes it in the same schema.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_driver import TMP, cadical, run_gen  # noqa: E402
from parabola_half_bound import clauses_for_pair  # noqa: E402


def already_tried(p: int) -> set[int]:
    done = set()
    for f in TMP.glob(f"_probe_{p}_*.log"):
        if "_sat" in f.name:
            continue
        try:
            done.add(int(f.name[:-4].split("_")[-1]))
        except ValueError:
            pass
    return done


def main() -> int:
    p = int(sys.argv[1])
    gen = sys.argv[2]
    floor_d = int(sys.argv[3])
    out = Path(sys.argv[4])
    h = (p - 1) // 2
    edges = run_gen(gen, p)
    done = already_tried(p)
    print(f"p={p} h={h} edges={len(edges)} already tried={len(done)}", flush=True)
    scanned = 0
    for d in range(h, floor_d - 1, -1):
        if d in done:
            continue
        clauses = clauses_for_pair(p, edges, d)
        body = "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)
        cnf = f"p cnf {h} {len(clauses)}\n" + body
        sat, model = cadical(cnf, f"{p}_{d}", timeout=30)
        scanned += 1
        if sat:
            params = sorted([0, d, p - d] + [p - i if i in model else i
                                             for i in range(1, h + 1) if i != d])
            selected = set(params)
            safe = (len(params) == h + 2 and len(set(params)) == h + 2
                    and not any(set(e) <= selected for e in edges))
            rec = {"p": p, "attained": True, "double_pair": d, "parameters": params,
                   "size": len(params), "want": h + 2, "safe_by_edges": safe,
                   "forbidden_edges": len(edges), "clauses": len(clauses),
                   "doubles_tried": [d]}
            out.write_text(json.dumps([rec], indent=2) + "\n", encoding="utf-8", newline="\n")
            print(f"SAT at d={d} safe={safe} scanned={scanned}", flush=True)
            return 0
        if scanned % 25 == 0:
            print(f"progress scanned={scanned} d={d}", flush=True)
            out.write_text(json.dumps([{"p": p, "attained": False, "scanned": scanned,
                                        "last_d": d, "status": "in_progress"}], indent=2) + "\n",
                           encoding="utf-8", newline="\n")
    out.write_text(json.dumps([{"p": p, "attained": False, "scanned": scanned,
                                "last_d": floor_d, "status": "exhausted"}], indent=2) + "\n",
                   encoding="utf-8", newline="\n")
    print(f"no SAT down to d={floor_d} after {scanned} new scans", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

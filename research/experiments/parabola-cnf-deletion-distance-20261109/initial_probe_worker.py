"""One fixed-pair RC2 probe. Run through a parent with a wall-clock timeout."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
ENCODER_DIR = ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"
sys.path.insert(0, str(ENCODER_DIR))
from parabola_half_bound import clauses_for_pair
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF


def save(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def violated(clauses, positive):
    return [c for c in clauses if not any((lit > 0) == (abs(lit) in positive) for lit in c)]


def selected_parameters(p, d, positive):
    return sorted([0, d, p-d] + [p-i if i in positive else i
                                  for i in range(1, (p-1)//2 + 1) if i != d])


def repair(p, params, bad):
    # A false positive literal requires the low side; a false negative literal
    # requires the high side. Every preimage forbidden quadruple contains it.
    supports = [{lit if lit > 0 else p+lit for lit in c} for c in bad]
    remaining = set(params)
    removed = []
    while supports:
        counts = Counter(t for support in supports for t in support)
        if not counts:
            raise ValueError("empty projected clause has no removable point")
        point = min(counts, key=lambda t: (-counts[t], t))
        if point not in remaining:
            raise ValueError("projection/removal polarity mismatch")
        removed.append(point)
        remaining.remove(point)
        supports = [s for s in supports if point not in s]
    return sorted(remaining), removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime", type=int, required=True)
    ap.add_argument("--double", type=int, required=True)
    ap.add_argument("--edges", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    p, d = args.prime, args.double
    h = (p-1)//2
    if not p > 2 or p % 2 != 1 or not 1 <= d <= h:
        raise ValueError("invalid p or d")
    if args.out.exists() or args.out.with_suffix(".cnf").exists():
        raise FileExistsError("use a fresh output name")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    edges_bytes = args.edges.read_bytes()
    edges = [tuple(map(int, line.split())) for line in edges_bytes.splitlines()]
    clauses = sorted({tuple(sorted(c, key=lambda lit: (abs(lit), lit)))
                      for c in clauses_for_pair(p, edges, d)})
    assert clauses and all(clauses)
    cnf_bytes = (f"p cnf {h} {len(clauses)}\n" + "".join(
        " ".join([*(str(lit) for lit in c), "0"]) + "\n" for c in clauses)).encode("ascii")
    cnf = args.out.with_suffix(".cnf")
    cnf.write_bytes(cnf_bytes)
    report = {"p": p, "d": d, "h": h, "clauses": len(clauses),
              "cnf_sha256": hashlib.sha256(cnf_bytes).hexdigest(),
              "edges_sha256": hashlib.sha256(edges_bytes).hexdigest(),
              "encoder_source_sha256": hashlib.sha256((ENCODER_DIR/"parabola_half_bound.py").read_bytes()).hexdigest(),
              "python_sat": importlib.metadata.version("python-sat"),
              "solver": "RC2(g3), all original clauses soft with weight 1", "stage": "READY"}
    save(args.out.with_suffix(".init.json"), report)
    print(f"READY p={p} d={d} clauses={len(clauses)}", flush=True)
    formula = WCNF()
    for c in clauses:
        formula.append(list(c), weight=1)
    formula.nv = max(formula.nv, h)
    started = time.monotonic()
    with RC2(formula, solver="g3") as optimizer:
        model = optimizer.compute()
        cost = optimizer.cost
    if model is None:
        raise RuntimeError("all-soft MaxSAT must admit an assignment")
    positive = {lit for lit in model if 0 < lit <= h}
    bad = violated(clauses, positive)
    if len(bad) != cost:
        raise ValueError("RC2 cost differs from direct original-clause evaluation")
    params = selected_parameters(p, d, positive)
    assert len(params) == len(set(params)) == h+2
    near, removed = repair(p, params, bad)
    report.update({"stage": "MODEL", "compute_seconds": time.monotonic()-started,
                   "rc2_reported_cost": cost, "verified_violation_count": len(bad),
                   "model_signed_original": [i if i in positive else -i for i in range(1, h+1)],
                   "violated_clauses": bad, "template_parameters": params,
                   "removed_parameters": removed, "candidate_parameters": near,
                   "candidate_size": len(near), "safe_by_cached_edges": None,
                   "scope": "Model gives a verified CNF-distance upper bound; RC2 optimality is not independently certified."})
    save(args.out, report)
    selected = set(near)
    bad_edges = sum(all(t in selected for t in edge) for edge in edges)
    report.update({"stage": "MODEL_AND_EDGE_CHECK", "remaining_forbidden_edges": bad_edges,
                   "safe_by_cached_edges": bad_edges == 0})
    save(args.out, report)
    print(f"MODEL cost={cost} removed={len(removed)} size={len(near)} forbidden={bad_edges}", flush=True)


if __name__ == "__main__":
    main()

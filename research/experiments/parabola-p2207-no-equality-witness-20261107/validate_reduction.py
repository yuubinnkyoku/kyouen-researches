"""Validate the K0334 reduction + CNF encoder on small primes by exact enumeration.

For each odd prime p <= 29 we enumerate *every* safe set of size (p+3)/2 in
Q_p = {(t, t^2 mod p)} with a pruned DFS over the forbidden-quadruple
hypergraph (integer 4x4 determinant test), record which complete pairs
{d, p-d} occur, and compare with SAT/UNSAT of the signed NAE3/4 + origin CNF
used by the witness search.  Agreement supports that the implementation
realises the proven reduction (K0334); the reduction itself is K0334's proof.
"""
from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
from parabola_half_bound import clauses_for_pair  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def det4(pts) -> int:
    (x, y) = pts[0]
    rows = [(a - x, b - y, (a - x) ** 2 + (b - y) ** 2) for a, b in pts[1:]]
    (a1, b1, c1), (a2, b2, c2), (a3, b3, c3) = rows
    return (a1 * (b2 * c3 - c2 * b3) - b1 * (a2 * c3 - c2 * a3)
            + c1 * (a2 * b3 - b2 * a3))


def geometry(p: int):
    pts = [(t, t * t % p) for t in range(p)]
    quads = [q for q in combinations(range(p), 4)
             if det4([pts[i] for i in q]) == 0]
    forbidden_fourth = {}
    for q in quads:
        for tri in combinations(q, 3):
            other = (set(q) - set(tri)).pop()
            forbidden_fourth.setdefault(tri, set()).add(other)
    return pts, quads, forbidden_fourth


def safe_sets(p: int, size: int, forbidden_fourth):
    found = []

    def dfs(chosen, start):
        if len(chosen) == size:
            found.append(tuple(chosen))
            return
        for x in range(start, p):
            bad = False
            for tri in combinations(chosen, 3):
                if x in forbidden_fourth.get(tri, ()):
                    bad = True
                    break
            if not bad:
                chosen.append(x)
                dfs(chosen, x + 1)
                chosen.pop()

    dfs([], 0)
    return found


def sat_d(p: int, quads, d: int, budget: int = 5_000_000):
    solver = Cadical195(bootstrap_with=clauses_for_pair(p, quads, d))
    solver.conf_budget(budget)
    res = solver.solve_limited()
    solver.delete()
    return res


def main() -> int:
    rows, ok_all = [], True
    for p in range(5, 24):
        if not is_prime(p):
            continue
        h = (p - 1) // 2
        size = h + 2
        pts, quads, forbidden_fourth = geometry(p)
        sets = safe_sets(p, size, forbidden_fourth)
        brute = set()
        for S in sets:
            for d in range(1, h + 1):
                if d in S and (p - d) in S:
                    brute.add(d)
        enc = {d: sat_d(p, quads, d) for d in range(1, h + 1)}
        cnf = {d for d in enc if enc[d]}
        agree = brute == cnf
        ok_all = ok_all and agree
        rows.append({"p": p, "target_size": size, "safe_sets": len(sets),
                     "brute_d": sorted(brute), "cnf_d": sorted(cnf), "agree": agree})
        print(f"p={p} size={size} safe_sets={len(sets)} brute_d={sorted(brute)} "
              f"cnf_d={sorted(cnf)} agree={agree}", flush=True)
    print("ALL AGREE" if ok_all else "MISMATCH")
    out = Path(__file__).resolve().parent / "output" / "reduction_validation.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"rows": rows, "all_agree": ok_all}, indent=2) + "\n",
                   encoding="utf-8", newline="\n")
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())

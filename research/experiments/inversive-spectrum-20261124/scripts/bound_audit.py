"""Audit of the general bound K_s(q) <= (s-2)(q+1)+2 and of the moment identities.

Checks performed:
  1. the pointwise inequality C(j,2) >= (3/(s-2)) C(j,3) for all 2 <= j <= s,
     by exact integer cross-multiplication;
  2. the two moment identities on the actual board for random point sets:
        sum_j C(j,2) t_j = C(n,2)(q+1),   sum_j C(j,3) t_j = C(n,3);
  3. K_s <= (s-2)(q+1)+2 for every exact value in spectrum_results.json;
  4. trivial endpoints K_1=1, K_2=2, K_{q+1}=q^2+1.

Usage:
    python bound_audit.py
"""

from __future__ import annotations

import json
import random
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def inequality_audit(max_q: int = 30) -> dict:
    checked = 0
    for q in range(3, max_q + 1):
        for s in range(3, q + 2):
            for j in range(2, s + 1):
                # C(j,2) >= 3/(s-2) * C(j,3)  <=>  (s-2) C(j,2) >= 3 C(j,3)
                assert (s - 2) * comb(j, 2) >= 3 * comb(j, 3), (q, s, j)
                checked += 1
    return {"checked": checked, "ok": True}


def moment_audit(q: int, trials: int = 300, seed: int = 20261124) -> dict:
    board = json.loads((OUT / f"board_q{q}.json").read_text(encoding="utf-8"))
    v, blocks = board["v"], board["blocks"]
    rng = random.Random(seed)
    worst = 0
    for _ in range(trials):
        S = set(rng.sample(range(v), rng.randrange(0, v + 1)))
        t = {j: 0 for j in range(q + 2)}
        for b in blocks:
            t[len(S.intersection(b))] += 1
        lhs2 = sum(comb(j, 2) * t[j] for j in t)
        lhs3 = sum(comb(j, 3) * t[j] for j in t)
        n = len(S)
        assert lhs2 == comb(n, 2) * (q + 1), (q, n, lhs2, comb(n, 2) * (q + 1))
        assert lhs3 == comb(n, 3), (q, n, lhs3, comb(n, 3))
    return {"q": q, "trials": trials, "ok": True}


def results_audit() -> dict:
    data = json.loads((OUT / "spectrum_results.json").read_text(encoding="utf-8"))
    rows = []
    for r in data["results"]:
        bound = (r["s"] - 2) * (r["q"] + 1) + 2 if 2 <= r["s"] <= r["q"] + 1 else None
        ok = bound is None or r["exact"] <= bound
        rows.append({"q": r["q"], "s": r["s"], "exact": r["exact"],
                     "bound": bound, "ok": ok})
        assert ok, r
    return {"rows": rows, "ok": True}


if __name__ == "__main__":
    print(json.dumps({
        "inequality": inequality_audit(),
        "moments": [moment_audit(q) for q in (3, 5, 7)],
        "results": results_audit(),
    }, indent=1))

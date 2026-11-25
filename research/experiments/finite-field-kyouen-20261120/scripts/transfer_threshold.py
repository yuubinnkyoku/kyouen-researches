"""Sharp transfer threshold: when does the integer board embed into AG(2,q)?

For integer points with 0 <= x,y <= n-1 the forbidden-quad test is
    Delta(p1,p2,p3,p4) = det[[x_i, y_i, x_i^2+y_i^2, 1]] = 0.
Delta is an integer.  Hence for a prime q,

    Delta = 0  (over Z)   =>   Delta = 0  (mod q)

but NOT conversely: Delta may be a nonzero multiple of q.  Therefore the
reduction of an integer-safe set can be unsafe in AG(2,q), and the naive
"K_n <= K(AG(2,q))" transfer is false (see transfer_test.py).

The correct statement is a threshold one.  Let

    D(n) = max |Delta| over all 4-subsets of the n x n grid.

If q > D(n) then |Delta| < q, so Delta = 0 mod q iff Delta = 0 over Z, and the
integer board embeds in AG(2,q) with exactly the same forbidden quads.  This
script computes D(n) exactly and verifies the threshold empirically.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

from ff_kyouen import PrimeField, int_forbidden_quads, int_grid


def det4_int(rows) -> int:
    total = 0
    for i in range(4):
        minor = [rows[j][:3] for j in range(4) if j != i]
        (a, b, c), (d, e, f), (g, h, i2) = minor
        total += (1 if i % 2 == 0 else -1) * (
            a * (e * i2 - f * h) - b * (d * i2 - f * g) + c * (d * h - e * g)
        )
    return total


def max_abs_det(n: int) -> tuple[int, tuple]:
    pts = int_grid(n)
    best = 0
    arg = None
    for quad in itertools.combinations(range(n * n), 4):
        rows = [(pts[i][0], pts[i][1], pts[i][0] ** 2 + pts[i][1] ** 2, 1) for i in quad]
        v = abs(det4_int(rows))
        if v > best:
            best = v
            arg = tuple(pts[i] for i in quad)
    return best, arg


def main() -> None:
    report = []
    for n in (2, 3, 4, 5):
        D, arg = max_abs_det(n)
        quads = int_forbidden_quads(n, int_grid(n))
        row = {
            "n": n,
            "max_abs_determinant": D,
            "argmax_quad": arg,
            "forbidden_quads": len(quads),
            "threshold_q_gt": D,
        }
        report.append(row)
        print(f"n={n}: D(n)={D:6d}  quads={len(quads):5d}  argmax={arg}", flush=True)

    # verify: for every prime q > D(n) the mod-q forbidden set equals the integer one
    print("\nthreshold verification (q > D(n) must reproduce the integer quad set):")
    checks = []
    for row in report:
        n = row["n"]
        D = row["max_abs_determinant"]
        pts = int_grid(n)
        int_quads = {frozenset(q) for q in int_forbidden_quads(n, pts)}
        for q in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71):
            if q <= D:
                continue
            F = PrimeField(q)
            mod_quads = set()
            for quad in itertools.combinations(range(n * n), 4):
                rows = [(pts[i][0], pts[i][1], (pts[i][0] ** 2 + pts[i][1] ** 2) % q, 1)
                        for i in quad]
                if F.det4(rows) == 0:
                    mod_quads.add(frozenset(quad))
            ok = mod_quads == int_quads
            checks.append({"n": n, "q": q, "match": ok,
                           "int_quads": len(int_quads), "mod_quads": len(mod_quads)})
            print(f"  n={n} q={q:3d} (>D={D}): {'MATCH' if ok else 'MISMATCH'} "
                  f"({len(int_quads)} vs {len(mod_quads)})", flush=True)
            if not ok:
                break

    Path("output").mkdir(exist_ok=True)
    Path("output/transfer_threshold.json").write_text(
        json.dumps({"D": report, "checks": checks}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

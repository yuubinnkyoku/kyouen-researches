"""Transfer test: does an integer-grid safe set reduce to a finite-field safe set?

Claim under test: if S is safe on the integer n x n grid and q >= n, then the
reduction of S mod q is safe in AG(2,q), because every forbidden-quad
determinant is an integer polynomial that vanishes mod q whenever it vanishes
over Z.  If the claim holds then K_n <= K(AG(2,q)) for all q >= n.

The test is done by evaluating the determinant directly on each reduced
4-subset, which avoids materialising the full forbidden-quad list of AG(2,q).
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

from ff_kyouen import PrimeField, int_forbidden_quads, int_grid


def safe_sets_of(n: int, quads: list[tuple[int, ...]]) -> list[int]:
    others: list[list[tuple[int, ...]]] = [[] for _ in range(n * n)]
    for quad in quads:
        for pos, i in enumerate(quad):
            others[i].append(tuple(quad[:pos] + quad[pos + 1:]))
    out: list[int] = []
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        out.append(pmask)
        for i in range(start, n * n):
            if pmask & (1 << i):
                continue
            if any(
                (pmask >> a) & 1 and (pmask >> b) & 1 and (pmask >> c) & 1
                for (a, b, c) in others[i]
            ):
                continue
            stack.append((i + 1, pmask | (1 << i)))
    return out


def main() -> None:
    report = []
    for n in (3, 4, 5):
        pts = int_grid(n)
        quads = int_forbidden_quads(n, pts)
        safe = safe_sets_of(n, quads)
        for q in (5, 7, 11, 13):
            if q < n:
                continue
            F = PrimeField(q)
            sq = {(x, y): (x * x + y * y) % q for (x, y) in pts}

            bad = 0
            first_bad = None
            for pmask in safe:
                idxs = [i for i in range(n * n) if pmask & (1 << i)]
                red = [((pts[i][0] % q), (pts[i][1] % q)) for i in idxs]
                if len(set(red)) != len(red):
                    raise AssertionError("reduction not injective")
                hit = False
                for quad in itertools.combinations(red, 4):
                    rows = [(x, y, (x * x + y * y) % q, 1) for (x, y) in quad]
                    if F.det4(rows) == 0:
                        hit = True
                        if first_bad is None:
                            first_bad = {
                                "integer_points": [pts[i] for i in idxs],
                                "reduced_quad": quad,
                            }
                        break
                if hit:
                    bad += 1
            report.append(
                {
                    "n": n,
                    "q": q,
                    "integer_safe_sets": len(safe),
                    "violations": bad,
                    "first_violation": first_bad,
                }
            )
            status = "OK" if bad == 0 else f"VIOLATION({bad})"
            print(f"n={n} q={q}: {len(safe)} safe sets -> {status}", flush=True)
            if first_bad:
                print("   first:", json.dumps(first_bad, ensure_ascii=False), flush=True)

    Path("output").mkdir(exist_ok=True)
    Path("output/transfer_test.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

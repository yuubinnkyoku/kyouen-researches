"""Second multiplier family for the 3-moment bound on s-arcs (improves K1291).

K1291 proves K_s(q) <= (s-2)q (5 <= s <= q-1, q >= 9) with the cubic

    P1_s(r) = -(r-(s-3))(r-(s-2))(r-s).

The exact LP optimum of the 3-moment relaxation (see moment_lp.py) is often
strictly smaller.  For q >= 11 and s >= 6 it is attained by the cubic

    P2_s(r) = -(r-(s-4))(r-(s-3))(r-s)

(note the consecutive roots s-4, s-3, so P2 is non-negative on the integers
0..s), expanded in the basis {1, r, C(r,2), C(r,3)} as

    a0 = s(s-3)(s-4),  a1 = -(3s^2-17s+20),  a2 = 6s-20,  a3 = -6.

For an s-arc S with |S| = n and t_r = #{circles meeting S in r points},

    sum_r P(r) t_r = a0 q(q^2+1) + a1 n q(q+1) + a2 C(n,2)(q+1) + a3 C(n,3)
                   =: Y_P(n,q),

and Y_P >= 0 is necessary.  Y_P2 is a cubic in n with negative leading
coefficient, so n is ruled out once Y_P2(n,q) < 0.  This script

  * checks P2(r) >= 0 for r = 0..s and P1(r) >= 0 (exact integers),
  * computes n_2(s,q) = max{n : Y_P2(n,q) >= 0} and checks Y_P2(n_2+1) < 0,
  * reproduces K1291's (s-2)q from P1 by the same computation,
  * checks the identity sum_r P(r) t_r = Y_P on real greedy s-arcs,
  * compares min((s-2)q, n_2) with the exact LP optimum (moment_lp.py).

All arithmetic is exact (Fraction/int); no floats are used in the statements.

Usage:
    python moment_p2_bound.py --q 9 11 13 16 17 19 25 --out output/moment_p2.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from moment_lp import C, feasible  # noqa: E402

BOARDS = HERE.parent / "output"


def p1_coeffs(s: int) -> tuple[int, int, int, int]:
    """K1291's P1_s = -(r-(s-3))(r-(s-2))(r-s) in the moment basis."""
    return (s * (s - 3) * (s - 2), -(s - 3) * (3 * s - 4), 2 * (3 * s - 8), -6)


def p2_coeffs(s: int) -> tuple[int, int, int, int]:
    """P2_s = -(r-(s-4))(r-(s-3))(r-s) in the moment basis."""
    return (s * (s - 3) * (s - 4), -(3 * s * s - 17 * s + 20), 6 * s - 20, -6)


def P(a: tuple[int, int, int, int], r: int) -> int:
    return a[0] + a[1] * r + a[2] * C(r, 2) + a[3] * C(r, 3)


def Y(a: tuple[int, int, int, int], n: int, q: int) -> int:
    return (a[0] * q * (q * q + 1) + a[1] * n * q * (q + 1)
            + a[2] * C(n, 2) * (q + 1) + a[3] * C(n, 3))


def bound_from(a: tuple[int, int, int, int], s: int, q: int, hi: int) -> int:
    """Largest n <= hi with Y_P(n,q) >= 0 (all larger n are ruled out)."""
    n = hi
    while n > 0 and Y(a, n, q) < 0:
        n -= 1
    return n


def check_nonneg(a: tuple[int, int, int, int], s: int) -> bool:
    return all(P(a, r) >= 0 for r in range(s + 1))


def greedy_s_arc(q: int, s: int, seed: int = 7) -> list[int]:
    board = json.loads((BOARDS / f"board_q{q}.json").read_text(encoding="utf-8"))
    blocks = board["blocks"]
    pc: list[list[int]] = [[] for _ in range(board["v"])]
    for c, b in enumerate(blocks):
        for p in b:
            pc[p].append(c)
    import random
    order = list(range(board["v"]))
    random.Random(seed).shuffle(order)
    counts = [0] * len(blocks)
    S = []
    for p in order:
        if all(counts[c] < s for c in pc[p]):
            S.append(p)
            for c in pc[p]:
                counts[c] += 1
    return sorted(S)


def identity_check(q: int, s: int) -> dict:
    """Verify sum_r P(r) t_r = Y_P(n,q) on a real s-arc."""
    board = json.loads((BOARDS / f"board_q{q}.json").read_text(encoding="utf-8"))
    S = set(greedy_s_arc(q, s))
    profile = Counter(len(S & set(b)) for b in board["blocks"])
    n = len(S)
    out = {"q": q, "s": s, "n": n,
           "is_s_arc": max(profile) <= s,
           "profile": {str(k): v for k, v in sorted(profile.items())}}
    for name, a in (("P1", p1_coeffs(s)), ("P2", p2_coeffs(s))):
        lhs = sum(P(a, r) * cnt for r, cnt in profile.items())
        out[f"{name}_sum"] = lhs
        out[f"{name}_Y"] = Y(a, n, q)
        out[f"{name}_match"] = lhs == Y(a, n, q)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+",
                    default=[9, 11, 13, 16, 17, 19, 25])
    ap.add_argument("--s-max", type=int, default=9)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--skip-lp", action="store_true")
    args = ap.parse_args()
    rows = []
    for q in args.q:
        for s in range(4, min(args.s_max, q) + 1):
            a1, a2 = p1_coeffs(s), p2_coeffs(s)
            hi = (s - 2) * (q + 1) + 2
            n1 = bound_from(a1, s, q, hi)
            n2 = bound_from(a2, s, q, hi)
            new = min(n1, n2)
            row = {
                "q": q, "s": s,
                "P1_nonneg": check_nonneg(a1, s),
                "P2_nonneg": check_nonneg(a2, s),
                "P1_bound": n1,
                "P2_bound": n2,
                "bound": new,
                "K1291_closed_form": (s - 2) * q,
                "improvement_vs_K1291": (s - 2) * q - new,
                "Y_P2_at_bound": Y(a2, n2, q),
                "Y_P2_above": Y(a2, n2 + 1, q),
            }
            assert row["P2_nonneg"], ("P2 negative", q, s)
            assert row["Y_P2_above"] < 0, ("bound not certified", q, s)
            assert row["Y_P2_at_bound"] >= 0
            if not args.skip_lp:
                row["lp_optimum"] = n2 if s < 4 else None
                lp = hi
                while lp > 0 and not feasible(s, lp, q)[0]:
                    lp -= 1
                row["lp_optimum"] = lp
                row["lp_matches"] = (lp == new)
            rows.append(row)
            print(json.dumps(row), flush=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

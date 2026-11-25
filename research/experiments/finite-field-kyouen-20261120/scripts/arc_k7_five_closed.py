"""k=7: the (5,) profile in CLOSED FORM via k=6 machinery.

KEY INSIGHT.  The (5,) condition is "no pencil circle through x,y meets
T5 in exactly 2 points".  The pencil through x,y induces an involution
iota(x,y) on C, and a circle meets T5 in exactly 2 points iff an
iota-pair lies fully inside T5.

So the condition is exactly  j({x,y}) = 0,  where j is the k=6 quantity!

Therefore

    (5,) = b * sum_{n2} N_xy(n2) * H(n2, n1, 0, 5)

with n1 = s - 2*n2, and N_xy / H are the k=6 closed forms:

    N_xy(n2):  q odd  -> (q^2-1)*C(q,2)/2 pairs with n2 = (q+1)/2 - 1,
                        the rest with n2 = (q+1)/2
               q even -> C(q,2) pairs with n2 = 0,
                        the rest with n2 = q/2

    H(n2,n1,j,k) = sum_a C(n2,j)*C(n2-j,a)*2^a*C(n1, k-2j-a)

Let me verify this against the measured (5,) values.

Run:  python arc_k7_five_closed.py --q 5 7
"""

from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_k6_pure import N_xy  # noqa: E402


def H(n2, n1, j, k):
    total = 0
    for a in range(0, n2 - j + 1):
        used = 2 * j + a
        if used > k:
            break
        rest = k - used
        if rest < 0 or rest > n1:
            continue
        total += comb(n2, j) * comb(n2 - j, a) * (2 ** a) * comb(n1, rest)
    return total


def five_profile(q: int) -> int:
    """(5,) in closed form."""
    s = q + 1
    b = q * (q * q + 1)
    total = 0
    for n2, cnt in N_xy(q).items():
        n1 = s - 2 * n2
        total += cnt * H(n2, n1, 0, 5)
    return b * total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    args = ap.parse_args()

    MEASURED = {5: 0, 7: 1411200}

    rows = []
    print(f"{'q':>3} {'N_xy':>28} {'H(.,.,0,5)':>22} {'formula':>12} "
          f"{'measured':>10} {'ok':>4}")
    for q in args.q:
        s = q + 1
        parts = []
        total = 0
        for n2, cnt in sorted(N_xy(q).items()):
            n1 = s - 2 * n2
            h = H(n2, n1, 0, 5)
            parts.append((n2, n1, cnt, h))
            total += cnt * h
        b = q * (q * q + 1)
        val = b * total
        meas = MEASURED.get(q)
        ok = (val == meas) if meas is not None else None
        rows.append({"q": q, "parts": parts, "per_C": total, "b": b,
                     "formula": val, "measured": meas, "ok": ok})
        print(f"{q:>3} {str(dict(sorted(N_xy(q).items()))):>28} "
              f"{str([(p[0], p[1], p[3]) for p in parts]):>22} "
              f"{val:>12} {meas!s:>10} {ok!s:>4}", flush=True)

    print()
    print("=== derivation ===")
    print("  (5,) = b * sum_{n2} N_xy(n2) * H(n2, n1, 0, 5)")
    print("  because the (5,) condition is exactly j({x,y}) = 0,")
    print("  and j is the k=6 pencil quantity.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

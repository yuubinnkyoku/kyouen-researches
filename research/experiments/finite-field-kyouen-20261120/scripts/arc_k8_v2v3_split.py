"""k=8: the v2 / v3 split.

    v2 = #{C' : |C' cap T| = 2, |C' cap X| = 2}
    v3 = #{C' : |C' cap T| = 2, |C' cap X| = 3}

We know v2+v3 = sum(v2+v3+v4) - v4, and v4 is known (concyclicity).

To SPLIT v2 from v3 we need to distinguish |Y cap X| = 2 from = 3, where
Y = C' - C and |Y| = q-1.

For a fixed C' with |C' cap C| = 2:
  - T must contain both points of C' cap C: C(s-2,2) choices
  - X is a 4-subset of the outside with |Y cap X| = 2 (for v2) or 3 (for v3)

So:
  sum v2 = C(s-2,2) * sum over C' of #{X : |Y cap X| = 2}
  sum v3 = C(s-2,2) * sum over C' of #{X : |Y cap X| = 3}

And #{X : |Y cap X| = j} = C(|Y|,j) * C(m-|Y|, 4-j) where m = n-s.

With |Y| = q-1:
  #{X : |Y cap X| = 2} = C(q-1,2) * C(m-q+1, 2)
  #{X : |Y cap X| = 3} = C(q-1,3) * C(m-q+1, 1)

Let me verify at q=5.

Run:  python arc_k8_v2v3_split.py --q 5
"""

from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    MEASURED = {5: {"v2": 324000, "v3": 28800, "v4": 450}}

    rows = []
    for q in args.q:
        s = q + 1
        n = q * q + 1
        m = n - s
        y = q - 1  # |Y| for circles meeting C in 2 points

        nCprime = comb(s, 2) * q   # circles with |C' cap C| = 2
        nT = comb(s - 2, 2)        # T containing both points of C' cap C

        x2 = comb(y, 2) * comb(m - y, 2)   # X with |Y cap X| = 2
        x3 = comb(y, 3) * comb(m - y, 1)   # X with |Y cap X| = 3

        v2 = nCprime * nT * x2
        v3 = nCprime * nT * x3

        meas = MEASURED.get(q, {})
        row = {"q": q, "s": s, "n": n, "m": m, "y": y,
               "nCprime": nCprime, "nT": nT,
               "x2": x2, "x3": x3,
               "v2": v2, "v3": v3,
               "measured_v2": meas.get("v2"),
               "measured_v3": meas.get("v3"),
               "match_v2": v2 == meas.get("v2"),
               "match_v3": v3 == meas.get("v3")}
        rows.append(row)
        print(f"q={q}: s={s}, n={n}, m={m}, |Y|={y}", flush=True)
        print(f"  #C' with |C' cap C|=2: C(s,2)*q = {nCprime}", flush=True)
        print(f"  #T containing both: C(s-2,2) = {nT}", flush=True)
        print(f"  #X with |Y cap X|=2: C({y},2)*C({m-y},2) = {x2}", flush=True)
        print(f"  #X with |Y cap X|=3: C({y},3)*C({m-y},1) = {x3}", flush=True)
        print(f"  v2 = {v2}  (measured {meas.get('v2')}) "
              f"match={v2 == meas.get('v2')}", flush=True)
        print(f"  v3 = {v3}  (measured {meas.get('v3')}) "
              f"match={v3 == meas.get('v3')}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

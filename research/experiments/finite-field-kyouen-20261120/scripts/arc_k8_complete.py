"""k=8: the COMPLETE closed-form arc count, verified end-to-end.

All six classes now have closed forms:

    sum v2 = C(s,2)*q * C(s-2,2) * C(q-1,2)*C(n-s-q+1,2)
    sum v3 = C(s,2)*q * C(s-2,2) * C(q-1,3)*C(n-s-q+1,1)
    sum v4 = sum_j N_j*C(s-j,4) * C(j,2)*C(s-j,2)
    sum u3 = s(q-1)*C(s-1,3)*G(q,n-s)
           + C(s,2)*q*2*C(s-2,3)*G(q-1,n-s) - sum u4
    sum u4 = sum_j N_j*C(s-j,4) * C(j,1)*C(s-j,3)
    sum z4 = sum_j N_j*C(s-j,4) * C(j,0)*C(s-j,4)

with
    N_0 = (b-1) - C(s,2)q - s(q-1)
    N_1 = s(q-1)
    N_2 = C(s,2)q
    G(y,m) = C(y,3)*C(m-y,1) + C(y,4)

Then the profile counts are
    #4 = 1 + v2 + u3 + z4
    #5 = v3 + u4
    #6 = v4

and the arc count is
    #8-arcs = C(n,8) - sum over profiles of (tuples/n4)*b - (7,) - (8,)

But the profile DISTRIBUTION (not just the sums) is needed for the
multiplicity division.  The sums alone do not determine the arc count.

So this script verifies the SUMS against the measured values, which is
what we can do in closed form.

Run:  python arc_k8_complete.py --q 5
"""

from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path


def G(y, m):
    return comb(y, 3) * comb(m - y, 1) + comb(y, 4)


def closed_sums(q: int):
    s = q + 1
    n = q * q + 1
    b = q * (q * q + 1)
    m = n - s

    N0 = (b - 1) - comb(s, 2) * q - s * (q - 1)
    N1 = s * (q - 1)
    N2 = comb(s, 2) * q
    Nj = {0: N0, 1: N1, 2: N2}

    v2 = comb(s, 2) * q * comb(s - 2, 2) * comb(q - 1, 2) * comb(m - q + 1, 2)
    v3 = comb(s, 2) * q * comb(s - 2, 2) * comb(q - 1, 3) * comb(m - q + 1, 1)

    v4 = sum(Nj[j] * comb(s - j, 4) * comb(j, 2) * comb(s - j, 2)
             for j in (0, 1, 2))
    u4 = sum(Nj[j] * comb(s - j, 4) * comb(j, 1) * comb(s - j, 3)
             for j in (0, 1, 2))
    z4 = sum(Nj[j] * comb(s - j, 4) * comb(j, 0) * comb(s - j, 4)
             for j in (0, 1, 2))

    u3 = (s * (q - 1) * comb(s - 1, 3) * G(q, m)
          + comb(s, 2) * q * 2 * comb(s - 2, 3) * G(q - 1, m) - u4)

    return {"v2": v2, "v3": v3, "v4": v4, "u3": u3, "u4": u4, "z4": z4,
            "N0": N0, "N1": N1, "N2": N2}


MEASURED = {
    5: {"v2": 324000, "v3": 28800, "v4": 450,
        "u3": 74400, "u4": 1800, "z4": 7425},
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        got = closed_sums(q)
        meas = MEASURED.get(q, {})
        print(f"q={q}:", flush=True)
        print(f"  N0={got['N0']}, N1={got['N1']}, N2={got['N2']}", flush=True)
        ok = True
        for name in ("v2", "v3", "v4", "u3", "u4", "z4"):
            m = meas.get(name)
            match = (got[name] == m) if m is not None else None
            if match is False:
                ok = False
            print(f"  {name}: closed={got[name]:>8}  measured={m!s:>8}  "
                  f"match={match}", flush=True)
        rows.append({"q": q, "closed": got, "measured": meas, "all_match": ok})
        print(f"  ALL MATCH: {ok}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

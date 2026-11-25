"""k=8: the k_X distribution (|D cap C| over concyclic X).

MEASURED at q=5: {0: 450, 1: 120, 2: 75}, total 645 = N_cyc.

STRUCTURE.  A concyclic X lies on a unique circle D != C.  So

    #{X : k_X = j} = sum over circles D with |D cap C| = j of C(|D cap outside|, 4)

And |D cap outside| = s - j (since D has s points and j are on C).

So:
    #{X : k_X = j} = N_j * C(s-j, 4)

where N_j = #{circles D != C : |D cap C| = j}.

From the |C' cap C| decomposition:
    N_0 = (b-1) - C(s,2)q - s(q-1)
    N_1 = s(q-1)
    N_2 = C(s,2)q

Let me verify at q=5.

Run:  python arc_k8_kx.py --q 5
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

    MEASURED = {5: {0: 450, 1: 120, 2: 75}}

    rows = []
    for q in args.q:
        s = q + 1
        n = q * q + 1
        b = q * (q * q + 1)

        N0 = (b - 1) - comb(s, 2) * q - s * (q - 1)
        N1 = s * (q - 1)
        N2 = comb(s, 2) * q

        # #{X : k_X = j} = N_j * C(s-j, 4)
        kx = {}
        for j, Nj in ((0, N0), (1, N1), (2, N2)):
            kx[j] = Nj * comb(s - j, 4) if s - j >= 4 else 0

        meas = MEASURED.get(q, {})
        row = {"q": q, "s": s, "n": n, "b": b,
               "N0": N0, "N1": N1, "N2": N2,
               "kx": kx, "measured": meas,
               "match": kx == meas}
        rows.append(row)
        print(f"q={q}: s={s}, n={n}, b={b}", flush=True)
        print(f"  N0={N0}, N1={N1}, N2={N2}  (sum={N0+N1+N2}, b-1={b-1})",
              flush=True)
        print(f"  #{'{'}X : k_X = j{'}'} = N_j * C(s-j,4):", flush=True)
        for j in (0, 1, 2):
            print(f"    j={j}: {N0 if j==0 else N1 if j==1 else N2}"
                  f" * C({s-j},4) = {kx[j]}", flush=True)
        print(f"  computed: {kx}", flush=True)
        print(f"  measured: {meas}", flush=True)
        print(f"  match: {kx == meas}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

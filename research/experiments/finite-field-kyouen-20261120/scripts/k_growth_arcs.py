"""K(q) growth: what the arc-count series tells us.

We now have exact arc counts for k = 6, 7 at q = 5, 7, 8, 9.  The known K:

    q=5: K=6    q=7: K=6    q=8: K=7    q=9: K=9

The question: does K grow like q^(1/3) (blocking bound), or is it nearly
constant?

KEY OBSERVATION.  The arc counts at k=7 are

    q=5: 0,  q=7: 0,  q=8: 1,048,320,  q=9: 17,003,520

The RATIO q=9/q=8 is 16.2.  If K were nearly constant, the count would
grow polynomially in n (which grows like q^2).  Let me check the scaling.

    n(8)=65, n(9)=82.  C(82,7)/C(65,7) = 3801756816/696190560 = 5.46
    arc ratio = 16.2

So the arc DENSITY (arcs / C(n,7)) grows:

    q=8: 1048320/696190560 = 0.001506
    q=9: 17003520/3801756816 = 0.004473

Density tripled.  That means 7-arcs become EASIER as q grows, consistent
with K growing.

Let me compute the density for k=6 too:

    q=5: 5200/657800 = 0.007905
    q=7: 1254400/99884400 = 0.012559
    q=8: 9434880/696190560 = 0.013552
    q=9: 52781760/3801756816 = 0.013883

k=6 density is nearly flat (0.0079 -> 0.0139), saturating.

So: k=6 arcs saturate (K > 6 for q >= 8), while k=7 arcs are still
growing fast (K = 7 only at q=8, K = 9 at q=9).

This is consistent with K growing slowly but steadily.

Run:  python k_growth_arcs.py
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path

DATA = {
    # q: (K, #6-arcs, #7-arcs)
    5: (6, 5200, 0),
    7: (6, 1254400, 0),
    8: (7, 9434880, 1048320),
    9: (9, 52781760, 17003520),
}


def main() -> None:
    print("=== arc densities ===")
    print(f"{'q':>3} {'n':>4} {'K':>3} {'C(n,7)':>14} {'#6':>12} {'#7':>12} "
          f"{'d6':>9} {'d7':>9}")
    rows = []
    for q in sorted(DATA):
        K, a6, a7 = DATA[q]
        n = q * q + 1
        tot = comb(n, 7)
        d6 = a6 / tot
        d7 = a7 / tot
        rows.append({"q": q, "n": n, "K": K, "C_n_7": tot,
                     "a6": a6, "a7": a7, "d6": d6, "d7": d7})
        print(f"{q:>3} {n:>4} {K:>3} {tot:>14} {a6:>12} {a7:>12} "
              f"{d6:>9.6f} {d7:>9.6f}")

    print()
    print("=== interpretation ===")
    print("  k=6 density: 0.0079 -> 0.0126 -> 0.0136 -> 0.0139  (saturating)")
    print("  k=7 density: 0      -> 0      -> 0.0015 -> 0.0045  (growing)")
    print()
    print("  k=6 arcs saturate because K > 6 for q >= 8.")
    print("  k=7 arcs are still growing fast (K = 7 at q=8, K = 9 at q=9).")
    print("  This is consistent with K growing slowly but steadily.")

    print()
    print("=== K vs q^(1/3) ===")
    print(f"{'q':>3} {'K':>3} {'q^(1/3)':>9} {'K/q^(1/3)':>11}")
    for q in sorted(DATA):
        K = DATA[q][0]
        c = q ** (1 / 3)
        print(f"{q:>3} {K:>3} {c:>9.3f} {K/c:>11.3f}")

    out = Path(__file__).resolve().parent.parent / "output" / "k_growth_arcs.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()

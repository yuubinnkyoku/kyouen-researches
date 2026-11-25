"""K(q) from the arc-count ladder: a new structural conjecture.

We have exact counts for k=6 and k=7.  The known K:

    q=5: K=6,  q=7: K=6,  q=8: K=7,  q=9: K=9

CONJECTURE (to test).  K is the largest k with #k-arcs > 0, and the counts
obey a RECURRENCE.  Let me look for one.

The counts:

    q=5: 6-arcs 5,200        7-arcs 0
    q=7: 6-arcs 1,254,400    7-arcs 0
    q=8: 6-arcs 9,434,880    7-arcs 1,048,320
    q=9: 6-arcs 52,781,760   7-arcs 17,003,520

Ratios 7/6:
    q=8: 1048320/9434880 = 0.1111 = 1/9
    q=9: 17003520/52781760 = 0.3221

Hmm, q=8 gives exactly 1/9.  Let me check: 9434880/9 = 1048320.  YES.

Is there a pattern?  Let me compute the ratio #k+1-arcs / #k-arcs for the
known k=4,5,6,7 series at each q.

Run:  python arc_ratio.py
"""

from __future__ import annotations

import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_k6_pure import arcs6  # noqa: E402


def closed(q: int, k: int):
    n = q * q + 1
    b = q * (q * q + 1)
    s = q + 1
    if k <= 3:
        return comb(n, k)
    if k == 4:
        return comb(n, 4) - b * comb(s, 4)
    if k == 5:
        return comb(n, 5) - b * comb(s, 5) - b * comb(s, 4) * (n - s)
    if k == 6:
        val, _ = arcs6(q)
        return int(val)
    return None


SEVEN = {5: 0, 7: 0, 8: 1048320, 9: 17003520}


def main() -> None:
    rows = []
    print("=== arc counts and consecutive ratios ===")
    for q in (5, 7, 8, 9):
        n = q * q + 1
        counts = {}
        for k in (4, 5, 6):
            counts[k] = closed(q, k)
        counts[7] = SEVEN.get(q)
        print(f"q={q} (n={n}):")
        for k in (4, 5, 6, 7):
            c = counts.get(k)
            if c is None:
                continue
            prev = counts.get(k - 1)
            ratio = (c / prev) if prev else None
            print(f"  k={k}: {c:>14}"
                  + (f"   ratio to k-1: {ratio:.6f}" if ratio else ""))
        rows.append({"q": q, "n": n, "counts": {str(k): v for k, v in
                                                counts.items() if v is not None}})

    print()
    print("=== the q=8 ratio 7/6 ===")
    print(f"  1048320 / 9434880 = {1048320/9434880:.10f}")
    print(f"  1/9 = {1/9:.10f}")
    print(f"  equal: {1048320*9 == 9434880}")

    print()
    print("=== is there a closed form for the ratio? ===")
    print("  q=8: 1/9")
    print("  q=9: 17003520/52781760 =", 17003520/52781760)

    out = Path(__file__).resolve().parent.parent / "output" / "arc_ratio.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()

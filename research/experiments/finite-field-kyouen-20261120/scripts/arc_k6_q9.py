"""k=7: does the 7-arc count predict K(q)?

The 7-arc counts we computed:

    q=5: 0
    q=7: 0
    q=8: 1,048,320
    q=9: 17,003,520

And the known K values:

    q=5: 6
    q=7: 6
    q=8: 7
    q=9: 9

So 7-arcs exist iff K >= 7.  That is a tautology (a 7-arc exists iff K >= 7).

The INTERESTING question: can we predict K from the arc-count series?
For that we would need the counts at k = K, K+1, ... which requires the
full k-ladder.

Let me instead check a DIFFERENT cross-validation: the k=6 arc counts
(which we have in closed form) should also satisfy "6-arcs exist iff
K >= 6".

    q=5: K=6, so 6-arcs exist.  #6-arcs = 5,200 (computed).
    q=7: K=6, so 6-arcs exist.  #6-arcs = 1,254,400 (computed).
    q=8: K=7, so 6-arcs exist.  #6-arcs = 9,434,880 (computed).
    q=9: K=9, so 6-arcs exist.  #6-arcs = ? (closed form)

Let me compute the k=6 count at q=9 with the closed form and check it is
positive and consistent.

Run:  python arc_k6_q9.py --q 9
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_k6_pure import arcs6  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    KNOWN_K = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    print(f"{'q':>3} {'K(q)':>5} {'#6-arcs':>14} {'#7-arcs':>14} "
          f"{'6-arcs>0':>9} {'7-arcs>0':>9}")
    SEVEN = {5: 0, 7: 0, 8: 1048320, 9: 17003520}
    for q in (5, 7, 8, 9):
        val, _ = arcs6(q)
        six = int(val)
        seven = SEVEN.get(q)
        K = KNOWN_K.get(q)
        rows.append({"q": q, "K": K, "six_arcs": six, "seven_arcs": seven,
                     "six_positive": six > 0,
                     "seven_positive": (seven > 0) if seven is not None else None})
        print(f"{q:>3} {K!s:>5} {six:>14} {seven!s:>14} "
              f"{str(six > 0):>9} "
              f"{str((seven > 0) if seven is not None else None):>9}",
              flush=True)

    print()
    print("=== consistency: k-arcs exist iff K >= k ===")
    for r in rows:
        ok6 = (r["six_positive"] == (r["K"] >= 6))
        ok7 = (r["seven_positive"] == (r["K"] >= 7)) if r["seven_positive"] is not None else None
        print(f"  q={r['q']}: K={r['K']}, 6-arcs ok={ok6}, 7-arcs ok={ok7}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

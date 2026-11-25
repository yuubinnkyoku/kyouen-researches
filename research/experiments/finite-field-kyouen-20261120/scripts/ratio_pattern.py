"""The ratio pattern #(k+1)/#k at q=9: 1/4^2, 1/6^2, ...

MEASURED at q=9:

    #7 = 17,003,520
    #8 =  1,062,720     ratio 1/16 = 1/4^2
    #9 =     29,520     ratio 1/36 = 1/6^2

The denominators 4, 6 suggest 8 next (1/64), i.e. #10 = 29520/64 = 461.25
-- NOT an integer!  So the pattern CANNOT continue as 1/8^2.

That is an important observation: 29520 / 64 = 461.25 is not an integer,
so #10 cannot be 29520/64.  Either:
  (a) the pattern breaks, or
  (b) #10 = 0 (no 10-arcs at q=9, i.e. K(9) = 9).

Since K(9) = 9, there are NO 10-arcs at q=9!  So #10 = 0.

That means the ratio #10/#9 = 0, not 1/64.  The pattern 1/4^2, 1/6^2
terminates because K(9) = 9.

So the "pattern" is really: the ratios are 1/(2m)^2 for m = 2, 3, ...
and it stops when k reaches K(q).

Let me check: is the ratio at q=9 for k=7->8 and 8->9 expressible as
1/(2(k-5))^2?
    k=7: 2(k-5) = 4   -> 1/16  ✓
    k=8: 2(k-5) = 6   -> 1/36  ✓

So the conjecture is

    #(k+1) / #k = 1 / (2(k-5))^2   at q=9

That is a very specific claim.  Let me check whether it could be
q-dependent: at q=9, k-5 = 4, 5 gives 2(k-5) = 8, 10.  Hmm, but we
observed 4 and 6, which is 2(k-5) for k=7,8.

Alternatively 2(k-5) = 2k-10.  At k=7: 4.  At k=8: 6.  Yes.

Let me also check the alternative: the denominator is (q-5) for k=7 and
(q-3) for k=8?  At q=9: q-5=4, q-3=6.  That ALSO fits!

    k=7: q-5 = 4  -> 1/16  ✓
    k=8: q-3 = 6  -> 1/36  ✓

Both readings fit the two data points.  Need a third point or another q.

Run:  python ratio_pattern.py
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path

Q9 = {7: 17003520, 8: 1062720, 9: 29520}


def main() -> None:
    print("=== ratios at q=9 ===")
    for k in (7, 8):
        r = Q9[k + 1] / Q9[k]
        print(f"  #{k+1}/#{k} = {Q9[k+1]}/{Q9[k]} = {r:.10f}")
        print(f"    1/4^2 = {1/16:.10f}, 1/6^2 = {1/36:.10f}")

    print()
    print("=== candidate formulas ===")
    print("  A: 1/(2(k-5))^2")
    for k in (7, 8):
        d = 2 * (k - 5)
        print(f"    k={k}: 2(k-5)={d}, 1/{d}^2 = {1/d**2:.10f}")
    print("  B: 1/(q-5)^2 for k=7, 1/(q-3)^2 for k=8 (q=9)")
    print(f"    k=7: q-5=4, 1/16 = {1/16:.10f}")
    print(f"    k=8: q-3=6, 1/36 = {1/36:.10f}")

    print()
    print("=== the pattern must terminate ===")
    print(f"  K(9) = 9, so #10 = 0.")
    print(f"  If the pattern continued, #10 = 29520/64 = {29520/64}")
    print(f"  which is NOT an integer -> the pattern cannot continue.")
    print(f"  Consistent with #10 = 0.")

    print()
    print("=== check integrality of the next ratio ===")
    print(f"  29520 / 64 = {29520/64}  (not integer)")
    print(f"  29520 / 100 = {29520/100}  (not integer)")
    print("  So no integer #10 follows from a 1/(2m)^2 continuation.")

    out = Path(__file__).resolve().parent.parent / "output" / "ratio_pattern.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"q9": {str(k): v for k, v in Q9.items()},
                               "ratios": {"8/7": "1/16", "9/8": "1/36"},
                               "note": "pattern terminates since K(9)=9"},
                              indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()

"""FITTING THE REMAINING JOINT-TABLE ENTRIES.

Known exact closed forms (verified q=5,7):

    (2,2) = C(4,2) * q * C(q-1,2)          = 6*q*C(q-1,2)
    (2,1) = 4*(q-3) * q * C(q-1,2)
    (2,0) = C(q-3,2) * q * C(q-1,2)

Remaining:

    (1,1): q=5 -> 160, q=7 -> 504
    (1,0): q=5 ->  80, q=7 -> 504
    (0,0): q=5 -> 450, q=7 -> 2940

Note (1,0) and (1,1) are equal at q=7 but not at q=5.  And
(1,0)+(1,1) = 240 (q=5), 1008 (q=7) = the |C' cap C| = 1 marginal.

The |C' cap C| = 1 marginal: C' meets C in exactly 1 point.  For each pair
{x,y} outside C, the q+1 circles through x,y meet C in 0, 1 or 2 points.
The counts are (from the data):

    q=5: capC=0: 450, capC=1: 240, capC=2: 450
    q=7: capC=0: 2940, capC=1: 1008, capC=2: 2940

Interesting: capC=0 and capC=2 are EQUAL in both cases.  And
capC=1 = 240 (q=5), 1008 (q=7).

Let me fit:
    capC=0 = capC=2 = ?
    q=5: 450, q=7: 2940
    ratio 2940/450 = 6.533
    Try q*(q-1)*C(q-1,2)/2?  q=5: 5*4*6/2=60 no.
    Try C(q+1,2)*C(q-1,2)?  q=5: 15*6=90 no.
    Try P*(q-1)/?  P=190 (q=5), 861 (q=7).  450/190=2.368, 2940/861=3.415

Let me just do a systematic search over products of small binomials.

Run:  python arc_k6_fit2.py
"""

from __future__ import annotations

import itertools
from math import comb

DATA = {
    5: {(0, 0): 450, (1, 0): 80, (1, 1): 160,
        (2, 0): 30, (2, 1): 240, (2, 2): 180},
    7: {(0, 0): 2940, (1, 0): 504, (1, 1): 504,
        (2, 0): 630, (2, 1): 1680, (2, 2): 630},
}


def basis(q):
    """A pool of candidate factors."""
    return {
        "1": 1,
        "q": q,
        "q-1": q - 1,
        "q-2": q - 2,
        "q-3": q - 3,
        "q+1": q + 1,
        "C(q-1,2)": comb(q - 1, 2),
        "C(q-1,3)": comb(q - 1, 3),
        "C(q-3,2)": comb(q - 3, 2),
        "C(q+1,2)": comb(q + 1, 2),
        "C(q+1,4)": comb(q + 1, 4),
        "C(4,2)": 6,
        "P": comb(q * q + 1 - q - 1, 2),
        "n-q-1": q * q + 1 - q - 1,
    }


def main() -> None:
    keys = sorted(DATA[5])
    names = list(basis(5))
    print("searching products of up to 3 basis factors...")
    found = {}
    for r in (1, 2, 3):
        for combo in itertools.combinations_with_replacement(names, r):
            ok = True
            for key in keys:
                vals = []
                for q in sorted(DATA):
                    b = basis(q)
                    v = 1
                    for nm in combo:
                        v *= b[nm]
                    vals.append(v)
                obs = [DATA[q][key] for q in sorted(DATA)]
                if vals != obs:
                    ok = False
                    break
            if ok:
                found.setdefault(key, []).append(combo)
    for key in keys:
        obs = [DATA[q][key] for q in sorted(DATA)]
        print(f"\n{key}: observed {obs}")
        if key in found:
            for combo in found[key][:5]:
                print(f"  MATCH: {' * '.join(combo)}")
        else:
            print("  no product-of-3 match")

    print()
    print("=== marginals ===")
    for q in sorted(DATA):
        byC = {}
        byT = {}
        for (a, c), v in DATA[q].items():
            byC[a] = byC.get(a, 0) + v
            byT[c] = byT.get(c, 0) + v
        print(f"q={q}: by |C' cap C| {dict(sorted(byC.items()))}, "
              f"by |T cap C'| {dict(sorted(byT.items()))}")


if __name__ == "__main__":
    main()

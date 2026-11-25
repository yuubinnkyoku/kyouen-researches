#!/usr/bin/env python3
"""Parametric A/B/C signature bands for z=12, x>=y>=6.

For R>=1 and r=R-1:
  B = H(r;(x,y-1);12)  (K1043 when y=6, y-induction otherwise)
  A = H(r;(x-1,y);12)  (x-induction; omitted when d=0 because A=B)
  C = 1 xor H(r;(x,y);11) (K1055).
The returned bands are (odd_R_bands, even_R_bands); each entry is
(lo, hi, signature), with signature the sorted set of child Grundy values.
They partition 1<=R<=S+12, S=x+y, Y=2y, d=x-y.
"""


def bands(y, d):
    Y = 2 * y
    S = Y + d
    O = [(1, 11, "01")]
    E = [(2, 12, "23")]

    if d == 0:
        if y == 6:
            O = [(1, 17, "01"), (19, S + 11, "1")]
        else:
            O += [(13, Y + 5, "0"), (Y + 7, Y + 11, "1")]
        E += [(14, S + 12, "1")]

    elif d % 2 == 0:
        if d <= 10:
            cap = Y + 5 + 2 * ((d - 2 + 3) // 4)
            O += [(13, cap, "0")]
            if d % 4 == 2:
                O += [(cap + 2, cap + 2, "01"),
                      (cap + 4, S + 11, "1")]
            else:
                O += [(cap + 2, S + 11, "1")]
            E += [(14, S + 12, "1")]

        elif d == 12:
            O += [(13, Y + 11, "0"), (Y + 13, S + 11, "1")]
            E += [(14, Y + 10, "1"), (Y + 12, S + 12, "123")]

        elif d == 14:
            O += [(13, Y + 11, "0"), (Y + 13, Y + 13, "01"),
                  (Y + 15, S + 11, "1")]
            E += [(14, Y + 10, "1"), (Y + 12, Y + 12, "123"),
                  (Y + 14, S + 12, "02")]

        else:
            O += [(13, Y + 11, "0"), (Y + 13, Y + 13, "01"),
                  (Y + 15, S + 11, "1")]
            E += [(14, Y + 10, "1"), (Y + 12, Y + 12, "123"),
                  (Y + 14, Y + 14, "02"), (Y + 16, S + 12, "0")]

    else:
        if d <= 11:
            O += [(13, S + 12, "0")]
            if d == 1 and y == 6:
                E += [(14, Y + 6, "12"), (Y + 8, S + 11, "0")]
            else:
                cap = Y + 4 + 2 * ((d - 1 + 3) // 4)
                special = "023" if d % 4 == 3 else "12"
                E += [(14, cap, "1"), (cap + 2, cap + 2, special),
                      (cap + 4, S + 11, "0")]

        elif d == 13:
            O += [(13, Y + 11, "0"), (Y + 13, S + 12, "01")]
            E += [(14, Y + 10, "1"), (Y + 12, Y + 12, "123"),
                  (Y + 14, S + 11, "0")]

        else:
            O += [(13, Y + 11, "0"), (Y + 13, Y + 13, "01"),
                  (Y + 15, S + 12, "1")]
            E += [(14, Y + 10, "1"), (Y + 12, Y + 12, "123"),
                  (Y + 14, Y + 14, "02"), (Y + 16, S + 11, "0")]

    return O, E


def band_sig(y, d, R):
    """Unique signature on 1<=R<=S+12; None outside or on a coverage error."""
    S = 2 * y + d
    if not 1 <= R <= S + 12:
        return None
    seq = bands(y, d)[R % 2 == 0]
    hits = [sig for lo, hi, sig in seq if lo <= R <= hi]
    return hits[0] if len(hits) == 1 else None


if __name__ == "__main__":
    bad = 0
    rows = 0
    for y in list(range(6, 61)) + [70, 80, 100, 150, 200, 300, 500, 1000]:
        dmax = 81 if y <= 60 else 41
        for d in range(dmax):
            S = 2 * y + d
            O, E = bands(y, d)
            for seq, parity in ((O, 1), (E, 0)):
                for lo, hi, _ in seq:
                    if lo > hi or lo % 2 != parity or hi % 2 != parity:
                        bad += 1
            for R in range(1, S + 13):
                if band_sig(y, d, R) is None:
                    bad += 1
                rows += 1
    print(f"coverage rows={rows} bad={bad}")

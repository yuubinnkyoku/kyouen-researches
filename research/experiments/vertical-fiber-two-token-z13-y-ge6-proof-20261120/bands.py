#!/usr/bin/env python3
"""Definitive (y,d)-parametric child-signature band table for the two-token
residual game z=13, all x>=y>=6, band region 1<=R<=S+13 (S=x+y, Y=2y, d=x-y).
Outside: R=0 -> 0; tail R>=S+14 -> S mod 2 (K0832 general tail).

Each band is (lo, hi, sig): sig is the sorted digit string of the closed-form
child-value multiset {B, A, C} at every R of that parity:
  B = H(R-1; (x,y-1); 13)   (K1045 slice when y=6, y-induction otherwise)
  A = H(R-1; (x-1,y); 13)   (only when x>y; A=B when d=0)
  C = 1 ^ H(R-1; (x,y); 12) (K1056 proved uniform)
Value at R = mex(sig). This module never calls the value closed form or the
engine: it is the explicit proof artifact.

Classes (O = odd R band list, E = even R band list):
  O: ladder (1,13,'01'); then
    d = 0            : (15, S+13, '1')
    d even <=12      : (15, S+13, '1')
    d = 14           : (15, Y+11, '1'), sweep (Y+13, S+13, '01')
    d even >=16      : (15, Y+11, '1'), pin (Y+13, '01'), (Y+15, S+13, '0')
    d odd <= 11, cap=Y+5+2*ceil((d-1)/4):
       pin (cap+2,'01') iff d≡1 (mod 4) [lattice point Y+(d+z)/2],
       then ('0') band [cap+4 or cap+2, S+12]
    d odd >= 13      : (15, Y+11, '1'), (Y+13, '01'), (Y+15, S+12, '0')
    degenerate base cells:
       (y,d)=(6,0): ladder stops at 11: (1,11,'01'), (13, S+13, '1')
       (y,d)=(6,1): contiguous ladder (1,19,'01'), then (21, S+12, '0')
  E: anti-ladder (2,12,'23'); then
    d odd <=11       : 14='02', (16, S+13, '0')
    d = 13           : 14='02', (16, Y+10, '0'), (Y+12, '02'), (Y+14, S+13, '023')
    d = 15           : 14='02', (16, Y+10, '0'), (Y+12, '02'), (Y+14, '123'),
                       (Y+16, S+13, '12')   [A-child shadow of the d=14 sweep]
    d odd >= 17      : ... same ... (Y+16, S+13, '1')
    d even <=12, t = Y+4+2*ceil(d/4):
       d ≡ 2 (mod 4): 14='02', (16, t, '0'), (t+2, '123'), (t+4, S+12, '1')
       d ≡ 0 (mod 4): 14='02', (16, t, '0'), (t+2, '02'),  (t+4, S+12, '1')
    d even >=14      : 14='02', (16, Y+10, '0'), (Y+12, '02'), (Y+14, '123'),
                       (Y+16, S+12, '1')
    d = 0, y >= 8    : standard d≡0 form (t=Y+4, '02' at Y+6)
    d = 0, y = 7     : (14, Y+6, '02'), (Y+8, S+12, '1')
    degenerate base cells:
       (y,d)=(6,0): (14,18,'13'), (20, S+12, '1')
       (y,d)=(6,1): (14, S+13, '0')
       (y,d)=(6,2): (14, Y+6, '02'), (Y+8, '123'), (Y+10, S+12, '1')
"""


def bands(y, d):
    """(odd_bands, even_bands); covers every R in [1, S+13] once per parity."""
    Y = 2 * y
    S = Y + d
    B = [(1, 13, "01")]
    E = [(2, 12, "23")]
    if d % 2 == 0:
        if d == 0:
            if y == 6:
                B = [(1, 11, "01"), (13, S + 13, "1")]
                E += [(14, 18, "13"), (20, S + 12, "1")]
            elif y == 7:
                B += [(15, S + 13, "1")]
                E += [(14, Y + 6, "02"), (Y + 8, S + 12, "1")]
            else:
                B += [(15, S + 13, "1")]
                E += [(14, 14, "02"), (16, Y + 4, "0"), (Y + 6, Y + 6, "02"),
                      (Y + 8, S + 12, "1")]
        elif d <= 12:
            t = Y + 4 + 2 * ((d + 3) // 4)      # Y+4+2*ceil(d/4)
            special = "123" if d % 4 == 2 else "02"
            B += [(15, S + 13, "1")]
            if y == 6 and d == 2:
                E += [(14, Y + 6, "02"), (Y + 8, Y + 8, "123"), (Y + 10, S + 12, "1")]
            else:
                E += [(14, 14, "02"), (16, t, "0"), (t + 2, t + 2, special),
                      (t + 4, S + 12, "1")]
        elif d == 14:
            B += [(15, Y + 11, "1"), (Y + 13, S + 13, "01")]
            E += [(14, 14, "02"), (16, Y + 10, "0"), (Y + 12, Y + 12, "02"),
                  (Y + 14, Y + 14, "123"), (Y + 16, S + 12, "1")]
        else:
            B += [(15, Y + 11, "1"), (Y + 13, Y + 13, "01"),
                  (Y + 15, S + 13, "0")]
            E += [(14, 14, "02"), (16, Y + 10, "0"), (Y + 12, Y + 12, "02"),
                  (Y + 14, Y + 14, "123"), (Y + 16, S + 12, "1")]
    else:
        if d == 1 and y == 6:
            # S=13 fixed: only x=7 row
            B = [(1, 19, "01"), (21, 25, "0")]
            E += [(14, 26, "0")]
        elif d <= 11:
            cap = Y + 5 + 2 * ((d - 1 + 3) // 4)   # Y+5+2*ceil((d-1)/4)
            pin = d % 4 == 1
            if pin:
                B += [(15, cap, "1"), (cap + 2, cap + 2, "01"),
                      (cap + 4, S + 12, "0")]
            else:
                B += [(15, cap, "1"), (cap + 2, S + 12, "0")]
            E += [(14, 14, "02"), (16, S + 13, "0")]
        elif d == 13:
            B += [(15, Y + 11, "1"), (Y + 13, Y + 13, "01"),
                  (Y + 15, S + 12, "0")]
            E += [(14, 14, "02"), (16, Y + 10, "0"), (Y + 12, Y + 12, "02"),
                  (Y + 14, S + 13, "023")]
        elif d == 15:
            B += [(15, Y + 11, "1"), (Y + 13, Y + 13, "01"),
                  (Y + 15, S + 12, "0")]
            E += [(14, 14, "02"), (16, Y + 10, "0"), (Y + 12, Y + 12, "02"),
                  (Y + 14, Y + 14, "123"), (Y + 16, S + 13, "12")]
        else:
            B += [(15, Y + 11, "1"), (Y + 13, Y + 13, "01"),
                  (Y + 15, S + 12, "0")]
            E += [(14, 14, "02"), (16, Y + 10, "0"), (Y + 12, Y + 12, "02"),
                  (Y + 14, Y + 14, "123"), (Y + 16, S + 13, "1")]
    return B, E


def band_sig(y, d, R):
    """Signature at R via the table (None outside [1, S+13])."""
    S = 2 * y + d
    if not (1 <= R <= S + 13):
        return None
    seq = bands(y, d)[R % 2 == 0]
    for lo, hi, sig in seq:
        if lo <= R <= hi:
            return sig
    return None


if __name__ == "__main__":
    bad = 0
    n = 0
    for y in list(range(6, 61)) + [70, 80, 100, 150, 200, 300, 500, 1000]:
        dmax = 61 if y <= 60 else 41
        for d in range(0, dmax):
            S = 2 * y + d
            B, E = bands(y, d)
            for lo, hi, sig in B + E:
                if lo > hi or lo % 2 != hi % 2:
                    print("EMPTY/PARITY BAD", y, d, lo, hi, sig)
                    bad += 1
            for R in range(1, S + 14):
                hits = 0
                for lo, hi, sig in (B if R % 2 == 1 else E):
                    if lo <= R <= hi:
                        hits += 1
                if hits != 1:
                    print("COVER", y, d, R, hits)
                    bad += 1
                n += 1
    print(f"coverage smoke: rows={n} bad={bad}")

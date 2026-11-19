#!/usr/bin/env python3
"""Definitive (y,d)-parametric child-signature band table for the two-token
residual game z=11, all x>=y>=6, band region 1<=R<=S+11 (S=x+y, d=x-y).
Outside: R=0 -> 0; tail R>=S+12 -> S mod 2 (K0832 general tail).

Each band is (lo, hi, sig): sig is the sorted digit string of the closed-form
child-value multiset {B, A, C} at every R of that parity:
  B = H(R-1; (x,y-1); 11)   (K1037 slice when y=6, y-induction otherwise)
  A = H(R-1; (x-1,y); 11)   (only when x>y; A=B when d=0)
  C = 1 ^ H(R-1; (x,y); 10) (K1002 proved uniform)
Value at R = mex(sig). This module is the explicit proof artifact: it never
calls the value closed form or the engine.

Classes (O = odd R band list, E = even R band list):
  O (all d): ladder O[1,11]:01; then
    d even <=10 : O[13,S+11]:1
    d = 12       : O[13,2y+9]:1, sweep O[2y+11,S+11]:01
    d even >=14  : O[13,2y+9]:1, pin (2y+11):01, O[2y+13,S+11]:0
    d odd, t=min(2y+7+2*floor((d+1)/4), 2y+13), pin at t-2 iff d=3,7 or d>=11:
       no pin : O[13,t-2]:1, O[t,S+10]:0
       pin    : O[13,t-4]:1, (t-2):01, O[t,S+10]:0
  E (all d): anti-ladder E[2,10]:23, fixed point 12:02; then
    d=0 y>=7 : E[14,2y+4]:0, (2y+6):13, E[2y+8,S+10]:1
    d=0 y=6  : degenerate: E[12,16]:02, 18:13, E[20,22]:1
               (the B child is K1037's h=z row x=6, whose odd ladder
                O[1,15] feeds value 2 into both even-row points 14,16)
    d in {2,6}   : cap=2y+4+2*ceil(d/4): E[14,cap-2]:0, cap:02, E[cap+2,S+10]:1
    d in {4,8}   : cap=2y+4+2*ceil(d/4): E[14,cap]:0, cap+2:123, E[cap+4,S+10]:1
    d = 10      : E[14,2y+8]:0, 2y+10:02, E[2y+12,S+10]:1
    d >= 12 even: E[14,2y+8]:0, 2y+10:02, 2y+12:123, E[2y+14,S+10]:1
    d odd <= 9  : E[14,S+11]:0
    d = 11      : E[14,2y+8]:0, 2y+10:02, E[2y+12,S+11]:023
    d = 13      : E[14,2y+8]:0, 2y+10:02, 2y+12:123, E[2y+14,S+11]:12
    d odd >=15  : E[14,2y+8]:0, 2y+10:02, 2y+12:123, E[2y+14,S+11]:1
  The d=13 "12" tail is the A-child shadow of the d=12 sweep column
  (A=2 for all even r>=2y+12 there); from d=15 the A child only supplies
  the stationary pin 2y+11, so the tail collapses to "1". The d=11 "023"
  band is the same effect one column earlier (A child column d=10 supplies
  value 0, C child column d=11 supplies 3 on z=10's sweep row).
"""

def bands(y, d):
    """(odd_bands, even_bands); covers every R in [1, S+11] once per parity."""
    Y = 2 * y
    S = Y + d
    B = [(1, 11, "01")]
    E = [(2, 10, "23")]
    if d % 2 == 0:
        cap = min(Y + 4 + 2 * ((d + 3) // 4), Y + 10)   # 2y+4+2*ceil(d/4)
        if d <= 10:
            B.append((13, S + 11, "1"))
        elif d == 12:
            B.append((13, Y + 9, "1"))
            B.append((Y + 11, S + 11, "01"))
        else:
            B.append((13, Y + 9, "1"))
            B.append((Y + 11, Y + 11, "01"))
            B.append((Y + 13, S + 11, "0"))
        if d == 0:
            if y == 6:
                E += [(12, 16, "02"), (18, 18, "13"), (20, S + 10, "1")]
            else:
                E += [(12, 12, "02"), (14, Y + 4, "0"),
                      (Y + 6, Y + 6, "13"), (Y + 8, S + 10, "1")]
        elif d <= 8:
            if d % 4 == 2:      # d in {2,6}
                E += [(12, 12, "02"), (14, cap - 2, "0"), (cap, cap, "02"),
                      (cap + 2, S + 10, "1")]
            else:               # d in {4,8}
                E += [(12, 12, "02"), (14, cap, "0"),
                      (cap + 2, cap + 2, "123"), (cap + 4, S + 10, "1")]
        elif d == 10:
            E += [(12, 12, "02"), (14, Y + 8, "0"), (Y + 10, Y + 10, "02"),
                  (Y + 12, S + 10, "1")]
        else:                   # d >= 12 even
            E += [(12, 12, "02"), (14, Y + 8, "0"), (Y + 10, Y + 10, "02"),
                  (Y + 12, Y + 12, "123"), (Y + 14, S + 10, "1")]
    else:                       # odd d
        # odd t-classes
        t = min(Y + 7 + 2 * ((d + 1) // 4), Y + 13)
        pin = (d % 4 == 3) or (d >= 11)
        B = B[:1]  # ladder only
        if pin:
            B += [(13, t - 4, "1"), (t - 2, t - 2, "01"), (t, S + 10, "0")]
        else:
            B += [(13, t - 2, "1"), (t, S + 10, "0")]
        if d <= 9:
            E += [(12, 12, "02"), (14, S + 11, "0")]
        elif d == 11:
            E += [(12, 12, "02"), (14, Y + 8, "0"), (Y + 10, Y + 10, "02"),
                  (Y + 12, S + 11, "023")]
        else:                   # d >= 13 odd
            E += [(12, 12, "02"), (14, Y + 8, "0"), (Y + 10, Y + 10, "02"),
                  (Y + 12, Y + 12, "123"),
                  (Y + 14, S + 11, "12" if d == 13 else "1")]
    return B, E


def band_sig(y, d, R):
    """Signature at R via the table (None outside [1, S+11])."""
    S = 2 * y + d
    if not (1 <= R <= S + 11):
        return None
    for lo, hi, sig in bands(y, d)[R % 2 == 0]:
        if lo <= R <= hi:
            return sig
    return None


if __name__ == "__main__":
    bad = 0
    n = 0
    for y in list(range(6, 41)) + [50, 60]:
        for d in range(0, 41):
            S = 2 * y + d
            B, E = bands(y, d)
            for lo, hi, sig in B + E:
                if lo > hi or (lo % 2 != hi % 2):
                    print("EMPTY/PARITY BAD", y, d, lo, hi, sig)
                    bad += 1
            for R in range(1, S + 12):
                hits = 0
                for lo, hi, sig in (B if R % 2 == 1 else E):
                    if lo <= R <= hi:
                        hits += 1
                if hits != 1:
                    print("COVER", y, d, R, hits)
                    bad += 1
                n += 1
    print(f"coverage smoke: rows={n} bad={bad}")

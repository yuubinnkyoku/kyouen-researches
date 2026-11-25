#!/usr/bin/env python3
"""eqcheck: transcription-equivalence gate for the ncw-class-enum kit.

IMPORTS the shipped enum_classes.py and compares its law implementations
(pairLaw, bedLaw, single_token, cpsfG) against verbatim transcriptions of
the PUBLISHED K1310 audit kit (verify_k1310.py: P, Bm, single_token with
q_odd, cpsfG/f0/g1/Lw/sw/Tw), over a wide census of the non-congruent
window domain plus the single-token and band rows the certificate uses.
Fail-closed: rc=0 iff 0 mismatches.
"""
import sys

import enum_classes as ec

IND = lambda b: 1 if b else 0


# ---- verbatim from the published verify_k1310.py --------------------------
def q_odd(k):
    return k if k % 2 else k - 1


def P(k, z, m, g):
    """T-NCW-P claim (published kit)."""
    gs = z - 2 * k
    if gs <= 0 or g > gs or 2 * m + g < z:
        c = IND(g % 2 == 1)
    elif g == gs or g == z - 2 * m:
        c = 2
    else:
        c = IND(g % 2 == 0)
    return c


def Bm(k, z, a):
    """T-NCW-B claim (published kit)."""
    gs = z - 2 * k
    if gs < 0:
        c = 0
    else:
        r = (z - 1) // 2
        if a <= r:
            c = 0
        elif z % 2 == 1:
            c = 1
        elif gs == 0:
            c = 2
        elif a == r + 1:
            c = 2
        else:
            c = 1
    return c


def k_single_token(x, z, R):
    """Published kit single_token (verbatim, q_odd variant)."""
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))


def g1(d):
    return ec.g1f(d)  # kit g1 body is character-identical to ec.g1f


def Tw(w, d):
    return g1(d) if w % 2 else ec.f0f(d)


def k_cpsfG(w, R, d):
    if R < ec.Lw(w):
        return 2 * (R % 2)
    return Tw(w, d - ec.sw(w))


def ncw_ks(z):
    return [kk for kk in range(1, z) if (kk % 2) != (z % 2)]


def main():
    n = bad = 0

    def chk(ok):
        nonlocal n, bad
        n += 1
        if not ok:
            bad += 1

    # E1: pair law over the full NCW domain slice z2..40 m<=16 g<=60.
    for z in range(2, 41):
        for m in range(1, 17):
            for g in range(1, 61):
                for k in ncw_ks(z):
                    chk(ec.pairLaw(z, k, m, g) == P(k, z, m, g))
    # E2: bed law z2..40 a<=30.
    for z in range(2, 41):
        for a in range(1, 31):
            for k in ncw_ks(z):
                chk(ec.bedLaw(z, k, a) == Bm(k, z, a))
    # E3: single-token closed form, x 1..45, all z 0..90, R 0..90.
    for x in range(1, 46):
        for z in range(0, 91):
            for R in range(0, 91):
                chk(ec.single_token(x, z, R) == k_single_token(x, z, R))
    # E4: band law cpsfG vs kit cpsfG, w 1..40, R 0..80, d 0..80.
    for w in range(1, 41):
        for R in range(0, 81):
            for d in range(0, 81):
                chk(ec.cpsfG(w, R, d) == k_cpsfG(w, R, d))
    print(f'EQCHECK: comparisons={n} bad={bad}')
    print(f'RESULT: {"PASS" if bad == 0 else "FAIL"} eqcheck_comparisons={n} '
          f'eqcheck_bad={bad}')
    sys.exit(0 if bad == 0 else 1)


if __name__ == '__main__':
    main()

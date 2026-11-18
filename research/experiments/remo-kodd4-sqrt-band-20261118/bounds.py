#!/usr/bin/env python3
"""K0964 bounds planner: exact per-M band bounds for the two sweeps.

Mode A (validation): reproduce the published K0963 band
    t in [4, T5(M)], Y in [(M+1)*4+1, (M+1)*T5+M-1], prime Y only,
    using band_tmax from the PUBLISHED kodd5_core.py verbatim.

Mode B (new, kodd=4 violation band = complete kodd=4 census band):
    part 1: t in [2, T36=(M-2)//36], all live kappa (prime Y);
            covers every kodd=4 kappa>=1 hit (K4-CAP gamma sharp bound
            t*2^{2a}p1^2 <= M-2 with a>=1, p1>=3 -> t <= (M-2)/36),
            every kodd=5 hit (T5 <= T36 checked), and the t=2,3 gap of
            the published sweep.
    part 2: t in (T36, T12=(M-2)//12], kappa=0 only (Y=(M+1)t+1);
            covers every kodd=4 kappa=0 hit (K4-CAP kappa=0 bound
            t*2^{2a}p1 <= M-2 -> t <= (M-2)/12).

Alpha-branch kodd=4 hits satisfy t < sqrt(M)/2^a + 1/M < sqrt(M)
(K0961), hence any kodd=4 hit with t >= ceil(sqrt(M)) is a
conj(i) VIOLATION, and the band [2, T12] contains all of them:
    kappa>=1 -> t <= T36; kappa=0 -> t <= T12; M prime odd -> bounds
    never integer, so t <= floor((M-2)/36) resp. floor((M-2)/12).
"""
from __future__ import annotations

import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.join(_HERE, "..", "remo-kodd5-cap-20261118")):
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
from kodd5_core import band_tmax, is_prime, primes_upto

MMAX = 10000
MLO = 2000


def main() -> None:
    Ms = [p for p in primes_upto(MMAX) if p > MLO]
    assert len(Ms) == 926, len(Ms)
    assert all(is_prime(M) for M in Ms)

    bandA, bandB = [], []
    for M in Ms:
        # --- mode A (published band, verbatim bounds) ---
        T = band_tmax(M)
        assert T >= 4, (M, T)
        assert T < M - 1, (M, T)          # Y=M^2 (t=M-1) outside band
        ylo = (M + 1) * 4 + 1
        yhi = (M + 1) * T + M - 1
        bandA.append({"M": M, "T": T, "ylo": ylo, "yhi": yhi})

        # --- mode B ---
        T36 = (M - 2) // 36
        T12 = (M - 2) // 12
        assert (M - 2) % 36 != 0 and (M - 2) % 12 != 0  # M odd prime
        assert T36 >= 2 and T12 >= T36, (M, T36, T12)
        # published kodd=5 band is inside part 1 (t>=4 subset check)
        assert T <= T36, (M, T, T36)
        # violation zone [ceil(sqrt(M)), T36] non-empty and covered
        cs = math.isqrt(M) + 1            # M prime > 1: never a square
        assert cs <= T36, (M, cs, T36)    # kappa>=1 violations covered
        assert cs <= T12, (M, cs, T12)    # kappa=0 violations covered
        ylo1 = (M + 1) * 2 + 1
        yhi1 = (M + 1) * T36 + M - 1
        yhi2 = (M + 1) * T12 + 1          # part 2 kappa=0, t = T12
        bandB.append({"M": M, "T36": T36, "T12": T12, "csqrt": cs,
                      "ylo1": ylo1, "yhi1": yhi1, "p2tlo": T36 + 1,
                      "p2thi": T12, "yhi2": yhi2})

    ymaxA = max(r["yhi"] for r in bandA)
    ymaxB = max(max(r["yhi1"], r["yhi2"]) for r in bandB)
    # Y range up to which the global prime sieve must extend
    json.dump({"Ms": Ms, "ymaxA": ymaxA, "ymaxB": ymaxB},
              open("bounds_meta.json", "w"))
    json.dump(bandA, open("bounds_bandA.json", "w"))
    json.dump(bandB, open("bounds_bandB.json", "w"))
    print("modeA rows", len(bandA), "ymaxA", ymaxA)
    print("modeB rows", len(bandB), "ymaxB", ymaxB)
    print("T36 range", bandB[0]["T36"], bandB[-1]["T36"],
          "T12 range", bandB[0]["T12"], bandB[-1]["T12"])
    tot1 = sum(r["yhi1"] - r["ylo1"] + 1 for r in bandB)
    print("part1 Y-span total", tot1)


if __name__ == "__main__":
    main()

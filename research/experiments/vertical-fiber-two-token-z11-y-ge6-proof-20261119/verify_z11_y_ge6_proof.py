#!/usr/bin/env python3
"""Independent verifier for: two-token residual game z=11, all x>=y>=6, all
R>=0, full Grundy classification (uniform band proof).

Anchors (proved, published):
  B child of the y=6 row : K1037 (z=11, y=5 boundary slice, all x)
  C child                : K1002 proved uniform z=10 formula (x>=y>=6)
  A/B recursion, Theorem T, general tail : K0832

Candidate artifacts under test (independent implementations):
  v11      value-level closed form (T/P membership + tail)   [candidate.py]
  bands    (y,d)-parametric child-signature table            [bands.py]
  cl_value closed-form child multiset {B,A,C} values          [band_derive.py]
  engines  two direct mex recursions (ordered / canonical)   [candidate.py]

The proof value of this audit: if bands == cl (children per closed form),
mex(bands) == v11 == engines, y=6 B-children match K1037's published slice,
C-children match K1002, R<=12 matches the height-only single-token
collapse, and the tail matches, then the classification is verified at
every audited point and the universal claim rests on the two-level
induction presented in report.md (y-strong induction + per-row x outer
induction), not on the finite audit alone.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from candidate import (H_ord, H_can, clear, v11, z10_uniform)
from k1037 import candidate as k1037_candidate
from band_derive import cl_value
from bands import bands, band_sig


class Audit:
    def __init__(self):
        self.counts = {}
        self.bad = {}

    def check(self, key, cond, n=1):
        self.counts[key] = self.counts.get(key, 0) + n
        if not cond:
            self.bad[key] = self.bad.get(key, 0) + n


def mex_of_sig(sig):
    opts = {int(c) for c in sig}
    m = 0
    while m in opts:
        m += 1
    return m


def main():
    au = Audit()

    # ---- V1: band sig == closed-form child multiset, mex(band)==v11 ----
    # big parametric grid, whole band region
    for y in list(range(6, 61)) + [70, 80, 100, 150, 200, 300, 500, 1000]:
        dmax = 61 if y > 60 else 41
        for d in range(0, dmax):
            S = 2 * y + d
            for R in range(1, S + 12):
                sig = band_sig(y, d, R)
                cl = "".join(str(v) for v in cl_value(y + d, y, R))
                au.check("V1_band_vs_cl", sig == cl)
                au.check("V2_mex_v11", mex_of_sig(sig) == v11(y + d, y, R))
                p = R % 2
                mx = mex_of_sig(sig)
                au.check("V3_theoremT", mx <= (2 if p else 1))
        if y >= 1000:
            break

    # ---- V1b: scatter (deterministic LCG), wide y,d,R ----
    state = 123456789
    for _ in range(40000):
        state = (state * 1103515245 + 12345) % (1 << 31)
        y = 6 + (state >> 7) % 400
        state = (state * 1103515245 + 12345) % (1 << 31)
        d = (state >> 7) % 400
        state = (state * 1103515245 + 12345) % (1 << 31)
        S = 2 * y + d
        R = 1 + (state >> 7) % (S + 200)
        sig = band_sig(y, d, R)
        if sig is None:
            au.check("V4_scatter_tail", v11(y + d, y, R) == S % 2 or R < S + 12)
            continue
        cl = "".join(str(v) for v in cl_value(y + d, y, R))
        au.check("V4_scatter_band_vs_cl", sig == cl)
        au.check("V4_scatter_mex_v11", mex_of_sig(sig) == v11(y + d, y, R))

    # ---- V5: engines vs v11 (both engines), moderate grid, incl. tail ----
    for y in range(6, 13):
        for d in range(0, 13):
            x = y + d
            S = x + y
            for R in range(0, S + 41):
                a = H_ord(R, (x, y), 11)
                b = H_can(R, (x, y), 11)
                au.check("V5_engine_dual", a == b)
                au.check("V6_engine_vs_v11", a == v11(x, y, R))
            clear()
    for y, dmax in ((13, 7), (14, 5), (15, 4), (16, 3), (18, 3), (20, 2), (25, 2)):
        for d in range(0, dmax):
            x = y + d
            S = x + y
            for R in range(0, S + 30):
                a = H_ord(R, (x, y), 11)
                au.check("V6_engine_vs_v11", a == v11(x, y, R))
            clear()

    # ---- V7: y=6 row B-anchor: K1037 slice vs engine ----
    for x in range(6, 31):
        for r in range(0, x + 26):
            au.check("V7_k1037_anchor",
                     k1037_candidate(x, r) == H_ord(r, (x, 5), 11))
        clear()

    # ---- V8: C-anchor: K1002 z=10 uniform vs engine ----
    for y in range(6, 17):
        for d in range(0, 13):
            x = y + d
            S = x + y
            for r in range(0, S + 12):
                au.check("V8_k1002_anchor",
                         z10_uniform(x, y, r) == H_ord(r, (x, y), 10))
            clear()

    # ---- V9: height-only collapse R<=12 vs single-token engine ----
    for y in range(6, 16):
        for d in range(0, 9):
            S = 2 * y + d
            for R in range(1, 13):
                au.check("V9_height_only",
                         v11(y + d, y, R) == H_ord(R, (S,), 11))
            clear()

    # ---- V10: tail: engine vs S mod 2, R in [S+12, S+40] ----
    for y in range(6, 12):
        for d in range(0, 10):
            S = 2 * y + d
            for R in range(S + 12, S + 41):
                au.check("V10_tail", H_ord(R, (y + d, y), 11) == S % 2)
            clear()

    # ---- assemble audit ----
    out = {
        "k": "z11_y>=6_uniform_full_grundy",
        "python": sys.version.split()[0],
        "pid_absent": True,
        "counts": au.counts,
        "bad": au.bad,
        "total": sum(au.counts.values()),
    }
    blob = json.dumps(out, sort_keys=True).encode()
    out["sha256"] = hashlib.sha256(blob).hexdigest()
    blob2 = json.dumps(out, sort_keys=True).encode()
    out["sha256_stable"] = hashlib.sha256(blob2).hexdigest()
    print(json.dumps(out, sort_keys=True, indent=1))
    return 0 if not au.bad else 1


if __name__ == "__main__":
    sys.exit(main())

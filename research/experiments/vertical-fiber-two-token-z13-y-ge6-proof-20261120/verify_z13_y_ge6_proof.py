#!/usr/bin/env python3
"""Independent verifier for: two-token residual game z=13, all x>=y>=6, all
R>=0, full Grundy classification (uniform band proof).

Anchors (proved, published):
  B child of the y=6 row : K1045 (z=13, y=5 boundary slice, all x)
  C child                : K1056 proved uniform z=12 formula (x>=y>=6)
  A/B recursion, Theorem T, general tail : K0832

Candidate artifacts under test (independent implementations):
  v13      value-level closed form (T/P membership + tail)   [candidate.py]
  bands    (y,d)-parametric child-signature table           [bands.py]
  cl_value closed-form child multiset {B,A,C} values         [band_derive.py]
  engines  two direct mex recursions (ordered / canonical)  [candidate.py]

The proof value of this audit: if bands == cl (children per closed form),
mex(bands) == v13 == engines, y=6 B-children match K1045's published slice,
C-children match K1056, R<=12 matches the height-only single-token collapse,
and the tail matches, then the classification is verified at every audited
point and the universal claim rests on the two-level induction presented in
report.md (y-strong induction + per-row x outer induction).
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from candidate import (H_ord, H_can, clear, v13, value12, k1045)
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

    # ---- V1: band sig == closed-form child multiset, mex(band)==v13 ----
    # big parametric grid, whole band region
    for y in list(range(6, 61)) + [70, 80, 100, 150, 200, 300, 500, 1000]:
        dmax = 61 if y <= 60 else 41
        for d in range(0, dmax):
            S = 2 * y + d
            for R in range(1, S + 14):
                sig = band_sig(y, d, R)
                cl = "".join(str(v) for v in cl_value(y + d, y, R))
                au.check("V1_band_vs_cl", sig == cl)
                au.check("V2_mex_v13", mex_of_sig(sig) == v13(y + d, y, R))
                p = R % 2
                mx = mex_of_sig(sig)
                au.check("V3_theoremT", mx <= (2 if p else 1))

    # ---- V1b: scatter (deterministic LCG), wide y,d,R ----
    state = 20261120
    for _ in range(50000):
        state = (state * 1103515245 + 12345) % (1 << 31)
        y = 6 + (state >> 7) % 400
        state = (state * 1103515245 + 12345) % (1 << 31)
        d = (state >> 7) % 400
        state = (state * 1103515245 + 12345) % (1 << 31)
        S = 2 * y + d
        R = 1 + (state >> 7) % (S + 200)
        sig = band_sig(y, d, R)
        if sig is None:
            au.check("V4_scatter_tail",
                     v13(y + d, y, R) == S % 2 or R < S + 14)
            continue
        cl = "".join(str(v) for v in cl_value(y + d, y, R))
        au.check("V4_scatter_band_vs_cl", sig == cl)
        au.check("V4_scatter_mex_v13", mex_of_sig(sig) == v13(y + d, y, R))

    # ---- V5: engines vs v13 (both engines), moderate grid, incl. tail ----
    for y in range(6, 14):
        for d in range(0, 13):
            x = y + d
            S = x + y
            for R in range(0, S + 43):
                a = H_ord(R, (x, y), 13)
                b = H_can(R, (x, y), 13)
                au.check("V5_engine_dual", a == b)
                au.check("V6_engine_vs_v13", a == v13(x, y, R))
            clear()
    for y, dmax in ((14, 8), (15, 6), (16, 5), (18, 4), (20, 3), (25, 3),
                    (30, 2)):
        for d in range(0, dmax):
            x = y + d
            S = x + y
            for R in range(0, S + 32):
                a = H_ord(R, (x, y), 13)
                au.check("V6_engine_vs_v13", a == v13(x, y, R))
            clear()

    # ---- V7: y=6 row B-anchor: K1045 slice vs engine ----
    for x in range(6, 32):
        for r in range(0, x + 28):
            au.check("V7_k1045_anchor", k1045(x, r) == H_ord(r, (x, 5), 13))
        clear()

    # ---- V8: C-anchor: K1056 z=12 uniform vs engine ----
    for y in range(6, 17):
        for d in range(0, 14):
            x = y + d
            S = x + y
            for r in range(0, S + 13):
                au.check("V8_k1056_anchor",
                         value12(x, y, r) == H_ord(r, (x, y), 12))
            clear()

    # ---- V9: height-only collapse R<=19 vs single-token engine ----
    for y in list(range(6, 17)) + [20, 25, 40]:
        for d in range(0, 13):
            S = 2 * y + d
            for R in range(1, 20):
                au.check("V9_height_only",
                         v13(y + d, y, R) == H_ord(R, (S,), 13))
            clear()
    # boundary documentation: collapse is exactly to R<=19; first failure at
    # (y,d)=(6,2), R=20
    au.check("V9_boundary_60_d2_R20",
             v13(8, 6, 20) == 0 and H_ord(20, (14,), 13) == 1)

    # ---- V10: tail: engine vs S mod 2, R in [S+14, S+40] ----
    for y in range(6, 12):
        for d in range(0, 10):
            S = 2 * y + d
            for R in range(S + 14, S + 41):
                au.check("V10_tail", H_ord(R, (y + d, y), 13) == S % 2)
            clear()

    # ---- assemble audit ----
    out = {
        "k": "z13_y>=6_uniform_full_grundy",
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
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(here, "output")
    os.makedirs(outdir, exist_ok=True)
    text = json.dumps(out, sort_keys=True, indent=1)
    with open(os.path.join(outdir, "audit.json"), "w") as f:
        f.write(text + "\n")
    print(text)
    return 0 if not au.bad else 1


if __name__ == "__main__":
    sys.exit(main())

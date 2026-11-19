#!/usr/bin/env python3
"""Derive the (y,d)-parametric A/B/C signature band table for z=13, y>=6.

Children (closed form, mirrors the proven decomposition):
  B = H(r;(x,y-1);13):  v13(x, y-1, r)  for y>=7;  K1045 candidate(x, r) for y=6
  A = H(r;(x-1,y);13):  v13(x-1, y, r)  (only when x>y)
  C = 1 ^ H(r;(x,y);12) = 1 ^ value12(x, y, r)
Band region 1<=R<=S+13; signature = sorted child value multiset digits.
Bands compress per parity (O = odd R, E = even R).
"""
from candidate import v13, value12, k1045


def cl_value(x, y, R):
    r = R - 1
    opts = set()
    if y == 6:
        opts.add(k1045(x, r))
    else:
        opts.add(v13(x, y - 1, r))
    d = x - y
    if d > 0:
        opts.add(v13(x - 1, y, r))
    opts.add(1 ^ value12(x, y, r))
    return tuple(sorted(opts))


def cl_runs(y, d):
    x = y + d
    S = x + y
    per = {1: [], 0: []}
    for R in range(1, S + 14):
        sig = "".join(str(v) for v in cl_value(x, y, R))
        p = R % 2
        seq = per[p]
        if seq and seq[-1][2] == sig:
            seq[-1][1] = R
        else:
            seq.append([R, R, sig])
    return per


def fmt(seq, S, y):
    out = []
    for lo, hi, sig in seq:
        los, his = f"{lo}", f"{hi}"
        for base, name in ((2 * y, "Y"), (S, "S")):
            if lo > 20 and 0 <= lo - base <= 60:
                los = f"{name}{f'{lo-base:+d}' if lo != base else ''}"
                break
        for base, name in ((2 * y, "Y"), (S, "S")):
            if hi > 20 and 0 <= hi - base <= 60:
                his = f"{name}{f'{hi-base:+d}' if hi != base else ''}"
                break
        if lo == hi:
            out.append(f"{los}={sig}")
        else:
            out.append(f"[{los},{his}]={sig}")
    return " ".join(out)


def show(ylist, dlist):
    for d in dlist:
        for y in ylist:
            runs = cl_runs(y, d)
            S = 2 * y + d
            print(f"d={d:2d} y={y:3d} S={S:3d} O: {fmt(runs[1], S, y)}")
            print(f"{'':38s}E: {fmt(runs[0], S, y)}")
        print()


if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "a"
    if which == "a":
        show([6, 9], list(range(0, 15)) + [15, 16, 20, 26])
    elif which == "b":
        show([8, 40], [0, 1, 5, 13, 14, 15, 16, 17, 20])

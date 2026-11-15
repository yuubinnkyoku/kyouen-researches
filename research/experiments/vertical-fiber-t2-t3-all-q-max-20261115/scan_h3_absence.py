#!/usr/bin/env python3
"""Targeted absence scan for H=3 in the M=3, p=1 residual token game.

H(e,R)=3 requires all three move types (climb0, climb1, spawn), i.e.
e_0>=1, e_1>=1, e_2>=1, and R>=1; so the scan restricts to that box.
Writes output/h3_scan.json.
"""
import json, os
from functools import lru_cache

def mex(opts):
    n = 0
    while n in opts:
        n += 1
    return n

@lru_cache(maxsize=None)
def H(e, R):
    if R == 0:
        return 0
    opts = set()
    for i in range(3):
        if e[i] >= 1:
            c = list(e); c[i] -= 1
            if i + 1 < 3:
                c[i + 1] += 1
                opts.add(H(tuple(c), R - 1))
            else:
                opts.add(H(tuple(c), R - 1) ^ 1)
    return mex(opts) if opts else 0

mx = 0; chk = 0; best = None
for e0 in range(1, 11):
    for e1 in range(1, 11):
        for e2 in range(1, 11):
            e = (e0, e1, e2)
            L = 3 * e0 + 2 * e1 + e2
            for R in range(1, min(80, L + 30)):
                chk += 1
                h = H(e, R)
                if h > mx:
                    mx = h; best = (e, R)
res = {"box": "1<=e_i<=10 (all three move types forced), 1<=R<=min(80,L+30)",
       "states_checked": chk, "max_H": mx, "argmax": best,
       "note": "H=3 never observed; sup H = 2 on this box. Finite scan, not a proof."}
os.makedirs("output", exist_ok=True)
with open("output/h3_scan.json", "w") as f:
    json.dump(res, f, indent=1)
print(res)

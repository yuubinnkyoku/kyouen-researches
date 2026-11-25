#!/usr/bin/env python3
"""Third independent implementation for H(R;(x,5);17).

Unlike verify_z17_y5.py (lru_cache tuple-slicing engines), this census
engine uses an explicit dict memo over canonical states and enumerates
moves per distinct token value with multiplicity, i.e. from state
(R, X, z) the token moves are: for each distinct value v in X (with
multiplicity), one move decrements a single token of value v.

Photographs rows x=5..45 for all 1<=R<=x+40, cross-checks every value
against the closed form transcription, and writes census.txt.
"""
import sys
from pathlib import Path

sys.setrecursionlimit(200000)

def mex(vals):
    m = 0; vals = set(vals)
    while m in vals: m += 1
    return m

MEMO = {}
def H(R, X, z):
    """X: tuple sorted descending. Explicit dict memo recursion."""
    if R == 0: return 0
    key = (R, X, z)
    v = MEMO.get(key)
    if v is not None: return v
    opts = []
    seen_values = set()
    for i, tok in enumerate(X):
        if tok in seen_values: continue
        seen_values.add(tok)
        if tok > 1:
            Y = list(X); Y[i] = tok - 1
            Y.sort(reverse=True)
            opts.append(H(R - 1, tuple(Y), z))
        else:
            Y = list(X); del Y[i]
            Y.sort(reverse=True)
            if not Y: Y = ()
            opts.append(H(R - 1, tuple(Y), z + 1))
    if z:
        opts.append(1 ^ H(R - 1, X, z - 1))
    v = mex(opts)
    MEMO[key] = v
    return v

BASEP = {18, 20, 22, 24, 26}
def T_pred(x, r):
    if x == 5: return r % 2 == 1 and r <= 9
    if x in (6, 7): return r % 2 == 1 and r <= 11
    if x in (8, 9): return r % 2 == 1 and r <= 13
    if x in (10, 11): return r % 2 == 1 and r <= 15
    if x == 12: return r % 2 == 1 and r <= 21
    if x == 14: return (r % 2 == 1 and r <= 17) or r == 23
    if x == 18: return (r % 2 == 1 and r <= 17) or r == 25
    if x == 22: return (r % 2 == 1 and r <= 17) or r == 27
    if x == 23: return (r % 2 == 1 and r <= 17) or (r % 2 == 1 and 27 <= r <= 45)
    if x >= 24: return (r % 2 == 1 and r <= 17) or r == 27
    return r % 2 == 1 and r <= 17

def P_pred(x, r):
    if x in (5, 7, 9, 11): return False
    if x == 6: return r >= 12
    if x == 8: return r >= 14
    if x == 10: return r >= 16
    if x == 12: return r in (18, 20, 22) or r >= 23
    if x in (13, 15): return r in (18, 20, 22)
    if x in (14, 16): return r in (18, 20, 22) or r >= 24
    if x in (17, 19): return r in (18, 20, 22, 24)
    if x in (18, 20): return r in (18, 20, 22, 24) or r >= 26
    if x == 21: return r in BASEP
    if x == 22: return r in BASEP or r >= 28
    if x == 23: return r in BASEP
    if x % 2: return r in BASEP or (r % 2 == 1 and 29 <= r <= x + 22)
    return r in BASEP or (r % 2 == 1 and 29 <= r <= x + 23) or r >= x + 24

def formula(x, r):
    if r == 0: return 0
    if r >= x + 23: return (x + 5) % 2
    if T_pred(x, r): return 2
    if P_pred(x, r): return 1
    return 0

def main():
    lines = []
    mismatches = 0
    total = 0
    frag = {}   # row photo: run-length encoding of values r=0..x+40
    for x in range(5, 46):
        vals = [H(r, (x, 5), 17) for r in range(0, x + 41)]
        for r, v in enumerate(vals):
            total += 1
            if v != formula(x, r):
                mismatches += 1
                lines.append(f"MISMATCH x={x} r={r} census={v} formula={formula(x, r)}")
        # run-length photo
        runs = []
        cur = vals[0]; start = 0
        for i in range(1, len(vals)):
            if vals[i] != cur:
                runs.append(f"[{start},{i-1}]={cur}")
                cur = vals[i]; start = i
        runs.append(f"[{start},{len(vals)-1}]={cur}")
        frag[x] = ' '.join(runs)
    lines.append(f"census engine states: {len(MEMO)}")
    lines.append(f"points compared: {total}, mismatches vs closed form: {mismatches}")
    lines.append("verdict: " + ("AGREE" if mismatches == 0 else "DISAGREE"))
    lines.append("")
    lines.append("== row photos (run-length of H(R;(x,5);17), R=0..x+40) ==")
    for x in range(5, 46):
        lines.append(f"x={x}: {frag[x]}")
    text = "\n".join(lines) + "\n"
    out = Path(__file__).resolve().parent / 'output' / 'census.txt'
    out.write_text(text, encoding='utf-8')
    print(text[:2000])
    print(f"... ({len(text)} chars) written to output/census.txt")
    return mismatches

if __name__ == '__main__':
    sys.exit(0 if main() == 0 else 1)

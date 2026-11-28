#!/usr/bin/env python3
"""brute_third.py — third, fully independent pure-Python full enumeration.

Deliberately written with a different algorithm shape from the C enumerator:
no Gray code, no per-line counters; it tests each subset mask directly with
popcounts over precomputed line bitmasks (upper bound early-exit pruning on
the safe side is intentionally NOT used, to stay dumb and independent).

Usage: brute_third.py <board.txt> <s>
Prints: maximal_safe {size: count, ...} minimal_blocking {size: count, ...}
"""
import sys

def main():
    path, s = sys.argv[1], int(sys.argv[2])
    toks = open(path).read().split()
    n, L = int(toks[0]), int(toks[1])
    i = 2; lines = []
    for _ in range(L):
        k = int(toks[i]); i += 1
        m = 0
        for j in range(k):
            m |= 1 << int(toks[i]); i += 1
        lines.append(m)
    l = lines[0].bit_count()
    assert all(m.bit_count() == l for m in lines)
    t = l - s
    full = (1 << n) - 1
    maxc = {}
    minc = {}
    for S in range(1 << n):
        cnts = [(S & m).bit_count() for m in lines]
        if all(c <= s for c in cnts):
            # maximal? every outside point has a line at exactly s
            maximal = True
            for p in range(n):
                if S >> p & 1: continue
                S2 = S | (1 << p)
                if all((S2 & m).bit_count() <= s for m in lines):
                    maximal = False; break
            if maximal:
                k = S.bit_count(); maxc[k] = maxc.get(k, 0) + 1
        if all(c >= t for c in cnts):
            minimal = True
            for p in range(n):
                if not (S >> p & 1): continue
                S2 = S & ~(1 << p)
                if all((S2 & m).bit_count() >= t for m in lines):
                    minimal = False; break
            if minimal:
                k = S.bit_count(); minc[k] = minc.get(k, 0) + 1
    print("maximal_safe", dict(sorted(maxc.items())),
          "minimal_blocking", dict(sorted(minc.items())))

if __name__ == "__main__":
    main()

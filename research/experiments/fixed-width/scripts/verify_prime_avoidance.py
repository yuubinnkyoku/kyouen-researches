#!/usr/bin/env python3
"""Finite sanity checks of the prime-avoidance lemma (not PNT(AP))."""
from math import log, floor

def primes_3mod4(a, b):
    return [p for p in range(int(a)+1,int(b)+1)
            if p%4==3 and all(p%d for d in range(2,int(p**.5)+1))]

for L in [30,100,300,1000,3000,10000]:
    available = len(primes_3mod4(2*L,8*L))
    max_divisors = floor(L/log(2*L))
    surviving = available-max_divisors
    requested = floor(.5*L/log(L))
    assert surviving>=requested,(L,available,max_divisors,requested)
    print(f"L={L}: primes={available}, max_g_divisors={max_divisors}, guaranteed={surviving}, s={requested}: PASS")
print("PASS: six finite checks only; unbounded prime supply relies on PNT(AP)")

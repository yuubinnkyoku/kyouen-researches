#!/usr/bin/env python3
"""Independent integer audit of the exact slope-9 Pell-orbit circle count.

Only the exact integer identities are machine checked. The asymptotic
liminf/limsup statements require the accompanying mathematical proof.
"""
from __future__ import annotations
import json
import math


def pell_chords(n: int) -> tuple[int, int, int, int]:
    u, v = 1, 0
    for _ in range(n):
        u, v = 19*u + 60*v, 6*u + 19*v
    assert u*u - 10*v*v == 1
    chords = (9*v-u, 3*u-v, 3*u+v, u+9*v)
    assert all(x > 0 and x % 2 for x in chords)
    assert all(a < b for a,b in zip(chords,chords[1:]))
    assert chords[0]**2-2*chords[1]**2+chords[2]**2 == -8
    assert chords[1]**2-2*chords[2]**2+chords[3]**2 == -8
    # Independent check in actual lattice coordinates, not only chord lengths.
    d = chords[-1]
    points = [(u,0),(9*v,0),(5*v-u,1),(2*u+4*v,1),
              (4*v-u,2),(2*u+5*v,2),(0,3),(d,3)]
    assert len(set(points)) == 8
    assert min(x for x,y in points) == 0
    assert max(x for x,y in points) == d
    for x,y in points:
        assert x*x+y*y-d*x-3*(u*v+1)*y+9*u*v == 0
    return chords


def widths(k: int) -> list[int]:
    a, b = 1, 73
    result = []
    for n in range(1, k+1):
        assert pell_chords(n)[-1] == b
        result.append(b)
        a, b = b, 38*b-a
    return result


def count_direct(m: int, ds: list[int]) -> int:
    return 2*sum(m-d for d in ds if d < m)


def count_closed(m: int, ds: list[int]) -> int:
    n = sum(d < m for d in ds)
    if n == 0:
        return 0
    d_n = ds[n-1]
    d_np1 = ds[n] if n < len(ds) else 38*ds[-1]-ds[-2]
    numerator = d_np1 - d_n - 72
    assert numerator % 18 == 0
    return 2*n*m - numerator//18


def main() -> None:
    ds = widths(28)
    assert ds[:6] == [73, 2773, 105301, 3998665, 151843969, 5766072157]
    checks = 0
    for n in range(1, 25):
        for m in (ds[n-1]-1,ds[n-1],ds[n-1]+1,
                  (ds[n-1]+ds[n])//2,ds[n],ds[n]+1):
            assert count_direct(m,ds) == count_closed(m,ds)
            checks += 1
        m=ds[n-1]
        # Discrete second derivative has exactly one 2-unit jump per width.
        assert count_direct(m+1,ds)-2*count_direct(m,ds)+count_direct(m-1,ds)==2
        if m>73:
            assert count_direct(m,ds)-2*count_direct(m-1,ds)+count_direct(m-2,ds)==0
    lam = 19+6*math.sqrt(10)
    alpha = (1+9/math.sqrt(10))/2
    x_star = lam*math.log(lam)/(lam-1)
    def fluctuation(x:float)->float:
        return -2*math.log(alpha*x)/math.log(lam)-2*lam/((lam-1)*x)
    # For each n choose integer m near alpha * lambda^n * x.
    samples = []
    for n in (5,10,15,20):
        for x in (1.0,x_star,lam):
            m = round(alpha * lam**n * x)
            z = count_direct(m,ds)/m - (2/math.log(lam))*math.log(m)
            samples.append({"n":n,"x":round(x,9),"normalized":round(z,9),
                            "predicted":round(fluctuation(x),9)})
    print(json.dumps({"status":"PASS","integer_identity_cases":checks,
          "first_widths":ds[:8],"leading_coefficient":2/math.log(lam),
          "liminf":fluctuation(1.0),"limsup":fluctuation(x_star),
          "x_star":x_star,"samples":samples},indent=2))

if __name__ == '__main__':
    main()

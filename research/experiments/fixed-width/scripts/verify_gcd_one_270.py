#!/usr/bin/env python3
"""Finite exact modular certificate: 25 double-hit rows in 270 rows imply gcd=1.

Enumerates every (c,n) modulo each listed modulus, retains the permitted
row-index masks, and intersects all masks. A set of >=25 rows surviving all
necessary congruence conditions would survive the intersection. None does.
"""
from math import gcd

WINDOW = 270
TARGET = 25
MODS = {
    2: (9, 7, 49, 11, 19, 23),
    3: (11, 19, 23, 31),
    4: (11, 19, 23),
    5: (11, 19, 23),
    6: (19, 23),
    7: (19, 23),
    8: (19,),
    9: (19,),
    10: (19,),
    11: (19,),
}


def masks_direct(width, modulus):
    sq = {(a * a) % modulus for a in range(modulus)}
    out = set()
    for c in range(modulus):
        shifts = [((2 * i + c) ** 2) % modulus for i in range(width)]
        for n in range(modulus):
            mask = sum(1 << i for i, z in enumerate(shifts) if (n - z) % modulus in sq)
            if mask.bit_count() >= TARGET:
                out.add(mask)
    return out


def masks_inverse(width, modulus):
    # Independent local construction: enumerate possible n for each (c,row)
    sq = {(a * a) % modulus for a in range(modulus)}
    out = set()
    for c in range(modulus):
        by_n = [0] * modulus
        for i in range(width):
            z = ((2 * i + c) ** 2) % modulus
            for s in sq:
                by_n[(z + s) % modulus] |= 1 << i
        out.update(m for m in by_n if m.bit_count() >= TARGET)
    return out


def verify():
    for step, moduli in MODS.items():
        assert all(gcd(step, m) == 1 for m in moduli)
        width = (WINDOW + step - 1) // step
        assert width >= TARGET
        states = {(1 << width) - 1}
        print(f"g={step} width={width}", flush=True)
        for m in moduli:
            direct = masks_direct(width, m)
            inverse = masks_inverse(width, m)
            assert direct == inverse, (step, m, "local mask mismatch")
            states = {a & b for a in states for b in direct if (a & b).bit_count() >= TARGET}
            print(f"  mod={m} local={len(direct)} survivors={len(states)}", flush=True)
            if not states:
                break
        assert not states, f"g={step}: congruence certificate insufficient"
    print("PASS: in any 270 consecutive integer rows, 25 double-hit rows imply gcd=1")


if __name__ == "__main__":
    verify()

"""Orbit-stabilizer verification of the census maximal counts.

For an explicit maximal cap of size k, PGL(3,9) maps it to maximal caps of size
k.  The orbit size = |PGL| / |Stab|, computed by enumerating all ordered
4-frames inside the cap and keeping the projectivities that map the cap to
itself.  Comparing with census maximal counts independently verifies those
counts (and shows the caps form a single PGL orbit).

Also does the same for a conic (maximal 10-cap); the stabilizer should be
PGL(2,9) of order 720.
"""
import itertools
from pathlib import Path

import pg
import verify_pgl_orbit as vo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "out"

PGL = 9**3 * (9**3 - 1) * (9**2 - 1)


def orbit_stabilizer(cap):
    cap = sorted(cap)
    F0 = cap[:4]
    M0 = vo.projectivity_from_standard(F0)
    invM0 = vo.matinv(M0)
    expected = set(cap)
    stab = 0
    total = 0
    for F in itertools.permutations(cap, 4):
        total += 1
        M1 = vo.projectivity_from_standard(F)
        g = vo.matmul(M1, invM0)
        img = {vo.apply_proj(g, p) for p in cap}
        if img == expected:
            stab += 1
    return stab, PGL // stab


def main():
    tests = [
        ("conic 10-cap", [0, 1, 10, 20, 31, 45, 51, 62, 75, 88], 58968),
        ("conic 7-cap", [0, 1, 10, 20, 31, 45, 51], 7076160),
        ("maximal 6-cap", [4, 32, 39, 55, 57, 81], 707616),
        ("maximal 7-cap", [33, 39, 57, 70, 74, 80, 89], 2021760),
        ("maximal 8-cap", [11, 22, 29, 32, 41, 44, 61, 89], 5307120),
        ("non-conic non-max 7-cap (orbit 1 of 2)", [11, 22, 29, 32, 44, 61, 89],
         21228480),
    ]
    for name, cap, expected in tests:
        assert len(cap) == len(set(cap)) and pg.is_cap(cap), name
        e = pg.addable_mask(cap)
        print(f"\n{name}: {sorted(cap)}")
        print(f"  cap=True size={len(cap)} addable={e.bit_count()} "
              f"maximal={e == 0}")
        stab, orbit = orbit_stabilizer(cap)
        print(f"  stabilizer order = {stab}")
        print(f"  orbit size = |PGL|/{stab} = {orbit}")
        print(f"  census/claimed count {expected}; equal = {orbit == expected}")
    print(f"\n  2 * {PGL // 2} = {PGL} "
          f"(claimed non-conic non-maximal 7-caps = 42456960)")


if __name__ == "__main__":
    main()

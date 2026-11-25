"""Two PGL(3,9) orbits of non-conic non-maximal 7-caps.

The maximal 8-cap A has a stabilizer of order 8 with two orbits of size 4 on
A (verified in verify_pgl_orbit.py).  Removing a point from each orbit gives
7-caps S, T.  Verify S and T each have stabilizer order 2 (orbit 2^? ) and
are in different PGL orbits.
"""
import itertools
from pathlib import Path

import pg
import verify_pgl_orbit as vo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "out"
PGL = 9**3 * (9**3 - 1) * (9**2 - 1)


def stabilizer_order(cap):
    cap = sorted(cap)
    M0 = vo.projectivity_from_standard(cap[:4])
    invM0 = vo.matinv(M0)
    expected = set(cap)
    stab = 0
    for F in itertools.permutations(cap, 4):
        M1 = vo.projectivity_from_standard(F)
        g = vo.matmul(M1, invM0)
        if {vo.apply_proj(g, p) for p in cap} == expected:
            stab += 1
    return stab


def maps_to(capA, capB):
    capA = sorted(capA)
    capB = sorted(capB)
    M0 = vo.projectivity_from_standard(capA[:4])
    invM0 = vo.matinv(M0)
    expected = set(capB)
    for F in itertools.permutations(capB, 4):
        M1 = vo.projectivity_from_standard(F)
        g = vo.matmul(M1, invM0)
        if {vo.apply_proj(g, p) for p in capA} == expected:
            return True
    return False


def main():
    A = [11, 22, 29, 32, 41, 44, 61, 89]
    conics = set(int(l) for l in (OUT / "conics.txt").read_text().splitlines())
    print("maximal 8-cap A:", A)
    # stabilizer orbits on A were [11,22,32,41] and [29,44,61,89]
    S = [x for x in A if x != 41]   # remove from orbit 1
    T = [x for x in A if x != 29]   # remove from orbit 2
    for name, cap in (("S=A\\{41}", S), ("T=A\\{29}", T)):
        cm = sum(1 << x for x in cap)
        stab = stabilizer_order(cap)
        print(f"{name} = {cap}")
        print(f"  cap={pg.is_cap(cap)} addable={pg.addable_mask(cap).bit_count()} "
              f"conic={cm in conics}")
        print(f"  stabilizer={stab} orbit=|PGL|/{stab}={PGL // stab}")
    print(f"maps_to(S,T) = {maps_to(S, T)}")
    # sanity: within stabilizer orbit 1
    S2 = [x for x in A if x != 11]
    print(f"maps_to(S,S2) = {maps_to(S, S2)} (same stabilizer orbit)")
    print(f"2 orbits of size |PGL|/2: {2 * (PGL // 2)} "
          f"(claimed non-conic non-maximal 7-caps = 42456960)")


if __name__ == "__main__":
    main()

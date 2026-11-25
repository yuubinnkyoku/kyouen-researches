#!/usr/bin/env python3
"""Parametric census for the two-token residual-game y=1 family.

For each z in [ZMIN, ZMAX] the candidate closed form cand(z, x, R) for
H(R; (x,1); z) -- derived from the published slices z=8,9,10,11 (parallel lane)
and z=12,13,14,15 (K1016, K1017, K1018, K1019/K1020) as a function of z and
parity -- is checked against two independent raw recursions (order-preserving
and descending-canonical) over x in [1, XMAX], R in [0, x+PAD].

This is a FINITE census supporting a CONJECTURE. It is not a universal proof
in z (nor in x). Any mismatch is recorded with full coordinates.
"""
from __future__ import annotations
import sys, json, time
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

ZMIN, ZMAX = 1, 60
PADZ = 6


def xmax_for(z):
    return max(60, z + 8)


def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


@lru_cache(None)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)


@lru_cache(None)
def H_canonical(R, X, z):
    X = tuple(sorted(X))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            opts.add(H_canonical(R - 1, tuple(sorted(X[:i] + (v - 1,) + X[i + 1:])), z))
        else:
            opts.add(H_canonical(R - 1, X[:i] + X[i + 1:], z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)


def cand(z, x, R):
    """Candidate closed form for H(R; (x, 1); z), y = 1, all z >= 4.

    Even z:  pin = z + 3 (value-2 ladder top z-1, advanced point z+1 at row
              x = z-1 as a T-point, P-point z+1 at rows x = z+1 and x >= z+2).
    Odd z:   pin = z + 2 (ladder top z, P-point z+1 at row x = z (and above),
              sweep row x = z+2 merges O[1, z] and O[pin, x+y+z] into O[1, 2z+3]).
    S = x + y + z with y = 1.
    """
    if R == 0:
        return 0
    if x < 1:
        return 0
    S = x + 1 + z
    if z % 2 == 0:
        # ---- T (value 2) ----
        if x % 2 == 0 and 2 <= x <= z - 2:
            T = (R % 2 == 1 and R <= x + 1)
        elif x % 2 == 1 and x <= z - 3:
            T = (R % 2 == 1 and R <= x)
        elif x == z - 1:
            T = (R % 2 == 1 and R <= z + 1)
        elif x in (z, z + 1):
            T = (R % 2 == 1 and R <= z - 1)
        elif x == z + 2:
            T = (R % 2 == 1 and (R <= z - 1 or z + 3 <= R <= 2 * z + 3))
        else:  # x >= z + 3
            T = (R == z + 3 or (R % 2 == 1 and R <= z - 1))
        # ---- P (value 1) ----
        if x % 2 == 1 and x <= z - 1:
            P = False
        elif x % 2 == 0 and x <= z - 2:
            P = (R >= x + 2)
        elif x == z:
            P = (R >= z + 1)
        elif x == z + 1:
            P = (R == z + 1)
        elif x % 2 == 0:  # >= z + 2
            P = (R == z + 1 or (R % 2 == 0 and z + 4 <= R <= S - 1) or R >= S + 1)
        else:  # x odd >= z + 3
            P = (R == z + 1 or (R % 2 == 0 and z + 4 <= R <= S))
    else:
        # ---- T (value 2) ----
        if x % 2 == 0 and x <= z - 1:
            T = (R % 2 == 1 and R <= x + 1)
        elif x % 2 == 1 and x <= z:
            T = (R % 2 == 1 and R <= x)
        elif x == z + 1:
            T = (R % 2 == 1 and R <= z + 2)
        elif x == z + 2:
            T = (R % 2 == 1 and R <= 2 * z + 3)
        else:  # x >= z + 3
            T = (R == z + 2 or (R % 2 == 1 and R <= z))
        # ---- P (value 1) ----
        if x % 2 == 1 and x <= z - 2:
            P = False
        elif x % 2 == 0 and x <= z - 1:
            P = (R >= x + 2)
        elif x == z:
            P = (R == z + 1)
        elif x == z + 1:
            P = (R == z + 1 or R >= z + 3)
        elif x == z + 2:
            P = (R == z + 1)
        elif x % 2 == 1:  # odd x >= z + 3
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S))
        else:  # even x >= z + 4
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S) or R >= S + 1)
    assert not (T and P), (z, x, R)
    return 2 if T else (1 if P else 0)


# ---- third-source agree check against published slice formulas ----
# K1018 (z=14, y=1): transcribed verbatim from the published
# census_z15_y1.py child-anchor functions (used as child C in the z=15 slice).
def T14(x, r):
    if x == 1: return r == 1
    if x == 13: return 1 <= r <= 15 and r % 2 == 1
    if x <= 12:
        top = x + 1 if x % 2 == 0 else x
        return 1 <= r <= top and r % 2 == 1
    if x == 14 or x == 15: return 1 <= r <= 13 and r % 2 == 1
    if x == 16:
        return (1 <= r <= 13 or 17 <= r <= 31) and r % 2 == 1
    return r in (1, 3, 5, 7, 9, 11, 13, 17)

def P14(x, r):
    if x % 2 == 1:
        if x <= 13: return False
        if x == 15: return r == 15
        return r == 15 or (r % 2 == 0 and 18 <= r <= x + 15)
    if x <= 12: return r >= x + 2
    if x == 14: return r >= 15
    return r == 15 or (r % 2 == 0 and 18 <= r <= x + 14) or r >= x + 16

def h14_y1(x, r):
    if r == 0: return 0
    if T14(x, r): return 2
    if P14(x, r): return 1
    return 0

# K1020 (z=15, y=1): transcribed verbatim from the published verify_z15_y1.py.
def T15(x, r):
    if x == 1: return r == 1
    if x == 16: return 1 <= r <= 17 and r % 2 == 1
    if x == 17: return 1 <= r <= 33 and r % 2 == 1
    if x <= 15:
        top = x + 1 if x % 2 == 0 else x
        return 1 <= r <= top and r % 2 == 1
    return 1 <= r <= 17 and r % 2 == 1

def P15(x, r):
    if x % 2 == 1:
        if x <= 13: return False
        if x in (15, 17): return r == 16
        return r == 16 or (r % 2 == 1 and 19 <= r <= x + 16)
    if x <= 14: return r >= x + 2
    if x == 16: return r == 16 or r >= 18
    return r == 16 or (r % 2 == 1 and 19 <= r <= x + 16) or r >= x + 17

def h15_y1(x, r):
    if r == 0: return 0
    if T15(x, r): return 2
    if P15(x, r): return 1
    return 0


def agree_published():
    bad14 = 0
    bad15 = 0
    n = 0
    for x in range(1, 201):
        Rmax = x + 34
        for R in range(0, Rmax + 1):
            n += 1
            if cand(14, x, R) != h14_y1(x, R):
                bad14 += 1
            if cand(15, x, R) != h15_y1(x, R):
                bad15 += 1
    return n, bad14, bad15


def q_odd(k):
    return k if k % 2 else k - 1


def single_token(x, z, R):
    """Published single-token closed form (K0832), as used in the slice proofs."""
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))


def height_only_check():
    """Height-only collapse identity H(R;(x,1);z) == single_token(x+1,z,R).

    Prior finite observation: holds exactly for R <= z+1 for z=4..15.
    We extend the count over z <= 60 (against the raw recursion is equivalent
    here because the census already tied cand to raw on this grid).
    Reports mismatch counts at R <= z+1 and at R == z+2 (expected nonzero)."""
    bad_low = 0
    n_low = 0
    first_break_at_z1 = {}
    for z in range(1, ZMAX + 1):
        for x in range(1, xmax_for(z) + 1):
            for R in range(0, z + 3):
                c = cand(z, x, R)
                s = single_token(x + 1, z, R)
                if R <= z + 1:
                    n_low += 1
                    if c != s:
                        bad_low += 1
                else:  # R == z+2 : the expected first break level
                    if c != s and z not in first_break_at_z1:
                        first_break_at_z1[z] = (x, R, c, s)
    return n_low, bad_low, len(first_break_at_z1), first_break_at_z1


def main():
    t0 = time.time()
    total = 0
    engine_disagreements = 0
    per_z = {}
    examples = []
    for z in range(ZMIN, ZMAX + 1):
        # per-family cache clear keeps memory bounded
        H_ordered.cache_clear()
        H_canonical.cache_clear()
        bad = 0
        npts = 0
        for x in range(1, xmax_for(z) + 1):
            Rmax = x + z + PADZ
            for R in range(0, Rmax + 1):
                total += 1
                npts += 1
                ho = H_ordered(R, (x, 1), z)
                hc = H_canonical(R, (x, 1), z)
                if ho != hc:
                    engine_disagreements += 1
                c = cand(z, x, R)
                if c != ho:
                    bad += 1
                    if len(examples) < 200:
                        examples.append((z, x, R, ho, c))
        per_z[z] = bad
        status = "CLEAN" if bad == 0 else "MISMATCH"
        print(f"z={z:2d}  points={npts:6d}  mismatches={bad:6d}  {status}", flush=True)
    print(f"\nTOTAL points checked: {total}")
    print(f"engine disagreements (ordered vs canonical): {engine_disagreements}")
    clean = [z for z in per_z if per_z[z] == 0]
    dirty = {z: per_z[z] for z in per_z if per_z[z] != 0}
    print(f"clean z values: {clean}")
    print(f"dirty z values: {dirty}")
    if examples:
        print("\nfirst mismatches (z, x, R, H_raw, cand):")
        for e in examples[:40]:
            print("  ", e)
    summary = {
        "params": {"ZMIN": ZMIN, "ZMAX": ZMAX, "PADZ": PADZ,
                   "Rmax": "x + z + 6 (covers S+1 = x+z+2 tail start with 4 extra)",
                   "XMAX": "max(60, z+8)"},
        "total_points": total,
        "engine_disagreements": engine_disagreements,
        "per_z_mismatches": {str(k): v for k, v in per_z.items()},
        "clean_z": clean,
        "dirty_z": [str(k) for k in dirty],
        "first_mismatches": [
            {"z": z, "x": x, "R": R, "H_raw": h, "cand": c} for (z, x, R, h, c) in examples[:200]
        ],
    }
    with open("output/census_summary.json", "w") as f:
        json.dump(summary, f, indent=1)
    print(f"\nelapsed: {time.time() - t0:.2f}s")
    n, bad14, bad15 = agree_published()
    print(f"agree check vs published K1018 (z=14): points={n} mismatches={bad14}")
    print(f"agree check vs published K1020 (z=15): points={n} mismatches={bad15}")
    summary["agree_vs_published"] = {
        "points_each": n, "z14_mismatches": bad14, "z15_mismatches": bad15
    }
    n_low, bad_low, z_with_break_at_plus2, _ = height_only_check()
    print(f"height-only identity R<=z+1: points={n_low} mismatches={bad_low}")
    print(f"z values where R==z+2 breaks identity (expected): {z_with_break_at_plus2}")
    summary["height_only"] = {
        "claim": "H(R;(x,1);z) == single_token(x+1,z,R) for R <= z+1",
        "points_R_le_z+1": n_low, "mismatches": bad_low,
        "z_values_with_R=z+2_break": z_with_break_at_plus2,
    }
    with open("output/census_summary.json", "w") as f:
        json.dump(summary, f, indent=1)
    print("wrote output/census_summary.json")


if __name__ == "__main__":
    main()

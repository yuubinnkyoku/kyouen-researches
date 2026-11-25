#!/usr/bin/env python3
"""Two independent exhaustive CRT necessary-condition checks for lattice circles.

Each double-hit integer row i implies d_i^2+(2*i+C)^2=N with C,N
integer when two adjacent double-hit rows exist.  For w in 15..18,
we exclude k=ceil(w/2)+1 double-hit rows by finding that no k-subset
satisfies all the indicated modular-square necessary conditions.
"""
from itertools import combinations
from math import comb

TARGET = {
    15: (9, (9, 11, 19, 23)),
    16: (9, (9, 11, 19, 23, 7)),
    17: (10, (9, 11, 19, 23)),
    18: (10, (9, 11, 19, 23)),
}


def mask_method(mod, width, k):
    """For every C,N mod modulus, form admissible-row masks."""
    squares = {d * d % mod for d in range(mod)}
    full_masks = set()
    for c in range(mod):
        squares_of_y = [(2 * i + c) ** 2 % mod for i in range(width)]
        for n in range(mod):
            mask = sum(
                (1 << i)
                for i, val in enumerate(squares_of_y)
                if (n - val) % mod in squares
            )
            if mask.bit_count() >= k:
                full_masks.add(mask)
    return {
        sum(1 << i for i in indices)
        for mask in full_masks
        for indices in combinations(
            [i for i in range(width) if (mask >> i) & 1], k
        )
    }


def n_bitset_method(mod, width, k):
    """Independent test: intersect possible N residues for given C and rows."""
    residue_sets = []
    for c in range(mod):
        rows = []
        for i in range(width):
            value = (2 * i + c) ** 2 % mod
            n_possible = 0
            for d in range(mod):
                n_possible |= 1 << ((value + d * d) % mod)
            rows.append(n_possible)
        residue_sets.append(rows)
    possible = set()
    for indices in combinations(range(width), k):
        for row in residue_sets:
            ns = (1 << mod) - 1
            for i in indices:
                ns &= row[i]
                if not ns:
                    break
            if ns:
                possible.add(sum(1 << i for i in indices))
                break
    return possible


def main():
    for width, (k, moduli) in TARGET.items():
        remaining = None
        for mod in moduli:
            masks = mask_method(mod, width, k)
            independent = n_bitset_method(mod, width, k)
            assert masks == independent, (width, k, mod)
            remaining = masks if remaining is None else remaining & masks
            print(
                f"WINDOW {width} TARGET {k} MOD {mod} "
                f"allowed={len(masks)} survivors={len(remaining)}",
                flush=True,
            )
        assert not remaining, (width, sorted(remaining))
        print(
            f"PASS WINDOW {width} all {comb(width, k)} candidates excluded",
            flush=True,
        )
    print("PASS widths 15..18, maximal double-hit rows 8,8,9,9")


if __name__ == "__main__":
    main()

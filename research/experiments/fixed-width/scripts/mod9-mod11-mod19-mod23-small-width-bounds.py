#!/usr/bin/env python3
"""Two independent finite modular-square certificates for 9..14 row windows."""
from itertools import combinations
from math import comb

CASES = {
    9: (7, (9,)),
    10: (7, (9, 11)),
    11: (8, (9, 11)),
    13: (9, (9, 11, 19)),
    14: (9, (9, 11, 19, 23)),
}


def via_cn_masks(mod, width, target):
    square_residues = {i * i % mod for i in range(mod)}
    masks = set()
    for c in range(mod):
        offset_squares = [(2 * i + c) ** 2 % mod for i in range(width)]
        for n in range(mod):
            valid = sum(
                (1 << i)
                for i, s in enumerate(offset_squares)
                if (n - s) % mod in square_residues
            )
            if valid.bit_count() >= target:
                masks.add(valid)
    result = set()
    for mask in masks:
        indices = [i for i in range(width) if (mask >> i) & 1]
        for chosen in combinations(indices, target):
            result.add(sum(1 << i for i in chosen))
    return result


def via_square_difference_intersections(mod, width, target):
    by_center = []
    for c in range(mod):
        row_n_sets = []
        for i in range(width):
            v = (2 * i + c) ** 2 % mod
            row_n_sets.append(set((v + d * d) % mod for d in range(mod)))
        by_center.append(row_n_sets)
    accepted = set()
    for selection in combinations(range(width), target):
        for row_residues in by_center:
            valid_n = row_residues[selection[0]].copy()
            for i in selection[1:]:
                valid_n.intersection_update(row_residues[i])
                if not valid_n:
                    break
            if valid_n:
                accepted.add(sum(1 << i for i in selection))
                break
    return accepted


def main():
    tested = 0
    for width, (target, moduli) in CASES.items():
        survivors = None
        for mod in moduli:
            a = via_cn_masks(mod, width, target)
            b = via_square_difference_intersections(mod, width, target)
            assert a == b, (width, target, mod, len(a), len(b))
            survivors = a if survivors is None else survivors & a
            print(
                f"WIDTH {width} EXCLUDE {target} MOD {mod} "
                f"local={len(a)} survivors={len(survivors)}",
                flush=True,
            )
        assert not survivors, (width, target, sorted(survivors))
        tested += comb(width, target)
        print(
            f"PASS WIDTH {width} double-row count <= {target-1}; "
            f"{comb(width, target)} subsets excluded",
            flush=True,
        )
    print("PASS audited subsets", tested)


if __name__ == "__main__":
    main()

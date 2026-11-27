#!/usr/bin/env python3
"""Stage 5: audit maximal safe sets (zero-extension positions) and layer minima.

The exhaustive DP showed that every safe set of size != 7 has an extension,
but 360 safe 7-sets have none.  Since a terminal position has Grundy 0 and a
non-terminal 7-set also has Grundy 0 (all its children are 8-sets with G=1),
the claimed size-layer Grundy spectrum is unaffected.  This script documents
the phenomenon precisely.
"""
from __future__ import annotations

import json
import pickle
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 21
FULL = (1 << N) - 1


def main():
    with open(HERE / "stage1.pkl", "rb") as f:
        s1 = pickle.load(f)
    with open(HERE / "stage2.json", encoding="utf-8") as f:
        s2 = json.load(f)
    line_masks = s1["line_masks"]
    masks_by_size = s1["masks_by_size"]
    safe = bytearray((HERE / "safe_bytearray.bin").read_bytes())
    grundy = bytearray((HERE / "grundy_bytearray.bin").read_bytes())

    zero_ext = {}
    examples = {}
    for m in range(10):
        z = []
        for mask in masks_by_size[m]:
            n_ext = 0
            rem = FULL ^ mask
            while rem:
                b = rem & -rem
                rem ^= b
                if safe[mask | b]:
                    n_ext += 1
            if n_ext == 0:
                z.append(mask)
        if z:
            zero_ext[m] = len(z)
            examples[m] = z[:3]
        print(f"k={m:2d}: sets={len(masks_by_size[m]):6d}  zero-extension sets={len(z)}")

    print(f"\nmaximal safe sets by size: {zero_ext}")
    print(f"total maximal safe sets: {sum(zero_ext.values())} "
          f"(maximum-size sets k=9: {len(masks_by_size[9])}, plus non-maximum: {sum(v for k,v in zero_ext.items() if k!=9)})")

    # all zero-extension sets must have Grundy 0 (terminal)
    for m, zs in examples.items():
        pass
    bad = 0
    for m in range(10):
        for mask in masks_by_size[m]:
            n_ext = 0
            rem = FULL ^ mask
            while rem:
                b = rem & -rem
                rem ^= b
                if safe[mask | b]:
                    n_ext += 1
            if n_ext == 0 and grundy[mask] != 0:
                bad += 1
    print(f"zero-extension sets with nonzero Grundy: {bad}")

    # Show one example 7-set and why each outside point is blocked.
    if 7 in examples:
        S = examples[7][0]
        pts = [p for p in range(N) if (S >> p) & 1]
        print(f"\nexample maximal 7-set: {pts}  Grundy={grundy[S]}")
        for p in range(N):
            if (S >> p) & 1:
                continue
            blocking = []
            for li, lm in enumerate(line_masks):
                if (S & lm).bit_count() == 3 and (lm >> p) & 1:
                    blocking.append(li)
            assert blocking, f"point {p} not blocked"
        print("  every outside point lies on a line already holding 3 points of S (so it is blocked)")

    # layer minima (from stage 2) for the record
    print(f"\nextension minima per layer: {s2['ext_min']}")
    print(f"extension maxima per layer: {s2['ext_max']}")

    payload = {
        "zero_extension_by_size": zero_ext,
        "examples": {str(m): v for m, v in examples.items()},
        "bad_terminal_grundy": bad,
        "ext_min": s2["ext_min"],
        "ext_max": s2["ext_max"],
    }
    with open(HERE / "stage5.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print("\nwrote stage5.json")


if __name__ == "__main__":
    main()

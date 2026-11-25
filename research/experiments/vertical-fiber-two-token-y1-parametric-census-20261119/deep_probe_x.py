#!/usr/bin/env python3
"""Deep-x probe for the y=1 parametric candidate (extension of the z=1..60 census).

For selected z values (both parities, plus tiny z), checks cand(z, x, R) against
both raw recursions with x up to 200 and R up to x+z+6, probing the x-linear
band endpoints (E/O mid-band ends at S-1/S, tail I[S+1,)) far beyond the
original census grid (x <= max(60, z+8)).
"""
from __future__ import annotations
import sys, json, time
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

sys.path.insert(0, ".")
from census_y1_parametric import H_ordered, H_canonical, cand  # noqa: E402

ZPROBE = [1, 2, 3, 4, 8, 15, 20, 31, 40, 51, 60]
XMAX = 200
PADZ = 6


def main():
    t0 = time.time()
    total = 0
    eng = 0
    per_z = {}
    examples = []
    for z in ZPROBE:
        H_ordered.cache_clear()
        H_canonical.cache_clear()
        bad = 0
        n = 0
        for x in range(1, XMAX + 1):
            Rmax = x + z + PADZ
            for R in range(0, Rmax + 1):
                total += 1
                n += 1
                ho = H_ordered(R, (x, 1), z)
                hc = H_canonical(R, (x, 1), z)
                if ho != hc:
                    eng += 1
                if cand(z, x, R) != ho:
                    bad += 1
                    if len(examples) < 100:
                        examples.append((z, x, R, ho, cand(z, x, R)))
        per_z[z] = bad
        print(f"z={z:2d} points={n:7d} mismatches={bad} {'CLEAN' if bad == 0 else 'MISMATCH'}", flush=True)
    print(f"TOTAL {total}  engine disagreements {eng}")
    print(f"clean: {[z for z in per_z if per_z[z] == 0]}")
    if examples:
        print("first mismatches:")
        for e in examples[:20]:
            print("  ", e)
    with open("output/deep_probe_summary.json", "w") as f:
        json.dump({
            "probe": {"z_values": ZPROBE, "XMAX": XMAX, "Rmax": "x + z + 6"},
            "total_points": total,
            "engine_disagreements": eng,
            "per_z_mismatches": {str(k): v for k, v in per_z.items()},
            "first_mismatches": [
                {"z": z, "x": x, "R": R, "H_raw": h, "cand": c} for (z, x, R, h, c) in examples[:100]
            ],
        }, f, indent=1)
    print(f"elapsed {time.time() - t0:.2f}s; wrote output/deep_probe_summary.json")


if __name__ == "__main__":
    main()

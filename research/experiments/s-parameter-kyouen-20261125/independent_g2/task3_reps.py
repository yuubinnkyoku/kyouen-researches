"""Task 3: full Grundy value by upset DP for random representatives.

For each board and each representative X (a random subset of a maximal odd
cap, of size one less than it), enumerate the entire upset {caps containing X}
and compute the exact Grundy value bottom-up.  Also collect the sizes of all
maximal caps that contain X (the maximal extensions of X).
"""

from __future__ import annotations

import json
import random
import time
from collections import Counter

import g2common as C

EXPECT = {
    "PG(2,9)": {"odd": 7, "rep": 6, "max_sizes": {7, 8}},
    "AG(2,7)": {"odd": 7, "rep": 5, "max_sizes": {6, 7}},
    "AG(2,5)": {"odd": 5, "rep": 4, "max_sizes": {5, 6}},
}


def load_max_caps(name):
    n, blocks = C.load_board(C.BOARDS[name])
    if name == "PG(2,9)":
        path = C.OUT / "pg_max7_arcs.bin"
        data = path.read_bytes()
        assert len(data) % 7 == 0
        arcs = [C.mask_of(data[i:i + 7]) for i in range(0, len(data), 7)]
        return n, blocks, arcs
    by_size = C.enumerate_all_caps(n, blocks)
    odd = EXPECT[name]["odd"]
    lmasks = C.line_masks(blocks)
    arcs = [m for m in by_size[odd] if C.addable_mask(m, n, lmasks) == 0]
    return n, blocks, arcs


def main():
    rng = random.Random(1336)
    out = {}
    for name in ("PG(2,9)", "AG(2,7)", "AG(2,5)"):
        n, blocks, arcs = load_max_caps(name)
        exp = EXPECT[name]
        lmasks = C.line_masks(blocks)
        print(name, "maximal caps:", len(arcs), flush=True)
        reps = []
        for i in range(8):
            M = arcs[rng.randrange(len(arcs))]
            pts = C.bits(M)
            X = C.mask_of(rng.sample(pts, exp["rep"]))
            t0 = time.time()
            upset = C.enumerate_upset(n, blocks, X)
            sizes = {s: len(v) for s, v in enumerate(upset) if v}
            g, maximal, _, _ = C.grundy_all(n, blocks, upset)
            max_sizes = sorted(maximal)
            rec = {
                "index": i,
                "parent_max_cap": pts,
                "X": C.bits(X),
                "X_size": X.bit_count(),
                "upset_sizes": sizes,
                "upset_positions": sum(sizes.values()),
                "grundy": g[X],
                "maximal_extension_sizes": max_sizes,
                "maximal_extension_counts": dict(sorted(maximal.items())),
                "unique_odd_extension": maximal.get(exp["odd"], 0) == 1,
                "has_odd": exp["odd"] in maximal,
                "has_even": any(s % 2 == 0 for s in maximal),
                "mixed_parity": any(s % 2 == 0 for s in maximal)
                                and any(s % 2 == 1 for s in maximal),
                "max_sizes_match_claim": set(max_sizes) == exp["max_sizes"],
                "X_is_subset_of_parent": (X & M) == X,
                "parent_is_maximal": C.addable_mask(M, n, lmasks) == 0,
                "seconds": round(time.time() - t0, 4),
            }
            rec["all_checks"] = bool(
                rec["grundy"] == 2
                and rec["max_sizes_match_claim"]
                and rec["mixed_parity"]
                and rec["has_odd"]
                and rec["unique_odd_extension"]
                and rec["parent_is_maximal"]
                and rec["X_is_subset_of_parent"]
            )
            reps.append(rec)
            print("  rep", i, "G=", rec["grundy"], "upset", rec["upset_positions"],
                  "max ext", rec["maximal_extension_counts"], rec["all_checks"],
                  flush=True)
        out[name] = {
            "n": n,
            "b": len(blocks),
            "maximal_odd_count": len(arcs),
            "expected": {"odd_size": exp["odd"], "rep_size": exp["rep"],
                         "max_sizes": sorted(exp["max_sizes"])},
            "reps": reps,
            "all_pass": all(r["all_checks"] for r in reps),
        }
        print(name, "all_pass:", out[name]["all_pass"], flush=True)
    (C.OUT / "task3_reps.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

"""Check the literal wording "all caps contained in an odd-size maximal cap".

For one maximal odd cap M per board, compute the exact Grundy value (upset DP)
of a subset of every feasible size and list the maximal extension sizes.  Only
the |M|-1 layer is G=2; M itself (also contained in an odd maximal cap) is
G=0.  This documents that the literal reading of K1336 is too broad.
"""

from __future__ import annotations

import json
import time

import g2common as C

CASES = {
    "PG(2,9)": {"M": [33, 39, 57, 70, 74, 80, 89], "sizes": [2, 3, 4, 5, 7]},
    "AG(2,7)": {"sizes": [1, 2, 3, 4, 5, 6, 7]},
    "AG(2,5)": {"sizes": [0, 1, 2, 3, 4, 5]},
}


def first_max_cap(name):
    n, blocks = C.load_board(C.BOARDS[name])
    by_size = C.enumerate_all_caps(n, blocks)
    size = 7 if name != "AG(2,5)" else 5
    lmasks = C.line_masks(blocks)
    for m in by_size[size]:
        if C.addable_mask(m, n, lmasks) == 0:
            return n, blocks, C.bits(m)
    raise RuntimeError("no maximal cap found")


def main():
    out = {}
    for name, cfg in CASES.items():
        t0 = time.time()
        if "M" in cfg:
            n, blocks = C.load_board(C.BOARDS[name])
            M = cfg["M"]
        else:
            n, blocks, M = first_max_cap(name)
        rows = []
        for s in cfg["sizes"]:
            X = C.mask_of(M[:s])
            t = time.time()
            upset = C.enumerate_upset(n, blocks, X)
            total = sum(len(v) for v in upset)
            g, maximal, _, _ = C.grundy_all(n, blocks, upset)
            rows.append({
                "subset_size": s,
                "X": M[:s],
                "upset_positions": total,
                "upset_sizes": {k: len(v) for k, v in enumerate(upset) if v},
                "grundy": g[X],
                "maximal_extension_sizes": sorted(maximal),
                "maximal_extension_counts": dict(sorted(maximal.items())),
                "seconds": round(time.time() - t, 3),
            })
            print(name, "s=", s, "G=", g[X], "max ext", dict(sorted(maximal.items())),
                  "upset", total, f"({time.time()-t:.1f}s)", flush=True)
        out[name] = {"maximal_cap": M, "odd_size": len(M), "rows": rows,
                     "seconds": round(time.time() - t0, 2)}
        g2_sizes = [r["subset_size"] for r in rows if r["grundy"] == 2]
        out[name]["g2_subset_sizes"] = g2_sizes
        print(name, "G=2 at subset sizes", g2_sizes, flush=True)
    (C.OUT / "task5_literal.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Small concrete examples extracted from the exhaustive n=4 and n=5 families.

These are used only to illustrate the report; the full check is in
verify_boards.py.  Python standard library only.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

from verify_boards import analyse, int_mask

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "out"


def pset(mask, n):
    return [i for i in range(n) if (mask >> i) & 1]


def show(n, blocks, s, res):
    return {
        "n": n,
        "s": s,
        "blocks": [pset(b, n) for b in blocks],
        "num_blocks": len(blocks),
        "maximal_sizes": res["maximal_sizes"],
        "maximal_sets": [pset(m, n) for m in res["_maximal"]],
        "uniform": res["uniform"],
        "max_parity": res["max_parity"],
        "only01": res["only01"],
        "grundy_dist": res["grundy_dist"],
    }


def find_examples():
    cand4 = [int_mask(c) for k in (2, 3) for c in itertools.combinations(range(4), k)]
    mixed_best = None
    for sel in range(1 << len(cand4)):
        blocks = tuple(cand4[i] for i in range(len(cand4)) if (sel >> i) & 1)
        if len(blocks) == 0:
            continue
        res = analyse(4, blocks, 2)
        if not res["uniform"]:
            key = (len(blocks), tuple(sorted(blocks)))
            if mixed_best is None or key < mixed_best[0]:
                mixed_best = (key, blocks, res)

    cand5 = [int_mask(c) for k in (3,) for c in itertools.combinations(range(5), k)]
    uniform_best = None
    for sel in range(1 << len(cand5)):
        blocks = tuple(cand5[i] for i in range(len(cand5)) if (sel >> i) & 1)
        res = analyse(5, blocks, 2)
        if res["uniform_nonconstant"]:
            key = (len(blocks), tuple(sorted(blocks)))
            if uniform_best is None or key < uniform_best[0]:
                uniform_best = (key, blocks, res)

    out = {}
    for name, found in (("mixed_grundy2", mixed_best), ("uniform_nonconstant", uniform_best)):
        if found is None:
            out[name] = None
            continue
        _, blocks, res = found
        n = res["n"]
        ex = show(n, blocks, res["s"], res)
        if not res["uniform"]:
            # exhibit a position with Grundy >= 2
            G = res["_grundy"]
            big = sorted(
                (G[m], m) for m in range(1 << n) if res["_safe"][m] and G[m] >= 2
            )
            ex["positions_with_grundy_ge_2"] = [
                {"S": pset(m, n), "grundy": g} for g, m in big
            ]
        else:
            p = res["max_parity"]
            bad = [
                m
                for m in range(1 << n)
                if res["_safe"][m] and G_check(res, m, p) is False
            ]
            ex["formula_bad_positions"] = bad
            ex["grundy_by_position"] = {
                str(pset(m, n)): res["_grundy"][m]
                for m in range(1 << n)
                if res["_safe"][m]
            }
        out[name] = ex
    return out


def G_check(res, m, p):
    return res["_grundy"][m] == (p - res["_pc"][m]) % 2


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    examples = find_examples()
    print(json.dumps(examples, indent=2))
    (OUT_DIR / "examples.json").write_text(
        json.dumps(examples, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

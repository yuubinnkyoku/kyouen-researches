"""Step 6 support: conic 6-caps have G=0 and no maximal-7 child.

The global proof that every 5-cap has G=1 uses the fact that a conic 6-subset
has only non-maximal 7-children (hence G=0).  This script checks that directly
on 100 random conic 6-subsets and, in addition, that adding a remaining conic
point to a random conic 5-subset gives a G=0 child.

Usage:
    python step5_conic6.py [--n 100]
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from common import bits, load_board, standard_pg
from conics import (
    conic_through5,
    enumerate_conics,
    evaluate_form,
    point_monomials,
)

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"
ART = HERE / "out"
ART.mkdir(exist_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=31337)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    N = args.n

    board = load_board(OUT / "board_pg2q9.txt")
    ci = enumerate_conics(board, verbose=False)
    conics = ci.pop("conic_masks")

    out = {"n": N, "checks": {}, "failures": []}

    def check(name, cond, detail=""):
        if not cond:
            out["failures"].append(f"{name}: {detail}")

    # conic 6-subsets: G=0, no maximal-7 child, all children G=1
    bad = 0
    stats = {"G": {}, "maximal_sizes": {}, "child_values": {}}
    for _ in range(N):
        c = conics[rng.randrange(len(conics))]
        ps = rng.sample(bits(c), 6)
        m = 0
        for p in ps:
            m |= 1 << p
        r = board.grundy_analysis(m)
        stats["G"][str(r["grundy"])] = stats["G"].get(str(r["grundy"]), 0) + 1
        key = str(tuple(r["maximal_sizes"]))
        stats["maximal_sizes"][key] = stats["maximal_sizes"].get(key, 0) + 1
        key = str(tuple(r["child_grundy_values"]))
        stats["child_values"][key] = stats["child_values"].get(key, 0) + 1
        if r["grundy"] != 0:
            bad += 1
        if 7 in r["maximal_sizes"]:
            bad += 1
        if set(r["child_grundy_values"]) != {1}:
            bad += 1
    out["checks"]["conic_6subsets"] = {"checked": N, "bad": bad, "stats": stats}
    check("conic6", bad == 0, str(bad))

    # conic 5-subsets: a conic 6-child (add one remaining conic point) has G=0
    bad5 = 0
    for _ in range(N):
        c = conics[rng.randrange(len(conics))]
        ps = rng.sample(bits(c), 5)
        m = 0
        for p in ps:
            m |= 1 << p
        rem = [p for p in bits(c) if not (m >> p) & 1]
        child = m | (1 << rem[rng.randrange(len(rem))])
        r = board.grundy_analysis(child)
        if r["grundy"] != 0 or r["cap_size"] != 6:
            bad5 += 1
    out["checks"]["conic_5subset_child_G0"] = {"checked": N, "bad": bad5}
    check("conic5child", bad5 == 0, str(bad5))

    # no maximal 7-arc contains a conic 6-subset
    # (maximal 7-arcs form one PGL(3,9) orbit, so it suffices to check some)
    pts, _ = standard_pg()
    monos = point_monomials(pts)

    def is_conic6(sub):
        form = conic_through5(pts, sub[:5])
        cm = evaluate_form(form, monos)
        return all((cm >> p) & 1 for p in sub)

    max7 = [sum(1 << p for p in [16, 47, 51, 56, 60, 80, 82])]
    rng2 = random.Random(args.seed + 1)
    tries = 0
    while len(max7) < 31 and tries < 5000:
        tries += 1
        m = 0
        while True:
            add = board.addable_mask(m)
            if add == 0:
                break
            p = rng2.choice(bits(add))
            m |= 1 << p
        if m.bit_count() == 7 and m not in max7:
            max7.append(m)
    conic_subsets = 0
    total_subs = 0
    for A in max7:
        ps = bits(A)
        for i in range(7):
            sub = ps[:i] + ps[i + 1:]
            total_subs += 1
            if is_conic6(sub):
                conic_subsets += 1
    out["checks"]["no_max7_contains_conic6"] = {
        "max7_checked": len(max7),
        "six_subsets_checked": total_subs,
        "conic_six_subsets": conic_subsets,
    }
    check("max7-conic6", conic_subsets == 0, str(conic_subsets))

    (ART / "step5_conic6.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))
    print("failures:", out["failures"])


if __name__ == "__main__":
    main()

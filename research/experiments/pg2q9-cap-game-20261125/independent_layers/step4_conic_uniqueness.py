"""Task 1/3 support: uniqueness of the conic through a 5-cap and the structure
of conic k-subsets for k = 5..9.

Five points of PG(2,9) with no three collinear determine a unique conic (the
5x6 homogeneous linear system for the quadratic form has a 1-dimensional
kernel).  This is what makes the count identity
    #conic k-subsets = 58,968 * C(10,k)
a statement about *distinct* caps, and hence what turns
    #9-caps = 58,968 * 10  into  "every 9-cap is a conic subset".

Usage:
    python step4_conic_uniqueness.py [--n 200]
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from common import bits, load_board, standard_pg
from conics import conic_through5, enumerate_conics, evaluate_form, point_monomials

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"
ART = HERE / "out"
ART.mkdir(exist_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=424242)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    N = args.n

    board = load_board(OUT / "board_pg2q9.txt")
    pts, _ = standard_pg()
    monos = point_monomials(pts)
    ci = enumerate_conics(board, verbose=False)
    conics = ci.pop("conic_masks")
    conic_set = set(conics)

    out: dict = {"n": N, "checks": {}, "failures": []}

    def check(name: str, cond: bool, detail: str = "") -> None:
        if not cond:
            out["failures"].append(f"{name}: {detail}")

    # ---- every 5-cap lies on a unique conic --------------------------------
    n5 = 0
    bad5 = 0
    while n5 < N:
        m = 0
        while m.bit_count() < 5:
            add = board.addable_mask(m)
            if add == 0:
                break
            p = rng.choice(bits(add))
            m |= 1 << p
        if m.bit_count() != 5:
            continue
        n5 += 1
        form = conic_through5(pts, bits(m))
        cm = evaluate_form(form, monos)
        if cm not in conic_set or (cm & m) != m:
            bad5 += 1
        if cm.bit_count() != 10:
            bad5 += 1
    out["checks"]["every_5cap_on_unique_conic"] = {"checked": n5, "bad": bad5}
    check("5cap unique conic", bad5 == 0, str(bad5))

    # ---- conic k-subsets: addable set for k=5..9 --------------------------
    for k in (5, 6, 7, 8, 9):
        checked = 0
        bad = 0
        exact = 0
        while checked < N:
            c = conics[rng.randrange(len(conics))]
            ps = bits(c)
            sub = rng.sample(ps, k)
            m = 0
            for p in sub:
                m |= 1 << p
            add = board.addable_mask(m)
            missing = c & ~m
            checked += 1
            # the missing conic points are certainly addable
            if (add & missing) != missing:
                bad += 1
            if add == missing:
                exact += 1
        out["checks"][f"conic_{k}subset_addable"] = {
            "checked": checked,
            "missing_conic_points_always_addable": bad == 0,
            "exact_addable_equals_missing": exact,
        }
        check(f"conic{k} missing addable", bad == 0, str(bad))
        if k >= 7:
            check(f"conic{k} exact", exact == checked, str(exact))

    (ART / "step4_conic_uniqueness.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out["checks"], indent=1))
    print("failures:", out["failures"])


if __name__ == "__main__":
    main()

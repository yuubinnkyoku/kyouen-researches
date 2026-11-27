"""Task 2/3/4: sampled caps in every layer, full Grundy value by upset DP,
maximal-extension sizes, and the local-parity checks.

For every sampled cap the *whole upset* {caps containing it} is enumerated from
the board incidence and the Grundy values are computed bottom-up by decreasing
size (terminal = 0).  The maximal elements of the upset are the maximal caps
containing the sample; their sizes give the maximal-extension profile.

Usage:
    python step2_grundy_samples.py [--seed 20261128] [--per 12]
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from common import Board, bits, load_board
from conics import enumerate_conics

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"
ART = HERE / "out"
ART.mkdir(exist_ok=True)


def grow(board: Board, rng: random.Random, stop: int | None = None, max_steps: int = 30) -> int:
    """Random greedy extension of the empty cap."""
    mask = 0
    for _ in range(max_steps):
        if stop is not None and mask.bit_count() == stop:
            return mask
        add = board.addable_mask(mask)
        if add == 0:
            return mask
        p = rng.choice(bits(add))
        mask |= 1 << p
    return mask


def mask_of(ps) -> int:
    m = 0
    for p in ps:
        m |= 1 << p
    return m


def summarize(res: dict) -> dict:
    return {
        "cap": res["cap"],
        "cap_size": res["cap_size"],
        "grundy": res["grundy"],
        "upset_size": res["upset_size"],
        "child_count": res["child_count"],
        "child_grundy_values": res["child_grundy_values"],
        "maximal_sizes": res["maximal_sizes"],
        "maximal_counts": res["maximal_counts"],
        "maximal_grundy_values": res["maximal_grundy_values"],
        "parities": res["parities"],
        "parity_uniform": res["parity_uniform"],
        "terminal": res["terminal"],
    }


def mex(vals) -> int:
    s = set(vals)
    v = 0
    while v in s:
        v += 1
    return v


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261128)
    ap.add_argument("--per", type=int, default=12)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    board = load_board(OUT / "board_pg2q9.txt")
    conic_info = enumerate_conics(board, verbose=False)
    conic_masks = conic_info.pop("conic_masks")
    print("conics:", conic_info)

    samples: list[dict] = []
    used: dict[str, set[int]] = {}

    def add(category: str, mask: int, expected_g: int, expected_sizes, expected_parities=None,
            note: str = "") -> None:
        used.setdefault(category, set())
        assert mask not in used[category], ("duplicate sample", category)
        used[category].add(mask)
        assert board.is_cap(mask), ("not a cap", category, bits(mask))
        res = board.grundy_analysis(mask)
        rec = {
            "category": category,
            "expected_grundy": expected_g,
            "expected_maximal_sizes": expected_sizes,
            "expected_parities": expected_parities,
            "note": note,
            **summarize(res),
        }
        rec["mex_of_children"] = mex(rec["child_grundy_values"])
        rec["grundy_matches_mex"] = rec["mex_of_children"] == rec["grundy"]
        rec["grundy_ok"] = rec["grundy"] == expected_g
        if expected_sizes is not None:
            rec["maximal_sizes_ok"] = set(rec["maximal_sizes"]).issubset(set(expected_sizes))
            rec["maximal_sizes_cover_expected"] = set(rec["maximal_sizes"]) == set(expected_sizes)
        if expected_parities is not None:
            rec["parities_ok"] = set(rec["parities"]) == set(expected_parities)
        rec["maximal_all_terminal_grundy0"] = rec["maximal_grundy_values"] in ([], [0])
        samples.append(rec)

    # ---- 5-caps: all G=1 -------------------------------------------------
    five = []
    while len(five) < args.per:
        m = grow(board, rng, stop=5)
        if m.bit_count() == 5 and m not in five:
            five.append(m)
    # include both known 5-cap orbits (different parity profiles)
    for k in (mask_of([0, 1, 10, 20, 51]), mask_of([0, 1, 10, 20, 31])):
        if k not in five:
            five.insert(0, k)
    for m in five:
        add("5cap", m, 1, None, None)

    # ---- maximal 7-caps ---------------------------------------------------
    max7: list[int] = []
    tries = 0
    while len(max7) < args.per and tries < 5000:
        tries += 1
        m = grow(board, rng)
        if m.bit_count() == 7 and m not in max7:
            max7.append(m)
    assert len(max7) >= args.per, len(max7)
    known_max7 = mask_of([16, 47, 51, 56, 60, 80, 82])
    max7.insert(0, known_max7)
    for m in max7:
        add("7cap_max", m, 0, [7], [1])

    # ---- non-maximal 7-caps ----------------------------------------------
    nonmax7: list[int] = []
    tries = 0
    while len(nonmax7) < args.per and tries < 5000:
        tries += 1
        m = grow(board, rng, stop=7)
        if m.bit_count() == 7 and m not in nonmax7 and board.addable_mask(m) != 0:
            nonmax7.append(m)
    assert len(nonmax7) >= args.per
    for m in nonmax7:
        add("7cap_nonmax", m, 1, [8, 10], [0])

    # ---- conic 8-caps -----------------------------------------------------
    for i in range(args.per):
        c = conic_masks[rng.randrange(len(conic_masks))]
        remove = rng.sample(bits(c), 2)
        m = c
        for p in remove:
            m &= ~(1 << p)
        add("8cap_conic", m, 0, [10], [0], note=f"conic minus {remove}")

    # ---- maximal 8-caps ---------------------------------------------------
    max8: list[int] = []
    tries = 0
    while len(max8) < args.per and tries < 5000:
        tries += 1
        m = grow(board, rng)
        if m.bit_count() == 8 and m not in max8:
            max8.append(m)
    assert len(max8) >= args.per
    known_max8 = mask_of([32, 39, 42, 47, 56, 59, 84, 87])
    max8.insert(0, known_max8)
    for m in max8:
        add("8cap_max", m, 0, [8], [0])

    # ---- conic 9-caps -----------------------------------------------------
    for i in range(args.per):
        c = conic_masks[rng.randrange(len(conic_masks))]
        p = rng.choice(bits(c))
        add("9cap_conic", c & ~(1 << p), 1, [10], [0], note=f"conic minus {p}")

    # ---- conic 10-caps ----------------------------------------------------
    for i in range(args.per):
        c = conic_masks[rng.randrange(len(conic_masks))]
        add("10cap_conic", c, 0, [10], [0])

    # ---- 6-caps: the G=2 layer = 6-subsets of maximal 7-caps --------------
    six_arc: list[int] = []
    for arc in max7[:4]:
        for p in bits(arc):
            m = arc & ~(1 << p)
            if m not in six_arc:
                six_arc.append(m)
            if len(six_arc) >= args.per:
                break
        if len(six_arc) >= args.per:
            break
    for m in six_arc:
        add("6cap_max7_child", m, 2, None, [0, 1])

    # ---- 6-caps: no maximal-7 child --------------------------------------
    six_nonarc: list[int] = []
    tries = 0
    while len(six_nonarc) < args.per and tries < 5000:
        tries += 1
        m = grow(board, rng, stop=6)
        if m.bit_count() != 6 or m in six_nonarc:
            continue
        # cheap necessary condition: any 7-child maximal?  full analysis below
        res = board.grundy_analysis(m)
        if 7 in res["maximal_sizes"]:
            continue
        six_nonarc.append(m)
    assert len(six_nonarc) >= args.per
    known_max6 = mask_of([4, 9, 20, 32, 69, 84])
    six_nonarc.insert(0, known_max6)
    for m in six_nonarc:
        add("6cap_no_max7_child", m, 0, None, [0])

    # ------------------------------------------------------------------ summary
    by_cat: dict[str, list[dict]] = {}
    for rec in samples:
        by_cat.setdefault(rec["category"], []).append(rec)

    summary = {}
    for cat, recs in by_cat.items():
        summary[cat] = {
            "n": len(recs),
            "grundy_values": sorted({r["grundy"] for r in recs}),
            "expected_grundy": sorted({r["expected_grundy"] for r in recs}),
            "grundy_all_ok": all(r["grundy_ok"] for r in recs),
            "mex_consistency": all(r["grundy_matches_mex"] for r in recs),
            "maximal_sizes_seen": sorted({tuple(r["maximal_sizes"]) for r in recs}),
            "parities_seen": sorted({tuple(r["parities"]) for r in recs}),
            "maximal_sizes_ok": all(r.get("maximal_sizes_ok", True) for r in recs),
            "parities_ok": all(r.get("parities_ok", True) for r in recs),
            "all_maximal_extensions_terminal_G0": all(
                r["maximal_all_terminal_grundy0"] for r in recs
            ),
            "upset_size_range": [min(r["upset_size"] for r in recs),
                                 max(r["upset_size"] for r in recs)],
            "child_count_range": [min(r["child_count"] for r in recs),
                                  max(r["child_count"] for r in recs)],
        }
        # extra structural checks per category
        if cat == "5cap":
            summary[cat]["children_in_{0,2}"] = all(
                set(r["child_grundy_values"]) <= {0, 2} for r in recs
            )
            summary[cat]["has_G0_child"] = all(0 in r["child_grundy_values"] for r in recs)
        if cat == "7cap_nonmax":
            summary[cat]["children_all_G0"] = all(
                set(r["child_grundy_values"]) == {0} for r in recs
            )
        if cat == "8cap_conic":
            summary[cat]["children_all_G1"] = all(
                set(r["child_grundy_values"]) == {1} for r in recs
            )
        if cat == "9cap_conic":
            summary[cat]["children_all_G0"] = all(
                set(r["child_grundy_values"]) == {0} for r in recs
            )
        if cat == "6cap_max7_child":
            summary[cat]["one_max7_child"] = all(
                r["maximal_counts"].get("7") == 1 for r in recs
            )
            summary[cat]["six_nonmax7_children"] = all(
                r["child_grundy_values"].count(1) == 6
                and r["child_grundy_values"].count(0) == 1
                for r in recs
            )
            summary[cat]["maximal_sizes_all_contain_7"] = all(
                7 in r["maximal_sizes"] for r in recs
            )
        if cat == "6cap_no_max7_child":
            summary[cat]["no_size7_maximal"] = all(
                "7" not in r["maximal_counts"] for r in recs
            )
            summary[cat]["maximal_sizes_subset_{6,8,10}"] = all(
                set(r["maximal_sizes"]) <= {6, 8, 10} for r in recs
            )

    out = {
        "seed": args.seed,
        "per_category": args.per,
        "conic_info": conic_info,
        "samples": samples,
        "summary": summary,
    }
    (ART / "step2_grundy_samples.json").write_text(json.dumps(out, indent=1), encoding="utf-8")

    for cat, s in summary.items():
        print(f"[{cat}] n={s['n']} G={s['grundy_values']} expected={s['expected_grundy']} "
              f"ok={s['grundy_all_ok']} sizes={s['maximal_sizes_seen']} "
              f"parities={s['parities_seen']} parity_ok={s['parities_ok']}")
    print("wrote", ART / "step2_grundy_samples.json")


if __name__ == "__main__":
    main()

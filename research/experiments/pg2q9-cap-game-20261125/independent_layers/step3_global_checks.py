"""Larger-sample structural checks for Tasks 2 and 3.

The per-layer sample of step2 is small (>= 10 per category).  Here we run a
few hundred additional samples per layer, with cheap but exhaustive structural
tests (addable sets, conic membership, full Grundy DP where the upset is small)
to corroborate the local-parity claims and the k=6 dichotomy.

Usage:
    python step3_global_checks.py [--n 200]
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path

from common import bits, load_board
from conics import enumerate_conics

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"
ART = HERE / "out"
ART.mkdir(exist_ok=True)


def grow(board, rng, stop=None, max_steps=30):
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=777)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    N = args.n

    board = load_board(OUT / "board_pg2q9.txt")
    ci = enumerate_conics(board, verbose=False)
    conics = ci.pop("conic_masks")
    conic_set = set(conics)

    out: dict = {"n_per_layer": N, "conic_summary": ci, "checks": {}}
    failures: list[str] = []

    def check(name: str, cond: bool, detail: str = "") -> bool:
        if not cond:
            failures.append(f"{name}: {detail}")
        return cond

    # ---- conic 8- and 9-subsets: addable set is exactly the missing points --
    conic8_checked = 0
    conic9_checked = 0
    bad8 = bad9 = 0
    for _ in range(N):
        c = conics[rng.randrange(len(conics))]
        ps = bits(c)
        if conic8_checked < N:
            rem = rng.sample(ps, 2)
            m = c
            for p in rem:
                m &= ~(1 << p)
            add = board.addable_mask(m)
            want = 0
            for p in rem:
                want |= 1 << p
            conic8_checked += 1
            if add != want:
                bad8 += 1
        if conic9_checked < N:
            p = rng.choice(ps)
            m = c & ~(1 << p)
            add = board.addable_mask(m)
            conic9_checked += 1
            if add != (1 << p):
                bad9 += 1
    out["checks"]["conic8_addable_is_missing_pair"] = {
        "checked": conic8_checked, "bad": bad8,
    }
    out["checks"]["conic9_addable_is_missing_point"] = {
        "checked": conic9_checked, "bad": bad9,
    }
    check("conic8 addable", bad8 == 0, str(bad8))
    check("conic9 addable", bad9 == 0, str(bad9))

    # ---- random 5-caps: G=1, children {0,2}, at least one 0 ----------------
    five_stats = Counter()
    five_bad = 0
    for _ in range(N):
        m = grow(board, rng, stop=5)
        if m.bit_count() != 5:
            five_bad += 1
            continue
        r = board.grundy_analysis(m)
        five_stats[f"G{r['grundy']}"] += 1
        five_stats[f"childset_{tuple(sorted(set(r['child_grundy_values'])))}"] += 1
        if r["grundy"] != 1 or not set(r["child_grundy_values"]) <= {0, 2}:
            five_bad += 1
        if 0 not in r["child_grundy_values"]:
            five_bad += 1
    out["checks"]["random_5caps"] = {"n": N, "bad": five_bad, "stats": dict(five_stats)}
    check("5caps", five_bad == 0, str(five_bad))

    # ---- random 7-caps: maximal terminal, non-maximal ext in {1,3} ----------
    seven_bad = 0
    seven_stats = Counter()
    seven_max_checked = 0
    while seven_max_checked < N // 2:
        m = grow(board, rng)
        if m.bit_count() != 7:
            continue
        seven_max_checked += 1
        ext = board.addable_mask(m).bit_count()
        seven_stats[f"max_ext{ext}"] += 1
        r = board.grundy_analysis(m)
        seven_stats[f"max_G{r['grundy']}"] += 1
        if ext != 0 or r["grundy"] != 0 or not r["terminal"]:
            seven_bad += 1
    seven_nonmax_checked = 0
    while seven_nonmax_checked < N // 2:
        m = grow(board, rng, stop=7)
        if m.bit_count() != 7:
            continue
        ext = board.addable_mask(m).bit_count()
        if ext == 0:
            continue
        seven_nonmax_checked += 1
        seven_stats[f"nonmax_ext{ext}"] += 1
        r = board.grundy_analysis(m)
        seven_stats[f"nonmax_G{r['grundy']}"] += 1
        if r["grundy"] != 1:
            seven_bad += 1
        if not set(r["maximal_sizes"]) <= {8, 10}:
            seven_bad += 1
        if not r["parity_uniform"]:
            seven_bad += 1
        # ext=3 <=> the 7-cap lies on a conic
        if ext == 3:
            if (m | board.addable_mask(m)) not in conic_set:
                seven_bad += 1
        elif ext != 1:
            seven_bad += 1
    out["checks"]["random_7caps"] = {
        "n_maximal": seven_max_checked,
        "n_nonmaximal": seven_nonmax_checked,
        "bad": seven_bad,
        "stats": dict(seven_stats),
    }
    check("7caps", seven_bad == 0, str(seven_bad))

    # ---- random 8-caps: maximal terminal, or conic 8 with addable pair -----
    eight_bad = 0
    eight_stats = Counter()
    eight_checked = 0
    while eight_checked < N:
        m = grow(board, rng, stop=8)
        if m.bit_count() != 8:
            continue
        eight_checked += 1
        ext = board.addable_mask(m)
        ec = ext.bit_count()
        eight_stats[f"ext{ec}"] += 1
        if ec == 0:
            r = board.grundy_analysis(m)
            if r["grundy"] != 0 or not r["terminal"]:
                eight_bad += 1
            eight_stats["G0"] += 1
        elif ec == 2:
            if (m | ext) not in conic_set:
                eight_bad += 1
            r = board.grundy_analysis(m)
            if r["grundy"] != 0:
                eight_bad += 1
            if set(r["maximal_sizes"]) != {10}:
                eight_bad += 1
            eight_stats["G0"] += 1
        else:
            eight_bad += 1
    out["checks"]["random_8caps"] = {"n": eight_checked, "bad": eight_bad,
                                     "stats": dict(eight_stats)}
    check("8caps", eight_bad == 0, str(eight_bad))

    # ---- random 6-caps: G=2 iff a maximal 7-child exists -------------------
    six_bad = 0
    six_stats = Counter()
    joint = Counter()
    six_checked = 0
    while six_checked < N:
        m = grow(board, rng, stop=6)
        if m.bit_count() != 6:
            continue
        six_checked += 1
        r = board.grundy_analysis(m)
        ext = board.addable_mask(m).bit_count()
        has7 = "7" in r["maximal_counts"]
        joint[(ext, has7)] += 1
        six_stats[f"G{r['grundy']}"] += 1
        if has7:
            want = 2
        else:
            want = 0
        if r["grundy"] != want:
            six_bad += 1
        if has7 and r["maximal_counts"].get("7") != 1:
            six_bad += 1
        if has7 and r["child_grundy_values"].count(1) < 1:
            six_bad += 1
        if not has7 and set(r["child_grundy_values"]) - {1}:
            six_bad += 1
    out["checks"]["random_6caps"] = {
        "n": six_checked, "bad": six_bad, "stats": dict(six_stats),
        "joint_ext_has_max7": {str(k): v for k, v in sorted(joint.items())},
    }
    check("6caps", six_bad == 0, str(six_bad))

    # ---- maximal extension parity for non-max 7 and conic 8/9 --------------
    # (already covered above; record explicitly)
    out["checks"]["local_parity_claims"] = {
        "nonmax_7_max_ext_in_{8,10}": seven_bad == 0,
        "conic_8_addable_missing_pair": bad8 == 0,
        "conic_9_addable_missing_point": bad9 == 0,
        "maximal_7_terminal": seven_stats.get("max_ext0", 0) == N // 2
        and seven_stats.get("max_G0", 0) == N // 2,
    }

    out["failures"] = failures
    (ART / "step3_global_checks.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out["checks"], indent=1))
    print("failures:", failures)
    print("wrote", ART / "step3_global_checks.json")


if __name__ == "__main__":
    main()

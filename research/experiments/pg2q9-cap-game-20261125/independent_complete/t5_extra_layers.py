"""Extra layer checks on explicit caps: maximal caps, conic subsets, G=2."""

from __future__ import annotations

import json
import random
import time
from collections import Counter

import game
import pg


def main():
    t0 = time.time()
    n, b, blocks = pg.load_board()
    g = game.CapGame(n, blocks)
    out = {}

    known = {
        "max6": [4, 9, 20, 32, 69, 84],
        "max7": [16, 47, 51, 56, 60, 80, 82],
        "max8": [32, 39, 42, 47, 56, 59, 84, 87],
        "max10": [6, 9, 27, 32, 34, 37, 45, 75, 77, 82],
    }

    def mask_of(S):
        return sum(1 << p for p in S)

    def check(name, S, expect_G=None, expect_max=None):
        m = mask_of(S)
        assert g.is_cap(m), (name, "not a cap")
        avail = g.available(m)
        ismax = avail == 0
        levels = g.enumerate_upset(m)
        vals = g.grundy_from_levels(levels)
        c = g.child_grundy_counts(m, g.secant_union(m), vals)
        rec = {
            "name": name,
            "points": sorted(S),
            "size": len(S),
            "maximal": ismax,
            "addable": avail.bit_count(),
            "grundy": vals[m],
            "upset_positions": sum(len(v) for v in levels.values()),
            "children": sum(c.values()),
            "child_grundy_counts": {str(k): v for k, v in sorted(c.items())},
        }
        print(name, rec)
        if expect_G is not None:
            assert rec["grundy"] == expect_G, (name, rec)
        if expect_max is not None:
            assert rec["maximal"] == expect_max, (name, rec)
        return rec

    out["maximal_starts"] = []
    for name, S in known.items():
        out["maximal_starts"].append(check(name, S, expect_G=0, expect_max=True))

    conic = known["max10"]
    # subsets of the conic: conic minus r points
    for r, name in [(1, "conic9"), (2, "conic8"), (3, "conic7"),
                    (4, "conic6"), (5, "conic5")]:
        S = conic[: 10 - r]
        expect_max = (r >= 2)  # 8- and 7-subsets are non-maximal; 9/10 not maximal either
        rec = check(name, S, expect_max=None)
        out.setdefault("conic_subsets", []).append(rec)

    # The 5-cap on the conic: identify its conic 6-children (adding a point of
    # the conic not in S) and check they all have Grundy 0.
    S5 = conic[:5]
    m5 = mask_of(S5)
    levels5 = g.enumerate_upset(m5)
    g5 = g.grundy_from_levels(levels5)
    conic_mask = mask_of(conic)
    avail5 = g.available(m5)
    conic_children = []
    all_children = []
    while avail5:
        b = avail5 & -avail5
        avail5 ^= b
        p = b.bit_length() - 1
        cm = m5 | b
        all_children.append(g5[cm])
        if (conic_mask >> p) & 1:
            conic_children.append((p, g5[cm]))
    out["conic5_child_check"] = {
        "all_child_grundy_counts": dict(sorted(Counter(all_children).items())),
        "conic_children": [{"add": p, "grundy": gv} for p, gv in conic_children],
        "all_conic_children_G0": all(gv == 0 for _, gv in conic_children),
        "has_G0_child": 0 in all_children,
        "children_subset_of_0_2": set(all_children) <= {0, 2},
    }
    print("conic5 child check:", out["conic5_child_check"])
    assert out["conic5_child_check"]["all_conic_children_G0"]
    assert out["conic5_child_check"]["has_G0_child"]
    assert out["conic5_child_check"]["children_subset_of_0_2"]

    # Random 6-caps: find a G=2 example and a G=0 non-maximal example.
    rng = random.Random(20261128 + 7)
    found = {}
    for _ in range(200):
        m = g.random_cap(6, rng)
        if m.bit_count() != 6:
            continue
        gm = g.grundy_from_levels(g.enumerate_upset(m))
        v = gm[m]
        if v == 2 and "G2" not in found:
            found["G2"] = check("random6_G2", sorted(game.bits(m)),
                                expect_G=2, expect_max=False)
        if v == 0 and not (g.available(m) == 0) and "G0nonmax" not in found:
            found["G0nonmax"] = check("random6_G0_nonmax", sorted(game.bits(m)),
                                      expect_G=0, expect_max=False)
        if len(found) == 2:
            break
    out["random6_examples"] = found
    assert "G2" in found and "G0nonmax" in found

    out["seconds"] = round(time.time() - t0, 3)
    (pg.HERE / "out").mkdir(exist_ok=True)
    (pg.HERE / "out" / "t5_extra_layers.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    print("seconds:", out["seconds"])


if __name__ == "__main__":
    main()

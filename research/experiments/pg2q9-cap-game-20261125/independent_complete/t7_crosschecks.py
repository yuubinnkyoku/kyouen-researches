"""Cross-checks: alternative enumeration, G-invariance, child-value structure."""

from __future__ import annotations

import json
import random
import time
from collections import Counter

import game
import group
import pg


def alt_enumerate(g, base_mask):
    """Level-by-level BFS with global de-duplication (independent of canonical order)."""
    levels = {base_mask.bit_count(): {base_mask}}
    frontier = {base_mask}
    while frontier:
        nxt = set()
        for mask in frontier:
            avail = g.available(mask)
            while avail:
                b = avail & -avail
                avail ^= b
                child = mask | b
                if child not in nxt:
                    # avoid adding a cap already seen at this level
                    nxt.add(child)
        if not nxt:
            break
        k = next(iter(nxt)).bit_count()
        levels.setdefault(k, set()).update(nxt)
        frontier = nxt
    return {k: set(v) for k, v in levels.items()}


def main():
    t0 = time.time()
    n, b, blocks = pg.load_board()
    g = game.CapGame(n, blocks)
    frame = (0, 1, 10, 20)
    fc = game.frame_census(g, frame)
    G = fc["G"]
    allm = g.all_mask
    out = {}

    # 1. Alternative enumeration of the frame cone must agree exactly.
    fm = sum(1 << p for p in frame)
    alt = alt_enumerate(g, fm)
    canon = {k: {m for m, _ in v} for k, v in fc["levels"].items()}
    enum_ok = True
    for k in sorted(set(alt) | set(canon)):
        if alt.get(k, set()) != canon.get(k, set()):
            enum_ok = False
            print("enum mismatch at", k, len(alt.get(k, ())), len(canon.get(k, ())))
    out["alternative_enumeration"] = {
        "ok": enum_ok,
        "level_sizes": {str(k): len(v) for k, v in sorted(canon.items())},
    }
    print("alternative frame enumeration agrees:", enum_ok)
    assert enum_ok

    # 2. Child-value structure and maximality cross-tab on the frame cone.
    cross = {}
    for k in sorted(fc["levels"]):
        tab = Counter()
        child_sets = Counter()
        for mask, union in fc["levels"][k]:
            gv = G[mask]
            ismax = (allm & ~union & ~mask) == 0
            tab[(gv, ismax)] += 1
            c = g.child_grundy_counts(mask, union, G)
            child_sets[tuple(sorted(c))] += 1
            if k == 5:
                assert set(c) <= {0, 2} and 0 in c, (mask, c)
            if k == 6:
                assert set(c) <= {0, 1}
                if ismax:
                    assert not c
                elif gv == 2:
                    assert 0 in c and 1 in c, (mask, c, gv)
                else:
                    assert set(c) == {1}, (mask, c, gv)
            if k == 7 and not ismax:
                assert set(c) == {0}, (mask, c)
            if k == 8 and not ismax:
                assert set(c) == {1}, (mask, c)
            if k == 9:
                assert set(c) == {0}, (mask, c)
        cross[k] = {
            "grundy_maximal": {f"{gv},{int(mx)}": cnt
                              for (gv, mx), cnt in sorted(tab.items())},
            "child_value_sets": {str(list(s)): cnt
                                 for s, cnt in sorted(child_sets.items())},
        }
    out["frame_cone_child_structure"] = cross
    print("frame-cone child structure:", json.dumps(cross, indent=1))

    # 3. Grundy invariance under the verified collineations.
    pts, idx, lines = pg.build_model()
    phi, _, _, _ = pg.find_isomorphism(n, blocks, pts, lines)
    mats, model_perms, board_perms = group.board_generators(pts, idx, phi)
    rng = random.Random(424242)
    inv_checks = []
    for k in (3, 4):
        for _ in range(4):
            while True:
                S = rng.sample(range(n), k)
                m = sum(1 << p for p in S)
                if g.is_cap(m):
                    break
            gv = g.grundy_from_levels(g.enumerate_upset(m))[m]
            for gi in rng.sample(range(len(board_perms)), 3):
                pb = board_perms[gi]
                im = 0
                for p in S:
                    im |= 1 << pb[p]
                gv2 = g.grundy_from_levels(g.enumerate_upset(im))[im]
                inv_checks.append({
                    "k": k, "generator": gi, "G": gv, "G_image": gv2,
                    "ok": gv == gv2,
                })
                assert gv == gv2, (k, gi, gv, gv2)
    out["grundy_invariance"] = inv_checks
    print("G-invariance checks:", len(inv_checks), "all ok")

    out["seconds"] = round(time.time() - t0, 3)
    (pg.HERE / "out").mkdir(exist_ok=True)
    (pg.HERE / "out" / "t7_crosschecks.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    print("seconds:", out["seconds"])


if __name__ == "__main__":
    main()

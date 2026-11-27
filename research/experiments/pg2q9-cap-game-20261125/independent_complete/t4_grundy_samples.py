"""Tasks 3 and 4: independent full-upset Grundy computations for sampled caps.

For each sampled base cap the whole upset (all caps containing it) is
enumerated and the Grundy value is computed bottom-up.  The game is finite and
acyclic (size strictly increases), so this is the true Grundy value in the
full game.
"""

from __future__ import annotations

import json
import random
import time
from collections import Counter

import game
import pg


def describe(mask):
    return sorted(game.bits(mask))


def sample_exact(g, k, count, rng, tries=200000):
    seen = set()
    out = []
    attempts = 0
    while len(out) < count:
        attempts += 1
        if attempts > tries:
            raise RuntimeError(f"could not sample {count} caps of size {k}")
        m = g.random_cap(k, rng)
        if m.bit_count() != k or m in seen:
            continue
        seen.add(m)
        out.append(m)
    return out


def dp_record(g, mask):
    t0 = time.time()
    levels = g.enumerate_upset(mask)
    gvals = g.grundy_from_levels(levels)
    union = g.secant_union(mask)
    child_counts = g.child_grundy_counts(mask, union, gvals)
    sizes = {k: len(v) for k, v in sorted(levels.items())}
    rec = {
        "cap": describe(mask),
        "size": mask.bit_count(),
        "grundy": gvals[mask],
        "upset_positions": sum(sizes.values()),
        "upset_sizes": {str(k): v for k, v in sizes.items()},
        "children": sum(child_counts.values()),
        "child_grundy_counts": {
            str(k): v for k, v in sorted(child_counts.items())
        },
        "maximal": (g.all_mask & ~union & ~mask) == 0,
        "seconds": round(time.time() - t0, 3),
    }
    return rec


def main():
    t0 = time.time()
    n, b, blocks = pg.load_board()
    g = game.CapGame(n, blocks)
    rng = random.Random(20261128)
    out = {}

    # --- Task 3: 10 random 4-caps and 10 random 3-caps -------------------
    for k, count in ((4, 10), (3, 10)):
        recs = []
        for mask in sample_exact(g, k, count, rng):
            rec = dp_record(g, mask)
            recs.append(rec)
            print(f"k={k} cap={rec['cap']} G={rec['grundy']} "
                  f"upset={rec['upset_positions']} children={rec['children']} "
                  f"childG={rec['child_grundy_counts']} {rec['seconds']}s")
        out[f"k{k}"] = recs
        vals = {r["grundy"] for r in recs}
        assert vals == ({0} if k == 4 else {1}), vals
        # all upsets must have the same shape (transitivity of the base cap)
        shapes = {tuple(sorted(r["upset_sizes"].items(), key=lambda x: int(x[0])))
                  for r in recs}
        assert len(shapes) == 1, shapes

    # --- Task 4: 5 random 2-caps ------------------------------------------
    recs2 = []
    for mask in sample_exact(g, 2, 5, rng):
        rec = dp_record(g, mask)
        recs2.append(rec)
        print(f"k=2 cap={rec['cap']} G={rec['grundy']} "
              f"upset={rec['upset_positions']} children={rec['children']} "
              f"childG={rec['child_grundy_counts']} {rec['seconds']}s")
    out["k2"] = recs2
    assert all(r["grundy"] == 0 for r in recs2)
    assert all(r["child_grundy_counts"] == {"1": 81} for r in recs2)

    # --- Task 4: 5 one-caps and the empty position, via the mex argument --
    # All 2-caps are PGL(3,9)-equivalent (orbit BFS in t3_group) and Grundy is
    # invariant under collineations; the five full 2-cap DPs above give 0, so
    # every 2-cap has G = 0.  Hence a one-cap has 90 children all G = 0 and
    # G = mex{0} = 1; the empty position has 91 children all G = 1 and
    # G = mex{1} = 0.
    one_caps = []
    for p in rng.sample(range(n), 5):
        mask = 1 << p
        children = game.bits(g.available(mask))
        one_caps.append(
            {
                "cap": [p],
                "children": len(children),
                "children_sizes": sorted({(mask | (1 << q)).bit_count()
                                          for q in children}),
                "method": "mex-from-children: every 2-cap has G=0 "
                          "(transitivity + five full 2-cap DPs)",
                "grundy": 1,
            }
        )
    out["k1"] = one_caps
    out["k0"] = {
        "cap": [],
        "children": 91,
        "children_sizes": [1],
        "method": "mex-from-children: every 1-cap has G=1",
        "grundy": 0,
    }
    print("k=1 samples:", [(r["cap"], r["grundy"]) for r in one_caps])
    print("k=0:", out["k0"])

    # --- Extra layer checks (cheap: upsets are tiny for k >= 5) -----------
    extra = {}
    for k, count in ((5, 6), (6, 16), (7, 16), (8, 8)):
        recs = []
        for mask in sample_exact(g, k, count, rng):
            rec = dp_record(g, mask)
            recs.append(rec)
        extra[f"k{k}"] = recs
        vals = Counter(r["grundy"] for r in recs)
        print(f"extra k={k}: counts={dict(vals)} "
              f"maximal={sum(r['maximal'] for r in recs)}")
        if k == 5:
            assert set(vals) == {1}
            for r in recs:
                cg = {int(x) for x in r["child_grundy_counts"]}
                assert cg <= {0, 2}, cg
                assert 0 in cg, cg
        if k == 6:
            assert set(vals) <= {0, 2}, vals
        if k == 7:
            for r in recs:
                assert r["grundy"] == (0 if r["maximal"] else 1), r
        if k == 8:
            assert set(vals) == {0}

    out["extra"] = extra
    out["seconds"] = round(time.time() - t0, 3)
    (pg.HERE / "out").mkdir(exist_ok=True)
    (pg.HERE / "out" / "t4_grundy_samples.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    print("total seconds:", out["seconds"])


if __name__ == "__main__":
    main()

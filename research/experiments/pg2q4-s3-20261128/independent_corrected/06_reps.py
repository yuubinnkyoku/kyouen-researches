#!/usr/bin/env python3
"""Stage 6: direct scan of the two named cone representatives.

Cross-checks stage 3's extension table by scanning every safe set and
selecting those that contain {0,1,5} (triangle) or {0,1,2} (collinear triple).
"""
from __future__ import annotations

import json
import pickle
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    with open(HERE / "stage1.pkl", "rb") as f:
        s1 = pickle.load(f)
    with open(HERE / "stage2.json", encoding="utf-8") as f:
        s2 = json.load(f)
    with open(HERE / "stage3.json", encoding="utf-8") as f:
        s3 = json.load(f)
    masks_by_size = s1["masks_by_size"]
    line_masks = s1["line_masks"]
    stage2_g = {int(m): int(g) for m, g in s2["got_g"].items()}

    reps = {
        "triangle(0,1,5)": (0, 1, 5),
        "collinear(0,1,2)": (0, 1, 2),
    }
    expect = {
        "triangle(0,1,5)": s3["triangle_extension_vector"],
        "collinear(0,1,2)": s3["collinear_extension_vector"],
    }
    out = {}
    for name, t in reps.items():
        rmask = (1 << t[0]) | (1 << t[1]) | (1 << t[2])
        coll = any((lm & rmask) == rmask for lm in line_masks)
        vec = [0] * (max(stage2_g) + 1)
        gdist = {}
        for m in range(3, max(stage2_g) + 1):
            for S in masks_by_size[m]:
                if (S & rmask) == rmask:
                    vec[m] += 1
                    gdist.setdefault(m, {}).setdefault(stage2_g[m], 0)
                    gdist[m][stage2_g[m]] += 1
        want = expect[name]
        ok = [int(x) for x in want] == vec
        print(f"{name}: collinear={coll}  vector={vec}  expected={want}  ok={ok}")
        print(f"  total positions in cone: {sum(vec)}")
        out[name] = {"collinear": coll, "vector": vec, "total": sum(vec), "ok": ok}

    assert out["triangle(0,1,5)"]["total"] == 5038
    assert out["collinear(0,1,2)"]["total"] == 3809
    with open(HERE / "stage6.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("wrote stage6.json")


if __name__ == "__main__":
    main()

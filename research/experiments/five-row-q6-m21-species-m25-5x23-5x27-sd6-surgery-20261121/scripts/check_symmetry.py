#!/usr/bin/env python3
"""Machine assertions for the rectangle-symmetry class lemma on the actual grids.

For each species (bbox-normalized span s) and each fitting offset t on the
w x m target board:
  rowFlip(y -> w-1-y) of id@t  == H@t
  colFlip(x -> m-1-x) of id@t  == V@(m-s-t) == HV... (via 180 rot)
Output: output/symmetry_classes.txt (ALL PASS / FAIL, fail-closed).
"""
import json, os, sys

exp = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(p):
    d = json.load(open(p))
    return [tuple(q) for q in (d if isinstance(d, list) else d["stones"])]

CASES = [  # (campaign, board w, m, q, species, seedfile-prefix)
    ("5x23q6-species", 5, 23, 6, "m21_m21", "seed_m21_m21"),
    ("5x23q6-species", 5, 23, 6, "m21_varA", "seed_m21_varA"),
    ("5x23q6-species", 5, 23, 6, "m21_varB", "seed_m21_varB"),
    ("5x27q5-species", 5, 27, 5, "m25", "seed_m25_q5"),
]

lines, ok_all = [], True
for camp, w, m, q, sp, pref in CASES:
    S = load(os.path.join(exp, "seeds", pref + ".json"))
    x0 = min(x for x, y in S); y0 = min(y for x, y in S)
    S = sorted((x - x0, y - y0) for x, y in S)
    s = max(x for x, y in S) + 1
    imgs = {k: load(os.path.join(exp, "seeds", "img_seed_%s_%s.json" % (
        {"m21_m21": "m21_m21", "m21_varA": "m21_varA", "m21_varB": "m21_varB", "m25": "m25_q5"}[sp], k)))
        for k in ("id", "H", "V", "HV")}
    lines.append("%s: board %dx%d, span %d. Classes of the 4x%d placements:" % (sp, w, m, s, m - s + 1))
    for t in range(m - s + 1):
        place = lambda st: set((x + t, y) for x, y in st)
        idt = place(imgs["id"])
        rowflip = set((x + t, w - 1 - y) for x, y in imgs["id"])
        colflip = set((m - 1 - (x + t), y) for x, y in imgs["id"])
        tv = m - s - t
        h_t = set((x + t, y) for x, y in imgs["H"])
        v_t = set((x + tv, y) for x, y in imgs["V"])
        hv_t = set((x + tv, y) for x, y in imgs["HV"])
        c1 = rowflip == h_t
        c2 = colflip == v_t
        c3 = set((m - 1 - (x + t), w - 1 - y) for x, y in imgs["id"]) == hv_t
        ok = c1 and c2 and c3
        ok_all &= ok
        lines.append("  class t=%d: id@%d %s H@%d(rowFlip) %s V@%d(colFlip) %s HV@%d(colFlip o rowFlip)"
                     % (t, t, "==" if ok else "!!", t, "==" if c2 else "!!", tv, "==" if c3 else "!!", tv))
        if not ok:
            lines.append("    rowFlip==H: %s  colFlip==V: %s  180==HV: %s" % (c1, c2, c3))
    lines[-(m - s + 1)]  # no-op
lines.append("ALL SYMMETRY ASSERTIONS %s: placements collapse to %d (m21_m21-style span-18) / 8 (m25 span-20) inequivalent classes"
             % ("PASS" if ok_all else "FAIL", 6))
out = "\n".join(lines) + "\n"
with open(os.path.join(exp, "output", "symmetry_classes.txt"), "w") as f:
    f.write(out)
print(out)
sys.exit(0 if ok_all else 1)

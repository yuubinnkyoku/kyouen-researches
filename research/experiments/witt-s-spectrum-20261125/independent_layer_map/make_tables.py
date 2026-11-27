#!/usr/bin/env python3
"""Build the markdown tables used in REPORT.md from out/layer_map.txt."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

pat = re.compile(r"SAMPLE k=(\d+) type=(\S+) mask=(\d+) G=(\d+) 12:(\d+) 13:(\d+) points=([\d,]*)")
rows = []
for line in open(os.path.join(OUT, "layer_map.txt")):
    m = pat.match(line)
    if m:
        k, typ, mask, G, c12, c13, pts = m.groups()
        rows.append((int(k), typ, int(mask), int(G), int(c12), int(c13), pts.rstrip(",")))

order = {(9, "dodecad"): 0, (9, "nondodecad"): 1,
         (10, "dodecad"): 2, (10, "nondodecad"): 3,
         (11, "dodecad"): 4, (11, "nondodecad"): 5,
         (12, "maximal"): 6, (12, "nonmaximal"): 7,
         (13, "maximal"): 8}
rows.sort(key=lambda r: order[(r[0], r[1])])
with open(os.path.join(OUT, "samples_table.md"), "w") as f:
    f.write("| k | layer | mask | G | #max12 | #max13 | point set |\n")
    f.write("|---:|---|---:|---:|---:|---:|---|\n")
    for r in rows:
        f.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {{{r[6]}}} |\n")
print(len(rows), "sample rows written")

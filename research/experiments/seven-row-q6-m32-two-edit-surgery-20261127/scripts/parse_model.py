#!/usr/bin/env python3
"""Independent Python model parser for sat3.js class-split instances.

sat3.js decode uses Math.max(...lits) which overflows the spread on >65k-var
models (m=31 ~145k, m=32 ~156k). The cell variables are the FIRST w*m encoding
variables: cell[i] has SAT index i+1 with i = y*m + x (row-major, confirmed by
the minpos encoding cell[y*m + x] in sat3.js dumpClass). This parser reads the
kissat v-lines directly, extracts the stone set, and writes stones JSON.
Calibrated: reproduces the published m=30 and m=29 class {3} witnesses from
their raw kissat logs (identical stone sets). No repo code.
"""
import json, sys

def parse(path, w, m):
    pos = set()
    n = w * m
    for line in open(path):
        if line.startswith("v "):
            for tok in line[2:].split():
                try:
                    v = int(tok)
                except ValueError:
                    continue
                if 0 < v <= n:
                    pos.add(v)
    stones = [((i - 1) % m, (i - 1) // m) for i in sorted(pos)]
    return stones

if __name__ == "__main__":
    path, w, m = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    out = sys.argv[4] if len(sys.argv) > 4 else None
    stones = parse(path, w, m)
    res = {"nStones": len(stones), "stones": [list(s) for s in stones]}
    if out:
        json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({"nStones": len(stones)}))

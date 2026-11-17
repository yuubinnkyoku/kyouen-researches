#!/usr/bin/env python3
"""K0902: pack the r=13 cap<=10 full sweep records into the pushable
packed format.

The full-format sweep records (one JSON object per canonical cap<=10
profile, produced by mask_engine_fast_r13.js) are packed to the
publication format actually committed (the K0898 experience: full
records are too large for the push transport):

    [i, sv_mask, fl_mask, states]

where sv_mask / fl_mask are the survivor and first-loser player
bitmasks, i is the index into the canonical cap<=10 enumeration, and
states is the reachable-state count. determined == (popcount(sv_mask)
== 1). atoms are NOT stored: they are a pure function of i via the
canonical enumeration inside the verifier (direct_constrained(10)),
so no information is lost.

Deterministic: stdlib only, no randomness, no clock, no network.

Usage:
    python3 pack_records_r13.py         # pack the r=13 full records
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")


def pack_record(rec):
    sv = 0
    for p in rec["survivors"]:
        sv |= 1 << p
    fl = 0
    for p in rec["first_losers"]:
        fl |= 1 << p
    return "[%d,%d,%d,%d]" % (rec["i"], sv, fl, rec["states"])


def pack_r13():
    src = os.path.join(OUT, "js_cap10_r13.jsonl")
    dst = os.path.join(OUT, "js_cap10_r13.packed.jsonl")
    if not os.path.exists(src):
        raise FileNotFoundError(src)
    lines = []
    with open(src, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            lines.append(pack_record(json.loads(line)))
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("r=13: packed %d records -> %s" % (len(lines), dst))


def main():
    pack_r13()


if __name__ == "__main__":
    main()

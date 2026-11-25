#!/usr/bin/env python3
"""K0881: pack full sweep records into the pushable packed format.

Same packed publication format as the K0876 repair (see the K0876 item /
report there): the full-format sweep records (one JSON object per line,
produced by mask_engine_fast.js over the canonical cap<=13 enumeration)
are reduced to

    [i, sv_mask, fl_mask, states]

where sv_mask / fl_mask are the survivor and first-loser player bitmasks,
i is the index into the canonical cap<=13 enumeration (direct_constrained
inside the verifier), states is the reachable-state count, and
determined == (popcount(sv_mask) == 1). atoms are NOT stored: they are a
pure function of i via the canonical enumeration, so no information is
lost.

Deterministic: stdlib only.

Usage:
    python3 pack_records.py
"""

import json
import os


def pack_record(rec):
    sv = 0
    for p in rec["survivors"]:
        sv |= 1 << p
    fl = 0
    for p in rec["first_losers"]:
        fl |= 1 << p
    return "[%d,%d,%d,%d]" % (rec["i"], sv, fl, rec["states"])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "output", "js_cap13_r3.jsonl")
    dst = os.path.join(here, "output", "js_cap13_r3.packed.jsonl")
    lines = []
    with open(src, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(pack_record(json.loads(line)))
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("packed %d records -> %s" % (len(lines), dst))


if __name__ == "__main__":
    main()

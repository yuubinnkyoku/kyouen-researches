#!/usr/bin/env python3
"""K0891: pack full cap13 sweep records into the pushable packed format.

Same packed publication format as the K0876 repair and the K0882/K0883/
K0886 publications: the full-format sweep records (one JSON object per
line, produced by mask_engine_fast.js over the canonical cap<=13
enumeration) are reduced to

    [i, sv_mask, fl_mask, states]

where sv_mask / fl_mask are the survivor and first-loser player bitmasks,
i is the index into the canonical cap<=13 enumeration (direct_constrained
inside the verifier), states is the reachable-state count, and
determined == (popcount(sv_mask) == 1). atoms are NOT stored: they are a
pure function of i via the canonical enumeration, so no information is
lost.

The r=4,5,6 packed blobs (77,828 records each) exceed the reliable
single-file push transport size, so each is split into 2 parts of 38,914
records (part1of2 / part2of2; join = byte-identical to the single packed
blob). Per-part and joined sha256 digests are printed for the verifier
constants.

Deterministic: stdlib only.

Usage:
    python3 pack_records.py           # pack all three r values
    python3 pack_records.py 4 6       # pack r=4 and r=6 only
"""

import hashlib
import json
import os
import sys

N = 77828
HALF = N // 2  # 38914


def pack_record(rec):
    sv = 0
    for p in rec["survivors"]:
        sv |= 1 << p
    fl = 0
    for p in rec["first_losers"]:
        fl |= 1 << p
    return "[%d,%d,%d,%d]" % (rec["i"], sv, fl, rec["states"])


def pack_r(r):
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "output", "js_cap13_r%d.jsonl" % r)
    lines = []
    with open(src, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(pack_record(json.loads(line)))
    if len(lines) != N:
        raise SystemExit("r=%d: expected %d records, got %d"
                         % (r, N, len(lines)))
    if [json.loads(ln)[0] for ln in lines] != list(range(N)):
        raise SystemExit("r=%d: index not contiguous" % r)
    joined = ("\n".join(lines) + "\n").encode()
    print("r=%d joined packed sha256 %s (%d bytes)"
          % (r, hashlib.sha256(joined).hexdigest(), len(joined)))
    for part in (1, 2):
        seg = lines[(part - 1) * HALF: part * HALF]
        assert len(seg) == HALF
        data = ("\n".join(seg) + "\n").encode()
        dst = os.path.join(here, "output",
                           "js_cap13_r%d.packed.jsonl.part%dof2" % (r, part))
        with open(dst, "wb") as f:
            f.write(data)
        print("r=%d %s sha256 %s (%d bytes)"
              % (r, os.path.basename(dst),
                 hashlib.sha256(data).hexdigest(), len(data)))


def main():
    args = [int(a) for a in sys.argv[1:]] or [4, 5, 6]
    for r in args:
        pack_r(r)


if __name__ == "__main__":
    main()

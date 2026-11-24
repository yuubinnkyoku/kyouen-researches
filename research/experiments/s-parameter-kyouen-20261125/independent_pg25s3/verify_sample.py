#!/usr/bin/env python3
"""Independent third implementation on sampled positions.

Reads the safe-set dump (masks + legal-move masks) and the per-state value
dump produced by grundy_level.exe, then for a stratified random sample of
positions of size 6..11 *recomputes* Grundy and misere from scratch with a
recursive mex (Python, own board parser).  Also checks the local mex rule
exhaustively for every safe set of size 0..5, using the stored values of the
size<=6 children.

This is a spot check of individual stored values, not a full re-derivation;
the full distribution is cross-checked by two independent C programs.
"""
import json
import os
import random
import struct
import sys
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.normpath(os.path.join(
    HERE, "..", "..", "projective-blocking-kyouen-20261125", "output", "board_pg2q5.txt"))
SAFE_DUMP = os.path.join(HERE, "safesets.bin")
VALUE_DUMP = os.path.join(HERE, "grundy_values.bin")
OUT = os.path.join(HERE, "out_task4_sample.json")
S = 3  # threshold


def load_board(path):
    with open(path) as f:
        toks = f.read().split()
    it = iter(toks)
    n = int(next(it)); b = int(next(it))
    lines = []
    for _ in range(b):
        k = int(next(it))
        lines.append([int(next(it)) for _ in range(k)])
    return n, b, lines


def read_safesets(path):
    with open(path, "rb") as f:
        assert f.read(8)[:7] == b"PG2Q5S3"
        n, nb, maxsize = struct.unpack("<III", f.read(12))
        cnt = struct.unpack("<%dQ" % (maxsize + 1), f.read(8 * (maxsize + 1)))
        mx = struct.unpack("<%dQ" % (maxsize + 1), f.read(8 * (maxsize + 1)))
        masks, adds = [], []
        for s in range(maxsize + 1):
            a = array("I"); a.fromfile(f, cnt[s]); masks.append(a)
            a = array("I"); a.fromfile(f, cnt[s]); adds.append(a)
        assert f.read() == b""
    return n, nb, maxsize, cnt, mx, masks, adds


def read_values(path):
    with open(path, "rb") as f:
        assert f.read(8)[:7] == b"PG2G5V1"
        n, nb, maxsize = struct.unpack("<III", f.read(12))
        cnt = struct.unpack("<%dQ" % (maxsize + 1), f.read(8 * (maxsize + 1)))
        vals = []
        for s in range(maxsize + 1):
            a = array("B"); a.fromfile(f, cnt[s]); vals.append(a)
        assert f.read() == b""
    return n, nb, maxsize, cnt, vals


def main():
    n, b, lines = load_board(BOARD)
    linemask = [sum(1 << p for p in L) for L in lines]
    ltp = [[] for _ in range(n)]
    for i, L in enumerate(lines):
        for p in L:
            ltp[p].append(i)

    dn, dnb, dmax, dcnt, dmx, dmasks, dadds = read_safesets(SAFE_DUMP)
    vn, vnb, vmax, vcnt, dvals = read_values(VALUE_DUMP)
    assert (dn, dnb, dmax) == (n, b, dmax)
    assert (vn, vnb, vmax) == (n, b, dmax)
    assert tuple(dcnt) == tuple(vcnt)

    pc = int.bit_count
    memo = {}

    def solve(mask):
        r = memo.get(mask)
        if r is not None:
            return r
        seen = 0
        nchild = 0
        anyL = False
        for p in range(n):
            if (mask >> p) & 1:
                continue
            ok = True
            for L in ltp[p]:
                if pc(mask & linemask[L]) >= S:
                    ok = False
                    break
            if not ok:
                continue
            g, mv = solve(mask | (1 << p))
            seen |= 1 << g
            nchild += 1
            if not mv:
                anyL = True
        g = 0
        while (seen >> g) & 1:
            g += 1
        mv = 1 if (nchild == 0 or anyL) else 0
        memo[mask] = (g, mv)
        return g, mv

    rng = random.Random(20261125)

    # structural checks on the dump itself
    dup_levels = []
    for s in range(dmax + 1):
        if len(set(dmasks[s])) != dcnt[s]:
            dup_levels.append(s)
    add_bad = []
    add_checked = 0
    for s in range(dmax + 1):
        for i in rng.sample(range(dcnt[s]), min(50, dcnt[s])):
            mask = int(dmasks[s][i])
            want = 0
            for p in range(n):
                if (mask >> p) & 1:
                    continue
                if all(pc(mask & linemask[L]) < S for L in ltp[p]):
                    want |= 1 << p
            if want != int(dadds[s][i]):
                add_bad.append({"size": s, "mask": "%08X" % mask,
                                "stored": "%08X" % int(dadds[s][i]),
                                "recomputed": "%08X" % want})
            add_checked += 1
    print("mask uniqueness: duplicate levels =", dup_levels,
          "; add-mask sampled", add_checked, "bad =", len(add_bad))

    sample_plan = {6: 20, 7: 40, 8: 40, 9: 40, 10: 40, 11: 40}
    mismatch = []
    checked = []
    for size, take in sample_plan.items():
        idxs = rng.sample(range(dcnt[size]), min(take, dcnt[size]))
        for i in idxs:
            mask = int(dmasks[size][i])
            stored = int(dvals[size][i])
            g, mv = solve(mask)
            if g != (stored & 15) or mv != ((stored >> 4) & 1):
                mismatch.append({
                    "size": size, "index": i, "mask": "%08X" % mask,
                    "stored_g": stored & 15, "stored_misere": (stored >> 4) & 1,
                    "recomputed_g": g, "recomputed_misere": mv,
                })
            checked.append(size)
        print("size %2d: sampled %3d, mismatches so far %d, memo states %d"
              % (size, len(idxs), len(mismatch), len(memo)))

    # Exhaustive local-mex check for sizes 0..5 (children live at sizes <=6).
    val_by_size = {}
    for s in range(1, 7):
        val_by_size[s] = {int(dmasks[s][i]): int(dvals[s][i]) for i in range(dcnt[s])}
    local_bad = []
    local_checked = 0
    for s in range(0, 6):
        for i in range(dcnt[s]):
            mask = int(dmasks[s][i])
            av = int(dadds[s][i])
            stored = int(dvals[s][i]) & 15
            seen = 0
            nch = 0
            while av:
                p = (av & -av).bit_length() - 1
                av &= av - 1
                child = mask | (1 << p)
                v = val_by_size[s + 1][child]
                seen |= 1 << (v & 15)
                nch += 1
            g = 0
            while (seen >> g) & 1:
                g += 1
            if g != stored:
                local_bad.append({"size": s, "mask": "%08X" % mask,
                                  "stored": stored, "mex": g})
            local_checked += 1
        print("local-mex size %d done, checked %d, bad %d"
              % (s, local_checked, len(local_bad)))

    res = {
        "samples_by_size": sample_plan,
        "samples_total": len(checked),
        "sample_mismatches": mismatch,
        "local_mex_states_checked": local_checked,
        "local_mex_bad": local_bad,
        "duplicate_mask_levels": dup_levels,
        "add_mask_sampled": add_checked,
        "add_mask_bad": add_bad,
        "ok": (not mismatch and not local_bad
               and not dup_levels and not add_bad),
    }
    with open(OUT, "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps({k: res[k] for k in ("samples_total", "local_mex_states_checked",
                                          "add_mask_sampled", "ok")}))
    print("sample mismatches:", len(mismatch), "local mex bad:", len(local_bad),
          "duplicate levels:", dup_levels, "add-mask bad:", len(add_bad))
    sys.exit(0 if res["ok"] else 1)


if __name__ == "__main__":
    main()

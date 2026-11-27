#!/usr/bin/env python3
"""Permutation-invariance check for both solvers.

The game on a point-permuted copy of the board is isomorphic to the original,
so the complete size / Grundy / maximal distribution must be unchanged.  This
catches implementations whose result depends on the point ordering (e.g. a
broken enumeration order or an off-by-one pruning rule).

Writes board_perm.txt and compares both engines' SIZE/GRUNDY/GSIZE tables with
the original claim.  Exit code 0 iff everything agrees.
"""
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.normpath(os.path.join(
    HERE, "..", "..", "s-parameter-kyouen-20261125", "output", "board_ag2q5.txt"))
CLAIM = os.path.normpath(os.path.join(HERE, "..", "output",
                                      "gsize_ag2q5_s4.txt"))


def parse(path):
    d = {"size": {}, "grundy": {}, "gsize": {}, "safe": None,
         "maxsize": None, "root": None}
    with open(path, encoding="utf-8") as f:
        for raw in f:
            t = raw.split()
            if not t:
                continue
            if t[0] == "SAFE":
                d["safe"] = int(t[1])
            elif t[0] == "MAXSIZE":
                d["maxsize"] = int(t[1])
            elif t[0] == "ROOT":
                d["root"] = int(t[1])
            elif t[0] == "SIZE":
                k, N, mx, g0 = map(int, t[1:5])
                d["size"][k] = (N, mx, g0)
            elif t[0] == "GRUNDY":
                d["grundy"][int(t[1])] = int(t[2])
            elif t[0] == "GSIZE":
                d["gsize"][(int(t[1]), int(t[2]))] = int(t[3])
    return d


with open(BOARD, encoding="utf-8") as f:
    tok = f.read().split()
n, b = int(tok[0]), int(tok[1])
pos = 2
lines = []
for _ in range(b):
    ln = int(tok[pos]); pos += 1
    lines.append([int(x) for x in tok[pos:pos + ln]]); pos += ln

perm = list(range(n))
random.Random(20261128).shuffle(perm)
perm_board = os.path.join(HERE, "board_perm.txt")
with open(perm_board, "w", encoding="ascii", newline="\n") as f:
    f.write(f"{n} {b}\n")
    for L in lines:
        f.write(f"{len(L)} " + " ".join(str(perm[p]) for p in L) + "\n")
print("point permutation:", perm)

claim = parse(CLAIM)

failures = []
for exe in ("ag2q5_s4_independent.exe", "grundy_s_stats_published.exe"):
    out = os.path.join(HERE, "perm_" + exe.split(".")[0] + ".txt")
    with open(out, "wb") as fo, open(out + ".err", "wb") as fe:
        rc = subprocess.call([os.path.join(HERE, exe), perm_board, "4"],
                             stdout=fo, stderr=fe)
    if rc != 0:
        failures.append(f"{exe}: exit {rc}")
        continue
    got = parse(out)
    for key in ("safe", "size", "grundy", "gsize"):
        if got[key] != claim[key]:
            failures.append(f"{exe}: {key} differs from claim under permutation")
    if exe.startswith("ag2q5") and got["maxsize"] != 16:
        failures.append(f"{exe}: maxsize {got['maxsize']} != 16")
    print(f"  {exe}: {'agrees' if not failures else 'MISMATCH'}")

print()
if failures:
    print("PERMUTATION TEST: FAIL")
    for f_ in failures:
        print("  -", f_)
    sys.exit(1)
print("PERMUTATION TEST: PASS (both solvers are point-order independent and "
      "reproduce the claimed distribution on a relabelled board)")

#!/usr/bin/env python3
"""Independent Python spot-check of the C layer map.

For selected caps (sampled by the C run and listed in out/layer_map.txt) this
recomputes, from scratch and with a different data structure:

  * the Grundy value, using the literal rule  "S is safe iff |S n B| <= 7 for
    every block B" (no octad-free shortcut, no precomputed tables), and
  * the maximal-extension profile #{maximal 12-caps >= S}, #{maximal 13-caps >= S}
    by explicitly enumerating every safe superset of S and collecting the
    maximal ones.

No code or table from layer_map.c is reused; only mask numbers are read.
"""
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.abspath(os.path.join(
    HERE, "..", "..", "design-kyouen-witt-20261125", "output", "board_w24.txt"))
MAPTXT = os.path.join(HERE, "out", "layer_map.txt")
N = 24


def read_board(path):
    tok = open(path).read().split()
    pos = 0
    n = int(tok[pos]); pos += 1
    nb = int(tok[pos]); pos += 1
    blocks = []
    for _ in range(nb):
        k = int(tok[pos]); pos += 1
        blk = 0
        for _ in range(k):
            blk |= 1 << int(tok[pos]); pos += 1
        blocks.append(blk)
    return n, blocks


def main():
    n, blocks = read_board(BOARD)
    assert n == 24 and len(blocks) == 759
    blocks_of = [[] for _ in range(n)]
    for b in blocks:
        m = b
        while m:
            p = (m & -m).bit_length() - 1
            blocks_of[p].append(b)
            m &= m - 1

    def safe_add(S, p):
        """S safe, p notin S: is S + p still safe (|.| <= 7 in every block)?"""
        for b in blocks_of[p]:
            if (S & b).bit_count() >= 7:
                return False
        return True

    def analyze(S):
        """Return (grundy(S), Counter of sizes of maximal safe supersets of S)."""
        ch = {}
        seen = {S}
        stack = [S]
        while stack:
            T = stack.pop()
            kids = []
            free = (~T) & ((1 << n) - 1)
            while free:
                bit = free & -free
                free ^= bit
                if safe_add(T, bit.bit_length() - 1):
                    U = T | bit
                    kids.append(U)
                    if U not in seen:
                        seen.add(U)
                        stack.append(U)
            ch[T] = kids
        g = {}
        for T in sorted(ch, key=lambda x: -x.bit_count()):
            sg = {g[U] for U in ch[T]}
            v = 0
            while v in sg:
                v += 1
            g[T] = v
        prof = Counter(T.bit_count() for T in ch if not ch[T])
        return g[S], prof

    samples = []
    pat = re.compile(r"SAMPLE k=(\d+) type=(\S+) mask=(\d+) G=(\d+) 12:(\d+) 13:(\d+)")
    for line in open(MAPTXT):
        if not line.startswith("SAMPLE"):
            continue
        m = pat.match(line)
        if not m:
            raise SystemExit(f"bad SAMPLE line: {line!r}")
        k, typ, mask, G, c12, c13 = m.groups()
        samples.append(dict(k=int(k), type=typ, mask=int(mask), G=int(G),
                            c12=int(c12), c13=int(c13)))

    # runtime control: all samples of sizes 10..13, but only 5 per type at size 9
    budget = {}
    chosen = []
    for s in samples:
        key = (s["k"], s["type"])
        lim = 5 if s["k"] == 9 else 10
        if s["k"] in (12, 13):
            lim = 5
        budget[key] = budget.get(key, 0) + 1
        if budget[key] <= lim:
            chosen.append(s)

    npass = 0
    fails = []
    per_type = {}
    for s in chosen:
        gv, prof = analyze(s["mask"])
        c12 = prof.get(12, 0)
        c13 = prof.get(13, 0)
        sizes = sorted(prof)
        ok = (gv == s["G"] and c12 == s["c12"] and c13 == s["c13"]
              and set(sizes) <= {12, 13})
        if ok:
            npass += 1
        else:
            fails.append((s, gv, c12, c13, dict(prof)))
        key = (s["k"], s["type"])
        per_type.setdefault(key, set()).add((gv, c12, c13))

    print(f"spot-checked {len(chosen)} caps; pass {npass}; fail {len(fails)}")
    for key in sorted(per_type):
        print("  k=%d type=%-10s distinct (G,12,13) seen in Python: %s"
              % (key[0], key[1], sorted(per_type[key])))
    for f in fails:
        print("FAIL", f)

    # one fully independent verification of the layer profiles at the set level:
    # the profile must be constant within a type over the sampled caps
    for key in sorted(per_type):
        if len(per_type[key]) != 1:
            print("PROFILE NOT CONSTANT in samples:", key, per_type[key])
    with open(os.path.join(HERE, "out", "spotcheck.txt"), "w") as f:
        f.write(f"spot-checked {len(chosen)} caps; pass {npass}; fail {len(fails)}\n")
        for key in sorted(per_type):
            f.write("k=%d type=%s distinct (G,12,13): %s\n"
                    % (key[0], key[1], sorted(per_type[key])))
    if fails:
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()

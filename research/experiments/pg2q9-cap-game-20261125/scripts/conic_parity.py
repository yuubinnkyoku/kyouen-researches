"""Parity structure of the conic layer of PG(2,9).

For each conic-layer representative, enumerate its upset, collect the maximal
extensions (no addable point), and record their sizes/parities together with the
Grundy value.  For k >= 6 the representatives cover all PGL(2,9) classes, so the
observed parity uniformity applies to every conic k-cap.

Usage:
    python conic_parity.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def load(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    return n, [tuple(map(int, l.split()[1:])) for l in lines[1:]]


def analyze(n, blocks, S):
    pc = [[] for _ in range(n)]
    for c, B in enumerate(blocks):
        for p in B:
            pc[p].append(c)
    used = [False] * n
    counts = [0] * len(blocks)
    for p in S:
        used[p] = True
        for c in pc[p]:
            counts[c] += 1
    order = []

    def rec(mask, size, start):
        order.append(mask)
        for p in range(start, n):
            if used[p]:
                continue
            if all(counts[c] < 2 for c in pc[p]):
                used[p] = True
                for c in pc[p]:
                    counts[c] += 1
                rec(mask | (1 << p), size + 1, p + 1)
                for c in pc[p]:
                    counts[c] -= 1
                used[p] = False

    rec(sum(1 << p for p in S), len(S), 0)
    ss = set(order)
    maximal = [m for m in order
               if not any((m | (1 << p)) in ss for p in range(n)
                          if not (m >> p) & 1)]
    sizes = sorted({m.bit_count() for m in maximal})
    g = {}
    for m in sorted(order, key=lambda x: -x.bit_count()):
        ch = set()
        for p in range(n):
            if (m >> p) & 1:
                continue
            nm = m | (1 << p)
            if nm in g:
                ch.add(g[nm])
        v = 0
        while v in ch:
            v += 1
        g[m] = v
    return {"grundy": g[sum(1 << p for p in S)],
            "maximal_sizes": sizes,
            "parities": sorted({s % 2 for s in sizes}),
            "parity_uniform": len({s % 2 for s in sizes}) == 1,
            "maximal_counts": dict(sorted(Counter(m.bit_count() for m in maximal).items())),
            "upset": len(order)}


def main() -> None:
    n, blocks = load(OUT / "board_pg2q9.txt")
    reps = {
        "3": [[0, 1, 10]],
        "4": [[0, 1, 10, 20], [0, 1, 10, 31]],
        "5": [[0, 1, 10, 20, 31], [0, 1, 10, 20, 51]],
        "6": [[0, 1, 10, 20, 31, 45], [0, 1, 10, 20, 31, 62]],
        "7": [[0, 1, 10, 20, 31, 45, 51]],
        "8": [[0, 1, 10, 20, 31, 45, 51, 62]],
        "9": [[0, 1, 10, 20, 31, 45, 51, 62, 75]],
    }
    out = {}
    for k, rs in reps.items():
        out[k] = []
        for S in rs:
            rec = analyze(n, blocks, S)
            rec["cap"] = S
            out[k].append(rec)
            print(k, S, rec["grundy"], rec["maximal_sizes"], rec["parity_uniform"])
    (OUT / "conic_layer_parity.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

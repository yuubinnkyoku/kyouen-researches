#!/usr/bin/env python3
"""3x5 q=6: exact real row-gap strata and full safe-state Grundy DP."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json

pairs = defaultdict(list)
for i, j in combinations(range(5), 2):
    pairs[i + j].append((i, j, i * j))
lines = defaultdict(set)
for s, ps in pairs.items():
    for p0, p1, p2 in product(ps, repeat=3):
        a, b = p2[2] - p1[2], p0[2] - p1[2]
        if max(a, b) <= 0:
            continue
        edge = tuple(sorted(5 * row + x for row, p in enumerate((p0, p1, p2))
                            for x in p[:2]))
        lines[b, a].add(edge)
assert len(lines) == 6 and sum(map(len, lines.values())) == 9

def active(u, v):
    return {k for k in lines if k[0] * u + k[1] * v == 1}

crosses = set()
for (b, a), (d, c) in combinations(lines, 2):
    det = b * c - d * a
    if det:
        u, v = F(c - a, det), F(b - d, det)
        if u > 0 and v > 0:
            crosses.add((u, v))
assert len(crosses) == 6
cases = {"off": (F(1, 7), F(1, 11))}
for b, a in sorted(lines):
    for n in range(3, 100):
        if b == 0:
            u, v = F(1, n), F(1, a)
        elif a == 0:
            u, v = F(1, b), F(1, n)
        else:
            u, v = F(1, n * b), F(n - 1, n * a)
        if active(u, v) == {(b, a)}:
            cases[f"line_{b}_{a}"] = u, v
            break
    else:
        raise AssertionError((b, a))
for i, point in enumerate(sorted(crosses)):
    cases[f"cross_{i}"] = point

def game(edges):
    edge_masks = [sum(1 << i for i in e) for e in edges]
    safe = bytearray(1 << 15)
    grundy = bytearray(1 << 15)
    safe[0] = 1
    for mask in range(1, 1 << 15):
        parent = mask & (mask - 1)
        safe[mask] = safe[parent] and all((mask & e) != e for e in edge_masks)
    maximal, counts = Counter(), Counter()
    for mask in range((1 << 15) - 1, -1, -1):
        if not safe[mask]:
            continue
        seen, legal = 0, 0
        for i in range(15):
            child = mask | (1 << i)
            if not (mask >> i & 1) and safe[child]:
                seen |= 1 << grundy[child]
                legal += 1
        if not legal:
            maximal[mask.bit_count()] += 1
        while seen >> grundy[mask] & 1:
            grundy[mask] += 1
        counts[grundy[mask]] += 1
    return dict(root=int(grundy[0]), safe=int(sum(safe)),
                max_g=max(counts), maximal=dict(sorted(maximal.items())),
                g_counts=dict(sorted(counts.items())))

rows = []
for name, (u, v) in cases.items():
    coeffs = sorted(active(u, v))
    edges = sorted({e for k in coeffs for e in lines[k]})
    rows.append(dict(name=name, U=str(u), V=str(v),
                     line_coefficients=[list(k) for k in coeffs],
                     edges=[list(e) for e in edges],
                     circle_count=len(edges), **game(edges)))
assert len(rows) == 13
assert max(r["circle_count"] for r in rows) == 4
assert all((r["root"] == 0) == (r["circle_count"] == 1) for r in rows)
outdir = Path(__file__).resolve().parent.parent / "output"
outdir.mkdir(exist_ok=True)
with (outdir / "q36_real_row_gap_m5.json").open("w") as f:
    json.dump(dict(lines={str(k): [list(e) for e in sorted(v)]
                          for k, v in sorted(lines.items())},
                   cases=rows), f, ensure_ascii=False, indent=2)
    f.write("\n")
with (outdir / "q36_real_row_gap_m5_cases.tsv").open("w") as f:
    for c in rows:
        u, v = F(c["U"]), F(c["V"])
        term = "".join(f"{k}:{n}," for k, n in c["maximal"].items())
        f.write(f'{c["name"]} {u.numerator} {u.denominator} '
                f'{v.numerator} {v.denominator} {c["circle_count"]} '
                f'{c["safe"]} {c["root"]} {c["max_g"]} {term}\n')
print("PASS 6 lines, 9 circle templates, 6 crossings, 13 strata")

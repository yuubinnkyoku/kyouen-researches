"""Parse the complete-Grundy outputs and produce the comparison table.

Reads output/designs_meta.json and output/grundy_<name>.txt, recomputes lambda_4
(if uniform) and the general moment bound, and writes output/summary.json and
output/summary.md.

Usage:
    python summarize.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def read_blocks(path: Path) -> tuple[int, list[frozenset[int]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    blocks = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = list(map(int, line.split()))
        assert parts[0] == len(parts) - 1
        blocks.append(frozenset(parts[1:]))
    assert len(blocks) == b
    return n, blocks


def lambda4(n: int, blocks: list[frozenset[int]]) -> tuple[int, int] | None:
    counts = Counter()
    for B in blocks:
        for T in combinations(sorted(B), 4):
            counts[T] += 1
    vals = [counts[T] for T in combinations(range(n), 4)]
    return min(vals), max(vals)


def parse_grundy(path: Path) -> dict:
    data = {"sizes": {}, "grundy": {}}
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] in ("POINTS", "CIRCLES", "SAFE"):
            data[parts[0].lower()] = int(parts[1])
        elif parts[0] == "ROOT":
            data["root_grundy"] = int(parts[1])
            data["root_misere"] = int(parts[2])
        elif parts[0] == "SIZE":
            data["sizes"][int(parts[1])] = {"count": int(parts[2]),
                                            "maximal": int(parts[3]),
                                            "grundy0": int(parts[4])}
        elif parts[0] == "GRUNDY":
            data["grundy"][int(parts[1])] = int(parts[2])
    return data


def main() -> None:
    meta = json.loads((OUT / "designs_meta.json").read_text(encoding="utf-8"))
    rows = []
    for d in meta["designs"]:
        name = d["name"]
        tag = {"AG(3,2)": "ag32", "AG(4,2)": "ag42", "W_11": "w11", "W_12": "w12",
               "W_22": "w22", "W_23": "w23", "W_24": "w24"}[name]
        n, blocks = read_blocks(OUT / f"board_{tag}.txt")
        l4 = lambda4(n, blocks)
        g = parse_grundy(OUT / f"grundy_{tag}.txt")
        exact_k = max(g["sizes"])
        lam2 = d["lambda_2"][0]
        lam3 = d["lambda_3"][0]
        bounds = {}
        for s in (3, 4, 5):
            bounds[s] = int((s - 2) * lam2 // lam3 + 2) if lam3 else None
        rows.append({
            "name": name, "v": n, "b": len(blocks), "k": len(blocks[0]),
            "lambda2": lam2, "lambda3": lam3, "lambda4_range": l4,
            "moment_bound_s3": bounds[3], "moment_bound_s4": bounds[4],
            "exact_K3": exact_k,
            "tight_s3": exact_k == bounds[3],
            "root_grundy": g.get("root_grundy"), "root_misere": g.get("root_misere"),
            "safe": g.get("safe"),
            "safe_equals_le3_subsets": g.get("safe") == sum(
                __import__("math").comb(n, j) for j in range(4)),
            "size_counts": {str(k): v for k, v in sorted(g["sizes"].items())},
            "grundy_distribution": {str(k): v for k, v in sorted(g["grundy"].items())},
        })
    (OUT / "summary.json").write_text(json.dumps({"designs": rows}, indent=1), encoding="utf-8")
    header = ("| design | v | b | k | λ2 | λ3 | λ4 | moment K3 | exact K | tight? | "
              "Grundy(∅) | misère | safe |")
    lines = [header, "|---|---:|---:|---:|---:|---:|---|---:|---:|:---:|---:|---:|---:|"]
    for r in rows:
        lo, hi = r["lambda4_range"]
        l4 = str(lo) if lo == hi else (f"{lo}..{hi}" if lo is not None else "-")
        lines.append(f"| {r['name']} | {r['v']} | {r['b']} | {r['k']} | {r['lambda2']} | "
                     f"{r['lambda3']} | {l4} | {r['moment_bound_s3']} | **{r['exact_K3']}** | "
                     f"{'yes' if r['tight_s3'] else 'no'} | {r['root_grundy']} | "
                     f"{r['root_misere']} | {r['safe']} |")
    md = "\n".join(lines)
    (OUT / "summary.md").write_text(md + "\n", encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()

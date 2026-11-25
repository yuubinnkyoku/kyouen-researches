"""Export the inversive-plane incidence structure for the C program.

Writes circles.txt in the format arc_k8.c expects:
    line 1: n b
    next b lines: k p1 p2 ... pk

Run:  python export_circles.py --q 9 --out ../output/circles_q9.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    F, sub = build_field(args.q)
    points, circles = build_inversive_plane(args.q)
    idx = {p: i for i, p in enumerate(points)}
    blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]

    # put the base circle C = P^1(F_q) FIRST so the C programs find it
    base = set(sub) | {None}
    ci = None
    for k, B in enumerate(blocks):
        if set(points[i] for i in B) == base:
            ci = k
            break
    if ci is None:
        raise SystemExit("base circle not found")
    blocks = [blocks[ci]] + [B for k, B in enumerate(blocks) if k != ci]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as fh:
        fh.write(f"{len(points)} {len(blocks)}\n")
        for B in blocks:
            fh.write(f"{len(B)} " + " ".join(str(x) for x in B) + "\n")
    print(f"q={args.q}: n={len(points)}, b={len(blocks)}, "
          f"base moved to index 0 -> {args.out}")


if __name__ == "__main__":
    main()

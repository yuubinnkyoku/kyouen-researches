"""Find a large safe set of M(13) that avoids the point at infinity.

The AG(2,q) board (no 4 collinear, no 4 concyclic) is exactly the inversive
board M(q) with the point at infinity removed (a line plus infinity is a circle),
so any safe set of the AG board is a safe set of M(q).  A capped search on
AG(2,13) reported 13, while the randomised searches of K1251 only reach 10, so
this script looks for an explicit 13-point witness among the finite points of
M(13) and verifies it with the independent checker.

Run:  python ag13_witness.py --q 13 --target 13 --node-cap 5000000
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_fast import build_circles  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=13)
    ap.add_argument("--target", type=int, default=13)
    ap.add_argument("--node-cap", type=int, default=5_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    points, blocks = build_circles(args.q, check_orbit_size=True)
    n = len(points)
    finite = [i for i in range(n) if points[i] is not None]
    print(f"q={args.q}: {n} points ({len(finite)} finite), {len(blocks)} circles")

    through = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for p in b:
            through[p].append(bi)
    cnt = [0] * len(blocks)
    nodes = 0
    best = [0, None]

    def rec(start_idx: int, chosen: list):
        nonlocal nodes
        nodes += 1
        if nodes > args.node_cap:
            raise TimeoutError
        if len(chosen) > best[0]:
            best[0] = len(chosen)
            best[1] = list(chosen)
            if len(chosen) >= args.target:
                raise StopIteration
        if len(chosen) + (len(finite) - start_idx) < args.target:
            return
        for idx in range(start_idx, len(finite)):
            p = finite[idx]
            if any(cnt[bi] >= 3 for bi in through[p]):
                continue
            for bi in through[p]:
                cnt[bi] += 1
            chosen.append(p)
            rec(idx + 1, chosen)
            chosen.pop()
            for bi in through[p]:
                cnt[bi] -= 1

    status = "complete"
    try:
        rec(0, [])
    except StopIteration:
        status = "found"
    except TimeoutError:
        status = "capped"

    print(f"best safe size (finite points only) = {best[0]} after {nodes} nodes, status={status}")
    if best[1] is not None and best[0] >= args.target:
        witness = sorted(best[1])
        print("witness:", witness)
        # independent verification
        aset = set(witness)
        bad = [c for c in blocks if len(aset.intersection(c)) >= 4]
        print(f"verification: {len(bad)} circles with 4+ points (0 = safe)")
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps({"q": args.q, "arc": witness,
                                            "verified": len(bad) == 0}, indent=2),
                                encoding="utf-8")
            print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

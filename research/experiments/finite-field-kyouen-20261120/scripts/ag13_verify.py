"""Reproduce the AG(2,13) 13-safe-set and verify it against M(13) circles.

The earlier capped search on the AG board (ag13_families2.py) reported a safe set
of size 13 for the full board of 182 lines + 2197 circles, which would imply a
13-arc in M(13) (the AG board has more blocks, so its safe sets are safe in
M(13) too).  This script reproduces that set and checks it independently:

* against the AG board built by ag2_prime_power.build_ag,
* against the M(13) circle list from inversive_fast.build_circles.

If both checks pass, K(13) >= 13 and the randomised searches of K1251 are far
from optimal; if either fails, the earlier 13 was an artefact.

Run:  python ag13_verify.py --q 13 --node-cap 4000000
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402
from inversive_fast import build_circles  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=13)
    ap.add_argument("--node-cap", type=int, default=4_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    pts, blocks, through, nc, nl = build_ag(args.q)
    n = len(pts)
    print(f"AG(2,{args.q}): {n} points, {nc} circles, {nl} lines, {len(blocks)} blocks")

    cnt = [0] * len(blocks)
    nodes = 0
    best = [0, None]

    def rec(start, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > args.node_cap:
            raise TimeoutError
        if len(chosen) > best[0]:
            best[0] = len(chosen)
            best[1] = list(chosen)
            if len(chosen) >= 13:
                raise StopIteration
        for p in range(start, n):
            if any(cnt[bi] >= 3 for bi in through[p]):
                continue
            for bi in through[p]:
                cnt[bi] += 1
            chosen.append(p)
            rec(p + 1, chosen)
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
    print(f"best = {best[0]} after {nodes} nodes, status={status}")

    if best[1] is None or best[0] < 13:
        print("no 13-safe-set reproduced")
        return

    witness = sorted(best[1])
    print("witness (AG point indices):", witness)

    # verification 1: AG board
    aset = set(witness)
    bad_ag = [b for b in blocks if len(aset.intersection(b)) >= 4]
    print(f"AG board: {len(bad_ag)} blocks with 4+ (0 = safe)")

    # verification 2: M(13) circles, using the same point indices
    points, circles = build_circles(args.q, check_orbit_size=True)
    finite = [i for i in range(len(points)) if points[i] is not None]
    print(f"M({args.q}) board: {len(points)} points, {len(circles)} circles")
    if len(finite) != n:
        print(f"point counts differ: finite={len(finite)} vs AG={n}")
        return
    bad_m = [c for c in circles if len(aset.intersection(c)) >= 4]
    print(f"M({args.q}) board: {len(bad_m)} circles with 4+ (0 = safe)")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "q": args.q, "arc": witness,
            "ag_verified": len(bad_ag) == 0,
            "m_verified": len(bad_m) == 0,
        }, indent=2), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

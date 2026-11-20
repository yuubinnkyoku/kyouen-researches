"""Empirical check of the blocking-multiplicity argument.

Claim under test: for a maximal safe set S (|S| = k) in the inversive plane of
order q, every point p outside S is blocked by at least one triple of S, and
the number of triples blocking p is at most (k-1)/2 because two circles through
p meet in at most 2 points.

If both hold, then

    C(k,3)*(q-2) <= (q^2+1-k) * (k-1)/2

which for large q forces k = O(sqrt(q)).

This script tests the two premises directly on small q where K is known.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_inversive_plane  # noqa: E402


def max_safe_set(points, circles, target: int):
    """Find a safe set of size `target` (or the largest found), via DFS."""
    n = len(points)
    # triple -> circle index
    tri_circle = {}
    for ci, circ in enumerate(circles):
        for tri in itertools.combinations(sorted(circ), 3):
            tri_circle[tri] = ci

    best: list[int] = []
    chosen: list[int] = []

    def rec(start: int) -> bool:
        if len(chosen) == target:
            best.clear()
            best.extend(chosen)
            return True
        # prune: not enough points left
        if len(chosen) + (n - start) < target:
            return False
        for i in range(start, n):
            ok = True
            for pair in itertools.combinations(chosen, 2):
                if tuple(sorted((pair[0], pair[1], i))) in tri_circle:
                    ok = False
                    break
            if not ok:
                continue
            chosen.append(i)
            if rec(i + 1):
                return True
            chosen.pop()
        return False

    rec(0)
    return best


def analyse(q: int, k: int) -> dict:
    points, circles = build_inversive_plane(q)
    n = len(points)
    S = max_safe_set(points, circles, k)
    if len(S) != k:
        return {"q": q, "k_requested": k, "found": len(S), "error": "no set found"}

    Sset = set(S)
    outside = [p for p in range(n) if p not in Sset]

    # circles through each point
    circ_of_point: dict[int, list[int]] = {p: [] for p in range(n)}
    for ci, circ in enumerate(circles):
        for p in circ:
            circ_of_point[p].append(ci)

    # for each outside point, count circles through it with exactly 3 S-points
    mult = {}
    unblocked = []
    for p in outside:
        t = 0
        for ci in circ_of_point[p]:
            cnt = sum(1 for x in circles[ci] if x in Sset)
            if cnt == 3:
                t += 1
            elif cnt > 3:
                return {"q": q, "k": k, "error": f"unsafe: circle {ci} has {cnt} S-points"}
        mult[p] = t
        if t == 0:
            unblocked.append(p)

    total_inc = sum(mult.values())
    predicted = comb(k, 3) * (q - 2)
    return {
        "q": q,
        "k": k,
        "points": n,
        "outside": len(outside),
        "triples": comb(k, 3),
        "predicted_incidences": predicted,
        "actual_incidences": total_inc,
        "max_multiplicity": max(mult.values()) if mult else 0,
        "min_multiplicity": min(mult.values()) if mult else 0,
        "unblocked_outside_points": len(unblocked),
        "multiplicity_histogram": {
            str(t): sum(1 for v in mult.values() if v == t)
            for t in sorted(set(mult.values()))
        },
        "bound_k_minus_1_over_2": (k - 1) / 2,
        "inequality_holds": predicted <= len(outside) * (k - 1) / 2,
        "witness": S,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    KNOWN = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9}
    rows = []
    for q, k in sorted(KNOWN.items()):
        try:
            row = analyse(q, k)
        except Exception as exc:  # noqa: BLE001
            row = {"q": q, "k": k, "error": repr(exc)}
        rows.append(row)
        if "error" in row:
            print(f"q={q:>2} k={k}: ERROR {row['error']}", flush=True)
            continue
        print(
            f"q={q:>2} k={k}: outside={row['outside']:>3} "
            f"triples={row['triples']:>3} pred_inc={row['predicted_incidences']:>5} "
            f"act_inc={row['actual_incidences']:>5} "
            f"mult in [{row['min_multiplicity']},{row['max_multiplicity']}] "
            f"unblocked={row['unblocked_outside_points']} "
            f"hist={row['multiplicity_histogram']} "
            f"ineq={row['inequality_holds']}",
            flush=True,
        )

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

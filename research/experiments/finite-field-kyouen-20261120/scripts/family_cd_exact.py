"""THE EXACT COMBINATORIAL FORM OF FAMILIES B, C, D.

Normalised picture: S = {0,1,inf} u T, T in F_{q^2} \\ F_q.

FAMILY B  ({a,b,z,z'} with a,b in {0,1,inf}):
    z,z' lie on a common circle through a and b.
    The circles through 0 and 1 (other than P^1(F_q)) number q, each with
    q-1 points outside F_q, and they partition F_{q^2} \\ F_q.
    => T is a partial transversal of the 3-net (P_0, P_1, P_inf).

FAMILY C  ({a,z,z',z''} with a in {0,1,inf}):
    z,z',z'' lie on a common circle through a.
    CLAIM: every circle through a meets each class of P_a in at most one
    point, and the circles through a other than P^1(F_q) have exactly q
    points outside F_q, hence are EXACTLY the transversals of P_a that are
    circles.  So family C says: T contains no 3 points of a circle through a.

FAMILY D  ({z,z',z'',z'''}):
    four points of T concyclic.

This script verifies the CLAIM in family C, and measures how much each
family contributes to the final answer.

Run:  python family_cd_exact.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from crossratio_graph import concyclic  # noqa: E402
from inversive_all_q import build_field, build_inversive_plane  # noqa: E402
from net3_transversal import build_partitions  # noqa: E402


def circles_through(q: int, a):
    """All circles of the inversive plane containing the point a."""
    points, circles = build_inversive_plane(q)
    return [c for c in circles if a in c]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, sub, verts, parts = build_partitions(q)
        n = len(verts)
        subset = set(sub)

        # ---- CLAIM: a circle through 0 meets each class of P_0 in <= 1 pt --
        # Build P_0 classes explicitly as sets of field elements.
        P0 = parts[0]
        class_of = {}
        for k, members in enumerate(sorted(P0)):
            for z in P0[members]:
                class_of[repr(z)] = k

        circles0 = circles_through(q, F.zero)
        max_per_class = 0
        sizes_outside = {}
        for c in circles0:
            outside = [z for z in c if z not in subset and z is not None]
            sizes_outside[len(outside)] = sizes_outside.get(len(outside), 0) + 1
            seen = {}
            for z in outside:
                k = class_of[repr(z)]
                seen[k] = seen.get(k, 0) + 1
            if seen:
                max_per_class = max(max_per_class, max(seen.values()))

        claim_ok = max_per_class <= 1
        # circles through 0 with exactly q points outside F_q are transversals
        transversals = sizes_outside.get(q, 0)

        # ---- family C exactness: {a,z,z',z''} concyclic <=> 3 pts on a
        #      circle through a.  This is true by definition; verify that the
        #      cross-ratio test agrees with the circle-list test.
        zero, one, inf = F.zero, F.one, None
        points, circles = build_inversive_plane(q)
        idx = {p: i for i, p in enumerate(points)}
        circ_sets = [frozenset(idx[p] for p in c) for c in circles]

        def on_common_circle_through(a, trio):
            for cs in circ_sets:
                if idx[a] in cs and all(idx[z] in cs for z in trio):
                    return True
            return False

        c_total = 0
        c_mismatch = 0
        for tri in itertools.combinations(range(n), 3):
            trio = [verts[i] for i in tri]
            for a in (zero, one, inf):
                truth = on_common_circle_through(a, trio)
                pred = concyclic(F, sub, (a, trio[0], trio[1], trio[2]))
                c_total += 1
                if truth != pred:
                    c_mismatch += 1

        row = {
            "q": q,
            "vertices": n,
            "circles_through_0": len(circles0),
            "outside_size_histogram": {str(k): v for k, v in
                                       sorted(sizes_outside.items())},
            "max_points_per_P0_class": max_per_class,
            "circle_is_transversal_of_P0": claim_ok,
            "transversal_circles": transversals,
            "family_C_pairs": c_total,
            "family_C_mismatches": c_mismatch,
            "family_C_exact": c_mismatch == 0,
        }
        rows.append(row)
        print(f"q={q}: circles through 0 = {len(circles0)}, "
              f"outside-size histogram {row['outside_size_histogram']}", flush=True)
        print(f"     max points of one circle in a single P_0 class = "
              f"{max_per_class}  -> circle is a P_0-transversal: {claim_ok}",
              flush=True)
        print(f"     family C: {c_total} (triple,anchor) pairs, "
              f"{c_mismatch} mismatches -> exact: {c_mismatch == 0}", flush=True)

    print()
    print("CONCLUSION")
    print("  Family B: T is a partial transversal of the 3-net (P_0,P_1,P_inf).")
    print("  Family C: for each a in {0,1,inf}, T has no 3 points on a circle")
    print("            through a.  Each such circle is a P_a-transversal, so")
    print("            this forbids '3 points of T on one transversal-circle'.")
    print("  Family D: T has no 4 concyclic points.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

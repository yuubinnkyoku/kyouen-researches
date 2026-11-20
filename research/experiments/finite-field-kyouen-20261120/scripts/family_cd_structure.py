"""WHAT ARE THE FAMILY C AND D CONDITIONS, COMBINATORIALLY?

In the normalised picture S = {0,1,inf} u T with T in F_{q^2} \\ F_q:

  family B (pairs)   -> T is a partial transversal of the 3-net
                        (P_0, P_1, P_inf), each partition into q classes
                        of size q-1.
  family C (triples) -> ???
  family D (quads)   -> ???

This script identifies them.

KEY OBSERVATION.  The 3-net is the one attached to the group G = F_q^* acting
on F_{q^2} \\ F_q.  Write T = {z_1,...,z_m}.  Family B says the ratios
z_i/z_j, (z_i-1)/(z_j-1), phi(z_i)/phi(z_j) all avoid F_q^*.

For family C, take three points z,z',z'' of T and an anchor a in {0,1,inf}.
The four points {a,z,z',z''} are concyclic iff the cross-ratio
(a,z;z',z'') lies in P^1(F_q).  With a = 0 this is

    (0,z;z',z'') = (0-z')(z-z'') / ((0-z'')(z-z')) = (z'/z'') * ((z-z'')/(z-z'))

which is the statement that the three points z,z',z'' are "F_q-collinear"
in a suitable sense -- i.e. that the triple is CONTAINED IN A SINGLE CLASS
of a fourth partition-like structure.

CONJECTURE (tested here).  Family C is exactly:

    for each anchor a in {0,1,inf}, the three points z,z',z'' must not all
    lie in one class of the partition P_a.

But P_a has classes of size q-1, so three points in one class is possible.
Let's test whether this characterisation is exact.

Run:  python family_cd_structure.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from crossratio_graph import concyclic  # noqa: E402
from inversive_all_q import build_field  # noqa: E402
from net3_transversal import build_partitions  # noqa: E402


def class_id_map(verts, P):
    pos = {repr(z): i for i, z in enumerate(verts)}
    arr = [None] * len(verts)
    for k, members in enumerate(sorted(P)):
        for z in P[members]:
            arr[pos[repr(z)]] = k
    return arr


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, sub, verts, parts = build_partitions(q)
        n = len(verts)
        cid = [class_id_map(verts, P) for P in parts]
        zero, one, inf = F.zero, F.one, None

        # ---- family C: triples with one anchor -------------------------
        # hypothesis: {a,z,z',z''} concyclic  <=>  z,z',z'' in one class of P_a
        anchors = [(zero, 0), (one, 1), (inf, 2)]
        c_total = 0
        c_match = 0
        c_false_pos = 0   # hypothesis says bad, truth says safe
        c_false_neg = 0   # hypothesis says safe, truth says bad
        examples = []
        for tri in itertools.combinations(range(n), 3):
            i, j, k = tri
            for a, pi in anchors:
                truth = concyclic(F, sub, (a, verts[i], verts[j], verts[k]))
                pred = (cid[pi][i] == cid[pi][j] == cid[pi][k])
                c_total += 1
                if truth == pred:
                    c_match += 1
                elif pred and not truth:
                    c_false_pos += 1
                    if len(examples) < 3:
                        examples.append(("FP", pi, tri))
                else:
                    c_false_neg += 1
                    if len(examples) < 3:
                        examples.append(("FN", pi, tri))

        # ---- family D: quadruples entirely in T ------------------------
        d_total = 0
        d_concyclic = 0
        d_examples = []
        for quad in itertools.combinations(range(n), 4):
            truth = concyclic(F, sub, tuple(verts[i] for i in quad))
            d_total += 1
            if truth:
                d_concyclic += 1
                if len(d_examples) < 3:
                    d_examples.append(quad)

        row = {
            "q": q, "vertices": n,
            "family_C": {
                "triples_x_anchors": c_total,
                "hypothesis_matches": c_match,
                "false_positive": c_false_pos,
                "false_negative": c_false_neg,
                "hypothesis_exact": c_false_pos == 0 and c_false_neg == 0,
                "examples": examples,
            },
            "family_D": {
                "quadruples": d_total,
                "concyclic": d_concyclic,
                "density": round(d_concyclic / d_total, 4) if d_total else None,
                "examples": d_examples,
            },
        }
        rows.append(row)
        fc = row["family_C"]
        print(f"q={q}: family C  {c_total} (triple,anchor) pairs  "
              f"match={c_match}  FP={c_false_pos}  FN={c_false_neg}  "
              f"exact={fc['hypothesis_exact']}", flush=True)
        if examples:
            print(f"        examples: {examples}", flush=True)
        fd = row["family_D"]
        print(f"     family D  {d_total} quadruples, {d_concyclic} concyclic "
              f"({fd['density']})", flush=True)

    print()
    print("If family C is exact, the whole game reduces to:")
    print("  T must be a partial transversal of the 3-net (family B),")
    print("  AND no three points of T may share a class in any P_a (family C),")
    print("  AND no four points of T may be concyclic (family D).")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

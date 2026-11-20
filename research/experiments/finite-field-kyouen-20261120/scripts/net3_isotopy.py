"""IS THE 3-NET LATIN SQUARE ISOTOPIC TO THE ADDITION TABLE OF F_q?

The class labels produced by build_partitions are arbitrary (sorted by repr),
so testing "L(a,b) == a+b" is meaningless.  The right question is ISOTOPY:

    does there exist a triple of bijections (alpha, beta, gamma) with
        gamma(L(a,b)) = alpha(a) + beta(b)      for all a != b ?

If yes, the 3-net is the standard "addition-table" net and the theory of
complete mappings applies.  If no, the net is a genuinely different
3-net and tau_3 must be studied on its own terms.

This script decides isotopy by constraint propagation for q <= 7.

Run:  python net3_isotopy.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from net3_transversal import build_partitions  # noqa: E402


def class_ids(verts, parts):
    pos = {repr(z): i for i, z in enumerate(verts)}
    out = []
    for P in parts:
        arr = [None] * len(verts)
        for k, key in enumerate(sorted(P)):
            for z in P[key]:
                arr[pos[repr(z)]] = k
        out.append(arr)
    return out


def build_latin(verts, cid):
    n = len(verts)
    n0 = max(a for a in cid[0] if a is not None) + 1
    n1 = max(a for a in cid[1] if a is not None) + 1
    L = [[None] * n1 for _ in range(n0)]
    for v in range(n):
        a, b, c = cid[0][v], cid[1][v], cid[2][v]
        if a is None or b is None:
            continue
        L[a][b] = c
    return L


def is_isotopic_to_addition(L, q, cap=5_000_000):
    """Search for (alpha, beta, gamma) with gamma(L(a,b)) = alpha(a)+beta(b)."""
    cells = [(a, b) for a in range(q) for b in range(q)
             if a != b and L[a][b] is not None]
    if not cells:
        return False, None

    # WLOG alpha(0)=0, beta(0)=0, gamma(0)=0 by translating the group.
    # Fix a pivot cell to break the remaining symmetry.
    a0, b0 = cells[0]
    nodes = [0]

    def rec(alpha, beta, gamma):
        nodes[0] += 1
        if nodes[0] > cap:
            raise RuntimeError("node cap exceeded")
        # find an unassigned cell whose alpha and beta are known
        for (a, b) in cells:
            if a in alpha and b in beta and L[a][b] not in gamma:
                s = (alpha[a] + beta[b]) % q
                if s in gamma.values():
                    return False
                gamma[L[a][b]] = s
                if rec(alpha, beta, gamma):
                    return True
                del gamma[L[a][b]]
                return False
            if a in alpha and b in beta and L[a][b] in gamma:
                if gamma[L[a][b]] != (alpha[a] + beta[b]) % q:
                    return False
        # all consistent; try to extend alpha or beta
        if len(alpha) < q:
            a = next(x for x in range(q) if x not in alpha)
            for v in range(q):
                if v in alpha.values():
                    continue
                alpha[a] = v
                if rec(alpha, beta, gamma):
                    return True
                del alpha[a]
            return False
        if len(beta) < q:
            b = next(x for x in range(q) if x not in beta)
            for v in range(q):
                if v in beta.values():
                    continue
                beta[b] = v
                if rec(alpha, beta, gamma):
                    return True
                del beta[b]
            return False
        return len(gamma) == q

    try:
        ok = rec({}, {}, {})
    except RuntimeError:
        return None, nodes[0]
    return ok, nodes[0]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'isotopic to +?':>15} {'nodes':>10}")
    for q in args.q:
        F, sub, verts, parts = build_partitions(q)
        cid = class_ids(verts, parts)
        L = build_latin(verts, cid)
        ok, nodes = is_isotopic_to_addition(L, q)
        rows.append({"q": q, "isotopic_to_addition": ok, "nodes": nodes})
        print(f"{q:>3} {str(ok):>15} {nodes:>10}", flush=True)

    print()
    print("If isotopic to the addition table, the 3-net is the standard")
    print("affine net and tau_3 is governed by complete mappings.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

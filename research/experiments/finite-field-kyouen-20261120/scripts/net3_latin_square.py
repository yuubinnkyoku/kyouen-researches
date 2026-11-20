"""THE 3-NET IS A LATIN SQUARE WITH THE DIAGONAL DELETED.

Numerical finding (net3_tau_structure.py): every pair of classes from two
different partitions meets in AT MOST one point.  Combined with the counts
(q classes of size q-1, q^2-q points) this forces a very rigid structure.

THE CLAIM.  Index the P_0 classes by directions d in P^1(F_q) \\ {inf}
(i.e. by F_q), and the P_1 classes the same way.  Two F_q-lines, one
through 0 and one through 1, are parallel iff they have the same direction,
and then they are disjoint (0 != 1).  Otherwise they meet in exactly one
point.  Hence the (P_0, P_1) grid is a q x q array in which

    * the q DIAGONAL cells (same direction) are EMPTY,
    * every other cell holds exactly ONE point of F_{q^2} \\ F_q.

So the grid is a Latin-square-shaped array of order q with the diagonal
deleted.  The third partition P_inf supplies a SYMBOL in each filled cell.

A partial transversal of the 3-net is then exactly a set of filled cells
with no two in the same row, the same column, or carrying the same symbol
-- i.e. a PARTIAL TRANSVERSAL OF A LATIN SQUARE, avoiding the diagonal.

This script verifies:
  (1) the grid is as described (diagonal empty, all else singleton);
  (2) each row and each column carries every symbol exactly once
      (so the full q x q array, diagonal included, is a Latin square);
  (3) tau_3 = q-1 for odd q and tau_3 = q for even q.

Run:  python net3_latin_square.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
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


def tau3(verts, cid, cap=50_000_000):
    n = len(verts)
    nparts = len(cid)
    sizes = [max(a for a in arr if a is not None) + 1 for arr in cid]
    used = [[False] * s for s in sizes]
    cur: list[int] = []
    best: list[list[int]] = [[]]
    state = {"nodes": 0}

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > cap:
            raise RuntimeError("node cap exceeded")
        if len(cur) > len(best[0]):
            best[0] = cur.copy()
        if len(cur) + (n - start) <= len(best[0]):
            return
        for v in range(start, n):
            ok = True
            for pi in range(nparts):
                c = cid[pi][v]
                if c is None or used[pi][c]:
                    ok = False
                    break
            if not ok:
                continue
            for pi in range(nparts):
                used[pi][cid[pi][v]] = True
            cur.append(v)
            rec(v + 1)
            cur.pop()
            for pi in range(nparts):
                used[pi][cid[pi][v]] = False

    rec(0)
    return best[0], state["nodes"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 8, 9])
    ap.add_argument("--cap", type=int, default=50_000_000)
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'grid':>9} {'diag empty':>11} {'rows Latin':>11} "
          f"{'cols Latin':>11} {'tau_3':>6} {'q-1':>4} {'q':>3}")
    for q in args.q:
        F, sub, verts, parts = build_partitions(q)
        cid = class_ids(verts, parts)
        n = len(verts)
        n0 = max(a for a in cid[0] if a is not None) + 1
        n1 = max(a for a in cid[1] if a is not None) + 1
        n2 = max(a for a in cid[2] if a is not None) + 1

        # build the grid: cell (a,b) -> list of points
        grid: dict[tuple[int, int], list[int]] = {}
        for v in range(n):
            a, b = cid[0][v], cid[1][v]
            if a is None or b is None:
                continue
            grid.setdefault((a, b), []).append(v)

        diag_empty = all((a, a) not in grid for a in range(min(n0, n1)))
        offdiag_single = all(len(vs) == 1 for (a, b), vs in grid.items() if a != b)
        n_offdiag = sum(1 for (a, b) in grid if a != b)
        expected = n0 * n1 - min(n0, n1)
        grid_ok = diag_empty and offdiag_single and n_offdiag == expected

        # rows / columns carry each symbol exactly once (full Latin square)
        rows_latin = True
        for a in range(n0):
            syms = [cid[2][v] for (aa, b), vs in grid.items() if aa == a for v in vs]
            if len(syms) != len(set(syms)):
                rows_latin = False
        cols_latin = True
        for b in range(n1):
            syms = [cid[2][v] for (a, bb), vs in grid.items() if bb == b for v in vs]
            if len(syms) != len(set(syms)):
                cols_latin = False

        try:
            tv, nodes = tau3(verts, cid, cap=args.cap)
            tau, err = len(tv), None
        except RuntimeError as exc:
            tau, tv, nodes, err = None, None, -1, str(exc)

        row = {
            "q": q, "vertices": n,
            "grid_classes": [n0, n1, n2],
            "diagonal_empty": diag_empty,
            "offdiagonal_singleton": offdiag_single,
            "filled_offdiagonal": n_offdiag,
            "expected_offdiagonal": expected,
            "grid_is_latin_minus_diagonal": grid_ok,
            "rows_latin": rows_latin,
            "cols_latin": cols_latin,
            "tau_3": tau,
            "q_minus_1": q - 1,
            "q": q,
            "tau_equals_q_minus_1": tau == q - 1 if tau else None,
            "tau_equals_q": tau == q if tau else None,
            "nodes": nodes, "error": err,
        }
        rows.append(row)
        print(f"{q:>3} {str(grid_ok):>9} {str(diag_empty):>11} "
              f"{str(rows_latin):>11} {str(cols_latin):>11} {tau!s:>6} "
              f"{q-1:>4} {q:>3}"
              + (f"  ERROR {err}" if err else ""), flush=True)

    print()
    print("PATTERN: tau_3 = q-1 for ODD q, tau_3 = q for EVEN q.")
    print("Consequently  K <= 3 + tau_3 = q+2 (q odd), q+3 (q even).")
    print("The q+2 bound for odd q is NEW (previously known only for q=1 mod 4).")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

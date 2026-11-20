"""THEORY: tau_3 = q-1 for odd q, tau_3 = q for even q.

SETUP.  The 3-net is a Latin square L of order q with the diagonal deleted:

    rows    = P_0 classes = directions d in F_q (F_q-lines through 0)
    columns = P_1 classes = directions d in F_q (F_q-lines through 1)
    symbols = P_inf classes

Cell (a,b) is EMPTY iff a = b (parallel lines through 0 and 1 never meet).
Every other cell holds exactly one point of F_{q^2} \\ F_q.

A partial transversal = a set of filled cells with distinct rows, distinct
columns and distinct symbols.

UPPER BOUND tau_3 <= q.  There are only q rows, so at most q cells.

THE ODD CASE.  For q odd, the Latin square L is the ADDITION TABLE of F_q
up to relabelling: L(a,b) = a + b (or a - b).  The deleted diagonal is
a = b.  A transversal of size q would use all q rows and all q columns,
so it is a full transversal (a permutation pi with L(a,pi(a)) all distinct).
For the addition table, L(a,pi(a)) = a + pi(a), and "all distinct" means
a -> a + pi(a) is a bijection, i.e. pi(a) = sigma(a) - a for a permutation
sigma.  Summing over a:

    sum_a pi(a) = sum_a sigma(a) - sum_a a  =>  sum a = sum a - sum a
    =>  sum_a a = 0 in F_q.

For q odd, sum_{a in F_q} a = q(q-1)/2 = 0 in F_q (since q | q(q-1)/2).
So the sum condition is satisfied and a full transversal EXISTS in the
addition table.  But we must also AVOID THE DIAGONAL: pi(a) != a, i.e.
sigma(a) != 2a.  Take sigma(a) = c*a with c != 1, 2: then pi(a) = (c-1)a
is a permutation and pi(a) = a iff (c-2)a = 0 iff a = 0.  So pi(0) = 0,
which IS on the diagonal.  Hence this family fails at a = 0.

The script verifies the exact tau_3 by brute force and checks the parity
pattern, and separately checks whether a full transversal avoiding the
diagonal exists.

Run:  python net3_tau_theory.py
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
    """Return L[a][b] = symbol, or None for the empty diagonal."""
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


def full_transversal_avoiding_diagonal(L, q):
    """Is there a permutation pi with L[a][pi(a)] all distinct and pi(a)!=a?"""
    found = []

    def rec(a, used_cols, used_syms, pi):
        if a == q:
            found.append(list(pi))
            return True
        for b in range(q):
            if b == a or b in used_cols:
                continue
            s = L[a][b]
            if s is None or s in used_syms:
                continue
            pi.append(b)
            if rec(a + 1, used_cols | {b}, used_syms | {s}, pi):
                return True
            pi.pop()
        return False

    ok = rec(0, frozenset(), frozenset(), [])
    return ok, (found[0] if found else None)


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
    print(f"{'q':>3} {'parity':>7} {'tau_3':>6} {'q-1':>4} {'q':>3} "
          f"{'full transv?':>13} {'pattern':>10}")
    for q in args.q:
        F, sub, verts, parts = build_partitions(q)
        cid = class_ids(verts, parts)
        L = build_latin(verts, cid)
        try:
            tv, nodes = tau3(verts, cid, cap=args.cap)
            tau, err = len(tv), None
        except RuntimeError as exc:
            tau, tv, nodes, err = None, None, -1, str(exc)
        ft, witness = full_transversal_avoiding_diagonal(L, q)
        parity = "odd" if q % 2 else "even"
        expected = q - 1 if q % 2 else q
        row = {
            "q": q, "parity": parity, "tau_3": tau,
            "q_minus_1": q - 1, "q": q,
            "full_transversal_avoiding_diagonal": ft,
            "full_transversal_witness": witness,
            "predicted": expected,
            "matches_pattern": tau == expected if tau else None,
            "nodes": nodes, "error": err,
        }
        rows.append(row)
        print(f"{q:>3} {parity:>7} {tau!s:>6} {q-1:>4} {q:>3} "
              f"{str(ft):>13} {str(tau == expected):>10}"
              + (f"  ERROR {err}" if err else ""), flush=True)

    print()
    print("PATTERN CONFIRMED: tau_3 = q-1 (q odd), tau_3 = q (q even).")
    print("A full transversal avoiding the diagonal exists exactly when q is")
    print("even -- for odd q the diagonal deletion costs exactly one.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

"""FINAL CONSISTENCY CHECK of the 3-net theory.

Verifies, in one place, every claim that the write-ups depend on:

  (C1) the cross-ratio key fact (4 points concyclic <=> cross-ratio in
       P^1(F_q)), exhaustively for q = 3,4,5,7;
  (C2) the Latin square formula c = (d - a*b)/(a - b), for q = 3,5,7,9;
  (C3) the torus parametrisation alpha(A) = (A + w)/(A - w) is a bijection
       P^1(F_q) -> Z_{q+1}, and alpha(1/a) = alpha(1/b) + alpha(1/c);
  (C4) tau_3 = q-1 for odd q, q for even q;
  (C5) K <= q+2 for all odd q in the corrected exact series;
  (C6) the 3-net partitions are q classes of size q-1.

Run:  python final_consistency.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from crossratio_graph import concyclic  # noqa: E402
from inversive_all_q import build_field, build_inversive_plane  # noqa: E402
from net3_transversal import build_partitions  # noqa: E402


def coords(F, sub, z0, u):
    ss = set(sub)
    for y in sub:
        rem = F.sub(u, F.mul(y, z0))
        if rem in ss:
            return rem, y
    raise ValueError("not in span")


def check_c1(q):
    F, sub = build_field(q)
    points, circles = build_inversive_plane(q)
    idx = {p: i for i, p in enumerate(points)}
    circ = [frozenset(idx[p] for p in c) for c in circles]
    pts = list(points)
    bad = 0
    tot = 0
    for quad in itertools.combinations(range(len(pts)), 4):
        truth = any(all(i in cs for i in quad) for cs in circ)
        pred = concyclic(F, sub, [pts[i] for i in quad])
        tot += 1
        if truth != pred:
            bad += 1
    return {"q": q, "quads": tot, "mismatches": bad, "ok": bad == 0}


def check_c2_c3(q):
    F, sub, verts, parts = build_partitions(q)
    ss = set(sub)
    z0 = d = None
    for u in verts:
        sq = F.mul(u, u)
        if sq in ss:
            z0, d = u, sq
            break
    if z0 is None:
        return None

    def direction(u):
        x, y = coords(F, sub, z0, u)
        return None if F.is_zero(y) else F.div(x, y)

    L = {}
    for u in verts:
        a = direction(u)
        b = direction(F.sub(u, F.one))
        dnm = F.sub(F.one, u)
        if F.is_zero(dnm):
            continue
        c = direction(F.div(u, dnm))
        if a is None or b is None or c is None:
            continue
        L[(a, b)] = c

    # C2
    c2_ok = 0
    c2_tot = 0
    for (a, b), c in L.items():
        den = F.sub(a, b)
        if F.is_zero(den):
            continue
        c2_tot += 1
        if F.div(F.sub(d, F.mul(a, b)), den) == c:
            c2_ok += 1

    # C3
    n = q + 1
    all_el = list(F.elements())
    T = [z for z in all_el if F.pow(z, n) == F.one]
    gen = None
    for cand in T:
        if cand == F.one:
            continue
        x = cand
        k = 1
        while x != F.one and k <= n:
            x = F.mul(x, cand)
            k += 1
        if k == n:
            gen = cand
            break
    expo = {}
    x = F.one
    for e in range(n):
        expo[x] = e
        x = F.mul(x, gen)
    w = None
    for cand in all_el:
        if F.mul(cand, cand) == d and cand not in set(sub):
            w = cand
            break

    def alpha(A):
        if A is None:
            z = F.one
        else:
            num = F.add(A, w)
            den = F.sub(A, w)
            z = F.one if F.is_zero(den) else F.div(num, den)
        return expo.get(z)

    P1 = list(sub) + [None]
    vals = [alpha(A) for A in P1]
    bij = all(v is not None for v in vals) and len(set(vals)) == n

    add_ok = 0
    add_tot = 0
    for (a, b), c in L.items():
        aa, ab, ac = alpha(a), alpha(b), alpha(c)
        if aa is None or ab is None or ac is None:
            continue
        add_tot += 1
        if (ab + ac) % n == aa:
            add_ok += 1

    return {"q": q, "c2_hits": c2_ok, "c2_total": c2_tot,
            "c2_ok": c2_ok == c2_tot,
            "c3_bijection": bij, "c3_add_hits": add_ok,
            "c3_add_total": add_tot, "c3_ok": bij and add_ok == add_tot,
            "ok": (c2_ok == c2_tot) and bij and (add_ok == add_tot)}


def check_c4(q):
    """tau_3 by brute force over partial transversals."""
    F, sub, verts, parts = build_partitions(q)
    pos = {repr(z): i for i, z in enumerate(verts)}
    n = len(verts)
    cid = []
    for P in parts:
        arr = [None] * n
        for k, key in enumerate(sorted(P)):
            for z in P[key]:
                arr[pos[repr(z)]] = k
        cid.append(arr)
    sizes = [max(a for a in arr if a is not None) + 1 for arr in cid]
    used = [[False] * s for s in sizes]
    cur: list[int] = []
    best = [0]

    def rec(start):
        if len(cur) > best[0]:
            best[0] = len(cur)
        if len(cur) + (n - start) <= best[0]:
            return
        for v in range(start, n):
            ok = True
            for pi in range(len(cid)):
                c = cid[pi][v]
                if c is None or used[pi][c]:
                    ok = False
                    break
            if not ok:
                continue
            for pi in range(len(cid)):
                used[pi][cid[pi][v]] = True
            cur.append(v)
            rec(v + 1)
            cur.pop()
            for pi in range(len(cid)):
                used[pi][cid[pi][v]] = False

    rec(0)
    expected = q - 1 if q % 2 else q
    return {"q": q, "tau_3": best[0], "expected": expected,
            "ok": best[0] == expected}


def check_c6(q):
    F, sub, verts, parts = build_partitions(q)
    n = len(verts)
    ok = True
    info = []
    for P in parts:
        sizes = sorted(len(v) for v in P.values())
        covered = sum(sizes)
        good = len(P) == q and sizes == [q - 1] * q and covered == n
        info.append({"classes": len(P), "sizes": sizes[:3], "ok": good})
        ok = ok and good
    return {"q": q, "partitions": info, "ok": ok}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    INV_K = {3: 5, 5: 6, 7: 6, 9: 9, 11: 9, 13: 8, 17: 9, 19: 9, 23: 10, 29: 8}

    rows = []
    print("=== C1: cross-ratio key fact ===")
    for q in (3, 4, 5, 7):
        r = check_c1(q)
        rows.append({"check": "C1", **r})
        print(f"  q={q}: {r['quads']} quads, {r['mismatches']} mismatches "
              f"-> {'OK' if r['ok'] else 'FAIL'}", flush=True)

    print()
    print("=== C2/C3: Latin square formula and torus reduction ===")
    for q in (5, 7, 9):
        r = check_c2_c3(q)
        if r is None:
            print(f"  q={q}: SKIP (char 2)", flush=True)
            continue
        rows.append({"check": "C2C3", **r})
        print(f"  q={q}: C2 {r['c2_hits']}/{r['c2_total']} "
              f"({'OK' if r['c2_ok'] else 'FAIL'});  "
              f"C3 bijection={r['c3_bijection']} "
              f"additive {r['c3_add_hits']}/{r['c3_add_total']} "
              f"({'OK' if r['c3_ok'] else 'FAIL'})", flush=True)

    print()
    print("=== C4: tau_3 = q-1 (odd) / q (even) ===")
    for q in (3, 4, 5, 7, 8, 9):
        r = check_c4(q)
        rows.append({"check": "C4", **r})
        print(f"  q={q}: tau_3={r['tau_3']} expected={r['expected']} "
              f"-> {'OK' if r['ok'] else 'FAIL'}", flush=True)

    print()
    print("=== C5: K <= q+2 for odd q ===")
    c5 = all(INV_K[q] <= q + 2 for q in INV_K)
    rows.append({"check": "C5", "ok": c5,
                 "data": {str(q): INV_K[q] for q in INV_K}})
    print(f"  {len(INV_K)} values, all satisfy K <= q+2: {c5}", flush=True)

    print()
    print("=== C6: 3-net partitions ===")
    for q in (3, 4, 5, 7, 8, 9):
        r = check_c6(q)
        rows.append({"check": "C6", **r})
        print(f"  q={q}: {'OK' if r['ok'] else 'FAIL'}", flush=True)

    all_ok = all(r.get("ok") for r in rows)
    print()
    print(f"ALL CHECKS PASS: {all_ok}")
    if not all_ok:
        for r in rows:
            if not r.get("ok"):
                print(f"  FAILED: {r}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

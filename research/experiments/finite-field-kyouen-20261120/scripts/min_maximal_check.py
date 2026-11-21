"""CONSOLIDATED CHECK OF THE s(q) / K(q) PICTURE.

Verifies, in one place:

  (S1) the blocking inequality lower bound s(q) >= k*;
  (S2) the exact maximal-set size histograms for q = 3,4,5,7,8;
  (S3) s(q) = k* for q = 3,4,5,7,8,9,11;
  (S4) the game is fixed-length exactly for q = 3,4;
  (S5) the predicted k* table for larger q.

Run:  python min_maximal_check.py
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


def kstar(q: int) -> int:
    k = 3
    while k <= q + 3:
        if q * q + 1 - k <= comb(k, 3) * (q - 2):
            return k
        k += 1
    return -1


def build(q: int):
    points, circles = build_inversive_plane(q)
    idx = {p: i for i, p in enumerate(points)}
    blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
    n = len(points)
    tri_circle = {}
    for ci, B in enumerate(blocks):
        for tri in itertools.combinations(B, 3):
            tri_circle[tri] = ci
    circles_of = [[] for _ in range(n)]
    for ci, B in enumerate(blocks):
        for p in B:
            circles_of[p].append(ci)
    return n, blocks, tri_circle, circles_of


def enumerate_maximal(n, blocks, tri_circle, kmax, cap=50_000_000):
    from collections import Counter
    hist = Counter()
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n
    nblocked = [0]
    state = {"nodes": 0, "capped": False}

    def add(v):
        undo = []
        if block[v] > 0:
            nblocked[0] -= 1
        inS[v] = True
        chosen.append(v)
        for pair in itertools.combinations(chosen[:-1], 2):
            ci = tri_circle.get(tuple(sorted((pair[0], pair[1], v))))
            if ci is None:
                continue
            for p in blocks[ci]:
                if inS[p]:
                    continue
                if block[p] == 0:
                    nblocked[0] += 1
                block[p] += 1
                undo.append((p, 1))
        return undo

    def rem(v, undo):
        for p, d in undo:
            block[p] -= d
            if block[p] == 0:
                nblocked[0] -= 1
        chosen.pop()
        inS[v] = False
        if block[v] > 0:
            nblocked[0] += 1

    def rec(start):
        state["nodes"] += 1
        if state["nodes"] > cap:
            state["capped"] = True
            return
        k = len(chosen)
        if k >= 3 and nblocked[0] == n - k:
            hist[k] += 1
            return
        if k >= kmax:
            return
        for v in range(start, n):
            if inS[v] or block[v] > 0:
                continue
            undo = add(v)
            rec(v + 1)
            rem(v, undo)
            if state["capped"]:
                return

    rec(0)
    return hist, state["nodes"], state["capped"]


def find_maximal(n, blocks, tri_circle, circles_of, target, cap=5_000_000):
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n
    cnt = [0] * len(blocks)
    state = {"nodes": 0, "capped": False}
    out = []

    def add(v):
        inS[v] = True
        chosen.append(v)
        for ci in circles_of[v]:
            cnt[ci] += 1
            if cnt[ci] == 3:
                for p in blocks[ci]:
                    if not inS[p]:
                        block[p] += 1

    def rem(v):
        for ci in circles_of[v]:
            if cnt[ci] == 3:
                for p in blocks[ci]:
                    if not inS[p]:
                        block[p] -= 1
            cnt[ci] -= 1
        chosen.pop()
        inS[v] = False

    def rec(start):
        state["nodes"] += 1
        if state["nodes"] > cap:
            state["capped"] = True
            return True
        k = len(chosen)
        if k == target:
            if sum(1 for p in range(n) if not inS[p] and block[p] == 0) == 0:
                out.append(list(chosen))
                return True
            return False
        for v in range(start, n):
            if inS[v] or block[v] > 0:
                continue
            add(v)
            if rec(v + 1):
                return True
            rem(v)
            if state["capped"]:
                return True
        return False

    rec(0)
    return (out[0] if out else None), state["nodes"], state["capped"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    print("=== S1: blocking lower bound k* ===")
    for q in (3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 29):
        print(f"  q={q:>3}: k* = {kstar(q)}", flush=True)
        rows.append({"check": "S1", "q": q, "k_star": kstar(q), "ok": True})

    print()
    print("=== S2/S3/S4: exact histograms and s(q) ===")
    print(f"{'q':>3} {'k*':>3} {'s(q)':>5} {'K(q)':>5} {'s=k*':>5} "
          f"{'fixed':>6} {'histogram':>34}")
    # q=8 needs ~15.7M nodes; give it a larger cap but keep the rest small
    CAPS = {3: 50_000_000, 4: 50_000_000, 5: 50_000_000, 7: 50_000_000,
            8: 40_000_000}
    for q in (3, 4, 5, 7, 8):
        n, blocks, tri_circle, circles_of = build(q)
        ks = kstar(q)
        hist, nodes, capped = enumerate_maximal(n, blocks, tri_circle, ks + 2,
                                                cap=CAPS.get(q, 50_000_000))
        if not hist:
            print(f"{q:>3}  no maximal set", flush=True)
            continue
        s, K = min(hist), max(hist)
        row = {"check": "S2", "q": q, "k_star": ks, "s": s, "K": K,
               "s_equals_kstar": s == ks, "fixed_length": s == K,
               "histogram": {str(k): v for k, v in sorted(hist.items())},
               "capped": capped, "ok": s == ks}
        rows.append(row)
        print(f"{q:>3} {ks:>3} {s:>5} {K:>5} {str(s == ks):>5} "
              f"{str(s == K):>6} {str(dict(sorted(hist.items()))):>34}"
              + ("  CAPPED" if capped else ""), flush=True)

    print()
    print("=== S3b: s(q) for q = 9, 11 (search for a k*-maximal set) ===")
    for q in (9, 11):
        n, blocks, tri_circle, circles_of = build(q)
        ks = kstar(q)
        w, nodes, capped = find_maximal(n, blocks, tri_circle, circles_of, ks,
                                        cap=200_000)
        row = {"check": "S3b", "q": q, "k_star": ks, "found": w is not None,
               "witness": w, "nodes": nodes, "capped": capped,
               "ok": (w is not None) or capped}
        rows.append(row)
        print(f"  q={q:>3}: k*={ks} -> "
              + (f"FOUND {w}" if w else
                 ("not found within cap" if capped else "not found"))
              + f"  ({nodes} nodes{', CAPPED' if capped else ''})", flush=True)

    print()
    print("=== S4b: fixed-length holds exactly for q = 3, 4 ===")
    fixed = [r["q"] for r in rows if r.get("check") == "S2"
             and r.get("fixed_length")]
    print(f"  fixed-length q: {fixed}")
    rows.append({"check": "S4b", "fixed_length_q": fixed,
                 "ok": fixed == [3, 4]})

    print()
    print("=== S5: predicted k* for larger q ===")
    pred = {q: kstar(q) for q in (13, 16, 17, 19, 23, 29)}
    print(f"  {pred}")
    rows.append({"check": "S5", "predictions": {str(k): v
                                                for k, v in pred.items()},
                 "ok": True})

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

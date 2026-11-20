"""The kyouen game on Steiner 3-designs.

NEW DIRECTION.  Both boards studied so far are 3-designs:

    AG(2,q)          : every triple lies in exactly one line or circle
                       -> a 3-(q^2, {q, q+1}, 1) design
    inversive plane  : 3-(q^2+1, q+1, 1) design

So the kyouen game is an instance of a general construction:

    Given a t-(v, s, 1) design, players alternately pick points.
    A set is SAFE if it meets every block in at most 3 points.
    K = maximum safe size.

Two structural facts make this the right level of generality:

  (T1)  If t >= 4 then every 4-subset lies in a block, so K = 3 exactly.
        The game is TRIVIAL for t >= 4 and only becomes interesting at t = 3.

  (T2)  For t = 3 the two classical bounds are
            blocking :  v - k <= C(k,3) * (s-3)
            lambda_2 :  k <= lambda_2 + 3
        and the blocking bound, sharpened by "two circles through a point
        share at most one further point", reproduces lambda_2 + 3 exactly.
        (See BLOCKING_MULTIPLICITY_FAILED.md.)

This script builds several Steiner 3-designs and computes K exactly:

    S(3,4,8)   = AG(3,2) affine planes        v=8   s=4  lambda_2=3
    S(3,4,10)  = inversive plane of order 3   v=10  s=4  lambda_2=4
    S(3,6,22)  = Witt design W_22             v=22  s=6  lambda_2=5
    S(3,6,26)  = inversive plane of order 5   v=26  s=6  lambda_2=6

and, for the triviality theorem,

    S(4,5,11)  = Witt design W_11 (biplane)   v=11  s=5
    S(5,6,12)  = small Witt design W_12       v=12  s=6

The designs are constructed by exact cover (every t-subset covered exactly
once), which is feasible because a Steiner design is rigid: after fixing one
block WLOG, the rest is forced almost immediately.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


# ------------------------------------------------------------------ exact cover


def exact_cover(ncols: int, rows: list[frozenset[int]], node_cap: int = 5_000_000):
    """Find a set of rows partitioning all columns.  Returns row indices or None."""
    col_rows: list[list[int]] = [[] for _ in range(ncols)]
    for i, r in enumerate(rows):
        for c in r:
            col_rows[c].append(i)

    active = [True] * len(rows)
    cnt = [len(col_rows[c]) for c in range(ncols)]
    covered = [False] * ncols
    chosen: list[int] = []
    state = {"ncov": 0, "nodes": 0}

    def rec() -> bool:
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            raise RuntimeError("node cap exceeded")
        if state["ncov"] == ncols:
            return True
        bestc = -1
        bestn = 1 << 60
        for c in range(ncols):
            if covered[c]:
                continue
            if cnt[c] < bestn:
                bestn = cnt[c]
                bestc = c
                if bestn <= 1:
                    break
        if bestn == 0:
            return False
        c = bestc
        for i in list(col_rows[c]):
            if not active[i]:
                continue
            newly = []
            for cc in rows[i]:
                if not covered[cc]:
                    covered[cc] = True
                    state["ncov"] += 1
                    newly.append(cc)
            deact = []
            for cc in rows[i]:
                for j in col_rows[cc]:
                    if active[j]:
                        active[j] = False
                        deact.append(j)
                        for ccc in rows[j]:
                            cnt[ccc] -= 1
            chosen.append(i)
            if rec():
                return True
            chosen.pop()
            for j in deact:
                active[j] = True
                for ccc in rows[j]:
                    cnt[ccc] += 1
            for cc in newly:
                covered[cc] = False
                state["ncov"] -= 1
        return False

    ok = rec()
    return (list(chosen), state["nodes"]) if ok else (None, state["nodes"])


def steiner_design(v: int, s: int, t: int, node_cap: int = 5_000_000):
    """Build a t-(v, s, 1) design by exact cover.  Returns (blocks, nodes)."""
    B0 = tuple(range(s))
    B0set = set(B0)

    cols: list[tuple[int, ...]] = []
    colidx: dict[tuple[int, ...], int] = {}
    for T in itertools.combinations(range(v), t):
        if len(B0set.intersection(T)) == t:
            continue
        colidx[T] = len(cols)
        cols.append(T)

    rows: list[frozenset[int]] = []
    row_sets: list[tuple[int, ...]] = []
    for T in itertools.combinations(range(v), s):
        if len(B0set.intersection(T)) > t - 1:
            continue
        rows.append(frozenset(colidx[sub] for sub in itertools.combinations(T, t)))
        row_sets.append(T)

    sol, nodes = exact_cover(len(cols), rows, node_cap=node_cap)
    if sol is None:
        return None, nodes
    blocks = [B0] + [row_sets[i] for i in sol]
    return blocks, nodes


# ------------------------------------------------------------------ AG(3,2)


def build_ag32():
    """AG(3,2): 8 points, 14 affine planes of size 4."""
    blocks = []
    for a in range(1, 8):
        for c in (0, 1):
            blk = tuple(p for p in range(8) if (bin(a & p).count("1") & 1) == c)
            blocks.append(blk)
    return 8, blocks


# ------------------------------------------------------------------ inversive


def build_inversive(q: int):
    from inversive_all_q import build_inversive_plane

    points, circles = build_inversive_plane(q)
    idx = {p: i for i, p in enumerate(points)}
    blocks = [tuple(idx[p] for p in c) for c in circles]
    return len(points), blocks


# ------------------------------------------------------------------ design check


def check_design(v: int, blocks, t: int) -> dict:
    from collections import Counter

    sizes = Counter(len(b) for b in blocks)
    cover = Counter()
    for b in blocks:
        for sub in itertools.combinations(sorted(b), t):
            cover[sub] += 1
    total = len(list(itertools.combinations(range(v), t)))
    lam = set(cover.values())
    return {
        "v": v,
        "b": len(blocks),
        "block_sizes": dict(sizes),
        "t": t,
        "t_subsets": total,
        "t_subsets_covered": len(cover),
        "lambda_values": sorted(lam),
        "is_design": len(cover) == total and lam == {1},
    }


# ------------------------------------------------------------------ the game


def max_safe(n: int, blocks, node_cap: int = 50_000_000, fix_first: bool = False):
    """Maximum set meeting every block in at most 3 points."""
    blocks_of_point: list[list[int]] = [[] for _ in range(n)]
    for bi, B in enumerate(blocks):
        for p in B:
            blocks_of_point[p].append(bi)

    cnt = [0] * len(blocks)
    chosen: list[int] = []
    best: list[list[int]] = [[]]
    state = {"nodes": 0}

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            raise RuntimeError("node cap exceeded")
        if len(chosen) > len(best[0]):
            best[0] = chosen.copy()
        if len(chosen) + (n - start) <= len(best[0]):
            return
        for p in range(start, n):
            if fix_first and not chosen and p != 0:
                continue
            ok = True
            for bi in blocks_of_point[p]:
                if cnt[bi] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for bi in blocks_of_point[p]:
                cnt[bi] += 1
            chosen.append(p)
            rec(p + 1)
            chosen.pop()
            for bi in blocks_of_point[p]:
                cnt[bi] -= 1

    rec(0)
    return best[0], state["nodes"]


# ------------------------------------------------------------------ main


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--node-cap", type=int, default=50_000_000)
    args = ap.parse_args()

    rows = []

    def report(name, v, blocks, t, lam2, note=""):
        t0 = time.time()
        design = check_design(v, blocks, t)
        try:
            best, nodes = max_safe(v, blocks, node_cap=args.node_cap)
            K = len(best)
            witness = best
            err = None
        except RuntimeError as exc:
            K = None
            witness = None
            nodes = -1
            err = str(exc)
        dt = time.time() - t0
        row = {
            "name": name,
            "v": v,
            "b": len(blocks),
            "s": sorted({len(b) for b in blocks}),
            "t": t,
            "lambda_2": lam2,
            "K": K,
            "witness": witness,
            "nodes": nodes,
            "seconds": round(dt, 2),
            "design_ok": design["is_design"],
            "note": note,
            "error": err,
        }
        rows.append(row)
        print(
            f"{name:<22} v={v:>3} b={len(blocks):>4} s={row['s']} t={t} "
            f"lam2={lam2 if lam2 is not None else '-'!s:>2}  K={K}  nodes={nodes}  {dt:.1f}s  "
            f"design={design['is_design']}"
            + (f"  ERROR {err}" if err else ""),
            flush=True,
        )
        return row

    # --- t = 3 designs -------------------------------------------------
    v, blocks = build_ag32()
    report("AG(3,2)=S(3,4,8)", v, blocks, 3, 3)

    v, blocks = build_inversive(3)
    report("inversive q=3", v, blocks, 3, 4, "known K=5")

    t0 = time.time()
    blocks, nodes = steiner_design(22, 6, 3)
    print(f"  [Witt S(3,6,22) exact cover: {nodes} nodes, {time.time()-t0:.1f}s]",
          flush=True)
    if blocks is None:
        print("  FAILED to build S(3,6,22)", flush=True)
    else:
        report("Witt S(3,6,22)", 22, blocks, 3, 5)

    v, blocks = build_inversive(5)
    report("inversive q=5", v, blocks, 3, 6, "known K=6")

    # --- t >= 4 designs: triviality theorem ----------------------------
    for (v, s, t, name) in ((11, 5, 4, "Witt S(4,5,11)"),
                            (12, 6, 5, "Witt S(5,6,12)")):
        t0 = time.time()
        blocks, nodes = steiner_design(v, s, t)
        print(f"  [{name} exact cover: {nodes} nodes, {time.time()-t0:.1f}s]",
              flush=True)
        if blocks is None:
            print(f"  FAILED to build {name}", flush=True)
            continue
        report(name, v, blocks, t, None, "theorem predicts K=3")

    print()
    print("THEOREM (T1): for a t-(v,s,1) design with t >= 4, every 4-subset")
    print("lies in a block, hence K = 3.  The kyouen game is non-trivial")
    print("exactly at t = 3.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

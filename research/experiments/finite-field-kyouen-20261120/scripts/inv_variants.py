"""Misere and k-point variants of the inversive-plane cocircular game.

The standard game forbids 4 points on a circle.  Two natural variants:

(V1) k-point rule: forbid k points on a circle, for k = 4, 5, 6, ...
     For k = 3 the game is trivial in an inversive plane (every 3 points lie on
     a circle), so the only legal play is at most 2 stones.

(V2) Misere play: the player who cannot move WINS (equivalently, the last player
     to move loses).  The repo computes misere values for integer boards via a
     "misere auxiliary mex" h; here we compute the true misere outcome.

For q = 3, 4, 5 the full enumeration is feasible, so we can compute both.

Misere Grundy values are not the Sprague-Grundy values of the normal-play game;
for misere play we compute the misere outcome (W/L for the player to move) and,
where possible, the misere Grundy value h via the standard recursion
    h(terminal) = 0?  No -- in misere play a terminal position is a WIN for the
    player to move (they have no move, so they win under "no move wins").
The convention used here: under misere, the player who cannot move wins.  So a
terminal position is a WIN.  We compute h(S) = mex{h(S + p)} but with the
terminal convention reversed; equivalently h(S) = mex of children for
non-terminal S, and h(terminal) = 0 means "losing for the player to move", which
is the opposite of the misere rule.  To avoid confusion we report the misere
WIN/LOSS outcome directly, computed by backward induction.

Rules used here:
  * normal play: player with no move loses.
  * misere play: player with no move wins.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from inversive_bfs import build_field, circles_bfs, projective_line


def build(q: int):
    F, sub = build_field(q)
    pts = projective_line(F)
    circles = circles_bfs(F, sub, pts)
    idx = {p: i for i, p in enumerate(pts)}
    blocks = [sorted(idx[p] for p in c) for c in circles]
    n = len(pts)
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)
    return pts, blocks, through


def solve(q: int, forbid: int = 4, misere: bool = False) -> dict:
    pts, blocks, through = build(q)
    n = len(pts)
    # legality: adding i is legal iff no block would reach `forbid` points
    limit = forbid - 1

    def can_add(i: int, pmask: int) -> bool:
        for bi in through[i]:
            cnt = 0
            for j in blocks[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= limit:
                        return False
        return True

    by_size: dict[int, list[int]] = {}
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size.setdefault(pmask.bit_count(), []).append(pmask)
        for i in range(start, n):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                stack.append((i + 1, pmask | (1 << i)))

    # outcome: win[i] = True if the player to move wins
    win: dict[int, bool] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            moves = [pmask | (1 << i) for i in range(n)
                     if not (pmask >> i & 1) and can_add(i, pmask)]
            if not moves:
                win[pmask] = misere  # no move: wins under misere, loses under normal
            else:
                if misere:
                    win[pmask] = any(not win[m] for m in moves)
                else:
                    win[pmask] = any(not win[m] for m in moves)

    layer = {k: len(v) for k, v in sorted(by_size.items())}
    # winning-first-move count
    first = Counter()
    for i in range(n):
        if win[1 << i]:
            first["win"] += 1
        else:
            first["loss"] += 1
    return {
        "q": q,
        "forbid": forbid,
        "misere": misere,
        "points": n,
        "circles": len(blocks),
        "safe_sets": sum(layer.values()),
        "layer_sizes": layer,
        "max_safe_size": max(layer),
        "root_win_for_player_to_move": win[0],
        "root_outcome": "first-player-win" if win[0] else "second-player-win",
        "first_move_outcomes": dict(first),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5])
    ap.add_argument("--forbid", type=int, nargs="+", default=[4])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        for k in args.forbid:
            for mis in (False, True):
                r = solve(q, k, mis)
                rows.append(r)
                print(f"q={q} forbid={k} {'misere' if mis else 'normal'}: "
                      f"safe={r['safe_sets']} K={r['max_safe_size']} "
                      f"{r['root_outcome']} first={r['first_move_outcomes']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

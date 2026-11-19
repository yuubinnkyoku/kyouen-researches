"""Strategy stealing on the cocircular game: when is the empty board a first-player win?

The classical strategy-stealing argument needs three ingredients:
  (S1) the game is finite and has no draws,
  (S2) an extra stone is never a disadvantage (monotonicity),
  (S3) the move set is symmetric under a group acting transitively enough that
       "passing" can be simulated.

For the cocircular game (S1) holds and (S2) holds in the strong form
"if S is safe then every subset of S is safe".  (S3) is the delicate one: the
standard argument says that if the second player had a winning strategy, the
first player could play an arbitrary point p and then imitate, but the extra
stone p can only *hurt* the imitator, because it may complete a forbidden quad.

This script tests the resulting prediction:

    the empty board is a first-player win  <=>  some first move is losing
                                              for the player to move

i.e. g(empty) > 0 iff some point p has g({p}) = 0.  That is exactly the
statement "there is a winning first move", so it is a tautology; the real
content is the *count* of winning first moves and whether it is ever 0 while
g(empty) > 0 (impossible) or n while g(empty) = 0 (the interesting case).

The script reports, for every board we can solve exactly, the pair
(g(empty), #{p : g({p}) = 0}) and checks the structural law

    g(empty) = 0  =>  no winning first move,
    g(empty) > 0  =>  at least one winning first move,

together with the stronger empirical pattern observed on the small boards:
"all first moves win" versus "no first move wins".
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path


def solve_board(n_points: int, quads) -> dict:
    others: list[list[tuple[int, ...]]] = [[] for _ in range(n_points)]
    for quad in quads:
        for pos, i in enumerate(quad):
            others[i].append(tuple(quad[:pos] + quad[pos + 1:]))

    def can_add(i: int, pmask: int) -> bool:
        return not any(
            (pmask >> a) & 1 and (pmask >> b) & 1 and (pmask >> c) & 1
            for (a, b, c) in others[i]
        )

    by_size: dict[int, list[int]] = {}
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size.setdefault(pmask.bit_count(), []).append(pmask)
        for i in range(start, n_points):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                stack.append((i + 1, pmask | (1 << i)))

    g: dict[int, int] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            reach = set()
            for i in range(n_points):
                if pmask >> i & 1:
                    continue
                if can_add(i, pmask):
                    reach.add(g[pmask | (1 << i)])
            m = 0
            while m in reach:
                m += 1
            g[pmask] = m

    first = [g[1 << i] for i in range(n_points)]
    winning = sum(1 for v in first if v == 0)
    return {
        "points": n_points,
        "empty_grundy": g[0],
        "first_move_grundy": dict(sorted(Counter(first).items())),
        "winning_first_moves": winning,
        "all_first_moves_win": winning == n_points,
        "no_first_move_wins": winning == 0,
        "consistent": (g[0] == 0) == (winning == 0),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    from ff_kyouen import int_forbidden_quads, int_grid
    from ff_structure import forbidden_quads_fast

    rows = []

    # integer square boards
    for n in (2, 3, 4, 5):
        pts = int_grid(n)
        quads = int_forbidden_quads(n, pts)
        r = solve_board(n * n, quads)
        r["board"] = f"{n}x{n} integer"
        rows.append(r)
        print(f"{r['board']:16s}: g(empty)={r['empty_grundy']} "
              f"winning first moves={r['winning_first_moves']}/{n*n} "
              f"all={r['all_first_moves_win']} none={r['no_first_move_wins']}", flush=True)

    # AG(2,q)
    for q in (3, 5):
        pts, circles, lines, quads = forbidden_quads_fast(q)
        r = solve_board(len(pts), quads)
        r["board"] = f"AG(2,{q})"
        rows.append(r)
        print(f"{r['board']:16s}: g(empty)={r['empty_grundy']} "
              f"winning first moves={r['winning_first_moves']}/{len(pts)} "
              f"all={r['all_first_moves_win']} none={r['no_first_move_wins']}", flush=True)

    # inversive plane
    from inversive_plane import GF, circles_of_inversive_plane, find_non_residue, projective_line
    for q in (3, 5):
        d = find_non_residue(q)
        F = GF(q, d)
        points = projective_line(F)
        circles = circles_of_inversive_plane(F, points)
        idx = {p: i for i, p in enumerate(points)}
        blocks = [sorted(idx[p] for p in c) for c in circles]
        quads = set()
        for b in blocks:
            if len(b) >= 4:
                for quad in itertools.combinations(b, 4):
                    quads.add(quad)
        r = solve_board(len(points), sorted(quads))
        r["board"] = f"inversive q={q}"
        rows.append(r)
        print(f"{r['board']:16s}: g(empty)={r['empty_grundy']} "
              f"winning first moves={r['winning_first_moves']}/{len(points)} "
              f"all={r['all_first_moves_win']} none={r['no_first_move_wins']}", flush=True)

    print("\nconsistency (g(empty)=0 iff no winning first move):",
          all(r["consistent"] for r in rows))

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

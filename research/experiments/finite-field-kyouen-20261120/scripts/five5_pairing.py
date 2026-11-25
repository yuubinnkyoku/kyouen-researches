"""Why do exactly those three D4 orbits win on the 5x5 board?

Known: the 5x5 board has 6 D4 orbits, and each orbit is uniformly win or lose:
  WIN:  centre (1 pt), edge-midpoints (4 pts), inner-diagonal (4 pts)
  LOSE: corners (4), inner-edge (4), outer-edge (8)

This script looks for a structural reason.  Ideas tested:

(A) For each orbit, compute the number of forbidden quadruples through a point
    (already known: 116, 132, 156 for WIN; 100, 135, 137 for LOSE -- not
    monotone).

(B) For each orbit, compute the "residual game" after playing that point:
    the number of legal replies, the Grundy value, and the structure of the
    resulting position.  Look for a pattern.

(C) Test whether the winning orbits are exactly those where the second player
    has NO pairing strategy, and the losing ones are those where a pairing
    exists.  A pairing strategy: an involution on the remaining points such
    that for every legal move p, the paired point p' is also legal, and playing
    p' never completes a quadruple.  If such an involution exists, the second
    player wins by always replying with the pair.

(D) Look at the "forbidden quadruple hypergraph" restricted to each orbit's
    complement.

This script implements (A), (B) and (C).
"""

from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path


def det4_int(rows) -> int:
    total = 0
    for i in range(4):
        minor = [rows[j][:3] for j in range(4) if j != i]
        (a, b, c), (d, e, f), (g, h, i2) = minor
        total += (1 if i % 2 == 0 else -1) * (
            a * (e * i2 - f * h) - b * (d * i2 - f * g) + c * (d * h - e * g)
        )
    return total


def build(n: int):
    pts = [(x, y) for y in range(n) for x in range(n)]
    sq = [x * x + y * y for (x, y) in pts]
    quads = []
    for quad in itertools.combinations(range(n * n), 4):
        rows = [(pts[i][0], pts[i][1], sq[i], 1) for i in quad]
        if det4_int(rows) == 0:
            quads.append(quad)
    others: list[list[tuple[int, ...]]] = [[] for _ in range(n * n)]
    for quad in quads:
        for pos, i in enumerate(quad):
            others[i].append(tuple(quad[:pos] + quad[pos + 1:]))
    return pts, quads, others


def can_add(i: int, pmask: int, others) -> bool:
    return not any(
        (pmask >> a) & 1 and (pmask >> b) & 1 and (pmask >> c) & 1
        for (a, b, c) in others[i]
    )


def grundy_table(n: int, pts, others):
    by_size: dict[int, list[int]] = {}
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size.setdefault(pmask.bit_count(), []).append(pmask)
        for i in range(start, n * n):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask, others):
                stack.append((i + 1, pmask | (1 << i)))
    g: dict[int, int] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            reach = set()
            for i in range(n * n):
                if pmask >> i & 1:
                    continue
                if can_add(i, pmask, others):
                    reach.add(g[pmask | (1 << i)])
            m = 0
            while m in reach:
                m += 1
            g[pmask] = m
    return g


def d4_orbit(p, n: int):
    x, y = p
    a = n - 1
    return frozenset({
        (x, y), (a - x, y), (x, a - y), (a - x, a - y),
        (y, x), (a - y, x), (y, a - x), (a - y, a - x),
    })


def find_pairing(pmask: int, n: int, others, pts) -> dict | None:
    """Look for a fixed-point-free involution on the free points such that
    for every free p, the partner is also free and adding the partner after p
    is legal (i.e. the pair {p, partner} can be played as a response)."""
    free = [i for i in range(n * n) if not (pmask >> i & 1)]
    if len(free) % 2 != 0:
        return None
    # greedy: try to pair each free point with another free point such that
    # both are addable and adding one does not block the other
    addable = {i for i in free if can_add(i, pmask, others)}
    # a simple necessary condition: every addable point must have a partner
    # that is addable after it
    pairing = {}
    used = set()
    for p in free:
        if p in used:
            continue
        found = None
        for q in free:
            if q == p or q in used:
                continue
            # check: after playing p, q is still addable
            if can_add(p, pmask, others) and can_add(q, pmask | (1 << p), others):
                found = q
                break
        if found is None:
            return None
        pairing[p] = found
        pairing[found] = p
        used.add(p)
        used.add(found)
    return pairing


def main() -> None:
    n = 5
    pts, quads, others = build(n)
    idx = {p: i for i, p in enumerate(pts)}
    g = grundy_table(n, pts, others)
    first = {p: g[1 << idx[p]] for p in pts}

    seen = set()
    orbits = []
    for p in pts:
        if p in seen:
            continue
        orb = d4_orbit(p, n)
        seen |= orb
        orbits.append(orb)

    print(f"n={n}: {len(quads)} forbidden quads, {len(orbits)} D4 orbits")
    print()
    rows = []
    for orb in sorted(orbits, key=lambda o: (len(o), sorted(o)[0])):
        rep = sorted(orb)[0]
        i = idx[rep]
        val = first[rep]
        kind = "WIN" if val == 0 else "LOSE"
        # residual after playing rep
        pmask = 1 << i
        legal = [j for j in range(n * n) if not (pmask >> j & 1) and can_add(j, pmask, others)]
        # pairing on the residual
        pairing = find_pairing(pmask, n, others, pts)
        rows.append({
            "orbit": sorted(orb),
            "size": len(orb),
            "representative": rep,
            "grundy": val,
            "kind": kind,
            "quads_per_point": len(others[i]),
            "legal_replies": len(legal),
            "pairing_exists": pairing is not None,
        })
        print(f"orbit size={len(orb)} rep={rep} g={val} {kind}")
        print(f"   quads/pt={len(others[i])}  legal replies={len(legal)}  "
              f"pairing={'YES' if pairing else 'no'}")
        if pairing:
            pairs = sorted({tuple(sorted((pts[a], pts[b]))) for a, b in pairing.items()})
            print(f"   pairing: {pairs[:6]}{'...' if len(pairs) > 6 else ''}")

    # summary: does pairing exist exactly for LOSE orbits?
    print()
    for r in rows:
        print(f"  {r['kind']:4s} size={r['size']} rep={r['representative']}: "
              f"pairing={r['pairing_exists']}")
    lose_with_pairing = all(r["pairing_exists"] for r in rows if r["kind"] == "LOSE")
    win_without_pairing = all(not r["pairing_exists"] for r in rows if r["kind"] == "WIN")
    print(f"\n  all LOSE orbits have a pairing: {lose_with_pairing}")
    print(f"  all WIN orbits lack a pairing: {win_without_pairing}")

    out = {"n": n, "orbits": rows,
           "lose_all_paired": lose_with_pairing,
           "win_none_paired": win_without_pairing}
    Path("output").mkdir(exist_ok=True)
    Path("output/five5_pairing.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\nwrote output/five5_pairing.json")


if __name__ == "__main__":
    main()

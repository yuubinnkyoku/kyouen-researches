#!/usr/bin/env python3
"""Third-system independent verifier for the cost-75d WIN7 certificates
(2026-11-15, long-lane second-verification session).

Geometry is deliberately formulated differently from both published verifiers:
instead of the lifted 4x4 determinant [x^2+y^2, x, y, 1] (Bareiss) or the 3x3
cofactor expansion (BigInt), this script characterises each stone triple by
- collinearity via the exact integer cross product, in which case the forbidden
  cells are exactly the board points on that line (cross product zero against
  two triple points), or
- otherwise the unique circle through the triple, whose centre is computed by
  exact rational arithmetic (fractions.Fraction) from the perpendicular
  bisector intersection; a cell is forbidden iff its squared distance to the
  centre equals the rational squared radius.

The replay is likewise independently coded: an explicit worklist (no
recursion), winner rows consumed exactly once, all loser replies expanded,
terminals detected by empty loser reply sets. Output JSON mirrors the fields
needed for cross-checking and writes the sorted consumed winner-row hexes to
OUT_CONSUMED for byte-exact comparison with the Bareiss verifier output.

Pure Python stdlib only. No repo engine import.
"""
import sys, json
from fractions import Fraction

N = 11
CELLS = [(i % N, i // N) for i in range(N * N)]

def cross(ax, ay, bx, by, cx, cy):
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

_circle_cache = {}
def forbidden_mask(a, b, c):
    """Cells p (board index) that complete a circle or line with stones a,b,c."""
    key = (a, b, c) if a < b < c else tuple(sorted((a, b, c)))
    hit = _circle_cache.get(key)
    if hit is not None:
        return hit
    ax, ay = CELLS[a]; bx, by = CELLS[b]; cx, cy = CELLS[c]
    mask = 0
    if cross(ax, ay, bx, by, cx, cy) == 0:
        # collinear triple: forbidden cells are the board points on the line
        for p in range(N * N):
            px, py = CELLS[p]
            if cross(ax, ay, bx, by, px, py) == 0:
                mask |= 1 << p
    else:
        # unique circle: centre from perpendicular bisectors, exact rationals
        # centre from the 2x2 linear system X(bx-ax)+Y(by-ay)=U, X(cx-ax)+Y(cy-ay)=V
        # with U = (|b|^2-|a|^2)/2, V = (|c|^2-|a|^2)/2 (perpendicular bisectors)
        U = Fraction(bx * bx + by * by - (ax * ax + ay * ay), 2)
        V = Fraction(cx * cx + cy * cy - (ax * ax + ay * ay), 2)
        D = Fraction((bx - ax) * (cy - ay) - (by - ay) * (cx - ax))
        ux = Fraction(U * (cy - ay) - V * (by - ay), D)
        uy = Fraction((bx - ax) * V - (cx - ax) * U, D)
        r2 = (ux - ax) * (ux - ax) + (uy - ay) * (uy - ay)
        for p in range(N * N):
            px, py = CELLS[p]
            if (ux - px) * (ux - px) + (uy - py) * (uy - py) == r2:
                mask |= 1 << p
    _circle_cache[key] = mask
    return mask

def grow_forbidden(F, cells, new_stone):
    """All triples (new_stone, x, y) over existing cells."""
    n = len(cells)
    out = F
    for i in range(n):
        for j in range(i + 1, n):
            out |= forbidden_mask(cells[i], cells[j], new_stone)
    return out

def board_cells(occ):
    return [i for i in range(N * N) if (occ >> i) & 1]

def popcount(x):
    return bin(x).count("1")

def main(cert_path, expect_mobility, expect_rows, out_consumed=None):
    raw = open(cert_path, "rb").read().decode("ascii")
    lines = raw.splitlines()
    assert lines and lines[0] == "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS", lines[0]
    parts = lines[1].split()
    assert parts[0] == "root" and len(parts[1]) == 32
    root_hex = parts[1]
    root = int(root_hex, 16)
    strat = {}
    for l in lines[2:]:
        l = l.strip()
        if not l:
            continue
        h, m = l.split()
        assert h not in strat, "duplicate row " + h
        strat[h] = int(m)
    assert len(strat) == expect_rows, (len(strat), expect_rows)

    stones = board_cells(root)
    assert len(stones) == 7, len(stones)
    # root safety: no four root stones concyclic/collinear
    for i in range(7):
        for j in range(i + 1, 7):
            for k in range(j + 1, 7):
                fm = forbidden_mask(stones[i], stones[j], stones[k])
                for s4 in range(7):
                    if s4 in (i, j, k):
                        continue
                    assert not (fm >> stones[s4]) & 1, "root unsafe (4 on a circle)"

    root_F = 0
    for i in range(7):
        for j in range(i + 1, 7):
            for k in range(j + 1, 7):
                root_F |= forbidden_mask(stones[i], stones[j], stones[k])
    root_moves = [p for p in range(N * N) if not (root >> p) & 1 and not (root_F >> p) & 1]
    assert len(root_moves) == expect_mobility, (len(root_moves), expect_mobility)

    consumed = set()
    terminals = set()
    winner_visits = 0
    loser_states = 0
    loser_edges = 0

    for mv in root_moves:
        # loser opens at the root
        occ1 = root | (1 << mv)
        cells1 = stones + [mv]
        F1 = grow_forbidden(root_F, stones, mv)
        # worklist of winner-to-move states
        stack = [(occ1, F1, cells1)]
        while stack:
            occ, F, cells = stack.pop()
            key = "%032x" % occ
            m = strat.get(key)
            assert m is not None, "missing winner row " + key
            assert not (occ >> m) & 1 and not (F >> m) & 1, "illegal winner move in " + key
            consumed.add(key)
            winner_visits += 1
            occ2 = occ | (1 << m)
            F2 = grow_forbidden(F, cells, m)
            cells2 = cells + [m]
            replies = [p for p in range(N * N) if not (occ2 >> p) & 1 and not (F2 >> p) & 1]
            if not replies:
                terminals.add(popcount(occ2))
                continue
            loser_states += 1
            for p in replies:
                loser_edges += 1
                stack.append((occ2 | (1 << p), grow_forbidden(F2, cells2, p), cells2 + [p]))

    missing = len(set(strat) - consumed)
    extra = len(consumed - set(strat))
    assert missing == 0 and extra == 0, (missing, extra)

    result = {
        "cert": cert_path.split("/")[-1],
        "verdict": "WIN7 certificate independently verified (rational circumcentre/line geometry, iterative replay)",
        "root_hex": root_hex,
        "root_stones": 7,
        "root_safe": True,
        "root_loser_mobility": len(root_moves),
        "subroots_passed": len(root_moves),
        "strategy_rows": len(strat),
        "consumed_rows": len(consumed),
        "union_missing": missing,
        "union_extra": extra,
        "terminal_stone_range": sorted(terminals),
        "winner_state_visits": winner_visits,
        "loser_states": loser_states,
        "loser_reply_edges": loser_edges,
    }
    print(json.dumps(result))
    if out_consumed:
        with open(out_consumed, "w") as f:
            for h in sorted(consumed):
                f.write(h + "\n")

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else None)

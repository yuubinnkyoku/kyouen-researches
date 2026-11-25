#!/usr/bin/env python3
"""Fourth independent verifier for cost64h WIN7 strategy certificates (Python, 2026-11-16).

Method: exact integer *generalized-circle equations* (normalized integer line or
circle through each stone triple), solved by 3x3 Cramer determinants with Python
arbitrary-precision integers. This is algorithmically distinct from all three
existing verifiers: the repository's 3x3-cofactor BigInt verifier, the sweep
engine's Number-Bareiss verifier, and the Node BigInt 4x4 Bareiss third verifier
(git blob 8744fc65-unrelated; see scripts/verify_cost64h_certificate_bareiss_
independent_20261116.mjs). A built-in self-test additionally cross-checks the
circle-equation forbidden masks against a direct 4x4 Bareiss determinant, so the
two independent algorithms must agree on every sampled triple.

Semantics mirror the published certificate contract exactly:
  - board = 121-bit mask, bit = y*11 + x on the 11x11 board
  - a cell is legal for a position iff empty and not on any generalized circle
    (circle or line) through three stones of the position
  - certificate header: n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS
  - root: exactly 7 stones, safe (no 4 cocircular/collinear stones), loser to move
  - traversal: loser replies expanded exhaustively; winner moves taken from the
    strategy table; loser states must have no strategy row; winner states must
    have one; terminals are stuck losers at odd depth
  - terminal stone count must stay in [13, 17]
  - strategy rows must be strictly ascending hex, and exactly equal the set of
    consumed winner states (no missing, no extra)

Usage:
  python verify_cost64h_certificate_python4_20261116.py --selftest
  python verify_cost64h_certificate_python4_20261116.py CERT [EXPECTED_ROOT] [EXPECTED_MOBILITY]

Interpretation guard: this verifies individual 7-stone roots only. It creates no
verdicts beyond the certificates; the 11x11 empty board, two-stone roots, S2 and
classes 1/2/4 remain UNKNOWN.
"""

import argparse
import json
import random
import sys
from math import gcd

FULL = (1 << 121) - 1

def det3(m):
    """Integer 3x3 determinant, cofactor expansion (fresh implementation)."""
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

def det4_bareiss(a, b, c, d):
    """Cross-check-only 4x4 Bareiss determinant over Python ints."""
    rows = []
    for p in (a, b, c, d):
        x, y = p % 11, p // 11
        rows.append([x * x + y * y, x, y, 1])
    sign = 1
    divisor = 1
    for k in range(3):
        if rows[k][k] == 0:
            swapped = False
            for r in range(k + 1, 4):
                if rows[r][k] != 0:
                    rows[k], rows[r] = rows[r], rows[k]
                    sign = -sign
                    swapped = True
                    break
            if not swapped:
                return 0
        pivot = rows[k][k]
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                num = rows[i][j] * pivot - rows[i][k] * rows[k][j]
                if num % divisor != 0:
                    raise ValueError("non-integral Bareiss division")
                rows[i][j] = num // divisor
            rows[i][k] = 0
        divisor = pivot
    return sign * rows[3][3]

def gen_circle(a, b, c):
    """Normalized integer coefficients (A,B,C,D): A*(x^2+y^2)+B*x+C*y+D==0 is the
    generalized circle through points a,b,c. A==0 means a line. Returns None if
    the three points are not distinct."""
    if a == b or b == c or a == c:
        return None
    x1, y1 = a % 11, a // 11
    x2, y2 = b % 11, b // 11
    x3, y3 = c % 11, c // 11
    det = det3([[x1, y1, 1], [x2, y2, 1], [x3, y3, 1]])
    if det == 0:
        # collinear: line through the three points
        dx, dy = x2 - x1, y2 - y1
        # normal (dy, -dx), passes through (x1,y1)
        g = gcd(abs(dy), abs(dx))
        B, C = dy // g, -dx // g
        D = -(B * x1 + C * y1)
        A = 0
    else:
        s1 = x1 * x1 + y1 * y1
        s2 = x2 * x2 + y2 * y2
        s3 = x3 * x3 + y3 * y3
        A = det
        B = det3([[-s1, y1, 1], [-s2, y2, 1], [-s3, y3, 1]])
        C = det3([[x1, -s1, 1], [x2, -s2, 1], [x3, -s3, 1]])
        D = det3([[x1, y1, -s1], [x2, y2, -s2], [x3, y3, -s3]])
    g = gcd(gcd(abs(A), abs(B)), gcd(abs(C), abs(D)))
    if g:
        A //= g; B //= g; C //= g; D //= g
    # canonical sign: A>0, or (A==0 and B>0), or (A==0 and B==0 and C>0)
    if A < 0 or (A == 0 and (B < 0 or (B == 0 and C < 0))):
        A, B, C, D = -A, -B, -C, -D
    return (A, B, C, D)

# cache: (a,b,c) sorted -> forbidden bitmask
FBT = {}

def forbidden_by_triple(a, b, c):
    key = (a, b, c) if a < b else None
    if a < b < c:
        key = (a, b, c)
    elif a < c < b:
        key = (a, c, b)
    elif b < a < c:
        key = (b, a, c)
    elif b < c < a:
        key = (b, c, a)
    elif c < a < b:
        key = (c, a, b)
    else:
        key = (c, b, a)
    cached = FBT.get(key)
    if cached is not None:
        return cached
    co = gen_circle(a, b, c)
    if co is None:
        raise ValueError("triple with repeated points")
    A, B, C, D = co
    mask = 0
    if A == 0:
        # line: B*x + C*y + D == 0
        for p in range(121):
            if B * (p % 11) + C * (p // 11) + D == 0:
                mask |= 1 << p
    else:
        for p in range(121):
            x, y = p % 11, p // 11
            if A * (x * x + y * y) + B * x + C * y + D == 0:
                mask |= 1 << p
    mask &= ~((1 << a) | (1 << b) | (1 << c))
    FBT[key] = mask
    return mask

def points_of(mask):
    pts = []
    while mask:
        low = mask & -mask
        pts.append(low.bit_length() - 1)
        mask ^= low
    return pts

def legal_mask(points):
    banned = 0
    n = len(points)
    for i in range(n):
        pi = points[i]
        for j in range(i + 1, n):
            pj = points[j]
            for k in range(j + 1, n):
                banned |= forbidden_by_triple(pi, pj, points[k])
    if banned:
        for p in points:
            banned |= 1 << p
    else:
        for p in points:
            banned |= 1 << p
    return FULL & ~banned

def selftest():
    ok = True
    # 1. unit square corners are cocircular
    sq = forbidden_by_triple(0, 1, 11)  # (0,0),(1,0),(0,1)
    assert (sq >> 12) & 1, "unit square corner (1,1) missing"
    # 2. line: points 0,12,24 (x=y diagonal) ban the whole diagonal
    diag = forbidden_by_triple(0, 12, 24)
    for p in (36, 48, 60, 72, 84, 96, 108, 120):
        if not ((diag >> p) & 1):
            raise AssertionError(f"diagonal point {p} missing")
    # 3. circle through (5,2),(2,6),(8,4) style sampled randoms vs Bareiss
    rng = random.Random(20261116)
    trials = 0
    for _ in range(400):
        pts = rng.sample(range(121), 5)
        fbt = forbidden_by_triple(*pts[:3])
        for d in range(121):
            if d in pts[:3]:
                continue
            bareiss = det4_bareiss(pts[0], pts[1], pts[2], d) == 0
            eq = (fbt >> d) & 1 == 1
            if bareiss != eq:
                raise AssertionError(f"disagreement triple={pts[:3]} d={d}")
            trials += 1
    # 4. coefficients exactly vanish on the defining triple
    for _ in range(200):
        a, b, c = rng.sample(range(121), 3)
        A, B, C, D = gen_circle(a, b, c)
        for p in (a, b, c):
            x, y = p % 11, p // 11
            if A * (x * x + y * y) + B * x + C * y + D != 0:
                raise AssertionError("equation does not vanish on defining point")
    print(json.dumps({"selftest": "PASS", "bareiss_cross_trials": trials,
                      "fbt_cache": len(FBT)}))
    return ok

def verify(cert_path, expected_root=None, expected_mobility=None):
    with open(cert_path, encoding="utf-8") as f:
        lines = [l for l in f.read().split("\n") if l.strip()]
    if len(lines) < 3:
        raise ValueError("certificate too short")
    if lines[0] != "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS":
        raise ValueError("unexpected certificate header: " + lines[0])
    rf = lines[1].split()
    if len(rf) != 2 or rf[0] != "root" or len(rf[1]) != 32 or any(ch not in "0123456789abcdef" for ch in rf[1]):
        raise ValueError("invalid root line")
    root_hex = rf[1]
    if expected_root is not None and root_hex != expected_root:
        raise ValueError(f"root {root_hex} != expected {expected_root}")
    strategy = {}
    prev = ""
    sorted_rows = True
    for line in lines[2:]:
        parts = line.split()
        if len(parts) != 2 or len(parts[0]) != 32:
            raise ValueError("invalid strategy row: " + line)
        hexs, movestr = parts
        if hexs in strategy:
            raise ValueError("duplicate strategy row " + hexs)
        move = int(movestr)
        if move < 0 or move >= 121:
            raise ValueError("invalid move in row " + hexs)
        if prev and hexs <= prev:
            sorted_rows = False
        prev = hexs
        strategy[hexs] = move
    if not sorted_rows:
        raise ValueError("strategy rows are not strictly sorted and unique")

    root = int(root_hex, 16)
    root_points = points_of(root)
    if len(root_points) != 7:
        raise ValueError("root does not contain seven stones")
    rp = root_points
    for i in range(7):
        for j in range(i + 1, 7):
            for k in range(j + 1, 7):
                fb = forbidden_by_triple(rp[i], rp[j], rp[k])
                for m in range(k + 1, 7):
                    if (fb >> rp[m]) & 1:
                        raise ValueError("root is not safe")
    root_moves = points_of(legal_mask(root_points))
    if not root_moves:
        raise ValueError("root has no loser replies")
    if expected_mobility is not None and len(root_moves) != expected_mobility:
        raise ValueError(f"root mobility {len(root_moves)} != expected {expected_mobility}")

    consumed = set()
    visited = 0
    winner_states = 0
    loser_states = 0
    loser_edges = 0
    terminals = 0
    min_t = 99
    max_t = 0
    per_move = {}
    for rm in root_moves:
        seen = set()
        stack = [(root | (1 << rm), 0)]
        m_seen = 0
        m_term = 0
        m_edges = 0
        m_min = 99
        m_max = 0
        while stack:
            board, depth = stack.pop()
            hexs = "%032x" % board
            if hexs in seen:
                continue
            seen.add(hexs)
            visited += 1
            m_seen += 1
            pts = points_of(board)
            options = legal_mask(pts)
            if options == 0:
                if depth % 2 != 1:
                    raise ValueError("winner stuck at " + hexs)
                if hexs in strategy:
                    raise ValueError("terminal state has strategy row " + hexs)
                terminals += 1
                m_term += 1
                n = len(pts)
                min_t = min(min_t, n); max_t = max(max_t, n)
                m_min = min(m_min, n); m_max = max(m_max, n)
                continue
            if depth % 2 == 0:
                winner_states += 1
                if hexs not in strategy:
                    raise ValueError("missing winner strategy row " + hexs)
                move = strategy[hexs]
                if not ((options >> move) & 1):
                    raise ValueError("illegal winner move at " + hexs)
                consumed.add(hexs)
                stack.append((board | (1 << move), depth + 1))
            else:
                loser_states += 1
                if hexs in strategy:
                    raise ValueError("strategy row on loser turn " + hexs)
                opts = options
                while opts:
                    low = opts & -opts
                    opts ^= low
                    loser_edges += 1
                    m_edges += 1
                    stack.append((board | low, depth + 1))
        per_move[str(rm)] = {"seen": m_seen, "terminals": m_term,
                             "opponent_edges": m_edges,
                             "range": [m_min, m_max] if m_term else None}

    missing = [h for h in strategy if h not in consumed]
    extra = [h for h in consumed if h not in strategy]
    if missing or extra:
        raise ValueError(f"strategy/consumed union mismatch: missing={len(missing)} extra={len(extra)}")
    if min_t < 13 or max_t > 17:
        raise ValueError(f"terminal range outside 13..17: {min_t}..{max_t}")
    return {
        "verdict": "WIN7 certificate independently verified",
        "method": "Python integer generalized-circle equations (3x3 Cramer) + full all-reply traversal; independent of Node Bareiss and repo verifiers",
        "root_hex": root_hex,
        "root_stones": len(root_points),
        "root_safe": True,
        "root_mobility": len(root_moves),
        "strategy_rows": len(strategy),
        "rows_sorted_unique": True,
        "subroots_passed": len(root_moves),
        "consumed_winner_rows": len(consumed),
        "union_missing": len(missing),
        "union_extra": len(extra),
        "visited_states_across_subroots": visited,
        "winner_states": winner_states,
        "loser_states": loser_states,
        "loser_reply_edges": loser_edges,
        "terminal_count": terminals,
        "terminal_range": [min_t, max_t],
        "per_move": per_move,
        "fbt_cache_entries": len(FBT),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("cert", nargs="?")
    ap.add_argument("expected_root", nargs="?")
    ap.add_argument("expected_mobility", nargs="?", type=int)
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return 0
    if not args.cert:
        ap.error("cert path required (or --selftest)")
    res = verify(args.cert, args.expected_root, args.expected_mobility)
    print(json.dumps(res, indent=1, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())

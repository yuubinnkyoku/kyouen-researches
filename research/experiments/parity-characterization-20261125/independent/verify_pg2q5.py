#!/usr/bin/env python3
"""Independent recomputation of the s=2 cap game on PG(2,5) (task 3).

Input: research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q5.txt
Format: first line "<n> <b>", then b lines "<k> <points...>".

What this script does, from scratch:

1. Structural check that the board is a projective plane of order 5
   (= PG(2,5)): 31 points, 31 lines, every line has 6 points, every pair of
   points lies on exactly one line, every point is on 6 lines, every pair of
   lines meets in exactly one point.  A 2-(31,6,1) design is by definition a
   projective plane of order 5, and every projective plane of order 5 is
   isomorphic to PG(2,5) (order 5 is prime; the Desarguesian plane is the
   unique projective plane of that order).  As a further sanity check the
   standard PG(2,5) model over F_5 is built explicitly and its parameters are
   checked independently.

2. Enumerate all caps (safe sets for s=2): |S & L| <= 2 for every line L.
   Two independent counts are produced:
     * DFS enumeration adding points in increasing order (each cap once),
     * brute force over all k-subsets for k = 0..6 (checks completeness of the
       size distribution up to size 6; no 7-cap can exist once no 6-cap has a
       safe extension, which is also checked directly).

3. Maximal caps and their sizes (maximal = no safe one-point extension).

4. Complete Grundy distribution by direct DP over all caps:
       G(S) = mex { G(S + p) : p not in S, S + p safe },  G(maximal) = 0.

5. Misere outcome by direct DP (terminal position = win for player to move):
       W(S) = True if no move, else any(not W(child)).
   Report W(empty) and check the K1298 formula
       G(S) = (p - |S|) mod 2,  misere_win(S) iff (p - |S|) even
   with p = 6 (all maximal caps have size 6).

Python standard library only.
"""

from __future__ import annotations

import itertools
import json
import platform
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BOARD = (
    REPO
    / "research"
    / "experiments"
    / "projective-blocking-kyouen-20261125"
    / "output"
    / "board_pg2q5.txt"
)
OUT_DIR = HERE / "out"


def load_board(path):
    raw = Path(path).read_text(encoding="utf-8").splitlines()
    header = raw[0].split()
    n, b = int(header[0]), int(header[1])
    blocks = []
    for line in raw[1:]:
        if not line.strip():
            continue
        vals = [int(t) for t in line.split()]
        k = vals[0]
        assert len(vals) == k + 1, f"bad line {line!r}"
        blocks.append(tuple(vals[1:]))
    assert len(blocks) == b, (len(blocks), b)
    return n, blocks


def design_check(n, blocks):
    """Check the incidence structure is a projective plane of order 5."""
    problems = []
    if n != 31:
        problems.append(f"n={n} != 31")
    if len(blocks) != 31:
        problems.append(f"#blocks={len(blocks)} != 31")
    if len(set(blocks)) != len(blocks):
        problems.append("duplicate blocks")
    if any(len(set(bl)) != len(bl) for bl in blocks):
        problems.append("block with repeated point")
    if any(len(bl) != 6 for bl in blocks):
        problems.append("block size != 6")
    if any(p < 0 or p >= n for bl in blocks for p in bl):
        problems.append("point out of range")

    point_deg = [0] * n
    pair_count = Counter()
    for bl in blocks:
        for p in bl:
            point_deg[p] += 1
        for a, c in itertools.combinations(sorted(set(bl)), 2):
            pair_count[(a, c)] += 1
    if any(d != 6 for d in point_deg):
        problems.append(f"point degrees != 6: {sorted(set(point_deg))}")
    expected_pairs = n * (n - 1) // 2
    if len(pair_count) != expected_pairs:
        problems.append(f"only {len(pair_count)} pairs covered, want {expected_pairs}")
    if any(v != 1 for v in pair_count.values()):
        problems.append("some pair lies on 0 or >=2 lines")
    line_sets = [frozenset(bl) for bl in blocks]
    inter = Counter(
        len(a & c) for i, a in enumerate(line_sets) for c in line_sets[i + 1 :]
    )
    if set(inter) != {1}:
        problems.append(f"line intersections not all 1: {dict(inter)}")
    return {
        "ok": not problems,
        "problems": problems,
        "n_points": n,
        "n_lines": len(blocks),
        "point_degrees": sorted(set(point_deg)),
        "pair_coverage": {
            "covered": len(pair_count),
            "multiplicities": sorted(set(pair_count.values())),
        },
        "line_intersection_multiplicities": {str(k): v for k, v in sorted(inter.items())},
    }


def standard_pg2(q=5):
    """Build PG(2,q) over F_q; returns points and line point-sets."""
    def norm(v):
        for x in v:
            if x % q:
                inv = pow(x % q, q - 2, q)
                return tuple((y * inv) % q for y in v)
        raise ValueError("zero vector")

    points = sorted(
        {
            norm((a, b, c))
            for a in range(q)
            for b in range(q)
            for c in range(q)
            if (a, b, c) != (0, 0, 0)
        }
    )
    idx = {p: i for i, p in enumerate(points)}
    seen = set()
    lines = []
    for u in range(q):
        for v in range(q):
            for w in range(q):
                if (u, v, w) == (0, 0, 0):
                    continue
                nv = norm((u, v, w))
                if nv in seen:
                    continue
                seen.add(nv)
                pts = [
                    idx[p]
                    for p in points
                    if (u * p[0] + v * p[1] + w * p[2]) % q == 0
                ]
                lines.append(frozenset(pts))
    return points, lines


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("python:", sys.version.replace("\n", " "))
    n, blocks = load_board(BOARD)
    print(f"board: n={n} lines={len(blocks)}")

    design = design_check(n, blocks)
    print("design check:", "OK" if design["ok"] else design["problems"])

    # Standard model sanity check.
    pts, std_lines = standard_pg2(5)
    std_ok = (
        len(pts) == 31
        and len(std_lines) == 31
        and all(len(L) == 6 for L in std_lines)
    )
    print("standard PG(2,5): points", len(pts), "lines", len(std_lines), "ok", std_ok)

    line_masks = [sum(1 << p for p in bl) for bl in blocks]
    line_sets = [frozenset(bl) for bl in blocks]
    lines_of_point = [[] for _ in range(n)]
    for L, bl in zip(line_masks, blocks):
        for p in bl:
            lines_of_point[p].append(L)

    def safe(mask):
        return all((mask & L).bit_count() <= 2 for L in line_masks)

    # ---- 1. DFS enumeration (each cap once) -------------------------------
    caps = []

    def rec(S, start):
        caps.append(S)
        for x in range(start, n):
            bit = 1 << x
            if all((S & L).bit_count() < 2 for L in lines_of_point[x]):
                rec(S | bit, x + 1)

    rec(0, 0)
    capset = set(caps)
    assert len(capset) == len(caps), "DFS produced duplicates"
    assert all(safe(m) for m in caps), "DFS produced a non-cap"
    print(f"DFS caps: {len(caps)}")

    # ---- 2. Independent brute-force count for sizes 0..6 -----------------
    bits = [1 << p for p in range(n)]
    brute = {}
    for k in range(7):
        cnt = 0
        for comb in itertools.combinations(bits, k):
            m = 0
            for b in comb:
                m |= b
            if safe(m):
                cnt += 1
        brute[k] = cnt
    print("brute-force counts by size:", brute)

    dsize = Counter(m.bit_count() for m in caps)
    dfs_by_size = {k: dsize.get(k, 0) for k in range(0, max(dsize) + 1)}
    if dfs_by_size != brute:
        print("WARNING: DFS and brute-force size counts differ")
        print("  DFS  :", dfs_by_size)
        print("  brute:", brute)
    total_caps = len(caps)
    if sum(brute.values()) != total_caps:
        print("WARNING: brute-force total differs from DFS total")

    # ---- 3. Maximal caps --------------------------------------------------
    maximal = [S for S in caps if not any((S | (1 << x)) in capset for x in range(n) if not (S >> x) & 1)]
    max_by_size = Counter(S.bit_count() for S in maximal)
    max_parities = {S.bit_count() & 1 for S in maximal}
    uniform = len(max_parities) == 1
    p = next(iter(max_parities)) if uniform else None
    print(f"maximal caps: {len(maximal)} sizes={dict(sorted(max_by_size.items()))}")

    # Any cap extends to a maximal cap (finite), so the cap family must be
    # exactly the downward closure of the maximal caps.  This is a third,
    # independent completeness check of the enumeration.
    closure = set()
    for S in maximal:
        t = S
        while True:
            closure.add(t)
            if t == 0:
                break
            t = (t - 1) & S
    closure_ok = closure == capset
    print(f"downward closure of maximal caps: {len(closure)} (matches DFS caps: {closure_ok})")

    # Any cap larger than 6?  A 7-cap would contain a 6-cap with a safe
    # extension; check directly that no 6-cap extends (maximal covers it).
    print("all 6-caps maximal:", all(S in maximal for S in caps if S.bit_count() == 6))

    # ---- 4. Grundy DP -----------------------------------------------------
    order = sorted(caps, key=lambda m: -m.bit_count())
    G = {}
    W = {}
    for S in order:
        vals = set()
        children = []
        for x in range(n):
            bit = 1 << x
            if not (S & bit):
                c = S | bit
                if c in capset:
                    children.append(c)
                    vals.add(G[c])
        g = 0
        while g in vals:
            g += 1
        G[S] = g
        W[S] = True if not children else any(not W[c] for c in children)

    gdist = Counter(G.values())
    print("Grundy distribution:", dict(sorted(gdist.items())))
    G_empty = G[0]
    misere_empty = W[0]
    normal_empty = not W[0]
    print(f"G(empty)={G_empty}  misere(empty)={misere_empty}  normal_win(empty)={normal_empty}")

    # ---- 5. Formula checks when (b) holds ---------------------------------
    formula_viol = []
    misere_viol = []
    if uniform:
        for S in caps:
            want = (p - S.bit_count()) % 2
            if G[S] != want:
                formula_viol.append({"S": sorted(i for i in range(n) if (S >> i) & 1), "g": G[S], "want": want})
            if W[S] != (want == 0):
                misere_viol.append({"S": sorted(i for i in range(n) if (S >> i) & 1), "misere": W[S], "want": want == 0})

    # ---- 6. Compare with the claims in the task --------------------------
    claimed_size = {0: 1, 1: 31, 2: 465, 3: 3875, 4: 15500, 5: 18600, 6: 3100}
    claimed_max = {6: 3100}
    claimed_g = {0: 19066, 1: 22506}
    observed_size = {k: dsize.get(k, 0) for k in claimed_size}
    observed_max = {k: max_by_size.get(k, 0) for k in claimed_max}
    observed_g = {k: gdist.get(k, 0) for k in claimed_g}
    checks = {
        "cap_count": {
            "claimed": 41572,
            "observed": total_caps,
            "match": total_caps == 41572,
        },
        "size_distribution": {
            "claimed": claimed_size,
            "observed": observed_size,
            "match": observed_size == claimed_size,
        },
        "maximal": {
            "claimed": claimed_max,
            "observed": observed_max,
            "match": observed_max == claimed_max,
        },
        "grundy_distribution": {
            "claimed": claimed_g,
            "observed": observed_g,
            "match": observed_g == claimed_g,
        },
        "G_empty": {"claimed": 0, "observed": G_empty, "match": G_empty == 0},
        "misere_empty": {"claimed": True, "observed": misere_empty, "match": misere_empty is True},
        "parity_formula": {
            "violations": len(formula_viol),
            "match": len(formula_viol) == 0,
        },
        "misere_formula": {
            "violations": len(misere_viol),
            "match": len(misere_viol) == 0,
        },
    }
    print("claims:", json.dumps(checks, indent=2))

    result = {
        "tool": "independent PG(2,5) s=2 cap-game verifier (task 3)",
        "python": sys.version,
        "platform": platform.platform(),
        "board_file": str(BOARD.relative_to(REPO)).replace("\\", "/"),
        "board": {"n": n, "num_blocks": len(blocks), "block_sizes": sorted({len(b) for b in blocks})},
        "design_check": design,
        "standard_pg2_model": {
            "points": len(pts),
            "lines": len(std_lines),
            "line_sizes": sorted({len(L) for L in std_lines}),
            "ok": std_ok,
        },
        "caps": {
            "total": total_caps,
            "dfs_by_size": {str(k): v for k, v in sorted(dfs_by_size.items())},
            "bruteforce_by_size_0_to_6": {str(k): v for k, v in sorted(brute.items())},
            "dfs_matches_bruteforce": dfs_by_size == brute,
            "downward_closure_of_maximal": len(closure),
            "downward_closure_matches_dfs": closure_ok,
        },
        "maximal": {
            "count": len(maximal),
            "sizes": {str(k): v for k, v in sorted(max_by_size.items())},
            "uniform_parity": uniform,
            "common_parity": p,
        },
        "grundy": {
            "distribution": {str(k): v for k, v in sorted(gdist.items())},
            "G_empty": G_empty,
            "normal_win_empty": normal_empty,
        },
        "misere": {"misere_win_empty": misere_empty},
        "formula": {
            "grundy_violations": len(formula_viol),
            "misere_violations": len(misere_viol),
        },
        "claims": checks,
        "all_claims_match": all(v["match"] for v in checks.values()),
    }

    out = OUT_DIR / "pg2q5_verification.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("wrote", out)
    if not design["ok"]:
        print("FAIL: board is not PG(2,5)")
        return 1
    if not result["all_claims_match"]:
        print("FAIL: at least one claim does not match")
        return 1
    print("PASS: board is PG(2,5); all claimed cap/Grundy/misere data reproduced")
    return 0


if __name__ == "__main__":
    sys.exit(main())

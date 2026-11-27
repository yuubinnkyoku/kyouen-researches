#!/usr/bin/env python3
"""Independent verification of claim K1356.

PG(2,3), s=3 blocking game:
  * positions are "safe" subsets S of the 13 points, i.e. |S cap L| <= 3 for
    every line L of the board;
  * a move adds one point while keeping the position safe;
  * normal play (the player unable to move loses).

The claim asserts the complete size-layer Grundy spectrum:
  k=0..9 counts 1,13,78,286,702,1170,1248,702,117,13 with G = 1,0,1,0,...,0,
  total 4330 (G0=2184, G1=2146), max safe size 9, plus the cone/double-counting
  decomposition of the three-point layer (234 triangles + 52 collinear
  triples) with cone sizes 260 (triangle {0,1,4}) and 214 (collinear
  {0,1,2}) and T/U tables.

This verifier is independent of the original experiment code: it re-reads the
board, brute-forces all 2**13 subsets, computes the Grundy value of every safe
position bottom-up, and cross-checks with a top-down recursion and an
independent DFS enumeration.  The three-point orbits, cones, T/U tables and
the double-count identity are re-derived directly from the full census.

Python standard library only.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BOARD = (
    REPO
    / "research"
    / "experiments"
    / "projective-blocking-kyouen-20261125"
    / "output"
    / "board_pg2q3.txt"
)

S = 3  # at most 3 points on every line

# ---------------------------------------------------------------------------
# The claim, transcribed exactly as handed to the verifier.
# ---------------------------------------------------------------------------
CLAIM = {
    "counts": {0: 1, 1: 13, 2: 78, 3: 286, 4: 702, 5: 1170, 6: 1248,
               7: 702, 8: 117, 9: 13},
    "grundy": {0: 1, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1, 9: 0},
    "total": 4330,
    "g0": 2184,
    "g1": 2146,
    "max_safe_size": 9,
    "triangles": 234,
    "collinear_triples": 52,
    "cone_triangle": 260,
    "cone_collinear": 214,
    # T_m(g): safe supersets of a fixed non-collinear triple ({0,1,4}).
    "T": {3: {0: 1}, 4: {1: 10}, 5: {0: 42}, 6: {1: 90},
          7: {0: 89}, 8: {1: 24}, 9: {0: 4}},
    # U_m(g): safe supersets of a fixed collinear triple ({0,1,2}).
    "U": {3: {0: 1}, 4: {1: 9}, 5: {0: 36}, 6: {1: 75},
          7: {0: 72}, 8: {1: 18}, 9: {0: 3}},
}

checks: list[dict] = []
failures: list[str] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    checks.append({"check": name, "ok": bool(ok), "detail": detail})
    if not ok:
        failures.append(f"{name}: {detail}")
    print(("PASS  " if ok else "FAIL  ") + name + (f"  [{detail}]" if detail else ""))


def main() -> int:
    # =====================================================================
    # 1. Board: parse and verify the PG(2,3) axioms.
    # =====================================================================
    print("\n== 1. Board verification ==")
    text = BOARD.read_text(encoding="utf-8")
    rows = [ln.strip() for ln in text.splitlines() if ln.strip()]
    header = rows[0].split()
    n, nb = int(header[0]), int(header[1])
    data_rows = [ln.split() for ln in rows[1:]]
    record("board has exactly 14 non-empty lines (header + 13 lines)",
           len(rows) == 14, str(len(rows)))
    record("every data row starts with 4 and has 5 tokens",
           all(len(r) == 5 and r[0] == "4" for r in data_rows))
    raw_lines: list[list[int]] = []
    for r in data_rows:
        vals = [int(v) for v in r]
        raw_lines.append(vals[1:])

    record("board header is '13 13'", header == ["13", "13"], str(header))
    record("n = 13 points", n == 13, str(n))
    record("number of line rows = 13", len(raw_lines) == 13 and nb == 13,
           f"{len(raw_lines)} rows, header b={nb}")
    record("every line row lists exactly 4 points",
           all(len(L) == 4 for L in raw_lines),
           str(sorted(Counter(len(L) for L in raw_lines).items())))
    record("points inside every line are distinct",
           all(len(set(L)) == 4 for L in raw_lines))
    record("all point labels are in 0..12",
           all(0 <= p < n for L in raw_lines for p in L))
    board_lines = [frozenset(L) for L in raw_lines]
    record("the 13 lines are pairwise distinct",
           len(set(board_lines)) == 13, f"{len(set(board_lines))} distinct")

    degrees = Counter(p for L in raw_lines for p in L)
    record("every point lies on exactly 4 lines",
           all(degrees[p] == 4 for p in range(n)),
           str(sorted(degrees.items())))

    pair_count: Counter[tuple[int, int]] = Counter()
    for L in raw_lines:
        for a, b in itertools.combinations(sorted(L), 2):
            pair_count[(a, b)] += 1
    all_pairs = list(itertools.combinations(range(n), 2))
    record("every pair of points lies on exactly one line",
           len(pair_count) == math.comb(n, 2)
           and all(pair_count.get(pr, 0) == 1 for pr in all_pairs),
           f"{len(pair_count)} pairs of C(13,2)={math.comb(n, 2)}")
    inter = Counter(
        len(set(raw_lines[i]) & set(raw_lines[j]))
        for i, j in itertools.combinations(range(nb), 2)
    )
    record("every pair of lines meets in exactly one point",
           set(inter) == {1}, str(dict(inter)))

    line_masks = []
    for L in raw_lines:
        m = 0
        for p in L:
            m |= 1 << p
        line_masks.append(m)
    point_lines: list[list[int]] = [[] for _ in range(n)]
    for ci, m in enumerate(line_masks):
        for p in range(n):
            if (m >> p) & 1:
                point_lines[p].append(ci)

    # Explicit F_3^3 coordinate model: exhibits the board as PG(2,3), not just
    # "a projective plane of order 3".
    coords: dict[int, tuple[int, int, int]] = {}
    for idx, p in enumerate(range(4, 13)):
        coords[p] = (idx % 3, idx // 3, 1)  # x = p mod 3, y = (p-4)//3
    coords[0] = (1, 0, 0)  # direction of y = const rows
    coords[1] = (0, 1, 0)  # direction of x = const columns
    coords[2] = (1, 1, 0)  # direction of y = x diagonals
    coords[3] = (1, 2, 0)  # direction of x + y = const diagonals

    record("explicit model: the 13 coordinates are 13 distinct projective points",
           len(set(coords.values())) == 13, str(sorted(coords.items())))

    def canon3(v: tuple[int, int, int]) -> tuple[int, int, int]:
        v = tuple(x % 3 for x in v)
        for x in v:
            if x:
                inv = 1 if x == 1 else 2
                return tuple((y * inv) % 3 for y in v)
        raise ValueError("zero vector")

    forms = sorted({canon3(v) for v in itertools.product(range(3), repeat=3)
                    if any(v)})
    standard_lines = set()
    for a, b, c in forms:
        pts = frozenset(
            p for p in range(n)
            if (a * coords[p][0] + b * coords[p][1] + c * coords[p][2]) % 3 == 0
        )
        standard_lines.add(pts)
    record("explicit model: exactly 13 projective lines of 4 points",
           len(standard_lines) == 13 and all(len(L) == 4 for L in standard_lines),
           str(sorted(len(L) for L in standard_lines)))
    record("explicit F_3^3 model reproduces exactly the 13 board lines",
           standard_lines == set(board_lines),
           "mismatched lines: "
           + str(sorted(map(sorted, standard_lines ^ set(board_lines)))))

    # =====================================================================
    # 2. Exhaustive enumeration of all 2**13 subsets and safety test.
    # =====================================================================
    print("\n== 2. Exhaustive safety census ==")
    ALL = 1 << n
    FULL = ALL - 1
    safe = bytearray(ALL)
    safe_by_size: dict[int, list[int]] = defaultdict(list)
    for mask in range(ALL):
        ok = True
        for lm in line_masks:
            if (mask & lm).bit_count() > S:
                ok = False
                break
        if ok:
            safe[mask] = 1
            safe_by_size[mask.bit_count()].append(mask)
    safe_masks = [m for m in range(ALL) if safe[m]]

    counts = {k: len(safe_by_size.get(k, [])) for k in range(n + 1)}
    record("total number of subsets tested is 2**13 = 8192",
           ALL == 8192, str(ALL))
    for k in range(10):
        record(f"k={k}: safe count {counts[k]} equals claim {CLAIM['counts'][k]}",
               counts[k] == CLAIM["counts"][k],
               f"{counts[k]} vs {CLAIM['counts'][k]}")
    for k in range(10, n + 1):
        record(f"k={k}: no safe sets (max safe size is 9)", counts[k] == 0,
               str(counts[k]))
    record("no safe 10-set exists (hence max safe size = 9)",
           counts[10] == 0, str(counts[10]))
    record("total safe sets 4330",
           len(safe_masks) == CLAIM["total"],
           f"{len(safe_masks)} vs {CLAIM['total']}")
    record("sum of per-size counts equals total",
           sum(counts.values()) == len(safe_masks), str(sum(counts.values())))

    # Structural characterisations that follow from the line structure and are
    # checked directly against the census.
    record("all 9-sets are exactly the complements of the 13 lines",
           set(safe_by_size[9]) == {FULL ^ lm for lm in line_masks},
           f"{len(safe_by_size[9])} nine-sets")
    expected8 = set()
    for lm in line_masks:
        comp = FULL ^ lm
        for q in range(n):
            if (comp >> q) & 1:
                expected8.add(comp & ~(1 << q))
    record("all 8-sets are exactly 'line complement minus one point' (13*9=117)",
           set(safe_by_size[8]) == expected8 and len(expected8) == 117,
           f"{len(safe_by_size[8])} eight-sets, expected {len(expected8)}")
    record("every line complement is safe",
           all(safe[FULL ^ lm] for lm in line_masks))
    record("every line itself is unsafe (4 points on a line)",
           all(not safe[lm] for lm in line_masks))
    record("the 13 unsafe 4-sets are exactly the 13 lines",
           set(m for m in range(ALL) if m.bit_count() == 4 and not safe[m])
           == set(line_masks))

    # Double-counting cross-checks of the size counts (inclusion-exclusion).
    record("k=4 count = C(13,4) - 13",
           counts[4] == math.comb(13, 4) - 13,
           f"{counts[4]} vs {math.comb(13, 4) - 13}")
    record("k=5 count = C(13,5) - 13*9",
           counts[5] == math.comb(13, 5) - 13 * 9,
           f"{counts[5]} vs {math.comb(13, 5) - 13 * 9}")
    record("k=6 count = C(13,6) - 13*C(9,2)",
           counts[6] == math.comb(13, 6) - 13 * math.comb(9, 2),
           f"{counts[6]} vs {math.comb(13, 6) - 13 * math.comb(9, 2)}")
    record("k=7 count = C(13,7) - 13*C(9,3) + C(13,2)",
           counts[7] == math.comb(13, 7) - 13 * math.comb(9, 3) + math.comb(13, 2),
           f"{counts[7]} vs {math.comb(13, 7) - 13 * math.comb(9, 3) + math.comb(13, 2)}")

    # Independent DFS enumeration from the empty set (second algorithm).
    def enumerate_dfs() -> set[int]:
        seen: set[int] = set()

        def rec(mask: int) -> None:
            if mask in seen:
                return
            seen.add(mask)
            for p in range(n):
                if not ((mask >> p) & 1) and safe[mask | (1 << p)]:
                    rec(mask | (1 << p))

        rec(0)
        return seen

    dfs_sets = enumerate_dfs()
    record("DFS from the empty set enumerates exactly the same safe sets",
           dfs_sets == set(safe_masks), f"{len(dfs_sets)} sets")

    # =====================================================================
    # 3. Full bottom-up Grundy DP over every safe position.
    # =====================================================================
    print("\n== 3. Full Grundy DP ==")
    grundy = [-1] * ALL
    for k in range(n, -1, -1):
        for mask in safe_by_size.get(k, []):
            opts = set()
            for p in range(n):
                if not ((mask >> p) & 1):
                    nm = mask | (1 << p)
                    if safe[nm]:
                        opts.add(grundy[nm])
            v = 0
            while v in opts:
                v += 1
            grundy[mask] = v

    record("Grundy values computed for every safe position",
           all(grundy[m] >= 0 for m in safe_masks))
    record("only Grundy values 0 and 1 occur",
           set(grundy[m] for m in safe_masks) <= {0, 1},
           str(sorted(set(grundy[m] for m in safe_masks))))

    grundy_dist: dict[int, dict[int, int]] = {}
    for k in range(n + 1):
        masks = safe_by_size.get(k, [])
        dist = Counter(grundy[m] for m in masks)
        grundy_dist[k] = {g: dist[g] for g in sorted(dist)}
        if k in CLAIM["counts"]:
            record(f"k={k}: all positions have G={CLAIM['grundy'][k]}",
                   set(dist) == {CLAIM["grundy"][k]},
                   f"distribution {dict(sorted(dist.items()))}")

    total_g0 = sum(1 for m in safe_masks if grundy[m] == 0)
    total_g1 = sum(1 for m in safe_masks if grundy[m] == 1)
    record("G=0 count 2184", total_g0 == CLAIM["g0"],
           f"{total_g0} vs {CLAIM['g0']}")
    record("G=1 count 2146", total_g1 == CLAIM["g1"],
           f"{total_g1} vs {CLAIM['g1']}")
    record("G0 + G1 = 4330", total_g0 + total_g1 == CLAIM["total"])

    # Option statistics per layer, and the mex chain.
    print("\n-- option statistics / mex chain --")
    layer_options: dict[int, dict] = {}
    for k in range(n + 1):
        masks = safe_by_size.get(k, [])
        if not masks:
            continue
        option_count_dist: Counter[int] = Counter()
        option_grundy_sets: Counter[frozenset[int]] = Counter()
        no_options = 0
        for m in masks:
            og = set()
            cnt = 0
            for p in range(n):
                if not ((m >> p) & 1):
                    nm = m | (1 << p)
                    if safe[nm]:
                        cnt += 1
                        og.add(grundy[nm])
            option_count_dist[cnt] += 1
            option_grundy_sets[frozenset(og)] += 1
            if cnt == 0:
                no_options += 1
        layer_options[k] = {
            "positions": len(masks),
            "option_count_dist": dict(sorted(option_count_dist.items())),
            "option_grundy_sets": {tuple(sorted(s)): c
                                   for s, c in option_grundy_sets.items()},
            "no_options": no_options,
            "min_options": min(option_count_dist),
            "max_options": max(option_count_dist),
        }
        print(f"k={k:2d} positions={len(masks):5d} option-counts="
              f"{dict(sorted(option_count_dist.items()))} "
              f"option-G-sets={layer_options[k]['option_grundy_sets']}")

    for k in list(range(7)) + [8]:
        expected_opt_g = (CLAIM["grundy"][k + 1],)
        record(f"mex chain k={k}: every option has G={CLAIM['grundy'][k + 1]}"
               f" (so mex is {CLAIM['grundy'][k]})",
               set(layer_options[k]["option_grundy_sets"]) == {expected_opt_g}
               and layer_options[k]["no_options"] == 0,
               str(layer_options[k]["option_grundy_sets"]))
    record("mex chain k=7: 234 terminal positions (mex of empty set = 0) and "
           "468 with both options of G=1 (mex {1} = 0); all G=0",
           layer_options[7]["option_grundy_sets"] == {(): 234, (1,): 468}
           and set(grundy_dist[7]) == {0},
           str(layer_options[7]["option_grundy_sets"]))
    record("mex chain k=9: no options (terminal), G=0",
           layer_options[9]["option_grundy_sets"] == {(): 13}
           and all(grundy[m] == 0 for m in safe_by_size[9]),
           str(layer_options[9]["option_grundy_sets"]))

    # Terminal positions.  There are two kinds: the 13 nine-sets (= line
    # complements) and 234 seven-sets (= triangle + free 4-arc).
    terminal_by_size: dict[int, list[int]] = {k: [] for k in range(n + 1)}
    for m in safe_masks:
        if not any(safe[m | (1 << p)] for p in range(n)
                   if not ((m >> p) & 1)):
            terminal_by_size[m.bit_count()].append(m)
    record("terminal positions: 234 of size 7 and 13 of size 9 (247 total)",
           len(terminal_by_size[7]) == 234
           and len(terminal_by_size[9]) == 13
           and sum(len(v) for v in terminal_by_size.values()) == 247,
           str({k: len(v) for k, v in terminal_by_size.items() if v}))
    record("no terminal positions of size <= 6 or of size 8",
           all(not terminal_by_size[k] for k in list(range(7)) + [8]))
    record("terminal 9-sets are exactly the complements of the 13 lines",
           set(terminal_by_size[9]) == {FULL ^ lm for lm in line_masks})
    record("every safe 8-set has exactly one legal move",
           set(layer_options[8]["option_count_dist"]) == {1},
           str(layer_options[8]["option_count_dist"]))

    # Characterise the 234 terminal 7-sets: their complements are exactly the
    # Pasch 6-sets (6 points, four 3-secant lines, each point on two of them),
    # and the terminal 7-sets are exactly T + free 4-arc over the triangles T.
    def is_pasch(mask: int) -> bool:
        if mask.bit_count() != 6:
            return False
        tri = [i for i, lm in enumerate(line_masks)
               if (mask & lm).bit_count() == 3]
        if len(tri) != 4:
            return False
        pts = [p for p in range(n) if (mask >> p) & 1]
        return all(sum(1 for i in tri if (line_masks[i] >> p) & 1) == 2
                   for p in pts)

    pasch_sets = {m for m in range(ALL) if is_pasch(m)}
    record("the 234 Pasch 6-sets are exactly the complements of the "
           "terminal 7-sets",
           len(pasch_sets) == 234
           and {FULL ^ m for m in terminal_by_size[7]} == pasch_sets,
           f"{len(pasch_sets)} Pasch sets")

    record("all 234 terminal 7-sets have G=0",
           all(grundy[m] == 0 for m in terminal_by_size[7]))
    record("the 468 non-terminal 7-sets each have exactly 2 moves, all G=1",
           layer_options[7]["option_count_dist"].get(2) == 468
           and layer_options[7]["no_options"] == 234)

    # Incidence double counting: summing the number of legal moves over all
    # safe k-sets must give (k+1) * N_{k+1}.
    for k in range(9):
        total_opts = sum(cnt * num for cnt, num
                         in layer_options[k]["option_count_dist"].items())
        record(f"incidence double count k={k}: sum of move counts = "
               f"(k+1)*N_(k+1)",
               total_opts == (k + 1) * counts[k + 1],
               f"{total_opts} vs {(k + 1) * counts[k + 1]}")

    # 4 lines in general position (no 3 concurrent) give 6 pairwise
    # intersections; these are exactly the Pasch 6-sets.
    general_position_lines = 0
    quad_point_sets = set()
    for comb in itertools.combinations(range(nb), 4):
        if not any(sum(1 for i in comb if (line_masks[i] >> p) & 1) >= 3
                   for p in range(n)):
            general_position_lines += 1
            pts = 0
            for i, j in itertools.combinations(comb, 2):
                pts |= line_masks[i] & line_masks[j]
            quad_point_sets.add(pts)
    record("234 4-line general-position sets, bijective to the Pasch 6-sets",
           general_position_lines == 234 and quad_point_sets == pasch_sets,
           f"{general_position_lines} line sets, {len(quad_point_sets)} "
           f"point sets")

    # Top-down recursion as an independent Grundy algorithm.
    @lru_cache(maxsize=None)
    def grundy_top(mask: int) -> int:
        opts = set()
        for p in range(n):
            if not ((mask >> p) & 1):
                nm = mask | (1 << p)
                if all((nm & lm).bit_count() <= S for lm in line_masks):
                    opts.add(grundy_top(nm))
        v = 0
        while v in opts:
            v += 1
        return v

    mismatches = [m for m in safe_masks if grundy_top(m) != grundy[m]]
    record("top-down recursion reproduces every bottom-up Grundy value",
           not mismatches, f"{len(mismatches)} mismatches")

    # =====================================================================
    # 4. Three-point layer: the two orbits and their Grundy values.
    # =====================================================================
    print("\n== 4. Three-point layer (3-caps) ==")
    triples = [m for m in range(ALL) if m.bit_count() == 3]
    record("there are C(13,3)=286 three-point sets", len(triples) == 286,
           str(len(triples)))
    record("every three-point set is safe (a line holds 4 points)",
           all(safe[m] for m in triples))
    collinear: list[int] = []
    triangles: list[int] = []
    bad_incidence: list[int] = []
    for t in triples:
        lines_with = [i for i, lm in enumerate(line_masks) if (t & lm) == t]
        if len(lines_with) == 1:
            collinear.append(t)
        elif len(lines_with) == 0:
            triangles.append(t)
        else:
            bad_incidence.append(t)
    record("a three-point set lies on at most one line",
           not bad_incidence, str(bad_incidence))
    record("collinear triples = 52", len(collinear) == 52, str(len(collinear)))
    record("non-collinear triples (triangles) = 234",
           len(triangles) == 234, str(len(triangles)))
    record("collinear + triangles = 286",
           len(collinear) + len(triangles) == 286)
    record("every three-point set has G=0",
           all(grundy[t] == 0 for t in triples),
           str(sorted(set(grundy[t] for t in triples))))

    # Terminal 7-sets are exactly T + free 4-arc over the 234 triangles T,
    # i.e. complements of the 6 side points of T (a Pasch configuration).
    def side_points(triangle: int) -> int:
        pts = [p for p in range(n) if (triangle >> p) & 1]
        union = 0
        for a, b in itertools.combinations(pts, 2):
            for lm in line_masks:
                if ((lm >> a) & 1) and ((lm >> b) & 1):
                    union |= lm
                    break
        return union & ~triangle

    triangle_terminal = {FULL ^ side_points(t) for t in triangles}
    record("terminal 7-sets are exactly 'triangle + free 4-arc' (one per "
           "triangle)",
           triangle_terminal == set(terminal_by_size[7])
           and len(triangle_terminal) == 234
           and all(m.bit_count() == 7 for m in triangle_terminal),
           f"{len(triangle_terminal)} distinct terminal 7-sets")

    free_arc_bad = 0
    for t in triangles:
        pts = [p for p in range(n) if (t >> p) & 1]
        union = 0
        for a, b in itertools.combinations(pts, 2):
            for lm in line_masks:
                if ((lm >> a) & 1) and ((lm >> b) & 1):
                    union |= lm
                    break
        free = FULL & ~(union | t)
        if free.bit_count() != 4 or any(
                (free & lm).bit_count() >= 3 for lm in line_masks):
            free_arc_bad += 1
    record("for every triangle the 4 free points form a cap (no 3 collinear)",
           free_arc_bad == 0, f"{free_arc_bad} failures")

    # =====================================================================
    # 5. Cones of one representative of each orbit; orbit uniformity.
    # =====================================================================
    print("\n== 5. Cones, T/U tables and double counting ==")

    def cone_hist(f: int) -> tuple[Counter[tuple[int, int]], list[int]]:
        hist: Counter[tuple[int, int]] = Counter()
        members: list[int] = []
        for s in safe_masks:
            if (s & f) == f:
                hist[(s.bit_count(), grundy[s])] += 1
                members.append(s)
        return hist, members

    tri_rep = sum(1 << p for p in (0, 1, 4))
    col_rep = sum(1 << p for p in (0, 1, 2))
    record("{0,1,4} is non-collinear (a triangle)", tri_rep in set(triangles))
    record("{0,1,2} is collinear", col_rep in set(collinear))
    record("G({0,1,4}) = 0", grundy[tri_rep] == 0, str(grundy[tri_rep]))
    record("G({0,1,2}) = 0", grundy[col_rep] == 0, str(grundy[col_rep]))

    h_tri, mem_tri = cone_hist(tri_rep)
    h_col, mem_col = cone_hist(col_rep)
    record("triangle {0,1,4} cone has 260 positions",
           len(mem_tri) == CLAIM["cone_triangle"],
           f"{len(mem_tri)} vs {CLAIM['cone_triangle']}")
    record("collinear {0,1,2} cone has 214 positions",
           len(mem_col) == CLAIM["cone_collinear"],
           f"{len(mem_col)} vs {CLAIM['cone_collinear']}")

    claim_T_hist = Counter({(m, g): c for m, d in CLAIM["T"].items()
                            for g, c in d.items()})
    claim_U_hist = Counter({(m, g): c for m, d in CLAIM["U"].items()
                            for g, c in d.items()})
    record("triangle cone size/G histogram equals the claimed T table",
           h_tri == claim_T_hist,
           f"computed {dict(sorted(h_tri.items()))}")
    record("collinear cone size/G histogram equals the claimed U table",
           h_col == claim_U_hist,
           f"computed {dict(sorted(h_col.items()))}")

    # The same histogram for *every* triple of each orbit (orbit uniformity).
    tri_hist_ok = all(cone_hist(t)[0] == h_tri for t in triangles)
    col_hist_ok = all(cone_hist(t)[0] == h_col for t in collinear)
    record("all 234 triangles have the same cone size/G histogram",
           tri_hist_ok)
    record("all 52 collinear triples have the same cone size/G histogram",
           col_hist_ok)

    # Independent DFS enumeration of the two cones and a cone-local DP.
    def cone_dfs(f: int) -> set[int]:
        seen = {f}
        stack = [f]
        while stack:
            m = stack.pop()
            for p in range(n):
                if not ((m >> p) & 1):
                    nm = m | (1 << p)
                    if safe[nm] and nm not in seen:
                        seen.add(nm)
                        stack.append(nm)
        return seen

    def cone_local_g(f: int) -> dict[int, int]:
        members = cone_dfs(f)
        lg: dict[int, int] = {}
        for m in sorted(members, key=lambda x: -x.bit_count()):
            opts = set()
            for p in range(n):
                if not ((m >> p) & 1):
                    nm = m | (1 << p)
                    if nm in members:
                        opts.add(lg[nm])
            v = 0
            while v in opts:
                v += 1
            lg[m] = v
        return lg

    dfs_tri = cone_dfs(tri_rep)
    dfs_col = cone_dfs(col_rep)
    record("DFS cone enumeration for {0,1,4} matches the filter census",
           dfs_tri == set(mem_tri), f"{len(dfs_tri)} positions")
    record("DFS cone enumeration for {0,1,2} matches the filter census",
           dfs_col == set(mem_col), f"{len(dfs_col)} positions")
    lg_tri = cone_local_g(tri_rep)
    lg_col = cone_local_g(col_rep)
    record("cone-local DP on {0,1,4} equals the global DP on all 260 positions",
           all(lg_tri[m] == grundy[m] for m in mem_tri))
    record("cone-local DP on {0,1,2} equals the global DP on all 214 positions",
           all(lg_col[m] == grundy[m] for m in mem_col))

    # T/U table transcription and the double-count identity.
    T: dict[int, dict[int, int]] = {}
    U: dict[int, dict[int, int]] = {}
    for m in range(3, 10):
        T[m] = {g: h_tri.get((m, g), 0) for g in (0, 1)}
        U[m] = {g: h_col.get((m, g), 0) for g in (0, 1)}
    T_nonzero = {m: {g: c for g, c in T[m].items() if c} for m in T}
    U_nonzero = {m: {g: c for g, c in U[m].items() if c} for m in U}
    record("T_m table matches the claim",
           T_nonzero == CLAIM["T"], f"computed {T_nonzero}")
    record("U_m table matches the claim",
           U_nonzero == CLAIM["U"], f"computed {U_nonzero}")
    record("sum over m of T_m = 260", sum(sum(T[m].values()) for m in T) == 260)
    record("sum over m of U_m = 214", sum(sum(U[m].values()) for m in U) == 214)

    print("\n-- double-count table: 234*T_m(g) + 52*U_m(g) = C(m,3)*N_m(g) --")
    identity_rows = []
    for m in range(3, 10):
        Nm = Counter(grundy[s] for s in safe_by_size[m])
        for g in (0, 1):
            lhs = 234 * T[m][g] + 52 * U[m][g]
            rhs = math.comb(m, 3) * Nm[g]
            row = {"m": m, "g": g, "T_m_g": T[m][g], "U_m_g": U[m][g],
                   "N_m_g": Nm[g], "lhs": lhs, "rhs": rhs, "ok": lhs == rhs}
            identity_rows.append(row)
            record(f"double count m={m}, g={g}: 234*{T[m][g]} + 52*{U[m][g]}"
                   f" = C({m},3)*{Nm[g]}",
                   lhs == rhs, f"{lhs} vs {rhs}")
            print(f"m={m} g={g}: T={T[m][g]:3d} U={U[m][g]:3d} "
                  f"LHS={lhs:5d}  C(m,3)={math.comb(m,3):2d} N={Nm[g]:4d} "
                  f"RHS={rhs:5d}")
    total_pairs_lhs = 234 * 260 + 52 * 214
    total_pairs_rhs = sum(math.comb(m, 3) * len(safe_by_size[m])
                          for m in range(3, 10))
    record("total double count 234*260 + 52*214 = sum_m C(m,3)*N_m",
           total_pairs_lhs == total_pairs_rhs,
           f"{total_pairs_lhs} vs {total_pairs_rhs}")

    # =====================================================================
    # 5b. Cross-check the claim's own output artifact, if present.
    # =====================================================================
    claim_artifact_path = (
        REPO / "research" / "experiments" / "pg2q3-s3-20261128" / "output"
        / "pg2q3_s3_spectrum.json"
    )
    artifact_ok = None
    if claim_artifact_path.exists():
        art = json.loads(claim_artifact_path.read_text(encoding="utf-8"))
        record("claim artifact: cone_triangle = 260",
               art.get("cone_triangle") == 260, str(art.get("cone_triangle")))
        record("claim artifact: cone_collinear = 214",
               art.get("cone_collinear") == 214, str(art.get("cone_collinear")))
        record("claim artifact: G3 = 0", art.get("G3") == 0,
               str(art.get("G3")))
        artifact_ok = True
        art_detail: list[str] = []

        def art_bad(msg: str) -> None:
            nonlocal artifact_ok
            artifact_ok = False
            art_detail.append(msg)

        for m in range(10):
            entry = art["sizes"].get(str(m))
            if entry is None:
                art_bad(f"m={m} missing")
                continue
            if entry["N"] != counts[m]:
                art_bad(f"m={m} N {entry['N']} != {counts[m]}")
            n_g = {int(g): c for g, c in entry["N_g"].items()}
            if n_g != grundy_dist[m]:
                art_bad(f"m={m} N_g {n_g} != {grundy_dist[m]}")
            if m >= 3:
                t_g = {int(g): c for g, c in entry["T_g"].items()}
                u_g = {int(g): c for g, c in entry["U_g"].items()}
                comp_t = {g: c for g, c in T[m].items() if c}
                comp_u = {g: c for g, c in U[m].items() if c}
                if entry["T"] != sum(t_g.values()):
                    art_bad(f"m={m} T total")
                if entry["U"] != sum(u_g.values()):
                    art_bad(f"m={m} U total")
                if t_g != comp_t:
                    art_bad(f"m={m} T_g {t_g} != {comp_t}")
                if u_g != comp_u:
                    art_bad(f"m={m} U_g {u_g} != {comp_u}")
        record("claim artifact agrees with the independent census in every field",
               artifact_ok, "; ".join(art_detail) if art_detail else "all fields")
    else:
        print("claim artifact not found; cross-check skipped")

    # =====================================================================
    # 6. Summary.
    # =====================================================================
    print("\n== 6. Summary ==")
    print(f"{'k':>2} {'safe':>6} {'G':>3} {'claim':>6} {'match':>5}")
    for k in range(10):
        ok = (counts[k] == CLAIM["counts"][k]
              and set(grundy_dist[k]) == {CLAIM["grundy"][k]})
        print(f"{k:>2} {counts[k]:>6} {CLAIM['grundy'][k]:>3} "
              f"{CLAIM['counts'][k]:>6} {str(ok):>5}")
    print(f"total {len(safe_masks)} (G0={total_g0}, G1={total_g1})")
    print(f"\n{len(checks) - len(failures)}/{len(checks)} checks passed")

    out = {
        "board": str(BOARD),
        "n": n,
        "line_count": nb,
        "counts": {str(k): counts[k] for k in range(n + 1)},
        "grundy_dist": {str(k): {str(g): c for g, c in v.items()}
                        for k, v in grundy_dist.items()},
        "total_safe": len(safe_masks),
        "max_safe_size": max(k for k, v in safe_by_size.items() if v),
        "total_g0": total_g0,
        "total_g1": total_g1,
        "triangles": len(triangles),
        "collinear_triples": len(collinear),
        "cone_triangle": len(mem_tri),
        "cone_collinear": len(mem_col),
        "T": {str(m): {str(g): c for g, c in T[m].items()} for m in T},
        "U": {str(m): {str(g): c for g, c in U[m].items()} for m in U},
        "identity": identity_rows,
        "layer_options": {
            str(k): {
                **{kk: vv for kk, vv in v.items()
                   if kk != "option_grundy_sets"},
                "option_grundy_sets": {
                    ",".join(str(x) for x in s) if s else "(none)": c
                    for s, c in v["option_grundy_sets"].items()
                },
            }
            for k, v in layer_options.items()
        },
        "terminal": {
            "total": sum(len(v) for v in terminal_by_size.values()),
            "by_size": {str(k): len(v) for k, v in terminal_by_size.items() if v},
            "characterisation_7": "complement is a Pasch 6-set; "
                                  "equivalently triangle + its free 4-arc",
            "characterisation_9": "complement of a board line",
        },
        "claim_artifact": {
            "path": str(claim_artifact_path),
            "present": claim_artifact_path.exists(),
            "match": artifact_ok,
        },
        "checks": checks,
        "failures": failures,
        "verdict": "PASS" if not failures else "FAIL",
    }
    (HERE / "verification.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nWrote {HERE / 'verification.json'}")
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(" -", f)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

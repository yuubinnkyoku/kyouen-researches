"""Task 1 - verify the board is PG(2,9) and that the claimed coordinate map is
consistent with it."""
import json
import sys

import gf9 as F
import pg9 as P

BOARD = "../output/board_pg2q9.txt"
OUT = "results_task1.json"


def p_map(idx, label):
    """Claimed coordinate map; `label` (9 entries) maps board index 0..8 to a
    canonical gf9 label."""
    if idx == 0:
        return (0, 0, 1)
    if idx <= 9:
        return (0, 1, label[idx - 1])
    p, j = divmod(idx - 10, 9)
    return (1, label[p], label[j])


def main():
    res = {}
    npoints, nlines, rows = F.load_board(BOARD)
    res["header"] = {"n_points": npoints, "n_lines": nlines}
    res["gf9_field_checks"] = F.field_checks()

    # ---- abstract incidence axioms of the board -------------------------
    ok = True
    notes = []
    if npoints != 91 or nlines != 91:
        ok = False
        notes.append("header is not 91 91")
    sets = [frozenset(r) for r in rows]
    if any(len(r) != 10 for r in rows):
        ok = False
        notes.append("some row does not have 10 points")
    if len(sets) != 91:
        ok = False
        notes.append("rows not distinct")
    if any(max(r) > 90 or min(r) < 0 for r in rows):
        ok = False
        notes.append("row contains out-of-range point")

    # every point on exactly 10 lines
    deg = [0] * 91
    for r in rows:
        for p in r:
            deg[p] += 1
    if set(deg) != {10}:
        ok = False
        notes.append("point degrees %s" % sorted(set(deg)))

    # every unordered point pair on a unique line
    pair_line = {}
    multi = 0
    for li, r in enumerate(sets):
        rr = sorted(r)
        for a in range(10):
            for b in range(a + 1, 10):
                key = (rr[a], rr[b])
                if key in pair_line:
                    multi += 1
                pair_line[key] = li
    npairs = 91 * 90 // 2
    if len(pair_line) != npairs or multi != 0:
        ok = False
        notes.append("point pairs: %d unique, %d repeats (expected %d, 0)"
                     % (len(pair_line), multi, npairs))

    # every unordered line pair meets in a unique point
    line_pair_pts = set()
    dup = 0
    for i in range(91):
        for j in range(i + 1, 91):
            inter = sets[i] & sets[j]
            if len(inter) != 1:
                ok = False
                notes.append("lines %d,%d meet in %d points" % (i, j, len(inter)))
            else:
                line_pair_pts.add((i, j, next(iter(inter))))
    res["abstract_incidence"] = {
        "ok": ok, "notes": notes[:10],
        "point_degree_all_10": set(deg) == {10},
        "pairs_on_unique_line": len(pair_line) == npairs and multi == 0,
        "line_pairs_meet_in_one_point": len(line_pair_pts) == npairs,
    }

    # ---- coordinate map --------------------------------------------------
    points = P.POINTS
    lines = P.LINES
    line_masks = P.LINE_MASKS
    line_set = set(lines)
    linelab = {ln: i for i, ln in enumerate(lines)}

    candidates = {
        "literal: index k is the element with (a,b)=(k%3,k//3), label a+3b": list(range(9)),
        "index k is the element with (a,b)=(k//3,k%3), label a+3b": [P.phi(k) for k in range(9)],
        "literal + Frobenius": [F.cube(k) for k in range(9)],
        "digit pair + Frobenius": [F.cube(P.phi(k)) for k in range(9)],
    }
    coord = {}
    for name, label in candidates.items():
        vecs = [p_map(i, label) for i in range(91)]
        bij = sorted(label) == list(range(9)) and len(set(vecs)) == 91
        row_as_line = 0
        row_lines = []
        for r in rows:
            vs = [vecs[i] for i in r]
            coll = all(F.det3(vs[0], vs[1], v) == 0 for v in vs[2:])
            if coll:
                row_as_line += 1
                row_lines.append(frozenset(P.LABEL[v] for v in vs))
        # also: are the rows exactly the set of all 91 abstract lines?
        exact = len(set(row_lines)) == 91 and set(row_lines) == line_set
        coord[name] = {"bijection": bij, "rows_that_are_lines": row_as_line,
                       "distinct_lines": len(set(row_lines)),
                       "rows_equal_full_line_set": exact}
    res["coordinate_map_candidates"] = coord

    # the working labelling: explicit line-equation check for every row
    label = [P.phi(k) for k in range(9)]
    vecs = [p_map(i, label) for i in range(91)]
    per_row = []
    for r in rows:
        vs = [vecs[i] for i in r]
        per_row.append(all(F.det3(vs[0], vs[1], v) == 0 for v in vs[2:]))
    res["coordinate_map_working"] = {
        "labelling": "board index k <-> GF(9) element a+b*i, (a,b)=(k//3,k%3)",
        "all_91_rows_are_lines": all(per_row),
        "constant_one": {"index_label": 3, "canonical_label": 1,
                         "note": "the field element (1,0)=1 is board index 3 "
                                 "under the (a,b)=(k//3,k%3) convention"},
        "i_element": {"index_label": 1, "canonical_label": 3},
    }

    # explicit examples to show the failure of the literal reading
    lit = list(range(9))
    vecs_lit = [p_map(i, lit) for i in range(91)]
    bad = []
    for ri, r in enumerate(rows):
        vs = [vecs_lit[i] for i in r]
        if not all(F.det3(vs[0], vs[1], v) == 0 for v in vs[2:]):
            bad.append(ri)
    res["literal_reading_failures"] = {
        "first_bad_rows": bad[:5], "count": len(bad),
        "example_row": rows[bad[0]] if bad else None,
    }

    # ---- explicit field element identities on the working labelling -----
    # i has board index 1; i^2 = -1 = 2 -> index of 2 is (2%3,2//3)=(2,0) -> 2
    checks = {
        "i_squared_is_minus_one": F.MUL[P.phi(1)][P.phi(1)] == P.phi(6),
        "one_is_index_3": P.phi(3) == 1,
        "two_is_index_6": P.phi(6) == 2,
        "minus_one_equals_two": F.NEG[1] == 2,
    }
    res["element_identities"] = checks

    res["pass"] = (res["abstract_incidence"]["ok"]
                   and coord["index k is the element with (a,b)=(k//3,k%3), label a+3b"][
                       "rows_equal_full_line_set"]
                   and all(per_row)
                   and all(checks.values()))
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))
    print("\nTASK1:", "PASS" if res["pass"] else "FAIL")


main()
